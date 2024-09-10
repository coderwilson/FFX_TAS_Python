import logging
from math import copysign, sqrt

import memory.main
import xbox

logger = logging.getLogger(__name__)
FFXC = xbox.controller_handle()


def set_movement(target) -> bool:
    player = memory.main.get_coords()
    (forward, right) = memory.main.get_movement_vectors()

    # Calculate forward and right directions relative to camera space
    pX = player[0]
    pY = player[1]
    eX = target[0]
    eY = target[1]
    fX = forward[0]
    fY = forward[1]
    rX = right[0]
    rY = right[1]

    Ly = fX * (eX - pX) + rX * (eY - pY)
    Lx = fY * (eX - pX) + rY * (eY - pY)
    sums_up = abs(Lx) + abs(Ly)
    if sums_up == 0:
        sums_up = 0.01
    Lx /= sums_up
    Ly /= sums_up
    if abs(Lx) > abs(Ly):
        Ly = copysign(Ly / Lx if Lx else 0, Ly)
        Lx = copysign(1, Lx)
    elif abs(Ly) > abs(Lx):
        Lx = copysign(Lx / Ly if Ly else 0, Lx)
        Ly = copysign(1, Ly)

    FFXC.set_movement(Lx, Ly)
    if memory.main.get_actor_id(0) == 20531:
        d = 10
    else:
        d = 3

    if abs(player[1] - target[1]) < d and abs(player[0] - target[0]) < d:
        return True  # Checkpoint reached
    else:
        return False


def distance(actor_index: int):
    # Assume index is passed in.
    actor_coords = memory.main.get_actor_coords(actor_index=actor_index)
    player_coords = memory.main.get_actor_coords(actor_index=0)
    distance = sqrt(
        ((player_coords[0] - actor_coords[0]) ** 2)
        + ((player_coords[1] - actor_coords[1]) ** 2)
    )
    return int(distance)

def distance_coords(target_coords):
    # Assume x/y coords are passed as array.
    player_coords = memory.main.get_actor_coords(actor_index=0)
    distance = sqrt(
        ((player_coords[0] - target_coords[0]) ** 2)
        + ((player_coords[1] - target_coords[1]) ** 2)
    )
    return int(distance)


def approach_actor_by_index(actor_index: int, talk: bool = True):
    return _approach_actor(actor_index=actor_index, talk=talk)


def approach_actor_by_id(actor_id: int, talk: bool = True):
    index = memory.main.actor_index(actor_num=actor_id)
    return _approach_actor(actor_index=index, talk=talk)


def approach_party_member(target_char, talk: bool = True):
    index = target_char.actor_id
    return approach_actor_by_id(actor_id=index, talk=talk)


def _approach_actor(actor_index: int = 999, talk: bool = True):
    # This function can be called with either the actor ID or the actor index.
    # The actor ID is not the same as their usual character ID like 0-6 for the party,
    # but rather the ID used for the actor information in the game files.
    logger.debug(f"Actor index {actor_index}")

    actor_coords = memory.main.get_actor_coords(actor_index=actor_index)
    target_coords = [actor_coords[0], actor_coords[1]]
    logger.debug(f"Actor's coordinates: {target_coords}")

    while (
        memory.main.user_control() and
        not memory.main.name_aeon_ready()
    ):
        set_movement(target_coords)
        if talk and distance(actor_index) < 15:
            xbox.tap_b()
        actor_coords = memory.main.get_actor_coords(actor_index=actor_index)
        target_coords = [actor_coords[0], actor_coords[1]]
    return True


def approach_coords(target_coords, diag:int = 999, click_through:bool = True):
    if diag != 999:
        logger.debug(f"Moving until dialog value achieved: {diag}")
        while memory.main.diag_progress_flag() != diag:
            if memory.main.user_control():
                set_movement(target_coords)
                if distance_coords(target_coords) < 20:
                    xbox.tap_b()
            elif memory.main.diag_skip_possible():
                xbox.tap_b()
                
    else:
        while memory.main.user_control():
            set_movement(target_coords)
            if distance_coords(target_coords) < 20:
                xbox.tap_b()
    if click_through:
        FFXC.set_neutral()
        memory.main.click_to_control()

# TODO: Doesn't appear to be used, but left for historical purposes
def seymour_natus():  # First checkpoint ever written. :D
    x = 15
    y = 150
    return [x, y]


# TODO: This appears to be unused. Was for a showcase in 2021.
def t_plains_dodging(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 29
        y = 149
    if checkpoint == 1:
        x = 16
        y = -59
    if checkpoint == 2:
        x = 115
        y = -297
    if checkpoint == 3:
        x = 35
        y = -616
    if checkpoint == 4:
        x = -91
        y = -866
    if checkpoint == 5:
        x = -121
        y = -1089
    if checkpoint == 6:
        x = -120
        y = -1300
    return [x, y]
