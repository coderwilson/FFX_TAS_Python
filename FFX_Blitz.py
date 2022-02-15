import FFX_Xbox
import time
import FFX_Logs
import FFX_memory
import FFX_blitzPathing
import FFX_vars
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

playerArray = [0,0,0,0,0,0,0,0,0,0,0,0]

#Initialize the player array
for i in range(12):
    playerArray[i] = FFX_memory.blitzActor(playerNum = i)


def goersScoreFirst():
    return FFX_memory.diagProgressFlag() in [47, 48, 49]

def halftimeDialog():
    return FFX_memory.diagProgressFlag() in [45,46]

def selectMovement():
    return FFX_memory.blitzMenuNum() == 146

def selectFormation():
    return FFX_memory.blitzMenuNum() == 133

def selectFormation2():
    return FFX_memory.blitzMenuNum() == 144

def selectBreakthrough():
    if FFX_memory.blitzMenuNum() >= 0 and FFX_memory.blitzMenuNum() <= 46:
        return True
    else:
        return False

def selectAction():
    return FFX_memory.blitzMenuNum() == 52

def selectPassTarget():
    return FFX_memory.blitzMenuNum() == 226

def selectShotType():
    return FFX_memory.blitzMenuNum() == 117

def targettedPlayer():
    retVal = FFX_memory.blitzTargetPlayer() - 2
    #print("++ ", retVal)
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
    #Map = 347, Dialog = 20
    print("Prepping for next period of play.")
    while FFX_memory.getMap() != 62:
        if FFX_memory.diagProgressFlag() == 135: #Select game mode (Tourney, League, Exhibiton, etc)
            FFX_memory.waitFrames(90)
            if FFX_memory.savePopupCursor() != 1:
                FFX_Xbox.menuDown()
                time.sleep(2)
            else:
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
        elif FFX_memory.diagProgressFlag() in [20,134]:
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
        #First half is 535
        #Hype halftime is 540
        #Second half starts on 560
        #575 - 9

def cursor1():
    return FFX_memory.blitzCursor()

def gameStage():
    #Stage 0: Killing time
    #Stage 1: Defensive, Letty dribble, consumes Jassu HP
    #Stage 2: Jassu position near the edge of the pool, look for opportunity.
    #Stage 3: Positioning Defender so Tidus can shoot/score
    #Stage 4: Pass to Tidus
    #Stage 5: Shoot for goal
    currentStage = 0
    if FFX_memory.getStoryProgress() < 540: #First half
        #stages = [0, 0, 150, 260, 280, 285]
        stages = [0, 285, 280, 280, 280, 280]
    elif FFX_memory.getStoryProgress() < 570: #Second half, before Tidus/Wakka swap
        stages = [0, 90, 90, 120, 145, 160]
    elif FFX_memory.getStoryProgress() < 700: #End of the storyline game
        stages = [0, 0, 0, 250, 280, 286]
    else: #Used for any non-story blitzing.
        stages = [0, 0, 0, 0, 0, 270]
    
    #Determine base stage. Modified by following logic.
    for i in range(5):
        if stages[i] < gameClock():
            currentStage = i
    
    if FFX_memory.getStoryProgress() < 700: #Only apply following logic for the storyline game
        #Logic that updates stage based on defender movements
        if playerArray[0].getCoords()[1] - playerArray[10].getCoords()[1] > 300:
            if currentStage < 3:
                currentStage = 4
        elif playerArray[10].getCoords()[1] < 200 and currentStage == 2:
            #Defender is pushed forward
            currentStage = 3
        
        #Logic that reduces stage if score is too far apart.
        if FFX_memory.blitzOwnScore() - FFX_memory.blitzOppScore() >= 1 \
            and FFX_memory.getStoryProgress() > 560:
            currentStage = 0
        elif abs(FFX_memory.blitzOwnScore() - FFX_memory.blitzOppScore()) >= 2:
            currentStage = 0
        
        #Logic that immediately moves to scoring phases if in overtime.
        if FFX_memory.getStoryProgress() >= 570 and FFX_memory.getStoryProgress() < 700:
            if gameClock() < 20 and not gameVars.getBlitzOT():
                gameVars.setBlitzOT(True)
            if gameVars.getBlitzOT() and currentStage < 3:
                currentStage = 3
    
    return currentStage

reportState = False

def passBall(target=0, breakThrough = 5):
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
        if cursor1() != 0: #Pass command
            FFX_Xbox.menuDown()
            FFX_memory.waitFrames(3)
        else:
            FFX_Xbox.menuB()
    elif selectPassTarget():
        if targettedPlayer() != target:
            FFX_Xbox.menuDown()
            FFX_memory.waitFrames(3)
        else:
            FFX_Xbox.menuB()

