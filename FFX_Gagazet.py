import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory
import FFX_targetPathing
import FFX_vars
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC


def checkGems():
    gemSlot = FFX_memory.getItemSlot(34)
    if gemSlot < 200:
        gems = FFX_memory.getItemCountSlot(gemSlot)
    else:
        gems = 0

    gemSlot = FFX_memory.getItemSlot(28)
    if gemSlot < 200:
        gems += FFX_memory.getItemCountSlot(gemSlot)
    print("Total gems:", gems)
    return gems


def calmLands():
    FFX_memory.awaitControl()
    # Start by getting away from the save sphere
    if FFX_memory.nextChanceRNG10() >= 6:
        FFX_memory.fullPartyFormat('rikku', fullMenuClose=False)
    else:
        FFX_memory.fullPartyFormat('kimahri', fullMenuClose=False)
    FFX_Battle.healUp(fullMenuClose=True)

    FFX_memory.printManipInfo()
    print("RNG10:", FFX_memory.rng10())
    print("RNG12:", FFX_memory.rng12())
    print("RNG13:", FFX_memory.rng13())
    # Enter the cutscene where Yuna muses about ending her journey.
    while not (FFX_memory.getCoords()[1] >= -1650 and FFX_memory.userControl()):
        if FFX_memory.userControl():
            FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

    checkpoint = 0
    while FFX_memory.getMap() != 279:
        if FFX_memory.userControl():
            if FFX_targetPathing.setMovement(FFX_targetPathing.calmLands(checkpoint)) == True:
                checkpoint += 1
                if checkpoint == 9:
                    if checkGems() < 2:
                        checkpoint -= 1
                        FFXC.set_movement(-1, 0)
                        FFX_memory.waitFrames(60)
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_Screen.BattleScreen():
                FFX_Battle.calmLandsManip()
                FFX_memory.clickToControl3()
                if FFX_memory.nextChanceRNG10() >= 6:
                    FFX_memory.fullPartyFormat('rikku', fullMenuClose=False)
                else:
                    FFX_memory.fullPartyFormat('kimahri', fullMenuClose=False)
                FFX_Battle.healUp(fullMenuClose=True)
                FFX_memory.printManipInfo()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.menuB()


def defenderX():
    FFX_memory.awaitControl()
    FFX_menu.prepCalmLands()
    FFX_memory.fullPartyFormat('kimahri')
    while FFX_targetPathing.setMovement([67, -255]) == False:
        pass
    FFXC.set_movement(0, 1)
    FFX_memory.awaitEvent()
    FFXC.set_neutral()

    FFX_Xbox.clickToBattle()
    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            if FFX_Screen.turnTidus():
                FFX_Battle.buddySwapYuna()
            elif FFX_Screen.turnYuna():
                FFX_Battle.aeonSummon(4)
            else:
                FFX_Battle.attack('none')
    FFXC.set_movement(0, 1)
    FFX_memory.clickToControl()
    FFX_memory.printManipInfo()


