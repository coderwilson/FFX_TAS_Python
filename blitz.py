import xbox
import time
import memory.main
import blitzPathing
import vars
import math
import rngTrack
import logs
gameVars = vars.varsHandle()
tidusXP = False

FFXC = xbox.controllerHandle()

reportState = False
playerArray = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Initialize the player array
for i in range(12):
    playerArray[i] = memory.main.blitzActor(playerNum=i)

global engageDefender
engageDefender = False


def goersScoreFirst():
    return memory.main.diagProgressFlag() in [47, 48, 49]


def halftimeDialog():
    return memory.main.diagProgressFlag() in [45, 46]


def selectMovement():
    return memory.main.blitzMenuNum() in [145, 146]


def selectFormation():
    return memory.main.blitzMenuNum() in [122, 133]


def selectFormation2():
    return memory.main.blitzMenuNum() == 144


def selectBreakthrough():
    if (memory.main.blitzMenuNum() >= 0 and memory.main.blitzMenuNum() <= 46) or memory.main.blitzMenuNum() == 246:
        return True
    else:
        return False


def selectAction():
    return memory.main.blitzMenuNum() in [47, 52]


def selectPassTarget():
    return memory.main.blitzMenuNum() in [226, 236]


def selectShotType():
    return memory.main.blitzMenuNum() in [113, 117]


def targetedPlayer():
    retVal = memory.main.blitzTargetPlayer() - 2
    return retVal


def activeClock():
    return not memory.main.blitzClockPause()


def aurochsControl():
    return memory.main.blitzTargetPlayer() < 8


def controllingPlayer():
    retVal = memory.main.blitzCurrentPlayer() - 2
    if retVal < 200:
        return retVal
    return 1


def halfSummaryScreen():
    return memory.main.getMap() == 212


def newHalf():
    return memory.main.getMap() == 347


def halftimeSpam():
    memory.main.clickToDiagProgress(20)


def gameClock():
    return memory.main.blitzClock()


def prepHalf():
    # Map = 347, Dialog = 20
    print("Prepping for next period of play.")
    while memory.main.getMap() != 62:
        if memory.main.diagProgressFlag() == 135:  # Select game mode (Tourney, League, Exhibiton, etc)
            memory.main.waitFrames(90)
            if memory.main.savePopupCursor() != 1:
                xbox.menuDown()
                time.sleep(2)
            else:
                xbox.menuB()
                xbox.menuB()
                xbox.menuUp()
                xbox.menuB()
        elif memory.main.diagProgressFlag() in [20, 134]:
            if memory.main.blitzCharSelectCursor() != 6:
                xbox.tapA()
            else:
                xbox.menuB()
                memory.main.waitFrames(5)
        elif memory.main.diagProgressFlag() == 40:
            print("Attempting to proceed.")
            if memory.main.blitzProceedCursor() != 0:
                xbox.menuUp()
            else:
                xbox.menuB()
            memory.main.waitFrames(2)
        elif memory.main.diagProgressFlag() == 47:
            if memory.main.blitzCursor() != 0:
                xbox.menuUp()
                memory.main.waitFrames(2)
            else:
                xbox.menuB()
        elif memory.main.diagProgressFlag() == 48:
            memory.main.waitFrames(20)
            xbox.menuLeft()
            xbox.menuUp()
            xbox.menuUp()
            xbox.menuB()
        elif memory.main.diagProgressFlag() == 113:
            if memory.main.blitzCursor() != 1:
                xbox.menuUp()
                memory.main.waitFrames(2)
            else:
                xbox.menuB()
                xbox.menuB()
                time.sleep(6)
        elif memory.main.diagSkipPossible():
            xbox.menuB()
    print("Prep complete.")


def Storyline(forceBlitzWin):
    current = memory.main.getStoryProgress()
    if not gameVars.csr():
        if current == 540:
            if forceBlitzWin:
                memory.main.blitzballPatriotsStyle()
            print("Halftime hype")
            memory.main.clickToDiagProgress(164)
            memory.main.clickToDiagProgress(20)
        elif current == 560 and memory.main.diagProgressFlag() > 1:
            print("Wakka story happening.")
            memory.main.clickToDiagProgress(11)
            while not activeClock():
                xbox.tapB()
        # First half is 535
        # Hype halftime is 540
        # Second half starts on 560
        # 575 - 9


def cursor1():
    return memory.main.blitzCursor()


def jassuPassTiming() -> int:
    shotDistance = distance(0, 11)
    shotMod = int(shotDistance / 160)
    if 540 <= memory.main.getStoryProgress() < 570:
        baseTiming = int(162 - shotMod)
    else:
        baseTiming = int(270 - shotMod)

    for x in range(5):
        if distance(0, x + 6) < 180:
            baseTiming = int(baseTiming - 4)
    return baseTiming


