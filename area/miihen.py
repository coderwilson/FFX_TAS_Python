import logging

import battle.boss
import battle.main
import memory.main
import pathing
import save_sphere
import screen
import vars
import xbox
from battle import avina_memory
from paths import Miihen1, MiihenAgency, MiihenLowroad
from players import Auron, Kimahri, Tidus, Wakka

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def post_battle_logic(section: str = "highroad_heals", battle_num: int = 0):
    heal_array = []
    ml_heals = False
    try:
        records = avina_memory.retrieve_memory()
        logger.debug(records.keys())
        seed_str = str(memory.main.rng_seed())
        logger.manip(f"Seed: {seed_str}")
        if seed_str in records.keys():
            if section in records[seed_str].keys():
                for i in range(30):
                    if i in records[seed_str][section]:
                        if records[seed_str][section][i] == "True":
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

    memory.main.update_formation(Tidus, Wakka, Auron, full_menu_close=False)
    hp_check = memory.main.get_hp()
    logger.debug(f"HP check: {hp_check}")
    logger.debug(f"ML heals value: {ml_heals}")
    if ml_heals:
        logger.warning("aVIna deciding if we need to heal.")
        if battle_num in heal_array:
            battle.main.heal_up()
        else:
            logger.debug("No need to heal up. Moving onward.")
    elif 1 in memory.main.ambushes():
        battle.main.heal_up()
    else:
        logger.debug("No need to heal up. Moving onward.")
    memory.main.close_menu()


