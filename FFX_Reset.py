import pyxinput
import pyautogui
import time
import FFX_Xbox
import FFX_Screen
import FFX_memory

FFXC = FFX_Xbox.FFXC

def allButtons():
    FFXC.set_value('BtnShoulderL', 1)
    FFXC.set_value('BtnShoulderR', 1)
    FFXC.set_value('TriggerL', 1)
    FFXC.set_value('TriggerR', 1)
    FFXC.set_value('BtnStart', 1)
    FFXC.set_value('BtnBack', 1)

def noButtons():
    FFXC.set_value('BtnBack', 0)
    FFXC.set_value('BtnStart', 0)
    FFXC.set_value('BtnShoulderL', 0)
    FFXC.set_value('BtnShoulderR', 0)
    FFXC.set_value('TriggerL', 0)
    FFXC.set_value('TriggerR', 0)
    if FFX_memory.menuOpen():
        FFX_memory.closeMenu()

def resetToMainMenu(mapValue):
    #Soft reset method
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    while FFX_memory.getMap() == mapValue:
        if FFX_memory.menuOpen():
            FFX_Xbox.menuA()
        elif FFX_memory.battleScreen():
            import FFX_Battle
            FFX_Battle.fleeAll()
        else:
            allButtons()
            time.sleep(0.2)
            noButtons()
            time.sleep(0.2)
            FFX_Xbox.menuB()
    time.sleep(4)
    FFX_memory.gameOverReset()
    FFX_Xbox.SkipDialog(4)

def resetToMainMenu_hardReset():
    #Hard reset method
    try:
        pyautogui.click(10,10)
        time.sleep(2)
        
        print("Attempting force quit (alt-F4 method)")
        with pyautogui.hold('alt'):
            pyautogui.press('f4')
        time.sleep(3)
        print("Did it work?")
        if FFX_Screen.imgSearch2('img/quit_game_OK.JPG', 0.85):
            print("Found image")
            pyautogui.click(793,511)
            print("Game quit command complete.")
        
        time.sleep(5)
        print("Now attempting to re-launch.")
        pyautogui.click(415,230)
    except Exception as errMsg:
        print("Not able to reset. Trying again.")
        print("Error: ", errMsg)
        time.sleep(5)
        resetToMainMenu()