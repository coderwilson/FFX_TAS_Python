import logging

import battle.main
import memory.main
from memory.main import check_near_actors, actor_index, get_actor_angle, set_game_speed
import pathing
from pathing import approach_coords
import xbox
import math
import time
from paths.nem import Race1, Race2, Race3, ToRemiem
from nemesis.arena_prep import (
    return_to_airship,
    unlock_omega,
    arena_return
)
from nemesis.arena_select import (
    arena_npc, arena_menu_select, start_fight,
    navigate_to_airship_destination,
    add_airship_unlocked_location,
)
from nemesis.arena_battles import yojimbo_battle
from json_ai_files.write_seed import write_big_text
from airship_pathing import air_ship_path
from area.sin import exit_cockpit
from paths.home import BikanelDesert
from paths.cactuar_village import (
    cactuar1,
    cactuar2,
    cactuar3,
    cactuar4,
    cactuar5,
    cactuar6,
    cactuar7,
    cactuar8,
    cactuar9,
    cactuar10
)
from paths.destro_spheres import (
    zan_destro_sphere,
    besaid_destro_sphere,
    kilika_destro_sphere,
    djose_destro_sphere,
    macalania_destro_sphere
)
from paths import Kilika1, Kilika2, Kilika3, KilikaTrials
from menu import equip_armor
from save_sphere import touch_and_go
from players import CurrentPlayer, Lulu
import reset
from area.dream_zan import new_game, split_timer
from json_ai_files.write_seed import write_custom_message
import time

FFXC = xbox.controller_handle()
logger = logging.getLogger(__name__)
import vars
game_vars = vars.vars_handle()
import random
import load_game





def all_races(skip_prep=False, try_fourth_race = False):
    write_big_text("Chocobo Training")
    if not skip_prep:
        #write_custom_message("Showcase!")
        # air_ship_destination(dest_num=12)
        navigate_to_airship_destination("Calm Lands")
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
        if attempts < 0:  # Formerly tried three times.
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

def choco_tame_1(race_to_race:bool = True):
    memory.main.click_to_diag_progress(43)
    logger.info("Race start!")
    race_left = memory.main.get_actor_coords(0)[0]
    race_right = memory.main.get_actor_coords(0)[0]
    while memory.main.diag_progress_flag() not in [44, 74]:
        angle = get_actor_angle(0)
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
        memory.main.wait_frames(3)
        if race_to_race:
            target=2  # let's try something else
        else:
            target=1  # I quit
            
        while memory.main.save_menu_cursor() != target:
            while memory.main.save_menu_cursor() != target:
                xbox.tap_up()
            memory.main.wait_frames(2)
        xbox.tap_b()
        if target == 2:
            while memory.main.save_menu_cursor() != 0:
                pass  # This resets it for the next screen.
            while memory.main.save_menu_cursor() != 1:
                while memory.main.save_menu_cursor() != 1:
                    xbox.tap_up()  # Change to dodger chocobo
                memory.main.wait_frames(2)
            xbox.tap_b()
        return True
    else:
        memory.main.click_to_diag_progress(76)
        memory.main.wait_frames(12)
        xbox.tap_b()
        return False


def choco_tame_2():
    FFXC.set_neutral()
    memory.main.click_to_diag_progress(40)
    balls = []
    for i in range(memory.main.get_actor_array_size()):
        if memory.main.get_actor_id(i) == 16425:
            logger.debug(f"Ball indices: {i}")
            balls.append(i)
    logger.debug(f"Tidus ID: {memory.main.get_actor_id(0)}")
    memory.main.click_to_diag_progress(43)
    bounce = "left"
    mode = "straight"
    mode_last = "straight"
    last_dodge = "none"
    last_ball = 0
    min_angle = 1.4
    max_angle = 1.6
    angle = get_actor_angle(0)
    near_end_reset = False
    while memory.main.diag_progress_flag() not in [44, 74]:
        position = memory.main.get_actor_coords(0)
        angle = get_actor_angle(0)

        if position[1] < -1180:  # Align first position
            if position[0] < -60:
                mode = "shallow_right"
            elif position[0] < -40:
                mode = "shallow_right"
            else:
                mode = "straight"
        elif position[1] > -100:  # End, get to center.
            if position[0] > -60:
                mode = "hard_left"
            if position[0] < -100:
                mode = "hard_right"
            else:
                mode = "straight"
        elif (
            pathing.distance(balls[0]) < 550 and
            memory.main.get_actor_coords(balls[0])[1] > position[1]
        ):  # First ball approaching
            if bounce == "left":
                mode = "hard_left"
            else:
                mode = "hard_right"
        elif (
            memory.main.get_actor_coords(balls[0])[1] < position[1] and
            memory.main.get_actor_coords(balls[2])[1] > position[1]
        ):  # Between first and third balls
            if bounce == "left":
                mode = "shallow_left"
            else:
                mode = "shallow_right"
        else:  # In between waves
            if position[0] < -130:
                mode = "shallow_right"
                bounce = "right"
            elif position[0] < -120:
                mode = "straight"
                bounce = "right"
            elif position[0] < -80:
                mode = "shallow_left"
                bounce = "right"
            elif position[0] < -40:
                mode = "shallow_right"
                bounce = "left"
            elif position[0] < -30:
                mode = "straight"
                bounce = "left"
            else:
                mode = "shallow_left"
                bounce = "left"
        
        #logger.debug(mode)
        #logger.debug(f"{round(position[0],2):>8} | {section:>6} | {mode}")
        
        if mode_last != mode:
            logger.debug(f"Mode change: {mode} | {round(position[1],2):>8} , {round(position[0],2):>8}")
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
            if FFXC.is_dpad_right():
                FFXC.set_value("d_pad", 0)
            FFXC.set_value("d_pad", 8)
        elif angle < min_angle:
            if FFXC.is_dpad_left():
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

        target=2  # let's try something else
            
        while memory.main.save_menu_cursor() != target:
            while memory.main.save_menu_cursor() != target:
                xbox.tap_up()
            memory.main.wait_frames(2)
        xbox.tap_b()
        while memory.main.save_menu_cursor() != 0:
            pass  # This resets it for the next screen.
        while memory.main.save_menu_cursor() != 2:
            while memory.main.save_menu_cursor() != 2:
                xbox.tap_up()  # Change to hyper dodger chocobo
            memory.main.wait_frames(2)
        xbox.tap_b()
        return True
    else:
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        xbox.tap_b()
        return False


def choco_tame_2_v2():
    FFXC.set_neutral()
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
    angle = get_actor_angle(0)
    near_end_reset = False
    while memory.main.diag_progress_flag() not in [44, 74]:
        position = memory.main.get_actor_coords(0)
        angle = get_actor_angle(0)
        
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
            # Middle section
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
            # Starting movement
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
            logger.debug(f"Mode change: {mode} | {round(position[1],2):>8} , {round(position[0],2):>8}")
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
            if FFXC.is_dpad_right():
                FFXC.set_value("d_pad", 0)
            FFXC.set_value("d_pad", 8)
        elif angle < min_angle:
            if FFXC.is_dpad_left():
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

        target=2  # let's try something else
            
        while memory.main.save_menu_cursor() != target:
            while memory.main.save_menu_cursor() != target:
                xbox.tap_up()
            memory.main.wait_frames(2)
        xbox.tap_b()
        while memory.main.save_menu_cursor() != 0:
            pass  # This resets it for the next screen.
        while memory.main.save_menu_cursor() != 2:
            while memory.main.save_menu_cursor() != 2:
                xbox.tap_up()  # Change to hyper dodger chocobo
            memory.main.wait_frames(2)
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
        get_actor_angle(0)
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


