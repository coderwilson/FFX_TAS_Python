import logging

from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

import battle.overdrive
import battle.utils
import logs
import memory.main
import rng_track
import screen
import vars
import xbox
from memory.main import s32

game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()

logger = logging.getLogger(__name__)


def tap_targeting():
    logger.debug(
        f"In Tap Targeting. Not battle menu: {not memory.main.main_battle_menu()}, Battle active: {memory.main.battle_active()}"
    )
    while (not memory.main.main_battle_menu()) and memory.main.battle_active():
        xbox.tap_b()
    logger.debug(
        f"Done. Not battle menu: {not memory.main.main_battle_menu()}, Battle active: {memory.main.battle_active()}"
    )


def defend():
    logger.debug("Defending")
    for _ in range(5):
        xbox.tap_y()


def tidus_flee():
    if memory.main.battle_active():
        logger.debug("Tidus Flee (or similar command pattern)")
        while memory.main.battle_menu_cursor() != 20:
            if memory.main.battle_menu_cursor() == 255:
                xbox.tap_up()
            elif memory.main.battle_menu_cursor() == 1:
                xbox.tap_up()
            elif memory.main.battle_menu_cursor() > 20:
                xbox.tap_up()
            else:
                xbox.tap_down()
            if memory.main.other_battle_menu():
                xbox.tap_a()
        logger.debug("Out")
        while not memory.main.other_battle_menu():
            xbox.tap_b()
        _navigate_to_position(0)
        while memory.main.other_battle_menu():
            xbox.tap_b()
        tap_targeting()


def yuna_cure_omnis():
    while memory.main.battle_menu_cursor() != 22:
        if not screen.turn_yuna():
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
        if not screen.turn_tidus():
            logger.debug("Attempting Haste, but it's not Tidus' turn")
            xbox.tap_up()
            xbox.tap_up()
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
    if target != 20 and memory.main.get_enemy_current_hp()[target - 20] != 0:
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
        logs.write_rng_track("Battle: " + str(memory.main.get_encounter_id()))
        logs.write_rng_track("Story flag: " + str(memory.main.get_story_progress()))
    if memory.main.get_throw_items_slot(item_num) > 250:
        attack("none")
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
    if memory.main.battle_target_id() != 0:
        while memory.main.battle_target_id() != 0:
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
    import rng_track

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
    logger.debug("#############################################")
    logger.debug(
        f"### Advances updated: {t_strike_results} | {yellows} | {advances} ###"
    )
    logger.debug("#############################################")
    return advances


@battle.utils.speedup_decorator
def piranhas():
    encounter_id = memory.main.get_encounter_id()
    logger.debug("#########Seed: {memory.main.rng_seed()}")
    # 11 = two piranhas
    # 12 = three piranhas with one being a triple formation (takes two hits)
    # 13 = four piranhas
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if memory.main.rng_seed() == 105:
                attack("none")
            elif encounter_id == 11 or (
                encounter_id == 12 and memory.main.battle_type() == 1
            ):
                attack("none")
            else:
                escape_all()
    memory.main.click_to_control()


@battle.utils.speedup_decorator
def besaid():
    logger.info("Fight start: Besaid battle")
    FFXC.set_neutral()
    while not memory.main.turn_ready():
        pass
    battle_format = memory.main.get_encounter_id()
    logger.debug(f"Besaid battle format number: {battle_format}")
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            enemy_hp = memory.main.get_enemy_current_hp()
            logger.debug(f"Enemy HP: {enemy_hp}")
            if screen.turn_yuna():
                buddy_swap_wakka()
            elif memory.main.get_encounter_id() == 27:
                if screen.turn_lulu():
                    thunder_target(22, "l")
                elif screen.turn_wakka():
                    attack_by_num(20, direction="r")
                elif screen.turn_tidus():
                    attack_by_num(21, direction="r")
            else:
                if screen.turn_lulu():
                    thunder_target(21, "l")
                else:
                    attack()
    memory.main.click_to_control_3()


@battle.utils.speedup_decorator
def lancet_tutorial():
    logger.info("Fight start: Lancet tutorial fight (Kilika)")
    xbox.click_to_battle()
    lancet("none")

    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if screen.turn_tidus():
                attack("none")
            elif screen.turn_kimahri():
                buddy_swap_yuna()
                defend()
            elif screen.turn_lulu():
                fire("none")
            else:
                defend()
    memory.main.click_to_control()


@battle.utils.speedup_decorator
def kilika_woods(valefor_charge=True, best_charge: int = 99, next_battle=[]):
    logger.info("Fight start: Kilika battle")
    logger.debug(f"Formation: {next_battle}")
    skip_charge = False
    turn_counter = 0
    enc_id = memory.main.get_encounter_id()
    logger.debug(f"Charge values: {memory.main.overdrive_state()}")
    screen.await_turn()

    FFXC.set_neutral()

    # These battles we want nothing to do with.
    if enc_id == 32:
        skip_charge = True
    # Only occurs if no best charge possible in the first three battles.
    elif best_charge == 99:
        best_charge = enc_id

    logger.info("Kilika battle")
    aeon_turn = False
    yuna_went = False
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():  # AKA end of battle screen
        if (
            not valefor_charge and not skip_charge and best_charge == next_battle
        ):  # Still to charge Valefor
            if memory.main.turn_ready():
                logger.debug("------------------------------")
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
                elif screen.turn_kimahri() or screen.turn_lulu():
                    if memory.main.get_battle_char_slot(4) >= 3:
                        buddy_swap_wakka()
                    elif memory.main.get_battle_char_slot(0) >= 3:
                        buddy_swap_tidus()
                    else:
                        buddy_swap_yuna()
                elif enc_id == 31:  # Working just fine.
                    logger.debug("Logic for battle number 31")
                    if screen.turn_tidus():
                        attack("none")
                    elif screen.turn_yuna():
                        aeon_summon(0)
                        screen.await_turn()
                        if not aeon_turn:
                            aeon_turn = True
                            if memory.main.get_next_turn() < 20:
                                aeon_shield()
                        aeon_boost()
                        screen.await_turn()
                        aeon_boost()
                        screen.await_turn()
                        aeon_spell(2)
                    elif screen.turn_aeon():
                        aeon_spell_direction(2, "right")
                    else:
                        defend()
                elif enc_id == 33:
                    logger.debug("Logic for battle number 33")
                    if screen.turn_yuna():

                        aeon_summon(0)
                        screen.await_turn()
                        if not aeon_turn:
                            aeon_turn = True
                            if memory.main.get_next_turn() < 20:
                                aeon_shield()
                        aeon_boost()
                        screen.await_turn()
                        aeon_spell_direction(1, "left")
                    elif screen.turn_aeon():
                        aeon_spell(2)
                    else:
                        defend()

                elif enc_id == 34:
                    logger.debug("Logic for battle number 34")
                    if screen.turn_tidus():
                        attack("none")
                    elif screen.turn_yuna():
                        aeon_summon(0)
                        screen.await_turn()
                        if not aeon_turn:
                            aeon_turn = True
                            if memory.main.get_next_turn() < 20:
                                aeon_shield()
                        aeon_boost()
                        screen.await_turn()
                        aeon_spell_direction(1, "right")
                    elif screen.turn_aeon():
                        aeon_spell_2(2, "left")
                    else:
                        defend()
                elif enc_id == 35:
                    logger.debug("Logic for battle number 35")
                    if screen.turn_tidus():
                        defend()
                    elif screen.turn_yuna():
                        aeon_summon(0)
                        screen.await_turn()
                        if not aeon_turn:
                            aeon_turn = True
                            if memory.main.get_next_turn() < 20:
                                aeon_shield()
                        aeon_boost()
                        screen.await_turn()
                        sonic_wings()
                        screen.await_turn()
                        aeon_spell(0)
                    elif screen.turn_aeon():
                        aeon_spell(0)
                    else:
                        defend()
                elif enc_id == 37:
                    logger.debug(
                        "Logic for battle number 37 - two bees and a plant thingey"
                    )
                    if screen.turn_tidus():
                        attack("none")
                    elif screen.turn_yuna():
                        aeon_summon(0)
                        screen.await_turn()
                        if not aeon_turn:
                            aeon_turn = True
                            if memory.main.get_next_turn() < 20:
                                aeon_shield()
                        aeon_spell_direction(1, "right")
                        screen.await_turn()
                        aeon_spell_direction(1, "right")
                    elif screen.turn_aeon():
                        while not memory.main.battle_complete():
                            if memory.main.turn_ready():
                                aeon_spell(0)
                    else:
                        defend()
                else:
                    skip_charge = True
                    logger.debug(f"Not going to charge Valefor. Battle num: {enc_id}")
        else:
            if memory.main.turn_ready():
                logger.debug("------------------------------")
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
                elif screen.turn_kimahri():
                    if memory.main.get_battle_char_slot(4) >= 3:
                        buddy_swap_wakka()
                    elif memory.main.get_battle_char_slot(0) >= 3:
                        buddy_swap_tidus()
                    else:
                        buddy_swap_yuna()
                elif screen.turn_lulu() and enc_id != 37:
                    if memory.main.get_battle_char_slot(4) >= 3:
                        buddy_swap_wakka()
                    elif memory.main.get_battle_char_slot(0) >= 3:
                        buddy_swap_tidus()
                    else:
                        buddy_swap_yuna()
                elif enc_id == 31:
                    if screen.turn_tidus():
                        if turn_counter < 4:
                            attack_by_num(num=20, direction="l")
                        # If Wakka crit, we can use that instead. Slightly faster.
                        else:
                            flee_all()
                    elif (
                        screen.turn_wakka()
                        and memory.main.get_enemy_current_hp()[0] != 0
                    ):
                        attack_by_num(num=20, direction="l")
                    else:
                        defend()
                elif enc_id == 32:
                    if screen.turn_tidus():
                        if turn_counter < 4:
                            attack_by_num(20, "r")
                        else:
                            flee_all()
                    elif screen.turn_wakka():
                        attack_by_num(21, "r")
                    else:
                        defend()
                elif enc_id == 33:
                    if screen.turn_tidus():
                        if turn_counter < 4:
                            defend()
                        else:
                            flee_all()
                    elif screen.turn_wakka():
                        attack_by_num(21, "r")
                    else:
                        defend()
                elif enc_id == 34:
                    if screen.turn_tidus():
                        if turn_counter < 4:
                            attack("none")
                        else:
                            flee_all()
                    elif screen.turn_wakka():
                        attack_by_num(22, "r")
                    else:
                        defend()
                elif enc_id == 35 or enc_id == 36:
                    flee_all()
                elif enc_id == 37:
                    if memory.main.get_speed() >= 16:
                        flee_all()
                    elif yuna_went:
                        flee_all()
                    elif (
                        screen.turn_wakka()
                        and memory.main.get_enemy_current_hp()[2] != 0
                    ):
                        attack_by_num(22, "l")
                        yuna_went = True
                    elif screen.turn_yuna():
                        buddy_swap_lulu()
                        thunder_target(target=21, direction="l")
                    else:
                        defend()
    FFXC.set_neutral()
    memory.main.click_to_control()  # Rewards screen
    hp_check = memory.main.get_hp()
    if hp_check[0] < 250 or hp_check[1] < 250 or hp_check[4] < 250:
        heal_up(3)
    else:
        logger.debug("No need to heal up. Moving onward.")
    if not valefor_charge and memory.main.overdrive_state()[8] == 20:
        valefor_charge = True
    logger.debug(f"Returning Valefor Charge value: {valefor_charge}")
    return valefor_charge


def sonic_wings():
    logger.debug("Valefor attempting to use Sonic Wings - 1")
    while memory.main.battle_menu_cursor() != 204:
        if memory.main.battle_menu_cursor() == 203:
            xbox.tap_down()
        else:
            xbox.tap_up()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    logger.debug("Valefor attempting to use Sonic Wings - 2")


@battle.utils.speedup_decorator
def luca_workers():
    logger.info("Fight start: Workers in Luca")
    xbox.click_to_battle()

    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if screen.turn_kimahri() or screen.turn_tidus():
                if screen.faint_check() >= 1:
                    revive()
                else:
                    defend()
            if screen.turn_lulu():
                thunder("none")
        elif memory.main.diag_skip_possible():
            xbox.tap_b()  # Clicking to get through the battle faster
    memory.main.click_to_control()


@battle.utils.speedup_decorator
def luca_workers_2(early_haste):
    logger.info("Fight start: Workers in Luca")
    hasted = False
    xbox.click_to_battle()

    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if screen.faint_check() >= 1:
                revive()
            elif early_haste >= 1:
                if screen.turn_tidus() and not hasted:
                    tidus_haste("left", character=5)
                    hasted = True
                elif screen.turn_lulu():
                    thunder("none")
                else:
                    defend()
            elif memory.main.luca_workers_battle_id() in [44, 35]:
                if screen.turn_tidus():
                    attack("none")
                elif screen.turn_kimahri():
                    if (
                        memory.main.get_enemy_current_hp().count(0) == 1
                        and memory.main.get_overdrive_battle(3) == 100
                        and memory.main.get_enemy_current_hp()[0] > 80
                    ):
                        battle.overdrive.kimahri(1)
                    else:
                        attack("none")
                elif screen.turn_lulu():
                    thunder("right")
            else:
                if screen.turn_lulu():
                    thunder("none")
                else:
                    defend()
        elif memory.main.diag_skip_possible():
            xbox.tap_b()  # Clicking to get through the battle faster
    memory.main.click_to_control()


@battle.utils.speedup_decorator
def after_blitz_1(early_haste):
    logger.info("Fight start: After Blitzball (the fisheys)")
    logger.debug(f"Early haste: {early_haste}")
    if early_haste != -1:
        screen.await_turn()

        # Tidus haste self
        tidus_haste("none")
    wakka_turns = 0

    while not memory.main.battle_complete():
        if memory.main.turn_ready():
            logger.debug(f"Enemy HP: {memory.main.get_enemy_current_hp()}")
            if screen.turn_tidus():
                attack("none")
            else:
                wakka_turns += 1
                hp_values = memory.main.get_battle_hp()
                if wakka_turns < 3:
                    attack_by_num(22, "l")
                elif hp_values[1] < 200:  # Tidus HP
                    use_potion_character(0, "u")
                elif hp_values[0] < 100:  # Wakka HP
                    use_potion_character(4, "u")
                else:
                    defend()


@battle.utils.speedup_decorator
def after_blitz_3(early_haste):
    logger.info("Ready to take on Garuda")
    logger.debug(f"Early haste: {early_haste}")
    # Wakka dark attack, or Auron power break
    screen.await_turn()
    tidus_turn = 0
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():
        while not memory.main.turn_ready():
            pass
        hp_values = memory.main.get_battle_hp()
        if screen.turn_auron():
            logger.debug("Auron Turn")
            attack("none")
        elif screen.turn_tidus():
            logger.debug(f"Tidus Turn: {tidus_turn}")
            if tidus_turn == 0:
                tidus_haste("d", character=2)
                tidus_turn += 1
            elif tidus_turn == 1:
                attack("none")
                tidus_turn += 1
            elif hp_values[0] < 202:
                use_potion_character(2, "u")
            else:
                defend()
        elif screen.turn_wakka():
            logger.debug("Wakka Turn")
            if hp_values[0] < 202 and (
                memory.main.get_next_turn() != 2
                or memory.main.get_enemy_current_hp()[0] > 268
            ):
                use_potion_character(2, "u")
            elif hp_values[1] < 312 and tidus_turn < 2:
                use_potion_character(0, "u")
            else:
                defend()
    FFXC.set_value("btn_b", 1)
    memory.main.wait_frames(30 * 4)
    FFXC.set_value("btn_b", 0)
    logger.info("Battle complete (Garuda)")
    # Get to control
    while not memory.main.user_control():
        if memory.main.cutscene_skip_possible():
            while not memory.main.diag_progress_flag() == 1:
                if memory.main.cutscene_skip_possible():
                    xbox.skip_scene()
            if game_vars.csr():
                memory.main.wait_frames(60)
            else:
                xbox.await_save(index=1)
        elif memory.main.diag_skip_possible() or memory.main.menu_open():
            xbox.tap_b()


