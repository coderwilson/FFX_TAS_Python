import logging

import battle.main
import battle.overdrive
import load_game
import memory.main
import menu
import nemesis.arena_select
import nemesis.menu
import nemesis.nemesis_pathing
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
    while not nemesis.nemesis_pathing.set_movement([-6, -27]):
        pass
    while not nemesis.nemesis_pathing.set_movement([-2, -2]):
        pass
    logger.debug("Arena - Touch Save Sphere, and actually save")
    save_sphere.touch_and_save(save_num=199)
    while not nemesis.nemesis_pathing.set_movement([-6, -27]):
        pass
    while not nemesis.nemesis_pathing.set_movement([2, -25]):
        pass


def touch_save(real_save=False):
    while not nemesis.nemesis_pathing.set_movement([-6, -27]):
        pass
    while not nemesis.nemesis_pathing.set_movement([-2, -2]):
        pass
    save_sphere.touch_and_go()
    while not nemesis.nemesis_pathing.set_movement([-6, -27]):
        pass
    while not nemesis.nemesis_pathing.set_movement([2, -25]):
        pass
    arena_npc()


def airship_destination(dest_num=0):  # Default to Sin.
    while memory.main.get_map() != 382:
        if memory.main.user_control():
            nemesis.nemesis_pathing.set_movement([-251, 340])
        else:
            FFXC.set_neutral()
        xbox.menu_b()
    while memory.main.diag_progress_flag() != 4:
        xbox.menu_b()
    logger.debug("Destination select on screen now.")
    while memory.main.map_cursor() != dest_num:
        if dest_num < 8:
            xbox.tap_down()
        else:
            xbox.tap_up()
    xbox.tap_b()
    memory.main.wait_frames(2)
    xbox.tap_b()
    memory.main.click_to_control_3()


def get_save_sphere_details():  # Should be obsolete
    map_val = memory.main.get_map()
    story_val = memory.main.get_story_progress()
    logger.debug("Map:", map_val, "| Story:", story_val)
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

    logger.debug("Values: [", x, ",", y, "] - ", diag)
    return [x, y, diag]


def return_to_airship():
    logger.debug("Attempting Return to Airship")

    ss_details = get_save_sphere_details()

    if memory.main.user_control():
        while memory.main.user_control():
            nemesis.nemesis_pathing.set_movement([ss_details[0], ss_details[1]])
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
            while not nemesis.nemesis_pathing.set_movement([-4, -21]):
                pass
            while not nemesis.nemesis_pathing.set_movement([-2, -2]):
                pass
        else:
            FFXC.set_neutral()
            if memory.main.save_menu_open():
                xbox.tap_a()
            elif memory.main.diag_progress_flag() == ss_details[2]:
                # logger.debug("Cursor test:", memory.save_menu_cursor())
                if memory.main.save_menu_cursor() != 1:
                    xbox.menu_down()
                else:
                    xbox.menu_b()
            elif memory.main.user_control():
                nemesis.nemesis_pathing.set_movement([ss_details[0], ss_details[1]])
                xbox.menu_b()
            elif memory.main.diag_skip_possible():
                xbox.menu_b()
            memory.main.wait_frames(4)
    logger.debug("Return to Airship Complete.")
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
    logger.debug("+Yuna Overdrive to summon Yojimbo")
    battle.overdrive.yuna()
    logger.debug("+Pay the man")
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
    logger.debug("Battle is complete.")
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
            logger.debug("Attempting Haste, but it's not Tidus's turn")
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
    logger.debug("### Battle Start:", memory.main.get_encounter_id())
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
    logger.debug("### Battle Start:", memory.main.get_encounter_id())
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
                logger.debug("Wrong position, moving away from sphere")
                while not nemesis.nemesis_pathing.set_movement([-6, -27]):
                    pass
                while not nemesis.nemesis_pathing.set_movement([2, -25]):
                    pass
            else:
                logger.debug("Engaging NPC")
                nemesis.nemesis_pathing.set_movement([5, -12])
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
    logger.debug("Mark 1")
    memory.main.wait_frames(3)  # This buffer can be improved later.
    logger.debug("Mark 2")


