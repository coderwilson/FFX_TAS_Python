import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory

FFXC = FFX_Xbox.FFXC
 
def arrival(blitzWin):
    print("Starting Macalania Temple section")
    if FFX_memory.getPower() < 26:
        FFX_memory.setPower(26) #Need 34 from here forward. 2 from Wendigo and 6 from bombs. 26 needed here.
    FFX_Screen.clickToMap1()
    FFX_menu.macTemple(blitzWin)
    #Start by getting away from the save sphere
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.4)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.15)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.touchSaveSphere()
    
    FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.3)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.3)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.3)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.085) #Shifting right
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.04)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.2)
    FFX_Xbox.menuB()
    
    FFX_Screen.clickToPixel(666,439,(223, 223, 223))
    time.sleep(0.5)
    FFX_Xbox.menuB()
    time.sleep(0.8)
    
    success = 0
    reportSkip = 0
    while success == 0:
        #Engage the skip (at least try)
        FFXC.set_value('AxisLx', 1)
        time.sleep(0.08)
        FFXC.set_value('BtnB', 1)
        time.sleep(0.1)
        FFXC.set_value('AxisLx', 0)
        FFXC.set_value('BtnB', 0)
        time.sleep(1.5)
        if FFX_Screen.PixelTest(577,809,(23, 23, 23)):
            reportSkip = 1
            print("Jyscal Skip successful.")
            success = 1
            FFX_Xbox.menuB() #Skip dialog (first)
            time.sleep(1.5)
            FFX_Xbox.menuB() #Skip dialog (second)
            time.sleep(0.5)
            FFXC.set_value('AxisLy', 1)
            FFXC.set_value('AxisLx', -1)
            time.sleep(0.6)
            FFXC.set_value('AxisLx', 0)
            time.sleep(1)
            FFXC.set_value('AxisLx', -1)
            time.sleep(1)
            FFXC.set_value('AxisLy', 0)
            time.sleep(1)
            FFXC.set_value('AxisLx', 0)
            FFX_Xbox.menuB()
            time.sleep(2.5)
            FFX_Xbox.menuB()
            time.sleep(0.3)
            FFXC.set_value('AxisLx', -1)
            time.sleep(1.5)
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', -1)
            time.sleep(2.5)
            FFXC.set_value('AxisLy', 0)
            
            FFX_Xbox.SkipDialog(2)
            FFXC.set_value('AxisLy', -1)
            time.sleep(3.5)
            FFXC.set_value('AxisLy', 0) # Through the door
        else:
            print("Jyscal Skip failed. Going to try again.")
            FFX_Xbox.menuB() #Skip dialog (first)
            FFX_Screen.awaitMap1()
    
    #After the skip
    while not FFX_Screen.PixelTestTol(658,9,(100, 105, 97),5):
        if FFX_Screen.Minimap1():
            reportSkip = 2
            print("Jyscal Skip failed. Backup strats.")
            FFXC.set_value('AxisLx', 1)
            FFXC.set_value('AxisLy', 1)
            time.sleep(3)
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            FFX_Screen.awaitMap1() #A sphere in Lady Yuna's belongings?
            FFXC.set_value('AxisLx', 1)
            time.sleep(2)
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 1)
            time.sleep(3)
            FFXC.set_value('AxisLy', 0)
            FFX_Screen.clickToPixel(215,224,(64, 193, 64)) #Jyscal scene
            FFXC.set_value('AxisLy', -1)
            time.sleep(1)
            FFXC.set_value('AxisLy', 0)
            FFX_Screen.awaitMap1()
            FFXC.set_value('AxisLy', -1)
            time.sleep(2.3)
            FFXC.set_value('AxisLy', 1)
            time.sleep(5)
            FFXC.set_value('AxisLy', 0)
        else:
            FFX_Xbox.menuB()
    
    FFX_Logs.writeStats("Jyscal skip:")
    if reportSkip == 1:
        FFX_Logs.writeStats("Yes")
    elif reportSkip == 2:
        FFX_Logs.writeStats("No")
    
    FFXC.set_value('AxisLy', 1)
    time.sleep(20)
    FFXC.set_value('AxisLy', 1)
    
    FFX_Battle.seymourGuado()
    
    time.sleep(2)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() #Confirm name for Shiva
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 0)
    time.sleep(4.5)
    FFXC.set_value('AxisLx', 0)

