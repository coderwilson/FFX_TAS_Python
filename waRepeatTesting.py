import pyxinput
import time
import FFX_Xbox
import FFX_Battle
import FFX_Screen
import FFX_core
import FFX_memory
import FFX_Reset
import FFX_LoadGame
import FFX_Logs

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

selfAuto = True
print("Looping section: Bevelle Trials")
while not FFX_Screen.PixelTest(1076,552,(157, 159, 157)):
    FFXC.set_value('BtnStart', 1)
    FFX_memory.waitFrames(30 * 0.1)
    FFXC.set_value('BtnStart', 0)
    FFX_memory.waitFrames(30 * 0.3)

FFX_memory.start()
#miihenSkipCount = 0
#miihenSkipAttempts = 0
#rngSeedNum = 6

attempts = 0
success = 0
while attempts < 20:
    #print("RNG seed for this attempt: ", rngSeed)
    attempts += 1
    
    print("Waiting to initialize - waiting on New Game screen")
    #---------- MAKE SURE THIS IS ON FOR A FRESH RUN --------------------
    while not FFX_Screen.PixelTest(1076,552,(157, 159, 157)):
        FFXC.set_value('BtnStart', 1)
        FFX_memory.waitFrames(30 * 0.1)
        FFXC.set_value('BtnStart', 0)
        FFX_memory.waitFrames(30 * 0.3)

    print("Game start screen")
    FFX_Screen.clearMouse(0)
    
    startTime = FFX_Logs.timeStamp()
    print("Timer starts now.")
    #---------This is the actual movement/code/logic/etc---------------
    import FFX_rescueYuna
    FFX_LoadGame.loadOffset(42)
    
    FFX_rescueYuna.trials()
    #attempts = 100
    
    #---------End of the actual movement/code/logic/etc---------------
    endTime = FFX_Logs.timeStamp()
    print("Duration: ", endTime - startTime)
    
    if attempts < 20:
        print("Clicking to control so we can reset. ", attempts)
        FFXC.set_neutral()
        FFX_memory.clickToControl()
        FFX_memory.waitFrames(30 * 2)
        
        print("Resetting.")
        #FFX_memory.end()

        FFX_Reset.resetToMainMenu()
    else:
        print(" ")
        print("---------------------------------------------------")
        print("---------------------------------------------------")
        print("Testing is complete.")
        print("---------------------------------------------------")
        print("Attempts: ", attempts)
        print("Success count: ", success)
    
    #rngSeedNum += 1

FFX_memory.waitFrames(30 * 5)

#print("Skip attempts: ", miihenSkipAttempts)
#print("Successful skips: ", miihenSkipCount)
FFX_memory.end()

FFX_memory.waitFrames(30 * 5)
print("--------------------------")
print("Program - end")
print("--------------------------")