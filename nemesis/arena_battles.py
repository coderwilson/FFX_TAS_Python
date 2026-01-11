import logging

import area.dream_zan
import battle.main
import battle.overdrive
import battle.utils
import load_game
import memory.main
import menu
import nemesis.arena_select
from nemesis.arena_prep import arena_npc
from json_ai_files.write_seed import write_custom_message
import nemesis.menu
import pathing
import reset
import save_sphere
import screen
import vars
import xbox

from memory.yojimbo_rng import zanmato_gil_needed, first_turn_action_occurs
from players import CurrentPlayer, Rikku, Tidus, Wakka, Yojimbo, Yuna, Lulu
from json_ai_files.write_seed import write_big_text
from gamestate import game
from sphere_grid.completion_functions import get_grid

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()

# The following functions extend the regular Bahamut run. Arena battles sections.


def zan_ready():
    needed_amount = zanmato_gil_needed()  # Set value
    if needed_amount > memory.main.get_gil_value() or first_turn_action_occurs():
        return False
    if Yuna.overdrive_percent() < 100:
        return False
    return True

def update_stream():
    success = 0
    total = 0
    array1,array2,array3 = game_vars.arena_arrays()
    for i in range(len(array1)):
        total += 1
        if array1[i] == 1:
            success += 1
    
    for i in range(len(array2)):
        total += 1
        if array2[i] == 1:
            success += 1
    
    for i in range(len(array3)):
        total += 1
        if array3[i] == 1:
            success += 1
    complete_percent = int(success / total * 100)
    if game.state == "Nem_Arena":
        str = f"Monster Arena Battles\nArena battle completion {complete_percent}%\n{success} / {total}\n"
        str += f"{game.state} | {game.step}"
        write_big_text(str)
        write_custom_message(str)

    


def save_game(actually_save=True):
    logger.info("Attempting to save")
    #if memory.main.get_coords()[1] < -4:
    while not pathing.set_movement([-6, -24]):
        pass
    while not pathing.set_movement([-2, -2]):
        pass
    if memory.main.get_actor_angle(0) < 1:
        xbox.menu_up()
        memory.main.wait_frames(12)
    logger.debug("Arena - Touch Save Sphere, and actually save")
    if actually_save:
        save_sphere.touch_and_save(save_num=199)
    else:
        save_sphere.touch_and_go()
    
    while memory.main.get_actor_angle(0) > -1:
        xbox.menu_down()
        memory.main.wait_frames(12)


def touch_save(real_save=False):
    nemesis.arena_select.arena_menu_select(4)
    save_game(actually_save=real_save)


def airship_destination(dest_num=0):  # Default to Sin.
    while memory.main.get_map() != 382:
        if memory.main.user_control():
            pathing.set_movement([-251, 340])
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
    logger.debug(f"Map:{map_val}| Story:{story_val}")
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

    logger.debug(f"Values: [{x},{y}] - {diag}")
    return [x, y, diag]


def return_to_airship():
    logger.debug("Attempting Return to Airship")

    ss_details = get_save_sphere_details()

    if memory.main.user_control():
        if memory.main.get_coords()[1] < -10:
            while not pathing.set_movement([-6, -27]):
                pass
            while not pathing.set_movement([-2, -2]):
                pass
        elif memory.main.get_actor_angle(0) < 1:
            while memory.main.get_actor_angle(0) < 1:
                xbox.menu_up()
                memory.main.wait_frames(12)
        while memory.main.user_control():
            pathing.set_movement([ss_details[0], ss_details[1]])
            xbox.tap_b()
            memory.main.wait_frames(1)
    FFXC.set_neutral()

    while memory.main.get_map() not in [194, 374]:
        if memory.main.get_map() == 307 and memory.main.get_coords()[1] < -5:
            while not pathing.set_movement([-4, -21]):
                pass
            while not pathing.set_movement([-2, -2]):
                pass
        else:
            FFXC.set_neutral()
            if memory.main.save_menu_open():
                xbox.tap_a()
            elif memory.main.diag_progress_flag() == ss_details[2]:
                if memory.main.save_menu_cursor() != 1:
                    xbox.menu_down()
                else:
                    xbox.menu_b()
            elif memory.main.user_control():
                pathing.set_movement([ss_details[0], ss_details[1]])
                xbox.menu_b()
            elif memory.main.diag_skip_possible():
                xbox.menu_b()
            memory.main.wait_frames(4)
    logger.debug("Return to Airship Complete.")
    memory.main.clear_save_menu_cursor()
    memory.main.clear_save_menu_cursor_2()


def aeon_start():
    screen.await_turn()
    battle.main.buddy_swap(Yuna)
    battle.main.aeon_summon(4)
    while not Tidus.is_turn():
        if memory.main.turn_ready():
            if screen.turn_aeon():
                CurrentPlayer().attack()
            else:
                CurrentPlayer().defend()
        elif not memory.main.battle_active():
            return False


