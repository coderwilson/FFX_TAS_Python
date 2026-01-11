import logging

import memory.main
from memory.main import get_menu_cursor_pos, get_menu_2_char_num
from memory.unlocks import od_mode_unlocks, od_mode_pos, od_mode_current
import vars
import xbox
import battle.main
import pathing
from json_ai_files.write_seed import write_big_text
from paths.nem import ArenaReturn
import menu
from gamestate import game
import save_sphere
from players import Rikku, Tidus, Wakka

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def arena_return(checkpoint: int = 0, godhand:int = 0, baaj:int = 0):
    logger.info(f"Returning to arena: {checkpoint} | {godhand} | {baaj}")
    if checkpoint == 0:
        # logger.info(f"Airship destination: {12+godhand+baaj}")
        # air_ship_destination(dest_num=12+godhand+baaj)
        navigate_to_airship_destination("Calm Lands")

    logger.info (f"Now at calm lands.")
    while memory.main.get_map() != 307:
        if memory.main.user_control():
            if checkpoint == 2:
                while memory.main.user_control():
                    pathing.set_movement([-641, -268])
                    xbox.tap_b()
                FFXC.set_neutral()
                checkpoint += 1
            elif pathing.set_movement(ArenaReturn.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()

# Default to Besaid. Maybe based on map number?
def air_ship_destination(dest_num=0, force_omega=False):
    logger.warning(f"OLD AIRSHIP FUNCTION, FIX THIS!!!")
    logger.warning(f"OLD AIRSHIP FUNCTION, FIX THIS!!!")
    logger.warning(f"OLD AIRSHIP FUNCTION, FIX THIS!!!")
    if len(memory.main.all_equipment()) > 120:
        rin_equip_dump()
    while memory.main.get_coords()[0] < -257:
        pathing.set_movement([-258, 345])
    while memory.main.get_map() not in [382, 999]:
        if memory.main.user_control():
            pathing.approach_actor_by_id(actor_id=8449)
        else:
            FFXC.set_neutral()
        xbox.menu_b()
    # while memory.main.diag_progress_flag() != 1:
    #     xbox.tap_b()
    while not memory.main.diag_progress_flag() in [4,5]:
        logger.debug(f"Attempting to open destination list. {memory.main.diag_progress_flag()}")
        xbox.tap_b()
    logger.debug("Destination select on screen now.")
    while memory.main.map_cursor() != dest_num:
        if dest_num < 8:
            xbox.tap_down()
        else:
            xbox.tap_up()
    memory.main.wait_frames(2)
    xbox.menu_b()
    memory.main.wait_frames(2)
    xbox.tap_b()
    while not memory.main.user_control():
        if memory.main.cutscene_skip_possible():
            xbox.skip_scene()
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
    if game_vars.platinum():
        od_check()
    logger.warning(f"OLD AIRSHIP FUNCTION, FIX THIS!!!")
    logger.warning(f"OLD AIRSHIP FUNCTION, FIX THIS!!!")
    logger.warning(f"OLD AIRSHIP FUNCTION, FIX THIS!!!")


AIRSHIP_DESTINATIONS_DATA = [
    {"name": "Penance", "full_list_position": 0, "map_id": 322, "default_unlocked": False},
    {"name": "Sin", "full_list_position": 1, "map_id": 322, "default_unlocked": True},
    {"name": "Baaj", "full_list_position": 2, "map_id": 49, "default_unlocked": False},
    {"name": "Besaid", "full_list_position": 3, "map_id": 19, "default_unlocked": True},
    {"name": "Besaid Ruins 1", "full_list_position": 4, "map_id": 21, "default_unlocked": False},
    {"name": "Besaid Ruins 2", "full_list_position": 5, "map_id": 21, "default_unlocked": False},
    {"name": "Besaid Falls", "full_list_position": 6, "map_id": 22, "default_unlocked": False},
    {"name": "Kilika", "full_list_position": 7, "map_id": 98, "default_unlocked": True},
    {"name": "Luca", "full_list_position": 8, "map_id": 123, "default_unlocked": True},
    {"name": "Mi'ihen Highroad", "full_list_position": 9, "map_id": 171, "default_unlocked": True},
    {"name": "Mi'ihen Ruins", "full_list_position": 10, "map_id": 58, "default_unlocked": False},
    {"name": "Mushroom Rock", "full_list_position": 11, "map_id": 92, "default_unlocked": False},
    {"name": "Battle_Site", "full_list_position": 12, "map_id": 254, "default_unlocked": False},
    {"name": "Djose", "full_list_position": 13, "map_id": 131, "default_unlocked": True},
    {"name": "Moonflow", "full_list_position": 14, "map_id": 235, "default_unlocked": True},
    {"name": "Guadosalam", "full_list_position": 15, "map_id": 243, "default_unlocked": True},
    {"name": "Thunder Plains", "full_list_position": 16, "map_id": 263, "default_unlocked": True},
    {"name": "Macalania", "full_list_position": 17, "map_id": 215, "default_unlocked": True},
    {"name": "Bikanel", "full_list_position": 18, "map_id": 129, "default_unlocked": True},
    {"name": "Sanubia", "full_list_position": 19, "map_id": 137, "default_unlocked": False},
    {"name": "Highbridge", "full_list_position": 20, "map_id": 208, "default_unlocked": True},
    {"name": "Calm Lands", "full_list_position": 21, "map_id": 223, "default_unlocked": True},
    {"name": "Omega", "full_list_position": 22, "map_id": 258, "default_unlocked": False},
    {"name": "Gagazet", "full_list_position": 23, "map_id": 259, "default_unlocked": True},
    {"name": "Zanarkand", "full_list_position": 24, "map_id": 313, "default_unlocked": True}
]
unlocked_airship_locations = set()

def add_airship_unlocked_location(loc:str):
    unlocked_airship_locations.add(loc)

def remove_airship_unlocked_location(loc: str):
    """Removes a previously unlocked airship destination from the set."""
    unlocked_airship_locations.discard(loc)

def _get_current_airship_menu_list():
    """Generates the list of currently available airship destinations in menu order."""
    current_list = []
    for dest_data in AIRSHIP_DESTINATIONS_DATA:
        if dest_data["default_unlocked"] or dest_data["name"] in unlocked_airship_locations:
            current_list.append(dest_data)
    current_list.sort(key=lambda x: x["full_list_position"])
    return current_list

def _perform_airship_navigation_steps(dest_num, target_map_id):
    """Handles the actual in-game navigation steps to select a destination."""
    logger.debug(f"Attempting to navigate to destination index: {dest_num}")

    if len(memory.main.all_equipment()) > 120:
        logger.info(f"Equipment count high, performing Rin equipment dump. {len(memory.main.all_equipment())}")
        rin_equip_dump()

    while memory.main.get_map() not in [382, 999]:
        logger.debug(f"Current map: {memory.main.get_map()}. Not on airship, attempting to get there.")
        if memory.main.user_control():
            pathing.approach_actor_by_id(actor_id=8449)
        else:
            FFXC.set_neutral()
            xbox.menu_b()

    # Wait for the destination select screen to appear.
    # while memory.main.diag_progress_flag() != 1:
    #     logger.debug(f"Attempting to start airship logic. {memory.main.diag_progress_flag()}")
    #     xbox.tap_b()
    while not memory.main.diag_progress_flag() in [4,5]:
        logger.debug(f"Attempting to open destination list. {memory.main.diag_progress_flag()}")
        xbox.tap_b()

    logger.debug("Destination select on screen now. Selecting destination.")

    # Reset cursor to 0 for consistent navigation.
    while memory.main.map_cursor() != 0:
        xbox.tap_up()
        memory.main.wait_frames(1)

    logger.debug(f"Cursor reset to 0. Now moving to target: {dest_num}")
    while memory.main.map_cursor() != dest_num:
        while memory.main.map_cursor() != dest_num:
            if dest_num < 8:
                xbox.tap_down()
            else:
                xbox.tap_up()
        memory.main.wait_frames(1)

    memory.main.wait_frames(2)
    xbox.menu_b()
    memory.main.wait_frames(2)
    xbox.tap_b()

    # Wait until user regains control.
    logger.debug("Waiting for user control after departure.")
    while not memory.main.user_control():
        if memory.main.cutscene_skip_possible():
            xbox.skip_scene()
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
        elif memory.main.battle_active() and memory.main.get_encounter_id() == 247:
            logger.debug(f"Nemesis Battle has started! Returning!!!")
            return True
        memory.main.wait_frames(1)

    logger.debug("User control regained. Validating arrival.")

    # Validate arrival at the correct map.
    current_map = memory.main.get_map()
    if current_map == target_map_id:
        logger.info(f"Successfully arrived at {current_map} (Expected: {target_map_id}).")
        if game_vars.platinum():
            od_check()
        return True
    else:
        logger.error(f"Arrived at incorrect map ID: {current_map}. Expected: {target_map_id}.")
        return False

def navigate_to_airship_destination(destination_name: str, max_retries: int = 2):
    """
    Navigates the airship to a specified destination by name, handling retries.
    """
    logger.info(f"Attempting to navigate to: {destination_name}")

    target_dest_data = next((d for d in AIRSHIP_DESTINATIONS_DATA if d["name"] == destination_name), None)
    if not target_dest_data:
        logger.error(f"Destination '{destination_name}' not found in AIRSHIP_DESTINATIONS_DATA.")
        return False

    target_map_id = target_dest_data["map_id"]

    for attempt in range(max_retries * 2):
        if attempt > 0:
            logger.warning(f"Navigation failed. Retrying (Attempt {attempt}/{max_retries})...")
            return_to_airship()

        current_airship_menu = _get_current_airship_menu_list()
        logger.debug(f"Current airship menu: {[d['name'] for d in current_airship_menu]}")

        try:
            dest_num = next(i for i, d in enumerate(current_airship_menu) if d["name"] == destination_name)
            if attempt < max_retries:
                dest_num = min(dest_num+attempt,len(current_airship_menu))
            else:
                dest_num = max(dest_num-attempt,0)
            logger.debug(f"'{destination_name}' found at dynamic index {dest_num}.")
        except StopIteration:
            logger.error(f"Destination '{destination_name}' is not currently available in the airship menu.")
            return False

        if _perform_airship_navigation_steps(dest_num, target_map_id):
            logger.info(f"Successfully navigated to '{destination_name}'.")
            return True
        else:
            logger.error(f"Failed to arrive at '{destination_name}' after navigation steps.")

    logger.error(f"Failed to navigate to '{destination_name}' after {max_retries} retries.")
    return False

def rin_equip_dump(
    buy_weapon:bool=False, 
    sell_nea:bool=False, 
    stock_downs:bool=False, 
    stock_distillers:bool=False,
    b_squad:bool=False,
    cap:bool=False
):
    write_big_text("Dumping extra equipments")
    if game_vars.nemesis():
        stock_downs = False
    if memory.main.get_map() != 374:
        return_to_airship()
    while not pathing.set_movement([-242, 298]):
        pass
    while not pathing.set_movement([-243, 160]):
        pass
    FFXC.set_movement(0, -1)
    while memory.main.user_control():
        pass
    while not pathing.set_movement([39, 53]):
        pass
    menu.auto_sort_equipment()
    pathing.approach_actor_by_id(actor_id=8426)
    FFXC.set_neutral()
    memory.main.click_to_diag_progress(48)
    memory.main.wait_frames(20)
    xbox.menu_b()
    memory.main.wait_frames(36)
    xbox.menu_right()
    xbox.menu_b()

    logger.debug("Now activating sell-all logic")
    menu.sell_all(nea=sell_nea,capture=cap)
    logger.debug("Sell all complete.")
    memory.main.close_menu()
    write_big_text("")
    memory.main.click_to_control_dumb()
    if buy_weapon:
        # Stock with 99 downs.
        logger.debug("Buying weapon")
        pathing.approach_actor_by_id(actor_id=8426)
        FFXC.set_neutral()
        memory.main.click_to_diag_progress(48)
        while not memory.main.airship_shop_dialogue_row() == 2:
            xbox.tap_up()
        while not memory.main.airship_shop_dialogue_row() == 0:
            while not memory.main.airship_shop_dialogue_row() == 0:
                xbox.tap_down()
        xbox.menu_b()  # Got any weapons?
        memory.main.wait_frames(60)
        xbox.menu_b()  # Select weapons.
        while memory.main.equip_buy_row() != 6:
            while memory.main.equip_buy_row() != 6:
                if memory.main.equip_buy_row() > 6:
                    xbox.tap_up()
                else:
                    xbox.tap_down()
            memory.main.wait_frames(1)
        xbox.menu_b()
        memory.main.wait_frames(60)
        xbox.menu_up()
        memory.main.wait_frames(60)
        xbox.menu_b()
        memory.main.wait_frames(60)
        xbox.menu_up()
        memory.main.wait_frames(60)
        xbox.menu_b()
        memory.main.wait_frames(60)
    elif stock_downs:
        # Stock with 99 downs.
        logger.debug("Stocking phoenix downs")
        pathing.approach_actor_by_id(actor_id=8426)
        FFXC.set_neutral()
        memory.main.click_to_diag_progress(48)
        while not memory.main.airship_shop_dialogue_row() == 0:
            pass
        while not memory.main.airship_shop_dialogue_row() == 1:
            xbox.tap_down()
        memory.main.wait_frames(3)
        xbox.tap_b()
        memory.main.wait_frames(120)
        xbox.tap_b()
        while memory.main.equip_buy_row() != 4:
            if memory.main.equip_buy_row() > 4:
                xbox.tap_up()
            else:
                xbox.tap_down()
        memory.main.wait_frames(2)
        xbox.tap_b()
        memory.main.wait_frames(2)
        for i in range(9):
            xbox.tap_up()
        xbox.tap_b()
    elif stock_distillers:
        logger.debug("Stocking distillers")
        pathing.approach_actor_by_id(actor_id=8426)
        FFXC.set_neutral()
        memory.main.click_to_diag_progress(48)
        while not memory.main.airship_shop_dialogue_row() == 0:
            pass
        while not memory.main.airship_shop_dialogue_row() == 1:
            xbox.tap_down()
        memory.main.wait_frames(3)
        xbox.tap_b()
        memory.main.wait_frames(120)
        xbox.tap_b()
        for i in range(4):
            loop_break = 0
            while memory.main.equip_buy_row() != 10+i:
                while memory.main.equip_buy_row() != 10+i:
                    if memory.main.equip_buy_row() > 10+i:
                        xbox.tap_up()
                    else:
                        xbox.tap_down()
                memory.main.wait_frames(1)
            
            memory.main.wait_frames(20)
            xbox.menu_b()
            memory.main.wait_frames(6)
            for i in range(3):
                xbox.tap_up()
            xbox.menu_b()
            memory.main.wait_frames(6)
            loop_break += 1
            if loop_break % 10 == 0:
                xbox.tap_right()
            memory.main.wait_frames(2)
            distiller_index = memory.main.get_item_slot(16+i)
            if distiller_index == 255:
                distiller_count = 0
            else:
                distiller_count = memory.main.get_item_count_slot(distiller_index)
            xbox.tap_confirm()
            memory.main.wait_frames(2)
            while distiller_count < 40:
                if 40 - distiller_count > 10:
                    xbox.tap_up()
                    distiller_count += 10
                else:
                    xbox.tap_right()
                    distiller_count += 1
            xbox.tap_confirm()
    elif b_squad:
        # Stock with 99 downs.
        logger.debug("B_squad logic")
        pathing.approach_actor_by_id(actor_id=8426)
        FFXC.set_neutral()
        memory.main.click_to_diag_progress(48)
        while not memory.main.airship_shop_dialogue_row() == 2:
            xbox.tap_up()
        while not memory.main.airship_shop_dialogue_row() == 0:
            while not memory.main.airship_shop_dialogue_row() == 0:
                xbox.tap_down()
        xbox.menu_b()  # Got any weapons?
        memory.main.wait_frames(60)
        xbox.menu_b()  # Purchase equipment
        if not game_vars.plat_triple_ap_check()[5]:
            # Lulu weapon, only if not obtained earlier.
            while memory.main.equip_buy_row() != 3:
                while memory.main.equip_buy_row() != 3:
                    if memory.main.equip_buy_row() > 3:
                        xbox.tap_up()
                    else:
                        xbox.tap_down()
                memory.main.wait_frames(1)
            xbox.menu_b()
            memory.main.wait_frames(60)
            xbox.menu_up()
            memory.main.wait_frames(60)
            xbox.menu_b()
            memory.main.wait_frames(60)
            xbox.menu_up()
            memory.main.wait_frames(60)
            xbox.menu_b()
            memory.main.wait_frames(60)

        while memory.main.equip_buy_row() != 10:
            # Lulu armor
            while memory.main.equip_buy_row() != 10:
                if memory.main.equip_buy_row() > 10:
                    xbox.tap_up()
                else:
                    xbox.tap_down()
            memory.main.wait_frames(1)
        memory.main.wait_frames(60)
        xbox.menu_b()
        memory.main.wait_frames(60)
        xbox.menu_up()
        memory.main.wait_frames(60)
        xbox.menu_b()
        memory.main.wait_frames(60)
        xbox.menu_up()
        memory.main.wait_frames(60)
        xbox.menu_b()
        memory.main.wait_frames(60)


    write_big_text("")
    memory.main.close_menu()
    memory.main.click_to_control_dumb()
    

    menu.auto_sort_equipment()
    while not pathing.set_movement([53, 110]):
        pass
    FFXC.set_movement(-1, -1)
    while memory.main.user_control():
        pass
    while not pathing.set_movement([-241, 223]):
        pass
    while not pathing.set_movement([-246, 329]):
        pass


def arena_npc():
    if memory.main.get_map() in [194,374]:
        arena_return()
    while not memory.main.user_control():
        if memory.main.diag_progress_flag() == 74 and memory.main.diag_skip_possible():
            return
        elif memory.main.menu_open():
            xbox.menu_a()
    if memory.main.get_map() != 307:
        return
    while not (
        memory.main.diag_progress_flag() == 74 and memory.main.diag_skip_possible()
    ):
        if memory.main.user_control():
            if memory.main.get_coords()[1] > -12 and memory.main.get_actor_angle(0) > -1:
                xbox.menu_down()
                memory.main.wait_frames(12)
            elif memory.main.get_coords()[1] < -22:
                pathing.set_movement([5,-19])
            else:
                pathing.approach_actor_by_id(actor_id=8241)
        else:
            FFXC.set_neutral()
            if memory.main.diag_progress_flag() == 59:
                xbox.menu_a()
                xbox.menu_a()
                xbox.menu_a()
                xbox.tap_b()
            elif memory.main.diag_skip_possible():
                xbox.tap_b()
    memory.main.wait_frames(3)  # This buffer can be improved later.


def area_array():
    # Not working properly
    return [
        60112,
        60736,
        61672,
        62296,
        62920,
        63544,
        58240,
        58552,
        59176,
        59488,
        59800,
        60424,
        61360,
        61984,
        62608,
        63232,
    ]


def area_index_check(index_num: int = 15):
    # Not working properly
    #logger.debug(memory.main.arena_cursor())
    if memory.main.arena_array[index_num] == memory.main.arena_cursor():
        return True
    return False


def arena_cursor():
    # Not working properly
    for x in range(16):
        logger.debug(memory.main.arena_cursor())
        if memory.main.arena_cursor() == area_array()[x]:
            return x
    return 255


def arena_menu_select(choice: int = 2):
    logger.debug(f"Selecting menu option: {choice}")
    if game_vars.use_pause():
        memory.main.wait_frames(2)
    if choice == 4:
        while not memory.main.user_control():
            if memory.main.battle_wrap_up_active():
                xbox.tap_confirm()
            elif memory.main.diag_skip_possible():
                if memory.main.blitz_cursor() != 4 or memory.main.menu_open():
                    xbox.tap_back()
                else:
                    xbox.tap_confirm()
            else:
                # I don't know, something goes here I guess.
                pass
                #logger.warning("Attempting to select option 4 - Unidentified state. Standing by.")
    else:
        if memory.main.user_control():
            arena_npc()
        elif memory.main.diag_skip_possible():
            while not memory.main.blitz_cursor() == choice:
                while not memory.main.blitz_cursor() == choice:
                    if memory.main.battle_wrap_up_active():
                        battle.main.wrap_up()
                    elif choice == 3:
                        xbox.menu_up()
                    else:
                        xbox.menu_down()
                    memory.main.wait_frames(1)
                    if game_vars.use_pause():
                        memory.main.wait_frames(2)
                memory.main.wait_frames(2)
        xbox.menu_b()
        memory.main.wait_frames(3)


def get_arena_cursor():
    cursor_loaded = False
    while not cursor_loaded:
        try:
            cursor1 = memory.main.arena_cursor_1()
            cursor2 = (memory.main.arena_cursor_2() - 89)
            logger.debug(cursor2)
            #memory.main.wait_frames(30)
            cursor_loaded = True
        except:
            pass
    
    cursor_position = (cursor2 / 33) * 2
    if cursor1 == 318:
        cursor_position += 1
    return cursor_position
    


def start_fight(area_index: int, monster_index: int = 0):
    while not (memory.main.menu_open() and memory.main.diag_progress_flag() == 74):
        if memory.main.battle_active():
            battle.main.flee_all()
        elif memory.main.diag_progress_flag() == 74:
            if memory.main.diag_skip_possible():
                arena_menu_select(1)
            elif memory.main.user_control():
                arena_npc()
        else:
            if memory.main.diag_skip_possible():
                xbox.tap_confirm()
            elif memory.main.user_control():
                arena_npc()

    logger.debug(f"Starting fight: {area_index} | {monster_index}")
    arenaCursor = get_arena_cursor()
    #memory.main.wait_frames(60)
    while arenaCursor != area_index:
        while arenaCursor != area_index:
            arenaCursor = get_arena_cursor()
            if arenaCursor % 2 == 0 and area_index % 2 == 1:
                xbox.tap_right()
            elif arenaCursor % 2 == 1 and area_index % 2 == 0:
                xbox.tap_left()
            elif arenaCursor < area_index:
                xbox.tap_down()
            elif arenaCursor > area_index:
                xbox.tap_up()
        arenaCursor = get_arena_cursor()
        memory.main.wait_frames(2)
    xbox.menu_b()
    memory.main.wait_frames(6)
    # Do we need to find cursors for these as well?
    if monster_index >= 7:
        xbox.menu_right()
        monster_index -= 7
    while monster_index != memory.main.arena_cursor_3():
        while monster_index != memory.main.arena_cursor_3():
            xbox.tap_down()
            # monster_index -= 1
        memory.main.wait_frames(2)
    xbox.tap_b()
    memory.main.wait_frames(6)
    xbox.tap_b()
    while not memory.main.battle_active():
        pass



def return_to_airship(extra_save=False):
    logger.debug("Attempting Return to Airship")
    while not memory.main.user_control():
        pass
    while memory.main.menu_open():
        xbox.menu_a()

    memory.main.get_save_sphere_details()
    
    if memory.main.get_map() in [194,374]:
        logger.warning("Exit return_to_airship function, we are already there.")
        return
    
    logger.warning("Mark A")
    if memory.main.get_map() == 307:  # Monster arena
        logger.warning("Monster Arena variant")
        if memory.main.get_coords()[1] < -10:
            while not pathing.set_movement([-6, -12]):
                if memory.main.get_map() in [194,374]:
                    logger.warning("Exit return_to_airship function, loop 1")
                    return
        elif memory.main.get_coords()[1] > -12 and memory.main.get_actor_angle(0) < -1:
            xbox.menu_up()
            memory.main.wait_frames(12)

    logger.warning("Mark B")
    if not save_sphere.approach_save_sphere():
        logger.warning("Mark E (for error) - Could not reach save sphere")
        FFXC.set_neutral()
        memory.main.wait_frames(9)
        return_to_airship()
        return
    logger.warning("Mark C")
    FFXC.set_neutral()
    while memory.main.save_menu_cursor() != 1:
        xbox.menu_down()
        memory.main.wait_frames(1)
        if memory.main.get_map() in [194,374]:
            logger.warning("Exit return_to_airship function, loop 2")
            return
    xbox.menu_b()
    xbox.menu_b()
    xbox.menu_b()
    logger.warning("Mark D")
    memory.main.await_control()
    logger.info("Return to Airship Complete.")
    memory.main.clear_save_menu_cursor()
    memory.main.clear_save_menu_cursor_2()
    nea_recheck()

    
def nea_recheck():
    memory.main.check_nea_armor()
    if not memory.main.equipped_armor_has_ability(char_num=game_vars.ne_armor()):
        menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)

