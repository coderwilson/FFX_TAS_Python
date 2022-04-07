import pyxinput
import time
import FFX_Xbox
import FFX_memory

from math import copysign
import numpy as np

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

def setMovement(target) -> bool:

    player = FFX_memory.getCoords()
    (forward, right) = FFX_memory.getMovementVectors()

    targetPos = np.array([target[0], target[1]])
    playerPos = np.array(player)

    # Calculate forward and right directions relative to camera space
    pX = player[0]
    pY = player[1]
    eX = target[0]
    eY = target[1]
    fX = forward[0]
    fY = forward[1]
    rX = right[0]
    rY = right[1]

    Ly = fX * (eX-pX) + rX * (eY-pY)
    Lx = fY * (eX-pX) + rY * (eY-pY)
    sumsUp = abs(Lx)+abs(Ly)
    if sumsUp == 0:
        sumsUp = 0.01
    Lx /= sumsUp
    Ly /= sumsUp
    if abs(Lx) > abs(Ly):
        Ly = copysign(Ly/Lx if Lx else 0, Ly)
        Lx = copysign(1, Lx)
    elif abs(Ly) > abs(Lx):
        Lx = copysign(Lx/Ly if Ly else 0, Lx)
        Ly = copysign(1, Ly)
    
    
    FFXC.set_movement(Lx, Ly)
    #FFX_memory.waitFrames(frames=1)
    
    if abs(player[1] - target[1]) < 3 and abs(player[0] - target[0]) < 9:
        return True #Checkpoint reached
    else:
        return False

def calmLands1(checkpoint):
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
    if checkpoint == 5: #First divergence from the standard path
        x = -1266
        y = -513
    if checkpoint == 6:
        x = -1418
        y = -224
    if checkpoint == 7:
        x = -1460
        y = 111
    if checkpoint == 8:
        x = -1547
        y = 378
    return [x,y]

def toRemiem(checkpoint):
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
    if checkpoint == 10: #Chocobo feather
        x = 0
        y = 0
    if checkpoint == 11:
        x = 1420
        y = -1268
    if checkpoint == 12:
        x = 1800
        y = -1270
    if checkpoint == 13: #First movement in temple map
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
    if checkpoint == 17: #Far side of bridge
        x = 396
        y = 357
    if checkpoint == 18: #Far side of bridge
        x = 396
        y = 357
    if checkpoint == 19: #Far side of bridge
        x = 396
        y = 357
    if checkpoint == 20: #Far side of bridge
        x = 396
        y = 357
    if checkpoint == 21: #Far side of bridge
        x = 396
        y = 357
    if checkpoint == 22: #Far side of bridge
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
    if checkpoint == 27: #Orb to initiate race
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
    if checkpoint == 31: #Past save sphere
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
    if checkpoint == 35: #Start race
        x = 0
        y = 0
    return [x,y]

def race1(checkpoint):
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
    if checkpoint == 8: #Left of first pole
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
    if checkpoint == 12: #Left of green pole
        x = 884
        y = 749
    if checkpoint == 13:
        x = 779
        y = 774
    if checkpoint == 14: #Around second green pole
        x = 673
        y = 776
    if checkpoint == 15:
        x = 644
        y = 751
    if checkpoint == 16:
        x = 673
        y = 733
    if checkpoint == 17: #End, around second green.
        x = 702
        y = 723
    if checkpoint == 18: #Around first yellow pole
        x = 771
        y = 717
    if checkpoint == 19:
        x = 797
        y = 691
    if checkpoint == 20:
        x = 759
        y = 666
    if checkpoint == 21: #End, around first yellow
        x = 709
        y = 676
    if checkpoint == 22:
        x = 581
        y = 615
    if checkpoint == 23: #Past second/last yellow, last pole
        x = 555
        y = 547
    if checkpoint == 24:
        x = 535
        y = 504
    if checkpoint == 25:
        x = 537
        y = 291
    if checkpoint == 26: #Past first red pole
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
    if checkpoint == 30: #Past second red pole
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
    if checkpoint == 34: #Past third red pole
        x = 762
        y = 532
    if checkpoint == 35:
        x = 662
        y = 437
    if checkpoint == 36: #Fin
        x = 699
        y = 338
    return [x,y]

def race2(checkpoint):
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
    if checkpoint == 8: #Right of first pole
        x = 1272
        y = 474
    if checkpoint == 9:
        x = 1228
        y = 595
    if checkpoint == 10:
        x = 1131
        y = 731
    if checkpoint == 11: #First chest
        x = 0
        y = 0
    if checkpoint == 12: #Right of green thing
        x = 955
        y = 736
    if checkpoint == 13: #Up ramp, avoiding pole
        x = 811
        y = 826
    if checkpoint == 14:
        x = 800
        y = 856
    if checkpoint == 15: #Around blue pole, back towards chest
        x = 830
        y = 881
    if checkpoint == 16:
        x = 964
        y = 824
    if checkpoint == 17: #Second chest
        x = 0
        y = 0
    if checkpoint == 18: #Right of green thing
        x = 955
        y = 736
    if checkpoint == 19: #Up ramp, avoiding pole
        x = 811
        y = 826
    if checkpoint == 20: #Towards third chest
        x = 735
        y = 882
    if checkpoint == 21:
        x = 604
        y = 860
    if checkpoint == 22: #Third chest
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
    if checkpoint == 27: #Left of first red pillar
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
    if checkpoint == 31: #Past second red pole
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
    if checkpoint == 35: #Past third red pole
        x = 762
        y = 532
    if checkpoint == 36:
        x = 662
        y = 437
    if checkpoint == 37: #Fin
        x = 699
        y = 338
    return [x,y]

