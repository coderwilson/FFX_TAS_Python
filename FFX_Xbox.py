import pyxinput
import time
FFXC = pyxinput.vController()

import FFX_memory
import FFX_Screen
import FFX_Battle
#FFXCread = pyxinput.rController(0)

def skipScene():
    print("Skip cutscene")
    FFXC.set_value('BtnStart', 1) #Generate button to skip
    time.sleep(0.1)
    FFXC.set_value('BtnStart', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnX', 1) #Perform the skip
    time.sleep(0.04)
    FFXC.set_value('BtnX', 0)

def skipSceneSpec():
    print("Skip cutscene and store an additional skip for a future scene")
    FFXC.set_value('BtnStart', 1) #Generate button to skip
    time.sleep(0.05)
    FFXC.set_value('BtnStart', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnX', 1) #Perform the skip
    time.sleep(0.04)
    FFXC.set_value('BtnX', 0)
    FFXC.set_value('BtnStart', 1) #Before despawn, regenerate the button for use in a future scene.
    time.sleep(0.05)
    FFXC.set_value('BtnStart', 0)
    
def skipStoredScene(skipTimer):
    print("Mashing skip button")
    currentTime = time.time()
    print("Current Time: ", currentTime)
    clickTimer = currentTime + skipTimer
    print("Click Until: ", clickTimer)
    while currentTime < clickTimer :
        
        FFXC.set_value('BtnX', 1) #Perform the skip
        time.sleep(0.04)
        FFXC.set_value('BtnX', 0)
        time.sleep(0.04)
        currentTime = time.time()
    print("Mashing skip button - Complete")

def Attack():
    print("Basic attack")
    FFXC.set_value('BtnB', 1)
    time.sleep(0.08)
    FFXC.set_value('BtnB', 0)
    time.sleep(0.08)
    FFXC.set_value('BtnB', 1)
    time.sleep(0.08)
    FFXC.set_value('BtnB', 0)
    time.sleep(0.5)
    
def touchSaveSphere():
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    print("Touching the save sphere")
    complete = False
    control = True
    while complete == False:
        if FFX_memory.userControl():
            if control == True:
                menuB()
                control = False
                time.sleep(0.1)
            else:
                complete = 1
        elif FFX_Screen.PixelTestTol(685,448,(164, 166, 164),5): #Tier 2 save sphere
            menuA()
            menuB()
        elif FFX_Screen.PixelTestTol(730,466,(154, 154, 154),5): #Tier 1 save sphere
            menuA()
            menuB()
        elif FFX_Screen.PixelTestTol(1564,25,(68, 74, 122),5): #Save menu has been opened.
            time.sleep(0.05)
            menuA()
            time.sleep(0.05)
            complete = 1
    FFX_memory.awaitControl()

def SkipDialog( Keystrokes ):
    Keystrokes
    print("Mashing B")
    currentTime = time.time()
    print("Current Time: ", currentTime)
    clickTimer = currentTime + Keystrokes
    print("Clicking for number of seconds: ", Keystrokes)
    while currentTime < clickTimer :
        FFXC.set_value('BtnB', 1)
        time.sleep(0.04)
        FFXC.set_value('BtnB', 0)
        time.sleep(0.04)
        currentTime = time.time()
    print("Mashing B - Complete")

def SkipDialogSpecial( Keystrokes ):
    Keystrokes
    print("Mashing B")
    currentTime = time.time()
    print("Current Time: ", currentTime)
    clickTimer = currentTime + Keystrokes
    print("Clicking for number of seconds: ", Keystrokes, " - Special skipping")
    while currentTime < clickTimer :
        FFXC.set_value('BtnB', 1)
        FFXC.set_value('BtnA', 1)
        time.sleep(0.035)
        FFXC.set_value('BtnB', 0)
        FFXC.set_value('BtnA', 0)
        time.sleep(0.035)
        currentTime = time.time()
    print("Mashing B - Complete")

def skipSave():
    print("Skipping save dialog popup")
    time.sleep(0.2)
    menuA()
    time.sleep(0.1)
    menuB()

def menuUp():
    FFXC.set_value('Dpad', 1)
    time.sleep(0.05)
    FFXC.set_value('Dpad', 0)
    time.sleep(0.06)
    
def menuDown():
    FFXC.set_value('Dpad', 2)
    time.sleep(0.05)
    FFXC.set_value('Dpad', 0)
    time.sleep(0.06)
    
def menuLeft():
    FFXC.set_value('Dpad', 4)
    time.sleep(0.05)
    FFXC.set_value('Dpad', 0)
    time.sleep(0.06)
    
def menuRight():
    FFXC.set_value('Dpad', 8)
    time.sleep(0.05)
    FFXC.set_value('Dpad', 0)
    time.sleep(0.06)
    
def shoulderLeft():
    FFXC.set_value('BtnShoulderL', 1)
    time.sleep(0.08)
    FFXC.set_value('BtnShoulderL', 0)
    time.sleep(0.08)
    
def shoulderRight():
    FFXC.set_value('BtnShoulderR', 1)
    time.sleep(0.08)
    FFXC.set_value('BtnShoulderR', 0)
    time.sleep(0.08)
    
def menuA():
    FFXC.set_value('BtnA', 1)
    time.sleep(0.08)
    FFXC.set_value('BtnA', 0)
    time.sleep(0.15)
    
def menuB():
    FFXC.set_value('BtnB', 1)
    time.sleep(0.06)
    FFXC.set_value('BtnB', 0)
    time.sleep(0.07)
    
def menuX():
    FFXC.set_value('BtnX', 1)
    time.sleep(0.08)
    FFXC.set_value('BtnX', 0)
    time.sleep(0.08)
    
def menuY():
    FFXC.set_value('BtnY', 1)
    time.sleep(0.08)
    FFXC.set_value('BtnY', 0)
    time.sleep(0.08)
    
def menuBack():
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.08)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.08)
    
