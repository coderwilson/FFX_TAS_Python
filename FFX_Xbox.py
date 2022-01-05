#import pyxinput
import vgamepad as vg
import time
import FFX_memory
import FFX_Screen
import pyautogui
import math

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
    FFX_memory.waitFrames(2)
    FFXC.set_value('BtnStart', 1) #Generate button to skip
    FFX_memory.waitFrames(1)
    FFXC.set_value('BtnStart', 0)

    FFX_memory.waitFrames(2)
    tapX()
    #FFX_memory.waitFrames(2)
    SkipDialog(2)

def skipSceneSpec():
    print("Skip cutscene and store an additional skip for a future scene")
    FFXC.set_value('BtnStart', 1) #Generate button to skip
    FFX_memory.waitFrames(30 * 0.07)
    FFXC.set_value('BtnStart', 0)
    FFX_memory.waitFrames(30 * 0.105)
    FFXC.set_value('BtnX', 1) #Perform the skip
    FFX_memory.waitFrames(30 * 0.035)
    FFXC.set_value('BtnX', 0)
    FFXC.set_value('BtnStart', 1) #Before despawn, regenerate the button for use in a future scene.
    FFX_memory.waitFrames(30 * 0.035)
    FFXC.set_value('BtnStart', 0)
    FFX_memory.waitFrames(30 * 0.2)
    
def skipStoredScene(skipTimer):
    print("Mashing skip button")
    currentTime = time.time()
    print("Current Time: ", currentTime)
    clickTimer = currentTime + skipTimer
    print("Click Until: ", clickTimer)
    while currentTime < clickTimer :
        
        FFXC.set_value('BtnX', 1) #Perform the skip
        FFX_memory.waitFrames(30 * 0.035)
        FFXC.set_value('BtnX', 0)
        FFX_memory.waitFrames(30 * 0.035)
        currentTime = time.time()
    print("Mashing skip button - Complete")

def Attack():
    print("Basic attack")
    FFXC.set_value('BtnB', 1)
    FFX_memory.waitFrames(30 * 0.08)
    FFXC.set_value('BtnB', 0)
    FFX_memory.waitFrames(30 * 0.08)
    FFXC.set_value('BtnB', 1)
    FFX_memory.waitFrames(30 * 0.08)
    FFXC.set_value('BtnB', 0)
    FFX_memory.waitFrames(30 * 0.5)
    
def touchSaveSphere():
    FFXC.set_neutral()
    print("Touching the save sphere")
    while FFX_memory.userControl():
        tapB()
        FFX_memory.waitFrames(3)
    FFX_memory.waitFrames(15)
    while not FFX_memory.userControl():
        if FFX_memory.menuControl():
            if not FFX_memory.saveMenuCursor():
                menuA()
                FFX_memory.waitFrames(1)
            else:
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
    #    FFX_memory.waitFrames(30 * 0.7)
    #FFX_memory.awaitControl()
    FFXC.set_neutral()
    FFX_memory.waitFrames(30 * 0.035)

def SkipDialog( Keystrokes ):
    # 2 frames per button mash
    num_repetitions = math.ceil(round(Keystrokes * 30) / 2)
    print(f"Mashing B {num_repetitions} number of times.")
    for _ in range(num_repetitions):
        tapB()
    print("Mashing B - Complete")
    
def MashNTimes( num_repetitions ):
    print(f"Mashing B {num_repetitions} number of times.")
    for _ in range(num_repetitions):
        tapB()
    print("Mashing B - Complete")

def SkipDialogSpecial( Keystrokes ):
    num_repetitions = math.ceil(round(Keystrokes * 30) / 2)
    print(f"Mashing A and B {num_repetitions} number of times.")
    for _ in range(num_repetitions) :
        FFXC.set_value('BtnB', 1)
        FFXC.set_value('BtnA', 1)
        FFX_memory.waitFrames(1)
        FFXC.set_value('BtnB', 0)
        FFXC.set_value('BtnA', 0)
        FFX_memory.waitFrames(1)
    print("Mashing A and B - Complete")
    
def menuUp():
    FFXC.set_value('Dpad', 1)
    FFX_memory.waitFrames(2)
    FFXC.set_value('Dpad', 0)
    FFX_memory.waitFrames(3)
    
def menuDown():
    FFXC.set_value('Dpad', 2)
    FFX_memory.waitFrames(2)
    FFXC.set_value('Dpad', 0)
    FFX_memory.waitFrames(3)
    
