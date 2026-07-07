from dataclasses import dataclass


@dataclass
class ExecutionResult:
    """
    Result returned by the Docker runner.
    """

    stdout: str
    stderr: str
    exit_code: int
    execution_time_ms: int