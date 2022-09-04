import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_memory
import FFX_Logs
import FFX_targetPathing
import FFX_vars
import FFX_menu

FFXC = FFX_Xbox.controllerHandle()
gameVars = FFX_vars.varsHandle()


def Beach():
    print("Starting Besaid section. Beach")
    if gameVars.csr():
        FFXC.set_neutral()
        FFX_memory.awaitControl()
    else:
        FFXC.set_movement(0, -1)
        FFX_memory.awaitControl()
        FFX_memory.waitFrames(30 * 4.5)
        FFXC.set_neutral()

    # Pathing, lots of pathing.
    besaidBattles = 0
    goodBattles = 0
    checkpoint = 0
    lastCP = 0
    while FFX_memory.getMap() != 122:
        if checkpoint != lastCP:
            print("Checkpoint reached:", checkpoint)
            lastCP = checkpoint
        if FFX_memory.userControl():
            # Events
            if checkpoint == 34:  # Into the temple for the first time
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 43:  # Wakka tent
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 44:  # Talk to Wakka
                while FFX_memory.userControl():
                    FFX_targetPathing.setMovement([15, 16])
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                FFX_memory.clickToControl()
                checkpoint += 1
            elif checkpoint == 45:  # Exiting tent
                print("Exiting tent")
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1

            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.besaid1(checkpoint)) == True:
                checkpoint += 1
        else:
            FFXC.set_neutral()
            if FFX_Screen.BattleScreen():
                FFX_Battle.piranhas()
                besaidBattles += 1
                battleNum = FFX_memory.getBattleNum()
                if battleNum == 11 or (battleNum == 12 and FFX_memory.battleType() == 1):
                    goodBattles += 1
            elif FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
                FFX_Xbox.tapB()

            # map changes
            elif checkpoint < 2 and FFX_memory.getMap() == 20:
                checkpoint = 2
            elif checkpoint < 6 and FFX_memory.getMap() == 41:
                checkpoint = 6
            elif checkpoint < 22 and FFX_memory.getMap() == 69:
                checkpoint = 22
            elif checkpoint < 29 and FFX_memory.getMap() == 133:
                if not gameVars.csr():
                    # You do remember the prayer?
                    FFX_memory.clickToDiagProgress(9)
                    FFX_memory.waitFrames(20)
                    FFX_Xbox.menuDown()
                    FFX_Xbox.menuB()
                checkpoint = 29
            elif checkpoint == 36 and FFX_memory.getMap() == 17:
                checkpoint = 37
    FFX_Logs.writeStats("piranha battles:")
    FFX_Logs.writeStats(str(besaidBattles))
    FFX_Logs.writeStats("Optimal piranha battles:")
    FFX_Logs.writeStats(str(goodBattles))


