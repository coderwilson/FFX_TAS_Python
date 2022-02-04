# Libraries and Core Files
import time
import FFX_Xbox
import FFX_Screen
import FFX_memory
import FFX_menu
import FFX_menuGrid
import FFX_zzairShipPath
import pyautogui
import FFX_targetPathing

#This file is intended to load the game to a saved file.
#This assumes that the save is the first non-auto-save in the list of saves.

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

def LoadFirst():
    print("Loading to first save file")
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(30 * 2.5)
    FFX_Xbox.menuDown()
    FFX_memory.waitFrames(30 * 0.1)
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(30 * 0.1)
    FFX_Xbox.menuB()
    FFX_memory.awaitControl()

def loadOffset(offset):
    print("Loading to save file in position ", offset)
    #FFX_memory.waitFrames(30 * 0.2)
    #FFX_Xbox.menuB()
    FFX_memory.waitFrames(30 * 2.5)
    for _ in range(offset):
        FFX_Xbox.tapDown()
    for _ in range(15):
        FFX_Xbox.tapB()
    FFX_memory.awaitControl()
    FFX_memory.waitFrames(30 * 0.5)
    FFX_memory.resetBattleEnd() #So that we don't evaluate battle as complete after loading.
    FFXC.set_neutral()

def loadOffsetBattle(offset):
    print("Loading to save file in position ", offset)
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(30 * 2.5)
    while offset > 0:
        FFX_Xbox.tapDown()
        offset -= 1
    FFX_memory.waitFrames(30 * 0.1)
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(30 * 0.1)
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(30 * 3)

def loadMemCursor():
    import FFX_vars
    gameVars = FFX_vars.varsHandle()
    FFX_memory.awaitControl()
    FFX_memory.openMenu()
    if FFX_memory.getStoryProgress() <= 200: #Up to Besaid save, after Trials
        cursorTarget = 5
    else:
        cursorTarget = 8# if FFX_memory.getStoryProgress() > 3000 else 9
    print("Aiming at ", cursorTarget)
    while FFX_memory.getMenuCursorPos() != cursorTarget:
        print(FFX_memory.getMenuCursorPos())
        FFX_Xbox.tapUp()
        print(FFX_memory.getMenuCursorPos())
        if gameVars.usePause():
            FFX_memory.waitFrames(2)
    while FFX_memory.menuNumber() == 5:
        FFX_Xbox.tapB()
        if gameVars.usePause():
            FFX_memory.waitFrames(90)
    while FFX_memory.configCursor() != 3:
        FFX_Xbox.tapDown()
        if gameVars.usePause():
            FFX_memory.waitFrames(1)
    while FFX_memory.configCursorColumn() != 1:
        FFX_Xbox.tapRight()
        if gameVars.usePause():
            FFX_memory.waitFrames(1)
    FFX_memory.closeMenu()

