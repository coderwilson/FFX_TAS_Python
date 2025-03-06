import logging

import area.gagazet
from area.chocobos import choco_tame_1,choco_tame_2,choco_tame_3
import battle.main
import memory.main
import nemesis.menu
#from nemesis.arena_prep import arena_npc
import pathing
import rng_track
import vars
import xbox
from save_sphere import touch_and_go
from paths.nem import CalmLands1, CalmLands2, LeaveRemiem, Race1, Race2, Race3, ToRemiem
from players import Auron, Kimahri, Rikku, Tidus, Yuna

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


# The following functions replace the default ones from the regular Bahamut run.


def arena_npc():
    memory.main.await_control()
    report_actors = True
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
                if report_actors:
                    memory.main.check_near_actors()
                    report_actors = False
                pathing.approach_actor_by_id(8241)
                return
                # 8241 or 20482
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


def gagazet_lv_4_chest():
    steps = [
        [-547, 215],
        [-510, 212],
        [-512, 233],
        [-543, 245],
        [-570, 261],
        [0, 0],  # Open chest
        [-543, 245],
        [-512, 233],
        [-510, 212],
        [-547, 215],
        [-569, 223],
    ]
    i = 0
    while i < len(steps):
        if memory.main.user_control():
            if i == 5:
                if pathing.approach_actor_by_index(16):
                    i += 1
            elif pathing.set_movement(steps[i]):
                i += 1
                if i == 5:
                    memory.main.check_near_actors()
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle.main.flee_all()
            else:
                xbox.tap_confirm()


def calm_lands():
    if memory.main.get_map() == 329:
        while memory.main.get_map() != 223:
            pathing.set_movement([35,200])
    FFXC.set_neutral()
    # Start chocobo races
    calm_lands_1()
    logger.info("Let's train a chocobo!")

    FFXC.set_neutral()
    memory.main.click_to_diag_progress(302)
    memory.main.wait_frames(18)
    xbox.menu_down()
    xbox.menu_down()
    xbox.tap_b()

    wobbly_complete = False
    while not wobbly_complete:
        wobbly_complete = choco_tame_1()

    logger.debug("Wobbly Chocobo complete")
    dodger_complete = False
    while not dodger_complete:
        dodger_complete = choco_tame_2()

    logger.debug("Dodger Chocobo complete")

    hyper_complete = False
    while not hyper_complete:
        hyper_complete = choco_tame_3()

    logger.debug("Hyper Chocobo complete")

    # catcher_complete = False
    # while not catcher_complete:
    #     catcher_complete = choco_tame_4()

    # logger.debug("Catcher Chocobo complete")


def calm_lands_1():
    # Enter the cutscene that starts Calm Lands
    memory.main.update_formation(Tidus, Yuna, Auron, full_menu_close=True)
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
            if checkpoint == 10:
                if area.gagazet.check_gems() < 2:
                    checkpoint -= 2
            if pathing.set_movement(CalmLands1.execute(checkpoint)) is True:
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                if area.gagazet.check_gems() < 2:
                    battle.main.calm_lands_gems()
                else:
                    battle.main.calm_lands_manip()
                memory.main.update_formation(Tidus, Rikku, Auron, full_menu_close=True)
                battle.main.heal_up(full_menu_close=True)
                rng_track.print_manip_info()
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()

    logger.debug("Now talk to NPC")
    arena_npc()
    arena_purchase()
    defender_x_nemesis()
    #back_to_chocobo_spawn()

'''
def choco_tame_1():
    memory.main.click_to_diag_progress(43)
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

    while memory.main.diag_progress_flag() not in [51, 69, 74]:
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
    while memory.main.diag_progress_flag() not in [44, 74]:
        memory.main.get_actor_angle(0)
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
    while memory.main.diag_progress_flag() not in [44, 74]:
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

    while memory.main.diag_progress_flag() not in [56, 69, 77]:
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
    while memory.main.diag_progress_flag() not in [44, 67]:
        memory.main.get_actor_angle(0)
        memory.main.get_actor_coords(0)
        logger.debug("User control")
        """
        if (
            position[1] > -1360 and checkpoint == 0
        ): #Start off aiming right to manip balls
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
'''

