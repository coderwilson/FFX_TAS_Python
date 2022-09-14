import FFX_Xbox
import FFX_Battle
import FFX_memory
import FFX_targetPathing
import FFX_vars
import FFX_Logs
import FFX_rngTrack
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()


def NewGame(Gamestate):
    print("Starting the game")
    print("Gamestate:", Gamestate)

    lastMessage = 0
    # New version
    if Gamestate == 'none':  # New Game
        while FFX_memory.getMap() != 0:
            if FFX_memory.getMap() != 23:
                if lastMessage != 1:
                    lastMessage = 1
                    print("Attempting to get to New Game screen")
                FFXC.set_value('BtnStart', 1)
                FFX_memory.waitFrames(1)
                FFXC.set_value('BtnStart', 0)
                FFX_memory.waitFrames(1)
            elif FFX_memory.saveMenuOpen():
                if lastMessage != 2:
                    lastMessage = 2
                    print("Load Game menu is open. Backing out.")
                FFX_Xbox.tapA()
            elif FFX_memory.saveMenuCursor() == 1:
                if lastMessage != 3:
                    lastMessage = 3
                    print("New Game is not selected. Switching.")
                FFX_Xbox.menuUp()
            else:
                if lastMessage != 4:
                    lastMessage = 4
                    print("New Game is selected. Starting game.")
                FFX_Xbox.menuB()
        FFX_memory.clickToDiagProgress(7)
    else:  # Load Game
        while not FFX_memory.saveMenuOpen():
            if FFX_memory.getMap() != 23:
                FFXC.set_value('BtnStart', 1)
                FFX_memory.waitFrames(1)
                FFXC.set_value('BtnStart', 0)
                FFX_memory.waitFrames(1)
            elif FFX_memory.saveMenuCursor() == 0:
                FFX_Xbox.menuDown()
            else:
                FFX_Xbox.menuB()


def NewGame2():
    # New game selected. Next, select options.
    timeBuffer = 17
    print("====================================")
    print("Countdown timer!!!")
    FFX_memory.waitFrames(timeBuffer)
    print("5")
    FFX_memory.waitFrames(timeBuffer)
    print("4")
    FFX_memory.waitFrames(timeBuffer)
    print("3")
    FFX_memory.waitFrames(timeBuffer)
    print("2")
    FFX_memory.waitFrames(timeBuffer)
    print("1")
    FFX_memory.waitFrames(timeBuffer)
    print("GO!!! Good fortune!")
    print("====================================")
    print("Reminder seed number:", FFX_memory.rngSeed())
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()


