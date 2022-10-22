import math

import battle.main
import memory.main
import menu
import targetPathing
import vars
import xbox

gameVars = vars.vars_handle()

FFXC = xbox.controller_handle()


def check_spheres():
    # Speed sphere stuff. Improve this later.
    needSpeed = False
    if memory.main.get_speed() < 5:
        needSpeed = True
        # Reprogram battle logic to throw some kind of grenades.

    # Same for Power spheres
    if gameVars.nemesis():
        if (
            memory.main.get_power() >= 28
            or (
                memory.main.get_speed() < 9
                and memory.main.get_power()
                >= (23 + math.ceil((9 - memory.main.get_speed()) / 2))
            )
            or (memory.main.get_speed() >= 9 and memory.main.get_power() >= 23)
        ):
            needPower = False
        else:
            needPower = True

    elif (
        memory.main.get_power() >= 19
        or (
            memory.main.get_speed() < 9
            and memory.main.get_power()
            >= (15 + math.ceil((9 - memory.main.get_speed()) / 2))
        )
        or (memory.main.get_speed() >= 9 and memory.main.get_power() >= 15)
    ):
        needPower = False
    else:
        needPower = True
    return needSpeed, needPower


def desert():
    memory.main.click_to_control()

    needSpeed, needPower = check_spheres()
    # Logic for finding Teleport Spheres x2 (only chest in this area)
    teleSlot = memory.main.get_item_slot(98)
    if teleSlot == 255:
        teleCount = 0
    else:
        teleCount = memory.main.get_item_count_slot(teleSlot)

    chargeState = memory.main.overdrive_state()[6] == 100
    # Bomb cores, sleeping powders, smoke bombs, silence grenades
    stealItems = [0, 0, 0, 0]
    itemsNeeded = 0

    # Now to figure out how many items we need.
    stealItems = battle.main.update_steal_items_desert()
    itemsNeeded = 7 - sum(stealItems)

    menu.equip_sonic_steel()
    memory.main.close_menu()

    checkpoint = 0
    firstFormat = False
    sandy1 = False
    while memory.main.get_map() != 130:
        if memory.main.user_control():
            # Map changes
            if checkpoint == 9:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 11 and len(memory.main.get_order_seven()) > 4:
                checkpoint += 1
            elif checkpoint < 39 and memory.main.get_map() == 137:
                checkpoint = 39
            elif checkpoint < 50 and memory.main.get_map() == 138:
                checkpoint = 50

            # Nemesis stuff
            elif checkpoint == 47 and gameVars.nemesis():
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
                    memory.main.click_to_control()
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
                    memory.main.click_to_control()
                    checkpoint += 1
            elif checkpoint == 76:
                checkpoint = 48

            # Other events
            elif checkpoint == 2 or checkpoint == 24:  # Save sphere
                FFXC.set_neutral()
                memory.main.wait_frames(30 * 0.2)
                memory.main.touch_save_sphere()
                checkpoint += 1
            elif checkpoint == 53:
                print("Going for first Sandragora and chest")
                teleSlot = memory.main.get_item_slot(98)
                if teleSlot == 255 or teleCount == memory.main.get_item_count_slot(
                    teleSlot
                ):
                    targetPathing.set_movement([-44, 446])
                    xbox.tap_b()
                else:
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
            elif checkpoint == 12 and not firstFormat:
                firstFormat = True
                memory.main.full_party_format("desert9")

            # Sandragora skip logic
            elif checkpoint == 57:
                checkpoint += 1
            elif checkpoint == 60:
                if (
                    memory.main.get_coords()[1] < 812
                ):  # Dialing in. 810 works 95%, but was short once.
                    FFXC.set_movement(0, 1)
                else:
                    FFXC.set_neutral()
                    checkpoint += 1
            elif checkpoint == 61:
                if memory.main.get_coords()[1] < 810:
                    # Accidentally encountered Sandragora, must re-position.
                    checkpoint -= 2
                elif memory.main.get_coords()[1] < 840:
                    FFXC.set_neutral()
                else:
                    checkpoint += 1

            # After Sandy2 logic
            elif checkpoint == 64:
                if itemsNeeded >= 1:  # Cannot move on if we're short on throwable items
                    checkpoint -= 2
                elif needSpeed:  # Cannot move on if we're short on speed spheres
                    checkpoint -= 2
                else:
                    checkpoint += 1

            # General pathing
            elif memory.main.user_control():
                if targetPathing.set_movement(targetPathing.desert(checkpoint)):
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not memory.main.battle_active():
                xbox.menu_b()
            if memory.main.battle_active():  # Lots of battle logic here.
                xbox.click_to_battle()
                if (
                    checkpoint < 7 and memory.main.get_encounter_id() == 197
                ):  # First battle in desert
                    battle.main.zu()
                elif memory.main.get_encounter_id() == 234:  # Sandragora logic
                    print("Sandragora fight")
                    if checkpoint < 55:
                        if not sandy1:
                            battle.main.sandragora(1)
                            sandy1 = True
                        else:
                            battle.main.flee_all()
                    else:
                        battle.main.sandragora(2)
                        checkpoint = 58
                else:
                    battle.main.bikanel_battle_logic(
                        [chargeState, needSpeed, needPower, itemsNeeded],
                        sandy_fight_complete=sandy1,
                    )

                # After-battle logic
                memory.main.click_to_control()

                # First, check and update party format.
                if checkpoint > 10:
                    if checkpoint < 23 and checkpoint > 10:
                        memory.main.full_party_format("desert9")
                    elif not chargeState:
                        memory.main.full_party_format("desert1")
                    elif needPower:
                        memory.main.full_party_format("desert1")
                    elif needSpeed:
                        memory.main.full_party_format("desert1")
                    elif itemsNeeded >= 1:
                        memory.main.full_party_format("desert1")
                    else:  # Catchall
                        memory.main.full_party_format("desert1")

                # Next, figure out how many items we need.
                stealItems = battle.main.update_steal_items_desert()
                print("-----------------------------")
                print("Items status:", stealItems)
                print("-----------------------------")
                itemsNeeded = 7 - sum(stealItems)

                # Finally, check for other factors and report to console.
                chargeState = memory.main.overdrive_state()[6] == 100
                needSpeed, needPower = check_spheres()
                print("-----------------------------Flag statuses")
                print("Rikku is charged up:", chargeState)
                print("Need more Speed spheres:", needSpeed)
                print("Need more Power spheres:", needPower)
                print("Number of additional items needed before Home:", itemsNeeded)
                print("-----------------------------Flag statuses (end)")
            elif memory.main.diag_skip_possible():
                xbox.tap_b()


