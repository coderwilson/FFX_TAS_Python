from paths.base import AreaMovementBase


class Kilika1(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-301, -258],
        1: [-269, -253],
        2: [-137, -226],
        3: [-59, -195],
        # Enter cutscene, Yunas dance
        5: [80, -22],
        # Yuna dancing, ends in the inn
        7: [41, 2],
        # Exit the inn
        9: [27, 114],
        10: [86, 96],
        11: [86, 31],
        # Back to first map
        13: [-31, -179],
        14: [-25, -216],
        15: [-1, -245],
        # Talking to Wakka
        17: [-24, -166],
        # Back towards the inn
        19: [84, 99],
        20: [4, 106],
        21: [-112, 117],
        22: [-125, 135],
        23: [-155, 205],
        24: [-155, 350],
    }
    checkpoint_fallback = {
        4: "Enter cutscene, Yunas dance",
        6: "Yuna dancing, ends in the inn",
        8: "Exit the inn",
        12: "Back to first map",
        16: "Talking to Wakka",
        18: "Back towards the inn",
    }


class Kilika2(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-77, -475],
        1: [-83, -427],
        2: [-101, -417],
        3: [-146, -413],
        4: [-179, -417],
        5: [-212, -416],
        6: [-221, -406],
        7: [-222, -362],
        8: [-224, -336],
        # Wakka Scout
        10: [-216, -330],
        11: [-216, -316],
        12: [-206, -305],
        13: [-204, -293],
        14: [-215, -275],
        15: [-226, -250],
        16: [-234, -226],
        17: [-241, -206],
        18: [-241, -135],
        19: [-242, -124],
        20: [-249, -101],
        21: [-241, -84],
        22: [-242, -57],
        23: [-240, -35],
        24: [-244, -20],
        25: [-251, 3],
        26: [-264, 25],
        27: [-259, 37],
        28: [-248, 53],
        29: [-237, 58],
        30: [-225, 68],
        31: [-217, 71],
        32: [-206, 61],
        33: [-185, 72],
        34: [-166, 51],
        35: [-144, 64],
        36: [-100, 65],
        37: [-86, 96],
        38: [-85, 124],
        39: [-100, 176],
        40: [-122, 211],
        41: [-134, 210],
        42: [-167, 210],
        43: [-178, 201],
        44: [-196, 212],
        45: [-217, 210],
        46: [-241, 208],
        # Picking up chest
        48: [-230, 212],
        49: [-199, 212],
        50: [-188, 208],
        51: [-178, 202],
        52: [-170, 204],
        53: [-160, 209],
        54: [-137, 208],
        55: [-118, 208],
        56: [-109, 195],
        57: [-92, 147],
        58: [-59, 99],
        59: [-49, 83],
        60: [-33, 79],
        61: [7, 71],
        62: [34, 72],
        63: [53, 76],
        64: [88, 79],
        65: [100, 70],
        66: [133, 79],
        67: [149, 87],
        68: [151, 110],
        69: [148, 132],
        70: [130, 175],
        71: [96, 212],
        72: [69, 249],
        73: [66, 258],
        74: [49, 268],
        75: [30, 284],
        76: [2, 292],
        77: [-30, 294],
        78: [-58, 299],
        79: [-66, 300],
        80: [-68, 328],
        81: [-70, 417],
        82: [-95, 415],
        # Into next area
        83: [-80, 500],
        84: [-58, 144],
        85: [-20, 172],
        # Stairs save sphere
        87: [-10, 192],
        88: [17, 233],
        89: [13, 286],
        90: [-51, 609],
        91: [-99, 656],
        92: [-129, 685],
        93: [-160, 740],
        94: [2, 270],
        # Into the temple
        95: [2, 500],
        96: [-1, -56],
        # non-CSR, slight left
        97: [-22, 6],
        # non-CSR, past Lulu
        98: [-30, 33],
        # non-CSR, pray to O'holland
        100: [2, 54],
    }
    checkpoint_fallback = {
        9: "Wakka Scout",
        47: "Picking up chest",
        86: "Stairs",
        99: "non-CSR, pray to O'holland",
    }


