from paths.base import AreaMovementBase


class CalmLands1(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-332, -1612],
        1: [-437, -1603],
        2: [-640, -1591],
        3: [-757, -1530],
        4: [-777, -1478],
        5: [-761, -1433],  # First divergence from the standard path
        6: [-253, -1038],
        7: [581, -464],
        8: [1223, -187],
        9: [1345, -129],
        10: [1500, -125],
    }


class CalmFarm(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [-634, -126],
        1: [-605, -144],
        2: [-579, -178],  # Zone 1 position 1
        3: [-561, -99],  # Zone 1 position 2
        4: [-503, -60],  # Zone 2 position 1
        5: [-521, 10],  # Zone 2 position 2
        # Zone 3 positions have been nudged slightly north-west
        # after consistently getting a no-encounter loop
        6: [-558, 37],  # Zone 3 position 1
        7: [-630, 41],  # Zone 3 position 2
        8: [-521, 3],
        9: [-550, -97],
    }


class CalmLands2(AreaMovementBase):
    checkpoint_coordiantes = {
        0: [1336, -101],
        1: [1349, 160],
        2: [1429, 486],
        3: [1480, 646],
        4: [1494, 878],
        5: [1542, 1021],
        6: [1561, 1112],
        7: [1600, 1300],
    }
