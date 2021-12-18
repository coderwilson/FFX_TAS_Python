import pyxinput
import time
import FFX_Xbox
import FFX_Screen
import FFX_memory

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

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

def gridOpen():
    return FFX_memory.sGridActive()
    
def _gridChar(*, char_id: int) -> bool:
    return FFX_memory.sGridChar() == char_id
    
def gridTidus():
    return _gridChar(char_id=0)
    
def gridYuna():
    return _gridChar(char_id=1)
    
def gridAuron():
    return _gridChar(char_id=2)
    
def gridKimahri():
    return _gridChar(char_id=3)  
    
def gridWakka():
    return _gridChar(char_id=4)
    
def gridLulu():
    return _gridChar(char_id=5)

def gridRikku():
    return _gridChar(char_id=6)

def firstPosition():
    if FFX_Screen.PixelTestTol(619,765,(255, 255, 255),5) and not FFX_Screen.PixelTestTol(178,786,(159, 161, 159),5):
        return True
    else: return False

def moveUseMenu():
    return FFX_Screen.PixelTestTol(347,526,(255, 255, 255),5)

def moveReady():
    if moveUseMenu():
        if FFX_memory.getGridMoveUsePos() == 0:
            return True
        else:
            return False
    else: return False

def moveActive():
    if readyUseSphere():
        return False
    else:
        return FFX_Screen.PixelTestTol(178,786,(159, 161, 159),5)

def moveComplete():
    if FFX_Screen.PixelTestTol(252,584,(218, 218, 218),5):
        if FFX_Screen.PixelTestTol(182,546,(156, 158, 156),5):
            return True
        else: return False
    else: return False
    
def useReady():
    if moveUseMenu():
        if FFX_memory.getGridMoveUsePos() == 1:
            return True
        else:
            return False
    else: return False

def readySelectSphere():
    return FFX_Screen.PixelTestTol(636,438,(255, 255, 255),5)

def readyUseSphere():
    if FFX_Screen.PixelTestTol(619,765,(255, 255, 255),5):
        if FFX_Screen.PixelTestTol(176,786,(159, 161, 159),5):
            return True
        elif FFX_Screen.PixelTestTol(225,785,(232, 13, 13),5):
            return True
        else:
            return False
    elif FFX_Screen.PixelTestTol(225,785,(232, 13, 13),5):
        return True
    else: return False
    
def quitGridReady():
    if FFX_Screen.PixelTestTol(252,584,(218, 218, 218),5):
        if FFX_Screen.PixelTestTol(182,546,(156, 158, 156),5):
            return True
        else: return False
    else: return False
    
def mainMenu():
    return FFX_Screen.PixelTestTol(1575,20,(67, 70, 117),5)
    
def useFirst():
    print("use first")
    while not readySelectSphere():
        if firstPosition():
            FFX_Xbox.menuB()
        elif moveReady():
            FFX_Xbox.menuDown()
        elif useReady():
            FFX_Xbox.menuB()
    #time.sleep(0.4)
    return True

def moveFirst():
    print("move first")
    while not moveActive():
        if firstPosition():
            FFX_Xbox.menuB()
        elif moveReady():
            FFX_Xbox.menuB()
        elif useReady():
            FFX_Xbox.menuUp()
    #time.sleep(0.2)
    return True

def moveAndUse():
    print("move and use")
    time.sleep(0.035)
    FFX_Xbox.menuB()
    time.sleep(0.035)
    while not readySelectSphere():
        if moveComplete() or firstPosition():
            FFX_Xbox.menuB()
        elif moveReady():
            FFX_Xbox.menuDown()
        elif useReady():
            FFX_Xbox.menuB()
    #time.sleep(0.2)
    return True

def useAndMove():
    print("use and move")
    time.sleep(0.035)
    FFX_Xbox.menuB()
    time.sleep(0.035)
    while not moveActive():
        if readyUseSphere() or firstPosition():
            FFX_Xbox.menuB()
        elif moveReady():
            FFX_Xbox.menuB()
        elif useReady():
            FFX_Xbox.menuUp()
        else:
            FFX_Xbox.menuB()
    #time.sleep(0.2)
    return True

def useAndUseAgain():
    print("use and use again")
    time.sleep(0.035)
    FFX_Xbox.menuB()
    time.sleep(0.035)
    while not readySelectSphere():
        if readyUseSphere() or firstPosition():
            FFX_Xbox.menuB()
        elif moveReady():
            FFX_Xbox.menuDown()
        elif useReady():
            FFX_Xbox.menuB()
    #time.sleep(0.2)
    return True

