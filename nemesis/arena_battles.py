import logging

import menu
import battle.main
import battle.overdrive
import memory.main
import nemesis.arenaSelect
import nemesis.menu
import nemesis.targetPath
import reset
import save_sphere
import screen
import vars
import xbox

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()

# The following functions extend the regular Bahamut run. Arena battles sections.


def save_game(first_save=False):
    while not nemesis.targetPath.set_movement([-6, -27]):
        pass
    while not nemesis.targetPath.set_movement([-2, -2]):
        pass
    print("Arena - Touch Save Sphere, and actually save")
    FFXC = xbox.controller_handle()
    FFXC.set_neutral()
    ss_details = memory.main.get_save_sphere_details()

    if memory.main.user_control():
        while memory.main.user_control():
            nemesis.targetPath.set_movement([ss_details[0], ss_details[1]])
            xbox.tap_b()
            memory.main.wait_frames(1)
    try:
        FFXC.set_neutral()
    except:
        FFXC = xbox.controller_handle()
        FFXC.set_neutral()
    memory.main.wait_frames(30)
    xbox.tap_b()
    memory.main.wait_frames(10)

    print("Controller is now neutral. Attemption to open save nemesis.menu.")
    while not memory.main.save_menu_open():
        pass
    print("Save menu is open.")
    memory.main.wait_frames(9)
    if not first_save:
        xbox.menu_down()
        xbox.menu_b()
        xbox.menu_left()
    xbox.menu_b()  # Select the save file
    xbox.menu_b()  # Confirm the save
    memory.main.wait_frames(90)
    xbox.menu_a()  # Back out
    xbox.menu_a()  # Back out
    xbox.menu_a()  # Back out
    xbox.menu_a()  # Back out

    print("Menu now closed. Back to the battles.")
    memory.main.clear_save_menu_cursor()
    memory.main.clear_save_menu_cursor_2()
    while not nemesis.targetPath.set_movement([-6, -27]):
        pass
    while not nemesis.targetPath.set_movement([2, -25]):
        pass


def touch_save(real_save=False):
    while not nemesis.targetPath.set_movement([-6, -27]):
        pass
    while not nemesis.targetPath.set_movement([-2, -2]):
        pass
    save_sphere.touch_and_go()
    while not nemesis.targetPath.set_movement([-6, -27]):
        pass
    while not nemesis.targetPath.set_movement([2, -25]):
        pass
    arena_npc()


def airship_destination(dest_num=0):  # Default to Sin.
    while memory.main.get_map() != 382:
        if memory.main.user_control():
            nemesis.targetPath.set_movement([-251, 340])
        else:
            FFXC.set_neutral()
        xbox.menu_b()
    while memory.main.diag_progress_flag() != 4:
        xbox.menu_b()
    print("Destination select on screen now.")
    while memory.main.map_cursor() != dest_num:
        if dest_num < 8:
            xbox.tap_down()
        else:
            xbox.tap_up()
    xbox.tap_b()
    memory.main.wait_frames(2)
    xbox.tap_b()
    memory.main.click_to_control_3()


def get_save_sphere_details():
    map_val = memory.main.get_map()
    story_val = memory.main.get_story_progress()
    print("Map:", map_val, "| Story:", story_val)
    x = 0
    y = 0
    diag = 0
    if map_val == 322:
        # Inside Sin, next to airship
        x = 225
        y = -250
        diag = 15
    if map_val == 19:
        # Besaid beach
        x = -310
        y = -475
        diag = 55
    if map_val == 263:
        # Thunder Plains agency
        x = -30
        y = -10
        diag = 114
    if map_val == 307:
        # Monster Arena
        x = 4
        y = 5
        diag = 166
    if map_val == 98:
        # Kilika docks
        x = 46
        y = -252
        diag = 34
    if map_val == 92:
        # MRR start
        x = -1
        y = -740
        diag = 43
    if map_val == 266:
        # Calm Lands Gorge
        x = -310
        y = 190
        diag = 43
    if map_val == 82:
        # Djose temple
        x = 100
        y = -240
        diag = 89
    if map_val == 221:
        # Macalania Woods, near Spherimorph
        x = 197
        y = -120
        diag = 23
    if map_val == 137:
        # Bikanel Desert
        x = -15
        y = 240
        diag = 31
    if map_val == 313:
        # Zanarkand campfire
        x = 135
        y = -1
        diag = 4
    if map_val == 327:
        # Sin, end zone
        x = -37
        y = -508
        diag = 10
    if map_val == 258:
        # Omega (only used in Nemesis)
        x = -112
        y = -1066
        diag = 23

    print("Values: [", x, ",", y, "] - ", diag)
    return [x, y, diag]


