# Libraries and Core Files
import xbox
import screen
import memory
import zzairShipPath
import targetPathing
import os
from pathlib import Path

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
    memory.waitFrames(20)
    if savePos != 255:
        while memory.loadGamePos() != savePos:
            if memory.loadGamePos() + 4 < savePos:
                xbox.TriggerR()
            elif memory.loadGamePos() < savePos:
                xbox.tapDown()
            else:
                xbox.tapUp()

        for _ in range(7):
            xbox.tapB()
        FFXC.set_neutral()
        memory.awaitControl()
        memory.waitFrames(5)
        # So that we don't evaluate battle as complete after loading.
        memory.resetBattleEnd()
    else:
        print("That save file does not exist. Quitting program.")
        exit()


def LoadFirst():
    print("Loading to first save file")
    xbox.menuB()
    memory.waitFrames(30 * 2.5)
    xbox.menuDown()
    memory.waitFrames(30 * 0.1)
    xbox.menuB()
    memory.waitFrames(30 * 0.1)
    xbox.menuB()
    memory.awaitControl()


def loadOffset(offset):
    print("Loading to save file in position", offset)
    totalOffset = offset
    memory.waitFrames(30 * 2.5)
    for _ in range(totalOffset):
        xbox.tapDown()
    for _ in range(7):
        xbox.tapB()
    FFXC.set_neutral()
    memory.waitFrames(120)
    # So that we don't evaluate battle as complete after loading.
    memory.resetBattleEnd()


def loadOffsetBattle(offset):
    print("Loading to save file in position", offset)
    xbox.menuB()
    memory.waitFrames(30 * 2.5)
    while offset > 0:
        xbox.tapDown()
        offset -= 1
    memory.waitFrames(30 * 0.1)
    xbox.menuB()
    memory.waitFrames(30 * 0.1)
    xbox.menuB()
    memory.waitFrames(30 * 3)


def loadMemCursor():
    import vars
    gameVars = vars.varsHandle()
    memory.awaitControl()
    memory.openMenu()
    if memory.getStoryProgress() <= 200:  # Up to Besaid save, after Trials
        cursorTarget = 5
    else:
        cursorTarget = 8
    print("Aiming at", cursorTarget)
    while memory.getMenuCursorPos() != cursorTarget:
        print(memory.getMenuCursorPos())
        xbox.tapUp()
        print(memory.getMenuCursorPos())
        if gameVars.usePause():
            memory.waitFrames(2)
    while memory.menuNumber() == 5:
        xbox.tapB()
        if gameVars.usePause():
            memory.waitFrames(90)
    while memory.configCursor() != 3:
        xbox.tapDown()
        if gameVars.usePause():
            memory.waitFrames(1)
    while memory.configCursorColumn() != 1:
        xbox.tapRight()
        if gameVars.usePause():
            memory.waitFrames(1)
    memory.closeMenu()


def loadPostBlitz():
    print("Loading to first save file")
    loadOffset(1)

    while not screen.Minimap1():
        if screen.Minimap4():
            FFXC.set_value('AxisLx', -1)
            FFXC.set_value('AxisLy', -1)
            memory.waitFrames(30 * 0.5)
            FFXC.set_value('AxisLx', 0)
            memory.waitFrames(30 * 1)
            FFXC.set_value('AxisLy', 0)
        else:
            xbox.menuB()

    # Reverse T screen
    FFXC.set_value('AxisLx', 1)
    memory.waitFrames(30 * 4.5)
    FFXC.set_value('AxisLy', -1)
    memory.waitFrames(30 * 1)
    FFXC.set_value('AxisLy', 0)
    memory.waitFrames(30 * 5)
    FFXC.set_value('AxisLx', 0)

    # Carnival vendor screen
    memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    memory.waitFrames(30 * 1.5)
    FFXC.set_value('AxisLx', 1)
    memory.waitFrames(30 * 3)
    FFXC.set_value('AxisLx', 0)
    memory.waitFrames(30 * 1)
    FFXC.set_value('AxisLx', 1)
    memory.waitFrames(30 * 3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)

    print("Rejoining the party.")
    memory.clickToControl()  # Scene, rejoining the party
    print("Walking up to Yuna.")
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    memory.waitFrames(30 * 3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)  # Enters laughing scene, ends Luca section.
    print("End of loading section.")


def LoadNeutral():
    LoadFirst()


def LoadBaaj():
    FFXC.set_movement(1, 0)
    memory.waitFrames(30 * 0.4)
    FFXC.set_neutral()
    memory.waitFrames(30 * 0.04)