@battle.utils.speedup_decorator
def after_blitz_3_late_haste(early_haste):
    logger.info("Ready to take on Zu")
    logger.debug(f"Early haste: {early_haste}")
    # Wakka dark attack, or Auron power break
    screen.await_turn()
    if screen.turn_auron():
        logger.debug("Auron's turn")
        use_skill(0)
    elif screen.turn_tidus():
        logger.debug("Tidus' turn")
        if early_haste != -1:
            tidus_haste("up")
        else:
            attack("none")
    else:
        logger.debug("Wakkas turn")
        use_skill(0)
    screen.await_turn()
    if screen.turn_auron():
        use_skill(0)
    elif screen.turn_tidus():
        if early_haste != -1:
            tidus_haste("up")
        else:
            attack("none")
    else:
        use_skill(0)
    screen.await_turn()
    if screen.turn_auron():
        use_skill(0)
    else:
        use_skill(0)

    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if screen.faint_check() > 0:
                revive()
            else:
                attack("none")
    FFXC.set_value("btn_b", 1)
    memory.main.wait_frames(30 * 4)
    FFXC.set_value("btn_b", 0)
    logger.info("Battle complete (Garuda)")
    # Get to control
    while not memory.main.user_control():
        if memory.main.cutscene_skip_possible():
            while not memory.main.diag_progress_flag() == 1:
                if memory.main.cutscene_skip_possible():
                    xbox.skip_scene()
            if game_vars.csr():
                memory.main.wait_frames(60)
            else:
                xbox.await_save(index=1)
        elif memory.main.diag_skip_possible() or memory.main.menu_open():
            xbox.tap_b()


@battle.utils.speedup_decorator
def miihen_road(self_destruct=False):
    logger.info("Fight start: Mi'ihen Road")
    logger.debug(f"Mi'ihen battle. Self-destruct: {game_vars.self_destruct_get()}")
    encounter_id = memory.main.get_encounter_id()

    while not memory.main.battle_complete():  # AKA end of battle screen
        if memory.main.battle_type() == 2 and not check_tidus_ok():
            logger.info("Looks like we got ambushed. Skipping this battle.")
            flee_all()
            break
        if memory.main.turn_ready():
            if screen.turn_tidus():
                if not game_vars.self_destruct_get():
                    if encounter_id in [51, 64, 66, 87]:
                        lancet_swap("none")
                        game_vars.self_destruct_learned()
                        break
                    elif encounter_id == 65 or encounter_id == 84:
                        lancet_swap("right")
                        game_vars.self_destruct_learned()
                        break
                    else:
                        flee_all()
                else:
                    flee_all()
            else:
                flee_all()

    FFXC.set_movement(0, 1)
    while not memory.main.user_control():
        FFXC.set_value("btn_b", 1)
        memory.main.wait_frames(2)
        FFXC.set_value("btn_b", 0)
        memory.main.wait_frames(3)

    logger.debug(f"self_destruct flag: {game_vars.self_destruct_get()}")


def aeon_shield():
    logger.info("Aeon Shield function")
    screen.await_turn()
    memory.main.wait_frames(6)
    while not memory.main.other_battle_menu():
        xbox.tap_right()
    if game_vars.use_pause():
        memory.main.wait_frames(2)
    while memory.main.other_battle_menu():
        if memory.main.battle_cursor_2() == 0:
            xbox.tap_b()
        else:
            xbox.tap_up()
    tap_targeting()


def aeon_boost():
    logger.info("Aeon Boost function")
    screen.await_turn()
    memory.main.wait_frames(6)
    while not memory.main.other_battle_menu():
        xbox.tap_right()
    if game_vars.use_pause():
        memory.main.wait_frames(2)
    while memory.main.other_battle_menu():
        if memory.main.battle_cursor_2() == 1:
            xbox.tap_b()
        elif memory.main.battle_cursor_2() == 0:
            xbox.tap_down()
        else:
            xbox.tap_up()
    tap_targeting()


def aeon_dismiss():
    logger.info("Aeon Dismiss function")
    screen.await_turn()
    memory.main.wait_frames(6)
    while not memory.main.other_battle_menu():
        xbox.tap_right()
    if game_vars.use_pause():
        memory.main.wait_frames(2)
    while memory.main.other_battle_menu():
        if memory.main.battle_cursor_2() == 2:
            xbox.tap_b()
        else:
            xbox.tap_down()
    tap_targeting()


def mrr_target():
    enc_id = memory.main.get_encounter_id()
    if enc_id == 96:
        attack_by_num(22, "r")
    elif enc_id == 97:
        attack_by_num(20, "r")
    elif enc_id == 98:
        lancet_target(target=21, direction="d")
    elif enc_id == 101:
        lancet_target(target=21, direction="l")
    elif enc_id in [100, 110]:
        attack_by_num(22, "l")
    elif enc_id in [102, 112, 113]:
        attack_by_num(20, "l")
    elif enc_id in [109, 111]:
        lancet_target(target=20, direction="l")
    else:
        defend()
    return memory.main.next_crit(character=3, char_luck=18, enemy_luck=15)


@battle.utils.speedup_decorator
def mrr_battle(status):
    # Yuna complete, Kimahri complete, Valefor overdrive, Battle counter, Yuna level up complete, Yuna grid, phase
    logger.info("------------------------------")
    logger.info("------------------------------")
    logger.info("Fight start: MRR")
    encounter_id = memory.main.get_encounter_id()
    logger.info(f"Battle number: {encounter_id}")
    # next_crit_kim = memory.next_crit(character=3, char_luck=18, enemy_luck=15)

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

    # If we're ambushed and take too much damage, this will trigger first.
    hp_array = memory.main.get_battle_hp()
    hp_total = hp_array[0] + hp_array[1] + hp_array[2]
    # Final charging for Yuna is a lower overall party HP
    if hp_total < 1800 and status[5] != 2:
        logger.info("----- We got ambushed. Not going to attempt to recover.")
        flee_all()
    elif screen.faint_check() >= 1:
        logger.info("--- Character is dead from the start of battle -> Escaping")
        flee_all()
    elif check_petrify():
        logger.warning("--- Character petrified. Unhandled case -> Escaping")
        flee_all()
    elif encounter_id == 102:  # Garuda, flee no matter what.
        flee_all()
    elif status[5] == 0:  # Phase zero - use Valefor overdrive to overkill for levels
        if status[3] < 3 and memory.main.rng_seed() != 160:
            # Battle number (zero-index)
            if (
                encounter_id == 100 or encounter_id == 101
            ):  # The two battles with Funguar
                while memory.main.battle_active():  # end of battle screen
                    if memory.main.turn_ready():
                        if check_petrify():
                            logger.warning(
                                "--- Character petrified. Unhandled case -> Escaping"
                            )
                            flee_all()
                        elif screen.turn_tidus():
                            buddy_swap_kimahri()
                        elif screen.turn_kimahri():
                            # if next_crit_kim > 9 - status[3] and next_crit_kim < 23 - (status[3] * 2):
                            #    next_crit_kim = mrr_target()
                            # else:
                            defend()
                        elif screen.turn_wakka():
                            defend()
                        else:
                            buddy_swap_yuna()
                            aeon_summon(0)
                            screen.await_turn()
                            battle.overdrive.valefor(version=1)
                            status[2] = 1
                            status[5] = 1
            else:
                flee_all()
        else:  # Starting with fourth battle, overdrive on any battle that isn't Garuda.
            while memory.main.battle_active():  # end of battle screen
                if memory.main.turn_ready():
                    if check_petrify():
                        logger.warning(
                            "--- Character petrified. Unhandled case -> Escaping"
                        )
                        flee_all()
                    elif screen.turn_tidus():
                        buddy_swap_kimahri()
                    elif screen.turn_kimahri():
                        # if next_crit_kim > 9 - status[3] and next_crit_kim < 23 - (status[3] * 2):
                        #     next_crit_kim = mrr_target()
                        # else:
                        defend()
                    elif screen.turn_wakka():
                        defend()
                    else:
                        buddy_swap_yuna()
                        aeon_summon(0)
                        screen.await_turn()
                        battle.overdrive.valefor(version=1)
                        status[2] = 1
                        status[5] = 1
    elif status[5] == 1:  # Next need to recharge Valefor
        valefor_charge_complete = True
        if memory.main.battle_type() == 1:
            for _ in range(3):
                screen.await_turn()
                defend()
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
                        if screen.turn_tidus():
                            buddy_swap_kimahri()
                            next_crit_kim = mrr_target()
                        elif screen.turn_wakka():
                            wakka_turns += 1
                            if wakka_turns == 1:
                                attack_by_num(21, "l")
                            else:
                                buddy_swap_yuna()
                                aeon_summon(0)
                        elif screen.turn_auron():
                            attack_by_num(22, "r")
                        elif screen.turn_kimahri():
                            buddy_swap_yuna()
                            aeon_summon(0)
                        elif screen.turn_aeon():
                            if aeon_turn == 0 and memory.main.get_next_turn() < 19:
                                aeon_boost()
                                aeon_turn = 1
                            elif aeon_turn < 2:
                                aeon_boost()
                                screen.await_turn()
                                attack("none")
                                aeon_turn = 2
                            else:
                                aeon_spell_2(3, "none")
        elif encounter_id == 97:  # Lamashtu, Gandarewa, Red Element (camera front)
            while memory.main.battle_active():  # end of battle screen
                if memory.main.turn_ready():
                    if check_petrify():
                        logger.warning(
                            "--- Character petrified. Unhandled case -> Escaping"
                        )
                        flee_all()
                    elif screen.turn_tidus():
                        buddy_swap_kimahri()
                        next_crit_kim = mrr_target()
                    elif screen.turn_wakka():
                        defend()
                    elif screen.turn_auron():
                        attack("none")
                    elif screen.turn_kimahri():
                        buddy_swap_yuna()
                        aeon_summon(0)
                    elif screen.turn_aeon():
                        if aeon_turn == 0 and memory.main.get_next_turn() < 19:
                            screen.await_turn()
                            aeon_boost()
                            aeon_turn = 1
                        elif aeon_turn < 2:
                            aeon_spell(2)
                            screen.await_turn()
                            aeon_boost()
                            aeon_turn = 2
                        else:
                            aeon_spell(3)
        elif encounter_id == 98:  # Raptor, Red Element, Gandarewa (camera side)
            while memory.main.battle_active():  # end of battle screen
                if memory.main.turn_ready():
                    if check_petrify():
                        logger.info("Someone is pretrified. Escaping battle.")
                        flee_all()
                        valefor_charge_complete = False
                    else:
                        logger.debug("No petrify issues.")
                        if screen.turn_tidus():
                            buddy_swap_kimahri()
                        elif screen.turn_kimahri():
                            next_crit_kim = mrr_target()
                        elif screen.turn_wakka():
                            attack("none")
                        elif screen.turn_auron():
                            buddy_swap_yuna()
                            aeon_summon(0)
                        elif screen.turn_aeon():
                            if aeon_turn == 0 and memory.main.get_next_turn() < 19:
                                aeon_boost()
                                aeon_turn = 1
                            elif aeon_turn < 2:
                                aeon_spell_2(2, "right")
                                screen.await_turn()
                                aeon_boost()
                                aeon_turn = 2
                            else:
                                aeon_spell_2(3, "right")
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
                        if screen.turn_tidus():
                            buddy_swap_kimahri()
                            # if next_crit_kim > 9 - status[3] and next_crit_kim < 23 - (status[3] * 2):
                            #     next_crit_kim = mrr_target()
                            # else:
                            defend()
                        elif screen.turn_wakka():
                            attack("none")
                        elif memory.main.get_enemy_current_hp()[0] != 0:
                            buddy_swap_tidus()
                            flee_all()
                            valefor_charge_complete = False
                        elif screen.turn_auron():
                            buddy_swap_yuna()
                            aeon_summon(0)
                        elif screen.turn_aeon():
                            if aeon_turn == 0 and memory.main.get_next_turn() < 19:
                                screen.await_turn()
                                aeon_boost()
                                aeon_turn = 1
                            elif aeon_turn < 2:
                                aeon_spell(0)
                                screen.await_turn()
                                aeon_boost()
                                aeon_turn = 2
                            else:
                                aeon_spell(3)
        # Funguar, Red Element, Gandarewa (camera reverse angle)
        elif encounter_id == 101:
            while memory.main.battle_active():  # end of battle screen
                if memory.main.turn_ready():
                    if check_petrify():
                        logger.warning(
                            "--- Character petrified. Unhandled case -> Escaping"
                        )
                        flee_all()
                    elif screen.turn_tidus():
                        buddy_swap_kimahri()
                        next_crit_kim = mrr_target()
                    elif screen.turn_wakka():
                        attack_by_num(22, "l")
                    elif memory.main.get_enemy_current_hp()[2] != 0:
                        buddy_swap_tidus()
                        flee_all()
                        valefor_charge_complete = False
                    elif screen.turn_auron():
                        buddy_swap_yuna()
                        aeon_summon(0)
                    elif screen.turn_aeon():
                        if aeon_turn == 0 and memory.main.get_next_turn() < 19:
                            aeon_boost()
                            aeon_turn = 1
                        elif aeon_turn < 2:
                            aeon_spell(0)
                            screen.await_turn()
                            aeon_boost()
                            aeon_turn = 2
                        else:
                            aeon_spell(3)
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
            while memory.main.battle_active():  # end of battle screen
                if memory.main.turn_ready():
                    if check_petrify():
                        logger.warning(
                            "--- Character petrified. Unhandled case -> Escaping"
                        )
                        flee_all()
                    elif screen.turn_tidus():
                        tidus_flee()
                    elif screen.faint_check() >= 1:
                        buddy_swap_tidus()
                    elif screen.turn_kimahri():
                        if memory.main.get_kimahri_slvl() >= 6 and yuna_turn_count:
                            # if next_crit_kim > 9 - status[3] and next_crit_kim < 23 - (status[3] * 2):
                            #     next_crit_kim = mrr_target()
                            # else:
                            flee_all()
                        else:
                            defend()
                    elif screen.turn_yuna():
                        yuna_turn_count += 1
                        if yuna_turn_count == 1:
                            defend()
                        else:
                            flee_all()
                    elif screen.turn_wakka():
                        if encounter_id in [96, 97, 101]:
                            if encounter_id == 101:
                                attack_by_num(22, "l")
                            else:
                                attack_by_num(21, "l")
                        elif encounter_id == 98 or encounter_id == 100:
                            attack("none")
                        else:
                            flee_all()
                    else:  # Should not occur, but you never know.
                        buddy_swap_tidus()
    else:  # Everything is done.
        flee_all()
    logger.debug("+++")
    logger.debug(f"Wakka late menu: {game_vars.wakka_late_menu()}")
    logger.debug("+++")
    # OK the battle should be complete now. Let's do some wrap-up stuff.
    wrap_up()

    # Check on sphere levels for our two heroes
    if status[0] == 0:
        if memory.main.get_slvl_yuna() > 573:
            status[0] = 1
    if status[1] == 0:
        if memory.main.get_slvl_kim() >= 495:
            status[1] = 1
    if status[5] == 2:  # Last phase is to level Yuna and Kimahri
        # Both Yuna and Kimahri have levels, good to go.
        if status[0] == 1 and status[1] == 1:
            status[5] = 3

    if status[5] == 3:
        memory.main.full_party_format("mrr1", full_menu_close=False)
    elif status[5] == 2:  # Still levelling Yuna or Kimahri
        memory.main.full_party_format("mrr2", full_menu_close=False)
        logger.debug("Yuna in front party, trying to get some more experience.")
    else:
        memory.main.full_party_format("mrr1", full_menu_close=False)

    # Now checking health values
    hp_check = memory.main.get_hp()
    logger.debug(f"HP values: {hp_check}")
    if status[5] == 2:
        heal_up(3, full_menu_close=False)
    elif hp_check != [520, 475, 1030, 644, 818, 380]:
        heal_up(full_menu_close=False)
    # donezo. Back to the main path.
    logger.debug("Clean-up is now complete.")
    return status


