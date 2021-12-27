#import pyxinput
import vgamepad as vg
import time
import FFX_memory
import FFX_Screen
import pyautogui

#import FFX_memory
#import FFX_Battle
#import FFX_Screen

#FFXC = pyxinput.vController()
#FFXC = pyxinput.rController(0)
#FFXCread = pyxinput.rController(0)

class vgTranslator:
    def __init__(self):
        self.gamepad = vg.VX360Gamepad()
        
    def set_value(self, xKey, value):
        #Buttons, pressing
        if xKey == "BtnBack" and value == 1:
            self.gamepad.press_button(button=0x0020)
        elif xKey == "BtnStart" and value == 1:
            self.gamepad.press_button(button=0x0010)
        elif xKey == "BtnA" and value == 1:
            self.gamepad.press_button(button=0x1000)
        elif xKey == "BtnB" and value == 1:
            self.gamepad.press_button(button=0x2000)
        elif xKey == "BtnX" and value == 1:
            self.gamepad.press_button(button=0x4000)
        elif xKey == "BtnY" and value == 1:
            self.gamepad.press_button(button=0x8000)
        elif xKey == "BtnShoulderL" and value == 1:
            self.gamepad.press_button(button=0x0100)
        elif xKey == "BtnShoulderR" and value == 1:
            self.gamepad.press_button(button=0x0200)
        elif xKey == "Dpad" and value == 1: #Dpad up
            self.gamepad.press_button(button=0x0001)
        elif xKey == "Dpad" and value == 2: #Dpad down
            self.gamepad.press_button(button=0x0002)
        elif xKey == "Dpad" and value == 4: #Dpad left
            self.gamepad.press_button(button=0x0004)
        elif xKey == "Dpad" and value == 8: #Dpad right
            self.gamepad.press_button(button=0x0008)
        
        #Buttons, releasing
        elif xKey == "BtnBack" and value == 0:
            self.gamepad.release_button(button=0x0020)
        elif xKey == "BtnStart" and value == 0:
            self.gamepad.release_button(button=0x0010)
        elif xKey == "BtnA" and value == 0:
            self.gamepad.release_button(button=0x1000)
        elif xKey == "BtnB" and value == 0:
            self.gamepad.release_button(button=0x2000)
        elif xKey == "BtnX" and value == 0:
            self.gamepad.release_button(button=0x4000)
        elif xKey == "BtnY" and value == 0:
            self.gamepad.release_button(button=0x8000)
        elif xKey == "BtnShoulderL" and value == 0:
            self.gamepad.release_button(button=0x0100)
        elif xKey == "BtnShoulderR" and value == 0:
            self.gamepad.release_button(button=0x0200)
        elif xKey == "Dpad" and value == 0:
            self.gamepad.release_button(button=0x0001)
            self.gamepad.release_button(button=0x0002)
            self.gamepad.release_button(button=0x0004)
            self.gamepad.release_button(button=0x0008)
        
        #Error states
        elif xKey == "AxisLx" or xKey == "AxisLy":
            print("ERROR - OLD MOVEMENT COMMAND FOUND")
            print("ERROR - OLD MOVEMENT COMMAND FOUND")
            print("ERROR - OLD MOVEMENT COMMAND FOUND")
            print("ERROR - OLD MOVEMENT COMMAND FOUND")
            print("ERROR - ", xKey)
            print("ERROR - OLD MOVEMENT COMMAND FOUND")
            print("ERROR - OLD MOVEMENT COMMAND FOUND")
            print("ERROR - OLD MOVEMENT COMMAND FOUND")
            print("ERROR - OLD MOVEMENT COMMAND FOUND")
            self.set_neutral()
        
        self.gamepad.update()
        #For additional details, review this website:
        #https://pypi.org/project/vgamepad/
    
    def set_movement(self, x, y):
        if x > 1:
            x = 1
        if x < -1:
            x = -1
        if y > 1:
            y = 1
        if y < -1:
            y = -1
        
        self.gamepad.left_joystick_float(x_value_float = x, y_value_float = y)
        self.gamepad.update()
    
    def set_neutral(self):
        self.gamepad.reset()
        self.gamepad.update()

FFXC = vgTranslator()

def controllerHandle():
    return FFXC

