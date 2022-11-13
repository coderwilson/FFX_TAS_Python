from paths.base import AreaMovementBase


class ZanarkandOutdoors(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-16, -671],
        1: [1, -507],
        2: [-17, -435],
        3: [-98, -442],
        # Fortune sphere, no direction from this function
        5: [-108, -418],
        6: [-210, -282],
        7: [-190, -100],
        # Weird cutscene where we don't lose control immediately
        8: [-94, 81],
        9: [-121, 301],
        10: [-187, 424],
        11: [-365, 565],
        12: [-523, 656],
        13: [-564, 801],
        14: [-628, 936],
        15: [-750, 1083],
    }
    checkpoint_fallback = {
        4: "Fortune sphere, no direction from this function",
    }


class ZanarkandDome(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [2, -325],
        1: [117, -203],
        2: [128, -162],
        3: [134, -85],
        4: [71, -20],
        5: [-20, 5],
        6: [-136, -32],
        7: [-186, -109],
        8: [-144, -124],  # Near save sphere
        9: [-132, -105],
        10: [-126, 49],  # Seymour scene
        11: [-101, 76],
        12: [3, 89],
        # Friend sphere, no direction from this function
        14: [-127, 68],
        15: [-230, 146],
        16: [-154, 195],
        17: [-73, 232],  # Mini-bridge, running with Braska/Jecht
        18: [-27, 286],
        19: [7, 386],
        20: [-5, 600],
        21: [-12, -188],
        22: [3, -96],
        23: [23, -80],
        # Luck sphere, no direction from this function
        25: [-15, -49],
        26: [1, 36],
        27: [5, 240],
        28: [-21, 352],
        # Touching save sphere, no direction from this function
        30: [-3, 360],
        31: [1, 500],
    }
    checkpoint_fallback = {
        13: "Friend sphere, no direction from this function",
        24: "Luck sphere, no direction from this function",
        29: "Touching save sphere, no direction from this function",
    }


class ZanarkandTrials(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [105, -57],
        1: [105, -44],
        2: [135, -35],
        3: [126, -14],
        4: [133, 5],
        5: [110, 18],
        6: [84, 25],
        7: [71, 25],
        # First pedetsol, no direction from here
        9: [-1, 11],  # First pattern in big room
        10: [-4, -6],
        11: [-25, -26],
        12: [-53, 18],
        13: [-79, 24],
        14: [-106, 19],
        15: [-125, 4],
        16: [-157, 45],
        17: [-103, 66],
        18: [-93, 86],
        19: [-90, 123],
        # Picking up Kilika sphere
        21: [-53, 63],
        22: [11, 70],
        23: [28, 72],
        24: [83, 34],
        25: [71, 4],
        # Placing Kilika sphere
        27: [72, -12],
        # Activating second pedestal
        29: [77, 43],
        # Moving into next room
        31: [-5, 74],  # Second pattern in big room
        32: [-17, 44],
        33: [-28, 42],
        34: [-88, 31],
        35: [-106, 33],
        36: [-114, -1],
        37: [-128, -29],
        38: [-156, -55],
        39: [-104, -64],
        40: [-84, -75],
        41: [-13, -42],
        42: [1, 57],
        43: [28, 74],
        44: [83, 34],
        45: [137, 23],
        # Activating second pedestal
        47: [84, 45],
        # Moving into next room
        49: [-5, 74],  # Third pattern in main room, start.
        50: [-17, 45],
        51: [-27, 44],
        52: [-57, 67],
        53: [-94, 85],
        54: [-106, 60],
        55: [-116, 40],
        56: [-124, 3],
        57: [-115, -31],
        58: [-104, -65],
        59: [-79, -57],
        60: [-23, -75],
        61: [-15, -43],
        62: [3, 65],
        63: [32, 73],
        64: [83, 34],
        65: [137, -22],
        # Activating second pedestal
        67: [84, 45],
        # Moving into next room
        69: [-6, 75],  # Last pattern in main room.
        70: [0, 6],
        71: [-14, -46],
        72: [-24, -75],
        73: [-86, -75],
        74: [-104, -67],
        75: [-124, -5],
        76: [-136, -1],
        77: [-155, 46],
        78: [-104, 78],
        79: [-92, 88],
        80: [-68, 110],
        # Picking up Besaid sphere
        82: [-67, 94],
        83: [5, 71],
        84: [33, 72],
        85: [83, 34],
        86: [136, -1],
        # Placing Besaid sphere
        88: [110, 20],
    }
    checkpoint_fallback = {
        8: "First pedetsol, no direction from here",
        20: "Picking up Kilika sphere",
        26: "Placing Kilika sphere",
        28: "Activating second pedestal",
        30: "Moving into next room",
        46: "Activating second pedestal",
        48: "Moving into next room",
        66: "Activating second pedestal",
        68: "Moving into next room",
        81: "Picking up Besaid sphere",
        87: "Placing Besaid sphere",
    }


class ZanarkandYunalesca(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [3, 8],
        1: [5, 35],
        2: [0, 0],
        3: [0, 80],
        4: [0, 0],
        5: [0, 0],
        6: [0, 0],
        7: [0, 0],
        8: [0, 0],
        9: [0, 0],
        10: [0, 0],
    }


class YunalescaToAirship(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-4, -179],
        1: [-4, -300],
        2: [0, 55],
        3: [0, -200],
        4: [0, -72],
        5: [-2, -132],
        6: [0, -160],
        7: [0, -160],  # Touch save sphere
        8: [0, -200],
        9: [0, -500],
        10: [-65, -56],
        11: [-46, -35],
        12: [3, 62],
        13: [28, 68],
        14: [83, 34],
        15: [99, -67],
        16: [100, -93],
        17: [100, -200],
        18: [-1, 243],
        19: [-3, 148],
        20: [-5, 39],
        21: [-12, -53],
        22: [-6, -89],
        23: [-10, -200],
        24: [-10, -400],
        25: [125, 1423],
    }
    checkpoint_fallback = {
        7: "Touch save sphere",  # TODO: This is maybe not intended as a fallback?
    }
