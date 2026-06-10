import vars
import xbox
import logging
import datetime
import rng_track
logger = logging.getLogger(__name__)
from json_ai_files.write_seed import write_big_text
import memory.main

from json_ai_files.write_seed import write_blitz_results
from area.dream_zan import split_timer
from memory.main import (
    click_to_story_progress,
    get_story_progress,
    diag_progress_flag,
    diag_skip_possible,
    get_map,
    wait_frames,
    blitzball_patriots_style,
    wait_seconds,
    save_popup_cursor
)
from blitzball.blitz_tools import (
    storyline,
    game_clock,
    select_movement_style,
    select_formation,
    cursor_1,
    new_half,
    dialog,
    aurochs_control,
    half_summary_screen,
    input_ready
)
from blitzball.blitz_actions import (
    tidus_needs_xp,
    jassu_train,
    prep_half,
    attempt_goals
)

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()

from blitzball import blitz_class
blitz_state = blitz_class.blitz_state_handle()

def general_game(
        first_match:bool=False, 
        tourney:bool=False, 
        jecht_shot:bool=False):
    last_phase = blitz_state.current_stage
    buffer_fast = 10
    buffer_slow = 60
    set_blitzers = first_match

    while True:  # End of Blitz
        try:
            clock = game_clock()
            if last_phase != blitz_state.current_stage and clock > 0 and clock < 300:
                last_phase = blitz_state.current_stage
                logger.info(f"New phase reached: {last_phase}")
                first_match = False
                jecht_shot = False
            if get_map() == 62:
                logger.info("Main Blitzball logic - Start")
                if first_match:
                    while not select_movement_style():
                        if dialog():
                            xbox.tap_confirm()
                        else:
                            blitz_state.update()
                            # logger.debug(blitz_state.controlling_player_index)
                            if aurochs_control():
                                xbox.tap_y()
                    FFXC.set_neutral()
                    logger.debug(f"Attempting to set formation (B)")
                    wait_seconds(2)
                    xbox.menu_down()
                    xbox.menu_b()
                    wait_seconds(2)
                    xbox.menu_b()
                    logger.debug(f"Formation set - complete (C)")
                    first_match = False
                    
                attempt_goals(timed=False)
            elif get_map() == 212:
                logger.info("Match summary screen")
                FFXC.set_neutral()
                # Match summary screens
                if diag_progress_flag() == 113:
                    if cursor_1() != 0:  # Continue or quit?
                        wait_frames(10)
                        xbox.menu_up()
                        wait_frames(3)
                    else:
                        wait_frames(10)
                        xbox.menu_b()
                        wait_frames(90)
                        return True
                else:
                    xbox.menu_b()
                    
            elif get_map() == 347:
                FFXC.set_neutral()
                logger.debug(f"Screen: {diag_progress_flag()}")
                if tourney and diag_progress_flag() == 135:
                    logger.info("Selecting tournament")
                    memory.main.wait_frames(2)
                    while save_popup_cursor() != 1:
                        if get_map() == 62:
                            break
                        if save_popup_cursor() > 2:
                            xbox.menu_up()
                        elif save_popup_cursor() == 2:
                            xbox.menu_up()
                            memory.main.wait_frames(3)
                            if save_popup_cursor() == 2:
                                xbox.tap_back()
                                xbox.tap_confirm()
                                return False  # Tournament is not available.
                        else:
                            xbox.menu_down()
                    wait_frames(3)
                    xbox.tap_confirm()
                    xbox.tap_confirm()
                elif diag_progress_flag() in [27,28]:
                    logger.info("Skill selection screen")
                    wait_frames(12)
                    if jecht_shot:
                        xbox.menu_b()
                        wait_frames(buffer_slow)
                        xbox.menu_b()
                        wait_frames(buffer_slow)
                        xbox.menu_b()
                        wait_frames(buffer_slow)
                        xbox.menu_a()
                        wait_frames(buffer_slow)
                        # xbox.menu_a()
                        # wait_frames(90)
                        jecht_shot = False
                    xbox.menu_a()
                    xbox.menu_b()
                    wait_frames(12)
                elif diag_progress_flag() in [20,134]:
                    test = diag_progress_flag()
                    logger.info(f"Special screen: {test}")
                    # 20 is skill selection, but with no XP gained.
                    # 134 is the Mark selection screen
                    wait_frames(12)
                    xbox.menu_a()
                    xbox.menu_b()
                    wait_seconds(2)
                    if test == 134:
                        xbox.menu_b()
                elif diag_progress_flag() == 41:
                    wait_frames(12)
                    for i in range(8):
                        # Print the actors in all the positions
                        memory.main.blitz_actor_order(i)
                    if memory.main.get_story_progress() > 700:
                        xbox.tap_confirm()  # Tidus
                        wait_frames(buffer_fast)
                        xbox.tap_confirm()  # Datto
                        wait_frames(buffer_fast)
                        xbox.tap_confirm()  # Letty
                        wait_frames(buffer_fast)
                        if set_blitzers:
                            xbox.menu_up()
                        xbox.tap_confirm()  # Ropp
                        wait_frames(buffer_fast)
                        if set_blitzers:
                            xbox.menu_up()
                        xbox.tap_confirm()  # Zalitz
                        wait_frames(buffer_fast)
                        if set_blitzers:
                            xbox.menu_up()
                        xbox.tap_confirm()  # Miyu
                        wait_frames(buffer_slow)
                        xbox.tap_confirm()
                        for i in range(8):
                            # Print the actors in all the positions
                            memory.main.blitz_actor_order(i)
                        wait_frames(buffer_slow)
                        if jecht_shot:
                            xbox.menu_b()
                            wait_frames(buffer_slow)
                            xbox.menu_b()
                            wait_frames(buffer_slow)
                            xbox.menu_b()
                            wait_frames(buffer_slow)
                            xbox.menu_a()
                            wait_frames(buffer_slow)
                            xbox.menu_a()
                            wait_frames(buffer_slow)
                        xbox.menu_a()
                        xbox.menu_b()
                        wait_frames(buffer_slow)
                        xbox.menu_a()
                        xbox.menu_b()
                        wait_frames(buffer_slow)
                        xbox.menu_b()
                        memory.main.wait_frames(30)
                        set_blitzers = False
                        for i in range(8):
                            # Print the actors in all the positions
                            memory.main.blitz_actor_order(i)
                        # memory.main.wait_frames(90000)
                    else:
                        if memory.main.diag_skip_possible():
                            logger.info("Quick selection")
                            xbox.menu_b()
                        memory.main.wait_frames(3)
                elif diag_progress_flag() in [22,23,24]:
                    # Stuck picking an ability
                    xbox.menu_a()
                    wait_seconds(2)
                    xbox.menu_a()
                    xbox.menu_b()
                # elif diag_progress_flag() == 135:
                #     # Select type of game
                #     xbox.menu_b()
                # elif diag_progress_flag() == 3:
                #     # Starting Game screen
                #     xbox.menu_b()
                else:
                    logger.info("Fallback, press B")
                    xbox.menu_b()
                    wait_seconds(1)

            else:
                FFXC.set_neutral()
                logger.warning("Unexpected map! How did we get here?!")
        except Exception as x_val:
            logger.error("Caught exception in blitz memory.main.:")
            logger.exception(x_val)