def tidusShotTiming() -> int:
    shotDistance = distance(0, 11)
    shotMod = int(shotDistance / 160)
    if 540 < memory.main.getStoryProgress() < 570:
        baseTiming = int(170 - shotMod)
    else:
        baseTiming = int(288 - shotMod)

    for x in range(5):
        if distance(0, x + 6) < 180:
            baseTiming = int(baseTiming - 4)
    return baseTiming


def gameStage():
    # Stage 0: Killing time
    # Stage 1: Defensive, Letty dribble, consumes Jassu HP
    # Stage 2: Jassu position near the edge of the pool, look for opportunity.
    # Stage 3: Positioning Defender so Tidus can shoot/score
    # Stage 4: Pass to Tidus
    # Stage 5: Shoot for goal
    currentStage = 0
    global engageDefender
    # Logic that immediately moves to scoring phases if in overtime.
    if memory.main.getStoryProgress() > 570 and memory.main.getStoryProgress() < 700:
        if gameClock() in [2, 3, 4, 5, 6, 7]:
            gameVars.setBlitzOT(True)

    if memory.main.getStoryProgress() < 570:
        if memory.main.getStoryProgress() > 540:
            # Requires special timing before Wakka comes in
            stages = [0, 30, 90, jassuPassTiming() - 12, jassuPassTiming(), tidusShotTiming()]
        elif memory.main.getStoryProgress() < 540 and not gameVars.blitzFirstShot():
            currentStage = 20  # default 20
        else:
            currentStage = 30
    else:
        if gameVars.getBlitzOT():
            stages = [0, 2, 2, 2, 300, 300]
        else:
            #print("After Wakka")
            stages = [0, 160, 200, jassuPassTiming() - 12, jassuPassTiming(), tidusShotTiming()]

    # Determine base stage. Modified by following logic.
    if abs(memory.main.blitzOwnScore() - memory.main.blitzOppScore()) >= 2 and memory.main.getStoryProgress() >= 570:
        currentStage = 30
    elif memory.main.blitzOwnScore() - memory.main.blitzOppScore() >= 1 \
            and 570 < memory.main.getStoryProgress() < 700:
        # Ahead by 1 goal after Wakka enters, just end the game.
        currentStage = 30
    elif memory.main.getStoryProgress() < 540:
        if not gameVars.blitzFirstShot():
            currentStage = 20
        else:
            currentStage = 30
    else:
        for i in range(6):
            if stages[i] < gameClock():
                currentStage = i

        if memory.main.getStoryProgress() < 700 and currentStage >= 1:
            # Only apply following logic for the storyline game
            # Logic that updates stage based on defender movements
            if playerArray[0].getCoords()[1] - playerArray[10].getCoords()[1] > 300:
                if currentStage < 3:
                    currentStage = 4

            # Logic that reduces stage if score is too far apart.
            if memory.main.blitzOwnScore() - memory.main.blitzOppScore() >= 2 \
                    and memory.main.getStoryProgress() >= 570:
                currentStage = 0

            # Logic if we're in defensive zone trying to move forward
            if currentStage == 3 and playerArray[controllingPlayer()].getCoords()[1] < -200:
                currentStage = 2
    if currentStage == 3 and not engageDefender:
        print("Start engaging defender!")
        engageDefender = True
    elif currentStage == 2 and engageDefender:
        currentStage = 3
    elif currentStage in [0, 1, 20, 30] and engageDefender:
        print("Disengaging defender logic")
        engageDefender = False

    if currentStage < 3 and controllingPlayer() == 0:
        currentStage = 30
    return currentStage


def distanceSpecial():
    try:
        player1 = playerArray[6].getCoords()
        player2 = [222, -238]  # Formerly 230,-260
        totalDistance = (
            abs(player1[1] - player2[1]) + abs(player1[0] - player2[0]))
        return totalDistance
    except Exception as x:
        print("Exception:", x)
        return 999


def getCharRadius(playerIndex: int = 10):
    playerCoords = playerArray[playerIndex].getCoords()
    try:
        result = math.sqrt((playerCoords[0] * playerCoords[0]) + (playerCoords[1] * playerCoords[1]))
    except Exception as E:
        print("Math error, using default value.")
        print(playerCoords[0]**2)
        result = 999
    return result


