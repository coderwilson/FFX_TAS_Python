import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory
import FFX_targetPathing

FFXC = FFX_Xbox.FFXC
 
def calmLands(blitzWin):
    FFX_memory.awaitControl()
    #Start by getting away from the save sphere
    FFX_menu.prepCalmLands(blitzWin)
    FFX_memory.fullPartyFormat('kimahri')
    
    FFXC.set_value('AxisLy', 1)
    time.sleep(4)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.clickToControl()
    #FFXC.set_value('AxisLx', -1)
    #time.sleep(2.2)
    #FFXC.set_value('AxisLx', 0)
    
    gemSlot = FFX_memory.getItemSlot(34)
    if gemSlot != 255:
        gems = FFX_memory.getItemCountSlot(gemSlot)
    else:
        gems = 0
    
    checkpoint = 0
    itemSteal = gems
    while FFX_memory.getMap() != 279:
        if FFX_memory.userControl():
            if checkpoint == 9 and itemSteal < 2:
                checkpoint = 8
                FFXC.set_value('AxisLy', -1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(2)
            elif FFX_targetPathing.setMovement(FFX_targetPathing.calmLands(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if FFX_Screen.BattleScreen():
                itemSteal += FFX_Battle.calmLands(itemSteal)
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.menuB()

def defenderX():
    time.sleep(0.5)
    FFX_memory.awaitControl()
    while FFX_targetPathing.setMovement([67,-255]) == False:
        doNothing = True
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.awaitEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.clickToBattle()
    FFX_Battle.buddySwap(0)
    FFX_Battle.aeonSummon(4)
    FFX_memory.clickToControl()
    
def toTheRonso():
    checkpoint = 0
    while FFX_memory.getMap() != 259:
        if FFX_memory.userControl():
            if FFX_targetPathing.setMovement(FFX_targetPathing.defenderX(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if FFX_memory.diagSkipPossible():
                FFXC.set_value('BtnB', 1)
                time.sleep(0.035)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.035)
    
    #Now in screen with Ronso
    checkpoint = 0
    while FFX_memory.getMap() != 244:
        if FFX_memory.userControl():
            if FFX_targetPathing.setMovement(FFX_targetPathing.kelkRonso(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if FFX_memory.battleScreen():
                endGameVersion = FFX_Battle.biranYenke()
            elif FFX_memory.diagSkipPossible():
                FFXC.set_value('BtnB', 1)
                time.sleep(0.035)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.035)
    
    return endGameVersion
    
def gagazetGates(blitzWin, endGameVersion):
    #Should appear on the map just before the Ronso hymn
    print("Grid version: " + str(endGameVersion))
    FFX_Logs.writeLog("Grid version: " + str(endGameVersion))
    FFX_memory.awaitControl()
    if FFX_memory.overdriveState()[6] == 100:
        FFX_memory.fullPartyFormat('kimahri')
    else:
        FFX_memory.fullPartyFormat('rikku')
    FFX_menu.afterRonso(endGameVersion, blitzWin)
    FFX_memory.closeMenu() #just in case
    
    print("Gagazet path section")
    checkpoint = 0
    while FFX_memory.getMap() != 285:
        if FFX_memory.userControl():
            if FFX_targetPathing.setMovement(FFX_targetPathing.gagazetSnow(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if FFX_memory.menuOpen():
                FFXC.set_value('BtnB', 1)
                time.sleep(0.035)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.035)
            elif FFX_memory.battleScreen():
                #Charge Rikku until full, otherwise flee all
                if FFX_memory.overdriveState()[6] == 100:
                    FFX_Battle.fleeAll()
                    FFX_memory.clickToControl()
                else:
                    FFX_Battle.gagazetPath()
                    FFX_memory.clickToControl()
                    if FFX_memory.overdriveState()[6] == 100:
                        FFX_memory.fullPartyFormat('kimahri')
                    else:
                        FFX_memory.fullPartyFormat('rikku')
            elif FFX_memory.diagSkipPossible():
                FFXC.set_value('BtnB', 1)
                time.sleep(0.035)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.035)
    #Should now be on the map with Seymour Flux. Moving to next section
    
def gagazetOldPath():
    print("Gagazet path section")
    
    checkpoint = 0
    lastCP = 0
    while checkpoint < 1000:
        pos = FFX_memory.getCoords()
        if lastCP != checkpoint:
            print("Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        if FFX_memory.userControl():
            if pos == [0.0,0.0]: #This means we've lost control of the character for any reason.
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                #if checkpoint == 0:
                #    FFX_Xbox.menuB()
            elif checkpoint == 0:
                if pos[1] > 150:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 10: #Up to the turn
                if pos[1] > 350:
                    checkpoint = 20
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < 40:
                        FFXC.set_value('AxisLx', 1)
                    elif pos[0] > 65:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 20: #Past first tobmstone
                if pos[0] < -80:
                    checkpoint = 30
                else:
                    FFXC.set_value('AxisLx', -1)
                    if pos[1] > 440:
                        FFXC.set_value('AxisLy', -1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 30:
                if pos[1] < 287:
                    checkpoint = 40
                else:
                    FFXC.set_value('AxisLx', -1)
                    if pos[1] > 410:
                        FFXC.set_value('AxisLy', 0)
                    else:
                        FFXC.set_value('AxisLy', -1)
            elif checkpoint == 40:
                if pos[1] > 500:
                    checkpoint = 50
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] < ((-2 * pos[0]) - 234):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 50:
                if pos[1] < 222:
                    checkpoint = 60
                else:
                    FFXC.set_value('AxisLx', -1)
                    if pos[1] < ((1.73 * pos[0]) + 1190): #Double check later
                        FFXC.set_value('AxisLy', 1)
                    elif pos[1] > ((1.73 * pos[0]) + 1170): #Double check later
                        FFXC.set_value('AxisLy', -1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 60:
                if pos[0] < -935:
                    checkpoint = 70
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] < ((0.17 * pos[0]) + 315):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 70: #Diagonal before Wantz
                if pos[1] > 565:
                    checkpoint = 80
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[1] > ((0.41 * pos[0]) + 586):
                        FFXC.set_value('AxisLy', -1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 80:
                if pos[0] > -650:
                    checkpoint = 90
                else:
                    FFXC.set_value('AxisLy', -1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 90:
                if pos[1] < 220:
                    checkpoint = 100
                else:
                    FFXC.set_value('AxisLx', -1)
                    if pos[1] > ((-3.81 * pos[0]) -1900):
                        FFXC.set_value('AxisLy', -1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 100: #Left side after Wantz
                if pos[0] < -700:
                    checkpoint = 110
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((0.04 * pos[0]) + 210):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 110: #Back to far right, near last tomb
                if pos[1] > 495:
                    checkpoint = 114
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[1] > ((-1.67 * pos[0]) -1180):
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 114:
                if pos[0] < -1090:
                    checkpoint = 118
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 118:
                if pos[1] < 470:
                    checkpoint = 120
                else:
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', -1)
            elif checkpoint == 120:
                if pos[1] < 10:
                    checkpoint = 130
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((2.89 * pos[0]) + 3760):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 130:
                if pos[1] < - 300:
                    checkpoint = 140
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] < ((2.89 * pos[0]) + 3820): #up for tweaking
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 140:
                FFX_memory.fullPartyFormat('yuna')
                FFX_menu.beforeFlux()
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(1.5)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.5)
                FFXC.set_value('AxisLx', 0)
                time.sleep(3)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                FFX_Battle.seymourFlux()
                checkpoint = 1000
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if FFX_Screen.BattleScreen():
                FFX_Battle.fleeAll()
            elif FFX_memory.menuOpen():
                FFXC.set_value('BtnB', 1)
                time.sleep(0.035)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.035)
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.menuB()
    return endGameVersion

def Flux():
    FFX_memory.fullPartyFormat('yuna')
    FFX_menu.beforeFlux()
    
    checkpoint = 0
    while FFX_memory.getMap() != 309:
        if FFX_memory.userControl():
            if checkpoint == 7:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.5)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                
                FFX_Xbox.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 8:
                while FFX_memory.userControl():
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 1)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            elif FFX_targetPathing.setMovement(FFX_targetPathing.Flux(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if FFX_memory.diagSkipPossible():
                FFXC.set_value('BtnB', 1)
                time.sleep(0.035)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.035)
            elif FFX_memory.menuOpen():
                FFXC.set_value('BtnB', 1)
                time.sleep(0.035)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.035)
            elif FFX_memory.battleScreen():
                FFX_Battle.seymourFlux()
                FFX_menu.afterFlux()
                FFX_memory.fullPartyFormat('kimahri')
    while not FFX_memory.cutsceneSkipPossible():
        if FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
    FFX_Xbox.skipScene()
    
def Flux_movement_old():
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Battle.seymourFlux()
    
    #Now literally after Flux
    FFX_memory.awaitControl()
    FFX_menu.afterFlux()
    FFX_memory.fullPartyFormat('kimahri')
    time.sleep(0.15)
    FFXC.set_value('AxisLy', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 1)
    time.sleep(7)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.touchSaveSphere() #Quick save sphere before we move onward.

def dream():
    #FFXC.set_value('AxisLx', 1)
    #time.sleep(0.3)
    #FFXC.set_value('AxisLy', 1)
    #time.sleep(3)
    #FFXC.set_value('AxisLx', 0)
    #time.sleep(1)
    #FFXC.set_value('AxisLy', 0)
    
    #time.sleep(1)
    #FFX_Xbox.skipScene()
    FFX_memory.clickToControl()
    print("*********")
    print("Dream sequence")
    print("*********")
    time.sleep(0.2)
    pos = FFX_memory.getCoords()
    while pos[1] > 180:
        FFXC.set_value('AxisLx', 1)
        FFXC.set_value('AxisLy', 1)
        pos = FFX_memory.getCoords()

    while pos[0] < -1:
        FFXC.set_value('AxisLx', 0)
        FFXC.set_value('AxisLy', 1)
        pos = FFX_memory.getCoords()
        
    while pos[1] > 20:
        FFXC.set_value('AxisLx', 1)
        FFXC.set_value('AxisLy', 1)
        pos = FFX_memory.getCoords()
    print("Onto the gangway")
        
    while pos[0] < 235:
        FFXC.set_value('AxisLx', -1)
        if pos[1] < -6:
            FFXC.set_value('AxisLy', 0)
        else:
            FFXC.set_value('AxisLy', 1)
        pos = FFX_memory.getCoords()

    while FFX_memory.userControl(): #Into the boathouse.
        FFXC.set_value('AxisLx', -1)
        FFXC.set_value('AxisLy', 0)
    print("Now inside the boathouse.")
    
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.7)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0) #Start convo with Bahamut child
    print("First talk with Bahamut child")
    FFX_memory.clickToControl()
    
    FFXC.set_value('AxisLy', -1) #End of conversation
    time.sleep(0.7)
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.7)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.7)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl()
    pos = FFX_memory.getCoords()
    while pos[1] > -20:
        FFXC.set_value('AxisLx', 1)
        FFXC.set_value('AxisLy', 0)
        pos = FFX_memory.getCoords()
    
    while pos[0] < 300:
        FFXC.set_value('AxisLx', 0)
        FFXC.set_value('AxisLy', 1)
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.SkipDialog(2)
    FFXC.set_value('AxisLx', 0) #Second/last convo with kid
    print("Second talk with Bahamut child")
    
    FFX_memory.clickToControl()
    
