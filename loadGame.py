# Libraries and Core Files
import os
from pathlib import Path

import memory.main
import screen
import targetPathing
import xbox
import zzairShipPath

# This file is intended to load the game to a saved file.
# This assumes that the save is the first non-auto-save in the list of saves.

FFXC = xbox.controllerHandle()


def getSavedFiles():
    import vars
    gameVars = vars.varsHandle()
    saveFilesFull = sorted(
        Path(gameVars.gameSavePath()).iterdir(), key=os.path.getmtime)
    saveFiles = [os.path.basename(i) for i in saveFilesFull]
    saveFiles = saveFiles[::-1]
    return saveFiles


def loadSaveNum(number):
    saveFiles = getSavedFiles()
    testString = "ffx_" + str(number).zfill(3)
    print("Searching for string:", testString)
    savePos = 255
    for x in range(len(saveFiles)):
        if saveFiles[x] == testString:
            print("Save file is in position:", x)
            savePos = x
    memory.main.waitFrames(20)
    if savePos != 255:
        while memory.main.loadGamePos() != savePos:
            if memory.main.loadGamePos() + 4 < savePos:
                xbox.TriggerR()
            elif memory.main.loadGamePos() < savePos:
                xbox.tapDown()
            else:
                xbox.tapUp()

        for _ in range(7):
            xbox.tapB()
        FFXC.set_neutral()
        memory.main.awaitControl()
        memory.main.waitFrames(5)
        # So that we don't evaluate battle as complete after loading.
        memory.main.resetBattleEnd()
    else:
        print("That save file does not exist. Quitting program.")
        exit()


def LoadFirst():
    print("Loading to first save file")
    xbox.menuB()
    memory.main.waitFrames(30 * 2.5)
    xbox.menuDown()
    memory.main.waitFrames(30 * 0.1)
    xbox.menuB()
    memory.main.waitFrames(30 * 0.1)
    xbox.menuB()
    memory.main.awaitControl()


def loadOffset(offset):
    print("Loading to save file in position", offset)
    totalOffset = offset
    memory.main.waitFrames(30 * 2.5)
    for _ in range(totalOffset):
        xbox.tapDown()
    for _ in range(7):
        xbox.tapB()
    FFXC.set_neutral()
    memory.main.waitFrames(120)
    # So that we don't evaluate battle as complete after loading.
    memory.main.resetBattleEnd()


def loadOffsetBattle(offset):
    print("Loading to save file in position", offset)
    xbox.menuB()
    memory.main.waitFrames(30 * 2.5)
    while offset > 0:
        xbox.tapDown()
        offset -= 1
    memory.main.waitFrames(30 * 0.1)
    xbox.menuB()
    memory.main.waitFrames(30 * 0.1)
    xbox.menuB()
    memory.main.waitFrames(30 * 3)


def loadMemCursor():
    import vars
    gameVars = vars.varsHandle()
    memory.main.awaitControl()
    memory.main.openMenu()
    if memory.main.getStoryProgress() <= 200:  # Up to Besaid save, after Trials
        cursorTarget = 5
    else:
        cursorTarget = 8
    print("Aiming at", cursorTarget)
    while memory.main.getMenuCursorPos() != cursorTarget:
        print(memory.main.getMenuCursorPos())
        xbox.tapUp()
        print(memory.main.getMenuCursorPos())
        if gameVars.usePause():
            memory.main.waitFrames(2)
    while memory.main.menuNumber() == 5:
        xbox.tapB()
        if gameVars.usePause():
            memory.main.waitFrames(90)
    while memory.main.configCursor() != 3:
        xbox.tapDown()
        if gameVars.usePause():
            memory.main.waitFrames(1)
    while memory.main.configCursorColumn() != 1:
        xbox.tapRight()
        if gameVars.usePause():
            memory.main.waitFrames(1)
    memory.main.closeMenu()


