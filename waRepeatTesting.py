import pyxinput
import time
import FFX_Xbox
import FFX_DreamZan
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

FFX_memory.start()

#miihenSkipCount = 0
#miihenSkipAttempts = 0
#rngSeedNum = 6

attempts = 0
success = 0
while attempts < 20:
    #print("RNG seed for this attempt: ", rngSeed)
    attempts += 1
    
    FFX_DreamZan.NewGame('Luca')
    FFX_LoadGame.loadOffset(1)
    
    print("Game start screen")
    FFX_Screen.clearMouse(0)
    
    startTime = FFX_Logs.timeStamp()
    print("Timer starts now.")
    #---------This is the actual movement/code/logic/etc---------------
    import FFX_Luca
    import FFX_Blitz
    
    FFX_Luca.blitzStart()
    blitzWin = FFX_Blitz.blitzMain(False)
    if blitzWin == True:
        success += 1
    
    #attempts = 100
    
    #---------End of the actual movement/code/logic/etc---------------
    endTime = FFX_Logs.timeStamp()
    print("Duration: ", endTime - startTime)
    
    if attempts < 20:
        #print("Clicking to control so we can reset. ", attempts)
        #FFXC.set_neutral()
        #FFX_memory.clickToControl()
        print(" ")
        print("---------------------------------------------------")
        print("---------------------------------------------------")
        print("Test number ", attempts, "is complete.")
        print("Blitzball wins: ", success)
        print("---------------------------------------------------")
        print("---------------------------------------------------")
        time.sleep(5)
        
        print("Resetting.")
        #FFX_memory.end()

        FFX_Reset.resetToMainMenu()
    else:
        print(" ")
        print("---------------------------------------------------")
        print("---------------------------------------------------")
        print("Testing is complete.")
        print("Attempts: ", attempts)
        print("Success count: ", success)
        print("---------------------------------------------------")
        print("---------------------------------------------------")
    
    #rngSeedNum += 1

time.sleep(5)

#print("Skip attempts: ", miihenSkipAttempts)
#print("Successful skips: ", miihenSkipCount)
FFX_memory.end()

time.sleep(5)
print("--------------------------")
print("Program - end")
print("--------------------------")