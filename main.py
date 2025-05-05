# Libraries and Core Files
import logging
import random
import sys
import argparse

# This needs to be before the other imports in case they log things when imported
import log_init

import area.baaj
import area.besaid
import area.boats
import area.chocobos
import area.djose
import area.dream_zan
from area.dream_zan import split_timer
import area.gagazet
import area.guadosalam
import area.home
import area.kilika
import area.luca
import area.mac_temple
import area.mac_woods
import area.miihen
import area.moonflow
import area.mrr
from area.mrr_skip import skip_prep, attempt_skip, advance_to_aftermath
import area.ne_armor
import area.rescue_yuna
import area.sin
import area.thunder_plains
import area.zanarkand
import battle.boss
import battle.main
import blitz
import config
import load_game
import logs
import memory.main
import nemesis.advanced_farm
import nemesis.arena_battles
import nemesis.arena_prep
import nemesis.changes
import pathing
import reset
import rng_track
import save_sphere
import screen
import vars
import xbox
from gamestate import game
from image_to_text import maybe_show_image
from json_ai_files.write_seed_results import add_to_seed_results, check_ml_heals
from json_ai_files.update_leaderboard import new_leaderboard
from json_ai_files.write_seed import write_big_text, current_big_text

import manip_planning.rng
import manip_planning.ammes
import manip_planning.baaj_to_tros
from datetime import timedelta
import time

# This sets up console and file logging (should only be called once)
log_init.initialize_logging()
logger = logging.getLogger(__name__)

FFXC = xbox.controller_handle()

truerng = False
blitz_duration = None


def configuration_setup():
    game_vars = vars.vars_handle()
    # Open the config file and parse game configuration
    # This may overwrite configuration above
    config_data = config.open_config()

    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-seed")
    parser.add_argument("-state")
    parser.add_argument("-step")
    parser.add_argument("-train_blitz")
    parser.add_argument("-godrng")
    parser.add_argument("-story")
    parser.add_argument("-classic")
    parser.add_argument("-nemesis")
    args = parser.parse_args()

    global truerng

    # gamestate
    try:
        # logger.warning(args)
        logger.info(f"Twitch states passed forward: {args.state}, {args.step}")
        if args.state is not None or args.step is not None:
            logger.warning(
                f"Loading in variables from Twitch, {args.state}, {args.step}"
            )
            game.state = args.state
            game.step = int(args.step)
        else:
            game.state = config_data.get("gamestate", "none")
            game.step = config_data.get("step_counter", 1)
    except Exception:
        logger.warning("Failure, could not load variables from Twitch")
        game.state = "VAR_ERROR"
        game.step = 999

    #if args.train_blitz is not None:
    #    game_vars.set_loop_blitz(True)
    #    logger.warning("Training Blitzball, may reset after Blitzball wins.")
    if args.seed is not None:
        logger.debug(f"Seed passed from Twitch: {args.seed}")
        twitch_seed = int(args.seed)
        game_vars.rng_seed_num_set(twitch_seed)
        game_length = "Seed set via Twitch chat"
    if args.godrng is not None:
        game_vars.activate_god_rng()
    logger.warning(f"All args check: {args}")
    time.sleep(4)
    logger.warning(f"Story Mode check: {args.story}")
    if args.story == "True":
        logger.warning("Running in story mode!!!")
        write_big_text("New game, Story Mode")
        game_vars.activate_story_mode()
    elif args.classic == "True":
        logger.warning("Running classic speed run! (No CSR)")
        write_big_text("New game, Classic speedrun")
    elif args.nemesis == "True":
        logger.warning("Running Nemesis mode.")
        write_big_text("New game, Nemesis speedrun")
        game_vars.nemesis_set(True)
    else:
        logger.warning("Running a regular CSR speed run.")
        write_big_text("New game, CSR speedrun")
    if game.state != "none":  # Loading a save file, no RNG manip here
        write_big_text(current_big_text().replace("New game", "Load game"))
        game_vars.rng_seed_num_set(256)
        game_length = "Loading mid point for testing."
    elif game_vars.rng_mode() == "set":
        game_length = f"Full Run, set seed: [{game_vars.rng_seed_num()}]"
    elif game_vars.rng_mode() == "preferred":
        game_vars.rng_seed_num_set(random.choice(game_vars.rng_preferred_array()))
        game_length = f"Full Run, favored seed: {game_vars.rng_seed_num()}"
    elif game_vars.rng_mode()=="truerng":
        truerng = True
    # Full run starting from New Game, random seed
    else:
        game_vars.rng_seed_num_set(random.choice(range(256)))
        # Current WR is on seed 160 for both any% and CSR%
        game_length = f"Full Run, random seed: {game_vars.rng_seed_num()}"

    logger.info(f"Game type will be: {game_length}")
    if game_vars.get_battle_speedup():
        logger.warning(
            "THIS RUN IS USING AUTOMATIC 4X BATTLE SPEEDUP. ONLY USE FOR TESTING."
        )
    time.sleep(4)


def set_confirm_button():
    last_big_text = current_big_text()
    write_big_text("Checking controls")
    logger.manip("Now checking control scheme. Stand by.")
    game_vars = vars.vars_handle()

    last_click = "none"
    while not memory.main.save_menu_open():
        if memory.main.get_map() in [348, 349]:
            logger.debug("Skip idle screen (B)")
            xbox.tap_start()
            xbox.tap_back()
        if memory.main.save_menu_cursor() != 1:
            xbox.tap_down()
        elif last_click == "back":
            last_click = "confirm"
            xbox.tap_confirm()
        else:
            last_click = "back"
            xbox.tap_back()
        memory.main.wait_frames(90)
    
    if last_click == "back":
        logger.warning(f"Check: {game_vars.get_invert_confirm()}")
        logger.warning("A is confirm. Inverting TAS controls! (no user action needed)")
        game_vars.set_invert_confirm(not game_vars.get_invert_confirm())
        logger.warning(f"Check: {game_vars.get_invert_confirm()}")
    else:
        logger.warning("B is confirm. Controls set correctly. No TAS change.")
    
    while memory.main.save_menu_open():
        xbox.menu_a()
        xbox.menu_a()
        xbox.menu_a()
    write_big_text(last_big_text)
    