def lBumper() :
    FFXC.set_value('BtnShoulderL', 1)
    time.sleep(0.08)
    FFXC.set_value('BtnShoulderL', 0)
    time.sleep(0.05)

def tidusOD():
    #This function has primarily moved to the FFX_Battle library. Leaving this version live in case
    #it continues to be used from other files outside of that library.
    print("Tidus overdrive activating")
    menuLeft()
    time.sleep(0.8)
    menuB()
    time.sleep(0.4)
    menuB()
    time.sleep(0.4)
    menuB() #Activate overdrive
    time.sleep(3)
    menuB()
    time.sleep(0.25)
    menuB()
    time.sleep(0.3)
    menuB()
    time.sleep(0.3)
    menuB()
    time.sleep(0.35)
    menuB()
    time.sleep(0.3)
    menuB()
    time.sleep(0.25)
    menuB()
    time.sleep(0.2)
    menuB()

def tidusFlee():
    #This function has primarily moved to the FFX_Battle library. Leaving this version live in case
    #it continues to be used from other files outside of that library.
    print("Character's first ability. This is modeled after Tidus using Flee prior to Gagazet.")
    menuDown()
    SkipDialog(2)

def tidusHaste(direction):
    direction = direction.lower()
    menuDown()
    menuDown()
    menuB()
    time.sleep(0.3)
    menuB()
    time.sleep(0.3)
    if direction == 'left':
        menuLeft()
    if direction == 'right':
        menuRight()
    if direction == 'up':
        menuUp()
    if direction == 'down':
        menuDown()
    menuB()
    menuB()
    menuB()
    time.sleep(0.8)

def tidusHasteLate(direction):
    direction = direction.lower()
    menuDown()
    menuDown()
    menuDown()
    menuB()
    time.sleep(0.3)
    menuB()
    time.sleep(0.3)
    if direction == 'left':
        menuLeft()
    if direction == 'right':
        menuRight()
    if direction == 'up':
        menuUp()
    if direction == 'down':
        menuDown()
    menuB()
    menuB()
    menuB()
    time.sleep(0.8)

def lateHaste(direction):
    direction = direction.lower()
    menuDown()
    menuDown()
    menuDown()
    menuB()
    time.sleep(0.3)
    menuB()
    time.sleep(0.3)
    if direction == 'left':
        menuLeft()
    if direction == 'right':
        menuRight()
    if direction == 'up':
        menuUp()
    if direction == 'down':
        menuDown()
    menuB()
    menuB()
    menuB()
    time.sleep(0.8)

