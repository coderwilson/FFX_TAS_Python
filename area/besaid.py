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
from area.dream_zan import split_timer
from paths.destro_spheres import besaid_destro_sphere

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
    
    checkpoint = 0
    if game_vars.platinum():
        # We grab Yuna's celestial item first.
        while checkpoint < 12:
            if memory.main.user_control():
                if checkpoint == 6:
                    pathing.approach_actor_by_id(20482)
                    memory.main.click_to_control()
                    checkpoint += 1
                elif pathing.set_movement(besaid_destro_sphere.execute(checkpoint)):
                    checkpoint += 1
                    logger.debug(f"Checkpoint {checkpoint}")

    # Pathing, lots of pathing.
    besaid_battles = 0
    good_battles = 0
    checkpoint = 0
    last_cp = 0
    while not (
        (memory.main.get_story_progress() == 119 and memory.main.diag_progress_flag() == 1) or
        memory.main.get_map() in [69,67]
    ):
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
                xbox.menu_b()
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
                if game_vars.story_mode():
                    logger.debug("Static time click")
                    memory.main.wait_seconds(10)
                    xbox.tap_confirm()
                    logger.debug("Click")
                memory.main.click_to_control() # Allows for story mode.
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
                if not game_vars.story_mode():
                    xbox.tap_b()
    
    split_timer()
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
                xbox.menu_b()
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
                if game_vars.story_mode():
                    logger.debug("Static time click")
                    memory.main.wait_seconds(10)
                    xbox.tap_confirm()
                    logger.debug("Click")
                memory.main.click_to_control() # Allows for story mode.
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
                if not game_vars.story_mode():
                    xbox.tap_b()
    logs.write_stats("piranha battles:")
    logs.write_stats(str(besaid_battles))
    # logs.write_stats("Optimal piranha battles:")
    # logs.write_stats(str(good_battles))


def night_scene():
    while memory.main.get_story_progress() < 190:
        if memory.main.user_control():
            if memory.main.get_story_progress() == 182:
                # Move towards Yuna.
                pathing.set_movement([60,230])
            else:
                # Move towards Wakka for sleep.
                pathing.approach_actor_by_id(5)
                FFXC.set_neutral()
        else:
            FFXC.set_neutral()
            story = memory.main.get_story_progress()
            dialog = memory.main.diag_progress_flag()
            #logger.debug(f"Story: {story} | dialog: {dialog}")
            if story == 182 and dialog == 47:  # She's cute, ya?
                memory.main.wait_frames(30)
                xbox.tap_down()
                xbox.tap_confirm()
                memory.main.wait_frames(3)
            elif story == 184 and dialog == 56:  # Ready for bed?
                xbox.tap_confirm()
            elif game_vars.story_mode():  # All other dialog, do not skip in story mode.
                pass
            else:  # All other scenarios, mash skip.
                xbox.tap_confirm()


def _distance(n1, n2):
    try:
        player1 = n1
        player2 = n2
        return abs(player1[1] - player2[1]) + abs(player1[0] - player2[0])
    except Exception as x:
        logger.exception(x)
        return 999


