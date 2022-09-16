import xbox
import screen
import battle
import menu
import logs
import memory
import targetPathing
import vars
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def checkGems():
    gemSlot = memory.getItemSlot(34)
    if gemSlot < 200:
        gems = memory.getItemCountSlot(gemSlot)
    else:
        gems = 0

    gemSlot = memory.getItemSlot(28)
    if gemSlot < 200:
        gems += memory.getItemCountSlot(gemSlot)
    print("Total gems:", gems)
    return gems


def calmLands():
    memory.awaitControl()
    # Start by getting away from the save sphere
    memory.fullPartyFormat('rikku', fullMenuClose=False)
    battle.healUp(fullMenuClose=True)

    memory.printManipInfo()
    print("RNG10:", memory.rng10())
    print("RNG12:", memory.rng12())
    print("RNG13:", memory.rng13())
    # Enter the cutscene where Yuna muses about ending her journey.
    while not (memory.getCoords()[1] >= -1650 and memory.userControl()):
        if memory.userControl():
            FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()

    checkpoint = 0
    while memory.getMap() != 279:
        if memory.userControl():
            if targetPathing.setMovement(targetPathing.calmLands(checkpoint)):
                checkpoint += 1
                if checkpoint == 9:
                    if checkGems() < 2:
                        checkpoint -= 1
                        FFXC.set_movement(-1, 0)
                        memory.waitFrames(60)
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if screen.BattleScreen():
                battle.calmLandsManip()
                memory.clickToControl3()
                memory.fullPartyFormat('rikku', fullMenuClose=False)
                battle.healUp(fullMenuClose=True)
                memory.printManipInfo()
            elif memory.menuOpen():
                xbox.tapB()
            elif memory.diagSkipPossible():
                xbox.menuB()


def defenderX():
    memory.awaitControl()
    menu.prepCalmLands()
    memory.fullPartyFormat('postbunyip')
    while not targetPathing.setMovement([67, -255]):
        pass
    FFXC.set_movement(0, 1)
    memory.awaitEvent()
    FFXC.set_neutral()

    xbox.clickToBattle()
    while memory.battleActive():
        if memory.turnReady():
            if screen.turnTidus():
                battle.buddySwapYuna()
            elif screen.turnYuna():
                battle.aeonSummon(4)
            else:
                battle.attack('none')
    FFXC.set_movement(0, 1)
    memory.clickToControl()
    memory.printManipInfo()


