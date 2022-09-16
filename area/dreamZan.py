import xbox
import battle
import memory
import targetPathing
import vars
import logs
import rngTrack
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def NewGame(Gamestate):
    print("Starting the game")
    print("Gamestate:", Gamestate)

    lastMessage = 0
    # New version
    if Gamestate == 'none':  # New Game
        while memory.getMap() != 0:
            if memory.getMap() != 23:
                if lastMessage != 1:
                    lastMessage = 1
                    print("Attempting to get to New Game screen")
                FFXC.set_value('BtnStart', 1)
                memory.waitFrames(1)
                FFXC.set_value('BtnStart', 0)
                memory.waitFrames(1)
            elif memory.saveMenuOpen():
                if lastMessage != 2:
                    lastMessage = 2
                    print("Load Game menu is open. Backing out.")
                xbox.tapA()
            elif memory.saveMenuCursor() == 1:
                if lastMessage != 3:
                    lastMessage = 3
                    print("New Game is not selected. Switching.")
                xbox.menuUp()
            else:
                if lastMessage != 4:
                    lastMessage = 4
                    print("New Game is selected. Starting game.")
                xbox.menuB()
        memory.clickToDiagProgress(7)
    else:  # Load Game
        while not memory.saveMenuOpen():
            if memory.getMap() != 23:
                FFXC.set_value('BtnStart', 1)
                memory.waitFrames(1)
                FFXC.set_value('BtnStart', 0)
                memory.waitFrames(1)
            elif memory.saveMenuCursor() == 0:
                xbox.menuDown()
            else:
                xbox.menuB()


def NewGame2():
    # New game selected. Next, select options.
    timeBuffer = 17
    print("====================================")
    print("Countdown timer!!!")
    memory.waitFrames(timeBuffer)
    print("5")
    memory.waitFrames(timeBuffer)
    print("4")
    memory.waitFrames(timeBuffer)
    print("3")
    memory.waitFrames(timeBuffer)
    print("2")
    memory.waitFrames(timeBuffer)
    print("1")
    memory.waitFrames(timeBuffer)
    print("GO!!! Good fortune!")
    print("====================================")
    print("Reminder seed number:", memory.rngSeed())
    xbox.menuB()
    xbox.menuB()


