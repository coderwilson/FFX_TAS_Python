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
    BikanelDesert,
)
from players import Auron, Rikku, Tidus, Yuna, CurrentPlayer

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
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
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
            elif checkpoint == 2 and game_vars.story_mode():
                checkpoint = 20
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
                FFXC.set_confirm()
                memory.main.wait_frames(4)
                FFXC.release_confirm()
                memory.main.wait_frames(45)
                FFXC.set_neutral()
                checkpoint += 1
                memory.main.click_to_control_3()
            elif checkpoint == 6 and not game_vars.story_mode():
                checkpoint = 11
            elif checkpoint == 11:
                logger.info("Check if skip is online")
                if game_vars.story_mode():
                    jyscal_skip_status = False
                    checkpoint = 20
                    skip_status = False
                elif game_vars.csr():
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
            elif checkpoint == 14:
                if not game_vars.csr():
                    FFXC.set_neutral()
                    xbox.skip_dialog(5)
                pathing.approach_coords([-1,160],click_through=not game_vars.story_mode())
                FFXC.set_neutral()
                memory.main.click_to_control()
                checkpoint += 1
            elif checkpoint < 16 and memory.main.get_map() == 239:
                checkpoint = 16

            # Recovery items
            elif checkpoint == 23:  # Door, Jyscal room
                memory.main.click_to_event_temple(0,story_mode_dialog=True)
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
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
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
    if not battle.main.seymour_guado():
        return False

    # Name for Shiva
    xbox.name_aeon("Shiva")

    memory.main.await_control()
    targets = [[6, -85], [2, -128], [2, -160]]

    checkpoint = 0
    while memory.main.get_map() == 80:
        if pathing.set_movement(targets[checkpoint]):
            checkpoint += 1

    FFXC.set_neutral()
    return True


def trials(destro=False):
    logger.debug("Start of trials.")
    memory.main.await_control()
    # FFXC.set_movement(0,1)
    # memory.main.wait_frames(15)
    if game_vars.story_mode() or game_vars.platinum():
        destro = True

    if destro or game_vars.csr():
        checkpoint = 3
    else:
        checkpoint = 0
    last_checkpoint = checkpoint
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
                if destro:
                    checkpoint += 1
                else:
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
            
            # Destro sphere section
            elif checkpoint == 61:
                approach_coords([-14,-116])
                memory.main.click_to_control()
                while memory.main.user_control():
                    FFXC.set_movement(-1,0)
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 68:
                approach_coords([0,109])
                memory.main.click_to_control()
                checkpoint += 1
            elif checkpoint == 75:
                FFXC.set_movement(1, 0)
                memory.main.await_event()
                FFXC.set_neutral()
                memory.main.wait_frames(30 * 1)
                checkpoint += 1
            elif checkpoint == 78:
                approach_coords([0,109])
                memory.main.click_to_control()
                checkpoint += 1
            elif checkpoint == 81:
                approach_coords([-80,59])
                checkpoint += 1
            elif checkpoint == 85:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 90:
                approach_coords([0,8])
                checkpoint += 1
            elif checkpoint == 92:
                approach_coords([-13,-16])
                checkpoint += 1
            elif checkpoint == 96:
                memory.main.check_near_actors(False)
                pathing.approach_actor_by_id(20482)
                memory.main.click_to_control()
                checkpoint += 1
            elif checkpoint == 106:
                approach_coords([1,7])
                checkpoint += 1
            elif checkpoint == 113:
                approach_coords([1,7])
                FFXC.set_neutral()
                memory.main.click_to_control()
                FFXC.set_movement(1, 0)
                memory.main.await_event()
                FFXC.set_neutral()
                memory.main.wait_frames(30)
                checkpoint += 1
            elif checkpoint == 117:
                approach_coords([-80,59])
                checkpoint += 1
            elif checkpoint == 120:
                approach_coords([1,7])
                checkpoint += 1
            elif checkpoint == 125:  # End of trials
                while memory.main.user_control():
                    if memory.main.get_actor_coords(0)[0] < -2:
                        FFXC.set_movement(0.5,1)
                    else:
                        FFXC.set_movement(0,1)
                memory.main.await_control()
                return

            # General pathing
            elif pathing.set_movement(MacalaniaTempleTrials.execute(checkpoint)):
                checkpoint += 1
            
            if last_checkpoint != checkpoint:
                logger.debug(f"Checkpoint: {checkpoint}")
                last_checkpoint = checkpoint
        else:
            FFXC.set_neutral()


def escape(dark_aeon:bool = False) -> bool:
    memory.main.click_to_control()

    # Foyer room can be a problem.
    if memory.main.get_map() == 106:
        while memory.main.get_map() != 153:
            if memory.main.get_coords()[1] > -70:
                pathing.set_movement([6,-75])
            else:
                pathing.set_movement([1,-180])
    FFXC.set_neutral()
    
    logger.info("First, some menuing")
    menu_done = game_vars.get_blitz_win()
    if not dark_aeon:
        menu.after_seymour()
        if game_vars.nemesis():
            memory.main.update_formation(Tidus, Yuna, Auron, full_menu_close=False)
        else:
            #menu.after_seymour()
            memory.main.update_formation(Tidus, Yuna, Rikku, full_menu_close=False)
        menu.equip_sonic_steel(full_menu_close=True)

        logger.info("Now to escape the Guado")

    if memory.main.get_map() == 192:
        checkpoint = 19
    elif dark_aeon:
        checkpoint = 3
    else:
        checkpoint = 0
    while memory.main.get_encounter_id() != 195:
        if dark_aeon and memory.main.get_map() == 192:
            FFXC.set_neutral()
            return
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
                if dark_aeon:
                    while memory.main.battle_active():
                        if Tidus.is_turn():
                            Tidus.attack()
                        else:
                            CurrentPlayer().defend()
                    if memory.main.game_over():
                        return False
                    battle.main.wrap_up()
                elif not menu_done:
                    battle.main.mac_flee_xp()
                    if memory.main.game_over():
                        return False
                    if memory.main.get_tidus_slvl() >= 2:
                        menu.home_grid()
                        menu_done = True
                    memory.main.update_formation(Tidus, Yuna, Rikku)
                    memory.main.close_menu()
                elif memory.main.get_encounter_id() == 195:
                    break
                else:
                    battle.main.flee_all()
                if memory.main.game_over():
                    return False
            elif memory.main.menu_open():
                xbox.tap_b()
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_b()

    logger.info("Done pathing. Now for the Wendigo fight.")
    return True
    
def attempt_wendigo():
    if battle.boss.wendigo():
        logger.info("Wendigo fight over")
        while not memory.main.battle_wrap_up_active():
            if not game_vars.story_mode():
                xbox.tap_confirm()
        while memory.main.battle_wrap_up_active():
            xbox.set_confirm()
        xbox.release_confirm()
        memory.main.click_to_control()
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
                    pathing.approach_coords([-4, -8], quick_return=True)
                FFXC.set_neutral()
                memory.main.click_to_control()
                checkpoint += 1

            # General pathing
            elif pathing.set_movement(MacalaniaUnderTemple.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_b()
    FFXC.set_neutral()
    memory.main.click_to_control()

    checkpoint = 0
    while checkpoint < 2:
        if pathing.set_movement(BikanelDesert.execute(checkpoint)):
            checkpoint += 1
            logger.debug(f"Checkpoint {checkpoint}")

