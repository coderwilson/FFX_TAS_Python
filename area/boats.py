import battle.boss
import battle.main
import logs
import memory.main
import menu
import targetPathing
import vars
import xbox

gameVars = vars.vars_handle()

FFXC = xbox.controller_handle()


def boat_dance():
    print("No dancing this time")
    memory.main.wait_frames(30 * 50)


def ss_liki():
    checkpoint = 0
    while memory.main.get_map() != 43:
        if memory.main.user_control():
            # events
            if checkpoint == 1:  # Group surrounding Yuna
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 3:  # Talk to Wakka
                memory.main.click_to_event_temple(3)
                print("Ready for SS Liki menu - (var) ", gameVars.early_tidus_grid())
                if not gameVars.early_tidus_grid():
                    menu.liki()
                    memory.main.close_menu()
                checkpoint += 1

            # General pathing
            elif targetPathing.set_movement(targetPathing.liki(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() or memory.main.menu_open():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                xbox.skip_scene()
            elif memory.main.battle_active():
                print("Ready to start fight with Sin's Fin")
                battle.boss.sin_fin()
                print("Sin's Fin fight complete. Waiting for next fight")
                battle.boss.echuilles()
                print("Sinspawn Echuilles fight complete")


def get_digit(number, n):
    return number // 10**n % 10


def _set_index_to_value(index, value, power):
    while memory.main.oaka_gil_cursor() != index:
        if memory.main.oaka_gil_cursor() < index:
            xbox.tap_right()
        else:
            xbox.tap_left()
    while get_digit(memory.main.oaka_gil_amount(), power) != value:
        if get_digit(memory.main.oaka_gil_amount(), power) < value:
            xbox.tap_up()
        else:
            xbox.tap_down()


def ss_winno():
    memory.main.click_to_control()
    # logs.writeStats("Winno Speed Count:")
    # logs.writeStats(memory.getSpeed())

    while memory.main.user_control():
        targetPathing.set_movement([28, -36])  # Through first door
    memory.main.wait_frames(2)
    FFXC.set_neutral()
    memory.main.click_to_control()
    memory.main.wait_frames(2)
    FFXC.set_movement(1, -1)
    memory.main.wait_frames(2)

    # Talk to O'akaXXIII
    oakaCoords = [
        memory.main.get_actor_coords(1)[0],
        memory.main.get_actor_coords(1)[1],
    ]
    while memory.main.user_control():
        targetPathing.set_movement(oakaCoords)
        xbox.tap_b()
        memory.main.wait_frames(3)
        oakaCoords = [
            memory.main.get_actor_coords(1)[0],
            memory.main.get_actor_coords(1)[1],
        ]
    FFXC.set_neutral()
    while memory.main.oaka_interface() != 12:
        xbox.tap_b()
    print("Setting Hundreds")
    _set_index_to_value(5, 0, 2)
    print("Setting Thousands")
    _set_index_to_value(4, 1, 3)
    print("Setting Zeroes")
    _set_index_to_value(7, 1, 0)
    while memory.main.oaka_interface() != 0:
        xbox.tap_b()
    while memory.main.shop_menu_dialogue_row() != 1:
        xbox.tap_down()
    xbox.tap_b()
    memory.main.click_to_control_3()


def ss_winno_2():
    # To the deck
    memory.main.await_control()
    checkpoint = 0

    while memory.main.get_story_progress() < 395:
        if memory.main.user_control():
            if checkpoint < 2 and memory.main.get_map() == 94:
                checkpoint = 2
            elif checkpoint == 6:
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint < 11 and memory.main.get_story_progress() == 385:
                checkpoint = 11
            elif checkpoint == 11:
                jecht_shot()
                checkpoint += 1
            elif targetPathing.set_movement(targetPathing.winno(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
    if not gameVars.csr():
        memory.main.click_to_diag_progress(142)
        xbox.clear_save_popup(0)


def jecht_shot_success():
    FFXC.set_value("Dpad", 1)  # Up
    xbox.tap_b()
    FFXC.set_neutral()
    FFXC.set_value("Dpad", 1)  # Up
    FFXC.set_value("Dpad", 8)  # Right
    xbox.tap_b()
    FFXC.set_neutral()
    FFXC.set_value("Dpad", 8)  # Right
    xbox.tap_b()
    FFXC.set_neutral()
    FFXC.set_value("Dpad", 8)  # Right
    FFXC.set_value("Dpad", 2)  # Down
    xbox.tap_b()
    FFXC.set_neutral()
    FFXC.set_value("Dpad", 2)  # Down
    xbox.tap_b()
    FFXC.set_neutral()
    FFXC.set_value("Dpad", 2)  # Down
    FFXC.set_value("Dpad", 4)  # Left
    xbox.tap_b()
    FFXC.set_neutral()
    FFXC.set_value("Dpad", 4)  # Left
    xbox.tap_b()
    FFXC.set_neutral()
    FFXC.set_value("Dpad", 4)  # Left
    FFXC.set_value("Dpad", 1)  # Up
    xbox.tap_b()
    FFXC.set_neutral()
    xbox.tap_b()


def jecht_shot():
    # Jecht shot tutorial
    print("Ready for Jecht Shot")
    memory.main.click_to_diag_progress(96)
    while memory.main.diag_progress_flag() != 100:
        if memory.main.diag_progress_flag() == 97:
            FFXC.set_value("Dpad", 1)  # Up
            FFXC.set_value("Dpad", 8)  # Right
            xbox.tap_b()
        elif memory.main.diag_progress_flag() == 98:
            FFXC.set_value("Dpad", 4)  # Left
            xbox.tap_b()
        elif memory.main.diag_progress_flag() == 99:
            FFXC.set_value("Dpad", 2)  # Down
            FFXC.set_value("Dpad", 8)  # Right
            xbox.tap_b()
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
        FFXC.set_neutral()

    # Failure logic
    xbox.skip_dialog(2)
    print("End Jecht Shot")
    print("We are intentionally failing the Jecht shot. Save the frames!")

    # Success logic
    # for i in range(15):
    #    jechtShotSuccess()
    # Does not work with CSR version 1.2.0
