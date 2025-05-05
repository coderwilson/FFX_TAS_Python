from players.base import Player
import memory.main
from memory.main import battle_cursor_3
import time
import xbox
FFXC = xbox.controller_handle()
import logging
logger = logging.getLogger(__name__)


class LuluImpl(Player):
    def __init__(self):
        super().__init__("Lulu", 5, [0, 20, 21, 1])
        
    def overdrive(self, spell_pos=0):
        while not memory.main.other_battle_menu():
            xbox.tap_left()
        while not memory.main.interior_battle_menu():
            xbox.menu_b()
    
        while battle_cursor_3() != spell_pos:
            while battle_cursor_3() != spell_pos:
                if battle_cursor_3() % 2 != spell_pos % 2:
                    xbox.tap_right()
                elif battle_cursor_3() < spell_pos:
                    xbox.tap_down()
                else:
                    xbox.tap_up()
            memory.main.wait_frames(1)
        xbox.tap_confirm()
        xbox.tap_confirm()
        xbox.tap_confirm()
        xbox.tap_confirm()
        xbox.tap_confirm()

        logger.warning("Lulu overdrive start")
        start_time = time.time()
        duration = 10  # Number of seconds to perform the overdrive.
        while time.time() < start_time + duration:


            '''
            FFXC.set_value('d_pad', 0)
            FFXC.set_value('d_pad', 4)
            memory.main.wait_frames(1)
            FFXC.set_value('d_pad', 0)
            FFXC.set_value('d_pad', 8)
            memory.main.wait_frames(1)
            '''

            FFXC.right_stick(-1,-1)
            memory.main.wait_frames(1)
            FFXC.right_stick(-1,1)
            memory.main.wait_frames(1)
            FFXC.right_stick(1,1)
            memory.main.wait_frames(1)
            FFXC.right_stick(1,-1)
            memory.main.wait_frames(1)
        FFXC.right_stick(0,0)
        FFXC.set_value('d_pad', 0)
        logger.warning("Lulu overdrive end")
        


Lulu = LuluImpl()
