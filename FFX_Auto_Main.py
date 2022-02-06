# Libraries and Core Files
import FFX_vars
gameVars = FFX_vars.varsHandle()
import time
import random
import FFX_core
import FFX_Screen
import FFX_Battle
import FFX_memory

#Plug in controller
import FFX_Xbox
FFXC = FFX_Xbox.controllerHandle()

#Speed run sectional files
import FFX_DreamZan
import FFX_Baaj
import FFX_Besaid1
#import FFX_Besaid2
import FFX_Boats
import FFX_Kilika
import FFX_Luca
import FFX_Blitz
import FFX_Miihen
import FFX_MRR
import FFX_Djose
import FFX_Moonflow
import FFX_Guadosalam
import FFX_ThunderPlains
import FFX_mWoods
import FFX_mTemple
import FFX_home
import FFX_rescueYuna
import FFX_Gagazet
import FFX_Zanarkand
import FFX_Sin

#Gamestate, "none" for new game, or set to a specific section to start from the first save.
#See the if statement tree below to determine starting position for Gamestate.
#These are the popular ones. New Game ('none') is the last one.
#Gamestate = "Baaj"
#StepCounter = 1
#StepCounter = 6
#Gamestate = "Besaid"
#StepCounter = 3
Gamestate = "Kilika"
StepCounter = 1
#Gamestate = "Luca"
#StepCounter = 1
#StepCounter = 3
#StepCounter = 5
#Gamestate = "Miihen"
#StepCounter = 1
#Gamestate = "MRR"
#StepCounter = 1
#Gamestate = "Djose"
#StepCounter = 1
#Gamestate = "Moonflow"
#StepCounter = 2
#Gamestate = "Guadosalam"
#StepCounter = 2
#Gamestate = "Macalania"
#StepCounter = 1
#StepCounter = 2
#StepCounter = 3
#StepCounter = 4 #Not working on Seymour fight
#StepCounter = 6 #Blitz loss, unsure if proper Thunder Plains purchase
#Gamestate = "Home"
#StepCounter = 1
#StepCounter = 2
#Gamestate = "rescueYuna"
#StepCounter = 1
#StepCounter = 2
#StepCounter = 5
#Gamestate = "Gagazet"
#StepCounter = 1
#StepCounter = 2 #Temp, do not use going forward
#StepCounter = 4
#Gamestate = "Zanarkand"
#StepCounter = 4
#Gamestate = "Sin"
#StepCounter = 2
#StepCounter = 4
Gamestate = "none"
StepCounter = 1

#Game length. Full is the same as any%, short is about 35 minutes with memory manip.
autoEggHunt = True

####################################################################################################
#RNG - Using Rossy's FFX.exe fix, this allows us to choose the RNG seed we want. From 0-255

forceBlitzWin = True
seedHunt = False #Update this to decide new seed or known seed
rngSeedNum = 130 #New seed number, only used if doing seed hunt.
####################################################################################################

if Gamestate != "none":
    rngSeedNum = 200 #Select a specific seed.
    rngReviewOnly = False
    gameLength = "Loading mid point for testing."
elif seedHunt == False: #Below logic for full runs only.
    rngSelectArray = [31,40,49,59,90,91,98,104,108,121,200]
    rngSeedNum = random.choice(rngSelectArray) #Select a favorite seed randomly
    #rngSeedNum = 40 #Select a specific seed.
    rngReviewOnly = False
    gameLength = "Full Run"
else: #Just to make sure we're running from new game for seed finding.
    StepCounter = 1
    rngReviewOnly = True
    gameLength = "Seed Hunt"

print("Game type will be: ", gameLength)
maxLoops = 25

#Other variables
rngSeedOrig = rngSeedNum
speedCount = 0
strengthCount = 0
gems = 0 #Set to 2 if loading in after Evrae Altana with two gems
earlyTidusGrid = False

