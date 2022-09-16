import time
import xbox
import memory
import targetPathing
import vars
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def arrival():
    print("Starting Guadosalam section")
    memory.clickToControl()

    FFXC.set_movement(-1, 1)
    memory.waitFrames(30 * 0.5)
    FFXC.set_movement(0, 1)
    memory.waitFrames(30 * 3.5)
    FFXC.set_movement(1, 1)
    memory.waitFrames(30 * 0.2)
    FFXC.set_movement(0, 1)
    memory.waitFrames(30 * 0.6)
    FFXC.set_neutral()

    memory.clickToControl3()
    FFXC.set_movement(0, -1)
    memory.waitFrames(30 * 1)
    FFXC.set_neutral()

    memory.clickToControl3()
    FFXC.set_movement(0, 1)
    memory.waitFrames(30 * 2)
    FFXC.set_neutral()  # Enter the room where we meet Seymour

    print("TestVar - ", gameVars.csr)
    if not gameVars.csr():
        memory.clickToControl3()
        while not targetPathing.setMovement([4, -114]):
            pass
        print("Mark1")
        while memory.userControl():  # Talk to Auron (first for affection)
            targetPathing.setMovement([18, -119])
            xbox.tapB()
        FFXC.set_neutral()
        memory.clickToControl3()

        while not targetPathing.setMovement([-39, -77]):
            pass
        print("Mark2")
        while memory.userControl():  # Start conversation with Wakka
            targetPathing.setMovement([-49, -61])
            xbox.tapB()
        FFXC.set_neutral()
        memory.clickToControl3()

        while not targetPathing.setMovement([-13, -67]):
            pass
        print("Mark3")
        while memory.userControl():  # Lulu conversation
            targetPathing.setMovement([-11, -55])
            xbox.tapB()
        FFXC.set_neutral()
        memory.clickToControl3()

        while not targetPathing.setMovement([15, -52]):
            pass
        while not targetPathing.setMovement([27, -37]):
            pass
        print("Mark4")
        while memory.userControl():  # Yunas turn
            targetPathing.setMovement([39, -33])
            xbox.tapB()
        FFXC.set_neutral()
        memory.clickToControl3()

        while not targetPathing.setMovement([22, -25]):
            pass
        print("Mark5")
        while memory.userControl():  # Start conversation with Rikku
            targetPathing.setMovement([8, -26])
            xbox.tapB()
        FFXC.set_neutral()

        while not memory.cutsceneSkipPossible():
            xbox.tapB()
        xbox.skipStoredScene(3)
    print("Ready for next movement.")


