from paths.base import AreaMovementBase


class GuadoStart(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-4, -5],
        1: [-21, 40],
        2: [-21, 83],
        3: [-2, 174],
        4: [0, 0],  # Into the door
        5: [-1, -111],
        6: [0, 0],  # Back out the door.
        7: [20, 24],
        8: [0, 0],  # Into the dining hall
        9: [8, -102],  # Skipped
        10: [0, 0],  # Talk to Auron or Wakka depending on CSR
        11: [0, 0],  # Talk to Wakka or Lulu depending on CSR
        12: [0, 0],  # Talk to Lulu or Auron depending on CSR
        13: [-9, -71],  # non-CSR only, walk around Lulu towards Rikku
        14: [14, -60],  # non-CSR only, walk around Lulu towards Rikku
        15: [21, -52],  # Two branches rejoin (csr vs non-csr)
        16: [20, -29],
        17: [16, -28],
        18: [0, 0],  # Talk to Rikku
        19: [32, -28],
        20: [0, 0],  # Talk to Yuna
    }


class GuadoStoryline(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-8, 109],
        1: [0, 0],  # Dialog with party
        2: [-56, 110],
        3: [-56, 110],
        4: [-56, 110],
        5: [-56, 110],
        6: [-82, 51],
        7: [-84, -3],
        8: [-50, -11],
        9: [-3, 9],
        10: [46, 34],
        11: [120, 92],
        12: [0, 0],  # Towards the farplane
        13: [-9, 11],
        14: [0, 0],  # Chest
        15: [-5, 101],
        16: [0, 0],  # Screen to screen
        17: [0, 0],  # Approach party
        18: [-1, 35],
        19: [-1, 88],
        20: [-4, 152],
        21: [0, 0],  # Into the farplane
        22: [-44, 0],
        23: [0, 0],  # Wakka convo
        24: [-26, -65],
        25: [0, 0],  # Yuna convo
        26: [64, 41],
        27: [31, 30],
        28: [-12, 9],
        29: [-54, -9],
        30: [-85, 0],
        31: [-66, 84],
        32: [-33, 115],
    }


class GuadoSkip(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [4, 0],
        1: [-59, 80],
        2: [-59, 97],
        3: [-43, 105],
        4: [-33, 92],
        # Test if skip was successful
        6: [-24, 61],
        7: [-43, 55],
        8: [-60, 83],
        9: [-80, 137],
        10: [-78, 166],
        11: [-70, 250],
        # 12-17?
        18: [-24, 61],
        19: [-43, 55],
        20: [-44, 56],  # Guado skip failed
        # Shelinda scene
        22: [-18, 96],
        23: [-25, 144],
        # Back to the party
        25: [-33, 92],
        26: [-24, 61],
        27: [-43, 55],
        28: [-60, 83],
        29: [-80, 137],
        30: [-78, 166],
        31: [-70, 250],
    }
    checkpoint_fallback = {
        5: "Test if skip was successful",
        20: "Guado skip failed",
        21: "Shelinda scene",
        24: "Back to the party",
    }
