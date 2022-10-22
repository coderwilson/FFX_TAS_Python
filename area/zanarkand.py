import battle.main
import logs
import memory.get
import memory.main
import menu
import rngTrack
import screen
import targetPathing
import vars
import xbox

gameVars = vars.vars_handle()

FFXC = xbox.controller_handle()


def print_nea_zone(battles: int):
    print("#### Charging Rikku zone:", gameVars.get_nea_zone())
    print("#### This will take", battles, "number of battles (99 means unknown)")


def decide_nea(bonus_advance: int = 0):
    import rngTrack

    maxBattles = 1
    zanOutdoors = rngTrack.coming_battles(
        area="zanarkand_(overpass)", battleCount=maxBattles, extraAdvances=bonus_advance
    )
    zanIndoors = rngTrack.coming_battles(
        area="zanarkand_(dome)", battleCount=maxBattles, extraAdvances=bonus_advance
    )
    seaSorrows = rngTrack.coming_battles(
        area="inside_sin_(front)",
        battleCount=maxBattles,
        extraAdvances=bonus_advance + 6,
    )

    for i in range(maxBattles):
        if "behemoth" in zanOutdoors[i]:
            gameVars.set_nea_zone(1)
            print_nea_zone(i + 1)
            return
        elif "defender_z" in zanIndoors[i]:
            gameVars.set_nea_zone(2)
            print_nea_zone(i + 1)
            return
        elif "behemoth_king" in seaSorrows[i]:
            gameVars.set_nea_zone(3)
            print_nea_zone(i + 1)
            return
        elif "adamantoise" in seaSorrows[i]:
            gameVars.set_nea_zone(3)
            print_nea_zone(i + 1)
            return
    # If we won't get it in next five per zone, default to Inside Sin. The most possible battles there.
    gameVars.set_nea_zone(99)
    print_nea_zone(99)
    return


