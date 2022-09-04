import FFX_Xbox
import time
import FFX_Logs
import FFX_memory
import FFX_blitzPathing
import FFX_vars
import math
import FFX_rngTrack
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

reportState = False
playerArray = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#trainTurn = 0

# Initialize the player array
for i in range(12):
    playerArray[i] = FFX_memory.blitzActor(playerNum=i)


def goersScoreFirst():
    return FFX_memory.diagProgressFlag() in [47, 48, 49]


def halftimeDialog():
    return FFX_memory.diagProgressFlag() in [45, 46]


def selectMovement():
    return FFX_memory.blitzMenuNum() in [145, 146]


def selectFormation():
    return FFX_memory.blitzMenuNum() in [122, 133]


def selectFormation2():
    return FFX_memory.blitzMenuNum() == 144


def selectBreakthrough():
    if (FFX_memory.blitzMenuNum() >= 0 and FFX_memory.blitzMenuNum() <= 46) or FFX_memory.blitzMenuNum() == 246:
        return True
    else:
        return False


def selectAction():
    return FFX_memory.blitzMenuNum() in [47, 52]


def selectPassTarget():
    return FFX_memory.blitzMenuNum() in [226, 236]


def selectShotType():
    return FFX_memory.blitzMenuNum() in [113, 117]


def targetedPlayer():
    retVal = FFX_memory.blitzTargetPlayer() - 2
    #print("++", retVal)
    return retVal


def activeClock():
    return not FFX_memory.blitzClockPause()


def aurochsControl():
    return FFX_memory.blitzTargetPlayer() < 8


def controllingPlayer():
    #print(FFX_memory.blitzCurrentPlayer() - 2)
    retVal = FFX_memory.blitzCurrentPlayer() - 2
    if retVal < 200:
        return retVal
    return 1


def halfSummaryScreen():
    return FFX_memory.getMap() == 212


def newHalf():
    return FFX_memory.getMap() == 347


def halftimeSpam():
    FFX_memory.clickToDiagProgress(20)


def gameClock():
    return FFX_memory.blitzClock()


def prepHalf():
    # Map = 347, Dialog = 20
    print("Prepping for next period of play.")
    while FFX_memory.getMap() != 62:
        if FFX_memory.diagProgressFlag() == 135:  # Select game mode (Tourney, League, Exhibiton, etc)
            FFX_memory.waitFrames(90)
            if FFX_memory.savePopupCursor() != 1:
                FFX_Xbox.menuDown()
                time.sleep(2)
            else:
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
        elif FFX_memory.diagProgressFlag() in [20, 134]:
            if FFX_memory.blitzCharSelectCursor() != 6:
                FFX_Xbox.tapA()
            else:
                FFX_Xbox.menuB()
                FFX_memory.waitFrames(5)
        elif FFX_memory.diagProgressFlag() == 40:
            print("Attempting to proceed.")
            if FFX_memory.blitzProceedCursor() != 0:
                FFX_Xbox.menuUp()
            else:
                FFX_Xbox.menuB()
            FFX_memory.waitFrames(2)
        elif FFX_memory.diagProgressFlag() == 47:
            if FFX_memory.blitzCursor() != 0:
                FFX_Xbox.menuUp()
                FFX_memory.waitFrames(2)
            else:
                FFX_Xbox.menuB()
        elif FFX_memory.diagProgressFlag() == 48:
            FFX_memory.waitFrames(20)
            FFX_Xbox.menuLeft()
            FFX_Xbox.menuUp()
            FFX_Xbox.menuUp()
            FFX_Xbox.menuB()
        elif FFX_memory.diagProgressFlag() == 113:
            if FFX_memory.blitzCursor() != 1:
                FFX_Xbox.menuUp()
                FFX_memory.waitFrames(2)
            else:
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()
                time.sleep(6)
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
    print("Prep complete.")


