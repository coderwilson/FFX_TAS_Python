import battle.boss
import battle.main
import memory.main
import menu
import pathing
import screen
import vars
import xbox
import save_sphere

game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def approach(do_grid=True):
    print("------------------------------Affection array:")
    print(memory.main.affection_array())
    print("------------------------------")
    memory.main.click_to_control()
    print("Approaching Macalania Temple")

    checkpoint = 0
    while memory.main.get_map() != 106:
        if memory.main.user_control():
            # Map changes
            if checkpoint < 2 and memory.main.get_map() == 153:
                checkpoint = 2

            # General pathing
            elif pathing.set_movement(pathing.m_temple_approach(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
    FFXC.set_neutral()
    memory.main.await_control()
    if do_grid:
        menu.mac_temple()
    save_sphere.touch_and_go()


def arrival():
    print("Starting Macalania Temple section")

    # Movement:
    jyscalSkipStatus = False
    checkpoint = 0
    skipStatus = True
    touchSave = False
    while memory.main.get_map() != 80:
        if memory.main.user_control():
            # Main events
            if checkpoint == 1:
                checkpoint += 1
            elif checkpoint == 2 and not touchSave:
                touchSave = True
                save_sphere.touch_and_go()
            elif checkpoint == 2 and game_vars.csr():
                checkpoint = 11
            elif checkpoint == 4:  # Talking to Trommell
                memory.main.click_to_event_temple(6)
                if memory.main.get_coords()[0] < 23.5:
                    memory.main.wait_frames(30 * 0.07)
                    FFXC.set_movement(1, 0)
                    memory.main.wait_frames(2)
                    FFXC.set_neutral()
                    memory.main.wait_frames(4)
                checkpoint += 1
            elif checkpoint == 5:  # Skip (new)
                print("Lining up for skip.")
                FFXC.set_movement(0, -1)
                memory.main.wait_frames(30 * 0.2)
                FFXC.set_neutral()
                while memory.main.get_coords()[1] < -101.5:
                    FFXC.set_value("Dpad", 8)
                    memory.main.wait_frames(2)
                    FFXC.set_value("Dpad", 0)
                    memory.main.wait_frames(5)

                print("Turning back")
                memory.main.wait_frames(3)
                FFXC.set_movement(-1, 0)
                memory.main.wait_frames(2)
                FFXC.set_neutral()
                memory.main.wait_frames(15)

                print("Now lined up. Here we go.")
                FFXC.set_movement(1, 0)
                memory.main.wait_frames(3)
                FFXC.set_value("BtnB", 1)
                memory.main.wait_frames(4)
                FFXC.set_value("BtnB", 0)
                memory.main.wait_frames(45)
                FFXC.set_neutral()
                checkpoint += 1
                memory.main.click_to_control_3()
            elif checkpoint == 6:
                checkpoint = 11
            elif checkpoint == 11:
                print("Check if skip is online")
                if game_vars.csr():
                    jyscalSkipStatus = True
                    checkpoint += 1
                elif memory.main.get_story_progress() < 1505:
                    jyscalSkipStatus = True
                    checkpoint += 1
                else:
                    jyscalSkipStatus = False
                    checkpoint = 20
                    skipStatus = False
                print("Jyscal Skip results:", skipStatus)
            elif checkpoint == 14 and game_vars.csr():
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 14:  # Pause so we don't mess up the skip
                if skipStatus:
                    FFXC.set_neutral()
                    xbox.skip_dialog(5)
                    FFXC.set_movement(0, -1)
                    memory.main.await_event()
                    FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint < 16 and memory.main.get_map() == 239:
                checkpoint = 16

            # Recovery items
            elif checkpoint == 23:  # Door, Jyscal room
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 24:  # Back to the main room
                memory.main.click_to_event_temple(5)
                checkpoint += 1
            elif checkpoint == 27:
                checkpoint = 12

            # General pathing
            elif pathing.set_movement(pathing.temple_foyer(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
    return jyscalSkipStatus


def start_seymour_fight():
    memory.main.click_to_control()
    while not pathing.set_movement([9, -53]):
        pass  # Allows us to move to the Seymour fight.
    FFXC.set_movement(1, 0)
    memory.main.await_event()
    FFXC.set_neutral()


def seymour_fight():
    battle.main.seymour_guado()

    # Name for Shiva
    xbox.name_aeon("Shiva")

    memory.main.await_control()
    FFXC.set_movement(-1, -1)
    memory.main.wait_frames(30 * 0.4)
    FFXC.set_movement(-1, 0)
    memory.main.await_event()
    FFXC.set_neutral()


def trials():
    memory.main.await_control()

    checkpoint = 0
    while memory.main.get_map() != 153:
        if memory.main.user_control():
            # CSR start point
            if checkpoint < 3 and game_vars.csr():
                checkpoint = 3

            # Map changes
            elif checkpoint < 2 and memory.main.get_map() == 239:
                checkpoint = 2

            # Spheres and Pedestals
            elif checkpoint == 2:
                memory.main.await_control()
                print("Activate the trials")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 9:  # Push pedestal - 1
                FFXC.set_movement(1, 0)
                memory.main.await_event()
                FFXC.set_neutral()
                memory.main.wait_frames(30 * 1)
                checkpoint += 1
            elif checkpoint == 13:  # Grab first Mac Sphere
                memory.main.click_to_event_temple(1)
                checkpoint += 1
            elif checkpoint == 17:  # Place first Mac Sphere
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 20:  # Push pedestal - 2
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 23:  # Grab glyph sphere
                memory.main.click_to_event_temple(2)
                checkpoint += 1
                print("Checkpoint:", checkpoint)
            elif checkpoint == 29:  # Push pedestal - 3
                FFXC.set_movement(1, 0)
                memory.main.await_event()
                FFXC.set_neutral()
                memory.main.wait_frames(30 * 1)
                checkpoint += 1
            elif checkpoint == 32:  # Place Glyph sphere
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 39:  # Grab second Mac sphere
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 46:  # Place second Mac sphere
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 51:  # Grab third Mac sphere
                memory.main.click_to_event_temple(1)
                checkpoint += 1
            elif checkpoint == 53:  # Place third Mac sphere
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 58:  # End of trials
                memory.main.click_to_event_temple(0)
                memory.main.await_control()
                # Just to start the next set of dialog.
                memory.main.click_to_event_temple(4)

            # General pathing
            elif pathing.set_movement(pathing.m_temple_trials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()


def escape():
    memory.main.click_to_control()
    print("First, some menuing")
    menuDone = False
    if game_vars.nemesis():
        memory.main.full_party_format("yuna", full_menu_close=False)
    else:
        menu.after_seymour()
        menuDone = True
        memory.main.full_party_format("macalaniaescape", full_menu_close=False)
    menu.equip_sonic_steel(full_menu_close=True)

    print("Now to escape the Guado")
    forceBattle = False

    checkpoint = 0
    while memory.main.get_encounter_id() != 195:
        if memory.main.user_control():
            # Events
            if checkpoint == 2:
                save_sphere.touch_and_go()
                checkpoint += 1
                print("Touching save sphere. Update checkpoint:", checkpoint)
            elif checkpoint == 18 and forceBattle:
                FFXC.set_neutral()

            # Map changes
            elif checkpoint < 19 and memory.main.get_map() == 192:
                checkpoint = 19
                print("Map change. Update checkpoint:", checkpoint)

            # General pathing
            elif pathing.set_movement(pathing.m_temple_escape(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                screen.await_turn()
                if checkpoint < 19:
                    battle.main.flee_all()
                    forceBattle = False
                elif not menuDone:
                    battle.main.escape_with_xp()
                    menu.after_seymour()
                    menuDone = True
                    memory.main.full_party_format("macalaniaescape")
                elif memory.main.get_encounter_id() == 195:
                    break
                else:
                    battle.main.flee_all()
            elif memory.main.menu_open():
                xbox.tap_b()
            elif memory.main.diag_skip_possible():
                xbox.tap_b()

    print("Done pathing. Now for the Wendigo fight.")
    battle.boss.wendigo()
    print("Wendigo fight over")


def under_lake():
    memory.main.click_to_control()
    checkpoint = 0
    while memory.main.get_map() != 129:
        if memory.main.user_control():
            if checkpoint == 4:
                FFXC.set_movement(0, 1)
                memory.main.click_to_event()
                FFXC.set_neutral()
                memory.main.click_to_control()
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(2)
                memory.main.click_to_event()
                FFXC.set_neutral()
                memory.main.click_to_control()
                checkpoint += 1
            elif checkpoint == 11:
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 15:
                while memory.main.user_control():
                    pathing.set_movement([-4, -8])
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_control_3()
                checkpoint += 1

            # General pathing
            elif pathing.set_movement(pathing.under_mac_temple(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
    FFXC.set_neutral()
    memory.main.click_to_control()


def under_lake_old():
    memory.main.click_to_control()
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 1)
    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(30 * 0.8)
    FFXC.set_movement(1, 1)
    memory.main.wait_frames(30 * 1)
    FFXC.set_movement(0, 1)
    memory.main.click_to_event()
    FFXC.set_neutral()

    memory.main.click_to_control()
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 1.5)  # Approach Yuna
    FFXC.set_neutral()

    memory.main.click_to_control()
    while memory.main.get_coords()[1] > 110:
        FFXC.set_movement(-1, 1)
    while memory.main.get_coords()[1] > 85:
        FFXC.set_movement(1, 1)
    while memory.main.get_coords()[0] > -30:
        if memory.main.get_coords()[1] < 110:
            FFXC.set_movement(1, -1)
        else:
            FFXC.set_movement(1, 0)
    FFXC.set_movement(1, 0)
    memory.main.click_to_event()  # Chest with Lv.2 Key Sphere
    FFXC.set_neutral()
    xbox.skip_dialog(0.2)
    memory.main.click_to_control()
    FFXC.set_movement(-1, 0)
    memory.main.wait_frames(30 * 0.25)
    while memory.main.get_coords()[0] < -5:
        FFXC.set_movement(-1, 1)
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 1)  # To Auron
    xbox.skip_dialog(1.5)
    FFXC.set_movement(1, 0)
    xbox.skip_dialog(0.4)
    FFXC.set_movement(-1, 0)
    xbox.skip_dialog(0.4)
    FFXC.set_neutral()
    memory.main.click_to_control()

    while memory.main.get_map() != 129:
        FFXC.set_movement(0, -1)
        if memory.main.diag_skip_possible():
            xbox.tap_b()
        elif memory.main.cutscene_skip_possible():
            xbox.skip_scene()
    FFXC.set_neutral()
    memory.main.click_to_control()