def loadPostBlitz():
    print("Loading to first save file")
    loadOffset(1)

    while not screen.Minimap1():
        if screen.Minimap4():
            FFXC.set_value('AxisLx', -1)
            FFXC.set_value('AxisLy', -1)
            memory.main.waitFrames(30 * 0.5)
            FFXC.set_value('AxisLx', 0)
            memory.main.waitFrames(30 * 1)
            FFXC.set_value('AxisLy', 0)
        else:
            xbox.menuB()

    # Reverse T screen
    FFXC.set_value('AxisLx', 1)
    memory.main.waitFrames(30 * 4.5)
    FFXC.set_value('AxisLy', -1)
    memory.main.waitFrames(30 * 1)
    FFXC.set_value('AxisLy', 0)
    memory.main.waitFrames(30 * 5)
    FFXC.set_value('AxisLx', 0)

    # Carnival vendor screen
    memory.main.awaitControl()
    FFXC.set_value('AxisLy', 1)
    memory.main.waitFrames(30 * 1.5)
    FFXC.set_value('AxisLx', 1)
    memory.main.waitFrames(30 * 3)
    FFXC.set_value('AxisLx', 0)
    memory.main.waitFrames(30 * 1)
    FFXC.set_value('AxisLx', 1)
    memory.main.waitFrames(30 * 3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)

    print("Rejoining the party.")
    memory.main.clickToControl()  # Scene, rejoining the party
    print("Walking up to Yuna.")
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    memory.main.waitFrames(30 * 3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)  # Enters laughing scene, ends Luca section.
    print("End of loading section.")


def LoadNeutral():
    LoadFirst()


def LoadBaaj():
    FFXC.set_movement(1, 0)
    memory.main.waitFrames(30 * 0.4)
    FFXC.set_neutral()
    memory.main.waitFrames(30 * 0.04)


def BesaidTrials():
    # Exit Tent
    while memory.main.getMap() != 17:
        tCoords = memory.main.getCoords()
        targetPathing.setMovement([-1, tCoords[1] - 15])

    # To the temple
    while not targetPathing.setMovement([35, 182]):
        pass
    while not targetPathing.setMovement([17, 22]):
        pass
    while not targetPathing.setMovement([14, -67]):
        pass
    while memory.main.getMap() != 42:
        tCoords = memory.main.getCoords()
        targetPathing.setMovement([-2, tCoords[1] - 15])

    #Start the trials
    while memory.main.getMap() != 122:
        tCoords = memory.main.getCoords()
        targetPathing.setMovement([-2, tCoords[1] + 15])


def Boat1():
    memory.main.waitFrames(30 * 3)
    # To the junction screen, then back.
    FFXC.set_value('AxisLy', -1)
    memory.main.waitFrames(30 * 1)
    FFXC.set_value('AxisLy', 0)
    memory.main.waitFrames(30 * 6)
    FFXC.set_value('AxisLy', -1)
    memory.main.waitFrames(30 * 1)
    FFXC.set_value('AxisLy', 0)


def Kilika():
    xbox.menuB()
    memory.main.waitFrames(30 * 2.5)
    xbox.menuDown()
    memory.main.waitFrames(30 * 0.1)
    xbox.menuDown()
    memory.main.waitFrames(30 * 0.1)
    xbox.menuDown()
    memory.main.waitFrames(30 * 0.1)
    xbox.menuDown()
    memory.main.waitFrames(30 * 0.1)
    xbox.menuDown()
    memory.main.waitFrames(30 * 0.1)
    xbox.menuDown()
    memory.main.waitFrames(30 * 0.1)
    xbox.menuB()
    memory.main.waitFrames(30 * 0.1)
    xbox.menuB()
    memory.main.waitFrames(30 * 4)
    memory.main.awaitControl()


def KilikaTrials():
    FFXC.set_movement(0, -1)
    memory.main.waitFrames(30 * 2)
    FFXC.set_neutral()


