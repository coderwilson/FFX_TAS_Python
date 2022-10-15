import battle.main
import logs
import memory.main
import menu
import rngTrack
import screen
import targetPathing
import vars
import xbox

gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def checkGems():
    gemSlot = memory.main.getItemSlot(34)
    if gemSlot < 200:
        gems = memory.main.getItemCountSlot(gemSlot)
    else:
        gems = 0

    gemSlot = memory.main.getItemSlot(28)
    if gemSlot < 200:
        gems += memory.main.getItemCountSlot(gemSlot)
    print("Total gems:", gems)
    return gems


def calmLands():
    memory.main.awaitControl()
    # Start by getting away from the save sphere
    memory.main.fullPartyFormat('rikku', fullMenuClose=True)
    #battle.main.healUp(fullMenuClose=True)

    rngTrack.printManipInfo()
    print("RNG10:", memory.main.rng10())
    print("RNG12:", memory.main.rng12())
    print("RNG13:", memory.main.rng13())
    # Enter the cutscene where Yuna muses about ending her journey.
    while not (memory.main.getCoords()[1] >= -1650 and memory.main.userControl()):
        if memory.main.userControl():
            FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()

    checkpoint = 0
    while memory.main.getMap() != 279:
        if memory.main.userControl():
            if targetPathing.setMovement(targetPathing.calmLands(checkpoint)):
                checkpoint += 1
                if checkpoint == 15:
                    if checkGems() < 2:
                        checkpoint -= 1
                        FFXC.set_movement(-1, -1)
                        memory.main.waitFrames(60)
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if screen.BattleScreen():
                battle.main.calmLandsManip()
                memory.main.clickToControl3()
                memory.main.fullPartyFormat('rikku', fullMenuClose=True)
                #battle.main.healUp(fullMenuClose=True)
                rngTrack.printManipInfo()
            elif memory.main.menuOpen():
                xbox.tapB()
            elif memory.main.diagSkipPossible():
                xbox.menuB()


def defenderX():
    memory.main.awaitControl()
    menu.prepCalmLands()
    memory.main.fullPartyFormat('postbunyip')
    while not targetPathing.setMovement([67, -255]):
        pass
    FFXC.set_movement(0, 1)
    memory.main.awaitEvent()
    FFXC.set_neutral()

    xbox.clickToBattle()
    while memory.main.battleActive():
        if memory.main.turnReady():
            if screen.turnTidus():
                battle.main.buddySwapYuna()
            elif screen.turnYuna():
                battle.main.aeonSummon(4)
            else:
                battle.main.attack('none')
    FFXC.set_movement(0, 1)
    memory.main.clickToControl()
    rngTrack.printManipInfo()


