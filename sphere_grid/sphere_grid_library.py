import json
import os
from collections import deque
import logging
from typing import Union
from memory.sphere_grid import node_type, unlocked_by, char_current_node

import memory.main

logger = logging.getLogger(__name__)


# --- Placeholder Mappings (User to fill in later) ---
# These dictionaries would map the numerical IDs from 'defaultContent'
# to human-readable names for node types.
# You will need to populate these based on your game's data.

NODE_TYPE_MAP = {
    0x00: "Lv. 3 Lock",
    0x01: "Empty Node",
    0x02: "Strength (1 pt)",
    0x03: "Strength (2 pt)",
    0x04: "Strength (3 pt)",
    0x05: "Strength (4 pt)",
    0x06: "Defense (1 pt)",
    0x07: "Defense (2 pt)",
    0x08: "Defense (3 pt)",
    0x09: "Defense (4 pt)",
    0x0A: "Magic (1 pt)",
    0x0B: "Magic (2 pt)",
    0x0C: "Magic (3 pt)",
    0x0D: "Magic (4 pt)",
    0x0E: "Magic Defense (1 pt)",
    0x0F: "Magic Defense (2 pt)",
    0x10: "Magic Defense (3 pt)",
    0x11: "Magic Defense (4 pt)",
    0x12: "Agility (1 pt)",
    0x13: "Agility (2 pt)",
    0x14: "Agility (3 pt)",
    0x15: "Agility (4 pt)",
    0x16: "Luck (1 pt)",
    0x17: "Luck (2 pt)",
    0x18: "Luck (3 pt)",
    0x19: "Luck (4 pt)",
    0x1A: "Evasion (1 pt)",
    0x1B: "Evasion (2 pt)",
    0x1C: "Evasion (3 pt)",
    0x1D: "Evasion (4 pt)",
    0x1E: "Accuracy (1 pt)",
    0x1F: "Accuracy (2 pt)",
    0x20: "Accuracy (3 pt)",
    0x21: "Accuracy (4 pt)",
    0x22: "HP (200 pt)",
    0x23: "HP (300 pt)",
    0x24: "MP (40 pt)",
    0x25: "MP (20 pt)",
    0x26: "MP (10 pt)",
    0x27: "Lv. 1 Lock",
    0x28: "Lv. 2 Lock",
    0x29: "Lv. 4 Lock",
    0x2A: "Delay Attack",
    0x2B: "Delay Buster",
    0x2C: "Sleep Attack",
    0x2D: "Silence Attack",
    0x2E: "Dark Attack",
    0x2F: "Zombie Attack",
    0x30: "Sleep Buster",
    0x31: "Silence Buster",
    0x32: "Dark Buster",
    0x33: "Triple Foul",
    0x34: "Power Break",
    0x35: "Magic Break",
    0x36: "Armor Break",
    0x37: "Mental Break",
    0x38: "Mug",
    0x39: "Quick Hit",
    0x3A: "Steal",
    0x3B: "Use",
    0x3C: "Flee",
    0x3D: "Pray",
    0x3E: "Cheer",
    0x3F: "Focus",
    0x40: "Reflex",
    0x41: "Aim",
    0x42: "Luck",
    0x43: "Jinx",
    0x44: "Lancet",
    0x45: "Guard",
    0x46: "Sentinel",
    0x47: "Spare Change",
    0x48: "Threaten",
    0x49: "Provoke",
    0x4A: "Entrust",
    0x4B: "Copycat",
    0x4C: "Doublecast",
    0x4D: "Bribe",
    0x4E: "Cure",
    0x4F: "Cura",
    0x50: "Curaga",
    0x51: "NulFrost",
    0x52: "NulBlaze",
    0x53: "NulShock",
    0x54: "NulTide",
    0x55: "Scan",
    0x56: "Esuna",
    0x57: "Life",
    0x58: "Full-Life",
    0x59: "Haste",
    0x5A: "Hastega",
    0x5B: "Slow",
    0x5C: "Slowga",
    0x5D: "Shell",
    0x5E: "Protect",
    0x5F: "Reflect",
    0x60: "Dispel",
    0x61: "Regen",
    0x62: "Holy",
    0x63: "Auto-Life",
    0x64: "Blizzard",
    0x65: "Fire",
    0x66: "Thunder",
    0x67: "Water",
    0x68: "Fira",
    0x69: "Blizzara",
    0x6A: "Thundara",
    0x6B: "Watera",
    0x6C: "Firaga",
    0x6D: "Blizzaga",
    0x6E: "Thundaga",
    0x6F: "Waterga",
    0x70: "Bio",
    0x71: "Demi",
    0x72: "Death",
    0x73: "Drain",
    0x74: "Osmose",
    0x75: "Flare",
    0x76: "Ultima",
    0x77: "Pilfer Gil",
    0x78: "Full Break",
    0x79: "Extract Power",
    0x7A: "Extract Mana",
    0x7B: "Extract Speed",
    0x7C: "Extract Ability",
    0x7D: "Nab Gil",
    0x7E: "Quick Pockets",
}

