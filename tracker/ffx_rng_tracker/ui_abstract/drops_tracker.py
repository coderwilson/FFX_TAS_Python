from ..data.monsters import MONSTERS
from ..events.parsing_functions import (ParsingFunction, parse_bribe,
                                        parse_death, parse_kill,
                                        parse_party_change, parse_roll,
                                        parse_steal)
from .base_tracker import TrackerUI


class DropsTracker(TrackerUI):
    notes_file = 'drops_notes.txt'

    def get_parsing_functions(self) -> dict[str, ParsingFunction]:
        parsing_functions = {
            'roll': parse_roll,
            'waste': parse_roll,
            'advance': parse_roll,
            'steal': parse_steal,
            'kill': parse_kill,
            'death': parse_death,
            'party': parse_party_change,
            'bribe': parse_bribe,
        }
        return parsing_functions

    def edit_input(self, input_text: str) -> str:
        input_lines = input_text.splitlines()
        for index, line in enumerate(input_lines):
            match line.lower().split():
                case [monster, *params] if monster in MONSTERS:
                    line = ' '.join(['kill', monster, *params])
            input_lines[index] = line
        return '\n'.join(input_lines)

    def edit_output(self, output: str) -> str:
        if output.find('///') >= 0:
            output = output.split('///')[-1]
            output = output[output.find('\n') + 1:]
        return output
