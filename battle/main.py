import logging

from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

import battle.utils
import logs
import manip_planning.baaj_to_tros
import memory.main
import rng_track
import screen
import vars
import xbox
from battle import avina_memory
from memory.main import (
    s32,
    future_attack_will_crit,
    who_goes_first_after_current_turn,
    get_next_turn,
    get_encounter_id
)
from players import (
    Auron,
    Bahamut,
    CurrentPlayer,
    Kimahri,
    Lulu,
    Rikku,
    Tidus,
    Valefor,
    Wakka,
    Yuna,
    Yojimbo
)
from players.rikku import omnis_items
from area.dream_zan import split_timer
from json_ai_files.write_seed import write_big_text
from gamestate import game
import memory.unlocks

game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()

logger = logging.getLogger(__name__)


def _navigate_to_position(position, battle_cursor=memory.main.battle_cursor_2):
    while battle_cursor() == 255:
        pass
    if battle_cursor() != position:
        logger.debug(f"Wrong position targeted {battle_cursor() % 2}, {position % 2}")
        while battle_cursor() % 2 != position % 2:
            if battle_cursor() < position:
                xbox.tap_right()
            else:
                xbox.tap_left()
            memory.main.wait_frames(1)
        while battle_cursor() != position:
            logger.debug(f"Battle_cursor: {battle_cursor()}")
            if battle_cursor() > position:
                xbox.tap_up()
            else:
                xbox.tap_down()
            memory.main.wait_frames(1)


def tap_targeting():
    logger.debug(
        f"In Tap Targeting. Not battle menu: {not memory.main.main_battle_menu()}, "
        + f"Battle active: {memory.main.battle_active()}"
    )
    while (not memory.main.main_battle_menu()) and memory.main.battle_active():
        xbox.tap_b()
    logger.debug(
        f"Done. Not battle menu: {not memory.main.main_battle_menu()}, "
        + f"Battle active: {memory.main.battle_active()}"
    )


def yuna_cure_omnis():
    while memory.main.battle_menu_cursor() != 22:
        if not Yuna.is_turn():
            logger.debug("Attempting Cure, but it's not Yunas turn")
            return
        if memory.main.battle_menu_cursor() == 1:
            xbox.tap_up()
        else:
            xbox.tap_down()
    while not memory.main.other_battle_menu():
        xbox.tap_b()
    _navigate_to_position(0)
    while memory.main.other_battle_menu():
        xbox.tap_b()
    while memory.main.battle_target_id() <= 20:
        if memory.main.battle_target_id() < 20:
            xbox.tap_down()
        elif memory.main.battle_target_id() == 20:
            xbox.tap_left()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()


def tidus_haste(direction, character=255):
    direction = direction.lower()
    while memory.main.battle_menu_cursor() != 22:
        if not Tidus.is_turn():
            logger.debug("Attempting Haste, but it's not Tidus' turn")
            xbox.tap_up()
            xbox.tap_up()
            return
        if memory.main.battle_menu_cursor() == 1:
            xbox.tap_up()
        else:
            xbox.tap_down()
    while not memory.main.other_battle_menu():
        xbox.menu_b()
    _navigate_to_position(0)
    while memory.main.other_battle_menu():
        xbox.menu_b()
    if character != 255:
        direction = "l"
        if character < 20:
            while character != memory.main.battle_target_id():
                if direction == "l":
                    xbox.tap_left()
                    if memory.main.battle_target_id() >= 20:
                        xbox.tap_right()
                        direction = "d"
                else:
                    xbox.tap_down()
                    if memory.main.battle_target_id() >= 20:
                        xbox.tap_up()
                        direction = "l"
        else:
            while character != memory.main.battle_target_id():
                if direction == "l":
                    xbox.tap_left()
                    if memory.main.battle_target_id() < 20:
                        xbox.tap_right()
                        direction = "d"
                else:
                    xbox.tap_down()
                    if memory.main.battle_target_id() < 20:
                        xbox.tap_up()
                        direction = "l"
    elif direction == "left":
        xbox.tap_left()
    elif direction == "right":
        xbox.tap_right()
    elif direction == "up":
        xbox.tap_up()
    elif direction == "down":
        xbox.tap_down()
    tap_targeting()


def use_skill(position: int = 0, target: int = 20):
    logger.debug(f"Using skill in position: {position}")
    while memory.main.battle_menu_cursor() != 19:
        logger.debug(f"Battle menu cursor: {memory.main.battle_menu_cursor()}")
        if memory.main.battle_menu_cursor() == 255:
            pass
        elif memory.main.battle_menu_cursor() == 1:
            xbox.tap_up()
        elif memory.main.battle_menu_cursor() > 19:
            xbox.tap_up()
        else:
            xbox.tap_down()
    while not memory.main.other_battle_menu():
        xbox.tap_b()
    _navigate_to_position(position)
    while memory.main.other_battle_menu():
        xbox.tap_b()
    if target >= 20 and memory.main.get_enemy_current_hp()[target - 20] != 0:
        direction = "l"
        while memory.main.battle_target_id() != target:
            if direction == "l":
                xbox.tap_left()
                if memory.main.battle_target_id() < 20:
                    xbox.tap_right()
                    direction = "d"
            else:
                xbox.tap_down()
                if memory.main.battle_target_id() < 20:
                    xbox.tap_up()
                    direction = "l"
    xbox.tap_confirm()
    tap_targeting()


def use_special(position, target: int = 20, direction: int = "u"):
    logger.debug(f"Using skill in position: {position}")
    while memory.main.battle_menu_cursor() != 20:
        logger.debug(f"Battle menu cursor: {memory.main.battle_menu_cursor()}")
        if memory.main.battle_menu_cursor() == 255:
            pass
        elif memory.main.battle_menu_cursor() == 1:
            xbox.tap_up()
        elif memory.main.battle_menu_cursor() > 20:
            xbox.tap_up()
        else:
            xbox.tap_down()
    while not memory.main.other_battle_menu():
        xbox.tap_b()
    _navigate_to_position(position)
    while memory.main.other_battle_menu():
        xbox.tap_b()

    if memory.main.battle_target_id() != target:
        if memory.main.get_enemy_current_hp()[target - 20] >= 1:
            while memory.main.battle_target_id() != target:
                if direction == "r":
                    xbox.tap_right()
                    if memory.main.battle_target_id() < 20:
                        xbox.tap_left()
                        direction = "u"
                else:
                    xbox.tap_up()
                    if memory.main.battle_target_id() < 20:
                        xbox.tap_down()
                        direction = "r"
    xbox.tap_confirm()
    tap_targeting()


def remedy(character: int, direction: str):
    logger.debug("Remedy")
    if memory.main.get_throw_items_slot(15) < 250:
        itemnum = 15
    else:
        itemnum = -1
    if itemnum > 0:
        _use_healing_item(character, direction, itemnum)
        return 1
    else:
        logger.debug("No restorative items available")
        return 0


def revive(item_num=6, report_for_rng=False):
    logger.debug("Using Phoenix Down")
    if report_for_rng:
        logs.write_rng_track("Reviving character")
        logs.write_rng_track("Battle: " + str(get_encounter_id()))
        logs.write_rng_track("Story flag: " + str(memory.main.get_story_progress()))
    if memory.main.get_throw_items_slot(item_num) > 250:
        CurrentPlayer().attack()
        return
    while not memory.main.main_battle_menu():
        pass
    while memory.main.battle_menu_cursor() != 1:
        xbox.tap_down()
    while memory.main.main_battle_menu():
        xbox.tap_b()
    item_pos = memory.main.get_throw_items_slot(item_num)
    _navigate_to_position(item_pos)
    while memory.main.other_battle_menu():
        xbox.tap_b()
    tap_targeting()


def revive_target(item_num=6, target=0):
    direction = "l"
    logger.debug("Using Phoenix Down")
    if memory.main.get_throw_items_slot(item_num) > 250:
        flee_all()
        return
    while not memory.main.main_battle_menu():
        pass
    while memory.main.battle_menu_cursor() != 1:
        xbox.tap_down()
    while memory.main.main_battle_menu():
        xbox.tap_b()
    item_pos = memory.main.get_throw_items_slot(item_num)
    _navigate_to_position(item_pos)
    while memory.main.other_battle_menu():
        xbox.tap_b()

    # Select target - default to Tidus
    if memory.main.battle_target_id() != target:
        while memory.main.battle_target_id() != target:
            if direction == "l":
                xbox.tap_left()
                if memory.main.battle_target_id() >= 20:
                    xbox.tap_right()
                    direction = "u"
            else:
                xbox.tap_up()
                if memory.main.battle_target_id() >= 20:
                    xbox.tap_down()
                    direction = "l"
    tap_targeting()


def revive_all():
    revive(item_num=7)


def get_advances(tros=True, report=False):
    return 2
    '''
    # We would need to revisit this in the future.
    t_strike_results, yellows = rng_track.t_strike_tracking(tros=tros, report=report)
    if t_strike_results[0] >= 1 and not yellows[0]:
        advances = 0
    elif t_strike_results[1] >= 1 and not yellows[1]:
        advances = 1
    elif t_strike_results[2] >= 1 and not yellows[2]:
        advances = 2
    elif t_strike_results[1] > t_strike_results[0]:
        advances = 1
    elif t_strike_results[2] > t_strike_results[1]:
        advances = 2
    else:
        advances = 0
    game_vars.set_yellows(yellows[advances])
    logger.debug(f"Advances updated: {t_strike_results} | {yellows} | {advances}")
    return advances
    '''


@battle.utils.speedup_decorator
def piranhas_truerng():
    encounter_id = get_encounter_id()
    logger.debug("Seed: {memory.main.rng_seed()}")
    # 11 = two piranhas
    # 12 = three piranhas with one being a triple formation (takes two hits)
    # 13 = four piranhas
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if memory.main.rng_seed() == 105:
                CurrentPlayer().attack()
            elif encounter_id == 11 or (
                encounter_id == 12 and memory.main.battle_type() == 1
            ):
                CurrentPlayer().attack()
            else:
                escape_all()
    wrap_up()


def piranhas(strat):

    # 11 = two piranhas
    # 12 = three piranhas with one being a triple formation (takes two hits)
    # 13 = four piranhas
    encounter_id = get_encounter_id()

    pc_turn = 0

    while not memory.main.turn_ready():

        pass

    while memory.main.battle_active():

        if memory.main.turn_ready():

            pc_turn += 1
            if strat == 0:

                escape_one()

            else:

                if encounter_id == 12 and pc_turn == 1:

                    CurrentPlayer().attack(target_id=21, direction_hint="l")

                else:

                    CurrentPlayer().attack()

    wrap_up()


@battle.utils.speedup_decorator
def besaid():
    logger.info("Fight start: Besaid battle")
    FFXC.set_neutral()
    while not memory.main.turn_ready():
        pass
    battle_format = get_encounter_id()
    logger.debug(f"Besaid battle format number: {battle_format}")
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            enemy_hp = memory.main.get_enemy_current_hp()
            logger.debug(f"Enemy HP: {enemy_hp}")
            if Yuna.is_turn():
                buddy_swap(Wakka)
            elif get_encounter_id() == 27:
                if Lulu.is_turn():
                    CurrentPlayer().cast_black_magic_spell(1, 22, "l")
                elif Wakka.is_turn():
                    Wakka.attack(target_id=20, direction_hint="r")
                elif Tidus.is_turn():
                    Tidus.attack(target_id=21, direction_hint="r")
            else:
                if Lulu.is_turn():
                    CurrentPlayer().cast_black_magic_spell(1, 21, "l")
                else:
                    attack()
    wrap_up()


@battle.utils.speedup_decorator
def lancet_tutorial():
    logger.info("Fight start: Lancet tutorial (Kilika)")
    xbox.click_to_battle()
    lancet("none")

    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if Tidus.is_turn():
                CurrentPlayer().attack()
            elif Kimahri.is_turn():
                buddy_swap(Wakka)
                CurrentPlayer().defend()
            elif Lulu.is_turn():
                CurrentPlayer().cast_black_magic_spell(0)
            else:
                CurrentPlayer().defend()
    wrap_up()


@battle.utils.speedup_decorator
def kilika_woods(valefor_charge=True, best_charge: int = 99, next_battle=[]):
    logger.info("Fight start: Kilika battle")
    logger.debug(f"Formation: {next_battle}")
    skip_charge = False
    turn_counter = 0
    enc_id = get_encounter_id()
    logger.debug(f"Charge values: {memory.main.overdrive_state()}")
    screen.await_turn()

    FFXC.set_neutral()

    # These battles we want nothing to do with.
    if enc_id == 32:
        skip_charge = True
    # Only occurs if no best charge possible in the first three battles.
    elif best_charge == 99:
        best_charge = next_battle

    logger.info("Kilika battle")
    aeon_turn = False
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():  # AKA end of battle screen
        if (
            not valefor_charge and not skip_charge and best_charge == next_battle
        ):  # Still to charge Valefor
            if memory.main.turn_ready():
                logger.debug("Battle Turn")
                logger.debug(f"Battle Number: {enc_id}")
                logger.debug(f"Valefor charge state: {valefor_charge}")
                logger.debug(f"skip_charge state: {skip_charge}")
                turn_counter += 1
                if (
                    not (
                        0 in memory.main.get_active_battle_formation()
                        and check_character_ok(0)
                    )
                    and not screen.turn_aeon()
                    and not game_vars.rng_seed_num() == 98
                ):
                    flee_all()
                elif turn_counter > 7:
                    flee_all()
                    break
                elif screen.faint_check():
                    revive()
                elif Kimahri.is_turn() or Lulu.is_turn():
                    if 1 not in memory.main.get_active_battle_formation():
                        buddy_swap(Yuna)
                    elif 4 not in memory.main.get_active_battle_formation():
                        buddy_swap(Wakka)
                    elif 0 not in memory.main.get_active_battle_formation():
                        buddy_swap(Tidus)
                    else:
                        buddy_swap(Yuna)
                elif enc_id == 31:  # Working just fine.
                    logger.debug("Logic for battle number 31")
                    if Tidus.is_turn():
                        CurrentPlayer().attack()
                    elif Yuna.is_turn():
                        aeon_summon(0)
                        screen.await_turn()
                        if not aeon_turn:
                            aeon_turn = True
                            if memory.main.get_next_turn() < 20:
                                CurrentPlayer().shield()
                        CurrentPlayer().boost()
                        screen.await_turn()
                        CurrentPlayer().boost()
                        screen.await_turn()
                        CurrentPlayer().cast_black_magic_spell(2)
                    elif screen.turn_aeon():
                        CurrentPlayer().cast_black_magic_spell(2, direction="right")
                    else:
                        CurrentPlayer().defend()
                elif enc_id == 33:
                    logger.debug("Logic for battle number 33")
                    if Yuna.is_turn():
                        aeon_summon(0)
                        screen.await_turn()
                        if not aeon_turn:
                            aeon_turn = True
                            if memory.main.get_next_turn() < 20:
                                CurrentPlayer().shield()
                        CurrentPlayer().boost()
                        screen.await_turn()
                        CurrentPlayer().cast_black_magic_spell(1, direction="left")
                        screen.await_turn()
                        logger.manip(
                            "Valefor overdrive value: "
                            + f"{Valefor.overdrive_percent(combat=True)}"
                        )
                        if Valefor.overdrive_percent(combat=True) < 18:
                            logger.debug("Extra attack for overdrive charging.")
                            CurrentPlayer().attack()
                    elif screen.turn_aeon():
                        CurrentPlayer().cast_black_magic_spell(2)
                    else:
                        CurrentPlayer().defend()

                elif enc_id == 34:
                    logger.debug("Logic for battle number 34")
                    if Tidus.is_turn():
                        CurrentPlayer().attack()
                    elif Yuna.is_turn():
                        aeon_summon(0)
                        screen.await_turn()
                        if not aeon_turn:
                            aeon_turn = True
                            if memory.main.get_next_turn() < 20:
                                CurrentPlayer().shield()
                        CurrentPlayer().boost()
                        screen.await_turn()
                        CurrentPlayer().cast_black_magic_spell(1, direction="right")
                        screen.await_turn()
                        logger.manip(
                            "Valefor overdrive value: "
                            + f"{Valefor.overdrive_percent(combat=True)}"
                        )
                        if Valefor.overdrive_percent(combat=True) < 18:
                            logger.debug("Extra attack for overdrive charging.")
                            CurrentPlayer().attack()
                    elif screen.turn_aeon():
                        CurrentPlayer().cast_black_magic_spell(2, direction="left")
                    elif Wakka.is_turn():
                        CurrentPlayer().defend()
                    else:
                        if 1 not in memory.main.get_active_battle_formation():
                            buddy_swap(Yuna)
                        else:
                            CurrentPlayer().defend()
                elif enc_id == 35:
                    logger.debug("Logic for battle number 35")
                    if Tidus.is_turn():
                        CurrentPlayer().defend()
                    elif Yuna.is_turn():
                        aeon_summon(0)
                        screen.await_turn()
                        if not aeon_turn:
                            aeon_turn = True
                            if memory.main.get_next_turn() < 20:
                                CurrentPlayer().shield()
                        CurrentPlayer().boost()
                        screen.await_turn()
                        Valefor.unique()
                        screen.await_turn()
                        CurrentPlayer().cast_black_magic_spell(0)
                    elif screen.turn_aeon():
                        CurrentPlayer().cast_black_magic_spell(0)
                    else:
                        CurrentPlayer().defend()
                elif enc_id == 37:
                    logger.debug(
                        "Logic for battle number 37 - two bees and a plant thingey"
                    )
                    if Tidus.is_turn():
                        CurrentPlayer().attack()
                    elif Wakka.is_turn():
                        CurrentPlayer().attack(target_id=21, direction_hint="r")
                    elif Lulu.is_turn():
                        buddy_swap(Yuna)
                    elif Yuna.is_turn():
                        aeon_summon(0)
                        screen.await_turn()
                        CurrentPlayer().cast_black_magic_spell(
                            1, direction="right", target_id=22
                        )
                        screen.await_turn()
                        if not aeon_turn:
                            aeon_turn = True
                            if memory.main.get_next_turn() < 20:
                                CurrentPlayer().shield()
                        CurrentPlayer().boost()
                    elif Valefor.is_turn():
                        while memory.main.battle_active():
                            if memory.main.turn_ready():
                                CurrentPlayer().cast_black_magic_spell(0)
                    else:
                        CurrentPlayer().defend()
                else:
                    skip_charge = True
                    logger.debug(f"Not going to charge Valefor. Battle num: {enc_id}")
        else:
            if memory.main.turn_ready():
                logger.debug("Battle Turn")
                logger.debug(f"Battle Number: {enc_id}")
                logger.debug(f"Valefor charge state: {valefor_charge}")
                logger.debug(f"skip_charge state: {skip_charge}")
                turn_counter += 1
                if (
                    not (
                        0 in memory.main.get_active_battle_formation()
                        and check_character_ok(0)
                    )
                    and not screen.turn_aeon()
                ):
                    flee_all()
                elif turn_counter > 7:
                    flee_all()
                    break
                elif screen.faint_check():
                    revive()
                elif memory.main.get_speed() >= 16:
                    flee_all()
                elif Kimahri.is_turn():
                    if memory.main.get_battle_char_slot(4) >= 3:
                        buddy_swap(Wakka)
                    elif memory.main.get_battle_char_slot(0) >= 3:
                        buddy_swap(Tidus)
                    else:
                        buddy_swap(Lulu)
                elif enc_id == 31:
                    if Tidus.is_turn():
                        if turn_counter < 4:
                            CurrentPlayer().attack(target_id=20, direction_hint="l")
                        # If Wakka crit, we can use that instead. Slightly faster.
                        else:
                            flee_all()
                    elif Wakka.is_turn() and memory.main.get_enemy_current_hp()[0] != 0:
                        CurrentPlayer().attack(target_id=20, direction_hint="l")
                    elif Lulu.is_turn() and memory.main.get_enemy_current_hp()[1] != 0:
                        memory.main.print_all_statuses()
                        if not Lulu.is_status_silenced():
                            CurrentPlayer().cast_black_magic_spell(2, target_id=21)
                        else:
                            flee_all()
                    else:
                        CurrentPlayer().defend()
                elif enc_id == 32:
                    if Tidus.is_turn():
                        if turn_counter < 4:
                            CurrentPlayer().attack(target_id=20, direction_hint="r")
                        else:
                            flee_all()
                    elif Wakka.is_turn():
                        CurrentPlayer().attack(target_id=21, direction_hint="r")
                    else:
                        CurrentPlayer().defend()
                elif enc_id == 33:
                    if Tidus.is_turn():
                        if turn_counter < 4:
                            CurrentPlayer().defend()
                        else:
                            flee_all()
                    elif Wakka.is_turn():
                        CurrentPlayer().attack(target_id=21, direction_hint="r")
                    elif Lulu.is_turn() and memory.main.get_enemy_current_hp()[0] != 0:
                        memory.main.print_all_statuses()
                        if not Lulu.is_status_silenced():
                            CurrentPlayer().cast_black_magic_spell(2, target_id=20)
                        else:
                            flee_all()
                    else:
                        CurrentPlayer().defend()
                elif enc_id == 34:
                    if Tidus.is_turn():
                        if turn_counter < 4:
                            CurrentPlayer().attack()
                        else:
                            flee_all()
                    elif Wakka.is_turn():
                        CurrentPlayer().attack(target_id=22, direction_hint="r")
                    elif Lulu.is_turn() and memory.main.get_enemy_current_hp()[1] != 0:
                        memory.main.print_all_statuses()
                        if not Lulu.is_status_silenced():
                            CurrentPlayer().cast_black_magic_spell(2, target_id=21)
                        else:
                            flee_all()
                    else:
                        CurrentPlayer().defend()
                elif enc_id == 35 or enc_id == 36:
                    flee_all()
                elif enc_id == 37:
                    hp_pool = memory.main.get_enemy_current_hp()
                    if hp_pool[1] and hp_pool[2] == 0:
                        flee_all()
                    elif Wakka.is_turn() and memory.main.get_enemy_current_hp()[2] != 0:
                        CurrentPlayer().attack(target_id=22, direction_hint="l")
                    elif Lulu.is_turn() and memory.main.get_enemy_current_hp()[1] != 0:
                        memory.main.print_all_statuses()
                        if not Lulu.is_status_silenced():
                            CurrentPlayer().cast_black_magic_spell(1, target_id=21)
                        else:
                            flee_all()
                    else:
                        CurrentPlayer().defend()
    logger.debug("Kilika Woods complete")
    FFXC.set_neutral()
    wrap_up()  # Rewards screen
    hp_check = memory.main.get_hp()
    if hp_check[0] < 250 or hp_check[5] < 250 or hp_check[4] < 250:
        heal_up()
    elif 1 in memory.main.ambushes():
        heal_up()
    else:
        logger.debug("No need to heal up. Moving onward.")
    if not valefor_charge and memory.main.overdrive_state()[8] == 20:
        valefor_charge = True
    logger.debug(f"Returning Valefor Charge value: {valefor_charge}")
    return valefor_charge


@battle.utils.speedup_decorator
def luca_workers():
    logger.info("Fight start: Workers in Luca")
    xbox.click_to_battle()

    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if Kimahri.is_turn() or Tidus.is_turn():
                if screen.faint_check() >= 1:
                    revive()
                else:
                    CurrentPlayer().defend()
            if Lulu.is_turn():
                CurrentPlayer().cast_black_magic_spell(1)
        elif memory.main.diag_skip_possible() and not game_vars.story_mode():
            xbox.tap_b()  # Clicking to get through the battle faster
    wrap_up()


@battle.utils.speedup_decorator
def luca_workers_2(early_haste):
    logger.info("Fight start: Workers in Luca")
    hasted = False
    xbox.click_to_battle()
    tidus_attacks = 0
    kimahri_attacks = 0
    force_lulu = False

    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if screen.faint_check() >= 1:
                revive()
            elif early_haste >= 1:
                if Tidus.is_turn() and not hasted:
                    tidus_haste("left", character=Lulu)
                    hasted = True
                elif Lulu.is_turn():
                    CurrentPlayer().cast_black_magic_spell(1)
                else:
                    CurrentPlayer().defend()
            elif memory.main.luca_workers_battle_id() in [44, 35] and not force_lulu:
                # First, decide if we want attacks or not.
                if tidus_attacks == 2 and kimahri_attacks == 2:
                    logger.debug("========================")
                    logger.debug(f"Tidus attacks: {tidus_attacks}")
                    logger.debug(f"Kimahri attacks: {kimahri_attacks}")
                    logger.debug(
                        f"Tidus crit 1: {future_attack_will_crit(character=0, char_luck=18, enemy_luck=15, equipment_bonus=6)}"  # noqa: E501
                    )
                    logger.debug(
                        f"Tidus crit 2: {future_attack_will_crit(character=0, char_luck=18, enemy_luck=15, equipment_bonus=6, attack_index=1)}"  # noqa: E501
                    )
                    logger.debug(
                        f"Kimahri crit 1: {future_attack_will_crit(character=3, char_luck=18, enemy_luck=15, equipment_bonus=3)}"  # noqa: E501
                    )
                    logger.debug(
                        f"Kimahri crit 2: {future_attack_will_crit(character=3, char_luck=18, enemy_luck=15, equipment_bonus=3, attack_index=1)}"  # noqa: E501
                    )
                    logger.debug(f"Kimahri overdrive: {Kimahri.has_overdrive()}")
                    logger.debug("========================")
                if (
                    tidus_attacks == 2
                    and kimahri_attacks == 2
                    and not Kimahri.has_overdrive()
                    and not future_attack_will_crit(
                        character=0, char_luck=18, enemy_luck=15, equipment_bonus=6
                    )
                    and not future_attack_will_crit(
                        character=0, char_luck=18, enemy_luck=15, equipment_bonus=6, attack_index=1
                    )
                    and not future_attack_will_crit(
                        character=3, char_luck=18, enemy_luck=15, equipment_bonus=3
                    )
                    and not future_attack_will_crit(
                        character=3, char_luck=18, enemy_luck=15, equipment_bonus=3, attack_index=1
                    )
                ):
                    logger.warning("No crits coming up. Lulu only.")
                    force_lulu = True
                elif tidus_attacks != 2 or kimahri_attacks != 2:
                    pass
                else:
                    logger.warning(
                        "Crits coming up (or has overdrive). Proceed to PWN!"
                    )

                if force_lulu:
                    pass
                elif Tidus.is_turn():
                    CurrentPlayer().attack()
                    tidus_attacks += 1
                elif Kimahri.is_turn():
                    if (
                        kimahri_attacks % 2 == 1
                        and Kimahri.has_overdrive()
                        and memory.main.get_enemy_current_hp()[0] > 80
                    ):
                        logger.debug(f"=== Kimahri attacks: {kimahri_attacks}")
                        logger.debug(f"=== Kimahri has OD: {Kimahri.has_overdrive()}")
                        logger.debug(
                            f"=== Target HP: {memory.main.get_enemy_current_hp()[0]}"
                        )
                        logger.debug(
                            f"=== Target Next Crit: {memory.main.next_crit(character=3, char_luck=18, enemy_luck=15)}"  # noqa: E501
                        )
                        if (
                            memory.main.next_crit(
                                character=3, char_luck=18, enemy_luck=15
                            )
                            == 0
                        ):
                            CurrentPlayer().attack()
                        else:
                            Kimahri.overdrive(1)
                    else:
                        CurrentPlayer().attack()
                    kimahri_attacks += 1
                elif Lulu.is_turn():
                    if tidus_attacks + kimahri_attacks in [3, 7, 8]:
                        xbox.weap_swap(0)
                    else:
                        CurrentPlayer().cast_black_magic_spell(spell_id=1, target_id=21)
            else:
                if Lulu.is_turn():
                    CurrentPlayer().cast_black_magic_spell(1)
                else:
                    CurrentPlayer().defend()
        elif memory.main.diag_skip_possible() and not game_vars.story_mode():
            xbox.tap_b()  # Clicking to get through the battle faster
    wrap_up()


@battle.utils.speedup_decorator
def after_blitz_1(early_haste):
    logger.info("Fight start: After Blitzball (the fisheys)")
    logger.debug(f"Early haste: {early_haste}")
    if early_haste != -1:
        screen.await_turn()

        # Tidus haste self
        tidus_haste("none")
    wakka_turns = 0
    tidus_cheers = 0
    if game_vars.story_mode():
        tidus_cheers = 5

    while memory.main.battle_active():
        if memory.main.turn_ready():
            logger.debug(f"Enemy HP: {memory.main.get_enemy_current_hp()}")
            if Tidus.is_turn():
                if tidus_cheers != 0:
                    cheer()
                    tidus_cheers -= 1
                else:
                    CurrentPlayer().attack()
            else:
                wakka_turns += 1
                hp_values = memory.main.get_battle_hp()
                if wakka_turns < 3:
                    Wakka.attack(target_id=22, direction_hint="l")
                elif hp_values[1] < 200:  # Tidus HP
                    if memory.main.get_item_slot(0) != 255:
                        use_potion_character(0, "u")
                    else:
                        Wakka.defend()
                elif hp_values[0] < 100:  # Wakka HP
                    if memory.main.get_item_slot(0) != 255:
                        use_potion_character(4, "u")
                    else:
                        Wakka.defend()
                else:
                    Wakka.defend()


