import logging

import battle
import memory
import xbox
from players.base import Player

# Because Auron is special
FFXC = xbox.controller_handle()


logger = logging.getLogger(__name__)


class AuronImpl(Player):
    def __init__(self):
        super().__init__("Auron", 2, [0, 19, 1])

    def overdrive(self, style="dragon fang"):
        while not memory.main.other_battle_menu():
            xbox.tap_left()
        while not memory.main.interior_battle_menu():
            xbox.tap_b()
        logger.info(f"Auron overdrive. Style: {style}")
        # Doing the actual overdrive
        if style == "dragon fang":
            battle.main._navigate_to_position(
                0, battle_cursor=memory.main.battle_cursor_3
            )
            while not self.overdrive_active():
                xbox.tap_b()
            logger.debug("Starting")
            for i in range(2):  # Do it twice in case there's a miss on the first one.
                FFXC.set_value("d_pad", 2)  # down
                memory.main.wait_frames(1)
                FFXC.set_value("d_pad", 0)
                FFXC.set_value("d_pad", 4)  # left
                memory.main.wait_frames(1)
                FFXC.set_value("d_pad", 0)
                FFXC.set_value("d_pad", 1)  # up
                memory.main.wait_frames(1)
                FFXC.set_value("d_pad", 0)
                FFXC.set_value("d_pad", 8)  # right
                memory.main.wait_frames(1)
                FFXC.set_value("d_pad", 0)
                FFXC.set_value("btn_shoulder_l", 1)
                memory.main.wait_frames(1)
                FFXC.set_value("btn_shoulder_l", 0)
                FFXC.set_value("btn_shoulder_r", 1)
                memory.main.wait_frames(1)
                FFXC.set_value("btn_shoulder_r", 0)
                FFXC.set_value("btn_a", 1)
                memory.main.wait_frames(1)
                FFXC.set_value("btn_a", 0)
                FFXC.set_value("btn_b", 1)
                memory.main.wait_frames(1)
                FFXC.set_value("btn_b", 0)
        elif style == "shooting star":
            battle.main._navigate_to_position(
                1, battle_cursor=memory.main.battle_cursor_3
            )
            while not self.overdrive_active():
                xbox.tap_b()
            for i in range(2):  # Do it twice in case there's a miss on the first one.
                FFXC.set_value("btn_y", 1)
                memory.main.wait_frames(1)
                FFXC.set_value("btn_y", 0)
                FFXC.set_value("btn_a", 1)
                memory.main.wait_frames(1)
                FFXC.set_value("btn_a", 0)
                FFXC.set_value("btn_x", 1)
                memory.main.wait_frames(1)
                FFXC.set_value("btn_x", 0)
                FFXC.set_value("btn_b", 1)
                memory.main.wait_frames(1)
                FFXC.set_value("btn_b", 0)
                FFXC.set_value("d_pad", 4)  # left
                memory.main.wait_frames(1)
                FFXC.set_value("d_pad", 0)
                FFXC.set_value("d_pad", 8)  # right
                memory.main.wait_frames(1)
                FFXC.set_value("d_pad", 0)
                FFXC.set_value("btn_b", 1)
                memory.main.wait_frames(1)
                FFXC.set_value("btn_b", 0)

    def overdrive_active(self):
        return memory.main.read_val(0x00F3D6B4, 1) == 4


Auron = AuronImpl()
