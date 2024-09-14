import logging

import memory.main
import xbox
from players.base import Player

logger = logging.getLogger(__name__)


class KimahriImpl(Player):
    def __init__(self):
        super().__init__("Kimahri", 3, [0, 20, 1])

    def overdrive(self, pos):
        logger.info(f"Kimahri using Overdrive, pos - {pos}")
        while not memory.main.other_battle_menu():
            xbox.tap_left()
        while memory.main.other_battle_menu():
            xbox.menu_b()
        self._navigate_to_position(pos, battle_cursor=memory.main.battle_cursor_3)
        while memory.main.interior_battle_menu():
            xbox.menu_b()
        self._tap_targeting()


Kimahri = KimahriImpl()
