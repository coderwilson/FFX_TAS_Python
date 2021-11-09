import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_memory
import FFX_Logs
import FFX_targetPathing

FFXC = FFX_Xbox.FFXC
 
def arrival():
    print("Waiting for Yuna/Tidus to stop laughing.")
    FFX_memory.clickToControl()
    print("Now onward to scenes and Mi'ihen skip. Good luck!")
    
    FFX_memory.fullPartyFormat('miihen')
    selfDestruct = 0
    miihenSkip = False
    battleCount = 0
    SDbattleNum = 0
    
    checkpoint = 0
    while FFX_memory.getMap() != 120:
        if FFX_memory.userControl():
        
            #Miihen skip attempt
            if checkpoint == 6:
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                time.sleep(0.3)
                checkpoint += 1
            elif checkpoint == 7:
                if FFX_memory.getCoords()[1] > 1354: #Into position
                    checkpoint += 1
                    print("Close to the spot")
                    print(FFX_memory.getCoords())
                elif FFX_memory.getCoords()[0] < -44.5: #Into position
                    FFXC.set_value('AxisLx', 1)
                    FFXC.set_value('AxisLy', 1)
                    time.sleep(0.07)
                    FFXC.set_value('AxisLx', 0)
                    FFXC.set_value('AxisLy', 0)
                    time.sleep(0.15)
                else:
                    FFXC.set_value('AxisLy', 1)
                    time.sleep(0.07)
                    FFXC.set_value('AxisLy', 0)
                    time.sleep(0.15)
            elif checkpoint == 8:
                if FFX_memory.getCoords()[0] > -44.5: #Into position
                    checkpoint += 1
                    print("Adjusting for horizontal position - complete")
                    print(FFX_memory.getCoords())
                else:
                    FFXC.set_value('AxisLx', 1)
                    time.sleep(0.07)
                    FFXC.set_value('AxisLx', 0)
                    time.sleep(0.15)
            elif checkpoint == 9:
                if FFX_memory.getCoords()[1] > 1357.5: #Into position
                    checkpoint += 1
                    print("Stopped and ready for the skip.")
                    print(FFX_memory.getCoords())
                else:
                    FFXC.set_value('AxisLy', 1)
                    time.sleep(0.07)
                    FFXC.set_value('AxisLy', 0)
                    time.sleep(0.2)
            elif checkpoint == 10:
                if FFX_memory.miihenGuyCoords()[1] < 1380: #Spear guy's position when we start moving. 
                    print("Skip engaging!!! Good luck!")
                    #Greater number for spear guy's position means we will start moving faster.
                    #Smaller number means moving later.
                    FFXC.set_value('AxisLy', 1)
                    time.sleep(0.2)
                    FFX_Xbox.SkipDialog(0.5) #Walk into the guy mashing B (or X, or whatever the key is)
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', 0) #Stop trying to move. (recommended by Crimson)
                    print("Starting special skipping.")
                    FFX_Xbox.SkipDialogSpecial(3) #Mash two buttons
                    print("End special skipping.")
                    print("Should now be able to see if it worked.")
                    time.sleep(3.5) #Don't move, avoiding a possible extra battle
                    FFX_memory.clickToControl3()
                    print("Mark 1")
                    time.sleep(1)
                    print("Mark 2")
                    try:
                        if FFX_memory.lucilleMiihenCoords()[1] > 1400 and FFX_memory.userControl():
                            miihenSkip = True
                        else:
                            FFX_memory.clickToControl3()
                    except:
                        miihenSkip = False
                    print("Skip successful: ", miihenSkip)
                    checkpoint += 1
            
            #Map changes
            elif checkpoint < 15 and FFX_memory.getMap() == 120:
                checkpoint = 15
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.miihen(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if FFX_Screen.BattleScreen():
                if checkpoint < 4: #Tutorial battle with Auron
                    FFX_memory.clickToControl()
                elif checkpoint == 25 and FFX_memory.battleActive() == False: #Shelinda dialog
                    FFX_Xbox.tapB()
                else:
                    print("Starting battle")
                    battleCount += 1
                    if selfDestruct == 0:
                        selfDestruct = FFX_Battle.MiihenRoad(selfDestruct)
                        if selfDestruct != 0:
                            SDbattleNum = battleCount
                    else:
                        FFX_Battle.MiihenRoad(selfDestruct)
                    print("Battle complete")
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    print("Miihen skip status: ", miihenSkip)
    return [selfDestruct, battleCount, SDbattleNum]

def arrival2(selfDestruct, battleCount, SDbattleNum):
    print("Start of the second map")
    checkpoint = 15
    while FFX_memory.getMap() != 171:
        if FFX_memory.userControl():
            
            #Map changes
            if checkpoint == 27:
                if FFX_memory.getCoords()[1] > 2810:
                    checkpoint += 1
                else:
                    FFXC.set_value('AxisLx', 0)
                    FFXC.set_value('AxisLy', 0)
                    FFX_Xbox.SkipDialog(4)
                    if FFX_memory.userControl():
                        FFX_memory.clickToControl3()
                        checkpoint += 1
            
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.miihen(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if FFX_Screen.BattleScreen():
                battleCount += 1
                if checkpoint == 27 and FFX_memory.battleActive() == False: #Shelinda dialog
                    FFX_Xbox.tapB()
                else:
                    print("Starting battle")
                    if selfDestruct == 0:
                        selfDestruct = FFX_Battle.MiihenRoad(selfDestruct)
                        if selfDestruct != 0:
                            SDbattleNum = battleCount
                    else:
                        FFX_Battle.MiihenRoad(selfDestruct)
                    print("Battle complete")
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif FFX_memory.diagSkipPossible(): #Exclude during the Miihen skip.
                if checkpoint < 6 or checkpoint > 12:
                    FFX_Xbox.tapB()
            
            #Map changes
            elif checkpoint < 13 and FFX_memory.getMap() == 120:
                checkpoint = 13
            elif checkpoint < 20 and FFX_memory.getMap() == 127:
                checkpoint = 20
            elif checkpoint < 31 and FFX_memory.getMap() == 58:
                checkpoint = 31
    return [selfDestruct, battleCount, SDbattleNum]

def miihenPath_Old():
    checkpoint = 0
    lastCP = 0
    while checkpoint != 100:
        pos = FFX_memory.getCoords()
        pos2 = FFX_memory.miihenGuyCoords()
        if lastCP != checkpoint:
            print("Checkpoint: ", checkpoint)
            lastCP = checkpoint
        if FFX_memory.getMap() == 58 or FFX_memory.getStoryProgress() >= 750:
            checkpoint = 100
        elif FFX_memory.userControl():
            #print("Spear guy coords: ", pos2)
            #print(checkpoint)
            if checkpoint == 0:
                if pos[1] > 1345: #Close to skip position, but not quite in position.
                    checkpoint = 3
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > 1230 and pos[0] < -47:
                        FFXC.set_value('AxisLx', 1)
                    elif pos[1] > 1230 and pos[0] > -41:
                        FFXC.set_value('AxisLx', -1)
                    elif pos[1] > 1080 and pos[1] < 1120 and pos[0] < -30:
                        FFXC.set_value('AxisLx', 1)
                    elif pos[1] < 1080 and pos[0] > -20:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 3:
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                time.sleep(0.3)
                checkpoint = 8
            elif checkpoint == 8:
                if pos[1] > 1358: #Into position - Inching forward. Stop at this point.
                    checkpoint = 10
                    FFXC.set_value('AxisLx', 0)
                    FFXC.set_value('AxisLy', 0)
                else:
                    FFXC.set_value('AxisLy', 1)
                    time.sleep(0.1)
                    FFXC.set_value('AxisLy', 0)
                    time.sleep(0.1)
            elif checkpoint == 10: #Waiting for the spear guy.
                if pos2[1] < 1379: #Spear guy's position when we start moving. 
                    #Greater number for spear guy's position means we will start moving faster.
                    #Smaller number means moving later.
                    FFXC.set_value('AxisLy', 1)
                    time.sleep(0.20)
                    FFX_Xbox.SkipDialog(1.5) #Walk into the guy mashing B (or X, or whatever the key is)
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', 0) #Stop trying to move. (recommended by Crimson)
                    FFX_Xbox.SkipDialogSpecial(6) #Mash two buttons
                    checkpoint = 20
            elif checkpoint == 20:
                if pos[1] < 500:
                    checkpoint = 30
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 30:
                if pos[1] > 900:
                    checkpoint = 40
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 1) #Diagonal section (Callie)
            elif checkpoint == 40:
                if pos[1] < 700:
                    checkpoint = 50
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 1) #Diagonal section (Callie)
            elif checkpoint == 50:
                if pos[1] > 2770:
                    checkpoint = 60
                else:
                    if pos[0] < -25:
                        FFXC.set_value('AxisLy', 0)
                    else:
                        FFXC.set_value('AxisLy', 1)
                    if pos[0] < -20:
                        FFXC.set_value('AxisLx', 1)
                    elif pos[0] > 10:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 60:
                if pos[1] > 2900:
                    checkpoint = 70
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
                    FFX_Xbox.menuB()
            elif checkpoint == 70:
                FFXC.set_value('AxisLy', 1)
                if pos[1] < 900:
                    FFXC.set_value('AxisLx', 1)
                elif pos[0] < -30:
                    FFXC.set_value('AxisLx', 1)
                elif pos[0] > 10:
                    FFXC.set_value('AxisLx', -1)
                else:
                    FFXC.set_value('AxisLx', 0)
        elif FFX_Screen.BattleScreen():
            print("Starting battle")
            if selfDestruct == 0:
                selfDestruct = FFX_Battle.MiihenRoad(selfDestruct)
                if FFX_memory.menuOpen() and FFX_memory.userControl() == False:
                    FFX_memory.clickToControl() # After-battle screen is still open.
            else:
                FFX_Battle.MiihenRoad(selfDestruct)
                if FFX_memory.menuOpen() and FFX_memory.userControl() == False:
                    FFX_memory.clickToControl() # After-battle screen is still open.
            print("Battle complete")
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
        elif checkpoint == 10 and FFX_Screen.PixelTestTol(478,768,(222, 222, 222),5):
            print("Talking to the guy for free spear.")
            time.sleep(1.2)
            FFX_Xbox.menuB() #Close dialog
            time.sleep(0.6)
            FFXC.set_value('BtnB', 1)
            time.sleep(0.035)
            FFXC.set_value('BtnB', 0)
            #while not FFX_memory.menuOpen():
            #    FFXC.set_value('BtnY', 1)
            #    time.sleep(0.035)
            #    FFXC.set_value('BtnY', 0)
            #    time.sleep(0.035)
            #time.sleep(2)
            #FFXC.set_value('BtnA', 1)
            #time.sleep(0.35)
            #FFXC.set_value('BtnA', 0)
            FFXC.set_value('AxisLy', 1)
            time.sleep(0.4)
            FFXC.set_value('BtnB', 1)
            time.sleep(0.05)
            FFXC.set_value('BtnB', 0)
            FFXC.set_value('AxisLy', 0)
            for x in range(50):
                FFXC.set_value('BtnB', 1)
                time.sleep(0.035)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.035)
                
            
            #Now to try to skip into the next scene
            checkpoint = 20
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
    print("Travel agency")
    if FFX_memory.getStoryProgress() < 750:
        FFXC.set_value('AxisLy', 1)
        FFX_Xbox.SkipDialog(10)
        FFXC.set_value('AxisLy', 0)
    return selfDestruct

