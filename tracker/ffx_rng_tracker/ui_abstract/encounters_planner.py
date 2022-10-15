import re
from dataclasses import dataclass

from ..data.monsters import MONSTERS
from .encounters_tracker import EncountersTracker
from .input_widget import InputWidget


@dataclass
class EncountersPlanner(EncountersTracker):
    search_bar: InputWidget

    def edit_output(self, output: str) -> str:
        output = output.replace('Simulation: ', 'Simulation')
        output = output.replace('Boss: ', 'Boss')

        monsters_tally = {}
        for monster in MONSTERS.values():
            name = monster.name
            index = 0
            while True:
                try:
                    index_1 = output.index(f', {name}', index)
                except ValueError:
                    index_1 = len(output) + 1
                try:
                    index_2 = output.index(f': {name}', index)
                except ValueError:
                    index_2 = len(output) + 1
                index = min(index_1, index_2)
                if index > len(output):
                    break
                tally = monsters_tally.get(name, 0) + 1
                monsters_tally[name] = tally
                index += len(name) + 2
                output = f'{output[:index]}{{{tally}}}{output[index:]}'

        captured_monsters = [re.escape(m)
                             for m, t in monsters_tally.items()
                             if t >= 10]
        pattern = '(?i)' + '|'.join(captured_monsters)
        self.output_widget.regex_patterns['captured monster'] = pattern

        important_monsters = self.search_bar.get_input()
        for symbol in (',', '-', '/', '\\', '.'):
            important_monsters = important_monsters.replace(symbol, ' ')
        important_monsters = important_monsters.split()
        pattern = '(?i)' + '|'.join(
            [re.escape(m.strip()) for m in important_monsters])
        self.output_widget.regex_patterns['important monster'] = pattern

        return super().edit_output(output)