def useShiftLeft(toon):
    print("use and shift")
    #time.sleep(0.1)
    FFX_Xbox.menuB()
    toon = toon.lower()
    if toon == 'yuna':
        while not gridYuna():
            if readyUseSphere():
                FFX_Xbox.menuB()
            elif moveUseMenu():
                FFX_Xbox.menuBack()
            elif firstPosition():
                FFX_Xbox.shoulderLeft()
    if toon == 'lulu':
        while not gridLulu():
            if readyUseSphere():
                FFX_Xbox.menuB()
            elif moveUseMenu():
                FFX_Xbox.menuBack()
            elif firstPosition():
                FFX_Xbox.shoulderLeft()
    if toon == 'auron':
        while not gridAuron():
            if readyUseSphere():
                FFX_Xbox.menuB()
            elif moveUseMenu():
                FFX_Xbox.menuBack()
            elif firstPosition():
                FFX_Xbox.shoulderLeft()
    if toon == 'wakka':
        while not gridWakka():
            if readyUseSphere():
                FFX_Xbox.menuB()
            elif moveUseMenu():
                FFX_Xbox.menuBack()
            elif firstPosition():
                FFX_Xbox.shoulderLeft()
    if toon == 'tidus':
        while not gridTidus():
            if readyUseSphere():
                FFX_Xbox.menuB()
            elif moveUseMenu():
                FFX_Xbox.menuBack()
            elif firstPosition():
                FFX_Xbox.shoulderLeft()
    if toon == 'kimahri':
        while not gridKimahri():
            if readyUseSphere():
                FFX_Xbox.menuB()
            elif moveUseMenu():
                FFX_Xbox.menuBack()
            elif firstPosition():
                FFX_Xbox.shoulderLeft()
    if toon == 'rikku':
        while not gridRikku():
            if readyUseSphere():
                FFX_Xbox.menuB()
            elif moveUseMenu():
                FFX_Xbox.menuBack()
            elif firstPosition():
                FFX_Xbox.shoulderLeft()
    print("Ready for grid: " + toon)

def useShiftRight(toon):
    print("use and shift")
    #time.sleep(0.1)
    FFX_Xbox.menuB()
    toon = toon.lower()
    if toon == 'yuna':
        while not gridYuna():
            if readyUseSphere():
                FFX_Xbox.menuB()
            elif moveUseMenu():
                FFX_Xbox.menuBack()
            elif firstPosition():
                FFX_Xbox.shoulderRight()
    if toon == 'lulu':
        while not gridLulu():
            if readyUseSphere():
                FFX_Xbox.menuB()
            elif moveUseMenu():
                FFX_Xbox.menuBack()
            elif firstPosition():
                FFX_Xbox.shoulderRight()
                time.sleep(0.3)
    if toon == 'auron':
        while not gridAuron():
            if readyUseSphere():
                FFX_Xbox.menuB()
            elif moveUseMenu():
                FFX_Xbox.menuBack()
            elif firstPosition():
                FFX_Xbox.shoulderRight()
    if toon == 'wakka':
        while not gridWakka():
            if readyUseSphere():
                FFX_Xbox.menuB()
            elif moveUseMenu():
                FFX_Xbox.menuBack()
            elif firstPosition():
                FFX_Xbox.shoulderRight()
    if toon == 'tidus':
        while not gridTidus():
            if readyUseSphere():
                FFX_Xbox.menuB()
            elif moveUseMenu():
                FFX_Xbox.menuBack()
            elif firstPosition():
                FFX_Xbox.shoulderRight()
    if toon == 'kimahri':
        while not gridKimahri():
            if readyUseSphere():
                FFX_Xbox.menuB()
            elif moveUseMenu():
                FFX_Xbox.menuBack()
            elif firstPosition():
                FFX_Xbox.shoulderRight()
    if toon == 'rikku':
        while not gridRikku():
            if readyUseSphere():
                FFX_Xbox.menuB()
            elif moveUseMenu():
                FFX_Xbox.menuBack()
            elif firstPosition():
                FFX_Xbox.shoulderRight()
    print("Ready for grid: " + toon)

