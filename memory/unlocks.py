import logging
from enum import Enum

from memory.main import read_bytes_external, base_value
#from players import Player

logger = logging.getLogger(__name__)


def od_mode_unlocks(char_index):
    key = 0xD320BC + (0x94 * char_index)
    ret_array = [1]  # Stoic is auto-learned for all characters.
    for i in range(17):
        if i != 2:
            if read_bytes_external(key+(2*i), 2) == 0:
                ret_array.append(1)
            else:
                ret_array.append(0)
    logger.manip(f"Unlocks for {char_index}: {ret_array}")
    # print(f"Node type: {ret_val}")
    return ret_array

def od_mode_pos(char_index, od_mode_id) -> int | None:
    check_array = []
    pos_array = od_mode_unlocks(char_index)
    if pos_array[od_mode_id] != 1:
        return None
    final_pos = 0
    if od_mode_id != 0:
        for i in range(0, od_mode_id):
            check_array.append(pos_array[i])
            if pos_array[i] == 1:
                final_pos += 1
    logger.warning(f"OD Mode position found: {final_pos}")
    logger.debug(f"Check array: {check_array}")
    return final_pos

def od_mode_current(char_index) -> int:
    key = 0xD32094 + (0x94 * char_index)

    true_mode = read_bytes_external(key, 1)
    if true_mode == 2:
        return 0 # aVIna will always treat Stoic as position zero
    elif true_mode < 2:
        return true_mode + 1
    else:
        return true_mode

CHARACTER_BLOCK_START_OFFSET = 0xD32000

# This is the consistent size of each character's skill data block.
# Calculated as (Yuna's Aim offset - Tidus's Aim offset) = 0xD32131 - 0xD3209D = 0x94.
CHARACTER_BLOCK_STRIDE = 0x94

# Character index mapping for convenience
CHARACTER_NAME_TO_INDEX = {
    "Tidus": 0,
    "Yuna": 1,
    "Auron": 2,
    "Kimahri": 3,
    "Wakka": 4,
    "Lulu": 5,
    "Rikku": 6
}

