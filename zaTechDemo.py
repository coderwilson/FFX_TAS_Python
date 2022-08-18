import time
import FFX_memory
import FFX_Xbox
import FFX_Logs
import FFX_LoadGame
import FFX_Screen
import FFX_Reset
import FFX_Battle

import FFX_DreamZan
import FFX_Miihen
import FFX_MRR
import FFX_Guadosalam
import FFX_mTemple
import FFX_Gagazet
import FFX_home
import FFX_Zanarkand
import FFX_Sin
import FFX_targetPathing
import FFX_vars
gameVars = FFX_vars.varsHandle()

#Plug in controller
FFXC = FFX_Xbox.controllerHandle()

print("Test 2")
print(FFXC)
#FFXC = FFX_Xbox.FFXC

#selfAuto = True
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
        # FFX_LoadGame.loadSaveNum(16) #With laughing scene
        # FFX_LoadGame.LoadMiihenStart_Laugh()
        FFXC.set_neutral()
        FFX_memory.setEncounterRate(0)
        FFX_memory.awaitControl()
        returnVal = FFX_Miihen.arrival()
        print(returnVal)
        SkipAttempts += 1
        if returnVal[3] == True:
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
        # FFX_MRR.mainPath(wakkaLateMenu[0])
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
        if guadoSkipStatus == True:
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
        if jyscalSkipStatus == True:
            SkipCount += 1
        # elif jyscalRetry == False:
            #attempts -= 1
            #jyscalRetry = True
        print("------------------------------")
        print("------------------------------")
        print("Attempts:", SkipAttempts)
        print("Success:", SkipCount)
        print("------------------------------")
        print("------------------------------")
    # elif attempts == 5:
    #    print("Demo - Gagazet Cave")
    #    FFX_LoadGame.loadOffset(6)
    #    FFX_LoadGame.loadGagazetDream()
    #    #FFX_memory.setEncounterRate(0)
    #    FFX_Gagazet.cave()
    # elif attempts == 5:
    #    print("Demo - Egg Hunt")
    #    FFX_LoadGame.loadOffset(3)

    #    FFXC.set_movement(1, 1)
    #    time.sleep(0.7)
    #    FFXC.set_movement(0, 1)
    #    time.sleep(34)
    #    FFXC.set_neutral()

    #    print("Start egg hunt only program")
    #    print("--------------------------No-control method")

    #    FFX_Sin.eggHunt(True)
    #    FFX_Battle.BFA() #If an extra 20-30 minutes is needed
    # elif attempts == 7:
    #    print("Demo - Lightning Dodging, no set duration")
    #    FFX_LoadGame.loadOffset(12)
    #    FFX_memory.awaitControl()
    #    FFXC.set_movement(0, -1)
    #    time.sleep(1)
    #    FFX_memory.setEncounterRate(0)
    #    FFX_memory.awaitEvent()
    #    FFXC.set_neutral()
    #
    #    lStrikeCount = FFX_memory.lStrikeCount()
    #    #print("Starting count of lightning strikes:", lStrikeCount)
    #    lStrikeStart = lStrikeCount
    #    complete = False
    #    while lStrikeCount - lStrikeStart < 200:
    #        if FFX_memory.dodgeLightning(lStrikeCount):
    #            FFX_memory.awaitControl()
    #            lStrikeCount = FFX_memory.lStrikeCount()
    #            print("Dodge count, ", lStrikeCount - lStrikeStart)
    #        elif FFX_memory.userControl():
    #            FFX_targetPathing.setMovement([62,780])
    #        else:
    #            FFXC.set_neutral()
    #            if FFX_Screen.BattleScreen():
    #                print("Battle is now online.")
    #                FFX_Screen.awaitTurn()
    #                FFX_Battle.fleeAll()
    #                print("Battle complete")
    #                FFX_memory.clickToControl()

    #    checkpoint = 0
    #    while FFX_memory.getMap() != 256:
    #        if FFX_memory.dodgeLightning(lStrikeCount):
    #            FFX_memory.awaitControl()
    #            lStrikeCount = FFX_memory.lStrikeCount()
    #            print("Dodge count, ", lStrikeCount - lStrikeStart)
    #        elif FFX_memory.userControl():
    #            if FFX_targetPathing.setMovement(FFX_targetPathing.tPlainsDodging(checkpoint)) == True:
    #                checkpoint += 1
    #                print("Checkpoint reached:", checkpoint)
    #        else:
    #            FFXC.set_neutral()
    #            if FFX_Screen.BattleScreen():
    #                print("Battle is now online.")
    #                FFX_Screen.awaitTurn()
    #                FFX_Battle.fleeAll()
    #                print("Battle complete")
    #                FFX_memory.clickToControl()

    #    #To the chest
    #    print("Positioning for chest")
    #    while FFX_targetPathing.setMovement([-64,53]) == False:
    #        moving = True
    #    FFX_memory.setEncounterRate(1)
    #    FFXC.set_movement(-1, 0)
    #    FFX_memory.clickToEvent()
    #    FFXC.set_neutral()
    #    print("Advertisement for the Travel Agency")
    #    FFX_memory.clickToControl3()
    #    time.sleep(0.07)
    #
    #    FFX_memory.clickToEvent()
    #    print("(extra event, not sure)")
    #    FFX_memory.clickToControl3()
    #    time.sleep(0.07)
    #
    #    FFX_memory.clickToEvent()
    #    print("X-potion x2 (5)")
    #    FFX_memory.clickToControl3()
    #    time.sleep(0.07)

    #    FFX_memory.clickToEvent()
    #    print("Mega-Potion x2 (10)")
    #    FFX_memory.clickToControl3()
    #    time.sleep(0.07)

    #    FFX_memory.clickToEvent()
    #    print("MP Sphere x2 (20)")
    #    FFX_memory.clickToControl3()
    #    time.sleep(0.07)

    #    FFX_memory.clickToEvent()
    #    print("Strength sphere x3 (50)")
    #    FFX_memory.clickToControl3()
    #    time.sleep(0.07)

    #    FFX_memory.clickToEvent()
    #    print("HP Sphere x3 (100)")
    #    FFX_memory.clickToControl3()
    #    time.sleep(0.07)

    #    FFX_memory.clickToEvent()
    #    print("Megalixir x4 (150)")
    #    FFX_memory.clickToControl3()
    #    time.sleep(0.07)

    #    FFX_memory.clickToEvent()
    #    print("Venus Sigil (200)")

    #    time.sleep(5)
    #    FFX_Xbox.tapB()
    #    time.sleep(5)
    #    FFX_Xbox.tapB()
    #    time.sleep(5)
    #    #attempts -= 1
    #    attempts = 100

    # elif attempts < 30: #Testing loop
    #    FFX_LoadGame.loadOffset(15)
    #    import FFX_home
    #    FFX_home.desert()
    else:  # Breaks the loop when everything is complete.
        attempts = 100

    # Clean-up for next round, or process termination.
    FFXC.set_neutral()
    if attempts < 100:
        print("Demo complete. Now clicking to control so we can reset. ", attempts)
        if FFX_memory.getStoryProgress() < 3380:
            FFX_memory.clickToControl()
            time.sleep(2)
        else:
            time.sleep(10)

        print("Resetting.")
        # FFX_memory.end()

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