@battle.utils.speedup_decorator
def yojimbo_battle(
    flee_available:bool=True, 
    diag_after:bool=False, 
    arena:bool=True, 
    anima:int=0
):
    if game.state == "Nem_Arena" and game_vars.platinum():
        anima=1
    success_check = False
    aeon_summoned = False
    zanmato_gil_needed()  # Report
    while not (memory.main.turn_ready() and Yuna.is_turn()):
        if not Yuna.active():
            battle.main.buddy_swap(Yuna)
        elif memory.main.turn_ready():
            CurrentPlayer().defend()
            memory.main.wait_frames(15)
        if not memory.main.battle_active():
            break
    if memory.main.battle_active():
        logger.debug("Yuna Overdrive to summon Yojimbo")
        Yuna.overdrive(aeon_num=5+anima)
        aeon_summoned=True
        if memory.main.game_over():
            return False
        
        needed_amount = zanmato_gil_needed()  # Set value
        success_check = True
        if needed_amount > 270000:
            needed_amount = 1
            success_check = False
        logger.debug(f"Pay the man: {needed_amount}")
        Yojimbo.pay(gil_value=needed_amount)
        memory.main.wait_frames(90)
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Yuna.is_turn():
                if not aeon_summoned:
                    logger.debug("Yuna Overdrive to summon Yojimbo")
                    Yuna.overdrive(aeon_num=5+anima)
                    aeon_summoned = True
                else:
                    Yuna.defend()
            if Tidus.is_turn():
                logger.debug("Tidus atempt flee")
                if flee_available:
                    Tidus.flee()
                    success_check = False
                else:
                    CurrentPlayer().defend()
            elif Yojimbo.is_turn():
                
                # May still be able to get it?
                needed_amount = zanmato_gil_needed()  # Set value
                success_check = True
                if needed_amount > 258000:
                    needed_amount = 1
                    success_check = False
                Yojimbo.pay(gil_value=needed_amount)
                memory.main.wait_frames(90)
            else:
                CurrentPlayer().defend()
    
        if memory.main.game_over():
            success_check = False
            return False
    if memory.main.game_over():
        success_check = False
        return False
    
    if arena:
        logger.debug("Yojimbo Battle is complete.")
        # After battle stuff
        battle.main.wrap_up()
        logger.debug("Yojimbo wrap-up is complete.")
        memory.main.wait_frames(2)
        if diag_after:
            return True
        while not memory.main.diag_skip_possible():
            if memory.main.user_control():
                return True
        logger.debug("Yojimbo - menu restored")
        memory.main.wait_frames(1)
        nemesis.arena_select.arena_menu_select(4)
        #save_game(actually_save=False)
        return memory.main.battle_arena_results()
    else:
        memory.main.click_to_control()
        return success_check

def one_eye_battle(killer:str = "any",drops_for:int = 0, cap_weap=True):
    if memory.main.equipped_weapon_has_ability(char_num=0, ability_num=0x807A):
        menu.equip_weapon(character=0, ability=32772,full_menu_close=True)  # Evade & Counter (Caldabolg)

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=14, monster_index=5)
    battle.main.one_eye(killer=killer)
    game_vars.arena_success(array_num=1, index=5)
    nemesis.arena_select.arena_menu_select(4)
    restock_downs()

    # Now we need to equip and customize the armor.
    menu.auto_sort_equipment(manual="n")
    menu.add_ability(
        owner=drops_for,
        equipment_type=0,
        ability_array=[32787, 255, 255, 255],
        ability_index=0x8011,
        slot_count=3,
        navigate_to_equip_menu=True,
        exit_out_of_current_weapon=True,
        close_menu=True,
        full_menu_close=True,
    )
    game_vars.plat_triple_ap_update(drops_for)
    if drops_for in [4,6]:
        menu.add_ability(
            owner=drops_for,
            equipment_type=0,
            ability_array=[32787, 0x8011, 255, 255],
            ability_index=0x8001,
            slot_count=3,
            navigate_to_equip_menu=True,
            exit_out_of_current_weapon=True,
            close_menu=True,
            full_menu_close=True,
        )
    menu.equip_weapon(character=drops_for, ability_list=[32787,0x8011],full_menu_close=False)
    if cap_weap:
        menu.equip_weapon(character=0, ability=0x807A,full_menu_close=True)

@battle.utils.speedup_decorator
def basic_quick_attacks(
    mega_phoenix=False,
    skip_throw=False,
    prefer_overdrives=False,
    game_over_return:bool=False,
    quick_return:bool=False
):
    logger.info(f"Battle Start:{memory.main.get_encounter_id()}")
    FFXC.set_neutral()
    item_thrown = skip_throw
    quick_hit_count = 0
    restore_mp = False
    yojimbo_summon = game_vars.yojimbo_unlocked() and (
        bool(zanmato_gil_needed() > 258000) or
        bool(first_turn_action_occurs())
    )
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Tidus.is_turn():
                logger.warning(f"Tidus MP: {Tidus.mp()}")
                if mega_phoenix and screen.faint_check() >= 2:
                    battle.main.revive(item_num=7)
                elif memory.main.get_overdrive_battle(0) == 100:
                    #Tidus.overdrive(version=od_version)
                    Tidus.overdrive()
                elif Tidus.mp() >= 36:
                    battle.main.quick_hit()  # Quick hit
                    quick_hit_count += 1
                else:
                    Tidus.attack()
                if Tidus.mp() < 100:
                    restore_mp = True
            elif Yojimbo.is_turn():
                Yojimbo.pay(gil_value=1)
            elif screen.turn_aeon():
                CurrentPlayer().attack()
            elif Yuna.is_turn():
                if not item_thrown:
                    logger.debug("Yuna will attempt to throw an item.")
                    twin_slot = memory.main.get_use_items_slot(item_num=66)
                    three_slot = memory.main.get_use_items_slot(item_num=69)
                    logger.debug(f"Slots for throwable items: {twin_slot}, {three_slot}")
                    
                    if memory.main.get_encounter_id() in [788,797,800]:
                        logger.debug("Do not throw an item for this battle.")
                        Yuna.defend()
                    elif twin_slot != 255:
                        # Twin stars, one target.
                        # battle.main.use_item(slot=twin_slot,target=0)
                        battle.main.use_item_new(item=66)
                    elif three_slot != 255:
                        # battle.main.use_item(slot=three_slot)
                        battle.main.use_item_new(item=69)
                    else:
                        Yuna.defend()
                    #memory.main.wait_seconds(10)
                    item_thrown = True
                elif yojimbo_summon:
                    logger.debug("Yuna will attempt to summon Yojimbo (RNG manip)")
                    if game_vars.platinum():
                        battle.main.aeon_summon(6)
                    else:
                        battle.main.aeon_summon(5)
                    yojimbo_summon = False
                    restore_mp = True
                elif (
                    memory.main.get_encounter_id() in [788,797,800] and
                    Yuna.overdrive_percent() != 100
                ):
                    logger.debug("Yuna will attack to gain Overdrive charge")
                    Yuna.attack()
                elif not Yuna.active():
                    battle.main.buddy_swap(Yuna)
                elif not Tidus.active():
                    battle.main.buddy_swap(Tidus)
                else:
                    logger.debug("Yuna will defend")
                    Yuna.defend()
            elif Wakka.is_turn() and memory.main.get_encounter_id() == 777:
                Wakka.aim()
            elif Wakka.is_turn() and game_vars.platinum():
                Wakka.attack()
            elif Wakka.is_turn() and prefer_overdrives and memory.main.get_overdrive_battle(4) == 100:
                Wakka.overdrive(reels="attack")
            elif not Wakka.active():
                battle.main.buddy_swap(Wakka)
            else:
                CurrentPlayer().defend()

    # After battle stuff
    battle.main.wrap_up()
    logger.debug("Battle is complete.")
    if (game_over_return and memory.main.game_over()) or quick_return:
        return False
    memory.main.wait_frames(2)
    while not memory.main.diag_skip_possible():
        pass
    memory.main.wait_frames(1)
    nemesis.arena_select.arena_menu_select(4)
    memory.main.update_formation(Tidus, Yuna, Rikku)
    if restore_mp:
        save_game(actually_save=False)
    return memory.main.battle_arena_results()