def arrival():
    logger.info("Waiting for Yuna/Tidus to stop laughing.")
    FFXC.set_movement(0, 1)
    memory.main.click_to_control()
    logger.info("Now onward to scenes and Mi'ihen skip. Good luck!")
    miihen_skip = False
    battle_count = 0

    checkpoint = 0
    while memory.main.get_map() != 120:
        if memory.main.user_control():
            # Miihen skip attempt
            if checkpoint > 3 and checkpoint < 11:
                if game_vars.csr():
                    # Only run this branch if CSR is online.
                    tidus_coords = memory.main.get_coords()
                    hunter_coords = memory.main.miihen_guy_coords()
                    hunter_distance = abs(tidus_coords[1] - hunter_coords[1]) + abs(
                        tidus_coords[0] - hunter_coords[0]
                    )

                    # Get spear
                    if memory.main.hunter_spear():
                        checkpoint = 11
                    elif hunter_distance < 200 or checkpoint in [6, 7, 8, 9, 10]:
                        pathing.set_movement(hunter_coords)
                        xbox.tap_b()

                    elif pathing.set_movement(Miihen1.execute(checkpoint)):
                        checkpoint += 1
                        logger.debug(f"Checkpoint {checkpoint}")

                else:
                    # Run this branch on a normal Any% run, no CSR
                    tidus_coords = memory.main.get_coords()
                    hunter_coords = memory.main.miihen_guy_coords()
                    if hunter_coords[1] < tidus_coords[1]:
                        checkpoint = 11
                        logger.debug("Late for Mi'ihen skip, forcing recovery.")
                    elif checkpoint == 6:
                        FFXC.set_neutral()
                        memory.main.wait_frames(9)
                        logger.debug("Updating checkpoint due to late skip.")
                        logger.debug(f"Checkpoint {checkpoint}")
                        checkpoint += 1
                    elif checkpoint == 7:
                        if memory.main.get_coords()[1] > 1356.5:  # Into position
                            if memory.main.get_coords()[0] < -44:
                                FFXC.set_movement(1, 0)
                                memory.main.wait_frames(30 * 0.06)
                                FFXC.set_neutral()
                                memory.main.wait_frames(30 * 0.09)
                            else:
                                checkpoint += 1
                                logger.debug("Close to the spot")
                            logger.debug(f"Coords: {memory.main.get_coords()}")
                        elif memory.main.get_coords()[0] < -43.5:  # Into position
                            FFXC.set_movement(1, 1)
                            memory.main.wait_frames(2)
                            FFXC.set_neutral()
                            memory.main.wait_frames(3)
                        else:
                            FFXC.set_movement(0, 1)
                            memory.main.wait_frames(2)
                            FFXC.set_neutral()
                            memory.main.wait_frames(3)
                    elif checkpoint == 8:
                        if memory.main.get_coords()[0] > -43.5:  # Into position
                            checkpoint += 1
                            logger.debug("Adjusting for horizontal position - complete")
                            logger.debug(f"Coords: {memory.main.get_coords()}")
                        else:
                            FFXC.set_movement(1, 0)
                            memory.main.wait_frames(2)
                            FFXC.set_neutral()
                            memory.main.wait_frames(3)
                    elif checkpoint == 9:
                        if memory.main.get_coords()[1] > 1358.5:  # Into position
                            checkpoint = 10
                            logger.debug("Stopped and ready for the skip.")
                            logger.debug(f"Coords: {memory.main.get_coords()}")
                        else:
                            FFXC.set_movement(0, 1)
                            memory.main.wait_frames(2)
                            FFXC.set_neutral()
                            memory.main.wait_frames(4)
                    elif checkpoint == 10:
                        # Spear guy's position when we start moving.
                        if memory.main.miihen_guy_coords()[1] < 1380:
                            logger.info("Skip engaging!!! Good luck!")
                            # Greater number for spear guy's position means we will start moving faster.
                            # Smaller number means moving later.
                            FFXC.set_movement(0, 1)
                            if game_vars.use_pause():
                                memory.main.wait_frames(2)
                            else:
                                memory.main.wait_frames(3)
                            # Walk into the guy mashing B (or X, or whatever the key is)
                            xbox.skip_dialog(0.3)
                            FFXC.set_neutral()  # Stop trying to move. (recommended by Crimson)
                            logger.debug("Starting special skipping.")
                            xbox.skip_dialog_special(3)  # Mash two buttons
                            logger.debug("End special skipping.")
                            logger.debug("Should now be able to see if it worked.")
                            # Don't move, avoiding a possible extra battle
                            memory.main.wait_frames(30 * 3.5)
                            memory.main.click_to_control_3()
                            logger.debug("Mark 1")
                            memory.main.wait_frames(30 * 1)
                            logger.debug("Mark 2")
                            try:
                                if (
                                    memory.main.lucille_miihen_coords()[1] > 1400
                                    and memory.main.user_control()
                                ):
                                    miihen_skip = True
                                else:
                                    memory.main.click_to_control_3()
                            except Exception:
                                miihen_skip = False
                            logger.debug(f"Skip successful: {miihen_skip}")
                            checkpoint += 1
                    elif pathing.set_movement(Miihen1.execute(checkpoint)):
                        checkpoint += 1
                        logger.debug(f"Checkpoint {checkpoint}")
            elif checkpoint == 11 and not memory.main.hunter_spear():
                pathing.set_movement(
                    [
                        memory.main.miihen_guy_coords()[0],
                        memory.main.miihen_guy_coords()[1],
                    ]
                )
                xbox.tap_b()

            # Map changes
            elif checkpoint < 15 and memory.main.get_map() == 120:
                checkpoint = 15
            # General pathing
            elif pathing.set_movement(Miihen1.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.turn_ready():
                if checkpoint < 4:  # Tutorial battle with Auron
                    while memory.main.battle_active():
                        if memory.main.turn_ready():
                            Tidus.attack()
                    FFXC.set_movement(0, 1)
                    while not memory.main.user_control():
                        xbox.tap_b()
                    post_battle_logic()
                    FFXC.set_neutral()
                elif checkpoint == 25 and not memory.main.battle_active():
                    # Shelinda dialog
                    FFXC.set_neutral()
                    xbox.tap_b()
                else:
                    FFXC.set_neutral()
                    logger.debug("Starting battle")
                    battle_count += 1
                    battle.main.miihen_road()
                    if memory.main.game_over():
                        seed_str = str(memory.main.rng_seed())
                        avina_memory.add_battle_to_memory(
                            seed=seed_str,
                            area="highroad_heals",
                            battle_num=battle_count - 1,
                        )
                        return [False, 0, False, False]
                    logger.debug("Battle complete")
                    post_battle_logic(battle_num=battle_count)

                # Kimahri manip
                next_crit_kim = memory.main.next_crit(
                    character=3, char_luck=18, enemy_luck=15
                )
                logger.debug(f"Next Kimahri crit: {next_crit_kim}")
            else:
                FFXC.set_movement(1, 1)
                if memory.main.menu_open():
                    FFXC.set_value("btn_b", 1)
                    memory.main.wait_frames(2)
                    FFXC.set_value("btn_b", 0)
                    memory.main.wait_frames(3)
                elif memory.main.diag_skip_possible():
                    FFXC.set_value("btn_b", 1)
                    memory.main.wait_frames(2)
                    FFXC.set_value("btn_b", 0)
                    memory.main.wait_frames(3)
    logger.debug(f"Mi'ihen skip status: {miihen_skip}")
    return [game_vars.self_destruct_get(), battle_count, True, miihen_skip]


def arrival_2(self_destruct, battle_count):
    logger.info("Start of the second map")
    checkpoint = 15
    while memory.main.get_map() != 171:
        if memory.main.user_control():
            # Map changes
            if checkpoint == 27:
                if memory.main.get_coords()[1] > 2810:
                    checkpoint += 1
                elif game_vars.csr():
                    checkpoint += 1
                else:
                    FFXC.set_neutral()
                    xbox.skip_dialog(1)
                    memory.main.click_to_control_3()
                    checkpoint += 1

            # General pathing
            elif pathing.set_movement(Miihen1.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                battle_count += 1
                if (
                    checkpoint == 27 and not memory.main.battle_active()
                ):  # Shelinda dialog
                    xbox.tap_b()
                else:
                    logger.debug("Starting battle")
                    battle.main.miihen_road()
                    if memory.main.game_over():
                        seed_str = str(memory.main.rng_seed())
                        avina_memory.add_battle_to_memory(
                            seed=seed_str,
                            area="highroad_heals",
                            battle_num=battle_count - 1,
                        )
                        return [False, 0, False, False]
                    logger.debug("Battle complete")
                    post_battle_logic()
            elif memory.main.menu_open():
                xbox.tap_b()
            elif memory.main.diag_skip_possible():  # Exclude during the Miihen skip.
                if checkpoint < 6 or checkpoint > 12:
                    xbox.tap_b()

            # Map changes
            elif checkpoint < 13 and memory.main.get_map() == 120:
                checkpoint = 13
            elif checkpoint < 20 and memory.main.get_map() == 127:
                checkpoint = 20
            elif checkpoint < 31 and memory.main.get_map() == 58:
                checkpoint = 31
    return [game_vars.self_destruct_get(), battle_count, True]


def mid_point():
    checkpoint = 0
    while memory.main.get_map() != 115:
        if memory.main.user_control():
            if memory.main.get_map() == 58:
                memory.main.update_formation(Tidus, Kimahri, Wakka)
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                FFXC.set_neutral()
            elif checkpoint in [2, 3]:
                checkpoint = 4
            elif checkpoint == 5:
                FFXC.set_movement(0, -1)
                memory.main.await_event()
                FFXC.set_neutral()
                checkpoint = 4
            elif pathing.set_movement(MiihenAgency.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
            elif memory.main.battle_active():
                FFXC.set_neutral()
                logger.info("Mi'ihen - ready for Chocobo Eater")
                battle.boss.chocobo_eater()
                logger.info("Mi'ihen - Chocobo Eater complete")


# Starts just after the save sphere.
def low_road(self_destruct, battle_count):
    checkpoint = 0
    post_battle_logic(battle_num=battle_count)
    while memory.main.get_map() != 79:
        if memory.main.user_control():
            # Utility stuff
            if checkpoint == 2:
                save_sphere.touch_and_go()
                checkpoint += 1
            elif checkpoint == 26 and not game_vars.self_destruct_get():
                checkpoint = 24
            elif checkpoint == 34:  # Talk to guard, then Seymour
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                FFXC.set_neutral()
                memory.main.wait_frames(30 * 0.2)
                memory.main.click_to_control()
                FFXC.set_movement(0, -1)
                memory.main.wait_frames(10)
                memory.main.await_event()
                FFXC.set_neutral()
                checkpoint += 1

            # Map changes
            elif checkpoint < 17 and memory.main.get_map() == 116:
                checkpoint = 17
            elif checkpoint < 28 and memory.main.get_map() == 59:
                checkpoint = 28

            # General pathing
            elif pathing.set_movement(MiihenLowroad.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
            elif checkpoint == 25:  # Shelinda dialog
                xbox.tap_b()
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                battle_count += 1
                logger.info("Starting battle")
                battle.main.miihen_road()
                if memory.main.game_over():
                    seed_str = str(memory.main.rng_seed())
                    avina_memory.add_battle_to_memory(
                        seed=seed_str,
                        area="highroad_heals",
                        battle_num=battle_count - 1,
                    )
                    return False
                logger.info("Battle complete")
                post_battle_logic(battle_num=battle_count)
            elif memory.main.menu_open():
                xbox.tap_b()
            elif memory.main.diag_skip_possible():
                if checkpoint < 6 or checkpoint > 12:
                    xbox.tap_b()
    # logs.write_stats('Miihen encounters:')
    # logs.write_stats(battle_count)
    return True