def skipScene():
    print("Skip cutscene")
    FFXC.set_value('BtnStart', 1) #Generate button to skip
    time.sleep(0.035)
    FFXC.set_value('BtnStart', 0)
    time.sleep(0.035)
    FFXC.set_value('BtnX', 1) #Perform the skip
    time.sleep(0.035)
    FFXC.set_value('BtnX', 0)
    time.sleep(0.07)
    SkipDialog(2)

def skipSceneSpec():
    print("Skip cutscene and store an additional skip for a future scene")
    FFXC.set_value('BtnStart', 1) #Generate button to skip
    time.sleep(0.07)
    FFXC.set_value('BtnStart', 0)
    time.sleep(0.105)
    FFXC.set_value('BtnX', 1) #Perform the skip
    time.sleep(0.035)
    FFXC.set_value('BtnX', 0)
    FFXC.set_value('BtnStart', 1) #Before despawn, regenerate the button for use in a future scene.
    time.sleep(0.035)
    FFXC.set_value('BtnStart', 0)
    time.sleep(0.2)
    
def skipStoredScene(skipTimer):
    print("Mashing skip button")
    currentTime = time.time()
    print("Current Time: ", currentTime)
    clickTimer = currentTime + skipTimer
    print("Click Until: ", clickTimer)
    while currentTime < clickTimer :
        
        FFXC.set_value('BtnX', 1) #Perform the skip
        time.sleep(0.035)
        FFXC.set_value('BtnX', 0)
        time.sleep(0.035)
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
    FFXC.set_neutral()
    print("Touching the save sphere")
    while FFX_memory.userControl():
        tapB()
        time.sleep(0.2)
    time.sleep(0.5)
    tapA()
    time.sleep(0.07)
    tapB()
    #while not FFX_memory.touchingSaveSphere():
    #    if FFX_memory.userControl():
    #        menuB()
    #    elif FFX_memory.diagSkipPossible() and not FFX_memory.touchingSaveSphere():
    #        menuB()
    #print("Save Mark 1")
    
    #while not FFX_memory.saveMenuCursor() >= 1:
    #    menuDown()
    #print("Save Mark 2")
    #while not FFX_memory.userControl():
    #    tapB()
    #    time.sleep(0.7)
    #FFX_memory.awaitControl()
    FFXC.set_neutral()
    time.sleep(0.035)

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
    time.sleep(0.4)
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

def tapA():
    FFXC.set_value('BtnA', 1)
    time.sleep(0.035)
    FFXC.set_value('BtnA', 0)
    time.sleep(0.035)

def tapB():
    FFXC.set_value('BtnB', 1)
    time.sleep(0.035)
    FFXC.set_value('BtnB', 0)
    time.sleep(0.035)

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

def weapSwap(position):
    print("Weapon swap, weapon in position: ", position)
    while FFX_memory.mainBattleMenu():
        menuRight()
    if position == 0:
        SkipDialog(2)
    else:
        time.sleep(0.5)
        menuB()
        time.sleep(0.07)
        while position > 0:
            menuDown()
            position -= 1
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

def awaitSave() :
    #FFX_Logs.writeLog("Awaiting save dialog to pop up")
    counter = 0
    complete = 0
    while complete == 0:
        counter += 1;
        if counter % 100 == 0:
            print("Waiting for Save dialog: ", counter / 100)
        savePopup = FFX_Screen.PixelTest(630,422,(70,53,124))
        saveScreen = FFX_Screen.PixelTest(1,1,(87, 85, 122))
        if FFX_Screen.PixelTestTol(591,769,(221, 221, 221),5): #Skips specific dialog, SS Winno
            menuB()
        elif FFX_Screen.PixelTestTol(580,768,(222, 222, 222),5): #Skips specific dialog, SS Winno
            menuB()
        elif FFX_Screen.PixelTestTol(493,735,(220, 220, 220),5): #Skips specific dialog, SS Winno
            menuB()
        elif FFX_Screen.PixelTestTol(482,738,(215, 215, 215),5): #Skips specific dialog, SS Winno
            menuB()
        elif savePopup == True:
            time.sleep(0.8)
            menuA()
            complete = 1
        elif saveScreen == True:
            tapA()
            tapA()
            tapA()
            time.sleep(0.07)
            #tapB()
            complete = 1
        else:
            if not FFX_Screen.PixelTestTol(1,1,(0,0,0),5):
                menuB()
    print("Save dialog achieved")
    #FFX_Logs.writeLog("Save dialog on screen.")
    complete = 0
    while complete == 0:
        savePopup = FFX_Screen.PixelTestTol(630,422,(0,0,0),5)
        #if savePopup == True:
        #    complete = 1
        if FFX_Screen.PixelTestTol(752,484,(149, 149, 149),5):
            time.sleep(0.6)
            tapA()
            time.sleep(0.07)
        elif FFX_Screen.PixelTestTol(752,518,(149, 149, 149),5):
            menuB()
            complete = 1
    print("Save dialog cleared. Moving on.")
    #FFX_Logs.writeLog("Save dialog cleared. Moving on.")

