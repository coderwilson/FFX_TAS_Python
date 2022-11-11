from pathing import AreaMovementBase


class Miihen1(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-15, 203],
        1: [-44, 419],
        2: [-49, 496],
        3: [-39, 538],
        4: [-10, 900],
        5: [-47, 1351],
        # Attempting Mi'ihen skip
        11: [17, 1536],
        12: [24, 1601],
        13: [0, 1796],
        14: [0, 2200],
        15: [-12, 629],
        16: [0, 895],
        17: [-9, 1222],
        18: [0, 1417],
        19: [0, 2000],
        20: [-22, 774],
        21: [-3, 1155],
        22: [-11, 1621],
        23: [-8, 2078],
        24: [5, 2369],
        25: [0, 2682],
        26: [-22, 2783],
        # Shelinda
        28: [5, 2982],
        29: [2, 3088],
        30: [0, 3500],
        31: [0, -227],
    }
    checkpoint_fallback = {
        range(6, 10): "Attempting Mi'ihen skip",
        27: "Shelinda",
    }


class MiihenAgency(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [26, -23],
        1: [15, -30],
        # Go for P.downs if less than 10.
        2: [-2, -27],
        # Talk to lady and purchase downs.
        3: [-2, -27],
        4: [-2, -56],
        5: [-10, -90],
    }
    checkpoint_fallback = {}


class MiihenLowroad(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [35, -932],
        1: [43, -919],
        # Touching save sphere
        3: [37, -903],
        4: [69, -805],
        5: [85, -742],
        6: [142, -616],
        7: [175, -515],
        8: [190, -417],
        9: [174, -355],
        10: [62, -244],
        11: [19, -178],
        12: [17, -153],
        13: [17, -16],
        14: [39, 33],
        15: [59, 59],
        16: [100, 100],
        # Second low road map
        17: [357, 120],
        18: [403, 129],
        19: [467, 152],
        20: [537, 176],
        21: [586, 212],
        22: [638, 258],
        23: [679, 299],
        24: [715, 378],
        # Last checkpoint before reviewing for Self Destruct
        25: [732, 448],
        26: [738, 481],
        27: [780, 530],
        # Final map, meeting Seymour
        28: [158, -209],
        29: [59, -104],
        30: [9, -44],
        31: [-41, 36],
        32: [-42, 152],
        33: [-57, 288],
        # Talk to the guard
        35: [-57, 288],
        36: [-50, 400],
    }
    checkpoint_fallback = {
        2: "Touching save sphere",
        34: "Talk to the guard",
    }
