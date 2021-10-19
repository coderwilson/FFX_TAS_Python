import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_memory
import FFX_targetPathing

FFXC = FFX_Xbox.FFXC

def Beach():
    print("Starting Besaid section. Beach")
    FFXC.set_value('AxisLy', -1)
    FFX_memory.awaitControl()
    time.sleep(4.5)
    FFXC.set_value('AxisLy', 0)
    
    #Pathing, lots of pathing.
    checkpoint = 0
    while FFX_memory.getMap() != 122:
        if FFX_memory.userControl():
            #print("Checkpoint (testing): ", checkpoint)
            #Events
            if checkpoint == 33: #Into the temple for the first time
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 42: #Wakka tent
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 43: #Talk to Wakka
                while FFX_memory.userControl():
                    FFX_targetPathing.setMovement([15,16])
                    FFX_Xbox.tapB()
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                FFX_memory.clickToControl()
                checkpoint += 1
            elif checkpoint == 44: #Exiting tent
                print("Exiting tent")
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.besaid1(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
            if FFX_Screen.BattleScreen():
                FFX_Battle.pirhanas()
            elif FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            
            #map changes
            elif checkpoint < 2 and FFX_memory.getMap() == 20:
                checkpoint = 2
            elif checkpoint < 6 and FFX_memory.getMap() == 41:
                checkpoint = 6
            elif checkpoint < 22 and FFX_memory.getMap() == 69:
                checkpoint = 22
            elif checkpoint < 29 and FFX_memory.getMap() == 133:
                FFX_Screen.awaitPixel(973,506,(187, 187, 187)) #You do remember the prayer?
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                checkpoint = 29
            elif checkpoint == 36 and FFX_memory.getMap() == 17:
                checkpoint = 37

def Beach_old():
    print("Starting Besaid section. Beach")
    FFXC.set_value('AxisLy', -1)
    FFX_memory.awaitControl()
    time.sleep(4.5)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.SkipDialog(20)
    FFX_memory.clickToControl()
    print("Run to Wakka")
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    #Time to head to the village (via Pirahnas, it's fine)
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.2)
    #FFXC.set_value('AxisLy', 0)
    #FFXC.set_value('AxisLx', 1)
    #time.sleep(0.8)
    #FFXC.set_value('AxisLx', 0)
    #FFXC.set_value('AxisLy', -1)
    #time.sleep(0.5)
    #FFXC.set_value('AxisLy', 0)
    
    #FFX_Xbox.touchSaveSphere()
    
    FFXC.set_value('AxisLy', -1)
    FFX_memory.awaitEvent()
    time.sleep(0.1)
    FFX_memory.awaitControl()
    time.sleep(0.6)
    while FFX_memory.getCoords()[1] < -20:
        FFXC.set_value('AxisLx', 1)
        FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.SkipDialog(12)
    FFXC.set_value('AxisLx', 0)
    
    #Now in the water
    FFX_memory.clickToControl() #Wakka pushing Tidus into the water.
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)

def swimming1():
    print("Function no longer used")

