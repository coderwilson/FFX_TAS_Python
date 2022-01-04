import FFX_Xbox
import time
import FFX_Logs
import FFX_memory
import FFX_blitzPathing

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

def selectBreakthrough():
    return FFX_memory.blitzMenuNum() in [12, 16, 18, 23, 28]

def selectAction():
    return FFX_memory.blitzMenuNum() == 52

def selectPassTarget():
    return FFX_memory.blitzMenuNum() == 226

def selectShotType():
    return FFX_memory.blitzMenuNum() == 117

def targettedPlayer():
    return FFX_memory.blitzTargetPlayer()

def activeClock():
    return not FFX_memory.blitzClockPause()

def aurochsControl():
    return FFX_memory.blitzTargetPlayer() < 8

def controllingPlayer():
    return FFX_memory.blitzCurrentPlayer()

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
    print("Prepping for second half.")
    while FFX_memory.getMap() != 62:
        if FFX_memory.diagProgressFlag() in [20,134]:
            if FFX_memory.blitzCharSelectCursor() != 6:
                FFX_Xbox.tapA()
            else:
                FFX_Xbox.tapB()
                FFX_memory.waitFrames(5)
        elif FFX_memory.diagProgressFlag() == 40:
            if FFX_memory.blitzProceedCursor() == 1:
                FFX_Xbox.menuUp()
            else:
                FFX_Xbox.menuB()
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
    print("Prep complete.")

def Storyline(forceBlitzWin):
    current = FFX_memory.getStoryProgress()
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
    #Stage 1: Positioning Defender so Tidus can shoot/score
    #Stage 2: Pass to Tidus
    #Stage 3: Shoot for goal
    currentStage = 0
    if FFX_memory.getStoryProgress() < 560: #First half
        stages = [0, 30, 300, 300, 300]
    elif FFX_memory.getStoryProgress() == 560: #Second half, before Tidus/Wakka swap
        stages = [0, 30, 120, 145, 163]
    else:
        stages = [0, 180, 240, 265, 283]
    if abs(FFX_memory.blitzOwnScore() - FFX_memory.blitzOppScore()) >= 1:
        currentStage = 0
    else:
        for i in range(5):
            if stages[i] < gameClock():
                currentStage = i
    #print("Stage: ", currentStage, " - Clock", gameClock())
    return currentStage
    

