import logging
import math

import battle.main
import memory.main
import menu
import pathing
import save_sphere
import vars
import xbox
import random
from paths import BikanelDesert, BikanelHome
from players import Auron, Kimahri, Rikku, Tidus, Wakka, Lulu

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def check_spheres():
    logger.debug("Checking spheres")
    # Speed sphere stuff. Improve this later.
    need_speed = False
    if memory.main.get_speed() < 5:
        need_speed = True
        # Reprogram battle logic to throw some kind of grenades.

    # Same for Power spheres
    if game_vars.nemesis():
        if (
            memory.main.get_power() >= 28
            or (
                memory.main.get_speed() < 9
                and memory.main.get_power()
                >= (24 + math.ceil((9 - memory.main.get_speed()) / 2))
            )
            or (memory.main.get_speed() >= 9 and memory.main.get_power() >= 24)
        ):
            need_power = False
        else:
            need_power = True

    elif (
        memory.main.get_power() >= 19
        or (
            memory.main.get_speed() < 9
            and memory.main.get_power()
            >= (15 + math.ceil((9 - memory.main.get_speed()) / 2))
        )
        or (memory.main.get_speed() >= 9 and memory.main.get_power() >= 15)
    ):
        need_power = False
    else:
        need_power = True
    return need_speed, need_power


