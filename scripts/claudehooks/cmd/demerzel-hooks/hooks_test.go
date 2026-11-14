package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"
)

// fakeSystem: a repository at root (git answers from a table), no gh, a fixed clock. No network,
// no real process.
func fakeSystem(root string, now time.Time) *system {
	return &system{
		now:    func() time.Time { return now },
		getenv: func(string) string { return "" },
		output: func(dir, name string, args ...string) (string, bool) {
			key := name + " " + strings.Join(args, " ")
			switch {
			case strings.HasSuffix(key, "rev-parse --abbrev-ref HEAD"):
				return "feat/x\n", true
			case strings.HasSuffix(key, "rev-parse --short HEAD"):
				return "abc1234\n", true
			case strings.HasSuffix(key, "log -1 --format=%s"):
				return "feat: it's done\n", true
			case strings.HasSuffix(key, "diff --shortstat HEAD~1"):
				return " 2 files changed, 3 insertions(+)\n", true
			}
			return "", false
		},
		executable: func() (string, error) { return "", errors.New("no executable in tests") },
		toplevel:   func() (string, bool) { return root, root != "" },
	}
}

// withGH makes gh answer an open pull request.
func withGH(sys *system, number string) *system {
	inner := sys.output
	sys.output = func(dir, name string, args ...string) (string, bool) {
		if name == "gh" {
			return `{"number":` + number + "}\n", true
		}
		return inner(dir, name, args...)
	}
	return sys
}

// withEnv sets environment variables for a hook.
func withEnv(sys *system, vars map[string]string) *system {
	sys.getenv = func(name string) string { return vars[name] }
	return sys
}

// recording wraps sys so that every process it would start is appended to *calls.
func recording(sys *system, calls *[]string) *system {
	output := sys.output
	sys.output = func(dir, name string, args ...string) (string, bool) {
		*calls = append(*calls, name+" "+strings.Join(args, " "))
		return output(dir, name, args...)
	}
	return sys
}

func runHook(t *testing.T, sys *system, name, stdin string, args ...string) (int, string, string) {
	t.Helper()
	var out, errb bytes.Buffer
	code := dispatch(append([]string{name}, args...), &env{stdin: strings.NewReader(stdin), stdout: &out, stderr: &errb, sys: sys})
	return code, out.String(), errb.String()
}

// newRepo is a temporary repository root holding the repository's two digest schemas, which
// the writer validates against.
func newRepo(t *testing.T) string {
	t.Helper()
	root := t.TempDir()
	dst := filepath.Join(root, "docs", "contracts")
	if err := os.MkdirAll(dst, 0o755); err != nil {
		t.Fatal(err)
	}
	for _, f := range schemaFiles {
		data, err := os.ReadFile(filepath.Join("..", "..", "..", "..", filepath.FromSlash(f)))
		if err != nil {
			t.Fatal(err)
		}
		if err := os.WriteFile(filepath.Join(root, filepath.FromSlash(f)), data, 0o644); err != nil {
			t.Fatal(err)
		}
	}
	return root
}

func writeLatest(t *testing.T, root string, age time.Duration, now time.Time) string {
	t.Helper()
	d := digestsOf(root)
	if err := os.MkdirAll(d.dir, 0o755); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(d.latest, []byte("---\nschema_version: 1\ntrigger: 'digest-skill'\n---\n\nDIGEST-MARKER\n"), 0o644); err != nil {
		t.Fatal(err)
	}
	mt := now.Add(-age)
	if err := os.Chtimes(d.latest, mt, mt); err != nil {
		t.Fatal(err)
	}
	return d.latest
}

func read(t *testing.T, path string) string {
	t.Helper()
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	return string(data)
}

// The hooks that fire on every prompt or every tool call start no process when they have
// nothing to do: each one cost 1 to 2.5 s on a loaded Windows machine.
func TestHotHooksStartNoProcess(t *testing.T) {
	now := time.Date(2026, 11, 14, 12, 0, 0, 0, time.UTC)
	root := newRepo(t)
	writeLatest(t, root, 5*time.Minute, now)
	for _, c := range []struct{ hook, stdin string }{
		{"correction-detector", `{"prompt":"no, not that file"}`},
		{"digest-staleness-nudge", `{"prompt":"continue"}`},
		{"digest-activity-tracker", ""},
		{"pr-rationale-capture", `{"tool_input":{"command":"gh pr view 1"}}`},
		{"digest-stop-finalize", ""},
		{"precompact-digest", `{"session_id":"s"}`},
	} {
		var calls []string
		runHook(t, recording(fakeSystem(root, now), &calls), c.hook, c.stdin)
		if len(calls) != 0 {
			t.Errorf("%s %s started %v", c.hook, c.stdin, calls)
		}
	}
}

