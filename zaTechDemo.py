import time
import FFX_memory
import FFX_Xbox
import FFX_Logs
import FFX_LoadGame
import FFX_Screen
import FFX_Reset

import FFX_DreamZan
import FFX_Miihen
import FFX_MRR
import FFX_Guadosalam
import FFX_mTemple
import FFX_vars
gameVars = FFX_vars.varsHandle()

# Plug in controller
FFXC = FFX_Xbox.controllerHandle()

print("Test 2")
print(FFXC)

print("Starting tech-demo program.")

FFX_memory.start()
startTime = FFX_Logs.timeStamp()
print("Timer starts now.")
SkipCount = 0
SkipAttempts = 0
gameVars.setCSR(False)

attempts = 0  # Determines where in the showcase we start
cycles = 0
jyscalRetry = False
while attempts < 20 and cycles < 50:
    attempts += 1
    cycles += 1
    print("Cycle number:", cycles)
    print(FFXC)
    print("Waiting to initialize - waiting on New Game screen")
    # ---------- MAKE SURE THIS IS ON FOR A FRESH RUN --------------------
    FFX_DreamZan.NewGame('techdemo')

    print("Game start screen")
    FFX_Screen.clearMouse(0)

    # Now to run the appropriate section depending on attempt number.
    if attempts == 1:
        print("Demo - Mi'ihen skip")
        FFX_LoadGame.loadSaveNum(26)  # W/O laughing scene
        FFX_LoadGame.LoadMiihenStart()
        FFXC.set_neutral()
        FFX_memory.setEncounterRate(0)
        FFX_memory.awaitControl()
        returnVal = FFX_Miihen.arrival()
        print(returnVal)
        SkipAttempts += 1
        if returnVal[3]:
            SkipCount += 1
        print("------------------------------")
        print("------------------------------")
        print("Attempts:", SkipAttempts)
        print("Success:", SkipCount)
        print("------------------------------")
        print("------------------------------")
    elif attempts == 2:
        print("Demo - MRR skip")
        FFX_LoadGame.loadSaveNum(38)
        # Fixes a low gil state for this save file.
        FFX_memory.setGilvalue(4000)
        FFX_LoadGame.LoadMRR()
        wakkaLateMenu = FFX_MRR.arrival()
        SkipCount += 1
        SkipAttempts += 1
        print("------------------------------")
        print("------------------------------")
        print("Attempts:", SkipAttempts)
        print("Success:", SkipCount)
        print("------------------------------")
        print("------------------------------")
    elif attempts == 3:
        print("Demo - Guado skip")
        FFX_LoadGame.loadSaveNum(3)
        FFX_LoadGame.loadGuadoSkip()
        SkipAttempts += 1
        guadoSkipStatus = FFX_Guadosalam.guadoSkip()
        if guadoSkipStatus:
            SkipCount += 1
        print("------------------------------")
        print("------------------------------")
        print("Attempts:", SkipAttempts)
        print("Success:", SkipCount)
        print("------------------------------")
        print("------------------------------")
    elif attempts == 4:
        print("Demo - Jyscal skip")
        # No remedy in inventory, likely game over.
        FFX_LoadGame.loadSaveNum(97)
        FFX_LoadGame.loadMacTemple()
        SkipAttempts += 1
        jyscalSkipStatus = FFX_mTemple.arrival(doGrid=False)
        if jyscalSkipStatus:
            SkipCount += 1
        print("------------------------------")
        print("------------------------------")
        print("Attempts:", SkipAttempts)
        print("Success:", SkipCount)
        print("------------------------------")
        print("------------------------------")
    else:  # Breaks the loop when everything is complete.
        attempts = 100

    # Clean-up for next round, or process termination.
    FFXC.set_neutral()
    if attempts < 100:
        print("Demo complete. Now clicking to control so we can reset.", attempts)
        if FFX_memory.getStoryProgress() < 3380:
            FFX_memory.clickToControl()
            time.sleep(2)
        else:
            time.sleep(10)

        print("Resetting.")

        FFX_Reset.resetToMainMenu()
    else:
        print(" ")
        print("------------------------------")
        print("------------------------------")
        print("Final demo is complete. Thanks for playing.")


endTime = FFX_Logs.timeStamp()
print("------------------------------")
print("------------------------------")
totalTime = endTime - startTime
print("The program duration (real time) was:", str(totalTime))
print("------------------------------")
print("------------------------------")

# print("--------TASgiving, please stop the timer-------------")
# print("--------------------------")
# print("Questing for Glory: Hope & Healing II")
# print("--------------------------")
# time.sleep(2)
# print("Thank you to the event organizers, planning staff, and volunteers that made this possible.")
# print("--------------------------")
# time.sleep(2)
# print("For this FFX project, thank you also to")
# print("these individuals:")
# time.sleep(1.5)
# print("-Blueaurora - my wife - for putting up with")
# print("me for literal years")
# time.sleep(1.5)
# print("-My wife is the best!")
# time.sleep(1.5)
# print("--------------------------")
# time.sleep(1.5)
# print("-DwangoAC and the TASbot community")
# time.sleep(1.5)
# print("-Inverted from the TASbot community")
# time.sleep(1.5)
# print("-TheAxeMan from the TASbot community")
# time.sleep(1.5)
# print("-Rossy__ from the FFX Speed-running community")
# time.sleep(1.5)
# print("-CrimsonInferno from the FFX Speed-running community")
# print("(current WR holder, multiple categories)")
# time.sleep(1.5)
# print("-Highspirits from QfG staff, amazing work on the event!")
# time.sleep(1.5)
# print("-And countless other people who have supported me along")
# print("the way on this project.")
# time.sleep(1.5)
# print("-May the rest of QfG:HH2 be a major success!")

time.sleep(5)
FFX_memory.end()
print("--------------------------")
print("Program - end")
print("--------------------------")
