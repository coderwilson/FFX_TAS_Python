import tkinter as tk
from tkinter import font
from typing import Callable

from .base_widgets import DEFAULT_FONT_ARGS, ScrollableText


class TkInputWidget(ScrollableText):

    def __init__(self, parent, *args, **kwargs) -> None:
        kwargs.setdefault('font', font.Font(**DEFAULT_FONT_ARGS))
        kwargs.setdefault('width', 40)
        kwargs.setdefault('undo', True)
        kwargs.setdefault('autoseparators', True)
        kwargs.setdefault('maxundo', -1)
        super().__init__(parent, *args, **kwargs)

    def get_input(self) -> str:
        return self.get('1.0', 'end')

    def set_input(self, text: str) -> None:
        self.set(text)

    def register_callback(self, callback_func: Callable) -> None:
        self.bind('<KeyRelease>', callback_func)


class TkSearchBarWidget(tk.Entry):

    def get_input(self) -> str:
        return self.get()

    def set_input(self, text: str) -> None:
        self.delete('1', 'end')
        self.insert('1', text)

    def register_callback(self, callback_func: Callable) -> None:
        self.bind('<KeyRelease>', callback_func)