def story_first_half():
    logger.warning(f"First half started")
    # First we should set proper movement.
    logger.debug(f"Attempting to set formation (A)")
    formation_selected = False

    while not select_movement_style():
        blitz_state.update()
        # logger.debug(blitz_state.controlling_player_index)
        if aurochs_control():
            xbox.tap_y()
        if dialog():
            xbox.menu_b()
    FFXC.set_neutral()
    logger.debug(f"Attempting to set formation (B)")
    while not formation_selected:
        if select_movement_style():
            if blitz_state.last_menu != 4:
                logger.debug("Selecting movement method")
                blitz_state.last_menu = 4
            if cursor_1() == 1:
                xbox.menu_b()
            else:
                xbox.menu_down()
                logger.debug(cursor_1())
        elif select_formation():
            if blitz_state.last_menu != 5:
                logger.debug("Selecting Formation")
                blitz_state.last_menu = 5
            if cursor_1() == 0:
                xbox.menu_b()
                formation_selected = True
            else:
                xbox.menu_up()
    logger.debug(f"Formation set - complete (C)")

    # Now to actually play the game
    while get_story_progress() < 560:
        # Mid-game dialog should be skipped
        if dialog():
            if blitz_state.last_menu != 3:
                logger.debug("Dialog on-screen")
                blitz_state.last_menu = 3
            FFXC.set_neutral()
            xbox.menu_b()
        
        # Next handle everything outside the sphere
        elif get_map() != 62:
            FFXC.set_neutral()
            # Reports
            if blitz_state.last_dialog != diag_progress_flag():
                blitz_state.last_dialog = diag_progress_flag()
                logger.debug(f"Dialog progress change: {blitz_state.last_dialog}")
            
            # Actions
            if half_summary_screen() and diag_skip_possible():
                if not game_vars.story_mode():
                    xbox.tap_confirm()
                elif get_story_progress() in [535,575]:
                    xbox.tap_confirm()
            elif new_half():
                FFXC.set_neutral()
                logger.debug("Starting new half")
                prep_half()
            else:
                storyline()  # Wakka talking, boys cheering, etc
        
        # Finally, what do we do during the game?
        elif not blitz_state.tidus_xp_gained:
            tidus_needs_xp()
        else:
            jassu_train()
    logger.warning(f"First half complete")


