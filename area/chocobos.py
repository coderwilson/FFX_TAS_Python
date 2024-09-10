import logging

import battle.main
import memory.main
from memory.main import check_near_actors
import pathing
import xbox
import math
from paths.nem import Race1, Race2, Race3, ToRemiem
from nemesis.arena_prep import (
    air_ship_destination,
    return_to_airship,
    unlock_omega
)
from nemesis.arena_battles import yojimbo_battle
from airship_pathing import air_ship_path
from area.sin import exit_cockpit
from paths.home import BikanelDesert
from menu import equip_armor
from save_sphere import touch_and_go
import tts
from players import CurrentPlayer
import reset
from json_ai_files.write_seed import write_custom_message

FFXC = xbox.controller_handle()
logger = logging.getLogger(__name__)
import vars
game_vars = vars.vars_handle()
import random
import load_game

try_fourth_race = False



def all_races():
    write_custom_message("Showcase!")
    air_ship_destination(dest_num=12)
    memory.main.await_control()

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
    attempts = 0
    while not dodger_complete:
        if attempts < 3:
            dodger_complete = choco_tame_2()
        else:
            dodger_complete = choco_tame_2_old()
        attempts += 1

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
    race_left = memory.main.get_actor_coords(0)[0]
    race_right = memory.main.get_actor_coords(0)[0]
    while memory.main.diag_progress_flag() not in [44, 74]:
        angle = memory.main.get_actor_angle(0)
        position = memory.main.get_actor_coords(0)
        
        # For troubleshooting:
        if position[0] < race_left:
            race_left = position[0]
        if position[0] > race_right:
            race_right = position[0]
        
        if position[0] < -100:
            min_angle = 1.1
            max_angle = 1.4
        elif position[0] > -60:
            min_angle = 1.6
            max_angle = 1.9
        else:
            min_angle = 1.4
            max_angle = 1.6
        
        
        if angle > max_angle:
            FFXC.set_value("d_pad", 8)
        elif angle < min_angle:
            FFXC.set_value("d_pad", 4)
        else:
            FFXC.set_value("d_pad", 0)
    
    
    FFXC.set_neutral()
    logger.info("Race end!")
    logger.debug(f"Race track extremes: [{race_left},{race_right}]")
    #memory.main.wait_frames(600)
    # [-216.0372772216797,54.41748046875]

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
    memory.main.click_to_diag_progress(40)
    balls = []
    for i in range(memory.main.get_actor_array_size()):
        if memory.main.get_actor_id(i) == 16425:
            logger.debug(f"Ball indices: {i}")
            balls.append(i)
    logger.debug(f"Tidus ID: {memory.main.get_actor_id(0)}")
    memory.main.click_to_diag_progress(43)
    mode = "straight"
    mode_last = "straight"
    last_dodge = "none"
    last_ball = 0
    min_angle = 1.4
    max_angle = 1.6
    angle = memory.main.get_actor_angle(0)
    near_end_reset = False
    while memory.main.diag_progress_flag() not in [44, 74]:
        position = memory.main.get_actor_coords(0)
        angle = memory.main.get_actor_angle(0)
        
        # V3 logic
        if position[1] > 100:  # Right at the end, force back to center.
            logger.debug("End - centralize")
            if position[0] < -110:
                mode = "hard_right"
            elif position[0] > -50:
                mode = "hard_left"
            elif position[0] > -80:
                mode = "shallow_left"
            else:
                mode = "shallow_right"
        elif position[1] < -600 or position[1] > -300:
            # The first bunch of dodges.
            if (
                memory.main.get_actor_coords(balls[1])[1] < position[1] + 100 and
                memory.main.get_actor_coords(balls[2])[1] > position[1]
            ):
                mode = "shallow_left"  # Between second and third
            elif (
                memory.main.get_actor_coords(balls[0])[1] < position[1] + 100 and
                memory.main.get_actor_coords(balls[1])[1] > position[1] + 100
            ):
                mode = "hard_left"  # Between first and second
            elif pathing.distance(balls[0]) < 550:
                mode = "shallow_right"  # Approaching first
            elif position[0] < -60:
                mode = "shallow_right"
            elif position[0] > -40:
                mode = "shallow_left"
            else:
                mode = "straight"
        else:
            # Middle section.
            if (
                memory.main.get_actor_coords(balls[1])[1] < position[1] and
                memory.main.get_actor_coords(balls[2])[1] > position[1]
            ):
                mode = "shallow_right"  # Between second and third
            elif (
                memory.main.get_actor_coords(balls[0])[1] < position[1] + 150 and
                memory.main.get_actor_coords(balls[1])[1] > position[1]
            ):
                mode = "hard_right"  # Between first and second
            elif pathing.distance(balls[0]) < 550:
                mode = "shallow_left"  # Approaching first
            elif position[0] < -150:
                mode = "shallow_right"
            elif position[0] > -130:
                mode = "shallow_left"
            else:
                mode = "straight"
        #logger.debug(mode)
        #logger.debug(f"{round(position[0],2):>8} | {section:>6} | {mode}")
        
        if mode_last != mode:
            logger.debug(f"Mode change: {mode}")
            mode_last = mode
        
        if mode == "hard_right":
            min_angle = 0.1
            max_angle = 0.4
        elif mode == "hard_left":
            min_angle = 2.4
            max_angle = 2.6
        elif mode == "shallow_right":
            min_angle = 1.0
            max_angle = 1.2
        elif mode == "shallow_left":
            min_angle = 1.9
            max_angle = 2.1
        #elif position[0] < -80:
        else:
            min_angle = 1.45
            max_angle = 1.65
        
        #logger.debug(f"{mode}: {min_angle},{max_angle}")
        
        if angle > max_angle:
            FFXC.set_value("d_pad", 0)
            FFXC.set_value("d_pad", 8)
        elif angle < min_angle:
            FFXC.set_value("d_pad", 0)
            FFXC.set_value("d_pad", 4)
        else:
            FFXC.set_value("d_pad", 0)
    
    
    logger.debug("Race two end. Let's see if we did it.")
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


def choco_tame_2_old():
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


def to_remiem(start_races:bool = True):
    memory.main.await_control()
    logger.info("Talking to chocobo lady")
    while memory.main.user_control():
        pathing.set_movement([-1565, 434])
        xbox.tap_b()
    FFXC.set_neutral()
    logger.info("Let me ride one!")
    memory.main.click_to_control()
    logger.info("Heading to Remiem")
    memory.main.set_game_speed(2)

    checkpoint = 0
    while checkpoint < 35:
        if memory.main.user_control():
            if memory.main.get_map() == 290 and checkpoint < 13:
                checkpoint = 13
            
            elif checkpoint == 24 and not start_races:
                checkpoint = 40

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
    
    if not start_races:
        while not pathing.set_movement([526,359]):
            pass
        xbox.set_neutral()
    
    memory.main.set_game_speed(0)


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
    for i in range(memory.main.get_actor_array_size()):
        if memory.main.get_actor_id(i) != 52685 and pathing.distance(i) < 60:
            logger.debug(f"Actor {i}: {memory.main.get_actor_id(i)}")
    pathing.approach_actor_by_id(20531)
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
    for i in range(memory.main.get_actor_array_size()):
        if memory.main.get_actor_id(i) != 52685 and pathing.distance(i) < 60:
            logger.debug(f"Actor {i}: {memory.main.get_actor_id(i)}")
    memory.main.click_to_control()
    pathing.approach_actor_by_id(20531)
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
    for i in range(memory.main.get_actor_array_size()):
        if memory.main.get_actor_id(i) != 52685 and pathing.distance(i) < 60:
            logger.debug(f"Actor {i}: {memory.main.get_actor_id(i)}")
    memory.main.click_to_control()
    pathing.approach_actor_by_id(20531)
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

