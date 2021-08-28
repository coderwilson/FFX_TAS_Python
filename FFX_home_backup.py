import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu

FFXC = FFX_Xbox.FFXC
 
def desert1():
    print("Starting Bikanel Island section")
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    time.sleep(4)
    FFXC.set_value('AxisLy', 0)
    
    while FFX_Screen.partySize() < 3:
        if FFX_Screen.BattleScreen():
            FFX_Battle.defend() #Skip turns until Lulu gets here
        else: FFX_Xbox.menuB() #Skip Dialog
    
    FFX_Screen.clickToBattle()
    FFX_Battle.fleeAll() #Get out of battle.
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLy', 1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.4)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.menuB()
    time.sleep(2)
    FFX_Xbox.menuB()
    time.sleep(1)
    FFX_Xbox.menuB()
    
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.awaitMap1()
    
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    complete = 0
    stepCount = 0
    stepMax = 550
    chargeState = [False,False,False] #Rikku and Kimahri charge status
    rikkuFound = False
    
    while complete == 0:
        mapOpen = FFX_Screen.Minimap1()
        if FFX_Screen.BattleScreen():
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
            if rikkuFound == False:
                FFX_Screen.awaitTurn()
                FFX_Battle.fleeAll()
            elif chargeState == [True,True,True]:
                FFX_Screen.awaitTurn()
                FFX_Battle.fleeAll()
            else:
                chargeState = FFX_Battle.bikanelCharge(chargeState[2])
                print("Current state of charging Rikku/Kimahri: ", chargeState)
        elif FFX_Screen.BattleComplete():
            FFXC.set_value('BtnB', 1)
            time.sleep(0.3)
            FFXC.set_value('BtnB', 0)
        elif FFX_Screen.PixelTestTol(23, 19, (90, 88, 127),5): #If the save game menu is open, we don't want to save.
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            FFX_Xbox.menuA()
        elif stepCount > 140 and not mapOpen and FFX_Screen.PixelTestTol(1108,823,(187, 187, 187),5):
            print("We may have hit the Al Bhed map. in the central area. Recovering.")
            time.sleep(0.1)
            FFX_Xbox.menuB()
            time.sleep(1)
            FFX_Xbox.menuB()
            time.sleep(1)
            FFXC.set_value('AxisLx', -1)
            time.sleep(1)
        elif FFX_Screen.PixelTest(1583,19,(60, 66, 115)): #Somehow the menu got opened, or save dialog.
            FFX_Xbox.menuA()
            FFX_Xbox.menuA()
            FFX_Xbox.menuA()
            FFX_Xbox.menuA()
        elif not mapOpen:
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
            FFX_Xbox.menuB() #Skipping dialog through various parts.
        elif FFX_Screen.PixelTest(284,153,(193, 193, 193)) and stepCount < 180:
            print("We've reached Rikku.")
            FFXC.set_value('AxisLy', 1)
            time.sleep(2)
            FFXC.set_value('AxisLy', 0)
            FFX_Xbox.touchSaveSphere()
            FFXC.set_value('AxisLy', -1)
            FFXC.set_value('AxisLx', -1)
            time.sleep(0.5)
            FFX_Xbox.SkipDialog(1)
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
            FFX_Xbox.SkipDialog(1)
            FFXC.set_value('AxisLx', -1)
            FFX_Xbox.SkipDialog(0.8)
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 1)
            time.sleep(1)
            FFXC.set_value('AxisLx', 1)
            time.sleep(7)
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            FFX_Screen.clickToBattle()
            FFX_Battle.buddySwap(2)
            FFX_Battle.Steal()
            rikkuFound = True
            
            #Formation change
            stepCount = 130
        else:
            stepCount += 1
            print(stepCount)
            if stepCount < 12:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.2)
            elif stepCount < 38:
                FFXC.set_value('AxisLy', -1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.2)
            elif stepCount < 48:
                FFXC.set_value('AxisLy', -1)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
            elif stepCount < 65:
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
            elif stepCount < 90:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.2)
            elif stepCount < 110:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.2)
            elif stepCount < 130: #Up to Rikku
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.4)
            elif stepCount < 150:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.2)
            elif stepCount < 160:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.2)
            elif stepCount < 175:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.2)
            elif stepCount < 205:
                FFXC.set_value('AxisLy', 1)
                if stepCount % 4 != 0:
                    FFXC.set_value('AxisLx', -1)
                else:
                    FFXC.set_value('AxisLx', 0)
                time.sleep(0.2)
            elif stepCount < 208:
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.2) #Into the next zone (Disney is that you?)
            elif stepCount < 210:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.2)
            elif stepCount < 215:
                FFXC.set_value('AxisLy', 1)
                if stepCount % 2 == 0:
                    FFXC.set_value('AxisLx', -1)
                else:
                    FFXC.set_value('AxisLx', 0)
                time.sleep(0.2)
            elif stepCount < 218:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.2)
            elif stepCount < 220:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
            elif stepCount < 268:
                FFXC.set_value('AxisLy', 1)
                if stepCount % 9 < 5:
                    FFXC.set_value('AxisLx', 0)
                else:
                    FFXC.set_value('AxisLx', -1)
                time.sleep(0.2) #Diagonal through the open desert
            elif stepCount < 281:
                FFXC.set_value('AxisLy', 1)
                if stepCount % 9 < 1:
                    FFXC.set_value('AxisLx', 0)
                else:
                    FFXC.set_value('AxisLx', -1)
                time.sleep(0.2) #Diagonal through the open desert
            elif stepCount < 294: #In the more dangerous area
                FFXC.set_value('AxisLy', 1)
                if stepCount % 8 == 0:
                    FFXC.set_value('AxisLx', -1)
                else:
                    FFXC.set_value('AxisLx', 0)
                time.sleep(0.2)
            elif stepCount < 320: #In the more dangerous area
                FFXC.set_value('AxisLx', 1)
                if stepCount % 8 < 7:
                    FFXC.set_value('AxisLy', 1)
                else:
                    FFXC.set_value('AxisLy', 0)
                time.sleep(0.2)
            elif stepCount < 321:
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
            elif stepCount < 375:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0) #To final desert zone, and straight into wall.
                time.sleep(0.2)
            elif stepCount < 407:
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 1) #To the right wall near Sandy #1
                time.sleep(0.2)
            elif stepCount < 410:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
            elif stepCount < 421:
                print("Diagonal: ", stepCount)
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.2)
            #elif stepCount < 480:
            #    print("line up: ", stepCount)
            #    FFXC.set_value('AxisLy', 0)
            #    FFXC.set_value('AxisLx', 1)
            #    time.sleep(0.2)
            elif stepCount < 424:
                print("line up: ", stepCount)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.3)
            else: complete = 1
    print("Lined up for the chest")
    complete = 0
    stepCount = 0
    stepMax = 100
    battleId = 1
    chestPattern = 0
    retries = 0
    counter = 0
    while complete == 0:
        if FFX_Screen.BattleScreen():
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            FFX_Xbox.menuUp()
            FFX_Xbox.menuUp()
            FFX_Xbox.menuUp()
            FFX_Xbox.menuUp()
            FFX_Xbox.menuUp()
            FFX_Xbox.menuUp()
            FFX_Xbox.menuUp()
            battleId = FFX_Battle.desertFights(battleId)
        #elif battleId == 3:
        #elif FFX_Screen.Minimap1() and not FFX_Screen.PixelTest(284,153,(193, 193, 193)):
        elif battleId == 2 and chestPattern == 0: #Pathing to get the chest
            retries = 0
            FFX_Screen.awaitMap1()
            FFXC.set_value('AxisLx', 1)
            time.sleep(3)
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', -1)
            time.sleep(1.1)
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', -1)
            time.sleep(1.62)
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 1)
            FFX_Xbox.SkipDialog(2)
            FFXC.set_value('AxisLy', 0)
            chestWait = 0
            while not FFX_Screen.PixelTestTol(991,442,(217, 217, 217),5):
                if chestWait % 100 == 0:
                    print("Waiting for chest to open.")
                chestWait += 1
            time.sleep(0.2)
            FFX_Xbox.menuB()
            time.sleep(0.4)
            chestPattern = 1
            stepCount = 30
        #    else:
        #        stepCount += 1
        elif FFX_Screen.Minimap1():
            stepCount += 1
            if retries > 2:
                stepCount = 22
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
            elif stepCount < 30 and battleId == 2:
                stepCount = 30
            elif battleId == 3:
                FFXC.set_value('AxisLy', 1)
                time.sleep(3)
                FFXC.set_value('AxisLy', 0)
                complete = 1
            elif stepCount < 10:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.3)
            elif stepCount < 11:
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
            elif stepCount < 20:
                FFXC.set_value('AxisLy', -1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.3)
            elif stepCount < 21:
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
            elif stepCount == 21:
                stepCount = 0
                retries += 1
            elif stepCount < 29:
                FFXC.set_value('AxisLy', -1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.2)
            elif stepCount == 29:
                stepCount = 0
                retries = 0
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
            elif stepCount < 45:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            elif stepCount < 90:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            elif battleId == 3:
                FFXC.set_value('AxisLy', 1)
                time.sleep(0.5)
                FFXC.set_value('AxisLy', 0)
