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

gameVars = vars.varsHandle()
gameVars.set_start_vars()

# Plug in controller
FFXC = xbox.controllerHandle()

# Speedrun sectional files
if gameVars.nemesis():
    import nemesis.arenaBattles
    import nemesis.arenaPrep
    import nemesis.changes

# Gamestate, "none" for new game, or set to a specific section to start from the first save.
# See the if statement tree below to determine starting position for Gamestate.
# These are the popular ones. New Game ('none') is the last one.
# Gamestate = "Baaj"
# StepCounter = 1 # x40 Baaj temple, before Geos boss
# StepCounter = 4 # x100 Al Bhed boat before Tros
# Gamestate = "Besaid"
# StepCounter = 1 # x111 Before first viewing Besaid beach
# StepCounter = 2 # x6 Crusader's hut before trials
# StepCounter = 3 # x39 Crusader's hut after trials
# Gamestate = "Boat1"
# StepCounter = 1 # 31 NOT WORKING
# Gamestate = "Kilika"
# StepCounter = 1 # x22
# Gamestate = "Luca"
# StepCounter = 1 # x112 Boat lands, first movement
# StepCounter = 3 # Blitzball only, do not use
# StepCounter = 5 # x5 between Blitz and swimmers/Garuda REMAKE THIS SAVE
# Gamestate = "Miihen"
# StepCounter = 1 # x16 with laughing scene, 26 after laughing scene
# StepCounter = 2 # x28 (Agency before Chocobo Eater)
# Gamestate = "MRR"
# StepCounter = 1 # x38, includes a low-gil fix
# Gamestate = "Djose"
# StepCounter = 1 # x27
# Gamestate = "Moonflow"
# StepCounter = 2 # x2 After Extractor
# Gamestate = "Guadosalam"
# StepCounter = 2 # x3 before Guadosalam Skip
# Gamestate = "Macalania"
# StepCounter = 1 # x9
# StepCounter = 2 # x7
# StepCounter = 4 # x10 Seymour
# StepCounter = 6 # x4 Before escape sequence - RE-CHECK SPHERE GRID
# Gamestate = "Home"
# StepCounter = 1 # x60
# StepCounter = 2 # x11
# Gamestate = "rescueYuna"
# StepCounter = 1 # x56 First save chance on airship, before any movement.
# StepCounter = 2 # x15
# StepCounter = 4 # x30 Altana
# StepCounter = 5 # x42 regular, 67 nemesis
# Gamestate = "Gagazet"
# StepCounter = 1 # x43
# StepCounter = 3 # x138 After B&Y
# StepCounter = 6 # x98 After Flux/Dream. Can select version 3 or 4 below.
# StepCounter = 10 # Nemesis variant, blitz win logic (not working)
# StepCounter = 11 # Remiem racing
# Gamestate = "Zanarkand"
# StepCounter = 1 # x99 Campfire
# StepCounter = 4 # x44 Before Yunalesca
# StepCounter = 5 # x48 After Yunalesca
# Gamestate = "Sin"
# StepCounter = 2 # x70 Shedinja Highbridge
# StepCounter = 3 # x50 Start of Sea of Sorrows
# StepCounter = 4 # x51 Before point of no return, with zombiestrike weapons (not Kimahri)
Gamestate = "none"
StepCounter = 1  # NEW GAME!

# Nemesis load testing
# Gamestate = "Nem_Farm"
# StepCounter = 2 #Start of Calm Lands (only one each)
# StepCounter = 3
# StepCounter = 6 #First Miihen farm
# StepCounter = 13 #Just before Djose farm
# StepCounter = 14 #Just before Thunder Plains farm
# StepCounter = 16 #Just before Bikanel farm
# StepCounter = 18 #Just before Fayth Cave farm
# StepCounter = 19 #Gagazet farm
# StepCounter = 20 #After Gagazet, before Calm Lands farm
# StepCounter = 22 #Before Sin/Omega farms, AFTER picking up oneMP weapon
# StepCounter = 24 #Final Prep before arena bosses

####################################################################################################
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

####################################################################################################

if Gamestate == "Luca" and StepCounter == 3:
    blitzTesting = True
    gameLength = "Testing Blitzball only"
elif Gamestate != "none":  # Loading a save file, no RNG manip here
    rngSeedNum = 255
    rngReviewOnly = False
    gameLength = "Loading mid point for testing."
    blitzTesting = False
    # gameVars.setCSR(True)
elif not seedHunt:  # Full run starting from New Game
    rngSeedNum = random.choice(
        range(256)
    )  # Select a seed randomly, overrules the set seed above.
    # rngSeedNum = random.choice(rngSelectArray)  # Select a favorite seed randomly, overrules the set seed above.
    # Current WR is on seed 160 for both any% and CSR%
    rngReviewOnly = False
    gameLength = "Full Run"
    blitzTesting = False
else:  # Don't use this.
    StepCounter = 1
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
    global StepCounter
    screen.clear_mouse(0)