def loadPostBlitz():
    print("Loading to first save file")
    loadOffset(1)
    
    while not FFX_Screen.Minimap1():
        if FFX_Screen.Minimap4():
            FFXC.set_value('AxisLx', -1)
            FFXC.set_value('AxisLy', -1)
            FFX_memory.waitFrames(30 * 0.5)
            FFXC.set_value('AxisLx', 0)
            FFX_memory.waitFrames(30 * 1)
            FFXC.set_value('AxisLy', 0)
        else:
            FFX_Xbox.menuB()
    
    #Reverse T screen
    FFXC.set_value('AxisLx', 1)
    FFX_memory.waitFrames(30 * 4.5)
    FFXC.set_value('AxisLy', -1)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.waitFrames(30 * 5)
    FFXC.set_value('AxisLx', 0)
    
    #Carnival vendor screen
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    FFX_memory.waitFrames(30 * 1.5)
    FFXC.set_value('AxisLx', 1)
    FFX_memory.waitFrames(30 * 3)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_value('AxisLx', 1)
    FFX_memory.waitFrames(30 * 3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    print("Rejoining the party.")
    FFX_memory.clickToControl() #Scene, rejoining the party
    print("Walking up to Yuna.")
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    FFX_memory.waitFrames(30 * 3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0) #Enters laughing scene, ends Luca section.
    print("End of loading section.")

def LoadNeutral():
    LoadFirst()
    
def LoadBaaj():
    FFXC.set_movement(1, 0)
    FFX_memory.waitFrames(30 * 0.4)
    FFXC.set_neutral()
    FFX_memory.waitFrames(30 * 0.04)

def BesaidTrials() :
    loadOffset(29)
    #Exit Tent
    FFXC.set_value('AxisLy', -1)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_value('AxisLx', 1)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.waitFrames(30 * 2)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.waitFrames(30 * 4)
    
    #To the temple
    FFXC.set_value('AxisLx', 1)
    FFX_memory.waitFrames(30 * 2)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    FFX_memory.waitFrames(30 * 12)
    FFXC.set_value('AxisLy', 0)

def Boat1() :
    FFX_memory.waitFrames(30 * 3)
    #To the junction screen, then back.
    FFXC.set_value('AxisLy', -1)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.waitFrames(30 * 6)
    FFXC.set_value('AxisLy', -1)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_value('AxisLy', 0)

def Kilika():
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(30 * 2.5)
    FFX_Xbox.menuDown()
    FFX_memory.waitFrames(30 * 0.1)
    FFX_Xbox.menuDown()
    FFX_memory.waitFrames(30 * 0.1)
    FFX_Xbox.menuDown()
    FFX_memory.waitFrames(30 * 0.1)
    FFX_Xbox.menuDown()
    FFX_memory.waitFrames(30 * 0.1)
    FFX_Xbox.menuDown()
    FFX_memory.waitFrames(30 * 0.1)
    FFX_Xbox.menuDown()
    FFX_memory.waitFrames(30 * 0.1)
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(30 * 0.1)
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(30 * 4)
    FFX_memory.awaitControl()

def KilikaTrials():
    FFXC.set_movement(0, -1)
    FFX_memory.waitFrames(30 * 2)
    FFXC.set_neutral()

def LoadMiihenStart_Laugh():
    import FFX_targetPathing
    while not FFX_targetPathing.setMovement([-440,0]):
        doNothing = True
    FFX_memory.clickToEventTemple(4)
    
    #Reverse T screen
    FFX_memory.awaitControl()
    while not FFX_targetPathing.setMovement([-39,18]):
        doNothing = True
    while not FFX_targetPathing.setMovement([3,31]):
        doNothing = True
    while not FFX_targetPathing.setMovement([64,15]):
        doNothing = True
    while not FFX_targetPathing.setMovement([163,0]):
        doNothing = True
    FFX_memory.clickToEventTemple(2)
    
    #Carnival vendor screen
    FFX_memory.awaitControl()
    while not FFX_targetPathing.setMovement([30,-86]):
        doNothing = True
    while not FFX_targetPathing.setMovement([60,-24]):
        doNothing = True
    while not FFX_targetPathing.setMovement([101,72]):
        doNothing = True
    while not FFX_targetPathing.setMovement([129,101]):
        doNothing = True
    FFX_memory.clickToEventTemple(1)
    FFX_memory.waitFrames(30 * 1)
    FFX_memory.clickToControl()
    FFXC.set_movement(-1, -1)
    FFX_memory.waitFrames(30 * 0.2)
    FFX_memory.awaitEvent()
    FFXC.set_neutral()

def LoadMiihenStart():
    import FFX_targetPathing
    while not FFX_targetPathing.setMovement([-440,0]):
        doNothing = True
    FFX_memory.clickToEventTemple(4)
    
    #Reverse T screen
    FFX_memory.awaitControl()
    while not FFX_targetPathing.setMovement([-39,18]):
        doNothing = True
    while not FFX_targetPathing.setMovement([3,31]):
        doNothing = True
    while not FFX_targetPathing.setMovement([64,15]):
        doNothing = True
    while not FFX_targetPathing.setMovement([163,0]):
        doNothing = True
    FFX_memory.clickToEventTemple(2)
    
    #Carnival vendor screen
    FFX_memory.awaitControl()
    while not FFX_targetPathing.setMovement([30,-86]):
        doNothing = True
    while not FFX_targetPathing.setMovement([60,-24]):
        doNothing = True
    while not FFX_targetPathing.setMovement([101,72]):
        doNothing = True
    while not FFX_targetPathing.setMovement([129,101]):
        doNothing = True
    FFX_memory.clickToEventTemple(1)
    
    
    #-----Use this if you've already done the laughing scene.
    FFX_memory.clickToControl()
    while not FFX_targetPathing.setMovement([2,57]):
        doNothing = True
    while not FFX_targetPathing.setMovement([108,59]):
        doNothing = True
    while not FFX_targetPathing.setMovement([108,26]):
        doNothing = True
    while not FFX_targetPathing.setMovement([78,-3]):
        doNothing = True
    while not FFX_targetPathing.setMovement([-68,-7]):
        doNothing = True
    while not FFX_targetPathing.setMovement([-99,24]):
        doNothing = True
    while not FFX_targetPathing.setMovement([-126,117]):
        doNothing = True
    FFX_memory.clickToEventTemple(1)
    
    print("Load complete. Now for Mi'ihen area.")

def LoadMRR():
    FFXC.set_movement(-1, 1)
    FFX_memory.waitFrames(30 * 2)
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_movement(1, 1)
    FFX_memory.waitFrames(30 * 2)
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 2)
    FFX_memory.awaitEvent()
    FFXC.set_neutral()
    FFX_memory.clickToControl()

def LoadMRR2():
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 0.3)
    FFXC.set_movement(1, 1)
    FFX_memory.waitFrames(30 * 1)
    FFX_Xbox.SkipDialog(2)
    FFXC.set_neutral()
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(30 * 2)
    FFX_memory.awaitControl()
    for i in range(20):
        print(f"Sleeping for {20-i} more seconds...")
        FFX_memory.waitFrames(30 * 1)