def midPoint():
    #Should now be at the Mi'ihen travel agency.
    FFX_memory.clickToControl3()
    
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.6)
    FFXC.set_value('AxisLx', -1)
    time.sleep(20)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    print("Evening scene")
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.clickToControl3() #Dude gives us some Lv.1 spheres
    
    print("Let's grab some P.downs")
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.4)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.3)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.menuB()
    time.sleep(1.5)
    FFX_Xbox.menuB()
    time.sleep(1.5)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(1.5)
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() #Extra P.downs
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    
    #Start conversation with Rin
    FFXC.set_value('AxisLy', -1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    print("Conversation with Rin")
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0) #Leave the shop
    
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    FFX_Battle.chocoEater()

def lowRoad(selfDestruct, battleCount, SDbattleNum): #Starts just after the save sphere.

    checkpoint = 0
    while FFX_memory.getMap() != 79:
        if FFX_memory.userControl():
            #Utility stuff
            if checkpoint == 2:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.2)
                FFX_Xbox.menuB()
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.8)
                FFX_Xbox.menuB()
                time.sleep(0.8)
                FFX_Xbox.menuB()
                time.sleep(0.8)
                FFX_Xbox.menuA()
                FFX_Xbox.menuB()
                time.sleep(0.8)
                checkpoint += 1
            elif checkpoint == 26 and selfDestruct == 0:
                checkpoint = 24
            elif checkpoint == 34: #Talk to guard, then Seymour
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0)
                FFX_memory.awaitEvent()
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.2)
                FFX_memory.clickToControl()
                FFXC.set_value('AxisLy', -1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(4)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                checkpoint += 1
            
            #Map changes
            elif checkpoint < 17 and FFX_memory.getMap() == 116:
                checkpoint = 17
            elif checkpoint < 28 and FFX_memory.getMap() == 59:
                checkpoint = 28
            
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.lowRoad(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
            elif checkpoint == 25: #Shelinda dialog
                FFX_Xbox.tapB()
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if FFX_Screen.BattleScreen():
                battleCount += 1
                print("Starting battle")
                if selfDestruct == 0:
                    selfDestruct = FFX_Battle.MiihenRoad(selfDestruct)
                    if selfDestruct != 0:
                        SDbattleNum = battleCount
                    if FFX_memory.menuOpen() and FFX_memory.userControl() == False:
                        FFX_memory.clickToControl() # After-battle screen is still open.
                else:
                    FFX_Battle.MiihenRoad(selfDestruct)
                    if FFX_memory.menuOpen() and FFX_memory.userControl() == False:
                        FFX_memory.clickToControl() # After-battle screen is still open.
                print("Battle complete")
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif FFX_memory.diagSkipPossible():
                if checkpoint < 6 or checkpoint > 12:
                    FFX_Xbox.tapB()
    FFX_Logs.writeStats('Miihen encounters:')
    FFX_Logs.writeStats(battleCount)
    FFX_Logs.writeStats('SelfDestruct Learned:')
    FFX_Logs.writeStats(SDbattleNum)

def lowRoad_old(selfDestruct): #Starts just after the save sphere.
    print("Starting low road section.")
    if selfDestruct == 0:
        print("Self Destruct has not yet been learned.")
    else:
        print("Self Destruct already learned. Good to go.")
    checkpoint = 0
    while checkpoint != 100:
        if FFX_Screen.BattleScreen():
            print("Starting battle")
            if selfDestruct == 0:
                selfDestruct = FFX_Battle.MiihenRoad(selfDestruct)
            else:
                FFX_Battle.MiihenRoad(selfDestruct)
            print("Battle complete")
        else:
            #print("Lowroad, Checkpoint: ", checkpoint)
            pos = FFX_memory.getCoords()
            if pos == [0.0,0.0]: #This means we've lost control of the character for any reason.
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                FFX_Xbox.menuB()
            elif checkpoint == 0:
                if pos[1] > -350:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 10:
                if pos[0] < 30:
                    checkpoint = 20
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', -1)
                    
            elif checkpoint == 20:
                if pos[1] > 0:
                    checkpoint = 30
                else:
                    if pos[0] < -5:
                        FFXC.set_value('AxisLy', 0)
                    else:
                        FFXC.set_value('AxisLy', 1)
                    if pos[0] < 0:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 30:
                if pos[0] > 220:
                    checkpoint = 40
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 1) #To the next zone
            elif checkpoint == 40:
                if pos[0] > 450:
                    checkpoint = 50
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 1)
            elif checkpoint == 50:
                if pos[0] > 600:
                    checkpoint = 60
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 60:
                FFXC.set_value('AxisLx', 0)
                if selfDestruct != 0:
                    FFXC.set_value('AxisLy', 0)
                    checkpoint = 70
                else:
                    FFXC.set_value('AxisLy', -1)
                    time.sleep(1)
                    FFXC.set_value('AxisLy', 1)
                    time.sleep(1)
                    FFXC.set_value('AxisLy', 0) #Wait for SelfDestruct if needed
            elif checkpoint == 70:
                if pos[1] < 0:
                    checkpoint = 80
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', -1)
            elif checkpoint == 80:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(5.8)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.5)
                FFXC.set_value('AxisLx', 0)
                checkpoint = 100


