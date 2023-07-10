import logging

import battle.main
import memory.main
import pathing
import xbox
import math
from paths.nem import Race1, Race2, Race3, ToRemiem

FFXC = xbox.controller_handle()
logger = logging.getLogger(__name__)

try_fourth_race = False


def all_races():
    # equip

    # counter = 0
    while not pathing.set_movement([-637, -246]):
        pass
    pathing.approach_actor_by_id(actor_id=20531)
    FFXC.set_neutral()
    memory.main.click_to_diag_progress(302)
    memory.main.wait_frames(30)
    xbox.menu_down()
    xbox.menu_down()
    xbox.tap_b()

    wobbly_complete = False
    while not wobbly_complete:
        wobbly_complete = choco_tame_1()

    logger.debug("Wobbly Chocobo complete")
    next_race()
    dodger_complete = False
    while not dodger_complete:
        dodger_complete = choco_tame_2()

    logger.debug("Dodger Chocobo complete")
    next_race()

    hyper_complete = False
    while not hyper_complete:
        hyper_complete = choco_tame_3()

    logger.debug("Hyper Chocobo complete")
    if try_fourth_race:
        catcher_complete = False
        while not catcher_complete:
            catcher_complete = choco_tame_4()

        logger.debug("Catcher Chocobo complete")


def choco_tame_1():
    memory.main.click_to_diag_progress(43)
    logger.info("Race start!")
    while memory.main.diag_progress_flag() not in [44, 74]:
        angle = memory.main.get_actor_angle(0)
        position = memory.main.get_actor_coords(0)
        if position[0] < -110:  # Need to move right
            if angle > 1.4:
                FFXC.set_value("d_pad", 8)
            elif angle < 1.2:
                FFXC.set_value("d_pad", 4)
            else:
                FFXC.set_value("d_pad", 0)
        elif position[0] > -60:  # Need to move left
            if angle > 1.8:
                FFXC.set_value("d_pad", 8)
            elif angle < 1.6:
                FFXC.set_value("d_pad", 4)
            else:
                FFXC.set_value("d_pad", 0)
        else:
            if angle > 1.6:  # Stay straight
                FFXC.set_value("d_pad", 8)
            elif angle < 1.4:
                FFXC.set_value("d_pad", 4)
            else:
                FFXC.set_value("d_pad", 0)
    FFXC.set_neutral()
    logger.info("Race end!")

    last_flag = 0
    while memory.main.diag_progress_flag() not in [51, 52, 53, 69, 74]:
        # 51 is success
        xbox.tap_b()
        if last_flag != memory.main.diag_progress_flag():
            logger.debug(f"Update: {memory.main.diag_progress_flag()}")
            last_flag = memory.main.diag_progress_flag()
    if memory.main.diag_progress_flag() in [51, 52, 53]:  # Success
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        xbox.tap_up()  # Up for next race, down for quit
        xbox.tap_b()
        memory.main.wait_frames(20)
        xbox.tap_up()
        xbox.tap_b()
        return True
    else:
        memory.main.click_to_diag_progress(76)
        memory.main.wait_frames(12)
        xbox.tap_b()
        return False


