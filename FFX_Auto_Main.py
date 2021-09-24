# Libraries and Core Files
import time
import FFX_Logs
#import FFX_core
import FFX_Screen
import FFX_Battle
import FFX_Xbox
FFXC = FFX_Xbox.FFXC

#Gamestate, "none" for new game, or set to a specific section to start from the first save.
#See the if statement tree below to determine starting position for Gamestate.
#Gamestate = "MRR"
#StepCounter = 1
#Gamestate = "Djose"
#StepCounter = 1
Gamestate = "none"
StepCounter = 1

#Game length. Full is the same as any%, short is about 35 minutes with memory manip.
#gameLength = "short"
gameLength = "full"
forceBlitzWin = True
autoEggHunt = True
print("Game type will be: ", gameLength)

#Other variables
speedCount = 0
strengthCount = 0
endGameVersion = 0
gems = 0 #Set to 2 if loading in after Evrae Altana with two gems
earlyTidusGrid = False
if forceBlitzWin == True:
    blitzWin = True
else:
    blitzWin = False

#Main functions
def reportGamestate():
    
    global Gamestate
    global StepCounter
    logText = "Gamestate: " + Gamestate + " : StepCounter: " + str(StepCounter)
    FFX_Logs.writeLog(logText + "\n")
    FFX_Screen.clearMouse(0)

#Main
print("FFX automation starting")
FFX_Logs.nextFile()
FFX_Logs.nextStats()
print("Please launch the game now.")
#time.sleep(5)
#print("Now attempting to activate FFX window")
reportGamestate()

#Press Start until the main menu comes up
#---------- MAKE SURE THIS IS ON FOR A FRESH RUN --------------------
while not FFX_Screen.PixelTest(1076,552,(157, 159, 157)):
    FFXC.set_value('BtnStart', 1)
    time.sleep(0.1)
    FFXC.set_value('BtnStart', 0)

print("Game start screen")
FFX_Screen.clearMouse(0)

#Initiate memory reading, after we know the game is open.
import FFX_memory
FFX_memory.start()

