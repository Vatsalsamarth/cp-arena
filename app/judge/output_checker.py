class OutputChecker:
    """
    Compares program output with expected output.
    """

    @staticmethod
    def normalize(
        output: str,
    ) -> str:
        """
        Normalize whitespace.
        """

        return "\n".join(line.strip() for line in output.strip().splitlines())

    @classmethod
    def compare(
        cls,
        actual: str,
        expected: str,
    ) -> bool:
        """
        Check whether outputs match.
        """

        return cls.normalize(actual) == cls.normalize(expected)