def od_check(preferred_mode:int=999):
    # od_mode_unlocks, od_mode_pos, od_mode_current
    if game.state == "Platinum" and game.step >= 6:
        return
    for character in [4,6]:
        current_mode = od_mode_current(character)
        unlocked_modes = od_mode_unlocks(character)
        if preferred_mode != 999:
            if current_mode != preferred_mode:
                if unlocked_modes[preferred_mode] == 1:
                    od_change(character=character, set_od_mode=preferred_mode)
        elif unlocked_modes[11] == 1:
            if current_mode != 11:
                # Most preferable is victor mode.
                od_change(character=character, set_od_mode=11)
        elif unlocked_modes[13] == 1:
            if current_mode != 13:
                # Second, Ally mode (charges on turn start)
                od_change(character=character, set_od_mode=13)
        elif unlocked_modes[2] == 1:
            if current_mode != 2:
                # Comrade better than Stoic
                od_change(character=character, set_od_mode=2)
        elif unlocked_modes[12] == 1:
            if current_mode != 12:
                # Coward slightly better than Stoic
                od_change(character=character, set_od_mode=12)



def od_change(character:int, set_od_mode:int, full_menu_close:bool=True):
    memory.main.open_menu()
    while get_menu_cursor_pos() != 3:
        while get_menu_cursor_pos() != 3:
            logger.debug(f"Menu cursor position: {get_menu_cursor_pos()}")
            xbox.tap_down()
        memory.main.wait_frames(1)
    xbox.menu_b()
    while get_menu_2_char_num() != character:
        while get_menu_2_char_num() != character:
            logger.debug(f"Menu cursor position 2: {get_menu_2_char_num()}")
            xbox.tap_down()
        memory.main.wait_frames(3)
    xbox.menu_b()
    memory.main.wait_frames(10)
    xbox.menu_a()
    memory.main.wait_frames(6)
    xbox.menu_right()
    memory.main.wait_frames(6)
    xbox.menu_b()
    memory.main.wait_frames(6)

    target = od_mode_pos(char_index=character, od_mode_id=set_od_mode)
    while memory.main.item_heal_character_cursor() != target:
        while memory.main.item_heal_character_cursor() != target:
            if target % 2 == 0 and memory.main.item_heal_character_cursor() % 2 == 1:
                xbox.tap_left()
            elif target % 2 == 1 and memory.main.item_heal_character_cursor() % 2 == 0:
                xbox.tap_right()
            elif target > memory.main.item_heal_character_cursor():
                xbox.tap_down()
            else:
                xbox.tap_up()
        memory.main.wait_frames(3)
    xbox.menu_b()
    
    if full_menu_close:
        memory.main.close_menu()
    else:
        memory.main.back_to_main_menu()
    