def toTheRonso():
    checkpoint = 2
    while memory.getMap() != 259:
        if memory.userControl():
            if targetPathing.setMovement(targetPathing.defenderX(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()

    # Now in screen with Ronso
    checkpoint = 0
    while memory.getMap() != 244:
        if memory.userControl():
            if targetPathing.setMovement(targetPathing.kelkRonso(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.turnReady():
                battle.biranYenke()
            elif memory.diagSkipPossible():
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
    memory.awaitControl()
    if memory.overdriveState()[6] == 100:
        memory.fullPartyFormat('kimahri', fullMenuClose=False)
    else:
        memory.fullPartyFormat('rikku', fullMenuClose=False)
    menu.afterRonso()
    memory.closeMenu()  # just in case

    print("Gagazet path section")
    checkpoint = 0
    while memory.getMap() != 285:
        if memory.userControl():
            if targetPathing.setMovement(targetPathing.gagazetSnow(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.menuOpen():
                xbox.tapB()
            elif memory.battleActive():
                # Charge Rikku until full, otherwise flee all
                if memory.overdriveState()[6] == 100:
                    battle.fleeAll()
                    memory.clickToControl()
                else:
                    battle.gagazetPath()
                    memory.clickToControl()
                    if memory.overdriveState()[6] == 100:
                        memory.fullPartyFormat('kimahri')
                    else:
                        memory.fullPartyFormat('rikku')
                memory.clickToControl()
                if memory.overdriveState2()[6] == 100 and gameVars.neArmor() != 255:
                    menu.equipArmor(
                        character=gameVars.neArmor(), ability=0x801D)
            elif memory.diagSkipPossible():
                xbox.tapB()
    print("Should now be on the map with Seymour Flux.")


def Flux():
    print("Flux screen - ready for Seymour again.")
    FFXC.set_neutral()
    if gameVars.endGameVersion() != 3:
        memory.fullPartyFormat('yuna')
    checkpoint = 0
    while memory.getMap() != 309:
        if memory.userControl():
            if checkpoint == 7:
                FFXC.set_movement(0, 1)
                FFXC.set_neutral()
                memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 8:
                while memory.userControl():
                    FFXC.set_movement(1, 1)
                FFXC.set_neutral()
            elif targetPathing.setMovement(targetPathing.Flux(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.battleActive():
                print("Flux battle start")
                battle.seymourFlux()
                # FFXC.set_movement(0,1)
                memory.clickToControl3()
                if gameVars.endGameVersion() != 3:
                    menu.afterFlux()
                memory.fullPartyFormat('kimahri')
            elif memory.diagSkipPossible():
                xbox.tapB()
            elif memory.menuOpen():
                xbox.tapB()
    if not gameVars.csr():
        while not memory.cutsceneSkipPossible():
            if memory.diagSkipPossible():
                xbox.tapB()
        xbox.skipScene()


def dream(checkpoint: int = 0):
    memory.clickToControl()
    print("*********")
    print("Dream sequence")
    print("*********")
    memory.waitFrames(3)

    while memory.getMap() != 309:
        if memory.userControl():
            if checkpoint == 11:
                FFXC.set_movement(-1, 1)
                memory.awaitEvent()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 15:
                FFXC.set_movement(0, 1)
                memory.awaitEvent()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 19:
                FFXC.set_movement(-1, -1)
                memory.awaitEvent()
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
    memory.clickToControl()
    print("*********")
    print("Dream sequence")
    print("*********")
    memory.waitFrames(3)
    pos = memory.getCoords()
    while pos[1] > 180:
        FFXC.set_movement(0.4, 1)
        pos = memory.getCoords()

    while pos[0] < -1:
        FFXC.set_movement(0, 1)
        pos = memory.getCoords()

    while pos[1] > 20:
        FFXC.set_movement(1, 1)
        pos = memory.getCoords()
    print("Onto the gangway")

    while pos[0] < 235:
        if pos[1] < -6:
            FFXC.set_movement(-1, 0)
        else:
            FFXC.set_movement(-1, 1)
        pos = memory.getCoords()

    while memory.userControl():  # Into the boathouse.
        FFXC.set_movement(-1, 0)
    print("Now inside the boathouse.")

    memory.awaitControl()
    FFXC.set_movement(1, 0)
    memory.waitFrames(30 * 0.7)
    FFXC.set_movement(0, 1)
    memory.waitFrames(30 * 1)
    FFXC.set_neutral()  # Start convo with Bahamut child
    print("First talk with Bahamut child")
    memory.clickToControl()

    if not gameVars.csr():
        FFXC.set_movement(0, -1)  # End of conversation
        memory.waitFrames(30 * 0.7)
        FFXC.set_movement(-1, 0)
        memory.waitFrames(30 * 0.7)
        FFXC.set_movement(0, -1)
        memory.waitFrames(30 * 0.7)
        FFXC.set_neutral()

        memory.clickToControl()
        pos = memory.getCoords()
        while pos[1] > -20:
            FFXC.set_movement(1, 0)
            pos = memory.getCoords()

        while pos[0] < 300:
            FFXC.set_movement(0, 1)
            pos = memory.getCoords()
        FFXC.set_movement(-1, 0)
        xbox.SkipDialog(2)
        FFXC.set_neutral()  # Second/last convo with kid
        print("Second talk with Bahamut child")

        memory.clickToControl()


def cave():
    checkpoint = 0

    while memory.getMap() != 272:
        if memory.userControl():
            if memory.getMap() == 309 and memory.getCoords()[0] > 1160:
                FFXC.set_movement(0.5, 1)
                memory.waitFrames(3)
                FFXC.set_movement(0, 1)
                memory.waitFrames(6)
            elif targetPathing.setMovement(targetPathing.gagazetPostDream(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()
            elif memory.menuOpen():
                xbox.tapB()

    memory.awaitControl()
    print("Gagazet cave section")

    checkpoint = 0
    powerNeeded = 6
    while memory.getMap() != 311:
        if memory.userControl():
            if checkpoint == 7:
                if memory.getMap() == 310:
                    print("Now in the trials map.")
                    checkpoint += 1
                else:
                    print("Into swimming map, first trial.")
                    FFXC.set_movement(0, 1)
                    memory.waitFrames(30 * 0.5)
            elif checkpoint == 12:
                print("Trial 1 - Let's Go!!!")
                while memory.userControl():
                    FFXC.set_movement(0, 1)
                FFXC.set_neutral()

                print("Now the trial has started.")
                xbox.SkipDialog(2)

                # Need logic here for when to start the trial

                FFXC.set_neutral()
                while not memory.userControl():
                    if memory.GTouterRing() < 2.3 and memory.GTouterRing() > 2.05:
                        if memory.GTinnerRing() < 2.9 and memory.GTinnerRing() > 1.3:
                            xbox.tapB()
                        elif memory.GTinnerRing() < 0.1 and memory.GTinnerRing() > -1.6:
                            xbox.tapB()
                    elif memory.GTouterRing() < -0.7 and memory.GTouterRing() > -1.1:
                        if memory.GTinnerRing() < 2.9 and memory.GTinnerRing() > 1.3:
                            xbox.tapB()
                        elif memory.GTinnerRing() < 0.1 and memory.GTinnerRing() > -1.6:
                            xbox.tapB()

                print("First trial complete")
                checkpoint += 1
            elif checkpoint == 17:
                if memory.getMap() == 272:
                    print("Leaving the trials map.")
                    checkpoint += 1
                else:
                    print("Back to main map after first trial.")
                    FFXC.set_movement(0, -1)
                    memory.waitFrames(30 * 0.5)
            elif checkpoint == 29:
                if memory.getMap() == 310:
                    print("Now in the trials map.")
                    checkpoint += 1
                else:
                    print("Into swimming map, second trial.")
                    FFXC.set_movement(0, 1)
                    memory.waitFrames(30 * 0.5)
            elif checkpoint == 35:
                if memory.userControl():
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_neutral()

            elif checkpoint == 42:
                print("Out of swimming map, second trial.")
                if memory.getMap() == 272:
                    print("Leaving the trials map.")
                    checkpoint += 1
                else:
                    FFXC.set_movement(0, -1)
                    memory.waitFrames(30 * 0.5)
            elif checkpoint == 59:  # Just before sanctuary keeper
                FFXC.set_neutral()
                print("Prepping for Sanctuary Keeper")
                memory.fullPartyFormat('yuna')
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
            if checkpoint == 35 and memory.diagProgressFlag() == 2:
                print("Second trial start")
                memory.waitFrames(90)
                xbox.menuB()
                memory.waitFrames(45)
                FFXC.set_value('Dpad', 8)
                memory.waitFrames(45)
                FFXC.set_neutral()
                memory.clickToControl()
                checkpoint += 1
                print("Second trial is complete")
            elif checkpoint == 35 and memory.diagProgressFlag() == 3:
                # CSR second trial
                memory.waitFrames(10)
                FFXC.set_value('Dpad', 8)
                memory.waitFrames(45)
                FFXC.set_neutral()
                memory.clickToControl()
                checkpoint += 1
            elif memory.battleActive():
                if memory.getPower() < powerNeeded:
                    if memory.getEncounterID() == 351:  # Two maelstroms and a splasher
                        battle.gagazetCave('down')
                    elif memory.getEncounterID() == 353:  # Two glowey guys, two splashers.
                        battle.gagazetCave('right')
                    elif memory.getEncounterID() == 354:  # Four groups of splashers
                        battle.gagazetCave('none')
                    elif memory.overdriveState2()[6] != 100:
                        if memory.getEncounterID() in [351, 352, 353, 354]:
                            battle.caveChargeRikku()
                        else:
                            battle.fleeAll()
                    else:
                        battle.fleeAll()
                else:
                    battle.fleeAll()
            elif memory.menuOpen():
                xbox.tapB()
            elif checkpoint == 6 or checkpoint == 54:
                if memory.battleActive():
                    battle.fleeAll()
                elif memory.diagSkipPossible():  # So we don't override the second trial
                    xbox.tapB()

    xbox.clickToBattle()
    battle.sKeeper()


def wrapUp():
    print("Cave section complete and Sanctuary Keeper is down.")
    print("Now onward to Zanarkand.")

    checkpoint = 0
    while memory.getMap() != 132:
        if memory.userControl():
            if memory.getMap() == 312 and checkpoint < 6:
                print("Move forward to next map. Final path before making camp.")
                checkpoint = 7
            elif checkpoint == 3:
                # Story progress - 2635 before hug, 2650 after hug, 2678 after the Mi'ihen scene
                while memory.getStoryProgress() < 2651:
                    targetPathing.setMovement([786, -819])
                    xbox.tapB()
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
            elif checkpoint == 6:
                if memory.getMap() == 312:
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
            if memory.diagSkipPossible():
                xbox.tapB()

    # Resting point before Zanarkand
    FFXC.set_neutral()
    memory.awaitControl()
    memory.waitFrames(30 * 0.07)

    if not gameVars.csr():
        FFXC.set_movement(0, 1)  # Start of the sadness cutscene.
        memory.awaitEvent()
        FFXC.set_neutral()

        sleepTime = 4
        print("Sadness cutscene")
        memory.waitFrames(30 * sleepTime)
        print("This is gunna be a while.")
        memory.waitFrames(30 * sleepTime)
        print("Maybe you should go get a drink or something.")
        memory.waitFrames(30 * sleepTime)
        print("Like... what even is this???")
        memory.waitFrames(30 * sleepTime)
        print("I just")
        memory.waitFrames(30 * sleepTime)
        print("I just can't")
        memory.waitFrames(30 * sleepTime)
        print("Do you realize that some poor soul")
        memory.waitFrames(30 * sleepTime)
        print("not only wrote the entire program for this by himself")
        memory.waitFrames(30 * sleepTime)
        print("And then wasted ten minutes to put in this ridiculous dialog?")
        memory.waitFrames(30 * sleepTime)
        print("Talk about not having a life.")
        memory.waitFrames(30 * sleepTime)
        print("Ah well, still have some time. Might as well shout out a few people.")
        memory.waitFrames(30 * sleepTime)
        print("First and most importantly, my wife for putting up with me for two years through this project.")
        memory.waitFrames(30 * sleepTime)
        print("My wife is the best!")
        memory.waitFrames(30 * sleepTime)
        print("Next, DwangoAC. He encouraged me to write my own code to do this.")
        memory.waitFrames(30 * sleepTime)
        print("And he put together the TASbot community which has been hugely helpful.")
        memory.waitFrames(30 * sleepTime)
        print("Shout out to DwangoAC and the TASbot Community. You guys rock!!!")
        memory.waitFrames(30 * sleepTime)
        print("Specifically from the TASbot Community, Inverted wrote the pathing logic for the Egg Hunt section.")
        memory.waitFrames(30 * sleepTime)
        print("You will see Inverted's work right before the final bosses.")
        memory.waitFrames(30 * sleepTime)
        print("Next, some people from the FFX speedrunning community.")
        memory.waitFrames(30 * sleepTime)
        print("CrimsonInferno, current world record holder for this category. Dude knows everything about this run!")
        memory.waitFrames(30 * sleepTime)
        print("Crimson re-wrote a great many boss fights for this project. From Spherimorph to Evrae Altana, and probably more.")
        memory.waitFrames(30 * sleepTime)
        print("Also, 'Rossy__' from the same community. Rossy helped me find a great many things in memory.")
        memory.waitFrames(30 * sleepTime)
        print("He also taught me a number of things about memory scans, pointers, etc. Dude is super smart.")
        memory.waitFrames(30 * sleepTime)
        print("Peppy too. He has found a few key things in memory too.")
        memory.waitFrames(30 * sleepTime)
        print("And last, Mr Tyton from the FFX speedrun community has re-written many pieces of my code.")
        memory.waitFrames(30 * sleepTime)
        print("He has also done a lot of optimizations I just couldn't get back to.")
        memory.waitFrames(30 * sleepTime)
        print("Legitimately Tyton pushed this project from decent towards excellent when I was running out of steam.")
        memory.waitFrames(30 * sleepTime)
        print("OK that wraps it up for this bit. I'll catch you when it's done.")
        memory.waitFrames(30 * sleepTime)

        memory.clickToControl()
        print("OMG finally! Let's get to it! (Do kids say that any more?)")
        FFXC.set_movement(0, 1)
        memory.waitFrames(30 * 1)
        FFXC.set_movement(-1, 1)
        memory.awaitEvent()
        FFXC.set_neutral()
        memory.waitFrames(30 * 0.2)