def choco_tame_2():
    memory.main.click_to_diag_progress(43)
    checkpoint = 0
    last_cp = 0
    while memory.main.diag_progress_flag() not in [44, 74]:
        if last_cp != checkpoint:
            logger.debug(f"Checkpoint: {checkpoint}")
            last_cp = checkpoint
        memory.main.get_actor_angle(0)
        position = memory.main.get_actor_coords(0)

        if (
            position[1] > -1360 and checkpoint == 0
        ):  # Start off aiming right to manip balls
            checkpoint += 1
            FFXC.set_value("d_pad", 8)  # Start to the Right
            memory.main.wait_frames(5)
            FFXC.set_value("d_pad", 0)
        if position[1] > -1200 and checkpoint == 1:  # Slight left
            checkpoint += 1
            FFXC.set_value("d_pad", 4)  # Left
            memory.main.wait_frames(11)
            FFXC.set_value("d_pad", 0)
        if position[1] > -970 and checkpoint == 2:  # Straighten out
            checkpoint += 1
            FFXC.set_value("d_pad", 8)  # Right
            memory.main.wait_frames(7)
            FFXC.set_value("d_pad", 0)
        if position[1] > -800 and checkpoint == 3:  # Juke right
            checkpoint += 1
            FFXC.set_value("d_pad", 8)  # Right
            memory.main.wait_frames(6)
            FFXC.set_value("d_pad", 0)
        if position[1] > -675 and checkpoint == 4:  # Quick left
            checkpoint += 1
            FFXC.set_value("d_pad", 4)  # Left
            memory.main.wait_frames(11)
            FFXC.set_value("d_pad", 0)
        if position[1] > -550 and checkpoint == 5:  # Left to right
            checkpoint += 1
            FFXC.set_value("d_pad", 8)  # Right
            memory.main.wait_frames(6)
            FFXC.set_value("d_pad", 0)
        if position[1] > -450 and checkpoint == 6:  # Juke left again
            checkpoint += 1
            FFXC.set_value("d_pad", 8)
            memory.main.wait_frames(6)
            FFXC.set_value("d_pad", 0)
        if position[1] > -250 and checkpoint == 7:  # Right to left
            checkpoint += 1
            FFXC.set_value("d_pad", 4)
            memory.main.wait_frames(14)
            FFXC.set_value("d_pad", 0)
        if position[1] > -110 and checkpoint == 8:
            checkpoint += 1
            FFXC.set_value("d_pad", 4)
            memory.main.wait_frames(14)
            FFXC.set_value("d_pad", 0)
        if position[1] > -90 and checkpoint == 9:  # The final juke right!
            checkpoint += 1
            FFXC.set_value("d_pad", 8)
            memory.main.wait_frames(6)
            FFXC.set_value("d_pad", 0)
        if position[1] > -90 and checkpoint == 10:  # The final juke right!
            checkpoint += 1
            FFXC.set_value("d_pad", 4)
            memory.main.wait_frames(12)
            FFXC.set_value("d_pad", 0)
    FFXC.set_neutral()

    while memory.main.diag_progress_flag() not in [54, 69, 77]:
        # 54 is success
        xbox.tap_b()
    if memory.main.diag_progress_flag() == 54:  # Success
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        xbox.tap_up()
        xbox.tap_b()
        memory.main.wait_frames(30)
        xbox.tap_up()
        xbox.tap_b()
        return True
    else:
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        xbox.tap_b()
        return False


