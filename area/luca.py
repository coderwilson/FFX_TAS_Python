import battle.main
import logs
import memory.main
import menu
import targetPathing
import vars
import xbox

gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def arrival():
    if not gameVars.csr():
        xbox.skipStoredScene(2)
    print("Starting Luca section")
    memory.main.clickToControl()

    earlyHaste = 0
    checkpoint = 0
    while checkpoint < 56:
        if memory.main.userControl():
            # Map changes
            if checkpoint < 5 and memory.main.getMap() == 268:
                checkpoint = 5
                print("Map change:", checkpoint)
            elif checkpoint < 10 and memory.main.getMap() == 123:  # Front of the Blitz dome
                print("Map change:", checkpoint)
                checkpoint = 10
            elif checkpoint < 13 and memory.main.getMap() == 77:
                print("Map change:", checkpoint)
                checkpoint = 13
            elif checkpoint < 15 and memory.main.getMap() == 104:
                print("Map change:", checkpoint)
                checkpoint = 15

            # events
            if checkpoint in [5, 6]:  # Seymour intro scene
                memory.main.awaitControl()
                print("Event: Seymour intro scene")
                FFXC.set_movement(1, 0)
                memory.main.awaitEvent()
                FFXC.set_neutral()
                if not gameVars.csr():
                    memory.main.clickToDiagProgress(18)  # Seymour scene
                    xbox.awaitSave(index=2)

                    memory.main.clickToDiagProgress(
                        82)  # Let's go over the basics
                    xbox.SkipDialog(1)
                while memory.main.blitzCursor() != 12:
                    xbox.tapA()
                xbox.menuB()
                if not gameVars.csr():
                    xbox.SkipDialogSpecial(45)  # Skip the Wakka Face scene
                memory.main.clickToControl()
                checkpoint = 7
                print("Seymour scene, updating checkpoint.")
            elif checkpoint == 12:  # Upside down T section
                print("Event: Upside down T section")
                memory.main.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 23:  # Into the bar
                print("Event: Into the bar looking for Auron")
                FFXC.set_movement(0, 1)
                memory.main.awaitEvent()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 33:  # Back to the front of the Blitz dome
                print("Event: Back to Blitz dome entrance")
                memory.main.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 36:  # To the docks
                print("Event: Towards the docks")
                FFXC.set_movement(0, 1)
                memory.main.waitFrames(9)
                memory.main.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 40:
                print("Event: First battle")
                FFXC.set_movement(0, 1)
                memory.main.awaitEvent()
                FFXC.set_neutral()
                battle.main.LucaWorkers()
                checkpoint += 1
            elif checkpoint == 42:  # First and second battles
                print("Event: Second battle")
                FFXC.set_movement(1, 1)
                memory.main.awaitEvent()
                FFXC.set_neutral()
                battle.main.LucaWorkers()
                checkpoint += 1
            elif checkpoint == 44:  # Third battle
                print("Tidus XP:", memory.main.getTidusXP())
                if memory.main.getTidusXP() >= 312:
                    FFXC.set_neutral()
                    earlyHaste = menu.LucaWorkers()
                    if earlyHaste != 0:
                        earlyHaste = 2
                print("Event: Third battle")
                FFXC.set_movement(1, 0)
                memory.main.awaitEvent()
                FFXC.set_neutral()
                battle.main.LucaWorkers2(earlyHaste)
                print("Tidus XP:", memory.main.getTidusXP())
                memory.main.clickToControl()
                if earlyHaste == 0 and memory.main.getTidusXP() >= 312:
                    earlyHaste = menu.LucaWorkers()

                checkpoint += 1
            elif checkpoint == 46 or checkpoint == 55:
                print("Event: Touch Save Sphere")
                memory.main.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 48:  # Oblitzerator
                print("Event: Oblitzerator fight")
                FFXC.set_movement(1, 0)
                memory.main.awaitEvent()
                FFXC.set_neutral()
                battle.main.Oblitzerator(earlyHaste)
                checkpoint += 1
            elif checkpoint == 50:
                memory.main.clickToEventTemple(4)

                if earlyHaste == 0:
                    earlyHaste = menu.LucaWorkers() - 1
                checkpoint += 1
            elif checkpoint == 52:
                memory.main.clickToEventTemple(5)
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.Luca1(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()
            elif memory.main.cutsceneSkipPossible():
                xbox.skipScene()

    logs.writeStats("Early Haste:")
    logs.writeStats(earlyHaste)
    gameVars.earlyHasteSet(earlyHaste)

    print("##Checking for thunderstrike weapons for Tidus or Wakka")
    thunderStrike = memory.main.checkThunderStrike()
    if thunderStrike == 0:
        print("##Neither character got a thunderstrike weapon.")
    elif thunderStrike == 1:
        print("##Tidus got a thunderstrike weapon.")
    elif thunderStrike == 2:
        print("##Wakka got a thunderstrike weapon.")
    else:
        print("##Both Tidus and Wakka somehow got a thunderstrike weapon.")

    logs.writeStats("Thunderstrike results:")
    logs.writeStats(thunderStrike)

    if thunderStrike != 0:
        if thunderStrike % 2 == 1:
            print("Equipping Tidus")
            fullClose = True
            menu.equipWeapon(
                character=0, ability=0x8026, fullMenuClose=fullClose)
    gameVars.setLStrike(thunderStrike)


def blitzStart():
    print("Starting the Blitzball game via lots of storyline.")
    checkpoint = 0
    while memory.main.getStoryProgress() < 519:
        if memory.main.userControl():
            if memory.main.getMap() == 72 and checkpoint < 3:
                checkpoint = 3
            elif memory.main.getMap() == 72 and memory.main.getCoords()[0] < -18 \
                    and checkpoint < 5:
                checkpoint = 5
            elif memory.main.getMap() == 72 and memory.main.getCoords()[0] > -15 \
                    and checkpoint >= 5:
                checkpoint = 4
            elif checkpoint == 8:
                targetPathing.setMovement([-111, -4])
                xbox.tapB()
            elif targetPathing.setMovement(targetPathing.LucaPreBlitz(checkpoint)):
                checkpoint += 1
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()


def afterBlitz():
    xbox.clickToBattle()
    encounterID = 0
    checkpoint = 0
    while checkpoint < 36:
        if memory.main.userControl():
            # Events
            if checkpoint == 8:  # First chest
                if gameVars.earlyHaste() == -1:
                    menu.lateHaste()
                    memory.main.closeMenu()
                print("First chest")
                while memory.main.userControl():
                    targetPathing.setMovement([-635, -410])
                    xbox.menuB()
                FFXC.set_neutral()
                memory.main.clickToControl()
                checkpoint += 1
            elif checkpoint == 10:  # Second chest
                print("Second chest")
                while memory.main.userControl():
                    targetPathing.setMovement([-620, -424])
                    xbox.menuB()
                FFXC.set_neutral()
                memory.main.clickToControl()
                checkpoint += 1
            elif checkpoint == 20:  # Target Auron
                if not gameVars.csr():
                    # First Auron affection, always zero
                    while memory.main.affectionArray()[2] == 0:
                        auronCoords = memory.main.getActorCoords(3)
                        targetPathing.setMovement(auronCoords)
                        xbox.tapB()
                checkpoint += 1  # After affection changes
            elif checkpoint == 35:  # Bring the party together
                print("Bring the party together")
                memory.main.clickToEventTemple(1)
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.Luca3(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                encounterID += 1
                print("After-Blitz Battle Number:", encounterID)
                if encounterID == 1:
                    battle.main.afterBlitz1(gameVars.earlyHaste())
                elif encounterID == 2:
                    xbox.clickToBattle()
                    battle.main.attack('none')  # Hardest boss in the game.
                    print("Well that boss was difficult.")
                    memory.main.waitFrames(30 * 6)
                elif encounterID == 3:
                    if gameVars.earlyHaste() == -1:
                        battle.main.afterBlitz3LateHaste(gameVars.earlyHaste())
                    else:
                        battle.main.afterBlitz3(gameVars.earlyHaste())
                    memory.main.clickToControl()
                    memory.main.waitFrames(4)
                    FFXC.set_neutral()
                    checkpoint = 0
            elif memory.main.diagSkipPossible():
                xbox.tapB()
            elif memory.main.cutsceneSkipPossible():
                memory.main.waitFrames(2)
                xbox.skipScene()
            elif memory.main.menuOpen():
                xbox.tapB()

            # Map changes
            elif checkpoint < 23 and memory.main.getMap() == 123:
                checkpoint = 23
                print("Map change:", checkpoint)
            elif checkpoint < 26 and memory.main.getMap() == 77:
                checkpoint = 26
                print("Map change:", checkpoint)
            elif checkpoint < 31 and memory.main.getMap() == 104:
                checkpoint = 31
                print("Map change:", checkpoint)
    FFXC.set_movement(-1, -1)
    memory.main.waitFrames(30 * 2)
    FFXC.set_neutral()

    logs.writeStats("Blitz Win:")
    logs.writeStats(gameVars.getBlitzWin())
