import logging

import memory.main
import xbox
from players.base import Player

logger = logging.getLogger(__name__)


class WakkaImpl(Player):
    def __init__(self):
        super().__init__("Wakka", 4, [0, 19, 1])

    def overdrive(self, reels:str="element"):
        logger.info("Wakka overdrive activating")
        while not memory.main.other_battle_menu():
            xbox.tap_left()
        while not memory.main.interior_battle_menu():
            xbox.tap_b()
            if self.overdrive_failed():
                return
        if reels == "attack":
            self._navigate_to_position(1, battle_cursor=memory.main.battle_cursor_3)
        while memory.main.interior_battle_menu():
            xbox.tap_b()

        memory.main.wait_frames(1)
        xbox.menu_b()
        xbox.menu_b()

        while not self.overdrive_active():
            if self.overdrive_failed():
                return
        if reels == "element":
            memory.main.wait_frames(74)
            logger.info("Hit Overdrive")
            xbox.tap_b()  # First reel
            memory.main.wait_frames(10)
            xbox.tap_b()  # Second reel
            memory.main.wait_frames(5)
            xbox.tap_b()  # Third reel
        elif reels == "attack":
            memory.main.wait_frames(78)
            logger.info("Hit Overdrive")
            xbox.tap_b()  # First reel
            memory.main.wait_frames(15)
            xbox.tap_b()  # Second reel
            memory.main.wait_frames(25)
            xbox.tap_b()  # Third reel
        while memory.main.battle_active() and not memory.main.turn_ready():
            if memory.main.game_over():
                return
            if memory.main.special_text_open():
                # Mostly used for Extractor fight.
                xbox.tap_b()

    def overdrive_active(self):
        return memory.main.read_val(0x00DA0BD0, 1) != 0
    
    def overdrive_failed(self):
        # if memory.main.turn_ready():
        #     logger.warning(f"Turn is ready?!")
        #     return True
        if memory.main.game_over():
            logger.warning(f"Game Over?!")
            return True
        if not self.is_turn():
            logger.warning(f"It is not Wakka's turn.")
            return True
        return False


Wakka = WakkaImpl()
