import memory.main
import vars
import xbox

gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def areaArray():
    # Not working properly
    return [
        60112,
        60736,
        61672,
        62296,
        62920,
        63544,
        58240,
        58552,
        59176,
        59488,
        59800,
        60424,
        61360,
        61984,
        62608,
        63232,
    ]


def areaIndexCheck(indexNum: int = 15):
    # Not working properly
    print(memory.main.arenaCursor())
    if memory.main.arenaArray[indexNum] == memory.main.arenaCursor():
        return True
    return False


def arenaCursor():
    # Not working properly
    for x in range(16):
        print(memory.main.arenaCursor())
        if memory.main.arenaCursor() == areaArray()[x]:
            return x
    return 255


def arenaMenuSelect(choice: int = 2):
    print("Selecting menu option: ", choice)
    if gameVars.usePause():
        memory.main.waitFrames(2)
    while not memory.main.blitzCursor() == choice:
        if choice == 4:
            xbox.menuA()
        elif choice == 3:
            xbox.menuUp()
        else:
            xbox.menuDown()
    xbox.tapB()
    memory.main.waitFrames(15)


def startFight(areaIndex: int, monsterIndex: int = 0):
    print("Starting fight: ", areaIndex, " | ", monsterIndex)
    arenaCursor = 0
    memory.main.waitFrames(90)
    while arenaCursor != areaIndex:
        # print(arenaCursor())
        if arenaCursor % 2 == 0 and areaIndex % 2 == 1:
            xbox.tapRight()
            arenaCursor += 1
        elif arenaCursor % 2 == 1 and areaIndex % 2 == 0:
            xbox.tapLeft()
            arenaCursor -= 1
        elif arenaCursor < areaIndex:
            xbox.tapDown()
            arenaCursor += 2
        else:
            xbox.tapUp()
            arenaCursor -= 2
    xbox.menuB()
    memory.main.waitFrames(6)
    if monsterIndex >= 7:
        xbox.tapRight()
        monsterIndex -= 7
    while monsterIndex > 0:
        xbox.tapDown()
        monsterIndex -= 1
    xbox.tapB()
    memory.main.waitFrames(6)
    xbox.tapB()
    while not memory.main.battleActive():
        pass
