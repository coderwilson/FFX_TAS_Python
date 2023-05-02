# Libraries and Core Files
import json
import logging
import os
from pathlib import Path

import airship_pathing
import area.dream_zan
import logs
import memory.main
import nemesis.arena_prep
import pathing
import reset
import screen
import vars
import xbox
from gamestate import game
from players import Kimahri, Rikku, Tidus

logger = logging.getLogger(__name__)

# This file is intended to load the game to a saved file.
# This assumes that the save is the first non-auto-save in the list of saves.

logger = logging.getLogger(__name__)
FFXC = xbox.controller_handle()
game_vars = vars.vars_handle()


def move_after_load(spec_move: str):
    if spec_move == "miihen_laugh":
        load_miihen_start_laugh()
    elif spec_move == "miihen_no_laugh":
        load_miihen_start()
    elif spec_move == "MRR":
        load_mrr()
    elif spec_move == "Kilika_rng_manip":
        kilika_rng_manip()


def load_into_game(gamestate: str, step_counter: str):
    logger.debug(f"Loading game state {gamestate} | {step_counter}")
    # If wrong maps are loaded in, try to reset.
    if memory.main.get_map() not in [23, 348, 349]:
        reset.reset_to_main_menu()
    area.dream_zan.new_game(gamestate=gamestate)

    # Now to get details for the load/save files
    filepath = os.path.join("json_ai_files", "save_load_details.json")
    with open(filepath, "r") as fp:
        results = json.load(fp)

    # Try to use new method, otherwise try old method.
    try:
        step_counter = str(step_counter)
        num_results = len(results[gamestate][step_counter])
        if num_results == 0:
            logger.debug("Failure 1")
            load_into_game_old(gamestate=gamestate, step_counter=step_counter)
            return

        # Init variables so we don't crash later
        save_num_conf = 0
        blitz_win = "none"
        end_ver = "none"
        nea_zone = "none"
        nem_ap = "none"
        spec_move = "none"

        logger.debug(results[gamestate][step_counter].keys())
        for key in results[gamestate][step_counter]:
            save_num = int(results[gamestate][step_counter][key]["save_num"])

            if save_num > 200:
                pass
            elif key != str(game_vars.nemesis()):
                pass
            else:
                nemesis = key
                logger.debug(f"Found save {save_num}")
                save_num_conf = save_num
                blitz_win = results[gamestate][step_counter][key]["blitz_win_value"]
                end_ver = results[gamestate][step_counter][key]["end_game_version_val"]
                logger.debug(f"Blitz Win {blitz_win}")
                logger.debug(f"End game version {end_ver}")
                nea_zone = results[gamestate][step_counter][key]["nea_zone"]
                nem_ap = results[gamestate][step_counter][key]["nem_ap_val"]
                spec_move = results[gamestate][step_counter][key]["special_movement"]
                logger.debug(f"NEA zone {nea_zone}")
                logger.debug(f"Nemesis checkpoint {nem_ap}")

        if save_num_conf == 0:
            logger.debug("Failure 2")
            load_into_game_old(gamestate=gamestate, step_counter=step_counter)
            return
        else:
            # Perform the load
            load_save_num(int(save_num_conf))
            game_vars.set_blitz_win(value=(blitz_win == "True"))
            game_vars.end_game_version_set(value=int(end_ver))
            if nemesis == str(game_vars.nemesis()):
                game_vars.set_nea_zone(value=int(nea_zone))
                game_vars.set_nem_checkpoint_ap(value=int(nem_ap))

            if spec_move != "none":
                logger.debug(f"Special movement needed: {spec_move}")
                move_after_load(spec_move=spec_move)
            else:
                logger.debug("No Special movement needed")

            logger.debug(f"Blitz Win {game_vars.get_blitz_win()}")
            logger.debug(f"End game version {game_vars.end_game_version()}")
            logger.debug(f"NEA zone {game_vars.get_nea_zone()}")
            logger.debug(f"Nemesis checkpoint {game_vars.nem_checkpoint_ap()}")
            memory.main.check_nea_armor()

    except Exception as err_msg:
        logger.debug(f"Error message: {err_msg}")
        logger.debug("Failure 3")
        load_into_game_old(gamestate=gamestate, step_counter=step_counter)