def trials():
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(8)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1.8)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.68) #Lining up with pedestol
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0) #Push the first pedestol
    
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.3)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.55)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.awaitControl()
    
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLx', 0)
    FFX_Screen.clickToPixel(930,830,(234, 140, 0)) #Removed Macalania sphere
    time.sleep(0.1)
    FFX_Xbox.menuB()
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.5)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.7)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1.3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.1)
    FFXC.set_value('AxisLx', 0) #Pedestol, lower level
    FFX_Xbox.menuB()
    time.sleep(0.5)
    FFX_Xbox.menuB()
    time.sleep(0.5)
    FFX_Xbox.menuB()
    time.sleep(1.5)
    FFX_Xbox.menuB()
    FFX_memory.awaitControl()
    
    
    FFXC.set_value('AxisLx', 1) #Push pedestol on lower level
    time.sleep(0.8)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.2)
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.9)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.3)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.3)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.menuB()
    time.sleep(0.5)
    FFX_Xbox.menuB()
    time.sleep(1.5)
    FFX_Xbox.menuB() # Pick up glyph sphere
    FFX_memory.awaitControl()
    
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.3)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.6)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.3)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1.3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.6)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.1)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.menuB()
    time.sleep(0.5)
    FFX_Xbox.menuB()
    time.sleep(0.5)
    FFX_Xbox.menuB()
    time.sleep(1.5)
    FFX_Xbox.menuB() #Insert glyph sphere
    FFX_memory.awaitControl()
    
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.4)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.2)
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.9)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.3)
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.menuB()
    time.sleep(0.5)
    FFX_Xbox.menuB()
    time.sleep(1.5)
    FFX_Xbox.menuB() # Pick up Macalania sphere
    FFX_memory.awaitControl()
    
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(2.5)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.5)
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.7)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.3)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.menuB()
    time.sleep(0.5)
    FFX_Xbox.menuB()
    time.sleep(0.5)
    FFX_Xbox.menuB()
    time.sleep(1.5)
    FFX_Xbox.menuB() #Insert Macalania sphere
    FFX_memory.awaitControl()
    
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1)
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.5)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.menuB()
    time.sleep(0.5)
    FFX_Xbox.menuB()
    time.sleep(1.5)
    FFX_Xbox.menuB() # Pick up Macalania sphere
    FFX_memory.awaitControl()
    
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1.9)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.3)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.menuB()
    time.sleep(0.5)
    FFX_Xbox.menuB()
    time.sleep(0.5)
    FFX_Xbox.menuB()
    time.sleep(1.5)
    FFX_Xbox.menuB() #Insert Macalania sphere
    FFX_memory.awaitControl()
    
    FFXC.set_value('AxisLy', 1) #Let's get out of here.
    time.sleep(0.7)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.6)
    FFXC.set_value('AxisLy', 0)
    time.sleep(1)
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.6)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    time.sleep(7)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.awaitMap1() #Back into the main room.
    FFXC.set_value('AxisLy', -1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)

