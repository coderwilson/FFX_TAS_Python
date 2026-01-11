from sphere_grid.sphere_grid_library import SphereGrid, NODE_TYPE_MAP
import memory.main
import memory.sphere_grid
from menu_grid import (
    move_first,
    use_first,
    move_and_use,
    use_and_move,
    use_and_use_again,
    move_and_quit,
    use_and_quit,
    sel_sphere,
    coords_movement
)
from menu import open_grid
import nemesis.arena_prep
import nemesis.arena_select
import logging
import battle.main
from players import (
    Rikku, Tidus, Wakka,
    Yuna, Auron, Lulu, Kimahri
)
from json_ai_files.write_seed import write_big_text, write_custom_message
import xbox
import menu
import vars
game_vars = vars.vars_handle()

logger = logging.getLogger(__name__)

_grid = None  # Use an internal variable, convention for "private" globals
grid_file_path = "sphere_grid/grid_info.json"

def get_grid():
    """
    Returns the initialized SphereGrid instance.
    Initializes it if it hasn't been already.
    """
    global _grid
    if _grid is None:
        logger.info(f"Initializing SphereGrid from {grid_file_path}")
        _grid = SphereGrid(grid_file_path)
    return _grid

# Now, all functions needing 'grid' will call get_grid()
def stock_all_locks(limit:int=3, to_airship:bool=True):
    # Defaults to the first three, which we can do without unlocking Nemesis.
    if memory.main.get_map() == 307:
        starting_point = 'arena'
    elif memory.main.get_map() == 374:
        nemesis.arena_select.arena_return()
        starting_point = 'airship'
    else:
        starting_point = f'Unknown-{memory.main.get_map()}'
    
    need1 = 0
    need2 = 0
    need3 = 0
    need4 = 0

    grid_instance = get_grid()
    memory.main.update_formation(Tidus, Wakka, Rikku)

    need1 = grid_instance.get_node_count("Lv. 1 Lock")
    slot = memory.main.get_item_slot(81)
    current1 = memory.main.get_item_count_slot(slot)
    logger.manip(f"Stock 1: {need1} - {current1} = {need1-current1}")
    while current1 < need1:
        nemesis.arena_prep.arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=9, monster_index=1)
        battle.main.bribe_battle(spare_change_value=25000)
        nemesis.arena_select.arena_menu_select(4)
        memory.main.update_formation(Tidus, Wakka, Rikku)
        need1 = grid_instance.get_node_count("Lv. 1 Lock")
        slot = memory.main.get_item_slot(81)
        current1 = memory.main.get_item_count_slot(slot)
        logger.manip(f"Stock 1: {need1} - {current1} = {need1-current1}")

    if limit >= 2:
        need2 = grid_instance.get_node_count("Lv. 2 Lock")
        slot = memory.main.get_item_slot(82)
        current2 = memory.main.get_item_count_slot(slot)
        logger.manip(f"Stock 2: {need2} - {current2} = {need2-current2}")
        while current2 < need2:
            nemesis.arena_prep.arena_npc()
            nemesis.arena_select.arena_menu_select(1)
            nemesis.arena_select.start_fight(area_index=10, monster_index=8)
            battle.main.bribe_battle(spare_change_value=580000)
            nemesis.arena_select.arena_menu_select(4)
            memory.main.update_formation(Tidus, Wakka, Rikku)
            need2 = grid_instance.get_node_count("Lv. 2 Lock")
            slot = memory.main.get_item_slot(82)
            current2 = memory.main.get_item_count_slot(slot)
            logger.manip(f"Stock 2: {need2} - {current2} = {need2-current2}")

    if limit >= 3:
        need3 = grid_instance.get_node_count("Lv. 3 Lock")
        slot = memory.main.get_item_slot(83)
        current3 = memory.main.get_item_count_slot(slot)
        logger.manip(f"Stock 3: {need3} - {current3} = {need3-current3}")
        while current3 < need3:
            nemesis.arena_prep.arena_npc()
            nemesis.arena_select.arena_menu_select(1)
            nemesis.arena_select.start_fight(area_index=11, monster_index=4)
            battle.main.bribe_battle(spare_change_value=1125000)
            nemesis.arena_select.arena_menu_select(4)
            memory.main.update_formation(Tidus, Wakka, Rikku)
            need3 = grid_instance.get_node_count("Lv. 3 Lock")
            slot = memory.main.get_item_slot(83)
            current3 = memory.main.get_item_count_slot(slot)
            logger.manip(f"Stock 3: {need3} - {current3} = {need3-current3}")

    if limit >= 4:
        need4 = grid_instance.get_node_count("Lv. 4 Lock")
        slot = memory.main.get_item_slot(84)
        current4 = memory.main.get_item_count_slot(slot)
        write_big_text(f"Lv.4 Key Spheres - {current4}/{need4}")
        logger.manip(f"Stock 4: {need4} - {current4} = {need4-current4}")
        while current4 < need4:
            # if memory.main.get_gil_value() > 500000:
            #     memory.main.update_formation(Tidus, Yuna, Rikku)
            # else:
            memory.main.update_formation(Tidus, Wakka, Rikku)
            nemesis.arena_prep.arena_npc()
            nemesis.arena_select.arena_menu_select(1)
            # if memory.main.get_gil_value() > 500000:
            #     nemesis.arena_select.start_fight(area_index=8, monster_index=7)
            #     battle.main.bribe_battle(spare_change_value=245000)
            # else:
            nemesis.arena_select.start_fight(area_index=15, monster_index=7)
            battle.main.shadow_gem_farm()  # Same logic works both ways.
            nemesis.arena_select.arena_menu_select(4)
            if game_vars.check_plat_test_mode():
                # Only works if plat test mode is active.
                memory.main.set_item_count(item_num=84,quantity=90)
            need4 = grid_instance.get_node_count("Lv. 4 Lock")
            slot = memory.main.get_item_slot(84)
            current4 = memory.main.get_item_count_slot(slot)
            write_big_text(f"Lv.4 Key Spheres - {current4}/{need4}")
            logger.manip(f"Stock 4: {need4} - {current4} = {need4-current4}")
    
    menu.equip_weapon(character=6, ability=0x8019,full_menu_close=False)
    menu.equip_weapon(character=4, ability=0x8019,full_menu_close=False)
    menu.equip_weapon(character=0, ability=0x8019,full_menu_close=True)
    logger.debug(f"Returning to starting point: {starting_point}")
    if starting_point == 'airship' and to_airship:
        nemesis.arena_select.return_to_airship()

