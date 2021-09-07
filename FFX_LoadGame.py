# Libraries and Core Files
import time
import FFX_Xbox
import FFX_Screen
import FFX_memory
import FFX_menu
import pyautogui

#This file is intended to load the game to a saved file.
#This assumes that the save is the first non-auto-save in the list of saves.

FFXC = FFX_Xbox.FFXC

def LoadFirst():
    print("Loading to first save file")
    FFX_Xbox.menuB()
    time.sleep(2.5)
    FFX_Xbox.menuDown()
    time.sleep(0.1)
    FFX_Xbox.menuB()
    time.sleep(0.1)
    FFX_Xbox.menuB()
    FFX_memory.awaitControl()

def loadOffset(offset):
    print("Loading to save file in position ", offset)
    FFX_Xbox.menuB()
    time.sleep(2.5)
    while offset > 0:
        FFX_Xbox.menuDown()
        offset -= 1
    time.sleep(0.1)
    FFX_Xbox.menuB()
    time.sleep(0.1)
    FFX_Xbox.menuB()
    FFX_memory.awaitControl()

def loadOffsetBattle(offset):
    print("Loading to save file in position ", offset)
    FFX_Xbox.menuB()
    time.sleep(2.5)
    while offset > 0:
        FFX_Xbox.menuDown()
        offset -= 1
    time.sleep(0.1)
    FFX_Xbox.menuB()
    time.sleep(0.1)
    FFX_Xbox.menuB()
    time.sleep(3)

def loadPostBlitz():
    print("Loading to first save file")
    loadOffset(1)
    
    while not FFX_Screen.Minimap1():
        if FFX_Screen.Minimap4():
            FFXC.set_value('AxisLx', -1)
            FFXC.set_value('AxisLy', -1)
            time.sleep(0.5)
            FFXC.set_value('AxisLx', 0)
            time.sleep(1)
            FFXC.set_value('AxisLy', 0)
        else:
            FFX_Xbox.menuB()
    
    #Reverse T screen
    FFXC.set_value('AxisLx', 1)
    time.sleep(4.5)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(5)
    FFXC.set_value('AxisLx', 0)
    
    #Carnival vendor screen
    FFX_Screen.awaitMap2()
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    print("Rejoining the party.")
    FFX_Screen.clickToMap1() #Scene, rejoining the party
    print("Walking up to Yuna.")
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0) #Enters laughing scene, ends Luca section.
    print("End of loading section.")

def LoadNeutral():
    LoadFirst()
    
def LoadBaaj():
    loadOffset(1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.4)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.04)

def BesaidTrials() :
    loadOffset(29)
    #Exit Tent
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    time.sleep(4)
    
    #To the temple
    FFXC.set_value('AxisLx', 1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    time.sleep(12)
    FFXC.set_value('AxisLy', 0)

def Boat1() :
    LoadFirst()
    time.sleep(3)
    #To the junction screen, then back.
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(6)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)

def Kilika():
    FFX_Xbox.menuB()
    time.sleep(2.5)
    FFX_Xbox.menuDown()
    time.sleep(0.1)
    FFX_Xbox.menuDown()
    time.sleep(0.1)
    FFX_Xbox.menuDown()
    time.sleep(0.1)
    FFX_Xbox.menuDown()
    time.sleep(0.1)
    FFX_Xbox.menuDown()
    time.sleep(0.1)
    FFX_Xbox.menuDown()
    time.sleep(0.1)
    FFX_Xbox.menuB()
    time.sleep(0.1)
    FFX_Xbox.menuB()
    time.sleep(4)
    FFX_Screen.awaitMap1()

def KilikaTrials():
    loadOffset(26)
    time.sleep(3)
    FFXC.set_value('AxisLy', -1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)

def LoadMiihenStart():
    loadOffset(3)
    time.sleep(1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(5)
    FFXC.set_value('AxisLy', 0)
    
    #Reverse T screen
    FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLx', 1)
    time.sleep(4.5)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    time.sleep(5)
    FFXC.set_value('AxisLx', 0)
    
    #Carnival vendor screen
    FFX_Screen.awaitMap2()
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.clickToMap1()
    #-----Scene, rejoining the party
    #FFXC.set_value('AxisLy', -1)
    #FFXC.set_value('AxisLx', -1)
    #time.sleep(2)
    #FFXC.set_value('AxisLx', 0)
    #FFXC.set_value('AxisLy', 0) #Enters laughing scene, ends Luca section.
    
    #-----Use this if you've already done the laughing scene.
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(5)
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(3)
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', -1)
    time.sleep(4)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(2)
    FFX_memory.awaitEvent()
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.4)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(3)
    #FFXC.set_value('AxisLy', 1)
    #FFXC.set_value('AxisLx', 1)
    #time.sleep(1.5)
    print("Load complete. Now for Mi'ihen area.")

