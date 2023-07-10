import logging
import time

import battle.boss
import battle.main
import logs
import memory.main
import menu
import pathing
import save_sphere
import screen
import vars
import xbox
from paths import MRRBattleSite, MRRBattleSiteAftermath, MRRMain, MRRStart
from players import Auron, Tidus, Wakka
from area.mrr_skip import skip_prep, attempt_skip, advance_to_aftermath

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def arrival():
    logger.info("Arrival at MRR")
    memory.main.click_to_control()
    memory.main.close_menu()

    checkpoint = 0
    while memory.main.get_map() != 92:
        if memory.main.user_control():
            if game_vars.csr() and checkpoint == 1:
                logger.debug("CSR, skipping forward")
                checkpoint = 4
                logger.debug(f"Checkpoint {checkpoint}")
            elif checkpoint == 6 and not game_vars.csr():
                skip_prep()
                if attempt_skip():
                    advance_to_aftermath()
                    game_vars.mrr_skip_set(1)
                    return 1
                else:
                    return 2
            elif checkpoint == 3:
                FFXC.set_movement(-1, 0)
                memory.main.wait_frames(30 * 0.7)
                FFXC.set_neutral()
                memory.main.wait_frames(30 * 0.4)
                FFXC.set_movement(1, -1)
                memory.main.wait_frames(30 * 0.035)
                FFXC.set_neutral()
                memory.main.wait_frames(30 * 2.3)
                if not memory.main.user_control():
                    battle.main.flee_all()
                    battle.main.wrap_up()
                    memory.main.update_formation(Tidus, Wakka, Auron)
                    FFXC.set_movement(-1, 0)
                    memory.main.wait_frames(30 * 0.7)
                    FFXC.set_neutral()
                    memory.main.wait_frames(30 * 0.4)
                    FFXC.set_movement(1, -1)
                    memory.main.wait_frames(30 * 0.035)
                    FFXC.set_neutral()
                    memory.main.wait_frames(30 * 0.3)
                logger.info("Attempting skip.")
                xbox.menu_b()

                # Now to wait for the skip to happen, or 60 second maximum limit
                start_time = time.time()
                # Max number of seconds that we will wait for the skip to occur.
                time_limit = 60
                max_time = start_time + time_limit
                while memory.main.get_actor_coords(6)[0] < -50:
                    current_time = time.time()
                    if current_time > max_time:
                        logger.warning("Skip seemingly failed. Moving on without it.")
                        break
                memory.main.click_to_control()
                FFXC.set_neutral()
                checkpoint += 1
            elif pathing.set_movement(MRRStart.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                battle.main.flee_all()
                memory.main.click_to_control_3()
                if memory.main.get_hp()[0] < 520:
                    battle.main.heal_up(full_menu_close=False)
                elif 1 in memory.main.ambushes():
                    battle.main.heal_up(full_menu_close=False)
                memory.main.update_formation(Tidus, Wakka, Auron)
                memory.main.close_menu()
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()
    FFXC.set_neutral()
    if game_vars.csr():
        # Logic for CSR mode
        memory.main.await_control()
        FFXC.set_movement(1, -1)
        memory.main.await_event()
        FFXC.set_neutral()
        memory.main.await_control()
        skip_prep()
        attempt_skip()
        advance_to_aftermath()
        game_vars.mrr_skip_set(True)
        return True
    logger.info("Done with prelim MRR area, now for the real deal.")
    return 0


def log_mrr_kimahri_crit_chance():
    crit_chance = memory.main.next_crit(character=3, char_luck=18, enemy_luck=15)
    logger.debug(f"Next Kimahri crit: {crit_chance}")


def main_path():
    memory.main.await_control()
    crit_manip = False
    # Yuna complete, Kimahri complete, Valefor overdrive, Battle counter, Yuna grid complete, MRR phase
    status = [0, 0, 0, 1, 0, 0]
    logger.debug("Resetting checkpoint.")
    last_gil_value = 0
    checkpoint = 0
    battle_count = 0
    while memory.main.get_map() != 119:
        if status[0] == 1 and status[1] == 1 and status[2] == 0:
            status[2] = 2  # No need to do Valefor's overdrive and recharge.
        if status[0] == 1 and status[1] == 1 and status[2] == 2:
            # All pieces are complete. Move phase to final phase.
            status[5] = 3
        if memory.main.user_control():
            if checkpoint == 1:
                save_sphere.touch_and_go()
                memory.main.update_formation(Tidus, Wakka, Auron)
                checkpoint += 1
            elif checkpoint == 4:
                logger.info("Up the first lift")
                xbox.skip_dialog(1)
                checkpoint += 1
            elif checkpoint == 45:
                if status[0] == 0 or status[1] == 0 or status[2] != 2:
                    if pathing.set_movement(MRRMain.execute(99)):
                        checkpoint -= 1
                else:
                    if pathing.set_movement(MRRMain.execute(45)):
                        checkpoint += 1

            elif checkpoint == 46:
                logger.info("Up the second lift.")
                FFXC.set_neutral()
                xbox.skip_dialog(1)
                checkpoint += 1
                logger.debug(f"Lift Checkpoint {checkpoint}")
            elif checkpoint == 48:  # X-potion for safety
                if memory.main.rng_seed() not in [31]:
                    memory.main.click_to_event_temple(7)
                    logger.info("Got X-potion")
                checkpoint += 1
            elif checkpoint >= 54 and checkpoint <= 56:  # 400 gil guy
                if memory.main.rng_seed() in [160, 31]:
                    checkpoint = 57
                elif memory.main.get_gil_value() != last_gil_value:
                    # check if we got the 400 from the guy
                    if memory.main.get_gil_value() == last_gil_value + 400:
                        logger.info("We've procured the 400 gil from the guy.")
                        checkpoint = 57  # now to the actual lift
                    else:
                        last_gil_value = memory.main.get_gil_value()
                else:
                    pathing.set_movement(memory.main.mrr_guy_coords())
                    xbox.tap_b()
            elif checkpoint == 58:
                logger.info("Up the third lift")
                while memory.main.user_control():
                    pathing.set_movement([29, 227])
                    xbox.tap_b()
                checkpoint += 1
            elif checkpoint == 66:
                xbox.skip_dialog(1)
                logger.info("Up the final lift")
                log_mrr_kimahri_crit_chance()
                checkpoint += 1
            elif checkpoint == 68:
                FFXC.set_movement(0, -1)
                memory.main.wait_frames(9)
                FFXC.set_movement(-1, -1)
                memory.main.wait_frames(9)
                checkpoint += 1
            elif checkpoint < 71 and memory.main.get_map() == 79:
                checkpoint = 71  # Into Battle Site zone (upper, cannon area)
            elif pathing.set_movement(MRRMain.execute(checkpoint)):
                if checkpoint == 61:
                    if memory.main.next_crit(
                        character=3, char_luck=18, enemy_luck=15
                    ) in [2, 3, 4, 5, 6, 7, 9]:
                        crit_manip = True
                        # Try to end on 1.
                        logger.debug(
                            f"We can manip: {memory.main.next_crit(character=3, char_luck=18, enemy_luck=15)}"
                        )
                        checkpoint = 59
                    else:
                        checkpoint += 1
                elif checkpoint == 90:
                    checkpoint = 62
                else:
                    checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                logger.info("Starting battle MRR")
                if checkpoint < 47:
                    status = battle.main.mrr_battle(status)
                    logger.debug(f"Status update: {status}")
                    status[3] += 1
                else:
                    if battle.main.mrr_manip(kim_max_advance=9):
                        crit_manip = True

                if memory.main.get_yuna_slvl() >= 8 and status[4] == 0:
                    logger.info("Yuna has enough levels now. Going to do her grid.")
                    menu.mrr_grid_yuna()
                    logger.info("Yunas gridding is complete for now.")
                    status[4] = 1
                if memory.main.get_slvl_wakka() >= 7:
                    menu.mrr_grid_2()
                memory.main.close_menu()
                logger.info("MRR battle complete")
                log_mrr_kimahri_crit_chance()
                battle_count += 1
            elif memory.main.menu_open():
                xbox.tap_b()
            elif memory.main.diag_skip_possible():
                memory.main.click_to_control_3()

            # Map changes
            elif checkpoint < 47 and memory.main.get_map() == 128:
                checkpoint = 47

        if memory.main.game_over():
            return
    # logs.write_stats("MRR Battles:")
    # logs.write_stats(battle_count)
    logs.write_stats("MRR crit manip:")
    logs.write_stats(crit_manip)
    logger.info("End of MRR section. Status:")
    logger.info("[Yuna AP, Kim AP, Valefor OD steps, then other stuff]")
    logger.info(status)

    # Get close to save sphere
    checkpoint = 0
    while checkpoint < 4:
        if pathing.set_movement(MRRBattleSite.execute(checkpoint)):
            checkpoint += 1
            logger.debug(f"Checkpoint {checkpoint}")


def battle_site():
    memory.main.await_control()
    if game_vars.get_l_strike() >= 2:
        menu.equip_weapon(character=4, ability=0x8026, full_menu_close=False)
    menu.battle_site_grid()

    checkpoint = 4
    while checkpoint < 99:
        if memory.main.user_control():
            if checkpoint == 5:
                logger.info("O'aka menu section")
                while memory.main.user_control():
                    pathing.set_movement([-45, 3425])
                    xbox.tap_b()
                FFXC.set_neutral()
                menu.battle_site_oaka_1()
                menu.battle_site_oaka_2()
                log_mrr_kimahri_crit_chance()
                checkpoint += 1
            elif checkpoint == 8:
                save_sphere.touch_and_go()
                log_mrr_kimahri_crit_chance()
                checkpoint += 1
            elif checkpoint == 12:
                FFXC.set_movement(1, 0)
                memory.main.wait_frames(45)
                checkpoint += 1
            elif checkpoint == 14:
                FFXC.set_movement(1, 0)
                memory.main.click_to_event()
                FFXC.set_neutral()
                memory.main.wait_frames(9)
                xbox.tap_b()  # Tell me when you're ready.
                FFXC.set_neutral()
                memory.main.wait_frames(15)
                xbox.menu_down()
                xbox.tap_b()
                checkpoint = 100
            elif pathing.set_movement(MRRBattleSite.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
    battle.boss.gui()


def aftermath():
    memory.main.click_to_control_dumb()
    checkpoint = 0
    while memory.main.get_map() != 93:
        if memory.main.user_control():
            if memory.main.get_map() == 131 and checkpoint < 4:
                checkpoint = 4
            elif checkpoint == 3:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 7:
                FFXC.set_movement(-1, 0)
                memory.main.await_event()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 15:
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                checkpoint += 1
            elif pathing.set_movement(MRRBattleSiteAftermath.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            memory.main.click_to_control_3()
