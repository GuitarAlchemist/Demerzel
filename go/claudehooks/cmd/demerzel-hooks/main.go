// demerzel-hooks is every Claude Code hook of this repository except Gaia's bus client
// (scripts/gaia_hook.py, owned by the Gaia lane), one subcommand per hook. It replaces the
// PowerShell scripts that lived in .claude/hooks/ (the user, 2026-11-05: "jamais de shell dans les
// hooks"). It mirrors tars's go/claudehooks (tars PR #419) and ix's (ix PR #512): the three repos'
// digest, correction and PR-rationale hooks are the same family. Demerzel's scripts wrote through
// DigestState.psm1's Write-Digest, so digest.go ports that writer too (schema-validated
// frontmatter, archive rotation, counter reset by trigger).
//
// .claude/settings.json runs `session-start` through `go run` (Go caches the built executable),
// and that subcommand installs the binary as .claude/hooks/bin/demerzel-hooks[.exe], which every
// other hook calls directly. The bin directory is gitignored.
//
// Each subcommand keeps its script's contract: the same inputs, the same exit codes, the same
// files written, the same text on stdout, except where the commit that ported them says otherwise.
package main

import (
	"fmt"
	"io"
	"os"
	"sort"
	"strings"
)

// env is what a hook may touch: its streams, its arguments and the outside world. Tests replace it.
type env struct {
	stdin  io.Reader
	stdout io.Writer
	stderr io.Writer
	args   []string
	sys    *system
}

var hooks = map[string]func(*env) int{
	"session-start":           sessionStart,
	"sessionstart-digest":     sessionstartDigest,
	"precompact-digest":       precompactDigest,
	"digest-staleness-nudge":  digestStalenessNudge,
	"correction-detector":     correctionDetector,
	"digest-activity-tracker": digestActivityTracker,
	"pr-rationale-capture":    prRationaleCapture,
	"digest-stop-finalize":    digestStopFinalize,
}

func main() {
	var stdin io.Reader = os.Stdin
	// A hook run by hand from a terminal does not wait for input.
	if fi, err := os.Stdin.Stat(); err == nil && fi.Mode()&os.ModeCharDevice != 0 {
		stdin = strings.NewReader("")
	}
	os.Exit(dispatch(os.Args[1:], &env{stdin: stdin, stdout: os.Stdout, stderr: os.Stderr, sys: realSystem()}))
}

func dispatch(args []string, e *env) int {
	if len(args) == 0 || hooks[args[0]] == nil {
		names := make([]string, 0, len(hooks))
		for n := range hooks {
			names = append(names, n)
		}
		sort.Strings(names)
		fmt.Fprintf(e.stderr, "usage: demerzel-hooks <hook> [args]\nhooks: %v\n", names)
		return 1 // never 2: a misnamed hook must not block anything
	}
	e.args = args[1:]
	return hooks[args[0]](e)
}
