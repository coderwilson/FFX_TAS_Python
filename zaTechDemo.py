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

FFXC = FFX_Xbox.FFXC

selfAuto = True
print("Starting tech-demo program.")

while not FFX_Screen.PixelTest(1076,552,(157, 159, 157)):
    FFXC.set_value('BtnStart', 1)
    time.sleep(0.1)
    FFXC.set_value('BtnStart', 0)
    time.sleep(0.3)

FFX_memory.start()
startTime = FFX_Logs.timeStamp()
print("Timer starts now.")
miihenSkipCount = 0
miihenSkipAttempts = 0

attempts = 0
while attempts < 100:
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
    
    #Now to run the appropriate section depending on attempt number.
    if attempts == 1 and miihenSkipCount == 0:
        print("Demo - Mi'ihen skip")
        FFX_LoadGame.loadOffset(20)
        FFX_LoadGame.LoadMiihenStart()
        import FFX_Miihen
        returnVal = FFX_Miihen.arrival()
        miihenSkipAttempts += 1
        if returnVal[1] == True:
            miihenSkipCount += 1
        print("-----------------------------------------------------")
        print("-----------------------------------------------------")
        print("Attempts: ", miihenSkipAttempts)
        print("Success: ", miihenSkipCount)
        print("-----------------------------------------------------")
        print("-----------------------------------------------------")
    elif attempts == 2:
        print("Demo - MRR skip")
        FFX_LoadGame.loadOffset(18)
        FFX_LoadGame.LoadMRR()
        import FFX_MRR
        FFX_MRR.arrival()
    elif attempts == 3:
        print("Demo - Guado skip")
        FFX_LoadGame.loadOffset(3)
        FFX_LoadGame.loadGuadoSkip()
        import FFX_Guadosalam
        FFX_Guadosalam.guadoSkip()
    elif attempts == 4:
        print("Demo - Jyscal skip")
        FFX_LoadGame.loadOffset(23)
        FFX_LoadGame.loadMacTemple()
        import FFX_mTemple
        FFX_mTemple.arrival(True)
        #FFX_mTemple.seymourFight()
    elif attempts == 5:
        print("Demo - Zanarkand path and trials.")
        FFX_LoadGame.loadOffset(22)
        FFX_LoadGame.zanEntrance()
        import FFX_Zanarkand
        FFX_Zanarkand.arrival()
        FFX_Zanarkand.trials()
        endGameVersion = 4
        # 4 == four Return spheres
        # 3 == four Friend spheres
        # 1 or 2 == two of each.
        FFX_Zanarkand.sanctuaryKeeper(endGameVersion)
    elif attempts == 6:
        print("Demo - Egg Hunt")
        FFX_LoadGame.loadOffset(2)

        FFXC.set_value('AxisLy',1)
        FFXC.set_value('AxisLx',1)
        time.sleep(0.7)
        FFXC.set_value('AxisLx',0)
        time.sleep(34)
        FFXC.set_value('AxisLy',0)

        print("Start egg hunt only program")
        print("--------------------------No-control method")

        import zz_eggHuntAuto
        import FFX_menu
        zz_eggHuntAuto.engage()
        
    #elif attempts < 30: #Testing loop
    #    FFX_LoadGame.loadOffset(15)
    #    import FFX_home
    #    FFX_home.desert()
    else: #Breaks the loop when everything is complete.
        attempts = 100
    if attempts < 100:
        print("Demo complete. Now clicking to control so we can reset. ", attempts)
        FFXC.set_value('AxisLx', 0)
        FFXC.set_value('AxisLy', 0)
        FFX_memory.clickToControl()
        time.sleep(2)
        
        print("Resetting.")
        #FFX_memory.end()

        FFX_Reset.resetToMainMenu(FFX_memory.getMap())
    else:
        print(" ")
        print("---------------------------------------------------")
        print("---------------------------------------------------")
        print("Final demo is complete. Thanks for playing.")

endTime = FFX_Logs.timeStamp()

totalTime = endTime - startTime
print("The game duration (real time) was: ", str(totalTime))
print("---------------------------------------------------")
print("---------------------------------------------------")
time.sleep(5)

#print("Skip attempts: ", miihenSkipAttempts)
#print("Successful skips: ", miihenSkipCount)
FFX_memory.end()
print("Thank you Questing for Glory event, and all the people that made this possible!")
time.sleep(5)
print("Program - end")