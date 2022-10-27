import memory.main
import menu
import menuGrid
import vars
import xbox

game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def grid_up():
    menuGrid.grid_up()


def grid_down():
    menuGrid.grid_down()


def grid_left():
    menuGrid.grid_left()


def grid_right():
    menuGrid.grid_right()


def await_move():
    print("Sphere Grid: Waiting for Move command to be highlighted")
    while memory.main.s_grid_active() == False:
        print("The Sphere Grid isn't even open! Awaiting manual recovery.")
        memory.main.wait_frames(30 * 1)
    complete = False
    while complete == False:
        menuVal = memory.main.s_grid_menu()
        if menuVal == 11 or menuVal == 255:
            xbox.menu_b()
        elif menuVal == 7:
            cursorLoc = memory.main.cursor_location()
            if cursorLoc[0] == 51 or cursorLoc[1] == 243:
                xbox.menu_up()
            xbox.menu_b()
            complete = True
            memory.main.wait_frames(30 * 0.25)
    print("Move command highlighted. Good to go.")


def await_use():
    print("Sphere Grid: Waiting for Use command to be highlighted")
    while memory.main.s_grid_active() == False:
        print("The Sphere Grid isn't even open! Awaiting manual recovery.")
        memory.main.wait_frames(30 * 1)
    complete = False
    while complete == False:
        menuVal = memory.main.s_grid_menu()
        print("Menu value: ", menuVal)
        if menuVal == 7:
            cursorLoc = memory.main.cursor_location()
            if cursorLoc[0] == 102 or cursorLoc[1] == 14:
                xbox.menu_down()
            xbox.menu_b()
            complete = True
            memory.main.wait_frames(30 * 0.25)
        else:
            xbox.menu_b()
    print("Use command highlighted. Good to go.")


def await_quit_sg():
    print("Sphere Grid: attempting to quit")
    while memory.main.s_grid_active():
        menuVal = memory.main.s_grid_menu()
        if menuVal == 255:
            xbox.menu_a()
        elif menuVal == 11:
            xbox.menu_b()
        else:
            xbox.menu_a()
    print("Back to the main menu")


def open_grid(character):
    try:
        FFXC.set_neutral()
    except:
        FFXC = xbox.controller_handle()
        FFXC.set_neutral()
    while not memory.main.s_grid_active():
        # print("Attempting to open Sphere Grid")
        if memory.main.user_control() and not memory.main.menu_open():
            #   print("Menu is not open at all")
            xbox.tap_y()
        elif memory.main.menu_number() == 5:  # Cursor on main menu
            #  print("Main menu cursor")
            while memory.main.get_menu_cursor_pos() != 0:
                memory.main.menu_direction(memory.main.get_menu_cursor_pos(), 0, 11)
            # print("Done with menu cursor")
            while memory.main.menu_number() == 5:
                xbox.tap_b()
        elif memory.main.menu_number() == 7:  # Cursor selecting party member
            print("Selecting party member")
            target_pos = memory.main.get_character_index_in_main_menu(character)
            while memory.main.get_char_cursor_pos() != target_pos:
                if (
                    memory.main.get_story_progress() == 2528
                ):  # After B&Y, party size is evaluated weird.
                    memory.main.menu_direction(
                        memory.main.get_char_cursor_pos(), target_pos, 7
                    )
                elif memory.main.party_size() < 3:
                    xbox.menu_down()
                else:
                    # memory.menuDirection(memory.getCharCursorPos(), target_pos, memory.partySize())
                    # Not working. Use this instead.
                    memory.main.menu_direction(
                        memory.main.get_char_cursor_pos(), target_pos, 7
                    )
            while memory.main.menu_number() == 7:
                xbox.menu_b()
            try:
                FFXC.set_neutral()
            except:
                FFXC = xbox.controller_handle()
                FFXC.set_neutral()
    try:
        FFXC.set_neutral()
    except:
        FFXC = xbox.controller_handle()
        FFXC.set_neutral()


# ------------------------------------------------------------
# Nemesis Control functions