@battle.utils.speedup_decorator
def after_blitz_3(early_haste):
    logger.info("Ready to take on Garuda (A)")
    logger.debug(f"Early haste: {early_haste}")
    # Wakka dark attack, or Auron power break
    wakka_dark = False
    if game_vars.story_mode() or game_vars.platinum():
        wakka_dark = True
    if memory.main.get_item_slot(item_num=0) == 255:
        wakka_dark = True
    screen.await_turn()
    tidus_turn = 0
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():
        if memory.main.turn_ready():
            hp_values = memory.main.get_battle_hp()
            if Auron.is_turn():
                logger.debug("Auron Turn")
                CurrentPlayer().attack()
            elif Tidus.is_turn():
                logger.debug(f"Tidus Turn: {tidus_turn}")
                if tidus_turn == 0:
                    tidus_haste("d", character=Auron)
                    tidus_turn += 1
                elif tidus_turn == 1:
                    CurrentPlayer().attack()
                    tidus_turn += 1
                elif hp_values[0] < 202:
                    use_potion_character(2, "u")
                else:
                    CurrentPlayer().defend()
            elif Wakka.is_turn():
                logger.debug("Wakka Turn")
                if (
                    hp_values[0] < 302
                    and hp_values[0] != 0
                    and (
                        memory.main.get_next_turn() != 2
                        or memory.main.get_enemy_current_hp()[0] > 268
                    )
                    and memory.main.get_item_slot(item_num=0) != 255
                ):
                    use_potion_character(2, "u")
                elif (
                    hp_values[1] < 312 and hp_values[1] != 0 and 
                    tidus_turn < 2 and
                    memory.main.get_item_slot(item_num=0) != 255
                ):
                    use_potion_character(0, "u")
                elif wakka_dark:
                    use_skill(0)
                    wakka_dark=False
                else:
                    CurrentPlayer().defend()
    logger.info("Battle complete (Garuda) A")
    memory.main.wait_frames(3)
    # split_timer()
    # Get to control
    if game_vars.story_mode():
        logger.debug("Ending battles after Blitz (early haste variant)")
        while not memory.main.battle_wrap_up_active():
            if memory.main.user_control():
                return
        logger.debug("Mark 1")
        FFXC.set_confirm()
        while memory.main.battle_wrap_up_active():
            if memory.main.user_control():
                FFXC.set_neutral()
                return
        logger.debug("Mark 2")
        FFXC.release_confirm()
        memory.main.wait_seconds(90)
        logger.debug("Mark 3")
        xbox.await_save(index=1)
        logger.debug("Mark 4")
    else:
        while not memory.main.user_control():
            if memory.main.battle_wrap_up_active():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                memory.main.wait_frames(15)
                xbox.skip_scene()
                memory.main.wait_frames(15)
                xbox.await_save(index=1)
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_b()
    if game_vars.god_mode():
        rng_track.force_preempt()


@battle.utils.speedup_decorator
def after_blitz_3_late_haste(early_haste):
    logger.info("Ready to take on Garuda (B)")
    logger.debug(f"Early haste: {early_haste}")
    # Wakka dark attack, or Auron power break
    wakka_dark = False
    if game_vars.story_mode():
        wakka_dark = True
    screen.await_turn()
    if Auron.is_turn():
        logger.debug("Auron's turn")
        use_skill(0)
    elif Tidus.is_turn():
        logger.debug("Tidus' turn")
        if early_haste != -1:
            tidus_haste("up")
        else:
            CurrentPlayer().attack()
    else:
        logger.debug("Wakkas turn")
        use_skill(0)
    screen.await_turn()
    if Auron.is_turn():
        use_skill(0)
    elif Tidus.is_turn():
        if early_haste != -1:
            tidus_haste("up")
        else:
            CurrentPlayer().attack()
    else:
        use_skill(0)
    screen.await_turn()
    if Auron.is_turn():
        use_skill(0)
    else:
        use_skill(0)

    while not memory.main.turn_ready():
        pass
    while not memory.main.battle_wrap_up_active():
        if memory.main.turn_ready():
            if screen.faint_check() > 0:
                revive()
            elif wakka_dark and Wakka.is_turn():
                use_skill(0)
                wakka_dark=False
            else:
                CurrentPlayer().attack()
    FFXC.set_confirm()
    memory.main.wait_frames(30 * 4)
    FFXC.release_confirm()
    logger.info("Battle complete (Garuda) B")
    # Get to control
    if game_vars.story_mode():
        logger.debug("Ending battles after Blitz (late haste variant)")
        while not memory.main.battle_wrap_up_active():
            if memory.main.user_control():
                return
        logger.debug("Mark 1")
        FFXC.set_confirm()
        while memory.main.battle_wrap_up_active():
            if memory.main.user_control():
                FFXC.set_neutral()
                return
        logger.debug("Mark 2")
        FFXC.release_confirm()
        memory.main.wait_seconds(90)
        logger.debug("Mark 3")
        xbox.await_save(index=1)
        logger.debug("Mark 4")
    else:
        while not memory.main.user_control():
            if memory.main.cutscene_skip_possible():
                while not memory.main.diag_progress_flag() == 1:
                    if memory.main.cutscene_skip_possible():
                        xbox.skip_scene()
                if game_vars.csr():
                    memory.main.wait_frames(60)
                else:
                    xbox.await_save(index=1)
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_b()
            elif memory.main.menu_open():
                xbox.tap_b()
    if game_vars.god_mode():
        rng_track.force_preempt()


@battle.utils.speedup_decorator
def miihen_road(self_destruct=False):
    while not memory.main.turn_ready():
        if memory.main.game_over():
            return False
    enc_id = get_encounter_id()
    logger.info(f"Fight start: Mi'ihen Road ({enc_id})")
    logger.warning(f"Mi'ihen battle. Self-destruct learned: {game_vars.self_destruct_get()}")
    if game_vars.story_mode() and not game_vars.self_destruct_get():
        # Need to track all encounters where we can learn self destruct.
        if enc_id in [51,87]:
            lancet_swap()
            if memory.main.game_over():
                return False
            game_vars.self_destruct_learned()  # Can't forget this.
        elif enc_id in [64,65,66,84] and memory.main.battle_type() != 2:
            lancet_swap(target_id=21)
            if memory.main.game_over():
                return False
            game_vars.self_destruct_learned()  # Can't forget this.

        # Once done learning, we should just leave.
        flee_all()
        if memory.main.game_over():
            return False
        memory.main.update_formation(Tidus, Wakka, Auron)
    else:
        flee_all()
        if memory.main.game_over():
            return False
    FFXC.set_movement(0, 1)
    wrap_up()
    return True


def mrr_target():
    enc_id = get_encounter_id()
    if enc_id == 96:
        CurrentPlayer().attack(target_id=22, direction_hint="r")
    elif enc_id == 97:
        CurrentPlayer().attack(target_id=20, direction_hint="r")
    elif enc_id == 98:
        lancet_target(target=21, direction="d")
    elif enc_id == 101:
        lancet_target(target=21, direction="l")
    elif enc_id in [100, 110]:
        CurrentPlayer().attack(target_id=22, direction_hint="l")
    elif enc_id in [102, 112, 113]:
        CurrentPlayer().attack(target_id=20, direction_hint="l")
    elif enc_id in [109, 111]:
        lancet_target(target=20, direction="l")
    else:
        CurrentPlayer().defend()
    return Kimahri.next_crit(15)


@battle.utils.speedup_decorator
def mrr_battle(status):
    # Yuna complete, Kimahri complete, Valefor overdrive,
    # Battle counter, Yuna level up complete, Yuna grid, phase
    logger.info("------------------------------")
    encounter_id = get_encounter_id()
    logger.info(f"Fight start: MRR {encounter_id}")
    # next_crit_kim = memory.next_crit(character=Kimahri, char_luck=18, enemy_luck=15)

    if encounter_id == 102:
        logger.info("Garuda battle, we want nothing to do with this.")
    elif status[5] == 0:
        logger.info(
            "If funguar present or more than three flees already, Valefor overdrive."
        )
    elif status[5] == 1:
        logger.info("Now we're going to try to charge Valefor's overdrive again.")
    elif status[5] == 2:
        logger.info("Yuna still needs levels.")
    else:
        logger.info("Nothing else, going to flee.")
    screen.await_turn()

    aeon_turn = 0
    valefor_charge_complete = False

    # If we're ambushed and take too much damage, this will trigger first.
    hp_array = memory.main.get_battle_hp()
    hp_total = hp_array[0] + hp_array[1] + hp_array[2]
    # Final charging for Yuna is a lower overall party HP
    if hp_total < 1800 and status[5] != 2:
        logger.info("--- We got ambushed. Not going to attempt to recover.")
        flee_all()
    elif screen.faint_check() >= 1:
        logger.info("--- Character is dead from the start of battle -> Escaping")
        flee_all()
    elif check_petrify():
        logger.warning("Character petrified. Unhandled case -> Escaping")
        flee_all()
    elif encounter_id == 102:  # Garuda, flee no matter what.
        flee_all()
    elif status[5] == 0:  # Phase zero - use Valefor overdrive to overkill for levels
        if status[3] < 3:
            # Encounter id (zero-index)
            if (
                encounter_id == 100 or encounter_id == 101
            ):  # The two battles with Funguar
                while memory.main.battle_active():  # end of battle screen
                    if memory.main.turn_ready():
                        if check_petrify():
                            logger.warning(
                                "Character petrified. Unhandled case -> Escaping"
                            )
                            flee_all()
                        elif Tidus.is_turn():
                            buddy_swap(Kimahri)
                        elif Kimahri.is_turn():
                            CurrentPlayer().defend()
                        elif Wakka.is_turn():
                            CurrentPlayer().defend()
                        else:
                            buddy_swap(Yuna)
                            aeon_summon(0)
                            screen.await_turn()
                            Valefor.overdrive(overdrive_num=0)
                            status[2] = 1
                            status[5] = 1
            else:
                flee_all()
        else:  # Starting with fourth battle, overdrive on any battle that isn't Garuda.
            while memory.main.battle_active():  # end of battle screen
                if memory.main.turn_ready():
                    if check_petrify():
                        logger.warning(
                            "Character petrified. Unhandled case -> Escaping"
                        )
                        flee_all()
                    elif Tidus.is_turn():
                        buddy_swap(Kimahri)
                    elif Kimahri.is_turn():
                        # if (
                        #     next_crit_kim > 9 - status[3]
                        #     and next_crit_kim < 23 - (status[3] * 2)
                        # ):
                        #     next_crit_kim = mrr_target()
                        # else:
                        CurrentPlayer().defend()
                    elif Wakka.is_turn():
                        CurrentPlayer().defend()
                    else:
                        buddy_swap(Yuna)
                        aeon_summon(0)
                        screen.await_turn()
                        Valefor.overdrive(overdrive_num=0)
                        status[2] = 1
                        status[5] = 1
    elif status[5] == 1:  # Next need to recharge Valefor
        valefor_charge_complete = True
        if memory.main.battle_type() == 1:
            for _ in range(3):
                screen.await_turn()
                CurrentPlayer().defend()
        if encounter_id == 96:  # Gandarewa, Red Element, Raptor (camera front)
            wakka_turns = 0
            while memory.main.battle_active():  # end of battle screen
                if memory.main.turn_ready():
                    if check_petrify():
                        logger.info("Someone is pretrified. Escaping battle.")
                        flee_all()
                        valefor_charge_complete = False
                    else:
                        logger.debug("No petrify issues.")
                        if Tidus.is_turn():
                            buddy_swap(Kimahri)
                            mrr_target()
                        elif Wakka.is_turn():
                            wakka_turns += 1
                            if wakka_turns == 1:
                                CurrentPlayer().attack(target_id=21, direction_hint="l")
                            else:
                                buddy_swap(Yuna)
                                aeon_summon(0)
                        elif Auron.is_turn():
                            CurrentPlayer().attack(target_id=22, direction_hint="r")
                        elif Kimahri.is_turn():
                            buddy_swap(Yuna)
                            aeon_summon(0)
                        elif screen.turn_aeon():
                            if aeon_turn == 0 and memory.main.get_next_turn() < 19:
                                CurrentPlayer().boost()
                                aeon_turn = 1
                            elif aeon_turn < 2:
                                CurrentPlayer().boost()
                                screen.await_turn()
                                CurrentPlayer().attack()
                                aeon_turn = 2
                            else:
                                CurrentPlayer().cast_black_magic_spell(3)
        elif encounter_id == 97:  # Lamashtu, Gandarewa, Red Element (camera front)
            while memory.main.battle_active():  # end of battle screen
                if memory.main.turn_ready():
                    if check_petrify():
                        logger.warning(
                            "Character petrified. Unhandled case -> Escaping"
                        )
                        flee_all()
                    elif Tidus.is_turn():
                        buddy_swap(Kimahri)
                        mrr_target()
                    elif Wakka.is_turn():
                        CurrentPlayer().defend()
                    elif Auron.is_turn():
                        CurrentPlayer().attack()
                    elif Kimahri.is_turn():
                        buddy_swap(Yuna)
                        aeon_summon(0)
                    elif screen.turn_aeon():
                        if aeon_turn == 0 and memory.main.get_next_turn() < 19:
                            screen.await_turn()
                            CurrentPlayer().boost()
                            aeon_turn = 1
                        elif aeon_turn < 2:
                            CurrentPlayer().cast_black_magic_spell(2)
                            screen.await_turn()
                            CurrentPlayer().boost()
                            aeon_turn = 2
                        else:
                            CurrentPlayer().cast_black_magic_spell(3)
        elif encounter_id == 98:  # Raptor, Red Element, Gandarewa (camera side)
            while memory.main.battle_active():  # end of battle screen
                if memory.main.turn_ready():
                    if check_petrify():
                        logger.info("Someone is pretrified. Escaping battle.")
                        flee_all()
                        valefor_charge_complete = False
                    else:
                        logger.debug("No petrify issues.")
                        if Tidus.is_turn():
                            buddy_swap(Kimahri)
                        elif Kimahri.is_turn():
                            mrr_target()
                        elif Wakka.is_turn():
                            CurrentPlayer().attack()
                        elif Auron.is_turn():
                            buddy_swap(Yuna)
                            aeon_summon(0)
                        elif screen.turn_aeon():
                            if aeon_turn == 0 and memory.main.get_next_turn() < 19:
                                CurrentPlayer().boost()
                                aeon_turn = 1
                            elif aeon_turn < 2:
                                CurrentPlayer().cast_black_magic_spell(
                                    2, direction="right"
                                )
                                screen.await_turn()
                                CurrentPlayer().boost()
                                aeon_turn = 2
                            else:
                                CurrentPlayer().cast_black_magic_spell(
                                    3, direction="right"
                                )
        # battle 99 is never used.
        elif encounter_id == 100:  # Raptor, Funguar, Red Element (camera front)
            while memory.main.battle_active():  # end of battle screen
                if memory.main.turn_ready():
                    if check_petrify():
                        logger.info("Someone is pretrified. Escaping battle.")
                        flee_all()
                        valefor_charge_complete = False
                    else:
                        logger.debug("No petrify issues.")
                        if Tidus.is_turn():
                            buddy_swap(Kimahri)
                            # if (
                            #     next_crit_kim > 9 - status[3]
                            #     and next_crit_kim < 23 - (status[3] * 2)
                            # ):
                            #     next_crit_kim = mrr_target()
                            # else:
                            CurrentPlayer().defend()
                        elif Wakka.is_turn():
                            CurrentPlayer().attack()
                        elif memory.main.get_enemy_current_hp()[0] != 0:
                            buddy_swap(Tidus)
                            flee_all()
                            valefor_charge_complete = False
                        elif Auron.is_turn():
                            buddy_swap(Yuna)
                            aeon_summon(0)
                        elif screen.turn_aeon():
                            if aeon_turn == 0 and memory.main.get_next_turn() < 19:
                                screen.await_turn()
                                CurrentPlayer().boost()
                                aeon_turn = 1
                            elif aeon_turn < 2:
                                CurrentPlayer().cast_black_magic_spell(0)
                                screen.await_turn()
                                CurrentPlayer().boost()
                                aeon_turn = 2
                            else:
                                CurrentPlayer().cast_black_magic_spell(3)
        # Funguar, Red Element, Gandarewa (camera reverse angle)
        elif encounter_id == 101:
            while memory.main.battle_active():  # end of battle screen
                if memory.main.turn_ready():
                    if check_petrify():
                        logger.warning(
                            "Character petrified. Unhandled case -> Escaping"
                        )
                        flee_all()
                    elif Tidus.is_turn():
                        buddy_swap(Kimahri)
                        mrr_target()
                    elif Wakka.is_turn():
                        CurrentPlayer().attack(target_id=22, direction_hint="l")
                    elif memory.main.get_enemy_current_hp()[2] != 0:
                        buddy_swap(Tidus)
                        flee_all()
                        valefor_charge_complete = False
                    elif Auron.is_turn():
                        buddy_swap(Yuna)
                        aeon_summon(0)
                    elif screen.turn_aeon():
                        if aeon_turn == 0 and memory.main.get_next_turn() < 19:
                            CurrentPlayer().boost()
                            aeon_turn = 1
                        elif aeon_turn < 2:
                            CurrentPlayer().cast_black_magic_spell(0)
                            screen.await_turn()
                            CurrentPlayer().boost()
                            aeon_turn = 2
                        else:
                            CurrentPlayer().cast_black_magic_spell(3)
        if valefor_charge_complete:
            status[5] = 2  # Phase 2, final phase to level up Kimahri and Yuna
            status[2] = 2  # Valefor is charged flag.
    elif status[5] == 2:  # Last phase is to level Yuna and Kimahri
        # Both Yuna and Kimahri have levels, good to go.
        if status[0] == 1 and status[1] == 1:
            status[5] = 3
            while memory.main.battle_active():  # end of battle screen
                if memory.main.turn_ready():
                    flee_all()
        else:
            # Wakka attack Raptors and Gandarewas for Yuna AP.
            yuna_turn_count = 0
            kim_turn_count = 0
            while memory.main.battle_active():  # end of battle screen
                if memory.main.turn_ready():
                    if check_petrify():
                        logger.warning(
                            "Character petrified. Unhandled case -> Escaping"
                        )
                        flee_all()
                    elif Tidus.is_turn():
                        Tidus.flee()
                    elif screen.faint_check() >= 1:
                        buddy_swap(Tidus)
                        flee_all()
                    elif Kimahri.is_turn():
                        if memory.main.get_kimahri_slvl() >= 8 and yuna_turn_count:
                            # if (
                            #     next_crit_kim > 9 - status[3]
                            #     and next_crit_kim < 23 - (status[3] * 2)
                            # ):
                            #     next_crit_kim = mrr_target()
                            # else:
                            flee_all()
                        else:
                            CurrentPlayer().defend()
                    elif Yuna.is_turn():
                        yuna_turn_count += 1
                        if yuna_turn_count == 1:
                            CurrentPlayer().defend()
                        else:
                            flee_all()
                    elif Wakka.is_turn():
                        if encounter_id in [96, 97, 101]:
                            if encounter_id == 101:
                                CurrentPlayer().attack(target_id=22, direction_hint="l")
                            else:
                                CurrentPlayer().attack(target_id=21, direction_hint="l")
                        elif encounter_id == 98 or encounter_id == 100:
                            CurrentPlayer().attack()
                        else:
                            flee_all()
                    else:  # Should not occur, but you never know.
                        buddy_swap(Tidus)
    else:  # Everything is done.
        flee_all()

    logger.debug(f"Wakka late menu: {game_vars.wakka_late_menu()}")
    # OK the battle should be complete now. Let's do some wrap-up stuff.
    wrap_up()

    if status[5] == 3:
        memory.main.update_formation(Tidus, Wakka, Auron, full_menu_close=False)
    elif status[5] == 2:  # Still levelling Yuna or Kimahri
        memory.main.update_formation(Yuna, Wakka, Auron, full_menu_close=False)
        logger.debug("Yuna in front party, trying to get some more experience.")
    else:
        memory.main.update_formation(Tidus, Wakka, Auron, full_menu_close=False)

    # Now checking health values
    if status[5] == 2:
        heal_up(3, full_menu_close=False)
    elif (
        Tidus.in_danger(520)
        or Yuna.in_danger(475)
        or Auron.in_danger(1030)
        or Kimahri.in_danger(644)
        or Wakka.in_danger(818)
        or Lulu.in_danger(380)
    ):
        heal_up(full_menu_close=False)
    # donezo. Back to the main path.
    logger.debug("Clean-up is now complete.")
    return status


def _mrr_manip_kimahri_crit():
    next_crit_kim = Kimahri.next_crit(15)
    logger.debug(f"Manip - Encounter id: {get_encounter_id()}")
    logger.debug(f"Next Kimahri Crit vs Gui: {next_crit_kim}")
    return next_crit_kim


@battle.utils.speedup_decorator
def mrr_manip(kim_max_advance: int = 6):
    screen.await_turn()
    attempt_manip = False
    logger.info("MRR_manip function")

    while memory.main.battle_active():
        if memory.main.turn_ready():
            next_chance = memory.main.next_crit(
                character=3, char_luck=18, enemy_luck=15
            )
            if next_chance >= 3 and next_chance <= 12:
                if 255 not in memory.main.get_active_battle_formation():
                    escape_one(exclude=3)
                elif not Kimahri.active() and 3 in memory.main.get_battle_formation():
                    buddy_swap(Kimahri)
                elif Kimahri.is_turn():
                    if 255 in memory.main.get_active_battle_formation():
                        lancet("none")
                        attempt_manip = True
                    else:
                        CurrentPlayer().defend()
                else:
                    CurrentPlayer().defend()
            elif next_chance == 2:
                if not Kimahri.active():
                    buddy_swap(Kimahri)
                elif Kimahri.is_turn():
                    escape_one()
                else:
                    escape_one()
            else:
                flee_all(exclude=3)
    wrap_up()
    # Now checking health values
    hp_check = memory.main.get_hp()
    logger.debug(f"HP values: {hp_check}")
    if hp_check != [520, 475, 1030, 644, 818, 380]:
        heal_up(full_menu_close=False)
    memory.main.update_formation(Tidus, Wakka, Auron)
    _mrr_manip_kimahri_crit()
    return attempt_manip


@battle.utils.speedup_decorator
def mrr_manip_old(kim_max_advance: int = 6):
    screen.await_turn()
    next_crit_kim = Kimahri.next_crit(15)
    logger.debug(f"Next Kimahri crit: {next_crit_kim}")
    attempt_manip = False
    if next_crit_kim >= 3:
        kim_turn = True
    else:
        kim_turn = False
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():
        if memory.main.turn_ready():
            next_crit_kim = _mrr_manip_kimahri_crit()
            if next_crit_kim > kim_max_advance:
                flee_all()
            elif kim_turn:
                attempt_manip = True
                if not Kimahri.active():
                    buddy_swap(Kimahri)
                elif Kimahri.is_turn():
                    next_crit_kim = mrr_target()
                    kim_turn = False
                else:
                    CurrentPlayer().defend()
            else:
                flee_all()
    wrap_up()
    # Now checking health values
    hp_check = memory.main.get_hp()
    logger.debug(f"HP values: {hp_check}")
    if hp_check != [520, 475, 1030, 644, 818, 380]:
        heal_up(full_menu_close=False)
    memory.main.update_formation(Tidus, Wakka, Auron)
    _mrr_manip_kimahri_crit()
    return attempt_manip


@battle.utils.speedup_decorator
def djose(battle_count=0):
    # AI logic - it remembers!!! Skynet and all that stuff.
    heal_array = []
    try:
        records = avina_memory.retrieve_memory()
        logger.debug(records.keys())
        seed_str = str(memory.main.rng_seed())
        logger.manip(f"Seed: {seed_str}")
        if seed_str in records.keys():
            if "djose_heals" in records[seed_str].keys():
                for i in range(30):
                    if i in records[seed_str]["djose_heals"]:
                        if records[seed_str]["djose_heals"][i] == "True":
                            heal_array.append(i)
            else:
                logger.info("I have no memory of this seed. (A)")
        else:
            logger.info("I have no memory of this seed. (B)")
    except Exception:
        logger.info("I have no memory of this seed. (C)")
    encounter_id = get_encounter_id()
    logger.info(f"Fight start: Djose road {encounter_id}")
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if Kimahri.is_overdrive_learned("stone breath"):  # Stone Breath already learned
                logger.debug("Djose: Stone breath already learned.")
                flee_all()
            else:  # Stone breath not yet learned
                if encounter_id in [128,134,136]:
                    logger.info("Djose: Learning Stone Breath.")
                    lancet_swap()
                elif encounter_id == 127:
                    logger.info("Djose: Learning Stone Breath")
                    # One basilisk with two wasps
                    lancet_swap(target_id=21)
                    break
                else:
                    logger.info("Djose: Cannot learn Stone Breath here.")
                    flee_all()
        elif memory.main.game_over():
            logger.warning("Djose battle, game over identified!!! (A)")
            seed_str = str(memory.main.rng_seed())
            avina_memory.add_battle_to_memory(
                seed=seed_str, area="djose_heals", battle_num=battle_count - 1
            )
            return False
    if memory.main.game_over():
        logger.warning("Djose battle, game over identified!!!(B)")
        seed_str = str(memory.main.rng_seed())
        avina_memory.add_battle_to_memory(
            seed=seed_str, area="djose_heals", battle_num=battle_count - 1
        )
        return False
    wrap_up()
    party_hp = memory.main.get_hp()
    logger.debug(f"Party hp: {party_hp}")
    if game_vars.ml_heals():
        logger.warning("aVIna deciding if we need to heal.")
        if battle_count in heal_array:
            heal_up()
    elif party_hp[0] < 300 or party_hp[4] < 300:
        logger.debug("Djose: recovering HP")
        heal_up(3)
    else:
        logger.debug("Djose: No need to heal.")
    memory.main.update_formation(Tidus, Wakka, Auron)


@battle.utils.speedup_decorator
def mix_tutorial():
    if game_vars.story_mode():
        memory.main.wait_seconds(5)
        xbox.tap_confirm()  # Ooh a treasure chest!
        memory.main.wait_seconds(2)
        xbox.tap_confirm()  # I wonder what's inside!
        memory.main.wait_seconds(5)
        xbox.tap_confirm()  # Tutorial 1
        memory.main.wait_seconds(2)
        xbox.tap_confirm()  # I Tutorial 2
    xbox.click_to_battle()
    write_big_text(f"Spheres: {memory.main.get_power()}/34")
    steal()
    logger.info("Mark 1")
    #if game_vars.story_mode():
    #    memory.main.wait_seconds(20)
    #xbox.click_to_battle()
    rikku_full_od("tutorial")
    logger.info("Mark 2")
    write_big_text(f"Escaping")
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Tidus.is_turn():
                flee_all()
            else:
                CurrentPlayer().defend()
    memory.main.click_to_control()
    write_big_text(f"")
    if game_vars.god_mode():
        rng_track.force_preempt()