#Next, check if we are loading to a save file
if Gamestate != "none" :
    FFX_Logs.writeLog("Loading to a specific gamestate.\n")
    startTime = FFX_Logs.timeStamp()
    FFX_Logs.writeStats("Start time:")
    FFX_Logs.writeStats(str(startTime))
    reportGamestate()
    import FFX_LoadGame
    
    if Gamestate == "Baaj" and StepCounter == 1:
        FFX_LoadGame.LoadBaaj()
    if Gamestate == "Baaj" and StepCounter == 5:
        FFX_LoadGame.LoadFirst()
    if Gamestate == "Besaid" and StepCounter == 1 : #Save pop-up after falling off of Rikku's boat
        FFX_LoadGame.loadOffset(45)
    if Gamestate == "Besaid" and StepCounter == 2 : #Crusader's lodge before trials start
        FFX_LoadGame.BesaidTrials()
    if Gamestate == "Besaid" and StepCounter == 3 : #Crusader's lodge after "Enough, Wakka!"
        FFX_LoadGame.loadOffset(25)
    if Gamestate == "Boat1" : #Besaid beach before boarding SS Liki ( nice alliteration :D )
        FFX_LoadGame.Boat1()
    if Gamestate == "Kilika" and StepCounter == 1: #Just after entering the woods
        FFX_LoadGame.loadOffset(22)
    if Gamestate == "Kilika" and StepCounter == 3: #Temple save sphere before scene with Donna
        FFX_LoadGame.KilikaTrials()
    if Gamestate == "Luca" and StepCounter == 1: # Approaching Luca via boat
        FFX_LoadGame.loadOffset(37)
    if Gamestate == "Luca" and StepCounter == 3: # after Oblitzerator, before Blitzball
        FFX_LoadGame.loadOffset(9)
    if Gamestate == "Luca" and StepCounter == 5: # After Blitzball, before battles.
        FFX_LoadGame.loadOffsetBattle(7)
        earlyHaste = 1
    #if Gamestate == "Luca" and StepCounter == 6: #After the talk with Auron
    #    FFX_LoadGame.loadPostBlitz()
    if Gamestate == "Miihen" and StepCounter == 1: #After the talk with Auron
        FFX_LoadGame.LoadMiihenStart()
    if Gamestate == "MRR" and StepCounter == 1: #Mi'ihen North after meeting Seymour
        FFX_LoadGame.loadOffset(17)
        FFX_LoadGame.LoadMRR()
    if Gamestate == "MRR" and StepCounter == 2: #Just before the last lift to the battle site
        FFX_LoadGame.LoadMRR2()
    if Gamestate == "Djose" and StepCounter == 1: # Aftermath, after talking to Seymour and then Auron
        FFX_LoadGame.AfterGui()
    if Gamestate == "Djose" and StepCounter == 2: #Just before the Djose temple
        FFX_LoadGame.djoseTemple()
    if Gamestate == "Moonflow" and StepCounter == 2: #North bank, before Rikku
        FFX_LoadGame.moonflow2()
    if Gamestate == "Guadosalam" and StepCounter == 2: #After the Farplane
        loadOffset(1)
        FFX_LoadGame.loadGuadoSkip()
    if Gamestate == "Macalania" and StepCounter == 1: #1 = south, 2 = north
        FFX_LoadGame.loadOffset(6)
    if Gamestate == "Macalania" and StepCounter == 2: #1 = south, 2 = north
        FFX_LoadGame.loadOffset(7)
    if Gamestate == "Macalania" and StepCounter == 3: #between Spherimorph and Crawler. Move to lake
        FFX_LoadGame.loadMacLake()
    if Gamestate == "Macalania" and StepCounter == 4: #Right before Jyscal skip
        FFX_LoadGame.loadMacTemple()
    if Gamestate == "Macalania" and StepCounter == 5: #After Seymour, before trials
        FFX_LoadGame.loadMacTemple2()
    if Gamestate == "Macalania" and StepCounter == 6: #Outside temple, before escaping.
        FFX_LoadGame.loadOffset(15)
        time.sleep(0.5)
        FFXC.set_value('AxisLy', 1)
        time.sleep(1.5)
        FFXC.set_value('AxisLy', 0)
        time.sleep(0.5)
    if Gamestate == "Macalania" and StepCounter == 7: #Before Wendigo
        FFX_LoadGame.loadWendigo()
    if Gamestate == "Home" and StepCounter == 1:
        FFX_LoadGame.loadOffset(99)
    if Gamestate == "Home" and StepCounter == 2:
        FFX_LoadGame.loadOffset(4)
    if Gamestate == "rescueYuna" and StepCounter == 1: # Airship, before pathing to the deck
        FFX_LoadGame.loadRescue()
    if Gamestate == "rescueYuna" and StepCounter == 2: # Bevelle trials
        FFX_LoadGame.loadBahamut()
    if Gamestate == "rescueYuna" and StepCounter == 5: # Highbridge before Seymour Natus
        FFX_LoadGame.loadOffset(4)
    if Gamestate == "Gagazet" and StepCounter == 1: # Just before Calm Lands
        FFX_LoadGame.loadCalm()
    if Gamestate == "Gagazet" and StepCounter == 2: # Gagazet gates
        FFX_LoadGame.loadGagaGates()
    if Gamestate == "Gagazet" and StepCounter == 3: # Just before Seymour Flux
        FFX_LoadGame.LoadNeutral()
    if Gamestate == "Gagazet" and StepCounter == 4: # After the dream
        FFX_LoadGame.loadGagazetDream()
    if Gamestate == "Zanarkand" and StepCounter == 1: # Intro scene revisited
        FFX_LoadGame.zanEntrance()
    if Gamestate == "Zanarkand" and StepCounter == 2: # Just before the trials.
        FFX_LoadGame.zanTrials()
    if Gamestate == "Zanarkand" and StepCounter == 4: # After Sanctuary Keeper
        FFX_LoadGame.loadOffset(1)
    if Gamestate == "Sin" and StepCounter == 2: #Save sphere on the Highbridge before talking to Shedinja
        FFX_LoadGame.loadOffset(22)
    if Gamestate == "Sin" and StepCounter == 3: #Before "inside sin" pathing
        FFX_LoadGame.loadOffset(2)
        

#Movement files
import FFX_DreamZan
if gameLength != "short":
    import FFX_Baaj
    import FFX_Besaid1
    import FFX_Besaid2
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