def return_to_airship():
    print("Attempting Return to Airship")

    ss_details = get_save_sphere_details()

    if memory.main.user_control():
        while memory.main.user_control():
            nemesis.targetPath.set_movement([ss_details[0], ss_details[1]])
            xbox.tap_b()
            memory.main.wait_frames(1)
    try:
        FFXC.set_neutral()
    except:
        FFXC = xbox.controller_handle()
        FFXC.set_neutral()
    FFXC.set_neutral()

    while not memory.main.get_map() in [194, 374]:
        if memory.main.get_map() == 307 and memory.main.get_coords()[1] < -5:
            while not nemesis.targetPath.set_movement([-4, -21]):
                pass
            while not nemesis.targetPath.set_movement([-2, -2]):
                pass
        else:
            FFXC.set_neutral()
            if memory.main.save_menu_open():
                xbox.tap_a()
            elif memory.main.diag_progress_flag() == ss_details[2]:
                # print("Cursor test:", memory.save_menu_cursor())
                if memory.main.save_menu_cursor() != 1:
                    xbox.menu_down()
                else:
                    xbox.menu_b()
            elif memory.main.user_control():
                nemesis.targetPath.set_movement([ss_details[0], ss_details[1]])
                xbox.menu_b()
            elif memory.main.diag_skip_possible():
                xbox.menu_b()
            memory.main.wait_frames(4)
    print("Return to Airship Complete.")
    memory.main.clear_save_menu_cursor()
    memory.main.clear_save_menu_cursor_2()


def aeon_start():
    screen.await_turn()
    battle.main.buddy_swap_yuna()
    battle.main.aeon_summon(4)
    while not screen.turn_tidus():
        if memory.main.turn_ready():
            if screen.turn_aeon():
                battle.main.attack("none")
            else:
                battle.main.defend()


def yojimbo_battle():
    # Incomplete
    screen.await_turn()
    if 1 not in memory.main.get_active_battle_formation():
        battle.main.buddy_swap_yuna()
    print("+Yuna Overdrive to summon Yojimbo")
    battle.overdrive.yuna()
    print("+Pay the man")
    battle.overdrive.yojimbo()
    memory.main.wait_frames(90)
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if screen.turn_tidus():
                battle.main.tidus_flee()
            elif screen.turn_aeon():
                xbox.skip_dialog(2)
            else:
                battle.main.defend()

    # After battle stuff
    while not memory.main.menu_open():
        xbox.tap_b()
    print("Battle is complete.")
    FFXC.set_value("btn_b", 1)
    memory.main.wait_frames(180)
    FFXC.set_neutral()
    memory.main.wait_frames(2)

    return memory.main.battle_arena_results()


def auto_life():
    while not (memory.main.turn_ready() and screen.turn_tidus()):
        if memory.main.turn_ready():
            if screen.turn_aeon():
                battle.main.attack("none")
            elif not screen.turn_tidus():
                battle.main.defend()
    while memory.main.battle_menu_cursor() != 22:
        if not screen.turn_tidus():
            print("Attempting Haste, but it's not Tidus's turn")
            xbox.tap_up()
            xbox.tap_up()
            return
        if memory.main.battle_menu_cursor() == 1:
            xbox.tap_up()
        else:
            xbox.tap_down()
    while not memory.main.other_battle_menu():
        xbox.tap_b()
    battle.main._navigate_to_position(1)
    while memory.main.other_battle_menu():
        xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()