def to_remiem():
    # Assumes we just finished training.
    memory.main.click_to_control_3()
    pathing.approach_actor_by_id(20531)
    FFXC.set_neutral()
    memory.main.click_to_control_3()
    while not pathing.set_movement([1500,883]):
        pass
    while not pathing.set_movement([1486,589]):
        pass
    while not pathing.set_movement([1121,-280]):
        pass

    checkpoint = 2
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
    logger.debug("Cloudy Mirror obtained.")
    choco_race_2()
    logger.debug("Obtained")
    choco_race_3()
    logger.debug("Something obtained")
    logger.debug("Now heading back to the monster arena.")


def choco_race_1():
    while memory.main.user_control():
        pathing.set_movement([790, 60])
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
        pathing.set_movement([790, 60])
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
        pathing.set_movement([790, 60])
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


def temple_to_Gagazet():
    memory.main.click_to_control_3()
    checkpoint = 0
    while memory.main.get_map() != 279:
        if memory.main.user_control():
            if memory.main.get_map() == 223 and checkpoint < 18:
                checkpoint = 18

            elif checkpoint == 20:
                while memory.main.user_control():
                    pathing.set_movement([1261, -1238])
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_control()
                checkpoint += 1

            elif checkpoint == 24:
                logger.debug("Feather")
                while memory.main.user_control():
                    pathing.set_movement([1101, -940])
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.await_control()
                checkpoint += 1
            elif pathing.set_movement(LeaveRemiem.execute(checkpoint)) is True:
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
    touch_and_go()
    while not pathing.set_movement([69,-329]):
        pass
    while not pathing.set_movement([66,-234]):
        pass
    while not pathing.set_movement([66,-140]):
        pass
    
    logger.info("Nemesis change - Now on Defender X map. Rejoining normal path.")


def arena_purchase():
    #memory.main.click_to_control()

    #logger.debug("Straight forward to the guy")
    #FFXC.set_movement(0, 1)
    #memory.main.click_to_event()
    #FFXC.set_neutral()
    logger.debug("Now for dialog")
    memory.main.click_to_diag_progress(65)
    logger.debug("Select Sure")
    memory.main.wait_frames(15)
    xbox.tap_down()
    xbox.tap_b()
    memory.main.click_to_diag_progress(73)
    memory.main.wait_frames(15)
    xbox.tap_b()  # Let's see your weapons
    nemesis.menu.arena_purchase_1()
    while not memory.main.user_control():
        xbox.menu_a()
        xbox.tap_b()
        memory.main.wait_frames(15)

    # ---Done buying.
    memory.main.await_control()
    memory.main.wait_frames(2)
    FFXC.set_movement(0, -1)
    memory.main.await_event()  # Exit the arena map
    FFXC.set_neutral()
    memory.main.await_control()

def defender_x_nemesis():
    checkpoint = 0
    while memory.main.get_map() != 279:
        if memory.main.user_control():
            if checkpoint == 7 and area.gagazet.check_gems() < 2:
                checkpoint -= 2
            elif pathing.set_movement(CalmLands2.execute(checkpoint)) is True:
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                if area.gagazet.check_gems() < 2:
                    battle.main.calm_lands_gems()
                else:
                    battle.main.calm_lands_manip()
                memory.main.update_formation(Tidus, Yuna, Auron)
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()

    memory.main.await_control()
    area.gagazet.defender_x()

def back_to_chocobo_spawn():
    # Assumes Defender X was just defeated.
    memory.main.click_to_control()
    while not pathing.set_movement([67,-144]):
        pass
    while not pathing.set_movement([65,-256]):
        pass
    while not pathing.set_movement([57,-403]):
        pass
    while memory.main.get_map() == 279:
        pathing.set_movement([57,-550])
    memory.main.await_control()
    while not pathing.set_movement([1405,923]):
        pass
    memory.main.check_near_actors()
    pathing.approach_actor_by_id(20531)



def arena_purchase_with_chocobo():
    while memory.main.user_control():  # Back onto chocobo
        pathing.set_movement([1347, -69])
        xbox.tap_b()

    while not pathing.set_movement([1488, 778]):
        pass
    while not pathing.set_movement([1545, 1088]):
        pass
    while not memory.main.get_map() == 279:
        pathing.set_movement([1700, 1200])

    memory.main.update_formation(Tidus, Kimahri, Auron)
