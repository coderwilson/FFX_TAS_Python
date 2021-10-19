import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_memory
import FFX_targetPathing

FFXC = FFX_Xbox.FFXC

def arrival():
    print("Starting Moonflow section")
    
    checkpoint = 0
    while FFX_memory.getMap() != 235:
        if FFX_memory.userControl():
            #Chests
            if checkpoint == 2: #Gil outside Djose temple
                print("Djose gil chest")
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
                FFX_Xbox.SkipDialog(1)
                FFXC.set_value('AxisLy', -1)
                FFXC.set_value('AxisLx', 1)
                FFX_memory.clickToControl()
                checkpoint += 1
            elif checkpoint == 33: #Moonflow chest
                print("Moonflow chest")
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            
            #Map changes
            elif checkpoint < 6 and FFX_memory.getMap() == 76:
                checkpoint = 6
            elif checkpoint < 11 and FFX_memory.getMap() == 93:
                checkpoint = 11
            elif checkpoint < 14 and FFX_memory.getMap() == 75:
                checkpoint = 14
            elif checkpoint < 39 and FFX_memory.getMap() == 105:
                checkpoint = 39
            elif checkpoint < 44 and FFX_memory.getStoryProgress() == 1045:
                checkpoint = 44
                print("Updating checkpoint based on story/map progress: ", checkpoint)
            elif checkpoint == 44 and FFX_memory.getMap() == 188:
                checkpoint = 45
                print("Updating checkpoint based on story/map progress: ", checkpoint)
                
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.moonflow(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if FFX_Screen.BattleScreen():
                FFX_Battle.fleeAll()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    print("End of approaching section, should now be talking to Lucille/Elma/etc.")

def arrival_old():
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
    print("South bank, Save sphere screen")
    
    #FFX_memory.clickToControl() #Screen with the Shoopuff platform
    #FFXC.set_value('AxisLx', -1)
    #time.sleep(3)
    #FFXC.set_value('AxisLx', 0)
    
    FFX_memory.clickToControl3() # "Where there's a will, there's a way."
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl3()
    partyHP = FFX_memory.getHP()
    if partyHP[4] < 800:
        FFX_Battle.healUp(2)
    elif partyHP[0] < 700:
        FFX_Battle.healUp(1)
    FFX_memory.closeMenu()
    
    checkpoint = 0
    while FFX_memory.getMap() != 291:
        if FFX_memory.userControl():
            if checkpoint == 4:
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                FFX_memory.clickToEvent()
                time.sleep(0.6)
                FFX_Xbox.menuB() #Ride ze Shoopuff?
                time.sleep(0.6)
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB() #All aboardz!
                FFX_Xbox.SkipDialog(3) #Just to clear some dialog
        
            elif FFX_targetPathing.setMovement(FFX_targetPathing.moonflowBankSouth(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
    
    
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
    
    checkpoint = 0
    print("Miihen North Bank pattern. Starts after talking to Auron.")
    while FFX_memory.getMap() != 135:
        if FFX_memory.userControl():
            if checkpoint == 7: #Rikku steal/mix tutorial
                FFXC.set_value('AxisLx', 1)
                FFXC.set_value('AxisLy', 1)
                FFX_memory.awaitEvent()
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                FFX_Battle.mixTutorial()
                FFX_memory.fullPartyFormat("postbunyip")
                FFX_memory.closeMenu()
                checkpoint += 1
            elif FFX_memory.getStoryProgress() >= 1085 and checkpoint < 4:
                checkpoint = 4
                print("Rikku scene, updating checkpoint: ", checkpoint)
                
            #Map changes
            elif checkpoint < 2 and FFX_memory.getMap() == 109:
                checkpoint = 2
            elif checkpoint < 12 and FFX_memory.getMap() == 97:
                checkpoint = 12
            
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.moonflowBankNorth(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
            if FFX_Screen.BattleScreen():
                FFX_Battle.fleeAll()
            elif FFX_memory.diagSkipPossible() and FFX_memory.battleActive() == False:
                FFX_Xbox.tapB()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
    
    
def northBankOldPathing():
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