import logging

import battle.boss
import battle.main
import memory.main
import menu
import pathing
import rng_track
import save_sphere
import screen
import vars
import xbox
import zz_airship_path
from paths import BevelleAirship, BevellePreTrials, BevelleTrials, SutekiDaNe
from players import Auron, Kimahri, Lulu, Rikku, Tidus, Wakka, Yuna

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def pre_evrae():
    FFXC.set_neutral()
    memory.main.click_to_control()
    logger.info("Starting first Airship section")
    checkpoint = 0
    while checkpoint < 19:
        if memory.main.user_control():
            if checkpoint < 4 and memory.main.get_map() == 265:
                memory.main.await_control()
                memory.main.click_to_event_temple(7)
                checkpoint = 4
            elif checkpoint == 9:
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 13:
                save_sphere.touch_and_go()
                memory.main.update_formation(Tidus, Rikku, Kimahri)
                checkpoint += 1
            elif checkpoint == 18:
                memory.main.click_to_event_temple(4)
                checkpoint += 1

            elif pathing.set_movement(BevelleAirship.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()

    zz_airship_path.air_ship_path(1)


def guards():
    logger.info("Start, Guards")
    memory.main.click_to_control()

    if not game_vars.get_blitz_win():
        menu.equip_sonic_steel(full_menu_close=False)

    sleeping_powders = memory.main.get_item_slot(37) != 255
    if not sleeping_powders:
        if memory.main.get_lulu_slvl() < 35:
            memory.main.update_formation(Tidus, Lulu, Rikku, full_menu_close=False)
        else:
            memory.main.update_formation(Tidus, Kimahri, Rikku, full_menu_close=False)
    if (
        memory.main.get_item_slot(3) < 200
        and memory.main.get_hp() != memory.main.get_max_hp()
    ):
        menu.before_guards()
    memory.main.close_menu()
    memory.main.wait_frames(2)

    guard_num = 1
    while memory.main.get_map() != 182:
        if memory.main.user_control():
            if memory.main.get_map() == 180:
                memory.main.click_to_event_temple(6)  # Take the spiral lift down
            elif memory.main.get_map() == 181:
                while not pathing.set_movement([-110, 0]):
                    pass
                memory.main.click_to_event_temple(0)  # Through the water door
            else:
                pathing.set_movement([0, -200])
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle.main.guards(guard_num, sleeping_powders)
                if guard_num == 2:
                    memory.main.click_to_control()
                    memory.main.update_formation(Tidus, Lulu, Rikku)
                elif guard_num == 5:
                    pass
                else:
                    memory.main.click_to_control()
                    memory.main.update_formation(Tidus, Kimahri, Rikku)
                guard_num += 1
            elif memory.main.menu_open():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                if memory.main.diag_progress_flag() == 12:
                    xbox.tap_x()
                else:
                    xbox.skip_scene()
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()
    logger.info("--- End of Bevelle guards")

    checkpoint = 0
    while checkpoint < 8:
        if memory.main.user_control():
            # Map changes
            if checkpoint < 2 and memory.main.get_map() == 182:
                checkpoint = 2
            # General pathing
            elif pathing.set_movement(BevellePreTrials.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()

            # Map changes
            elif checkpoint < 2 and memory.main.get_map() == 182:
                checkpoint = 2


def trials():
    logger.info("Starting Bevelle trials section.")

    checkpoint = 0
    while checkpoint < 53:
        if memory.main.user_control():
            # Map changes
            if checkpoint < 2 and memory.main.get_map() == 306:
                checkpoint = 2

            # Spheres, Pedestals, and gliding across glowing paths.
            elif checkpoint == 3:  # Pedestal that starts it all.
                FFXC.set_movement(0, 1)
                memory.main.await_event()  # Pedestal - START!!!
                FFXC.set_neutral()

                while not memory.main.user_control():
                    if memory.main.get_actor_coords(0)[1] < -100:
                        if memory.main.bt_bi_direction() == 1:
                            FFXC.set_value("btn_b", 1)
                        else:
                            FFXC.set_value("btn_b", 0)
                    elif (
                        memory.main.get_actor_coords(0)[1] > 30
                        and memory.main.get_actor_coords(0)[1] < 90
                    ):
                        FFXC.set_value("btn_b", 1)
                    else:
                        FFXC.set_value("btn_b", 0)
                FFXC.set_neutral()
                if memory.main.get_actor_coords(0)[0] < -20:
                    logger.info("Correct alcove. Moving on with swiftness.")
                    checkpoint += 2
                else:
                    logger.warning("Incorrect alcove. Recovering.")
                    checkpoint += 1
            elif checkpoint == 4:  # Recovery
                FFXC.set_movement(1, 0)
                memory.main.wait_frames(30 * 1.5)
                FFXC.set_movement(-1, 0)
                memory.main.wait_frames(30 * 1.5)
                FFXC.set_neutral()
                memory.main.wait_frames(30 * 10.5)

                xbox.skip_dialog(2)
                memory.main.wait_frames(30 * 3)
                cam = memory.main.get_camera()
                while cam[2] < -69:
                    cam = memory.main.get_camera()
                xbox.skip_dialog(2)
                memory.main.await_control()
                if memory.main.get_coords()[0] < -10:
                    logger.info("Correct alcove. Moving on with swiftness.")
                    checkpoint += 1
                else:
                    logger.warning("Incorrect alcove. Recovering.")
            elif checkpoint == 7:  # First Bevelle sphere, and then more gliding.
                logger.info("Bevelle sphere")
                memory.main.click_to_event_temple(7)
                while memory.main.get_actor_coords(0)[0] < -25:
                    FFXC.set_movement(0, -1)
                    if not memory.main.user_control():
                        xbox.menu_b()
                FFXC.set_neutral()
                logger.debug("Mark 1")
                memory.main.wait_frames(30 * 1)
                FFXC.set_value("btn_b", 1)
                logger.debug("Mark 2")
                memory.main.await_control()
                logger.debug("Mark 3")
                FFXC.set_value("btn_b", 0)
                checkpoint += 1
            elif checkpoint == 10:  # Insert Bevelle sphere. Activate lower areas.
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 13:  # Down to the lower areas.
                FFXC.set_neutral()
                memory.main.wait_frames(2)
                FFXC.set_movement(-1, 0)
                memory.main.wait_frames(30 * 2)
                FFXC.set_neutral()

                while not memory.main.user_control():
                    if memory.main.get_actor_coords(0)[0] < 40:
                        if (
                            memory.main.get_actor_coords(0)[1] > 100
                            or memory.main.get_actor_coords(0)[1] < 10
                        ):
                            FFXC.set_value("btn_b", 1)
                        else:
                            FFXC.set_value("btn_b", 0)

                    elif memory.main.get_actor_coords(0)[1] < -10:
                        if (
                            memory.main.bt_bi_direction() == 1
                            and memory.main.bt_tri_direction_main() == 0
                        ):
                            memory.main.wait_frames(2)
                            if (
                                memory.main.bt_bi_direction() == 1
                                and memory.main.bt_tri_direction_main() == 0
                            ):
                                xbox.menu_b()
                                memory.main.wait_frames(20)
                    else:
                        if (
                            memory.main.get_actor_coords(0)[1] > 293
                            and memory.main.get_actor_coords(0)[1] < 432
                        ):
                            FFXC.set_value("btn_b", 1)
                        else:
                            FFXC.set_value("btn_b", 0)
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 16:  # Take Glyph sphere from second alcove
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 18:  # To third alcove
                FFXC.set_movement(1, -1)
                memory.main.wait_frames(30 * 2)
                FFXC.set_neutral()
                memory.main.wait_frames(30 * 2)
                while not memory.main.user_control():
                    if memory.main.get_actor_coords(0)[0] < 40:
                        if (
                            memory.main.get_actor_coords(0)[1] > 100
                            or memory.main.get_actor_coords(0)[1] < 10
                        ):
                            FFXC.set_value("btn_b", 1)
                        else:
                            FFXC.set_value("btn_b", 0)

                    elif memory.main.get_actor_coords(0)[1] > 425:
                        FFXC.set_value("btn_b", 1)
                    elif (
                        memory.main.get_actor_coords(0)[1] < -30
                        and memory.main.bt_bi_direction() == 0
                        and memory.main.bt_tri_direction_main() == 0
                    ):
                        memory.main.wait_frames(2)
                        if (
                            memory.main.bt_bi_direction() == 0
                            and memory.main.bt_tri_direction_main() == 0
                        ):
                            xbox.menu_b()
                            memory.main.wait_frames(20)
                    else:
                        FFXC.set_value("btn_b", 0)
                # Go ahead and insert Glyph sphere.
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 22:  # Remove Bevelle sphere
                memory.main.click_to_event_temple(4)
                checkpoint += 1
            elif checkpoint == 24:  # Insert Bevelle sphere
                memory.main.click_to_event_temple(5)
                checkpoint += 1
            elif checkpoint == 28:  # Take Glyph sphere
                FFXC.set_neutral()
                memory.main.wait_frames(30 * 0.07)
                memory.main.click_to_event()
                memory.main.wait_frames(30 * 0.035)
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 32:  # Insert Glyph sphere
                while memory.main.user_control():
                    pathing.set_movement([450, 525])
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 34:  # Take Destro sphere
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 37:  # Insert Destro sphere
                FFXC.set_neutral()
                memory.main.wait_frames(30 * 0.1)
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(30 * 0.07)
                FFXC.set_neutral()
                xbox.skip_dialog(1)
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 39:  # Take Bevelle sphere
                memory.main.click_to_event_temple(5)
                checkpoint += 1
            elif checkpoint == 41:  # back on the track.
                FFXC.set_movement(0, -1)
                memory.main.wait_frames(30 * 3)
                FFXC.set_neutral()

                memory.main.wait_frames(30 * 10)
                while not memory.main.user_control():
                    if memory.main.get_actor_coords(0)[0] < 40:
                        if (
                            memory.main.get_actor_coords(0)[1] > 100
                            or memory.main.get_actor_coords(0)[1] < 10
                        ):
                            FFXC.set_value("btn_b", 1)
                        else:
                            FFXC.set_value("btn_b", 0)

                    elif memory.main.get_actor_coords(0)[1] < -30:
                        if (
                            memory.main.bt_bi_direction() == 1
                            and memory.main.bt_tri_direction_main() == 0
                        ):
                            memory.main.wait_frames(2)
                            if (
                                memory.main.bt_bi_direction() == 1
                                and memory.main.bt_tri_direction_main() == 0
                            ):
                                xbox.menu_b()
                                memory.main.wait_frames(20)
                    elif (
                        memory.main.get_actor_coords(0)[1] > 250
                        and memory.main.get_actor_coords(0)[1] < 450
                    ):
                        FFXC.set_value("btn_b", 1)
                    else:
                        FFXC.set_value("btn_b", 0)
                FFXC.set_neutral()
                logger.info("Arriving in the second alcove again.")
                checkpoint += 1
            elif checkpoint == 43:  # Place Bevelle sphere (second alcove)
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 47:  # Take Destro sphere
                FFXC.set_movement(1, -1)
                memory.main.wait_frames(30 * 0.1)
                FFXC.set_neutral()
                xbox.skip_dialog(1)
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 50:  # Insert Destro sphere
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 52:  # Back on track, to the exit
                FFXC.set_movement(1, -1)
                memory.main.wait_frames(30 * 2)
                FFXC.set_neutral()
                memory.main.wait_frames(30 * 19)
                while not memory.main.user_control():
                    if memory.main.get_actor_coords(0)[0] < 40:
                        if (
                            memory.main.get_actor_coords(0)[1] > 100
                            or memory.main.get_actor_coords(0)[1] < 10
                        ):
                            FFXC.set_value("btn_b", 1)
                        else:
                            FFXC.set_value("btn_b", 0)

                    elif memory.main.get_actor_coords(0)[1] < -30:
                        if (
                            memory.main.bt_bi_direction() == 0
                            and memory.main.bt_tri_direction_main() == 0
                        ):
                            memory.main.wait_frames(2)
                            if (
                                memory.main.bt_bi_direction() == 0
                                and memory.main.bt_tri_direction_main() == 0
                            ):
                                xbox.menu_b()
                                memory.main.wait_frames(20)
                    else:
                        if memory.main.get_actor_coords(0)[1] < 250:
                            FFXC.set_value("btn_b", 1)
                        else:
                            FFXC.set_value("btn_b", 0)
                FFXC.set_neutral()
                memory.main.await_control()
                FFXC.set_movement(0, -1)
                memory.main.wait_frames(30 * 2)
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 58:
                memory.main.click_to_event_temple(2)
                checkpoint += 1

            # General pathing
            elif pathing.set_movement(BevelleTrials.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            if memory.main.diag_skip_possible():
                xbox.tap_b()
            if checkpoint < 3:
                FFXC.set_neutral()

    FFXC.set_neutral()


def trials_end():
    checkpoint = 53
    while memory.main.get_map() != 226:
        if memory.main.user_control():
            if pathing.set_movement(BevelleTrials.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
        elif checkpoint == 58:
            memory.main.click_to_event_temple(2)
            checkpoint += 1
        else:
            FFXC.set_neutral()

    FFXC.set_neutral()

    # Name for Bahamut
    xbox.name_aeon("Bahamut")
    if not game_vars.csr():
        xbox.await_save(index=29)


# TODO: Switch to using pathing instead, if possible
def via_purifico():
    memory.main.click_to_control()
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 3)
    FFXC.set_movement(1, 1)
    memory.main.wait_frames(30 * 0.15)
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 5)
    FFXC.set_neutral()

    if not game_vars.csr():
        memory.main.wait_frames(30 * 5.7)  # Wait for the right direction
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 2)
    FFXC.set_neutral()

    memory.main.click_to_control()
    menu.via_purifico()

    while memory.main.get_map() != 209:  # Map number for Altana
        if memory.main.user_control():
            if memory.main.get_slvl_yuna() < 15 and memory.main.get_coords()[1] > 1460:
                FFXC.set_movement(0, -1)
                memory.main.wait_frames(30 * 2)
            else:
                FFXC.set_movement(0, 1)
        elif screen.battle_screen():
            battle.boss.isaaru()
        else:
            FFXC.set_neutral()
            xbox.tap_b()


# TODO: Switch to using pathing instead, if possible
def evrae_altana():
    memory.main.click_to_control()
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(30 * 2)
    FFXC.set_neutral()

    checkpoint = 0
    last_cp = 0
    while checkpoint < 100:
        if last_cp != checkpoint:
            logger.debug(f"Checkpoint reached: {checkpoint}")
            last_cp = checkpoint
        if memory.main.get_story_progress() > 2220:
            logger.info("End of Evrae Altana section.")
            FFXC.set_neutral()
            checkpoint = 100
        if memory.main.user_control():
            pos = memory.main.get_coords()
            cam = memory.main.get_camera()
            if checkpoint == 0:
                if pos[1] > -1550 and cam[0] > 0.5:
                    checkpoint = 10
                else:
                    FFXC.set_movement(0, 1)
            elif checkpoint == 10:
                if pos[1] > -1490:
                    checkpoint = 20
                else:
                    FFXC.set_movement(1, 0)
            elif checkpoint == 20:
                if pos[0] < 1050:
                    checkpoint = 30
                if pos[1] < -1470:
                    FFXC.set_movement(1, 1)
                elif pos[1] > -1365:
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(0, 1)
            elif checkpoint == 30:
                if pos[0] < 625:
                    checkpoint = 40
                if pos[1] < -1410:
                    FFXC.set_movement(1, 1)
                elif pos[1] > -1377:
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(0, 1)

            elif checkpoint == 40:  # Diagonal with swinging camera
                if pos[1] > -540:
                    checkpoint = 50
                if pos[1] < ((-9.83 * pos[0]) + 4840):
                    FFXC.set_movement(1, 1)
                else:
                    FFXC.set_movement(0, 1)
            elif checkpoint == 50:
                if pos[1] > -310:
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(0, 1)
        elif screen.battle_screen():
            battle.boss.evrae_altana()
            rng_track.print_manip_info()
        elif screen.battle_complete():
            xbox.menu_b()
        else:
            FFXC.set_neutral()
            if checkpoint == 50:
                xbox.tap_b()
    return 0


def seymour_natus():
    memory.main.click_to_control()

    if memory.main.get_yuna_slvl() >= 14:
        if game_vars.get_blitz_win():
            menu.seymour_natus_blitz_win()
        else:
            menu.seymour_natus_blitz_loss()

    memory.main.update_formation(Tidus, Yuna, Auron)
    save_sphere.touch_and_go()
    complete = 0
    while complete == 0:
        if memory.main.user_control():
            pathing.set_movement([2, memory.main.get_coords()[1] - 50])
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                logger.info("Battle Start")
                if memory.main.battle_type() == 2:
                    battle.main.flee_all()
                else:
                    complete = battle.boss.seymour_natus()

                if memory.main.get_yuna_slvl() >= 14:
                    if game_vars.get_blitz_win():
                        menu.seymour_natus_blitz_win()
                    else:
                        menu.seymour_natus_blitz_loss()
                rng_track.print_manip_info()

    # Movement for make-out scene
    memory.main.click_to_control()

    checkpoint = 0
    while checkpoint < 13:
        if memory.main.user_control():
            # Events and map changes
            if checkpoint == 1 or checkpoint == 3:
                memory.main.click_to_event_temple(4)
                checkpoint += 1
            elif checkpoint == 5:
                logger.debug("Checkpoint 5")
                FFXC.set_movement(-1, 0)
                memory.main.await_event()
                FFXC.set_neutral()
                memory.main.wait_frames(3)
                checkpoint += 1
            elif checkpoint == 6:
                logger.debug("Checkpoint 6")
                if not game_vars.csr():
                    memory.main.click_to_event_temple(3)
                checkpoint += 1
            elif checkpoint == 8:
                logger.debug("Checkpoint 8")
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 12:
                logger.debug("Checkpoint 12")
                memory.main.click_to_event_temple(0)
                checkpoint += 1

            elif pathing.set_movement(SutekiDaNe.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                xbox.skip_scene()