def find_summoners():
    print("Desert complete. Starting Home section")
    menu.home_grid()

    checkpoint = 0
    while memory.main.get_map() != 261:
        if memory.main.user_control():
            # events
            if checkpoint == 7:
                FFXC.set_neutral()
                memory.main.touch_save_sphere()

                checkpoint += 1
            elif checkpoint < 12 and memory.main.get_map() == 276:
                checkpoint = 12
            elif checkpoint < 18 and memory.main.get_map() == 280:
                checkpoint = 19
            elif checkpoint == 34 and gameVars.nemesis():
                checkpoint = 60
            elif checkpoint == 34 and gameVars.skip_kilika_luck():
                checkpoint = 60
            elif checkpoint == 63:
                memory.main.click_to_event_temple(6)
                checkpoint = 35
            # Bonus room, blitzLoss only
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
                FFXC.set_movement(1, -1)
                memory.main.await_event()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 88:
                checkpoint = 21
            elif checkpoint == 20:
                if gameVars.get_blitz_win():
                    checkpoint = 21
                else:
                    checkpoint = 81
            elif checkpoint == 31 and not gameVars.csr():
                memory.main.click_to_event_temple(6)
                checkpoint += 1
            elif checkpoint == 39:
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint == 42:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 45:
                memory.main.click_to_event_temple(1)
                checkpoint += 1
            elif targetPathing.set_movement(targetPathing.home(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                if memory.main.get_encounter_id() == 417:
                    print("Home, battle 1")
                    battle.main.home_1()
                elif memory.main.get_encounter_id() == 419:
                    if memory.main.get_map() == 280:
                        print("Home, battle 2")
                        battle.main.home_2()
                        memory.main.full_party_format("desert1")
                    else:
                        print("Home, bonus battle for Blitz loss")
                        battle.main.home_3()
                elif memory.main.get_encounter_id() == 420:
                    print("Home, final battle")
                    battle.main.home_4()
                    memory.main.full_party_format("evrae")
                else:
                    print("Flee from battle:", memory.main.get_encounter_id())
                    battle.main.flee_all()
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()
    print("Let's go get that airship!")
    FFXC.set_neutral()
    if not gameVars.csr():
        memory.main.click_to_diag_progress(27)
        while not memory.main.cutscene_skip_possible():
            xbox.tap_b()
        xbox.skip_scene()
        memory.main.click_to_diag_progress(105)
        memory.main.wait_frames(15)
        xbox.tap_b()
        memory.main.wait_frames(15)
        xbox.skip_scene()

    while not memory.main.user_control():
        if memory.main.diag_skip_possible():
            xbox.tap_b()
        elif memory.main.cutscene_skip_possible():
            xbox.skip_scene()
    print("Airship is good to go. Now for Yuna.")