def cave():
    checkpoint = 0
    
    checkpoint = 0
    while FFX_memory.getMap() != 272:
        if FFX_memory.userControl():
            if FFX_targetPathing.setMovement(FFX_targetPathing.gagazetDream(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if FFX_memory.diagSkipPossible():
                FFXC.set_value('BtnB', 1)
                time.sleep(0.035)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.035)
            elif FFX_memory.menuOpen():
                FFXC.set_value('BtnB', 1)
                time.sleep(0.035)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.035)
    
    
    FFX_memory.awaitControl()
    print("Gagazet cave section")
    #FFX_menu.gagazetCave()
    
    checkpoint = 0
    lastCP = 0
    powerNeeded = 6
    while FFX_memory.getMap() != 311:
        if FFX_memory.userControl():
            if checkpoint == 7:
                if FFX_memory.getMap() == 310:
                    print("Now in the trials map.")
                    checkpoint += 1
                else:
                    print("Into swimming map, first trial.")
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
                    time.sleep(0.5)
            elif checkpoint == 12:
                print("Trial 1 - Let's Go!!!")
                while FFX_memory.userControl():
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                
                print("Now the trial has started.")
                FFX_Xbox.SkipDialog(4)
                FFX_Screen.awaitPixel(1184,226,(255,255,255))
                time.sleep(1.2)
                FFX_Xbox.menuB() #Attempting for first shot
                print("First attempt.")
                time.sleep(3)
                complete = False
                while complete == False:
                    if FFX_memory.userControl():
                        complete = True
                    elif FFX_Screen.PixelTestTol(1184,226,(255,255,255),5):
                        time.sleep(5.1)
                        FFX_Xbox.menuB() #Subsequent attempts
                        print("Additional attempt.")
                        time.sleep(4.4)
                        if FFX_memory.userControl():
                            complete = True
                        else:
                            time.sleep(1.6) #Timing to re-try
                print("First trial complete")
                checkpoint += 1
            elif checkpoint == 17:
                if FFX_memory.getMap() == 272:
                    print("Leaving the trials map.")
                    checkpoint += 1
                else:
                    print("Back to main map after first trial.")
                    FFXC.set_value('AxisLy', -1)
                    FFXC.set_value('AxisLx', 0)
                    time.sleep(0.5)
            elif checkpoint == 29:
                if FFX_memory.getMap() == 310:
                    print("Now in the trials map.")
                    checkpoint += 1
                else:
                    print("Into swimming map, second trial.")
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
                    time.sleep(0.5)
            elif checkpoint == 35:
                if FFX_memory.userControl():
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', -1)
                else:
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', 0)
                    
            elif checkpoint == 42:
                print("Out of swimming map, second trial.")
                if FFX_memory.getMap() == 272:
                    print("Leaving the trials map.")
                    checkpoint += 1
                else:
                    FFXC.set_value('AxisLy', -1)
                    FFXC.set_value('AxisLx', 0)
                    time.sleep(0.5)
            elif checkpoint == 59: #Just before sanctuary keeper
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                print("Prepping for Sanctuary Keeper")
                FFX_memory.fullPartyFormat('yuna')
                checkpoint += 1
            elif FFX_targetPathing.setMovement(FFX_targetPathing.gagazetCave(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if checkpoint == 35 and (FFX_Screen.PixelTestTol(495,440,(234, 195, 0),5)):
                print("Second trial start")
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.07)
                FFX_Xbox.menuB()
                time.sleep(2.5)
                FFX_Xbox.menuRight()
                time.sleep(0.3)
                FFX_memory.clickToControl()
                checkpoint += 1
                print("Second trial is complete")
            elif FFX_memory.battleScreen():
                if FFX_memory.getPower() < powerNeeded:
                    if FFX_memory.getBattleNum() == 351: #Two maelstroms and a splasher
                        FFX_Battle.gagazetCave('down')
                    elif FFX_memory.getBattleNum() == 353: #Two glowey guys, two splashers.
                        FFX_Battle.gagazetCave('right')
                    elif FFX_memory.getBattleNum() == 354: #Four groups of splashers
                        FFX_Battle.gagazetCave('none')
                    else:
                        FFX_Battle.fleeAll()
                else:
                    FFX_Battle.fleeAll()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif checkpoint == 6 or checkpoint == 54:
                if FFX_memory.battleActive():
                    FFX_Battle.fleeAll()
                elif FFX_memory.diagSkipPossible(): #So we don't override the second trial
                    FFX_Xbox.tapB()
                
                #if FFX_memory.getPower() < powerNeeded and checkpoint >= 30 and checkpoint < 60:
                #    FFX_Battle.gagazetCave()
                #elif FFX_memory.getPower() < powerNeeded and checkpoint >= 90 and checkpoint < 110:
                #    FFX_Battle.gagazetCave()
                #else:
    FFX_Screen.clickToBattle()
    FFX_Battle.sKeeper()
    
def cave_oldMovement():
    while checkpoint < 200:
        pos = FFX_memory.getCoords()
        if lastCP != checkpoint:
            print("Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        if FFX_memory.userControl():
            if checkpoint == 0: #First movement in the cave
                if pos[1] > -1140:
                    checkpoint = 5
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] < ((6.03 * pos[0]) -959.17):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 5: #Approach save sphere from the entrance.
                if pos[1] > -958:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((1.37 * pos[0]) -1078.65):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 10: #Deviate towards first trial
                if pos[1] > -790:
                    checkpoint = 20
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((-2.76 * pos[0]) -709.76):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 20: #Down hallway, into the first swimming area.
                if pos[1] > -450:
                    checkpoint = 25
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] < ((8.21 * pos[0]) -829.88):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 25:
                if FFX_memory.getMap() == 310:
                    checkpoint = 30
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((1.44 * pos[0]) -579.19):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 30: #Room with first trial, approaching trial.
                FFXC.set_value('AxisLy', 1)
                if pos[1] < -285 and pos[1] > ((2.23 * pos[0]) -295.33):
                    FFXC.set_value('AxisLx', 1)
                elif pos[1] < -12 and pos[1] < ((3.25 * pos[0]) -344.81):
                    FFXC.set_value('AxisLx', -1)
                elif pos[1] > ((1.39 * pos[0]) -113.74):
                    FFXC.set_value('AxisLx', 1)
                else:
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 40: #Move away from the trial.
                FFXC.set_value('AxisLy', -1)
                time.sleep(3)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.5)
                FFXC.set_value('AxisLx', 0)
                time.sleep(2)
                FFXC.set_value('AxisLy', 0)
                checkpoint = 50
            elif checkpoint == 50:
                if pos[1] < -370:
                    checkpoint = 55
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', 0)
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[1] < ((2.29 * pos[0]) - 346):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 55: #Swim back to first map
                if FFX_memory.getMap() == 272:
                    checkpoint = 60
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[0] < -66:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 60: #Back to dry land
                if pos[1] < -540:
                    checkpoint = 65
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[1] > ((1.33 * pos[0]) -587.92):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 65: #Path back towards save sphere
                if pos[1] < ((0.70 * pos[0]) -1018.70):
                    checkpoint = 70
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[1] < ((-57.25 * pos[0]) + 942.75):
                        FFXC.set_value('AxisLx', 1)
                    elif pos[1] < ((-1.25 * pos[0]) -793.16):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 70: #Camera change near save sphere
                if pos[1] > -850:
                    checkpoint = 80
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((1.17 * pos[0]) -1114.4):
                        FFXC.set_value('AxisLx', 1)
                    elif pos[0] > 230:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 80: #Diagonal towards second water section (hard left)
                if pos[1] > -680:
                    checkpoint = 85
                else:
                    if pos[1] > ((-2.18 * pos[0]) -243.36):
                        FFXC.set_value('AxisLy', 0)
                    else:
                        FFXC.set_value('AxisLy', 1)
                    if pos[1] < -660 and pos[1] > ((-2.71 * pos[0]) -146.22):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 85: #Diagonal towards second water section (back to the right)
                if FFX_memory.getMap() == 310:
                    checkpoint = 90
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] < -300 and pos[1] > ((8.21 * pos[0]) -2178.71):
                        FFXC.set_value('AxisLx', 1)
                    elif pos[0] > 245:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 90: #Second trial area, before the curve
                if pos[1] > 210:
                    checkpoint = 95
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((5.90 * pos[0]) -1000.76):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 95: #Curving to second trial
                if pos[1] > ((-0.38 * pos[0]) + 360):
                    FFXC.set_value('AxisLy', 0)
                else:
                    FFXC.set_value('AxisLy', 1)
                if pos[1] > ((9.86 * pos[0]) -1799.14):
                    FFXC.set_value('AxisLx', -1)
                elif pos[1] > ((-1.27 * pos[0]) + 527.00):
                    FFXC.set_value('AxisLx', -1)
                elif pos[1] > ((-0.38 * pos[0]) + 357.75):
                    FFXC.set_value('AxisLx', -1)
                else:
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 100:
                if pos[1] < 280:
                    checkpoint = 104
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[1] < 72:
                        if pos[1] < ((-11.78 * pos[0]) + 2,157.67):
                            FFXC.set_value('AxisLx', 1)
                        else:
                            FFXC.set_value('AxisLx', 0)
                    if pos[0] > 220:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 104: #All the way out of the water
                if pos[1] < -270:
                    checkpoint = 110
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[0] > 260:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 110: #Back to line up with the new stairs
                if pos[1] < -450:
                    checkpoint = 120
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[0] > 220:
                        FFXC.set_value('AxisLx', -1)
                    elif pos[1] < ((2.29 * pos[0]) -890.17):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 120: #Left to stairs
                if pos[0] < 170:
                    checkpoint = 130
                else:
                    FFXC.set_value('AxisLx', -1)
                    if pos[1] > -440:
                        FFXC.set_value('AxisLy', -1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 130:
                if pos[1] > -354:
                    checkpoint = 140
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < 160:
                        FFXC.set_value('AxisLx', 1)
                    if pos[0] > 175:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 140:
                if pos[1] > -283:
                    checkpoint = 150
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] > 165:
                        FFXC.set_value('AxisLx', -1)
                    elif pos[0] < 150:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 150:
                if pos[0] > 170:
                    checkpoint = 155
                else:
                    FFXC.set_value('AxisLx', 1)
                    FFXC.set_value('AxisLy', 0)
            elif checkpoint == 155:
                if pos[1] > -236:
                    checkpoint = 160
                else:
                    FFXC.set_value('AxisLx', -1)
                    FFXC.set_value('AxisLy', 1)
            elif checkpoint == 160: #Move into the scene with Yuna and Auron
                if pos[1] > -160:
                    checkpoint = 170
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 1)
            elif checkpoint == 170: # Final path, part 1
                if pos[1] > -10:
                    checkpoint = 180
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] < ((-5.07 * pos[0]) + 810.07):
                        FFXC.set_value('AxisLx', 0)
                    else:
                        FFXC.set_value('AxisLx', -1)
            elif checkpoint == 180: # Final path, part 2
                if pos[1] > 215:
                    checkpoint = 185
                else:
                    if pos[1] > ((-0.65 * pos[0]) + 108):
                        FFXC.set_value('AxisLy', 0)
                    else:
                        FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((-0.65 * pos[0]) + 104.6):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 185:
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                print("Prepping for Sanctuary Keeper")
                FFX_memory.fullPartyFormat('yuna')
                #FFX_menu.gagazetCave()
                checkpoint = 190
            elif checkpoint == 190:
                FFXC.set_value('AxisLy', 1)
                if pos[1] > ((0.15 * pos[0]) + 275.54):
                    FFXC.set_value('AxisLx', -1)
                else:
                    FFXC.set_value('AxisLx', 0)
        elif FFX_Screen.BattleScreen():
            if FFX_memory.getPower() < powerNeeded and checkpoint >= 30 and checkpoint < 60:
                FFX_Battle.gagazetCave()
            elif FFX_memory.getPower() < powerNeeded and checkpoint >= 90 and checkpoint < 110:
                FFX_Battle.gagazetCave()
            elif checkpoint == 190:
                if FFX_Battle.sKeeper() == 1:
                    checkpoint = 200
            else:
                FFX_Battle.fleeLateGame()
        elif FFX_Screen.PixelTestTol(896,460,(235, 188, 0),5): #First trial
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
            print("First trial")
            time.sleep(0.2)
            FFX_Xbox.menuB()
            FFX_Screen.awaitPixel(1184,226,(255,255,255))
            time.sleep(1.2)
            FFX_Xbox.menuB() #Attempting for first shot
            time.sleep(3)
            while checkpoint == 30:
                if FFX_memory.userControl():
                    checkpoint = 40
                elif FFX_Screen.PixelTestTol(1184,226,(255,255,255),5):
                    time.sleep(5.1)
                    FFX_Xbox.menuB() #Subsequent attempts
                    time.sleep(4.4)
                    if FFX_memory.userControl():
                        checkpoint = 40
                    else:
                        time.sleep(1.6) #Timing to re-try
            print("First trial complete")
        elif FFX_Screen.PixelTestTol(495,440,(235, 195, 0),5): #Second trial
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
            print("Second trial")
            time.sleep(0.5)
            FFX_Xbox.menuB()
            time.sleep(2.5)
            FFX_Xbox.menuRight()
            time.sleep(0.3)
            FFX_Screen.clickToMap1()
            checkpoint = 100
            print("Second trial is complete")
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
        else:
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
            if FFX_memory.menuOpen():
                FFX_Xbox.menuB()

