package main

import (
	"regexp"
	"strings"
	"unicode"
)

// prRationaleCapture (PostToolUse on Bash; was pr-rationale-capture.ps1) snapshots a
// `gh pr create`'s title, body and diff stats to state/digests/pr-<num>-<slug>.md, so the
// rationale survives later edits of the pull request (Cherny's PR rationale capture).
func prRationaleCapture(e *env) int {
	root := e.repoRoot()
	if root == "" {
		return 0
	}
	p := e.payload()
	if p == nil {
		return 0
	}
	cmd := field(p, "tool_input", "command")
	if cmd == "" || !ghPRCreate.MatchString(cmd) {
		return 0
	}
	output := ""
	switch r := p["tool_response"].(type) {
	case map[string]any:
		output = field(r, "output")
	case string:
		output = r
	}

	title := ""
	if m := titleFlag.FindStringSubmatch(cmd); m != nil {
		title = m[1] + m[2]
	}
	body := bodyFlag(cmd)
	num := "unknown"
	if m := prURL.FindStringSubmatch(output); m != nil {
		num = m[1]
	}
	// `& git diff --shortstat` kept git's leading space; only the line end goes.
	shortStat := e.git(root, "diff", "--shortstat", "HEAD~1")

	e.writeDigest(root, digestWrite{
		kind:      "rationale",
		facts:     repoFacts{branch: e.git(root, "rev-parse", "--abbrev-ref", "HEAD")},
		prNumber:  num,
		title:     title,
		shortstat: shortStat,
		body:      "# PR #" + num + " — " + title + "\n\n## Title\n\n" + title + "\n\n## Body\n\n" + body,
	}, "pr-rationale-capture", e.stderr)
	return 0
}

var (
	ghPRCreate = regexp.MustCompile(`(?i)gh\s+pr\s+create`) // -notmatch ignores case
	titleFlag  = regexp.MustCompile(`--title\s+(?:"([^"]*)"|'([^']*)')`)
	bodyStart  = regexp.MustCompile(`--body\s+["']`)
	prURL      = regexp.MustCompile(`pull/(\d+)`)
	nonSlug    = regexp.MustCompile(`[^a-z0-9]+`)
)

// bodyFlag is the script's `--body\s+(?:"([\s\S]*?)"(?=\s|$)|'([\s\S]*?)'(?=\s|$))`: the text up
// to the first matching quote that ends the command or is followed by whitespace. RE2 has no
// look-ahead, so the closing quote is searched by hand.
func bodyFlag(cmd string) string {
	for _, loc := range bodyStart.FindAllStringIndex(cmd, -1) {
		quote := cmd[loc[1]-1]
		rest := cmd[loc[1]:]
		for i := 0; i < len(rest); i++ {
			if rest[i] != quote {
				continue
			}
			if i+1 == len(rest) || unicode.IsSpace(rune(rest[i+1])) {
				return rest[:i]
			}
		}
	}
	return ""
}

// prSlug: lowercased, every run of other characters one dash, no dash at either end, cut to 40
// characters and trimmed of dashes again; "untitled" when nothing is left.
func prSlug(title string) string {
	s := strings.Trim(nonSlug.ReplaceAllString(strings.ToLower(title), "-"), "-")
	if len(s) > 40 {
		s = strings.Trim(s[:40], "-")
	}
	if s == "" {
		return "untitled"
	}
	return s
}