def restock_downs():
    logger.debug("Restocking phoenix downs")
    if memory.main.get_item_count_slot(memory.main.get_item_slot(6)) >= 80:
        logger.debug("Restock not needed. Disregard.")
        return
    arena_npc()
    nemesis.arena_select.arena_menu_select(3)
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
        nemesis.menu.equip_armor(character=1, ability=0x800A, full_menu_close=False)
    if not memory.main.equipped_armor_has_ability(char_num=4, ability_num=0x800A):
        nemesis.menu.equip_armor(character=4, ability=0x800A)
    memory.main.close_menu()
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=0)
    while not basic_quick_attacks():
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=0)
    game_vars.arena_success(array_num=0, index=0)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=1)
    aeon_start()
    auto_life()
    while not basic_quick_attacks(mega_phoenix=True):
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(4)
        memory.main.full_party_format("kilikawoods1")
        touch_save()
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=1)
        aeon_start()
        if screen.turn_tidus():
            auto_life()
    game_vars.arena_success(array_num=0, index=1)
    restock_downs()
    nemesis.arena_select.arena_menu_select(4)
    memory.main.full_party_format("kilikawoods1")
    menu.tidus_slayer(od_pos=0)

    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=2)
    while not basic_quick_attacks(yuna_autos=True):
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=2)
    game_vars.arena_success(array_num=0, index=2)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=3)
    while not basic_quick_attacks():
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=3)
    game_vars.arena_success(array_num=0, index=3)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=4)
    auto_life()
    while not basic_quick_attacks(mega_phoenix=True):
        logger.debug("Battle not completed successfully.")
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=4)
        auto_life()
    game_vars.arena_success(array_num=0, index=4)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=5)
    while not basic_quick_attacks():
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=5)
    game_vars.arena_success(array_num=0, index=5)
    restock_downs()

    check_yojimbo_possible()

    nemesis.arena_select.arena_menu_select(4)
    menu.tidus_slayer(od_pos=2)
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=6)
    while not basic_quick_attacks():
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=6)
    game_vars.arena_success(array_num=0, index=6)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=7)
    while not basic_quick_attacks():
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=7)
    game_vars.arena_success(array_num=0, index=7)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=8)
    while not basic_quick_attacks():
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=8)
    game_vars.arena_success(array_num=0, index=8)
    restock_downs()

    check_yojimbo_possible()

    nemesis.arena_select.arena_menu_select(4)
    menu.tidus_slayer(od_pos=0)
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=9)
    while not basic_quick_attacks(yuna_autos=True):
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=9)
    game_vars.arena_success(array_num=0, index=9)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=10)
    auto_life()
    while not basic_quick_attacks():
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=10)
        auto_life()
    game_vars.arena_success(array_num=0, index=10)
    restock_downs()

    check_yojimbo_possible()


def battles_2():
    logger.debug("++Starting second section++")
    nemesis.arena_select.arena_menu_select(4)
    touch_save()
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=14, monster_index=1)
    while not basic_quick_attacks():
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(4)
        touch_save()
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=14, monster_index=1)
    game_vars.arena_success(array_num=1, index=1)
    restock_downs()

    check_yojimbo_possible()

    nemesis.arena_select.arena_menu_select(4)
    touch_save()
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=14, monster_index=3)
    while not basic_quick_attacks():
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=14, monster_index=3)
    game_vars.arena_success(array_num=1, index=3)
    restock_downs()

    check_yojimbo_possible()

    nemesis.arena_select.arena_menu_select(4)
    touch_save()
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=14, monster_index=5)
    while not basic_quick_attacks():
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=14, monster_index=5)
    game_vars.arena_success(array_num=1, index=5)
    restock_downs()

    check_yojimbo_possible()

    nemesis.arena_select.arena_menu_select(4)
    touch_save()
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=14, monster_index=8)
    while not basic_quick_attacks():
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=14, monster_index=8)
    game_vars.arena_success(array_num=1, index=8)
    restock_downs()
    nemesis.arena_select.arena_menu_select(4)
    touch_save()

    check_yojimbo_possible()


def jug_farm_done():
    logger.debug("||| Slot: ", memory.main.get_item_slot(87))
    if memory.main.get_item_slot(87) > 250:
        return False
    else:
        logger.debug("Count: ", memory.main.get_item_count_slot(memory.main.get_item_slot(87)))
        if memory.main.get_item_count_slot(memory.main.get_item_slot(87)) < 6:
            return False
    return True


def juggernaut_farm():
    check_yojimbo_possible()
    while not jug_farm_done():
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=14, monster_index=12)
        auto_life()
        basic_quick_attacks(mega_phoenix=True, od_version=1)
        restock_downs()
        check_yojimbo_possible()
        nemesis.arena_select.arena_menu_select(4)
        touch_save()
    logger.debug("Good to go on strength spheres")
    game_vars.arena_success(array_num=1, index=12)
    logger.debug("Starting menu to finish strength.")
    nemesis.arena_select.arena_menu_select(4)
    nemesis.menu.str_boost()
    logger.debug("Touch save sphere, and then good to go.")
    touch_save()


