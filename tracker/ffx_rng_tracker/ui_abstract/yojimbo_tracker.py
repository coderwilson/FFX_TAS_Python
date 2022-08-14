from ..data.actions import YOJIMBO_ACTIONS
from ..events.parsing_functions import (ParsingFunction,
                                        parse_compatibility_update,
                                        parse_death, parse_roll,
                                        parse_yojimbo_action)
from .base_tracker import TrackerUI


class YojimboTracker(TrackerUI):
    """Widget used to track Yojimbo rng."""
    notes_file = 'yojimbo_notes.txt'

    def get_parsing_functions(self) -> dict[str, ParsingFunction]:
        parsing_functions = {
            'roll': parse_roll,
            'waste': parse_roll,
            'advance': parse_roll,
            'death': parse_death,
            'compatibility': parse_compatibility_update,
            'yojimboturn': parse_yojimbo_action,
        }
        return parsing_functions

    def edit_input(self, input_text: str) -> str:
        input_lines = input_text.splitlines()
        for index, line in enumerate(input_lines):
            match line.lower().split():
                case ['death', *_]:
                    line = 'death yojimbo'
                case [action_name, *params] if action_name in YOJIMBO_ACTIONS:
                    line = ' '.join(['yojimboturn', action_name, *params])
            input_lines[index] = line
        return '\n'.join(input_lines)

    def edit_output(self, output: str) -> str:
        # if the text contains /// it hides the lines before it
        if output.find('///') >= 0:
            output = output.split('///')[-1]
            output = output[output.find('\n') + 1:]
        return output
