import time

import battle.boss
import battle.main
import logs
import memory.main
import menu
import screen
import targetPathing
import vars
import xbox

game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def arrival():
    memory.main.click_to_control()
    memory.main.close_menu()
    claskoSkip = True

    checkpoint = 0
    while memory.main.get_map() != 92:
        if memory.main.user_control():
            if game_vars.csr() and checkpoint == 1:
                print("CSR, skipping forward")
                checkpoint = 4
                print("Checkpoint reached:", checkpoint)
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
                    FFXC.set_movement(-1, 0)
                    memory.main.wait_frames(30 * 0.7)
                    FFXC.set_neutral()
                    memory.main.wait_frames(30 * 0.4)
                    FFXC.set_movement(1, -1)
                    memory.main.wait_frames(30 * 0.035)
                    FFXC.set_neutral()
                    memory.main.wait_frames(30 * 0.3)
                print("Attempting skip.")
                xbox.menu_b()

                # Now to wait for the skip to happen, or 60 second maximum limit
                startTime = time.time()
                # Max number of seconds that we will wait for the skip to occur.
                timeLimit = 60
                maxTime = startTime + timeLimit
                while memory.main.get_actor_coords(6)[0] < -50:
                    currentTime = time.time()
                    if currentTime > maxTime:
                        print("Skip failed for some reason. Moving on without skip.")
                        claskoSkip = False
                        break
                memory.main.click_to_control()
                FFXC.set_neutral()
                checkpoint += 1
            elif targetPathing.set_movement(targetPathing.mrr_start(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                battle.main.flee_all()
                memory.main.click_to_control_3()
                if memory.main.get_hp()[0] < 520:
                    battle.main.heal_up()
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()
    FFXC.set_neutral()
    print("Done with perlim MRR area, now for the real deal.")
    return claskoSkip


def main_path():
    memory.main.await_control()
    critManip = False
    # Yuna complete, Kimahri complete, Valefor overdrive, Battle counter, Yuna grid complete, MRR phase
    status = [0, 0, 0, 1, 0, 0]
    print("Resetting checkpoint.")
    lastGilValue = 0
    checkpoint = 0
    battleCount = 0
    while memory.main.get_map() != 119:
        if status[0] == 1 and status[1] == 1 and status[2] == 0:
            status[2] = 2  # No need to do Valefor's overdrive and recharge.
        if status[0] == 1 and status[1] == 1 and status[2] == 2:
            # All pieces are complete. Move phase to final phase.
            status[5] = 3
        if memory.main.user_control():
            if checkpoint == 1:
                memory.main.touch_save_sphere()
                memory.main.full_party_format("mrr1")
                checkpoint += 1
            elif checkpoint == 4:
                print("Up the first lift")
                xbox.skip_dialog(1)
                checkpoint += 1
            elif checkpoint == 45:
                if status[0] == 0 or status[1] == 0 or status[2] != 2:
                    if targetPathing.set_movement(targetPathing.mrr_main(99)):
                        checkpoint -= 1
                else:
                    if targetPathing.set_movement(targetPathing.mrr_main(45)):
                        checkpoint += 1

            elif checkpoint == 46:
                print("Up the second lift.")
                FFXC.set_neutral()
                xbox.skip_dialog(1)
                checkpoint += 1
                print("Lift checkpoint:", checkpoint)
            elif checkpoint == 48:  # X-potion for safety
                if not memory.main.rng_seed() in [31]:
                    memory.main.click_to_event_temple(7)
                    print("Got X-potion")
                checkpoint += 1
            elif checkpoint >= 54 and checkpoint <= 56:  # 400 gil guy
                if memory.main.rng_seed() in [160, 31]:
                    checkpoint = 57
                elif (
                    memory.main.get_gil_value() != lastGilValue
                ):  # check if we got the 400 from the guy
                    if memory.main.get_gil_value() == lastGilValue + 400:
                        print("We've procured the 400 gil from the guy.")
                        checkpoint = 57  # now to the actual lift
                    else:
                        lastGilValue = memory.main.get_gil_value()
                else:
                    targetPathing.set_movement(memory.main.mrr_guy_coords())
                    xbox.tap_b()
            elif checkpoint == 58:
                print("Up the third lift")
                while memory.main.user_control():
                    targetPathing.set_movement([29, 227])
                    xbox.tap_b()
                checkpoint += 1
            elif checkpoint == 66:
                xbox.skip_dialog(1)
                print("Up the final lift")
                print(
                    "======== Next Kimahri crit:",
                    memory.main.next_crit(character=3, char_luck=18, enemy_luck=15),
                )
                checkpoint += 1
            elif checkpoint == 68:
                FFXC.set_movement(0, -1)
                memory.main.wait_frames(9)
                FFXC.set_movement(-1, -1)
                memory.main.wait_frames(9)
                checkpoint += 1
            elif checkpoint < 71 and memory.main.get_map() == 79:
                checkpoint = 71  # Into Battle Site zone (upper, cannon area)
            elif targetPathing.set_movement(targetPathing.mrr_main(checkpoint)):
                if checkpoint == 61:
                    if memory.main.next_crit(
                        character=3, char_luck=18, enemy_luck=15
                    ) in [
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        9,
                    ]:
                        critManip = True
                        # Try to end on 1.
                        print(
                            "+++++++++++ We can manip:",
                            memory.main.next_crit(
                                character=3, char_luck=18, enemy_luck=15
                            ),
                        )
                        checkpoint = 59
                    else:
                        checkpoint += 1
                elif checkpoint == 90:
                    checkpoint = 62
                else:
                    checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                print("Starting battle MRR")
                if checkpoint < 47:
                    status = battle.main.mrr_battle(status)
                    print("Status update:", status)
                    status[3] += 1
                else:
                    if battle.main.mrr_manip(kim_max_advance=9):
                        critManip = True

                if memory.main.get_yuna_slvl() >= 8 and status[4] == 0:
                    print("Yuna has enough levels now. Going to do her grid.")
                    menu.mrr_grid_yuna()
                    print("Yunas gridding is complete for now.")
                    status[4] = 1
                if memory.main.get_slvl_wakka() >= 7:
                    menu.mrr_grid_2()
                memory.main.close_menu()
                print("MRR battle complete")
                print(
                    "======== Next Kimahri crit:",
                    memory.main.next_crit(character=3, char_luck=18, enemy_luck=15),
                )
                battleCount += 1
            elif memory.main.menu_open():
                xbox.tap_b()
            elif memory.main.diag_skip_possible():
                memory.main.click_to_control_3()

            # Map changes
            elif checkpoint < 47 and memory.main.get_map() == 128:
                checkpoint = 47

        if memory.main.game_over():
            return
    # logs.writeStats("MRR Battles:")
    # logs.writeStats(battleCount)
    logs.write_stats("MRR crit manip:")
    logs.write_stats(critManip)
    print("End of MRR section. Status:")
    print("[Yuna AP, Kim AP, Valefor OD steps, then other stuff]")
    print(status)


def battle_site():
    memory.main.await_control()
    if game_vars.get_l_strike() >= 2:
        menu.equip_weapon(character=4, ability=0x8026, full_menu_close=False)
    menu.battle_site_grid()

    checkpoint = 0
    while checkpoint < 99:
        if memory.main.user_control():
            if checkpoint == 5:
                print("O'aka menu section")
                while memory.main.user_control():
                    targetPathing.set_movement([-45, 3425])
                    xbox.tap_b()
                FFXC.set_neutral()
                menu.battle_site_oaka_1()
                menu.battle_site_oaka_2()
                print(
                    "======== Next Kimahri crit:",
                    memory.main.next_crit(character=3, char_luck=18, enemy_luck=15),
                )
                checkpoint += 1
            elif checkpoint == 8:
                memory.main.touch_save_sphere()
                print(
                    "======== Next Kimahri crit:",
                    memory.main.next_crit(character=3, char_luck=18, enemy_luck=15),
                )
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
            elif targetPathing.set_movement(targetPathing.battle_site(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()


def gui_and_aftermath():
    battle.boss.gui()

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
            elif targetPathing.set_movement(
                targetPathing.battle_site_aftermath(checkpoint)
            ):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            memory.main.click_to_control_3()