@battle.utils.speedup_decorator
def thunder_plains(section, battle_count: int = 0):
    # AI logic - it remembers!!! Skynet and all that stuff.
    heal_array = []
    try:
        records = avina_memory.retrieve_memory()
        logger.debug(records.keys())
        seed_str = str(memory.main.rng_seed())
        logger.manip(f"Seed: {seed_str}")
        if seed_str in records.keys():
            if "t_plains_heals" in records[seed_str].keys():
                for i in range(30):
                    if i in records[seed_str]["t_plains_heals"]:
                        if records[seed_str]["t_plains_heals"][i] == "True":
                            heal_array.append(i)
            else:
                logger.info("I have no memory of this seed. (A)")
        else:
            logger.info("I have no memory of this seed. (B)")
    except Exception:
        logger.info("I have no memory of this seed. (C)")

    enc_id = get_encounter_id()
    grenade_slot = memory.main.get_item_slot(35)
    logger.debug(f"Grenade Slot {grenade_slot}")
    grenade_count = memory.main.get_item_count_slot(grenade_slot)
    logger.debug(f"Grenade count: {grenade_count}")
    speed_count = memory.main.get_speed()
    logger.debug(f"Speed sphere count: {speed_count}")
    use_grenades = grenade_count > 3 and speed_count < 14
    logger.debug(f"Use Grenades decision: {use_grenades}")
    use_grenade_slot = memory.main.get_use_items_slot(35)
    lunar_slot = game_vars.get_blitz_win() or memory.main.get_item_slot(56) != 255
    light_slot = memory.main.get_item_slot(57) != 255
    petrify_slot = memory.main.get_item_slot(49) != 255

    tidus_turns = 0
    while not memory.main.turn_ready():
        if memory.main.game_over():
            return False
        if memory.main.battle_wrap_up_active():
            wrap_up()
            return True

    # Petrify check is not working. Requires review.
    if check_petrify():
        logger.warning("Character petrified. Unhandled case -> Escaping")
        flee_all()
    elif memory.main.battle_type() == 2:
        flee_all()
    elif enc_id in [152, 155, 162]:  # Any battle with Larvae
        if lunar_slot:
            # No longer need Lunar Curtain for Evrae fight, Blitz win logic.
            flee_all()
        else:  # Blitz loss strat
            logger.info(f"Battle with Larvae. Encounter id: {enc_id}")
            while memory.main.battle_active():
                if memory.main.turn_ready():
                    if not lunar_slot and memory.main.turn_ready():
                        if Tidus.is_turn():
                            if tidus_turns == 0:
                                buddy_swap(Rikku)
                            else:
                                flee_all()
                            tidus_turns += 1
                        elif Rikku.is_turn():
                            steal()
                            lunar_slot = (
                                game_vars.get_blitz_win()
                                or memory.main.get_item_slot(56) != 255
                            )
                        else:
                            buddy_swap(Tidus)
                    else:
                        flee_all()
    elif enc_id == 160:
        logger.info(f"Battle with Iron Giant. Encounter id: {enc_id}")
        while memory.main.battle_active():
            screen.await_turn()
            if light_slot:
                flee_all()
            else:
                buddy_swap(Rikku)
            while memory.main.battle_active():
                if Rikku.is_turn():
                    if not light_slot:
                        steal()
                        light_slot = memory.main.get_item_slot(57) != 255
                    elif not Rikku.has_overdrive():
                        CurrentPlayer().attack()
                    else:
                        flee_all()
                else:
                    if not Rikku.has_overdrive() and not Rikku.is_status_ok():
                        escape_one()
                    else:
                        flee_all()
    elif enc_id == 161:
        logger.info(f"Battle with Iron Giant and Buer monsters. Encounter id: {enc_id}")
        while memory.main.battle_active():
            screen.await_turn()
            if use_grenades or not light_slot:
                buddy_swap(Rikku)
                grenade_thrown = False
                while memory.main.battle_active():
                    if memory.main.turn_ready():
                        if Rikku.is_turn():
                            if use_grenades and not grenade_thrown:
                                logger.debug(f"Grenade Slot {use_grenade_slot}")
                                use_item(use_grenade_slot, "none")
                                grenade_thrown = True
                            elif not light_slot:
                                steal()
                                light_slot = memory.main.get_item_slot(57) != 255
                            elif not Rikku.has_overdrive():
                                CurrentPlayer().attack()
                            else:
                                flee_all()
                        else:
                            if not Rikku.is_status_ok():
                                flee_all()
                            elif not Rikku.has_overdrive():
                                escape_one()
                            elif light_slot and (not use_grenades or grenade_thrown):
                                flee_all()
                            else:
                                CurrentPlayer().defend()
            else:
                flee_all()
    elif enc_id in [154, 156, 164] and use_grenades:
        logger.info(f"Battle with random mobs including Buer. Encounter id: {enc_id}")
        while memory.main.battle_active():
            screen.await_turn()
            if use_grenades:
                buddy_swap(Rikku)
                use_item(use_grenade_slot, "none")
            flee_all()
    elif memory.main.next_steal_rare() or (
        not game_vars.get_blitz_win() and not petrify_slot and enc_id in [153, 154, 163]
    ):
        logger.debug("Grabbing petrify grenade. Blitz Loss only strat.")
        while memory.main.battle_active():
            if memory.main.turn_ready():
                if enc_id in [153, 163]:
                    if Tidus.is_turn():
                        buddy_swap(Rikku)
                        screen.await_turn()
                        steal()
                    else:
                        buddy_swap(Tidus)
                        screen.await_turn()
                        flee_all()
                else:
                    if Tidus.is_turn():
                        buddy_swap(Rikku)
                        screen.await_turn()
                        steal_right()
                    else:
                        buddy_swap(Tidus)
                        screen.await_turn()
                        flee_all()
    else:  # Nothing useful this battle. Moving on.
        flee_all()
    logger.info("Battle is ended - Thunder Plains")
    while not memory.main.user_control():
        if memory.main.game_over():
            seed_str = str(memory.main.rng_seed())
            avina_memory.add_battle_to_memory(
                seed=seed_str, area="t_plains_heals", battle_num=battle_count - 1
            )
            return False
        elif memory.main.battle_wrap_up_active():
            wrap_up()
    memory.main.wait_frames(2)  # Allow lightning to attemt a strike
    if memory.main.dodge_lightning(game_vars.get_l_strike()):
        logger.debug("Dodge")
        game_vars.set_l_strike(memory.main.l_strike_count())
    logger.debug("Checking party format and resolving if needed.")
    memory.main.update_formation(Tidus, Wakka, Auron, full_menu_close=False)
    logger.debug(
        "Party format is good. Now checking health values (check for ambush only)."
    )
    logger.debug(f"ML heals value: {game_vars.ml_heals()}")
    if game_vars.ml_heals():
        logger.warning("aVIna deciding if we need to heal.")
        if battle_count in heal_array:
            heal_up()
    else:
        logger.warning("Old heal logic.")
        if (
            Tidus.in_danger(400)
            or Auron.in_danger(400)
            or Wakka.in_danger(400)
            or Rikku.in_danger(280)
        ):
            heal_up()
        elif 1 in memory.main.ambushes():
            heal_up()
    memory.main.close_menu()
    logger.debug("Ready to continue onward.")
    return True


@battle.utils.speedup_decorator
def m_woods():
    logger.debug("Logic depends on completion of specific goals. In Order:")
    encounter_id = get_encounter_id()
    logger.debug(f"Battle Start - Battle Number: {encounter_id}")
    # need_arctic_wind, need_fish_scale = False, False
    # I think we can just skip these thanks to RNG manip.
    need_arctic_wind, need_fish_scale = True, True
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if memory.main.get_use_items_slot(24) == 255:
                need_arctic_wind = True
            if memory.main.get_use_items_slot(32) == 255:
                need_fish_scale = True
            rikku_charged = Rikku.has_overdrive()
            kimahri_charged = Kimahri.has_overdrive()
            logging.info(f"Rikku charge state: {rikku_charged}")
            logging.info(f"Kimahri charge state: {kimahri_charged}")
            if not rikku_charged:
                if (
                    need_arctic_wind
                    or need_fish_scale
                    and encounter_id in [171, 172, 175]
                ):
                    if check_petrify_tidus() or not Rikku.active():
                        logger.info("Tidus or Rikku incapacitated, fleeing")
                        flee_all()
                    elif not Rikku.active():
                        if encounter_id == 175 and need_arctic_wind:
                            buddy_swap(Rikku)
                        elif encounter_id in [171, 172] and need_fish_scale:
                            buddy_swap(Rikku)
                        else:
                            flee_all()
                    elif Rikku.is_turn():
                        if encounter_id == 175 and need_arctic_wind:
                            logger.debug("Marker 2")
                            steal_new()
                        elif encounter_id == 172 and need_fish_scale:
                            logger.debug("Marker 3")
                            steal_down()
                        elif encounter_id == 171 and need_fish_scale:
                            logger.debug("Marker 4")
                            steal_right()
                        elif not Rikku.has_overdrive():
                            logger.debug("Charging")
                            CurrentPlayer().attack(target_id=Rikku, direction_hint="u")
                        else:
                            logger.debug("Escaping")
                            flee_all()
                    elif not Rikku.has_overdrive():
                        escape_one()
                    else:
                        flee_all()
                elif Rikku.is_turn():
                    if memory.main.next_steal_rare(pre_advance=2):
                        # Manip for crit
                        _steal()
                    else:
                        CurrentPlayer().defend()
                elif not Rikku.active():
                    buddy_swap(Rikku)
                elif Kimahri.is_turn() and not Kimahri.has_overdrive():
                    Kimahri.defend()
                elif not Kimahri.active() and not kimahri_charged:
                    buddy_swap(Kimahri)
                else:
                    escape_one()
            elif memory.main.next_steal_rare(pre_advance=2):
                logger.debug("Looking ahead, manip for non-crit steal")
                if not Rikku.active():
                    buddy_swap(Rikku)
                    steal_new()
                else:
                    flee_all()
            else:
                logger.debug("Looking ahead, no need to manip")
                flee_all()

    if memory.main.game_over():
        # aVIna heal logic handled by 'area' file.
        return False
    logger.info("Battle complete, now to deal with the aftermath.")
    wrap_up()


def spheri_spell_item_ready():
    if memory.main.get_char_weakness(20) == 1:
        if memory.main.get_item_slot(27) > 200:
            return False
    elif memory.main.get_char_weakness(20) == 2:
        if memory.main.get_item_slot(24) > 200:
            return False
    elif memory.main.get_char_weakness(20) == 4:
        if memory.main.get_item_slot(30) > 200:
            return False
    elif memory.main.get_char_weakness(20) == 8:
        if memory.main.get_item_slot(32) > 200:
            return False
    return True


def negator_with_steal():
    tidus_turns = 0
    rikku_turns = 0
    kimahriturns = 0
    luluturns = 0
    yunaturns = 0
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if Tidus.is_turn():
                if rikku_turns == 0:
                    buddy_swap(Rikku)
                # elif faint_check(): #Optional revive on Kimahri
                #    revive()
                else:
                    CurrentPlayer().defend()
                tidus_turns += 1
            elif Kimahri.is_turn():
                lightningmarbleslot = memory.main.get_use_items_slot(30)
                if kimahriturns == 0:
                    use_item(lightningmarbleslot)
                elif kimahriturns == 1:
                    CurrentPlayer().swap_battle_weapon()
                elif kimahriturns == 2:
                    _steal()
                elif not Tidus.active():
                    buddy_swap(Tidus)
                else:
                    CurrentPlayer().defend()
                kimahriturns += 1
            elif Lulu.is_turn():
                if luluturns == 0:
                    revive()
                else:
                    buddy_swap(Yuna)
                luluturns += 1
            elif Yuna.is_turn():
                if yunaturns == 0:
                    revive()
                else:
                    buddy_swap(Tidus)
                yunaturns += 1
            elif Rikku.is_turn():
                lightningmarbleslot = memory.main.get_use_items_slot(30)
                if rikku_turns == 0:
                    use_item(lightningmarbleslot, target=21)
                    while memory.main.get_enemy_current_hp()[1] == 1000:
                        pass
                    if memory.main.get_enemy_current_hp()[1] != 0:
                        rikku_turns -= 1
                elif rikku_turns in [1, 2]:
                    use_item(lightningmarbleslot)
                elif tidus_turns < 2:
                    CurrentPlayer().swap_battle_weapon()
                else:
                    logger.debug("Starting Rikkus overdrive")
                    rikku_full_od("crawler")
                rikku_turns += 1


def get_anima_item_slot():
    useable_slot = memory.main.get_use_items_slot(32)
    if useable_slot > 200:
        useable_slot = memory.main.get_use_items_slot(30)
    if useable_slot > 200:
        useable_slot = memory.main.get_use_items_slot(24)
    if useable_slot > 200:
        useable_slot = memory.main.get_use_items_slot(27)
    if useable_slot > 200:
        useable_slot = 255
    return useable_slot


def _print_confused_state():
    logger.debug("Confused states:")
    logger.debug(f"Yuna confusion: {memory.main.state_confused(1)}")
    logger.debug(f"Tidus confusion: {memory.main.state_confused(0)}")
    logger.debug(f"Kimahri confusion: {memory.main.state_confused(3)}")
    logger.debug(f"Auron confusion: {memory.main.state_confused(2)}")
    logger.debug(f"Lulu confusion: {memory.main.state_confused(5)}")


@battle.utils.speedup_decorator
def seymour_guado_blitz_win():
    od_array = memory.main.kim_od_unlocks()
    tidushaste = False
    kimahriconfused = False
    missbackup = False
    kimahridead = False
    tidus_turns = 0
    yunaturns = 0
    kimahriturns = 0
    auronturns = 0
    wakka_turns = 0
    rikku_turns = 0
    animahits = 0
    animamiss = 0
    steal_count = 0
    rareptr = 0
    swap_timing = 4
    anima_targets = rng_track.enemy_target_predictions()

    while not memory.main.turn_ready():
        pass
    screen.await_turn()
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            for i in range(0, 3):
                if memory.main.get_battle_hp()[i] == 0:
                    if memory.main.get_battle_char_slot(2) == i:
                        logger.debug("Auron is dead")
                    elif memory.main.get_battle_char_slot(3) == i:
                        logger.debug("Kimahri is dead")
                        kimahridead = True
                    elif memory.main.get_battle_char_slot(4) == i:
                        logger.debug("Wakka is dead")
            if Tidus.is_turn():
                logger.debug("Tidus turn start!")
                next_hit = rng_track.next_action_hit(
                    character=memory.main.get_current_turn(), enemy="anima"
                )
                logger.debug("Mark 1")
                if tidus_turns == 0:
                    logger.debug("Tidus Haste self")
                    tidus_haste("none")
                    tidushaste = True
                elif tidus_turns == 1:
                    logger.debug("Talk to Seymour")
                    while not memory.main.other_battle_menu():
                        xbox.tap_left()
                    while memory.main.battle_cursor_2() != 1:
                        xbox.tap_down()
                    while memory.main.other_battle_menu():
                        xbox.tap_b()
                    xbox.tap_left()
                    tap_targeting()
                elif tidus_turns == 2:
                    logger.debug("Tidus defend")
                    CurrentPlayer().defend()
                elif tidus_turns == 3:
                    logger.debug("Tidus attack Seymour")
                    CurrentPlayer().attack()
                elif tidus_turns == 4 and anima_targets[2] == 0:
                    logger.debug("Swap Wakka")
                    buddy_swap(Wakka)
                elif who_goes_first_after_current_turn([0,20,21,22,23]) >= 20 and animahits in [2,3] and not next_hit:
                    logger.debug("Next attack warning")
                    if rng_track.enemy_target_predictions(chars=2)[0] == 0 or rng_track.enemy_target_predictions()[0] == 0:
                        logger.debug("Swap to Lulu")
                        buddy_swap(Lulu)
                        CurrentPlayer().defend()
                    else:
                        logger.debug("Attack should be fine.")
                        CurrentPlayer().attack()
                elif not tidushaste:
                    logger.debug("Tidus Haste self (backup)")
                    tidus_haste("none")
                    tidushaste = True
                elif animahits < 4:
                    logger.debug("Regular attack (A)")
                    old_hp = memory.main.get_enemy_current_hp()[3]
                    CurrentPlayer().attack()
                    if memory.main.battle_active():
                        new_hp = memory.main.get_enemy_current_hp()[3]
                        if new_hp < old_hp:
                            logger.debug("Hit Anima")
                            animahits += 1
                        else:
                            logger.debug("Miss Anima")
                            animamiss += 1
                else:
                    logger.debug("Regular attack (B)")
                    CurrentPlayer().attack()
                logger.debug("Mark 2")
                tidus_turns += 1
                logger.debug(f"Tidus turns: {tidus_turns}")
            elif Yuna.is_turn():
                logger.debug("Yuna turn start!")
                if yunaturns == 0:
                    CurrentPlayer().swap_battle_weapon()
                else:
                    if 2 not in memory.main.get_active_battle_formation():
                        buddy_swap(Auron)
                    elif not Rikku.active():
                        buddy_swap(Rikku)
                    elif not Wakka.active():
                        buddy_swap(Wakka)
                    elif not Kimahri.active():
                        buddy_swap(Kimahri)
                    else:
                        CurrentPlayer().defend()
                yunaturns += 1
                logger.debug("Yuna turn, complete")
            elif Kimahri.is_turn():
                logger.debug("Kimahri turn start!")
                if kimahriconfused:
                    tidusposition = memory.main.get_battle_char_slot(0)
                    rikkuposition = memory.main.get_battle_char_slot(6)
                    if tidusposition >= 3:
                        buddy_swap(Tidus)
                    elif rikkuposition >= 3:
                        buddy_swap(Rikku)
                elif kimahriturns == 0:
                    # if memory.main.get_item_count(49) >= 2:
                    #     use_item_new(49)
                    # else:
                    Kimahri.overdrive(od_name="stone breath", od_array=od_array)
                elif kimahriturns == 1:
                    CurrentPlayer().defend()
                elif animamiss > 0 and (not missbackup or screen.faint_check() == 0):
                    CurrentPlayer().swap_battle_weapon()
                else:
                    tidusposition = memory.main.get_battle_char_slot(0)
                    rikkuposition = memory.main.get_battle_char_slot(6)
                    if tidusposition >= 3:
                        buddy_swap(Tidus)
                    elif rikkuposition >= 3:
                        buddy_swap(Rikku)
                    elif not memory.main.next_steal_rare(pre_advance=steal_count):
                        steal()
                        steal_count += 1
                        rareptr += 1
                    else:
                        CurrentPlayer().defend()
                kimahriturns += 1
                logger.debug("Kimahri turn, complete")
            elif Auron.is_turn():
                logger.debug("Auron turn start!")
                tidusposition = memory.main.get_battle_char_slot(0)
                kimahriposition = memory.main.get_battle_char_slot(3)
                rikkuposition = memory.main.get_battle_char_slot(6)
                if auronturns == 0:
                    _print_confused_state()
                    if memory.main.state_confused(3):
                        remedy(character=Kimahri, direction="l")
                        kimahriconfused = True
                    elif Kimahri.is_dead():
                        revive_target(target=3)
                    else:
                        CurrentPlayer().defend()
                elif auronturns == 1:  # Stone Breath logic
                    if anima_targets[2] != 2 and rikkuposition >= 3:
                            buddy_swap(Rikku)
                    else:
                        if Kimahri.is_dead():
                            revive_target(target=3)
                        else:
                            CurrentPlayer().defend()
                elif animamiss > 0 and (not missbackup or screen.faint_check() == 0):
                    if kimahridead and rikku_turns == 0:
                        if rikkuposition >= 3:
                            buddy_swap(Rikku)
                        elif tidusposition >= 3:
                            buddy_swap(Tidus)
                        elif kimahriposition >= 3:
                            buddy_swap(Kimahri)
                        else:
                            CurrentPlayer().defend()
                    else:
                        CurrentPlayer().defend()
                else:
                    if tidusposition >= 3:
                        buddy_swap(Tidus)
                    elif rikkuposition >= 3:
                        buddy_swap(Rikku)
                    elif kimahriposition >= 3:
                        buddy_swap(Kimahri)
                    else:
                        CurrentPlayer().defend()
                auronturns += 1
                logger.debug("Auron turn, complete")
            elif Wakka.is_turn():
                logger.debug("Wakka turn start!")
                if wakka_turns == 0:
                    CurrentPlayer().swap_battle_weapon()
                elif animamiss > 0 and (not missbackup or screen.faint_check() == 0):
                    if kimahridead and rikku_turns == 0:
                        buddy_swap(Rikku)
                    else:
                        CurrentPlayer().swap_battle_weapon()
                else:
                    tidusposition = memory.main.get_battle_char_slot(0)
                    rikkuposition = memory.main.get_battle_char_slot(6)
                    if tidusposition >= 3:
                        buddy_swap(Tidus)
                    elif rikkuposition >= 3:
                        buddy_swap(Rikku)
                    else:
                        CurrentPlayer().defend()
                wakka_turns += 1
                logger.debug("Wakka turn, complete")
            elif Rikku.is_turn():
                logger.debug("Rikku turn start!")
                if screen.faint_check() == 2:
                    revive_all()
                    missbackup = True
                    tidushaste = False
                elif animamiss > 0 and (not missbackup or screen.faint_check() == 0):
                    if kimahridead and rikku_turns == 0:
                        if not memory.main.next_steal_rare(pre_advance=steal_count):
                            steal()
                        elif memory.main.next_steal(steal_count=steal_count, pre_advance=rareptr):
                            if not memory.main.next_steal_rare(pre_advance=rareptr):
                                steal()
                            else:
                                CurrentPlayer().defend()
                        else:
                            CurrentPlayer().defend()
                    else:
                        if memory.main.get_battle_char_slot(0) >= 3:
                            buddy_swap(Tidus)
                        # elif memory.main.get_battle_char_slot(1) >= 3:
                        #    buddy_swap(Yuna)
                        # elif memory.main.get_battle_char_slot(5) >= 3:
                        #    buddy_swap(Lulu)
                        else:
                            CurrentPlayer().defend()
                elif animahits < 4:
                    if memory.main.next_steal(steal_count=steal_count, pre_advance=rareptr):
                        if not memory.main.next_steal_rare(pre_advance=rareptr):
                            steal()
                        else:
                            CurrentPlayer().defend()
                    else:
                        CurrentPlayer().defend()
                elif (
                    memory.main.get_battle_hp()[memory.main.get_battle_char_slot(0)]
                    == 0
                ):
                    revive_target(target=0)
                else:
                    CurrentPlayer().defend()
                rikku_turns += 1
                logger.debug("Rikku turn, complete")
            elif Lulu.is_turn():
                logger.debug("Lulu turn start!")
                if not missbackup:
                    revive()
                    missbackup = True
                else:
                    tidusposition = memory.main.get_battle_char_slot(0)
                    rikkuposition = memory.main.get_battle_char_slot(6)
                    if tidusposition >= 3:
                        buddy_swap(Tidus)
                    elif rikkuposition >= 3:
                        buddy_swap(Rikku)
                    else:
                        CurrentPlayer().defend()
                logger.debug("Lulu turn, complete")
            else:
                logger.debug("No turn. Holding for next action.")
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
            logger.debug("Diag skip")
    if memory.main.get_enemy_current_hp()[1] == 0:
        split_timer()
    while not memory.main.battle_wrap_up_active():
        if memory.main.game_over():
            logger.info(f"Seymour section fail! Resetting! (B)")
            return False
    
    wrap_up()
    logger.info(f"Seymour section complete! (B)")
    return True


@battle.utils.speedup_decorator
def seymour_guado_blitz_loss():
    xbox.click_to_battle()
    od_array = memory.main.kim_od_unlocks()

    tidushaste = False
    kimahriconfused = False
    missbackup = False
    kimahridead = False
    tidus_turns = 0
    yunaturns = 0
    kimahriturns = 0
    wakka_turns = 0
    rikku_turns = 0
    animahits = 0
    animamiss = 0
    thrown_items = 0

    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            for i in range(0, 3):
                if memory.main.get_battle_hp()[i] == 0:
                    if memory.main.get_battle_char_slot(2) == i:
                        logger.debug("Auron is dead")
                    elif memory.main.get_battle_char_slot(3) == i:
                        logger.debug("Kimahri is dead")
                        kimahridead = True
                    elif memory.main.get_battle_char_slot(4) == i:
                        logger.debug("Wakka is dead")
            if Tidus.is_turn():
                if memory.main.get_enemy_current_hp()[1] < 2999:
                    attack()
                    logger.debug("Should be last attack of the fight.")
                elif tidus_turns == 0:
                    logger.debug("Tidus Haste self")
                    tidus_haste("none")
                    tidushaste = True
                elif tidus_turns == 1:
                    logger.debug("Talk to Seymour")
                    while not memory.main.other_battle_menu():
                        xbox.tap_left()
                    while memory.main.battle_cursor_2() != 1:
                        xbox.tap_down()
                    while memory.main.other_battle_menu():
                        xbox.tap_b()
                    xbox.tap_left()
                    tap_targeting()
                elif tidus_turns == 2:
                    cheer()
                elif tidus_turns == 3:
                    Tidus.attack()
                    #logger.debug("Swap to Brotherhood")
                    #Tidus.swap_battle_weapon(named_equip="brotherhood")
                elif tidus_turns == 4:
                    buddy_swap(Wakka)
                elif (
                    animahits + animamiss == 3 and animamiss > 0 and not missbackup
                    and memory.main.get_enemy_current_hp()[3] > 0
                ):
                    buddy_swap(Lulu)
                    screen.await_turn()
                    revive()
                    missbackup = True
                elif not tidushaste:
                    logger.debug("Tidus Haste self")
                    tidus_haste("none")
                    tidushaste = True
                elif animahits < 4:
                    old_hp = memory.main.get_enemy_current_hp()[3]
                    attack()
                    if memory.main.battle_active():
                        new_hp = memory.main.get_enemy_current_hp()[3]
                        if new_hp < old_hp:
                            logger.debug("Hit Anima")
                            animahits += 1
                        else:
                            logger.debug("Miss Anima")
                            animamiss += 1
                else:
                    logger.debug("Plain Attacking")
                    attack()
                tidus_turns += 1
                logger.debug(f"Tidus turns: {tidus_turns}")
            elif Yuna.is_turn():
                if yunaturns == 0:
                    CurrentPlayer().swap_battle_weapon()
                else:
                    buddy_swap(Auron)
                    screen.await_turn()
                    _print_confused_state()
                    if memory.main.state_confused(3):
                        remedy(character=Kimahri, direction="l")
                        kimahriconfused = True
                    else:
                        CurrentPlayer().defend()
                yunaturns += 1
                logger.debug("Yuna turn, complete")
            elif Auron.is_turn():
                buddy_swap(Rikku)
            elif Kimahri.is_turn():
                if kimahriconfused:
                    tidusposition = memory.main.get_battle_char_slot(0)
                    rikkuposition = memory.main.get_battle_char_slot(6)
                    if tidusposition >= 3:
                        buddy_swap(Tidus)
                    elif rikkuposition >= 3:
                        buddy_swap(Rikku)
                    else:
                        CurrentPlayer().defend()
                elif kimahriturns == 0:
                    if memory.main.get_item_count(49) >= 2:
                        use_item_new(49)
                    else:
                        Kimahri.overdrive(od_name="stone breath", od_array=od_array)
                elif thrown_items < 2:
                    item_slot = get_anima_item_slot()
                    if item_slot != 255:
                        use_item(item_slot)
                    else:
                        steal()
                    thrown_items += 1
                elif animamiss > 0 and (not missbackup or screen.faint_check() == 0):
                    steal()
                else:
                    tidusposition = memory.main.get_battle_char_slot(0)
                    rikkuposition = memory.main.get_battle_char_slot(6)
                    if tidusposition >= 3:
                        buddy_swap(Tidus)
                    elif rikkuposition >= 3:
                        buddy_swap(Rikku)
                    else:
                        steal()
                kimahriturns += 1
                logger.debug("Kimahri turn, complete")
            elif Lulu.is_turn():
                tidusposition = memory.main.get_battle_char_slot(0)
                rikkuposition = memory.main.get_battle_char_slot(6)
                kimahriposition = memory.main.get_battle_char_slot(3)
                if tidusposition >= 3:
                    buddy_swap(Tidus)
                elif rikkuposition >= 3:
                    buddy_swap(Rikku)
                elif kimahriposition >= 3:
                    buddy_swap(Kimahri)
                else:
                    CurrentPlayer.defend()
            elif Wakka.is_turn():
                if wakka_turns == 0:
                    CurrentPlayer().swap_battle_weapon()
                elif animamiss > 0 and (not missbackup or screen.faint_check() == 0):
                    if kimahridead and rikku_turns < 2:
                        buddy_swap(Rikku)
                    else:
                        CurrentPlayer().swap_battle_weapon()
                else:
                    tidusposition = memory.main.get_battle_char_slot(0)
                    rikkuposition = memory.main.get_battle_char_slot(6)
                    if tidusposition >= 3:
                        buddy_swap(Tidus)
                    elif rikkuposition >= 3:
                        buddy_swap(Rikku)
                    else:
                        CurrentPlayer().defend()
                wakka_turns += 1
                logger.debug("Wakka turn, complete")
            elif Rikku.is_turn():
                if screen.faint_check() == 2:
                    revive_all()
                    missbackup = True
                    tidushaste = False
                elif thrown_items < 2:
                    item_slot = get_anima_item_slot()
                    if item_slot != 255:
                        use_item(item_slot)
                    else:
                        steal()
                    thrown_items += 1
                else:
                    #tidusposition = memory.main.get_battle_char_slot(0)
                    #if tidusposition >= 3:
                    #    buddy_swap(Tidus)
                    if animamiss > 0 and (
                        not missbackup or screen.faint_check() == 0
                    ):
                        steal()
                    elif animahits < 4:
                        steal()
                    elif (
                        memory.main.get_battle_hp()[memory.main.get_battle_char_slot(0)]
                        == 0
                    ):
                        revive_target(target=0)
                    else:
                        CurrentPlayer().defend()
                rikku_turns += 1
                logger.debug("Rikku turn, complete")
            else:
                logger.debug("No turn. Holding for next action.")
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
            logger.debug("Diag skip")
    memory.main.wait_frames(3)
    if memory.main.game_over():
        logger.info(f"Seymour section fail! Resetting! (C)")
        return False
    split_timer()
    wrap_up()
    logger.info(f"Seymour section complete. (C)")
    return True


def seymour_guado() -> bool:
    if game_vars.get_blitz_win():
        return seymour_guado_blitz_win()
    else:
        return seymour_guado_blitz_loss()


def escape_with_xp():
    rikku_item = False
    item_to_use = 255
    # Guide says to only use silence grenade. Unsure if we even want petrify.
    if memory.main.get_item_slot(39) < 200:
        item_to_use = 39  # Silence grenade
    elif memory.main.get_item_slot(49) < 200:
        item_to_use = 49  # Petrify grenade
    
    if item_to_use == 255:
        flee_all()
        wrap_up()
    else:
        while not memory.main.turn_ready():
            pass
        while memory.main.battle_active():
            if memory.main.turn_ready():
                if Tidus.is_turn():
                    #if not rikku_item:
                    #    Tidus.swap_battle_armor(ability=[0x8028])
                    #    screen.await_turn()
                    #    buddy_swap(Rikku)
                    #else:
                    CurrentPlayer().attack()
                elif Rikku.is_turn():
                    if not rikku_item:
                        use_item(memory.main.get_use_items_slot(item_to_use))
                        rikku_item = True
                    else:
                        CurrentPlayer().defend()
                elif Yuna.is_turn():
                    Yuna.defend()
                else:
                    Tidus_slot = memory.main.get_battle_char_slot(0)
                    Rikku_slot = memory.main.get_battle_char_slot(6)
                    Yuna_slot = memory.main.get_battle_char_slot(3)
                    if Rikku_slot == 255:
                        flee_all()
                    elif Tidus_slot != 255 and not Tidus.active():
                        buddy_swap(Tidus)
                    elif Rikku_slot != 255 and not Rikku.active():
                        buddy_swap(Rikku)
                    elif Yuna_slot != 255 and not Yuna.active():
                        buddy_swap(Yuna)
                    else:
                        CurrentPlayer().defend()
        wrap_up()


def fullheal(target: int, direction: str):
    logger.info("Full Heal function")
    if memory.main.get_throw_items_slot(2) < 255:
        itemnum = 2
        itemname = "X-Potion"
    elif memory.main.get_throw_items_slot(8) < 255:
        itemnum = 8
        itemname = "Elixir"
    elif memory.main.get_throw_items_slot(3) < 255:
        itemnum = 3
        itemname = "Mega-Potion"
        target = 255
    else:
        itemnum = -1
        itemname = "noitemfound"

    if itemnum >= 0:
        logger.debug(f"Using item: {itemname}")
        _use_healing_item(target, direction, itemnum)
        return 1
    else:
        logger.warning("No restorative items available")
        return 0