def memory_setup():
    # Initiate memory reading, after we know the game is open.
    while not memory.main.start():
        pass

    # Main
    if memory.main.get_map not in [23, 348, 349]:
        reset.reset_to_main_menu()
    
    set_confirm_button()

    logger.info("Game start screen")


def rng_seed_setup():
    game_vars = vars.vars_handle()
    # Using Rossy's FFX.exe fix,
    # this allows us to choose the RNG seed we want. From 0-255
    if game_vars.game_is_patched():
        memory.main.set_rng_seed(game_vars.rng_seed_num())

    rng_seed = memory.main.rng_seed()
    logger.info(f"RNG Seed: {rng_seed}")
    if game.state == "none":
        # record the RNG seed on full runs.
        logs.next_stats(rng_seed)
        logs.write_stats("RNG seed:")
        logs.write_stats(rng_seed)


def load_game_state():
    from json_ai_files.write_seed import write_state_step

    # loading from a save file
    write_state_step(state=game.state, step=game.step)
    load_game.load_into_game(gamestate=game.state, step_counter=game.step)
    game.start_time = logs.time_stamp()
    write_big_text("")


def maybe_create_save(save_num: int):
    FFXC.set_neutral()
    memory.main.await_control()
    memory.main.wait_frames(6)
    game_vars = vars.vars_handle()
    if game_vars.create_saves():
        save_sphere.touch_and_save(
            save_num=save_num, game_state=game.state, step_count=game.step
        )


