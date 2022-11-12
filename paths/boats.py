from paths.base import AreaMovementBase


class BoatsLiki(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [5, 176],
        # Group around Yuna
        2: [-22, 90],
        # Talk to Wakka
        4: [-15, 127],
        5: [0, 350],
    }
    checkpoint_fallback = {
        1: "Group around Yuna",
        3: "Talk to Wakka",
    }


class BoatsWinno(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [11, 61],
        1: [11, 150],
        2: [-34, -50],
        3: [-42, -59],
        4: [-35, -66],
        5: [-26, -67],
        # Start Lulu/Wakka conversation
        6: [0, 0],
        7: [-43, -17],
        8: [-34, 12],
        9: [-23, 85],
        10: [0, 152],
        11: [0, 152],
        12: [22, 104],
    }