def _mrr_manip_kimahri_crit():
    next_crit_kim = memory.main.next_crit(character=3, char_luck=18, enemy_luck=15)
    logger.debug(f"||| Manip - Battle number: {memory.main.get_encounter_id()}")
    logger.debug(f"||| Next Kimahri Crit vs Gui: {next_crit_kim}")
    return next_crit_kim


@battle.utils.speedup_decorator
def mrr_manip(kim_max_advance: int = 6):
    screen.await_turn()
    next_crit_kim = memory.main.next_crit(character=3, char_luck=18, enemy_luck=15)
    logger.debug(f"======== Next Kimahri crit: {next_crit_kim}")
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
                if 3 not in memory.main.get_active_battle_formation():
                    buddy_swap_kimahri()
                elif screen.turn_kimahri():
                    next_crit_kim = mrr_target()
                    kim_turn = False
                else:
                    defend()
            else:
                flee_all()
    wrap_up()
    # Now checking health values
    hp_check = memory.main.get_hp()
    logger.debug(f"HP values: {hp_check}")
    if hp_check != [520, 475, 1030, 644, 818, 380]:
        heal_up(full_menu_close=False)
    memory.main.full_party_format("mrr1")
    _mrr_manip_kimahri_crit()
    return attempt_manip


@battle.utils.speedup_decorator
def djose(stone_breath):
    logger.info("Fight start: Djose road")
    while not memory.main.battle_complete():  # AKA end of battle screen
        encounter_id = memory.main.get_encounter_id()
        if memory.main.turn_ready():
            if stone_breath == 1:  # Stone Breath already learned
                logger.debug("Djose: Stone breath already learned.")
                flee_all()
            else:  # Stone breath not yet learned
                if encounter_id == 128 or encounter_id == 134 or encounter_id == 136:
                    logger.info("Djose: Learning Stone Breath.")
                    lancet_swap("none")
                    stone_breath = 1
                elif encounter_id == 127:
                    logger.info("Djose: Learning Stone Breath")
                    # One basilisk with two wasps
                    lancet_swap("up")
                    stone_breath = 1
                    break
                else:
                    logger.info("Djose: Cannot learn Stone Breath here.")
                    flee_all()

    logger.debug("Mark 2")
    memory.main.click_to_control()
    logger.debug("Mark 3")
    party_hp = memory.main.get_hp()
    logger.debug(f"Party hp: {party_hp}")
    if party_hp[0] < 300 or party_hp[4] < 300:
        logger.debug("Djose: recovering HP")
        heal_up(3)
    else:
        logger.debug("Djose: No need to heal.")
    memory.main.full_party_format("djose")
    return stone_breath


@battle.utils.speedup_decorator
def mix_tutorial():
    xbox.click_to_battle()
    steal()
    xbox.click_to_battle()
    rikku_full_od("tutorial")
    memory.main.click_to_control()


@battle.utils.speedup_decorator
def thunder_plains(section):
    enc_id = memory.main.get_encounter_id()
    grenade_slot = memory.main.get_item_slot(35)
    logger.debug(f"++Grenade Slot {grenade_slot}")
    grenade_count = memory.main.get_item_count_slot(grenade_slot)
    logger.debug(f"++Grenade count: {grenade_count}")
    speed_count = memory.main.get_speed()
    logger.debug(f"++Speed sphere count: {speed_count}")
    use_grenades = grenade_count > 3 and speed_count < 14
    logger.debug(f"++Use Grenades decision: {use_grenades}")
    use_grenade_slot = memory.main.get_use_items_slot(35)
    lunar_slot = game_vars.get_blitz_win() or memory.main.get_item_slot(56) != 255
    light_slot = memory.main.get_item_slot(57) != 255
    petrify_slot = memory.main.get_item_slot(49) != 255

    tidus_turns = 0
    while not memory.main.turn_ready():
        pass

    # Petrify check is not working. Requires review.
    if check_petrify():
        logger.warning("--- Character petrified. Unhandled case -> Escaping")
        flee_all()
    elif enc_id in [152, 155, 162]:  # Any battle with Larvae
        if lunar_slot:
            # No longer need Lunar Curtain for Evrae fight, Blitz win logic.
            flee_all()
        else:  # Blitz loss strat
            logger.info(f"Battle with Larvae. Battle number: {enc_id}")
            while not memory.main.battle_complete():
                if memory.main.turn_ready():
                    if not lunar_slot and memory.main.turn_ready():
                        if screen.turn_tidus():
                            if tidus_turns == 0:
                                buddy_swap_rikku()
                            else:
                                flee_all()
                            tidus_turns += 1
                        elif screen.turn_rikku():
                            steal()
                            lunar_slot = (
                                game_vars.get_blitz_win()
                                or memory.main.get_item_slot(56) != 255
                            )
                        else:
                            buddy_swap_tidus()
                    else:
                        flee_all()
    elif enc_id == 160:
        logger.info(f"Battle with Iron Giant. Battle number: {enc_id}")
        while not memory.main.battle_complete():
            screen.await_turn()
            if light_slot:
                flee_all()
            else:
                buddy_swap_rikku()
            while not memory.main.battle_complete():
                if screen.turn_rikku():
                    if not light_slot:
                        steal()
                        light_slot = memory.main.get_item_slot(57) != 255
                    elif memory.main.get_overdrive_battle(6) < 100:
                        attack("none")
                    else:
                        flee_all()
                else:
                    if (
                        memory.main.get_overdrive_battle(6) < 100
                        and not check_rikku_ok()
                    ):
                        escape_one()
                    else:
                        flee_all()
    elif enc_id == 161:
        logger.info(
            f"Battle with Iron Giant and Buer monsters. Battle number: {enc_id}"
        )
        while not memory.main.battle_complete():
            screen.await_turn()
            if use_grenades or not light_slot:
                buddy_swap_rikku()
                grenade_thrown = False
                while not memory.main.battle_complete():
                    if memory.main.turn_ready():
                        if screen.turn_rikku():
                            if use_grenades and not grenade_thrown:
                                logger.debug(f"Grenade Slot {use_grenade_slot}")
                                use_item(use_grenade_slot, "none")
                                grenade_thrown = True
                            elif not light_slot:
                                steal()
                                light_slot = memory.main.get_item_slot(57) != 255
                            elif memory.main.get_overdrive_battle(6) < 100:
                                attack("none")
                            else:
                                flee_all()
                        else:
                            if not check_rikku_ok():
                                flee_all()
                            elif memory.main.get_overdrive_battle(6) < 100:
                                escape_one()
                            elif light_slot and (not use_grenades or grenade_thrown):
                                flee_all()
                            else:
                                defend()
            else:
                flee_all()
    elif enc_id in [154, 156, 164] and use_grenades:
        logger.info(f"Battle with random mobs including Buer. Battle number: {enc_id}")
        while not memory.main.battle_complete():
            screen.await_turn()
            if use_grenades:
                buddy_swap_rikku()
                use_item(use_grenade_slot, "none")
            flee_all()
    elif (
        not game_vars.get_blitz_win() and not petrify_slot and enc_id in [153, 154, 163]
    ):
        logger.debug("Grabbing petrify grenade. Blitz Loss only strat.")
        while not memory.main.battle_complete():
            if memory.main.turn_ready():
                if enc_id in [153, 163]:
                    if screen.turn_tidus():
                        buddy_swap_rikku()
                        screen.await_turn()
                        steal()
                    else:
                        buddy_swap_tidus()
                        screen.await_turn()
                        flee_all()
                else:
                    if screen.turn_tidus():
                        buddy_swap_rikku()
                        screen.await_turn()
                        steal_right()
                    else:
                        buddy_swap_tidus()
                        screen.await_turn()
                        flee_all()
    else:  # Nothing useful this battle. Moving on.
        flee_all()

    logger.info("Battle is ended - Thunder Plains")
    memory.main.click_to_control()
    memory.main.wait_frames(2)  # Allow lightning to attemt a strike
    if memory.main.dodge_lightning(game_vars.get_l_strike()):
        logger.debug("Dodge")
        game_vars.set_l_strike(memory.main.l_strike_count())
    logger.debug("Checking party format and resolving if needed.")
    memory.main.full_party_format("postbunyip", full_menu_close=False)
    logger.debug("Party format is good. Now checking health values.")
    hp_values = memory.main.get_hp()
    if (
        hp_values[0] < 400
        or hp_values[2] < 400
        or hp_values[4] < 400
        or hp_values[6] < 180
    ):
        heal_up()
    memory.main.close_menu()
    logger.debug("Ready to continue onward.")


@battle.utils.speedup_decorator
def m_woods():
    logger.debug("Logic depends on completion of specific goals. In Order:")
    encounter_id = memory.main.get_encounter_id()
    logger.debug(f"------------- Battle Start - Battle Number: {encounter_id}")
    need_arctic_wind, need_fish_scale = False, False
    while not memory.main.battle_complete():  # AKA end of battle screen
        if memory.main.turn_ready():
            if memory.main.get_use_items_slot(24) == 255:
                need_arctic_wind = True
            if memory.main.get_use_items_slot(32) == 255:
                need_fish_scale = True
            turn_char = memory.main.get_battle_char_turn()
            rikku_charged = memory.main.get_overdrive_battle(6) == 100
            logging.info(f"Rikku charge state: {rikku_charged}")
            if not rikku_charged:
                if (
                    need_arctic_wind
                    or need_fish_scale
                    and encounter_id in [171, 172, 175]
                ):
                    if (
                        check_petrify_tidus()
                        or 6 not in memory.main.get_battle_formation()
                    ):
                        logger.info("Tidus or Rikku incapacitated, fleeing")
                        flee_all()
                    elif 6 not in memory.main.get_active_battle_formation():
                        if encounter_id == 175 and need_arctic_wind:
                            buddy_swap_rikku()
                        elif encounter_id in [171, 172] and need_fish_scale:
                            buddy_swap_rikku()
                        else:
                            flee_all()
                    elif turn_char == 6:
                        if encounter_id == 175 and need_arctic_wind:
                            logger.debug("Marker 2")
                            steal()
                        elif encounter_id == 172 and need_fish_scale:
                            logger.debug("Marker 3")
                            steal_down()
                        elif encounter_id == 171 and need_fish_scale:
                            logger.debug("Marker 4")
                            steal_right()
                        elif memory.main.get_overdrive_battle(6) != 100:
                            logger.debug("Charging")
                            attack_by_num(6, "u")
                        else:
                            logger.debug("Escaping")
                            flee_all()
                    elif memory.main.get_overdrive_battle(6) != 100:
                        escape_one()
                    else:
                        flee_all()
                elif turn_char == 6:
                    if memory.main.next_steal_rare(pre_advance=2):
                        # Manip for crit
                        _steal()
                    else:
                        defend()
                elif 6 not in memory.main.get_active_battle_formation():
                    buddy_swap_rikku()
                else:
                    escape_one()
            elif memory.main.next_steal_rare(pre_advance=2):
                logger.debug("##Looking ahead, manip for non-crit steal")
                if 6 not in memory.main.get_active_battle_formation():
                    buddy_swap_rikku()
                    _steal()
                else:
                    flee_all()
            else:
                logger.debug("##Looking ahead, no need to manip")
                flee_all()

    logger.info("Battle complete, now to deal with the aftermath.")
    memory.main.click_to_control_3()
    logger.debug("M.woods, back in control")


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


@battle.utils.speedup_decorator
def negator_with_steal():
    tidus_turns = 0
    rikku_turns = 0
    kimahriturns = 0
    luluturns = 0
    yunaturns = 0
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            turn_char = memory.main.get_battle_char_turn()
            if turn_char == 0:
                if rikku_turns == 0:
                    buddy_swap_rikku()
                # elif faint_check(): #Optional revive on Kimahri
                #    revive()
                else:
                    defend()
                tidus_turns += 1
            elif turn_char == 3:
                lightningmarbleslot = memory.main.get_use_items_slot(30)
                if kimahriturns == 0:
                    use_item(lightningmarbleslot)
                elif kimahriturns == 1:
                    xbox.weap_swap(0)
                elif kimahriturns == 2:
                    _steal()
                elif 0 not in memory.main.get_active_battle_formation():
                    buddy_swap_tidus()
                else:
                    defend()
                kimahriturns += 1
            elif turn_char == 5:
                if luluturns == 0:
                    revive()
                else:
                    buddy_swap_yuna()
                luluturns += 1
            elif turn_char == 1:
                if yunaturns == 0:
                    revive()
                else:
                    buddy_swap_tidus()
                yunaturns += 1
            elif turn_char == 6:
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
                    xbox.weap_swap(0)
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


