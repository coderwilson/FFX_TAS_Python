from paths.base import AreaMovementBase


class BesaidFarm(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-345, -470],
        1: [0, 0],  # Map change
        2: [51, -34],
        3: [13, 2],
        4: [-15, -21],
        5: [-38, -19],
        6: [-35, 2],
        7: [-22, 24],
        8: [-16, 43],
        9: [-35, 57],
        10: [-67, 69],
        11: [0, 0],  # Map to map
        12: [424, 122],
        13: [369, 5],
        14: [424, 122],
        15: [454, 199],
        16: [5000, 3000],  # Back to previous map
        17: [-22, 52],
        18: [-12, 25],
        19: [-38, -2],
        20: [-31, -20],
        21: [4, -11],
        22: [18, 0],
        23: [64, -28],
        24: [70, -73],
        # TODO: Unused?
        25: [0, 0],  # Back to beach
        26: [0, 0],
        27: [0, 0],
        28: [0, 0],
        29: [0, 0],
        30: [0, 0],
    }


class KilikaFarm(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [23, -255],
        1: [-17, -247],
        2: [-27, -207],
        3: [-34, -170],
        4: [0, 0],  # To next map
        5: [85, 90],
        6: [0, 119],
        7: [-112, 114],
        8: [-124, 137],
        9: [-158, 210],
        10: [-150, 259],
        11: [-130, 350],  # To the woods
        12: [-67, -451],
        13: [-84, -527],
        14: [-100, -600],  # Return if complete
        15: [-152, 195],
        16: [-118, 115],
        17: [-97, 103],
        18: [-4, 109],
        19: [91, 97],
        20: [91, 37],
        21: [0, 0],  # Back to save sphere screen
        22: [-48, -201],
        23: [-3, -248],
        24: [31, -258],
        25: [0, 0],
        26: [0, 0],
        27: [0, 0],
        28: [0, 0],
        29: [0, 0],
        30: [0, 0],
    }


