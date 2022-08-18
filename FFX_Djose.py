import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory
import FFX_targetPathing
import FFX_vars
gameVars = FFX_vars.varsHandle()
#import FFX_Djose_Skip_Path

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC


def path():
    FFX_memory.clickToControl()
    FFX_memory.closeMenu()
    #FFX_memory.waitFrames(30 * 1)
    FFX_memory.fullPartyFormat('djose')
    FFX_memory.closeMenu()

    countBattles = 0
    checkpoint = 0
    lastCP = 0
    stoneBreath = 0
    print("Starting Djose pathing section")
    # FFX_memory.setEncounterRate(0) #TESTING ONLY!!! MAKE SURE TO COMMENT OUT THIS COMMAND!!!

    while FFX_memory.getMap() != 81:  # All the way into the temple
        if lastCP != checkpoint:
            print("Checkpoint reached:", checkpoint)
            lastCP = checkpoint

        if FFX_memory.userControl():
            if checkpoint in [45, 46] and stoneBreath == 1:
                checkpoint = 47
            elif checkpoint == 47 and stoneBreath == 0:
                checkpoint = 45

            # This is for the attempted Djose skip. It is not viable. Feel free to re-try this.
            # elif checkpoint == 33:# and stoneBreath == 0: #Turn/talk
            #    FFXC.set_movement(-1, 1)
            #    FFX_memory.waitFrames(4)
            #    while FFX_memory.userControl() and FFX_memory.getActorCoords(11)[1] < 790:
            #        FFX_Xbox.tapB()
            #    FFXC.set_neutral()
            #    checkpoint += 1
            # elif checkpoint == 34:# and stoneBreath == 0:
            #    while FFX_memory.getActorCoords(0)[1] < 790 and \
            #        FFX_memory.getActorCoords(11)[1] < 790:
            #
            #        FFX_memory.waitFrames(1)
            #    FFX_memory.clickToControl3()
            #    checkpoint += 1

            else:
                # Map changes
                if FFX_memory.getMap() == 76 and checkpoint < 49:
                    checkpoint = 50
                if checkpoint in [49, 54, 56]:
                    FFX_memory.clickToEventTemple(0)
                    checkpoint += 1
                elif FFX_targetPathing.djosePath(checkpoint)[0] < FFX_memory.getActorCoords(0)[0] \
                        and checkpoint < 46 and checkpoint > 18:
                    checkpoint += 1
                elif FFX_targetPathing.djosePath(checkpoint)[1] < FFX_memory.getActorCoords(0)[1] \
                        and checkpoint < 46 and checkpoint > 18:
                    checkpoint += 1
                # General pathing
                elif FFX_targetPathing.setMovement(FFX_targetPathing.djosePath(checkpoint)) == True:
                    checkpoint += 1
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                print("Starting battle")
                if stoneBreath == 0:
                    print("Still looking for Stone Breath.")
                stoneBreath = FFX_Battle.djose(stoneBreath)
                print("Battles complete.")
                countBattles += 1
            elif FFX_memory.menuOpen():
                FFX_Xbox.menuB()
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.menuB()

    FFX_Logs.writeStats("Djose battles:")
    FFX_Logs.writeStats(countBattles)


def temple():
    FFX_memory.clickToControl()
    FFX_menu.djoseTemple()
    if not gameVars.csr():
        FFXC.set_movement(0, -1)
        FFX_memory.waitFrames(30 * 0.3)
        FFXC.set_movement(-1, -1)
        FFX_memory.clickToEvent()  # Talk to Auron
        FFX_memory.waitFrames(30 * 0.2)
        FFX_memory.clickToControl3()  # Done talking

    checkpoint = 0
    while not FFX_memory.getMap() == 214:
        target = [[-1, 32], [-1, 111], [-1, 111], [-1, 200]]
        if checkpoint == 2:
            FFX_memory.clickToEventTemple(0)
            checkpoint += 1
        elif FFX_memory.userControl():
            if FFX_targetPathing.setMovement(target[checkpoint]) == True:
                checkpoint += 1
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()