# --- Sphere Item ID to Name Mappings ---
# These are the actual in-game item IDs for the spheres, and their names.
# This list is now streamlined to only include sphere types that directly unlock nodes.
SPHERE_ID_TO_NAME = {
    70: "Power Sphere",
    71: "Mana Sphere",
    72: "Speed Sphere",
    73: "Ability Sphere",
    74: "Fortune Sphere",
    81: "Lv. 1 Key Sphere",
    82: "Lv. 2 Key Sphere",
    83: "Lv. 3 Key Sphere",
    84: "Lv. 4 Key Sphere",
}

# Create a reverse mapping for easy lookup by name
SPHERE_NAME_TO_ID = {name: id for id, name in SPHERE_ID_TO_NAME.items()}


# IMPORTANT: Define the rules for which node content IDs require which sphere types.
# This list is ordered; the first matching rule will be applied.
# The sphere types here MUST match the values in SPHERE_ID_TO_NAME.
NODE_CONTENT_SPHERE_REQUIREMENTS = [
    # Power Spheres for Strength/Defense nodes, now including HP nodes (0x22, 0x23)
    ({0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x22, 0x23}, 70),
    # Mana Spheres for Magic/Magic Defense/MP nodes
    ({0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x24, 0x25, 0x26}, 71),
    # Speed Spheres for Agility/Evasion/Accuracy nodes
    ({0x12, 0x13, 0x14, 0x15, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21}, 72),
    # Fortune Spheres for Luck nodes
    ({0x16, 0x17, 0x18, 0x19}, 74),
    # Ability Spheres for many abilities, now including White Magic (0x4E-0x63) and Black Magic (0x64-0x76)
    ({
        *range(0x2A, 0x4E), # Delay Attack to Bribe
        *range(0x4E, 0x77), # Cure to Ultima (White and Black Magic)
        *range(0x77, 0x7F), # Pilfer Gil to Quick Pockets
    }, 73),
    # Key Spheres for Lock nodes
    ({0x27}, 81), # Lv. 1 Key Sphere
    ({0x28}, 82), # Lv. 2 Key Sphere
    ({0x00}, 83), # Lv. 3 Key Sphere
    ({0x29}, 84), # Lv. 4 Key Sphere
    # Empty Nodes usually don't require a sphere to activate (just to move past if not filled)
    ({0x01}, None), # Empty Node
]


# IMPORTANT: Add the string names of node types that represent impassable Key Sphere Locks.
# These are the nodes that will block paths until explicitly "unlocked" by a Key Sphere.
KEY_SPHERE_LOCK_TYPES = [
    "Lv. 1 Lock",
    "Lv. 2 Lock",
    "Lv. 3 Lock",
    "Lv. 4 Lock",
    # Add other types that you consider "locked" for traversal
]