def leave_temple():
    # Assumes we start standing next to the chocobo on the right.
    memory.main.await_control()
    memory.main.wait_frames(6)
    
    path = [
        [590,139],
        [495,271],
        [495,322]
    ]
    
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    return_to_airship()

def butterflies():
    air_ship_destination(dest_num=9)
    memory.main.click_to_control()
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    memory.main.set_game_speed(1)
    
    # Inside Rin travel agency
    while not pathing.set_movement([-3,-54]):
        pass
    while memory.main.user_control():
        pathing.set_movement([-3,-154])
    memory.main.click_to_control()
    
    # Lake Macalania
    path = [
        [79,-27],
        [129,0],
        [168,60]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    while memory.main.user_control():
        pathing.set_movement([210,120])
    
    # Spherimorph junction
    path = [
        [19,-32],
        [94,-59],
        [146,-86],
        [188,-101],
        [216,-118]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    while memory.main.user_control():
        pathing.set_movement([300,-120])
        
    
    # First Butterfly game
    path = [
        [-614,-43],
        [-605,24],
        [-605,119],
        [-605,130],  # Trigger game start.
        [-595,80],
        [-586,18],
        [-584,-2],  # North butterfly
        [-586,18],
        [-595,80],
        [-605,130],  # Back to starting point.
        [-621,157],  # Blue near start
        [-709,170],
        [-720,157],
        [-716,101],
        [-734,82],
        [-743,69],
        [-746,55],
        [-754,33],
        [-756,28],
        [-747,-18],
        [-717,-50],
        [-686,-59],
        [-669,-88],
        [-642,-109],
        [-614,-142],
        [-555,-159],
        [-536,-141],
        [-526,-108],
        [-504,-92],
        [-468,-56],
        [-453,-26],
        [-450,-8],
        [-450,11],  # This is where the chest will spawn.
        [-453,30],
        [-521,39],
        [-545,40],
        [-565,56],
        [-581,72],
        [-567,107],
        [-556,139],
        [-521,154],
        [-487,149],
        [-484,125],
        [-498,47],
        [-493,6],
        [-497,-14],  # Last butterfly.
        [-493,6],
        [-498,47],
        [-484,125],
        [-487,149],
        [-521,154],
        [-556,139],
        [-567,107],
        [-581,72],
        [-565,56],
        [-545,40],
        [-521,39],
        [-453,30],
        [-450,11]  # Ready to open chest.
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            logger.debug(path[i])
    
    # Open the chest!
    while memory.main.user_control():
        pathing.set_movement([-435,-8])
        xbox.tap_b()
    memory.main.click_to_control()
        
        
    # Path towards second butterfly game.
    path = [
        [-450,11],
        [-453,30],
        [-521,39],
        [-545,40],
        [-565,56],
        [-581,72],
        [-567,107],
        [-556,139],
        [-521,154],
        [-487,149],
        [-484,125],
        [-498,47],
        [-493,6],
        [-497,-14]  # Last butterfly.
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    while memory.main.user_control():
        pathing.set_movement([-400,-40])
    
    # Second butterfly game.
    path = [
        [-163,-162],
        [-152,-195],  # Trigger game start.
        [-145,-203],
        [-79,-213],
        [-56,-213],
        [-9,-192],
        [13,-172],
        [33,-180],
        [54,-197],
        [138,-165],
        [171,-138],
        [197,-90],
        [166,-29],
        [141,1],
        [121,-3],
        [73,42],
        [-19,72],
        [-62,71],
        [-86,70],
        [-131,20],
        [-161,8],
        [-187,33],
        [-213,63],
        [-227,69],
        [-181,112],
        [-146,127],
        [-109,125],
        [-86,90],
        [-82,74],
        [-61,58],
        [-51,14],
        [-35,-41],
        [1,-78],
        [36,-96],
        [60,-78],
        [66,-49],
        [64,-14],
        [63,80],
        [99,101],
        [119,111],  # The last butterfly.
        [99,101],  # Backtrack.
        [63,80],
        [64,-14],
        [66,-49],
        [60,-78],
        [36,-96],
        [1,-78],
        [-35,-41]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            logger.debug(path[i])
    # Open the chest!
    while memory.main.user_control():
        pathing.set_movement([-52,-30])
        xbox.tap_b()
    FFXC.set_neutral()
    #memory.main.wait_frames(150)
    memory.main.click_to_control()
        
    # Exit this area.
    path = [
        [-35,-41],
        [1,-78],
        [36,-96],
        [60,-78],
        [66,-49],
        [64,-14],
        [63,80],
        [99,101],
        [119,111]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    while memory.main.user_control():
        pathing.set_movement([300,140])
        
    # First Macalania screen.
    path = [
        [-130,257],
        [-89,177],
        [-110,64],
        [-102,26],
        [24,5],
        [18,114],
        [220,46]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    memory.main.set_game_speed(0)
    
# How about getting the celestial mirror?
def upgrade_mirror():
    # Assume we have already arrived near the family.
    while not pathing.set_movement([253,45]):
        pass
    memory.main.set_game_speed(1)
    while not pathing.set_movement([255,62]):
        pass
    while memory.main.user_control():  # Talk to lady
        pathing.set_movement([245,62])
        xbox.tap_b()
    memory.main.click_to_control()
    while not pathing.set_movement([267,110]):
        pass
    while memory.main.user_control():  # Screen change
        pathing.set_movement([70,400])
    memory.main.click_to_control()
    
    #Second screen
    while memory.main.user_control():
        pathing.set_movement([1,-20])
    memory.main.click_to_control()
    
    # Third screen
    while not pathing.set_movement([57,28]):
        pass
    while memory.main.user_control():
        pathing.set_movement([60,80])
        
    # Talk to husband
    while not pathing.set_movement([14,-15]):
        pass
    for i in range(memory.main.get_actor_array_size()):
        if memory.main.get_actor_id(i) != 52685:
            logger.debug(f"Actor {i}: {memory.main.get_actor_id(i)}")
    pathing.approach_actor_by_id(8238)
    FFXC.set_neutral()
    memory.main.click_to_control()
    while not pathing.set_movement([2,-20]):
        pass
    while memory.main.user_control():
        pathing.set_movement([0,-80])
    memory.main.click_to_control()
    
    # Third screen
    while not pathing.set_movement([33,-4]):
        pass
    while memory.main.user_control():
        pathing.set_movement([-20,-20])
    memory.main.click_to_control()
    memory.main.wait_frames(3)
        
    # Second screen
    while memory.main.user_control():
        pathing.set_movement([-200,-10])
    memory.main.click_to_control()
    
    # Family again
    while not pathing.set_movement([265,91]):
        pass
    while not pathing.set_movement([255,65]):
        pass
    while memory.main.user_control():  # Talk to lady (1)
        pathing.set_movement([245,62])
        xbox.tap_b()
    memory.main.click_to_control()
    while memory.main.user_control():  # Talk to lady (2)
        pathing.set_movement([245,62])
        xbox.tap_b()
    memory.main.click_to_control()
    
    # Up the glowing path.
    path = [
        [245,40],
        [183,29],
        [165,25],
        [62,-8],
        [-32,41]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    while memory.main.user_control():
        pathing.set_movement([-120,90])
    
    # On the glowing path.
    path = [
        [-95,8],
        [-112,-15],
        [-154,-126]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    for i in range(memory.main.get_actor_array_size()):
        if memory.main.get_actor_id(i) != 52685:
            logger.debug(f"Actor {i}: {memory.main.get_actor_id(i)} | {pathing.distance(i)}")
    pathing.approach_actor_by_id(8234)
    FFXC.set_neutral()
    
    # Talk to boy, create celestial mirror.
    while memory.main.diag_progress_flag() != 25:
        if memory.main.diag_skip_possible():
            logger.debug(f"Dialog progress: {memory.main.diag_progress_flag()}")
            xbox.tap_b()
    logger.debug(f"Dialog progress: {memory.main.diag_progress_flag()}")
    memory.main.wait_frames(15)
    xbox.tap_up()
    xbox.tap_b()
    
    memory.main.click_to_control()
    
    leave_mirror_area(to_airship=False)
    
    memory.main.set_game_speed(0)
    
def leave_mirror_area(to_airship:bool = False):
    # Leave this area.
    memory.main.set_game_speed(2)
    path = [
        [-112,-15],
        [-62,-3]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    while memory.main.user_control():
        pathing.set_movement([100,-50])
    memory.main.click_to_control()
    
    #Down to save sphere.
    path = [
        [63,-11],
        [181,30],
        [223,28]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    
    if to_airship:
        return_to_airship()

def spirit_lance():
    # Assumes we start from Macalania Woods first screen.
    #memory.main.set_game_speed(1)
    
    dodge_count = memory.main.l_strike_count()
    start_count = dodge_count
    
    memory.main.set_game_speed(2)
    # Towards thunder plains
    path = [
        [431,-4],
        [649,55]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    while memory.main.user_control():
        pathing.set_movement([900,55])
    memory.main.set_game_speed(0)
    
    logger.debug("Enter thunder plains north.")
    # Approach first cactuar stone
    path = [
        [65,695],
        [-57,475],
        [-142,478],
        [-161,485]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            if memory.main.dodge_lightning(dodge_count):
                dodge_count = memory.main.l_strike_count()
    FFXC.set_neutral()
    logger.debug("Waiting for cactuar stone to change status.")
    
    memory.main.set_game_speed(2)
    while not memory.main.cactuar_stone_4():
        logger.debug(f"Cactuar status: {memory.main.cactuar_stone_4()}")
    memory.main.set_game_speed(0)
    
    for i in range(2):
        while not pathing.set_movement([-165,577]):
            if memory.main.dodge_lightning(dodge_count):
                dodge_count = memory.main.l_strike_count()
        xbox.tap_x()
        logger.debug("Activating stone!")
        memory.main.click_to_control()
    #memory.main.set_game_speed(1)
    
    
    # South towards travel agency
    path = [
        [-166,428],
        [-144,367],
        [-103,277],
        [-45,190],
        [45,-25],
        [90,-191],
        [93,-328],
        [68,-598],  # Somewhat close to Dark Ixion
        [48,-727],
        [15,-887]  # Last tower, north section.
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            if memory.main.dodge_lightning(dodge_count):
                dodge_count = memory.main.l_strike_count()
                
    logger.debug("Ready to dodge.")
    #memory.main.set_game_speed(1)
    run_count = 0
    while dodge_count < start_count + 200:
        if run_count % 3 == 0:
            if pathing.set_movement([-95,-1000]):
                run_count = random.choice(range(0, 1000))
        elif run_count % 3 == 1:
            if pathing.set_movement([-137,-1020]):
                run_count = random.choice(range(0, 1000))
        else:
            if pathing.set_movement([-112,-971]):
                run_count = random.choice(range(0, 1000))
        if memory.main.dodge_lightning(dodge_count):
            dodge_count = memory.main.l_strike_count()
            logger.debug(f"Dodges left: {start_count + 200 - dodge_count}")
    memory.main.set_game_speed(0)
    
    
    # Wrap up North map
    path = [
        [-58,-1026],
        [-22,-1087]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            if memory.main.dodge_lightning(dodge_count):
                dodge_count = memory.main.l_strike_count()
            
    
    while memory.main.user_control():
        pathing.set_movement([1,-1500])
        if memory.main.dodge_lightning(dodge_count):
            dodge_count = memory.main.l_strike_count()
    FFXC.set_neutral()
    
    # Now south towards Kimahri's weapon
    path = [
        [137,950],
        [60,847],
        [45,680],
        [80,504],
        [72,476],
        [69,400],
        [114,336],
        [55,76],
        [53,36],
        [88,-54],
        [109,-125]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            if memory.main.dodge_lightning(dodge_count):
                dodge_count = memory.main.l_strike_count()
            
    for i in range(2):  # Trigger Kimahri's weapon event.
        while not pathing.set_movement([124,-154]):
            if memory.main.dodge_lightning(dodge_count):
                dodge_count = memory.main.l_strike_count()
        xbox.tap_x()
        memory.main.click_to_control()
    
    while not pathing.set_movement([101,-177]):
        if memory.main.dodge_lightning(dodge_count):
            dodge_count = memory.main.l_strike_count()
    
    logger.debug("Now to find and approach the chest/actor.")
    target_index = 0
    for i in range(memory.main.get_actor_array_size()):
        if memory.main.get_actor_id(i) == 20482 and pathing.distance(i) < 50:
            target_index = i
    logger.debug(f"Approaching chest: {target_index}")
    pathing.approach_actor_by_index(target_index)
    FFXC.set_neutral()
    logger.debug("Approach complete.")
    memory.main.click_to_control()
    logger.debug("Control re-gained.")
    
    # Back north towards agency.
    path = [
        [109,-125],
        [88,-54],
        [53,36],
        [55,76],
        [114,336],
        [69,400],
        [72,476],
        [80,504],
        [45,680],
        [45,887],
        [-10,1100]
    ]
    for i in range(len(path)):  # Reverses the previous path.
        logger.debug(f"Pathing to position {path[i]}")
        while not pathing.set_movement(path[i]):
            if memory.main.dodge_lightning(dodge_count):
                dodge_count = memory.main.l_strike_count()
    logger.debug("Map to map")
    while memory.main.get_map() == 140:
        pathing.set_movement([-50,1200])
        if memory.main.dodge_lightning(dodge_count):
            dodge_count = memory.main.l_strike_count()
    FFXC.set_neutral()
    
    # Back at agency, time to open chest.
    while not pathing.set_movement([-56,39]):
        pass
    
    for i in range(memory.main.get_actor_array_size()):
        if memory.main.get_actor_id(i) == 20482 and pathing.distance(i) < 30:
            target_index = i
    
    item_index = memory.main.get_item_slot(9)
    item_count = 0
    if item_index == 255:
        while memory.main.get_item_slot(9) == 255:
            logger.debug(f"A - Index: {item_index} | Count: {item_count}")
            pathing.approach_actor_by_index(target_index)
            FFXC.set_neutral()
            memory.main.click_to_control()
    else:
        item_count = memory.main.get_item_count_slot(item_index)
        while memory.main.get_item_count_slot(item_index) == item_count:
            logger.debug(f"B - Index: {item_index} | Count: {item_count}")
            pathing.approach_actor_by_index(target_index)
            FFXC.set_neutral()
            memory.main.click_to_control()
    
    logger.debug("Next one should be Lulu's item.")
    # Now we have all items except Lulu's celestial. One more time.
    pathing.approach_actor_by_index(target_index)
    FFXC.set_neutral()
    logger.debug("Got it. Let's get going!")
    memory.main.click_to_control()
    
    while not pathing.set_movement([-79,28]):
        pass
    while memory.main.get_map() == 256:
        pathing.set_movement([-100,35])  # Into the agency.
    FFXC.set_neutral()
    memory.main.click_to_control()
    while not pathing.set_movement([-32,-19]):
        pass
    return_to_airship()

def rusty_sword():
    air_ship_destination(dest_num=14)
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    memory.main.set_game_speed(2)
    
    # Ronso area
    path1 = [
        [-30,60],
        [20,-190],
        [13,-361],
        [-16,-456],
        [-124,-559],
        [-157,-627]
    ]
    for i in range(len(path1)):
        while not pathing.set_movement(path1[i]):
            pass
    while memory.main.user_control():
        pathing.set_movement([-190,-700])
    memory.main.await_control()
    
    # Defender X area
    path2 = [
        [-11,220],
        [-12,105],
        [10,95],
        [110,108],
        [120,122],
        [123,150],
        [91,156],
        [-85,160]
    ]
    for i in range(len(path2)):
        while not pathing.set_movement(path2[i]):
            pass
    while memory.main.user_control():
        pathing.set_movement([-200,160])
    memory.main.await_control()
    
    # Sword area
    path3 = [
        [-224,161],
        [-203,3],
        [-176,-13],
        [-82,-15],
        [-37,13],
        [4,69],
        [47,102],
        [151,102],
        [195,105]
    ]
    for i in range(len(path3)):
        while not pathing.set_movement(path3[i]):
            pass
    FFXC.set_neutral()
    
    memory.main.set_game_speed(0)
    
    for i in range(memory.main.get_actor_array_size()):
        if memory.main.get_actor_id(i) != 52685:
            logger.debug(f"Actor {i}: {memory.main.get_actor_id(i)}")
    pathing.approach_actor_by_id(20568)
    FFXC.set_neutral()
    #memory.main.wait_frames(300)
    memory.main.click_to_control()
    memory.main.set_game_speed(2)
    
    # Return trip from the rusty sword
    for i in range(len(path3)-1, -1, -1):
        while not pathing.set_movement(path3[i]):
            pass
    FFXC.set_neutral()
    while memory.main.user_control():
        pathing.set_movement([-224,400])
    memory.main.await_control()
    
    # Return trip, defender X area
    for i in range(len(path2)-2, -1, -1):
        while not pathing.set_movement(path2[i]):
            pass
    while not pathing.set_movement([20,350]):
        pass
    while memory.main.user_control():
        pathing.set_movement([20,600])
    memory.main.await_control()
    
    # Return trip, ronso area
    for i in range(len(path1)-1, -1, -1):
        while not pathing.set_movement(path1[i]):
            pass
    
    #return_to_airship()
    memory.main.set_game_speed(0)
    #memory.main.await_control()

def masamune():
    air_ship_destination(dest_num=5)
    memory.main.set_game_speed(2)
    
    # Aftermath map
    path = [
        [295,-408],
        [276,-416],
        [258,-426],
        [255,-448],
        [268,-468]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    while memory.main.user_control():
        pathing.set_movement([285,-488])
    memory.main.await_control()
    
    # To the lift
    path = [
        [312,506],
        [257,331],
        [134,148],
        [49,18],
        [32,-95],
        [16,-129],
        [-31,-155],
        [-118,-30],
        [-121,33]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            logger.debug(path[i])
    memory.main.set_game_speed(0)
    FFXC.set_neutral()
    xbox.tap_b()  # Lift
    xbox.tap_b()
    xbox.tap_b()
    memory.main.await_control()
    while not pathing.set_movement([-119,109]):  # Use rusty sword.
        pass
    FFXC.set_neutral()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    memory.main.click_to_control()
    while not pathing.set_movement([-130,165]):  # Unlock Masamune.
        pass
    FFXC.set_neutral()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    memory.main.click_to_control()
    
    while not pathing.set_movement([-114,51]):  # Back to the lift.
        pass
    FFXC.set_neutral()
    xbox.tap_b()  # Lift back down.
    xbox.tap_b()
    xbox.tap_b()
    memory.main.click_to_control()
    memory.main.set_game_speed(2)
    
    # Back towards High/Low roads.
    path = [
        [-50,-128],
        [-1,-210],
        [-18,-439],
        [-24,-587],
        [-64,-659],
        [-43,-729],
        [-43,-853]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    while memory.main.user_control():
        pathing.set_movement([-100,-1000])
    memory.main.await_control()
    
    # Chocobo???
    path = [
        [-56,176],
        [39,11]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    FFXC.set_neutral()
    for i in range(memory.main.get_actor_array_size()):
        if memory.main.get_actor_id(i) != 52685:
            logger.debug(f"Actor {i}: {memory.main.get_actor_id(i)}, {pathing.distance(i)}")
    FFXC.set_neutral()
    memory.main.click_to_control()
    
    # Down Low Road path
    path = [
        [-11,-51],
        [147,-191]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    while memory.main.user_control():
        pathing.set_movement([300,-340])
    memory.main.await_control()
    
    # Short run!
    path = [
        [661,282],
        [608,211],
        [354,120],
        [224,132]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    while memory.main.user_control():
        pathing.set_movement([100,120])
    memory.main.await_control()
    
    # Long run! All the way!
    path = [
        [3,-41],
        [5,-186],
        [188,-377],
        [185,-498],
        [66,-779],
        [26,-905],
        [20,-1048],
        [142,-1331],
        [113,-1530]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    
    FFXC.set_neutral()
    for i in range(memory.main.get_actor_array_size()):
        if memory.main.get_actor_id(i) != 52685:
            logger.debug(f"Actor {i}: {memory.main.get_actor_id(i)}, {pathing.distance(i)}")
    xbox.tap_x()
    xbox.tap_x()
    xbox.tap_x()
    
    while not pathing.set_movement([119,-1557]):
        pass
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    #pathing.approach_actor_by_id(20482)
    FFXC.set_neutral()
    memory.main.click_to_control()
    
    for i in range(len(path)-1, len(path)-4, -1):
        while not pathing.set_movement(path[i]):
            pass
    memory.main.click_to_control()
    
    memory.main.set_game_speed(0)
    return_to_airship()

def saturn_crest():
    #air_ship_destination(dest_num=14)
    memory.main.click_to_control()
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    memory.main.set_game_speed(2)
    
    #Teleporter pad.
    while not pathing.set_movement([54,107]):
        pass
    memory.main.click_to_event_temple(1)
    memory.main.click_to_control()
    
    # Up the mountain.
    path = [
        [-1145,452],
        [-1251,150],
        [-1339,-54]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    while memory.main.get_map() == 244:
        pathing.set_movement([-1350,-300])
    memory.main.click_to_control()
    
    # To the chest
    path = [
        [-448,-340],
        [-372,-325],
        [-179,-193],
        [7,-195],
        [167,-300],
        [181,-368],
        [190,-468]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    
    # Open chest
    for i in range(memory.main.get_actor_array_size()):
        if memory.main.get_actor_id(i) != 52685 and pathing.distance(i) < 150:
            logger.debug(f"Actor {i}: {memory.main.get_actor_id(i)}, {pathing.distance(i)}")
            if memory.main.get_actor_id(i) == 20482:
                pathing.approach_actor_by_index(i)
    FFXC.set_neutral()
    memory.main.click_to_control()
    
    while not pathing.set_movement([154,-601]):
        pass
    memory.main.set_game_speed(0)
    return_to_airship()
    
    
def moon_crest():  # Not used in current route
    air_ship_destination(dest_num=1)
    memory.main.click_to_control()
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    memory.main.set_game_speed(2)
    
    # To the chest, used both directions.
    path = [
        [-304,-432],
        [-252,-332],
        [-268,-125],
        [-311,29],
        [-384,63],
        [-439,40],
        [-446,-42]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    
    # Open chest
    for i in range(memory.main.get_actor_array_size()):
        if memory.main.get_actor_id(i) != 52685 and pathing.distance(i) < 150:
            logger.debug(f"Actor {i}: {memory.main.get_actor_id(i)}, {pathing.distance(i)}")
            if memory.main.get_actor_id(i) == 20482:
                pathing.approach_actor_by_index(i)
    FFXC.set_neutral()
    memory.main.click_to_control()
    
    # Return trip
    for i in range(len(path)-1, -1, -1):
        while not pathing.set_movement(path[i]):
            pass
    
    memory.main.set_game_speed(0)
    return_to_airship()

def belgemine():  # Not yet working.
    # Assumes airship start.
    air_ship_destination(dest_num=12)
    to_remiem(start_races=False)
    
    # First battle, Valefor
    memory.main.click_to_event_temple(0)  # Just to go north.
    battle.main.belgemine()
    
    for i in range(memory.main.get_actor_array_size()):
        if memory.main.get_actor_id(i) != 52685 and pathing.distance(i) < 200:
            logger.debug(f"Actor {i}: {memory.main.get_actor_id(i)}, {pathing.distance(i)}")
    
    for i in range(4):
        while memory.main.user_control():
            pathing.set_movement([-10,0])
        if i == 3:
            battle.main.belgemine(use_aeon=3)
        else:
            battle.main.belgemine()
        
    # To the girls
    path = [
        [-61,-61],
        [11,-78],
        [105,-26],
        [145,-4]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    memory.main.click_to_event_temple(0)  # Just to go north.

def desert_path(start:int=4, end:int=55):
    # Let's borrow the movement from the run.
    checkpoint = start
    logger.debug(f"Starting checkpoint:  {checkpoint}")
    if start < end:
        # Forward movement!
        while checkpoint < end:
            if memory.main.user_control():
                # Map changes
                if not checkpoint in BikanelDesert.checkpoint_coordiantes.keys():
                    checkpoint += 1
                if checkpoint in [8,9,10] and memory.main.get_map() == 129:
                    pathing.set_movement([250,-390])
                    checkpoint = 10
                elif checkpoint == 1 and len(memory.main.get_order_seven()) > 4:
                    checkpoint += 1
                elif checkpoint < 14 and memory.main.get_map() == 136:
                    checkpoint = 14
                elif checkpoint < 39 and memory.main.get_map() == 137:
                    checkpoint = 39
                elif checkpoint < 50 and memory.main.get_map() == 138:
                    checkpoint = 50

                # General pathing
                elif memory.main.user_control():
                    if pathing.set_movement(BikanelDesert.execute(checkpoint)):
                        checkpoint += 1
                        logger.debug(f"Checkpoint {checkpoint}")
    else:
        while checkpoint > end:
            if memory.main.user_control():
                # Map changes
                if not checkpoint in BikanelDesert.checkpoint_coordiantes.keys():
                    checkpoint -= 1
                if checkpoint == 15:
                    memory.main.click_to_event_temple(4)
                    checkpoint = 7
                elif checkpoint in [36,37,38] and memory.main.get_map() == 137:
                    pathing.set_movement([500,-900])
                    checkpoint = 36
                elif checkpoint <= 49 and memory.main.get_map() == 138:
                    pathing.set_movement([-625,-450])
                    checkpoint = 48

                # General pathing
                elif memory.main.user_control():
                    if pathing.set_movement(BikanelDesert.execute(checkpoint)):
                        checkpoint -= 1
                        logger.debug(f"Checkpoint {checkpoint}")
    

def divert_to_stone_south(return_north:bool = False,last_path:bool = False):
    while not pathing.set_movement([185,650]):
        pass
    while memory.main.user_control():
        pathing.set_movement([250,900])
    memory.main.await_control()
    while not pathing.set_movement([349,-346]):
        pass
        
    # Approach stone
    #speed_check = memory.main.get_game_speed()
    #memory.main.set_game_speed(0)
    while memory.main.user_control():
        pathing.set_movement([350,-340])
        xbox.tap_b()
    memory.main.click_to_control()
    #memory.main.set_game_speed(speed_check)
    
    if last_path:
        return
    elif return_north:
        while not pathing.set_movement([45,-297]):
            pass
        while not pathing.set_movement([-80,-210]):
            pass
    else:
        while not pathing.set_movement([-34,-892]):
            pass
        while not pathing.set_movement([-82,-974]):
            pass
        memory.main.click_to_event_temple(5)
        
def divert_to_stone_north(return_north:bool = True):
    # Assumes we've gotten to the map with the two directions sign.
    while not pathing.set_movement([-80,-210]):
        pass
    while not pathing.set_movement([45,-297]):
        pass
    while not pathing.set_movement([349,-346]):
        pass
    #speed_check = memory.main.get_game_speed()
    #memory.main.set_game_speed(0)
    while memory.main.user_control():
        pathing.set_movement([350,-340])
        xbox.tap_b()
    memory.main.click_to_control()
    #memory.main.set_game_speed(speed_check)
    
    if return_north:
        while not pathing.set_movement([45,-297]):
            pass
        while not pathing.set_movement([-80,-210]):
            pass
    else:
        while not pathing.set_movement([-34,-892]):
            pass
        while not pathing.set_movement([-82,-974]):
            pass
        memory.main.click_to_event_temple(5)

def engage_cactuar(cactuar_num:int = 99):
    speed_check = memory.main.get_game_speed()
    memory.main.set_game_speed(0)
    if cactuar_num == 6:
        touch_and_go()
    elif cactuar_num == 7:
        pathing.approach_actor_by_id(20482)
    elif cactuar_num == 9:
        while memory.main.user_control():
            pathing.set_movement([7,-200])
    elif not cactuar_num in [3,10]:
        pathing.approach_actor_by_id(4304)
    memory.main.click_to_control()
    while not memory.main.diag_progress_flag() in [64, 77, 78, 92, 95, 106]:
        if memory.main.user_control():
            FFXC.set_movement(0,-1)
        else:
            logger.debug(f"Progress flag: {memory.main.diag_progress_flag()}")
            FFXC.set_neutral()
            xbox.tap_b()
    logger.debug(f"Final Progress flag: {memory.main.diag_progress_flag()}")
    memory.main.click_to_control()
    memory.main.set_game_speed(speed_check)

def cactuars():
    # Assumes airship start.
    air_ship_destination(dest_num=10)
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    memory.main.set_game_speed(2)
    
    desert_path(start=4, end=40)
    
    divert_to_stone_south()
    desert_path(start=39, end=3)
    while not pathing.set_movement([-43,-98]):
        pass
    check_near_actors(wait_results=False)
    engage_cactuar()  # First cactuar
    
    desert_path(start=5, end=40)
    divert_to_stone_south()
    desert_path(start=39, end=34)
    while not pathing.set_movement([412,532]):
        pass
    check_near_actors(wait_results=False)
    engage_cactuar()  # Second cactuar
    desert_path(start=35, end=40)
    divert_to_stone_south(return_north=True)
    while not pathing.set_movement([-280,-90]):
        pass
    memory.main.click_to_event_temple(0)
    engage_cactuar(cactuar_num=3)  # Third cactuar (number guys)
    divert_to_stone_north()
    desert_path(start=50, end=47)
    while not pathing.set_movement([-622,437]):
        pass
    engage_cactuar()  # 4 and 5, brothers.
    desert_path(start=48, end=51)
    divert_to_stone_north(return_north=False)
    desert_path(start=36, end=24)
    engage_cactuar(cactuar_num=6)  # sixth cactuar (save sphere guys)
    desert_path(start=25, end=40)
    divert_to_stone_south()
    
    # Getting to seven goes perpendicular to the rails.
    path = [
        [116,185],
        [-372,-87],
        [-777,-96],
        [-778,-94]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            logger.debug(f"{i}: {path[i]}")
    check_near_actors(False)
    engage_cactuar(cactuar_num=7)
    
    for i in range(len(path)-1,0,-1):
        while not pathing.set_movement(path[i]):
            pass
    divert_to_stone_south()
    
    divert_to_stone_south(return_north=True)
    
    # For 8, grabbing the mercury crest
    logger.debug("Break out for mercury crest.")
    path = [
        [-190,103],
        [-237,123],
        [-293,116],
        [-352,83],
        [-421,94]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            logger.debug(f"{i}: {path[i]}")
    check_near_actors(False)
    pathing.approach_actor_by_id(20482)
    memory.main.click_to_control()
    
    # Then to the actual guy.
    path = [
        [-352,83],
        [-293,116],
        [-237,123],
        [-221,193],
        [-183,304]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    engage_cactuar()
    divert_to_stone_north(return_north=False)
    
    
    # Airship guy.
    desert_path(start=39, end=2)
    memory.main.set_game_speed(0)
    return_to_airship()
    FFXC.set_neutral()
    
def cactuars_finish():
    logger.debug("== Path to the upper deck.")
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    exit_cockpit()
    air_ship_path(1)
    FFXC.set_neutral()
    logger.debug("== Now on the deck!!!")
    # tts.message("Mark")
    memory.main.wait_frames(60)
    memory.main.click_to_control()
    #memory.main.wait_frames(900)
    engage_cactuar(cactuar_num=9)
    memory.main.click_to_control()
    while memory.main.user_control():
        pathing.set_movement([7,200])
    logger.debug("Path back down. (1)")
    memory.main.click_to_control()
    
    while not pathing.set_movement([1,-38]):
        pass
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    memory.main.wait_frames(30)
    memory.main.click_to_control()
    while not pathing.set_movement([-1,-60]):
        pass
    memory.main.click_to_event_temple(4)
    memory.main.click_to_control()
    #while not pathing.set_movement([-30,-19]):
    #    pass
    #while not pathing.set_movement([-35,-75]):
    #    pass
    logger.debug("Path back down. (2)")
    air_ship_path(2, checkpoint=25)
    
    air_ship_destination(dest_num=10)
    memory.main.await_control()
    
    memory.main.set_game_speed(2)
    desert_path(start=4, end=40)
    divert_to_stone_south(last_path=True)
    
    engage_cactuar(cactuar_num=10)  # Last one starts automatically.
    while memory.main.user_control():  # Straight back to the stone.
        pathing.set_movement([350,-340])
        xbox.tap_b()
    memory.main.click_to_control()  # Last time on the stone.
    
    # Down into the canyon.
    path = [
        [45,-297],
        [-80,-210],
        [-1,-152],
        [101,-103],
        [209,-9],
        [379,-8],
        [400,14]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    check_near_actors(False)
    pathing.approach_actor_by_id(20482)
    memory.main.click_to_control()
    
    for i in range(len(path)-1, 2, -1):
        while not pathing.set_movement(path[i]):
            pass
    
    desert_path(start=50, end=3)
    memory.main.set_game_speed(0)
    return_to_airship()
    
    FFXC.set_neutral()

def onion_knight():
    unlock_omega(x=14,y=-60)  # Baaj temple
    air_ship_destination(1)
    memory.main.await_control()
    
    path = [
        [224,-171],
        [181,-138],
        [154,-118],
        [114,-87],
        [77,-57],
        [17,-15]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    memory.main.click_to_event_temple(0)  # Into the water.
    memory.main.click_to_control()  # For dialog.
    
    # Must fight Geo first.
    while memory.main.user_control():
        pathing.set_movement([20,300])
    FFXC.set_neutral()
    xbox.click_to_battle()
    while memory.main.battle_active():
        if CurrentPlayer().is_turn():
            CurrentPlayer().attack()
    memory.main.click_to_control()
    
    # Now to get chest.
    FFXC.set_value("btn_a", 1)
    while not pathing.set_movement([14,-93]):
        pass
    while not pathing.set_movement([67,-143]):
        pass
    while not pathing.set_movement([54,-140]):
        pass
    FFXC.set_movement(0,0)
    FFXC.set_value("btn_a", 0)
    while memory.main.user_control():
        xbox.tap_b()
    FFXC.set_neutral()
    logger.debug("Chest triggered.")
    memory.main.click_to_control()
    logger.debug("Chest complete.")
    
    xbox.menu_x()
    xbox.menu_x()
    xbox.menu_x()
    xbox.menu_x()
    xbox.menu_x()
    xbox.menu_x()
    xbox.menu_x()
    logger.debug("Should be surfacing now.")
    
    # Back to sphere.
    for i in range(len(path)-1, -1, -1):
        while not pathing.set_movement(path[i]):
            pass
    
    return_to_airship()
    return 1
    
def godhand(baaj:int=0):
    # Assumes Baaj already unlocked.
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
        
    # Similar logic to airship 'search' in arena_prep
    while memory.main.get_coords()[0] < -257:
        pathing.set_movement([-258, 345])
    while memory.main.get_map() not in [382, 999]:
        if memory.main.user_control():
            pathing.set_movement([-251, 340])
        else:
            FFXC.set_neutral()
        if memory.main.diag_progress_flag() == 4:
            xbox.menu_a()
        else:
            xbox.menu_b()
    while memory.main.diag_progress_flag() != 2:
        xbox.menu_down()
    xbox.menu_b()
    while memory.main.diag_progress_flag() != 7:
        pass
    
    memory.main.wait_frames(30)
    xbox.menu_b()
    memory.main.wait_frames(90)
    xbox.name_aeon("GODHAND")
    memory.main.wait_frames(10)
    xbox.tap_start()
    memory.main.wait_frames(30)
    xbox.menu_b()
    memory.main.wait_frames(30)
    xbox.menu_a()
    xbox.menu_b()
    memory.main.wait_frames(30)
    xbox.menu_a()
    xbox.menu_b()
    memory.main.wait_frames(90)
    air_ship_destination(5+baaj)
    
    path = [
        [-29,-98],
        [-25,1],
        [-30,70],
        [-25,158],
        [-38,175],
        [-80,197],
        [-137,216],
        [-161,265]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
            
    check_near_actors(False)
    target_index = 0
    for i in range(memory.main.get_actor_array_size()):
        if memory.main.get_actor_id(i) == 20482 and pathing.distance(i) < 50:
            target_index = i
    logger.debug(f"Approaching chest: {target_index}")
    pathing.approach_actor_by_index(target_index)
    memory.main.click_to_control()
    
    for i in range(len(path)-1,-1,-1):
        while not pathing.set_movement(path[i]):
            pass
    
    return_to_airship()
    return 1

def check_actors_count(wait_results:bool = False):
    actors = {}
    for i in range(memory.main.get_actor_array_size()):
        actor_id = memory.main.get_actor_id(i)
        if actor_id != 52685:
            if actor_id in actors.keys():
                actors[actor_id] += 1
            else:
                actors[actor_id] = 1
    logger.debug("=====  Actor counts  =====")
    for key in actors.keys():
        logger.debug(f"{key:>6} : {actors[key]}")
    logger.debug("==========================")
    
    if wait_results:
        FFXC.set_neutral()
        memory.main.wait_frames(300)

def get_actor_indices(actor_id:int) -> []:
    actors = []
    for i in range(memory.main.get_actor_array_size()):
        if memory.main.get_actor_id(i) == actor_id:
            actors.append(i)
    return actors


def sun_sigil(godhand:int = 1, baaj:int = 1):
    # Assumes airship start.
    
    air_ship_destination(dest_num=(12+godhand+baaj))
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    #memory.main.set_game_speed(2)
    
    # Dialog with chocobo lady
    while not pathing.set_movement([-637, -246]):
        pass
    pathing.approach_actor_by_id(actor_id=20531)
    FFXC.set_neutral()
    memory.main.click_to_diag_progress(302)
    memory.main.wait_frames(30)
    xbox.menu_down()
    xbox.menu_down()
    xbox.tap_b()
    memory.main.click_to_diag_progress(3)
    memory.main.wait_frames(30)
    xbox.menu_up()
    xbox.tap_b()
    
    catcher_complete = False
    while not catcher_complete:
        catcher_complete = choco_tame_4()

    logger.debug("Catcher Chocobo complete. Let's get our prize!")
    memory.main.await_control()
    memory.main.set_game_speed(2)
    #pathing.approach_actor_by_id(actor_id=20531)
    #FFXC.set_neutral()
    #memory.main.click_to_diag_progress(302)
    #memory.main.wait_frames(30)
    #xbox.menu_b()
    #memory.main.click_to_control()
    
    path = [
        [-560,-162],
        [-500,7],
        [-915,331], # In between cracks in the ground
        [-923,372], # In between cracks in the ground
        [-1109,659],
        [-1115,726],
        [-1053,735],
        [-862,730],
        [-858,722]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    FFXC.set_neutral()
    memory.main.set_game_speed(0)
    xbox.menu_b()  # Use celestial mirror
    xbox.menu_b()  # Use celestial mirror
    memory.main.click_to_event()
    xbox.menu_b()  # Use celestial mirror
    
    memory.main.click_to_control()
    memory.main.set_game_speed(2)
    for i in range(len(path)-2,-1,-1):
        while not pathing.set_movement(path[i]):
            pass
    while not pathing.set_movement([-620,-137]):
        pass
    while not pathing.set_movement([-656,-64]):
        pass
    memory.main.set_game_speed(0)
    return_to_airship()
    

def closest_balloon(balloons):
    
    closest = 999
    distance = 1000

    for i in range(len(balloons)):
        dist = pathing.distance(balloons[i])
        pos = memory.main.get_actor_coords(balloons[i])
        player = memory.main.get_actor_coords(0)
        if dist < distance:
            if (
                player[1] < -1400 and
                player[0] > -750 and
                pos[1] < -1400 and 
                pos[0] < player[0] 
            ):
                # Before the turn
                closest = balloons[i]
                distance = dist
            elif (
                player[1] > -300 and
                pos[1] > player[1] # Balloon north of player
            ):
                # The final stretch
                closest = balloons[i]
                distance = dist
            elif (
                player[1] > -1400 and
                player[1] < (-0.748*player[0]) + 665.82 and
                pos[1] >= -1400 and 
                (-0.748*pos[0]) < (-0.748*player[0]) # Balloon northeast of player.
            ):
                # Between the turn and the final stretch.
                closest = balloons[i]
                distance = dist
    #logger.warning(f"Balloon: {closest:>3} | Distance: {round(distance):>4}")
    return closest

def adjust_for_birds(birds, desired_angle) -> float:
    dodge = False
    closest_bird = 0
    dist_check = 999
    for i in range(len(birds)):
        dist = pathing.distance(birds[i])
        bird_forward = memory.main.get_actor_coords(birds[i])[0]
        player_forward = memory.main.get_actor_coords(0)[0]
        if dist < dist_check:
            if (
                dist < 300 and
                (-0.5*bird_forward) < (-0.5*player_forward)
                # Bird in front of us and close enough to justify dodge.
            ):
                dist_check = dist
                closest_bird = birds[i]
                dodge = True
    if dodge:
        # Positive is dodging left, negative is right.
        #if memory.main.get_actor_coords(0)[1] > 300:
        #    pass  # Do not dodge at the end.
        
        inverse_angle = memory.main.get_actor_angle(closest_bird)# + 3.14159
        player_angle = memory.main.get_actor_angle(0)
        #logger.debug(f"P: {round(player_angle,2)} | I: {round(inverse_angle,2)}")
        '''
        diff = min(abs(inverse_angle - player_angle), abs(player_angle - inverse_angle))
        if diff < 0.7:
            if inverse_angle > player_angle:
                desired_angle = inverse_angle - 0.6
            else:
                desired_angle = inverse_angle + 0.6
        '''
        if memory.main.get_actor_coords(0)[1] > -400:
            if memory.main.get_actor_angle(0) > 1.2:
                desired_angle += 0.6
            else:
                desired_angle -= 0.6
        else:
            if memory.main.get_actor_angle(0) > 0.6:
                desired_angle += 0.9
            else:
                desired_angle -= 0.9
        
    return desired_angle

def balloon_turns(angle, desired_angle, last_button) -> int:
    # Maybe need some logic if abs(delta) greater than a threshold.
    if abs(desired_angle - angle) > 3.14159:
        desired_angle -= 3.14
        if desired_angle < -3.142:
            desired_angle += 6.28
        angle -= 3.14
        if angle < -3.142:
            angle += 6.28

    if abs(desired_angle - angle) < 0.2:
        if last_button != 0:
            #logger.debug(f"Straight: {round(desired_angle,2)} | {round(angle,2)}")
            last_button = 0
        FFXC.set_value("d_pad", 0)
    elif desired_angle > angle:
        if last_button != 1:
            #logger.warning(f"Left: {round(desired_angle,2)} | {round(angle,2)}")
            last_button = 1
        FFXC.set_value("d_pad", 0)
        FFXC.set_value("d_pad", 4)
    else:
        if last_button != 2:
            #logger.warning(f"Right: {round(desired_angle,2)} | {round(angle,2)}")
            last_button = 2
        FFXC.set_value("d_pad", 0)
        FFXC.set_value("d_pad", 8)
    return last_button

def get_all_angles():
    actors = {}
    for i in range(memory.main.get_actor_array_size()):
        actor_id = memory.main.get_actor_id(i)
        if not actor_id in [52685,0,1]:
            actor_angle = memory.main.get_actor_angle(i)
            actors[i] = actor_angle
    return actors

def choco_tame_4():
    logger.debug("START - CATCHER CHOCOBO")
    angles = get_all_angles()
    logger.debug(angles)
    while not memory.main.diag_progress_flag() == 40:
        #for key in angles.keys():
        #    if angles[key] != get_all_angles()[key]:
        #        logger.debug(f"Angle change: {key} - {round(angles[key],2)}")
        #        angles = get_all_angles()
        xbox.tap_b()
    
    #memory.main.click_to_diag_progress(40)
    check_actors_count(False)
    balloons = get_actor_indices(20579)
    birds = get_actor_indices(20503)
    logger.debug("==== Balloons ahead check: ====")
    for i in range(len(balloons)):
        if memory.main.get_actor_coords(balloons[i])[1] < -1450:
            dist = pathing.distance(balloons[i])
            logger.debug(f"{balloons[i]:>4} | {round(dist,2):>10}")
    logger.debug("===============================")
    
    memory.main.click_to_diag_progress(43)
    last_balloon = 999
    angle = memory.main.get_actor_angle(0)
    position = memory.main.get_actor_coords(0)
    balloon = 999
    last_button = 0
    
    # Race in two parts, before and after the turn. This section for before.
    while position[1] < -1450:
        angle = memory.main.get_actor_angle(0)
        position = memory.main.get_actor_coords(0)
        balloon = closest_balloon(balloons)
        if balloon != last_balloon and balloon != 999:
            logger.debug(f"Targetting new balloon: {balloon}")
            last_balloon = balloon
        
        if position[0] < -650:
            if position[1] > -1510:
                b_pos = [-600,-1434]
            elif position[1] > -1570:
                b_pos = [-807,-1500]
            elif position[1] > -1620:
                b_pos = [-765,-1560]
            else:
                b_pos = [-655,-1618]
        else:
            if balloon == 999:
                b_pos = [-655,-1618]
            elif memory.main.distance(balloon,2) < memory.main.distance(balloon,0):
                b_pos = [-655,-1618]
            else:
                b_pos = memory.main.get_actor_coords(balloon)
        delta_x = b_pos[0] - position[0]
        delta_y = b_pos[1] - position[1]
        desired_angle = math.atan2(delta_y, delta_x)
        
        last_button= balloon_turns(
            angle=angle, 
            desired_angle=desired_angle,
            last_button=last_button
        )
        
        # Clean up balloons as we get them.
        try:
            if pathing.distance(balloon) < 15:
                balloons.remove(balloon)
        except:
            pass

    
    # Logic for after the turn.
    while memory.main.diag_progress_flag() not in [44, 67]:
        birds = get_actor_indices(20503)
        angle = memory.main.get_actor_angle(0)
        position = memory.main.get_actor_coords(0)
        balloon = closest_balloon(balloons)
        if balloon != last_balloon and balloon != 999:
            logger.debug(f"Targetting new balloon: {balloon}")
            last_balloon = balloon
        if balloon == 999:
            if position[1] < -1470:
                b_pos = [-807,-1465]
            else:
                b_pos = [1490,900]
        else:
            b_pos = memory.main.get_actor_coords(balloon)
        
        delta_x = b_pos[0] - position[0]
        delta_y = b_pos[1] - position[1]
        desired_angle = math.atan2(delta_y, delta_x)
        #logger.debug(position[1])
        
        # Change target position for nearest bird.
        #logger.debug(f"{round(memory.main.distance(balloon)):>6}")
        if memory.main.distance(balloon) > 90:
            desired_angle = adjust_for_birds(birds, desired_angle)
        
        last_button= balloon_turns(
            angle=angle, 
            desired_angle=desired_angle,
            last_button=last_button
        )
        
        # Clean up balloons as we get them.
        try:
            if pathing.distance(balloon) < 15:
                balloons.remove(balloon)
        except:
            pass

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


def venus_crest(godhand:int = 1, baaj:int = 1):
    # Assumes airship start.
    
    air_ship_destination(dest_num=(7+godhand+baaj))
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    #memory.main.set_game_speed(2)
    
    
    path = [
        [-17,-21],
        [1,-44],
        [1,-100],  # Forward, leave inn
        [60,30],  # Back, into inn
        #[32,11],
        [13,-20],
        [-17,1],
        [-25,92],
        [-50,104],
        [-81,52],
        [-88,18],
        [-66,-14],
        [-13,9],
        [34,27],
        [120,94],
        [150,130],  # Forward, Guado Main area to crooked map.
        [5,-100],  # Back, leaving crooked map
        [5,-1],
        [-1,40],
        [4,142],
        [4,300],  # Forward, crooked map to ramp map
        [-30,-300],  # Back, leaving ramp map
        [-15,-128],
        [2,-47],
        [2,300],  # Forward, into farplane
        [5,200],  # Back, out of farplane
        [5,41],
        [62,-34]
    ]
    last_map = memory.main.get_map()
    i_update = 0
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            if i < i_update:
                break
            elif memory.main.get_map() != last_map:
                last_map = memory.main.get_map()
                i_update = i+2
                FFXC.set_neutral()
                memory.main.click_to_control()
    
    check_near_actors(False)
    pathing.approach_actor_by_id(20482)
    memory.main.click_to_control()
    i_update = len(path)
    
    for i in range(len(path)-1,-1,-1):
        while not pathing.set_movement(path[i]):
            if i > i_update:
                break
            elif memory.main.get_map() != last_map:
                last_map = memory.main.get_map()
                i_update = i-2
                FFXC.set_neutral()
                memory.main.click_to_control()
    
    #memory.main.set_game_speed(0)
    return_to_airship()


def sun_crest(godhand:int = 1, baaj:int = 1):
    # Assumes Yuna has overdrive.
    air_ship_destination(dest_num=(15+godhand+baaj))
    memory.main.update_formation(0, 3, 5)
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    
    
    while not pathing.set_movement([114,32]):
        pass
    FFXC.set_neutral()
    memory.main.wait_frames(15)
    xbox.menu_left()
    xbox.menu_b()
    memory.main.wait_frames(10)
    memory.main.click_to_control()
    
    while not pathing.set_movement([6,1644]):
        pass
    FFXC.set_neutral()
    thismap = memory.main.get_map()
    while memory.main.get_map() == thismap:
        memory.main.wait_frames(15)
        xbox.menu_up()
        xbox.menu_b()
    memory.main.wait_frames(10)
    memory.main.click_to_control()
    
    while not pathing.set_movement([-1,38]):
        pass
    while not pathing.set_movement([3,356]):
        pass
    while memory.main.user_control():
        pathing.set_movement([1,600])
    memory.main.click_to_control()
    
    # Trials room
    path = [
        [94,-68],
        [89,-47],
        [91,7],
        [96,21],
        [96,32],
        [77,54],
        [2,68],
        [-21,21],
        [-41,-15],
        [-44,-40],
        [-66,-59],
        [-79,-48]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            if path[i] == [2,68]:
                FFXC.set_movement(-1,1)
                memory.main.wait_frames(30)
                break
    memory.main.click_to_event_temple(0)
    memory.main.await_control()
    
    # Room with save sphere
    while pathing.set_movement([-6,10]):
        pass
    while memory.main.user_control():
        pathing.set_movement([-2,60])
    
    success = False
    while not success:
        # Room with 'You're being selfish' scene
        while memory.main.get_map() != 319:
            pass
        memory.main.wait_frames(60)
        memory.main.await_control()
        while not pathing.set_movement([0,45]):
            pass
        while memory.main.user_control():
            pathing.set_movement([0,200])
    
        xbox.click_to_battle()
        memory.main.set_game_speed(2)
        cur_gil = min(memory.main.get_gil_value(),990000)
        cur_gil = memory.main.get_gil_value()
        success = yojimbo_battle(flee_available=False, needed_amount=cur_gil)
        logger.debug(f"Yojimbo results: {success}")
        if not success:
            reset.reset_to_main_menu()
            #xbox.menu_b()
            area.dream_zan.new_game(gamestate="reload_autosave")
            load_game.load_save_num(0)
    
    memory.main.await_control()
    memory.main.update_formation(0, 4, 6)
    while not pathing.set_movement([-36,-22]):
        pass
    while not pathing.set_movement([-29,94]):
        pass
    while memory.main.get_actor_coords(0)[1] > 50:
        FFXC.set_movement(1,0)
    while not pathing.set_movement([-59,-146]):
        pass
    while not pathing.set_movement([-36,-22]):
        pass
    while not pathing.set_movement([-45,94]):
        pass
    
    # Open chest
    check_near_actors(False)
    pathing.approach_actor_by_id(20482)
    memory.main.click_to_control()
    
    while not pathing.set_movement([-36,-22]):
        pass
    while not pathing.set_movement([-13,-173]):
        pass
    while memory.main.user_control():
        pathing.set_movement([-10,-300])
    memory.main.await_control()
    while memory.main.user_control():
        pathing.set_movement([-3,-150])
    memory.main.await_control()
    
    # Save sphere screen
    while not pathing.set_movement([-1,-51]):
        pass
    while not pathing.set_movement([-1,-163]):
        pass
    
    memory.main.set_game_speed(0)
    return_to_airship()

def upgrade_celestials(godhand:int=1, baaj:int=1, Yuna:bool=False, Wakka:bool=False):
    air_ship_destination(dest_num=(9+godhand+baaj))
    memory.main.await_control()
    
    # Inside Rin travel agency
    while not pathing.set_movement([-3,-54]):
        pass
    while memory.main.user_control():
        pathing.set_movement([-3,-154])
    memory.main.click_to_control()
    
    # Lake Macalania
    path = [
        [79,-27],
        [129,0],
        [168,60]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    while memory.main.user_control():
        pathing.set_movement([210,120])
    
    # Spherimorph junction
    path = [
        [19,-32],
        [94,-59],
        [168,-6]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    while memory.main.user_control():
        pathing.set_movement([300,60])
        
    # Shining path north
    path = [
        [-900,185],
        [-872,178],
        [-633,-59]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    while memory.main.user_control():
        FFXC.set_movement(-1,1)
        
    # Shining path south
    path = [
        [-105,18],
        [-102,-4],
        [-166,-140]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    while memory.main.user_control():
        FFXC.set_movement(0,1)
    FFXC.set_neutral()
    click_to_diag_progress(33)
    
    for i in range(7):
        if i == 1 and not Yuna:
            pass
        elif i == 4 and not Wakka:
            pass
        else:
            upgrade_engage(i)
    leave_mirror_area(True)
    

def upgrade_engage(menu_id:int):
    for i in range(2):
        memory.main.wait_frames(15)
        while memory.main.save_menu_cursor() != menu_id:
            xbox.menu_down()
        xbox.menu_b()
        xbox.menu_b()
        if i % 2 == 1 and menu_id==7:
            click_to_diag_progress(62)
            memory.main.wait_frames(15)
            xbox.menu_down()
            xbox.menu_b()
        else:
            click_to_diag_progress(33)
    