try:

    #Start of the game, start of Dream Zanarkand section
    if Gamestate == "none" and StepCounter == 1:
        reportGamestate()
        Gamestate = "DreamZan"
        time.sleep(0.5)
        FFX_DreamZan.NewGame(gameLength)
        startTime = FFX_Logs.timeStamp()
        FFX_Logs.writeStats("Start time:")
        FFX_Logs.writeStats(str(startTime))
        print("Timer starts now.")
        FFX_DreamZan.listenStory(gameLength)
        #Start of the game, up through Sinspawn Ammes fight
        StepCounter = 2
        #if gameLength == "short":
        #    FFX_DreamZan.ammesBattleShort()
        #else:
        FFX_DreamZan.ammesBattle()
            

    if Gamestate == "DreamZan" and StepCounter == 2:
        reportGamestate()
        FFX_Battle.Ammes()
        #Finishes Sinspawn Ammes fight
        
        StepCounter = 3
        reportGamestate()

    if Gamestate == "DreamZan" and StepCounter == 3:
        FFX_DreamZan.AfterAmmes()
        
        #if gameLength == "short":
        #    FFX_Battle.TankerShort()
        #else:
        FFX_Battle.Tanker()
        
        #Sin drops us near Baaj temple.
        StepCounter = 4
        reportGamestate()
        
    if Gamestate == "DreamZan" and StepCounter == 4:
        if gameLength == "short":
            FFX_DreamZan.SwimToJecht_shortGame()
            Gamestate = "shortGame"
            StepCounter = 1
        else:
            FFX_DreamZan.SwimToJecht()
            Gamestate = "Baaj"
            StepCounter = 1

    if Gamestate == "shortGame" and StepCounter == 1:
        #Only for the short game. Run these pieces then skip down to the last Sin section.
        #If not a short game, continue as regular to the Baaj sections.
        import FFX_cheater_cheese
        FFX_cheater_cheese.BaajEntrance()
        FFX_cheater_cheese.sphereGrid()
        FFX_cheater_cheese.items()
        FFX_cheater_cheese.BackToSin()
        FFX_Sin.insideSin(gameLength, autoEggHunt)
        FFX_Battle.BFA_TASonly()
        Gamestate = "gameOver"
        stepCounter = 999

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
        FFX_Besaid2.trials()
        FFX_Besaid2.aeonAndSleep()
        StepCounter = 3
        reportGamestate()

    if Gamestate == "Besaid" and StepCounter == 3 :
        earlyTidusGrid = FFX_Besaid2.leaving()
        FFX_Besaid2.waterfalls()
        
        Gamestate = "Boat1"
        StepCounter = 1
        reportGamestate()

    if Gamestate == "Boat1" :
        reportGamestate()
        FFX_Boats.ssLiki(earlyTidusGrid)
        FFX_Kilika.arrival()
        Gamestate = "Kilika"

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
        Gamestate = "Luca"

    if Gamestate == "Luca" and StepCounter == 1:
        reportGamestate()
        FFX_Luca.arrival()
        FFX_Luca.followYuna()
        StepCounter = 2

    if Gamestate == "Luca" and StepCounter == 2:
        reportGamestate()
        earlyHaste = FFX_Luca.preBlitz()
        StepCounter = 3

    if Gamestate == "Luca" and StepCounter == 3:
        reportGamestate()
        FFX_Luca.blitzStart()
        StepCounter = 4

    if Gamestate == "Luca" and StepCounter == 4:
        reportGamestate()
        blitzWin = FFX_Blitz.blitzMain(forceBlitzWin)
        FFX_Screen.awaitSave()
        StepCounter = 5
        

    if Gamestate == "Luca" and StepCounter == 5:
        reportGamestate()
        FFX_Luca.afterBlitz(earlyHaste)
        StepCounter = 1
        Gamestate = "Miihen"
        #Gamestate = "manualBreak" # Used for testing only.

    if Gamestate == "Miihen" and StepCounter == 1:
        reportGamestate()
        selfDestruct = FFX_Miihen.arrival()
        FFX_Miihen.midPoint()
        print("End of Miihen mid point section.")
        FFX_Miihen.lowRoad(selfDestruct)
        StepCounter = 2

    if Gamestate == "Miihen" and StepCounter == 2:
        reportGamestate()
        FFX_Miihen.wrapUp()
        StepCounter = 1
        Gamestate = "MRR"
        FFX_Logs.nextFile()
        
    if Gamestate == "MRR" and StepCounter == 1:
        reportGamestate()
        wakkaLateMenu = FFX_MRR.arrival()
        FFX_MRR.mainPath(wakkaLateMenu)
        StepCounter = 2
        #Gamestate = "manualBreak" # Used for testing only.

    if Gamestate == "MRR" and StepCounter == 2:
        reportGamestate()
        success = FFX_MRR.battleSite()
        if success == 2:
            Gamestate = "Error"
            reportGamestate()
            time.sleep(90)
        if success == 1:
            Gamestate = "Djose"
            StepCounter = 1
        FFX_Logs.nextFile()

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
        status = [False,False,False,False]
        reportGamestate()
        status = FFX_ThunderPlains.southPathing(blitzWin)
        StepCounter = 2

    if Gamestate == "ThunderPlains" and StepCounter == 2:
        FFX_ThunderPlains.agency(blitzWin)
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
        FFX_mWoods.afterCrawler()
        StepCounter = 4
        #Gamestate = "manualBreak" # Used for testing only.

    if Gamestate == "Macalania" and StepCounter == 4:
        reportGamestate()
        FFX_mTemple.arrival(blitzWin)
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
        FFX_mTemple.wendigoFight()
        StepCounter = 7
        #Gamestate = "manualBreak" # Used for testing only.
        
    if Gamestate == "Macalania" and StepCounter == 7:
        FFX_mTemple.underLake()
        StepCounter = 1
        Gamestate = "Home"
        #Gamestate = "manualBreak" # Used for testing only.

    if Gamestate == "Home" and StepCounter == 1:
        reportGamestate()
        FFX_home.desert1()
        StepCounter = 2
        #Gamestate = "manualBreak" # Used for testing only.

    if Gamestate == "Home" and StepCounter == 2:
        reportGamestate()
        FFX_home.findSummoners(blitzWin)
        FFX_rescueYuna.preEvrae()
        StepCounter = 1
        Gamestate = "rescueYuna"
        #Gamestate = "manualBreak" # Used for testing only.

    if Gamestate == "rescueYuna" and StepCounter == 1:
        reportGamestate()
        FFX_rescueYuna.Evrae()
        FFX_rescueYuna.guards()
        StepCounter = 2
        #Gamestate = "manualBreak" # Used for testing only.
        
    if Gamestate == "rescueYuna" and StepCounter == 2:
        reportGamestate()
        FFX_rescueYuna.trials()
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
        FFX_rescueYuna.seymourNatus(blitzWin)
        StepCounter = 1
        Gamestate = "Gagazet"
        FFX_Logs.nextFile()
        #Gamestate = "manualBreak" # Used for testing only.

    if Gamestate == "Gagazet" and StepCounter == 1:
        reportGamestate()
        FFX_Gagazet.calmLands(blitzWin)
        FFX_Gagazet.defenderX()
        FFX_Gagazet.toTheRonso()
        StepCounter = 2

    if Gamestate == "Gagazet" and StepCounter == 2:
        reportGamestate()
        endGameVersion = FFX_Gagazet.gagazetGates(blitzWin)
        FFX_Gagazet.afterFlux()
        StepCounter = 3

    #In case we're loading mid game...
    if endGameVersion == 0:
        endGameVersion = 4
        # 1 = two Return spheres, two Friend spheres
        # 2 = two Return spheres, two Friend spheres
        # 3 = Game over (four Friend spheres)
        # 4 = four Return spheres

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
        if endGameVersion == 0:
            endGameVersion = 1 #Used during segmented testing.
            # 4 == four Return spheres
            # 3 == four Friend spheres
            # 1 or 2 == two of each.
        FFX_Zanarkand.sanctuaryKeeper(endGameVersion)
        StepCounter = 4

    if Gamestate == "Zanarkand" and StepCounter == 4:
        reportGamestate()
        FFX_Zanarkand.yunalesca()
        StepCounter = 1
        Gamestate = "Sin"

    if Gamestate == "Sin" and StepCounter == 1:
        reportGamestate()
        FFX_Sin.makingPlans()
        StepCounter = 2

    print("Mark1")
    if Gamestate == "Sin" and StepCounter == 2:
        reportGamestate()
        FFX_Sin.Shedinja()
        #FFX_Sin.auronWeap()
        FFX_Sin.facingSin()
        StepCounter = 3

    print("Mark2")
    if Gamestate == "Sin" and StepCounter == 3:
        reportGamestate()
        FFX_Sin.insideSin(gameLength, autoEggHunt)
        FFX_Battle.BFA()
        StepCounter = 4
    print("Mark3")

    #print("Waiting for Yu Yevon to die.")
    #time.sleep(6)
    print("Time! The game is now over.")

except Exception as errMsg:
    print("--------------------------------------------------")
    print("Something went wrong during the run. Error:")
    print(errMsg)
    print("--------------------------------------------------")
    time.sleep(20)
    FFXC.set_value('AxisLx',0)
    FFXC.set_value('AxisLy',0)
    FFXC.set_value('BtnB',0)
    FFXC.set_value('BtnA',0)
    FFXC.set_value('BtnX',0)
    FFXC.set_value('BtnY',0)
    FFXC.set_value('Dpad', 0)
    FFXC.set_value('BtnShoulderL', 0)
    FFXC.set_value('BtnShoulderR', 0)

endTime = FFX_Logs.timeStamp()
FFX_Logs.writeStats("End time:")
FFX_Logs.writeStats(str(endTime))

totalTime = endTime - startTime
FFX_Logs.writeStats("Total time:")
FFX_Logs.writeStats(str(totalTime))
print("The game duration was: ", str(totalTime))
time.sleep(10)


FFX_memory.end()
try:
    FFX_Screen.clickImage("stop_recording.JPG")
except:
    print("Could not stop recording.")

print("Automation complete. Unplugging controller.")
import Reset_Controller
print("Unplugging complete. Shutting it down! Have a great day!")