def Storyline(forceBlitzWin):
    current = FFX_memory.getStoryProgress()
    if not gameVars.csr():
        if current == 540:
            if forceBlitzWin:
                FFX_memory.blitzballPatriotsStyle()
            print("Halftime hype")
            FFX_memory.clickToDiagProgress(164)
            FFX_memory.clickToDiagProgress(20)
        elif current == 560 and FFX_memory.diagProgressFlag() > 1:
            print("Wakka story happening.")
            FFX_memory.clickToDiagProgress(11)
            while not activeClock():
                FFX_Xbox.tapB()
        #First half is 535
        #Hype halftime is 540
        #Second half starts on 560
        #575 - 9


def cursor1():
    return FFX_memory.blitzCursor()


def tidusShotTiming() -> int:
    baseTiming = int(170)
    for x in range(5):
        if distance(0, x+6) < 180:
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
    if FFX_memory.getStoryProgress() < 570:  # Second half, before Tidus/Wakka swap
        #stages = [0, 110, 110, 140, 159, tidusShotTiming()]
        if FFX_memory.rngSeed() == 31:
            stages = [0, 2, 115, 144, 157, tidusShotTiming()]
            # previously 141 for defender manip, 157 for force pass to Tidus.
        else:
            stages = [0, 2, 2, 142, 155, tidusShotTiming()]
    elif FFX_memory.getStoryProgress() < 700 and not gameVars.getBlitzOT():  # End of the storyline game
        stages = [0, 2, 2, 264, 278, 278]
        #stages = [0, 6, 6, 264, 278, 278]
    else:  # Overtime
        #stages = [0, 0, 0, 0, 0, 270]
        if playerArray[controllingPlayer()].getCoords()[1] < 40:
            stages = [0, 2, 2, 300, 300, 300]
        else:
            stages = [0, 2, 2, 10, 10, 278]

    # Determine base stage. Modified by following logic.
    if FFX_memory.getStoryProgress() < 540:
        # First half logic for the storyline game uses different logic.
        if gameVars.blitzFirstShot():
            currentStage = 30  # default 20
        else:
            currentStage = 20  # default 20
    elif abs(FFX_memory.blitzOwnScore() - FFX_memory.blitzOppScore()) >= 2:
        currentStage = 30
    elif abs(FFX_memory.blitzOwnScore() - FFX_memory.blitzOppScore()) >= 1 \
            and FFX_memory.getStoryProgress() > 570 \
            and FFX_memory.getStoryProgress() < 700:
        currentStage = 30
    else:
        for i in range(6):
            if stages[i] < gameClock():
                currentStage = i

        if FFX_memory.getStoryProgress() < 700 and currentStage >= 1:
            # Only apply following logic for the storyline game
            # Logic that updates stage based on defender movements
            if playerArray[0].getCoords()[1] - playerArray[10].getCoords()[1] > 300:
                if currentStage < 3:
                    currentStage = 4

            # Logic that reduces stage if score is too far apart.
            if FFX_memory.blitzOwnScore() - FFX_memory.blitzOppScore() >= 1 \
                    and FFX_memory.getStoryProgress() >= 570:
                currentStage = 0

            # Logic that immediately moves to scoring phases if in overtime.
            if FFX_memory.getStoryProgress() >= 570 and FFX_memory.getStoryProgress() < 700:
                if gameClock() < 20 and not gameVars.getBlitzOT():
                    gameVars.setBlitzOT(True)
            if gameVars.getBlitzOT() and currentStage < 3:
                currentStage = 3

            # Logic if we're in defensive zone trying to move forward
            if currentStage == 3 and playerArray[controllingPlayer()].getCoords()[1] < -200:
                currentStage = 2

            # Finally, if the defender is too far forward
            # if (playerArray[10].getCoords()[0] < -350 or playerArray[10].getCoords()[1] < 200) \
            #    and currentStage == 2:
            #    currentStage = 3

    if currentStage < 3 and controllingPlayer() == 0:
        currentStage = 30
    # if reportState:
    #    print("Stage:", currentStage)
    return currentStage


