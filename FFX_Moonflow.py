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
    print("Starting Moonflow section")
    
    checkpoint = 0
    lastCP = 0
    while checkpoint != 150:
        pos = FFX_memory.getCoords()
        if lastCP != checkpoint:
            print("Checkpoint reached: ",checkpoint)
            lastCP = checkpoint
        if FFX_memory.userControl():
            if FFX_memory.getMap() == 105:
                checkpoint = 150
            elif checkpoint == 0:
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
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(4)
    FFXC.set_value('AxisLx', 0)
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLx', -1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLx', -1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl3()
    #FFX_Battle.healUpNoCombat(2)
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1.7)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    time.sleep(0.8)
    FFX_Xbox.menuB() #Ride ze Shoopuff?
    time.sleep(0.8)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #All aboardz!
    
    FFX_Battle.extractor()
    
def northBank():
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLx', -1)
    FFX_memory.awaitEvent()
    time.sleep(1)
    FFX_memory.awaitControl()
    time.sleep(1.5)
    FFX_memory.clickToEvent() #Talk to Auron
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.3)
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.5)
    FFX_memory.awaitEvent()
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.5)
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0) #Last screen before Rikku
    
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLx', -1)
    time.sleep(4)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_memory.clickToControl3()
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
    time.sleep(7)
    FFXC.set_value('AxisLy', 0)
    
    while FFX_memory.getMap() != 135:
        pos = FFX_memory.getCoords()
        if FFX_memory.userControl():
            FFXC.set_value('AxisLy', 1)
            if pos[1] < ((-3.08* pos[0]) - 10.82):
                FFXC.set_value('AxisLx', 1)
            else:
                FFXC.set_value('AxisLx', 0)
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if FFX_Screen.BattleScreen():
                FFX_Battle.fleeAll()
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.menuB()
            elif FFX_memory.menuOpen():
                FFXC.set_value('BtnB', 1)
                time.sleep(0.035)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.035)