def battles_3():
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=11)
    auto_life()
    while not basic_quick_attacks(mega_phoenix=True):
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=11)
        auto_life()
    game_vars.arena_success(array_num=0, index=11)
    restock_downs()

    check_yojimbo_possible()

    nemesis.arena_select.arena_menu_select(4)
    touch_save()
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=14, monster_index=2)
    aeon_start()
    auto_life()
    while not basic_attack(use_od=False):
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(4)
        touch_save()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=14, monster_index=2)
        auto_life()
    game_vars.arena_success(array_num=1, index=2)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=14, monster_index=0)
    auto_life()
    while not basic_quick_attacks(mega_phoenix=True, od_version=1):
        # Should use Slice & Dice
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=14, monster_index=0)
        auto_life()
    game_vars.arena_success(array_num=1, index=0)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=14, monster_index=9)
    auto_life()
    while not basic_quick_attacks(mega_phoenix=True, od_version=1):
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=14, monster_index=9)
        auto_life()
    game_vars.arena_success(array_num=1, index=9)
    restock_downs()

    check_yojimbo_possible()

    nemesis.arena_select.arena_menu_select(4)
    touch_save()
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=14, monster_index=10)
    auto_life()
    while not basic_quick_attacks(mega_phoenix=True, od_version=1):
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=14, monster_index=10)
        auto_life()
    game_vars.arena_success(array_num=1, index=10)
    restock_downs()

    check_yojimbo_possible()


def battles_4():
    nemesis.arena_select.arena_menu_select(4)
    touch_save()
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=15, monster_index=0)
    auto_life()
    while not basic_quick_attacks(mega_phoenix=True, od_version=1):
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=15, monster_index=0)
        auto_life()
    game_vars.arena_success(array_num=2, index=0)
    restock_downs()

    check_yojimbo_possible()
    nemesis.arena_select.arena_menu_select(4)
    touch_save()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=15, monster_index=6)

    while not shinryu_battle():
        logger.debug("Battle not completed successfully.")
        restock_downs()
        nemesis.arena_select.arena_menu_select(4)
        touch_save()
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=15, monster_index=6)

    game_vars.arena_success(array_num=2, index=6)
    restock_downs()


def item_dump():
    nemesis.arena_select.arena_menu_select(2)
    memory.main.wait_frames(90)
    xbox.menu_right()
    xbox.menu_b()
    nemesis.menu.sell_all(NEA=True)
    xbox.menu_a()
    xbox.menu_a()
    xbox.menu_a()
    xbox.menu_a()


def quick_reset_logic():
    reset.reset_to_main_menu()
    # memory.main.wait_frames(90)
    while memory.main.get_map() != 23:
        FFXC.set_value("btn_start", 1)
        memory.main.wait_frames(2)
        FFXC.set_value("btn_start", 0)
        memory.main.wait_frames(2)
    memory.main.wait_frames(60)
    xbox.menu_b()
    memory.main.wait_frames(60)
    load_game.load_save_num(199)
    FFXC.set_neutral()
    game_vars.print_arena_status()
    # memory.main.wait_frames(30)


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
        nemesis.arena_select.arena_menu_select(4)
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
    rikku_first_turn = False
    rikku_drive_complete = False
    screen.await_turn()
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if screen.turn_rikku():
                if not rikku_first_turn:
                    battle.main.defend()
                elif rikku_drive_complete:
                    battle.main._use_healing_item(item_id=9)
                else:
                    battle.main.rikku_full_od("shinryu")
                    rikku_drive_complete = True
            elif screen.turn_tidus():
                if memory.main.get_overdrive_battle(0) == 100:
                    battle.overdrive.tidus(version=1)
                elif rikku_drive_complete and not memory.main.state_auto_life():
                    auto_life()
                else:
                    battle.main.attack("none")
            else:
                battle.main.defend()

    # After battle stuff
    while not memory.main.menu_open():
        xbox.tap_b()
    FFXC.set_value("btn_b", 1)
    memory.main.wait_frames(170)
    FFXC.set_neutral()
    memory.main.wait_frames(2)
    return memory.main.battle_arena_results()


