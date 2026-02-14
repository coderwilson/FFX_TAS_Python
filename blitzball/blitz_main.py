import vars
import xbox
import logging
import datetime
import rng_track
logger = logging.getLogger(__name__)
from json_ai_files.write_seed import write_big_text

from json_ai_files.write_seed import write_blitz_results
from area.dream_zan import split_timer
from memory.main import (
    click_to_story_progress,
    get_story_progress,
    diag_progress_flag,
    diag_skip_possible,
    get_map,
    wait_frames,
    blitzball_patriots_style
)
from blitzball.blitz_tools import (
    storyline,
    game_clock,
    active_clock,
    select_movement_style,
    select_formation,
    select_formation_2,
    cursor_1,
    new_half,
    goers_score_first,
    halftime_dialog,
    aurochs_control,
    half_summary_screen
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

def general_game():
    last_phase = blitz_state.current_stage
    while True:  # End of Blitz
        logger.debug("First half")

        try:
            clock = game_clock()
            if last_phase != blitz_state.current_stage and clock > 0 and clock < 301:
                last_phase = blitz_state.current_stage
                logger.info(f"New phase reached: {last_phase}")
            if get_map() == 62:
                attempt_goals(timed=False)
            else:
                FFXC.set_neutral()
                if blitz_state.last_dialog != diag_progress_flag():
                    blitz_state.last_dialog = diag_progress_flag()
                    logger.debug(f"Dialog progress change: {blitz_state.last_dialog}")
                if half_summary_screen():
                    if diag_progress_flag() == 113:
                        if cursor_1() != 0:  # Continue or quit?
                            wait_frames(60)
                            xbox.menu_up()
                            wait_frames(3)
                        else:
                            wait_frames(60)
                            xbox.menu_b()
                            wait_frames(90)
                            return 0
                    elif (
                        diag_skip_possible()
                    ):  # Skip through everything else
                        if game_vars.story_mode():
                            if get_story_progress() in [535,575]:
                                xbox.tap_confirm()
                            #logger.debug(f"{get_story_progress()}, {diag_progress_flag()}")
                        else:
                            xbox.menu_b()
                elif new_half():
                    logger.debug("Starting new half")
                    if diag_progress_flag() == 347:
                        # Used for repeated Blitz games, not for story.
                        movement_set_flag = False
                    prep_half()
                else:
                    storyline()  # Wakka talking, boys cheering, etc
        except Exception as x_val:
            logger.error("Caught exception in blitz memory.main.:")
            logger.exception(x_val)

def story_first_half():
    logger.warning(f"First half started")
    # First we should set proper movement.
    logger.debug(f"Attempting to set formation (A)")

    while not select_movement_style():
        blitz_state.update()
        # logger.debug(blitz_state.controlling_player_index)
        if aurochs_control():
            xbox.tap_y()
        elif goers_score_first():
            xbox.tap_confirm()
    FFXC.set_neutral()
    logger.debug(f"Attempting to set formation (B)")
    # Now do all the selections
    while not active_clock():
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
            else:
                xbox.menu_up()
        elif select_formation_2():
            if blitz_state.last_menu != 5:
                logger.debug("Selecting Formation")
                blitz_state.last_menu = 5
            if cursor_1() == 7:
                xbox.menu_b()
            else:
                xbox.menu_up()
    logger.debug(f"Formation set - complete (C)")

    # Now to actually play the game
    while get_story_progress() < 560:
        # Mid-game dialog should be skipped
        if goers_score_first() or halftime_dialog():
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
        elif diag_skip_possible():
            if goers_score_first():
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

        

def blitz_engage(force_blitz_win):
    logger.info("-Start of Blitzball program")
    logger.info("-First, clicking to the start of the match.")
    click_to_story_progress(535)
    logger.info("-Match is now starting.")
    start_time = datetime.datetime.now()

    if get_story_progress() > 700:
        logger.info(f"Engaging Post-Luca game")
        general_game()
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