def moveShiftLeft(toon):
    print("Move and shift, left")
    FFX_Xbox.menuB()
    toon = toon.lower()
    if toon == 'yuna':
        while not gridYuna():
            if moveReady() or moveActive() or moveComplete():
                FFX_Xbox.menuB()
            elif moveUseMenu():
                FFX_Xbox.menuBack()
            elif firstPosition():
                FFX_Xbox.shoulderLeft()
    if toon == 'lulu':
        while not gridLulu():
            if moveReady() or moveActive() or moveComplete():
                FFX_Xbox.menuB()
            elif moveUseMenu():
                FFX_Xbox.menuBack()
            elif firstPosition():
                FFX_Xbox.shoulderLeft()
    print("Ready for grid: " + toon)

def moveShiftRight(toon):
    print("Move and shift, right")
    FFX_Xbox.menuB()
    toon = toon.lower()
    if toon == 'yuna':
        while not gridYuna():
            if moveReady() or moveActive() or moveComplete():
                FFX_Xbox.menuB()
            elif moveUseMenu():
                FFX_Xbox.menuBack()
            elif firstPosition():
                FFX_Xbox.shoulderRight()
    if toon == 'lulu':
        while not gridLulu():
            if moveReady() or moveActive() or moveComplete():
                FFX_Xbox.menuB()
            elif moveUseMenu():
                FFX_Xbox.menuBack()
            elif firstPosition():
                FFX_Xbox.shoulderRight()
    print("Ready for grid: " + toon)

def useAndQuit():
    time.sleep(0.1)
    FFX_Xbox.menuB()
    while not mainMenu():
        if readyUseSphere():
            print("Using the current item.")
            FFX_Xbox.menuB()
        elif firstPosition():
            print("Opening the Quit menu")
            FFX_Xbox.menuA()
        elif quitGridReady():
            print("quitting sphere grid")
            FFX_Xbox.menuB()
    time.sleep(0.3)
    return True

def cursorPos():
    if FFX_Screen.PixelTestTol(180,459,(179, 181, 179),5):
        return 1
    elif FFX_Screen.PixelTestTol(176,504,(147, 148, 147),5):
        return 2
    elif FFX_Screen.PixelTestTol(176,547,(148, 150, 148),5):
        return 3
    elif FFX_Screen.PixelTestTol(176,591,(145, 145, 145),5):
        return 4
    else: return cursorPos()

def sphereColor(desired):
    print("Desired color: ", desired)
    position = cursorPos()
    print("Testing position: ", position)
    if position == 1:
        color = FFX_Screen.PixelValue(230,460)
        print("Position 1: ", color)
        if color == (220, 9, 9):
            print("Position 1, red sphere found.")
            if desired == 'red':
                print("Desired color found.")
                return 1
        if color == (68, 69, 69):
            print("Position 1, black sphere found.")
            if desired == 'black':
                print("Desired color found.")
                return 4
    if position == 2:
        color = FFX_Screen.PixelValue(230,505)
        print("Position 2: ", color)
        if color == (222, 1, 1):
            print("Position 2, red sphere found.")
            if desired == 'red':
                print("Desired color found.")
                return 2
        if color == (182, 143, 2):
            print("Position 2, yellow sphere found.")
            if desired == 'yellow':
                print("Desired color found.")
                return 2
    if position == 3:
        color = FFX_Screen.PixelValue(230,550)
        print("Position 3: ", color)
        if color == (147, 0, 0):
            print("Position 3, red sphere found.")
            if desired == 'red':
                print("Desired color found.")
                return 3
        if color == (141, 123, 0):
            print("Position 3, yellow sphere found.")
            if desired == 'yellow':
                print("Desired color found.")
                return 3
    if position == 4:
        color = FFX_Screen.PixelValue(230,590)
        print("Position 4: ", color)
        if color == (215, 7, 7):
            print("Position 4, red sphere found.")
            if desired == 'red':
                print("Desired color found.")
                return 4
        if color == (193, 223, 231):
            print("Position 4, white sphere found.")
            if desired == 'white':
                print("Desired color found.")
                return 4
        if color == (114, 18, 210):
            print("Position 4, purple sphere found.")
            if desired == 'purple':
                print("Desired color found.")
                return 4
        if color == (49, 50, 50):
            print("Position 4, black sphere found.")
            if desired == 'black':
                print("Desired color found.")
                return 4
        if color == (198, 167, 6):
            print("Position 4, yellow sphere found.")
            if desired == 'yellow':
                print("Desired color found.")
                return 4
    return 0

