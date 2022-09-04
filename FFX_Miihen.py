import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_memory
import FFX_Logs
import FFX_targetPathing
import FFX_vars
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()


def arrival():
    print("Waiting for Yuna/Tidus to stop laughing.")
    FFXC.set_movement(0, 1)
    FFX_memory.clickToControl()
    print("Now onward to scenes and Mi'ihen skip. Good luck!")

    FFX_memory.fullPartyFormat('djose')
    miihenSkip = False
    battleCount = 0
    SDencounterID = 0

    checkpoint = 0
    while FFX_memory.getMap() != 120:
        if FFX_memory.userControl():
            # Miihen skip attempt
            if checkpoint > 3 and checkpoint < 11:
                if gameVars.csr():
                    # Only run this branch if CSR is online.
                    tidusCoords = FFX_memory.getCoords()
                    hunterCoords = FFX_memory.miihenGuyCoords()
                    hunterDistance = abs(tidusCoords[1] - hunterCoords[1]) \
                        + abs(tidusCoords[0] - hunterCoords[0])

                    # Get spear
                    if FFX_memory.hunterSpear():
                        checkpoint = 11
                    elif hunterDistance < 200 or checkpoint in [6, 7, 8, 9, 10]:
                        FFX_targetPathing.setMovement(hunterCoords)
                        FFX_Xbox.tapB()

                    elif FFX_targetPathing.setMovement(FFX_targetPathing.miihen(checkpoint)):
                        checkpoint += 1
                        print("Checkpoint reached:", checkpoint)

                else:
                    # Run this branch on a normal Any% run, no CSR
                    tidusCoords = FFX_memory.getCoords()
                    hunterCoords = FFX_memory.miihenGuyCoords()
                    if hunterCoords[1] < tidusCoords[1]:
                        checkpoint = 11
                        print("**Late for Mi'ihen skip, forcing recovery.")
                    elif checkpoint == 6:
                        FFXC.set_neutral()
                        FFX_memory.waitFrames(9)
                        print("Updating checkpoint due to late skip.")
                        print("Checkpoint reached:", checkpoint)
                        checkpoint += 1
                    elif checkpoint == 7:
                        if FFX_memory.getCoords()[1] > 1356.5:  # Into position
                            if FFX_memory.getCoords()[0] < -44:
                                FFXC.set_movement(1, 0)
                                FFX_memory.waitFrames(30 * 0.06)
                                FFXC.set_neutral()
                                FFX_memory.waitFrames(30 * 0.09)
                            else:
                                checkpoint += 1
                                print("Close to the spot")
                            print(FFX_memory.getCoords())
                        elif FFX_memory.getCoords()[0] < -43.5:  # Into position
                            FFXC.set_movement(1, 1)
                            FFX_memory.waitFrames(2)
                            FFXC.set_neutral()
                            FFX_memory.waitFrames(3)
                        else:
                            FFXC.set_movement(0, 1)
                            FFX_memory.waitFrames(2)
                            FFXC.set_neutral()
                            FFX_memory.waitFrames(3)
                    elif checkpoint == 8:
                        if FFX_memory.getCoords()[0] > -43.5:  # Into position
                            checkpoint += 1
                            print("Adjusting for horizontal position - complete")
                            print(FFX_memory.getCoords())
                        else:
                            FFXC.set_movement(1, 0)
                            FFX_memory.waitFrames(2)
                            FFXC.set_neutral()
                            FFX_memory.waitFrames(3)
                    elif checkpoint == 9:
                        if FFX_memory.getCoords()[1] > 1358.5:  # Into position
                            checkpoint = 10
                            print("Stopped and ready for the skip.")
                            print(FFX_memory.getCoords())
                        else:
                            FFXC.set_movement(0, 1)
                            FFX_memory.waitFrames(2)
                            FFXC.set_neutral()
                            FFX_memory.waitFrames(4)
                    elif checkpoint == 10:
                        # Spear guy's position when we start moving.
                        if FFX_memory.miihenGuyCoords()[1] < 1380:
                            print("Skip engaging!!! Good luck!")
                            # Greater number for spear guy's position means we will start moving faster.
                            # Smaller number means moving later.
                            FFXC.set_movement(0, 1)
                            if gameVars.usePause():
                                FFX_memory.waitFrames(2)
                            else:
                                FFX_memory.waitFrames(3)
                            # Walk into the guy mashing B (or X, or whatever the key is)
                            FFX_Xbox.SkipDialog(0.3)
                            FFXC.set_neutral()  # Stop trying to move. (recommended by Crimson)
                            print("Starting special skipping.")
                            FFX_Xbox.SkipDialogSpecial(3)  # Mash two buttons
                            print("End special skipping.")
                            print("Should now be able to see if it worked.")
                            # Don't move, avoiding a possible extra battle
                            FFX_memory.waitFrames(30 * 3.5)
                            FFX_memory.clickToControl3()
                            print("Mark 1")
                            FFX_memory.waitFrames(30 * 1)
                            print("Mark 2")
                            try:
                                if FFX_memory.lucilleMiihenCoords()[1] > 1400 and FFX_memory.userControl():
                                    miihenSkip = True
                                else:
                                    FFX_memory.clickToControl3()
                            except:
                                miihenSkip = False
                            print("Skip successful:", miihenSkip)
                            checkpoint += 1
                    elif FFX_targetPathing.setMovement(FFX_targetPathing.miihen(checkpoint)):
                        checkpoint += 1
                        print("Checkpoint reached:", checkpoint)
            elif checkpoint == 11 and not FFX_memory.hunterSpear():
                FFX_targetPathing.setMovement(
                    [FFX_memory.miihenGuyCoords()[0], FFX_memory.miihenGuyCoords()[1]])
                FFX_Xbox.tapB()

            # Map changes
            elif checkpoint < 15 and FFX_memory.getMap() == 120:
                checkpoint = 15
            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.miihen(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.turnReady():
                if checkpoint < 4:  # Tutorial battle with Auron
                    while FFX_memory.battleActive():
                        FFX_Xbox.tapB()
                    FFXC.set_movement(0, 1)
                    while not FFX_memory.userControl():
                        FFX_Xbox.tapB()
                    while not FFX_memory.menuOpen():
                        FFX_Xbox.tapY()
                    FFXC.set_neutral()
                    FFX_memory.fullPartyFormat('djose')
                    FFX_memory.closeMenu()
                elif checkpoint == 25 and not FFX_memory.battleActive():  # Shelinda dialog
                    FFXC.set_neutral()
                    FFX_Xbox.tapB()
                else:
                    FFXC.set_neutral()
                    print("Starting battle")
                    battleCount += 1
                    FFX_Battle.MiihenRoad()
                    print("Battle complete")

                # Kimahri manip
                nextCritKim = FFX_memory.nextCrit(character=3, charLuck=18, enemyLuck=15)
                print("#### Next Kimahri crit: ", nextCritKim)
            else:
                FFXC.set_movement(1, 1)
                if FFX_memory.menuOpen():
                    FFXC.set_value('BtnB', 1)
                    FFX_memory.waitFrames(2)
                    FFXC.set_value('BtnB', 0)
                    FFX_memory.waitFrames(3)
                elif FFX_memory.diagSkipPossible():
                    FFXC.set_value('BtnB', 1)
                    FFX_memory.waitFrames(2)
                    FFXC.set_value('BtnB', 0)
                    FFX_memory.waitFrames(3)
    print("Mi'ihen skip status:", miihenSkip)
    return [gameVars.selfDestructGet(), battleCount, SDencounterID, miihenSkip]


def arrival2(selfDestruct, battleCount, SDencounterID):
    print("Start of the second map")
    checkpoint = 15
    while FFX_memory.getMap() != 171:
        if FFX_memory.userControl():

            # Map changes
            if checkpoint == 27:
                if FFX_memory.getCoords()[1] > 2810:
                    checkpoint += 1
                elif gameVars.csr():
                    checkpoint += 1
                else:
                    FFXC.set_neutral()
                    FFX_Xbox.SkipDialog(1)
                    FFX_memory.clickToControl3()
                    checkpoint += 1

            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.miihen(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_Screen.BattleScreen():
                battleCount += 1
                if checkpoint == 27 and not FFX_memory.battleActive():  # Shelinda dialog
                    FFX_Xbox.tapB()
                else:
                    print("Starting battle")
                    FFX_Battle.MiihenRoad()
                    print("Battle complete")
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif FFX_memory.diagSkipPossible():  # Exclude during the Miihen skip.
                if checkpoint < 6 or checkpoint > 12:
                    FFX_Xbox.tapB()

            # Map changes
            elif checkpoint < 13 and FFX_memory.getMap() == 120:
                checkpoint = 13
            elif checkpoint < 20 and FFX_memory.getMap() == 127:
                checkpoint = 20
            elif checkpoint < 31 and FFX_memory.getMap() == 58:
                checkpoint = 31
    return [gameVars.selfDestructGet(), battleCount, SDencounterID]


def midPoint():
    checkpoint = 0
    FFX_memory.fullPartyFormat('tidkimwak')
    while not FFX_memory.battleActive():
        if FFX_memory.userControl():
            pDownSlot = FFX_memory.getItemSlot(6)
            if FFX_memory.getMap() != 171:
                FFXC.set_movement(0, 1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
            elif checkpoint == 2 and FFX_memory.getItemCountSlot(pDownSlot) >= 10:
                checkpoint = 4
            elif checkpoint == 3:
                checkpoint = 4
            elif checkpoint == 5:
                FFXC.set_movement(0, -1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                checkpoint = 4
            elif FFX_targetPathing.setMovement(FFX_targetPathing.miihenAgency(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

    print("Mi'ihen - ready for Chocobo Eater")
    FFX_Battle.chocoEater()
    print("Mi'ihen - Chocobo Eater complete")


# Starts just after the save sphere.
def lowRoad(selfDestruct, battleCount, SDencounterID):
    checkpoint = 0
    FFX_memory.fullPartyFormat('djose')
    while FFX_memory.getMap() != 79:
        if FFX_memory.userControl():
            # Utility stuff
            if checkpoint == 2:
                FFX_memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 26 and not gameVars.selfDestructGet():
                checkpoint = 24
            elif checkpoint == 34:  # Talk to guard, then Seymour
                FFXC.set_movement(0, 1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_memory.waitFrames(30 * 0.2)
                FFX_memory.clickToControl()
                FFXC.set_movement(0, -1)
                FFX_memory.waitFrames(30 * 4)
                FFXC.set_neutral()
                checkpoint += 1

            # Map changes
            elif checkpoint < 17 and FFX_memory.getMap() == 116:
                checkpoint = 17
            elif checkpoint < 28 and FFX_memory.getMap() == 59:
                checkpoint = 28

            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.lowRoad(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
            elif checkpoint == 25:  # Shelinda dialog
                FFX_Xbox.tapB()
        else:
            FFXC.set_neutral()
            if FFX_Screen.BattleScreen():
                battleCount += 1
                print("Starting battle")
                FFX_Battle.MiihenRoad()
                print("Battle complete")
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif FFX_memory.diagSkipPossible():
                if checkpoint < 6 or checkpoint > 12:
                    FFX_Xbox.tapB()
    FFX_Logs.writeStats('Miihen encounters:')
    FFX_Logs.writeStats(battleCount)


def wrapUp():
    print("Now ready to meet Seymour")
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 5)
    FFXC.set_neutral()

    FFX_memory.clickToControl()
    FFXC.set_movement(0, 1)
    FFX_Xbox.SkipDialog(4.5)
    FFXC.set_neutral()
    FFX_Xbox.SkipDialog(2.5)
    FFXC.set_movement(0, -1)
    FFX_Xbox.SkipDialog(12)
    FFXC.set_neutral()
    FFX_memory.clickToControl()  # Seymour scene
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 12)
    FFXC.set_neutral()
