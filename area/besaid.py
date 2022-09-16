import xbox
import screen
import battle
import memory
import logs
import targetPathing
import vars
import menu

FFXC = xbox.controllerHandle()
gameVars = vars.varsHandle()


def Beach():
    print("Starting Besaid section. Beach")
    if gameVars.csr():
        FFXC.set_neutral()
        memory.awaitControl()
    else:
        FFXC.set_movement(0, -1)
        memory.awaitControl()
        memory.waitFrames(30 * 4.5)
        FFXC.set_neutral()

    # Pathing, lots of pathing.
    besaidBattles = 0
    goodBattles = 0
    checkpoint = 0
    lastCP = 0
    while memory.getMap() != 122:
        if checkpoint != lastCP:
            print("Checkpoint reached:", checkpoint)
            lastCP = checkpoint
        if memory.userControl():
            # Events
            if checkpoint == 34:  # Into the temple for the first time
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 43:  # Wakka tent
                memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 44:  # Talk to Wakka
                while memory.userControl():
                    targetPathing.setMovement([15, 16])
                    xbox.tapB()
                FFXC.set_neutral()
                memory.clickToControl()
                checkpoint += 1
            elif checkpoint == 45:  # Exiting tent
                print("Exiting tent")
                memory.clickToEventTemple(7)
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.besaid1(checkpoint)):
                checkpoint += 1
        else:
            FFXC.set_neutral()
            if screen.BattleScreen():
                battle.piranhas()
                besaidBattles += 1
                encounterID = memory.getEncounterID()
                if encounterID == 11 or (encounterID == 12 and memory.battleType() == 1):
                    goodBattles += 1
            elif memory.diagSkipPossible() or memory.menuOpen():
                xbox.tapB()

            # map changes
            elif checkpoint < 2 and memory.getMap() == 20:
                checkpoint = 2
            elif checkpoint < 6 and memory.getMap() == 41:
                checkpoint = 6
            elif checkpoint < 22 and memory.getMap() == 69:
                checkpoint = 22
            elif checkpoint < 29 and memory.getMap() == 133:
                if not gameVars.csr():
                    # You do remember the prayer?
                    memory.clickToDiagProgress(9)
                    memory.waitFrames(20)
                    xbox.menuDown()
                    xbox.menuB()
                checkpoint = 29
            elif checkpoint == 36 and memory.getMap() == 17:
                checkpoint = 37
    logs.writeStats("piranha battles:")
    logs.writeStats(str(besaidBattles))
    # logs.writeStats("Optimal piranha battles:")
    # logs.writeStats(str(goodBattles))


def trials():
    checkpoint = 0

    while memory.getMap() != 69:
        if memory.userControl():
            # Spheres, glyphs, and pedestals
            if checkpoint == 1:  # First glyph
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 3:  # Second glyph
                memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 7:  # First Besaid sphere
                memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 12:  # Insert Besaid sphere
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 20:  # Touch the hidden door glyph
                while memory.userControl():
                    targetPathing.setMovement([-13, -33])
                    xbox.tapB()
                FFXC.set_neutral()
                memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 23:  # Second Besaid sphere
                while memory.userControl():
                    targetPathing.setMovement([-14, 31])
                    xbox.tapB()
                FFXC.set_neutral()
                memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 26:  # Insert Besaid sphere, and push to completion
                while memory.userControl():
                    targetPathing.setMovement([-13, -60])
                    xbox.tapB()
                FFXC.set_neutral()
                memory.clickToControl3()
                if gameVars.usePause():
                    memory.waitFrames(2)
                while memory.getMap() == 122:
                    FFXC.set_movement(0, 1)
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 34:  # Night, talk to Yuna and Wakka
                FFXC.set_movement(-1, -1)
                memory.awaitEvent()
                FFXC.set_neutral()

                memory.clickToDiagProgress(47)  # Wakka, "She's cute, ya?"
                while memory.shopMenuDialogueRow() != 1:
                    xbox.tapDown()
                xbox.tapB()
                checkpoint += 1
            elif checkpoint == 36:  # Sleep tight
                memory.clickToEventTemple(3)
                checkpoint += 1
            elif checkpoint > 15 and checkpoint < 37 and memory.getMap() == 252:
                checkpoint = 37
            elif checkpoint == 39:  # Dream about girls
                memory.clickToEventTemple(7)
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.besaidTrials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()

            elif checkpoint == 32 and memory.menuOpen():
                # Name for Valefor
                xbox.nameAeon("Valefor")
                checkpoint += 1  # To the night scene

            # map changes
            elif checkpoint < 29 and memory.getMap() == 83:
                checkpoint = 29


