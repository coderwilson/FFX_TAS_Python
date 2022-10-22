# Libraries and Core Files
import os
from pathlib import Path

import memory.main
import screen
import targetPathing
import vars
import xbox
import zzairShipPath

# This file is intended to load the game to a saved file.
# This assumes that the save is the first non-auto-save in the list of saves.

FFXC = xbox.controller_handle()
game_vars = vars.vars_handle()


def get_saved_files():
    saveFilesFull = sorted(
        Path(game_vars.game_save_path()).iterdir(), key=os.path.getmtime
    )
    saveFiles = [os.path.basename(i) for i in saveFilesFull]
    saveFiles = saveFiles[::-1]
    return saveFiles


def load_save_num(number):
    saveFiles = get_saved_files()
    testString = "ffx_" + str(number).zfill(3)
    print("Searching for string:", testString)
    savePos = 255
    for x in range(len(saveFiles)):
        if saveFiles[x] == testString:
            print("Save file is in position:", x)
            savePos = x
    memory.main.wait_frames(20)
    if savePos != 255:
        while memory.main.load_game_pos() != savePos:
            if memory.main.load_game_pos() + 4 < savePos:
                xbox.trigger_r()
            elif memory.main.load_game_pos() < savePos:
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
        print("That save file does not exist. Quitting program.")
        exit()


def load_first():
    print("Loading to first save file")
    xbox.menu_b()
    memory.main.wait_frames(30 * 2.5)
    xbox.menu_down()
    memory.main.wait_frames(30 * 0.1)
    xbox.menu_b()
    memory.main.wait_frames(30 * 0.1)
    xbox.menu_b()
    memory.main.await_control()


def load_offset(offset):
    print("Loading to save file in position", offset)
    totalOffset = offset
    memory.main.wait_frames(30 * 2.5)
    for _ in range(totalOffset):
        xbox.tap_down()
    for _ in range(7):
        xbox.tap_b()
    FFXC.set_neutral()
    memory.main.wait_frames(120)
    # So that we don't evaluate battle as complete after loading.
    memory.main.reset_battle_end()


def load_offset_battle(offset):
    print("Loading to save file in position", offset)
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
        cursorTarget = 5
    else:
        cursorTarget = 8
    print("Aiming at", cursorTarget)
    while memory.main.get_menu_cursor_pos() != cursorTarget:
        print(memory.main.get_menu_cursor_pos())
        xbox.tap_up()
        print(memory.main.get_menu_cursor_pos())
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
    print("Loading to first save file")
    load_offset(1)

    while not screen.Minimap1():
        if screen.Minimap4():
            FFXC.set_value("AxisLx", -1)
            FFXC.set_value("AxisLy", -1)
            memory.main.wait_frames(30 * 0.5)
            FFXC.set_value("AxisLx", 0)
            memory.main.wait_frames(30 * 1)
            FFXC.set_value("AxisLy", 0)
        else:
            xbox.menu_b()

    # Reverse T screen
    FFXC.set_value("AxisLx", 1)
    memory.main.wait_frames(30 * 4.5)
    FFXC.set_value("AxisLy", -1)
    memory.main.wait_frames(30 * 1)
    FFXC.set_value("AxisLy", 0)
    memory.main.wait_frames(30 * 5)
    FFXC.set_value("AxisLx", 0)

    # Carnival vendor screen
    memory.main.await_control()
    FFXC.set_value("AxisLy", 1)
    memory.main.wait_frames(30 * 1.5)
    FFXC.set_value("AxisLx", 1)
    memory.main.wait_frames(30 * 3)
    FFXC.set_value("AxisLx", 0)
    memory.main.wait_frames(30 * 1)
    FFXC.set_value("AxisLx", 1)
    memory.main.wait_frames(30 * 3)
    FFXC.set_value("AxisLx", 0)
    FFXC.set_value("AxisLy", 0)

    print("Rejoining the party.")
    memory.main.click_to_control()  # Scene, rejoining the party
    print("Walking up to Yuna.")
    FFXC.set_value("AxisLy", -1)
    FFXC.set_value("AxisLx", -1)
    memory.main.wait_frames(30 * 3)
    FFXC.set_value("AxisLx", 0)
    FFXC.set_value("AxisLy", 0)  # Enters laughing scene, ends Luca section.
    print("End of loading section.")


def load_neutral():
    load_first()


def load_baaj():
    FFXC.set_movement(1, 0)
    memory.main.wait_frames(30 * 0.4)
    FFXC.set_neutral()
    memory.main.wait_frames(30 * 0.04)


def besaid_trials():
    # Exit Tent
    while memory.main.get_map() != 17:
        tCoords = memory.main.get_coords()
        targetPathing.set_movement([-1, tCoords[1] - 15])

    # To the temple
    while not targetPathing.set_movement([35, 182]):
        pass
    while not targetPathing.set_movement([17, 22]):
        pass
    while not targetPathing.set_movement([14, -67]):
        pass
    while memory.main.get_map() != 42:
        tCoords = memory.main.get_coords()
        targetPathing.set_movement([-2, tCoords[1] - 15])

    # Start the trials
    while memory.main.get_map() != 122:
        tCoords = memory.main.get_coords()
        targetPathing.set_movement([-2, tCoords[1] + 15])