def listenStory():
    FFX_memory.waitFrames(10)
    FFX_vars.initVars()
    while not FFX_memory.userControl():
        if FFX_memory.getMap() == 132:
            if FFX_memory.diagProgressFlag() == 1:
                gameVars.setCSR(False)
                print("Skipping intro scene, we'll watch this properly in about 8 hours.")
                FFX_memory.awaitControl()
            FFXC.set_value('BtnBack', 1)
            FFX_memory.waitFrames(1)
            FFXC.set_value('BtnBack', 0)
            FFX_memory.waitFrames(1)

    print("### CSR check:", gameVars.csr())
    checkpoint = 0
    while FFX_memory.getEncounterID() != 414:  # Sinspawn Ammes
        if FFX_memory.userControl():
            # Events
            if checkpoint == 5:
                FFXC.set_movement(0, -1)
                while FFX_memory.userControl():
                    FFX_Xbox.tapB()
                FFXC.set_neutral()

                # Name Tidus
                FFX_Xbox.nameAeon("Tidus")

                checkpoint += 1
            elif checkpoint == 7 and gameVars.csr():
                checkpoint = 9
            elif checkpoint == 8:
                while FFX_memory.userControl():
                    FFXC.set_movement(1, 0)
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                FFX_memory.awaitControl()
                print("Done clicking")
                checkpoint += 1
            elif checkpoint < 11 and FFX_memory.getStoryProgress() >= 5:
                checkpoint = 11
            elif checkpoint < 21 and FFX_memory.getMap() == 371:
                checkpoint = 21
            elif checkpoint < 25 and FFX_memory.getMap() == 370:
                checkpoint = 25
            elif checkpoint == 27:  # Don't cry.
                while FFX_memory.userControl():
                    FFXC.set_movement(1, -1)
                FFXC.set_neutral()
                checkpoint += 1

            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.tidusHome(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            elif FFX_memory.cutsceneSkipPossible():
                if FFX_memory.getStoryProgress() == 10 and FFX_memory.diagProgressFlag() == 2:
                    print("Special Skip")
                    FFX_memory.waitFrames(130)
                    # Generate button to skip later
                    FFXC.set_value('BtnStart', 1)
                    FFX_memory.waitFrames(1)
                    FFXC.set_value('BtnStart', 0)
                    FFX_Xbox.SkipDialog(10)
                else:
                    if gameVars.usePause():
                        FFX_memory.waitFrames(1)
                    FFX_Xbox.skipScene(fast_mode=True)
                    FFX_Xbox.SkipDialog(3)


def ammesBattle():
    print("Starting ammes")
    FFX_Xbox.clickToBattle()
    FFX_memory.lastHitInit()
    FFX_Battle.defend()
    FFX_Logs.writeStats("First Six Hits:")
    hitsArray = []

    print("Killing Sinspawn")
    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            FFX_Battle.attack('none')
            lastHit = FFX_memory.lastHitCheckChange()
            while lastHit == 9999:
                lastHit = FFX_memory.lastHitCheckChange()
            print("Confirm - last hit: ", lastHit)
            hitsArray.append(lastHit)
            print(hitsArray)
    print("#####################################")
    print("### Unconfirmed seed check:", FFX_memory.rngSeed())
    correctSeed = FFX_rngTrack.hitsToSeed(hitsArray=hitsArray)
    FFX_Logs.writeStats("Corrected RNG seed:")
    FFX_Logs.writeStats(correctSeed)
    print("### Corrected RNG seed:", correctSeed)
    if correctSeed != "Err_seed_not_found":
        gameVars.setConfirmedSeed(correctSeed)
    print("Confirming RNG seed: ", FFX_memory.rngSeed())
    print("#####################################")
    print("Done Killing Sinspawn")
    FFX_memory.waitFrames(6)  # Just for no overlap
    print("Clicking to battle.")
    FFX_Xbox.clickToBattle()
    print("Waiting for Auron's Turn")
    print("At Overdrive")
    # Auron overdrive tutorial
    FFX_Battle.auronOD()


def AfterAmmes():
    FFX_memory.clickToControl()
    checkpoint = 0

    while FFX_memory.getMap() != 49:
        if FFX_memory.userControl():
            # Map changes and events
            if checkpoint == 6:  # Save sphere
                FFX_memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint < 9 and FFX_memory.getStoryProgress() >= 20:  # Swim to Jecht
                checkpoint = 9
            elif checkpoint < 11 and FFX_memory.getStoryProgress() >= 30:  # Towards Baaj temple
                checkpoint = 11

            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.allStartsHere(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.turnReady():
                FFX_Battle.Tanker()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            elif FFX_memory.cutsceneSkipPossible():
                FFX_Xbox.skipStoredScene(3)


def SwimToJecht():
    print("Swimming to Jecht")

    FFXC.set_value('BtnA', 1)
    FFXC.set_movement(-1, -1)
    FFX_memory.waitFrames(30 * 8)
    while FFX_memory.userControl():
        FFXC.set_movement(-1, 1)

    FFXC.set_neutral()
    FFXC.set_value('BtnA', 0)
    print("We've now reached Jecht.")
    FFX_Xbox.SkipDialog(5)

    # Next, swim to Baaj temple
    FFX_memory.clickToControl()
    FFXC.set_movement(1, 0)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_movement(1, 1)
    FFX_memory.waitFrames(30 * 0.6)
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 5)
    FFXC.set_movement(-1, 1)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 14)
    FFXC.set_movement(-1, 1)
    FFX_memory.waitFrames(30 * 1.5)  # Line up with stairs

    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 3)

    while FFX_memory.getMap() == 48:
        pos = FFX_memory.getCoords()
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
    FFX_memory.waitFrames(30 * 0.3)
