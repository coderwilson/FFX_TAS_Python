import logging
from enum import IntEnum
from typing import List, Optional

import memory.main
import xbox

logger = logging.getLogger(__name__)


class PlayerMagicNumbers(IntEnum):
    CHAR_STRUCT_SIZE = 0x94
    CHAR_STAT_POINTER = 0x003AB9B0
    BATTLE_STRUCT_SIZE = 0x90
    BATTLE_STATE_STRUCT_SIZE = 0xF90
    BATTLE_STATE_STRUCT_POINTER = 0x00D334CC
    CUR_HP = 0x00D32078
    MAX_HP = 0x00D32080
    BATTLE_CUR_HP = 0x00F3F7A4
    BATTLE_MAX_HP = 0x00F3F7A8
    LUCK = 0x34
    ACCURACY = 0x36
    BATTLE_OVERDRIVE = 0x5BC
    DEFENDING = 0x617
    OVERDRIVE = 0x39
    AFFECTION_POINTER = 0x00D2CABC
    SLVL = 0x00D32097
    RNG_COMP = 0x7FFFFFFF
    ESCAPED = 0xDC8
    ACTIVE_BATTLE_SLOTS = 0x00F3F76C
    BACKLINE_BATTLE_SLOTS = 0x00D2C8A3
    ARMOR_ID = 1
    WEAPON_ID = 0


