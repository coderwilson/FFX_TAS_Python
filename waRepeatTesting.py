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

global FFXC
#FFXC = FFX_Xbox.FFXC

selfAuto = True
print("Looping section over RNG seeds")
while not FFX_Screen.PixelTest(1076,552,(157, 159, 157)):
    FFXC.set_value('BtnStart', 1)
    time.sleep(0.1)
    FFXC.set_value('BtnStart', 0)
    time.sleep(0.3)

FFX_memory.start()
miihenSkipCount = 0
miihenSkipAttempts = 0
rngSeedNum = 6

attempts = 0
success = 0
while attempts < 20:
    print("RNG seed for this attempt: ", rngSeed)
    attempts += 1
    
    print("Waiting to initialize - waiting on New Game screen")
    #---------- MAKE SURE THIS IS ON FOR A FRESH RUN --------------------
    while not FFX_Screen.PixelTest(1076,552,(157, 159, 157)):
        FFXC.set_value('BtnStart', 1)
        time.sleep(0.1)
        FFXC.set_value('BtnStart', 0)
        time.sleep(0.3)

    print("Game start screen")
    FFX_Screen.clearMouse(0)
    
    startTime = FFX_Logs.timeStamp()
    print("Timer starts now.")
    #---------This is the actual movement/code/logic/etc---------------
    import FFX_MRR
    FFX_LoadGame.loadOffset(18)
    FFX_LoadGame.LoadMRR()
    
    retArray = FFX_MRR.arrival()
    if retArray[1] == True:
        success += 1
    FFX_MRR.mainPath(retArray[0])
    #---------End of the actual movement/code/logic/etc---------------
    endTime = FFX_Logs.timeStamp()
    
    if attempts < 20:
        print("Demo complete. Now clicking to control so we can reset. ", attempts)
        FFXC.set_neutral()
        FFX_memory.clickToControl()
        time.sleep(2)
        
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
        print("Success count: " success)
    
    #rngSeedNum += 1

time.sleep(5)

#print("Skip attempts: ", miihenSkipAttempts)
#print("Successful skips: ", miihenSkipCount)
FFX_memory.end()
#print("--------------------------")
#print("Questing for Glory: Hope & Healing II")
#print("--------------------------")
#time.sleep(2)
#print("Thank you to the event organizers, planning staff, and volunteers that made this possible.")
#print("--------------------------")
#time.sleep(2)
#print("For this FFX project, thank you also to")
#print("these individuals:")
#time.sleep(1.5)
#print("-Blueaurora - my wife - for putting up with")
#print("me for literal years")
#time.sleep(1.5)
#print("-My wife is the best!")
#time.sleep(1.5)
#print("--------------------------")
#time.sleep(1.5)
#print("-DwangoAC and the TASbot community")
#time.sleep(1.5)
#print("-Inverted from the TASbot community")
#time.sleep(1.5)
#print("-TheAxeMan from the TASbot community")
#time.sleep(1.5)
#print("-Rossy__ from the FFX Speed-running community")
#time.sleep(1.5)
#print("-CrimsonInferno from the FFX Speed-running community")
#print("(current WR holder, multiple categories) ")
#time.sleep(1.5)
#print("-Highspirits from QfG staff, amazing work on the event!")
#time.sleep(1.5)
#print("-And countless other people who have supported me along")
#print("the way on this project.")
#time.sleep(1.5)
#print("-May the rest of QfG:HH2 be a major success!")

time.sleep(5)
print("--------------------------")
print("Program - end")
print("--------------------------")