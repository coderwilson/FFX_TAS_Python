import xbox
import memory.main
import vars
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def gridUp():
    FFXC.set_value('Dpad', 1)
    memory.main.waitFrames(2)
    FFXC.set_value('Dpad', 0)
    memory.main.waitFrames(3)


def gridDown():
    FFXC.set_value('Dpad', 2)
    memory.main.waitFrames(2)
    FFXC.set_value('Dpad', 0)
    memory.main.waitFrames(3)


def gridLeft():
    FFXC.set_value('Dpad', 4)
    memory.main.waitFrames(2)
    FFXC.set_value('Dpad', 0)
    memory.main.waitFrames(3)


def gridRight():
    FFXC.set_value('Dpad', 8)
    memory.main.waitFrames(2)
    FFXC.set_value('Dpad', 0)
    memory.main.waitFrames(3)


def gridTidus():
    if memory.main.sGridChar() == 0:
        return True
    else:
        return False


def gridKimahri():
    if memory.main.sGridChar() == 3:
        return True
    else:
        return False


def gridAuron():
    if memory.main.sGridChar() == 2:
        return True
    else:
        return False


def gridLulu():
    if memory.main.sGridChar() == 5:
        return True
    else:
        return False


def gridWakka():
    if memory.main.sGridChar() == 4:
        return True
    else:
        return False


def gridYuna():
    if memory.main.sGridChar() == 1:
        return True
    else:
        return False


def gridRikku():
    if memory.main.sGridChar() == 6:
        return True
    else:
        return False


def firstPosition():
    if memory.main.sGridMenu() == 255:
        if memory.main.getGridMoveActive():
            return False
        else:
            return True
    else:
        return False


def moveUseMenu():
    if memory.main.sGridMenu() == 7:
        return True
    else:
        return False


def moveReady():
    if moveUseMenu():
        if memory.main.getGridMoveUsePos() == 0:
            return True
        else:
            return False
    elif readyUseSphere() or moveActive():
        xbox.menuA()
    else:
        return False


def moveActive():
    if memory.main.getGridMoveActive() and memory.main.sGridMenu() == 255:
        return True
    else:
        return False


def moveComplete():
    if memory.main.getGridMoveActive() and memory.main.sGridMenu() == 11:
        return True
    else:
        return False


def useReady():
    if moveUseMenu():
        if memory.main.getGridMoveUsePos() == 1:
            return True
        else:
            return False
    elif readyUseSphere() or moveActive():
        xbox.menuA()
    else:
        return False


def readySelectSphere():
    if memory.main.sGridMenu() == 8:
        return True
    else:
        return False


def readyUseSphere():
    if memory.main.getGridUseActive():
        return True
    else:
        return False


def quitGridReady():
    if memory.main.sGridMenu() == 11:
        if useReady():
            return False
        elif moveComplete():
            return False
        else:
            return True
    else:
        return False


def useFirst():
    print("use first")
    while not readySelectSphere():
        if firstPosition():
            xbox.menuB()
        elif moveReady():
            xbox.menuDown()
        elif useReady():
            xbox.menuB()
    return True


def moveFirst():
    print("move first")
    while not moveActive():
        if firstPosition():
            xbox.menuB()
        elif moveReady():
            xbox.menuB()
            memory.main.waitFrames(3)
        elif useReady():
            xbox.menuUp()
    return True


def moveAndUse():
    print("move and use")
    memory.main.waitFrames(1)
    xbox.menuB()
    memory.main.waitFrames(1)
    while not readySelectSphere():
        if moveComplete() or firstPosition():
            xbox.menuB()
        elif moveReady():
            xbox.menuDown()
        elif useReady():
            xbox.menuB()
    return True


def useAndMove():
    print("use and move")
    memory.main.waitFrames(1)
    xbox.menuB()
    memory.main.waitFrames(1)
    while not moveActive():
        if readyUseSphere() or firstPosition():
            xbox.menuB()
        elif moveReady():
            xbox.menuB()
        elif useReady():
            xbox.menuUp()
        else:
            xbox.menuB()
    return True


def useAndUseAgain():
    print("use and use again")
    memory.main.waitFrames(1)
    xbox.menuB()
    memory.main.waitFrames(1)
    while not readySelectSphere():
        if readyUseSphere() or firstPosition():
            xbox.menuB()
        elif moveReady():
            xbox.menuDown()
        elif useReady():
            xbox.menuB()
    if gameVars.usePause():
        memory.main.waitFrames(6)
    return True


def useShiftLeft(toon):
    print("use and shift")
    memory.main.waitFrames(1)
    xbox.menuB()
    toon = toon.lower()
    if toon == 'yuna':
        while not gridYuna():
            if readyUseSphere():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderLeft()
    if toon == 'lulu':
        while not gridLulu():
            if readyUseSphere():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderLeft()
    if toon == 'auron':
        while not gridAuron():
            if readyUseSphere():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderLeft()
    if toon == 'wakka':
        while not gridWakka():
            if readyUseSphere():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderLeft()
    if toon == 'tidus':
        while not gridTidus():
            if readyUseSphere():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderLeft()
    if toon == 'kimahri':
        while not gridKimahri():
            if readyUseSphere():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderLeft()
    if toon == 'rikku':
        while not gridRikku():
            if readyUseSphere():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderLeft()
    print("Ready for grid: " + toon)