# --- Skill Definitions (Migrated from XML - Single Source with corrections) ---
SKILL_DEFINITIONS = [
    {"name": "Aim", "type": "Special", "offset_from_block": 0x9D, "bit": 3},
    {"name": "Armor Break", "type": "Skill", "offset_from_block": 0x9C, "bit": 2},
    {"name": "Auto-Life", "type": "White Magic", "offset_from_block": 0xA2, "bit": 0},
    {"name": "Bio", "type": "Black Magic", "offset_from_block": 0xA3, "bit": 5},
    {"name": "Blizzaga", "type": "Black Magic", "offset_from_block": 0xA3, "bit": 2},
    {"name": "Blizzara", "type": "Black Magic", "offset_from_block": 0xA2, "bit": 6},
    {"name": "Blizzard", "type": "Black Magic", "offset_from_block": 0xA2, "bit": 1},
    {"name": "Bribe", "type": "Special", "offset_from_block": 0x9F, "bit": 2},
    {"name": "Cheer", "type": "Special", "offset_from_block": 0x9D, "bit": 2},
    {"name": "Copycat", "type": "Special", "offset_from_block": 0x9F, "bit": 0},
    {"name": "Cura", "type": "White Magic", "offset_from_block": 0x9F, "bit": 4},
    {"name": "Curaga", "type": "White Magic", "offset_from_block": 0x9F, "bit": 5},
    {"name": "Cure", "type": "White Magic", "offset_from_block": 0x9F, "bit": 3},
    {"name": "Dark Attack", "type": "Skill", "offset_from_block": 0x9B, "bit": 2},
    {"name": "Dark Buster", "type": "Skill", "offset_from_block": 0x9B, "bit": 6},
    {"name": "Death", "type": "Black Magic", "offset_from_block": 0xA3, "bit": 7},
    {"name": "Delay Attack", "type": "Skill", "offset_from_block": 0x9A, "bit": 6},
    {"name": "Delay Buster", "type": "Skill", "offset_from_block": 0x9A, "bit": 7},
    {"name": "Demi", "type": "Black Magic", "offset_from_block": 0xA3, "bit": 6},
    {"name": "Dispel", "type": "White Magic", "offset_from_block": 0xA1, "bit": 5},
    {"name": "Doublecast", "type": "Special", "offset_from_block": 0x9F, "bit": 1},
    {"name": "Drain", "type": "Black Magic", "offset_from_block": 0xA4, "bit": 0},
    {"name": "Entrust", "type": "Special", "offset_from_block": 0x9E, "bit": 7},
    {"name": "Esuna", "type": "White Magic", "offset_from_block": 0xA0, "bit": 3},
    {"name": "Extract Ability", "type": "Skill", "offset_from_block": 0xA5, "bit": 5},
    {"name": "Extract Mana", "type": "Skill", "offset_from_block": 0xA5, "bit": 3},
    {"name": "Extract Power", "type": "Skill", "offset_from_block": 0xA5, "bit": 2},
    {"name": "Extract Speed", "type": "Skill", "offset_from_block": 0xA5, "bit": 4},
    {"name": "Fira", "type": "Black Magic", "offset_from_block": 0xA2, "bit": 5},
    {"name": "Firaga", "type": "Black Magic", "offset_from_block": 0xA3, "bit": 1},
    {"name": "Fire", "type": "Black Magic", "offset_from_block": 0xA2, "bit": 2},
    {"name": "Flare", "type": "Black Magic", "offset_from_block": 0xA4, "bit": 2},
    {"name": "Flee", "type": "Special", "offset_from_block": 0x9D, "bit": 0}, # Type changed to Special
    {"name": "Focus", "type": "Special", "offset_from_block": 0x9D, "bit": 4}, # Type changed to Special
    {"name": "Full Break", "type": "Skill", "offset_from_block": 0xA5, "bit": 1},
    {"name": "Full-Life", "type": "White Magic", "offset_from_block": 0xA0, "bit": 5},
    {"name": "Guard", "type": "Special", "offset_from_block": 0x9E, "bit": 2}, # Type changed to Special
    {"name": "Haste", "type": "White Magic", "offset_from_block": 0xA0, "bit": 6},
    {"name": "Hastega", "type": "White Magic", "offset_from_block": 0xA0, "bit": 7},
    {"name": "Holy", "type": "White Magic", "offset_from_block": 0xA1, "bit": 7},
    {"name": "Jinx", "type": "Special", "offset_from_block": 0x9D, "bit": 7}, # Type changed to Special
    {"name": "Lancet", "type": "Special", "offset_from_block": 0x9E, "bit": 0},
    {"name": "Life", "type": "White Magic", "offset_from_block": 0xA0, "bit": 4},
    {"name": "Luck", "type": "Special", "offset_from_block": 0x9D, "bit": 6}, # Type changed to Special
    {"name": "Magic Break", "type": "Skill", "offset_from_block": 0x9C, "bit": 1},
    {"name": "Mental Break", "type": "Skill", "offset_from_block": 0x9C, "bit": 3},
    {"name": "Mug", "type": "Skill", "offset_from_block": 0x9C, "bit": 4}, # Type changed to Skill
    {"name": "Nab Gil", "type": "Skill", "offset_from_block": 0xA5, "bit": 6}, # Type changed to Skill
    {"name": "NulBlaze", "type": "White Magic", "offset_from_block": 0x9F, "bit": 7},
    {"name": "NulFrost", "type": "White Magic", "offset_from_block": 0x9F, "bit": 6},
    {"name": "NulShock", "type": "White Magic", "offset_from_block": 0xA0, "bit": 0},
    {"name": "NulTide", "type": "White Magic", "offset_from_block": 0xA0, "bit": 1},
    {"name": "Osmose", "type": "Black Magic", "offset_from_block": 0xA4, "bit": 1},
    {"name": "Pilfer Gil", "type": "Special", "offset_from_block": 0xA5, "bit": 0},
    {"name": "Power Break", "type": "Skill", "offset_from_block": 0x9C, "bit": 0},
    {"name": "Pray", "type": "Special", "offset_from_block": 0x9D, "bit": 1}, # Type changed to Special
    {"name": "Protect", "type": "White Magic", "offset_from_block": 0xA1, "bit": 3},
    {"name": "Provoke", "type": "Special", "offset_from_block": 0x9E, "bit": 6}, # Type changed to Special
    {"name": "Quick Hit", "type": "Skill", "offset_from_block": 0x9C, "bit": 5},
    {"name": "Quick pockets", "type": "Special", "offset_from_block": 0xA5, "bit": 7},
    {"name": "Reflect", "type": "White Magic", "offset_from_block": 0xA1, "bit": 4},
    {"name": "Reflex", "type": "Special", "offset_from_block": 0x9D, "bit": 5}, # Name and Type changed
    {"name": "Regen", "type": "White Magic", "offset_from_block": 0xA1, "bit": 6},
    {"name": "Scan", "type": "White Magic", "offset_from_block": 0xA0, "bit": 2}, # Type changed to White Magic
    {"name": "Sentinal", "type": "Special", "offset_from_block": 0x9E, "bit": 3}, # Name and Type changed
    {"name": "Shell", "type": "White Magic", "offset_from_block": 0xA1, "bit": 2},
    {"name": "Silence Attack", "type": "Skill", "offset_from_block": 0x9B, "bit": 1},
    {"name": "Silence Buster", "type": "Skill", "offset_from_block": 0x9B, "bit": 5},
    {"name": "Sleep Attack", "type": "Skill", "offset_from_block": 0x9B, "bit": 0},
    {"name": "Sleep Buster", "type": "Skill", "offset_from_block": 0x9B, "bit": 4},
    {"name": "Slow", "type": "White Magic", "offset_from_block": 0xA1, "bit": 0},
    {"name": "Slowga", "type": "White Magic", "offset_from_block": 0xA1, "bit": 1},
    {"name": "Spare Change", "type": "Special", "offset_from_block": 0x9E, "bit": 4},
    {"name": "Steal", "type": "Special", "offset_from_block": 0x9C, "bit": 6},
    {"name": "Threaten", "type": "Special", "offset_from_block": 0x9E, "bit": 5}, # Name and Type changed
    {"name": "Thundaga", "type": "Black Magic", "offset_from_block": 0xA3, "bit": 3},
    {"name": "Thundara", "type": "Black Magic", "offset_from_block": 0xA2, "bit": 7},
    {"name": "Thunder", "type": "Black Magic", "offset_from_block": 0xA2, "bit": 3},
    {"name": "Triple Foul", "type": "Skill", "offset_from_block": 0x9B, "bit": 7},
    {"name": "Ultima", "type": "Black Magic", "offset_from_block": 0xA4, "bit": 3},
    {"name": "Use", "type": "Special", "offset_from_block": 0x9C, "bit": 7},
    {"name": "Water", "type": "Black Magic", "offset_from_block": 0xA2, "bit": 4},
    {"name": "Watera", "type": "Black Magic", "offset_from_block": 0xA3, "bit": 0},
    {"name": "Waterga", "type": "Black Magic", "offset_from_block": 0xA3, "bit": 4},
    {"name": "Zombie Attack", "type": "Skill", "offset_from_block": 0x9B, "bit": 3}
]

