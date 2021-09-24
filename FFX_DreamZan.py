import pyxinput
import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_memory

FFXC = FFX_Xbox.FFXC

def NamingTidus_slow():
    #Clear Tidus
    time.sleep(0.1)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB() # Delete all but T
    
    #Replace with TAS
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB() # A
    FFX_Xbox.menuDown()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB() # S
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() # Confirm
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() # Confirm again

def NamingTidus():
    FFX_Xbox.menuB() # Confirm
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() # Confirm again
    
def NewGame(gameLength):
    FFX_Screen.awaitPixel(1076,552,(157, 159, 157))
    print("Starting the game")
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.1)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('BtnB', 1)
    time.sleep(0.1)
    FFXC.set_value('BtnB', 0)
    
    #New game selected. Next, select options.
    time.sleep(3)
    print("Default Sphere Grid")
    FFX_Xbox.menuB()
    time.sleep(1)
    print("Confirm sphere grid")
    FFX_Xbox.menuB()
    time.sleep(1)
    print("Orchestrated soundtrack.")
    FFX_Xbox.menuB()
    time.sleep(1)
    print("Confirm Orchestrated soundtrack.")
    FFX_Xbox.menuB()
    print("This will be a ", gameLength, " run.")
    #Options selected (all standard for the remake)

def listenStory(gameLength):
    #Skip cutscene (multiple presses)
    time.sleep(9)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    
    #Talk to kids
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', -1)
    while FFX_memory.userControl():
        pos = FFX_memory.getCoords()
        if pos[0] > 45 and pos[1] > 2:
            FFXC.set_value('AxisLx', 1)
        else:
            FFXC.set_value('AxisLx', 0)
        if pos[0] < 35:
            FFX_Xbox.menuB()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    #Name Tidus (custom function in this library. Can be changed later.
    FFX_Screen.awaitPixel(316,374,(224, 182, 138))
    NamingTidus()
    
    #Now to talk to the ladies.
    #FFX_Screen.awaitPixel(1554,657,(255, 192, 210))
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.5)
    FFX_Xbox.SkipDialog( 2 )
    FFXC.set_value('AxisLx', 0)
    
    #Leave house area
    FFX_memory.awaitControl()
    #time.sleep(30)
    FFXC.set_value('AxisLy', -1)
    time.sleep(6)
    FFXC.set_value('AxisLy', 0)
    
    #Zanar talks to himself.
    FFX_memory.awaitControl()
    #time.sleep(74)
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.4)
    FFXC.set_value('AxisLx', 0)
    while FFX_memory.getMap() != 371:
        time.sleep(0.05)
    
    FFXC.set_value('AxisLy', 0)
    #Front of the Blitz dome
    FFX_memory.clickToControl()
    time.sleep(0.15)
    FFXC.set_value('AxisLy', 1)
    FFX_Xbox.SkipDialog(0.3)
    while FFX_memory.getStoryProgress() < 6:
        if FFX_memory.userControl():
            FFXC.set_value('AxisLy', 1)
            if FFX_memory.getCoords()[0] > 2:
                FFXC.set_value('AxisLx', 1)
            elif FFX_memory.getCoords()[0] < -10:
                FFXC.set_value('AxisLx', -1)
            else:
                FFXC.set_value('AxisLx', 0)
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            FFX_Xbox.menuB()
    
    #Skip blitball scene
    time.sleep(2.9)
    FFX_Xbox.skipScene()
    
    #Run to Auron
    FFX_memory.awaitControl()
    #FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.4)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.3)
    while FFX_memory.getStoryProgress() < 10:
        if FFX_memory.userControl():
            pos = FFX_memory.getCoords()
            if pos[1] < ((8.43 * pos[0]) + 805.14):
                FFXC.set_value('AxisLx', 1)
            elif pos[1] > ((8.43 * pos[0]) + 835):
                FFXC.set_value('AxisLx', -1)
            else:
                FFXC.set_value('AxisLx', 0)
        else:
            FFX_Xbox.menuB()
    
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    #Two possible cutscene skips, possible to save 8~10 seconds
    waitCounter = 0
    while FFX_memory.getMap() != 389:
        waitCounter += 1
        if waitCounter % 100000 == 0:
            print("Waiting for time to stop freezing. ", waitCounter / 100000)
    print("OK time has returned to normal. Now timing for skip.")
    
    time.sleep(16.4)
    FFX_Xbox.skipScene()
    time.sleep(23)
    FFXC.set_value('BtnStart', 1) #Generate button to skip a later scene ("This is your story")
    time.sleep(0.1)
    FFXC.set_value('BtnStart', 0)
    
    #Just to make sure...
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)

def ammesBattle():
    FFX_Screen.clickToBattle()
    FFX_Battle.defend()
    
    #Auron overdrive tutorial
    FFX_Screen.clickToPixel(724,314,(234, 196, 0))
    time.sleep(0.2)
    FFX_Screen.awaitPixel(1072,526,(234, 175, 0))
    time.sleep(0.2)
    FFXC.set_value('BtnB', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnB', 0)
    
    time.sleep(1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.2)
    FFX_Xbox.SkipDialog(3) #Initiate overdrive
    time.sleep(1) #Static delay, the same every time.
    
    #Doing the actual overdrive
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.04)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.04)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.04)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.04)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.04)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.04)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.04)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.04)
    FFXC.set_value('BtnShoulderL', 1)
    time.sleep(0.04)
    FFXC.set_value('BtnShoulderL', 0)
    time.sleep(0.04)
    FFXC.set_value('BtnShoulderR', 1)
    time.sleep(0.04)
    FFXC.set_value('BtnShoulderR', 0)
    time.sleep(0.04)
    FFXC.set_value('BtnA', 1)
    time.sleep(0.04)
    FFXC.set_value('BtnA', 0)
    time.sleep(0.04)
    FFXC.set_value('BtnB', 1)
    time.sleep(0.04)
    FFXC.set_value('BtnB', 0)
    time.sleep(2)
    
