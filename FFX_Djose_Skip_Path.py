import FFX_memory
import FFX_targetPathing


def toCoords(items):
    return list(map(lambda i: (i.x, i.y), items))

# def distance(a, b):
#     return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


checkpoints = [[467, -122], [500, 64], [860, 19], [1015, 54],  # Move into next area
               # First half of area
               [-243, -739],
               [-200, -300],
               # Second half of area, exact coordinates of lucille
               [-155.6760711669922, -173.4205780029297],
               [-148.83901977539062, -160.09024047851562],
               [-123.31393432617188, -99.24992370605469],
               [-117.18793487548828, -85.20985412597656],
               [-110.04093170166016, -68.82976531982422],
               [-95.02725982666016, -35.96002960205078],
               [-92.92814636230469, -26.13880729675293],
               [-82.38444519042969, 10.618974685668945],
               [-80.4589614868164, 22.940702438354492],
               [-75.82816314697266, 37.54235076904297],
               [-64.91490936279297, 66.361328125],
               [-59.478553771972656, 75.00630187988281],
               [-33.65585708618164, 118.2311782836914],
               [27.503202438354492, 215.4871368408203],
               [38.37591552734375, 232.77708435058594],
               [56.04407501220703, 260.87322998046875],
               [94.09864044189453, 321.388427734375],
               [111.766845703125, 349.48480224609375],
               [123.99868774414062, 368.9361267089844],
               [137.58961486816406, 390.5487365722656],
               [157.97604370117188, 422.9676208496094],
               [177.0034637451172, 453.2252502441406],
               [213.79518127441406, 506.0111999511719],
               [234.78477478027344, 521.9990844726562],
               [266.2691650390625, 543.8006591796875],
               [329.2375183105469, 587.404052734375],
               [337.63330078125, 593.2178344726562],
               [375.4143981933594, 619.3798828125],
               [450.011474609375, 656.1323852539062],
               # [442.06561279296875, 651.6763305664062], # Attempt to turn back
               [495.8471374511719, 700.2091064453125],
               [546.3902587890625, 745.9745483398438],

               # More possible stops
               #[565.3033447265625, 763.1240234375],
               #[552.0641479492188, 751.1195068359375],
               #[542.6076049804688, 742.5446166992188],
               ]  # [431.89208984375, 656.8260498046875], [639.948486328125, 829.5191040039062]]


def lucillePush():
    buttonPressed = False
    delta = [0, 0]
    lucille = [0, 0]
    target = checkpoints.pop(0)
    print("Target:", target)
    player = FFX_memory.getCoords()
    lucille = FFX_memory.lucilleDjoseCoords()
    lucilleCheckpoints = [[0, 0]]
    newLucille = FFX_memory.lucilleDjoseCoords()
    if newLucille[0] != 0 and lucille[0] != 0:
        newDelta = [newLucille[0] - lucille[0], newLucille[1] - lucille[1]]
        deltaSum = max(0.01, abs(newDelta[0]) + abs(newDelta[1]))
        newDelta[0] /= deltaSum
        newDelta[1] /= deltaSum
        if newDelta[0] != 0 or newDelta[1] != 0:
            delta = newDelta
            # if not isclose(delta[0], prevDelta[0], abs_tol=0.1) or not isclose(delta[1], prevDelta[1], abs_tol=0.1):
            #     if distance(newLucille, lucilleCheckpoints[-1]) > 10:
            #         lucilleCheckpoints.append(newLucille)
    lucille = newLucille
    atCheckpoint = FFX_targetPathing.setMovement(target, 1.5)
    if len(checkpoints) > 0:
        if atCheckpoint:
            target = checkpoints.pop(0)
