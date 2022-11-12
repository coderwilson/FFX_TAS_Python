from paths.base import AreaMovementBase


class BevelleAirship(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-232, 332],
        1: [-242, 308],
        2: [-241, 215],
        3: [-240, 80],
        4: [-240, 324],  # After leaving and re-entering the cockpit
        5: [-226, 352],
        6: [-223, 366],
        7: [-243, 384],
        8: [-242, 407],
        9: [0, 0],  # Talk to Brother
        10: [-244, 383],
        11: [-257, 375],
        12: [-269, 353],
        13: [0, 0],  # Touch save sphere
        14: [-260, 343],
        15: [-257, 325],
        16: [-244, 314],
        17: [-244, 314],
        18: [0, 0],
        19: [0, 0],
        20: [0, 0],
    }


class BevellePreTrials(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-97, -1],
        1: [-200, -3],
        2: [4, -44],
        3: [26, -18],
        4: [71, -16],
        5: [80, 4],
        6: [85, 115],
        7: [71, 150],
    }


class BevelleTrials(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [64, 177],
        1: [75, 200],
        2: [-19, -62],
        # First pedestal
        # Missed first alcove, recovering
        5: [-50, 88],
        6: [-66, 93],
        # First Bevelle sphere, and then more gliding
        8: [13, 88],
        9: [13, 93],
        # Insert Bevelle sphere. Activate lower areas
        11: [27, 92],
        12: [26, 86],
        # Down to the lower areas
        14: [397, 357],
        15: [501, 363],
        # Take sphere from second alcove
        17: [406, 364],
        # To third alcove, and insert Glyph sphere
        19: [353, 531],
        20: [367, 532],
        21: [370, 526],
        # Remove Bevelle sphere
        23: [367, 532],
        # Insert Bevelle sphere
        25: [353, 531],
        26: [342, 527],
        27: [352, 525],
        # Take Glyph sphere
        29: [367, 532],
        30: [374, 526],
        31: [431, 527],
        # Insert Glyph sphere
        33: [499, 522],
        # Take Destro sphere
        35: [374, 524],
        36: [366, 524],
        # Insert Destro sphere
        38: [367, 532],
        # Remove Bevelle sphere
        40: [369, 526],
        # Back on track
        42: [392, 366],
        # Insert Bevelle sphere (back in second alcove)
        44: [395, 372],
        45: [407, 370],
        46: [406, 363],
        # Take Destro sphere
        48: [493, 371],
        49: [493, 371],
        # Insert Destro sphere
        51: [406, 364],
        # Back on track, to the exit
        53: [95, 271],  # Final map with chests.
        54: [83, 271],
        55: [76, 263],
        56: [-5, 270],
        57: [-16, 279],
        # Picking up chest
        59: [-5, 302],
        60: [-5, 400],
    }
    checkpoint_fallback = {
        3: "First pedestal",
        4: "Missed first alcove, recovering",
        7: "First Bevelle sphere, and then more gliding",
        10: "Insert Bevelle sphere. Activate lower areas",
        13: "Down to the lower areas",
        16: "Take sphere from second alcove",
        18: "To third alcove, and insert Glyph sphere",
        22: "Remove Bevelle sphere",
        24: "Insert Bevelle sphere",
        28: "Take Glyph sphere",
        32: "Insert Glyph sphere",
        34: "Take Destro sphere",
        37: "Insert Destro sphere",
        39: "Remove Bevelle sphere",
        41: "Back on track",
        43: "Insert Bevelle sphere (back in second alcove)",
        47: "Take Destro sphere",
        50: "Insert Destro sphere",
        52: "Back on track, to the exit",
        58: "Picking up chest",  # TODO: This line gets spammed in the log
    }


class SutekiDaNe(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-3, 17],
        # 1?
        2: [42, -55],
        # 3?
        4: [208, 51],
        # Enjoy this very long scene
        # 6?
        7: [93, -9],
        # 8?
        9: [-55, -29],
        10: [-20, 4],
        11: [6, 50],
        12: [0, 0],
        13: [0, 0],
        14: [0, 0],
        15: [0, 0],
    }
    checkpoint_fallback = {
        5: "Enjoy this very long scene",
    }