# Process written by CrimsonInferno
def wendigo_res_heal(turn_char: int, use_power_break: int, tidus_max_hp: int):
    try:
        logger.debug("Wendigo Res/Heal function")
        party_hp = memory.main.get_battle_hp()
        if screen.faint_check() == 2:
            logger.debug("2 Characters are dead")
            if memory.main.get_throw_items_slot(7) < 255:
                revive_all()
            elif memory.main.get_throw_items_slot(6) < 255:
                revive_target(target=0)
        # If just Tidus is dead revive him
        elif party_hp[memory.main.get_battle_char_slot(0)] == 0:
            logger.debug("Reviving tidus")
            revive()
        elif use_power_break:
            logger.debug("Swapping to Auron to Power Break")
            buddy_swap(Auron)
        # If tidus is less than max HP heal him
        elif party_hp[memory.main.get_battle_char_slot(0)] < tidus_max_hp:
            logger.debug("Tidus need healing")
            if fullheal(target=0, direction="l") == 0:
                if screen.faint_check():
                    logger.debug("No healing available so reviving instead")
                    if memory.main.get_throw_items_slot(6) < 255:
                        revive()
                    elif memory.main.get_throw_items_slot(7) < 255:
                        revive_all()
                else:
                    CurrentPlayer().defend()
        elif screen.faint_check():
            logger.debug("Reviving non-Tidus")
            revive()
        else:
            return False
    except:
        return False

    return True


@battle.utils.speedup_decorator
def zu():
    screen.await_turn()
    CurrentPlayer().attack()
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if memory.main.party_size() <= 2:
                if memory.unlocks.has_ability_unlocked(
                    character_index=0,
                    ability_name="Steal"
                ) and Tidus.is_turn():
                    steal_new(0)
                else:
                    CurrentPlayer().defend()
            elif Tidus.is_turn():
                Tidus.flee()
            elif not check_tidus_ok():
                escape_one()
            else:
                CurrentPlayer().defend()
        elif memory.main.diag_skip_possible():
            xbox.tap_b()  # Skip Dialog
    if memory.main.game_over():
        return False
    memory.main.click_to_control()
    if game_vars.god_mode():
        rng_track.force_preempt()
    return True


@battle.utils.speedup_decorator
def bikanel_battle_logic(status, sandy_fight_complete: bool = False):
    # status should be an array length 4
    # [rikku_charged (unused), speed_needed, power_needed, items_needed]
    encounter_id = get_encounter_id()
    logger.warning(f"DESERT BATTLE {encounter_id} START")
    logger.warning(status)
    item_stolen = status[3] <= 0
    item_thrown = False
    throw_power = False
    throw_speed = False

    # Set throw encounters, only if we still need speed or power.
    if encounter_id in [199,200,208,209,221]:
        if status[1]:
            throw_speed = True
        if status[2]:
            throw_power = True
    if encounter_id in [218,222]:
        if status[2]:
            throw_power = True
    
    logger.warning(f"A - {throw_power} | {throw_speed} > {item_thrown}")
    if not throw_speed and not throw_power:
        item_thrown = True
    logger.warning(f"B - {throw_power} | {throw_speed} > {item_thrown}")

    # Set steal targets
    steal_slot = 20
    if encounter_id in [201,203,204,205,210,212,213,215,219,223,224,226,227]:
        item_stolen = True # Don't steal for these encounters. See Google Sheet list.
    else:
        if encounter_id in [209,217,221,222]:
            steal_slot = 21  # Check 226 later

        # Zu needs special logic.
        if encounter_id in [202, 211, 216, 225]:  # Zu battles
            steal_slot = 20
    
    # Flee from these battles
    flee_battle = [201,203,205,210,212,215]


    # Here we are going to explicitly state our plan to the console.
    plan = "Plan is to "
    if not item_stolen:
        plan += "steal once, "
    if throw_speed or throw_power:
        plan += "throw an item, and if the battle continues, []"
    plan += "escape or flee."
    logger.debug(f"Story progress: {memory.main.get_story_progress()}")
    xbox.click_to_battle()
        
    # Set charges
    logger.debug(f"Rikku: {Rikku.overdrive_percent(combat=False)}")
    charge_rikku = bool(Rikku.overdrive_percent() != 100)
    logger.debug(f"Kimahri: {Kimahri.overdrive_percent(combat=False)}")
    charge_kimahri = bool(Kimahri.overdrive_percent() != 100 and (
        game_vars.story_mode() or
        game_vars.platinum()
    ))

    logger.debug(f"Auron: {Auron.overdrive_percent(combat=False)} ({sandy_fight_complete})")
    charge_auron = bool(Auron.overdrive_percent(combat=False) != 100 and not sandy_fight_complete)
    # If sandy fight complete, we do not need to recharge Auron.
    
    
    # We don't want to do too much. This helps with that.
    # That messes with Wakka's logic, so it's not worth.
    if (
        memory.main.get_story_progress() >= 1718 and
        memory.main.get_story_progress() < 1720
    ):
        logger.info("Too early, don't do too much until Rikku is in party.")
        if not item_stolen:
            throw_speed = False
            throw_power = False
        charge_rikku = False
        charge_kimahri = False
        charge_auron = False
    if charge_auron:
        charge_rikku = False

    logger.warning(f"{charge_kimahri} {charge_rikku} {charge_auron}")

    if charge_auron or charge_kimahri or charge_rikku:
        plan2 = "charge OD for [ "
        if charge_kimahri:
            plan2 += "Kimahri "
        if charge_rikku:
            plan2 += "Rikku "
        if charge_auron:
            plan2 += "Auron "
        plan2 += "] before we "
        plan.replace("[]", plan2)
    else:
        plan.replace("[]","")
    
    
    if memory.main.battle_type() == 2:
        # Check ambushes
        if not encounter_id in [202,211,216,225]:
            logger.warning(f"Ambush = escape for battle {encounter_id}")
            flee_all()
            return
    elif encounter_id in flee_battle:
        logger.warning(f"Preferable flee scenario for {encounter_id}")
        flee_all()
        return
    
    logger.info(plan)  # Report before jumping to first turn.
    # memory.main.wait_frames(120)

    # Now to perform the logic sequentially.
    while memory.main.battle_active():
        '''
        if Tidus.is_turn() and (
            charge_rikku or
            charge_kimahri or
            charge_auron
        ):
            escape_one()
        '''
        if not item_stolen:
            logger.debug("Looking to steal an item.")
            if memory.main.turn_ready():
                if not Kimahri.active():
                    buddy_swap(Kimahri)
                elif not item_stolen and (Kimahri.is_turn() or Rikku.is_turn()):
                    steal_target(steal_slot)
                    item_stolen = True
                else:
                    CurrentPlayer().defend()
                logger.manip(plan)
        elif not item_thrown:
            logger.debug("Looking to throw an item.")
            if memory.main.turn_ready():
                items = update_steal_items_desert()
                if not Kimahri.active():
                    buddy_swap(Kimahri)
                elif not item_thrown:
                    if items[2] >= 1:
                        item_to_use = 40
                    elif items[1] >= 1:
                        item_to_use = 37
                    elif items[3] >= 1:
                        item_to_use = 39
                    else:
                        item_to_use = 999

                    if item_to_use == 999:
                        logger.warning("No items to throw.")
                    else:
                        use_item(memory.main.get_use_items_slot(item_to_use), "none")
                    item_thrown = True
                else:
                    escape_one()
                logger.manip(plan)
        elif memory.main.turn_ready():
            if charge_rikku and not Rikku.active():
                buddy_swap(Rikku)
                logger.manip(plan)
            elif charge_rikku and Rikku.is_turn():
                if Rikku.hp() < 100:
                    Rikku.attack()
                else:
                    Rikku.attack(target_id=6)
                logger.manip(plan)
            elif charge_kimahri and not Kimahri.active():
                buddy_swap(Kimahri)
                logger.manip(plan)
            elif charge_kimahri and Kimahri.is_turn():
                if Kimahri.hp() < 200:
                    Kimahri.attack()
                else:
                    Kimahri.attack(target_id=3)
                logger.manip(plan)
            elif charge_auron and not Auron.active():
                buddy_swap(Auron)
                logger.manip(plan)
            elif charge_auron and Auron.is_turn():
                # Note this can only occur if either Rikku or Kimahri have already charged.
                if Auron.hp() < 200:
                    Auron.attack()
                else:
                    Auron.attack(target_id=2)
                logger.manip(plan)
            elif not charge_rikku and not charge_kimahri and not charge_auron:
                logger.warning("All other needs complete, ready to flee.")
                flee_all()
                return
            else:
                escape_one()
                logger.manip(plan)
    if not memory.main.game_over():
        wrap_up()

@battle.utils.speedup_decorator
def bikanel_battle_logic_old(status, sandy_fight_complete: bool = False):
    # status should be an array length 4
    # [rikku_charged, speed_needed, power_needed, items_needed]
    encounter_id = get_encounter_id()
    item_stolen = False
    item_thrown = False
    throw_power = False
    throw_speed = False
    steal_direction = "none"
    if game_vars.story_mode():
        kimahri_charged = memory.main.overdrive_state()[3] == 100
    else:
        kimahri_charged = True  # Self-destruct not learned on Miihen Highroad.
    logger.debug(f"Starting desert battle: {encounter_id}")
    if memory.main.get_battle_char_slot(3) == 255:
        logger.warning("Kimahri not in party yet. Fleeing and returning.")
        flee_all()
        wrap_up()
        return

    # First, determine what the best case scenario is for each battle.
    if encounter_id == 199:
        steal_direction = "none"
        if status[1]:
            throw_speed = True
        if status[2]:
            throw_power = True
    if encounter_id == 200:
        steal_direction = "none"
        if status[1]:
            throw_speed = True
        if status[2]:
            throw_power = True
    if encounter_id == 208:
        steal_direction = "none"
        if status[1]:
            throw_speed = True
        if status[2]:
            throw_power = True
    if encounter_id == 209:
        steal_direction = "right"
        if status[1]:
            throw_speed = True
        if status[2]:
            throw_power = True
    if encounter_id == 218:
        steal_direction = "none"
        if status[2]:
            throw_power = True
    if encounter_id == 221:
        steal_direction = "up"
        if status[1]:
            throw_speed = True
        if status[2]:
            throw_power = True
    if encounter_id == 222:
        steal_direction = "left"
        if status[2]:
            throw_power = True
    if encounter_id == 226:
        steal_direction = "none"

    zu_battles = [202, 211, 216, 225]
    if encounter_id in zu_battles:  # Zu battles
        steal_direction = "none"
    if encounter_id == 217:  # Special Zu battle
        steal_direction = "up"  # Not confirmed
    # Flee from these battles
    flee_battle = [201, 203, 204, 205, 210, 212, 213, 215, 217, 219, 223, 224, 226, 227]

    # Next, determine what we want to do
    if encounter_id in flee_battle:
        if status[0] and kimahri_charged:
            battle_goal = 3  # Nothing to do here, we just want to flee.
        else:
            battle_goal = 2
    elif memory.main.battle_type() == 2:
        battle_goal = 3
    else:
        items = update_steal_items_desert()
        if items[1] < 2 and memory.main.battle_type() != 2:
            battle_goal = 0  # Steal an item
        elif items[1] == 0 and items[2] == 0 and memory.main.battle_type() != 2:
            battle_goal = 0  # Steal an item
        # Extra items into power/speed
        elif status[3] <= -1 and (throw_power or throw_speed):
            battle_goal = 1  # Throw an item
        elif status[3] > -1:
            # Steal to an excess of one item (so we can throw in future battles)
            battle_goal = 0
        elif not status[0] and memory.main.battle_type() != 2:
            battle_goal = 2  # Rikku or Kimahri still need charging.
        elif not kimahri_charged:
            battle_goal = 3  # Kimahri needs a charge IF story mode is active.
        else:
            battle_goal = 4  # Nothing to do but get to Home.

    # Then we take action.
    while memory.main.battle_active():
        if battle_goal == 0:  # Steal an item
            logger.debug("Looking to steal an item.")
            if memory.main.turn_ready():
                if not Kimahri.active():
                    buddy_swap(Kimahri)
                elif not item_stolen and (Kimahri.is_turn() or Rikku.is_turn()):
                    if steal_direction == "left":
                        steal_left()
                    elif steal_direction == "right":
                        steal_right()
                    elif steal_direction == "up":
                        steal_up()
                    elif steal_direction == "down":
                        steal_down()
                    else:
                        steal()
                    item_stolen = True

                    # After stealing an item, what to do next?
                    if throw_power or throw_speed:
                        battle_goal = 1
                    else:
                        battle_goal = 3
                elif not status[0]:
                    if memory.main.get_battle_char_turn() == 6:
                        CurrentPlayer().attack()
                    else:
                        escape_one()
                else:
                    flee_all()
        elif battle_goal == 1:  # Throw an item
            logger.debug("Throw item with Kimahri, everyone else escape.")
            if memory.main.turn_ready():
                items = update_steal_items_desert()
                if not Kimahri.active():
                    buddy_swap(Kimahri)
                elif not item_thrown and (Kimahri.is_turn() or Rikku.is_turn()):
                    if items[2] >= 1:
                        item_to_use = 40
                    elif items[1] >= 1:
                        item_to_use = 37
                    elif items[3] >= 1:
                        item_to_use = 39
                    else:
                        item_to_use = 999

                    if item_to_use == 999:
                        escape_one()
                    else:
                        use_item(memory.main.get_use_items_slot(item_to_use), "none")
                    item_thrown = True
                elif not status[0]:
                    if Rikku.is_turn() == 6:
                        CurrentPlayer().attack()
                    else:
                        escape_one()
                else:
                    flee_all()
        elif battle_goal == 2:  # Charge Rikku
            logger.debug("Attack/Steal with Rikku, everyone else escape.")
            if memory.main.turn_ready():
                if Rikku.is_turn():
                    if memory.main.get_use_items_slot(20) < 200:
                        use_item(memory.main.get_use_items_slot(20))
                    else:
                        Rikku.attack()
                elif Auron.is_turn() and not Auron.has_overdrive():
                    Auron.attack(target_id=Auron)
                elif Rikku.active():
                    escape_one()
                else:
                    flee_all()
        elif battle_goal == 3:  # Charge Kimahri
            logger.debug("Attack/Steal with Rikku, everyone else escape.")
            if memory.main.turn_ready():
                if Kimahri.is_turn() and game_vars.story_mode():
                    CurrentPlayer().attack()
                elif Auron.is_turn() and not Auron.has_overdrive():
                    Auron.attack(target_id=Auron)
                elif Kimahri.active():
                    escape_one()
                else:
                    flee_all()
        else:  # Charge Auron if needed, otherwise flee
            if not Auron.has_overdrive() and not sandy_fight_complete:
                if Auron.is_turn():
                    Auron.attack(target_id=Auron)
                else:
                    escape_one()
            else:
                logger.debug("Flee all battles, nothing more to do.")
                flee_all()
    if game_vars.god_mode():
        rng_track.force_preempt()


def update_steal_items_desert():
    item_array = [0, 0, 0, 0]
    # Bomb cores
    #index = memory.main.get_item_slot(27)
    #if index == 255:
    item_array[0] = 0  # We're going to ignore bomb cores now.
    #else:
    #    item_array[0] = memory.main.get_item_count_slot(index)

    # Sleeping Powders
    index = memory.main.get_item_slot(37)
    if index == 255:
        item_array[1] = 0
    else:
        item_array[1] = memory.main.get_item_count_slot(index)

    # Smoke Bombs
    index = memory.main.get_item_slot(40)
    if index == 255:
        item_array[2] = 0
    else:
        item_array[2] = memory.main.get_item_count_slot(index)

    # Silence Grenades
    index = memory.main.get_item_slot(39)
    if index == 255:
        item_array[3] = 0
    elif memory.main.get_item_count_slot(index) == 1:
        item_array[3] = 0  # Save one for NEA manip
    else:
        item_array[3] = memory.main.get_item_count_slot(index)

    return item_array


@battle.utils.speedup_decorator
def sandragora(version):
    while not memory.main.turn_ready():
        pass
    if version != 1:  # Second Sandy, reset and try skip again.
        flee_all()
        memory.main.click_to_control()
        return
    if memory.main.battle_type() == 2 and Auron.active():
        while memory.main.battle_type() == 2:
            logger.debug("Ambushed, swapping out.")
            flee_all()
            memory.main.click_to_control()
            FFXC.set_movement(0, 1)
            memory.main.await_event()
            FFXC.set_neutral()
            while not memory.main.turn_ready():
                pass

    if 2 not in memory.main.get_active_battle_formation():
        buddy_swap(Auron)  # Tidus for Auron
    else:
        tidus_haste("l", character=Auron)
    screen.await_turn()
    if Kimahri.is_turn() or Rikku.is_turn():
        logger.debug("Kimahri/Rikku taking a spare turn. Just defend.")
        CurrentPlayer().defend()
        screen.await_turn()
    logger.debug("Setting up Auron overdrive")
    Auron.overdrive(style="shooting star")
    wrap_up()


@battle.utils.speedup_decorator
def home_1():
    FFXC.set_neutral()
    xbox.click_to_battle()
    logger.debug("Tidus vs Bombs")
    
    use_lancet = (
        Kimahri.overdrive_percent() != 100 and 
        not game_vars.story_mode() and 
        (game_vars.platinum() or not game_vars.get_blitz_win())
    )
    throw_petrify = bool(memory.main.get_item_count(49) >= 1)
    petrify_turns = 0
    
    od_learns = 2
    if not throw_petrify:
        tidus_haste("none")
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if screen.faint_check() > 0:
                revive()
            elif Tidus.is_turn():
                if throw_petrify:
                    if petrify_turns == 0:
                        Tidus.defend()
                        petrify_turns += 1
                    elif not Kimahri.active():
                        buddy_swap(Kimahri)
                    else:
                        CurrentPlayer().defend()
                else:
                    CurrentPlayer().attack()
            elif Auron.is_turn() and memory.main.get_enemy_current_hp()[0] != 0:
                CurrentPlayer().attack()
            elif not Kimahri.active() and (
                use_lancet or throw_petrify
            ):
                buddy_swap(Kimahri)  # Tidus for Kimahri
            elif Kimahri.is_turn():
                if use_lancet:
                    lancet_target(target=23, direction="d", post_steal=True)
                    use_lancet = False
                    od_learns += 1
                elif throw_petrify:
                    use_item_new(49)
                    throw_petrify = False
                elif not Tidus.active():
                    buddy_swap(Tidus)
                else:
                    CurrentPlayer().defend()
            elif not Tidus.active():
                buddy_swap(Tidus)
            else:
                CurrentPlayer().defend()
    logger.debug("Home 1 shows as fight complete.")
    if memory.main.game_over():
        return 0
    memory.main.click_to_control()
    if game_vars.god_mode():
        rng_track.force_preempt()
    return od_learns


@battle.utils.speedup_decorator
def home_2(od_learns=2):
    xbox.click_to_battle()
    od_array = memory.main.kim_od_unlocks()  # Just for the report.

    logger.debug("Kimahri vs dual horns")
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if Kimahri.is_turn():
                Kimahri.overdrive(od_name="stone breath", od_array=od_array)
                #if game_vars.get_blitz_win():
                #    Kimahri.overdrive(2)
                #else:
                #    Kimahri.overdrive(od_learns)
            elif memory.main.get_battle_char_slot(3) >= 3:
                buddy_swap(Kimahri)  # Tidus for Kimahri
                logger.warning(f"Kim OD: {Kimahri.overdrive_percent(combat=True)}")
                if Kimahri.overdrive_percent(combat=True) != 100:
                    lancet_target(target=21, direction="l", post_steal=True)
                    od_learns += 1
            else:
                CurrentPlayer().defend()
    logger.debug("Home 2 shows as fight complete.")
    FFXC.set_neutral()
    if memory.main.game_over():
        return False
    memory.main.click_to_control()
    if game_vars.god_mode():
        rng_track.force_preempt()
    return od_learns


@battle.utils.speedup_decorator
def home_3(od_learns):
    return home_2(od_learns) # Same logic is now used. Old logic archived.


def home_3_old():
    logger.debug("Home 3 fight")
    xbox.click_to_battle()
    if memory.main.get_use_items_slot(49) > 200:
        tidus_haste("none")
    else:
        while not Rikku.is_turn():
            CurrentPlayer().defend()
            xbox.click_to_battle()
            use_item(memory.main.get_use_items_slot(49), "none")

    rikku_item_thrown = 0
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            logger.debug("- Turn:")
            if Tidus.is_turn():
                logger.debug("  Tidus")
                if memory.main.get_use_items_slot(49) != 255:
                    CurrentPlayer().defend()
                else:
                    CurrentPlayer().attack()
            elif Rikku.is_turn() and rikku_item_thrown < 1 and home_3_item() != 255:
                logger.debug("  Rikku")
                use_item_slot = home_3_item()
                use_item(use_item_slot, "none")
                rikku_item_thrown += 1
            elif screen.faint_check() > 0:
                logger.debug("  any, revive")
                revive()
            else:
                logger.debug("  any, defend")
                CurrentPlayer().defend()
    FFXC.set_neutral()
    logger.debug("Home 3 shows as fight complete.")
    if game_vars.god_mode():
        rng_track.force_preempt()


def home_3_item():
    throw_slot = memory.main.get_use_items_slot(49)  # Petrify Grenade
    if throw_slot != 255:
        return throw_slot
    throw_slot = memory.main.get_use_items_slot(40)  # Smoke Bomb
    if throw_slot != 255:
        return throw_slot
    throw_slot = memory.main.get_use_items_slot(39)  # Silence - for the Guado-face.
    if throw_slot != 255:
        return throw_slot
    return 255


@battle.utils.speedup_decorator
def home_4():
    xbox.click_to_battle()
    od_array = memory.main.kim_od_unlocks()  # Just for the report.

    logger.debug("Kimahri vs Chimera")
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if Kimahri.is_turn():
                Kimahri.overdrive(od_name="stone breath", od_array=od_array)
                #if game_vars.get_blitz_win():
                #    Kimahri.overdrive(3)
                #else:
                #    Kimahri.overdrive(4)
            elif memory.main.get_battle_char_slot(3) >= 3:
                buddy_swap(Kimahri)  # Tidus for Kimahri
                if Kimahri.overdrive_percent(combat=True) != 100:
                    lancet_target(target=21, direction="u", post_steal=True)
            else:
                CurrentPlayer().defend()
    logger.debug("Home 4 shows as fight complete.")
    if memory.main.game_over():
        return
    memory.main.click_to_control()
    if game_vars.god_mode():
        rng_track.force_preempt()


def distiller_count_total():
    slot1 = memory.main.get_item_slot(16)
    slot2 = memory.main.get_item_slot(17)
    slot3 = memory.main.get_item_slot(18)

    count = memory.main.get_item_count_slot(slot1)
    count += memory.main.get_item_count_slot(slot2)
    count += memory.main.get_item_count_slot(slot3)
    return count


def distiller_target(seed:int=2, ignore=[]):
    targets = memory.main.get_enemy_current_hp(ignore_dead=False)
    final_targets = []
    for i in range(len(targets)):
        if targets[i] > 20 and not i+20 in ignore:
            final_targets.append(i + 20)

    if len(final_targets) == 0:
        logger.warning(f"No available distiller targets: - | Ignored: {ignore}")
        #memory.main.wait_frames(120)  # For testing only
        return 0,0

    logger.warning(f"Distiller target: {final_targets[0]} | Ignored: {ignore}")
    #memory.main.wait_frames(120)  # For testing only
    return final_targets[0], len(final_targets)


def guards_report_items():
    sleep_slot = memory.main.get_item_slot(37)
    silence_slot = memory.main.get_item_slot(39)
    smoke_slot = memory.main.get_item_slot(40)
    power_slot = memory.main.get_item_slot(70)
    speed_slot = memory.main.get_item_slot(72)

    sleep_count = memory.main.get_item_count_slot(sleep_slot)
    silence_count = memory.main.get_item_count_slot(silence_slot)
    smoke_count = memory.main.get_item_count_slot(smoke_slot)
    power_count = memory.main.get_item_count_slot(power_slot)
    speed_count = memory.main.get_item_count_slot(speed_slot)
    
    report_str = f"Sleep: {sleep_count}\n"
    report_str += f"Silence: {silence_count}\n"
    report_str += f"Smoke: {smoke_count}\n"
    report_str += f"Power: {power_count} (15/19)\n"
    report_str += f"Speed: {speed_count} (5)\n"
    write_big_text(report_str)


@battle.utils.speedup_decorator
def guards(group_num, sleeping_powders):
    guards_report_items()
    max_steals = 0
    remaining_steals = 0
    nea_result_array = rng_track.guards_to_calm_equip_drop_count(
        guard_battle_num=group_num
    )
    
    # Now to determine best number of steals
    if group_num in [1,3]:
        max_steals = 2
        if (
            nea_result_array[0] <= nea_result_array[1] and
            nea_result_array[0] <= nea_result_array[2]
        ):
            remaining_steals = 0
        elif nea_result_array[1] <= nea_result_array[2]:
            remaining_steals = 1
        else:
            remaining_steals = 2
    elif group_num in [2,4]:
        # For now, never manip on the fifth fight.
        max_steals = 1
        if nea_result_array[0] <= nea_result_array[1]:
            remaining_steals = 0
        else:
            remaining_steals = 1
    # Group 5, should not need any steals. No else statement needed.
    
    nea_drop_counts = rng_track.guards_to_calm_equip_drop_count(
        guard_battle_num=group_num,
        report_num=remaining_steals
    )
    #logger.debug(f"0-2 Steals result in extras needed: {nea_result_array}")
    logger.warning(f"Expected steals this fight: {remaining_steals}/{max_steals}")
    xbox.click_to_battle()
    distiller_total = distiller_count_total()
    if group_num == 5:
        distiller_count = min(distiller_total,1)
    elif group_num in [1,3]:
        distiller_count = min(distiller_total,2)
    else:
        distiller_count = min(distiller_total,2)
    logger.warning(f"Distillers needed this fight: {distiller_count} | total still needed {distiller_total}")
    distilled_targets = []
    num_throws = 0  # This is for grenade throws.
    hasted = False
    tidus_went = False
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            guards_report_items()
            target, distiller_targets = distiller_target(seed=distiller_count,ignore=distilled_targets)
            if distiller_targets < distiller_count:
                distiller_count = distiller_targets
            logger.manip(memory.main.get_enemy_current_hp())
            if group_num in [1, 3]:
                if Tidus.is_turn():
                    CurrentPlayer().attack()
                elif remaining_steals != 0 and (Rikku.is_turn() or Kimahri.is_turn()):
                    steal()
                    remaining_steals -= 1
                elif remaining_steals != 0 and Lulu.is_turn():
                    if 6 not in memory.main.get_active_battle_formation():
                        buddy_swap(Rikku)
                    elif 3 not in memory.main.get_active_battle_formation():
                        buddy_swap(Kimahri)
                    else:
                        CurrentPlayer.defend()
                elif distiller_count >= 1 and (Rikku.is_turn() or Kimahri.is_turn()):
                    if memory.main.get_item_slot(18) != 255:
                        _use_healing_item(num=target,item_id=18)
                    elif memory.main.get_item_slot(16) != 255:
                        _use_healing_item(num=target,item_id=16)
                    else:
                        _use_healing_item(num=target,item_id=17)
                    distiller_count -= 1
                    distilled_targets.append(target)
                elif (
                    Rikku.active() and Rikku.in_danger(121) and not Rikku.is_dead()
                ):
                    if memory.main.get_item_slot(0) != 255:
                        use_potion_character(Rikku, "r")
                    elif memory.main.get_item_slot(1) != 255:
                        _use_healing_item(num=Rikku, direction="r", item_id=1)
                    else:
                        CurrentPlayer().defend()
                else:
                    CurrentPlayer().defend()
            elif group_num in [2, 4]:
                if Rikku.is_turn():
                    if num_throws < 2:
                        if num_throws == 0:
                            if memory.main.get_item_slot(37) < 200:
                                use_item(memory.main.get_use_items_slot(37))
                            elif memory.main.get_item_slot(39) < 200:
                                use_item(memory.main.get_use_items_slot(39))
                            else:
                                use_item(memory.main.get_use_items_slot(40))
                        else:
                            if memory.main.get_use_items_slot(40) != 255:
                                # Smoke grenade
                                use_item(memory.main.get_use_items_slot(40))
                            elif (
                                memory.main.get_item_slot(37) != 255 and
                                memory.main.get_item_count_slot(memory.main.get_item_slot(37)) > 1
                            ):
                                # Sleep Powder
                                use_item(memory.main.get_use_items_slot(37))
                            elif (
                                memory.main.get_item_slot(39) != 255 and
                                memory.main.get_item_count_slot(memory.main.get_item_slot(39)) > 2
                            ):
                                # Throw Silence grenades last.
                                use_item(memory.main.get_use_items_slot(39))
                            elif memory.main.get_use_items_slot(27) != 255:
                                # If we're throwing bomb cores, we're already in panic mode.
                                use_item(memory.main.get_use_items_slot(27))
                            else:
                                CurrentPlayer().defend()
                        num_throws += 1
                    elif remaining_steals >= 1:
                        steal()
                        remaining_steals -= 1
                    else:
                        CurrentPlayer().defend()
                elif Tidus.is_turn():
                    if not Kimahri.active() and not sleeping_powders and num_throws < 1:
                        buddy_swap(Kimahri)
                        if memory.main.get_item_slot(40) < 200:
                            use_item(memory.main.get_use_items_slot(40))
                        else:
                            use_item(memory.main.get_use_items_slot(39))
                        num_throws += 1
                    else:
                        CurrentPlayer().attack()
                elif Kimahri.is_turn():
                    if not Tidus.active():
                        buddy_swap(Tidus)
                        Tidus.attack()
                    elif remaining_steals >= 1:
                        steal()
                        remaining_steals -= 1
                    else:
                        CurrentPlayer().defend()
                else:
                    CurrentPlayer().defend()

            elif group_num == 5:
                if screen.faint_check():
                    revive()
                elif Tidus.is_turn():
                    if not hasted:
                        tidus_haste("left", character=6)
                        hasted = True
                    else:
                        CurrentPlayer().attack(target_id=22, direction_hint="r")
                elif Rikku.is_turn() or Kimahri.is_turn():
                    silence_slot = memory.main.get_item_slot(39)
                    if num_throws < 2:
                        if memory.main.get_use_items_slot(40) != 255:
                            use_item(memory.main.get_use_items_slot(40))
                        elif memory.main.get_use_items_slot(37) != 255:
                            use_item(memory.main.get_use_items_slot(37))
                        #elif memory.main.get_use_items_slot(27) != 255:
                        #    use_item(memory.main.get_use_items_slot(27))
                        elif memory.main.get_use_items_slot(39) != 255:
                            use_item(memory.main.get_use_items_slot(39))
                            # Silence as a last resort.
                        else:
                            CurrentPlayer().defend()
                        num_throws += 1
                        
                    elif remaining_steals == 1:
                        steal()
                        remaining_steals -= 1
                    else:
                        CurrentPlayer().defend()
        guards_report_items()
    logger.debug("Guards battle complete.")
    wrap_up()

