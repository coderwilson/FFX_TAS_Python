import logging

import memory.main
import xbox
from players.base import Player

logger = logging.getLogger(__name__)


class KimahriImpl(Player):
    def __init__(self):
        super().__init__("Kimahri", 3, [0, 20, 1])
    
    def is_overdrive_learned(self, od_name:str) -> bool:
        od_index = self.od_name_to_bit_num(od_name)
        ret_val = bool(memory.main.kim_od_unlocks()[od_index] == 1)
        logger.debug(f"Overdrive '{od_name}' learned: {ret_val}")
        return ret_val


    def od_name_to_bit_num(self, od_name):
        od_name = od_name.lower()
        # Starting from index zero, here are the ones we know.
        if od_name == "jump":
            return 0
        if od_name == "fire breath":
            return 1
        if od_name == "seed cannon":
            return 2
        if od_name == "self-destruct":
            return 3
        if od_name == "thrust kick":
            return 4
        if od_name == "stone breath":
            return 5
        if od_name == "aqua breath":
            return 6
        if od_name == "doom":
            return 7
        if od_name == "white wind":
            return 8
        if od_name == "bad breath":
            return 9
        if od_name == "mighty guard":
            return 10
        if od_name == "nova":
            return 11
        return 99  # No result found.

    def overdrive(self, pos=2,od_name=None, od_array=[1,0,1,0,0,0,0,0,0,0,0,0]):
        if od_name != None:
            bit_index = self.od_name_to_bit_num(od_name=od_name)
            if bit_index != 99:
                pos = bit_index
                for i in range(bit_index):
                    if od_array[i] == 0:
                        pos -= 1
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
