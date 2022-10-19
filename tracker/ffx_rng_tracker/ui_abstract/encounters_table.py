import re
from dataclasses import dataclass

from ..data.encounter_formations import ZONES
from ..events.encounter import MultizoneRandomEncounter
from ..events.main import Event
from .encounters_tracker import EncountersTracker
from .input_widget import InputWidget


@dataclass
class EncountersTable(EncountersTracker):
    search_bar: InputWidget

    def __post_init__(self) -> None:
        super().__post_init__()
        self.paddings = self._get_paddings()

    def events_to_string(self, events: list[Event]) -> str:
        output = []
        for event in events:
            match event:
                case MultizoneRandomEncounter():
                    if not output:
                        zones = []
                        for zone in event.zones:
                            zone_name = ZONES[zone].name
                            padding = self.paddings[zone]
                            zones.append(f'{zone_name:{padding}}')
                        first_line = (' ' * 26) + ''.join(zones)
                        output.append(first_line)
                        output.append('=' * len(first_line))
                    for count, enc in enumerate(event.encounters):
                        # append a spacer before appending encounters
                        # but only if there is already data
                        if output and count == 0:
                            enc = event.encounters[0]
                            line = (f'{enc.index:4}|{enc.random_index:4}|'
                                    f'{enc.zone_index:3}: {enc.condition:10} ')
                        padding = self.paddings[enc.name]
                        line += f'{enc.formation:{padding}}'
                    output.append(line)

        important_monsters = self.search_bar.get_input()
        for symbol in (',', '-', '/', '\\', '.'):
            important_monsters = important_monsters.replace(symbol, ' ')
        important_monsters = important_monsters.split()
        pattern = '(?i)' + '|'.join(
            [re.escape(m.strip()) for m in important_monsters])
        self.output_widget.regex_patterns['important monster'] = pattern

        return '\n'.join(output)

    def edit_output(self, output: str) -> str:
        output = output.replace(' Normal', '       ')
        return output

    def _get_paddings(self) -> dict[str, int]:
        paddings = {}
        for zone, data in ZONES.items():
            padding = len(zone)
            for f in data.formations:
                padding = max(padding, len(', '.join([str(m) for m in f])))
            paddings[zone] = padding + 1
        return paddings
