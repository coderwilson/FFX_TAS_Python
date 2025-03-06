import logging

import memory.main
import menu
import menu_grid
from menu_grid import grid_up, grid_down, grid_left, grid_right
import vars
import xbox

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def await_move():
    logger.debug("Sphere Grid: Waiting for Move command to be highlighted")
    while not memory.main.s_grid_active():
        logger.debug("The Sphere Grid isn't even open! Awaiting manual recovery.")
        memory.main.wait_frames(30 * 1)
    complete = False
    while not complete:
        menu_val = memory.main.s_grid_menu()
        if menu_val == 11 or menu_val == 255:
            xbox.menu_b()
        elif menu_val == 7:
            cursor_loc = memory.main.cursor_location()
            if cursor_loc[0] == 51 or cursor_loc[1] == 243:
                xbox.menu_up()
            xbox.menu_b()
            complete = True
            memory.main.wait_frames(30 * 0.25)
    logger.debug("Move command highlighted. Good to go.")


def await_use():
    logger.debug("Sphere Grid: Waiting for Use command to be highlighted")
    while not memory.main.s_grid_active():
        logger.debug("The Sphere Grid isn't even open! Awaiting manual recovery.")
        memory.main.wait_frames(30 * 1)
    complete = False
    while not complete:
        menu_val = memory.main.s_grid_menu()
        logger.debug(f"Menu value: {menu_val}")
        if menu_val == 7:
            cursor_loc = memory.main.cursor_location()
            if cursor_loc[0] == 102 or cursor_loc[1] == 14:
                xbox.menu_down()
            xbox.menu_b()
            complete = True
            memory.main.wait_frames(30 * 0.25)
        else:
            xbox.menu_b()
    logger.debug("Use command highlighted. Good to go.")


def await_quit_sg():
    logger.debug("Sphere Grid: attempting to quit")
    while memory.main.s_grid_active():
        menu_val = memory.main.s_grid_menu()
        if menu_val == 255:
            xbox.menu_a()
        elif menu_val == 11:
            xbox.menu_b()
        else:
            xbox.menu_a()
    logger.debug("Back to the main menu")


def open_grid(character):
    FFXC.set_neutral()
    while not memory.main.s_grid_active():
        if memory.main.user_control() and not memory.main.menu_open():
            xbox.tap_y()
        elif memory.main.menu_number() == 5:  # Cursor on main menu
            while memory.main.get_menu_cursor_pos() != 0:
                memory.main.menu_direction(memory.main.get_menu_cursor_pos(), 0, 11)
            while memory.main.menu_number() == 5:
                xbox.tap_b()
        elif memory.main.menu_number() == 7:  # Cursor selecting party member
            logger.debug("Selecting party member")
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
                    # Not working. Use this instead.
                    memory.main.menu_direction(
                        memory.main.get_char_cursor_pos(), target_pos, 7
                    )
            while memory.main.menu_number() == 7:
                xbox.menu_b()
            FFXC.set_neutral()
    FFXC.set_neutral()


# ------------------------------------------------------------
# Nemesis Control functions


