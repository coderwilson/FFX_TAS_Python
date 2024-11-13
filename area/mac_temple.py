import logging

import battle.boss
import battle.main
import memory.main
import menu
import pathing
from pathing import approach_coords
import save_sphere
import screen
import vars
import xbox
import random
from paths import (
    MacalaniaTempleApproach,
    MacalaniaTempleEscape,
    MacalaniaTempleFoyer,
    MacalaniaTempleTrials,
    MacalaniaUnderTemple,
)
from players import Auron, Rikku, Tidus, Yuna

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def approach(do_grid=True):
    logger.debug("Affection array:")
    logger.debug(memory.main.affection_array())
    memory.main.click_to_control()
    logger.info("Approaching Macalania Temple")

    checkpoint = 0
    while memory.main.get_map() != 106:
        if memory.main.user_control():
            # Map changes
            if checkpoint < 2 and memory.main.get_map() == 153:
                checkpoint = 2

            # General pathing
            elif pathing.set_movement(MacalaniaTempleApproach.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
    FFXC.set_neutral()
    memory.main.await_control()
    if do_grid:
        menu.mac_temple()
    # save_sphere.touch_and_go()


def arrival():
    logger.info("Starting Macalania Temple section")

    # Movement:
    jyscal_skip_status = False
    checkpoint = 0
    skip_status = True
    touch_save = False
    while memory.main.get_map() != 80:
        if memory.main.user_control():
            # Main events
            if checkpoint == 1:
                checkpoint += 1
            elif checkpoint == 2 and not touch_save:
                touch_save = True
                save_sphere.touch_and_go()
            elif checkpoint == 2 and game_vars.csr():
                checkpoint = 11
            elif checkpoint == 4:  # Talking to Trommell
                memory.main.click_to_event_temple(6)
                if memory.main.get_coords()[0] < 23.5:
                    memory.main.wait_frames(30 * 0.07)
                    FFXC.set_movement(1, 0)
                    memory.main.wait_frames(2)
                    FFXC.set_neutral()
                    memory.main.wait_frames(4)
                checkpoint += 1
            elif checkpoint == 5:  # Skip (new)
                logger.info("Lining up for skip.")
                FFXC.set_movement(0, -1)
                memory.main.wait_frames(30 * 0.2)
                FFXC.set_neutral()
                while memory.main.get_coords()[1] < -101.5:
                    FFXC.set_value("d_pad", 8)
                    memory.main.wait_frames(2)
                    FFXC.set_value("d_pad", 0)
                    memory.main.wait_frames(5)

                logger.info("Turning back")
                memory.main.wait_frames(3)
                FFXC.set_movement(-1, 0)
                memory.main.wait_frames(2)
                FFXC.set_neutral()
                memory.main.wait_frames(15)

                logger.info("Now lined up. Here we go.")
                FFXC.set_movement(1, 0)
                memory.main.wait_frames(3)
                FFXC.set_value("btn_b", 1)
                memory.main.wait_frames(4)
                FFXC.set_value("btn_b", 0)
                memory.main.wait_frames(45)
                FFXC.set_neutral()
                checkpoint += 1
                memory.main.click_to_control_3()
            elif checkpoint == 6:
                checkpoint = 11
            elif checkpoint == 11:
                logger.info("Check if skip is online")
                if game_vars.csr():
                    jyscal_skip_status = True
                    checkpoint += 1
                elif memory.main.get_story_progress() < 1505:
                    jyscal_skip_status = True
                    checkpoint += 1
                else:
                    jyscal_skip_status = False
                    checkpoint = 20
                    skip_status = False
                logger.info(f"Jyscal Skip results: {skip_status}")
            elif checkpoint == 14 and game_vars.csr():
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 14:  # Pause so we don't mess up the skip
                if skip_status:
                    FFXC.set_neutral()
                    xbox.skip_dialog(5)
                    FFXC.set_movement(0, -1)
                    memory.main.await_event()
                    FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint < 16 and memory.main.get_map() == 239:
                checkpoint = 16

            # Recovery items
            elif checkpoint == 23:  # Door, Jyscal room
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 24:  # Back to the main room
                memory.main.click_to_event_temple(5)
                checkpoint += 1
            elif checkpoint == 27:
                checkpoint = 12

            # General pathing
            elif pathing.set_movement(MacalaniaTempleFoyer.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
    return jyscal_skip_status


def start_seymour_fight():
    memory.main.click_to_control()
    while not pathing.set_movement([9, -53]):
        pass  # Allows us to move to the Seymour fight.
    FFXC.set_movement(1, 0)
    memory.main.await_event()
    FFXC.set_neutral()


def seymour_fight():
    logger.info("Fighting Seymour Guado")
    battle.main.seymour_guado()
    if memory.main.game_over():
        return

    # Name for Shiva
    xbox.name_aeon("Shiva")

    memory.main.await_control()
    targets = [[6, -85], [2, -128], [2, -160]]

    checkpoint = 0
    while memory.main.get_map() == 80:
        if pathing.set_movement(targets[checkpoint]):
            checkpoint += 1

    FFXC.set_neutral()


def trials():
    logger.debug("Start of trials.")
    memory.main.await_control()
    # FFXC.set_movement(0,1)
    # memory.main.wait_frames(15)

    checkpoint = 0
    while memory.main.get_map() != 153:
        if memory.main.user_control():
            # CSR start point
            if checkpoint < 3 and game_vars.csr():
                checkpoint = 3

            # Map changes
            elif checkpoint < 2 and memory.main.get_map() == 239:
                checkpoint = 2

            # Spheres and Pedestals
            elif checkpoint == 2:
                memory.main.await_control()
                logger.info("Activate the trials")
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 9:  # Push pedestal - 1
                FFXC.set_movement(1, 0)
                memory.main.await_event()
                FFXC.set_neutral()
                memory.main.wait_frames(30 * 1)
                checkpoint += 1
            elif checkpoint == 13:  # Grab first Mac Sphere
                approach_coords([2,109])
                checkpoint += 1
            elif checkpoint == 17:  # Place first Mac Sphere
                approach_coords([34,48])
                checkpoint += 1
            elif checkpoint == 20:  # Push pedestal - 2
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 23:  # Grab glyph sphere
                approach_coords([1,10])
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
            elif checkpoint == 29:  # Push pedestal - 3
                FFXC.set_movement(1, 0)
                memory.main.await_event()
                FFXC.set_neutral()
                memory.main.wait_frames(30)
                checkpoint += 1
            elif checkpoint == 32:  # Place Glyph sphere
                approach_coords([-14,-53])
                checkpoint += 1
            elif checkpoint == 39:  # Grab second Mac sphere
                approach_coords([-24,-55])
                checkpoint += 1
            elif checkpoint == 46:  # Place second Mac sphere
                approach_coords([0,-34])
                checkpoint += 1
            elif checkpoint == 51:  # Grab third Mac sphere
                approach_coords([-80,59])
                checkpoint += 1
            elif checkpoint == 53:  # Place third Mac sphere
                approach_coords([1,10])
                checkpoint += 1
            elif checkpoint == 58:  # End of trials
                while memory.main.user_control():
                    if memory.main.get_actor_coords(0)[0] < -2:
                        FFXC.set_movement(0.5,1)
                    else:
                        FFXC.set_movement(0,1)
                memory.main.await_control()
                
                # Into/through foyer
                FFXC.set_movement(0,-1)
                memory.main.await_event()
                FFXC.set_neutral()

            # General pathing
            elif pathing.set_movement(MacalaniaTempleTrials.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()


def escape():
    while not memory.main.user_control():
        xbox.tap_b()
    
    logger.info("First, some menuing")
    menu_done = game_vars.get_blitz_win()
    if game_vars.nemesis():
        memory.main.update_formation(Tidus, Yuna, Auron, full_menu_close=False)
    else:
        menu.after_seymour()
        memory.main.update_formation(Tidus, Yuna, Rikku, full_menu_close=False)
    menu.equip_sonic_steel(full_menu_close=True)

    logger.info("Now to escape the Guado")
    chance = random.choice(range(0, 100))
    #if game_vars.rng_seed_num() == 139:
    #    chance = 1  # Testing where 139 does the extra battle.
    #else:
    #    chance = 99  # For now, don't use randomness.
    #if chance < 20 or not game_vars.get_blitz_win():
    #    force_battle = True
    #else:
    #    force_battle = False

    checkpoint = 0
    while memory.main.get_encounter_id() != 195:
        if memory.main.user_control():
            # Events
            if checkpoint == 2:
                save_sphere.touch_and_go()
                checkpoint += 1
                logger.debug(f"Touching save sphere. Update Checkpoint {checkpoint}")
            elif checkpoint == 18 and not menu_done:
                FFXC.set_neutral()

            # Map changes
            elif checkpoint < 19 and memory.main.get_map() == 192:
                checkpoint = 19
                logger.debug(f"Map change. Update Checkpoint {checkpoint}")

            # General pathing
            elif pathing.set_movement(MacalaniaTempleEscape.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                screen.await_turn()
                if not menu_done:
                    battle.main.mac_flee_xp()
                    if memory.main.get_tidus_slvl() >= 2:
                        menu.home_grid()
                        menu_done = True
                    memory.main.update_formation(Tidus, Yuna, Rikku)
                    memory.main.close_menu()
                elif memory.main.get_encounter_id() == 195:
                    break
                else:
                    battle.main.flee_all()
            elif memory.main.menu_open():
                xbox.tap_b()
            elif memory.main.diag_skip_possible():
                xbox.tap_b()

    logger.info("Done pathing. Now for the Wendigo fight.")
    
def attempt_wendigo():
    if battle.boss.wendigo():
        logger.info("Wendigo fight over")
        memory.main.click_to_control_dumb()
        return True
    else:
        logger.warning("Wendigo fight fail! Reset!")
        return False


def under_lake():
    memory.main.click_to_control()
    checkpoint = 0
    while memory.main.get_map() != 129:
        if memory.main.user_control():
            if checkpoint == 4:
                FFXC.set_movement(0, 1)
                memory.main.click_to_event()
                FFXC.set_neutral()
                memory.main.click_to_control()
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(2)
                memory.main.click_to_event()
                FFXC.set_neutral()
                memory.main.click_to_control()
                checkpoint += 1
            elif checkpoint == 11:
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 15:
                while memory.main.user_control():
                    pathing.set_movement([-4, -8])
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_control_3()
                checkpoint += 1

            # General pathing
            elif pathing.set_movement(MacalaniaUnderTemple.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
    FFXC.set_neutral()
    memory.main.click_to_control()


# TODO: This is unused, remove?
def under_lake_old():
    memory.main.click_to_control()
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 1)
    FFXC.set_movement(-1, 1)
    memory.main.wait_frames(30 * 0.8)
    FFXC.set_movement(1, 1)
    memory.main.wait_frames(30 * 1)
    FFXC.set_movement(0, 1)
    memory.main.click_to_event()
    FFXC.set_neutral()

    memory.main.click_to_control()
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 1.5)  # Approach Yuna
    FFXC.set_neutral()

    memory.main.click_to_control()
    while memory.main.get_coords()[1] > 110:
        FFXC.set_movement(-1, 1)
    while memory.main.get_coords()[1] > 85:
        FFXC.set_movement(1, 1)
    while memory.main.get_coords()[0] > -30:
        if memory.main.get_coords()[1] < 110:
            FFXC.set_movement(1, -1)
        else:
            FFXC.set_movement(1, 0)
    FFXC.set_movement(1, 0)
    memory.main.click_to_event()  # Chest with Lv.2 Key Sphere
    FFXC.set_neutral()
    xbox.skip_dialog(0.2)
    memory.main.click_to_control()
    FFXC.set_movement(-1, 0)
    memory.main.wait_frames(30 * 0.25)
    while memory.main.get_coords()[0] < -5:
        FFXC.set_movement(-1, 1)
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 1)  # To Auron
    xbox.skip_dialog(1.5)
    FFXC.set_movement(1, 0)
    xbox.skip_dialog(0.4)
    FFXC.set_movement(-1, 0)
    xbox.skip_dialog(0.4)
    FFXC.set_neutral()
    memory.main.click_to_control()

    while memory.main.get_map() != 129:
        FFXC.set_movement(0, -1)
        if memory.main.diag_skip_possible():
            xbox.tap_b()
        elif memory.main.cutscene_skip_possible():
            xbox.skip_scene()
    FFXC.set_neutral()
    memory.main.click_to_control()
