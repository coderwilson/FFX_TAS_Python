import memory
import xbox

FFXC = xbox.controller_handle()
import json
import math

import pathing
import vars

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
        if actor_mem != 52685:
            print(actor_mem, " | ", x)
        if actor_mem in [20481, 20482, 20651]:
            save_actors.append(x)
    print(save_actors)
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
    memory.main.clear_save_menu_cursor()
    memory.main.clear_save_menu_cursor_2()
    target_actor = nearest_save_actor()
    target_coords = memory.main.get_actor_coords(target_actor)
    target_details = get_save_sphere_settings(target_actor)
    print("Approaching actor: ", target_actor)
    while not (
        memory.main.diag_progress_flag() == target_details[2]
        and memory.main.diag_skip_possible()
    ):
        if memory.main.user_control():
            pathing.set_movement([target_coords[0], target_coords[1]])
            xbox.tap_b()
        else:
            FFXC.set_neutral()
            if memory.main.get_map() == 347:
                print("Blitzball menu opened")
                memory.main.wait_frames(30)
                while memory.main.save_popup_cursor() != 5:
                    xbox.tap_a()
                xbox.tap_b()
                memory.main.wait_frames(90)
            elif memory.main.save_menu_open():
                print("Mark 1 - ", memory.main.diag_progress_flag())
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
                # while memory.main.user_control():
                #     pathing.set_movement([target_coords[0], target_coords[1]])
                #     xbox.tap_b()
                #     memory.main.wait_frames(6)
                # memory.main.wait_frames(20)
                target_details = get_save_sphere_settings(target_actor)
            else:
                FFXC.set_neutral()
                if memory.main.battle_active():
                    print("Mark 2", memory.main.diag_progress_flag())
                    battle.main.flee_all()
                    memory.main.click_to_control()
                elif memory.main.diag_skip_possible():
                    print("Mark 3", memory.main.diag_progress_flag())
                    xbox.tap_b()
    FFXC.set_neutral()


def disengage_save_sphere():
    while memory.main.save_menu_cursor() == 0 and memory.main.save_menu_cursor_2() == 0:
        print("Cursor")
        xbox.tap_a()
    while not memory.main.user_control():
        xbox.tap_b()


def touch_and_go():
    approach_save_sphere()
    print("Now touching save sphere.")
    disengage_save_sphere()


def touch_and_save(save_num: int = 999):
    if save_num >= 200:
        print("Cannot save number ", save_num, ", out of bounds error")
        save_num = 999
    save_pos = 999
    if save_num != 999:
        import loadGame

        saveFiles = loadGame.get_saved_files()
        testString = "ffx_" + str(save_num).zfill(3)
        for x in range(len(saveFiles)):
            if saveFiles[x] == testString:
                save_pos = x

    approach_save_sphere()
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
    memory.main.wait_frames(2)
    xbox.tap_b()
    while not memory.main.user_control():
        xbox.tap_a()

    if save_num != 999 and save_pos == 999:
        saveFiles = loadGame.get_saved_files()
        print(
            "File was expected as save number ",
            save_num,
            ", but could not find this file.",
        )
        print("Actual save file: ", saveFiles[0])
        file_orig = game_vars.game_save_path() + saveFiles[0]
        print(file_orig)
        file_dest = game_vars.game_save_path() + "ffx_" + str(save_num).zfill(3)
        print(file_dest)
        import shutil

        shutil.move(src=file_orig, dst=file_dest)


def get_save_sphere_settings(actor_index: int):
    filepath = "json_ai_files\\save_sphere_details.json"
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

    return ret_array


def record_save_sphere(x_val: int, y_val: int, diag_prog: int, actor: int):
    filepath = "json_ai_files\\save_sphere_details.json"
    with open(filepath, "r") as fp:
        records = json.load(fp)
    map_num = str(memory.main.get_map())
    diag_num = str(memory.main.get_story_progress())
    actor_num = str(actor)
    print("========================")
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