// The repository root is found without starting git, from a nested directory, for a checkout
// (.git directory) and a worktree (.git file).
func TestFindTopLevel(t *testing.T) {
	for _, worktree := range []bool{false, true} {
		root := t.TempDir()
		var err error
		if worktree {
			err = os.WriteFile(filepath.Join(root, ".git"), []byte("gitdir: elsewhere\n"), 0o644)
		} else {
			err = os.Mkdir(filepath.Join(root, ".git"), 0o755)
		}
		nested := filepath.Join(root, "a", "b")
		if err != nil || os.MkdirAll(nested, 0o755) != nil {
			t.Fatal("setup")
		}
		for _, from := range []string{root, nested} {
			got, ok := findTopLevel(from)
			if !ok || got != filepath.ToSlash(root) {
				t.Errorf("worktree=%v from %s: got %q %v, want %q", worktree, from, got, ok, filepath.ToSlash(root))
			}
		}
	}
}

// Every hook exits 0 and writes nothing outside a repository.
func TestOutsideARepository(t *testing.T) {
	for name := range hooks {
		code, out, _ := runHook(t, fakeSystem("", time.Now()), name, `{"prompt":"stop","session_id":"s","tool_input":{"command":"gh pr create --title x"}}`)
		if code != 0 || out != "" {
			t.Errorf("%s outside a repository: exit %d, out %q", name, code, out)
		}
	}
}

func TestCorrectionDetector(t *testing.T) {
	now := time.Now()
	fires := []string{
		"no, use the worktree",
		"No, don't amend after CI passed.",
		"Don't rewrite the README.",
		"dont touch master",
		"Stop rewriting the README.",
		"Wait, that is not what I asked.",
		"Actually we discussed this before.",
		"That's wrong, the port is 5176.",
		"thats wrong",
		"Incorrect: it is a policy.",
	}
	for _, prompt := range fires {
		root := t.TempDir() // a fresh throttle counter: the first match fires
		in, _ := json.Marshal(map[string]string{"prompt": prompt})
		code, out, _ := runHook(t, fakeSystem(root, now), "correction-detector", string(in))
		want := `{"additionalContext":"[correction-nudge] Detected correction language. Consider invoking /correct to formalize this into CLAUDE.md so the rule persists across sessions (Cherny self-improvement loop)."}` + "\n"
		if code != 0 || out != want {
			t.Errorf("fires: %q: exit %d, out %q", prompt, code, out)
		}
	}
	silent := map[string]string{
		"a request":                   `{"prompt": "Can you run the tests on Windows?"}`,
		"no as part of a word":        `{"prompt": "Nothing to change, go on."}`,
		"an opener after the start":   `{"prompt": "Thanks.\nno, not this file"}`,
		"an opener after 200 chars":   `{"prompt": "` + strings.Repeat("x", 200) + ` no"}`,
		"french is not matched":       `{"prompt": "Non, pas comme ça."}`,
		"empty prompt":                `{"prompt": ""}`,
		"empty stdin":                 ``,
		"raw text is not read":        `no, raw text`,
		"user_prompt is read, no hit": `{"user_prompt": "The build passes."}`,
	}
	for desc, in := range silent {
		root := t.TempDir()
		if code, out, _ := runHook(t, fakeSystem(root, now), "correction-detector", in); code != 0 || out != "" {
			t.Errorf("silent: %s: exit %d, out %q", desc, code, out)
		}
		if readCounter(root, counterCorrection) != 0 {
			t.Errorf("silent: %s: counted", desc)
		}
	}
	if _, out, _ := runHook(t, fakeSystem(t.TempDir(), now), "correction-detector", `{"user_prompt": "stop that"}`); out == "" {
		t.Error("user_prompt is not read")
	}
}

