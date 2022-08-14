import tkinter as tk
from typing import Callable

from ..ui_abstract.seedfinder import SeedFinder
from .actions_tracker import TkActionsOutputWidget
from .base_widgets import TkConfirmPopup, TkWarningPopup
from .input_widget import TkInputWidget


class TkDamageValuesWidget(tk.StringVar):

    def get_input(self) -> str:
        return self.get()

    def set_input(self, text: str) -> None:
        self.set(text)

    def register_callback(self, callback_func: Callable) -> None:
        raise NotImplementedError()


class TkSeedFinder(tk.Frame):
    """Widget used to find the starting seed."""

    def __init__(self, parent, seed: int = 0, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        frame = tk.Frame(self)
        frame.pack(fill='y', side='left')
        tk.Label(frame, text='Actions').pack()

        input_widget = TkInputWidget(frame)
        input_widget.pack(fill='y', expand=True)

        tk.Label(frame, text='Damage values').pack()

        damage_values_widget = TkDamageValuesWidget(self)
        tk.Entry(frame, textvariable=damage_values_widget).pack(fill='x')

        button = tk.Button(frame, text='Search Seed')
        button.pack()

        output_widget = TkActionsOutputWidget(self)
        output_widget.pack(expand=True, fill='both', side='right')

        self.tracker = SeedFinder(
            seed=seed,
            input_widget=input_widget,
            output_widget=output_widget,
            warning_popup=TkWarningPopup(),
            confirmation_popup=TkConfirmPopup(),
            damage_values_widget=damage_values_widget,
        )
        button.configure(command=self.tracker.find_seed)
