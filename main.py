# Libraries and Core Files
import random
import sys

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
import reset
import screen
import vars
import xbox
from game import get_gamestate

def variables_setup():
    vars.init_vars()
    game_vars = vars.vars_handle()
    game_vars.set_start_vars()

    # Speedrun sectional files
    if game_vars.nemesis():
        import nemesis.arena_battles
        import nemesis.arenaPrep
        import nemesis.changes

# List below is kept as a reference, use config.yaml instead

# Gamestate, "none" for new game, or set to a specific section to start from the first save.
# See the if statement tree below to determine starting position for Gamestate.
# These are only here for reference, set the value in config.yaml!

# These are the popular ones.
# Gamestate = "none"
# step_counter = 1  # NEW GAME!
# Gamestate = "Baaj"
# step_counter = 1 # x40 Baaj temple, before Geos boss
# step_counter = 4 # x100 Al Bhed boat before Tros
# Gamestate = "Besaid"
# step_counter = 1 # x111 Before first viewing Besaid beach
# step_counter = 2 # x6 Crusader's hut before trials
# step_counter = 3 # x39 Crusader's hut after trials
# Gamestate = "Boat1"
# step_counter = 1 # 31 NOT WORKING
# Gamestate = "Kilika"
# step_counter = 1 # x22
# Gamestate = "Luca"
# step_counter = 1 # x112 Boat lands, first movement
# step_counter = 3 # Blitzball only, do not use
# step_counter = 5 # x5 between Blitz and swimmers/Garuda REMAKE THIS SAVE
# Gamestate = "Miihen"
# step_counter = 1 # x16 with laughing scene, 26 after laughing scene
# step_counter = 2 # x28 (Agency before Chocobo Eater)
# Gamestate = "MRR"
# step_counter = 1 # x38, includes a low-gil fix
# Gamestate = "Djose"
# step_counter = 1 # x27
# Gamestate = "Moonflow"
# step_counter = 2 # x2 After Extractor
# Gamestate = "Guadosalam"
# step_counter = 2 # x3 before Guadosalam Skip
# Gamestate = "Macalania"
# step_counter = 1 # x9
# step_counter = 2 # x7
# step_counter = 4 # x10 Seymour
# step_counter = 6 # x4 Before escape sequence - RE-CHECK SPHERE GRID
# Gamestate = "Home"
# step_counter = 1 # x60
# step_counter = 2 # x11
# Gamestate = "rescueYuna"
# step_counter = 1 # x56 First save chance on airship, before any movement.
# step_counter = 2 # x15
# step_counter = 4 # x30 Altana (any%) / x12 Altana (nemesis)
# step_counter = 5 # x42 regular, 67 nemesis
# Gamestate = "Gagazet"
# step_counter = 1 # x43
# step_counter = 3 # x138 After B&Y
# step_counter = 6 # x98 After Flux/Dream. Can select version 3 or 4 below.
# step_counter = 10 # Nemesis variant, blitz win logic (not working)
# step_counter = 11 # Remiem racing
# Gamestate = "Zanarkand"
# step_counter = 1 # x99 Campfire
# step_counter = 4 # x44 Before Yunalesca
# step_counter = 5 # x48 After Yunalesca any%, x13 for Nemesis
# Gamestate = "Sin"
# step_counter = 2 # x70 Shedinja Highbridge
# step_counter = 3 # x50 Start of Sea of Sorrows
# step_counter = 4 # x51 Before point of no return, with zombiestrike weapons (not Kimahri)

# Nemesis load testing
# Gamestate = "Nem_Farm"
# step_counter = 1 # x14 Inside Sin, right at start of the branching logic.
# step_counter = 13 # x17 Just before Djose farm
# step_counter = 14 #Just before Thunder Plains farm
# step_counter = 16 #Just before Bikanel farm
# step_counter = 18 #Just before Fayth Cave farm
# step_counter = 19 #Gagazet farm
# step_counter = 20 #After Gagazet, before Calm Lands farm
# step_counter = 22 #Before Sin/Omega farms, AFTER picking up oneMP weapon
# step_counter = 24 #Final Prep before arena bosses