class MiihenFarm(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [13, -26],
        1: [-8, -59],
        2: [-8, -90],  # Exit agency
        3: [50, -185],
        4: [40, -173],
        5: [26, -103],
        6: [-15, 302],
        7: [-15, 302],
        8: [-57, 600],  # To the map with encounters
        9: [-173, -815],
        10: [-159, -715],
        11: [-117, -623],
        12: [-46, -501],
        13: [39, -357],
        14: [136, -170],
        15: [136, -170],  # Bridge
        16: [162, -30],
        17: [142, 44],
        18: [100, 180],  # Into next zone
        19: [20, 294],
        20: [21, 376],
        21: [127, 471],
        22: [181, 462],
        23: [212, 430],
        24: [192, 348],
        25: [221, 282],
        26: [288, 222],
        27: [426, 249],
        28: [605, 343],
        29: [610, 470],  # Dismount Chocobo
        30: [610, 461],  # Farm zone 1
        31: [593, 552],  # Farm zone 2
        32: [500, 700],  # To the "meeting Seymour" screen
        33: [-300, -305],  # Return to newroad
        34: [-107, -250],  # Branch to zone 2 vs zones >= 3
        35: [-68, -69],
        36: [14, -68],  # Entrance towards area 2
        37: [185, -223],
        38: [227, -274],
        39: [270, -320],  # Into lower area
        40: [800, 650],  # Return
        41: [708, 335],
        42: [740, 450],
        43: [800, 650],  # Return to map
        44: [172, -219],
        45: [47, -107],
        46: [14, -40],  # Branch to zone 1 vs zones >= 3
        47: [2, 109],
        48: [2, 109],  # Save sphere, touch if needed.
        49: [-45, 193],
        50: [-42, 318],
        51: [-42, 600],  # To MRR start area
        52: [-87, -1100],  # Farm area 3(A)
        53: [-87, -911],  # Farm area 3(A)
        54: [-46, -817],
        55: [-44, -716],
        56: [-48, -643],
        57: [-23, -571],
        58: [-38, -492],
        59: [-115, -476],  # Farm area 3(B)
        60: [-209, -420],  # Farm area 3(B)
        61: [-300, -350],  # To MRR map
        62: [21, -725],  # Farm area 4
        63: [52, -690],  # Farm area 4 and save sphere
        64: [66, -850],  # Back to Clasko map
        65: [-118, -469],
        66: [-52, -487],
        67: [-17, -562],
        68: [-43, -639],
        69: [-53, -694],
        70: [-43, -722],
        71: [-56, -850],
        72: [-79, -950],
        73: [-90, -1100],  # Back to transition map
        74: [-56, 255],
        75: [-32, 174],
        76: [4, 132],
        77: [-3, 22],  # Save sphere, and back towards areas 1/2
        78: [-58, -105],  # Back towards area 1
        79: [-144, -247],
        80: [-230, -330],  # Map change
        # 80-89?
        90: [-39, -236],  # Area 6 back to 5 logic
        91: [-53, -274],  # Area 6 back to 5 logic
        # Down the lift
        92: [-53, -274],  # Area 6 back to 5 logic
        93: [66, 874],  # Area 6 back to 5 logic
        # 94-99?
        100: [12, -738],  # Start, area 5/6 logic
        101: [12, -738],
        102: [-28, -663],
        103: [-37, -601],
        # First lift
        105: [-48, -571],
        106: [-108, -463],
        107: [-108, -428],
        108: [-85, -391],
        109: [-87, -372],
        110: [-78, -361],
        111: [-38, -367],
        112: [-6, -381],
        113: [38, -414],
        114: [63, -398],
        115: [109, -339],
        116: [127, -198],
        117: [122, -166],
        118: [91, -176],
        119: [0, -215],
        120: [-63, -189],
        121: [-88, -141],
        122: [-104, 54],
        123: [-102, 73],
        124: [-86, 87],
        125: [25, 138],
        126: [32, 151],
        127: [23, 233],
        128: [-89, 295],
        129: [-91, 321],
        130: [-87, 368],
        131: [-68, 402],
        132: [-48, 425],
        133: [35, 461],
        134: [92, 515],
        135: [51, 543],
        136: [-20, 568],
        137: [-71, 593],
        138: [-109, 604],
        139: [-115, 687],
        140: [-71, 775],
        141: [-39, 829],
        142: [-12, 838],
        143: [26, 828],
        144: [44, 834],
        145: [59, 898],
        # Second lift
        147: [-36, -194],
        148: [-36, -194],
        149: [24, -157],
        150: [52, -135],
        151: [116, 4],
        152: [121, 50],
        153: [112, 100],
        154: [29, 227],
        155: [29, 227],
        156: [29, 227],
        157: [29, 227],
        # Up the third lift
        159: [59, 244],
        160: [99, 254],
        161: [198, 251],
        162: [219, 202],
        163: [226, 170],  # Diagonal towards the save sphere
        200: [70, -192],  # Early Miihen section
        201: [25, -256],
        202: [-26, -374],
        203: [-50, -600],  # Map change
        204: [-30, 3300],  # Reverse map change
        205: [20, 3116],
        206: [29, 3049],
    }
    checkpoint_fallback = {
        104: "First lift",
        146: "Up the second lift",
        158: "Up the third lift",
    }


class ArenaReturn(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-635, -137],
        1: [-637, -245],
        2: [97, -298],
        3: [553, -245],
        4: [1308, -138],
        5: [1398, -129],
        6: [1500, -250],
        7: [0, 0],
        8: [0, 0],
        9: [0, 0],
        10: [0, 0],
    }


