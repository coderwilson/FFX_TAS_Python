from pathing import AreaMovementBase


class BaajRamp(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [224, -177],
        1: [156, -119],
        2: [115, -84],
        3: [77, -59],
        4: [-2, -2],
        5: [-28, 17],
        # click_to_event_temple
        7: [-200, 150],
    }
    checkpoint_fallback = {
        6: "click_to_event_temple",
    }


class BaajHallway(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-8, 87],
        1: [7, 115],
        2: [6, 154],
        3: [1, 160],
        4: [-4, 167],
        5: [8, 176],
        6: [13, 231],
        7: [6, 240],
        8: [-2, 250],
    }
    checkpoint_fallback = {}


class BaajPuzzle(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-71, 79],
        1: [-94, 120],
        2: [-100, 139],
        # Save sphere
        4: [-113, 119],
        # Through first door
        # Flint obtained.
        # Back to main room
        8: [-87, 94],
        9: [-24, -10],
        10: [81, -90],
        11: [135, -137],
        # Map change towards withered bouquet
        13: [85, 71],
        14: [78, 30],
        15: [72, 8],
        16: [76, -6],
        17: [65, -31],
        18: [48, -39],
        19: [29, -64],
        20: [8, -78],
        # Withered bouquet
        22: [8, -78],
        23: [29, -64],
        24: [48, -39],
        25: [65, -31],
        26: [76, -6],
        27: [72, 8],
        28: [78, 30],
        29: [85, 71],
        30: [82, 81],
        31: [75, 90],
        # Back to main room
    }
    checkpoint_fallback = {
        3: "Save sphere",
        5: "Through first door",
        6: "Flint obtained.",
        7: "Back to main room",
        12: "Map change towards withered bouquet",
        21: "Withered bouquet",
        32: "Back to main room",
    }
