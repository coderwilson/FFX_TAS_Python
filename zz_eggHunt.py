import pyxinput
import time
import FFX_Xbox
import FFX_Battle
import FFX_Screen
import FFX_core
import FFX_memory
import FFX_Reset

FFXC = FFX_Xbox.FFXC

selfAuto = True

attempts = 0
while attempts < 10:
    attempts += 1
    
    if selfAuto == True:
        print("Starting egg-hunt-only program.")
        print("Waiting to initialize - waiting on New Game screen")
        #---------- MAKE SURE THIS IS ON FOR A FRESH RUN --------------------
        while not FFX_Screen.PixelTest(1076,552,(157, 159, 157)):
            FFXC.set_value('BtnStart', 1)
            FFX_memory.waitFrames(30 * 0.1)
            FFXC.set_value('BtnStart', 0)

        print("Game start screen")
        FFX_Screen.clearMouse(0)

        #Initiate memory reading, after we know the game is open.
        FFX_memory.start()

        import FFX_LoadGame
        FFX_LoadGame.loadOffset(37)

        FFXC.set_value('AxisLy',1)
        FFXC.set_value('AxisLx',1)
        FFX_memory.waitFrames(30 * 0.7)
        FFXC.set_value('AxisLx',0)
        FFX_memory.waitFrames(30 * 34)
        FFXC.set_value('AxisLy',0)

        print("Start egg hunt only program")
        print("--------------------------No-control method")

        import zz_eggHuntAuto
        zz_eggHuntAuto.engage()
    else:
        #Initiate memory reading, after we know the game is open.
        print("Start egg hunt only program")
        print("--------------------------No-control method")
        FFX_memory.start()
        import FFX_Logs
        FFX_Logs.nextPlot()
        waitCount = 0
        while FFX_memory.getMap() == 324:
            if FFX_memory.battleActive():
                print("GTFO battle.")
                FFX_Battle.fleeAll()
            elif FFX_memory.menuOpen():
                FFX_Xbox.menuB()
            else:
                waitCount += 1
                if waitCount % 10 == 0:
                    print(waitCount)
                    cam = FFX_memory.getCamera()
                    FFX_Logs.writePlot(str(cam[0]) + "," + str(cam[4]))
                else:
                    FFX_memory.waitFrames(30 * 0.035)
                if waitCount > 10000:
                    break

    print("Allowing time for review.")
    FFX_memory.waitFrames(30 * 35)
    print("Resetting.")
    FFX_memory.end()

    FFX_Reset.resetToMainMenu()