def shootBall(breakThrough = 5):
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
        else:
            FFX_Xbox.menuB()
    elif selectAction():
        if cursor1() != 1: #Shoot
            FFX_Xbox.menuDown()
            FFX_memory.waitFrames(3)
        else:
            FFX_Xbox.menuB()

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
    #Graav proximity always counts as guarded.
    if distance(playerNum, 8) < 340:
        return True
        
    #Two or more player proximity always counts as guarded.
    otherDistance = 0
    if distance(0,6) < 350:
        otherDistance += 1
    if distance(0,7) < 350:
        otherDistance += 1
    if distance(0,9) < 350:
        otherDistance += 1
    if distance(0,10) < 350:
        otherDistance += 1
    if otherDistance >= 2:
        return True
        
    #Specific cases depending on player.
    if playerNum in [2,3,4]:
        if distance(playerNum, 9):
            return True
        if distance(playerNum, 10):
            return True
    return False

def tidusMove():
    currentStage = gameStage()
    if reportState == True:
        print("Tidus movement")
    graavDistance = distance(0,8)
    
    goalDistance = distance(0,11)
    otherDistance = 0
    if distance(0,6) < 280:
        otherDistance += 1
    if distance(0,7) < 280:
        otherDistance += 1
    if graavDistance < 280:
        otherDistance += 1
    if distance(0,9) < 280:
        otherDistance += 1
    if distance(0,10) < 280:
        otherDistance += 1
    
    shootTarget = [-150, 552]
    
    if FFX_memory.getStoryProgress() > 700:
        if otherDistance >= 2:
            FFX_Xbox.tapX()
        elif currentStage == 4:
            FFX_Xbox.tapX()
        elif FFX_blitzPathing.setMovement(shootTarget):
            FFX_Xbox.tapX()
    elif currentStage == 5:
        #Late on the timer. Shoot at all costs.
        FFXC.set_movement(-1, 0)
        FFX_Xbox.tapX()
    elif goalDistance < 150:
        #Close to goal. Shoot.
        FFXC.set_movement(-1, 0)
        FFX_Xbox.tapX()
    elif graavDistance > 240 and graavDistance < 270:
        #Graav too close.
        FFXC.set_movement(-1, 0)
        FFX_Xbox.tapX()
    elif otherDistance >= 2:
        #Too many players closing in.
        FFXC.set_movement(-1, 0)
        FFX_Xbox.tapX()
    #elif playerArray[0].getCoords()[1] < playerArray[8].getCoords()[1]:
    #    #Move up even with (or past) Graav
    #    targetCoords = [playerArray[8].getCoords()[0] - 380, playerArray[8].getCoords()[1] + 20]
    #    FFX_blitzPathing.setMovement(targetCoords)
    elif FFX_blitzPathing.setMovement(shootTarget):
        #Lastly, push towards the goal.
        FFX_Xbox.tapX()

def tidusAct():
    currentStage = gameStage()
    if reportState == True:
        print("Tidus act")
    graavDistance = distance(0,8)
    
    goalDistance = distance(0,11)
    otherDistance = 0
    if distance(0,6) < 280:
        otherDistance += 1
    if distance(0,7) < 280:
        otherDistance += 1
    if distance(0,9) < 280:
        otherDistance += 1
    if distance(0,10) < 280:
        otherDistance += 1
    
    if FFX_memory.getStoryProgress() > 700:
        shootBall(breakThrough = 0)
    elif currentStage == 5:
        #Late on the timer. Shoot at all costs.
        if FFX_memory.getStoryProgress() < 540:
            print("First half, shooting without breakthrough.")
            if gameClock() < 270 and distance(0,8) > 250:
                shootBall()
            else:
                shootBall(breakThrough = 0)
        else:
            print("Stage 5 - shoot the ball!")
            shootBall()
    elif goalDistance < 400 and currentStage == 4:
        #Close to goal. Shoot.
        print("In position - shoot the ball!")
        if graavDistance < 200:
            shootBall(breakThrough = 0)
        elif distance(0,10) < 200 and FFX_memory.getStoryProgress() < 560:
            print("First half, shooting without breakthrough.")
            shootBall(breakThrough = 0)
        else:
            shootBall()
    elif goalDistance < 500 and FFX_memory.getStoryProgress() > 560:
        #Wakka can shoot farther than Tidus.
        shootBall()
    elif graavDistance > 240 and graavDistance < 270:
        #Graav too close.
        shootBall()
    elif otherDistance >= 2:
        #Too many players closing in.
        shootBall()
    else:
        shootBall()

