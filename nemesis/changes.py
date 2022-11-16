import logging

import area.gagazet
import battle.main
import memory.main
import nemesis.nemesis_pathing
import rng_track
import vars
import xbox

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


# The following functions replace the default ones from the regular Bahamut run.


def arena_npc():
    memory.main.await_control()
    if memory.main.get_map() != 307:
        return
    while not (
        memory.main.diag_progress_flag() == 74 and memory.main.diag_skip_possible()
    ):
        if memory.main.user_control():
            if memory.main.get_coords()[1] > -12:
                FFXC.set_movement(0, -1)
                memory.main.wait_frames(1)
            else:
                nemesis.nemesis_pathing.set_movement([2, -15])
                xbox.tap_b()
        else:
            FFXC.set_neutral()
            if memory.main.diag_progress_flag() == 59:
                xbox.menu_a()
                xbox.menu_a()
                xbox.menu_a()
                xbox.menu_a()
                xbox.tap_b()
            elif memory.main.diag_skip_possible():
                xbox.tap_b()
    memory.main.wait_frames(3)


def next_race():
    FFXC.set_neutral()
    memory.main.click_to_diag_progress(28)
    memory.main.wait_frames(9)
    xbox.tap_b()


def calm_lands():
    # Start chocobo races
    calm_lands_1()

    FFXC.set_neutral()
    memory.main.click_to_diag_progress(28)
    memory.main.wait_frames(9)
    xbox.tap_b()
    wobbly_complete = False
    while not wobbly_complete:
        wobbly_complete = choco_tame_1()

    logger.debug("Wobbly Chocobo complete")
    # Shenef don't remove these please.
    # next_race()
    # dodger_complete = False
    # while not dodger_complete:
    #     dodger_complete = choco_tame_2()

    # logger.debug("Dodger Chocobo complete")
    # next_race()

    # hyper_complete = False
    # while not hyper_complete:
    #     hyper_complete = choco_tame_3()

    # logger.debug("Hyper Chocobo complete")

    # catcher_complete = False
    # while not catcher_complete:
    #     catcher_complete = choco_tame_4()

    #logger.debug("Catcher Chocobo complete")

    to_remiem()


