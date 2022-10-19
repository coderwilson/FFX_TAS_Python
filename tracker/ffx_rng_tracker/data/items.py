import csv
from dataclasses import dataclass

from .file_functions import get_resource_path


@dataclass(frozen=True)
class Item:
    name: str
    index: int

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class ItemDrop:
    item: Item
    quantity: int
    rare: bool

    def __str__(self) -> str:
        string = f"{self.item} x{self.quantity}"
        if self.rare:
            string += " (rare)"
        return string


def _get_items(file_path: str) -> tuple[str]:
    """Retrieves the items names."""
    absolute_file_path = get_resource_path(file_path)
    with open(absolute_file_path) as file_object:
        file_reader = csv.reader(file_object, delimiter=",")
        # skips first line
        next(file_reader)
        items = []
        for line in file_reader:
            items.append(Item(line[1], line[0]))
    return tuple(items)


ITEMS = _get_items("tracker\\data\\items.csv")