def configuration_setup():
    game_vars = vars.vars_handle()
    game = get_gamestate()
    # Open the config file and parse game configuration
    # This may overwrite configuration above
    config_data = config.open_config()
    # Gamestate
    game.state = config_data.get("Gamestate", "none")
    game.step = config_data.get("step_counter", 1)

    ############################################################################################
    # RNG - Using Rossy's FFX.exe fix, this allows us to choose the RNG seed we want. From 0-255
    forceBlitzWin = config_data.get("forceBlitzWin", False)
    seedHunt = config_data.get("seedHunt", False) # Update this to decide new seed or known seed
    game.rng_seed_num = config_data.get("rngSeedNum", 160) # If you don't randomly select below, this will be the seed you run.
    useFavoredSeed = config_data.get("useFavoredSeed", False)

    rngSelectArray = [31, 160]
    maybeGoodSeeds = [2, 31, 142, 157, 160, 172, 177, 182, 183, 200, 224, 254]
    rtaGoodSeeds = [160, 142, 34, 62, 210, 31, 159]
    favoriteSeedsSoFar = [31, 160]
    # TAS PB is on seed 31
    # 160 is WR for both categories, just has a bad start
    # Need review on the others
    ############################################################################################

    # Set these to False by default. Overwritten below in some cases.
    blitzTesting = False
    rngReviewOnly = False

    if game.state == "Luca" and game.step == 3:
        blitzTesting = True
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
    maxLoops = 12

    # Other variables
    rngSeedOrig = game.rng_seed_num
    specialZanLoad = False


# Main functions
def report_gamestate():
    screen.clear_mouse(0)


def memory_setup():
    # Initiate memory reading, after we know the game is open.
    while not memory.main.start():
        pass

    # Main
    report_gamestate()
    if memory.main.get_map in [23, 348, 349]:
        pass
    else:
        reset.reset_to_main_menu()

    print("Game start screen")
    screen.clear_mouse(0)


def rng_seed_setup():
    game_vars = vars.vars_handle()
    # Using Rossy's FFX.exe fix, this allows us to choose the RNG seed we want. From 0-255
    if game_vars.use_set_seed():
        memory.main.set_rng_seed(game.rng_seed_num)

    rngSeed = memory.main.rng_seed()
    print("---RNG seed:", rngSeed)
    logs.next_stats(rngSeed)
    logs.write_stats("RNG seed:")
    logs.write_stats(rngSeed)


