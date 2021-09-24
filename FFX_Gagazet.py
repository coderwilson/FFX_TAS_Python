import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory

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
    FFXC.set_value('AxisLx', -1)
    time.sleep(2.2)
    FFXC.set_value('AxisLx', 0)
    
    gemSlot = FFX_memory.getItemSlot(34)
    if gemSlot != 255:
        gems = FFX_memory.getItemCountSlot(gemSlot)
    else:
        gems = 0
    
    checkpoint = 0
    lastCP = 0
    itemSteal = gems
    while checkpoint < 1000:
        pos = FFX_memory.getCoords()
        if lastCP != checkpoint:
            print("Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        if FFX_memory.userControl():
            if pos == [0.0,0.0]: #This means we've lost control of the character for any reason.
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                if checkpoint == 0:
                    FFX_Xbox.menuB()
            elif checkpoint == 0:
                if pos[0] < -660:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > -1610:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 10: #Up to the turn
                if pos[1] > -1542:
                    checkpoint = 20
                else:
                    if pos[0] < -770:
                        FFXC.set_value('AxisLy', 0)
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLy', 1)
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 20: #Through the turn
                if pos[1] > -1470:
                    checkpoint = 30
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < -770:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 30:
                if pos[0] > 1290:
                    checkpoint = 40
                else:
                    #In case we're too far to the left
                    #print("CP30: ", ((float(pos[0]) * 58/76) - 900))
                    #if pos[1] > ((float(pos[0]) * 58/76) - 600):
                    #    FFXC.set_value('AxisLy', 0)
                    #else:
                    #    FFXC.set_value('AxisLy', 1)
                    
                    
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((float(pos[0]) * 58/76) - 830):
                        FFXC.set_value('AxisLx', 1)
                    
                    
                    
                    #elif pos[1] < ((float(pos[0]) * 58/76) - 800):
                    #    FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 40:
                if pos[1] > 980:
                    checkpoint = 50
                else:
                    if pos[1] > ((1.88 * pos[0]) - 1995):
                        #If we're too far from the wall, move back towards the wall.
                        FFXC.set_value('AxisLy', 1)
                        FFXC.set_value('AxisLx', 0)
                    else:
                        #Otherwise head up and (if needed) left.
                        FFXC.set_value('AxisLy', 1)
                        if pos[1] > ((4.34 * pos[0]) - 5721):
                            FFXC.set_value('AxisLx', -1)
                        else:
                            FFXC.set_value('AxisLx', 0)
            elif checkpoint == 50:
                if itemSteal < 2:
                    FFXC.set_value('AxisLx', 0)
                    FFXC.set_value('AxisLy', -1)
                    time.sleep(1)
                    FFXC.set_value('AxisLy', 1)
                    time.sleep(1)
                else:
                    checkpoint = 60
            elif checkpoint == 60:
                if pos[1] < -1:
                    checkpoint = 1000
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if FFX_Screen.BattleScreen():
                itemSteal += FFX_Battle.calmLands(itemSteal)
            elif FFX_memory.menuOpen():
                FFXC.set_value('BtnB', 1)
                time.sleep(0.035)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.035)
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.menuB()

