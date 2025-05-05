import logging

import memory.main
import vars
import xbox
import battle.main
import pathing

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def arena_npc():
    memory.main.await_control()
    if memory.main.get_map() != 307:
        return
    while not (
        memory.main.diag_progress_flag() == 74 and memory.main.diag_skip_possible()
    ):
        if memory.main.user_control():
            if memory.main.get_coords()[1] > -12 and memory.main.get_actor_angle(0) > -1:
                xbox.menu_down()
                memory.main.wait_frames(12)
            else:
                pathing.approach_actor_by_id(actor_id=8241)
        else:
            FFXC.set_neutral()
            if memory.main.diag_progress_flag() == 59:
                xbox.menu_a()
                xbox.menu_a()
                xbox.menu_a()
                xbox.tap_b()
            elif memory.main.diag_skip_possible():
                xbox.tap_b()
    memory.main.wait_frames(3)  # This buffer can be improved later.


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
    #logger.debug(memory.main.arena_cursor())
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
    logger.debug(f"Selecting menu option: {choice}")
    if game_vars.use_pause():
        memory.main.wait_frames(2)
    if choice == 4:
        while not memory.main.user_control():
            if memory.main.battle_wrap_up_active():
                xbox.tap_confirm()
            elif memory.main.diag_skip_possible():
                if memory.main.blitz_cursor() != 4 or memory.main.menu_open():
                    xbox.tap_back()
                else:
                    xbox.tap_confirm()
            else:
                # I don't know, something goes here I guess.
                pass
                #logger.warning("Attempting to select option 4 - Unidentified state. Standing by.")
    else:
        if memory.main.user_control():
            arena_npc()
        elif memory.main.diag_skip_possible():
            while not memory.main.blitz_cursor() == choice:
                while not memory.main.blitz_cursor() == choice:
                    if memory.main.battle_wrap_up_active():
                        battle.main.wrap_up()
                    elif choice == 3:
                        xbox.menu_up()
                    else:
                        xbox.menu_down()
                    memory.main.wait_frames(1)
                    if game_vars.use_pause():
                        memory.main.wait_frames(2)
                memory.main.wait_frames(2)
        xbox.menu_b()
        memory.main.wait_frames(3)


def get_arena_cursor():
    cursor_loaded = False
    while not cursor_loaded:
        try:
            cursor1 = memory.main.arena_cursor_1()
            cursor2 = (memory.main.arena_cursor_2() - 89)
            logger.debug(cursor2)
            #memory.main.wait_frames(30)
            cursor_loaded = True
        except:
            pass
    
    cursor_position = (cursor2 / 33) * 2
    if cursor1 == 318:
        cursor_position += 1
    return cursor_position
    


def start_fight(area_index: int, monster_index: int = 0):
    logger.debug(f"Starting fight: {area_index} | {monster_index}")
    arenaCursor = get_arena_cursor()
    #memory.main.wait_frames(60)
    while arenaCursor != area_index:
        while arenaCursor != area_index:
            arenaCursor = get_arena_cursor()
            if arenaCursor % 2 == 0 and area_index % 2 == 1:
                xbox.tap_right()
            elif arenaCursor % 2 == 1 and area_index % 2 == 0:
                xbox.tap_left()
            elif arenaCursor < area_index:
                xbox.tap_down()
            elif arenaCursor > area_index:
                xbox.tap_up()
        arenaCursor = get_arena_cursor()
        memory.main.wait_frames(2)
    xbox.menu_b()
    memory.main.wait_frames(6)
    # Do we need to find cursors for these as well?
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