#Main functions
def reportGamestate():
    
    global Gamestate
    global StepCounter
    logText = "Gamestate: " + Gamestate + " : StepCounter: " + str(StepCounter)
    FFX_Logs.writeLog(logText + "\n")
    FFX_Screen.clearMouse(0)

#Initiate memory reading, after we know the game is open.
#import FFX_memory
FFX_memory.start()

#Main
import FFX_Logs
print("FFX automation starting")
FFX_Logs.nextStats(rngSeedNum)
print("Please launch the game now.")
#FFX_memory.waitFrames(30 * 5)
#print("Now attempting to activate FFX window")
reportGamestate()

print("Game start screen")
FFX_Screen.clearMouse(0)


#FFX_memory.setRngSeed(rngSeedNum) #Using Rossy's FFX.exe fix, this allows us to choose the RNG seed we want. From 0-255
rngSeed = FFX_memory.rngSeed()
print("---RNG seed: ", rngSeed)
FFX_Logs.writeStats("RNG seed:")
FFX_Logs.writeStats(rngSeed)

#Next, check if we are loading to a save file
if Gamestate != "none" :
    FFX_DreamZan.NewGame(Gamestate)
    FFX_Logs.writeLog("Loading to a specific gamestate.\n")
    startTime = FFX_Logs.timeStamp()
    #FFX_Logs.writeStats("Start time:")
    #FFX_Logs.writeStats(str(startTime))
    reportGamestate()
    import FFX_LoadGame
    
    if Gamestate == "Baaj" and StepCounter == 1:
        FFX_LoadGame.loadOffset(22)
        #FFX_LoadGame.LoadBaaj()
    if Gamestate == "Baaj" and StepCounter == 5:
        FFX_LoadGame.LoadFirst()
    if Gamestate == "Baaj" and StepCounter == 6:
        FFX_LoadGame.loadOffset(1)
    if Gamestate == "Besaid" and StepCounter == 1 : #Save pop-up after falling off of Rikku's boat
        FFX_LoadGame.loadOffset(48)
    if Gamestate == "Besaid" and StepCounter == 2 : #Crusader's lodge before trials start
        FFX_LoadGame.BesaidTrials()
    if Gamestate == "Besaid" and StepCounter == 3 : #Crusader's lodge after "Enough, Wakka!"
        FFX_LoadGame.loadOffset(29)
        print("Load complete")
        FFX_LoadGame.loadMemCursor()
        while FFX_memory.userControl():
            if FFX_memory.getCoords()[0] > 0.5:
                FFXC.set_movement(1, 1)
            else:
                FFXC.set_movement(0, 1)
        print("Ready for regular path")
    if Gamestate == "Boat1" : #Besaid beach before boarding SS Liki ( nice alliteration :D )
        FFX_LoadGame.loadOffset(41)
        FFX_LoadGame.Boat1()
    if Gamestate == "Kilika" and StepCounter == 1: #Just after entering the woods
        FFX_LoadGame.loadOffset(22)
        FFXC.set_movement(0, 1)
        FFX_memory.waitFrames(30 * 5)
        FFXC.set_neutral()
    if Gamestate == "Boat3":
        FFX_LoadGame.loadOffset(1)
        FFXC.set_movement(0, 1)
        FFX_memory.waitFrames(30 * 1)
        FFXC.set_neutral()
        FFX_memory.waitFrames(30 * 2)
    if Gamestate == "Luca" and StepCounter == 1: # Approaching Luca via boat
        FFX_LoadGame.loadOffset(46)
    if Gamestate == "Luca" and StepCounter == 3: # after Oblitzerator, before Blitzball
        FFX_LoadGame.loadOffset(26)
    if Gamestate == "Luca" and StepCounter == 5: # After Blitzball, before battles.
        FFX_LoadGame.loadOffsetBattle(5)
    #if Gamestate == "Luca" and StepCounter == 6: #After the talk with Auron
    #    FFX_LoadGame.loadPostBlitz()
    if Gamestate == "Miihen" and StepCounter == 1: #After the talk with Auron
        FFX_LoadGame.loadOffset(33)
        import FFX_menu
        FFX_menu.mrrGrid1()
        FFX_LoadGame.LoadMiihenStart_Laugh()
    if Gamestate == "MRR" and StepCounter == 1: #Mi'ihen North after meeting Seymour
        FFX_LoadGame.loadOffset(29)
        import FFX_menu
        FFX_menu.mrrGrid1()
        FFX_menu.equipScout()
        FFX_LoadGame.LoadMRR()
    if Gamestate == "MRR" and StepCounter == 2: #Just before the last lift to the battle site
        FFX_LoadGame.loadOffset(1)
        FFX_LoadGame.LoadMRR2()
    if Gamestate == "Djose" and StepCounter == 1: # Aftermath, after talking to Seymour and then Auron
        FFX_LoadGame.loadOffset(8)
        FFX_LoadGame.AfterGui()
    if Gamestate == "Djose" and StepCounter == 2: #Just before the Djose temple
        FFX_LoadGame.djoseTemple()
    if Gamestate == "Moonflow" and StepCounter == 2: #North bank, before Rikku
        FFX_LoadGame.loadOffset(20)
        FFX_LoadGame.moonflow2()
    if Gamestate == "Guadosalam" and StepCounter == 2: #After the Farplane
        FFX_LoadGame.loadOffset(4)
        FFX_LoadGame.loadGuadoSkip()
    if Gamestate == "Macalania" and StepCounter == 1: #1 = south, 2 = north
        FFX_LoadGame.loadOffset(9)
    if Gamestate == "Macalania" and StepCounter == 2: #1 = south, 2 = north
        FFX_LoadGame.loadOffset(12)
    if Gamestate == "Macalania" and StepCounter == 3: #between Spherimorph and Crawler. Move to lake
        FFX_LoadGame.loadOffset(18)
        FFX_LoadGame.loadMacLake()
    if Gamestate == "Macalania" and StepCounter == 4: #Right before Jyscal skip
        FFX_LoadGame.loadOffset(10) #No remedy in inventory, likely game over.
        FFX_LoadGame.loadMacTemple()
    if Gamestate == "Macalania" and StepCounter == 5: #After Seymour, before trials
        FFX_LoadGame.loadMacTemple2()
    if Gamestate == "Macalania" and StepCounter == 6: #Outside temple, before escaping.
        FFX_LoadGame.loadOffset(17)
        FFX_LoadGame.loadMacTemple2()
    if Gamestate == "Macalania" and StepCounter == 7: #Before Wendigo
        FFX_LoadGame.loadOffsetBattle(0)
        FFX_LoadGame.loadWendigo()
    if Gamestate == "Home" and StepCounter == 1:
        FFX_LoadGame.loadOffset(16)
    if Gamestate == "Home" and StepCounter == 2:
        FFX_LoadGame.loadOffset(7)
    if Gamestate == "rescueYuna" and StepCounter == 1: # Airship, before pathing to the deck
        FFX_LoadGame.loadOffset(30)
        FFX_LoadGame.loadRescue()
    if Gamestate == "rescueYuna" and StepCounter == 2: # Bevelle trials
        FFX_LoadGame.loadOffset(42)
        #FFX_LoadGame.loadBahamut()
    if Gamestate == "rescueYuna" and StepCounter == 5: # Highbridge before Seymour Natus
        FFX_LoadGame.loadOffset(2)
    if Gamestate == "Gagazet" and StepCounter == 1: # Just before Calm Lands
        FFX_LoadGame.loadOffset(11)
        FFX_LoadGame.loadCalm()
    if Gamestate == "Gagazet" and StepCounter == 2: # Gagazet gates
        FFX_LoadGame.loadOffset(0)
        #FFX_LoadGame.loadGagaGates()
        #for i in range(60):
            #print(f"Sleeping for {60-i} more seconds...")
            #time.sleep(1)
    if Gamestate == "Gagazet" and StepCounter == 3: # Just before Seymour Flux
        FFX_LoadGame.LoadNeutral()
    if Gamestate == "Gagazet" and StepCounter == 4: # After the dream
        FFX_LoadGame.loadOffset(6)
        FFX_LoadGame.loadGagazetDream()
    if Gamestate == "Zanarkand" and StepCounter == 1: # Intro scene revisited
        FFX_LoadGame.zanEntrance()
    if Gamestate == "Zanarkand" and StepCounter == 2: # Just before the trials.
        FFX_LoadGame.loadOffset(36)
        FFX_LoadGame.zanTrials()
    if Gamestate == "Zanarkand" and StepCounter == 4: # After Sanctuary Keeper
        FFX_LoadGame.loadOffset(10)
        import FFX_menu
        FFX_menu.zombieStrkeBackup()
    if Gamestate == "Sin" and StepCounter == 2: #Save sphere on the Highbridge before talking to Shedinja
        FFX_LoadGame.loadOffset(28)
    if Gamestate == "Sin" and StepCounter == 4: #Before point of no return
        FFX_LoadGame.loadOffset(3)
        FFX_LoadGame.loadEggHunt()
    
    #if FFX_memory.getStoryProgress() >= 80:
    #    if Gamestate == "Luca" and StepCounter == 5:
    #        noMemCursor = True
    #    elif Gamestate == "Besaid" and StepCounter == 3:
    #        noMemCursor = True
    #    elif Gamestate == "Boat3":
    #        noMemCursor = True
    #    elif Gamestate == "Sin" and StepCounter == 4:
    #        noMemCursor = True
    #    else:
    #        print("Setting memory cursor")
    #        FFX_LoadGame.loadMemCursor()
    #    print("Done with memory cursor")