def sphereNum(sType) -> int:
    sType = sType.lower()
    if sType == 'power':
        return 70
    elif sType == 'mana':
        return 71
    elif sType == 'speed':
        return 72
    elif sType == 'ability':
        return 73
    elif sType == 'fortune':
        return 74
    elif sType == 'attribute':
        return 75
    elif sType == 'special':
        return 76
    elif sType == 'skill':
        return 77
    elif sType == 'wmag':
        return 78
    elif sType == 'bmag':
        return 79
    elif sType == 'master':
        return 80
    elif sType == 'lv1':
        return 81
    elif sType == 'lv2':
        return 82
    elif sType == 'lv3':
        return 83
    elif sType == 'lv4':
        return 84
    elif sType == 'hp':
        return 85
    elif sType == 'mp':
        return 86
    elif sType == 'strength':
        return 87
    elif sType == 'defense':
        return 88
    elif sType == 'magic':
        return 89
    elif sType == 'mdef':
        return 90
    elif sType == 'agility':
        return 91
    elif sType == 'evasion':
        return 92
    elif sType == 'accuracy':
        return 93
    elif sType == 'luck':
        return 94
    elif sType == 'clear':
        return 95
    elif sType == 'ret':
        return 96
    elif sType == 'friend':
        return 97
    elif sType == 'tele':
        return 98
    elif sType == 'warp':
        return 99
    return 255

def selSphere(sType, direction, shift):
    #The direction variable is no longer used.
    sNum = 255
    menuPos = 0
    print("-----------------------------------")
    print("-----------------------------------")
    print(sType)
    sNum = sphereNum(sType)
    print(sNum)
    menuPos = FFX_memory.getGridItemsSlot(sNum)
    print(menuPos)
    print("-----------------------------------")
    print("-----------------------------------")
    if menuPos == 255:
        print("Sphere ", sType, "is not in inventory.")
        return
    complete = False
    while complete == False:
        if menuPos > FFX_memory.getGridCursorPos():
            FFX_Xbox.menuDown()
        elif menuPos < FFX_memory.getGridCursorPos():
            FFX_Xbox.menuUp()
        
        if menuPos == FFX_memory.getGridCursorPos():
            time.sleep(0.1)
            if menuPos == FFX_memory.getGridCursorPos():
                FFX_Xbox.menuB()
                complete = True
    if shift == 'none':
        FFX_Xbox.SkipDialog(0.7)
    else:
        time.sleep(0.2)
        if shift == 'up':
            gridUp()
        if shift == 'left':
            gridLeft()
        if shift == 'l5':
            gridLeft()
            gridLeft()
            gridLeft()
            gridLeft()
            gridLeft()
        if shift == 'right':
            gridRight()
        if shift == 'r2':
            gridRight()
            gridRight()
        if shift == 'down':
            gridDown()
        if shift == 'd2':
            gridDown()
            gridDown()
        if shift == 'up2':
            gridUp()
            gridUp()
        if shift == 'd5':
            gridDown()
            gridDown()
            gridDown()
            gridDown()
            gridDown()
        if shift == 'aftersk':
            gridUp()
            gridRight()
            gridDown()
            #gridDown()
        if shift == 'aftersk2':
            gridRight()
            gridRight()
            time.sleep(0.1)
            gridLeft()
        if shift == 'torikku':
            time.sleep(0.2)
            gridDown()
            gridDown()
            gridLeft()
            gridLeft()
        if shift == 'yunaspec':
            #Yuna Special
            gridDown()
            gridRight()
            gridRight()
            gridDown()
            gridDown()
        FFX_Xbox.SkipDialog(0.7)