def stock_return_sphere():
    # Assume we start at the arena.
    nemesis.arena_prep.arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=9, monster_index=2)
    battle.main.bribe_battle(spare_change_value=50000)
    nemesis.arena_select.arena_menu_select(4)
    memory.main.update_formation(Tidus, Wakka, Rikku)

def nearest_interesting_node(
        actor_id, 
        include_empty:bool=True, 
        locks:int=0,
        target_node_id: int | None = None, # Highest Priority Target
        clear_luck:bool=False
    ):
    grid_instance = get_grid() # Get the grid instance
    dist_dict = {}
    nodes_dict = {}
    start_node = grid_instance.character_at_node(actor_id)
    logger.debug(f"ACTOR {actor_id} START NODE CHECK: {start_node}")
    
    char_name = memory.main.name_from_number(actor_id)
    char_levels = memory.sphere_grid.char_sphere_levels(actor_id)
    logger.debug(f"{char_name} has slvls: {char_levels}, target node {target_node_id}")
    
    path_nodes = None
    final_target_id = target_node_id # This will hold the node we are ultimately pathing towards

    # --- 1. Determine Target and Path Constraint Priority ---

    # Priority 1: Explicit target_node_id provided
    if final_target_id is not None:
        logger.debug("Mark 1: Processing explicit target node (Priority 1).")
        path_nodes_raw = grid_instance.find_shortest_path(start_node, final_target_id)
        if not path_nodes_raw:
            logger.warning(f"No valid path found to explicit target node {final_target_id}")
            return None, None, None
        
        path_nodes = set(path_nodes_raw)

    # Priority 2: Dead-End Search (Only runs if no explicit target was provided)
    elif final_target_id is None:
        dead_end_path = grid_instance.find_path_to_nearest_dead_end(start_node, actor_id)
        
        if dead_end_path:
            logger.debug(f"Dead-end path found (Priority 2): {dead_end_path}")
            
            # Set the dead end as the final target
            final_target_id = dead_end_path[-1] 
            
            # Set path_nodes to constrain all subsequent searches to this path
            path_nodes = set(dead_end_path)
            
            # # Add the dead-end to the dicts for selection among other nodes on the path
            # nodes_dict["dead_end"] = final_target_id
            # dist_dict["dead_end"] = len(dead_end_path) - 1 # Distance is path length - 1

    # Priority 3: No path constraint (path_nodes remains None)
    if final_target_id:
        logger.info(f"Mark 2: Path constraint set by target: {final_target_id} - distance {len(path_nodes)-1}")
        logger.info(f"Path nodes: {path_nodes}.")
    else:
        logger.info(f"No destination set.")
    # memory.main.wait_frames(90)

    # --- 2. Find Nearest Nodes (Constrained by path_nodes) ---
    
    # Lock nodes
    if locks >= 1 and memory.main.get_item_slot(81) != 255:
        nodes_dict["lv1"], dist_dict["lv1"] = grid_instance.find_nearest_node_of_type(start_node, "Lv. 1 Lock", path_nodes)
    if locks >= 2 and memory.main.get_item_slot(82) != 255:
        nodes_dict["lv2"], dist_dict["lv2"] = grid_instance.find_nearest_node_of_type(start_node, "Lv. 2 Lock", path_nodes)
    if locks >= 3 and memory.main.get_item_slot(83) != 255:
        nodes_dict["lv3"], dist_dict["lv3"] = grid_instance.find_nearest_node_of_type(start_node, "Lv. 3 Lock", path_nodes)
    if locks >= 4 and memory.main.get_item_slot(84) != 255:
        nodes_dict["lv4"], dist_dict["lv4"] = grid_instance.find_nearest_node_of_type(start_node, "Lv. 4 Lock", path_nodes)
    
    # Luck node
    if clear_luck:
        nodes_dict["luck"], dist_dict["luck"] = grid_instance.find_nearest_node_of_type(start_node, "Luck_Up", path_nodes)
    
    # Multi-unlock nodes
    nodes_dict["single"], dist_dict["single"] = grid_instance.find_nearest_multi_unlock_for_character(start_node, char_name, 1, path_nodes, include_empty=include_empty)
    nodes_dict["double"], dist_dict["double"] = grid_instance.find_nearest_multi_unlock_for_character(start_node, char_name, 2, path_nodes, include_empty=include_empty)
    nodes_dict["triple"], dist_dict["triple"] = grid_instance.find_nearest_multi_unlock_for_character(start_node, char_name, 3, path_nodes, include_empty=include_empty)

    # --- 3. Determine Best Node (Shortest distance along the constrained path or general search) ---
    
    best_dist = None
    best_key = None
    logger.warning(dist_dict)

    # Initialize best_dist/best_key from the dict
    for key in dist_dict:
        current_dist = dist_dict[key]
        if current_dist is None:
            continue
            
        if best_dist is None or current_dist < best_dist:
            best_dist = current_dist
            best_key = key
        
        # Complex tie-breakers (Reincorporated exactly as you had them)
        elif key == "double" and best_key == "single" and current_dist - dist_dict.get("single", 0) == 1:
            best_dist = current_dist
            best_key = key
        elif key == "triple":
            if best_key == "double" and current_dist - dist_dict.get("double", 0) <= 1:
                best_dist = current_dist
                best_key = key
            elif best_key == "single" and current_dist - dist_dict.get("single", 0) <= 2:
                best_dist = current_dist
                best_key = key


    # --- 4. Final Decision and Path Traversal ---

    # Case A: A target path was set (explicit or dead-end)
    if final_target_id is not None:
        
        # If no interesting nodes were found *along the path* OR the shortest path is too long
        if best_key is None or (best_dist > char_levels and best_dist < 60):
            logger.debug("Level limit reached.")
            return None, None, None
            # logger.debug(f"Target path found, but best node ({best_key}) is too far ({best_dist}) or no intermediate nodes found. Try again with general pathing (Priority 3).")
            # # Recurse to find the general best node (Priority 3). target_node_id=None forces general search.
            # return nearest_interesting_node(
            #     actor_id=actor_id, 
            #     include_empty=include_empty, 
            #     locks=locks,
            #     target_node_id = None,
            #     clear_luck=clear_luck
            # )
        
        # If the best node is found *along* the constrained path, we need to travel along it.
        if best_dist is not None and best_dist <= char_levels:
            
            # The *best* node found (e.g., a "single" unlock) is our immediate goal.
            path_target_id = nodes_dict[best_key]
            
            # Get the full shortest path to the intermediate best node.
            full_path = grid_instance.find_shortest_path(start_node, path_target_id)
            
            if not full_path or len(full_path) == 0:
                 logger.info(f"Cannot path to selected target {path_target_id}. Re-running without target.")
                 return nearest_interesting_node(actor_id=actor_id, include_empty=include_empty, locks=locks, target_node_id = None, clear_luck=clear_luck)

            # Determine the maximum distance we can travel: min(char_levels, distance to target)
            travel_distance = min(char_levels, len(full_path) - 1)
            
            # The final node to land on is at the maximum travel distance
            final_node_id = full_path[travel_distance]
            
            logger.info(f"== Pathing along constrained path. Target: {path_target_id}. Max travel: {travel_distance} steps.")
            logger.info(f"Targeting final node: {final_node_id} (Type: {best_key})")
            return final_node_id, best_key, travel_distance

    # Case B: No target path was set (General Search / Priority 3)
    
    # If no interesting node was found at all
    if best_key is None:
        logger.debug(f"== No interesting nodes in range. Return (B)")
        return None, None, None

    # If best node is too far, but we have enough Sphere Levels (char_levels) to travel part of the way
    if isinstance(best_dist, int) and best_dist > char_levels:
        
        # Find shortest path to the best overall node (regardless of distance)
        next_path = grid_instance.find_shortest_path(start_node, nodes_dict[best_key])
        
        if next_path and char_levels >= 1:
            # Travel as far as possible along that path (up to char_levels)
            final_node_index = min(char_levels, len(next_path) - 1)
            final_node = next_path[final_node_index]
            travel_dist = final_node_index
            
            logger.info("== No interesting nodes in range. Traveling along path toward furthest goal.")
            logger.info(f"Targeting node {final_node} at distance {travel_dist}.")
            return final_node, "shortened_path", travel_dist
        
        # Fallback if char_levels is too low or no path exists
        logger.debug(f"== No interesting nodes in range and cannot travel. Return (C)")
        return None, None, None

    # Case C: Best node found is within char_levels range in the general search
    if best_dist is not None and char_levels is not None and best_dist <= char_levels:
        logger.info(f"== Best node identified: {nodes_dict[best_key]}")
        logger.info(f"== Type: {best_key} | Dist: {best_dist}")
        return nodes_dict[best_key], best_key, best_dist
    
    # Final safety fallback
    return None, None, None

