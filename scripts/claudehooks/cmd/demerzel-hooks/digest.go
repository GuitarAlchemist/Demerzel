package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"io/fs"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
	"time"
)

// The digest hooks keep state/digests/latest.md: a nudge when it goes stale, a metadata stub
// after enough activity, at Stop and before a compaction, and its injection at SessionStart.
// Karpathy R1+R4, Cherny's session continuity (see .claude/skills/digest/SKILL.md). The writer
// below is the hooks' half of DigestState.psm1's Write-Digest; the module itself stays, because
// the /digest skill writes through it.

type digestPaths struct {
	dir, archive, latest string
}

func digestsOf(root string) digestPaths {
	dir := filepath.Join(root, "state", "digests")
	return digestPaths{dir, filepath.Join(dir, "archive"), filepath.Join(dir, "latest.md")}
}

// The counters' file names, kept from DigestState so an in-flight session's counts carry over.
const (
	counterActivity   = ".activity-counter"   // staleness nudge; reset only by /digest
	counterMid        = ".activity-count"     // mid-session auto-digest gate
	counterCorrection = ".correction-counter" // /correct throttle
)

// readCounter is Get-Counter: the file's whole number (`^\d+$` once trimmed), 0 otherwise.
func readCounter(root, name string) int {
	raw, err := os.ReadFile(filepath.Join(digestsOf(root).dir, name))
	if err != nil {
		return 0
	}
	s := strings.TrimSpace(strings.TrimPrefix(string(raw), bom))
	if s == "" || strings.Trim(s, "0123456789") != "" || len(s) > 9 {
		return 0
	}
	n, _ := strconv.Atoi(s)
	return n
}

// stepCounter is Step-Counter: increment, persist (best effort, as Set-Content under
// ErrorAction SilentlyContinue), return the new value.
func stepCounter(root, name string) int {
	dir := digestsOf(root).dir
	_ = os.MkdirAll(dir, 0o755) // a failure only loses the count
	next := readCounter(root, name) + 1
	_ = writeText(filepath.Join(dir, name), strconv.Itoa(next))
	return next
}

// resetCounter is Reset-Counter: 0 when the file exists, nothing otherwise.
func resetCounter(root, name string) {
	path := filepath.Join(digestsOf(root).dir, name)
	if _, err := os.Stat(path); err == nil {
		_ = writeText(path, "0")
	}
}

// formatYAML is Format-Yaml: a single-quoted YAML scalar, line breaks as spaces, cut to max
// characters with "..." appended, quotes doubled; null when empty.
func formatYAML(v string, max int) string {
	if v == "" {
		return "null"
	}
	c := []rune(strings.NewReplacer("\r", " ", "\n", " ").Replace(v))
	s := string(c)
	if len(c) > max {
		s = string(c[:max]) + "..."
	}
	return "'" + strings.ReplaceAll(s, "'", "''") + "'"
}

var safeIDChars = regexp.MustCompile(`^[A-Za-z0-9._-]+$`)

// formatYAMLID is Format-YamlId: v stripped of CR, LF and tabs and cut to max characters when it
// is then a plain identifier, fallback otherwise (no path traversal in a file name).
func formatYAMLID(v, fallback string, max int) string {
	if v == "" {
		return fallback
	}
	c := []rune(strings.NewReplacer("\r", "", "\n", "", "\t", "").Replace(v))
	if len(c) > max {
		c = c[:max]
	}
	if !safeIDChars.MatchString(string(c)) {
		return fallback
	}
	return string(c)
}

// repoFacts is Get-RepoFacts: HEAD's branch, short sha and subject, "" when git prints nothing,
// and the branch's pull request as "#<n>", "" without gh or without one.
type repoFacts struct {
	branch, sha, subject, openPR string
}

