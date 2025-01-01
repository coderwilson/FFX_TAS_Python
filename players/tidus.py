import logging

import memory.main
import vars
import xbox
import time
from players.base import Player
from rng_track import current_battle_formation, luck_check

game_vars = vars.vars_handle()

logger = logging.getLogger(__name__)


class TidusImpl(Player):
    def __init__(self):
        super().__init__("Tidus", 0, [0, 19, 20, 22, 1])

    def overdrive(self, direction=None, version: int = 0, character=99):
        if game_vars.god_mode():
            logger.warning("Attempting to force a crit, per settings")
            # Determine enemy name and luck stat
            enemies = current_battle_formation()
            if len(enemies) != 0:
                try:
                    if target_id is None:
                        # In multi-enemy battles, the first enemy is almost always the boss.
                        luck_value = luck_check(enemies[0])
                    else:
                        luck_value = luck_check(enemies[target_id-20])
                except:
                    luck_value = 15
            else:
                luck_value = 15
            # Force forward to the next crit.
            memory.main.future_attack_will_crit(
                character=self.id,
                char_luck=self.luck(),
                enemy_luck=luck_value
            )
        while not memory.main.other_battle_menu():
            xbox.tap_left()
        while not memory.main.interior_battle_menu():
            xbox.tap_b()
        self._navigate_to_position(version, battle_cursor=memory.main.battle_cursor_3)
        while memory.main.interior_battle_menu():
            xbox.tap_b()
        if character != 99 and memory.main.get_enemy_current_hp()[character - 20] != 0:
            while (
                character != memory.main.battle_target_id()
                and memory.main.get_enemy_current_hp()[character - 20] != 0
            ):
                xbox.tap_left()
        elif direction:
            if direction == "left":
                xbox.tap_left()
        while not self.overdrive_active():
            xbox.tap_b()
        memory.main.wait_frames(11)
        xbox.tap_b()  # First try pog
        logger.info("Hit Overdrive")

        # Backup attempts, used with low-quality computers only. No impact normally.
        memory.main.wait_frames(10)
        xbox.tap_b()  # Extra attempt in case of miss
        memory.main.wait_frames(10)
        xbox.tap_b()  # Extra attempt in case of miss
        memory.main.wait_frames(11)
        xbox.tap_b()  # Extra attempt in case of miss
        memory.main.wait_frames(11)
        xbox.tap_b()  # Extra attempt in case of miss
        memory.main.wait_frames(12)
        xbox.tap_b()  # Extra attempt in case of miss

    def overdrive_active(self):
        return memory.main.read_val(0x00F3D6F4, 1) == 4

    def flee(self):
        logger.debug("Fleeing with Tidus")
        self.navigate_to_battle_menu(20)
        while not memory.main.other_battle_menu():
            xbox.tap_b()
        self._navigate_to_position(0)
        while memory.main.other_battle_menu():
            xbox.tap_b()
        self._tap_targeting()


Tidus = TidusImpl()
