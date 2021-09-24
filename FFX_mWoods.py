import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_memory

FFXC = FFX_Xbox.FFXC
 
def arrival(rikkucharged):
    FFX_memory.clickToControl()
    if rikkucharged == True:
        FFX_memory.fullPartyFormat_New("mwoodsgotcharge", 11)
    else:
        FFX_memory.fullPartyFormat_New("mwoodsneedcharge", 11)
    FFX_memory.closeMenu()
    #Start by getting away from the save sphere
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    
    print("Start of Macalania Woods section")
    checkpoint = 0
    lastCP = 0
    complete = 0
    woodsVars = [False, False, False] #Rikku's charge, Fish Scales, and Arctic Winds
    woodsVars[0] = rikkucharged
    #As a side note, Rikku is always charged in thunder plains.
    while complete == 0:
        if lastCP != checkpoint:
            print("Checkpoint: ", checkpoint)
            lastCP = checkpoint
        if FFX_memory.userControl():
            #print("Checkpoint: ", checkpoint)
            pos = FFX_memory.getCoords()
            if checkpoint == 0:
                if pos[0] < 10:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] < 33:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            #elif checkpoint == 1:
            #    if pos[0] > -3:
            #        checkpoint = 2
            #    else:
            #        FFXC.set_value('AxisLy', 1)
            #        if pos[0] < -60:
            #            FFXC.set_value('AxisLx', 1)
            #        else:
            #            FFXC.set_value('AxisLx', 0)
            elif checkpoint == 10:
                if pos[1] < 2:
                    checkpoint = 30
                else:
                    FFXC.set_value('AxisLx', -1)
                    FFXC.set_value('AxisLy', 0)
            elif checkpoint == 30:
                if pos[0] < -108:
                    checkpoint = 40
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < -40: 
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 40:
                if pos[1] > 225:
                    checkpoint = 45
                else:
                    cam = FFX_memory.getCamera()
                    if cam[0] > 1.5:
                        FFXC.set_value('AxisLx', 1)
                        FFXC.set_value('AxisLy', 0)
                    else:
                        FFXC.set_value('AxisLx', 0)
                        FFXC.set_value('AxisLy', -1)
            elif checkpoint == 45:
                if pos[0] <= -136 and pos[1] < 230:
                    checkpoint = 50
                else:
                    if pos[0] > -136:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
                    if pos[1] > 230:
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 50:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                FFX_Xbox.SkipDialog(1) #Open chest
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            elif checkpoint == 60:
                if pos[0] > 10:
                    checkpoint = 70
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[0] > -140:
                        FFXC.set_value('AxisLy', -1)
                    else:
                        FFXC.set_value('AxisLy', 1)
            elif checkpoint == 70:
                if pos[1] < -80:
                    checkpoint = 80
                else:
                    FFXC.set_value('AxisLx', -1)
                    FFXC.set_value('AxisLy', 1)
            elif checkpoint == 80:
                if pos[0] < -60:
                    checkpoint = 90
                else:
                    FFXC.set_value('AxisLx', 1)
                    FFXC.set_value('AxisLy', 0)
            elif checkpoint == 90:
                if pos[0] < -85:
                    checkpoint = 100
                else:
                    FFXC.set_value('AxisLx', 1)
                    FFXC.set_value('AxisLy', -1)
            elif checkpoint == 100:
                if pos[0] < -200:
                    checkpoint = 110
                else:
                    FFXC.set_value('AxisLx', 1)
                    FFXC.set_value('AxisLy', 1)
            elif checkpoint == 110:
                if pos[1] < 40:
                    checkpoint = 115
                else:
                    FFXC.set_value('AxisLx', -1)
                    FFXC.set_value('AxisLy', 1)
            elif checkpoint == 115:
                if pos[1] < -1:
                    checkpoint = 120
                else:
                    FFXC.set_value('AxisLx', -1)
                    FFXC.set_value('AxisLy', 0)
            elif checkpoint == 120:
                if pos[0] > 160:
                    checkpoint = 130
                else:
                    FFXC.set_value('AxisLx', -1)
                    FFXC.set_value('AxisLy', -1)
            elif checkpoint == 130:
                if pos[1] < -40:
                    checkpoint = 140
                else:
                    FFXC.set_value('AxisLx', -1)
                    FFXC.set_value('AxisLy', 0)
            elif checkpoint == 140:
                if pos[1] < -40:
                    checkpoint = 150
                else:
                    FFXC.set_value('AxisLx', -1)
                    FFXC.set_value('AxisLy', 0)
            elif checkpoint == 150:
                if pos[1] < -170:
                    checkpoint = 160
                else:
                    FFXC.set_value('AxisLx', -1)
                    FFXC.set_value('AxisLy', 1)
            elif checkpoint == 160:
                if pos[0] < -145:
                    checkpoint = 170
                else:
                    FFXC.set_value('AxisLx', 0)
                    FFXC.set_value('AxisLy', 1) #Up to butterflies
            elif checkpoint == 170:
                if pos[1] > -20:
                    checkpoint = 180
                else:
                    FFXC.set_value('AxisLx', 1)
                    FFXC.set_value('AxisLy', 0) #Into the last zone
            elif checkpoint == 180:
                if pos[1] > 185:
                    checkpoint = 190
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[1] < 70:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 190:
                if pos[1] < -5:
                    checkpoint = 200
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > 70:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', -1) #Up the ramp
            elif checkpoint == 200:
                if pos[0] < -745:
                    checkpoint = 210
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[0] > -570:
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', -1)
            elif checkpoint == 210:
                if pos[1] > 170:
                    checkpoint = 220
                else:
                    FFXC.set_value('AxisLx', 0)
                    FFXC.set_value('AxisLy', -1) #Down the ramp
            elif checkpoint == 220:
                FFXC.set_value('AxisLy', 0)
                if woodsVars[0] == False or woodsVars[1] == False or woodsVars[2] == False:
                    #stepCount -= 1
                    FFXC.set_value('AxisLx', 1)
                    time.sleep(1.5)
                    FFXC.set_value('AxisLx', -1)
                    time.sleep(1.5)
                    FFXC.set_value('AxisLx', 0)
                else:
                    checkpoint = 230
            elif checkpoint == 230:
                #print("checkpoint: ", checkpoint)
                if woodsVars[0] == False or woodsVars[1] == False or woodsVars[2] == False:
                    checkpoint = 220
                elif pos[0] > -605:
                    checkpoint = 240
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', 0)
                else:
                    FFXC.set_value('AxisLx', -1)
                    if pos[0] < -680:
                        FFXC.set_value('AxisLy', 0)
                    elif pos[1] > 130:
                        FFXC.set_value('AxisLy', 1)
                    elif pos[1] < 126:
                        FFXC.set_value('AxisLy', -1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 240:
                #print("checkpoint: ", checkpoint)
                if pos[0] > 1:
                    checkpoint = 250
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] < 0:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 250:
                print("Mark")
                FFXC.set_value('AxisLx', -1)
                FFXC.set_value('AxisLy', 0)
                time.sleep(0.3)
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                FFX_Xbox.touchSaveSphere()
                FFXC.set_value('AxisLx', 1)
                FFXC.set_value('AxisLy', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                complete = 1
        elif FFX_Screen.BattleScreen():
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            print("Starting battle")
            print("variable check 1: ",woodsVars)
            woodsVars = FFX_Battle.mWoods(woodsVars)
            print("variable check 2: ",woodsVars)
        elif FFX_memory.userControl() == False:
            if checkpoint == 50 and FFX_Screen.PixelTestTol(923,441,(219, 219, 219),5):
                print("Chest is opened.")
                FFX_memory.clickToControl()
                checkpoint = 60
            elif checkpoint > 80:
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                FFX_Xbox.menuB()
            else:
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)