func (e *env) repoFacts(root string) repoFacts {
	return repoFacts{
		branch:  e.git(root, "rev-parse", "--abbrev-ref", "HEAD"),
		sha:     e.git(root, "rev-parse", "--short", "HEAD"),
		subject: e.git(root, "log", "-1", "--format=%s"),
		openPR:  e.openPR(root),
	}
}

func (e *env) openPR(root string) string {
	out, ok := e.sys.output(root, "gh", "pr", "view", "--json", "number")
	if !ok || strings.TrimSpace(out) == "" {
		return ""
	}
	var v struct {
		Number json.Number `json:"number"`
	}
	if json.Unmarshal([]byte(out), &v) != nil || v.Number == "" {
		return ""
	}
	return "#" + v.Number.String()
}

func timestamps(now time.Time) (iso, file string) {
	now = now.UTC()
	return now.Format("2006-01-02T15:04:05Z"), now.Format("2006-01-02T15-04-05Z")
}

// kv is one frontmatter field; val is nil, an int or a string.
type kv struct {
	key string
	val any
}

// renderFrontmatter is ConvertTo-FrontmatterYaml for the scalars the hooks write: null, an
// integer as it is, an empty string as two single quotes, anything else through formatYAML.
func renderFrontmatter(fields []kv) string {
	lines := []string{"---"}
	for _, f := range fields {
		switch v := f.val.(type) {
		case nil:
			lines = append(lines, f.key+": null")
		case int:
			lines = append(lines, f.key+": "+strconv.Itoa(v))
		case string:
			if v == "" {
				lines = append(lines, f.key+": ''")
			} else {
				lines = append(lines, f.key+": "+formatYAML(v, 200))
			}
		}
	}
	return strings.Join(append(lines, "---"), "\n")
}

// digestWrite is what a hook asks of writeDigest (Write-Digest's parameters the hooks used).
type digestWrite struct {
	kind         string // "digest" or "rationale"
	facts        repoFacts
	body         string
	trigger      string // digest
	sessionID    string // digest
	archiveLabel string // digest
	mutations    *int   // digest, when set
	prNumber     string // rationale
	title        string // rationale
	shortstat    string // rationale
}

// writeDigest is Write-Digest: it builds the frontmatter, rotates latest.md into the archive
// (digest kind), validates the fields against the kind's schema, writes, and resets the counters
// the trigger resets. Fail-open: an invalid frontmatter is still written, with a warning on warn.
// hook names the caller in the stderr lines.
func (e *env) writeDigest(root string, w digestWrite, hook string, warn io.Writer) {
	d := digestsOf(root)
	_ = os.MkdirAll(d.archive, 0o755) // a failure surfaces when archiving or writing
	tsIso, tsFile := timestamps(e.sys.now())
	defer func() {
		if w.kind == "digest" && w.trigger == "activity-tracker-mid-session" {
			resetCounter(root, counterMid)
		}
	}()

	var fields []kv
	var target string
	if w.kind == "digest" {
		session := w.sessionID
		if session == "" {
			session = "unknown"
		}
		var openPR any
		if w.facts.openPR != "" {
			openPR = w.facts.openPR
		}
		fields = []kv{
			{"schema_version", 1},
			{"session_id", session},
			{"written_at", tsIso},
			{"trigger", w.trigger},
			{"branch", w.facts.branch},
			{"head_sha", w.facts.sha},
			{"head_subject", w.facts.subject},
			{"open_pr", openPR},
		}
		if w.mutations != nil {
			fields = append(fields, kv{"mutations_since_last", *w.mutations})
		}
		target = d.latest
		label := w.archiveLabel
		if label == "" {
			label = w.trigger
		}
		if !archiveLatest(e, d, tsFile+"-"+formatYAMLID(label, "unknown", 64)+".md", hook) {
			return
		}
	} else {
		num := w.prNumber
		if num == "" {
			num = "unknown"
		}
		fields = []kv{
			{"schema_version", 1},
			{"trigger", "pr-rationale-capture"},
			{"captured_at", tsIso},
			{"branch", w.facts.branch},
			{"pr_number", num},
			{"diff_shortstat", w.shortstat},
		}
		target = filepath.Join(d.dir, "pr-"+num+"-"+prSlug(w.title)+".md")
	}

	verr := validateFields(root, w.kind, fields)
	text := renderFrontmatter(fields) + "\n\n" + strings.TrimLeft(w.body, "\r\n")
	if err := replaceFile(target, text); err != nil {
		fmt.Fprintf(e.stderr, "[%s] could not write %s: %v\n", hook, filepath.Base(target), err)
		return
	}
	if verr != nil {
		fmt.Fprintf(warn, "WARNING: Write-Digest: schema validation failed for %s — %v\n", target, verr)
	}
}

