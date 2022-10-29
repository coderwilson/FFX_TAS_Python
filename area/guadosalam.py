import time

import memory.main
import targetPathing
import vars
import xbox

game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def arrival():
    print("Starting Guadosalam section")
    memory.main.click_to_control()

    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(30 * 0.5)
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 3.5)
    FFXC.set_movement(1, 1)
    memory.main.wait_frames(30 * 0.2)
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 0.6)
    FFXC.set_neutral()

    memory.main.click_to_control_3()
    FFXC.set_movement(0, -1)
    memory.main.wait_frames(30 * 1)
    FFXC.set_neutral()

    memory.main.click_to_control_3()
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 2)
    FFXC.set_neutral()  # Enter the room where we meet Seymour

    print("TestVar -", game_vars.csr)
    # Adjusted branch CSR logic, start
    memory.main.click_to_control_3()
    if game_vars.csr():
        while not targetPathing.set_movement([-13, -67]):
            pass
        print("Mark3")
        while memory.main.user_control():  # Lulu conversation
            targetPathing.set_movement([-11, -55])
            xbox.tap_b()
        FFXC.set_neutral()
        memory.main.click_to_control_3()

        while not targetPathing.set_movement([-39, -77]):
            pass
        print("Mark2")
        while memory.main.user_control():  # Start conversation with Wakka
            targetPathing.set_movement([-49, -61])
            xbox.tap_b()
        FFXC.set_neutral()
        memory.main.click_to_control_3()

        while not targetPathing.set_movement([4, -114]):
            pass
        print("Mark1")
        while memory.main.user_control():  # Talk to Auron
            targetPathing.set_movement([18, -119])
            xbox.tap_b()
        FFXC.set_neutral()
        memory.main.click_to_control_3()

    else:
        while not targetPathing.set_movement([4, -114]):
            pass
        print("Mark1")
        while memory.main.user_control():  # Talk to Auron (first for affection)
            targetPathing.set_movement([18, -119])
            xbox.tap_b()
        FFXC.set_neutral()
        memory.main.click_to_control_3()

        while not targetPathing.set_movement([-39, -77]):
            pass
        print("Mark2")
        while memory.main.user_control():  # Start conversation with Wakka
            targetPathing.set_movement([-49, -61])
            xbox.tap_b()
        FFXC.set_neutral()
        memory.main.click_to_control_3()

        while not targetPathing.set_movement([-13, -67]):
            pass
        print("Mark3")
        while memory.main.user_control():  # Lulu conversation
            targetPathing.set_movement([-11, -55])
            xbox.tap_b()
        FFXC.set_neutral()
        memory.main.click_to_control_3()

    # Line up for Rikku/Yuna
    while not targetPathing.set_movement([15, -52]):
        pass

    while not targetPathing.set_movement([22, -25]):
        pass
    print("Mark5")
    while memory.main.user_control():  # Start conversation with Rikku
        targetPathing.set_movement([8, -26])
        xbox.tap_b()
    FFXC.set_neutral()
    memory.main.click_to_control_3()

    while not targetPathing.set_movement([27, -37]):
        pass
    print("Mark4")
    while memory.main.user_control():  # Yunas turn
        targetPathing.set_movement([39, -33])
        xbox.tap_b()
    FFXC.set_neutral()
    memory.main.click_to_control_3()

    if not game_vars.csr():
        while not memory.main.cutscene_skip_possible():
            xbox.tap_b()
        xbox.skip_stored_scene(3)
    # Adjusted CSR branch logic, end
    print("Ready for next movement.")


