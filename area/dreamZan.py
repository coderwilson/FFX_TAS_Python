import battle.main
import logs
import memory.main
import rngTrack
import targetPathing
import vars
import xbox

gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def NewGame(Gamestate):
    print("Starting the game")
    print("Gamestate:", Gamestate)

    lastMessage = 0
    # New version
    if Gamestate == 'none':  # New Game
        while memory.main.getMap() != 0:
            if memory.main.getMap() != 23:
                if lastMessage != 1:
                    lastMessage = 1
                    print("Attempting to get to New Game screen")
                FFXC.set_value('BtnStart', 1)
                memory.main.waitFrames(1)
                FFXC.set_value('BtnStart', 0)
                memory.main.waitFrames(1)
            elif memory.main.saveMenuOpen():
                if lastMessage != 2:
                    lastMessage = 2
                    print("Load Game menu is open. Backing out.")
                xbox.tapA()
            elif memory.main.saveMenuCursor() == 1:
                if lastMessage != 3:
                    lastMessage = 3
                    print("New Game is not selected. Switching.")
                xbox.menuUp()
            else:
                if lastMessage != 4:
                    lastMessage = 4
                    print("New Game is selected. Starting game.")
                xbox.menuB()
        memory.main.clickToDiagProgress(7)
    else:  # Load Game
        while not memory.main.saveMenuOpen():
            if memory.main.getMap() != 23:
                FFXC.set_value('BtnStart', 1)
                memory.main.waitFrames(1)
                FFXC.set_value('BtnStart', 0)
                memory.main.waitFrames(1)
            elif memory.main.saveMenuCursor() == 0:
                xbox.menuDown()
            else:
                xbox.menuB()


def NewGame2():
    # New game selected. Next, select options.
    timeBuffer = 17
    print("====================================")
    print("Countdown timer!!!")
    memory.main.waitFrames(timeBuffer)
    print("5")
    memory.main.waitFrames(timeBuffer)
    print("4")
    memory.main.waitFrames(timeBuffer)
    print("3")
    memory.main.waitFrames(timeBuffer)
    print("2")
    memory.main.waitFrames(timeBuffer)
    print("1")
    memory.main.waitFrames(timeBuffer)
    print("GO!!! Good fortune!")
    print("====================================")
    print("Reminder seed number:", memory.main.rngSeed())
    xbox.menuB()
    xbox.menuB()