def lettyMove():
    if reportState == True:
        print("Letty movement")
    currentStage = gameStage()
    graavDistance = distance(2,8)
    
    if currentStage >= 3:
        FFXC.set_movement(1, 0)
        FFX_Xbox.tapX()
    elif currentStage == 2:
        targetCoords = [playerArray[8].getCoords()[0] + 180, playerArray[8].getCoords()[1] - 230]
        FFX_blitzPathing.setMovement(targetCoords)
        if playerArray[0].getCoords()[0] - playerArray[8].getCoords()[0] < -350:
            FFX_Xbox.tapX()
    else:
        if playerArray[2].currentHP() < 10:
            print("Letty out of HP. Passing to Jassu.")
            FFX_Xbox.tapX()
        elif graavDistance < 340:
            print("Graav too close. Passing ball away.")
            FFXC.set_movement(1, 0)
            FFX_Xbox.tapX()
        elif playerArray[7].getCoords()[1] < -100:
            #Hide in goal
            targetCoords = [20, -600]
            FFX_blitzPathing.setMovement(targetCoords)
        elif playerArray[6].getCoords()[1] < -100:
            #Hide in goal
            targetCoords = [20, -600]
            FFX_blitzPathing.setMovement(targetCoords)
        else:
            #defend at a set distance from opposing forward.
            targetCoords = [0, playerArray[6].getCoords()[1] - 380]
            FFX_blitzPathing.setMovement(targetCoords)

def lettyAct():
    currentStage = gameStage()
    
    if FFX_memory.getStoryProgress() > 700: #Post-storyline blitzball only
        if playerArray[0].getCoords()[1] > playerArray[1].getCoords()[1]:
            passBall(target = 0, breakThrough = 0)
        else:
            passBall(target = 1, breakThrough = 0)
    elif currentStage >= 4:
        passBall(target = 0)
        if reportState == True:
            print("Letty Action 1")
    elif currentStage == 3:
        passBall(target = 3)
        if reportState == True:
            print("Letty Action 2")
    elif playerArray[2].currentHP() < 10:
        passBall(target = 3)
    elif currentStage == 2:
        if playerArray[0].getCoords()[0] - playerArray[8].getCoords()[0] < -350:
            passBall(target = 3)
        else:
            dribbleBall()
    elif distance(2, 8) < 340:
        passBall(target = 0, breakThrough = 0)
    else:
        dribbleBall()
        if reportState == True:
            print("Letty Action 5")

def jassuMove():
    currentStage = gameStage()
    if reportState == True:
        print("Jassu movement")
        print("Stage: ", currentStage)
    graavDistance = distance(3,8)
    otherDistance = 0
    if distance(3,6) < 350:
        otherDistance += 1
    if distance(3,7) < 350:
        otherDistance += 1
    if distance(3,9) < 350:
        otherDistance += 1
    if distance(3,10) < 350:
        otherDistance += 1
    
    
    if currentStage >= 1 and playerArray[3].currentHP() < 10:
        FFX_Xbox.tapX()
    elif currentStage in [0,1]:
        #Defend in the goal for safety.
        targetCoords = [-20, -595]
        FFX_blitzPathing.setMovement(targetCoords)
        if playerArray[2].currentHP() >= 20:
            if distance(2,8) > 360:
                FFX_Xbox.tapX()
        elif playerArray[8].getCoords()[1] < -350 or distance(3,8) < 310:
            FFX_Xbox.tapX()
    elif currentStage == 2:
        targetCoords = [-572, -123]
        FFX_blitzPathing.setMovement(targetCoords)
        if playerArray[8].getCoords()[0] < -300:
            FFX_Xbox.tapB()
    elif currentStage == 3:
        p10C = playerArray[10].getCoords()
        tidusC = playerArray[0].getCoords()
        relDist = (tidusC[0] + tidusC[1]) - (p10C[0] + p10C[1])
        if relDist > 270:
            FFX_Xbox.tapX()
        elif abs(playerArray[6].getCoords()[1] - playerArray[10].getCoords()[1]) < 50:
            if p10C[0] < -400:
                targetCoords = [p10C[0] - 0,p10C[1] - 280]
            else:
                targetCoords = [p10C[0] - 180,p10C[1] - 120]
            FFX_blitzPathing.setMovement(targetCoords)
        elif playerArray[3].getCoords()[1] < -200:
            #In position to see if anything happens
            if p10C[0] < -400:
                targetCoords = [p10C[0] - 0,p10C[1] - 280]
            else:
                targetCoords = [p10C[0] - 180,p10C[1] - 120]
            FFX_blitzPathing.setMovement(targetCoords)
        else:
            targetCoords = [p10C[0] - 180,p10C[1] - 120]
            FFX_blitzPathing.setMovement(targetCoords)
    else: #Pass to Tidus
        FFX_Xbox.tapX()

