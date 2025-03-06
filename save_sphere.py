import datetime
import json
import logging
import math
import os
import shutil

from jsonmerge import merge

import battle.main
import load_game
import memory
import pathing
import vars
import xbox

FFXC = xbox.controller_handle()

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()


def distance(save_index) -> int:
    tidus_coords = memory.main.get_coords()
    target_coords = memory.main.get_actor_coords(save_index)

    return int(
        math.sqrt(
            (target_coords[1] - tidus_coords[1]) ** 2
            + (target_coords[0] - tidus_coords[0]) ** 2
        )
    )


def nearest_save_actor() -> int:
    save_actors = []
    FFXC.set_neutral()
    for x in range(memory.main.get_actor_array_size()):
        actor_mem = memory.main.get_actor_id(x)
        # if actor_mem != 52685:
        # logger.debug(f"nearest_save_actor: {actor_mem} | {x}")
        if actor_mem in [20481, 20482, 20651]:
            save_actors.append(x)
    logger.debug(save_actors)
    if len(save_actors) == 0:
        return 999
    elif len(save_actors) == 1:
        return save_actors[0]
    else:
        best_actor = 255
        best_dist = 255
        for j in range(len(save_actors)):
            if best_actor == 255:
                best_actor = save_actors[j]
                best_dist = distance(save_actors[j])
            elif distance(save_actors[j]) < best_dist:
                best_actor = save_actors[j]
                best_dist = distance(save_actors[j])
        return best_actor


def approach_save_sphere():
    if not memory.main.user_control():
        while not memory.main.user_control():
            if memory.main.diag_skip_possible():
                xbox.tap_b()
            elif memory.main.menu_open():
                xbox.tap_b()
    memory.main.clear_save_menu_cursor()
    memory.main.clear_save_menu_cursor_2()
    target_actor = nearest_save_actor()
    target_coords = memory.main.get_actor_coords(target_actor)
    target_details = get_save_sphere_settings(target_actor)
    logger.debug(f"Approaching actor: {target_actor}")

    # Time-out logic
    start_timer = datetime.datetime.now()
    if target_actor == 999:
        logger.debug("Disregard, save sphere could not be found.")
        return False
    else:
        logger.debug("80 second time-out logic.")
        logger.debug("The run is NOT SOFT LOCKED")
        while not (
            memory.main.diag_progress_flag() == target_details[2]
            and memory.main.diag_skip_possible()
        ):
            # Time-out logic
            end_timer = datetime.datetime.now()
            total_time = end_timer - start_timer
            if total_time.total_seconds() > 80:
                logger.debug("Save sphere time out - could not reach save sphere.")
                return False

            # Touch sphere logic
            if memory.main.user_control():
                pathing.set_movement([target_coords[0], target_coords[1]])
                if distance(save_index=target_actor) < 20:
                    xbox.tap_b()
                    #memory.main.wait_frames(3)  # To avoid overzealous touching.
                    if memory.main.user_control():
                        memory.main.wait_frames(1)
            else:
                FFXC.set_neutral()
                if memory.main.get_map() == 347:
                    logger.debug("Blitzball menu opened")
                    memory.main.wait_frames(30)
                    while memory.main.save_popup_cursor() != 5:
                        xbox.tap_a()
                    xbox.tap_b()
                    memory.main.wait_frames(90)
                elif memory.main.save_menu_open():
                    logger.debug(f"Mark 1 - {memory.main.diag_progress_flag()}")
                    record_save_sphere(
                        x_val=target_coords[0],
                        y_val=target_coords[1],
                        diag_prog=memory.main.diag_progress_flag(),
                        actor=target_actor,
                    )
                    while not memory.main.user_control():
                        xbox.tap_a()
                    memory.main.wait_frames(2)
                    memory.main.clear_save_menu_cursor()
                    memory.main.clear_save_menu_cursor_2()
                    target_details = get_save_sphere_settings(target_actor)
                else:
                    FFXC.set_neutral()
                    if memory.main.battle_active():
                        logger.debug(f"Mark 2 {memory.main.diag_progress_flag()}")
                        battle.main.flee_all()
                        memory.main.click_to_control()
                        target_actor = nearest_save_actor()
                        target_coords = memory.main.get_actor_coords(target_actor)
                        target_details = get_save_sphere_settings(target_actor)
                        logger.debug(f"Updating actor: {target_actor}")
                    elif memory.main.diag_skip_possible():
                        logger.debug(f"Mark 3 {memory.main.diag_progress_flag()}")
                        if not (
                            memory.main.diag_progress_flag() == target_details[2]
                            and memory.main.diag_skip_possible()
                        ):
                            xbox.tap_b()  # Causes over-zealous touching.
    FFXC.set_neutral()
    return True


def disengage_save_sphere():
    while memory.main.save_menu_cursor() == 0 and memory.main.save_menu_cursor_2() == 0:
        logger.debug("Cursor")
        xbox.tap_a()
        if memory.main.user_control():
            return
    while not memory.main.user_control():
        xbox.tap_b()


def touch_and_go():
    if approach_save_sphere():
        logger.debug("Now touching save sphere.")
        disengage_save_sphere()