def leaving():
    print("Ready to leave Besaid")
    memory.clickToControl()
    checkpoint = 0

    while memory.getMap() != 301:
        if memory.userControl():
            # Events
            if checkpoint == 0:  # Back into the village
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 3:  # Tent 1
                memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 5:  # Shopkeeper
                FFXC.set_movement(-1, -1)
                memory.waitFrames(30 * 0.2)
                FFXC.set_neutral()
                xbox.tapB()
                while memory.shopMenuDialogueRow() != 1:
                    xbox.tapDown()
                xbox.tapB()
                memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 7:  # Exit tent
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 9:  # Tent 2
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 11:  # Good doggo
                memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 13:  # Exit tent
                memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 16:  # Exit the front gates
                memory.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 18:  # First tutorial
                logs.writeRNGTrack("###########################")
                logs.writeRNGTrack("Pre-tutorial array")
                logs.writeRNGTrack(memory.rng10Array(arrayLen=1))
                print("Tutorial - Tidus and Wakka")
                FFXC.set_movement(1, -1)
                memory.clickToEvent()
                FFXC.set_neutral()
                memory.clickToControl()
                checkpoint += 1
            elif checkpoint == 23:  # Second tutorial
                print("Tutorial - Lulu magic")
                while memory.userControl():
                    FFXC.set_movement(1, 0)
                FFXC.set_neutral()
                xbox.clickToBattle()
                battle.attack('none')
                xbox.clickToBattle()
                battle.thunder('none')
                memory.clickToControl()
                checkpoint += 1
            elif checkpoint == 24:  # Hilltop
                memory.clickToEventTemple(2)
                print("Ready for SS Liki menu - (var)",
                      gameVars.earlyTidusGrid())
                if memory.getTidusSlvl() >= 3:
                    menu.Liki()
                    gameVars.earlyTidusGridSetTrue()
                logs.writeRNGTrack("###########################")
                logs.writeRNGTrack("Pre-Kimahri array")
                logs.writeRNGTrack(memory.rng10Array(arrayLen=1))
                checkpoint += 1
            elif checkpoint in [59]:  # Beach, save sphere
                logs.writeRNGTrack("###########################")
                logs.writeRNGTrack("Pre-Sin array")
                logs.writeRNGTrack(memory.rng10Array(arrayLen=1))
                checkpoint += 1
            elif checkpoint in [60]:  # Beach, save sphere
                checkpoint += 1
            elif checkpoint == 70:
                checkpoint -= 2

            # General pathing
            elif targetPathing.setMovement(targetPathing.besaid2(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()
            elif memory.cutsceneSkipPossible():
                xbox.skipScene(fast_mode=True)
            elif checkpoint > 25 and checkpoint < 30 and screen.BattleScreen():  # Kimahri fight
                FFXC.set_neutral()
                healCount = 0
                while memory.battleActive():
                    if screen.BattleScreen():
                        battleHP = memory.getBattleHP()
                        enemyHP = memory.getEnemyCurrentHP()
                        if not gameVars.earlyTidusGrid() and battleHP[0] < 120 and enemyHP[0] > 119:
                            if memory.rngSeed() == 31:
                                battle.attack('none')
                            else:
                                battle.usePotionCharacter(0, 'l')
                                healCount += 1
                        else:
                            battle.attack('none')
                    elif memory.diagSkipPossible():
                        xbox.tapB()
                # logs.writeStats("Kimahri heal count:")
                # logs.writeStats(healCount)
                memory.clickToControl()
            # Valefor summon tutorial
            elif checkpoint in [31, 32, 33, 34, 35, 36, 37, 38] and screen.BattleScreen():
                xbox.clickToBattle()
                while not screen.turnAeon():
                    if memory.turnReady():
                        if screen.turnYuna():
                            battle.aeonSummon(0)
                        elif screen.turnAeon():
                            pass
                        elif 1 not in memory.getActiveBattleFormation():
                            battle.buddySwapYuna()
                        else:
                            battle.defend()
                while memory.battleActive():
                    if memory.turnReady():
                        battle.aeonSpell(1)
                print("Now to open the menu")
                memory.clickToControl()
                memory.fullPartyFormat('Besaid')
                checkpoint += 1
            elif checkpoint == 39 and screen.BattleScreen():  # Dark Attack tutorial
                battle.escapeAll()
                memory.clickToControl()
                memory.fullPartyFormat('Besaid2')
                checkpoint += 1
            elif checkpoint > 39 and screen.BattleScreen():  # One forced battle on the way out of Besaid
                battle.besaid()

            # Map changes
            elif checkpoint > 10 and checkpoint < 24 and memory.getMap() == 67:  # Hilltop
                checkpoint = 24
            elif checkpoint < 27 and memory.getMap() == 21:  # Kimahri map
                checkpoint = 27
            elif checkpoint < 32 and memory.getMap() == 22:
                checkpoint = 32
            elif checkpoint < 51 and memory.getMap() == 20:
                checkpoint = 51
            elif checkpoint < 59 and memory.getMap() == 19:
                checkpoint = 59
