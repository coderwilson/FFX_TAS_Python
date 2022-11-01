# Libraries and Core Files
import logging
import random
import sys

# This needs to be before the other imports in case they decide to log things when imported
import logger

# This sets up console and file logging (should only be called once)
logger.initialize_logging()

import area.baaj
import area.besaid
import area.boats
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
import logs
import memory.main
import nemesis.arena_battles
import nemesis.arenaPrep
import nemesis.changes
import reset
import screen
import vars
import xbox
from gamestate import game


def configuration_setup():
    game_vars = vars.vars_handle()
    # Open the config file and parse game configuration
    # This may overwrite configuration above
    config_data = config.open_config()
    # gamestate
    game.state = config_data.get("gamestate", "none")
    game.step = config_data.get("step_counter", 1)

    ############################################################################################
    # RNG - Using Rossy's FFX.exe fix, this allows us to choose the RNG seed we want. From 0-255
    game.rng_seed_num = config_data.get(
        "rngSeedNum", 160
    )  # If you don't randomly select below, this will be the seed you run.
    useFavoredSeed = config_data.get("useFavoredSeed", False)

    rngSelectArray = [31, 160]

    # TAS PB is on seed 31
    # 160 is WR for both categories, just has a bad start
    # Need review on the others
    ############################################################################################

    if game.state == "Luca" and game.step == 3:
        gameLength = "Testing Blitzball only"
    elif game.state != "none":  # Loading a save file, no RNG manip here
        game.rng_seed_num = 255
        gameLength = "Loading mid point for testing."
        # gameVars.setCSR(True)
    elif game_vars.use_set_seed():
        gameLength = f"Full Run, set seed [{game.rng_seed_num}]"
    elif useFavoredSeed:
        game.rng_seed_num = random.choice(rngSelectArray)
        gameLength = "Full Run, favored seed"
    # Full run starting from New Game, random seed
    else:
        game.rng_seed_num = random.choice(range(256))
        # Current WR is on seed 160 for both any% and CSR%
        gameLength = "Full Run, random seed"

    print("Game type will be:", gameLength)


def memory_setup():
    # Initiate memory reading, after we know the game is open.
    while not memory.main.start():
        pass

    # Main
    if memory.main.get_map not in [23, 348, 349]:
        reset.reset_to_main_menu()

    print("Game start screen")


def rng_seed_setup():
    game_vars = vars.vars_handle()
    # Using Rossy's FFX.exe fix, this allows us to choose the RNG seed we want. From 0-255
    if game_vars.use_set_seed():
        memory.main.set_rng_seed(game.rng_seed_num)

    rngSeed = memory.main.rng_seed()
    print("---RNG seed:", rngSeed)

    # Next, check if we are loading to a save file, or record the RNG seed on full runs.
    if game.state != "none":
        import load_game

        load_game.load_into_game(gamestate=game.state, step_counter=game.step)
    else:
        logs.next_stats(rngSeed)
        logs.write_stats("RNG seed:")
        logs.write_stats(rngSeed)