def menuLeft():
    FFXC.set_value('Dpad', 4)
    FFX_memory.waitFrames(2)
    FFXC.set_value('Dpad', 0)
    FFX_memory.waitFrames(3)
    
def menuRight():
    FFXC.set_value('Dpad', 8)
    FFX_memory.waitFrames(2)
    FFXC.set_value('Dpad', 0)
    FFX_memory.waitFrames(3)
    
def tapUp():
    FFXC.set_value('Dpad', 1)
    FFX_memory.waitFrames(1)
    FFXC.set_value('Dpad', 0)
    FFX_memory.waitFrames(1)
    
def tapDown():
    FFXC.set_value('Dpad', 2)
    FFX_memory.waitFrames(1)
    FFXC.set_value('Dpad', 0)
    FFX_memory.waitFrames(1)
    
def tapLeft():
    FFXC.set_value('Dpad', 4)
    FFX_memory.waitFrames(1)
    FFXC.set_value('Dpad', 0)
    FFX_memory.waitFrames(1)
    
def tapRight():
    FFXC.set_value('Dpad', 8)
    FFX_memory.waitFrames(1)
    FFXC.set_value('Dpad', 0)
    FFX_memory.waitFrames(1)
    
def shoulderLeft():
    FFXC.set_value('BtnShoulderL', 1)
    FFX_memory.waitFrames(2)
    FFXC.set_value('BtnShoulderL', 0)
    FFX_memory.waitFrames(2)
    
def shoulderRight():
    FFXC.set_value('BtnShoulderR', 1)
    FFX_memory.waitFrames(2)
    FFXC.set_value('BtnShoulderR', 0)
    FFX_memory.waitFrames(2)
    
def menuA():
    FFXC.set_value('BtnA', 1)
    FFX_memory.waitFrames(2)
    FFXC.set_value('BtnA', 0)
    FFX_memory.waitFrames(4)
    
def menuB():
    FFXC.set_value('BtnB', 1)
    FFX_memory.waitFrames(2)
    FFXC.set_value('BtnB', 0)
    FFX_memory.waitFrames(4)

def tapA():
    FFXC.set_value('BtnA', 1)
    FFX_memory.waitFrames(1)
    FFXC.set_value('BtnA', 0)
    FFX_memory.waitFrames(1)

def tapB():
    FFXC.set_value('BtnB', 1)
    FFX_memory.waitFrames(1)
    FFXC.set_value('BtnB', 0)
    FFX_memory.waitFrames(1)

def menuX():
    FFXC.set_value('BtnX', 1)
    FFX_memory.waitFrames(2)
    FFXC.set_value('BtnX', 0)
    FFX_memory.waitFrames(4)
    
def menuY():
    FFXC.set_value('BtnY', 1)
    FFX_memory.waitFrames(2)
    FFXC.set_value('BtnY', 0)
    FFX_memory.waitFrames(4)
    
def tapX():
    FFXC.set_value('BtnX', 1)
    FFX_memory.waitFrames(2)
    FFXC.set_value('BtnX', 0)
    FFX_memory.waitFrames(1)
    
def tapY():
    FFXC.set_value('BtnY', 1)
    FFX_memory.waitFrames(1)
    FFXC.set_value('BtnY', 0)
    FFX_memory.waitFrames(1)
    
def menuBack():
    FFXC.set_value('BtnBack', 1)
    FFX_memory.waitFrames(2)
    FFXC.set_value('BtnBack', 0)
    FFX_memory.waitFrames(2)
    
def lBumper() :
    FFXC.set_value('BtnShoulderL', 1)
    FFX_memory.waitFrames(2)
    FFXC.set_value('BtnShoulderL', 0)
    FFX_memory.waitFrames(2)

def tidusOD():
    #This function has primarily moved to the FFX_Battle library. Leaving this version live in case
    #it continues to be used from other files outside of that library.
    print("Tidus overdrive activating")
    menuLeft()
    FFX_memory.waitFrames(30 * 0.8)
    menuB()
    FFX_memory.waitFrames(30 * 0.4)
    menuB()
    FFX_memory.waitFrames(30 * 0.4)
    menuB() #Activate overdrive
    FFX_memory.waitFrames(30 * 3)
    menuB()
    FFX_memory.waitFrames(30 * 0.25)
    menuB()
    FFX_memory.waitFrames(30 * 0.3)
    menuB()
    FFX_memory.waitFrames(30 * 0.3)
    menuB()
    FFX_memory.waitFrames(30 * 0.35)
    menuB()
    FFX_memory.waitFrames(30 * 0.3)
    menuB()
    FFX_memory.waitFrames(30 * 0.25)
    menuB()
    FFX_memory.waitFrames(30 * 0.2)
    menuB()

