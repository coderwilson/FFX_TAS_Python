import logging
from typing import List

import battle.boss
import battle.main
import memory.main
import menu
import pathing
import save_sphere
import screen
import vars
import xbox
from battle import avina_memory
from paths import MacalaniaLake, MacalaniaWoods
from players import Auron, Kimahri, Lulu, Rikku, Tidus, Wakka, Yuna

logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def wait_for_rng2_weakness(valid_weakness: List[int]):
    prev_rng2_prediction = None
    while True:
        cur_next_rng2 = memory.main.get_next_rng2()
        if cur_next_rng2 == prev_rng2_prediction:
            continue
        prev_rng2_prediction = cur_next_rng2
        current_weakness = cur_next_rng2 % 4
        logger.manip(
            f"Next RNG2: {cur_next_rng2}, "
            + f"Valid Weakness: {valid_weakness}, "
            + f"Current Weakness: {current_weakness}"
        )
        if current_weakness in valid_weakness:
            logger.info("Weakness has lined up.")
            return


def calculate_possible_weaknesses() -> List[int]:
    items_contained = []
    for i, item_val in enumerate([27, 24, 30, 32]):
        if memory.main.get_use_items_slot(item_val) != 255:
            items_contained.append(i)
    return items_contained


def arrival(rikku_charged):
    # ML logic, this qualifies us as AI, right? Right?? Awwww :(
    battle_count = 0
    heal_array = []
    ml_heals = False
    try:
        records = avina_memory.retrieve_memory()
        logger.debug(records.keys())
        seed_str = str(memory.main.rng_seed())
        if seed_str in records.keys():
            if "macalania_heals" in records[seed_str].keys():
                for i in range(30):
                    if i in records[seed_str]["macalania_heals"]:
                        if records[seed_str]["macalania_heals"][i] == "True":
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

    logger.info("Arriving at Macalania Woods")
    memory.main.click_to_control()
    if ml_heals and 0 in heal_array:
        logger.warning("aVIna deciding if we need to heal.")
        battle.main.heal_up(full_menu_close=False)
    memory.main.update_formation(Tidus, Rikku, Auron)
    memory.main.close_menu()

    last_gil = 0  # for first chest
    checkpoint = 0
    while memory.main.get_map() != 221:  # All the way to O'aka
        if memory.main.user_control():
            # Events
            if checkpoint == 14:  # First chest
                if last_gil != memory.main.get_gil_value():
                    if last_gil == memory.main.get_gil_value() - 2000:
                        checkpoint += 1
                        logger.debug(
                            f"Chest obtained. Updating Checkpoint {checkpoint}"
                        )
                    else:
                        last_gil = memory.main.get_gil_value()
                else:
                    pathing.set_movement([-141,225])
                    xbox.tap_b()
            elif checkpoint == 59:
                logger.debug(f"Rikku Charge: {rikku_charged}")
                if not rikku_charged:
                    checkpoint -= 2
                else:  # All good to proceed
                    checkpoint += 1
            elif checkpoint == 60:
                logger.info("Waiting for RNG2 to sync up for Sphermiroph Weakness.")
                items_contained = calculate_possible_weaknesses()
                logger.manip(f"We currently can do: {items_contained}")
                FFXC.set_neutral()
                wait_for_rng2_weakness(items_contained)
                checkpoint += 1

            # Map changes
            elif checkpoint < 18 and memory.main.get_map() == 241:
                checkpoint = 18
            elif checkpoint < 40 and memory.main.get_map() == 242:
                checkpoint = 40

            # General pathing
            elif pathing.set_movement(MacalaniaWoods.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle_count += 1
                battle.main.m_woods()
                if memory.main.game_over():
                    seed_str = str(memory.main.rng_seed())
                    avina_memory.add_battle_to_memory(
                        seed=seed_str,
                        area="macalania_heals",
                        battle_num=battle_count - 1,
                    )
                    return False
                rikku_charged = memory.main.overdrive_state()[6] == 100
                memory.main.click_to_control()
                logger.info(
                    "Rikku charged" if rikku_charged else "Rikku is not charged."
                )
                if ml_heals:
                    logger.warning("aVIna deciding if we need to heal.")
                    if battle_count in heal_array:
                        battle.main.heal_up(full_menu_close=False)
                else:
                    party_hp = memory.main.get_hp()
                    if (
                        party_hp[0] < 450
                        or (party_hp[6] < 180 and not rikku_charged)
                        or party_hp[2] + party_hp[4] < 500
                    ):
                        battle.main.heal_up(full_menu_close=False)
                if rikku_charged:
                    memory.main.update_formation(Tidus, Wakka, Auron)
                else:
                    memory.main.update_formation(Tidus, Rikku, Auron)
                memory.main.close_menu()
                if checkpoint == 61:
                    checkpoint = 60
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
            elif checkpoint in [14,36]:  # First chest, then butterfly guy
                xbox.tap_confirm()

    # Save sphere
    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(2)
    memory.main.await_control()
    memory.main.wait_frames(1)
    save_sphere.touch_and_go()
    FFXC.set_neutral()
    return True


def lake_road():
    logger.info("Lake road")
    memory.main.await_control()
    while not pathing.set_movement([174, -96]):
        pass
    while not pathing.set_movement([138, -83]):
        pass
    while not pathing.set_movement([101, -82]):
        pass
    while memory.main.user_control():
        FFXC.set_movement(0, 1)
        xbox.tap_b()
    FFXC.set_neutral()
    menu.m_woods()  # Selling and buying, item sorting, etc
    memory.main.click_to_control()
    memory.main.update_formation(Tidus, Kimahri, Yuna)
    while not pathing.set_movement([101, -72]):
        pass

    while not memory.main.battle_active():
        if memory.main.user_control():
            map_val = memory.main.get_map()
            tidus_pos = memory.main.get_coords()
            if map_val == 221:
                if tidus_pos[0] > 35:
                    pathing.set_movement([33, -35])
                else:
                    pathing.set_movement([-4, 15])
            elif map_val == 248:
                if tidus_pos[0] < -131:
                    pathing.set_movement([-129, -343])
                elif tidus_pos[1] < -235:
                    pathing.set_movement([-49, -233])
                elif tidus_pos[1] < -95:
                    pathing.set_movement([-1, -93])
                else:
                    pathing.set_movement([-1, 100])
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_b()

    FFXC.set_neutral()  # Engage Spherimorph

    logger.info("Battle against the Spherimorph")
    battle.boss.spherimorph()
    logger.info("Battle is over.")
    if game_vars.story_mode():
        while not memory.main.battle_wrap_up_active():
            pass
        FFXC.set_confirm()
        while memory.main.battle_wrap_up_active():
            pass
        FFXC.release_confirm()
        while memory.main.get_story_progress() < 1455:
            pass
    memory.main.click_to_control_3()  # Jecht's memories
    logger.debug("Jecht should be done talking now.")


def lake_road_2():
    path = [
        [-6, 25],
        [-4, -50],
        [-45, -212],
        [-49, -245],
        [-145, -358],
        [-245,-450]
    ]

    checkpoint = 0
    story = memory.main.get_story_progress()
    logger.debug(f"Checkpoint initialized: {checkpoint} (story: {story})")
    auron_affection = memory.main.affection_array()[2]
    logger.manip(f"Auron affection initialized: {auron_affection}")
    actors_report = True
    last_dialog = memory.main.diag_progress_flag()
    while memory.main.get_map() != 221:
        if memory.main.user_control():
            auron_index = memory.main.actor_index(103)
            #auron_index = memory.main.actor_index(2)
            #auron_index = 3
            if memory.main.affection_array()[2] != auron_affection:
                #auron_affection = memory.main.affection_array()[2]
                logger.manip(f"Auron affection updated: {memory.main.affection_array()[2]}")
                logger.manip(memory.main.affection_array())
                auron_affection = memory.main.affection_array()[2]
            if (
                checkpoint == 5 and
                memory.main.affection_array()[2] == auron_affection  # and
                #memory.main.distance(auron_index) < 30
            ):
                logger.warning("Attempting to approach Auron.")
                while (
                    memory.main.get_map() != 221 and
                    memory.main.affection_array()[2] == auron_affection
                ):
                    FFXC.set_movement(-1,-1)
                    xbox.tap_confirm()
                #temp_coords = memory.main.get_actor_coords(auron_index)
                #tar_coords = [round(temp_coords[0],2),round(temp_coords[1],2)]
                #logger.debug(f"Approaching coords: {tar_coords}")
                #pathing.set_movement(tar_coords)
                #xbox.tap_confirm()
                logger.warning(f"Break {logger.manip(memory.main.affection_array())}")
            elif pathing.set_movement(path[checkpoint]):
                checkpoint += 1
                story = memory.main.get_story_progress()
                logger.debug(f"Checkpoint updated: {checkpoint} (story: {story})")
            if checkpoint == 5 and actors_report:
                memory.main.check_near_actors(False,super_coords=True,max_dist=2000)
                #memory.main.check_moving_actors()
                actors_report = False
        else:
            FFXC.set_neutral()
            if last_dialog != memory.main.diag_progress_flag():
                last_dialog = memory.main.diag_progress_flag()
                story_state = memory.main.get_story_progress()
                logger.debug(f"Dialog change: {last_dialog} (story: {story_state})")
            if game_vars.story_mode():
                if memory.main.diag_skip_possible() and last_dialog in [43,44]:
                    xbox.tap_confirm()
            else:
                xbox.tap_confirm()
    memory.main.await_control()
    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(2)
    memory.main.await_event()
    FFXC.set_neutral()


def lake_road_2_old():
    FFXC.set_movement(0, -1)
    if game_vars.csr():
        checkpoint = 0
        while checkpoint < 5:
            if checkpoint == 0:
                if pathing.set_movement():
                    checkpoint += 1
            elif checkpoint == 1:
                if pathing.set_movement():
                    checkpoint += 1
            elif checkpoint == 2:
                if pathing.set_movement():
                    checkpoint += 1
            elif checkpoint == 3:
                if pathing.set_movement():
                    checkpoint += 1
            else:
                if pathing.set_movement():
                    checkpoint += 1

    else:
        FFXC.set_movement(0, -1)
        memory.main.wait_frames(3)
        memory.main.await_event()
        FFXC.set_neutral()

        memory.main.click_to_control()  # Auron's musings.
        logger.debug(f"Affection (before): {memory.main.affection_array()}")
        memory.main.wait_frames(30 * 0.2)
        auron_affection = memory.main.affection_array()[2]
        # Make sure we get Auron affection
        while memory.main.affection_array()[2] == auron_affection:
            auron_coords = memory.main.get_actor_coords(3)
            pathing.set_movement(auron_coords)
            xbox.tap_b()
        logger.debug(f"Affection (after): {memory.main.affection_array()}")
    while memory.main.user_control():
        FFXC.set_movement(-1, -1)
    FFXC.set_neutral()

    memory.main.click_to_control()  # Last map in the woods
    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(2)
    memory.main.await_event()
    FFXC.set_neutral()


def lake():
    logger.info("Now to the frozen lake")
    if memory.main.get_hp()[3] < 1000:  # Otherwise we under-level Tidus off of Crawler
        battle.main.heal_up(full_menu_close=False)

    memory.main.update_formation(Tidus, Kimahri, Lulu, full_menu_close=False)
    menu.m_lake_grid()
    memory.main.await_control()

    logger.debug("Affection array:")
    logger.debug(memory.main.affection_array())

    checkpoint = 0
    while memory.main.get_encounter_id() != 194:
        if memory.main.user_control():
            if pathing.set_movement(MacalaniaLake.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active() and memory.main.get_encounter_id() != 194:
                battle.main.flee_all()
            elif memory.main.menu_open():
                xbox.tap_confirm()
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
    if game_vars.story_mode():
        memory.main.wait_seconds(12)
        xbox.tap_confirm()
    else:
        xbox.click_to_battle()
    battle.boss.crawler()


def after_crawler():
    logger.debug("Affection array")
    logger.debug(memory.main.affection_array())
    memory.main.click_to_control()
    while memory.main.get_map() != 153:
        pos = memory.main.get_coords()
        if memory.main.user_control():
            if pos[1] > ((2.94 * pos[0]) + 505.21):
                FFXC.set_movement(1, 1)
            elif pos[1] < ((2.59 * pos[0]) + 469.19):
                FFXC.set_movement(-1, 1)
            else:
                FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()

    memory.main.click_to_control()

    checkpoint = 0
    last_cp = 0
    while checkpoint != 100:
        if last_cp != checkpoint:
            logger.debug(f"Checkpoint {checkpoint}")
            last_cp = checkpoint
        pos = memory.main.get_coords()
        if checkpoint == 0:
            if pos[0] > 130:
                checkpoint = 10
            else:
                if pos[1] < ((1.99 * pos[0]) + 5):
                    FFXC.set_movement(-1, -1)
                else:
                    FFXC.set_movement(-1, 0)
        elif checkpoint == 10:
            if pos[0] > 450:
                checkpoint = 20
            else:
                if pos[1] > ((0.37 * pos[0]) + 240):
                    FFXC.set_movement(-1, 1)
                elif pos[1] > 385:
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(-1, 0)
        elif checkpoint == 20:
            if pos[0] > 690:
                checkpoint = 40
            else:
                if pos[1] > ((-0.65 * pos[0]) + 693):
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(-1, 0)
        elif checkpoint == 30:
            if pos[1] < 100:
                checkpoint = 40
            else:
                if pos[1] < ((-1.49 * pos[0]) + 1235):
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(-1, 0)
        elif checkpoint == 40:
            if memory.main.get_map() == 106:
                FFXC.set_neutral()
                checkpoint = 100
            else:
                if pos[0] > 815:
                    FFXC.set_movement(1, 1)
                elif pos[0] < 810:
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(0, 1)
    logger.info("End of Macalania Woods section. Next is temple section.")
