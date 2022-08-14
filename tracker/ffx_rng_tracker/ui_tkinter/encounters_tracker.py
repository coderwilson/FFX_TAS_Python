import re
import tkinter as tk
from tkinter import ttk
from typing import Callable

from ..configs import Configs
from ..data.encounter_formations import ZONES
from ..data.encounters import EncounterData, get_encounters
from ..ui_abstract.encounters_planner import EncountersPlanner
from ..ui_abstract.encounters_table import EncountersTable
from ..ui_abstract.encounters_tracker import EncountersTracker
from ..ui_tkinter.input_widget import TkSearchBarWidget
from ..utils import stringify
from .base_widgets import (BetterSpinbox, ScrollableFrame, TkConfirmPopup,
                           TkWarningPopup)
from .output_widget import TkOutputWidget


class EncounterSlider(tk.Frame):

    def __init__(self,
                 parent,
                 label: str,
                 min: int,
                 default: int,
                 max: int,
                 variable: tk.Variable = None,
                 value=None,
                 command: Callable = None,
                 *args,
                 **kwargs,
                 ) -> None:
        super().__init__(parent, *args, **kwargs)

        self.scale = tk.Scale(
            self, orient='horizontal', label=None, from_=min, to=max,
            command=command)
        self.scale.set(default)
        self.scale.pack(side='left', anchor='w')

        if value is None:
            value = label
        self.button = tk.Radiobutton(
            self, text=label, variable=variable, value=value, command=command)
        self.button.pack(side='right', anchor='se')

    def get(self) -> int:
        return self.scale.get()

    def get_name(self) -> str:
        return self.button.cget(key='text')

    def config(self, command=None, *args, **kwargs) -> None:
        if command is not None:
            self.scale.config(command=command)
            self.button.config(command=command)
        super().config(*args, **kwargs)


class TkEncountersInputWidget(tk.Frame):

    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.encounters: list[EncounterData] = []

        self.callback_func: Callable = None

        self.initiative_equip = ttk.Checkbutton(self, text='Sentry')
        self.initiative_equip.grid(row=0, column=0, sticky='w')
        self.initiative_equip.state(['selected'])

        self.current_zone = tk.StringVar(value='Start')

        self.sliders_frame = ScrollableFrame(self)
        self.sliders_frame.grid(row=1, column=0, columnspan=2, sticky='nsew')
        self.rowconfigure(1, weight=1)

        self.sliders: dict[str, EncounterSlider] = {}

        self.start_button = tk.Radiobutton(
            self, text='Start', variable=self.current_zone, value='Start')
        self.start_button.grid(row=0, column=1, sticky='w')

    def add_slider(self, label: str, min: int, default: int, max: int) -> None:
        slider = EncounterSlider(
            self.sliders_frame, label, min, default, max, self.current_zone)
        slider.pack(anchor='w')
        self.sliders[label] = slider

    def get_input(self) -> str:
        spacer = '# ' + ('=' * 60)
        current_zone = self.current_zone.get()
        initiative_equip = 'selected' in self.initiative_equip.state()

        input_data = []
        for encounter in self.encounters:
            if initiative_equip and encounter.initiative:
                initiative = 'initiative'
            else:
                initiative = ''
            if encounter.type == 'boss':
                encs = 1
            else:
                encs = self.sliders[encounter.label].get()
                if encs >= 0:
                    input_data.append(spacer)
                    if current_zone == encounter.label:
                        input_data.append('///')
                    input_data.append(f'#     {encounter.label}:')
            for _ in range(encs):
                input_data.append(f'encounter {encounter.type} '
                                  f'{encounter.name} {initiative}')
        return '\n'.join(input_data)

    def set_input(self, text: str) -> None:
        return

    def register_callback(self, callback_func: Callable) -> None:
        self.initiative_equip.config(command=callback_func)
        self.start_button.config(command=callback_func)
        for slider in self.sliders.values():
            slider.config(command=callback_func)
        self.callback_func = callback_func