def blitzMovement():
    FFXC = FFX_Xbox.controllerHandle()
    currentStage = gameStage()
    updatePlayerArray()
    
    #Now to determine what we want to do with the stage.
    if currentStage == 0:
        #print("Pass to player 3, then hide in goal. ", controllingPlayer())
        if gameClock() < 1:
            FFXC.set_movement(1, 0)
        elif controllingPlayer() != 5:
            try:
                if playerArray[controllingPlayer() - 2].getCoords()[1] > -450:
                    FFXC.set_movement(1, 0)
                else:
                    plannedAction = 'pass'
                    updatePlayerArray()
                    if plannedAction == 'pass':
                        FFX_Xbox.tapX()
                    else:
                        targetCoords = [playerArray[7].getCoords()[0], playerArray[7].getCoords()[1] - 360]
                        FFX_blitzPathing.setMovement(targetCoords)
            except Exception as e:
                doNothing = True
        else:
            FFX_blitzPathing.setMovement([0, -600])
    elif currentStage == 1: #Still hide unless the defender comes out
        if controllingPlayer() == 2:
            #Tidus has the ball behind enemy lines
            if FFX_blitzPathing.setMovement([-40, 562]):
                FFX_Xbox.tapX()
        elif controllingPlayer() != 5:
            try:
                if playerArray[controllingPlayer() - 2].getCoords()[1] > -450:
                    FFXC.set_movement(1, 0)
                else:
                    FFX_Xbox.tapX()
            except Exception as e:
                doNothing = True
        elif playerArray[10].getCoords()[1] < -100:
            if playerArray[0].getCoords()[1] - playerArray[10].getCoords()[1] > 250:
                FFX_Xbox.tapX()
            else:
                if playerArray[10].getCoords()[0] < -350:
                    targetCoords = [playerArray[10].getCoords()[0] + 80, playerArray[10].getCoords()[1] - 180]
                else:
                    targetCoords = [playerArray[10].getCoords()[0], playerArray[10].getCoords()[1] - 250]
                FFX_blitzPathing.setMovement(targetCoords)
        else:
            if playerArray[7].getCoords()[1] < playerArray[8].getCoords()[1]:
                if playerArray[7].getCoords()[1] < -160:
                    FFX_blitzPathing.setMovement([0, -600])
                else:
                    targetCoords = [playerArray[7].getCoords()[0], playerArray[7].getCoords()[1] - 360]
                    FFX_blitzPathing.setMovement(targetCoords)
            else:
                if playerArray[8].getCoords()[1] < -160:
                    FFX_blitzPathing.setMovement([0, -600])
                else:
                    targetCoords = [playerArray[8].getCoords()[0], playerArray[8].getCoords()[1] - 360]
                    FFX_blitzPathing.setMovement(targetCoords)
    elif currentStage == 2: #Start moving forward. Pass if defender is deep.
        if controllingPlayer() == 2:
            #Tidus has the ball behind enemy lines
            if FFX_blitzPathing.setMovement([-40, 552]):
                FFX_Xbox.tapX()
        elif controllingPlayer() != 5:
            FFX_Xbox.tapX()
        elif playerArray[0].getCoords()[1] - playerArray[10].getCoords()[1] > 100 \
            or playerArray[10].getCoords()[1] < 200:
            if playerArray[0].getCoords()[1] - playerArray[10].getCoords()[1] > 250:
                FFX_Xbox.tapX()
            else:
                targetCoords = [playerArray[10].getCoords()[0] - 80, playerArray[10].getCoords()[1] - 250]
                FFX_blitzPathing.setMovement(targetCoords)
        else:
            updatePlayerArray()
            #print("Test - ", playerArray[3].getCoords())
            if playerArray[3].getCoords()[1] < -250:
                if playerArray[3].getCoords()[1] < -481:
                    FFX_blitzPathing.setMovement([-206, -480])
                elif playerArray[3].getCoords()[1] < -394:
                    FFX_blitzPathing.setMovement([-434, -390])
                else:
                    FFX_blitzPathing.setMovement([-586, 0])
            else:
                targetCoords = [playerArray[8].getCoords()[0] - 250, playerArray[8].getCoords()[1] - 200]
                FFX_blitzPathing.setMovement(targetCoords)
    elif currentStage == 3: #Pass to Tidus
        if controllingPlayer() != 2:
            FFX_Xbox.tapX()
        else:
            if FFX_blitzPathing.setMovement([-197, 552]):
                FFX_Xbox.tapX()
    else: #Shoot the ball
        FFX_Xbox.tapX()