def load_into_game_old(gamestate: str, step_counter: str):
    xbox.tap_a()
    logger.warning(f"No game state found for vars {gamestate} | {step_counter}")
    
    # Now to tell the user where they went wrong:
    filepath = os.path.join("json_ai_files", "save_load_details.json")
    with open(filepath, "r") as fp:
        results = json.load(fp)
    try:
        if len(results[gamestate]) >= 1:
            logger.warning(f"For game state {gamestate}, the valid values are (in non-sorted order): ")
            list_keys = results[gamestate].keys()
            for key in list_keys:
                logger.warning(key)
    except:
        logger.warning(f"For game states, the valid values are (in non-sorted order): ")
        list_keys = results.keys()
        for key in list_keys:
            logger.warning(key + list_keys[key])
    
    logger.error("TAS terminating")
    exit(1)

def get_saved_files():
    save_files_full = sorted(
        Path(game_vars.game_save_path()).iterdir(), key=os.path.getmtime
    )
    save_files = [os.path.basename(i) for i in save_files_full]
    save_files = save_files[::-1]
    return save_files


def load_save_num(number):
    save_files = get_saved_files()

    # First get the autosave position
    test_string = "ffx_000"
    logger.debug(f"Searching for string: {test_string}")
    save_pos = 255
    for x in range(len(save_files)):
        if save_files[x] == test_string:
            logger.debug(f"Save file is in position: {x}")
            save_pos = x
    save_zero = save_pos
    save_pos = 255
    # Then get the actual save position
    test_string = "ffx_" + str(number).zfill(3)
    logger.debug(f"Searching for string: {test_string}")
    save_pos = 255
    for x in range(len(save_files)):
        if save_files[x] == test_string:
            logger.info(f"Save file is in position: {x}")
            save_pos = x
    if save_zero > save_pos:
        save_pos += 1
    memory.main.wait_frames(20)
    if save_pos != 255:
        while memory.main.load_game_pos() != save_pos:
            if memory.main.load_game_pos() + 4 < save_pos:
                xbox.trigger_r()
            elif memory.main.load_game_pos() < save_pos:
                xbox.tap_down()
            else:
                xbox.tap_up()

        for _ in range(7):
            xbox.tap_b()
        FFXC.set_neutral()
        memory.main.await_control()
        memory.main.wait_frames(5)
        # So that we don't evaluate battle as complete after loading.
        memory.main.reset_battle_end()
    else:
        logger.error("That save file does not exist. Quitting program.")
        exit()


def load_first():
    logger.info("Loading to first save file")
    xbox.menu_b()
    memory.main.wait_frames(30 * 2.5)
    xbox.menu_down()
    memory.main.wait_frames(30 * 0.1)
    xbox.menu_b()
    memory.main.wait_frames(30 * 0.1)
    xbox.menu_b()
    memory.main.await_control()


def load_offset(offset):
    logger.info(f"Loading to save file in position {offset}")
    total_offset = offset
    memory.main.wait_frames(30 * 2.5)
    for _ in range(total_offset):
        xbox.tap_down()
    for _ in range(7):
        xbox.tap_b()
    FFXC.set_neutral()
    memory.main.wait_frames(120)
    # So that we don't evaluate battle as complete after loading.
    memory.main.reset_battle_end()


def load_offset_battle(offset):
    logger.info(f"Loading to save file in position {offset}")
    xbox.menu_b()
    memory.main.wait_frames(30 * 2.5)
    while offset > 0:
        xbox.tap_down()
        offset -= 1
    memory.main.wait_frames(30 * 0.1)
    xbox.menu_b()
    memory.main.wait_frames(30 * 0.1)
    xbox.menu_b()
    memory.main.wait_frames(30 * 3)


def load_mem_cursor():
    memory.main.await_control()
    memory.main.open_menu()
    if memory.main.get_story_progress() <= 200:  # Up to Besaid save, after Trials
        cursor_target = 5
    else:
        cursor_target = 8
    logger.debug(f"Aiming at {cursor_target}")
    while memory.main.get_menu_cursor_pos() != cursor_target:
        logger.debug(memory.main.get_menu_cursor_pos())
        xbox.tap_up()
        logger.debug(memory.main.get_menu_cursor_pos())
        if game_vars.use_pause():
            memory.main.wait_frames(2)
    while memory.main.menu_number() == 5:
        xbox.tap_b()
        if game_vars.use_pause():
            memory.main.wait_frames(90)
    while memory.main.config_cursor() != 3:
        xbox.tap_down()
        if game_vars.use_pause():
            memory.main.wait_frames(1)
    while memory.main.config_cursor_column() != 1:
        xbox.tap_right()
        if game_vars.use_pause():
            memory.main.wait_frames(1)
    memory.main.close_menu()


