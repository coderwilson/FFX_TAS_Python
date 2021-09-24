import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_memory
import FFX_menu

FFXC = FFX_Xbox.FFXC

def trials():
    FFX_memory.clickToControl3()
    print("Starting trials")
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.2)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.SkipDialog(2) #Touching the first glyph
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Xbox.SkipDialog(2) #Touching the wall
    
    print("To the glyph sphere tutorial")
    FFX_memory.clickToControl3()
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 1)
    FFX_Xbox.SkipDialog(5) #Learn about spheres
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.clickToControl3()
    
    print("Moving to the lower door")
    #From Tutorial spot to the next door
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.8)
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.5)
    
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        FFXC.set_value('AxisLy', 1)
        if pos[0] < -22:
            FFXC.set_value('AxisLx', -1)
        else:
            FFXC.set_value('AxisLx', 0)
        FFX_Xbox.menuB()
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.clickToControl3()
    
    print("Heading around to the other side.")
    camera = FFX_memory.getCamera()
    while camera[0] < 1:
        FFXC.set_value('AxisLy', 1)
        camera = FFX_memory.getCamera()
    
    pos = FFX_memory.getCoords()
    while pos[0] < 25:
        FFXC.set_value('AxisLy', -1)
        FFXC.set_value('AxisLx', 0)
        pos = FFX_memory.getCoords()
    while pos[1] > 25:
        FFXC.set_value('AxisLy', 0)
        FFXC.set_value('AxisLx', -1)
        pos = FFX_memory.getCoords()
    while pos[1] > -40:
        FFXC.set_value('AxisLy', 1)
        FFXC.set_value('AxisLx', 0)
        pos = FFX_memory.getCoords()
    while pos[0] > 2: #Around last corner
        FFXC.set_value('AxisLy', 0)
        FFXC.set_value('AxisLx', 1)
        pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        FFXC.set_value('AxisLx', 1)
        if pos[0] > -2:
            FFXC.set_value('AxisLy', 1)
        else:
            FFXC.set_value('AxisLy', -1)
        FFX_Xbox.menuB()
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_memory.clickToControl3()
    #Into the glyph room
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.5)
    
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        if pos[1] < 20:
            FFXC.set_value('AxisLy', 1)
            FFXC.set_value('AxisLx', 0)
        else:
            FFXC.set_value('AxisLy', 1)
            FFXC.set_value('AxisLx', -1)
            FFX_Xbox.menuB()
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl3()
    
    #To the pedestol
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        if pos[1] > -50:
            FFXC.set_value('AxisLy', -1)
            FFXC.set_value('AxisLx', 0)
        else:
            FFXC.set_value('AxisLx', -1)
            if pos[0] < -14:
                FFXC.set_value('AxisLy', -1)
            else:
                FFXC.set_value('AxisLy', 1)
            FFX_Xbox.menuB()
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_memory.clickToControl3()
    
    #Push the pedestol
    FFXC.set_value('AxisLy', 1)
    time.sleep(12)
    FFXC.set_value('AxisLy', 0)
    print("Confirm: trials complete")

def aeonAndSleep() :
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.6)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.2)
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        if pos[0] > 15:
            FFXC.set_value('AxisLx', 0)
        else:
            FFXC.set_value('AxisLx', 1)
        if pos[0] > 10:
            FFXC.set_value('AxisLy', -1)
        elif pos[0] < -1:
            FFXC.set_value('AxisLy', 1)
        else:
            FFXC.set_value('AxisLy', 0)
        pos = FFX_memory.getCoords()
        
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.2)
    
    FFX_memory.awaitControl()
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        FFXC.set_value('AxisLx', -1)
        if pos[0] > -5:
            FFXC.set_value('AxisLy', -1)
        elif pos[0] < -15:
            FFXC.set_value('AxisLy', 1)
        else:
            FFXC.set_value('AxisLy', 0)
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    #Name Valefor and then skip dialog for night phase
    FFX_Screen.awaitPixel(408,257, (244, 0, 37))
    FFX_Xbox.menuB()
    time.sleep(0.5)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    
    #Skip dialog for "Victory", then run to Yuna
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLx', -1)
    time.sleep(5)
    FFXC.set_value('AxisLx', 0)
    FFX_Screen.clickToPixel(673,494,(216, 216, 216)) #Skip more dialog
    time.sleep(0.5)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    
    #Time to sleep
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLx', 1)
    time.sleep(1.05)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', -1)
    print("Talk to Wakka")
    FFX_Xbox.SkipDialog(0.5) #Talk to Wakka
    FFXC.set_value('AxisLy', 0)
    print("Pre-dream")
    FFX_Xbox.SkipDialog(4)
    
    FFX_memory.clickToControl() #Dreaming
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.2)
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        FFXC.set_value('AxisLy', 1)
        if pos[0] > 350:
            FFXC.set_value('AxisLx', -1)
        else:
            FFXC.set_value('AxisLx', 0)
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    
    print("Skipping what we can in the dream sequence. Jecht is mean!")
    FFX_memory.clickToControl()
    #End on the scene with Wakka and Lulu