def load_game_state():
    game = get_gamestate()
    game_vars = vars.vars_handle()
    # Plug in controller
    FFXC = xbox.controller_handle()

    if not (game.state == "Luca" and game.step == 3):
        area.dream_zan.new_game(game.state)
        game.start_time = logs.time_stamp()
        logs.write_stats("Start time:")
        logs.write_stats(str(game.start_time))
        report_gamestate()
    import load_game

    # Need to update these to use loadGame.loadSaveNum(number) for all.

    if game.state == "Baaj" and game.step == 1:
        load_game.load_save_num(40)
    if game.state == "Baaj" and game.step == 4:
        load_game.load_save_num(100)
    # Save pop-up after falling off of Rikkus boat
    if game.state == "Besaid" and game.step == 1:
        load_game.load_save_num(111)
    # Save pop-up after falling off of Rikkus boat
    if game.state == "Besaid" and game.step == 2:
        load_game.load_save_num(6)
        load_game.besaid_trials()
    # Crusader's lodge after "Enough, Wakka!"
    if game.state == "Besaid" and game.step == 3:
        load_game.load_save_num(39)
        print("Load complete")
        while memory.main.user_control():
            if memory.main.get_coords()[0] > 0.5:
                FFXC.set_movement(1, 1)
            else:
                FFXC.set_movement(0, 1)
        print("Ready for regular path")
    # Besaid beach before boarding SS Liki ( nice alliteration :D )
    if game.state == "Boat1":
        load_game.load_save_num(31)
        load_game.boat_1()
    if game.state == "Kilika" and game.step == 1:  # Just after entering the woods
        load_game.load_save_num(22)
    if game.state == "Luca" and game.step == 1:  # Approaching Luca via boat
        load_game.load_save_num(112)
    if game.state == "Luca" and game.step == 5:
        load_game.load_save_num(5)
    if game.state == "Miihen" and game.step == 1:  # After the talk with Auron
        load_game.load_save_num(16)  # With laughing scene
        load_game.load_miihen_start_laugh()
    if game.state == "Miihen" and game.step == 2:  # Agency
        load_game.load_save_num(28)
        returnArray = [False, 0, 0, False]
    if game.state == "MRR" and game.step == 1:  # Mi'ihen North after meeting Seymour
        load_game.load_save_num(38)
        memory.main.set_gil_value(4000)  # Fixes a low gil state for this save file.
        load_game.load_mrr()
    # Aftermath, after talking to Seymour and then Auron
    if game.state == "Djose" and game.step == 1:
        load_game.load_save_num(27)
        load_game.after_gui()
    if game.state == "Moonflow" and game.step == 2:  # North bank, before Rikku
        load_game.load_save_num(2)
        load_game.moonflow_2()
    if game.state == "Guadosalam" and game.step == 2:  # After the Farplane
        load_game.load_save_num(3)
        load_game.load_guado_skip()
    if game.state == "Macalania" and game.step == 1:  # 1 = south, 2 = north
        load_game.load_save_num(1)
    if game.state == "Macalania" and game.step == 2:  # 1 = south, 2 = north
        load_game.load_save_num(1)
    if game.state == "Macalania" and game.step == 4:  # Right before Jyscal skip
        load_game.load_save_num(190)
        load_game.load_mac_temple()
        import menu

        menu.equip_weapon(character=0, special="brotherhood")
        menu.mac_temple()
    # Outside temple, before escaping.
    if game.state == "Macalania" and game.step == 6:
        load_game.load_save_num(4)
    if game.state == "Home" and game.step == 1:
        load_game.load_save_num(60)
    if game.state == "Home" and game.step == 2:
        load_game.load_save_num(11)
    if game.state == "rescueYuna" and game.step == 1:  # Airship, first movement.
        # Blitz Win, save less speed/power spheres
        load_game.load_save_num(56)
    if game.state == "rescueYuna" and game.step == 2:  # Bevelle trials
        load_game.load_save_num(15)
    if game.state == "rescueYuna" and game.step == 4:  # Altana
        load_game.load_save_num(12)
        # memory.main.setEncounterRate(setVal=0)
        # memory.main.setGameSpeed(setVal=1)
    # Highbridge before Seymour Natus
    if game.state == "rescueYuna" and game.step == 5:
        load_game.load_save_num(42)  # Regular
        # loadGame.loadSaveNum(67) #Nemesis
    if game.state == "Gagazet" and game.step == 1:  # Just before Calm Lands
        load_game.load_save_num(43)
        load_game.load_calm()
        game_vars.set_blitz_win(True)
    if game.state == "Gagazet" and game.step == 2:  # NE armor save
        load_game.load_save_num(57)
    if game.state == "Gagazet" and game.step == 3:  # Gagazet gates, after B&Y
        load_game.load_save_num(138)  # Blitz Win
        # loadGame.loadSaveNum(53) # Blitz Loss
        game_vars.end_game_version_set(4)
        load_game.load_gagazet_gates()
    if game.state == "Gagazet" and game.step == 6:  # After the dream
        load_game.load_save_num(98)
        game_vars.end_game_version_set(4)
        load_game.load_gagazet_dream()
        game_vars.flux_overkill_success()
    if game.state == "Gagazet" and game.step == 10:  # Calm Lands, but Nemesis version
        load_game.load_save_num(43)
        load_game.load_calm()
    if game.state == "Gagazet" and game.step == 11:  # Calm Lands, but Nemesis version
        load_game.load_save_num(64)
        FFXC.set_movement(1, 0)
        memory.main.wait_frames(60)
        FFXC.set_movement(0, 1)
        memory.main.wait_frames(60)
        FFXC.set_neutral()
        import menu

        menu.prep_calm_lands()
    if game.state == "Zanarkand" and game.step == 1:  # Intro scene revisited
        load_game.load_save_num(99)
        game_vars.end_game_version_set(1)
        game_vars.flux_overkill_success()
        game_vars.end_game_version_set(4)
    if game.state == "Zanarkand" and game.step == 2:  # Just before the trials.
        load_game.load_offset(35)
        load_game.zan_trials()
        game_vars.end_game_version_set(4)
    if game.state == "Zanarkand" and game.step == 3:  # After trials, before boss
        load_game.load_save_num(45)
        game_vars.end_game_version_set(4)
    if game.state == "Zanarkand" and game.step == 4:  # After Sanctuary Keeper
        load_game.load_save_num(44)
        game_vars.end_game_version_set(4)
    if game.state == "Zanarkand" and game.step == 5:  # After Yunalesca
        load_game.load_save_num(13)
        specialZanLoad = True
    # Save sphere on the Highbridge before talking to Shedinja
    if game.state == "Sin" and game.step == 2:
        # loadGame.loadSaveNum(49)
        # Nemesis logic, double friend sphere drops from B&Y
        load_game.load_save_num(70)
        while not memory.main.oaka_gil_cursor() in [8, 20]:
            if memory.main.user_control():
                import pathing

                pathing.set_movement([-251, 340])
            else:
                FFXC.set_neutral()
            xbox.menu_b()
        memory.main.check_nea_armor()
    if game.state == "Sin" and game.step == 3:  # Start of "Sea of Sorrows" section
        load_game.load_save_num(50)
    if game.state == "Sin" and game.step == 4:  # Before point of no return
        # This save has zombiestrike weapons for all except Kimahri
        # Please use for egg hunt and zombie weapon testing.
        load_game.load_save_num(51)
        game_vars.set_zombie(5)
        load_game.load_egg_hunt()

    # Nemesis run loads
    if game.state == "Nem_Farm" and game.step == 1:
        load_game.load_save_num(14)
    if game.state == "Nem_Farm" and game.step == 2:
        load_game.load_save_num(69)
    if game.state == "Nem_Farm" and game.step == 3:
        load_game.load_save_num(84)
        game_vars.set_nem_checkpoint_ap(3)  # See nemesis.menu
        # import nemesis.arenaPrep
        nemesis.arenaPrep.arena_return()
    if game.state == "Nem_Farm" and game.step == 5:
        load_game.load_save_num(71)
    if game.state == "Nem_Farm" and game.step == 6:
        load_game.load_save_num(72)
        game_vars.set_nem_checkpoint_ap(2)  # See nemesis.menu
    if game.state == "Nem_Farm" and game.step == 8:
        load_game.load_save_num(73)
    if game.state == "Nem_Farm" and game.step == 9:
        load_game.load_save_num(75)
        game_vars.set_nem_checkpoint_ap(3)  # See nemesis.menu
    if game.state == "Nem_Farm" and game.step == 13:
        load_game.load_save_num(17)
        game_vars.set_nem_checkpoint_ap(7)  # See nemesis.menu
    if game.state == "Nem_Farm" and game.step == 14:
        load_game.load_save_num(76)
        game_vars.set_nem_checkpoint_ap(10)  # See nemesis.menu
    if game.state == "Nem_Farm" and game.step == 16:
        load_game.load_save_num(113)
        game_vars.set_nem_checkpoint_ap(12)  # See nemesis.menu
    if game.state == "Nem_Farm" and game.step == 17:
        load_game.load_save_num(111)
        game_vars.set_nem_checkpoint_ap(14)  # See nemesis.menu
    if game.state == "Nem_Farm" and game.step == 18:
        load_game.load_save_num(114)
        game_vars.set_nem_checkpoint_ap(15)  # See nemesis.menu
    if game.state == "Nem_Farm" and game.step == 19:  # Gagazet
        load_game.load_save_num(115)
        game_vars.set_nem_checkpoint_ap(19)  # See nemesis.menu
    if game.state == "Nem_Farm" and game.step == 21:
        load_game.load_save_num(79)
        nemesis.arenaPrep.arena_return()
        game_vars.set_nem_checkpoint_ap(27)  # See nemesis.menu
    if game.state == "Nem_Farm" and game.step == 22:
        load_game.load_save_num(82)
        # import nemesis.menu
        # nemesis.menu.rikkuHaste()
        game_vars.set_nem_checkpoint_ap(24)  # See nemesis.menu
    if game.state == "Nem_Farm" and game.step == 23:
        load_game.load_save_num(80)
        game_vars.set_nem_checkpoint_ap(30)  # See nemesis.menu
    if game.state == "Nem_Farm" and game.step == 24:
        load_game.load_save_num(81)
        game_vars.set_nem_checkpoint_ap(30)
        game_vars.set_nem_checkpoint_ap(30)  # See nemesis.menu
    if game.state == "Nem_Farm" and game.step == 20:
        load_game.load_save_num(85)
        game_vars.set_nem_checkpoint_ap(30)
    if game.state == "Nem_Farm":
        memory.main.check_nea_armor()
    memory.main.check_nea_armor()


