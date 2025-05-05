import logging

import airship_pathing
import battle.boss
import battle.main
import memory.main
import menu
import pathing
from pathing import approach_coords
import rng_track
import save_sphere
import screen
import vars
import xbox
from paths import BevelleAirship, BevellePreTrials, BevelleTrials, SutekiDaNe
from players import Auron, Kimahri, Lulu, Rikku, Tidus, Yuna
from area.dream_zan import split_timer
from json_ai_files.write_seed import write_big_text

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def pre_evrae():
    FFXC.set_neutral()
    while not memory.main.user_control():
        if memory.main.battle_active():
            # Reloaded autosave into the evrae fight will trigger this branch.
            #xbox.click_to_battle()
            return
        xbox.tap_b()
    memory.main.wait_frames(2)
    logger.info("Starting first Airship section")
    #rng_track.print_manip_info()
    logger.manip(f"Evrae attack prediction: {rng_track.evrae_targets()}")
    checkpoint = 0
    while checkpoint < 19:
        if memory.main.user_control():
            if checkpoint < 4 and memory.main.get_map() == 265:
                memory.main.await_control()
                memory.main.click_to_event_temple(7,story_mode_dialog=True)
                checkpoint = 4
            elif checkpoint == 9:
                memory.main.click_to_event_temple(7,story_mode_dialog=True)
                checkpoint += 1
            elif checkpoint == 13:
                save_sphere.touch_and_go()
                memory.main.update_formation(Tidus, Rikku, Kimahri)
                checkpoint += 1
            elif checkpoint == 18:
                memory.main.click_to_event_temple(4,story_mode_dialog=True)
                checkpoint += 1

            elif pathing.set_movement(BevelleAirship.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_b()

    logger.manip(f"Evrae attack prediction: {rng_track.evrae_targets()}")
    airship_pathing.air_ship_path(1)


def guards():
    logger.info("Start, Guards")
    #rng_track.print_manip_info()
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
        menu.overworld_use_item()
    memory.main.close_menu()
    memory.main.wait_frames(2)

    guard_num = 1
    while memory.main.get_map() != 182:
        if memory.main.user_control():
            if memory.main.get_map() == 180:
                memory.main.click_to_event_temple(6,story_mode_dialog=True)  # Take the spiral lift down
            elif memory.main.get_map() == 181:
                while not pathing.set_movement([-110, 0]):
                    pass
                memory.main.click_to_event_temple(0,story_mode_dialog=True)  # Through the water door
            else:
                pathing.set_movement([0, -200])
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle.main.guards(guard_num, sleeping_powders)
                if guard_num in [2,4] or not sleeping_powders:
                    #if Rikku.hp() < 250:
                    #    battle.main.heal_up_2(0, single_item=True, full_menu_close=False)
                    memory.main.update_formation(Tidus, Lulu, Rikku)
                elif guard_num == 5:
                    pass
                else:
                    #if Rikku.hp() < 250:
                    #    battle.main.heal_up_2(0, single_item=True, full_menu_close=False)
                    memory.main.update_formation(Tidus, Kimahri, Rikku)
                #rng_track.print_manip_info()
                guard_num += 1
                #logger.manip(memory.main.rng_array_from_index(index=10, array_len=40))
            elif memory.main.menu_open():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                if memory.main.diag_progress_flag() == 12:
                    xbox.tap_x()
                else:
                    xbox.skip_scene()
            elif memory.main.menu_open():
                xbox.tap_b()
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_b()
    logger.info("--- End of Bevelle guards")
    write_big_text("")

    checkpoint = 0
    while checkpoint < 8:
        if memory.main.user_control():
            # Map changes
            if checkpoint < 2 and memory.main.get_map() == 182:
                checkpoint = 2
            # General pathing
            elif pathing.set_movement(BevellePreTrials.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
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

            # Spheres, Pedestols, and gliding across glowing paths.
            elif checkpoint == 3:  # Pedestol that starts it all.
                FFXC.set_movement(0, 1)
                memory.main.await_event()  # Pedestol - START!!!
                FFXC.set_neutral()

                while not memory.main.user_control():
                    if memory.main.get_actor_coords(0)[1] < -100:
                        if memory.main.bt_bi_direction() == 1:
                            FFXC.set_confirm()
                        else:
                            FFXC.release_confirm()
                    elif (
                        memory.main.get_actor_coords(0)[1] > 30
                        and memory.main.get_actor_coords(0)[1] < 90
                    ):
                        FFXC.set_confirm()
                    else:
                        FFXC.release_confirm()
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
                approach_coords([-73,85],diag=1,click_through=True)
                while memory.main.get_actor_coords(0)[0] < -25:
                    FFXC.set_movement(0, -1)
                    if not memory.main.user_control():
                        xbox.menu_b()
                FFXC.set_neutral()
                logger.debug("Mark 1")
                memory.main.wait_frames(30 * 1)
                FFXC.set_confirm()
                logger.debug("Mark 2")
                memory.main.await_control()
                logger.debug("Mark 3")
                FFXC.release_confirm()
                checkpoint += 1
            elif checkpoint == 10:  # Insert Bevelle sphere. Activate lower areas.
                approach_coords([13,97],diag=8,click_through=True)
                checkpoint += 1
            elif checkpoint == 13:  # Down to the lower areas.
                FFXC.set_neutral()
                memory.main.wait_frames(2)
                FFXC.set_movement(-1, 0)
                memory.main.wait_frames(120)
                FFXC.set_neutral()

                while not memory.main.user_control():
                    if memory.main.get_actor_coords(0)[0] < 40:
                        if (
                            memory.main.get_actor_coords(0)[1] > 100
                            or memory.main.get_actor_coords(0)[1] < 10
                        ):
                            FFXC.set_confirm()
                        else:
                            FFXC.release_confirm()

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
                            FFXC.set_confirm()
                        else:
                            FFXC.release_confirm()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 16:  # Take Glyph sphere from second alcove
                approach_coords([503,365],diag=1,click_through=True)
                checkpoint += 1
            elif checkpoint == 18:  # To third alcove
                FFXC.set_movement(1, -1)
                memory.main.wait_frames(60)
                FFXC.set_neutral()
                memory.main.wait_frames(60)
                while not memory.main.user_control():
                    if memory.main.get_actor_coords(0)[0] < 40:
                        if (
                            memory.main.get_actor_coords(0)[1] > 100
                            or memory.main.get_actor_coords(0)[1] < 10
                        ):
                            FFXC.set_confirm()
                        else:
                            FFXC.release_confirm()

                    elif memory.main.get_actor_coords(0)[1] > 425:
                        FFXC.set_confirm()
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
                        FFXC.release_confirm()
                # Go ahead and insert Glyph sphere.
                approach_coords([355,525],diag=8,click_through=True)
                checkpoint += 1
            elif checkpoint == 22:  # Remove Bevelle sphere
                # This takes special logic. Can't just smash face into the pedestol.
                FFXC.set_neutral()
                memory.main.wait_frames(6)
                FFXC.set_movement(0,-1)
                memory.main.wait_frames(7)
                FFXC.set_neutral()
                #memory.main.wait_frames(2)
                xbox.tap_b()
                xbox.tap_b()
                memory.main.click_to_event()
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 24:  # Insert Bevelle sphere
                approach_coords([360,539],diag=8,click_through=True)
                checkpoint += 1
            elif checkpoint == 28:  # Take Glyph sphere
                FFXC.set_movement(1,1)
                memory.main.wait_frames(2)
                FFXC.set_neutral()
                #memory.main.wait_frames(30)
                xbox.tap_b()
                xbox.tap_b()
                approach_coords([355,525],diag=1,click_through=True)
                checkpoint += 1
            elif checkpoint == 32:  # Insert Glyph sphere
                approach_coords([450,525],diag=8,click_through=True)
                checkpoint += 1
            elif checkpoint == 34:  # Take Destro sphere
                approach_coords([505,525],diag=1,click_through=True)
                checkpoint += 1
            elif checkpoint == 37:  # Insert Destro sphere
                approach_coords([365,525],diag=8,click_through=True)
                checkpoint += 1
            elif checkpoint == 39:  # Take Bevelle sphere
                approach_coords([360,539],diag=1,click_through=True)
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
                            FFXC.set_confirm()
                        else:
                            FFXC.release_confirm()

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
                        FFXC.set_confirm()
                    else:
                        FFXC.release_confirm()
                FFXC.set_neutral()
                logger.info("Arriving in the second alcove again.")
                checkpoint += 1
            elif checkpoint == 43:  # Place Bevelle sphere (second alcove)
                approach_coords([395,365],diag=8,click_through=True)
                checkpoint += 1
            elif checkpoint == 47:  # Take Destro sphere
                # This takes special logic. Can't just smash face into the pedestol.
                FFXC.set_neutral()
                memory.main.wait_frames(3)
                FFXC.set_movement(1,-1)
                memory.main.wait_frames(12)
                FFXC.set_neutral()
                memory.main.wait_frames(6)
                memory.main.click_to_event()
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 50:  # Insert Destro sphere
                approach_coords([505,365],diag=8,click_through=True)
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
                            FFXC.set_confirm()
                        else:
                            FFXC.release_confirm()

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
                            FFXC.set_confirm()
                        else:
                            FFXC.release_confirm()
                FFXC.set_neutral()
                memory.main.await_control()
                memory.main.wait_frames(3)
                FFXC.set_movement(0, -1)
                memory.main.wait_frames(60)
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 58:
                memory.main.click_to_event_temple(2)
                checkpoint += 1

            # General pathing
            elif pathing.set_movement(BevelleTrials.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
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
                logger.debug(f"Checkpoint {checkpoint}")
        elif memory.main.diag_skip_possible() and not game_vars.story_mode():
            xbox.tap_b()
        elif checkpoint == 58:
            memory.main.click_to_event_temple(2)
            checkpoint += 1
        else:
            FFXC.set_neutral()
    split_timer()
    FFXC.set_neutral()

    # Name for Bahamut
    xbox.name_aeon("Bahamut")
    if not game_vars.csr():
        xbox.await_save(index=29)
    
    last_report = memory.main.get_frame_count()
    i = 0
    while memory.main.get_story_progress() != 2220:
        if memory.main.get_frame_count() - last_report > 30:
            logger.debug(f"Story: {memory.main.get_story_progress()} | dialog: {memory.main.diag_progress_flag()} | {i}")
            last_report = memory.main.get_frame_count()
            i += 1
        if not game_vars.story_mode():
            xbox.tap_confirm()
    logger.info("Reached Via Purifico map - ending 'trials_end' function.")

    if game_vars.story_mode():
        memory.main.wait_seconds(5)


def via_purifico():
    memory.main.click_to_control_3()
    # Print RNG info
    #rng_track.guards_to_calm_equip_drop_count(guard_battle_num=6,report_num=0)
    routes, best = rng_track.purifico_to_nea()
    write_big_text(str(routes))
    
    # Determine variables for the path forward.
    if bool(best % 2 == 0 and routes[best] != routes[best+1]):
        game_vars.set_force_third_larvae(True)
    else:
        game_vars.set_force_third_larvae(False)
    game_vars.set_def_x_drop(bool((best % 4) >= 2))
    game_vars.set_nea_after_bny(bool(best >= 4))
    logger.manip(f"Third larvae: {game_vars.get_force_third_larvae()}")
    #logger.manip(memory.main.rng_array_from_index(index=10, array_len=40))
    
    memory.main.click_to_control_3()

    # New logic
    path = [[-1, 142], [-2, 324], [-2, 503]]
    checkpoint = 0
    create_save = game_vars.create_saves()
    while checkpoint < len(path):
        if checkpoint == 1 and create_save:
            save_sphere.touch_and_save(
                save_num=64, game_state="rescue_yuna", step_count=3
            )
            create_save = False
        if pathing.set_movement(path[checkpoint]):
            logger.debug(f"Checkpoint {checkpoint}")
            checkpoint += 1
    FFXC.set_neutral()
    logger.debug("Ready to step on glyph")

    while memory.main.via_quad_direction() != 1:
        pass
    logger.debug("Glyph is now lined up")
    while memory.main.user_control():
        pathing.set_movement([-2, 550])

    # End logic replacement
    memory.main.click_to_control()
    finish_grid_late = menu.via_purifico()
    if (
        1 in memory.main.ambushes() or
        2 in memory.main.ambushes() or
        3 in memory.main.ambushes()
    ):
        save_sphere.touch_and_go()
    larvae_count = 0
    rng_track.purifico_to_nea(stage=0)

    while memory.main.get_map() != 209:  # Map number for Altana
        if memory.main.user_control():
            #if memory.main.get_slvl_yuna() < 15 and memory.main.get_coords()[1] > 1460:
            #    FFXC.set_movement(0, -1)
            #    memory.main.wait_frames(60)
            if (
                game_vars.get_force_third_larvae() and
                larvae_count < 3 and 
                memory.main.get_coords()[1] > 1460
            ):
                FFXC.set_movement(0, -1)
                memory.main.wait_frames(60)
            elif (
                finish_grid_late and 
                memory.main.get_slvl_yuna() < 8 and
                memory.main.get_coords()[1] > 1460
            ):
                FFXC.set_movement(0, -1)
                memory.main.wait_frames(60)
            else:
                FFXC.set_movement(0, 1)
        elif memory.main.battle_active():
            logger.warning(f"{larvae_count}, {memory.main.get_slvl_yuna()}")
            if memory.main.get_encounter_id() < 258:
                larvae_count += 1
            battle.boss.isaaru()
            if memory.main.game_over():
                logger.warning("via_purifico function, RETURN FALSE")
                game_vars.reset_rescue_count()
                return False
            elif 1 in memory.main.ambushes() and memory.main.get_encounter_id() == 257:
                memory.main.click_to_control()
                battle.main.heal_up(full_menu_close=True)
            
            if memory.main.get_encounter_id() < 258:
                if memory.main.get_slvl_yuna() >= 8 and finish_grid_late:
                    menu.via_purifico_noTerra_recovery()
                    finish_grid_late = False
            logger.warning(f"{larvae_count}, {memory.main.get_slvl_yuna()}")
            #logger.manip(memory.main.rng_array_from_index(index=10, array_len=40))
        else:
            FFXC.set_neutral()
            if not game_vars.story_mode():
                xbox.tap_confirm()
    split_timer()
    return True


# TODO: Switch to using pathing instead, if possible
def evrae_altana():
    path = [
        [1641,-1656],
        [1637,-1518],
        [1604,-1492],
        [1338,-1450],
        [831,-1419],  # This checkpoint engages Altana
        [666,-1389],
        [631,-1363],
        [575,-1110],
        [565,-476],
        [514,-374],
        [467,-338],
        [300,-307],
        [10,-300]
    ]

    checkpoint = 0
    while memory.main.get_map() != 208:
        if memory.main.user_control():
            if pathing.set_movement(path[checkpoint]):
                checkpoint += 1
                logger.debug(f"Checkpoint: {checkpoint}")
        else:
            if screen.battle_screen():
                battle.boss.evrae_altana()
                logger.debug("Mark")
                logger.debug(memory.main.get_encounter_id())
                if memory.main.get_encounter_id() == 266:
                    paths, best = rng_track.purifico_to_nea(stage=1)
                    write_big_text(str(paths))
                    logger.debug(f"Rescue count: {game_vars.get_rescue_count()}")
            elif memory.main.battle_wrap_up_active():
                xbox.menu_b()

    FFXC.set_neutral()
    memory.main.click_to_control()


def evrae_altana_old():
    # Print RNG info
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(60)
    #logger.manip(memory.main.rng_array_from_index(index=10, array_len=30))
    FFXC.set_neutral()

    checkpoint = 0
    last_cp = 0
    while checkpoint < 100:
        if last_cp != checkpoint:
            logger.debug(f"Checkpoint {checkpoint}")
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
            logger.debug(memory.main.get_encounter_id())
            if memory.main.get_encounter_id() == 266:
                rng_track.purifico_to_nea(stage=1)
                logger.debug(f"Rescue count: {game_vars.get_rescue_count()}")
        elif memory.main.battle_wrap_up_active():
            xbox.menu_b()
        else:
            FFXC.set_neutral()
            if checkpoint == 50:
                xbox.tap_b()
    return 0


def natus_formation(battles: int = 0, full_menu_close: bool = True):
    memory.main.update_formation(Tidus, Yuna, Auron, full_menu_close=full_menu_close)
    """
    if memory.main.get_yuna_slvl() <= 13:
        # Just need levels
        memory.main.update_formation(
            Tidus, Wakka, Auron, full_menu_close=full_menu_close
        )
    elif battles >= 2 or memory.main.highbridge_drops()[0] - (battles * 9) > 20:
        # Must be ready for Natus, and no reason to manip if nothing drops here.
        memory.main.update_formation(
            Tidus, Yuna, Auron, full_menu_close=full_menu_close
        )
    elif rng_track.nea_track()[1] >= 3:
        # Need to advance RNG
        memory.main.update_formation(
            Tidus, Wakka, Auron, full_menu_close=full_menu_close
        )
    else:
        memory.main.update_formation(
            Tidus, Yuna, Auron, full_menu_close=full_menu_close
        )
    """


def seymour_natus():
    memory.main.click_to_control()
    start_count = game_vars.get_rescue_count()
    if start_count == 0:
        start_count = 3
        game_vars.set_rescue_count(value=start_count)

    delay_grid = True
    memory.main.update_formation(Tidus, Yuna, Auron, full_menu_close=False)
    if memory.main.get_yuna_slvl() >= 9:
        delay_grid = False
        if game_vars.get_blitz_win():
            menu.seymour_natus_blitz_win()
        else:
            menu.seymour_natus_blitz_loss()
    memory.main.close_menu()
    #logger.manip(memory.main.rng_array_from_index(index=10, array_len=30))

    save_sphere.touch_and_go()
    rng_track.purifico_to_nea(stage=1)
    logger.debug(f"Rescue count: {game_vars.get_rescue_count()}")
    while memory.main.get_story_progress() < 2300:
        if memory.main.user_control():
            if delay_grid and memory.main.get_coords()[1] < 260:
                pathing.set_movement([2, memory.main.get_coords()[1] + 50])
                memory.main.wait_frames(30)
            else:
                pathing.set_movement([2, memory.main.get_coords()[1] - 50])
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                logger.info("Battle Start")
                if memory.main.battle_type() == 2:
                    battle.main.flee_all()
                    battle.main.wrap_up()
                else:
                    battle.boss.seymour_natus(delay_grid)
                    battle.main.wrap_up()
                    '''
                    if complete == 1 and not game_vars.csr():
                        memory.main.click_to_diag_progress(num=9)
                        memory.main.click_to_control()
                    else:
                        battle.main.wrap_up()
                    '''

                memory.main.update_formation(Tidus, Yuna, Auron, full_menu_close=False)
                battle.main.heal_up(full_menu_close=True)
                if memory.main.get_yuna_slvl() >= 9 and delay_grid:
                    delay_grid = False
                    if game_vars.get_blitz_win():
                        menu.seymour_natus_blitz_win()
                    else:
                        menu.seymour_natus_blitz_loss()
                memory.main.close_menu()
                logger.debug(f"Rescue count: {game_vars.get_rescue_count()}")
                #logger.manip(memory.main.rng_array_from_index(index=10, array_len=30))
                #rng_track.print_manip_info()
            elif memory.main.battle_wrap_up_active():
                xbox.tap_confirm()
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
    logger.info("Natus fight complete, onward to cutscenes.")
    memory.main.click_to_control()

    # To the make-out scene
    while memory.main.get_story_progress() <= 2300:
        if memory.main.user_control():
            map = memory.main.get_map()
            if map == 183:
                pathing.set_movement([-30,35])
            elif map == 274:
                pathing.set_movement([35,-80])
            elif map == 206:
                pathing.set_movement([200,25])
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
            elif memory.main.cutscene_skip_possible():
                xbox.skip_scene()
    
    # Back to the party
    while memory.main.get_map() != 223:
        if memory.main.user_control():
            map = memory.main.get_map()
            if map == 206:
                pathing.set_movement([300,100])
            elif map == 177:
                pathing.set_movement([200,-30])
            elif map == 329:
                if memory.main.get_coords()[0] < -30:
                    pathing.set_movement([-20,-10])
                else:
                    return
                    # This should end near the save sphere.
                    #pathing.set_movement([35,200])

        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()



    '''  # Old logic
    # Movement for make-out scene
    checkpoint = 0
    while checkpoint < 13:
        if memory.main.user_control():
            # Events and map changes
            if checkpoint == 1 or checkpoint == 3:
                while memory.main.get_map() == 183:
                    pathing.set_movement([-30,35])
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
                    FFXC.set_movement(1,-1)
                    memory.main.await_event()
                    FFXC.set_neutral()
                    memory.main.click_to_control()
                checkpoint += 1
            elif checkpoint == 8:
                logger.debug("Checkpoint 8")
                FFXC.set_movement(1,0)
                memory.main.await_event()
                FFXC.set_neutral()
                memory.main.click_to_control()
                checkpoint += 1
            elif checkpoint == 12:
                logger.debug("Checkpoint 12")
                FFXC.set_movement(0,1)
                memory.main.await_event()
                FFXC.set_neutral()
                memory.main.click_to_control()
                checkpoint += 1

            elif pathing.set_movement(SutekiDaNe.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                xbox.skip_scene()
    '''