def leaving() :
    FFX_memory.awaitControl()
    pos = FFX_memory.getCoords()
    while pos[0] > 5:
        FFXC.set_value('AxisLx', 1)
        FFXC.set_value('AxisLy', 0)
        pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        FFXC.set_value('AxisLy', 1)
        if pos[0] > 5:
            FFXC.set_value('AxisLx', 1)
        else:
            FFXC.set_value('AxisLx', 0)
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.2)
    FFX_memory.clickToControl()
    
    #Back in for Valefor overdrive
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.awaitControl()
    
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        FFXC.set_value('AxisLy', 1)
        if pos[1] < ((-1.94 * pos[0]) + 455.80):
            FFXC.set_value('AxisLx', -1)
        else:
            FFXC.set_value('AxisLx', 0)
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    #Should now be in the tent
    FFX_Screen.awaitPixel(342,183,(64, 193, 64))
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.6)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.4)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('BtnB', 1) # Talk to shop keeper
    time.sleep(0.1)
    FFXC.set_value('BtnB', 0)
    FFX_Screen.awaitPixel(704,466,(154, 154, 154))
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.1)
    FFX_Xbox.menuB() # Don't buy anything
    FFX_memory.clickToControl()
    
    #Exit the tent
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.awaitMap1()
    
    #Towards the dog tent
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(3.5)
    FFXC.set_value('AxisLy', 0)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    FFX_Screen.awaitPixel(202,150,(64, 193, 64))
    FFXC.set_value('AxisLx', 1)
    FFX_Xbox.SkipDialog(0.8)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.3)
    FFXC.set_value('AxisLy', 0)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    
    #Heading out of the village, finally!
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', -1)
    time.sleep(9)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    #Skip dialog for first tutorial
    FFX_memory.clickToControl2()
    FFXC.set_value('AxisLx', 1)
    time.sleep(4)
    FFXC.set_value('AxisLy', -1)
    time.sleep(8)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    #Magic tutorial
    FFX_Screen.clickToPixelTol(274,771,(137, 137, 137),5)
    time.sleep(0.3)
    FFX_Battle.thunder('none')
    FFX_memory.clickToControl()
    
    #Hilltop scene
    FFXC.set_value('AxisLx', 1)
    time.sleep(6)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.clickToControl()
    earlyTidusGrid = False
    if FFX_memory.getTidusSlvl() >= 3:
        FFX_menu.Liki()
        earlyTidusGrid = True
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.2)
    
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        FFXC.set_value('AxisLy', 1)
        FFXC.set_value('AxisLx', 0)
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.2)
    FFX_memory.awaitControl()
    
    #Kimahri fight
    FFXC.set_value('AxisLy', 1)
    time.sleep(4.5)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.skipScene()
    
    tidusTurn = 0
    while not FFX_memory.userControl():
        FFXC.set_value('AxisLx', 0)
        FFXC.set_value('AxisLy', 0)
        if FFX_Screen.BattleScreen():
            battleHP = FFX_memory.getBattleHP()
            print(FFX_memory.getEnemyCurrentHP())
            if battleHP[1] < 140:
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.SkipDialog(2) #Quick potion
            else:
                tidusTurn += 1
                #if tidusTurn == 5:
                #    FFX_Xbox.tidusOD()
                #else:
                #    FFX_Battle.attack('none')
                FFX_Battle.attack('none')
        else:
            FFX_Xbox.menuB()
    return earlyTidusGrid