class TkEncountersOutputWidget(TkOutputWidget):

    def get_regex_patterns(self) -> dict[str, str]:
        important_monsters = '(?i)' + '|'.join(
            [re.escape(m) for m in Configs.important_monsters])
        patterns = {
            'wrap margin': '^.+$',
            'preemptive': 'Preemptive',
            'ambush': 'Ambush',
            'important monster': important_monsters,
            'encounter': '^#(.+?)?$',
        }
        return patterns


class TkEncountersTracker(tk.Frame):

    def __init__(self, parent, seed: int, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        input_widget = TkEncountersInputWidget(self)
        encounters = get_encounters('encounters_notes.csv', seed)
        input_widget.encounters = encounters
        for encounter in encounters:
            if encounter.type == 'boss':
                continue
            input_widget.add_slider(
                encounter.label, encounter.min,
                encounter.default, encounter.max)
        input_widget.pack(fill='y', side='left')

        output_widget = TkEncountersOutputWidget(self)
        output_widget.pack(expand=True, fill='both', side='right')

        self.tracker = EncountersTracker(
            seed=seed,
            input_widget=input_widget,
            output_widget=output_widget,
            warning_popup=TkWarningPopup(),
            confirmation_popup=TkConfirmPopup(),
            )


class TkEncountersPlannerInputWidget(tk.Frame):

    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.callback_func: Callable = None

        self.searchbar = TkSearchBarWidget(self)
        self.searchbar.pack(fill='x')
        self.searchbar.set_input('Type monster names here')

        options = ['Boss', 'Simulation']
        options.extend([z.name for z in ZONES.values()])
        self.selected_zone = tk.StringVar(self)
        self.selected_zone.set(options[0])
        combobox = ttk.Combobox(
            self, values=options, state='readonly',
            textvariable=self.selected_zone)
        combobox.pack(fill='x')
        button = tk.Button(
            self, text='Add Slider',
            command=lambda: self.add_slider(self.selected_zone.get()))
        button.pack(fill='x')

        self.initiative_equip = ttk.Checkbutton(self, text='Initiative')
        self.initiative_equip.pack(fill='x')
        self.initiative_equip.state(['selected'])

        self.current_zone_index = tk.IntVar(self, value=0)

        self.sliders_frame = ScrollableFrame(self)
        self.sliders_frame.pack(expand=True, fill='both')
        self.sliders: list[EncounterSlider] = []

    def add_slider(self,
                   label: str,
                   min: int = 0,
                   default: int = 1,
                   max: int = 100
                   ) -> None:
        value = len(self.sliders)
        slider = EncounterSlider(
            self.sliders_frame, label, min, default, max,
            self.current_zone_index, value, self.callback_func)
        slider.pack(anchor='w')
        self.sliders.append(slider)

    def get_input(self) -> str:
        spacer = '# ' + ('=' * 60)
        current_zone_index = self.current_zone_index.get()
        initiative_equip = 'selected' in self.initiative_equip.state()
        initiative = 'initiative' if initiative_equip else ''

        input_data = []
        for index, scale in enumerate(self.sliders):
            name = stringify(scale.get_name())
            match name:
                case 'boss':
                    name = 'dummy'
                    encounter_type = 'optional_boss'
                case 'simulation':
                    name = 'simulation_(dummy)'
                    encounter_type = 'simulated'
                case _:
                    encounter_type = 'random'
            for count in range(scale.get()):
                if count == 0:
                    # if there is some data append a spacer
                    if input_data:
                        input_data.append(spacer)
                    if index == current_zone_index:
                        input_data.append('///')
                    if name in ZONES:
                        input_data.append(f'#     {ZONES[name].name}:')
                line = f'encounter {encounter_type} {name} {initiative}'
                input_data.append(line)
        return '\n'.join(input_data)

    def set_input(self, text: str) -> None:
        return

    def register_callback(self, callback_func: Callable) -> None:
        self.searchbar.register_callback(callback_func)
        self.initiative_equip.config(command=callback_func)
        for slider in self.sliders:
            slider.config(command=callback_func)
        self.callback_func = callback_func


class TkEncountersPlanner(tk.Frame):
    """"""

    def __init__(self, parent, seed: int, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        input_widget = TkEncountersPlannerInputWidget(self)
        input_widget.pack(fill='y', side='left')

        output_widget = TkEncountersOutputWidget(self)
        output_widget.pack(expand=True, fill='both', side='right')

        self.tracker = EncountersPlanner(
            seed=seed,
            input_widget=input_widget,
            output_widget=output_widget,
            warning_popup=TkWarningPopup(),
            confirmation_popup=TkConfirmPopup(),
            search_bar=input_widget.searchbar,
            )


class TkEncountersTableInputWidget(tk.Frame):
    """"""
    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.searchbar = TkSearchBarWidget(self)
        self.searchbar.grid(row=0, column=0, columnspan=2, sticky='ew')
        self.searchbar.set_input('Type monster names here')

        self.initiative_equip = ttk.Checkbutton(self, text='Initiative')
        self.initiative_equip.grid(row=1, column=0, sticky='w')
        self.initiative_equip.state(['selected'])

        tk.Label(self, text='Random Encounters').grid(row=2, column=0)
        self.random_encounters = BetterSpinbox(self, from_=0, to=2000)
        self.random_encounters.grid(row=2, column=1)

        tk.Label(self, text='Bosses').grid(row=3, column=0)
        self.forced_encounters = BetterSpinbox(self, from_=0, to=2000)
        self.forced_encounters.grid(row=3, column=1)

        tk.Label(self, text='Simulated Encounters').grid(row=4, column=0)
        self.simulated_encounters = BetterSpinbox(self, from_=0, to=2000)
        self.simulated_encounters.grid(row=4, column=1)

        zones_frame = ScrollableFrame(self)
        zones_frame.grid(row=10, column=0, columnspan=2, sticky='nsew')
        self.rowconfigure(10, weight=1)

        tk.Label(self, text='Encounters to show').grid(row=11, column=0)
        self.shown_encounters = BetterSpinbox(self, from_=0, to=2000)
        self.shown_encounters.grid(row=11, column=1)
        self.shown_encounters.set(20)

        self.zones_buttons: dict[str, ttk.Checkbutton] = {}
        self.zones: dict[str, tk.BooleanVar] = {}
        for zone_name, zone in ZONES.items():
            zone_var = tk.BooleanVar(zones_frame, value=False)
            checkbutton = ttk.Checkbutton(
                zones_frame, text=zone.name, variable=zone_var)
            checkbutton.pack(anchor='w', fill='x')
            self.zones[zone_name] = zone_var
            self.zones_buttons[zone_name] = checkbutton

    def get_input(self) -> str:
        initiative_equip = 'selected' in self.initiative_equip.state()
        initiative = 'initiative' if initiative_equip else ''

        input_data = []
        for _ in range(int(self.forced_encounters.get())):
            input_data.append('encounter boss dummy')

        for _ in range(int(self.random_encounters.get())):
            input_data.append('encounter random besaid_lagoon')

        for _ in range(int(self.simulated_encounters.get())):
            input_data.append('encounter simulated simulation_(dummy)')

        zones = []
        for zone_name, active in self.zones.items():
            if active.get():
                zones.append(zone_name)
        if zones:
            for _ in range(int(self.shown_encounters.get())):
                input_data.append(f'encounter multizone {"/".join(zones)} '
                                  f'{initiative}')
        return '\n'.join(input_data)

    def set_input(self, text: str) -> None:
        return

    def register_callback(self, callback_func: Callable) -> None:
        self.searchbar.register_callback(callback_func)
        self.initiative_equip.config(command=callback_func)
        self.random_encounters.config(command=callback_func)
        self.forced_encounters.config(command=callback_func)
        self.simulated_encounters.config(command=callback_func)
        for button in self.zones_buttons.values():
            button.config(command=callback_func)
        self.shown_encounters.config(command=callback_func)


class TkEncountersTable(tk.Frame):
    """"""

    def __init__(self, parent, seed: int, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        input_widget = TkEncountersTableInputWidget(self)
        input_widget.pack(fill='y', side='left')

        output_widget = TkEncountersOutputWidget(self, wrap='none')
        output_widget.pack(expand=True, fill='both', side='right')

        self.tracker = EncountersTable(
            seed=seed,
            input_widget=input_widget,
            output_widget=output_widget,
            warning_popup=TkWarningPopup(),
            confirmation_popup=TkConfirmPopup(),
            search_bar=input_widget.searchbar,
            )
