import logging

import memory.main
import xbox
from players.base import Player

logger = logging.getLogger(__name__)


class YunaImpl(Player):
    def __init__(self):
        super().__init__("Yuna", 1, [0, 23, 22, 1])

    def overdrive(self, aeon_num: int = 0):
        while not memory.main.other_battle_menu():
            xbox.tap_left()
        while not memory.main.interior_battle_menu():
            xbox.tap_b()
        while memory.main.battle_cursor_3() != aeon_num:
            if aeon_num > memory.main.battle_cursor_3():
                xbox.tap_down()
            else:
                xbox.tap_up()
        while memory.main.interior_battle_menu():
            xbox.tap_b()
            if memory.main.game_over():
                return False


Yuna = YunaImpl()