def toTheRonso():
    checkpoint = 2
    while memory.main.getMap() != 259:
        if memory.main.userControl():
            if targetPathing.setMovement(targetPathing.defenderX(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()

    # Now in screen with Ronso
    checkpoint = 0
    while memory.main.getMap() != 244:
        if memory.main.userControl():
            if targetPathing.setMovement(targetPathing.kelkRonso(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.turnReady():
                battle.main.biranYenke()
            elif memory.main.diagSkipPossible():
                xbox.tapB()


def gagazetGates():
    # Should appear on the map just before the Ronso hymn
    endVer = gameVars.endGameVersion()
    print("Grid version: " + str(endVer))
    logs.writeStats("B&Y Return spheres:")
    if endVer == 4:
        logs.writeStats("4")
    elif endVer == 3:
        logs.writeStats("0")
    else:
        logs.writeStats("2")
    memory.main.awaitControl()
    if memory.main.overdriveState()[6] == 100:
        memory.main.fullPartyFormat('kimahri', fullMenuClose=False)
    else:
        memory.main.fullPartyFormat('rikku', fullMenuClose=False)
    menu.afterRonso()
    memory.main.closeMenu()  # just in case

    print("Gagazet path section")
    checkpoint = 0
    while memory.main.getMap() != 285:
        if memory.main.userControl():
            if targetPathing.setMovement(targetPathing.gagazetSnow(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.menuOpen():
                xbox.tapB()
            elif memory.main.battleActive():
                # Charge Rikku until full, otherwise flee all
                if memory.main.overdriveState()[6] == 100:
                    battle.main.fleeAll()
                    memory.main.clickToControl()
                else:
                    battle.main.gagazetPath()
                    memory.main.clickToControl()
                    if memory.main.overdriveState()[6] == 100:
                        memory.main.fullPartyFormat('kimahri')
                    else:
                        memory.main.fullPartyFormat('rikku')
                memory.main.clickToControl()
                if memory.main.overdriveState2()[6] == 100 and gameVars.neArmor() != 255:
                    menu.equipArmor(
                        character=gameVars.neArmor(), ability=0x801D)
            elif memory.main.diagSkipPossible():
                xbox.tapB()
    print("Should now be on the map with Seymour Flux.")


def Flux():
    print("Flux screen - ready for Seymour again.")
    FFXC.set_neutral()
    if gameVars.endGameVersion() != 3:
        memory.main.fullPartyFormat('yuna')
    checkpoint = 0
    while memory.main.getMap() != 309:
        if memory.main.userControl():
            if checkpoint == 7:
                FFXC.set_movement(0, 1)
                FFXC.set_neutral()
                memory.main.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 8:
                while memory.main.userControl():
                    FFXC.set_movement(1, 1)
                FFXC.set_neutral()
            elif targetPathing.setMovement(targetPathing.Flux(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                print("Flux battle start")
                battle.main.seymourFlux()
                # FFXC.set_movement(0,1)
                memory.main.clickToControl3()
                if gameVars.endGameVersion() != 3:
                    menu.afterFlux()
                memory.main.fullPartyFormat('kimahri')
            elif memory.main.diagSkipPossible():
                xbox.tapB()
            elif memory.main.menuOpen():
                xbox.tapB()
    if not gameVars.csr():
        while not memory.main.cutsceneSkipPossible():
            if memory.main.diagSkipPossible():
                xbox.tapB()
        xbox.skipScene()


def dream(checkpoint: int = 0):
    memory.main.clickToControl()
    print("*********")
    print("Dream sequence")
    print("*********")
    memory.main.waitFrames(3)

    while memory.main.getMap() != 309:
        if memory.main.userControl():
            if checkpoint == 11:
                FFXC.set_movement(-1, 1)
                memory.main.awaitEvent()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 15:
                FFXC.set_movement(0, 1)
                memory.main.awaitEvent()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 19:
                FFXC.set_movement(-1, -1)
                memory.main.awaitEvent()
                FFXC.set_neutral()
                checkpoint += 1
            elif targetPathing.setMovement(targetPathing.gagazetDreamSeq(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

            # Start the final dialog
            if checkpoint == 25:
                xbox.tapB()
        else:
            xbox.tapB()  # Skip all dialog
    print("*********")
    print("Dream sequence over")
    print("*********")


def dream_old():
    memory.main.clickToControl()
    print("*********")
    print("Dream sequence")
    print("*********")
    memory.main.waitFrames(3)
    pos = memory.main.getCoords()
    while pos[1] > 180:
        FFXC.set_movement(0.4, 1)
        pos = memory.main.getCoords()

    while pos[0] < -1:
        FFXC.set_movement(0, 1)
        pos = memory.main.getCoords()

    while pos[1] > 20:
        FFXC.set_movement(1, 1)
        pos = memory.main.getCoords()
    print("Onto the gangway")

    while pos[0] < 235:
        if pos[1] < -6:
            FFXC.set_movement(-1, 0)
        else:
            FFXC.set_movement(-1, 1)
        pos = memory.main.getCoords()

    while memory.main.userControl():  # Into the boathouse.
        FFXC.set_movement(-1, 0)
    print("Now inside the boathouse.")

    memory.main.awaitControl()
    FFXC.set_movement(1, 0)
    memory.main.waitFrames(30 * 0.7)
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 1)
    FFXC.set_neutral()  # Start convo with Bahamut child
    print("First talk with Bahamut child")
    memory.main.clickToControl()

    if not gameVars.csr():
        FFXC.set_movement(0, -1)  # End of conversation
        memory.main.waitFrames(30 * 0.7)
        FFXC.set_movement(-1, 0)
        memory.main.waitFrames(30 * 0.7)
        FFXC.set_movement(0, -1)
        memory.main.waitFrames(30 * 0.7)
        FFXC.set_neutral()

        memory.main.clickToControl()
        pos = memory.main.getCoords()
        while pos[1] > -20:
            FFXC.set_movement(1, 0)
            pos = memory.main.getCoords()

        while pos[0] < 300:
            FFXC.set_movement(0, 1)
            pos = memory.main.getCoords()
        FFXC.set_movement(-1, 0)
        xbox.SkipDialog(2)
        FFXC.set_neutral()  # Second/last convo with kid
        print("Second talk with Bahamut child")

        memory.main.clickToControl()


def cave():
    checkpoint = 0

    while memory.main.getMap() != 272:
        if memory.main.userControl():
            if memory.main.getMap() == 309 and memory.main.getCoords()[0] > 1160:
                FFXC.set_movement(0.5, 1)
                memory.main.waitFrames(3)
                FFXC.set_movement(0, 1)
                memory.main.waitFrames(6)
            elif targetPathing.setMovement(targetPathing.gagazetPostDream(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()
            elif memory.main.menuOpen():
                xbox.tapB()

    memory.main.awaitControl()
    print("Gagazet cave section")

    checkpoint = 0
    powerNeeded = 6
    while memory.main.getMap() != 311:
        if memory.main.userControl():
            if checkpoint == 7:
                if memory.main.getMap() == 310:
                    print("Now in the trials map.")
                    checkpoint += 1
                else:
                    print("Into swimming map, first trial.")
                    FFXC.set_movement(0, 1)
                    memory.main.waitFrames(30 * 0.5)
            elif checkpoint == 12:
                print("Trial 1 - Let's Go!!!")
                while memory.main.userControl():
                    FFXC.set_movement(0, 1)
                FFXC.set_neutral()

                print("Now the trial has started.")
                xbox.SkipDialog(2)

                # Need logic here for when to start the trial

                FFXC.set_neutral()
                while not memory.main.userControl():
                    if memory.main.GTouterRing() < 2.3 and memory.main.GTouterRing() > 2.05:
                        if memory.main.GTinnerRing() < 2.9 and memory.main.GTinnerRing() > 1.3:
                            xbox.tapB()
                        elif memory.main.GTinnerRing() < 0.1 and memory.main.GTinnerRing() > -1.6:
                            xbox.tapB()
                    elif memory.main.GTouterRing() < -0.7 and memory.main.GTouterRing() > -1.1:
                        if memory.main.GTinnerRing() < 2.9 and memory.main.GTinnerRing() > 1.3:
                            xbox.tapB()
                        elif memory.main.GTinnerRing() < 0.1 and memory.main.GTinnerRing() > -1.6:
                            xbox.tapB()

                print("First trial complete")
                checkpoint += 1
            elif checkpoint == 17:
                if memory.main.getMap() == 272:
                    print("Leaving the trials map.")
                    checkpoint += 1
                else:
                    print("Back to main map after first trial.")
                    FFXC.set_movement(0, -1)
                    memory.main.waitFrames(30 * 0.5)
            elif checkpoint == 29:
                if memory.main.getMap() == 310:
                    print("Now in the trials map.")
                    checkpoint += 1
                else:
                    print("Into swimming map, second trial.")
                    FFXC.set_movement(0, 1)
                    memory.main.waitFrames(30 * 0.5)
            elif checkpoint == 35:
                if memory.main.userControl():
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_neutral()

            elif checkpoint == 42:
                print("Out of swimming map, second trial.")
                if memory.main.getMap() == 272:
                    print("Leaving the trials map.")
                    checkpoint += 1
                else:
                    FFXC.set_movement(0, -1)
                    memory.main.waitFrames(30 * 0.5)
            elif checkpoint == 59:  # Just before sanctuary keeper
                FFXC.set_neutral()
                print("Prepping for Sanctuary Keeper")
                memory.main.fullPartyFormat('yuna')
                checkpoint += 1

                # Determine drops from Yunalesca
                # logs.openRNGTrack()
                # import rngTrack
                # zombieResults = rngTrack.zombieTrack(report=True)
                # logs.writeRNGTrack("Final results:"+str(zombieResults))
            elif targetPathing.setMovement(targetPathing.gagazetCave(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if checkpoint == 35 and memory.main.diagProgressFlag() == 2:
                print("Second trial start")
                memory.main.waitFrames(90)
                xbox.menuB()
                memory.main.waitFrames(45)
                FFXC.set_value('Dpad', 8)
                memory.main.waitFrames(45)
                FFXC.set_neutral()
                memory.main.clickToControl()
                checkpoint += 1
                print("Second trial is complete")
            elif checkpoint == 35 and memory.main.diagProgressFlag() == 3:
                # CSR second trial
                memory.main.waitFrames(10)
                FFXC.set_value('Dpad', 8)
                memory.main.waitFrames(45)
                FFXC.set_neutral()
                memory.main.clickToControl()
                checkpoint += 1
            elif memory.main.battleActive():
                if memory.main.getPower() < powerNeeded:
                    if memory.main.getEncounterID() == 351:  # Two maelstroms and a splasher
                        battle.main.gagazetCave('down')
                    elif memory.main.getEncounterID() == 353:  # Two glowey guys, two splashers.
                        battle.main.gagazetCave('right')
                    elif memory.main.getEncounterID() == 354:  # Four groups of splashers
                        battle.main.gagazetCave('none')
                    elif memory.main.overdriveState2()[6] != 100:
                        if memory.main.getEncounterID() in [351, 352, 353, 354]:
                            battle.main.caveChargeRikku()
                        else:
                            battle.main.fleeAll()
                    else:
                        battle.main.fleeAll()
                else:
                    battle.main.fleeAll()
            elif memory.main.menuOpen():
                xbox.tapB()
            elif checkpoint == 6 or checkpoint == 54:
                if memory.main.battleActive():
                    battle.main.fleeAll()
                elif memory.main.diagSkipPossible():  # So we don't override the second trial
                    xbox.tapB()

    xbox.clickToBattle()
    battle.main.sKeeper()


def wrapUp():
    print("Cave section complete and Sanctuary Keeper is down.")
    print("Now onward to Zanarkand.")

    checkpoint = 0
    while memory.main.getMap() != 132:
        if memory.main.userControl():
            if memory.main.getMap() == 312 and checkpoint < 6:
                print("Move forward to next map. Final path before making camp.")
                checkpoint = 7
            elif checkpoint == 3:
                # Story progress - 2635 before hug, 2650 after hug, 2678 after the Mi'ihen scene
                while memory.main.getStoryProgress() < 2651:
                    targetPathing.setMovement([786, -819])
                    xbox.tapB()
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
            elif checkpoint == 6:
                if memory.main.getMap() == 312:
                    print("Final path before making camp.")
                    FFXC.set_neutral()
                    checkpoint += 1
                else:
                    FFXC.set_movement(1, 1)
            elif targetPathing.setMovement(targetPathing.gagazetPeak(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()

    # Resting point before Zanarkand
    FFXC.set_neutral()
    memory.main.awaitControl()
    memory.main.waitFrames(30 * 0.07)

    if not gameVars.csr():
        FFXC.set_movement(0, 1)  # Start of the sadness cutscene.
        memory.main.awaitEvent()
        FFXC.set_neutral()

        sleepTime = 4
        print("Sadness cutscene")
        memory.main.waitFrames(30 * sleepTime)
        print("This is gunna be a while.")
        memory.main.waitFrames(30 * sleepTime)
        print("Maybe you should go get a drink or something.")
        memory.main.waitFrames(30 * sleepTime)
        print("Like... what even is this???")
        memory.main.waitFrames(30 * sleepTime)
        print("I just")
        memory.main.waitFrames(30 * sleepTime)
        print("I just can't")
        memory.main.waitFrames(30 * sleepTime)
        print("Do you realize that some poor soul")
        memory.main.waitFrames(30 * sleepTime)
        print("not only wrote the entire program for this by himself")
        memory.main.waitFrames(30 * sleepTime)
        print("And then wasted ten minutes to put in this ridiculous dialog?")
        memory.main.waitFrames(30 * sleepTime)
        print("Talk about not having a life.")
        memory.main.waitFrames(30 * sleepTime)
        print("Ah well, still have some time. Might as well shout out a few people.")
        memory.main.waitFrames(30 * sleepTime)
        print("First and most importantly, my wife for putting up with me for two years through this project.")
        memory.main.waitFrames(30 * sleepTime)
        print("My wife is the best!")
        memory.main.waitFrames(30 * sleepTime)
        print("Next, DwangoAC. He encouraged me to write my own code to do this.")
        memory.main.waitFrames(30 * sleepTime)
        print("And he put together the TASbot community which has been hugely helpful.")
        memory.main.waitFrames(30 * sleepTime)
        print("Shout out to DwangoAC and the TASbot Community. You guys rock!!!")
        memory.main.waitFrames(30 * sleepTime)
        print("Specifically from the TASbot Community, Inverted wrote the pathing logic for the Egg Hunt section.")
        memory.main.waitFrames(30 * sleepTime)
        print("You will see Inverted's work right before the final bosses.")
        memory.main.waitFrames(30 * sleepTime)
        print("Next, some people from the FFX speedrunning community.")
        memory.main.waitFrames(30 * sleepTime)
        print("CrimsonInferno, current world record holder for this category. Dude knows everything about this run!")
        memory.main.waitFrames(30 * sleepTime)
        print("Crimson re-wrote a great many boss fights for this project. From Spherimorph to Evrae Altana, and probably more.")
        memory.main.waitFrames(30 * sleepTime)
        print("Also, 'Rossy__' from the same community. Rossy helped me find a great many things in memory.")
        memory.main.waitFrames(30 * sleepTime)
        print("He also taught me a number of things about memory scans, pointers, etc. Dude is super smart.")
        memory.main.waitFrames(30 * sleepTime)
        print("Peppy too. He has found a few key things in memory too.")
        memory.main.waitFrames(30 * sleepTime)
        print("And last, Mr Tyton from the FFX speedrun community has re-written many pieces of my code.")
        memory.main.waitFrames(30 * sleepTime)
        print("He has also done a lot of optimizations I just couldn't get back to.")
        memory.main.waitFrames(30 * sleepTime)
        print("Legitimately Tyton pushed this project from decent towards excellent when I was running out of steam.")
        memory.main.waitFrames(30 * sleepTime)
        print("OK that wraps it up for this bit. I'll catch you when it's done.")
        memory.main.waitFrames(30 * sleepTime)

        memory.main.clickToControl()
        print("OMG finally! Let's get to it! (Do kids say that any more?)")
        FFXC.set_movement(0, 1)
        memory.main.waitFrames(30 * 1)
        FFXC.set_movement(-1, 1)
        memory.main.awaitEvent()
        FFXC.set_neutral()
        memory.main.waitFrames(30 * 0.2)