def selSphere_old(sType, direction, shift):
    sType = sType.lower()
    shift = shift.lower()
    found = 0
    limit = 0
    speed = 0.05
    position = 0
    color = 'none'
    print("Looking for sphere: '",sType,"'")
    if sType == 'power' or sType == 'speed' or sType == 'mana' or sType == 'ability' or sType == 'fortune':
        color = 'red'
    if sType == 'tele' or sType == 'ret' or sType == 'friend':
        color = 'white'
    if sType == 'magic' or sType == 'luck' or sType == 'strength' or sType == 'purpAny':
        color = 'purple'
    if sType == 'lv1' or sType == 'lv2' or sType == 'lv3' or sType == 'lv4':
        color = 'black'
    if sType == 'skill' or sType == 'att':
        color = 'yellow'
    
    
    while not readyUseSphere():
        print(color)
        position = sphereColor(color)
        if position != 0:
            if sType == 'power':
                if position == 1:
                    if FFX_Screen.PixelTestTol(370,473,(171, 171, 171),5):
                        FFX_Xbox.menuB() #Found a power sphere
                        time.sleep(0.1)
                        found = 1
                    else:
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                elif position == 2:
                    if FFX_Screen.PixelTestTol(389,495,(22, 22, 22),5):
                        FFX_Xbox.menuB() #Found a power sphere
                        time.sleep(0.1)
                        found = 1
                    else:
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                else:
                    if direction == 'd':
                        FFX_Xbox.menuDown()
                    if direction == 'u':
                        FFX_Xbox.menuUp()
            elif sType == 'mana':
                if position == 1:
                    if FFX_Screen.PixelTestTol(357,473,(171, 171, 171),5):
                        FFX_Xbox.menuB() #Found mana sphere
                        time.sleep(0.1)
                        found = 1
                if position == 2:
                    if FFX_Screen.PixelTestTol(356,516,(172, 172, 172),5):
                        FFX_Xbox.menuB() #Found mana sphere
                        time.sleep(0.1)
                        found = 1
                    else:
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                else:
                    if direction == 'd':
                        FFX_Xbox.menuDown()
                    if direction == 'u':
                        FFX_Xbox.menuUp()
            elif sType == 'speed':
                if position == 1:
                    if FFX_Screen.PixelTestTol(275,472,(174, 174, 174),5):
                        FFX_Xbox.menuB() #Found a speed sphere
                        time.sleep(0.1)
                        found = 1
                    else:
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                elif position == 2:
                    if FFX_Screen.PixelTestTol(275,516,(172, 172, 172),5):
                        FFX_Xbox.menuB() #Found a speed sphere
                        time.sleep(0.1)
                        found = 1
                    else:
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                elif position == 3:
                    print("Ping")
                    if FFX_Screen.PixelTestTol(275,560,(170, 170, 170),5):
                        print("Ping 2")
                        FFX_Xbox.menuB() #Found a speed sphere
                        time.sleep(0.1)
                        found = 1
                    else:
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                elif position == 4 and direction == 'd':
                    direction = 'u'
                else:
                    if direction == 'd':
                        FFX_Xbox.menuDown()
                    if direction == 'u':
                        FFX_Xbox.menuUp()
            elif sType == 'ability':
                if position == 1:
                    if FFX_Screen.PixelTestTol(300,452,(222, 222, 222),5):
                        FFX_Xbox.menuB() #Found ability sphere
                        time.sleep(0.1)
                        found = 1
                if position == 4:
                    if FFX_Screen.PixelTestTol(300,582,(222, 222, 222),5):
                        FFX_Xbox.menuB() #Found ability sphere
                        time.sleep(0.1)
                        found = 1
                    else:
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                else:
                    if direction == 'd':
                        FFX_Xbox.menuDown()
                    if direction == 'u':
                        FFX_Xbox.menuUp()
            elif sType == 'fortune':
                if position == 4:
                    if FFX_Screen.PixelTestTol(391,602,(172, 172, 172),5):
                        FFX_Xbox.menuB() #Found ability sphere
                        time.sleep(0.1)
                        found = 1
                    else:
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                else:
                    if direction == 'd':
                        FFX_Xbox.menuDown()
                    if direction == 'u':
                        FFX_Xbox.menuUp()
            elif sType == 'tele':
                if position == 4:
                    if FFX_Screen.PixelTestTol(316,603,(169, 169, 169),5):
                        FFX_Xbox.menuB() #Found a teleport sphere
                        time.sleep(0.1)
                        found = 1
                    else:
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                else:
                    if direction == 'd':
                        FFX_Xbox.menuDown()
                    if direction == 'u':
                        FFX_Xbox.menuUp()
            elif sType == 'friend':
                if position == 4:
                    if FFX_Screen.PixelTestTol(331,581,(223, 223, 223),5):
                        FFX_Xbox.menuB() #Found a friend sphere
                        time.sleep(0.1)
                        found = 1
                    else:
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                else:
                    if direction == 'd':
                        FFX_Xbox.menuDown()
                    if direction == 'u':
                        FFX_Xbox.menuUp()
            elif sType == 'ret':
                if position == 4:
                    if FFX_Screen.PixelTestTol(295,582,(222, 222, 222),5):
                        print("Found Return sphere")
                        FFX_Xbox.menuB() #Found a return sphere
                        time.sleep(0.1)
                        found = 1
                    else:
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                else:
                    if direction == 'd':
                        FFX_Xbox.menuDown()
                    if direction == 'u':
                        FFX_Xbox.menuUp()
            elif sType == 'lv1' or sType == 'lv2' or sType == 'lv3' or sType == 'lv4':
                pixel2 = FFX_Screen.PixelValue(307,598)
                print(pixel2)
                if position == 4 and FFX_Screen.PixelTestTol(258,583,(220, 220, 220),5):
                    #Should be more specific. Just getting tired of finding the right level.
                    FFX_Xbox.menuB() # Lv.1 sphere
                    time.sleep(0.1)
                    found = 1
                elif position == 1:
                    print("Found a key sphere in position 1")
                    FFX_Xbox.menuB() # Lv.1 sphere
                    time.sleep(0.1)
                    found = 1
                elif position == 3: #This is just a placeholder until we feel like coming back to improve this.
                    if (sType == 'lv3' or sType == 'lv4') and FFX_Screen.PixelTestTol(258,583,(220, 220, 220),5):
                        print("Found a Lv.3/4 sphere (these are never side by side)")
                        FFX_Xbox.menuB() # Lv.1 sphere
                        time.sleep(0.1)
                        found = 1
                    elif FFX_Screen.PixelTestTol(317,581,(137, 132, 160),5): # Top corner of the 1 in Lv.1
                        print("Found a Lv.1 unlock sphere.")
                        if sType == 'lv1':
                            FFX_Xbox.menuB() # Lv.1 sphere
                            time.sleep(0.1)
                            found = 1
                        else:
                            print("Wrong sphere.")
                            if direction == 'd':
                                FFX_Xbox.menuDown()
                            if direction == 'u':
                                FFX_Xbox.menuUp()
                    elif pixel2 == (184, 184, 184): #Bottom left of the 2 in Lv.2
                        print("Found a Lv.2 unlock sphere.")
                        if sType == 'lv2':
                            FFX_Xbox.menuB() # Lv.2 sphere
                            time.sleep(0.1)
                            found = 1
                        else:
                            print("Wrong sphere.")
                            if direction == 'd':
                                FFX_Xbox.menuDown()
                            if direction == 'u':
                                FFX_Xbox.menuUp()
                    else:
                        print("Could not identify sphere.")
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                else:
                    if direction == 'd':
                        FFX_Xbox.menuDown()
                    if direction == 'u':
                        FFX_Xbox.menuUp()
            elif sType == 'magic':
                if position == 4:
                    if FFX_Screen.PixelTestTol(301,602,(172, 172, 172),5):
                        FFX_Xbox.menuB() #Found a magic sphere
                        time.sleep(0.1)
                        found = 1
                    else:
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                else:
                    if direction == 'd':
                        FFX_Xbox.menuDown()
                    if direction == 'u':
                        FFX_Xbox.menuUp()
            elif sType == 'luck':
                if position == 4:
                    if FFX_Screen.PixelTestTol(303,580,(225, 225, 225),5):
                        FFX_Xbox.menuB() #Found a Luck sphere
                        time.sleep(0.1)
                        found = 1
                    else:
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                else:
                    if direction == 'd':
                        FFX_Xbox.menuDown()
                    if direction == 'u':
                        FFX_Xbox.menuUp()
            elif sType == 'strength':
                if position == 4:
                    if FFX_Screen.PixelTestTol(421,581,(223, 223, 223),5):
                        FFX_Xbox.menuB() #Found a Strength sphere
                        time.sleep(0.1)
                        found = 1
                    else:
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                else:
                    if direction == 'd':
                        FFX_Xbox.menuDown()
                    if direction == 'u':
                        FFX_Xbox.menuUp()
            elif sType == 'skill':
                if position == 2:
                    if FFX_Screen.PixelTestTol(306,494,(224, 224, 224),5) and FFX_Screen.PixelTestTol(343,516,(172, 172, 172),5):
                        FFX_Xbox.menuB() #Found a Skill sphere
                        time.sleep(0.1)
                        found = 1
                    else:
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                elif position == 3:
                    if FFX_Screen.PixelTestTol(306,538,(223, 223, 223),5) and FFX_Screen.PixelTestTol(343,560,(170, 170, 170),5):
                        FFX_Xbox.menuB() #Found a Skill sphere
                        time.sleep(0.1)
                        found = 1
                    else:
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                elif position == 4:
                    if FFX_Screen.PixelTestTol(306,585,(216, 216, 216),5) and FFX_Screen.PixelTestTol(343,601,(175, 175, 175),5):
                        FFX_Xbox.menuB() #Found a Skill sphere
                        time.sleep(0.1)
                        found = 1
                    else:
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                else:
                    if direction == 'd':
                        FFX_Xbox.menuDown()
                    if direction == 'u':
                        FFX_Xbox.menuUp()
            elif sType == 'att':
                if position == 2:
                    if FFX_Screen.PixelTestTol(412,516,(172, 172, 172),5):
                        FFX_Xbox.menuB() #Found an Attribute sphere
                        time.sleep(0.1)
                        found = 1
                    else:
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                elif position == 3:
                    if FFX_Screen.PixelTestTol(412,559,(173, 173, 173),5):
                        FFX_Xbox.menuB() #Found an Attribute sphere
                        time.sleep(0.1)
                        found = 1
                    else:
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                elif position == 4:
                    if FFX_Screen.PixelTestTol(412,603,(169, 169, 169),5):
                        FFX_Xbox.menuB() #Found an Attribute sphere
                        time.sleep(0.1)
                        found = 1
                    else:
                        if direction == 'd':
                            FFX_Xbox.menuDown()
                        if direction == 'u':
                            FFX_Xbox.menuUp()
                else:
                    if direction == 'd':
                        FFX_Xbox.menuDown()
                    if direction == 'u':
                        FFX_Xbox.menuUp()
        else:
            if direction == 'd':
                FFX_Xbox.menuDown()
            if direction == 'u':
                FFX_Xbox.menuUp()
        if found == 1:
            if shift == 'up':
                gridUp()
            if shift == 'left':
                gridLeft()
            if shift == 'l5':
                gridLeft()
                gridLeft()
                gridLeft()
                gridLeft()
                gridLeft()
            if shift == 'right':
                gridRight()
            if shift == 'r2':
                gridRight()
                gridRight()
            if shift == 'down':
                gridDown()
            if shift == 'd2':
                gridDown()
                gridDown()
            if shift == 'd5':
                gridDown()
                gridDown()
                gridDown()
                gridDown()
                gridDown()
            if shift == 'aftersk':
                gridUp()
                gridRight()
                gridDown()
                #gridDown()
            if shift == 'aftersk2':
                gridRight()
                gridRight()
                time.sleep(0.1)
                gridLeft()
            if shift == 'torikku':
                gridDown()
                gridDown()
                gridLeft()
                gridLeft()
            if shift == 'yunaspec':
                #Yuna Special
                gridDown()
                gridRight()
                gridRight()
                gridDown()
                gridDown()
                
        if found == 0:
            if limit == 1:
                limit = 0
                print("Limit reached without success. Resetting.")
                print("Reminder, sphere type: ", sType)
                if direction == 'd' and FFX_Screen.PixelTestTol(681,611,(112, 111, 138),5):
                    #We've hit the bottom. Resetting.
                    #time.sleep(5)
                    while not FFX_Screen.PixelTestTol(680,440,(128, 127, 156),5):
                        FFX_Xbox.menuUp()
                elif direction == 'u' and FFX_Screen.PixelTestTol(680,440,(128, 127, 156),5):
                    #We've hit the top. Resetting.
                    #time.sleep(5)
                    if color != 'red':
                        print("Item sort issue. Adjusting.")
                        while not FFX_Screen.PixelTestTol(681,611,(112, 111, 138),5):
                            FFX_Xbox.menuDown()
                    elif sType == 'power':
                        print("No need to shift. Power spheres are always at the top.")
                        limit = 1
                    elif sType == 'ability':
                        direction = 'd'
                    else:
                        while not FFX_Screen.PixelTestTol(681,611,(112, 111, 138),5):
                            FFX_Xbox.menuDown()
            elif limit == 0:
                if direction == 'd' and FFX_Screen.PixelTestTol(681,611,(112, 111, 138),5):
                    limit = 1
                elif direction == 'u' and FFX_Screen.PixelTestTol(680,440,(128, 127, 156),5):
                    limit = 1