// Fires on the 1st match, then on every DEMERZEL_CORRECTION_THROTTLE-th (5 by default).
func TestCorrectionDetectorThrottle(t *testing.T) {
	for _, c := range []struct {
		throttle string
		want     string
	}{
		{"", "1000100001"},  // matches 1..10 with the default 5
		{"3", "1010010010"}, // 1, 3, 6, 9
		{"x", "1000100001"}, // not a number: the default
		{"0", "1000000000"}, // the first match only
	} {
		root := t.TempDir()
		sys := withEnv(fakeSystem(root, time.Now()), map[string]string{"DEMERZEL_CORRECTION_THROTTLE": c.throttle})
		got := ""
		for i := 0; i < 10; i++ {
			if _, out, _ := runHook(t, sys, "correction-detector", `{"prompt":"no"}`); out != "" {
				got += "1"
			} else {
				got += "0"
			}
		}
		if got != c.want {
			t.Errorf("throttle %q: fired %s, want %s", c.throttle, got, c.want)
		}
		if n := readCounter(root, counterCorrection); n != 10 {
			t.Errorf("throttle %q: counter %d", c.throttle, n)
		}
	}
}

func TestSessionstartDigest(t *testing.T) {
	now := time.Now()
	root := t.TempDir()
	if code, out, _ := runHook(t, fakeSystem(root, now), "sessionstart-digest", ""); code != 0 || out != "" {
		t.Errorf("no digest: %d %q", code, out)
	}
	for _, c := range []struct {
		age  time.Duration
		want string
	}{
		{5 * time.Minute, "\n=== Session digest (last written 5 min ago) ===\n---\nschema_version: 1"},
		{90 * time.Minute, "last written 1h 30m ago"},
		{23*time.Hour + 59*time.Minute, "last written 23h 59m ago"},
	} {
		writeLatest(t, root, c.age, now)
		_, out, _ := runHook(t, fakeSystem(root, now), "sessionstart-digest", `{"source":"compact"}`)
		if !strings.HasPrefix(out, "\n=== Session digest") || !strings.Contains(out, c.want) || !strings.HasSuffix(out, "DIGEST-MARKER\n\n=== End digest ===\n\n") {
			t.Errorf("age %v: %q", c.age, out)
		}
	}
	writeLatest(t, root, 25*time.Hour, now)
	if _, out, _ := runHook(t, fakeSystem(root, now), "sessionstart-digest", ""); out != "\nSession digest exists but is >24h old — skipping injection. Run /digest to refresh.\n\n" {
		t.Errorf("a day-old digest: %q", out)
	}
}

func TestSessionStartInstallsTheBinaryThenInjects(t *testing.T) {
	now := time.Now()
	root := t.TempDir()
	writeLatest(t, root, time.Minute, now)
	exe := filepath.Join(t.TempDir(), "built")
	if err := os.WriteFile(exe, []byte("v1"), 0o755); err != nil {
		t.Fatal(err)
	}
	sys := fakeSystem(root, now)
	sys.executable = func() (string, error) { return exe, nil }
	if _, out, _ := runHook(t, sys, "session-start", "{}"); !strings.Contains(out, "DIGEST-MARKER") {
		t.Errorf("digest not injected: %q", out)
	}
	if got, _ := os.ReadFile(binPath(root)); string(got) != "v1" {
		t.Fatalf("installed %q", got)
	}
	if err := os.WriteFile(exe, []byte("v2"), 0o755); err != nil {
		t.Fatal(err)
	}
	runHook(t, sys, "session-start", "{}")
	if got, _ := os.ReadFile(binPath(root)); string(got) != "v2" {
		t.Fatalf("not refreshed: %q", got)
	}
	left, _ := filepath.Glob(filepath.Join(filepath.Dir(binPath(root)), ".demerzel-hooks-*.tmp"))
	if len(left) != 0 {
		t.Fatalf("temporary files left: %v", left)
	}
	// A failed install says so and still injects the digest.
	sys.executable = func() (string, error) { return "", errors.New("gone") }
	if code, out, errs := runHook(t, sys, "session-start", "{}"); code != 0 || !strings.Contains(errs, "could not install") || !strings.Contains(out, "DIGEST-MARKER") {
		t.Errorf("failed install: %d %q %q", code, out, errs)
	}
}