def swimming1_old():
    print("Start of swimming section in Besaid.")
    checkpoint = 0
    lastCP = 0
    while checkpoint < 100:
        if lastCP != checkpoint:
            print("Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        if FFX_memory.userControl():
            pos = FFX_memory.getCoords()
            if checkpoint == 0:
                if pos[0] > 250:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((-0.63 * pos[0]) -572):
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 10:
                if pos[0] > 435:
                    checkpoint = 20
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((0.29 * pos[0]) -780.57):
                        FFXC.set_value('AxisLx', 1)
                    elif pos[1] < ((0.29 * pos[0]) -790.57):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 20:
                if pos[1] > -420:
                    checkpoint = 30
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > ((2.65 * pos[0]) -1826.94):
                        FFXC.set_value('AxisLx', 1)
                    elif pos[1] < ((2.65 * pos[0]) -1856.94):
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 30:
                if FFX_memory.getMap() != 41:
                    checkpoint = 100
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < 535:
                        FFXC.set_value('AxisLx', 1)
                    elif pos[0] > 545:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
        elif FFX_Screen.BattleScreen():
            battleNum = FFX_memory.getBattleNum()
            #11 = two pirhanas
            #12 = three pirhanas with one being a triple formation (takes two hits)
            #13 = four pirhanas
            if battleNum == 11:
                FFX_Battle.attack('none')
            else:
                FFX_Battle.escapeAll()
        elif FFX_Screen.BattleComplete():
            FFXC.set_value('BtnB', 1)
            time.sleep(0.035)
            FFXC.set_value('BtnB', 0)
            time.sleep(0.035)
        elif not FFX_memory.userControl():
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if checkpoint > 20:
                FFX_Xbox.menuB()

def enteringVillage():
    print("Function no longer used")

def enteringVillage_old():
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(5)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.SkipDialog(10)
    FFXC.set_value('AxisLy', 0)
    
    #Conversation with Luzzu and Gatta
    #FFX_Xbox.SkipDialog(18)
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(5)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    #Learning about the prayer
    FFX_Screen.awaitPixel(973,506,(187, 187, 187))
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    
    #Wait for Tidus to gain control
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.9)
    FFXC.set_value('AxisLx', 0)
    time.sleep(13)
    FFXC.set_value('AxisLy', 0)
    
    #Next, run towards the Braska statue
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLx', -1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.awaitControl() #Finally receive our statue.
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.4)
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        FFXC.set_value('AxisLx', 1)
        if pos[0] > 8:
            FFXC.set_value('AxisLy', -1)
        elif pos[0] < -5:
            FFXC.set_value('AxisLy', 1)
        else:
            FFXC.set_value('AxisLy', 0)
        pos = FFX_memory.getCoords()
        
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.2)
    
    #Temple to Wakka's tent
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', -1)
    time.sleep(7)
    FFXC.set_value('AxisLx', 1)
    time.sleep(4)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    #Approach Wakka
    FFX_Screen.awaitPixel(198,160, (64, 193, 64))
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    FFX_Xbox.SkipDialog(2.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.SkipDialog(3)
    
    #Sleeping
    FFX_memory.clickToControl()
    
    #Awake
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.3)
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        FFXC.set_value('AxisLy', 1)
        if pos[0] > 18:
            FFXC.set_value('AxisLx', 1)
        elif pos[0] < -18:
            FFXC.set_value('AxisLx', -1)
        else:
            FFXC.set_value('AxisLx', 0)
        pos = FFX_memory.getCoords()
    
    
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.2)
    FFX_memory.awaitControl()
    
    #Start of conversation with Wakka and the priest.
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        FFXC.set_value('AxisLx', -1)
        if pos[0] > 10:
            FFXC.set_value('AxisLy', -1)
        else:
            FFXC.set_value('AxisLy', 0)
        pos = FFX_memory.getCoords()
        
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.2)
    print("Pathing is complete. Ready for trials")