def LoadMiihenStart_Laugh():
    import targetPathing
    while not targetPathing.setMovement([-440, 0]):
        pass
    memory.main.clickToEventTemple(4)

    # Reverse T screen
    memory.main.awaitControl()
    while not targetPathing.setMovement([-39, 18]):
        pass
    while not targetPathing.setMovement([3, 31]):
        pass
    while not targetPathing.setMovement([64, 15]):
        pass
    while not targetPathing.setMovement([163, 0]):
        pass
    memory.main.clickToEventTemple(2)

    # Carnival vendor screen
    memory.main.awaitControl()
    while not targetPathing.setMovement([30, -86]):
        pass
    while not targetPathing.setMovement([60, -24]):
        pass
    while not targetPathing.setMovement([101, 72]):
        pass
    while not targetPathing.setMovement([129, 101]):
        pass
    memory.main.clickToEventTemple(1)
    memory.main.waitFrames(30 * 1)
    memory.main.clickToControl()
    FFXC.set_movement(-1, -1)
    memory.main.waitFrames(30 * 0.2)
    memory.main.awaitEvent()
    FFXC.set_neutral()


def LoadMiihenStart():
    import targetPathing
    while not targetPathing.setMovement([-440, 0]):
        pass
    memory.main.clickToEventTemple(4)

    # Reverse T screen
    memory.main.awaitControl()
    while not targetPathing.setMovement([-39, 18]):
        pass
    while not targetPathing.setMovement([3, 31]):
        pass
    while not targetPathing.setMovement([64, 15]):
        pass
    while not targetPathing.setMovement([163, 0]):
        pass
    memory.main.clickToEventTemple(2)

    # Carnival vendor screen
    memory.main.awaitControl()
    while not targetPathing.setMovement([30, -86]):
        pass
    while not targetPathing.setMovement([60, -24]):
        pass
    while not targetPathing.setMovement([101, 72]):
        pass
    while not targetPathing.setMovement([129, 101]):
        pass
    memory.main.clickToEventTemple(1)

    # -----Use this if you've already done the laughing scene.
    memory.main.clickToControl()
    while not targetPathing.setMovement([2, 57]):
        pass
    while not targetPathing.setMovement([108, 59]):
        pass
    while not targetPathing.setMovement([108, 26]):
        pass
    while not targetPathing.setMovement([78, -3]):
        pass
    while not targetPathing.setMovement([-68, -7]):
        pass
    while not targetPathing.setMovement([-99, 24]):
        pass
    while not targetPathing.setMovement([-126, 117]):
        pass
    memory.main.clickToEventTemple(1)

    print("Load complete. Now for Mi'ihen area.")


def LoadMRR():
    FFXC.set_movement(-1, 1)
    memory.main.waitFrames(30 * 2)
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 1)
    FFXC.set_movement(1, 1)
    memory.main.waitFrames(30 * 2)
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 2)
    memory.main.awaitEvent()
    FFXC.set_neutral()
    memory.main.clickToControl()


def LoadMRR2():
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 0.3)
    FFXC.set_movement(1, 1)
    memory.main.waitFrames(30 * 1)
    xbox.SkipDialog(2)
    FFXC.set_neutral()
    xbox.menuB()
    memory.main.waitFrames(30 * 2)
    memory.main.awaitControl()
    for i in range(20):
        print(f"Sleeping for {20-i} more seconds...")
        memory.main.waitFrames(30 * 1)


def AfterGui():
    memory.main.awaitControl()
    FFXC.set_movement(-1, 0)
    memory.main.waitFrames(30 * 2.5)
    FFXC.set_neutral()

    target = [[463, -163], [498, 77], [615, -39], [935, 12], [1200, 200]]

    checkpoint = 0
    while memory.main.getMap() != 93:
        if memory.main.userControl():
            if targetPathing.setMovement(target[checkpoint]):
                checkpoint += 1
        else:
            FFXC.set_neutral()
    FFXC.set_neutral()


def djoseTemple():
    loadOffset(19)
    memory.main.waitFrames(30 * 6)
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    memory.main.waitFrames(30 * 1.7)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    memory.main.waitFrames(30 * 0.5)


def moonflow2():
    memory.main.waitFrames(30 * 2)
    FFXC.set_movement(-1, -1)
    memory.main.waitFrames(30 * 0.7)
    FFXC.set_neutral()
    memory.main.waitFrames(30 * 0.5)