def distanceSpecial():
    try:
        player1 = playerArray[6].getCoords()
        player2 = [222, -238]  # Formerly 230,-260
        totalDistance = (
            abs(player1[1] - player2[1]) + abs(player1[0] - player2[0]))
        #print("Distance test:", totalDistance)
        return totalDistance
    except Exception as x:
        print("Exception:", x)
        return 999


def workingForward():
    cPlayer = playerArray[controllingPlayer()].getCoords()
    # if distance(controllingPlayer(), 7) < 290:
    #    FFX_blitzPathing.setMovement([playerArray[7].getCoords()[0], playerArray[7].getCoords()[1] - 320])
    if cPlayer[1] < -500 or cPlayer[0] > -300:
        FFX_blitzPathing.setMovement([-319, -493])
    elif cPlayer[1] < -360:
        FFX_blitzPathing.setMovement([-462, -354])
    else:
        FFX_blitzPathing.setMovement([-585, -130])


def findSafePlace():
    # current player
    cPlayer = playerArray[controllingPlayer()].getCoords()
    cPlayerNum = controllingPlayer()
    # graav coords
    dPos = playerArray[8].getCoords()
    forwardSpecial = False
    safeSpot = 255

    # Determin target coords based on character and state.
    if cPlayerNum in [1, 4]:
        targetCoords = [520, -20]
    elif cPlayerNum in [2, 3]:
        if playerArray[9].getCoords()[1] < 150:
            safeSpot = 3
        elif dPos[1] < -20 and cPlayer[1] > -500 and distance(cPlayerNum, 8) > 370 and distance(cPlayerNum, 10) > 370:
            if cPlayer[0] > dPos[0]:
                safeSpot = 1
            else:
                safeSpot = 2
        elif distanceSpecial() < 200:
            forwardSpecial = True
        else:
            safeSpot = 3
    elif distanceSpecial() < 70:
        forwardSpecial = True
    else:  # Should never occur, should never get Tidus/Wakka into this logic.
        safeSpot = 3

    # if safeSpot != 255:
    #    print("safeSpot value:", safeSpot)

    if safeSpot == 1:
        targetCoords = [-521, -266]
    elif safeSpot == 2:
        targetCoords = [-521, -266]
    elif safeSpot == 3:
        targetCoords = [-225, -543]

    # I think this is still the best option.
    targetCoords = [-2, -595]

    # Now attempt to move to the target.
    # If we're at the target, return True.
    # Decision-making will be based on if we're at the target, dealt with in parent function.
    # if forwardSpecial == True:
    #    if playerArray[controllingPlayer()].getCoords()[1] < -380:
    #        workingForward()
    #    else:
    #        FFX_blitzPathing.setMovement([-521,-266])
    if FFX_blitzPathing.setMovement(targetCoords):
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
            nextX = abs(math.sqrt((radius * radius) -
                        (jassuCoords[1] * jassuCoords[1])))
            if nextX < jassuCoords[0]:
                nextX = jassuCoords[0] + 50
    elif jassuCoords[0] < -150:  # Lower section
        version = "C"
        nextY = jassuCoords[1] - 20
        nextX = math.sqrt((radius * radius) -
                          (jassuCoords[1] * jassuCoords[1]))
        nextX *= -1
    elif jassuCoords[1] < -100:  # Near own goal
        version = "D"
        nextX = jassuCoords[0] + 100
        nextY = jassuCoords[1]
    else:  # Near opponent goal
        version = "B"

    #nextX = playerArray[3].getCoords()[0] - 10
    #nextY = playerArray[3].getCoords()[1]
    targetCoords = [int(nextX), int(nextY)]
    FFX_blitzPathing.setMovement(targetCoords)
    return [version, nextX, nextY]


def jassuTrain():
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
        elif math.sqrt((jassuCoords[0]*jassuCoords[0])+(jassuCoords[1]*jassuCoords[1])) < 480:
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
    elif playerArray[6].aggro() == False:
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
        nextX = math.sqrt((radius*radius)-(nextY*nextY)) * -1
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

    if useCircle == False:
        targetCoords = [int(nextX), int(nextY)]
        if reportState:
            print(version[0], "- ", targetCoords)
        FFX_blitzPathing.setMovement(targetCoords)
    else:
        if reportState:
            print(version)


