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
    # memory.wait_frames(frames=1)

    if abs(player[1] - target[1]) < 3 and abs(player[0] - target[0]) < 9:
        return True  # Checkpoint reached
    else:
        return False


def to_remiem(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -1442
        y = 123
    if checkpoint == 1:
        x = -1429
        y = -218
    if checkpoint == 2:
        x = -927
        y = -1415
    if checkpoint == 3:
        x = -820
        y = -1547
    if checkpoint == 4:
        x = -576
        y = -1654
    if checkpoint == 5:
        x = -244
        y = -1619
    if checkpoint == 6:
        x = 212
        y = -1611
    if checkpoint == 7:
        x = 544
        y = -1601
    if checkpoint == 8:
        x = 831
        y = -1503
    if checkpoint == 9:
        x = 1006
        y = -1445
    if checkpoint == 10:  # Chocobo feather
        x = 0
        y = 0
    if checkpoint == 11:
        x = 1420
        y = -1268
    if checkpoint == 12:
        x = 1800
        y = -1270
    if checkpoint == 13:  # First movement in temple map
        x = -604
        y = 359
    if checkpoint == 14:
        x = -530
        y = 353
    if checkpoint == 15:
        x = -325
        y = 355
    if checkpoint == 16:
        x = -257
        y = 355
    if checkpoint == 17:  # Far side of bridge
        x = 396
        y = 357
    if checkpoint == 18:  # Far side of bridge
        x = 396
        y = 357
    if checkpoint == 19:  # Far side of bridge
        x = 396
        y = 357
    if checkpoint == 20:  # Far side of bridge
        x = 396
        y = 357
    if checkpoint == 21:  # Far side of bridge
        x = 396
        y = 357
    if checkpoint == 22:  # Far side of bridge
        x = 396
        y = 357
    if checkpoint == 23:
        x = 478
        y = 380
    if checkpoint == 24:
        x = 496
        y = 438
    if checkpoint == 25:
        x = 594
        y = 570
    if checkpoint == 26:
        x = 757
        y = 630
    if checkpoint == 27:  # Orb to initiate race
        x = 0
        y = 0
    if checkpoint == 28:
        x = 757
        y = 630
    if checkpoint == 29:
        x = 594
        y = 570
    if checkpoint == 30:
        x = 496
        y = 438
    if checkpoint == 31:  # Past save sphere
        x = 492
        y = 339
    if checkpoint == 32:
        x = 497
        y = 274
    if checkpoint == 33:
        x = 599
        y = 141
    if checkpoint == 34:
        x = 763
        y = 71
    if checkpoint == 35:  # Start race
        x = 0
        y = 0
    return [x, y]


def race_1(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 809
        y = 20
    if checkpoint == 1:
        x = 830
        y = -3
    if checkpoint == 2:
        x = 890
        y = -27
    if checkpoint == 3:
        x = 1013
        y = -48
    if checkpoint == 4:
        x = 1117
        y = -14
    if checkpoint == 5:
        x = 1182
        y = 34
    if checkpoint == 6:
        x = 1249
        y = 193
    if checkpoint == 7:
        x = 1284
        y = 322
    if checkpoint == 8:  # Left of first pole
        x = 1227
        y = 451
    if checkpoint == 9:
        x = 1180
        y = 489
    if checkpoint == 10:
        x = 1093
        y = 615
    if checkpoint == 11:
        x = 958
        y = 724
    if checkpoint == 12:  # Left of green pole
        x = 884
        y = 749
    if checkpoint == 13:
        x = 779
        y = 774
    if checkpoint == 14:  # Around second green pole
        x = 673
        y = 776
    if checkpoint == 15:
        x = 644
        y = 751
    if checkpoint == 16:
        x = 673
        y = 733
    if checkpoint == 17:  # End, around second green.
        x = 702
        y = 723
    if checkpoint == 18:  # Around first yellow pole
        x = 771
        y = 717
    if checkpoint == 19:
        x = 797
        y = 691
    if checkpoint == 20:
        x = 759
        y = 666
    if checkpoint == 21:  # End, around first yellow
        x = 709
        y = 676
    if checkpoint == 22:
        x = 581
        y = 615
    if checkpoint == 23:  # Past second/last yellow, last pole
        x = 555
        y = 547
    if checkpoint == 24:
        x = 535
        y = 504
    if checkpoint == 25:
        x = 537
        y = 291
    if checkpoint == 26:  # Past first red pole
        x = 613
        y = 205
    if checkpoint == 27:
        x = 733
        y = 136
    if checkpoint == 28:
        x = 890
        y = 177
    if checkpoint == 29:
        x = 913
        y = 206
    if checkpoint == 30:  # Past second red pole
        x = 928
        y = 239
    if checkpoint == 31:
        x = 980
        y = 351
    if checkpoint == 32:
        x = 928
        y = 503
    if checkpoint == 33:
        x = 762
        y = 532
    if checkpoint == 34:  # Past third red pole
        x = 762
        y = 532
    if checkpoint == 35:
        x = 662
        y = 437
    if checkpoint == 36:  # Fin
        x = 699
        y = 338
    return [x, y]


def race_2(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 809
        y = 20
    if checkpoint == 1:
        x = 830
        y = -3
    if checkpoint == 2:
        x = 890
        y = -27
    if checkpoint == 3:
        x = 1013
        y = -48
    if checkpoint == 4:
        x = 1117
        y = -14
    if checkpoint == 5:
        x = 1182
        y = 34
    if checkpoint == 6:
        x = 1249
        y = 193
    if checkpoint == 7:
        x = 1284
        y = 322
    if checkpoint == 8:  # Right of first pole
        x = 1272
        y = 474
    if checkpoint == 9:
        x = 1228
        y = 595
    if checkpoint == 10:
        x = 1131
        y = 731
    if checkpoint == 11:  # First chest
        x = 0
        y = 0
    if checkpoint == 12:  # Right of green thing
        x = 955
        y = 736
    if checkpoint == 13:  # Up ramp, avoiding pole
        x = 811
        y = 826
    if checkpoint == 14:
        x = 800
        y = 856
    if checkpoint == 15:  # Around blue pole, back towards chest
        x = 830
        y = 881
    if checkpoint == 16:
        x = 964
        y = 824
    if checkpoint == 17:  # Second chest
        x = 0
        y = 0
    if checkpoint == 18:  # Right of green thing
        x = 955
        y = 736
    if checkpoint == 19:  # Up ramp, avoiding pole
        x = 811
        y = 826
    if checkpoint == 20:  # Towards third chest
        x = 735
        y = 882
    if checkpoint == 21:
        x = 604
        y = 860
    if checkpoint == 22:  # Third chest
        x = 0
        y = 0
    if checkpoint == 23:
        x = 569
        y = 580
    if checkpoint == 24:
        x = 549
        y = 538
    if checkpoint == 25:
        x = 529
        y = 463
    if checkpoint == 26:
        x = 569
        y = 230
    if checkpoint == 27:  # Left of first red pillar
        x = 619
        y = 200
    if checkpoint == 28:
        x = 890
        y = 177
    if checkpoint == 29:
        x = 890
        y = 177
    if checkpoint == 30:
        x = 913
        y = 206
    if checkpoint == 31:  # Past second red pole
        x = 928
        y = 239
    if checkpoint == 32:
        x = 980
        y = 351
    if checkpoint == 33:
        x = 928
        y = 503
    if checkpoint == 34:
        x = 762
        y = 532
    if checkpoint == 35:  # Past third red pole
        x = 762
        y = 532
    if checkpoint == 36:
        x = 662
        y = 437
    if checkpoint == 37:  # Fin
        x = 699
        y = 338
    return [x, y]


def race_3(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 809
        y = 20
    if checkpoint == 1:
        x = 830
        y = -3
    if checkpoint == 2:
        x = 890
        y = -27
    if checkpoint == 3:
        x = 1013
        y = -48
    if checkpoint == 4:
        x = 1117
        y = -14
    if checkpoint == 5:
        x = 1182
        y = 34
    if checkpoint == 6:
        x = 1249
        y = 193
    if checkpoint == 7:
        x = 1284
        y = 322
    if checkpoint == 8:  # Right of first pole
        x = 1272
        y = 474
    if checkpoint == 9:
        x = 1228
        y = 595
    if checkpoint == 10:
        x = 1131
        y = 731
    if checkpoint == 11:  # First chest
        x = 0
        y = 0
    if checkpoint == 12:  # Right of green thing
        x = 955
        y = 736
    if checkpoint == 13:  # Up ramp, avoiding pole
        x = 811
        y = 826
    if checkpoint == 14:
        x = 800
        y = 856
    if checkpoint == 15:  # Around blue pole, back towards chest
        x = 830
        y = 881
    if checkpoint == 16:
        x = 964
        y = 824
    if checkpoint == 17:  # Second chest
        x = 0
        y = 0
    if checkpoint == 18:  # Right of green thing
        x = 955
        y = 736
    if checkpoint == 19:  # Up ramp, avoiding pole
        x = 811
        y = 826
    if checkpoint == 20:  # Towards third chest
        x = 735
        y = 882
    if checkpoint == 21:
        x = 604
        y = 860
    if checkpoint == 22:  # Third chest
        x = 0
        y = 0
    if checkpoint == 23:
        x = 431
        y = 394
    if checkpoint == 24:
        x = 431
        y = 394
    if checkpoint == 25:
        x = 462
        y = 208
    if checkpoint == 26:
        x = 527
        y = 121
    if checkpoint == 27:  # Fourth chest
        x = 0
        y = 0
    if checkpoint == 28:
        x = 833
        y = 48
    if checkpoint == 29:  # Left of yellow
        x = 914
        y = 89
    if checkpoint == 30:
        x = 961
        y = 121
    if checkpoint == 31:  # Between yellows
        x = 1060
        y = 249
    if checkpoint == 32:  # Left of yellow
        x = 1074
        y = 316
    if checkpoint == 33:
        x = 1098
        y = 339
    if checkpoint == 34:  # Around yellow
        x = 1115
        y = 308
    if checkpoint == 35:  # Next to green
        x = 1112
        y = 231
    if checkpoint == 36:
        x = 1133
        y = 206
    if checkpoint == 37:  # Right of green
        x = 1157
        y = 228
    if checkpoint == 38:
        x = 1173
        y = 360
    if checkpoint == 39:  # Last chest
        x = 0
        y = 0
    if checkpoint == 40:
        x = 787
        y = 541
    if checkpoint == 41:  # Past third red pole
        x = 762
        y = 532
    if checkpoint == 42:
        x = 662
        y = 437
    if checkpoint == 43:  # Fin
        x = 699
        y = 338
    return [x, y]


def leave_remiem(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 754
        y = 87
    if checkpoint == 1:
        x = 663
        y = 113
    if checkpoint == 2:
        x = 593
        y = 139
    if checkpoint == 3:
        x = 537
        y = 206
    if checkpoint == 4:
        x = 494
        y = 277
    if checkpoint == 5:
        x = 477
        y = 335
    if checkpoint == 6:
        x = 398
        y = 357
    if checkpoint == 7:
        x = 356
        y = 357
    if checkpoint == 8:
        x = 356
        y = 357
    if checkpoint == 9:
        x = 356
        y = 357
    if checkpoint == 10:
        x = 356
        y = 357
    if checkpoint == 11:
        x = 356
        y = 357
    if checkpoint == 12:  # On the bridge
        x = 356
        y = 357
    if checkpoint == 13:  # Other end of the bridge
        x = -269
        y = 357
    if checkpoint == 14:
        x = -492
        y = 352
    if checkpoint == 15:
        x = -605
        y = 348
    if checkpoint == 16:
        x = -662
        y = 343
    if checkpoint == 17:  # Back to main Calm Lands map
        x = -800
        y = 200
    if checkpoint == 18:
        x = 1394
        y = -1279
    if checkpoint == 19:
        x = 1321
        y = -1258
    if checkpoint == 20:  # Chocobo
        x = 0
        y = 0
    if checkpoint == 21:
        x = 1183
        y = -1141
    if checkpoint == 22:
        x = 1116
        y = -990
    if checkpoint == 23:
        x = 1110
        y = -950
    if checkpoint == 24:  # Feather
        x = 0
        y = 0
    if checkpoint == 25:
        x = 1062
        y = -659
    if checkpoint == 26:
        x = 1062
        y = -659
    if checkpoint == 27:
        x = 1062
        y = -659
    if checkpoint == 28:
        x = 1062
        y = -659
    if checkpoint == 29:
        x = 1207
        y = -254
    if checkpoint == 30:  # Near the arena
        x = 1315
        y = -148
    if checkpoint == 31:
        x = 1418
        y = -147
    if checkpoint == 32:  # Into monster arena
        x = 1500
        y = -190
    if checkpoint == 33:
        x = 0
        y = 0
    if checkpoint == 34:
        x = 0
        y = 0
    if checkpoint == 35:
        x = 0
        y = 0
    if checkpoint == 36:
        x = 0
        y = 0
    if checkpoint == 37:
        x = 0
        y = 0
    if checkpoint == 38:
        x = 0
        y = 0
    if checkpoint == 39:
        x = 0
        y = 0
    if checkpoint == 40:
        x = 0
        y = 0
    return [x, y]


def tp_farm(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 6
        y = -54
    if checkpoint == 1:
        x = 10
        y = -200
    if checkpoint == 2:  # Outside agency
        x = -48
        y = 54
    if checkpoint == 3:  # To North
        x = 0
        y = 300
    if checkpoint == 4:  # North pos 1
        x = -127
        y = -1083
    if checkpoint == 5:  # North pos 2
        x = -106
        y = -1185
    if checkpoint == 6:  # Back to agency front
        x = -115
        y = -1400
    if checkpoint == 7:
        x = -55
        y = 27
    if checkpoint == 8:  # To South
        x = -50
        y = -200
    if checkpoint == 9:  # South pos 1
        x = -44
        y = 1075
    if checkpoint == 10:  # South pos 2
        x = 16
        y = 1116
    if checkpoint == 11:  # Back to agency front
        x = 4
        y = 1300
    if checkpoint == 12:
        x = -56
        y = 51
    if checkpoint == 13:  # Back to north
        x = 0
        y = 300
    if checkpoint == 14:
        x = 0
        y = 0
    if checkpoint == 15:
        x = 0
        y = 0
    if checkpoint == 16:
        x = 0
        y = 0
    if checkpoint == 17:
        x = 0
        y = 0
    if checkpoint == 18:
        x = 0
        y = 0
    if checkpoint == 19:
        x = 0
        y = 0
    if checkpoint == 20:
        x = -84
        y = 32
    if checkpoint == 21:  # Into agency
        x = -150
        y = 35
    if checkpoint == 22:
        x = -31
        y = -17
    if checkpoint == 23:
        x = 0
        y = 0
    if checkpoint == 24:
        x = 0
        y = 0
    if checkpoint == 25:
        x = 0
        y = 0
    if checkpoint == 26:
        x = 0
        y = 0
    if checkpoint == 27:
        x = 0
        y = 0
    if checkpoint == 28:
        x = 0
        y = 0
    if checkpoint == 29:
        x = 0
        y = 0
    if checkpoint == 30:
        x = 0
        y = 0
    if checkpoint == 31:
        x = 0
        y = 0
    if checkpoint == 32:
        x = 0
        y = 0
    if checkpoint == 33:
        x = 0
        y = 0
    if checkpoint == 34:
        x = 0
        y = 0
    if checkpoint == 35:
        x = 0
        y = 0
    if checkpoint == 36:
        x = 0
        y = 0
    if checkpoint == 37:
        x = 0
        y = 0
    if checkpoint == 38:
        x = 0
        y = 0
    if checkpoint == 39:
        x = 0
        y = 0
    if checkpoint == 40:
        x = 0
        y = 0
    if checkpoint == 41:
        x = 0
        y = 0
    if checkpoint == 42:
        x = 0
        y = 0
    if checkpoint == 43:
        x = 0
        y = 0
    if checkpoint == 44:
        x = 0
        y = 0
    if checkpoint == 45:
        x = 0
        y = 0
    if checkpoint == 46:
        x = 0
        y = 0
    if checkpoint == 47:
        x = 0
        y = 0
    if checkpoint == 48:
        x = 0
        y = 0
    if checkpoint == 49:
        x = 0
        y = 0
    if checkpoint == 50:
        x = 0
        y = 0
    return [x, y]


def calm_lands_1_old(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -620
        y = -142
    if checkpoint == 1:
        x = -519
        y = -301
    if checkpoint == 2:
        x = -435
        y = -568
    if checkpoint == 3:  # First farm position
        x = -351
        y = -706
    if checkpoint == 4:
        x = -370
        y = -902
    if checkpoint == 5:  # Onward to next area
        x = -201
        y = 143
    if checkpoint == 6:
        x = 266
        y = -559
    if checkpoint == 7:
        x = 969
        y = -253
    if checkpoint == 8:
        x = 1179
        y = -212
    if checkpoint == 9:
        x = 1314
        y = -83
    if checkpoint == 10:  # Continue on to the arena
        x = 1402
        y = -134
    if checkpoint == 11:
        x = 1500
        y = -200
    return [x, y]


def calm_lands_1(checkpoint):
    # logger.debug("CKP:", checkpoint)
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
    if checkpoint == 5:  # First divergence from the standard path
        x = -761
        y = -1433
    if checkpoint == 6:
        x = -253
        y = -1038
    if checkpoint == 7:
        x = 581
        y = -464
    if checkpoint == 8:
        x = 1223
        y = -187
    if checkpoint == 9:
        x = 1345
        y = -129
    if checkpoint == 10:
        x = 1500
        y = -125
    return [x, y]


def calm_farm(checkpoint):
    # logger.debug("CKP:", checkpoint)
    x = 999
    y = 999
    if checkpoint == 0:
        x = -634
        y = -126
    if checkpoint == 1:
        x = -605
        y = -144
    if checkpoint == 2:  # Zone 1 position 1
        x = -579
        y = -178
    if checkpoint == 3:  # Zone 1 position 2
        x = -561
        y = -99
    if checkpoint == 4:  # Zone 2 position 1
        x = -503
        y = -60
    if checkpoint == 5:  # Zone 2 position 2
        x = -521
        y = 10
    if checkpoint == 6:  # Zone 3 position 1
        x = -548
        y = 22
    if checkpoint == 7:  # Zone 3 position 2
        x = -620
        y = 26
    if checkpoint == 8:
        x = -521
        y = 3
    if checkpoint == 9:
        x = -550
        y = -97
    return [x, y]


def calm_lands_2(checkpoint):
    # logger.debug("CKP2:", checkpoint)
    x = 999
    y = 999
    if checkpoint == 0:
        x = 1336
        y = -101
    if checkpoint == 1:
        x = 1349
        y = 160
    if checkpoint == 2:
        x = 1429
        y = 486
    if checkpoint == 3:
        x = 1480
        y = 646
    if checkpoint == 4:
        x = 1494
        y = 878
    if checkpoint == 5:
        x = 1542
        y = 1021
    if checkpoint == 6:
        x = 1561
        y = 1112
    if checkpoint == 7:
        x = 1600
        y = 1300
    return [x, y]


def besaid_farm(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -345
        y = -470
    if checkpoint == 1:  # Map change
        x = 0
        y = 0
    if checkpoint == 2:
        x = 51
        y = -34
    if checkpoint == 3:
        x = 13
        y = 2
    if checkpoint == 4:
        x = -15
        y = -21
    if checkpoint == 5:
        x = -38
        y = -19
    if checkpoint == 6:
        x = -35
        y = 2
    if checkpoint == 7:
        x = -22
        y = 24
    if checkpoint == 8:
        x = -16
        y = 43
    if checkpoint == 9:
        x = -35
        y = 57
    if checkpoint == 10:
        x = -67
        y = 69
    if checkpoint == 11:  # Map to map
        x = 0
        y = 0
    if checkpoint == 12:
        x = 424
        y = 122
    if checkpoint == 13:
        x = 369
        y = 5
    if checkpoint == 14:
        x = 424
        y = 122
    if checkpoint == 15:
        x = 454
        y = 199
    if checkpoint == 16:  # Back to previous map
        x = 5000
        y = 3000
    if checkpoint == 17:
        x = -22
        y = 52
    if checkpoint == 18:
        x = -12
        y = 25
    if checkpoint == 19:
        x = -38
        y = -2
    if checkpoint == 20:
        x = -31
        y = -20
    if checkpoint == 21:
        x = 4
        y = -11
    if checkpoint == 22:
        x = 18
        y = 0
    if checkpoint == 23:
        x = 64
        y = -28
    if checkpoint == 24:
        x = 70
        y = -73
    if checkpoint == 25:  # Back to beach
        x = 0
        y = 0
    if checkpoint == 26:
        x = 0
        y = 0
    if checkpoint == 27:
        x = 0
        y = 0
    if checkpoint == 28:
        x = 0
        y = 0
    if checkpoint == 29:
        x = 0
        y = 0
    if checkpoint == 30:
        x = 0
        y = 0
    return [x, y]


def kilika_farm(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 23
        y = -255
    if checkpoint == 1:
        x = -17
        y = -247
    if checkpoint == 2:
        x = -27
        y = -207
    if checkpoint == 3:
        x = -34
        y = -170
    if checkpoint == 4:  # To next map
        x = 0
        y = 0
    if checkpoint == 5:
        x = 85
        y = 90
    if checkpoint == 6:
        x = 0
        y = 119
    if checkpoint == 7:
        x = -112
        y = 114
    if checkpoint == 8:
        x = -124
        y = 137
    if checkpoint == 9:
        x = -158
        y = 210
    if checkpoint == 10:
        x = -150
        y = 259
    if checkpoint == 11:  # To the woods
        x = 0
        y = 0
    if checkpoint == 12:
        x = -67
        y = -451
    if checkpoint == 13:
        x = -84
        y = -527
    if checkpoint == 14:  # Return if complete
        x = -100
        y = -600
    if checkpoint == 15:
        x = -152
        y = 195
    if checkpoint == 16:
        x = -118
        y = 115
    if checkpoint == 17:
        x = -97
        y = 103
    if checkpoint == 18:
        x = -4
        y = 109
    if checkpoint == 19:
        x = 91
        y = 97
    if checkpoint == 20:
        x = 91
        y = 37
    if checkpoint == 21:  # Back to save sphere screen
        x = 0
        y = 0
    if checkpoint == 22:
        x = -48
        y = -201
    if checkpoint == 23:
        x = -3
        y = -248
    if checkpoint == 24:
        x = 31
        y = -258
    if checkpoint == 25:
        x = 0
        y = 0
    if checkpoint == 26:
        x = 0
        y = 0
    if checkpoint == 27:
        x = 0
        y = 0
    if checkpoint == 28:
        x = 0
        y = 0
    if checkpoint == 29:
        x = 0
        y = 0
    if checkpoint == 30:
        x = 0
        y = 0
    return [x, y]


def miihen_farm(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 13
        y = -26
    if checkpoint == 1:
        x = -8
        y = -59
    if checkpoint == 2:  # Exit agency
        x = 0
        y = 0
    if checkpoint == 3:
        x = 42
        y = -185
    if checkpoint == 4:
        x = 40
        y = -173
    if checkpoint == 5:
        x = 26
        y = -103
    if checkpoint == 6:
        x = -15
        y = 302
    if checkpoint == 7:
        x = -57
        y = 348
    if checkpoint == 8:  # To the map with encounters
        x = 0
        y = 0
    if checkpoint == 9:
        x = -173
        y = -815
    if checkpoint == 10:
        x = -159
        y = -715
    if checkpoint == 11:
        x = -117
        y = -623
    if checkpoint == 12:
        x = -46
        y = -501
    if checkpoint == 13:
        x = 39
        y = -357
    if checkpoint == 14:
        x = 63
        y = -289
    if checkpoint == 15:  # Bridge
        x = 136
        y = -170
    if checkpoint == 16:
        x = 162
        y = -30
    if checkpoint == 17:
        x = 142
        y = 44
    if checkpoint == 18:  # Into next zone
        x = 100
        y = 180
    if checkpoint == 19:
        x = 20
        y = 294
    if checkpoint == 20:
        x = 21
        y = 376
    if checkpoint == 21:
        x = 127
        y = 471
    if checkpoint == 22:
        x = 181
        y = 462
    if checkpoint == 23:
        x = 212
        y = 430
    if checkpoint == 24:
        x = 192
        y = 348
    if checkpoint == 25:
        x = 221
        y = 282
    if checkpoint == 26:
        x = 288
        y = 222
    if checkpoint == 27:
        x = 426
        y = 249
    if checkpoint == 28:
        x = 605
        y = 370
    if checkpoint == 29:
        x = 610
        y = 411
    if checkpoint == 30:  # Farm zone 1
        x = 593
        y = 552
    if checkpoint == 31:  # To the "meeting Seymour" screen
        x = 500
        y = 700
    if checkpoint == 32:
        x = -62
        y = -98
    if checkpoint == 33:  # Branch to zone 2 vs zones >= 3
        x = -31
        y = -81
    if checkpoint == 34:
        x = 14
        y = -75
    if checkpoint == 35:  # Entrance towards area 2
        x = 86
        y = -143
    if checkpoint == 36:
        x = 185
        y = -223
    if checkpoint == 37:
        x = 227
        y = -274
    if checkpoint == 38:  # Into lower area
        x = 270
        y = -320
    if checkpoint == 39:  # Into lower area
        x = 270
        y = -320
    if checkpoint == 40:
        x = 708
        y = 335
    if checkpoint == 41:
        x = 740
        y = 450
    if checkpoint == 42:  # Return to map
        x = 800
        y = 550
    if checkpoint == 43:
        x = 172
        y = -219
    if checkpoint == 44:
        x = 47
        y = -107
    if checkpoint == 45:  # Branch to zone 1 vs zones >= 3
        x = 14
        y = -40
    if checkpoint == 46:
        x = 2
        y = 109
    if checkpoint == 47:  # Save sphere, touch if needed.
        x = 2
        y = 109
    if checkpoint == 48:
        x = -45
        y = 193
    if checkpoint == 49:
        x = -42
        y = 318
    if checkpoint == 50:  # To MRR start area
        x = -42
        y = 500
    if checkpoint == 51:  # Farm area 3(A)
        x = -87
        y = -911
    if checkpoint == 52:  # Farm area 3(A)
        x = -78
        y = -861
    if checkpoint == 53:
        x = -46
        y = -757
    if checkpoint == 54:
        x = -44
        y = -716
    if checkpoint == 55:
        x = -48
        y = -643
    if checkpoint == 56:
        x = -23
        y = -571
    if checkpoint == 57:
        x = -38
        y = -492
    if checkpoint == 58:  # Farm area 3(B)
        x = -115
        y = -476
    if checkpoint == 59:  # Farm area 3(B)
        x = -209
        y = -420
    if checkpoint == 60:  # To MRR map
        x = -300
        y = -350
    if checkpoint == 61:  # Farm area 4
        x = 21
        y = -725
    if checkpoint == 62:  # Farm area 4 and save sphere
        x = 52
        y = -690
    if checkpoint == 63:  # Back to Clasko map
        x = 66
        y = -850
    if checkpoint == 64:
        x = -118
        y = -469
    if checkpoint == 65:
        x = -52
        y = -487
    if checkpoint == 66:
        x = -17
        y = -562
    if checkpoint == 67:
        x = -43
        y = -639
    if checkpoint == 68:
        x = -53
        y = -694
    if checkpoint == 69:
        x = -43
        y = -722
    if checkpoint == 70:
        x = -56
        y = -850
    if checkpoint == 71:
        x = -79
        y = -950
    if checkpoint == 72:  # Back to transition map
        x = -90
        y = -1100
    if checkpoint == 73:
        x = -56
        y = 255
    if checkpoint == 74:
        x = -32
        y = 174
    if checkpoint == 75:
        x = 4
        y = 132
    if checkpoint == 76:  # Save sphere, and back towards areas 1/2
        x = -3
        y = 22
    if checkpoint == 77:  # Back towards area 1
        x = -58
        y = -105
    if checkpoint == 78:
        x = -144
        y = -247
    if checkpoint == 79:  # Map change
        x = -230
        y = -330
    if checkpoint == 90:  # Area 6 back to 5 logic
        x = -39
        y = -236
    if checkpoint == 91:  # Area 6 back to 5 logic
        x = -53
        y = -274
    if checkpoint == 92:  # Area 6 back to 5 logic
        # Down the lift
        x = -53
        y = -274
    if checkpoint == 93:  # Area 6 back to 5 logic
        x = 66
        y = 874
    if checkpoint == 100:  # Start, area 5/6 logic
        x = 12
        y = -738
    if checkpoint == 101:
        x = 12
        y = -738
    if checkpoint == 102:
        x = -28
        y = -663
    if checkpoint == 103:
        x = -37
        y = -601
    if checkpoint == 104:  # First lift
        logger.debug("First lift")
    if checkpoint == 105:
        x = -48
        y = -571
    if checkpoint == 106:
        x = -108
        y = -463
    if checkpoint == 107:
        x = -108
        y = -428
    if checkpoint == 108:
        x = -85
        y = -391
    if checkpoint == 109:
        x = -87
        y = -372
    if checkpoint == 110:
        x = -78
        y = -361
    if checkpoint == 111:
        x = -38
        y = -367
    if checkpoint == 112:
        x = -6
        y = -381
    if checkpoint == 113:
        x = 38
        y = -414
    if checkpoint == 114:
        x = 63
        y = -398
    if checkpoint == 115:
        x = 109
        y = -339
    if checkpoint == 116:
        x = 127
        y = -198
    if checkpoint == 117:
        x = 122
        y = -166
    if checkpoint == 118:
        x = 91
        y = -176
    if checkpoint == 119:
        x = 0
        y = -215
    if checkpoint == 120:
        x = -63
        y = -189
    if checkpoint == 121:
        x = -88
        y = -141
    if checkpoint == 122:
        x = -104
        y = 54
    if checkpoint == 123:
        x = -102
        y = 73
    if checkpoint == 124:
        x = -86
        y = 87
    if checkpoint == 125:
        x = 25
        y = 138
    if checkpoint == 126:
        x = 32
        y = 151
    if checkpoint == 127:
        x = 23
        y = 233
    if checkpoint == 128:
        x = -89
        y = 295
    if checkpoint == 129:
        x = -91
        y = 321
    if checkpoint == 130:
        x = -87
        y = 368
    if checkpoint == 131:
        x = -68
        y = 402
    if checkpoint == 132:
        x = -48
        y = 425
    if checkpoint == 133:
        x = 35
        y = 461
    if checkpoint == 134:
        x = 92
        y = 515
    if checkpoint == 135:
        x = 51
        y = 543
    if checkpoint == 136:
        x = -20
        y = 568
    if checkpoint == 137:
        x = -71
        y = 593
    if checkpoint == 138:
        x = -109
        y = 604
    if checkpoint == 139:
        x = -115
        y = 687
    if checkpoint == 140:
        x = -71
        y = 775
    if checkpoint == 141:
        x = -39
        y = 829
    if checkpoint == 142:
        x = -12
        y = 838
    if checkpoint == 143:
        x = 26
        y = 828
    if checkpoint == 144:
        x = 44
        y = 834
    if checkpoint == 145:
        x = 59
        y = 898
    if checkpoint == 146:  # Second lift
        logger.debug("Up the second lift")
    if checkpoint == 147:
        x = -36
        y = -194
    if checkpoint == 148:
        x = -36
        y = -194
    if checkpoint == 149:
        x = 24
        y = -157
    if checkpoint == 150:
        x = 52
        y = -135
    if checkpoint == 151:
        x = 116
        y = 4
    if checkpoint == 152:
        x = 121
        y = 50
    if checkpoint == 153:
        x = 112
        y = 100
    if checkpoint == 154:
        x = 29
        y = 227
    if checkpoint == 155:
        x = 29
        y = 227
    if checkpoint == 156:
        x = 29
        y = 227
    if checkpoint == 157:
        x = 29
        y = 227
    if checkpoint == 158:
        logger.debug("Up the third lift")
    if checkpoint == 159:
        x = 59
        y = 244
    if checkpoint == 160:
        x = 99
        y = 254
    if checkpoint == 161:
        x = 198
        y = 251
    if checkpoint == 162:
        x = 219
        y = 202
    if checkpoint == 163:  # Diagonal towards the save sphere
        x = 226
        y = 170
    # logger.debug("Dest: [", x, ", ", y, "]")
    return [x, y]


def mrr_farm(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -8
        y = -705
    if checkpoint == 1:
        x = -74
        y = -606
    if checkpoint == 2:
        x = -8
        y = -705
    if checkpoint == 3:
        x = 6
        y = -733
    if checkpoint == 4:
        x = 0
        y = 0
    return [x, y]


def arena_return(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -635
        y = -137
    if checkpoint == 1:
        x = -637
        y = -245
    if checkpoint == 2:
        x = 97
        y = -298
    if checkpoint == 3:
        x = 553
        y = -245
    if checkpoint == 4:
        x = 1308
        y = -138
    if checkpoint == 5:
        x = 1398
        y = -129
    if checkpoint == 6:
        x = 1500
        y = -250
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


def yojimbo(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 1
        y = 23
    if checkpoint == 1:
        x = 26
        y = -207
    if checkpoint == 2:
        x = 17
        y = -357
    if checkpoint == 3:
        x = -20
        y = -474
    if checkpoint == 4:
        x = -98
        y = -523
    if checkpoint == 5:  # To Defender X map
        x = 0
        y = 0
    if checkpoint == 6:
        x = -8
        y = 227
    if checkpoint == 7:
        x = -11
        y = 94
    if checkpoint == 8:
        x = 120
        y = 105
    if checkpoint == 9:
        x = 120
        y = 105
    if checkpoint == 10:
        x = 120
        y = 105
    if checkpoint == 11:
        x = 143
        y = 155
    if checkpoint == 12:
        x = 80
        y = 173
    if checkpoint == 13:
        x = -52
        y = 186
    if checkpoint == 14:  # To gorge map
        x = 0
        y = 0
    if checkpoint == 15:
        x = -224
        y = 204
    if checkpoint == 16:
        x = -282
        y = 155
    if checkpoint == 17:
        x = -323
        y = 158
    if checkpoint == 18:
        x = -387
        y = 157
    if checkpoint == 19:  # Into the cave
        x = 0
        y = 0
    if checkpoint == 20:
        x = -2
        y = 180
    if checkpoint == 21:
        x = 78
        y = 272
    if checkpoint == 22:
        x = 187
        y = 277
    if checkpoint == 23:
        x = 309
        y = 284
    if checkpoint == 24:
        x = 392
        y = 326
    if checkpoint == 25:  # White 1
        x = 418
        y = 385
    if checkpoint == 26:  # White 2
        x = 430
        y = 440
    if checkpoint == 27:  # Green 1
        x = 424
        y = 481
    if checkpoint == 28:  # Green 2
        x = 451
        y = 507
    if checkpoint == 29:  # Green 3
        x = 453
        y = 469
    if checkpoint == 30:  # Onward
        x = 435
        y = 510
    if checkpoint == 31:
        x = 435
        y = 510
    if checkpoint == 32:
        x = 435
        y = 510
    if checkpoint == 33:
        x = 435
        y = 510
    if checkpoint == 34:
        x = 435
        y = 510
    if checkpoint == 35:
        x = 435
        y = 510
    if checkpoint == 36:  # Conversation with the party
        x = 426
        y = 805
    if checkpoint == 37:
        x = 420
        y = 912
    if checkpoint == 38:
        x = 387
        y = 934
    if checkpoint == 39:
        x = 320
        y = 956
    if checkpoint == 40:
        x = 262
        y = 1038
    if checkpoint == 41:
        x = 267
        y = 1162
    if checkpoint == 42:
        x = 251
        y = 1291
    if checkpoint == 43:
        x = 190
        y = 1291
    if checkpoint == 44:
        x = 10
        y = 1304
    if checkpoint == 45:
        x = -64
        y = 1399
    if checkpoint == 46:  # Near the chest, hard right.
        x = -67
        y = 1501
    if checkpoint == 47:  # Save sphere
        x = 36
        y = 1536
    if checkpoint == 48:
        x = 106
        y = 1633
    if checkpoint == 49:
        x = 94
        y = 1823
    if checkpoint == 50:
        x = 93
        y = 1927
    if checkpoint == 51:  # On the platform.
        x = 93
        y = 1961
    if checkpoint == 52:  # Teleport to boss room
        x = 0
        y = 0
    if checkpoint == 53:  # Talking to Yojimbo's fayth
        x = 0
        y = 0
    if checkpoint == 54:
        x = 93
        y = 1961
    if checkpoint == 55:  # Teleport to start.
        x = 0
        y = 0
    if checkpoint == 56:
        x = 0
        y = 164
    if checkpoint == 57:
        x = 5
        y = 88
    if checkpoint == 58:
        x = -8
        y = 11
    if checkpoint == 59:  # Back to gorge map
        x = 0
        y = 0
    if checkpoint == 60:
        x = -378
        y = 132
    if checkpoint == 61:
        x = -313
        y = 163
    return [x, y]


def djose_farm(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 491
        y = -126
    if checkpoint == 1:
        x = 488
        y = 11
    if checkpoint == 2:
        x = 503
        y = 47
    if checkpoint == 3:
        x = 605
        y = 26
    if checkpoint == 4:
        x = 826
        y = 19
    if checkpoint == 5:
        x = 950
        y = 56
    if checkpoint == 6:
        x = 1040
        y = 150
    if checkpoint == 7:  # Map to map
        x = 1300
        y = 300
    if checkpoint == 8:
        x = -238
        y = -771
    if checkpoint == 9:
        x = -235
        y = -661
    if checkpoint == 10:
        x = -186
        y = -405
    if checkpoint == 11:
        x = -117
        y = -164
    if checkpoint == 12:
        x = -64
        y = 40
    if checkpoint == 13:
        x = -40
        y = 75
    if checkpoint == 14:
        x = 30
        y = 214
    if checkpoint == 15:
        x = 138
        y = 409
    if checkpoint == 16:
        x = 212
        y = 479
    if checkpoint == 17:
        x = 298
        y = 577
    if checkpoint == 18:
        x = 456
        y = 714
    if checkpoint == 19:
        x = 536
        y = 746
    if checkpoint == 20:
        x = 617
        y = 803
    if checkpoint == 21:
        x = 642
        y = 847
    if checkpoint == 22:
        x = 615
        y = 983
    if checkpoint == 23:
        x = 536
        y = 967
    if checkpoint == 24:  # To next zone
        x = 550
        y = 1100
    if checkpoint == 25:
        x = -977
        y = 1705
    if checkpoint == 26:
        x = -875
        y = 1824
    if checkpoint == 27:  # Back to previous map
        x = -775
        y = 1950
    if checkpoint == 28:
        x = 631
        y = 858
    if checkpoint == 29:
        x = 750
        y = 861
    if checkpoint == 30:  # To the temple map
        x = 900
        y = 870
    if checkpoint == 31:
        x = 37
        y = -139
    if checkpoint == 32:
        x = 38
        y = -111
    if checkpoint == 33:
        x = 64
        y = -18
    if checkpoint == 34:
        x = 22
        y = 164
    if checkpoint == 35:  # Map to map
        x = 0
        y = 300
    if checkpoint == 36:
        x = 88
        y = -263
    if checkpoint == 37:
        x = 0
        y = 0
    if checkpoint == 38:  # Start heading back
        x = 20
        y = -353
    if checkpoint == 39:  # Back to bridge map
        x = 0
        y = -450
    if checkpoint == 40:
        x = 43
        y = 73
    if checkpoint == 41:
        x = 45
        y = 16
    if checkpoint == 42:
        x = 58
        y = -30
    if checkpoint == 43:
        x = 53
        y = -124
    if checkpoint == 44:
        x = -2
        y = -277
    if checkpoint == 45:  # Back to area 1
        x = -50
        y = -440
    if checkpoint == 46:
        x = 623
        y = 850
    if checkpoint == 47:
        x = 0
        y = 0
    if checkpoint == 48:
        x = 0
        y = 0
    if checkpoint == 49:
        x = 0
        y = 0
    if checkpoint == 50:
        x = 0
        y = 0
    return [x, y]


def mac_farm(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 19
        y = -23
    if checkpoint == 1:
        x = -9
        y = -61
    if checkpoint == 2:  # Exit agency
        x = -14
        y = -150
    if checkpoint == 3:
        x = 52
        y = -34
    if checkpoint == 4:
        x = 121
        y = -33
    if checkpoint == 5:  # Edge of snow zone
        x = 176
        y = 60
    if checkpoint == 6:  # Leave lake area
        x = 250
        y = 200
    if checkpoint == 7:
        x = 33
        y = -34
    if checkpoint == 8:
        x = 95
        y = -57
    if checkpoint == 9:
        x = 146
        y = -84
    if checkpoint == 10:  # Past save sphere
        x = 214
        y = -111
    if checkpoint == 11:  # Exit to woods area
        x = 300
        y = -120
    if checkpoint == 12:
        x = -596
        y = -20
    if checkpoint == 13:
        x = -643
        y = -82
    if checkpoint == 14:  # Back to save sphere map
        x = -700
        y = -150
    if checkpoint == 15:
        x = 214
        y = -111
    if checkpoint == 16:
        x = 146
        y = -84
    if checkpoint == 17:
        x = 95
        y = -57
    if checkpoint == 18:
        x = 33
        y = -34
    if checkpoint == 19:  # North to lake
        x = -150
        y = -150
    if checkpoint == 20:
        x = 0
        y = 0
    return [x, y]


def bikanel_farm(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -11
        y = -96
    if checkpoint == 1:
        x = 9
        y = -244
    if checkpoint == 2:
        x = 54
        y = -384
    if checkpoint == 3:
        x = 93
        y = -399
    if checkpoint == 4:
        x = 197
        y = -394
    if checkpoint == 5:  # Second map
        x = 300
        y = -390
    if checkpoint == 6:
        x = -49
        y = -584
    if checkpoint == 7:
        x = -222
        y = -459
    if checkpoint == 8:
        x = -170
        y = -313
    if checkpoint == 9:
        x = -20
        y = -296
    if checkpoint == 10:
        x = 155
        y = -220
    if checkpoint == 11:
        x = 186
        y = -122
    if checkpoint == 12:
        x = 166
        y = 3
    if checkpoint == 13:
        x = 157
        y = 38
    if checkpoint == 14:  # Past Rikku tent
        x = 181
        y = 71
    if checkpoint == 15:
        x = 238
        y = 110
    if checkpoint == 16:
        x = 343
        y = 102
    if checkpoint == 17:
        x = 611
        y = 141
    if checkpoint == 18:
        x = 669
        y = 255
    if checkpoint == 19:
        x = 652
        y = 542
    if checkpoint == 20:  # Sign post
        x = 625
        y = 789
    if checkpoint == 21:
        x = 705
        y = 870
    if checkpoint == 22:  # Into big map (the first one)
        x = 800
        y = 1000
    if checkpoint == 23:
        x = 490
        y = -770
    if checkpoint == 24:
        x = 400
        y = -438
    if checkpoint == 25:
        x = 17
        y = 88
    if checkpoint == 26:
        x = -116
        y = 265
    if checkpoint == 27:
        x = -263
        y = 305
    if checkpoint == 28:  # Just before the danger zone
        x = -312
        y = 387
    if checkpoint == 29:  # Now in the danger zone
        x = -350
        y = 470
    if checkpoint == 30:  # Danger zone 2
        x = -363
        y = 583
    if checkpoint == 31:  # Onward (if needed) to the other zone
        x = -522
        y = 649
    if checkpoint == 32:
        x = -656
        y = 752
    if checkpoint == 33:  # Into the West zone
        x = -660
        y = 900
    if checkpoint == 34:
        x = -310
        y = -235
    if checkpoint == 35:
        x = -447
        y = -188
    if checkpoint == 36:  # Back to ruins
        x = -700
        y = -300
    if checkpoint == 37:
        x = -587
        y = 632
    if checkpoint == 38:
        x = -439
        y = 547
    if checkpoint == 39:  # Around danger zone 2
        x = -343
        y = 461
    if checkpoint == 40:
        x = -305
        y = 399
    if checkpoint == 41:
        x = -266
        y = 341
    if checkpoint == 42:
        x = -149
        y = 293
    if checkpoint == 43:
        x = -30
        y = 249
    if checkpoint == 44:  # Back to airship
        x = 0
        y = 0
    if checkpoint == 45:
        x = 0
        y = 0
    if checkpoint == 46:
        x = 0
        y = 0
    if checkpoint == 47:
        x = 0
        y = 0
    if checkpoint == 48:
        x = 0
        y = 0
    if checkpoint == 49:
        x = 0
        y = 0
    if checkpoint == 50:
        x = 0
        y = 0
    return [x, y]


def gagazet(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:  # Arrival, start of sections 2/4
        x = 39
        y = 99
    if checkpoint == 1:  # Platform, to cave
        x = 54
        y = 105
    if checkpoint == 2:  # Activate platform
        x = 0
        y = 0
    if checkpoint == 3:
        x = 95
        y = -946
    if checkpoint == 4:
        x = 27
        y = -830
    if checkpoint == 5:
        x = 24
        y = -658
    if checkpoint == 6:
        x = 15
        y = -553
    if checkpoint == 7:
        x = 61
        y = -482
    if checkpoint == 8:
        x = 178
        y = -363
    if checkpoint == 9:  # To Wakka trials zone
        x = 250
        y = -190
    if checkpoint == 10:
        x = -55
        y = -414
    if checkpoint == 11:
        x = -82
        y = -475
    if checkpoint == 12:  # Return when complete
        x = -55
        y = -600
    if checkpoint == 13:
        x = 65
        y = -484
    if checkpoint == 14:
        x = 19
        y = -555
    if checkpoint == 15:
        x = 18
        y = -659
    if checkpoint == 16:
        x = 42
        y = -785
    if checkpoint == 17:
        x = 69
        y = -906
    if checkpoint == 18:
        x = 124
        y = -964
    if checkpoint == 19:
        x = 109
        y = -1021
    if checkpoint == 20:  # Platform, back to ronso
        x = 113
        y = -1034
    if checkpoint == 21:  # Activate platform - end of sections 2/4
        x = 0
        y = 0
    # Start of Zanarkand Overpass section (after platform)
    if checkpoint == 22:
        x = 106
        y = -63
    if checkpoint == 23:  # To next map
        x = 240
        y = -200
    if checkpoint == 24:
        x = 12
        y = -855
    if checkpoint == 25:
        x = 0
        y = -961
    if checkpoint == 26:  # Back to campfire map
        x = 0
        y = -1100
    if checkpoint == 27:
        x = 97
        y = -56
    if checkpoint == 28:
        x = 111
        y = 28
    if checkpoint == 29:  # End of Zanarkand Overpass section
        x = 0
        y = 0
    if checkpoint == 30:  # Start of Mountain Path
        x = 36
        y = 85
    if checkpoint == 31:
        x = 20
        y = 165
    if checkpoint == 32:
        x = 42
        y = 266
    if checkpoint == 33:
        x = 59
        y = 369
    if checkpoint == 34:  # To mountain path
        x = 70
        y = 600
    if checkpoint == 35:
        x = -10
        y = -60
    if checkpoint == 36:
        x = 7
        y = -146
    if checkpoint == 37:  # Return when complete
        x = 7
        y = -300
    if checkpoint == 38:
        x = 52
        y = 329
    if checkpoint == 39:
        x = 34
        y = 218
    if checkpoint == 40:  # End of Mountain Path
        x = 21
        y = 125
    if checkpoint == 41:  # Back towards save sphere
        x = 30
        y = 83
    if checkpoint == 42:
        x = -37
        y = 87
    if checkpoint == 43:  # Return to airship, or touch sphere and start over
        x = 0
        y = 0
    if checkpoint == 44:
        x = 8
        y = -51
    if checkpoint == 45:
        x = 19
        y = 81
    if checkpoint == 46:
        x = 45
        y = 241
    if checkpoint == 47:
        x = 63
        y = 349
    if checkpoint == 48:
        x = 9
        y = 414
    if checkpoint == 49:
        x = -34
        y = 441
    if checkpoint == 50:
        x = -79
        y = 452
    if checkpoint == 51:
        x = -137
        y = 407
    if checkpoint == 52:
        x = -206
        y = 325
    if checkpoint == 53:
        x = -247
        y = 311
    if checkpoint == 54:
        x = -275
        y = 317
    if checkpoint == 55:
        x = -320
        y = 371
    if checkpoint == 56:
        x = -349
        y = 441
    if checkpoint == 57:
        x = -389
        y = 476
    if checkpoint == 58:
        x = -436
        y = 438
    if checkpoint == 59:
        x = -456
        y = 377
    if checkpoint == 60:
        x = -527
        y = 279
    if checkpoint == 61:
        x = -578
        y = 220
    if checkpoint == 62:
        x = -722
        y = 202
    if checkpoint == 63:
        x = -916
        y = 167
    if checkpoint == 64:
        x = -940
        y = 188
    if checkpoint == 65:
        x = -925
        y = 306
    if checkpoint == 66:
        x = -881
        y = 376
    if checkpoint == 67:
        x = -865
        y = 478
    if checkpoint == 68:
        x = -825
        y = 540
    if checkpoint == 69:
        x = -737
        y = 572
    if checkpoint == 70:
        x = -661
        y = 541
    if checkpoint == 71:
        x = -623
        y = 505
    if checkpoint == 72:
        x = -594
        y = 358
    if checkpoint == 73:
        x = -564
        y = 241
    if checkpoint == 74:
        x = -527
        y = 208
    if checkpoint == 75:
        x = -499
        y = 220
    if checkpoint == 76:
        x = -522
        y = 243
    if checkpoint == 77:
        x = -574
        y = 262
    if checkpoint == 78: # Open chest
        x = 0
        y = 0
    if checkpoint == 79:
        x = 0
        y = 0
    if checkpoint == 80:
        x = 0
        y = 0
    return [x, y]


def gagazet_1(checkpoint):  # No longer used
    x = 999
    y = 999
    if checkpoint == 0:
        x = 39
        y = 99
    if checkpoint == 1:
        x = 54
        y = 105
    if checkpoint == 2:  # Platform, to cave
        x = 0
        y = 0
    if checkpoint == 3:
        x = 95
        y = -946
    if checkpoint == 4:
        x = 27
        y = -830
    if checkpoint == 5:
        x = 24
        y = -658
    if checkpoint == 6:
        x = 15
        y = -553
    if checkpoint == 7:
        x = 61
        y = -482
    if checkpoint == 8:
        x = 178
        y = -363
    if checkpoint == 9:  # To Wakka trials zone
        x = 250
        y = -190
    if checkpoint == 10:
        x = -55
        y = -414
    if checkpoint == 11:
        x = -82
        y = -475
    if checkpoint == 12:  # Return when complete
        x = -55
        y = -600
    if checkpoint == 13:
        x = 65
        y = -484
    if checkpoint == 14:
        x = 19
        y = -555
    if checkpoint == 15:
        x = 18
        y = -659
    if checkpoint == 16:
        x = 42
        y = -785
    if checkpoint == 17:
        x = 69
        y = -906
    if checkpoint == 18:
        x = 124
        y = -964
    if checkpoint == 19:
        x = 109
        y = -1021
    if checkpoint == 20:  # Platform, back to ronso
        x = 109
        y = -1040
    if checkpoint == 21:
        x = 0
        y = 0
    if checkpoint == 22:
        x = 0
        y = 0
    if checkpoint == 23:
        x = 0
        y = 0
    if checkpoint == 24:
        x = 0
        y = 0
    if checkpoint == 25:
        x = 0
        y = 0
    return [x, y]


def gagazet_2(checkpoint):  # No longer used
    x = 999
    y = 999
    if checkpoint == 0:
        x = 36
        y = 85
    if checkpoint == 1:
        x = 20
        y = 165
    if checkpoint == 2:
        x = 42
        y = 266
    if checkpoint == 3:
        x = 59
        y = 369
    if checkpoint == 4:  # To mountain path
        x = 70
        y = 600
    if checkpoint == 5:
        x = -15
        y = -1
    if checkpoint == 6:
        x = 7
        y = -146
    if checkpoint == 7:  # Return when complete
        x = 7
        y = -300
    if checkpoint == 8:
        x = 52
        y = 329
    if checkpoint == 9:
        x = 34
        y = 218
    if checkpoint == 10:
        x = 21
        y = 125
    if checkpoint == 11:
        x = 0
        y = 0
    if checkpoint == 12:
        x = 0
        y = 0
    if checkpoint == 13:
        x = 0
        y = 0
    if checkpoint == 14:
        x = 0
        y = 0
    if checkpoint == 15:
        x = 0
        y = 0
    return [x, y]


def gagazet_3(checkpoint):  # No longer used
    x = 999
    y = 999
    if checkpoint == 0:
        x = 49
        y = 119
    if checkpoint == 1:
        x = 49
        y = 119
    if checkpoint == 2:  # To Zanarkand starting spot
        x = 0
        y = 0
    if checkpoint == 3:
        x = 97
        y = -70
    if checkpoint == 4:
        x = 212
        y = -143
    if checkpoint == 5:  # To next map
        x = 340
        y = -210
    if checkpoint == 6:
        x = 4
        y = -808
    if checkpoint == 7:
        x = 1
        y = -944
    if checkpoint == 8:  # Return when farming is complete
        x = 1
        y = -1100
    if checkpoint == 9:
        x = 103
        y = -81
    if checkpoint == 10:
        x = 114
        y = -24
    if checkpoint == 11:
        x = 0
        y = 0
    if checkpoint == 12:
        x = 0
        y = 0
    if checkpoint == 13:
        x = 0
        y = 0
    if checkpoint == 14:
        x = 0
        y = 0
    if checkpoint == 15:
        x = 0
        y = 0
    return [x, y]


def sin(checkpoint):
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
    return [x, y]


def omega(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -105
        y = -1030
    if checkpoint == 1:
        x = -55
        y = -943
    if checkpoint == 2:
        x = -109
        y = -1055
    if checkpoint == 3:  # Return to airship
        x = 0
        y = 0
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