def remove():
    print("Controller may freeze the program here. If so, please restart your PC.")
    #time.sleep(2)
    #FFXC.UnPlug(FFXC)

def gridUp():
    FFXC.set_value('Dpad', 1)
    time.sleep(0.04)
    FFXC.set_value('Dpad', 0)
    time.sleep(0.12)

def gridDown():
    FFXC.set_value('Dpad', 2)
    time.sleep(0.04)
    FFXC.set_value('Dpad', 0)
    time.sleep(0.12)

def gridLeft():
    FFXC.set_value('Dpad', 4)
    time.sleep(0.04)
    FFXC.set_value('Dpad', 0)
    time.sleep(0.12)

def gridRight():
    FFXC.set_value('Dpad', 8)
    time.sleep(0.04)
    FFXC.set_value('Dpad', 0)
    time.sleep(0.12)

def clickToPixel(x,y,rgb):
    counter = 0
    print("Clicking to pixel: (", x, ", ", y, ") color: ", rgb)
    while not FFX_Screen.PixelTestTol(x,y,rgb,5):
        counter += 1;
        if counter % 100 == 0:
            print("awaiting pixel (clicking): ", counter)
            print("Pixel being tested: (",x,",",y,")")
            print("Test state: ",rgb)
            try:
                print("Current State: ", pyautogui.pixel(x, y))
            except:
                print("Cannot get current state.")
        menuB()
    print("Trigger pixel achieved. Waiting is complete.")
    
def clickToPixelTol(x,y,rgb,tol):
    counter = 0
    print("Clicking to pixel: (", x, ", ", y, ") color: ", rgb)
    while not FFX_Screen.PixelTestTol(x,y,rgb, tol):
        counter += 1;
        if counter % 100 == 0:
            print("awaiting pixel (clicking): ", counter)
            print("Pixel being tested: (",x,",",y,")")
            print("Test state: ",rgb)
            try:
                print("Current State: ", pyautogui.pixel(x, y))
            except:
                print("Cannot get current state.")
        menuB()
    print("Trigger pixel achieved. Waiting is complete.")
    
def clickToBattle():
    #FFX_Logs.writeLog("Clicking until it's someone's turn in battle")
    print("Clicking until it's someone's turn in battle")
    FFXC.set_neutral()
    complete = 0
    while not FFX_memory.turnReady():
        if FFX_memory.userControl():
            break
        elif not FFX_memory.battleActive():
            menuB()
        elif FFX_memory.diagSkipPossible():
            menuB()

def clearSavePopup(clickToDiagNum):
    FFXC = controllerHandle()
    FFXC.set_neutral()
    FFX_memory.clickToDiagProgress(clickToDiagNum)
    FFX_memory.waitFrames(100)
    while FFX_memory.savePopupCursor() != 1:
        menuDown()
    menuB()
    FFX_memory.waitFrames(5)

def nameAeon():
    print("Waiting for aeon naming screen to come up")
    
    while not FFX_memory.nameAeonReady():
        if FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
            tapB()
    
    print("Naming screen is up.")
    time.sleep(0.3)
    tapB()
    time.sleep(0.035)
    FFXC.set_value('Dpad', 1)
    time.sleep(0.035)
    FFXC.set_neutral()
    time.sleep(0.035)
    tapB()
    time.sleep(0.3)
    
    print("Now clearing the value so we're ready for the next aeon later.")
    FFX_memory.clearNameAeonReady()