def AfterGui():
    FFX_memory.awaitControl()
    FFXC.set_movement(-1, 0)
    FFX_memory.waitFrames(30 * 2.5)
    FFXC.set_neutral()
    
    target = [[463,-163],[498,77],[615,-39],[935,12],[1200,200]]
    
    checkpoint = 0
    while FFX_memory.getMap() != 93:
        if FFX_memory.userControl():
            if FFX_targetPathing.setMovement(target[checkpoint]):
                checkpoint += 1
        else:
            FFXC.set_neutral()
    FFXC.set_neutral()
    
def djoseTemple():
    loadOffset(19)
    FFX_memory.waitFrames(30 * 6)
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    FFX_memory.waitFrames(30 * 1.7)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.waitFrames(30 * 0.5)
    
def moonflow2():
    FFX_memory.waitFrames(30 * 2)
    FFXC.set_movement(-1, -1)
    FFX_memory.waitFrames(30 * 0.7)
    FFXC.set_neutral()
    FFX_memory.waitFrames(30 * 0.5)

def loadGuadoSkip():
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_movement(1, -1)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_neutral()
    FFX_memory.awaitControl()
    FFXC.set_movement(-1, 0)
    FFX_memory.waitFrames(30 * 0.6)
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 1.5)
    FFXC.set_movement(-1, 1)
    FFX_memory.waitFrames(30 * 0.9)
    FFXC.set_movement(-1, -1)
    FFX_memory.waitFrames(30 * 2.2)
    FFXC.set_movement(1, -1)
    FFX_memory.waitFrames(30 * 2)
    FFXC.set_movement(1, 1)
    FFX_memory.awaitEvent()
    FFXC.set_neutral()
    FFX_memory.waitFrames(30 * 0.2)
    FFX_memory.awaitControl()
    FFXC.set_movement(0, -1)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_neutral()
    import FFX_Guadosalam
    FFX_Guadosalam.afterSpeech(checkpoint = 26)

def loadMacLake():
    FFX_memory.awaitControl()
    FFXC.set_movement(0, 1)
    FFX_memory.awaitEvent()
    FFXC.set_neutral()
    FFX_memory.awaitControl()

def loadMacTemple():
    FFXC.set_movement(-1, 0)
    FFX_memory.waitFrames(30 * 3)
    FFXC.set_neutral()
    FFX_memory.awaitControl()
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 3)
    FFXC.set_neutral()
    
def loadMacTemple2():
    loadOffset(42)
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', -1)
    FFX_memory.waitFrames(30 * 1.5)
    FFXC.set_value('AxisLy', 1)
    FFX_memory.waitFrames(30 * 1.5)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)

def loadWendigo():
    import FFX_Battle
    #FFX_memory.awaitControl()
    #while FFX_memory.getBattleNum() < 195:
    #    if FFX_Screen.BattleScreen():
    #        FFXC.set_neutral()
    #        FFX_Battle.fleeAll()
    #    elif FFX_memory.userControl():
    #        set_movement(0, -1)
    #    else:
    #        FFXC.set_neutral()
    
    FFX_Battle.wendigo()
    print("Wendigo fight over - end of loading game to Wendigo fight")

def loadRescue():
    FFX_memory.awaitControl()
    FFXC.set_movement(1, -1)
    FFX_memory.waitFrames(30 * 0.7)
    FFXC.set_movement(0, -1)
    while FFX_memory.userControl():
        doNothing = True
    FFXC.set_neutral()
    FFX_memory.waitFrames(30 * 1)
    FFX_memory.awaitControl()
    FFX_memory.fullPartyFormat('evrae')
    #FFX_menu.weddingPrep()
    
    FFX_zzairShipPath.airShipPath(1) #The run from cockpit to the deck

def loadBahamut():
    loadOffset(1)
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    FFX_memory.waitFrames(30 * 0.2)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.waitFrames(30 * 2)
    FFXC.set_value('AxisLy', 0)
    
def loadCalm():
    FFXC.set_movement(1, 1)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 2)
    FFXC.set_neutral()
    FFX_memory.awaitControl()
    
def loadGagaGates():
    FFXC.set_movement(1, 1)
    FFX_memory.waitFrames(30 * 3)
    FFXC.set_movement(0, 1)
    FFX_memory.awaitEvent()
    FFXC.set_neutral()

def zanEntrance():
    FFXC.set_value('AxisLy', 1)
    FFX_memory.waitFrames(30 * 2)
    FFXC.set_value('AxisLx', -1)
    FFX_memory.waitFrames(30 * 2.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)

def zanTrials():
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    FFX_memory.waitFrames(30 * 0.5)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.waitFrames(30 * 2)
    FFXC.set_value('AxisLy', 0)

def loadGagazetDream():
    FFXC.set_movement(1, 1)
    FFX_memory.waitFrames(30 * 2)
    FFXC.set_neutral()
    FFX_memory.awaitControl()

def loadEggHunt():
    FFXC.set_movement(1, 1)
    FFX_memory.waitFrames(30 * 2)
    FFXC.set_movement(0, 1)
    while FFX_memory.getMap() == 327:
        keepMoving = True
    FFXC.set_neutral()
    FFX_memory.waitFrames(30 * 1)
