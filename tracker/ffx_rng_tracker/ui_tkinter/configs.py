import tkinter as tk

from ..configs import Configs
from ..utils import treeview
from .output_widget import TkOutputWidget


class ConfigsPage(tk.Frame):
    """Widget that shows the loaded configuration."""

    def __init__(self, parent, _, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.output_widget = TkOutputWidget(self, wrap='none')
        self.output_widget.pack(expand=True, fill='both')
        self.output_widget.print_output(treeview(Configs.get_configs()))