def waterfalls() :
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.6)
    FFXC.set_value('AxisLy', 0)
    time.sleep(5.5)
    FFXC.set_value('AxisLx', 0)
    
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.7)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.25)
    FFXC.set_value('AxisLx', 0)
    time.sleep(4.5)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.SkipDialog(9)
    
    #Swap Tidus for Yuna
    FFX_Screen.clickToBattle()
    while FFX_memory.mainBattleMenu():
        FFX_Xbox.lBumper()
    FFX_Xbox.SkipDialog(1.5) #Swap Tidus out for Yuna
    FFX_Screen.clickToBattle()
    FFX_Battle.aeonSummon(0)
    FFX_Screen.clickToBattle()
    
    while not FFX_memory.menuOpen():
        if FFX_memory.battleScreen():
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
    
    pos = FFX_memory.getCoords()
    while FFX_memory.userControl():
        FFXC.set_value('AxisLy', 1)
        print("pos[1] vs Path formula: ", round(pos[1],2), " | ", round(((-0.25 * pos[0]) -35.14)),2)
        if pos[1] > ((-0.18 * pos[0]) -11.45):
            FFXC.set_value('AxisLx', 1)
        else:
            FFXC.set_value('AxisLx', 0)
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    FFX_Screen.clickToBattle()
    while not FFX_memory.userControl():
        if FFX_memory.battleScreen():
            FFX_Battle.escapeOne()
        elif FFX_Screen.BattleComplete():
            FFX_Xbox.menuB()
    
    stepCount = 0
    checkpoint = 0
    lastCP = 0
    while checkpoint != 1000:
        if lastCP != checkpoint:
            print("Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        if FFX_Screen.BattleScreen() :
            FFX_Battle.besaid()
        elif FFX_memory.userControl():
            pos = FFX_memory.getCoords()
            if checkpoint == 0:
                if pos[0] > -80:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[1] < ((-0.47 * pos[0]) -76.86):
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 10:
                if pos[0] > 90:
                    checkpoint = 15
                FFXC.set_value('AxisLx', 1)
                FFXC.set_value('AxisLy', 0)
            elif checkpoint == 15:
                if pos[0] > 240:
                    checkpoint = 20
                FFXC.set_value('AxisLx', 1)
                if pos[1] < ((-0.06 * pos[0]) -95.93): #Dialing in
                    FFXC.set_value('AxisLy', 1)
                else:
                    FFXC.set_value('AxisLy', 0)
            elif checkpoint == 20:
                if pos[1] > -23:
                    checkpoint = 30
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[1] < ((1.07 * pos[0]) -360): #Dialing in. neg 380 - 360
                        FFXC.set_value('AxisLy', 1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 30:
                if pos[0] < -1:
                    checkpoint = 40
                else:
                    FFXC.set_value('AxisLx', 1)
                    if pos[1] > ((2.62 * pos[0]) -988.80):
                        FFXC.set_value('AxisLy', -1)
                    else:
                        FFXC.set_value('AxisLy', 0)
            elif checkpoint == 40: #Start of last screen before the beach.
                if pos[1] < ((1.40 * pos[0]) + 53.00):
                    checkpoint = 50
                else:
                    FFXC.set_value('AxisLy', -1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 50:
                if pos[1] < ((-1.00 * pos[0]) -35.00):
                    checkpoint = 60
                else:
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', -1)
            elif checkpoint == 60:
                FFXC.set_value('AxisLy', -1)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.5)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.4)
                checkpoint = 70
            elif checkpoint == 70:
                if pos[0] > 50:
                    checkpoint = 80
                else:
                    FFXC.set_value('AxisLy', -1)
                    FFXC.set_value('AxisLx', 1)
            elif checkpoint == 80:
                if pos[1] < -300:
                    checkpoint = 1000
                    FFXC.set_value('AxisLx', 0)
                    FFXC.set_value('AxisLy', 0)
                    time.sleep(1)
                else:
                    FFXC.set_value('AxisLy', -1)
                    if pos[0] > 65:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            else:
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                time.sleep(0.5)