import battle.boss
import battle.main
import logs
import memory.main
import menu
import targetPathing
import vars
import xbox

FFXC = xbox.controllerHandle()
gameVars = vars.varsHandle()


def arrival():
    # For certain seed/s, preferable to get luck sphere just to manipulate battles.
    # if memory.main.rngSeed() == 31 and gameVars.skipKilikaLuck():
    #    gameVars.dontSkipKilikaLuck()

    print("Arrived at Kilika docks.")
    memory.main.clickToControl()

    checkpoint = 0
    while memory.main.getMap() != 18:
        if memory.main.userControl():
            # events
            if checkpoint == 4:  # Move into Yunas dance
                memory.main.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 6:  # Move into Yuna's dance
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 8:  # Exit the inn
                # Can be improved, there's a tiny ledge to get stuck on.
                FFXC.set_movement(-1, -1)
                memory.main.awaitEvent()
                memory.main.waitFrames(5)
                memory.main.awaitControl()
                checkpoint += 1
            elif checkpoint == 12:  # Back to first map
                memory.main.clickToEventTemple(3)
                checkpoint += 1
            elif checkpoint == 16:  # Talking to Wakka
                memory.main.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 18:  # Back to the map with the inn
                memory.main.clickToEventTemple(7)
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.Kilika1(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()
            elif memory.main.cutsceneSkipPossible():
                xbox.skipSceneSpec()

            # Map changes
            elif checkpoint < 7 and memory.main.getMap() == 152:
                checkpoint = 7


def selectBestOfTwo(comingBattles):
    if comingBattles == [["dinonix", "killer_bee"], ["dinonix", "killer_bee"]]:
        return 99
    priority = [
        ["ragora", "killer_bee", "killer_bee"],
        ["dinonix", "yellow_element", "killer_bee"],
        ["yellow_element", "killer_bee"],
        ["ragora"],
        ["dinonix", "yellow_element"],
        ["ragora", "ragora"],
    ]
    for i in range(len(priority)):
        if priority[i] in comingBattles:
            print("--------------Best charge, battle num:", priority[i])
            return priority[i]
    return 99


def forest1():
    kilikaBattles = 0
    optimalBattles = 0
    nextThree = []
    nextBattle = []
    import rngTrack

    valeforCharge = False
    if gameVars.csr():
        checkpoint = 0
    else:
        checkpoint = 2
    while memory.main.getMap() != 108:  # All the way into the trials
        if checkpoint == 101:  # Into the trials
            if not memory.main.userControl():
                FFXC.set_neutral()
                xbox.tapB()
            elif memory.main.getCoords()[0] > 3:
                FFXC.set_movement(-1, 1)
            elif memory.main.getCoords()[0] < -3:
                FFXC.set_movement(1, 1)
            else:
                FFXC.set_movement(0, 1)
        elif memory.main.userControl():
            if checkpoint == 81 or checkpoint == 82:
                if valeforCharge:
                    checkpoint = 83
            if checkpoint == 83 and not valeforCharge:
                checkpoint = 81
            if checkpoint == 83 and memory.main.getMap() == 65:
                checkpoint = 84
            if checkpoint == 37 and gameVars.skipKilikaLuck():
                checkpoint = 60

            # events
            if checkpoint == 9:  # Chest with Wakkas weapon Scout
                memory.main.clickToEventTemple(0)
                menu.woodsMenuing()
                checkpoint += 1
            elif checkpoint == 47:  # Luck sphere chest
                luckSlot = memory.main.getItemSlot(94)
                if luckSlot == 255:
                    targetPathing.setMovement([-250, 200])
                    xbox.tapB()
                else:
                    checkpoint += 1
            elif checkpoint == 86:
                memory.main.touchSaveSphere()
                if not gameVars.didFullKilikMenu():
                    menu.Geneaux()
                checkpoint += 1
            elif checkpoint == 99:  # Lord O'holland
                while memory.main.userControl():
                    targetPathing.setMovement([-30, 45])
                    xbox.tapB()
                FFXC.set_neutral()
                memory.main.clickToControl3()
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.Kilika2(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                if checkpoint < 9:
                    battle.main.lancetTutorial()
                    nextTwo = rngTrack.comingBattles(area="kilika_woods", battleCount=2)
                    bestOfTwo = selectBestOfTwo(nextTwo)
                    nextBattle = rngTrack.comingBattles(
                        area="kilika_woods", battleCount=1
                    )[0]
                    print("################# Next Battle:", nextBattle)
                elif checkpoint > 86:
                    battle.boss.geneaux()
                else:
                    print("---------------This should be battle number:", kilikaBattles)
                    print("---------------Reminder (north-bound only):", nextThree)
                    valeforCharge = battle.main.KilikaWoods(
                        valeforCharge, bestOfTwo, nextBattle
                    )
                    nextBattle = rngTrack.comingBattles(
                        area="kilika_woods", battleCount=1
                    )[0]
                    print("##########################", nextBattle)
                    kilikaBattles += 1
                memory.main.fullPartyFormat("kilika")
            elif memory.main.diagSkipPossible():
                xbox.tapB()

            # Map changes
            elif checkpoint < 84 and memory.main.getMap() == 65:  # Stairs
                checkpoint = 84
            elif checkpoint < 94 and memory.main.getMap() == 78:  # Temple Entrance
                checkpoint = 94
            elif checkpoint < 96 and memory.main.getMap() == 96:  # Temple interior
                checkpoint = 96
    # logs.writeStats("Kilika battles (North):")
    # logs.writeStats(str(kilikaBattles))
    # logs.writeStats("Kilika optimal battles (North):")
    # logs.writeStats(str(optimalBattles))


def trials():
    memory.main.clickToControl()
    checkpoint = 0
    while memory.main.getMap() != 45:
        if memory.main.userControl():
            # Spheres and glyphs
            if checkpoint == 2:  # First sphere
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 5:  # Insert and remove, opens door
                memory.main.clickToEventTemple(0)
                memory.main.waitFrames(30 * 0.07)
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 9:  # Insert and remove, generate glyph
                memory.main.clickToEventTemple(0)
                memory.main.waitFrames(30 * 0.07)
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 11:  # Put the sphere out of the way
                memory.main.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 13:  # Touch glyph
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 18:  # Kilika sphere (in the way)
                memory.main.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 25:  # Kilika sphere (now out of the way)
                memory.main.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 27:  # Glyph sphere
                while not memory.main.diagSkipPossible():
                    targetPathing.setMovement([-21, -30])
                    if memory.main.userControl():
                        xbox.tapB()
                FFXC.set_neutral()
                memory.main.clickToControl3()
                checkpoint += 1
            elif checkpoint == 33:  # Insert Glyph sphere
                memory.main.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 39:  # Pick up last Kilika sphere
                memory.main.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 50:  # Insert and remove, opens door
                memory.main.clickToEventTemple(0)
                memory.main.waitFrames(30 * 0.07)
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            # elif checkpoint == 53 and gameVars.csr():
            #    memory.main.awaitControl()
            #    FFXC.set_movement(0, 1)
            #    memory.main.waitFrames(2)
            #    memory.main.awaitEvent()
            #    FFXC.set_neutral()
            #    xbox.nameAeon("Ifrit")  # Set Ifrit name
            #    checkpoint = 55
            elif checkpoint == 54 and not gameVars.csr():  # Talk to Wakka
                memory.main.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 56:  # Leave inner sanctum
                FFXC.set_movement(0, -1)
                memory.main.awaitEvent()
                FFXC.set_neutral()
                xbox.nameAeon("Ifrit")  # Set Ifrit name
                checkpoint += 1
            elif checkpoint == 57:  # Leaving the temple
                memory.main.clickToEventTemple(4)
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.KilikaTrials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()

            # Map changes
            elif checkpoint < 53 and memory.main.getMap() == 45:  # Inner sanctum
                checkpoint = 53


def trialsEnd():
    # Talking to Wakka
    while memory.main.getStoryProgress() < 346:
        if memory.main.userControl():
            if memory.main.getCoords()[0] < -28:
                targetPathing.setMovement([-10, -23])
            else:
                targetPathing.setMovement([-20, 1])
                xbox.tapB()
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()

    # Leave the chamber, then name Ifrit.
    memory.main.clickToControl3()
    while memory.main.userControl():
        FFXC.set_movement(0, -1)
    FFXC.set_neutral()
    xbox.nameAeon("Ifrit")  # Set Ifrit name

    while memory.main.getMap() != 18:
        if memory.main.userControl():
            FFXC.set_movement(0, -1)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()


def forest3():
    # First, re-order the party
    memory.main.fullPartyFormat("kilika")
    kilikaBattles = 0
    optimalBattles = 0
    checkpoint = 0
    while checkpoint < 69:  # All the way to the boats
        if memory.main.userControl():
            # Events
            if checkpoint == 68:
                FFXC.set_movement(0, -1)
                memory.main.awaitEvent()
                FFXC.set_neutral()
                xbox.SkipDialog(0.3)
                memory.main.clickToControl3()
                checkpoint += 1
            elif checkpoint < 53 and memory.main.getMap() == 46:  # Exit woods
                checkpoint = 53
            elif checkpoint < 64 and memory.main.getMap() == 16:  # Map with boat
                checkpoint = 64

            # General pathing
            elif targetPathing.setMovement(targetPathing.Kilika3(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                battle.main.KilikaWoods(True)
                kilikaBattles += 1
                if memory.main.getEncounterID() in [32, 34, 37]:
                    optimalBattles += 1
                if kilikaBattles == 1 and memory.main.rngSeed() == 31:
                    memory.main.fullPartyFormat("kilikawoodsbackup")
                else:
                    memory.main.fullPartyFormat("kilika")
            elif memory.main.diagSkipPossible():
                xbox.tapB()

            # Map changes
            elif checkpoint < 53 and memory.main.getMap() == 46:  # Exit woods
                checkpoint = 53
            elif checkpoint < 64 and memory.main.getMap() == 16:  # Map with boat
                checkpoint = 64
    # logs.writeStats("Kilika battles (South):")
    # logs.writeStats(str(kilikaBattles))
    # logs.writeStats("Kilika optimal battles (South):")
    # logs.writeStats(str(optimalBattles))