def choco_tame_3(try_fourth_race=False):
    FFXC.set_neutral()
    memory.main.click_to_diag_progress(42)
    FFXC.set_value("d_pad", 4)
    while not memory.main.diag_progress_flag() == 43:
        pass
    checkpoint = 0
    last_cp = 0
    mode_last = "none"
    while memory.main.diag_progress_flag() not in [44, 74]:
        position = memory.main.get_actor_coords(0)
        angle = get_actor_angle(0)
        
        # V3 logic
        if position[1] > 100:  # Right at the end, force back to center.
            #logger.debug("End - centralize")
            if position[0] < -110:
                mode = "hard_right"
            elif position[0] > -50:
                mode = "hard_left"
            elif position[0] > -80:
                mode = "shallow_left"
            else:
                mode = "straight"
        elif position[1] < -1180:  # First movement.
            if position[0] > -140:
                mode = "shallow_left"
            else:
                mode = "straight"
        elif position[1] < -1050:  # Juke right
            if position[0] < -105:
                mode = "hard_right"
            elif position[0] > -90:
                mode = "shallow_left"
            else:
                mode = "straight"
        #elif position[1] < -940:
        #    mode = "shallow_left"
        elif position[1] < -900:  # Second juke right
            if position[0] < -10:
                mode = "hard_right"
            elif position[0] > -1:
                mode = "shallow_left"
            else:
                mode = "straight"
        elif position[1] < -750:
            mode = "shallow_right"
        elif position[1] < -590:  # Juke left
            if position[0] > -80:
                mode = "hard_left"
            else:
                mode = "straight"
        elif position[1] < -440:  # Juke right
            if position[0] < -60:
                mode = "hard_right"
            else:
                mode = "straight"
        elif position[1] < -290:  # Juke left again!
            if position[0] > -90:
                mode = "hard_left"
            else:
                mode = "straight"
        elif position[1] < -100:  # Juke right
            if position[0] < -60:
                mode = "hard_right"
            else:
                mode = "straight"
        elif position[1] < 50:  # Shove face into the wall for an extra dodge.
            mode = "hard_right"
        else:
            mode = "shallow_left"
        #logger.debug(mode)
        #logger.debug(f"{round(position[1],2):>8} , {round(position[0],2):>8} | {mode}")
        
        if mode_last != mode:
            logger.debug(f"Mode change: {mode} | {round(position[1],2):>8} , {round(position[0],2):>8}")
            mode_last = mode
        
        if mode == "hard_right":
            min_angle = 0.3
            max_angle = 0.5
        elif mode == "hard_left":
            min_angle = 2.4
            max_angle = 2.6
        elif mode == "shallow_right":
            min_angle = 1.3
            max_angle = 1.5
        elif mode == "shallow_left":
            min_angle = 1.8
            max_angle = 2.0
        #elif position[0] < -80:
        else:
            min_angle = 1.45
            max_angle = 1.65
        
        #logger.debug(f"{mode}: {min_angle},{max_angle}")
        
        if angle > max_angle:
            if FFXC.is_dpad_right():
                FFXC.set_value("d_pad", 0)
            FFXC.set_value("d_pad", 8)
        elif angle < min_angle:
            if FFXC.is_dpad_left():
                FFXC.set_value("d_pad", 0)
            FFXC.set_value("d_pad", 4)
        else:
            FFXC.set_value("d_pad", 0)
    FFXC.set_neutral()

    while memory.main.diag_progress_flag() not in [56, 69, 77]:
        # 56 is success
        xbox.tap_b()
    if memory.main.diag_progress_flag() == 56:  # Success
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        if try_fourth_race:
            target=2  # let's try something else
        else:
            target=1  # I quit
            
        while memory.main.save_menu_cursor() != target:
            while memory.main.save_menu_cursor() != target:
                xbox.tap_up()
            memory.main.wait_frames(2)
        xbox.tap_b()
        if target == 2:
            while memory.main.save_menu_cursor() != 0:
                pass  # This resets it for the next screen.
            while memory.main.save_menu_cursor() != 2:
                while memory.main.save_menu_cursor() != 2:
                    xbox.tap_up()  # Change to catcher chocobo
                memory.main.wait_frames(2)
            xbox.tap_b()
        return True
    else:
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        xbox.tap_b()
        return False


def choco_tame_3_old(try_fourth_race=False):
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
            target=2  # let's try something else
        else:
            target=1  # I quit
            
        while memory.main.save_menu_cursor() != target:
            while memory.main.save_menu_cursor() != target:
                xbox.tap_up()
            memory.main.wait_frames(2)
        xbox.tap_b()
        memory.main.wait_frames(3)
        if target == 2:
            while memory.main.save_menu_cursor() != 2:
                while memory.main.save_menu_cursor() != 2:
                    xbox.tap_up()  # Change to catcher chocobo
                memory.main.wait_frames(2)
            xbox.tap_b()
        return True
    else:
        memory.main.click_to_diag_progress(77)
        memory.main.wait_frames(12)
        xbox.tap_b()
        return False


def to_remiem(start_races:bool = True, get_primer=False):
    # write_big_text("Remiem Races")
    memory.main.await_control()
    logger.info("Talking to chocobo lady")
    pathing.approach_actor_by_id(20531)
    #while memory.main.user_control():
    #    pathing.set_movement([-1565, 434])
    #    xbox.tap_b()
    FFXC.set_neutral()
    logger.info("Let me ride one!")
    memory.main.click_to_control()
    logger.info("Heading to Remiem")
    #set_game_speed(2)

    pos = memory.main.get_actor_coords(0)
    if pos[0] > 1200 and pos[1] > -200:
        while not pathing.set_movement([533, -132]):
            pass
        checkpoint = 0
    elif pos[0] < -1400 and pos[1] > 275:
        while not pathing.set_movement([-1389, 130]):
            pass
        while not pathing.set_movement([-1427, -228]):
            pass
        checkpoint = 2
    else:
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
            elif checkpoint == 28 and get_primer:
                memory.main.await_control()
                pathing.primer()
                FFXC.set_neutral()
                get_primer = False
                memory.main.click_to_control_3()
            elif pathing.set_movement(ToRemiem.execute(checkpoint)) is True:
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
    
    memory.main.set_game_speed(0)
    FFXC.set_neutral()
    

def remiem_races():
    logger.debug("Ready to start races")
    choco_race_1()
    logger.info("Cloudy Mirror obtained.")
    choco_race_2()
    logger.info("Obtained Wings to Discovery")
    choco_race_3()
    logger.info("Obtained Three Stars!")


def choco_race_1():
    FFXC.set_neutral()
    check_near_actors(wait_results=False)
    while not pathing.set_movement([766,85]):
        pass
    pathing.approach_actor_by_id(20531, use_raw_coords=True)
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
    check_near_actors(wait_results=False)
    memory.main.click_to_control()
    #while not pathing.set_movement([766,85]):
    #    pass
    pathing.approach_actor_by_id(20531, use_raw_coords=True)
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
    check_near_actors(wait_results=False)
    memory.main.click_to_control()
    #while not pathing.set_movement([766,85]):
    #    pass
    pathing.approach_actor_by_id(20531, use_raw_coords=True)
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

def leave_temple(to_airship=True):
    write_big_text("")
    # Assumes we start standing next to the chocobo on the right.
    memory.main.await_control()
    memory.main.wait_frames(6)
    if to_airship:
        path = [
            [590,139],
            [495,271],
            [495,322]
        ]
    else:
        path = [
            [590,139],
            [495,271],
            [495,322],
            [399,356],
            [272,360],
            [-268,360],
            [-637,360],
            [-715,300],
            [1347,-1275],
            [1279,-1244],
            [0,0],
            [1103,-1064],
            [1111,-935],
            [0,0],
            [-390,-1169],
            [-873,-1450],
            [-782,-1645],
            [-442,-1657],
            [498,-1610],
            [551,-1645],
            [551,-1681],
            [540,-1960]
        ]
    
    for i in range(len(path)):
        if memory.main.get_map() == 329:
            logger.debug("Reached map 329. Return. (A)")
            FFXC.set_neutral()
            return
        if i == 7:
            FFXC.set_movement(0,-1)
            memory.main.await_event()
            FFXC.set_neutral()
            memory.main.await_control()
        elif i == 10:
            pathing.approach_actor_by_id(20531)
        elif i == 13:
            pathing.approach_coords([1102,-930])
            memory.main.click_to_control()
        else:
            while not pathing.set_movement(path[i]):
                if memory.main.get_map() == 329:
                    logger.debug("Reached map 329. Return. (B)")
                    FFXC.set_neutral()
                    return
            logger.debug(f"Reached marker {i}")
    if to_airship:
        return_to_airship()
    else:
        logger.debug("Reached map 329. Return. (C)")

