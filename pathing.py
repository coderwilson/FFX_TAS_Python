import logging
from math import copysign

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

    if abs(player[1] - target[1]) < 3 and abs(player[0] - target[0]) < 3:
        return True  # Checkpoint reached
    else:
        return False


# TODO: Doesn't appear to be used, but left for historical purposes
def seymour_natus():  # First checkpoint ever written. :D
    x = 15
    y = 150
    return [x, y]


# TODO: This appears to be unused
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


def inside_sin(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 108
        y = -849
    if checkpoint == 1:
        x = 106
        y = -815
    if checkpoint == 2:
        x = 119
        y = -770
    if checkpoint == 3:
        x = 234
        y = -687
    if checkpoint == 4:
        x = 289
        y = -606
    if checkpoint == 5:
        x = 331
        y = -478
    if checkpoint == 6:
        x = 384
        y = -392
    if checkpoint == 7:
        x = 358
        y = -315
    if checkpoint == 8:
        x = 274
        y = -274
    if checkpoint == 9:
        x = 155
        y = -261
    if checkpoint == 10:
        x = 66
        y = -242
    if checkpoint == 11:
        x = 13
        y = -224
    if checkpoint == 12:
        x = -7
        y = -204
    if checkpoint == 13:
        x = -8
        y = -133
    if checkpoint == 14:
        x = 17
        y = -32
    if checkpoint == 15:
        x = 28
        y = 36
    if checkpoint == 16:
        x = -33
        y = 69
    if checkpoint == 17:
        x = -178
        y = 56
    if checkpoint == 18:
        x = -207
        y = 64
    if checkpoint == 19:
        x = -294
        y = 121
    if checkpoint == 20:
        x = -325
        y = 144
    if checkpoint == 21:
        x = -322
        y = 177
    if checkpoint == 22:
        x = -232
        y = 298
    if checkpoint == 23:
        x = -85
        y = 392
    if checkpoint == 24:
        x = 39
        y = 461
    if checkpoint == 25:
        x = 153
        y = 491
    if checkpoint == 26:
        x = 205
        y = 485
    if checkpoint == 27:
        x = 257
        y = 395
    if checkpoint == 28:
        x = 272
        y = 350
    if checkpoint == 29:
        x = 326
        y = 315
    if checkpoint == 30:
        x = 376
        y = 308
    if checkpoint == 31:
        x = 414
        y = 369
    if checkpoint == 32:
        x = 389
        y = 503
    if checkpoint == 33:
        x = 377
        y = 606
    if checkpoint == 34:
        x = 370
        y = 698
    if checkpoint == 35:
        x = 351
        y = 710
    if checkpoint == 36:
        x = 252
        y = 756
    if checkpoint == 37:
        x = 227
        y = 780
    if checkpoint == 38:
        x = 232
        y = 838
    if checkpoint == 39:
        x = 216
        y = 952
    if checkpoint == 40:
        x = 218
        y = 1100
    if checkpoint == 41:
        x = 414
        y = -638
    if checkpoint == 42:
        x = 432
        y = -566
    if checkpoint == 43:
        x = 438
        y = -488
    if checkpoint == 44:
        x = 398
        y = -412
    if checkpoint == 45:
        x = 215
        y = -276
    if checkpoint == 46:
        x = 134
        y = -249
    if checkpoint == 47:
        x = 82
        y = -222
    if checkpoint == 48:
        x = 40
        y = -205
    if checkpoint == 49:
        x = 30
        y = -186
    if checkpoint == 50:
        x = -1
        y = -138
    if checkpoint == 51:
        x = -4
        y = -105
    if checkpoint == 52:
        x = 3
        y = -48
    if checkpoint == 53:
        x = 14
        y = -3
    if checkpoint == 54:
        x = 12
        y = 57
    if checkpoint == 55:
        x = 18
        y = 119
    if checkpoint == 56:
        x = 31
        y = 163
    if checkpoint == 57:
        x = 55
        y = 168
    if checkpoint == 58:
        x = 262
        y = 187
    if checkpoint == 59:
        x = 313
        y = 255
    if checkpoint == 60:
        x = 346
        y = 322
    if checkpoint == 61:
        x = 330
        y = 343
    if checkpoint == 62:
        x = 315
        y = 387
    if checkpoint == 63:
        x = 322
        y = 432
    if checkpoint == 64:
        x = 342
        y = 477
    if checkpoint == 65:
        x = 401
        y = 513
    if checkpoint == 66:
        x = 466
        y = 496
    if checkpoint == 67:
        x = 550
        y = 485
    if checkpoint == 68:
        x = -33
        y = -525
    if checkpoint == 69:
        x = -2
        y = -480
    if checkpoint == 70:
        x = 0
        y = 10
    return [x, y]


def air_ship(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 17
        y = 47
    if checkpoint == 1:
        x = 25
        y = 32
    if checkpoint == 2:  # Room to room
        x = 0
        y = 0
    if checkpoint == 3:  # Screen with guardians
        x = -7
        y = 72
    if checkpoint == 4:
        x = -3
        y = 11
    if checkpoint == 5:
        x = 20
        y = -100
    if checkpoint == 6:  # Screen with Isaaru
        x = 33
        y = 53
    if checkpoint == 7:
        x = 22
        y = 22
    if checkpoint == 8:
        x = -10
        y = -10
    if checkpoint == 9:  # Gallery
        x = 0
        y = -40
    if checkpoint == 10:
        x = -10
        y = -79
    if checkpoint == 11:
        x = -19
        y = -86
    if checkpoint == 12:
        x = -33
        y = -86
    if checkpoint == 13:
        x = -33
        y = -57
    if checkpoint == 14:
        x = -35
        y = 7
    if checkpoint == 15:  # Split to specific pattern here if necessary
        x = -11
        y = 70
    if checkpoint == 16:  # Map change
        x = 999
        y = 999
    if checkpoint == 17:
        x = -4
        y = -8
    if checkpoint == 18:  # Up the lift
        x = 999
        y = 999
    if checkpoint == 19:  # Completion states
        x = 999
        y = 999
    if checkpoint == 23:
        x = -29
        y = -6
    if checkpoint == 25:
        x = -32
        y = -7
    if checkpoint == 26:
        x = -33
        y = -57
    if checkpoint == 27:
        x = -33
        y = -86
    if checkpoint == 28:
        x = -19
        y = -86
    if checkpoint == 29:
        x = -10
        y = -79
    if checkpoint == 30:
        x = 0
        y = -9
    if checkpoint == 31:  # Transition to next map
        x = 0
        y = 0
    if checkpoint == 32:
        x = 51
        y = 75
    if checkpoint == 33:
        x = 76
        y = 83
    if checkpoint == 34:  # Transition to next map
        x = 0
        y = 0
    if checkpoint == 35:
        x = 2
        y = 50
    if checkpoint == 36:
        x = 3
        y = 167
    if checkpoint == 37:  # Transition to next map
        x = 0
        y = 0
    if checkpoint == 38:
        x = 38
        y = 93
    if checkpoint == 39:
        x = 52
        y = 113
    if checkpoint == 40:  # Back into cockpit
        x = 0
        y = 0
    if checkpoint == 41:
        x = -241
        y = 195
    if checkpoint == 42:
        x = -242
        y = 316
    if checkpoint == 43:
        x = -245
        y = 327
    if checkpoint == 44:  # Cid
        x = 0
        y = 0
    if checkpoint == 45:  # non-CSR
        x = -245
        y = 327
    if checkpoint == 46:  # non-CSR Cid
        x = 0
        y = 0
    return [x, y]
