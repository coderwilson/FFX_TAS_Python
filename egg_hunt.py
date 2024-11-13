import logging
import time
from math import copysign, radians, cos, sin

import numpy as np

import battle.main
import logs
import memory.main
import xbox

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




def engage():
    FFXC = xbox.controller_handle()
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
            logger.info("Battle engaged - using flee.")
            FFXC.set_neutral()
            battle.main.flee_all()
            battle_count += 1
        else:
            egg_array = memory.main.build_eggs()
            ice_array = (
                memory.main.build_icicles()
            )
            if active_egg == 99:
                for marker in range(10):  # Only print active eggs/icicles
                    if (
                        active_egg == 99
                        and egg_array[marker].go_for_egg
                        and egg_array[marker].egg_life < 150
                    ):
                        active_egg = marker
                        target = [egg_array[marker].x, egg_array[marker].y]
                        # We will hunt for this egg for this many seconds.
            elif not egg_array[active_egg].go_for_egg:
                active_egg = 99
            elif egg_array[active_egg].egg_life == 150:
                active_egg = 99

            if active_egg == 99:  # Positions to go to if we are stalling.
                loop_break = 0
                while (
                    active_egg == 99 and memory.main.user_control() and loop_break < 100
                ):
                    if checkpoint == 0:
                        target = [-50, -50]
                    elif checkpoint == 1:
                        target = [50, -50]
                    elif checkpoint == 2:
                        target = [50, 50]
                    elif checkpoint >= 3:
                        target = [-50, 50]
                    elif checkpoint >= 4:
                        checkpoint = 0
                    if check_icicle_distances(target, ice_array):
                        active_egg = 100  # just to break loop
                    else:
                        checkpoint += 1
                    loop_break += 1
            if active_egg == 100:
                active_egg = 99  # Put it back after breaking the loop.

            # And now the code to move to the target.
            old_target = target
            player = memory.main.get_coords()
            ice_array = memory.main.build_icicles()
            (forward, right) = memory.main.get_movement_vectors()

            target_pos = np.array([target[0], target[1]])
            player_pos = np.array(player)

            closest_intersect = 9999
            intersect_point = []
            for icicle in ice_array:
                num_intersect, hits = line_sphere_intersect(
                    player_pos, target_pos, np.array([icicle.x, icicle.y])
                )
                if num_intersect > 0:
                    intersect_distance = (player[0] - hits[0][0]) ** 2 + (
                        player[1] - hits[0][1]
                    ) ** 2
                    if intersect_distance < closest_intersect:
                        closest_intersect = intersect_distance
                        intersect_point = hits[0]

            if closest_intersect < 9999:
                # Move around icicle instead
                target = path_around(player_pos, np.array(intersect_point), target_pos)

            # Calculate forward and right directions relative to camera space
            pX = player[0]
            pY = player[1]
            eX = target[0]
            eY = target[1]
            fX = forward[0]
            fY = forward[1]
            rX = right[0]
            rY = right[1]

            Ly = fX * (eX - pX) + rX * (eY - pY)
            Lx = fY * (eX - pX) + rY * (eY - pY)
            sums_up = abs(Lx) + abs(Ly)
            if sums_up == 0:
                sums_up = 0.01
            Lx /= sums_up
            Ly /= sums_up
            if abs(Lx) > abs(Ly):
                Ly = copysign(Ly / Lx if Lx else 0, Ly)
                Lx = copysign(1, Lx)
            elif abs(Ly) > abs(Lx):
                Lx = copysign(Lx / Ly if Ly else 0, Lx)
                Ly = copysign(1, Ly)

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