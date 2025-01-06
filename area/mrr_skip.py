import logging

import battle.main
from battle import avina_memory
import memory.main
from memory.main import wait_frames, actor_index, get_actor_coords, get_coords
import pathing
from paths import MRRSkip
import vars
import xbox
from players import Auron, Kimahri, Tidus, Wakka
import time

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()
import time


def remaining_time(max:int=99, current:int=99, coords=[]):
    if len(coords) >= 2:
        logger.debug(f"Soft lock check: {int(max - current)} seconds to reset - Coords: {coords}")
    else:
        logger.manip(f"Encounter distance: {memory.main.distance_to_encounter()}")


def _distance(n1, n2):
    try:
        player1 = n1
        player2 = n2
        return abs(player1[1] - player2[1]) + abs(player1[0] - player2[0])
    except Exception as x:
        logger.exception(x)
        return 999


def movements(target, stutter: bool = False, buffer: int = 10, report=False):
    start_time = time.time()
    max_time = start_time + 15
    pos = memory.main.get_coords()
    tidus_coords = [round(pos[0],2),round(pos[1],2)]
    # Max number of seconds that we will wait for the skip to occur.
    last_count = 0
    while _distance(get_coords(), target) > buffer:
        # Time-related items and infinite loop protection
        current_time = time.time()
        pos = memory.main.get_coords()
        if pos != [0,0]:
            tidus_coords = [round(pos[0],2),round(pos[1],2)]
        if current_time > max_time:
            logger.warning("Skip seemingly failed. Resetting.")
            return False
        elif int(current_time - start_time) > int(last_count):
            remaining_time(max=max_time, current = current_time, coords=tidus_coords)
            #logger.debug(f"Wait incrementer: {int(current_time - start_time)} - Coords: {tidus_coords}")
            last_count = int(current_time - start_time)
        
        if memory.main.user_control():
            pathing.set_movement(target)
            if stutter:
                if report:
                    logger.debug(get_coords())
                wait_frames(2)
                FFXC.set_neutral()
                wait_frames(3)
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle.main.flee_all()
                battle.main.wrap_up()
                return False
    FFXC.set_neutral()
    wait_frames(9)
    return True


def loop_back(checkpoint = 0):
    if memory.main.get_map() == 92:
        logger.info("CSR mode, looping back.")
        memory.main.await_control()
        FFXC.set_movement(1, -1)
        memory.main.await_event()
        FFXC.set_neutral()
        memory.main.await_control()
    remaining_time()

    next_enc_dist = memory.main.distance_to_encounter()
    force_enc = next_enc_dist < 295
    path = [
        [-169,-446],
        [-130,-466],
        [-112,-466],
        [-86,-465],
        [-52,-457],
        [-28,-445],
        [-18, -418]
    ]
    while checkpoint < len(path):
        if memory.main.user_control():
            if pathing.set_movement(path[checkpoint]):
                checkpoint += 1
        elif memory.main.battle_active():
            FFXC.set_neutral()
            force_enc = False
            battle.main.flee_all()
            if memory.main.game_over():
                return False
            battle.main.wrap_up()
    logger.debug("Loop back function complete.")
    return force_enc


def past_clasko():
    # This is the non-CSR logic, but really we just leverage the same logic.
    loop_back(checkpoint=5)


def align_1_side():
    target = [-19, -400]
    if movements(target, stutter=True, buffer=0.5):
        return True
    return False

def align_1_ready():
    logger.info("Stutter step to position.")
    target = [-14.7, -400.1]
    if movements(target, stutter=True, buffer=0.3):
        wait_frames(15)
        #FFXC.set_movement(1, 0)
        FFXC.set_movement(0, -1)
        wait_frames(1)
        FFXC.set_neutral()
        wait_frames(3)
        logger.info("In position.")
        return True
    return False


def force_battle():
    logger.warning("Forcing extra battle for skip consistency!")
    path = [
        [-24, -405],
        [-12, -405],
    ]
    ptr = 0
    while not memory.main.battle_active():
        if pathing.set_movement(path[ptr%2]):
            ptr += 1
    battle.main.flee_all()
    if memory.main.game_over():
        return False
    battle.main.wrap_up()


def skip_prep():
    if memory.main.get_map() == 92 or memory.main.get_coords()[0] < -120:
        # CSR logic
        if loop_back():
            # Force encounter so we don't have to deal with it mid-attempt.
            force_battle()
        align_1_side()
    elif memory.main.get_coords()[1] < -490:
        # any% logic
        past_clasko()
        align_1_side()

