from pathing import AreaMovementBase


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