def basic_quick_attacks(mega_phoenix=False, od_version: int = 0, yuna_autos=False):
    print("### Battle Start:", memory.main.get_encounter_id())
    FFXC.set_neutral()
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if screen.turn_tidus():
                if mega_phoenix and screen.faint_check() >= 2:
                    battle.main.revive(item_num=7)
                elif memory.main.get_overdrive_battle(0) == 100:
                    battle.overdrive.tidus(version=od_version)
                else:
                    battle.main.use_skill(1)  # Quick hit
            elif screen.turn_aeon():
                battle.main.attack("none")
            else:
                battle.main.defend()

    # After battle stuff
    while not memory.main.menu_open():
        xbox.tap_b()
    FFXC.set_value("btn_b", 1)
    memory.main.wait_frames(150)
    FFXC.set_neutral()
    memory.main.wait_frames(2)
    return memory.main.battle_arena_results()


def basic_attack(
    mega_phoenix=False, od_version: int = 0, use_od=False, yuna_autos=False
):
    print("### Battle Start:", memory.main.get_encounter_id())
    FFXC.set_neutral()
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if screen.turn_tidus():
                if mega_phoenix and screen.faint_check() >= 2:
                    battle.main.revive(item_num=7)
                elif use_od and memory.main.get_overdrive_battle(0) == 100:
                    battle.overdrive.tidus(version=od_version)
                else:
                    battle.main.attack("none")
            elif screen.turn_yuna() and yuna_autos:
                battle.attack("none")
            elif screen.turn_aeon():
                battle.attack("none")
            else:
                battle.main.defend()

    # After battle stuff
    while not memory.main.menu_open():
        xbox.tap_b()
    FFXC.set_value("btn_b", 1)
    memory.main.wait_frames(150)
    FFXC.set_neutral()
    memory.main.wait_frames(2)
    return memory.main.battle_arena_results()


def arena_npc():
    if memory.main.get_map() != 307:
        return
    while not (
        memory.main.diag_progress_flag() == 74 and memory.main.diag_skip_possible()
    ):
        if memory.main.user_control():
            if memory.main.get_coords()[1] > -15:
                print("Wrong position, moving away from sphere")
                while not nemesis.targetPath.set_movement([-6, -27]):
                    pass
                while not nemesis.targetPath.set_movement([2, -25]):
                    pass
            else:
                print("Engaging NPC")
                nemesis.targetPath.set_movement([5, -12])
                xbox.tap_b()
        else:
            FFXC.set_neutral()
            if memory.main.diag_progress_flag() == 59:
                xbox.menu_a()
                xbox.menu_a()
                xbox.menu_a()
                xbox.tap_b()
            elif (
                memory.main.diag_skip_possible()
                and not memory.main.diag_progress_flag() == 74
            ):
                xbox.tap_b()
    print("Mark 1")
    memory.main.wait_frames(30)  # This buffer can be improved later.
    print("Mark 2")


def restock_downs():
    print("Restocking phoenix downs")
    if memory.main.get_item_count_slot(memory.main.get_item_slot(6)) >= 80:
        print("Restock not needed. Disregard.")
        return
    arena_npc()
    nemesis.arenaSelect.arena_menu_select(3)
    memory.main.wait_frames(60)
    xbox.tap_b()
    memory.main.wait_frames(6)
    while memory.main.equip_buy_row() != 2:
        if memory.main.equip_buy_row() < 2:
            xbox.tap_down()
        else:
            xbox.tap_up()
    xbox.tap_b()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_b()
    memory.main.wait_frames(6)
    xbox.menu_a()
    memory.main.wait_frames(6)
    xbox.menu_a()


