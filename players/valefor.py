import memory.main
import xbox
import logging
logger = logging.getLogger(__name__)
from players.aeon import Aeon


class ValeforImpl(Aeon):
    def __init__(self):
        super().__init__("Valefor", 8, [203, 204, 21])

    def overdrive(self, overdrive_num, sin_fin=False):
        logger.debug("Attempting Valefor overdrive!")
        logger.debug(f"Charge percentage: {memory.main.get_overdrive_battle(character=7) * 5}%")
        logger.debug(f"Charge percentage: {memory.main.get_overdrive_battle(character=8) * 5}%")
        while not memory.main.other_battle_menu():
            xbox.tap_left()
        self._navigate_to_single_column_index(
            overdrive_num, memory.main.battle_cursor_2
        )
        while memory.main.other_battle_menu():
            xbox.tap_b()
        if sin_fin and memory.main.battle_line_target() == 0:
            xbox.tap_down()
            xbox.tap_left()
        self._tap_targeting()


Valefor = ValeforImpl()