# --- Custom In-Game Menu Orders (UPDATED WITH YOUR PROVIDED LIST) ---
CUSTOM_MENU_ORDER = {
    "White Magic": [
        "Cure", "Cura", "Curaga", "Scan", "NulBlaze", "NulShock", "NulTide", "NulFrost",
        "Esuna", "Life", "Full-Life", "Haste", "Hastega", "Slow", "Slowga",
        "Shell", "Protect", "Reflect", "Dispel", "Regen", "Holy", "Auto-Life"
    ],
    "Black Magic": [
        "Fire", "Thunder", "Water", "Blizzard", "Fira", "Thundara", "Watera", "Blizzara",
        "Firaga", "Thundaga", "Waterga", "Blizzaga", "Bio", "Demi", "Death", "Drain", "Osmose",
        "Flare", "Ultima"
    ],
    "Skill": [
        "Sleep Attack", "Silence Attack", "Dark Attack",
        "Sleep Buster", "Silence Buster", "Dark Buster",
        "Zombie Attack", "Triple Foul", "Delay Attack", "Delay Buster",
        "Power Break", "Magic Break", "Armor Break", "Mental Break",
        "Extract Power", "Extract Mana", "Extract Speed", "Extract Ability",
        "Full Break", "Mug", "Nab Gil", "Quick Hit"
    ],
    "Special": [
        "Flee", "Steal", "Use", "Pray", "Cheer", "Aim",
        "Focus", "Reflex", "Luck", "Jinx", "Lancet", "Guard",
        "Sentinal", "Spare Change", "Threaten", "Provoke",
        "Entrust", "Copycat", "Pilfer Gil", "Quick pockets",
        "Doublecast", "Bribe"
    ]
}

# --- Initialize PRE_SORTED_SKILLS_BY_TYPE based on CUSTOM_MENU_ORDER ---
# This block runs once when the script is loaded.
PRE_SORTED_SKILLS_BY_TYPE = {}
for skill_type, ordered_names in CUSTOM_MENU_ORDER.items():
    # Create a temporary dictionary to map names to skill full info for easy lookup
    skill_info_by_name = {skill["name"]: skill for skill in SKILL_DEFINITIONS if skill["type"] == skill_type}

    # Populate the pre-sorted list using the custom order
    sorted_list = []
    for name in ordered_names:
        if name in skill_info_by_name:
            sorted_list.append(skill_info_by_name[name])
        else:
            if logger:
                logger.warning(f"Skill '{name}' defined in CUSTOM_MENU_ORDER for '{skill_type}' "
                               f"but not found or type mismatch in SKILL_DEFINITIONS. Skipping.")
    PRE_SORTED_SKILLS_BY_TYPE[skill_type] = sorted_list


