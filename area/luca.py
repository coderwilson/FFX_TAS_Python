import battle.boss
import battle.main
import logs
import memory.main
import menu
import targetPathing
import vars
import xbox

game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def arrival():
    if not game_vars.csr():
        xbox.skip_stored_scene(2)
    print("Starting Luca section")
    memory.main.click_to_control()

    earlyHaste = 0
    checkpoint = 0
    while checkpoint < 56:
        if memory.main.user_control():
            # Map changes
            if checkpoint < 5 and memory.main.get_map() == 268:
                checkpoint = 5
                print("Map change:", checkpoint)
            elif checkpoint < 10 and memory.main.get_map() == 123:
                # Front of the Blitz dome
                print("Map change:", checkpoint)
                checkpoint = 10
            elif checkpoint < 13 and memory.main.get_map() == 77:
                print("Map change:", checkpoint)
                checkpoint = 13
            elif checkpoint < 15 and memory.main.get_map() == 104:
                print("Map change:", checkpoint)
                checkpoint = 15

            # events
            if checkpoint in [5, 6]:  # Seymour intro scene
                memory.main.await_control()
                print("Event: Seymour intro scene")
                FFXC.set_movement(1, 0)
                memory.main.await_event()
                FFXC.set_neutral()
                if not game_vars.csr():
                    memory.main.click_to_diag_progress(18)  # Seymour scene
                    xbox.await_save(index=2)

                    memory.main.click_to_diag_progress(82)  # Let's go over the basics
                    xbox.skip_dialog(1)
                while memory.main.blitz_cursor() != 12:
                    xbox.tap_a()
                xbox.menu_b()
                if not game_vars.csr():
                    xbox.skip_dialog_special(45)  # Skip the Wakka Face scene
                memory.main.click_to_control()
                checkpoint = 7
                print("Seymour scene, updating checkpoint.")
            elif checkpoint == 12:  # Upside down T section
                print("Event: Upside down T section")
                memory.main.click_to_event_temple(4)
                checkpoint += 1
            elif checkpoint == 23:  # Into the bar
                print("Event: Into the bar looking for Auron")
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 33:  # Back to the front of the Blitz dome
                print("Event: Back to Blitz dome entrance")
                memory.main.click_to_event_temple(6)
                checkpoint += 1
            elif checkpoint == 36:  # To the docks
                print("Event: Towards the docks")
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(9)
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 40:
                print("Event: First battle")
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                FFXC.set_neutral()
                battle.main.luca_workers()
                checkpoint += 1
            elif checkpoint == 42:  # First and second battles
                print("Event: Second battle")
                FFXC.set_movement(1, 1)
                memory.main.await_event()
                FFXC.set_neutral()
                battle.main.luca_workers()
                checkpoint += 1
            elif checkpoint == 44:  # Third battle
                print("Tidus XP:", memory.main.get_tidus_xp())
                if memory.main.get_tidus_xp() >= 312:
                    FFXC.set_neutral()
                    earlyHaste = menu.luca_workers()
                    if earlyHaste != 0:
                        earlyHaste = 2
                print("Event: Third battle")
                FFXC.set_movement(1, 0)
                memory.main.await_event()
                FFXC.set_neutral()
                battle.main.luca_workers_2(earlyHaste)
                print("Tidus XP:", memory.main.get_tidus_xp())
                memory.main.click_to_control()
                if earlyHaste == 0 and memory.main.get_tidus_xp() >= 312:
                    earlyHaste = menu.luca_workers()

                checkpoint += 1
            elif checkpoint == 46 or checkpoint == 55:
                print("Event: Touch Save Sphere")
                memory.main.touch_save_sphere()
                checkpoint += 1
            elif checkpoint == 48:  # Oblitzerator
                print("Event: Oblitzerator fight")
                FFXC.set_movement(1, 0)
                memory.main.await_event()
                FFXC.set_neutral()
                battle.boss.oblitzerator(earlyHaste)
                checkpoint += 1
            elif checkpoint == 50:
                memory.main.click_to_event_temple(4)

                if earlyHaste == 0:
                    earlyHaste = menu.luca_workers() - 1
                checkpoint += 1
            elif checkpoint == 52:
                memory.main.click_to_event_temple(5)
                checkpoint += 1

            # General pathing
            elif targetPathing.set_movement(targetPathing.luca_1(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                xbox.skip_scene()

    logs.write_stats("Early Haste:")
    logs.write_stats(earlyHaste)
    game_vars.early_haste_set(earlyHaste)

    print("##Checking for thunderstrike weapons for Tidus or Wakka")
    thunderStrike = memory.main.check_thunder_strike()
    if thunderStrike == 0:
        print("##Neither character got a thunderstrike weapon.")
    elif thunderStrike == 1:
        print("##Tidus got a thunderstrike weapon.")
    elif thunderStrike == 2:
        print("##Wakka got a thunderstrike weapon.")
    else:
        print("##Both Tidus and Wakka somehow got a thunderstrike weapon.")

    logs.write_stats("Thunderstrike results:")
    logs.write_stats(thunderStrike)

    if thunderStrike != 0:
        if thunderStrike % 2 == 1:
            print("Equipping Tidus")
            fullClose = True
            menu.equip_weapon(character=0, ability=0x8026, full_menu_close=fullClose)
    game_vars.set_l_strike(thunderStrike)


def blitz_start():
    print("Starting the Blitzball game via lots of storyline.")
    checkpoint = 0
    while memory.main.get_story_progress() < 519:
        if memory.main.user_control():
            if memory.main.get_map() == 72 and checkpoint < 3:
                checkpoint = 3
            elif (
                memory.main.get_map() == 72
                and memory.main.get_coords()[0] < -18
                and checkpoint < 5
            ):
                checkpoint = 5
            elif (
                memory.main.get_map() == 72
                and memory.main.get_coords()[0] > -15
                and checkpoint >= 5
            ):
                checkpoint = 4
            elif checkpoint == 8:
                targetPathing.set_movement([-111, -4])
                xbox.tap_b()
            elif targetPathing.set_movement(targetPathing.luca_pre_blitz(checkpoint)):
                checkpoint += 1
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()


def after_blitz():
    xbox.click_to_battle()
    encounterID = 0
    checkpoint = 0
    while checkpoint < 36:
        if memory.main.user_control():
            # Events
            if checkpoint == 8:  # First chest
                if game_vars.early_haste() == -1:
                    menu.late_haste()
                    memory.main.close_menu()
                print("First chest")
                while memory.main.user_control():
                    targetPathing.set_movement([-635, -410])
                    xbox.menu_b()
                FFXC.set_neutral()
                memory.main.click_to_control()
                checkpoint += 1
            elif checkpoint == 10:  # Second chest
                print("Second chest")
                while memory.main.user_control():
                    targetPathing.set_movement([-620, -424])
                    xbox.menu_b()
                FFXC.set_neutral()
                memory.main.click_to_control()
                checkpoint += 1
            elif checkpoint == 20:  # Target Auron
                if not game_vars.csr():
                    # First Auron affection, always zero
                    while memory.main.affection_array()[2] == 0:
                        auronCoords = memory.main.get_actor_coords(3)
                        targetPathing.set_movement(auronCoords)
                        xbox.tap_b()
                checkpoint += 1  # After affection changes
            elif checkpoint == 35:  # Bring the party together
                print("Bring the party together")
                memory.main.click_to_event_temple(1)
                checkpoint += 1

            # General pathing
            elif targetPathing.set_movement(targetPathing.luca_3(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                encounterID += 1
                print("After-Blitz Battle Number:", encounterID)
                if encounterID == 1:
                    battle.main.after_blitz_1(game_vars.early_haste())
                elif encounterID == 2:
                    xbox.click_to_battle()
                    battle.main.attack("none")  # Hardest boss in the game.
                    print("Well that boss was difficult.")
                    memory.main.wait_frames(30 * 6)
                elif encounterID == 3:
                    if game_vars.early_haste() == -1:
                        battle.main.after_blitz_3_late_haste(game_vars.early_haste())
                    else:
                        battle.main.after_blitz_3(game_vars.early_haste())
                    memory.main.click_to_control()
                    memory.main.wait_frames(4)
                    FFXC.set_neutral()
                    checkpoint = 0
            elif memory.main.diag_skip_possible():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                memory.main.wait_frames(2)
                xbox.skip_scene()
            elif memory.main.menu_open():
                xbox.tap_b()

            # Map changes
            elif checkpoint < 23 and memory.main.get_map() == 123:
                checkpoint = 23
                print("Map change:", checkpoint)
            elif checkpoint < 26 and memory.main.get_map() == 77:
                checkpoint = 26
                print("Map change:", checkpoint)
            elif checkpoint < 31 and memory.main.get_map() == 104:
                checkpoint = 31
                print("Map change:", checkpoint)
    FFXC.set_movement(-1, -1)
    memory.main.wait_frames(30 * 2)
    FFXC.set_neutral()

    logs.write_stats("Blitz Win:")
    logs.write_stats(game_vars.get_blitz_win())
