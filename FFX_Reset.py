import FFX_Xbox
import FFX_memory
import datetime
import FFX_Logs
import FFX_vars
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()


def midRunReset(landRun: bool = False, startTime=datetime.datetime.now()):
    if landRun:
        endTime = FFX_Logs.timeStamp()
        totalTime = endTime - startTime
        FFX_Logs.writeStats("Total time:")
        FFX_Logs.writeStats(str(totalTime))
        print("The game duration was:", str(totalTime))
        print("This duration is intended for comparison reference only, not as a true timer.")
        print("Please do not use this as your submitted time.")
        FFX_memory.waitFrames(30)
        print("--------")
        print("In order to conform with speedrun standards,")
        FFX_memory.waitFrames(60)
        print("we now wait until the end of the credits and stuff")
        FFX_memory.waitFrames(60)
        print("and then will open up the list of saves.")
        FFX_memory.waitFrames(60)
        print("This will show the autosave values, which conforms to the speedrun rules.")
        # Bring up auto-save
        while FFX_memory.getMap() != 23:
            if FFX_memory.getMap() in [348, 349]:
                FFX_Xbox.tapStart()
            elif FFX_memory.cutsceneSkipPossible():
                FFX_Xbox.skipScene()
        FFX_memory.waitFrames(180)
        while not FFX_memory.saveMenuOpen():
            FFX_Xbox.tapB()
        FFX_memory.waitFrames(180)
        FFX_Xbox.menuA()
        FFX_Xbox.menuA()
        FFX_Xbox.menuA()
    else:
        FFX_memory.waitFrames(60)
        resetToMainMenu()

    # Now to re-start
    gameVars.setStartVars()
    rngSeed = FFX_memory.rngSeed()
    if landRun:
        rngSeed += 1
        if rngSeed == 256:
            rngSeed = 0
    FFX_Logs.resetStatsLog()
    FFX_Logs.nextStats(rngSeed)  # Start next stats file
    if gameVars.useSetSeed():
        FFX_memory.setRngSeed(rngSeed)
    print("-------------This game will be using RNG seed:", rngSeed)
    FFX_Logs.nextStats(rngSeed)
    FFX_Logs.writeStats("RNG seed:")
    FFX_Logs.writeStats(rngSeed)
    Gamestate = 'none'
    StepCounter = 1

    return Gamestate, StepCounter


def resetToMainMenu():
    FFXC.set_neutral()
    if FFX_memory.getStoryProgress() <= 8:
        FFX_memory.waitFrames(30 * 0.07)
        while not FFX_memory.getMap() in [23, 348, 349]:
            print("----------Attempting reset")
            print("FFX map:", FFX_memory.getMap())
            print("----------")
            FFX_memory.setMapReset()
            FFX_memory.waitFrames(30 * 0.1)
            FFX_memory.forceMapLoad()
            FFX_memory.waitFrames(30 * 1)
    elif FFX_memory.battleActive():
        print("Battle is active. Forcing battle to end so we can soft reset.")
        while not FFX_memory.turnReady():
            FFX_Xbox.menuA()
        FFX_memory.resetBattleEnd()
        while not FFX_memory.getMap() in [23, 348, 349]:
            FFX_Xbox.menuB()

    else:
        FFX_memory.waitFrames(30 * 0.07)
        while not FFX_memory.getMap() in [23, 348, 349]:
            print("----------Attempting reset")
            print("FFX map:", FFX_memory.getMap())
            print("----------")
            FFX_memory.setMapReset()
            FFX_memory.waitFrames(30 * 0.1)
            FFX_memory.forceMapLoad()
            FFX_memory.waitFrames(30 * 1)
    print("Resetting")
