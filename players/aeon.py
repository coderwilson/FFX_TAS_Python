import logging
from typing import List

import memory.main
import xbox
from players.base import Player

logger = logging.getLogger(__name__)


class Aeon(Player):
    def __init__(self, name: str, id: int, battle_menu: List[int]):
        super().__init__(name, id, battle_menu)
        self.char_rng = 27

    def _aeon_side_menu(self, target):
        while not memory.main.other_battle_menu():
            xbox.tap_right()
        self._navigate_to_single_column_index(target, memory.main.battle_cursor_2)
        while memory.main.other_battle_menu():
            xbox.tap_b()
        self._tap_targeting()

    def unique(self, direction=None, target_far_line=False):
        self.navigate_to_battle_menu(self.battle_menu[1])
        while not memory.main.other_battle_menu():
            xbox.tap_b()
        # This should be generealized
        if direction == "left":
            xbox.tap_left()
        if target_far_line:
            while not memory.main.battle_line_target():
                xbox.tap_left()
        xbox.tap_b()
        xbox.tap_b()
        self._tap_targeting()

    def shield(self):
        logger.debug("Using Aeon Shield command")
        self._aeon_side_menu(0)

    def boost(self):
        logger.debug("Using Aeon Boost command")
        self._aeon_side_menu(1)

    def dismiss(self):
        logger.debug("Dismissing Aeon")
        self._aeon_side_menu(2)

    def overdrive(self, overdrive_num: int):
        while memory.main.main_battle_menu():
            xbox.tap_left()
        self._navigate_to_single_column_index(
            overdrive_num, memory.main.battle_cursor_2
        )
        while memory.main.other_battle_menu():
            xbox.tap_b()
        self._tap_targeting()
