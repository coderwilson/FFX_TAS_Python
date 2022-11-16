import logging

import battle.main
import logs
import memory.main
import menu
import pathing
import screen
import vars
import xbox
from paths import Besaid1, Besaid2, BesaidTrials
from players import Auron, Kimahri, Lulu, Rikku, Tidus, Wakka, Yuna

FFXC = xbox.controller_handle()
game_vars = vars.vars_handle()

logger = logging.getLogger(__name__)


def beach():
    logger.info("Starting Besaid section. Beach")
    if game_vars.csr():
        FFXC.set_neutral()
        memory.main.await_control()
    else:
        FFXC.set_movement(0, -1)
        memory.main.await_control()
        memory.main.wait_frames(30 * 4.5)
        FFXC.set_neutral()

    # Pathing, lots of pathing.
    besaid_battles = 0
    good_battles = 0
    checkpoint = 0
    last_cp = 0
    while memory.main.get_map() != 122:
        if checkpoint != last_cp:
            logger.debug(f"Checkpoint reached: {checkpoint}")
            last_cp = checkpoint

        # map changes
        if checkpoint < 2 and memory.main.get_map() == 20:
            checkpoint = 2
            logger.debug(f"Map change. Checkpoint: {checkpoint}")
        elif checkpoint < 6 and memory.main.get_map() == 41:
            checkpoint = 6
            logger.debug(f"Map change. Checkpoint: {checkpoint}")
        elif checkpoint < 22 and memory.main.get_map() == 69:
            checkpoint = 22
            logger.debug(f"Map change. Checkpoint: {checkpoint}")
        elif checkpoint < 29 and memory.main.get_map() == 133:
            if not game_vars.csr():
                # You do remember the prayer?
                memory.main.click_to_diag_progress(9)
                memory.main.wait_frames(20)
                xbox.menu_down()
                xbox.menu_b()
            checkpoint = 29
        elif checkpoint == 36 and memory.main.get_map() == 17:
            checkpoint = 37

        # Events
        elif memory.main.user_control():
            if checkpoint == 34:  # Into the temple for the first time
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 43:  # Wakka tent
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 44:  # Talk to Wakka
                while memory.main.user_control():
                    pathing.set_movement([15, 16])
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_control()
                checkpoint += 1
            elif checkpoint == 45:  # Exiting tent
                logger.info("Exiting tent")
                memory.main.click_to_event_temple(7)
                checkpoint += 1

            # General pathing
            elif pathing.set_movement(Besaid1.execute(checkpoint)):
                checkpoint += 1
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                battle.main.piranhas()
                besaid_battles += 1
                encounter_id = memory.main.get_encounter_id()
                if encounter_id == 11 or (
                    encounter_id == 12 and memory.main.battle_type() == 1
                ):
                    good_battles += 1
            elif memory.main.diag_skip_possible() or memory.main.menu_open():
                xbox.tap_b()
    logs.write_stats("piranha battles:")
    logs.write_stats(str(besaid_battles))
    # logs.write_stats("Optimal piranha battles:")
    # logs.write_stats(str(good_battles))


