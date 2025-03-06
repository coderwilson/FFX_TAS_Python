import logging

import battle.boss
import battle.main
import logs
import memory.main
from memory.main import check_near_actors
import manip_planning.baaj_to_tros
import pathing
import rng_track
import save_sphere
import tts
import vars
import xbox
from paths import AllStartsHere, TidusHomeMovement
from players import Auron, CurrentPlayer, Tidus
from json_ai_files.write_seed import write_seed_num, write_seed_err, write_big_text

game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()

logger = logging.getLogger(__name__)


def new_game(gamestate):
    logger.info("Starting the game")
    logger.debug(f"Gamestate: {gamestate}")

    last_message = 0
    # New version
    if gamestate == "none":  # New Game
        while memory.main.get_map() != 0:
            if memory.main.get_map() != 23:
                if last_message != 1:
                    last_message = 1
                    logger.info("Attempting to get to New Game screen")
                FFXC.set_value("btn_start", 1)
                memory.main.wait_frames(1)
                FFXC.set_value("btn_start", 0)
                memory.main.wait_frames(1)
            elif memory.main.save_menu_open():
                if last_message != 2:
                    last_message = 2
                    logger.info("Load Game menu is open. Backing out.")
                xbox.tap_a()
            elif memory.main.save_menu_cursor() == 1:
                if last_message != 3:
                    last_message = 3
                    logger.info("New Game is not selected. Switching.")
                xbox.menu_up()
            else:
                if last_message != 4:
                    last_message = 4
                    logger.info("New Game is selected. Starting game.")
                xbox.menu_b()
        if game_vars.use_legacy_soundtrack():
            memory.main.click_to_diag_progress(6,force=True)
            # tts.message("Setting original soundtrack")
            memory.main.wait_frames(3)
            xbox.tap_down()
            memory.main.wait_frames(3)
            memory.main.click_to_diag_progress(8,force=True)
        else:
            memory.main.click_to_diag_progress(7,force=True)
            for i in range(8):
                xbox.tap_b()
    else:  # Load Game
        while not memory.main.save_menu_open():
            if memory.main.get_map() != 23:
                FFXC.set_value("btn_start", 1)
                memory.main.wait_frames(1)
                FFXC.set_value("btn_start", 0)
                memory.main.wait_frames(1)
            elif memory.main.save_menu_cursor() == 0:
                xbox.menu_down()
            else:
                xbox.menu_b()


def new_game_2():
    # New game selected. Next, select options.
    time_buffer = 15
    #logger.info("====================================")
    #logger.info("Starting in")
    #logger.info("33")
    #memory.main.wait_frames(time_buffer)
    #logger.info("2")
    #memory.main.wait_frames(time_buffer)
    ##logger.info("1")
    #memory.main.wait_frames(time_buffer)
    logger.info("GO!!! Good fortune!")
    logger.info("====================================")
    #logger.info(f"Set seed: {memory.main.rng_seed()}")
    xbox.menu_b()
    xbox.menu_b()


