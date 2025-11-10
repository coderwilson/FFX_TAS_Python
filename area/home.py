import logging
import math

import battle.main
import memory.main
import menu
import pathing
import save_sphere
import vars
import xbox
import time
import random
#import rng_track
from paths import BikanelDesert, BikanelHome
from players import Auron, Kimahri, Rikku, Tidus, Wakka, Lulu
from reset import reset_to_main_menu
from area.dream_zan import new_game, split_timer
from load_game import load_save_num
from battle.main import guards_report_items
from json_ai_files.write_seed import write_big_text

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def quick_reset():
    reset_to_main_menu()
    new_game(gamestate="reload_autosave")
    load_save_num(0)


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


def reverse_battle_rng():
    FFXC.set_neutral()
    memory.main.check_near_actors()
    pathing.approach_actor_by_id(actor_id=20496)
    FFXC.set_neutral()
    memory.main.wait_frames(63)

    # Start battle
    xbox.tap_down()
    xbox.tap_b()
    xbox.tap_b()
    xbox.click_to_battle()

    # Escape and back out of menu
    battle.main.flee_all(wrap_up_battle=False)
    while not memory.main.user_control():
        xbox.tap_a()


def desert():
    logger.info("Desert")

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
    if memory.main.get_item_slot(39) == 255:
        items_needed_total = 6
    else:
        items_needed_total = 8
        # The extra one is for Ghost. If no silence grenade, no need for 8.
    items_needed = items_needed_total - sum(steal_items)

    menu.equip_sonic_steel()
    memory.main.close_menu()
    
    #rng_track.print_manip_info()
    #logger.manip(f"Drop counts to Evrae: {rng_track.desert_to_evrae_equip_drop_count()}")
    flip_rng = "flip_bikanel" in game_vars.run_modifier()
    # flip_rng = True  # Override for testing.

    checkpoint = 2  # This is so we can create a save file properly.
    first_format = False
    sandy1 = False
    timer_start = False
    start_time = time.time()
    next_enc_dist = 999
    get_primer1 = False # Salvage ship
    get_primer2 = game_vars.platinum() # SS Liki
    get_primer3 = game_vars.platinum() # SS Winno
    get_primer4 = game_vars.platinum() # Thunder Plains (Rin)
    get_primer5 = game_vars.platinum() # always spawns in desert
    get_primer6 = game_vars.platinum() # always spawns in desert

    # This is to recover from game-over state.
    if memory.main.get_map() != 129:
        if memory.main.get_map() == 136:
            if memory.main.get_story_progress() == 1720:
                checkpoint = 23
                get_primer2 = False
                get_primer3 = False
            else:
                checkpoint = 10
                get_primer2 = False
        if memory.main.get_map() == 137:
            checkpoint = 39
            get_primer2 = False
            get_primer3 = False
            get_primer4 = False
            get_primer5 = False
            get_primer6 = False
        if memory.main.get_map() == 138:
            checkpoint = 50
            get_primer2 = False
            get_primer3 = False
            get_primer4 = False
            get_primer5 = False
            get_primer6 = False
        

    while memory.main.get_map() != 130:
        if memory.main.user_control():
            #logger.debug(f"Checkpoint {checkpoint}")
            # RNG manip first
            if checkpoint == 6 and flip_rng:
                checkpoint = 85
            if checkpoint == 91:
                checkpoint = 9

            # Map changes
            elif checkpoint < 10 and memory.main.get_map() == 136:
                checkpoint = 10
            elif checkpoint == 11 and len(memory.main.get_order_seven()) > 4:
                checkpoint += 1
            elif checkpoint < 39 and memory.main.get_map() == 137:
                checkpoint = 39
            elif checkpoint < 50 and memory.main.get_map() == 138:
                checkpoint = 50
            
            # Platinum specific stuff (mostly primers)
            elif checkpoint == 5 and get_primer1:
                logger.manip("Primer 1")
                pathing.primer()
                get_primer1 = False
            elif checkpoint == 8 and get_primer2:
                logger.manip("Primer 2")
                get_primer2 = not pathing.primer()
            elif checkpoint == 11 and get_primer3:
                logger.manip("Primer 3")
                get_primer3 = not pathing.primer()
            elif checkpoint == 36 and get_primer4:
                logger.manip("Primer 4")
                if pathing.set_movement([437,645]):
                    get_primer4 = not pathing.primer()
            elif checkpoint == 39 and get_primer5:
                logger.manip("Primer 5")
                checkpoint = 100
            elif checkpoint == 101:
                switch = 0
                while not memory.main.battle_active():
                    if switch % 2 == 0:
                        FFXC.set_movement(-1,0)
                    else:
                        FFXC.set_movement(1,0)
                    memory.main.wait_frames(12)
                    switch += 1
                FFXC.set_neutral()
                battle.main.flee_all()
                memory.main.click_to_control_3()
                pathing.primer()
                get_primer5 = False
                checkpoint += 1
            elif checkpoint == 103:
                checkpoint = 42
            elif checkpoint == 47 and get_primer6:
                logger.manip("Primer 6")
                checkpoint = 104
            elif checkpoint == 106:
                switch = 0
                while not memory.main.battle_active():
                    if switch % 2 == 0:
                        FFXC.set_movement(-1,0)
                    else:
                        FFXC.set_movement(1,0)
                    memory.main.wait_frames(12)
                    switch += 1
                FFXC.set_neutral()
                battle.main.flee_all()
                memory.main.click_to_control_3()
                pathing.primer()
                checkpoint += 1
                get_primer6 = False
            elif checkpoint == 108:
                checkpoint = 47


            # Nemesis stuff
            elif checkpoint == 47 and (
                game_vars.nemesis() or 
                game_vars.story_mode() or
                game_vars.platinum()
            ):
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
                    memory.main.click_to_control_3()
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
                    memory.main.click_to_control_3()
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
                if Auron.overdrive_percent() < 100 and not sandy1:
                    checkpoint -= 2
                else:
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
            elif checkpoint == 88:
                reverse_battle_rng()
                checkpoint += 1
            elif checkpoint == 12 and not first_format:
                first_format = True
                memory.main.update_formation(Tidus, Wakka, Lulu)

            # Sandragora skip logic
            elif checkpoint == 57:
                #if next_enc_dist < 275:
                #    FFXC.set_movement(1,0)
                #    memory.main.wait_seconds(1)
                checkpoint += 1
            elif checkpoint == 60:
                if manip_drops:
                    FFXC.set_movement(-1, 1)
                    memory.main.await_event()
                    manip_drops = False
                    checkpoint -= 2
                elif memory.main.get_coords()[1] < 811:
                    # Dialing in. 810 works 95%, but was short once.
                    # 812 will sometimes get stuck with an incomplete push.
                    FFXC.set_movement(0, 1)
                else:
                    FFXC.set_neutral()
                    checkpoint += 1
            elif checkpoint == 61:
                if not timer_start:
                    start_time = time.time()
                    logger.debug("Sandragora Skip timer start")
                    timer_start = True
                elif time.time() - start_time >= 8:
                    logger.warning("Stuck attempting Sandy Skip. Triggering un-stuck logic.")
                    FFXC.set_movement(-1,0)
                    memory.main.wait_frames(15)
                    FFXC.set_neutral()
                    checkpoint = 58
                    timer_start = False
                elif memory.main.get_coords()[1] < 810:
                    # Accidentally encountered Sandragora, must re-position.
                    checkpoint -= 2
                elif memory.main.get_coords()[1] < 840:
                    FFXC.set_neutral()
                else:
                    checkpoint += 1

            # After Sandy2 logic
            elif checkpoint == 64:
                if (
                    items_needed > 0
                ):  # Cannot move on if we're short on throwable items
                    checkpoint -= 2
                #elif need_speed:  # Cannot move on if we're short on speed spheres
                #    checkpoint -= 2
                elif 1 in memory.main.ambushes() and Kimahri.overdrive_percent() < 100:
                    # Avoids game-over state on the second battle, new with Terra skip
                    checkpoint -= 2
                elif Rikku.overdrive_percent() < 100:
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
            if memory.main.battle_active():  # Lots of battle logic here.
                if checkpoint < 7 and memory.main.get_encounter_id() == 197:
                    # First battle in desert
                    if not battle.main.zu():
                        return False
                elif memory.main.get_encounter_id() == 234:  # Sandragora logic
                    logger.info("Sandragora fight")
                    if checkpoint < 55:
                        if not sandy1:
                            battle.main.sandragora(1)
                            next_enc_dist = memory.main.distance_to_encounter()
                            logger.warning(f"Next Enc distance: {next_enc_dist}")
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
                    if memory.main.game_over():
                        return False

                # After-battle logic
                memory.main.click_to_control()
                steal_items = battle.main.update_steal_items_desert()
                guards_report_items()
                # Come back to this. Could save some runs.
                # if 1 in memory.main.ambushes():
                #    menu.main.overworld_use_item()

                # First, check and update party format and health.
                need_heal = False
                if checkpoint > 30 and (Wakka.hp() < 600 or Kimahri.hp() < 600):
                    need_heal = True
                if checkpoint > 10:
                    if checkpoint < 23 and checkpoint > 10:
                        memory.main.update_formation(Tidus, Wakka, Auron,full_menu_close=not need_heal)
                    elif (
                        not charge_state or 
                        items_needed > 0 or
                        need_power or
                        need_speed
                    ):
                        memory.main.update_formation(Tidus, Wakka, Rikku,full_menu_close=not need_heal)
                    else:  # Catchall
                        memory.main.update_formation(Tidus, Wakka, Rikku,full_menu_close=not need_heal)
                    if need_heal:
                        menu.overworld_use_item(item_to_use=1,heal_array=[3,4],full_menu_close=True)
                        memory.main.close_menu()

                # Next, figure out how many items we need.
                logger.debug(f"Items status: {steal_items}")
                items_needed = items_needed_total - sum(steal_items)

                # Finally, check for other factors and report to console.
                charge_state = memory.main.overdrive_state()[6] == 100
                need_speed, need_power = check_spheres()
                logger.debug("Flag statuses")
                logger.debug(f"Rikku is charged up: {charge_state}")
                logger.manip(f"Additional items needed before Home: {items_needed}")
                #rng_track.print_manip_info()
                #logger.manip(
                #    f"Drop counts to Evrae: {rng_track.desert_to_evrae_equip_drop_count()}"
                #)
                if checkpoint == 60:
                    checkpoint = 58
                    
                if timer_start:
                    start_time = time.time()
                    logger.debug("Sandragora Skip timer restart")
                
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
            elif checkpoint == 53:
                xbox.tap_confirm()

    return True