def defenderX():
    FFXC.set_value('AxisLy', 1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.clickToBattle()
    FFX_Battle.buddySwap(0)
    FFX_Battle.aeonSummon(4)
    FFX_memory.clickToControl()
    
def toTheRonso():
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(4)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', 0)
    time.sleep(2.5)
    FFXC.set_value('AxisLy', 1)
    time.sleep(8)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFXC.set_value('AxisLy', 1)
    FFX_Screen.clickToMap1() #Just before Kelk Ronso conversation
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(6)
    FFXC.set_value('AxisLy', 0)
    
def gagazetGates(blitzWin):
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLy', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    
    endGameVersion = FFX_Battle.biranYenke()
    print("Grid version: " + str(endGameVersion))
    FFX_Logs.writeLog("Grid version: " + str(endGameVersion))
    FFX_Screen.clickToMap1()
    FFX_memory.fullPartyFormat('kimahri')
    FFX_menu.afterRonso(endGameVersion, blitzWin)
    
    FFXC.set_value('AxisLy', 1)
    time.sleep(12)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.clickToControl()
    
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

def afterFlux():
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
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.3)
    FFXC.set_value('AxisLy', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    
    time.sleep(1)
    FFX_Xbox.skipScene()
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
    FFXC.set_value('AxisLy', 1)
    time.sleep(8)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.3)
    FFXC.set_value('AxisLx', 0)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.awaitControl()
    print("Gagazet cave section")
    #FFX_menu.gagazetCave()
    
    checkpoint = 0
    lastCP = 0
    powerNeeded = 6
    while checkpoint < 200:
        pos = FFX_memory.getCoords()
        if lastCP != checkpoint:
            print("Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        if FFX_memory.userControl():
            if checkpoint == 0:
                if pos[1] > -1220:
                    checkpoint = 5
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 5:
                if pos[1] > -1118:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] > -25:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 10:
                if pos[1] > -945:
                    checkpoint = 20
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < 90:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 20:
                if pos[0] < 70:
                    checkpoint = 25
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', -1)
            elif checkpoint == 25:
                if pos[1] > -450:
                    checkpoint = 30
                else:
                    FFXC.set_value('AxisLy', 1) #Up to the first water area
                    if pos[0] < 1:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 30:
                if pos[1] < -457:
                    checkpoint = 35
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 35:
                if pos[1] > 110:
                    checkpoint = 40
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < -35:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 40: #First trial
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(4)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                FFX_Screen.awaitPixel(896,460,(235, 188, 0))
                print("First trial")
                time.sleep(0.2)
                FFX_Xbox.menuB()
                FFX_Screen.awaitPixel(1184,226,(255,255,255))
                time.sleep(2.2)
                FFX_Xbox.menuB() #Attempting for first shot
                time.sleep(3)
                while checkpoint == 40:
                    if FFX_memory.userControl():
                        checkpoint = 45
                    elif FFX_Screen.PixelTestTol(1184,226,(255,255,255),5):
                        time.sleep(5.1)
                        FFX_Xbox.menuB() #Subsequent attempts
                        time.sleep(6)
                print("First trial complete")
            elif checkpoint == 45:
                FFXC.set_value('AxisLy', -1)
                time.sleep(3)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.5)
                FFXC.set_value('AxisLx', 0)
                time.sleep(2)
                FFXC.set_value('AxisLy', 0)
                checkpoint = 50
            elif checkpoint == 50:
                if pos[1] < -390:
                    checkpoint = 55
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', 0)
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[1] < ((2.29 * pos[0]) - 346):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 55:
                if pos[0] > 170:
                    checkpoint = 60
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[0] < -66:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 60:
                if pos[1] < -950:
                    checkpoint = 65
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[0] < (-4.49 * (float(pos[0])) - 565):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 65:
                if pos[1] > -870:
                    checkpoint = 70
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < 140:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 70:
                if pos[1] > -600:
                    checkpoint = 75
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] > 180:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 75:
                if pos[1] > -530:
                    checkpoint = 80
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] > 180:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 80:
                if pos[1] > -218: #Up to the second water
                    checkpoint = 90
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < 200:
                        FFXC.set_value('AxisLx', 1)
                    elif pos[0] > 260:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 90: #Second trial area, before the curve
                if pos[1] > 120:
                    checkpoint = 94
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < 180:
                        FFXC.set_value('AxisLx', 1)
                    elif pos[0] > 260:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 94: #First part of curve
                if pos[1] > 280:
                    checkpoint = 98
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < 190:
                        FFXC.set_value('AxisLx', 1)
                    elif pos[0] > 210:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 98: #Into the trial
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
            elif checkpoint == 100:
                if pos[1] < 280:
                    checkpoint = 104
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[0] < 190:
                        FFXC.set_value('AxisLx', 1)
                    elif pos[0] > 210:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 104: #All the way out of the water
                if pos[1] < -225:
                    checkpoint = 110
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[0] > 260:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 110:
                if pos[1] < -470:
                    checkpoint = 120
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[0] > 220:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 120:
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
            elif checkpoint == 160:
                if pos[1] > -160:
                    checkpoint = 165
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 1)
            elif checkpoint == 165:
                if pos[1] > 215:
                    checkpoint = 169
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 169:
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                print("Prepping for Sanctuary Keeper")
                FFX_memory.fullPartyFormat('yuna')
                #FFX_menu.gagazetCave()
                checkpoint = 170
            elif checkpoint == 170:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
        elif FFX_Screen.BattleScreen():
            if FFX_memory.getPower() < powerNeeded and checkpoint >= 30 and checkpoint < 60:
                FFX_Battle.gagazetCave()
            elif FFX_memory.getPower() < powerNeeded and checkpoint >= 90 and checkpoint < 110:
                FFX_Battle.gagazetCave()
            elif checkpoint == 170:
                if FFX_Battle.sKeeper() == 1:
                    checkpoint = 200
            else:
                FFX_Battle.fleeLateGame()
        elif FFX_Screen.PixelTestTol(495,440,(235, 195, 0),5):
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
    FFXC.set_value('AxisLx', -1)
    time.sleep(8)
    FFXC.set_value('AxisLx', 0)
    print("Cutscene, first time seeing Zanarkand")
    
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    FFX_Xbox.SkipDialog(4)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    print("Scene at the Highroad agency")
    
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(2.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(8)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', -1)
    time.sleep(12)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    while FFX_memory.userControl(): #Down the ramp
        FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.awaitControl()
    time.sleep(0.2)
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
    time.sleep(5)
    
    FFX_Screen.awaitMap1()
    print("OMG finally! Let's get to it! (Do kids say that any more?)")
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(6)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)