def trials():
    checkpoint = 0

    while memory.main.get_map() != 69:
        if memory.main.user_control():
            # Spheres, glyphs, and pedestals
            if checkpoint == 1:  # First glyph
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 3:  # Second glyph
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 7:  # First Besaid sphere
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 12:  # Insert Besaid sphere
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 20:  # Touch the hidden door glyph
                while memory.main.user_control():
                    pathing.set_movement([-13, -33])
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 23:  # Second Besaid sphere
                while memory.main.user_control():
                    pathing.set_movement([-14, 31])
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 26:  # Insert Besaid sphere, and push to completion
                while memory.main.user_control():
                    pathing.set_movement([-13, -60])
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_control_3()
                if game_vars.use_pause():
                    memory.main.wait_frames(2)
                while memory.main.get_map() == 122:
                    FFXC.set_movement(0, 1)
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 34:  # Night, talk to Yuna and Wakka
                FFXC.set_movement(-1, -1)
                memory.main.await_event()
                FFXC.set_neutral()

                memory.main.click_to_diag_progress(47)  # Wakka, "She's cute, ya?"
                while memory.main.shop_menu_dialogue_row() != 1:
                    xbox.tap_down()
                xbox.tap_b()
                checkpoint += 1
            elif checkpoint == 36:  # Sleep tight
                memory.main.click_to_event_temple(3)
                checkpoint += 1
            elif checkpoint > 15 and checkpoint < 37 and memory.main.get_map() == 252:
                checkpoint = 37
            elif checkpoint == 39:  # Dream about girls
                memory.main.click_to_event_temple(7)
                checkpoint += 1

            # General pathing
            elif pathing.set_movement(BesaidTrials.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()

            elif checkpoint == 32 and memory.main.menu_open():
                # Name for Valefor
                xbox.name_aeon("Valefor")
                checkpoint += 1  # To the night scene

            # map changes
            elif checkpoint < 29 and memory.main.get_map() == 83:
                checkpoint = 29


def leaving():
    logger.info("Ready to leave Besaid")
    memory.main.click_to_control()
    checkpoint = 0

    while memory.main.get_map() != 301:
        if memory.main.user_control():
            # Events
            if checkpoint == 0:  # Back into the village
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 3:  # Tent 1
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 5:  # Shopkeeper
                while memory.main.user_control():
                    pathing.set_movement([1, 15])
                    xbox.tap_b()
                FFXC.set_neutral()
                while memory.main.shop_menu_dialogue_row() != 1:
                    xbox.tap_down()
                xbox.tap_b()
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 7:  # Exit tent
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 9:  # Tent 2
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 11:  # Good doggo
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 13:  # Exit tent
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 16:  # Exit the front gates
                memory.main.click_to_event_temple(4)
                checkpoint += 1
            elif checkpoint == 18:  # First tutorial
                logs.write_rng_track("###########################")
                logs.write_rng_track("Pre-tutorial array")
                logs.write_rng_track(memory.main.rng_10_array(array_len=1))
                logger.debug("Tutorial - Tidus and Wakka")
                FFXC.set_movement(1, -1)
                memory.main.click_to_event()
                FFXC.set_neutral()
                memory.main.click_to_control()
                checkpoint += 1
            elif checkpoint == 23:  # Second tutorial
                logger.debug("Tutorial - Lulu magic")
                while memory.main.user_control():
                    FFXC.set_movement(1, 0)
                FFXC.set_neutral()
                xbox.click_to_battle()
                battle.main.attack("none")
                xbox.click_to_battle()
                battle.main.thunder("none")
                memory.main.click_to_control()
                checkpoint += 1
            elif checkpoint == 24:  # Hilltop
                memory.main.click_to_event_temple(2)
                logger.debug(f"Ready for SS Liki menu: {game_vars.early_tidus_grid()}")
                if memory.main.get_tidus_slvl() >= 3:
                    menu.liki()
                    game_vars.early_tidus_grid_set_true()
                logs.write_rng_track("###########################")
                logs.write_rng_track("Pre-Kimahri array")
                logs.write_rng_track(memory.main.rng_10_array(array_len=1))
                checkpoint += 1
            elif checkpoint in [59]:  # Beach, save sphere
                logs.write_rng_track("###########################")
                logs.write_rng_track("Pre-Sin array")
                logs.write_rng_track(memory.main.rng_10_array(array_len=1))
                checkpoint += 1
            elif checkpoint in [60]:  # Beach, save sphere
                checkpoint += 1
            elif checkpoint == 70:
                checkpoint -= 2

            # General pathing
            elif pathing.set_movement(Besaid2.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                xbox.skip_scene(fast_mode=True)
            # Kimahri fight
            elif checkpoint > 25 and checkpoint < 30 and screen.battle_screen():
                FFXC.set_neutral()
                heal_count = 0
                while memory.main.battle_active():
                    if screen.battle_screen():
                        battle_hp = memory.main.get_battle_hp()
                        enemy_hp = memory.main.get_enemy_current_hp()
                        if (
                            not game_vars.early_tidus_grid()
                            and Tidus.in_danger(120, combat=True)
                            and enemy_hp[0] > 119
                        ):
                            if Tidus.next_crit(12) == 2:
                                battle.main.attack("none")
                            else:
                                battle.main.use_potion_character(Tidus, "l")
                                heal_count += 1
                        else:
                            battle.main.attack("none")
                    elif memory.main.diag_skip_possible():
                        xbox.tap_b()
                # logs.write_stats("Kimahri heal count:")
                # logs.write_stats(heal_count)
                memory.main.click_to_control()
            # Valefor summon tutorial
            elif (
                checkpoint in [31, 32, 33, 34, 35, 36, 37, 38]
                and screen.battle_screen()
            ):
                xbox.click_to_battle()
                while not screen.turn_aeon():
                    if memory.main.turn_ready():
                        if Yuna.is_turn():
                            battle.main.aeon_summon(0)
                        elif screen.turn_aeon():
                            pass
                        elif not Yuna.active():
                            battle.main.buddy_swap(Yuna)
                        else:
                            battle.main.defend()
                while memory.main.battle_active():
                    if memory.main.turn_ready():
                        battle.main.aeon_spell(1)
                logger.info("Now to open the menu")
                memory.main.click_to_control()
                memory.main.update_formation(Tidus, Yuna, Lulu)
                checkpoint += 1
            elif checkpoint == 39 and screen.battle_screen():  # Dark Attack tutorial
                battle.main.escape_all()
                memory.main.click_to_control()
                memory.main.update_formation(Tidus, Wakka, Lulu)
                checkpoint += 1
            # One forced battle on the way out of Besaid
            elif checkpoint > 39 and screen.battle_screen():
                battle.main.besaid()

            # Map changes
            # Hilltop
            elif checkpoint > 10 and checkpoint < 24 and memory.main.get_map() == 67:
                checkpoint = 24
            # Kimahri map
            elif checkpoint < 27 and memory.main.get_map() == 21:
                checkpoint = 27
            elif checkpoint < 32 and memory.main.get_map() == 22:
                checkpoint = 32
            elif checkpoint < 51 and memory.main.get_map() == 20:
                checkpoint = 51
            elif checkpoint < 59 and memory.main.get_map() == 19:
                checkpoint = 59
