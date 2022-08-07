import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_nem_menu
import FFX_memory
import FFX_targetPathNem
import FFX_vars
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()


def areaArray():
    # Not working properly
    return [60112, 60736, 61672, 62296, 62920, 63544, 58240, 58552, 59176, 59488, 59800, 60424, 61360, 61984, 62608, 63232]


def areaIndexCheck(indexNum: int = 15):
    # Not working properly
    print(FFX_memory.arenaCursor())
    if arenaArray[indexNum] == FFX_memory.arenaCursor():
        return True
    return False


def arenaCursor():
    # Not working properly
    for x in range(16):
        print(FFX_memory.arenaCursor())
        if FFX_memory.arenaCursor() == areaArray()[x]:
            return x
    return 255

def arenaMenuSelect(choice:int=2):
    print("Selecting menu option: ", choice)
    if gameVars.usePause():
        FFX_memory.waitFrames(2)
    while not FFX_memory.blitzCursor() == choice:
        if choice == 4:
            FFX_Xbox.menuA()
        elif choice == 3:
            FFX_Xbox.menuUp()
        else:
            FFX_Xbox.menuDown()
    FFX_Xbox.tapB()
    FFX_memory.waitFrames(15)


def startFight(areaIndex: int, monsterIndex: int = 0):
    print("Starting fight:", areaIndex, "|", monsterIndex)
    arenaCursor = 0
    FFX_memory.waitFrames(90)
    while arenaCursor != areaIndex:
        # print(arenaCursor())
        if arenaCursor % 2 == 0 and areaIndex % 2 == 1:
            FFX_Xbox.tapRight()
            arenaCursor += 1
        elif arenaCursor % 2 == 1 and areaIndex % 2 == 0:
            FFX_Xbox.tapLeft()
            arenaCursor -= 1
        elif arenaCursor < areaIndex:
            FFX_Xbox.tapDown()
            arenaCursor += 2
        else:
            FFX_Xbox.tapUp()
            arenaCursor -= 2
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(6)
    if monsterIndex >= 7:
        FFX_Xbox.tapRight()
        monsterIndex -= 7
    while monsterIndex > 0:
        FFX_Xbox.tapDown()
        monsterIndex -= 1
    FFX_Xbox.tapB()
    FFX_memory.waitFrames(6)
    FFX_Xbox.tapB()
    while not FFX_memory.battleActive():
        pass
