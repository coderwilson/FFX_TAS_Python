import memory.main
import vars
game_vars = vars.vars_handle()
import logging
logger = logging.getLogger(__name__)
from json_ai_files.write_seed import write_big_text
from blitzball import blitz_class
blitz_state = blitz_class.blitz_state_handle()

def goers_score_first():
    if not active_clock():
        return False
    if blitz_state.debug_mode == "flags":
        write_big_text(f"Flag: {memory.main.diag_progress_flag()} | Menu: {memory.main.blitz_menu_num()}")
    return memory.main.diag_progress_flag() in [47, 48, 49]


def halftime_dialog():
    if blitz_state.debug_mode == "flags":
        write_big_text(f"Flag: {memory.main.diag_progress_flag()} | Menu: {memory.main.blitz_menu_num()}")
    return memory.main.diag_progress_flag() in [45, 46]


def select_movement_style():
    if blitz_state.debug_mode == "flags":
        write_big_text(f"Flag: {memory.main.diag_progress_flag()} | Menu: {memory.main.blitz_menu_num()}")
    return memory.main.blitz_menu_num() in [145, 146]


def select_formation():
    if blitz_state.debug_mode == "flags":
        write_big_text(f"Flag: {memory.main.diag_progress_flag()} | Menu: {memory.main.blitz_menu_num()}")
    return memory.main.blitz_menu_num() in range(122, 145)


def select_formation_2():
    if blitz_state.debug_mode == "flags":
        write_big_text(f"Flag: {memory.main.diag_progress_flag()} | Menu: {memory.main.blitz_menu_num()}")
    return memory.main.blitz_menu_num() == 144


def select_breakthrough():
    memory.main.wait_frames(3)
    if blitz_state.debug_mode == "flags":
        write_big_text(f"Flag: {memory.main.diag_progress_flag()} | Menu: {memory.main.blitz_menu_num()}")
    if active_clock():
        return False
    if (
        memory.main.blitz_menu_num() >= 0 and memory.main.blitz_menu_num() <= 46
    ) or memory.main.blitz_menu_num() == 246:
        return True
    else:
        return False


def select_action():
    memory.main.wait_frames(3)
    if blitz_state.debug_mode == "flags":
        write_big_text(f"Flag: {memory.main.diag_progress_flag()} | Menu: {memory.main.blitz_menu_num()}")
    if active_clock():
        return False
    return memory.main.blitz_menu_num() in range(47, 53)


def select_pass_target():
    memory.main.wait_frames(3)
    if blitz_state.debug_mode == "flags":
        write_big_text(f"Flag: {memory.main.diag_progress_flag()} | Menu: {memory.main.blitz_menu_num()}")
    if active_clock():
        return False
    if memory.main.blitz_menu_num() == 246:
        return False
    return memory.main.blitz_menu_num() in range(226, 256)


def select_shot_type():
    memory.main.wait_frames(3)
    if blitz_state.debug_mode == "flags":
        write_big_text(f"Flag: {memory.main.diag_progress_flag()} | Menu: {memory.main.blitz_menu_num()}")
    if active_clock():
        return False
    return memory.main.blitz_menu_num() in range(111, 118)


def targeted_player():
    return memory.main.blitz_target_player() - 2


def active_clock():
    return not memory.main.blitz_clock_pause()


def aurochs_control():
    return memory.main.blitz_target_player() < 8


def controlling_player():
    ret_val = memory.main.blitz_current_player() - 2
    if ret_val < 200:
        return ret_val
    return 1


def half_summary_screen():
    return memory.main.get_map() == 212


def new_half():
    return memory.main.get_map() == 347


def halftime_spam():
    memory.main.click_to_diag_progress(20)


def game_clock():
    return memory.main.blitz_clock()


def cursor_1():
    return memory.main.blitz_cursor()
'''
def player_guarded(player_num):
    # Graav proximity always counts as guarded.
    if distance(player_num, 8) < 360:
        return True

    # Two or more player proximity always counts as guarded.
    other_distance = 0
    if distance(0, 6) < 360:
        other_distance += 1
    if distance(0, 7) < 360:
        other_distance += 1
    if distance(0, 9) < 360:
        other_distance += 1
    if distance(0, 10) < 360:
        other_distance += 1
    if other_distance >= 2:
        return True

    # Specific cases depending on player.
    if player_num in [3, 4]:
        if distance(player_num, 9) < 340:
            return True
        if distance(player_num, 10) < 340:
            return True
    return False


def distance(n1, n2):
    try:
        player1 = player_array[n1].get_coords()
        player2 = player_array[n2].get_coords()
        return abs(player1[1] - player2[1]) + abs(player1[0] - player2[0])
    except Exception as x:
        logger.exception(x)
        return 999
'''

def storyline():
    write_big_text(f"Flag: {memory.main.diag_progress_flag()} | Menu: {memory.main.blitz_menu_num()}")
    current = memory.main.get_story_progress()
    if not game_vars.csr():
        if current == 540:
            logger.info("Halftime hype")
            memory.main.click_to_diag_progress(164)
            memory.main.click_to_diag_progress(20)
        elif current == 560 and memory.main.diag_progress_flag() > 1:
            logger.info("Wakka story happening.")
            memory.main.click_to_diag_progress(11)
            while not active_clock():
                xbox.tap_b()
        # First half is 535
        # Hype halftime is 540
        # Second half starts on 560
        # 575 - Wakka is in the game