def choco_tame_3():
    memory.main.click_to_diag_progress(43)
    checkpoint = 0
    last_cp = 0
    while memory.main.diag_progress_flag() not in [44, 74]:
        if last_cp != checkpoint:
            logger.debug(f"Checkpoint: {checkpoint}")
            last_cp = checkpoint
        position = memory.main.get_actor_coords(0)
        if position[1] > -1370 and checkpoint == 0:
            checkpoint += 1
            FFXC.set_value("d_pad", 4)  # Left
            memory.main.wait_frames(3)
            FFXC.set_value("d_pad", 0)
        if position[1] > -1200 and checkpoint == 1:
            checkpoint += 1
            FFXC.set_value("d_pad", 8)  # Right
            memory.main.wait_frames(10)
            FFXC.set_value("d_pad", 0)
        if position[1] > -1100 and checkpoint == 2:
            checkpoint += 1
            FFXC.set_value("d_pad", 4)
            memory.main.wait_frames(12)
            FFXC.set_value("d_pad", 0)
        if position[1] > -1040 and checkpoint == 3:
            checkpoint += 1
            FFXC.set_value("d_pad", 8)
            memory.main.wait_frames(9)
            FFXC.set_value("d_pad", 0)
        if position[1] > -950 and checkpoint == 4:
            checkpoint += 1
            FFXC.set_value("d_pad", 4)
            memory.main.wait_frames(12)
            FFXC.set_value("d_pad", 0)
        if position[1] > -700 and checkpoint == 5:
            checkpoint += 1
            FFXC.set_value("d_pad", 8)
            memory.main.wait_frames(12)
            FFXC.set_value("d_pad", 0)
        if position[1] > -600 and checkpoint == 6:
            checkpoint += 1
            FFXC.set_value("d_pad", 4)
            memory.main.wait_frames(12)
            FFXC.set_value("d_pad", 0)
        if position[1] > -500 and checkpoint == 7:
            checkpoint += 1
            FFXC.set_value("d_pad", 4)
            memory.main.wait_frames(6)
            FFXC.set_value("d_pad", 0)
        if position[1] > -400 and checkpoint == 8:
            checkpoint += 1
            FFXC.set_value("d_pad", 8)
            memory.main.wait_frames(16)
            FFXC.set_value("d_pad", 0)
        if position[1] > -250 and checkpoint == 9:
            checkpoint += 1
            FFXC.set_value("d_pad", 4)
            memory.main.wait_frames(16)
            FFXC.set_value("d_pad", 0)
        # Still dialing in on this one.
        if position[1] > -130 and checkpoint == 10:
            checkpoint += 1
            FFXC.set_value("d_pad", 8)
            memory.main.wait_frames(18)
            FFXC.set_value("d_pad", 0)
        if position[1] > 20 and checkpoint == 11:
            checkpoint += 1
            FFXC.set_value("d_pad", 4)
            memory.main.wait_frames(10)
            FFXC.set_value("d_pad", 0)
    FFXC.set_neutral()

    while memory.main.diag_progress_flag() not in [56, 69, 77]:
        # 56 is success
        xbox.tap_b()
    if memory.main.diag_progress_flag() == 56:  # Success
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        if try_fourth_race:
            xbox.tap_up()  # Up for something else, down for done.
            # xbox.tap_down()  # Up for something else, down for done.
            xbox.tap_b()
            memory.main.wait_frames(30)
            xbox.tap_up()
        else:
            xbox.tap_down()
        xbox.tap_b()
        return True
    else:
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        xbox.tap_b()
        return False


def distance_balloon(index: int):
    try:
        player1 = memory.main.get_actor_coords(actor_index=0)
        player2 = memory.main.get_actor_coords(actor_index=index)
        return abs(player1[1] - player2[1]) + abs(player1[0] - player2[0])
    except Exception as x:
        logger.error(f"Exception: {x}")
        return 999


def closest_balloon():
    targets = memory.main.get_actor_array_size()
    # logger.debug(f"Target count: {targets}")
    closest = 999
    distance = 1000

    for i in range(targets):
        char_id = memory.main.get_actor_id(actor_num=i)
        if char_id == 0x5063:
            dist = distance_balloon(i)
            if dist < distance:
                closest = i
                distance = dist
    # logger.warning(f"Balloon: {closest} | Distance: {distance}")
    return closest


def choco_tame_4():
    logger.debug("START - CATCHER CHOCOBO")
    memory.main.click_to_diag_progress(43)
    memory.main.wait_frames(90)
    last_button = 0
    last_balloon = 999
    while memory.main.diag_progress_flag() not in [44, 67]:
        angle = memory.main.get_actor_angle(0)
        position = memory.main.get_actor_coords(0)
        balloon = closest_balloon()
        if balloon != last_balloon:
            logger.debug(f"Targetting new balloon: {balloon}")
            last_balloon = balloon
        b_pos = memory.main.get_actor_coords(balloon)
        delta_x = position[0] - b_pos[0]
        delta_y = position[1] - b_pos[1]

        desired_angle = math.atan2(delta_y, delta_x)
        # math.atan2(y,x)/math.pi*180 gives from -180 to 180
        # logger.warning(f"Desired: {desired_angle} | Actual: {angle}")

        if abs(desired_angle - angle) < 0.3:
            if last_button != 0:
                logger.debug("Straight")
                FFXC.set_neutral()
                last_button = 0
        elif desired_angle < angle:
            if last_button != 4:
                FFXC.set_neutral()
                logger.warning("Left")
                FFXC.set_value("d_pad", 4)
                last_button = 4
        else:
            if last_button != 8:
                FFXC.set_neutral()
                logger.warning("Right")
                FFXC.set_value("d_pad", 8)
                last_button = 8

    logger.debug("Race complete.")
    FFXC.set_neutral()

    while memory.main.diag_progress_flag() not in [67, 77]:
        # 67 is 0:00.0 run
        xbox.tap_b()
    if memory.main.diag_progress_flag() == 67:  # Success
        logger.debug("Great run! Perfect score!")
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        xbox.tap_down()
        xbox.tap_b()
        return True
    else:
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        xbox.tap_b()
        return False