#Movement files - moved to FFX_compileAll.py

#try:
rikkucharged = 0

while Gamestate != "End":

    if rngSeedNum >= 256:
        Gamestate = "End"

    #Start of the game, start of Dream Zanarkand section
    if Gamestate == "none" and StepCounter == 1:
        reportGamestate()
        FFX_DreamZan.NewGame(Gamestate)
        Gamestate = "DreamZan"
        FFX_memory.waitFrames(30 * 0.5)
        FFX_DreamZan.NewGame2()
        startTime = FFX_Logs.timeStamp()
        FFX_Logs.writeStats("Start time:")
        FFX_Logs.writeStats(str(startTime))
        print("Timer starts now.")
        FFX_DreamZan.listenStory()
        #Start of the game, up through the start of Sinspawn Ammes fight
        StepCounter = 2
        FFX_DreamZan.ammesBattle()

    if Gamestate == "DreamZan" and StepCounter == 2:
        reportGamestate()
        FFX_Battle.Ammes()
        #Finishes Sinspawn Ammes fight
        
        StepCounter = 3
        reportGamestate()

    if Gamestate == "DreamZan" and StepCounter == 3:
        FFX_DreamZan.AfterAmmes()
        #Sin drops us near Baaj temple.
        Gamestate = "Baaj"
        StepCounter = 1
    
    if Gamestate == "Baaj" and StepCounter == 1 :
        reportGamestate()
        print ("Starting Baaj temple section")
        FFX_Baaj.Entrance()
        StepCounter = 2

    if Gamestate == "Baaj" and StepCounter == 2 :
        reportGamestate()
        FFX_Baaj.Baaj_puzzle()
        StepCounter = 3
        #Gamestate = "manualBreak" # Used for testing only.

    if Gamestate == "Baaj" and StepCounter == 3 :
        FFX_Baaj.Klikk_fight()
        StepCounter = 4
        reportGamestate()
        
    if Gamestate == "Baaj" and StepCounter == 4:
        #Klikk fight done. Now to wait for the Al Bhed ship.
        print("Al Bhed boat part 1")
        FFX_Baaj.ABboat1()
        StepCounter = 5
        
    if Gamestate == "Baaj" and StepCounter == 5:
        reportGamestate()
        FFX_Baaj.ABswimming1()
        StepCounter = 6
        reportGamestate()
        
    if Gamestate == "Baaj" and StepCounter == 6:
        print("Underwater Airship section")
        FFX_Baaj.ABswimming2()
        Gamestate = "Besaid"
        StepCounter = 1
        reportGamestate()

    if Gamestate == "Besaid" and StepCounter == 1 :
        reportGamestate()
        FFX_Besaid1.Beach()
        FFX_Besaid1.swimming1()
        FFX_Besaid1.enteringVillage()
        StepCounter = 2
        reportGamestate()

    if Gamestate == "Besaid" and StepCounter == 2 :
        FFX_Besaid1.trials()
        FFX_Besaid1.aeonAndSleep()
        StepCounter = 3
        reportGamestate()

    if Gamestate == "Besaid" and StepCounter == 3 :
        FFX_Besaid1.leaving()
        FFX_Besaid1.waterfalls()
        
        Gamestate = "Boat1"
        StepCounter = 1
        reportGamestate()

    if Gamestate == "Boat1" :
        reportGamestate()
        FFX_Boats.ssLiki()
        FFX_Kilika.arrival()
        Gamestate = "Kilika"
        #Gamestate = "manualBreak" # Used for testing only.

    if Gamestate == "Kilika" and StepCounter == 1 :
        reportGamestate()
        FFX_Kilika.forest1()
        FFX_Kilika.forest2()
        reportGamestate()
        #speedCount += FFX_Kilika.forest2()
        #print ("Speed spheres: ",speedCount)
        StepCounter = 2
        FFX_Kilika.Geneaux()
        StepCounter = 3

    if Gamestate == "Kilika" and StepCounter == 3 :
        reportGamestate()
        FFX_Kilika.trials()
        StepCounter = 4

    if Gamestate == "Kilika" and StepCounter == 4 :
        reportGamestate()
        FFX_Kilika.forest3()
        StepCounter = 5

    if Gamestate == "Kilika" and StepCounter == 5 :
        reportGamestate()
        FFX_Kilika.departure()
        StepCounter = 1
        Gamestate = "Boat2"
        FFX_Logs.nextFile()

    if Gamestate == "Boat2" :
        reportGamestate()
        FFX_Boats.ssWinno()
        
        Gamestate = "Boat3"
    
    
    if Gamestate == "Boat3":
        reportGamestate()
        FFX_Boats.ssWinno2()
        
        Gamestate = "Luca"

    if Gamestate == "Luca" and StepCounter == 1:
        reportGamestate()
        FFX_Luca.arrival()
        FFX_Luca.followYuna()
        StepCounter = 2

    if Gamestate == "Luca" and StepCounter == 2:
        reportGamestate()
        FFX_Luca.preBlitz()
        endTime = FFX_Logs.timeStamp()
        totalTime = endTime - startTime
        print("Pre-Blitz time: ", str(totalTime))
        FFX_Logs.writeStats("Pre Blitz time:")
        FFX_Logs.writeStats(totalTime)
        if rngReviewOnly == True and rngSeedNum - rngSeedOrig < maxLoops: # Used to run multiple tests via a single execution
            Gamestate = 'none'
            StepCounter = 1
            FFXC.set_movement(0, -1) #Step away from the save sphere
            FFX_memory.waitFrames(30 * 2)
            FFXC.set_neutral()
            import FFX_Reset
            print("------------------------------------------")
            print("------------------------------------------")
            print("Resetting")
            print("------------------------------------------")
            print("------------------------------------------")
            #FFX_memory.clickToControl()
            
            
            #FFX_Logs.writeStats("Test duration:")
            #FFX_Logs.writeStats(totalTime)
            FFX_memory.waitFrames(30 * 2)

            FFX_Reset.resetToMainMenu()
            StepCounter = 1
            rngSeedNum += 1
            FFX_Logs.nextStats(rngSeedNum) #Start next stats file
            FFX_memory.setRngSeed(rngSeedNum) #Using Rossy's FFX.exe fix, this allows us to choose the RNG seed we want. From 0-255
            rngSeed = FFX_memory.rngSeed()
            print("-------------This game will be using RNG seed: ", rngSeed)
            FFX_Logs.writeStats("RNG seed:")
            FFX_Logs.writeStats(rngSeed)
        else:
            StepCounter = 3

    if Gamestate == "Luca" and StepCounter == 3:
        reportGamestate()
        FFX_Luca.blitzStart()
        StepCounter = 4

    if Gamestate == "Luca" and StepCounter == 4:
        reportGamestate()
        gameVars.setBlitzWin(FFX_Blitz.blitzMain(forceBlitzWin))
        if not gameVars.csr():
            FFX_Xbox.awaitSave()
        StepCounter = 5
        

    if Gamestate == "Luca" and StepCounter == 5:
        reportGamestate()
        FFX_Luca.afterBlitz()
        StepCounter = 1
        Gamestate = "Miihen"
        #Gamestate = "manualBreak" # Used for testing only.
    
    #Just to make sure we set this variable somewhere.
    if Gamestate == "Miihen" and StepCounter == 1:
        reportGamestate()
        returnArray = FFX_Miihen.arrival()
        selfDestruct = FFX_Miihen.arrival2(returnArray[0], returnArray[1], returnArray[2])
        FFX_Miihen.midPoint()
        print("End of Miihen mid point section.")
        FFX_Miihen.lowRoad(returnArray[0], returnArray[1], returnArray[2])
        StepCounter = 2

    if Gamestate == "Miihen" and StepCounter == 2:
        reportGamestate()
        
        #Report duration at the end of Mi'ihen section for all runs.
        endTime = FFX_Logs.timeStamp()
        totalTime = endTime - startTime
        print("Mi'ihen End timer is: ", str(totalTime))
        FFX_Logs.writeStats("Miihen End time:")
        FFX_Logs.writeStats(totalTime)
        
        if rngReviewOnly == True and rngSeedNum - rngSeedOrig < maxLoops: # Used to run multiple tests via a single execution
            Gamestate = "none"
            StepCounter = 1
            import FFX_Reset
            print("------------------------------------------")
            print("------------------------------------------")
            print("Resetting")
            print("------------------------------------------")
            print("------------------------------------------")
            FFXC.set_neutral()
            FFX_memory.clickToControl()

            FFX_memory.waitFrames(30 * 2)

            FFX_Reset.resetToMainMenu()
            StepCounter = 1
            rngSeedNum += 1 #Start next stats file
            FFX_Logs.nextStats(rngSeedNum)
            FFX_memory.setRngSeed(rngSeedNum) #Using Rossy's FFX.exe fix, this allows us to choose the RNG seed we want. From 0-255
            rngSeed = FFX_memory.rngSeed()
            print("-------------This game will be using RNG seed: ", rngSeed)
            FFX_Logs.writeStats("RNG seed:")
            FFX_Logs.writeStats(rngSeed)
        else: #The last test, we will allow to run to completion (maybe)
            Gamestate = "MRR"
            StepCounter = 1
        
    if Gamestate == "MRR" and StepCounter == 1:
        reportGamestate()
        FFX_MRR.arrival()
        FFX_MRR.mainPath()
        if FFX_memory.gameOver():
            Gamestate = "gameOverError"
        StepCounter = 2
        #Gamestate = "End" # Used for testing only.

    if Gamestate == "MRR" and StepCounter == 2:
        reportGamestate()
        FFX_MRR.battleSite()
        FFX_MRR.guiAndAftermath()
        Gamestate = "Djose"
        StepCounter = 1
        #Gamestate = "End" # Used for testing only.

    if Gamestate == "Djose" and StepCounter == 1:
        reportGamestate()
        FFX_Djose.path()
        StepCounter = 2

    if Gamestate == "Djose" and StepCounter == 2:
        reportGamestate()
        FFX_Djose.temple()
        FFX_Djose.trials()
        StepCounter = 3

    if Gamestate == "Djose" and StepCounter == 3:
        reportGamestate()
        FFX_Djose.leavingDjose()
        StepCounter = 1
        Gamestate = "Moonflow"

    if Gamestate == "Moonflow" and StepCounter == 1:
        reportGamestate()
        FFX_Moonflow.arrival()
        FFX_Moonflow.southBank()
        StepCounter = 2

    if Gamestate == "Moonflow" and StepCounter == 2:
        reportGamestate()
        FFX_Moonflow.northBank()
        StepCounter = 1
        Gamestate = "Guadosalam"

    if Gamestate == "Guadosalam" and StepCounter == 1:
        reportGamestate()
        FFX_Guadosalam.arrival()
        FFX_Guadosalam.afterSpeech()
        StepCounter = 2

    if Gamestate == "Guadosalam" and StepCounter == 2:
        reportGamestate()
        FFX_Guadosalam.guadoSkip()
        StepCounter = 1
        Gamestate = "ThunderPlains"
        FFX_Logs.nextFile()

    if Gamestate == "ThunderPlains" and StepCounter == 1:
        status = [False,False,False,False,False]
        reportGamestate()
        status = FFX_ThunderPlains.southPathing(status)
        StepCounter = 2

    if Gamestate == "ThunderPlains" and StepCounter == 2:
        FFX_ThunderPlains.agency()
        StepCounter = 3

    if Gamestate == "ThunderPlains" and StepCounter == 3:
        status = FFX_ThunderPlains.northPathing(status)
        rikkucharged = status[0]
        Gamestate = "Macalania"
        StepCounter = 1

    if Gamestate == "Macalania" and StepCounter == 1:
        reportGamestate()
        FFX_mWoods.arrival(rikkucharged)
        StepCounter = 2

    if Gamestate == "Macalania" and StepCounter == 2:
        reportGamestate()
        FFX_mWoods.lakeRoad()
        FFX_mWoods.lakeRoad2()
        StepCounter = 3

    if Gamestate == "Macalania" and StepCounter == 3:
        reportGamestate()
        FFX_mWoods.lake()
        #FFX_mWoods.afterCrawler()
        FFX_mTemple.approach()
        StepCounter = 4
        #Gamestate = "manualBreak" # Used for testing only.

    if Gamestate == "Macalania" and StepCounter == 4:
        reportGamestate()
        FFX_mTemple.arrival()
        FFX_mTemple.startSeymourFight()
        FFX_mTemple.seymourFight()
        StepCounter = 5

    if Gamestate == "Macalania" and StepCounter == 5:
        reportGamestate()
        FFX_mTemple.trials()
        #Gamestate = "manualBreak" # Used for testing only.
        StepCounter = 6

    if Gamestate == "Macalania" and StepCounter == 6:
        reportGamestate()
        FFX_mTemple.escape()
        #FFX_mTemple.wendigoFight()
        StepCounter = 7
        #Gamestate = "manualBreak" # Used for testing only.
        
    if Gamestate == "Macalania" and StepCounter == 7:
        FFX_mTemple.underLake()
        StepCounter = 1
        Gamestate = "Home"
        #Gamestate = "manualBreak" # Used for testing only.

    if Gamestate == "Home" and StepCounter == 1:
        reportGamestate()
        FFX_home.desert()
        StepCounter = 2
        #Gamestate = "manualBreak" # Used for testing only.

    if Gamestate == "Home" and StepCounter == 2:
        reportGamestate()
        FFX_home.findSummoners()
        FFX_rescueYuna.preEvrae()
        StepCounter = 1
        Gamestate = "rescueYuna"
        #Gamestate = "manualBreak" # Used for testing only.

    if Gamestate == "rescueYuna" and StepCounter == 1:
        reportGamestate()
        FFX_Battle.Evrae()
        FFX_rescueYuna.guards()
        StepCounter = 2
        #Gamestate = "manualBreak" # Used for testing only.
        
    if Gamestate == "rescueYuna" and StepCounter == 2:
        reportGamestate()
        FFX_rescueYuna.trials()
        FFX_rescueYuna.trialsEnd()
        StepCounter = 3

    if Gamestate == "rescueYuna" and StepCounter == 3:
        reportGamestate()
        FFX_rescueYuna.ViaPurifico()
        StepCounter = 4

    if Gamestate == "rescueYuna" and StepCounter == 4:
        reportGamestate()
        FFX_rescueYuna.evraeAltana()
        #Gamestate = "manualBreak" # Used for testing only.
        StepCounter = 5

    if Gamestate == "rescueYuna" and StepCounter == 5:
        reportGamestate()
        FFX_rescueYuna.seymourNatus()
        StepCounter = 1
        Gamestate = "Gagazet"
        FFX_Logs.nextFile()
        #Gamestate = "manualBreak" # Used for testing only.

    if Gamestate == "Gagazet" and StepCounter == 1:
        reportGamestate()
        FFX_Gagazet.calmLands()
        FFX_Gagazet.defenderX()
        FFX_Gagazet.toTheRonso()
        StepCounter = 2

    if Gamestate == "Gagazet" and StepCounter == 2:
        reportGamestate()
        FFX_Gagazet.gagazetGates()
        FFX_Gagazet.Flux()
        StepCounter = 3
    if Gamestate == "Gagazet" and StepCounter == 3:
        reportGamestate()
        FFX_Gagazet.dream()
        StepCounter = 4

    if Gamestate == "Gagazet" and StepCounter == 4:
        reportGamestate()
        FFX_Gagazet.cave()
        FFX_Gagazet.wrapUp()
        StepCounter = 1
        Gamestate = "Zanarkand"

    if Gamestate == "Zanarkand" and StepCounter == 1:
        reportGamestate()
        FFX_Zanarkand.arrival()
        StepCounter = 2

    if Gamestate == "Zanarkand" and StepCounter == 2:
        reportGamestate()
        FFX_Zanarkand.trials()
        StepCounter = 3

    if Gamestate == "Zanarkand" and StepCounter == 3:
        reportGamestate()
        FFX_Zanarkand.sanctuaryKeeper()
        StepCounter = 4

    if Gamestate == "Zanarkand" and StepCounter == 4:
        reportGamestate()
        FFX_Zanarkand.yunalesca()
        StepCounter = 1
        Gamestate = "Sin"
        #Gamestate = "End" # Used for testing only.

    if Gamestate == "Sin" and StepCounter == 1:
        reportGamestate()
        FFX_Sin.makingPlans()
        StepCounter = 2

    if Gamestate == "Sin" and StepCounter == 2:
        reportGamestate()
        FFX_Sin.Shedinja()
        #FFX_Sin.auronWeap()
        FFX_Sin.facingSin()
        StepCounter = 3

    if Gamestate == "Sin" and StepCounter == 3:
        reportGamestate()
        FFX_Sin.insideSin()
        StepCounter = 4
    
    if Gamestate == "Sin" and StepCounter == 4:
        FFX_Sin.eggHunt(autoEggHunt)
        FFX_Battle.BFA()
        Gamestate = "End"

#print("Waiting for Yu Yevon to die.")
#FFX_memory.waitFrames(30 * 6)
print("Time! The game is now over.")

#except Exception as errMsg:
#    print("--------------------------------------------------")
#    print("Something went wrong during the run. Error:")
#    print(errMsg)
#    print("--------------------------------------------------")
#    FFX_memory.waitFrames(30 * 20)

endTime = FFX_Logs.timeStamp()
FFX_Logs.writeStats("End time:")
FFX_Logs.writeStats(str(endTime))

totalTime = endTime - startTime
FFX_Logs.writeStats("Total time:")
FFX_Logs.writeStats(str(totalTime))
print("The game duration was: ", str(totalTime))
FFX_memory.waitFrames(30 * 10)


FFX_memory.end()

print("Automation complete. Unplugging controller.")
import Reset_Controller
print("Unplugging complete. Shutting it down! Have a great day!")