def weapSwap(position):
    print("Weapon swap, weapon in position: ", position)
    while FFX_memory.mainBattleMenu():
        menuRight()
    if position == 0:
        SkipDialog(2)
    else:
        time.sleep(0.5)
        menuB()
        while FFX_memory.battleCursor2() != position :
            if FFX_memory.battleCursor2() < position:
                menuDown()
            elif FFX_memory.battleCursor2() > position:
                menuUp()
            weap += 1
        menuB()
        menuB()
        time.sleep(0.3)

def armorSwap(position):
    print("Armor swap, armor in position: ", position)
    menuRight()
    time.sleep(0.5)
    menuDown()
    time.sleep(0.5)
    menuB()
    time.sleep(0.7)
    armor = 0
    while armor < position :
        menuDown()
        armor += 1
    menuB()
    menuB()
    time.sleep(0.3)

def airShipPath(version):
    FFX_memory.clickToControl()
    
    checkpoint = 0
    lastCP = 0
    while checkpoint != 1000:
        if lastCP != checkpoint:
            print("Checkpoint: ", checkpoint)
            lastCP = checkpoint
        pos = FFX_memory.getCoords()
        if pos == [0.0,0.0]:
            if FFX_Screen.BattleScreen():
                FFX_Battle.fleeAll()
            else:
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                menuB()
                if checkpoint == 50:
                    FFX_memory.clickToControl()
        else:
            if checkpoint == 0: #First room
                if pos[1] > 130:
                    checkpoint = 10
                else:
                    time.sleep(0.05)
                    FFXC.set_value('AxisLx', 1)
                    FFXC.set_value('AxisLy', -1)
            elif checkpoint == 10: #Rin's room
                if pos[0] > 60:
                    checkpoint = 20
                else:
                    time.sleep(0.05)
                    FFXC.set_value('AxisLy', -1)
                    if pos[1] > 80:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 20: #Isaaru's room
                if pos[0] < 1:
                    checkpoint = 30
                else:
                    time.sleep(0.05)
                    FFXC.set_value('AxisLy', -1)
                    if pos[1] < 70:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 30:
                if pos[1] < -90:
                    checkpoint = 40
                else:
                    time.sleep(0.05)
                    FFXC.set_value('AxisLy', -1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 40:
                if pos[0] < -30:
                    checkpoint = 50
                else:
                    time.sleep(0.05)
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', -1)
            elif checkpoint == 50:
                if pos[1] > -15:
                    if version == 1:
                        print("Pre-Evrae pathing")
                        checkpoint = 60
                    elif version == 2:
                        print("Talking to Yuna/Kimahri in the gallery")
                        checkpoint = 120
                    elif version == 3:
                        print("Straight to the deck, three skips.")
                        checkpoint = 150
                    elif version == 4:
                        print("Straight to the deck, talking to Yuna.")
                        checkpoint = 180
                    elif version == 5:
                        print("Final pathing. Sin's face.")
                        checkpoint = 200
                    elif version == 6:
                        print("Final pathing. Sin's face.")
                        checkpoint = 70
                    else:
                        print("Something maybe went wrong?")
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', 0)
                else:
                    time.sleep(0.05)
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            
            elif checkpoint == 60: #Pre-Evrae with items
                if pos[1] < -10:
                    checkpoint = 65
                else:
                    time.sleep(0.05)
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < -5:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            
             #Pre-Evrae with items
            elif checkpoint == 65:
                FFX_memory.awaitControl()
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.15)
                FFXC.set_value('AxisLy', 0)
                time.sleep(0.5)
                FFXC.set_value('AxisLx', 0)
                FFX_Xbox.SkipDialog(2.5) #Talk to Rin
                FFX_Screen.awaitPixel(600,408,(151, 151, 151))
                FFX_Xbox.menuB()
                time.sleep(1)
                FFX_Xbox.menuRight()
                time.sleep(0.5)
                FFX_Xbox.menuB()
                time.sleep(0.2)
                FFX_Xbox.menuB()
                time.sleep(0.2)
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB() #Sell old Tidus armor
                FFX_Xbox.menuA()
                time.sleep(0.1)
                FFX_Xbox.menuLeft()
                time.sleep(0.5)
                FFX_Xbox.menuB()
                time.sleep(0.2)
                FFX_Xbox.menuB()
                time.sleep(0.2)
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB() #Purchase Baroque sword
                time.sleep(0.1)
                FFX_Xbox.menuB() #Do not equip yet.
                FFX_Xbox.menuA()
                FFX_Xbox.menuA()
                
                FFX_memory.clickToControl()
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLx', 0)
                FFX_Xbox.SkipDialog(3)
                FFX_memory.awaitControl()
                FFX_Xbox.SkipDialog(5)
                FFXC.set_value('AxisLy', 0)
                checkpoint = 1000
                
            #Pre-Evrae, no items
            elif checkpoint == 70:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.5)
                FFXC.set_value('AxisLx', 0)
                SkipDialog(5)
                FFXC.set_value('AxisLy', 0)
                FFX_memory.awaitControl()
                
                FFXC.set_value('AxisLy', 1)
                time.sleep(2)
                FFXC.set_value('AxisLy', 0)
                
                checkpoint = 1000
            
            #Yuna/Kimahri in the gallery
            elif checkpoint == 120:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
                SkipDialog(2)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                if FFX_memory.userControl():
                    print("Something went wrong. Trying the other way.")
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', -1)
                    SkipDialog(4)
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', 0)
                else:
                    checkpoint = 1000
                    FFX_memory.clickToControl()
            
            #Sin's arms
            elif checkpoint == 150:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.5)
                FFXC.set_value('AxisLx', 0)
                SkipDialog(4)
                FFXC.set_value('AxisLy', 0)
                FFX_memory.awaitControl()
                
                FFXC.set_value('AxisLy', 1)
                time.sleep(2)
                FFXC.set_value('AxisLy', 0)
                
                SkipDialog(64)
                skipScene()
                SkipDialog(6)
                skipScene()
                SkipDialog(26)
                skipScene()
                checkpoint = 1000
                
            #Yuna reflecting
            elif checkpoint == 180:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.5)
                FFXC.set_value('AxisLx', 0)
                SkipDialog(4)
                FFXC.set_value('AxisLy', 0)
                FFX_memory.awaitControl()
                
                FFXC.set_value('AxisLy', 1)
                time.sleep(2)
                FFXC.set_value('AxisLy', 0)
                
                FFX_memory.awaitControl()
                FFXC.set_value('AxisLx', -1)
                time.sleep(2.4)
                FFXC.set_value('AxisLy', 1)
                SkipDialog(0.5) #Hi Yuna. Let's have a quick chat.
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                SkipDialog(126)
                skipScene()
                checkpoint = 1000
                
            #Sin's face
            elif checkpoint == 200:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.5)
                FFXC.set_value('AxisLx', 0)
                SkipDialog(4)
                FFXC.set_value('AxisLy', 0)
                FFX_memory.awaitControl()
                
                FFXC.set_value('AxisLy', 1)
                time.sleep(2)
                FFXC.set_value('AxisLy', 0)
                time.sleep(6.5)
                skipScene()
                checkpoint = 1000

