import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_memory

FFXC = FFX_Xbox.FFXC
 
def arrival():
    #FFX_Screen.clickToMap1()
    #FFX_menu.moonflowWakkaWeap()
    print("Starting Djose section")
    
    checkpoint = 0
    lastCP = 0
    while checkpoint != 150:
        if lastCP != checkpoint:
            print("Checkpoint reached: ",checkpoint)
            lastCP = checkpoint
        if FFX_memory.userControl():
            pos = FFX_memory.getCoords()
            if checkpoint == 0:
                if pos[0] < -1:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0) #Make sure we're not stuck in Djose area still
            elif checkpoint == 10:
                if pos[1] < 1320:
                    checkpoint = 20
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((6.02 * pos[0]) + 8595.22):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 20:
                if pos[1] < 820:
                    checkpoint = 30
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((6.02 * pos[0]) + 8595.22):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 30:
                if pos[0] < -1550:
                    checkpoint = 40
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] < ((0.60 * pos[0]) + 1576.00):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 40:
                if pos[1] < 150:
                    checkpoint = 60
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((1.52 * pos[0]) + 3089.53):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 60:
                if pos[1] < -500:
                    checkpoint = 70
                else:
                    FFXC.set_value('AxisLy', 1) #Long path past Belgemine
                    if pos[0] < -1898:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 70:
                if pos[0] > -1805:
                    checkpoint = 90
                else:
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', -1)
            elif checkpoint == 90:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0)
                FFX_Xbox.menuB()
            elif checkpoint == 100:
                if pos[0] < -1940:
                    checkpoint = 110
                else:
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', 1)
            elif checkpoint == 110:
                if pos[1] > 1:
                    checkpoint = 150
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
                    
        elif checkpoint == 90 and FFX_Screen.PixelTestTol(613,446,(208, 208, 208),5):
            print("Mdef sphere chest.")
            FFX_memory.clickToControl()
            checkpoint = 100
        elif FFX_Screen.BattleScreen():
            FFX_Battle.fleeAll()
        elif FFX_memory.menuOpen():
            FFX_Xbox.menuB()
        elif checkpoint == 20:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('BtnB', 1)
            time.sleep(0.035)
            FFXC.set_value('BtnB', 0)
            time.sleep(0.035)
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if FFX_Screen.BattleScreen():
                FFX_Battle.fleeAll()
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.menuB()

def southBank():
    #Arrive at the south bank of the moonflow.
    FFX_Battle.healUp(2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(8)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.clickToMap2()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(4)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.clickToPixel(453,173,(156, 117, 0)) #O'aka standing next to a bench
    FFXC.set_value('AxisLx', -1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.awaitPixel(543,39,(26, 139, 56)) #Shoopuff screen
    FFXC.set_value('AxisLx', -1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.clickToPixel(226,134,(193, 193, 193)) #Lucil, a will, a way
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.awaitPixel(543,39,(26, 139, 56)) #Shoopuff screen
    #FFX_Battle.healUpNoCombat(2)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1.8)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', -1)
    FFX_Xbox.SkipDialog(0.4)
    FFXC.set_value('AxisLx', 0)
    
    time.sleep(0.5)
    FFX_Xbox.menuB()
    time.sleep(0.5)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    
    FFX_Battle.extractor()
    
def northBank():
    FFX_Screen.clickToPixel(459,380,(90, 112, 69))
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    FFX_Screen.awaitPixel(908,433,(72, 64, 90))
    FFXC.set_value('AxisLx', -1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    FFX_Screen.awaitPixel(886,49,(162, 67, 63))
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0) #Last screen before Rikku
    
    FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLx', -1)
    time.sleep(4)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(3)
    FFXC.set_value('AxisLx', 1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Battle.mixTutorial()
    FFX_memory.fullPartyFormat_New("postbunyip", 10)
    FFX_memory.closeMenu()
    
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(6)
    FFXC.set_value('AxisLy', 0)
    
    complete = 0
    stepCount = 0
    while complete == 0:
        if FFX_memory.userControl():
            stepCount += 1
            if stepCount % 20 == 0:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.4)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            else:
                FFXC.set_value('AxisLy', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
        elif FFX_Screen.PixelTest(657,249,(234, 196, 0)): #Customize tutorial screen
            complete = 1
        elif FFX_Screen.BattleScreen():
            FFX_Battle.fleeAll()
        elif FFX_Screen.BattleComplete():
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            FFX_Xbox.menuB()
        elif not FFX_Screen.PixelTest(1,1,(0,0,0)):
            FFX_Xbox.menuB()