def trials():
    print("Starting Trials section.")
    FFX_memory.clickToControl()

    checkpoint = 0
    while FFX_memory.getMap() != 90:
        if FFX_memory.userControl():
            if checkpoint == 1:  # First sphere
                print("First sphere")
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 3:  # Sphere door
                print("Sphere door")
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 5:  # Second sphere
                print("Second sphere")
                FFX_memory.clickToEventTemple(3)
                checkpoint += 1
            elif checkpoint == 7:  # Sphere door opens
                print("Sphere door opens")
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 13:  # Left Sphere
                print("Left sphere")
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 16:  # Insert Left Sphere
                print("Insert left sphere")
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 19:  # Right Sphere
                print("Right sphere")
                FFX_memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 22:
                print("Pushing pedestal")
                FFXC.set_movement(1, 0)
                FFX_memory.awaitEvent()
                while FFX_memory.getActorCoords(0)[0] < 62:
                    FFXC.set_movement(1, 0)
                FFXC.set_neutral()
                FFX_memory.waitFrames(15)
                print("Push complete.")
                checkpoint += 1
                print("Insert right sphere")
                FFX_memory.clickToEventTemple(0)
                FFXC.set_movement(-1, 1)
                FFX_memory.waitFrames(30 * 0.2)
                checkpoint += 1
            elif checkpoint == 24:  # Insert Right Sphere
                print("Insert right sphere")
                FFX_memory.clickToEventTemple(1)
                checkpoint = 27
            elif checkpoint == 28:
                print("Left sphere")
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 31 or checkpoint == 56:  # Reset switch event
                print("Reset switch")
                FFX_memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 34:
                print("Insert left sphere")
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 38:
                print("Powered sphere")
                FFX_memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 40:
                print("Insert powered sphere")
                FFX_memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 43:
                print("Right sphere")
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 45:
                print("Insert right sphere")
                FFX_memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 48:  # All of the hidden room stuff at once
                print("Pushing pedestal")
                FFXC.set_movement(0, 1)
                FFX_memory.awaitEvent()
                FFX_memory.waitFrames(30 * 9)
                print("Push complete.")
                FFX_memory.awaitControl()
                FFXC.set_movement(0, 1)
                FFX_memory.waitFrames(30 * 0.4)
                FFXC.set_neutral()
                FFX_memory.waitFrames(30 * 0.5)
                FFX_memory.awaitControl()
                print("Extra pedestal")
                FFXC.set_movement(0, 1)
                FFX_Xbox.SkipDialog(2)
                FFXC.set_neutral()
                FFX_memory.awaitControl()
                FFXC.set_movement(0, -1)
                FFX_memory.waitFrames(30 * 0.8)
                FFXC.set_neutral()
                FFX_memory.waitFrames(30 * 0.5)
                checkpoint += 1
            elif checkpoint == 51:
                print("Powered sphere")
                FFX_memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 53:
                print("Insert powered sphere")
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 58:
                print("Left sphere")
                while FFX_memory.userControl():
                    FFX_targetPathing.setMovement([-5, 24])
                    FFX_memory.waitFrames(3)
                    FFXC.set_neutral()
                    FFX_memory.waitFrames(3)
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                FFX_memory.clickToControl3()
                # FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 63:
                print("Final insert Left sphere")
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 68:
                print("Right sphere")
                while FFX_memory.userControl():
                    FFX_targetPathing.setMovement([5, 24])
                    FFX_memory.waitFrames(3)
                    FFXC.set_neutral()
                    FFX_memory.waitFrames(3)
                    FFX_Xbox.tapB()
                    FFX_memory.waitFrames(3)
                FFXC.set_neutral()
                FFX_memory.clickToControl3()
                # FFX_memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 73:
                print("Final insert Right sphere")
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 76:  # No longer doing Destruction Sphere stuff.
                checkpoint = 85
            elif checkpoint == 80:
                print("Destruction Glyph")
                while FFX_memory.userControl():
                    FFX_targetPathing.setMovement([-58, 38])
                    FFX_memory.waitFrames(3)
                    FFXC.set_neutral()
                    FFX_memory.waitFrames(4)
                    FFX_Xbox.tapB()
                    FFX_memory.waitFrames(3)
                FFXC.set_neutral()
                print("Glyph touched.")
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 82:
                print("Destruction sphere")
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 85:  # Lift
                if FFX_targetPathing.setMovement([0, 30]) == True:
                    FFXC.set_neutral()
                    FFX_memory.waitFrames(30 * 0.2)
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
            elif checkpoint == 88:
                print("Pedestal 1")
                FFX_memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 90:
                print("Pedestal 2")
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 92:
                print("Pedestal 3")
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 94:
                print("Pedestal 4")
                FFX_memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 96:
                print("Pedestal 5")
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 100:
                checkpoint += 2
            elif checkpoint == 102:
                checkpoint += 1
            elif checkpoint == 104:
                print("End of Trials")
                if gameVars.csr():
                    FFXC.set_movement(-1, 1)
                    FFX_memory.awaitEvent()
                    FFXC.set_neutral()
                    break
                else:
                    FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif FFX_targetPathing.setMovement(FFX_targetPathing.djoseTrials(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        elif FFX_memory.nameAeonReady():
            FFX_memory.clearNameAeonReady()

    FFXC.set_neutral()
    if not gameVars.csr():
        FFX_memory.awaitControl()
        FFX_memory.waitFrames(30 * 0.3)
        print("Talk to Auron while we wait.")
        FFXC.set_movement(1, -1)
        FFX_memory.clickToEvent()
        FFXC.set_movement(-1, -1)
        FFX_memory.clickToControl3()
        FFX_memory.waitFrames(30 * 0.07)

        # Dance
        checkpoint = 0
        while FFX_memory.userControl():
            if FFX_targetPathing.setMovement(FFX_targetPathing.djoseDance(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

            if checkpoint == 8:
                checkpoint = 0

        FFX_memory.clickToControl()
        print("Leaving the fayth room")

        while FFX_targetPathing.setMovement([-1, -60]) == False:
            movingToExit = True
        FFXC.set_movement(1, 1)
        FFX_memory.awaitEvent()
        FFXC.set_neutral()

    FFX_Xbox.nameAeon("Ixion")


def leavingDjose():
    FFX_memory.awaitControl()

    checkpoint = 0
    while FFX_memory.getMap() != 75:
        if FFX_memory.userControl():
            if checkpoint == 1:
                if not gameVars.csr():
                    FFXC.set_movement(1, 0)
                    FFX_memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 11:  # No longer do we pick up the Remedy
                checkpoint = 13
            elif checkpoint in [3, 9, 12]:
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 14:
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 18:
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint in [22, 29]:
                FFX_memory.clickToEventTemple(4)
                checkpoint += 1
            elif FFX_targetPathing.setMovement(FFX_targetPathing.djoseExit(checkpoint)) == True:
                checkpoint += 1
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                FFX_Battle.fleeAll()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

    FFXC.set_neutral()
