import pyxinput
import pyautogui
import time
import FFX_Xbox
import FFX_Screen
import FFX_memory

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

def resetToMainMenu():
    if FFX_memory.battleActive():
        print("Battle is active. Forcing battle to end so we can soft reset.")
        FFX_memory.resetBattleEnd()
        FFX_memory.clickToControl()
    print("Resetting - 2 seconds")
    time.sleep(2)
    while not FFX_memory.getMap() in [23,348,349]:
        FFX_memory.setMapReset()
        time.sleep(0.1)
        FFX_memory.forceMapLoad()
        time.sleep(2)