// archiveLatest copies latest.md into the archive before a hook replaces it, when there is one.
// On an error the caller keeps latest.md as it is rather than lose the previous digest.
func archiveLatest(e *env, d digestPaths, name, hook string) bool {
	data, err := os.ReadFile(d.latest)
	if errors.Is(err, fs.ErrNotExist) {
		return true
	}
	if err == nil {
		err = os.WriteFile(filepath.Join(d.archive, name), data, 0o644)
	}
	if err != nil {
		fmt.Fprintf(e.stderr, "[%s] could not archive latest.md, kept as it is: %v\n", hook, err)
		return false
	}
	return true
}

// replaceFile writes text (and a line break) through a temporary file and a rename, so a failed
// write never leaves the target truncated.
func replaceFile(target, text string) error {
	tmp, err := os.CreateTemp(filepath.Dir(target), ".digest-*.tmp")
	if err != nil {
		return err
	}
	_, err = tmp.WriteString(text + "\n")
	if cerr := tmp.Close(); err == nil {
		err = cerr
	}
	if err == nil {
		err = os.Rename(tmp.Name(), target)
	}
	if err != nil {
		_ = os.Remove(tmp.Name()) // a leftover temporary file is harmless; err is the one reported
	}
	return err
}

// precompactDigest (PreCompact; was precompact-digest.ps1) archives latest.md under the session's
// id and, when /digest has not written it in the last 30 minutes, replaces it with a
// metadata-only fallback. Validation warnings stay silent, as the script's WarningPreference.
func precompactDigest(e *env) int {
	root := e.repoRoot()
	if root == "" {
		return 0
	}
	d := digestsOf(root)
	session := field(e.payload(), "session_id")
	if session == "" {
		session = "unknown"
	}
	safeSession := formatYAMLID(session, "unknown", 64)
	if age, ok := e.age(d.latest); ok && age.Minutes() < 30 {
		_ = os.MkdirAll(d.archive, 0o755) // a failure surfaces in archiveLatest
		_, tsFile := timestamps(e.sys.now())
		archiveLatest(e, d, tsFile+"-"+safeSession+".md", "precompact-digest")
		return 0
	}
	e.writeDigest(root, digestWrite{
		kind:         "digest",
		facts:        e.repoFacts(root),
		trigger:      "precompact-hook-fallback",
		sessionID:    session,
		archiveLabel: safeSession,
		body: `# Session digest (fallback — /digest was not invoked before compaction)

## Model-driven sections

_No ` + "`/digest`" + ` invocation was captured before this compaction. Re-orient from
` + "`git log`" + ` and the open PR. Invoke ` + "`/digest`" + ` mid-session to populate the
**Next action**, **In-flight**, **Live hypotheses**, **Open questions**, and
**Do NOT carry forward** sections before the next compaction event._`,
	}, "precompact-digest", io.Discard)
	return 0
}

