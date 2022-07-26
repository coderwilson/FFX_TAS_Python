import pyxinput
import time
import FFX_memory
import FFX_Xbox
import FFX_DreamZan
import FFX_Battle
import FFX_Screen
import FFX_core
import FFX_Reset
import FFX_LoadGame
#import FFX_Logs
FFXC = FFX_Xbox.controllerHandle()

#FFXC = FFX_Xbox.FFXC

FFX_memory.start()

#miihenSkipCount = 0
#miihenSkipAttempts = 0
#rngSeedNum = 6

attempts = 0
success = 0
rngRootArray = [0] * 200
rngSuccessArray = [0] * 21
rngMod2Array = [0] * 200
rngMod3Array = [0] * 200
rngMod4Array = [0] * 200
rngMod5Array = [0] * 200
rngMod6Array = [0] * 200
rngMod7Array = [0] * 200
rngMod8Array = [0] * 200
rngMod9Array = [0] * 200
rngMod10Array = [0] * 200
rngMod11Array = [0] * 200
rngMod12Array = [0] * 200
rngMod13Array = [0] * 200
rngMod14Array = [0] * 200
rngMod15Array = [0] * 200
rngMod16Array = [0] * 200
rngMod17Array = [0] * 200
rngMod18Array = [0] * 200
rngMod19Array = [0] * 200
rngMod20Array = [0] * 200
import FFX_Luca
import FFX_Blitz

