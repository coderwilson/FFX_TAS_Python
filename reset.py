import xbox
import memory
import datetime
import logs
import vars
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def midRunReset(landRun: bool = False, startTime=datetime.datetime.now()):
    if landRun:
        endTime = logs.timeStamp()
        totalTime = endTime - startTime
        logs.writeStats("Total time:")
        logs.writeStats(str(totalTime))
        print("The game duration was:", str(totalTime))
        print("This duration is intended for comparison reference only, not as a true timer.")
        print("Please do not use this as your submitted time.")
        memory.waitFrames(30)
        print("--------")
        print("In order to conform with speedrun standards,")
        memory.waitFrames(60)
        print("we now wait until the end of the credits and stuff")
        memory.waitFrames(60)
        print("and then will open up the list of saves.")
        memory.waitFrames(60)
        print("This will show the autosave values, which conforms to the speedrun rules.")
        # Bring up auto-save
        while memory.getMap() != 23:
            if memory.getMap() in [348, 349]:
                xbox.tapStart()
            elif memory.cutsceneSkipPossible():
                xbox.skipScene()
        memory.waitFrames(180)
        while not memory.saveMenuOpen():
            xbox.tapB()
        memory.waitFrames(180)
        xbox.menuA()
        xbox.menuA()
        xbox.menuA()
    else:
        memory.waitFrames(60)
        resetToMainMenu()

    # Now to re-start
    gameVars.setStartVars()
    rngSeed = memory.rngSeed()
    if landRun:
        rngSeed += 1
        if rngSeed == 256:
            rngSeed = 0
    logs.resetStatsLog()
    logs.nextStats(rngSeed)  # Start next stats file
    if gameVars.useSetSeed():
        memory.setRngSeed(rngSeed)
    print("-------------This game will be using RNG seed:", rngSeed)
    logs.nextStats(rngSeed)
    logs.writeStats("RNG seed:")
    logs.writeStats(rngSeed)
    Gamestate = 'none'
    StepCounter = 1

    return Gamestate, StepCounter


def resetToMainMenu():
    FFXC.set_neutral()
    if memory.getStoryProgress() <= 8:
        memory.waitFrames(30 * 0.07)
        while not memory.getMap() in [23, 348, 349]:
            print("----------Attempting reset")
            print("FFX map:", memory.getMap())
            print("----------")
            memory.setMapReset()
            memory.waitFrames(30 * 0.1)
            memory.forceMapLoad()
            memory.waitFrames(30 * 1)
    elif memory.battleActive():
        print("Battle is active. Forcing battle to end so we can soft reset.")
        while not memory.turnReady():
            xbox.menuA()
        memory.resetBattleEnd()
        while not memory.getMap() in [23, 348, 349]:
            xbox.menuB()

    else:
        memory.waitFrames(30 * 0.07)
        while not memory.getMap() in [23, 348, 349]:
            print("----------Attempting reset")
            print("FFX map:", memory.getMap())
            print("----------")
            memory.setMapReset()
            memory.waitFrames(30 * 0.1)
            memory.forceMapLoad()
            memory.waitFrames(30 * 1)
    print("Resetting")