def decideAction():
    FFXC = FFX_Xbox.controllerHandle()
    currentStage = gameStage()
    
    #Now to determine what we want to do with the stage.
    if selectShotType():
        if cursor1() == 1:
            FFX_Xbox.tapB()
        else:
            FFX_Xbox.menuDown()
            FFX_memory.waitFrames(3)
    elif currentStage == 0:
        if controllingPlayer() != 5:
            if selectBreakthrough():
                if cursor1() == 0:
                    FFX_Xbox.menuUp()
                else:
                    FFX_Xbox.tapB()
            elif selectAction():
                if cursor1() != 0:
                    FFX_Xbox.menuUp()
                else:
                    FFX_Xbox.tapB()
            elif selectPassTarget():
                if targettedPlayer() != 5:
                    FFX_Xbox.menuUp()
                    FFX_memory.waitFrames(3)
                else:
                    FFX_Xbox.tapB()
        else:
            if cursor1() == 0:
                FFX_Xbox.menuUp()
            else:
                FFX_Xbox.tapB()
    elif currentStage in [1, 2]:
        if controllingPlayer() == 2:
            if selectBreakthrough():
                if cursor1() == 0:
                    FFX_Xbox.menuUp()
                    FFX_memory.waitFrames(1)
                else:
                    FFX_Xbox.tapB()
            elif selectAction():
                if cursor1() != 1:
                    FFX_Xbox.menuDown()
                    FFX_memory.waitFrames(3)
                else:
                    FFX_Xbox.tapB()
        elif controllingPlayer() != 5:
            if selectBreakthrough():
                if cursor1() == 0:
                    FFX_Xbox.menuUp()
                else:
                    FFX_Xbox.tapB()
            elif selectAction():
                if cursor1() != 0:
                    FFX_Xbox.menuUp()
                    FFX_memory.waitFrames(3)
                else:
                    FFX_Xbox.tapB()
            elif selectPassTarget():
                if targettedPlayer() != 5:
                    FFX_Xbox.menuDown()
                    FFX_memory.waitFrames(3)
                else:
                    FFX_Xbox.tapB()
        else:
            if playerArray[0].getCoords()[1] - playerArray[10].getCoords()[1] > 150:
                if selectBreakthrough():
                    if cursor1() == 0:
                        FFX_Xbox.menuUp()
                        FFX_memory.waitFrames(3)
                    else:
                        FFX_Xbox.tapB()
                elif selectAction():
                    if cursor1() != 0:
                        FFX_Xbox.menuUp()
                        FFX_memory.waitFrames(3)
                    else:
                        FFX_Xbox.tapB()
                elif selectPassTarget():
                    if targettedPlayer() != 2:
                        FFX_Xbox.menuDown()
                        FFX_memory.waitFrames(3)
                    else:
                        FFX_Xbox.tapB()
            elif cursor1() == 0:
                FFX_Xbox.menuUp()
                FFX_memory.waitFrames(3)
            else:
                FFX_Xbox.tapB()
    elif currentStage == 3: #Pass to Tidus
        if controllingPlayer() != 2:
            if selectBreakthrough():
                if cursor1() == 0:
                    FFX_Xbox.menuUp()
                    FFX_memory.waitFrames(3)
                else:
                    FFX_Xbox.tapB()
            elif selectAction():
                if cursor1() != 0:
                    FFX_Xbox.menuUp()
                    FFX_memory.waitFrames(3)
                else:
                    FFX_Xbox.tapB()
            elif selectPassTarget():
                if targettedPlayer() != 2:
                    FFX_Xbox.menuDown()
                    FFX_memory.waitFrames(3)
                else:
                    FFX_Xbox.tapB()
        else:
            if cursor1() == 0:
                FFX_Xbox.menuUp()
                FFX_memory.waitFrames(3)
            else:
                FFX_Xbox.tapB()
    else: #Shoot the ball
        if selectBreakthrough():
            if cursor1() == 0:
                FFX_Xbox.menuUp()
                FFX_memory.waitFrames(3)
            else:
                FFX_Xbox.tapB()
        elif selectAction():
            if cursor1() != 1:
                FFX_Xbox.menuDown()
                FFX_memory.waitFrames(3)
            else:
                FFX_Xbox.tapB()

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
    while FFX_memory.getStoryProgress() < 582: #End of Blitz
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
            FFX_Xbox.tapB()
        if FFX_memory.getMap() == 62:
            if activeClock():
                if lastState != 1:
                    print("Clock running.")
                    lastState = 1
                if aurochsControl():
                    if lastMenu != 2:
                        print("Aurochs are in control of the ball.")
                        lastMenu = 2
                    if movementSetFlag == False:
                        FFX_Xbox.tapY()
                    else:
                        blitzMovement()
                else:
                    if lastMenu != 8:
                        print("Opponent in control")
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
                        FFX_Xbox.tapB()
                        movementSetFlag = True
                    else:
                        FFX_Xbox.menuDown()
                        print(cursor1())
                elif selectFormation():
                    if lastMenu != 5:
                        print("Selecting Formation")
                        lastMenu = 5
                    if cursor1() == 0:
                        FFX_Xbox.tapB()
                    else:
                        FFX_Xbox.menuUp()
                elif selectBreakthrough():
                    if lastMenu != 6:
                        print("Selecting Break-through")
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
                    decideAction()
                elif selectAction():
                    if lastMenu != 7:
                        print("Selecting action (Shoot/Pass/Dribble)")
                        lastMenu = 7
                    decideAction()
        else:
            if lastState != 3:
                print("Screen outside the Blitz sphere")
                lastState = 3
            if halfSummaryScreen():
                FFX_Xbox.tapB()
            elif newHalf():
                prepHalf()
            else:
                Storyline(forceBlitzWin)
    
    print("Blitz game has completed.")
    #FFX_Xbox.clearSavePopup()