def trials():
    checkpoint = 0

    while FFX_memory.getMap() != 69:
        if FFX_memory.userControl():
            # Spheres, glyphs, and pedestals
            if checkpoint == 1:  # First glyph
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 3:  # Second glyph
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 7:  # First Besaid sphere
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 12:  # Insert Besaid sphere
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 20:  # Touch the hidden door glyph
                while FFX_memory.userControl():
                    FFX_targetPathing.setMovement([-13, -33])
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 23:  # Second Besaid sphere
                while FFX_memory.userControl():
                    FFX_targetPathing.setMovement([-14, 31])
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 26:  # Insert Besaid sphere, and push to completion
                while FFX_memory.userControl():
                    FFX_targetPathing.setMovement([-13, -60])
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                FFX_memory.clickToControl3()
                if gameVars.usePause():
                    FFX_memory.waitFrames(2)
                while FFX_memory.getMap() == 122:
                    FFXC.set_movement(0, 1)
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 34:  # Night, talk to Yuna and Wakka
                FFXC.set_movement(-1, -1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()

                FFX_memory.clickToDiagProgress(47)  # Wakka, "She's cute, ya?"
                while FFX_memory.shopMenuDialogueRow() != 1:
                    FFX_Xbox.tapDown()
                FFX_Xbox.tapB()
                checkpoint += 1
            elif checkpoint == 36:  # Sleep tight
                FFX_memory.clickToEventTemple(3)
                checkpoint += 1
            elif checkpoint > 15 and checkpoint < 37 and FFX_memory.getMap() == 252:
                checkpoint = 37
            elif checkpoint == 39:  # Dream about girls
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1

            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.besaidTrials(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

            elif checkpoint == 32 and FFX_memory.menuOpen():
                # Name for Valefor
                FFX_Xbox.nameAeon("Valefor")
                checkpoint += 1  # To the night scene

            # map changes
            elif checkpoint < 29 and FFX_memory.getMap() == 83:
                checkpoint = 29


def leaving():
    print("Ready to leave Besaid")
    FFX_memory.clickToControl()
    checkpoint = 0

    while FFX_memory.getMap() != 301:
        if FFX_memory.userControl():
            # Events
            if checkpoint == 0:  # Back into the village
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 3:  # Tent 1
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 5:  # Shopkeeper
                FFXC.set_movement(-1, -1)
                FFX_memory.waitFrames(30 * 0.2)
                FFXC.set_neutral()
                FFX_Xbox.tapB()
                while FFX_memory.shopMenuDialogueRow() != 1:
                    FFX_Xbox.tapDown()
                FFX_Xbox.tapB()
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 7:  # Exit tent
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 9:  # Tent 2
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 11:  # Good doggo
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 13:  # Exit tent
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 16:  # Exit the front gates
                FFX_memory.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 18:  # First tutorial
                FFX_Logs.writeRNGTrack("###########################")
                FFX_Logs.writeRNGTrack("Pre-tutorial array")
                FFX_Logs.writeRNGTrack(FFX_memory.rng10Array(arrayLen=1))
                print("Tutorial - Tidus and Wakka")
                FFXC.set_movement(1, -1)
                FFX_memory.clickToEvent()
                FFXC.set_neutral()
                FFX_memory.clickToControl()
                checkpoint += 1
            elif checkpoint == 23:  # Second tutorial
                print("Tutorial - Lulu magic")
                while FFX_memory.userControl():
                    FFXC.set_movement(1, 0)
                FFXC.set_neutral()
                FFX_Xbox.clickToBattle()
                FFX_Battle.attack('none')
                FFX_Xbox.clickToBattle()
                FFX_Battle.thunder('none')
                FFX_memory.clickToControl()
                checkpoint += 1
            elif checkpoint == 24:  # Hilltop
                FFX_memory.clickToEventTemple(2)
                print("Ready for SS Liki menu - (var)",
                      gameVars.earlyTidusGrid())
                if FFX_memory.getTidusSlvl() >= 3:
                    FFX_menu.Liki()
                    gameVars.earlyTidusGridSetTrue()
                FFX_Logs.writeRNGTrack("###########################")
                FFX_Logs.writeRNGTrack("Pre-Kimahri array")
                FFX_Logs.writeRNGTrack(FFX_memory.rng10Array(arrayLen=1))
                checkpoint += 1
            elif checkpoint in [59]:  # Beach, save sphere
                FFX_Logs.writeRNGTrack("###########################")
                FFX_Logs.writeRNGTrack("Pre-Sin array")
                FFX_Logs.writeRNGTrack(FFX_memory.rng10Array(arrayLen=1))
                checkpoint += 1
            elif checkpoint in [60]:  # Beach, save sphere
                checkpoint += 1
            elif checkpoint == 70:
                checkpoint -= 2

            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.besaid2(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            elif FFX_memory.cutsceneSkipPossible():
                FFX_Xbox.skipScene(fast_mode=True)
            elif checkpoint > 25 and checkpoint < 30 and FFX_Screen.BattleScreen():  # Kimahri fight
                FFXC.set_neutral()
                healCount = 0
                while FFX_memory.battleActive():
                    if FFX_Screen.BattleScreen():
                        battleHP = FFX_memory.getBattleHP()
                        enemyHP = FFX_memory.getEnemyCurrentHP()
                        if not gameVars.earlyTidusGrid() and battleHP[0] < 120 and enemyHP[0] > 119:
                            if FFX_memory.rngSeed() == 31:
                                FFX_Battle.attack('none')
                            else:
                                FFX_Battle.usePotionCharacter(0, 'l')
                                healCount += 1
                        else:
                            FFX_Battle.attack('none')
                    elif FFX_memory.diagSkipPossible():
                        FFX_Xbox.tapB()
                FFX_Logs.writeStats("Kimahri heal count:")
                FFX_Logs.writeStats(healCount)
                FFX_memory.clickToControl()
            # Valefor summon tutorial
            elif checkpoint in [31,32,33,34,35,36,37,38] and FFX_Screen.BattleScreen():
                FFX_Xbox.clickToBattle()
                while not FFX_Screen.turnAeon():
                    if FFX_memory.turnReady():
                        if FFX_Screen.turnYuna():
                            FFX_Battle.aeonSummon(0)
                        elif FFX_Screen.turnAeon():
                            pass
                        elif not 1 in FFX_memory.getActiveBattleFormation():
                            FFX_Battle.buddySwapYuna()
                        else:
                            FFX_Battle.defend()
                while FFX_memory.battleActive():
                    if FFX_memory.turnReady():
                        FFX_Battle.aeonSpell(1)
                print("Now to open the menu")
                FFX_memory.clickToControl()
                FFX_memory.fullPartyFormat('Besaid')
                checkpoint += 1
            elif checkpoint == 39 and FFX_Screen.BattleScreen():  # Dark Attack tutorial
                FFX_Battle.escapeAll()
                FFX_memory.clickToControl()
                FFX_memory.fullPartyFormat('Besaid2')
                checkpoint += 1
            elif checkpoint > 39 and FFX_Screen.BattleScreen():  # One forced battle on the way out of Besaid
                FFX_Battle.besaid()

            # Map changes
            elif checkpoint > 10 and checkpoint < 24 and FFX_memory.getMap() == 67:  # Hilltop
                checkpoint = 24
            elif checkpoint < 27 and FFX_memory.getMap() == 21:  # Kimahri map
                checkpoint = 27
            elif checkpoint < 32 and FFX_memory.getMap() == 22:
                checkpoint = 32
            elif checkpoint < 51 and FFX_memory.getMap() == 20:
                checkpoint = 51
            elif checkpoint < 59 and FFX_memory.getMap() == 19:
                checkpoint = 59
