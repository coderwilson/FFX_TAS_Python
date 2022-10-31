import time
from math import copysign

import numpy as np

import battle.main
import logs
import memory.main
import xbox


def line_sphere_intersect(start, end, circle, radius=11):
    numHits = 0
    hits = []

    direction = end - start
    sphereToStart = start - circle
    a = np.dot(direction, direction)
    b = 2 * np.dot(sphereToStart, direction)
    c = np.dot(sphereToStart, sphereToStart) - radius**2
    d = b**2 - 4 * a * c
    if d < 0:  # no intersection
        return (numHits, hits)

    d = np.sqrt(d)
    # Solve quadratic equation
    t1 = (-b - d) / (2 * a)
    t2 = (-b + d) / (2 * a)

    if t1 >= 0 and t1 <= 1:
        numHits += 1
        hits.append(start + direction * t1)
    if t2 >= 0 and t2 <= 1:
        numHits += 1
        hits.append(start + direction * t2)
    return (numHits, hits)


def path_around(player, circle, target, radius=11):
    line = player - circle
    line /= np.linalg.norm(line)  # normalize to length 1
    angle = np.arctan2(line[1], line[0])

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
    FFXC = xbox.controller_handle()
    print("Start egg hunt")
    start_time = time.time()
    checkpoint = 0
    battleCount = 0
    lookingCount = 0
    print("Generating Plot file (the X/Y kind)")
    activeEgg = 99
    target = [10, -10]
    checkpoint = 0
    print("Ready for movement.")
    while memory.main.get_story_progress() < 3251:
        lookingCount += 1
        if lookingCount % 40 == 0:
            checkpoint += 1
        if memory.main.battle_active():
            print("Battle engaged - using flee.")
            FFXC.set_neutral()
            battle.main.flee_all()
            battleCount += 1
        else:  # User control is different for this section.
            eggArray = memory.main.build_eggs()
            iceArray = memory.main.build_icicles()  # Added for additional pathing needs
            if activeEgg == 99:
                for marker in range(10):  # Only print active eggs/icicles
                    if (
                        activeEgg == 99
                        and eggArray[marker].goForEgg
                        and eggArray[marker].eggLife < 150
                    ):
                        activeEgg = marker
                        target = [eggArray[marker].x, eggArray[marker].y]
                        # We will hunt for this egg for this many seconds.
            elif not eggArray[activeEgg].goForEgg:
                activeEgg = 99
            elif eggArray[activeEgg].eggLife == 150:
                activeEgg = 99

            if activeEgg == 99:  # Positions to go to if we are stalling.
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

            # And now the code to move to the target.
            oldTarget = target
            player = memory.main.get_coords()
            iceArray = memory.main.build_icicles()
            (forward, right) = memory.main.get_movement_vectors()

            targetPos = np.array([target[0], target[1]])
            playerPos = np.array(player)

            closestIntersect = 9999
            intersectPoint = []
            for icicle in iceArray:
                numIntersect, hits = line_sphere_intersect(
                    playerPos, targetPos, np.array([icicle.x, icicle.y])
                )
                if numIntersect > 0:
                    intersectDistance = (player[0] - hits[0][0]) ** 2 + (
                        player[1] - hits[0][1]
                    ) ** 2
                    if intersectDistance < closestIntersect:
                        closestIntersect = intersectDistance
                        intersectPoint = hits[0]

            if closestIntersect < 9999:
                # Move around icicle instead
                target = path_around(playerPos, np.array(intersectPoint), targetPos)

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
            sumsUp = abs(Lx) + abs(Ly)
            if sumsUp == 0:
                sumsUp = 0.01
            Lx /= sumsUp
            Ly /= sumsUp
            if abs(Lx) > abs(Ly):
                Ly = copysign(Ly / Lx if Lx else 0, Ly)
                Lx = copysign(1, Lx)
            elif abs(Ly) > abs(Lx):
                Lx = copysign(Lx / Ly if Ly else 0, Lx)
                Ly = copysign(1, Ly)

            try:
                FFXC.set_movement(Lx, Ly)
            except Exception:
                pass
            target = oldTarget

            # Now if we're close, we want to slow down a bit.
            if (
                activeEgg != 99
                and eggArray[activeEgg].distance < 15
                and eggArray[activeEgg].eggLife < 130
            ):
                time.sleep(0.15)
                FFXC.set_neutral()
                print("Stutter-step to egg. |", checkpoint)
                xbox.tap_b()
            elif activeEgg == 99:
                print("Looking for a new egg. |", checkpoint)
                xbox.tap_b()
            else:
                print("Targeting egg: |", checkpoint)
            xbox.tap_b()
    end_time = time.time()
    print("End egg hunt")
    FFXC.set_neutral()
    duration = end_time - start_time
    print("Duration:", str(duration))
    print("Battle count:", battleCount)
    while memory.main.get_map() != 325:
        if memory.main.battle_active():
            battle.main.flee_all()
    try:
        logs.write_stats("Egg hunt duration (seconds):")
        logs.write_stats(str(round(duration, 2)))
        logs.write_stats("Egg hunt battles:")
        logs.write_stats(str(battleCount))
    except Exception:
        print("No log file.")