# Initiate memory reading, after we know the game is open.
# import memory
while not memory.main.start():
    pass

# Main
report_gamestate()
if memory.main.getMap in [23, 348, 349]:
    pass
else:
    reset.reset_to_main_menu()

print("Game start screen")
screen.clear_mouse(0)

# Using Rossy's FFX.exe fix, this allows us to choose the RNG seed we want. From 0-255
if gameVars.useSetSeed():
    memory.main.setRngSeed(rngSeedNum)

rngSeed = memory.main.rngSeed()
print("---RNG seed:", rngSeed)
logs.next_stats(rngSeed)
logs.write_stats("RNG seed:")
logs.write_stats(rngSeed)

# Next, check if we are loading to a save file
if Gamestate != "none":
    if not (Gamestate == "Luca" and StepCounter == 3):
        area.dreamZan.NewGame(Gamestate)
        startTime = logs.time_stamp()
        logs.write_stats("Start time:")
        logs.write_stats(str(startTime))
        report_gamestate()
    import loadGame

    # Need to update these to use loadGame.loadSaveNum(number) for all.

    if Gamestate == "Baaj" and StepCounter == 1:
        loadGame.load_save_num(40)
    if Gamestate == "Baaj" and StepCounter == 4:
        loadGame.load_save_num(100)
    if (
        Gamestate == "Besaid" and StepCounter == 1
    ):  # Save pop-up after falling off of Rikkus boat
        loadGame.load_save_num(111)
    if (
        Gamestate == "Besaid" and StepCounter == 2
    ):  # Save pop-up after falling off of Rikkus boat
        loadGame.load_save_num(6)
        loadGame.besaid_trials()
    if (
        Gamestate == "Besaid" and StepCounter == 3
    ):  # Crusader's lodge after "Enough, Wakka!"
        loadGame.load_save_num(39)
        print("Load complete")
        while memory.main.userControl():
            if memory.main.getCoords()[0] > 0.5:
                FFXC.set_movement(1, 1)
            else:
                FFXC.set_movement(0, 1)
        print("Ready for regular path")
    # Besaid beach before boarding SS Liki ( nice alliteration :D )
    if Gamestate == "Boat1":
        loadGame.load_save_num(31)
        loadGame.boat_1()
    if Gamestate == "Kilika" and StepCounter == 1:  # Just after entering the woods
        loadGame.load_save_num(22)
    if Gamestate == "Luca" and StepCounter == 1:  # Approaching Luca via boat
        loadGame.load_save_num(112)
    if Gamestate == "Luca" and StepCounter == 5:
        loadGame.load_save_num(5)
    if Gamestate == "Miihen" and StepCounter == 1:  # After the talk with Auron
        loadGame.load_save_num(16)  # With laughing scene
        loadGame.load_miihen_start_laugh()
    if Gamestate == "Miihen" and StepCounter == 2:  # Agency
        loadGame.load_save_num(28)
        returnArray = [False, 0, 0, False]
    if Gamestate == "MRR" and StepCounter == 1:  # Mi'ihen North after meeting Seymour
        loadGame.load_save_num(38)
        memory.main.setGilvalue(4000)  # Fixes a low gil state for this save file.
        loadGame.load_mrr()
    if (
        Gamestate == "Djose" and StepCounter == 1
    ):  # Aftermath, after talking to Seymour and then Auron
        loadGame.load_save_num(27)
        loadGame.after_gui()
    if Gamestate == "Moonflow" and StepCounter == 2:  # North bank, before Rikku
        loadGame.load_save_num(2)
        loadGame.moonflow_2()
    if Gamestate == "Guadosalam" and StepCounter == 2:  # After the Farplane
        loadGame.load_save_num(3)
        loadGame.load_guado_skip()
    if Gamestate == "Macalania" and StepCounter == 1:  # 1 = south, 2 = north
        loadGame.load_save_num(9)
    if Gamestate == "Macalania" and StepCounter == 2:  # 1 = south, 2 = north
        loadGame.load_save_num(7)
    if Gamestate == "Macalania" and StepCounter == 4:  # Right before Jyscal skip
        loadGame.load_save_num(10)
        loadGame.load_mac_temple()
    # Outside temple, before escaping.
    if Gamestate == "Macalania" and StepCounter == 6:
        loadGame.load_save_num(4)
    if Gamestate == "Home" and StepCounter == 1:
        loadGame.load_save_num(60)
    if Gamestate == "Home" and StepCounter == 2:
        loadGame.load_save_num(11)
    if Gamestate == "rescueYuna" and StepCounter == 1:  # Airship, first movement.
        # Blitz Win, save less speed/power spheres
        loadGame.load_save_num(56)
    if Gamestate == "rescueYuna" and StepCounter == 2:  # Bevelle trials
        loadGame.load_save_num(15)
    if Gamestate == "rescueYuna" and StepCounter == 4:  # Altana
        loadGame.load_save_num(30)
        # memory.main.setEncounterRate(setVal=0)
        # memory.main.setGameSpeed(setVal=1)
    if (
        Gamestate == "rescueYuna" and StepCounter == 5
    ):  # Highbridge before Seymour Natus
        loadGame.load_save_num(42)  # Regular
        # loadGame.loadSaveNum(67) #Nemesis
    if Gamestate == "Gagazet" and StepCounter == 1:  # Just before Calm Lands
        loadGame.load_save_num(43)
        loadGame.load_calm()
        gameVars.setBlitzWin(True)
    if Gamestate == "Gagazet" and StepCounter == 2:  # NE armor save
        loadGame.load_save_num(57)
    if Gamestate == "Gagazet" and StepCounter == 3:  # Gagazet gates, after B&Y
        loadGame.load_save_num(138)  # Blitz Win
        # loadGame.loadSaveNum(53) # Blitz Loss
        gameVars.endGameVersionSet(4)
        loadGame.load_gagazet_gates()
    if Gamestate == "Gagazet" and StepCounter == 6:  # After the dream
        loadGame.load_save_num(98)
        gameVars.endGameVersionSet(4)
        loadGame.load_gagazet_dream()
        gameVars.fluxOverkillSuccess()
    if Gamestate == "Gagazet" and StepCounter == 10:  # Calm Lands, but Nemesis version
        loadGame.load_save_num(43)
        loadGame.load_calm()
    if Gamestate == "Gagazet" and StepCounter == 11:  # Calm Lands, but Nemesis version
        loadGame.load_save_num(64)
        FFXC.set_movement(1, 0)
        memory.main.waitFrames(60)
        FFXC.set_movement(0, 1)
        memory.main.waitFrames(60)
        FFXC.set_neutral()
        import menu

        menu.prep_calm_lands()
    if Gamestate == "Zanarkand" and StepCounter == 1:  # Intro scene revisited
        loadGame.load_save_num(99)
        gameVars.endGameVersionSet(1)
        gameVars.fluxOverkillSuccess()
        gameVars.endGameVersionSet(4)
    if Gamestate == "Zanarkand" and StepCounter == 2:  # Just before the trials.
        loadGame.load_offset(35)
        loadGame.zan_trials()
        gameVars.endGameVersionSet(4)
    if Gamestate == "Zanarkand" and StepCounter == 3:  # After trials, before boss
        loadGame.load_save_num(45)
        gameVars.endGameVersionSet(4)
    if Gamestate == "Zanarkand" and StepCounter == 4:  # After Sanctuary Keeper
        loadGame.load_save_num(44)
        gameVars.endGameVersionSet(4)
    if Gamestate == "Zanarkand" and StepCounter == 5:  # After Yunalesca
        loadGame.load_save_num(48)
        specialZanLoad = True
    if (
        Gamestate == "Sin" and StepCounter == 2
    ):  # Save sphere on the Highbridge before talking to Shedinja
        # loadGame.loadSaveNum(49)
        # Nemesis logic, double friend sphere drops from B&Y
        loadGame.load_save_num(70)
        while not memory.main.oakaGilCursor() in [8, 20]:
            if memory.main.userControl():
                import targetPathing

                targetPathing.set_movement([-251, 340])
            else:
                FFXC.set_neutral()
            xbox.menuB()
        memory.main.checkNEArmor()
    if Gamestate == "Sin" and StepCounter == 3:  # Start of "Sea of Sorrows" section
        loadGame.load_save_num(50)
    if Gamestate == "Sin" and StepCounter == 4:  # Before point of no return
        # This save has zombiestrike weapons for all except Kimahri
        # Please use for egg hunt and zombie weapon testing.
        loadGame.load_save_num(51)
        gameVars.setZombie(5)
        loadGame.load_egg_hunt()

    # Nemesis run loads
    if Gamestate == "Nem_Farm" and StepCounter == 1:
        loadGame.load_save_num(66)
    if Gamestate == "Nem_Farm" and StepCounter == 2:
        loadGame.load_save_num(69)
    if Gamestate == "Nem_Farm" and StepCounter == 3:
        loadGame.load_save_num(84)
        gameVars.setNemCheckpointAP(3)  # See nemesis.menu
        # import nemesis.arenaPrep
        nemesis.arenaPrep.arenaReturn()
    if Gamestate == "Nem_Farm" and StepCounter == 5:
        loadGame.load_save_num(71)
    if Gamestate == "Nem_Farm" and StepCounter == 6:
        loadGame.load_save_num(72)
        gameVars.setNemCheckpointAP(2)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and StepCounter == 8:
        loadGame.load_save_num(73)
    if Gamestate == "Nem_Farm" and StepCounter == 9:
        loadGame.load_save_num(75)
        gameVars.setNemCheckpointAP(3)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and StepCounter == 13:
        loadGame.load_save_num(116)
        gameVars.setNemCheckpointAP(7)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and StepCounter == 14:
        loadGame.load_save_num(76)
        gameVars.setNemCheckpointAP(10)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and StepCounter == 16:
        loadGame.load_save_num(113)
        gameVars.setNemCheckpointAP(12)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and StepCounter == 17:
        loadGame.load_save_num(111)
        gameVars.setNemCheckpointAP(14)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and StepCounter == 18:
        loadGame.load_save_num(114)
        gameVars.setNemCheckpointAP(15)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and StepCounter == 19:  # Gagazet
        loadGame.load_save_num(115)
        gameVars.setNemCheckpointAP(19)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and StepCounter == 21:
        loadGame.load_save_num(79)
        nemesis.arenaPrep.arenaReturn()
        gameVars.setNemCheckpointAP(27)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and StepCounter == 22:
        loadGame.load_save_num(82)
        # import nemesis.menu
        # nemesis.menu.rikkuHaste()
        gameVars.setNemCheckpointAP(24)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and StepCounter == 23:
        loadGame.load_save_num(80)
        gameVars.setNemCheckpointAP(30)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and StepCounter == 24:
        loadGame.load_save_num(81)
        gameVars.setNemCheckpointAP(30)
        gameVars.setNemCheckpointAP(30)  # See nemesis.menu
    if Gamestate == "Nem_Farm" and StepCounter == 20:
        loadGame.load_save_num(85)
        gameVars.setNemCheckpointAP(30)
    if Gamestate == "Nem_Farm":
        memory.main.checkNEArmor()
    memory.main.checkNEArmor()

