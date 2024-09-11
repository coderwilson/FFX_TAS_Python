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


def _distance(n1, n2):
    try:
        player1 = n1
        player2 = n2
        return abs(player1[1] - player2[1]) + abs(player1[0] - player2[0])
    except Exception as x:
        logger.exception(x)
        return 999


def movements(target, stutter: bool = False, buffer: int = 10, report=False):
    while _distance(get_coords(), target) > buffer:
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


def skip_prep():
    logger.info("Attempting MRR Skip")
    memory.main.await_control()
    FFXC.set_movement(1, -1)
    memory.main.await_event()
    FFXC.set_neutral()
    memory.main.await_control()

    # Get near the spot, but out of the way of the runner.
    logger.info("Near but away from the runner")
    runner_index = actor_index(8323)
    while get_actor_coords(runner_index)[1] > get_coords()[1] - 100:
        target = [-20, -400]
        movements(target, buffer=2)
        if memory.main.diag_skip_possible():
            xbox.tap_b()
    logger.info("Runner seems in a good spot. Let's go.")

    align_complete = False
    while not align_complete:
        logger.info("Moving to position.")
        target = [-17.2, -400]
        if movements(target):
            logger.info("Stutter step to position.")
            target = [-14.7, -400]
            if movements(target, stutter=True, buffer=0.5):
                align_complete = True
            else:
                # If fail, move away and try again.
                movements([-22, -440])
        else:
            # If fail, move away and try again.
            movements([-22, -440])
    wait_frames(15)
    FFXC.set_movement(0, -1)
    wait_frames(1)
    FFXC.set_neutral()
    wait_frames(3)
    logger.info("In position.")

def attempt_skip():
    logger.info("Waiting for the guy to come back")
    part_1_done = False
    part_2_done = False
    attempt = True
    try:
        
        logger.info("It's possible to get stuck in this section.")
        logger.info("We will set a time limit of 600 seconds to get through this.")
        logger.info("If we exceed the limit, reset and try again.")
        start_time = time.time()
        # Max number of seconds that we will wait for the skip to occur.
        time_limit = 180
        max_time = start_time + time_limit
        last_count = 0

        while not part_1_done:
            # Time-related items and infinite loop protection
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
            runner_index = actor_index(8323)
            position = get_actor_coords(runner_index)
            #tidus_coords = get_coords()

            if attempt and position[1] > tidus_coords[1] + 15:
                logger.debug(" - Runner too far. Wait for him to come back.")
                attempt = False
            if not attempt and position[1] < tidus_coords[1] - 15:
                logger.debug(" - Runner is lining up. Prepare for skip.")
                attempt = True
            if memory.main.battle_active():
                battle.main.flee_all()
                if memory.main.game_over():
                    return False
                battle.main.wrap_up()
                if _distance(position, tidus_coords) >= 15:
                    if memory.main.get_hp()[0] < 520:
                        battle.main.heal_up()
                    memory.main.update_formation(Tidus, Wakka, Auron)
            elif (
                memory.main.diag_skip_possible() or memory.main.battle_wrap_up_active()
            ):
                xbox.tap_b()

            if attempt:
                if _distance(position, tidus_coords) < 15:
                    # Attempting skip / talking
                    FFXC.set_value("btn_b", 1)
                    wait_frames(1)
                    FFXC.set_value("btn_b", 0)
                    wait_frames(1)
            if (
                tidus_coords[1] > -398
                and _distance(position, tidus_coords) > 60
            ):
                part_1_done = True

        if memory.main.get_hp()[0] < 520:
            battle.main.heal_up()
            memory.main.update_formation(Tidus, Wakka, Auron)
        logger.info("First barrier passed.")
        
        '''
        logger.info("It's possible to get stuck in this section.")
        logger.info("We will set a time limit of 600 seconds to get through this.")
        logger.info("If we exceed the limit, reset and try again.")
        # Now to wait for the skip to happen, or 60 second maximum limit
        start_time = time.time()
        # Max number of seconds that we will wait for the skip to occur.
        time_limit = 600
        max_time = start_time + time_limit
        last_count = 0

        #while not movements([-10,-386], stutter=True, buffer=0.5, report=True):
        #    logger.debug("Let's try that again.")
        logger.debug("Now waiting for the runner to pass.")
        runner_index = actor_index(8323)
        position = get_actor_coords(runner_index)
        pos = memory.main.get_coords()
        if pos != [0,0]:
            tidus_coords = [round(pos[0],2),round(pos[1],2)]
        while position[1] < tidus_coords[1]:
            current_time = time.time()
            pos = memory.main.get_coords()
            if pos != [0,0]:
                tidus_coords = [round(pos[0],2),round(pos[1],2)]
            runner_index = actor_index(8323)
            position = get_actor_coords(runner_index)
            pos = memory.main.get_coords()
            if pos != [0,0]:
                tidus_coords = [round(pos[0],2),round(pos[1],2)]
            if int(current_time - start_time) > int(last_count):
                logger.debug(f"Wait incrementer: {int(current_time - start_time)} - Coords: {tidus_coords}")
                last_count = int(current_time - start_time)

        '''
        attempt = True

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
                logger.debug(f"Wait incrementer: {int(current_time - start_time)} - Coords: {tidus_coords}")
                last_count = int(current_time - start_time)
            
            # Skip logic
            if get_coords()[1] != 0:
                runner_index = actor_index(8323)
                position = get_actor_coords(runner_index)
                #tidus_coords = get_coords()
            #if not attempt and position[1] < tidus_coords[1] - 15:
            #    logger.debug(" - Runner is lining up. Prepare for skip.")
            #    attempt = True
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

            elif attempt:
                if tidus_coords[1] > -360:
                    part_2_done = True
                    logger.info("Part 2 complete, we should be able to continue.")
                elif _distance(position, tidus_coords) < 15:
                    # Attempting skip / talking
                    FFXC.set_value("btn_b", 1)
                    wait_frames(1)
                    FFXC.set_value("btn_b", 0)
                    wait_frames(1)
                else:
                    target = [-17, -380.2]
                    if _distance(tidus_coords, target) > 2:
                        movements(target, stutter=True, buffer=0.5)
                        FFXC.set_movement(-1, -1)
                        wait_frames(1)
                        FFXC.set_neutral()
                        wait_frames(3)
                        logger.info("In position.")

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
