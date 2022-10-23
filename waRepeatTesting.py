import time

import area.dreamZan
import loadGame
import logs
import memory.main
import reset
import screen
import xbox

FFXC = xbox.controller_handle()

selfAuto = True
print("Looping section: Bevelle Trials")

memory.main.start()

attempts = 0
success = 0
while attempts < 20:
    attempts += 1

    area.dreamZan.new_game("Luca")
    loadGame.load_offset(1)

    print("Game start screen")
    screen.clear_mouse(0)

    startTime = logs.time_stamp()
    print("Timer starts now.")
    # ---------This is the actual movement/code/logic/etc---------------
    import area.luca as luca
    import blitz

    luca.blitz_start()
    blitzWin = blitz.blitz_main(False)
    if blitzWin:
        success += 1

    # ---------End of the actual movement/code/logic/etc---------------
    endTime = logs.time_stamp()
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

        reset.reset_to_main_menu()
    else:
        print("------------------------------")
        print("------------------------------")
        print("Testing is complete.")
        print("Attempts:", attempts)
        print("Success count:", success)
        print("------------------------------")
        print("------------------------------")

time.sleep(5)

memory.main.end()

time.sleep(5)
print("--------------------------")
print("Program - end")
print("--------------------------")