def kottos_fight():
    distiller_thrown = False
    
    power = memory.main.get_item_count_slot(memory.main.get_item_slot(16))
    mana = memory.main.get_item_count_slot(memory.main.get_item_slot(17))
    speed = memory.main.get_item_count_slot(memory.main.get_item_slot(18))
    ability = memory.main.get_item_count_slot(memory.main.get_item_slot(19))

    power_count = memory.main.get_item_count_slot(memory.main.get_item_slot(70))
    mana_count = memory.main.get_item_count_slot(memory.main.get_item_slot(71))
    speed_count = memory.main.get_item_count_slot(memory.main.get_item_slot(72))
    ability_count = memory.main.get_item_count_slot(memory.main.get_item_slot(73))

    xbox.click_to_battle()
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if not distiller_thrown:
                if power_count < 80 and power >= 1:
                    use_item_new(16)
                    distiller_thrown = True
                elif mana_count < 80 and mana >= 1:
                    use_item_new(17)
                    distiller_thrown = True
                elif speed_count < 80 and speed >= 1:
                    use_item_new(18)
                    distiller_thrown = True
                elif ability_count < 80 and ability >= 1:
                    use_item_new(19)
                    distiller_thrown = True
            else:
                CurrentPlayer().attack()
    wrap_up()

def altana_heal():
    direction = "d"
    if memory.main.get_throw_items_slot(2) < 255:
        itemnum = 2
        itemname = "X-Potion"
    elif memory.main.get_throw_items_slot(8) < 255:
        itemnum = 8
        itemname = "Elixir"
    elif memory.main.get_throw_items_slot(6) < 255:
        itemnum = 6
        itemname = "Phoenix Down"
    elif memory.main.get_throw_items_slot(7) < 255:
        itemnum = 7
        itemname = "Phoenix Down"
    else:
        itemnum = -1
        itemname = "noitemfound"
    if itemnum >= 0:
        logger.debug(f"Using item: {itemname}")
        while not memory.main.turn_ready():
            pass
        while memory.main.main_battle_menu():
            if memory.main.battle_menu_cursor() != 1:
                xbox.tap_down()
            else:
                xbox.tap_b()
        while memory.main.main_battle_menu():
            xbox.tap_b()
        item_pos = memory.main.get_throw_items_slot(itemnum)
        logger.debug(f"Position: {item_pos}")
        _navigate_to_position(item_pos)
        while memory.main.other_battle_menu():
            xbox.tap_b()
        logger.debug(f"Direction: {direction}")
        while not memory.main.targeting_enemy():
            if direction == "l":
                xbox.tap_left()
                if not memory.main.targeting_enemy():
                    logger.debug("Wrong battle line targeted.")
                    xbox.tap_right()
                    direction = "u"
            elif direction == "r":
                xbox.tap_right()
                if not memory.main.targeting_enemy():
                    logger.debug("Wrong battle line targeted.")
                    xbox.tap_left()
                    direction = "d"
            elif direction == "u":
                xbox.tap_up()
                if not memory.main.targeting_enemy():
                    logger.debug("Wrong battle line targeted.")
                    xbox.tap_down()
                    direction = "l"
            elif direction == "d":
                xbox.tap_down()
                if not memory.main.targeting_enemy():
                    logger.debug("Wrong battle line targeted.")
                    xbox.tap_up()
                    direction = "r"
        tap_targeting()
        return 1

    else:
        logger.debug("No restorative items available")
        return 0


def highbridge_attack():
    if memory.main.get_enemy_current_hp().count(0) == 1:
        return False
    elif get_encounter_id() == 271:
        CurrentPlayer().attack(target_id=21, direction_hint="l")
    else:
        CurrentPlayer().attack()
    return True



def highbridge_rescue_battle(delay_grid):
    while not memory.main.turn_ready():
        pass  # This is so we don't trigger the wrong battle.
    logger.warning(f"Rescue count check: {game_vars.get_rescue_count()}")
    # memory.main.wait_frames(300)  # For testing
    if game_vars.story_mode() and get_encounter_id() != 272:
        if memory.main.battle_type() == 2:
            # Ambushed
            flee_all()
        else:
            calm_impulse()  # Repurposed, does what we want already.
        wrap_up()
    
    # I don't actually know what this condition is trying to do.
    # I am suspicious this is messing up RNG manipulation.
    # elif (
    #     memory.main.next_chance_rng_10(30) == 0
    #     and memory.main.next_chance_rng_12() == 1
    # ):
    #     steal_occurred = False
    #     while memory.main.battle_active():
    #         if (
    #             game_vars.completed_rescue_fights() and 
    #             not delay_grid
    #         ):
    #             battle.main.flee_all()
    #         elif memory.main.turn_ready():
    #             if Rikku.is_turn() and not steal_occurred:
    #                 battle.main.steal()
    #                 steal_occurred = True
    #             elif not Rikku.active() and not steal_occurred:
    #                 battle.main.buddy_swap(Rikku)
    #             elif Tidus.is_turn() or Yuna.is_turn():
    #                 if not highbridge_attack():
    #                     battle.main.flee_all()
    #             elif not Tidus.active():
    #                 battle.main.buddy_swap(Tidus)
    #             elif not Yuna.active():
    #                 battle.main.buddy_swap(Yuna)
    #             else:
    #                 CurrentPlayer().defend()
    elif get_encounter_id() == 270:  # YAT-63 x2
        while memory.main.battle_active():
            if game_vars.completed_rescue_fights() and not delay_grid:
                flee_all()
            elif memory.main.turn_ready():
                if Tidus.is_turn() or Yuna.is_turn():
                    if memory.main.get_enemy_current_hp().count(0) == 1:
                        flee_all()
                        game_vars.add_rescue_count()
                    else:
                        highbridge_attack()
                else:
                    CurrentPlayer().defend()
    elif get_encounter_id() == 269:  # YAT-63 with two guard guys
        while memory.main.battle_active():
            if game_vars.completed_rescue_fights() and not delay_grid:
                flee_all()
            elif memory.main.turn_ready():
                if Tidus.is_turn() or Yuna.is_turn():
                    if memory.main.get_enemy_current_hp().count(0) == 1:
                        flee_all()
                        game_vars.add_rescue_count()
                    else:
                        highbridge_attack()
                else:
                    CurrentPlayer().defend()
    elif get_encounter_id() == 271:  # one YAT-63, two YAT-99
        while memory.main.battle_active():
            if game_vars.completed_rescue_fights() and not delay_grid:
                flee_all()
            elif memory.main.turn_ready():
                if Tidus.is_turn() or Yuna.is_turn():
                    if memory.main.get_enemy_current_hp().count(0) == 1:
                        flee_all()
                        game_vars.add_rescue_count()
                    else:
                        highbridge_attack()
                else:
                    CurrentPlayer().defend()
    wrap_up()

def attack_highbridge():
    if get_encounter_id() == 271:
        CurrentPlayer().attack(target_id=21, direction_hint="l")
    else:
        CurrentPlayer().attack()


def highbridge_drops():
    advances = memory.main.highbridge_drops()
    if memory.main.get_turn_by_index(turn_index=1) >= 20:
        # We got ambushed. Just hit it very hard.
        screen.await_turn()
        buddy_swap(Yuna)
        aeon_summon(4)
        Bahamut.unique()
    else:
        steal_complete = False
        while memory.main.battle_active():
            if memory.main.turn_ready():
                if Tidus.is_turn():
                    # Tidus logic
                    if 0 in advances or 3 in advances or 6 in advances:
                        buddy_swap(Yuna)
                    elif advances[0] % 3 != 0:
                        buddy_swap(Rikku)
                    else:
                        buddy_swap(Yuna)
                elif Rikku.is_turn():
                    if not steal_complete:
                        if get_encounter_id() == 270:
                            steal_right()
                        elif get_encounter_id() == 271:
                            steal_left()
                        else:
                            steal()
                        steal_complete = True
                    else:
                        if (
                            0 in advances
                            or 3 in advances
                            or 6 in advances
                            or advances[0] > 9
                        ):
                            buddy_swap(Yuna)
                        elif memory.main.get_turn_by_index(turn_index=1) < 20:
                            if get_encounter_id() == 270:
                                steal_right()
                            elif get_encounter_id() == 271:
                                steal_left()
                            else:
                                steal()
                        elif memory.main.get_turn_by_index(turn_index=2) < 20:
                            if get_encounter_id() == 270:
                                steal_right()
                            elif get_encounter_id() == 271:
                                steal_left()
                            else:
                                steal()
                        else:
                            buddy_swap(Tidus)
                            flee_all()
                elif Yuna.is_turn():
                    aeon_summon(4)
                elif Bahamut.is_turn():
                    Bahamut.unique()
                else:
                    buddy_swap(Yuna)
    if game_vars.god_mode():
        rng_track.force_preempt()

def mac_lake_recover():
    logger.info(f"Battle num: {get_encounter_id()}")
    while not memory.main.turn_ready():
        if memory.main.game_over():
            return False
    rikku_counter = 0
    tidus_counter = 0
    
    if memory.main.battle_type() == 2:
        # Any ambush is an immediate flee.
        flee_all()  # Don't need this for speed spheres

    if get_encounter_id() == 177:
        # Eye, Flan, Wolf
        while memory.main.battle_active():
            if memory.main.turn_ready():
                if Rikku.is_turn():
                    if memory.main.get_item_slot(35) != 255 and rikku_counter == 0:
                        Rikku.use_special_by_name(command_name='Steal',target_id=22)
                        rikku_counter += 1
                    elif rikku_counter == 1:
                        use_item_new(item=35)
                        rikku_counter += 1
                    else:
                        escape_one()
                elif Tidus.is_turn():
                    if tidus_counter == 0:
                        Tidus.attack(22)
                        tidus_counter += 1
                    else:
                        flee_all()
                elif not Rikku.active():
                    buddy_swap(Rikku)
                elif not Tidus.active():
                    buddy_swap(Tidus)
                # elif Lulu.is_turn():
                #     Lulu.cast_black_magic_spell_by_name(spell_name='Fire',target_id=21)
                # elif not Lulu.active():
                #     buddy_swap(Lulu)
                else:
                    # This should never occur.
                    escape_one()
        wrap_up()
    elif get_encounter_id() == 179:
        # Wolf, Flan, Wolf
        flee_all()  # Don't need this for speed spheres
    elif get_encounter_id() == 178:
        # Wolf, Flan, Mafdet
        flee_all()  # Don't need this for speed spheres
    else:
        print(f"ENCOUNTER ERROR: {get_encounter_id()}")
        quit()


def mac_flee_xp():
    while not memory.main.turn_ready():
        if memory.main.game_over():
            return False
    if memory.main.get_item_slot(39) != 255 or memory.main.get_item_slot(49) != 255:
        battle.main.escape_with_xp()
    else:
        while memory.main.battle_active():
            if memory.main.turn_ready():
                if not Tidus.active():
                    buddy_swap(Tidus)
                elif Tidus.is_turn():
                    Tidus.attack()
                else:
                    CurrentPlayer().defend()
    if memory.main.game_over():
        return False
    wrap_up()
    return True


def calm_impulse():
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Bahamut.is_turn():
                Bahamut.unique()
            elif not Yuna.active():
                buddy_swap(Yuna)
            elif Yuna.is_turn():
                aeon_summon(4)
            else:
                CurrentPlayer().defend()
    wrap_up()


def one_eye(killer:str="any"):
    aeon_summon_bool = bool(killer=="aeon")
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if not Yuna.active() and Rikku.is_turn():
                buddy_swap(Yuna)
            elif aeon_summon_bool:
                if Bahamut.is_turn():
                    Bahamut.unique()
                    aeon_summon_bool=False
                elif (
                    Yuna.is_turn() and 
                    memory.main.get_enemy_current_hp()[0] < 70999
                ):
                    aeon_summon(4)
                elif (
                    Tidus.is_turn() and
                    memory.main.get_enemy_current_hp()[0] > 99999
                ):
                    Tidus.attack()
                elif (
                    not Tidus.is_turn() and
                    memory.main.get_enemy_current_hp()[0] > 70000
                ):
                    CurrentPlayer().attack()
                else:
                    CurrentPlayer().defend()
            else:
                CurrentPlayer().attack()
    wrap_up()


@battle.utils.speedup_decorator
def gagazet_path():
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Rikku.is_turn():
                if get_encounter_id() == 337:
                    steal_new(target=21)
                else:
                    steal_new()
            else:
                escape_one()
    if game_vars.god_mode():
        rng_track.force_preempt()


@battle.utils.speedup_decorator
def cave_charge_rikku():
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Rikku.is_turn():
                CurrentPlayer().attack()
            else:
                escape_one()
                
    if memory.main.game_over():
        return
    wrap_up()


def gagazet_cave(direction):
    screen.await_turn()
    if memory.main.battle_type() == 2:
        escape_one()
    else:
        attack(direction)
    flee_all()

def use_item(slot: int, direction="none", target=None, rikku_flee=False):
    logger.debug("Using items via the Use command")
    logger.debug(f"Item slot: {slot}")
    logger.debug(f"Direction: {direction}")

    while not memory.main.main_battle_menu():
        pass
    logger.debug("Mark 1, turn is active.")
    move_count = 0
    while memory.main.battle_menu_cursor() != 20:
        #if not Rikku.is_turn() and not Kimahri.is_turn():
        #    return 
        logger.debug(f"Menu ID: {memory.main.battle_menu_cursor()}")
        if memory.main.battle_menu_cursor() in [0, 19, 23]:
            xbox.tap_down()
        elif memory.main.battle_menu_cursor() == 1:
            xbox.tap_up()
        elif memory.main.battle_menu_cursor() > 20:
            xbox.tap_up()
        else:
            xbox.tap_down()
        move_count += 1
        if move_count > 10:
            CurrentPlayer().defend()
            return
    if game_vars.use_pause():
        memory.main.wait_frames(3)
    logger.debug("Mark 8")
    while memory.main.main_battle_menu():
        xbox.tap_b()
    logger.debug("Mark 9")
    if rikku_flee:
        logger.debug("Mark 2, selecting 'Use' command in position 2")
        _navigate_to_position(2)
    else:
        logger.debug("Mark 2, selecting 'Use' command in position 1")
        _navigate_to_position(1)
    if game_vars.use_pause():
        memory.main.wait_frames(3)
    while memory.main.other_battle_menu():
        xbox.menu_b()
    logger.debug("Mark 3, navigating to item slot")
    _navigate_to_position(slot, memory.main.battle_cursor_3)
    if game_vars.use_pause():
        memory.main.wait_frames(3)
    while memory.main.interior_battle_menu():
        xbox.tap_b()
    if target is not None:
        if target >= 20 and memory.main.get_enemy_current_hp()[target - 20] == 0:
            tap_targeting()
        elif target <= 20 and not target in memory.main.get_active_battle_formation():
            tap_targeting()
        elif target <= 20 and memory.main.get_battle_hp()[memory.main.get_battle_char_slot(target)] == 0:
            tap_targeting()
        else:
            last_line = memory.main.battle_line_target()
            desired_line = 0 if target <= 20 else 1
            orientation = 0
            try:
                while memory.main.battle_target_id() != target:
                    logger.debug("Targetting based on character number")
                    if orientation == 0:
                        if last_line == desired_line:
                            xbox.tap_right()
                        else:
                            xbox.tap_up()
                    else:
                        if last_line == desired_line:
                            xbox.tap_up()
                        else:
                            xbox.tap_right()
                    memory.main.wait_frames(2)
                    if last_line != battle_line_target():
                        orientation = (orientation + 1) %2
                    last_line = memory.main.battle_line_target()
                tap_targeting()
            except Exception:
                xbox.tap_b()
                xbox.tap_b()
                xbox.tap_b()
                xbox.tap_b()
                xbox.tap_b()
                xbox.tap_b()
    elif direction == "none":
        logger.debug("No direction variation")
        tap_targeting()
    else:
        logger.debug(f"Direction variation: {direction}")
        if direction == "left":
            xbox.tap_left()
        elif direction == "right":
            xbox.tap_right()
        elif direction == "up":
            xbox.tap_up()
        elif direction == "down":
            xbox.tap_down()
        tap_targeting()


def use_item_tidus(slot: int, direction="none", target=255):
    logger.debug("Using items via the Use command")
    logger.debug(f"Item slot: {slot}")
    logger.debug(f"Direction: {direction}")
    while not memory.main.main_battle_menu():
        pass
    logger.debug("Mark 1")
    while memory.main.battle_menu_cursor() != 20:
        if not Tidus.is_turn():
            return
        if memory.main.battle_menu_cursor() == 1:
            xbox.tap_up()
        elif memory.main.battle_menu_cursor() > 20:
            xbox.tap_up()
        else:
            xbox.tap_down()
    if game_vars.use_pause():
        memory.main.wait_frames(3)
    while memory.main.main_battle_menu():
        xbox.tap_b()
    if game_vars.use_pause():
        memory.main.wait_frames(3)
    logger.debug("Mark 2")
    _navigate_to_position(2)
    while memory.main.other_battle_menu():
        xbox.tap_b()
    if game_vars.use_pause():
        memory.main.wait_frames(3)
    logger.debug("Mark 3")
    _navigate_to_position(slot, memory.main.battle_cursor_3)
    if game_vars.use_pause():
        memory.main.wait_frames(3)
    while memory.main.interior_battle_menu():
        xbox.tap_b()
    if target != 255:
        try:
            logger.debug("Targetting based on character number")
            if target >= 20 and memory.main.get_enemy_current_hp()[target - 20] != 0:
                direction = "l"
                while memory.main.battle_target_id() != target:
                    if memory.main.battle_target_id() < 20:
                        xbox.tap_right()
                        direction = "u"
                    elif direction == "u":
                        xbox.tap_up()
                    else:
                        xbox.tap_left()
            elif target < 20 and target != 0:
                direction = "l"
                while memory.main.battle_target_id() != target:
                    if memory.main.battle_target_id() >= 20:
                        xbox.tap_right()
                        direction = "u"
                    elif direction == "u":
                        xbox.tap_up()
                    else:
                        xbox.tap_left()
            elif target == 0:
                direction = "l"
                while memory.main.battle_target_id() != 0:
                    if memory.main.battle_target_id() >= 20:
                        xbox.tap_right()
                        direction = "u"
                    elif direction == "u":
                        xbox.tap_up()
                    else:
                        xbox.tap_left()

            tap_targeting()
        except Exception:
            xbox.tap_b()
            xbox.tap_b()
            xbox.tap_b()
            xbox.tap_b()
            xbox.tap_b()
            xbox.tap_b()
    elif direction == "none":
        logger.debug("No direction variation")
        tap_targeting()
    else:
        logger.debug(f"Direction variation: {direction}")
        if direction == "left":
            xbox.tap_left()
        elif direction == "right":
            xbox.tap_right()
        elif direction == "up":
            xbox.tap_up()
        elif direction == "down":
            xbox.tap_down()
        tap_targeting()


def cheer():
    logger.debug("Cheer command")
    while memory.main.battle_menu_cursor() != 20:
        if not Tidus.is_turn():
            return
        if memory.main.battle_menu_cursor() == 0:
            xbox.tap_down()
        else:
            xbox.tap_up()
    while not memory.main.other_battle_menu():
        xbox.tap_b()
    _navigate_to_position(1)
    while memory.main.other_battle_menu():
        xbox.tap_b()
    tap_targeting()


def seymour_spell(target_face=True):
    logger.debug("Seymour casting tier 2 spell")
    num = 21  # Should be the enemy number for the head
    if not memory.main.turn_ready():
        logger.debug("Battle menu isn't up.")
        screen.await_turn()

    while memory.main.battle_menu_cursor() != 21:
        logger.debug(f"Battle menu cursor: {memory.main.battle_menu_cursor()}")
        if memory.main.battle_menu_cursor() == 0:
            xbox.tap_down()
        else:
            xbox.tap_up()
    while memory.main.main_battle_menu():
        xbox.tap_b()  # Black magic
    logger.debug(f"Battle cursor 2: {memory.main.battle_cursor_2()}")
    _navigate_to_position(5)
    while memory.main.other_battle_menu():
        xbox.tap_b()

    if (
        target_face and memory.main.get_enemy_current_hp()[1] != 0
    ):  # Target head if alive.
        while memory.main.battle_target_id() != num:
            xbox.tap_left()

    tap_targeting()


def _use_healing_item(num=None, direction="l", item_id=0):
    logger.debug(f"Healing character, {num}")
    direction = direction.lower()
    if not memory.main.turn_ready():
        logger.debug("Battle menu isn't up.")
        return
    while not memory.main.main_battle_menu():
        pass
    while memory.main.battle_menu_cursor() != 1:
        xbox.tap_down()
    while memory.main.main_battle_menu():
        xbox.tap_b()
    while not memory.main.other_battle_menu():
        pass
    logger.debug(f"Battle cursor 2: {memory.main.battle_cursor_2()}")
    logger.debug(
        f"get_throw_items_slot({item_id}): {memory.main.get_throw_items_slot(item_id)}"
    )
    _navigate_to_position(memory.main.get_throw_items_slot(item_id))
    while memory.main.other_battle_menu():
        xbox.tap_b()
    if num is not None:
        while memory.main.battle_target_id() != num:
            if direction == "l":
                if memory.main.battle_target_id() >= 20:
                    logger.debug("Wrong battle line targeted.")
                    xbox.tap_right()
                    direction = "u"
                else:
                    xbox.tap_left()
            elif direction == "r":
                if memory.main.battle_target_id() >= 20:
                    logger.debug("Wrong character targeted.")
                    xbox.tap_left()
                    direction = "d"
                else:
                    xbox.tap_right()
            elif direction == "u":
                if memory.main.battle_target_id() >= 20:
                    logger.debug("Wrong character targeted.")
                    xbox.tap_down()
                    direction = "l"
                else:
                    xbox.tap_up()
            elif direction == "d":
                if memory.main.battle_target_id() >= 20:
                    logger.debug("Wrong character targeted.")
                    xbox.tap_up()
                    direction = "r"
                else:
                    xbox.tap_down()
    tap_targeting()


def use_potion_character(num, direction):
    logger.debug(f"Healing character, {num}")
    _use_healing_item(num=num, direction=direction, item_id=0)


def use_hi_potion_character(num, direction):
    # Check for hi-potions
    pot_check = memory.main.get_item_slot(1) < 50
    if pot_check:
        pot_type = 1
        logger.debug(f"Hi-Pot character, {num}")
    else:
        pot_type = 0
        logger.debug(f"Potion character, {num}")
    _use_healing_item(num=num, direction=direction, item_id=pot_type)


def oblitz_rng_wait():
    rng_values = rng_track.oblitz_history()
    logger.debug(f"rng_values: {rng_values}")
    last_rng = memory.main.rng_from_index(index=2)
    coming_seeds = memory.main.rng_array_from_index(index=2, array_len=8)
    seed_num = str(memory.main.rng_seed())
    logger.debug(f"coming_seeds: {coming_seeds}")
    pos = 0

    if seed_num not in rng_values:
        logger.debug(f"No values for this RNG seed - {memory.main.rng_seed()}")
        first_result = [coming_seeds[1], 10, True, 1]
        second_result = [coming_seeds[2], 20, True, 2]
    else:
        logger.debug("Scanning values for this RNG seed")
        if game_vars.loop_blitz():  # This will cause us to prefer results hunting
            logger.debug("Looping on blitz, we will try a new value.")
            # Seed value, time to completion, Win/Loss, and position
            first_result = [coming_seeds[1], 9999, True, 0]
            second_result = [coming_seeds[2], 9999, True, 0]
        else:  # For full runs, take the best result.
            logger.debug("This is a full run. Selecting best known result.")
            first_result = [coming_seeds[1], 9999, False, 0]
            second_result = [coming_seeds[2], 9999, False, 0]
        for i in range(len(coming_seeds)):
            # logger.debug(f"Checking seed {coming_seeds[i]}")
            # Set up duration and victory values
            if str(coming_seeds[i]) in rng_values[seed_num]:
                duration = (
                    int(rng_values[seed_num][str(coming_seeds[i])]["duration"]) + pos
                )
                # logger.debug(duration)
                victory = bool(rng_values[seed_num][str(coming_seeds[i])]["victory"])
                logger.debug(
                    f"Known result: {[coming_seeds[i], duration, victory, pos]}"
                )
                # logger.debug(victory)
            elif game_vars.loop_blitz():
                duration = 1 + pos
                victory = True
                logger.debug(
                    "No result (preferred), loop. "
                    + f"{[coming_seeds[i], duration, victory, pos]}"
                )
            else:
                duration = 480 + pos
                # 460-480 is about the maximum duration we desire.
                victory = True
                logger.debug(
                    "No result (undesirable), full. "
                    + f"{[coming_seeds[i], duration, victory, pos]}"
                )
            # Fill as first two RNG values,
            # then test against previously set RNG values until we've exhausted tests.
            if i == 0:
                pass
            elif first_result[2] and not second_result[2]:
                if duration < second_result[1] and victory:
                    second_result = [coming_seeds[i], duration, victory, pos]
                    # logger.debug(f"Better Result for Second: {pos} - A")
                else:
                    # logger.debug(f"Result for {pos} is not as good. - A")
                    pass
            elif second_result[2] and not first_result[2]:
                if duration < first_result[1] and victory:
                    first_result = [coming_seeds[i], duration, victory, pos]
                    # logger.debug(f"Better Result for First: {pos} - B")
                else:
                    # logger.debug(f"Result for {pos} is not as good. - B")
                    pass
            elif second_result[1] < first_result[1]:
                if duration < second_result[1] and victory:
                    second_result = [coming_seeds[i], duration, victory, pos]
                    # logger.debug(f"Better Result for Second: {pos} - C")
                else:
                    # logger.debug(f"Result for {pos} is not as good. - C")
                    pass
            else:
                if duration < first_result[1] and victory:
                    first_result = [coming_seeds[i], duration, victory, pos]
                    # logger.debug(f"Better Result for First: {pos} - D")
                else:
                    # logger.debug(f"Result for {pos} is not as good. - D")
                    pass
            pos += 1
    if first_result[1] <= second_result[1]:
        best = first_result
    else:
        best = second_result
    logs.write_stats("Chosen Blitzball result:")
    logs.write_stats(best)

    next_rng = last_rng
    j = 0
    logger.debug("Chosen results (RNG, duration, victory, waits):")
    logger.debug(best)
    # Now wait for one of the two results to come up
    while next_rng != best[0] and j < 15:
        next_rng = memory.main.rng_from_index(index=2) & 0x7FFFFFFF
        if last_rng != next_rng:
            logger.debug(
                f"{j} | {s32(next_rng)} | "
                + f"{s32(memory.main.rng_from_index(index=2))} | {s32(best[0])}"
            )
            j += 1
            last_rng = next_rng
    logger.debug(f"Success. Attacking. {j} | {next_rng}")
    game_vars.set_oblitz_rng(value=next_rng)
    return next_rng


def attack_oblitz_end():
    logger.debug("Attack")
    if not memory.main.turn_ready():
        while not memory.main.turn_ready():
            pass
    while memory.main.main_battle_menu():
        if memory.main.battle_menu_cursor() not in [0, 203, 210, 216]:
            logger.debug(f"Battle Menu Cursor: {memory.main.battle_menu_cursor()}")
            xbox.tap_up()
        elif not memory.main.battle_active():
            return
        else:
            xbox.menu_b()
    memory.main.wait_frames(1)
    oblitz_rng_wait()
    xbox.tap_b()
    xbox.tap_b()
    # logs.write_stats("RNG02 on attack:")
    # logs.write_stats(memory.s32(rng_wait_results))


def attack(direction="none"):
    logger.debug("Attack")
    direction = direction.lower()
    if not memory.main.turn_ready():
        while not memory.main.turn_ready():
            pass
    while memory.main.main_battle_menu():
        if memory.main.battle_menu_cursor() not in [0, 203, 210, 216]:
            logger.debug(f"Battle Menu Cursor: {memory.main.battle_menu_cursor()}")
            xbox.tap_up()
        elif not memory.main.battle_active():
            return
        else:
            xbox.tap_b()
    if direction == "left":
        xbox.tap_left()
    if direction == "right":
        xbox.tap_right()
    if direction == "r2":
        xbox.tap_right()
        xbox.tap_right()
    if direction == "r3":
        xbox.tap_right()
        xbox.tap_right()
        xbox.tap_right()
    if direction == "up":
        xbox.tap_up()
    if direction == "down":
        xbox.tap_down()
    tap_targeting()


