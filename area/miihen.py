import xbox
import screen
import battle.main
import memory.main
import logs
import targetPathing
import vars
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def arrival():
    print("Waiting for Yuna/Tidus to stop laughing.")
    FFXC.set_movement(0, 1)
    memory.main.clickToControl()
    print("Now onward to scenes and Mi'ihen skip. Good luck!")
    miihenSkip = False
    battleCount = 0
    SDencounterID = 0

    checkpoint = 0
    while memory.main.getMap() != 120:
        if memory.main.userControl():
            # Miihen skip attempt
            if checkpoint > 3 and checkpoint < 11:
                if gameVars.csr():
                    # Only run this branch if CSR is online.
                    tidusCoords = memory.main.getCoords()
                    hunterCoords = memory.main.miihenGuyCoords()
                    hunterDistance = abs(tidusCoords[1] - hunterCoords[1]) \
                        + abs(tidusCoords[0] - hunterCoords[0])

                    # Get spear
                    if memory.main.hunterSpear():
                        checkpoint = 11
                    elif hunterDistance < 200 or checkpoint in [6, 7, 8, 9, 10]:
                        targetPathing.setMovement(hunterCoords)
                        xbox.tapB()

                    elif targetPathing.setMovement(targetPathing.miihen(checkpoint)):
                        checkpoint += 1
                        print("Checkpoint reached:", checkpoint)

                else:
                    # Run this branch on a normal Any% run, no CSR
                    tidusCoords = memory.main.getCoords()
                    hunterCoords = memory.main.miihenGuyCoords()
                    if hunterCoords[1] < tidusCoords[1]:
                        checkpoint = 11
                        print("**Late for Mi'ihen skip, forcing recovery.")
                    elif checkpoint == 6:
                        FFXC.set_neutral()
                        memory.main.waitFrames(9)
                        print("Updating checkpoint due to late skip.")
                        print("Checkpoint reached:", checkpoint)
                        checkpoint += 1
                    elif checkpoint == 7:
                        if memory.main.getCoords()[1] > 1356.5:  # Into position
                            if memory.main.getCoords()[0] < -44:
                                FFXC.set_movement(1, 0)
                                memory.main.waitFrames(30 * 0.06)
                                FFXC.set_neutral()
                                memory.main.waitFrames(30 * 0.09)
                            else:
                                checkpoint += 1
                                print("Close to the spot")
                            print(memory.main.getCoords())
                        elif memory.main.getCoords()[0] < -43.5:  # Into position
                            FFXC.set_movement(1, 1)
                            memory.main.waitFrames(2)
                            FFXC.set_neutral()
                            memory.main.waitFrames(3)
                        else:
                            FFXC.set_movement(0, 1)
                            memory.main.waitFrames(2)
                            FFXC.set_neutral()
                            memory.main.waitFrames(3)
                    elif checkpoint == 8:
                        if memory.main.getCoords()[0] > -43.5:  # Into position
                            checkpoint += 1
                            print("Adjusting for horizontal position - complete")
                            print(memory.main.getCoords())
                        else:
                            FFXC.set_movement(1, 0)
                            memory.main.waitFrames(2)
                            FFXC.set_neutral()
                            memory.main.waitFrames(3)
                    elif checkpoint == 9:
                        if memory.main.getCoords()[1] > 1358.5:  # Into position
                            checkpoint = 10
                            print("Stopped and ready for the skip.")
                            print(memory.main.getCoords())
                        else:
                            FFXC.set_movement(0, 1)
                            memory.main.waitFrames(2)
                            FFXC.set_neutral()
                            memory.main.waitFrames(4)
                    elif checkpoint == 10:
                        # Spear guy's position when we start moving.
                        if memory.main.miihenGuyCoords()[1] < 1380:
                            print("Skip engaging!!! Good luck!")
                            # Greater number for spear guy's position means we will start moving faster.
                            # Smaller number means moving later.
                            FFXC.set_movement(0, 1)
                            if gameVars.usePause():
                                memory.main.waitFrames(2)
                            else:
                                memory.main.waitFrames(3)
                            # Walk into the guy mashing B (or X, or whatever the key is)
                            xbox.SkipDialog(0.3)
                            FFXC.set_neutral()  # Stop trying to move. (recommended by Crimson)
                            print("Starting special skipping.")
                            xbox.SkipDialogSpecial(3)  # Mash two buttons
                            print("End special skipping.")
                            print("Should now be able to see if it worked.")
                            # Don't move, avoiding a possible extra battle
                            memory.main.waitFrames(30 * 3.5)
                            memory.main.clickToControl3()
                            print("Mark 1")
                            memory.main.waitFrames(30 * 1)
                            print("Mark 2")
                            try:
                                if memory.main.lucilleMiihenCoords()[1] > 1400 and memory.main.userControl():
                                    miihenSkip = True
                                else:
                                    memory.main.clickToControl3()
                            except Exception:
                                miihenSkip = False
                            print("Skip successful:", miihenSkip)
                            checkpoint += 1
                    elif targetPathing.setMovement(targetPathing.miihen(checkpoint)):
                        checkpoint += 1
                        print("Checkpoint reached:", checkpoint)
            elif checkpoint == 11 and not memory.main.hunterSpear():
                targetPathing.setMovement(
                    [memory.main.miihenGuyCoords()[0], memory.main.miihenGuyCoords()[1]])
                xbox.tapB()

            # Map changes
            elif checkpoint < 15 and memory.main.getMap() == 120:
                checkpoint = 15
            # General pathing
            elif targetPathing.setMovement(targetPathing.miihen(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.turnReady():
                if checkpoint < 4:  # Tutorial battle with Auron
                    while memory.main.battleActive():
                        xbox.tapB()
                    FFXC.set_movement(0, 1)
                    while not memory.main.userControl():
                        xbox.tapB()
                    while not memory.main.menuOpen():
                        xbox.tapY()
                    FFXC.set_neutral()
                elif checkpoint == 25 and not memory.main.battleActive():  # Shelinda dialog
                    FFXC.set_neutral()
                    xbox.tapB()
                else:
                    FFXC.set_neutral()
                    print("Starting battle")
                    battleCount += 1
                    battle.main.MiihenRoad()
                    print("Battle complete")
                if memory.main.overdriveState2()[1] >= 43:
                    if gameVars.selfDestructGet(): 
                        memory.main.fullPartyFormat('tidkimwak', fullMenuClose=False)
                    else:
                        memory.main.fullPartyFormat('djose', fullMenuClose=False)
                else:
                    memory.main.fullPartyFormat('kilikawoods1', fullMenuClose=False)
                hpCheck = memory.main.getHP()
                print("------------------ HP check:", hpCheck)
                if hpCheck[0] < 520:
                    battle.main.healUp()
                else:
                    print("No need to heal up. Moving onward.")
                memory.main.closeMenu()

                # Kimahri manip
                nextCritKim = memory.main.nextCrit(character=3, charLuck=18, enemyLuck=15)
                print("#### Next Kimahri crit:", nextCritKim)
            else:
                FFXC.set_movement(1, 1)
                if memory.main.menuOpen():
                    FFXC.set_value('BtnB', 1)
                    memory.main.waitFrames(2)
                    FFXC.set_value('BtnB', 0)
                    memory.main.waitFrames(3)
                elif memory.main.diagSkipPossible():
                    FFXC.set_value('BtnB', 1)
                    memory.main.waitFrames(2)
                    FFXC.set_value('BtnB', 0)
                    memory.main.waitFrames(3)
    print("Mi'ihen skip status:", miihenSkip)
    return [gameVars.selfDestructGet(), battleCount, SDencounterID, miihenSkip]


def arrival2(selfDestruct, battleCount, SDencounterID):
    print("Start of the second map")
    checkpoint = 15
    while memory.main.getMap() != 171:
        if memory.main.userControl():

            # Map changes
            if checkpoint == 27:
                if memory.main.getCoords()[1] > 2810:
                    checkpoint += 1
                elif gameVars.csr():
                    checkpoint += 1
                else:
                    FFXC.set_neutral()
                    xbox.SkipDialog(1)
                    memory.main.clickToControl3()
                    checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.miihen(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if screen.BattleScreen():
                battleCount += 1
                if checkpoint == 27 and not memory.main.battleActive():  # Shelinda dialog
                    xbox.tapB()
                else:
                    print("Starting battle")
                    battle.main.MiihenRoad()
                    print("Battle complete")
                if memory.main.overdriveState2()[1] >= 43:
                    if gameVars.selfDestructGet(): 
                        memory.main.fullPartyFormat('tidkimwak')
                    else:
                        memory.main.fullPartyFormat('djose')
                else:
                    memory.main.fullPartyFormat('kilikawoods1')
            elif memory.main.menuOpen():
                xbox.tapB()
            elif memory.main.diagSkipPossible():  # Exclude during the Miihen skip.
                if checkpoint < 6 or checkpoint > 12:
                    xbox.tapB()

            # Map changes
            elif checkpoint < 13 and memory.main.getMap() == 120:
                checkpoint = 13
            elif checkpoint < 20 and memory.main.getMap() == 127:
                checkpoint = 20
            elif checkpoint < 31 and memory.main.getMap() == 58:
                checkpoint = 31
    return [gameVars.selfDestructGet(), battleCount, SDencounterID]


def midPoint():
    checkpoint = 0
    while memory.main.getMap() != 115:
        if memory.main.userControl():
            pDownSlot = memory.main.getItemSlot(6)
            if memory.main.getMap() == 58:
                memory.main.fullPartyFormat('tidkimwak')
                FFXC.set_movement(0, 1)
                memory.main.awaitEvent()
                FFXC.set_neutral()
            #elif checkpoint == 2 and memory.main.getItemCountSlot(pDownSlot) >= 10:
            #    checkpoint = 4
            elif checkpoint in [2, 3]:
                checkpoint = 4
            elif checkpoint == 5:
                FFXC.set_movement(0, -1)
                memory.main.awaitEvent()
                FFXC.set_neutral()
                checkpoint = 4
            elif targetPathing.setMovement(targetPathing.miihenAgency(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()
            elif memory.main.battleActive():
                FFXC.set_neutral()
                print("Mi'ihen - ready for Chocobo Eater")
                battle.main.chocoEater()
                print("Mi'ihen - Chocobo Eater complete")


# Starts just after the save sphere.
def lowRoad(selfDestruct, battleCount, SDencounterID):
    checkpoint = 0
    memory.main.fullPartyFormat('djose')
    while memory.main.getMap() != 79:
        if memory.main.userControl():
            # Utility stuff
            if checkpoint == 2:
                memory.main.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 26 and not gameVars.selfDestructGet():
                checkpoint = 24
            elif checkpoint == 34:  # Talk to guard, then Seymour
                FFXC.set_movement(0, 1)
                memory.main.awaitEvent()
                FFXC.set_neutral()
                memory.main.waitFrames(30 * 0.2)
                memory.main.clickToControl()
                FFXC.set_movement(0, -1)
                memory.main.waitFrames(30 * 4)
                FFXC.set_neutral()
                checkpoint += 1

            # Map changes
            elif checkpoint < 17 and memory.main.getMap() == 116:
                checkpoint = 17
            elif checkpoint < 28 and memory.main.getMap() == 59:
                checkpoint = 28

            # General pathing
            elif targetPathing.setMovement(targetPathing.lowRoad(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
            elif checkpoint == 25:  # Shelinda dialog
                xbox.tapB()
        else:
            FFXC.set_neutral()
            if screen.BattleScreen():
                battleCount += 1
                print("Starting battle")
                battle.main.MiihenRoad()
                print("Battle complete")
            elif memory.main.menuOpen():
                xbox.tapB()
            elif memory.main.diagSkipPossible():
                if checkpoint < 6 or checkpoint > 12:
                    xbox.tapB()
    # logs.writeStats('Miihen encounters:')
    # logs.writeStats(battleCount)


def wrapUp():
    print("Now ready to meet Seymour")
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 5)
    FFXC.set_neutral()

    memory.main.clickToControl()
    FFXC.set_movement(0, 1)
    xbox.SkipDialog(4.5)
    FFXC.set_neutral()
    xbox.SkipDialog(2.5)
    FFXC.set_movement(0, -1)
    xbox.SkipDialog(12)
    FFXC.set_neutral()
    memory.main.clickToControl()  # Seymour scene
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 12)
    FFXC.set_neutral()