class Player:
    def __init__(self, name: str, id: int, battle_menu: List[int]):
        self.name = name
        self.id = id
        self.struct_offset = id * PlayerMagicNumbers.CHAR_STRUCT_SIZE
        self.char_rng = 20 + id
        self.battle_menu = battle_menu

    @property
    def actor_id(self):
        return self.id + 1

    def __eq__(self, other):
        if isinstance(other, int):
            return self.id == other
        else:
            return self.id == other.id

    def __hash__(self):
        return self.id

    def __lt__(self, other):
        if isinstance(other, int):
            return self.id < other
        else:
            return self.id < other.id

    def __gt__(self, other):
        return not self == other and not self < other

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    def __ne__(self, other):
        return not self == other

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def _read_char_offset_address(self, address):
        return memory.main.read_val(address + self.struct_offset)

    def _read_char_battle_offset_address(self, address, offset):
        return memory.main.read_val(
            address + ((PlayerMagicNumbers.BATTLE_STRUCT_SIZE * offset))
        )

    def _read_char_battle_state_address(self, offset):
        pointer = memory.main.read_val(
            PlayerMagicNumbers.BATTLE_STATE_STRUCT_POINTER, 4
        )
        new_offset = (PlayerMagicNumbers.BATTLE_STATE_STRUCT_SIZE * self.id) + offset
        return memory.main.read_val(pointer + new_offset, 1, find_base=False)

    def _read_char_stat_offset_address(self, address):
        pointer = memory.main.read_val(PlayerMagicNumbers.CHAR_STAT_POINTER, 4)
        return memory.main.read_val(
            pointer + self.struct_offset + address, 1, find_base=False
        )

    def _target_specific_id(self, target_id: int, direction: str = "l"):
        direction = direction or "l"
        if target_id < 20:
            friendly_target = True
        else:
            friendly_target = False
        if (
            not friendly_target
            and memory.main.get_enemy_current_hp()[target_id - 20] != 0
        ):
            while memory.main.battle_target_id() != target_id:
                if direction == "l" or direction == "left":
                    if memory.main.battle_target_id() < 20:
                        direction = "u"
                    xbox.tap_left()
                elif direction == "r" or direction == "right":
                    if memory.main.battle_target_id() < 20:
                        direction = "d"
                    xbox.tap_right()
                elif direction == "u" or direction == "up":
                    if memory.main.battle_target_id() < 20:
                        direction = "l"
                    xbox.tap_up()
                elif direction == "d" or direction == "down":
                    if memory.main.battle_target_id() < 20:
                        direction = "r"
                    xbox.tap_down()
        elif friendly_target:
            while memory.main.battle_target_id() != target_id:
                if direction == "l" or direction == "left":
                    if memory.main.battle_target_id() >= 20:
                        direction = "u"
                    xbox.tap_left()
                elif direction == "r" or direction == "right":
                    if memory.main.battle_target_id() >= 20:
                        direction = "d"
                    xbox.tap_right()
                elif direction == "u" or direction == "up":
                    if memory.main.battle_target_id() >= 20:
                        direction = "l"
                    xbox.tap_up()
                elif direction == "d" or direction == "down":
                    if memory.main.battle_target_id() >= 20:
                        direction = "r"
                    xbox.tap_down()

    def attack(
        self,
        target_id: Optional[int] = None,
        direction_hint: Optional[str] = "u",
        record_results: bool = False,
    ):
        skip_direction = False
        if target_id is None:
            logger.debug("Attack enemy, first targetted.")
        elif target_id in range(7):
            logger.debug(f"Attack player character {target_id}")
        elif memory.main.get_enemy_current_hp()[target_id - 20] == 0:
            logger.debug(
                f"Enemy {target_id} is not attack-able. Resorting to basic attack."
            )
            skip_direction = True
        else:
            logger.debug(
                f"Attacking a specific target with id {target_id}, direction hint is {direction_hint}"
            )
        if not memory.main.turn_ready():
            while not memory.main.turn_ready():
                if memory.main.battle_complete():
                    return
        attack_menu_id = [x for x in [0, 203, 207, 210, 216] if x in self.battle_menu][
            0
        ]
        self.navigate_to_battle_menu(attack_menu_id)
        while memory.main.main_battle_menu():
            xbox.tap_b()
            if memory.main.battle_complete():
                return
        if target_id is not None and not skip_direction:
            self._target_specific_id(target_id, direction_hint)
        if record_results:
            xbox.tap_b()
            xbox.tap_b()
            xbox.tap_b()
        else:
            self._tap_targeting()

    # spell_id should become an enum at some point
    def cast_black_magic_spell(
        self,
        spell_id: int,
        target_id: Optional[int] = None,
        direction: Optional[str] = None,
    ):
        if target_id is None:
            logger.debug(f"Casting {spell_id}")
        else:
            logger.debug(
                f"Casting {spell_id} on a specific target with id {target_id}, direction is {direction}"
            )
        try:
            self.navigate_to_battle_menu(21)
        except:
            return
        while memory.main.main_battle_menu():
            xbox.tap_b()
        self._navigate_to_position(spell_id)
        while memory.main.other_battle_menu():
            xbox.tap_b()
        if target_id is not None:
            self._target_specific_id(target_id, direction)
        elif direction:
            direction = direction.lower()
            if direction == "right" or direction == "r":
                xbox.tap_right()
            elif direction == "left" or direction == "l":
                xbox.tap_left()
            elif direction == "up" or direction == "u":
                xbox.tap_up()
            elif direction == "down" or direction == "d":
                xbox.tap_down()
            elif direction == "l2":
                xbox.tap_left()
                xbox.tap_left()
            elif direction == "rd":
                xbox.tap_right()
                xbox.tap_down()
            elif direction == "right2" or direction == "r2":
                xbox.tap_right()
                xbox.tap_right()
                xbox.tap_down()
            elif direction == "d2":
                xbox.tap_down()
                xbox.tap_down()
            else:
                logger.error(f"UNSURE DIRECTION: {direction}")
                raise ValueError("Unsure direction")
        self._tap_targeting()

    def skill(self):
        raise NotImplementedError()

    def defend(self):
        logger.debug(f"Defending with {self}")
        # Update matches memory.main.turn_ready.
        # Updated 11/27/22, still to be validated.

        # Make sure we are not already in defend state_berserk
        while self.is_defending() == 1:
            pass
        memory.main.wait_frames(1)  # Buffer for safety

        result = 0
        # Now tap to defending status.
        while result == 0 and memory.main.battle_active():
            result = self.is_defending()
            if result == 0:
                xbox.tap_y()
        memory.main.wait_frames(1)  # Buffer for safety
        return True

    def navigate_to_battle_menu(self, target: int):
        """Different characters have different menu orders."""
        current_position = memory.main.battle_menu_cursor()
        while current_position == 255:
            current_position = memory.main.battle_menu_cursor()
        target_position = self.battle_menu.index(target)
        while current_position != target:
            if current_position == 255:
                pass
            elif self.battle_menu.index(current_position) > target_position:
                xbox.tap_up()
            else:
                xbox.tap_down()
            current_position = memory.main.battle_menu_cursor()

    def luck(self) -> int:
        return self._read_char_stat_offset_address(PlayerMagicNumbers.LUCK)

    def accuracy(self) -> int:
        return self._read_char_stat_offset_address(PlayerMagicNumbers.ACCURACY)

    def _navigate_to_position(
        self, position, battle_cursor=memory.main.battle_cursor_2
    ):
        while battle_cursor() == 255:
            pass
        if battle_cursor() != position:
            logger.debug(
                f"Wrong position targeted {battle_cursor() % 2}, {position % 2}"
            )
            while battle_cursor() % 2 != position % 2:
                if battle_cursor() < position:
                    xbox.tap_right()
                else:
                    xbox.tap_left()
            while battle_cursor() != position:
                logger.debug(f"Battle_cursor: {battle_cursor()}")
                if battle_cursor() > position:
                    xbox.tap_up()
                else:
                    xbox.tap_down()

    def _tap_targeting(self):
        logger.debug(
            f"In Tap Targeting, Class Edition. Not battle menu: {not memory.main.main_battle_menu()}, Battle active: {memory.main.battle_active()}"
        )
        while (not memory.main.main_battle_menu()) and memory.main.battle_active():
            xbox.tap_b()
        logger.debug(
            f"Done. Not battle menu: {not memory.main.main_battle_menu()}, Battle active: {memory.main.battle_active()}"
        )

    def affection(self) -> int:
        if self.id == 0:
            return 255
        return memory.main.read_val(
            PlayerMagicNumbers.AFFECTION_POINTER + ((4 * self.id)), 1
        )

    def _navigate_to_single_column_index(self, position, cursor):
        while cursor() != position:
            if cursor() < position:
                xbox.tap_down()
            else:
                xbox.tap_up()

    def next_crits(self, enemy_luck: int, length: int = 20) -> List[int]:
        """Note that this says the number of increments, so the previous roll will be a hit, and this one will be the crit."""
        results = []
        cur_rng = memory.main.rng_from_index(self.char_rng)
        cur_rng = memory.main.roll_next_rng(cur_rng, self.char_rng)
        cur_rng = memory.main.roll_next_rng(cur_rng, self.char_rng)
        index = 2
        while len(results) < length:
            crit_roll = memory.main.s32(cur_rng & PlayerMagicNumbers.RNG_COMP) % 101
            crit_chance = self.luck() - enemy_luck
            if crit_roll < crit_chance:
                results.append(index)
                index += 1
            cur_rng = memory.main.roll_next_rng(cur_rng, self.char_rng)
        return results

    def next_crit(self, enemy_luck) -> int:
        return self.next_crits(enemy_luck, length=1)[0]

    def overdrive(self, *args, **kwargs):
        raise NotImplementedError()

    def overdrive_active(self):
        raise NotImplementedError()

    def overdrive_percent(self, combat=False) -> int:
        if combat:
            return self._read_char_battle_state_address(
                PlayerMagicNumbers.BATTLE_OVERDRIVE
            )
        else:
            return self._read_char_stat_offset_address(PlayerMagicNumbers.OVERDRIVE)

    def in_combat(self):
        return memory.main.battle_active()

    def has_overdrive(self) -> bool:
        # Passed variable now does nothing, 11/30, clean up if the below logic works.
        return self.overdrive_percent(combat=self.in_combat()) == 100

    def is_turn(self) -> bool:
        return memory.main.get_battle_char_turn() == self.id

    def in_danger(self, danger_threshold) -> bool:
        logger.debug(f"Danger check: {self.id}")
        logger.debug(self.in_combat())
        logger.debug(self.hp(self.in_combat()))
        return self.hp(self.in_combat()) <= danger_threshold

    def is_dead(self) -> bool:
        return memory.main.state_dead(self.id)

    def is_status_ok(self) -> bool:
        if not self.active():
            return True
        return not any(
            func(self.id)
            for func in [
                memory.main.state_petrified,
                memory.main.state_confused,
                memory.main.state_dead,
                memory.main.state_berserk,
                memory.main.state_sleep,
            ]
        )

    def escaped(self) -> bool:
        return self._read_char_battle_state_address(PlayerMagicNumbers.ESCAPED)

    def is_defending(self) -> int:
        defend_byte = self._read_char_battle_state_address(
            offset=PlayerMagicNumbers.DEFENDING
        )
        result = (defend_byte >> 3) & 1
        if self.id != memory.main.get_battle_char_turn():
            return 9
        return result

    def hp(self, combat=False) -> int:
        if not combat:
            return self._read_char_offset_address(PlayerMagicNumbers.CUR_HP)
        else:
            return memory.main.get_battle_hp()[self.battle_slot()]
            #return self._read_char_battle_offset_address(
            #    PlayerMagicNumbers.BATTLE_CUR_HP, self.battle_slot()
            #)

    def max_hp(self, combat=False) -> int:
        if not combat:
            return self._read_char_offset_address(PlayerMagicNumbers.MAX_HP)
        else:
            return self._read_char_battle_offset_address(
                PlayerMagicNumbers.BATTLE_MAX_HP, self.battle_slot()
            )

    def active(self) -> bool:
        return self in memory.main.get_active_battle_formation()

    def battle_slot(self) -> int:
        for i in range(0, 3):
            if (
                memory.main.read_val(PlayerMagicNumbers.ACTIVE_BATTLE_SLOTS + (2 * i))
                == self.id
            ):
                
                #logger.debug(f"Char {self.id} in slot {i}")
                return i

        offset = 0
        for i in range(0, 7):
            val = memory.main.read_val(PlayerMagicNumbers.BACKLINE_BATTLE_SLOTS + i)
            if val == 255:
                offset += 1
                continue
            elif val == self.id:
                return i + 3 - offset
        return 255

    def formation_slot(self) -> int:
        try:
            return memory.main.get_order_seven().index(self.id)
        except Exception:
            return 255

    def slvl(self) -> int:
        return self._read_char_offset_address(PlayerMagicNumbers.SLVL)

    def armors(self) -> List[memory.main.Equipment]:
        equipments = memory.main.all_equipment()
        return [
            x
            for x in equipments
            if (
                x.owner() == self.id
                and x.equipment_type() == PlayerMagicNumbers.ARMOR_ID
            )
        ]

    def equipped_armor(self) -> memory.main.Equipment:
        return [x for x in self.armors() if x.is_equipped()][0]

    def weapons(self) -> List[memory.main.Equipment]:
        equipments = memory.main.all_equipment()
        return [
            x
            for x in equipments
            if (
                x.owner() == self.id
                and x.equipment_type() == PlayerMagicNumbers.WEAPON_ID
            )
        ]

    def equipped_weapon(self) -> memory.main.Equipment:
        return [x for x in self.weapons() if x.is_equipped()][0]

    def _swap_battle(self, weapon: bool, ability: Optional[List[int]] = None):
        if weapon:
            menu_index = 0
            equip_func = self.weapons
        else:
            menu_index = 1
            equip_func = self.armors
        while memory.main.main_battle_menu():
            xbox.tap_right()
        self._navigate_to_single_column_index(menu_index, memory.main.battle_cursor_2)
        while memory.main.other_battle_menu():
            xbox.tap_b()
        if ability is not None:
            for i, equip in enumerate(equip_func()):
                if set(ability).issubset(set(equip.abilities())):
                    equip_index = i
                    break
        else:
            equip_index = 0
        logger.debug(f"Equip is in index {equip_index}.")
        self._navigate_to_single_column_index(equip_index, memory.main.battle_cursor_3)
        while memory.main.interior_battle_menu():
            xbox.tap_b()

    def swap_battle_weapon(
        self, ability: Optional[List[int]] = None, named_equip: Optional[str] = None
    ):
        if named_equip is not None:
            if named_equip == "baroque":
                ability = [0x8063, 255, 255, 255]
            elif named_equip == "brotherhood":
                ability = [32867, 32868, 32810, 32768]
        self._swap_battle(True, ability)

    def swap_battle_armor(self, ability: Optional[List[int]] = None):
        self._swap_battle(False, ability)

    def main_menu_index(self) -> int:
        return memory.main.get_character_index_in_main_menu(self.id)