def load_post_blitz():
    logger.info("Loading to first save file")
    load_offset(1)

    while not screen.Minimap1():
        if screen.Minimap4():
            FFXC.set_value("axis_lx", -1)
            FFXC.set_value("axis_ly", -1)
            memory.main.wait_frames(30 * 0.5)
            FFXC.set_value("axis_lx", 0)
            memory.main.wait_frames(30 * 1)
            FFXC.set_value("axis_ly", 0)
        else:
            xbox.menu_b()

    # Reverse T screen
    FFXC.set_value("axis_lx", 1)
    memory.main.wait_frames(30 * 4.5)
    FFXC.set_value("axis_ly", -1)
    memory.main.wait_frames(30 * 1)
    FFXC.set_value("axis_ly", 0)
    memory.main.wait_frames(30 * 5)
    FFXC.set_value("axis_lx", 0)

    # Carnival vendor screen
    memory.main.await_control()
    FFXC.set_value("axis_ly", 1)
    memory.main.wait_frames(30 * 1.5)
    FFXC.set_value("axis_lx", 1)
    memory.main.wait_frames(30 * 3)
    FFXC.set_value("axis_lx", 0)
    memory.main.wait_frames(30 * 1)
    FFXC.set_value("axis_lx", 1)
    memory.main.wait_frames(30 * 3)
    FFXC.set_value("axis_lx", 0)
    FFXC.set_value("axis_ly", 0)

    logger.debug("Rejoining the party.")
    memory.main.click_to_control()  # Scene, rejoining the party
    logger.debug("Walking up to Yuna.")
    FFXC.set_value("axis_ly", -1)
    FFXC.set_value("axis_lx", -1)
    memory.main.wait_frames(30 * 3)
    FFXC.set_value("axis_lx", 0)
    FFXC.set_value("axis_ly", 0)  # Enters laughing scene, ends Luca section.
    logger.debug("End of loading section.")


def load_neutral():
    load_first()


def load_baaj():
    FFXC.set_movement(1, 0)
    memory.main.wait_frames(30 * 0.4)
    FFXC.set_neutral()
    memory.main.wait_frames(30 * 0.04)


def kilika_rng_manip():
    # Kilika start, RNG01
    # 1904657448
    logger.warning("==== Hard setting value for testing")
    rng_value = 1904657448
    memory.main.set_rng_by_index(value=rng_value, index=1)

    # Basically, hunt until we don't find a good battle in 'advances'
    advances = 5
    import area.kilika
    import rng_track

    next_two = rng_track.coming_battles(
        area="kilika_woods", battle_count=advances, extra_advances=1
    )
    while area.kilika.select_best_of_two(next_two) != 99:
        rng_value += 1
        memory.main.set_rng_by_index(value=rng_value, index=1)
        next_two = rng_track.coming_battles(
            area="kilika_woods", battle_count=advances, extra_advances=1
        )
    logger.warning(f"==== Chosen Value: {rng_value}")


def besaid_trials():
    # Exit Tent
    while memory.main.get_map() != 17:
        t_coords = memory.main.get_coords()
        pathing.set_movement([-1, t_coords[1] - 15])

    # To the temple
    while not pathing.set_movement([35, 182]):
        pass
    while not pathing.set_movement([17, 22]):
        pass
    while not pathing.set_movement([14, -67]):
        pass
    while memory.main.get_map() != 42:
        t_coords = memory.main.get_coords()
        pathing.set_movement([-2, t_coords[1] - 15])

    # Start the trials
    while memory.main.get_map() != 122:
        t_coords = memory.main.get_coords()
        pathing.set_movement([-2, t_coords[1] + 15])


def boat_1():
    memory.main.wait_frames(30 * 3)
    # To the junction screen, then back.
    FFXC.set_value("axis_ly", -1)
    memory.main.wait_frames(30 * 1)
    FFXC.set_value("axis_ly", 0)
    memory.main.wait_frames(30 * 6)
    FFXC.set_value("axis_ly", -1)
    memory.main.wait_frames(30 * 1)
    FFXC.set_value("axis_ly", 0)


