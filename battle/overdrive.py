import logging

import battle.main
import memory.main
import screen
import xbox

FFXC = xbox.controller_handle()

logger = logging.getLogger(__name__)


def yojimbo(gil_value: int = 263000):
    logger.info("Yojimbo overdrive")
    screen.await_turn()
    if not screen.turn_aeon():
        return
    while memory.main.battle_menu_cursor() != 35:
        xbox.tap_up()
    memory.main.wait_frames(6)
    xbox.menu_b()
    logger.info("Selecting amount")
    memory.main.wait_frames(15)
    battle.main.calculate_spare_change_movement(gil_value)
    logger.info(f"Amount selected: {gil_value}")
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    return