#print("--------TASgiving, please stop the timer-------------")
# print("--------------------------")
#print("Questing for Glory: Hope & Healing II")
# print("--------------------------")
# time.sleep(2)
#print("Thank you to the event organizers, planning staff, and volunteers that made this possible.")
# print("--------------------------")
# time.sleep(2)
#print("For this FFX project, thank you also to")
#print("these individuals:")
# time.sleep(1.5)
#print("-Blueaurora - my wife - for putting up with")
#print("me for literal years")
# time.sleep(1.5)
#print("-My wife is the best!")
# time.sleep(1.5)
# print("--------------------------")
# time.sleep(1.5)
#print("-DwangoAC and the TASbot community")
# time.sleep(1.5)
#print("-Inverted from the TASbot community")
# time.sleep(1.5)
#print("-TheAxeMan from the TASbot community")
# time.sleep(1.5)
#print("-Rossy__ from the FFX Speed-running community")
# time.sleep(1.5)
#print("-CrimsonInferno from the FFX Speed-running community")
#print("(current WR holder, multiple categories) ")
# time.sleep(1.5)
#print("-Highspirits from QfG staff, amazing work on the event!")
# time.sleep(1.5)
#print("-And countless other people who have supported me along")
#print("the way on this project.")
# time.sleep(1.5)
#print("-May the rest of QfG:HH2 be a major success!")

time.sleep(5)
FFX_memory.end()
print("--------------------------")
print("Program - end")
print("--------------------------")
