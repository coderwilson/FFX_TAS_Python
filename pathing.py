from math import copysign

import memory.main
import xbox

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


def tidus_home(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 181
        y = -1
    if checkpoint == 1:
        x = 146
        y = 1
    if checkpoint == 2:
        x = 115
        y = 1
    if checkpoint == 3:
        x = 60
        y = 6
    if checkpoint == 4:
        x = 28
        y = 5
    if checkpoint == 5:
        print("Talk to the kids")
    if checkpoint == 6:
        x = 13
        y = 3
    if checkpoint == 7:
        x = 10
        y = -5
    if checkpoint == 8:
        print("Talk to the girls")
    if checkpoint == 9:
        x = 6
        y = -1
    if checkpoint == 10:  # Finish the first section
        x = -30
        y = -1
    if checkpoint == 11:  # Start of second section
        x = 426
        y = -3
    if checkpoint == 12:
        x = 426
        y = -3
    if checkpoint == 13:
        x = 426
        y = -3
    if checkpoint == 14:
        x = 426
        y = -3
    if checkpoint == 15:
        x = 426
        y = -3
    if checkpoint == 16:  # Ready for bridge
        x = 426
        y = -3
    if checkpoint == 17:
        x = 147
        y = -30
    if checkpoint == 18:
        x = 54
        y = -33
    if checkpoint == 19:
        x = -62
        y = -62
    if checkpoint == 20:
        x = -200
        y = -100
    if checkpoint == 21:
        x = 0
        y = 880
    if checkpoint == 22:
        x = 0
        y = 830
    if checkpoint == 23:
        x = 0
        y = 700
    if checkpoint == 24:
        x = 2
        y = 838
    if checkpoint == 25:
        x = 14
        y = 940
    if checkpoint == 26:
        x = 32
        y = 1200
    if checkpoint == 27:
        x = 2
        y = 940
    if checkpoint == 28:
        x = 2
        y = 1200
    return [x, y]


def all_starts_here(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 849
        y = -92
    if checkpoint == 1:
        x = 885
        y = -101
    if checkpoint == 2:
        x = 905
        y = -149
    if checkpoint == 3:
        x = 918
        y = -179
    if checkpoint == 4:
        x = 957
        y = -219
    if checkpoint == 5:
        x = 987
        y = -257
    if checkpoint == 6:
        print("Save sphere")
    if checkpoint == 7:
        x = 1003
        y = -253
    if checkpoint == 8:
        x = 1100
        y = -350
    if checkpoint == 9:
        x = 16
        y = -67
    if checkpoint == 10:
        x = 16
        y = -67
    if checkpoint == 11:
        x = 79
        y = -457
    if checkpoint == 12:
        x = 99
        y = -383
    if checkpoint == 13:
        x = 95
        y = -171
    if checkpoint == 14:
        x = 68
        y = 24
    if checkpoint == 15:
        x = 6
        y = 348
    if checkpoint == 16:
        x = -3
        y = 492
    if checkpoint == 17:
        x = -6
        y = 559
    if checkpoint == 18:
        x = -39
        y = 610
    if checkpoint == 19:
        x = -72
        y = 642
    if checkpoint == 20:
        x = -80
        y = 680
    return [x, y]


def baaj_ramp(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 224
        y = -177
    if checkpoint == 1:
        x = 156
        y = -119
    if checkpoint == 2:
        x = 115
        y = -84
    if checkpoint == 3:
        x = 77
        y = -59
    if checkpoint == 4:
        x = -2
        y = -2
    if checkpoint == 5:
        x = -28
        y = 17
    if checkpoint == 7:
        x = -200
        y = 150
    return [x, y]


def baaj_hallway(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -8
        y = 87
    if checkpoint == 1:
        x = 7
        y = 115
    if checkpoint == 2:
        x = 6
        y = 154
    if checkpoint == 3:
        x = 1
        y = 160
    if checkpoint == 4:
        x = -4
        y = 167
    if checkpoint == 5:
        x = 8
        y = 176
    if checkpoint == 6:
        x = 13
        y = 231
    if checkpoint == 7:
        x = 6
        y = 240
    if checkpoint == 8:
        x = -2
        y = 250
    return [x, y]


def baaj_puzzle(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -71
        y = 79
    if checkpoint == 1:
        x = -94
        y = 120
    if checkpoint == 2:
        x = -100
        y = 139
    if checkpoint == 3:
        print("Save sphere")
    if checkpoint == 4:
        x = -113
        y = 119
    if checkpoint == 5:
        print("Through first door")
    if checkpoint == 6:
        print("Flint obtained.")
    if checkpoint == 7:
        print("Back to main room")
    if checkpoint == 8:
        x = -87
        y = 94
    if checkpoint == 9:
        x = -24
        y = -10
    if checkpoint == 10:
        x = 81
        y = -90
    if checkpoint == 11:
        x = 135
        y = -137
    if checkpoint == 12:
        print("Map change towards withered bouquet")
    if checkpoint == 13:
        x = 85
        y = 71
    if checkpoint == 14:
        x = 78
        y = 30
    if checkpoint == 15:
        x = 72
        y = 8
    if checkpoint == 16:
        x = 76
        y = -6
    if checkpoint == 17:
        x = 65
        y = -31
    if checkpoint == 18:
        x = 48
        y = -39
    if checkpoint == 19:
        x = 29
        y = -64
    if checkpoint == 20:
        x = 8
        y = -78
    if checkpoint == 21:
        print("Withered bouquet")
    if checkpoint == 22:
        x = 8
        y = -78
    if checkpoint == 23:
        x = 29
        y = -64
    if checkpoint == 24:
        x = 48
        y = -39
    if checkpoint == 25:
        x = 65
        y = -31
    if checkpoint == 26:
        x = 76
        y = -6
    if checkpoint == 27:
        x = 72
        y = 8
    if checkpoint == 28:
        x = 78
        y = 30
    if checkpoint == 29:
        x = 85
        y = 71
    if checkpoint == 30:
        x = 82
        y = 81
    if checkpoint == 31:
        x = 75
        y = 90
    if checkpoint == 32:
        print("Back to main room")
    return [x, y]


def besaid_1(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -263
        y = -390
    if checkpoint == 1:
        x = -509
        y = -552
    if checkpoint == 2:
        x = 72
        y = -31
    if checkpoint == 3:
        x = 84
        y = -8
    if checkpoint == 4:
        x = 137
        y = 1
    if checkpoint == 5:
        x = 250
        y = 5
    if checkpoint == 6:
        x = -601
        y = -411
    if checkpoint == 7:  # Wakka pushes Tidus
        x = -229
        y = -359
    if checkpoint == 8:
        x = 64
        y = -612
    if checkpoint == 9:
        x = 64
        y = -612
    if checkpoint == 10:
        x = 64
        y = -612
    if checkpoint == 11:
        x = 206
        y = -679
    if checkpoint == 12:
        x = 236
        y = -699
    if checkpoint == 13:
        x = 262
        y = -702
    if checkpoint == 14:
        x = 280
        y = -700
    if checkpoint == 15:
        x = 307
        y = -691
    if checkpoint == 16:
        x = 412
        y = -646
    if checkpoint == 17:
        x = 439
        y = -631
    if checkpoint == 18:
        x = 488
        y = -459
    if checkpoint == 19:  # Pillar, before the big open area.
        x = 498
        y = -414
    if checkpoint == 20:  # Adjust to best trigger for piranhas
        x = 480
        y = -37
    if checkpoint == 21:  # Adjust to best trigger for piranhas
        x = 480
        y = 100
    if checkpoint == 22:  # Hilltop
        x = 73
        y = -49
    if checkpoint == 23:
        x = 0
        y = -182
    if checkpoint == 24:
        x = -10
        y = -226
    if checkpoint == 25:
        x = -9
        y = -270
    if checkpoint == 26:
        x = 20
        y = -374
    if checkpoint == 27:
        x = 82
        y = -534
    if checkpoint == 28:
        x = 75
        y = -700
    if checkpoint == 29:  # Enter Besaid village
        x = -18
        y = 444
    if checkpoint == 30:
        x = -22
        y = 186
    if checkpoint == 31:
        x = -16
        y = 14
    if checkpoint == 32:
        x = -8
        y = -59
    if checkpoint == 33:
        x = -5
        y = -179
    if checkpoint == 34:  # Temple
        print("Temple")
    if checkpoint == 35:
        x = 38
        y = 27
    if checkpoint == 36:
        x = 0
        y = -124
    if checkpoint == 37:
        x = 0
        y = -180
    if checkpoint == 38:
        x = -13
        y = -69
    if checkpoint == 39:
        x = -15
        y = -5
    if checkpoint == 40:
        x = -17
        y = 50
    if checkpoint == 41:
        x = -51
        y = 202
    if checkpoint == 42:
        x = -79
        y = 292
    if checkpoint == 43:  # Into Wakka's tent
        print("Into Wakka's tent")
    if checkpoint == 44:
        print("Sleep tight.")
    if checkpoint == 45:
        print("Exit the tent")
    if checkpoint == 46:
        x = -51
        y = 202
    if checkpoint == 47:
        x = -17
        y = 50
    if checkpoint == 48:
        x = -15
        y = -5
    if checkpoint == 49:
        x = -13
        y = -69
    if checkpoint == 50:
        x = 0
        y = -200
    if checkpoint == 51:  # The Precepts must be obeyed!
        x = 0
        y = 30
    return [x, y]


def besaid_trials(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -30
        y = 126
    if checkpoint == 1:
        print("First glyph")
    if checkpoint == 2:
        x = -11
        y = 116
    if checkpoint == 3:
        print("Second glyph")
    if checkpoint == 4:
        x = 7
        y = 117
    if checkpoint == 5:
        x = 45
        y = 123
    if checkpoint == 6:
        x = 67
        y = 133
    if checkpoint == 7:
        print("Pick up Besaid sphere")
    if checkpoint == 8:
        x = 41
        y = 146
    if checkpoint == 9:
        x = -4
        y = 143
    if checkpoint == 10:
        x = -14
        y = 133
    if checkpoint == 11:
        x = -17
        y = 104
    if checkpoint == 12:
        print("Insert Besaid sphere")
    if checkpoint == 13:
        x = -22
        y = 78
    if checkpoint == 14:
        x = -16
        y = 68
    if checkpoint == 15:
        x = 34
        y = 52
    if checkpoint == 16:
        x = 37
        y = 43
    if checkpoint == 17:
        x = 34
        y = -29
    if checkpoint == 18:
        x = 22
        y = -36
    if checkpoint == 19:
        x = -6
        y = -32
    if checkpoint == 20:
        print("Touch the hidden door glyph")
    if checkpoint == 21:
        x = -17
        y = -24
    if checkpoint == 22:
        x = -15
        y = 17
    if checkpoint == 23:
        print("Besaid sphere")
    if checkpoint == 24:
        x = -14
        y = -26
    if checkpoint == 25:
        x = -10
        y = -50
    if checkpoint == 26:
        print("Insert Besaid sphere, and push to completion")
    if checkpoint == 27:  # Back from the temple
        x = 0
        y = -107
    if checkpoint == 28:
        x = 0
        y = -130
    if checkpoint == 29:
        x = -19
        y = -52
    if checkpoint == 30:
        x = -16
        y = -17
    if checkpoint == 31:
        x = -13
        y = 76
    if checkpoint == 32:  # Approach Valefor's first scene
        x = 0
        y = 200
    if checkpoint == 33:  # Night scene
        x = 15
        y = 194
    if checkpoint == 34:
        print("Talk to Yuna")
    if checkpoint == 35:
        x = -3
        y = 174
    if checkpoint == 36:
        print("Sleep tight")
    if checkpoint == 37:
        x = 340
        y = 15
    if checkpoint == 38:
        x = 343
        y = 105
    if checkpoint == 39:
        print("Dream about girls")
    if checkpoint == 40:  # Ready to leave village.
        x = 7
        y = 24
    if checkpoint == 41:
        x = 4
        y = -46
    if checkpoint == 42:
        x = 0
        y = -200
    return [x, y]


def besaid_2(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        print("Back into the village")
    if checkpoint == 1:
        x = 7
        y = 413
    if checkpoint == 2:
        x = 42
        y = 375
    if checkpoint == 3:
        print("Tent 1")
    if checkpoint == 4:
        x = -2
        y = 5
    if checkpoint == 5:
        print("Shopkeeper")
    if checkpoint == 6:
        x = -2
        y = -18
    if checkpoint == 7:
        print("Exit tent")
    if checkpoint == 8:
        x = -76
        y = 223
    if checkpoint == 9:
        print("Tent 2")
    if checkpoint == 10:
        x = -3
        y = -4
    if checkpoint == 11:
        print("Good doggo")
    if checkpoint == 12:
        x = -4
        y = -19
    if checkpoint == 13:
        print("Exit tent")
    if checkpoint == 14:
        x = -37
        y = 406
    if checkpoint == 15:
        x = -12
        y = 502
    if checkpoint == 16:
        print("Exit the front gates")
    if checkpoint == 17:  # Outside village
        x = 63
        y = -469
    if checkpoint == 18:
        print("First tutorial")
    if checkpoint == 19:
        x = -10
        y = -270
    if checkpoint == 20:
        x = -17
        y = -245
    if checkpoint == 21:
        x = -1
        y = -189
    if checkpoint == 22:
        x = 43
        y = 21
    if checkpoint == 23:
        print("Second tutorial")
    if checkpoint == 24:
        print("Hilltop")
    if checkpoint == 25:
        x = -24
        y = 124
    if checkpoint == 26:
        x = 0
        y = 250
    if checkpoint == 27:
        x = 26
        y = -85
    if checkpoint == 28:
        x = 97
        y = 33
    if checkpoint == 29:
        x = 65
        y = 84
    if checkpoint == 30:
        x = -12
        y = 183
    if checkpoint == 31:
        x = -40
        y = 300
    if checkpoint == 32:  # Waterfalls
        x = -803
        y = 39
    if checkpoint == 33:
        x = -686
        y = 78
    if checkpoint == 34:
        x = -630
        y = 91
    if checkpoint == 35:
        x = -570
        y = 91
    if checkpoint == 36:
        x = -499
        y = 80
    if checkpoint == 37:
        x = -334
        y = 43
    if checkpoint == 38:
        x = -245
        y = 36
    if checkpoint == 39:
        x = -186
        y = 21
    if checkpoint == 40:
        x = -109
        y = -27
    if checkpoint == 41:
        x = -27
        y = -71
    if checkpoint == 42:
        x = 26
        y = -93
    if checkpoint == 43:
        x = 90
        y = -120
    if checkpoint == 44:
        x = 159
        y = -133
    if checkpoint == 45:
        x = 215
        y = -123
    if checkpoint == 46:
        x = 253
        y = -108
    if checkpoint == 47:
        x = 354
        y = -2
    if checkpoint == 48:
        x = 410
        y = 96
    if checkpoint == 49:
        x = 453
        y = 197
    if checkpoint == 50:
        x = 490
        y = 300
    if checkpoint == 51:  # Weird T screen
        x = -23
        y = 48
    if checkpoint == 52:
        x = -19
        y = 29
    if checkpoint == 53:
        x = -40
        y = -9
    if checkpoint == 54:
        x = -31
        y = -17
    if checkpoint == 55:
        x = 14
        y = -4
    if checkpoint == 56:
        x = 43
        y = -31
    if checkpoint == 57:
        x = 56
        y = -44
    if checkpoint == 58:
        x = 80
        y = -150
    if checkpoint == 59:  # Beach
        x = -318
        y = -472
    if checkpoint == 60:  # Save sphere, but no longer used.
        print("Save sphere")
    if checkpoint == 61:
        x = -283
        y = -438
    if checkpoint == 62:
        x = -218
        y = -367
    if checkpoint == 63:
        x = 105
        y = -72
    if checkpoint == 64:
        x = 306
        y = -58
    if checkpoint == 65:
        x = 329
        y = -39
    if checkpoint == 66:
        x = 357
        y = 13
    if checkpoint == 67:
        x = 425
        y = -4
    if checkpoint == 68:
        x = 425
        y = 50
    if checkpoint == 69:
        x = 425
        y = 90
    return [x, y]


def liki(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 5
        y = 176
    if checkpoint == 1:
        print("Group around Yuna")
    if checkpoint == 2:
        x = -22
        y = 90
    if checkpoint == 3:
        print("Talk to Wakka")
    if checkpoint == 4:
        x = -15
        y = 127
    if checkpoint == 5:
        x = 0
        y = 350
    return [x, y]


def kilika_1(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -301
        y = -258
    if checkpoint == 1:
        x = -269
        y = -253
    if checkpoint == 2:
        x = -137
        y = -226
    if checkpoint == 3:
        x = -59
        y = -195
    if checkpoint == 4:
        print("Enter cutscene, Yunas dance")
    if checkpoint == 5:
        x = 80
        y = -22
    if checkpoint == 6:
        print("Yuna dancing, ends in the inn")
    if checkpoint == 7:
        x = 41
        y = 2
    if checkpoint == 8:
        print("Exit the inn")
    if checkpoint == 9:
        x = 27
        y = 114
    if checkpoint == 10:
        x = 86
        y = 96
    if checkpoint == 11:
        x = 86
        y = 31
    if checkpoint == 12:
        print("Back to first map")
    if checkpoint == 13:
        x = -31
        y = -179
    if checkpoint == 14:
        x = -25
        y = -216
    if checkpoint == 15:
        x = -1
        y = -245
    if checkpoint == 16:
        print("Talking to Wakka")
    if checkpoint == 17:
        x = -24
        y = -166
    if checkpoint == 18:
        print("Back towards the inn")
    if checkpoint == 19:
        x = 84
        y = 99
    if checkpoint == 20:
        x = 4
        y = 106
    if checkpoint == 21:
        x = -112
        y = 117
    if checkpoint == 22:
        x = -125
        y = 135
    if checkpoint == 23:
        x = -155
        y = 205
    if checkpoint == 24:
        x = -155
        y = 350
    return [x, y]


def kilika_2(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -77
        y = -475
    if checkpoint == 1:
        x = -83
        y = -427
    if checkpoint == 2:
        x = -101
        y = -417
    if checkpoint == 3:
        x = -146
        y = -413
    if checkpoint == 4:
        x = -179
        y = -417
    if checkpoint == 5:
        x = -212
        y = -416
    if checkpoint == 6:
        x = -221
        y = -406
    if checkpoint == 7:
        x = -222
        y = -362
    if checkpoint == 8:
        x = -224
        y = -336
    if checkpoint == 9:
        print("Wakka Scout")
    if checkpoint == 10:
        x = -216
        y = -330
    if checkpoint == 11:
        x = -216
        y = -316
    if checkpoint == 12:
        x = -206
        y = -305
    if checkpoint == 13:
        x = -204
        y = -293
    if checkpoint == 14:
        x = -215
        y = -275
    if checkpoint == 15:
        x = -226
        y = -250
    if checkpoint == 16:
        x = -234
        y = -226
    if checkpoint == 17:
        x = -241
        y = -206
    if checkpoint == 18:
        x = -241
        y = -135
    if checkpoint == 19:
        x = -242
        y = -124
    if checkpoint == 20:
        x = -249
        y = -101
    if checkpoint == 21:
        x = -241
        y = -84
    if checkpoint == 22:
        x = -242
        y = -57
    if checkpoint == 23:
        x = -240
        y = -35
    if checkpoint == 24:
        x = -244
        y = -20
    if checkpoint == 25:
        x = -251
        y = 3
    if checkpoint == 26:
        x = -264
        y = 25
    if checkpoint == 27:
        x = -259
        y = 37
    if checkpoint == 28:
        x = -248
        y = 53
    if checkpoint == 29:
        x = -237
        y = 58
    if checkpoint == 30:
        x = -225
        y = 68
    if checkpoint == 31:
        x = -217
        y = 71
    if checkpoint == 32:
        x = -206
        y = 61
    if checkpoint == 33:
        x = -185
        y = 72
    if checkpoint == 34:
        x = -166
        y = 51
    if checkpoint == 35:
        x = -144
        y = 64
    if checkpoint == 36:
        x = -100
        y = 65
    if checkpoint == 37:
        x = -86
        y = 96
    if checkpoint == 38:
        x = -85
        y = 124
    if checkpoint == 39:
        x = -100
        y = 176
    if checkpoint == 40:
        x = -122
        y = 211
    if checkpoint == 41:
        x = -134
        y = 210
    if checkpoint == 42:
        x = -167
        y = 210
    if checkpoint == 43:
        x = -178
        y = 201
    if checkpoint == 44:
        x = -196
        y = 212
    if checkpoint == 45:
        x = -217
        y = 210
    if checkpoint == 46:
        x = -241
        y = 208
    if checkpoint == 47:
        print("Picking up chest")
    if checkpoint == 48:
        x = -230
        y = 212
    if checkpoint == 49:
        x = -199
        y = 212
    if checkpoint == 50:
        x = -188
        y = 208
    if checkpoint == 51:
        x = -178
        y = 202
    if checkpoint == 52:
        x = -170
        y = 204
    if checkpoint == 53:
        x = -160
        y = 209
    if checkpoint == 54:
        x = -137
        y = 208
    if checkpoint == 55:
        x = -118
        y = 208
    if checkpoint == 56:
        x = -109
        y = 195
    if checkpoint == 57:
        x = -92
        y = 147
    if checkpoint == 58:
        x = -59
        y = 99
    if checkpoint == 59:
        x = -49
        y = 83
    if checkpoint == 60:
        x = -33
        y = 79
    if checkpoint == 61:
        x = 7
        y = 71
    if checkpoint == 62:
        x = 34
        y = 72
    if checkpoint == 63:
        x = 53
        y = 76
    if checkpoint == 64:
        x = 88
        y = 79
    if checkpoint == 65:
        x = 100
        y = 70
    if checkpoint == 66:
        x = 133
        y = 79
    if checkpoint == 67:
        x = 149
        y = 87
    if checkpoint == 68:
        x = 151
        y = 110
    if checkpoint == 69:
        x = 148
        y = 132
    if checkpoint == 70:
        x = 130
        y = 175
    if checkpoint == 71:
        x = 96
        y = 212
    if checkpoint == 72:
        x = 69
        y = 249
    if checkpoint == 73:
        x = 66
        y = 258
    if checkpoint == 74:
        x = 49
        y = 268
    if checkpoint == 75:
        x = 30
        y = 284
    if checkpoint == 76:
        x = 2
        y = 292
    if checkpoint == 77:
        x = -30
        y = 294
    if checkpoint == 78:
        x = -58
        y = 299
    if checkpoint == 79:
        x = -66
        y = 300
    if checkpoint == 80:
        x = -68
        y = 328
    if checkpoint == 81:
        x = -70
        y = 417
    if checkpoint == 82:
        x = -95
        y = 415
    if checkpoint == 83:  # Into next area
        x = -80
        y = 500
    if checkpoint == 84:
        x = -58
        y = 144
    if checkpoint == 85:
        x = -20
        y = 172
    if checkpoint == 86:  # Stairs save sphere
        print("Stairs")
    if checkpoint == 87:
        x = -10
        y = 192
    if checkpoint == 88:
        x = 17
        y = 233
    if checkpoint == 89:
        x = 13
        y = 286
    if checkpoint == 90:
        x = -51
        y = 609
    if checkpoint == 91:
        x = -99
        y = 656
    if checkpoint == 92:
        x = -129
        y = 685
    if checkpoint == 93:
        x = -160
        y = 740
    if checkpoint == 94:
        x = 2
        y = 270
    if checkpoint == 95:  # Into the temple
        x = 2
        y = 500
    if checkpoint == 96:
        x = -1
        y = -56
    if checkpoint == 97:  # non-CSR, slight left
        x = -22
        y = 6
    if checkpoint == 98:  # non-CSR, past Lulu
        x = -30
        y = 33
    if checkpoint == 99:  # non-CSR, pray to O'holland
        print("non-CSR, pray to O'holland")
    if checkpoint == 100:
        x = 2
        y = 54
    return [x, y]


def kilika_trials(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -6
        y = -247
    if checkpoint == 1:
        x = -17
        y = -215
    if checkpoint == 2:
        print("Pick up Kilika sphere")
    if checkpoint == 3:
        x = -10
        y = -205
    if checkpoint == 4:
        x = 8
        y = -188
    if checkpoint == 5:
        print("Insert and remove, opens door")
    if checkpoint == 6:
        x = 5
        y = -181
    if checkpoint == 7:
        x = 1
        y = -176
    if checkpoint == 8:
        x = 0
        y = 11
    if checkpoint == 9:
        print("Insert and remove, generate glyph")
    if checkpoint == 10:
        x = 37
        y = -18
    if checkpoint == 11:
        print("Insert, out of the way")
    if checkpoint == 12:
        x = 1
        y = 11
    if checkpoint == 13:
        print("Touch glyph")
    if checkpoint == 14:
        x = 1
        y = 34
    if checkpoint == 15:
        x = 8
        y = 133
    if checkpoint == 16:
        x = 30
        y = 165
    if checkpoint == 17:
        x = 52
        y = 167
    if checkpoint == 18:
        print("Remove Kilika sphere")
    if checkpoint == 19:
        x = 52
        y = 167
    if checkpoint == 20:
        x = 30
        y = 165
    if checkpoint == 21:
        x = 8
        y = 133
    if checkpoint == 22:
        x = 1
        y = 34
    if checkpoint == 23:
        x = -2
        y = 15
    if checkpoint == 24:
        x = -37
        y = -8
    if checkpoint == 25:
        print("Insert Kilika sphere")
    if checkpoint == 26:
        x = -24
        y = -25
    if checkpoint == 27:
        print("Pick up Glyph sphere")
    if checkpoint == 28:
        x = -2
        y = 15
    if checkpoint == 29:
        x = 1
        y = 34
    if checkpoint == 30:
        x = 8
        y = 133
    if checkpoint == 31:
        x = 30
        y = 165
    if checkpoint == 32:
        x = 52
        y = 167
    if checkpoint == 33:
        print("Insert Glyph sphere")
    if checkpoint == 34:
        x = 30
        y = 165
    if checkpoint == 35:
        x = 8
        y = 133
    if checkpoint == 36:
        x = 1
        y = 34
    if checkpoint == 37:
        x = 1
        y = 15
    if checkpoint == 38:
        x = 36
        y = -18
    if checkpoint == 39:
        print("Pick up last Kilika sphere")
    if checkpoint == 40:
        x = 1
        y = 15
    if checkpoint == 41:
        x = 1
        y = 34
    if checkpoint == 42:
        x = -9
        y = 133
    if checkpoint == 43:
        x = -29
        y = 163
    if checkpoint == 44:
        x = -36
        y = 177
    if checkpoint == 45:
        x = -38
        y = 207
    if checkpoint == 46:
        x = 31
        y = 225
    if checkpoint == 47:
        x = 37
        y = 232
    if checkpoint == 48:
        x = 35
        y = 270
    if checkpoint == 49:
        x = 17
        y = 275
    if checkpoint == 50:
        print("Insert and remove, opens door")
    if checkpoint == 51:
        x = 5
        y = 278
    if checkpoint == 52:
        x = 0
        y = 400
    if checkpoint == 53:  # Inner sanctum
        x = -13
        y = -10
    if checkpoint == 54:  # Talk to Wakka
        print("Talk to Wakka")
    if checkpoint == 55:
        x = -6
        y = -20
    return [x, y]


def kilika_3(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -68
        y = 314
    if checkpoint == 1:
        x = -65
        y = 299
    if checkpoint == 2:
        x = -33
        y = 289
    if checkpoint == 3:
        x = 26
        y = 284
    if checkpoint == 4:
        x = 38
        y = 278
    if checkpoint == 5:
        x = 64
        y = 258
    if checkpoint == 6:
        x = 78
        y = 242
    if checkpoint == 7:
        x = 101
        y = 211
    if checkpoint == 8:
        x = 126
        y = 178
    if checkpoint == 9:
        x = 149
        y = 138
    if checkpoint == 10:
        x = 153
        y = 107
    if checkpoint == 11:
        x = 148
        y = 81
    if checkpoint == 12:
        x = 120
        y = 72
    if checkpoint == 13:
        x = 89
        y = 77
    if checkpoint == 14:
        x = 70
        y = 75
    if checkpoint == 15:
        x = 28
        y = 70
    if checkpoint == 16:
        x = -38
        y = 80
    if checkpoint == 17:
        x = -112
        y = 59
    if checkpoint == 18:
        x = -150
        y = 58
    if checkpoint == 19:
        x = -184
        y = 71
    if checkpoint == 20:
        x = -207
        y = 64
    if checkpoint == 21:
        x = -228
        y = 63
    if checkpoint == 22:
        x = -245
        y = 52
    if checkpoint == 23:
        x = -254
        y = 45
    if checkpoint == 24:
        x = -256
        y = 36
    if checkpoint == 25:
        x = -259
        y = 25
    if checkpoint == 26:
        x = -256
        y = 14
    if checkpoint == 27:
        x = -246
        y = -10
    if checkpoint == 28:
        x = -244
        y = -25
    if checkpoint == 29:
        x = -240
        y = -39
    if checkpoint == 30:
        x = -242
        y = -54
    if checkpoint == 31:  # Before crossing log, between two trees.
        x = -241
        y = -80
    if checkpoint == 32:  # Right before stepping on the log
        x = -246
        y = -122
    if checkpoint == 33:
        x = -241
        y = -144
    if checkpoint == 34:
        x = -244
        y = -204
    if checkpoint == 35:
        x = -236
        y = -233
    if checkpoint == 36:
        x = -229
        y = -249
    if checkpoint == 37:
        x = -220
        y = -263
    if checkpoint == 38:
        x = -207
        y = -289
    if checkpoint == 39:
        x = -206
        y = -298
    if checkpoint == 40:
        x = -214
        y = -323
    if checkpoint == 41:
        x = -218
        y = -338
    if checkpoint == 42:
        x = -226
        y = -342
    if checkpoint == 43:
        x = -225
        y = -356
    if checkpoint == 44:
        x = -223
        y = -388
    if checkpoint == 45:
        x = -218
        y = -411
    if checkpoint == 46:
        x = -209
        y = -417
    if checkpoint == 47:
        x = -174
        y = -417
    if checkpoint == 48:
        x = -104
        y = -418
    if checkpoint == 49:
        x = -84
        y = -430
    if checkpoint == 50:
        x = -78
        y = -452
    if checkpoint == 51:
        x = -85
        y = -525
    if checkpoint == 52:  # Back to the docks
        x = -70
        y = -600
    if checkpoint == 53:
        x = -150
        y = 200
    if checkpoint == 54:
        x = -126
        y = 149
    if checkpoint == 55:
        x = -121
        y = 127
    if checkpoint == 56:
        x = -111
        y = 109
    if checkpoint == 57:
        x = -59
        y = 108
    if checkpoint == 58:
        x = -6
        y = 110
    if checkpoint == 59:
        x = 41
        y = 102
    if checkpoint == 60:
        x = 80
        y = 99
    if checkpoint == 61:
        x = 87
        y = 89
    if checkpoint == 62:
        x = 88
        y = 43
    if checkpoint == 63:
        x = 88
        y = -100
    if checkpoint == 64:
        x = -48
        y = -184
    if checkpoint == 65:
        x = -56
        y = -194
    if checkpoint == 66:
        x = -84
        y = -213
    if checkpoint == 67:  # Just before the boat, after the hammer guy
        x = -161
        y = -241
    return [x, y]


def winno(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 11
        y = 61
    if checkpoint == 1:
        x = 11
        y = 150
    if checkpoint == 2:
        x = -34
        y = -50
    if checkpoint == 3:
        x = -42
        y = -59
    if checkpoint == 4:
        x = -35
        y = -66
    if checkpoint == 5:
        x = -26
        y = -67
    if checkpoint == 6:  # Start Lulu/Wakka conversation
        x = 0
        y = 0
    if checkpoint == 7:
        x = -43
        y = -17
    if checkpoint == 8:
        x = -34
        y = 12
    if checkpoint == 9:
        x = -23
        y = 85
    if checkpoint == 10:
        x = 0
        y = 152
    if checkpoint == 11:
        x = 0
        y = 152
    if checkpoint == 12:
        x = 22
        y = 104
    return [x, y]


def luca_1(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 126
        y = 381
    if checkpoint == 1:
        x = 130
        y = 362
    if checkpoint == 2:
        x = 157
        y = 302
    if checkpoint == 3:
        x = 189
        y = 285
    if checkpoint == 4:  # Map to map
        x = 230
        y = 250
    if checkpoint == 5:  # Just before Seymour gets introduced
        x = 328
        y = 63
    if checkpoint == 6:  # Seymour intro scene
        print("Seymour intro scene")
    if checkpoint == 7:
        x = 0
        y = -200
    if checkpoint == 8:  # buffer
        x = 0
        y = -200
    if checkpoint == 9:  # buffer
        x = 0
        y = -200
    if checkpoint == 10:  # Luca stadium front
        x = -256
        y = -76
    if checkpoint == 11:
        x = -600
        y = -19
    if checkpoint == 12:  # Reverse T map
        x = 187
        y = 18
    if checkpoint == 13:  # Reverse T map - into next zone
        x = 300
        y = 10
    if checkpoint == 14:
        x = 28
        y = -60
    if checkpoint == 15:
        x = 39
        y = -52
    if checkpoint == 16:
        x = 53
        y = -36
    if checkpoint == 17:
        x = 61
        y = -8
    if checkpoint == 18:
        x = 60
        y = 29
    if checkpoint == 19:
        x = 21
        y = 90
    if checkpoint == 20:
        x = 4
        y = 131
    if checkpoint == 21:
        x = -1
        y = 161
    if checkpoint == 22:
        x = -1
        y = 161
    if checkpoint == 23:  # Into the bar
        print("Into the bar")
    if checkpoint == 24:  # buffer
        x = 37
        y = -26
    if checkpoint == 25:  # buffer
        x = 37
        y = -26
    if checkpoint == 26:  # buffer
        x = 37
        y = -26
    if checkpoint == 27:  # buffer
        x = 37
        y = -26
    if checkpoint == 28:
        x = 37
        y = -26
    if checkpoint == 29:
        x = -4
        y = -30
    if checkpoint == 30:
        x = -60
        y = -19
    if checkpoint == 31:
        x = -149
        y = -12
    if checkpoint == 32:
        x = -257
        y = 10
    if checkpoint == 33:
        print("Back to the front of the Blitz dome")
    if checkpoint == 34:
        x = -395
        y = 38
    if checkpoint == 35:
        x = -320
        y = 95
    if checkpoint == 36:
        print("To the docks")
    if checkpoint == 37:
        x = -239
        y = 160
    if checkpoint == 38:
        x = -224
        y = 178
    if checkpoint == 39:
        x = -195
        y = 203
    if checkpoint == 40:  # First battle
        print("First battle")
    if checkpoint == 41:
        x = 185
        y = 240
    if checkpoint == 42:  # Second battle
        print("Second battle")
    if checkpoint == 43:
        x = 281
        y = -75
    if checkpoint == 44:  # Third battle
        print("Third battle")
    if checkpoint == 45:
        x = 167
        y = -312
    if checkpoint == 46:
        print("Touch save sphere")
    if checkpoint == 47:
        x = 150
        y = -337
    if checkpoint == 48:  # Start of Oblitzerator fight
        print("Start of Oblitzerator fight")
    if checkpoint == 49:
        x = -8
        y = -311
    if checkpoint == 50:
        print("Screen change")
    if checkpoint == 51:
        x = -304
        y = -53
    if checkpoint == 52:
        print("Screen change")
    if checkpoint == 53:
        x = -293
        y = -87
    if checkpoint == 54:
        x = -275
        y = -50
    if checkpoint == 55:  # Save sphere and end of section
        print("Save sphere and end of section")
    return [x, y]


def luca_pre_blitz(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -270
        y = -56
    if checkpoint == 1:
        x = -173
        y = -67
    if checkpoint == 2:
        x = 20
        y = -67
    if checkpoint == 3:
        x = -4
        y = -11
    if checkpoint == 4:
        x = -16
        y = -1
    if checkpoint == 5:
        x = -61
        y = -9
    if checkpoint == 6:
        x = -75
        y = -19
    if checkpoint == 7:
        x = -108
        y = -10
    return [x, y]


def luca_3(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -549
        y = -373
    if checkpoint == 1:
        x = -573
        y = -384
    if checkpoint == 2:
        x = -582
        y = -378
    if checkpoint == 3:
        x = -596
        y = -361
    if checkpoint == 4:
        x = -612
        y = -363
    if checkpoint == 5:
        x = -636
        y = -381
    if checkpoint == 6:
        x = -638
        y = -397
    if checkpoint == 7:
        x = -632
        y = -403
    if checkpoint == 6:  # First chest
        print("First chest")
    if checkpoint == 9:
        x = -621
        y = -417
    if checkpoint == 10:  # Second chest
        print("Second chest")
    if checkpoint == 11:
        x = -627
        y = -404
    if checkpoint == 12:
        x = -637
        y = -397
    if checkpoint == 13:
        x = -640
        y = -382
    if checkpoint == 14:
        x = -602
        y = -362
    if checkpoint == 15:
        x = -591
        y = -364
    if checkpoint == 16:
        x = -577
        y = -382
    if checkpoint == 17:
        x = -563
        y = -380
    if checkpoint == 18:
        x = -431
        y = -275
    if checkpoint == 19:
        x = -316
        y = -144
    if checkpoint == 20:  # Target Auron
        print("Target Auron")
    if checkpoint == 21:
        x = -294
        y = -42
    if checkpoint == 22:  # Into registration map
        x = -220
        y = -10
    if checkpoint == 23:
        x = -347
        y = -63
    if checkpoint == 24:
        x = -407
        y = -32
    if checkpoint == 25:
        x = -500
        y = -32
    if checkpoint == 26:  # Upside down T map
        x = -63
        y = -18
    if checkpoint == 27:
        x = -1
        y = -32
    if checkpoint == 28:
        x = 38
        y = -22
    if checkpoint == 29:
        x = 164
        y = -4
    if checkpoint == 30:
        x = 300
        y = 0
    if checkpoint == 31:  # Carnival screen
        x = 29
        y = -87
    if checkpoint == 32:
        x = 65
        y = -32
    if checkpoint == 33:
        x = 90
        y = 61
    if checkpoint == 34:
        x = 140
        y = 92
    if checkpoint == 35:  # Bring the party together
        print("Bring the party together")
    return [x, y]


def miihen(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -15
        y = 203
    if checkpoint == 1:
        x = -44
        y = 419
    if checkpoint == 2:
        x = -49
        y = 496
    if checkpoint == 3:
        x = -39
        y = 538
    if checkpoint == 4:
        x = -10
        y = 900
    if checkpoint == 5:
        x = -47
        y = 1351
    if checkpoint in [6, 7, 8, 9, 10]:
        print("Attempting Mi'ihen skip")
    if checkpoint == 11:
        x = 17
        y = 1536
    if checkpoint == 12:
        x = 24
        y = 1601
    if checkpoint == 13:
        x = 0
        y = 1796
    if checkpoint == 14:
        x = 0
        y = 2200
    if checkpoint == 15:
        x = -12
        y = 629
    if checkpoint == 16:
        x = 0
        y = 895
    if checkpoint == 17:
        x = -9
        y = 1222
    if checkpoint == 18:
        x = 0
        y = 1417
    if checkpoint == 19:
        x = 0
        y = 2000
    if checkpoint == 20:
        x = -22
        y = 774
    if checkpoint == 21:
        x = -3
        y = 1155
    if checkpoint == 22:
        x = -11
        y = 1621
    if checkpoint == 23:
        x = -8
        y = 2078
    if checkpoint == 24:
        x = 5
        y = 2369
    if checkpoint == 25:
        x = 0
        y = 2682
    if checkpoint == 26:
        x = -22
        y = 2783
    if checkpoint == 27:  # Shelinda
        print("Shelinda")
    if checkpoint == 28:
        x = 5
        y = 2982
    if checkpoint == 29:
        x = 2
        y = 3088
    if checkpoint == 30:
        x = 0
        y = 3500
    if checkpoint == 31:
        x = 0
        y = -227
    return [x, y]


def miihen_agency(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 26
        y = -23
    if checkpoint == 1:
        x = 15
        y = -30
    if checkpoint == 2:  # Go for P.downs if less than 10.
        x = -2
        y = -27
    if checkpoint == 3:  # Talk to lady and purchase downs.
        x = -2
        y = -27
    if checkpoint == 4:
        x = -2
        y = -56
    if checkpoint == 5:
        x = -10
        y = -90
    return [x, y]


def low_road(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 35
        y = -932
    if checkpoint == 1:
        x = 43
        y = -919
    if checkpoint == 2:
        print("Touching save sphere")
    if checkpoint == 3:
        x = 37
        y = -903
    if checkpoint == 4:
        x = 69
        y = -805
    if checkpoint == 5:
        x = 85
        y = -742
    if checkpoint == 6:
        x = 142
        y = -616
    if checkpoint == 7:
        x = 175
        y = -515
    if checkpoint == 8:
        x = 190
        y = -417
    if checkpoint == 9:
        x = 174
        y = -355
    if checkpoint == 10:
        x = 62
        y = -244
    if checkpoint == 11:
        x = 19
        y = -178
    if checkpoint == 12:
        x = 17
        y = -153
    if checkpoint == 13:
        x = 17
        y = -16
    if checkpoint == 14:
        x = 39
        y = 33
    if checkpoint == 15:
        x = 59
        y = 59
    if checkpoint == 16:
        x = 100
        y = 100
    if checkpoint == 17:  # Second low road map
        x = 357
        y = 120
    if checkpoint == 18:
        x = 403
        y = 129
    if checkpoint == 19:
        x = 467
        y = 152
    if checkpoint == 20:
        x = 537
        y = 176
    if checkpoint == 21:
        x = 586
        y = 212
    if checkpoint == 22:
        x = 638
        y = 258
    if checkpoint == 23:
        x = 679
        y = 299
    if checkpoint == 24:
        x = 715
        y = 378
    if checkpoint == 25:  # Last checkpoint before reviewing for Self Destruct
        x = 732
        y = 448
    if checkpoint == 26:
        x = 738
        y = 481
    if checkpoint == 27:
        x = 780
        y = 530
    if checkpoint == 28:  # Final map, meeting Seymour
        x = 158
        y = -209
    if checkpoint == 29:
        x = 59
        y = -104
    if checkpoint == 30:
        x = 9
        y = -44
    if checkpoint == 31:
        x = -41
        y = 36
    if checkpoint == 32:
        x = -42
        y = 152
    if checkpoint == 33:
        x = -57
        y = 288
    if checkpoint == 34:
        print("Talk to the guard")
    if checkpoint == 35:
        x = -57
        y = 288
    if checkpoint == 36:
        x = -50
        y = 400
    return [x, y]


def mrr_start(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -40
        y = -667
    if checkpoint == 1:
        x = -58
        y = -614
    if checkpoint == 2:
        x = -62
        y = -616
    if checkpoint == 3:
        print("Attempt skip")
    if checkpoint == 4:
        x = -21
        y = -593
    if checkpoint == 5:
        x = -30
        y = -530
    if checkpoint == 6:
        x = -59
        y = -498
    if checkpoint == 7:
        x = -80
        y = -488
    if checkpoint == 8:
        x = -115
        y = -488
    if checkpoint == 9:
        x = -206
        y = -418
    if checkpoint == 10:
        x = -206
        y = -300
    return [x, y]


def mrr_main(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 12
        y = -738
    if checkpoint == 1:
        print("Touching save sphere")
    if checkpoint == 2:
        x = -28
        y = -663
    if checkpoint == 3:
        x = -37
        y = -601
    if checkpoint == 4:
        print("Up the first lift")
    if checkpoint == 5:
        x = -48
        y = -571
    if checkpoint == 6:
        x = -108
        y = -463
    if checkpoint == 7:
        x = -108
        y = -428
    if checkpoint == 8:
        x = -85
        y = -391
    if checkpoint == 9:
        x = -87
        y = -372
    if checkpoint == 10:
        x = -78
        y = -361
    if checkpoint == 11:
        x = -38
        y = -367
    if checkpoint == 12:
        x = -6
        y = -381
    if checkpoint == 13:
        x = 38
        y = -414
    if checkpoint == 14:
        x = 63
        y = -398
    if checkpoint == 15:
        x = 109
        y = -339
    if checkpoint == 16:
        x = 127
        y = -198
    if checkpoint == 17:
        x = 122
        y = -166
    if checkpoint == 18:
        x = 91
        y = -176
    if checkpoint == 19:
        x = 0
        y = -215
    if checkpoint == 20:
        x = -63
        y = -189
    if checkpoint == 21:
        x = -88
        y = -141
    if checkpoint == 22:
        x = -104
        y = 54
    if checkpoint == 23:
        x = -102
        y = 73
    if checkpoint == 24:
        x = -86
        y = 87
    if checkpoint == 25:
        x = 25
        y = 138
    if checkpoint == 26:
        x = 32
        y = 151
    if checkpoint == 27:
        x = 23
        y = 233
    if checkpoint == 28:
        x = -89
        y = 295
    if checkpoint == 29:
        x = -91
        y = 321
    if checkpoint == 30:
        x = -87
        y = 368
    if checkpoint == 31:
        x = -68
        y = 402
    if checkpoint == 32:
        x = -48
        y = 425
    if checkpoint == 33:
        x = 35
        y = 461
    if checkpoint == 34:
        x = 92
        y = 515
    if checkpoint == 35:
        x = 51
        y = 543
    if checkpoint == 36:
        x = -20
        y = 568
    if checkpoint == 37:
        x = -71
        y = 593
    if checkpoint == 38:
        x = -109
        y = 604
    if checkpoint == 39:
        x = -115
        y = 687
    if checkpoint == 40:
        x = -71
        y = 775
    if checkpoint == 41:
        x = -39
        y = 829
    if checkpoint == 42:
        x = -12
        y = 838
    if checkpoint == 43:
        x = 26
        y = 828
    if checkpoint == 44:
        x = 44
        y = 834
    if checkpoint == 45:
        x = 59
        y = 898
    if checkpoint == 46:
        print("Up the second lift")
    if checkpoint == 47:
        x = -36
        y = -194
    if checkpoint == 48:
        print("Grabbing X-potion from the dude")
    if checkpoint == 49:
        x = 24
        y = -157
    if checkpoint == 50:
        x = 52
        y = -135
    if checkpoint == 51:
        x = 116
        y = 4
    if checkpoint == 52:
        x = 121
        y = 50
    if checkpoint == 53:
        x = 112
        y = 100
    if checkpoint == 54:  # Lining up with the guy for 400 gil
        x = 61
        y = 140
    if checkpoint == 55:
        x = 29
        y = 154
    if checkpoint == 56:
        x = -21
        y = 223
    if checkpoint == 57:
        x = 29
        y = 227
    if checkpoint == 58:
        print("Up the third lift")
    if checkpoint == 59:
        x = 59
        y = 244
    if checkpoint == 60:
        x = 99
        y = 254
    if checkpoint == 61:
        x = 198
        y = 251
    if checkpoint == 62:
        x = 219
        y = 202
    if checkpoint == 63:  # Diagonal towards the save sphere
        x = 226
        y = 170
    if checkpoint == 64:
        x = 248
        y = 169
    if checkpoint == 65:
        x = 271
        y = 183
    if checkpoint == 66:
        print("Up the final lift.")
    if checkpoint == 67:
        x = 304
        y = 186
    if checkpoint == 68:
        x = 327
        y = 185
    if checkpoint == 69:
        x = 341
        y = 172
    if checkpoint == 70:
        x = 450
        y = 160
    if checkpoint == 71:  # Into Battle Site zone (upper, cannon area)
        x = 47
        y = 513
    if checkpoint == 72:
        x = 70
        y = 606
    if checkpoint == 73:
        x = 84
        y = 629
    if checkpoint == 74:
        x = 70
        y = 707
    if checkpoint == 75:
        x = -67
        y = 830
    if checkpoint == 90:
        x = 204
        y = 136
    if checkpoint == 99:
        x = 77
        y = 872
    return [x, y]


def battle_site(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -430
        y = 3274
    if checkpoint == 1:
        x = -258
        y = 3227
    if checkpoint == 2:
        x = -207
        y = 3230
    if checkpoint == 3:
        x = -115
        y = 3330
    if checkpoint == 4:
        x = -52
        y = 3414
    if checkpoint == 5:
        print("O'aka menu")
    if checkpoint == 6:
        x = -68
        y = 3354
    if checkpoint == 7:
        x = -59
        y = 3345
    if checkpoint == 8:
        print("Touching save sphere")
    if checkpoint == 9:
        x = -71
        y = 3324
    if checkpoint == 10:
        x = -45
        y = 3296
    if checkpoint == 11:
        x = -16
        y = 3276
    if checkpoint == 12:
        print("Into the scene with Kinoc")
    if checkpoint == 13:
        x = 217
        y = 3134
    if checkpoint == 14:
        print("Start of fight, Sinspawn Gui")
    return [x, y]


def battle_site_aftermath(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 148
        y = 2836
    if checkpoint == 1:
        x = 75
        y = 2992
    if checkpoint == 2:  # Clasko position
        x = 50
        y = 3092
    if checkpoint == 4:
        x = 609
        y = -175
    if checkpoint == 5:
        x = 548
        y = -159
    if checkpoint == 6:
        x = 417
        y = -160
    if checkpoint == 7:
        print("Start conversation with Auron")
    if checkpoint == 8:
        x = 428
        y = -116
    if checkpoint == 9:
        x = 501
        y = 40
    if checkpoint == 10:
        x = 520
        y = 40
    if checkpoint == 11:
        x = 671
        y = 47
    if checkpoint == 12:
        x = 830
        y = 39
    if checkpoint == 13:
        x = 941
        y = 59
    if checkpoint == 14:
        x = 978
        y = 77
    if checkpoint == 15:
        print("Towards Djose section.")
    return [x, y]


def djose_path(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -237
        y = -672
    if checkpoint == 1:
        x = -191
        y = -450
    if checkpoint == 2:
        x = -152
        y = -279
    if checkpoint == 3:
        x = -126
        y = -166
    if checkpoint == 4:
        x = -126
        y = -166
    if checkpoint == 5:
        x = -126
        y = -166
    if checkpoint == 6:
        x = -126
        y = -166
    if checkpoint == 7:
        x = -126
        y = -166
    if checkpoint == 8:
        x = -126
        y = -166
    if checkpoint == 9:
        x = -126
        y = -166
    if checkpoint == 10:
        x = -126
        y = -166
    if checkpoint == 11:
        x = -126
        y = -166
    if checkpoint == 12:
        x = -126
        y = -166
    if checkpoint == 13:
        x = -126
        y = -166
    if checkpoint == 14:
        x = -60
        y = 32
    if checkpoint == 15:
        x = -60
        y = 32
    if checkpoint == 16:
        x = -60
        y = 32
    if checkpoint == 17:
        x = -60
        y = 32
    if checkpoint == 18:
        x = -60
        y = 32
    if checkpoint == 19:
        x = -60
        y = 32
    if checkpoint == 20:
        x = -60
        y = 32
    if checkpoint == 21:
        x = -34
        y = 92
    if checkpoint == 22:
        x = -34
        y = 92
    if checkpoint == 23:
        x = -34
        y = 92
    if checkpoint == 24:
        x = -33
        y = 118
    if checkpoint == 25:
        x = 27
        y = 215
    if checkpoint == 26:
        x = 38
        y = 232
    if checkpoint == 27:
        x = 56
        y = 260
    if checkpoint == 28:
        x = 94
        y = 321
    if checkpoint == 29:
        x = 111
        y = 349
    if checkpoint == 30:
        x = 123
        y = 368
    if checkpoint == 31:
        x = 137
        y = 390
    if checkpoint == 32:
        x = 157
        y = 422
    if checkpoint == 33:
        x = 177
        y = 453
    if checkpoint == 34:
        x = 213
        y = 506
    if checkpoint == 35:
        x = 234
        y = 521
    if checkpoint == 36:
        x = 266
        y = 543
    if checkpoint == 37:
        x = 329
        y = 587
    if checkpoint == 38:
        x = 337
        y = 593
    if checkpoint == 39:
        x = 375
        y = 619
    if checkpoint == 40:
        x = 440
        y = 650
    if checkpoint == 41:
        x = 447
        y = 651
    if checkpoint in [42, 43, 44, 45, 46]:
        x = 461.5
        y = 658
    if checkpoint == 47:  # Point of deferral 1
        x = 550
        y = 730
    if checkpoint == 48:  # Point of deferral 2
        x = 489
        y = 730
    if checkpoint == 49:  # Point of continuation
        x = 604
        y = 836
    if checkpoint == 50:
        x = 734
        y = 859
    if checkpoint == 51:  # Transition to next map
        x = 0
        y = 0
    if checkpoint == 52:
        x = 27
        y = -231
    if checkpoint == 53:
        x = 59
        y = -14
    if checkpoint == 54:
        x = 51
        y = 0
    if checkpoint == 55:
        x = 9
        y = 151
    if checkpoint == 56:  # Transition to temple map
        x = 0
        y = 0
    if checkpoint == 57:
        x = -4
        y = -87
    if checkpoint == 58:  # Transition into temple
        x = 0
        y = 0
    return [x, y]


def djose_trials(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -22
        y = -233
    if checkpoint == 1:
        print("First sphere")
    if checkpoint == 2:
        x = -6
        y = -193
    if checkpoint == 3:
        print("Sphere door")
    if checkpoint == 4:
        x = 24
        y = -208
    if checkpoint == 5:
        print("Second sphere")
    if checkpoint == 6:
        x = 6
        y = -191
    if checkpoint == 7:
        print("Sphere door")
    if checkpoint == 8:
        x = 0
        y = -176
    if checkpoint == 9:
        x = 0
        y = -58
    if checkpoint == 10:
        x = -3
        y = -7
    if checkpoint == 11:
        x = -8
        y = 18
    if checkpoint == 12:
        x = -19
        y = 42
    if checkpoint == 13:
        print("Left sphere")
    if checkpoint == 14:
        x = 34
        y = 31
    if checkpoint == 15:
        x = 69
        y = 34
    if checkpoint == 16:
        print("Insert left sphere")
    if checkpoint == 17:
        x = 31
        y = 30
    if checkpoint == 18:
        x = 23
        y = 43
    if checkpoint == 19:
        print("Right sphere")
    if checkpoint == 20:
        x = -18
        y = 22
    if checkpoint == 21:
        x = -7
        y = 24
    if checkpoint == 22:
        print("Pushing pedestal")
    if checkpoint == 23:
        x = 56
        y = 33
    if checkpoint == 24:
        print("Insert right sphere")
    if checkpoint == 25:
        print("Unused")
    if checkpoint == 26:
        print("Unused")
    if checkpoint == 27:
        x = 57
        y = 34
    if checkpoint == 28:
        print("Left sphere")
    if checkpoint == 29:
        x = 14
        y = 27
    if checkpoint == 30:
        x = -65
        y = 24
    if checkpoint == 31:
        print("Reset switch")
    if checkpoint == 32:
        x = -41
        y = 24
    if checkpoint == 33:
        x = -10
        y = 22
    if checkpoint == 34:
        print("Insert left sphere")
    if checkpoint == 35:
        x = -4
        y = 10
    if checkpoint == 36:
        x = 9
        y = 15
    if checkpoint == 37:
        x = 12
        y = 22
    if checkpoint == 38:
        print("Powered sphere")
    if checkpoint == 39:
        x = 22
        y = 39
    if checkpoint == 40:
        print("Insert powered sphere")
    if checkpoint == 41:
        x = 32
        y = 31
    if checkpoint == 42:
        x = 66
        y = 28
    if checkpoint == 43:
        print("Right sphere")
    if checkpoint == 44:
        x = 8
        y = 24
    if checkpoint == 45:
        print("Insert right sphere")
    if checkpoint == 46:
        x = 8
        y = 13
    if checkpoint == 47:
        x = 0
        y = 16
    if checkpoint == 48:
        print("All the hidden room stuff.")
    if checkpoint == 49:
        x = 2
        y = 47
    if checkpoint == 50:
        x = 20
        y = 47
    if checkpoint == 51:
        print("Powered sphere")
    if checkpoint == 52:
        x = -19
        y = 46
    if checkpoint == 53:
        print("Insert powered sphere")
    if checkpoint == 54:
        x = -14
        y = 24
    if checkpoint == 55:
        x = -65
        y = 24
    if checkpoint == 56:
        print("Reset switch")
    if checkpoint == 57:
        x = -9
        y = 22
    if checkpoint == 58:
        print("Left sphere")
    if checkpoint == 59:
        x = -2
        y = 1
    if checkpoint == 60:
        x = -2
        y = -53
    if checkpoint == 61:
        x = -2
        y = -191
    if checkpoint == 62:
        x = -26
        y = -216
    if checkpoint == 63:
        print("Final insert Left sphere")
    if checkpoint == 64:
        x = -1
        y = -185
    if checkpoint == 65:
        x = 3
        y = -9
    if checkpoint == 66:
        x = 6
        y = 5
    if checkpoint == 67:
        x = 9
        y = 19  # Dial in
    if checkpoint == 68:
        print("Right sphere")
    if checkpoint == 69:
        x = 6
        y = 5
    if checkpoint == 70:
        x = 3
        y = -9
    if checkpoint == 71:
        x = 3
        y = -185
    if checkpoint == 72:
        x = 26
        y = -214
    if checkpoint == 73:
        print("Final insert Right sphere")
    if checkpoint == 74:
        x = 3
        y = -185
    if checkpoint == 75:
        x = -3
        y = -8
    if checkpoint == 76:
        x = -3
        y = 0
    if checkpoint == 77:
        x = -4
        y = 4
    if checkpoint == 78:
        x = -37
        y = 26
    if checkpoint == 79:
        x = -54
        y = 25
    if checkpoint == 80:  # Destro glyph
        print("Destruction Glyph")
    if checkpoint == 81:
        x = -62
        y = 55
    if checkpoint == 82:
        print("Destruction Sphere")
    if checkpoint == 83:
        x = -58
        y = 28
    if checkpoint == 84:
        x = -11
        y = 28
    if checkpoint == 85:
        print("Ride ze lift")
    if checkpoint == 86:
        x = -11
        y = 110
    if checkpoint == 87:
        x = -21
        y = 115
    if checkpoint == 88:
        print("Pedestal 1")
    if checkpoint == 89:
        x = -22
        y = 144
    if checkpoint == 90:
        print("Pedestal 2")
    if checkpoint == 91:
        x = -3
        y = 157
    if checkpoint == 92:
        print("Pedestal 3")
    if checkpoint == 93:
        x = 19
        y = 146
    if checkpoint == 94:
        print("Pedestal 4")
    if checkpoint == 95:
        x = 20
        y = 117
    if checkpoint == 96:
        print("Pedestal 5")
    if checkpoint == 97:
        x = 9
        y = 106
    if checkpoint == 98:
        x = 8
        y = 70
    if checkpoint == 99:
        x = 0
        y = 61
    if checkpoint == 100:
        print("Insert destro sphere")
    if checkpoint == 101:
        x = 22
        y = 42
    if checkpoint == 102:
        print("Destro chest")
    if checkpoint == 103:
        x = -26
        y = 37
    if checkpoint == 104:
        print("End of Trials")
    return [x, y]


def djose_dance(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 0
        y = -9
    if checkpoint == 1:
        x = 3
        y = 17
    if checkpoint == 2:
        x = 16
        y = 24
    if checkpoint == 3:
        x = 30
        y = 12
    if checkpoint == 4:
        x = 16
        y = 1
    if checkpoint == 5:
        x = -17
        y = 3
    if checkpoint == 6:
        x = -26
        y = -13
    if checkpoint == 7:
        x = -8
        y = -16
    return [x, y]


def djose_exit(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 11
        y = -149
    if checkpoint == 1:  # Talk to Auron
        x = 0
        y = 0
    if checkpoint == 2:
        x = -1
        y = -88
    if checkpoint == 3:  # Enter temple
        x = 0
        y = 0
    if checkpoint == 4:
        x = -18
        y = 6
    if checkpoint == 5:
        x = -41
        y = 56
    if checkpoint == 6:
        x = -41
        y = 56
    if checkpoint == 7:
        x = -41
        y = 56
    if checkpoint == 8:
        x = -52
        y = 94
    if checkpoint == 9:  # Enter room where Yuna is resting
        x = 0
        y = 0
    if checkpoint == 10:
        x = 13
        y = -1
    if checkpoint == 11:
        x = 13
        y = -1
    if checkpoint == 12:  # Remedy
        x = 0
        y = 0
    if checkpoint == 13:
        x = 11
        y = 28
    if checkpoint == 14:  # Wake up Yuna
        x = 0
        y = 0
    if checkpoint == 15:
        x = -31
        y = -211
    if checkpoint == 16:
        x = -129
        y = -253
    if checkpoint == 17:
        x = -178
        y = -261
    if checkpoint == 18:  # 4k gold chest
        x = 0
        y = 0
    if checkpoint == 19:
        x = -131
        y = -287
    if checkpoint == 20:
        x = -93
        y = -311
    if checkpoint == 21:
        x = -40
        y = -360
    if checkpoint == 22:  # Switch maps, to Bridge
        x = 0
        y = 0
    if checkpoint == 23:
        x = 26
        y = 50
    if checkpoint == 24:
        x = 53
        y = -17
    if checkpoint == 25:
        x = 58
        y = -52
    if checkpoint == 26:
        x = 37
        y = -113
    if checkpoint == 27:
        x = 4
        y = -236
    if checkpoint == 28:
        x = -9
        y = -333
    if checkpoint == 29:  # Switch map, to Djose road
        x = 0
        y = 0
    if checkpoint == 30:
        x = 626
        y = 858
    if checkpoint == 31:
        x = 591
        y = 985
    if checkpoint == 32:
        x = 550
        y = 1100
    if checkpoint == 33:
        x = 500
        y = 1200
    if checkpoint == 34:
        x = 0
        y = 0
    if checkpoint == 35:  # Remedy logic
        x = -18
        y = 19
    if checkpoint == 36:  # Pick up Remedy
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


def moonflow(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -138
        y = -254
    if checkpoint == 1:
        x = -179
        y = -262
    if checkpoint == 2:
        print("Picking up chest")
    if checkpoint == 3:
        x = -114
        y = -291
    if checkpoint == 4:
        x = -36
        y = -369
    if checkpoint == 5:
        x = -10
        y = -450
    if checkpoint == 6:
        x = 57
        y = -19
    if checkpoint == 7:
        x = 60
        y = -54
    if checkpoint == 8:
        x = 3
        y = -227
    if checkpoint == 9:
        x = -11
        y = -325
    if checkpoint == 10:
        x = -20
        y = -400
    if checkpoint == 11:  # Map - Fork in the road
        x = 610
        y = 843
    if checkpoint == 12:
        x = 567
        y = 991
    if checkpoint == 13:
        x = 567
        y = 1200
    if checkpoint == 14:  # Start of the long Moonflow path/map
        x = -988
        y = 1678
    if checkpoint == 15:
        x = -1072
        y = 1557
    if checkpoint == 16:
        x = -1112
        y = 1484
    if checkpoint == 17:
        x = -1159
        y = 1369
    if checkpoint == 18:
        x = -1176
        y = 1347
    if checkpoint == 19:
        x = -1230
        y = 1140
    if checkpoint == 20:
        x = -1317
        y = 783
    if checkpoint == 21:  # Ronso discussion
        x = -1317
        y = 783
    if checkpoint == 22:
        x = -1348
        y = 758
    if checkpoint == 23:
        x = -1438
        y = 717
    if checkpoint == 24:
        x = -1523
        y = 661
    if checkpoint == 25:
        x = -1571
        y = 624
    if checkpoint == 26:
        x = -1624
        y = 573
    if checkpoint == 27:
        x = -1666
        y = 538
    if checkpoint == 28:
        x = -1704
        y = 484
    if checkpoint == 29:
        x = -1801
        y = 365
    if checkpoint == 30:
        x = -1833
        y = 317
    if checkpoint == 31:
        x = -1838
        y = 299
    if checkpoint == 32:
        x = -1838
        y = 299
    if checkpoint == 33:
        x = -1856
        y = 214
    if checkpoint == 34:
        x = -1864
        y = 162
    if checkpoint == 35:
        x = -1866
        y = 124
    if checkpoint == 36:
        x = -1872
        y = -23
    if checkpoint == 37:
        x = -1880
        y = -163
    if checkpoint == 38:
        x = -1901
        y = -401
    if checkpoint == 39:
        x = -1898
        y = -483
    if checkpoint == 40:
        x = -1893
        y = -506
    if checkpoint == 41:
        x = -1855
        y = -503
    if checkpoint == 42:
        x = -1812
        y = -476
    if checkpoint == 43:  # Moonflow chest
        print("Moonflow chest")
    if checkpoint == 44:
        x = -1862
        y = -511
    if checkpoint == 45:
        x = -1901
        y = -513
    if checkpoint == 46:
        x = -1913
        y = -559
    if checkpoint == 47:
        x = -1968
        y = -650
    if checkpoint == 48:
        x = -1970
        y = -900
    if checkpoint == 49:  # Actual Moonflow map
        x = -1190
        y = 193
    if checkpoint == 50:
        x = -1118  # Can be used for tuning later.
        y = -614
    if checkpoint == 51:
        x = -1118
        y = -614
    if checkpoint == 52:
        x = -1034
        y = -566
    if checkpoint == 53:  # Last before "Whoa a Shoopuff"
        x = -960
        y = -500
    if checkpoint == 54:
        x = -200
        y = -60
    if checkpoint == 55:
        x = -30
        y = 180
    return [x, y]


def moonflow_bank_south(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -104
        y = 112
    if checkpoint == 1:
        x = -108
        y = 97
    if checkpoint == 2:
        x = -83
        y = 69
    if checkpoint == 3:
        x = -71
        y = 48
    return [x, y]


def moonflow_bank_north(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -305
        y = 184
    if checkpoint == 1:
        x = -400
        y = 150
    if checkpoint == 2:
        x = -1001
        y = -767
    if checkpoint == 3:  # Rikku scene
        x = -1135
        y = -807
    if checkpoint == 4:
        x = -1123
        y = -759
    if checkpoint == 5:
        x = -1134
        y = -699
    if checkpoint == 6:
        x = -1125
        y = -627
    if checkpoint == 7:  # Rikku steal/mix tutorial.
        print("Rikku steal/mix tutorial.")
    if checkpoint == 8:
        x = -1076
        y = -553
    if checkpoint == 9:
        x = -944
        y = -384
    if checkpoint == 10:
        x = -892
        y = -327
    if checkpoint == 11:  # Into the Guadosalam entrance map
        x = -800
        y = -270
    if checkpoint == 12:
        x = 313
        y = -911
    if checkpoint == 13:
        x = 269
        y = -812
    if checkpoint == 14:
        x = 130
        y = -443
    if checkpoint == 15:
        x = 98
        y = -300
    if checkpoint == 16:
        x = 86
        y = -190
    if checkpoint == 17:
        x = 74
        y = 32
    if checkpoint == 18:
        x = 70
        y = 200
    return [x, y]


def guado_storyline(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -8
        y = 109
    if checkpoint == 1:  # Dialog with party
        x = 0
        y = 0
    if checkpoint == 2:
        x = -56
        y = 110
    if checkpoint == 3:
        x = -56
        y = 110
    if checkpoint == 4:
        x = -56
        y = 110
    if checkpoint == 5:
        x = -56
        y = 110
    if checkpoint == 6:
        x = -82
        y = 51
    if checkpoint == 7:
        x = -84
        y = -3
    if checkpoint == 8:
        x = -50
        y = -11
    if checkpoint == 9:
        x = -3
        y = 9
    if checkpoint == 10:
        x = 46
        y = 34
    if checkpoint == 11:
        x = 120
        y = 92
    if checkpoint == 12:  # Towards the farplane
        x = 0
        y = 0
    if checkpoint == 13:
        x = -9
        y = 11
    if checkpoint == 14:  # Chest
        x = 0
        y = 0
    if checkpoint == 15:
        x = -5
        y = 101
    if checkpoint == 16:  # Screen to screen
        x = 0
        y = 0
    if checkpoint == 17:  # Approach party
        x = 0
        y = 0
    if checkpoint == 18:
        x = -1
        y = 35
    if checkpoint == 19:
        x = -1
        y = 88
    if checkpoint == 20:
        x = -4
        y = 152
    if checkpoint == 21:  # Into the farplane
        x = 0
        y = 0
    if checkpoint == 22:
        x = -44
        y = 0
    if checkpoint == 23:  # Wakka convo
        x = 0
        y = 0
    if checkpoint == 24:
        x = -26
        y = -65
    if checkpoint == 25:  # Yuna convo
        x = 0
        y = 0
    if checkpoint == 26:
        x = 64
        y = 41
    if checkpoint == 27:
        x = 31
        y = 30
    if checkpoint == 28:
        x = -12
        y = 9
    if checkpoint == 29:
        x = -54
        y = -9
    if checkpoint == 30:
        x = -85
        y = 0
    if checkpoint == 31:
        x = -66
        y = 84
    if checkpoint == 32:
        x = -33
        y = 115
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


def guado_skip(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 4
        y = 0
    if checkpoint == 1:
        x = -59
        y = 80
    if checkpoint == 2:
        x = -59
        y = 97
    if checkpoint == 3:
        x = -43
        y = 105
    if checkpoint == 4:
        x = -33
        y = 92
    if checkpoint == 5:
        print("Test if skip was successful.")
    if checkpoint == 6:
        x = -24
        y = 61
    if checkpoint == 7:
        x = -43
        y = 55
    if checkpoint == 8:
        x = -60
        y = 83
    if checkpoint == 9:
        x = -80
        y = 137
    if checkpoint == 10:
        x = -78
        y = 166
    if checkpoint == 11:
        x = -70
        y = 250
    if checkpoint == 18:
        x = -24
        y = 61
    if checkpoint == 19:
        x = -43
        y = 55
    if checkpoint == 20:
        print("Guado skip failed.")
        x = -44
        y = 56
    if checkpoint == 21:
        print("Shelinda scene")
    if checkpoint == 22:
        x = -18
        y = 96
    if checkpoint == 23:
        x = -25
        y = 144
    if checkpoint == 24:
        print("Back to the party")
    if checkpoint == 25:
        x = -33
        y = 92
    if checkpoint == 26:
        x = -24
        y = 61
    if checkpoint == 27:
        x = -43
        y = 55
    if checkpoint == 28:
        x = -60
        y = 83
    if checkpoint == 29:
        x = -80
        y = 137
    if checkpoint == 30:
        x = -78
        y = 166
    if checkpoint == 31:
        x = -70
        y = 250
    return [x, y]


def t_plains_south(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -23
        y = -1023
    if checkpoint == 1:
        x = -32
        y = -973
    if checkpoint == 2:
        x = -24
        y = -927
    if checkpoint == 3:
        x = 1
        y = -840
    if checkpoint == 4:
        x = -3
        y = -663
    if checkpoint == 5:  # Past crater
        x = -7
        y = -635
    if checkpoint == 6:
        x = 5
        y = -522
    if checkpoint == 7:
        x = -12
        y = -290
    if checkpoint == 8:
        x = 3
        y = 4
    if checkpoint == 9:
        x = 7
        y = 362
    if checkpoint == 10:
        x = 12
        y = 495
    if checkpoint == 11:
        x = 45
        y = 787
    if checkpoint == 12:
        x = 54
        y = 865
    if checkpoint == 13:
        x = 54
        y = 1200
    if checkpoint == 20:  # Nemesis route changes significantly.
        x = -44
        y = -887
    if checkpoint == 21:  # Touch save sphere
        x = 0
        y = 0
    if checkpoint == 22:
        x = -57
        y = -872
    if checkpoint == 23:
        x = -101
        y = -739
    if checkpoint == 24:
        x = -170
        y = -491
    if checkpoint == 25:  # Touch cactuar stone 1
        x = 0
        y = 0
    if checkpoint == 26:
        x = -63
        y = -361
    if checkpoint == 27:
        x = -20
        y = -152
    if checkpoint == 28:
        x = 2
        y = 9
    if checkpoint == 29:
        x = 63
        y = 98
    if checkpoint == 30:
        x = 114
        y = 193
    if checkpoint == 31:
        x = 185
        y = 204
    if checkpoint == 32:
        x = 204
        y = 166
    if checkpoint == 33:  # Touch cactuar stone 2
        x = 0
        y = 0
    if checkpoint == 34:  # Count 50 dodges
        x = 0
        y = 0
    if checkpoint == 35:
        x = 188
        y = 187
    if checkpoint == 36:
        x = 116
        y = 223
    if checkpoint == 37:
        x = 116
        y = 339
    if checkpoint == 38:
        x = 58
        y = 380
    return [x, y]


def t_plains_agency(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 4
        y = -36
    if checkpoint == 1:  # Agency shop
        x = 0
        y = 0
    if checkpoint == 2:
        x = 21
        y = -28
    if checkpoint == 3:
        x = 29
        y = -10
    if checkpoint == 4:  # Scene with Yuna
        x = 0
        y = 0
    if checkpoint == 5:
        x = 31
        y = -17
    if checkpoint == 6:
        x = 25
        y = -36
    if checkpoint == 7:  # Talk to Kimahri, affection manip
        x = 0
        y = 0
    if checkpoint == 8:  # Talk to Rikku to leave the agency
        x = 0
        y = 0
    if checkpoint == 9:
        x = -59
        y = 19
    if checkpoint == 10:
        x = -44
        y = 99
    if checkpoint == 11:  # Lightning shield, and exit to North pathing.
        x = 0
        y = 0
    return [x, y]


def t_plains_north(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -102
        y = -1162
    if checkpoint == 1:
        x = -92
        y = -1066
    if checkpoint == 2:
        x = -54
        y = -870
    if checkpoint == 3:
        x = -16
        y = -649
    if checkpoint == 4:
        x = 16
        y = -498
    if checkpoint == 5:
        x = 26
        y = -426
    if checkpoint == 6:
        x = 44
        y = -396
    if checkpoint == 7:
        x = 57
        y = -324
    if checkpoint == 8:
        x = 72
        y = -304
    if checkpoint == 9:
        x = 76
        y = -261
    if checkpoint == 10:
        x = 79
        y = -134
    if checkpoint == 11:
        x = 79
        y = -18
    if checkpoint == 12:
        x = 70
        y = 0
    if checkpoint == 13:
        x = 52
        y = 123
    if checkpoint == 14:  # any% only (non-CSR)
        x = -52
        y = 414
    if checkpoint == 15:
        x = -26
        y = 451
    if checkpoint == 16:  # Both back on track
        x = -1
        y = 739
    if checkpoint == 17:
        x = -18
        y = 797
    if checkpoint == 18:
        x = -35
        y = 883
    if checkpoint == 19:
        x = -37
        y = 967
    if checkpoint == 20:
        x = -73
        y = 1025
    if checkpoint == 21:
        x = -73
        y = 1300
    return [x, y]


def m_woods(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 206
        y = 41
    if checkpoint == 1:
        x = 142
        y = 62
    if checkpoint == 2:
        x = 102
        y = 108
    if checkpoint == 3:
        x = 34
        y = 114
    if checkpoint == 4:
        x = 6
        y = 87
    if checkpoint == 5:
        x = 15
        y = 2
    if checkpoint == 6:
        x = 1
        y = -6
    if checkpoint == 7:
        x = -66
        y = 10
    if checkpoint == 8:
        x = -109
        y = 60
    if checkpoint == 9:
        x = -113
        y = 116
    if checkpoint == 10:
        x = -96
        y = 172
    if checkpoint == 11:
        x = -115
        y = 214
    if checkpoint == 12:
        x = -131
        y = 234
    if checkpoint == 13:
        x = -131
        y = 234
    if checkpoint == 14:  # First chest
        print("First chest")
    if checkpoint == 15:
        x = -154
        y = 247
    if checkpoint == 16:
        x = -201
        y = 230
    if checkpoint == 17:
        x = -250
        y = 200
    if checkpoint == 18:  # Second map - with the loop
        x = 57
        y = 60
    if checkpoint == 19:
        x = 56
        y = -60
    if checkpoint == 20:
        x = 47
        y = -72
    if checkpoint == 21:
        x = 25
        y = -78
    if checkpoint == 22:
        x = -45
        y = -31
    if checkpoint == 23:
        x = -81
        y = 84
    if checkpoint == 24:
        x = -110
        y = 120
    if checkpoint == 25:
        x = -165
        y = 120
    if checkpoint == 26:
        x = -201
        y = 81
    if checkpoint == 27:
        x = -185
        y = 25
    if checkpoint == 28:
        x = -158
        y = 8
    if checkpoint == 29:
        x = -89
        y = 56
    if checkpoint == 30:
        x = -49
        y = 76
    if checkpoint == 31:
        x = 160
        y = 6
    if checkpoint == 32:  # Bartello
        x = 178
        y = -46
    if checkpoint == 33:
        x = 168
        y = -134
    if checkpoint == 34:
        x = 105
        y = -174
    if checkpoint == 35:
        x = -28
        y = -188
    if checkpoint == 36:  # Butterfly guy
        x = -97
        y = -214
    if checkpoint == 37:  # Touch butterfly
        x = -146
        y = -204
    if checkpoint == 38:
        x = -182
        y = -131
    if checkpoint == 39:
        x = -250
        y = -50
    if checkpoint == 40:  # Into next screen
        x = -505
        y = 36
    if checkpoint == 41:
        x = -508
        y = 139
    if checkpoint == 42:
        x = -527
        y = 148
    if checkpoint == 43:
        x = -580
        y = 82
    if checkpoint == 44:
        x = -569
        y = 43
    if checkpoint == 45:
        x = -523
        y = 37
    if checkpoint == 46:
        x = -449
        y = 16
    if checkpoint == 47:
        x = -447
        y = -8
    if checkpoint == 48:
        x = -481
        y = -72
    if checkpoint == 49:
        x = -562
        y = -151
    if checkpoint == 50:
        x = -590
        y = -151
    if checkpoint == 51:
        x = -620
        y = -137
    if checkpoint == 52:
        x = -675
        y = -84
    if checkpoint == 53:
        x = -752
        y = 2
    if checkpoint == 54:
        x = -737
        y = 62
    if checkpoint == 55:
        x = -717
        y = 115
    if checkpoint == 56:
        x = -717
        y = 163
    if checkpoint == 57:
        x = -645
        y = 167
    if checkpoint == 58:
        x = -612
        y = 144
    if checkpoint == 59:  # Check for completion status
        print("Check for completion status")
    if checkpoint == 60:  # Check for RNG2
        x, y = [-614,123]
    if checkpoint == 61:
        x = -601
        y = 126
    if checkpoint == 62:
        x = -596
        y = 59
    if checkpoint == 63:
        x = -613
        y = -53
    if checkpoint == 64:
        x = -654
        y = -98
    if checkpoint == 65:
        x = -750
        y = -200
    return [x, y]


def m_lake(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 50
        y = -51
    if checkpoint == 1:
        x = -13
        y = -99
    if checkpoint == 2:
        x = -32
        y = -143
    if checkpoint == 3:
        x = -43
        y = -195
    if checkpoint == 4:
        x = -69
        y = -244
    if checkpoint == 5:
        x = -97
        y = -267
    if checkpoint == 6:
        x = -130
        y = -285
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


def m_temple_approach(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 22
        y = 538
    if checkpoint == 1:
        x = 30
        y = 650
    if checkpoint == 2:  # From snowmobile screen to curve screen
        x = 39
        y = 86
    if checkpoint == 3:
        x = 87
        y = 202
    if checkpoint == 4:
        x = 166
        y = 298
    if checkpoint == 5:
        x = 216
        y = 323
    if checkpoint == 6:
        x = 310
        y = 358
    if checkpoint == 7:
        x = 396
        y = 382
    if checkpoint == 8:
        x = 472
        y = 378
    if checkpoint == 9:
        x = 526
        y = 338
    if checkpoint == 10:
        x = 646
        y = 270
    if checkpoint == 11:
        x = 714
        y = 217
    if checkpoint == 12:
        x = 778
        y = 101
    if checkpoint == 13:
        x = 801
        y = -45
    if checkpoint == 14:
        x = 801
        y = -206
    if checkpoint == 15:
        x = 815
        y = -455
    if checkpoint == 16:  # Into the door (dial in)
        x = 801
        y = -500
    return [x, y]


def temple_foyer(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -18
        y = -124
    if checkpoint == 1:
        print("Touch save sphere")
    if checkpoint == 2:
        x = 19
        y = -103
    if checkpoint == 3:
        x = 23
        y = -102
    if checkpoint == 4:
        print("Trommell")
    if checkpoint == 5:
        print("Lining up for skip")
    if checkpoint == 6:
        x = -73
        y = -14
    if checkpoint == 7:
        x = -109
        y = -22
    if checkpoint == 8:
        print("Chest")
    if checkpoint == 9:
        x = -73
        y = -14
    if checkpoint == 10:
        x = -21
        y = 4
    if checkpoint == 11:
        print("Check if skip successful")
    if checkpoint == 12:
        x = 2
        y = 38
    if checkpoint == 13:
        x = 0
        y = 103
    if checkpoint == 14:
        print("Check if pause necessary")
    if checkpoint == 15:  # Into the room before Seymour
        x = 0
        y = 300
    if checkpoint == 16:  # Into Seymour's room
        x = 0
        y = -300
    if checkpoint == 20:  # Skip fail, use this path instead.
        x = 16
        y = 30
    if checkpoint == 21:
        x = 41
        y = 59
    if checkpoint == 22:
        x = 59
        y = 118
    if checkpoint == 23:
        print("Into the door, Jyscal sphere")
    if checkpoint == 24:
        print("And back out again")
    if checkpoint == 25:
        x = 35
        y = 48
    if checkpoint == 26:
        x = 15
        y = 31
    return [x, y]


def m_temple_trials(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 2
        y = -114
    if checkpoint == 1:
        x = 2
        y = -200
    if checkpoint == 2:
        print("Activate the trials")
    if checkpoint == 3:
        x = -12
        y = -116
    if checkpoint == 4:
        x = -33
        y = -113
    if checkpoint == 5:
        x = -50
        y = -88
    if checkpoint == 6:
        x = -66
        y = -16
    if checkpoint == 7:
        x = -47
        y = -12
    if checkpoint == 8:
        x = 31
        y = 4
    if checkpoint == 9:
        print("Push pedestal")
    if checkpoint == 10:
        x = 18
        y = 52
    if checkpoint == 11:
        x = 6
        y = 83
    if checkpoint == 12:
        x = 2
        y = 107
    if checkpoint == 13:
        print("Grab first Mac Sphere")
    if checkpoint == 14:
        x = 11
        y = 71
    if checkpoint == 15:
        x = 26
        y = 44
    if checkpoint == 16:
        x = 31
        y = 43
    if checkpoint == 17:
        print("Place first Mac Sphere")
    if checkpoint == 18:
        x = 41
        y = 44
    if checkpoint == 19:
        x = 42
        y = 49
    if checkpoint == 20:
        print("Push pedestal")
    if checkpoint == 21:
        x = 12
        y = 2
    if checkpoint == 22:
        x = 0
        y = 3
    if checkpoint == 23:
        print("Pick up Glyph sphere")
    if checkpoint == 24:
        x = -8
        y = 4
    if checkpoint == 25:  # Spot next to the ramp-sphere
        x = -77
        y = 54
    if checkpoint == 26:
        x = -80
        y = 24
    if checkpoint == 27:  # Bottom of the ramp
        x = -15
        y = 7
    if checkpoint == 28:
        x = 0
        y = 4
    if checkpoint == 29:
        print("Push pedestal")
    if checkpoint == 30:
        x = -11
        y = -27
    if checkpoint == 31:
        x = -9
        y = -49
    if checkpoint == 32:
        print("Insert glyph sphere")
    if checkpoint == 33:
        x = -15
        y = 7
    if checkpoint == 34:
        x = -80
        y = 24
    if checkpoint == 35:
        x = -77
        y = 54
    if checkpoint == 36:
        x = -62
        y = 51
    if checkpoint == 37:
        x = -21
        y = -40
    if checkpoint == 38:
        x = -19
        y = -53
    if checkpoint == 39:
        print("Second Mac sphere")
    if checkpoint == 40:
        x = -21
        y = -40
    if checkpoint == 41:
        x = -62
        y = 51
    if checkpoint == 42:
        x = -77
        y = 54
    if checkpoint == 43:
        x = -80
        y = 24
    if checkpoint == 44:
        x = -15
        y = 7
    if checkpoint == 45:
        x = 11
        y = -32
    if checkpoint == 46:
        print("Second Mac sphere")
    if checkpoint == 47:
        x = 10
        y = -27
    if checkpoint == 48:
        x = -15
        y = 7
    if checkpoint == 49:
        x = -80
        y = 24
    if checkpoint == 50:
        x = -77
        y = 54
    if checkpoint == 51:
        print("Third Mac sphere")
    if checkpoint == 52:
        x = -3
        y = 4
    if checkpoint == 53:
        print("Third Mac sphere")
    if checkpoint == 54:  # Ready to get out of here
        x = -68
        y = -17
    if checkpoint == 55:
        x = -48
        y = -93
    if checkpoint == 56:
        x = -20
        y = -116
    if checkpoint == 57:
        x = -5
        y = -106
    if checkpoint == 58:
        print("Trials - end")
    return [x, y]


def m_temple_escape(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 807
        y = -263
    if checkpoint == 1:
        x = 817
        y = -244
    if checkpoint == 2:
        print("Touching save sphere")
    if checkpoint == 3:
        x = 815
        y = -227
    if checkpoint == 4:
        x = 815
        y = -206
    if checkpoint == 5:  # Start of turn
        x = 801
        y = -45
    if checkpoint == 6:
        x = 778
        y = 101
    if checkpoint == 7:
        x = 714
        y = 217
    if checkpoint == 8:
        x = 646
        y = 270
    if checkpoint == 9:
        x = 526
        y = 338
    if checkpoint == 10:
        x = 472
        y = 378
    if checkpoint == 11:
        x = 396
        y = 382
    if checkpoint == 12:
        x = 310
        y = 358
    if checkpoint == 13:
        x = 216
        y = 323
    if checkpoint == 14:
        x = 166
        y = 298
    if checkpoint == 15:
        x = 87
        y = 202
    if checkpoint == 16:
        x = 39
        y = 86
    if checkpoint == 17:
        x = -9
        y = -38
    if checkpoint == 18:
        x = -50
        y = -100
    if checkpoint == 19:  # Back to the snowmobiles
        x = -13
        y = 410
    if checkpoint == 20:
        x = 6
        y = 363
    if checkpoint == 21:
        x = 44
        y = 320
    if checkpoint == 22:
        x = 51
        y = 274
    if checkpoint == 23:
        x = 40
        y = 243
    if checkpoint == 24:
        x = 25
        y = 218
    if checkpoint == 25:
        x = -32
        y = 196
    if checkpoint == 26:
        x = -30
        y = 169
    if checkpoint == 27:
        x = -28
        y = 63
    if checkpoint == 28:
        x = -20
        y = -159
    if checkpoint == 29:
        x = -8
        y = -269
    if checkpoint == 30:
        x = 13
        y = -420
    if checkpoint == 31:
        x = 33
        y = -565
    if checkpoint == 32:
        x = 33
        y = -700
    return [x, y]


def under_mac_temple(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 1
        y = 146
    if checkpoint == 1:
        x = 34
        y = 116
    if checkpoint == 2:
        x = 29
        y = 98
    if checkpoint == 3:
        x = 0
        y = 80
    if checkpoint == 4:  # Talk to Rikku then Yuna
        x = 0
        y = 0
    if checkpoint == 5:
        x = 1
        y = 146
    if checkpoint == 6:
        x = 34
        y = 116
    if checkpoint == 7:
        x = 29
        y = 98
    if checkpoint == 8:
        x = 10
        y = 86
    if checkpoint == 9:
        x = -24
        y = 103
    if checkpoint == 10:
        x = -41
        y = 95
    if checkpoint == 11:  # Open chest
        x = 0
        y = 0
    if checkpoint == 12:
        x = -21
        y = 103
    if checkpoint == 13:
        x = 0
        y = 73
    if checkpoint == 14:
        x = -5
        y = 13
    if checkpoint == 15:  # Talk to Auron
        x = 0
        y = 0
    if checkpoint == 16:  # Back down to next scene
        x = 0
        y = 73
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
    return [x, y]


def desert(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 0
        y = -74
    if checkpoint == 1:
        x = 20
        y = -69
    if checkpoint == 2:
        print("Touching save sphere")
    if checkpoint == 3:
        x = 3
        y = -79
    if checkpoint == 4:
        x = -13
        y = -128
    if checkpoint == 5:
        x = 12
        y = -288
    if checkpoint == 6:
        x = 134
        y = -440
    if checkpoint == 7:
        x = 147
        y = -421
    if checkpoint == 8:
        x = 197
        y = -387
    if checkpoint == 9:
        print("Map change")
    if checkpoint == 10:
        x = 172
        y = -569
    if checkpoint == 11:
        x = 441
        y = -366
    if checkpoint == 12:
        x = 228
        y = -523
    if checkpoint == 13:
        x = 206
        y = -534
    if checkpoint == 14:
        x = 89
        y = -522
    if checkpoint == 15:
        x = -26
        y = -523
    if checkpoint == 16:
        x = -120
        y = -494
    if checkpoint == 17:
        x = -186
        y = -395
    if checkpoint == 18:
        x = -158
        y = -346
    if checkpoint == 19:
        x = 44
        y = -250
    if checkpoint == 20:
        x = 138
        y = -200
    if checkpoint == 21:
        x = 164
        y = -134
    if checkpoint == 22:
        x = 190
        y = -8
    if checkpoint == 23:
        x = 199
        y = 28
    if checkpoint == 24:
        print("Touching save sphere")
    if checkpoint == 25:
        x = 187
        y = 26
    if checkpoint == 26:
        x = 170
        y = 29
    if checkpoint == 27:
        x = 160
        y = 46
    if checkpoint == 28:
        x = 180
        y = 67
    if checkpoint == 29:
        x = 253
        y = 116
    if checkpoint == 30:
        x = 352
        y = 126
    if checkpoint == 31:  # Machina battle mid-path
        x = 478
        y = 139
    if checkpoint == 32:
        x = 552
        y = 157
    if checkpoint == 33:
        x = 594
        y = 224
    if checkpoint == 34:
        x = 659
        y = 444
    if checkpoint == 35:
        x = 657
        y = 698
    if checkpoint == 36:
        x = 664
        y = 790
    if checkpoint == 37:
        x = 698
        y = 854
    if checkpoint == 38:
        x = 800
        y = 1000
    if checkpoint == 39:  # Large open map with two directions
        x = 333
        y = -501
    if checkpoint == 40:
        x = -70
        y = 177
    if checkpoint == 41:
        x = -158
        y = 278
    if checkpoint == 42:
        x = -278
        y = 360
    if checkpoint == 43:  # Extra spots for future precision if needed
        x = -278
        y = 360
    if checkpoint == 44:  # Extra spots for future precision if needed
        x = -278
        y = 360
    if checkpoint == 45:
        x = -356
        y = 468
    if checkpoint == 46:
        x = -426
        y = 550
    if checkpoint == 47:
        x = -624
        y = 693
    if checkpoint == 48:
        x = -667
        y = 773
    if checkpoint == 49:
        x = -680
        y = 850
    if checkpoint == 50:  # Final map before Home
        x = -252
        y = -101
    if checkpoint == 51:
        x = -192
        y = 45
    if checkpoint == 52:
        x = -41
        y = 419
    if checkpoint == 53:  # Sandragora #1
        print("Sandragora #1")
    if checkpoint == 54:
        x = -57
        y = 439
    if checkpoint == 55:
        x = -228
        y = 764
    if checkpoint == 56:
        x = -228
        y = 764
    if checkpoint == 58:  # Lining up for Sandy skip
        x = -228
        y = 764
    if checkpoint == 59:  # Lining up for Sandy skip
        x = -235
        y = 797
    if checkpoint == 61:  # Waiting to be pushed
        x = -273
        y = 850
    if checkpoint == 62:  # Past Sandy
        x = -273
        y = 850
    if checkpoint == 63:
        x = -294
        y = 886
    if checkpoint == 64:
        print("Test for area completion")
    if checkpoint == 65:
        x = -300
        y = 1000
    if checkpoint == 70:  # Nemesis logic
        x = -457
        y = 521
    if checkpoint == 71:
        x = -446
        y = 458
    if checkpoint == 72:  # Chest, lv.2 key sphere
        x = 0
        y = 0
    if checkpoint == 73:
        x = -474
        y = 476
    if checkpoint == 74:  # Chest, 10k gil
        x = 0
        y = 0
    if checkpoint == 75:
        x = -481
        y = 505
    return [x, y]


def home(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 5
        y = -35
    if checkpoint == 1:
        x = 46
        y = 21
    if checkpoint == 2:
        x = 70
        y = 69
    if checkpoint == 3:
        x = 70
        y = 82
    if checkpoint == 4:
        x = 67
        y = 89
    if checkpoint == 5:  # Extra in case we need refactoring later.
        x = 67
        y = 89
    if checkpoint == 6:  # Extra in case we need refactoring later.
        x = 67
        y = 89
    if checkpoint == 7:  # Touch save sphere
        x = 0
        y = 0
    if checkpoint == 8:
        x = 71
        y = 68
    if checkpoint == 9:
        x = 55
        y = 52
    if checkpoint == 10:
        x = 3
        y = 82
    if checkpoint == 11:
        x = 0
        y = 120
    if checkpoint == 12:
        x = 0
        y = 0
    if checkpoint == 13:
        x = 0
        y = -5
    if checkpoint == 14:  # First battle
        x = 0
        y = -5
    if checkpoint == 15:
        x = 41
        y = 35
    if checkpoint == 16:
        x = 81
        y = 65
    if checkpoint == 17:
        x = 161
        y = 125
    if checkpoint == 18:  # Into second battle and new map
        x = 0
        y = 220
    if checkpoint == 19:
        x = 0
        y = 220
    if checkpoint == 20:  # Branch based on blitz win
        x = 0
        y = 0
    if checkpoint == 21:
        x = -2
        y = 236
    if checkpoint == 22:
        x = -5
        y = 310
    if checkpoint == 23:
        x = -13
        y = 330
    if checkpoint == 24:  # Right next to door
        x = -70
        y = 359
    if checkpoint == 25:
        x = -168
        y = 275
    if checkpoint == 26:
        x = -184
        y = 253
    if checkpoint == 27:  # Screen change before next battle
        x = -184
        y = 253
    if checkpoint == 28:
        x = -174
        y = 223
    if checkpoint == 29:
        x = -184
        y = 210
    if checkpoint == 30:
        x = -184
        y = 210
    if checkpoint == 31:  # Down the stairs, storyline.
        x = -234
        y = 162
    if checkpoint == 32:
        x = -296
        y = 217
    if checkpoint == 33:
        x = -315
        y = 217
    if checkpoint == 34:
        x = -343
        y = 189
    if checkpoint == 35:
        x = -354
        y = 182
    if checkpoint == 36:
        x = -367
        y = 193
    if checkpoint == 37:
        x = -360
        y = 231
    if checkpoint == 38:
        x = -352
        y = 265
    if checkpoint == 39:  # Open chest
        x = 0
        y = 0
    if checkpoint == 40:
        x = -398
        y = 219
    if checkpoint == 41:
        x = -414
        y = 211
    if checkpoint == 42:  # Big Reveal room
        x = 0
        y = 0
    if checkpoint == 43:
        x = 91
        y = -25
    if checkpoint == 44:
        x = 124
        y = -50
    if checkpoint == 45:  # Stairs to airship
        x = 0
        y = 0
    if checkpoint == 46:
        x = 188
        y = 58
    if checkpoint == 47:
        x = 101
        y = 59
    if checkpoint == 48:
        x = 0
        y = 60
    if checkpoint == 49:
        x = 0
        y = 0
    if checkpoint == 50:
        x = 0
        y = 0
    if checkpoint == 60:  # Used for Kilika skip and Nemesis, extra chest.
        x = -343
        y = 189
    if checkpoint == 61:
        x = -339
        y = 169
    if checkpoint == 62:
        x = -311
        y = 146
    if checkpoint == 63:  # Nemesis, extra chest.
        x = 0
        y = 0
    if checkpoint == 81:
        x = 0
        y = 97
    if checkpoint == 82:
        x = -6
        y = 29
    if checkpoint == 83:
        x = -20
        y = 15
    if checkpoint == 84:
        x = -2
        y = 39
    if checkpoint == 85:
        x = 6
        y = 44
    if checkpoint == 86:  # Open chest
        x = 0
        y = 0
    if checkpoint == 87:
        x = 1
        y = 157
    return [x, y]


def rescue_airship(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -232
        y = 332
    if checkpoint == 1:
        x = -242
        y = 308
    if checkpoint == 2:
        x = -241
        y = 215
    if checkpoint == 3:
        x = -240
        y = 80
    if checkpoint == 4:  # After leaving and re-entering the cockpit
        x = -240
        y = 324
    if checkpoint == 5:
        x = -226
        y = 352
    if checkpoint == 6:
        x = -223
        y = 366
    if checkpoint == 7:
        x = -243
        y = 384
    if checkpoint == 8:
        x = -242
        y = 407
    if checkpoint == 9:  # Talk to Brother
        x = 0
        y = 0
    if checkpoint == 10:
        x = -244
        y = 383
    if checkpoint == 11:
        x = -257
        y = 375
    if checkpoint == 12:
        x = -269
        y = 353
    if checkpoint == 13:  # Touch save sphere
        x = 0
        y = 0
    if checkpoint == 14:
        x = -260
        y = 343
    if checkpoint == 15:
        x = -257
        y = 325
    if checkpoint == 16:
        x = -244
        y = 314
    if checkpoint == 17:
        x = -244
        y = 314
    if checkpoint == 18:
        x = 0
        y = 0
    if checkpoint == 19:
        x = 0
        y = 0
    if checkpoint == 20:
        x = 0
        y = 0
    return [x, y]


def bevelle_pre_trials(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -97
        y = -1
    if checkpoint == 1:
        x = -200
        y = -3
    if checkpoint <= 2:
        x = 4
        y = -44
    if checkpoint == 3:
        x = 26
        y = -18
    if checkpoint == 4:
        x = 71
        y = -16
    if checkpoint == 5:
        x = 80
        y = 4
    if checkpoint == 6:
        x = 85
        y = 115
    if checkpoint == 7:
        x = 71
        y = 150
    return [x, y]


def bevelle_trials(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = 64
        y = 177
    if checkpoint == 1:
        x = 75
        y = 200
    if checkpoint == 2:
        x = -19
        y = -62
    if checkpoint == 3:
        print("First pedestal.")
    if checkpoint == 4:
        print("Missed first alcove, recovering.")
    if checkpoint == 5:
        x = -50
        y = 88
    if checkpoint == 6:
        x = -66
        y = 93
    if checkpoint == 7:
        print("First Bevelle sphere, and then more gliding.")
    if checkpoint == 8:
        x = 13
        y = 88
    if checkpoint == 9:
        x = 13
        y = 93
    if checkpoint == 10:
        print("Insert Bevelle sphere. Activate lower areas.")
    if checkpoint == 11:
        x = 27
        y = 92
    if checkpoint == 12:
        x = 26
        y = 86
    if checkpoint == 13:
        print("Down to the lower areas.")
    if checkpoint == 14:
        x = 397
        y = 357
    if checkpoint == 15:
        x = 501
        y = 363
    if checkpoint == 16:
        print("Take sphere from second alcove")
    if checkpoint == 17:
        x = 406
        y = 364
    if checkpoint == 18:
        print("To third alcove, and insert Glyph sphere")
    if checkpoint == 19:
        x = 353
        y = 531
    if checkpoint == 20:
        x = 367
        y = 532
    if checkpoint == 21:
        x = 370
        y = 526
    if checkpoint == 22:
        print("Remove Bevelle sphere")
    if checkpoint == 23:
        x = 367
        y = 532
    if checkpoint == 24:
        print("Insert Bevelle sphere")
    if checkpoint == 25:
        x = 353
        y = 531
    if checkpoint == 26:
        x = 342
        y = 527
    if checkpoint == 27:
        x = 352
        y = 525
    if checkpoint == 28:
        print("Take Glyph sphere")
    if checkpoint == 29:
        x = 367
        y = 532
    if checkpoint == 30:
        x = 374
        y = 526
    if checkpoint == 31:
        x = 431
        y = 527
    if checkpoint == 32:
        print("Insert Glyph sphere")
    if checkpoint == 33:
        x = 499
        y = 522
    if checkpoint == 34:
        print("Take Destro sphere")
    if checkpoint == 35:
        x = 374
        y = 524
    if checkpoint == 36:
        x = 366
        y = 524
    if checkpoint == 37:
        print("Insert Destro sphere")
    if checkpoint == 38:
        x = 367
        y = 532
    if checkpoint == 39:
        print("Remove Bevelle sphere")
    if checkpoint == 40:
        x = 369
        y = 526
    if checkpoint == 41:
        print("Back on track")
    if checkpoint == 42:
        x = 392
        y = 366
    if checkpoint == 43:
        print("Insert Bevelle sphere (back in second alcove)")
    if checkpoint == 44:
        x = 395
        y = 372
    if checkpoint == 45:
        x = 407
        y = 370
    if checkpoint == 46:
        x = 406
        y = 363
    if checkpoint == 47:
        print("Take Destro sphere")
    if checkpoint == 48:
        x = 493
        y = 371
    if checkpoint == 49:
        x = 493
        y = 371
    if checkpoint == 50:
        print("Insert Destro sphere")
    if checkpoint == 51:
        x = 406
        y = 364
    if checkpoint == 52:
        print("Back on track, to the exit")
    if checkpoint == 53:  # Final map with chests.
        x = 95
        y = 271
    if checkpoint == 54:
        x = 83
        y = 271
    if checkpoint == 55:
        x = 76
        y = 263
    if checkpoint == 56:
        x = -5
        y = 270
    if checkpoint == 57:
        x = -16
        y = 279
    if checkpoint == 58:
        print("Picking up chest")
    if checkpoint == 59:
        x = -5
        y = 302
    if checkpoint == 60:
        x = -5
        y = 400
    return [x, y]


def seymour_natus():  # First checkpoint ever written. :D
    x = 15
    y = 150
    return [x, y]


def suteki_da_ne(checkpoint):
    x = 999
    y = 999
    if checkpoint == 0:
        x = -3
        y = 17
    if checkpoint == 2:
        x = 42
        y = -55
    if checkpoint == 4:
        x = 208
        y = 51
    if checkpoint == 5:  # Enjoy scene
        print("Enjoy this very long scene")
    if checkpoint == 7:
        x = 93
        y = -9
    if checkpoint == 9:
        x = -55
        y = -29
    if checkpoint == 10:
        x = -20
        y = 4
    if checkpoint == 11:
        x = 6
        y = 50
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
        print("Map change, no target from this function.")
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
        print("Map change, no target from this function.")
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
        print("Map change, no target from this function.")
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
        print("Second trial, no target from this function.")
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
        print("Map change, no target from this function.")
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
        print("Mi'ihen agency scene, no target from this function.")
    if checkpoint == 4:
        x = 779
        y = -695
    if checkpoint == 5:
        x = 844
        y = -551
    if checkpoint == 6:
        print("Map change, no target from this function.")
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
        print("Fortune sphere, no direction from this function.")
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
        print("Friend sphere, no direction from this function.")
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
        print("Luck sphere, no direction from this function.")
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
        print("Touching save sphere, no direction from this function.")
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
        print("First pedetsol, no direction from here.")
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
        print("Picking up Kilika sphere")
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
        print("Placing Kilika sphere")
    if checkpoint == 27:
        x = 72
        y = -12
    if checkpoint == 28:
        print("Activating second pedestal")
    if checkpoint == 29:
        x = 77
        y = 43
    if checkpoint == 30:
        print("Moving into next room.")
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
        print("Activating second pedestal")
    if checkpoint == 47:
        x = 84
        y = 45
    if checkpoint == 48:
        print("Moving into next room.")
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
        print("Activating second pedestal")
    if checkpoint == 67:
        x = 84
        y = 45
    if checkpoint == 68:
        print("Moving into next room.")
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
        print("Picking up Besaid sphere")
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
        print("Placing Besaid sphere")
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
        print("Touch save sphere")
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
