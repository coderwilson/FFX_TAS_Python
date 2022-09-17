import time
import xbox
import memory.main
import targetPathing
import vars
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def arrival():
    print("Starting Guadosalam section")
    memory.main.clickToControl()

    FFXC.set_movement(-1, 1)
    memory.main.waitFrames(30 * 0.5)
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 3.5)
    FFXC.set_movement(1, 1)
    memory.main.waitFrames(30 * 0.2)
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 0.6)
    FFXC.set_neutral()

    memory.main.clickToControl3()
    FFXC.set_movement(0, -1)
    memory.main.waitFrames(30 * 1)
    FFXC.set_neutral()

    memory.main.clickToControl3()
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 2)
    FFXC.set_neutral()  # Enter the room where we meet Seymour

    print("TestVar - ", gameVars.csr)
    if not gameVars.csr():
        memory.main.clickToControl3()
        while not targetPathing.setMovement([4, -114]):
            pass
        print("Mark1")
        while memory.main.userControl():  # Talk to Auron (first for affection)
            targetPathing.setMovement([18, -119])
            xbox.tapB()
        FFXC.set_neutral()
        memory.main.clickToControl3()

        while not targetPathing.setMovement([-39, -77]):
            pass
        print("Mark2")
        while memory.main.userControl():  # Start conversation with Wakka
            targetPathing.setMovement([-49, -61])
            xbox.tapB()
        FFXC.set_neutral()
        memory.main.clickToControl3()

        while not targetPathing.setMovement([-13, -67]):
            pass
        print("Mark3")
        while memory.main.userControl():  # Lulu conversation
            targetPathing.setMovement([-11, -55])
            xbox.tapB()
        FFXC.set_neutral()
        memory.main.clickToControl3()

        while not targetPathing.setMovement([15, -52]):
            pass
        while not targetPathing.setMovement([27, -37]):
            pass
        print("Mark4")
        while memory.main.userControl():  # Yunas turn
            targetPathing.setMovement([39, -33])
            xbox.tapB()
        FFXC.set_neutral()
        memory.main.clickToControl3()

        while not targetPathing.setMovement([22, -25]):
            pass
        print("Mark5")
        while memory.main.userControl():  # Start conversation with Rikku
            targetPathing.setMovement([8, -26])
            xbox.tapB()
        FFXC.set_neutral()

        while not memory.main.cutsceneSkipPossible():
            xbox.tapB()
        xbox.skipStoredScene(3)
    print("Ready for next movement.")


