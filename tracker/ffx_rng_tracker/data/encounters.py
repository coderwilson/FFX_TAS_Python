import csv
from dataclasses import dataclass
from itertools import count

from .notes import get_notes


@dataclass
class EncounterData:
    name: str
    type: str
    initiative: bool
    label: str
    min: int
    default: int
    max: int


def get_encounters(file_path: str, seed: int) -> list[EncounterData]:
    encounters_notes = get_notes(file_path, seed)
    encounters = {}
    csv_reader = csv.reader(encounters_notes.splitlines())
    for line in csv_reader:
        if line[0].startswith('#'):
            continue
        name = line[0]
        encounter_type = line[1]
        initiative = line[2] == 'true'
        label = line[3]
        if label in encounters:
            for i in count(2):
                new_label = f'{label} #{i}'
                if new_label not in encounters:
                    label = new_label
                    break

        if encounter_type == 'boss':
            min = default = max = 0
        else:
            min = int(line[4])
            default = int(line[5])
            max = int(line[6])
        encounters[label] = EncounterData(
            name=name,
            type=encounter_type,
            initiative=initiative,
            label=label,
            min=min,
            default=default,
            max=max,
        )
    return list(encounters.values())
