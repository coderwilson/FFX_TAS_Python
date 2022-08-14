from typing import Callable, Protocol


class InputWidget(Protocol):
    """Protocol class for input widgets."""

    def get_input(self) -> str:
        """Returns the input data as a string."""

    def set_input(self, text: str) -> None:
        """Setup the input widget contents."""

    def register_callback(self, callback_func: Callable) -> None:
        """Register the function called as a callback."""
