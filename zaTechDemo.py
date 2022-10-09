import time
import memory.main
import xbox
import logs
import loadGame
import screen
import reset

import area.dreamZan
import area.miihen
import area.MRR
import area.guadosalam
import area.mTemple
import Showcase.chocoEater
import vars
gameVars = vars.varsHandle()

# Plug in controller
FFXC = xbox.controllerHandle()

print("Test 2")
print(FFXC)

print("Starting tech-demo program.")

memory.main.start()
startTime = logs.timeStamp()
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
    area.dreamZan.NewGame('techdemo')

    print("Game start screen")
    screen.clearMouse(0)

    # Now to run the appropriate section depending on attempt number.
    if attempts == 1:
        print("Demo - Mi'ihen skip")
        loadGame.loadSaveNum(26)  # W/O laughing scene
        loadGame.LoadMiihenStart()
        FFXC.set_neutral()
        memory.main.setEncounterRate(0)
        memory.main.awaitControl()
        returnVal = area.miihen.arrival()
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
        loadGame.loadSaveNum(38)
        # Fixes a low gil state for this save file.
        memory.main.setGilvalue(4000)
        loadGame.LoadMRR()
        wakkaLateMenu = area.MRR.arrival()
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
        loadGame.loadSaveNum(3)
        loadGame.loadGuadoSkip()
        SkipAttempts += 1
        guadoSkipStatus = area.guadosalam.guadoSkip()
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
        loadGame.loadSaveNum(97)
        loadGame.loadMacTemple()
        SkipAttempts += 1
        jyscalSkipStatus = area.mTemple.arrival(doGrid=False)
        if jyscalSkipStatus:
            SkipCount += 1
        print("------------------------------")
        print("------------------------------")
        print("Attempts:", SkipAttempts)
        print("Success:", SkipCount)
        print("------------------------------")
        print("------------------------------")
    elif attempts == 5:
        print("###  Just for fun - Chocobo Eater Stomp")
        print("###  Please engage the CSR now!")
        loadGame.loadSaveNum(28)
        Showcase.chocoEater.engage()
        Showcase.chocoEater.battle()
    else:  # Breaks the loop when everything is complete.
        attempts = 100

    # Clean-up for next round, or process termination.
    FFXC.set_neutral()
    if attempts < 100:
        print("Demo complete. Now clicking to control so we can reset.", attempts)
        if memory.main.getStoryProgress() < 3380:
            memory.main.clickToControl()
            time.sleep(2)
        else:
            time.sleep(10)

        print("Resetting.")

        reset.resetToMainMenu()
    else:
        print("------------------------------")
        print("------------------------------")
        print("Final demo is complete. Thanks for playing.")


endTime = logs.timeStamp()
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
memory.main.end()
print("--------------------------")
print("Program - end")
print("--------------------------")
