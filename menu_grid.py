import logging

import memory.main
import vars
import xbox

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def grid_up():
    FFXC.set_value("d_pad", 1)
    memory.main.wait_frames(2)
    FFXC.set_value("d_pad", 0)
    memory.main.wait_frames(3)


def grid_down():
    FFXC.set_value("d_pad", 2)
    memory.main.wait_frames(2)
    FFXC.set_value("d_pad", 0)
    memory.main.wait_frames(3)


def grid_left():
    FFXC.set_value("d_pad", 4)
    memory.main.wait_frames(2)
    FFXC.set_value("d_pad", 0)
    memory.main.wait_frames(3)


def grid_right():
    FFXC.set_value("d_pad", 8)
    memory.main.wait_frames(2)
    FFXC.set_value("d_pad", 0)
    memory.main.wait_frames(3)


def grid_tidus():
    if memory.main.s_grid_char() == 0:
        return True
    else:
        return False


def grid_kimahri():
    if memory.main.s_grid_char() == 3:
        return True
    else:
        return False


def grid_auron():
    if memory.main.s_grid_char() == 2:
        return True
    else:
        return False


def grid_lulu():
    if memory.main.s_grid_char() == 5:
        return True
    else:
        return False


def grid_wakka():
    if memory.main.s_grid_char() == 4:
        return True
    else:
        return False


def grid_yuna():
    if memory.main.s_grid_char() == 1:
        return True
    else:
        return False


def grid_rikku():
    if memory.main.s_grid_char() == 6:
        return True
    else:
        return False


def first_position():
    if memory.main.s_grid_menu() == 255:
        if memory.main.get_grid_move_active():
            return False
        else:
            return True
    else:
        return False


def move_use_menu():
    if memory.main.s_grid_menu() == 7:
        return True
    else:
        return False


def move_ready():
    if move_use_menu():
        if memory.main.get_grid_move_use_pos() == 0:
            return True
        else:
            return False
    elif ready_use_sphere() or move_active():
        xbox.menu_a()
    else:
        return False


def move_active():
    if memory.main.get_grid_move_active() and memory.main.s_grid_menu() == 255:
        return True
    else:
        return False


def move_complete():
    if memory.main.get_grid_move_active() and memory.main.s_grid_menu() == 11:
        return True
    else:
        return False


def use_ready():
    if move_use_menu():
        if memory.main.get_grid_move_use_pos() == 1:
            return True
        else:
            return False
    elif ready_use_sphere() or move_active():
        xbox.menu_a()
    else:
        return False


def ready_select_sphere():
    if memory.main.s_grid_menu() == 8:
        return True
    else:
        return False


def ready_use_sphere():
    if memory.main.get_grid_use_active():
        return True
    else:
        return False


def quit_grid_ready():
    if memory.main.s_grid_menu() == 11:
        if use_ready():
            return False
        elif move_complete():
            return False
        else:
            return True
    else:
        return False


def use_first():
    logger.debug("use first")
    while not ready_select_sphere():
        if first_position():
            xbox.menu_b()
        elif move_ready():
            xbox.menu_down()
        elif use_ready():
            xbox.menu_b()
    return True


def move_first():
    logger.debug("move first")
    while not move_active():
        if first_position():
            xbox.menu_b()
        elif move_ready():
            xbox.menu_b()
            memory.main.wait_frames(3)
        elif use_ready():
            xbox.menu_up()
    return True


def move_and_use():
    logger.debug("move and use")
    memory.main.wait_frames(1)
    xbox.menu_b()
    memory.main.wait_frames(1)
    while not ready_select_sphere():
        if move_complete() or first_position():
            xbox.menu_b()
        elif move_ready():
            xbox.menu_down()
        elif use_ready():
            xbox.menu_b()
    return True


def use_and_move():
    logger.debug("use and move")
    memory.main.wait_frames(1)
    xbox.menu_b()
    memory.main.wait_frames(1)
    while not move_active():
        if ready_use_sphere() or first_position():
            xbox.menu_b()
        elif move_ready():
            xbox.menu_b()
        elif use_ready():
            xbox.menu_up()
        else:
            xbox.menu_b()
    return True


