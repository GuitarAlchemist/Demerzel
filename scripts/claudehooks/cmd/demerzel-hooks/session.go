package main

import (
	"bytes"
	"crypto/sha256"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"runtime"
	"time"
)

// sessionStart is the one SessionStart hook of this program: it installs this binary for the other
// hooks, then injects the digest (sessionstartDigest). settings.json runs it through `go run`, so a
// session always starts with the hooks built from the checked-out source.
func sessionStart(e *env) int {
	if root := e.repoRoot(); root != "" {
		if err := e.install(root); err != nil {
			fmt.Fprintf(e.stderr, "[demerzel-hooks] could not install .claude/hooks/bin: %v (the previous build stays)\n", err)
		}
	}
	return sessionstartDigest(e)
}

// binPath is where the hooks other than session-start find the binary.
func binPath(root string) string {
	name := "demerzel-hooks"
	if runtime.GOOS == "windows" {
		name += ".exe"
	}
	return filepath.Join(root, ".claude", "hooks", "bin", name)
}

// install copies the running executable to binPath when its content differs. The copy goes to a
// temporary name first and is renamed over the target, so a hook starting meanwhile runs either
// the old binary or the new one, never half of one. On Windows the rename fails while another
// session runs the old binary; that session's next start retries.
func (e *env) install(root string) error {
	self, err := e.sys.executable()
	if err != nil {
		return err
	}
	want, err := os.ReadFile(self)
	if err != nil {
		return err
	}
	target := binPath(root)
	if have, err := os.ReadFile(target); err == nil && sha256.Sum256(have) == sha256.Sum256(want) {
		return nil
	}
	if err := os.MkdirAll(filepath.Dir(target), 0o755); err != nil {
		return err
	}
	tmp, err := os.CreateTemp(filepath.Dir(target), ".demerzel-hooks-*.tmp")
	if err != nil {
		return err
	}
	_, werr := io.Copy(tmp, bytes.NewReader(want))
	cerr := tmp.Close()
	if werr != nil || cerr != nil {
		_ = os.Remove(tmp.Name()) // best-effort cleanup; the write error is the one reported
		return fmt.Errorf("writing %s: %v %v", tmp.Name(), werr, cerr)
	}
	err = os.Chmod(tmp.Name(), 0o755)
	if err == nil {
		err = os.Rename(tmp.Name(), target)
	}
	if err != nil {
		_ = os.Remove(tmp.Name()) // best-effort cleanup; err is the one reported
		return err
	}
	return nil
}

// sessionstartDigest prints state/digests/latest.md for the session's context (was
// sessionstart-digest.ps1); one line instead when it is more than 24 hours old.
func sessionstartDigest(e *env) int {
	root := e.repoRoot()
	if root == "" {
		return 0
	}
	latest := digestsOf(root).latest
	age, ok := e.age(latest)
	if !ok {
		return 0
	}
	if age.Hours() > 24 {
		fmt.Fprint(e.stdout, "\nSession digest exists but is >24h old — skipping injection. Run /digest to refresh.\n\n")
		return 0
	}
	data, err := os.ReadFile(latest)
	if err != nil {
		return 0
	}
	fmt.Fprintf(e.stdout, "\n=== Session digest (last written %s ago) ===\n", ageString(age))
	_, _ = e.stdout.Write(data) // `Get-Content -Raw | Write-Host`: the file, then a line break
	fmt.Fprint(e.stdout, "\n=== End digest ===\n\n")
	return 0
}

// ageString is "<n> min" under an hour, "<h>h <m>m" above. The script rounded the hours
// ([int]TotalHours), so 1h30 read "2h 30m"; they are whole hours here, as in tars and ix.
func ageString(age time.Duration) string {
	if age.Minutes() < 60 {
		return fmt.Sprintf("%d min", psInt(age.Minutes()))
	}
	return fmt.Sprintf("%dh %dm", int64(age.Hours()), int64(age.Minutes())%60)
}