def unused2():
    stepCount = 0
    stuckCount = 0
    stepMax = 180
    complete = 0
    while complete == 0:
        if FFX_Screen.BattleScreen():
            print("Starting battle")
            if selfDestruct == 0:
                selfDestruct = FFX_Battle.MiihenRoad(selfDestruct)
                if FFX_memory.menuOpen() and FFX_memory.userControl() == False:
                    FFX_memory.clickToControl() # After-battle screen is still open.
            else:
                FFX_Battle.MiihenRoad(selfDestruct)
                if FFX_memory.menuOpen() and FFX_memory.userControl() == False:
                    FFX_memory.clickToControl() # After-battle screen is still open.
            print("Battle complete")
        elif FFX_Screen.PixelTestTol(788,325,(255, 253, 99),15):
            complete = 1
        elif FFX_Screen.Minimap2():
            stepCount += 1
            print("Mi'ihen pathing: ", stepCount)
            if stepCount < 43:
                FFXC.set_value('AxisLy', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
            elif stepCount < 55:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            elif stepCount == 55:
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLx', 0)
            elif stepCount < 115:
                FFXC.set_value('AxisLy', 1)
                if stepCount % 4 < 2:
                    FFXC.set_value('AxisLx', 1)
                time.sleep(0.1)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            else:
                stuckCount += 1
                print("Limit reached.")
                if stuckCount > 20:
                    FFXC.set_value('AxisLy', -1)
                    time.sleep(1.5)
                    FFXC.set_value('AxisLx', 1)
                    time.sleep(1.5)
                    FFXC.set_value('AxisLx', 0)
                    FFXC.set_value('AxisLy', 0)
                    stuckCount = 0
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 1)
                    time.sleep(0.3)
                    FFXC.set_value('AxisLx', 0)
                    time.sleep(0.3)
                    FFXC.set_value('AxisLy', 0)
                stepCount -= 1
        elif FFX_Screen.Minimap1():
            stepCount += 1
            print("Mi'ihen pathing: ", stepCount)
            if stepCount < 120:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            elif selfDestruct == 0: #Make sure we learn Self Destruct
                print("Self Destruct not yet learned. Extra pathing until we get it.")
                stepCount -= 1
                FFXC.set_value('AxisLy', 1)
                time.sleep(0.5)
                FFXC.set_value('AxisLy', -1)
                time.sleep(0.5)
                FFXC.set_value('AxisLy', 0)
            elif stepCount < stepMax:
                FFXC.set_value('AxisLy', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
            elif stepCount >= stepMax:
                stepCount -= 1
                FFXC.set_value('AxisLy', 1)
                time.sleep(0.5)
                FFXC.set_value('AxisLy', 0)
    print("Highroad North End. Ready to meet Seymour.")
    
def wrapUp():
    print("Now ready to meet Seymour")
    FFXC.set_value('AxisLy', 1)
    #FFXC.set_value('AxisLx', 1)
    #time.sleep(2.5)
    #FFXC.set_value('AxisLx', 0)
    time.sleep(5)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLy', 1)
    FFX_Xbox.SkipDialog(4.5)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.SkipDialog(2.5)
    FFXC.set_value('AxisLy', -1)
    FFX_Xbox.SkipDialog(12)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.clickToMap1() #Seymour scene
    FFXC.set_value('AxisLy', 1)
    time.sleep(12)
    FFXC.set_value('AxisLy', 0)