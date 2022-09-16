import xbox
import battle
import menu
import logs
import memory
import targetPathing
import vars
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def path():
    memory.clickToControl()
    memory.closeMenu()
    memory.fullPartyFormat('djose')
    memory.closeMenu()

    countBattles = 0
    checkpoint = 0
    lastCP = 0
    stoneBreath = 0
    print("Starting Djose pathing section")

    while memory.getMap() != 81:  # All the way into the temple
        if lastCP != checkpoint:
            print("Checkpoint reached:", checkpoint)
            lastCP = checkpoint

        if memory.userControl():
            if checkpoint in [45, 46] and stoneBreath == 1:
                checkpoint = 47
            elif checkpoint == 47 and stoneBreath == 0:
                checkpoint = 45

            else:
                # Map changes
                if memory.getMap() == 76 and checkpoint < 49:
                    checkpoint = 50
                if checkpoint in [49, 54, 56]:
                    memory.clickToEventTemple(0)
                    checkpoint += 1
                elif targetPathing.djosePath(checkpoint)[0] < memory.getActorCoords(0)[0] \
                        and checkpoint < 46 and checkpoint > 18:
                    checkpoint += 1
                elif targetPathing.djosePath(checkpoint)[1] < memory.getActorCoords(0)[1] \
                        and checkpoint < 46 and checkpoint > 18:
                    checkpoint += 1
                # General pathing
                elif targetPathing.setMovement(targetPathing.djosePath(checkpoint)):
                    checkpoint += 1
        else:
            FFXC.set_neutral()
            if memory.battleActive():
                print("Starting battle")
                if stoneBreath == 0:
                    print("Still looking for Stone Breath.")
                stoneBreath = battle.djose(stoneBreath)
                print("Battles complete.")
                countBattles += 1
            elif memory.menuOpen():
                xbox.menuB()
            elif memory.diagSkipPossible():
                xbox.menuB()

    # logs.writeStats("Djose battles:")
    # logs.writeStats(countBattles)


def temple():
    memory.clickToControl()
    menu.djoseTemple()
    if not gameVars.csr():
        FFXC.set_movement(0, -1)
        memory.waitFrames(30 * 0.3)
        FFXC.set_movement(-1, -1)
        memory.clickToEvent()  # Talk to Auron
        memory.waitFrames(30 * 0.2)
        memory.clickToControl3()  # Done talking

    checkpoint = 0
    while not memory.getMap() == 214:
        target = [[-1, 32], [-1, 111], [-1, 111], [-1, 200]]
        if checkpoint == 2:
            memory.clickToEventTemple(0)
            checkpoint += 1
        elif memory.userControl():
            if targetPathing.setMovement(target[checkpoint]):
                checkpoint += 1
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()


