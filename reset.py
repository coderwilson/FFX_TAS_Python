import datetime

import logs
import memory.main
import vars
import xbox

gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def midRunReset(landRun: bool = False, startTime=datetime.datetime.now()):
    if landRun:
        endTime = logs.timeStamp()
        totalTime = endTime - startTime
        logs.writeStats("Total time:")
        logs.writeStats(str(totalTime))
        print("The game duration was:", str(totalTime))
        print(
            "This duration is intended for comparison reference only, not as a true timer."
        )
        print("Please do not use this as your submitted time.")
        memory.main.waitFrames(30)
        print("--------")
        print("In order to conform with speedrun standards,")
        memory.main.waitFrames(60)
        print("we now wait until the end of the credits and stuff")
        memory.main.waitFrames(60)
        print("and then will open up the list of saves.")
        memory.main.waitFrames(60)
        print(
            "This will show the autosave values, which conforms to the speedrun rules."
        )
        # Bring up auto-save
        while memory.main.getMap() != 23:
            if memory.main.getMap() in [348, 349]:
                xbox.tapStart()
            elif memory.main.cutsceneSkipPossible():
                xbox.skipScene()
        memory.main.waitFrames(180)
        while not memory.main.saveMenuOpen():
            xbox.tapB()
        memory.main.waitFrames(180)
        xbox.menuA()
        xbox.menuA()
        xbox.menuA()
    else:
        memory.main.waitFrames(60)
        resetToMainMenu()

    # Now to re-start
    gameVars.setStartVars()
    rngSeed = memory.main.rngSeed()
    if landRun:
        rngSeed += 0
        if rngSeed == 256:
            rngSeed = 0
    logs.resetStatsLog()
    logs.nextStats(rngSeed)  # Start next stats file
    if gameVars.useSetSeed():
        memory.main.setRngSeed(rngSeed)
    print("-------------This game will be using RNG seed:", rngSeed)
    logs.nextStats(rngSeed)
    logs.writeStats("RNG seed:")
    logs.writeStats(rngSeed)
    Gamestate = "none"
    StepCounter = 1

    return Gamestate, StepCounter


def resetToMainMenu():
    FFXC.set_neutral()
    if memory.main.getStoryProgress() <= 8:
        memory.main.waitFrames(30 * 0.07)
        while not memory.main.getMap() in [23, 348, 349]:
            print("----------Attempting reset")
            print("FFX map:", memory.main.getMap())
            print("----------")
            memory.main.setMapReset()
            memory.main.waitFrames(30 * 0.1)
            memory.main.forceMapLoad()
            memory.main.waitFrames(30 * 1)
    elif memory.main.battleActive():
        print("Battle is active. Forcing battle to end so we can soft reset.")
        while not memory.main.turnReady():
            xbox.menuA()
        memory.main.resetBattleEnd()
        while not memory.main.getMap() in [23, 348, 349]:
            xbox.menuB()

    else:
        memory.main.waitFrames(30 * 0.07)
        while not memory.main.getMap() in [23, 348, 349]:
            print("----------Attempting reset")
            print("FFX map:", memory.main.getMap())
            print("----------")
            memory.main.setMapReset()
            memory.main.waitFrames(30 * 0.1)
            memory.main.forceMapLoad()
            memory.main.waitFrames(30 * 1)
    print("Resetting")
