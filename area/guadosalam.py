import logging
import time

import memory.main
from memory.main import calculate_encounter_count
import pathing
import vars
import xbox
from paths import GuadoSkip, GuadoStart, GuadoStoryline
from players import Auron, Lulu, Rikku, Wakka, Yuna
import battle.main
import menu
from json_ai_files.write_seed import write_big_text

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def arrival():
    logger.info("Starting Guadosalam section")
    checkpoint = 0
    FFXC.set_neutral()
    if game_vars.story_mode() and not game_vars.create_saves():
        memory.main.wait_seconds(69)
    memory.main.click_to_control_3()

    # Predicting thunder plains ambushes
    segments_1 = [2223]
    enc_count, second_ptr = calculate_encounter_count(segments_1, danger_val=35, initial_ptr=0)
    segments_2 = [1455,675]
    enc_count_2, second_ptr = calculate_encounter_count(segments_2, danger_val=30, initial_ptr=second_ptr)
    enc_count += enc_count_2
    str_1 = f"We are expecting {enc_count} encounters in Thunder Plains."
    logger.info(str_1)
    count_noflip = memory.main.ambush_count(battles=enc_count,extra=0)
    count_flip = memory.main.ambush_count(battles=enc_count,extra=1)
    str_2 = f"Ambush counts: if {count_noflip} > {count_flip} => flip!"
    logger.info(str_2)
    write_big_text(str_1 + "\n" + str_2)
    if count_noflip > count_flip+1:  # At least two more ambushes
        # Map change
        while not pathing.set_movement([21,-22]):
            pass
        while memory.main.get_map() == 135:
            pathing.set_movement([35,22])

        # Flip it!
        while not pathing.set_movement([20,-30]):
            pass
        reverse_battle_rng(realign=False)
        while not pathing.set_movement([2,-45]):
            pass
        while memory.main.get_map() != 135:
            pathing.set_movement([2,-80])


    while memory.main.get_map() != 141:  # Up to the dining hall scenes
        if memory.main.user_control():
            if checkpoint == 4:
                # Into the first door
                write_big_text("")
                if 1 in memory.main.ambushes():
                    FFXC.set_neutral()
                    battle.main.heal_up(full_menu_close=False)
                menu.t_plains_terra_skip()
                FFXC.set_movement(-1, 1)
                memory.main.await_event()
                checkpoint += 1
            elif checkpoint == 6:
                # Back out the door
                if memory.main.get_story_progress() < 1104:
                    FFXC.set_movement(0, -1)
                    memory.main.await_event()
                checkpoint += 1
            elif checkpoint == 8:
                # Into the dining hall
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                checkpoint += 1
            elif pathing.set_movement(GuadoStart.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if not game_vars.story_mode():
                xbox.tap_confirm()

    # Checkpoint carries over.
    # We skip the first movement checkpoint, replaced by the approach feature.
    checkpoint += 1
    logger.info("Now in the room with all the food")
    while not memory.main.get_map() == 163:
        if memory.main.user_control():
            if checkpoint == 10:
                if game_vars.csr():
                    pathing.approach_party_member(Wakka)
                else:
                    pathing.approach_party_member(Auron)
                checkpoint += 1
            elif checkpoint == 11:
                if game_vars.csr():
                    pathing.approach_party_member(Lulu)
                else:
                    pathing.approach_party_member(Wakka)
                checkpoint += 1
            elif checkpoint == 12:
                if game_vars.csr():
                    pathing.approach_party_member(Auron)
                    checkpoint = 15
                else:
                    pathing.approach_party_member(Lulu)
                    checkpoint += 1
            elif checkpoint == 18:
                pathing.approach_party_member(Rikku)
                checkpoint += 1
            elif checkpoint == 20:
                pathing.approach_party_member(Yuna)
                checkpoint += 1
            elif pathing.set_movement(GuadoStart.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                memory.main.wait_frames(9)
                xbox.skip_stored_scene()
                memory.main.click_to_control()

    # Adjusted CSR branch logic, end
    logger.debug("Ready for next movement.")


def primer1():
    while not pathing.set_movement([-80,-29]):
        pass
    while not pathing.set_movement([-153,60]):
        pass
    while memory.main.user_control():
        pathing.set_movement([-168,85])
    FFXC.set_neutral()
    memory.main.await_control()
    while not pathing.set_movement([-19,-6]):
        pass
    pathing.primer()
    while not pathing.set_movement([-19,-6]):
        pass
    #while not pathing.set_movement([14,-27]):
    #    pass
    while memory.main.user_control():
        pathing.set_movement([20,-35])
    FFXC.set_neutral()
    memory.main.await_control()


def after_speech(checkpoint=0):
    memory.main.click_to_control()  # Skips through the long cutscene
    logger.debug("Starting movement.")
    logger.debug(f"Starting Checkpoint {checkpoint}")
    farplane_lulu = game_vars.story_mode()
    get_primer = game_vars.platinum()

    if checkpoint == 0:
        memory.main.click_to_event_temple(4)

    while checkpoint != 34:
        if memory.main.user_control():
            if checkpoint > 17 and checkpoint < 26 and memory.main.get_map() == 135:
                checkpoint = 26
            elif checkpoint == 1:
                memory.main.click_to_event_temple(4, story_mode_dialog=True)
                checkpoint += 1
            elif checkpoint in [12, 16, 21]:
                memory.main.click_to_event_temple(0, story_mode_dialog=True)
                checkpoint += 1
            elif checkpoint == 33:
                if game_vars.story_mode():
                    FFXC.set_movement(0,1)
                    memory.main.await_event()
                    FFXC.set_neutral()
                    memory.main.wait_seconds(32)
                    xbox.tap_down()
                    xbox.tap_confirm()  # I guess you're right (big chance with Yuna)
                    #xbox.tap_up()
                    #xbox.tap_confirm()  # I'd rather have you, Rikku.
                    memory.main.await_control()
                else:
                    memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 31 and get_primer:
                primer1()
                get_primer = False
            elif checkpoint == 17:
                if not game_vars.csr():
                    memory.main.click_to_event_temple(0, story_mode_dialog=True)
                checkpoint += 1
            elif checkpoint == 14:
                memory.main.click_to_event_temple(5)
                checkpoint += 1
            elif checkpoint == 23:
                logger.warning("Approaching Wakka")
                memory.main.click_to_event_temple(2, story_mode_dialog=True)
                checkpoint += 1
            #elif checkpoint == 24 and farplane_lulu:
            #    memory.main.check_near_actors()
            #    logger.warning("Approaching Lulu")
            #    memory.main.click_to_event_temple(1, story_mode_dialog=True)
            #    farplane_lulu = False
            elif checkpoint == 25:
                logger.warning("Approaching Yuna")
                memory.main.click_to_event_temple(7, story_mode_dialog=True)
                checkpoint += 1

            elif pathing.set_movement(GuadoStoryline.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
            elif memory.main.get_story_progress() == 1190 and memory.main.diag_progress_flag() == 82:
                xbox.tap_confirm()
    logger.debug("End of farplane section.")



def guado_skip():
    memory.main.click_to_control()
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
                memory.main.click_to_event_temple(0, story_mode_dialog=True)
                checkpoint += 1
            elif checkpoint == 24:  # Back to party
                logger.debug("Back to party")
                memory.main.click_to_event_temple(7, story_mode_dialog=True)
                checkpoint += 1

            # General pathing
            elif memory.main.user_control():
                if pathing.set_movement(GuadoSkip.execute(checkpoint)):
                    checkpoint += 1
                    logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_b()
    FFXC.set_neutral()
    logger.debug("End of Guadosalam section.")
    return guado_skip_status

def reverse_battle_rng(realign=True):
    FFXC.set_neutral()
    memory.main.check_near_actors()
    pathing.approach_actor_by_id(actor_id=20496)
    FFXC.set_neutral()
    memory.main.wait_frames(63)

    # Start battle
    xbox.tap_down()
    xbox.tap_b()
    xbox.tap_b()
    xbox.click_to_battle()

    # Escape and back out of menu
    battle.main.flee_all()
    while not memory.main.user_control():
        xbox.tap_a()

    if realign:
        # Back to alginment with the path
        while not pathing.set_movement([-69,156]):
            pass
