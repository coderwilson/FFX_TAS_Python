import logging
import time

import memory.main
import pathing
import vars
import xbox
from paths import GuadoSkip, GuadoStoryline

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def arrival():
    logger.info("Starting Guadosalam section")
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

    logger.debug(f"Test Var (CSR) - {game_vars.csr}")
    # Adjusted branch CSR logic, start
    memory.main.click_to_control_3()
    if game_vars.csr():
        while not pathing.set_movement([-13, -67]):
            pass
        logger.debug("Lulu conversation")
        while memory.main.user_control():  # Lulu conversation
            pathing.set_movement([-11, -55])
            xbox.tap_b()
        FFXC.set_neutral()
        memory.main.click_to_control_3()

        while not pathing.set_movement([-39, -77]):
            pass
        logger.debug("Wakka conversation")
        while memory.main.user_control():  # Start conversation with Wakka
            pathing.set_movement([-49, -61])
            xbox.tap_b()
        FFXC.set_neutral()
        memory.main.click_to_control_3()

        while not pathing.set_movement([4, -114]):
            pass
        logger.debug("Talk to Auron")
        while memory.main.user_control():  # Talk to Auron
            pathing.set_movement([18, -119])
            xbox.tap_b()
        FFXC.set_neutral()
        memory.main.click_to_control_3()

    else:
        while not pathing.set_movement([4, -114]):
            pass
        logger.debug("Talk to Auron")
        while memory.main.user_control():  # Talk to Auron (first for affection)
            pathing.set_movement([18, -119])
            xbox.tap_b()
        FFXC.set_neutral()
        memory.main.click_to_control_3()

        while not pathing.set_movement([-39, -77]):
            pass
        logger.debug("Wakka conversation")
        while memory.main.user_control():  # Start conversation with Wakka
            pathing.set_movement([-49, -61])
            xbox.tap_b()
        FFXC.set_neutral()
        memory.main.click_to_control_3()

        while not pathing.set_movement([-13, -67]):
            pass
        logger.debug("Lulu conversation")
        while memory.main.user_control():  # Lulu conversation
            pathing.set_movement([-11, -55])
            xbox.tap_b()
        FFXC.set_neutral()
        memory.main.click_to_control_3()

    # Line up for Rikku/Yuna
    while not pathing.set_movement([15, -52]):
        pass

    while not pathing.set_movement([22, -25]):
        pass
    logger.debug("Rikku conversation")
    while memory.main.user_control():  # Start conversation with Rikku
        pathing.set_movement([8, -26])
        xbox.tap_b()
    FFXC.set_neutral()
    memory.main.click_to_control_3()

    while not pathing.set_movement([27, -37]):
        pass
    logger.debug("Yuna conversation")
    while memory.main.user_control():  # Yunas turn
        pathing.set_movement([39, -33])
        xbox.tap_b()
    FFXC.set_neutral()
    memory.main.click_to_control_3()

    if not game_vars.csr():
        while not memory.main.cutscene_skip_possible():
            xbox.tap_b()
        xbox.skip_stored_scene(3)
    # Adjusted CSR branch logic, end
    logger.debug("Ready for next movement.")