def radiusMovement(radius: int = 570, direction='forward'):
    playerCoords = playerArray[controllingPlayer()].getCoords()
    targetCoords = [-400, -400]
    playerCoords[0] *= radius / getCharRadius(controllingPlayer())
    playerCoords[1] *= radius / getCharRadius(controllingPlayer())

    if 10 > playerCoords[0] > -10:
        # Too close to the center line
        playerCoords[0] = -30
    else:
        if direction == 'forward':
            targetCoords = [playerCoords[0] - 10, playerCoords[1] + 10]
        else:
            targetCoords = [playerCoords[0] - 10, playerCoords[1] - 10]
        try:
            targetCoords[0] = math.sqrt((radius**2) - (targetCoords[1]**2))
            if playerCoords[0] < -1:
                targetCoords[0] *= -1
        except:
            print("Math error, out of bounds.")
            targetCoords[0] = playerCoords[0]
        #print("Radius movement: ", targetCoords)
    blitzPathing.setMovement(targetCoords)
    return targetCoords


def workingForward():
    cPlayer = playerArray[controllingPlayer()].getCoords()
    #if distance(3,10) < 330:
    #    radiusMovement(direction='back')
    if cPlayer[1] > -180:
        #print("In position")
        blitzPathing.setMovement([-585, -130])
    else:
        radiusMovement()


def findSafePlace():
    # current player
    cPlayer = playerArray[controllingPlayer()].getCoords()
    cPlayerNum = controllingPlayer()
    # graav coords
    graavPos = playerArray[8].getCoords()
    forwardPos = playerArray[7].getCoords()
    safeSpot = 255

    # Determin target coords based on character and state.
    if cPlayerNum in [1, 4]:
        targetCoords = [520, -20]
    elif getCharRadius(controllingPlayer()) < 450:
        radiusMovement(radius=480, direction='back')
    elif cPlayerNum in [2, 3]:
        if playerArray[9].getCoords()[1] < 150:
            safeSpot = 3
        elif graavPos[1] < -20 and cPlayer[1] > -500 and distance(cPlayerNum, 8) > 370 and distance(cPlayerNum, 10) > 370:
            if cPlayer[0] > graavPos[0]:
                safeSpot = 1
            else:
                safeSpot = 2
        elif forwardPos[1] > 250:
            safeSpot = 2
        else:
            safeSpot = 3
    else:  # Should never occur, should never get Tidus/Wakka into this logic.
        safeSpot = 3

    if safeSpot == 1:  # Near the left wall
        targetCoords = [-521, -266]
    elif safeSpot == 2:  # About half way
        targetCoords = [-380, -550]
    elif safeSpot == 3:  # All the way back
        targetCoords = [-2, -595]

    # I think this is still the best option.
    #targetCoords = [-2, -595]

    if blitzPathing.setMovement(targetCoords):
        return True
    else:
        return False


def jassuCircle():
    radius = 540
    jassuCoords = playerArray[3].getCoords()
    if jassuCoords[0] > 150:  # Upper section
        version = "A"
        if distance(3, 6) < 500 and not playerArray[6].aggro():
            tarPlayer = playerArray[8].getCoords()
            if tarPlayer[1] - jassuCoords[1] > 300:
                nextX = tarPlayer[0]
                nextY = tarPlayer[1] - 280
            else:
                nextX = tarPlayer[0] - 200
                nextY = tarPlayer[1] - 100
        else:
            nextY = jassuCoords[1] + 30
            nextX = abs(math.sqrt((radius * radius) - (jassuCoords[1] * jassuCoords[1])))
            if nextX < jassuCoords[0]:
                nextX = jassuCoords[0] + 50
    elif jassuCoords[0] < -150:  # Lower section
        version = "C"
        nextY = jassuCoords[1] - 20
        nextX = math.sqrt((radius * radius) - (jassuCoords[1] * jassuCoords[1]))
        nextX *= -1
    elif jassuCoords[1] < -100:  # Near own goal
        version = "D"
        nextX = jassuCoords[0] + 100
        nextY = jassuCoords[1]
    else:  # Near opponent goal
        version = "B"

    targetCoords = [int(nextX), int(nextY)]
    blitzPathing.setMovement(targetCoords)
    return [version, nextX, nextY]


def jassuTrain():
    targetCoords = [0, -600]
    if reportState:
        print(version[0], " - ", targetCoords)
    blitzPathing.setMovement(targetCoords)