# Process written by CrimsonInferno
@battle.utils.speedup_decorator
def seymour_guado_blitz_win():
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

    while not memory.main.turn_ready():
        pass
    screen.await_turn()
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            turn_char = memory.main.get_battle_char_turn()
            for i in range(0, 3):
                if memory.main.get_battle_hp()[i] == 0:
                    if memory.main.get_battle_char_slot(2) == i:
                        logger.debug("Auron is dead")
                    elif memory.main.get_battle_char_slot(3) == i:
                        logger.debug("Kimahri is dead")
                        kimahridead = True
                    elif memory.main.get_battle_char_slot(4) == i:
                        logger.debug("Wakka is dead")
            if turn_char == 0:
                next_hit = rng_track.next_action_hit(
                    character=memory.main.get_current_turn(), enemy="anima"
                )
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
                    defend()
                elif tidus_turns == 3:
                    attack(direction="none")
                elif tidus_turns == 4:
                    buddy_swap_wakka()
                elif animahits + animamiss == 3 and animamiss > 0 and not missbackup:
                    buddy_swap_lulu()
                elif animahits + animamiss == 3 and not next_hit:
                    buddy_swap_lulu()
                    animamiss += 1
                elif not tidushaste:
                    logger.debug("Tidus Haste self")
                    tidus_haste("none")
                    tidushaste = True
                elif animahits < 4:
                    old_hp = memory.main.get_enemy_current_hp()[3]
                    attack(direction="none")
                    new_hp = memory.main.get_enemy_current_hp()[3]
                    if new_hp < old_hp:
                        logger.debug("Hit Anima")
                        animahits += 1
                    else:
                        logger.debug("Miss Anima")
                        animamiss += 1
                else:
                    attack(direction="none")
                tidus_turns += 1
                logger.debug(f"Tidus turns: {tidus_turns}")
            elif turn_char == 1:
                if yunaturns == 0:
                    xbox.weap_swap(0)
                else:
                    if 2 not in memory.main.get_active_battle_formation():
                        buddy_swap_auron()
                    elif 6 not in memory.main.get_active_battle_formation():
                        buddy_swap_rikku()
                    elif 4 not in memory.main.get_active_battle_formation():
                        buddy_swap_wakka()
                    elif 3 not in memory.main.get_active_battle_formation():
                        buddy_swap_kimahri()
                    else:
                        defend()
                yunaturns += 1
                logger.debug("Yuna turn, complete")
            elif turn_char == 3:
                if kimahriconfused:
                    tidusposition = memory.main.get_battle_char_slot(0)
                    rikkuposition = memory.main.get_battle_char_slot(6)
                    if tidusposition >= 3:
                        buddy_swap_tidus()
                    elif rikkuposition >= 3:
                        buddy_swap_rikku()
                elif kimahriturns == 0:
                    battle.overdrive.kimahri(3)
                elif kimahriturns == 1:
                    logs.write_rng_track("RNG11 on Seymour steal command")
                    logs.write_rng_track(
                        memory.main.rng_array_from_index(index=11, array_len=2)
                    )
                    if not memory.main.next_steal_rare(pre_advance=0):
                        steal()
                    elif memory.main.next_steal(steal_count=1, pre_advance=1):
                        if not memory.main.next_steal_rare(pre_advance=1):
                            steal()
                        else:
                            defend()
                    else:
                        defend()
                elif animamiss > 0 and (not missbackup or screen.faint_check() == 0):
                    xbox.weap_swap(0)
                else:
                    tidusposition = memory.main.get_battle_char_slot(0)
                    rikkuposition = memory.main.get_battle_char_slot(6)
                    if tidusposition >= 3:
                        buddy_swap_tidus()
                    elif rikkuposition >= 3:
                        buddy_swap_rikku()
                    else:
                        steal()
                kimahriturns += 1
                logger.debug("Kimahri turn, complete")
            elif turn_char == 2:
                if auronturns == 0:
                    _print_confused_state()
                    if memory.main.state_confused(3):
                        remedy(character=3, direction="l")
                        kimahriconfused = True
                    else:
                        defend()
                elif auronturns == 1:  # Stone Breath logic
                    defend()
                elif animamiss > 0 and (not missbackup or screen.faint_check() == 0):
                    if kimahridead and rikku_turns == 0:
                        buddy_swap_rikku()
                    else:
                        xbox.weap_swap(1)
                else:
                    tidusposition = memory.main.get_battle_char_slot(0)
                    rikkuposition = memory.main.get_battle_char_slot(6)
                    if tidusposition >= 3:
                        buddy_swap_tidus()
                    elif rikkuposition >= 3:
                        buddy_swap_rikku()
                    else:
                        defend()
                auronturns += 1
                logger.debug("Auron turn, complete")
            elif turn_char == 4:
                if wakka_turns == 0:
                    xbox.weap_swap(0)
                elif animamiss > 0 and (not missbackup or screen.faint_check() == 0):
                    if kimahridead and rikku_turns == 0:
                        buddy_swap_rikku()
                    else:
                        xbox.weap_swap(0)
                else:
                    tidusposition = memory.main.get_battle_char_slot(0)
                    rikkuposition = memory.main.get_battle_char_slot(6)
                    if tidusposition >= 3:
                        buddy_swap_tidus()
                    elif rikkuposition >= 3:
                        buddy_swap_rikku()
                    else:
                        defend()
                wakka_turns += 1
                logger.debug("Wakka turn, complete")
            elif turn_char == 6:
                if screen.faint_check() == 2:
                    revive_all()
                    missbackup = True
                    tidushaste = False
                elif animamiss > 0 and (not missbackup or screen.faint_check() == 0):
                    if kimahridead and rikku_turns == 0:
                        if not memory.main.next_steal_rare(pre_advance=0):
                            steal()
                        elif memory.main.next_steal(steal_count=1, pre_advance=1):
                            if not memory.main.next_steal_rare(pre_advance=1):
                                steal()
                            else:
                                defend()
                        else:
                            defend()
                    else:
                        if memory.main.get_battle_char_slot(0) >= 3:
                            buddy_swap_tidus()
                        # elif memory.main.get_battle_char_slot(1) >= 3:
                        #    buddy_swap_yuna()
                        # elif memory.main.get_battle_char_slot(5) >= 3:
                        #    buddy_swap_lulu()
                        else:
                            defend()
                elif animahits < 4:
                    if memory.main.next_steal(steal_count=1, pre_advance=0):
                        if not memory.main.next_steal_rare(pre_advance=0):
                            steal()
                        else:
                            defend()
                    else:
                        defend()
                elif (
                    memory.main.get_battle_hp()[memory.main.get_battle_char_slot(0)]
                    == 0
                ):
                    revive_target(target=0)
                else:
                    defend()
                rikku_turns += 1
                logger.debug("Rikku turn, complete")
            elif turn_char == 5:
                if not missbackup:
                    revive()
                    missbackup = True
                else:
                    tidusposition = memory.main.get_battle_char_slot(0)
                    rikkuposition = memory.main.get_battle_char_slot(6)
                    if tidusposition >= 3:
                        buddy_swap_tidus()
                    elif rikkuposition >= 3:
                        buddy_swap_rikku()
                    else:
                        defend()
                logger.debug("Lulu turn, complete")
            else:
                logger.debug("No turn. Holding for next action.")
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
            logger.debug("Diag skip")
    logger.info("Battle summary screen")
    FFXC.set_value("btn_b", 1)
    memory.main.wait_frames(30 * 2.8)
    FFXC.set_value("btn_b", 0)