# --- SphereGridNode Class ---
class SphereGridNode:
    """
    Represents a single node on the Final Fantasy X Sphere Grid.
    """
    def __init__(self, node_data: dict):
        """
        Initializes a SphereGridNode object from a dictionary of node data.

        Args:
            node_data (dict): A dictionary containing raw node information
                              from the grid_info.json file.
        """
        self._id = node_data.get("id")
        self._x = node_data.get("x")
        self._y = node_data.get("y")
        self._default_content_id = node_data.get("defaultContent")
        self._current_content_id = node_type(self._id)
        # Extract adjacent IDs, handling cases where 'adjacent' might be missing or empty
        self._adjacent_ids = [adj_info.get("adj_id") for adj_info in node_data.get("adjacent", []) if adj_info.get("adj_id") is not None]

        # --- Placeholder Attributes for external data ---
        self._unlocked_by_characters = {}    # dict: {character_id: True/False/Status}
                                             # e.g., {'Tidus': True, 'Yuna': False}
        # A flag to indicate if a Key Sphere lock on this node has been 'broken'
        # This will need to be managed externally based on game state.
        self._is_key_lock_unlocked = False

    @property
    def id(self) -> int:
        """The unique ID of the node."""
        return self._id

    @property
    def position(self) -> tuple[int, int]:
        """The (x, y) coordinates of the node on the grid."""
        return (self._x, self._y)

    @property
    def default_content_id(self) -> int:
        """The numerical ID representing the default content of the node."""
        return self._default_content_id

    @property
    def default_node_type(self) -> str:
        """
        Returns the human-readable type of the node based on its default content ID.
        Uses the NODE_TYPE_MAP.
        """
        return NODE_TYPE_MAP.get(self._default_content_id, "Unknown Type")

    @property
    def current_content_id(self) -> int:
        """The numerical ID representing the default content of the node."""
        return self._current_content_id

    @property
    def current_node_type(self) -> str:
        """
        Returns the human-readable type of the node based on its default content ID.
        Uses the NODE_TYPE_MAP.
        """
        return NODE_TYPE_MAP.get(self._current_content_id, "Unknown Type")
    
    def update_node_type(self, report:bool=False):
        self._current_content_id = node_type(self._id)
        if report:
            logger.warning(f"Node type check: {self._current_content_id}")
    
    def change_node_type(self, new_type, report:bool=False):
        self._current_content_id = new_type
        if report:
            logger.warning(f"Node type check: {self._current_content_id}")

    @property
    def adjacent_node_ids(self) -> list[int]:
        """A list of IDs of nodes directly adjacent to this node."""
        return self._adjacent_ids

    @property
    def sphere_type_unlocked_by(self) -> int | None:
        """
        The type of sphere required to unlock this node (e.g., 'Power Sphere',
        'Level 1 Key Sphere'). This is now derived from NODE_CONTENT_SPHERE_REQUIREMENTS.
        """
        # logger.warning("========= DID WE GET HERE?! (B) =========")
        for content_ids_set, sphere_type in NODE_CONTENT_SPHERE_REQUIREMENTS:
            # logger.warning(f"Type {sphere_type} unlocks nodes {content_ids_set}")
            if self.current_content_id in content_ids_set:
                return sphere_type
        return None # No matching sphere type found for this content ID

    def get_unlock_sphere_id(self) -> int | None:
        # logger.warning("========= DID WE GET HERE?! (A) =========")
        ret_val = self.sphere_type_unlocked_by
        # logger.warning(ret_val)
        return ret_val

    @property
    def unlocked_by_characters(self) -> dict:
        """
        A dictionary indicating which characters have unlocked this node.
        Keys are character identifiers (e.g., 'Tidus', 'Yuna'), values are
        status (e.g., True/False, or a more detailed status).
        This is a placeholder to be set externally (e.g., from memory reading).
        """
        results = {}
        bits = unlocked_by(node_id=self._id)

        # Define a mapping of bit values to character names
        character_map = {
            1: 'Tidus',
            2: 'Yuna',
            4: 'Auron',
            8: 'Kimahri',
            16: 'Wakka',
            32: 'Lulu',
            64: 'Rikku',
        }

        for bit_value, character_name in character_map.items():
            if (bits & bit_value):
                results[character_name] = True
            else:
                results[character_name] = False # Explicitly set to False if not unlocked

        self._unlocked_by_characters = dict(results) # Convert defaultdict back to dict for storage

        return dict(results) # Convert defaultdict back to dict for return

    def set_unlocked_status(self, character_id: str, status: bool):
        """
        Sets the unlocked status for a specific character on this node.

        Args:
            character_id (str): The identifier for the character (e.g., "Tidus").
            status (bool): True if unlocked, False otherwise.
        """
        self._unlocked_by_characters[character_id] = status

    @property
    def is_key_lock_unlocked(self) -> bool:
        """
        Indicates if a Key Sphere lock on this node has been 'broken' (e.g.,
        a Level 1 Key Sphere has been used on a Level 1 Lock node).
        This flag needs to be set externally based on game state.
        """
        return self._is_key_lock_unlocked

    @is_key_lock_unlocked.setter
    def is_key_lock_unlocked(self, status: bool):
        """Sets the status of a key sphere lock on this node."""
        self._is_key_lock_unlocked = status


    def __repr__(self):
        """String representation for debugging."""
        return (f"SphereGridNode(id={self.id}, pos={self.position}, "
                f"default_type='{self.default_node_type}', adj={self.adjacent_node_ids})")