@battle.utils.speedup_decorator
def basic_attack(
    mega_phoenix=False, od_version: int = 0, use_od=False, yuna_autos=False
):
    logger.debug(f"Battle Start:{memory.main.get_encounter_id()}")
    FFXC.set_neutral()
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Tidus.is_turn():
                if mega_phoenix and screen.faint_check() >= 2:
                    battle.main.revive(item_num=7)
                elif use_od and memory.main.get_overdrive_battle(0) == 100:
                    Tidus.overdrive()
                else:
                    CurrentPlayer().attack()
            elif Yuna.is_turn() and yuna_autos:
                CurrentPlayer().attack()
            elif screen.turn_aeon():
                CurrentPlayer().attack()
            else:
                CurrentPlayer().defend()

    # After battle stuff
    battle.main.wrap_up()
    logger.debug("Battle is complete.")
    memory.main.wait_frames(2)
    while not memory.main.diag_skip_possible():
        pass
    memory.main.wait_frames(1)
    nemesis.arena_select.arena_menu_select(4)
    #save_game(actually_save=False)
    return memory.main.battle_arena_results()

def restock_downs():
    # update_stream()
    logger.debug("Restocking phoenix downs")
    if memory.main.get_item_count_slot(memory.main.get_item_slot(6)) >= 80:
        logger.debug("Restock not needed. Disregard.")
        return
    armor_check()
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
    while memory.main.menu_open():
        xbox.tap_back()
    nemesis.arena_select.arena_menu_select(4)


def battles_1():
    logger.info("We are ready to start fighting monsters!")
    if memory.main.get_map() == 374:
        logger.info("Returning to the arena.")
        nemesis.arena_select.arena_return()
    update_stream()
    menu.tidus_slayer(od_pos=0)
    if not memory.main.equipped_weapon_has_ability(char_num=1, ability_num=0x8019):
        menu.equip_weapon(character=1, ability=0x8019, full_menu_close=True)
    logger.debug("Mark 1")

    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=2)
    while not basic_quick_attacks(mega_phoenix=True):
        logger.debug("Battle not completed successfully.")
        restock_downs()
        memory.main.update_formation(Tidus, Yuna, Rikku)
        touch_save()
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=2)
    game_vars.arena_success(array_num=0, index=2)
    nemesis.arena_select.arena_menu_select(4)
    restock_downs()
    memory.main.update_formation(Tidus, Yuna, Rikku)

    check_yojimbo_possible()
    

    nemesis.arena_select.arena_menu_select(4)
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=5)
    while not basic_quick_attacks():
        logger.debug("Battle not completed successfully.")
        restock_downs()
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=5)
    game_vars.arena_success(array_num=0, index=5)
    nemesis.arena_select.arena_menu_select(4)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=9)
    while not basic_quick_attacks():
        logger.debug("Battle not completed successfully.")
        restock_downs()
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=9)
    game_vars.arena_success(array_num=0, index=9)
    nemesis.arena_select.arena_menu_select(4)
    restock_downs()

    check_yojimbo_possible()