def passBall(target=0, breakThrough=5):
    if controllingPlayer() == 4:
        breakThrough = 0
    if selectBreakthrough():
        if breakThrough == 5:
            if cursor1() == 0:
                FFX_Xbox.menuUp()
                FFX_memory.waitFrames(1)
            else:
                FFX_Xbox.menuB()
        else:
            FFX_Xbox.menuB()
    elif selectAction():
        if cursor1() != 0:  # Pass command
            FFX_Xbox.menuDown()
            FFX_memory.waitFrames(3)
        else:
            FFX_Xbox.menuB()
    elif selectPassTarget():
        if targetedPlayer() != target:
            FFX_Xbox.menuDown()
            FFX_memory.waitFrames(3)
        else:
            FFX_Xbox.tapB()
    else:
        FFX_Xbox.tapB()


def shootBall(breakThrough=5):
    if FFX_memory.getStoryProgress() < 570 and controllingPlayer() == 0:
        if gameClock() > 167:
            breakThrough = 5
        else:
            breakThrough = 0
    else:
        breakThrough = 5
    if selectShotType():
        if cursor1() == 1:
            FFX_Xbox.menuB()
        else:
            FFX_Xbox.menuDown()
            FFX_memory.waitFrames(3)
    elif selectBreakthrough():
        if breakThrough == 5:
            if cursor1() == 0:
                FFX_Xbox.menuUp()
                FFX_memory.waitFrames(1)
            else:
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()
        else:
            FFX_Xbox.menuB()
            FFX_Xbox.menuB()
    elif selectAction():
        if cursor1() != 1:  # Shoot
            FFX_Xbox.menuDown()
            FFX_memory.waitFrames(3)
        else:
            FFX_Xbox.menuB()
        gameVars.blitzFirstShotTaken()


def dribbleBall():
    if selectBreakthrough():
        if cursor1() == 0:
            FFX_Xbox.menuUp()
            FFX_memory.waitFrames(2)
        else:
            FFX_Xbox.menuB()
    elif selectAction():
        if cursor1() != 2:
            FFX_Xbox.menuUp()
            FFX_memory.waitFrames(3)
        else:
            FFX_Xbox.menuB()


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
    if reportState == True:
        print("Tidus movement")
    graavDistance = distance(0, 8)

    goalDistance = distance(0, 11)
    otherDistance = 0
    if distance(0, 6) < 180:
        otherDistance += 1
    if distance(0, 7) < 180:
        otherDistance += 1
    if distance(0, 9) < 180:
        otherDistance += 1
    if distance(0, 10) < 180:
        otherDistance += 1

    shootTarget = [-170, 584]

    if currentStage > 15:
        targetCoords = playerArray[3].getCoords()
        FFX_blitzPathing.setMovement(targetCoords)
        if distance(0, 3) < 290:
            FFX_Xbox.tapX()
    elif FFX_memory.getStoryProgress() > 700:
        if otherDistance >= 2:
            FFX_Xbox.tapX()
        elif currentStage == 4:
            FFX_Xbox.tapX()
        elif FFX_blitzPathing.setMovement(shootTarget):
            FFX_Xbox.tapX()
    elif currentStage in [0, 1, 2, 5]:
        FFXC.set_movement(-1, -1)
        FFX_Xbox.tapX()
    elif currentStage == 4:
        if graavDistance < 280:
            # Graav too close.
            FFXC.set_movement(-1, -1)
            FFX_Xbox.tapX()
        elif otherDistance >= 2:
            # Too many players closing in.
            FFXC.set_movement(-1, -1)
            FFX_Xbox.tapX()
        elif FFX_blitzPathing.setMovement(shootTarget) and FFX_memory.getStoryProgress() >= 570:
            FFXC.set_movement(-1, -1)
            FFX_Xbox.tapX()
    else:  # stages 3 and 4 only. All other stages we try to pass, or just shoot.
        if FFX_blitzPathing.setMovement(shootTarget) and FFX_memory.getStoryProgress() >= 570:
            FFXC.set_movement(-1, -1)
            FFX_Xbox.tapX()