def trials(destro:bool=False):
    checkpoint = 0
    if game_vars.story_mode() or game_vars.platinum():
        destro=True
        memory.main.wait_seconds(7)
        xbox.tap_confirm()
    else:
        FFXC.set_neutral()

    while memory.main.get_map() == 122:
        if memory.main.user_control():
            # Spheres, glyphs, and pedestals
            if checkpoint == 1:  # First glyph
                pathing.approach_coords([-26, 141])

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
                logger.debug(f"Mark {checkpoint}")
                while memory.main.user_control():
                    pathing.set_movement([-13, -33])
                    xbox.tap_b()
                FFXC.set_neutral()
                logger.debug(f"Mark {checkpoint}")
                while not memory.main.user_control():
                    xbox.tap_confirm()
                logger.debug(f"Mark {checkpoint}")
                #memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 23:  # Second Besaid sphere
                logger.debug(f"Mark {checkpoint}")
                pathing.approach_coords([-14, 31], quick_return=True)
                FFXC.set_neutral()
                logger.debug(f"Mark {checkpoint}")
                memory.main.click_to_control_3()
                logger.debug(f"Mark {checkpoint}")
                checkpoint += 1
            elif checkpoint == 26:  # Insert Besaid sphere, and push to completion
                logger.debug(f"Mark {checkpoint}")
                pathing.approach_coords([-13, -63], quick_return=True)
                logger.debug(f"Mark {checkpoint}")
                memory.main.click_to_control_3()
                if destro:
                    checkpoint = 54
                else:
                    while memory.main.get_map() == 122:
                        FFXC.set_movement(0, 1)
                    FFXC.set_neutral()
                    checkpoint += 1
                logger.debug(f"Mark {checkpoint}")
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
                if game_vars.story_mode():
                    memory.main.click_to_control_3()
                checkpoint = 14
            elif checkpoint == 53:
                pathing.approach_coords([67, 3], quick_return=True)
                if game_vars.story_mode():
                    memory.main.click_to_control_3()
                checkpoint = 17
            elif checkpoint == 55:
                checkpoint += 1
            elif checkpoint == 58:
                pathing.approach_coords([93, 4], quick_return=True)
                if game_vars.story_mode():
                    memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 63:
                pathing.approach_coords([-14, 32], quick_return=True)
                if game_vars.story_mode():
                    memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 68:
                pathing.approach_coords([-72, 75], quick_return=True)
                if game_vars.story_mode():
                    memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 72:
                # Line up to finish pushing.
                FFXC.set_neutral()
                memory.main.check_near_actors(False, max_dist=50)
                memory.main.wait_frames(16)
                #while _distance(memory.main.get_coords(), BesaidTrials.execute(checkpoint)) > 1.5:
                while pathing.distance(1) > 9:
                    logger.debug(memory.main.get_coords())
                    pathing.set_movement(BesaidTrials.execute(checkpoint))
                    memory.main.wait_frames(2)
                    FFXC.set_neutral()
                    memory.main.wait_frames(3)

                while memory.main.get_map() == 122:
                    pathing.set_movement([-14,-150])
                FFXC.set_neutral()
                if memory.main.get_story_progress() > 2000:
                    return
                else:
                    checkpoint = 27

            # General pathing
            elif pathing.set_movement(BesaidTrials.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
                if checkpoint in [70,71,72]:
                    memory.main.check_near_actors(False)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()

    logger.debug("Besaid Trials complete. Let's go meet the summoner!")
    while memory.main.get_map() != 252:
        if memory.main.user_control():
            if memory.main.get_map() == 100:
                night_scene()
                checkpoint = 35
            
            # General pathing
            if pathing.set_movement(BesaidTrials.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
            elif checkpoint == 32 and memory.main.menu_open():
                # Name for Valefor
                logger.debug("Waiting for Valefor naming screen.")
                xbox.name_aeon("Valefor")
                checkpoint += 1  # To the night scene
                logger.debug(f"Checkpoint {checkpoint}")

            # map changes
            elif checkpoint < 29 and memory.main.get_map() == 83:
                checkpoint = 29

    
    logger.debug("Mark - start of dream sequence")
    memory.main.await_control()
    while not pathing.set_movement([336,73]):
        pass
    while not pathing.set_movement([341,110]):
        pass
    while memory.main.user_control():
        FFXC.set_movement(0,1)
    FFXC.set_neutral()
    if not game_vars.story_mode():
        memory.main.click_to_control()


def leaving(checkpoint = 17):
    logger.info("Ready to leave Besaid")
    if game_vars.story_mode():
        checkpoint = 0
        memory.main.await_control()
    memory.main.click_to_control()
    while not pathing.set_movement([0, 23]):
        pass
    while not pathing.set_movement([0, -42]):
        pass
    if game_vars.platinum():
        pathing.primer()
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
                FFXC.set_movement(1,0)
                memory.main.await_event()
                FFXC.set_neutral()
                if game_vars.story_mode():
                    memory.main.await_control()
                    pathing.approach_coords([5,-47],quick_return=True)
                    FFXC.set_neutral()
                    memory.main.wait_seconds(21)
                    xbox.tap_confirm()
                    memory.main.await_control()
                else:
                    memory.main.click_to_control()
                logger.debug(f"Ready for SS Liki menu: {game_vars.early_tidus_grid()}")
                if memory.main.get_tidus_slvl() >= 3:
                    menu.liki()
                    game_vars.early_tidus_grid_set_true()
                checkpoint += 1
            elif checkpoint in [59]:  # Beach, save sphere
                checkpoint += 1
            elif checkpoint in [60]:  # Beach, save sphere
                # here
                save_sphere.touch_and_go()
                checkpoint += 1
            elif checkpoint == 65 and not gil_guy:
                pathing.approach_actor_by_index(13)
                gil_guy = True
                memory.main.click_to_control_3()
            elif checkpoint == 70:
                checkpoint -= 2

            # General pathing
            elif pathing.set_movement(Besaid2.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
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
                and memory.main.battle_active()
            ):
                battle.boss.summon_tutorial()
                logger.info("Now to open the menu")
                memory.main.click_to_control_3()
                memory.main.update_formation(Tidus, Yuna, Lulu)
                checkpoint += 1
            elif checkpoint == 39 and screen.battle_screen():  # Dark Attack tutorial
                battle.boss.dark_attack_tutorial()
                memory.main.click_to_control_3()
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