def jassuTrain_stillInDev():
    jassuCoords = playerArray[3].getCoords()
    version = "None"
    useCircle = False
    radius = 540
    bufferLeft = -90
    bufferRight = -200
    nextX = jassuCoords[0] - 20
    if not playerArray[8].aggro() and not playerArray[6].aggro():
        nextX = -2
        nextY = -595
    elif jassuCoords[1] < bufferRight:
        # Defensive zone
        if not playerArray[6].aggro():
            nextX = playerArray[6].getCoords()[0]
            nextY = playerArray[6].getCoords()[1] - 130
            version = "6"
        elif playerArray[9].getCoords()[1] > jassuCoords[1] + 150 and distance(3, 9) < 400:
            tarPlayer = playerArray[9].getCoords()
            nextY = tarPlayer[1] - 200
            nextX = tarPlayer[0] - 100
            version = "9"
        elif math.sqrt((jassuCoords[0] * jassuCoords[0]) + (jassuCoords[1] * jassuCoords[1])) < 480:
            # Too close to center. Get to own goal near full radius.
            if jassuCoords[1] > -300:
                nextX = -10
                nextY = -310
            else:
                nextX = 100
                nextY = -500
            version = "E"
        else:
            version = jassuCircle()
            useCircle = True
    elif not playerArray[6].aggro():
        tarPlayer = playerArray[6].getCoords()
        nextY = tarPlayer[1] - 300
        nextX = tarPlayer[0] + 100
        version = "6"
    elif playerArray[8].getCoords()[1] > jassuCoords[1] + 150 and distance(3, 8) < 400:
        tarPlayer = playerArray[8].getCoords()
        nextY = tarPlayer[1] - 300
        nextX = tarPlayer[0] - 100
        version = "8"
    elif playerArray[8].getCoords()[0] < jassuCoords[0] - 150 and distance(3, 8) < 400:
        tarPlayer = playerArray[8].getCoords()
        nextY = tarPlayer[1] - 300
        nextX = tarPlayer[0] - 100
        version = "8"
    elif playerArray[7].getCoords()[0] < jassuCoords[0] - 100 and distance(3, 7) < 600:
        tarPlayer = playerArray[7].getCoords()
        nextY = tarPlayer[1] - 300
        nextX = tarPlayer[0] + 150
        version = "7"
    elif playerArray[10].getCoords()[1] > jassuCoords[1] + 150 and distance(3, 10) < 400:
        tarPlayer = playerArray[10].getCoords()
        nextY = tarPlayer[1] - 300
        nextX = tarPlayer[0] - 100
        version = "10"
    elif jassuCoords[0] < -450 and jassuCoords[1] > bufferRight - 5:
        nextY = bufferRight - 10
        nextX = math.sqrt((radius * radius) - (nextY * nextY)) * -1
        version = "L"
    elif jassuCoords[1] >= bufferRight and jassuCoords[1] < bufferLeft:
        # Buffer zone
        nextX = jassuCoords[0] - 20
        if jassuCoords[0] > 100:
            nextY = jassuCoords[1] + 40
        elif jassuCoords[0] < -300:
            nextX = jassuCoords[0] - 40
            nextY = jassuCoords[1] - 40
        else:
            nextY = jassuCoords[1]
        version = "F"
    else:
        nextX = jassuCoords[0] - 500
        nextY = jassuCoords[1]
        version = "T"

    if not useCircle:
        targetCoords = [int(nextX), int(nextY)]
        if reportState:
            print(version[0], " - ", targetCoords)
        blitzPathing.setMovement(targetCoords)
    else:
        if reportState:
            print(version)


def passBall(target=0, breakThrough=5):
    if controllingPlayer() == 4:
        breakThrough = 0
    if selectBreakthrough():
        if breakThrough == 5:
            if cursor1() == 0:
                xbox.menuUp()
                memory.main.waitFrames(1)
            else:
                xbox.menuB()
        else:
            xbox.menuB()
    elif selectAction():
        if cursor1() != 0:  # Pass command
            xbox.menuDown()
            memory.main.waitFrames(3)
        else:
            xbox.menuB()
    elif selectPassTarget():
        while not activeClock():
            if targetedPlayer() != target:
                xbox.menuDown()
            else:
                xbox.tapB()
    else:
        xbox.menuB()


def shootBall(breakThrough=5):
    if memory.main.getStoryProgress() < 570 and controllingPlayer() == 0:
        if gameClock() > 167:
            breakThrough = 5
        else:
            breakThrough = 0
    else:
        breakThrough = 5
    if selectShotType():
        if cursor1() == 1:
            xbox.menuB()
        else:
            xbox.menuDown()
            memory.main.waitFrames(3)
    elif selectBreakthrough():
        if breakThrough == 5:
            if cursor1() == 0:
                xbox.menuUp()
                memory.main.waitFrames(1)
            else:
                xbox.menuB()
                xbox.menuB()
        else:
            xbox.menuB()
            xbox.menuB()
    elif selectAction():
        if cursor1() != 1:  # Shoot
            xbox.menuDown()
            memory.main.waitFrames(3)
        else:
            xbox.menuB()
        gameVars.blitzFirstShotTaken()