def tidusAct():
    currentStage = gameStage()
    if reportState == True:
        print("Tidus act")
    graavDistance = distance(0, 8)

    goalDistance = distance(0, 11)
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
    elif FFX_memory.getStoryProgress() > 700:
        shootBall(breakThrough=0)
    elif currentStage in [4, 5]:
        # Late on the timer. Shoot at all costs.
        if FFX_memory.getStoryProgress() < 540:
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
    # elif goalDistance < 400 and currentStage == 4:
    #    #Close to goal. Shoot.
    #    print("In position - shoot the ball!")
    #    if graavDistance < 200:
    #        shootBall(breakThrough = 0)
    #    elif distance(0,10) < 200 and FFX_memory.getStoryProgress() < 540:
    #        print("First half, shooting without breakthrough.")
    #        shootBall(breakThrough = 0)
    #    else:
    #        shootBall(breakThrough = 0)
    else:
        shootBall(breakThrough=0)


def lettyMove():
    if reportState == True:
        print("Letty movement")
    currentStage = gameStage()
    graavDistance = distance(2, 8)

    if currentStage == 20:
        findSafePlace()
        if distance(0, 8) > 400 and distance(0, 10) > 400:
            FFX_Xbox.tapX()
        else:
            findSafePlace()
    elif currentStage == 30:
        findSafePlace()
        FFX_Xbox.tapX()
    elif currentStage >= 3:
        FFXC.set_movement(1, 0)
        FFX_Xbox.tapX()
    elif currentStage == 2:
        targetCoords = [-20, -585]
        FFX_blitzPathing.setMovement(targetCoords)
        if not playerGuarded(3):
            FFX_Xbox.tapX()
        elif not playerGuarded(2):
            FFX_Xbox.tapX()
    elif currentStage == 1:
        if not playerGuarded(3) and distance(3, 10) > 380 and graavDistance > 380:
            FFX_Xbox.tapX()
        else:
            if findSafePlace() and graavDistance < 320:
                FFX_Xbox.tapX()
    elif gameVars.blitzFirstShot():
        findSafePlace()
    else:
        if distance(3, 8) < 340 or distance(3, 7) < 340:
            if findSafePlace() and graavDistance < 280:
                FFX_Xbox.tapX()
        elif playerArray[2].currentHP() < 10:
            print("Letty out of HP. Passing to Jassu.")
            FFX_Xbox.tapX()
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
    elif FFX_memory.getStoryProgress() > 700:  # Post-storyline blitzball only
        if playerArray[0].getCoords()[1] > playerArray[1].getCoords()[1]:
            passBall(target=0, breakThrough=0)
        else:
            passBall(target=1, breakThrough=0)
    elif currentStage >= 4:
        passBall(target=0)
        if reportState == True:
            print("Letty Action 1")
    elif currentStage == 3:
        passBall(target=3)
        if reportState == True:
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
            tar = 4
        passBall(target=tar, breakThrough=breakThroughVal)
    elif currentStage == 1:
        if not playerGuarded(3) and distance(3, 10) > 380 and graavDistance > 380:
            passBall(target=3)
        else:
            dribbleBall()
    elif gameVars.blitzFirstShot():
        dribbleBall()
    elif playerArray[2].currentHP() < 10:
        if playerGuarded(3):
            dribbleBall()
        else:
            passBall(target=3)
    else:
        dribbleBall()
        if reportState == True:
            print("Letty Action 5")


