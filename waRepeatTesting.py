import time
import xbox
import area.dreamZan as dreamZan
import screen
import memory
import reset
import loadGame
import logs

FFXC = xbox.controllerHandle()

selfAuto = True
print("Looping section: Bevelle Trials")

memory.start()

attempts = 0
success = 0
while attempts < 20:
    attempts += 1

    dreamZan.NewGame('Luca')
    loadGame.loadOffset(1)

    print("Game start screen")
    screen.clearMouse(0)

    startTime = logs.timeStamp()
    print("Timer starts now.")
    # ---------This is the actual movement/code/logic/etc---------------
    import area.luca as luca
    import blitz

    luca.blitzStart()
    blitzWin = blitz.blitzMain(False)
    if blitzWin:
        success += 1

    # ---------End of the actual movement/code/logic/etc---------------
    endTime = logs.timeStamp()
    print("Duration:", endTime - startTime)

    if attempts < 20:
        print("------------------------------")
        print("------------------------------")
        print("Test number", attempts, "is complete.")
        print("Blitzball wins:", success)
        print("------------------------------")
        print("------------------------------")
        time.sleep(5)

        print("Resetting.")

        reset.resetToMainMenu()
    else:
        print("------------------------------")
        print("------------------------------")
        print("Testing is complete.")
        print("Attempts:", attempts)
        print("Success count:", success)
        print("------------------------------")
        print("------------------------------")

time.sleep(5)

memory.end()

time.sleep(5)
print("--------------------------")
print("Program - end")
print("--------------------------")