def dribbleBall():
    if selectBreakthrough():
        if cursor1() == 0:
            xbox.menuUp()
            memory.main.waitFrames(2)
        else:
            xbox.menuB()
    elif selectAction():
        if cursor1() != 2:
            xbox.menuUp()
            memory.main.waitFrames(3)
        else:
            xbox.menuB()


def playerGuarded(playerNum):
    # Graav proximity always counts as guarded.
    if distance(playerNum, 8) < 360:
        return True

    # Two or more player proximity always counts as guarded.
    otherDistance = 0
    if distance(0, 6) < 360:
        otherDistance += 1
    if distance(0, 7) < 360:
        otherDistance += 1
    if distance(0, 9) < 360:
        otherDistance += 1
    if distance(0, 10) < 360:
        otherDistance += 1
    if otherDistance >= 2:
        return True

    # Specific cases depending on player.
    if playerNum in [3, 4]:
        if distance(playerNum, 9) < 340:
            return True
        if distance(playerNum, 10) < 340:
            return True
    return False


def tidusMove():
    currentStage = gameStage()
    if reportState:
        print("Tidus movement")
    graavDistance = distance(0, 8)

    otherDistance = 0
    if distance(0, 6) < 180:
        otherDistance += 1
    if distance(0, 7) < 180:
        otherDistance += 1
    if distance(0, 9) < 180:
        otherDistance += 1
    if distance(0, 10) < 180:
        otherDistance += 1

    shootTarget = [-170, 540]

    if currentStage > 15:
        radiusMovement(radius=400, direction='back')
        if distance(0, 3) < 330:
            xbox.tapX()
    elif memory.main.getStoryProgress() > 700:
        if otherDistance >= 2:
            xbox.tapX()
        elif currentStage == 4:
            xbox.tapX()
        elif blitzPathing.setMovement(shootTarget):
            xbox.tapX()
    elif currentStage in [0, 1, 2, 5]:
        FFXC.set_movement(-1, -1)
        xbox.tapX()
    elif currentStage == 4:
        if graavDistance < 240:
            # Graav too close.
            FFXC.set_movement(-1, -1)
            xbox.tapX()
        elif otherDistance >= 2:
            # Too many players closing in.
            FFXC.set_movement(-1, -1)
            xbox.tapX()
        elif blitzPathing.setMovement(shootTarget) and memory.main.getStoryProgress() >= 570:
            FFXC.set_movement(-1, -1)
            xbox.tapX()
    else:  # stages 3 and 4 only. All other stages we try to pass, or just shoot.
        if playerArray[0].getCoords()[1] > 470:  # Force shot
            FFXC.set_movement(-1, -1)
            xbox.tapX()
        else:
            radiusMovement(radius=570, direction='forward')


def tidusAct():
    currentStage = gameStage()
    if reportState:
        print("Tidus act")

    otherDistance = 0
    if distance(0, 6) < 280:
        otherDistance += 1
    if distance(0, 7) < 280:
        otherDistance += 1
    if distance(0, 9) < 280:
        otherDistance += 1
    if distance(0, 10) < 280:
        otherDistance += 1

    if currentStage > 15:
        passBall(target=3)
        gameVars.blitzFirstShotTaken()
    elif memory.main.getStoryProgress() > 700:
        shootBall(breakThrough=0)
    elif currentStage in [4, 5]:
        # Late on the timer. Shoot at all costs.
        if memory.main.getStoryProgress() < 540:
            print("First half, shooting without breakthrough.")
            shootBall(breakThrough=0)
        else:
            print("Stage 5 - shoot the ball!")
            shootBall(breakThrough=0)
    elif currentStage in [0, 1, 2]:
        # Early game. Try to get the ball to Jassu.
        if distance(0, 3) < 350:
            passBall(target=3)
            gameVars.blitzFirstShotTaken()
        elif distance(0, 2) < 350:
            passBall(target=2)
            gameVars.blitzFirstShotTaken()
        else:
            shootBall()
    else:
        shootBall(breakThrough=0)