def battles_2():
    logger.debug("Starting second section")
    nemesis.arena_select.arena_menu_select(4)
    touch_save()
    if Tidus.overdrive_percent() != 100:
        menu.tidus_slayer(od_pos=0)
        recharge_overdrives(check_weap=False)
    menu.tidus_slayer(od_pos=5)
    check_yojimbo_possible()
    memory.main.update_formation(Tidus, Yuna, Wakka)

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=14, monster_index=0)
    battle.main.auto_life(target=0)
    while not basic_quick_attacks(mega_phoenix=True, skip_throw=True):
        # Should use Slice & Dice
        logger.debug("Battle not completed successfully.")
        restock_downs()
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=14, monster_index=0)
        battle.main.auto_life(target=0)
    game_vars.arena_success(array_num=1, index=0)
    nemesis.arena_select.arena_menu_select(4)
    menu.tidus_slayer(od_pos=1)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=0)
    while not basic_quick_attacks():
        logger.debug("Battle not completed successfully.")
        restock_downs()
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=0)
    game_vars.arena_success(array_num=0, index=0)
    nemesis.arena_select.arena_menu_select(4)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=4)
    battle.main.auto_life(target=0)
    while not basic_quick_attacks(mega_phoenix=True,skip_throw=True):
        logger.debug("Battle not completed successfully.")
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=4)
        battle.main.auto_life(target=0)
    game_vars.arena_success(array_num=0, index=4)
    nemesis.arena_select.arena_menu_select(4)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=6)
    while not basic_quick_attacks():
        logger.debug("Battle not completed successfully.")
        restock_downs()
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=6)
    game_vars.arena_success(array_num=0, index=6)
    nemesis.arena_select.arena_menu_select(4)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=3)
    while not basic_quick_attacks():
        logger.debug("Battle not completed successfully.")
        restock_downs()
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=3)
    game_vars.arena_success(array_num=0, index=3)
    nemesis.arena_select.arena_menu_select(4)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=7)
    while not basic_quick_attacks():
        logger.debug("Battle not completed successfully.")
        restock_downs()
        arena_npc()
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
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=8)
    game_vars.arena_success(array_num=0, index=8)
    nemesis.arena_select.arena_menu_select(4)
    restock_downs()

    check_yojimbo_possible()

    nemesis.arena_select.arena_menu_select(4)
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=10)
    battle.main.auto_life(target=0)
    while not basic_quick_attacks(skip_throw=True):
        logger.debug("Battle not completed successfully.")
        restock_downs()
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=10)
        battle.main.auto_life(target=0)
    game_vars.arena_success(array_num=0, index=10)
    nemesis.arena_select.arena_menu_select(4)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=1)
    aeon_start()
    battle.main.auto_life(target=0)
    while not basic_quick_attacks(skip_throw=True):
        logger.debug("Battle not completed successfully.")
        restock_downs()
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=1)
        aeon_start()
        battle.main.auto_life(target=0)
    game_vars.arena_success(array_num=0, index=1)
    nemesis.arena_select.arena_menu_select(4)
    restock_downs()

    check_yojimbo_possible()
    if Tidus.overdrive_percent() != 100:
        menu.tidus_slayer(od_pos=0)
        recharge_overdrives(check_weap=False)
    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=14, monster_index=1)
    while not basic_quick_attacks():
        logger.debug("Battle not completed successfully.")
        restock_downs()
        touch_save()
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=14, monster_index=1)
    game_vars.arena_success(array_num=1, index=1)
    nemesis.arena_select.arena_menu_select(4)
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
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=14, monster_index=3)
    game_vars.arena_success(array_num=1, index=3)
    nemesis.arena_select.arena_menu_select(4)
    restock_downs()

    check_yojimbo_possible()
    if game_vars.arena_arrays()[1][5] != 1:
        nemesis.arena_select.arena_menu_select(4)
        touch_save()
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=14, monster_index=5)
        while not basic_quick_attacks():
            logger.debug("Battle not completed successfully.")
            restock_downs()
            arena_npc()
            nemesis.arena_select.arena_menu_select(1)
            nemesis.arena_select.start_fight(area_index=14, monster_index=5)
        game_vars.arena_success(array_num=1, index=5)
        nemesis.arena_select.arena_menu_select(4)
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
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=14, monster_index=8)
    game_vars.arena_success(array_num=1, index=8)
    nemesis.arena_select.arena_menu_select(4)
    restock_downs()
    touch_save()

    check_yojimbo_possible()


def juggernaught_battle():
    attack_count = 0
    nulblaze_used = False
    yojimbo_summon = (
        bool(zanmato_gil_needed() > 258000) or
        bool(first_turn_action_occurs())
    )
    mega_phoenix = False
    revive = False
    battle.main.auto_life(target=0)
    while memory.main.battle_active():
        if memory.main.turn_ready():
            ab_pot_slot = memory.main.get_use_items_slot(item_num=20)
            if Tidus.is_turn():
                if screen.faint_check() >= 2:
                    battle.main.revive(item_num=7)
                    mega_phoenix = True
                elif attack_count > 5 and not nulblaze_used:
                    battle.main.nulblaze()
                    nulblaze_used = True
                elif memory.main.get_overdrive_battle(0) == 100:
                    #Tidus.overdrive(version=od_version)
                    Tidus.overdrive()
                    attack_count += 1
                elif Tidus.mp() >= 36:
                    battle.main.quick_hit()  # Quick hit
                    attack_count += 1
                else:
                    Tidus.attack()
                    attack_count += 1
                logger.warning(f"Attack count: {attack_count}")
            elif Yuna.is_turn() and yojimbo_summon and mega_phoenix:
                logger.debug("Yuna will attempt to summon Yojimbo (RNG manip)")
                if game_vars.platinum():
                    battle.main.aeon_summon(6)
                else:
                    battle.main.aeon_summon(5)
                yojimbo_summon = False
                revive = True
            elif Yojimbo.is_turn():
                # May still be able to get it?
                Yojimbo.pay(gil_value=1)
            else:
                CurrentPlayer().defend()
    battle.main.wrap_up()
    if revive:
        memory.main.wait_frames(15)
        nemesis.arena_select.arena_menu_select(4)
        touch_save()


