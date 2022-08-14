import tkinter as tk

from .output_widget import TkOutputWidget
from ..data.constants import EquipmentType
from ..ui_functions import get_encounter_predictions, get_equipment_types
from ..utils import treeview


class TkSeedInfoOutputWidget(TkOutputWidget):

    def get_regex_patterns(self) -> dict[str, str]:
        return {'equipment': str(EquipmentType.ARMOR)}


class TkSeedInfo(tk.Frame):
    """Widget that shows general information
    about the seed.
    """
    def __init__(self, parent, seed, *args, **kwargs) -> None:
        super().__init__(parent, *args, *kwargs)

        self.output_widget = TkSeedInfoOutputWidget(self, wrap='none')
        self.output_widget.pack(expand=True, fill='both')

        encounter_predictions = treeview(get_encounter_predictions(seed), 1)
        data = [
            f'Seed number: {seed}',
            'Encounters predictions:\n' + encounter_predictions,
            get_equipment_types(seed, 50, 2),
        ]
        output = '\n\n'.join(data)

        self.output_widget.print_output(treeview(output))