def calm_lands_1():
    # Enter the cutscene that starts Calm Lands
    memory.main.full_party_format("yuna", full_menu_close=True)
    while not (memory.main.get_coords()[1] >= -1650 and memory.main.user_control()):
        if memory.main.user_control():
            FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()

    # Now head to the chocobo lady.
    # memory.set_encounter_rate(0) #Testing only
    checkpoint = 0
    while memory.main.get_map() != 307:
        if memory.main.user_control():
            # if checkpoint == 10:
            #     if area.gagazet.check_gems() < 2:
            #         checkpoint -= 2
            if (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.calm_lands_1(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                if area.gagazet.check_gems() < 2:
                    battle.main.calm_lands_gems()
                else:
                    battle.main.calm_lands_manip()
                memory.main.full_party_format("rikku", full_menu_close=True)
                battle.main.heal_up(full_menu_close=True)
                rng_track.print_manip_info()
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()

    logger.debug("Now talk to NPC")
    # arena_npc()
    # arena_purchase()
    # memory.wait_frames(6)
    # xbox.tap_b() #I want to ride a chocobo.


def choco_tame_1():
    memory.main.click_to_diag_progress(43)
    while not memory.main.diag_progress_flag() in [44, 74]:
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

    while not memory.main.diag_progress_flag() in [51, 69, 74]:
        # 51 is success
        xbox.tap_b()
    if memory.main.diag_progress_flag() == 51:  # Success
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        xbox.tap_down()  # Up for next race, down for quit
        xbox.tap_b()
        # memory.wait_frames(20)
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
    while not memory.main.diag_progress_flag() in [44, 74]:
        angle = memory.main.get_actor_angle(0)
        position = memory.main.get_actor_coords(0)

        if (
            position[1] > -1360 and checkpoint == 0
        ):  # Start off aiming right to manip balls
            checkpoint += 1
            FFXC.set_value("d_pad", 8)  # Right
            memory.main.wait_frames(5)
            FFXC.set_value("d_pad", 0)
        if position[1] > -1200 and checkpoint == 1:  # Slight left
            checkpoint += 1
            FFXC.set_value("d_pad", 4)  # Left
            memory.main.wait_frames(11)
            FFXC.set_value("d_pad", 0)
        if position[1] > -1000 and checkpoint == 2:  # Straighten out
            checkpoint += 1
            FFXC.set_value("d_pad", 8)  # Right
            memory.main.wait_frames(7)
            FFXC.set_value("d_pad", 0)
        if position[1] > -800 and checkpoint == 3:  # Juke right
            checkpoint += 1
            FFXC.set_value("d_pad", 8)  # Right
            memory.main.wait_frames(5)
            FFXC.set_value("d_pad", 0)
        if position[1] > -650 and checkpoint == 4:  # Back to the left
            checkpoint += 1
            FFXC.set_value("d_pad", 4)  # Left
            memory.main.wait_frames(11)
            FFXC.set_value("d_pad", 0)
        if position[1] > -550 and checkpoint == 5:  # Straighten out
            checkpoint += 1
            FFXC.set_value("d_pad", 8)  # Right
            memory.main.wait_frames(6)
            FFXC.set_value("d_pad", 0)
        if position[1] > -450 and checkpoint == 6:  # Juke right again
            checkpoint += 1
            FFXC.set_value("d_pad", 8)
            memory.main.wait_frames(6)
            FFXC.set_value("d_pad", 0)
        if position[1] > -250 and checkpoint == 7:  # Straighten out
            checkpoint += 1
            FFXC.set_value("d_pad", 4)
            memory.main.wait_frames(14)
            FFXC.set_value("d_pad", 0)
        if position[1] > -90 and checkpoint == 8:  # The final juke!
            checkpoint += 1
            FFXC.set_value("d_pad", 8)
            memory.main.wait_frames(13)
            FFXC.set_value("d_pad", 0)
    FFXC.set_neutral()

    while not memory.main.diag_progress_flag() in [54, 69, 77]:
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
    while not memory.main.diag_progress_flag() in [44, 74]:
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
        if position[1] > -120 and checkpoint == 10:
            checkpoint += 1
            FFXC.set_value("d_pad", 8)
            memory.main.wait_frames(16)
            FFXC.set_value("d_pad", 0)
        if position[1] > -20 and checkpoint == 11:
            checkpoint += 1
            FFXC.set_value("d_pad", 4)
            memory.main.wait_frames(10)
            FFXC.set_value("d_pad", 0)
    FFXC.set_neutral()

    while not memory.main.diag_progress_flag() in [56, 69, 77]:
        # 56 is success
        xbox.tap_b()
    if memory.main.diag_progress_flag() == 56:  # Success
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        xbox.tap_down()  # Up for something else, down for done.
        xbox.tap_b()
        memory.main.wait_frames(30)
        # xbox.tap_up()
        # xbox.tap_b()
        return True
    else:
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        xbox.tap_b()
        return False


def choco_tame_4():
    logger.debug("START - CATCHER CHOCOBO")
    memory.main.click_to_diag_progress(43)
    checkpoint = 0
    while not memory.main.diag_progress_flag() in [44, 67]:
        angle = memory.main.get_actor_angle(0)
        position = memory.main.get_actor_coords(0)
        logger.debug("User control")
        """
        if position[1] > -1360 and checkpoint == 0: #Start off aiming right to manip balls
            checkpoint += 1
            FFXC.set_value('d_pad', 8) #Right
            memory.wait_frames(5)
            FFXC.set_value('d_pad', 0)
        if position[1] > -1200 and checkpoint == 1: #Slight left
            checkpoint += 1
            FFXC.set_value('d_pad', 4)#Left
            memory.wait_frames(10)
            FFXC.set_value('d_pad', 0)
        if position[1] > -770 and checkpoint == 3: #Left between balls
            checkpoint += 1
            FFXC.set_value('d_pad', 4)#Left
            memory.wait_frames(10)
            FFXC.set_value('d_pad', 0)
        if position[1] > -600 and checkpoint == 4: #Straighten out
            checkpoint += 1
            FFXC.set_value('d_pad', 8) #Right
            memory.wait_frames(6)
            FFXC.set_value('d_pad', 0)
        if position[1] > -100:
            if position[0] > -40:
                FFXC.set_value('d_pad', 4)#Left
            elif position[0] < -100:
                FFXC.set_value('d_pad', 8) #Right
            elif angle > 1.7:
                FFXC.set_value('d_pad', 8) #Right
            elif angle < 1.3:
                FFXC.set_value('d_pad', 4)#Left
            else:
                FFXC.set_value('d_pad', 0)
    """
    logger.debug("Race complete.")
    FFXC.set_neutral()

    while not memory.main.diag_progress_flag() in [67, 77]:
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
    memory.main.click_to_control()
    while memory.main.user_control():
        nemesis.nemesis_pathing.set_movement([-1565, 434])
        xbox.tap_b()
        logger.debug("Near chocobo lady")
    FFXC.set_neutral()
    memory.main.click_to_control_3()

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
                    nemesis.nemesis_pathing.set_movement([770, 631])
                    xbox.tap_b()
                memory.main.click_to_control_3()
                checkpoint += 1
            elif (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.to_remiem(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")


def remiem_races():
    logger.debug("Ready to start races")
    choco_race_1()
    logger.debug("Celestial Weapon obtained.")
    # Shenef, don't remove these please. I want to play with them later.
    # choco_race_2()
    # logger.debug("Obtained")
    # choco_race_3()
    # logger.debug("Something obtained")
    logger.debug("Now heading back to the monster arena.")


def choco_race_1():
    while memory.main.user_control():
        nemesis.nemesis_pathing.set_movement([790, 60])
        xbox.tap_b()
    FFXC.set_neutral()
    memory.main.click_to_control()
    checkpoint = 0
    while checkpoint != 37:
        if memory.main.user_control():
            if (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.race_1(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
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
        nemesis.nemesis_pathing.set_movement([790, 60])
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
            if (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.race_2(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
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
        nemesis.nemesis_pathing.set_movement([790, 60])
        xbox.tap_b()
    FFXC.set_neutral()
    checkpoint = 0
    while checkpoint != 44:
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
            if (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.race_3(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
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


def temple_to_arena():
    memory.main.click_to_control_3()
    checkpoint = 0
    while memory.main.get_map() != 307:
        if memory.main.user_control():
            if memory.main.get_map() == 223 and checkpoint < 18:
                checkpoint = 18

            elif checkpoint == 20:
                while memory.main.user_control():
                    nemesis.nemesis_pathing.set_movement([1261, -1238])
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_control()
                checkpoint += 1

            elif checkpoint == 24:
                logger.debug("Feather")
                while memory.main.user_control():
                    nemesis.nemesis_pathing.set_movement([1101, -940])
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.await_control()
                checkpoint += 1
            elif (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.leave_remiem(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")


def arena_purchase():
    memory.main.click_to_control()

    logger.debug("Straight forward to the guy")
    FFXC.set_movement(0, 1)
    memory.main.click_to_event()
    FFXC.set_neutral()
    logger.debug("Now for dialog")
    memory.main.click_to_diag_progress(65)
    logger.debug("Select Sure")
    memory.main.wait_frames(15)
    xbox.tap_down()
    xbox.tap_b()
    memory.main.click_to_diag_progress(73)
    memory.main.wait_frames(15)
    # xbox.tap_up()
    xbox.tap_b()  # Let's see your weapons
    # memory.wait_frames(9000)
    nemesis.menu.arena_purchase_1()
    # Sell all undesirable equipment
    # Purchase the following weapons:
    # -Tidus x4
    # -Yuna x1

    # ---Done buying.
    memory.main.await_control()
    memory.main.wait_frames(2)
    FFXC.set_movement(0, -1)
    memory.main.await_event()  # Exit the arena map
    FFXC.set_neutral()
    memory.main.await_control()

    checkpoint = 0
    while memory.main.get_map() != 279:
        if memory.main.user_control():
            if checkpoint == 7 and area.gagazet.check_gems() < 2:
                checkpoint -= 2
            elif (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.calm_lands_2(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                if area.gagazet.check_gems() < 2:
                    battle.main.calm_lands_gems()
                else:
                    battle.main.calm_lands_manip()
                memory.main.full_party_format("yuna")
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()


def arena_purchase_with_chocobo():
    while memory.main.user_control():  # Back onto chocobo
        nemesis.nemesis_pathing.set_movement([1347, -69])
        xbox.tap_b()

    while not nemesis.nemesis_pathing.set_movement([1488, 778]):
        pass
    while not nemesis.nemesis_pathing.set_movement([1545, 1088]):
        pass
    while not memory.main.get_map() == 279:
        nemesis.nemesis_pathing.set_movement([1700, 1200])

    memory.main.full_party_format("kimahri")
