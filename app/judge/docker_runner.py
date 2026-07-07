import subprocess
import tempfile
import time
from pathlib import Path

from app.judge.execution_result import ExecutionResult


class DockerRunner:
    """
    Executes source code inside Docker.
    """

    def run_python(
        self,
        *,
        source_code: str,
        stdin: str = "",
    ) -> ExecutionResult:
        """
        Execute Python code inside an isolated Docker container.
        """

        with tempfile.TemporaryDirectory() as temp_dir:

            source_file = Path(temp_dir) / "solution.py"

            source_file.write_text(
                source_code,
                encoding="utf-8",
            )

            command = [
                "docker",
                "run",
                "--rm",
                "-i",
                "-v",
                f"{temp_dir}:/workspace",
                "-w",
                "/workspace",
                "python:3.12-slim",
                "python",
                "solution.py",
            ]

            start = time.perf_counter()

            completed = subprocess.run(
                command,
                input=stdin,
                capture_output=True,
                text=True,
                )

            end = time.perf_counter()

            return ExecutionResult(
                stdout=completed.stdout,
                stderr=completed.stderr,
                exit_code=completed.returncode,
                execution_time_ms=int(
                    (end - start) * 1000
                ),
            )