def touch_and_save(save_num: int = 999, game_state: str = "tbd", step_count: int = 999):
    if game_vars.nemesis() and save_num != 199:
        save_num += 100
        game_mode = "Nemesis"
    elif game_vars.story_mode() and save_num != 199:
        save_num += 50
        game_mode = "Story"
    else:
        game_mode = "Speed"
    if save_num >= 200:
        logger.debug(f"Cannot save number {save_num} out of bounds error")
        save_num = 999
    save_pos = 999
    if save_num != 999:
        save_files = load_game.get_saved_files()
        test_string = "ffx_000"
        for y in range(len(save_files)):
            if save_files[y] == test_string:
                save_pos = y
        auto_save = save_pos
        save_pos = 999
        test_string = "ffx_" + str(save_num).zfill(3)
        for x in range(len(save_files)):
            if save_files[x] == test_string:
                save_pos = x
        if auto_save > save_pos:
            save_pos += 1
    if approach_save_sphere():
        memory.main.wait_frames(2)
        while not memory.main.save_menu_open():
            xbox.tap_b()
        memory.main.wait_frames(9)
        if save_pos == 999:
            while memory.main.load_game_pos() != 0:
                xbox.tap_up()
        else:
            while memory.main.load_game_pos() != save_pos:
                if memory.main.load_game_pos() + 4 < save_pos:
                    xbox.trigger_r()
                elif memory.main.load_game_pos() < save_pos:
                    xbox.tap_down()
                else:
                    xbox.tap_up()
                memory.main.wait_frames(1)
        xbox.tap_b()
        logger.debug(f"===={save_num}====")
        memory.main.wait_frames(2)
        while memory.main.save_conf_cursor() != 1:
            xbox.tap_left()
        xbox.tap_b()
        xbox.tap_b()
        while not memory.main.user_control():
            xbox.tap_a()

        logger.debug(f"==== Save num {save_num}====")
        logger.debug(f"==== Save pos {save_pos}====")
        if save_num != 999 and save_pos == 999:
            save_files = load_game.get_saved_files()
            logger.debug(
                f"File was expected as save number {save_num} "
                + "but could not find this file."
            )
            logger.debug(f"Actual save file: {save_files[0]}")
            file_orig = game_vars.game_save_path() + save_files[0]
            logger.debug(file_orig)
            file_dest = game_vars.game_save_path() + "ffx_" + str(save_num).zfill(3)
            logger.debug(file_dest)

            shutil.move(src=file_orig, dst=file_dest)
        else:
            logger.debug(f"File number {save_num} was found.")

        # Finally, register save in json.
        if save_num not in [199, 999]:
            # 199 is used for Arena battles. Reserved.
            # 999 means any unused save. No special save for this.
            if game_state == "tbd" or step_count == 999:
                return

            logger.debug("Registering save")
            filepath = os.path.join("json_ai_files", "save_load_details.json")
            with open(filepath, "r") as fp:
                results = json.load(fp)

            # game_state already a string
            step_count_val = str(step_count)
            save_num_value = str(save_num)
            blitz_win_value = str(game_vars.get_blitz_win())
            end_game_version_val = str(game_vars.end_game_version())
            nea_zone = str(game_vars.get_nea_zone())
            nem_ap_val = str(game_vars.nem_checkpoint_ap())
            mrr_skip = game_vars.mrr_skip_val()

            new_val = {
                game_state: {
                    step_count_val: {
                        game_mode: {
                            "save_num": save_num_value,
                            "blitz_win_value": blitz_win_value,
                            "end_game_version_val": end_game_version_val,
                            "nea_zone": nea_zone,
                            "nem_ap_val": nem_ap_val,
                            "special_movement": "none",
                            "mrr_skip": mrr_skip,
                        }
                    }
                }
            }
            results = merge(results, new_val)
            with open(filepath, "w") as fp:
                json.dump(results, fp, indent=4)


def get_save_sphere_settings(actor_index: int):
    filepath = os.path.join("json_ai_files", "save_sphere_details.json")
    with open(filepath, "r") as fp:
        results = json.load(fp)

    map_num = str(memory.main.get_map())
    diag_num = str(memory.main.get_story_progress())
    actor_num = str(actor_index)
    ret_array = [999, 999, 999]
    if map_num in results:
        if diag_num in results[map_num]:
            if actor_num in results[map_num][diag_num]:
                ret_array = [
                    results[map_num][diag_num][actor_num]["x"],
                    results[map_num][diag_num][actor_num]["y"],
                    results[map_num][diag_num][actor_num]["diag"],
                ]
    logger.debug(ret_array)
    return ret_array


def record_save_sphere(x_val: int, y_val: int, diag_prog: int, actor: int):
    filepath = os.path.join("json_ai_files", "save_sphere_details.json")
    logger.debug(f"Recording save sphere to {filepath}")
    with open(filepath, "r") as fp:
        records = json.load(fp)
    map_num = str(memory.main.get_map())
    diag_num = str(memory.main.get_story_progress())
    actor_num = str(actor)
    new_val = {
        map_num: {diag_num: {actor_num: {"x": x_val, "y": y_val, "diag": diag_prog}}}
    }
    if map_num in records.keys():
        if diag_num in (records[map_num].keys()):
            if actor_num in records[map_num][diag_num]:
                if (
                    records[map_num][diag_num][actor_num]["diag"]
                    != new_val[map_num][diag_num][actor_num]["diag"]
                ):
                    records[map_num][diag_num][actor_num]["x"] = new_val[map_num][
                        diag_num
                    ][actor_num]["x"]
                    records[map_num][diag_num][actor_num]["y"] = new_val[map_num][
                        diag_num
                    ][actor_num]["y"]
                    records[map_num][diag_num][actor_num]["diag"] = new_val[map_num][
                        diag_num
                    ][actor_num]["diag"]
            else:
                records[map_num][diag_num].update(new_val[map_num][diag_num])
        else:
            records[map_num].update(new_val[map_num])
    else:
        records.update(new_val)

    with open(filepath, "w") as fp:
        json.dump(records, fp, indent=4)
