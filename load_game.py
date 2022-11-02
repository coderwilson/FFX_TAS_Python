# Libraries and Core Files
import os
from pathlib import Path

import area.dream_zan
import logs
import memory.main
import pathing
import screen
import vars
import xbox
import zz_airship_path
from gamestate import game

# This file is intended to load the game to a saved file.
# This assumes that the save is the first non-auto-save in the list of saves.

FFXC = xbox.controller_handle()
game_vars = vars.vars_handle()


def load_into_game(gamestate: str, step_counter: str):
    if not (gamestate == "Luca" and step_counter == 3):
        area.dream_zan.new_game(gamestate)
        game.start_time = logs.time_stamp()
        logs.write_stats("Start time:")
        logs.write_stats(str(game.start_time))
    import load_game

    # Need to update these to use loadGame.loadSaveNum(number) for all.

    if gamestate == "Baaj" and step_counter == 1:
        load_save_num(40)
    if gamestate == "Baaj" and step_counter == 4:
        load_save_num(100)
    # Save pop-up after falling off of Rikkus boat
    if gamestate == "Besaid" and step_counter == 1:
        load_save_num(111)
    # Save pop-up after falling off of Rikkus boat
    if gamestate == "Besaid" and step_counter == 2:
        load_save_num(6)
        besaid_trials()
    # Crusader's lodge after "Enough, Wakka!"
    if gamestate == "Besaid" and step_counter == 3:
        load_save_num(39)
        print("Load complete")
        while memory.main.user_control():
            if memory.main.get_coords()[0] > 0.5:
                FFXC.set_movement(1, 1)
            else:
                FFXC.set_movement(0, 1)
        print("Ready for regular path")
    # Besaid beach before boarding SS Liki ( nice alliteration :D )
    if gamestate == "Boat1":
        load_save_num(31)
        boat_1()
    if gamestate == "Kilika" and step_counter == 1:  # Just after entering the woods
        load_save_num(22)
    if gamestate == "Luca" and step_counter == 1:  # Approaching Luca via boat
        load_save_num(112)
    if gamestate == "Luca" and step_counter == 5:
        load_save_num(5)
    if gamestate == "Miihen" and step_counter == 1:  # After the talk with Auron
        load_save_num(16)  # With laughing scene
        load_miihen_start_laugh()
    if gamestate == "Miihen" and step_counter == 2:  # Agency
        load_save_num(28)
        returnArray = [False, 0, 0, False]
    if gamestate == "MRR" and step_counter == 1:  # Mi'ihen North after meeting Seymour
        load_save_num(38)
        memory.main.set_gil_value(4000)  # Fixes a low gil state for this save file.
        load_mrr()
    # Aftermath, after talking to Seymour and then Auron
    if gamestate == "Djose" and step_counter == 1:
        load_save_num(27)
        after_gui()
    if gamestate == "Moonflow" and step_counter == 2:  # North bank, before Rikku
        load_save_num(2)
        moonflow_2()
    if gamestate == "Guadosalam" and step_counter == 2:  # After the Farplane
        load_save_num(3)
        load_guado_skip()
    if gamestate == "Macalania" and step_counter == 1:  # 1 = south, 2 = north
        load_save_num(9)
    if gamestate == "Macalania" and step_counter == 2:  # 1 = south, 2 = north
        load_save_num(7)
    if gamestate == "Macalania" and step_counter == 4:  # Right before Jyscal skip
        load_save_num(190)
        load_mac_temple()
        import menu

        menu.equip_weapon(character=0, special="brotherhood")
        menu.mac_temple()
    # Outside temple, before escaping.
    if gamestate == "Macalania" and step_counter == 6:
        load_save_num(4)
    if gamestate == "Home" and step_counter == 1:
        load_save_num(60)
    if gamestate == "Home" and step_counter == 2:
        load_save_num(11)
    if gamestate == "rescueYuna" and step_counter == 1:  # Airship, first movement.
        # Blitz Win, save less speed/power spheres
        load_save_num(56)
    if gamestate == "rescueYuna" and step_counter == 2:  # Bevelle trials
        load_save_num(15)
    if gamestate == "rescueYuna" and step_counter == 4:  # Altana
        load_save_num(12)
        # memory.main.setEncounterRate(setVal=0)
        # memory.main.setGameSpeed(setVal=1)
    # Highbridge before Seymour Natus
    if gamestate == "rescueYuna" and step_counter == 5:
        load_save_num(42)  # Regular
        # loadGame.loadSaveNum(67) #Nemesis
    if gamestate == "Gagazet" and step_counter == 1:  # Just before Calm Lands
        load_save_num(43)
        load_calm()
        game_vars.set_blitz_win(True)
    if gamestate == "Gagazet" and step_counter == 2:  # NE armor save
        load_save_num(57)
    if gamestate == "Gagazet" and step_counter == 3:  # Gagazet gates, after B&Y
        load_save_num(138)  # Blitz Win
        # loadGame.loadSaveNum(53) # Blitz Loss
        game_vars.end_game_version_set(4)
        load_gagazet_gates()
    if gamestate == "Gagazet" and step_counter == 6:  # After the dream
        load_save_num(98)
        game_vars.end_game_version_set(4)
        load_gagazet_dream()
        game_vars.flux_overkill_success()
    if gamestate == "Gagazet" and step_counter == 10:  # Calm Lands, but Nemesis version
        load_save_num(43)
        load_calm()
    if gamestate == "Gagazet" and step_counter == 11:  # Calm Lands, but Nemesis version
        load_save_num(64)
        FFXC.set_movement(1, 0)
        memory.main.wait_frames(60)
        FFXC.set_movement(0, 1)
        memory.main.wait_frames(60)
        FFXC.set_neutral()
        import menu

        menu.prep_calm_lands()
    if gamestate == "Zanarkand" and step_counter == 1:  # Intro scene revisited
        load_save_num(99)
        game_vars.end_game_version_set(1)
        game_vars.flux_overkill_success()
        game_vars.end_game_version_set(4)
    if gamestate == "Zanarkand" and step_counter == 2:  # Just before the trials.
        load_offset(35)
        zan_trials()
        game_vars.end_game_version_set(4)
    if gamestate == "Zanarkand" and step_counter == 3:  # After trials, before boss
        load_save_num(45)
        game_vars.end_game_version_set(4)
    if gamestate == "Zanarkand" and step_counter == 4:  # After Sanctuary Keeper
        load_save_num(44)
        game_vars.end_game_version_set(4)
    if gamestate == "Zanarkand" and step_counter == 5:  # After Yunalesca
        load_save_num(13)
    # Save sphere on the Highbridge before talking to Shedinja
    if gamestate == "Sin" and step_counter == 2:
        # loadGame.loadSaveNum(49)
        # Nemesis logic, double friend sphere drops from B&Y
        load_save_num(70)
        while not memory.main.oaka_gil_cursor() in [8, 20]:
            if memory.main.user_control():
                import pathing

                pathing.set_movement([-251, 340])
            else:
                FFXC.set_neutral()
            xbox.menu_b()
        memory.main.check_nea_armor()
    if gamestate == "Sin" and step_counter == 3:  # Start of "Sea of Sorrows" section
        load_save_num(50)
    if gamestate == "Sin" and step_counter == 4:  # Before point of no return
        # This save has zombiestrike weapons for all except Kimahri
        # Please use for egg hunt and zombie weapon testing.
        load_save_num(51)
        game_vars.set_zombie(5)
        load_egg_hunt()

    # Nemesis run loads
    if gamestate == "Nem_Farm" and step_counter == 1:
        load_save_num(14)
    if gamestate == "Nem_Farm" and step_counter == 2:
        load_save_num(69)
    if gamestate == "Nem_Farm" and step_counter == 3:
        load_save_num(84)
        game_vars.set_nem_checkpoint_ap(3)  # See nemesis.menu
        # import nemesis.arenaPrep
        nemesis.arenaPrep.arena_return()
    if gamestate == "Nem_Farm" and step_counter == 5:
        load_save_num(71)
    if gamestate == "Nem_Farm" and step_counter == 6:
        load_save_num(72)
        game_vars.set_nem_checkpoint_ap(2)  # See nemesis.menu
    if gamestate == "Nem_Farm" and step_counter == 8:
        load_save_num(73)
    if gamestate == "Nem_Farm" and step_counter == 9:
        load_save_num(75)
        game_vars.set_nem_checkpoint_ap(3)  # See nemesis.menu
    if gamestate == "Nem_Farm" and step_counter == 13:
        load_save_num(17)
        game_vars.set_nem_checkpoint_ap(7)  # See nemesis.menu
    if gamestate == "Nem_Farm" and step_counter == 14:
        load_save_num(76)
        game_vars.set_nem_checkpoint_ap(10)  # See nemesis.menu
    if gamestate == "Nem_Farm" and step_counter == 16:
        load_save_num(113)
        game_vars.set_nem_checkpoint_ap(12)  # See nemesis.menu
    if gamestate == "Nem_Farm" and step_counter == 17:
        load_save_num(111)
        game_vars.set_nem_checkpoint_ap(14)  # See nemesis.menu
    if gamestate == "Nem_Farm" and step_counter == 18:
        load_save_num(114)
        game_vars.set_nem_checkpoint_ap(15)  # See nemesis.menu
    if gamestate == "Nem_Farm" and step_counter == 19:  # Gagazet
        load_save_num(115)
        game_vars.set_nem_checkpoint_ap(19)  # See nemesis.menu
    if gamestate == "Nem_Farm" and step_counter == 21:
        load_save_num(79)
        nemesis.arenaPrep.arena_return()
        game_vars.set_nem_checkpoint_ap(27)  # See nemesis.menu
    if gamestate == "Nem_Farm" and step_counter == 22:
        load_save_num(82)
        # import nemesis.menu
        # nemesis.menu.rikkuHaste()
        game_vars.set_nem_checkpoint_ap(24)  # See nemesis.menu
    if gamestate == "Nem_Farm" and step_counter == 23:
        load_save_num(80)
        game_vars.set_nem_checkpoint_ap(30)  # See nemesis.menu
    if gamestate == "Nem_Farm" and step_counter == 24:
        load_save_num(81)
        game_vars.set_nem_checkpoint_ap(30)
        game_vars.set_nem_checkpoint_ap(30)  # See nemesis.menu
    if gamestate == "Nem_Farm" and step_counter == 20:
        load_save_num(85)
        game_vars.set_nem_checkpoint_ap(30)
    if gamestate == "Nem_Farm":
        memory.main.check_nea_armor()
    memory.main.check_nea_armor()


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

    print("Rejoining the party.")
    memory.main.click_to_control()  # Scene, rejoining the party
    print("Walking up to Yuna.")
    FFXC.set_value("axis_ly", -1)
    FFXC.set_value("axis_lx", -1)
    memory.main.wait_frames(30 * 3)
    FFXC.set_value("axis_lx", 0)
    FFXC.set_value("axis_ly", 0)  # Enters laughing scene, ends Luca section.
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
        pathing.set_movement([-1, tCoords[1] - 15])

    # To the temple
    while not pathing.set_movement([35, 182]):
        pass
    while not pathing.set_movement([17, 22]):
        pass
    while not pathing.set_movement([14, -67]):
        pass
    while memory.main.get_map() != 42:
        tCoords = memory.main.get_coords()
        pathing.set_movement([-2, tCoords[1] - 15])

    # Start the trials
    while memory.main.get_map() != 122:
        tCoords = memory.main.get_coords()
        pathing.set_movement([-2, tCoords[1] + 15])


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

    zz_airship_path.air_ship_path(1)  # The run from cockpit to the deck


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
    print("Positioning to next map")
    while memory.main.get_map() != 309:
        FFXC.set_movement(1, 1)
    FFXC.set_neutral()
    print("Positioning complete")
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