def arrival():
    memory.main.await_control()
    decide_nea()
    # Starts from the map just after the fireplace chat.
    reEquipNE = False
    if memory.main.overdrive_state_2()[6] != 100 and gameVars.get_nea_zone() == 1:
        memory.main.full_party_format("rikku", full_menu_close=False)
        menu.equip_armor(character=gameVars.ne_armor(), ability=99)
        reEquipNE = True

    gameVars.set_skip_zan_luck(rngTrack.decide_skip_zan_luck())
    logs.write_stats("Zanarkand Luck Skip:")
    logs.write_stats(gameVars.get_skip_zan_luck())
    # gameVars.setSkipZanLuck(True) #For testing
    print("Outdoor Zanarkand pathing section")
    while memory.main.get_map() != 225:
        if memory.main.user_control():
            if memory.main.get_coords()[1] > -52:
                targetPathing.set_movement([103, -54])
            elif memory.main.get_coords()[0] < 172:
                targetPathing.set_movement([176, -118])
            else:
                FFXC.set_movement(-1, 1)
        else:
            FFXC.set_neutral()

    fortuneSlot = memory.main.get_item_slot(74)
    if fortuneSlot == 255:
        fortuneCount = 0
    else:
        fortuneCount = memory.main.get_item_count_slot(fortuneSlot)

    checkpoint = 0
    while memory.main.get_map() != 314:
        if memory.main.user_control():
            if checkpoint == 3 and gameVars.get_skip_zan_luck():
                checkpoint = 5
            elif checkpoint == 4:  # First chest
                fortuneSlot = memory.main.get_item_slot(74)
                if fortuneSlot == 255:
                    fortuneCount = 0
                    FFXC.set_movement(-1, 1)
                    xbox.tap_b()
                else:
                    if memory.main.get_item_count_slot(fortuneSlot) > fortuneCount:
                        checkpoint += 1
                        memory.main.click_to_control()
                    else:
                        FFXC.set_movement(-1, 1)
                        xbox.tap_b()
            elif targetPathing.set_movement(
                targetPathing.zanarkand_outdoors(checkpoint)
            ):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()

            if screen.battle_screen():
                battle.main.charge_rikku_od()
                if reEquipNE and memory.main.overdrive_state_2()[6] == 100:
                    reEquipNE = False
                    memory.main.click_to_control()
                    memory.main.full_party_format("yuna", full_menu_close=False)
                    menu.equip_armor(character=gameVars.ne_armor(), ability=0x801D)
                    memory.main.close_menu()
            elif memory.main.diag_skip_possible() and not memory.main.battle_active():
                xbox.tap_b()
            elif memory.main.menu_open():
                xbox.tap_b()

    # Outside the dome
    print("Now approaching the Blitz dome.")
    print("Close observation will reveal this is the same blitz dome")
    print("as the one from the opening of the game.")
    while memory.main.get_map() != 222:
        FFXC.set_movement(0, 1)
        xbox.tap_b()

    print("Start of Zanarkand Dome section")
    friendSlot = memory.main.get_item_slot(97)
    if friendSlot == 255:
        friendCount = 0
    else:
        friendCount = memory.main.get_item_count_slot(friendSlot)

    luckSlot = memory.main.get_item_slot(94)
    if luckSlot == 255:
        friendCount = 0
    else:
        luckCount = memory.main.get_item_count_slot(luckSlot)

    if memory.main.overdrive_state_2()[6] != 100 and gameVars.get_nea_zone() == 2:
        memory.main.full_party_format("rikku", full_menu_close=False)
        menu.equip_armor(character=gameVars.ne_armor(), ability=99)
        reEquipNE = True

    checkpoint = 0
    while memory.main.get_map() != 320:
        if memory.main.user_control():
            if checkpoint == 13:  # Second chest
                friendSlot = memory.main.get_item_slot(97)
                if friendSlot == 255:
                    friendCount = 0
                    targetPathing.set_movement([8, 90])
                    memory.main.wait_frames(1)
                    xbox.tap_b()
                else:
                    if memory.main.get_item_count_slot(friendSlot) > friendCount:
                        checkpoint += 1
                        memory.main.click_to_control()
                    else:
                        targetPathing.set_movement([8, 90])
                        memory.main.wait_frames(1)
                        xbox.tap_b()
            if checkpoint == 23 and gameVars.get_skip_zan_luck():
                checkpoint = 25
            elif checkpoint == 24:  # Third chest
                luckSlot = memory.main.get_item_slot(94)
                if luckSlot == 255:
                    luckCount = 0
                    FFXC.set_movement(1, 1)
                    xbox.tap_b()
                else:
                    if memory.main.get_item_count_slot(luckSlot) > luckCount:
                        checkpoint += 1
                        print("Updating checkpoint:", checkpoint)
                        memory.main.click_to_control()
                    else:
                        FFXC.set_movement(1, 1)
                        xbox.tap_b()
            elif checkpoint == 29:  # Save sphere
                memory.main.touch_save_sphere()
                checkpoint += 1
            elif (
                memory.main.get_map() == 316 and checkpoint < 21
            ):  # Final room before trials
                print("Final room before trials")
                checkpoint = 21
            elif targetPathing.set_movement(targetPathing.zanarkand_dome(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                battle.main.charge_rikku_od()
                if reEquipNE and memory.main.overdrive_state_2()[6] == 100:
                    reEquipNE = False
                    memory.main.click_to_control()
                    memory.main.full_party_format("yuna", full_menu_close=False)
                    menu.equip_armor(character=gameVars.ne_armor(), ability=0x801D)
                    memory.main.close_menu()
            elif memory.main.diag_skip_possible() and not memory.main.battle_active():
                xbox.tap_b()
            elif memory.main.menu_open():
                xbox.tap_b()


def trials():
    checkpoint = 0
    while checkpoint < 89:
        checkpoint = trials_0(checkpoint)
        checkpoint = trials_1(checkpoint)
        checkpoint = trials_2(checkpoint)
        checkpoint = trials_3(checkpoint)
        checkpoint = trials_4(checkpoint)


def trials_0(checkpoint):
    memory.main.await_control()

    while checkpoint < 9:
        if memory.main.user_control():
            if checkpoint == 8:
                FFXC.set_movement(-1, 0)
                while memory.main.user_control():
                    xbox.tap_b()
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(30 * 0.2)
                memory.main.await_control()
                memory.main.wait_frames(30 * 1.3)
                FFXC.set_movement(0, 1)
                checkpoint += 1
            elif targetPathing.set_movement(targetPathing.zanarkand_trials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
    return checkpoint


def trials_1(checkpoint):
    memory.main.await_control()

    while checkpoint < 31:
        if memory.main.user_control():
            if checkpoint == 20:
                FFXC.set_movement(-1, 1)
                memory.main.click_to_event()
                FFXC.set_neutral()
                xbox.skip_dialog(0.5)
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 26 or checkpoint == 28:
                FFXC.set_movement(-1, -1)
                memory.main.click_to_event()
                FFXC.set_neutral()
                xbox.skip_dialog(0.5)
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 30:
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                memory.main.wait_frames(30 * 0.2)
                FFXC.set_neutral()
                checkpoint += 1
            elif targetPathing.set_movement(targetPathing.zanarkand_trials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
    return checkpoint


def trials_2(checkpoint):
    memory.main.await_control()

    while checkpoint < 49:
        if memory.main.user_control():
            if checkpoint == 46:
                FFXC.set_movement(1, 0)
                memory.main.click_to_event()
                FFXC.set_neutral()
                xbox.skip_dialog(0.5)
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 48:
                FFXC.set_movement(-1, 1)
                memory.main.await_event()
                memory.main.wait_frames(30 * 0.2)
                FFXC.set_neutral()
                checkpoint += 1
            elif targetPathing.set_movement(targetPathing.zanarkand_trials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
    return checkpoint


def trials_3(checkpoint):
    memory.main.await_control()

    while checkpoint < 69:
        if memory.main.user_control():
            if checkpoint == 66:
                FFXC.set_movement(1, 0)
                memory.main.click_to_event()
                FFXC.set_neutral()
                xbox.skip_dialog(0.7)
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 68:
                FFXC.set_movement(-1, 1)
                memory.main.await_event()
                memory.main.wait_frames(30 * 0.2)
                FFXC.set_neutral()
                checkpoint += 1
            elif targetPathing.set_movement(targetPathing.zanarkand_trials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
    return checkpoint


def trials_4(checkpoint):
    memory.main.await_control()

    while checkpoint < 89:
        if memory.main.user_control():
            if checkpoint == 81:
                FFXC.set_movement(0, 1)
                memory.main.click_to_event()
                FFXC.set_neutral()
                xbox.skip_dialog(0.5)
                memory.main.click_to_control_3()
                checkpoint += 1
            elif checkpoint == 87:
                while memory.main.user_control():
                    targetPathing.set_movement([141, 1])
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_control_3()
                checkpoint += 1
            elif targetPathing.set_movement(targetPathing.zanarkand_trials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
    FFXC.set_neutral()
    return checkpoint


def sanctuary_keeper():
    ver = gameVars.end_game_version()
    print("Now prepping for Sanctuary Keeper fight")

    if ver == 4:
        print("Pattern for four return spheres off of the B&Y fight")
        menu.sk_return()
    elif ver == 3:
        menu.sk_friend()
    else:
        menu.sk_mixed()
    memory.main.full_party_format("yuna")
    memory.main.close_menu()

    while not targetPathing.set_movement([110, 20]):
        pass
    FFXC.set_movement(-1, 1)
    memory.main.await_event()
    xbox.click_to_battle()
    if screen.turn_tidus():
        battle.main.defend()
        xbox.click_to_battle()
    battle.main.aeon_summon(4)  # This is the whole fight. Kinda sad.
    print(
        "Next Aeon Crit:",
        memory.main.next_crit(character=7, char_luck=17, enemy_luck=15),
    )
    while not memory.main.battle_complete():
        if memory.main.turn_ready():
            print(memory.main.rng_array_from_index(index=43, array_len=4))
            battle.main.attack("none")
    memory.main.click_to_control()


def yunalesca():
    ver = gameVars.end_game_version()
    while not targetPathing.set_movement([-2, -179]):
        if memory.main.diag_skip_possible():
            xbox.tap_b()

    if ver == 4:
        print("Final pattern for four return spheres off of the B&Y fight")
        menu.sk_return_2()
        memory.main.close_menu()
    else:
        print("No further sphere gridding needed at this time.")

    print("Sphere grid is done. Moving on to storyline and eventually Yunalesca.")

    memory.main.touch_save_sphere()

    checkpoint = 0
    # Gets us to Yunalesca battle through multiple rooms.
    while not memory.main.battle_active():
        if memory.main.menu_open():
            memory.main.close_menu()
        elif memory.main.user_control():
            if checkpoint in [2, 4]:
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
            elif targetPathing.set_movement(targetPathing.yunalesca(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            FFXC.set_value("BtnB", 1)
            FFXC.set_value("BtnA", 1)
            memory.main.wait_frames(1)
            FFXC.set_value("BtnB", 0)
            FFXC.set_value("BtnA", 0)
            memory.main.wait_frames(1)
    xbox.click_to_battle()
    battle.main.aeon_summon(4)  # Summon Bahamut and attack.
    memory.main.click_to_control()  # This does all the attacking and dialog skipping

    # Now to check for zombie strike and then report to logs.
    print("Ready to check for Zombiestrike")
    logs.write_stats("Zombiestrike:")
    logs.write_stats(gameVars.zombie_weapon())
    print("++Zombiestrike:")
    print("++", gameVars.zombie_weapon())


def post_yunalesca(checkpoint=0):
    print("Heading back outside.")
    FFXC.set_neutral()
    if gameVars.nemesis():
        menu.equip_weapon(character=0, ability=0x807A, full_menu_close=True)
    memory.main.wait_frames(2)
    while memory.main.get_map() != 194:
        if memory.main.user_control():
            if (
                checkpoint < 2 and memory.main.get_map() == 319
            ):  # Back to room before Yunalesca
                checkpoint = 2
                print("Checkpoint reached:", checkpoint)
            elif (
                checkpoint < 4 and memory.main.get_map() == 318
            ):  # Exit to room with the inert Aeon
                checkpoint = 4
                print("Checkpoint reached:", checkpoint)
            elif checkpoint == 7:
                memory.main.touch_save_sphere()
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
            elif (
                checkpoint < 10 and memory.main.get_map() == 320
            ):  # Back to larger of the puzzle rooms
                checkpoint = 10
                print("Checkpoint reached:", checkpoint)
            elif (
                checkpoint < 18 and memory.main.get_map() == 316
            ):  # Hallway before puzzle rooms
                checkpoint = 18
                print("Checkpoint reached:", checkpoint)
            elif (
                checkpoint < 25 and memory.main.get_map() == 315
            ):  # Hallway before puzzle rooms
                checkpoint = 25
                print("Checkpoint reached:", checkpoint)
            elif checkpoint == 26:
                FFXC.set_neutral()
            elif targetPathing.set_movement(
                targetPathing.yunalesca_to_airship(checkpoint)
            ):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                battle.main.flee_all()
            elif memory.main.diag_skip_possible() and not memory.main.battle_active():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                print(memory.get.cutscene_id())
                if memory.get.cutscene_id() == (5673, 2850, 3):
                    memory.main.wait_frames(10)
                    xbox.skip_scene()
