import csv

from .file_functions import get_resource_path


def get_text_characters(file_path: str) -> dict[int, str]:
    """Retrieves the character encoding chart used in prize structs."""
    absolute_file_path = get_resource_path(file_path)
    with open(absolute_file_path) as file_object:
        file_reader = csv.reader(file_object, delimiter=",")
        # skips first line
        next(file_reader)
        text_characters = {}
        for line in file_reader:
            text_characters[int(line[0])] = line[2]
    return text_characters


TEXT_CHARACTERS = get_text_characters("tracker\\data\\text_characters.csv")
