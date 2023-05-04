# Libraries and Core Files
import logging
import random
import sys
import argparse

# This needs to be before the other imports in case they decide to log things when imported
import log_init

# This sets up console and file logging (should only be called once)
log_init.initialize_logging()

logger = logging.getLogger(__name__)

import area.baaj
import area.besaid
import area.boats
import area.chocobos
import area.djose
import area.dream_zan
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

FFXC = xbox.controller_handle()


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
    args = parser.parse_args()
    
    # gamestate
    try:
        logger.warning(args)
        logger.info(f"Twitch states passed forward: {args.state}, {args.step}")
        if args.state != None or args.step != None:
            logger.warning(f"Loading in variables from Twitch, {args.state}, {args.step}")
            game.state = args.state
            game.step = int(args.step)
        else:
            game.state = config_data.get("gamestate", "none")
            game.step = config_data.get("step_counter", 1)
    except:
        logger.warning("Failure, could not load variables from Twitch")
        game.state = "VAR_ERROR"
        game.step = 999
    
    if args.seed != None:
        logger.debug(f"Seed passed from Twitch: {args.seed}")
        twitch_seed = int(args.seed)
        game_vars.rng_seed_num_set(twitch_seed)
        game_length = "Seed set via Twitch chat"
    elif game.state != "none":  # Loading a save file, no RNG manip here
        game_vars.rng_seed_num_set(255)
        game_length = "Loading mid point for testing."
    elif game_vars.rng_mode() == "set":
        game_length = f"Full Run, set seed: [{game_vars.rng_seed_num()}]"
    elif game_vars.rng_mode() == "preferred":
        game_vars.rng_seed_num_set(random.choice(game_vars.rng_preferred_array()))
        game_length = f"Full Run, favored seed: {game_vars.rng_seed_num()}"
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


def memory_setup():
    # Initiate memory reading, after we know the game is open.
    while not memory.main.start():
        pass

    # Main
    if memory.main.get_map not in [23, 348, 349]:
        reset.reset_to_main_menu()

    logger.info("Game start screen")


def rng_seed_setup():
    game_vars = vars.vars_handle()
    # Using Rossy's FFX.exe fix, this allows us to choose the RNG seed we want. From 0-255
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
    # loading from a save file
    load_game.load_into_game(gamestate=game.state, step_counter=game.step)
    game.start_time = logs.time_stamp()


def maybe_create_save(save_num: int):
    memory.main.wait_frames(6)
    game_vars = vars.vars_handle()
    if game_vars.create_saves():
        save_sphere.touch_and_save(
            save_num=save_num, game_state=game.state, step_count=game.step
        )

# Temporarily needed
def log_mrr_kimahri_crit_chance():
    crit_chance = memory.main.next_crit(character=3, char_luck=18, enemy_luck=15)
    logger.warning(f"Next Kimahri crit: {crit_chance}")
# end


