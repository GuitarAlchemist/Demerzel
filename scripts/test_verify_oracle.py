import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


class VerifyOracleTests(unittest.TestCase):
    def test_oracle_runs_python_tests_and_checks_the_exit_code(self):
        script = (ROOT / "scripts" / "verify.ps1").read_text(encoding="utf-8")

        self.assertIn("python -m unittest discover -s scripts -p 'test_*.py'", script)
        self.assertIn("Assert-NativeSuccess 'python unit tests'", script)

    def test_oracle_fails_when_python_tests_fail(self):
        pwsh = shutil.which("pwsh")
        self.assertIsNotNone(pwsh, "pwsh is required to test the repository oracle")

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            scripts = root / "scripts"
            bin_dir = root / "bin"
            scripts.mkdir()
            bin_dir.mkdir()
            shutil.copy2(ROOT / "scripts" / "verify.ps1", scripts / "verify.ps1")

            fake_python = bin_dir / ("python.cmd" if os.name == "nt" else "python")
            fake_python.write_text(
                "@exit /b 7\n" if os.name == "nt" else "#!/bin/sh\nexit 7\n",
                encoding="utf-8",
            )
            fake_python.chmod(0o755)
            env = os.environ | {"PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}"}

            result = subprocess.run(
                [pwsh, "-NoProfile", "-File", str(scripts / "verify.ps1")],
                capture_output=True,
                text=True,
                env=env,
                check=False,
            )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("python unit tests failed with exit code 7", result.stderr)


if __name__ == "__main__":
    unittest.main()