def story_second_half():
    logger.warning(f"Second half started")
    while (get_story_progress() < 583):
        if get_map() != 62:
            FFXC.set_neutral()
            # Reports
            if blitz_state.last_dialog != diag_progress_flag():
                blitz_state.last_dialog = diag_progress_flag()
                logger.debug(f"Dialog progress change: {blitz_state.last_dialog}")
            
            # Actions
            if half_summary_screen() and diag_skip_possible():
                blitz_state.overtime = True
                if not game_vars.story_mode():
                    xbox.tap_confirm()
                elif get_story_progress() in [535,575]:
                    xbox.tap_confirm()
            if new_half():
                prep_half()
                blitz_state.overtime = True
        elif diag_skip_possible() and not input_ready():
            if dialog():
                xbox.tap_b()
            else:
                xbox.tap_b()
        elif blitz_state.overtime:
            # Score as fast as possible
            attempt_goals()
        elif blitz_state.own_score > blitz_state.opp_score:
            # While winning, we should not try to score again.
            jassu_train()
        else:
            # Attempt scoring at specific times
            attempt_goals()
    logger.warning(f"Second half complete")

        

def blitz_engage(force_blitz_win, first_match:bool=False, tourney:bool=False, jecht_shot:bool=False):
    logger.info("-Start of Blitzball program")
    logger.info("-First, clicking to the start of the match.")
    click_to_story_progress(535)
    logger.info("-Match is now starting.")
    start_time = datetime.datetime.now()

    if get_story_progress() > 700:
        logger.info(f"Engaging Post-Luca game")
        general_game(first_match=first_match, tourney=tourney, jecht_shot=jecht_shot)
        write_big_text("")
        return
    else:
        logger.info(f"First half")
        story_first_half()
        if force_blitz_win:
            blitzball_patriots_style()
        prep_half()
        logger.info(f"Second half")
        story_second_half()

    blitz_state.update()
    logger.info("Blitz game has completed.")
    split_timer()
    # Set the blitz_win flag for the rest of the run.
    logger.info(
        f"Final scores: Aurochs: {blitz_state.own_score}, "
        + f"Opponent score: {blitz_state.opp_score}"
    )
    write_big_text(
        f"Final scores:\nAurochs: {blitz_state.own_score}\n"
        + f"Goers score: {blitz_state.opp_score}"
    )
    FFXC.set_neutral()
    if blitz_state.own_score > blitz_state.opp_score:
        game_vars.set_blitz_win(True)
        write_blitz_results("Yes")
    else:
        game_vars.set_blitz_win(False)
        write_blitz_results("No")

    logger.debug("Blitz results registered.")
    end_time = datetime.datetime.now()
    time_diff = end_time - start_time
    total_time = int(time_diff.total_seconds())
    if game_vars.get_force_blitz_win() or game_vars.story_mode() or game_vars.platinum():
        pass
    else:
        rng_track.record_blitz_results(duration=total_time)
    logger.info(f"--Blitz Win value: {game_vars.get_blitz_win()}")
    return total_time



