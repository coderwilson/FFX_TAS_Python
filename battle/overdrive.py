import logging

import battle.main
import battle.utils
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
    xbox.tap_left()
    xbox.tap_left()
    xbox.tap_left()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_left()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_left()
    xbox.tap_up()
    xbox.tap_up()
    logger.info("Amount selected")
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    return