def jug_farm_done():
    logger.debug(f"Slot: {memory.main.get_item_slot(87)}")
    if memory.main.get_item_slot(87) > 250:
        return False
    elif game_vars.platinum():
        if memory.main.get_item_count_slot(memory.main.get_item_slot(87)) < 16:
            return False
    else:
        if memory.main.get_item_count_slot(memory.main.get_item_slot(87)) < 7:
            return False
    return True

def juggernaut_single():
    memory.main.update_formation(Tidus, Wakka, Rikku)
    arena_npc()
    while (
        memory.main.get_item_slot(57) == 255 or
        memory.main.get_item_count_slot(memory.main.get_item_slot(57)) < 20
    ):
        nemesis.arena_select.arena_menu_select(4)
        memory.main.await_control()
        arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=14, monster_index=12)
    juggernaught_battle()
    touch_save()
    restock_downs()
    game_vars.arena_success(array_num=1, index=12)
    nemesis.arena_select.arena_menu_select(4)


def juggernaut_farm(include_yojimbo:bool=True):
    if include_yojimbo:
        check_yojimbo_possible()
    if include_yojimbo and game_vars.platinum():
        logger.debug(f"Merging Plat and Nemesis. We already did Juggernaught farm. Return.")
        return
    write_custom_message("Detour 1\nJuggernauts for\nMAXIMUM STRENGTH!!!")
    if not memory.main.equipped_armor_has_ability(char_num=0, ability_num=0x800A):
        menu.equip_armor(character=0, ability=0x800A, full_menu_close=False)
    if not memory.main.equipped_armor_has_ability(char_num=4, ability_num=0x800A):
        menu.equip_armor(character=4, ability=0x800A)
    power_count = memory.main.get_item_count_slot(memory.main.get_item_slot(87))
    if game_vars.platinum():
        memory.main.update_formation(Tidus, Wakka, Rikku)
        big_text = f"Strength Sphere count: {power_count}/16"
    else:
        memory.main.update_formation(Tidus, Yuna, Rikku)
        big_text = f"Strength Sphere count: {power_count}/7"
    arena_npc()
    if game_vars.platinum():
        while (
            (
                memory.main.get_item_slot(64) == 255 or
                memory.main.get_item_count_slot(memory.main.get_item_slot(64)) < 20
            ) and (
                memory.main.get_item_slot(57) == 255 or
                memory.main.get_item_count_slot(memory.main.get_item_slot(57)) < 20
            )
        ):
            nemesis.arena_select.arena_menu_select(4)
            memory.main.await_control()
            arena_npc()
    else:
        while (
            memory.main.get_item_slot(57) == 255 or
            memory.main.get_item_count_slot(memory.main.get_item_slot(57)) < 20
        ):
            nemesis.arena_select.arena_menu_select(4)
            memory.main.await_control()
            arena_npc()
    while not jug_farm_done():
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=14, monster_index=12)
        write_big_text(big_text)
        juggernaught_battle()
        nemesis.arena_select.arena_menu_select(4)
        if game_vars.check_plat_test_mode():
            # Only works if plat test mode is active.
            memory.main.set_item_count(item_num=87,quantity=16)
        power_count = memory.main.get_item_count_slot(memory.main.get_item_slot(87))
        if game_vars.platinum():
            memory.main.update_formation(Tidus, Wakka, Rikku)
            big_text = f"Strength Sphere count: {power_count}/16"
        else:
            memory.main.update_formation(Tidus, Yuna, Rikku)
            big_text = f"Strength Sphere count: {power_count}/7"
        write_big_text(big_text)
        touch_save()
        restock_downs()
        if include_yojimbo:
            check_yojimbo_possible()
    logger.debug("Good to go on strength spheres")
    game_vars.arena_success(array_num=1, index=12)
    logger.debug("Starting menu to finish strength.")
    nemesis.arena_select.arena_menu_select(4)
    nemesis.menu.str_boost()
    if not game_vars.platinum():
        memory.main.update_formation(Tidus, Yuna, Rikku)
    # write_custom_message("Detour 2\nSteal from evil eyes\nfor 48 musk\ninto confuseproof\non Wakka")
    # musk_farm()
    logger.debug("Touch save sphere, and then good to go.")


def vidatu_farm_done():
    logger.debug(f"Slot: {memory.main.get_item_slot(87)}")
    if memory.main.get_item_slot(86) > 250:
        return False
    # grid_instance = get_grid()
    # empty_need = min(96, grid_instance.count_nodes_of_type(node_type=0x01))
    empty_need = 96
    if memory.main.get_item_count_slot(memory.main.get_item_slot(86)) < empty_need:
        return False
    return True


def vidatu_farm():
    # grid_instance = get_grid()
    # empty_need = min(96, grid_instance.count_nodes_of_type(node_type=0x01))
    empty_need = 96
    current = memory.main.get_item_count_slot(memory.main.get_item_slot(86))
    write_custom_message(f"Detour 2\Vidatu for MP nodes\n{current}/{empty_need}")
    if not memory.main.equipped_armor_has_ability(char_num=0, ability_num=0x800A):
        logger.debug("Vidatu: armor for Tidus")
        menu.equip_armor(character=0, ability=0x800A, full_menu_close=False)
    if not memory.main.equipped_armor_has_ability(char_num=4, ability_num=0x800A):
        logger.debug("Vidatu: armor for Wakka")
        menu.equip_armor(character=4, ability=0x800A)
    memory.main.update_formation(Tidus, Wakka, Rikku)
    big_text = f"MP Sphere count: {current}/{empty_need}"
    while not vidatu_farm_done():
        if memory.main.get_gil_value() < 10000:
            item_dump()
        memory.main.update_formation(Tidus, Wakka, Rikku)
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=14, monster_index=4)
        write_big_text(big_text)
        basic_quick_attacks(mega_phoenix=False,skip_throw=True)
        if game_vars.check_plat_test_mode():
            # Only works if plat test mode is active.
            memory.main.set_item_count(item_num=86,quantity=99)
        nemesis.arena_select.arena_menu_select(4)
        current = memory.main.get_item_count_slot(memory.main.get_item_slot(86))
        big_text = f"MP Sphere count: {current}/{empty_need}"
        write_custom_message(f"Detour 2\Vidatu for MP nodes\n{current}/{empty_need}")
        touch_save()
        restock_downs()
    write_big_text("")
    logger.debug("Good to go on MP spheres spheres")
    game_vars.arena_success(array_num=1, index=4)
    nemesis.arena_select.arena_menu_select(4)
    memory.main.update_formation(Tidus, Yuna, Rikku)
    logger.debug("Touch save sphere, and then good to go.")