def listen_story():
    memory.main.wait_frames(10)
    vars.init_vars()
    while not memory.main.user_control():
        if memory.main.get_map() == 132:
            if memory.main.diag_progress_flag() == 1:
                game_vars.set_csr(False)
                logger.info("Skipping intro scene, we'll watch this properly later")
                memory.main.await_control()
            if game_vars.accessibility_vars()[0]:
                FFXC.set_value("btn_back", 1)
                memory.main.wait_frames(1)
                FFXC.set_value("btn_back", 0)
                memory.main.wait_frames(1)

    logger.info(f"### CSR check: {game_vars.csr()}")
    write_big_text("")
    checkpoint = 0
    zanar_wait = game_vars.story_mode()
    while memory.main.get_encounter_id() != 414:  # First Sinspawn
        if memory.main.user_control():
            # Events
            if checkpoint == 6:
                #while not pathing.set_movement([15,9]):
                #    pass
                check_near_actors(False)
                pathing.approach_actor_by_id(8544)
                FFXC.set_neutral()
                #FFXC.set_movement(-1, -1)
                while not memory.main.name_aeon_ready():
                    pass
                logger.info("Ready to name Tidus")
                FFXC.set_neutral()
                memory.main.wait_frames(6)

                # Name Tidus
                xbox.name_aeon("Tidus")
                logger.info("Tidus name complete.")

                checkpoint += 1
            # elif checkpoint == 7 and game_vars.csr():
            #    checkpoint = 9
            elif checkpoint == 8:
                check_near_actors(False)
                #while memory.main.user_control():
                #    FFXC.set_movement(1, 0)
                #    xbox.tap_b()
                pathing.approach_actor_by_id(8201)
                FFXC.set_neutral()
                memory.main.click_to_control()
                checkpoint += 1
            elif checkpoint < 11 and memory.main.get_story_progress() >= 5:
                checkpoint = 11
                if zanar_wait:  # Story mode only
                    zanar_wait = False
                    FFXC.set_neutral()
                    memory.main.wait_seconds(50)
            elif checkpoint < 21 and memory.main.get_map() == 371:
                checkpoint = 21
            elif checkpoint < 25 and memory.main.get_map() == 370:
                checkpoint = 25
            elif checkpoint == 27:  # Don't cry.
                while memory.main.user_control():
                    FFXC.set_movement(1, -1)
                FFXC.set_neutral()
                checkpoint += 1
            # General pathing
            elif pathing.set_movement(TidusHomeMovement.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible() and not game_vars.story_mode():
                if (
                    memory.main.get_story_progress() == 10
                    and memory.main.diag_progress_flag() == 2
                ):
                    logger.info("Special Skip")
                    memory.main.wait_frames(130)
                    # Generate button to skip later
                    FFXC.set_value("btn_start", 1)
                    memory.main.wait_frames(1)
                    FFXC.set_value("btn_start", 0)
                    xbox.skip_dialog(10)
                else:
                    if game_vars.use_pause():
                        memory.main.wait_frames(1)
                    xbox.skip_scene(fast_mode=True)
                    xbox.skip_dialog(3)


def ammes_battle_truerng():
    logger.info("Starting ammes")
    xbox.click_to_battle()
    logger.debug("Auron Overdrive turn start")
    memory.main.last_hit_init()
    CurrentPlayer().defend()
    # logs.write_stats("First Six Hits:")
    hits_array = []

    logger.info("Killing Sinspawn")
    while memory.main.battle_active():
        if memory.main.turn_ready():
            CurrentPlayer().attack(record_results=True)
            last_hit = memory.main.last_hit_check_change()
            while last_hit == 9999:
                last_hit = memory.main.last_hit_check_change()
            logger.debug(f"Recorded hit: {last_hit}")
            hits_array.append(last_hit)
            logger.debug(f"{hits_array}")
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
    logger.debug(f"Unconfirmed seed check: {memory.main.rng_seed()}")
    correct_seed = rng_track.hits_to_seed(hits_array=hits_array)
    logs.write_stats("Corrected RNG seed:")
    logs.write_stats(correct_seed)
    logger.debug(f"Corrected RNG seed: {correct_seed}")
    if correct_seed != "Err_seed_not_found":
        game_vars.set_confirmed_seed(correct_seed)
        write_seed_num(seed=memory.main.rng_seed())
    else:
        logging.error(f"Unable to derive seed from recorded hits: {hits_array}")
        write_seed_err()
    logger.info(f"Confirmed RNG seed: {memory.main.rng_seed()}")
    logger.info("Done Killing Sinspawn")
    memory.main.wait_frames(6)  # Just for no overlap
    logger.debug("Clicking to battle.")
    xbox.click_to_battle()
    logger.debug("Waiting for Auron's Turn")
    logger.debug("At Overdrive")
    # Auron overdrive tutorial
    Auron.overdrive()


def ammes_battle(tidus_total_attacks: int, tidus_potion: bool):
    logger.info("Starting ammes")
    xbox.click_to_battle()
    write_seed_num(seed=memory.main.rng_seed())
    logger.debug("Auron Overdrive turn start")
    memory.main.last_hit_init()

    auron_total_attacks = 6 - tidus_total_attacks
    tidus_attacks = 0
    auron_attacks = 0

    if tidus_potion:
        battle.main.use_potion_character(Tidus, "l")
    else:
        CurrentPlayer().defend()

    logger.info("Killing Sinspawn")
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if memory.main.get_current_turn() == 0:
                if tidus_attacks < tidus_total_attacks:
                    tidus_attacks += 1
                    logging.debug(f"Tidus Attack {tidus_attacks}/{tidus_total_attacks}")
                    CurrentPlayer().attack()
                else:
                    logging.debug(f"Tidus Defend because he has already filled his Attack quota")
                    CurrentPlayer().defend()
            else:
                if auron_attacks < auron_total_attacks:
                    auron_attacks += 1
                    logging.debug(f"Auron Attack {auron_attacks}/{auron_total_attacks}")
                    CurrentPlayer().attack()
                else:
                    logging.debug(f"Auron Defend because he has already filled his Attack quota")
                    CurrentPlayer().defend()
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
    logger.debug("Clicking to battle.")
    if game_vars.story_mode():
        memory.main.wait_seconds(42)
        FFXC.tap_confirm()
        FFXC.tap_confirm()
    else:
        xbox.click_to_battle()
    # Auron overdrive tutorial
    Auron.overdrive()


def after_ammes_truerng():
    memory.main.click_to_control()
    checkpoint = 0
    # memory.main.wait_frames(90)
    # logger.debug("MARK")
    # memory.main.ammes_fix(actor_index=0)
    # memory.main.wait_frames(90)

    while memory.main.get_map() != 49:
        if memory.main.user_control():
            start_pos = memory.main.get_coords()
            if int(start_pos[0]) in [866, 867, 868, 869, 870] and int(start_pos[1]) in [
                -138,
                -139,
                -140,
                -141,
            ]:
                logger.warning("Positioning error")
                FFXC.set_neutral()
                memory.main.wait_frames(20)
                memory.main.ammes_fix(actor_index=0)
                memory.main.wait_frames(20)
            else:
                # Map changes and events
                if checkpoint == 6:  # Save sphere
                    save_sphere.touch_and_go()
                    checkpoint += 1
                # Swim to Jecht
                elif checkpoint < 9 and memory.main.get_story_progress() >= 20:
                    checkpoint = 9
                # Towards Baaj temple
                elif checkpoint < 11 and memory.main.get_story_progress() >= 30:
                    checkpoint = 11

                # General pathing
                elif pathing.set_movement(AllStartsHere.execute(checkpoint)):
                    checkpoint += 1
                    logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.turn_ready():
                battle.boss.tanker()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                xbox.skip_stored_scene(3)


def after_ammes(tanker_sinscale_kill: bool, klikk_steals: int):
    memory.main.click_to_control()
    checkpoint = 0
    strats_calculated = False
    # memory.main.wait_frames(90)
    # logger.debug("MARK")
    # memory.main.ammes_fix(actor_index=0)
    # memory.main.wait_frames(90)

    while memory.main.get_map() != 49:

        if memory.main.get_story_progress() == 20 and not strats_calculated:
            strats = manip_planning.baaj_to_tros.plan_manips(klikk_steals=klikk_steals)
            strats_calculated = True

        if memory.main.user_control():
            start_pos = memory.main.get_coords()
            if int(start_pos[0]) in [866, 867, 868, 869, 870] and int(start_pos[1]) in [
                -138,
                -139,
                -140,
                -141,
            ]:
                logger.warning("Positioning error")
                FFXC.set_neutral()
                memory.main.wait_frames(20)
                memory.main.ammes_fix(actor_index=0)
                memory.main.wait_frames(20)
            else:
                # Map changes and events
                if checkpoint == 6:  # Save sphere
                    save_sphere.touch_and_go()
                    checkpoint += 1
                # Swim to Jecht
                elif checkpoint < 9 and memory.main.get_story_progress() >= 20:
                    checkpoint = 9
                # Towards Baaj temple
                elif checkpoint < 11 and memory.main.get_story_progress() >= 30:
                    checkpoint = 11

                # General pathing
                elif pathing.set_movement(AllStartsHere.execute(checkpoint)):
                    checkpoint += 1
                    logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.turn_ready():
                battle.boss.tanker(sinscale_kill=tanker_sinscale_kill)
            if memory.main.diag_skip_possible():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                xbox.skip_stored_scene(3)

    return strats


def swim_to_jecht():
    logger.info("Swimming to Jecht")

    FFXC.set_back()
    FFXC.set_movement(-1, -1)
    memory.main.wait_frames(30 * 8)
    while memory.main.user_control():
        FFXC.set_movement(-1, 1)

    FFXC.set_neutral()
    FFXC.release_back()
    logger.info("We've now reached Jecht.")
    xbox.skip_dialog(5)

    # Next, swim to Baaj temple
    memory.main.click_to_control()
    FFXC.set_movement(1, 0)
    memory.main.wait_frames(30 * 1)
    FFXC.set_movement(1, 1)
    memory.main.wait_frames(30 * 0.6)
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 5)
    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(30 * 1)
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 14)
    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(30 * 1.5)  # Line up with stairs

    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 3)

    while memory.main.get_map() == 48:
        pos = memory.main.get_coords()
        if pos[1] < 550:
            if pos[0] < -5:
                FFXC.set_movement(1, 1)
            elif pos[0] > 5:
                FFXC.set_movement(-1, 1)
            else:
                FFXC.set_movement(0, 1)
        else:
            if pos[1] > ((-1.00 * pos[0]) + 577.00):
                FFXC.set_movement(-1, 1)
            else:
                FFXC.set_movement(0, 1)

    FFXC.set_neutral()
    memory.main.wait_frames(30 * 0.3)