func TestDigestStalenessNudge(t *testing.T) {
	now := time.Now()
	root := t.TempDir()
	d := digestsOf(root)
	nudge := func() string {
		_, out, _ := runHook(t, fakeSystem(root, now), "digest-staleness-nudge", "")
		return out
	}
	if out := nudge(); out != `{"additionalContext":"[digest-nudge] No session digest exists yet. Invoke /digest at your next natural breakpoint."}`+"\n" {
		t.Errorf("missing digest: %q", out)
	}
	writeLatest(t, root, 45*time.Minute, now)
	if out := nudge(); out != "" {
		t.Errorf("no mutations, 45 min: nudged %q", out)
	}
	if err := os.WriteFile(filepath.Join(d.dir, counterActivity), []byte("11\r\n"), 0o644); err != nil {
		t.Fatal(err)
	}
	if out := nudge(); out != `{"additionalContext":"[digest-nudge] Last digest 45 min ago; 11 mutations since. Karpathy R4: task complete != goal achieved — consider /digest to mark success criteria status."}`+"\n" {
		t.Errorf("drifted digest: %q", out)
	}
	// [int] rounds: 30.5 min reads 30 (halves to even), not over the threshold.
	writeLatest(t, root, 30*time.Minute+30*time.Second, now)
	if out := nudge(); out != "" {
		t.Errorf("30.5 min nudged: %q", out)
	}
	writeLatest(t, root, 30*time.Minute+31*time.Second, now)
	if out := nudge(); !strings.Contains(out, "Last digest 31 min ago") {
		t.Errorf("30.52 min rounds to 31: %q", out)
	}
	writeLatest(t, root, 100*time.Minute, now)
	if err := os.WriteFile(filepath.Join(d.dir, counterActivity), []byte("x"), 0o644); err != nil {
		t.Fatal(err)
	}
	if out := nudge(); !strings.Contains(out, "Last digest 100 min ago. Session drifting — invoke /digest before the next compaction.") {
		t.Errorf("old digest: %q", out)
	}
}

func TestDigestActivityTrackerWritesAStubAtTheThreshold(t *testing.T) {
	now := time.Date(2026, 11, 14, 12, 0, 0, 0, time.UTC)
	root := newRepo(t)
	writeLatest(t, root, time.Minute, now)
	sys := withGH(fakeSystem(root, now), "7")
	for i := 0; i < 19; i++ {
		runHook(t, sys, "digest-activity-tracker", "")
	}
	d := digestsOf(root)
	if !strings.Contains(read(t, d.latest), "DIGEST-MARKER") {
		t.Fatal("stub written before the threshold")
	}
	_, _, errs := runHook(t, sys, "digest-activity-tracker", "")
	data := read(t, d.latest)
	want := "---\nschema_version: 1\nsession_id: 'mid-session-auto'\nwritten_at: '2026-11-14T12:00:00Z'\ntrigger: 'activity-tracker-mid-session'\n" +
		"branch: 'feat/x'\nhead_sha: 'abc1234'\nhead_subject: 'feat: it''s done'\nopen_pr: '#7'\nmutations_since_last: 20\n---\n\n" +
		"# Session digest (mid-session auto — activity threshold reached)\n\n## Model-driven sections\n\n" +
		"_Auto-written by digest-activity-tracker after 20 mutations / 1m since last digest.\n"
	if !strings.HasPrefix(data, want) || !strings.HasSuffix(data, "and **Success criteria**._\n") {
		t.Errorf("stub:\n%s", data)
	}
	if errs != "" {
		t.Errorf("a valid stub warned: %q", errs)
	}
	if readCounter(root, counterMid) != 0 || readCounter(root, counterActivity) != 20 {
		t.Fatal("mid counter not reset, or activity counter not kept")
	}
	if !strings.Contains(read(t, filepath.Join(d.archive, "2026-11-14T12-00-00Z-pre-mid.md")), "DIGEST-MARKER") {
		t.Fatal("previous digest not archived")
	}
}

// After DEMERZEL_DIGEST_MID_MIN minutes, 3 mutations are enough; 2 are not.
func TestDigestActivityTrackerByAge(t *testing.T) {
	now := time.Date(2026, 11, 14, 12, 0, 0, 0, time.UTC)
	root := newRepo(t)
	writeLatest(t, root, 10*time.Minute, now)
	sys := withEnv(fakeSystem(root, now), map[string]string{"DEMERZEL_DIGEST_MID_MIN": "10"})
	runHook(t, sys, "digest-activity-tracker", "")
	runHook(t, sys, "digest-activity-tracker", "")
	if !strings.Contains(read(t, digestsOf(root).latest), "DIGEST-MARKER") {
		t.Fatal("stub after 2 mutations")
	}
	runHook(t, sys, "digest-activity-tracker", "")
	if data := read(t, digestsOf(root).latest); !strings.Contains(data, "after 3 mutations / 10m since last digest") || !strings.Contains(data, "open_pr: null\n") {
		t.Fatalf("no stub after 3 mutations and 10 min: %s", data)
	}
	// No digest at all reads as 99999 minutes old.
	root = newRepo(t)
	sys = fakeSystem(root, now)
	for i := 0; i < 3; i++ {
		runHook(t, sys, "digest-activity-tracker", "")
	}
	if data := read(t, digestsOf(root).latest); !strings.Contains(data, "/ 99999m since") {
		t.Fatalf("no stub without a digest: %s", data)
	}
	if left, _ := filepath.Glob(filepath.Join(digestsOf(root).archive, "*")); len(left) != 0 {
		t.Fatalf("archived a digest that did not exist: %v", left)
	}
}

