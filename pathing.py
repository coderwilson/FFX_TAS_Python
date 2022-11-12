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


def zanarkand_outdoors(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -16
        y = -671
    if checkpoint == 1:
        x = 1
        y = -507
    if checkpoint == 2:
        x = -17
        y = -435
    if checkpoint == 3:
        x = -98
        y = -442
    if checkpoint == 4:
        logger.info("Fortune sphere, no direction from this function.")
    if checkpoint == 5:
        x = -108
        y = -418
    if checkpoint == 6:
        x = -210
        y = -282
    if checkpoint == 7:
        x = -190
        y = -100
    if checkpoint == 8:  # Weird cutscene where we don't lose control immediately
        x = -94
        y = 81
    if checkpoint == 9:
        x = -121
        y = 301
    if checkpoint == 10:
        x = -187
        y = 424
    if checkpoint == 11:
        x = -365
        y = 565
    if checkpoint == 12:
        x = -523
        y = 656
    if checkpoint == 13:
        x = -564
        y = 801
    if checkpoint == 14:
        x = -628
        y = 936
    if checkpoint == 15:
        x = -750
        y = 1083
    return [x, y]


def zanarkand_dome(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 2
        y = -325
    if checkpoint == 1:
        x = 117
        y = -203
    if checkpoint == 2:
        x = 128
        y = -162
    if checkpoint == 3:
        x = 134
        y = -85
    if checkpoint == 4:
        x = 71
        y = -20
    if checkpoint == 5:
        x = -20
        y = 5
    if checkpoint == 6:
        x = -136
        y = -32
    if checkpoint == 7:
        x = -186
        y = -109
    if checkpoint == 8:  # Near save sphere
        x = -144
        y = -124
    if checkpoint == 9:
        x = -132
        y = -105
    if checkpoint == 10:  # Seymour scene
        x = -126
        y = 49
    if checkpoint == 11:
        x = -101
        y = 76
    if checkpoint == 12:
        x = 3
        y = 89
    if checkpoint == 13:
        logger.info("Friend sphere, no direction from this function.")
    if checkpoint == 14:
        x = -127
        y = 68
    if checkpoint == 15:
        x = -230
        y = 146
    if checkpoint == 16:
        x = -154
        y = 195
    if checkpoint == 17:  # Mini-bridge, running with Braska/Jecht
        x = -73
        y = 232
    if checkpoint == 18:
        x = -27
        y = 286
    if checkpoint == 19:
        x = 7
        y = 386
    if checkpoint == 20:
        x = -5
        y = 600
    if checkpoint == 21:
        x = -12
        y = -188
    if checkpoint == 22:
        x = 3
        y = -96
    if checkpoint == 23:
        x = 23
        y = -80
    if checkpoint == 24:
        logger.info("Luck sphere, no direction from this function.")
    if checkpoint == 25:
        x = -15
        y = -49
    if checkpoint == 26:
        x = 1
        y = 36
    if checkpoint == 27:
        x = 5
        y = 240
    if checkpoint == 28:
        x = -21
        y = 352
    if checkpoint == 29:
        logger.info("Touching save sphere, no direction from this function.")
    if checkpoint == 30:
        x = -3
        y = 360
    if checkpoint == 31:
        x = 1
        y = 500
    return [x, y]


def zanarkand_trials(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 105
        y = -57
    if checkpoint == 1:
        x = 105
        y = -44
    if checkpoint == 2:
        x = 135
        y = -35
    if checkpoint == 3:
        x = 126
        y = -14
    if checkpoint == 4:
        x = 133
        y = 5
    if checkpoint == 5:
        x = 110
        y = 18
    if checkpoint == 6:
        x = 84
        y = 25
    if checkpoint == 7:
        x = 71
        y = 25
    if checkpoint == 8:
        logger.info("First pedetsol, no direction from here.")
    if checkpoint == 9:  # First pattern in big room
        x = -1
        y = 11
    if checkpoint == 10:
        x = -4
        y = -6
    if checkpoint == 11:
        x = -25
        y = -26
    if checkpoint == 12:
        x = -53
        y = 18
    if checkpoint == 13:
        x = -79
        y = 24
    if checkpoint == 14:
        x = -106
        y = 19
    if checkpoint == 15:
        x = -125
        y = 4
    if checkpoint == 16:
        x = -157
        y = 45
    if checkpoint == 17:
        x = -103
        y = 66
    if checkpoint == 18:
        x = -93
        y = 86
    if checkpoint == 19:
        x = -90
        y = 123
    if checkpoint == 20:
        logger.info("Picking up Kilika sphere")
    if checkpoint == 21:
        x = -53
        y = 63
    if checkpoint == 22:
        x = 11
        y = 70
    if checkpoint == 23:
        x = 28
        y = 72
    if checkpoint == 24:
        x = 83
        y = 34
    if checkpoint == 25:
        x = 71
        y = 4
    if checkpoint == 26:
        logger.info("Placing Kilika sphere")
    if checkpoint == 27:
        x = 72
        y = -12
    if checkpoint == 28:
        logger.info("Activating second pedestal")
    if checkpoint == 29:
        x = 77
        y = 43
    if checkpoint == 30:
        logger.info("Moving into next room.")
    if checkpoint == 31:  # Second pattern in big room
        x = -5
        y = 74
    if checkpoint == 32:
        x = -17
        y = 44
    if checkpoint == 33:
        x = -28
        y = 42
    if checkpoint == 34:
        x = -88
        y = 31
    if checkpoint == 35:
        x = -106
        y = 33
    if checkpoint == 36:
        x = -114
        y = -1
    if checkpoint == 37:
        x = -128
        y = -29
    if checkpoint == 38:
        x = -156
        y = -55
    if checkpoint == 39:
        x = -104
        y = -64
    if checkpoint == 40:
        x = -84
        y = -75
    if checkpoint == 41:
        x = -13
        y = -42
    if checkpoint == 42:
        x = 1
        y = 57
    if checkpoint == 43:
        x = 28
        y = 74
    if checkpoint == 44:
        x = 83
        y = 34
    if checkpoint == 45:
        x = 137
        y = 23
    if checkpoint == 46:
        logger.info("Activating second pedestal")
    if checkpoint == 47:
        x = 84
        y = 45
    if checkpoint == 48:
        logger.info("Moving into next room.")
    if checkpoint == 49:  # Third pattern in main room, start.
        x = -5
        y = 74
    if checkpoint == 50:
        x = -17
        y = 45
    if checkpoint == 51:
        x = -27
        y = 44
    if checkpoint == 52:
        x = -57
        y = 67
    if checkpoint == 53:
        x = -94
        y = 85
    if checkpoint == 54:
        x = -106
        y = 60
    if checkpoint == 55:
        x = -116
        y = 40
    if checkpoint == 56:
        x = -124
        y = 3
    if checkpoint == 57:
        x = -115
        y = -31
    if checkpoint == 58:
        x = -104
        y = -65
    if checkpoint == 59:
        x = -79
        y = -57
    if checkpoint == 60:
        x = -23
        y = -75
    if checkpoint == 61:
        x = -15
        y = -43
    if checkpoint == 62:
        x = 3
        y = 65
    if checkpoint == 63:
        x = 32
        y = 73
    if checkpoint == 64:
        x = 83
        y = 34
    if checkpoint == 65:
        x = 137
        y = -22
    if checkpoint == 66:
        logger.info("Activating second pedestal")
    if checkpoint == 67:
        x = 84
        y = 45
    if checkpoint == 68:
        logger.info("Moving into next room.")
    if checkpoint == 69:  # Last pattern in main room.
        x = -6
        y = 75
    if checkpoint == 70:
        x = 0
        y = 6
    if checkpoint == 71:
        x = -14
        y = -46
    if checkpoint == 72:
        x = -24
        y = -75
    if checkpoint == 73:
        x = -86
        y = -75
    if checkpoint == 74:
        x = -104
        y = -67
    if checkpoint == 75:
        x = -124
        y = -5
    if checkpoint == 76:
        x = -136
        y = -1
    if checkpoint == 77:
        x = -155
        y = 46
    if checkpoint == 78:
        x = -104
        y = 78
    if checkpoint == 79:
        x = -92
        y = 88
    if checkpoint == 80:
        x = -68
        y = 110
    if checkpoint == 81:  # Pick up Besaid sphere
        logger.info("Picking up Besaid sphere")
    if checkpoint == 82:
        x = -67
        y = 94
    if checkpoint == 83:
        x = 5
        y = 71
    if checkpoint == 84:
        x = 33
        y = 72
    if checkpoint == 85:
        x = 83
        y = 34
    if checkpoint == 86:
        x = 136
        y = -1
    if checkpoint == 87:
        logger.info("Placing Besaid sphere")
    if checkpoint == 88:
        x = 110
        y = 20
    return [x, y]


def yunalesca(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 3
        y = 8
    if checkpoint == 1:
        x = 5
        y = 35
    if checkpoint == 2:
        x = 0
        y = 0
    if checkpoint == 3:
        x = 0
        y = 80
    if checkpoint == 4:
        x = 0
        y = 0
    if checkpoint == 5:
        x = 0
        y = 0
    if checkpoint == 6:
        x = 0
        y = 0
    if checkpoint == 7:
        x = 0
        y = 0
    if checkpoint == 8:
        x = 0
        y = 0
    if checkpoint == 9:
        x = 0
        y = 0
    if checkpoint == 10:
        x = 0
        y = 0
    return [x, y]


def yunalesca_to_airship(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -4
        y = -179
    if checkpoint == 1:
        x = -4
        y = -300
    if checkpoint == 2:
        x = 0
        y = 55
    if checkpoint == 3:
        x = 0
        y = -200
    if checkpoint == 4:
        x = 0
        y = -72
    if checkpoint == 5:
        x = -2
        y = -132
    if checkpoint == 6:
        x = 0
        y = -160
    if checkpoint == 7:
        logger.info("Touch save sphere")
        x = 0
        y = -160
    if checkpoint == 8:
        x = 0
        y = -200
    if checkpoint == 9:
        x = 0
        y = -500
    if checkpoint == 10:
        x = -65
        y = -56
    if checkpoint == 11:
        x = -46
        y = -35
    if checkpoint == 12:
        x = 3
        y = 62
    if checkpoint == 13:
        x = 28
        y = 68
    if checkpoint == 14:
        x = 83
        y = 34
    if checkpoint == 15:
        x = 99
        y = -67
    if checkpoint == 16:
        x = 100
        y = -93
    if checkpoint == 17:
        x = 100
        y = -200
    if checkpoint == 18:
        x = -1
        y = 243
    if checkpoint == 19:
        x = -3
        y = 148
    if checkpoint == 20:
        x = -5
        y = 39
    if checkpoint == 21:
        x = -12
        y = -53
    if checkpoint == 22:
        x = -6
        y = -89
    if checkpoint == 23:
        x = -10
        y = -200
    if checkpoint == 24:
        x = -10
        y = -400
    if checkpoint == 25:
        x = 125
        y = 1423
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