def max_level_ups(
    actor_id, 
    include_empty:bool=True, 
    locks:int=0, 
    dest_index=None,
    clear_luck:bool=False
) -> str:
    slot = memory.main.get_item_slot(86)
    # These will avoid opening the grid while on low spheres.
    if slot == 255:
        logger.debug("No MP spheres, we haven't reached that point yet. (A)")
        return "low_spheres"
    count = memory.main.get_item_count_slot(slot)
    if count < 3:
        logger.debug("No MP spheres, we haven't reached that point yet. (B)")
        return "low_spheres"
    if memory.main.get_item_count_slot(memory.main.get_item_slot(70)) < 4:
        logger.warning(f"Out of power spheres!")
        char_levels = 0
        return "low_spheres"
    if memory.main.get_item_count_slot(memory.main.get_item_slot(71)) < 4:
        logger.warning(f"Out of mana spheres!")
        char_levels = 0
        return "low_spheres"
    if memory.main.get_item_count_slot(memory.main.get_item_slot(72)) < 4:
        logger.warning(f"Out of speed spheres!")
        char_levels = 0
        return "low_spheres"

    grid_instance = get_grid() # Get the grid instance
    # logger.warning("===============")
    # logger.warning(grid_instance)
    # logger.warning(f"Nodes: {len(grid_instance._nodes)}")
    # logger.warning("===============")
    grid_big_text_update()
    start = grid_instance.character_at_node(actor_id)
    char_levels = memory.sphere_grid.char_sphere_levels(actor_id)
    logger.debug(f"==== Starting max level up function for {actor_id}: {char_levels} ====")
    logger.debug(f"Include empty nodes:  {include_empty}")
    open_grid(actor_id)
    err_type = None
    target, tar_type, _ = nearest_interesting_node(
        actor_id=actor_id, 
        include_empty=include_empty, 
        locks=locks,
        target_node_id=dest_index,
        clear_luck=clear_luck
    )
    logger.debug(f"{target} | {grid_instance.get_node(target)}")
    if tar_type == "shortened_path":
        move_first()
        dest = list(grid_instance.get_node(target).position)
        logger.info(f"Moving to position: {dest}")
        coords_movement(dest)
        move_and_quit()
        memory.main.close_menu()
        grid_big_text_update(clear=True)
        return tar_type
    if target is None:
        use_first()
    elif target != memory.sphere_grid.cursor_current_node():
        move_first()
        dest = list(grid_instance.get_node(target).position)
        logger.info(f"Moving to position: {dest}")
        coords_movement(dest)
        move_and_use()
    else:
        use_first()

    while char_levels is not None and char_levels >= 1:
        update_completion_report()
        # if count_still_locked(actor_id=actor_id) == 1:
        #     # Figure this out later, this would be very helpful.
        #     sel_sphere(unlock_array[i], "master")
        if memory.main.get_item_count_slot(memory.main.get_item_slot(70)) < 4:
            logger.warning(f"Out of power spheres!")
            char_levels = 0
            err_type = "low_spheres"
        elif memory.main.get_item_count_slot(memory.main.get_item_slot(71)) < 4:
            logger.warning(f"Out of mana spheres!")
            char_levels = 0
            err_type = "low_spheres"
        elif memory.main.get_item_count_slot(memory.main.get_item_slot(72)) < 4:
            logger.warning(f"Out of speed spheres!")
            char_levels = 0
            err_type = "low_spheres"
        elif memory.main.get_item_count_slot(memory.main.get_item_slot(86)) < 4:
            logger.warning(f"Out of MP spheres!")
            char_levels = 0
            err_type = "low_filler_spheres"
        elif not perform_level_up(
            tar_node=target,
            include_empty=include_empty,
            locks=locks,
            clear_luck=clear_luck
        ):
            update_completion_report()
            char_levels = 0
        else:
            char_levels = memory.sphere_grid.char_sphere_levels(actor_id)
            logger.debug(f"Remaining sphere levels: {char_levels}")
            try:
                target, tar_type, _ = nearest_interesting_node(
                    actor_id=actor_id,
                    include_empty=include_empty, 
                    locks=locks,
                    target_node_id=dest_index,
                    clear_luck=clear_luck
                )
                if tar_type == "shortened_path":
                    use_and_move()
                    dest = list(grid_instance.get_node(target).position)
                    logger.info(f"Moving to position: {dest}")
                    coords_movement(dest)
                    move_and_quit()
                    memory.main.close_menu()
                    grid_big_text_update(clear=True)
                    update_completion_report()
                    return tar_type
                logger.debug(f"{target} | {grid_instance.get_node(target)}")
                if char_levels is None or target is None:
                    char_levels = 0
                elif char_levels >= 1:
                    use_and_move()
                    
                    dest = list(grid_instance.get_node(target).position)
                    logger.info(f"Moving to position: {dest}")
                    coords_movement(dest)
                    move_and_use()
            except Exception as e:
                logger.error(f"max_level_ups error: {e}")
                break
                # quit()
    
    logger.info("Wrapping up sphere grid for this character.")
    use_and_quit()
    memory.main.close_menu()
    grid_big_text_update(clear=True)
    if err_type is not None:
        logger.warning(err_type)
        return err_type
    elif dest_index == grid_instance.character_at_node(actor_id):
        logger.warning("Reached destination!!!")
        # memory.main.wait_frames(150)
        return "dest_reached"
    elif char_levels is None or char_levels == 0:
        logger.warning("Out of levels!!!")
        # memory.main.wait_frames(150)
        return "levels"
    logger.warning("Unknown return state!")
    # memory.main.wait_frames(150)
    return "other"

    