def butterflies():
    # air_ship_destination(dest_num=9)
    navigate_to_airship_destination("Macalania")
    write_big_text("Butterfly Minigame")
    memory.main.click_to_control()
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    #set_game_speed(1)
    
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
            #logger.debug(path[i])
            pass
    
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
            #logger.debug(path[i])
            pass
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
    write_big_text("")
        
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
    get_jecht_sphere = game_vars.platinum()
    if get_jecht_sphere:
        while not pathing.set_movement([260,52]):
            pass
        while not pathing.set_movement([277,104]):
            pass
        while not pathing.set_movement([230,136]):
            pass
        pathing.approach_coords([210,135])
        FFXC.set_neutral()
        memory.main.click_to_control()
        while not pathing.set_movement([230,136]):
            pass
        while not pathing.set_movement([277,104]):
            pass
        while not pathing.set_movement([260,52]):
            pass
    #set_game_speed(0)
    
# How about getting the celestial mirror?
def upgrade_mirror(to_airship:bool=False, skip_approach=False):
    write_big_text("Upgrading Mirror")
    #set_game_speed(0)
    if not skip_approach:
        # Assume we have already arrived near the family.
        while not pathing.set_movement([253,45]):
            pass
        while not pathing.set_movement([255,62]):
            pass
        while memory.main.user_control():  # Talk to lady
            pathing.set_movement([245,62])
            xbox.tap_b()
    memory.main.click_to_control()
    while not pathing.set_movement([250,70]):
        pass
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
    write_big_text("")
    
    leave_mirror_area(to_airship=to_airship)
    
def leave_mirror_area(to_airship:bool = False):
    # Leave this area.
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

