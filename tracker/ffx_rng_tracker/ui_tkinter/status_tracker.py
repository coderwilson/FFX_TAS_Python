import tkinter as tk

from ..ui_functions import get_status_chance_string
from .output_widget import TkOutputWidget


class TkStatusTrackerOutputWidget(TkOutputWidget):

    def get_regex_patterns(self) -> dict[str, str]:
        return {'status miss': '100'}


class TkStatusTracker(tk.Frame):
    """Widget that shows status RNG rolls."""

    def __init__(self, parent, seed, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.output_widget = TkStatusTrackerOutputWidget(self, wrap='none')
        self.output_widget.pack(expand=True, fill='both')
        self.output_widget.print_output(get_status_chance_string(seed, 100))