def wrapUp():
    print("Cave section complete and Sanctuary Keeper is down.")
    print("Now onward to Zanarkand.")
    
    checkpoint = 0
    while FFX_memory.getMap() != 132:
        if FFX_memory.userControl():
            if FFX_memory.getMap() == 312 and checkpoint < 6:
                print("Move forward to next map. Final path before making camp.")
                checkpoint = 7
            elif checkpoint == 3:
                if FFX_memory.getStoryProgress() >= 2651:
                    checkpoint += 1
                else: #2635 before agency scene, 2650 during the agency scene
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', -1)
                    FFXC.set_value('BtnB', 1)
                    time.sleep(0.035)
                    FFXC.set_value('BtnB', 0)
                    time.sleep(0.035)
            elif checkpoint == 6:
                if FFX_memory.getMap() == 312:
                    print("Final path before making camp.")
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', 0)
                    checkpoint += 1
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 1)
            elif FFX_targetPathing.setMovement(FFX_targetPathing.gagazetPeak(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    
    
    #Resting point before Zanarkand
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.awaitControl()
    time.sleep(0.07)
    FFXC.set_value('AxisLy', 1) #Start of the sadness cutscene.
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    
    sleepTime = 4
    print("Sadness cutscene")
    time.sleep(sleepTime)
    print("This is gunna be a while.")
    time.sleep(sleepTime)
    print("Maybe you should go get a drink or something.")
    time.sleep(sleepTime)
    print("Like... what even is this???")
    time.sleep(sleepTime)
    print("I just")
    time.sleep(sleepTime)
    print("I just can't")
    time.sleep(sleepTime)
    print("Do you realize that some poor soul")
    time.sleep(sleepTime)
    print("not only wrote the entire program for this by himself")
    time.sleep(sleepTime)
    print("And then wasted ten minutes to put in this ridiculous dialog?")
    time.sleep(sleepTime)
    print("Talk about not having a life.")
    time.sleep(sleepTime)
    print("Ah well, still have some time. Might as well shout out a few people.")
    time.sleep(sleepTime)
    print("First and most importantly, my wife for putting up with me for two years through this project.")
    time.sleep(sleepTime)
    print("My wife is the best!")
    time.sleep(sleepTime)
    print("Next, DwangoAC. He encouraged me to write my own code to do this.")
    time.sleep(sleepTime)
    print("And he put together the TASbot community which has been hugely helpful.")
    time.sleep(sleepTime)
    print("Shout out to DwangoAC and the TASbot Community. You guys rock!!!")
    time.sleep(sleepTime)
    print("Specifically from the TASbot Community, Inverted wrote the pathing logic for the Egg Hunt section.")
    time.sleep(sleepTime)
    print("You will see Inverted's work right before the final bosses.")
    time.sleep(sleepTime)
    print("Next, some people from the FFX speed-running community.")
    time.sleep(sleepTime)
    print("CrimsonInferno, current world record holder for this category. Dude knows everything about this run!")
    time.sleep(sleepTime)
    print("Crimson re-wrote a great many boss fights for this project. From Spherimorph to Evrae Altana, and probably more.")
    time.sleep(sleepTime)
    print("Also, 'Rossy__' from the same community. Rossy helped me find a great many things in memory.")
    time.sleep(sleepTime)
    print("He also taught me a number of things about memory scans, pointers, etc. Dude is super smart.")
    time.sleep(sleepTime)
    print("OK now for a silly reference. Does anyone watch DBZ Abridged?")
    time.sleep(sleepTime)
    print("------------------------------------------------------------------------")
    print("Goku?! Goku what have you done? You've blasted off into space!!!")
    time.sleep(sleepTime)
    print("You're incredibly luck that I've already set the coordinates for Namek but you...")
    time.sleep(sleepTime)
    print("You....")
    time.sleep(sleepTime)
    print("Where did you get that muffin?")
    time.sleep(sleepTime)
    print("Muffin button?")
    time.sleep(sleepTime)
    print("But I never installed a muffin button!")
    time.sleep(sleepTime)
    print("Then where did I get this muffin?")
    time.sleep(sleepTime)
    print("OK enough of the silly references. I'll catch you when it's done.")
    time.sleep(sleepTime)
    
    FFX_memory.clickToControl()
    print("OMG finally! Let's get to it! (Do kids say that any more?)")
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', -1)
    FFX_memory.awaitEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.2)