def race3(checkpoint):
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
    if checkpoint == 8: #Right of first pole
        x = 1272
        y = 474
    if checkpoint == 9:
        x = 1228
        y = 595
    if checkpoint == 10:
        x = 1131
        y = 731
    if checkpoint == 11: #First chest
        x = 0
        y = 0
    if checkpoint == 12: #Right of green thing
        x = 955
        y = 736
    if checkpoint == 13: #Up ramp, avoiding pole
        x = 811
        y = 826
    if checkpoint == 14:
        x = 800
        y = 856
    if checkpoint == 15: #Around blue pole, back towards chest
        x = 830
        y = 881
    if checkpoint == 16:
        x = 964
        y = 824
    if checkpoint == 17: #Second chest
        x = 0
        y = 0
    if checkpoint == 18: #Right of green thing
        x = 955
        y = 736
    if checkpoint == 19: #Up ramp, avoiding pole
        x = 811
        y = 826
    if checkpoint == 20: #Towards third chest
        x = 735
        y = 882
    if checkpoint == 21:
        x = 604
        y = 860
    if checkpoint == 22: #Third chest
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
    if checkpoint == 27: #Fourth chest
        x = 0
        y = 0
    if checkpoint == 28:
        x = 833
        y = 48
    if checkpoint == 29: #Left of yellow
        x = 914
        y = 89
    if checkpoint == 30:
        x = 961
        y = 121
    if checkpoint == 31: #Between yellows
        x = 1060
        y =249
    if checkpoint == 32: #Left of yellow
        x = 1074
        y = 316
    if checkpoint == 33:
        x = 1098
        y = 339
    if checkpoint == 34: #Around yellow
        x = 1115
        y = 308
    if checkpoint == 35: #Next to green
        x = 1112
        y = 231
    if checkpoint == 36:
        x = 1133
        y = 206
    if checkpoint == 37: #Right of green
        x = 1157
        y = 228
    if checkpoint == 38:
        x = 1173
        y = 360
    if checkpoint == 39: #Last chest
        x = 0
        y = 0
    if checkpoint == 40:
        x = 787
        y = 541
    if checkpoint == 41: #Past third red pole
        x = 762
        y = 532
    if checkpoint == 42:
        x = 662
        y = 437
    if checkpoint == 43: #Fin
        x = 699
        y = 338
    return [x,y]

def leaveRemiem(checkpoint):
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
    if checkpoint == 12: #On the bridge
        x = 356
        y = 357
    if checkpoint == 13: #Other end of the bridge
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
    if checkpoint == 17: #Back to main Calm Lands map
        x = -800
        y = 200
    if checkpoint == 18:
        x = 1394
        y = -1279
    if checkpoint == 19:
        x = 1321
        y = -1258
    if checkpoint == 20: #Chocobo
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
    if checkpoint == 24: #Feather
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
    if checkpoint == 30: #Near the arena
        x = 1315
        y = -148
    if checkpoint == 31:
        x = 1418
        y = -147
    if checkpoint == 32: #Into monster arena
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
    return [x,y]

def tpFarm(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 6
        y = -54
    if checkpoint == 1:
        x = 10
        y = -200
    if checkpoint == 2: #Outside agency
        x = -48
        y = 54
    if checkpoint == 3:
        x = 0
        y = 300
    if checkpoint == 4: #North thunder plains
        x = -97
        y = -1056
    if checkpoint == 5:
        x = -99
        y = -974
    if checkpoint == 6: #Beneath tower
        x = -65
        y = -901
    if checkpoint == 7:
        x = -38
        y = -833
    if checkpoint == 8: #Beneath tower
        x = -65
        y = -901
    if checkpoint == 9:
        x = -99
        y = -974
    if checkpoint == 10:
        x = -97
        y = -1056
    if checkpoint == 11: #Back to agency
        x = -97
        y = -1500
    if checkpoint == 12:
        x = -55
        y = 39
    if checkpoint == 13:
        x = -72
        y = 42
    if checkpoint == 14: #Into the agency
        x = 0
        y = 0
    if checkpoint == 15:
        x = -36
        y = -21
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
        x = 0
        y = 0
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
    return [x,y]

def calm(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -633
        y = -104
    if checkpoint == 1:
        x = -597
        y = -144
    if checkpoint == 2:
        x = -528
        y = -99
    if checkpoint == 3:
        x = 437
        y = -123
    if checkpoint == 4:
        x = 582
        y = -138
    if checkpoint == 5: #First farm position
        x = 892
        y = -100
    if checkpoint == 6:
        x = 1005
        y = -110
    if checkpoint == 7: #Continue on to the arena
        x = 1362
        y = -152
    if checkpoint == 8:
        x = 1500
        y = -200
    return [x,y]


def besaidFarm(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -345
        y = -470
    if checkpoint == 1: #Map change
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
    if checkpoint == 11: #Map to map
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
    if checkpoint == 16: #Back to previous map
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
    if checkpoint == 25: #Back to beach
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
    return [x,y]

def template(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 0
        y = 0
    if checkpoint == 1:
        x = 0
        y = 0
    if checkpoint == 2:
        x = 0
        y = 0
    if checkpoint == 3:
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
        x = 0
        y = 0
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
    return [x,y]