def battles_1():
    if not memory.main.equipped_armor_has_ability(char_num=1, ability_num=0x800A):
        nemesis.menu.equipArmor(character=1, ability=0x800A, fullMenuClose=False)
    if not memory.main.equipped_armor_has_ability(char_num=4, ability_num=0x800A):
        nemesis.menu.equipArmor(character=4, ability=0x800A)
    memory.main.close_menu()
    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=13, monster_index=0)
    while not basic_quick_attacks():
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=13, monster_index=0)
    game_vars.arena_success(array_num=0, index=0)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=13, monster_index=1)
    aeon_start()
    auto_life()
    while not basic_quick_attacks(mega_phoenix=True):
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(4)
        memory.main.full_party_format("kilikawoods1")
        touch_save()
        arena_npc()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=13, monster_index=1)
        aeon_start()
        if screen.turn_tidus():
            auto_life()
    game_vars.arena_success(array_num=0, index=1)
    restock_downs()
    nemesis.arenaSelect.arena_menu_select(4)
    memory.main.full_party_format("kilikawoods1")
    menu.tidus_slayer(odPos=0)

    check_yojimbo_possible()

    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=13, monster_index=2)
    while not basic_quick_attacks(yuna_autos=True):
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=13, monster_index=2)
    game_vars.arena_success(array_num=0, index=2)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=13, monster_index=3)
    while not basic_quick_attacks():
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=13, monster_index=3)
    game_vars.arena_success(array_num=0, index=3)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=13, monster_index=4)
    auto_life()
    while not basic_quick_attacks(mega_phoenix=True):
        print("Battle not completed successfully.")
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=13, monster_index=4)
        auto_life()
    game_vars.arena_success(array_num=0, index=4)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=13, monster_index=5)
    while not basic_quick_attacks():
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=13, monster_index=5)
    game_vars.arena_success(array_num=0, index=5)
    restock_downs()

    check_yojimbo_possible()

    nemesis.arenaSelect.arena_menu_select(4)
    menu.tidus_slayer(odPos=2)
    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=13, monster_index=6)
    while not basic_quick_attacks():
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=13, monster_index=6)
    game_vars.arena_success(array_num=0, index=6)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=13, monster_index=7)
    while not basic_quick_attacks():
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=13, monster_index=7)
    game_vars.arena_success(array_num=0, index=7)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=13, monster_index=8)
    while not basic_quick_attacks():
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=13, monster_index=8)
    game_vars.arena_success(array_num=0, index=8)
    restock_downs()

    check_yojimbo_possible()

    nemesis.arenaSelect.arena_menu_select(4)
    menu.tidus_slayer(odPos=0)
    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=13, monster_index=9)
    while not basic_quick_attacks(yuna_autos=True):
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=13, monster_index=9)
    game_vars.arena_success(array_num=0, index=9)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=13, monster_index=10)
    auto_life()
    while not basic_quick_attacks():
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=13, monster_index=10)
        auto_life()
    game_vars.arena_success(array_num=0, index=10)
    restock_downs()

    check_yojimbo_possible()


def battles_2():
    print("++Starting second section++")
    nemesis.arenaSelect.arena_menu_select(4)
    touch_save()
    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=14, monster_index=1)
    while not basic_quick_attacks():
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(4)
        touch_save()
        arena_npc()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=14, monster_index=1)
    game_vars.arena_success(array_num=1, index=1)
    restock_downs()

    check_yojimbo_possible()

    nemesis.arenaSelect.arena_menu_select(4)
    touch_save()
    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=14, monster_index=3)
    while not basic_quick_attacks():
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=14, monster_index=3)
    game_vars.arena_success(array_num=1, index=3)
    restock_downs()

    check_yojimbo_possible()

    nemesis.arenaSelect.arena_menu_select(4)
    touch_save()
    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=14, monster_index=5)
    while not basic_quick_attacks():
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=14, monster_index=5)
    game_vars.arena_success(array_num=1, index=5)
    restock_downs()

    check_yojimbo_possible()

    nemesis.arenaSelect.arena_menu_select(4)
    touch_save()
    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=14, monster_index=8)
    while not basic_quick_attacks():
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=14, monster_index=8)
    game_vars.arena_success(array_num=1, index=8)
    restock_downs()
    nemesis.arenaSelect.arena_menu_select(4)
    touch_save()

    check_yojimbo_possible()