func TestDigestStopFinalize(t *testing.T) {
	now := time.Date(2026, 11, 14, 12, 0, 0, 0, time.UTC)
	root := newRepo(t)
	d := digestsOf(root)
	_, _, errs := runHook(t, fakeSystem(root, now), "digest-stop-finalize", "")
	want := "---\nschema_version: 1\nsession_id: 'stop-finalize'\nwritten_at: '2026-11-14T12:00:00Z'\ntrigger: 'stop-hook-finalize'\n" +
		"branch: 'feat/x'\nhead_sha: 'abc1234'\nhead_subject: 'feat: it''s done'\nopen_pr: null\n---\n\n" +
		"# Session digest (Stop-hook finalize — /digest not invoked in last 10 min)\n\n" +
		"**Branch:** feat/x @ abc1234 — feat: it's done\n\n## Model-driven sections\n\n" +
		"_Session ended without a recent `/digest`. Next session: re-orient from\n`git log` + open PR. Prior digests (if any) are in `state/digests/archive/`._\n"
	if data := read(t, d.latest); data != want || errs != "" {
		t.Errorf("stop digest (stderr %q):\n%s", errs, data)
	}
	// Written 9 minutes ago: Stop leaves it.
	if err := os.Chtimes(d.latest, now.Add(-9*time.Minute), now.Add(-9*time.Minute)); err != nil {
		t.Fatal(err)
	}
	runHook(t, fakeSystem(root, now), "digest-stop-finalize", "")
	if _, err := os.Stat(filepath.Join(d.archive, "2026-11-14T12-00-00Z-stop.md")); err == nil {
		t.Fatal("a 9-minute-old digest was finalized")
	}
	// Eleven minutes: archived as -stop, replaced, the open pull request named.
	if err := os.Chtimes(d.latest, now.Add(-11*time.Minute), now.Add(-11*time.Minute)); err != nil {
		t.Fatal(err)
	}
	runHook(t, withGH(fakeSystem(root, now), "42"), "digest-stop-finalize", "")
	if read(t, filepath.Join(d.archive, "2026-11-14T12-00-00Z-stop.md")) != want {
		t.Error("the previous digest was not archived as -stop")
	}
	if data := read(t, d.latest); !strings.Contains(data, "open_pr: '#42'\n") || !strings.Contains(data, "feat: it's done\n**Open PR:** #42\n\n## Model-driven sections") {
		t.Errorf("open pull request not named:\n%s", data)
	}
}

func TestPrecompactDigest(t *testing.T) {
	now := time.Date(2026, 11, 14, 12, 0, 0, 0, time.UTC)
	root := newRepo(t)
	d := digestsOf(root)
	sys := withGH(fakeSystem(root, now), "42")
	// No digest yet: the fallback is written, nothing archived.
	runHook(t, sys, "precompact-digest", `{"session_id":"s-1"}`)
	want := "---\nschema_version: 1\nsession_id: 's-1'\nwritten_at: '2026-11-14T12:00:00Z'\ntrigger: 'precompact-hook-fallback'\n" +
		"branch: 'feat/x'\nhead_sha: 'abc1234'\nhead_subject: 'feat: it''s done'\nopen_pr: '#42'\n---\n\n" +
		"# Session digest (fallback — /digest was not invoked before compaction)\n\n## Model-driven sections\n\n" +
		"_No `/digest` invocation was captured before this compaction. Re-orient from\n`git log` and the open PR. Invoke `/digest` mid-session to populate the\n" +
		"**Next action**, **In-flight**, **Live hypotheses**, **Open questions**, and\n**Do NOT carry forward** sections before the next compaction event._\n"
	if data := read(t, d.latest); data != want {
		t.Errorf("fallback:\n%s", data)
	}
	// A fresh digest (under 30 minutes) is archived under the session id and kept.
	latest := writeLatest(t, root, 5*time.Minute, now)
	runHook(t, sys, "precompact-digest", `{"session_id":"../../evil"}`)
	if !strings.Contains(read(t, filepath.Join(d.archive, "2026-11-14T12-00-00Z-unknown.md")), "DIGEST-MARKER") {
		t.Fatal("a traversing session id was not replaced by 'unknown'")
	}
	if !strings.Contains(read(t, latest), "DIGEST-MARKER") {
		t.Fatal("a fresh digest was overwritten before compaction")
	}
	// A stale one is archived under the session id cut to 64, then replaced; the long id is
	// quoted and cut with "..." in the frontmatter; no session id reads 'unknown'.
	writeLatest(t, root, time.Hour, now)
	long := strings.Repeat("s", 210)
	runHook(t, sys, "precompact-digest", `{"session_id":"`+long+`"}`)
	if !strings.Contains(read(t, filepath.Join(d.archive, "2026-11-14T12-00-00Z-"+strings.Repeat("s", 64)+".md")), "DIGEST-MARKER") {
		t.Error("the archive name does not carry the session id cut to 64")
	}
	if data := read(t, d.latest); !strings.Contains(data, "session_id: '"+strings.Repeat("s", 200)+"...'\n") {
		t.Errorf("long session id:\n%s", data)
	}
	if err := os.Chtimes(d.latest, now.Add(-time.Hour), now.Add(-time.Hour)); err != nil {
		t.Fatal(err)
	}
	runHook(t, sys, "precompact-digest", "")
	if data := read(t, d.latest); !strings.Contains(data, "session_id: 'unknown'\n") {
		t.Errorf("no session id:\n%s", data)
	}
}