def lettyMove():
    if reportState:
        print("Letty movement")
    currentStage = gameStage()
    graavDistance = distance(2, 8)

    if currentStage == 20:
        findSafePlace()
        if distance(0, 8) > 400 and distance(0, 10) > 400:
            xbox.tapX()
        else:
            findSafePlace()
    elif currentStage == 30:
        findSafePlace()
        xbox.tapX()
    elif currentStage >= 3:
        FFXC.set_movement(1, 0)
        xbox.tapX()
    elif currentStage == 2:
        targetCoords = [-20, -585]
        blitzPathing.setMovement(targetCoords)
        if not playerGuarded(3):
            xbox.tapX()
        elif not playerGuarded(2):
            xbox.tapX()
    elif currentStage == 1:
        #if not playerGuarded(3) and distance(3, 10) > 380 and graavDistance > 380:
        if distance(3, 8) < 360:
            xbox.tapX()
        else:
            if findSafePlace() and graavDistance < 320:
                xbox.tapX()
    elif gameVars.blitzFirstShot():
        findSafePlace()
    else:
        if distance(3, 8) < 340 or distance(3, 7) < 340:
            if findSafePlace() and graavDistance < 280:
                xbox.tapX()
        elif playerArray[2].currentHP() < 10:
            print("Letty out of HP. Passing to Jassu.")
            xbox.tapX()
        else:
            findSafePlace()


def lettyAct():
    currentStage = gameStage()
    graavDistance = distance(0, 2)

    if currentStage == 20:
        if distance(0, 8) > 400:
            passBall(target=0)
        else:
            dribbleBall()
    elif currentStage == 30:
        passBall(target=3)
    elif memory.main.getStoryProgress() > 700:  # Post-storyline blitzball only
        if playerArray[0].getCoords()[1] > playerArray[1].getCoords()[1]:
            passBall(target=0, breakThrough=0)
        else:
            passBall(target=1, breakThrough=0)
    elif currentStage >= 4:
        passBall(target=0)
        if reportState:
            print("Letty Action 1")
    elif currentStage == 3:
        passBall(target=3)
        if reportState:
            print("Letty Action 2")
    elif playerArray[2].currentHP() < 10:
        passBall(target=3)
    elif currentStage == 2:
        if distance(2, 8) < 250:
            breakThroughVal = 5
        else:
            breakThroughVal = 0

        if not playerGuarded(3):
            tar = 3
        elif not playerGuarded(0):
            tar = 0
        else:
            tar = 3
        passBall(target=tar, breakThrough=breakThroughVal)
    elif currentStage in [0, 1]:
        print("Letty pass to Jassu")
        passBall(target=3)
    elif gameVars.blitzFirstShot():
        dribbleBall()
    elif playerArray[2].currentHP() < 10:
        if playerGuarded(3):
            dribbleBall()
        else:
            passBall(target=3)
    else:
        dribbleBall()
        if reportState:
            print("Letty Action 5")


def jassuMove():
    currentStage = gameStage()
    playerCoords = playerArray[controllingPlayer()].getCoords()
    targetCoords = [-585, -130]
    p10C = playerArray[10].getCoords()
    graavC = playerArray[8].getCoords()
    tidusC = playerArray[0].getCoords()
    findSafety = False
    moveForward = False
    graavDistance = distance(3, 8)
    otherDistance = 0
    targetCoords = [-600, -100]
    if distance(3, 6) < 350:
        otherDistance += 1
    if distance(3, 7) < 350:
        otherDistance += 1
    if distance(3, 9) < 350:
        otherDistance += 1
    if distance(3, 10) < 350:
        otherDistance += 1

    if currentStage == 20:
        findSafePlace()
        if distance(0, 8) > 300 and distance(0, 10) > 360:
            if playerArray[9].getCoords()[1] > 100:
                xbox.tapX()
    elif currentStage == 30:
        #jassuTrain()
        findSafePlace()
        moveForward = True
    elif currentStage <= 1 and playerArray[3].currentHP() < 10:
        if playerArray[2].currentHP() >= 40 and distance(2, 8) > 360:
            xbox.tapX()
        elif graavDistance < 320:
            xbox.tapX()
        else:
            findSafety = True
    elif currentStage == 0:
        # Defend in the goal for safety.
        findSafety = True
        if playerArray[2].currentHP() >= 40 and currentStage == 0:
            if distance(2, 8) > 360 and distance(2, 7) > 360 and distance(2, 6) > 360:
                xbox.tapX()
    elif currentStage == 1:
        if playerArray[10].getCoords()[1] < 150:
            findSafePlace()
        elif distance(3, 8) < 350:
            findSafePlace()
        else:
            workingForward()
        moveForward = True
    elif currentStage == 2:
        # Move forward to staging position, prep for shot.
        workingForward()
        moveForward = True
    elif currentStage == 3:
        relDist = int((tidusC[1] - p10C[1]) + (tidusC[0] - p10C[0]))
        relDist2 = int((tidusC[1] - graavC[1]) + (tidusC[0] - graavC[0]))
        if relDist > 220:  # Tidus in position behind defender
            xbox.tapX()
            moveForward = True
        elif distance(3, 10) > 340:
            moveRadius = min(int(getCharRadius() + 150), 570)
            targetCoords = radiusMovement(radius=moveRadius, direction='forward')
            moveForward = True
        else:
            moveRadius = min(int(getCharRadius() + 150), 570)
            targetCoords = radiusMovement(radius=moveRadius, direction='back')
            moveForward = True
    else:  # Pass to Tidus
        targetCoords = [p10C[0] - 180, p10C[1] - 150]
        xbox.tapX()

    if currentStage < 15:
        if findSafety:
            if findSafePlace() and graavDistance < 320:
                xbox.tapX()
        elif not moveForward:
            try:
                blitzPathing.setMovement(targetCoords)
            except:
                pass