@battle.utils.speedup_decorator
def seymour_guado_blitz_loss():
    screen.await_turn()

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

    while not memory.main.battle_complete():  # AKA end of battle screen
        if memory.main.turn_ready():
            turn_char = memory.main.get_battle_char_turn()
            for i in range(0, 3):
                if memory.main.get_battle_hp()[i] == 0:
                    if memory.main.get_battle_char_slot(2) == i:
                        logger.debug("Auron is dead")
                    elif memory.main.get_battle_char_slot(3) == i:
                        logger.debug("Kimahri is dead")
                        kimahridead = True
                    elif memory.main.get_battle_char_slot(4) == i:
                        logger.debug("Wakka is dead")
            if turn_char == 0:
                if memory.main.get_enemy_current_hp()[1] < 2999:
                    attack(direction="none")
                    logger.debug("Should be last attack of the fight.")
                elif tidus_turns == 0:
                    logger.debug("Tidus Haste self")
                    tidus_haste("none")
                    tidushaste = True
                elif tidus_turns == 1:
                    cheer()
                elif tidus_turns == 2:
                    logger.debug("Talk to Seymour")
                    while not memory.main.other_battle_menu():
                        xbox.tap_left()
                    while memory.main.battle_cursor_2() != 1:
                        xbox.tap_down()
                    while memory.main.other_battle_menu():
                        xbox.tap_b()
                    xbox.tap_left()
                    tap_targeting()
                elif tidus_turns == 3:
                    logger.debug("Swap to Brotherhood")
                    equip_in_battle(special="brotherhood")
                elif tidus_turns == 4:
                    logger.debug("Tidus overdrive activating")
                    screen.await_turn()
                    battle.overdrive.tidus("left")
                elif tidus_turns == 5:
                    buddy_swap_wakka()
                elif animahits + animamiss == 3 and animamiss > 0 and not missbackup:
                    buddy_swap_lulu()
                    defend()
                    missbackup = True
                elif not tidushaste:
                    logger.debug("Tidus Haste self")
                    tidus_haste("none")
                    tidushaste = True
                elif animahits < 4:
                    old_hp = memory.main.get_enemy_current_hp()[3]
                    attack(direction="none")
                    new_hp = memory.main.get_enemy_current_hp()[3]
                    if new_hp < old_hp:
                        logger.debug("Hit Anima")
                        animahits += 1
                    else:
                        logger.debug("Miss Anima")
                        animamiss += 1
                else:
                    logger.debug("Plain Attacking")
                    attack(direction="none")
                tidus_turns += 1
                logger.debug(f"Tidus turns: {tidus_turns}")
            elif turn_char == 1:
                if yunaturns == 0:
                    xbox.weap_swap(0)
                else:
                    buddy_swap_lulu()
                    screen.await_turn()
                    _print_confused_state()
                    if memory.main.state_confused(3):
                        remedy(character=3, direction="l")
                        kimahriconfused = True
                    else:
                        xbox.weap_swap(0)
                yunaturns += 1
                logger.debug("Yuna turn, complete")
            elif turn_char == 5:
                if animahits == 0:
                    _print_confused_state()
                    buddy_swap_rikku()
                    if memory.main.state_confused(0):
                        remedy(character=0, direction="l")
                    elif memory.main.state_confused(3):
                        remedy(character=3, direction="l")
                else:
                    buddy_swap_tidus()
                    attack(direction="none")
            elif turn_char == 3:
                if kimahriconfused:
                    tidusposition = memory.main.get_battle_char_slot(0)
                    rikkuposition = memory.main.get_battle_char_slot(6)
                    if tidusposition >= 3:
                        buddy_swap_tidus()
                    elif rikkuposition >= 3:
                        buddy_swap_rikku()
                    else:
                        defend()
                elif kimahriturns == 0:
                    _print_confused_state()
                    if memory.main.state_confused(0):
                        remedy(character=0, direction="l")
                    elif memory.main.state_confused(1):
                        remedy(character=1, direction="l")
                    elif memory.main.state_confused(5):
                        remedy(character=5, direction="l")
                    else:
                        defend()
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
                        buddy_swap_tidus()
                    elif rikkuposition >= 3:
                        buddy_swap_rikku()
                    else:
                        steal()
                kimahriturns += 1
                logger.debug("Kimahri turn, complete")
            elif turn_char == 4:
                if wakka_turns == 0:
                    xbox.weap_swap(0)
                elif animamiss > 0 and (not missbackup or screen.faint_check() == 0):
                    if kimahridead and rikku_turns < 2:
                        buddy_swap_rikku()
                    else:
                        xbox.weap_swap(0)
                else:
                    tidusposition = memory.main.get_battle_char_slot(0)
                    rikkuposition = memory.main.get_battle_char_slot(6)
                    if tidusposition >= 3:
                        buddy_swap_tidus()
                    elif rikkuposition >= 3:
                        buddy_swap_rikku()
                    else:
                        defend()
                wakka_turns += 1
                logger.debug("Wakka turn, complete")
            elif turn_char == 6:
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
                    tidusposition = memory.main.get_battle_char_slot(0)
                    if tidusposition >= 3:
                        buddy_swap_tidus()
                    elif animamiss > 0 and (
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
                        defend()
                rikku_turns += 1
                logger.debug("Rikku turn, complete")
            else:
                logger.debug("No turn. Holding for next action.")
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
            logger.debug("Diag skip")
    logger.info("Battle summary screen")
    FFXC.set_value("btn_b", 1)
    memory.main.wait_frames(30 * 2.8)
    FFXC.set_value("btn_b", 0)


def seymour_guado():
    if game_vars.get_blitz_win():
        seymour_guado_blitz_win()
    else:
        seymour_guado_blitz_loss()


def escape_with_xp():
    rikku_item = False
    if memory.main.get_item_slot(39) > 200:
        flee_all()
    else:
        while not memory.main.turn_ready():
            pass
        while memory.main.battle_active():
            if memory.main.turn_ready():
                if screen.turn_tidus():
                    if not rikku_item:
                        equip_in_battle(equip_type="armor", ability_num=0x8028)
                        screen.await_turn()
                        buddy_swap_rikku()
                    else:
                        attack("none")
                elif screen.turn_rikku():
                    if not rikku_item:
                        use_item(memory.main.get_use_items_slot(39))
                        rikku_item = True
                    else:
                        defend()
                elif screen.turn_auron():
                    attack("none")
                else:
                    buddy_swap_tidus()
    memory.main.click_to_control()


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
    logger.debug("Wendigo Res/Heal function")
    party_hp = memory.main.get_battle_hp()
    if screen.faint_check() == 2:
        logger.debug("2 Characters are dead")
        if memory.main.get_throw_items_slot(7) < 255:
            revive_all()
        elif memory.main.get_throw_items_slot(6) < 255:
            revive()  # This should technically target tidus but need to update this logic
    # If just Tidus is dead revive him
    elif party_hp[memory.main.get_battle_char_slot(0)] == 0:
        logger.debug("Reviving tidus")
        revive()
    elif use_power_break:
        logger.debug("Swapping to Auron to Power Break")
        buddy_swap_auron()
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
                defend()
    elif screen.faint_check():
        logger.debug("Reviving non-Tidus")
        revive()
    else:
        return False

    return True


@battle.utils.speedup_decorator
def zu():
    screen.await_turn()
    attack("none")
    while not memory.main.battle_complete():
        if memory.main.turn_ready():
            if memory.main.party_size() <= 2:
                defend()
            else:
                flee_all()
        elif memory.main.diag_skip_possible():
            xbox.tap_b()  # Skip Dialog
    memory.main.click_to_control()


@battle.utils.speedup_decorator
def bikanel_battle_logic(status, sandy_fight_complete: bool = False):
    # status should be an array length 2
    # [rikku_charged, speed_needed, power_needed, items_needed]
    encounter_id = memory.main.get_encounter_id()
    item_stolen = False
    item_thrown = False
    throw_power = False
    throw_speed = False
    steal_direction = "none"
    logger.debug(f"---------------Starting desert battle: {encounter_id}")

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
    flee_battles = [
        201,
        203,
        204,
        205,
        210,
        212,
        213,
        215,
        217,
        219,
        223,
        224,
        226,
        227,
    ]

    # Next, determine what we want to do
    if encounter_id in flee_battles:
        if status[0]:
            battle_goal = 3  # Nothing to do here, we just want to flee.
        else:
            battle_goal = 2
    else:
        items = update_steal_items_desert()
        if items[1] < 2:
            battle_goal = 0  # Steal an item
        elif items[1] == 0 and items[2] == 0:
            battle_goal = 0  # Steal an item
        # Extra items into power/speed
        elif status[3] <= -1 and (throw_power or throw_speed):
            battle_goal = 1  # Throw an item
        elif status[3] > -1:
            # Steal to an excess of one item (so we can throw in future battles)
            battle_goal = 0
        elif not status[0]:
            battle_goal = 2  # Rikku still needs charging.
        else:
            battle_goal = 3  # Nothing to do but get to Home.

    # Then we take action.
    while not memory.main.battle_complete():
        if battle_goal == 0:  # Steal an item
            logger.debug("Looking to steal an item.")
            if memory.main.turn_ready():
                if memory.main.get_battle_char_turn() == 0:
                    buddy_swap_kimahri()
                elif not item_stolen and (screen.turn_kimahri() or screen.turn_ready()):
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

                    # After stealing an item, what to do next?
                    if throw_power or throw_speed:
                        battle_goal = 1
                    else:
                        battle_goal = 3
                elif not status[0]:
                    if memory.main.get_battle_char_turn() == 6:
                        attack("none")
                    else:
                        escape_one()
                else:
                    buddy_swap_tidus()
                    screen.await_turn()
                    flee_all()
        elif battle_goal == 1:  # Throw an item
            logger.debug("Throw item with Kimahri, everyone else escape.")
            if memory.main.turn_ready():
                items = update_steal_items_desert()
                if memory.main.get_battle_char_turn() == 0:
                    buddy_swap_kimahri()
                elif not item_thrown and (screen.turn_kimahri() or screen.turn_rikku()):
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
                    if memory.main.get_battle_char_turn() == 6:
                        attack("none")
                    else:
                        escape_one()
                else:
                    flee_all()
        elif battle_goal == 2:  # Charge Rikku
            logger.debug("Attack/Steal with Rikku, everyone else escape.")
            if memory.main.turn_ready():
                if memory.main.get_battle_char_turn() == 6:
                    attack("none")
                elif screen.turn_auron() and memory.main.get_overdrive_battle(2) != 100:
                    attack_by_num(2)
                elif 6 in memory.main.get_active_battle_formation():
                    escape_one()
                else:
                    flee_all()
        else:  # Charge Auron if needed, otherwise flee
            if memory.main.get_overdrive_battle(2) != 100 and not sandy_fight_complete:
                if screen.turn_auron():
                    attack_by_num(2)
                else:
                    escape_one()
            else:
                logger.debug("Flee all battles, nothing more to do.")
                flee_all()


def update_steal_items_desert():
    item_array = [0, 0, 0, 0]
    # Bomb cores
    index = memory.main.get_item_slot(27)
    if index == 255:
        item_array[0] = 0
    else:
        item_array[0] = memory.main.get_item_count_slot(index)

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
    screen.await_turn()
    if version != 1:  # Kimahri's turn
        flee_all()
        memory.main.click_to_control()
    else:  # Auron's turn
        # Manip for NE armor
        if memory.main.battle_type() == 2:
            while memory.main.battle_type() == 2:
                logger.debug("Ambushed, swapping out.")
                flee_all()
                memory.main.click_to_control()
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                FFXC.set_neutral()
                screen.await_turn()
        # elif FX_memory.rng_seed() == 31:
        #    logger.debug("Manipulating known seed 31")
        #    flee_all()
        #    memory.click_to_control()
        #    FFXC.set_movement(0, 1)
        #    memory.await_event()
        #    FFXC.set_neutral()
        #    screen.await_turn()
        else:
            logger.debug("DO NOT Swap odd/even seeds on RNG01")

        tidus_haste("l", character=2)
        screen.await_turn()
        if screen.turn_kimahri() or screen.turn_rikku():
            logger.debug("Kimahri/Rikku taking a spare turn. Just defend.")
            defend()
            screen.await_turn()
        logger.debug("Setting up Auron overdrive")
        battle.overdrive.auron(style="shooting star")
        memory.main.click_to_control()


@battle.utils.speedup_decorator
def home_1():
    FFXC.set_neutral()
    xbox.click_to_battle()
    logger.debug("Tidus vs Bombs")
    tidus_haste("none")
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if screen.faint_check() > 0:
                revive()
            elif screen.turn_tidus():
                attack("none")
            elif screen.turn_auron() and memory.main.get_enemy_current_hp()[0] != 0:
                attack("none")
            else:
                defend()
    logger.debug("Home 1 shows as fight complete.")
    memory.main.click_to_control()


@battle.utils.speedup_decorator
def home_2():
    xbox.click_to_battle()

    logger.debug("Kimahri vs dual horns")
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():

            if screen.turn_kimahri():
                battle.overdrive.kimahri(3)
            elif memory.main.get_battle_char_slot(3) >= 3:
                buddy_swap_kimahri()  # Tidus for Kimahri
                lancet_home("none")
            else:
                defend()
    logger.debug("Home 2 shows as fight complete.")
    FFXC.set_neutral()
    memory.main.click_to_control()


@battle.utils.speedup_decorator
def home_3():
    logger.debug("Home 3 fight")
    xbox.click_to_battle()
    if memory.main.get_use_items_slot(49) > 200:
        tidus_haste("none")
    else:
        while not screen.turn_rikku():
            defend()
            xbox.click_to_battle()
            use_item(memory.main.get_use_items_slot(49), "none")

    rikku_item_thrown = 0
    while not memory.main.battle_complete():  # AKA end of battle screen
        if memory.main.turn_ready():
            logger.debug("- Turn:")
            if screen.turn_tidus():
                logger.debug("  Tidus")
                if memory.main.get_use_items_slot(49) != 255:
                    defend()
                else:
                    attack("none")
            elif screen.turn_rikku() and rikku_item_thrown < 1 and home_3_item() != 255:
                logger.debug("  Rikku")
                use_item_slot = home_3_item()
                use_item(use_item_slot, "none")
                rikku_item_thrown += 1
            elif screen.faint_check() > 0:
                logger.debug("  any, revive")
                revive()
            else:
                logger.debug("  any, defend")
                defend()
    FFXC.set_neutral()
    logger.debug("Home 3 shows as fight complete.")


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

    logger.debug("Kimahri vs Chimera")
    while memory.main.battle_active():  # AKA end of battle screen
        if memory.main.turn_ready():
            if screen.turn_kimahri():
                battle.overdrive.kimahri(4)
            elif memory.main.get_battle_char_slot(3) >= 3:
                buddy_swap_kimahri()  # Tidus for Kimahri
                lancet_home("none")
            else:
                defend()
    logger.debug("Home 4 shows as fight complete.")
    memory.main.click_to_control()


@battle.utils.speedup_decorator
def guards(group_num, sleeping_powders):
    xbox.click_to_battle()
    throw_distiller = (
        memory.main.get_item_slot(16) != 255 or memory.main.get_item_slot(18) != 255
    )
    num_throws = 0
    hasted = False
    tidus_went = False
    if sleeping_powders:  # We have sleeping powders
        while not memory.main.battle_complete():  # AKA end of battle screen
            if group_num in [1, 3]:
                if screen.turn_tidus():
                    attack("none")
                elif throw_distiller:
                    if memory.main.get_item_slot(18) != 255:
                        _use_healing_item(item_id=18)
                    else:
                        _use_healing_item(item_id=16)
                    throw_distiller = False
                elif (
                    6 in memory.main.get_active_battle_formation()
                    and memory.main.get_battle_hp()[memory.main.get_battle_char_slot(6)]
                    <= 120
                    and memory.main.get_battle_hp()[memory.main.get_battle_char_slot(6)]
                    != 0
                ):
                    if memory.main.get_item_slot(0) != 255:
                        use_potion_character(6, "r")
                    elif memory.main.get_item_slot(1) != 255:
                        _use_healing_item(num=6, direction="r", item_id=1)
                    else:
                        defend()
                else:
                    defend()
            elif group_num in [2, 4]:
                if screen.turn_tidus():
                    attack("none")
                elif (screen.turn_rikku() or screen.turn_kimahri()) and num_throws < 2:
                    silence_slot = memory.main.get_item_slot(39)
                    if num_throws == 0 and memory.main.get_use_items_slot(37) < 200:
                        use_item(memory.main.get_use_items_slot(37))
                    else:
                        if memory.main.get_use_items_slot(40) != 255:
                            use_item(memory.main.get_use_items_slot(40))
                        elif (
                            silence_slot != 255
                            and memory.main.get_item_count_slot(silence_slot) > 1
                        ):
                            # Save one for later if possible
                            use_item(memory.main.get_use_items_slot(39))
                        elif memory.main.get_use_items_slot(37) != 255:
                            use_item(memory.main.get_use_items_slot(37))
                        elif memory.main.get_use_items_slot(27) != 255:
                            use_item(memory.main.get_use_items_slot(27))
                        elif silence_slot != 255:
                            # Throw last Silence grenade as a last resort.
                            use_item(memory.main.get_use_items_slot(39))
                        else:
                            defend()
                    num_throws += 1
                else:
                    defend()
            elif group_num == 5:
                if screen.faint_check():
                    revive()
                elif screen.turn_tidus():
                    if not hasted:
                        tidus_haste("left", character=6)
                        hasted = True
                    else:
                        attack_by_num(22, "r")
                elif screen.turn_rikku() or screen.turn_kimahri():
                    silence_slot = memory.main.get_item_slot(39)
                    if num_throws < 2:
                        if memory.main.get_use_items_slot(40) != 255:
                            use_item(memory.main.get_use_items_slot(40))
                        elif (
                            silence_slot != 255
                            and memory.main.get_item_count_slot(silence_slot) > 1
                        ):
                            # Save one for later if possible
                            use_item(memory.main.get_use_items_slot(39))
                        elif memory.main.get_use_items_slot(37) != 255:
                            use_item(memory.main.get_use_items_slot(37))
                        elif memory.main.get_use_items_slot(27) != 255:
                            use_item(memory.main.get_use_items_slot(27))
                        elif memory.main.get_use_items_slot(39) != 255:
                            use_item(memory.main.get_use_items_slot(39))
                        else:
                            defend()
                        num_throws += 1
                    else:
                        defend()
    else:  # We do not have sleeping powders
        while not memory.main.battle_complete():
            if group_num in [1, 3]:
                if screen.turn_tidus():
                    attack("none")
                elif throw_distiller:
                    if memory.main.get_item_slot(18) != 255:
                        _use_healing_item(item_id=18)
                    else:
                        _use_healing_item(item_id=16)
                    throw_distiller = False
                elif (
                    6 in memory.main.get_active_battle_formation()
                    and memory.main.get_battle_hp()[memory.main.get_battle_char_slot(6)]
                    <= 120
                    and memory.main.get_battle_hp()[memory.main.get_battle_char_slot(6)]
                    != 0
                ):
                    if memory.main.get_item_slot(0) != 255:
                        use_potion_character(6, "r")
                    elif memory.main.get_item_slot(1) != 255:
                        _use_healing_item(num=6, direction="r", item_id=1)
                    else:
                        defend()
                else:
                    defend()
            elif group_num in [2, 4]:
                if screen.turn_tidus():
                    if not tidus_went:
                        buddy_swap_kimahri()
                        tidus_went = True
                    else:
                        attack("none")
                elif screen.turn_kimahri() or screen.turn_rikku():
                    silence_slot = memory.main.get_item_slot(39)
                    if memory.main.get_use_items_slot(40) != 255:
                        use_item(memory.main.get_use_items_slot(40))
                    elif (
                        silence_slot != 255
                        and memory.main.get_item_count_slot(silence_slot) >= 2
                    ):
                        # Save one for later if possible
                        use_item(memory.main.get_use_items_slot(39))
                    elif memory.main.get_use_items_slot(37) != 255:
                        use_item(memory.main.get_use_items_slot(37))
                    elif memory.main.get_use_items_slot(27) != 255:
                        use_item(memory.main.get_use_items_slot(27))
                    elif memory.main.get_use_items_slot(39) != 255:
                        use_item(memory.main.get_use_items_slot(39))
                    else:
                        defend()
                else:
                    defend()
            elif group_num == 5:
                if screen.turn_tidus():
                    if not tidus_went:
                        buddy_swap_rikku()
                        tidus_went = True
                    else:
                        attack_by_num(22, "l")
                elif screen.turn_rikku() or screen.turn_kimahri():
                    silence_slot = memory.main.get_item_slot(39)
                    if num_throws < 2:
                        if memory.main.get_use_items_slot(40) != 255:
                            use_item(memory.main.get_use_items_slot(40))
                        elif (
                            silence_slot != 255
                            and memory.main.get_item_count_slot(silence_slot) > 1
                        ):
                            # Save one for later if possible
                            use_item(memory.main.get_use_items_slot(39))
                        elif memory.main.get_use_items_slot(37) != 255:
                            use_item(memory.main.get_use_items_slot(37))
                        elif memory.main.get_use_items_slot(27) != 255:
                            use_item(memory.main.get_use_items_slot(27))
                        elif (
                            memory.main.get_use_items_slot(39) != 255 and num_throws < 2
                        ):
                            use_item(memory.main.get_use_items_slot(39))
                        else:
                            defend()
                    else:
                        defend()
                    num_throws += 1
                elif screen.turn_kimahri():
                    buddy_swap_tidus()
                else:
                    defend()


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


def evrae_altana_steal():
    logger.debug("=================================")
    logger.debug("Steal logic, we will get two gems")
    logger.debug("=================================")
    haste_count = False
    steal_count = False
    while memory.main.get_item_slot(34) == 255:
        if memory.main.turn_ready():
            if screen.turn_tidus() and not haste_count:
                tidus_haste(direction="l", character=6)
                haste_count = True
            elif screen.turn_rikku() and not steal_count:
                _steal()
                steal_count = True
            else:
                defend()
    logger.debug("====================================")
    logger.debug("End of steal logic. Back to regular.")
    logger.debug("====================================")
    # memory.main.wait_frames(180)


def attack_highbridge():
    if memory.main.get_encounter_id() == 270:
        attack_by_num(22, "r")
    elif memory.main.get_encounter_id() == 271:
        attack_by_num(21, "l")
    else:
        attack("none")


@battle.utils.speedup_decorator
def calm_lands_gems():
    while not memory.main.turn_ready():
        pass
    steal_complete = False
    if not memory.main.get_encounter_id() in [273, 275, 281, 283]:
        flee_all()
    else:
        while memory.main.battle_active():
            if memory.main.turn_ready():
                if 3 not in memory.main.get_active_battle_formation():
                    buddy_swap_kimahri()
                elif steal_complete:
                    flee_all()
                elif screen.turn_kimahri():
                    # Red element in center slot, with machina and dog
                    if memory.main.get_encounter_id() in [273, 281]:
                        logger.debug("Grabbing a gem here.")
                        steal_left()
                    # Red element in top slot, with bee and tank
                    elif memory.main.get_encounter_id() in [275, 283]:
                        logger.debug("Grabbing a gem here.")
                        buddy_swap_kimahri()
                        steal_down()
                    else:
                        defend()
                    steal_complete = True
                else:
                    defend()
    memory.main.click_to_control()


@battle.utils.speedup_decorator
def gagazet_path():
    while not memory.main.turn_ready():
        pass
    if memory.main.get_encounter_id() == 337:
        while memory.main.battle_active():
            if memory.main.turn_ready():
                if screen.turn_rikku():
                    steal_right()
                else:
                    escape_one()
    else:
        flee_all()


@battle.utils.speedup_decorator
def cave_charge_rikku():
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if screen.turn_rikku():
                attack("none")
            else:
                escape_one()
    memory.main.click_to_control()


def gagazet_cave(direction):
    screen.await_turn()
    attack(direction)
    flee_all()


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
        while battle_cursor() != position:
            logger.debug(f"Battle_cursor: {battle_cursor()}")
            if battle_cursor() > position:
                xbox.tap_up()
            else:
                xbox.tap_down()


def use_item(slot: int, direction="none", target=255, rikku_flee=False):
    logger.debug("Using items via the Use command")
    logger.debug(f"Item slot: {slot}")
    logger.debug(f"Direction: {direction}")
    while not memory.main.main_battle_menu():
        pass
    logger.debug("Mark 1, turn is active.")
    while memory.main.battle_menu_cursor() != 20:
        if not screen.turn_rikku() and not screen.turn_kimahri():
            return
        if memory.main.battle_menu_cursor() in [0, 19]:
            xbox.tap_down()
        elif memory.main.battle_menu_cursor() == 1:
            xbox.tap_up()
        elif memory.main.battle_menu_cursor() > 20:
            xbox.tap_up()
        else:
            xbox.tap_down()
    if game_vars.use_pause():
        memory.main.wait_frames(3)
    while memory.main.main_battle_menu():
        xbox.tap_b()
    if rikku_flee:
        logger.debug("Mark 2, selecting 'Use' command in position 2")
    else:
        logger.debug("Mark 2, selecting 'Use' command in position 1")
    if rikku_flee:
        _navigate_to_position(2)
    else:
        _navigate_to_position(1)
    if game_vars.use_pause():
        memory.main.wait_frames(3)
    while memory.main.other_battle_menu():
        xbox.tap_b()
    logger.debug("Mark 3, navigating to item slot")
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


def use_item_tidus(slot: int, direction="none", target=255):
    logger.debug("Using items via the Use command")
    logger.debug(f"Item slot: {slot}")
    logger.debug(f"Direction: {direction}")
    while not memory.main.main_battle_menu():
        pass
    logger.debug("Mark 1")
    while memory.main.battle_menu_cursor() != 20:
        if not screen.turn_tidus():
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
        if not screen.turn_tidus():
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
    while not memory.main.turn_ready():
        logger.debug("Battle menu isn't up.")
        pass
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


def attack_by_num(num, direction="u"):
    if num < 20:
        friendly_target = True
    else:
        friendly_target = False
    logger.debug(f"Attacking specific character, {num}")
    direction = direction.lower()
    if not memory.main.turn_ready():
        logger.debug("Battle menu isn't up.")
        while not memory.main.turn_ready():
            # Waiting for battle menu to come up.
            pass
        # Make sure we actually have control
    if (
        memory.main.battle_menu_cursor() != 0
        and memory.main.battle_menu_cursor() != 216
    ):
        while not memory.main.battle_menu_cursor() in [0, 216]:
            xbox.tap_up()
            if screen.battle_complete():
                return  # Safety
    while memory.main.main_battle_menu():
        xbox.tap_b()

    if not friendly_target and memory.main.get_enemy_current_hp()[num - 20] != 0:
        while memory.main.battle_target_id() != num:
            if direction == "l":
                if memory.main.battle_target_id() < 20:
                    direction = "u"
                xbox.tap_left()
            elif direction == "r":
                if memory.main.battle_target_id() < 20:
                    direction = "d"
                xbox.tap_right()
            elif direction == "u":
                if memory.main.battle_target_id() < 20:
                    direction = "l"
                xbox.tap_up()
            elif direction == "d":
                if memory.main.battle_target_id() < 20:
                    direction = "r"
                xbox.tap_down()
    elif friendly_target:
        while memory.main.battle_target_id() != num:
            if direction == "l":
                if memory.main.battle_target_id() >= 20:
                    direction = "u"
                xbox.tap_left()
            elif direction == "r":
                if memory.main.battle_target_id() >= 20:
                    direction = "d"
                xbox.tap_right()
            elif direction == "u":
                if memory.main.battle_target_id() >= 20:
                    direction = "l"
                xbox.tap_up()
            elif direction == "d":
                if memory.main.battle_target_id() >= 20:
                    direction = "r"
                xbox.tap_down()
    tap_targeting()


def attack_self_tanker():
    logger.debug("Attacking specific character, Auron (self)")
    if not memory.main.turn_ready():
        logger.debug("Battle menu isn't up.")
        while not memory.main.turn_ready():
            # Waiting for battle menu to come up.
            pass
    if (
        memory.main.battle_menu_cursor() != 0
        and memory.main.battle_menu_cursor() != 216
    ):
        while not memory.main.battle_menu_cursor() in [0, 216]:
            xbox.tap_up()
            if screen.battle_complete():
                return  # Safety
    while memory.main.main_battle_menu():
        xbox.tap_b()
    while memory.main.battle_target_id() != 2:
        if memory.main.battle_target_id() > 20:
            xbox.tap_down()
        else:
            xbox.tap_left()
    tap_targeting()


def oblitz_rng_wait():
    rng_values = rng_track.oblitz_history()
    logger.debug(f"rng_values: {rng_values}")
    last_rng = memory.main.rng_from_index(index=2)
    coming_seeds = memory.main.rng_array_from_index(index=2, array_len=8)
    seed_num = str(memory.main.rng_seed())
    logger.debug(f"coming_seeds: {coming_seeds}")
    pos = 0

    if seed_num not in rng_values:
        logger.debug(f"## No values for this RNG seed - {memory.main.rng_seed()}")
        first_result = [coming_seeds[1], 10, True, 1]
        second_result = [coming_seeds[2], 20, True, 2]
    else:
        logger.debug("## Scanning values for this RNG seed")
        if game_vars.loop_blitz():  # This will cause us to prefer results hunting
            logger.debug("### Looping on blitz, we will try a new value.")
            # Seed value, time to completion, Win/Loss, and position
            first_result = [coming_seeds[1], 9999, True, 0]
            second_result = [coming_seeds[2], 9999, True, 0]
        else:  # For full runs, take the best result.
            logger.debug("### This is a full run. Selecting best known result.")
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
                    f"No result (preferred), loop. {[coming_seeds[i], duration, victory, pos]}"
                )
            else:
                duration = 540 + pos
                # 540 is about the maximum duration we desire.
                victory = False
                logger.debug(
                    f"No result (undesirable), full. {[coming_seeds[i], duration, victory, pos]}"
                )
            # Fill as first two RNG values, then test against previously set RNG values until we've exhausted tests.
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
    logger.debug("====================================")
    logger.debug("Chosen results (RNG, duration, victory, waits):")
    logger.debug(best)
    logger.debug("====================================")
    # Now wait for one of the two results to come up
    while next_rng != best[0] and j < 15:
        next_rng = memory.main.rng_from_index(index=2) & 0x7FFFFFFF
        if last_rng != next_rng:
            logger.debug(
                f"{j} | {s32(next_rng)} | {s32(memory.main.rng_from_index(index=2))} | {s32(best[0])}"
            )
            j += 1
            last_rng = next_rng
    logger.debug("====================================")
    logger.debug(f"Success. Attacking. {j} | {next_rng}")
    game_vars.set_oblitz_rng(value=next_rng)
    return next_rng


