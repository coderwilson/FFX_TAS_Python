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
from json_ai_files.write_seed import write_big_text
import xbox
import menu

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
            if memory.main.get_gil_value() > 500000:
                memory.main.update_formation(Tidus, Yuna, Rikku)
            else:
                memory.main.update_formation(Tidus, Wakka, Rikku)
            nemesis.arena_prep.arena_npc()
            nemesis.arena_select.arena_menu_select(1)
            if memory.main.get_gil_value() > 500000:
                nemesis.arena_select.start_fight(area_index=8, monster_index=7)
                battle.main.bribe_battle(spare_change_value=245000)
            else:
                nemesis.arena_select.start_fight(area_index=15, monster_index=7)
                battle.main.shadow_gem_farm()  # Same logic works both ways.
            nemesis.arena_select.arena_menu_select(4)
            need4 = grid_instance.get_node_count("Lv. 4 Lock")
            slot = memory.main.get_item_slot(84)
            current4 = memory.main.get_item_count_slot(slot)
            write_big_text(f"Lv.4 Key Spheres - {current4}/{need4}")
            logger.manip(f"Stock 4: {need4} - {current4} = {need4-current4}")
    
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
        target_node_id: int | None = None,
        clear_luck:bool=False
    ):
    grid_instance = get_grid() # Get the grid instance
    dist_dict = {}
    nodes_dict = {}
    start_node = grid_instance.character_at_node(actor_id)
    logger.debug(f"ACTOR {actor_id} START NODE CHECK: {start_node}")
    # memory.main.wait_seconds(5)
    char_name = memory.main.name_from_number(actor_id)
    char_levels = memory.sphere_grid.char_sphere_levels(actor_id)
    logger.debug(f"{char_name} has slvls: {char_levels}, target node {target_node_id}")
    
    path_nodes = None
    if target_node_id is not None:
        logger.debug("Mark 1")
        path_nodes_raw = grid_instance.find_shortest_path(start_node, target_node_id)
        logger.debug(f"Path to target node {target_node_id}: {path_nodes_raw}")
        if not path_nodes_raw:
            logger.warning(f"No valid path found to target node {target_node_id}")
            return None, None, None
        path_nodes = set(path_nodes_raw)
    logger.debug("Mark 2")

    # path_nodes = None
    # if target_node_id is not None:
    #     logger.debug("Mark 1")
    #     path = grid_instance.find_shortest_path(start_node, target_node_id)
    #     logger.debug(f"Path to target node {target_node_id}: {path}")
    #     if not path:
    #         logger.warning(f"No valid path found to target node {target_node_id}")
    #         return None, None
    #     path_nodes = set(path)
    # logger.debug("Mark 2")

    if locks >= 1:
        if memory.main.get_item_slot(81) != 255:
            nodes_dict["lv1"], dist_dict["lv1"] = grid_instance.find_nearest_node_of_type(start_node, "Lv. 1 Lock", path_nodes)
    if locks >= 2:
        if memory.main.get_item_slot(82) != 255:
            nodes_dict["lv2"], dist_dict["lv2"] = grid_instance.find_nearest_node_of_type(start_node, "Lv. 2 Lock", path_nodes)
    if locks >= 3:
        if memory.main.get_item_slot(83) != 255:
            nodes_dict["lv3"], dist_dict["lv3"] = grid_instance.find_nearest_node_of_type(start_node, "Lv. 3 Lock", path_nodes)
    if locks >= 4:
        if memory.main.get_item_slot(84) != 255:
            nodes_dict["lv4"], dist_dict["lv4"] = grid_instance.find_nearest_node_of_type(start_node, "Lv. 4 Lock", path_nodes)
    if clear_luck:
        nodes_dict["luck"], dist_dict["luck"] = grid_instance.find_nearest_node_of_type(start_node, "Luck_Up", path_nodes)
    # if include_empty:
    #     nodes_dict["empty"], dist_dict["empty"] = grid_instance.find_nearest_node_of_type(start_node, "Empty Node", path_nodes)
    nodes_dict["single"], dist_dict["single"] = grid_instance.find_nearest_multi_unlock_for_character(start_node, char_name, 1, path_nodes, include_empty=include_empty)
    nodes_dict["double"], dist_dict["double"] = grid_instance.find_nearest_multi_unlock_for_character(start_node, char_name, 2, path_nodes, include_empty=include_empty)
    nodes_dict["triple"], dist_dict["triple"] = grid_instance.find_nearest_multi_unlock_for_character(start_node, char_name, 3, path_nodes, include_empty=include_empty)

    best_dist = None
    best_key = None
    logger.warning(dist_dict)
    # memory.main.wait_frames(120)
    for key in dist_dict:
        if dist_dict[key] == 0:
            best_dist = dist_dict[key] # Corrected: access value from dict
            best_key = key
        elif dist_dict[key]:
            if best_dist == None or dist_dict[key] < best_dist:
                best_dist = dist_dict[key] # Corrected: access value from dict
                best_key = key
            elif key == "double" and best_key == "single":
                if dist_dict[key] - best_dist == 1:
                    best_dist = dist_dict[key] # Corrected
                    best_key = key
            elif key == "triple":
                if best_key == "double":
                    if dist_dict[key] - best_dist <= 1:
                        best_dist = dist_dict[key] # Corrected
                        best_key = key
                elif best_key == "single":
                    if dist_dict[key] - best_dist <= 2:
                        best_dist = dist_dict[key] # Corrected
                        best_key = key
    # This isn't working yet.
    # if best_dist == 0 and best_dist is not None:
    #     return nodes_dict[best_key], best_key, best_dist
    # try:
    #     logger.debug(f"Dist check: {best_dist}/{char_levels}")
    #     if best_dist > char_levels:
    #         logger.debug(f"Cannot reach best node. Moving that direction instead.")
    #         best_dist = char_levels
    #         logger.debug(path_nodes_raw)
    #         logger.debug(path_nodes)
    #         best_key = path_nodes[char_levels-1]
    #         logger.debug(f"Moving towards node {best_key} instead.")
    # except:
    #     pass

    if target_node_id is not None:
        logger.debug(f"Target: {target_node_id}, Path: {path_nodes}")
        if best_dist is None or char_levels is None:
            logger.debug(f"No nearby dead-end nodes. Try again with general pathing.")
            return nearest_interesting_node(
                actor_id=actor_id, 
                include_empty=include_empty, 
                locks=locks,
                target_node_id = None,
                clear_luck=clear_luck
            )
        elif best_dist > char_levels:
            logger.debug(f"No nearby dead-end nodes. Try again with general pathing.")
            return nearest_interesting_node(
                actor_id=actor_id, 
                include_empty=include_empty, 
                locks=locks,
                target_node_id = None,
                clear_luck=clear_luck
            )
    elif char_levels < 3:
        return None, None, None
    elif isinstance(best_dist,int) and best_dist > char_levels:
        # Here
        # Find shortest path to best_key
        # Travel as far as possible along that path.
        next_path = grid_instance.find_shortest_path(start_node, nodes_dict[best_key])
        logger.info("== No interesting nodes in range. Let's travel along this path instead.")
        logger.info(f"{next_path[char_levels-1]} | {next_path}")
        # memory.main.wait_frames(120)  # For testing only. Promise I won't forget this.
        return next_path[char_levels-1], "shortened_path", char_levels-1

        # logger.debug(f"== No interesting nodes in range. Return (A)")
        # return None, None, None
    if best_key is None:
        logger.debug(f"== No interesting nodes in range. Return (B)")
        return None, None, None

   
    # Assuming char_levels is a single number representing a max distance or similar.
    # The original logic `best_dist <= char_levels` seems to imply `best_dist` is a numerical value
    # and `char_levels` is also numerical.
    # logger.info(dist_dict)
    # logger.warning(nodes_dict)
    logger.info(f"== Best node identified: {nodes_dict[best_key]}")
    logger.info(f"== Type: {best_key} | Dist: {best_dist}")
    logger.debug(f"{best_dist} | {char_levels}")
    if best_dist is not None and char_levels is not None and best_dist <= char_levels:
        return nodes_dict[best_key], best_key, best_dist # Changed to best_key
    else:
        return None, None, None

def max_level_ups(
    actor_id, 
    include_empty:bool=True, 
    locks:int=0, 
    dest_index=None,
    clear_luck:bool=False
) -> str:
    slot = memory.main.get_item_slot(86)
    if slot == 255:
        logger.debug("No MP spheres, we haven't reached that point yet.")
        return
    count = memory.main.get_item_count_slot(slot)
    if count < 4:
        logger.debug("No MP spheres, we haven't reached that point yet.")
        return
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
                    grid_big_text_update(clear=True)
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
                logger.warning(f"Filling with STR (1)")
                unlock_array.append(87)
                unlock_array.append(70)
                current_node.change_node_type(0x05)
                current_node.set_unlocked_status(character_id=char_name, status=True)
                str_count -= 1
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
