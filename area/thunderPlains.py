import battle.main
import memory.main
import menu
import screen
import targetPathing
import vars
import xbox

game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def south_pathing():
    memory.main.click_to_control()

    game_vars.set_l_strike(memory.main.l_strike_count())

    memory.main.full_party_format("postbunyip")
    memory.main.close_menu()
    count50 = 0
    checkpoint = 0
    while memory.main.get_map() != 256:
        if memory.main.user_control():
            # Lightning dodging
            if memory.main.dodge_lightning(game_vars.get_l_strike()):
                game_vars.set_l_strike(memory.main.l_strike_count())
                if checkpoint == 34:
                    count50 += 1
                    print("Dodge:", count50)
            elif checkpoint == 2 and game_vars.nemesis():
                checkpoint = 20
            elif checkpoint == 2 and not game_vars.get_blitz_win():
                checkpoint = 20
            elif checkpoint == 21:
                # memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 25:
                while memory.main.user_control():
                    targetPathing.set_movement([-175, -487])
                    xbox.tap_x()
                checkpoint += 1
            elif checkpoint == 33:
                while memory.main.user_control():
                    targetPathing.set_movement([205, 160])
                    xbox.tap_x()
                checkpoint += 1
                print("Now ready to dodge some lightning.")
            elif checkpoint == 34:
                if count50 == 50:
                    checkpoint += 1
                else:  # Dodging fifty bolts.
                    FFXC.set_neutral()
            elif checkpoint == 39:  # Back to the normal path
                checkpoint = 10

            # General pathing
            elif memory.main.user_control():
                if targetPathing.set_movement(targetPathing.t_plains_south(checkpoint)):
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not memory.main.battle_active():
                xbox.menu_b()
            elif screen.battle_screen():
                battle.main.thunder_plains(1)
            elif memory.main.menu_open():
                xbox.tap_b()

    memory.main.await_control()
    while not targetPathing.set_movement([-73, 14]):
        if memory.main.diag_skip_possible():
            xbox.menu_b()
    while not targetPathing.set_movement([-83, 29]):
        if memory.main.diag_skip_possible():
            xbox.menu_b()
    while not memory.main.get_map() == 263:
        FFXC.set_movement(-1, 1)
        if memory.main.diag_skip_possible():
            xbox.menu_b()
    FFXC.set_neutral()
    menu.auto_sort_equipment()


def agency_shop():
    speedCount = memory.main.get_speed()

    # 15 plus two (Spherimorph, Flux), minus 1 because it starts on 1
    speedNeeded = max(0, min(2, 14 - speedCount))
    if memory.main.rng_seed() == 160 and not game_vars.get_blitz_win() and game_vars.new_game_check():
        speedNeeded = 0
    grenade_slot = memory.main.get_item_slot(35)
    if grenade_slot == 255:
        cur_grenades = 0
    else:
        cur_grenades = memory.main.get_item_count_slot(grenade_slot)
    total_grenades_needed = 3 + speedNeeded - cur_grenades
    #Don't panic if we have more grenades than expected.
    if total_grenades_needed < 0:
        total_grenades_needed = 0
    memory.main.click_to_diag_progress(92)
    while memory.main.shop_menu_dialogue_row() != 2:
        xbox.tap_down()  # Select "Got any items?"
    while not memory.main.item_shop_menu() == 7:
        xbox.tap_b()  # Click through until items menu comes up
    while not memory.main.item_shop_menu() == 10:
        xbox.tap_b()  # Select buy command

    # For safety (Wendigo is the worst), buying extra phoenix downs first.
    while memory.main.equip_buy_row() != 1:  # Buy some phoenix downs first
        if memory.main.equip_buy_row() < 1:
            xbox.tap_down()
        else:
            xbox.tap_up()
    while not memory.main.item_shop_menu() == 16:
        xbox.tap_b()
    while memory.main.purchasing_amount_items() != 4:
        if memory.main.purchasing_amount_items() < 4:
            xbox.tap_right()
        else:
            xbox.tap_left()
    while not memory.main.item_shop_menu() == 10:
        # Should result in +8 phoenix downs. Can be dialed in later.
        xbox.tap_b()

    if total_grenades_needed:
        # Then buying grenades for multiple uses through the rest of the run.
        while memory.main.equip_buy_row() != 6:
            if memory.main.equip_buy_row() < 6:
                xbox.tap_down()
            else:
                xbox.tap_up()
        while not memory.main.item_shop_menu() == 16:
            xbox.tap_b()
        while memory.main.purchasing_amount_items() != total_grenades_needed:
            if memory.main.purchasing_amount_items() < total_grenades_needed:
                xbox.tap_right()
            else:
                xbox.tap_left()
        while not memory.main.item_shop_menu() == 10:
            xbox.tap_b()
    memory.main.close_menu()

    # Next, Grab Auron's weapon
    xbox.skip_dialog(0.1)
    FFXC.set_neutral()
    memory.main.click_to_diag_progress(90)
    memory.main.click_to_diag_progress(92)
    while memory.main.shop_menu_dialogue_row() != 1:
        xbox.tap_down()
    all_equipment = memory.main.all_equipment()
    tidus_longsword = [
        i
        for i, handle in enumerate(all_equipment)
        if (handle.abilities() == [255, 255, 255, 255] and handle.owner() == 0)
    ][0]
    print("Tidus Longsword in slot:", tidus_longsword)
    auron_katana = [
        i
        for i, handle in enumerate(all_equipment)
        if (handle.abilities() == [0x800B, 255, 255, 255] and handle.owner() == 2)
    ][0]
    print("Auron Katana in slot:", auron_katana)
    other_slots = [
        i
        for i, handle in enumerate(all_equipment)
        if (
            i not in [tidus_longsword, auron_katana]
            and handle.equipStatus == 255
            and not handle.is_brotherhood()
        )
    ]
    print("Sellable Items in :", other_slots)
    menu.sell_weapon(tidus_longsword)
    menu.sell_weapon(auron_katana)
    if game_vars.get_blitz_win() and memory.main.get_gil_value() < 8725:
        for loc in other_slots:
            menu.sell_weapon(loc)
            if memory.main.get_gil_value() >= 8725:
                break
    elif not game_vars.get_blitz_win() and memory.main.get_gil_value() < 9550:
        for loc in other_slots:
            menu.sell_weapon(loc)
            if memory.main.get_gil_value() >= 9550:
                break
    # if not gameVars.getBlitzWin(): # This may come back later.
    #    menu.buyWeapon(0, equip=False)
    menu.buy_weapon(5, equip=False)
    memory.main.close_menu()