# --- Core Logic for Memory Reading ---
def _read_byte_from_memory(address):
    return read_bytes_external(address,1)
    """
    Helper function to read a single byte from memory.
    This function depends on your 'process' object.
    """
    global process
    if not process:
        if logger:
            logger.error("Memory process object is not initialized.")
        return 0 # Return 0 if process is not available

    try:
        # Assuming process.read_bytes reads a byte and returns an integer
        return process.read_bytes(address, 1)
    except Exception as e:
        if logger:
            logger.error(f"Error reading memory at 0x{address:X}: {e}")
        return 0 # Return 0 on error, implying skill is not unlocked or unreadable


# --- Function 1: Check if a given character has a given ability unlocked ---
def has_ability_unlocked(character_index: int, ability_name: str) -> bool:
    """
    Checks if a specific character (by index) has a specific ability unlocked.

    Args:
        character_index (int): The 0-indexed position of the character (e.g., 0 for Tidus, 1 for Yuna).
        ability_name (str): The name of the ability to check (e.g., "Fire", "Steal").

    Returns:
        bool: True if the ability is unlocked for the character, False otherwise.
    """

    # Find the ability in our predefined list
    ability_info = next((skill for skill in SKILL_DEFINITIONS if skill["name"] == ability_name), None)

    if ability_info is None:
        if logger:
            logger.warning(f"Ability '{ability_name}' not found in SKILL_DEFINITIONS.")
        return False

    # Calculate the exact memory address for the ability
    full_address = (character_index * 0x94) + ability_info["offset_from_block"]

    byte_value = _read_byte_from_memory(full_address)
    is_unlocked = bool((byte_value >> ability_info["bit"]) & 1)
    return is_unlocked

# --- Function 2: Track a given ability's position within its grouping ---
def get_unlocked_abilities_by_type(character_index: int, report:bool=True) -> dict:
    """
    Retrieves all unlocked abilities for a given character (by index), sorted by type and then
    according to the CUSTOM_MENU_ORDER, and includes their display position within their group.
    Locked abilities are removed.

    Args:
        character_index (int): The 0-indexed position of the character (e.g., 0 for Tidus, 1 for Yuna).

    Returns:
        dict: A dictionary where keys are skill types (e.g., "White Magic", "Skill")
              and values are lists of dictionaries. Each inner dictionary contains
              "name" and "position" (its 0-indexed position within its sorted, unlocked group).
              Example: {"White Magic": [{"name": "Cure", "position": 0}, ...]}
    """
    unlocked_and_positioned_abilities = {
        "White Magic": [],
        "Black Magic": [],
        "Skill": [],
        "Special": []
    }

    # Iterate through each skill type and its pre-sorted skills
    for skill_type, skills_in_category in PRE_SORTED_SKILLS_BY_TYPE.items():
        current_unlocked_list = [] # List to hold unlocked skills for this category

        for skill in skills_in_category:
            # Calculate the full memory offset from FFX.exe for the current skill
            # Since _read_byte_from_memory (via read_bytes_external) handles the FFX.exe base,
            # this calculation provides the direct offset from the module's start.
            full_offset_from_exe_base = (
                CHARACTER_BLOCK_START_OFFSET +
                (character_index * CHARACTER_BLOCK_STRIDE) +
                skill["offset_from_block"]
            )

            # Read memory for the current skill directly using the calculated offset
            byte_value = _read_byte_from_memory(full_offset_from_exe_base)
            is_unlocked = bool((byte_value >> skill["bit"]) & 1)

            # logger.manip(f"Check {character_index}: {skill} unlocked {is_unlocked}")
            if is_unlocked:
                current_unlocked_list.append({"name": skill["name"]})

        # Assign positions after filtering unlocked skills for the current category
        for i, skill_entry in enumerate(current_unlocked_list):
            skill_entry["position"] = i
        unlocked_and_positioned_abilities[skill_type] = current_unlocked_list


    if logger and report:
        # Reverse lookup character name for logging
        char_name = next((name for name, idx in CHARACTER_NAME_TO_INDEX.items() if idx == character_index), f"Character {character_index}")
        logger.info(f"Unlocked and positioned abilities for {char_name}:")
        for skill_type, abilities in unlocked_and_positioned_abilities.items():
            if abilities:
                logger.info(f"  --- {skill_type} ---")
                for ab in abilities:
                    logger.info(f"    - {ab['name']} (Position: {ab['position']})")
    return unlocked_and_positioned_abilities

