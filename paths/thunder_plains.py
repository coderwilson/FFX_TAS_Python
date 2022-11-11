from pathing import AreaMovementBase


class ThunderPlainsSouth(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-23, -1023],
        1: [-32, -973],
        2: [-24, -927],
        3: [1, -840],
        4: [-3, -663],
        5: [-7, -635],  # Past crater
        6: [5, -522],
        7: [-12, -290],
        8: [3, 4],
        9: [7, 362],
        10: [12, 495],
        11: [45, 787],
        12: [54, 865],
        13: [54, 1200],
        # 14-19?
        # Nemesis route changes significantly.
        20: [-44, -887],  # Touch save sphere
        21: [0, 0],
        22: [-57, -872],
        23: [-101, -739],
        24: [-170, -491],
        25: [0, 0],  # Touch cactuar stone 1
        26: [-63, -361],
        27: [-20, -152],
        28: [2, 9],
        29: [63, 98],
        30: [114, 193],
        31: [185, 204],
        32: [204, 166],
        33: [0, 0],  # Touch cactuar stone 2
        34: [0, 0],  # Count 50 dodges
        35: [188, 187],
        36: [116, 223],
        37: [116, 339],
        38: [58, 380],
    }
    checkpoint_fallback = {}


class ThunderPlainsAgency(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [4, -36],
        1: [0, 0],  # Agency shop
        2: [21, -28],
        3: [29, -10],
        4: [0, 0],  # Scene with Yuna
        5: [31, -17],
        6: [25, -36],
        7: [0, 0],  # Talk to Kimahri, affection manip
        8: [0, 0],  # Talk to Rikku to leave the agency
        9: [-59, 19],
        10: [-44, 99],
        11: [0, 0],  # Lightning shield, and exit to North pathing.
    }
    checkpoint_fallback = {}


class ThunderPlainsNorth(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-102, -1162],
        1: [-92, -1066],
        2: [-54, -870],
        3: [-16, -649],
        4: [16, -498],
        5: [26, -426],
        6: [44, -396],
        7: [57, -324],
        8: [72, -304],
        9: [76, -261],
        10: [79, -134],
        11: [79, -18],
        12: [70, 0],
        13: [52, 123],
        14: [-52, 414],  # any% only (non-CSR)
        15: [-26, 451],
        16: [-1, 739],  # Both back on track
        17: [-18, 797],
        18: [-35, 883],
        19: [-37, 967],
        20: [-73, 1025],
        21: [-73, 1300],
    }
    checkpoint_fallback = {}