class YojimboFarm(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [1, 23],
        1: [26, -207],
        2: [17, -357],
        3: [-20, -474],
        4: [-98, -523],
        5: [-300, -800],  # To Defender X map
        6: [-8, 227],
        7: [-11, 94],
        8: [120, 105],
        9: [120, 105],
        10: [120, 105],
        11: [143, 155],
        12: [80, 173],
        13: [-52, 186],
        14: [-250, 185],  # To gorge map
        15: [-224, 204],
        16: [-282, 155],
        17: [-378, 132],
        18: [-378, 132],
        19: [-450, 300],  # Into the cave
        20: [-3, -25],  # Back out of cave
        21: [-3, 25],
        22: [8, 182],
        23: [75, 273],
        24: [309, 284],
        25: [392, 326],
        26: [418, 385],  # White 1
        27: [430, 440],  # White 2
        28: [424, 481],  # Green 1
        29: [451, 507],  # Green 3
        30: [435, 510],  # Onward TODO: buffer needed? Can remove?
        31: [435, 510],
        32: [435, 510],
        33: [435, 510],
        34: [435, 510],
        35: [435, 510],
        36: [426, 805],  # Conversation with the party
        37: [420, 912],
        38: [387, 934],
        39: [320, 956],
        40: [262, 1038],
        41: [267, 1162],
        42: [251, 1291],
        43: [190, 1291],
        44: [10, 1304],
        45: [-64, 1399],
        46: [-67, 1501],  # Near the chest, hard right.
        47: [36, 1536],  # Save sphere
        48: [106, 1633],
        49: [94, 1823],
        50: [93, 1927],
        51: [93, 1961],  # On the platform.
        52: [0, 0],  # Teleport to boss room
        53: [0, 0],  # Talking to Yojimbo's fayth
        54: [93, 1961],
        55: [0, 0],  # Teleport to start.
        56: [0, 164],
        57: [5, 88],
        58: [-8, 11],
        59: [-5, -50],  # Back to gorge map
        60: [-378, 132],
        61: [-313, 163],
    }


class DjoseFarm(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [491, -126],
        1: [488, 11],
        2: [503, 47],
        3: [605, 26],
        4: [826, 19],
        5: [950, 56],
        6: [1040, 150],
        7: [1300, 300],  # Map to map
        8: [-238, -950],  # Return
        9: [-235, -661],
        10: [-186, -405],
        11: [-117, -164],
        12: [-64, 40],
        13: [-40, 75],
        14: [30, 214],
        15: [138, 409],
        16: [212, 479],
        17: [298, 577],
        18: [456, 714],
        19: [536, 746],
        20: [617, 803],
        21: [642, 847],
        22: [615, 983],
        23: [536, 967],
        24: [550, 1100],  # To next zone
        25: [-600, 2200],  # Return
        26: [-977, 1705],
        27: [-875, 1824],
        28: [-775, 1950],  # Back to previous map
        29: [631, 858],
        30: [750, 861],
        31: [900, 870],  # To the temple map
        32: [37, -139],
        33: [38, -111],
        34: [64, -18],
        35: [22, 164],
        36: [0, 300],  # Map to map
        37: [88, -263],
        38: [0, 0],
        39: [20, -353],  # Start heading back
        40: [0, -450],  # Back to bridge map
        41: [43, 73],
        42: [45, 16],
        43: [58, -30],
        44: [53, -124],
        45: [-2, -277],
        46: [-50, -440],  # Back to area 1
        47: [623, 850],
    }


class MacFarm(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [19, -23],
        1: [-9, -61],
        2: [-14, -150],  # Exit agency
        3: [52, -34],
        4: [121, -33],
        5: [176, 60],  # Edge of snow zone
        6: [250, 200],  # Leave lake area
        7: [-100, -100],  # Return path
        8: [51, -41],
        9: [146, -84],
        10: [199, -105],  # Past save sphere
        11: [300, -120],  # Exit to woods area
        12: [-700, -150],  # Back to save sphere map
        13: [-596, -20],
        14: [-643, -82],
        15: [-700, -150],  # Back to save sphere map
        16: [214, -111],
        17: [146, -84],
        18: [95, -57],
        19: [33, -34],
        20: [-150, -150],  # North to lake
        21: [0, 0],
    }


