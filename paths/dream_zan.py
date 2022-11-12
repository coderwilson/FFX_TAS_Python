from paths.base import AreaMovementBase


class TidusHomeMovement(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [181, -1],
        1: [146, 1],
        2: [115, 1],
        3: [60, 6],
        4: [28, 5],
        6: [13, 3],
        7: [10, -5],
        9: [6, -1],
        # Finish the first section
        10: [-30, -1],
        # Start the second section
        11: [426, -3],
        12: [426, -3],
        13: [426, -3],
        14: [426, -3],
        15: [426, -3],
        # Ready for bridge
        16: [426, -3],
        17: [147, -30],
        18: [54, -33],
        19: [-62, -62],
        20: [-200, -100],
        21: [0, 880],
        22: [0, 830],
        23: [0, 700],
        24: [2, 838],
        25: [14, 940],
        26: [32, 1200],
        27: [2, 940],
        28: [2, 1200],
    }
    checkpoint_fallback = {
        0: "Testing!",
        5: "Talk to the kids",
        8: "Talk to the girls",
    }


class AllStartsHere(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [849, -92],
        1: [885, -101],
        2: [905, -149],
        3: [918, -179],
        4: [957, -219],
        5: [987, -257],
        7: [1003, -253],
        8: [1100, -350],
        9: [16, -67],
        10: [16, -67],
        11: [79, -457],
        12: [99, -383],
        13: [95, -171],
        14: [68, 24],
        15: [6, 348],
        16: [-3, 492],
        17: [-6, 559],
        18: [-39, 610],
        19: [-72, 642],
        20: [-80, 680],
    }
    checkpoint_fallback = {
        6: "Save sphere",
    }