def battles_5(completion_version: int):
    logger.debug("Yojimbo battle number: ", completion_version)
    if completion_version >= 12 and completion_version != 99:
        return True  # These battles are complete at this point.
    yojimbo_success = False

    # Now for the Yojimbo section
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)

    # Battles here
    if completion_version == 1:
        nemesis.arena_select.start_fight(area_index=15, monster_index=1)
        if yojimbo_battle():
            game_vars.arena_success(array_num=2, index=1)
            yojimbo_success = True

    elif completion_version == 2:
        nemesis.arena_select.start_fight(area_index=15, monster_index=2)
        if yojimbo_battle():
            game_vars.arena_success(array_num=2, index=2)
            yojimbo_success = True

    elif completion_version == 3:
        nemesis.arena_select.start_fight(area_index=15, monster_index=3)
        if yojimbo_battle():
            game_vars.arena_success(array_num=2, index=3)
            yojimbo_success = True

    elif completion_version == 4:
        nemesis.arena_select.start_fight(area_index=15, monster_index=4)
        if yojimbo_battle():
            game_vars.arena_success(array_num=2, index=4)
            yojimbo_success = True

    elif completion_version == 5:
        nemesis.arena_select.start_fight(area_index=15, monster_index=5)
        if yojimbo_battle():
            game_vars.arena_success(array_num=2, index=5)
            yojimbo_success = True

    elif completion_version == 6:
        nemesis.arena_select.start_fight(area_index=13, monster_index=12)
        if yojimbo_battle():
            game_vars.arena_success(array_num=0, index=12)
            yojimbo_success = True

    elif completion_version == 7:
        nemesis.arena_select.start_fight(area_index=14, monster_index=13)
        if yojimbo_battle():
            game_vars.arena_success(array_num=1, index=13)
            yojimbo_success = True

    elif completion_version == 8:
        nemesis.arena_select.start_fight(area_index=14, monster_index=11)
        if yojimbo_battle():
            game_vars.arena_success(array_num=1, index=11)
            yojimbo_success = True

    elif completion_version == 9:
        nemesis.arena_select.start_fight(area_index=14, monster_index=7)
        if yojimbo_battle():
            game_vars.arena_success(array_num=1, index=7)
            yojimbo_success = True

    elif completion_version == 10:
        nemesis.arena_select.start_fight(area_index=14, monster_index=6)
        if yojimbo_battle():
            game_vars.arena_success(array_num=1, index=6)
            yojimbo_success = True

    elif completion_version == 11:
        nemesis.arena_select.start_fight(area_index=14, monster_index=4)
        if yojimbo_battle():
            game_vars.arena_success(array_num=1, index=4)
            yojimbo_success = True

    elif completion_version == 99:  # Nemesis
        nemesis.arena_select.start_fight(area_index=15, monster_index=7)
        if yojimbo_battle():
            memory.main.click_to_diag_progress(2)
            memory.main.click_to_control_3()
            return True
        else:
            return False

    # Wrap up decisions
    if yojimbo_success:
        game_vars.yojimbo_increment_index()
        if completion_version != 99:
            restock_downs()
        return True
    else:
        nemesis.arena_select.arena_menu_select(4)
        return False


def recharge_yuna():
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=9)
    screen.await_turn()
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if screen.turn_yuna():
                battle.main.attack("none")
            else:
                battle.main.escape_one()


def nemesis_battle():
    if game_vars.yojimbo_get_index() < 12:
        nemesis.arena_select.arena_menu_select(4)
        touch_save()
        while game_vars.yojimbo_get_index() < 12:
            # If Yuna is charged, do next battle. Otherwise charge.
            if memory.main.overdrive_state_2()[1] == 100:
                battles_5(game_vars.yojimbo_get_index())
            else:
                recharge_yuna()
            nemesis.arena_select.arena_menu_select(4)
            touch_save()

    if memory.main.overdrive_state_2()[1] != 100:
        recharge_yuna()
    if memory.main.get_gil_value() < 300000:
        nemesis.arena_select.arena_menu_select(4)
        nemesis.menu.auto_sort_equipment()
        # nemesis.menu.auto_sort_items()
        arena_npc()
        nemesis.arena_select.arena_menu_select(2)
        memory.main.wait_frames(90)
        xbox.menu_right()
        xbox.menu_b()
        nemesis.menu.sell_all()
        xbox.menu_a()
        xbox.menu_a()
        xbox.menu_a()
        xbox.menu_a()
        xbox.menu_a()
        xbox.menu_a()
        xbox.menu_a()
    nemesis.arena_select.arena_menu_select(4)
    memory.main.full_party_format("kilikawoods1")
    save_game(first_save=False)
    while not battles_5(completion_version=99):
        quick_reset_logic()
    # nemesis.nemesis.arena_select.arena_menu_select(4)


def return_to_sin():
    FFXC = xbox.controller_handle()
    while not nemesis.nemesis_pathing.set_movement([-6, -27]):
        pass
    while not nemesis.nemesis_pathing.set_movement([-2, -2]):
        pass
    return_to_airship()

    nemesis.menu.equip_weapon(character=0, ability=0x8001, full_menu_close=True)
    airship_destination(dest_num=0)
    memory.main.await_control()
    FFXC.set_movement(0, -1)
    memory.main.wait_frames(2)
    memory.main.await_event()
    FFXC.set_neutral()
