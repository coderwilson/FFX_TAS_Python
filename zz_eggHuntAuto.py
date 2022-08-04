import pyautogui
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

    # Create two points rotated 90 degrees from player -> circle intersection
    newAngle1 = angle + 0.5 * np.pi
    newAngle2 = angle - 0.5 * np.pi
    p1 = circle + [radius * np.cos(newAngle1), radius * np.sin(newAngle1)]
    p2 = circle + [radius * np.cos(newAngle2), radius * np.sin(newAngle2)]
    # Find which of two possible points gives shortest path
    p1length = np.linalg.norm(p1 - player) + np.linalg.norm(target - p1)
    p2length = np.linalg.norm(p2 - player) + np.linalg.norm(target - p2)
    if p1length < p2length:
        return p1
    return p2

def engage():
    FFXC = FFX_Xbox.controllerHandle()
    print("Start egg hunt")
    startTime = time.time()
    checkpoint = 0
    battleCount = 0
    lookingCount = 0
    camCount = 0
    print("Generating Plot file (the X/Y kind)")
    activeEgg = 99
    target = [10,-10]
    moveVersion = 0
    checkpoint = 0
    print("Ready for movement.")
    while FFX_memory.getStoryProgress() < 3251:
        lookingCount += 1
        if lookingCount % 40 == 0:
            checkpoint += 1
        if FFX_memory.battleActive():
            print("Battle engaged - using flee.")
            FFXC.set_neutral()
            FFX_Battle.fleeAll()
        else: #User control is different for this section.
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
                        #print("New target egg:", target)
            elif eggArray[activeEgg].goForEgg == False:
                activeEgg = 99
            elif eggArray[activeEgg].eggLife == 150:
                activeEgg = 99
            
            if activeEgg == 99: #Positions to go to if we are stalling.
                if checkpoint == 0:
                    target = [-20, -20]
                elif checkpoint == 1:
                    target = [20, -20]
                elif checkpoint == 2:
                    target = [20, 20]
                elif checkpoint >= 3:
                    target = [-20, 20]
                elif checkpoint >= 4:
                    checkpoint = 0
                #print(lookingCount, "|", target)
            
            #And now the code to move to the target.
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
                target = pathAround(playerPos, np.array(intersectPoint), targetPos) # Move around icicle instead

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

            try:
                FFXC.set_movement(Lx, Ly)
            except:
                pass
            target = oldTarget

            #camCount += 1
            #print(camCount)
            #if camCount % 20 == 0:
            #    FFX_Logs.writePlot("TEST")


            #Now if we're close, we want to slow down a bit.
            if activeEgg != 99 and eggArray[activeEgg].distance < 15 and eggArray[activeEgg].eggLife < 130:
                time.sleep(0.15)
                FFXC.set_neutral()
                #print("Studder-step to egg. | ",lookingCount)
                print("Studder-step to egg. | ",checkpoint)
                FFX_Xbox.tapB()
            elif activeEgg == 99:
                #print("Looking for a new egg. | ",lookingCount)
                print("Looking for a new egg. | ",checkpoint)
                FFX_Xbox.tapB()
            else:
                #print("Targetting egg: | ",target)
                print("Targetting egg: | ",checkpoint)
            FFX_Xbox.tapB()
    endTime = time.time()
    print("End egg hunt")
    FFXC.set_neutral()
    duration = endTime - startTime
    print("Duration:", str(duration))
    print("Battle count:", battleCount)
    while FFX_memory.getMap() != 325:
        if FFX_memory.battleActive():
            FFX_Battle.fleeAll()
    try:
        FFX_Logs.writeStats("Egg hunt duration (seconds):")
        FFX_Logs.writeStats(str(round(duration,2)))
        FFX_Logs.writeStats("Egg hunt battles:")
        FFX_Logs.writeStats(str(battleCount))
    except:
        print("No log file.")