def desert():
    logger.info("Desert")
    memory.main.click_to_control()

    need_speed, need_power = check_spheres()
    # Logic for finding Teleport Spheres x2 (only chest in this area)
    tele_slot = memory.main.get_item_slot(98)
    if tele_slot == 255:
        tele_count = 0
    else:
        tele_count = memory.main.get_item_count_slot(tele_slot)

    charge_state = memory.main.overdrive_state()[6] == 100
    # Bomb cores, sleeping powders, smoke bombs, silence grenades
    steal_items = [0, 0, 0, 0]
    items_needed = 0
    chance = random.choice(range(0, 100))
    chance = 99  # For now, no randomness.
    if chance < 20:
        manip_drops = True
    else:
        manip_drops = False

    # Now to figure out how many items we need.
    steal_items = battle.main.update_steal_items_desert()
    items_needed = 7 - sum(steal_items)

    menu.equip_sonic_steel()
    memory.main.close_menu()

    checkpoint = 0
    first_format = False
    sandy1 = False
    while memory.main.get_map() != 130:
        if memory.main.user_control():
            # Map changes
            if checkpoint == 9:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 11 and len(memory.main.get_order_seven()) > 4:
                checkpoint += 1
            elif checkpoint < 39 and memory.main.get_map() == 137:
                checkpoint = 39
            elif checkpoint < 50 and memory.main.get_map() == 138:
                checkpoint = 50

            # Nemesis stuff
            elif checkpoint == 47 and game_vars.nemesis():
                checkpoint = 70
            elif checkpoint == 72:
                FFXC.set_neutral()
                memory.main.wait_frames(6)
                FFXC.set_movement(-1, 0)
                memory.main.wait_frames(4)
                FFXC.set_neutral()
                memory.main.wait_frames(6)
                if memory.main.user_control():
                    xbox.tap_b()
                    memory.main.wait_frames(2)
                    memory.main.click_to_control()
                    checkpoint += 1
            elif checkpoint == 74:
                FFXC.set_neutral()
                memory.main.wait_frames(6)
                FFXC.set_movement(-1, 0)
                memory.main.wait_frames(4)
                FFXC.set_neutral()
                memory.main.wait_frames(6)
                if memory.main.user_control():
                    xbox.tap_b()
                    memory.main.wait_frames(2)
                    memory.main.click_to_control()
                    checkpoint += 1
            elif checkpoint == 76:
                checkpoint = 48

            # Other events
            elif checkpoint == 2 or checkpoint == 24:  # Save sphere
                FFXC.set_neutral()
                memory.main.wait_frames(30 * 0.2)
                save_sphere.touch_and_go()
                checkpoint += 1
            elif checkpoint == 53:
                logger.info("Going for first Sandragora and chest")
                tele_slot = memory.main.get_item_slot(98)
                if tele_slot == 255 or tele_count == memory.main.get_item_count_slot(
                    tele_slot
                ):
                    pathing.set_movement([-44, 446])
                    xbox.tap_b()
                else:
                    checkpoint += 1
                    logger.debug(f"Checkpoint {checkpoint}")
            elif checkpoint == 12 and not first_format:
                first_format = True
                memory.main.update_formation(Tidus, Wakka, Lulu)

            # Sandragora skip logic
            elif checkpoint == 57:
                checkpoint += 1
            elif checkpoint == 60:
                if manip_drops:
                    FFXC.set_movement(-1, 1)
                    memory.main.await_event()
                    manip_drops = False
                    checkpoint -= 2
                elif memory.main.get_coords()[1] < 812:
                    # Dialing in. 810 works 95%, but was short once.
                    FFXC.set_movement(0, 1)
                else:
                    FFXC.set_neutral()
                    checkpoint += 1
            elif checkpoint == 61:
                if memory.main.get_coords()[1] < 810:
                    # Accidentally encountered Sandragora, must re-position.
                    checkpoint -= 2
                elif memory.main.get_coords()[1] < 840:
                    FFXC.set_neutral()
                else:
                    checkpoint += 1

            # After Sandy2 logic
            elif checkpoint == 64:
                if (
                    items_needed >= 1
                ):  # Cannot move on if we're short on throwable items
                    checkpoint -= 2
                elif need_speed:  # Cannot move on if we're short on speed spheres
                    checkpoint -= 2
                elif 1 in memory.main.ambushes() and Kimahri.overdrive_percent() < 100:
                    # Avoids game-over state on the second battle, new with Terra skip
                    checkpoint -= 2
                else:
                    checkpoint += 1

            # General pathing
            elif memory.main.user_control():
                if pathing.set_movement(BikanelDesert.execute(checkpoint)):
                    checkpoint += 1
                    logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not memory.main.battle_active():
                xbox.menu_b()
            if memory.main.battle_active():  # Lots of battle logic here.
                xbox.click_to_battle()
                if checkpoint < 7 and memory.main.get_encounter_id() == 197:
                    # First battle in desert
                    battle.main.zu()
                elif memory.main.get_encounter_id() == 234:  # Sandragora logic
                    logger.info("Sandragora fight")
                    if checkpoint < 55:
                        if not sandy1:
                            battle.main.sandragora(1)
                            sandy1 = True
                        else:
                            battle.main.flee_all()
                    else:
                        battle.main.sandragora(2)
                        checkpoint = 58
                else:
                    battle.main.bikanel_battle_logic(
                        [charge_state, need_speed, need_power, items_needed],
                        sandy_fight_complete=sandy1,
                    )

                # After-battle logic
                memory.main.click_to_control()
                # Come back to this. Could save some runs.
                # if 1 in memory.main.ambushes():
                #    menu.main.overworld_use_item()

                # First, check and update party format.
                if checkpoint > 10:
                    if checkpoint < 23 and checkpoint > 10:
                        memory.main.update_formation(Tidus, Wakka, Auron)
                    elif not charge_state:
                        memory.main.update_formation(Tidus, Auron, Rikku)
                    elif need_power:
                        memory.main.update_formation(Tidus, Auron, Rikku)
                    elif need_speed:
                        memory.main.update_formation(Tidus, Auron, Rikku)
                    elif items_needed >= 1:
                        memory.main.update_formation(Tidus, Auron, Rikku)
                    else:  # Catchall
                        memory.main.update_formation(Tidus, Wakka, Lulu)

                # Next, figure out how many items we need.
                steal_items = battle.main.update_steal_items_desert()
                logger.debug(f"Items status: {steal_items}")
                items_needed = 7 - sum(steal_items)

                # Finally, check for other factors and report to console.
                charge_state = memory.main.overdrive_state()[6] == 100
                need_speed, need_power = check_spheres()
                logger.debug("Flag statuses")
                logger.debug(f"Rikku is charged up: {charge_state}")
                logger.debug(f"Need more Speed spheres: {need_speed}")
                logger.debug(f"Need more Power spheres: {need_power}")
                logger.debug(f"Additional items needed before Home: {items_needed}")
                if checkpoint == 60:
                    checkpoint = 58
            elif memory.main.diag_skip_possible():
                xbox.tap_b()

    # Move to save sphere
    checkpoint = 0
    while checkpoint < 7:
        if pathing.set_movement(BikanelHome.execute(checkpoint)):
            checkpoint += 1
            logger.debug(f"Checkpoint {checkpoint}")


