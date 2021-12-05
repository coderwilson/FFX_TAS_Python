import pyxinput
import time
import FFX_Xbox
import FFX_Screen
import FFX_memory

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

def _gridMove(direction: int) -> None:
    FFXC.set_value('Dpad', direction)
    time.sleep(0.04)
    FFXC.set_value('Dpad', 0)
    time.sleep(0.12)
    

def gridUp(times_to_repeat: int = 1) -> None:
    for _ in range(times_to_repeat)
        _gridMove(1)

def gridDown(times_to_repeat: int = 1) -> None:
    for _ in range(times_to_repeat)
        _gridMove(2)

def gridLeft(times_to_repeat: int = 1) -> None:
    for _ in range(times_to_repeat)
        _gridMove(4)

def gridRight(times_to_repeat: int = 1) -> None:
    for _ in range(times_to_repeat)
        _gridMove(8)

def gridOpen():
    return FFX_memory.sGridActive()
	
def _gridActive(character_num: int) -> bool:
    """ Returns True if the GridChar is the character num."""
    return FFX_memory.sGridChar() == character_num
    
def gridTidus() -> bool:
    return _gridActive(0)
    
def gridYuna() -> bool:
    return _gridActive(1)
    
def gridAuron() -> bool:
    return _gridActive(2)
    
def gridKimahri() -> bool:
    return _gridActive(3)
    
def gridWakka() -> bool:
    return _gridActive(4)
    
def gridLulu() -> bool:
    return _gridActive(5)

def gridRikku() -> bool:
    return _gridActive(6)

def firstPosition():
    return FFX_Screen.PixelTestTol(619,765,(255, 255, 255),5) and not FFX_Screen.PixelTestTol(178,786,(159, 161, 159),5)

def moveUseMenu():
    return FFX_Screen.PixelTestTol(347,526,(255, 255, 255),5)

def moveReady():
    if moveUseMenu():
        return FFX_memory.getGridMoveUsePos() == 0
    return False

def moveActive():
    if readyUseSphere():
        return False
    return FFX_Screen.PixelTestTol(178,786,(159, 161, 159),5)

def moveComplete():
    return FFX_Screen.PixelTestTol(252,584,(218, 218, 218),5) and FFX_Screen.PixelTestTol(182,546,(156, 158, 156),5)
    
def useReady():
    if moveUseMenu():
        return FFX_memory.getGridMoveUsePos() == 1
    return False

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
    return FFX_Screen.PixelTestTol(252,584,(218, 218, 218),5) and FFX_Screen.PixelTestTol(182,546,(156, 158, 156),5)
    
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
	match toon:
        case 'yuna':
            while not gridYuna():
                if readyUseSphere():
                    FFX_Xbox.menuB()
                elif moveUseMenu():
                    FFX_Xbox.menuBack()
                elif firstPosition():
                    FFX_Xbox.shoulderRight()
        case 'lulu':
            while not gridLulu():
                if readyUseSphere():
                    FFX_Xbox.menuB()
                elif moveUseMenu():
                    FFX_Xbox.menuBack()
                elif firstPosition():
                    FFX_Xbox.shoulderRight()
                    time.sleep(0.3)
        case 'auron':
            while not gridAuron():
                if readyUseSphere():
                    FFX_Xbox.menuB()
                elif moveUseMenu():
                    FFX_Xbox.menuBack()
                elif firstPosition():
                    FFX_Xbox.shoulderRight()
        case 'wakka':
            while not gridWakka():
                if readyUseSphere():
                    FFX_Xbox.menuB()
                elif moveUseMenu():
                    FFX_Xbox.menuBack()
                elif firstPosition():
                    FFX_Xbox.shoulderRight()
        case 'tidus':
            while not gridTidus():
                if readyUseSphere():
                    FFX_Xbox.menuB()
                elif moveUseMenu():
                    FFX_Xbox.menuBack()
                elif firstPosition():
                    FFX_Xbox.shoulderRight()
        case 'kimahri':
            while not gridKimahri():
                if readyUseSphere():
                    FFX_Xbox.menuB()
                elif moveUseMenu():
                    FFX_Xbox.menuBack()
                elif firstPosition():
                    FFX_Xbox.shoulderRight()
        case 'rikku':
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
    match sType:
        case 'power':
            return 70
        case 'mana':
            return 71
        case 'speed':
            return 72
        case 'ability':
            return 73
        case 'fortune':
            return 74
        case 'attribute':
            return 75
        case 'special':
            return 76
        case 'skill':
            return 77
        case 'wmag':
            return 78
        case 'bmag':
            return 79
        case 'master':
            return 80
        case 'lv1':
            return 81
        case 'lv2':
            return 82
        case 'lv3':
            return 83
        case 'lv4':
            return 84
        case 'hp':
            return 85
        case 'mp':
            return 86
        case 'strength':
            return 87
        case 'defense':
            return 88
        case 'magic':
            return 89
        case 'mdef':
            return 90
        case 'agility':
            return 91
        case 'evasion':
            return 92
        case 'accuracy':
            return 93
        case 'luck':
            return 94
        case 'clear':
            return 95
        case 'ret':
            return 96
        case 'friend':
            return 97
        case 'tele':
            return 98
        case 'warp':
            return 99
        case _:
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
        match shift:
            case 'up':
                gridUp(1)
            case 'left':
                gridLeft(1)
            case 'l5':
                gridLeft(5)
            case 'right':
                gridRight(1)
            case 'r2':
                gridRight(2)
            case 'down':
                gridDown(1)
            case 'd2':
                gridDown(2)
            case 'up2':
                gridUp(2)
            case 'd5':
                gridDown(5)
            case 'aftersk':
                gridUp(1)
                gridRight(1)
                gridDown(1)
            case 'aftersk2':
                gridRight(2)
                time.sleep(0.1)
                gridLeft(1)
            case 'torikku':
                time.sleep(0.2)
                gridDown(2)
                gridLeft(2)
            case 'yunaspec':
                #Yuna Special
                gridDown(1)
                gridRight(2)
                gridDown(2)
        FFX_Xbox.SkipDialog(0.7)