def use_and_use_again():
    logger.debug("use and use again")
    memory.main.wait_frames(1)
    xbox.menu_b()
    memory.main.wait_frames(1)
    while not ready_select_sphere():
        if ready_use_sphere() or first_position():
            xbox.menu_b()
        elif move_ready():
            xbox.menu_down()
        elif use_ready():
            xbox.menu_b()
    if game_vars.use_pause():
        memory.main.wait_frames(6)
    return True


def use_shift_left(toon):
    logger.debug("use and shift")
    memory.main.wait_frames(1)
    xbox.menu_b()
    toon = toon.lower()
    if toon == "yuna":
        while not grid_yuna():
            if ready_use_sphere():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_left()
    if toon == "lulu":
        while not grid_lulu():
            if ready_use_sphere():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_left()
    if toon == "auron":
        while not grid_auron():
            if ready_use_sphere():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_left()
    if toon == "wakka":
        while not grid_wakka():
            if ready_use_sphere():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_left()
    if toon == "tidus":
        while not grid_tidus():
            if ready_use_sphere():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_left()
    if toon == "kimahri":
        while not grid_kimahri():
            if ready_use_sphere():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_left()
    if toon == "rikku":
        while not grid_rikku():
            if ready_use_sphere():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_left()
    logger.debug(f"Ready for grid: {toon}")


def use_shift_right(toon):
    logger.debug("use and shift")
    xbox.menu_b()
    toon = toon.lower()
    if toon == "yuna":
        while not grid_yuna():
            if ready_use_sphere():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_right()
    if toon == "lulu":
        while not grid_lulu():
            if ready_use_sphere():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_right()
                memory.main.wait_frames(30 * 0.3)
    if toon == "auron":
        while not grid_auron():
            if ready_use_sphere():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_right()
    if toon == "wakka":
        while not grid_wakka():
            if ready_use_sphere():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_right()
    if toon == "tidus":
        while not grid_tidus():
            if ready_use_sphere():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_right()
    if toon == "kimahri":
        while not grid_kimahri():
            if ready_use_sphere():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_right()
    if toon == "rikku":
        while not grid_rikku():
            if ready_use_sphere():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_right()
    logger.debug(f"Ready for grid: {toon}")


def move_shift_left(toon):
    logger.debug("Move and shift, left")
    memory.main.wait_frames(2)
    xbox.menu_b()
    memory.main.wait_frames(2)
    toon = toon.lower()
    if toon == "yuna":
        while not grid_yuna():
            if move_ready() or move_active() or move_complete():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_left()
    if toon == "lulu":
        while not grid_lulu():
            if move_ready() or move_active() or move_complete():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_left()
    if toon == "tidus":
        while not grid_tidus():
            if move_ready() or move_active() or move_complete():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_left()
    if toon == "rikku":
        while not grid_rikku():
            if move_ready() or move_active() or move_complete():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_left()
    logger.debug(f"Ready for grid: {toon}")


def move_shift_right(toon):
    logger.debug("Move and shift, right")
    memory.main.wait_frames(2)
    xbox.menu_b()
    memory.main.wait_frames(2)
    toon = toon.lower()
    if toon == "yuna":
        while not grid_yuna():
            if move_ready() or move_active() or move_complete():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_right()
    elif toon == "lulu":
        while not grid_lulu():
            if move_ready() or move_active() or move_complete():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_right()
    if toon == "tidus":
        while not grid_tidus():
            if move_ready() or move_active() or move_complete():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_right()
    if toon == "rikku":
        while not grid_rikku():
            if move_ready() or move_active() or move_complete():
                xbox.menu_b()
            elif move_use_menu():
                xbox.menu_back()
            elif first_position():
                xbox.shoulder_right()
    logger.debug(f"Ready for grid: {toon}")


def use_and_quit():
    memory.main.wait_frames(30 * 0.1)
    xbox.menu_b()
    while memory.main.s_grid_active():
        if ready_use_sphere():
            logger.debug("Using the current item.")
            xbox.menu_b()
        elif first_position():
            logger.debug("Opening the Quit menu")
            xbox.menu_a()
        elif quit_grid_ready():
            logger.debug("quitting sphere grid")
            xbox.menu_b()
    while memory.main.menu_number() != 5:
        pass
    return True