def afterSpeech(checkpoint=0):
    memory.clickToControl()  # Skips through the long cutscene
    print("Starting movement.")
    print("Starting checkpoint:", checkpoint)

    if checkpoint == 0:
        memory.clickToEventTemple(4)

    while checkpoint != 34:
        if memory.userControl():
            if checkpoint > 17 and checkpoint < 26 and memory.getMap() == 135:
                checkpoint = 26
            elif checkpoint == 1:
                memory.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint in [12, 16, 21, 33]:
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 17:
                if not gameVars.csr():
                    memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 14:
                memory.clickToEventTemple(5)
                checkpoint += 1
            elif checkpoint == 23:
                memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 25:
                memory.clickToEventTemple(7)
                checkpoint += 1

            elif targetPathing.setMovement(targetPathing.guadoStoryline(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()


def guadoSkip():
    memory.clickToControl3()
    FFXC.set_movement(-1, -1)
    pos = memory.getCoords()
    while pos[0] > -85:
        pos = memory.getCoords()

    if gameVars.csr():
        checkpoint = 2
    else:
        FFXC.set_movement(0, 1)
        xbox.SkipDialog(0.8)  # Talk to the walking guado
        FFXC.set_neutral()
        memory.waitFrames(30 * 2.6)
        xbox.menuB()  # Close dialog
        memory.waitFrames(30 * 0.2)
        FFXC.set_movement(0, 1)
        print("Past walking guado")
        while pos[1] < 50:
            pos = memory.getCoords()
        FFXC.set_movement(1, 0)
        print("Angle right")
        while pos[0] < -44:
            pos = memory.getCoords()
        FFXC.set_movement(1, -1)
        print("Towards position")
        while pos[0] < 9:
            pos = memory.getCoords()
        FFXC.set_movement(0, -1)
        print("Adjustment 1")
        while pos[1] > -7.5:
            pos = memory.getCoords()
        FFXC.set_neutral()
        memory.waitFrames(5)

        pos = memory.getCoords()
        recovery = False
        print("Adjustment 2")
        while pos[0] > 8 and not recovery:
            tidusPos = memory.getCoords()
            guadoPos = memory.getActorCoords(17)
            if abs(tidusPos[0] - guadoPos[0]) + abs(tidusPos[1] - guadoPos[1]) < 30:
                while memory.userControl():
                    targetPathing.setMovement(guadoPos[0], guadoPos[1])
                    xbox.tapB()
                recovery = True
            else:
                FFXC.set_value('Dpad', 4)
                memory.waitFrames(3)
                FFXC.set_value('Dpad', 0)
                memory.waitFrames(5)
                pos = memory.getCoords()
        print("Adjustment 3")
        while pos[1] < -8.5 and not recovery:
            tidusPos = memory.getCoords()
            guadoPos = memory.getActorCoords(17)
            if abs(tidusPos[0] - guadoPos[0]) + abs(tidusPos[1] - guadoPos[1]) < 30:
                while memory.userControl():
                    targetPathing.setMovement([guadoPos[0], guadoPos[1]])
                    xbox.tapB()
                recovery = True
            else:
                FFXC.set_value('Dpad', 1)
                memory.waitFrames(3)
                FFXC.set_value('Dpad', 0)
                memory.waitFrames(5)
                pos = memory.getCoords()

        memory.waitFrames(30 * 0.15)
        FFXC.set_movement(0, -1)
        memory.waitFrames(30 * 0.04)
        FFXC.set_neutral()  # Face downward
        memory.waitFrames(4)
        skipActivate = False
        while not skipActivate and not recovery:
            tidusPos = memory.getCoords()
            guadoPos = memory.getActorCoords(17)
            if abs(tidusPos[0] - guadoPos[0]) + abs(tidusPos[1] - guadoPos[1]) < 30:
                if guadoPos[0] < 10:
                    skipActivate = True
                    print("MARK")
                    xbox.SkipDialog(0.5)
            elif pos[1] > -9:
                FFXC.set_value('Dpad', 2)
                memory.waitFrames(2)
                FFXC.set_value('Dpad', 0)
                memory.waitFrames(5)
                pos = memory.getCoords()

        if not recovery:
            # Time limit for safety
            startTime = time.time()
            # Max number of seconds that we will wait for the skip to occur.
            timeLimit = 8
            maxTime = startTime + timeLimit

            # Waiting for walking guado to push us into the door
            while memory.getCamera()[0] < 0.6:
                currentTime = time.time()
                if currentTime > maxTime:
                    print("Skip failed for some reason. Moving on without skip.")
                    break
            memory.waitFrames(30 * 0.035)  # Guado potions good!
            xbox.tapB()
        checkpoint = 0

    guadoSkipStatus = False
    while memory.getMap() != 140:
        if memory.userControl():
            if checkpoint == 5:
                print(memory.getCamera())
                if memory.getCamera()[1] < -9:
                    print("Guado skip success.")
                    if gameVars.csr():
                        guadoSkipStatus = False
                        checkpoint = 18
                    else:
                        guadoSkipStatus = True
                        checkpoint += 1
                else:
                    print("Guado skip fail. Back-up strats.")
                    guadoSkipStatus = False
                    checkpoint = 18
            elif checkpoint == 21:  # Shelinda conversation
                print("Shelinda")
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 24:  # Back to party
                print("Back to party")
                memory.clickToEventTemple(7)
                checkpoint += 1

            # General pathing
            elif memory.userControl():
                if targetPathing.setMovement(targetPathing.guadoSkip(checkpoint)):
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()
    FFXC.set_neutral()
    return guadoSkipStatus
