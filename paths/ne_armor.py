from paths.base import AreaMovementBase


class NEApproach(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [121, 120],
        1: [122, 134],
        2: [113, 150],
        3: [-35, 167],
        4: [-200, 170],
        5: [-228, 228],
        6: [-278, 172],
        7: [-328, 150],
        8: [-385, 168],
        9: [-250, 10],
    }


class NEForceEncountersWhite(AreaMovementBase):
    @classmethod
    def execute(cls, checkpoint: int):
        if checkpoint % 2 == 0:
            return [0, 70]
        return [0, 20]


class NEForceEncountersGreen(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [0, 70],
        1: [0, 170],
        2: [0, 170],
        3: [0, 170],
        4: [13, 186],
        5: [67, 251],
        6: [95, 271],
        7: [153, 287],
        8: [298, 283],
        9: [353, 307],
        10: [389, 335],
        11: [416, 382],
        12: [430, 438],
        13: [431, 484],  # Light area 1
        14: [458, 505],  # Light area 2
    }


class NEReturnGreen(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [428, 452],
        1: [421, 405],
        2: [411, 370],
        3: [384, 327],
        4: [341, 300],
        5: [297, 285],
        6: [208, 281],
        7: [114, 278],
        8: [73, 261],
        9: [6, 177],
        10: [0, 0],
    }


class NEReturn(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [0, -100],
        1: [-305, 168],
        # 2?
        3: [-282, 189],
        4: [-231, 230],
        5: [-223, 243],
        6: [-220, 350],
        7: [-2, 163],
        8: [91, 150],
        9: [120, 144],
        10: [126, 134],
        11: [119, 122],
        12: [109, 111],
        13: [64, 95],
        14: [8, 105],
        15: [-4, 106],
        16: [-12, 116],
        17: [-11, 174],
        18: [-9, 214],
        19: [-6, 254],
        20: [4, 290],
        21: [17, 550],  # Through the trigger to Gagazet gates
        22: [100, 800],  # Safety
    }
    checkpoint_fallback = {}


class GagazetNELoopback(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [33, 197],
        1: [22, -64],
        2: [18, -198],
        3: [24, -300],
        4: [11, -354],
        5: [5, -396],
        6: [-7, -445],
        7: [-33, -473],
        8: [-78, -521],
        9: [-111, -536],
        10: [-140, -591],
        11: [-168, -645],
        12: [-190, -800],  # Transition to previous map
        13: [21, 366],
        14: [-8, 238],
        15: [-9, 190],
        16: [-10, 108],
        17: [7, 94],
    }
    checkpoint_fallback = {}