def trials():
    checkpoint = 0
    
    while FFX_memory.getMap() != 69:
        if FFX_memory.userControl():
            #Spheres, glyphs, and pedestols
            if checkpoint == 1: #First glyph
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 3: #Second glyph
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 7: #First Besaid sphere
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 12: #Insert Besaid sphere
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 20: #Touch the hidden door glyph
                FFX_memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 23: #Second Besaid sphere
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 26: #Insert Besaid sphere, and push to completion
                FFX_memory.clickToEventTemple(6)
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(10)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                checkpoint += 1
            elif checkpoint == 34: #Night, talk to Yuna and Wakka
                FFXC.set_value('AxisLy', -1)
                FFXC.set_value('AxisLx', -1)
                FFX_memory.awaitEvent()
                
                FFX_Screen.clickToPixel(673,494,(216, 216, 216)) #Wakka, "She's cute, ya?"
                time.sleep(0.5)
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                checkpoint += 1
            elif checkpoint == 36: #Sleep tight
                FFX_memory.clickToEventTemple(3)
                checkpoint += 1
            elif checkpoint == 39: #Dream about girls
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1

            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.besaidTrials(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            
            elif checkpoint == 32 and FFX_memory.menuOpen():
                time.sleep(0.2)
                FFX_Xbox.menuB()
                time.sleep(0.2)
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
                checkpoint += 1 #To the night scene
                
            
            #map changes
            elif checkpoint < 29 and FFX_memory.getMap() == 83:
                checkpoint = 29

def aeonAndSleep():
    print("Function no longer used.")

def waterfalls():
    print("Function no longer used.")

def leaving():
    FFX_memory.clickToControl()
    checkpoint = 0
    
    while FFX_memory.getMap() != 301:
        if FFX_memory.userControl():
            #Events
            if checkpoint == 0: #Back into the village
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 3: #Tent 1
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 5: #Shopkeeper
                FFXC.set_value('AxisLy', -1)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.5)
                FFX_Xbox.tapB()
                time.sleep(0.5)
                FFX_Xbox.menuDown()
                FFX_Xbox.tapB()
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 7: #Exit tent
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 9: #Tent 2
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 11: #Good doggo
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 13: #Exit tent
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 16: #Exit the front gates
                FFX_memory.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 18: #First tutorial
                print("Tuturial - Tidus and Wakka")
                FFX_memory.clickToEventTemple(3)
                checkpoint += 1
            elif checkpoint == 23: #Second tutorial
                print("Tutorial - Lulu magic")
                while FFX_memory.userControl():
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', 1)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                FFX_Screen.clickToBattle()
                FFX_Battle.attack('none')
                FFX_Screen.clickToBattle()
                FFX_Battle.thunder('none')
                FFX_memory.clickToControl()
                checkpoint += 1
            elif checkpoint == 24: #Hilltop
                FFX_memory.clickToEventTemple(2)
                earlyTidusGrid = False
                if FFX_memory.getTidusSlvl() >= 3:
                    FFX_menu.Liki()
                    earlyTidusGrid = True
                checkpoint += 1
            elif checkpoint == 60: #Beach, save sphere
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                time.sleep(0.2)
                FFX_Xbox.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 70:
                checkpoint -= 2
            
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.besaid2(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            elif FFX_memory.cutsceneSkipPossible():
                FFX_Xbox.skipScene()
            elif checkpoint < 20 and FFX_Screen.BattleScreen(): #Attacking tutorial
                while not FFX_memory.userControl():
                    FFX_Xbox.tapB()
            elif checkpoint > 25 and checkpoint < 30 and FFX_Screen.BattleScreen(): #Kimahri
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                while not FFX_memory.menuOpen():
                    if FFX_Screen.BattleScreen():
                        battleHP = FFX_memory.getBattleHP()
                        enemyHP = FFX_memory.getEnemyCurrentHP()
                        if battleHP[1] < 140 and enemyHP[0] > 110:
                            FFX_Xbox.menuDown()
                            FFX_Xbox.menuDown()
                            FFX_Xbox.SkipDialog(2) #Quick potion
                        else:
                            FFX_Battle.attack('none')
                    elif FFX_memory.diagSkipPossible():
                        FFX_Xbox.tapB()
                FFX_memory.clickToControl()
            elif checkpoint in [33, 34, 35] and FFX_Screen.BattleScreen(): #Valefor summon tutorial
                while not FFX_Screen.PixelTestTol(324, 92, (223, 223, 223), 5):
                    FFX_Xbox.lBumper()
                FFX_Xbox.SkipDialog(2) #Yuna to the party
                FFX_Screen.clickToBattle()
                FFX_Battle.aeonSummon(0)
                while not FFX_memory.menuOpen():
                    if FFX_Screen.BattleScreen():
                        FFX_Battle.aeonSpell(0)
                        time.sleep(0.4)
                print("Now to open the menu")
                FFX_memory.clickToControl()
                FFX_memory.openMenu() #Quick party reformat
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB() #Tidus for Wakka
                FFX_memory.closeMenu()
                checkpoint += 1
            elif checkpoint == 39 and FFX_Screen.BattleScreen(): #Dark Attack tutorial
                FFX_Battle.escapeAll()
                FFX_memory.clickToControl()
                checkpoint += 1
            elif checkpoint > 39 and FFX_Screen.BattleScreen(): #One forced battle on the way out of Besaid
                FFX_Battle.besaid()
            
            #Map changes
            elif checkpoint > 10 and checkpoint < 24 and FFX_memory.getMap() == 67: #Hilltop
                checkpoint = 24
            elif checkpoint < 27 and FFX_memory.getMap() == 21: #Kimahri map
                checkpoint = 27
            elif checkpoint < 32 and FFX_memory.getMap() == 22:
                checkpoint = 32
            elif checkpoint < 51 and FFX_memory.getMap() == 20:
                checkpoint = 51
            elif checkpoint < 59 and FFX_memory.getMap() == 19:
                checkpoint = 59
    
    return earlyTidusGrid