def jassuAct():
    currentStage = gameStage()
    playerCoords = playerArray[controllingPlayer()].getCoords()
    targetCoords = [-585, -130]
    p10C = playerArray[10].getCoords()
    graavC = playerArray[8].getCoords()
    tidusC = playerArray[0].getCoords()
    findSafety = False
    targetCoords = [-600, -100]
    currentStage = gameStage()
    if reportState:
        print("Jassu Action")
        print("Stage:", currentStage)
    graavDistance = distance(3, 8)
    otherDistance = 0
    if distance(3, 6) < 350:
        otherDistance += 1
    if distance(3, 7) < 350:
        otherDistance += 1
    if distance(3, 9) < 350:
        otherDistance += 1
    if distance(3, 10) < 350:
        otherDistance += 1

    if currentStage == 20:
        if distance(0, 8) > 280:
            passBall(0)
        else:
            dribbleBall()
    elif currentStage == 30:
        dribbleBall()
    elif currentStage == 0:
        if playerArray[2].currentHP() >= 40 and distance(2, 8) > 360:
            passBall(target=2)
        else:
            dribbleBall()
    elif currentStage == 1:
        dribbleBall()
    elif playerArray[3].currentHP() < 10:
        passBall(target=0)
    elif currentStage == 2:
        dribbleBall()
    elif currentStage == 3:
        relDist = int((tidusC[1] - p10C[1]) + (tidusC[0] - p10C[0]))
        relDist2 = int((tidusC[1] - graavC[1]) + (tidusC[0] - graavC[0]))
        if relDist > 220:
            passBall(target=0)
        elif graavDistance < 150:
            # Graav too close
            passBall(target=0)
        elif playerArray[0].getCoords()[1] - playerArray[10].getCoords()[1] > 280:
            # Tidus in position for break-away.
            passBall(target=0)
        else:
            dribbleBall()
    else:  # Pass to Tidus
        passBall(target=0)


def otherMove():  # fix
    if getCharRadius(controllingPlayer()) < 540:
        FFXC.set_movement(0, 1)
    elif playerArray[controllingPlayer()].getCoords()[1] < -400:
        xbox.tapX()
    elif distance(controllingPlayer(), 8) < 300:
        xbox.tapX()
    else:
        radiusMovement(radius=570, direction='back')


def otherAct():
    currentStage = gameStage()

    if reportState:
        print("Botta/Datto action")
        print("Stage:", currentStage)

    if memory.main.getStoryProgress() > 700:
        if controllingPlayer() == 1:
            shootBall()
        else:
            if playerArray[0].getCoords()[1] > playerArray[1].getCoords()[1]:
                passBall(target=2, breakThrough=0)
            else:
                passBall(target=3, breakThrough=0)
    elif distance(controllingPlayer(), 8) < 300:
        passBall(target=2)
    else:
        passBall(target=3)


def blitzMovement():
    updatePlayerArray()

    if controllingPlayer() == 0:
        tidusMove()
    elif controllingPlayer() == 2:
        lettyMove()
    elif controllingPlayer() == 3:
        jassuMove()
    else:
        otherMove()


def decideAction():
    FFXC = xbox.controllerHandle()
    FFXC.set_neutral()
    updatePlayerArray()
    if controllingPlayer() == 0:
        tidusAct()
    elif controllingPlayer() == 2:
        lettyAct()
    elif controllingPlayer() == 3:
        jassuAct()
    else:
        otherAct()


def distance(n1, n2):
    try:
        player1 = playerArray[n1].getCoords()
        player2 = playerArray[n2].getCoords()
        return (abs(player1[1] - player2[1]) + abs(player1[0] - player2[0]))
    except Exception as x:
        print("Exception:", x)
        return 999


def updatePlayerArray():
    for i in range(12):
        playerArray[i].updateCoords()