def perform_level_up(tar_node, include_empty:bool=True, locks:int=0, clear_luck:bool=False):
    grid_big_text_update()
    grid_instance = get_grid() # Get the grid instance
    character_id = memory.main.s_grid_char()
    char_name = memory.main.name_from_number(character_id)
    str_count = memory.main.get_item_count_slot(memory.main.get_item_slot(87))
    hp_count = memory.main.get_item_count_slot(memory.main.get_item_slot(85))
    mp_count = memory.main.get_item_count_slot(memory.main.get_item_slot(86))
    mdef_count = memory.main.get_item_count_slot(memory.main.get_item_slot(90))
    lv4_count = memory.main.get_item_count_slot(memory.main.get_item_slot(84))
    
    current_node = grid_instance.get_node(tar_node)
    unlock_array = []

    if current_node:
        logger.info(f"Unlocking for {char_name} ({clear_luck})")
        use_sphere_type = current_node.get_unlock_sphere_id()
        logger.debug(f"Current node sphere type: {use_sphere_type}")
        if use_sphere_type == None:
            if include_empty:
                if str_count >= 1:
                    logger.warning(f"Filling with STR (1)")
                    unlock_array.append(87)
                    unlock_array.append(70)
                    current_node.change_node_type(0x05)
                    current_node.set_unlocked_status(character_id=char_name, status=True)
                    str_count -= 1
                elif mdef_count >= 1:
                    logger.warning(f"Filling with MDEF (1)")
                    unlock_array.append(90)
                    unlock_array.append(71)
                    current_node.change_node_type(0x11)
                    current_node.set_unlocked_status(character_id=char_name, status=True)
                    mdef_count -= 1
                elif hp_count >= 1:
                    logger.warning(f"Filling with HP (1)")
                    unlock_array.append(85)
                    unlock_array.append(70)
                    current_node.change_node_type(0x23)
                    current_node.set_unlocked_status(character_id=char_name, status=True)
                    hp_count -= 1
                elif mp_count >= 1:
                    logger.warning(f"Filling with MP (1)")
                    unlock_array.append(86)
                    unlock_array.append(71)
                    current_node.change_node_type(0x24)
                    current_node.set_unlocked_status(character_id=char_name, status=True)
                    mp_count -= 1
            else:
                # logger.debug("Skipping blank nodes.")
                pass
        elif clear_luck and use_sphere_type == 74:
            unlock_array.append(95)  # Clear sphere
            if str_count >= 1:
                logger.warning(f"Filling with STR (1A)")
                unlock_array.append(87)
                unlock_array.append(70)
                current_node.change_node_type(0x05)
                current_node.set_unlocked_status(character_id=char_name, status=True)
                str_count -= 1
            elif mdef_count >= 1:
                logger.warning(f"Filling with MDEF (1A)")
                unlock_array.append(90)
                unlock_array.append(71)
                current_node.change_node_type(0x11)
                current_node.set_unlocked_status(character_id=char_name, status=True)
                mdef_count -= 1
            elif hp_count >= 1:
                logger.warning(f"Filling with HP (1A)")
                unlock_array.append(85)
                unlock_array.append(70)
                current_node.change_node_type(0x23)
                current_node.set_unlocked_status(character_id=char_name, status=True)
                hp_count -= 1
            elif mp_count >= 1:
                logger.warning(f"Filling with MP (1A)")
                unlock_array.append(86)
                unlock_array.append(71)
                current_node.change_node_type(0x24)
                current_node.set_unlocked_status(character_id=char_name, status=True)
                mp_count -= 1

        elif not current_node.unlocked_by_characters.get(char_name, False):
            if memory.main.get_item_slot(current_node.get_unlock_sphere_id()) != 255:
                logger.debug(f"Attempting to use: {use_sphere_type}")
                unlock_array.append(use_sphere_type)
                if use_sphere_type in [70,71,72,73,74]:
                    current_node.set_unlocked_status(character_id=char_name, status=True)
    
        for neighbor_id in current_node.adjacent_node_ids:
            neighbor_node = grid_instance.get_node(neighbor_id)
            use_sphere_type = neighbor_node.get_unlock_sphere_id()
            if use_sphere_type == None:
                if include_empty:
                    if str_count >= 1:
                        logger.warning(f"Filling with STR (2)")
                        unlock_array.append(87)
                        unlock_array.append(70)
                        neighbor_node.change_node_type(0x05)
                        neighbor_node.set_unlocked_status(character_id=char_name, status=True)
                        str_count -= 1
                    elif mdef_count >= 1:
                        logger.warning(f"Filling with MDEF (2)")
                        unlock_array.append(90)
                        unlock_array.append(71)
                        current_node.change_node_type(0x11)
                        current_node.set_unlocked_status(character_id=char_name, status=True)
                        mdef_count -= 1
                    elif hp_count >= 1:
                        logger.warning(f"Filling with HP (300)")
                        unlock_array.append(85)
                        unlock_array.append(70)
                        neighbor_node.change_node_type(0x23)
                        neighbor_node.set_unlocked_status(character_id=char_name, status=True)
                        hp_count -= 1
                    elif mp_count >= 1:
                        logger.warning(f"Filling with MP (2)")
                        unlock_array.append(86)
                        unlock_array.append(71)
                        neighbor_node.change_node_type(0x24)
                        neighbor_node.set_unlocked_status(character_id=char_name, status=True)
                        mp_count -= 1
                else:
                    # logger.debug("Skipping blank nodes.")
                    pass
            elif not neighbor_node.unlocked_by_characters.get(char_name, False):
                logger.debug(f"Check node {neighbor_id} - node type {use_sphere_type}")
                if (
                    use_sphere_type in [81,82,83,84] and
                    use_sphere_type - 80 > locks
                ):
                    logger.debug(f"No unlock for node {neighbor_id} | {locks}")
                    pass
                elif memory.main.get_item_slot(neighbor_node.get_unlock_sphere_id()) != 255:
                    logger.debug(f"Attempting to use: {use_sphere_type}")
                    if use_sphere_type == 84 and lv4_count >= 1:
                        unlock_array.append(use_sphere_type)
                        neighbor_node.change_node_type(0x01)
                        if include_empty:
                            if str_count >= 1:
                                logger.warning(f"Filling with STR (3)")
                                unlock_array.append(87)
                                unlock_array.append(70)
                                neighbor_node.change_node_type(0x05)
                                neighbor_node.set_unlocked_status(character_id=char_name, status=True)
                                str_count -= 1
                            elif mdef_count >= 1:
                                logger.warning(f"Filling with MDEF (3)")
                                unlock_array.append(90)
                                unlock_array.append(71)
                                current_node.change_node_type(0x11)
                                current_node.set_unlocked_status(character_id=char_name, status=True)
                                mdef_count -= 1
                            elif hp_count >= 1:
                                logger.warning(f"Filling with HP (300)")
                                unlock_array.append(85)
                                unlock_array.append(70)
                                neighbor_node.change_node_type(0x23)
                                neighbor_node.set_unlocked_status(character_id=char_name, status=True)
                                hp_count -= 1
                            elif mp_count >= 1:
                                logger.warning(f"Filling with MP (3)")
                                unlock_array.append(86)
                                unlock_array.append(71)
                                neighbor_node.change_node_type(0x24)
                                neighbor_node.set_unlocked_status(character_id=char_name, status=True)
                                mp_count -= 1
                    elif use_sphere_type in [81,82,83] and use_sphere_type-80 <= locks:
                        logger.debug(f"Adding unlock sphere to queue: {use_sphere_type}")
                        unlock_array.append(use_sphere_type)
                        neighbor_node.change_node_type(0x01)
                        if include_empty:
                            if str_count >= 1:
                                logger.warning(f"Filling with STR (5)")
                                unlock_array.append(87)
                                unlock_array.append(70)
                                neighbor_node.change_node_type(0x05)
                                neighbor_node.set_unlocked_status(character_id=char_name, status=True)
                                str_count -= 1
                            elif mdef_count >= 1:
                                logger.warning(f"Filling with MDEF (5)")
                                unlock_array.append(90)
                                unlock_array.append(71)
                                current_node.change_node_type(0x11)
                                current_node.set_unlocked_status(character_id=char_name, status=True)
                                mdef_count -= 1
                            elif mp_count >= 1:
                                logger.warning(f"Filling with MP (5)")
                                unlock_array.append(86)
                                unlock_array.append(71)
                                neighbor_node.change_node_type(0x24)
                                neighbor_node.set_unlocked_status(character_id=char_name, status=True)
                                mp_count -= 1
                    else:
                        unlock_array.append(use_sphere_type)
                        if use_sphere_type in [70,71,72,73,74]:
                            logger.debug(f"Regular node: {use_sphere_type}")
                            current_node.set_unlocked_status(character_id=char_name, status=True)
                        if use_sphere_type in [81,82,83,84]:
                            neighbor_node.change_node_type(0x01)
                            if include_empty:
                                if str_count >= 1:
                                    logger.warning(f"Filling with STR (4)")
                                    unlock_array.append(87)
                                    unlock_array.append(70)
                                    neighbor_node.change_node_type(0x05)
                                    neighbor_node.set_unlocked_status(character_id=char_name, status=True)
                                    str_count -= 1
                                elif mdef_count >= 1:
                                    logger.warning(f"Filling with MDEF (4)")
                                    unlock_array.append(90)
                                    unlock_array.append(71)
                                    current_node.change_node_type(0x11)
                                    current_node.set_unlocked_status(character_id=char_name, status=True)
                                    mdef_count -= 1
                                elif mp_count >= 1:
                                    logger.warning(f"Filling with MP (4)")
                                    unlock_array.append(86)
                                    unlock_array.append(71)
                                    neighbor_node.change_node_type(0x24)
                                    neighbor_node.set_unlocked_status(character_id=char_name, status=True)
                                    mp_count -= 1
    
    logger.debug(f"Using the following spheres: {unlock_array}")
    if len(unlock_array) == 0:
        xbox.menu_a()
        use_and_quit()
        memory.main.close_menu()
        logger.info(f"Nothing to unlock. Returning.")
        return False
    for i in range(len(unlock_array)):
        if not sel_sphere(unlock_array[i], "none"):
            # This occurs if there was an issue unlocking a node.
            grid_instance.check_all_node_types()

            xbox.menu_a()
            xbox.menu_a()
            use_and_use_again()
        if i != len(unlock_array) - 1:
            use_and_use_again()

    logger.debug("Done leveling up from this node.")
    grid_big_text_update()
    return True