// When the archive cannot be written (a file where the archive directory should be), each hook
// that replaces latest.md keeps the previous digest instead of losing it, says so on stderr and
// still exits 0.
func TestAFailedArchiveKeepsTheLatestDigest(t *testing.T) {
	now := time.Date(2026, 11, 14, 12, 0, 0, 0, time.UTC)
	for _, c := range []struct{ hook, stdin string }{
		{"digest-activity-tracker", ""},
		{"digest-stop-finalize", ""},
		{"precompact-digest", `{"session_id":"s-1"}`},
	} {
		root := newRepo(t)
		latest := writeLatest(t, root, 2*time.Hour, now)
		before := read(t, latest)
		if err := os.WriteFile(digestsOf(root).archive, []byte("not a directory\n"), 0o644); err != nil {
			t.Fatal(err)
		}
		sys := withEnv(fakeSystem(root, now), map[string]string{"DEMERZEL_DIGEST_MID_COUNT": "1"})
		code, _, errs := runHook(t, sys, c.hook, c.stdin)
		if after := read(t, latest); code != 0 || before != after || !strings.Contains(errs, "could not archive latest.md, kept as it is") {
			t.Errorf("%s: exit %d, stderr %q, latest.md now %q", c.hook, code, errs, after)
		}
	}
}

// A frontmatter the schema rejects is still written (fail-open), with a warning on stderr; the
// PreCompact hook stays silent, as the script's WarningPreference.
func TestSchemaFailureWarnsButWrites(t *testing.T) {
	now := time.Date(2026, 11, 14, 12, 0, 0, 0, time.UTC)
	for _, c := range []struct {
		hook, stdin string
		warns       bool
	}{
		{"digest-stop-finalize", "", true},
		{"digest-activity-tracker", "", true},
		{"precompact-digest", `{"session_id":"s"}`, false},
	} {
		root := t.TempDir() // no schema: Test-SchemaObject reported "schema not found"
		sys := withEnv(fakeSystem(root, now), map[string]string{"DEMERZEL_DIGEST_MID_COUNT": "1"})
		code, out, errs := runHook(t, sys, c.hook, c.stdin)
		if code != 0 || out != "" || !strings.Contains(read(t, digestsOf(root).latest), "schema_version: 1") {
			t.Errorf("%s: exit %d, out %q", c.hook, code, out)
		}
		if got := strings.Contains(errs, "WARNING: Write-Digest: schema validation failed for ") && strings.Contains(errs, "schema not found"); got != c.warns {
			t.Errorf("%s: stderr %q", c.hook, errs)
		}
	}
}

