import xbox
import battle
import menu
import logs
import memory
import targetPathing
import vars
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def arrival():
    if not gameVars.csr():
        xbox.skipStoredScene(2)
    print("Starting Luca section")
    memory.clickToControl()

    earlyHaste = 0
    checkpoint = 0
    while checkpoint < 46:
        if memory.userControl():
            # events
            if checkpoint == 4:  # Seymour intro scene
                print("Event: Seymour intro scene")
                FFXC.set_movement(1, 0)
                memory.awaitEvent()
                FFXC.set_neutral()
                if not gameVars.csr():
                    memory.clickToDiagProgress(18)  # Seymour scene
                    xbox.awaitSave(index=2)

                    memory.clickToDiagProgress(
                        82)  # Let's go over the basics
                    xbox.SkipDialog(1)
                while memory.blitzCursor() != 12:
                    xbox.tapA()
                xbox.menuB()
                if not gameVars.csr():
                    xbox.SkipDialogSpecial(45)  # Skip the Wakka Face scene
                memory.clickToControl()
                checkpoint += 1
            elif checkpoint == 8:  # Upside down T section
                print("Event: Upside down T section")
                memory.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 17:  # Into the bar
                print("Event: Into the bar looking for Auron")
                FFXC.set_movement(0, 1)
                memory.awaitEvent()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 23:  # Back to the front of the Blitz dome
                print("Event: Back to Blitz dome entrance")
                memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 26:  # To the docks
                print("Event: Towards the docks")
                memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 30 or checkpoint == 32:  # First and second battles
                print("Event: First/Second battle")
                FFXC.set_movement(1, 1)
                memory.awaitEvent()
                FFXC.set_neutral()
                battle.LucaWorkers()
                checkpoint += 1
            elif checkpoint == 34:  # Third battle
                print("Tidus XP:", memory.getTidusXP())
                if memory.getTidusXP() >= 312:
                    FFXC.set_neutral()
                    earlyHaste = menu.LucaWorkers()
                    if earlyHaste != 0:
                        earlyHaste = 2
                print("Event: Third battle")
                FFXC.set_movement(1, 0)
                memory.awaitEvent()
                FFXC.set_neutral()
                battle.LucaWorkers2(earlyHaste)
                print("Tidus XP:", memory.getTidusXP())
                memory.clickToControl()
                if earlyHaste == 0 and memory.getTidusXP() >= 312:
                    earlyHaste = menu.LucaWorkers()

                checkpoint += 1
            elif checkpoint == 36 or checkpoint == 45:
                print("Event: Touch Save Sphere")
                memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 38:  # Oblitzerator
                print("Event: Oblitzerator fight")
                FFXC.set_movement(1, 0)
                memory.awaitEvent()
                FFXC.set_neutral()
                battle.Oblitzerator(earlyHaste)
                checkpoint += 1
            elif checkpoint == 40:
                memory.clickToEventTemple(4)

                if earlyHaste == 0:
                    earlyHaste = menu.LucaWorkers() - 1
                checkpoint += 1
            elif checkpoint == 42:
                memory.clickToEventTemple(5)
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.Luca1(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()
            elif memory.cutsceneSkipPossible():
                xbox.skipScene()

            # Map changes
            elif checkpoint < 3 and memory.getMap() == 268:
                checkpoint = 3
                print("Map change:", checkpoint)
            elif checkpoint < 6 and memory.getMap() == 123:  # Front of the Blitz dome
                print("Map change:", checkpoint)
                checkpoint = 6
            elif checkpoint < 11 and memory.getMap() == 104:
                print("Map change:", checkpoint)
                checkpoint = 11

    logs.writeStats("Early Haste:")
    logs.writeStats(earlyHaste)
    gameVars.earlyHasteSet(earlyHaste)

    print("##Checking for thunderstrike weapons for Tidus or Wakka")
    thunderStrike = memory.checkThunderStrike()
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
    while memory.getStoryProgress() < 519:
        if memory.userControl():
            if memory.getMap() == 72 and checkpoint < 3:
                checkpoint = 3
            elif memory.getMap() == 72 and memory.getCoords()[0] < -18 \
                    and checkpoint < 5:
                checkpoint = 5
            elif memory.getMap() == 72 and memory.getCoords()[0] > -15 \
                    and checkpoint >= 5:
                checkpoint = 4
            elif checkpoint == 8:
                targetPathing.setMovement([-111, -4])
                xbox.tapB()
            elif targetPathing.setMovement(targetPathing.LucaPreBlitz(checkpoint)):
                checkpoint += 1
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()


def afterBlitz():
    xbox.clickToBattle()
    encounterID = 0
    checkpoint = 0
    while checkpoint < 36:
        if memory.userControl():
            # Events
            if checkpoint == 8:  # First chest
                if gameVars.earlyHaste() == -1:
                    menu.lateHaste()
                    memory.closeMenu()
                print("First chest")
                while memory.userControl():
                    targetPathing.setMovement([-635, -410])
                    xbox.menuB()
                FFXC.set_neutral()
                memory.clickToControl()
                checkpoint += 1
            elif checkpoint == 10:  # Second chest
                print("Second chest")
                while memory.userControl():
                    targetPathing.setMovement([-620, -424])
                    xbox.menuB()
                FFXC.set_neutral()
                memory.clickToControl()
                checkpoint += 1
            elif checkpoint == 20:  # Target Auron
                if not gameVars.csr():
                    # First Auron affection, always zero
                    while memory.affectionArray()[2] == 0:
                        auronCoords = memory.getActorCoords(3)
                        targetPathing.setMovement(auronCoords)
                        xbox.tapB()
                checkpoint += 1  # After affection changes
            elif checkpoint == 35:  # Bring the party together
                print("Bring the party together")
                memory.clickToEventTemple(1)
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.Luca3(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

        else:
            FFXC.set_neutral()
            if memory.battleActive():
                encounterID += 1
                print("After-Blitz Battle Number:", encounterID)
                if encounterID == 1:
                    battle.afterBlitz1(gameVars.earlyHaste())
                elif encounterID == 2:
                    xbox.clickToBattle()
                    battle.attack('none')  # Hardest boss in the game.
                    print("Well that boss was difficult.")
                    memory.waitFrames(30 * 6)
                elif encounterID == 3:
                    if gameVars.earlyHaste() == -1:
                        battle.afterBlitz3LateHaste(gameVars.earlyHaste())
                    else:
                        battle.afterBlitz3(gameVars.earlyHaste())
                    memory.clickToControl()
                    memory.waitFrames(4)
                    FFXC.set_neutral()
                    checkpoint = 0
            elif memory.diagSkipPossible():
                xbox.tapB()
            elif memory.cutsceneSkipPossible():
                memory.waitFrames(2)
                xbox.skipScene()
            elif memory.menuOpen():
                xbox.tapB()

            # Map changes
            elif checkpoint < 23 and memory.getMap() == 123:
                checkpoint = 23
                print("Map change:", checkpoint)
            elif checkpoint < 26 and memory.getMap() == 77:
                checkpoint = 26
                print("Map change:", checkpoint)
            elif checkpoint < 31 and memory.getMap() == 104:
                checkpoint = 31
                print("Map change:", checkpoint)
    FFXC.set_movement(-1, -1)
    memory.waitFrames(30 * 2)
    FFXC.set_neutral()

    logs.writeStats("Blitz Win:")
    logs.writeStats(gameVars.getBlitzWin())
