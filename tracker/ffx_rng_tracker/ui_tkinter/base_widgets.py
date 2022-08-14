import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from ..configs import Configs
from ..data.constants import GameVersion
from ..data.seeds import DAMAGE_VALUES_NEEDED, get_seed
from ..errors import InvalidDamageValueError, SeedNotFoundError


class ScrollableText(tk.Text):
    """Upgraded Text widget with an highlight_pattern
    method, a set method and with a vertical scrollbar
    and an optional horizontal scrollbar.
    """

    def __init__(self, parent, *args, **kwargs) -> None:
        self.frame = tk.Frame(parent)
        self.v_scrollbar = tk.Scrollbar(self.frame)
        self.v_scrollbar.grid(row=0, column=1, sticky='ns')
        kwargs['yscrollcommand'] = self.v_scrollbar.set
        super().__init__(self.frame, *args, **kwargs)
        self.grid(row=0, column=0, sticky='nsew')
        self.v_scrollbar.configure(command=self.yview)
        if kwargs.get('wrap') == 'none':
            self._add_h_scrollbar()

        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self._override_geometry_managers()

    def _override_geometry_managers(self) -> None:
        """Override the geometry managers methods with the ones
        from the frame."""
        text_meths = vars(tk.Text).keys()
        methods = (vars(tk.Pack).keys()
                   | vars(tk.Grid).keys()
                   | vars(tk.Place).keys())
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

    def _add_h_scrollbar(self) -> None:
        self.h_scrollbar = tk.Scrollbar(self.frame, orient='horizontal')
        self.h_scrollbar.grid(row=1, column=0, sticky='ew')
        self.configure(xscrollcommand=self.h_scrollbar.set)
        self.h_scrollbar.configure(command=self.xview)

    def highlight_pattern(self, pattern: str, tag: str) -> None:
        """Apply the given tag to all occurrences of the pattern."""
        start = '1.0'
        end = '1.0'
        count = tk.IntVar()
        while True:
            start = self.search(pattern, end, 'end', count=count, regexp=True)
            characters = count.get()
            if start == '' or characters == 0:
                break
            end = f'{start}+{characters}c'
            self.tag_add(tag, start, end)

    def set(self, text: str) -> None:
        """Replaces the previous text and scrolls back to
        the previous position.
        """
        current_text = self.get('1.0', 'end')[:-1]
        current_number_of_lines = len(current_text.split('\n'))
        last_line = self.index(f'@0,{self.winfo_height()}')
        line_index = int(last_line.split('.')[0])

        self.replace(1.0, 'end', text)

        # scroll down if the last line of the text was visible
        # but only if there was at least 1 line
        if line_index == current_number_of_lines and line_index > 1:
            self.yview_pickplace('end')


class BetterSpinbox(ttk.Spinbox):
    """Upgraded Spinbox widget with a set method
    and readonly by default.
    """

    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.set(0)

    def set(self, text: str | int) -> None:
        """Set the spinbox content."""
        self.config(state='normal')
        self.delete(0, 'end')
        self.insert(0, text)
        self.config(state='readonly')


class ScrollableFrame(tk.Frame):
    """"""

    def __init__(self, parent, *args, **kwargs) -> None:
        self.parent = parent
        self.outer_frame = tk.Frame(parent)
        canvas = tk.Canvas(self.outer_frame, width=280)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar = tk.Scrollbar(
            self.outer_frame, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')
        canvas.config(yscrollcommand=scrollbar.set)
        super().__init__(canvas, *args, **kwargs)
        super().pack(fill='both', expand=True)
        self.bind(
            '<Configure>',
            lambda _: canvas.config(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=self, anchor='nw')
        # when the mouse enters the canvas it binds the mousewheel to scroll
        canvas.bind(
            '<Enter>',
            lambda _: canvas.bind_all(
                '<MouseWheel>',
                lambda e: canvas.yview_scroll(
                    int(-1 * (e.delta / 120)), 'units')))
        # when the mouse leaves the canvas it unbinds the mousewheel
        canvas.bind('<Leave>', lambda _: canvas.unbind_all('<MouseWheel>'))
        self.pack = self.outer_frame.pack
        self.grid = self.outer_frame.grid


class DamageValuesDialogue(simpledialog.Dialog):
    """Input dialogue used to get damage values."""

    def __init__(self, *args, **kwargs) -> None:
        self.warning_label = False
        self.seed = None
        super().__init__(*args, **kwargs)

    def body(self, parent: tk.Tk) -> tk.Entry:
        self.parent = parent
        text = 'Damage values (Auron1 Tidus1 A2 T2 A3 T3)'
        if Configs.game_version is not GameVersion.HD:
            text = text[:-1] + ' A4 A5)'
        tk.Label(parent, text=text).pack()
        self.entry = tk.Entry(parent, width=25)
        self.entry.pack(fill='x')
        return self.entry

    def buttonbox(self) -> None:
        tk.Button(self, text='Submit', command=self.validate_input).pack()
        self.bind('<Return>', lambda _: self.validate_input())
        self.bind('<Escape>', lambda _: self.parent.quit())

    def validate_input(self) -> None:
        input_string = self.entry.get()
        # replace different symbols with spaces
        for symbol in (',', '-', '/', '\\', '.'):
            input_string = input_string.replace(symbol, ' ')
        seed_info = input_string.split()
        try:
            seed_info = [int(i) for i in seed_info]
        except ValueError as error:
            error = str(error).split(':', 1)[1]
            self.show_warning(f'{error} is not a valid damage value.')
            return
        damage_values_needed = DAMAGE_VALUES_NEEDED[Configs.game_version]
        match seed_info:
            case []:
                return
            case [seed]:
                if not (0 <= seed <= 0xffffffff):
                    self.show_warning(
                        'Seed must be an integer between 0 and 4294967295')
                    return
            case _ if len(seed_info) < damage_values_needed:
                self.show_warning(
                    f'Need at least {damage_values_needed} damage values.')
                return
            case _:
                try:
                    seed = get_seed(seed_info)
                except (InvalidDamageValueError,
                        SeedNotFoundError) as error:
                    self.show_warning(error)
                    return

        self.seed = seed
        self.destroy()

    def show_warning(self, text) -> None:
        if self.warning_label:
            self.warning_label.config(text=text)
        else:
            self.warning_label = tk.Label(self, text=text)
            self.warning_label.pack(fill='x')


class TkWarningPopup:

    def print_output(self, output: str) -> None:
        messagebox.showwarning(message=output)


class TkConfirmPopup:
    confirmed: bool

    def print_output(self, output: str) -> None:
        self.confirmed = messagebox.askokcancel(message=output)


DEFAULT_FONT_ARGS = dict(family='Courier New', size=Configs.font_size)