def to_remiem():
    memory.main.await_control()
    memory.main.wait_frames(6)
    logger.info("Talking to chocobo lady")
    while memory.main.user_control():
        pathing.set_movement([-1565, 434])
        xbox.tap_b()
    FFXC.set_neutral()
    logger.info("Let me ride one!")
    memory.main.click_to_control()
    logger.info("Heading to Remiem")

    checkpoint = 0
    while checkpoint < 35:
        if memory.main.user_control():
            if memory.main.get_map() == 290 and checkpoint < 13:
                checkpoint = 13

            elif checkpoint == 10:
                logger.debug("Feather")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 27:
                logger.debug("Orb thing")
                while memory.main.user_control():
                    pathing.set_movement([770, 631])
                    xbox.tap_b()
                memory.main.click_to_control_3()
                checkpoint += 1
            elif pathing.set_movement(ToRemiem.execute(checkpoint)) is True:
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")


def remiem_races():
    logger.debug("Ready to start races")
    choco_race_1()
    logger.info("Cloudy Mirror obtained.")
    # Shenef, don't remove these please. I want to play with them later.
    choco_race_2()
    logger.info("Obtained Wings to Discovery")
    choco_race_3()
    logger.info("Obtained Three Stars!")


def choco_race_1():
    while memory.main.user_control():
        pathing.set_movement([780, 60])
        xbox.tap_b()
    FFXC.set_neutral()
    memory.main.click_to_control()
    checkpoint = 0
    while checkpoint != 37:
        if memory.main.user_control():
            if pathing.set_movement(Race1.execute(checkpoint)) is True:
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle.main.flee_all()
            else:
                xbox.tap_b()
    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(10)
    FFXC.set_neutral()
    memory.main.click_to_control_3()


def choco_race_2():
    FFXC.set_neutral()
    memory.main.click_to_control()
    while memory.main.user_control():
        pathing.set_movement([780, 60])
        xbox.tap_b()
    FFXC.set_neutral()
    checkpoint = 0
    while checkpoint != 38:
        if memory.main.user_control():
            if checkpoint == 11:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            if checkpoint == 17:
                memory.main.click_to_event_temple(5)
                checkpoint += 1
            if checkpoint == 22:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            if pathing.set_movement(Race2.execute(checkpoint)) is True:
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle.main.flee_all()
            else:
                xbox.tap_b()
    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(10)
    FFXC.set_neutral()
    memory.main.click_to_control_3()


def choco_race_3():
    FFXC.set_neutral()
    memory.main.click_to_control()
    while memory.main.user_control():
        pathing.set_movement([780, 60])
        xbox.tap_b()
    FFXC.set_neutral()
    checkpoint = 0
    while checkpoint != 43:
        if memory.main.user_control():
            if checkpoint == 11:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            if checkpoint == 17:
                memory.main.click_to_event_temple(5)
                checkpoint += 1
            if checkpoint == 22:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            if checkpoint == 27:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            if checkpoint == 39:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            # if checkpoint == 42: #Since it's not tight enough movement yet
            #     FFXC.set_neutral()
            #     memory.wait_frames(120)
            #     memory.click_to_control_3()
            #     break
            if pathing.set_movement(Race3.execute(checkpoint)) is True:
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle.main.flee_all()
            else:
                xbox.tap_b()
    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(60)
    FFXC.set_neutral()
    memory.main.click_to_control_3()
    logger.debug("End of third race")


def next_race():
    FFXC.set_neutral()
    memory.main.click_to_diag_progress(28)
    memory.main.wait_frames(9)
    xbox.tap_b()
