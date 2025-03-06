import logging

import battle.boss
import battle.main
import logs
import memory.main
from memory.main import check_near_actors
import menu
import pathing
from pathing import approach_coords
import save_sphere
import vars
import xbox
from paths import Kilika1, Kilika2, Kilika3, KilikaTrials
from players import Tidus, Wakka, Yuna, Lulu, Valefor

logger = logging.getLogger(__name__)
FFXC = xbox.controller_handle()
game_vars = vars.vars_handle()


def arrival():
    # For certain seed/s, preferable to get luck sphere just to manipulate battles.
    # if memory.main.rng_seed() == 31 and game_vars.skip_kilika_luck():
    #    game_vars.dont_skip_kilika_luck()
    game_vars.dont_skip_kilika_luck()

    logs.write_rng_track("Kilika start, RNG01")
    logs.write_rng_track(memory.main.rng_01())

    logger.info("Arrived at Kilika docks.")
    memory.main.click_to_control()

    checkpoint = 0
    while memory.main.get_map() != 18:
        if memory.main.user_control():
            # events
            if checkpoint == 4:  # Move into Yunas dance
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 6:  # Move into Yuna's dance
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 8:  # Exit the inn
                # Can be improved, there's a tiny ledge to get stuck on.
                FFXC.set_movement(-1, -1)
                memory.main.await_event()
                memory.main.wait_frames(5)
                memory.main.await_control()
                checkpoint += 1
            elif checkpoint == 12:  # Back to first map
                memory.main.click_to_event_temple(3)
                checkpoint += 1
            elif checkpoint == 16:  # Talking to Wakka
                memory.main.click_to_event_temple(1)
                checkpoint += 1
            elif checkpoint == 18:  # Back to the map with the inn
                memory.main.click_to_event_temple(7)
                checkpoint += 1

            # General pathing
            elif pathing.set_movement(Kilika1.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")

        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                xbox.skip_scene_spec()

            # Map changes
            elif checkpoint < 7 and memory.main.get_map() == 152:
                checkpoint = 7


def select_best_of_two(coming_battles):
    if coming_battles == [["dinonix", "killer_bee"], ["dinonix", "killer_bee"]]:
        return 99
    priority = [
        ["ragora", "killer_bee", "killer_bee"],
        ["dinonix", "yellow_element", "killer_bee"],
        ["yellow_element", "killer_bee"],
        ["ragora"],
        ["dinonix", "yellow_element"],
    ]
    for i in range(len(priority)):
        if priority[i] in coming_battles:
            logger.debug(f"Best charge, battle num: {priority[i]}")
            return priority[i]
    return 99


def forest_1():
    logger.info("Kilika forest 1")
    kilika_battles = 0
    best_of_two = 99  # Used to find the best battle coming up.
    advances = 2  # Used to find the best battle coming up.
    next_battle = []
    import rng_track
    save_after_pray = False
    if game_vars.story_mode():
        save_after_pray = True


    game_vars.dont_skip_kilika_luck()

    valefor_charge = Valefor.overdrive_percent() >= 20
    if game_vars.csr():
        checkpoint = 0
    else:
        checkpoint = 2
    while not memory.main.get_map() in [108,44]:  # All the way into the trials
        if checkpoint == 101:  # Into the trials
            if not memory.main.user_control():
                FFXC.set_neutral()
                xbox.tap_b()
            elif memory.main.get_coords()[0] > 3:
                FFXC.set_movement(-1, 1)
            elif memory.main.get_coords()[0] < -3:
                FFXC.set_movement(1, 1)
            else:
                FFXC.set_movement(0, 1)
        elif memory.main.user_control():
            if checkpoint == 81 or checkpoint == 82:
                if valefor_charge:
                    checkpoint = 83
            if checkpoint == 83 and not valefor_charge:
                checkpoint = 81
            if checkpoint == 83 and memory.main.get_map() == 65:
                checkpoint = 84
            if checkpoint == 37 and game_vars.skip_kilika_luck():
                checkpoint = 60

            # events
            if checkpoint == 9:  # Chest with Wakkas weapon Scout
                memory.main.click_to_event_temple(0)
                menu.woods_menuing()
                # memory.main.update_formation(Tidus, Wakka, Lulu)
                checkpoint += 1
            elif checkpoint == 47:  # Luck sphere chest
                luck_slot = memory.main.get_item_slot(94)
                if luck_slot == 255:
                    pathing.set_movement([-250, 200])
                    xbox.tap_b()
                else:
                    checkpoint += 1
            elif checkpoint == 86:
                save_sphere.touch_and_go()
                memory.main.update_formation(Tidus, Wakka, Yuna)
                if not game_vars.did_full_kilika_menu():
                    menu.geneaux()
                memory.main.close_menu()
                checkpoint += 1
            elif checkpoint == 99:  # Lord O'holland
                pathing.approach_actor_by_id(5)  # Wakka is party member 4, ID 5
                FFXC.set_neutral()
                if game_vars.story_mode():
                    memory.main.wait_seconds(6)
                    xbox.tap_confirm()
                    memory.main.await_control()
                else:
                    memory.main.click_to_control_dumb()
                checkpoint += 1
            elif checkpoint == 100 and save_after_pray:
                save_sphere.touch_and_go()
                save_after_pray = False

            # General pathing
            elif pathing.set_movement(Kilika2.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")

        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                if checkpoint < 9:
                    battle.main.lancet_tutorial()
                    memory.main.update_formation(Tidus, Wakka, Lulu)
                    while best_of_two == 99:
                        next_two = rng_track.coming_battles(
                            area="kilika_woods", battle_count=advances
                        )
                        best_of_two = select_best_of_two(next_two)
                        advances += 1
                        if advances > 150:
                            logger.manip("No valid battles.")
                            break
                    next_battle = rng_track.coming_battles(
                        area="kilika_woods", battle_count=1
                    )[0]
                    logger.debug(f"Next Battle: {next_battle}")
                elif checkpoint > 86:
                    battle.boss.geneaux()
                else:
                    logger.debug(f"This should be battle number: {kilika_battles}")
                    logger.debug(f"Reminder (north-bound only): {best_of_two}")
                    valefor_charge = battle.main.kilika_woods(
                        valefor_charge, best_of_two, next_battle
                    )
                    next_battle = rng_track.coming_battles(
                        area="kilika_woods", battle_count=1
                    )[0]
                    logger.debug(f"{next_battle}")
                    kilika_battles += 1
                memory.main.update_formation(Tidus, Wakka, Lulu)
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
            elif checkpoint == 47 and game_vars.story_mode():
                # Story mode needs a little help with the Luck chest.
                xbox.tap_confirm()

            # Map changes
            elif checkpoint < 84 and memory.main.get_map() == 65:  # Stairs
                checkpoint = 84
            elif checkpoint < 94 and memory.main.get_map() == 78:  # Temple Entrance
                checkpoint = 94
            elif checkpoint < 96 and memory.main.get_map() == 96:  # Temple interior
                checkpoint = 96
    # logs.write_stats("Kilika battles (North):")
    # logs.write_stats(str(kilika_battles))
    # logs.write_stats("Kilika optimal battles (North):")
    # logs.write_stats(str(optimal_battles))
    
    if memory.main.get_map() != 108 and game_vars.csr():
        while not pathing.set_movement([-1,-4]):
            pass
        FFXC.set_neutral()
        xbox.tap_b()
        xbox.tap_b()
        xbox.tap_b()
        xbox.tap_b()
        if memory.main.user_control():
            while memory.main.user_control():
                xbox.tap_b()
        memory.main.await_control()
        while not pathing.set_movement([-1,100]):
            pass
    
    while memory.main.get_map() != 108:
        if memory.main.user_control():
            if pathing.set_movement([-1,282]):
                xbox.tap_b()
        else:
            FFXC.set_neutral()
            if game_vars.story_mode():
                if memory.main.get_actor_coords(0)[1] > 250:
                    memory.main.wait_seconds(2)  # So Tidus dialog plays
                    xbox.tap_confirm()  # Only if near the door.
                    memory.main.wait_seconds(27)  # So Tidus dialog plays
                # Else, don't skip dialog.
            else:
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
    logger.info("Kilika trials")
    memory.main.click_to_control()
    if game_vars.story_mode():
        destro = True
    checkpoint = 0
    while memory.main.get_map() != 45:
        if memory.main.user_control():
            # Spheres and glyphs
            if checkpoint == 2:  # First sphere
                approach_coords([-20,-200])
                checkpoint += 1
            elif checkpoint == 5:  # Insert and remove, opens door
                check_near_actors(False)
                approach_coords([11,-177])
                memory.main.wait_frames(3)
                approach_coords([11,-177])
                checkpoint += 1
            elif checkpoint == 9:  # Insert and remove, generate glyph
                check_near_actors(False)
                approach_coords([1,20])
                memory.main.wait_frames(3)
                approach_coords([1,20])
                checkpoint += 1
            elif checkpoint == 11:  # Put the sphere out of the way
                approach_coords([40,-21])
                checkpoint += 1
            elif checkpoint == 13:  # Touch glyph
                approach_coords([1,20])
                checkpoint += 1
            elif checkpoint == 18:  # Kilika sphere (in the way)
                approach_coords([56,175])
                checkpoint += 1
            elif checkpoint == 25:  # Kilika sphere (now out of the way)
                approach_coords([-40,-21])
                checkpoint += 1
            elif checkpoint == 27:  # Glyph sphere
                approach_coords([-20,-30])
                checkpoint += 1
            elif checkpoint == 33:  # Insert Glyph sphere
                approach_coords([56,175])
                checkpoint += 1
            elif checkpoint == 39:  # Pick up last Kilika sphere
                approach_coords([-40,-21])
                if destro:
                    checkpoint = 60
                else:
                    checkpoint += 1
            elif checkpoint == 50:  # Insert and remove, opens door
                approach_coords([12,280])
                memory.main.wait_frames(3)
                approach_coords([12,280])
                checkpoint += 1

            # Destro sphere pieces
            elif checkpoint == 61:
                approach_coords([-20,-30])
                checkpoint += 1
            elif checkpoint == 68:  # Reset glyph
                approach_coords([50,205])
                checkpoint += 1
            elif checkpoint == 71:
                # Line up to push north
                FFXC.set_neutral()
                memory.main.wait_frames(16)
                while _distance(memory.main.get_coords(), KilikaTrials.execute(checkpoint)) > 1.5:
                    logger.debug(memory.main.get_coords())
                    pathing.set_movement(KilikaTrials.execute(checkpoint))
                    memory.main.wait_frames(2)
                    FFXC.set_neutral()
                    memory.main.wait_frames(3)
                memory.main.wait_frames(9)
                while memory.main.get_coords()[1] < 180.6:
                    FFXC.set_movement(0,1)
                FFXC.set_neutral()
                memory.main.wait_frames(6)
                checkpoint += 1
                   
            elif checkpoint == 77:  # Push east towards hidden room
                while memory.main.get_actor_coords(0)[0] < 44:
                    FFXC.set_movement(1,-0.5)
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 81:  # Push podium north to where it locks in.
                FFXC.set_neutral()
                memory.main.wait_frames(16)
                while _distance(memory.main.get_coords(), [50,181]) > 1.5:
                    logger.debug(memory.main.get_coords())
                    pathing.set_movement([50,181])
                    memory.main.wait_frames(2)
                    FFXC.set_neutral()
                    memory.main.wait_frames(3)
                memory.main.wait_frames(9)
                while memory.main.get_actor_coords(0)[1] < 189.7:
                    FFXC.set_movement(0,1)
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 88:  # Pick up kilika sphere
                approach_coords([58,208])
                checkpoint += 1
            elif checkpoint == 91:  # Place kilika sphere
                approach_coords([15,282])
                checkpoint += 1
            elif checkpoint == 97:  # Pick up destro sphere
                approach_coords([86,174])
                checkpoint += 1
            elif checkpoint == 107:  # Place destro sphere
                approach_coords([58,208])
                checkpoint += 1
            elif checkpoint == 109:  # Open chest
                approach_coords([65,208])
                checkpoint += 1
            elif checkpoint == 113:  # Pick up kilika sphere
                approach_coords([15,282])
                checkpoint = 51  # Back to regular path
            
            # Chamber pieces
            elif checkpoint == 54 and memory.main.get_story_progress() > 2000:
                return
            elif checkpoint == 54 and not game_vars.csr():  # Talk to Wakka
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 56:  # Leave inner sanctum
                FFXC.set_movement(0, -1)
                memory.main.await_event()
                FFXC.set_neutral()
                xbox.name_aeon("Ifrit")  # Set Ifrit name
                checkpoint += 1
            elif checkpoint == 57:  # Leaving the temple
                memory.main.click_to_event_temple(4)
                checkpoint += 1

            # General pathing
            elif pathing.set_movement(KilikaTrials.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()

            # Map changes
            elif checkpoint < 53 and memory.main.get_map() == 45:  # Inner sanctum
                checkpoint = 53


def trials_end():
    logger.info("Kilika trials end")
    # Talking to Wakka
    while memory.main.get_story_progress() < 346:
        if memory.main.user_control():
            if memory.main.get_coords()[0] < -28:
                pathing.set_movement([-10, -23])
            else:
                pathing.set_movement([-20, 1])
                xbox.tap_b()
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()

    # Leave the chamber, then name Ifrit.
    memory.main.click_to_control_3()
    while memory.main.user_control():
        FFXC.set_movement(0, -1)
    FFXC.set_neutral()
    xbox.name_aeon("Ifrit")  # Set Ifrit name

    while memory.main.get_map() != 18:
        if memory.main.user_control():
            FFXC.set_movement(0, -1)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()


def forest_3():
    logger.info("Kilika forest 3")
    # First, re-order the party
    memory.main.update_formation(Tidus, Wakka, Lulu)
    kilika_battles = 0
    optimal_battles = 0
    valefor_charge = True  # No need to recharge.
    if game_vars.story_mode():
        valefor_charge = memory.main.overdrive_state()[7] == 20
    checkpoint = 0
    while memory.main.get_map() != 167:  # All the way to the boats
        if memory.main.user_control():
            # Events
            if checkpoint == 68:
                FFXC.set_movement(0, -1)
                memory.main.await_event()
                FFXC.set_neutral()
                xbox.skip_dialog(0.3)
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint < 53 and memory.main.get_map() == 46:  # Exit woods
                checkpoint = 53
            elif checkpoint < 64 and memory.main.get_map() == 16:  # Map with boat
                checkpoint = 64

            # General pathing
            elif pathing.set_movement(Kilika3.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                valefor_charge = battle.main.kilika_woods(valefor_charge)
                kilika_battles += 1
                if memory.main.get_encounter_id() in [32, 34, 37]:
                    optimal_battles += 1
                memory.main.update_formation(Tidus, Wakka, Lulu)
            elif memory.main.diag_skip_possible():
                xbox.tap_b()

            # Map changes
            elif checkpoint < 53 and memory.main.get_map() == 46:  # Exit woods
                checkpoint = 53
            elif checkpoint < 64 and memory.main.get_map() == 16:  # Map with boat
                checkpoint = 64
    # logs.write_stats("Kilika battles (South):")
    # logs.write_stats(str(kilika_battles))
    # logs.write_stats("Kilika optimal battles (South):")
    # logs.write_stats(str(optimal_battles))
