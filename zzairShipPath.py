import math

import battle.main
import memory.main
import targetPathing
import vars
import xbox

gameVars = vars.vars_handle()

FFXC = xbox.controller_handle()


def air_ship_path(version):
    memory.main.click_to_control()
    distillerPurchase = False

    complete = False
    checkpoint = 0
    while not complete:
        if memory.main.user_control():
            # Map changes
            if checkpoint == 2:
                memory.main.click_to_event_temple(3)
                checkpoint += 1
            elif (
                version == 1
                and not distillerPurchase
                and checkpoint == 5
                and (memory.main.get_speed() < 9 or memory.main.get_power() < 23)
            ):

                # Tyton to update this with the actual purchase.
                while memory.main.diag_progress_flag() != 44:
                    if memory.main.user_control():
                        targetPathing.set_movement([-6, 6])
                        xbox.tap_b()
                    else:
                        FFXC.set_neutral()
                        if memory.main.battle_active():
                            battle.main.flee_all()
                        elif memory.main.menu_open():
                            xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_diag_progress(48)
                while memory.main.airship_shop_dialogue_row() != 1:
                    xbox.tap_down()
                while not memory.main.item_shop_menu() == 7:
                    xbox.tap_b()  # Click through until items menu comes up
                while not memory.main.item_shop_menu() == 10:
                    xbox.tap_b()  # Select buy command
                if memory.main.get_power() < 23:
                    while memory.main.equip_buy_row() != 7:
                        if memory.main.equip_buy_row() < 7:
                            xbox.tap_down()
                        else:
                            xbox.tap_up()
                    while not memory.main.item_shop_menu() == 16:
                        xbox.tap_b()
                    while memory.main.purchasing_amount_items() != min(
                        math.ceil((23 - memory.main.get_power()) / 2), 3
                    ):
                        if memory.main.purchasing_amount_items() < min(
                            math.ceil((23 - memory.main.get_power()) / 2), 3
                        ):
                            xbox.tap_right()
                        else:
                            xbox.tap_left()
                    while not memory.main.item_shop_menu() == 10:
                        xbox.tap_b()
                if memory.main.get_speed() < 9:
                    while memory.main.equip_buy_row() != 9:
                        if memory.main.equip_buy_row() < 9:
                            xbox.tap_down()
                        else:
                            xbox.tap_up()
                    while not memory.main.item_shop_menu() == 16:
                        xbox.tap_b()
                    while memory.main.purchasing_amount_items() != min(
                        math.ceil((9 - memory.main.get_speed()) / 2), 2
                    ):
                        if memory.main.purchasing_amount_items() < min(
                            math.ceil((9 - memory.main.get_speed()) / 2), 2
                        ):
                            xbox.tap_right()
                        else:
                            xbox.tap_left()
                    while not memory.main.item_shop_menu() == 10:
                        xbox.tap_b()
                memory.main.close_menu()
                memory.main.click_to_control_3()
                distillerPurchase = True
            elif checkpoint < 6 and memory.main.get_map() == 351:  # Screen with Isaaru
                checkpoint = 6
            elif (
                checkpoint < 9 and memory.main.get_map() == 211
            ):  # Gallery screen (includes lift screens)
                checkpoint = 9
                # Optional save sphere can be touched here.
                # Should not be necessary, we should be touching save sphere in Home
            elif checkpoint == 14 and version == 2:
                print("Talking to Yuna/Kimahri in the gallery")
                checkpoint = 23
                print("Checkpoint update:", checkpoint)
            elif checkpoint == 16:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 18:
                FFXC.set_neutral()
                xbox.skip_dialog(1)
                memory.main.await_control()
                checkpoint += 1
            elif checkpoint == 24:
                memory.main.click_to_event_temple(7)
                checkpoint += 1

            # Return trip map changes
            elif checkpoint in [32, 34]:  # Formerly included 13
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 37:
                memory.main.click_to_event_temple(1)
                checkpoint += 1
            elif checkpoint == 40:
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint in [43, 44] and not gameVars.csr():
                checkpoint = 45
            elif checkpoint == 44:  # Talk to Cid
                while memory.main.user_control():
                    targetPathing.set_movement([-250, 339])
                    xbox.tap_b()
                FFXC.set_neutral()
                complete = True
            elif checkpoint == 46:  # Talk to Cid
                while memory.main.user_control():
                    targetPathing.set_movement([-230, 366])
                    xbox.tap_b()
                FFXC.set_neutral()
                complete = True

            # Complete states
            elif checkpoint == 19 and version == 1:
                print("Pre-Evrae pathing")
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(30 * 3)
                FFXC.set_neutral()
                complete = True
            elif checkpoint == 19 and version == 3:
                print("Sin's Arms")
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(30 * 3)
                FFXC.set_neutral()
                while not memory.main.battle_active():
                    if memory.main.diag_skip_possible():
                        xbox.tap_b()
                    elif memory.main.cutscene_skip_possible():
                        xbox.skip_scene()
                complete = True
            elif checkpoint == 19 and version == 4:
                print("Straight to the deck, talking to Yuna.")
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(30 * 3)
                FFXC.set_neutral()
                memory.main.await_control()
                targetPathing.set_movement([-2, -15])
                memory.main.wait_frames(30 * 0.5)
                while memory.main.user_control():
                    targetPathing.set_movement([-2, -15])
                    xbox.tap_b()
                FFXC.set_neutral()
                while not memory.main.user_control():
                    if memory.main.diag_skip_possible():
                        xbox.tap_b()
                    elif memory.main.cutscene_skip_possible():
                        xbox.skip_scene()
                complete = True
            elif checkpoint == 19 and version == 5:
                print("Again to the deck, three skips.")
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(30 * 3)
                FFXC.set_neutral()
                while not memory.main.battle_active():
                    if memory.main.diag_skip_possible():
                        xbox.tap_b()
                    elif memory.main.cutscene_skip_possible():
                        xbox.skip_scene()
                complete = True
            elif checkpoint == 19 and version == 6:
                print("Sin's Face")
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(30 * 3)
                FFXC.set_neutral()
                complete = True

            # General Pathing
            elif targetPathing.set_movement(targetPathing.air_ship(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle.main.flee_all()
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                print("Mark")
                xbox.tap_b()

    print("End of section, Airship pathing")


def air_ship_return():
    print("Conversation with Yuna/Kimahri.")
    memory.main.click_to_control()

    pos = memory.main.get_coords()
    print("Ready to run back to the cockpit.")
    while pos[1] > -90:  # Leaving Yuna/Kimahri, heading back down.
        FFXC.set_value("AxisLy", -1)
        FFXC.set_value("AxisLx", 0)
        pos = memory.main.get_coords()
    print("Turn East")
    while pos[0] < -1:
        FFXC.set_value("AxisLx", 1)
        FFXC.set_value("AxisLy", 0)
        pos = memory.main.get_coords()
    print("Turn North")
    while memory.main.user_control():
        FFXC.set_value("AxisLx", 0)
        FFXC.set_value("AxisLy", 1)
        pos = memory.main.get_coords()

    FFXC.set_value("AxisLy", 0)
    FFXC.set_value("AxisLx", 0)
    memory.main.await_control()

    while memory.main.user_control():
        FFXC.set_value("AxisLx", 0)
        FFXC.set_value("AxisLy", 1)

    FFXC.set_value("AxisLy", 0)
    FFXC.set_value("AxisLx", 0)
    memory.main.await_control()

    while memory.main.user_control():
        pos = memory.main.get_coords()
        memory.main.wait_frames(30 * 0.05)
        FFXC.set_value("AxisLy", 1)
        if pos[0] < -1:
            FFXC.set_value("AxisLx", 1)
        else:
            FFXC.set_value("AxisLx", 0)

    FFXC.set_value("AxisLy", 0)
    FFXC.set_value("AxisLx", 0)
    memory.main.await_control()
    FFXC.set_value("AxisLy", 1)
    memory.main.wait_frames(30 * 1.2)
    FFXC.set_value("AxisLy", 0)
    FFXC.set_value("AxisLx", -1)
    memory.main.wait_frames(30 * 0.5)

    while memory.main.user_control():
        FFXC.set_value("AxisLy", 1)
        FFXC.set_value("AxisLx", -1)
    FFXC.set_value("AxisLy", 0)
    FFXC.set_value("AxisLx", 0)
