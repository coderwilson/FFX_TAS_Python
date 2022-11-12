from paths.base import AreaMovementBase


class MacalaniaTempleApproach(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [22, 538],
        1: [30, 650],
        2: [39, 86],  # From snowmobile screen to curve screen
        3: [87, 202],
        4: [166, 298],
        5: [216, 323],
        6: [310, 358],
        7: [396, 382],
        8: [472, 378],
        9: [526, 338],
        10: [646, 270],
        11: [714, 217],
        12: [778, 101],
        13: [801, -45],
        14: [801, -206],
        15: [815, -455],
        16: [801, -500],  # Into the door (dial in)
    }


class MacalaniaTempleFoyer(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-18, -124],
        # Touch save sphere
        2: [19, -103],
        3: [23, -102],
        # Trommell
        # Lining up for skip
        6: [-73, -14],
        7: [-109, -22],
        # Chest
        9: [-73, -14],
        10: [-21, 4],
        # Check if skip successful
        12: [2, 38],
        13: [0, 103],
        # Check if pause necessary
        15: [0, 300],  # Into the room before Seymour
        16: [0, -300],  # Into Seymour's room
        # 17-19?
        20: [16, 30],  # Skip fail, use this path instead.
        21: [41, 59],
        22: [59, 118],
        # Into the door, Jyscal sphere
        # And back out again
        25: [35, 48],
        26: [15, 31],
    }
    checkpoint_fallback = {
        1: "Touch save sphere",
        4: "Trommell",
        5: "Lining up for skip",
        8: "Chest",
        11: "Check if skip successful",
        14: "Check if pause necessary",
        23: "Into the door, Jyscal sphere",
        24: "And back out again",
    }


class MacalaniaTempleTrials(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [2, -114],
        1: [2, -200],
        # Activate the trials
        3: [-12, -116],
        4: [-33, -113],
        5: [-50, -88],
        6: [-66, -16],
        7: [-47, -12],
        8: [31, 4],
        # Push pedestal
        10: [18, 52],
        11: [6, 83],
        12: [2, 107],
        # Grab first Mac Sphere
        14: [11, 71],
        15: [26, 44],
        16: [31, 43],
        # Place first Mac Sphere
        18: [41, 44],
        19: [42, 49],
        # Push pedestal
        21: [12, 2],
        22: [0, 3],
        # Pick up Glyph sphere
        24: [-8, 4],
        25: [-77, 54],  # Spot next to the ramp-sphere
        26: [-80, 24],
        27: [-15, 7],  # Bottom of the ramp
        28: [0, 4],
        # Push pedestal
        30: [-11, -27],
        31: [-9, -49],
        # Insert glyph sphere
        33: [-15, 7],
        34: [-80, 24],
        35: [-77, 54],
        36: [-62, 51],
        37: [-21, -40],
        38: [-19, -53],
        # Second Mac sphere
        40: [-21, -40],
        41: [-62, 51],
        42: [-77, 54],
        43: [-80, 24],
        44: [-15, 7],
        45: [11, -32],
        # Second Mac sphere
        47: [10, -27],
        48: [-15, 7],
        49: [-80, 24],
        50: [-77, 54],
        # Third Mac sphere
        52: [-3, 4],
        # Third Mac sphere
        54: [-68, -17],  # Ready to get out of here
        55: [-48, -93],
        56: [-20, -116],
        57: [-5, -106],
        # Trials - end
    }
    checkpoint_fallback = {
        2: "Activate the trials",
        9: "Push pedestal",
        13: "Grab first Mac Sphere",
        17: "Place first Mac Sphere",
        20: "Push pedestal",
        23: "Pick up Glyph sphere",
        29: "Push pedestal",
        32: "Insert glyph sphere",
        39: "Second Mac sphere",
        46: "Second Mac sphere",
        51: "Third Mac sphere",
        53: "Third Mac sphere",
        58: "Trials - end",
    }


class MacalaniaTempleEscape(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [807, -263],
        1: [817, -244],
        # Touching save sphere
        3: [815, -227],
        4: [815, -206],
        5: [801, -45],  # Start of turn
        6: [778, 101],
        7: [714, 217],
        8: [646, 270],
        9: [526, 338],
        10: [472, 378],
        11: [396, 382],
        12: [310, 358],
        13: [216, 323],
        14: [166, 298],
        15: [87, 202],
        16: [39, 86],
        17: [-9, -38],
        18: [-50, -100],
        19: [-13, 410],  # Back to the snowmobiles
        20: [6, 363],
        21: [44, 320],
        22: [51, 274],
        23: [40, 243],
        24: [25, 218],
        25: [-32, 196],
        26: [-30, 169],
        27: [-28, 63],
        28: [-20, -159],
        29: [-8, -269],
        30: [13, -420],
        31: [33, -565],
        32: [33, -700],
    }
    checkpoint_fallback = {
        2: "Touching save sphere",
    }


class MacalaniaUnderTemple(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [1, 146],
        1: [34, 116],
        2: [29, 98],
        3: [0, 80],
        4: [0, 0],  # Talk to Rikku then Yuna
        5: [1, 146],
        6: [34, 116],
        7: [29, 98],
        8: [10, 86],
        9: [-24, 103],
        10: [-41, 95],
        11: [0, 0],  # Open chest
        12: [-21, 103],
        13: [0, 73],
        14: [-5, 13],
        15: [0, 0],  # Talk to Auron
        16: [0, 73],  # Back down to next scene
        17: [0, 0],
        18: [0, 0],
        19: [0, 0],
        20: [0, 0],
    }
