from ..data.encounter_formations import ZONES
from ..events.parsing_functions import (ParsingFunction, parse_encounter,
                                        parse_roll)
from .base_tracker import TrackerUI


class EncountersTracker(TrackerUI):
    """Widget used to track encounters RNG."""

    def get_default_input_data(self) -> str:
        return ''

    def get_parsing_functions(self) -> dict[str, ParsingFunction]:
        parsing_functions = {
            'roll': parse_roll,
            'waste': parse_roll,
            'advance': parse_roll,
            'encounter': parse_encounter,
        }
        return parsing_functions

    def edit_input(self, input_text: str) -> str:
        return input_text

    def edit_output(self, output: str) -> str:
        # if the text contains /// it hides the lines before it
        if output.find('///') >= 0:
            output = output.split('///')[-1]
            output = output[output.find('\n') + 1:]

        # remove icvs
        output_lines = output.splitlines()
        for index, line in enumerate(output_lines):
            if line.endswith(']') and '/' not in line:
                output_lines[index] = line.split('[')[0][:-3]
        output = '\n'.join(output_lines)

        # remove zone names
        for zone in ZONES.values():
            output = output.replace(f' - {zone.name}', '')
            output = output.replace(f'/{zone.name}', '')

        # remove implied information
        output = output.replace(' Normal', '')
        output = output.replace('Encounter ', '')

        return output
