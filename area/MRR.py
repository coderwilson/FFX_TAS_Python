import time
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


def arrival():
    memory.clickToControl()
    memory.closeMenu()
    memory.fullPartyFormat('mrr1')
    memory.closeMenu()
    claskoSkip = True

    checkpoint = 0
    while memory.getMap() != 92:
        if memory.userControl():
            if gameVars.csr() and checkpoint == 1:
                print("CSR, skipping forward")
                checkpoint = 4
                print("Checkpoint reached:", checkpoint)
            elif checkpoint == 3:
                FFXC.set_movement(-1, 0)
                memory.waitFrames(30 * 0.7)
                FFXC.set_neutral()
                memory.waitFrames(30 * 0.4)
                FFXC.set_movement(1, -1)
                memory.waitFrames(30 * 0.035)
                FFXC.set_neutral()
                memory.waitFrames(30 * 2.3)
                if not memory.userControl():
                    battle.fleeAll()
                    battle.wrapUp()
                    FFXC.set_movement(-1, 0)
                    memory.waitFrames(30 * 0.7)
                    FFXC.set_neutral()
                    memory.waitFrames(30 * 0.4)
                    FFXC.set_movement(1, -1)
                    memory.waitFrames(30 * 0.035)
                    FFXC.set_neutral()
                    memory.waitFrames(30 * 0.3)
                print("Attempting skip.")
                xbox.menuB()

                # Now to wait for the skip to happen, or 60 second maximum limit
                startTime = time.time()
                # Max number of seconds that we will wait for the skip to occur.
                timeLimit = 60
                maxTime = startTime + timeLimit
                while memory.getActorCoords(6)[0] < -50:
                    currentTime = time.time()
                    if currentTime > maxTime:
                        print("Skip failed for some reason. Moving on without skip.")
                        claskoSkip = False
                        break
                memory.clickToControl()
                FFXC.set_neutral()
                checkpoint += 1
            elif targetPathing.setMovement(targetPathing.mrrStart(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if screen.BattleScreen():
                battle.fleeAll()
                memory.clickToControl3()
                if memory.getHP()[0] < 520:
                    battle.healUp()
            elif memory.menuOpen() or memory.diagSkipPossible():
                xbox.tapB()
    FFXC.set_neutral()
    print("Done with perlim MRR area, now for the real deal.")
    return claskoSkip


def mainPath():
    memory.awaitControl()
    critManip = False
    # Yuna complete, Kimahri complete, Valefor overdrive, Battle counter, Yuna grid complete, MRR phase
    status = [0, 0, 0, 1, 0, 0]
    print("Resetting checkpoint.")
    lastGilValue = 0
    checkpoint = 0
    battleCount = 0
    while memory.getMap() != 119:
        if status[0] == 1 and status[1] == 1 and status[2] == 0:
            status[2] = 2  # No need to do Valefor's overdrive and recharge.
        if status[0] == 1 and status[1] == 1 and status[2] == 2:
            # All pieces are complete. Move phase to final phase.
            status[5] = 3
        if memory.userControl():
            if checkpoint == 1:
                memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 4:
                print("Up the first lift")
                xbox.SkipDialog(1)
                checkpoint += 1
            elif checkpoint == 45:
                if status[0] == 0 or status[1] == 0 or status[2] != 2:
                    if targetPathing.setMovement(targetPathing.mrrMain(99)):
                        checkpoint -= 1
                else:
                    if targetPathing.setMovement(targetPathing.mrrMain(45)):
                        checkpoint += 1

            elif checkpoint == 46:
                print("Up the second lift.")
                FFXC.set_neutral()
                xbox.SkipDialog(1)
                checkpoint += 1
                print("Lift checkpoint:", checkpoint)
            elif checkpoint == 48:  # X-potion for safety
                if not memory.rngSeed() in [31]:
                    memory.clickToEventTemple(7)
                    print("Got X-potion")
                checkpoint += 1
            elif checkpoint >= 54 and checkpoint <= 56:  # 400 gil guy
                if memory.rngSeed() in [160, 31]:
                    checkpoint = 57
                elif memory.getGilvalue() != lastGilValue:  # check if we got the 400 from the guy
                    if memory.getGilvalue() == lastGilValue + 400:
                        print("We've procured the 400 gil from the guy.")
                        checkpoint = 57  # now to the actual lift
                    else:
                        lastGilValue = memory.getGilvalue()
                else:
                    targetPathing.setMovement(memory.mrrGuyCoords())
                    xbox.tapB()
            elif checkpoint == 58:
                print("Up the third lift")
                while memory.userControl():
                    targetPathing.setMovement([29, 227])
                    xbox.tapB()
                checkpoint += 1
            elif checkpoint == 66:
                xbox.SkipDialog(1)
                print("Up the final lift")
                print("======== Next Kimahri crit:", memory.nextCrit(character=3, charLuck=18, enemyLuck=15))
                checkpoint += 1
            elif checkpoint == 68:
                FFXC.set_movement(0, -1)
                memory.waitFrames(9)
                FFXC.set_movement(-1, -1)
                memory.waitFrames(9)
                checkpoint += 1
            elif checkpoint < 71 and memory.getMap() == 79:
                checkpoint = 71  # Into Battle Site zone (upper, cannon area)
            elif targetPathing.setMovement(targetPathing.mrrMain(checkpoint)):
                if checkpoint == 61:
                    if memory.nextCrit(character=3, charLuck=18, enemyLuck=15) in [2, 3, 4, 5, 6, 7, 9]:
                        critManip = True
                        # Try to end on 1.
                        print("+++++++++++ We can manip:", memory.nextCrit(character=3, charLuck=18, enemyLuck=15))
                        checkpoint = 59
                    else:
                        checkpoint += 1
                elif checkpoint == 90:
                    checkpoint = 62
                else:
                    checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.battleActive():
                print("Starting battle MRR")
                if checkpoint < 47:
                    status = battle.MRRbattle(status)
                    print("Status update:", status)
                    status[3] += 1
                else:
                    if battle.MRRmanip(kimMaxAdvance=9):
                        critManip = True

                if memory.getYunaSlvl() >= 8 and status[4] == 0:
                    print("Yuna has enough levels now. Going to do her grid.")
                    menu.mrrGridYuna()
                    print("Yunas gridding is complete for now.")
                    status[4] = 1
                if memory.getSLVLWakka() >= 7:
                    menu.mrrGrid2()
                memory.closeMenu()
                print("MRR battle complete")
                print("======== Next Kimahri crit:", memory.nextCrit(character=3, charLuck=18, enemyLuck=15))
                battleCount += 1
            elif memory.menuOpen():
                xbox.tapB()
            elif memory.diagSkipPossible():
                memory.clickToControl3()

            # Map changes
            elif checkpoint < 47 and memory.getMap() == 128:
                checkpoint = 47

        if memory.gameOver():
            return
    # logs.writeStats("MRR Battles:")
    # logs.writeStats(battleCount)
    logs.writeStats("MRR crit manip:")
    logs.writeStats(critManip)
    print("End of MRR section. Status:")
    print("[Yuna AP, Kim AP, Valefor OD steps, then other stuff]")
    print(status)


def battleSite():
    memory.awaitControl()
    if gameVars.getLStrike() >= 2:
        menu.equipWeapon(character=4, ability=0x8026, fullMenuClose=False)
    menu.battleSiteGrid()

    checkpoint = 0
    while checkpoint < 99:
        if memory.userControl():
            if checkpoint == 5:
                print("O'aka menu section")
                while memory.userControl():
                    targetPathing.setMovement([-45, 3425])
                    xbox.tapB()
                FFXC.set_neutral()
                menu.battleSiteOaka1()
                menu.battleSiteOaka2()
                print("======== Next Kimahri crit:", memory.nextCrit(character=3, charLuck=18, enemyLuck=15))
                checkpoint += 1
            elif checkpoint == 8:
                memory.touchSaveSphere()
                print("======== Next Kimahri crit:", memory.nextCrit(character=3, charLuck=18, enemyLuck=15))
                checkpoint += 1
            elif checkpoint == 12:
                FFXC.set_movement(1, 0)
                memory.waitFrames(45)
                checkpoint += 1
            elif checkpoint == 14:
                FFXC.set_movement(1, 0)
                memory.clickToEvent()
                FFXC.set_neutral()
                memory.waitFrames(9)
                xbox.tapB()  # Tell me when you're ready.
                FFXC.set_neutral()
                memory.waitFrames(15)
                xbox.menuDown()
                xbox.tapB()
                checkpoint = 100
            elif targetPathing.setMovement(targetPathing.battleSite(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()


def guiAndAftermath():
    battle.battleGui()

    checkpoint = 0
    while memory.getMap() != 93:
        if memory.userControl():
            if memory.getMap() == 131 and checkpoint < 4:
                checkpoint = 4
            elif checkpoint == 3:
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 7:
                FFXC.set_movement(-1, 0)
                memory.awaitEvent()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 15:
                FFXC.set_movement(0, 1)
                memory.awaitEvent()
                checkpoint += 1
            elif targetPathing.setMovement(targetPathing.battleSiteAftermath(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            memory.clickToControl3()
