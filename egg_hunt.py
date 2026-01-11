import logging
import time
from math import copysign, radians, cos, sin

import numpy as np

import battle.main
import logs
import memory.main
import xbox
import vars
game_vars = vars.vars_handle()
from players import Tidus, Rikku, Kimahri

logger = logging.getLogger(__name__)

def compute_escape_vector(player_pos, ice_array, target, avoidance_radius=15):
    def is_inside(pos, icicle):
        distance = np.linalg.norm(pos - np.array([icicle.x, icicle.y]))
        return distance < avoidance_radius

    if not any(is_inside(player_pos, icicle) for icicle in ice_array):
        return np.array([0.0, 0.0])

    angle = 0.0
    angle_increment = radians(10)
    radius = 0.0

    # Start expanding outward in concentric circles until a valid position is found
    for _ in range(100):
        radius += 2
        # Check multiple angles to find a valid position
        valid_positions = []
        for i in range(int(360 / 10)):
            theta = angle + i * angle_increment
            new_x = player_pos[0] + radius * cos(theta)
            new_y = player_pos[1] + radius * sin(theta)
            new_pos = [new_x, new_y]
            if not any(is_inside(new_pos, icicle) for icicle in ice_array):
                valid_positions.append(new_pos)

        # If we find multiple valid positions, choose one that is closest to our target so we still attempt to move forward
        if len(valid_positions) > 0 and target:
            min_dist = float('inf')
            closest = valid_positions[0]
            for position in valid_positions:
                distance = np.linalg.norm(target - np.array(position))
                if distance < min_dist:
                    min_dist = distance
                    closest = position
            return closest - player_pos


    return np.array([0.0, 0.0])


def under_level() -> bool:
    if game_vars.end_game_version() == 3:
        if memory.main.get_yuna_slvl() < 22:
            return True
    else:
        if memory.main.get_yuna_slvl() < 18:
            return True
    return False


def engage():
    FFXC = xbox.controller_handle()
    if under_level():
        memory.main.update_formation(Tidus, Rikku, Kimahri)
    logger.info("Start egg hunt")
    start_time = time.time()
    battle_count = 0
    looking_count = 0
    active_egg = 99
    target = [10, -10]
    target_egg = [0, 0]
    logger.info("Ready for movement.")
    while memory.main.get_story_progress() < 3251:
        looking_count += 1
        player = memory.main.get_coords()
        (forward, right) = memory.main.get_movement_vectors()

        player_pos = np.array(player)

        if memory.main.battle_active():
            if under_level():
                logger.info("Battle engaged - using impulse for levels.")
                battle.main.calm_impulse()
                memory.main.update_formation(Tidus, Rikku, Kimahri)
            else:
                logger.info("Battle engaged - using flee.")
                FFXC.set_neutral()
                battle.main.flee_all()
                battle_count += 1
        elif under_level():
            FFXC.set_neutral()
        else:
            egg_array = memory.main.build_eggs()
            ice_array = (
                memory.main.build_icicles()
            )
            if active_egg == 99:
                min_dist = float('inf')
                for marker in range(10):  # Only print active eggs/icicles
                    egg = egg_array[marker]
                    # find closest egg
                    if not egg.egg_picked and egg.egg_life > 5 and egg.egg_life != 150:
                        dist = np.linalg.norm(player_pos - np.array([egg.x, egg.y]))
                        if dist < min_dist:
                            active_egg = marker
                            target_egg = [egg.x, egg.y]
                            min_dist = dist
            elif egg_array[active_egg].egg_picked == 1:
                active_egg = 99
            elif egg_array[active_egg].egg_life == 150:
                active_egg = 99

            if active_egg == 99:  # Position to go to if we are stalling.
                target = [0, 0]
            else:
                target = target_egg

            escape_vector = compute_escape_vector(player_pos, ice_array, target, avoidance_radius=20)
            need_to_dodge = np.linalg.norm(escape_vector) > 0
            if need_to_dodge:
                # Prioritize avoidance over moving towards the target
                desired_movement_dir = escape_vector
                logger.debug("Avoiding icicles.")
            else:
                # Move towards the target
                desired_movement_dir = target - player_pos

            distance_to_target = np.linalg.norm(desired_movement_dir)
            if distance_to_target > 0:
                desired_movement_dir /= distance_to_target
            else:
                desired_movement_dir = np.array([0.0, 0.0])

            fX, fY = forward
            rX, rY = right

            Lx = fY * desired_movement_dir[0] + rY * desired_movement_dir[1]
            Ly = fX * desired_movement_dir[0] + rX * desired_movement_dir[1]

            max_input = max(abs(Lx), abs(Ly))
            if max_input > 0:
                Lx /= max_input
                Ly /= max_input

            try:
                FFXC.set_movement(Lx, Ly)
            except Exception:
                pass

            # Now if we're close, we want to slow down a bit.
            if (
                    active_egg != 99
                    and egg_array[active_egg].distance < 15
                    and egg_array[active_egg].egg_life < 150
                    and not need_to_dodge
            ):
                logger.debug(f"Stutter-step to egg. ")
                memory.main.wait_frames(7)
                FFXC.set_neutral()
            xbox.tap_b()
    end_time = time.time()
    logger.info("End egg hunt")
    FFXC.set_neutral()
    duration = end_time - start_time
    logger.info(f"Duration: {duration}")
    logger.info(f"Battle count: {battle_count}")
    while memory.main.get_map() != 325:
        if memory.main.battle_active():
            battle.main.flee_all()
    try:
        logs.write_stats("Egg hunt duration (seconds):")
        logs.write_stats(str(round(duration, 2)))
        logs.write_stats("Egg hunt battles:")
        logs.write_stats(str(battle_count))
    except Exception as E:
        logger.error("No log file.")
        logger.exception(E)