def steal_target(index):
    if index < 20:
        # This makes it automatically target enemy 0, 1, 2 
        # or 20, 21, 22 which are the same command.
        index += 20
    while not Kimahri.is_turn() and not Rikku.is_turn():
        if not Kimahri.active():
            logger.debug("Steal_target function, swapping in Kimahri")
            buddy_swap(Kimahri)
        elif not Rikku.active():
            logger.debug("Steal_target function, swapping in Rikku")
            buddy_swap(Rikku)
        else:
            logger.warning("Steal_target function ERROR - cannot swap.")
            CurrentPlayer().defend()

    while memory.main.battle_menu_cursor() != 20:
        if Rikku.is_turn():
            Rikku.navigate_to_battle_menu(20)
        elif Kimahri.is_turn():
            Kimahri.navigate_to_battle_menu(20)
        else:
            return
    while not memory.main.other_battle_menu():
        xbox.tap_confirm()
    _navigate_to_position(0)
    logger.debug(f"Other battle menu: {memory.main.other_battle_menu()}")
    while memory.main.other_battle_menu():
        xbox.tap_confirm()  # Lock in the Steal
    logger.debug(f"Other battle menu: {memory.main.other_battle_menu()}")
    
    # Target the appropriate enemy.
    direction = "l"
    retry = 0
    if memory.main.get_enemy_current_hp()[index - 20] != 0:
        # Only steal from living targets.
        while memory.main.battle_target_id() != index:
            while memory.main.battle_target_id() != index:
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

    tap_targeting()


def quick_hit(target:int = 20):
    CurrentPlayer().quick_hit(target=target)

    # Obsoleted logic.
    '''
    logger.debug("Quick Hit function")
    if not memory.main.main_battle_menu():
        while not memory.main.main_battle_menu():
            pass
    actor = CurrentPlayer().raw_id()
    skill_menu = memory.unlocks.get_unlocked_abilities_by_type(actor)['Skill']
    # logger.warning(special_menu)
    ability_position = None
    for ability in skill_menu:
        if ability['name'] == 'Quick Hit':
            ability_position = ability['position']
    if ability_position is None:
        logger.warning("This character does not know Quick Hit!")
        CurrentPlayer().attack()
        return
    while memory.main.battle_menu_cursor() != 19:
        CurrentPlayer().navigate_to_battle_menu(19)
    while not memory.main.other_battle_menu():
        xbox.tap_b()
    _navigate_to_position(ability_position)
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

    tap_targeting()
    '''


def bribe(target:int = 20, spare_change_value:int = 10000):
    logger.debug("Bribe function")
    if not memory.main.main_battle_menu():
        while not memory.main.main_battle_menu():
            pass
    actor = CurrentPlayer().raw_id()
    special_menu = memory.unlocks.get_unlocked_abilities_by_type(actor)['Special']
    # logger.warning(special_menu)
    ability_position = None
    for ability in special_menu:
        if ability['name'] == 'Bribe':
            ability_position = ability['position']
    if ability_position is None:
        logger.warning("This character does not know Bribe!")
        CurrentPlayer().defend()
        return
    while memory.main.battle_menu_cursor() != 20:
        CurrentPlayer().navigate_to_battle_menu(20)
    while not memory.main.other_battle_menu():
        xbox.tap_b()
    _navigate_to_position(ability_position)
    logger.debug(f"Other battle menu: {memory.main.other_battle_menu()}")
    while memory.main.other_battle_menu():
        xbox.tap_b()  # Use the command
        
    calculate_spare_change_movement(spare_change_value)

    while memory.main.spare_change_open():
        xbox.tap_b()
        
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

    tap_targeting()


def entrust(target:int = 4):
    logger.debug("Entrust function")
    if not memory.main.main_battle_menu():
        while not memory.main.main_battle_menu():
            pass
    actor = CurrentPlayer().raw_id()
    special_menu = memory.unlocks.get_unlocked_abilities_by_type(actor)['Special']
    # logger.warning(special_menu)
    ability_position = None
    for ability in special_menu:
        if ability['name'] == 'Entrust':
            ability_position = ability['position']
    if ability_position is None:
        logger.warning("This character does not know Entrust!")
        CurrentPlayer().defend()
        return
    while memory.main.battle_menu_cursor() != 20:
        CurrentPlayer().navigate_to_battle_menu(20)
    while not memory.main.other_battle_menu():
        xbox.tap_b()
    _navigate_to_position(ability_position)
    logger.debug(f"Other battle menu: {memory.main.other_battle_menu()}")
    while memory.main.other_battle_menu():
        xbox.tap_b()  # Use the command

    # Target the appropriate enemy.
    direction = "l"
    retry = 0
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

    tap_targeting()


def provoke(target:int = 20):
    CurrentPlayer().provoke(target=target)
#     logger.debug("Provoke function")
#     if not memory.main.main_battle_menu():
#         while not memory.main.main_battle_menu():
#             pass
#     actor = CurrentPlayer().raw_id()
#     special_menu = memory.unlocks.get_unlocked_abilities_by_type(actor)['Special']
#     # logger.warning(special_menu)
#     ability_position = None
#     for ability in special_menu:
#         if ability['name'] == 'Provoke':
#             ability_position = ability['position']
#     if ability_position is None:
#         logger.warning("This character does not know Provoke!")
#         CurrentPlayer().defend()
#         return
#     while memory.main.battle_menu_cursor() != 20:
#         CurrentPlayer().navigate_to_battle_menu(20)
#     while not memory.main.other_battle_menu():
#         xbox.tap_b()
#     _navigate_to_position(ability_position)
#     logger.debug(f"Other battle menu: {memory.main.other_battle_menu()}")
#     while memory.main.other_battle_menu():
#         xbox.tap_b()  # Use the command
        
#     # Target the appropriate enemy.
#     direction = "l"
#     retry = 0
#     if memory.main.get_enemy_current_hp()[target - 20] != 0:
#         # Only attack
#         while memory.main.battle_target_id() != target:
#             while memory.main.battle_target_id() != target:
#                 if direction == "l":
#                     if retry > 5:
#                         retry = 0
#                         logger.debug("Wrong battle line targeted.")
#                         xbox.tap_right()
#                         direction = "u"
#                         retry = 0
#                     else:
#                         xbox.tap_left()
#                 elif direction == "r":
#                     if retry > 5:
#                         retry = 0
#                         logger.debug("Wrong character targeted.")
#                         xbox.tap_left()
#                         direction = "d"
#                     else:
#                         xbox.tap_right()
#                 elif direction == "u":
#                     if retry > 5:
#                         retry = 0
#                         logger.debug("Wrong character targeted.")
#                         xbox.tap_down()
#                         direction = "l"
#                     else:
#                         xbox.tap_up()
#                 elif direction == "d":
#                     if retry > 5:
#                         retry = 0
#                         logger.debug("Wrong character targeted.")
#                         xbox.tap_up()
#                         direction = "r"
#                     else:
#                         xbox.tap_down()
#                 retry += 1
#             memory.main.wait_frames(1)

#     tap_targeting()


def dispel(target:int = 20):
    logger.debug("Dispel function")
    if CurrentPlayer().mp() < 12:
        CurrentPlayer().defend()
        return
    if not memory.main.main_battle_menu():
        while not memory.main.main_battle_menu():
            pass
    actor = CurrentPlayer().raw_id()
    white_mag_menu = memory.unlocks.get_unlocked_abilities_by_type(actor)['White Magic']
    # logger.warning(special_menu)
    ability_position = None
    for ability in white_mag_menu:
        if ability['name'] == 'Dispel':
            ability_position = ability['position']
    if ability_position is None:
        logger.warning("This character does not know Dispel!")
        CurrentPlayer().defend()
        return
    logger.debug(f"Confirmed Dispel is in position {ability_position}")
    while memory.main.battle_menu_cursor() != 22:
        logger.debug(f"Mark 0: {memory.main.battle_menu_cursor()}")
        CurrentPlayer().navigate_to_battle_menu(22)
    logger.debug("Mark 1")
    while not memory.main.other_battle_menu():
        xbox.tap_b()
    logger.debug("Mark 2")
    _navigate_to_position(ability_position)
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

    tap_targeting()


def auto_life(target:int=0):
    logger.debug("Auto-Life function")
    if not memory.main.main_battle_menu():
        while not memory.main.main_battle_menu():
            if memory.main.game_over():
                return
    actor = CurrentPlayer().raw_id()
    white_mag_menu = memory.unlocks.get_unlocked_abilities_by_type(actor)['White Magic']
    # logger.warning(special_menu)
    ability_position = None
    for ability in white_mag_menu:
        if ability['name'] == 'Auto-Life':
            ability_position = ability['position']
    if ability_position is None:
        logger.warning("This character does not know Auto-Life!")
        CurrentPlayer().defend()
        return
    while memory.main.battle_menu_cursor() != 22:
        CurrentPlayer().navigate_to_battle_menu(22)
    while not memory.main.other_battle_menu():
        xbox.tap_b()
    _navigate_to_position(ability_position)
    logger.debug(f"Other battle menu: {memory.main.other_battle_menu()}")
    while memory.main.other_battle_menu():
        xbox.tap_b()  # Use the command
        
    # Target the appropriate ally.
    direction = "l"
    retry = 0
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

    tap_targeting()


def nulblaze():
    logger.debug("NulBlaze function")
    if not memory.main.main_battle_menu():
        while not memory.main.main_battle_menu():
            pass
    actor = CurrentPlayer().raw_id()
    white_mag_menu = memory.unlocks.get_unlocked_abilities_by_type(actor)['White Magic']
    # logger.warning(special_menu)
    ability_position = None
    for ability in white_mag_menu:
        if ability['name'] == 'NulBlaze':
            ability_position = ability['position']
    if ability_position is None:
        logger.warning("This character does not know NulBlaze!")
        CurrentPlayer().defend()
        return
    while memory.main.battle_menu_cursor() != 22:
        CurrentPlayer().navigate_to_battle_menu(22)
    while not memory.main.other_battle_menu():
        xbox.tap_b()
    _navigate_to_position(ability_position)
    logger.debug(f"Other battle menu: {memory.main.other_battle_menu()}")
    while memory.main.other_battle_menu():
        xbox.tap_b()  # Use the command
    
    tap_targeting()


def aim():
    logger.debug("Aim function")
    if not memory.main.main_battle_menu():
        while not memory.main.main_battle_menu():
            pass
    actor = CurrentPlayer().raw_id()
    special_menu = memory.unlocks.get_unlocked_abilities_by_type(actor)['Special']
    ability_position = None
    for ability in special_menu:
        if ability['name'] == 'Aim':
            ability_position = ability['position']
    if ability_position is None:
        logger.warning("This character does not know Aim!")
        CurrentPlayer().defend()
        return
    while memory.main.battle_menu_cursor() != 20:
        CurrentPlayer().navigate_to_battle_menu(20)
    while not memory.main.other_battle_menu():
        xbox.tap_b()
    _navigate_to_position(ability_position)
    logger.debug(f"Other battle menu: {memory.main.other_battle_menu()}")
    while memory.main.other_battle_menu():
        xbox.tap_b()  # Use the command
    
    tap_targeting()


def _steal(direction=None, steal_position=0,target:int=20):
    if not memory.main.main_battle_menu():
        while not memory.main.main_battle_menu():
            pass
    while memory.main.battle_menu_cursor() != 20:
        CurrentPlayer().navigate_to_battle_menu(20)
        '''
        if Rikku.is_turn():
            Rikku.navigate_to_battle_menu(20)
        elif Kimahri.is_turn():
            Kimahri.navigate_to_battle_menu(20)
        else:
            return
        '''
    while not memory.main.other_battle_menu():
        xbox.tap_b()
    _navigate_to_position(steal_position)
    logger.debug(f"Other battle menu: {memory.main.other_battle_menu()}")
    while memory.main.other_battle_menu():
        xbox.tap_b()  # Use the Steal
    logger.debug(f"Other battle menu: {memory.main.other_battle_menu()}")
    if direction == "down":
        xbox.tap_down()
    elif direction == "up":
        xbox.tap_up()
    elif direction == "right":
        xbox.tap_right()
    elif direction == "left":
        xbox.tap_left()
    elif target != 20:
        direction = 'l'
        if memory.main.get_enemy_current_hp()[target - 20] != 0:
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
    logger.debug("Firing steal")
    tap_targeting()


def steal_new(actor:int=None,target=20):
    if actor is None:
        actor = CurrentPlayer().raw_id()
    logger.debug("Steal (new)")
    special_menu = memory.unlocks.get_unlocked_abilities_by_type(actor)['Special']
    # logger.warning(special_menu)
    steal_position = None
    for ability in special_menu:
        if ability['name'] == 'Steal':
            steal_position = ability['position']
    if steal_position is None:
        logger.warning("This character does not know Steal!")
        CurrentPlayer().defend()
        return
    logger.warning(f"Steal command in position {steal_position}")
    if get_encounter_id() in [273, 281]:
        _steal("left", steal_position=steal_position)
    elif get_encounter_id() in [276, 279, 289]:
        _steal("up", steal_position=steal_position)
    else:
        _steal(steal_position=steal_position, target=target)

def shadow_gem_farm():
    screen.await_turn()
    steal_count = 0
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if steal_count < 10:
                steal_new(CurrentPlayer().raw_id())
                steal_count += 1
            else:
                flee_all()
    wrap_up()

def use_item_new(item:int, target:int|None=None):
    actor = CurrentPlayer().raw_id()
    # If a single target is designated, throw the item at that target.
    # Otherwise it will ignore this step and just push through.
    item_slot = memory.main.get_use_items_slot(item)
    logger.debug(f"Use (new), item slot {item_slot}")
    if item_slot > 200:
        logger.warning(f"We are out of that item! Fall back to defend command!")
        CurrentPlayer().defend()
        return
    special_menu = memory.unlocks.get_unlocked_abilities_by_type(actor)['Special']
    # logger.warning(special_menu)
    ability_position = None
    for ability in special_menu:
        if ability['name'] == 'Use':
            ability_position = ability['position']
    if ability_position is None:
        logger.warning("This character does not know Use!")
        CurrentPlayer().defend()
        return
    logger.debug("Selecting 'Special' command")
    
    # Navigate to Special command
    move_count = 0  # Used to escape infinite loop if needed.
    while memory.main.battle_menu_cursor() != 20:
        while memory.main.battle_menu_cursor() != 20:
            #if not Rikku.is_turn() and not Kimahri.is_turn():
            #    return 
            logger.debug(f"Menu ID: {memory.main.battle_menu_cursor()}")
            if memory.main.battle_menu_cursor() in [0, 19, 23]:
                xbox.tap_down()
            elif memory.main.battle_menu_cursor() == 1:
                xbox.tap_up()
            elif memory.main.battle_menu_cursor() > 20:
                xbox.tap_up()
            else:
                xbox.tap_down()
            move_count += 1
            if move_count > 10:
                CurrentPlayer().defend()
                return
        memory.main.wait_frames(1)
    while memory.main.main_battle_menu():
        xbox.tap_b()
    logger.debug("Selecting 'Use' command")

    # Navigate to 'Use' command on interior menu
    logger.warning(f"Use command in position {ability_position}")
    _navigate_to_position(ability_position)
    logger.debug(f"Other battle menu: {memory.main.other_battle_menu()}")
    while memory.main.other_battle_menu():
        xbox.menu_b()
    
    # Target the item to be used
    _navigate_to_position(item_slot, memory.main.battle_cursor_3)
    while memory.main.interior_battle_menu():
        xbox.menu_b()
    
    # Only attack
    if target is not None:
        xbox.tap_up()  # For testing
        # memory.main.wait_frames(2)
        last_line = memory.main.enemy_targetted()
        desired_line = 0 if target <= 20 else 1
        orientation = 0
        logger.warning(f"Tar: {memory.main.battle_target_id()}/{target}")
        logger.warning(f"Line: {last_line}/{desired_line} ({orientation})")
        while memory.main.battle_target_id() != target:
            try:
                logger.debug("Targetting based on character number")
                if orientation == 0:
                    if last_line == desired_line:
                        xbox.tap_right()
                    else:
                        xbox.tap_up()
                else:
                    if last_line == desired_line:
                        xbox.tap_up()
                    else:
                        xbox.tap_right()
                # memory.main.wait_frames(2)
                if (
                    last_line == memory.main.enemy_targetted() and 
                    last_line != desired_line
                ):
                    logger.warning(f"Orientation swap: {last_line},{memory.main.enemy_targetted()},{desired_line}")
                    orientation = (orientation + 1) %2
                    # memory.main.wait_frames(60)
                last_line = memory.main.enemy_targetted()
                logger.warning(f"Tar: {memory.main.battle_target_id()}/{target}")
                logger.warning(f"Line: {last_line}/{desired_line} ({orientation})")
            except Exception as e:
                logger.error(f"Error: {e}")

    tap_targeting()
    


def steal(steal_position=0):
    if memory.main.rikku_learned_flee() and steal_position == 0:
        steal_position = 1
    logger.debug("Steal")
    if get_encounter_id() in [273, 281]:
        _steal("left")
    elif get_encounter_id() in [276, 279, 289]:
        _steal("up")
    else:
        _steal(steal_position=steal_position)


def steal_down():
    logger.debug("Steal Down")
    _steal("down")


def steal_up():
    logger.debug("Steal Up")
    _steal("up")


def steal_right():
    logger.debug("Steal Right")
    _steal("right")


def steal_left():
    logger.debug("Steal Left")
    _steal("left")


def chain_encounter(strat: int, enemy_formation: int):

    tidus_turn = 0
    rikku_turn = 0

    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Tidus.is_turn():
                tidus_turn += 1

                if strat == 0:

                    Tidus.attack()

                elif strat == 1:

                    if enemy_formation == 0:

                        Tidus.attack(target_id=21, direction_hint="l")

                    else:

                        Tidus.attack()

                elif strat == 2:

                    Tidus.attack()

            if Rikku.is_turn():
                rikku_turn += 1

                if strat == 0:

                    Rikku.attack()

                elif strat == 1:

                    if rikku_turn == 1:

                        steal()

                    else:

                        Rikku.attack()

                elif strat == 2:

                    steal()

    return


def ruins_encounter(strat: int):

    tidus_turn = 0
    rikku_turn = 0

    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Tidus.is_turn():
                Tidus.attack()

            if Rikku.is_turn():
                rikku_turn += 1

                # Rikku Attack > Tidus Attack > Rikku Attack > Tidus Attack
                if strat == 0:

                    Rikku.attack()

                # Rikku Attack > Tidus Attack > Rikku Steal > Tidus Attack > Rikku Attack
                elif strat == 1:

                    if rikku_turn == 2:

                        steal()

                    else:

                        Rikku.attack()

                # Rikku Attack > Tidus Attack > Rikku Steal > Tidus Attack > Rikku Defend > Tidus Attack
                elif strat == 2:

                    if rikku_turn == 1:

                        Rikku.attack()

                    elif rikku_turn == 2:

                        steal()

                    else:

                        Rikku.defend()

                # Rikku Steal > Tidus Attack > Rikku Steal > Tidus Attack > Rikku Attack > Tidus Attack
                elif strat == 3:

                    if rikku_turn == 1:

                        steal()

                    elif rikku_turn == 2:

                        steal_up()

                    else:

                        Rikku.attack()
    wrap_up()
    return


def steal_and_attack():
    logger.debug("Steal/Attack function")
    FFXC.set_neutral()
    screen.await_turn()
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Rikku.is_turn():
                grenade_slot = memory.main.get_item_slot(35)
                grenade_count = memory.main.get_item_count_slot(grenade_slot)
                if grenade_count < 5:
                    steal()
                else:
                    CurrentPlayer().attack()
            if Tidus.is_turn():
                CurrentPlayer().attack()
        elif memory.main.other_battle_menu():
            xbox.tap_b()
    memory.main.click_to_control()

@battle.utils.speedup_decorator
def steal_and_attack_pre_tros():
    logger.debug("Steal/Attack function before Tros")
    turn_counter = 0
    advances = get_advances(tros=False)
    FFXC.set_neutral()
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Rikku.is_turn():
                turn_counter += 1
                if turn_counter == 1:
                    grenade_slot = memory.main.get_item_slot(35)
                    grenade_count = memory.main.get_item_count_slot(grenade_slot)
                    if grenade_count < 5:
                        steal()
                    elif advances in [1, 2]:
                        steal()
                        advances = get_advances(tros=False)
                    else:
                        CurrentPlayer().attack()
                elif turn_counter == 2:
                    grenade_slot = memory.main.get_item_slot(35)
                    grenade_count = memory.main.get_item_count_slot(grenade_slot)
                    if grenade_count < 6:
                        steal()
                    elif advances in [1, 2]:
                        steal()
                        advances = get_advances(tros=False)
                    else:
                        CurrentPlayer().attack()
                else:
                    CurrentPlayer().attack()
            if Tidus.is_turn():
                CurrentPlayer().attack()
        elif memory.main.other_battle_menu():
            xbox.tap_b()
    memory.main.click_to_control()


# move to battle.aeon
def aeon_summon(position):
    logger.debug(f"Summoning Aeon {position}")
    backup = 0
    while not memory.main.main_battle_menu():
        pass
    while memory.main.battle_menu_cursor() != 23:
        if not Yuna.is_turn():
            return
        if memory.main.battle_menu_cursor() == 255:
            pass
        elif (
            memory.main.battle_menu_cursor() >= 1
            and memory.main.battle_menu_cursor() < 23
        ):
            xbox.tap_up()
        else:
            xbox.tap_down()
    while memory.main.main_battle_menu():
        xbox.tap_confirm()
    while position != memory.main.battle_cursor_2():
        logger.debug(f"Battle cursor 2: {memory.main.battle_cursor_2()}")
        if memory.main.battle_cursor_2() < position:
            xbox.tap_down()
        else:
            xbox.tap_up()
        backup += 1
        if backup > 20:
            position -= 1
    while memory.main.other_battle_menu():
        xbox.tap_confirm()

    with logging_redirect_tqdm():
        fmt = "Waiting for Aeon's turn... elapsed {elapsed}"
        with tqdm(bar_format=fmt) as pbar:
            while not memory.main.turn_ready():
                pbar.update()


def heal_up(chars=3, *, full_menu_close=True):
    logger.info(f"Menuing, healing characters: {chars}")
    if memory.main.get_yuna_mp() < 4:
        logger.debug(f"Yuna out of MP: {memory.main.get_yuna_mp()}")
        if full_menu_close:
            memory.main.close_menu()
        else:
            memory.main.back_to_main_menu()
        return
    if memory.main.get_hp() == memory.main.get_max_hp():
        logger.debug("No need to heal. Exiting menu.")
        logger.debug(memory.main.menu_number())
        if full_menu_close:
            memory.main.close_menu()
        else:
            if memory.main.menu_open():
                memory.main.back_to_main_menu()
        return
    if not memory.main.menu_open():
        memory.main.open_menu()
    FFXC.set_neutral()
    while memory.main.get_menu_cursor_pos() != 2:
        logger.debug(f"Selecting Ability command - {memory.main.get_menu_cursor_pos()}")
        memory.main.menu_direction(memory.main.get_menu_cursor_pos(), 2, 11)
    while memory.main.menu_number() == 5:
        logger.debug(f"Select Ability - {memory.main.menu_number()}")
        xbox.tap_b()
    logger.debug("Mark 1")
    target_pos = Yuna.main_menu_index()
    logger.debug(f"Target pos: {target_pos}")
    while memory.main.get_char_cursor_pos() != target_pos:
        memory.main.menu_direction(
            memory.main.get_char_cursor_pos(),
            target_pos,
            len(memory.main.get_order_seven()),
        )
    logger.debug("Mark 2")
    while memory.main.menu_number() != 26:
        if memory.main.get_menu_2_char_num() == 1:
            xbox.tap_b()
        else:
            xbox.tap_down()
    while not memory.main.heal_menu_open():
        xbox.tap_b()
    character_positions = {
        0: memory.main.get_char_formation_slot(0),  # Tidus
        1: memory.main.get_char_formation_slot(1),  # Yuna
        2: memory.main.get_char_formation_slot(2),  # Auron
        3: memory.main.get_char_formation_slot(3),  # Kimahri
        4: memory.main.get_char_formation_slot(4),  # Wakka
        5: memory.main.get_char_formation_slot(5),  # Lulu
        6: memory.main.get_char_formation_slot(6),  # Rikku
    }
    logger.debug(f"Character positions: {character_positions}")
    positions_to_characters = {
        val: key for key, val in character_positions.items() if val != 255
    }
    logger.debug(f"Positions to characters: {positions_to_characters}")
    maximal_hp = memory.main.get_max_hp()
    logger.debug(f"Max HP: {maximal_hp}")
    current_hp = memory.main.get_hp()
    for cur_position in range(len(positions_to_characters)):
        while (
            current_hp[positions_to_characters[cur_position]]
            < maximal_hp[positions_to_characters[cur_position]]
        ):
            logger.debug(f"Current hp: {current_hp} - Yuna MP: {memory.main.get_yuna_mp()}")
            while memory.main.assign_ability_to_equip_cursor() != cur_position and memory.main.get_yuna_mp() >= 4:
                if memory.main.assign_ability_to_equip_cursor() < cur_position:
                    xbox.tap_down()
                else:
                    xbox.tap_up()
            xbox.tap_b()
            current_hp = memory.main.get_hp()
            if current_hp == maximal_hp or memory.main.get_yuna_mp() < 4:
                break
    logger.debug("Healing complete. Exiting menu.")
    logger.debug(memory.main.menu_number())
    if full_menu_close:
        memory.main.close_menu()
    else:
        memory.main.back_to_main_menu()


# Heal methods
# 1 = Heal with items
# 2 = Heal with cure

# Heal Items
# 0 = Potion
# 1 = Hi-Potion
# 2 = X-Potion
# 3 = Mega-Potion
# 8 = Elixir
# 9 = Megalixir

def heal_up_2(*chars, heal_method: int = 1, item_index: int = 0, single_item: bool = False, full_menu_close=True):
    logger.info(f"Menuing, healing characters: {chars}")

    if not heal_method in [1, 2]:
        logger.debug("Invalid heal method selected. Value of 1 or 2 is expected. Please review code.")

    # Check if healing is needed for each character
    healing_necessary = False
    for char in chars:
        if memory.main.get_hp() == memory.main.get_max_hp():
            logger.debug(f"{char} has full HP")
        else:
            healing_necessary = True

    # If we're not on the main menu return to or open the main menu
    memory.main.back_to_main_menu()

    FFXC.set_neutral()

    main_menu_target_pos = heal_method

    # Move to position in main menu for Items / Abilities
    while memory.main.get_menu_cursor_pos() != main_menu_target_pos:
        logger.debug(f"Selecting Ability command - {memory.main.get_menu_cursor_pos()}")
        memory.main.menu_direction(memory.main.get_menu_cursor_pos(), target_menu_position=main_menu_target_pos, menu_size=11)

    # Select the menu option
    while memory.main.menu_number() == 5:
        logger.debug(f"Select Ability - {memory.main.menu_number()}")
        xbox.tap_b()
    logger.debug("Mark 1")

    if heal_method == 1:

        item_menu_position = memory.main.get_item_slot(item_num=item_index)
        item_menu_target_row = item_menu_position // 2
        item_menu_target_column = item_menu_position % 2

        item_menu_row, item_menu_column = memory.main.get_item_menu_cursor_pos()

        # Navigate to the target item in the menu
        while item_menu_row < item_menu_target_row:
            xbox.tap_down()
            item_menu_row, item_menu_column = memory.main.get_item_menu_cursor_pos()

        while item_menu_column < item_menu_target_column:
            xbox.tap_down()
            item_menu_row, item_menu_column = memory.main.get_item_menu_cursor_pos()

    else:

        yuna_menu_pos = Yuna.main_menu_index()
        logger.debug(f"Target pos: {yuna_menu_pos}")

        # Move to Yuna in the menu
        while memory.main.get_char_cursor_pos() != yuna_menu_pos:
            memory.main.menu_direction(
                memory.main.get_char_cursor_pos(),
                yuna_menu_pos,
                len(memory.main.get_order_seven()),
            )
        logger.debug("Mark 2")

    # Open heal menu
    while not memory.main.heal_menu_open():
        while not memory.main.heal_menu_open():
            xbox.tap_b()
        memory.main.wait_frames(1)

    # Get the character position for each character
    character_positions = {
        0: memory.main.get_char_formation_slot(0),  # Tidus
        1: memory.main.get_char_formation_slot(1),  # Yuna
        2: memory.main.get_char_formation_slot(2),  # Auron
        3: memory.main.get_char_formation_slot(3),  # Kimahri
        4: memory.main.get_char_formation_slot(4),  # Wakka
        5: memory.main.get_char_formation_slot(5),  # Lulu
        6: memory.main.get_char_formation_slot(6),  # Rikku
    }
    logger.debug(f"Character positions: {character_positions}")

    # Get the character that sits in each position
    positions_to_characters = {
        val: key for key, val in character_positions.items() if val != 255
    }
    logger.debug(f"Positions to characters: {positions_to_characters}")

    maximal_hp = memory.main.get_max_hp()
    logger.debug(f"Max HP: {maximal_hp}")
    current_hp = memory.main.get_hp()

    for cur_position in range(len(positions_to_characters)):
        character_index = positions_to_characters[cur_position]
        if character_index not in chars:
            continue
        else:
            logger.debug(f"Healing {character_index}")

        starting_hp = current_hp[character_index]

        while current_hp[character_index] < maximal_hp[character_index]:
            logger.debug(f"Current hp: {current_hp}")

            if heal_method == 1:
                while memory.main.item_heal_character_cursor() != cur_position:
                    if memory.main.item_heal_character_cursor() < cur_position:
                        xbox.tap_down()
                    else:
                        xbox.tap_up()
            else:
                while memory.main.assign_ability_to_equip_cursor() != cur_position:
                    if memory.main.assign_ability_to_equip_cursor() < cur_position:
                        xbox.tap_down()
                    else:
                        xbox.tap_up()
            xbox.tap_b()
            current_hp = memory.main.get_hp()
            if heal_method == 1 and memory.main.get_item_count_slot(item_menu_position) == 0:
                break
            if heal_method == 2 and memory.main.get_yuna_mp() < 4:
                break
            if heal_method == 1 and single_item and current_hp[character_index] > starting_hp:
                break
        if current_hp == maximal_hp:
            break
        if heal_method==1 and memory.main.get_item_count_slot(item_menu_position)==0:
            break
        if heal_method==2 and memory.main.get_yuna_mp() < 4:
            break
    logger.debug("Healing complete. Exiting menu.")
    logger.debug(memory.main.menu_number())

    if full_menu_close:
        memory.main.close_menu()
    else:
        memory.main.back_to_main_menu()