def attack_oblitz_end():
    logger.debug("Attack")
    if not memory.main.turn_ready():
        while not memory.main.turn_ready():
            pass
    while memory.main.main_battle_menu():
        if not memory.main.battle_menu_cursor() in [0, 203, 210, 216]:
            logger.debug(f"Battle Menu Cursor: {memory.main.battle_menu_cursor()}")
            xbox.tap_up()
        elif screen.battle_complete():
            return
        else:
            xbox.menu_b()
    memory.main.wait_frames(1)
    rng_wait_results = oblitz_rng_wait()
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
        if not memory.main.battle_menu_cursor() in [0, 203, 210, 216]:
            logger.debug(f"Battle Menu Cursor: {memory.main.battle_menu_cursor()}")
            xbox.tap_up()
        elif screen.battle_complete():
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


def _steal(direction=None):
    if not memory.main.main_battle_menu():
        while not memory.main.main_battle_menu():
            pass
    while memory.main.battle_menu_cursor() != 20:
        if not screen.turn_rikku() and not screen.turn_kimahri():
            return
        if memory.main.battle_menu_cursor() == 1:
            xbox.tap_up()
        elif memory.main.battle_menu_cursor() > 20:
            xbox.tap_up()
        else:
            xbox.tap_down()
    while not memory.main.other_battle_menu():
        xbox.tap_b()
    _navigate_to_position(0)
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
    logger.debug("Firing steal")
    tap_targeting()


def steal():
    logger.debug("Steal")
    if memory.main.get_encounter_id() in [273, 281]:
        _steal("left")
    elif memory.main.get_encounter_id() in [276, 279, 289]:
        _steal("up")
    else:
        _steal()


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


def steal_and_attack():
    logger.debug("Steal/Attack function")
    FFXC.set_neutral()
    screen.await_turn()
    while not memory.main.battle_complete():
        if memory.main.turn_ready():
            if screen.turn_rikku():
                grenade_slot = memory.main.get_item_slot(35)
                gregrenade_count = memory.main.get_item_count_slot(grenade_slot)
                if gregrenade_count < 5:
                    steal()
                else:
                    attack("none")
            if screen.turn_tidus():
                attack("none")
        elif memory.main.other_battle_menu():
            xbox.tap_b()
    memory.main.click_to_control()


@battle.utils.speedup_decorator
def steal_and_attack_pre_tros():
    logger.debug("Steal/Attack function before Tros")
    turn_counter = 0
    advances = get_advances(tros=False)
    FFXC.set_neutral()
    while not memory.main.battle_complete():
        if memory.main.turn_ready():
            if screen.turn_rikku():
                turn_counter += 1
                if turn_counter == 1:
                    grenade_slot = memory.main.get_item_slot(35)
                    gregrenade_count = memory.main.get_item_count_slot(grenade_slot)
                    if gregrenade_count < 5:
                        steal()
                    elif advances in [1, 2]:
                        steal()
                        advances = get_advances(tros=False)
                    else:
                        attack("none")
                elif turn_counter == 2:
                    grenade_slot = memory.main.get_item_slot(35)
                    gregrenade_count = memory.main.get_item_count_slot(grenade_slot)
                    if gregrenade_count < 6:
                        steal()
                    elif advances in [1, 2]:
                        steal()
                        advances = get_advances(tros=False)
                    else:
                        attack("none")
                else:
                    attack("none")
            if screen.turn_tidus():
                attack("none")
        elif memory.main.other_battle_menu():
            xbox.tap_b()
    memory.main.click_to_control()


def cast_spell(direction, spell_id):
    if not screen.turn_lulu():
        logger.debug("Lulu is not the current person. Deferring turn.")
        return
    while memory.main.battle_menu_cursor() != 21:
        logger.debug(f"Battle menu cursor: {memory.main.battle_menu_cursor()}")
        if memory.main.battle_menu_cursor() == 0:
            xbox.tap_down()
        else:
            xbox.tap_up()
    while memory.main.main_battle_menu():
        xbox.tap_b()  # Black magic
    _navigate_to_position(spell_id)
    while memory.main.other_battle_menu():
        xbox.tap_b()  # Cast the Spell
    direction = direction.lower()
    if direction == "right":
        xbox.tap_right()
    elif direction == "left":
        xbox.tap_left()
    elif direction == "up":
        xbox.tap_up()
    elif direction == "down":
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
    elif not direction or direction == "none":
        pass
    else:
        logger.error(f"UNSURE DIRECTION: {direction}")
        raise ValueError("Unsure direction")
    tap_targeting()


def thunder(direction="none"):
    logger.debug("Black magic - Thunder")
    cast_spell(direction, 1)


def fire(direction="none"):
    logger.debug("Black magic - Fire")
    cast_spell(direction, 0)


def water(direction="none"):
    logger.debug("Black magic - Water")
    cast_spell(direction, 2)


def ice(direction="none"):
    logger.debug("Black magic - Ice")
    cast_spell(direction, 3)


def thunder_target(target, direction):
    logger.debug("Black magic - Thunder")
    if not screen.turn_lulu():
        logger.debug("Lulu is not the current person. Deferring turn.")
        return
    direction = direction.lower()
    while memory.main.main_battle_menu():
        if memory.main.battle_menu_cursor() != 21:
            logger.debug(f"Battle menu cursor: {memory.main.battle_menu_cursor()}")
            if memory.main.battle_menu_cursor() == 0:
                xbox.tap_down()
            else:
                xbox.tap_up()
        else:
            xbox.tap_b()
    logger.debug(f"Battle cursor 2: {memory.main.battle_cursor_2()}")
    _navigate_to_position(1)
    while memory.main.other_battle_menu():
        xbox.tap_b()  # Thunder
    while memory.main.battle_target_id() != target:
        if direction == "l":
            if memory.main.battle_target_id() < 20:
                logger.debug("Wrong battle line targeted.")
                xbox.tap_right()
                direction = "u"
            else:
                xbox.tap_left()
        elif direction == "r":
            if memory.main.battle_target_id() < 20:
                logger.debug("Wrong character targeted.")
                xbox.tap_left()
                direction = "d"
            else:
                xbox.tap_right()
        elif direction == "u":
            if memory.main.battle_target_id() < 20:
                logger.debug("Wrong character targeted.")
                xbox.tap_down()
                direction = "l"
            else:
                xbox.tap_up()
        elif direction == "d":
            if memory.main.battle_target_id() < 20:
                logger.debug("Wrong character targeted.")
                xbox.tap_up()
                direction = "r"
            else:
                xbox.tap_down()
    tap_targeting()


def aeon_summon(position):
    logger.debug(f"Summoning Aeon {position}")
    while not memory.main.main_battle_menu():
        pass
    while memory.main.battle_menu_cursor() != 23:
        if not screen.turn_yuna():
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
        xbox.tap_b()
    while position != memory.main.battle_cursor_2():
        logger.debug(f"Battle cursor 2: {memory.main.battle_cursor_2()}")
        if memory.main.battle_cursor_2() < position:
            xbox.tap_down()
        else:
            xbox.tap_up()
    while memory.main.other_battle_menu():
        xbox.tap_b()

    with logging_redirect_tqdm():
        fmt = "Waiting for Aeon's turn... elapsed {elapsed}"
        with tqdm(bar_format=fmt) as pbar:
            while not memory.main.turn_ready():
                pbar.update()


def aeon_spell(position):
    aeon_spell_direction(position, None)


def aeon_spell_2(position, direction):
    aeon_spell_direction(position, direction)


def aeon_spell_direction(position, direction):
    logger.debug(f"Aeon casting a spell. Special direction: {direction}")
    while memory.main.battle_menu_cursor() != 21:
        xbox.tap_down()
    while memory.main.main_battle_menu():
        xbox.tap_b()  # Black magic
    logger.debug("In Black Magic")
    _navigate_to_position(position)
    logger.debug(f"Other battle menu: {memory.main.other_battle_menu()}")
    while memory.main.other_battle_menu():
        xbox.tap_b()  # Cast the Spell
    logger.debug(f"Other battle menu: {memory.main.other_battle_menu()}")
    if direction == "left":
        xbox.tap_left()
    elif direction == "right":
        xbox.tap_right()
    elif direction == "up":
        xbox.tap_up()
    elif direction == "down":
        xbox.tap_down()
    tap_targeting()
    logger.debug("Aeon casting spell")


def heal_up(chars=3, *, full_menu_close=True):
    logger.info(f"Menuing, healing characters: {chars}")
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
    target_pos = memory.main.get_character_index_in_main_menu(1)
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
    while not memory.main.cure_menu_open():
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
            logger.debug(f"Current hp: {current_hp}")
            while memory.main.assign_ability_to_equip_cursor() != cur_position:
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


