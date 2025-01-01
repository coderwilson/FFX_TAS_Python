import logging

import battle.boss
import battle.main
import logs
import memory.main
import menu
import pathing
import screen
import vars
import xbox
from paths import Besaid1, Besaid2, BesaidTrials
from players import Lulu, Tidus, Wakka, Yuna
import save_sphere

FFXC = xbox.controller_handle()
game_vars = vars.vars_handle()

logger = logging.getLogger(__name__)


def beach(lagoon_strats):
    logger.info("Starting Besaid section. Beach")

    lagoon_encounter = 0

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
            logger.debug(f"Checkpoint {checkpoint}")
            last_cp = checkpoint

        # map changes
        if checkpoint < 2 and memory.main.get_map() == 20:
            checkpoint = 2
            logger.debug(f"Map change. Checkpoint {checkpoint}")
        elif checkpoint < 6 and memory.main.get_map() == 41:
            checkpoint = 6
            logger.debug(f"Map change. Checkpoint {checkpoint}")
        elif checkpoint < 22 and memory.main.get_map() == 69:
            checkpoint = 22
            logger.debug(f"Map change. Checkpoint {checkpoint}")
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
                logging.debug(f"Lagoon Encounter: {lagoon_encounter} / Strat: {lagoon_strats[lagoon_encounter]}")
                battle.main.piranhas(strat=lagoon_strats[lagoon_encounter])
                lagoon_encounter += 1
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


def night_scene():
    memory.main.await_control()
    while not pathing.set_movement([18,186]):
        pass
    memory.main.check_near_actors(False)
    FFXC.set_movement(-1, -1)
    memory.main.await_event()
    FFXC.set_neutral()
    memory.main.click_to_control()
    pathing.approach_actor_by_id(5)
    FFXC.set_neutral()
    memory.main.click_to_control()
    


def trials(destro:bool=False):
    checkpoint = 0

    while memory.main.get_map() != 60:
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
                if destro:
                    checkpoint = 50
                else:
                    checkpoint += 1
            elif checkpoint == 20:  # Touch the hidden door glyph
                while memory.main.user_control():
                    pathing.set_movement([-13, -33])
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 23:  # Second Besaid sphere
                pathing.approach_coords([-14, 31])
                checkpoint += 1
            elif checkpoint == 26:  # Insert Besaid sphere, and push to completion
                pathing.approach_coords([-13, -60])
                if destro:
                    checkpoint = 54
                else:
                    while memory.main.get_map() == 122:
                        FFXC.set_movement(0, 1)
                    FFXC.set_neutral()
                    checkpoint += 1
            elif memory.main.get_map() == 100:
                night_scene()
                checkpoint = 35
            
            # Destro sphere pieces
            elif checkpoint == 16 and destro:
                checkpoint = 52
            elif checkpoint == 51:
                FFXC.set_neutral()
                memory.main.check_near_actors(False)
                pathing.approach_actor_by_id(20597)
                checkpoint = 14
            elif checkpoint == 53:
                pathing.approach_coords([67, 3])
                checkpoint = 17
            elif checkpoint == 58:
                pathing.approach_coords([93, 4])
                checkpoint += 1
            elif checkpoint == 63:
                pathing.approach_coords([-14, 32])
                checkpoint += 1
            elif checkpoint == 68:
                pathing.approach_coords([-72, 75])
                checkpoint += 1
            elif checkpoint == 72:
                FFXC.set_neutral()
                memory.main.wait_frames(16)
                while memory.main.get_map() != 103:
                    FFXC.set_movement(-1,0)
                FFXC.set_neutral()
                if memory.main.get_story_progress() > 2000:
                    return
                else:
                    checkpoint = 27


            # After trials pieces
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
                logger.debug(f"Checkpoint {checkpoint}")
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


def leaving(checkpoint = 17):
    logger.info("Ready to leave Besaid")
    memory.main.click_to_control()
    while not pathing.set_movement([0, 23]):
        pass
    while not pathing.set_movement([0, -35]):
        pass
    pathing.set_movement([0, -100])
    memory.main.await_event()
    FFXC.set_neutral()
    gil_guy = False
    
    if memory.main.get_map() == 21:
        checkpoint = 25

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
                battle.boss.tidus_wakka_tutorial()
                FFXC.set_movement(1, -1)
                checkpoint += 1
            elif checkpoint == 23:  # Second tutorial
                logger.debug("Tutorial - Lulu magic")
                while memory.main.user_control():
                    FFXC.set_movement(1, 0)
                battle.boss.black_magic_tutorial()
                FFXC.set_neutral()
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
                # here
                save_sphere.touch_and_go()
                checkpoint += 1
            elif checkpoint == 65 and not gil_guy:
                pathing.approach_actor_by_index(13)
                gil_guy = True
                memory.main.click_to_control()
            elif checkpoint == 70:
                checkpoint -= 2

            # General pathing
            elif pathing.set_movement(Besaid2.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                xbox.skip_scene(fast_mode=True)
            # Kimahri fight
            elif checkpoint > 25 and checkpoint < 30 and screen.battle_screen():
                boss_kim_success = battle.boss.kimahri()
                if not boss_kim_success:
                    return False
            # Valefor summon tutorial
            elif (
                checkpoint in [31, 32, 33, 34, 35, 36, 37, 38]
                and screen.battle_screen()
            ):
                battle.boss.summon_tutorial()
                logger.info("Now to open the menu")
                memory.main.click_to_control()
                memory.main.update_formation(Tidus, Yuna, Lulu)
                checkpoint += 1
            elif checkpoint == 39 and screen.battle_screen():  # Dark Attack tutorial
                battle.boss.dark_attack_tutorial()
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
    return True