def afterSpeech(checkpoint=0):
    memory.main.clickToControl()  # Skips through the long cutscene
    print("Starting movement.")
    print("Starting checkpoint:", checkpoint)

    if checkpoint == 0:
        memory.main.clickToEventTemple(4)

    while checkpoint != 34:
        if memory.main.userControl():
            if checkpoint > 17 and checkpoint < 26 and memory.main.getMap() == 135:
                checkpoint = 26
            elif checkpoint == 1:
                memory.main.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint in [12, 16, 21, 33]:
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 17:
                if not gameVars.csr():
                    memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 14:
                memory.main.clickToEventTemple(5)
                checkpoint += 1
            elif checkpoint == 23:
                memory.main.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 25:
                memory.main.clickToEventTemple(7)
                checkpoint += 1

            elif targetPathing.setMovement(targetPathing.guadoStoryline(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()


def guadoSkip():
    memory.main.clickToControl3()
    FFXC.set_movement(-1, -1)
    pos = memory.main.getCoords()
    while pos[0] > -85:
        pos = memory.main.getCoords()

    if gameVars.csr():
        checkpoint = 2
    else:
        FFXC.set_movement(0, 1)
        xbox.SkipDialog(0.8)  # Talk to the walking guado
        FFXC.set_neutral()
        memory.main.waitFrames(30 * 2.6)
        xbox.menuB()  # Close dialog
        memory.main.waitFrames(30 * 0.2)
        FFXC.set_movement(0, 1)
        print("Past walking guado")
        while pos[1] < 50:
            pos = memory.main.getCoords()
        FFXC.set_movement(1, 0)
        print("Angle right")
        while pos[0] < -44:
            pos = memory.main.getCoords()
        FFXC.set_movement(1, -1)
        print("Towards position")
        while pos[0] < 9:
            pos = memory.main.getCoords()
        FFXC.set_movement(0, -1)
        print("Adjustment 1")
        while pos[1] > -7.5:
            pos = memory.main.getCoords()
        FFXC.set_neutral()
        memory.main.waitFrames(5)

        pos = memory.main.getCoords()
        recovery = False
        print("Adjustment 2")
        while pos[0] > 8 and not recovery:
            tidusPos = memory.main.getCoords()
            guadoPos = memory.main.getActorCoords(17)
            if abs(tidusPos[0] - guadoPos[0]) + abs(tidusPos[1] - guadoPos[1]) < 30:
                while memory.main.userControl():
                    targetPathing.setMovement(guadoPos[0], guadoPos[1])
                    xbox.tapB()
                recovery = True
            else:
                FFXC.set_value('Dpad', 4)
                memory.main.waitFrames(3)
                FFXC.set_value('Dpad', 0)
                memory.main.waitFrames(5)
                pos = memory.main.getCoords()
        print("Adjustment 3")
        while pos[1] < -8.5 and not recovery:
            tidusPos = memory.main.getCoords()
            guadoPos = memory.main.getActorCoords(17)
            if abs(tidusPos[0] - guadoPos[0]) + abs(tidusPos[1] - guadoPos[1]) < 30:
                while memory.main.userControl():
                    targetPathing.setMovement([guadoPos[0], guadoPos[1]])
                    xbox.tapB()
                recovery = True
            else:
                FFXC.set_value('Dpad', 1)
                memory.main.waitFrames(3)
                FFXC.set_value('Dpad', 0)
                memory.main.waitFrames(5)
                pos = memory.main.getCoords()

        memory.main.waitFrames(30 * 0.15)
        FFXC.set_movement(0, -1)
        memory.main.waitFrames(30 * 0.04)
        FFXC.set_neutral()  # Face downward
        memory.main.waitFrames(4)
        skipActivate = False
        while not skipActivate and not recovery:
            tidusPos = memory.main.getCoords()
            guadoPos = memory.main.getActorCoords(17)
            if abs(tidusPos[0] - guadoPos[0]) + abs(tidusPos[1] - guadoPos[1]) < 30:
                if guadoPos[0] < 10:
                    skipActivate = True
                    print("MARK")
                    xbox.SkipDialog(0.5)
            elif pos[1] > -9:
                FFXC.set_value('Dpad', 2)
                memory.main.waitFrames(2)
                FFXC.set_value('Dpad', 0)
                memory.main.waitFrames(5)
                pos = memory.main.getCoords()

        if not recovery:
            # Time limit for safety
            startTime = time.time()
            # Max number of seconds that we will wait for the skip to occur.
            timeLimit = 8
            maxTime = startTime + timeLimit

            # Waiting for walking guado to push us into the door
            while memory.main.getCamera()[0] < 0.6:
                currentTime = time.time()
                if currentTime > maxTime:
                    print("Skip failed for some reason. Moving on without skip.")
                    break
            memory.main.waitFrames(30 * 0.035)  # Guado potions good!
            xbox.tapB()
        checkpoint = 0

    guadoSkipStatus = False
    while memory.main.getMap() != 140:
        if memory.main.userControl():
            if checkpoint == 5:
                print(memory.main.getCamera())
                if memory.main.getCamera()[1] < -9:
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
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 24:  # Back to party
                print("Back to party")
                memory.main.clickToEventTemple(7)
                checkpoint += 1

            # General pathing
            elif memory.main.userControl():
                if targetPathing.setMovement(targetPathing.guadoSkip(checkpoint)):
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()
    FFXC.set_neutral()
    return guadoSkipStatus