def lancet_swap(direction):
    logger.debug("Lancet Swap function")
    # Assumption is formation: Tidus, Wakka, Auron, Kimahri, and Yuna in last slot.
    direction = direction.lower()
    buddy_swap_kimahri()

    lancet(direction)

    screen.await_turn()
    flee_all()


def lancet(direction):
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


def lancet_target(target, direction):
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
    while memory.main.other_battle_menu():
        xbox.tap_b()
    retry = 0
    if memory.main.get_enemy_current_hp()[target - 20] != 0:
        # Only lancet living targets.
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

    tap_targeting()


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


def flee_all():
    logger.debug("Attempting escape (all party members and end screen)")
    if memory.main.battle_active():
        while memory.main.battle_active():
            if memory.main.user_control():
                return
            if memory.main.turn_ready():
                tidus_position = memory.main.get_battle_char_slot(0)
                logger.debug(f"Tidus Position: {tidus_position}")
                if screen.turn_tidus():
                    tidus_flee()
                elif tidus_position >= 3 and tidus_position != 255:
                    buddy_swap_tidus()
                elif (
                    not check_tidus_ok()
                    or tidus_position == 255
                    or memory.main.tidus_escaped_state()
                ):
                    escape_one()
                else:
                    defend()
    memory.main.click_to_control_3()
    logger.info("Flee complete")


def escape_all():
    logger.info("escape_all function")
    while not screen.battle_complete():
        if memory.main.turn_ready():
            escape_one()


def escape_action():
    while memory.main.main_battle_menu():
        if memory.main.battle_complete():
            break
        else:
            xbox.tap_right()
    logger.debug("In other battle menu")
    while memory.main.battle_cursor_2() != 2:
        if memory.main.battle_complete():
            break
        else:
            xbox.tap_down()
    logger.debug("Targeted Escape")
    while memory.main.other_battle_menu():
        if memory.main.battle_complete():
            break
        else:
            xbox.tap_b()
    if memory.main.battle_active():
        logger.debug("Selected Escaping")
        tap_targeting()


def escape_one():
    next_action_escape = rng_track.next_action_escape(
        character=memory.main.get_current_turn()
    )
    logger.debug(f"##### The next character will escape: {next_action_escape}")
    if not next_action_escape and not memory.main.get_encounter_id() == 26:
        if memory.main.get_story_progress() < 154:
            logger.debug("Character cannot escape (Lagoon). Attacking instead.")
            attack("none")
        else:
            logger.debug("Character will not escape. Looking for a replacement.")
            replacement = 255
            replace_array = memory.main.get_battle_formation()
            for i in range(len(replace_array)):
                if replacement != 255:
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
                    tidus_flee()
                    return False
                elif memory.main.get_current_turn() == 1:
                    escape_action()
                else:
                    attack_by_num(num=memory.main.get_current_turn(), direction="u")
                    return False
    else:
        escape_action()
        logger.debug("Attempting escape, one person")
        return True


def buddy_swap_char(character):
    memory.main.wait_frames(6)
    logger.debug("Swapping characters (in battle) - by char num")
    position = memory.main.get_battle_char_slot(character)

    if position < 3:
        char_name = memory.main.name_from_number(character)
        logger.debug(
            f"Cannot swap with character {char_name}, that character is in the front party."
        )
        return
    else:
        while not memory.main.other_battle_menu():
            xbox.l_bumper()
        position -= 3
        reserveposition = position % 4
        logger.debug(f"Character is in reserve position {reserveposition}")
        if reserveposition == 3:  # Swap with last slot
            direction = "up"
        else:
            direction = "down"

        while reserveposition != memory.main.battle_cursor_2():
            if direction == "down":
                xbox.tap_down()
            else:
                xbox.tap_up()

        while memory.main.other_battle_menu():
            xbox.tap_b()
        xbox.click_to_battle()
        screen.await_turn()
        return


def buddy_swap_tidus():
    logger.debug("++Swapping in Tidus")
    buddy_swap_char(0)


def buddy_swap_yuna():
    logger.debug("++Swapping in Yuna")
    buddy_swap_char(1)


def buddy_swap_auron():
    logger.debug("++Swapping in Auron")
    buddy_swap_char(2)


def buddy_swap_kimahri():
    logger.debug("++Swapping in Kimahri")
    buddy_swap_char(3)


def buddy_swap_wakka():
    logger.debug("++Swapping in Wakka")
    buddy_swap_char(4)


def buddy_swap_lulu():
    logger.debug("++Swapping in Lulu")
    buddy_swap_char(5)


def buddy_swap_rikku():
    logger.debug("++Swapping in Rikku")
    buddy_swap_char(6)


def wrap_up():
    logger.debug("^^Wrapping up battle.")
    while not memory.main.user_control():
        if memory.main.menu_open() or memory.main.diag_skip_possible():
            xbox.tap_b()
        elif memory.main.turn_ready():
            logger.debug("^^Still someone's turn. Could not wrap up battle.")
            return False
        else:
            pass
    logger.debug("^^Wrap up complete.")
    return True


def impulse(direction=None, target_far_line=False):
    while memory.main.battle_menu_cursor() != 217:
        if memory.main.battle_menu_cursor() == 216:
            xbox.tap_down()
        else:
            xbox.tap_up()
    while not memory.main.other_battle_menu():
        xbox.tap_b()
    if direction == "left":
        xbox.tap_left()
    if target_far_line:
        while not memory.main.battle_line_target():
            xbox.tap_left()
    tap_targeting()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()


@battle.utils.speedup_decorator
def sin_arms():
    logger.info("Fight start: Sin's Arms")
    # Area for improvement later. Multiple skippable FMVs
    xbox.click_to_battle()
    aeon_summon(4)
    while memory.main.battle_active():  # Arm1
        if memory.main.turn_ready():
            impulse()
            xbox.tap_b()
            xbox.tap_b()
        else:
            xbox.tap_b()

    xbox.skip_dialog(0.3)
    while not memory.main.battle_active():
        if memory.main.cutscene_skip_possible():
            xbox.skip_scene()
        elif memory.main.menu_open() or memory.main.diag_skip_possible():
            xbox.tap_b()

    aeon_summon(4)

    while memory.main.battle_active():  # Arm2
        if memory.main.turn_ready():
            impulse()
            xbox.tap_b()
            xbox.tap_b()
        else:
            xbox.tap_b()

    xbox.skip_dialog(0.3)
    while not memory.main.battle_active():
        if memory.main.cutscene_skip_possible():
            xbox.skip_scene()
        elif memory.main.menu_open() or memory.main.diag_skip_possible():
            xbox.tap_b()

    xbox.click_to_battle()  # Start of Sin Core
    aeon_summon(4)
    screen.await_turn()
    if game_vars.nemesis():
        while not memory.main.battle_complete():
            if memory.main.turn_ready():
                attack("none")
    else:
        impulse(target_far_line=True)
        xbox.tap_b()
        xbox.tap_b()

    while not memory.main.user_control():
        if memory.main.diag_skip_possible() or memory.main.menu_open():
            xbox.tap_b()
        elif memory.main.cutscene_skip_possible():
            xbox.skip_scene()
    logger.info("Done with Sin's Arms section")


@battle.utils.speedup_decorator
def sin_face():
    logger.info("Fight start: Sin's Face")
    xbox.click_to_battle()
    FFXC.set_neutral()

    aeon_first_turn = True
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if screen.turn_yuna():
                aeon_summon(4)
            elif screen.turn_aeon():
                if aeon_first_turn:
                    impulse()
                    aeon_first_turn = False
                else:
                    attack("none")
            else:
                defend()
        else:
            xbox.tap_b()


@battle.utils.speedup_decorator
def yojimbo():
    while not memory.main.turn_ready():
        pass
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if screen.turn_yuna():
                aeon_summon(4)
            elif screen.turn_aeon():
                attack("none")
            else:
                defend()
        elif memory.main.diag_skip_possible():
            xbox.tap_b()


def omnis_items():
    item1 = 99
    if memory.main.get_item_slot(32) < 200:
        item1 = 32
    elif memory.main.get_item_slot(30) < 200:
        item1 = 30
    elif memory.main.get_item_slot(27) < 200:
        item1 = 27
    else:
        item1 = 24

    if memory.main.get_item_slot(1) < 200:
        item2 = 1
    elif memory.main.get_item_slot(3) < 200:
        item2 = 3
    elif memory.main.get_item_slot(2) < 200:
        item2 = 2
    else:
        item2 = 7
    return [item1, item2]


@battle.utils.speedup_decorator
def bfa_nem():
    FFXC.set_movement(1, 0)
    memory.main.wait_frames(30 * 0.4)
    FFXC.set_movement(1, 1)
    memory.main.wait_frames(30 * 3)
    FFXC.set_neutral()
    tidus_first_turn = False

    xbox.click_to_battle()

    while memory.main.battle_active():
        if memory.main.turn_ready():
            if screen.turn_tidus():
                if tidus_first_turn:
                    equip_in_battle(equip_type="weap", ability_num=0x8019, character=0)
                    tidus_first_turn = True
                else:
                    attack("none")
            else:
                defend()

    while memory.main.get_story_progress() < 3400:  # End of game
        if memory.main.battle_active():
            if memory.main.turn_ready():
                if screen.turn_tidus():
                    if (
                        memory.main.get_encounter_id() == 401
                        and memory.main.overdrive_state_2()[0] == 100
                    ):
                        battle.overdrive.tidus()
                    else:
                        attack("none")
                elif screen.turn_yuna():
                    buddy_swap_wakka()
                elif screen.turn_auron():
                    buddy_swap_lulu()
                else:
                    defend()
        elif memory.main.cutscene_skip_possible():
            memory.main.wait_frames(2)
            if memory.main.cutscene_skip_possible():
                xbox.skip_scene()
        elif memory.main.diag_skip_possible():
            xbox.tap_b()


def yu_yevon_item():
    if memory.main.get_item_slot(6) < 200:
        return 6
    elif memory.main.get_item_slot(7) < 200:
        return 7
    elif memory.main.get_item_slot(8) < 200:
        return 8
    elif memory.main.get_item_slot(2) < 200:
        return 2
    elif memory.main.get_item_slot(1) < 200:
        return 1
    elif memory.main.get_item_slot(0) < 200:
        return 0
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
    if battle == "tutorial":
        item1 = memory.main.get_item_slot(73)
        logger.debug(f"Ability sphere in slot: {item1}")
        item2 = item1
    elif battle == "Evrae":
        if game_vars.skip_kilika_luck():
            item1 = memory.main.get_item_slot(81)
            logger.debug(f"Lv1 sphere in slot: {item1}")
            item2 = memory.main.get_item_slot(84)
            logger.debug(f"Lv4 sphere in slot: {item2}")
        else:
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
        item2 = memory.main.get_item_slot(85)
        logger.debug(f"Mdef Sphere in slot: {item2}")
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

    while not memory.main.other_battle_menu():
        xbox.tap_left()

    while not memory.main.interior_battle_menu():
        xbox.tap_b()
    rikku_od_items(item1)
    while not memory.main.rikku_overdrive_item_selected_number():
        xbox.tap_b()
    rikku_od_items(item2)
    while memory.main.interior_battle_menu():
        xbox.tap_b()
    tap_targeting()


def equip_in_battle(equip_type="weap", ability_num=0, character=0, special="none"):
    equip_type = equip_type.lower()
    while memory.main.main_battle_menu():
        xbox.tap_right()
    if equip_type == "weap":
        equip_handles = memory.main.weapon_array_character(character)
    else:
        while memory.main.battle_cursor_2() != 1:
            xbox.tap_down()
        equip_handles = memory.main.armor_array_character(character)
    while memory.main.other_battle_menu():
        xbox.tap_b()

    logger.debug("@@@@@")
    logger.debug(f"Character: {character}")
    logger.debug(f"Equipment type: {equip_type}")
    logger.debug(f"Number of items: {len(equip_handles)}")
    logger.debug(f"Special: {special}")
    logger.debug("@@@@@")
    equip_num = 255
    i = 0
    while len(equip_handles) > 0:
        current_handle = equip_handles.pop(0)
        logger.debug(current_handle.abilities())
        if special == "baroque":
            if current_handle.abilities() == [0x8063, 255, 255, 255]:
                equip_num = i
        elif special == "brotherhood":
            if current_handle.abilities() == [32867, 32868, 32810, 32768]:
                equip_num = i
        elif ability_num == 0:
            logger.debug("Equipping just the first available equipment.")
            equip_num = 0
        elif current_handle.has_ability(ability_num):  # First Strike for example
            equip_num = i
        i += 1
    while memory.main.battle_cursor_3() != equip_num:
        logger.debug(f"'''Battle cursor 3: {memory.main.battle_cursor_3()}")
        logger.debug(f"'''equip_num: {equip_num}")
        if memory.main.battle_cursor_3() < equip_num:
            xbox.tap_down()
        else:
            xbox.tap_up()
    while memory.main.interior_battle_menu():
        xbox.tap_b()

    logger.debug(f"Desired equipment is in slot {equip_num}")


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