def listenStory():
    memory.waitFrames(10)
    vars.initVars()
    while not memory.userControl():
        if memory.getMap() == 132:
            if memory.diagProgressFlag() == 1:
                gameVars.setCSR(False)
                print("Skipping intro scene, we'll watch this properly in about 8 hours.")
                memory.awaitControl()
            FFXC.set_value('BtnBack', 1)
            memory.waitFrames(1)
            FFXC.set_value('BtnBack', 0)
            memory.waitFrames(1)

    print("### CSR check:", gameVars.csr())
    checkpoint = 0
    while memory.getEncounterID() != 414:  # Sinspawn Ammes
        if memory.userControl():
            # Events
            if checkpoint == 5:
                FFXC.set_movement(0, -1)
                while memory.userControl():
                    xbox.tapB()
                FFXC.set_neutral()

                # Name Tidus
                xbox.nameAeon("Tidus")

                checkpoint += 1
            elif checkpoint == 7 and gameVars.csr():
                checkpoint = 9
            elif checkpoint == 8:
                while memory.userControl():
                    FFXC.set_movement(1, 0)
                    xbox.tapB()
                FFXC.set_neutral()
                memory.awaitControl()
                print("Done clicking")
                checkpoint += 1
            elif checkpoint < 11 and memory.getStoryProgress() >= 5:
                checkpoint = 11
            elif checkpoint < 21 and memory.getMap() == 371:
                checkpoint = 21
            elif checkpoint < 25 and memory.getMap() == 370:
                checkpoint = 25
            elif checkpoint == 27:  # Don't cry.
                while memory.userControl():
                    FFXC.set_movement(1, -1)
                FFXC.set_neutral()
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.tidusHome(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()
            elif memory.cutsceneSkipPossible():
                if memory.getStoryProgress() == 10 and memory.diagProgressFlag() == 2:
                    print("Special Skip")
                    memory.waitFrames(130)
                    # Generate button to skip later
                    FFXC.set_value('BtnStart', 1)
                    memory.waitFrames(1)
                    FFXC.set_value('BtnStart', 0)
                    xbox.SkipDialog(10)
                else:
                    if gameVars.usePause():
                        memory.waitFrames(1)
                    xbox.skipScene(fast_mode=True)
                    xbox.SkipDialog(3)


def ammesBattle():
    print("Starting ammes")
    xbox.clickToBattle()
    memory.lastHitInit()
    battle.defend()
    # logs.writeStats("First Six Hits:")
    hitsArray = []

    print("Killing Sinspawn")
    while memory.battleActive():
        if memory.turnReady():
            battle.attack('none')
            lastHit = memory.lastHitCheckChange()
            while lastHit == 9999:
                lastHit = memory.lastHitCheckChange()
            print("Confirm - last hit: ", lastHit)
            hitsArray.append(lastHit)
            print(hitsArray)
    print("#####################################")
    print("### Unconfirmed seed check:", memory.rngSeed())
    correctSeed = rngTrack.hitsToSeed(hitsArray=hitsArray)
    logs.writeStats("Corrected RNG seed:")
    logs.writeStats(correctSeed)
    print("### Corrected RNG seed:", correctSeed)
    if correctSeed != "Err_seed_not_found":
        gameVars.setConfirmedSeed(correctSeed)
    print("Confirming RNG seed: ", memory.rngSeed())
    print("#####################################")
    print("Done Killing Sinspawn")
    memory.waitFrames(6)  # Just for no overlap
    print("Clicking to battle.")
    xbox.clickToBattle()
    print("Waiting for Auron's Turn")
    print("At Overdrive")
    # Auron overdrive tutorial
    battle.auronOD()


def AfterAmmes():
    memory.clickToControl()
    checkpoint = 0

    while memory.getMap() != 49:
        if memory.userControl():
            # Map changes and events
            if checkpoint == 6:  # Save sphere
                memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint < 9 and memory.getStoryProgress() >= 20:  # Swim to Jecht
                checkpoint = 9
            elif checkpoint < 11 and memory.getStoryProgress() >= 30:  # Towards Baaj temple
                checkpoint = 11

            # General pathing
            elif targetPathing.setMovement(targetPathing.allStartsHere(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.turnReady():
                battle.Tanker()
            if memory.diagSkipPossible():
                xbox.tapB()
            elif memory.cutsceneSkipPossible():
                xbox.skipStoredScene(3)


def SwimToJecht():
    print("Swimming to Jecht")

    FFXC.set_value('BtnA', 1)
    FFXC.set_movement(-1, -1)
    memory.waitFrames(30 * 8)
    while memory.userControl():
        FFXC.set_movement(-1, 1)

    FFXC.set_neutral()
    FFXC.set_value('BtnA', 0)
    print("We've now reached Jecht.")
    xbox.SkipDialog(5)

    # Next, swim to Baaj temple
    memory.clickToControl()
    FFXC.set_movement(1, 0)
    memory.waitFrames(30 * 1)
    FFXC.set_movement(1, 1)
    memory.waitFrames(30 * 0.6)
    FFXC.set_movement(0, 1)
    memory.waitFrames(30 * 5)
    FFXC.set_movement(-1, 1)
    memory.waitFrames(30 * 1)
    FFXC.set_movement(0, 1)
    memory.waitFrames(30 * 14)
    FFXC.set_movement(-1, 1)
    memory.waitFrames(30 * 1.5)  # Line up with stairs

    FFXC.set_movement(0, 1)
    memory.waitFrames(30 * 3)

    while memory.getMap() == 48:
        pos = memory.getCoords()
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
    memory.waitFrames(30 * 0.3)
