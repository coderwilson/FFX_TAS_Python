from typing import Protocol


class OutputWidget(Protocol):
    """Protocol class for output widgets."""
    regex_patterns: dict[str, str]

    def print_output(self, output: str) -> None:
        """Prints the output data to the screen."""


class ConfirmationPopup(OutputWidget):
    confirmed: bool
