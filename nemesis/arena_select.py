import logging

import memory.main
import vars
import xbox

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def area_array():
    # Not working properly
    return [
        60112,
        60736,
        61672,
        62296,
        62920,
        63544,
        58240,
        58552,
        59176,
        59488,
        59800,
        60424,
        61360,
        61984,
        62608,
        63232,
    ]


def area_index_check(index_num: int = 15):
    # Not working properly
    logger.debug(memory.main.arena_cursor())
    if memory.main.arena_array[index_num] == memory.main.arena_cursor():
        return True
    return False


def arena_cursor():
    # Not working properly
    for x in range(16):
        logger.debug(memory.main.arena_cursor())
        if memory.main.arena_cursor() == area_array()[x]:
            return x
    return 255


def arena_menu_select(choice: int = 2):
    logger.debug("Selecting menu option: ", choice)
    if game_vars.use_pause():
        memory.main.wait_frames(2)
    while not memory.main.blitz_cursor() == choice:
        if choice == 4:
            xbox.menu_a()
        elif choice == 3:
            xbox.menu_up()
        else:
            xbox.menu_down()
        memory.main.wait_frames(1)
    xbox.tap_b()
    xbox.tap_b()
    memory.main.wait_frames(15)


def start_fight(area_index: int, monster_index: int = 0):
    logger.debug("Starting fight: ", area_index, " | ", monster_index)
    arenaCursor = 0
    memory.main.wait_frames(90)
    while arenaCursor != area_index:
        # logger.debug(arenaCursor())
        if arenaCursor % 2 == 0 and area_index % 2 == 1:
            xbox.tap_right()
            arenaCursor += 1
        elif arenaCursor % 2 == 1 and area_index % 2 == 0:
            xbox.tap_left()
            arenaCursor -= 1
        elif arenaCursor < area_index:
            xbox.tap_down()
            arenaCursor += 2
        else:
            xbox.tap_up()
            arenaCursor -= 2
    xbox.menu_b()
    memory.main.wait_frames(6)
    if monster_index >= 7:
        xbox.tap_right()
        monster_index -= 7
    while monster_index > 0:
        xbox.tap_down()
        monster_index -= 1
    xbox.tap_b()
    memory.main.wait_frames(6)
    xbox.tap_b()
    while not memory.main.battle_active():
        pass
