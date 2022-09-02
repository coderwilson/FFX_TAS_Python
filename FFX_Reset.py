import FFX_Xbox
import FFX_Screen
import FFX_memory

FFXC = FFX_Xbox.controllerHandle()


def resetToMainMenu():
    FFXC.set_neutral()
    if FFX_memory.getStoryProgress() <= 8:
        FFX_memory.waitFrames(30 * 0.07)
        while not FFX_memory.getMap() in [23, 348, 349]:
            print("----------Attempting reset")
            print("FFX map:", FFX_memory.getMap())
            print("----------")
            FFX_memory.setMapReset()
            FFX_memory.waitFrames(30 * 0.1)
            FFX_memory.forceMapLoad()
            FFX_memory.waitFrames(30 * 1)
    elif FFX_memory.battleActive():
        print("Battle is active. Forcing battle to end so we can soft reset.")
        FFX_Screen.awaitTurn()
        FFX_memory.resetBattleEnd()
        while not FFX_memory.getMap() in [23, 348, 349]:
            FFX_Xbox.menuB()
    
    else:
        FFX_memory.waitFrames(30 * 0.07)
        while not FFX_memory.getMap() in [23, 348, 349]:
            print("----------Attempting reset")
            print("FFX map:", FFX_memory.getMap())
            print("----------")
            FFX_memory.setMapReset()
            FFX_memory.waitFrames(30 * 0.1)
            FFX_memory.forceMapLoad()
            FFX_memory.waitFrames(30 * 1)
    print("Resetting")