# --- SphereGrid Class ---
class SphereGrid:
    """
    Manages the entire Final Fantasy X Sphere Grid, loading nodes
    from a JSON file and providing methods to query them.
    """
    def __init__(self, json_filepath: str):
        """
        Initializes the SphereGrid by loading node data from the specified JSON file.

        Args:
            json_filepath (str): The path to the grid_info.json file.
        """
        if not os.path.exists(json_filepath):
            raise FileNotFoundError(f"Sphere Grid JSON file not found: {json_filepath}")

        self._nodes: dict[int, SphereGridNode] = {}
        self._load_grid_data(json_filepath)

    def _load_grid_data(self, json_filepath: str):
        """
        Loads the sphere grid data from the JSON file and populates the _nodes dictionary.
        """
        try:
            with open(json_filepath, 'r', encoding='utf-8') as f:
                raw_nodes_data = json.load(f)
                # print(raw_nodes_data)
                # print("---")
                # print("---")

            for node_data in raw_nodes_data:
                # print(node_data)
                # print("---")
                node = SphereGridNode(node_data)
                # print("-+-")
                self._nodes[node.id] = node
        except json.JSONDecodeError as e:
            logger.debug(f"Error decoding JSON from {json_filepath}: {e}")
            self._nodes = {} # Ensure nodes is empty on error
        except Exception as e:
            logger.debug(f"An unexpected error occurred while loading grid data: {e}")
            self._nodes = {}

    def get_node(self, node_id: int) -> SphereGridNode | None:
        """
        Retrieves a SphereGridNode object by its ID.

        Args:
            node_id (int): The ID of the node to retrieve.

        Returns:
            SphereGridNode: The SphereGridNode object if found, None otherwise.
        """
        return self._nodes.get(node_id)

    def get_node_position(self, node_id: int) -> tuple[int, int] | None:
        """
        Returns the (x, y) coordinates of a specific node.

        Args:
            node_id (int): The ID of the node.

        Returns:
            tuple[int, int]: (x, y) coordinates if node exists, None otherwise.
        """
        node = self.get_node(node_id)
        return node.position if node else None

    def get_node_default_type(self, node_id: int) -> str | None:
        """
        Returns the human-readable default type of the node (e.g., "Strength +1").

        Args:
            node_id (int): The ID of the node.

        Returns:
            str: The default type string if node exists, None otherwise.
        """
        node = self.get_node(node_id)
        return node.default_node_type if node else None

    def get_node_unlock_sphere_type(self, node_id: int) -> int | None:
        """
        Returns the type of sphere required to unlock the node.
        This relies on the `sphere_type_unlocked_by` property of the node,
        which is now derived from NODE_CONTENT_SPHERE_REQUIREMENTS.

        Args:
            node_id (int): The ID of the node.

        Returns:
            str: The sphere type string if node exists and info is available, None otherwise.
        """
        node = self.get_node(node_id)
        return node.sphere_type_unlocked_by if node else None

    def get_node_unlocked_by(self, node_id: int) -> dict | None:
        """
        Returns a dictionary showing which characters have unlocked the node.
        This relies on the `unlocked_by_characters` attribute of the node,
        which needs to be set externally (e.g., from memory reading).

        Args:
            node_id (int): The ID of the node.

        Returns:
            dict: A dictionary of character unlock statuses if node exists, None otherwise.
        """
        node = self.get_node(node_id)
        return node.unlocked_by_characters if node else None

    def get_adjacent_nodes_ids(self, node_id: int) -> list[int] | None:
        """
        Returns a list of IDs of nodes adjacent to the given node.

        Args:
            node_id (int): The ID of the node.

        Returns:
            list[int]: A list of adjacent node IDs if node exists, None otherwise.
        """
        node = self.get_node(node_id)
        return node.adjacent_node_ids if node else None

    def get_all_nodes(self) -> dict[int, SphereGridNode]:
        """
        Returns the entire dictionary of SphereGridNode objects.
        """
        return self._nodes

    def _is_node_traversable(self, node_id: int) -> bool:
        """
        Internal helper to determine if a node is traversable.
        A node is considered traversable if it's not a Key Sphere Lock node
        that hasn't been explicitly unlocked.

        Args:
            node_id (int): The ID of the node to check.

        Returns:
            bool: True if the node is traversable, False otherwise.
        """
        node = self.get_node(node_id)
        if not node:
            return False # Node doesn't exist

        # If the node's default type is in the list of KEY_SPHERE_LOCK_TYPES
        # AND its 'is_key_lock_unlocked' flag is False, then it's not traversable.
        if node.current_node_type in KEY_SPHERE_LOCK_TYPES and not node.is_key_lock_unlocked:
            return False
        return True

    def find_shortest_path(self, start_node_id: int, target_node_id: int) -> list[int] | None:
        logger.debug("Finding shortest path.")
        """
        Finds the shortest path between two nodes on the Sphere Grid using BFS,
        taking into account locked (impassable) nodes.

        Args:
            start_node_id (int): The ID of the starting node.
            target_node_id (int): The ID of the target node.

        Returns:
            list[int] | None: A list of node IDs representing the shortest path
                              from start to target, or None if no path exists.
        """
        logger.debug("Mark A")
        if start_node_id == target_node_id:
            logger.debug("Start node is sufficient.")
            return [start_node_id]

        logger.debug(f"Mark B: {start_node_id} | {target_node_id}")
        start_node = self.get_node(start_node_id)
        target_node = self.get_node(target_node_id)
        logger.debug("Mark C")

        if not start_node or not target_node:
            logger.debug(f"Error: Start node {start_node_id} or target node {target_node_id} not found.")
            return None
        
        logger.debug("Mark D")
        if not self._is_node_traversable(start_node_id):
            logger.debug(f"Error: Start node {start_node_id} is not traversable.")
            return None

        logger.debug("Mark E")
        queue = deque([(start_node_id, [start_node_id])]) # (current_node, path_so_far)
        visited = {start_node_id}

        logger.debug("Mark F")
        while queue:
            current_node_id, path = queue.popleft()

            if current_node_id == target_node_id:
                logger.debug(f"Path chosen: {path}")
                return path

            current_node = self.get_node(current_node_id)
            if current_node:
                for neighbor_id in current_node.adjacent_node_ids:
                    if neighbor_id not in visited and self._is_node_traversable(neighbor_id):
                        visited.add(neighbor_id)
                        new_path = list(path) # Create a copy to avoid modifying original path
                        new_path.append(neighbor_id)
                        queue.append((neighbor_id, new_path))
        logger.debug("No path found.")
        return None # No path found

    def find_nearest_node_of_type(
            self, start_node_id: int, 
            target_node_type: str,
            path_nodes: [] # This parameter seems unused in your original function, consider if you need it.
        ) -> tuple[int | None, int | None]:
        logger.debug(f"Checking specific node, {start_node_id}, {target_node_type}, {path_nodes}")
        """
        Finds the nearest node of a specific type from a starting node using BFS,
        taking into account locked (impassable) nodes.

        Args:
            start_node_id (int): The ID of the starting node.
            target_node_type (str): The human-readable type of node to search for
                                    (e.g., "Empty Node", "Strength (1 pt)", "Lv. 1 Lock").

        Returns:
            tuple[SphereGridNode | None, int | None]: A tuple containing the nearest
            SphereGridNode object and its distance from the start node, or (None, None)
            if no node of the target type is found or the start node is invalid/impassable.
        """
        start_node = self.get_node(start_node_id)
        if not start_node:
            logger.debug(f"Error: Start node {start_node_id} not found.")
            logger.debug("return1")
            return None, None
        
        if not self._is_node_traversable(start_node_id):
            logger.debug(f"Error: Start node {start_node_id} is not traversable for finding nearest node of type.")
            logger.debug("return2")
            return None, None

        # Check if the start node itself is the target type
        if start_node.current_node_type == target_node_type:
            logger.debug("return3")
            return start_node_id, 0

        queue = deque([(start_node_id, 0)]) # (current_node_id, distance)
        visited = {start_node_id}
        impassable = set() # Changed from {999} to an empty set to be more general. 
                           # Nodes will be added if _is_node_traversable returns False.

        while queue:
            report = False
            current_node_id, distance = queue.popleft()
            current_node = self.get_node(current_node_id)
            # if current_node_id in path_nodes:
                # logger.manip(f"Check current node: {current_node_id})")
                # report = True
                # pass

            if current_node: # Ensure current_node exists
                if report:
                    logger.manip(f"Node {current_node_id} exists")
                if target_node_type == "Luck_Up":
                    if self.get_node_unlock_sphere_type(current_node_id) == 74:
                        return current_node_id, distance
                for neighbor_id in current_node.adjacent_node_ids:
                    if report:
                        logger.manip(f"Neighbor Node {neighbor_id}")
                    if neighbor_id not in visited:
                        if report:
                            logger.manip(f"Neighbor Node {neighbor_id} not yet visited")
                        visited.add(neighbor_id)
                        if not self._is_node_traversable(neighbor_id):
                            if report:
                                logger.manip(f"Neighbor Node {neighbor_id} not traversable")
                            impassable.add(neighbor_id)
                            # continue # Skip processing this neighbor if it's impassable

                        neighbor_node = self.get_node(neighbor_id)
                        if neighbor_node and neighbor_node.current_node_type == target_node_type:
                            if report:
                                logger.manip(f"Neighbor Node {neighbor_id} is the correct type")
                            if path_nodes is None or current_node_id in path_nodes:
                                logger.debug("return4")
                                return current_node_id, distance
                        else:
                            if report:
                                logger.manip(f"Neighbor Node {neighbor_id} is NOT the correct type")
                        
                        # Only add to queue if it's not impassable
                        if neighbor_id not in impassable:
                            queue.append((neighbor_id, distance + 1))
        return None, None # No node of target type found

    def find_path_to_nearest_dead_end(
        self, start_node_id: int, character_id: str, MAX_DISTANCE:int = 8
    ) -> list[int]:
        from collections import deque
        """
        Finds the shortest path (list of node IDs) from start_node_id to the 
        nearest unactivated dead-end node, limited to a maximum path length of 8.

        Args:
            start_node_id (int): The ID of the starting node.
            character_id (str): The ID of the current character.

        Returns:
            list[int]: The shortest path as a list of node IDs (including start and end), 
            or an empty list if no unactivated dead-end node is found within 8 steps.
        """
        character_name = name_from_number(character_id)
        if character_name == "Unknown":
            logger.error(f"Invalid character ID provided: {character_id}. Cannot determine character name.")
            return []

        actual_start_node_id = self.character_at_node(character_id)
        if actual_start_node_id is None:
            logger.error(f"Could not determine start node ID for character ID {character_id}.")
            return []
        
        start_node_id = actual_start_node_id

        logger.debug(f"Searching for shortest path to nearest unactivated dead end from {start_node_id} (character {character_name}) with max distance of {MAX_DISTANCE}.")

        # --- Dead-End Node Identification ---
        # This setup remains the same: identify all dead-end nodes in the grid
        all_nodes = self.get_all_nodes()
        dead_end_nodes_ids = set()
        accounted_for = []

        for node_id in all_nodes:
            current_node = self.get_node(node_id)
            if not current_node: continue
            
            # 1. Degree 1 check
            if len(current_node.adjacent_node_ids) == 1:
                dead_end_nodes_ids.add(node_id)
            # 2. Degree 2 pair check (cul-de-sac)
            # N has two neighbors, N1 and N2.
            elif (
                len(current_node.adjacent_node_ids) == 2 and
                not node_id in accounted_for
            ):
                N1, N2 = current_node.adjacent_node_ids
                
                # Check N1: Is N1 also Degree 2?
                N1_node = self.get_node(N1)
                N2_node = self.get_node(N2)
                if N1_node and len(N1_node.adjacent_node_ids) == 2:
                    if (
                        node_id in N1_node.adjacent_node_ids and
                        N2 in N1_node.adjacent_node_ids
                    ):
                        dead_end_nodes_ids.add(node_id)
                        accounted_for.append(N1)
                elif N2_node and len(N2_node.adjacent_node_ids) == 2:
                    if (
                        node_id in N2_node.adjacent_node_ids and
                        N1 in N2_node.adjacent_node_ids
                    ):
                        dead_end_nodes_ids.add(node_id)
                        accounted_for.append(N2)
        
        start_node = self.get_node(start_node_id)
        if not start_node or not self._is_node_traversable(start_node_id):
            logger.debug(f"Error: Start node {start_node_id} is invalid or not traversable.")
            return []

        # Optimization: Check if the start node itself is an unactivated dead end
        start_node.update_node_type()
        start_node.unlocked_by_characters
        if start_node_id in dead_end_nodes_ids and \
           not start_node.unlocked_by_characters.get(character_name, False):
            logger.debug(f"Start node {start_node_id} is an unactivated dead end.")
            return [start_node_id] # Path is just the node itself

        # Begin BFS: We track the full path to the current node
        # queue = [(current_node_id, distance, path_list)]
        queue = deque([(start_node_id, 0, [start_node_id])])
        visited = {start_node_id}

        while queue:
            current_node_id, distance, path = queue.popleft()
            current_node = self.get_node(current_node_id)

            if not current_node:
                continue

            # Skip processing neighbors if we are already at the distance limit
            if distance >= MAX_DISTANCE:
                continue

            for neighbor_id in current_node.adjacent_node_ids:
                if neighbor_id not in visited:
                    
                    new_distance = distance + 1
                    
                    # If the next step exceeds the 8-node limit, skip the neighbor
                    if new_distance > MAX_DISTANCE:
                        continue 
                        
                    visited.add(neighbor_id)
                    neighbor_node = self.get_node(neighbor_id)
                    
                    if not neighbor_node:
                        logger.warning(f"Neighbor node {neighbor_id} not found, skipping.")
                        continue

                    neighbor_node.update_node_type()
                    neighbor_node.unlocked_by_characters

                    # Check if the neighbor is traversable
                    if not self._is_node_traversable(neighbor_id):
                        logger.debug(f"Neighbor {neighbor_id} is impassable (locked), stopping path.")
                        # Do NOT queue impassable nodes, but keep track of visited to prevent re-checking
                        continue

                    new_path = path + [neighbor_id]

                    # CHECK FOR THE TARGET: Unactivated Dead End
                    if neighbor_id in dead_end_nodes_ids and \
                       not neighbor_node.unlocked_by_characters.get(character_name, False):
                        
                        logger.debug(f"Found nearest unactivated dead end: {neighbor_id} at distance {new_distance}. Path found.")
                        # The path includes the dead end node
                        return new_path
                        
                    # Queue the neighbor for the next iteration
                    queue.append((neighbor_id, new_distance, new_path))
        
        logger.debug(f"No unactivated dead end found within {MAX_DISTANCE} steps from {start_node_id}. Returning empty path.")
        return []

    def _resolve_sphere_identifier(self, sphere_input: Union[int, str]) -> str | None:
        """
        Internal helper to resolve a sphere input (ID or name) to its canonical string name.

        Args:
            sphere_input (Union[int, str]): The sphere's ID (e.g., 70) or name (e.g., "Power Sphere").

        Returns:
            str | None: The canonical string name of the sphere if found, None otherwise.
        """
        if isinstance(sphere_input, int):
            return SPHERE_ID_TO_NAME.get(sphere_input)
        elif isinstance(sphere_input, str):
            # Check if the string is a direct match
            if sphere_input in SPHERE_NAME_TO_ID:
                return sphere_input
            # Try a case-insensitive search if direct match fails
            for name in SPHERE_NAME_TO_ID:
                if name.lower() == sphere_input.lower():
                    return name
            return None # Not found by direct or case-insensitive name
        else:
            logger.debug(f"Invalid sphere input type: {type(sphere_input)}. Expected int or str.")
            return None

    def get_nodes_requiring_sphere(self, sphere_identifier: Union[int, str]) -> list[SphereGridNode]:
        """
        Finds all nodes on the Sphere Grid that require a specific type of sphere
        to unlock/activate them.

        Args:
            sphere_identifier (Union[int, str]): The ID (e.g., 70) or name (e.g., "Power Sphere")
                                                of the sphere type to search for.

        Returns:
            list[SphereGridNode]: A list of SphereGridNode objects that require the specified sphere.
                                 Returns an empty list if no matching sphere type is found or
                                 no nodes require that sphere.
        """
        resolved_sphere_name = self._resolve_sphere_identifier(sphere_identifier)

        if not resolved_sphere_name:
            logger.debug(f"Could not resolve sphere identifier: '{sphere_identifier}' to a known sphere type.")
            return []

        matching_nodes = []
        for node_id in self._nodes:
            node = self.get_node(node_id)
            if node and node.sphere_type_unlocked_by == sphere_identifier:
                matching_nodes.append(node)
        return matching_nodes

    def find_nearest_unlocked_node_for_character(self, start_node_id: int, character_id: str) -> tuple[SphereGridNode | None, int | None]:
        return self.find_nearest_multi_unlock_for_character(start_node_id=start_node_id, character_id=character_id, min_unlocks=1)

    def find_nearest_multi_unlock_for_character(
            self, 
            start_node_id: int, 
            character_name: str,
            min_unlocks:int,
            path_nodes,
            include_empty:bool
        ) -> tuple[SphereGridNode | None, int | None]:
        logger.debug(f"Checking multi-unlock, {character_name}, {min_unlocks}, {include_empty}, {path_nodes}")
        # memory.main.wait_frames(60)
        """
        Finds the nearest node on the Sphere Grid that has not yet been unlocked
        by the specified character, considering traversable paths.

        Args:
            start_node_id (int): The ID of the starting node (current character position).
            character_id (str): The identifier for the character (e.g., "Tidus", "Yuna").

        Returns:
            tuple[SphereGridNode | None, int | None]: A tuple containing the nearest
            SphereGridNode object that the character has not unlocked, and the distance
            (number of steps) to reach it. Returns (None, None) if no such node is found
            or the starting node is invalid/impassable.
        """
        start_node = self.get_node(start_node_id)
        if not start_node:
            logger.debug(f"Error: Start node {start_node_id} not found.")
            return None, None

        if not self._is_node_traversable(start_node_id):
            logger.debug(f"Error: Start node {start_node_id} is not traversable for finding unlocked node.")
            return None, None

        # Check if the start node itself is not unlocked by the character
        # This covers cases where the character is standing on an unactivated node
        # if not start_node.unlocked_by_characters.get(character_id, False):
        #     logger.debug("Single - current node is candidate.")
        #     return start_node_id, 0

        queue = deque([(start_node_id, 0)]) # (current_node_id, distance)
        visited = {start_node_id}

        while queue:
            current_node_id, distance = queue.popleft()
            current_node = self.get_node(current_node_id)
            report = current_node_id in [999]
            if report:
                logger.warning(f"Queue length({min_unlocks}): {len(queue)}")

            if current_node:
                if report:
                    logger.warning(f"Unlockables: {self.count_unlockables(current_node_id, character_name)}")
                if self.count_unlockables(current_node_id, character_name, include_empty=include_empty) >= min_unlocks:
                    # logger.debug(path_nodes)
                    if path_nodes == None or current_node_id in path_nodes:
                        if report:
                            logger.info(f"Target identified for min {min_unlocks}: {current_node_id}")
                        return current_node_id, distance
                for neighbor_id in current_node.adjacent_node_ids:
                    # Only traverse to nodes that are generally traversable (not blocked by key locks)
                    if neighbor_id not in visited and self._is_node_traversable(neighbor_id):
                        visited.add(neighbor_id)
                        queue.append((neighbor_id, distance + 1))
        return None, None # No unlocked node found for the character

    def count_nodes_of_type(self, node_type):
        # Primarily used for the level locks
        total_count = 0
        for node_id in self._nodes:
            node = self.get_node(node_id)
            # logger.manip(f"{node_id}: {node.current_node_type}")
            if node.current_node_type == node_type:
                total_count += 1
        # memory.main.wait_frames(300)
        return total_count

    def character_at_node(self, actor_id):
        return char_current_node(actor_id)
    
    def count_unlockables(self, node_id, char_name, include_empty):
        # Use the "report" array to specify nodes we want to check additional details on.
        report = node_id in [999]
        if report:
            logger.info(char_name)
        unlockable_count = 0
        current_node = self.get_node(node_id)
        if report:
            # logger.manip(f"c-{node_id}: {current_node.unlocked_by_characters.get(char_name, False)}")
            logger.manip(f"c-{node_id}: {current_node.get_unlock_sphere_id()}")
        
        # current_node.update_node_type()
        if current_node and not current_node.current_content_id in [0x0,0x27,0x28,0x29]:
            if not current_node.unlocked_by_characters.get(char_name, False):
                if current_node.current_content_id == 0x01 and include_empty:
                    unlockable_count += 1
                elif memory.main.get_item_slot(current_node.get_unlock_sphere_id()) != 255:
                    unlockable_count += 1

        if current_node:
            for neighbor_id in current_node.adjacent_node_ids:
                # Only traverse to nodes that are generally traversable (not blocked by key locks)
                neighbor_node = self.get_node(neighbor_id)
                if report:
                    # logger.manip(f"n-{neighbor_id}: {current_node.unlocked_by_characters.get(char_name, False)}")
                    logger.manip(f"n-{neighbor_id}: {neighbor_node.get_unlock_sphere_id()}")
                # neighbor_node.update_node_type()
                if neighbor_node and not neighbor_node.current_content_id in [0x0,0x27,0x28,0x29]:
                    # Check if this neighbor node is *not* unlocked by the character
                    if neighbor_node.current_content_id == 0x01 and include_empty:
                        unlockable_count += 1
                    elif not neighbor_node.unlocked_by_characters.get(char_name, False):
                        if memory.main.get_item_slot(neighbor_node.get_unlock_sphere_id()) != 255:
                            unlockable_count += 1
        return unlockable_count
    
    def count_all_unlockables(self, actor_id) -> int:
        total = 860
        change_nodes = [0x0,0x01,0x27,0x28,0x29,0x16,0x17,0x18,0x19]
        for i in range(len(self.get_all_nodes())):
            current_node = self.get_node(i)
            if current_node.unlocked_by_characters.get(name_from_number(actor_id), True):
                total -= 1
        logger.debug(f"Actor {actor_id} has {total} remaining nodes to unlock.")
        return total
    

    def check_all_unlocks(self):
        # No longer used. Unlocks seems to lag behind by one action for some reason.
        for node_id in self._nodes:
            current_node = self.get_node(node_id)
            current_node.unlocked_by_characters
            current_node.update_node_type()
    
    def check_all_node_types(self):
        for node_id in self._nodes:
            current_node = self.get_node(node_id)
            current_node.update_node_type()

    def get_node_count(self, target_node_type):
        total = 0
        for node_id in self._nodes:
            current_node = self.get_node(node_id)
            if current_node.current_node_type == target_node_type:
                total += 1
        return total


def name_from_number(char_num):
    if char_num == 0:
        return "Tidus"
    if char_num == 1:
        return "Yuna"
    if char_num == 2:
        return "Auron"
    if char_num == 3:
        return "Kimahri"
    if char_num == 4:
        return "Wakka"
    if char_num == 5:
        return "Lulu"
    if char_num == 6:
        return "Rikku"
    if char_num == 9:
        return "Killing_Blow"