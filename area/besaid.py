import battle.main
import logs
import memory.main
import menu
import screen
import targetPathing
import vars
import xbox

FFXC = xbox.controllerHandle()
gameVars = vars.varsHandle()


def Beach():
    print("Starting Besaid section. Beach")
    if gameVars.csr():
        FFXC.set_neutral()
        memory.main.awaitControl()
    else:
        FFXC.set_movement(0, -1)
        memory.main.awaitControl()
        memory.main.waitFrames(30 * 4.5)
        FFXC.set_neutral()

    # Pathing, lots of pathing.
    besaidBattles = 0
    goodBattles = 0
    checkpoint = 0
    lastCP = 0
    while memory.main.getMap() != 122:
        if checkpoint != lastCP:
            print("Checkpoint reached:", checkpoint)
            lastCP = checkpoint

        # map changes
        if checkpoint < 2 and memory.main.getMap() == 20:
            checkpoint = 2
            print("Map change. Checkpoint: ", checkpoint)
        elif checkpoint < 6 and memory.main.getMap() == 41:
            checkpoint = 6
            print("Map change. Checkpoint: ", checkpoint)
        elif checkpoint < 22 and memory.main.getMap() == 69:
            checkpoint = 22
            print("Map change. Checkpoint: ", checkpoint)
        elif checkpoint < 29 and memory.main.getMap() == 133:
            if not gameVars.csr():
                # You do remember the prayer?
                memory.main.clickToDiagProgress(9)
                memory.main.waitFrames(20)
                xbox.menuDown()
                xbox.menuB()
            checkpoint = 29
        elif checkpoint == 36 and memory.main.getMap() == 17:
            checkpoint = 37

        # Events
        elif memory.main.userControl():
            if checkpoint == 34:  # Into the temple for the first time
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 43:  # Wakka tent
                memory.main.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 44:  # Talk to Wakka
                while memory.main.userControl():
                    targetPathing.set_movement([15, 16])
                    xbox.tapB()
                FFXC.set_neutral()
                memory.main.clickToControl()
                checkpoint += 1
            elif checkpoint == 45:  # Exiting tent
                print("Exiting tent")
                memory.main.clickToEventTemple(7)
                checkpoint += 1

            # General pathing
            elif targetPathing.set_movement(targetPathing.besaid_1(checkpoint)):
                checkpoint += 1
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                battle.main.piranhas()
                besaidBattles += 1
                encounterID = memory.main.getEncounterID()
                if encounterID == 11 or (
                    encounterID == 12 and memory.main.battleType() == 1
                ):
                    goodBattles += 1
            elif memory.main.diagSkipPossible() or memory.main.menuOpen():
                xbox.tapB()
    logs.write_stats("piranha battles:")
    logs.write_stats(str(besaidBattles))
    # logs.writeStats("Optimal piranha battles:")
    # logs.writeStats(str(goodBattles))


