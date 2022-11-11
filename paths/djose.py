from pathing import AreaMovementBase


class DjosePath(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-237, -672],
        1: [-191, -450],
        2: [-152, -279],
        3: [-126, -166],
        4: [-126, -166],
        5: [-126, -166],
        6: [-126, -166],
        7: [-126, -166],
        8: [-126, -166],
        9: [-126, -166],
        10: [-126, -166],
        11: [-126, -166],
        12: [-126, -166],
        13: [-126, -166],
        14: [-60, 32],
        15: [-60, 32],
        16: [-60, 32],
        17: [-60, 32],
        18: [-60, 32],
        19: [-60, 32],
        20: [-60, 32],
        21: [-34, 92],
        22: [-34, 92],
        23: [-34, 92],
        24: [-33, 118],
        25: [27, 215],
        26: [38, 232],
        27: [56, 260],
        28: [94, 321],
        29: [111, 349],
        30: [123, 368],
        31: [137, 390],
        32: [157, 422],
        33: [177, 453],
        34: [213, 506],
        35: [234, 521],
        36: [266, 543],
        37: [329, 587],
        38: [337, 593],
        39: [375, 619],
        40: [440, 650],
        41: [447, 651],
        42: [461.5, 658],
        43: [461.5, 658],
        44: [461.5, 658],
        45: [461.5, 658],
        46: [461.5, 658],
        47: [550, 730],  # Point of deferral 1
        48: [489, 730],  # Point of deferral 2
        49: [604, 836],  # Point of continuation
        50: [734, 859],
        51: [0, 0],  # Transition to next map
        52: [27, -231],
        53: [59, -14],
        54: [51, 0],
        55: [9, 151],
        56: [0, 0],  # Transition to temple map
        57: [-4, -87],
        58: [0, 0],  # Transition into temple
    }


class DjoseTrials(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-22, -233],
        # First sphere
        2: [-6, -193],
        # Sphere door
        4: [24, -208],
        # Second sphere
        6: [6, -191],
        # Sphere door
        8: [0, -176],
        9: [0, -58],
        10: [-3, -7],
        11: [-8, 18],
        12: [-19, 42],
        # Left sphere
        14: [34, 31],
        15: [69, 34],
        # Insert left sphere
        17: [31, 30],
        18: [23, 43],
        # Right sphere
        20: [-18, 22],
        21: [-7, 24],
        # Pushing pedestal
        23: [56, 33],
        # Insert right sphere
        # Unused
        # Unused
        27: [57, 34],
        # Left sphere
        29: [14, 27],
        30: [-65, 24],
        # Reset switch
        32: [-41, 24],
        33: [-10, 22],
        # Insert left sphere
        35: [-4, 10],
        36: [9, 15],
        37: [12, 22],
        # Powered sphere
        39: [22, 39],
        # Insert powered sphere
        41: [32, 31],
        42: [66, 28],
        # Right sphere
        44: [8, 24],
        # Insert right sphere
        46: [8, 13],
        47: [0, 16],
        # All the hidden room stuff
        49: [2, 47],
        50: [20, 47],
        # Powered sphere
        52: [-19, 46],
        # Insert powered sphere
        54: [-14, 24],
        55: [-65, 24],
        # Reset switch
        57: [-9, 22],
        # Left sphere
        59: [-2, 1],
        60: [-2, -53],
        61: [-2, -191],
        62: [-26, -216],
        # Final insert Left sphere
        64: [-1, -185],
        65: [3, -9],
        66: [6, 5],
        67: [9, 19],  # Dial in
        # Right sphere
        69: [6, 5],
        70: [3, -9],
        71: [3, -185],
        72: [26, -214],
        # Final insert Right sphere
        74: [3, -185],
        75: [-3, -8],
        76: [-3, 0],
        77: [-4, 4],
        78: [-37, 26],
        79: [-54, 25],
        # Destro glyph
        81: [-62, 55],
        # Destruction Sphere
        83: [-58, 28],
        84: [-11, 28],
        # Ride ze lift
        86: [-11, 110],
        87: [-21, 115],
        # Pedestal 1
        89: [-22, 144],
        # Pedestal 2
        91: [-3, 157],
        # Pedestal 3
        93: [19, 146],
        # Pedestal 4
        95: [20, 117],
        # Pedestal 5
        97: [9, 106],
        98: [8, 70],
        99: [0, 61],
        # Insert destro sphere
        101: [22, 42],
        # Destro chest
        103: [-26, 37],
        # End of Trials
    }
    checkpoint_fallback = {
        1: "First sphere",
        3: "Sphere door",
        5: "Second sphere",
        7: "Sphere door",
        13: "Left sphere",
        16: "Insert left sphere",
        19: "Right sphere",
        22: "Pushing pedestal",
        24: "Insert right sphere",
        25: "Unused",
        26: "Unused",
        28: "Left sphere",
        31: "Reset switch",
        34: "Insert left sphere",
        38: "Powered sphere",
        40: "Insert powered sphere",
        43: "Right sphere",
        45: "Insert right sphere",
        48: "All the hidden room stuff",
        51: "Powered sphere",
        53: "Insert powered sphere",
        56: "Reset switch",
        58: "Left sphere",
        63: "Final insert Left sphere",
        68: "Right sphere",
        73: "Final insert Right sphere",
        80: "Destruction Glyph",
        82: "Destruction Sphere",
        85: "Ride ze lift",
        88: "Pedestal 1",
        90: "Pedestal 2",
        92: "Pedestal 3",
        94: "Pedestal 4",
        96: "Pedestal 5",
        100: "Insert destro sphere",
        102: "Destro chest",
        104: "End of Trials",
    }


class DjoseDance(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [0, -9],
        1: [3, 17],
        2: [16, 24],
        3: [30, 12],
        4: [16, 1],
        5: [-17, 3],
        6: [-26, -13],
        7: [-8, -16],
    }


class DjoseExit(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [11, -149],
        1: [0, 0],  # Talk to Auron
        2: [-1, -88],
        3: [0, 0],  # Enter temple
        4: [-18, 6],
        5: [-41, 56],
        6: [-41, 56],
        7: [-41, 56],
        8: [-52, 94],
        9: [0, 0],  # Enter room where Yuna is resting
        10: [13, -1],
        11: [13, -1],
        12: [0, 0],  # Remedy
        13: [11, 28],
        14: [0, 0],  # Wake up Yuna
        15: [-31, -211],
        16: [-129, -253],
        17: [-178, -261],
        18: [0, 0],  # 4k gold chest
        19: [-131, -287],
        20: [-93, -311],
        21: [-40, -360],
        22: [0, 0],  # Switch maps, to Bridge
        23: [26, 50],
        24: [53, -17],
        25: [58, -52],
        26: [37, -113],
        27: [4, -236],
        28: [-9, -333],
        29: [0, 0],  # Switch map, to Djose road
        30: [626, 858],
        31: [591, 985],
        32: [550, 1100],
        33: [500, 1200],
        34: [0, 0],
        35: [-18, 19],  # Remedy logic
        36: [0, 0],  # Pick up Remedy
        37: [0, 0],
        38: [0, 0],
        39: [0, 0],
        40: [0, 0],
    }