def find_summoners():
    logger.info("Desert complete. Starting Home section")
    if game_vars.get_blitz_win():
        menu.home_grid()
    learn_first_OD = False

    checkpoint = 7
    while memory.main.get_map() != 261:
        if memory.main.user_control():
            # events
            if checkpoint == 7:
                FFXC.set_neutral()
                save_sphere.touch_and_go()

                checkpoint += 1
            elif checkpoint < 12 and memory.main.get_map() == 276:
                checkpoint = 12
            elif checkpoint < 18 and memory.main.get_map() == 280:
                checkpoint = 19
            elif checkpoint < 25 and memory.main.get_coords()[0] < -100:
                checkpoint = 25
            elif checkpoint == 34:
                checkpoint = 60
            elif checkpoint == 63:
                memory.main.click_to_event_temple(6)
                checkpoint = 35
            # Bonus room
            elif checkpoint in [81, 82, 83] and memory.main.get_map() == 286:
                checkpoint = 84
            elif checkpoint == 86:
                FFXC.set_movement(0, 1)
                memory.main.click_to_event()
                FFXC.set_neutral()
                memory.main.wait_frames(15)
                xbox.tap_b()
                memory.main.wait_frames(15)
                xbox.tap_left()
                xbox.tap_left()
                xbox.tap_b()
                memory.main.wait_frames(15)
                xbox.tap_left()
                xbox.tap_left()
                xbox.tap_left()
                xbox.tap_left()
                xbox.tap_b()
                memory.main.wait_frames(15)
                xbox.tap_right()
                xbox.tap_right()
                xbox.tap_right()
                xbox.tap_right()
                xbox.tap_b()
                memory.main.click_to_control()
                FFXC.set_movement(1, -1)
                memory.main.await_event()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 88:
                checkpoint = 21
            elif checkpoint == 20:
                if game_vars.get_blitz_win():
                    checkpoint = 21
                else:
                    checkpoint = 81
            elif checkpoint in [24, 25] and 1 in memory.main.ambushes():
                checkpoint = 22
            elif checkpoint == 31 and not game_vars.csr():
                memory.main.click_to_event_temple(6)
                checkpoint += 1
            elif checkpoint == 39:
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 42:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 45:
                memory.main.click_to_event_temple(1)
                checkpoint += 1
            elif pathing.set_movement(BikanelHome.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                if memory.main.get_encounter_id() == 417:
                    logger.info("Home, battle 1")
                    battle.main.home_1()
                    memory.main.update_formation(Tidus, Auron, Lulu)
                elif memory.main.get_encounter_id() == 419:
                    if memory.main.get_map() == 280:
                        logger.info("Home, battle 2")
                        learn_first_OD = battle.main.home_2()
                        memory.main.update_formation(Tidus, Auron, Lulu)
                    else:
                        logger.info("Home, bonus battle for Blitz loss")
                        battle.main.home_3()
                elif memory.main.get_encounter_id() == 420:
                    logger.info("Home, final battle")
                    battle.main.home_4(learn_first_OD)
                    memory.main.update_formation(Tidus, Rikku, Kimahri)
                else:
                    logger.debug(f"Flee from battle: {memory.main.get_encounter_id()}")
                    battle.main.flee_all()
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()
    logger.info("Let's go get that airship!")
    FFXC.set_neutral()
    if not game_vars.csr():
        memory.main.click_to_diag_progress(27)
        while not memory.main.cutscene_skip_possible():
            xbox.tap_b()
        xbox.skip_scene()
        memory.main.click_to_diag_progress(105)
        memory.main.wait_frames(15)
        xbox.tap_b()
        memory.main.wait_frames(15)
        xbox.skip_scene()

    while not memory.main.user_control():
        if memory.main.diag_skip_possible():
            xbox.tap_b()
        elif memory.main.cutscene_skip_possible():
            xbox.skip_scene()
    logger.info("Airship is good to go. Now for Yuna.")