def listenStory():
    memory.main.waitFrames(10)
    vars.initVars()
    while not memory.main.userControl():
        if memory.main.getMap() == 132:
            if memory.main.diagProgressFlag() == 1:
                gameVars.setCSR(False)
                print("Skipping intro scene, we'll watch this properly in about 8 hours.")
                memory.main.awaitControl()
            FFXC.set_value('BtnBack', 1)
            memory.main.waitFrames(1)
            FFXC.set_value('BtnBack', 0)
            memory.main.waitFrames(1)

    print("### CSR check:", gameVars.csr())
    checkpoint = 0
    while memory.main.getEncounterID() != 414:  # Sinspawn Ammes
        if memory.main.userControl():
            # Events
            if checkpoint == 5:
                FFXC.set_movement(0, -1)
                while not memory.main.nameAeonReady():
                    xbox.tapB()
                print("Ready to name Tidus")
                FFXC.set_neutral()
                memory.main.waitFrames(1)

                # Name Tidus
                xbox.nameAeon("Tidus")
                print("Tidus name complete.")

                checkpoint += 1
            #elif checkpoint == 7 and gameVars.csr():
            #    checkpoint = 9
            elif checkpoint == 8:
                while memory.main.userControl():
                    FFXC.set_movement(1, 0)
                    xbox.tapB()
                FFXC.set_neutral()
                memory.main.awaitControl()
                print("Done clicking")
                checkpoint += 1
            elif checkpoint < 11 and memory.main.getStoryProgress() >= 5:
                checkpoint = 11
            elif checkpoint < 21 and memory.main.getMap() == 371:
                checkpoint = 21
            elif checkpoint < 25 and memory.main.getMap() == 370:
                checkpoint = 25
            elif checkpoint == 27:  # Don't cry.
                while memory.main.userControl():
                    FFXC.set_movement(1, -1)
                FFXC.set_neutral()
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.tidusHome(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()
            elif memory.main.cutsceneSkipPossible():
                if memory.main.getStoryProgress() == 10 and memory.main.diagProgressFlag() == 2:
                    print("Special Skip")
                    memory.main.waitFrames(130)
                    # Generate button to skip later
                    FFXC.set_value('BtnStart', 1)
                    memory.main.waitFrames(1)
                    FFXC.set_value('BtnStart', 0)
                    xbox.SkipDialog(10)
                else:
                    if gameVars.usePause():
                        memory.main.waitFrames(1)
                    xbox.skipScene(fast_mode=True)
                    xbox.SkipDialog(3)


def ammesBattle():
    print("Starting ammes")
    xbox.clickToBattle()
    memory.main.lastHitInit()
    battle.main.defend()
    # logs.writeStats("First Six Hits:")
    hitsArray = []

    print("Killing Sinspawn")
    while memory.main.battleActive():
        if memory.main.turnReady():
            battle.main.attack('none')
            lastHit = memory.main.lastHitCheckChange()
            while lastHit == 9999:
                lastHit = memory.main.lastHitCheckChange()
            print("Confirm - last hit: ", lastHit)
            hitsArray.append(lastHit)
            print(hitsArray)
    print("#####################################")
    print("### Unconfirmed seed check:", memory.main.rngSeed())
    correctSeed = rngTrack.hitsToSeed(hitsArray=hitsArray)
    logs.writeStats("Corrected RNG seed:")
    logs.writeStats(correctSeed)
    print("### Corrected RNG seed:", correctSeed)
    if correctSeed != "Err_seed_not_found":
        gameVars.setConfirmedSeed(correctSeed)
    print("Confirming RNG seed: ", memory.main.rngSeed())
    print("#####################################")
    print("Done Killing Sinspawn")
    memory.main.waitFrames(6)  # Just for no overlap
    print("Clicking to battle.")
    xbox.clickToBattle()
    print("Waiting for Auron's Turn")
    print("At Overdrive")
    # Auron overdrive tutorial
    battle.main.auronOD()


def AfterAmmes():
    memory.main.clickToControl()
    checkpoint = 0
    #memory.main.waitFrames(90)
    #print("#### MARK ####")
    #memory.main.ammesFix(actorIndex=0)
    #memory.main.waitFrames(90)

    while memory.main.getMap() != 49:
        if memory.main.userControl():
            startPos = memory.main.getCoords()
            if int(startPos[0]) in [866, 867, 868, 869, 870] \
                    and int(startPos[1]) in [-138, -139, -140, -141]:
                print("Positioning error")
                FFXC.set_neutral()
                memory.main.waitFrames(20)
                memory.main.ammesFix(actorIndex=0)
                memory.main.waitFrames(20)
            else:
                # Map changes and events
                if checkpoint == 6:  # Save sphere
                    memory.main.touchSaveSphere()
                    checkpoint += 1
                elif checkpoint < 9 and memory.main.getStoryProgress() >= 20:  # Swim to Jecht
                    checkpoint = 9
                elif checkpoint < 11 and memory.main.getStoryProgress() >= 30:  # Towards Baaj temple
                    checkpoint = 11

                # General pathing
                elif targetPathing.setMovement(targetPathing.allStartsHere(checkpoint)):
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.turnReady():
                battle.main.Tanker()
            if memory.main.diagSkipPossible():
                xbox.tapB()
            elif memory.main.cutsceneSkipPossible():
                xbox.skipStoredScene(3)


def SwimToJecht():
    print("Swimming to Jecht")

    FFXC.set_value('BtnA', 1)
    FFXC.set_movement(-1, -1)
    memory.main.waitFrames(30 * 8)
    while memory.main.userControl():
        FFXC.set_movement(-1, 1)

    FFXC.set_neutral()
    FFXC.set_value('BtnA', 0)
    print("We've now reached Jecht.")
    xbox.SkipDialog(5)

    # Next, swim to Baaj temple
    memory.main.clickToControl()
    FFXC.set_movement(1, 0)
    memory.main.waitFrames(30 * 1)
    FFXC.set_movement(1, 1)
    memory.main.waitFrames(30 * 0.6)
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 5)
    FFXC.set_movement(-1, 1)
    memory.main.waitFrames(30 * 1)
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 14)
    FFXC.set_movement(-1, 1)
    memory.main.waitFrames(30 * 1.5)  # Line up with stairs

    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 3)

    while memory.main.getMap() == 48:
        pos = memory.main.getCoords()
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
    memory.main.waitFrames(30 * 0.3)