def BesaidTrials():
    loadOffset(29)
    # Exit Tent
    FFXC.set_value('AxisLy', -1)
    memory.waitFrames(30 * 1)
    FFXC.set_value('AxisLx', 1)
    memory.waitFrames(30 * 1)
    FFXC.set_value('AxisLy', 0)
    memory.waitFrames(30 * 2)
    FFXC.set_value('AxisLx', 0)
    memory.waitFrames(30 * 4)

    # To the temple
    FFXC.set_value('AxisLx', 1)
    memory.waitFrames(30 * 2)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    memory.waitFrames(30 * 12)
    FFXC.set_value('AxisLy', 0)


def Boat1():
    memory.waitFrames(30 * 3)
    # To the junction screen, then back.
    FFXC.set_value('AxisLy', -1)
    memory.waitFrames(30 * 1)
    FFXC.set_value('AxisLy', 0)
    memory.waitFrames(30 * 6)
    FFXC.set_value('AxisLy', -1)
    memory.waitFrames(30 * 1)
    FFXC.set_value('AxisLy', 0)


def Kilika():
    xbox.menuB()
    memory.waitFrames(30 * 2.5)
    xbox.menuDown()
    memory.waitFrames(30 * 0.1)
    xbox.menuDown()
    memory.waitFrames(30 * 0.1)
    xbox.menuDown()
    memory.waitFrames(30 * 0.1)
    xbox.menuDown()
    memory.waitFrames(30 * 0.1)
    xbox.menuDown()
    memory.waitFrames(30 * 0.1)
    xbox.menuDown()
    memory.waitFrames(30 * 0.1)
    xbox.menuB()
    memory.waitFrames(30 * 0.1)
    xbox.menuB()
    memory.waitFrames(30 * 4)
    memory.awaitControl()


def KilikaTrials():
    FFXC.set_movement(0, -1)
    memory.waitFrames(30 * 2)
    FFXC.set_neutral()


def LoadMiihenStart_Laugh():
    import targetPathing
    while not targetPathing.setMovement([-440, 0]):
        pass
    memory.clickToEventTemple(4)

    # Reverse T screen
    memory.awaitControl()
    while not targetPathing.setMovement([-39, 18]):
        pass
    while not targetPathing.setMovement([3, 31]):
        pass
    while not targetPathing.setMovement([64, 15]):
        pass
    while not targetPathing.setMovement([163, 0]):
        pass
    memory.clickToEventTemple(2)

    # Carnival vendor screen
    memory.awaitControl()
    while not targetPathing.setMovement([30, -86]):
        pass
    while not targetPathing.setMovement([60, -24]):
        pass
    while not targetPathing.setMovement([101, 72]):
        pass
    while not targetPathing.setMovement([129, 101]):
        pass
    memory.clickToEventTemple(1)
    memory.waitFrames(30 * 1)
    memory.clickToControl()
    FFXC.set_movement(-1, -1)
    memory.waitFrames(30 * 0.2)
    memory.awaitEvent()
    FFXC.set_neutral()


def LoadMiihenStart():
    import targetPathing
    while not targetPathing.setMovement([-440, 0]):
        pass
    memory.clickToEventTemple(4)

    # Reverse T screen
    memory.awaitControl()
    while not targetPathing.setMovement([-39, 18]):
        pass
    while not targetPathing.setMovement([3, 31]):
        pass
    while not targetPathing.setMovement([64, 15]):
        pass
    while not targetPathing.setMovement([163, 0]):
        pass
    memory.clickToEventTemple(2)

    # Carnival vendor screen
    memory.awaitControl()
    while not targetPathing.setMovement([30, -86]):
        pass
    while not targetPathing.setMovement([60, -24]):
        pass
    while not targetPathing.setMovement([101, 72]):
        pass
    while not targetPathing.setMovement([129, 101]):
        pass
    memory.clickToEventTemple(1)

    # -----Use this if you've already done the laughing scene.
    memory.clickToControl()
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
    memory.clickToEventTemple(1)

    print("Load complete. Now for Mi'ihen area.")


def LoadMRR():
    FFXC.set_movement(-1, 1)
    memory.waitFrames(30 * 2)
    FFXC.set_movement(0, 1)
    memory.waitFrames(30 * 1)
    FFXC.set_movement(1, 1)
    memory.waitFrames(30 * 2)
    FFXC.set_movement(0, 1)
    memory.waitFrames(30 * 2)
    memory.awaitEvent()
    FFXC.set_neutral()
    memory.clickToControl()


def LoadMRR2():
    FFXC.set_movement(0, 1)
    memory.waitFrames(30 * 0.3)
    FFXC.set_movement(1, 1)
    memory.waitFrames(30 * 1)
    xbox.SkipDialog(2)
    FFXC.set_neutral()
    xbox.menuB()
    memory.waitFrames(30 * 2)
    memory.awaitControl()
    for i in range(20):
        print(f"Sleeping for {20-i} more seconds...")
        memory.waitFrames(30 * 1)


