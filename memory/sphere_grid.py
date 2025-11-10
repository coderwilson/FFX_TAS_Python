import logging
from enum import Enum

from memory.main import read_bytes_external, base_value
#from players import Player

logger = logging.getLogger(__name__)



def node_type(node_id):
    # One byte, FFX.exe+D2EC7C + (node_id*2)
    key = 0x00D2EC7C + (node_id*2)
    ret_val = read_bytes_external(key, 1)
    # print(f"Node type: {ret_val}")
    return ret_val


def unlocked_by(node_id):
    # One byte, FFX.exe+D2EC7C + (node_id*2)
    key = 0x00D2EC7D + (node_id*2)
    ret_val = read_bytes_external(key, 1)
    # print(f"Node unlocks: {ret_val}")
    return ret_val

def char_current_node(character):
    key = 0x12BE93C + (0x50 * character)
    ret_val = read_bytes_external(key, 2)
    # print(f"Character is at node: {ret_val}")
    return ret_val

def cursor_current_node():
    key = 0x12BEB6C
    ret_val = read_bytes_external(key, 2)
    # print(f"Character is at node: {ret_val}")
    return ret_val

def char_sphere_levels(character):
    key = 0xD32097 + (0x94 * character)
    ret_val = read_bytes_external(key, 1)
    return ret_val