while attempts < 20:
    FFX_DreamZan.NewGame("BlitzballTesting")
    FFX_LoadGame.loadSaveNum(37)
    FFX_memory.resetBattleEnd()
    rngRootArray[attempts] = FFX_memory.rng02()
    offset = 1
    blitzoffWin = False
    
    #print("Game start screen")
    FFX_Screen.clearMouse(0)
    
    #startTime = FFX_Logs.timeStamp()
    #print("Timer starts now.")
    #---------This is the actual movement/code/logic/etc---------------
    
    rolledArray = FFX_memory.rng02Array()
    
    FFX_Luca.blitzStart()
    while not FFX_memory.blitzClock() in [1,2]:
        FFXC.set_neutral()
    while not (FFX_Blitz.selectFormation() or FFX_Blitz.selectMovement()):
        #if FFX_Blitz.selectBreakthrough():
        #    FFX_Xbox.tapA()
        #    FFX_Xbox.tapA()
        #    FFX_Xbox.tapB()
        #elif FFX_Blitz.selectAction():
        #    FFX_Xbox.tapB()
        #else:
        FFX_Xbox.tapY()
    
    FFXC.set_neutral()
    if FFX_Blitz.selectMovement():
        blitzoffWin = True
    else:
        blitzoffWin = False
    
    rngMod2Array[attempts] = rolledArray[offset] % 2
    rngMod3Array[attempts] = rolledArray[offset] % 3
    rngMod4Array[attempts] = rolledArray[offset] % 4
    rngMod5Array[attempts] = rolledArray[offset] % 5
    rngMod6Array[attempts] = rolledArray[offset] % 6
    rngMod7Array[attempts] = rolledArray[offset] % 7
    rngMod8Array[attempts] = rolledArray[offset] % 8
    rngMod9Array[attempts] = rolledArray[offset] % 9
    rngMod10Array[attempts] = rolledArray[offset] % 10
    rngMod11Array[attempts] = rolledArray[offset] % 11
    rngMod12Array[attempts] = rolledArray[offset] % 12
    rngMod13Array[attempts] = rolledArray[offset] % 13
    rngMod14Array[attempts] = rolledArray[offset] % 14
    rngMod15Array[attempts] = rolledArray[offset] % 15
    rngMod16Array[attempts] = rolledArray[offset] % 16
    rngMod17Array[attempts] = rolledArray[offset] % 17
    rngMod18Array[attempts] = rolledArray[offset] % 18
    rngMod19Array[attempts] = rolledArray[offset] % 19
    rngMod20Array[attempts] = rolledArray[offset] % 20
    
    if blitzoffWin and rngMod2Array[attempts]:
        rngSuccessArray[2] += 1
    elif not blitzoffWin and not rngMod2Array[attempts]:
        rngSuccessArray[2] += 1
    if blitzoffWin and rngMod3Array[attempts]:
        rngSuccessArray[3] += 1
    elif not blitzoffWin and not rngMod3Array[attempts]:
        rngSuccessArray[3] += 1
    if blitzoffWin and rngMod4Array[attempts]:
        rngSuccessArray[4] += 1
    elif not blitzoffWin and not rngMod4Array[attempts]:
        rngSuccessArray[4] += 1
    if blitzoffWin and rngMod5Array[attempts]:
        rngSuccessArray[5] += 1
    elif not blitzoffWin and not rngMod5Array[attempts]:
        rngSuccessArray[5] += 1
    if blitzoffWin and rngMod6Array[attempts]:
        rngSuccessArray[6] += 1
    elif not blitzoffWin and not rngMod6Array[attempts]:
        rngSuccessArray[6] += 1
    if blitzoffWin and rngMod7Array[attempts]:
        rngSuccessArray[7] += 1
    elif not blitzoffWin and not rngMod7Array[attempts]:
        rngSuccessArray[7] += 1
    if blitzoffWin and rngMod8Array[attempts]:
        rngSuccessArray[8] += 1
    elif not blitzoffWin and not rngMod8Array[attempts]:
        rngSuccessArray[8] += 1
    if blitzoffWin and rngMod9Array[attempts]:
        rngSuccessArray[9] += 1
    elif not blitzoffWin and not rngMod9Array[attempts]:
        rngSuccessArray[9] += 1
    if blitzoffWin and rngMod10Array[attempts]:
        rngSuccessArray[10] += 1
    elif not blitzoffWin and not rngMod10Array[attempts]:
        rngSuccessArray[10] += 1
    if blitzoffWin and rngMod11Array[attempts]:
        rngSuccessArray[11] += 1
    elif not blitzoffWin and not rngMod11Array[attempts]:
        rngSuccessArray[11] += 1
    if blitzoffWin and rngMod12Array[attempts]:
        rngSuccessArray[12] += 1
    elif not blitzoffWin and not rngMod12Array[attempts]:
        rngSuccessArray[12] += 1
    if blitzoffWin and rngMod13Array[attempts]:
        rngSuccessArray[13] += 1
    elif not blitzoffWin and not rngMod13Array[attempts]:
        rngSuccessArray[13] += 1
    if blitzoffWin and rngMod14Array[attempts]:
        rngSuccessArray[14] += 1
    elif not blitzoffWin and not rngMod14Array[attempts]:
        rngSuccessArray[14] += 1
    if blitzoffWin and rngMod15Array[attempts]:
        rngSuccessArray[15] += 1
    elif not blitzoffWin and not rngMod15Array[attempts]:
        rngSuccessArray[15] += 1
    if blitzoffWin and rngMod16Array[attempts]:
        rngSuccessArray[16] += 1
    elif not blitzoffWin and not rngMod16Array[attempts]:
        rngSuccessArray[16] += 1
    if blitzoffWin and rngMod17Array[attempts]:
        rngSuccessArray[17] += 1
    elif not blitzoffWin and not rngMod17Array[attempts]:
        rngSuccessArray[17] += 1
    if blitzoffWin and rngMod18Array[attempts]:
        rngSuccessArray[18] += 1
    elif not blitzoffWin and not rngMod18Array[attempts]:
        rngSuccessArray[18] += 1
    if blitzoffWin and rngMod19Array[attempts]:
        rngSuccessArray[19] += 1
    elif not blitzoffWin and not rngMod19Array[attempts]:
        rngSuccessArray[19] += 1
    if blitzoffWin and rngMod20Array[attempts]:
        rngSuccessArray[20] += 1
    elif not blitzoffWin and not rngMod20Array[attempts]:
        rngSuccessArray[20] += 1
    
    attempts += 1
    print("------------------------------")
    print("------------------------------")
    print("Attempts: ", attempts)
    print("Success: ", success)
    print("All attempts results:")
    print(rngSuccessArray)
    print("------------------------------")
    print("------------------------------")
    time.sleep(5)
    if blitzoffWin == True:
        success += 1
    
    #attempts = 100
    
    #---------End of the actual movement/code/logic/etc---------------
    #endTime = FFX_Logs.timeStamp()
    #print("Duration: ", endTime - startTime)
    
    if attempts < 20:
        #print("Clicking to control so we can reset. ", attempts)
        #FFXC.set_neutral()
        #FFX_memory.clickToControl()
        #print(" ")
        #print("---------------------------------------------------")
        #print("---------------------------------------------------")
        #print("Test number ", attempts, "is complete.")
        #print("Blitzball wins: ", success)
        #print("---------------------------------------------------")
        #print("---------------------------------------------------")
        #time.sleep(5)
        
        print("Resetting.")
        #FFX_memory.end()
        
        FFX_memory.resetBlitzMenuNum()
        FFX_Reset.resetToMainMenu()
    else:
        print("Final Results:")
        print("------------------------------")
        print("------------------------------")
        print("Attempts: ", attempts)
        print("Success: ", success)
        print("All attempts results:")
        print(rngSuccessArray)
        print("------------------------------")
        print("------------------------------")
    
    #rngSeedNum += 1

time.sleep(5)

#print("Skip attempts: ", miihenSkipAttempts)
#print("Successful skips: ", miihenSkipCount)
FFX_memory.end()

time.sleep(5)
print("--------------------------")
print("Program - end")
print("--------------------------")