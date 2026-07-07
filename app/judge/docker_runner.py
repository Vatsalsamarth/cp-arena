import logging
import subprocess
import tempfile
import time
from pathlib import Path

from app.judge.execution_result import ExecutionResult

logger = logging.getLogger(__name__)


class DockerRunner:
    """
    Executes source code inside Docker.
    """

    DEFAULT_TIMEOUT_SECONDS = 10

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
            source_file.write_text(source_code, encoding="utf-8")

            command = [
                "docker",
                "run",
                "--rm",
                "-i",
                "--network=none",
                "--security-opt",
                "no-new-privileges",
                "--pids-limit",
                "64",
                "--memory",
                "128m",
                "-v",
                f"{temp_dir}:/workspace:rw",
                "-w",
                "/workspace",
                "python:3.12-slim",
                "python",
                "solution.py",
            ]

            start = time.perf_counter()

            try:
                completed = subprocess.run(
                    command,
                    input=stdin,
                    capture_output=True,
                    text=True,
                    timeout=self.DEFAULT_TIMEOUT_SECONDS,
                )
            except subprocess.TimeoutExpired as exc:
                logger.warning("Docker execution timed out.")
                return ExecutionResult(
                    stdout=exc.stdout or "",
                    stderr="Execution timed out.",
                    exit_code=-1,
                    execution_time_ms=int(self.DEFAULT_TIMEOUT_SECONDS * 1000),
                )
            except FileNotFoundError as exc:
                logger.exception("Docker binary not found.")
                return ExecutionResult(
                    stdout="",
                    stderr="Docker is not installed or not available in PATH.",
                    exit_code=-1,
                    execution_time_ms=0,
                )
            except subprocess.SubprocessError as exc:
                logger.exception("Docker execution failed.")
                return ExecutionResult(
                    stdout="",
                    stderr=str(exc),
                    exit_code=-1,
                    execution_time_ms=0,
                )
            finally:
                end = time.perf_counter()

            return ExecutionResult(
                stdout=completed.stdout,
                stderr=completed.stderr,
                exit_code=completed.returncode,
                execution_time_ms=int((end - start) * 1000),
            )