def primer_and_save():
    
    if game_vars.platinum():
        while not pathing.set_movement([-34,-108]):
            pass
        while not pathing.set_movement([-81,-78]):
            pass
        pathing.primer()

    # Move to save sphere
    checkpoint = 0
    write_big_text("")
    while checkpoint < 7:
        if pathing.set_movement(BikanelHome.execute(checkpoint)):
            checkpoint += 1
            logger.debug(f"Checkpoint {checkpoint}")


def find_summoners():
    logger.info("Desert complete. Starting Home section")
    if game_vars.story_mode():
        menu.equip_weapon(character=2, ability=0x8002, full_menu_close=False)
    if game_vars.get_blitz_win():
        menu.home_grid()
    memory.main.update_formation(Tidus, Auron, Rikku)
    memory.main.close_menu()
    od_learns = 2
    ambush_check = memory.main.ambushes()
    last_story = memory.main.get_story_progress()
    last_dialog = memory.main.diag_progress_flag()


    checkpoint = 7
    hall_primer = game_vars.platinum()
    while memory.main.get_map() != 219:
        if memory.main.user_control():
            coords = memory.main.get_coords()

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
                checkpoint = 26
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
                if game_vars.platinum():
                    pathing.primer()
                FFXC.set_movement(1, -1)
                memory.main.await_event()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 88:
                checkpoint = 21
            elif checkpoint == 20:
                if game_vars.platinum() or not game_vars.get_blitz_win():
                    checkpoint = 81
                else:
                    checkpoint = 21
            elif checkpoint in [24, 25] and 1 in ambush_check:
                checkpoint = 22
            elif checkpoint == 23 and hall_primer:
                checkpoint = 90  # Primer branch
            elif checkpoint == 93:
                pathing.primer()
                hall_primer = False
                checkpoint += 1
            elif checkpoint == 96:
                checkpoint = 24

            elif checkpoint == 31 and not game_vars.csr():
                #memory.main.click_to_event_temple(6)
                FFXC.set_movement(-1,0)
                memory.main.await_event()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 39:
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 42:
                FFXC.set_movement(0,1)
                memory.main.await_event()
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
                    od_learns = battle.main.home_1()
                    if memory.main.game_over():
                        quick_reset()
                    else:
                        memory.main.update_formation(Tidus, Auron, Lulu)
                elif memory.main.get_encounter_id() == 419:
                    if memory.main.get_map() == 280:
                        logger.info("Home, battle 2")
                        od_learns = battle.main.home_2(od_learns)
                        if memory.main.game_over():
                            quick_reset()
                        else:
                            memory.main.update_formation(Tidus, Auron, Lulu)
                        od_learns = min(od_learns, 2)
                    else:
                        logger.info("Home, bonus battle for Blitz loss")
                        od_learns = battle.main.home_3(od_learns)
                        if memory.main.game_over():
                            quick_reset()
                        else:
                            memory.main.update_formation(Tidus, Auron, Lulu)
                elif memory.main.get_encounter_id() == 420:
                    logger.info("Home, final battle")
                    battle.main.home_4()
                    memory.main.update_formation(Tidus, Rikku, Kimahri)
                else:
                    logger.debug(f"Flee from battle: {memory.main.get_encounter_id()}")
                    battle.main.flee_all()
                battle.main.wrap_up()
                ambush_check = memory.main.ambushes()
            elif memory.main.menu_open():
                xbox.tap_confirm()
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()

            # Just so the console has something to do
            if (
                last_story != memory.main.get_story_progress() or
                last_dialog != memory.main.diag_progress_flag()
            ):
                last_story = memory.main.get_story_progress()
                last_dialog = memory.main.diag_progress_flag()
                logger.debug(f"Progress update - story: {last_story} | dialog {last_dialog}")

    split_timer()
    logger.info("Let's go get that airship!")
    # Summoner's Sanctum room
    while memory.main.get_map() != 303:
        coords = memory.main.get_coords()
        if coords[0] < 100:
            pathing.set_movement([105,-40])
        else:
            pathing.set_movement([160,-50])
    # Ramp to airship
    while memory.main.get_map() == 303:
        coords = memory.main.get_coords()
        if coords[0] > 185:
            if coords[1] < 56:
                pathing.set_movement([190,60])
            else:
                pathing.set_movement([165,58])
        else:
            pathing.set_movement([80,60])

    # Now aboard the airship
    FFXC.set_neutral()
    if game_vars.story_mode():
        logger.debug("Story mode, no need to wait on these scenes.")
        memory.main.await_control()
        return
    if not game_vars.csr():
        memory.main.click_to_diag_progress(27)
        while not memory.main.cutscene_skip_possible():
            if not game_vars.story_mode():
                xbox.tap_confirm()
        xbox.skip_scene()
        memory.main.click_to_diag_progress(105)
        memory.main.wait_frames(15)
        xbox.tap_confirm()
        memory.main.wait_frames(15)
        xbox.skip_scene()

    while not memory.main.user_control():
        if memory.main.diag_skip_possible() and not game_vars.story_mode():
            xbox.tap_b()
        elif memory.main.cutscene_skip_possible():
            xbox.skip_scene()
    logger.info("Airship is good to go. Now for Yuna.")