def loadGuadoSkip():
    memory.main.clickToControl3()
    FFXC.set_movement(1, -1)
    memory.main.awaitEvent()
    FFXC.set_neutral()
    memory.main.awaitControl()
    FFXC.set_movement(-1, 0)
    memory.main.waitFrames(30 * 0.6)
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 1.5)
    FFXC.set_movement(-1, 1)
    memory.main.waitFrames(30 * 0.9)
    FFXC.set_movement(-1, -1)
    memory.main.waitFrames(30 * 2.2)
    FFXC.set_movement(1, -1)
    memory.main.waitFrames(30 * 2)
    FFXC.set_movement(1, 1)
    memory.main.awaitEvent()
    FFXC.set_neutral()
    memory.main.waitFrames(30 * 0.2)
    memory.main.awaitControl()
    FFXC.set_movement(0, -1)
    memory.main.waitFrames(30 * 1)
    FFXC.set_neutral()
    import area.guadosalam as guadosalam
    guadosalam.afterSpeech(checkpoint=26)


def loadMacLake():
    memory.main.awaitControl()
    FFXC.set_movement(0, 1)
    memory.main.awaitEvent()
    FFXC.set_neutral()
    memory.main.awaitControl()


def loadMacTemple():
    FFXC.set_movement(-1, 0)
    memory.main.waitFrames(30 * 3)
    FFXC.set_neutral()
    memory.main.awaitControl()
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 3)
    FFXC.set_neutral()


def loadMacTemple2():
    memory.main.awaitControl()
    FFXC.set_movement(-1, -1)
    memory.main.waitFrames(30 * 1.5)
    FFXC.set_movement(-1, 1)
    memory.main.waitFrames(30 * 1.5)
    FFXC.set_neutral()


def loadWendigo():
    import battle.main
    battle.main.wendigo()
    print("Wendigo fight over - end of loading game to Wendigo fight")


def loadRescue():
    memory.main.awaitControl()
    FFXC.set_movement(1, -1)
    memory.main.waitFrames(30 * 0.7)
    FFXC.set_movement(0, -1)
    while memory.main.userControl():
        pass
    FFXC.set_neutral()
    memory.main.waitFrames(30 * 1)
    memory.main.awaitControl()
    memory.main.fullPartyFormat('evrae')

    zzairShipPath.airShipPath(1)  # The run from cockpit to the deck


def loadBahamut():
    loadOffset(1)
    memory.main.awaitControl()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    memory.main.waitFrames(30 * 0.2)
    FFXC.set_value('AxisLx', 0)
    memory.main.waitFrames(30 * 2)
    FFXC.set_value('AxisLy', 0)


def loadCalm():
    FFXC.set_movement(1, 1)
    memory.main.waitFrames(30 * 1)
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 2)
    FFXC.set_neutral()
    memory.main.awaitControl()


def loadGagaGates():
    FFXC.set_movement(1, 1)
    memory.main.waitFrames(30 * 3)
    FFXC.set_movement(0, 1)
    memory.main.awaitEvent()
    FFXC.set_neutral()


def zanEntrance():
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 2)
    FFXC.set_movement(1, 1)
    memory.main.waitFrames(30 * 2.5)
    FFXC.set_neutral()


def zanTrials():
    FFXC.set_movement(1, 1)
    memory.main.waitFrames(30 * 0.5)
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 2)
    FFXC.set_neutral()


def loadGagazetDream():
    print("Positioning to next map")
    while memory.main.getMap() != 309:
        FFXC.set_movement(1, 1)
    FFXC.set_neutral()
    print("Positioning complete")
    memory.main.awaitControl()


def loadEggHunt():
    memory.main.awaitControl()
    while not targetPathing.setMovement([-10, -507]):
        pass
    while not targetPathing.setMovement([-5, -360]):
        pass

    while memory.main.getMap() != 324:
        FFXC.set_movement(0, 1)
    FFXC.set_neutral()
