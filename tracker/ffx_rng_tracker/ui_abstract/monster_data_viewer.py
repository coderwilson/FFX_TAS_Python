from dataclasses import dataclass, field

from ..data.monsters import MONSTERS
from ..ui_functions import format_monster_data
from .input_widget import InputWidget
from .output_widget import OutputWidget


@dataclass
class MonsterDataViewer:
    """Widget used to display monster's data."""

    monster_selection_widget: InputWidget
    search_bar_widget: InputWidget
    output_widget: OutputWidget
    monster_data: dict[str, str] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.monster_data = {k: format_monster_data(v)
                             for k, v in MONSTERS.items()}

    def callback(self, *_, **__) -> None:
        monster_name = self.monster_selection_widget.get_input()
        try:
            monster_data = self.monster_data[monster_name]
        except KeyError:
            return
        self.output_widget.print_output(monster_data)

    def filter_monsters(self, *_, **__) -> None:
        filter = self.search_bar_widget.get_input().lower()
        monsters_names = [name
                          for name, data in self.monster_data.items()
                          if filter in name or filter in data.lower()
                          ]
        monsters_names.sort()
        self.monster_selection_widget.set_input(monsters_names)