def kilika():
    xbox.menu_b()
    memory.main.wait_frames(30 * 2.5)
    xbox.menu_down()
    memory.main.wait_frames(30 * 0.1)
    xbox.menu_down()
    memory.main.wait_frames(30 * 0.1)
    xbox.menu_down()
    memory.main.wait_frames(30 * 0.1)
    xbox.menu_down()
    memory.main.wait_frames(30 * 0.1)
    xbox.menu_down()
    memory.main.wait_frames(30 * 0.1)
    xbox.menu_down()
    memory.main.wait_frames(30 * 0.1)
    xbox.menu_b()
    memory.main.wait_frames(30 * 0.1)
    xbox.menu_b()
    memory.main.wait_frames(30 * 4)
    memory.main.await_control()


def kilika_trials():
    FFXC.set_movement(0, -1)
    memory.main.wait_frames(30 * 2)
    FFXC.set_neutral()


def load_miihen_start_laugh():
    import pathing

    while not pathing.set_movement([-440, 0]):
        pass
    memory.main.click_to_event_temple(4)

    # Reverse T screen
    memory.main.await_control()
    while not pathing.set_movement([-39, 18]):
        pass
    while not pathing.set_movement([3, 31]):
        pass
    while not pathing.set_movement([64, 15]):
        pass
    while not pathing.set_movement([163, 0]):
        pass
    memory.main.click_to_event_temple(2)

    # Carnival vendor screen
    memory.main.await_control()
    while not pathing.set_movement([30, -86]):
        pass
    while not pathing.set_movement([60, -24]):
        pass
    while not pathing.set_movement([101, 72]):
        pass
    while not pathing.set_movement([129, 101]):
        pass
    memory.main.click_to_event_temple(1)
    memory.main.wait_frames(30 * 1)
    memory.main.click_to_control()
    FFXC.set_movement(-1, -1)
    memory.main.wait_frames(30 * 0.2)
    memory.main.await_event()
    FFXC.set_neutral()


def load_miihen_start():
    import pathing

    while not pathing.set_movement([-440, 0]):
        pass
    memory.main.click_to_event_temple(4)

    # Reverse T screen
    memory.main.await_control()
    while not pathing.set_movement([-39, 18]):
        pass
    while not pathing.set_movement([3, 31]):
        pass
    while not pathing.set_movement([64, 15]):
        pass
    while not pathing.set_movement([163, 0]):
        pass
    memory.main.click_to_event_temple(2)

    # Carnival vendor screen
    memory.main.await_control()
    while not pathing.set_movement([30, -86]):
        pass
    while not pathing.set_movement([60, -24]):
        pass
    while not pathing.set_movement([101, 72]):
        pass
    while not pathing.set_movement([129, 101]):
        pass
    memory.main.click_to_event_temple(1)

    # -----Use this if you've already done the laughing scene.
    memory.main.click_to_control()
    while not pathing.set_movement([2, 57]):
        pass
    while not pathing.set_movement([108, 59]):
        pass
    while not pathing.set_movement([108, 26]):
        pass
    while not pathing.set_movement([78, -3]):
        pass
    while not pathing.set_movement([-68, -7]):
        pass
    while not pathing.set_movement([-99, 24]):
        pass
    while not pathing.set_movement([-126, 117]):
        pass
    memory.main.click_to_event_temple(1)

    logger.info("Load complete. Now for Mi'ihen area.")


def load_mrr():
    memory.main.await_control()
    while not pathing.set_movement([-49, 166]):
        pass
    while not pathing.set_movement([-43, 285]):
        pass
    while not pathing.set_movement([-39, 354]):
        pass

    FFXC.set_movement(0, 1)
    memory.main.await_event()
    FFXC.set_neutral()
    memory.main.click_to_control()


def load_mrr_2():
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 0.3)
    FFXC.set_movement(1, 1)
    memory.main.wait_frames(30 * 1)
    xbox.skip_dialog(2)
    FFXC.set_neutral()
    xbox.menu_b()
    memory.main.wait_frames(30 * 2)
    memory.main.await_control()
    for i in range(20):
        logger.debug(f"Sleeping for {20-i} more seconds...")
        memory.main.wait_frames(30 * 1)


def after_gui():
    memory.main.await_control()
    FFXC.set_movement(-1, 0)
    memory.main.wait_frames(30 * 2.5)
    FFXC.set_neutral()

    target = [[463, -163], [498, 77], [615, -39], [935, 12], [1200, 200]]

    checkpoint = 0
    while memory.main.get_map() != 93:
        if memory.main.user_control():
            if pathing.set_movement(target[checkpoint]):
                checkpoint += 1
        else:
            FFXC.set_neutral()
    FFXC.set_neutral()