def spirit_lance(skip_dodges:bool=False):
    # Assumes we start from Macalania Woods first screen.
    if not skip_dodges:
        write_big_text("Dodges Remaining: 200")
    
    dodge_count = memory.main.l_strike_count()
    start_count = dodge_count
    
    #set_game_speed(2)
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
    #set_game_speed(0)
    
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
                
    
    if not skip_dodges:
        logger.debug("Ready to dodge.")
        run_count = 0
        while dodge_count < start_count + 200:
            if run_count % 3 == 0:
                if pathing.set_movement([-95,-1000]):
                    run_count = random.choice(range(0, 1000))
            elif run_count % 3 == 1:
                if pathing.set_movement([-137,-1020]):
                    run_count = random.choice(range(0, 1000))
            else:
                if pathing.set_movement([-112,-961]):
                    run_count = random.choice(range(0, 1000))
            if memory.main.dodge_lightning(dodge_count):
                dodge_count = memory.main.l_strike_count()
                logger.debug(f"Dodges left: {start_count + 200 - dodge_count}")
                write_big_text(f"Dodges Remaining: {start_count + 200 - dodge_count}")
    
    
    # Wrap up North map
    path = [
        [-58,-1026],
        [-22,-1087]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            if memory.main.dodge_lightning(dodge_count):
                dodge_count = memory.main.l_strike_count()
            
    write_big_text("Kimahri's second item")
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
    write_big_text("Lulu's sigil")
    
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
    if not skip_dodges:
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
    write_big_text("")

def rusty_sword(godhand:int = 0, baaj:int = 0):
    write_big_text("Rusty Sword")
    # air_ship_destination(dest_num=14+godhand+baaj)
    navigate_to_airship_destination("Gagazet")
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    #set_game_speed(2)
    
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
    
    #set_game_speed(0)
    
    for i in range(memory.main.get_actor_array_size()):
        if memory.main.get_actor_id(i) != 52685:
            logger.debug(f"Actor {i}: {memory.main.get_actor_id(i)}")
    pathing.approach_actor_by_id(20568)
    FFXC.set_neutral()
    memory.main.click_to_control()
    #set_game_speed(2)
    
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
    if game_vars.platinum():
        return_to_airship()
    
def masamune(godhand:int = 0, baaj:int = 0):
    write_big_text("Auron's Celestial")
    # air_ship_destination(dest_num=5+godhand+baaj)
    navigate_to_airship_destination("Djose")
    #set_game_speed(2)
    
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
        if i == len(path) - 2:
            #set_game_speed(0)
            pass
        while not pathing.set_movement(path[i]):
            logger.debug(path[i])
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
    #set_game_speed(2)
    
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

    if game_vars.platinum():
        while not pathing.set_movement([-34,167]):
            pass
        return_to_airship()
        return
    
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
    
    #set_game_speed(0)

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
    
    return_to_airship()

def saturn_crest(godhand:int = 0, baaj:int = 0):
    write_big_text("Saturn Crest")
    #air_ship_destination(dest_num=14+godhand+baaj)
    memory.main.click_to_control()
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    
    #Teleporter pad.
    while not pathing.set_movement([54,107]):
        pass
    memory.main.click_to_event_temple(1)
    memory.main.click_to_control()
    #set_game_speed(2)
    
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
    #set_game_speed(0)
    
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
    return_to_airship()
    
    
def moon_crest():  # Not used in current route
    write_big_text("Moon Crest")
    # air_ship_destination(dest_num=1)
    navigate_to_airship_destination("Besaid")
    memory.main.click_to_control()
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    #set_game_speed(2)
    
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
    #set_game_speed(0)
    
    # Open chest
    for i in range(memory.main.get_actor_array_size()):
        if memory.main.get_actor_id(i) != 52685 and pathing.distance(i) < 150:
            logger.debug(f"Actor {i}: {memory.main.get_actor_id(i)}, {pathing.distance(i)}")
            if memory.main.get_actor_id(i) == 20482:
                pathing.approach_actor_by_index(i)
    FFXC.set_neutral()
    memory.main.click_to_control()
    
    #set_game_speed(2)
    # Return trip
    for i in range(len(path)-1, -1, -1):
        while not pathing.set_movement(path[i]):
            pass
    
    #set_game_speed(0)
    return_to_airship()

def desert_path(start:int=4, end:int=55):
    write_big_text("Cactuar Minigame")
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
    speed_check = memory.main.get_game_speed()
    #memory.main.set_game_speed(0)
    start_time = int(time.time())  # Record the starting time as an integer.
    while memory.main.user_control():
        current_time = int(time.time())  # Get the current timestamp as an integer.
        elapsed_time = current_time - start_time

        if elapsed_time % 2 == 1:  # Every third second.
            pathing.set_movement([340, -340])
        else:  # For the other two seconds.
            pathing.set_movement([350, -340])
        
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
    speed_check = memory.main.get_game_speed()
    #memory.main.set_game_speed(0)
    start_time = int(time.time())  # Record the starting time as an integer.
    while memory.main.user_control():
        current_time = int(time.time())  # Get the current timestamp as an integer.
        elapsed_time = current_time - start_time

        if elapsed_time % 2 == 1:  # Every third second.
            pathing.set_movement([340, -340])
        else:  # For the other two seconds.
            pathing.set_movement([350, -340])
        
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

def move_cactuar(cactuar_num:int = 4, checkpoint:int = 0):
    try:
        if cactuar_num == 1:
            pos = cactuar1.checkpoint_coordiantes[checkpoint]
        elif cactuar_num == 2:
            pos = cactuar2.checkpoint_coordiantes[checkpoint]
        elif cactuar_num == 3:
            #pos = cactuar3.checkpoint_coordiantes[checkpoint]
            pos = []
        elif cactuar_num == 4:
            pos = cactuar4.checkpoint_coordiantes[checkpoint]
        elif cactuar_num == 5:
            # Technically there is no 5. Paired with 4.
            pos = cactuar5.checkpoint_coordiantes[checkpoint]
        elif cactuar_num == 6:
            #pos = cactuar6.checkpoint_coordiantes[checkpoint]
            pos = []
        elif cactuar_num == 7:
            pos = cactuar7.checkpoint_coordiantes[checkpoint]
        elif cactuar_num == 8:
            pos = cactuar8.checkpoint_coordiantes[checkpoint]
        elif cactuar_num == 9:
            pos = cactuar9.checkpoint_coordiantes[checkpoint]
            pos = []
        elif cactuar_num == 10:
            #pos = cactuar10.checkpoint_coordiantes[checkpoint]
            pos = []
        else:
            pos = []
    except:
        pos = []
    #logger.warning(pos)

    #if cactuar_num in [8]:
    #    FFXC.set_neutral()
    #    return
    if len(pos) != 0:
        #logger.debug(f"From [{round(memory.main.get_coords()[0],2)}, {round(memory.main.get_coords()[1],2)}] towards: {pos}")
        if pathing.set_movement(pos):
            return True
    else:
        #logger.debug(f"From [{round(memory.main.get_coords()[0],2)}, {round(memory.main.get_coords()[1],2)}] towards: Cactuar")
        #pathing.approach_actor_by_id(4304)
        cactuar_index = actor_index(4304)
        pathing.set_movement(memory.main.get_actor_coords(cactuar_index))
    return False


def engage_cactuar(cactuar_num:int = 99):
    speed_check = memory.main.get_game_speed()
    #memory.main.set_game_speed(0)
    if cactuar_num == 6:
        touch_and_go()
    elif cactuar_num == 7:
        pathing.approach_actor_by_id(20482)
    elif cactuar_num == 9:
        while memory.main.user_control():
            pathing.set_movement([7,-200])
    elif not cactuar_num in [3,10]:
        pathing.approach_actor_by_id(4304)
    if cactuar_num == 9:
        memory.main.click_to_diag_progress(33)
    else:
        memory.main.click_to_diag_progress(41)
    memory.main.click_to_control()
    start_frame = memory.main.get_frame_count()
    last_turn_frame = start_frame
    check_near_actors(wait_results=False, max_dist=350)
    if cactuar_num == 4:
        # Some value between 19 and 22 (inclusive)
        cactuar_index = 21
    else:
        cactuar_index = actor_index(4304)
    cactuar_angle = get_actor_angle(cactuar_index)
    angle_set = False
    last_status = "None"
    new_status = "None"
    last_diag = memory.main.diag_progress_flag()
    logger.warning(f"Prepping cactuar angle: {cactuar_angle}")
    checkpoint = 0
    #while not memory.main.diag_progress_flag() in [64, 77, 78, 92, 95, 106]:
    while (
        (not memory.main.battle_active()) and 
        (not memory.main.diag_progress_flag() in [64, 77, 78, 92, 95, 106])
    ):
        if memory.main.diag_progress_flag() == 40:
            checkpoint = 0
        elif memory.main.user_control():
            # General movement.
            if memory.main.get_frame_count() - start_frame < 4:
                # Always move for the first four frames.
                new_status = "First Four Frames"
                last_turn_frame = memory.main.get_frame_count()
                if move_cactuar(cactuar_num=cactuar_num, checkpoint=checkpoint):
                    checkpoint += 1
            elif cactuar_num == 4 and memory.main.get_frame_count() - start_frame < 15:
                last_turn_frame = memory.main.get_frame_count()
                new_status = "First Ten Frames"
                if move_cactuar(cactuar_num=cactuar_num, checkpoint=checkpoint):
                    checkpoint += 1
            elif not angle_set:
                # First time we hit this, should be after four frames so Cactuar adjusts.
                cactuar_angle = get_actor_angle(cactuar_index)
                logger.debug(f"Angle update: {cactuar_angle}")
                angle_set = True
            elif cactuar_num == 8 and checkpoint in [1,2]:
                last_turn_frame = memory.main.get_frame_count()
                new_status = "Underground Move"
                if move_cactuar(cactuar_num=cactuar_num, checkpoint=checkpoint):
                    checkpoint += 1
            elif get_actor_angle(cactuar_index) == cactuar_angle:
                last_turn_frame = memory.main.get_frame_count()
                new_status = "Main Move"
                if move_cactuar(cactuar_num=cactuar_num, checkpoint=checkpoint):
                    checkpoint += 1
            elif memory.main.get_frame_count() - last_turn_frame < 4:
                new_status = "Buffer Move"
                # As cactuar is turning, we have a small buffer to continue moving.
                if move_cactuar(cactuar_num=cactuar_num, checkpoint=checkpoint):
                    checkpoint += 1
            else:
                new_status = "HOOOOOOOOLD"
                FFXC.set_neutral()
            
        elif memory.main.diag_progress_flag() != last_diag:
            FFXC.set_neutral()
            new_status = "Diag progress change"
            xbox.tap_b()
            last_diag = memory.main.diag_progress_flag()
        else:
            FFXC.set_neutral()
            xbox.tap_b()
        
        if last_status != new_status:
            if new_status == "Diag progress change":
                logger.debug(f"Diag: {memory.main.diag_progress_flag()} | {new_status}")
            else:
                logger.debug(f"[{round(memory.main.get_coords()[0],2)}, {round(memory.main.get_coords()[1],2)}] | {new_status}")
            #logger.debug(f"[{round(last_angle,2)}, {round(get_actor_angle(cactuar_index),2)}] | {new_status}")
            last_status = new_status
        
        if (cactuar_num==9 and memory.main.diag_progress_flag() == 41):
            dist_check = int(memory.main.distance(actor_index=cactuar_index))
            logger.debug(f"Dist: {dist_check}")
            if dist_check > 200:
                break
    logger.debug(f"Final Progress flag: {memory.main.diag_progress_flag()}")
    # If battle started, we will just blindly attack to victory.
    while not memory.main.user_control():
        if memory.main.battle_active():
            while not memory.main.battle_wrap_up_active():
                if memory.main.turn_ready():
                    CurrentPlayer().attack()
            battle.main.wrap_up()
        else:
            xbox.tap_confirm()
    #memory.main.set_game_speed(speed_check)

def cactuars(godhand:int = 0, baaj:int = 0):
    # Assumes airship start.
    # air_ship_destination(dest_num=10+godhand+baaj)
    navigate_to_airship_destination("Bikanel")
    memory.main.update_formation(0, 1, 4)
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    ##memory.main.set_game_speed(2)
    
    desert_path(start=4, end=40)
    
    divert_to_stone_south()
    desert_path(start=39, end=3)
    while not pathing.set_movement([-43,-98]):
        pass
    check_near_actors(wait_results=False)
    engage_cactuar(cactuar_num = 1)  # First cactuar
    
    desert_path(start=5, end=40)
    divert_to_stone_south()
    desert_path(start=39, end=34)
    while not pathing.set_movement([412,532]):
        pass
    check_near_actors(wait_results=False)
    engage_cactuar(cactuar_num = 2)  # Second cactuar
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
    engage_cactuar(cactuar_num=4)  # 4 and 5, brothers.
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
    engage_cactuar(cactuar_num=7)  # seventh cactuar (chest guys)
    
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
    engage_cactuar(cactuar_num=8)  # Eighth cactuar (sinkhole guys)
    divert_to_stone_north(return_north=False)
    
    
    # Airship guy.
    desert_path(start=39, end=2)
    #memory.main.set_game_speed(0)
    return_to_airship()
    FFXC.set_neutral()
    
def cactuars_finish(godhand:int = 0, baaj:int = 0):
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
    memory.main.wait_frames(60)
    memory.main.click_to_control()
    #memory.main.wait_frames(900)
    engage_cactuar(cactuar_num=9)  # Airship guy
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
    
    # air_ship_destination(dest_num=10+godhand+baaj)
    navigate_to_airship_destination("Bikanel")
    memory.main.await_control()
    
    ##memory.main.set_game_speed(2)
    desert_path(start=4, end=40)
    divert_to_stone_south(last_path=True)
    
    engage_cactuar(cactuar_num=10)  # Last one is behind you.
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
    #memory.main.set_game_speed(0)
    return_to_airship()
    
    FFXC.set_neutral()

def onion_knight(godhand:int = 0, baaj:int = 0):
    write_big_text("Onion Knight")
    unlock_omega(x=15,y=-60)  # Baaj temple
    # air_ship_destination(1)
    add_airship_unlocked_location("Baaj")
    navigate_to_airship_destination("Baaj")
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

    # Let's go get Seymour's mom
    current_map = memory.main.get_map()
    while current_map == memory.main.get_map():
        pathing.set_movement([2,230])
        FFXC.set_back()
    FFXC.set_neutral()
    memory.main.click_to_control()
    while not pathing.set_movement([-5,-241]):
        pass
    while not pathing.set_movement([-92,-147]):
        pass
    while not pathing.set_movement([-22,-147]):
        pass
    while not pathing.set_movement([-3,-110]):
        pass
    current_map = memory.main.get_map()
    while current_map == memory.main.get_map():
        pathing.set_movement([-2,10])
    memory.main.click_to_control()

    # Room with six statues
    while not pathing.set_movement([0,-29]):
        pass
    pathing.approach_coords([-20,-29])
    FFXC.set_neutral()
    memory.main.click_to_control()
    pathing.approach_coords([20,-29])
    FFXC.set_neutral()
    memory.main.click_to_control()
    
    while not pathing.set_movement([0,0]):
        pass
    pathing.approach_coords([-20,0])
    FFXC.set_neutral()
    memory.main.click_to_control()
    pathing.approach_coords([20,0])
    FFXC.set_neutral()
    memory.main.click_to_control()
    
    while not pathing.set_movement([0,30]):
        pass
    pathing.approach_coords([-20,29])
    FFXC.set_neutral()
    memory.main.click_to_control()
    pathing.approach_coords([20,29])
    FFXC.set_neutral()
    memory.main.click_to_control()

    
    while not pathing.set_movement([0,41]):
        pass
    memory.main.click_to_event_temple(0)
    memory.main.await_control()

    # Room with aeon
    FFXC.set_movement(0,1)
    memory.main.await_event()
    FFXC.set_neutral()
    while not memory.main.name_aeon_ready():
        pass
    xbox.name_aeon("Anima")  # Set Anima name
    memory.main.await_control()
    FFXC.set_movement(0,-1)  # Leave chamber
    memory.main.await_event()
    FFXC.set_neutral()
    memory.main.await_control()
    FFXC.set_movement(0,-1)  # Leave statue room
    memory.main.await_event()
    FFXC.set_neutral()

    # Back to circle area
    while not pathing.set_movement([-24,-147]):
        pass
    while not pathing.set_movement([-92,-147]):
        pass
    while not pathing.set_movement([-92,-183]):
        pass
    while not pathing.set_movement([-4,-248]):
        pass
    while not pathing.set_movement([0,-341]):
        pass
    current_map = memory.main.get_map()
    while current_map == memory.main.get_map():
        pathing.set_movement([0,-600])
    FFXC.set_neutral()
    
    
    # Now to get Lulu's chest.
    FFXC.set_back()
    while not pathing.set_movement([14,-93]):
        pass
    while not pathing.set_movement([67,-143]):
        pass
    while not pathing.set_movement([54,-140]):
        pass
    FFXC.set_movement(0,0)
    FFXC.release_back()
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

def belgemine(godhand:int = 1, baaj:int = 1):
    write_big_text("Belgemine / Yuna's Celestial")
    arena_return(godhand=godhand, baaj=baaj)

    FFXC.set_neutral()
    memory.main.await_control()
    pathing.approach_actor_by_id(20482)  # Open chest for Yuna
    FFXC.set_neutral()
    memory.main.click_to_control()
    
    current_map = memory.main.get_map()
    while current_map == memory.main.get_map():
        FFXC.set_movement(0,-1)
    #return_to_airship()
    #memory.main.await_control()
    #air_ship_destination(dest_num=12+godhand+baaj)
    #while not pathing.set_movement([-638, -121]):
    #    pass
    memory.main.click_to_control()
    check_near_actors(wait_results=False, max_dist=350)

    to_remiem(start_races=False)
    while not pathing.set_movement([501, 357]):
        pass
    while not pathing.set_movement([542, 357]):
        pass
    current_map = memory.main.get_map()
    while current_map == memory.main.get_map():
        FFXC.set_movement(0,1)
    FFXC.set_neutral()
    logger.debug("Belgemine dialogue")
    while not memory.main.diag_progress_flag() == 9:
        pass
    
    for i in range(7):
        if memory.main.user_control():
            while memory.main.user_control():
                pathing.set_movement([-10,0])
        logger.warning(f"Belgemine Battle Number: {i}")
        if i == 4:  # Bahamut battle, can't run mirror matchup.
            battle.main.belgemine(use_aeon=2)
        elif i in [3,5]:
            battle.main.belgemine(impulse=True)
        else:
            battle.main.belgemine()
        FFXC.set_neutral()

        
    # To the girls
    path = [
        [-61,-61],
        [11,-78],
        [105,-26]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
        logger.debug(f"mark {i}")
    logger.debug("Approach 1")
    while memory.main.user_control():
        pathing.set_movement([160,0])
        xbox.tap_b()
    FFXC.set_neutral()
    logger.debug("Approach 2")
    while not memory.main.name_aeon_ready():
        xbox.menu_b()
    logger.debug("Names")
    #xbox.name_aeon("Cindy")
    memory.main.wait_frames(90)
    xbox.menu_b()
    memory.main.wait_frames(30)
    xbox.menu_up()
    xbox.menu_b()
    #xbox.name_aeon("Sandy")
    memory.main.wait_frames(90)
    xbox.menu_b()
    memory.main.wait_frames(30)
    xbox.menu_up()
    xbox.menu_b()
    #xbox.name_aeon("Mindy")
    memory.main.wait_frames(90)
    xbox.menu_b()
    memory.main.wait_frames(30)
    xbox.menu_up()
    xbox.menu_b()
    memory.main.await_control()
    while memory.main.user_control():
        pathing.set_movement([160,0])  # Dialog with the girls
        
    last_time = int(time.time())
    while memory.main.diag_progress_flag() != 2:
        current_time = int(time.time())
        if current_time != last_time:
            logger.debug(f"Dialog: {memory.main.diag_progress_flag()}")
            last_time = current_time
    
    memory.main.wait_frames(240)
    memory.main.click_to_control()

    current_map = memory.main.get_map()  # Leave girls room.
    while current_map == memory.main.get_map():
        pathing.set_movement([0, -105])
    memory.main.await_control()
    
    while memory.main.user_control():
        pathing.set_movement([-10,0])
    battle.main.belgemine(impulse=True, special_end=True)
    FFXC.set_neutral()

    last_time = int(time.time())
    while memory.main.diag_progress_flag() != 48:
        current_time = int(time.time())
        if current_time != last_time:
            logger.debug(f"Dialog: {memory.main.diag_progress_flag()}")
            last_time = current_time
        if memory.main.diag_progress_flag() in [38,45]:
            xbox.menu_b()
            
    memory.main.wait_frames(240)
    memory.main.click_to_control()
    
    while not pathing.set_movement([-135, 0]):
        pass
    current_map = memory.main.get_map()
    while current_map == memory.main.get_map():
        pathing.set_movement([-180, 0])
    memory.main.click_to_control()
    
    while not pathing.set_movement([501, 361]):
        pass
    return_to_airship()


def godhand(baaj:int=0):
    write_big_text("Rikku's Celestial")
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
    xbox.menu_up()
    xbox.menu_b()
    
    # Borrowed from airship destination logic
    # logger.debug("Destination select on screen now.")
    dest_num = 5 + baaj
    while memory.main.map_cursor() != dest_num:
        if dest_num < 8:
            xbox.tap_down()
        else:
            xbox.tap_up()
    memory.main.wait_frames(2)
    xbox.menu_b()
    memory.main.wait_frames(2)
    xbox.tap_b()
    while not memory.main.user_control():
        if memory.main.cutscene_skip_possible():
            xbox.skip_scene()
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
    
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


def sun_sigil(godhand:int = 1, baaj:int = 1, redo_training=False):
    write_big_text("Sun Sigil")
    # Assumes airship start.
    logger.debug("Now to get the Sun Sigil.")
    
    # air_ship_destination(dest_num=(12+godhand+baaj))
    navigate_to_airship_destination("Calm Lands")
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    ##memory.main.set_game_speed(2)
    
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

    if redo_training:
        all_races(skip_prep=True, try_fourth_race = True)
    else:
        memory.main.wait_seconds(8)
        xbox.tap_b()
        memory.main.wait_seconds(10)
        xbox.menu_up()
        xbox.tap_b()
        #memory.main.wait_seconds(30)
        catcher_complete = False
        while not catcher_complete:
            catcher_complete = choco_tame_4()

    logger.debug("Catcher Chocobo complete. Let's get our prize!")
    memory.main.await_control()
    #memory.main.set_game_speed(2)
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
    #memory.main.set_game_speed(0)
    pathing.approach_coords([-851,720])
    
    
    memory.main.click_to_control()
    #memory.main.set_game_speed(2)
    get_primer = True
    for i in range(len(path)-2,-1,-1):
        if i == 5 and get_primer:
            while not pathing.set_movement([-1273,454]):
                pass
            pathing.approach_coords([-1770,220])
            FFXC.set_neutral()
            memory.main.click_to_control()
            get_primer = False
        while not pathing.set_movement(path[i]):
            pass
        logger.debug(f"Checkpoint {i} reached.")
    while not pathing.set_movement([-620,-137]):
        pass
    while not pathing.set_movement([-656,-64]):
        pass
    #memory.main.set_game_speed(0)
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
    write_big_text("SEAGULLS!!!")
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
        try:
            if memory.main.distance(balloon) > 90:
                desired_angle = adjust_for_birds(birds, desired_angle)
        except:
            desired_angle = 0
        
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
    write_big_text("Venus Crest")
    # Assumes airship start.
    
    # air_ship_destination(dest_num=(7+godhand+baaj))
    navigate_to_airship_destination("Guadosalam")
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    ##memory.main.set_game_speed(2)
    
    
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
    
    ##memory.main.set_game_speed(0)
    return_to_airship()

def besaid_destro(godhand:int = 1, baaj:int = 1, jecht_sphere:bool=False, checkpoint:int = 0):
    write_big_text("Besaid Destruction Sphere")
    # Includes destro sphere
    #write_custom_message("Showcase!")
    # memory.main.fill_overdrive()  # We now fill Yojimbo's overdrive properly.
    # air_ship_destination(dest_num=(1+baaj))
    navigate_to_airship_destination("Besaid")
    memory.main.update_formation(0, 4, 6)
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    # memory.main.set_gil_value(999999999)
    
    current_map = memory.main.get_map()
    #while current_map == memory.main.get_map():
    #    pathing.set_movement([-380,-460])
    memory.main.await_control()
    current_map = memory.main.get_map()

    while memory.main.get_map() != 17:
        if memory.main.user_control():
            # events
            if current_map != memory.main.get_map():
                checkpoint += 1
                current_map = memory.main.get_map()
            elif checkpoint == 6:
                pathing.approach_actor_by_id(20482)
                memory.main.click_to_control()
                checkpoint += 1

            # General pathing
            elif pathing.set_movement(besaid_destro_sphere.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
    
    success = False
    while not success:
        xbox.click_to_battle()
        cur_gil = min(memory.main.get_gil_value(),99999999)
        success = yojimbo_battle(flee_available=False)
        logger.debug(f"Yojimbo results: {success}")
        if not success:
            logger.debug("Starting reset process.")
            reset.reset_to_main_menu()
            logger.debug("Intro screen - load game")
            new_game(gamestate="reload_autosave")
            logger.debug("Selecting save number.")
            load_game.load_save_num(0)
    split_timer()
    memory.main.await_control()

    path = [
        [-1,492],
        [-19,74],
        [-22,20],
        [-15,-42],
        [-5,-75],
        [-2,-176],
        [0,-250],
        [1,33],
        [1,77],
        [-1,200]
    ]
    current_map = memory.main.get_map()
    for i in range(len(path)):
        if i == 2 and jecht_sphere:
            while not pathing.set_movement([-124,43]):
                pass
            while not pathing.set_movement([-137,17]):
                pass
            pathing.approach_coords([-147,-5])
            FFXC.set_neutral()
            memory.main.click_to_control()
            while not pathing.set_movement([-137,17]):
                pass
            while not pathing.set_movement([-124,43]):
                pass
            while not pathing.set_movement([-19,104]):
                pass
            while not pathing.set_movement([80,231]):
                pass
            while not pathing.set_movement([105,231]):
                pass
            FFXC.set_movement(-1,1)
            memory.main.await_event()
            FFXC.set_neutral()
            memory.main.await_control()
            
            while not pathing.set_movement([-1,-2]):
                pass
            while not pathing.set_movement([-1,-52]):
                pass
            return_to_airship()
            return  # End of section, assuming we get the Jecht Sphere.
        while current_map == memory.main.get_map() and not pathing.set_movement(path[i]):
            pass
        if current_map != memory.main.get_map():
            current_map = memory.main.get_map()
    import area.besaid

    area.besaid.trials(destro=True)

    current_map = memory.main.get_map()
    while current_map == memory.main.get_map():
        pathing.set_movement([0, memory.main.get_actor_coords(0)[1] + 30])
    FFXC.set_neutral()
    while memory.main.diag_progress_flag() != 3:
        pass
    memory.main.wait_frames(270)  # Because I like the dialog here
    memory.main.click_to_control()

    while not pathing.set_movement([27,-21]):
        # Chest 1
        pass
    FFXC.set_neutral()
    check_near_actors(False)
    pathing.approach_actor_by_id(20482)
    memory.main.click_to_control()

    while not pathing.set_movement([19,19]):
        # Chest 2
        pass
    FFXC.set_neutral()
    check_near_actors(False)
    pathing.approach_actor_by_id(20482)
    memory.main.click_to_control()

    while not pathing.set_movement([-16,31]):
        # Chest 3
        pass
    FFXC.set_neutral()
    check_near_actors(False)
    pathing.approach_actor_by_id(20482)
    memory.main.click_to_control()

    while not pathing.set_movement([-30,-12]):
        # Chest 4
        pass
    FFXC.set_neutral()
    check_near_actors(False)
    pathing.approach_actor_by_id(20482)
    memory.main.click_to_control()

    while not pathing.set_movement([0,-43]):
        # Near exit
        pass
    
    current_map = memory.main.get_map()
    while current_map == memory.main.get_map():
        FFXC.set_movement(0,-1)  # Out of fayth chamber
    FFXC.set_neutral()
    memory.main.await_control()

    while not pathing.set_movement([0,-68]):
        # Near exit
        pass
    
    current_map = memory.main.get_map()
    while current_map == memory.main.get_map():
        FFXC.set_movement(0,-1)  # Out of fayth foyer
    FFXC.set_neutral()
    memory.main.await_control()

    current_map = memory.main.get_map()
    while current_map == memory.main.get_map():
        pathing.set_movement([-1,-140])  # Leave temple
    FFXC.set_neutral()
    memory.main.await_control()

    # Save sphere in crusaders' tent
    while not pathing.set_movement([20,-11]):
        pass
    while not pathing.set_movement([22,39]):
        pass
    while not pathing.set_movement([40,138]):
        pass
    while not pathing.set_movement([63,204]):
        pass
    while not pathing.set_movement([102,220]):
        pass
    
    current_map = memory.main.get_map()
    while current_map == memory.main.get_map():
        pathing.set_movement([150,225])  # Crusader tent
    FFXC.set_neutral()
    memory.main.await_control()

    while not pathing.set_movement([-3,48]):
        pass
    return_to_airship()
    

def kilika_destro(godhand:int = 0, baaj:int = 0):
    write_big_text("Kilika Destruction Sphere")
    import area.kilika
    #write_custom_message("Showcase!")
    # air_ship_destination(dest_num=(2+baaj))
    navigate_to_airship_destination("Kilika")
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    # memory.main.set_gil_value(999999999)

    path = Kilika1.checkpoint_coordiantes
    i = 17
    current_map = memory.main.get_map()
    while memory.main.get_map() == current_map:
        if i == 18:
            FFXC.set_movement(-1,1)
            memory.main.await_event()
        else:
            logger.debug(f"Path check: ({i}) - {path[i]}")
            while not pathing.set_movement(path[i]):
                pass
        i += 1
        
    logger.debug(f"Transition to next map: {memory.main.get_map()}")
    current_map = memory.main.get_map()
    while memory.main.get_map() == current_map:
        if i == 18:
            FFXC.set_movement(-1,1)
            memory.main.await_event()
        else:
            logger.debug(f"Path check: ({i}) - {path[i]}")
            while (not pathing.set_movement(path[i])) and memory.main.get_map() == current_map:
                pass
        i += 1
        
    logger.debug(f"Transition to next map: {memory.main.get_map()}")
    path = Kilika2.checkpoint_coordiantes
    i = 0
    current_map = memory.main.get_map()
    while memory.main.get_map() == current_map:
        try:
            logger.debug(f"Path check: ({i}) - {path[i]}")
            if i in [9,82] or i in range(37,60):
                pass
            else:
                while not pathing.set_movement(path[i]) and memory.main.get_map() == current_map:
                    pass
        except:
            # Skip the ones where there is an event in the normal run.
            pass
        i += 1

    current_map = memory.main.get_map()  # Geneaux map
    while memory.main.get_map() == current_map:
        try:
            logger.debug(f"Path check: ({i}) - {path[i]}")
            if i == 9 or i in range(38,58):
                pass
            else:
                while not pathing.set_movement(path[i]) and memory.main.get_map() == current_map:
                    pass
        except:
            # Skip the ones where there is an event in the normal run.
            pass
        i += 1

    current_map = memory.main.get_map()  # Outside temple
    while memory.main.get_map() == current_map:
        try:
            logger.debug(f"Path check: ({i}) - {path[i]}")
            if i == 9 or i in range(38,58):
                pass
            else:
                while not pathing.set_movement(path[i]) and memory.main.get_map() == current_map:
                    pass
        except:
            # Skip the ones where there is an event in the normal run.
            pass
        i += 1

    current_map = memory.main.get_map()  # Inside temple
    while i < 101:
        try:
            logger.debug(f"Path check: ({i}) - {path[i]}")
            while not pathing.set_movement(path[i]) and memory.main.get_map() == current_map:
                pass
        except:
            # Skip the ones where there is an event in the normal run.
            pass
        i += 1
    
    FFXC.set_movement(0,1)
    memory.main.await_event()
    FFXC.set_neutral()
    memory.main.click_to_control()
    
    while not pathing.set_movement([-1,-4]):
        # Elevator down
        pass
    FFXC.set_neutral()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    if memory.main.user_control():
        while memory.main.user_control():
            xbox.tap_b()
    memory.main.await_control()
    
    current_map = memory.main.get_map()
    while current_map == memory.main.get_map():
        pathing.set_movement([-1,320])
    memory.main.await_control()
    
    area.kilika.trials(destro=True)
    memory.main.await_control()

    current_map = memory.main.get_map()
    while current_map == memory.main.get_map():
        pathing.set_movement([-1,100])

    FFXC.set_neutral()  # Fayth dialog
    while memory.main.diag_progress_flag() != 2:
        pass
    #while not memory.main.user_control():
    #    logger.debug(memory.main.diag_progress_flag())
    memory.main.wait_frames(270)  # Because I like the dialog here
    memory.main.click_to_control()

    while not pathing.set_movement([27,-21]):
        # Chest 1
        pass
    FFXC.set_neutral()
    check_near_actors(False)
    pathing.approach_actor_by_id(20482)
    memory.main.click_to_control()

    while not pathing.set_movement([16,21]):
        # Chest 2
        pass
    FFXC.set_neutral()
    check_near_actors(False)
    pathing.approach_actor_by_id(20482)
    memory.main.click_to_control()

    while not pathing.set_movement([-16,26]):
        # Chest 3
        pass
    FFXC.set_neutral()
    check_near_actors(False)
    pathing.approach_actor_by_id(20482)
    memory.main.click_to_control()
    
    while not pathing.set_movement([-1,-44]):
        # Near exit
        pass
    
    current_map = memory.main.get_map()  # Leave fayth room
    while current_map == memory.main.get_map():
        pathing.set_movement([-1,-130])
    current_map = memory.main.get_map()  # Leave fayth foyer
    while current_map == memory.main.get_map():
        pathing.set_movement([-1,-130])
    
    
    while not pathing.set_movement([-1,-4]):
        # Elevator up
        pass
    FFXC.set_neutral()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    if memory.main.user_control():
        while memory.main.user_control():
            xbox.tap_b()
    memory.main.await_control()

    
    current_map = memory.main.get_map()  # Leave elevator room
    while current_map == memory.main.get_map():
        pathing.set_movement([-1,-80])
    memory.main.await_control()
    
    while not pathing.set_movement([1,55]):
        pass
    while not pathing.set_movement([27,35]):
        pass
    return_to_airship()

def djose_destro(godhand:int = 1, baaj:int = 1):
    write_big_text("Djose Destruction Sphere")
    # Includes destro sphere
    #write_custom_message("Showcase!")
    # air_ship_destination(dest_num=(5+godhand+baaj))
    navigate_to_airship_destination("Djose")
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    
    checkpoint = 0
    current_map = memory.main.get_map()
    while checkpoint < 28:
        if memory.main.user_control():
            # events
            if current_map != memory.main.get_map():
                checkpoint += 1
                current_map = memory.main.get_map()

            # General pathing
            elif pathing.set_movement(djose_destro_sphere.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
    while memory.main.user_control():
        pathing.set_movement([0,200])  # Are you prepared?
    FFXC.set_neutral()
    memory.main.click_to_control()
    while memory.main.user_control():
        pathing.set_movement([0,200])
    
    import area.djose
    area.djose.trials(destro=True)

    while not pathing.set_movement([0,50]):
        pass
    current_map = memory.main.get_map()
    while current_map == memory.main.get_map():
        pathing.set_movement([0,100])
        
    FFXC.set_neutral()  # Fayth dialog
    while memory.main.diag_progress_flag() != 4:
        pass
    #while not memory.main.user_control():
    #    if memory.main.diag_skip_possible():
    #        logger.debug(memory.main.diag_progress_flag())
    #        xbox.tap_b()
    memory.main.wait_frames(270)  # Because I like the dialog here
    memory.main.click_to_control()

    while not pathing.set_movement([25,23]):
        # Chest 1
        pass
    FFXC.set_neutral()
    check_near_actors(False)
    pathing.approach_actor_by_id(20482)
    memory.main.click_to_control()

    while not pathing.set_movement([-13,31]):
        # Chest 2
        pass
    FFXC.set_neutral()
    check_near_actors(False)
    pathing.approach_actor_by_id(20482)
    memory.main.click_to_control()

    while not pathing.set_movement([-1,-44]):
        # Near exit
        pass
    
    current_map = memory.main.get_map()  # Leave fayth room
    while current_map == memory.main.get_map():
        pathing.set_movement([-1,-130])
    current_map = memory.main.get_map()  # Leave fayth foyer
    while current_map == memory.main.get_map():
        pathing.set_movement([-1,-90])
    current_map = memory.main.get_map()  # Leave temple
    while current_map == memory.main.get_map():
        pathing.set_movement([-1,-160])
        
    while not pathing.set_movement([18,-161]):
        pass
    while not pathing.set_movement([81,-239]):
        pass
    return_to_airship()
    
def ice_destro(godhand:int = 1, baaj:int = 1):
    write_big_text("Macalania Destruction Sphere")
    # Includes destro sphere
    # memory.main.fill_overdrive()  # We now fill Yojimbo's overdrive properly.
    # memory.main.set_gil_value(999999999)
    #write_custom_message("Showcase!")
    # air_ship_destination(dest_num=(9+godhand+baaj))
    navigate_to_airship_destination("Macalania")
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    memory.main.update_formation(0, 2, 5)
    import area.mac_temple
    
    checkpoint = 0
    current_map = memory.main.get_map()
    while checkpoint < 51:  # Ends after entering temple.
    # while checkpoint < 68:  # Ends in fayth room.
        if memory.main.user_control():
            # events
            if current_map != memory.main.get_map():
                checkpoint += 1
                current_map = memory.main.get_map()

            # General pathing
            elif pathing.set_movement(macalania_destro_sphere.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if checkpoint == 67 and memory.main.get_map() == 284:
                break
            elif memory.main.battle_active():
                xbox.click_to_battle()
                cur_gil = min(memory.main.get_gil_value(),99999999)
                success = yojimbo_battle(flee_available=False)
                logger.debug(f"Yojimbo results: {success}")
                if success:
                    split_timer()
                    area.mac_temple.escape(dark_aeon=True)
                    checkpoint = 33
                else:
                    logger.debug("Starting reset process.")
                    reset.reset_to_main_menu()
                    logger.debug("Intro screen - load game")
                    new_game(gamestate="reload_autosave")
                    logger.debug("Selecting save number.")
                    load_game.load_save_num(0)
                    checkpoint = 35
                memory.main.await_control()

    # checkpoint += 1
    # FFXC.set_neutral()  # Fayth dialog
    # logger.debug("Fayth room")
    # while memory.main.diag_progress_flag() != 4:
    #     pass
    # #while not memory.main.user_control():
    # #    if memory.main.diag_skip_possible():
    # #        logger.debug(memory.main.diag_progress_flag())
    # #        xbox.tap_b()
    # memory.main.wait_frames(270)  # Because I like the dialog here
    # memory.main.click_to_control()

    # while not pathing.set_movement([22,22]):
    #     # Chest 1
    #     pass
    # FFXC.set_neutral()
    # check_near_actors(False)
    # pathing.approach_actor_by_id(20482)
    # memory.main.click_to_control()

    # while not pathing.set_movement([-13,30]):
    #     # Chest 2
    #     pass
    # FFXC.set_neutral()
    # check_near_actors(False)
    # pathing.approach_actor_by_id(20482)
    # memory.main.click_to_control()

    # while not pathing.set_movement([0,-42]):
    #     # Near exit
    #     pass

    # current_map = memory.main.get_map()
    # while checkpoint < 79:
    #     if memory.main.user_control():
    #         # events
    #         if current_map != memory.main.get_map():
    #             checkpoint += 1
    #             current_map = memory.main.get_map()

    #         # General pathing
    #         elif pathing.set_movement(macalania_destro_sphere.execute(checkpoint)):
    #             checkpoint += 1
    #             logger.debug(f"Checkpoint {checkpoint}")
    
    # area.mac_temple.trials(destro=True)

    # while not pathing.set_movement([-6, -76]):
    #     pass
    # while not pathing.set_movement([-14, -108]):
    #     pass
    return_to_airship()
  

def sun_crest(godhand:int = 1, baaj:int = 1, face_bahamut=True, get_crest=True):
    write_big_text("Sun Crest")
    # Includes destro sphere
    #write_custom_message("Showcase!")
    # memory.main.fill_overdrive()  # We now fill Yojimbo's overdrive properly.
    # air_ship_destination(dest_num=(15+godhand+baaj))
    navigate_to_airship_destination("Zanarkand")
    memory.main.update_formation(0, 3, 5)
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    # memory.main.set_gil_value(999999999)
    
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
    path = zan_destro_sphere.checkpoint_coordiantes
    for i in range(len(path)):
        if i in [8,31]:
            FFXC.set_movement(-1,1)
            memory.main.wait_frames(30)
        elif i == 26:
            FFXC.set_movement(1,0)
            memory.main.wait_frames(30)
        elif i == 28:
            pathing.approach_coords([105, 50])
        elif i == 34:
            pathing.approach_coords([-68, 120])
        elif i == 36:
            pathing.approach_coords([-82, 130])
        else:
            while not pathing.set_movement(path[i]):
                pass
    memory.main.click_to_event_temple(0)
    memory.main.await_control()
    
    if face_bahamut:
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
            #memory.main.set_game_speed(2)
            cur_gil = min(memory.main.get_gil_value(),99999999)
            #cur_gil = memory.main.get_gil_value()
            success = yojimbo_battle(flee_available=False)
            logger.debug(f"Yojimbo results: {success}")
            if not success:
                logger.debug("Starting reset process.")
                reset.reset_to_main_menu()
                logger.debug("Intro screen - load game")
                new_game(gamestate="reload_autosave")
                logger.debug("Selecting save number.")
                load_game.load_save_num(0)
            else:
                split_timer()
        memory.main.await_control()

    if get_crest:
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
    
    memory.main.await_control()
    while memory.main.get_map() != 318:
        coords = memory.main.get_coords()
        if memory.main.get_map() == 270:
            if coords[0] < -25 or coords[1] > -140:
                pathing.set_movement([-12,-156])
            else:
                pathing.set_movement([-2,-250])
        elif memory.main.get_map() == 270:
            if coords[1] > -40:
                pathing.set_movement([-1,-45])
            else:
                pathing.set_movement([-1,-120])
    memory.main.await_control()
    
    # Save sphere screen
    coords = memory.main.get_coords()
    while coords[1] > -165 or coords[1] < -185:
        coords = memory.main.get_coords()
        if coords[1] > -45:
            pathing.set_movement([0,-50])
        elif coords[1] > -165:
            pathing.set_movement([0,-170])
        elif coords[1] < -185:
            pathing.set_movement([0,-170])
    
    #memory.main.set_game_speed(0)
    return_to_airship()

def upgrade_celestials(godhand:int=1, baaj:int=1, Yuna:bool=False, Wakka:bool=False,Tidus_only=False):
    write_big_text("Upgrading Celestial Weapons")
    # air_ship_destination(dest_num=(9+godhand+baaj))
    navigate_to_airship_destination("Macalania")
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
        xbox.tap_b()
    FFXC.set_neutral()
    memory.main.click_to_diag_progress(33)
    if Tidus_only:
        upgrade_engage(0,force_end=True)
    else:
        for i in range(7):
            if i == 1 and not Yuna:
                pass
            elif i == 4 and not Wakka:
                pass
            else:
                upgrade_engage(i)
    leave_mirror_area(True)
    pass


def end_showcase(godhand:bool=False, baaj:bool=False):
    write_big_text("")
    # air_ship_destination(dest_num=14+godhand+baaj)
    navigate_to_airship_destination("Gagazet")
    memory.main.click_to_control()
    memory.main.check_nea_armor()
    if game_vars.ne_armor() != 255:
        equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    else:
        memory.main.set_encounter_rate(0)
    
    #Teleporter pad.
    while not pathing.set_movement([54,107]):
        pass
    FFXC.set_neutral()
    approach_coords([70,120], click_through=False)
    FFXC.set_neutral()
    memory.main.wait_frames(90)
    xbox.menu_down()
    xbox.menu_down()
    xbox.tap_confirm()
    memory.main.click_to_control()
    
    # Up the mountain.
    path = [
        [-71,146],
        [-187,231],
        [-231,229]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    while memory.main.get_map() == 272:
        pathing.set_movement([-350,200])
    memory.main.click_to_control()
    
    # Flashback mountain!
    path = [
        [1044,-1076],
        [899,-1043],
        [854,-977],
        [776,-872],
        [787,-781],
        [802,-606],
        [834,-567]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    while memory.main.get_map() == 361:
        pathing.set_movement([880,-400])
    memory.main.click_to_control()
    
    # To the lookout
    path = [
        [-201,-602],
        [-172,-546]
    ]
    for i in range(len(path)):
        while not pathing.set_movement(path[i]):
            pass
    
    FFXC.set_neutral()
    # Showcase ends here.

    

def upgrade_engage(menu_id:int, force_end=False):
    for i in range(2):
        memory.main.wait_frames(15)
        while memory.main.save_menu_cursor() != menu_id:
            xbox.menu_down()
        xbox.menu_b()
        xbox.menu_b()
        if i % 2 == 1 and (menu_id==6 or force_end):
            memory.main.click_to_diag_progress(62)
            memory.main.wait_frames(15)
            xbox.menu_a()
            xbox.menu_b()
        else:
            memory.main.click_to_diag_progress(33)

def lulu_overdrive_test():
    # Assumes we are starting at the monster arena

    arena_npc()
    arena_menu_select(1)
    start_fight(area_index=13, monster_index=9)
    memory.main.wait_frames(1)
    battle.main.lulu_overdrive_demo(version="full")
    arena_menu_select(4)