def findSummoners():
    FFX_Screen.clickToMap1()
    FFX_menu.homeGrid()
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.7)
    FFXC.set_value('AxisLx', 1)
    time.sleep(2.9)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.touchSaveSphere()
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(3) #Enter Home
    FFXC.set_value('AxisLx', 0)
    time.sleep(6)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Battle.home1() #First battle
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.7)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3.5)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.clickToBattle()
    FFX_Battle.home2() #Second battle
    FFX_menu.homeHeal() #Healing up
    FFXC.set_value('AxisLy', -1)
    time.sleep(2.5)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.3)
    FFXC.set_value('AxisLy', -1)
    time.sleep(3)
    FFXC.set_value('AxisLx', -1)
    time.sleep(2.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Battle.home3() #Third battle (the spare room)
    time.sleep(0.5)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.3)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.7)
    FFX_Xbox.menuB()
    FFXC.set_value('AxisLy', 0)
    time.sleep(1)
    FFX_Xbox.menuB()
    time.sleep(1)
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuB()
    time.sleep(1)
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuB()
    time.sleep(1)
    FFX_Xbox.menuRight()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    time.sleep(3)
    FFX_Xbox.menuB()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLy', 1)
    time.sleep(5)
    FFXC.set_value('AxisLy', 0)
    while not FFX_Screen.BattleScreen():
        if FFX_Screen.Minimap1():
            FFXC.set_value('AxisLy', -1)
            time.sleep(1)
            FFXC.set_value('AxisLy', 1)
            time.sleep(1)
            FFXC.set_value('AxisLy', 0)
            
    FFX_Battle.fleeAll()
    
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', -1)
    time.sleep(5) #Just to make sure we're in the cutscene.
    FFXC.set_value('AxisLy', 1)
    time.sleep(5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.2)
    FFX_Battle.home4()
    
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.SkipDialog(2)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    FFX_Xbox.SkipDialog(3)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(8)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.clickToPixel(351,225,(64,193,64)) #40C140
    #FFX_Screen.awaitPixel(351,225,(64,193,64)) #40C140
    FFXC.set_value('AxisLy', -1)
    time.sleep(2.6)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', -1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Xbox.SkipDialog(92)
    FFX_Xbox.skipScene()
    FFX_Xbox.SkipDialog(9)
    FFX_Xbox.skipScene()
    FFX_Xbox.SkipDialog(53)
    FFX_Xbox.skipScene()