def attempt_skip():
    logger.info("Waiting for the guy to come back")
    part_1_done = False
    part_2_done = False
    attempt = 0
    try:
        logger.info("It's possible to get stuck in this section.")
        logger.info("We will set a time limit to get through this.")
        logger.info("If we exceed the limit, reset and try again.")
        start_time = time.time()
        # Max number of seconds that we will wait for the skip to occur.
        if game_vars.csr():
            time_limit = 115
        else:
            time_limit = 155
        max_time = start_time + time_limit
        last_count = 0

        while not part_1_done:
            # Time-related items and infinite loop protection
            current_time = time.time()
            tidus_coords = get_coords()
            pos = memory.main.get_coords()
            if pos != [0,0]:
                tidus_coords = [round(pos[0],2),round(pos[1],2)]
            if current_time > max_time:
                logger.warning("Skip seemingly failed. Resetting.")
                return False
            elif int(current_time - start_time) > int(last_count):
                remaining_time(max=max_time, current = current_time, coords=tidus_coords)
                #logger.debug(f"Wait incrementer: {int(current_time - start_time)} - Coords: {tidus_coords}")
                last_count = int(current_time - start_time)
            
            # Skip logic
            runner_index = actor_index(8323)
            position = get_actor_coords(runner_index)

            if memory.main.battle_active():
                battle.main.flee_all()
                if memory.main.game_over():
                    return False
                battle.main.wrap_up()
                if _distance(position, tidus_coords) >= 15:
                    if memory.main.get_hp()[0] < 520:
                        battle.main.heal_up()
                    memory.main.update_formation(Tidus, Wakka, Auron)
            if (
                memory.main.get_map() == 92 or
                memory.main.get_coords()[0] < -120 or
                memory.main.get_coords()[1] < -490
            ):
                skip_prep()
            elif _distance(position, tidus_coords) < 15:
                if attempt % 2 == 1 and tidus_coords[1] < -390:
                    # Attempting skip / talking
                    FFXC.set_confirm()
                    wait_frames(1)
                    FFXC.release_confirm()
                    wait_frames(1)
            elif tidus_coords[1] > -398 and tidus_coords[1] != 0:
                if _distance(position, tidus_coords) > 15:
                    part_1_done = True
                    attempt += 1
            elif attempt % 2 == 1 and position[1] > tidus_coords[1] + 15:
                logger.debug(" - Runner too far North. Wait for him to come back.")
                align_1_side()  # Resets us to starting position.
                attempt += 1
            elif attempt % 2 == 0 and position[1] < tidus_coords[1] - 20:
                logger.debug(" - Runner is lining up. Prepare for skip.")
                align_1_ready()
                attempt += 1
            elif (
                    memory.main.diag_skip_possible() or memory.main.battle_wrap_up_active()
                ):
                    xbox.tap_b()

        if memory.main.get_hp()[0] < 520:
            battle.main.heal_up()
            memory.main.update_formation(Tidus, Wakka, Auron)
        logger.info("First barrier passed.")
        attempt += 1
        
        while not part_2_done:
            # Time-related items and infinite loop protection
            current_time = time.time()
            pos = memory.main.get_coords()
            if pos != [0,0]:
                tidus_coords = [round(pos[0],2),round(pos[1],2)]
            if current_time > max_time:
                logger.warning("Skip seemingly failed. Resetting.")
                return False
            elif int(current_time - start_time) > int(last_count):
                remaining_time(max=max_time, current = current_time, coords=tidus_coords)
                #logger.debug(f"Wait incrementer: {int(current_time - start_time)} - Coords: {tidus_coords}")
                last_count = int(current_time - start_time)
            
            # Skip logic
            runner_index = actor_index(8323)
            position = get_actor_coords(runner_index)

            if memory.main.battle_active():
                battle.main.flee_all()
                if memory.main.game_over():
                    return False
                battle.main.wrap_up()
                if _distance(position, tidus_coords) >= 15:
                    if memory.main.get_hp()[0] < 520:
                        battle.main.heal_up()
                    memory.main.update_formation(Tidus, Wakka, Auron)
            target = [-16.8, -380.2]
            if tidus_coords[1] > -360:
                #if _distance(position, tidus_coords) > 15:
                part_2_done = True
                attempt += 1
            elif _distance(position, tidus_coords) < 15:
                if attempt % 2 == 1:
                    # Attempting skip / talking
                    FFXC.set_confirm()
                    wait_frames(1)
                    FFXC.release_confirm()
                    wait_frames(1)
            elif attempt % 2 == 1 and position[1] > tidus_coords[1] + 15:
                logger.debug(" - Runner too far North. Wait for him to come back.")
                attempt += 1
            elif attempt % 2 == 0 and position[1] < tidus_coords[1] - 20:
                logger.debug(" - Runner is lining up. Prepare for skip.")
                attempt += 1
            elif attempt % 2 == 0 and _distance(tidus_coords, target) > 5:
                if not movements(target, stutter=True, buffer=0.5):
                    if memory.main.game_over():
                        return False
                else:
                    wait_frames(15)
                    FFXC.set_movement(-1, -1)
                    wait_frames(1)
                    FFXC.set_neutral()
                    wait_frames(3)
            elif (
                    memory.main.diag_skip_possible() or memory.main.battle_wrap_up_active()
                ):
                    xbox.tap_b()

            '''
            current_time = time.time()
            pos = memory.main.get_coords()
            if pos != [0,0]:
                tidus_coords = [round(pos[0],2),round(pos[1],2)]
            if current_time > max_time:
                logger.warning("Skip seemingly failed. Resetting.")
                return False
            elif int(current_time - start_time) > int(last_count):
                logger.debug(f"Wait incrementer: {int(current_time - start_time)} - Coords: {tidus_coords}")
                last_count = int(current_time - start_time)
            
            # Skip logic
            if get_coords()[1] != 0:
                runner_index = actor_index(8323)
                position = get_actor_coords(runner_index)
            if memory.main.battle_active():
                battle.main.flee_all()
                if memory.main.game_over():
                    return False
                battle.main.wrap_up()
                if _distance(position, tidus_coords) >= 15:
                    if memory.main.get_hp()[0] < 520:
                        battle.main.heal_up()
                    memory.main.update_formation(Tidus, Wakka, Auron)
            elif memory.main.diag_skip_possible():
                xbox.tap_b()

            target = [-17, -380.2]
            if attempt % 2 == 1 and position[1] > tidus_coords[1] + 15:
                logger.debug(" - Runner too far North. Wait for him to come back.")
                attempt += 1
            elif attempt % 2 == 0 and position[1] < tidus_coords[1] - 20:
                logger.debug(" - Runner is lining up. Prepare for skip.")
                attempt += 1
            if tidus_coords[1] > -360:
                part_2_done = True
                logger.info("Part 2 complete, we should be able to continue.")
            elif attempt % 2 == 1 and _distance(position, tidus_coords) < 10:
                # Attempting skip / talking
                FFXC.set_confirm()
                wait_frames(1)
                FFXC.release_confirm()
                wait_frames(1)
            elif (
                tidus_coords[1] < -355 and
                tidus_coords[1] < -397 and
                tidus_coords[0] < -18.5
            ):
                # This should not trigger during the push.
                logger.warning("Push failed, returning for (hopefully) a reattempt.")
                FFXC.set_neutral()
                return False
            elif attempt % 2 == 0 and _distance(tidus_coords, target) > 20:
                movements(target, stutter=True, buffer=0.5, report=True)
                FFXC.set_movement(-1, -1)
                wait_frames(1)
                FFXC.set_neutral()
                wait_frames(3)
                logger.info("In position.")
            '''

        FFXC.set_neutral()
        if memory.main.get_hp()[0] < 520 or 1 in memory.main.ambushes():
            battle.main.heal_up()
        memory.main.update_formation(Tidus, Kimahri, Auron)
        logger.info("Success!")
        return True
    except Exception as e:
        logger.warning(e)
        return False