def lancet_swap(direction:str="none", target_id=20):
    logger.debug("Lancet Swap function")

    # Assumption is formation: Tidus, Wakka, Auron, Kimahri, and Yuna in last slot.
    direction = direction.lower()
    lancet_complete = False
    while not lancet_complete:
        if memory.main.game_over():
            return False
        if not Kimahri.active():
            buddy_swap(Kimahri)
        elif Kimahri.is_turn():
            # if target_id == 99:
            memory.main.kim_od_unlocks()
            CurrentPlayer().use_special_by_name(command_name="Lancet",direction=direction,target_id=target_id)
            memory.main.kim_od_unlocks()
                # lancet_target(target=20, direction='u')
            # else:
            #     memory.main.kim_od_unlocks()
            #     CurrentPlayer().use_special_by_name(command_name="Lancet",direction=direction,target_id=target_id)
            #     memory.main.kim_od_unlocks()
            #     lancet_target(target=target_id, direction='u')
            lancet_complete = True
        else:
            CurrentPlayer().defend()

    screen.await_turn()
    flee_all()
    wrap_up()
    return True


def lancet(direction):
    memory.main.kim_od_unlocks()
    CurrentPlayer().use_special_by_name(command_name="Lancet",direction=direction,target_id=20)
    memory.main.kim_od_unlocks()
    '''
    memory.main.kim_od_unlocks()
    logger.debug(f"Casting Lancet with variation: {direction}")
    while memory.main.battle_menu_cursor() != 20:
        if memory.main.battle_menu_cursor() == 255:
            pass
        elif memory.main.battle_menu_cursor() == 1:
            xbox.tap_up()
        elif memory.main.battle_menu_cursor() > 20:
            xbox.tap_up()
        else:
            xbox.tap_down()
    while memory.main.main_battle_menu():
        xbox.tap_b()
    _navigate_to_position(0)
    while memory.main.other_battle_menu():
        xbox.tap_b()
    if direction == "left":
        xbox.tap_left()
    if direction == "right":
        xbox.tap_right()
    if direction == "up":
        xbox.tap_up()
    if direction == "down":
        xbox.tap_down()
    tap_targeting()
    memory.main.kim_od_unlocks()
    '''


def lancet_target(target, direction='l', post_steal=False):
    memory.main.kim_od_unlocks()
    CurrentPlayer().use_special_by_name(command_name="Lancet",direction=direction,target_id=target)
    memory.main.kim_od_unlocks()


def lancet_target_old(target, direction, post_steal=False):
    memory.main.kim_od_unlocks()
    logger.debug(f"Casting Lancet with variation: {direction}")
    while memory.main.battle_menu_cursor() != 20:
        if memory.main.battle_menu_cursor() == 255:
            pass
        elif memory.main.battle_menu_cursor() == 1:
            xbox.tap_up()
        elif memory.main.battle_menu_cursor() > 20:
            xbox.tap_up()
        else:
            xbox.tap_down()
    while memory.main.main_battle_menu():
        xbox.tap_b()
    if post_steal:
        _navigate_to_position(2)
    while memory.main.other_battle_menu():
        xbox.tap_b()
    retry = 0
    if memory.main.get_enemy_current_hp()[target - 20] != 0:
        # Only lancet living targets.
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

    tap_targeting()
    memory.main.kim_od_unlocks()


def lancet_home(direction):
    logger.debug("Lancet (home) function")
    while memory.main.battle_menu_cursor() != 20:
        if memory.main.battle_menu_cursor() == 255:
            pass
        elif memory.main.battle_menu_cursor() == 1:
            xbox.tap_up()
        elif memory.main.battle_menu_cursor() > 20:
            xbox.tap_up()
        else:
            xbox.tap_down()
    while memory.main.main_battle_menu():
        xbox.tap_b()
    _navigate_to_position(2)
    while memory.main.other_battle_menu():
        xbox.tap_b()
    if direction == "left":
        xbox.tap_left()
    if direction == "right":
        xbox.tap_right()
    if direction == "up":
        xbox.tap_up()
    if direction == "down":
        xbox.tap_down()
    tap_targeting()


def lancet_omega():
    lancet_used = False
    while not memory.main.battle_wrap_up_active():
        if memory.main.turn_ready():
            if not lancet_used:
                if Kimahri.is_turn():
                    lancet_target(target=20, direction='l')
                    lancet_used=True
                elif not Kimahri.active():
                    buddy_swap(Kimahri)
                else:
                    CurrentPlayer().defend()
            else:
                if screen.turn_aeon():
                    from memory.yojimbo_rng import zanmato_gil_needed
                    needed_amount = zanmato_gil_needed(zan_level=3)  # Set value
                    # needed_amount = 2255000  # Set value
                    logger.debug(f"Check: {needed_amount}")
                    # if needed_amount > 255000:
                    #     needed_amount = 1
                    logger.debug(f"Pay the man: {needed_amount}")
                    Yojimbo.pay(gil_value=needed_amount)
                    memory.main.wait_frames(90)
                elif Yuna.is_turn():
                    Yuna.overdrive(aeon_num=5)
                elif not Yuna.active():
                    buddy_swap(Yuna)
                else:
                    CurrentPlayer().defend()
    wrap_up()


def flee_all(exclude: int = 99, wrap_up_battle=True):
    FFXC.set_neutral()
    logger.debug("Attempting escape (all party members and end screen)")
    if memory.main.battle_active():
        while memory.main.battle_active():
            if memory.main.user_control():
                return True
            if memory.main.turn_ready():
                tidus_position = memory.main.get_battle_char_slot(0)
                logger.debug(f"Tidus Position: {tidus_position}")
                if CurrentPlayer().knows_flee():
                    CurrentPlayer().flee()
                elif tidus_position >= 3 and tidus_position != 255:
                    buddy_swap(Tidus)
                elif (
                    not check_tidus_ok()
                    or tidus_position == 255
                    or memory.main.tidus_escaped_state()
                ):
                    escape_one(exclude=exclude)
                else:
                    CurrentPlayer().defend()
    if memory.main.game_over():
        return False
    logger.info("Flee complete")
    if wrap_up_battle:
        wrap_up()
    return True


def escape_all():
    logger.info("escape_all function")
    while memory.main.battle_active():
        if memory.main.turn_ready():
            escape_one()


def escape_action():
    while memory.main.main_battle_menu():
        if not memory.main.battle_active():
            break
        else:
            xbox.tap_right()
    logger.debug("In other battle menu")
    while memory.main.battle_cursor_2() != 2:
        if not memory.main.battle_active():
            break
        else:
            xbox.tap_down()
    logger.debug("Targeted Escape")
    while memory.main.other_battle_menu():
        if not memory.main.battle_active():
            break
        else:
            xbox.tap_b()
    if memory.main.battle_active():
        logger.debug("Selected Escaping")
        tap_targeting()


def escape_one(exclude: int = 99):
    if exclude == memory.main.get_current_turn():
        not_turn = True
    else:
        not_turn = False
    next_action_escape = rng_track.next_action_escape(
        character=memory.main.get_current_turn()
    )
    logger.debug(f"The next character will escape: {next_action_escape}")
    if (
        not next_action_escape or not_turn
    ) and not get_encounter_id() == 26:
        if memory.main.get_story_progress() < 154:
            logger.debug("Character cannot escape (Lagoon). Attacking instead.")
            CurrentPlayer().attack()
        else:
            logger.debug("Character will not escape. Looking for a replacement.")
            replacement = 255
            replace_array = memory.main.get_battle_formation()
            for i in range(len(replace_array)):
                if replacement != 255:
                    pass
                elif replacement == exclude:
                    pass
                elif (
                    i == 3
                    and memory.main.rng_seed() == 31
                    and memory.main.get_story_progress() < 865
                ):
                    pass
                elif replace_array[i] == 255:
                    pass
                elif replace_array[i] in memory.main.get_active_battle_formation():
                    pass
                elif rng_track.next_action_escape(replace_array[i]):
                    logger.debug(f"Character {replace_array[i]} can escape. Swapping.")
                    replacement = replace_array[i]
                    buddy_swap_char(replacement)
                    return escape_one()
                else:
                    pass
            if replacement == 255:
                logger.debug("No character could be found.")
                if memory.main.get_current_turn() == 0:
                    Tidus.flee()
                    return False
                elif memory.main.get_current_turn() == 1:
                    escape_action()
                else:
                    CurrentPlayer().attack(
                        target_id=memory.main.get_current_turn(), direction_hint="u"
                    )
                    return False
    else:
        escape_action()
        logger.debug("Attempting escape, one person")
        return True


def buddy_swap(character, quick_return:bool=False):
    logger.debug(f"Swapping {character} (in battle)")
    position = character.battle_slot()
    if position == 255:
        logger.warning(f"Cannot swap to {character}, that person is not in the back line.")
        escape_one()
        return

    if position < 3:
        logger.debug(
            f"Cannot swap with {character}, that character is in the front party."
        )
        return
    else:
        while not memory.main.other_battle_menu():
            xbox.l_bumper()
            if not memory.main.battle_active():
                return
        position -= 3
        reserveposition = position % 4
        logger.debug(f"Character is in reserve position {reserveposition}")
        if reserveposition == 3:  # Swap with last slot
            direction = "up"
        else:
            direction = "down"

        while reserveposition != memory.main.battle_cursor_2():
            logger.debug(f"Moving to reserve position {reserveposition}: {memory.main.battle_cursor_2()}")
            if not memory.main.battle_active():
                return
            if direction == "down":
                xbox.tap_down()
            else:
                xbox.tap_up()

        xbox.tap_confirm()
        xbox.tap_confirm()
        xbox.tap_confirm()
        xbox.tap_confirm()
        xbox.tap_confirm()
        xbox.tap_confirm()
        if quick_return:
            logger.debug("Swap - Quick return")
            return
        else:
            logger.debug("Swap - clicking until turn.")
            xbox.click_to_battle()
            logger.debug("Swap - Normal return")
            return


def buddy_swap_char(character:int):
    # This is a temporary hotfix, to be removed once this function is deprecated.
    if isinstance(character, int):
        if character == 0:
            return buddy_swap(Tidus)
        elif character == 1:
            return buddy_swap(Yuna)
        elif character == 2:
            return buddy_swap(Auron)
        elif character == 3:
            return buddy_swap(Kimahri)
        elif character == 4:
            return buddy_swap(Wakka)
        elif character == 5:
            return buddy_swap(Lulu)
        elif character == 6:
            return buddy_swap(Rikku)
    return buddy_swap(character)


def wrap_up():
    # When memory.main.battle_wrap_up_active() is working, we want
    # to pivot to that method instead.
    if memory.main.battle_active():
        while memory.main.battle_value() != 0:
            if memory.main.get_map() == 307:
                pass  # Do not return on the Arena map.
            elif memory.main.turn_ready():
                logger.debug("wrap_up exit, turn is active.")
                return False
            elif memory.main.user_control():
                logger.debug("wrap_up exit, user control regained. (A)")
                return False

    logger.debug("Wrapping up battle.")
    while not memory.main.battle_wrap_up_active():
        if memory.main.user_control():
            logger.debug("wrap_up exit, user control regained. (B)")
            return False
        elif memory.main.menu_open():
            memory.main.wait_frames(3)
            if not memory.main.battle_wrap_up_active():
                logger.debug("wrap_up exit, some other menu is open.")
                return False
        elif memory.main.battle_active():
            logger.debug("wrap_up exit, battle is active.")
            return False
    memory.main.wait_frames(1)
    while memory.main.battle_wrap_up_active():
        FFXC.set_confirm()
    FFXC.release_confirm()
    logger.debug("Wrap up complete.")
    memory.main.wait_frames(1)
    if game_vars.god_mode():
        rng_track.force_preempt()
    
    if game.state == "Nem_Farm":
        post_battle_grid_report()
        
    if game_vars.no_battle_music():
        memory.main.disable_battle_music()
    return True


def post_battle_grid_report():
    out_text = "Post-battle report:\n"
    
    sphere_index = memory.main.get_item_slot(70)
    if sphere_index == 255:
        sphere_count = 0
    else:
        sphere_count = memory.main.get_item_count_slot(sphere_index)
    out_text += f"Power: {sphere_count}\n"
    sphere_index = memory.main.get_item_slot(71)
    if sphere_index == 255:
        sphere_count = 0
    else:
        sphere_count = memory.main.get_item_count_slot(sphere_index)
    out_text += f"Mana: {sphere_count}\n"
    sphere_index = memory.main.get_item_slot(72)
    if sphere_index == 255:
        sphere_count = 0
    else:
        sphere_count = memory.main.get_item_count_slot(sphere_index)
    out_text += f"Speed: {sphere_count}\n\n"
    out_text += "Char levels:\n"

    for i in range(7):
        name = memory.main.name_from_number(i)
        char_levels = memory.sphere_grid.char_sphere_levels(i)
        if i in [0,4,6]:
            out_text += f"{name}: {char_levels}\n"
    
    write_big_text(out_text)


@battle.utils.speedup_decorator
def sin_arms():
    logger.info("Fight start: Sin's Arms")
    # Area for improvement later. Multiple skippable FMVs
    xbox.click_to_battle()
    aeon_summon(4)
    while memory.main.battle_active():  # Arm1
        if memory.main.turn_ready():
            Bahamut.unique()
            xbox.tap_b()
            xbox.tap_b()
        else:
            xbox.tap_b()

    xbox.skip_dialog(0.3)
    while not memory.main.battle_active():
        if memory.main.cutscene_skip_possible():
            xbox.skip_scene()
        elif memory.main.menu_open():
            xbox.tap_b()
        elif memory.main.diag_skip_possible() and not game_vars.story_mode():
            xbox.tap_b()

    aeon_summon(4)

    while memory.main.battle_active():  # Arm2
        if memory.main.turn_ready():
            Bahamut.unique()
            xbox.tap_b()
            xbox.tap_b()
        else:
            xbox.tap_b()

    xbox.skip_dialog(0.3)
    while not memory.main.battle_active():
        if memory.main.cutscene_skip_possible():
            xbox.skip_scene()
        elif memory.main.menu_open():
            xbox.tap_b()
        elif memory.main.diag_skip_possible() and not game_vars.story_mode():
            xbox.tap_b()

    xbox.click_to_battle()  # Start of Sin Core
    aeon_summon(4)
    screen.await_turn()
    if game_vars.nemesis() or game_vars.ne_armor() > 200 or game_vars.platinum():
        while memory.main.battle_active():
            if memory.main.turn_ready():
                CurrentPlayer().attack()
    else:
        Bahamut.unique(target_far_line=True)
        while memory.main.battle_active():
            xbox.tap_b()
    split_timer()

    while not memory.main.user_control():
        if memory.main.cutscene_skip_possible():
            xbox.skip_scene()
        elif memory.main.menu_open():
            xbox.tap_b()
        elif memory.main.diag_skip_possible() and not game_vars.story_mode():
            xbox.tap_b()
    if game_vars.god_mode():
        rng_track.force_preempt()
    logger.info("Done with Sin's Arms section")


@battle.utils.speedup_decorator
def sin_face():
    logger.info("Fight start: Sin's Face")
    xbox.click_to_battle()
    FFXC.set_neutral()

    aeon_first_turn = True
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Yuna.is_turn():
                aeon_summon(4)
            elif screen.turn_aeon():
                if aeon_first_turn:
                    Bahamut.unique()
                    aeon_first_turn = False
                else:
                    CurrentPlayer().attack()
            else:
                CurrentPlayer().defend()
        else:
            xbox.tap_b()
    logger.info("Fight end: Sin's Face")
    split_timer()
    while not (memory.main.user_control() or memory.main.cutscene_skip_possible()):
        xbox.tap_b()
    if memory.main.cutscene_skip_possible():
        memory.main.wait_frames(2)
        xbox.skip_scene(fast_mode=True)
        while not memory.main.user_control():
            if not game_vars.story_mode():
                xbox.tap_b()
    if game_vars.god_mode():
        rng_track.force_preempt()


@battle.utils.speedup_decorator
def yojimbo():
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Yuna.is_turn():
                aeon_summon(4)
            elif screen.turn_aeon():
                CurrentPlayer().attack()
            else:
                CurrentPlayer().defend()
        elif memory.main.diag_skip_possible():
            xbox.tap_b()


def bfa_nem():
    logger.debug("Start of BFA/Nemesis")
    FFXC.set_movement(1, 0)
    memory.main.wait_frames(30 * 0.4)
    FFXC.set_movement(1, 1)
    memory.main.await_event()
    FFXC.set_neutral()
    tidus_first_turn = False

    xbox.click_to_battle()

    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Tidus.is_turn():
                if tidus_first_turn:
                    Tidus.swap_battle_weapon(ability=[0x8019])
                    tidus_first_turn = True
                else:
                    CurrentPlayer().attack()
            else:
                CurrentPlayer().defend()
    logger.debug("BFA down")
    split_timer()

    while memory.main.get_story_progress() < 3380:
    #while memory.main.get_story_progress() < 3400:  # End of game
        if memory.main.battle_active():
            if memory.main.turn_ready():
                if get_encounter_id() == 404:
                    if Wakka.is_turn() or Tidus.is_turn():
                        CurrentPlayer().attack()
                    else:
                        CurrentPlayer().cast_black_magic_spell_by_name(spell_name="Ultima")
                elif Tidus.is_turn():
                    CurrentPlayer().attack(record_results=True)
                    logger.debug(f"Battle Num: {get_encounter_id()}")
                elif Yuna.is_turn() and not Wakka.active():
                    buddy_swap(Wakka)
                elif Auron.is_turn() and not Lulu.active():
                    buddy_swap(Lulu)
                else:
                    CurrentPlayer().defend()
            elif memory.main.diag_skip_possible():
                xbox.tap_b()
        elif memory.main.cutscene_skip_possible():
            memory.main.wait_frames(2)
            if memory.main.cutscene_skip_possible():
                xbox.skip_scene()
        else:
            xbox.tap_b()
            
    screen.await_turn()
    while memory.main.get_enemy_current_hp()[0] != 0:
        if memory.main.battle_active():
            if memory.main.turn_ready():
                if Tidus.is_turn():
                    CurrentPlayer().attack(record_results=True)
                    logger.debug(f"Battle Num: {get_encounter_id()}")
                elif Yuna.is_turn():
                    buddy_swap(Wakka)
                elif Auron.is_turn():
                    buddy_swap(Lulu)
                else:
                    CurrentPlayer().defend()
        elif memory.main.cutscene_skip_possible():
            memory.main.wait_frames(2)
            if memory.main.cutscene_skip_possible():
                xbox.skip_scene()
        else:
            xbox.tap_b()
    while int(memory.main.get_camera()[1]) != 0:
        pass
    split_timer()
    logger.debug("GG Nemesis%")
    logger.debug("Returning to main")
    return True


def yu_yevon_item():
    if memory.main.get_item_slot(6) < 200:
        return 6
    elif memory.main.get_item_slot(7) < 200:
        return 7
    elif memory.main.get_item_slot(8) < 200:
        return 8
    elif memory.main.get_item_slot(2) < 200:
        return 2
    #elif memory.main.get_item_slot(1) < 200:
    #    return 1
    #elif memory.main.get_item_slot(0) < 200:
    #    return 0
    else:
        return 99


def check_petrify():
    # This function is always returning as if someone is petrified, needs review.
    for iter_var in range(7):
        logger.debug(f"Checking character {iter_var} for petrification")
        if memory.main.state_petrified(iter_var):
            logger.debug(f"Character {iter_var} is petrified.")
            return True
    logger.debug("Everyone looks good - no petrification")
    return False


def check_petrify_tidus():
    return memory.main.state_petrified(0)


def rikku_od_items(slot):
    _navigate_to_position(slot, battle_cursor=memory.main.rikku_od_cursor_1)


def rikku_full_od(battle):
    # First, determine which items we are using
    path = "any"
    if battle == "tutorial":
        pot_slot = memory.main.get_item_slot(0)
        if pot_slot == 255:
            pot_count = 0
        else:
            pot_count = memory.main.get_item_count_slot(pot_slot)
        hi_pot_slot = memory.main.get_item_slot(1)
        if hi_pot_slot == 255:
            hi_pot_count = 0
        else:
            hi_pot_count = memory.main.get_item_count_slot(pot_slot)
        ability_slot = memory.main.get_item_slot(73)
        
        # Now pick the best path.
        if memory.main.get_power() < 34:
            item1 = ability_slot
            item2 = ability_slot
        elif pot_count >= 2:
            item1 = pot_slot
            item2 = pot_slot
            path = "potions"
        elif pot_count == 1 and hi_pot_count >= 1:
            item1 = pot_slot
            item2 = hi_pot_slot
            path = "potions"
        else:
            item1 = ability_slot
            item2 = ability_slot
    elif battle == "Evrae":
        # No longer viable with Terra skip
        '''
        if game_vars.skip_kilika_luck():
            item1 = memory.main.get_item_slot(81)
            logger.debug(f"Lv1 sphere in slot: {item1}")
            item2 = memory.main.get_item_slot(84)
            logger.debug(f"Lv4 sphere in slot: {item2}")
        else:
        '''
        item1 = memory.main.get_item_slot(94)
        logger.debug(f"Luck sphere in slot: {item1}")
        item2 = memory.main.get_item_slot(100)
        logger.debug(f"Map in slot: {item2}")
    elif battle == "Flux":
        item1 = memory.main.get_item_slot(35)
        logger.debug(f"Grenade in slot: {item1}")
        item2 = memory.main.get_item_slot(85)
        logger.debug(f"HP Sphere in slot: {item2}")
    elif battle == "trio":
        item1 = 108
        item2 = 108
        logger.debug(f"Wings are in slot: {item1}")
    elif battle == "crawler":
        item1 = memory.main.get_item_slot(30)
        logger.debug(f"Lightning Marble in slot: {item1}")
        item2 = memory.main.get_item_slot(82)
        logger.debug(f"Lv2 Sphere in slot: {item2}")
    elif battle == "spherimorph1":
        item1 = memory.main.get_item_slot(24)
        logger.debug(f"Arctic Wind in slot: {item1}")
        item2 = memory.main.get_item_slot(90)
        logger.debug(f"Mag Def Sphere in slot: {item2}")
    elif battle == "spherimorph2":
        item1 = memory.main.get_item_slot(32)
        logger.debug(f"Fish Scale in slot: {item1}")
        item2 = memory.main.get_item_slot(90)
        logger.debug(f"Mag Sphere in slot: {item2}")
    elif battle == "spherimorph3":
        item1 = memory.main.get_item_slot(30)
        logger.debug(f"Lightning Marble in slot: {item1}")
        item2 = memory.main.get_item_slot(90)
        logger.debug(f"Mag Sphere in slot: {item2}")
    elif battle == "spherimorph4":
        item1 = memory.main.get_item_slot(27)
        logger.debug(f"Bomb Core in slot: {item1}")
        item2 = memory.main.get_item_slot(90)
        logger.debug(f"Mag Sphere in slot: {item2}")
    elif battle == "bfa":
        item1 = memory.main.get_item_slot(35)
        logger.debug(f"Grenade in slot: {item1}")
        item2 = memory.main.get_item_slot(85)
        logger.debug(f"HP Sphere in slot: {item2}")
    elif battle == "shinryu":
        item1 = memory.main.get_item_slot(109)
        logger.debug(f"Gambler's Spirit in slot: {item1}")
        item2 = memory.main.get_item_slot(58)
        logger.debug(f"Star Curtain in slot: {item2}")
    elif battle == "omnis":
        both_items = omnis_items()
        logger.debug("Omnis items, many possible combinations.")
        item1 = memory.main.get_item_slot(both_items[0])
        item2 = memory.main.get_item_slot(both_items[1])

    if item1 > item2:
        item3 = item1
        item1 = item2
        item2 = item3

    # Now to enter commands

    logger.warning("Mark A")
    while not memory.main.other_battle_menu():
        xbox.tap_left()

    logger.warning("Mark B")
    while not memory.main.interior_battle_menu():
        xbox.menu_b()
    logger.warning("Mark C")
    rikku_od_items(item1)
    logger.warning("Mark D")
    if path == "potions":
        memory.main.wait_frames(3)
        xbox.menu_b()
    else:
        while not memory.main.rikku_overdrive_item_selected_number():
            xbox.menu_b()
    logger.warning("Mark E")
    rikku_od_items(item2)
    logger.warning("Mark 1")
    while memory.main.interior_battle_menu():
        xbox.tap_b()
    logger.warning("Mark 2")
    tap_targeting()
    logger.warning("Mark 3")


def check_character_ok(char_num):
    if char_num not in memory.main.get_active_battle_formation():
        return True
    return not any(
        func(char_num)
        for func in [
            memory.main.state_petrified,
            memory.main.state_confused,
            memory.main.state_dead,
            memory.main.state_berserk,
            memory.main.state_sleep,
        ]
    )


def check_tidus_ok():
    return check_character_ok(0)


def check_rikku_ok():
    return check_character_ok(6)


# unused
def check_yuna_ok():
    return check_character_ok(1)


def get_digit(number, n):
    return number // 10**n % 10


def calculate_spare_change_movement(gil_amount, force_max=False):
    max_gil_check = False
    if gil_amount > memory.main.get_gil_value():
        gil_amount = memory.main.get_gil_value()
        max_gil_check = True
        
    if max_gil_check or force_max:
        # If we snap to max, the original logic will not work.
        xbox.menu_right()
        for _ in range(10):
            xbox.tap_up()
        memory.main.wait_frames(3)
        xbox.tap_b()
        xbox.tap_b()
        xbox.tap_b()
        xbox.tap_b()
        return
    gil_amount = min(gil_amount, 999999)
    # gil_amount = min(gil_amount, 100000)
    position = {}
    gil_copy = gil_amount
    for index in range(0, 7):
        amount = get_digit(gil_amount, index)
        if gil_copy * 10 > memory.main.get_gil_value():
            if amount > 5:
                gil_amount += 10 ** (index + 1)
        position[index] = amount
    logger.debug(f"Amt1: {gil_amount} | Amt2: {amount} | Copy: {gil_copy}")
    logger.debug(position)

    for cur in range(6, -1, -1):
        if not position[cur]:
            continue
        while memory.main.spare_change_cursor() != cur:
            memory.main.side_to_side_direction(
                memory.main.spare_change_cursor(), cur, 6
            )
        target = position[cur]
        while get_digit(memory.main.spare_change_amount(), cur) != target:
            if target > 5:
                xbox.tap_down()
            else:
                xbox.tap_up()
        if memory.main.spare_change_amount() == gil_copy:
            return
    return


def charge_rikku_od():
    logger.debug(f"Battle Number: {get_encounter_id()}")
    if Rikku.overdrive_percent() < 100 and get_encounter_id() in [
        360,
        361,
        376,
        378,
        381,
        384,
        386,
    ]:
        if (
            not Tidus.escaped() and not Tidus.is_status_ok()
        ) or not Rikku.is_status_ok():
            logger.debug("Tidus or Rikku incapacitated, fleeing")
            logger.debug(f"{not Tidus.escaped()}")
            logger.debug(f"{not Tidus.is_status_ok()}")
            logger.debug(f"{not Rikku.is_status_ok()}")
            flee_all()
        else:
            logger.debug("Ready to charge.")
            while memory.main.battle_active():
                if memory.main.turn_ready():
                    if Rikku.is_turn():
                        Rikku.attack(target_id=Rikku, direction_hint="u")
                    elif Rikku.has_overdrive():
                        flee_all()
                    elif not Rikku.active():
                        buddy_swap(Rikku)
                    else:
                        escape_one()
        memory.main.click_to_control_3()
    else:
        logger.debug("Something is wrong. Getting out!")
        flee_all()


def faint_check_with_escapes():
    faints = 0
    for x in range(3):
        if memory.main.get_active_battle_formation()[x] == 255:
            pass
        elif memory.main.state_dead(memory.main.get_active_battle_formation()[x]):
            faints += 1
    return faints


def check_gems():
    gem_slot = memory.main.get_item_slot(34)
    if gem_slot < 200:
        gems = memory.main.get_item_count_slot(gem_slot)
    else:
        gems = 0

    gem_slot = memory.main.get_item_slot(28)
    if gem_slot < 200:
        gems += memory.main.get_item_count_slot(gem_slot)
    logger.debug(f"Total gems: {gems}")
    return gems