def jassuMove():
    currentStage = gameStage()
    playerCoords = playerArray[controllingPlayer()].getCoords()
    targetCoords = [-572, -123]
    p10C = playerArray[10].getCoords()
    graavC = playerArray[8].getCoords()
    tidusC = playerArray[0].getCoords()
    findSafety = False
    moveForward = False
    # if reportState == True:
    #    print("Jassu movement")
    #    print("Stage:", currentStage)
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
        findSafePlace()
        if distance(0, 8) > 300 and distance(0, 10) > 360:
            FFX_Xbox.tapX()
    elif currentStage == 30:
        # if reportState:
        #    print("All aboard!!!")
        jassuTrain()
    elif currentStage <= 1 and playerArray[3].currentHP() < 10:
        if playerArray[2].currentHP() >= 40 and distance(2, 8) > 360:
            FFX_Xbox.tapX()
        elif graavDistance < 320:
            FFX_Xbox.tapX()
        else:
            findSafety = True
    elif currentStage in [0, 1]:
        # Defend in the goal for safety.
        findSafety = True
        if playerArray[2].currentHP() >= 40 and currentStage == 0:
            if distance(2, 8) > 360 and distance(2, 7) > 360 and distance(2, 6) > 360:
                FFX_Xbox.tapX()
    elif currentStage == 2:
        if playerArray[10].getCoords()[1] < 100:
            targetCoords = [playerArray[10].getCoords(
            )[0], playerArray[10].getCoords()[1] - 300]
        else:
            # Move forward to staging position, prep for shot.
            workingForward()
            moveForward = True
    elif currentStage == 3:
        relDist = (tidusC[0] + tidusC[1]) - (p10C[0] + p10C[1])
        relDist2 = (tidusC[0] + tidusC[1]) - (graavC[0] + graavC[1])
        if graavC[0] < -300:
            if relDist2 > 320:
                FFX_Xbox.tapX()
            else:
                targetCoords = [graavC[0] - 180, graavC[1] - 180]
        elif relDist > 260:  # Tidus in position behind defender
            FFX_Xbox.tapX()
        elif abs(playerArray[6].getCoords()[1] - playerArray[10].getCoords()[1]) < 50:
            if p10C[0] < -400:
                # Can re-use this later
                targetCoords = [playerCoords[0], playerCoords[1] - 100]
            else:
                targetCoords = [p10C[0] - 120, p10C[1] - 240]
        elif playerArray[3].getCoords()[1] < -200:
            # In position to see if anything happens
            targetCoords = [p10C[0] - 180, p10C[1] - 180]
        else:
            targetCoords = [p10C[0] - 180, p10C[1] - 180]
    else:  # Pass to Tidus
        targetCoords = [p10C[0] - 180, p10C[1] - 150]
        FFX_Xbox.tapX()

    if currentStage < 15:
        if findSafety:
            if findSafePlace() and graavDistance < 320:
                FFX_Xbox.tapX()
        elif not moveForward:
            FFX_blitzPathing.setMovement(targetCoords)


def jassuAct():
    currentStage = gameStage()
    if reportState == True:
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
        p10C = playerArray[10].getCoords()
        tidusC = playerArray[0].getCoords()
        relDist = (tidusC[0] + tidusC[1]) - (p10C[0] + p10C[1])
        if relDist > 270:
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


def otherMove():
    if findSafePlace() and distance(3, 8) > 350:
        FFX_Xbox.tapX()
    elif controllingPlayer() == 1:
        FFX_Xbox.tapX()
    else:
        FFX_Xbox.tapX()


def otherAct():
    currentStage = gameStage()

    if reportState == True:
        print("Botta/Datto action")
        print("Stage:", currentStage)

    if FFX_memory.getStoryProgress() > 700:
        if controllingPlayer() == 1:
            shootBall()
        else:
            if playerArray[0].getCoords()[1] > playerArray[1].getCoords()[1]:
                passBall(target=2, breakThrough=0)
            else:
                passBall(target=3, breakThrough=0)
    # elif currentStage <= 1:
    #    if distance(2,8) < 350:
    #        passBall(target = 3)
    #    else:
    #        passBall(target = 3)
    # elif currentStage == 2:
    #    if distance(3,8) < 350:
    #        passBall(target = 2)
    #    else:
    #        passBall(target = 3)
    else:
        passBall(target=3)


