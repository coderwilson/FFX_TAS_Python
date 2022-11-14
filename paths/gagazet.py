from paths.base import AreaMovementBase


class CalmLands(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-332, -1612],
        1: [-437, -1603],
        2: [-640, -1591],
        3: [-757, -1530],
        4: [-777, -1478],
        # Southeast of agency, northeast of the turn.
        5: [-186, -715],
        6: [461, -35],
        7: [708, 215],
        8: [766, 276],
        9: [821, 290],
        10: [1366, 609],
        11: [1422, 663],
        12: [1440, 724],
        13: [1466, 841],
        14: [1549, 1059],
        15: [1630, 1230],
    }


class DefenderX(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [62, -66],
        1: [69, -229],
        2: [-14, 104],
        3: [-9, 240],
        4: [12, 350],
    }


class KelkRonso(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-122, -552],
        1: [-10, -444],
        2: [23, -369],
        3: [21, -192],
        4: [17, 146],
        5: [50, 290],
        6: [80, 550],
    }


class GagazetSnow(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [18, 45],
        1: [57, 328],
        2: [40, 375],
        3: [-1, 421],
        4: [-49, 444],
        5: [-237, 311],
        6: [-273, 315],
        7: [-327, 383],
        8: [-369, 465],
        9: [-409, 460],
        10: [-538, 264],
        11: [-619, 210],
        12: [-913, 163],
        13: [-941, 191],
        14: [-903, 330],
        15: [-878, 433],
        16: [-830, 540],
        17: [-728, 565],
        18: [-664, 537],
        19: [-633, 497],
        20: [-599, 370],
        21: [-592, 262],
        22: [-600, 223],
        23: [-790, 207],
        24: [-877, 232],
        25: [-1034, 491],
        26: [-1065, 502],
        27: [-1133, 446],
        28: [-1248, 166],
        29: [-1307, -1],
        30: [-1365, -85],
    }


class SeymourFlux(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-368, -330],
        1: [-303, -259],
        2: [31, -202],
        3: [146, -285],
        4: [173, -343],
        5: [167, -550],
        6: [150, -619],
    }


class GagazetDreamSeq(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-62, 180],
        1: [-29, 134],
        2: [-20, 113],
        3: [15, 21],
        4: [23, 9],
        5: [58, 3],
        6: [123, 1],
        7: [149, 0],
        8: [173, 1],
        9: [205, 3],
        10: [239, 18],
        11: [0, 0],  # Into the door
        12: [62, -35],
        13: [63, -14],
        14: [52, -12],
        15: [0, 0],  # Start first conversation
        16: [64, -12],
        17: [64, -25],
        18: [64, -46],
        19: [0, 0],  # Back to outdoor area
        20: [235, 8],
        21: [234, -18],
        22: [238, -26],
        23: [269, -30],
        24: [288, -25],
        25: [326, -1],
    }


class GagazetPostDream(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [1143, 73],
        1: [1054, 289],
        2: [1016, 383],
        3: [1023, 404],
        4: [1019, 494],
        5: [990, 529],
        6: [991, 585],
        7: [1020, 620],
        8: [1046, 643],
        9: [1200, 643],
    }


class GagazetCave(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-45, -1252],
        1: [-27, -1142],
        2: [79, -969],
        3: [90, -949],
        4: [47, -812],
        5: [25, -552],
        6: [161, -376],
        # Map change, no target from this function
        8: [-45, -393],
        9: [9, -257],
        10: [106, 9],
        11: [192, 153],
        # 12?
        13: [100, -3],
        14: [7, -266],
        15: [-49, -420],
        16: [-52, -477],
        # Map change, no target from this function
        18: [36, -535],
        19: [35, -767],
        20: [56, -832],
        21: [143, -929],
        22: [232, -853],
        23: [241, -788],
        24: [192, -669],
        25: [180, -625],
        26: [208, -418],
        27: [248, -270],
        28: [240, -63],
        # Map change, no target from this function
        30: [183, 66],
        31: [201, 208],
        32: [208, 260],
        33: [181, 292],
        34: [140, 301],
        # Second trial, no target from this function
        36: [168, 295],
        37: [189, 283],
        38: [208, 256],
        39: [199, 175],
        40: [179, 67],
        41: [204, -10],
        # Map change, no target from this function
        43: [229, -274],
        44: [215, -375],
        45: [197, -435],
        46: [184, -445],  # Turn to go up the new stairs
        47: [177, -433],
        48: [172, -356],
        49: [161, -335],
        50: [156, -288],
        51: [168, -252],
        52: [159, -236],
        53: [183, -196],
        54: [181, -107],
        55: [162, -26],
        56: [142, 14],
        57: [7, 99],
        58: [-208, 240],
        # 59?
        60: [-260, 200],
    }
    checkpoint_fallback = {
        7: "Map change, no target from this function",
        17: "Map change, no target from this function",
        29: "Map change, no target from this function",
        35: "Second trial, no target from this function",
        42: "Map change, no target from this function",
    }


class GagazetPeak(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [943, -1055],
        1: [860, -994],
        2: [787, -839],
        # Mi'ihen agency scene, no target from this function
        4: [779, -695],
        5: [844, -551],
        # Map change, no target from this function
        7: [-135, -669],
        8: [129, -534],
        9: [139, -448],
        10: [107, -386],
        11: [47, -310],
        12: [-151, -181],
        13: [-204, -119],
        14: [-295, 123],
        15: [-303, 382],
        16: [-320, 450],
    }
    checkpoint_fallback = {
        3: "Mi'ihen agency scene, no target from this function",
        6: "Map change, no target from this function",
    }