@battle.utils.speedup_decorator
def calm_lands_manip():
    gem_need = max(2-check_gems(),0)
    from rng_track import nea_track
    _, defender_x_drop, _, _, _ = nea_track()
    rng10_array = memory.main.next_chance_rng_10_full()
    rng10_align = gem_need
    logger.info(f"Drop: {defender_x_drop} - Gem need: {gem_need}")

    found = False
    chosen_steals = 0
    chosen_deaths = 0
    if defender_x_drop:
        if not rng10_align in rng10_array:
            for j in range(3):
                for i in range(4):
                    if int(j + rng10_align + (i * 3)) in rng10_array:
                        if not found:
                            chosen_steals = j
                            chosen_deaths = i
                            found = True
    else:
        if rng10_align in rng10_array:
            for j in range(3):
                for i in range(4):
                    if not int(j + rng10_align + (i * 3)) in rng10_array:
                        if not found:
                            chosen_steals = j
                            chosen_deaths = i
                            found = True

    while memory.main.battle_active():
        if memory.main.turn_ready():
            logger.info(f"Calm manip: {gem_need} gems + {chosen_steals} steals + {chosen_deaths} deaths")
            next_turn = who_goes_first_after_current_turn(range(30))


            if chosen_steals == 0 and chosen_deaths == 0:
                logger.debug("Calm manip: No advances needed. Flee command.")
                flee_all()
            elif Tidus.is_turn():
                if chosen_deaths == 0:
                    if next_turn >= 20:
                        logger.debug(f"Can't afford a death - Tidus escape.")
                        flee_all()
                    else:
                        buddy_swap(Kimahri)
                else:
                    logger.debug("Calm manip: Tidus escape for > 3 manip (B)")
                    escape_one()
            elif Rikku.is_turn():
                if chosen_deaths == 0 and next_turn >= 20:
                    # buddy_swap(Tidus)
                    flee_all()
                elif chosen_deaths == 1:
                    logger.debug("Calm manip: Rikku escape (C)")
                    escape_one()
                elif chosen_steals != 0:
                    logger.debug("Calm manip: Trigger steal command. (C)")
                    if get_encounter_id() in [273,274,276,279,281,282,289]:
                        steal_target(index=21)
                        chosen_steals -= 1
                    else:
                        steal_target(index=20)
                        chosen_steals -= 1
                else:
                    logger.debug("Calm manip: Rikku defend for >= 2 death (D)")
                    Rikku.defend()
            elif Kimahri.is_turn():
                if chosen_steals != 0:
                    if get_encounter_id() in [273,274,276,279,281,282,289]:
                        steal_target(index=21)
                        chosen_steals -= 1
                    else:
                        steal_target(index=20)
                        chosen_steals -= 1
                else:
                    Kimahri.defend()
            elif chosen_steals != 0 and not Kimahri.active():
                buddy_swap(Kimahri)
            else:
                logger.debug("Calm manip: Current player defend for 2 deaths (E)")
                CurrentPlayer().defend()

        else:
            FFXC.set_neutral()
    wrap_up()


def calm_lands_gems():
    # _,_,_,_ = rng_track.nea_track()
    while not memory.main.turn_ready():
        pass
    
    steal_complete = False
    if get_encounter_id() not in [273, 275, 281, 283]:
        flee_all()
        return
    if memory.main.battle_type() == 2:
        logger.debug("Avoiding ambush. Flee.")
        flee_all()
        return
    
    while memory.main.battle_active():
        check_array = [get_next_turn(),20,21,22,23]
        if memory.main.turn_ready():
            #next_turn = who_goes_first_after_current_turn(check_array)
            # We should start with predicting character deaths. Add later.
            #if next_turn >= 20:
            #    flee_all()
            #    return
            if steal_complete:
                flee_all()
                return
            next_turn = who_goes_first_after_current_turn(range(30))
            if next_turn >= 20:
                flee_all()
                return
            elif not Kimahri.active():
                buddy_swap(Kimahri)
                screen.await_turn()
            elif Kimahri.is_turn():
                # Red element in center slot, with machina and dog
                if get_encounter_id() in [273, 281]:
                    logger.debug("Grabbing a gem here.")
                    steal_target(index=21)
                # Red element in top slot, with bee and tank
                elif get_encounter_id() in [275, 283]:
                    logger.debug("Grabbing a gem here.")
                    steal_target(index=22)
                else:
                    CurrentPlayer().defend()
                steal_complete = True
            else:
                CurrentPlayer().defend()
    wrap_up()


def calm_steal():
    if get_encounter_id() in [276, 313]:
        _steal("down")
    elif get_encounter_id() == 289:
        _steal("up")
    elif get_encounter_id() == 314:
        _steal("right")
    else:
        _steal()


def gorge_manip_battle(epaaj_kills:int=2):
    from battle.gorge_manip import gorge_manip_engage
    gorge_manip_engage(epaaj_kills=epaaj_kills)
    if memory.main.game_over():
        return False
    return True

    
def gorge_manip_battle_dec_2025(epaaj_kills:int=2):
    aeon_turns = 0

    while memory.main.battle_active():
        if memory.main.turn_ready():
            rng10_array = memory.main.next_chance_rng_10_full()
            align_array = []
            for i in range(30):
                if i in rng10_array:
                    align_array.append(i)
            active_party = memory.main.get_active_battle_formation()
            logger.debug(f"Active party: {active_party}")
            while 255 in active_party:
                active_party.remove(255)
            logger.debug(f"Active party (abridged): {active_party}")
            logger.debug(f"Full party: {memory.main.get_battle_formation()}")

            if screen.turn_aeon():
                if aeon_turns >= 1:
                    Bahamut.dismiss()
                elif memory.main.get_encounter_id() == 312 and (
                    epaaj_kills >= 2 or
                    (
                        3 in align_array and
                        not 0 in align_array
                    ) or
                    (
                        not 3 in align_array and
                        0 in align_array
                    )
                ):
                    Bahamut.unique()
                elif memory.main.get_encounter_id() == 312:
                    Bahamut.attack(target_id=20)
                else:
                    Bahamut.unique()
                aeon_turns += 1
            elif Yuna.is_turn() and aeon_turns == 0 and (
                0 in align_array or (
                    3 in align_array and
                    memory.main.get_encounter_id() == 312
                )
            ):
                aeon_summon(4)
            elif aeon_turns == 0 and not Yuna.active() and (
                0 in align_array or (
                    3 in align_array and memory.main.get_encounter_id() == 312
                )
            ):
                buddy_swap(Yuna)
            elif (
                1 in align_array and 
                not Kimahri.active() and 
                3 in memory.main.get_battle_formation() and
                memory.main.get_next_turn() < 7
            ):
                buddy_swap(Kimahri)
            elif (
                1 in align_array and 
                Kimahri.is_turn() and
                memory.main.get_next_turn() < 7
            ):
                steal_new(Kimahri.raw_id())
            elif aeon_turns != 0:
                if Tidus.is_turn() or (
                    0 in memory.main.get_battle_formation() and 
                    not 0 in active_party
                ):
                    flee_all()
                else:
                    escape_one()
            else:
                # Not close enough for alignment, now we must manip.
                if Tidus.is_turn():
                    escape_one()  # We need to live the battle regardless.
                elif 3 in align_array:
                    if len(active_party) > 1:
                        escape_one()
                    else:
                        CurrentPlayer().defend()
                elif 6 in align_array:
                    if screen.faint_check():
                        revive()
                    else:
                        CurrentPlayer().defend()
                elif 4 in align_array:
                    if memory.unlocks.has_ability_unlocked(
                        character_index=CurrentPlayer().raw_id(),
                        ability_name="Steal"
                    ):
                        steal_new()
                    elif (
                        3 in memory.main.get_battle_formation() and 
                        not 3 in active_party
                    ):
                        buddy_swap(Kimahri)
                        steal_new()
                    elif (
                        6 in memory.main.get_battle_formation() and 
                        not 6 in active_party
                    ):
                        buddy_swap(Rikku)
                        steal_new()
                    elif len(active_party) > 1:
                        escape_one()
                    else:
                        CurrentPlayer().defend()
                elif 7 in align_array:
                    if memory.unlocks.has_ability_unlocked(
                        character_index=CurrentPlayer().raw_id(),
                        ability_name="Steal"
                    ):
                        steal_new()
                    elif (
                        3 in memory.main.get_battle_formation() and 
                        not 3 in active_party
                    ):
                        buddy_swap(Kimahri)
                        steal_new()
                    elif (
                        6 in memory.main.get_battle_formation() and 
                        not 6 in active_party
                    ):
                        buddy_swap(Rikku)
                        steal_new()
                    else:
                        CurrentPlayer().defend()
                else:
                    # Remove low values, where we have no chance to hit those values.
                    while align_array[0] < 7:
                        align_array.remove(align_array[0])
                    if align_array[0] % 3 == 0:
                        CurrentPlayer().defend()
                    elif memory.unlocks.has_ability_unlocked(
                        character_index=CurrentPlayer().raw_id(),
                        ability_name="Steal"
                    ):
                        steal_new()
                    elif (
                        3 in memory.main.get_battle_formation() and 
                        not 3 in active_party
                    ):
                        buddy_swap(Kimahri)
                        steal_new()
                    elif (
                        6 in memory.main.get_battle_formation() and 
                        not 6 in active_party
                    ):
                        buddy_swap(Rikku)
                        steal_new()
                    else:
                        CurrentPlayer().defend()
    wrap_up()



def advance_rng_10(num_advances: int):
    skip_attempt = False
    if (
        not game_vars.get_def_x_drop() and
        memory.main.next_chance_rng_10() != 0
    ):
        skip_attempt = True

    if memory.main.get_next_turn() >= 20 and num_advances < 3:
        # Enemy taking next turn.
        flee_all()
    elif skip_attempt and memory.main.get_map() != 266:
        flee_all()
    else:
        escape_success_count = 0
        logger.debug("RNG10 logic")
        logger.debug(f"{num_advances}")
        logger.debug(f"{screen.faint_check()}")
        while memory.main.battle_active():
            if memory.main.turn_ready():
                logger.debug(f"Registering advances: {num_advances}")
                if memory.main.get_next_turn() >= 20 and num_advances < 3:
                    flee_all()
                elif get_encounter_id() == 321:
                    logger.debug("Registering evil jar guy, fleeing.")
                    flee_all()
                # elif get_encounter_id() == 287:
                #    logger.debug("Registering Anaconadeur - I am French!!! - fleeing")
                #    flee_all()
                elif num_advances >= 6:
                    if escape_success_count == 0:
                        if escape_one():
                            escape_success_count += 1
                    elif faint_check_with_escapes() == 2:
                        logger.debug("Registering two people down. Escaping.")
                        flee_all()
                    elif Kimahri.is_turn() or Rikku.is_turn():
                        logger.debug("Registering turn, steal character")
                        # Most convenient since overdrive is needed for Flux.
                        if num_advances % 3 != 0:
                            calm_steal()
                            num_advances -= 1
                        elif escape_success_count == 0:
                            if escape_one():
                                escape_success_count += 1
                        else:
                            CurrentPlayer().defend()
                    elif (
                        3 in memory.main.get_battle_formation()
                        and not Kimahri.active()
                        and num_advances % 3 != 0
                    ):
                        buddy_swap(Kimahri)
                    elif escape_success_count == 0:
                        if escape_one():
                            escape_success_count += 1
                    else:
                        CurrentPlayer().defend()
                elif num_advances >= 3:
                    if faint_check_with_escapes() >= 1:
                        flee_all()
                    elif escape_success_count == 0:
                        if escape_one():
                            escape_success_count += 1
                    elif Rikku.is_turn() and escape_success_count == 1:
                        if escape_one():
                            escape_success_count += 1
                    elif Kimahri.is_turn():
                        logger.debug("Registering turn, steal character")
                        # Most convenient since overdrive is needed for Flux.
                        if num_advances % 3 != 0:
                            calm_steal()
                            num_advances -= 1
                        else:
                            CurrentPlayer().defend()
                    elif (
                        3 in memory.main.get_battle_formation()
                        and not Kimahri.active()
                        and num_advances % 3 != 0
                    ):
                        buddy_swap(Kimahri)
                    elif escape_success_count in [0, 1]:
                        if escape_one():
                            escape_success_count += 1
                    else:
                        CurrentPlayer().defend()
                elif num_advances in [1, 2]:
                    logger.debug(f"Registering advances: {num_advances}")
                    if Kimahri.is_turn() or Rikku.is_turn():
                        logger.debug("Registering turn, steal character")
                        calm_steal()
                        num_advances -= 1
                    elif not Kimahri.active():
                        buddy_swap(Kimahri)
                    elif not Rikku.active():
                        buddy_swap(Rikku)
                    elif Tidus.is_turn():
                        flee_all()
                    elif not Tidus.active():
                        buddy_swap(Tidus)
                    else:
                        CurrentPlayer().defend()  # should not occur.
                else:  # any other scenarios, ready to advance.
                    logger.debug("Registering no advances needed, forcing flee.")
                    flee_all()
    memory.main.click_to_control_3()


def rng_12_attack():
    logger.debug("RNG12 logic (attack only)")
    if screen.turn_aeon():
        if get_encounter_id() in [283, 309, 313]:
            CurrentPlayer().attack(target_id=21, direction_hint="u")  # Second target
        elif get_encounter_id() in [284]:
            CurrentPlayer().attack(target_id=22, direction_hint="u")  # Third target
        elif get_encounter_id() in [275, 289]:
            CurrentPlayer().attack(
                target_id=21, direction_hint="r"
            )  # Second target, aim right (aeon only)
        elif get_encounter_id() in [303]:
            CurrentPlayer().attack(target_id=21, direction_hint="l")  # Second target
        elif get_encounter_id() in [304]:
            CurrentPlayer().attack(target_id=23, direction_hint="u")  # fourth target
        elif get_encounter_id() in [314]:
            CurrentPlayer().attack(target_id=21, direction_hint="r")
        else:
            CurrentPlayer().attack()
    else:  # Non-aeon logic, fix this later.
        CurrentPlayer().attack()


def advance_rng_12():
    logger.debug("RNG12 logic (decision logic)")
    attack_count = False
    aeon_turn = False
    use_impulse = False
    double_drop = False
    while memory.main.battle_active():
        if get_encounter_id() == 321:
            logger.debug("Registering evil jar guy")
            logger.debug("Aw hell naw, we want nothing to do with this guy!")
            flee_all()
        elif memory.main.turn_ready():
            #pre_x, post_x, _ = rng_track.nea_track()
            _,_,_,epaaj_count,_ = rng_track.nea_track()
            #if post_x == 1:
            #    advances = 1
            #elif memory.main.get_map() == 223:
            #    advances = pre_x
            #else:
            #    advances = post_x
            if Yuna.is_turn():
                if aeon_turn:
                    flee_all()
                else:
                    aeon_summon(4)
            elif screen.turn_aeon():
                if not aeon_turn:
                    rng_12_attack()
                else:
                    if get_encounter_id() in [313, 314]:
                        Bahamut.unique()
                    else:
                        CurrentPlayer().dismiss()

                aeon_turn = True
            else:
                if aeon_turn:
                    flee_all()
                elif not Yuna.active():
                    buddy_swap(Yuna)
                else:
                    CurrentPlayer().defend()
    memory.main.click_to_control_3()


@battle.utils.speedup_decorator
def ghost_kill():
    next_drop, _ = rng_track.item_to_be_dropped()
    owner1 = next_drop.equip_owner
    owner2 = next_drop.equip_owner_alt
    tidus_hasted = False

    if owner2 in [0, 4, 6]:
        logger.manip(f"Aeon kill results in NEA on char:{owner2}")
        aeon_kill=True
    elif owner1 in [0, 4, 6]:
        logger.manip(f"Any character kill results in NEA on char:{owner1}")
        aeon_kill=False
    elif owner1 == 9:
        logger.manip(f"Has to be Tidus kill: {owner1}")
        aeon_kill=False
    else:
        logger.manip(f"No way to get an optimal drop. Resorting to aeon: {owner2}")
        aeon_kill=True
    
    silence_slot = memory.main.get_item_slot(39)
    if silence_slot != 255:
        silence_count = memory.main.get_item_count_slot(silence_slot)
    else:
        silence_count = 0
    write_big_text(f"Silence grenade count: {silence_count}")

    advance_needed = memory.main.next_chance_rng_10()
    if aeon_kill and advance_needed < 3:
        silence_slot = 255
    
    use_silence = bool(silence_slot != 255)

    if advance_needed:
        tidus_hasted, silence_slot = ghost_advance_rng_10_silence(
            use_silence=use_silence, aeon_kill=aeon_kill
        )
        use_silence = False
    if not memory.main.battle_active():
        wrap_up()
        memory.main.click_to_control_3()
        return

    if owner2 in [0, 4, 6]:
        ghost_kill_aeon()
    elif owner1 in [0, 4, 6]:
        ghost_kill_any(use_silence=use_silence, self_haste=tidus_hasted)
    elif owner1 == 9:
        ghost_kill_tidus(use_silence=use_silence, self_haste=tidus_hasted)
    else:
        ghost_kill_aeon()

    memory.main.click_to_control_3()
    if game_vars.god_mode():
        rng_track.force_preempt()


def ghost_advance_rng_10_silence(use_silence:bool = False,aeon_kill:bool = True):
    logger.debug("RNG10 is not aligned. Special logic to align.")
    # Premise is that we must have a silence grenade in inventory.
    # We should force extra manip in gorge if no silence grenade,
    # so should be guaranteed if this triggers.
    # pref_drop = [0, 4, 6, 9]  # 9 indicates equipment drops for killer.
    if use_silence:
        silence_slot = memory.main.get_use_items_slot(39)
        silence_used = False
    else:
        silence_slot = 255
        silence_used = True
    tidus_hasted = not aeon_kill
    while memory.main.next_chance_rng_10():
        if memory.main.turn_ready():
            logger.manip(f"Steals needed: {memory.main.next_chance_rng_10()}")
            if not silence_used:
                if not Kimahri.active():
                    buddy_swap(Kimahri)
                    use_item(slot=silence_slot)  # Throw silence grenade
                    silence_used = True
                    silence_slot = 255
                elif not Rikku.active():
                    buddy_swap(Rikku)
                    use_item(slot=silence_slot)  # Throw silence grenade
                    silence_used = True
                    silence_slot = 255
                elif Rikku.is_turn() or Kimahri.is_turn():
                    use_item(slot=silence_slot)  # Throw silence grenade
                    silence_used = True
                    silence_slot = 255
                elif Tidus.is_turn() and not tidus_hasted:
                    tidus_haste("left", character=0)
                else:
                    CurrentPlayer().defend()
            else:
                if Kimahri.is_turn():
                    steal()
                elif not Kimahri.active():
                    buddy_swap(Kimahri)
                elif aeon_kill:
                    if Rikku.is_turn():
                        steal()
                    elif not Rikku.active():
                        buddy_swap(Rikku)
                    else:
                        CurrentPlayer().defend()
                else:
                    if not Yuna.active():
                        buddy_swap(Yuna)
                    elif Yuna.is_turn():
                        if memory.main.get_enemy_current_hp()[0] > 6000:
                            Yuna.attack()
                        else:
                            Yuna.defend()
                    elif not Tidus.active():
                        buddy_swap(Tidus)
                    elif Tidus.is_turn():
                        if not tidus_hasted:
                            tidus_haste("left", character=0)
                        elif memory.main.get_enemy_current_hp()[0] > 4500:
                            Tidus.attack()
                        else:
                            Tidus.defend()
                    else:
                        CurrentPlayer().defend()


    logger.debug("RNG10 is now aligned.")
    if game_vars.god_mode():
        rng_track.force_preempt()
    return tidus_hasted, silence_slot


def ghost_kill_tidus(use_silence: bool, self_haste: bool):
    if use_silence:
        silence_slot = memory.main.get_use_items_slot(39)
    else:
        silence_slot = 255
    logger.debug(f"Silence slot: {silence_slot}")
    if not self_haste and silence_slot < 200:
        screen.await_turn()
        if not Rikku.active():
            buddy_swap(Rikku)
        elif not Kimahri.active():
            buddy_swap(Kimahri)
        screen.await_turn()
        use_item(slot=silence_slot)  # Throw silence grenade

    while memory.main.battle_active():
        # Try to get NEA on Tidus
        if memory.main.turn_ready():
            if not Tidus.active():
                logger.debug("Get Tidus back in")
                buddy_swap(Tidus)
            elif Tidus.is_turn():
                if not self_haste:
                    tidus_haste("none")
                    self_haste = True
                elif (
                    memory.main.get_enemy_current_hp()[0] <= 2800
                    and Tidus.has_overdrive()
                ):
                    Tidus.overdrive()
                else:
                    CurrentPlayer().attack()
            elif not Yuna.active():
                logger.debug("Get Yuna in for extra smacks")
                buddy_swap(Yuna)
            elif Yuna.is_turn() and memory.main.get_enemy_current_hp()[0] > 3250:
                # Yuna confirmed can do 3180 damage.
                Yuna.attack()
            else:
                Yuna.defend()
    wrap_up()
    if game_vars.god_mode():
        rng_track.force_preempt()


def ghost_kill_any(use_silence: bool, self_haste: bool):
    yuna_haste = False
    # item_thrown = silence_slot >= 200  # item_thrown is assigned to but never used
    if use_silence:
        silence_slot = memory.main.get_use_items_slot(39)
    else:
        silence_slot = 255
    logger.debug(f"Silence slot: {silence_slot}")
    if not self_haste and silence_slot < 200:
        screen.await_turn()
        if not Rikku.active():
            buddy_swap(Rikku)
        elif not Kimahri.active():
            buddy_swap(Kimahri)
        screen.await_turn()
        use_item(slot=silence_slot)  # Throw silence grenade

    while memory.main.battle_active():
        if memory.main.turn_ready():
            if not Tidus.active():
                logger.debug("Get Tidus back in")
                buddy_swap(Tidus)
            elif Tidus.is_turn():
                if not self_haste:
                    tidus_haste("none")
                    self_haste = True
                elif (
                    Yuna.active()
                    and not yuna_haste
                    and memory.main.get_enemy_current_hp()[0] <= 6000
                ):
                    tidus_haste(direction="l", character=Yuna)
                    yuna_haste = True
                elif (
                    memory.main.get_enemy_current_hp()[0] <= 2800
                    and Tidus.has_overdrive()
                ):
                    Tidus.overdrive()
                else:
                    CurrentPlayer().attack()
            elif not Yuna.active():
                logger.debug("Get Yuna in for extra smacks")
                buddy_swap(Yuna)
            elif Yuna.is_turn():
                Yuna.attack()
            else:
                CurrentPlayer().defend()
    wrap_up()
    if game_vars.god_mode():
        rng_track.force_preempt()


def ghost_kill_aeon():
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if screen.turn_aeon():
                CurrentPlayer().attack()
            elif not Yuna.active():
                buddy_swap(Yuna)
            elif Yuna.is_turn():
                aeon_summon(4)
            else:
                CurrentPlayer().defend()
    wrap_up()
    if game_vars.god_mode():
        rng_track.force_preempt()


def belgemine(use_aeon:int = 4, impulse:bool = False, special_end=False):
    # Used in showcase mode only
    FFXC.set_neutral()
    if not memory.main.battle_active():
        memory.main.click_to_diag_progress(9)
        logger.debug("Mark 1")
        memory.main.wait_frames(45)
        xbox.tap_b()
        logger.debug("Mark 2")
        memory.main.wait_frames(60)
        xbox.tap_up()
        xbox.tap_up()
        xbox.tap_b()
        xbox.click_to_battle()
    while memory.main.battle_active():
        if Yuna.is_turn():
            aeon_summon(use_aeon)
        elif Bahamut.is_turn():
            if impulse:
                Bahamut.unique()
            else:
                Bahamut.attack()
        elif screen.turn_aeon():
            CurrentPlayer().attack()
        else:
            CurrentPlayer().defend()
    memory.main.wait_seconds(15)
    if special_end:
        xbox.tap_confirm()
        memory.main.wait_seconds(40)
    memory.main.click_to_control()

def zanarkand_levels():
    while memory.main.battle_active():
        if get_encounter_id() in [360,361]:
            flee_all()
        elif memory.main.turn_ready():
            if Yuna.is_turn():
                aeon_summon(4)
            elif Bahamut.is_turn():
                Bahamut.unique()
            elif not Yuna.active():
                buddy_swap(Yuna)
            else:
                CurrentPlayer().defend()
    wrap_up()


def lulu_overdrive_heal():
    '''
    # Healing does not work on this boss.
    slot = memory.main.get_item_slot(8)  # Elixir
    if slot != 255:
        logger.warning("THROWING ELIXIR")
        _use_healing_item(num=20, direction='u',item_id=8)
        return
    slot = memory.main.get_item_slot(2)  # X-pot
    if slot != 255:
        logger.warning("THROWING HI-POTION")
        _use_healing_item(num=20, direction='u',item_id=2)
        return
    '''
    logger.warning("NO HEALING ITEMS!!! (they don't work here)")
    CurrentPlayer().defend()

def lulu_overdrive_demo(version="short"):
    if version == "short":
        spell_pos = 0
    else:
        spell_pos = 9
    od_completed = False
    while not memory.main.battle_active():
        pass
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if not Kimahri.active():
                buddy_swap(Kimahri)
            elif Kimahri.is_turn():
                lulu_overdrive_heal()
            elif not Auron.active():
                buddy_swap(Auron)
            elif Auron.is_turn():
                lulu_overdrive_heal()
            elif Lulu.is_turn():
                if Lulu.overdrive_percent() == 100:
                    Lulu.overdrive(spell_pos=spell_pos)
                    if spell_pos == 0:
                        od_completed=True
                    elif spell_pos in [8,9,10,11]:
                        spell_pos = 13
                    elif spell_pos == 13:
                        spell_pos = 17
                    elif spell_pos == 17:
                        spell_pos = 18
                    else:
                        od_completed=True
                else:
                    Lulu.attack()
            elif not Lulu.active():
                buddy_swap(Lulu)
            elif od_completed:
                flee_all()
            else:
                lulu_overdrive_heal()
    wrap_up()


def bribe_battle(spare_change_value: int = 12000):
    logger.debug(f"value (2): {spare_change_value}")
    first_attempt = True
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Lulu.is_turn():
                bribe(spare_change_value=spare_change_value)
                spare_change_value = max(spare_change_value/50, 2000)
            elif not Lulu.active():
                buddy_swap(Lulu)
            else:
                CurrentPlayer().defend()
    logger.debug("Battle is complete.")
    wrap_up()
    logger.debug("Now back in control.")

def distiller_and_killer(distiller_num:int=16, skip_throw:bool = False):
    memory.main.wait_seconds(1)
    logger.debug("Starting distiller fight")
    slot = memory.main.get_throw_items_slot(distiller_num)
    logger.debug(f"Distiller {distiller_num} is in slot {slot}")
    item_thrown = skip_throw
    while not memory.main.battle_wrap_up_active():
        if memory.main.turn_ready():
            if not item_thrown:
                while memory.main.main_battle_menu():
                    if memory.main.battle_menu_cursor() != 1:
                        xbox.tap_down()
                    else:
                        xbox.tap_b()
                while memory.main.main_battle_menu():
                    xbox.tap_b()
                logger.debug(f"Position: {slot}")
                _navigate_to_position(slot)
                while memory.main.other_battle_menu():
                    xbox.tap_b()
                tap_targeting()
                item_thrown = True
            elif Tidus.is_turn() and Tidus.has_overdrive():
                Tidus.overdrive()
            elif Wakka.is_turn() and Wakka.has_overdrive():
                Wakka.overdrive(reels="attack")
            else:
                CurrentPlayer().attack()
    wrap_up()

def dark_aeon(backup_aeon:int=0):
    logger.debug("Starting Dark Yojimbo fight")
    aim_count = 0
    aeon_num = backup_aeon
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Wakka.is_turn():
                if Wakka.has_overdrive():
                    Wakka.overdrive(reels="attack")
                # elif not Wakka.has_auto_life():
                #     Wakka.cast_white_magic_spell_by_name(
                #         spell_name="Auto-Life",
                #         target_id=4
                #     )
                elif Lulu.is_dead():
                    revive_target(target=5)
                elif Yuna.is_dead():
                    revive_target(target=1)
                # elif aim_count < 5:
                #     Wakka.aim()
                #     aim_count += 1
                else:
                    Wakka.defend()
            elif Lulu.is_turn():
                if not Lulu.has_auto_life():
                    Lulu.cast_white_magic_spell_by_name(
                        spell_name="Auto-Life",
                        target_id=5
                    )
                elif Wakka.is_dead():
                    revive_target(target=4)
                elif Yuna.is_dead():
                    revive_target(target=1)
                elif Lulu.has_overdrive() and not Wakka.has_overdrive():
                    Tidus.entrust(target_character=4)
                elif not Wakka.has_auto_life():
                    Lulu.cast_white_magic_spell_by_name(
                        spell_name="Auto-Life",
                        target_id=4
                    )
                elif not Yuna.has_auto_life():
                    Lulu.cast_white_magic_spell_by_name(
                        spell_name="Auto-Life",
                        target_id=1
                    )
                # elif Tidus.has_overdrive():
                #     Tidus.overdrive()
                else:
                    Lulu.defend()
            elif Yuna.is_turn():
                enemy_od = memory.main.get_overdrive_battle(20)
                logger.manip(f"Enemy OD: {enemy_od}")
                if enemy_od == 100 and aeon_num != 99:
                    aeon_summon(aeon_num)
                    aeon_num += 1
                elif not Yuna.has_auto_life():
                    Yuna.cast_white_magic_spell_by_name(
                        spell_name="Auto-Life",
                        target_id=1
                    )
                elif Lulu.is_dead():
                    revive_target(target=5)
                elif Wakka.is_dead():
                    revive_target(target=4)
                elif Yuna.has_overdrive() and not Wakka.has_overdrive():
                    Yuna.entrust(4)
                # elif Yuna.has_overdrive() and not Tidus.has_overdrive():
                #     Yuna.entrust(0)
                elif not Lulu.has_auto_life():
                    Yuna.cast_white_magic_spell_by_name(
                        spell_name="Auto-Life",
                        target_id=5
                    )
                elif not Wakka.has_auto_life():
                    Yuna.cast_white_magic_spell_by_name(
                        spell_name="Auto-Life",
                        target_id=4
                    )
                # else:
                #     Yuna.cast_white_magic_spell_by_name(
                #         spell_name="Haste",
                #         target_id=4
                #     )
                else:
                    Yuna.defend()
            elif screen.turn_aeon():
                CurrentPlayer().attack()
            elif not Wakka.active():
                buddy_swap(Wakka)
            elif not Yuna.active():
                buddy_swap(Yuna)
            elif not Lulu.active():
                buddy_swap(Lulu)
            else:
                CurrentPlayer().attack()
        if memory.main.game_over():
            logger.warning(f"Dark Yojimbo battle is over (fail)")
            return backup_aeon
    logger.warning(f"Dark Yojimbo battle is over (success)")
    if not memory.main.game_over():
        wrap_up()
        return aeon_num
    return backup_aeon