def musk_steal_battle():
    steal_complete = False
    while memory.main.battle_active():
        if Yuna.is_turn():
            battle.main.steal()
            steal_complete = True
        elif Rikku.is_turn():
            battle.main.steal(steal_position=1)
        elif steal_complete and Tidus.is_turn():
            Tidus.flee()
        else:
            CurrentPlayer().defend()
    battle.main.wrap_up()


def musk_farm():
    memory.main.update_formation(Tidus, Yuna, Rikku)
    Yuna.update_battle_menu([0,23,20,21,22,1])
    musk_slot = memory.main.get_item_slot(102)
    logger.debug(f"Musk Slot {musk_slot}")
    musk_count = memory.main.get_item_count_slot(musk_slot)
    logger.debug(f"Musk count: {musk_count}")
    arena_npc()
    while musk_count < 48:
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=12, monster_index=1)
        musk_steal_battle()
        musk_slot = memory.main.get_item_slot(102)
        logger.debug(f"Musk Slot {musk_slot}")
        musk_count = memory.main.get_item_count_slot(musk_slot)
        logger.debug(f"Musk count: {musk_count}")
        while memory.main.blitz_cursor() != 0:
            xbox.menu_up()
    nemesis.arena_select.arena_menu_select(4)
    
    memory.main.update_formation(Tidus, Yuna, Rikku, full_menu_close=False)
    menu.add_ability(
        owner=4,  # Wakka armor, Confuse-proof for Fenrir
        equipment_type=1,
        ability_array=[32882, 32778, 32816, 255],
        ability_index=32846,
        slot_count=4,
        navigate_to_equip_menu=True,
        exit_out_of_current_weapon=False,
        close_menu=True,
        full_menu_close=True,
    )


def battles_3():
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=13, monster_index=11)
    battle.main.auto_life(target=0)
    while not basic_quick_attacks(mega_phoenix=True,skip_throw=True):
        logger.debug("Battle not completed successfully.")
        restock_downs()
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=13, monster_index=11)
        battle.main.auto_life(target=0)
    game_vars.arena_success(array_num=0, index=11)
    nemesis.arena_select.arena_menu_select(4)
    restock_downs()
    menu.tidus_slayer(od_pos=0)

    check_yojimbo_possible()

    
    touch_save()
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=14, monster_index=2)
    aeon_start()
    battle.main.auto_life(target=0)
    while not basic_attack(use_od=False):
        logger.debug("Battle not completed successfully.")
        restock_downs()
        touch_save()
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=14, monster_index=2)
        battle.main.auto_life(target=0)
    game_vars.arena_success(array_num=1, index=2)
    nemesis.arena_select.arena_menu_select(4)
    restock_downs()

    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=14, monster_index=9)
    battle.main.auto_life(target=0)
    while not basic_quick_attacks(mega_phoenix=True, skip_throw=True):
        logger.debug("Battle not completed successfully.")
        restock_downs()
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=14, monster_index=9)
        battle.main.auto_life(target=0)
    game_vars.arena_success(array_num=1, index=9)
    nemesis.arena_select.arena_menu_select(4)
    restock_downs()

    check_yojimbo_possible()

    nemesis.arena_select.arena_menu_select(4)
    touch_save()
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=14, monster_index=10)
    battle.main.auto_life(target=0)
    while not basic_quick_attacks(mega_phoenix=True, skip_throw=True):
        logger.debug("Battle not completed successfully.")
        restock_downs()
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=14, monster_index=10)
        battle.main.auto_life(target=0)
    game_vars.arena_success(array_num=1, index=10)
    nemesis.arena_select.arena_menu_select(4)
    restock_downs()

    check_yojimbo_possible()


def battles_4():
    nemesis.arena_select.arena_menu_select(4)
    touch_save()
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=15, monster_index=0)
    battle.main.auto_life(target=0)
    while not basic_quick_attacks(mega_phoenix=True, skip_throw=True):
        logger.debug("Battle not completed successfully.")
        restock_downs()
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=15, monster_index=0)
        battle.main.auto_life(target=0)
    game_vars.arena_success(array_num=2, index=0)
    nemesis.arena_select.arena_menu_select(4)
    restock_downs()

    check_yojimbo_possible()
    touch_save()
    if Tidus.overdrive_percent() != 100:
        recharge_overdrives(check_weap=False)
    check_yojimbo_possible()

    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=15, monster_index=6)

    while not shinryu_battle():
        logger.debug("Battle not completed successfully.")
        nemesis.arena_select.arena_menu_select(4)
        restock_downs()
        touch_save()
        
        if Tidus.overdrive_percent() != 100:
            recharge_overdrives(check_weap=False)
        check_yojimbo_possible()
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=15, monster_index=6)

    game_vars.arena_success(array_num=2, index=6)
    nemesis.arena_select.arena_menu_select(4)
    restock_downs()