def AfterGui():
    memory.awaitControl()
    FFXC.set_movement(-1, 0)
    memory.waitFrames(30 * 2.5)
    FFXC.set_neutral()

    target = [[463, -163], [498, 77], [615, -39], [935, 12], [1200, 200]]

    checkpoint = 0
    while memory.getMap() != 93:
        if memory.userControl():
            if targetPathing.setMovement(target[checkpoint]):
                checkpoint += 1
        else:
            FFXC.set_neutral()
    FFXC.set_neutral()


def djoseTemple():
    loadOffset(19)
    memory.waitFrames(30 * 6)
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    memory.waitFrames(30 * 1.7)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    memory.waitFrames(30 * 0.5)


def moonflow2():
    memory.waitFrames(30 * 2)
    FFXC.set_movement(-1, -1)
    memory.waitFrames(30 * 0.7)
    FFXC.set_neutral()
    memory.waitFrames(30 * 0.5)


def loadGuadoSkip():
    memory.clickToControl3()
    FFXC.set_movement(1, -1)
    memory.awaitEvent()
    FFXC.set_neutral()
    memory.awaitControl()
    FFXC.set_movement(-1, 0)
    memory.waitFrames(30 * 0.6)
    FFXC.set_movement(0, 1)
    memory.waitFrames(30 * 1.5)
    FFXC.set_movement(-1, 1)
    memory.waitFrames(30 * 0.9)
    FFXC.set_movement(-1, -1)
    memory.waitFrames(30 * 2.2)
    FFXC.set_movement(1, -1)
    memory.waitFrames(30 * 2)
    FFXC.set_movement(1, 1)
    memory.awaitEvent()
    FFXC.set_neutral()
    memory.waitFrames(30 * 0.2)
    memory.awaitControl()
    FFXC.set_movement(0, -1)
    memory.waitFrames(30 * 1)
    FFXC.set_neutral()
    import area.guadosalam as guadosalam
    guadosalam.afterSpeech(checkpoint=26)


def loadMacLake():
    memory.awaitControl()
    FFXC.set_movement(0, 1)
    memory.awaitEvent()
    FFXC.set_neutral()
    memory.awaitControl()


def loadMacTemple():
    FFXC.set_movement(-1, 0)
    memory.waitFrames(30 * 3)
    FFXC.set_neutral()
    memory.awaitControl()
    FFXC.set_movement(0, 1)
    memory.waitFrames(30 * 3)
    FFXC.set_neutral()


def loadMacTemple2():
    memory.awaitControl()
    FFXC.set_movement(-1, -1)
    memory.waitFrames(30 * 1.5)
    FFXC.set_movement(-1, 1)
    memory.waitFrames(30 * 1.5)
    FFXC.set_neutral()


def loadWendigo():
    import battle
    battle.wendigo()
    print("Wendigo fight over - end of loading game to Wendigo fight")


def loadRescue():
    memory.awaitControl()
    FFXC.set_movement(1, -1)
    memory.waitFrames(30 * 0.7)
    FFXC.set_movement(0, -1)
    while memory.userControl():
        pass
    FFXC.set_neutral()
    memory.waitFrames(30 * 1)
    memory.awaitControl()
    memory.fullPartyFormat('evrae')

    zzairShipPath.airShipPath(1)  # The run from cockpit to the deck


def loadBahamut():
    loadOffset(1)
    memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    memory.waitFrames(30 * 0.2)
    FFXC.set_value('AxisLx', 0)
    memory.waitFrames(30 * 2)
    FFXC.set_value('AxisLy', 0)


def loadCalm():
    FFXC.set_movement(1, 1)
    memory.waitFrames(30 * 1)
    FFXC.set_movement(0, 1)
    memory.waitFrames(30 * 2)
    FFXC.set_neutral()
    memory.awaitControl()


def loadGagaGates():
    FFXC.set_movement(1, 1)
    memory.waitFrames(30 * 3)
    FFXC.set_movement(0, 1)
    memory.awaitEvent()
    FFXC.set_neutral()


def zanEntrance():
    FFXC.set_movement(0, 1)
    memory.waitFrames(30 * 2)
    FFXC.set_movement(1, 1)
    memory.waitFrames(30 * 2.5)
    FFXC.set_neutral()


def zanTrials():
    FFXC.set_movement(1, 1)
    memory.waitFrames(30 * 0.5)
    FFXC.set_movement(0, 1)
    memory.waitFrames(30 * 2)
    FFXC.set_neutral()


def loadGagazetDream():
    print("Positioning to next map")
    while memory.getMap() != 309:
        FFXC.set_movement(1, 1)
    FFXC.set_neutral()
    print("Positioning complete")
    memory.awaitControl()


def loadEggHunt():
    memory.awaitControl()
    while not targetPathing.setMovement([-10, -507]):
        pass
    while not targetPathing.setMovement([-5, -360]):
        pass

    while memory.getMap() != 324:
        FFXC.set_movement(0, 1)
    FFXC.set_neutral()