def sphere_num(s_type) -> int:
    s_type = s_type.lower()
    if s_type == "power":
        return 70
    elif s_type == "mana":
        return 71
    elif s_type == "speed":
        return 72
    elif s_type == "ability":
        return 73
    elif s_type == "fortune":
        return 74
    elif s_type == "attribute":
        return 75
    elif s_type == "special":
        return 76
    elif s_type == "skill":
        return 77
    elif s_type == "wmag":
        return 78
    elif s_type == "bmag":
        return 79
    elif s_type == "master":
        return 80
    elif s_type == "lv1":
        return 81
    elif s_type == "lv2":
        return 82
    elif s_type == "lv3":
        return 83
    elif s_type == "lv4":
        return 84
    elif s_type == "hp":
        return 85
    elif s_type == "mp":
        return 86
    elif s_type == "strength":
        return 87
    elif s_type == "defense":
        return 88
    elif s_type == "magic":
        return 89
    elif s_type == "mdef":
        return 90
    elif s_type == "agility":
        return 91
    elif s_type == "evasion":
        return 92
    elif s_type == "accuracy":
        return 93
    elif s_type == "luck":
        return 94
    elif s_type == "clear":
        return 95
    elif s_type == "ret":
        return 96
    elif s_type == "friend":
        return 97
    elif s_type == "tele":
        return 98
    elif s_type == "warp":
        return 99
    return 255


def sel_sphere(s_type, shift):
    s_num = 255
    menu_pos = 0
    logger.debug("------------------------------")
    logger.debug(s_type)
    s_num = sphere_num(s_type)
    logger.debug(s_num)
    menu_pos = memory.main.get_grid_items_slot(s_num)
    logger.debug(menu_pos)
    logger.debug("------------------------------")
    if menu_pos == 255:
        logger.debug(f"Sphere {s_type} is not in inventory.")
        return
    while menu_pos != memory.main.get_grid_cursor_pos():
        if menu_pos > memory.main.get_grid_cursor_pos():
            if game_vars.use_pause():
                xbox.tap_down()
            else:
                if (
                    menu_pos - memory.main.get_grid_cursor_pos() >= 3
                    and len(memory.main.get_grid_items_order()) > 4
                ):
                    if (
                        menu_pos - memory.main.get_grid_cursor_pos() == 3
                        and menu_pos == len(memory.main.get_grid_items_order()) - 1
                    ):
                        xbox.tap_down()
                    else:
                        xbox.trigger_r()
                else:
                    xbox.tap_down()
        elif menu_pos < memory.main.get_grid_cursor_pos():
            if game_vars.use_pause():
                xbox.tap_up()
            else:
                if memory.main.get_grid_cursor_pos() - menu_pos >= 3:
                    if (
                        menu_pos == 0
                        and memory.main.get_grid_cursor_pos() - menu_pos == 3
                    ) or len(memory.main.get_grid_items_order()) <= 4:
                        xbox.tap_up()
                    else:
                        xbox.trigger_l()
                else:
                    xbox.tap_up()
    while not memory.main.sphere_grid_placement_open():
        xbox.menu_b()
    if shift == "up":
        grid_up()
    if shift == "left":
        grid_left()
    if shift == "l2":
        grid_left()
        grid_left()
    if shift == "l5":
        grid_left()
        grid_left()
        grid_left()
        grid_left()
        grid_left()
    if shift == "right":
        grid_right()
    if shift == "r2":
        grid_right()
        grid_right()
    if shift == "down":
        grid_down()
    if shift == "d2":
        grid_down()
        grid_down()
    if shift == "up2":
        grid_up()
        grid_up()
    if shift == "d5":
        grid_down()
        grid_down()
        grid_down()
        grid_down()
        grid_down()
    if shift == "aftersk":
        grid_up()
        grid_right()
        grid_down()
        memory.main.wait_frames(4)
        if memory.main.s_grid_node_selected() == [248, 195]:
            grid_down()
    if shift == "aftersk2":
        grid_right()
        grid_right()
        memory.main.wait_frames(30 * 0.1)
        grid_left()
    if shift == "after_by_spec":
        grid_right()
        grid_right()
        grid_up()
    if shift == "torikku":
        memory.main.wait_frames(30 * 0.2)
        grid_down()
        grid_down()
        grid_left()
        grid_left()
    if shift == "yunaspec":
        # Yuna Special
        grid_down()
        grid_right()
        grid_right()
        grid_down()
        grid_down()
    while memory.main.sphere_grid_placement_open():
        xbox.menu_b()