def perform_next_grid(limit: int = 255):
    # Conditions to hard disregard further evaluations.
    print("###   Next Version: ", game_vars.nem_checkpoint_ap())
    print("### Current S.lvls: ", memory.main.get_tidus_slvl())
    print("### Needed  S.lvls: ", next_ap_needed(game_vars.nem_checkpoint_ap()))
    if limit != 255:
        print("###          Limit: ", limit)
    if game_vars.nem_checkpoint_ap() == 0:
        print("###Something wrong: ", game_vars.nem_checkpoint_ap())
        return False
    if game_vars.nem_checkpoint_ap() > limit:
        print("### Limit exceeded: ", limit)
        return False

    # If the above checks are passed, check Tidus level and do sphere grid.
    if memory.main.get_tidus_slvl() >= next_ap_needed(game_vars.nem_checkpoint_ap()):
        print("##### Attemping Nemesis Grid #", game_vars.nem_checkpoint_ap())
        if game_vars.nem_checkpoint_ap() == 1:
            nem_gridding_1()
        elif game_vars.nem_checkpoint_ap() == 2:
            nem_gridding_2()
        elif game_vars.nem_checkpoint_ap() == 3:
            nem_gridding_3()
        elif game_vars.nem_checkpoint_ap() == 4:
            nem_gridding_4()
        elif game_vars.nem_checkpoint_ap() == 5:
            nem_gridding_5()
        elif game_vars.nem_checkpoint_ap() == 6:
            nem_gridding_6()
        elif game_vars.nem_checkpoint_ap() == 7:
            nem_gridding_7()
        elif game_vars.nem_checkpoint_ap() == 8:
            nem_gridding_8()
        elif game_vars.nem_checkpoint_ap() == 9:
            nem_gridding_9()
        elif game_vars.nem_checkpoint_ap() == 10:
            nem_gridding_10()
        elif game_vars.nem_checkpoint_ap() == 11:
            nem_gridding_11()
        elif game_vars.nem_checkpoint_ap() == 12:
            nem_gridding_12()
        elif game_vars.nem_checkpoint_ap() == 13:
            nem_gridding_13()
        elif game_vars.nem_checkpoint_ap() == 14:
            nem_gridding_14()
        elif game_vars.nem_checkpoint_ap() == 15:
            nem_gridding_15()
        elif game_vars.nem_checkpoint_ap() == 16:
            nem_gridding_16()
        elif game_vars.nem_checkpoint_ap() == 17:
            nem_gridding_17()
        elif game_vars.nem_checkpoint_ap() == 18:
            nem_gridding_18()
        elif game_vars.nem_checkpoint_ap() == 19:
            nem_gridding_19()
        elif game_vars.nem_checkpoint_ap() == 20:
            nem_gridding_20()
        elif game_vars.nem_checkpoint_ap() == 21:
            nem_gridding_21()
        elif game_vars.nem_checkpoint_ap() == 22:
            nem_gridding_22()
        elif game_vars.nem_checkpoint_ap() == 23:
            nem_gridding_23()
        elif game_vars.nem_checkpoint_ap() == 24:
            nem_gridding_24()
        elif game_vars.nem_checkpoint_ap() == 25:
            nem_gridding_25()
        elif game_vars.nem_checkpoint_ap() == 26:
            nem_gridding_26()
        else:
            print("----------------------------")
            print("End of sphere grid, no further grid logic programmed.")
            print("----------------------------")
            game_vars.set_nem_checkpoint_ap(
                game_vars.nem_checkpoint_ap() - 1
            )  # Decrement
        game_vars.set_nem_checkpoint_ap(game_vars.nem_checkpoint_ap() + 1)  # Increment
    # else:
    # print("###Not enough Slvl:", memory.getTidusSlvl() - nextAPneeded(gameVars.nemCheckpointAP()))


