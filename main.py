# Libraries and Core Files
import random
import sys

import area.baaj
import area.besaid
import area.boats
import area.djose
import area.dreamZan
import area.gagazet
import area.guadosalam
import area.home
import area.kilika
import area.luca
import area.miihen
import area.moonflow
import area.MRR
import area.mTemple
import area.mWoods
import area.rescueYuna
import area.sin
import area.thunderPlains
import area.zanarkand
import battle.boss
import battle.main
import blitz
import logs
import memory.main
import reset
import screen
import vars
import xbox

game_vars = vars.vars_handle()
game_vars.set_start_vars()

# Plug in controller
FFXC = xbox.controller_handle()

# Speedrun sectional files
if game_vars.nemesis():
    import nemesis.arenaBattles
    import nemesis.arenaPrep
    import nemesis.changes

# Gamestate, "none" for new game, or set to a specific section to start from the first save.
# See the if statement tree below to determine starting position for Gamestate.
# These are the popular ones. New Game ('none') is the last one.
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
# step_counter = 4 # x30 Altana
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
# step_counter = 5 # x48 After Yunalesca
# Gamestate = "Sin"
# step_counter = 2 # x70 Shedinja Highbridge
# step_counter = 3 # x50 Start of Sea of Sorrows
# step_counter = 4 # x51 Before point of no return, with zombiestrike weapons (not Kimahri)
Gamestate = "none"
step_counter = 1  # NEW GAME!

# Nemesis load testing
# Gamestate = "Nem_Farm"
# step_counter = 2 #Start of Calm Lands (only one each)
# step_counter = 3
# step_counter = 6 #First Miihen farm
# step_counter = 13 #Just before Djose farm
# step_counter = 14 #Just before Thunder Plains farm
# step_counter = 16 #Just before Bikanel farm
# step_counter = 18 #Just before Fayth Cave farm
# step_counter = 19 #Gagazet farm
# step_counter = 20 #After Gagazet, before Calm Lands farm
# step_counter = 22 #Before Sin/Omega farms, AFTER picking up oneMP weapon
# step_counter = 24 #Final Prep before arena bosses

############################################################################################
# RNG - Using Rossy's FFX.exe fix, this allows us to choose the RNG seed we want. From 0-255

forceBlitzWin = False
seedHunt = False  # Update this to decide new seed or known seed
rngSelectArray = [31, 160]
maybeGoodSeeds = [2, 31, 142, 157, 160, 172, 177, 182, 183, 200, 224, 254]
rtaGoodSeeds = [160, 142, 34, 62, 210, 31, 159]
favoriteSeedsSoFar = [31, 160]
rngSeedNum = 160  # If you don't randomly select below, this will be the seed you run.
# TAS PB is on seed 31
# 160 is WR for both categories, just has a bad start
# Need review on the others

############################################################################################

if Gamestate == "Luca" and step_counter == 3:
    blitzTesting = True
    gameLength = "Testing Blitzball only"
elif Gamestate != "none":  # Loading a save file, no RNG manip here
    rngSeedNum = 255
    rngReviewOnly = False
    gameLength = "Loading mid point for testing."
    blitzTesting = False
    # gameVars.setCSR(True)
elif not seedHunt:  # Full run starting from New Game
    # Select a seed randomly, overrules the set seed above.
    rngSeedNum = random.choice(range(256))
    # Select a favorite seed randomly, overrules the set seed above.
    # rngSeedNum = random.choice(rngSelectArray)
    # Current WR is on seed 160 for both any% and CSR%
    rngReviewOnly = False
    gameLength = "Full Run"
    blitzTesting = False
else:  # Don't use this.
    step_counter = 1
    rngReviewOnly = True
    gameLength = "Seed Hunt"
    blitzTesting = False

print("Game type will be:", gameLength)
maxLoops = 12

# Other variables
rngSeedOrig = rngSeedNum
speedCount = 0
strengthCount = 0
gems = 0  # Set to 2 if loading in after Evrae Altana with two gems
autoEggHunt = True
specialZanLoad = False


# Main functions
def report_gamestate():
    global Gamestate
    global step_counter
    screen.clear_mouse(0)


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

# Using Rossy's FFX.exe fix, this allows us to choose the RNG seed we want. From 0-255
if game_vars.use_set_seed():
    memory.main.set_rng_seed(rngSeedNum)

rngSeed = memory.main.rng_seed()
print("---RNG seed:", rngSeed)
logs.next_stats(rngSeed)
logs.write_stats("RNG seed:")
logs.write_stats(rngSeed)

