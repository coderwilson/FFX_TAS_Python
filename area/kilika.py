import battle.boss
import battle.main
import logs
import memory.main
import menu
import pathing
import save_sphere
import vars
import xbox

FFXC = xbox.controller_handle()
game_vars = vars.vars_handle()


def arrival():
    # For certain seed/s, preferable to get luck sphere just to manipulate battles.
    # if memory.main.rng_seed() == 31 and gameVars.skipKilikaLuck():
    #    gameVars.dontSkipKilikaLuck()

    print("Arrived at Kilika docks.")
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
            elif pathing.set_movement(pathing.kilika_1(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
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
        ["ragora", "ragora"],
    ]
    for i in range(len(priority)):
        if priority[i] in coming_battles:
            print("--------------Best charge, battle num:", priority[i])
            return priority[i]
    return 99


def forest_1():
    kilikaBattles = 0
    optimalBattles = 0
    nextThree = []
    nextBattle = []
    import rng_track

    valeforCharge = False
    if game_vars.csr():
        checkpoint = 0
    else:
        checkpoint = 2
    while memory.main.get_map() != 108:  # All the way into the trials
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
                if valeforCharge:
                    checkpoint = 83
            if checkpoint == 83 and not valeforCharge:
                checkpoint = 81
            if checkpoint == 83 and memory.main.get_map() == 65:
                checkpoint = 84
            if checkpoint == 37 and game_vars.skip_kilika_luck():
                checkpoint = 60

            # events
            if checkpoint == 9:  # Chest with Wakkas weapon Scout
                memory.main.click_to_event_temple(0)
                menu.woods_menuing()
                checkpoint += 1
            elif checkpoint == 47:  # Luck sphere chest
                luckSlot = memory.main.get_item_slot(94)
                if luckSlot == 255:
                    pathing.set_movement([-250, 200])
                    xbox.tap_b()
                else:
                    checkpoint += 1
            elif checkpoint == 86:
                save_sphere.touch_and_go()
                if not game_vars.did_full_kilik_menu():
                    menu.geneaux()
                checkpoint += 1
            elif checkpoint == 99:  # Lord O'holland
                while memory.main.user_control():
                    pathing.set_movement([-30, 45])
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_control_3()
                checkpoint += 1

            # General pathing
            elif pathing.set_movement(pathing.kilika_2(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                if checkpoint < 9:
                    battle.main.lancet_tutorial()
                    nextTwo = rng_track.coming_battles(
                        area="kilika_woods", battleCount=2
                    )
                    bestOfTwo = select_best_of_two(nextTwo)
                    nextBattle = rng_track.coming_battles(
                        area="kilika_woods", battleCount=1
                    )[0]
                    print("################# Next Battle:", nextBattle)
                elif checkpoint > 86:
                    battle.boss.geneaux()
                else:
                    print("------------This should be battle number:", kilikaBattles)
                    print("------------Reminder (north-bound only):", nextThree)
                    valeforCharge = battle.main.kilika_woods(
                        valeforCharge, bestOfTwo, nextBattle
                    )
                    nextBattle = rng_track.coming_battles(
                        area="kilika_woods", battleCount=1
                    )[0]
                    print("##########################", nextBattle)
                    kilikaBattles += 1
                memory.main.full_party_format("kilika")
            elif memory.main.diag_skip_possible():
                xbox.tap_b()

            # Map changes
            elif checkpoint < 84 and memory.main.get_map() == 65:  # Stairs
                checkpoint = 84
            elif checkpoint < 94 and memory.main.get_map() == 78:  # Temple Entrance
                checkpoint = 94
            elif checkpoint < 96 and memory.main.get_map() == 96:  # Temple interior
                checkpoint = 96
    # logs.writeStats("Kilika battles (North):")
    # logs.writeStats(str(kilikaBattles))
    # logs.writeStats("Kilika optimal battles (North):")
    # logs.writeStats(str(optimalBattles))


def trials():
    memory.main.click_to_control()
    checkpoint = 0
    while memory.main.get_map() != 45:
        if memory.main.user_control():
            # Spheres and glyphs
            if checkpoint == 2:  # First sphere
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 5:  # Insert and remove, opens door
                memory.main.click_to_event_temple(0)
                memory.main.wait_frames(30 * 0.07)
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 9:  # Insert and remove, generate glyph
                memory.main.click_to_event_temple(0)
                memory.main.wait_frames(30 * 0.07)
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 11:  # Put the sphere out of the way
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 13:  # Touch glyph
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 18:  # Kilika sphere (in the way)
                memory.main.click_to_event_temple(1)
                checkpoint += 1
            elif checkpoint == 25:  # Kilika sphere (now out of the way)
                memory.main.click_to_event_temple(6)
                checkpoint += 1
            elif checkpoint == 27:  # Glyph sphere
                while not memory.main.diag_skip_possible():
                    pathing.set_movement([-21, -30])
                    if memory.main.user_control():
                        xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 33:  # Insert Glyph sphere
                memory.main.click_to_event_temple(1)
                checkpoint += 1
            elif checkpoint == 39:  # Pick up last Kilika sphere
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 50:  # Insert and remove, opens door
                memory.main.click_to_event_temple(0)
                memory.main.wait_frames(30 * 0.07)
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            # elif checkpoint == 53 and gameVars.csr():
            #    memory.main.awaitControl()
            #    FFXC.set_movement(0, 1)
            #    memory.main.waitFrames(2)
            #    memory.main.awaitEvent()
            #    FFXC.set_neutral()
            #    xbox.nameAeon("Ifrit")  # Set Ifrit name
            #    checkpoint = 55
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
            elif pathing.set_movement(pathing.kilika_trials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()

            # Map changes
            elif checkpoint < 53 and memory.main.get_map() == 45:  # Inner sanctum
                checkpoint = 53


def trials_end():
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
    # First, re-order the party
    memory.main.full_party_format("kilika")
    kilikaBattles = 0
    optimalBattles = 0
    checkpoint = 0
    while checkpoint < 69:  # All the way to the boats
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
            elif pathing.set_movement(pathing.kilika_3(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle.main.kilika_woods(True)
                kilikaBattles += 1
                if memory.main.get_encounter_id() in [32, 34, 37]:
                    optimalBattles += 1
                if kilikaBattles == 1 and memory.main.rng_seed() == 31:
                    memory.main.full_party_format("kilikawoodsbackup")
                else:
                    memory.main.full_party_format("kilika")
            elif memory.main.diag_skip_possible():
                xbox.tap_b()

            # Map changes
            elif checkpoint < 53 and memory.main.get_map() == 46:  # Exit woods
                checkpoint = 53
            elif checkpoint < 64 and memory.main.get_map() == 16:  # Map with boat
                checkpoint = 64
    # logs.writeStats("Kilika battles (South):")
    # logs.writeStats(str(kilikaBattles))
    # logs.writeStats("Kilika optimal battles (South):")
    # logs.writeStats(str(optimalBattles))
