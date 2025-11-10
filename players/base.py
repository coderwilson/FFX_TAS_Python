import logging
from enum import IntEnum
from typing import List, Optional
from rng_track import area_formations, current_battle_formation, luck_check

import memory.main
import battle.main
from memory.unlocks import get_unlocked_abilities_by_type
import xbox

logger = logging.getLogger(__name__)

import vars
game_vars = vars.vars_handle()

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
    
    def raw_id(self):
        return self.id

    def update_battle_menu(self, value=[]):
        list = get_unlocked_abilities_by_type(self.id, report=False)

        # Set attack command and (for aeons) their special command.
        if self.id == 8:  # Valefor
            final = [203,204]
        elif self.id == 9:  # Ifrit
            final = [207,208]
        elif self.id == 10:  # Ixion
            final = [210,211]
        elif self.id == 11:  # Shiva
            final = [213,214]
        elif self.id == 12:  # Bahamut
            final = [216,217]
        elif self.id == 13:  # Anima
            final = [219,220]
        elif self.id == 14:  # Yojimbo
            final = [35,87]
            self.battle_menu = final
            return
        elif self.id == 15:  # Cindy (probably doesn't work)
            final = [36,39,86]
        elif self.id == 16:  # Sandy (probably doesn't work)
            final = [36,39,86]
        elif self.id == 17:  # Mindy (probably doesn't work)
            final = [36,39,86]
        elif self.id == 1:
            final = [0,23]
        else:
            final = [0]
        
        if len(list["Skill"]) >= 1:
            final.append(19)
        if len(list["Special"]) >= 1:
            final.append(20)
        if len(list["Black Magic"]) >= 1:
            final.append(21)
        if len(list["White Magic"]) >= 1:
            final.append(22)
        if self.id <= 6:
            final.append(1)
        self.battle_menu = final

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
        return memory.main.read_val(address=address + self.struct_offset, bytes=4)

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
        counter = 0
        if target_id < 20:
            friendly_target = True
        else:
            friendly_target = False
        if (
            not friendly_target
            and memory.main.get_enemy_current_hp()[target_id - 20] != 0
        ):
            while memory.main.battle_target_id() != target_id:
                logger.warning(f"Target mode 1: {target_id}, {memory.main.battle_target_id()}")
                if memory.main.main_battle_menu():
                    logger.warning("Wrong menu active. Returning.")
                    return
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
                counter += 1
                if counter % 5 == 0:
                    if direction in ["r","l"]:
                        direction = "u"
                    else:
                        direction = "r"
        elif friendly_target:
            while memory.main.battle_target_id() != target_id:
                logger.warning("Target mode 2: {target_id}, {memory.main.battle_target_id()}")
                if memory.main.main_battle_menu():
                    logger.warning("Wrong menu active. Returning.")
                    return
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
                counter += 1
                if counter % 5 == 0:
                    if direction in ["r","l"]:
                        direction = "u"
                    else:
                        direction = "r"

    def attack(
        self,
        target_id: Optional[int] = None,
        direction_hint: Optional[str] = "u",
        record_results: bool = False,
        short_taps: bool = False
    ):
        
        skip_direction = False
        if target_id is None:
            logger.debug("Attack enemy, first targetted.")
            skip_direction = True
        elif target_id in range(7):
            logger.debug(f"Attack player character {target_id}")
        elif memory.main.get_enemy_current_hp()[target_id - 20] == 0:
            logger.debug(
                f"Enemy {target_id} is not attack-able. Resorting to basic attack."
            )
            skip_direction = True
        else:
            logger.debug(
                f"Attacking a specific target with id {target_id}, "
                + f"direction hint is {direction_hint}"
            )
        if not memory.main.turn_ready():
            logger.warning("Bad practice - should not attack when turn is not ready.")
            while not memory.main.turn_ready():
                if memory.main.game_over() or not memory.main.battle_complete():
                    logger.warning("Battle has ended. Returning.")
                    return
        attack_indices = [0, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216]
        self.update_battle_menu()
        attack_menu_id = [x for x in attack_indices if x in self.battle_menu][
            0
        ]
        self.navigate_to_battle_menu(attack_menu_id)
        while memory.main.main_battle_menu():
            if not memory.main.battle_active():
                logger.warning("Battle is complete! Possibly something is wrong.")
                return
            logger.debug("Battle menu is up.")
            xbox.menu_b()
        if target_id is not None and not skip_direction:
            logger.debug(f"Targetting ID {target_id}")
            self._target_specific_id(target_id, direction_hint)

        enc_id = memory.main.get_encounter_id()
        enemies = current_battle_formation()
        logger.debug(f"Battle: {enc_id} | Enemies: {enemies}")
        if len(enemies) != 0:
            try:
                if target_id is None:
                    # In multi-enemy battles, the first enemy is almost always the boss.
                    luck_value = luck_check(enemies[0])
                else:
                    luck_value = luck_check(enemies[target_id-20])
                logger.manip(f"Enemy Luck stat confirmed: {luck_value}")
            except:
                luck_value = 15
                logger.manip(f"Enemy Luck stat assumed: {luck_value}")
        else:
            luck_value = 15
        
        # This logic is only for cheese runs! See var 'god_mode'.
        if game_vars.god_mode():
            logger.warning("Attempting to force a crit, per settings")
            # Determine enemy name and luck stat
            logger.warning(f"Player luck: {self.luck()} || Enemy luck: {luck_value}")
                
            # Force forward to the next crit.
            memory.main.future_attack_will_crit(
                character=self.id,
                char_luck=self.luck(),
                enemy_luck=luck_value
            )
        self.next_crits(enemy_luck=luck_value)
        
        if record_results or short_taps:
            logger.debug("First six hits logic")
            xbox.tap_b()
            xbox.tap_b()
            xbox.tap_b()
            xbox.tap_b()
            xbox.tap_b()
            xbox.tap_b()
        else:
            logger.debug("Tap targetting logic.")
            self._tap_targeting()
    
    def quick_hit(self, target:int=20):
        logger.debug("Quick Hit function")
        if not memory.main.main_battle_menu():
            while not memory.main.main_battle_menu():
                pass

        # First, if we don't have mana, don't try quick attack.
        if self.mp() < 36:
            logger.warning("This character does not have enough MP.")
            self.attack()
            return
        
        # Next, make sure the character knows Quick Hit.
        skill_menu = memory.unlocks.get_unlocked_abilities_by_type(self.raw_id())['Skill']
        ability_position = None
        for ability in skill_menu:
            if ability['name'] == 'Quick Hit':
                ability_position = ability['position']
        if ability_position is None:
            logger.warning("This character does not know Quick Hit!")
            self.attack()
            return
        while memory.main.battle_menu_cursor() != 19:
            self.navigate_to_battle_menu(19)
        while not memory.main.other_battle_menu():
            xbox.tap_b()
        self._navigate_to_position(ability_position)
        logger.debug(f"Other battle menu: {memory.main.other_battle_menu()}")
        while memory.main.other_battle_menu():
            xbox.tap_b()  # Use the command
            
        # Target the appropriate enemy.
        direction = "l"
        retry = 0
        if memory.main.get_enemy_current_hp()[target - 20] != 0:
            # Only attack
            while memory.main.battle_target_id() != target:
                while memory.main.battle_target_id() != target:
                    if direction == "l":
                        if retry > 5:
                            logger.debug("Wrong battle line targeted.")
                            xbox.tap_right()
                            direction = "u"
                            retry = 0
                        else:
                            xbox.tap_left()
                    elif direction == "r":
                        if retry > 5:
                            retry = 0
                            logger.debug("Wrong character targeted.")
                            xbox.tap_left()
                            direction = "d"
                        else:
                            xbox.tap_right()
                    elif direction == "u":
                        if retry > 5:
                            retry = 0
                            logger.debug("Wrong character targeted.")
                            xbox.tap_down()
                            direction = "l"
                        else:
                            xbox.tap_up()
                    elif direction == "d":
                        if retry > 5:
                            retry = 0
                            logger.debug("Wrong character targeted.")
                            xbox.tap_up()
                            direction = "r"
                        else:
                            xbox.tap_down()
                    retry += 1
                memory.main.wait_frames(1)

        battle.main.tap_targeting()


    def quick_attack(self):
        self.quick_hit()


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
                f"Casting {spell_id} on a specific target with id {target_id}, "
                + "direction is {direction}"
            )
        try:
            self.navigate_to_battle_menu(21)
        except Exception:
            return
        while memory.main.main_battle_menu():
            xbox.menu_b()
        self._navigate_to_position(spell_id)
        while memory.main.other_battle_menu():
            xbox.menu_b()
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

    # spell_id should become an enum at some point
    def cast_white_magic_spell(
        self,
        spell_id: int=0,
        target_id: int = 99,
        direction: str = "right",
    ):
        self.update_battle_menu()
        if target_id is None:
            logger.debug(f"Casting white magic {spell_id}")
        else:
            logger.debug(
                f"Casting white magic {spell_id} on a specific target with id {target_id}, "
                + "direction is {direction}"
            )
        try:
            self.navigate_to_battle_menu(22)
        except Exception:
            return
        while memory.main.main_battle_menu():
            xbox.menu_b()
        self._navigate_to_position(spell_id)
        while memory.main.other_battle_menu():
            xbox.menu_b()
        if target_id != 99:
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
        
    # spell_id should become an enum at some point
    def cast_white_magic_spell_by_name(
        self,
        spell_name: str,
        target_id: int = 99,
        direction: str = "right"
    ):
        if target_id is None:
            logger.debug(f"Casting white magic {spell_name}")
        else:
            logger.debug(
                f"Casting white magic {spell_name} on a specific target with id {target_id}, "
                + f"direction is {direction}"
            )
        try:
            self.navigate_to_battle_menu(22)
        except Exception:
            return
        while memory.main.main_battle_menu():
            xbox.menu_b()
        unlocked_white = get_unlocked_abilities_by_type(self.raw_id())["White Magic"]
        spell_pos = 99  # Default to first position.
        # logger.manip(f"Default position: {spell_pos}")
        for key in unlocked_white:
            # logger.manip(key)
            if key['name'] == spell_name:
                spell_pos = key['position']
                # logger.manip(f"Found in pos {spell_pos} | {key['name']}")
        if spell_pos != 99:
            self._navigate_to_position(spell_pos)
        while memory.main.other_battle_menu():
            xbox.menu_b()
        if target_id != 99:
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

    # spell_id should become an enum at some point
    def cast_black_magic_spell_by_name(
        self,
        spell_name: str,
        target_id: int = 99,
        direction: str = "right"
    ):
        if target_id is None:
            logger.debug(f"Casting black magic {spell_name}")
        else:
            logger.debug(
                f"Casting black magic {spell_name} on a specific target with id {target_id}, "
                + f"direction is {direction}"
            )
        try:
            self.navigate_to_battle_menu(21)
        except Exception:
            return
        while memory.main.main_battle_menu():
            xbox.menu_b()
        unlocked_white = get_unlocked_abilities_by_type(self.raw_id())["Black Magic"]
        spell_pos = 99  # Default to first position.
        # logger.manip(f"Default position: {spell_pos}")
        for key in unlocked_white:
            # logger.manip(key)
            if key['name'] == spell_name:
                spell_pos = key['position']
                # logger.manip(f"Found in pos {spell_pos} | {key['name']}")
        if spell_pos != 99:
            self._navigate_to_position(spell_pos)
        while memory.main.other_battle_menu():
            xbox.menu_b()
        if target_id != 99:
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

    def provoke(self, target:int=20):
        logger.debug("Provoke function")
        if self.mp() < 4:
            logger.warning("Bad practice to provoke with no MP")
            battle.main.escape_one()
            return
        if not memory.main.main_battle_menu():
            while not memory.main.main_battle_menu():
                pass
        actor = self.raw_id()
        special_menu = memory.unlocks.get_unlocked_abilities_by_type(actor)['Special']
        # logger.warning(special_menu)
        ability_position = None
        for ability in special_menu:
            if ability['name'] == 'Provoke':
                ability_position = ability['position']
        if ability_position is None:
            logger.warning("This character does not know Provoke!")
            self.defend()
            return
        while memory.main.battle_menu_cursor() != 20:
            self.navigate_to_battle_menu(20)
        while not memory.main.other_battle_menu():
            xbox.tap_b()
        battle.main._navigate_to_position(ability_position)
        logger.debug(f"Other battle menu: {memory.main.other_battle_menu()}")
        while memory.main.other_battle_menu():
            xbox.tap_b()  # Use the command
            
        # Target the appropriate enemy.
        direction = "l"
        retry = 0
        if memory.main.get_enemy_current_hp()[target - 20] != 0:
            # Only attack
            while memory.main.battle_target_id() != target:
                while memory.main.battle_target_id() != target:
                    if direction == "l":
                        if retry > 5:
                            retry = 0
                            logger.debug("Wrong battle line targeted.")
                            xbox.tap_right()
                            direction = "u"
                            retry = 0
                        else:
                            xbox.tap_left()
                    elif direction == "r":
                        if retry > 5:
                            retry = 0
                            logger.debug("Wrong character targeted.")
                            xbox.tap_left()
                            direction = "d"
                        else:
                            xbox.tap_right()
                    elif direction == "u":
                        if retry > 5:
                            retry = 0
                            logger.debug("Wrong character targeted.")
                            xbox.tap_down()
                            direction = "l"
                        else:
                            xbox.tap_up()
                    elif direction == "d":
                        if retry > 5:
                            retry = 0
                            logger.debug("Wrong character targeted.")
                            xbox.tap_up()
                            direction = "r"
                        else:
                            xbox.tap_down()
                    retry += 1
                memory.main.wait_frames(1)

        battle.main.tap_targeting()

    def knows_flee(self):
        unlocked_specials = get_unlocked_abilities_by_type(self.raw_id())["Special"]
        for key in unlocked_specials:
            # logger.manip(key)
            if key['name'] == "Flee":
                return True
        return False

    def flee(self):
        if not self.knows_flee():
            logger.warning(f"{self.name} does not know Flee")
            self.defend()
            return False
        logger.debug(f"Fleeing with {self.name}")
        self.use_special_by_name(command_name="Flee")
        return True


    # spell_id should become an enum at some point
    def use_special_by_name(
        self,
        command_name: str,
        target_id: int = 99,
        direction: str = "right"
    ):
        if target_id is None:
            logger.debug(f"Using Special command {command_name}")
        else:
            logger.debug(
                f"Using Special command {command_name} on a specific target with id {target_id}, "
                + f"direction is {direction}"
            )
        try:
            self.navigate_to_battle_menu(20)
        except Exception:
            return
        while memory.main.main_battle_menu():
            xbox.menu_b()
        unlocked_specials = get_unlocked_abilities_by_type(self.raw_id())["Special"]
        spell_pos = 99  # Default to first position.
        # logger.manip(f"Default position: {spell_pos}")
        for key in unlocked_specials:
            # logger.manip(key)
            if key['name'] == command_name:
                spell_pos = key['position']
                # logger.manip(f"Found in pos {spell_pos} | {key['name']}")
        if spell_pos != 99:
            self._navigate_to_position(spell_pos)
        while memory.main.other_battle_menu():
            xbox.menu_b()
        if target_id != 99:
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
    
    def entrust(self,target_character:int=4):
        battle.main.entrust(target=target_character)
        
    def aim(self):
        battle.main.aim()

    def defend(self):
        logger.debug(f"Defending with {self}")
        # Update matches memory.main.turn_ready.
        # Updated 11/27/22, still to be validated.

        # Make sure we are not already in defend state_berserk
        while self.is_defending() == 1:
            logger.debug("Waiting previous defend to end.")
        memory.main.wait_frames(1)  # Buffer for safety

        result = 0
        # Now tap to defending status.
        while result == 0 and memory.main.battle_active():
            xbox.tap_y()
            result = self.is_defending()
            # logger.debug(f"Is defending: {result}")
        memory.main.wait_frames(1)  # Buffer for safety
        return True

    def navigate_to_battle_menu(self, target: int):
        self.update_battle_menu()
        """Different characters have different menu orders."""
        current_position = memory.main.battle_menu_cursor()
        while current_position == 255:
            current_position = memory.main.battle_menu_cursor()
        if not target in self.battle_menu:
            logger.debug(f"Target {target} is not in list {self.battle_menu}.")
            return False
        target_position = self.battle_menu.index(target)
        logger.debug(f"Navigating to {target} : {target_position}")
        logger.debug(self.battle_menu)
        while self.battle_menu.index(current_position) != target_position:
            logger.debug(f"{self.battle_menu.index(current_position)} | {target_position}")
            try:
                if current_position == 255:
                    logger.warning("Something is wrong with the cursor.")
                    pass
                elif self.battle_menu.index(current_position) > target_position:
                    xbox.tap_up()
                else:
                    xbox.tap_down()
                current_position = memory.main.battle_menu_cursor()
            except Exception as e:
                logger.warning(f'Navigation error: {e}')
                # xbox.tap_down()
                current_position = memory.main.battle_menu_cursor()
        return True


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
                while battle_cursor() % 2 != position % 2:
                    if battle_cursor() < position:
                        xbox.tap_right()
                    else:
                        xbox.tap_left()
                memory.main.wait_frames(1)
            while battle_cursor() != position:
                while battle_cursor() != position:
                    logger.debug(f"Battle_cursor: {battle_cursor()}")
                    if battle_cursor() > position:
                        xbox.tap_up()
                    else:
                        xbox.tap_down()
                memory.main.wait_frames(1)

    def _tap_targeting(self):
        logger.debug(
            "In Tap Targeting, Class Edition. "
            + f"Not battle menu: {not memory.main.main_battle_menu()}, "
            + f"Battle active: {memory.main.battle_active()}"
        )
        if game_vars.story_mode():
            xbox.tap_confirm()
            xbox.tap_confirm()
            xbox.tap_confirm()
            xbox.tap_confirm()
            logger.debug(
                f"Story. Not battle menu: {not memory.main.main_battle_menu()}, "
                + "Battle active: {memory.main.battle_active()}"
            )
            return
        while (not memory.main.main_battle_menu()) and memory.main.battle_active():
            xbox.tap_b()
            # if not self.is_turn():
            #    return
        logger.debug(
            f"Done. Not battle menu: {not memory.main.main_battle_menu()}, "
            + "Battle active: {memory.main.battle_active()}"
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

    def next_crits(self, enemy_luck: int = 15,length: int = 10) -> List[int]:
        # Note that this says the number of increments, so the previous roll
        # will be a hit, and this one will be the crit.
        results = []
        for i in range(length):
            if i == 0:
                pass
            elif memory.main.future_attack_will_crit(
                character=self.raw_id(),
                char_luck=self.luck(),
                enemy_luck=enemy_luck,
                attack_index=i,
                report=False
            ):
                #logger.warning(f"Attack {i} will crit")
                results.append(i)
            #else:
            #    logger.manip(f"Attack {i} will not crit, actor {self.raw_id()}")
        
        '''
        rng_array = memory.main.rng_array_from_index(
            index=self.char_rng, array_len=((length*2)+4)
        )
        #cur_rng = memory.main.rng_from_index(self.char_rng)
        #cur_rng = memory.main.roll_next_rng(cur_rng, self.char_rng)
        #cur_rng = memory.main.roll_next_rng(cur_rng, self.char_rng)
        index = 1

        # Note that the RNG to be rolled is every second RNG value, after damage rolls.
        # That's why we check only those even values starting at value 2 (index*2).
        while index*2 < len(rng_array):
            crit_roll = (rng_array[index*2] & 0x7FFFFFFF) % 101
            crit_chance = self.luck() - enemy_luck
            if crit_roll < crit_chance:
                results.append(index)
            index += 1
        '''
        logger.manip(f"Upcoming crits: {results}")
        return results

    def next_crit(self, enemy_luck) -> int:
        array = self.next_crits(enemy_luck, length=1)
        if len(array) != 0:
            return array[0]
        else:
            return 0

    def overdrive(self, *args, **kwargs):
        raise NotImplementedError()

    def overdrive_active(self):
        raise NotImplementedError()

    def overdrive_percent(self, combat=False) -> int:
        combat = memory.main.battle_active()  # Overwrites passed variable.
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
        logger.warning(self.overdrive_percent())
        if self.id < 10:
            if self.overdrive_percent() == 100:
                return True
        else:
            if self.overdrive_percent() == 20:
                return True
        return False
        # This never worked correctly.
        # return self.overdrive_percent(combat=self.in_combat()) == 100

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
    
    def is_status_silenced(self) -> bool:
        return memory.main.state_silence(self.id) != 0

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

    def has_auto_life(self) -> bool:
        return memory.main.state_auto_life(character=self.raw_id())

    def hp(self, combat=False) -> int:
        if not combat:
            return self._read_char_offset_address(PlayerMagicNumbers.CUR_HP)
        else:
            return memory.main.get_battle_hp()[self.battle_slot()]
            # return self._read_char_battle_offset_address(
            #    PlayerMagicNumbers.BATTLE_CUR_HP, self.battle_slot()
            # )

    def max_hp(self, combat=False) -> int:
        if not combat:
            return self._read_char_offset_address(PlayerMagicNumbers.MAX_HP)
        else:
            return self._read_char_battle_offset_address(
                PlayerMagicNumbers.BATTLE_MAX_HP, self.battle_slot()
            )

    def mp(self) -> int:
        # Assumes always in combat.
        return memory.main.get_battle_mp(self.id)
    
    def max_mp(self) -> int:
        return memory.main.get_max_mp(self.raw_id())

    def active(self) -> bool:
        return self in memory.main.get_active_battle_formation()

    def battle_slot(self) -> int:
        for i in range(0, 3):
            if (
                memory.main.read_val(PlayerMagicNumbers.ACTIVE_BATTLE_SLOTS + (2 * i))
                == self.id
            ):
                # logger.debug(f"Char {self.id} in slot {i}")
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