def perform_TAS():
    # Force looping on Blitzball only.
    if game.state == "Luca" and game.step == 3:
        only_play_blitz = False  # Normally this would be True, but something bugged.
        logger.warning("Who's ready to play some Blitzball?")
    else:
        only_play_blitz = False

    game_vars = vars.vars_handle()
    results_mod = "not_set"
    use_heals = False
    blitz_duration = int(0)

    # Original seed for when looping
    rng_seed_orig = game_vars.rng_seed_num()
    blitz_loops = 0
    max_loops = 12  # TODO: Move into config.yaml?

    seed_found = False

    while game.state != "End":
        try:
            if not truerng:
                strats = manip_planning.baaj_to_tros.plan_manips(klikk_steals=0)
                klikk_steals, tanker_sinscale_kill = manip_planning.baaj_to_tros.plan_klikk_steals()
            # If not starting from dream zan, must first initialize strats variable.
            if game_vars.rng_seed_num() > 256:
                game.state = "End"

            # Start of the game, start of Dream Zanarkand section
            if game.state == "none" and game.step == 1:
                from json_ai_files.write_seed import write_new_game

                write_new_game(game_vars.rng_seed_num())
                game_vars.set_csr(True)
                if game_vars.story_mode():
                    game_vars.set_ml_heals(False)
                    results_mod = "story"
                    use_heals = False
                else:
                    try:
                        results_mod, use_heals = check_ml_heals(seed_num=game_vars.rng_seed_num())
                        logger.warning(f"Response check: {results_mod}, {use_heals}")

                        if use_heals:
                            game_vars.set_ml_heals(True)
                            logger.warning("Setting to use aVIna heal method!")
                        else:
                            game_vars.set_ml_heals(False)
                            logger.warning("No aVIna heal method. Set to heal always.")
                    except Exception as e:
                        logger.warning(f"Response check 2: {e}")
                        game_vars.set_ml_heals(False)
                        results_mod = "standard"
                logger.warning(f"Response check 3: {results_mod}, {use_heals}")
                game_vars.set_run_modifier(results_mod)
                logger.warning(f"Run modifier: {game_vars.run_modifier()}")

                logger.info("Variables initialized.")
                memory.main.wait_frames(60)
                logger.warning(f"Run type: {results_mod}")
                logger.info("New Game 1 function initiated.")
                area.dream_zan.new_game(game.state)
                logger.info("New Game 1 function complete.")
                game.state = "DreamZan"
                game.step = 1

            if game.state == "DreamZan":
                if game.step == 1:
                    #memory.main.wait_frames(15)
                    logger.info("New Game 2 function initiated.")

                    maybe_show_image(filename="images/laugh.jpg")

                    area.dream_zan.new_game_2()
                    game.start_time = logs.time_stamp()
                    logs.write_stats("Start time:")
                    logs.write_stats(str(game.start_time))
                    # reset reference timestamp so that log output is synced to run time
                    log_init.reset_logging_time_reference()
                    logger.info("Timer starts now.")
                    area.dream_zan.listen_story()

                    # Find rng seed from memory
                    rng_seed = manip_planning.rng.get_seed()
                    if rng_seed != "Err_seed_not_found":
                        game_vars.set_confirmed_seed(rng_seed)
                    else:
                        logging.error(f"Unable to derive seed")
                    seed_found = True

                    # Calculate manips for Sinscales and Ammes
                    tidus_sinspawn_attacks, tidus_potion, tidus_spiral_cut_turn = manip_planning.ammes.plan_ammes()
                    logger.debug(f"Tidus Sinspawn Attacks: {tidus_sinspawn_attacks}")
                    logger.debug(f"Tidus Potion: {tidus_potion}")
                    logger.debug(f"Spiral Cut Turn: {tidus_spiral_cut_turn}")

                    # game.state, game.step = reset.mid_run_reset()
                    # Start of the game, up through the start of Sinspawn Ammes fight
                    if truerng:
                        area.dream_zan.ammes_battle_classic()
                    else:
                        area.dream_zan.ammes_battle_crimson(tidus_total_attacks=tidus_sinspawn_attacks, tidus_potion=tidus_potion)
                    game.step = 2

                if game.step == 2:
                    if truerng:
                        battle.boss.ammes_classic()
                    else:
                        battle.boss.ammes_crimson(spiral_cut_turn=tidus_spiral_cut_turn)
                    game.step = 3

                if game.step == 3:
                    klikk_steals, tanker_sinscale_kill = manip_planning.baaj_to_tros.plan_klikk_steals()
                    logger.debug(f"Steals: {klikk_steals}")
                    logger.debug(f"Tanker Sinscale Kill: {tanker_sinscale_kill}")

                    if truerng:
                        area.dream_zan.after_ammes_classic()
                    else:
                        strats = area.dream_zan.after_ammes_crimson(tanker_sinscale_kill=tanker_sinscale_kill,
                                                            klikk_steals=klikk_steals)

                    # Sin drops us near Baaj temple.
                    game.state = "Baaj"
                    game.step = 1
                    maybe_create_save(save_num=20)

            if game.state == "Baaj":
                if game.step == 1:
                    logger.info("Starting Baaj temple section")
                    # klikk_steals = 4
                    # strats = manip_planning.baaj_to_tros.plan_manips(klikk_steals=klikk_steals)

                    if truerng:
                        area.baaj.entrance_classic()
                    else:
                        area.baaj.entrance_crimson(sahagin_b_first=strats["sahagin_b_first"], geos_potion=strats["geos_potion"],
                                           geos_attacks=strats["geos_attacks"])
                    game.step = 2

                if game.step == 2:
                    area.baaj.baaj_puzzle()
                    game.step = 3

                if game.step == 3:
                    if truerng:
                        area.baaj.klikk_fight_classic()
                    else:
                        area.baaj.klikk_fight_crimson(tidus_potion_klikk=strats["tidus_potion_klikk"],
                                              tidus_potion_turn=strats["tidus_potion_turn"],
                                              rikku_potion_klikk=strats["rikku_potion_klikk"],
                                              klikk_steals=klikk_steals)
                    game.step = 4
                    maybe_create_save(save_num=21)

                if game.step == 4:
                    # Klikk fight done. Now to wait for the Al Bhed ship.
                    logger.info("Al Bhed boat part 1")
                    area.baaj.ab_boat_1()
                    game.step = 5

                if game.step == 5:
                    if truerng:
                        area.baaj.ab_swimming_1_classic()
                    else:
                        rikku_attacks_left = area.baaj.ab_swimming_1_crimson(chain_encounter_strat=strats["chain_encounter_strat"])
                    game.step = 6

                if game.step == 6:
                    logger.info("Underwater Airship section")
                    if truerng:
                        area.baaj.ab_swimming_2_classic()
                    else:
                        area.baaj.ab_swimming_2_crimson(ruins_encounter_strat=strats["ruins_encounter_strat"])
                    game.state = "Besaid"
                    game.step = 1

            if game.state == "Besaid":
                if game.step == 1:
                    area.besaid.beach(lagoon_strats=strats["lagoon_strats"])
                    game.step = 2
                    #maybe_create_save(save_num=22)

                if game.step == 2:
                    area.besaid.trials()
                    game.step = 3
                    maybe_create_save(save_num=22)

                if game.step == 3:
                    kim_success = area.besaid.leaving()
                    if kim_success:
                        game.state = "Boat1"
                        game.step = 1
                    else:
                        #game.state, game.step = reset.mid_run_reset()
                        reset.reset_to_main_menu()
                        area.dream_zan.new_game(gamestate="reload_autosave")
                        load_game.load_save_num(0)
                        # Do not change game.state or game.step. Will restart this section.

            if game.state == "Boat1":
                area.boats.ss_liki()
                area.kilika.arrival()
                game.state = "Kilika"
                maybe_create_save(save_num=23)

            if game.state == "Kilika":
                if game.step == 1:
                    area.kilika.forest_1()
                    game.step = 3

                if game.step == 3:
                    area.kilika.trials()
                    area.kilika.trials_end()
                    game.step = 4

                if game.step == 4:
                    area.kilika.forest_3()
                    game.step = 5

                if game.step == 5:
                    game.step = 1
                    game.state = "Boat2"

            if game.state == "Boat2":
                area.boats.ss_winno()
                game.state = "Boat3"

            if game.state == "Boat3":
                if game_vars.story_mode():
                    area.boats.ss_winno_2_story()
                else:
                    area.boats.ss_winno_2()
                game.state = "Luca"
                maybe_create_save(save_num=24)

            if game.state == "Luca":
                if game.step == 1:
                    area.luca.arrival()
                    game.step = 2

                if game.step == 2:
                    end_time = logs.time_stamp()
                    total_time = end_time - game.start_time
                    logger.info(f"Pre-Blitz time: {total_time}")
                    logs.write_stats("Pre Blitz time:")
                    logs.write_stats(total_time)
                    game.step = 3
                    maybe_create_save(save_num=25)

                if game.step == 3:
                    area.luca.blitz_start()
                    game.step = 4

                if game.step == 4:
                    blitz_threshold = 410
                    logger.info("----- Blitz Start")
                    force_blitz_win = game_vars.get_force_blitz_win()
                    blitz_duration = blitz.blitz_main(force_blitz_win)
                    logger.info("----- Blitz End")
                    if not game_vars.csr():
                        xbox.await_save()

                    if only_play_blitz:
                        logger.info("------------------------")
                        logger.info("- Need more Blitzball! -")
                        logger.info("------------------------")
                        game.state, game.step = reset.mid_run_reset()
                        load_game.load_into_game(gamestate="Luca", step_counter=3)
                        game.step = 3
                        game.state = "Luca"

                    elif game_vars.loop_blitz() and blitz_duration < blitz_threshold:
                        logger.manip("--------------")
                        logger.manip(
                            "Good Blitz, worth completing. Duration in seconds:"
                        )
                        logger.manip(blitz_duration)
                        logger.manip("--------------")
                        game.step = 5
                    elif game_vars.loop_blitz() and blitz_loops < max_loops:
                        FFXC.set_neutral()
                        logger.info("-------------")
                        logger.info(
                            "- Resetting: Blitz time: {blitz_duration} seconds."
                        )
                        logger.info("-------------")
                        screen.await_turn()
                        game.state, game.step = reset.mid_run_reset()
                        blitz_loops += 1
                    elif game_vars.blitz_loss_reset() and not game_vars.get_blitz_win():
                        FFXC.set_neutral()
                        logger.info("------------------------------")
                        logger.info("- Resetting - Lost Blitzball -")
                        logger.info("------------------------------")
                        screen.await_turn()
                        game.state, game.step = reset.mid_run_reset()
                    else:
                        logger.info("--------------")
                        logger.info("- Post-Blitz -")
                        logger.info("--------------")
                        game.step = 5

                if game.step == 5:
                    area.luca.after_blitz()
                    game.step = 1
                    game.state = "Miihen"
                    maybe_create_save(save_num=26)

            # Just to make sure we set this variable somewhere.
            if game.state == "Miihen":
                return_array = [False, 0, False, False]
                if game.step == 1:
                    return_array = area.miihen.arrival()
                    if return_array[2] is False:
                        game.state, game.step = reset.mid_run_reset()
                    else:
                        game.step = 2
                        
                if game.step == 2:
                    return_array = area.miihen.arrival_2(
                        return_array[0], return_array[1]
                    )
                    if return_array[2] is False:
                        game.state, game.step = reset.mid_run_reset()
                    else:
                        split_timer()
                        area.miihen.mid_point()
                        logger.info("End of Mi'ihen mid point section.")
                        game.step = 3
                        maybe_create_save(save_num=27)

                if game.step == 3:
                    if not area.miihen.low_road(return_array[0], return_array[1]):
                        reset.reset_to_main_menu()
                        area.dream_zan.new_game(gamestate="reload_autosave")
                        load_game.load_save_num(0)
                    else:
                        # Report duration at the end of Mi'ihen section for all runs.
                        split_timer()
                        end_time = logs.time_stamp()
                        total_time = end_time - game.start_time
                        logger.info(f"Mi'ihen End timer is: {total_time}")
                        logs.write_stats("Miihen End time:")
                        logs.write_stats(total_time)
                        game.state = "MRR"
                        game.step = 1

            if game.state == "MRR":
                if game.step == 1:
                    if area.mrr.arrival() == 1:  # Perform section before Terra skip attempt.
                        if game_vars.story_mode():
                            game.step = 12
                            game_vars.mrr_skip_set(False)
                        elif not game_vars.csr():
                            game_vars.mrr_skip_set(True)
                            #skip_prep()
                            if attempt_skip():  # i.e. if this step is successful
                                if advance_to_aftermath():  # i.e. if this step is successful
                                    game.step = 4  # There is no 3 since Terra Skip found.
                                else:
                                    reset.reset_to_main_menu()
                                    area.dream_zan.new_game(gamestate="reload_autosave")
                                    load_game.load_save_num(0)
                                    # Do not change game.state or game.step. Will restart this section.
                        
                        else:
                            game_vars.mrr_skip_set(True)
                            game.step = 2
                    else:
                        reset.reset_to_main_menu()
                        area.dream_zan.new_game(gamestate="reload_autosave")
                        load_game.load_save_num(0)
                        # Do not change game.state or game.step. Will restart this section.
                        
                if game.step == 2:
                    # These three steps are all performed on the same map.
                    # i.e. they reload to the same autosave.
                    skip_prep()
                    if attempt_skip():  # i.e. if this step is successful
                        if advance_to_aftermath():  # i.e. if this step is successful
                            game.step = 4  # There is no 3 since Terra Skip found.
                    
                    # Cathall for all the Else statements
                    if game.step == 2:
                        reset.reset_to_main_menu()
                        area.dream_zan.new_game(gamestate="reload_autosave")
                        load_game.load_save_num(0)
                        # Do not change game.state or game.step. Will restart this section.

                    '''
                    if result == 1:
                        game.step = 4
                    elif result == 2:
                        game.state, game.step = reset.mid_run_reset()
                    else:
                        game.step = 2
                        maybe_create_save(save_num=27)
                    '''

                if game.step == 12:
                    # Formerly step 2, this was the section leading up to battle site.
                    area.mrr.main_path()
                    if memory.main.game_over():
                        game.state = "game_over_error"
                    game.step = 13
                    maybe_create_save(save_num=28)

                if game.step == 13:
                    # Formerly step 3, this was the entire battle site logic.
                    area.mrr.battle_site()
                    game.step = 4

                if game.step == 4:
                    area.mrr.aftermath()
                    end_time = logs.time_stamp()
                    total_time = end_time - game.start_time
                    logger.info(f"End of Battle Site timer is: {total_time}")
                    logs.write_stats("Djose-Start time:")
                    logs.write_stats(total_time)
                    game.state = "Djose"
                    game.step = 1
                    maybe_create_save(save_num=29)

            if game.state == "Djose":
                if game.step == 1:
                    area.djose.path()
                    game.step = 2

                if game.step == 2:
                    area.djose.temple()
                    area.djose.trials()
                    game.step = 3
                    if game_vars.create_saves():
                        while not pathing.set_movement([66, -227]):
                            pass
                        maybe_create_save(save_num=30)

                if game.step == 3:
                    area.djose.leaving_djose()
                    game.step = 1
                    game.state = "Moonflow"

            if game.state == "Moonflow":
                if game.step == 1:
                    area.moonflow.arrival()
                    split_timer()
                    area.moonflow.south_bank()
                    game.step = 2
                    maybe_create_save(save_num=31)

                if game.step == 2:
                    area.moonflow.north_bank()
                    game.step = 1
                    game.state = "Guadosalam"
                    if game_vars.create_saves():
                        logger.warning("Special logic to save the game in Guadosalam!")
                        memory.main.click_to_control_3()
                        while memory.main.get_map() != 243:
                            FFXC.set_movement(1, 1)
                        FFXC.set_neutral()
                        memory.main.await_control()
                        maybe_create_save(save_num=32)
                        while memory.main.get_map() != 135:
                            FFXC.set_movement(1, -1)
                        FFXC.set_neutral()
                        memory.main.wait_frames(1)
                        memory.main.await_control()

            if game.state == "Guadosalam":
                if game.step == 1:
                    area.guadosalam.arrival()
                    area.guadosalam.after_speech()
                    game.step = 2

                if game.step == 2:
                    area.guadosalam.guado_skip()
                    split_timer()
                    game.step = 1
                    game.state = "ThunderPlains"

            if game.state == "ThunderPlains":
                if game.step == 1:
                    plains_battles = area.thunder_plains.south_pathing()
                    if plains_battles == 999:
                        #game.state, game.step = reset.mid_run_reset()
                        reset.reset_to_main_menu()
                        area.dream_zan.new_game(gamestate="reload_autosave")
                        load_game.load_save_num(0)
                        # Do not change game.state or game.step. Will restart this section.
                    else:
                        game.step = 2
                        # maybe_create_save(save_num=33)

                if game.step == 2:
                    area.thunder_plains.agency()
                    game.step = 3

                if game.step == 3:
                    result = area.thunder_plains.north_pathing(plains_battles)
                    if result:
                        game.state = "Macalania"
                        game.step = 1
                        maybe_create_save(save_num=34)
                    else:
                        #game.state, game.step = reset.mid_run_reset()
                        reset.reset_to_main_menu()
                        area.dream_zan.new_game(gamestate="reload_autosave")
                        load_game.load_save_num(0)
                        # Do not change game.state or game.step. Will restart this section.

            if game.state == "Macalania":
                if game.step == 1:
                    if area.mac_woods.arrival(False):
                        # Successful completion of this area.
                        game.step = 2
                    else:
                        reset.reset_to_main_menu()
                        area.dream_zan.new_game(gamestate="reload_autosave")
                        load_game.load_save_num(0)
                        # Do not change game.state or game.step. Will restart this section.
                    maybe_create_save(save_num=35)

                if game.step == 2:
                    area.mac_woods.lake_road()
                    area.mac_woods.lake_road_2()
                    game.step = 3

                if game.step == 3:
                    area.mac_woods.lake()
                    area.mac_temple.approach()
                    game.step = 4
                    maybe_create_save(save_num=36)

                if game.step == 4:
                    if memory.main.get_map() != 80:
                        area.mac_temple.arrival()
                    area.mac_temple.start_seymour_fight()
                    if area.mac_temple.seymour_fight():
                        game.step = 5
                    else:
                        reset.reset_to_main_menu()
                        area.dream_zan.new_game(gamestate="reload_autosave")
                        load_game.load_save_num(0)
                        # Do not change game.state or game.step. Will restart this section.

                if game.step == 5:
                    area.mac_temple.trials()
                    game.step = 6
                    maybe_create_save(save_num=37)

                if game.step == 6:
                    area.mac_temple.escape()
                    game.step = 7

                if game.step == 7:
                    if area.mac_temple.attempt_wendigo():
                        game.step = 8
                        maybe_create_save(save_num=38)
                    else:
                        reset.reset_to_main_menu()
                        area.dream_zan.new_game(gamestate="reload_autosave")
                        load_game.load_save_num(0)
                        # Do not change game.state or game.step. Will restart this section.

                if game.step == 8:
                    area.mac_temple.under_lake()
                    game.step = 1
                    game.state = "Home"
                    if game_vars.create_saves():
                        memory.main.click_to_control()
                        maybe_create_save(save_num=39)

            # Home section
            if game.state == "Home":
                if game.step == 1:
                    if area.home.desert():
                        game.step = 2
                        maybe_create_save(save_num=40)
                    else:
                        reset.reset_to_main_menu()
                        area.dream_zan.new_game(gamestate="reload_autosave")
                        load_game.load_save_num(0)
                        # Do not change game.state or game.step. Will restart this section.

                if game.step == 2:
                    area.home.find_summoners()
                    game.step = 1
                    game.state = "rescue_yuna"
                    maybe_create_save(save_num=41)

            # Rescuing Yuna
            if game.state == "rescue_yuna":
                if game.step == 1:
                    area.rescue_yuna.pre_evrae()
                    if battle.boss.evrae():
                        area.rescue_yuna.guards()
                        game.step = 2
                    else:
                        reset.reset_to_main_menu()
                        area.dream_zan.new_game(gamestate="reload_autosave")
                        load_game.load_save_num(0)
                        # Do not change game.state or game.step. Will restart this section.

                if game.step == 2:
                    area.rescue_yuna.trials()
                    area.rescue_yuna.trials_end()
                    game.step = 3

                if game.step == 3:
                    if area.rescue_yuna.via_purifico():
                        game.step = 4
                        maybe_create_save(save_num=42)
                    else:
                        reset.reset_to_main_menu()
                        area.dream_zan.new_game(gamestate="reload_autosave")
                        load_game.load_save_num(0)
                        # Do not change game.state or game.step. Will restart this section.

                if game.step == 4:
                    area.rescue_yuna.evrae_altana()
                    game.step = 5
                    maybe_create_save(save_num=43)

                if game.step == 5:
                    area.rescue_yuna.seymour_natus()
                    game.state = "Gagazet"
                    if game_vars.nemesis():
                        game.step = 10
                    else:
                        game.step = 1
                    game.step = 1
                    if game_vars.create_saves():
                        maybe_create_save(save_num=44)
                        '''
                        FFXC.set_movement(0, -1)
                        memory.main.await_event()
                        FFXC.set_neutral()
                        memory.main.await_control()
                        maybe_create_save(save_num=44)
                        FFXC.set_movement(1, 1)
                        memory.main.await_event()
                        FFXC.set_neutral()
                        '''

            # Gagazet section
            if game.state == "Gagazet":
                if game.step == 1:
                    area.gagazet.calm_lands()
                    if game_vars.nemesis():
                            nemesis.changes.arena_npc()
                            nemesis.changes.arena_purchase()
                            area.gagazet.calm_lands(checkpoint=9)
                    area.gagazet.defender_x()
                    logger.debug("Determining next decision")

                    if game_vars.get_nea_after_bny() or game_vars.get_nea_ignore():
                        game.step = 3
                    else:
                        game.step = 2
                        # Something about final_nea_check is not working.
                        
                        #success,direct = rng_track.final_nea_check()
                        #_,indirect = rng_track.final_nea_check(with_ronso=True)
                        #if success and direct <= indirect:
                        #    game.step = 2
                        #else:
                        #    game.step = 3

                if game.step == 2:
                    #nea_possible_check, _ = rng_track.final_nea_check()
                    #if nea_possible_check:  #game_vars.try_for_ne() and nea_possible_check:
                    #if game_vars.get_nea_after_bny():
                    manip_time_1 = logs.time_stamp()
                    area.ne_armor.next_green(report=True)

                    logger.debug("Mark 1")
                    if area.ne_armor.to_hidden_cave():
                        logger.debug("Mark 2")
                        area.ne_armor.drop_hunt()
                    logger.debug("Mark 3")
                    area.ne_armor.return_to_gagazet()
                    manip_time_2 = logs.time_stamp()
                    try:
                        manip_time = manip_time_2 - manip_time_1
                        logger.info(f"NEA Manip duration: {str(manip_time)}")
                        logs.write_stats("NEA Manip duration:")
                        logs.write_stats(manip_time)
                    except Exception as e:
                        logger.warning(e)
                    game.step = 3

                if game.step == 3:
                    area.gagazet.to_the_ronso()
                    drop_check,_ = rng_track.final_nea_check()
                    logger.warning(f"NE Armor check main: {game_vars.ne_armor()}")
                    logger.warning(f"  NEA can drop main: {drop_check}")
                    if game_vars.get_nea_ignore():
                        area.gagazet.to_the_ronso(checkpoint=6)
                        game.step = 4
                    elif game_vars.get_nea_after_bny() and game_vars.ne_armor() == 255:
                        area.ne_armor.loop_back_from_ronso()
                        game.step = 2
                    else:
                        area.gagazet.to_the_ronso(checkpoint=6)
                        game.step = 4
                    # maybe_create_save(save_num=45) # Placeholder.
                    # This save is used for immediately before climbing Gagazet.
                    # However, it does not properly save automatically.
                    # Must be created manually.

                if game.step == 4:
                    area.gagazet.gagazet_climb()
                    game.step = 5
                
                if game.step == 5:
                    if area.gagazet.flux():
                        game.step = 6
                        maybe_create_save(save_num=46)
                    else:
                        reset.reset_to_main_menu()
                        area.dream_zan.new_game(gamestate="reload_autosave")
                        load_game.load_save_num(0)
                        # Do not change game.state or game.step. Will restart this section.

                if game.step == 6:
                    area.gagazet.dream()
                    game.step = 7

                if game.step == 7:
                    area.gagazet.cave()
                    area.gagazet.wrap_up()
                    game.step = 1
                    game.state = "Zanarkand"
                    maybe_create_save(save_num=47)
                
                if game.step == 10:
                    nemesis.changes.calm_lands_1()
                    success,direct = rng_track.final_nea_check()
                    _,indirect = rng_track.final_nea_check(with_ronso=True)
                    if success and direct <= indirect:
                        game.step = 2
                    else:
                        game.step = 3

            # Zanarkand section
            if game.state == "Zanarkand":
                if game.step == 1:
                    area.zanarkand.arrival()
                    game.step = 2

                if game.step == 2:
                    area.zanarkand.dome_interior()
                    game.step = 3

                if game.step == 3:
                    area.zanarkand.trials()
                    game.step = 4

                if game.step == 4:
                    if area.zanarkand.sanctuary_keeper():
                        area.zanarkand.yunalesca_prep()
                        game.step = 5
                        maybe_create_save(save_num=48)
                    else:
                        reset.reset_to_main_menu()
                        area.dream_zan.new_game(gamestate="reload_autosave")
                        load_game.load_save_num(0)
                        game.step = 2
                        # Do not change game.state or game.step. Will restart this section.

                if game.step == 5:
                    if area.zanarkand.yunalesca():
                        game.step = 6
                    else:
                        reset.reset_to_main_menu()
                        area.dream_zan.new_game(gamestate="reload_autosave")
                        load_game.load_save_num(0)
                        # Do not change game.state or game.step. Will restart this section.
                        #game.state, game.step = reset.mid_run_reset()

                if game.step == 6:
                    area.zanarkand.post_yunalesca()
                    game.step = 1
                    game.state = "Sin"
                    maybe_create_save(save_num=49)

            # Sin section
            if game.state == "Sin":
                if game.step == 1:
                    area.sin.making_plans()
                    game.step = 2

                if game.step == 2:
                    logger.debug("Test 1")
                    area.sin.shedinja()
                    logger.debug("Test 2")
                    area.sin.facing_sin()
                    logger.debug("Test 3")
                    if game_vars.nemesis():
                        game.state = "Nem_Farm"
                        game.step = 1
                    else:
                        game.step = 3
                    maybe_create_save(save_num=50)

                if game.step == 3:
                    # Up to and including Seymour Omnis
                    if area.sin.inside_sin(checkpoint=0):
                        game.step = 4
                    else:
                        # Seymour fail/death
                        reset.reset_to_main_menu()
                        area.dream_zan.new_game(gamestate="reload_autosave")
                        load_game.load_save_num(0)
                
                if game.step == 4:
                    # After Seymour Omnis
                    area.sin.inside_sin(checkpoint=41)
                    game.step = 5

                if game.step == 5:
                    area.sin.execute_egg_hunt()
                    final_battle = True
                    if game_vars.nemesis():
                        final_battle = battle.main.bfa_nem()
                    else:
                        final_battle = battle.boss.bfa()
                        if final_battle:
                            battle.boss.yu_yevon()
                    if final_battle:
                        game.state = "End"
                    else:
                        game.state, game.step = reset.mid_run_reset()
                    logger.debug(f"State: {game.state}")
                    logger.debug(f"Step: {game.step}")

            # Nemesis logic only:
            if game.state == "Gagazet":
                if game.step == 10:
                    nemesis.changes.calm_lands_1()
                    game.step = 12

                if game.step == 11:
                    nemesis.changes.remiem_races()
                    game.step += 1

                if game.step == 12:
                    memory.main.await_control()
                    nemesis.changes.arena_purchase()
                    area.gagazet.defender_x()
                    logger.debug("Determining next decision")

                    extra_drops, _ = rng_track.nea_track()
                    if extra_drops in [0, 1]:
                        logger.info(f"Straight to NEA area: {extra_drops}")
                        game.step = 2
                    else:
                        logger.info(f"B&Y battle before NEA: {extra_drops}")
                        game.step = 3

            # Nemesis farming section
            if game.state == "Nem_Farm":
                if game.step == 1:
                    #nemesis.arena_prep.Macalania_pass(approach="family")  # Performed later.
                    nemesis.arena_prep.transition()
                    nemesis.arena_prep.unlock_omega()
                    while not nemesis.arena_prep.t_plains(cap_num=1):
                        pass
                    while not nemesis.arena_prep.calm(cap_num=1, airship_return=False):
                        pass
                    # maybe_create_save(save_num=51)
                    game.step = 2

                if game.step == 2:
                    nemesis.arena_prep.kilika_shop()
                    logger.debug("===Kilika shop to farm")
                    nemesis.arena_prep.kilika_farm(cap_num=1, checkpoint=3)
                    nemesis.arena_prep.besaid_farm(cap_num=1)
                    game.step = 3
                    maybe_create_save(save_num=52)

                if game.step == 3:
                    nemesis.arena_prep.mac_woods(cap_num=1)
                    nemesis.arena_prep.stolen_fayth_cave(cap_num=1)
                    game.step = 4
                    maybe_create_save(save_num=53)

                if game.step == 4:
                    nemesis.arena_prep.od_to_ap()
                    game.step = 5
                    maybe_create_save(save_num=54)

                if game.step == 5:
                    nemesis.arena_prep.besaid_farm(cap_num=10)
                    nemesis.arena_prep.kilika_farm(cap_num=10)
                    game.step = 6
                    maybe_create_save(save_num=55)

                if game.step == 6:
                    nemesis.advanced_farm.full_farm(phase=3)
                    game.step = 7
                    maybe_create_save(save_num=56)

                if game.step == 7:
                    nemesis.arena_prep.auto_phoenix()
                    logger.debug("Auto_phoenix done.")
                    game.step = 8
                    maybe_create_save(save_num=57)

                if game.step == 8:
                    nemesis.advanced_farm.full_farm(phase=4)
                    # nemesis.advanced_farm.full_farm(phase=7)
                    game.step = 9
                    maybe_create_save(save_num=58)

                if game.step == 9:
                    nemesis.arena_prep.kilika_money()
                    nemesis.arena_prep.arena_return()
                    nemesis.arena_prep.lv1_bribe()
                    nemesis.arena_prep.quick_levels(force_levels=27, mon="don_tonberry")
                    nemesis.arena_prep.one_mp_weapon()
                    # Phase 5 farm
                    game.step = 10
                    maybe_create_save(save_num=59)

                if game.step == 10:
                    nemesis.advanced_farm.full_farm(phase=5)
                    # Back to arena for auto-life and auto-haste
                    game.step = 11
                    maybe_create_save(save_num=60)

                if game.step == 11:
                    nemesis.arena_prep.gagazet()
                    game.step = 12
                    maybe_create_save(save_num=61)

                if game.step == 12:
                    nemesis.advanced_farm.full_farm(phase=6)
                    game.step = 13
                    nemesis.arena_prep.split_timer()
                    maybe_create_save(save_num=62)

                if game.step == 13:
                    nemesis.arena_prep.final_push_updates(stage=0)
                    area.chocobos.all_races()
                    area.chocobos.to_remiem()
                    area.chocobos.remiem_races()
                    nemesis.arena_prep.final_push_updates(stage=1)
                    area.chocobos.leave_temple()
                    nemesis.arena_prep.Macalania_pass(approach="family")
                    nemesis.arena_prep.final_push_updates(stage=2)
                    #nemesis.arena_prep.Macalania_pass(approach="Wantz")
                    area.chocobos.sun_sigil(godhand=0, baaj=0)
                    nemesis.arena_prep.final_push_updates(stage=3)
                    area.chocobos.upgrade_celestials(godhand=0, baaj=0, Tidus_only=True)
                    game.step = 14
                    maybe_create_save(save_num=63)

                if game.step == 14:
                    nemesis.arena_prep.final_push_updates(stage=4)
                    nemesis.arena_prep.final_armor()
                    nemesis.arena_prep.final_push_updates(stage=5)
                    logger.info("Nemesis Prep is complete. Ready to start battles. (1)")
                    nemesis.arena_prep.split_timer()

                    game.state = "Nem_Arena"
                    game.step = 1

            # Nemesis Arena section
            if game.state == "Nem_Arena":
                if game.step == 1:
                    logger.info("Nemesis Prep is complete. Ready to start battles. (2)")
                    nemesis.arena_battles.battles_1()
                    game_vars.print_arena_status()
                    game.step = 2

                if game.step == 2:
                    nemesis.arena_battles.juggernaut_farm()
                    game_vars.print_arena_status()
                    game.step = 3

                if game.step == 3:
                    nemesis.arena_battles.battles_2()
                    game_vars.print_arena_status()
                    game.step = 4

                if game.step == 4:
                    nemesis.arena_battles.battles_3()
                    game_vars.print_arena_status()
                    game.step = 5

                if game.step == 5:
                    nemesis.arena_battles.battles_4()
                    game_vars.print_arena_status()
                    game.step = 6

                if game.step == 6:
                    nemesis.arena_battles.nemesis_battle()
                    game.step = 7
                    maybe_create_save(save_num=63)
                    nemesis.arena_prep.split_timer()

                if game.step == 7:
                    nemesis.arena_battles.return_to_sin()
                    game.state = "Sin"
                    game.step = 3

            # End of game section
            if (
                game.state == "End"
                and game_vars.loop_seeds()
                and game_vars.rng_seed_num() - rng_seed_orig < max_loops
            ):
                # End of seed logic.
                game.state, game.step = reset.mid_run_reset(
                    land_run=True, start_time=game.start_time
                )
            logger.debug("Looping")
            logger.debug(f"{game.state} | {game.step}")

        except KeyboardInterrupt as e:
            logger.info("Keyboard Interrupt - Exiting.")
            logging.exception(e)
            sys.exit(0)

    logger.info("Time! The game is now over.")

    if memory.main.get_story_progress() > 3210:
        end_time = logs.time_stamp()
        total_time = end_time - game.start_time
        bcount = game_vars.ne_extra_battles()
        logs.write_stats("Total time:")
        logs.write_stats(str(total_time))
        logger.info(f"The game duration was: {str(total_time)}")
        logger.info("This duration is intended for internal comparisons only.")
        logger.info("It is not comparable to non-TAS runs.")
        try:
            adj_time = total_time - timedelta(seconds=blitz_duration)
            logger.debug(f"Time checks: {total_time} | {blitz_duration} | {adj_time}")
            if (
                blitz_duration != None and
                not truerng and
                not game_vars.nemesis() and
                not game_vars.story_mode() and
                game_vars.csr() == True
            ):
                if game_vars.get_blitz_win():
                    logger.debug(f"Writing seed results to memory: {adj_time}")
                    add_to_seed_results(
                        seed=game_vars.rng_seed_num(), 
                        modifier=game_vars.run_modifier(),
                        avina_heals=str(game_vars.ml_heals()),
                        raw=str(total_time),
                        blitz=str(blitz_duration),
                        adjusted=str(adj_time),
                        bcount=str(bcount)
                    )
                else:
                    logger.debug(f"Do not write seed results to memory for Blitz loss.")
                write_big_text(f"ADJ TIME: {adj_time}")
            else:
                logger.info(f"Identified run started as a test, no results to confirm.")
        except Exception as e:
            logger.warning(f"Error calculating results: {e}")
        
        # Update leaderboard
        new_leaderboard()

        memory.main.wait_frames(30)
        logger.info("--------")
        logger.info("In order to conform to the speedrun.com/ffx ruleset,")
        memory.main.wait_frames(60)
        logger.info("we now wait until the end of the credits and open")
        memory.main.wait_frames(60)
        logger.info("the Load Game menu to show the last autosave.")

        while memory.main.get_map() != 23:
            if memory.main.get_map() in [348, 349]:
                xbox.tap_start()
            elif memory.main.cutscene_skip_possible():
                memory.main.wait_seconds(251)
                xbox.skip_scene()
                memory.main.wait_seconds(2)
        write_big_text("")
        memory.main.wait_frames(180)
        while not memory.main.save_menu_open():
            xbox.tap_b()

    logger.info("That's the end of the run, but we have one more thing to do.")
    memory.main.wait_frames(90)
    xbox.tap_a()
    game_vars.deactivate_story_mode()
    memory.main.wait_frames(90)

    import z_choco_races_test

    memory.main.end()
    logger.info("Automation complete. Shutting down. Have a great day!")


# Main entry point of TAS
if __name__ == "__main__":
    # Load up vars.py
    vars.init_vars()

    # Set up gamestate and rng-related variables
    configuration_setup()

    # Initialize memory access
    memory_setup()

    # Initialize rng seed and patch (if applicable)
    rng_seed_setup()

    # Next, check if we are loading to a save file
    if game.state != "none":
        load_game_state()

    # Run the TAS itself
    # game.state = "Baaj"
    # game.step = 1
    perform_TAS()
