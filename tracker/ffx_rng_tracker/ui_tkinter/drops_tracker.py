import tkinter as tk

from ..ui_abstract.drops_tracker import DropsTracker
from .base_widgets import TkConfirmPopup, TkWarningPopup
from .input_widget import TkInputWidget
from .output_widget import TkOutputWidget


class TkDropsOutputWidget(TkOutputWidget):

    def get_regex_patterns(self) -> dict[str, str]:
        tags = {
            'equipment': 'Equipment',
            'no encounters': 'No Encounters',
            'stat update': '^.*changed to.+$',
        }
        tags.update(super().get_regex_patterns())
        return tags


class TkDropsTracker(tk.Frame):
    """Widget used to track monster drops RNG."""
    def __init__(self, parent, seed: int, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        input_widget = TkInputWidget(self)
        input_widget.pack(fill='y', side='left')
        input_widget.bind(
            '<Control-s>', lambda _: self.tracker.save_input_data())

        output_widget = TkDropsOutputWidget(self)
        output_widget.pack(expand=True, fill='both', side='right')

        self.tracker = DropsTracker(
            seed=seed,
            input_widget=input_widget,
            output_widget=output_widget,
            warning_popup=TkWarningPopup(),
            confirmation_popup=TkConfirmPopup(),
            )