def trials():
    checkpoint = 0

    while memory.main.getMap() != 69:
        if memory.main.userControl():
            # Spheres, glyphs, and pedestals
            if checkpoint == 1:  # First glyph
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 3:  # Second glyph
                memory.main.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 7:  # First Besaid sphere
                memory.main.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 12:  # Insert Besaid sphere
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 20:  # Touch the hidden door glyph
                while memory.main.userControl():
                    targetPathing.set_movement([-13, -33])
                    xbox.tapB()
                FFXC.set_neutral()
                memory.main.clickToControl3()
                checkpoint += 1
            elif checkpoint == 23:  # Second Besaid sphere
                while memory.main.userControl():
                    targetPathing.set_movement([-14, 31])
                    xbox.tapB()
                FFXC.set_neutral()
                memory.main.clickToControl3()
                checkpoint += 1
            elif checkpoint == 26:  # Insert Besaid sphere, and push to completion
                while memory.main.userControl():
                    targetPathing.set_movement([-13, -60])
                    xbox.tapB()
                FFXC.set_neutral()
                memory.main.clickToControl3()
                if gameVars.usePause():
                    memory.main.waitFrames(2)
                while memory.main.getMap() == 122:
                    FFXC.set_movement(0, 1)
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 34:  # Night, talk to Yuna and Wakka
                FFXC.set_movement(-1, -1)
                memory.main.awaitEvent()
                FFXC.set_neutral()

                memory.main.clickToDiagProgress(47)  # Wakka, "She's cute, ya?"
                while memory.main.shopMenuDialogueRow() != 1:
                    xbox.tapDown()
                xbox.tapB()
                checkpoint += 1
            elif checkpoint == 36:  # Sleep tight
                memory.main.clickToEventTemple(3)
                checkpoint += 1
            elif checkpoint > 15 and checkpoint < 37 and memory.main.getMap() == 252:
                checkpoint = 37
            elif checkpoint == 39:  # Dream about girls
                memory.main.clickToEventTemple(7)
                checkpoint += 1

            # General pathing
            elif targetPathing.set_movement(targetPathing.besaid_trials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()

            elif checkpoint == 32 and memory.main.menuOpen():
                # Name for Valefor
                xbox.nameAeon("Valefor")
                checkpoint += 1  # To the night scene

            # map changes
            elif checkpoint < 29 and memory.main.getMap() == 83:
                checkpoint = 29


def leaving():
    print("Ready to leave Besaid")
    memory.main.clickToControl()
    checkpoint = 0

    while memory.main.getMap() != 301:
        if memory.main.userControl():
            # Events
            if checkpoint == 0:  # Back into the village
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 3:  # Tent 1
                memory.main.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 5:  # Shopkeeper
                while memory.main.userControl():
                    targetPathing.set_movement([1, 15])
                    xbox.tapB()
                FFXC.set_neutral()
                while memory.main.shopMenuDialogueRow() != 1:
                    xbox.tapDown()
                xbox.tapB()
                memory.main.clickToControl3()
                checkpoint += 1
            elif checkpoint == 7:  # Exit tent
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 9:  # Tent 2
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 11:  # Good doggo
                memory.main.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 13:  # Exit tent
                memory.main.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 16:  # Exit the front gates
                memory.main.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 18:  # First tutorial
                logs.write_rng_track("###########################")
                logs.write_rng_track("Pre-tutorial array")
                logs.write_rng_track(memory.main.rng10Array(arrayLen=1))
                print("Tutorial - Tidus and Wakka")
                FFXC.set_movement(1, -1)
                memory.main.clickToEvent()
                FFXC.set_neutral()
                memory.main.clickToControl()
                checkpoint += 1
            elif checkpoint == 23:  # Second tutorial
                print("Tutorial - Lulu magic")
                while memory.main.userControl():
                    FFXC.set_movement(1, 0)
                FFXC.set_neutral()
                xbox.clickToBattle()
                battle.main.attack("none")
                xbox.clickToBattle()
                battle.main.thunder("none")
                memory.main.clickToControl()
                checkpoint += 1
            elif checkpoint == 24:  # Hilltop
                memory.main.clickToEventTemple(2)
                print("Ready for SS Liki menu - (var)", gameVars.earlyTidusGrid())
                if memory.main.getTidusSlvl() >= 3:
                    menu.liki()
                    gameVars.earlyTidusGridSetTrue()
                logs.write_rng_track("###########################")
                logs.write_rng_track("Pre-Kimahri array")
                logs.write_rng_track(memory.main.rng10Array(arrayLen=1))
                checkpoint += 1
            elif checkpoint in [59]:  # Beach, save sphere
                logs.write_rng_track("###########################")
                logs.write_rng_track("Pre-Sin array")
                logs.write_rng_track(memory.main.rng10Array(arrayLen=1))
                checkpoint += 1
            elif checkpoint in [60]:  # Beach, save sphere
                checkpoint += 1
            elif checkpoint == 70:
                checkpoint -= 2

            # General pathing
            elif targetPathing.set_movement(targetPathing.besaid_2(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()
            elif memory.main.cutsceneSkipPossible():
                xbox.skipScene(fast_mode=True)
            elif (
                checkpoint > 25 and checkpoint < 30 and screen.battle_screen()
            ):  # Kimahri fight
                FFXC.set_neutral()
                healCount = 0
                while memory.main.battleActive():
                    if screen.battle_screen():
                        battleHP = memory.main.getBattleHP()
                        enemyHP = memory.main.getEnemyCurrentHP()
                        if (
                            not gameVars.earlyTidusGrid()
                            and battleHP[0] < 120
                            and enemyHP[0] > 119
                        ):
                            if memory.main.rngSeed() == 31:
                                battle.main.attack("none")
                            else:
                                battle.main.usePotionCharacter(0, "l")
                                healCount += 1
                        else:
                            battle.main.attack("none")
                    elif memory.main.diagSkipPossible():
                        xbox.tapB()
                # logs.writeStats("Kimahri heal count:")
                # logs.writeStats(healCount)
                memory.main.clickToControl()
            # Valefor summon tutorial
            elif (
                checkpoint in [31, 32, 33, 34, 35, 36, 37, 38]
                and screen.battle_screen()
            ):
                xbox.clickToBattle()
                while not screen.turn_aeon():
                    if memory.main.turnReady():
                        if screen.turn_yuna():
                            battle.main.aeonSummon(0)
                        elif screen.turn_aeon():
                            pass
                        elif 1 not in memory.main.getActiveBattleFormation():
                            battle.main.buddySwapYuna()
                        else:
                            battle.main.defend()
                while memory.main.battleActive():
                    if memory.main.turnReady():
                        battle.main.aeonSpell(1)
                print("Now to open the menu")
                memory.main.clickToControl()
                memory.main.fullPartyFormat("Besaid")
                checkpoint += 1
            elif checkpoint == 39 and screen.battle_screen():  # Dark Attack tutorial
                battle.main.escapeAll()
                memory.main.clickToControl()
                memory.main.fullPartyFormat("Besaid2")
                checkpoint += 1
            elif (
                checkpoint > 39 and screen.battle_screen()
            ):  # One forced battle on the way out of Besaid
                battle.main.besaid()

            # Map changes
            elif (
                checkpoint > 10 and checkpoint < 24 and memory.main.getMap() == 67
            ):  # Hilltop
                checkpoint = 24
            elif checkpoint < 27 and memory.main.getMap() == 21:  # Kimahri map
                checkpoint = 27
            elif checkpoint < 32 and memory.main.getMap() == 22:
                checkpoint = 32
            elif checkpoint < 51 and memory.main.getMap() == 20:
                checkpoint = 51
            elif checkpoint < 59 and memory.main.getMap() == 19:
                checkpoint = 59