def LoadMRR():
    loadOffset(13)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(2.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(4)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)

def LoadMRR2():
    loadOffset(27)
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.3)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFX_Xbox.SkipDialog(2)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.menuB()
    time.sleep(2)
    FFX_Screen.awaitMap2()
    while not FFX_Screen.Minimap4():
        if FFX_Screen.Minimap2():
            FFXC.set_value('AxisLy', -1)
            FFXC.set_value('AxisLx', -1)
            time.sleep(0.5)
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)

def AfterGui():
    loadOffset(1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    
    #Same pattern as the actual run.
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(6)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.5)
    pos = FFX_memory.getCoords()
    while pos[0] < ((0.05 * pos[1]) + 942.12):
        FFXC.set_value('AxisLx', 1)
        FFXC.set_value('AxisLy', 0)
        pos = FFX_memory.getCoords()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(5.5)
    FFXC.set_value('AxisLy', 0)
    
def djoseTemple():
    loadOffset(19)
    time.sleep(6)
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1.7)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.5)
    
def moonflow2():
    loadOffset(2)
    time.sleep(6)
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.7)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    time.sleep(0.5)

def loadGuadoSkip():
    loadOffset(5)
    time.sleep(1)
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.6)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', -1)
    time.sleep(2)
    FFXC.set_value('AxisLy', -1)
    time.sleep(4)
    FFXC.set_value('AxisLx', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(2)
    FFXC.set_value('AxisLx', 1)
    time.sleep(4.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLy', -1)
    time.sleep(1)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)

def loadMacLake():
    loadOffset(6)
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    FFX_memory.awaitEvent()
    FFXC.set_value('AxisLy', 0)
    FFX_memory.awaitControl()

def loadMacTemple():
    loadOffset(1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLy', 1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    
def loadMacTemple2():
    loadOffset(42)
    FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(1.5)
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.5)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)

def loadWendigo():
    import FFX_Battle
    loadOffset(1)
    FFX_memory.awaitControl()
    while FFX_memory.getBattleNum() < 195:
        if FFX_Screen.BattleScreen():
            FFXC.set_value('AxisLy', 0)
            FFX_Battle.fleeAll()
        elif FFX_memory.userControl():
            FFXC.set_value('AxisLy', -1)
        else:
            FFXC.set_value('AxisLy', 0)
    
    FFX_Battle.wendigo()
    print("Wendigo fight over - end of loading game to Wendigo fight")

def loadRescue():
    LoadFirst()
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.7)
    FFXC.set_value('AxisLx', 0)
    while FFX_memory.userControl():
        print("Just running to the next area.")
    FFXC.set_value('AxisLy', 0)
    time.sleep(1)
    FFX_memory.awaitControl()
    FFX_menu.weddingPrep()
    
    FFX_Xbox.airShipPath(6) #The run from cockpit to the deck

def loadBahamut():
    loadOffset(1)
    FFX_Screen.awaitMap1()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.2)
    FFXC.set_value('AxisLx', 0)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    
def loadCalm():
    loadOffset(1)
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    
def loadGagaGates():
    loadOffset(1)
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(3)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)

def zanEntrance():
    loadOffset(15)
    FFXC.set_value('AxisLy', 1)
    time.sleep(2)
    FFXC.set_value('AxisLx', -1)
    time.sleep(2.5)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)

def zanTrials():
    LoadFirst()
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)

def hymnIsKey_old():
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.SkipDialog(155)
    FFX_Screen.clickToPixel(545,218,(62, 51, 20))
    time.sleep(1)
    FFX_Xbox.menuB() #Skip dialog
    
    while not FFX_Screen.PixelTestTol(610,483,(156, 157, 156),5):
        if FFX_Screen.PixelTestTol(704,466,(154, 154, 154),5):
            FFX_Xbox.menuB()
        if FFX_Screen.PixelTestTol(612,449,(152, 152, 152),5):
            FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #We fight Yu Yevon.

def loadGagazetDream():
    loadOffset(1)
    FFXC.set_value('AxisLy', 1)
    FFXC.set_value('AxisLx', 1)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.awaitControl()
    