def item_dump():
    if not memory.main.diag_skip_possible():
        arena_npc()
    nemesis.arena_select.arena_menu_select(2)
    memory.main.wait_frames(90)
    xbox.menu_right()
    xbox.menu_b()
    menu.sell_all()
    while memory.main.menu_open():
        xbox.tap_back()


def quick_reset_logic():
    reset.reset_to_main_menu()
    area.dream_zan.new_game("Yojimbo")
    load_game.load_save_num(199)
    FFXC.set_neutral()
    game_vars.print_arena_status()


def check_yojimbo_possible():
    # update_stream()
    if Yuna.overdrive_percent() != 100:
        return False
    if first_turn_action_occurs():
        return False
    if zanmato_gil_needed() > 260000:
        return False
    if (
        memory.main.overdrive_state_2()[1] == 100
        and memory.main.get_gil_value() < 265000
    ):
        item_dump()
    armor_check()

    if (
        memory.main.overdrive_state_2()[1] == 100
        and memory.main.get_gil_value() >= 265000
    ):
        # Save game in preparation for the Yojimbo attempt
        memory.main.wait_frames(20)
        memory.main.update_formation(Tidus, Yuna, Rikku)

        # Now attempt to get Zanmato until successful, no re-saving.
        while not battles_5(game_vars.yojimbo_get_index()):
            quick_reset_logic()
        return True
    else:
        return False


def shinryu_battle():
    update_stream()
    rikku_first_turn = False
    rikku_drive_complete = False
    screen.await_turn()
    while memory.main.battle_active():
        if memory.main.turn_ready():
            '''
            if Rikku.is_turn():
                if not rikku_first_turn:
                    CurrentPlayer().defend()
                elif rikku_drive_complete:
                    battle.main._use_healing_item(item_id=9)
                else:
                    battle.main.rikku_full_od("shinryu")
                    rikku_drive_complete = True
            '''
            if Tidus.is_turn():
                '''
                if (
                    memory.main.who_goes_first_after_current_turn([0,20]) == 20
                    and not memory.main.state_battle.main.auto_life(target=0)
                ):
                    battle.main.auto_life(target=0)
                '''
                if screen.faint_check() >= 2:
                    battle.main.revive(item_num=7)
                elif memory.main.get_overdrive_battle(0) == 100:
                    Tidus.overdrive()
                else:
                    CurrentPlayer().attack()
            else:
                CurrentPlayer().defend()

    # After battle stuff
    while not memory.main.menu_open():
        xbox.tap_b()
    FFXC.set_confirm()
    memory.main.wait_frames(170)
    FFXC.set_neutral()
    memory.main.wait_frames(2)
    return memory.main.battle_arena_results()


def battles_5(completion_version: int):
    update_stream()
    logger.info(f"Yojimbo battle number: {completion_version}")
    if completion_version >= 12 and completion_version != 99:
        return True  # These battles are complete at this point.
    yojimbo_success = False

    if not zan_ready():
        recharge_overdrives(align_zan=True)
    memory.main.update_formation(Tidus, Lulu, Rikku)

    # Now for the Yojimbo section
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)

    # Battles here
    if completion_version == 5:
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

    elif completion_version == 1:
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
        if game_vars.arena_arrays()[1][4] != 1:
            nemesis.arena_select.start_fight(area_index=14, monster_index=4)
            if yojimbo_battle():
                game_vars.arena_success(array_num=1, index=4)
                yojimbo_success = True
        else:
            return True

    elif completion_version == 99:  # Nemesis
        nemesis.arena_select.start_fight(area_index=15, monster_index=7)
        if yojimbo_battle(diag_after=True):
            memory.main.click_to_diag_progress(2)
            memory.main.click_to_control_3()
            return True
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


def recharge_overdrives(align_zan:bool=False, check_weap = True):
    start = 'arena'
    yuna_weap = False
    if memory.main.get_map() == 374:
        start = 'airship'
        nemesis.arena_select.arena_return()

    while not zan_ready():
        if Yuna.overdrive_percent() != 100:
            logger.debug("Yuna is not charged. Recharging with tonberry.")
            write_big_text("Overdrive recharge logic")
            if check_weap and memory.main.equipped_weapon_has_ability(char_num=1, ability_num=0x8011):
                menu.equip_weapon(character=1)  # Sets back to default (I think)
                yuna_weap = True
            arena_npc()
            nemesis.arena_select.arena_menu_select(1)
            nemesis.arena_select.start_fight(area_index=13, monster_index=9)
            screen.await_turn()
            yuna_escape = False
            tidus_escape = False
            while memory.main.battle_active():
                if memory.main.turn_ready():
                    if not Yuna.active() and not yuna_escape:
                        battle.main.buddy_swap(Yuna)
                    elif Yuna.is_turn():
                        if Yuna.overdrive_percent() != 100:
                            Yuna.attack()
                        else:
                            battle.main.escape_one()
                            yuna_escape = True
                    elif not Tidus.active() and not tidus_escape:
                        battle.main.buddy_swap(Tidus)
                    elif Tidus.is_turn():
                        if (
                            Tidus.overdrive_percent() == 100 and
                            Yuna.overdrive_percent() == 100
                        ):
                            Tidus.flee()
                        elif Tidus.overdrive_percent() != 100:
                            Tidus.attack()
                        else:
                            Tidus.defend()
                            # battle.main.escape_one()
                            # tidus_escape = True
                    else:
                        battle.main.escape_one()

            logger.debug("Battle is complete.")
            nemesis.arena_select.arena_menu_select(4)
            memory.main.wait_frames(2)
            if yuna_weap:
                menu.equip_weapon(character=1, ability=0x8011, full_menu_close=True)
        elif align_zan and not zan_ready():
            logger.debug("Yojimbo is not aligned.")
            write_big_text("Yojimbo RNG manip battle")
            touch_save()
            memory.main.update_formation(Tidus, Lulu, Rikku)
            restock_downs()
            arena_npc()
            nemesis.arena_select.arena_menu_select(1)
            nemesis.arena_select.start_fight(area_index=1, monster_index=1)
            screen.await_turn()
            # summon_complete = not game_vars.yojimbo_unlocked()
            summon_complete = False
            while memory.main.battle_active():
                if memory.main.turn_ready():
                    if Yojimbo.is_turn():
                        summon_complete=True
                        Yojimbo.pay(gil_value=1)
                    elif not Yuna.active():
                        battle.main.buddy_swap(Yuna)
                        battle.main.aeon_summon(6)
                        summon_complete=True
                    elif Yuna.is_turn():
                        if not summon_complete:
                            battle.main.aeon_summon(6)
                            summon_complete=True
                        else:
                            battle.main.flee_all()
                    elif summon_complete:
                        battle.main.flee_all()
                    else:
                        CurrentPlayer().defend()
            nemesis.arena_select.arena_menu_select(4)
            memory.main.wait_frames(2)
        else:
            if start == 'airship':
                return_to_airship()
            else:
                touch_save()
            return
    if start == 'airship':
        return_to_airship()
    else:
        touch_save()