// digestStalenessNudge (UserPromptSubmit; was digest-staleness-nudge.ps1) says when the digest is
// missing or has drifted; silent when it is fresh.
func digestStalenessNudge(e *env) int {
	root := e.repoRoot()
	if root == "" {
		return 0
	}
	age, exists := e.age(digestsOf(root).latest)
	ageMin := psInt(age.Minutes())
	mutations := readCounter(root, counterActivity)

	var reason string
	switch {
	case !exists:
		reason = "No session digest exists yet. Invoke /digest at your next natural breakpoint."
	case ageMin > 30 && mutations > 10:
		reason = fmt.Sprintf("Last digest %d min ago; %d mutations since. Karpathy R4: task complete != goal achieved — consider /digest to mark success criteria status.", ageMin, mutations)
	case ageMin > 90:
		reason = fmt.Sprintf("Last digest %d min ago. Session drifting — invoke /digest before the next compaction.", ageMin)
	default:
		return 0
	}
	writeContext(e.stdout, "[digest-nudge] "+reason)
	return 0
}

// digestActivityTracker (PostToolUse on Edit|Write|Bash; was digest-activity-tracker.ps1) counts
// mutations, and after DEMERZEL_DIGEST_MID_COUNT of them (20), or DEMERZEL_DIGEST_MID_MIN minutes
// (30) with at least 3, writes a metadata-only mid-session digest, so a crash or a network drop
// does not lose the session's place before Stop or PreCompact.
func digestActivityTracker(e *env) int {
	root := e.repoRoot()
	if root == "" {
		return 0
	}
	stepCounter(root, counterActivity)
	mid := stepCounter(root, counterMid)

	thresholdCount := envCount(e, "DEMERZEL_DIGEST_MID_COUNT", 20)
	thresholdMin := envCount(e, "DEMERZEL_DIGEST_MID_MIN", 30)
	ageMin := int64(99999)
	if a, ok := e.age(digestsOf(root).latest); ok {
		ageMin = psInt(a.Minutes())
	}
	if !(mid >= thresholdCount || (ageMin >= int64(thresholdMin) && mid >= 3)) {
		return 0
	}
	e.writeDigest(root, digestWrite{
		kind:         "digest",
		facts:        e.repoFacts(root),
		trigger:      "activity-tracker-mid-session",
		sessionID:    "mid-session-auto",
		archiveLabel: "pre-mid",
		mutations:    &mid,
		body: fmt.Sprintf(`# Session digest (mid-session auto — activity threshold reached)

## Model-driven sections

_Auto-written by digest-activity-tracker after %d mutations / %dm since last digest.
Invoke `+"`/digest`"+` at your next natural breakpoint to populate **Next action**,
**In-flight**, **Live hypotheses**, **Open questions**, **Do NOT carry forward**,
and **Success criteria**._`, mid, ageMin),
	}, "digest-activity-tracker", e.stderr)
	return 0
}

// digestStopFinalize (Stop; was digest-stop-finalize.ps1) writes a metadata digest when /digest
// has not written one in the last 10 minutes, archiving the previous one first.
func digestStopFinalize(e *env) int {
	root := e.repoRoot()
	if root == "" {
		return 0
	}
	if age, ok := e.age(digestsOf(root).latest); ok && age.Minutes() < 10 {
		return 0
	}
	facts := e.repoFacts(root)
	prLine := ""
	if facts.openPR != "" {
		prLine = "**Open PR:** " + facts.openPR + "\n"
	}
	e.writeDigest(root, digestWrite{
		kind:         "digest",
		facts:        facts,
		trigger:      "stop-hook-finalize",
		sessionID:    "stop-finalize",
		archiveLabel: "stop",
		body: fmt.Sprintf(`# Session digest (Stop-hook finalize — /digest not invoked in last 10 min)

**Branch:** %s @ %s — %s
%s
## Model-driven sections

_Session ended without a recent `+"`/digest`"+`. Next session: re-orient from
`+"`git log`"+` + open PR. Prior digests (if any) are in `+"`state/digests/archive/`"+`._`,
			facts.branch, facts.sha, facts.subject, prLine),
	}, "digest-stop-finalize", e.stderr)
	return 0
}
