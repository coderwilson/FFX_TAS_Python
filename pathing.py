import logging
from math import copysign

import memory.main
import xbox

logger = logging.getLogger(__name__)
FFXC = xbox.controller_handle()


class AreaMovementBase:
    checkpoint_fallback = {}

    @classmethod
    def execute(cls, checkpoint):
        # If we have a message here, something has probably gone wrong
        if message := cls.checkpoint_fallback.get(checkpoint):
            logger.warning(message)
        return cls.checkpoint_coordiantes.get(checkpoint, [999, 999])


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


def calm_lands(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -332
        y = -1612
    if checkpoint == 1:
        x = -437
        y = -1603
    if checkpoint == 2:
        x = -640
        y = -1591
    if checkpoint == 3:
        x = -757
        y = -1530
    if checkpoint == 4:
        x = -777
        y = -1478
    if checkpoint == 5:  # Southeast of agency, northeast of the turn.
        x = -186
        y = -715
    if checkpoint == 6:
        x = 461
        y = -35
    if checkpoint == 7:
        x = 708
        y = 215
    if checkpoint == 8:
        x = 766
        y = 276
    if checkpoint == 9:
        x = 821
        y = 290
    if checkpoint == 10:
        x = 1366
        y = 609
    if checkpoint == 11:
        x = 1422
        y = 663
    if checkpoint == 12:
        x = 1440
        y = 724
    if checkpoint == 13:
        x = 1466
        y = 841
    if checkpoint == 14:
        x = 1549
        y = 1059
    if checkpoint == 15:
        x = 1630
        y = 1230
    return [x, y]


def defender_x(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 62
        y = -66
    if checkpoint == 1:
        x = 69
        y = -229
    if checkpoint == 2:
        x = -14
        y = 104
    if checkpoint == 3:
        x = -9
        y = 240
    if checkpoint == 4:
        x = 12
        y = 350
    return [x, y]


def ne_approach(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 121
        y = 120
    if checkpoint == 1:
        x = 122
        y = 134
    if checkpoint == 2:
        x = 113
        y = 150
    if checkpoint == 3:
        x = -35
        y = 167
    if checkpoint == 4:
        x = -200
        y = 170
    if checkpoint == 5:
        x = -228
        y = 228
    if checkpoint == 6:
        x = -278
        y = 172
    if checkpoint == 7:
        x = -328
        y = 150
    if checkpoint == 8:
        x = -385
        y = 168
    if checkpoint == 9:
        x = -250
        y = 10
    return [x, y]


def ne_force_encounters_white(checkpoint):
    x = 0
    y = 999
    if checkpoint % 2 == 0:
        y = 70
    if checkpoint % 2 == 1:
        y = 20
    return [x, y]


def ne_force_encounters_green(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 0
        y = 70
    if checkpoint == 1:
        x = 0
        y = 170
    if checkpoint == 2:
        x = 0
        y = 170
    if checkpoint == 3:
        x = 0
        y = 170
    if checkpoint == 4:
        x = 13
        y = 186
    if checkpoint == 5:
        x = 67
        y = 251
    if checkpoint == 6:
        x = 95
        y = 271
    if checkpoint == 7:
        x = 153
        y = 287
    if checkpoint == 8:
        x = 298
        y = 283
    if checkpoint == 9:
        x = 353
        y = 307
    if checkpoint == 10:
        x = 389
        y = 335
    if checkpoint == 11:
        x = 416
        y = 382
    if checkpoint == 12:
        x = 430
        y = 438
    if checkpoint == 13:  # Light area 1
        x = 431
        y = 484
    if checkpoint == 14:  # Light area 2
        x = 458
        y = 505
    return [x, y]


def ne_return_green(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 428
        y = 452
    if checkpoint == 1:
        x = 421
        y = 405
    if checkpoint == 2:
        x = 411
        y = 370
    if checkpoint == 3:
        x = 384
        y = 327
    if checkpoint == 4:
        x = 341
        y = 300
    if checkpoint == 5:
        x = 297
        y = 285
    if checkpoint == 6:
        x = 208
        y = 281
    if checkpoint == 7:
        x = 114
        y = 278
    if checkpoint == 8:
        x = 73
        y = 261
    if checkpoint == 9:
        x = 6
        y = 177
    if checkpoint == 10:
        x = 0
        y = 0
    return [x, y]


def ne_return(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 0
        y = -100
    if checkpoint == 1:
        x = -305
        y = 168
    if checkpoint == 3:
        x = -282
        y = 189
    if checkpoint == 4:
        x = -231
        y = 230
    if checkpoint == 5:
        x = -223
        y = 243
    if checkpoint == 6:
        x = -220
        y = 350
    if checkpoint == 7:
        x = -2
        y = 163
    if checkpoint == 8:
        x = 91
        y = 150
    if checkpoint == 9:
        x = 120
        y = 144
    if checkpoint == 10:
        x = 126
        y = 134
    if checkpoint == 11:
        x = 119
        y = 122
    if checkpoint == 12:
        x = 109
        y = 111
    if checkpoint == 13:
        x = 64
        y = 95
    if checkpoint == 14:
        x = 8
        y = 105
    if checkpoint == 15:
        x = -4
        y = 106
    if checkpoint == 16:
        x = -12
        y = 116
    if checkpoint == 17:
        x = -11
        y = 174
    if checkpoint == 18:
        x = -9
        y = 214
    if checkpoint == 19:
        x = -6
        y = 254
    if checkpoint == 20:
        x = 4
        y = 290
    if checkpoint == 21:  # Through the trigger to Gagazet gates
        x = 17
        y = 550
    if checkpoint == 22:  # Safety
        x = 100
        y = 800
    return [x, y]


def kelk_ronso(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -122
        y = -552
    if checkpoint == 1:
        x = -10
        y = -444
    if checkpoint == 2:
        x = 23
        y = -369
    if checkpoint == 3:
        x = 21
        y = -192
    if checkpoint == 4:
        x = 17
        y = 146
    if checkpoint == 5:
        x = 50
        y = 290
    if checkpoint == 6:
        x = 80
        y = 550
    return [x, y]


def gagazet_nea_loop_back(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 33
        y = 197
    if checkpoint == 1:
        x = 22
        y = -64
    if checkpoint == 2:
        x = 18
        y = -198
    if checkpoint == 3:
        x = 24
        y = -300
    if checkpoint == 4:
        x = 11
        y = -354
    if checkpoint == 5:
        x = 5
        y = -396
    if checkpoint == 6:
        x = -7
        y = -445
    if checkpoint == 7:
        x = -33
        y = -473
    if checkpoint == 8:
        x = -78
        y = -521
    if checkpoint == 9:
        x = -111
        y = -536
    if checkpoint == 10:
        x = -140
        y = -591
    if checkpoint == 11:
        x = -168
        y = -645
    if checkpoint == 12:  # Transition to previous map
        x = -190
        y = -800
    if checkpoint == 13:
        x = 21
        y = 366
    if checkpoint == 14:
        x = -8
        y = 238
    if checkpoint == 15:
        x = -9
        y = 190
    if checkpoint == 16:
        x = -10
        y = 108
    if checkpoint == 17:
        x = 7
        y = 94
    return [x, y]


def gagazet_snow(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 18
        y = 45
    if checkpoint == 1:
        x = 57
        y = 328
    if checkpoint == 2:
        x = 40
        y = 375
    if checkpoint == 3:
        x = -1
        y = 421
    if checkpoint == 4:
        x = -49
        y = 444
    if checkpoint == 5:
        x = -237
        y = 311
    if checkpoint == 6:
        x = -273
        y = 315
    if checkpoint == 7:
        x = -327
        y = 383
    if checkpoint == 8:
        x = -369
        y = 465
    if checkpoint == 9:
        x = -409
        y = 460
    if checkpoint == 10:
        x = -538
        y = 264
    if checkpoint == 11:
        x = -619
        y = 210
    if checkpoint == 12:
        x = -913
        y = 163
    if checkpoint == 13:
        x = -941
        y = 191
    if checkpoint == 14:
        x = -903
        y = 330
    if checkpoint == 15:
        x = -878
        y = 433
    if checkpoint == 16:
        x = -830
        y = 540
    if checkpoint == 17:
        x = -728
        y = 565
    if checkpoint == 18:
        x = -664
        y = 537
    if checkpoint == 19:
        x = -633
        y = 497
    if checkpoint == 20:
        x = -599
        y = 370
    if checkpoint == 21:
        x = -592
        y = 262
    if checkpoint == 22:
        x = -600
        y = 223
    if checkpoint == 23:
        x = -790
        y = 207
    if checkpoint == 24:
        x = -877
        y = 232
    if checkpoint == 25:
        x = -1034
        y = 491
    if checkpoint == 26:
        x = -1065
        y = 502
    if checkpoint == 27:
        x = -1133
        y = 446
    if checkpoint == 28:
        x = -1248
        y = 166
    if checkpoint == 29:
        x = -1307
        y = -1
    if checkpoint == 30:
        x = -1365
        y = -85
    return [x, y]


def flux(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -368
        y = -330
    if checkpoint == 1:
        x = -303
        y = -259
    if checkpoint == 2:
        x = 31
        y = -202
    if checkpoint == 3:
        x = 146
        y = -285
    if checkpoint == 4:
        x = 173
        y = -343
    if checkpoint == 5:
        x = 167
        y = -550
    if checkpoint == 6:
        x = 150
        y = -619
    return [x, y]


def gagazet_dream_seq(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -62
        y = 180
    if checkpoint == 1:
        x = -29
        y = 134
    if checkpoint == 2:
        x = -20
        y = 113
    if checkpoint == 3:
        x = 15
        y = 21
    if checkpoint == 4:
        x = 23
        y = 9
    if checkpoint == 5:
        x = 58
        y = 3
    if checkpoint == 6:
        x = 123
        y = 1
    if checkpoint == 7:
        x = 149
        y = 0
    if checkpoint == 8:
        x = 173
        y = 1
    if checkpoint == 9:
        x = 205
        y = 3
    if checkpoint == 10:
        x = 239
        y = 18
    if checkpoint == 11:  # Into the door
        x = 0
        y = 0
    if checkpoint == 12:
        x = 62
        y = -35
    if checkpoint == 13:
        x = 63
        y = -14
    if checkpoint == 14:
        x = 52
        y = -12
    if checkpoint == 15:  # Start first conversation
        x = 0
        y = 0
    if checkpoint == 16:
        x = 64
        y = -12
    if checkpoint == 17:
        x = 64
        y = -25
    if checkpoint == 18:
        x = 64
        y = -46
    if checkpoint == 19:  # Back to outdoor area
        x = 0
        y = 0
    if checkpoint == 20:
        x = 235
        y = 8
    if checkpoint == 21:
        x = 234
        y = -18
    if checkpoint == 22:
        x = 238
        y = -26
    if checkpoint == 23:
        x = 269
        y = -30
    if checkpoint == 24:
        x = 288
        y = -25
    if checkpoint == 25:
        x = 326
        y = -1
    return [x, y]


def gagazet_post_dream(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 1143
        y = 73
    if checkpoint == 1:
        x = 1054
        y = 289
    if checkpoint == 2:
        x = 1016
        y = 383
    if checkpoint == 3:
        x = 1023
        y = 404
    if checkpoint == 4:
        x = 1019
        y = 494
    if checkpoint == 5:
        x = 990
        y = 529
    if checkpoint == 6:
        x = 991
        y = 585
    if checkpoint == 7:
        x = 1020
        y = 620
    if checkpoint == 8:
        x = 1046
        y = 643
    if checkpoint == 9:
        x = 1200
        y = 643
    return [x, y]


def gagazet_cave(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -45
        y = -1252
    if checkpoint == 1:
        x = -27
        y = -1142
    if checkpoint == 2:
        x = 79
        y = -969
    if checkpoint == 3:
        x = 90
        y = -949
    if checkpoint == 4:
        x = 47
        y = -812
    if checkpoint == 5:
        x = 25
        y = -552
    if checkpoint == 6:
        x = 161
        y = -376
    if checkpoint == 7:
        logger.info("Map change, no target from this function.")
    if checkpoint == 8:
        x = -45
        y = -393
    if checkpoint == 9:
        x = 9
        y = -257
    if checkpoint == 10:
        x = 106
        y = 9
    if checkpoint == 11:
        x = 192
        y = 153
    if checkpoint == 13:
        x = 100
        y = -3
    if checkpoint == 14:
        x = 7
        y = -266
    if checkpoint == 15:
        x = -49
        y = -420
    if checkpoint == 16:
        x = -52
        y = -477
    if checkpoint == 17:
        logger.info("Map change, no target from this function.")
    if checkpoint == 18:
        x = 36
        y = -535
    if checkpoint == 19:
        x = 35
        y = -767
    if checkpoint == 20:
        x = 56
        y = -832
    if checkpoint == 21:
        x = 143
        y = -929
    if checkpoint == 22:
        x = 232
        y = -853
    if checkpoint == 23:
        x = 241
        y = -788
    if checkpoint == 24:
        x = 192
        y = -669
    if checkpoint == 25:
        x = 180
        y = -625
    if checkpoint == 26:
        x = 208
        y = -418
    if checkpoint == 27:
        x = 248
        y = -270
    if checkpoint == 28:
        x = 240
        y = -63
    if checkpoint == 29:
        logger.info("Map change, no target from this function.")
    if checkpoint == 30:
        x = 183
        y = 66
    if checkpoint == 31:
        x = 201
        y = 208
    if checkpoint == 32:
        x = 208
        y = 260
    if checkpoint == 33:
        x = 181
        y = 292
    if checkpoint == 34:
        x = 140
        y = 301
    if checkpoint == 35:
        logger.info("Second trial, no target from this function.")
    if checkpoint == 36:
        x = 168
        y = 295
    if checkpoint == 37:
        x = 189
        y = 283
    if checkpoint == 38:
        x = 208
        y = 256
    if checkpoint == 39:
        x = 199
        y = 175
    if checkpoint == 40:
        x = 179
        y = 67
    if checkpoint == 41:
        x = 204
        y = -10
    if checkpoint == 42:
        logger.info("Map change, no target from this function.")
    if checkpoint == 43:
        x = 229
        y = -274
    if checkpoint == 44:
        x = 215
        y = -375
    if checkpoint == 45:
        x = 197
        y = -435
    if checkpoint == 46:  # Turn to go up the new stairs
        x = 184
        y = -445
    if checkpoint == 47:
        x = 177
        y = -433
    if checkpoint == 48:
        x = 172
        y = -356
    if checkpoint == 49:
        x = 161
        y = -335
    if checkpoint == 50:
        x = 156
        y = -288
    if checkpoint == 51:
        x = 168
        y = -252
    if checkpoint == 52:
        x = 159
        y = -236
    if checkpoint == 53:
        x = 183
        y = -196
    if checkpoint == 54:
        x = 181
        y = -107
    if checkpoint == 55:
        x = 162
        y = -26
    if checkpoint == 56:
        x = 142
        y = 14
    if checkpoint == 57:
        x = 7
        y = 99
    if checkpoint == 58:
        x = -208
        y = 240
    if checkpoint == 60:
        x = -260
        y = 200
    return [x, y]


def gagazet_peak(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 943
        y = -1055
    if checkpoint == 1:
        x = 860
        y = -994
    if checkpoint == 2:
        x = 787
        y = -839
    if checkpoint == 3:
        logger.info("Mi'ihen agency scene, no target from this function.")
    if checkpoint == 4:
        x = 779
        y = -695
    if checkpoint == 5:
        x = 844
        y = -551
    if checkpoint == 6:
        logger.info("Map change, no target from this function.")
    if checkpoint == 7:
        x = -135
        y = -669
    if checkpoint == 8:
        x = 129
        y = -534
    if checkpoint == 9:
        x = 139
        y = -448
    if checkpoint == 10:
        x = 107
        y = -386
    if checkpoint == 11:
        x = 47
        y = -310
    if checkpoint == 12:
        x = -151
        y = -181
    if checkpoint == 13:
        x = -204
        y = -119
    if checkpoint == 14:
        x = -295
        y = 123
    if checkpoint == 15:
        x = -303
        y = 382
    if checkpoint == 16:
        x = -320
        y = 450
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
