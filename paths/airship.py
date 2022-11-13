from paths.base import AreaMovementBase


class Airship(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [17, 47],
        1: [25, 32],
        2: [0, 0],  # Room to room
        3: [-7, 72],  # Screen with guardians
        4: [-3, 11],
        5: [20, -100],
        6: [33, 53],  # Screen with Isaaru
        7: [22, 22],
        8: [-10, -10],
        9: [0, -40],  # Gallery
        10: [-10, -79],
        11: [-19, -86],
        12: [-33, -86],
        13: [-33, -57],
        14: [-35, 7],
        15: [-11, 70],  # Split to specific pattern here if necessary
        16: [999, 999],  # Map change
        17: [-4, -8],
        18: [999, 999],  # Up the lift
        19: [999, 999],  # Completion states
        # 20-22
        23: [-29, -6],
        # 24?
        25: [-32, -7],
        26: [-33, -57],
        27: [-33, -86],
        28: [-19, -86],
        29: [-10, -79],
        30: [0, -9],
        31: [0, 0],  # Transition to next map
        32: [51, 75],
        33: [76, 83],
        34: [0, 0],  # Transition to next map
        35: [2, 50],
        36: [3, 167],
        37: [0, 0],  # Transition to next map
        38: [38, 93],
        39: [52, 113],
        40: [0, 0],  # Back into cockpit
        41: [-241, 195],
        42: [-242, 316],
        43: [-245, 327],
        44: [0, 0],  # Cid
        45: [-245, 327],  # non-CSR
        46: [0, 0],  # non-CSR Cid
    }
