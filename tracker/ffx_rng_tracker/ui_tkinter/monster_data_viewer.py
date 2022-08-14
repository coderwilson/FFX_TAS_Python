import re
import tkinter as tk
from typing import Callable

from ..ui_abstract.monster_data_viewer import MonsterDataViewer
from .input_widget import TkSearchBarWidget
from .output_widget import TkOutputWidget


class TkMonsterSelectionWidget(tk.Listbox):

    def __init__(self, parent, *args, **kwargs) -> None:
        kwargs.setdefault('listvariable', tk.StringVar())
        super().__init__(parent, *args, **kwargs)
        self._listvar: tk.StringVar = kwargs['listvariable']
        self._monster_names: list[str] = []

    def get_input(self) -> str:
        input_data = self.curselection()
        try:
            monster_index = input_data[0]
        # if there is nothing selected
        # curselection returns an empty tuple
        except IndexError:
            return ''
        return self._monster_names[monster_index]

    def set_input(self, data: list[str]) -> None:
        self._monster_names = data
        self._listvar.set(data)

    def register_callback(self, callback_func: Callable) -> None:
        self.bind('<<ListboxSelect>>', callback_func)


class TkMonsterDataViewer(tk.Frame):
    """Widget used to display monster's data."""

    def __init__(self, parent, _=None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        outer_frame = tk.Frame(self)
        outer_frame.pack(fill='y', side='left')

        inner_frame = tk.Frame(outer_frame)
        inner_frame.pack(fill='x')
        tk.Label(inner_frame, text='Search:').pack(side='left')
        search_bar_widget = TkSearchBarWidget(inner_frame)
        search_bar_widget.pack(fill='x', side='right')

        monster_selection_widget = TkMonsterSelectionWidget(
            outer_frame, width=30)
        monster_selection_widget.pack(expand=True, fill='y')

        self.output_widget = TkOutputWidget(self, wrap='none')
        self.output_widget.pack(expand=True, fill='both', side='right')

        self.tracker = MonsterDataViewer(
            monster_selection_widget=monster_selection_widget,
            search_bar_widget=search_bar_widget,
            output_widget=self.output_widget,
        )

        monster_selection_widget.set_input(sorted(self.tracker.monster_data))
        search_bar_widget.register_callback(self.tracker.filter_monsters)
        monster_selection_widget.register_callback(self.callback)

    def callback(self, *_, **__) -> None:
        filter = '(?i)' + re.escape(self.tracker.search_bar_widget.get_input())
        self.output_widget.regex_patterns['important monster'] = filter
        self.tracker.callback()
