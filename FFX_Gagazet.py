import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory
import FFX_targetPathing

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC
 
def calmLands(blitzWin):
    FFX_memory.awaitControl()
    #Start by getting away from the save sphere
    FFX_menu.prepCalmLands(blitzWin)
    FFX_memory.fullPartyFormat('kimahri')
    
    FFXC.set_movement(0, 1)
    time.sleep(4)
    FFXC.set_neutral()
    FFX_memory.clickToControl()
    
    gemSlot = FFX_memory.getItemSlot(34)
    if gemSlot != 255:
        gems = FFX_memory.getItemCountSlot(gemSlot)
    else:
        gems = 0
    
    checkpoint = 0
    itemSteal = gems
    while FFX_memory.getMap() != 279:
        if FFX_memory.userControl():
            if checkpoint == 9 and itemSteal < 2:
                checkpoint = 8
                FFXC.set_movement(0, -1)
                time.sleep(2)
            elif FFX_targetPathing.setMovement(FFX_targetPathing.calmLands(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_Screen.BattleScreen():
                itemSteal += FFX_Battle.calmLands(itemSteal)
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.menuB()

def defenderX():
    time.sleep(0.5)
    FFX_memory.awaitControl()
    while FFX_targetPathing.setMovement([67,-255]) == False:
        doNothing = True
    FFXC.set_movement(0, 1)
    FFX_memory.awaitEvent()
    FFXC.set_neutral()
    
    FFX_Xbox.clickToBattle()
    FFX_Battle.buddySwap(0)
    FFX_Battle.aeonSummon(4)
    FFX_memory.clickToControl()
    
def toTheRonso():
    checkpoint = 0
    while FFX_memory.getMap() != 259:
        if FFX_memory.userControl():
            if FFX_targetPathing.setMovement(FFX_targetPathing.defenderX(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFXC.set_value('BtnB', 1)
                time.sleep(0.035)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.035)
    
    #Now in screen with Ronso
    checkpoint = 0
    while FFX_memory.getMap() != 244:
        if FFX_memory.userControl():
            if FFX_targetPathing.setMovement(FFX_targetPathing.kelkRonso(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.turnReady():
                endGameVersion = FFX_Battle.biranYenke()
            elif FFX_memory.diagSkipPossible():
                FFXC.set_value('BtnB', 1)
                time.sleep(0.035)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.035)
    
    return endGameVersion
    
def gagazetGates(blitzWin, endGameVersion):
    #Should appear on the map just before the Ronso hymn
    print("Grid version: " + str(endGameVersion))
    FFX_Logs.writeLog("Grid version: " + str(endGameVersion))
    FFX_memory.awaitControl()
    if FFX_memory.overdriveState()[6] == 100:
        FFX_memory.fullPartyFormat('kimahri')
    else:
        FFX_memory.fullPartyFormat('rikku')
    FFX_menu.afterRonso(endGameVersion, blitzWin)
    FFX_memory.closeMenu() #just in case
    
    print("Gagazet path section")
    checkpoint = 0
    while FFX_memory.getMap() != 285:
        if FFX_memory.userControl():
            if FFX_targetPathing.setMovement(FFX_targetPathing.gagazetSnow(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.menuOpen():
                FFXC.set_value('BtnB', 1)
                time.sleep(0.035)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.035)
            elif FFX_memory.turnReady():
                #Charge Rikku until full, otherwise flee all
                if FFX_memory.overdriveState()[6] == 100:
                    FFX_Battle.fleeAll()
                    FFX_memory.clickToControl()
                else:
                    FFX_Battle.gagazetPath()
                    FFX_memory.clickToControl()
                    if FFX_memory.overdriveState()[6] == 100:
                        FFX_memory.fullPartyFormat('kimahri')
                    else:
                        FFX_memory.fullPartyFormat('rikku')
            elif FFX_memory.diagSkipPossible():
                FFXC.set_value('BtnB', 1)
                time.sleep(0.035)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.035)
    #Should now be on the map with Seymour Flux. Moving to next section

def Flux():
    FFX_memory.fullPartyFormat('yuna')
    FFX_menu.beforeFlux()
    
    checkpoint = 0
    while FFX_memory.getMap() != 309:
        if FFX_memory.userControl():
            if checkpoint == 7:
                FFXC.set_movement(0, 1)
                time.sleep(0.5)
                FFXC.set_neutral()
                
                FFX_Xbox.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 8:
                while FFX_memory.userControl():
                    FFXC.set_movement(1, 1)
                FFXC.set_neutral()
            elif FFX_targetPathing.setMovement(FFX_targetPathing.Flux(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif FFX_memory.turnReady():
                FFX_Battle.seymourFlux()
                FFX_menu.afterFlux()
                FFX_memory.fullPartyFormat('kimahri')
    while not FFX_memory.cutsceneSkipPossible():
        if FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
    FFX_Xbox.skipScene()

def dream():
    FFX_memory.clickToControl()
    print("*********")
    print("Dream sequence")
    print("*********")
    time.sleep(0.2)
    pos = FFX_memory.getCoords()
    while pos[1] > 180:
        FFXC.set_movement(1, 1)
        pos = FFX_memory.getCoords()

    while pos[0] < -1:
        FFXC.set_movement(0, 1)
        pos = FFX_memory.getCoords()
        
    while pos[1] > 20:
        FFXC.set_movement(1, 1)
        pos = FFX_memory.getCoords()
    print("Onto the gangway")
        
    while pos[0] < 235:
        if pos[1] < -6:
            FFXC.set_movement(-1, 0)
        else:
            FFXC.set_movement(-1, 1)
        pos = FFX_memory.getCoords()

    while FFX_memory.userControl(): #Into the boathouse.
        FFXC.set_movement(-1, 0)
    print("Now inside the boathouse.")
    
    FFX_memory.awaitControl()
    FFXC.set_movement(1, 0)
    time.sleep(0.7)
    FFXC.set_movement(0, 1)
    time.sleep(1)
    FFXC.set_neutral() #Start convo with Bahamut child
    print("First talk with Bahamut child")
    FFX_memory.clickToControl()
    
    FFXC.set_movement(0, -1) #End of conversation
    time.sleep(0.7)
    FFXC.set_movement(-1, 0)
    time.sleep(0.7)
    FFXC.set_movement(0, -1)
    time.sleep(0.7)
    FFXC.set_neutral()
    
    FFX_memory.clickToControl()
    pos = FFX_memory.getCoords()
    while pos[1] > -20:
        FFXC.set_movement(1, 0)
        pos = FFX_memory.getCoords()
    
    while pos[0] < 300:
        FFXC.set_movement(0, 1)
        pos = FFX_memory.getCoords()
    FFXC.set_movement(-1, 0)
    FFX_Xbox.SkipDialog(2)
    FFXC.set_neutral() #Second/last convo with kid
    print("Second talk with Bahamut child")
    
    FFX_memory.clickToControl()
    
def cave():
    checkpoint = 0
    
    checkpoint = 0
    while FFX_memory.getMap() != 272:
        if FFX_memory.userControl():
            if FFX_targetPathing.setMovement(FFX_targetPathing.gagazetDream(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
    
    
    FFX_memory.awaitControl()
    print("Gagazet cave section")
    #FFX_menu.gagazetCave()
    
    checkpoint = 0
    lastCP = 0
    powerNeeded = 6
    while FFX_memory.getMap() != 311:
        if FFX_memory.userControl():
            if checkpoint == 7:
                if FFX_memory.getMap() == 310:
                    print("Now in the trials map.")
                    checkpoint += 1
                else:
                    print("Into swimming map, first trial.")
                    FFXC.set_movement(0, 1)
                    time.sleep(0.5)
            elif checkpoint == 12:
                print("Trial 1 - Let's Go!!!")
                while FFX_memory.userControl():
                    FFXC.set_movement(0, 1)
                FFXC.set_neutral()
                
                print("Now the trial has started.")
                FFX_Xbox.SkipDialog(4)
                FFX_Screen.awaitPixel(1184,226,(255,255,255))
                time.sleep(1.2)
                FFX_Xbox.menuB() #Attempting for first shot
                print("First attempt.")
                time.sleep(3)
                complete = False
                while complete == False:
                    if FFX_memory.userControl():
                        complete = True
                    elif FFX_Screen.PixelTestTol(1184,226,(255,255,255),5):
                        time.sleep(5.1)
                        FFX_Xbox.menuB() #Subsequent attempts
                        print("Additional attempt.")
                        time.sleep(4.4)
                        if FFX_memory.userControl():
                            complete = True
                        else:
                            time.sleep(1.6) #Timing to re-try
                print("First trial complete")
                checkpoint += 1
            elif checkpoint == 17:
                if FFX_memory.getMap() == 272:
                    print("Leaving the trials map.")
                    checkpoint += 1
                else:
                    print("Back to main map after first trial.")
                    FFXC.set_movement(0, -1)
                    time.sleep(0.5)
            elif checkpoint == 29:
                if FFX_memory.getMap() == 310:
                    print("Now in the trials map.")
                    checkpoint += 1
                else:
                    print("Into swimming map, second trial.")
                    FFXC.set_movement(0, 1)
                    time.sleep(0.5)
            elif checkpoint == 35:
                if FFX_memory.userControl():
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_neutral()
                    
            elif checkpoint == 42:
                print("Out of swimming map, second trial.")
                if FFX_memory.getMap() == 272:
                    print("Leaving the trials map.")
                    checkpoint += 1
                else:
                    FFXC.set_movement(0, -1)
                    time.sleep(0.5)
            elif checkpoint == 59: #Just before sanctuary keeper
                FFXC.set_neutral()
                print("Prepping for Sanctuary Keeper")
                FFX_memory.fullPartyFormat('yuna')
                checkpoint += 1
            elif FFX_targetPathing.setMovement(FFX_targetPathing.gagazetCave(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if checkpoint == 35 and (FFX_Screen.PixelTestTol(495,440,(234, 195, 0),5)):
                print("Second trial start")
                time.sleep(0.07)
                FFX_Xbox.menuB()
                time.sleep(1.5)
                FFXC.set_value('Dpad', 8)
                time.sleep(1.5)
                FFXC.set_neutral()
                FFX_memory.clickToControl()
                checkpoint += 1
                print("Second trial is complete")
            elif FFX_memory.turnReady():
                if FFX_memory.getPower() < powerNeeded:
                    if FFX_memory.getBattleNum() == 351: #Two maelstroms and a splasher
                        FFX_Battle.gagazetCave('down')
                    elif FFX_memory.getBattleNum() == 353: #Two glowey guys, two splashers.
                        FFX_Battle.gagazetCave('right')
                    elif FFX_memory.getBattleNum() == 354: #Four groups of splashers
                        FFX_Battle.gagazetCave('none')
                    else:
                        FFX_Battle.fleeAll()
                else:
                    FFX_Battle.fleeAll()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif checkpoint == 6 or checkpoint == 54:
                if FFX_memory.battleActive():
                    FFX_Battle.fleeAll()
                elif FFX_memory.diagSkipPossible(): #So we don't override the second trial
                    FFX_Xbox.tapB()
                
                #if FFX_memory.getPower() < powerNeeded and checkpoint >= 30 and checkpoint < 60:
                #    FFX_Battle.gagazetCave()
                #elif FFX_memory.getPower() < powerNeeded and checkpoint >= 90 and checkpoint < 110:
                #    FFX_Battle.gagazetCave()
                #else:
    FFX_Xbox.clickToBattle()
    FFX_Battle.sKeeper()

def wrapUp():
    print("Cave section complete and Sanctuary Keeper is down.")
    print("Now onward to Zanarkand.")
    
    checkpoint = 0
    while FFX_memory.getMap() != 132:
        if FFX_memory.userControl():
            if FFX_memory.getMap() == 312 and checkpoint < 6:
                print("Move forward to next map. Final path before making camp.")
                checkpoint = 7
            elif checkpoint == 3:
                if FFX_memory.getStoryProgress() >= 2651:
                    checkpoint += 1
                else: #2635 before agency scene, 2650 during the agency scene
                    FFXC.set_movement(-1, 1)
                    FFXC.set_value('BtnB', 1)
                    time.sleep(0.035)
                    FFXC.set_value('BtnB', 0)
                    time.sleep(0.035)
            elif checkpoint == 6:
                if FFX_memory.getMap() == 312:
                    print("Final path before making camp.")
                    FFXC.set_neutral()
                    checkpoint += 1
                else:
                    FFXC.set_movement(1, 1)
            elif FFX_targetPathing.setMovement(FFX_targetPathing.gagazetPeak(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    
    
    #Resting point before Zanarkand
    FFXC.set_neutral()
    FFX_memory.awaitControl()
    time.sleep(0.07)
    FFXC.set_movement(0, 1) #Start of the sadness cutscene.
    time.sleep(3)
    FFXC.set_neutral()
    
    sleepTime = 4
    print("Sadness cutscene")
    time.sleep(sleepTime)
    print("This is gunna be a while.")
    time.sleep(sleepTime)
    print("Maybe you should go get a drink or something.")
    time.sleep(sleepTime)
    print("Like... what even is this???")
    time.sleep(sleepTime)
    print("I just")
    time.sleep(sleepTime)
    print("I just can't")
    time.sleep(sleepTime)
    print("Do you realize that some poor soul")
    time.sleep(sleepTime)
    print("not only wrote the entire program for this by himself")
    time.sleep(sleepTime)
    print("And then wasted ten minutes to put in this ridiculous dialog?")
    time.sleep(sleepTime)
    print("Talk about not having a life.")
    time.sleep(sleepTime)
    print("Ah well, still have some time. Might as well shout out a few people.")
    time.sleep(sleepTime)
    print("First and most importantly, my wife for putting up with me for two years through this project.")
    time.sleep(sleepTime)
    print("My wife is the best!")
    time.sleep(sleepTime)
    print("Next, DwangoAC. He encouraged me to write my own code to do this.")
    time.sleep(sleepTime)
    print("And he put together the TASbot community which has been hugely helpful.")
    time.sleep(sleepTime)
    print("Shout out to DwangoAC and the TASbot Community. You guys rock!!!")
    time.sleep(sleepTime)
    print("Specifically from the TASbot Community, Inverted wrote the pathing logic for the Egg Hunt section.")
    time.sleep(sleepTime)
    print("You will see Inverted's work right before the final bosses.")
    time.sleep(sleepTime)
    print("Next, some people from the FFX speed-running community.")
    time.sleep(sleepTime)
    print("CrimsonInferno, current world record holder for this category. Dude knows everything about this run!")
    time.sleep(sleepTime)
    print("Crimson re-wrote a great many boss fights for this project. From Spherimorph to Evrae Altana, and probably more.")
    time.sleep(sleepTime)
    print("Also, 'Rossy__' from the same community. Rossy helped me find a great many things in memory.")
    time.sleep(sleepTime)
    print("He also taught me a number of things about memory scans, pointers, etc. Dude is super smart.")
    time.sleep(sleepTime)
    print("OK I'll catch you when it's done.")
    time.sleep(sleepTime)
    
    FFX_memory.clickToControl()
    print("OMG finally! Let's get to it! (Do kids say that any more?)")
    FFXC.set_movement(0, 1)
    time.sleep(1)
    FFXC.set_movement(-1, 1)
    FFX_memory.awaitEvent()
    FFXC.set_neutral()
    time.sleep(0.2)