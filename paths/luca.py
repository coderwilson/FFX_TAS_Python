from pathing import AreaMovementBase


class Luca1(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [126, 381],
        1: [130, 362],
        2: [157, 302],
        3: [189, 285],
        # Map to map
        4: [230, 250],
        # Just before Seymour gets introduced
        5: [328, 63],
        # Seymour intro scene
        7: [0, -200],
        8: [0, -200],  # buffer
        9: [0, -200],  # buffer
        # Luca stadium front
        10: [-256, -76],
        11: [-600, -19],
        # Reverse T map
        12: [187, 18],
        # Reverse T map - into next zone
        13: [300, 10],
        14: [28, -60],
        15: [39, -52],
        16: [53, -36],
        17: [61, -8],
        18: [60, 29],
        19: [21, 90],
        20: [4, 131],
        21: [-1, 161],
        22: [-1, 161],
        # Into the bar
        24: [37, -26],  # buffer
        25: [37, -26],  # buffer
        26: [37, -26],  # buffer
        27: [37, -26],  # buffer
        28: [37, -26],  # buffer
        29: [-4, -30],
        30: [-60, -19],
        31: [-149, -12],
        32: [-257, 10],
        # Back to the front of the Blitz dome
        34: [-395, 38],
        35: [-320, 95],
        # To the docks
        37: [-239, 160],
        38: [-224, 178],
        39: [-195, 203],
        # First battle
        41: [185, 240],
        # Second battle
        43: [281, -75],
        # Third battle
        45: [167, -312],
        # Touch save sphere
        47: [150, -337],
        # Start of Oblitzerator fight
        49: [-8, -311],
        # Screen change
        51: [-304, -53],
        # Screen change
        53: [-293, -87],
        54: [-275, -50],
        # Save sphere and end of section
    }
    checkpoint_fallback = {
        6: "Seymour intro scene",
        23: "Into the bar",
        33: "Back to the front of the Blitz dome",
        36: "To the docks",
        40: "First battle",
        42: "Second battle",
        44: "Third battle",
        46: "Touch save sphere",
        48: "Start of Oblitzerator fight",
        50: "Screen change",
        52: "Screen change",
        55: "Save sphere and end of section",
    }


class LucaPreBlitz(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-270, -56],
        1: [-173, -67],
        2: [20, -67],
        3: [-4, -11],
        4: [-16, -1],
        5: [-61, -9],
        6: [-75, -19],
        7: [-108, -10],
    }
    checkpoint_fallback = {}


class Luca3(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-549, -373],
        1: [-573, -384],
        2: [-582, -378],
        3: [-596, -361],
        4: [-612, -363],
        5: [-636, -381],
        # First chest
        6: [-638, -397],
        7: [-632, -403],
        # First chest
        9: [-621, -417],
        # Second chest
        11: [-627, -404],
        12: [-637, -397],
        13: [-640, -382],
        14: [-602, -362],
        15: [-591, -364],
        16: [-577, -382],
        17: [-563, -380],
        18: [-431, -275],
        19: [-316, -144],
        # Target Auron
        21: [-294, -42],
        # Into registration map
        22: [-220, -10],
        23: [-347, -63],
        24: [-407, -32],
        25: [-500, -32],
        # Upside down T map
        26: [-63, -18],
        27: [-1, -32],
        28: [38, -22],
        29: [164, -4],
        30: [300, 0],
        # Carnival screen
        31: [29, -87],
        32: [65, -32],
        33: [90, 61],
        34: [140, 92],
        # Bring the party together
    }
    checkpoint_fallback = {
        8: "First chest",
        10: "Second chest",
        20: "Target Auron",
        35: "Bring the party together",
    }