def restock_mp():
    menu.equip_weapon(character=0, ability=32772,full_menu_close=True)  # Evade & Counter (Caldabolg)
    nemesis.arena_battles.vidatu_farm()
    menu.equip_weapon(character=0, ability=0x8011,full_menu_close=True)

def restock_spheres(sphere_type:int=70):

    logger.warning("Restocking spheres!")
    distiller_type = 0
    distiller_count = 0
    if sphere_type in [70,71,72,73]:
        distiller_type = sphere_type - 54
        distiller_index = memory.main.get_item_slot(distiller_type)
        if distiller_index < 150:
            distiller_count = memory.main.get_item_count_slot(distiller_index)
        if distiller_count <= 4:
            nemesis.arena_select.rin_equip_dump(stock_distillers=True)
    
    if memory.main.get_map() != 307:
        nemesis.arena_select.arena_return()
    
    # The four main spheres use distillers.
    if sphere_type in [70,71,72,73]:
        for i in range(4):
            distiller_type = sphere_type + i - 54

            # Determine initial sphere count
            sphere_index = memory.main.get_item_slot(sphere_type+i)
            if sphere_index != 255:
                sphere_count = 0
            else:
                sphere_count = memory.main.get_item_count_slot(sphere_index)
            while sphere_count < 60:
                nemesis.arena_select.arena_npc()
                nemesis.arena_select.arena_menu_select(1)
                nemesis.arena_select.start_fight(area_index=13, monster_index=2)
                battle.main.distiller_and_killer(distiller_type)
                nemesis.arena_select.arena_menu_select(4)

                # Re-identify sphere count.
                sphere_index = memory.main.get_item_slot(sphere_type+i)
                if sphere_index < 150:
                    sphere_count = memory.main.get_item_count_slot(sphere_index)
                else:
                    sphere_count = 0
    else:
        # We'll need to figure this out later.
        # Fortune spheres, for unlocking luck
        # lv4 steals from Nemesis
        # idk something else for filling in blanks?
        pass
    