def perform_TAS():
    game = get_gamestate()
    game_vars = vars.vars_handle()

    rikkuCharged = 0
    blitzLoops = 0

    while game.state != "End":

        try:
            # Blitzball testing logic
            if game.state == "Luca" and game.step == 3:
                area.dream_zan.new_game(game.state)
                load_game.load_save_num(37)

            if game.rng_seed_num >= 256:
                game.state = "End"

            # Start of the game, start of Dream Zanarkand section
            if game.state == "none" and game.step == 1:
                report_gamestate()
                print("New Game 1 function initiated.")
                area.dream_zan.new_game(game.state)
                print("New Game 1 function complete.")
                game_vars.set_new_game()
                game_vars.set_csr(True)
                print("Variables initialized.")
                game.state = "DreamZan"
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

            if game.state == "DreamZan" and game.step == 2:
                report_gamestate()
                battle.boss.ammes()
                game.step = 3
                report_gamestate()

            if game.state == "DreamZan" and game.step == 3:
                area.dream_zan.after_ammes()
                # Sin drops us near Baaj temple.
                game.state = "Baaj"
                game.step = 1

            if game.state == "Baaj" and game.step == 1:
                report_gamestate()
                print("Starting Baaj temple section")
                area.baaj.entrance()
                game.step = 2

            if game.state == "Baaj" and game.step == 2:
                report_gamestate()
                area.baaj.baaj_puzzle()
                game.step = 3

            if game.state == "Baaj" and game.step == 3:
                area.baaj.klikk_fight()
                game.step = 4
                report_gamestate()

            if game.state == "Baaj" and game.step == 4:
                # Klikk fight done. Now to wait for the Al Bhed ship.
                print("Al Bhed boat part 1")
                area.baaj.ab_boat_1()
                game.step = 5

            if game.state == "Baaj" and game.step == 5:
                report_gamestate()
                area.baaj.ab_swimming_1()
                game.step = 6
                report_gamestate()

            if game.state == "Baaj" and game.step == 6:
                print("Underwater Airship section")
                area.baaj.ab_swimming_2()
                game.state = "Besaid"
                game.step = 1
                report_gamestate()

            if game.state == "Besaid" and game.step == 1:
                report_gamestate()
                area.besaid.beach()
                game.step = 2
                report_gamestate()

            if game.state == "Besaid" and game.step == 2:
                area.besaid.trials()
                game.step = 3
                report_gamestate()

            if game.state == "Besaid" and game.step == 3:
                area.besaid.leaving()
                game.state = "Boat1"
                if memory.main.get_tidus_slvl() < 3:
                    print("=========================")
                    print("=== Under-levelled!!! ===")
                    print("=========================")
                    game.state, game.step = reset.mid_run_reset()
                else:
                    game.step = 1
                    report_gamestate()

            if game.state == "Boat1":
                report_gamestate()
                area.boats.ss_liki()
                area.kilika.arrival()
                game.state = "Kilika"

            if game.state == "Kilika" and game.step == 1:
                report_gamestate()
                area.kilika.forest_1()
                report_gamestate()
                game.step = 3

            if game.state == "Kilika" and game.step == 3:
                report_gamestate()
                area.kilika.trials()
                area.kilika.trials_end()
                game.step = 4

            if game.state == "Kilika" and game.step == 4:
                report_gamestate()
                area.kilika.forest_3()
                game.step = 5

            if game.state == "Kilika" and game.step == 5:
                report_gamestate()
                game.step = 1
                game.state = "Boat2"

            if game.state == "Boat2":
                report_gamestate()
                area.boats.ss_winno()
                game.state = "Boat3"

            if game.state == "Boat3":
                report_gamestate()
                area.boats.ss_winno_2()
                game.state = "Luca"

            if game.state == "Luca" and game.step == 1:
                report_gamestate()
                area.luca.arrival()
                game.step = 2

            if game.state == "Luca" and game.step == 2:
                report_gamestate()
                endTime = logs.time_stamp()
                totalTime = endTime - game.start_time
                print("Pre-Blitz time:", str(totalTime))
                logs.write_stats("Pre Blitz time:")
                logs.write_stats(totalTime)
                game.step = 3

            if game.state == "Luca" and game.step == 3:
                report_gamestate()
                area.luca.blitz_start()
                game.step = 4

            if game.state == "Luca" and game.step == 4:
                report_gamestate()
                print("------Blitz Start")
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

            if game.state == "Luca" and game.step == 5:
                report_gamestate()
                area.luca.after_blitz()
                game.step = 1
                game.state = "Miihen"

            # Just to make sure we set this variable somewhere.
            if game.state == "Miihen" and game.step == 1:
                report_gamestate()
                returnArray = area.miihen.arrival()
                selfDestruct = area.miihen.arrival_2(
                    returnArray[0], returnArray[1], returnArray[2]
                )
                game.step = 2

            if game.state == "Miihen" and game.step == 2:
                report_gamestate()
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

            if game.state == "MRR" and game.step == 1:
                report_gamestate()
                area.mrr.arrival()
                area.mrr.main_path()
                if memory.main.game_over():
                    game.state = "gameOverError"
                game.step = 2

            if game.state == "MRR" and game.step == 2:
                report_gamestate()
                area.mrr.battle_site()
                area.mrr.gui_and_aftermath()
                endTime = logs.time_stamp()
                totalTime = endTime - game.start_time
                print("End of Battle Site timer is:", str(totalTime))
                logs.write_stats("Djose-Start time:")
                logs.write_stats(totalTime)
                game.state = "Djose"
                game.step = 1

            if game.state == "Djose" and game.step == 1:
                report_gamestate()
                area.djose.path()
                game.step = 2

            if game.state == "Djose" and game.step == 2:
                report_gamestate()
                area.djose.temple()
                area.djose.trials()
                game.step = 3

            if game.state == "Djose" and game.step == 3:
                report_gamestate()
                area.djose.leaving_djose()
                game.step = 1
                game.state = "Moonflow"

            if game.state == "Moonflow" and game.step == 1:
                report_gamestate()
                area.moonflow.arrival()
                area.moonflow.south_bank()
                game.step = 2

            if game.state == "Moonflow" and game.step == 2:
                report_gamestate()
                area.moonflow.north_bank()
                game.step = 1
                game.state = "Guadosalam"

            if game.state == "Guadosalam" and game.step == 1:
                report_gamestate()
                area.guadosalam.arrival()
                area.guadosalam.after_speech()
                game.step = 2

            if game.state == "Guadosalam" and game.step == 2:
                report_gamestate()
                area.guadosalam.guado_skip()
                game.step = 1
                game.state = "ThunderPlains"

            if game.state == "ThunderPlains" and game.step == 1:
                report_gamestate()
                status = area.thunder_plains.south_pathing()
                game.step = 2

            if game.state == "ThunderPlains" and game.step == 2:
                area.thunder_plains.agency()
                game.step = 3

            if game.state == "ThunderPlains" and game.step == 3:
                area.thunder_plains.north_pathing()
                game.state = "Macalania"
                game.step = 1

            if game.state == "Macalania" and game.step == 1:
                report_gamestate()
                area.mac_woods.arrival(False)
                game.step = 2

            if game.state == "Macalania" and game.step == 2:
                report_gamestate()
                area.mac_woods.lake_road()
                area.mac_woods.lake_road_2()
                game.step = 3

            if game.state == "Macalania" and game.step == 3:
                report_gamestate()
                area.mac_woods.lake()
                area.mac_temple.approach()
                game.step = 4

            if game.state == "Macalania" and game.step == 4:
                report_gamestate()
                area.mac_temple.arrival()
                area.mac_temple.start_seymour_fight()
                area.mac_temple.seymour_fight()
                game.step = 5

            if game.state == "Macalania" and game.step == 5:
                report_gamestate()
                area.mac_temple.trials()
                game.step = 6

            if game.state == "Macalania" and game.step == 6:
                report_gamestate()
                area.mac_temple.escape()
                game.step = 7

            if game.state == "Macalania" and game.step == 7:
                area.mac_temple.under_lake()
                game.step = 1
                game.state = "Home"

            if game.state == "Home" and game.step == 1:
                report_gamestate()
                area.home.desert()
                game.step = 2

            if game.state == "Home" and game.step == 2:
                report_gamestate()
                area.home.find_summoners()
                game.step = 1
                game.state = "rescueYuna"

            if game.state == "rescueYuna" and game.step == 1:
                report_gamestate()
                area.rescue_yuna.pre_evrae()
                battle.boss.evrae()
                area.rescue_yuna.guards()
                game.step = 2

            if game.state == "rescueYuna" and game.step == 2:
                report_gamestate()
                area.rescue_yuna.trials()
                area.rescue_yuna.trials_end()
                game.step = 3

            if game.state == "rescueYuna" and game.step == 3:
                report_gamestate()
                area.rescue_yuna.via_purifico()
                game.step = 4

            if game.state == "rescueYuna" and game.step == 4:
                report_gamestate()
                area.rescue_yuna.evrae_altana()
                game.step = 5

            if game.state == "rescueYuna" and game.step == 5:
                report_gamestate()
                area.rescue_yuna.seymour_natus()
                game.state = "Gagazet"
                if game_vars.nemesis():
                    game.step = 10
                else:
                    game.step = 1

            if game.state == "Gagazet" and game.step == 1:
                report_gamestate()
                area.gagazet.calm_lands()
                area.gagazet.defender_x()
                import rng_track

                advancePreX, advancePostX = rng_track.nea_track()
                if advancePostX in [0, 1]:
                    game.step = 2
                else:
                    game.step = 3

            if game.state == "Gagazet" and game.step == 2:
                report_gamestate()
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

            if game.state == "Gagazet" and game.step == 3:
                report_gamestate()
                area.gagazet.to_the_ronso()
                if game_vars.ne_armor() == 255:
                    area.ne_armor.loop_back_from_ronso()
                    game.step = 2
                else:
                    area.gagazet.gagazet_gates()
                    game.step = 4

            if game.state == "Gagazet" and game.step == 4:
                report_gamestate()
                area.gagazet.flux()
                game.step = 5

            if game.state == "Gagazet" and game.step == 5:
                report_gamestate()
                area.gagazet.dream()
                game.step = 6

            if game.state == "Gagazet" and game.step == 6:
                report_gamestate()
                area.gagazet.cave()
                area.gagazet.wrap_up()
                game.step = 1
                game.state = "Zanarkand"

            if game.state == "Zanarkand" and game.step == 1:
                report_gamestate()
                area.zanarkand.arrival()
                game.step = 2

            if game.state == "Zanarkand" and game.step == 2:
                report_gamestate()
                area.zanarkand.trials()
                game.step = 3

            if game.state == "Zanarkand" and game.step == 3:
                report_gamestate()
                area.zanarkand.sanctuary_keeper()
                game.step = 4

            if game.state == "Zanarkand" and game.step == 4:
                report_gamestate()
                area.zanarkand.yunalesca()
                game.step = 5

            if game.state == "Zanarkand" and game.step == 5:
                area.zanarkand.post_yunalesca()
                game.step = 1
                game.state = "Sin"

            if game.state == "Sin" and game.step == 1:
                report_gamestate()
                area.sin.making_plans()
                game.step = 2

            if game.state == "Sin" and game.step == 2:
                report_gamestate()
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

            if game.state == "Sin" and game.step == 3:
                report_gamestate()
                area.sin.inside_sin()
                game.step = 4

            if game.state == "Sin" and game.step == 4:
                area.sin.egg_hunt(game_vars.get_sin_auto_egg_hunt())
                if game_vars.nemesis():
                    battle.main.bfa_nem()
                else:
                    battle.boss.bfa()
                    battle.boss.yu_yevon()
                game.state = "End"

            # Nemesis logic only:
            if game.state == "Gagazet" and game.step == 10:
                nemesis.changes.calm_lands_1()
                game.step = 12

            if game.state == "Gagazet" and game.step == 11:
                nemesis.changes.remiem_races()
                game.step += 1

            if game.state == "Gagazet" and game.step == 12:
                print("MAAAAARK")
                memory.main.await_control()
                nemesis.changes.arena_purchase()
                area.gagazet.defender_x()
                game.step = 2

            if game.state == "Nem_Farm" and game.step == 1:
                report_gamestate()
                nemesis.arenaPrep.transition()
                while not nemesis.arenaPrep.t_plains(cap_num=1):
                    pass
                game.step = 2

            if game.state == "Nem_Farm" and game.step == 2:
                report_gamestate()
                while not nemesis.arenaPrep.calm(cap_num=1, airship_return=False):
                    pass
                game.step = 3

            if game.state == "Nem_Farm" and game.step == 3:
                report_gamestate()
                nemesis.arenaPrep.kilika_shop()
                game.step = 4

            if game.state == "Nem_Farm" and game.step == 4:
                report_gamestate()
                nemesis.arenaPrep.besaid_farm(cap_num=1)
                game.step = 5

            if game.state == "Nem_Farm" and game.step == 5:
                report_gamestate()
                nemesis.arenaPrep.kilika_farm(cap_num=1)
                game.step = 6

            if game.state == "Nem_Farm" and game.step == 6:
                report_gamestate()
                nemesis.arenaPrep.miihen_farm(cap_num=1)
                game.step = 7

            if game.state == "Nem_Farm" and game.step == 7:
                # reportGamestate()
                # nemesis.arenaPrep.mrrFarm(capNum=1)
                game.step = 8

            if game.state == "Nem_Farm" and game.step == 8:
                report_gamestate()
                nemesis.arenaPrep.od_to_ap()
                game.step = 9

            if game.state == "Nem_Farm" and game.step == 9:
                report_gamestate()
                nemesis.arenaPrep.besaid_farm(cap_num=10)
                game.step = 10

            if game.state == "Nem_Farm" and game.step == 10:
                report_gamestate()
                nemesis.arenaPrep.kilika_farm(cap_num=10)
                game.step = 11

            if game.state == "Nem_Farm" and game.step == 11:
                report_gamestate()
                nemesis.arenaPrep.miihen_farm(cap_num=10)
                game.step = 12

            if game.state == "Nem_Farm" and game.step == 12:
                # reportGamestate()
                # nemesis.arenaPrep.mrrFarm(capNum=10)
                game.step = 13

            if game.state == "Nem_Farm" and game.step == 13:
                report_gamestate()
                nemesis.arenaPrep.djose_farm(cap_num=10)
                game.step = 14

            if game.state == "Nem_Farm" and game.step == 14:
                report_gamestate()
                nemesis.arenaPrep.t_plains(cap_num=10, auto_haste=True)
                game.step = 15

            if game.state == "Nem_Farm" and game.step == 15:
                report_gamestate()
                nemesis.arenaPrep.bikanel(cap_num=10)
                game.step = 16

            if game.state == "Nem_Farm" and game.step == 16:
                report_gamestate()
                nemesis.arenaPrep.arena_return()
                nemesis.arenaPrep.auto_phoenix()
                game.step = 17

            if game.state == "Nem_Farm" and game.step == 17:
                report_gamestate()
                nemesis.arenaPrep.mac_woods(cap_num=10)
                game.step = 18

            if game.state == "Nem_Farm" and game.step == 18:
                report_gamestate()
                nemesis.arenaPrep.stolen_fayth_cave()
                game.step = 19

            if game.state == "Nem_Farm" and game.step == 19:
                report_gamestate()
                nemesis.arenaPrep.gagazet()
                # nemesis.arenaPrep.gagazet1()
                # nemesis.arenaPrep.gagazet2()
                # nemesis.arenaPrep.gagazet3()
                # game.state = "End" #Testing only
                game.step = 20

            if game.state == "Nem_Farm" and game.step == 20:
                report_gamestate()
                nemesis.arenaPrep.calm(cap_num=10, airship_return=False, force_levels=27)
                game.step = 21

            if game.state == "Nem_Farm" and game.step == 21:
                report_gamestate()
                nemesis.arenaPrep.one_mp_weapon()
                game.step = 22

            if game.state == "Nem_Farm" and game.step == 22:
                report_gamestate()
                nemesis.arenaPrep.inside_sin(cap_num=10)
                game.step = 23

            if game.state == "Nem_Farm" and game.step == 23:
                report_gamestate()
                nemesis.arenaPrep.unlock_omega()
                nemesis.arenaPrep.omega_ruins()
                game.step = 24

            if game.state == "Nem_Farm" and game.step == 24:
                nemesis.arenaPrep.kilika_final_shop()
                game.step = 25

            if game.state == "Nem_Farm" and game.step == 25:
                nemesis.arenaPrep.arena_return()
                nemesis.arenaPrep.final_weapon()
                game.state = "Nem_Arena"
                game.step = 1

            if game.state == "Nem_Arena" and game.step == 1:
                nemesis.arena_battles.battles_1()
                game_vars.print_arena_status()
                game.step = 2

            if game.state == "Nem_Arena" and game.step == 2:
                nemesis.arena_battles.battles_2()
                game_vars.print_arena_status()
                game.step = 3

            if game.state == "Nem_Arena" and game.step == 3:
                nemesis.arena_battles.juggernaut_farm()
                game_vars.print_arena_status()
                game.step = 4

            if game.state == "Nem_Arena" and game.step == 4:
                nemesis.arena_battles.battles_3()
                game_vars.print_arena_status()
                game.step = 5

            if game.state == "Nem_Arena" and game.step == 5:
                nemesis.arena_battles.battles_4()
                game_vars.print_arena_status()
                game.step = 6

            if game.state == "Nem_Arena" and game.step == 6:
                nemesis.arena_battles.nemesis_battle()
                game.step = 7

            if game.state == "Nem_Arena" and game.step == 7:
                nemesis.arena_battles.return_to_sin()
                game.state = "Sin"
                game.step = 3

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
    game = get_gamestate()

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
if __name__ == '__main__':
    game = get_gamestate()

    # Load up vars.py
    variables_setup()

    # Set up Gamestate and rng-related variables
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