func TestPRRationaleCapture(t *testing.T) {
	now := time.Date(2026, 11, 14, 12, 0, 0, 0, time.UTC)
	root := newRepo(t)
	in, _ := json.Marshal(map[string]any{
		"tool_input":    map[string]any{"command": `gh pr create --title "Fix: the Thing!" --body 'why it''s "here" matters' --base master`},
		"tool_response": map[string]any{"output": "https://github.com/o/r/pull/42\n"},
	})
	var calls []string
	_, _, errs := runHook(t, recording(fakeSystem(root, now), &calls), "pr-rationale-capture", string(in))
	want := "---\nschema_version: 1\ntrigger: 'pr-rationale-capture'\ncaptured_at: '2026-11-14T12:00:00Z'\nbranch: 'feat/x'\npr_number: '42'\n" +
		"diff_shortstat: ' 2 files changed, 3 insertions(+)'\n---\n\n# PR #42 — Fix: the Thing!\n\n## Title\n\nFix: the Thing!\n\n## Body\n\nwhy it''s \"here\" matters\n"
	if data := read(t, filepath.Join(root, "state", "digests", "pr-42-fix-the-thing.md")); data != want || errs != "" {
		t.Errorf("rationale (stderr %q):\n%s", errs, data)
	}
	for _, c := range calls {
		if strings.HasPrefix(c, "gh ") {
			t.Errorf("started gh: %s", c)
		}
	}
	// A string tool_response, a body ending the command, no number in the output, no diff.
	sys := fakeSystem(root, now)
	inner := sys.output
	sys.output = func(dir, name string, args ...string) (string, bool) {
		if strings.Contains(strings.Join(args, " "), "--shortstat") {
			return "", false
		}
		return inner(dir, name, args...)
	}
	in, _ = json.Marshal(map[string]any{
		"tool_input":    map[string]any{"command": `GH PR CREATE --title '` + strings.Repeat("ab ", 20) + `' --body "last"`},
		"tool_response": "created",
	})
	runHook(t, sys, "pr-rationale-capture", string(in))
	data := read(t, filepath.Join(root, "state", "digests", "pr-unknown-"+strings.Repeat("ab-", 13)+"a.md"))
	if !strings.Contains(data, "pr_number: 'unknown'\ndiff_shortstat: ''\n---") || !strings.HasSuffix(data, "## Body\n\nlast\n") {
		t.Fatalf("%s", data)
	}
	for _, other := range []string{`{"tool_input":{"command":"gh pr view 1"}}`, `{"tool_input":{}}`, `not json`, ``} {
		runHook(t, fakeSystem(root, now), "pr-rationale-capture", other)
	}
	if all, _ := filepath.Glob(filepath.Join(root, "state", "digests", "pr-*.md")); len(all) != 2 {
		t.Fatalf("captured a non-create command: %v", all)
	}
}

func TestPRSlugAndBody(t *testing.T) {
	for title, want := range map[string]string{
		"":                             "untitled",
		"!!!":                          "untitled",
		"Été — déjà vu":                "t-d-j-vu",
		strings.Repeat("a", 39) + " b": strings.Repeat("a", 39), // cut at 40, then the dash trimmed
	} {
		if got := prSlug(title); got != want {
			t.Errorf("prSlug(%q) = %q, want %q", title, got, want)
		}
	}
	for cmd, want := range map[string]string{
		`gh pr create --body "a" --title x`:      "a",
		`gh pr create --body "a"b" --x`:          `a"b`,
		`gh pr create --body "unterminated`:      "",
		`gh pr create --body "$(cat <<'EOF'`:     "",
		`gh pr create --body 'one' --body 'two'`: "one",
	} {
		if got := bodyFlag(cmd); got != want {
			t.Errorf("bodyFlag(%q) = %q, want %q", cmd, got, want)
		}
	}
}

// Ported from tests/powershell/DigestState.Tests.ps1 (Format-Yaml, Format-YamlId, counters).
func TestFormatYAMLAndCounters(t *testing.T) {
	for in, want := range map[string]string{
		"":     "null",
		"it's": "'it''s'",
		"a\nb": "'a b'",
		"a\rb": "'a b'",
	} {
		if got := formatYAML(in, 200); got != want {
			t.Errorf("formatYAML(%q) = %q, want %q", in, got, want)
		}
	}
	if got := formatYAML(strings.Repeat("x", 300), 10); got != "'xxxxxxxxxx...'" {
		t.Errorf("cap: %q", got)
	}
	for in, want := range map[string]string{"": "fb", "a.b_c-1": "a.b_c-1", "a\tb": "ab", "../x": "fb", "a b": "fb"} {
		if got := formatYAMLID(in, "fb", 64); got != want {
			t.Errorf("formatYAMLID(%q) = %q, want %q", in, got, want)
		}
	}
	root := t.TempDir()
	if readCounter(root, counterActivity) != 0 || stepCounter(root, counterActivity) != 1 || stepCounter(root, counterActivity) != 2 || readCounter(root, counterActivity) != 2 {
		t.Fatal("step/read")
	}
	resetCounter(root, counterActivity)
	if readCounter(root, counterActivity) != 0 {
		t.Fatal("reset")
	}
	resetCounter(root, counterMid) // absent: stays absent
	if _, err := os.Stat(filepath.Join(digestsOf(root).dir, counterMid)); err == nil {
		t.Fatal("reset created a counter")
	}
	for _, raw := range []string{bom + "7\r\n", " 7 "} {
		if err := os.WriteFile(filepath.Join(digestsOf(root).dir, counterMid), []byte(raw), 0o644); err != nil {
			t.Fatal(err)
		}
		if n := readCounter(root, counterMid); n != 7 {
			t.Errorf("counter %q read %d", raw, n)
		}
	}
}