def jug_farm_done():
    print("||| Slot: ", memory.main.get_item_slot(87))
    if memory.main.get_item_slot(87) > 250:
        return False
    else:
        print("Count: ", memory.main.get_item_count_slot(memory.main.get_item_slot(87)))
        if memory.main.get_item_count_slot(memory.main.get_item_slot(87)) < 6:
            return False
    return True


def juggernaut_farm():
    check_yojimbo_possible()
    while not jug_farm_done():
        arena_npc()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=14, monster_index=12)
        auto_life()
        basic_quick_attacks(mega_phoenix=True, od_version=1)
        restock_downs()
        check_yojimbo_possible()
        nemesis.arenaSelect.arena_menu_select(4)
        touch_save()
    print("Good to go on strength spheres")
    game_vars.arena_success(array_num=1, index=12)
    print("Starting menu to finish strength.")
    nemesis.arenaSelect.arena_menu_select(4)
    nemesis.menu.str_boost()
    print("Touch save sphere, and then good to go.")
    touch_save()


def battles_3():
    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=13, monster_index=11)
    auto_life()
    while not basic_quick_attacks(mega_phoenix=True):
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=13, monster_index=11)
        auto_life()
    game_vars.arena_success(array_num=0, index=11)
    restock_downs()

    check_yojimbo_possible()

    nemesis.arenaSelect.arena_menu_select(4)
    touch_save()
    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=14, monster_index=2)
    aeon_start()
    auto_life()
    while not basic_attack(use_od=False):
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(4)
        touch_save()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=14, monster_index=2)
        auto_life()
    game_vars.arena_success(array_num=1, index=2)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=14, monster_index=0)
    auto_life()
    while not basic_quick_attacks(mega_phoenix=True, od_version=1):
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=14, monster_index=0)
        auto_life()
    game_vars.arena_success(array_num=1, index=0)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=14, monster_index=9)
    auto_life()
    while not basic_quick_attacks(mega_phoenix=True, od_version=1):
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=14, monster_index=9)
        auto_life()
    game_vars.arena_success(array_num=1, index=9)
    restock_downs()

    check_yojimbo_possible()

    nemesis.arenaSelect.arena_menu_select(4)
    touch_save()
    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=14, monster_index=10)
    auto_life()
    while not basic_quick_attacks(mega_phoenix=True, od_version=1):
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=14, monster_index=10)
        auto_life()
    game_vars.arena_success(array_num=1, index=10)
    restock_downs()

    check_yojimbo_possible()


def battles_4():
    nemesis.arenaSelect.arena_menu_select(4)
    touch_save()
    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=15, monster_index=0)
    auto_life()
    while not basic_quick_attacks(mega_phoenix=True, od_version=1):
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=15, monster_index=0)
        auto_life()
    game_vars.arena_success(array_num=2, index=0)
    restock_downs()

    check_yojimbo_possible()
    nemesis.arenaSelect.arena_menu_select(4)
    touch_save()

    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=15, monster_index=6)

    while not shinryu_battle():
        print("Battle not completed successfully.")
        restock_downs()
        nemesis.arenaSelect.arena_menu_select(4)
        touch_save()
        arena_npc()
        nemesis.arenaSelect.arena_menu_select(1)
        nemesis.arenaSelect.start_fight(area_index=15, monster_index=6)

    game_vars.arena_success(array_num=2, index=6)
    restock_downs()


def item_dump():
    nemesis.arenaSelect.arena_menu_select(2)
    memory.main.wait_frames(90)
    xbox.menu_right()
    xbox.menu_b()
    nemesis.menu.sellAll(NEA=True)
    xbox.menu_a()
    xbox.menu_a()
    xbox.menu_a()
    xbox.menu_a()