def lakeRoad():
    if FFX_memory.getSpeed() < 12:
        FFX_memory.setSpeed(12)
    FFX_menu.mWoods() #Selling and buying, item sorting, etc
    FFX_memory.fullPartyFormat('spheri')
    FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    time.sleep(4)
    FFXC.set_value('AxisLx', -1)
    time.sleep(4)
    FFXC.set_value('AxisLy', 0) #Engage Spherimorph
    
    FFX_Battle.spherimorph()
    print("Battle is over.")
    FFX_Xbox.SkipDialog(3)
    FFX_memory.clickToControl() #Jecht's memories
    
def lakeRoad2():
    FFXC.set_value('AxisLy', -1)
    time.sleep(6)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl() #Auron's musings.
    FFXC.set_value('AxisLy', -1)
    FFX_Xbox.SkipDialog(3.5)
    FFXC.set_value('AxisLx', -1)
    FFX_memory.clickToEvent(3.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_memory.clickToControl() #Last map in the woods
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(4)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)

def lake():
    print("Now to the frozen lake")
    FFX_memory.fullPartyFormat('crawler')
    FFX_memory.awaitControl()
    FFX_menu.mLakeGrid()
    
    complete = 0
    checkpoint = 0
    lastCP = 0
    while checkpoint != 100:
        if lastCP != checkpoint:
            print("Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        if FFX_memory.userControl():
            battle = FFX_memory.getBattleNum()
            #cam = FFX_memory.getCamera()
            pos = FFX_memory.getCoords()
            if checkpoint == 0:
                if pos[0] < 50:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((0.56 * pos[0]) - 55):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 10:
                if pos[1] < -215:
                    checkpoint = 20
                else:
                    FFXC.set_value('AxisLx', -1)
                    if pos[1] < -120:
                        FFXC.set_value('AxisLy', -1)
                    elif pos[1] < ((1.92 * pos[0]) -101.65):
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 20:
                FFXC.set_value('AxisLy', -1)
                FFXC.set_value('AxisLx', -1)
        elif FFX_Screen.BattleScreen():
            FFX_Battle.fleeAll()
        elif FFX_Screen.PixelTest(614,98,(234, 194, 0)): #Negator pop-up
            checkpoint = 100
        else:
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
            FFX_Xbox.menuB() #Skipping dialog
    
    FFX_Battle.negator()

def afterCrawler():
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.3)
    FFXC.set_value('AxisLx', 0)
    time.sleep(4)
    FFXC.set_value('AxisLy', 0)

    FFX_memory.clickToControl()
    
    checkpoint = 0
    lastCP = 0
    while checkpoint != 100:
        if lastCP != checkpoint:
            print("Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        pos = FFX_memory.getCoords()
        if checkpoint == 0:
            if pos[0] > 130:
                checkpoint = 10
            else:
                FFXC.set_value('AxisLx', -1)
                if pos[1] < ((1.99 * pos[0]) + 5):
                    FFXC.set_value('AxisLy', -1)
                else:
                    FFXC.set_value('AxisLy', 0)
        elif checkpoint == 10:
            if pos[0] > 450:
                checkpoint = 20
            else:
                FFXC.set_value('AxisLx', -1)
                if pos[1] > ((0.37 * pos[0]) + 240):
                    FFXC.set_value('AxisLy', 1)
                elif pos[1] > 385:
                    FFXC.set_value('AxisLy', 1)
                else:
                    FFXC.set_value('AxisLy', 0)
        elif checkpoint == 20:
            if pos[0] > 690:
                checkpoint = 40
            else:
                FFXC.set_value('AxisLx', -1)
                if pos[1] > ((-0.65 * pos[0]) + 693):
                    FFXC.set_value('AxisLy', 1)
                else:
                    FFXC.set_value('AxisLy', 0)
        elif checkpoint == 30:
            if pos[1] < 100:
                checkpoint = 40
            else:
                FFXC.set_value('AxisLy', 1)
                if pos[1] < ((-1.49 * pos[0]) + 1235):
                    FFXC.set_value('AxisLx', -1)
                else:
                    FFXC.set_value('AxisLy', 0)
        elif checkpoint == 40:
            if FFX_memory.getMap() == 106:
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                checkpoint = 100
            else:
                FFXC.set_value('AxisLy', 1)
                if pos[0] > 815:
                    FFXC.set_value('AxisLx', 1)
                elif pos[0] < 810:
                    FFXC.set_value('AxisLx', -1)
                else:
                    FFXC.set_value('AxisLx', 0)
    print("End of Macalania Woods section. Next is temple section.")