def escape():
    FFX_memory.clickToControl()
    FFX_menu.autoSortItems('n')
    FFX_menu.afterSeymour()
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', -1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.touchSaveSphere()
    
    FFX_memory.awaitControl()
    FFX_memory.fullPartyFormat('macalaniaescape')
    checkpoint = 0
    lastCP = 0
    while checkpoint != 1000:
        #print("Checkpoint: ", checkpoint)
        if lastCP != checkpoint:
            print("Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        if FFX_Screen.BattleScreen():
            if FFX_memory.getBattleNum() == 195:
                checkpoint = 1000
            else:
                FFX_Xbox.tidusFlee()
                FFX_memory.clickToControl()
        elif FFX_memory.userControl():
            pos = FFX_memory.getCoords()
            if checkpoint == 0:
                #print("Movement ", checkpoint)
                if pos[1] > 80:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[0] > 805:
                        FFXC.set_value('AxisLx', 1)
                    elif pos[0] < 800:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 10:
                #print("Movement ", checkpoint)
                if pos[0] < 620:
                    checkpoint = 20
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[1] > ((-1.49 * pos[0]) + 1235):
                        FFXC.set_value('AxisLx', 1)
                    elif pos[1] > ((-0.65 * pos[0]) + 700):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 20:
                #print("Movement ", checkpoint)
                if pos[0] < 430:
                    checkpoint = 30
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[1] > 390:
                        FFXC.set_value('AxisLy', 1)
                    elif pos[1] > 385:
                        FFXC.set_value('AxisLy', 0)
                    elif pos[1] < ((-0.65 * pos[0]) + 700):
                        FFXC.set_value('AxisLy', -1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 30:
                #print("Movement ", checkpoint)
                if FFX_memory.getMap() == 192:
                    checkpoint = 40
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[1] > ((0.37 * pos[0]) + 240):
                        FFXC.set_value('AxisLy', 1)
                    elif pos[1] > ((2.94 * pos[0]) + -56):
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
                    
            elif checkpoint == 40:
                #Second screen.
                #print("Movement ", checkpoint)
                #print("Placeholder - section not yet programmed")
                if pos[1] < 390:
                    checkpoint = 50
                else:
                    FFXC.set_value('AxisLy', -1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 50:
                if pos[1] < 230:
                    checkpoint = 60
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[0] > 36:
                        FFXC.set_value('AxisLy', -1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 60:
                if pos[0] < -32:
                    checkpoint = 70
                else:
                    FFXC.set_value('AxisLy', -1)
                    FFXC.set_value('AxisLx', -1)
            elif checkpoint == 70:
                if pos[1] < -145:
                    checkpoint = 80
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[0] < -35:
                        FFXC.set_value('AxisLx', 1)
                    if pos[0] > -15:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 80:
                FFXC.set_value('AxisLy', -1)
                if pos[0] < -15:
                    FFXC.set_value('AxisLx', 1)
                else:
                    FFXC.set_value('AxisLx', 0)
        else:
            #print("No action ", checkpoint)
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
    
    print("Done pathing. Now for the Wendigo fight.")
    FFX_Battle.wendigo()
    print("Wendigo fight over")
    

def escape_old():
    FFX_Screen.clickToMap1()
    FFX_menu.afterSeymour()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1.9)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.touchSaveSphere()
    
    FFX_memory.awaitControl()
    
    FFXC.set_value('AxisLy', -1)
    time.sleep(8)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    time.sleep(12)
    FFXC.set_value('AxisLx', 0)
    FFX_Battle.fleeAll()
    
    FFXC.set_value('AxisLx', 1)
    time.sleep(10)
    FFXC.set_value('AxisLx', 0)
    FFX_Battle.fleeAll()
    
    FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLx', 1)
    time.sleep(5)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.awaitMap1()
    #return #Testing only
    
    complete = 0
    stepCount = 0
    stepMax = 500
    while complete == 0:
        if FFX_Screen.BattleScreen():
            if FFX_memory.getBattleNum() == 195:
                print("Seymour escape complete.")
                complete = 1
            else:
                FFX_Battle.fleeAll()
        elif FFX_Screen.BattleComplete():
            FFX_Xbox.menuB()
        elif not FFX_memory.userControl():
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
        else:
            stepCount += 1
            print("Seymour escape pathing: ", stepCount)
            if stepCount < 13:
                FFXC.set_value('AxisLy', -1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.2)
            elif stepCount < 22:
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.2)
            elif stepCount == 35:
                FFXC.set_value('AxisLy', -1)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
            elif stepCount < 300:
                FFXC.set_value('AxisLy', -1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.2)
            elif stepCount < stepMax:
                print("Max step count exceeded. Awaiting user input. ", stepCount)
                time.sleep(5)
            else: complete = 1
    
    FFX_Battle.wendigo()
    print("Wendigo fight over")
    
def underLake():
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.8)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.5) #Approach Yuna
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    while FFX_memory.getCoords()[1] > 110:
        FFXC.set_value('AxisLx', -1)
    while FFX_memory.getCoords()[1] > 85:
        FFXC.set_value('AxisLx', 1)
    while FFX_memory.getCoords()[0] > -30:
        if FFX_memory.getCoords()[1] < 110:
            FFXC.set_value('AxisLy', -1)
        else:
            FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 1)
    FFX_memory.clickToEvent() #Chest with Lv.2 Key Sphere
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.SkipDialog(0.2)
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.25)
    while FFX_memory.getCoords()[0] < -5:
        FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    time.sleep(1) #To Auron
    FFX_Xbox.SkipDialog(1.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 1)
    FFX_Xbox.SkipDialog(0.4)
    FFXC.set_value('AxisLx', -1)
    FFX_Xbox.SkipDialog(0.4)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.clickToControl()
    
    FFXC.set_value('AxisLy', -1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    time.sleep(10)
    FFX_Xbox.skipScene()
    
    #Now at the oasis
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLy', 1)
    time.sleep(5)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.9)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.touchSaveSphere()