def agency():
    # Arrive at the travel agency
    memory.main.click_to_control_3()
    checkpoint = 0

    while memory.main.get_map() != 162:
        strCount = memory.main.get_item_count_slot(memory.main.get_item_slot(87))
        if memory.main.user_control():
            if checkpoint == 1:
                while not memory.main.diag_skip_possible():
                    targetPathing.set_movement([2, -31])
                    xbox.tap_b()
                    memory.main.wait_frames(3)
                FFXC.set_neutral()
                agency_shop()
                checkpoint += 1
            elif checkpoint == 4:
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                FFXC.set_neutral()
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 7:
                if not game_vars.csr():
                    kimahriAffection = memory.main.affection_array()[3]
                    print("Kimahri affection, ", kimahriAffection)
                    while memory.main.affection_array()[3] == kimahriAffection:
                        targetPathing.set_movement([27, -44])
                        xbox.tap_b()
                    print("Updated, full affection array:")
                    print(memory.main.affection_array())
                checkpoint += 1
            elif checkpoint == 8:
                while not memory.main.get_map() == 256:
                    targetPathing.set_movement([3, -52])
                    xbox.tap_b()
                memory.main.click_to_control()
                if game_vars.nemesis() or not game_vars.get_blitz_win():
                    # Back in and out to spawn the chest
                    FFXC.set_movement(-1, 1)
                    while memory.main.get_map() != 263:
                        pass
                    FFXC.set_neutral()
                    memory.main.wait_frames(3)
                    while memory.main.get_map() != 256:
                        targetPathing.set_movement([3, -150])
                        xbox.tap_b()
                    FFXC.set_neutral()
                    memory.main.await_control()
                checkpoint += 1
            elif (
                checkpoint == 9
                and (game_vars.nemesis() or not game_vars.get_blitz_win())
                and strCount < 3
            ):
                targetPathing.set_movement([-73, 45])
                xbox.tap_b()
            elif checkpoint == 11:
                game_vars.set_blitz_win(value=True)
                FFXC.set_movement(0, 1)
                memory.main.click_to_event()

            elif targetPathing.set_movement(targetPathing.t_plains_agency(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()


def north_pathing():
    memory.main.click_to_control()

    lStrikeCount = memory.main.l_strike_count()
    lunarSlot = memory.main.get_item_slot(56) != 255

    checkpoint = 0
    while memory.main.get_map() != 110:
        if memory.main.user_control():
            # Lightning dodging
            if memory.main.dodge_lightning(lStrikeCount):
                print("Dodge")
                lStrikeCount = memory.main.l_strike_count()
            elif game_vars.csr() and checkpoint == 14:
                checkpoint = 16
            elif checkpoint == 17 and not game_vars.get_blitz_win() and not lunarSlot:
                checkpoint -= 2
                print("No lunar curtain. Checkpoint:", checkpoint)

            # General pathing
            elif memory.main.user_control():
                if targetPathing.set_movement(targetPathing.t_plains_north(checkpoint)):
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not memory.main.battle_active():
                xbox.menu_b()
            if screen.battle_screen():
                battle.main.thunder_plains(1)
                lunarSlot = memory.main.get_item_slot(56) != 255
            elif memory.main.menu_open():
                xbox.tap_b()

    FFXC.set_neutral()
    memory.main.await_control()
    print("Thunder Plains North complete. Moving up to the Macalania save sphere.")
    if not game_vars.csr():
        FFXC.set_movement(0, 1)
        xbox.skip_dialog(6)
        FFXC.set_neutral()

        # Conversation with Auron about Yuna being hard to guard.
        memory.main.click_to_control_3()

        FFXC.set_movement(1, 1)
        memory.main.wait_frames(30 * 2)
        FFXC.set_movement(0, 1)
        xbox.skip_dialog(6)
        FFXC.set_neutral()  # Approaching the party

    else:
        while not targetPathing.set_movement([258, -7]):
            pass