def after_speech(checkpoint=0):
    memory.main.click_to_control()  # Skips through the long cutscene
    print("Starting movement.")
    print("Starting checkpoint:", checkpoint)

    if checkpoint == 0:
        memory.main.click_to_event_temple(4)

    while checkpoint != 34:
        if memory.main.user_control():
            if checkpoint > 17 and checkpoint < 26 and memory.main.get_map() == 135:
                checkpoint = 26
            elif checkpoint == 1:
                memory.main.click_to_event_temple(4)
                checkpoint += 1
            elif checkpoint in [12, 16, 21, 33]:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 17:
                if not game_vars.csr():
                    memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 14:
                memory.main.click_to_event_temple(5)
                checkpoint += 1
            elif checkpoint == 23:
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 25:
                memory.main.click_to_event_temple(7)
                checkpoint += 1

            elif targetPathing.set_movement(targetPathing.guado_storyline(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()


def guado_skip():
    memory.main.click_to_control_3()
    FFXC.set_movement(-1, -1)
    pos = memory.main.get_coords()
    while pos[0] > -85:
        pos = memory.main.get_coords()

    if game_vars.csr():
        checkpoint = 2
    else:
        FFXC.set_movement(0, 1)
        xbox.skip_dialog(0.8)  # Talk to the walking guado
        FFXC.set_neutral()
        memory.main.wait_frames(30 * 2.6)
        xbox.menu_b()  # Close dialog
        memory.main.wait_frames(30 * 0.2)
        FFXC.set_movement(0, 1)
        print("Past walking guado")
        while pos[1] < 50:
            pos = memory.main.get_coords()
        FFXC.set_movement(1, 0)
        print("Angle right")
        while pos[0] < -44:
            pos = memory.main.get_coords()
        FFXC.set_movement(1, -1)
        print("Towards position")
        while pos[0] < 9:
            pos = memory.main.get_coords()
        FFXC.set_movement(0, -1)
        print("Adjustment 1")
        while pos[1] > -7.5:
            pos = memory.main.get_coords()
        FFXC.set_neutral()
        memory.main.wait_frames(5)

        pos = memory.main.get_coords()
        recovery = False
        print("Adjustment 2")
        while pos[0] > 8 and not recovery:
            tidusPos = memory.main.get_coords()
            guadoPos = memory.main.get_actor_coords(17)
            if abs(tidusPos[0] - guadoPos[0]) + abs(tidusPos[1] - guadoPos[1]) < 30:
                while memory.main.user_control():
                    targetPathing.set_movement(guadoPos[0], guadoPos[1])
                    xbox.tap_b()
                recovery = True
            else:
                FFXC.set_value("Dpad", 4)
                memory.main.wait_frames(3)
                FFXC.set_value("Dpad", 0)
                memory.main.wait_frames(5)
                pos = memory.main.get_coords()
        print("Adjustment 3")
        while pos[1] < -8.5 and not recovery:
            tidusPos = memory.main.get_coords()
            guadoPos = memory.main.get_actor_coords(17)
            if abs(tidusPos[0] - guadoPos[0]) + abs(tidusPos[1] - guadoPos[1]) < 30:
                while memory.main.user_control():
                    targetPathing.set_movement([guadoPos[0], guadoPos[1]])
                    xbox.tap_b()
                recovery = True
            else:
                FFXC.set_value("Dpad", 1)
                memory.main.wait_frames(3)
                FFXC.set_value("Dpad", 0)
                memory.main.wait_frames(5)
                pos = memory.main.get_coords()

        memory.main.wait_frames(30 * 0.15)
        FFXC.set_movement(0, -1)
        memory.main.wait_frames(30 * 0.04)
        FFXC.set_neutral()  # Face downward
        memory.main.wait_frames(4)
        skipActivate = False
        while not skipActivate and not recovery:
            tidusPos = memory.main.get_coords()
            guadoPos = memory.main.get_actor_coords(17)
            if abs(tidusPos[0] - guadoPos[0]) + abs(tidusPos[1] - guadoPos[1]) < 30:
                if guadoPos[0] < 10:
                    skipActivate = True
                    print("MARK")
                    xbox.skip_dialog(0.5)
            elif pos[1] > -9:
                FFXC.set_value("Dpad", 2)
                memory.main.wait_frames(2)
                FFXC.set_value("Dpad", 0)
                memory.main.wait_frames(5)
                pos = memory.main.get_coords()

        if not recovery:
            # Time limit for safety
            startTime = time.time()
            # Max number of seconds that we will wait for the skip to occur.
            timeLimit = 8
            maxTime = startTime + timeLimit

            # Waiting for walking guado to push us into the door
            while memory.main.get_camera()[0] < 0.6:
                currentTime = time.time()
                if currentTime > maxTime:
                    print("Skip failed for some reason. Moving on without skip.")
                    break
            memory.main.wait_frames(30 * 0.035)  # Guado potions good!
            xbox.tap_b()
        checkpoint = 0

    guadoSkipStatus = False
    while memory.main.get_map() != 140:
        if memory.main.user_control():
            if checkpoint == 5:
                print(memory.main.get_camera())
                if memory.main.get_camera()[1] < -9:
                    print("Guado skip success.")
                    if game_vars.csr():
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
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 24:  # Back to party
                print("Back to party")
                memory.main.click_to_event_temple(7)
                checkpoint += 1

            # General pathing
            elif memory.main.user_control():
                if targetPathing.set_movement(targetPathing.guado_skip(checkpoint)):
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
    FFXC.set_neutral()
    return guadoSkipStatus
