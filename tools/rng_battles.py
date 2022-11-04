# currently unused file, should be removed if abandoned
import memory.main


def all_formations(area: int):
    if area == 10:  # Kilika
        return [31, 31, 32, 32, 33, 33, 34, 34, 35, 35, 35, 36, 37]
    if area == 69:  # Zanarkand, outdoors
        return [356, 357, 358, 359, 360]
    if area == 70:  # Zanarkand, indoors
        return [361, 361, 361, 362, 363, 364, 365, 366]
    if area == 77:  # Sea of Sorrows
        return [374, 374, 375, 375, 376, 376, 376, 377, 377, 378]
    if area == 79:  # City of Dying Dreams
        return [380, 381, 382, 383, 384, 385, 386, 387]


def coming_battles(area: int = 10, battle_count: int = 10, extra_advances: int = 0):
    formations = all_formations(area)
    advances = memory.main.rng_01_advances((battle_count * 2) + extra_advances)
    if extra_advances != 0:
        while extra_advances != 0:
            del advances[0]
            extra_advances -= 1
    battles = []
    for i in range(battle_count):
        next_value = formations[(advances[(i * 2) + 1] & 0x7FFFFFFF) % len(formations)]
        battles.append(next_value)
    print("Upcoming battles:", battles)
    print("=========================")
    return battles