def useShiftRight(toon):
    print("use and shift")
    xbox.menuB()
    toon = toon.lower()
    if toon == 'yuna':
        while not gridYuna():
            if readyUseSphere():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderRight()
    if toon == 'lulu':
        while not gridLulu():
            if readyUseSphere():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderRight()
                memory.main.waitFrames(30 * 0.3)
    if toon == 'auron':
        while not gridAuron():
            if readyUseSphere():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderRight()
    if toon == 'wakka':
        while not gridWakka():
            if readyUseSphere():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderRight()
    if toon == 'tidus':
        while not gridTidus():
            if readyUseSphere():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderRight()
    if toon == 'kimahri':
        while not gridKimahri():
            if readyUseSphere():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderRight()
    if toon == 'rikku':
        while not gridRikku():
            if readyUseSphere():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderRight()
    print("Ready for grid: " + toon)


def moveShiftLeft(toon):
    print("Move and shift, left")
    memory.main.waitFrames(2)
    xbox.menuB()
    memory.main.waitFrames(2)
    toon = toon.lower()
    if toon == 'yuna':
        while not gridYuna():
            if moveReady() or moveActive() or moveComplete():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderLeft()
    if toon == 'lulu':
        while not gridLulu():
            if moveReady() or moveActive() or moveComplete():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderLeft()
    if toon == 'tidus':
        while not gridTidus():
            if moveReady() or moveActive() or moveComplete():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderLeft()
    if toon == 'rikku':
        while not gridRikku():
            if moveReady() or moveActive() or moveComplete():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderLeft()
    print("Ready for grid: " + toon)


def moveShiftRight(toon):
    print("Move and shift, right")
    memory.main.waitFrames(2)
    xbox.menuB()
    memory.main.waitFrames(2)
    toon = toon.lower()
    if toon == 'yuna':
        while not gridYuna():
            if moveReady() or moveActive() or moveComplete():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderRight()
    elif toon == 'lulu':
        while not gridLulu():
            if moveReady() or moveActive() or moveComplete():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderRight()
    if toon == 'tidus':
        while not gridTidus():
            if moveReady() or moveActive() or moveComplete():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderRight()
    if toon == 'rikku':
        while not gridRikku():
            if moveReady() or moveActive() or moveComplete():
                xbox.menuB()
            elif moveUseMenu():
                xbox.menuBack()
            elif firstPosition():
                xbox.shoulderRight()
    print("Ready for grid: " + toon)


def useAndQuit():
    memory.main.waitFrames(30 * 0.1)
    xbox.menuB()
    while memory.main.sGridActive():
        if readyUseSphere():
            print("Using the current item.")
            xbox.menuB()
        elif firstPosition():
            print("Opening the Quit menu")
            xbox.menuA()
        elif quitGridReady():
            print("quitting sphere grid")
            xbox.menuB()
    while memory.main.menuNumber() != 5:
        pass
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


def selSphere(sType, shift):
    sNum = 255
    menuPos = 0
    print("------------------------------")
    print(sType)
    sNum = sphereNum(sType)
    print(sNum)
    menuPos = memory.main.getGridItemsSlot(sNum)
    print(menuPos)
    print("------------------------------")
    if menuPos == 255:
        print("Sphere", sType, "is not in inventory.")
        return
    while menuPos != memory.main.getGridCursorPos():
        if menuPos > memory.main.getGridCursorPos():
            if gameVars.usePause():
                xbox.tapDown()
            else:
                if menuPos - memory.main.getGridCursorPos() >= 3 and len(memory.main.getGridItemsOrder()) > 4:
                    if menuPos - memory.main.getGridCursorPos() == 3 and menuPos == len(memory.main.getGridItemsOrder()) - 1:
                        xbox.tapDown()
                    else:
                        xbox.TriggerR()
                else:
                    xbox.tapDown()
        elif menuPos < memory.main.getGridCursorPos():
            if gameVars.usePause():
                xbox.tapUp()
            else:
                if memory.main.getGridCursorPos() - menuPos >= 3:
                    if (menuPos == 0 and memory.main.getGridCursorPos() - menuPos == 3) or len(memory.main.getGridItemsOrder()) <= 4:
                        xbox.tapUp()
                    else:
                        xbox.TriggerL()
                else:
                    xbox.tapUp()
    while not memory.main.sphereGridPlacementOpen():
        xbox.menuB()
    if shift == 'up':
        gridUp()
    if shift == 'left':
        gridLeft()
    if shift == 'l2':
        gridLeft()
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
        memory.main.waitFrames(4)
        if memory.main.sGridNodeSelected() == [248, 195]:
            gridDown()
    if shift == 'aftersk2':
        gridRight()
        gridRight()
        memory.main.waitFrames(30 * 0.1)
        gridLeft()
    if shift == 'afterBYSpec':
        gridRight()
        gridRight()
        gridUp()
    if shift == 'torikku':
        memory.main.waitFrames(30 * 0.2)
        gridDown()
        gridDown()
        gridLeft()
        gridLeft()
    if shift == 'yunaspec':
        # Yuna Special
        gridDown()
        gridRight()
        gridRight()
        gridDown()
        gridDown()
    while memory.main.sphereGridPlacementOpen():
        xbox.menuB()
