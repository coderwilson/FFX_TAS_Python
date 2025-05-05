from paths.base import AreaMovementBase


class BikanelDesert(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [0, -74],
        1: [20, -69],
        # Touching save sphere
        3: [3, -79],
        4: [-13, -128],
        5: [12, -288],
        6: [121, -409],
        7: [147, -421],
        8: [197, -387],
        9: [220, -400],
        10: [172, -569],
        11: [441, -366],
        12: [228, -523],
        13: [206, -534],
        14: [89, -522],
        15: [-26, -523],
        16: [-120, -494],
        17: [-186, -395],
        18: [-158, -346],
        19: [44, -250],
        20: [138, -200],
        21: [164, -134],
        22: [190, -8],
        23: [199, 28],
        # Touching save sphere
        25: [187, 26],
        26: [170, 29],
        27: [160, 46],
        28: [180, 67],
        29: [253, 116],
        30: [352, 126],
        31: [478, 139],  # Machina battle mid-path
        32: [552, 157],
        33: [594, 224],
        34: [659, 444],
        35: [657, 698],
        36: [664, 790],
        37: [698, 854],
        38: [800, 1000],
        # Large open map with two directions
        39: [333, -501],
        40: [-70, 177],
        41: [-158, 278],
        42: [-278, 360],
        # Extra spots for future precision if needed
        43: [-278, 360],
        44: [-278, 360],
        45: [-356, 468],
        46: [-426, 550],
        47: [-624, 693],
        48: [-667, 773],
        49: [-680, 850],
        # Final map before Home
        50: [-252, -101],
        51: [-192, 45],
        52: [-41, 419],
        # Sandragora #1
        54: [-57, 439],
        55: [-228, 764],
        56: [-228, 764],
        # 57?
        58: [-228, 764],  # Lining up for Sandy skip
        59: [-235, 797],  # Lining up for Sandy skip
        # 60?
        61: [-273, 850],  # Waiting to be pushed
        62: [-273, 850],  # Past Sandy
        63: [-294, 886],
        # Test for area completion
        65: [-300, 1000],
        # 66-69?
        70: [-457, 521],  # Nemesis logic
        71: [-446, 458],
        72: [0, 0],  # Chest, lv.2 key sphere
        73: [-474, 476],
        74: [0, 0],  # Chest, 10k gil
        75: [-481, 505],
        85: [127, -467],
        86: [145, -482],
        87: [175, -481],
        88: [175, -481],  # Flip RNG
        89: [189, -478],
        90: [212, -439],
    }
    checkpoint_fallback = {
        2: "Touching save sphere",
        9: "Map change",
        24: "Touching save sphere",
        53: "Sandragora #1",
        64: "Test for area completion",
    }


class BikanelHome(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [5, -35],
        1: [46, 21],
        2: [70, 69],
        3: [70, 82],
        4: [67, 89],
        # Extra in case we need refactoring later.
        5: [67, 89],
        6: [67, 89],
        7: [0, 0],  # Touch save sphere
        8: [71, 68],
        9: [55, 52],
        10: [3, 82],
        11: [0, 120],
        12: [0, 0],
        13: [0, -5],
        14: [0, -5],  # First battle
        15: [41, 35],
        16: [81, 65],
        17: [161, 125],
        18: [0, 220],  # Into second battle and new map
        19: [0, 220],
        20: [0, 0],  # Branch based on blitz win
        21: [-2, 236],
        22: [-5, 310],
        23: [-13, 330],
        24: [-66, 359],  # Right next to door
        25: [-168, 275],  # Into the door. Load into same map.
        26: [-168, 275],
        27: [-184, 253],  # Screen change before next battle
        28: [-174, 223],
        29: [-184, 210],
        30: [-184, 210],
        31: [-234, 162],  # Down the stairs, storyline.
        32: [-296, 217],
        33: [-315, 217],
        34: [-343, 189],
        35: [-354, 182],
        36: [-367, 193],
        37: [-360, 231],
        38: [-352, 265],
        39: [0, 0],  # Open chest
        40: [-398, 219],
        41: [-414, 211],
        42: [0, 0],  # Big Reveal room
        43: [91, -25],
        44: [124, -50],
        45: [0, 0],  # Stairs to airship
        46: [188, 58],
        47: [101, 59],
        48: [0, 60],
        49: [0, 0],
        50: [0, 0],
        # 51-59?
        # Used for Kilika skip and Nemesis, extra chest.
        60: [-343, 189],
        61: [-339, 169],
        62: [-311, 146],
        63: [0, 0],  # Nemesis, extra chest.
        # 64-80?
        81: [0, 97],
        82: [-6, 29],
        83: [-20, 15],
        84: [-2, 39],
        85: [6, 44],
        86: [0, 0],  # Open chest
        87: [1, 157],
    }
