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

    def overdrive(self, direction=None, version: int = 99, character=99):
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
        if version == 99:
            count = memory.main.tidus_od_count()
            logger.debug(f"Checking overdrive count: {count}")
            if count < 10:
                version = 0
                self._navigate_to_position(0, battle_cursor=memory.main.battle_cursor_3)
            #elif count < 30:
                #version = 1
            #    self._navigate_to_position(1, battle_cursor=memory.main.battle_cursor_3)
            elif count < 80:
                #version = 2
                #self._navigate_to_position(2, battle_cursor=memory.main.battle_cursor_3)
                # Energy Rain may be undesirable in general.
                version = 1
                self._navigate_to_position(1, battle_cursor=memory.main.battle_cursor_3)
            else:
                version = 3
                self._navigate_to_position(3, battle_cursor=memory.main.battle_cursor_3)
        else:
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
        xbox.tap_b()
        xbox.tap_b()
        while not self.overdrive_active():
            pass
        if version == 0:
            memory.main.wait_frames(13)
        elif version == 1:
            memory.main.wait_frames(12)
        elif version == 2:
            memory.main.wait_frames(11)
        elif version == 3:
            memory.main.wait_frames(11)
        else:
            # Backup. I don't know how this can occur.
            memory.main.wait_frames(10)
        xbox.tap_b()  # First try pog
        logger.info("Hit Overdrive")

        # Backup attempts, used with low-quality computers only. No impact normally.
        memory.main.wait_frames(8)
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

Tidus = TidusImpl()