def calculate_spare_change_movement(gil_amount):
    if gil_amount > memory.main.get_gil_value():
        gil_amount = memory.main.get_gil_value()
    gil_amount = min(gil_amount, 100000)
    position = {}
    gil_copy = gil_amount
    for index in range(0, 7):
        amount = get_digit(gil_amount, index)
        if amount > 5:
            gil_amount += 10 ** (index + 1)
        position[index] = amount
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
    logger.debug(f"#####Battle Number: {memory.main.get_encounter_id()}")
    if memory.main.get_overdrive_battle(
        6
    ) != 100 and memory.main.get_encounter_id() in [
        360,
        361,
        376,
        378,
        381,
        384,
        386,
    ]:
        if (
            not memory.main.tidus_escaped_state() and not check_tidus_ok()
        ) or not check_rikku_ok():
            logger.debug("Tidus or Rikku incapacitated, fleeing")
            logger.debug(f"-- {not memory.main.tidus_escaped_state()}")
            logger.debug(f"-- {not check_tidus_ok()}")
            logger.debug(f"-- {not check_rikku_ok()}")
            flee_all()
        else:
            while not memory.main.battle_complete():
                if memory.main.turn_ready():
                    turn_char = memory.main.get_battle_char_turn()
                    if turn_char == 6:
                        attack_by_num(6, direction="u")
                    elif memory.main.get_overdrive_battle(6) == 100:
                        flee_all()
                    elif 6 not in memory.main.get_active_battle_formation():
                        buddy_swap_rikku()
                    else:
                        escape_one()
        memory.main.click_to_control_3()
    else:
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
    logger.debug(f"++ Calm Lands Battle number: {memory.main.get_encounter_id()}")
    rng_10_next_chance_low = memory.main.next_chance_rng_10(12)
    low_array = [273, 275, 276, 281, 283, 284]
    rng_10_next_chance_mid = memory.main.next_chance_rng_10(60)
    mid_array = [277, 279, 285, 287, 289, 290]
    rng_10_next_chance_high = memory.main.next_chance_rng_10(128)
    high_array = [278, 286, 288]
    if check_gems() < 2:
        logger.debug(f"++++ Gems: {check_gems()}")
        logger.debug("++++ Calm Lands battle, need gems.")
        calm_lands_gems()
    else:
        logger.debug("++++ Gems good. NEA manip logic.")
        advance_pre_x, advance_post_x = rng_track.nea_track()  # returns integers
        if advance_pre_x not in [0, 2] and advance_post_x not in [0, 2]:
            # Non-zero for both
            logger.debug("Not lined up for NEA")
            if (
                rng_10_next_chance_low == 0
                and memory.main.get_encounter_id() in low_array
            ):
                advance_rng_12()
            elif (
                rng_10_next_chance_mid == 0
                and memory.main.get_encounter_id() in mid_array
            ):
                advance_rng_12()
            elif (
                rng_10_next_chance_high == 0
                and memory.main.get_encounter_id() in high_array
            ):
                advance_rng_12()
            else:  # If we can't advance on this battle, try to get the next "mid" level advance.
                logger.debug("Can't drop off of this battle.")
                advance_rng_10(rng_10_next_chance_mid)
        elif advance_post_x == 2:
            # Lined up for non-drop defender X + drops on B&Y drops.
            if memory.main.next_chance_rng_10() == 0:
                advance_rng_10(1)
                # Don't want to have Defender X drop an item
            else:
                flee_all()
        elif advance_post_x == 0:  # Lined up for next drop NEA before defender X.
            logger.debug("The next equipment to drop will be NEA")
            if memory.main.get_coords()[0] > 1300:
                logger.debug("--Near Gagazet, just get off RNG10 equipment drop.")
                if memory.main.next_chance_rng_10() == 0:
                    advance_rng_10(1)
                    # Gets us off of a drop on defender X - probably. :D
                    # Don't want to have Defender X drop an item
                else:
                    flee_all()
            elif memory.main.next_chance_rng_10_calm():
                advance_rng_10(memory.main.next_chance_rng_10_calm())
            else:
                logger.debug("Lined up OK, ready for NEA. Just flee.")
                flee_all()
        elif advance_pre_x == 2:  # Lined up for drops on defender X + B&Y drops.
            if memory.main.next_chance_rng_10() != 0:
                advance_rng_10(memory.main.next_chance_rng_10())
            else:
                logger.debug("Perfectly lined up pre-X + B&Y. Just flee.")
                flee_all()
        elif advance_pre_x == 0:
            logger.debug("The second equipment drop from now will be NEA.")
            if memory.main.next_chance_rng_10() != 0:
                advance_rng_10(memory.main.next_chance_rng_10())
                # Trying to get onto a good drop.
            else:
                logger.debug("Perfectly lined up pre-X. Just flee.")
                flee_all()
        else:
            logger.debug("Fallback logic, not sure.")
            memory.main.wait_frames(180)
            flee_all()


def calm_steal():
    if memory.main.get_encounter_id() == 313:
        _steal("down")
    elif memory.main.get_encounter_id() == 289:
        _steal("up")
    elif memory.main.get_encounter_id() == 314:
        _steal("right")
    else:
        _steal()


def advance_rng_10(num_advances: int):
    escape_success_count = 0
    logger.debug("#################")
    logger.debug("###RNG10 logic###")
    logger.debug(f"##    {num_advances}      ##")
    logger.debug(f"##    {screen.faint_check()}      ##")
    logger.debug("#################")
    while memory.main.battle_active():
        if memory.main.turn_ready():
            logger.debug(f"+++Registering advances: {num_advances}")
            if memory.main.battle_type() == 2:
                logger.debug("+++Registering ambush")
                flee_all()
            elif memory.main.get_encounter_id() == 321:
                logger.debug("+++Registering evil jar guy, fleeing.")
                flee_all()
            elif memory.main.get_encounter_id() == 287:
                logger.debug("+++Registering Anaconadeur - I am French!!! - fleeing")
                flee_all()
            elif num_advances >= 6:
                if escape_success_count == 0:
                    if escape_one():
                        escape_success_count += 1
                elif faint_check_with_escapes() == 2:
                    logger.debug("+++Registering two people down. Escaping.")
                    flee_all()
                elif screen.turn_kimahri() or screen.turn_rikku():
                    logger.debug("+++Registering turn, steal character")
                    # Most convenient since overdrive is needed for Flux.
                    if num_advances % 3 != 0:
                        calm_steal()
                        num_advances -= 1
                    elif escape_success_count == 0:
                        if escape_one():
                            escape_success_count += 1
                    else:
                        defend()
                elif (
                    3 in memory.main.get_battle_formation()
                    and 3 not in memory.main.get_active_battle_formation()
                    and num_advances % 3 != 0
                ):
                    buddy_swap_kimahri()
                elif escape_success_count == 0:
                    if escape_one():
                        escape_success_count += 1
                else:
                    defend()
            elif num_advances >= 3:
                if faint_check_with_escapes() >= 1:
                    flee_all()
                elif escape_success_count == 0:
                    if escape_one():
                        escape_success_count += 1
                elif screen.turn_rikku() and escape_success_count == 1:
                    if escape_one():
                        escape_success_count += 1
                elif screen.turn_kimahri():
                    logger.debug("+++Registering turn, steal character")
                    # Most convenient since overdrive is needed for Flux.
                    if num_advances % 3 != 0:
                        calm_steal()
                        num_advances -= 1
                    else:
                        defend()
                elif (
                    3 in memory.main.get_battle_formation()
                    and 3 not in memory.main.get_active_battle_formation()
                    and num_advances % 3 != 0
                ):
                    buddy_swap_kimahri()
                elif escape_success_count in [0, 1]:
                    if escape_one():
                        escape_success_count += 1
                else:
                    defend()
            elif num_advances in [1, 2]:
                logger.debug("+++Registering advances:", num_advances)
                if screen.turn_kimahri():
                    logger.debug("+++Registering turn, steal character")
                    calm_steal()
                    num_advances -= 1
                elif 3 not in memory.main.get_active_battle_formation():
                    buddy_swap_kimahri()
                elif screen.turn_tidus():
                    flee_all()
                elif 0 not in memory.main.get_active_battle_formation():
                    buddy_swap_tidus()
                else:
                    defend()  # should not occur.
            else:  # any other scenarios, ready to advance.
                logger.debug("+++Registering no advances needed, forcing flee.")
                flee_all()
    memory.main.click_to_control_3()


def rng_12_attack(try_impulse=False):
    logger.debug("#################")
    logger.debug("###RNG12 logic (attack only) ###")
    logger.debug("#################")
    if screen.turn_aeon():
        if memory.main.get_encounter_id() in [283, 309, 313]:
            attack_by_num(21, "u")  # Second target
        elif memory.main.get_encounter_id() in [284]:
            attack_by_num(22, "u")  # Third target
        elif memory.main.get_encounter_id() in [275, 289]:
            attack_by_num(21, "r")  # Second target, aim right (aeon only)
        elif memory.main.get_encounter_id() in [303]:
            attack_by_num(21, "l")  # Second target
        elif memory.main.get_encounter_id() in [304]:
            attack_by_num(23, "u")  # fourth target
        elif memory.main.get_encounter_id() in [314]:
            attack_by_num(21, "r")
        else:
            attack("none")
    else:  # Non-aeon logic, fix this later.
        attack("none")


def advance_rng_12():
    logger.debug("#################")
    logger.debug("###RNG12 logic (decision logic) ###")
    logger.debug("#################")
    attack_count = False
    aeon_turn = False
    use_impulse = False
    double_drop = False
    while memory.main.battle_active():
        if memory.main.get_encounter_id() == 321:
            logger.debug("+++Registering evil jar guy")
            logger.debug("Aw hell naw, we want nothing to do with this guy!")
            flee_all()
        elif memory.main.turn_ready():
            pre_x, post_x = rng_track.nea_track()
            if post_x == 1:
                advances = 1
            elif memory.main.get_map() == 223:
                advances = pre_x
            else:
                advances = post_x
            if screen.turn_yuna():
                if aeon_turn:
                    flee_all()
                else:
                    aeon_summon(4)
            elif screen.turn_aeon():
                num_enemies = len(memory.main.get_enemy_current_hp())
                logger.debug(f"+++ {memory.main.get_enemy_current_hp()}")
                logger.debug(f"+++ {num_enemies}")
                check_ahead = num_enemies * 3
                logger.debug(f"+++ {check_ahead}")
                ahead_array = memory.main.next_chance_rng_10_full()
                for h in range(check_ahead):
                    if h == 3:
                        pass
                    elif h % 3 != 0 and ahead_array[h]:
                        double_drop = True
                for i in range(7):
                    if ahead_array[i + check_ahead] and not attack_count:
                        use_impulse = True
                if not attack_count:
                    if memory.main.get_encounter_id() in [314]:
                        impulse()
                        attack_count = True
                    elif advances >= 2:
                        impulse()
                        attack_count = True
                    elif advances == 1:
                        if use_impulse and not double_drop:
                            impulse()
                            attack_count = True
                        else:
                            attack_count = True
                            rng_12_attack()
                    else:
                        aeon_dismiss()
                else:
                    aeon_dismiss()
                aeon_turn = True
            else:
                if aeon_turn:
                    flee_all()
                elif 1 not in memory.main.get_active_battle_formation():
                    buddy_swap_yuna()
                else:
                    defend()
    memory.main.click_to_control_3()


@battle.utils.speedup_decorator
def ghost_kill():
    import rng_track

    next_drop, _ = rng_track.item_to_be_dropped()
    owner1 = next_drop.equip_owner
    owner2 = next_drop.equip_owner_alt
    silence_slot_check = memory.main.get_item_slot(39)
    if silence_slot_check == 255:
        silence_slot = 255
    else:
        silence_slot = memory.main.get_use_items_slot(39)
    tidus_hasted = False

    if memory.main.next_chance_rng_10():
        tidus_hasted = ghost_advance_rng_10_silence(
            silence_slot=silence_slot, owner_1=owner1, owner_2=owner2
        )
        silence_slot = 255  # will be used while prepping RNG10 anyway.

    if owner2 in [0, 4, 6]:
        logger.debug(f"Aeon kill results in NEA on char:{owner2}")
        ghost_kill_aeon()
    elif silence_slot > 200:
        logger.debug(f"No silence grenade, going with aeon kill: {owner2}")
        ghost_kill_aeon()
    elif owner1 in [0, 4, 6]:
        logger.debug(f"Any character kill results in NEA on char:{owner1}")
        ghost_kill_any(silence_slot=silence_slot, self_haste=tidus_hasted)
    elif owner1 == 9:
        logger.debug(f"Has to be Tidus kill: {owner1}")
        ghost_kill_tidus(silence_slot=silence_slot, self_haste=tidus_hasted)
    else:
        logger.debug(f"No way to get an optimal drop. Resorting to aeon: {owner2}")
        ghost_kill_aeon()

    memory.main.click_to_control_3()


def ghost_advance_rng_10_silence(silence_slot: int, owner_1: int, owner_2: int):
    logger.debug("RNG10 is not aligned. Special logic to align.")
    # Premise is that we must have a silence grenade in inventory.
    # We should force extra manip in gorge if no silence grenade,
    # so should be guaranteed if this triggers.
    pref_drop = [0, 4, 6]
    silence_used = False
    tidus_hasted = False
    while memory.main.next_chance_rng_10():
        if memory.main.turn_ready():
            if not silence_used:
                if 6 not in memory.main.get_active_battle_formation():
                    buddy_swap_rikku()
                    use_item(slot=silence_slot)  # Throw silence grenade
                    silence_used = True
                elif 3 not in memory.main.get_active_battle_formation():
                    buddy_swap_kimahri()
                    use_item(slot=silence_slot)  # Throw silence grenade
                    silence_used = True
                elif screen.turn_rikku() or screen.turn_kimahri():
                    use_item(slot=silence_slot)  # Throw silence grenade
                    silence_used = True
                else:
                    defend()
            # Next, put in preferred team
            elif owner_2 in pref_drop or owner_1 not in pref_drop:  # prefer aeon kill
                if screen.turn_rikku() or screen.turn_kimahri():
                    steal()
                elif 6 not in memory.main.get_active_battle_formation():
                    buddy_swap_rikku()
                elif 3 not in memory.main.get_active_battle_formation():
                    buddy_swap_kimahri()
                elif 0 not in memory.main.get_active_battle_formation():
                    buddy_swap_tidus()
                else:
                    defend()
            else:  # Will need a non-Aeon kill
                if screen.turn_rikku() or screen.turn_kimahri():
                    steal()
                elif 6 not in memory.main.get_active_battle_formation():
                    buddy_swap_rikku()
                elif 0 not in memory.main.get_active_battle_formation():
                    buddy_swap_tidus()
                elif 3 not in memory.main.get_active_battle_formation():
                    buddy_swap_kimahri()
                elif screen.turn_tidus() and not tidus_hasted:
                    tidus_hasted = True
                    tidus_haste("none")
                elif memory.main.get_enemy_current_hp()[0] > 3000:
                    attack()
                else:
                    defend()
    logger.debug("RNG10 is now aligned.")
    return tidus_hasted


def ghost_kill_tidus(silence_slot: int, self_haste: bool):
    logger.debug(f"++Silence slot: {silence_slot}")
    while memory.main.battle_active():
        # Try to get NEA on Tidus
        if memory.main.turn_ready():
            if 0 not in memory.main.get_active_battle_formation():
                logger.debug("+++Get Tidus back in")
                buddy_swap_tidus()
            elif screen.turn_tidus():
                if not self_haste:
                    tidus_haste("none")
                    self_haste = True
                elif (
                    memory.main.get_enemy_current_hp()[0] <= 2800
                    and memory.main.get_overdrive_battle(0) == 100
                ):
                    battle.overdrive.tidus()
                else:
                    attack("none")
            elif 1 not in memory.main.get_active_battle_formation():
                logger.debug("+++Get Yuna in for extra smacks")
                buddy_swap_yuna()
            elif screen.turn_yuna() and memory.main.get_enemy_current_hp()[0] > 3000:
                attack("none")
            else:
                defend()


def ghost_kill_any(silence_slot: int, self_haste: bool):
    yuna_haste = False
    item_thrown = silence_slot >= 200
    logger.debug(f"++Silence slot: {silence_slot}")
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if 0 not in memory.main.get_active_battle_formation():
                logger.debug("+++Get Tidus back in")
                buddy_swap_tidus()
            elif screen.turn_tidus():
                if not self_haste:
                    tidus_haste("none")
                    self_haste = True
                elif (
                    1 in memory.main.get_active_battle_formation()
                    and not yuna_haste
                    and memory.main.get_enemy_current_hp()[0] <= 6000
                ):
                    tidus_haste(direction="l", character=1)
                    yuna_haste = True
                elif (
                    memory.main.get_enemy_current_hp()[0] <= 2800
                    and memory.main.get_overdrive_battle(0) == 100
                ):
                    battle.overdrive.tidus()
                else:
                    attack("none")
            elif 1 not in memory.main.get_active_battle_formation():
                logger.debug("+++Get Yuna in for extra smacks")
                buddy_swap_yuna()
            elif screen.turn_yuna():
                attack("none")
            else:
                defend()


def ghost_kill_aeon():
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if screen.turn_aeon():
                attack("none")
            elif 1 not in memory.main.get_active_battle_formation():
                buddy_swap_yuna()
            elif screen.turn_yuna():
                aeon_summon(4)
            else:
                defend()