def perform_TAS():
    game_vars = vars.vars_handle()

    # Original seed for when looping
    rngSeedOrig = game.rng_seed_num
    blitzLoops = 0
    maxLoops = 12  # TODO: Move into config.yaml?

    while game.state != "End":

        try:
            # Blitzball testing logic
            if game.state == "Luca" and game.step == 3:
                area.dream_zan.new_game(game.state)
                load_game.load_save_num(37)  # TODO: Magic number

            if game.rng_seed_num >= 256:
                game.state = "End"

            # Start of the game, start of Dream Zanarkand section
            if game.state == "none" and game.step == 1:
                print("New Game 1 function initiated.")
                area.dream_zan.new_game(game.state)
                print("New Game 1 function complete.")
                game_vars.set_new_game()
                game_vars.set_csr(True)
                print("Variables initialized.")
                game.state = "DreamZan"
                game.step = 1

            if game.state == "DreamZan":
                if game.step == 1:
                    memory.main.wait_frames(30 * 0.5)
                    print("New Game 2 function initiated.")
                    area.dream_zan.new_game_2()
                    game.start_time = logs.time_stamp()
                    logs.write_stats("Start time:")
                    logs.write_stats(str(game.start_time))
                    print("Timer starts now.")
                    area.dream_zan.listen_story()
                    # game.state, game.step = reset.midRunReset()
                    # Start of the game, up through the start of Sinspawn Ammes fight
                    game.step = 2
                    area.dream_zan.ammes_battle()

                if game.step == 2:
                    battle.boss.ammes()
                    game.step = 3

                if game.step == 3:
                    area.dream_zan.after_ammes()
                    # Sin drops us near Baaj temple.
                    game.state = "Baaj"
                    game.step = 1

            if game.state == "Baaj":
                if game.step == 1:
                    print("Starting Baaj temple section")
                    area.baaj.entrance()
                    game.step = 2

                if game.step == 2:
                    area.baaj.baaj_puzzle()
                    game.step = 3

                if game.step == 3:
                    area.baaj.klikk_fight()
                    game.step = 4

                if game.step == 4:
                    # Klikk fight done. Now to wait for the Al Bhed ship.
                    print("Al Bhed boat part 1")
                    area.baaj.ab_boat_1()
                    game.step = 5

                if game.step == 5:
                    area.baaj.ab_swimming_1()
                    game.step = 6

                if game.step == 6:
                    print("Underwater Airship section")
                    area.baaj.ab_swimming_2()
                    game.state = "Besaid"
                    game.step = 1

            if game.state == "Besaid":
                if game.step == 1:
                    area.besaid.beach()
                    game.step = 2

                if game.step == 2:
                    area.besaid.trials()
                    game.step = 3

                if game.step == 3:
                    area.besaid.leaving()
                    game.state = "Boat1"
                    if memory.main.get_tidus_slvl() < 3:
                        print("=========================")
                        print("=== Under-levelled!!! ===")
                        print("=========================")
                        game.state, game.step = reset.mid_run_reset()
                    else:
                        game.step = 1

            if game.state == "Boat1":
                area.boats.ss_liki()
                area.kilika.arrival()
                game.state = "Kilika"

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
                    endTime = logs.time_stamp()
                    totalTime = endTime - game.start_time
                    print("Pre-Blitz time:", str(totalTime))
                    logs.write_stats("Pre Blitz time:")
                    logs.write_stats(totalTime)
                    game.step = 3

                if game.step == 3:
                    area.luca.blitz_start()
                    game.step = 4

                if game.step == 4:
                    print("------Blitz Start")
                    forceBlitzWin = game_vars.get_force_blitz_win()
                    blitz.blitz_main(forceBlitzWin)
                    print("------Blitz End")
                    if not game_vars.csr():
                        xbox.await_save()

                    if game_vars.loop_blitz() and blitzLoops < maxLoops:
                        FFXC.set_neutral()
                        print("-------------")
                        print("- Resetting -")
                        print("-------------")
                        screen.await_turn()
                        game.state, game.step = reset.mid_run_reset()
                        blitzLoops += 1
                    elif game_vars.blitz_loss_reset() and not game_vars.get_blitz_win():
                        FFXC.set_neutral()
                        print("------------------------------")
                        print("- Resetting - Lost Blitzball -")
                        print("------------------------------")
                        screen.await_turn()
                        game.state, game.step = reset.mid_run_reset()
                    else:
                        print("--------------")
                        print("- Post-Blitz -")
                        print("--------------")
                        game.step = 5

                if game.step == 5:
                    area.luca.after_blitz()
                    game.step = 1
                    game.state = "Miihen"

            # Just to make sure we set this variable somewhere.
            if game.state == "Miihen":
                if game.step == 1:
                    returnArray = area.miihen.arrival()
                    selfDestruct = area.miihen.arrival_2(
                        returnArray[0], returnArray[1], returnArray[2]
                    )
                    game.step = 2

                if game.step == 2:
                    area.miihen.mid_point()
                    print("End of Mi'ihen mid point section.")
                    area.miihen.low_road(returnArray[0], returnArray[1], returnArray[2])

                    # Report duration at the end of Mi'ihen section for all runs.
                    endTime = logs.time_stamp()
                    totalTime = endTime - game.start_time
                    print("Mi'ihen End timer is:", str(totalTime))
                    logs.write_stats("Miihen End time:")
                    logs.write_stats(totalTime)
                    game.state = "MRR"
                    game.step = 1

            if game.state == "MRR":
                if game.step == 1:
                    area.mrr.arrival()
                    area.mrr.main_path()
                    if memory.main.game_over():
                        game.state = "gameOverError"
                    game.step = 2

                if game.step == 2:
                    area.mrr.battle_site()
                    area.mrr.gui_and_aftermath()
                    endTime = logs.time_stamp()
                    totalTime = endTime - game.start_time
                    print("End of Battle Site timer is:", str(totalTime))
                    logs.write_stats("Djose-Start time:")
                    logs.write_stats(totalTime)
                    game.state = "Djose"
                    game.step = 1

            if game.state == "Djose":
                if game.step == 1:
                    area.djose.path()
                    game.step = 2

                if game.step == 2:
                    area.djose.temple()
                    area.djose.trials()
                    game.step = 3

                if game.step == 3:
                    area.djose.leaving_djose()
                    game.step = 1
                    game.state = "Moonflow"

            if game.state == "Moonflow":
                if game.step == 1:
                    area.moonflow.arrival()
                    area.moonflow.south_bank()
                    game.step = 2

                if game.step == 2:
                    area.moonflow.north_bank()
                    game.step = 1
                    game.state = "Guadosalam"

            if game.state == "Guadosalam":
                if game.step == 1:
                    area.guadosalam.arrival()
                    area.guadosalam.after_speech()
                    game.step = 2

                if game.step == 2:
                    area.guadosalam.guado_skip()
                    game.step = 1
                    game.state = "ThunderPlains"

            if game.state == "ThunderPlains":
                if game.step == 1:
                    status = area.thunder_plains.south_pathing()
                    game.step = 2

                if game.step == 2:
                    area.thunder_plains.agency()
                    game.step = 3

                if game.step == 3:
                    area.thunder_plains.north_pathing()
                    game.state = "Macalania"
                    game.step = 1

            if game.state == "Macalania":
                if game.step == 1:
                    area.mac_woods.arrival(False)
                    game.step = 2

                if game.step == 2:
                    area.mac_woods.lake_road()
                    area.mac_woods.lake_road_2()
                    game.step = 3

                if game.step == 3:
                    area.mac_woods.lake()
                    area.mac_temple.approach()
                    game.step = 4

                if game.step == 4:
                    area.mac_temple.arrival()
                    area.mac_temple.start_seymour_fight()
                    area.mac_temple.seymour_fight()
                    game.step = 5

                if game.step == 5:
                    area.mac_temple.trials()
                    game.step = 6

                if game.step == 6:
                    area.mac_temple.escape()
                    game.step = 7

                if game.step == 7:
                    area.mac_temple.under_lake()
                    game.step = 1
                    game.state = "Home"

            # Home section
            if game.state == "Home":
                if game.step == 1:
                    area.home.desert()
                    game.step = 2

                if game.step == 2:
                    area.home.find_summoners()
                    game.step = 1
                    game.state = "rescueYuna"

            # Rescuing Yuna
            if game.state == "rescueYuna":
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

                if game.step == 4:
                    area.rescue_yuna.evrae_altana()
                    game.step = 5

                if game.step == 5:
                    area.rescue_yuna.seymour_natus()
                    game.state = "Gagazet"
                    if game_vars.nemesis():
                        game.step = 10
                    else:
                        game.step = 1

            # Gagazet section
            if game.state == "Gagazet":
                if game.step == 1:
                    area.gagazet.calm_lands()
                    area.gagazet.defender_x()
                    import rng_track

                    advancePreX, advancePostX = rng_track.nea_track()
                    if advancePostX in [0, 1]:
                        game.step = 2
                    else:
                        game.step = 3

                if game.step == 2:
                    if game_vars.try_for_ne():
                        manipTime1 = logs.time_stamp()

                        print("Mark 1")
                        area.ne_armor.to_hidden_cave()
                        print("Mark 2")
                        area.ne_armor.drop_hunt()
                        print("Mark 3")
                        area.ne_armor.return_to_gagazet()
                        manipTime2 = logs.time_stamp()
                        try:
                            manipTime = manipTime2 - manipTime1
                            print("NEA Manip duration:", str(manipTime))
                            logs.write_stats("NEA Manip duration:")
                            logs.write_stats(manipTime)
                        except:
                            pass
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

                if game.step == 5:
                    area.gagazet.dream()
                    game.step = 6

                if game.step == 6:
                    area.gagazet.cave()
                    area.gagazet.wrap_up()
                    game.step = 1
                    game.state = "Zanarkand"

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

                if game.step == 4:
                    area.zanarkand.yunalesca()
                    game.step = 5

                if game.step == 5:
                    area.zanarkand.post_yunalesca()
                    game.step = 1
                    game.state = "Sin"

            # Sin section
            if game.state == "Sin":
                if game.step == 1:
                    area.sin.making_plans()
                    game.step = 2

                if game.step == 2:
                    print("Test 1")
                    area.sin.shedinja()
                    print("Test 2")
                    area.sin.facing_sin()
                    print("Test 3")
                    if game_vars.nemesis():
                        game.state = "Nem_Farm"
                        game.step = 1
                    else:
                        game.step = 3

            if game.state == "Sin":
                if game.step == 3:
                    area.sin.inside_sin()
                    game.step = 4

                if game.step == 4:
                    area.sin.egg_hunt()
                    if game_vars.nemesis():
                        battle.main.bfa_nem()
                    else:
                        battle.boss.bfa()
                        battle.boss.yu_yevon()
                    game.state = "End"

            # Nemesis logic only:
            if game.state == "Gagazet":
                if game.step == 10:
                    nemesis.changes.calm_lands_1()
                    game.step = 12

                if game.step == 11:
                    nemesis.changes.remiem_races()
                    game.step += 1

                if game.step == 12:
                    print("MAAAAARK")
                    memory.main.await_control()
                    nemesis.changes.arena_purchase()
                    area.gagazet.defender_x()
                    game.step = 2

            # Nemesis farming section
            if game.state == "Nem_Farm":
                if game.step == 1:
                    nemesis.arenaPrep.transition()
                    while not nemesis.arenaPrep.t_plains(cap_num=1):
                        pass
                    game.step = 2

                if game.step == 2:
                    while not nemesis.arenaPrep.calm(cap_num=1, airship_return=False):
                        pass
                    game.step = 3

                if game.step == 3:
                    nemesis.arenaPrep.kilika_shop()
                    game.step = 4

                if game.step == 4:
                    nemesis.arenaPrep.besaid_farm(cap_num=1)
                    game.step = 5

                if game.step == 5:
                    nemesis.arenaPrep.kilika_farm(cap_num=1)
                    game.step = 6

                if game.step == 6:
                    nemesis.arenaPrep.miihen_farm(cap_num=1)
                    game.step = 7

                if game.step == 7:
                    # reportGamestate()
                    # nemesis.arenaPrep.mrrFarm(capNum=1)
                    game.step = 8

                if game.step == 8:
                    nemesis.arenaPrep.od_to_ap()
                    game.step = 9

                if game.step == 9:
                    nemesis.arenaPrep.besaid_farm(cap_num=10)
                    game.step = 10

                if game.step == 10:
                    nemesis.arenaPrep.kilika_farm(cap_num=10)
                    game.step = 11

                if game.step == 11:
                    nemesis.arenaPrep.miihen_farm(cap_num=10)
                    game.step = 12

                if game.step == 12:
                    # reportGamestate()
                    # nemesis.arenaPrep.mrrFarm(capNum=10)
                    game.step = 13

                if game.step == 13:
                    nemesis.arenaPrep.djose_farm(cap_num=10)
                    game.step = 14

                if game.step == 15:
                    nemesis.arenaPrep.bikanel(cap_num=10)
                    game.step = 16

                if game.step == 16:
                    nemesis.arenaPrep.arena_return()
                    nemesis.arenaPrep.auto_phoenix()
                    game.step = 17

                if game.step == 17:
                    nemesis.arenaPrep.mac_woods(cap_num=10)
                    game.step = 18

                if game.step == 18:
                    nemesis.arenaPrep.stolen_fayth_cave()
                    game.step = 19

                if game.step == 19:
                    nemesis.arenaPrep.gagazet()
                    # nemesis.arenaPrep.gagazet1()
                    # nemesis.arenaPrep.gagazet2()
                    # nemesis.arenaPrep.gagazet3()
                    # game.state = "End" #Testing only
                    game.step = 20

                if game.step == 20:
                    nemesis.arenaPrep.calm(
                        cap_num=10, airship_return=False, force_levels=27
                    )
                    game.step = 21

                if game.step == 21:
                    nemesis.arenaPrep.one_mp_weapon()
                    game.step = 22

                if game.step == 22:
                    nemesis.arenaPrep.inside_sin(cap_num=10)
                    game.step = 23

                if game.step == 23:
                    nemesis.arenaPrep.unlock_omega()
                    nemesis.arenaPrep.omega_ruins()
                    game.step = 24

                if game.step == 24:
                    nemesis.arenaPrep.kilika_final_shop()
                    game.step = 25

                if game.step == 25:
                    nemesis.arenaPrep.arena_return()
                    nemesis.arenaPrep.final_weapon()
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

                if game.step == 7:
                    nemesis.arena_battles.return_to_sin()
                    game.state = "Sin"
                    game.step = 3

            # End of game section
            if (
                game.state == "End"
                and game_vars.loop_seeds()
                and game.rng_seed_num - rngSeedOrig < maxLoops
            ):
                # End of seed logic.
                game.state, game.step = reset.mid_run_reset(
                    land_run=True, start_time=game.start_time
                )

            print("------------------------------")
            print("Looping")
            print(f"{game.state} | {game.step}")
            print("------------------------------")

        except KeyboardInterrupt:
            print("Keyboard Interrupt - Exiting.")
            sys.exit(0)

    print("Time! The game is now over.")


def write_final_logs():
    if memory.main.get_story_progress() > 3210:
        endTime = logs.time_stamp()
        totalTime = endTime - game.start_time
        logs.write_stats("Total time:")
        logs.write_stats(str(totalTime))
        print("The game duration was:", str(totalTime))
        print("This duration is intended for internal comparisons only.")
        print("It is not comparable to non-TAS runs.")
        memory.main.wait_frames(30)
        print("--------")
        print("In order to conform to the speedrun.com/ffx ruleset,")
        memory.main.wait_frames(60)
        print("we now wait until the end of the credits and open")
        memory.main.wait_frames(60)
        print("the Load Game menu to show the last autosave.")

        while memory.main.get_map() != 23:
            if memory.main.get_map() in [348, 349]:
                xbox.tap_start()
            elif memory.main.cutscene_skip_possible():
                xbox.skip_scene()
        memory.main.wait_frames(180)
        while not memory.main.save_menu_open():
            xbox.tap_b()

    memory.main.end()

    print("Automation complete. Shutting down. Have a great day!")


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
    # if game.state != "none":
    #    load_game_state()

    # Run the TAS itself
    perform_TAS()

    # Finalize writing to logs
    write_final_logs()