def quick_reset_logic():
    reset.reset_to_main_menu()
    memory.main.wait_frames(90)
    while memory.main.get_map() != 23:
        FFXC.set_value("btn_start", 1)
        memory.main.wait_frames(2)
        FFXC.set_value("btn_start", 0)
        memory.main.wait_frames(2)
    memory.main.wait_frames(60)
    xbox.menu_b()
    memory.main.wait_frames(60)
    xbox.menu_down()
    xbox.menu_b()
    xbox.menu_b()
    FFXC.set_neutral()
    game_vars.print_arena_status()
    memory.main.wait_frames(30)


def check_yojimbo_possible():
    if memory.main.overdrive_state_2()[1] < 100:
        return False
    if (
        memory.main.overdrive_state_2()[1] == 100
        and memory.main.get_gil_value() < 300000
    ):
        item_dump()

    if (
        memory.main.overdrive_state_2()[1] == 100
        and memory.main.get_gil_value() >= 300000
    ):
        # Save game in preparation for the Yojimbo attempt
        memory.main.wait_frames(20)
        nemesis.arenaSelect.arena_menu_select(4)
        memory.main.full_party_format("kilikawoods1")
        if game_vars.yojimbo_get_index() == 1:
            save_game(first_save=True)
        else:
            save_game(first_save=False)

        # Now attempt to get Zanmato until successful, no re-saving.
        while not battles_5(game_vars.yojimbo_get_index()):
            quick_reset_logic()
        return True
    else:
        return False


def shinryu_battle():
    rikkuFirstTurn = False
    rikkuDriveComplete = False
    screen.await_turn()
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if screen.turn_rikku():
                if not rikkuFirstTurn:
                    battle.main.defend()
                elif rikkuDriveComplete:
                    battle.main._use_healing_item(item_id=9)
                else:
                    battle.main.rikku_full_od("shinryu")
                    rikkuDriveComplete = True
            elif screen.turn_tidus():
                if memory.main.get_overdrive_battle(0) == 100:
                    battle.overdrive.tidus(version=1)
                elif rikkuDriveComplete and not memory.main.state_auto_life():
                    auto_life()
                else:
                    battle.main.attack("none")
            else:
                battle.main.defend()

    # After battle stuff
    while not memory.main.menu_open():
        xbox.tap_b()
    FFXC.set_value("btn_b", 1)
    memory.main.wait_frames(150)
    FFXC.set_neutral()
    memory.main.wait_frames(2)
    return memory.main.battle_arena_results()