def blitzMain(forceBlitzWin):
    print("-Start of Blitzball program")
    print("-First, clicking to the start of the match.")
    memory.main.clickToStoryProgress(535)
    print("-Match is now starting.")
    startTime = logs.timeStamp()

    FFXC = xbox.controllerHandle()
    gameVars.blitzFirstShotReset()
    movementSetFlag = False
    lastState = 0
    lastMenu = 0
    lastPhase = 99
    while memory.main.getStoryProgress() < 582 or memory.main.getStoryProgress() > 700:  # End of Blitz
        try:
            if lastPhase != gameStage() and gameClock() > 0 and gameClock() < 301:
                lastPhase = gameStage()
                print("------------------------------")
                print("New phase reached.", lastPhase)
                print("------------------------------")
            if goersScoreFirst() or halftimeDialog():
                if lastMenu != 3:
                    print("Dialog on-screen")
                    lastMenu = 3
                FFXC.set_neutral()
                xbox.menuB()
            if memory.main.getMap() == 62:
                if activeClock():
                    if lastState != 1:
                        print("Clock running.")
                        lastState = 1
                    if aurochsControl():
                        if lastMenu != 2:
                            #print("Camera focusing Aurochs player")
                            lastMenu = 2
                        if not movementSetFlag:
                            xbox.tapY()
                        else:
                            blitzMovement()
                    else:
                        if lastMenu != 8:
                            #print("Camera focusing opposing player")
                            lastMenu = 8
                else:
                    FFXC.set_neutral()
                    if lastState != 2:
                        print("Menu should be coming up")
                        lastState = 2
                    if selectMovement():
                        if lastMenu != 4:
                            print("Selecting movement method")
                            lastMenu = 4
                        if cursor1() == 1:
                            xbox.menuB()
                            movementSetFlag = True
                        else:
                            xbox.menuDown()
                            print(cursor1())
                    elif selectFormation():
                        if lastMenu != 5:
                            print("Selecting Formation")
                            lastMenu = 5
                        if cursor1() == 0:
                            xbox.menuB()
                        else:
                            xbox.menuUp()
                    elif selectFormation2():
                        if lastMenu != 5:
                            print("Selecting Formation")
                            lastMenu = 5
                        if cursor1() == 7:
                            xbox.menuB()
                        else:
                            xbox.menuUp()
                    elif selectBreakthrough():
                        if lastMenu != 6:
                            print("Selecting Break-through")
                            memory.main.waitFrames(2)
                            lastMenu = 6
                        decideAction()
                    elif selectPassTarget():
                        if lastMenu != 11:
                            print("Selecting pass target.")
                            lastMenu = 11
                        decideAction()
                    elif selectShotType():
                        if lastMenu != 12:
                            print("Selecting shot type")
                            lastMenu = 12
                        if cursor1() == 1:
                            xbox.menuB()
                        else:
                            xbox.menuDown()
                            memory.main.waitFrames(3)
                    elif selectAction():
                        if lastMenu != 7:
                            print("Selecting action (Shoot/Pass/Dribble)")
                            lastMenu = 7
                        decideAction()
            else:
                FFXC.set_neutral()
                if lastState != 3:
                    print("Screen outside the Blitz sphere")
                    lastState = 3
                if halfSummaryScreen():
                    if memory.main.diagProgressFlag() == 113:
                        if cursor1() != 1:  # Pass command
                            xbox.menuDown()
                            memory.main.waitFrames(3)
                        else:
                            xbox.menuB()
                    elif memory.main.diagSkipPossible():  # Skip through everything else
                        xbox.menuB()
                elif newHalf():
                    if forceBlitzWin:
                        memory.main.blitzballPatriotsStyle()
                    if memory.main.diagProgressFlag() == 347:
                        # Used for repeated Blitz games, not for story.
                        movementSetFlag = False
                    prepHalf()
                else:
                    Storyline(forceBlitzWin)
        except Exception as xVal:
            print("Caught exception in blitz memory.main.:")
            print(xVal)

    print("Blitz game has completed.")
    # Set the blitzWin flag for the rest of the run.
    print("Final scores: Aurochs:", memory.main.blitzOwnScore(),
          ", Opponent score:", memory.main.blitzOppScore())
    FFXC.set_neutral()
    if memory.main.blitzOwnScore() > memory.main.blitzOppScore():
        gameVars.setBlitzWin(True)
    else:
        gameVars.setBlitzWin(False)

    endTime = logs.timeStamp()
    timeDiff = endTime - startTime
    totalTime = int(timeDiff.total_seconds())
    rngTrack.recordBlitzResults(duration=totalTime)
    print("--Blitz Win value:", gameVars.getBlitzWin())