def toTheRonso():
    checkpoint = 2
    while FFX_memory.getMap() != 259:
        if FFX_memory.userControl():
            if FFX_targetPathing.setMovement(FFX_targetPathing.defenderX(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

    # Now in screen with Ronso
    checkpoint = 0
    while FFX_memory.getMap() != 244:
        if FFX_memory.userControl():
            if FFX_targetPathing.setMovement(FFX_targetPathing.kelkRonso(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.turnReady():
                FFX_Battle.biranYenke()
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()


def gagazetGates():
    # Should appear on the map just before the Ronso hymn
    endVer = gameVars.endGameVersion()
    print("Grid version: " + str(endVer))
    FFX_Logs.writeLog("Grid version: " + str(endVer))
    FFX_Logs.writeStats("B&Y Return spheres:")
    if endVer == 4:
        FFX_Logs.writeStats("4")
    elif endVer == 3:
        FFX_Logs.writeStats("0")
    else:
        FFX_Logs.writeStats("2")
    #FFX_Logs.writeStats("B&Y Friend spheres:")
    # if endVer == 4:
    #    FFX_Logs.writeStats("0")
    # elif endVer == 3:
    #    FFX_Logs.writeStats("4")
    # else:
    #    FFX_Logs.writeStats("2")
    FFX_memory.awaitControl()
    if FFX_memory.overdriveState()[6] == 100:
        FFX_memory.fullPartyFormat('kimahri', fullMenuClose=False)
    else:
        FFX_memory.fullPartyFormat('rikku', fullMenuClose=False)
    FFX_menu.afterRonso()
    FFX_memory.closeMenu()  # just in case

    print("Gagazet path section")
    checkpoint = 0
    while FFX_memory.getMap() != 285:
        if FFX_memory.userControl():
            if FFX_targetPathing.setMovement(FFX_targetPathing.gagazetSnow(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif FFX_memory.battleActive():
                # Charge Rikku until full, otherwise flee all
                if FFX_memory.overdriveState()[6] == 100:
                    FFX_Battle.fleeAll()
                    FFX_memory.clickToControl()
                else:
                    FFX_Battle.gagazetPath()
                    FFX_memory.clickToControl()
                    if FFX_memory.overdriveState()[6] == 100:
                        FFX_memory.fullPartyFormat('kimahri')
                        # FFX_memory.setEncounterRate(0)
                    else:
                        FFX_memory.fullPartyFormat('rikku')
                FFX_memory.clickToControl()
                if FFX_memory.overdriveState2()[6] == 100 and gameVars.neArmor() != 255:
                    FFX_menu.equipArmor(
                        character=gameVars.neArmor(), ability=0x801D)
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    print("Should now be on the map with Seymour Flux.")


def Flux():
    print("Flux screen - ready for Seymour again.")
    FFXC.set_neutral()
    if gameVars.endGameVersion() != 3:
        FFX_memory.fullPartyFormat('yuna')
    checkpoint = 0
    while FFX_memory.getMap() != 309:
        if FFX_memory.userControl():
            if checkpoint == 7:
                FFXC.set_movement(0, 1)
                FFXC.set_neutral()
                FFX_memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 8:
                while FFX_memory.userControl():
                    FFXC.set_movement(1, 1)
                FFXC.set_neutral()
            elif FFX_targetPathing.setMovement(FFX_targetPathing.Flux(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                print("Flux battle start")
                FFX_Battle.seymourFlux()
                # FFXC.set_movement(0,1)
                FFX_memory.clickToControl3()
                if gameVars.endGameVersion() != 3:
                    FFX_menu.afterFlux()
                FFX_memory.fullPartyFormat('kimahri')
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
    if not gameVars.csr():
        while not FFX_memory.cutsceneSkipPossible():
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
        FFX_Xbox.skipScene()


def dream(checkpoint: int = 0):
    FFX_memory.clickToControl()
    print("*********")
    print("Dream sequence")
    print("*********")
    FFX_memory.waitFrames(3)

    while FFX_memory.getMap() != 309:
        if FFX_memory.userControl():
            if checkpoint == 11:
                FFXC.set_movement(-1, 1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 15:
                FFXC.set_movement(0, 1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 19:
                FFXC.set_movement(-1, -1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                checkpoint += 1
            elif FFX_targetPathing.setMovement(FFX_targetPathing.gagazetDreamSeq(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

            # Start the final dialog
            if checkpoint == 25:
                FFX_Xbox.tapB()
        else:
            FFX_Xbox.tapB()  # Skip all dialog
    print("*********")
    print("Dream sequence over")
    print("*********")


def dream_old():
    FFX_memory.clickToControl()
    print("*********")
    print("Dream sequence")
    print("*********")
    FFX_memory.waitFrames(3)
    pos = FFX_memory.getCoords()
    while pos[1] > 180:
        FFXC.set_movement(0.4, 1)
        pos = FFX_memory.getCoords()

    while pos[0] < -1:
        FFXC.set_movement(0, 1)
        pos = FFX_memory.getCoords()

    while pos[1] > 20:
        FFXC.set_movement(1, 1)
        pos = FFX_memory.getCoords()
    print("Onto the gangway")

    while pos[0] < 235:
        if pos[1] < -6:
            FFXC.set_movement(-1, 0)
        else:
            FFXC.set_movement(-1, 1)
        pos = FFX_memory.getCoords()

    while FFX_memory.userControl():  # Into the boathouse.
        FFXC.set_movement(-1, 0)
    print("Now inside the boathouse.")

    FFX_memory.awaitControl()
    FFXC.set_movement(1, 0)
    FFX_memory.waitFrames(30 * 0.7)
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_neutral()  # Start convo with Bahamut child
    print("First talk with Bahamut child")
    FFX_memory.clickToControl()

    if not gameVars.csr():
        FFXC.set_movement(0, -1)  # End of conversation
        FFX_memory.waitFrames(30 * 0.7)
        FFXC.set_movement(-1, 0)
        FFX_memory.waitFrames(30 * 0.7)
        FFXC.set_movement(0, -1)
        FFX_memory.waitFrames(30 * 0.7)
        FFXC.set_neutral()

        FFX_memory.clickToControl()
        pos = FFX_memory.getCoords()
        while pos[1] > -20:
            FFXC.set_movement(1, 0)
            pos = FFX_memory.getCoords()

        while pos[0] < 300:
            FFXC.set_movement(0, 1)
            pos = FFX_memory.getCoords()
        FFXC.set_movement(-1, 0)
        FFX_Xbox.SkipDialog(2)
        FFXC.set_neutral()  # Second/last convo with kid
        print("Second talk with Bahamut child")

        FFX_memory.clickToControl()


def cave():
    checkpoint = 0
    while FFX_memory.getMap() != 272:
        if FFX_memory.userControl():
            if FFX_memory.getMap() == 309 and FFX_memory.getCoords()[0] > 1160:
                FFXC.set_movement(0.5, 1)
                FFX_memory.waitFrames(3)
                FFXC.set_movement(0, 1)
                FFX_memory.waitFrames(6)
            elif FFX_targetPathing.setMovement(FFX_targetPathing.gagazetPostDream(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()

    FFX_memory.awaitControl()
    print("Gagazet cave section")
    # FFX_menu.gagazetCave()

    checkpoint = 0
    lastCP = 0
    powerNeeded = 6
    while FFX_memory.getMap() != 311:
        if FFX_memory.userControl():
            if checkpoint == 7:
                if FFX_memory.getMap() == 310:
                    print("Now in the trials map.")
                    checkpoint += 1
                else:
                    print("Into swimming map, first trial.")
                    FFXC.set_movement(0, 1)
                    FFX_memory.waitFrames(30 * 0.5)
            elif checkpoint == 12:
                print("Trial 1 - Let's Go!!!")
                while FFX_memory.userControl():
                    FFXC.set_movement(0, 1)
                FFXC.set_neutral()

                print("Now the trial has started.")
                FFX_Xbox.SkipDialog(2)

                # Need logic here for when to start the trial

                FFXC.set_neutral()
                while not FFX_memory.userControl():
                    if FFX_memory.GTouterRing() < 2.3 and FFX_memory.GTouterRing() > 2.05:
                        if FFX_memory.GTinnerRing() < 2.9 and FFX_memory.GTinnerRing() > 1.3:
                            FFX_Xbox.tapB()
                        elif FFX_memory.GTinnerRing() < 0.1 and FFX_memory.GTinnerRing() > -1.6:
                            FFX_Xbox.tapB()
                    elif FFX_memory.GTouterRing() < -0.7 and FFX_memory.GTouterRing() > -1.1:
                        if FFX_memory.GTinnerRing() < 2.9 and FFX_memory.GTinnerRing() > 1.3:
                            FFX_Xbox.tapB()
                        elif FFX_memory.GTinnerRing() < 0.1 and FFX_memory.GTinnerRing() > -1.6:
                            FFX_Xbox.tapB()

                print("First trial complete")
                checkpoint += 1
            elif checkpoint == 17:
                if FFX_memory.getMap() == 272:
                    print("Leaving the trials map.")
                    checkpoint += 1
                else:
                    print("Back to main map after first trial.")
                    FFXC.set_movement(0, -1)
                    FFX_memory.waitFrames(30 * 0.5)
            elif checkpoint == 29:
                if FFX_memory.getMap() == 310:
                    print("Now in the trials map.")
                    checkpoint += 1
                else:
                    print("Into swimming map, second trial.")
                    FFXC.set_movement(0, 1)
                    FFX_memory.waitFrames(30 * 0.5)
            elif checkpoint == 35:
                if FFX_memory.userControl():
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_neutral()

            elif checkpoint == 42:
                print("Out of swimming map, second trial.")
                if FFX_memory.getMap() == 272:
                    print("Leaving the trials map.")
                    checkpoint += 1
                else:
                    FFXC.set_movement(0, -1)
                    FFX_memory.waitFrames(30 * 0.5)
            elif checkpoint == 58:  # Just before sanctuary keeper
                FFXC.set_neutral()
                print("Prepping for Sanctuary Keeper")
                FFX_memory.fullPartyFormat('yuna')
                checkpoint += 1
            elif FFX_targetPathing.setMovement(FFX_targetPathing.gagazetCave(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if checkpoint == 35 and FFX_memory.diagProgressFlag() == 2:
                print("Second trial start")
                FFX_memory.waitFrames(90)
                FFX_Xbox.menuB()
                FFX_memory.waitFrames(45)
                FFXC.set_value('Dpad', 8)
                FFX_memory.waitFrames(45)
                FFXC.set_neutral()
                FFX_memory.clickToControl()
                checkpoint += 1
                print("Second trial is complete")
            elif checkpoint == 35 and FFX_memory.diagProgressFlag() == 3:
                # CSR second trial
                FFX_memory.waitFrames(10)
                FFXC.set_value('Dpad', 8)
                FFX_memory.waitFrames(45)
                FFXC.set_neutral()
                FFX_memory.clickToControl()
                checkpoint += 1
            elif FFX_memory.battleActive():
                if FFX_memory.getPower() < powerNeeded:
                    if FFX_memory.getBattleNum() == 351:  # Two maelstroms and a splasher
                        FFX_Battle.gagazetCave('down')
                    elif FFX_memory.getBattleNum() == 353:  # Two glowey guys, two splashers.
                        FFX_Battle.gagazetCave('right')
                    elif FFX_memory.getBattleNum() == 354:  # Four groups of splashers
                        FFX_Battle.gagazetCave('none')
                    elif FFX_memory.overdriveState2()[6] != 100:
                        if FFX_memory.getBattleNum() in [351, 352, 353, 354]:
                            FFX_Battle.caveChargeRikku()
                        else:
                            FFX_Battle.fleeAll()
                    else:
                        FFX_Battle.fleeAll()
                else:
                    FFX_Battle.fleeAll()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif checkpoint == 6 or checkpoint == 54:
                if FFX_memory.battleActive():
                    FFX_Battle.fleeAll()
                elif FFX_memory.diagSkipPossible():  # So we don't override the second trial
                    FFX_Xbox.tapB()

                # if FFX_memory.getPower() < powerNeeded and checkpoint >= 30 and checkpoint < 60:
                #    FFX_Battle.gagazetCave()
                # elif FFX_memory.getPower() < powerNeeded and checkpoint >= 90 and checkpoint < 110:
                #    FFX_Battle.gagazetCave()
                # else:
    FFX_Xbox.clickToBattle()
    FFX_Battle.sKeeper()


def wrapUp():
    print("Cave section complete and Sanctuary Keeper is down.")
    print("Now onward to Zanarkand.")

    checkpoint = 0
    while FFX_memory.getMap() != 132:
        if FFX_memory.userControl():
            if FFX_memory.getMap() == 312 and checkpoint < 6:
                print("Move forward to next map. Final path before making camp.")
                checkpoint = 7
            elif checkpoint == 3:
                # Story progress - 2635 before hug, 2650 after hug, 2678 after the Mi'ihen scene
                while FFX_memory.getStoryProgress() < 2651:
                    FFX_targetPathing.setMovement([786, -819])
                    FFX_Xbox.tapB()
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
            elif checkpoint == 6:
                if FFX_memory.getMap() == 312:
                    print("Final path before making camp.")
                    FFXC.set_neutral()
                    checkpoint += 1
                else:
                    FFXC.set_movement(1, 1)
            elif FFX_targetPathing.setMovement(FFX_targetPathing.gagazetPeak(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

    # Resting point before Zanarkand
    FFXC.set_neutral()
    FFX_memory.awaitControl()
    FFX_memory.waitFrames(30 * 0.07)

    if not gameVars.csr():
        FFXC.set_movement(0, 1)  # Start of the sadness cutscene.
        FFX_memory.awaitEvent()
        FFXC.set_neutral()

        sleepTime = 4
        print("Sadness cutscene")
        FFX_memory.waitFrames(30 * sleepTime)
        print("This is gunna be a while.")
        FFX_memory.waitFrames(30 * sleepTime)
        print("Maybe you should go get a drink or something.")
        FFX_memory.waitFrames(30 * sleepTime)
        print("Like... what even is this???")
        FFX_memory.waitFrames(30 * sleepTime)
        print("I just")
        FFX_memory.waitFrames(30 * sleepTime)
        print("I just can't")
        FFX_memory.waitFrames(30 * sleepTime)
        print("Do you realize that some poor soul")
        FFX_memory.waitFrames(30 * sleepTime)
        print("not only wrote the entire program for this by himself")
        FFX_memory.waitFrames(30 * sleepTime)
        print("And then wasted ten minutes to put in this ridiculous dialog?")
        FFX_memory.waitFrames(30 * sleepTime)
        print("Talk about not having a life.")
        FFX_memory.waitFrames(30 * sleepTime)
        print("Ah well, still have some time. Might as well shout out a few people.")
        FFX_memory.waitFrames(30 * sleepTime)
        print("First and most importantly, my wife for putting up with me for two years through this project.")
        FFX_memory.waitFrames(30 * sleepTime)
        print("My wife is the best!")
        FFX_memory.waitFrames(30 * sleepTime)
        print("Next, DwangoAC. He encouraged me to write my own code to do this.")
        FFX_memory.waitFrames(30 * sleepTime)
        print("And he put together the TASbot community which has been hugely helpful.")
        FFX_memory.waitFrames(30 * sleepTime)
        print("Shout out to DwangoAC and the TASbot Community. You guys rock!!!")
        FFX_memory.waitFrames(30 * sleepTime)
        print("Specifically from the TASbot Community, Inverted wrote the pathing logic for the Egg Hunt section.")
        FFX_memory.waitFrames(30 * sleepTime)
        print("You will see Inverted's work right before the final bosses.")
        FFX_memory.waitFrames(30 * sleepTime)
        print("Next, some people from the FFX speedrunning community.")
        FFX_memory.waitFrames(30 * sleepTime)
        print("CrimsonInferno, current world record holder for this category. Dude knows everything about this run!")
        FFX_memory.waitFrames(30 * sleepTime)
        print("Crimson re-wrote a great many boss fights for this project. From Spherimorph to Evrae Altana, and probably more.")
        FFX_memory.waitFrames(30 * sleepTime)
        print("Also, 'Rossy__' from the same community. Rossy helped me find a great many things in memory.")
        FFX_memory.waitFrames(30 * sleepTime)
        print("He also taught me a number of things about memory scans, pointers, etc. Dude is super smart.")
        FFX_memory.waitFrames(30 * sleepTime)
        print("Peppy too. He has found a few key things in memory too.")
        FFX_memory.waitFrames(30 * sleepTime)
        print("And last, Mr Tyton from the FFX speedrun community has re-written many pieces of my code.")
        FFX_memory.waitFrames(30 * sleepTime)
        print("He has also done a lot of optimizations I just couldn't get back to.")
        FFX_memory.waitFrames(30 * sleepTime)
        print("Legitimately Tyton pushed this project from decent towards excellent when I was running out of steam.")
        FFX_memory.waitFrames(30 * sleepTime)
        print("OK that wraps it up for this bit. I'll catch you when it's done.")
        FFX_memory.waitFrames(30 * sleepTime)

        FFX_memory.clickToControl()
        print("OMG finally! Let's get to it! (Do kids say that any more?)")
        FFXC.set_movement(0, 1)
        FFX_memory.waitFrames(30 * 1)
        FFXC.set_movement(-1, 1)
        FFX_memory.awaitEvent()
        FFXC.set_neutral()
        FFX_memory.waitFrames(30 * 0.2)
