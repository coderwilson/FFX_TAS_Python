from paths.base import AreaMovementBase


class Besaid1(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-263, -390],
        1: [-509, -552],
        2: [72, -31],
        3: [84, -8],
        4: [137, 1],
        5: [250, 5],
        6: [-601, -411],
        # Wakka pushes Tidus
        7: [-229, -359],
        8: [64, -612],
        9: [64, -612],
        10: [64, -612],
        11: [206, -679],
        12: [236, -699],
        13: [262, -702],
        14: [280, -700],
        15: [307, -691],
        16: [412, -646],
        17: [439, -631],
        18: [488, -459],
        # Pillar, before the big open area.
        19: [498, -414],
        # Adjust to best trigger for piranhas
        20: [480, -37],
        # Adjust to best trigger for piranhas
        21: [480, 100],
        # Hilltop
        22: [73, -49],
        23: [0, -182],
        24: [-10, -226],
        25: [-9, -270],
        26: [20, -374],
        27: [82, -534],
        28: [75, -700],
        # Enter Besaid village
        29: [-18, 444],
        30: [-22, 186],
        31: [-16, 14],
        32: [-8, -59],
        33: [-5, -179],
        # Temple
        35: [38, 27],
        36: [0, -124],
        37: [0, -180],
        38: [-13, -69],
        39: [-15, -5],
        40: [-17, 50],
        41: [-51, 202],
        42: [-79, 292],
        # Into Wakka's tent
        # Sleep tight.
        # Exit the tent
        46: [-51, 202],
        47: [-17, 50],
        48: [-15, -5],
        49: [-13, -69],
        50: [0, -200],
        # The Precepts must be obeyed!
        51: [0, 30],
    }
    checkpoint_fallback = {
        34: "Temple",
        43: "Into Wakka's tent",
        44: "Sleep tight.",
        45: "Exit the tent",
    }


class BesaidTrials(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-20, 126],
        # First glyph
        2: [-11, 116],
        # Second glyph
        4: [7, 117],
        5: [45, 123],
        6: [67, 133],
        # Pick up Besaid sphere
        8: [41, 146],
        9: [-4, 143],
        10: [-14, 133],
        11: [-17, 104],
        # Insert Besaid sphere
        13: [-22, 78],
        14: [-16, 68],
        15: [34, 52],
        16: [37, 43],
        17: [34, -29],
        18: [22, -36],
        19: [-6, -32],
        # Touch the hidden door glyph
        21: [-17, -24],
        22: [-15, 17],
        # Besaid sphere
        24: [-14, -26],
        25: [-10, -50],
        # Insert Besaid sphere, and push to completion
        # Back from the temple
        27: [0, -107],
        28: [0, -130],
        29: [-19, -52],
        30: [-16, -17],
        31: [-13, 76],
        # Approach Valefor's first scene
        32: [0, 200],
        # Night scene
        33: [15, 194],
        # Talk to Yuna
        35: [-3, 174],
        # Sleep tight
        37: [340, 15],
        38: [343, 105],
        # Dream about girls
        # Ready to leave village.
        40: [7, 24],
        41: [4, -46],
        42: [0, -200],

        # Destro sphere items
        50: [-31,70],
        # 51, Grab used sphere
        52: [56,3],
        # 53, Insert orb, open door
        54: [56,3],
        55: [36,-37],
        56: [54,4],
        57: [85,3],
        # 58, pick up destro sphere
        59: [54,4],
        60: [36,-37],
        61: [-14,-33],
        62: [-16,10],
        # 63, insert destro sphere
        64: [-16,10],
        65: [-14,-33],
        66: [-71,-32],
        67: [-75,45],
        # 68, open destro chest
        69: [-71,-32],
        70: [-17,-40],
        71: [-14.5,-58],
        72: [-13.5,-82.5],
    }
    checkpoint_fallback = {
        1: "First glyph",
        3: "Second glyph",
        7: "Pick up Besaid sphere",
        12: "Insert Besaid sphere",
        20: "Touch the hidden door glyph",
        23: "Besaid sphere",
        26: "Insert Besaid sphere, and push to completion",
        34: "Talk to Yuna",
        36: "Sleep tight",
        39: "Dream about girls",
    }


class Besaid2(AreaMovementBase):
    checkpoint_coordiantes = {
        # Back into the village
        1: [7, 413],
        2: [42, 375],
        # Tent 1
        4: [-2, 5],
        # Shopkeeper
        6: [-2, -18],
        # Exit tent
        8: [-76, 223],
        # Tent 2
        10: [-3, -4],
        # Good doggo
        12: [-4, -19],
        # Exit tent
        14: [-37, 406],
        15: [-12, 502],
        # Exit the front gates
        # Outside village
        17: [63, -469],
        # First tutorial
        19: [-10, -270],
        20: [-17, -245],
        21: [-1, -189],
        22: [43, 21],
        # Second tutorial
        # Hilltop
        25: [-24, 124],
        26: [0, 250],
        27: [26, -85],
        28: [97, 33],
        29: [65, 84],
        30: [-12, 183],
        31: [-40, 300],
        # Waterfalls
        32: [-803, 39],
        33: [-686, 78],
        34: [-630, 91],
        35: [-570, 91],
        36: [-499, 80],
        37: [-334, 43],
        38: [-245, 36],
        39: [-186, 21],
        40: [-109, -27],
        41: [-27, -71],
        42: [26, -93],
        43: [90, -120],
        44: [159, -133],
        45: [215, -123],
        46: [253, -108],
        47: [354, -2],
        48: [410, 96],
        49: [453, 197],
        50: [490, 300],
        # Weird T screen
        51: [-23, 48],
        52: [-19, 29],
        53: [-40, -9],
        54: [-31, -17],
        55: [14, -4],
        56: [43, -31],
        57: [56, -44],
        58: [80, -150],
        # Beach
        59: [-318, -472],
        # Save sphere
        61: [-265, -389],
        62: [-212, -339],
        63: [105, -72],
        64: [306, -58],
        65: [329, -39],
        66: [357, 13],
        67: [425, -4],
        68: [425, 50],
        69: [425, 90],
    }
    checkpoint_fallback = {
        0: "Back into the village",
        3: "Tent 1",
        5: "Shopkeeper",
        7: "Exit tent",
        9: "Tent 2",
        11: "Good doggo",
        13: "Exit tent",
        16: "Exit the front gates",
        18: "First tutorial",
        23: "Second tutorial",
        24: "Hilltop",
        60: "Save sphere",
    }