# # --- Function 2: Track a given ability's position within its grouping ---
# def get_unlocked_abilities_by_type(character_index: int) -> dict:
#     """
#     Retrieves all unlocked abilities for a given character (by index), sorted by type and then
#     according to the CUSTOM_MENU_ORDER, and includes their display position within their group.
#     Locked abilities are removed.

#     Args:
#         character_index (int): The 0-indexed position of the character (e.g., 0 for Tidus, 1 for Yuna).
#         game_executable_base_address (int): The base memory address for the game's executable (FFX.exe).

#     Returns:
#         dict: A dictionary where keys are skill types (e.g., "White Magic", "Skill")
#               and values are lists of dictionaries. Each inner dictionary contains
#               "name" and "position" (its 0-indexed position within its sorted, unlocked group).
#               Example: {"White Magic": [{"name": "Cure", "position": 0}, ...]}
#     """
#     unlocked_and_positioned_abilities = {
#         "White Magic": [],
#         "Black Magic": [],
#         "Skill": [],
#         "Special": []
#     }

#     # Optimize memory reads by grouping by byte address
#     addresses_to_read = {} # Key: full_address, Value: list of (skill_type, skill_name, bit_position)
#     for skill_type, skills_in_category in PRE_SORTED_SKILLS_BY_TYPE.items():
#         for skill in skills_in_category:
#             full_address = CHARACTER_BLOCK_START_OFFSET + (character_index * 0x94) + skill["offset_from_block"]
#             logger.manip(f"{skill_type} | {skill} | ffx.exe + {full_address}")
#             # This is now generating the desired address.
#             # However I have no idea what the rest of this is doing.
#             # We should be able to read memory from here using _read_byte_from_memory
#             # and immediately start building (or add to) the appropriate category.
#             if full_address not in addresses_to_read:
#                 addresses_to_read[full_address] = []
#             addresses_to_read[full_address].append((skill_type, skill["name"], skill['address'], skill["bit"]))

    

#     # Perform memory reads
#     read_byte_values = {} # Key: full_address, Value: byte_value
#     for address in addresses_to_read.keys():
#         read_byte_values[address] = _read_byte_from_memory(address)

#     # Populate unlocked abilities, maintaining the PRE_SORTED_SKILLS_BY_TYPE order (which is now custom)
#     for skill_type, skills_in_category in PRE_SORTED_SKILLS_BY_TYPE.items():
#         current_unlocked_list = []
#         for skill in skills_in_category:
#             full_address = skill["offset_from_block"]
#             byte_value = read_byte_values.get(full_address, 0) # Get the read byte, default to 0 if failed
#             is_unlocked = bool((byte_value >> skill["bit"]) & 1)

#             if is_unlocked:
#                 current_unlocked_list.append({"name": skill["name"]})

#         # Assign positions after filtering unlocked skills
#         for i, skill_entry in enumerate(current_unlocked_list):
#             skill_entry["position"] = i
#         unlocked_and_positioned_abilities[skill_type] = current_unlocked_list


#     if logger:
#         # Reverse lookup character name for logging
#         char_name = next((name for name, idx in CHARACTER_NAME_TO_INDEX.items() if idx == character_index), f"Character {character_index}")
#         logger.info(f"Unlocked and positioned abilities for {char_name}:")
#         for skill_type, abilities in unlocked_and_positioned_abilities.items():
#             if abilities:
#                 logger.info(f"  --- {skill_type} ---")
#                 for ab in abilities:
#                     logger.info(f"    - {ab['name']} (Position: {ab['position']})")
#     return unlocked_and_positioned_abilities


# --- Function to report the full ability order by type ---
def report_full_ability_order() -> dict:
    """
    Reports the full, sorted order of all abilities within each of their four types.
    This order is based on the CUSTOM_MENU_ORDER.

    Returns:
        dict: A dictionary where keys are skill types and values are lists of
              skill names, representing their defined and custom-menu order.
    """
    ability_order_report = {}
    if logger:
        logger.info("\n--- Full Ability Order Report (According to Custom Menu Order) ---")

    for skill_type, skills_list in PRE_SORTED_SKILLS_BY_TYPE.items():
        # Extract just the names for the report
        ordered_names = [skill["name"] for skill in skills_list]
        ability_order_report[skill_type] = ordered_names

        if logger:
            logger.info(f"--- {skill_type} ---")
            for i, name in enumerate(ordered_names):
                logger.info(f"  {i+1}. {name}") # 1-indexed for human readability in report

    return ability_order_report