def after_speech(checkpoint=0):
    memory.main.click_to_control()  # Skips through the long cutscene
    logger.debug("Starting movement.")
    logger.debug(f"Starting checkpoint: {checkpoint}")

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

            elif pathing.set_movement(GuadoStoryline.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
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
        logger.debug("Past walking guado")
        while pos[1] < 50:
            pos = memory.main.get_coords()
        FFXC.set_movement(1, 0)
        logger.debug("Angle right")
        while pos[0] < -44:
            pos = memory.main.get_coords()
        FFXC.set_movement(1, -1)
        logger.debug("Towards position")
        while pos[0] < 9:
            pos = memory.main.get_coords()
        FFXC.set_movement(0, -1)
        logger.debug("Adjustment 1")
        while pos[1] > -7.5:
            pos = memory.main.get_coords()
        FFXC.set_neutral()
        memory.main.wait_frames(5)

        pos = memory.main.get_coords()
        recovery = False
        logger.debug("Adjustment 2")
        while pos[0] > 8 and not recovery:
            tidus_pos = memory.main.get_coords()
            guado_pos = memory.main.get_actor_coords(17)
            if abs(tidus_pos[0] - guado_pos[0]) + abs(tidus_pos[1] - guado_pos[1]) < 30:
                while memory.main.user_control():
                    pathing.set_movement(guado_pos[0], guado_pos[1])
                    xbox.tap_b()
                recovery = True
            else:
                FFXC.set_value("d_pad", 4)
                memory.main.wait_frames(3)
                FFXC.set_value("d_pad", 0)
                memory.main.wait_frames(5)
                pos = memory.main.get_coords()
        logger.debug("Adjustment 3")
        while pos[1] < -8.5 and not recovery:
            tidus_pos = memory.main.get_coords()
            guado_pos = memory.main.get_actor_coords(17)
            if abs(tidus_pos[0] - guado_pos[0]) + abs(tidus_pos[1] - guado_pos[1]) < 30:
                while memory.main.user_control():
                    pathing.set_movement([guado_pos[0], guado_pos[1]])
                    xbox.tap_b()
                recovery = True
            else:
                FFXC.set_value("d_pad", 1)
                memory.main.wait_frames(3)
                FFXC.set_value("d_pad", 0)
                memory.main.wait_frames(5)
                pos = memory.main.get_coords()

        memory.main.wait_frames(30 * 0.15)
        FFXC.set_movement(0, -1)
        memory.main.wait_frames(30 * 0.04)
        FFXC.set_neutral()  # Face downward
        memory.main.wait_frames(4)
        skip_activate = False
        while not skip_activate and not recovery:
            tidus_pos = memory.main.get_coords()
            guado_pos = memory.main.get_actor_coords(17)
            if abs(tidus_pos[0] - guado_pos[0]) + abs(tidus_pos[1] - guado_pos[1]) < 30:
                if guado_pos[0] < 10:
                    skip_activate = True
                    logger.debug("MARK")
                    xbox.skip_dialog(0.5)
            elif pos[1] > -9:
                FFXC.set_value("d_pad", 2)
                memory.main.wait_frames(2)
                FFXC.set_value("d_pad", 0)
                memory.main.wait_frames(5)
                pos = memory.main.get_coords()

        if not recovery:
            # Time limit for safety
            start_time = time.time()
            # Max number of seconds that we will wait for the skip to occur.
            time_limit = 8
            max_time = start_time + time_limit

            # Waiting for walking guado to push us into the door
            while memory.main.get_camera()[0] < 0.6:
                current_time = time.time()
                if current_time > max_time:
                    logger.warning("Skip failed for some reason. Moving on without it.")
                    break
            memory.main.wait_frames(30 * 0.035)  # Guado potions good!
            xbox.tap_b()
        checkpoint = 0

    guado_skip_status = False
    while memory.main.get_map() != 140:
        if memory.main.user_control():
            if checkpoint == 5:
                logger.debug(f"Get camera: {memory.main.get_camera()}")
                if memory.main.get_camera()[1] < -9:
                    logger.info("Guado skip success.")
                    if game_vars.csr():
                        guado_skip_status = False
                        checkpoint = 18
                    else:
                        guado_skip_status = True
                        checkpoint += 1
                else:
                    logger.warning("Guado skip fail. Back-up strats.")
                    guado_skip_status = False
                    checkpoint = 18
            elif checkpoint == 21:  # Shelinda conversation
                logger.debug("Shelinda")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 24:  # Back to party
                logger.debug("Back to party")
                memory.main.click_to_event_temple(7)
                checkpoint += 1

            # General pathing
            elif memory.main.user_control():
                if pathing.set_movement(GuadoSkip.execute(checkpoint)):
                    checkpoint += 1
                    logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
    FFXC.set_neutral()
    return guado_skip_status