# Next, check if we are loading to a save file
if Gamestate != "none":
    if not (Gamestate == "Luca" and step_counter == 3):
        area.dreamZan.new_game(Gamestate)
        startTime = logs.time_stamp()
        logs.write_stats("Start time:")
        logs.write_stats(str(startTime))
        report_gamestate()
    import loadGame

    # Need to update these to use loadGame.loadSaveNum(number) for all.

    if Gamestate == "Baaj" and step_counter == 1:
        loadGame.load_save_num(40)
    if Gamestate == "Baaj" and step_counter == 4:
        loadGame.load_save_num(100)
    # Save pop-up after falling off of Rikkus boat
    if Gamestate == "Besaid" and step_counter == 1:
        loadGame.load_save_num(111)
    # Save pop-up after falling off of Rikkus boat
    if Gamestate == "Besaid" and step_counter == 2:
        loadGame.load_save_num(6)
        loadGame.besaid_trials()
    # Crusader's lodge after "Enough, Wakka!"
    if Gamestate == "Besaid" and step_counter == 3:
        loadGame.load_save_num(39)
        print("Load complete")
        while memory.main.user_control():
            if memory.main.get_coords()[0] > 0.5:
                FFXC.set_movement(1, 1)
            else:
                FFXC.set_movement(0, 1)
        print("Ready for regular path")
    # Besaid beach before boarding SS Liki ( nice alliteration :D )
    if Gamestate == "Boat1":
        loadGame.load_save_num(31)
        loadGame.boat_1()
    if Gamestate == "Kilika" and step_counter == 1:  # Just after entering the woods
        loadGame.load_save_num(22)
    if Gamestate == "Luca" and step_counter == 1:  # Approaching Luca via boat
        loadGame.load_save_num(112)
    if Gamestate == "Luca" and step_counter == 5:
        loadGame.load_save_num(5)
    if Gamestate == "Miihen" and step_counter == 1:  # After the talk with Auron
        loadGame.load_save_num(16)  # With laughing scene
        loadGame.load_miihen_start_laugh()
    if Gamestate == "Miihen" and step_counter == 2:  # Agency
        loadGame.load_save_num(28)
        returnArray = [False, 0, 0, False]
    if Gamestate == "MRR" and step_counter == 1:  # Mi'ihen North after meeting Seymour
        loadGame.load_save_num(38)
        memory.main.set_gil_value(4000)  # Fixes a low gil state for this save file.
        loadGame.load_mrr()
    # Aftermath, after talking to Seymour and then Auron
    if Gamestate == "Djose" and step_counter == 1:
        loadGame.load_save_num(27)
        loadGame.after_gui()
    if Gamestate == "Moonflow" and step_counter == 2:  # North bank, before Rikku
        loadGame.load_save_num(2)
        loadGame.moonflow_2()
    if Gamestate == "Guadosalam" and step_counter == 2:  # After the Farplane
        loadGame.load_save_num(3)
        loadGame.load_guado_skip()
    if Gamestate == "Macalania" and step_counter == 1:  # 1 = south, 2 = north
        loadGame.load_save_num(1)
    if Gamestate == "Macalania" and step_counter == 2:  # 1 = south, 2 = north
        loadGame.load_save_num(1)
    if Gamestate == "Macalania" and step_counter == 4:  # Right before Jyscal skip
        loadGame.load_save_num(1)
        loadGame.load_mac_temple()
    # Outside temple, before escaping.
    if Gamestate == "Macalania" and step_counter == 6:
        loadGame.load_save_num(4)
    if Gamestate == "Home" and step_counter == 1:
        loadGame.load_save_num(60)
    if Gamestate == "Home" and step_counter == 2:
        loadGame.load_save_num(11)
    if Gamestate == "rescueYuna" and step_counter == 1:  # Airship, first movement.
        # Blitz Win, save less speed/power spheres
        loadGame.load_save_num(56)
    if Gamestate == "rescueYuna" and step_counter == 2:  # Bevelle trials
        loadGame.load_save_num(15)
    if Gamestate == "rescueYuna" and step_counter == 4:  # Altana
        loadGame.load_save_num(30)
        # memory.main.setEncounterRate(setVal=0)
        # memory.main.setGameSpeed(setVal=1)
    # Highbridge before Seymour Natus
    if Gamestate == "rescueYuna" and step_counter == 5:
        loadGame.load_save_num(42)  # Regular
        # loadGame.loadSaveNum(67) #Nemesis
    if Gamestate == "Gagazet" and step_counter == 1:  # Just before Calm Lands
        loadGame.load_save_num(43)
        loadGame.load_calm()
        game_vars.set_blitz_win(True)
    if Gamestate == "Gagazet" and step_counter == 2:  # NE armor save
        loadGame.load_save_num(57)
    if Gamestate == "Gagazet" and step_counter == 3:  # Gagazet gates, after B&Y
        loadGame.load_save_num(138)  # Blitz Win
        # loadGame.loadSaveNum(53) # Blitz Loss
        game_vars.end_game_version_set(4)
        loadGame.load_gagazet_gates()
    if Gamestate == "Gagazet" and step_counter == 6:  # After the dream
        loadGame.load_save_num(98)
        game_vars.end_game_version_set(4)
        loadGame.load_gagazet_dream()
        game_vars.flux_overkill_success()
    if Gamestate == "Gagazet" and step_counter == 10:  # Calm Lands, but Nemesis version
        loadGame.load_save_num(43)
        loadGame.load_calm()
    if Gamestate == "Gagazet" and step_counter == 11:  # Calm Lands, but Nemesis version
        loadGame.load_save_num(64)
        FFXC.set_movement(1, 0)
        memory.main.wait_frames(60)
        FFXC.set_movement(0, 1)
        memory.main.wait_frames(60)
        FFXC.set_neutral()
        import menu

        menu.prep_calm_lands()
    if Gamestate == "Zanarkand" and step_counter == 1:  # Intro scene revisited
        loadGame.load_save_num(99)
        game_vars.end_game_version_set(1)
        game_vars.flux_overkill_success()
        game_vars.end_game_version_set(4)
    if Gamestate == "Zanarkand" and step_counter == 2:  # Just before the trials.
        loadGame.load_offset(35)
        loadGame.zan_trials()
        game_vars.end_game_version_set(4)
    if Gamestate == "Zanarkand" and step_counter == 3:  # After trials, before boss
        loadGame.load_save_num(45)
        game_vars.end_game_version_set(4)
    if Gamestate == "Zanarkand" and step_counter == 4:  # After Sanctuary Keeper
        loadGame.load_save_num(44)
        game_vars.end_game_version_set(4)
    if Gamestate == "Zanarkand" and step_counter == 5:  # After Yunalesca
        loadGame.load_save_num(48)
        specialZanLoad = True
    # Save sphere on the Highbridge before talking to Shedinja
    if Gamestate == "Sin" and step_counter == 2:
        # loadGame.loadSaveNum(49)
        # Nemesis logic, double friend sphere drops from B&Y
        loadGame.load_save_num(70)
        while not memory.main.oaka_gil_cursor() in [8, 20]:
            if memory.main.user_control():
                import targetPathing

                targetPathing.set_movement([-251, 340])
            else:
                FFXC.set_neutral()
            xbox.menu_b()
        memory.main.check_nea_armor()
    if Gamestate == "Sin" and step_counter == 3:  # Start of "Sea of Sorrows" section
        loadGame.load_save_num(50)
    if Gamestate == "Sin" and step_counter == 4:  # Before point of no return
        # This save has zombiestrike weapons for all except Kimahri
        # Please use for egg hunt and zombie weapon testing.
        loadGame.load_save_num(51)
        game_vars.set_zombie(5)
        loadGame.load_egg_hunt()

    # Nemesis run loads
    if Gamestate == "Nem_Farm" and step_counter == 1:
        loadGame.load_save_num(66)
    if Gamestate == "Nem_Farm" and step_counter == 2:
        loadGame.load_save_num(69)
    if Gamestate == "Nem_Farm" and step_counter == 3:
        loadGame.load_save_num(84)
        game_vars.set_nem_checkpoint_ap(3)  # See nemesis.menu
        # import nemesis.arenaPrep
        nemesis.arenaPrep.arena_return()
    if Gamestate == "Nem_Farm" and step_counter == 5:
        loadGame.load_save_num(71)
    if Gamestate == "Nem_Farm" and step_counter == 6:
        loadGame.load_save_num(72)
        game_vars.set_nem_checkpoint_ap(2)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and step_counter == 8:
        loadGame.load_save_num(73)
    if Gamestate == "Nem_Farm" and step_counter == 9:
        loadGame.load_save_num(75)
        game_vars.set_nem_checkpoint_ap(3)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and step_counter == 13:
        loadGame.load_save_num(116)
        game_vars.set_nem_checkpoint_ap(7)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and step_counter == 14:
        loadGame.load_save_num(76)
        game_vars.set_nem_checkpoint_ap(10)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and step_counter == 16:
        loadGame.load_save_num(113)
        game_vars.set_nem_checkpoint_ap(12)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and step_counter == 17:
        loadGame.load_save_num(111)
        game_vars.set_nem_checkpoint_ap(14)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and step_counter == 18:
        loadGame.load_save_num(114)
        game_vars.set_nem_checkpoint_ap(15)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and step_counter == 19:  # Gagazet
        loadGame.load_save_num(115)
        game_vars.set_nem_checkpoint_ap(19)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and step_counter == 21:
        loadGame.load_save_num(79)
        nemesis.arenaPrep.arena_return()
        game_vars.set_nem_checkpoint_ap(27)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and step_counter == 22:
        loadGame.load_save_num(82)
        # import nemesis.menu
        # nemesis.menu.rikkuHaste()
        game_vars.set_nem_checkpoint_ap(24)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and step_counter == 23:
        loadGame.load_save_num(80)
        game_vars.set_nem_checkpoint_ap(30)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and step_counter == 24:
        loadGame.load_save_num(81)
        game_vars.set_nem_checkpoint_ap(30)
        game_vars.set_nem_checkpoint_ap(30)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and step_counter == 20:
        loadGame.load_save_num(85)
        game_vars.set_nem_checkpoint_ap(30)
    if Gamestate == "Nem_Farm":
        memory.main.check_nea_armor()
    memory.main.check_nea_armor()