def boat_1():
    memory.main.wait_frames(30 * 3)
    # To the junction screen, then back.
    FFXC.set_value("AxisLy", -1)
    memory.main.wait_frames(30 * 1)
    FFXC.set_value("AxisLy", 0)
    memory.main.wait_frames(30 * 6)
    FFXC.set_value("AxisLy", -1)
    memory.main.wait_frames(30 * 1)
    FFXC.set_value("AxisLy", 0)


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
    import targetPathing

    while not targetPathing.set_movement([-440, 0]):
        pass
    memory.main.click_to_event_temple(4)

    # Reverse T screen
    memory.main.await_control()
    while not targetPathing.set_movement([-39, 18]):
        pass
    while not targetPathing.set_movement([3, 31]):
        pass
    while not targetPathing.set_movement([64, 15]):
        pass
    while not targetPathing.set_movement([163, 0]):
        pass
    memory.main.click_to_event_temple(2)

    # Carnival vendor screen
    memory.main.await_control()
    while not targetPathing.set_movement([30, -86]):
        pass
    while not targetPathing.set_movement([60, -24]):
        pass
    while not targetPathing.set_movement([101, 72]):
        pass
    while not targetPathing.set_movement([129, 101]):
        pass
    memory.main.click_to_event_temple(1)
    memory.main.wait_frames(30 * 1)
    memory.main.click_to_control()
    FFXC.set_movement(-1, -1)
    memory.main.wait_frames(30 * 0.2)
    memory.main.await_event()
    FFXC.set_neutral()


def load_miihen_start():
    import targetPathing

    while not targetPathing.set_movement([-440, 0]):
        pass
    memory.main.click_to_event_temple(4)

    # Reverse T screen
    memory.main.await_control()
    while not targetPathing.set_movement([-39, 18]):
        pass
    while not targetPathing.set_movement([3, 31]):
        pass
    while not targetPathing.set_movement([64, 15]):
        pass
    while not targetPathing.set_movement([163, 0]):
        pass
    memory.main.click_to_event_temple(2)

    # Carnival vendor screen
    memory.main.await_control()
    while not targetPathing.set_movement([30, -86]):
        pass
    while not targetPathing.set_movement([60, -24]):
        pass
    while not targetPathing.set_movement([101, 72]):
        pass
    while not targetPathing.set_movement([129, 101]):
        pass
    memory.main.click_to_event_temple(1)

    # -----Use this if you've already done the laughing scene.
    memory.main.click_to_control()
    while not targetPathing.set_movement([2, 57]):
        pass
    while not targetPathing.set_movement([108, 59]):
        pass
    while not targetPathing.set_movement([108, 26]):
        pass
    while not targetPathing.set_movement([78, -3]):
        pass
    while not targetPathing.set_movement([-68, -7]):
        pass
    while not targetPathing.set_movement([-99, 24]):
        pass
    while not targetPathing.set_movement([-126, 117]):
        pass
    memory.main.click_to_event_temple(1)

    print("Load complete. Now for Mi'ihen area.")


def load_mrr():
    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(30 * 2)
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 1)
    FFXC.set_movement(1, 1)
    memory.main.wait_frames(30 * 2)
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 2)
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
        print(f"Sleeping for {20-i} more seconds...")
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
            if targetPathing.set_movement(target[checkpoint]):
                checkpoint += 1
        else:
            FFXC.set_neutral()
    FFXC.set_neutral()


def djose_temple():
    load_offset(19)
    memory.main.wait_frames(30 * 6)
    FFXC.set_value("AxisLy", -1)
    FFXC.set_value("AxisLx", -1)
    memory.main.wait_frames(30 * 1.7)
    FFXC.set_value("AxisLy", 0)
    FFXC.set_value("AxisLx", 0)
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
    print("Wendigo fight over - end of loading game to Wendigo fight")


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
    memory.main.full_party_format("evrae")

    zzairShipPath.air_ship_path(1)  # The run from cockpit to the deck


def load_bahamut():
    load_offset(1)
    memory.main.await_control()
    FFXC.set_value("AxisLy", 1)
    FFXC.set_value("AxisLx", 1)
    memory.main.wait_frames(30 * 0.2)
    FFXC.set_value("AxisLx", 0)
    memory.main.wait_frames(30 * 2)
    FFXC.set_value("AxisLy", 0)


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
    print("Positioning to next map")
    while memory.main.get_map() != 309:
        FFXC.set_movement(1, 1)
    FFXC.set_neutral()
    print("Positioning complete")
    memory.main.await_control()


def load_egg_hunt():
    memory.main.await_control()
    while not targetPathing.set_movement([-10, -507]):
        pass
    while not targetPathing.set_movement([-5, -360]):
        pass

    while memory.main.get_map() != 324:
        FFXC.set_movement(0, 1)
    FFXC.set_neutral()