def ammesBattleShort():
    FFX_Screen.clickToBattle()
    FFX_memory.setEnemyCurrentHP(0, 20)
    FFX_memory.setEnemyCurrentHP(1, 0)
    FFX_memory.setEnemyCurrentHP(2, 0)
    
    FFX_Battle.attack('none')
    time.sleep(0.5)
    FFX_Screen.clickToBattle()
    FFX_memory.setEnemyCurrentHP(0, 0)
    FFX_memory.setEnemyCurrentHP(1, 0)
    FFX_memory.setEnemyCurrentHP(2, 0)
    
    #Now to wait for the Auron overdrive
    FFX_Screen.clickToPixel(724,314,(234, 196, 0))
    time.sleep(0.2)
    FFX_memory.setEnemyCurrentHP(0, 20)
    FFX_Screen.awaitPixel(1072,526,(234, 175, 0))
    time.sleep(0.2)
    FFXC.set_value('BtnB', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnB', 0)
    
    time.sleep(1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.2)
    FFX_Xbox.SkipDialog(3) #Initiate overdrive
    time.sleep(1) #Static delay, the same every time.
    
    #Doing the actual overdrive
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.04)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.04)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.04)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.04)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.04)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.04)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.04)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.04)
    FFXC.set_value('BtnShoulderL', 1)
    time.sleep(0.04)
    FFXC.set_value('BtnShoulderL', 0)
    time.sleep(0.04)
    FFXC.set_value('BtnShoulderR', 1)
    time.sleep(0.04)
    FFXC.set_value('BtnShoulderR', 0)
    time.sleep(0.04)
    FFXC.set_value('BtnA', 1)
    time.sleep(0.04)
    FFXC.set_value('BtnA', 0)
    time.sleep(0.04)
    FFXC.set_value('BtnB', 1)
    time.sleep(0.04)
    FFXC.set_value('BtnB', 0)
    time.sleep(2)

def AfterAmmes():
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.45)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.clickToEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    
    #Touch the save sphere
    time.sleep(0.4)
    FFX_Xbox.menuB()
    time.sleep(0.5)
    FFX_Xbox.menuA()
    FFX_Xbox.menuB()
    
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(2.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    time.sleep(3.5)
    
    #Finally, finish with the Tanker fight.
    
def SwimToJecht() :
    #FFX_memory.awaitControl()
    
    #time.sleep(1.5)
    print("Swimming to Jecht")
    
    FFXC.set_value('BtnA', 1)
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(8)
    while FFX_memory.userControl():
        FFXC.set_value('AxisLy', 1)
    
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('BtnA', 0)
    print("We've now reached Jecht.")
    FFX_Xbox.SkipDialog(5)
    
    #Next, swim to Baaj temple
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.6)
    FFXC.set_value('AxisLx', 0)
    time.sleep(5)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(14)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1.5) # Line up with stairs
    
    FFXC.set_value('AxisLx', 0)
    #time.sleep(600)
    time.sleep(3)
    
    while FFX_memory.getMap() == 48:
        pos = FFX_memory.getCoords()
        if pos[1] < 550:
            FFXC.set_value('AxisLy', 1)
            if pos[0] < -5:
                FFXC.set_value('AxisLx', 1)
            elif pos[0] > 5:
                FFXC.set_value('AxisLx', -1)
            else:
                FFXC.set_value('AxisLx', 0)
        else:
            #print("How is this position?")
            #FFXC.set_value('AxisLx', 0)
            #FFXC.set_value('AxisLy', 0)
            #time.sleep(10)
            FFXC.set_value('AxisLy', 1)
            if pos[1] > ((-1.00 * pos[0]) + 577.00):
                FFXC.set_value('AxisLx', -1)
            else:
                FFXC.set_value('AxisLx', 0)
    
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.3)

def SwimToJecht_shortGame():
    #FFX_memory.awaitControl()
    
    #time.sleep(1.5)
    print("Swimming to Jecht")
    
    FFXC.set_value('BtnA', 1)
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(8)
    while FFX_memory.userControl():
        FFXC.set_value('AxisLy', 1)
    
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('BtnA', 0)
    print("We've now reached Jecht.")
    FFX_Xbox.SkipDialog(5)
    
    #Next, swim to Baaj temple
    FFX_Screen.clickToMap1()
    FFX_memory.itemHack(1)
    FFX_memory.changeGold(9999999) #Obviously, we gotta be rich.
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.6)
    FFXC.set_value('AxisLx', 0)
    time.sleep(5)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(14)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1.5) # Line up with stairs
    FFX_memory.changeStory(3210) #Jump to game state, point of no return
    FFXC.set_value('AxisLx', 0)
    #time.sleep(600)
    time.sleep(3)
    
    while FFX_memory.getMap() == 48:
        pos = FFX_memory.getCoords()
        if pos[1] < 550:
            FFXC.set_value('AxisLy', 1)
            if pos[0] < -5:
                FFXC.set_value('AxisLx', 1)
            elif pos[0] > 5:
                FFXC.set_value('AxisLx', -1)
            else:
                FFXC.set_value('AxisLx', 0)
        else:
            #print("How is this position?")
            #FFXC.set_value('AxisLx', 0)
            #FFXC.set_value('AxisLy', 0)
            #time.sleep(10)
            FFXC.set_value('AxisLy', 1)
            if pos[1] > ((-1.00 * pos[0]) + 577.00):
                FFXC.set_value('AxisLx', -1)
            else:
                FFXC.set_value('AxisLx', 0)
    
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    time.sleep(0.3)
