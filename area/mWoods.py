import xbox
import screen
import battle
import menu
import memory
import targetPathing
import vars
import logs
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def arrival(rikkuCharged):
    memory.clickToControl()
    memory.fullPartyFormat("mwoodsneedcharge")
    memory.closeMenu()

    # Rikkus charge, Fish Scales, and Arctic Winds
    woodsVars = [False, False, False]
    woodsVars[0] = rikkuCharged

    lastGil = 0  # for first chest
    checkpoint = 0
    totalBattles = 0
    while memory.getMap() != 221:  # All the way to O'aka
        if memory.userControl():
            # Events
            if checkpoint == 14:  # First chest
                if lastGil != memory.getGilvalue():
                    if lastGil == memory.getGilvalue() - 2000:
                        checkpoint += 1
                        print("Chest obtained. Updating checkpoint:", checkpoint)
                    else:
                        lastGil = memory.getGilvalue()
                else:
                    FFXC.set_movement(1, 1)
                    xbox.tapB()
            elif checkpoint == 59:
                if not woodsVars[0]:
                    checkpoint -= 2
                elif not woodsVars[1] and not woodsVars[2]:
                    checkpoint -= 2
                else:  # All good to proceed
                    checkpoint += 1

            # Map changes
            elif checkpoint < 18 and memory.getMap() == 241:
                checkpoint = 18
            elif checkpoint < 40 and memory.getMap() == 242:
                checkpoint = 40

            # General pathing
            elif targetPathing.setMovement(targetPathing.mWoods(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if screen.BattleScreen():
                print("variable check 1:", woodsVars)
                woodsVars = battle.mWoods(woodsVars)
                print("variable check 2:", woodsVars)
                if memory.overdriveState()[6] == 100:
                    memory.fullPartyFormat("mwoodsgotcharge")
                else:
                    memory.fullPartyFormat("mwoodsneedcharge")
                totalBattles += 1
            elif not memory.battleActive() and memory.diagSkipPossible():
                xbox.tapB()

    # logs.writeStats("Mac Woods battles:")
    # logs.writeStats(totalBattles)
    # Save sphere
    FFXC.set_movement(-1, 1)
    memory.waitFrames(2)
    memory.awaitControl()
    memory.waitFrames(1)
    memory.touchSaveSphere()
    FFXC.set_neutral()


def lakeRoad():
    memory.awaitControl()
    while not targetPathing.setMovement([174, -96]):
        pass
    while not targetPathing.setMovement([138, -83]):
        pass
    while not targetPathing.setMovement([101, -82]):
        pass
    while memory.userControl():
        FFXC.set_movement(0, 1)
        xbox.tapB()
    FFXC.set_neutral()
    menu.mWoods()  # Selling and buying, item sorting, etc
    memory.fullPartyFormat('spheri')
    while not targetPathing.setMovement([101, -72]):
        pass

    while not memory.battleActive():
        if memory.userControl():
            mapVal = memory.getMap()
            tidusPos = memory.getCoords()
            if mapVal == 221:
                if tidusPos[0] > 35:
                    targetPathing.setMovement([33, -35])
                else:
                    targetPathing.setMovement([-4, 15])
            elif mapVal == 248:
                if tidusPos[0] < -131:
                    targetPathing.setMovement([-129, -343])
                elif tidusPos[1] < -235:
                    targetPathing.setMovement([-49, -233])
                elif tidusPos[1] < -95:
                    targetPathing.setMovement([-1, -93])
                else:
                    targetPathing.setMovement([-1, 100])
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()

    FFXC.set_neutral()  # Engage Spherimorph

    battle.spherimorph()
    print("Battle is over.")
    memory.clickToControl()  # Jecht's memories


def lakeRoad2():
    FFXC.set_movement(0, -1)
    if gameVars.csr():
        checkpoint = 0
        while checkpoint < 5:
            if checkpoint == 0:
                if targetPathing.setMovement([-6, 25]):
                    checkpoint += 1
            elif checkpoint == 1:
                if targetPathing.setMovement([-4, -50]):
                    checkpoint += 1
            elif checkpoint == 2:
                if targetPathing.setMovement([-45, -212]):
                    checkpoint += 1
            elif checkpoint == 3:
                if targetPathing.setMovement([-49, -245]):
                    checkpoint += 1
            else:
                if targetPathing.setMovement([-145, -358]):
                    checkpoint += 1

    else:
        FFXC.set_movement(0, -1)
        memory.waitFrames(3)
        memory.awaitEvent()
        FFXC.set_neutral()

        memory.clickToControl()  # Auron's musings.
        print("Affection (before):", memory.affectionArray())
        memory.waitFrames(30 * 0.2)
        auronAffection = memory.affectionArray()[2]
        # Make sure we get Auron affection
        while memory.affectionArray()[2] == auronAffection:
            auronCoords = memory.getActorCoords(3)
            targetPathing.setMovement(auronCoords)
            xbox.tapB()
        print("Affection (after):", memory.affectionArray())
    while memory.userControl():
        FFXC.set_movement(-1, -1)
    FFXC.set_neutral()

    memory.clickToControl()  # Last map in the woods
    FFXC.set_movement(-1, 1)
    memory.waitFrames(2)
    memory.awaitEvent()
    FFXC.set_neutral()


def lake():
    print("Now to the frozen lake")
    if memory.getHP()[3] < 1000:  # Otherwise we under-level Tidus off of Crawler
        battle.healUp(fullMenuClose=False)

    memory.fullPartyFormat('crawler', fullMenuClose=False)
    menu.mLakeGrid()
    memory.awaitControl()

    print("------------------------------Affection array:")
    print(memory.affectionArray())
    print("------------------------------")

    checkpoint = 0
    while memory.getEncounterID() != 194:
        if memory.userControl():
            if targetPathing.setMovement(targetPathing.mLake(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.battleActive() and memory.getEncounterID() != 194:
                battle.fleeAll()
            elif memory.diagSkipPossible() or memory.menuOpen():
                xbox.menuB()
    xbox.clickToBattle()
    battle.negator()


def afterCrawler():
    print("------------------------------Affection array:")
    print(memory.affectionArray())
    print("------------------------------")
    memory.clickToControl()
    while memory.getMap() != 153:
        pos = memory.getCoords()
        if memory.userControl():
            if pos[1] > ((2.94 * pos[0]) + 505.21):
                FFXC.set_movement(1, 1)
            elif pos[1] < ((2.59 * pos[0]) + 469.19):
                FFXC.set_movement(-1, 1)
            else:
                FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()

    memory.clickToControl()

    checkpoint = 0
    lastCP = 0
    while checkpoint != 100:
        if lastCP != checkpoint:
            print("Checkpoint reached:", checkpoint)
            lastCP = checkpoint
        pos = memory.getCoords()
        if checkpoint == 0:
            if pos[0] > 130:
                checkpoint = 10
            else:
                if pos[1] < ((1.99 * pos[0]) + 5):
                    FFXC.set_movement(-1, -1)
                else:
                    FFXC.set_movement(-1, 0)
        elif checkpoint == 10:
            if pos[0] > 450:
                checkpoint = 20
            else:
                if pos[1] > ((0.37 * pos[0]) + 240):
                    FFXC.set_movement(-1, 1)
                elif pos[1] > 385:
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(-1, 0)
        elif checkpoint == 20:
            if pos[0] > 690:
                checkpoint = 40
            else:
                if pos[1] > ((-0.65 * pos[0]) + 693):
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(-1, 0)
        elif checkpoint == 30:
            if pos[1] < 100:
                checkpoint = 40
            else:
                if pos[1] < ((-1.49 * pos[0]) + 1235):
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(-1, 0)
        elif checkpoint == 40:
            if memory.getMap() == 106:
                FFXC.set_neutral()
                checkpoint = 100
            else:
                if pos[0] > 815:
                    FFXC.set_movement(1, 1)
                elif pos[0] < 810:
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(0, 1)
    print("End of Macalania Woods section. Next is temple section.")