// The schema subset the writer asserts, against the repository's own two schemas.
func TestValidateFields(t *testing.T) {
	root := newRepo(t)
	good := []kv{{"schema_version", 1}, {"session_id", "s"}, {"written_at", "2026-11-14T12:00:00Z"}, {"trigger", "digest-skill"},
		{"branch", ""}, {"head_sha", "h"}, {"head_subject", "x"}, {"open_pr", nil}, {"mutations_since_last", 3}}
	if err := validateFields(root, "digest", good); err != nil {
		t.Fatalf("valid digest: %v", err)
	}
	replace := func(key string, val any) []kv {
		out := append([]kv(nil), good...)
		for i := range out {
			if out[i].key == key {
				out[i].val = val
			}
		}
		return out
	}
	for desc, c := range map[string]struct {
		fields []kv
		want   string
	}{
		"bad trigger":       {replace("trigger", "not-a-real-trigger"), "/trigger"},
		"schema version 2":  {replace("schema_version", 2), "/schema_version"},
		"empty session id":  {replace("session_id", ""), "shorter than"},
		"null branch":       {replace("branch", nil), "/branch"},
		"negative count":    {replace("mutations_since_last", -1), "less than"},
		"unknown property":  {append(append([]kv(nil), good...), kv{"extra", "x"}), `"extra" is not allowed`},
		"missing head_sha":  {good[:5], `"head_sha" is missing`},
		"open_pr is number": {replace("open_pr", 4), "/open_pr"},
	} {
		if err := validateFields(root, "digest", c.fields); err == nil || !strings.Contains(err.Error(), c.want) {
			t.Errorf("%s: %v, want %q", desc, err, c.want)
		}
	}
	rationale := []kv{{"schema_version", 1}, {"trigger", "pr-rationale-capture"}, {"captured_at", "t"}, {"branch", "b"}, {"pr_number", "9"}, {"diff_shortstat", ""}}
	if err := validateFields(root, "rationale", rationale); err != nil {
		t.Fatalf("valid rationale: %v", err)
	}
	rationale[1].val = "digest-skill"
	if err := validateFields(root, "rationale", rationale); err == nil || !strings.Contains(err.Error(), "constant") {
		t.Errorf("rationale trigger const: %v", err)
	}
	if err := validateFields(t.TempDir(), "digest", good); err == nil || !strings.Contains(err.Error(), "schema not found") {
		t.Errorf("no schema: %v", err)
	}
	// success_criteria items: the nested shape the /digest skill writes.
	var sc []any
	if err := json.Unmarshal([]byte(`[{"criterion":"build green","status":"pending","evidence":null}]`), &sc); err != nil {
		t.Fatal(err)
	}
	if err := validateFields(root, "digest", append(append([]kv(nil), good...), kv{"success_criteria", sc})); err != nil {
		t.Errorf("success_criteria: %v", err)
	}
	sc[0].(map[string]any)["status"] = "done"
	if err := validateFields(root, "digest", append(append([]kv(nil), good...), kv{"success_criteria", sc})); err == nil || !strings.Contains(err.Error(), "/success_criteria/0/status") {
		t.Errorf("bad success_criteria status: %v", err)
	}
}

func TestUnknownHookDoesNotBlock(t *testing.T) {
	for _, args := range [][]string{{"no-such-hook"}, {}} {
		var out, errb bytes.Buffer
		code := dispatch(args, &env{stdin: strings.NewReader(""), stdout: &out, stderr: &errb, sys: fakeSystem("", time.Now())})
		if code != 1 || !strings.Contains(errb.String(), "usage: demerzel-hooks") {
			t.Fatalf("%v: exit %d %q", args, code, errb.String())
		}
	}
}
