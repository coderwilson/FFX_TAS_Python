import pyxinput
import time
import FFX_Xbox
import FFX_Battle
import FFX_Screen
import FFX_core
import FFX_memory
import FFX_Logs
from math import copysign
import numpy as np

FFXC = FFX_Xbox.FFXC

def lineSphereIntersect(start, end, circle, radius=11):
    numHits = 0
    hits = []

    direction = end - start
    sphereToStart = start - circle
    a = np.dot(direction, direction)
    b = 2 * np.dot(sphereToStart, direction)
    c = np.dot(sphereToStart, sphereToStart) - radius**2
    d = b**2 - 4*a*c
    if d < 0: # no intersection
        return (numHits, hits)

    d = np.sqrt(d)
    # Solve quadratic equation
    t1 = (-b -d)/(2*a)
    t2 = (-b +d)/(2*a)

    if t1 >= 0 and t1 <= 1:
        numHits += 1
        hits.append(start + direction * t1)
    if t2 >= 0 and t2 <= 1:
        numHits += 1
        hits.append(start + direction * t2)
    return (numHits, hits)

def pathAround(player, circle, target, radius = 11):
    line = player - circle
    line /= np.linalg.norm(line) # normalize to length 1
    angle = np.arctan2(line[1],line[0])
    newAngle1 = angle + 0.5 * np.pi
    newAngle2 = angle - 0.5 * np.pi
    p1 = circle +  [radius * np.cos(newAngle1), radius * np.sin(newAngle1)]
    p2 = circle +  [radius * np.cos(newAngle2), radius * np.sin(newAngle2)]
    print(circle, p1, p2)
    # Find which of two possible points gives shortest path
    p1length = np.linalg.norm(p1 - player) + np.linalg.norm(target - p1)
    p2length = np.linalg.norm(p2 - player) + np.linalg.norm(target - p2)
    if p1length < p2length:
        return p1
    return p2

def engage():
    print("Start egg hunt")
    startTime = time.time()
    checkpoint = 0
    battleCount = 0
    lookingCount = 0
    camCount = 0
    print("Generating Plot file (the X/Y kind)")
    #FFX_Logs.nextPlot()
    #time.sleep(3)
    while FFX_memory.getStoryProgress() < 3251:
        if FFX_Screen.BattleScreen():
            print("Battle engaged - using flee.")
            FFX_Battle.fleeLateGame()
            battleCount += 1
        elif FFX_memory.menuOpen():
            print("Clicking to control.")
            FFXC.set_value('BtnB',1)
            time.sleep(0.035)
            FFXC.set_value('BtnB',0)
            time.sleep(0.035)
        else:

            #Move to first egg, while in control.
            complete = 0
            activeEgg = 99
            target = [10,-10]
            moveVersion = 0
            while complete == 0:

                if activeEgg == 99:
                    if lookingCount % 200 < 100:
                        target = [20,-20]
                    else:
                        target = [-20,20]
                #print("Building egg array")
                eggArray = FFX_memory.buildEggs()
                iceArray = FFX_memory.buildIcicles() #Added for additional pathing needs
                currentTime = time.time()
                if activeEgg == 99:
                    for marker in range(10): #Only print active eggs/icicles
                        if activeEgg == 99 and eggArray[marker].goForEgg == True and eggArray[marker].eggLife < 150:
                            activeEgg = marker
                            target = [eggArray[marker].x, eggArray[marker].y]
                            clickTimer = currentTime + 8 #We will hunt for this egg for this many seconds.
                            print("New target egg: ", target)
                elif eggArray[activeEgg].goForEgg == False:
                    activeEgg = 99
                    if lookingCount % 200 < 100:
                        target = [20,-20]
                    else:
                        target = [-20,20]
                elif eggArray[activeEgg].eggLife == 150:
                    activeEgg = 99
                    if lookingCount % 200 < 100:
                        target = [20,-20]
                    else:
                        target = [-20,20]
                if FFX_Screen.BattleScreen():
                    print("Battle engaged - using flee. (Loop break)")
                    complete = 1
                elif FFX_memory.getStoryProgress() > 3250:
                    print("Story progress trigger. Moving on. (loop break)")
                    complete = 1
                else:
                    #print("Movement happening.")
                    #target = [-70,-70]
                    oldTarget = target
                    player = FFX_memory.getCoords()
                    iceArray = FFX_memory.buildIcicles()
                    (forward, right) = FFX_memory.getMovementVectors()

                    targetPos = np.array([target[0], target[1]])
                    playerPos = np.array(player)

                    closestIntersect = 9999
                    intersectPoint = []
                    for icicle in iceArray:
                        numIntersect, hits = lineSphereIntersect(playerPos, targetPos, np.array([icicle.x, icicle.y]))
                        if numIntersect > 0:
                            intersectDistance = (player[0] - hits[0][0])**2 + (player[1] - hits[0][1])**2
                            if intersectDistance < closestIntersect:
                                closestIntersect = intersectDistance
                                intersectPoint = hits[0]

                    if closestIntersect < 9999:
                        target = pathAround(playerPos, np.array(intersectPoint), targetPos)

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

                    FFXC.set_value('AxisLx', Lx)
                    FFXC.set_value('AxisLy', Ly)
                    target = oldTarget

                    #camCount += 1
                    #print(camCount)
                    #if camCount % 20 == 0:
                    #    FFX_Logs.writePlot("TEST")


                    #Now if we're close, we want to slow down a bit.
                    if activeEgg != 99 and eggArray[activeEgg].distance < 15 and eggArray[activeEgg].eggLife < 130:
                        time.sleep(0.15)
                        FFXC.set_value('AxisLx', 0)
                        FFXC.set_value('AxisLy', 0)
                        time.sleep(0.15)
                    elif activeEgg == 99:
                        print("Looking for a new egg. Move version: ", moveVersion," | ",lookingCount)
                        lookingCount += 1
                    else:
                        print("Targetting egg: ", moveVersion," | ",target)
                if FFX_memory.userControl() == False:
                    if FFX_Screen.Minimap2():
                        FFX_Xbox.menuB()
                    else:
                        FFXC.set_value('AxisLx', 0)
                        FFXC.set_value('AxisLy', 0)
    endTime = time.time()
    print("End egg hunt")
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    duration = endTime - startTime
    print("Duration: ", str(duration))
    print("Battle count: ", battleCount)
    try:
        FFX_Logs.writeStats("Egg hunt duration in seconds:")
        FFX_Logs.writeStats(str(round(duration,2)))
        FFX_Logs.writeStats("Egg hunt battles:")
        FFX_Logs.writeStats(str(battleCount))
    except:
        print("No log file.")