class KilikaTrials(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-6, -247],
        1: [-17, -215],
        # Pick up Kilika sphere
        3: [-10, -205],
        4: [8, -188],
        # Insert and remove, opens door
        6: [5, -181],
        7: [1, -176],
        8: [0, 11],
        # Insert and remove, generate glyph
        10: [37, -18],
        # Insert, out of the way
        12: [1, 11],
        # Touch glyph
        14: [1, 34],
        15: [8, 133],
        16: [30, 165],
        17: [52, 167],
        # Remove Kilika sphere
        19: [52, 167],
        20: [30, 165],
        21: [8, 133],
        22: [1, 34],
        23: [-2, 15],
        24: [-37, -8],
        # Insert Kilika sphere
        26: [-24, -25],
        # Pick up Glyph sphere
        28: [-2, 15],
        29: [1, 34],
        30: [8, 133],
        31: [30, 165],
        32: [52, 167],
        # Insert Glyph sphere
        34: [30, 165],
        35: [8, 133],
        36: [1, 34],
        37: [1, 15],
        38: [-36, -18],
        # Pick up last Kilika sphere
        40: [1, 15],
        41: [1, 34],
        42: [-9, 133],
        43: [-29, 163],
        44: [-36, 177],
        45: [-38, 207],
        46: [31, 225],
        47: [37, 232],
        48: [35, 270],
        49: [17, 275],
        # Insert and remove, opens door
        51: [5, 278],
        52: [0, 400],
        # Inner sanctum
        53: [-13, -10],
        # Talk to Wakka
        55: [-6, -20],

        # These are for destro sphere
        60: [-24, -25],
        # Place Kilika sphere
        62: [-2, 15],
        63: [1, 34],
        64: [8, 133],
        65: [30, 165],
        66: [50, 189],
        67: [50, 197],
        # Reset glyph
        69: [47, 178],
        70: [5,121],
        71: [1,137],  # Stutter step to position, then push
        72: [-8,172],
        73: [-17,187],
        74: [-7,188],
        75: [-7,188],
        76: [-7,188],
        # Push east towards hidden room
        78: [42,177],
        79: [50,172],
        80: [49,179],  # 51
        # Push pedestol north to final spot
        82: [51,173],
        83: [-29,168],
        84: [-40,178],
        85: [-40,209],
        86: [-26,213],
        87: [46,208],
        # Pick up Kilika sphere
        89: [35,261],
        90: [29,275],
        # Place Kilika sphere
        92: [38,266],
        93: [36,222],
        94: [-39,208],
        95: [-36,164],
        96: [46,171],
        # Pick up destro sphere
        98: [46,171],  # Buffer
        99: [46,171],  # Buffer

        100: [64,174],
        101: [56,174],
        102: [-29,168],
        103: [-40,178],
        104: [-40,209],
        105: [-26,213],
        106: [46,208],
        # Place up destro sphere
        108: [55,208],
        # Pick up chest
        110: [46,208],
        111: [35,261],
        112: [29,275],
    }
    checkpoint_fallback = {
        2: "Pick up Kilika sphere",
        5: "Insert and remove, opens door",
        9: "Insert and remove, generate glyph",
        11: "Insert, out of the way",
        13: "Touch glyph",
        18: "Remove Kilika sphere",
        25: "Insert Kilika sphere",
        27: "Pick up Glyph sphere",
        33: "Insert Glyph sphere",
        39: "Pick up last Kilika sphere",
        50: "Insert and remove, opens door",
        54: "Talk to Wakka",
    }


class Kilika3(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-68, 314],
        1: [-65, 299],
        2: [-33, 289],
        3: [26, 284],
        4: [38, 278],
        5: [64, 258],
        6: [78, 242],
        7: [101, 211],
        8: [126, 178],
        9: [149, 138],
        10: [153, 107],
        11: [148, 81],
        12: [120, 72],
        13: [89, 77],
        14: [70, 75],
        15: [28, 70],
        16: [-38, 80],
        17: [-112, 59],
        18: [-150, 58],
        19: [-184, 71],
        20: [-207, 64],
        21: [-228, 63],
        22: [-245, 52],
        23: [-254, 45],
        24: [-256, 36],
        25: [-259, 25],
        26: [-256, 14],
        27: [-246, -10],
        28: [-244, -25],
        29: [-240, -39],
        30: [-242, -54],
        # Before crossing log, between two trees.
        31: [-241, -80],
        # Right before stepping on the log
        32: [-246, -122],
        33: [-241, -144],
        34: [-244, -204],
        35: [-236, -233],
        36: [-229, -249],
        37: [-220, -263],
        38: [-207, -289],
        39: [-206, -298],
        40: [-214, -323],
        41: [-218, -338],
        42: [-226, -342],
        43: [-225, -356],
        44: [-223, -388],
        45: [-218, -411],
        46: [-209, -417],
        47: [-174, -417],
        48: [-104, -418],
        49: [-84, -430],
        50: [-78, -452],
        51: [-85, -525],
        # Back to the docks
        52: [-70, -600],
        53: [-150, 200],
        54: [-126, 149],
        55: [-121, 127],
        56: [-111, 109],
        57: [-59, 108],
        58: [-6, 110],
        59: [41, 102],
        60: [80, 99],
        61: [87, 89],
        62: [88, 43],
        63: [88, -100],
        64: [-48, -184],
        65: [-56, -194],
        66: [-84, -213],
        # Just before the boat, after the hammer guy
        67: [-161, -241],
    }