def recharge_overdrives_overworld():
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if not Yuna.active():
                battle.main.buddy_swap(Yuna)
            elif Yuna.is_turn() and Yuna.overdrive_percent() != 100:
                CurrentPlayer().attack()
            elif not Tidus.active():
                battle.main.buddy_swap(Tidus)
            elif (
                Tidus.is_turn() and
                Tidus.overdrive_percent() == 100 and
                Yuna.overdrive_percent() == 100
            ):
                battle.main.flee_all()
            elif Tidus.is_turn() and Tidus.overdrive_percent() != 100:
                CurrentPlayer().attack()
            else:
                battle.main.escape_one()


def yojimbo_advance_battle():
    # Advances Yojimbo's RNG.
    aeon_id = 5
    if game_vars.platinum():
        aeon_id = 6
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Yuna.is_turn():
                battle.main.aeon_summon(aeon_id)
            elif screen.turn_aeon():
                Yojimbo.pay(gil_value=1)
            elif not Yuna.active():
                battle.main.buddy_swap(Yuna)
            else:
                CurrentPlayer().defend()
    battle.main.wrap_up()



def nemesis_battle():
    if memory.main.get_map() == 374:
        logger.info("Returning to the arena.")
        nemesis.arena_select.arena_return()
    update_stream()
    if game_vars.yojimbo_get_index() < 12:
        nemesis.arena_select.arena_menu_select(4)
        touch_save()
        while game_vars.yojimbo_get_index() < 12:
            logger.debug(f"Previous bosses not clear. {game_vars.yojimbo_get_index()}")
            # If Yuna is charged, do next battle. Otherwise charge.
            if zan_ready():
                battles_5(game_vars.yojimbo_get_index())
                nemesis.arena_select.arena_menu_select(4)
            else:
                recharge_overdrives(check_weap=False, align_zan=True)
    logger.debug("Bosses have now been clear, Nemesis unlocked.")
    # if Yuna.overdrive_percent() != 100:
    while not zan_ready():
        recharge_overdrives(check_weap=False, align_zan=True)
        # arena_npc()
        # logger.debug("Advance Yojimbo RNG")
        # nemesis.arena_select.arena_menu_select(1)
        # nemesis.arena_select.start_fight(area_index=0, monster_index=0)
        # yojimbo_advance_battle()
        # nemesis.arena_select.arena_menu_select(4)
        # touch_save()
    
    logger.debug("Yojimbo RNG aligned.")
    memory.main.update_formation(Tidus, Yuna, Rikku)
    touch_save()
    logger.debug("Yojimbo battle START!!!  (Anime music here)")
    battles_5(completion_version=99)
    logger.debug("Yojimbo battle end!")
    # while not battles_5(completion_version=99):
    #     nemesis.arena_select.arena_menu_select(4)
    #     quick_reset_logic()
    # xbox.controller_handle()
    while not pathing.set_movement([-6, -27]):
        pass
    while not pathing.set_movement([-2, -2]):
        pass
    if game_vars.platinum():
        menu.equip_weapon(character=1, ability=0x8011, full_menu_close=True)  # OD to AP
    else:
        return_to_airship()
    
    write_big_text("")


def return_to_sin():
    airship_destination(dest_num=0)
    memory.main.await_control()
    menu.equip_weapon(character=0, ability=0x8001, full_menu_close=True)
    FFXC.set_movement(0, -1)
    memory.main.wait_frames(2)

def armor_check():
    if not memory.main.equipped_armor_has_ability(char_num=0, ability_num=0x8056):
        # Auto-haste for Tidus
        menu.equip_armor(character=1, ability=0x8056, full_menu_close=False)
    if not memory.main.equipped_armor_has_ability(char_num=1, ability_num=0x800A):
        # Auto-phoenix for Yuna
        menu.equip_armor(character=1, ability=0x800A, full_menu_close=False)
    if not memory.main.equipped_armor_has_ability(char_num=4, ability_num=0x800A):
        # Auto-phoenix for Wakka
        menu.equip_armor(character=4, ability=0x800A)