def djose_temple():
    load_offset(19)
    memory.main.wait_frames(30 * 6)
    FFXC.set_value("axis_ly", -1)
    FFXC.set_value("axis_lx", -1)
    memory.main.wait_frames(30 * 1.7)
    FFXC.set_value("axis_ly", 0)
    FFXC.set_value("axis_lx", 0)
    memory.main.wait_frames(30 * 0.5)


def moonflow_2():
    memory.main.wait_frames(30 * 2)
    FFXC.set_movement(-1, -1)
    memory.main.wait_frames(30 * 0.7)
    FFXC.set_neutral()
    memory.main.wait_frames(30 * 0.5)


def load_guado_skip():
    memory.main.click_to_control_3()
    FFXC.set_movement(1, -1)
    memory.main.await_event()
    FFXC.set_neutral()
    memory.main.await_control()
    FFXC.set_movement(-1, 0)
    memory.main.wait_frames(30 * 0.6)
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 1.5)
    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(30 * 0.9)
    FFXC.set_movement(-1, -1)
    memory.main.wait_frames(30 * 2.2)
    FFXC.set_movement(1, -1)
    memory.main.wait_frames(30 * 2)
    FFXC.set_movement(1, 1)
    memory.main.await_event()
    FFXC.set_neutral()
    memory.main.wait_frames(30 * 0.2)
    memory.main.await_control()
    FFXC.set_movement(0, -1)
    memory.main.wait_frames(30 * 1)
    FFXC.set_neutral()
    import area.guadosalam as guadosalam

    guadosalam.after_speech(checkpoint=26)


def load_mac_lake():
    memory.main.await_control()
    FFXC.set_movement(0, 1)
    memory.main.await_event()
    FFXC.set_neutral()
    memory.main.await_control()


def load_mac_temple():
    FFXC.set_movement(-1, 0)
    memory.main.wait_frames(30 * 3)
    FFXC.set_neutral()
    memory.main.await_control()
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 3)
    FFXC.set_neutral()


def load_mac_temple_2():
    memory.main.await_control()
    FFXC.set_movement(-1, -1)
    memory.main.wait_frames(30 * 1.5)
    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(30 * 1.5)
    FFXC.set_neutral()


def load_wendigo():
    import battle.boss
    import battle.main

    battle.boss.wendigo()
    logger.info("Wendigo fight over - end of loading game to Wendigo fight")


def load_rescue():
    memory.main.await_control()
    FFXC.set_movement(1, -1)
    memory.main.wait_frames(30 * 0.7)
    FFXC.set_movement(0, -1)
    while memory.main.user_control():
        pass
    FFXC.set_neutral()
    memory.main.wait_frames(30 * 1)
    memory.main.await_control()
    memory.main.update_formation(Tidus, Rikku, Kimahri)

    airship_pathing.air_ship_path(1)  # The run from cockpit to the deck


def load_bahamut():
    load_offset(1)
    memory.main.await_control()
    FFXC.set_value("axis_ly", 1)
    FFXC.set_value("axis_lx", 1)
    memory.main.wait_frames(30 * 0.2)
    FFXC.set_value("axis_lx", 0)
    memory.main.wait_frames(30 * 2)
    FFXC.set_value("axis_ly", 0)


def load_calm():
    FFXC.set_movement(1, 1)
    memory.main.wait_frames(30 * 1)
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 2)
    FFXC.set_neutral()
    memory.main.await_control()


def load_gagazet_gates():
    FFXC.set_movement(1, 1)
    memory.main.wait_frames(30 * 3)
    FFXC.set_movement(0, 1)
    memory.main.await_event()
    FFXC.set_neutral()


def zan_entrance():
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 2)
    FFXC.set_movement(1, 1)
    memory.main.wait_frames(30 * 2.5)
    FFXC.set_neutral()


def zan_trials():
    FFXC.set_movement(1, 1)
    memory.main.wait_frames(30 * 0.5)
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 2)
    FFXC.set_neutral()


def load_gagazet_dream():
    logger.debug("Positioning to next map")
    while memory.main.get_map() != 309:
        FFXC.set_movement(1, 1)
    FFXC.set_neutral()
    logger.debug("Positioning complete")
    memory.main.await_control()


def load_egg_hunt():
    memory.main.await_control()
    while not pathing.set_movement([-10, -507]):
        pass
    while not pathing.set_movement([-5, -360]):
        pass

    while memory.main.get_map() != 324:
        FFXC.set_movement(0, 1)
    FFXC.set_neutral()