def perform_TAS():
    game_vars = vars.vars_handle()

    # Original seed for when looping
    rng_seed_orig = game_vars.rng_seed_num()
    blitz_loops = 0
    max_loops = 12  # TODO: Move into config.yaml?

    while game.state != "End":
        try:
            if game_vars.rng_seed_num() >= 256:
                game.state = "End"

            # Start of the game, start of Dream Zanarkand section
            if game.state == "none" and game.step == 1:
                logger.info("New Game 1 function initiated.")
                area.dream_zan.new_game(game.state)
                logger.info("New Game 1 function complete.")
                game_vars.set_csr(True)
                logger.info("Variables initialized.")
                game.state = "DreamZan"
                game.step = 1

            if game.state == "DreamZan":
                if game.step == 1:
                    memory.main.wait_frames(30 * 0.5)
                    logger.info("New Game 2 function initiated.")

                    maybe_show_image(filename="images/laugh.jpg")

                    area.dream_zan.new_game_2()
                    game.start_time = logs.time_stamp()
                    logs.write_stats("Start time:")
                    logs.write_stats(str(game.start_time))
                    # reset reference timestamp so that log output is synced to run time
                    log_init.reset_logging_time_reference()
                    log_mrr_kimahri_crit_chance()  # Temp needed
                    logger.info("Timer starts now.")
                    area.dream_zan.listen_story()
                    # game.state, game.step = reset.mid_run_reset()
                    # Start of the game, up through the start of Sinspawn Ammes fight
                    area.dream_zan.ammes_battle()
                    game.step = 2

                if game.step == 2:
                    battle.boss.ammes()
                    game.step = 3

                if game.step == 3:
                    area.dream_zan.after_ammes()
                    # Sin drops us near Baaj temple.
                    game.state = "Baaj"
                    game.step = 1
                    maybe_create_save(save_num=20)

            if game.state == "Baaj":
                if game.step == 1:
                    logger.info("Starting Baaj temple section")
                    area.baaj.entrance()
                    game.step = 2

                if game.step == 2:
                    area.baaj.baaj_puzzle()
                    game.step = 3

                if game.step == 3:
                    area.baaj.klikk_fight()
                    game.step = 4
                    maybe_create_save(save_num=21)

                if game.step == 4:
                    # Klikk fight done. Now to wait for the Al Bhed ship.
                    logger.info("Al Bhed boat part 1")
                    area.baaj.ab_boat_1()
                    game.step = 5

                if game.step == 5:
                    area.baaj.ab_swimming_1()
                    game.step = 6

                if game.step == 6:
                    logger.info("Underwater Airship section")
                    area.baaj.ab_swimming_2()
                    game.state = "Besaid"
                    game.step = 1

            if game.state == "Besaid":
                if game.step == 1:
                    area.besaid.beach()
                    game.step = 2
                    # maybe_create_save(save_num=22)

                if game.step == 2:
                    area.besaid.trials()
                    game.step = 3

                if game.step == 3:
                    area.besaid.leaving()
                    game.state = "Boat1"
                    game.step = 1

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
                area.boats.ss_winno_2()
                game.state = "Luca"

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
                    maybe_create_save(save_num=24)

                if game.step == 3:
                    area.luca.blitz_start()
                    game.step = 4

                if game.step == 4:
                    logger.info("----- Blitz Start")
                    force_blitz_win = game_vars.get_force_blitz_win()
                    blitz.blitz_main(force_blitz_win)
                    logger.info("----- Blitz End")
                    if not game_vars.csr():
                        xbox.await_save()

                    if game_vars.loop_blitz() and blitz_loops < max_loops:
                        FFXC.set_neutral()
                        logger.info("-------------")
                        logger.info("- Resetting -")
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
                    maybe_create_save(save_num=25)

            # Just to make sure we set this variable somewhere.
            if game.state == "Miihen":
                if game.step == 1:
                    return_array = area.miihen.arrival()
                    area.miihen.arrival_2(
                        return_array[0], return_array[1], return_array[2]
                    )
                    area.miihen.mid_point()
                    logger.info("End of Mi'ihen mid point section.")
                    game.step = 2
                    maybe_create_save(save_num=26)

                if game.step == 2:
                    area.miihen.low_road(
                        return_array[0], return_array[1], return_array[2]
                    )

                    # Report duration at the end of Mi'ihen section for all runs.
                    end_time = logs.time_stamp()
                    total_time = end_time - game.start_time
                    logger.info(f"Mi'ihen End timer is: {total_time}")
                    logs.write_stats("Miihen End time:")
                    logs.write_stats(total_time)
                    game.state = "MRR"
                    game.step = 1

            if game.state == "MRR":
                if game.step == 1:
                    area.mrr.arrival()
                    game.step = 2
                    maybe_create_save(save_num=27)
                
                if game.step == 2:
                    area.mrr.main_path()
                    if memory.main.game_over():
                        game.state = "game_over_error"
                    game.step = 3
                    maybe_create_save(save_num=88)

                if game.step == 3:
                    area.mrr.battle_site()
                    area.mrr.gui_and_aftermath()
                    end_time = logs.time_stamp()
                    total_time = end_time - game.start_time
                    logger.info(f"End of Battle Site timer is: {total_time}")
                    logs.write_stats("Djose-Start time:")
                    logs.write_stats(total_time)
                    game.state = "Djose"
                    game.step = 1
                    maybe_create_save(save_num=28)

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
                        maybe_create_save(save_num=29)

                if game.step == 3:
                    area.djose.leaving_djose()
                    game.step = 1
                    game.state = "Moonflow"

            if game.state == "Moonflow":
                if game.step == 1:
                    area.moonflow.arrival()
                    area.moonflow.south_bank()
                    game.step = 2
                    maybe_create_save(save_num=30)

                if game.step == 2:
                    area.moonflow.north_bank()
                    game.step = 1
                    game.state = "Guadosalam"
                    if game_vars.create_saves():
                        while memory.main.get_map() != 243:
                            FFXC.set_movement(1, 1)
                        maybe_create_save(save_num=31)
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
                    # maybe_create_save(save_num=32)

                if game.step == 2:
                    area.guadosalam.guado_skip()
                    game.step = 1
                    game.state = "ThunderPlains"

            if game.state == "ThunderPlains":
                if game.step == 1:
                    area.thunder_plains.south_pathing()
                    game.step = 2
                    # maybe_create_save(save_num=33)

                if game.step == 2:
                    area.thunder_plains.agency()
                    game.step = 3

                if game.step == 3:
                    area.thunder_plains.north_pathing()
                    game.state = "Macalania"
                    game.step = 1
                    maybe_create_save(save_num=34)

            if game.state == "Macalania":
                if game.step == 1:
                    area.mac_woods.arrival(False)
                    game.step = 2
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
                    area.mac_temple.arrival()
                    area.mac_temple.start_seymour_fight()
                    area.mac_temple.seymour_fight()
                    game.step = 5

                if game.step == 5:
                    area.mac_temple.trials()
                    game.step = 6
                    maybe_create_save(save_num=37)

                if game.step == 6:
                    area.mac_temple.escape()
                    game.step = 7
                    maybe_create_save(save_num=38)

                if game.step == 7:
                    area.mac_temple.under_lake()
                    game.step = 1
                    game.state = "Home"
                    if game_vars.create_saves():
                        memory.main.click_to_control()
                        maybe_create_save(save_num=39)

            # Home section
            if game.state == "Home":
                if game.step == 1:
                    area.home.desert()
                    game.step = 2
                    maybe_create_save(save_num=40)

                if game.step == 2:
                    area.home.find_summoners()
                    game.step = 1
                    game.state = "rescue_yuna"
                    maybe_create_save(save_num=41)

            # Rescuing Yuna
            if game.state == "rescue_yuna":
                if game.step == 1:
                    area.rescue_yuna.pre_evrae()
                    battle.boss.evrae()
                    area.rescue_yuna.guards()
                    game.step = 2

                if game.step == 2:
                    area.rescue_yuna.trials()
                    area.rescue_yuna.trials_end()
                    game.step = 3

                if game.step == 3:
                    area.rescue_yuna.via_purifico()
                    game.step = 4
                    maybe_create_save(save_num=42)

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
                    if game_vars.create_saves():
                        FFXC.set_movement(0, -1)
                        memory.main.await_event()
                        FFXC.set_neutral()
                        memory.main.await_control()
                        maybe_create_save(save_num=44)
                        FFXC.set_movement(1, 1)
                        memory.main.await_event()
                        FFXC.set_neutral()

            # Gagazet section
            if game.state == "Gagazet":
                if game.step == 1:
                    area.gagazet.calm_lands()
                    area.gagazet.defender_x()
                    logger.debug("Determining next decision")

                    advance_pre_x, advance_post_x = rng_track.nea_track()
                    if advance_post_x in [0, 1]:
                        logger.info(f"Straight to NEA area: {advance_post_x}")
                        game.step = 2
                    else:
                        logger.info(f"B&Y battle before NEA: {advance_post_x}")
                        game.step = 3

                if game.step == 2:
                    if game_vars.try_for_ne():
                        manip_time_1 = logs.time_stamp()

                        logger.debug("Mark 1")
                        area.ne_armor.to_hidden_cave()
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
                    if game_vars.ne_armor() == 255:
                        area.ne_armor.loop_back_from_ronso()
                        game.step = 2
                    else:
                        area.gagazet.gagazet_gates()
                        game.step = 4

                if game.step == 4:
                    area.gagazet.flux()
                    game.step = 5
                    maybe_create_save(save_num=45)

                if game.step == 5:
                    area.gagazet.dream()
                    game.step = 6

                if game.step == 6:
                    area.gagazet.cave()
                    area.gagazet.wrap_up()
                    game.step = 1
                    game.state = "Zanarkand"
                    maybe_create_save(save_num=46)

            # Zanarkand section
            if game.state == "Zanarkand":
                if game.step == 1:
                    area.zanarkand.arrival()
                    game.step = 2

                if game.step == 2:
                    area.zanarkand.trials()
                    game.step = 3

                if game.step == 3:
                    area.zanarkand.sanctuary_keeper()
                    game.step = 4
                    maybe_create_save(save_num=47)

                if game.step == 4:
                    area.zanarkand.yunalesca()
                    game.step = 5

                if game.step == 5:
                    area.zanarkand.post_yunalesca()
                    game.step = 1
                    game.state = "Sin"
                    maybe_create_save(save_num=48)

            # Sin section
            if game.state == "Sin":
                if game.step == 1:
                    area.sin.making_plans()
                    game.step = 2
                    # maybe_create_save(save_num=49)

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
                    area.sin.inside_sin()
                    game.step = 4

                if game.step == 4:
                    area.sin.execute_egg_hunt()
                    if game_vars.nemesis():
                        battle.main.bfa_nem()
                    else:
                        battle.boss.bfa()
                        battle.boss.yu_yevon()
                    game.state = "End"
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

                    advance_pre_x, advance_post_x = rng_track.nea_track()
                    if advance_post_x in [0, 1]:
                        logger.info(f"Straight to NEA area: {advance_post_x}")
                        game.step = 2
                    else:
                        logger.info(f"B&Y battle before NEA: {advance_post_x}")
                        game.step = 3

            # Nemesis farming section
            if game.state == "Nem_Farm":
                if game.step == 1:
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
                    #nemesis.advanced_farm.full_farm(phase=7)
                    game.step = 9
                    maybe_create_save(save_num=58)

                if game.step == 9:
                    nemesis.arena_prep.kilika_money()
                    nemesis.arena_prep.arena_return()
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
                    maybe_create_save(save_num=62)

                if game.step == 13:
                    nemesis.arena_prep.kilika_final_shop()
                    nemesis.arena_prep.arena_return()
                    nemesis.arena_prep.final_weapon()
                    game.state = "Nem_Arena"
                    game.step = 1

            # Nemesis Arena section
            if game.state == "Nem_Arena":
                if game.step == 1:
                    nemesis.arena_battles.battles_1()
                    game_vars.print_arena_status()
                    game.step = 2

                if game.step == 2:
                    nemesis.arena_battles.battles_2()
                    game_vars.print_arena_status()
                    game.step = 3

                if game.step == 3:
                    nemesis.arena_battles.juggernaut_farm()
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


def write_final_logs():
    if memory.main.get_story_progress() > 3210:
        end_time = logs.time_stamp()
        total_time = end_time - game.start_time
        logs.write_stats("Total time:")
        logs.write_stats(str(total_time))
        logger.info(f"The game duration was: {str(total_time)}")
        logger.info("This duration is intended for internal comparisons only.")
        logger.info("It is not comparable to non-TAS runs.")
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
                xbox.skip_scene()
        memory.main.wait_frames(180)
        while not memory.main.save_menu_open():
            xbox.tap_b()

    logger.info("That's the end of the run, but we have one more thing to do.")
    memory.main.wait_frames(90)
    xbox.tap_a()
    memory.main.wait_frames(90)

    load_game.load_into_game(gamestate="Nem_Farm", step_counter=1)
    nemesis.arena_prep.return_to_airship()
    nemesis.arena_prep.air_ship_destination(dest_num=12)
    area.chocobos.all_races()
    # Use the following to go straight into remiem races.
    # while not pathing.set_movement([-637, -246]):
    #    pass
    area.chocobos.to_remiem()
    area.chocobos.remiem_races()

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
    perform_TAS()

    # Finalize writing to logs
    write_final_logs()