def blitzMovement():
    FFXC = FFX_Xbox.controllerHandle()
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
    FFXC = FFX_Xbox.controllerHandle()
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
    FFX_memory.clickToStoryProgress(535)
    print("-Match is now starting.")
    startTime = FFX_Logs.timeStamp()

    FFXC = FFX_Xbox.controllerHandle()
    gameVars.blitzFirstShotReset()
    movementSetFlag = False
    lastState = 0
    lastMenu = 0
    lastPhase = 99
    while FFX_memory.getStoryProgress() < 582 or FFX_memory.getStoryProgress() > 700:  # End of Blitz
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
                FFX_Xbox.menuB()
            if FFX_memory.getMap() == 62:
                if activeClock():
                    if lastState != 1:
                        print("Clock running.")
                        lastState = 1
                    if aurochsControl():
                        if lastMenu != 2:
                            print("Camera focusing Aurochs player")
                            lastMenu = 2
                        if movementSetFlag == False:
                            FFX_Xbox.tapY()
                        else:
                            blitzMovement()
                    else:
                        if lastMenu != 8:
                            print("Camera focusing opposing player")
                            lastMenu = 8
                else:
                    FFXC.set_neutral()
                    if lastState != 2:
                        print("Menu should be coming up")
                        lastState = 2
                    # FFX_memory.menuControl() # Could use this too
                    # print(FFX_memory.blitzMenuNum())
                    if selectMovement():
                        if lastMenu != 4:
                            print("Selecting movement method")
                            lastMenu = 4
                        if cursor1() == 1:
                            FFX_Xbox.menuB()
                            movementSetFlag = True
                        else:
                            FFX_Xbox.menuDown()
                            print(cursor1())
                    elif selectFormation():
                        if lastMenu != 5:
                            print("Selecting Formation")
                            lastMenu = 5
                        if cursor1() == 0:
                            FFX_Xbox.menuB()
                        else:
                            FFX_Xbox.menuUp()
                    elif selectFormation2():
                        if lastMenu != 5:
                            print("Selecting Formation")
                            lastMenu = 5
                        if cursor1() == 7:
                            FFX_Xbox.menuB()
                        else:
                            FFX_Xbox.menuUp()
                    elif selectBreakthrough():
                        if lastMenu != 6:
                            print("Selecting Break-through")
                            FFX_memory.waitFrames(2)
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
                            FFX_Xbox.menuB()
                        else:
                            FFX_Xbox.menuDown()
                            FFX_memory.waitFrames(3)
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
                    if FFX_memory.diagProgressFlag() == 113:
                        if cursor1() != 1:  # Pass command
                            FFX_Xbox.menuDown()
                            FFX_memory.waitFrames(3)
                        else:
                            FFX_Xbox.menuB()
                    elif FFX_memory.diagSkipPossible():  # Skip through everything else
                        FFX_Xbox.menuB()
                elif newHalf():
                    if forceBlitzWin:
                        FFX_memory.blitzballPatriotsStyle()
                    if FFX_memory.diagProgressFlag() == 347:
                        # Used for repeated Blitz games, not for story.
                        movementSetFlag = False
                    prepHalf()
                else:
                    Storyline(forceBlitzWin)
        except Exception as xVal:
            print("Caught exception in blitz main:")
            print(xVal)

    print("Blitz game has completed.")
    # Set the blitzWin flag for the rest of the run.
    print("Final scores: Aurochs:", FFX_memory.blitzOwnScore(),
          ", Opponent score:", FFX_memory.blitzOppScore())
    FFXC.set_neutral()
    if FFX_memory.blitzOwnScore() > FFX_memory.blitzOppScore():
        gameVars.setBlitzWin(True)
    else:
        gameVars.setBlitzWin(False)

    endTime = FFX_Logs.timeStamp()
    timeDiff = endTime - startTime
    totalTime = int(timeDiff.total_seconds())
    FFX_rngTrack.recordBlitzResults(duration=totalTime)
    print("--Blitz Win value:", gameVars.getBlitzWin())