def next_ap_needed(checkpoint):
    if checkpoint == 1:
        return 13
    if checkpoint == 2:
        return 2
    if checkpoint == 3:
        return 13
    if checkpoint == 4:
        return 11
    if checkpoint == 5:
        return 11
    if checkpoint == 6:
        return 9
    if checkpoint == 7:
        return 9
    if checkpoint == 8:
        return 21
    if checkpoint == 9:
        return 22
    if checkpoint == 10:
        return 18
    if checkpoint == 11:
        return 14
    if checkpoint == 12:
        return 18
    if checkpoint == 13:
        return 4
    if checkpoint == 14:
        return 17
    if checkpoint == 15:
        return 18
    if checkpoint == 16:
        return 10
    if checkpoint == 17:
        return 25
    if checkpoint == 18:
        return 26
    if checkpoint == 19:
        return 17
    if checkpoint == 20:
        return 19
    if checkpoint == 21:
        return 19
    if checkpoint == 22:
        return 24
    if checkpoint == 23:
        return 11
    if checkpoint == 24:
        return 22
    if checkpoint == 25:
        return 22
    if checkpoint == 26:
        return 42
    return 100  # If no further grids are possible, continue indefinitely.


# ------------------------------------------------------------
# Nemesis menus


def nem_gridding_1():
    if memory.main.get_power() < 4 or memory.main.get_speed() < 4:
        game_vars.set_nem_checkpoint_ap(value=0)
        return
    # Requires X levels
    menu.auto_sort_items()
    open_grid(character=0)
    menuGrid.move_first()
    grid_right()
    grid_right()
    grid_right()
    menuGrid.move_and_use()
    # menuGrid.selSphere('power','none') #HP sphere
    # menuGrid.useAndUseAgain()
    menuGrid.sel_sphere("lv3", "none")
    menuGrid.use_and_move()
    grid_right()
    grid_right()
    grid_right()
    # menuGrid.moveAndUse()
    # menuGrid.selSphere('power','none')
    # menuGrid.useAndMove()
    grid_right()
    # menuGrid.moveAndUse()
    # menuGrid.selSphere('power','none')
    # menuGrid.useAndMove()
    grid_right()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_2():
    # Requires 2 levels
    open_grid(character=0)
    menuGrid.move_first()
    grid_right()
    grid_up()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_3():
    # Starts between the two accuracy nodes, top right of the grid.
    # Requires 13 levels to perform.
    open_grid(0)
    menuGrid.move_first()
    grid_right()
    grid_right()
    grid_right()
    grid_down()
    grid_down()
    menuGrid.move_and_use()
    # menuGrid.selSphere('power','none')
    # menuGrid.useAndUseAgain()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_left()
    grid_left()
    grid_down()
    grid_left()
    menuGrid.move_and_use()
    # menuGrid.selSphere('hp','none')
    # menuGrid.useAndUseAgain()
    # menuGrid.selSphere('power','none')
    # menuGrid.useAndUseAgain()
    # menuGrid.selSphere('power','none')
    # menuGrid.useAndUseAgain()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_4():
    # Starts on created HP node, just north of Auron.
    # Requires 11 levels to perform.
    open_grid(0)
    menuGrid.move_first()
    grid_left()
    grid_left()
    menuGrid.move_and_use()
    # menuGrid.selSphere('power','none')
    # menuGrid.useAndUseAgain()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_left()
    grid_down()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "right")
    # menuGrid.useAndUseAgain()
    # menuGrid.selSphere('power','none')
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_5():
    # Starts west of Auron.
    # Requires 11 levels to perform.
    open_grid(0)
    menuGrid.move_first()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "left")
    # menuGrid.useAndUseAgain()
    # menuGrid.selSphere('power','none')
    menuGrid.use_and_move()
    grid_up()
    grid_right()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "down")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_6():
    # Starts east of Auron, on an HP node in the right corner.
    # Requires 9 levels to perform.
    open_grid(0)
    menuGrid.move_first()
    grid_left()
    grid_left()
    grid_down()
    grid_down()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("mana", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_left()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "left")
    # menuGrid.useAndUseAgain()
    # menuGrid.selSphere('power','none')
    menuGrid.use_and_move()
    grid_down()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "right")
    # menuGrid.useAndUseAgain()
    # menuGrid.selSphere('power','none')
    if game_vars.end_game_version() in [1, 2]:
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("lv1", "none")
    # menuGrid.useAndUseAgain()
    # menuGrid.selSphere('hp','none')
    # menuGrid.useAndUseAgain()
    # menuGrid.selSphere('power','none')
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_7():
    # Starts in the center of the circle, near end of any% grid.
    # Requires 9 levels to perform.
    open_grid(0)
    menuGrid.move_first()
    grid_right()
    grid_down()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("mana", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    # menuGrid.useAndUseAgain()
    # menuGrid.selSphere('power','none')
    menuGrid.use_and_move()
    grid_right()
    grid_down()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    # menuGrid.useAndUseAgain()
    # menuGrid.selSphere('power','none')
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_8():
    open_grid(0)
    menuGrid.move_first()
    grid_right()
    grid_right()
    grid_down()
    grid_right()
    grid_right()
    grid_right()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_up()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_up()
    grid_up()
    grid_left()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("lv1", "none")
    menuGrid.use_and_move()
    grid_right()
    grid_up()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_9():  # Ends near Wakka
    open_grid(0)
    menuGrid.move_first()
    grid_down()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    grid_down()
    grid_down()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_right()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_right()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_10():  # Starts near Wakka
    open_grid(0)
    menuGrid.move_first()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("lv2", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_down()
    grid_right()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("lv2", "none")
    menuGrid.use_and_move()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_right()
    grid_down()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_left()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("lv4", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("lv4", "none")
    menuGrid.use_and_move()
    FFXC.set_movement(1, -1)
    memory.main.wait_frames(30)
    FFXC.set_movement(0, 0)
    FFXC.set_neutral()
    memory.main.wait_frames(6)
    menuGrid.move_and_use()
    menuGrid.sel_sphere("lv4", "none")
    menuGrid.use_and_move()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_11():  # Back from Ultima to Wakka's grid
    open_grid(0)
    menuGrid.move_first()
    grid_left()
    grid_up()
    grid_up()
    grid_up()
    grid_left()
    grid_up()
    grid_up()
    grid_left()
    grid_up()
    grid_up()
    grid_up()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_left()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("lv1", "none")
    menuGrid.use_and_move()
    grid_up()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_12():  # Through Kimahri's grid to Rikku's.
    open_grid(0)
    menuGrid.move_first()
    grid_left()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_left()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    grid_up()
    grid_up()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("ability", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("ability", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_13():  # Start on the Steal command
    open_grid(0)
    menuGrid.move_first()
    grid_right()
    grid_down()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "right")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_14():
    open_grid(0)
    menuGrid.move_first()
    grid_left()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_down()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("mana", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_down()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("mana", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_15():  # Weird off-shoot with the three +1 strength nodes
    open_grid(0)
    menuGrid.move_first()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_right()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "right")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "right")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "left")
    menuGrid.use_and_move()
    grid_down()
    grid_down()
    grid_down()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_right()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_16():
    open_grid(0)
    menuGrid.move_first()
    grid_up()
    grid_up()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_down()
    grid_down()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_17():  # Ends near Lulu
    open_grid(0)
    menuGrid.move_first()
    grid_down()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_down()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("mana", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_right()
    grid_down()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_18():  # All the way back to Kimahri grid
    open_grid(0)
    menuGrid.move_first()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_left()
    grid_left()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_19():
    open_grid(0)
    menuGrid.move_first()
    grid_up()
    grid_up()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "left")
    menuGrid.use_and_move()
    grid_right()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_left()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("lv1", "none")
    menuGrid.use_and_move()
    grid_up()
    grid_up()
    grid_up()
    grid_left()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_right()
    grid_right()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_20():  # Starts next to Haste node
    open_grid(0)
    menuGrid.move_first()
    grid_right()
    grid_right()
    grid_right()
    grid_down()
    menuGrid.move_and_use()  # Into Auron's grid
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_down()
    grid_right()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_21():  # Auron's grid back to Tidus
    open_grid(0)
    menuGrid.move_first()
    grid_left()
    grid_up()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    grid_up()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_left()
    grid_left()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_22():
    open_grid(0)
    menuGrid.move_first()
    grid_left()
    grid_down()
    grid_down()
    grid_down()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_up()
    grid_up()
    grid_up()
    grid_left()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("lv3", "none")
    menuGrid.use_and_move()
    grid_up()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_23():
    open_grid(0)
    menuGrid.move_first()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_right()
    grid_down()
    grid_down()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_24():
    open_grid(0)
    menuGrid.move_first()
    grid_left()
    grid_down()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_up()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_down()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_left()
    grid_left()
    grid_up()
    grid_left()
    grid_left()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_right()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def nem_gridding_25():  # End Tidus grid, Quick Hit
    open_grid(0)
    menuGrid.move_first()
    grid_up()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_right()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("lv3", "none")
    menuGrid.use_and_move()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_down()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_left()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("ability", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("lv3", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


# Backtrack to Auto-life, or can go through Yuna's grid on refactor.
def nem_gridding_26():
    open_grid(0)
    menuGrid.move_first()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    grid_up()
    grid_right()
    grid_up()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("lv4", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_right()
    grid_up()
    grid_up()
    grid_right()
    grid_right()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("lv4", "none")
    menuGrid.use_and_move()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("ability", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def lulu_bribe():
    open_grid(5)
    menuGrid.move_first()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("ability", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def rikku_haste():
    open_grid(character=6)

    menuGrid.move_first()
    if game_vars.end_game_version() == 3:
        grid_up()
        grid_up()
        grid_right()
        grid_up()
        grid_up()
        grid_up()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    grid_right()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    grid_left()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("ability", "aftersk")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def rikku_provoke():
    open_grid(6)
    menuGrid.move_first()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("ability", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()


def str_boost():
    open_grid(0)
    menuGrid.move_first()
    grid_right()
    grid_right()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("strength", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("strength", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("strength", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_left()
    grid_down()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("strength", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("strength", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("strength", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_quit()
    memory.main.close_menu()

# ------------------------------
# Nemesis menus

def arena_purchase_1():
    memory.main.wait_frames(60)
    xbox.tap_b()
    memory.main.wait_frames(15)
    xbox.tap_b()  # Tidus catcher
    memory.main.wait_frames(15)
    xbox.tap_up()
    xbox.tap_b()  # Confirm
    memory.main.wait_frames(15)
    xbox.tap_b()  # Do not equip
    memory.main.wait_frames(15)
    xbox.tap_down()
    xbox.tap_b()  # Yuna catcher
    memory.main.wait_frames(15)
    xbox.tap_up()
    xbox.tap_b()  # Confirm
    memory.main.wait_frames(15)
    xbox.tap_up()
    xbox.tap_b()  # Do equip
    memory.main.wait_frames(15)
    xbox.tap_a()
    memory.main.wait_frames(15)
    xbox.tap_a()
    memory.main.wait_frames(15)
    xbox.tap_up()
    xbox.tap_a()
    memory.main.wait_frames(15)
    xbox.tap_b()
    memory.main.wait_frames(60)


def remove_all_nea():
    for i in range(7):
        if memory.main.equipped_armor_has_ability(charNum=i):  # Defaults to NEA
            if i == 0:
                if memory.main.check_ability_armor(ability=0x8056)[i]:
                    equip_armor(character=i, ability=0x8056)  # Auto-Haste
                else:
                    equip_armor(character=i, ability=99)  # Remove equipment
            elif i in [4, 6]:
                if memory.main.check_ability_armor(ability=0x801D)[i]:
                    equip_armor(character=i, ability=0x801D)  # Auto-Phoenix
                elif memory.main.check_ability_armor(ability=0x8072, slot_count=4)[i]:
                    equip_armor(character=i, ability=0x8072, slot_count=4)
                else:
                    equip_armor(character=i, ability=99)  # Remove equipment
            else:
                equip_armor(character=i, ability=99)  # Unequip
