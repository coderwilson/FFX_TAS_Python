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

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def _distance(n1, n2):
    try:
        player1 = n1
        player2 = n2
        return abs(player1[1] - player2[1]) + abs(player1[0] - player2[0])
    except Exception as x:
        logger.exception(x)
        return 999


def movements(target, stutter: bool = False, buffer: int = 10):
    while _distance(get_coords(), target) > buffer:
        if memory.main.user_control():
            pathing.set_movement(target)
            if stutter:
                wait_frames(2)
                FFXC.set_neutral()
                wait_frames(3)
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle.main.flee_all()
            elif (
                memory.main.battle_wrap_up_active() or memory.main.diag_skip_possible()
            ):
                xbox.tap_b()
    FFXC.set_neutral()
    wait_frames(9)


def skip_prep():
    logger.info("Attempting MRR Skip")

    # Get near the spot, but out of the way of the runner.
    logger.info("Near but away from the runner")
    runner_index = actor_index(8323)
    while get_actor_coords(runner_index)[1] > get_coords()[1] - 100:
        target = [-20, -400]
        movements(target, buffer=2)
        if memory.main.diag_skip_possible():
            xbox.tap_b()
    logger.info("Runner seems in a good spot. Let's go.")

    target = [-18, -400]
    movements(target)
    logger.info("Moving to position.")

    target = [-14.7, -400]
    movements(target, stutter=True, buffer=0.5)
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
        while not part_1_done:
            runner_index = actor_index(8323)
            position = get_actor_coords(runner_index)
            tidus_coords = get_coords()

            if attempt and position[1] > tidus_coords[1] + 15:
                logger.debug(" - Runner too far. Wait for him to come back.")
                attempt = False
            if not attempt and position[1] < tidus_coords[1] - 15:
                logger.debug(" - Runner is lining up. Prepare for skip.")
                attempt = True
            if memory.main.battle_active():
                battle.main.flee_all()
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
                elif (
                    -380 > tidus_coords[1] > -400
                    and _distance(position, tidus_coords) < 60
                ):
                    part_1_done = True

        if memory.main.get_hp()[0] < 520:
            battle.main.heal_up()
            memory.main.update_formation(Tidus, Wakka, Auron)
        logger.info("First barrier passed.")
        # FFXC.set_movement(1,1)
        # wait_frames(60)
        # FFXC.set_neutral()
        # wait_frames(6)
        while not part_2_done:
            if get_coords()[1] != 0:
                runner_index = actor_index(8323)
                position = get_actor_coords(runner_index)
                tidus_coords = get_coords()
            if attempt and position[1] > tidus_coords[1] + 25:
                logger.debug(" - Runner too far. Wait for him to come back.")
                attempt = False
            if not attempt and position[1] < tidus_coords[1] - 15:
                logger.debug(" - Runner is lining up. Prepare for skip.")
                attempt = True
            if memory.main.battle_active():
                battle.main.flee_all()
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
    except Exception as e:
        logger.warning(e)


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
