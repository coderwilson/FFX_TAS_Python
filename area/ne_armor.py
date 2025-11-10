import logging

import battle.main
import logs
import memory.main
import menu
import pathing
import rng_track
import save_sphere
import tts
import vars
import xbox
from paths import (
    GagazetNELoopback,
    NEApproach,
    NEForceEncountersGreen,
    NEForceEncountersWhite,
    NEReturn,
    NEReturnGreen,
)
from players import Auron, Rikku, Tidus
from json_ai_files.write_seed import write_big_text

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def loop_back_from_ronso(checkpoint=0):
    write_big_text("")
    memory.main.update_formation(Tidus, Rikku, Auron)
    battle.main.heal_up(full_menu_close=True)
    rng_track.print_manip_info()
    logger.info("Looping back to the Ronso")
    while checkpoint != 18:
        if memory.main.user_control():
            if checkpoint < 13 and memory.main.get_map() == 279:
                checkpoint = 13
            elif pathing.set_movement(GagazetNELoopback.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.menu_open():
                xbox.tap_confirm()
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()


def to_hidden_cave():
    next_green(report=True)
    memory.main.update_formation(Tidus, Rikku, Auron)
    battle.main.heal_up(full_menu_close=True)
    rng_track.print_manip_info()
    last_report = False
    first_save = False
    checkpoint = 0
    prep_battles = 0
    #next_drop, advances = rng_track.nea_track()
    #nea_possible_check, next_drop = rng_track.final_nea_check()
    _, next_drop = rng_track.final_nea_check()
    nea_possible_check = True
    write_str = f"Next drop: {next_drop}\nRNG10: "
    write_str += str(memory.main.next_chance_rng_10())
    write_big_text(write_str)
    while memory.main.get_map() != 56:
        #if not nea_possible_check or next_drop == 99:
        #    return False
        if memory.main.user_control():
            if checkpoint < 5 and memory.main.get_map() == 266:
                checkpoint = 5
            if checkpoint == 7 and not first_save:
                save_sphere.touch_and_go()
                first_save = True
            if checkpoint == 8 and (
                next_drop >= 1 or memory.main.next_chance_rng_10() >= 9
            ):
                write_big_text(f"Need {next_drop} Epaaj kills.")
                if not last_report:
                    logger.info("Need more advances before entering cave.")
                    last_report = True
                checkpoint -= 2
            elif (
                checkpoint == 8
                and memory.main.get_item_slot(39) == 255
                and memory.main.next_chance_rng_10() > 4
            ):
                if not last_report:
                    logger.info("No silence grenade | Advancing further before cave")
                    last_report = True
                checkpoint -= 2
            elif checkpoint == 9:
                FFXC.set_movement(-1, 1)
            elif pathing.set_movement(NEApproach.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                last_report = False
                logger.info("### Starting manip battle")
                rng_track.print_manip_info()
                memory.main.wait_frames(2)
                if next_drop >= 1:
                    if memory.main.next_chance_rng_10() != 0:
                        battle.main.advance_rng_10(memory.main.next_chance_rng_10())
                    else:
                        battle.main.advance_rng_12()
                elif memory.main.next_chance_rng_10():
                    battle.main.advance_rng_10(memory.main.next_chance_rng_10())
                else:
                    logger.error("Failed to determine next steps, requires dev review.")
                    logger.error(f"RNG10: {memory.main.next_chance_rng_10()}")
                    logger.error(f"RNG12: {memory.main.next_chance_rng_12()}")
                    battle.main.flee_all()
                prep_battles += 1
                game_vars.ne_battles_increment()
                memory.main.update_formation(Tidus, Rikku, Auron)
                save_sphere.touch_and_go()
                #next_drop, advances = rng_track.nea_track()
                nea_possible_check, next_drop = rng_track.final_nea_check()
                rng_track.print_manip_info()
                write_str = f"Next drop: {next_drop}\nRNG10: "
                write_str += str(memory.main.next_chance_rng_10())
                write_big_text(write_str)
            elif memory.main.menu_open():
                xbox.tap_confirm()
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
    logs.write_stats("NEA extra manip battles:")
    logs.write_stats(prep_battles)
    return True


def next_green(report:bool = False) -> bool:
    next_green_val = [0, 0, 0]
    next_green_val[0] = memory.main.next_chance_rng_01(version="green")[0][0]
    next_green_val[1] = memory.main.next_chance_rng_01(version="green")[0][1]
    next_green_val[2] = memory.main.next_chance_rng_01(version="green")[0][2]
    next_white = memory.main.next_chance_rng_01()[0][0]
    logger.manip("Next Ghost coming up:")
    logger.manip(
        f"Green: {next_green_val[0]}, {next_green_val[1]}, {next_green_val[2]}"
    )
    logger.manip(f"White: {next_white}")
    go_green = False
    if next_green_val[0] < next_white:
        if next_green_val[0] >= 2:
            go_green = True
            if report:
                write_big_text(f"Green - Extra battles: {next_green_val[0]}")
    if not go_green and next_green_val[1] < next_white:
        if next_green_val[1] >= 2:
            go_green = True
            if report:
                write_big_text(f"Green - Extra battles: {next_green_val[1]}")
    if not go_green and next_green_val[2] < next_white:
        if next_green_val[2] >= 2:
            go_green = True
            if report:
                write_big_text(f"Green - Extra battles: {next_green_val[2]}")
    logger.debug(f"## Going to Green: {go_green}")
    if game_vars.accessibility_vars()[2]:
        if go_green:
            tts.message("Green")
            tts.message(str(next_green_val))
        else:
            tts.message("White")
            tts.message(str(next_white))
            if report:
                write_big_text(f"White - Extra battles: {next_white}")
    return go_green


def drop_hunt():
    logger.info("Now in the cave. Ready to try to get the NE armor.")
    memory.main.update_formation(Tidus, Rikku, Auron)

    go_green = next_green()

    rng_track.print_manip_info()
    checkpoint = 0
    pre_ghost_battles = 0
    while game_vars.ne_armor() == 255:
        if memory.main.user_control():
            if go_green:
                if checkpoint == 15:
                    checkpoint -= 2
                elif pathing.set_movement(NEForceEncountersGreen.execute(checkpoint)):
                    checkpoint += 1
                    logger.debug(f"Checkpoint {checkpoint}")
            else:
                if pathing.set_movement(NEForceEncountersWhite.execute(checkpoint)):
                    checkpoint += 1
                    if checkpoint == 2:
                        checkpoint = 0
                    logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                write_big_text("")
                if memory.main.get_encounter_id() in [319, 323]:
                    battle.main.ghost_kill()
                else:
                    battle.main.flee_all()
                memory.main.click_to_control_3()
                memory.main.update_formation(Tidus, Rikku, Auron, full_menu_close=False)
                battle.main.heal_up(full_menu_close=False)
                memory.main.check_nea_armor()
                next_green()
                if game_vars.ne_armor() == 255:
                    if next_green() and not go_green:
                        go_green = True
                    pre_ghost_battles += 1
                memory.main.close_menu()
                game_vars.ne_battles_increment()
            elif memory.main.menu_open():
                xbox.tap_confirm()
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
    logger.info(f"The NE armor hunt is complete. Char: {game_vars.ne_armor()}")
    logs.write_stats("Pre-Ghost flees:")
    logs.write_stats(pre_ghost_battles)
    logs.write_stats("NEA char:")
    logs.write_stats(game_vars.ne_armor())


def return_to_gagazet():
    nea_actor = memory.main.name_from_number(char_num=game_vars.ne_armor())
    write_big_text(f"NEA dropped for: {nea_actor}")
    if memory.main.get_coords()[0] > 300:
        go_green = True
        menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        go_green = False

    checkpoint = 0
    while memory.main.get_map() != 259:
        if memory.main.user_control():
            if go_green:
                if checkpoint == 10:
                    go_green = False
                    checkpoint = 0
                elif pathing.set_movement(NEReturnGreen.execute(checkpoint)):
                    checkpoint += 1
                    logger.debug(f"Checkpoint {checkpoint}")
            elif checkpoint < 1 and memory.main.get_map() == 266:
                checkpoint = 1
            elif checkpoint == 2:
                save_sphere.touch_and_go()
                checkpoint += 1
            elif checkpoint < 7 and memory.main.get_map() == 279:
                checkpoint = 7
            elif pathing.set_movement(NEReturn.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle.main.flee_all()
            elif memory.main.menu_open():
                xbox.tap_confirm()
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