def advance_to_aftermath():
    logger.info("Now to escape this area")
    checkpoint = 0
    battle_num = 0
    heal_array = []
    ml_heals = False
    try:
        records = avina_memory.retrieve_memory()
        logger.debug(records.keys())
        seed_str = str(memory.main.rng_seed())
        if seed_str in records.keys():
            if "mrr_heals" in records[seed_str].keys():
                for i in range(30):
                    if i in records[seed_str]["mrr_heals"]:
                        if records[seed_str]["mrr_heals"][i] == "True":
                            heal_array.append(i)
            else:
                logger.info("I have no memory of this seed. (A)")
            if "ml_heals" in records[seed_str].keys():
                if records[seed_str]["ml_heals"] == "True":
                    ml_heals = True
        else:
            logger.info("I have no memory of this seed. (B)")
    except Exception:
        logger.info("I have no memory of this seed. (C)")
    if 0 in heal_array:
        battle.main.heal_up()
    while memory.main.get_map() != 131:
        if memory.main.user_control():
            if pathing.set_movement(MRRSkip.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle_num += 1
                logger.debug(f"Battle Start: {battle_num}")
                while not memory.main.turn_ready():
                    pass
                if memory.main.game_over():
                    avina_memory.add_battle_to_memory(
                        seed=seed_str, area="mrr_heals", key=battle_num - 1
                    )
                    return False
                battle.main.flee_all()
                battle.main.wrap_up()
                if not ml_heals:
                    if memory.main.get_hp()[0] < 520 or 1 in memory.main.ambushes():
                        battle.main.heal_up()
                else:
                    if battle_num in heal_array:
                        battle.main.heal_up()
                memory.main.update_formation(Tidus, Wakka, Auron)
            elif memory.main.diag_skip_possible():
                xbox.tap_b()
    return True