rikkuCharged = 0
blitzLoops = 0

while Gamestate != "End":

    try:
        # Blitzball testing logic
        if Gamestate == "Luca" and step_counter == 3:
            area.dreamZan.new_game(Gamestate)
            loadGame.load_save_num(37)

        if rngSeedNum >= 256:
            Gamestate = "End"

        # Start of the game, start of Dream Zanarkand section
        if Gamestate == "none" and step_counter == 1:
            report_gamestate()
            print("New Game 1 function initiated.")
            area.dreamZan.new_game(Gamestate)
            print("New Game 1 function complete.")
            game_vars.set_new_game()
            game_vars.set_csr(True)
            print("Variables initialized.")
            Gamestate = "DreamZan"
            memory.main.wait_frames(30 * 0.5)
            print("New Game 2 function initiated.")
            area.dreamZan.new_game_2()
            startTime = logs.time_stamp()
            logs.write_stats("Start time:")
            logs.write_stats(str(startTime))
            print("Timer starts now.")
            area.dreamZan.listen_story()
            # Gamestate, step_counter = reset.midRunReset()
            # Start of the game, up through the start of Sinspawn Ammes fight
            step_counter = 2
            area.dreamZan.ammes_battle()

        if Gamestate == "DreamZan" and step_counter == 2:
            report_gamestate()
            battle.boss.ammes()
            step_counter = 3
            report_gamestate()

        if Gamestate == "DreamZan" and step_counter == 3:
            area.dreamZan.after_ammes()
            # Sin drops us near Baaj temple.
            Gamestate = "Baaj"
            step_counter = 1

        if Gamestate == "Baaj" and step_counter == 1:
            report_gamestate()
            print("Starting Baaj temple section")
            area.baaj.entrance()
            step_counter = 2

        if Gamestate == "Baaj" and step_counter == 2:
            report_gamestate()
            area.baaj.baaj_puzzle()
            step_counter = 3

        if Gamestate == "Baaj" and step_counter == 3:
            area.baaj.klikk_fight()
            step_counter = 4
            report_gamestate()

        if Gamestate == "Baaj" and step_counter == 4:
            # Klikk fight done. Now to wait for the Al Bhed ship.
            print("Al Bhed boat part 1")
            area.baaj.ab_boat_1()
            step_counter = 5

        if Gamestate == "Baaj" and step_counter == 5:
            report_gamestate()
            area.baaj.ab_swimming_1()
            step_counter = 6
            report_gamestate()

        if Gamestate == "Baaj" and step_counter == 6:
            print("Underwater Airship section")
            area.baaj.ab_swimming_2()
            Gamestate = "Besaid"
            step_counter = 1
            report_gamestate()

        if Gamestate == "Besaid" and step_counter == 1:
            report_gamestate()
            area.besaid.beach()
            step_counter = 2
            report_gamestate()

        if Gamestate == "Besaid" and step_counter == 2:
            area.besaid.trials()
            step_counter = 3
            report_gamestate()

        if Gamestate == "Besaid" and step_counter == 3:
            area.besaid.leaving()
            Gamestate = "Boat1"
            if memory.main.get_tidus_slvl() < 3:
                print("=========================")
                print("=== Under-levelled!!! ===")
                print("=========================")
                Gamestate, step_counter = reset.mid_run_reset()
            else:
                step_counter = 1
                report_gamestate()

        if Gamestate == "Boat1":
            report_gamestate()
            area.boats.ss_liki()
            area.kilika.arrival()
            Gamestate = "Kilika"

        if Gamestate == "Kilika" and step_counter == 1:
            report_gamestate()
            area.kilika.forest_1()
            report_gamestate()
            step_counter = 3

        if Gamestate == "Kilika" and step_counter == 3:
            report_gamestate()
            area.kilika.trials()
            area.kilika.trials_end()
            step_counter = 4

        if Gamestate == "Kilika" and step_counter == 4:
            report_gamestate()
            area.kilika.forest_3()
            step_counter = 5

        if Gamestate == "Kilika" and step_counter == 5:
            report_gamestate()
            step_counter = 1
            Gamestate = "Boat2"

        if Gamestate == "Boat2":
            report_gamestate()
            area.boats.ss_winno()
            Gamestate = "Boat3"

        if Gamestate == "Boat3":
            report_gamestate()
            area.boats.ss_winno_2()
            Gamestate = "Luca"

        if Gamestate == "Luca" and step_counter == 1:
            report_gamestate()
            area.luca.arrival()
            step_counter = 2

        if Gamestate == "Luca" and step_counter == 2:
            report_gamestate()
            endTime = logs.time_stamp()
            totalTime = endTime - startTime
            print("Pre-Blitz time:", str(totalTime))
            logs.write_stats("Pre Blitz time:")
            logs.write_stats(totalTime)
            step_counter = 3

        if Gamestate == "Luca" and step_counter == 3:
            report_gamestate()
            area.luca.blitz_start()
            step_counter = 4

        if Gamestate == "Luca" and step_counter == 4:
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
                Gamestate, step_counter = reset.mid_run_reset()
                blitzLoops += 1
            elif game_vars.blitz_loss_reset() and not game_vars.get_blitz_win():
                FFXC.set_neutral()
                print("------------------------------")
                print("- Resetting - Lost Blitzball -")
                print("------------------------------")
                screen.await_turn()
                Gamestate, step_counter = reset.mid_run_reset()
            else:
                print("--------------")
                print("- Post-Blitz -")
                print("--------------")
                step_counter = 5

        if Gamestate == "Luca" and step_counter == 5:
            report_gamestate()
            area.luca.after_blitz()
            step_counter = 1
            Gamestate = "Miihen"

        # Just to make sure we set this variable somewhere.
        if Gamestate == "Miihen" and step_counter == 1:
            report_gamestate()
            returnArray = area.miihen.arrival()
            selfDestruct = area.miihen.arrival_2(
                returnArray[0], returnArray[1], returnArray[2]
            )
            step_counter = 2

        if Gamestate == "Miihen" and step_counter == 2:
            report_gamestate()
            area.miihen.mid_point()
            print("End of Mi'ihen mid point section.")
            area.miihen.low_road(returnArray[0], returnArray[1], returnArray[2])

            # Report duration at the end of Mi'ihen section for all runs.
            endTime = logs.time_stamp()
            totalTime = endTime - startTime
            print("Mi'ihen End timer is:", str(totalTime))
            logs.write_stats("Miihen End time:")
            logs.write_stats(totalTime)
            Gamestate = "MRR"
            step_counter = 1

        if Gamestate == "MRR" and step_counter == 1:
            report_gamestate()
            area.MRR.arrival()
            area.MRR.main_path()
            if memory.main.game_over():
                Gamestate = "gameOverError"
            step_counter = 2

        if Gamestate == "MRR" and step_counter == 2:
            report_gamestate()
            area.MRR.battle_site()
            area.MRR.gui_and_aftermath()
            endTime = logs.time_stamp()
            totalTime = endTime - startTime
            print("End of Battle Site timer is:", str(totalTime))
            logs.write_stats("Djose-Start time:")
            logs.write_stats(totalTime)
            Gamestate = "Djose"
            step_counter = 1

        if Gamestate == "Djose" and step_counter == 1:
            report_gamestate()
            area.djose.path()
            step_counter = 2

        if Gamestate == "Djose" and step_counter == 2:
            report_gamestate()
            area.djose.temple()
            area.djose.trials()
            step_counter = 3

        if Gamestate == "Djose" and step_counter == 3:
            report_gamestate()
            area.djose.leaving_djose()
            step_counter = 1
            Gamestate = "Moonflow"

        if Gamestate == "Moonflow" and step_counter == 1:
            report_gamestate()
            area.moonflow.arrival()
            area.moonflow.south_bank()
            step_counter = 2

        if Gamestate == "Moonflow" and step_counter == 2:
            report_gamestate()
            area.moonflow.north_bank()
            step_counter = 1
            Gamestate = "Guadosalam"

        if Gamestate == "Guadosalam" and step_counter == 1:
            report_gamestate()
            area.guadosalam.arrival()
            area.guadosalam.after_speech()
            step_counter = 2

        if Gamestate == "Guadosalam" and step_counter == 2:
            report_gamestate()
            area.guadosalam.guado_skip()
            step_counter = 1
            Gamestate = "ThunderPlains"

        if Gamestate == "ThunderPlains" and step_counter == 1:
            report_gamestate()
            status = area.thunderPlains.south_pathing()
            step_counter = 2

        if Gamestate == "ThunderPlains" and step_counter == 2:
            area.thunderPlains.agency()
            step_counter = 3

        if Gamestate == "ThunderPlains" and step_counter == 3:
            area.thunderPlains.north_pathing()
            Gamestate = "Macalania"
            step_counter = 1

        if Gamestate == "Macalania" and step_counter == 1:
            report_gamestate()
            area.mWoods.arrival(False)
            step_counter = 2

        if Gamestate == "Macalania" and step_counter == 2:
            report_gamestate()
            area.mWoods.lake_road()
            area.mWoods.lake_road_2()
            step_counter = 3

        if Gamestate == "Macalania" and step_counter == 3:
            report_gamestate()
            area.mWoods.lake()
            area.mTemple.approach()
            step_counter = 4

        if Gamestate == "Macalania" and step_counter == 4:
            report_gamestate()
            area.mTemple.arrival()
            area.mTemple.start_seymour_fight()
            area.mTemple.seymour_fight()
            step_counter = 5

        if Gamestate == "Macalania" and step_counter == 5:
            report_gamestate()
            area.mTemple.trials()
            step_counter = 6

        if Gamestate == "Macalania" and step_counter == 6:
            report_gamestate()
            area.mTemple.escape()
            step_counter = 7

        if Gamestate == "Macalania" and step_counter == 7:
            area.mTemple.under_lake()
            step_counter = 1
            Gamestate = "Home"

        if Gamestate == "Home" and step_counter == 1:
            report_gamestate()
            area.home.desert()
            step_counter = 2

        if Gamestate == "Home" and step_counter == 2:
            report_gamestate()
            area.home.find_summoners()
            step_counter = 1
            Gamestate = "rescueYuna"

        if Gamestate == "rescueYuna" and step_counter == 1:
            report_gamestate()
            area.rescueYuna.pre_evrae()
            battle.boss.evrae()
            area.rescueYuna.guards()
            step_counter = 2

        if Gamestate == "rescueYuna" and step_counter == 2:
            report_gamestate()
            area.rescueYuna.trials()
            area.rescueYuna.trials_end()
            step_counter = 3

        if Gamestate == "rescueYuna" and step_counter == 3:
            report_gamestate()
            area.rescueYuna.via_purifico()
            step_counter = 4

        if Gamestate == "rescueYuna" and step_counter == 4:
            report_gamestate()
            area.rescueYuna.evrae_altana()
            step_counter = 5

        if Gamestate == "rescueYuna" and step_counter == 5:
            report_gamestate()
            area.rescueYuna.seymour_natus()
            Gamestate = "Gagazet"
            if game_vars.nemesis():
                step_counter = 10
            else:
                step_counter = 1

        if Gamestate == "Gagazet" and step_counter == 1:
            manipTime1 = logs.time_stamp()
            report_gamestate()
            area.gagazet.calm_lands()
            area.gagazet.defender_x()
            step_counter = 2

        if Gamestate == "Gagazet" and step_counter == 2:
            report_gamestate()
            if game_vars.try_for_ne():
                import area.neArmor

                print("Mark 1")
                area.neArmor.to_hidden_cave()
                print("Mark 2")
                area.neArmor.drop_hunt()
                print("Mark 3")
                area.neArmor.return_to_gagazet()
            manipTime2 = logs.time_stamp()
            manipTime = manipTime2 - manipTime1
            print("NEA Manip duration:", str(manipTime))
            logs.write_stats("NEA Manip duration:")
            logs.write_stats(manipTime)
            step_counter = 3

        if Gamestate == "Gagazet" and step_counter == 3:
            report_gamestate()
            area.gagazet.to_the_ronso()
            area.gagazet.gagazet_gates()
            step_counter = 4

        if Gamestate == "Gagazet" and step_counter == 4:
            report_gamestate()
            area.gagazet.flux()
            step_counter = 5

        if Gamestate == "Gagazet" and step_counter == 5:
            report_gamestate()
            area.gagazet.dream()
            step_counter = 6

        if Gamestate == "Gagazet" and step_counter == 6:
            report_gamestate()
            area.gagazet.cave()
            area.gagazet.wrap_up()
            step_counter = 1
            Gamestate = "Zanarkand"

        if Gamestate == "Zanarkand" and step_counter == 1:
            report_gamestate()
            area.zanarkand.arrival()
            step_counter = 2

        if Gamestate == "Zanarkand" and step_counter == 2:
            report_gamestate()
            area.zanarkand.trials()
            step_counter = 3

        if Gamestate == "Zanarkand" and step_counter == 3:
            report_gamestate()
            area.zanarkand.sanctuary_keeper()
            step_counter = 4

        if Gamestate == "Zanarkand" and step_counter == 4:
            report_gamestate()
            area.zanarkand.yunalesca()
            step_counter = 5

        if Gamestate == "Zanarkand" and step_counter == 5:
            area.zanarkand.post_yunalesca()
            step_counter = 1
            Gamestate = "Sin"

        if Gamestate == "Sin" and step_counter == 1:
            report_gamestate()
            area.sin.making_plans()
            step_counter = 2

        if Gamestate == "Sin" and step_counter == 2:
            report_gamestate()
            print("Test 1")
            area.sin.shedinja()
            print("Test 2")
            area.sin.facing_sin()
            print("Test 3")
            if game_vars.nemesis():
                Gamestate = "Nem_Farm"
                step_counter = 1
            else:
                step_counter = 3

        if Gamestate == "Sin" and step_counter == 3:
            report_gamestate()
            area.sin.inside_sin()
            step_counter = 4

        if Gamestate == "Sin" and step_counter == 4:
            area.sin.egg_hunt(autoEggHunt)
            if game_vars.nemesis():
                battle.main.bfa_nem()
            else:
                battle.boss.bfa()
                battle.boss.yu_yevon()
            Gamestate = "End"

        # Nemesis logic only:
        if Gamestate == "Gagazet" and step_counter == 10:
            nemesis.changes.calm_lands_1()
            step_counter = 12

        if Gamestate == "Gagazet" and step_counter == 11:
            nemesis.changes.remiem_races()
            step_counter += 1

        if Gamestate == "Gagazet" and step_counter == 12:
            print("MAAAAARK")
            memory.main.await_control()
            nemesis.changes.arena_purchase()
            area.gagazet.defender_x()
            step_counter = 2

        if Gamestate == "Nem_Farm" and step_counter == 1:
            report_gamestate()
            nemesis.arenaPrep.transition()
            while not nemesis.arenaPrep.t_plains(cap_num=1):
                pass
            step_counter = 2

        if Gamestate == "Nem_Farm" and step_counter == 2:
            report_gamestate()
            while not nemesis.arenaPrep.calm(cap_num=1, airship_return=False):
                pass
            step_counter = 3

        if Gamestate == "Nem_Farm" and step_counter == 3:
            report_gamestate()
            nemesis.arenaPrep.kilika_shop()
            step_counter = 4

        if Gamestate == "Nem_Farm" and step_counter == 4:
            report_gamestate()
            nemesis.arenaPrep.besaid_farm(cap_num=1)
            step_counter = 5

        if Gamestate == "Nem_Farm" and step_counter == 5:
            report_gamestate()
            nemesis.arenaPrep.kilika_farm(cap_num=1)
            step_counter = 6

        if Gamestate == "Nem_Farm" and step_counter == 6:
            report_gamestate()
            nemesis.arenaPrep.miihen_farm(cap_num=1)
            step_counter = 7

        if Gamestate == "Nem_Farm" and step_counter == 7:
            # reportGamestate()
            # nemesis.arenaPrep.mrrFarm(capNum=1)
            step_counter = 8

        if Gamestate == "Nem_Farm" and step_counter == 8:
            report_gamestate()
            nemesis.arenaPrep.od_to_ap()
            step_counter = 9

        if Gamestate == "Nem_Farm" and step_counter == 9:
            report_gamestate()
            nemesis.arenaPrep.besaid_farm(cap_num=10)
            step_counter = 10

        if Gamestate == "Nem_Farm" and step_counter == 10:
            report_gamestate()
            nemesis.arenaPrep.kilika_farm(cap_num=10)
            step_counter = 11

        if Gamestate == "Nem_Farm" and step_counter == 11:
            report_gamestate()
            nemesis.arenaPrep.miihen_farm(cap_num=10)
            step_counter = 12

        if Gamestate == "Nem_Farm" and step_counter == 12:
            # reportGamestate()
            # nemesis.arenaPrep.mrrFarm(capNum=10)
            step_counter = 13

        if Gamestate == "Nem_Farm" and step_counter == 13:
            report_gamestate()
            nemesis.arenaPrep.djose_farm(cap_num=10)
            step_counter = 14

        if Gamestate == "Nem_Farm" and step_counter == 14:
            report_gamestate()
            nemesis.arenaPrep.t_plains(cap_num=10, auto_haste=True)
            step_counter = 15

        if Gamestate == "Nem_Farm" and step_counter == 15:
            report_gamestate()
            nemesis.arenaPrep.bikanel(cap_num=10)
            step_counter = 16

        if Gamestate == "Nem_Farm" and step_counter == 16:
            report_gamestate()
            nemesis.arenaPrep.arena_return()
            nemesis.arenaPrep.auto_phoenix()
            step_counter = 17

        if Gamestate == "Nem_Farm" and step_counter == 17:
            report_gamestate()
            nemesis.arenaPrep.mac_woods(cap_num=10)
            step_counter = 18

        if Gamestate == "Nem_Farm" and step_counter == 18:
            report_gamestate()
            nemesis.arenaPrep.stolen_fayth_cave()
            step_counter = 19

        if Gamestate == "Nem_Farm" and step_counter == 19:
            report_gamestate()
            nemesis.arenaPrep.gagazet()
            # nemesis.arenaPrep.gagazet1()
            # nemesis.arenaPrep.gagazet2()
            # nemesis.arenaPrep.gagazet3()
            # Gamestate = "End" #Testing only
            step_counter = 20

        if Gamestate == "Nem_Farm" and step_counter == 20:
            report_gamestate()
            nemesis.arenaPrep.calm(cap_num=10, airship_return=False, force_levels=27)
            step_counter = 21

        if Gamestate == "Nem_Farm" and step_counter == 21:
            report_gamestate()
            nemesis.arenaPrep.one_mp_weapon()
            step_counter = 22

        if Gamestate == "Nem_Farm" and step_counter == 22:
            report_gamestate()
            nemesis.arenaPrep.inside_sin(cap_num=10)
            step_counter = 23

        if Gamestate == "Nem_Farm" and step_counter == 23:
            report_gamestate()
            nemesis.arenaPrep.unlock_omega()
            nemesis.arenaPrep.omega_ruins()
            step_counter = 24

        if Gamestate == "Nem_Farm" and step_counter == 24:
            nemesis.arenaPrep.kilika_final_shop()
            step_counter = 25

        if Gamestate == "Nem_Farm" and step_counter == 25:
            nemesis.arenaPrep.arena_return()
            nemesis.arenaPrep.final_weapon()
            Gamestate = "Nem_Arena"
            step_counter = 1

        if Gamestate == "Nem_Arena" and step_counter == 1:
            nemesis.arenaBattles.battles_1()
            game_vars.print_arena_status()
            step_counter = 2

        if Gamestate == "Nem_Arena" and step_counter == 2:
            nemesis.arenaBattles.battles_2()
            game_vars.print_arena_status()
            step_counter = 3

        if Gamestate == "Nem_Arena" and step_counter == 3:
            nemesis.arenaBattles.juggernaut_farm()
            game_vars.print_arena_status()
            step_counter = 4

        if Gamestate == "Nem_Arena" and step_counter == 4:
            nemesis.arenaBattles.battles_3()
            game_vars.print_arena_status()
            step_counter = 5

        if Gamestate == "Nem_Arena" and step_counter == 5:
            nemesis.arenaBattles.battles_4()
            game_vars.print_arena_status()
            step_counter = 6

        if Gamestate == "Nem_Arena" and step_counter == 6:
            nemesis.arenaBattles.nemesis_battle()
            step_counter = 7

        if Gamestate == "Nem_Arena" and step_counter == 7:
            nemesis.arenaBattles.return_to_sin()
            Gamestate = "Sin"
            step_counter = 3

        if (
            Gamestate == "End"
            and game_vars.loop_seeds()
            and rngSeedNum - rngSeedOrig < maxLoops
        ):
            # End of seed logic.
            Gamestate, step_counter = reset.mid_run_reset(
                land_run=True, start_time=startTime
            )

        print("------------------------------")
        print("Looping")
        print(Gamestate, "|", step_counter)
        print("------------------------------")

    except KeyboardInterrupt:
        print("Keyboard Interrupt - Exiting.")
        sys.exit(0)

print("Time! The game is now over.")

endTime = logs.time_stamp()

if memory.main.get_story_progress() > 3210:
    totalTime = endTime - startTime
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