def perform_next_grid(limit: int = 255):
    # Conditions to hard disregard further evaluations.
    logger.debug(f"Next Version: {game_vars.nem_checkpoint_ap()}")
    logger.debug(f"Current S.lvls: {memory.main.get_tidus_slvl()}")
    logger.debug(f"Needed  S.lvls: {next_ap_needed(game_vars.nem_checkpoint_ap())}")
    if limit != 255:
        logger.debug(f"Limit: {limit}")
    if game_vars.nem_checkpoint_ap() == 0:
        logger.debug(f"Something wrong: {game_vars.nem_checkpoint_ap()}")
        return False
    if game_vars.nem_checkpoint_ap() > limit:
        logger.debug(f"Limit exceeded: {limit}")
        return False

    # If the above checks are passed, check Tidus level and do sphere grid.
    if memory.main.get_tidus_slvl() >= next_ap_needed(game_vars.nem_checkpoint_ap()):
        performed = False
        logger.info(f"Attemping Nemesis Grid #{game_vars.nem_checkpoint_ap()}")
        if game_vars.nem_checkpoint_ap() == 1:
            if nem_gridding_1():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 2:
            if nem_gridding_2():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 3:
            if nem_gridding_3():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 4:
            if nem_gridding_4():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 5:
            if nem_gridding_5():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 6:
            if nem_gridding_6():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 7:
            if nem_gridding_7():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 8:
            if nem_gridding_8():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 9:
            if nem_gridding_9():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 10:
            if nem_gridding_10():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 11:
            if nem_gridding_11():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 12:
            if nem_gridding_12():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 13:
            if nem_gridding_13():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 14:
            if nem_gridding_14():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 15:
            if nem_gridding_15():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 16:
            if nem_gridding_16():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 17:
            if nem_gridding_17():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 18:
            if nem_gridding_18():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 19:
            if nem_gridding_19():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 20:
            if nem_gridding_20():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 21:
            if nem_gridding_21():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 22:
            if nem_gridding_22():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 23:
            if nem_gridding_23():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 24:
            if nem_gridding_24():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 25:
            if nem_gridding_25():
                performed = True
        elif game_vars.nem_checkpoint_ap() == 26:
            if nem_gridding_26():
                performed = True
        else:
            performed = False
            logger.info("End of sphere grid, no further grid logic programmed.")
            game_vars.set_nem_checkpoint_ap(
                game_vars.nem_checkpoint_ap() - 1
            )  # Decrement
        if performed:
            # Increment
            game_vars.set_nem_checkpoint_ap(game_vars.nem_checkpoint_ap() + 1)
        return performed


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
        return 60
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
    menu_grid.move_first()
    grid_right()
    grid_right()
    grid_right()
    menu_grid.move_and_use()
    # menu_grid.sel_sphere('power','none') #HP sphere
    # menu_grid.use_and_use_again()
    menu_grid.sel_sphere("lv3", "none")
    menu_grid.use_and_move()
    grid_up()
    grid_up()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_2():
    # Requires 2 levels
    open_grid(character=0)
    menu_grid.move_first()
    grid_right()
    grid_up()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_3():
    # Starts between the two accuracy nodes, top right of the grid.
    # Requires 13 levels to perform.
    open_grid(0)
    menu_grid.move_first()
    grid_right()
    grid_right()
    grid_right()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    grid_down()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_4():
    # Starts on created HP node, just north of Auron.
    # Requires 11 levels to perform.
    open_grid(0)
    menu_grid.move_first()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_down()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "right")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_5():
    # Starts west of Auron.
    # Requires 11 levels to perform.
    open_grid(0)
    menu_grid.move_first()
    grid_right()
    grid_up()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "left")
    menu_grid.use_and_move()
    grid_up()
    grid_right()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "down")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_6():
    # Starts east of Auron, on an HP node in the right corner.
    # Requires 9 levels to perform.
    open_grid(0)
    menu_grid.move_first()
    grid_left()
    grid_left()
    grid_down()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_move()
    grid_down()
    grid_left()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "left")
    menu_grid.use_and_move()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "right")
    if game_vars.end_game_version() == 3:
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("lv1", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_7():
    # Starts in the center of the circle, near end of any% grid.
    # Requires 9 levels to perform.
    open_grid(0)
    menu_grid.move_first()
    grid_right()
    grid_down()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_right()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_8():
    open_grid(0)
    menu_grid.move_first()
    grid_right()
    grid_right()
    grid_down()
    grid_right()
    grid_right()
    grid_right()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_up()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_up()
    grid_up()
    grid_left()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("lv1", "none")
    menu_grid.use_and_move()
    grid_right()
    grid_up()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_9():  # Ends near Wakka
    open_grid(0)
    menu_grid.move_first()
    grid_down()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    grid_down()
    grid_down()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_down()
    grid_right()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_down()
    grid_right()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_10():  # Starts near Wakka
    open_grid(0)
    menu_grid.move_first()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("lv2", "none")
    menu_grid.use_and_move()
    grid_down()
    grid_down()
    grid_right()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("lv2", "none")
    menu_grid.use_and_move()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_right()
    grid_down()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("lv4", "none")
    menu_grid.use_and_move()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("lv4", "none")
    menu_grid.use_and_move()
    FFXC.set_movement(1, -1)
    memory.main.wait_frames(10)
    FFXC.set_movement(0, 0)
    FFXC.set_neutral()
    memory.main.wait_frames(6)
    menu_grid.move_and_use()
    menu_grid.sel_sphere("lv4", "none")
    menu_grid.use_and_move()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_11():  # Back from Ultima to Wakka's grid
    open_grid(0)
    menu_grid.move_first()
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
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("lv1", "none")
    menu_grid.use_and_move()
    grid_up()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_12():  # Through Kimahri's grid to Rikku's.
    open_grid(0)
    menu_grid.move_first()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_down()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_move()
    grid_down()
    grid_left()
    grid_left()
    grid_left()
    grid_up()
    grid_up()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("ability", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("ability", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_13():  # Start on the Steal command
    open_grid(0)
    menu_grid.move_first()
    grid_up()
    grid_down()
    grid_down()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "right")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_14():
    open_grid(0)
    menu_grid.move_first()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_move()
    grid_down()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_down()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_quit()
    kimahri_dispel()
    memory.main.close_menu()
    return True


def nem_gridding_15():  # Weird off-shoot with the three +1 strength nodes
    open_grid(0)
    menu_grid.move_first()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_right()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "right")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "right")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "left")
    menu_grid.use_and_move()
    grid_down()
    grid_down()
    grid_down()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_right()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_16():
    open_grid(0)
    menu_grid.move_first()
    grid_up()
    grid_up()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    FFXC.set_movement(1, -1)
    memory.main.wait_frames(9)
    FFXC.set_movement(0, 0)
    FFXC.set_neutral()
    memory.main.wait_frames(6)
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_17():  # Ends near Lulu
    open_grid(0)
    menu_grid.move_first()
    grid_down()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_down()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_move()
    grid_down()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_right()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_18():  # All the way back to Kimahri grid
    open_grid(0)
    menu_grid.move_first()
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
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_19():
    open_grid(0)
    menu_grid.move_first()
    grid_up()
    grid_up()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "left")
    menu_grid.use_and_move()
    grid_right()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("lv1", "none")
    menu_grid.use_and_move()
    grid_up()
    grid_up()
    grid_up()
    grid_left()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_right()
    grid_right()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_20():  # Starts next to Haste node
    open_grid(0)
    menu_grid.move_first()
    grid_right()
    grid_right()
    grid_right()
    grid_down()
    menu_grid.move_and_use()  # Into Auron's grid
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_right()
    grid_right()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_21():  # Auron's grid back to Tidus
    open_grid(0)
    menu_grid.move_first()
    grid_left()
    grid_up()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    grid_up()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_22():
    open_grid(0)
    menu_grid.move_first()
    grid_left()
    grid_down()
    grid_down()
    grid_down()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_up()
    grid_up()
    grid_up()
    grid_left()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("lv3", "none")
    menu_grid.use_and_move()
    grid_up()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_23():
    open_grid(0)
    menu_grid.move_first()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    grid_down()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_24():
    open_grid(0)
    menu_grid.move_first()
    grid_left()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_up()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_down()
    grid_down()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    grid_up()
    grid_left()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_down()
    grid_up()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def nem_gridding_25():  # End Tidus grid, Quick Hit
    open_grid(0)
    menu_grid.move_first()
    grid_up()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_down()
    grid_right()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("lv3", "none")
    menu_grid.use_and_move()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_down()
    grid_down()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("ability", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("lv3", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


# Backtrack to Auto-life, or can go through Yuna's grid on refactor.
def nem_gridding_26():
    if (
        memory.main.get_item_slot(84) == 255
        or memory.main.get_item_count_slot(memory.main.get_item_slot(84)) == 1
    ):
        return False
    open_grid(0)
    menu_grid.move_first()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    grid_up()
    grid_right()
    grid_up()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("mp", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_move()
    #grid_down()
    #grid_right()
    grid_up()
    grid_up()
    grid_right()
    grid_right()
    grid_down()
    #grid_up()
    #grid_right()
    #grid_left()
    #grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_down()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("lv4", "none")
    menu_grid.use_and_move()
    grid_up()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("ability", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return True


def lulu_bribe():
    open_grid(5)
    menu_grid.move_first()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("ability", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()


def rikku_haste():
    open_grid(character=6)

    menu_grid.move_first()
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
    menu_grid.move_and_use()
    menu_grid.sel_sphere("ability", "aftersk")
    menu_grid.use_and_quit()
    memory.main.close_menu()


def rikku_provoke():
    open_grid(6)
    menu_grid.move_first()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("ability", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()


def kimahri_dispel():
    open_grid(3)
    menu_grid.move_first()
    grid_up()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("lv2", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("ability", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()


def yuna_use_command():
    open_grid(1)
    menu_grid.use_first()
    menu_grid.sel_sphere("friend", "none")
    menu_grid.use_and_move()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("ability", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("ability", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()


def wakka_aim_command():
    open_grid(4)
    menu_grid.move_first()
    grid_right()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("ability", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()


def rikku_nulblaze():
    open_grid(6)
    menu_grid.move_first()
    grid_down()
    grid_down()
    grid_left()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("lv2", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    grid_up()
    grid_left()
    grid_left()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("ability", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()


def str_boost():
    open_grid(0)
    menu_grid.use_first()
    menu_grid.sel_sphere("strength", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_right()
    grid_right()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("strength", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("strength", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("strength", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_down()
    grid_left()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("strength", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("strength", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("strength", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    '''
    menu_grid.use_and_move()
    grid_left()
    grid_up()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("strength", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("strength", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    '''
    menu_grid.use_and_quit()
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
    menu.remove_all_nea()