rikkuCharged = 0
blitzLoops = 0

while Gamestate != "End":

    try:
        # Blitzball testing logic
        if Gamestate == "Luca" and StepCounter == 3:
            area.dreamZan.NewGame(Gamestate)
            loadGame.load_save_num(37)

        if rngSeedNum >= 256:
            Gamestate = "End"

        # Start of the game, start of Dream Zanarkand section
        if Gamestate == "none" and StepCounter == 1:
            report_gamestate()
            print("New Game 1 function initiated.")
            area.dreamZan.NewGame(Gamestate)
            print("New Game 1 function complete.")
            gameVars.setNewGame()
            gameVars.setCSR(True)
            print("Variables initialized.")
            Gamestate = "DreamZan"
            memory.main.waitFrames(30 * 0.5)
            print("New Game 2 function initiated.")
            area.dreamZan.NewGame2()
            startTime = logs.time_stamp()
            logs.write_stats("Start time:")
            logs.write_stats(str(startTime))
            print("Timer starts now.")
            area.dreamZan.listenStory()
            # Gamestate, StepCounter = reset.midRunReset()
            # Start of the game, up through the start of Sinspawn Ammes fight
            StepCounter = 2
            area.dreamZan.ammesBattle()

        if Gamestate == "DreamZan" and StepCounter == 2:
            report_gamestate()
            battle.boss.ammes()
            StepCounter = 3
            report_gamestate()

        if Gamestate == "DreamZan" and StepCounter == 3:
            area.dreamZan.AfterAmmes()
            # Sin drops us near Baaj temple.
            Gamestate = "Baaj"
            StepCounter = 1

        if Gamestate == "Baaj" and StepCounter == 1:
            report_gamestate()
            print("Starting Baaj temple section")
            area.baaj.Entrance()
            StepCounter = 2

        if Gamestate == "Baaj" and StepCounter == 2:
            report_gamestate()
            area.baaj.Baaj_puzzle()
            StepCounter = 3

        if Gamestate == "Baaj" and StepCounter == 3:
            area.baaj.Klikk_fight()
            StepCounter = 4
            report_gamestate()

        if Gamestate == "Baaj" and StepCounter == 4:
            # Klikk fight done. Now to wait for the Al Bhed ship.
            print("Al Bhed boat part 1")
            area.baaj.ABboat1()
            StepCounter = 5

        if Gamestate == "Baaj" and StepCounter == 5:
            report_gamestate()
            area.baaj.ABswimming1()
            StepCounter = 6
            report_gamestate()

        if Gamestate == "Baaj" and StepCounter == 6:
            print("Underwater Airship section")
            area.baaj.ABswimming2()
            Gamestate = "Besaid"
            StepCounter = 1
            report_gamestate()

        if Gamestate == "Besaid" and StepCounter == 1:
            report_gamestate()
            area.besaid.Beach()
            StepCounter = 2
            report_gamestate()

        if Gamestate == "Besaid" and StepCounter == 2:
            area.besaid.trials()
            StepCounter = 3
            report_gamestate()

        if Gamestate == "Besaid" and StepCounter == 3:
            area.besaid.leaving()
            Gamestate = "Boat1"
            if memory.main.getTidusSlvl() < 3:
                print("=======================")
                print("=======================")
                print("== Under-levelled!!! ==")
                print("=======================")
                print("=======================")
                Gamestate, StepCounter = reset.mid_run_reset()
            else:
                StepCounter = 1
                report_gamestate()

        if Gamestate == "Boat1":
            report_gamestate()
            area.boats.ssLiki()
            area.kilika.arrival()
            Gamestate = "Kilika"

        if Gamestate == "Kilika" and StepCounter == 1:
            report_gamestate()
            area.kilika.forest1()
            report_gamestate()
            StepCounter = 3

        if Gamestate == "Kilika" and StepCounter == 3:
            report_gamestate()
            area.kilika.trials()
            area.kilika.trialsEnd()
            StepCounter = 4

        if Gamestate == "Kilika" and StepCounter == 4:
            report_gamestate()
            area.kilika.forest3()
            StepCounter = 5

        if Gamestate == "Kilika" and StepCounter == 5:
            report_gamestate()
            StepCounter = 1
            Gamestate = "Boat2"

        if Gamestate == "Boat2":
            report_gamestate()
            area.boats.ssWinno()
            Gamestate = "Boat3"

        if Gamestate == "Boat3":
            report_gamestate()
            area.boats.ssWinno2()
            Gamestate = "Luca"

        if Gamestate == "Luca" and StepCounter == 1:
            report_gamestate()
            area.luca.arrival()
            StepCounter = 2

        if Gamestate == "Luca" and StepCounter == 2:
            report_gamestate()
            endTime = logs.time_stamp()
            totalTime = endTime - startTime
            print("Pre-Blitz time:", str(totalTime))
            logs.write_stats("Pre Blitz time:")
            logs.write_stats(totalTime)
            StepCounter = 3

        if Gamestate == "Luca" and StepCounter == 3:
            report_gamestate()
            area.luca.blitzStart()
            StepCounter = 4

        if Gamestate == "Luca" and StepCounter == 4:
            report_gamestate()
            print("------Blitz Start")
            blitz.blitz_main(forceBlitzWin)
            print("------Blitz End")
            if not gameVars.csr():
                xbox.awaitSave()

            if gameVars.loopBlitz() and blitzLoops < maxLoops:
                FFXC.set_neutral()
                print("------------------------------")
                print("Resetting")
                print("------------------------------")
                screen.await_turn()
                Gamestate, StepCounter = reset.mid_run_reset()
                blitzLoops += 1
            elif gameVars.blitz_loss_reset() and not gameVars.getBlitzWin():
                FFXC.set_neutral()
                print("------------------------------")
                print("Resetting - BLITZ LOSS IS FAILED RUN!!!")
                print("------------------------------")
                screen.await_turn()
                Gamestate, StepCounter = reset.mid_run_reset()
            else:
                print("------------------------------")
                print("Post-Blitz")
                print("------------------------------")
                StepCounter = 5

        if Gamestate == "Luca" and StepCounter == 5:
            report_gamestate()
            area.luca.afterBlitz()
            StepCounter = 1
            Gamestate = "Miihen"

        # Just to make sure we set this variable somewhere.
        if Gamestate == "Miihen" and StepCounter == 1:
            report_gamestate()
            returnArray = area.miihen.arrival()
            selfDestruct = area.miihen.arrival2(
                returnArray[0], returnArray[1], returnArray[2]
            )
            StepCounter = 2

        if Gamestate == "Miihen" and StepCounter == 2:
            report_gamestate()
            area.miihen.midPoint()
            print("End of Mi'ihen mid point section.")
            area.miihen.lowRoad(returnArray[0], returnArray[1], returnArray[2])

            # Report duration at the end of Mi'ihen section for all runs.
            endTime = logs.time_stamp()
            totalTime = endTime - startTime
            print("Mi'ihen End timer is:", str(totalTime))
            logs.write_stats("Miihen End time:")
            logs.write_stats(totalTime)
            Gamestate = "MRR"
            StepCounter = 1

        if Gamestate == "MRR" and StepCounter == 1:
            report_gamestate()
            area.MRR.arrival()
            area.MRR.mainPath()
            if memory.main.gameOver():
                Gamestate = "gameOverError"
            StepCounter = 2

        if Gamestate == "MRR" and StepCounter == 2:
            report_gamestate()
            area.MRR.battleSite()
            area.MRR.guiAndAftermath()
            endTime = logs.time_stamp()
            totalTime = endTime - startTime
            print("End of Battle Site timer is:", str(totalTime))
            logs.write_stats("Djose-Start time:")
            logs.write_stats(totalTime)
            Gamestate = "Djose"
            StepCounter = 1

        if Gamestate == "Djose" and StepCounter == 1:
            report_gamestate()
            area.djose.path()
            StepCounter = 2

        if Gamestate == "Djose" and StepCounter == 2:
            report_gamestate()
            area.djose.temple()
            area.djose.trials()
            StepCounter = 3

        if Gamestate == "Djose" and StepCounter == 3:
            report_gamestate()
            area.djose.leavingDjose()
            StepCounter = 1
            Gamestate = "Moonflow"

        if Gamestate == "Moonflow" and StepCounter == 1:
            report_gamestate()
            area.moonflow.arrival()
            area.moonflow.southBank()
            StepCounter = 2

        if Gamestate == "Moonflow" and StepCounter == 2:
            report_gamestate()
            area.moonflow.northBank()
            StepCounter = 1
            Gamestate = "Guadosalam"

        if Gamestate == "Guadosalam" and StepCounter == 1:
            report_gamestate()
            area.guadosalam.arrival()
            area.guadosalam.afterSpeech()
            StepCounter = 2

        if Gamestate == "Guadosalam" and StepCounter == 2:
            report_gamestate()
            area.guadosalam.guadoSkip()
            StepCounter = 1
            Gamestate = "ThunderPlains"

        if Gamestate == "ThunderPlains" and StepCounter == 1:
            report_gamestate()
            status = area.thunderPlains.southPathing()
            StepCounter = 2

        if Gamestate == "ThunderPlains" and StepCounter == 2:
            area.thunderPlains.agency()
            StepCounter = 3

        if Gamestate == "ThunderPlains" and StepCounter == 3:
            area.thunderPlains.northPathing()
            Gamestate = "Macalania"
            StepCounter = 1

        if Gamestate == "Macalania" and StepCounter == 1:
            report_gamestate()
            area.mWoods.arrival(False)
            StepCounter = 2

        if Gamestate == "Macalania" and StepCounter == 2:
            report_gamestate()
            area.mWoods.lakeRoad()
            area.mWoods.lakeRoad2()
            StepCounter = 3

        if Gamestate == "Macalania" and StepCounter == 3:
            report_gamestate()
            area.mWoods.lake()
            area.mTemple.approach()
            StepCounter = 4

        if Gamestate == "Macalania" and StepCounter == 4:
            report_gamestate()
            area.mTemple.arrival()
            area.mTemple.startSeymourFight()
            area.mTemple.seymourFight()
            StepCounter = 5

        if Gamestate == "Macalania" and StepCounter == 5:
            report_gamestate()
            area.mTemple.trials()
            StepCounter = 6

        if Gamestate == "Macalania" and StepCounter == 6:
            report_gamestate()
            area.mTemple.escape()
            StepCounter = 7

        if Gamestate == "Macalania" and StepCounter == 7:
            area.mTemple.underLake()
            StepCounter = 1
            Gamestate = "Home"

        if Gamestate == "Home" and StepCounter == 1:
            report_gamestate()
            area.home.desert()
            StepCounter = 2

        if Gamestate == "Home" and StepCounter == 2:
            report_gamestate()
            area.home.findSummoners()
            StepCounter = 1
            Gamestate = "rescueYuna"

        if Gamestate == "rescueYuna" and StepCounter == 1:
            report_gamestate()
            area.rescueYuna.preEvrae()
            battle.boss.evrae()
            area.rescueYuna.guards()
            StepCounter = 2

        if Gamestate == "rescueYuna" and StepCounter == 2:
            report_gamestate()
            area.rescueYuna.trials()
            area.rescueYuna.trialsEnd()
            StepCounter = 3

        if Gamestate == "rescueYuna" and StepCounter == 3:
            report_gamestate()
            area.rescueYuna.ViaPurifico()
            StepCounter = 4

        if Gamestate == "rescueYuna" and StepCounter == 4:
            report_gamestate()
            area.rescueYuna.evraeAltana()
            StepCounter = 5

        if Gamestate == "rescueYuna" and StepCounter == 5:
            report_gamestate()
            area.rescueYuna.seymourNatus()
            Gamestate = "Gagazet"
            if gameVars.nemesis():
                StepCounter = 10
            else:
                StepCounter = 1

        if Gamestate == "Gagazet" and StepCounter == 1:
            manipTime1 = logs.time_stamp()
            report_gamestate()
            area.gagazet.calmLands()
            area.gagazet.defenderX()
            StepCounter = 2

        if Gamestate == "Gagazet" and StepCounter == 2:
            report_gamestate()
            if gameVars.tryForNE():
                import area.neArmor

                print("Mark 1")
                area.neArmor.toHiddenCave()
                print("Mark 2")
                area.neArmor.dropHunt()
                print("Mark 3")
                area.neArmor.returnToGagazet()
            manipTime2 = logs.time_stamp()
            manipTime = manipTime2 - manipTime1
            print("NEA Manip duration:", str(manipTime))
            logs.write_stats("NEA Manip duration:")
            logs.write_stats(manipTime)
            StepCounter = 3

        if Gamestate == "Gagazet" and StepCounter == 3:
            report_gamestate()
            area.gagazet.toTheRonso()
            area.gagazet.gagazetGates()
            StepCounter = 4

        if Gamestate == "Gagazet" and StepCounter == 4:
            report_gamestate()
            area.gagazet.Flux()
            StepCounter = 5

        if Gamestate == "Gagazet" and StepCounter == 5:
            report_gamestate()
            area.gagazet.dream()
            StepCounter = 6

        if Gamestate == "Gagazet" and StepCounter == 6:
            report_gamestate()
            area.gagazet.cave()
            area.gagazet.wrapUp()
            StepCounter = 1
            Gamestate = "Zanarkand"

        if Gamestate == "Zanarkand" and StepCounter == 1:
            report_gamestate()
            area.zanarkand.arrival()
            StepCounter = 2

        if Gamestate == "Zanarkand" and StepCounter == 2:
            report_gamestate()
            area.zanarkand.trials()
            StepCounter = 3

        if Gamestate == "Zanarkand" and StepCounter == 3:
            report_gamestate()
            area.zanarkand.sanctuaryKeeper()
            StepCounter = 4

        if Gamestate == "Zanarkand" and StepCounter == 4:
            report_gamestate()
            area.zanarkand.yunalesca()
            StepCounter = 5

        if Gamestate == "Zanarkand" and StepCounter == 5:
            area.zanarkand.post_Yunalesca()
            StepCounter = 1
            Gamestate = "Sin"

        if Gamestate == "Sin" and StepCounter == 1:
            report_gamestate()
            area.sin.makingPlans()
            StepCounter = 2

        if Gamestate == "Sin" and StepCounter == 2:
            report_gamestate()
            print("Test 1")
            area.sin.Shedinja()
            print("Test 2")
            area.sin.facingSin()
            print("Test 3")
            if gameVars.nemesis():
                Gamestate = "Nem_Farm"
                StepCounter = 1
            else:
                StepCounter = 3

        if Gamestate == "Sin" and StepCounter == 3:
            report_gamestate()
            area.sin.insideSin()
            StepCounter = 4

        if Gamestate == "Sin" and StepCounter == 4:
            area.sin.eggHunt(autoEggHunt)
            if gameVars.nemesis():
                battle.main.BFA_nem()
            else:
                battle.boss.BFA()
                battle.boss.yuYevon()
            Gamestate = "End"

        # Nemesis logic only:
        if Gamestate == "Gagazet" and StepCounter == 10:
            nemesis.changes.calmLands_1()
            StepCounter = 12

        if Gamestate == "Gagazet" and StepCounter == 11:
            nemesis.changes.remiemRaces()
            StepCounter += 1

        if Gamestate == "Gagazet" and StepCounter == 12:
            print("MAAAAARK")
            memory.main.awaitControl()
            nemesis.changes.arenaPurchase()
            area.gagazet.defenderX()
            StepCounter = 2

        if Gamestate == "Nem_Farm" and StepCounter == 1:
            report_gamestate()
            nemesis.arenaPrep.transition()
            while not nemesis.arenaPrep.tPlains(capNum=1):
                pass
            StepCounter = 2

        if Gamestate == "Nem_Farm" and StepCounter == 2:
            report_gamestate()
            while not nemesis.arenaPrep.calm(capNum=1, airshipReturn=False):
                pass
            StepCounter = 3

        if Gamestate == "Nem_Farm" and StepCounter == 3:
            report_gamestate()
            nemesis.arenaPrep.kilikaShop()
            StepCounter = 4

        if Gamestate == "Nem_Farm" and StepCounter == 4:
            report_gamestate()
            nemesis.arenaPrep.besaidFarm(capNum=1)
            StepCounter = 5

        if Gamestate == "Nem_Farm" and StepCounter == 5:
            report_gamestate()
            nemesis.arenaPrep.kilikaFarm(capNum=1)
            StepCounter = 6

        if Gamestate == "Nem_Farm" and StepCounter == 6:
            report_gamestate()
            nemesis.arenaPrep.miihenFarm(capNum=1)
            StepCounter = 7

        if Gamestate == "Nem_Farm" and StepCounter == 7:
            # reportGamestate()
            # nemesis.arenaPrep.mrrFarm(capNum=1)
            StepCounter = 8

        if Gamestate == "Nem_Farm" and StepCounter == 8:
            report_gamestate()
            nemesis.arenaPrep.odToAP()
            StepCounter = 9

        if Gamestate == "Nem_Farm" and StepCounter == 9:
            report_gamestate()
            nemesis.arenaPrep.besaidFarm(capNum=10)
            StepCounter = 10

        if Gamestate == "Nem_Farm" and StepCounter == 10:
            report_gamestate()
            nemesis.arenaPrep.kilikaFarm(capNum=10)
            StepCounter = 11

        if Gamestate == "Nem_Farm" and StepCounter == 11:
            report_gamestate()
            nemesis.arenaPrep.miihenFarm(capNum=10)
            StepCounter = 12

        if Gamestate == "Nem_Farm" and StepCounter == 12:
            # reportGamestate()
            # nemesis.arenaPrep.mrrFarm(capNum=10)
            StepCounter = 13

        if Gamestate == "Nem_Farm" and StepCounter == 13:
            report_gamestate()
            nemesis.arenaPrep.djoseFarm(capNum=10)
            StepCounter = 14

        if Gamestate == "Nem_Farm" and StepCounter == 14:
            report_gamestate()
            nemesis.arenaPrep.tPlains(capNum=10, autoHaste=True)
            StepCounter = 15

        if Gamestate == "Nem_Farm" and StepCounter == 15:
            report_gamestate()
            nemesis.arenaPrep.bikanel(capNum=10)
            StepCounter = 16

        if Gamestate == "Nem_Farm" and StepCounter == 16:
            report_gamestate()
            nemesis.arenaPrep.arenaReturn()
            nemesis.arenaPrep.autoPhoenix()
            StepCounter = 17

        if Gamestate == "Nem_Farm" and StepCounter == 17:
            report_gamestate()
            nemesis.arenaPrep.macWoods(capNum=10)
            StepCounter = 18

        if Gamestate == "Nem_Farm" and StepCounter == 18:
            report_gamestate()
            nemesis.arenaPrep.stolenFaythCave()
            StepCounter = 19

        if Gamestate == "Nem_Farm" and StepCounter == 19:
            report_gamestate()
            nemesis.arenaPrep.gagazet()
            # nemesis.arenaPrep.gagazet1()
            # nemesis.arenaPrep.gagazet2()
            # nemesis.arenaPrep.gagazet3()
            # Gamestate = "End" #Testing only
            StepCounter = 20

        if Gamestate == "Nem_Farm" and StepCounter == 20:
            report_gamestate()
            nemesis.arenaPrep.calm(capNum=10, airshipReturn=False, forceLevels=27)
            StepCounter = 21

        if Gamestate == "Nem_Farm" and StepCounter == 21:
            report_gamestate()
            nemesis.arenaPrep.oneMpWeapon()
            StepCounter = 22

        if Gamestate == "Nem_Farm" and StepCounter == 22:
            report_gamestate()
            nemesis.arenaPrep.insideSin(capNum=10)
            StepCounter = 23

        if Gamestate == "Nem_Farm" and StepCounter == 23:
            report_gamestate()
            nemesis.arenaPrep.unlockOmega()
            nemesis.arenaPrep.omegaRuins()
            StepCounter = 24

        if Gamestate == "Nem_Farm" and StepCounter == 24:
            nemesis.arenaPrep.kilikaFinalShop()
            StepCounter = 25

        if Gamestate == "Nem_Farm" and StepCounter == 25:
            nemesis.arenaPrep.arenaReturn()
            nemesis.arenaPrep.finalWeapon()
            Gamestate = "Nem_Arena"
            StepCounter = 1

        if Gamestate == "Nem_Arena" and StepCounter == 1:
            nemesis.arenaBattles.battles1()
            gameVars.printArenaStatus()
            StepCounter = 2

        if Gamestate == "Nem_Arena" and StepCounter == 2:
            nemesis.arenaBattles.battles2()
            gameVars.printArenaStatus()
            StepCounter = 3

        if Gamestate == "Nem_Arena" and StepCounter == 3:
            nemesis.arenaBattles.juggernautFarm()
            gameVars.printArenaStatus()
            StepCounter = 4

        if Gamestate == "Nem_Arena" and StepCounter == 4:
            nemesis.arenaBattles.battles3()
            gameVars.printArenaStatus()
            StepCounter = 5

        if Gamestate == "Nem_Arena" and StepCounter == 5:
            nemesis.arenaBattles.battles4()
            gameVars.printArenaStatus()
            StepCounter = 6

        if Gamestate == "Nem_Arena" and StepCounter == 6:
            nemesis.arenaBattles.nemesisBattle()
            StepCounter = 7

        if Gamestate == "Nem_Arena" and StepCounter == 7:
            nemesis.arenaBattles.returnToSin()
            Gamestate = "Sin"
            StepCounter = 3

        if (
            Gamestate == "End"
            and gameVars.loopSeeds()
            and rngSeedNum - rngSeedOrig < maxLoops
        ):
            # End of seed logic.
            Gamestate, StepCounter = reset.mid_run_reset(
                land_run=True, start_time=startTime
            )

        print("------------------------------")
        print("Looping")
        print(Gamestate, "|", StepCounter)
        print("------------------------------")

    except KeyboardInterrupt:
        print("Keyboard Interrupt - Exiting.")
        sys.exit(0)

print("Time! The game is now over.")

endTime = logs.time_stamp()

if memory.main.getStoryProgress() > 3210:
    totalTime = endTime - startTime
    logs.write_stats("Total time:")
    logs.write_stats(str(totalTime))
    print("The game duration was:", str(totalTime))
    print(
        "This duration is intended for comparison reference only, not as a true timer."
    )
    print("Please do not use this as your submitted time.")
    memory.main.waitFrames(30)
    print("--------")
    print("In order to conform with speedrun standards,")
    memory.main.waitFrames(60)
    print("we now wait until the end of the credits and stuff")
    memory.main.waitFrames(60)
    print("and then will open up the list of saves.")
    memory.main.waitFrames(60)
    print("This will show the autosave values, which conforms to the speedrun rules.")

    while memory.main.getMap() != 23:
        if memory.main.getMap() in [348, 349]:
            xbox.tapStart()
        elif memory.main.cutsceneSkipPossible():
            xbox.skipScene()
    memory.main.waitFrames(180)
    while not memory.main.saveMenuOpen():
        xbox.tapB()

memory.main.end()

print("Automation complete. Shutting down now. Have a great day!")