def od_check_2():
    # od_mode_unlocks, od_mode_pos, od_mode_current
    # for character in [1,2,3,5]:
    for character in [0,1,2,3,4,5,6]:
        current_mode = od_mode_current(character)
        unlocked_modes = od_mode_unlocks(character)
        if unlocked_modes[2] == 1:
            if current_mode != 2:
                # Comrade better than Stoic
                od_change(character=character, set_od_mode=2)
    
def distill_spheres():
    power = memory.main.get_item_count_slot(memory.main.get_item_slot(16))
    mana = memory.main.get_item_count_slot(memory.main.get_item_slot(17))
    speed = memory.main.get_item_count_slot(memory.main.get_item_slot(18))
    ability = memory.main.get_item_count_slot(memory.main.get_item_slot(19))
    
    if not memory.main.equipped_armor_has_ability(char_num=0, ability_num=0x800A):
        logger.debug("Spheres: armor for Tidus")
        menu.equip_armor(character=0, ability=0x800A, full_menu_close=False)
    if not memory.main.equipped_armor_has_ability(char_num=4, ability_num=0x800A):
        logger.debug("Spheres: armor for Wakka")
        menu.equip_armor(character=4, ability=0x800A, full_menu_close=False)
    menu.equip_weapon(character=0, ability=0x800F,full_menu_close=False)
    memory.main.update_formation(Tidus, Wakka, Rikku)
    if memory.main.get_gil_value() < 10000:
        item_dump()
    else:
        arena_npc()
    if power < 5 or mana < 5 or speed < 5 or ability < 5:
        arena_menu_select(3)
        memory.main.wait_frames(60)
        xbox.tap_b()
        memory.main.wait_frames(6)
        if power < 5:
            while memory.main.equip_buy_row() != 8:
                while memory.main.equip_buy_row() != 8:
                    if memory.main.equip_buy_row() < 8:
                        xbox.tap_down()
                    else:
                        xbox.tap_up()
                memory.main.wait_frames(3)
            memory.main.wait_frames(6)
            xbox.menu_b()
            memory.main.wait_frames(6)
            xbox.menu_up()
            memory.main.wait_frames(6)
            xbox.menu_b()
            memory.main.wait_frames(6)
        if mana < 5:
            while memory.main.equip_buy_row() != 9:
                while memory.main.equip_buy_row() != 9:
                    if memory.main.equip_buy_row() < 9:
                        xbox.tap_down()
                    else:
                        xbox.tap_up()
                memory.main.wait_frames(3)
            memory.main.wait_frames(6)
            xbox.menu_b()
            memory.main.wait_frames(6)
            xbox.menu_up()
            memory.main.wait_frames(6)
            xbox.menu_b()
            memory.main.wait_frames(6)
        if speed < 5:
            while memory.main.equip_buy_row() != 10:
                while memory.main.equip_buy_row() != 10:
                    if memory.main.equip_buy_row() < 10:
                        xbox.tap_down()
                    else:
                        xbox.tap_up()
                memory.main.wait_frames(3)
            memory.main.wait_frames(6)
            xbox.menu_b()
            memory.main.wait_frames(6)
            xbox.menu_up()
            memory.main.wait_frames(6)
            xbox.menu_b()
            memory.main.wait_frames(6)
        if ability < 5:
            while memory.main.equip_buy_row() != 11:
                while memory.main.equip_buy_row() != 11:
                    if memory.main.equip_buy_row() < 11:
                        xbox.tap_down()
                    else:
                        xbox.tap_up()
                memory.main.wait_frames(3)
            memory.main.wait_frames(6)
            xbox.menu_b()
            memory.main.wait_frames(6)
            xbox.menu_up()
            memory.main.wait_frames(6)
            xbox.menu_b()
            memory.main.wait_frames(6)
        xbox.menu_a()
        xbox.menu_a()
        xbox.menu_a()
        xbox.menu_a()
        
    power_count = memory.main.get_item_count_slot(memory.main.get_item_slot(70))
    mana_count = memory.main.get_item_count_slot(memory.main.get_item_slot(71))
    speed_count = memory.main.get_item_count_slot(memory.main.get_item_slot(72))
    ability_count = memory.main.get_item_count_slot(memory.main.get_item_slot(73))
    throw_item = 16
    while (
        power_count < 80 or
        mana_count < 80 or
        speed_count < 80 or
        ability_count < 80 or
        throw_item == 255
    ):
        throw_item = 255
        if power_count < 80 and memory.main.get_item_slot(16) != 255:
            throw_item = 16
        elif mana_count < 80 and memory.main.get_item_slot(17) != 255:
            throw_item = 17
        elif speed_count < 80 and memory.main.get_item_slot(18) != 255:
            throw_item = 18
        elif ability_count < 80 and memory.main.get_item_slot(19) != 255:
            throw_item = 19
        arena_menu_select(1)
        start_fight(area_index=13, monster_index=2)
        battle.main.distiller_and_killer(throw_item)
        if memory.main.get_item_count_slot(memory.main.get_item_slot(6)) < 40:
            arena_menu_select(4)
            # restock_downs()
            if memory.main.get_gil_value() < 10000:
                item_dump()
            arena_npc()
        power_count = memory.main.get_item_count_slot(memory.main.get_item_slot(70))
        mana_count = memory.main.get_item_count_slot(memory.main.get_item_slot(71))
        speed_count = memory.main.get_item_count_slot(memory.main.get_item_slot(72))
        ability_count = memory.main.get_item_count_slot(memory.main.get_item_slot(73))
    arena_menu_select(4)
    
    menu.equip_weapon(character=0, ability=0x8004,full_menu_close=False)
