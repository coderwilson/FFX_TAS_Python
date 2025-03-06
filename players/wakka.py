import logging

import memory.main
import battle.main
import xbox
from players.base import Player

logger = logging.getLogger(__name__)


class WakkaImpl(Player):
    def __init__(self):
        super().__init__("Wakka", 4, [0, 19, 1])

    def overdrive(self):
        logger.info("Wakka overdrive activating")
        while not memory.main.other_battle_menu():
            xbox.tap_left()
        while not memory.main.interior_battle_menu():
            xbox.tap_b()
        while memory.main.interior_battle_menu():
            xbox.tap_b()

        memory.main.wait_frames(1)
        xbox.menu_b()

        while not self.overdrive_active():
            pass
        memory.main.wait_frames(74)
        logger.info("Hit Overdrive")
        xbox.tap_b()  # First reel
        memory.main.wait_frames(10)
        xbox.tap_b()  # Second reel
        memory.main.wait_frames(5)
        xbox.tap_b()  # Third reel
        while memory.main.battle_active() and not memory.main.turn_ready():
            if memory.main.special_text_open():
                # Mostly used for Extractor fight.
                xbox.tap_b()

    def overdrive_active(self):
        return memory.main.read_val(0x00DA0BD0, 1) != 0

    def aim(self):
        # Assumes we have already learned the Aim ability, and no others.
        while memory.main.battle_menu_cursor() != 20:
            self.navigate_to_battle_menu(20)
        
        while not memory.main.other_battle_menu():
            xbox.tap_b()
        while memory.main.other_battle_menu():
            xbox.tap_b()  # Use the Aim command
        battle.main.tap_targeting()


Wakka = WakkaImpl()