def battles_5(completion_version: int):
    print("Yojimbo battle number: ", completion_version)
    if completion_version >= 12 and completion_version != 99:
        return True  # These battles are complete at this point.
    yojimboSuccess = False

    # Now for the Yojimbo section
    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)

    # Battles here
    if completion_version == 1:
        nemesis.arenaSelect.start_fight(area_index=15, monster_index=1)
        if yojimbo_battle():
            game_vars.arena_success(array_num=2, index=1)
            yojimboSuccess = True

    elif completion_version == 2:
        nemesis.arenaSelect.start_fight(area_index=15, monster_index=2)
        if yojimbo_battle():
            game_vars.arena_success(array_num=2, index=2)
            yojimboSuccess = True

    elif completion_version == 3:
        nemesis.arenaSelect.start_fight(area_index=15, monster_index=3)
        if yojimbo_battle():
            game_vars.arena_success(array_num=2, index=3)
            yojimboSuccess = True

    elif completion_version == 4:
        nemesis.arenaSelect.start_fight(area_index=15, monster_index=4)
        if yojimbo_battle():
            game_vars.arena_success(array_num=2, index=4)
            yojimboSuccess = True

    elif completion_version == 5:
        nemesis.arenaSelect.start_fight(area_index=15, monster_index=5)
        if yojimbo_battle():
            game_vars.arena_success(array_num=2, index=5)
            yojimboSuccess = True

    elif completion_version == 6:
        nemesis.arenaSelect.start_fight(area_index=13, monster_index=12)
        if yojimbo_battle():
            game_vars.arena_success(array_num=0, index=12)
            yojimboSuccess = True

    elif completion_version == 7:
        nemesis.arenaSelect.start_fight(area_index=14, monster_index=13)
        if yojimbo_battle():
            game_vars.arena_success(array_num=1, index=13)
            yojimboSuccess = True

    elif completion_version == 8:
        nemesis.arenaSelect.start_fight(area_index=14, monster_index=11)
        if yojimbo_battle():
            game_vars.arena_success(array_num=1, index=11)
            yojimboSuccess = True

    elif completion_version == 9:
        nemesis.arenaSelect.start_fight(area_index=14, monster_index=7)
        if yojimbo_battle():
            game_vars.arena_success(array_num=1, index=7)
            yojimboSuccess = True

    elif completion_version == 10:
        nemesis.arenaSelect.start_fight(area_index=14, monster_index=6)
        if yojimbo_battle():
            game_vars.arena_success(array_num=1, index=6)
            yojimboSuccess = True

    elif completion_version == 11:
        nemesis.arenaSelect.start_fight(area_index=14, monster_index=4)
        if yojimbo_battle():
            game_vars.arena_success(array_num=1, index=4)
            yojimboSuccess = True

    elif completion_version == 99:  # Nemesis
        nemesis.arenaSelect.start_fight(area_index=15, monster_index=7)
        if yojimbo_battle():
            memory.main.click_to_diag_progress(2)
            memory.main.click_to_control_3()
            return True
        else:
            return False

    # Wrap up decisions
    if yojimboSuccess:
        game_vars.yojimbo_increment_index()
        if completion_version != 99:
            restock_downs()
        return True
    else:
        nemesis.arenaSelect.arena_menu_select(4)
        return False


def recharge_yuna():
    arena_npc()
    nemesis.arenaSelect.arena_menu_select(1)
    nemesis.arenaSelect.start_fight(area_index=13, monster_index=9)
    screen.await_turn()
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if screen.turn_yuna():
                battle.main.attack("none")
            else:
                battle.main.escape_one()


def nemesis_battle():
    if game_vars.yojimbo_get_index() < 12:
        nemesis.arenaSelect.arena_menu_select(4)
        touch_save()
        while game_vars.yojimbo_get_index() < 12:
            # If Yuna is charged, do next battle. Otherwise charge.
            if memory.main.overdrive_state_2()[1] == 100:
                battles_5(game_vars.yojimbo_get_index())
            else:
                recharge_yuna()
            nemesis.arenaSelect.arena_menu_select(4)
            touch_save()

    if memory.main.overdrive_state_2()[1] != 100:
        recharge_yuna()
    if memory.main.get_gil_value() < 300000:
        nemesis.arenaSelect.arena_menu_select(4)
        nemesis.menu.autoSortEquipment()
        # nemesis.menu.autoSortItems()
        arena_npc()
        nemesis.arenaSelect.arena_menu_select(2)
        memory.main.wait_frames(90)
        xbox.menu_right()
        xbox.menu_b()
        nemesis.menu.sellAll()
        xbox.menu_a()
        xbox.menu_a()
        xbox.menu_a()
        xbox.menu_a()
        xbox.menu_a()
        xbox.menu_a()
        xbox.menu_a()
    nemesis.arenaSelect.arena_menu_select(4)
    memory.main.full_party_format("kilikawoods1")
    save_game(first_save=False)
    while not battles_5(completion_version=99):
        quick_reset_logic()
    # nemesis.nemesis.arenaSelect.arenaMenuSelect(4)


def return_to_sin():
    FFXC = xbox.controller_handle()
    while not nemesis.targetPath.set_movement([-6, -27]):
        pass
    while not nemesis.targetPath.set_movement([-2, -2]):
        pass
    return_to_airship()

    nemesis.menu.equipWeapon(character=0, ability=0x8001, fullMenuClose=True)
    airship_destination(dest_num=0)
    memory.main.await_control()
    FFXC.set_movement(0, -1)
    memory.main.wait_frames(2)
    memory.main.await_event()
    FFXC.set_neutral()
