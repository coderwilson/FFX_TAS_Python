import FFX_Xbox
import FFX_Battle
import FFX_menu
import FFX_memory
import FFX_Logs
import FFX_targetPathing
import FFX_vars

FFXC = FFX_Xbox.controllerHandle()
gameVars = FFX_vars.varsHandle()

def arrival():
    print("Arrived at Kilika docks.")
    FFX_memory.clickToControl()

    checkpoint = 0
    while FFX_memory.getMap() != 18:
        if FFX_memory.userControl():
            # events
            if checkpoint == 4:  # Move into Yunas dance
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 6:  # Move into Yuna's dance
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 8:  # Exit the inn
                # Can be improved, there's a tiny ledge to get stuck on.
                FFXC.set_movement(-1, -1)
                FFX_memory.awaitEvent()
                FFX_memory.waitFrames(5)
                FFX_memory.awaitControl()
                checkpoint += 1
            elif checkpoint == 12:  # Back to first map
                FFX_memory.clickToEventTemple(3)
                checkpoint += 1
            elif checkpoint == 16:  # Talking to Wakka
                FFX_memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 18:  # Back to the map with the inn
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1

            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.Kilika1(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            elif FFX_memory.cutsceneSkipPossible():
                FFX_Xbox.skipSceneSpec()

            # Map changes
            elif checkpoint < 7 and FFX_memory.getMap() == 152:
                checkpoint = 7

def selectBestOfThree(comingBattles):
    if comingBattles == [["dinonix", "killer_bee"],["dinonix", "killer_bee"],["dinonix", "killer_bee"]]:
        return 99
    priority = [
        ["ragora", "killer_bee", "killer_bee"],
        ["dinonix", "yellow_element", "killer_bee"],
        ["yellow_element", "killer_bee"],
        ["dinonix", "yellow_element"],
        ["ragora"],
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
    import FFX_rngTrack

    valeforCharge = False
    if gameVars.csr():
        checkpoint = 0
    else:
        checkpoint = 2
    while FFX_memory.getMap() != 108:  # All the way into the trials
        if checkpoint == 101:  # Into the trials
            if not FFX_memory.userControl():
                FFXC.set_neutral()
                FFX_Xbox.tapB()
            elif FFX_memory.getCoords()[0] > 3:
                FFXC.set_movement(-1, 1)
            elif FFX_memory.getCoords()[0] < -3:
                FFXC.set_movement(1, 1)
            else:
                FFXC.set_movement(0, 1)
        elif FFX_memory.userControl():
            if checkpoint == 81 or checkpoint == 82:
                if valeforCharge == True:
                    checkpoint = 83
            if checkpoint == 83 and valeforCharge == False:
                checkpoint = 81

            # events
            if checkpoint == 9:  # Chest with Wakkas weapon Scout
                FFX_memory.clickToEventTemple(0)
                FFX_menu.woodsMenuing()
                checkpoint += 1
            elif checkpoint == 47:  # Luck sphere chest
                luckSlot = FFX_memory.getItemSlot(94)
                if luckSlot == 255:
                    FFX_targetPathing.setMovement([-250, 200])
                    FFX_Xbox.tapB()
                else:
                    checkpoint += 1
            elif checkpoint == 86:
                FFX_memory.touchSaveSphere()
                if not gameVars.didFullKilikMenu():
                    FFX_menu.Geneaux()
                checkpoint += 1
            elif checkpoint == 99:  #Lord O'holland
                while FFX_memory.userControl():
                    FFX_targetPathing.setMovement([-30, 45])
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                FFX_memory.clickToControl3()
                checkpoint += 1

            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.Kilika2(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                if checkpoint < 9:
                    FFX_Battle.lancetTutorial()
                    nextThree = FFX_rngTrack.comingBattles(area="kilika_woods", battleCount=3)
                    bestOfThree = selectBestOfThree(nextThree)
                    nextBattle = FFX_rngTrack.comingBattles(area="kilika_woods", battleCount=1)[0]
                    print("################# Next Battle:",nextBattle)
                elif checkpoint > 86:
                    FFX_Battle.Geneaux()
                else:
                    print("---------------This should be battle number:", kilikaBattles)
                    print("---------------Reminder (north-bound only):", nextThree)
                    valeforCharge = FFX_Battle.KilikaWoods(valeforCharge, bestOfThree, nextBattle)
                    nextBattle = FFX_rngTrack.comingBattles(area="kilika_woods", battleCount=1)[0]
                    print("##########################",nextBattle)
                    kilikaBattles += 1
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

            # Map changes
            elif checkpoint < 84 and FFX_memory.getMap() == 65:  # Stairs
                checkpoint = 84
            elif checkpoint < 94 and FFX_memory.getMap() == 78:  # Temple Entrance
                checkpoint = 94
            elif checkpoint < 96 and FFX_memory.getMap() == 96:  # Temple interior
                checkpoint = 96
    FFX_Logs.writeStats("Kilika battles (North):")
    FFX_Logs.writeStats(str(kilikaBattles))
    FFX_Logs.writeStats("Kilika optimal battles (North):")
    FFX_Logs.writeStats(str(optimalBattles))


def trials():
    FFX_memory.clickToControl()
    checkpoint = 0
    while FFX_memory.getMap() != 18:
        if FFX_memory.userControl():
            #Spheres and glyphs
            if checkpoint == 2:  # First sphere
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 5:  # Insert and remove, opens door
                FFX_memory.clickToEventTemple(0)
                FFX_memory.waitFrames(30 * 0.07)
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 9:  # Insert and remove, generate glyph
                FFX_memory.clickToEventTemple(0)
                FFX_memory.waitFrames(30 * 0.07)
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 11:  # Put the sphere out of the way
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 13:  # Touch glyph
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 18:  # Kilika sphere (in the way)
                FFX_memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 25:  # Kilika sphere (now out of the way)
                FFX_memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 27:  # Glyph sphere
                while not FFX_memory.diagSkipPossible():
                    FFX_targetPathing.setMovement([-21, -30])
                    FFX_memory.waitFrames(3)
                    FFXC.set_neutral()
                    FFX_memory.waitFrames(6)
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 33:  # Insert Glyph sphere
                FFX_memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 39:  # Pick up last Kilika sphere
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 50:  # Insert and remove, opens door
                FFX_memory.clickToEventTemple(0)
                FFX_memory.waitFrames(30 * 0.07)
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 53 and gameVars.csr():
                FFX_memory.awaitControl()
                FFXC.set_movement(0, 1)
                FFX_memory.waitFrames(2)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_Xbox.nameAeon("Ifrit")  # Set Ifrit name
                checkpoint = 55
            elif checkpoint == 54 and not gameVars.csr():  # Talk to Wakka
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 56:  # Leave inner sanctum
                FFXC.set_movement(0, -1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_Xbox.nameAeon("Ifrit")  # Set Ifrit name
                checkpoint += 1
            elif checkpoint == 57:  # Leaving the temple
                FFX_memory.clickToEventTemple(4)
                checkpoint += 1

            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.KilikaTrials(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

            # Map changes
            elif checkpoint < 53 and FFX_memory.getMap() == 45:  # Inner sanctum
                checkpoint = 53


def forest3():
    # First, re-order the party
    FFX_memory.fullPartyFormat('kilika')
    kilikaBattles = 0
    optimalBattles = 0
    checkpoint = 0
    while checkpoint < 69:  # All the way to the boats
        if FFX_memory.userControl():
            # Events
            if checkpoint == 68:
                FFXC.set_movement(0, -1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_Xbox.SkipDialog(0.3)
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint < 53 and FFX_memory.getMap() == 46:  # Exit woods
                checkpoint = 53
            elif checkpoint < 64 and FFX_memory.getMap() == 16:  # Map with boat
                checkpoint = 64

            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.Kilika3(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                FFX_Battle.KilikaWoods(True)
                kilikaBattles += 1
                if FFX_memory.getBattleNum() in [32, 34, 37]:
                    optimalBattles += 1
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

            # Map changes
            elif checkpoint < 53 and FFX_memory.getMap() == 46:  # Exit woods
                checkpoint = 53
            elif checkpoint < 64 and FFX_memory.getMap() == 16:  # Map with boat
                checkpoint = 64
    FFX_Logs.writeStats("Kilika battles (South):")
    FFX_Logs.writeStats(str(kilikaBattles))
    FFX_Logs.writeStats("Kilika optimal battles (South):")
    FFX_Logs.writeStats(str(optimalBattles))
