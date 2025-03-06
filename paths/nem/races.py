from paths.base import AreaMovementBase


class ToRemiem(AreaMovementBase):
    checkpoint_coordiantes = {
        # 0: [-1442, 123],  # From the northwest corner
        # 1: [-1429, -218],  # From the northwest corner
        0: [-584, -325],  # From the agency
        1: [-703, -584],  # From the agency
        2: [-927, -1415],
        3: [-820, -1547],
        4: [-576, -1654],
        5: [-244, -1619],
        6: [212, -1611],
        7: [544, -1601],
        8: [831, -1503],
        9: [1006, -1445],
        10: [0, 0],  # Chocobo feather
        11: [1420, -1268],
        12: [1800, -1270],
        13: [-604, 359],  # First movement in temple map
        14: [-530, 353],
        15: [-325, 355],
        16: [-257, 355],
        17: [396, 357],  # Far side of bridge
        18: [396, 357],  # Far side of bridge
        19: [396, 357],  # Far side of bridge
        20: [396, 357],  # Far side of bridge
        21: [396, 357],  # Far side of bridge
        22: [396, 357],  # Far side of bridge
        23: [478, 380],
        24: [496, 438],
        25: [594, 570],
        26: [757, 630],
        27: [0, 0],  # Orb to initiate race
        28: [757, 630],
        29: [594, 570],
        30: [496, 438],
        31: [492, 339],  # Past save sphere
        32: [497, 274],
        33: [599, 141],
        34: [763, 71],
        35: [0, 0],  # Start race
    }


class Race1(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [809, 20],
        1: [830, -3],
        2: [890, -27],
        3: [1013, -48],
        4: [1117, -14],
        5: [1182, 34],
        6: [1249, 193],
        7: [1284, 322],
        8: [1227, 451],  # Left of first pole
        9: [1180, 489],
        10: [1093, 615],
        11: [958, 724],
        12: [884, 749],  # Left of green pole
        13: [779, 774],
        14: [673, 776],  # Around second green pole
        15: [644, 751],
        16: [673, 733],
        17: [702, 723],  # End, around second green.
        18: [771, 717],  # Around first yellow pole
        19: [797, 691],
        20: [759, 666],
        21: [709, 676],  # End, around first yellow
        22: [581, 615],
        23: [555, 547],  # Past second/last yellow, last pole
        24: [535, 504],
        25: [537, 291],
        26: [613, 205],  # Past first red pole
        27: [733, 136],
        28: [890, 177],
        29: [913, 206],
        30: [928, 239],  # Past second red pole
        31: [980, 351],
        32: [928, 503],
        33: [762, 532],
        34: [762, 532],  # Past third red pole
        35: [662, 437],
        36: [699, 338],  # Fin
    }


class Race2(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [809, 20],
        1: [830, -3],
        2: [890, -27],
        3: [1013, -48],
        4: [1117, -14],
        5: [1182, 34],
        6: [1249, 193],
        7: [1284, 322],
        8: [1272, 474],  # Right of first pole
        9: [1228, 595],
        10: [1131, 731],
        11: [0, 0],  # First chest
        12: [955, 736],  # Right of green thing
        13: [913, 795],  # Up ramp, avoiding pole
        14: [816, 824],
        15: [830, 881],  # Around blue pole, back towards chest
        16: [964, 824],
        17: [0, 0],  # Second chest
        18: [955, 736],  # Right of green thing
        19: [913, 795],  # Up ramp, avoiding pole
        20: [816, 824],  # Towards third chest
        21: [604, 860],
        22: [0, 0],  # Third chest
        23: [569, 580],
        24: [549, 538],
        25: [529, 463],
        26: [569, 230],
        27: [619, 200],  # Left of first red pillar
        28: [890, 177],
        29: [890, 177],
        30: [913, 206],
        31: [928, 239],  # Past second red pole
        32: [980, 351],
        33: [928, 503],
        34: [762, 532],
        35: [762, 532],  # Past third red pole
        36: [662, 437],
        37: [699, 338],  # Fin
    }


class Race3(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [809, 20],
        1: [830, -3],
        2: [890, -27],
        3: [1013, -48],
        4: [1117, -14],
        5: [1182, 34],
        6: [1249, 193],
        7: [1284, 322],
        8: [1272, 474],  # Right of first pole
        9: [1228, 595],
        10: [1131, 731],
        11: [0, 0],  # First chest
        12: [955, 736],  # Right of green thing
        13: [913, 795],  # Up ramp, avoiding pole
        14: [816, 824],
        15: [830, 881],  # Around blue pole, back towards chest
        16: [964, 824],
        17: [0, 0],  # Second chest
        18: [955, 736],  # Right of green thing
        19: [913, 795],  # Up ramp, avoiding pole
        20: [816, 824],  # Towards third chest
        21: [604, 860],
        22: [0, 0],  # Third chest
        23: [431, 394],
        24: [431, 394],
        25: [462, 208],
        26: [527, 121],
        27: [0, 0],  # Fourth chest
        28: [833, 48],
        29: [914, 89],  # Left of yellow
        30: [961, 121],
        31: [1060, 249],  # Between yellows
        32: [1074, 316],  # Left of yellow
        33: [1098, 339],
        34: [1115, 308],  # Around yellow
        35: [1112, 231],  # Next to green
        36: [1133, 206],
        37: [1157, 228],  # Right of green
        38: [1173, 360],
        39: [0, 0],  # Last chest
        40: [787, 541],
        41: [762, 532],  # Past third red pole
        42: [662, 437],
        43: [699, 338],  # Fin
    }


class LeaveRemiem(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [754, 87],
        1: [663, 113],
        2: [593, 139],
        3: [537, 206],
        4: [494, 277],
        5: [477, 335],
        6: [398, 357],
        7: [356, 357],
        8: [356, 357],
        9: [356, 357],
        10: [356, 357],
        11: [356, 357],
        12: [356, 357],  # On the bridge
        13: [-269, 357],  # Other end of the bridge
        14: [-492, 352],
        15: [-605, 348],
        16: [-662, 343],
        17: [-800, 200],  # Back to main Calm Lands map
        18: [1394, -1279],
        19: [1321, -1258],
        20: [0, 0],  # Chocobo
        21: [1183, -1141],
        22: [1116, -990],
        23: [1110, -950],
        24: [0, 0],  # Feather
        25: [1062, -659],
        26: [1062, -659],
        27: [1062, -659],
        28: [1062, -659],
        29: [1207, -254],
        30: [1315, -148],  # Near the arena
        31: [1301, 271],
        32: [1475, 628],
        33: [1529, 1039],
        34: [1568, 1106],
        35: [1595, 1144],
        36: [1600, 1300],
        37: [0, 0],
        38: [0, 0],
        39: [0, 0],
        40: [0, 0],
    }
