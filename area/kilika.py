import xbox
import battle
import menu
import memory
import logs
import targetPathing
import vars

FFXC = xbox.controllerHandle()
gameVars = vars.varsHandle()


def arrival():
    # For certain seed/s, preferable to get luck sphere just to manipulate battles.
    if memory.rngSeed() == 31 and gameVars.skipKilikaLuck():
        gameVars.dontSkipKilikaLuck()

    print("Arrived at Kilika docks.")
    memory.clickToControl()

    checkpoint = 0
    while memory.getMap() != 18:
        if memory.userControl():
            # events
            if checkpoint == 4:  # Move into Yunas dance
                memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 6:  # Move into Yuna's dance
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 8:  # Exit the inn
                # Can be improved, there's a tiny ledge to get stuck on.
                FFXC.set_movement(-1, -1)
                memory.awaitEvent()
                memory.waitFrames(5)
                memory.awaitControl()
                checkpoint += 1
            elif checkpoint == 12:  # Back to first map
                memory.clickToEventTemple(3)
                checkpoint += 1
            elif checkpoint == 16:  # Talking to Wakka
                memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 18:  # Back to the map with the inn
                memory.clickToEventTemple(7)
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.Kilika1(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()
            elif memory.cutsceneSkipPossible():
                xbox.skipSceneSpec()

            # Map changes
            elif checkpoint < 7 and memory.getMap() == 152:
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
        ["ragora", "ragora"]]
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
    while memory.getMap() != 108:  # All the way into the trials
        if checkpoint == 101:  # Into the trials
            if not memory.userControl():
                FFXC.set_neutral()
                xbox.tapB()
            elif memory.getCoords()[0] > 3:
                FFXC.set_movement(-1, 1)
            elif memory.getCoords()[0] < -3:
                FFXC.set_movement(1, 1)
            else:
                FFXC.set_movement(0, 1)
        elif memory.userControl():
            if checkpoint == 81 or checkpoint == 82:
                if valeforCharge:
                    checkpoint = 83
            if checkpoint == 83 and not valeforCharge:
                checkpoint = 81
            if checkpoint == 83 and memory.getMap() == 65:
                checkpoint = 84
            if checkpoint == 37 and gameVars.skipKilikaLuck():
                checkpoint = 60

            # events
            if checkpoint == 9:  # Chest with Wakkas weapon Scout
                memory.clickToEventTemple(0)
                menu.woodsMenuing()
                checkpoint += 1
            elif checkpoint == 47:  # Luck sphere chest
                luckSlot = memory.getItemSlot(94)
                if luckSlot == 255:
                    targetPathing.setMovement([-250, 200])
                    xbox.tapB()
                else:
                    checkpoint += 1
            elif checkpoint == 86:
                memory.touchSaveSphere()
                if not gameVars.didFullKilikMenu():
                    menu.Geneaux()
                checkpoint += 1
            elif checkpoint == 99:  # Lord O'holland
                while memory.userControl():
                    targetPathing.setMovement([-30, 45])
                    xbox.tapB()
                FFXC.set_neutral()
                memory.clickToControl3()
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.Kilika2(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

        else:
            FFXC.set_neutral()
            if memory.battleActive():
                if checkpoint < 9:
                    battle.lancetTutorial()
                    nextTwo = rngTrack.comingBattles(area="kilika_woods", battleCount=2)
                    bestOfTwo = selectBestOfTwo(nextTwo)
                    nextBattle = rngTrack.comingBattles(area="kilika_woods", battleCount=1)[0]
                    print("################# Next Battle:", nextBattle)
                elif checkpoint > 86:
                    battle.Geneaux()
                else:
                    print("---------------This should be battle number:", kilikaBattles)
                    print("---------------Reminder (north-bound only):", nextThree)
                    valeforCharge = battle.KilikaWoods(valeforCharge, bestOfTwo, nextBattle)
                    nextBattle = rngTrack.comingBattles(area="kilika_woods", battleCount=1)[0]
                    print("##########################", nextBattle)
                    kilikaBattles += 1
                memory.fullPartyFormat('kilika')
            elif memory.diagSkipPossible():
                xbox.tapB()

            # Map changes
            elif checkpoint < 84 and memory.getMap() == 65:  # Stairs
                checkpoint = 84
            elif checkpoint < 94 and memory.getMap() == 78:  # Temple Entrance
                checkpoint = 94
            elif checkpoint < 96 and memory.getMap() == 96:  # Temple interior
                checkpoint = 96
    # logs.writeStats("Kilika battles (North):")
    # logs.writeStats(str(kilikaBattles))
    # logs.writeStats("Kilika optimal battles (North):")
    # logs.writeStats(str(optimalBattles))


def trials():
    memory.clickToControl()
    checkpoint = 0
    while memory.getMap() != 18:
        if memory.userControl():
            # Spheres and glyphs
            if checkpoint == 2:  # First sphere
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 5:  # Insert and remove, opens door
                memory.clickToEventTemple(0)
                memory.waitFrames(30 * 0.07)
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 9:  # Insert and remove, generate glyph
                memory.clickToEventTemple(0)
                memory.waitFrames(30 * 0.07)
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 11:  # Put the sphere out of the way
                memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 13:  # Touch glyph
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 18:  # Kilika sphere (in the way)
                memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 25:  # Kilika sphere (now out of the way)
                memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 27:  # Glyph sphere
                while not memory.diagSkipPossible():
                    targetPathing.setMovement([-21, -30])
                    memory.waitFrames(3)
                    FFXC.set_neutral()
                    memory.waitFrames(6)
                    xbox.tapB()
                FFXC.set_neutral()
                memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 33:  # Insert Glyph sphere
                memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 39:  # Pick up last Kilika sphere
                memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 50:  # Insert and remove, opens door
                memory.clickToEventTemple(0)
                memory.waitFrames(30 * 0.07)
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 53 and gameVars.csr():
                memory.awaitControl()
                FFXC.set_movement(0, 1)
                memory.waitFrames(2)
                memory.awaitEvent()
                FFXC.set_neutral()
                xbox.nameAeon("Ifrit")  # Set Ifrit name
                checkpoint = 55
            elif checkpoint == 54 and not gameVars.csr():  # Talk to Wakka
                memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 56:  # Leave inner sanctum
                FFXC.set_movement(0, -1)
                memory.awaitEvent()
                FFXC.set_neutral()
                xbox.nameAeon("Ifrit")  # Set Ifrit name
                checkpoint += 1
            elif checkpoint == 57:  # Leaving the temple
                memory.clickToEventTemple(4)
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.KilikaTrials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()

            # Map changes
            elif checkpoint < 53 and memory.getMap() == 45:  # Inner sanctum
                checkpoint = 53


def forest3():
    # First, re-order the party
    memory.fullPartyFormat('kilika')
    kilikaBattles = 0
    optimalBattles = 0
    checkpoint = 0
    while checkpoint < 69:  # All the way to the boats
        if memory.userControl():
            # Events
            if checkpoint == 68:
                FFXC.set_movement(0, -1)
                memory.awaitEvent()
                FFXC.set_neutral()
                xbox.SkipDialog(0.3)
                memory.clickToControl3()
                checkpoint += 1
            elif checkpoint < 53 and memory.getMap() == 46:  # Exit woods
                checkpoint = 53
            elif checkpoint < 64 and memory.getMap() == 16:  # Map with boat
                checkpoint = 64

            # General pathing
            elif targetPathing.setMovement(targetPathing.Kilika3(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.battleActive():
                battle.KilikaWoods(True)
                kilikaBattles += 1
                if memory.getEncounterID() in [32, 34, 37]:
                    optimalBattles += 1
            elif memory.diagSkipPossible():
                xbox.tapB()

            # Map changes
            elif checkpoint < 53 and memory.getMap() == 46:  # Exit woods
                checkpoint = 53
            elif checkpoint < 64 and memory.getMap() == 16:  # Map with boat
                checkpoint = 64
    # logs.writeStats("Kilika battles (South):")
    # logs.writeStats(str(kilikaBattles))
    # logs.writeStats("Kilika optimal battles (South):")
    # logs.writeStats(str(optimalBattles))
