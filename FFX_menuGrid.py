import pyxinput
import time
import FFX_Xbox
import FFX_Screen
import FFX_memory

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

def gridUp():
    FFXC.set_value('Dpad', 1)
    FFX_memory.waitFrames(1)
    FFXC.set_value('Dpad', 0)
    FFX_memory.waitFrames(4)

def gridDown():
    FFXC.set_value('Dpad', 2)
    FFX_memory.waitFrames(1)
    FFXC.set_value('Dpad', 0)
    FFX_memory.waitFrames(4)

def gridLeft():
    FFXC.set_value('Dpad', 4)
    FFX_memory.waitFrames(1)
    FFXC.set_value('Dpad', 0)
    FFX_memory.waitFrames(4)

def gridRight():
    FFXC.set_value('Dpad', 8)
    FFX_memory.waitFrames(1)
    FFXC.set_value('Dpad', 0)
    FFX_memory.waitFrames(4)

def gridTidus():
    if FFX_memory.sGridChar() == 0:
        return True
    else:
        return False
    
def gridKimahri():
    if FFX_memory.sGridChar() == 3:
        return True
    else:
        return False
    
def gridAuron():
    if FFX_memory.sGridChar() == 2:
        return True
    else:
        return False
    
def gridLulu():
    if FFX_memory.sGridChar() == 5:
        return True
    else:
        return False
    
def gridWakka():
    if FFX_memory.sGridChar() == 4:
        return True
    else:
        return False
    
def gridYuna():
    if FFX_memory.sGridChar() == 1:
        return True
    else:
        return False

def gridRikku():
    if FFX_memory.sGridChar() == 6:
        return True
    else:
        return False

def firstPosition():
    if FFX_memory.sGridMenu() == 255:
        if FFX_memory.getGridMoveActive():
            return False
        else:
            return True
    else: return False

def moveUseMenu():
    if FFX_memory.sGridMenu() == 7:
        return True
    else:
        return False

def moveReady():
    if moveUseMenu():
        if FFX_memory.getGridMoveUsePos() == 0:
            return True
        else:
            return False
    elif readyUseSphere() or moveActive():
        FFX_Xbox.menuA()
    else: return False

def moveActive():
    if FFX_memory.getGridMoveActive() and FFX_memory.sGridMenu() == 255:
        return True
    else:
        return False

def moveComplete():
    if FFX_memory.getGridMoveActive() and FFX_memory.sGridMenu() == 11:
        return True
    else:
        return False

    
def useReady():
    if moveUseMenu():
        if FFX_memory.getGridMoveUsePos() == 1:
            return True
        else:
            return False
    elif readyUseSphere() or moveActive():
        FFX_Xbox.menuA()
    else: return False

def readySelectSphere():
    if FFX_memory.sGridMenu() == 8:
        return True
    else:
        return False

def readyUseSphere():
    if FFX_memory.getGridUseActive():
        return True
    else:
        return False
    
def quitGridReady():
    if FFX_memory.sGridMenu() == 11:
        if useReady():
            return False
        elif moveComplete():
            return False
        else:
            return True
    else: return False

def useFirst():
    print("use first")
    while not readySelectSphere():
        if firstPosition():
            FFX_Xbox.menuB()
        elif moveReady():
            FFX_Xbox.menuDown()
        elif useReady():
            FFX_Xbox.menuB()
    #FFX_memory.waitFrames(30 * 0.4)
    return True

def moveFirst():
    print("move first")
    while not moveActive():
        if firstPosition():
            FFX_Xbox.menuB()
        elif moveReady():
            FFX_Xbox.menuB()
            FFX_memory.waitFrames(3)
        elif useReady():
            FFX_Xbox.menuUp()
    #FFX_memory.waitFrames(30 * 0.2)
    return True

def moveAndUse():
    print("move and use")
    FFX_memory.waitFrames(2)
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(1)
    while not readySelectSphere():
        if moveComplete() or firstPosition():
            FFX_Xbox.menuB()
        elif moveReady():
            FFX_Xbox.menuDown()
        elif useReady():
            FFX_Xbox.menuB()
    #FFX_memory.waitFrames(30 * 0.2)
    return True

def useAndMove():
    print("use and move")
    FFX_memory.waitFrames(1)
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(1)
    while not moveActive():
        if readyUseSphere() or firstPosition():
            FFX_Xbox.menuB()
        elif moveReady():
            FFX_Xbox.menuB()
            FFX_memory.waitFrames(3)
        elif useReady():
            FFX_Xbox.menuUp()
        else:
            FFX_Xbox.menuB()
    #FFX_memory.waitFrames(30 * 0.2)
    return True

def useAndUseAgain():
    print("use and use again")
    FFX_memory.waitFrames(1)
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(1)
    while not readySelectSphere():
        if readyUseSphere() or firstPosition():
            FFX_Xbox.menuB()
        elif moveReady():
            FFX_Xbox.menuDown()
        elif useReady():
            FFX_Xbox.menuB()
    #FFX_memory.waitFrames(30 * 0.2)
    return True

def useShiftLeft(toon):
    print("use and shift")
    FFX_memory.waitFrames(1)
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
    #FFX_memory.waitFrames(30 * 0.1)
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
                FFX_memory.waitFrames(30 * 0.3)
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
    FFX_memory.waitFrames(2)
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(2)
    toon = toon.lower()
    if toon == 'yuna':
        while not gridYuna():
            if moveReady() or moveActive() or moveComplete():
                FFX_Xbox.menuB()
            elif moveUseMenu():
                FFX_Xbox.menuBack()
            elif firstPosition():
                FFX_Xbox.shoulderRight()
    elif toon == 'lulu':
        while not gridLulu():
            if moveReady() or moveActive() or moveComplete():
                FFX_Xbox.menuB()
            elif moveUseMenu():
                FFX_Xbox.menuBack()
            elif firstPosition():
                FFX_Xbox.shoulderRight()
    print("Ready for grid: " + toon)

def useAndQuit():
    FFX_memory.waitFrames(30 * 0.1)
    FFX_Xbox.menuB()
    while FFX_memory.sGridActive():
        if readyUseSphere():
            print("Using the current item.")
            FFX_Xbox.menuB()
        elif firstPosition():
            print("Opening the Quit menu")
            FFX_Xbox.menuA()
        elif quitGridReady():
            print("quitting sphere grid")
            FFX_Xbox.menuB()
    FFX_memory.waitFrames(20)
    return True

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
            FFX_memory.waitFrames(30 * 0.1)
            if menuPos == FFX_memory.getGridCursorPos():
                FFX_Xbox.menuB()
                complete = True
    if shift == 'none':
        FFX_Xbox.SkipDialog(0.7)
    else:
        FFX_memory.waitFrames(30 * 0.2)
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
            FFX_memory.waitFrames(30 * 0.1)
            gridLeft()
        if shift == 'torikku':
            FFX_memory.waitFrames(30 * 0.2)
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