class ThunderPlainsFarm(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-28, -23],
        1: [-28, -23],
        2: [6, -54],
        3: [10, -200],  # Outside agency
        4: [-180, 35],  # Into agency
        5: [-56, 39],
        6: [-47, 67],
        7: [0, 300],  # To North
        8: [-115, -1400],  # Back to agency front
        9: [-127, -1083],  # North pos 1
        10: [-106, -1185],  # North pos 2
        11: [-115, -1400],  # Back to agency front
        12: [0, 300],  # To North
        13: [-47, 67],
        14: [-61, -4],
        15: [-70, -150],  # To South
        16: [4, 1300],  # Back to agency front
        17: [-44, 1075],  # South pos 1
        18: [16, 1116],  # South pos 2
        19: [16, 1116],
        20: [16, 1116],
    }


class BikanelFarm(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-11, -96],
        1: [9, -244],
        2: [54, -384],
        3: [93, -399],
        4: [197, -394],
        5: [300, -390],  # Second map
        6: [200, -900],  # Back to first map
        7: [-49, -584],
        8: [-222, -459],
        9: [-170, -313],
        10: [-20, -296],
        11: [155, -220],
        12: [186, -122],
        13: [166, 3],
        14: [157, 38],
        15: [181, 71],  # Past Rikku tent
        16: [238, 110],
        17: [343, 102],
        18: [611, 141],
        19: [669, 255],
        20: [652, 542],
        21: [625, 789],  # Sign post
        22: [705, 870],
        23: [800, 1000],  # Into big map (the first one)
        24: [490, -770],
        25: [400, -438],
        26: [17, 88],
        27: [-116, 265],
        28: [-263, 305],
        29: [-312, 387],  # Just before the danger zone
        30: [-350, 470],  # Now in the danger zone
        31: [-363, 583],  # Danger zone 2
        32: [-522, 649],  # Onward (if needed) to the other zone
        33: [-656, 752],
        34: [-660, 900],  # Into the West zone
        35: [-310, -235],
        36: [-447, -188],
        37: [-700, -300],  # Back to ruins
        38: [-587, 632],
        39: [-439, 547],
        40: [-343, 461],  # Around danger zone 2
        41: [-305, 399],
        42: [-266, 341],
        43: [-149, 293],
        44: [-30, 249],
        # TODO: Unused?
        45: [0, 0],  # Back to airship
        46: [0, 0],
        47: [0, 0],
        48: [0, 0],
        49: [0, 0],
        50: [0, 0],
    }


class SinFarm(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [240, -244],
        1: [240, -300],  # To Sea of Sorrows
        2: [300, -1100],  # Back to save
        3: [182, -942],
        4: [100, -825],
        5: [119, -770],
        6: [234, -687],
        7: [289, -606],
        8: [331, -478],
        9: [384, -392],
        10: [358, -315],
        11: [274, -274],
        12: [155, -261],
        13: [66, -242],
        14: [13, -224],
        15: [-7, -204],
        16: [-8, -133],
        17: [17, -32],
        18: [28, 36],
        19: [-33, 69],
        20: [-178, 56],
        21: [-207, 64],
        22: [-294, 121],
        23: [-325, 144],
        24: [-322, 177],
        25: [-232, 298],
        26: [-85, 392],
        27: [39, 461],
        28: [153, 491],
        29: [205, 485],
        30: [257, 395],
        31: [272, 350],
        32: [326, 315],
        33: [376, 308],
        34: [414, 369],
        35: [389, 503],
        36: [377, 606],
        37: [370, 698],
        38: [351, 710],
        39: [252, 756],
        40: [227, 780],
        41: [220, 929],
        42: [216, 976],  # Save sphere
        43: [218, 1100],  # Forwards towards Seymour
        44: [414, -888],  # Back towards Seymour
        45: [369, -713],
        46: [416, -714],
    }


class OmegaFarm(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-105, -1030],
        1: [-55, -943],
        2: [-109, -1055],
        3: [0, 0],  # Return to airship
        4: [0, 0],
        5: [0, 0],
        6: [0, 0],
        7: [0, 0],
        8: [0, 0],
        9: [0, 0],
        10: [0, 0],
    }


class ZanarkandFarm2(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [126, 3],
        1: [108, -60],
        2: [138, -85],
        3: [154, -98],
        4: [350, -200],  # Zone to Zone
        5: [-14, -1100],  # Return
        6: [1, -944],
        7: [16, -879],
    }