def airShipReturn():
    print("Conversation with Yuna/Kimahri.")
    FFX_memory.clickToControl()
    
    pos = FFX_memory.getCoords()
    print("Ready to run back to the cockpit.")
    while pos[1] > -90: #Leaving Yuna/Kimahri, heading back down.
        FFXC.set_value('AxisLy', -1)
        FFXC.set_value('AxisLx', 0)
        pos = FFX_memory.getCoords()
    print("Turn East")
    while pos[0] < -1:
        FFXC.set_value('AxisLx', 1)
        FFXC.set_value('AxisLy', 0)
        pos = FFX_memory.getCoords()
    print("Turn North")
    while FFX_memory.userControl():
        FFXC.set_value('AxisLx', 0)
        FFXC.set_value('AxisLy', 1)
        pos = FFX_memory.getCoords()
        
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.awaitControl()
    
    while FFX_memory.userControl():
        FFXC.set_value('AxisLx', 0)
        FFXC.set_value('AxisLy', 1)
        
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.awaitControl()
    
    while FFX_memory.userControl():
        pos = FFX_memory.getCoords()
        time.sleep(0.05)
        FFXC.set_value('AxisLy', 1)
        if pos[0] < -1:
            FFXC.set_value('AxisLx', 1)
        else:
            FFXC.set_value('AxisLx', 0)
            
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.2)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.5)
    
    while FFX_memory.userControl():
        FFXC.set_value('AxisLy', 1)
        FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)

def remove():
    print("Controller may freeze the program here. If so, please restart your PC.")
    time.sleep(2)
    FFXC.UnPlug(FFXC)