def jassuAct():
    currentStage = gameStage()
    if reportState == True:
        print("Jassu Action")
        print("Stage: ", currentStage)
    graavDistance = distance(3,8)
    otherDistance = 0
    if distance(3,6) < 350:
        otherDistance += 1
    if distance(3,7) < 350:
        otherDistance += 1
    if distance(3,9) < 350:
        otherDistance += 1
    if distance(3,10) < 350:
        otherDistance += 1
    
    
    if currentStage in [0,1]:
        if playerArray[8].getCoords()[1] < -350 or distance(3,8) < 310:
            passBall(target = 0)
        else:
            passBall(target = 2)
    elif playerArray[3].currentHP() < 10:
        passBall(target = 0)
    elif currentStage == 2:
        if playerArray[8].getCoords()[0] < -300:
            passBall(target=0)
        else:
            dribbleBall()
    elif currentStage == 3:
        p10C = playerArray[10].getCoords()
        tidusC = playerArray[0].getCoords()
        relDist = (tidusC[0] + tidusC[1]) - (p10C[0] + p10C[1])
        if relDist > 270:
            passBall(target = 0)
        elif graavDistance < 150:
            #Graav too close
            passBall(target = 0)
        elif playerArray[0].getCoords()[1] - playerArray[10].getCoords()[1] > 280:
            #Tidus in position for break-away.
            passBall(target = 0)
        else:
           dribbleBall()
    else: #Pass to Tidus
        passBall(target = 0)


def otherMove():
    if reportState == True:
        print("Botta/Datto movement")
    graavDistance = distance(controllingPlayer(),8)
    if FFX_memory.getStoryProgress() > 700 and \
        playerArray[0].getCoords()[1] > 250:
        FFXC.set_movement(0, 1)
    elif graavDistance > 280 and graavDistance < 320:
        FFXC.set_movement(0, 1)
    elif playerArray[controllingPlayer()].getCoords()[0] > 500:
        FFXC.set_movement(0, 1)
    else:
        FFX_blitzPathing.setMovement([150, -510])
    if distance(controllingPlayer(),8) > 300:
        FFX_Xbox.tapX()

def otherAct():
    currentStage = gameStage()
    
    if reportState == True:
        print("Botta/Datto action")
        print("Stage: ", currentStage)
    
    if FFX_memory.getStoryProgress() > 700:
        if controllingPlayer() == 1:
            shootBall()
        else:
            if playerArray[0].getCoords()[1] > playerArray[1].getCoords()[1]:
                passBall(target = 0, breakThrough = 0)
            else:
                passBall(target = 1, breakThrough = 0)
    elif currentStage <= 1:
        if playerGuarded(2):
            passBall(target = 3)
        else:
            passBall(target = 2)
    elif currentStage == 2:
        if playerGuarded(3):
            passBall(target = 2)
        else:
            passBall(target = 3)
    else:
        passBall(target = 0)

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
        print("Exception: ", x)
        return 999

def updatePlayerArray():
    for i in range(12):
        playerArray[i].updateCoords()

def blitzMain(forceBlitzWin):
    print("-Start of Blitzball program")
    print("-First, clicking to the start of the match.")
    FFX_memory.clickToStoryProgress(535)
    print("-Match is now starting.")
    
    FFXC = FFX_Xbox.controllerHandle()
    movementSetFlag = False
    lastState = 0
    lastMenu = 0
    lastPhase = 99
    while FFX_memory.getStoryProgress() < 582 or FFX_memory.getStoryProgress() > 700: #End of Blitz
        if lastPhase != gameStage() and gameClock() > 0 and gameClock() < 301:
            lastPhase = gameStage()
            print("--------------------------------------")
            print("--------------------------------------")
            print("New phase reached. ", lastPhase)
            print("--------------------------------------")
            print("--------------------------------------")
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
                #FFX_memory.menuControl() # Could use this too
                #print(FFX_memory.blitzMenuNum())
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
                    if cursor1() != 1: #Pass command
                        FFX_Xbox.menuDown()
                        FFX_memory.waitFrames(3)
                    else:
                        FFX_Xbox.menuB()
                elif FFX_memory.diagSkipPossible(): #Skip through everything else
                    FFX_Xbox.menuB()
            elif newHalf():
                if forceBlitzWin:
                    FFX_memory.blitzballPatriotsStyle()
                if FFX_memory.diagProgressFlag() == 347:
                    #Used for repeated Blitz games, not for story.
                    movementSetFlag = False
                prepHalf()
            else:
                Storyline(forceBlitzWin)
    
    print("Blitz game has completed.")
    #Set the blitzWin flag for the rest of the run.
    print("Final scores: Aurochs: ", FFX_memory.blitzOwnScore(), \
        ", Opponent score: ", FFX_memory.blitzOppScore())
    FFXC.set_neutral()
    if FFX_memory.blitzOwnScore() > FFX_memory.blitzOppScore():
        gameVars.setBlitzWin(True)
    else:
        gameVars.setBlitzWin(False)