def grid_big_text_update(clear:bool=False):
    if clear:
        write_big_text("")
        return
        
    out_text = "Grid Sphere check:\n"
    
    sphere_index = memory.main.get_item_slot(70)
    if sphere_index == 255:
        sphere_count = 0
    else:
        sphere_count = memory.main.get_item_count_slot(sphere_index)
    out_text += f"Power: {sphere_count}\n"
    sphere_index = memory.main.get_item_slot(71)
    if sphere_index == 255:
        sphere_count = 0
    else:
        sphere_count = memory.main.get_item_count_slot(sphere_index)
    out_text += f"Mana: {sphere_count}\n"
    sphere_index = memory.main.get_item_slot(72)
    if sphere_index == 255:
        sphere_count = 0
    else:
        sphere_count = memory.main.get_item_count_slot(sphere_index)
    out_text += f"Speed: {sphere_count}"

    write_big_text(out_text)
    return


def count_still_locked(actor_id:int) -> int:
    grid_instance = get_grid() # Get the grid instance
    return grid_instance.count_all_unlockables(actor_id)

def update_completion_report():
    total_remaining = 0
    remaining_array = [0]*7
    for i in range(7):
        remaining_array[i] = count_still_locked(actor_id=i)
        total_remaining += remaining_array[i]
    completion = round((6020-total_remaining)/60.20,2)
    logger.info(f"Remaining sphere grid across all characters: {remaining_array}")
    report_str = f"Complete: {completion}% ({total_remaining} remain)\nPer-char: {remaining_array}"
    write_custom_message(report_str)