def trials():
    print("Starting Trials section.")
    memory.clickToControl()

    checkpoint = 0
    while memory.getMap() != 90:
        if memory.userControl():
            if checkpoint == 1:  # First sphere
                print("First sphere")
                memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 3:  # Sphere door
                print("Sphere door")
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 5:  # Second sphere
                print("Second sphere")
                memory.clickToEventTemple(3)
                checkpoint += 1
            elif checkpoint == 7:  # Sphere door opens
                print("Sphere door opens")
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 13:  # Left Sphere
                print("Left sphere")
                memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 16:  # Insert Left Sphere
                print("Insert left sphere")
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 19:  # Right Sphere
                print("Right sphere")
                memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 22:
                print("Pushing pedestal")
                FFXC.set_movement(1, 0)
                memory.awaitEvent()
                while memory.getActorCoords(0)[0] < 62:
                    FFXC.set_movement(1, 0)
                FFXC.set_neutral()
                memory.waitFrames(15)
                print("Push complete.")
                checkpoint += 1
                print("Insert right sphere")
                memory.clickToEventTemple(0)
                FFXC.set_movement(-1, 1)
                memory.waitFrames(30 * 0.2)
                checkpoint += 1
            elif checkpoint == 24:  # Insert Right Sphere
                print("Insert right sphere")
                memory.clickToEventTemple(1)
                checkpoint = 27
            elif checkpoint == 28:
                print("Left sphere")
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 31 or checkpoint == 56:  # Reset switch event
                print("Reset switch")
                memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 34:
                print("Insert left sphere")
                memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 38:
                print("Powered sphere")
                memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 40:
                print("Insert powered sphere")
                memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 43:
                print("Right sphere")
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 45:
                print("Insert right sphere")
                memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 48:  # All of the hidden room stuff at once
                print("Pushing pedestal")
                FFXC.set_movement(0, 1)
                memory.awaitEvent()
                memory.waitFrames(30 * 9)
                print("Push complete.")
                memory.awaitControl()
                FFXC.set_movement(0, 1)
                memory.waitFrames(30 * 0.4)
                FFXC.set_neutral()
                memory.waitFrames(30 * 0.5)
                memory.awaitControl()
                print("Extra pedestal")
                FFXC.set_movement(0, 1)
                xbox.SkipDialog(2)
                FFXC.set_neutral()
                memory.awaitControl()
                FFXC.set_movement(0, -1)
                memory.waitFrames(30 * 0.8)
                FFXC.set_neutral()
                memory.waitFrames(30 * 0.5)
                checkpoint += 1
            elif checkpoint == 51:
                print("Powered sphere")
                memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 53:
                print("Insert powered sphere")
                memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 58:
                print("Left sphere")
                while memory.userControl():
                    targetPathing.setMovement([-5, 24])
                    memory.waitFrames(3)
                    FFXC.set_neutral()
                    memory.waitFrames(3)
                    xbox.tapB()
                FFXC.set_neutral()
                memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 63:
                print("Final insert Left sphere")
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 68:
                print("Right sphere")
                while memory.userControl():
                    targetPathing.setMovement([5, 24])
                    memory.waitFrames(3)
                    FFXC.set_neutral()
                    memory.waitFrames(3)
                    xbox.tapB()
                    memory.waitFrames(3)
                FFXC.set_neutral()
                memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 73:
                print("Final insert Right sphere")
                memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 76:  # No longer doing Destruction Sphere stuff.
                checkpoint = 85
            elif checkpoint == 80:
                print("Destruction Glyph")
                while memory.userControl():
                    targetPathing.setMovement([-58, 38])
                    memory.waitFrames(3)
                    FFXC.set_neutral()
                    memory.waitFrames(4)
                    xbox.tapB()
                    memory.waitFrames(3)
                FFXC.set_neutral()
                print("Glyph touched.")
                memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 82:
                print("Destruction sphere")
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 85:  # Lift
                if targetPathing.setMovement([0, 30]):
                    FFXC.set_neutral()
                    memory.waitFrames(30 * 0.2)
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
            elif checkpoint == 88:
                print("Pedestal 1")
                memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 90:
                print("Pedestal 2")
                memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 92:
                print("Pedestal 3")
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 94:
                print("Pedestal 4")
                memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 96:
                print("Pedestal 5")
                memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 100:
                checkpoint += 2
            elif checkpoint == 102:
                checkpoint += 1
            elif checkpoint == 104:
                print("End of Trials")
                if gameVars.csr():
                    FFXC.set_movement(-1, 1)
                    memory.awaitEvent()
                    FFXC.set_neutral()
                    break
                else:
                    memory.clickToEventTemple(7)
                checkpoint += 1
            elif targetPathing.setMovement(targetPathing.djoseTrials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

    FFXC.set_neutral()
    if not gameVars.csr():
        memory.awaitControl()
        memory.waitFrames(30 * 0.3)
        print("Talk to Auron while we wait.")
        FFXC.set_movement(1, -1)
        memory.clickToEvent()
        FFXC.set_movement(-1, -1)
        memory.clickToControl3()
        memory.waitFrames(30 * 0.07)

        # Dance
        checkpoint = 0
        while memory.userControl():
            if targetPathing.setMovement(targetPathing.djoseDance(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

            if checkpoint == 8:
                checkpoint = 0

        memory.clickToControl()
        print("Leaving the fayth room")

        FFXC.set_movement(1, 1)
        memory.awaitEvent()
        FFXC.set_neutral()

    xbox.nameAeon("Ixion")


def leavingDjose():
    memory.awaitControl()

    checkpoint = 0
    lastCP = 0
    while memory.getMap() != 75:
        if lastCP != checkpoint:
            print("Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        if memory.userControl():
            if checkpoint == 1:
                if not gameVars.csr():
                    FFXC.set_movement(1, 0)
                    memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 11:  # and not gameVars.skipKilikaLuck(): #Do we need this chest for kilika luck skip? I think not.
                checkpoint = 13
            elif checkpoint in [3, 9, 12]:
                memory.clickToEventTemple(0)
                if checkpoint == 9:
                    checkpoint = 35
                else:
                    checkpoint += 1
            elif checkpoint == 14:
                memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 18:
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint in [22, 29]:
                memory.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 36:
                while memory.userControl():
                    targetPathing.setMovement([-18, 35])
                    xbox.tapB()
                FFXC.set_neutral()
                memory.clickToControl()
                checkpoint = 13
            elif targetPathing.setMovement(targetPathing.djoseExit(checkpoint)):
                checkpoint += 1
        else:
            FFXC.set_neutral()
            if memory.battleActive():
                battle.fleeAll()
            elif memory.menuOpen():
                xbox.tapB()
            elif memory.diagSkipPossible():
                xbox.tapB()

    FFXC.set_neutral()
