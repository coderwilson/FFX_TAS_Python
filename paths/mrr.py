from paths.base import AreaMovementBase


class MRRStart(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-40, -667],
        1: [-58, -614],
        2: [-62, -616],
        # Attempt skip
        4: [-21, -593],
        5: [-30, -530],
        6: [-59, -498],
        7: [-80, -488],
        8: [-115, -488],
        9: [-206, -418],
        10: [-206, -300],
    }
    checkpoint_fallback = {
        3: "Attempt skip",
    }


class MRRMain(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [12, -738],
        # Touching save sphere
        2: [-28, -663],
        3: [-37, -601],
        # Up the first lift
        5: [-48, -571],
        6: [-108, -463],
        7: [-108, -428],
        8: [-85, -391],
        9: [-87, -372],
        10: [-78, -361],
        11: [-38, -367],
        12: [-6, -381],
        13: [38, -414],
        14: [63, -398],
        15: [109, -339],
        16: [127, -198],
        17: [122, -166],
        18: [91, -176],
        19: [0, -215],
        20: [-63, -189],
        21: [-88, -141],
        22: [-104, 54],
        23: [-102, 73],
        24: [-86, 87],
        25: [25, 138],
        26: [32, 151],
        27: [23, 233],
        28: [-89, 295],
        29: [-91, 321],
        30: [-87, 368],
        31: [-68, 402],
        32: [-48, 425],
        33: [35, 461],
        34: [92, 515],
        35: [51, 543],
        36: [-20, 568],
        37: [-71, 593],
        38: [-109, 604],
        39: [-115, 687],
        40: [-71, 775],
        41: [-39, 829],
        42: [-12, 838],
        43: [26, 828],
        44: [44, 834],
        45: [59, 898],
        # Up the second lift
        47: [-36, -194],
        # Grabbing X-potion from the dude
        49: [24, -157],
        50: [52, -135],
        51: [116, 4],
        52: [121, 50],
        53: [112, 100],
        # Lining up with the guy for 400 gil
        54: [61, 140],
        55: [29, 154],
        56: [-21, 223],
        57: [29, 227],
        # Up the third lift
        59: [59, 244],
        60: [99, 254],
        61: [198, 251],
        62: [219, 202],
        # Diagonal towards the save sphere
        63: [226, 170],
        64: [248, 169],
        65: [271, 183],
        # Up the final lift
        67: [304, 186],
        68: [327, 185],
        69: [341, 172],
        70: [450, 160],
        # Into Battle Site zone (upper, cannon area)
        71: [47, 513],
        72: [70, 606],
        73: [84, 629],
        74: [70, 707],
        75: [-67, 830],
        90: [204, 136],
        99: [77, 872],
    }
    checkpoint_fallback = {
        1: "Touching save sphere",
        4: "Up the first lift",
        46: "Up the second lift",
        48: "Grabbing X-potion from the dude",
        58: "Up the third lift",
        66: "Up the final lift",
    }


class MRRBattleSite(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-430, 3274],
        1: [-258, 3227],
        2: [-207, 3230],
        3: [-115, 3330],
        4: [-52, 3414],
        # O'aka menu
        6: [-68, 3354],
        7: [-59, 3345],
        # Touching save sphere
        9: [-71, 3324],
        10: [-45, 3296],
        11: [-16, 3276],
        # Into the scene with Kinoc
        13: [217, 3134],
        # Start of fight, Sinspawn Gui
    }
    checkpoint_fallback = {
        5: "O'aka menu",
        8: "Touching save sphere",
        12: "Into the scene with Kinoc",
        14: "Start of fight, Sinspawn Gui",
    }


class MRRSkip(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-21, -313],
        1: [1, -202],
        2: [46, -81],
        3: [65, 39],
        4: [121, 132],
        5: [183, 197],
        6: [267, 347],
        7: [318, 526],
        8: [373, 772],
        9: [390, 800],
    }

class MRRBattleSiteAftermath(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [148, 2836],
        1: [75, 2992],
        # Clasko position
        2: [50, 3092],
        # click_to_event_temple
        4: [609, -175],
        5: [548, -159],
        6: [417, -160],
        # Start conversation with Auron
        8: [428, -116],
        9: [501, 40],
        10: [520, 40],
        11: [671, 47],
        12: [830, 39],
        13: [941, 59],
        14: [978, 77],
        # Towards Djose section
    }
    checkpoint_fallback = {
        3: "click_to_event_temple",
        7: "Start conversation with Auron",
        15: "Towards Djose section",
    }