def weapSwap(position):
    print("Weapon swap, weapon in position: ", position)
    while FFX_memory.mainBattleMenu():
        menuRight()
    if position == 0:
        SkipDialog(2)
    else:
        FFX_memory.waitFrames(30 * 0.5)
        menuB()
        FFX_memory.waitFrames(30 * 0.07)
        while position > 0:
            menuDown()
            position -= 1
        menuB()
        menuB()
        FFX_memory.waitFrames(30 * 0.3)

def armorSwap(position):
    print("Armor swap, armor in position: ", position)
    menuRight()
    FFX_memory.waitFrames(30 * 0.5)
    menuDown()
    FFX_memory.waitFrames(30 * 0.5)
    menuB()
    FFX_memory.waitFrames(30 * 0.7)
    armor = 0
    while armor < position :
        menuDown()
        armor += 1
    menuB()
    menuB()
    FFX_memory.waitFrames(30 * 0.3)

def clearSavePopup(clickToDiagNum=0):
    FFXC = controllerHandle()
    FFXC.set_neutral()
    FFX_memory.clickToDiagProgress(clickToDiagNum)
    complete = 0
    counter = 0
    while complete == 0:
        counter += 1;
        if counter % 100 == 0:
            print("Waiting for Save dialog: ", counter / 100)
        
        if FFX_memory.diagProgressFlag() != clickToDiagNum and FFX_memory.diagSkipPossible():
            tapB()
        
        elif FFX_memory.diagSkipPossible():
            if FFX_memory.savePopupCursor() == 0:
                menuUp()
            else:
                menuB()
                complete = 1
    FFX_memory.waitFrames(5)

def awaitSave(index=0):
    clearSavePopup(clickToDiagNum = index)

def awaitSave_old() :
    #FFX_Logs.writeLog("Awaiting save dialog to pop up")
    counter = 0
    complete = 0
    while complete == 0:
        counter += 1;
        if counter % 100 == 0:
            print("Waiting for Save dialog: ", counter / 100)
        
        if FFX_memory.diagProgressFlag() != 0 and FFX_memory.diagSkipPossible():
            tapB()
        
        elif diagSkipPossible():
            if FFX_memory.savePopupCursor() == 0:
                menuUp()
            else:
                menuB()
                complete = 1

def remove():
    print("Controller may freeze the program here. If so, please restart your PC.")
    #FFX_memory.waitFrames(30 * 2)
    #FFXC.UnPlug(FFXC)

def gridUp():
    FFXC.set_value('Dpad', 1)
    FFX_memory.waitFrames(30 * 0.04)
    FFXC.set_value('Dpad', 0)
    FFX_memory.waitFrames(30 * 0.12)

def gridDown():
    FFXC.set_value('Dpad', 2)
    FFX_memory.waitFrames(30 * 0.04)
    FFXC.set_value('Dpad', 0)
    FFX_memory.waitFrames(30 * 0.12)

def gridLeft():
    FFXC.set_value('Dpad', 4)
    FFX_memory.waitFrames(30 * 0.04)
    FFXC.set_value('Dpad', 0)
    FFX_memory.waitFrames(30 * 0.12)

def gridRight():
    FFXC.set_value('Dpad', 8)
    FFX_memory.waitFrames(30 * 0.04)
    FFXC.set_value('Dpad', 0)
    FFX_memory.waitFrames(30 * 0.12)

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
    while not FFX_memory.battleActive() and FFX_memory.turnReady():
        if FFX_memory.userControl():
            break
        elif not FFX_memory.battleActive():
            menuB()
        elif FFX_memory.diagSkipPossible():
            menuB()

def nameAeon():
    print("Waiting for aeon naming screen to come up")
    
    while not FFX_memory.nameAeonReady():
        if FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
            tapB()
    
    print("Naming screen is up.")
    FFX_memory.waitFrames(20)
    menuB()
    FFX_memory.waitFrames(4)
    FFXC.set_value('Dpad', 1)
    FFX_memory.waitFrames(2)
    FFXC.set_neutral()
    FFX_memory.waitFrames(2)
    tapB()
    FFX_memory.waitFrames(9)
    
    print("Now clearing the value so we're ready for the next aeon later.")
    FFX_memory.clearNameAeonReady()