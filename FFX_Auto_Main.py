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

if gameVars.nemesis():
    import FFX_nemesisChanges
    import FFX_nem_arenaPrep
    import FFX_nem_arenaBattles

#Gamestate, "none" for new game, or set to a specific section to start from the first save.
#See the if statement tree below to determine starting position for Gamestate.
#These are the popular ones. New Game ('none') is the last one.
#Gamestate = "Baaj"
#StepCounter = 1
#StepCounter = 6
#Gamestate = "Besaid"
#StepCounter = 3
#Gamestate = "Kilika"
#StepCounter = 1
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
Gamestate = "rescueYuna"
#StepCounter = 1 #Blitz Win, short two power and speed spheres for testing.
#StepCounter = 2
StepCounter = 5 #Can pick regular run vs nemesis below.
#Gamestate = "Gagazet"
#StepCounter = 1 #Blitz Win, no end game version selected
#StepCounter = 2 #NE armor testing
#StepCounter = 3 #After B&Y, supports all four versions, choose down below. Blitz Win/Loss also.
#StepCounter = 6 #After Flux/Dream. Can select version 3 or 4 below.
#StepCounter = 10 #Nemesis variant, blitz win logic (not working)
#StepCounter = 11 #Remiem racing
#Gamestate = "Zanarkand"
#StepCounter = 3 #Blitz win, end game version 1 or 2
#StepCounter = 4 #Before Yunalesca
#StepCounter = 5 #After Yunalesca
#Gamestate = "Sin"
#StepCounter = 2 #Shedinja Highbridge
#StepCounter = 3 #Before Sea of Sorrows
#StepCounter = 4 #Before point of no return, with zombiestrike weapons (not Kimahri)
Gamestate = "none"
StepCounter = 1

#Nemesis load testing
#Gamestate = "Nem_Farm"
#StepCounter = 2 #Start of Calm Lands (only one each)
#StepCounter = 3
#StepCounter = 20 #After Gagazet, before Calm Lands farm
#StepCounter = 22 #Before Sin/Omega farms, AFTER picking up oneMP weapon
#StepCounter = 24 #Final Prep before arena bosses


####################################################################################################
#RNG - Using Rossy's FFX.exe fix, this allows us to choose the RNG seed we want. From 0-255

forceBlitzWin = False
seedHunt = False #Update this to decide new seed or known seed
rngSeedNum = 255 #New seed number, only used if doing seed hunt.
rngSelectArray = [31,41,157,182,224]
goodSeeds = [31,41,157,160,182,224]
#160 is WR for both categories, but otherwise rather unimpressive.
#182, needs improved Spherimorph logic.
#224 do not switch on Sandragora.
secondLook = [18,24,44,52,96,105,138,200,232,254]
####################################################################################################

if Gamestate == "Luca" and StepCounter == 3:
    blitzTesting = True
    gameLength = "Testing Blitzball only"
elif Gamestate != "none":
    rngSeedNum = 255 #Select a specific seed.
    rngReviewOnly = False
    gameLength = "Loading mid point for testing."
    blitzTesting = False
elif seedHunt == False: #Below logic for full runs only.
    rngSeedNum = random.choice(rngSelectArray) #Select a favorite seed randomly
    rngSeedNum = 31 #Manually choose seed here.
    #Current WR is on seed 160 for both any% and CSR%
    rngReviewOnly = False
    gameLength = "Full Run"
    blitzTesting = False
else: #Just to make sure we're running from new game for seed finding.
    StepCounter = 1
    rngReviewOnly = True
    gameLength = "Seed Hunt"
    blitzTesting = False

print("Game type will be: ", gameLength)
maxLoops = 25

#Other variables
rngSeedOrig = rngSeedNum
speedCount = 0
strengthCount = 0
gems = 0 #Set to 2 if loading in after Evrae Altana with two gems
autoEggHunt = True
specialZanLoad = False

#Main functions
def reportGamestate():
    
    global Gamestate
    global StepCounter
    #logText = "Gamestate: " + Gamestate + " : StepCounter: " + str(StepCounter)
    #FFX_Logs.writeLog(logText + "\n")
    FFX_Screen.clearMouse(0)

#Initiate memory reading, after we know the game is open.
#import FFX_memory
FFX_memory.start()

#Main
import FFX_Logs
print("FFX automation starting")
print("Please launch the game now.")
#FFX_memory.waitFrames(30 * 5)
#print("Now attempting to activate FFX window")
reportGamestate()

print("Game start screen")
FFX_Screen.clearMouse(0)

#FFX_memory.setRngSeed(rngSeedNum) #Using Rossy's FFX.exe fix, this allows us to choose the RNG seed we want. From 0-255

#Next, check if we are loading to a save file
if Gamestate != "none" :
    if not (Gamestate == "Luca" and StepCounter == 3):

        FFX_DreamZan.NewGame(Gamestate)
        rngSeed = FFX_memory.rngSeed()
        print("---RNG seed: ", rngSeed)
        FFX_Logs.nextStats(rngSeed)
        FFX_Logs.writeStats("RNG seed:")
        FFX_Logs.writeStats(rngSeed)
        startTime = FFX_Logs.timeStamp()
        reportGamestate()
    import FFX_LoadGame
    
    #Need to update these to use FFX_LoadGame.loadSaveNum(number) for all.
    
    if Gamestate == "Baaj" and StepCounter == 1:
        FFX_LoadGame.loadSaveNum(40)
        #FFX_LoadGame.LoadBaaj()
    if Gamestate == "Besaid" and StepCounter == 1 : #Save pop-up after falling off of Rikku's boat
        FFX_LoadGame.loadSaveNum(111)
    if Gamestate == "Besaid" and StepCounter == 3 : #Crusader's lodge after "Enough, Wakka!"
        FFX_LoadGame.loadSaveNum(39)
        print("Load complete")
        FFX_LoadGame.loadMemCursor()
        while FFX_memory.userControl():
            if FFX_memory.getCoords()[0] > 0.5:
                FFXC.set_movement(1, 1)
            else:
                FFXC.set_movement(0, 1)
        print("Ready for regular path")
    if Gamestate == "Boat1" : #Besaid beach before boarding SS Liki ( nice alliteration :D )
        FFX_LoadGame.loadSaveNum(31)
        FFX_LoadGame.Boat1()
    if Gamestate == "Kilika" and StepCounter == 1: #Just after entering the woods
        FFX_LoadGame.loadSaveNum(22)
        FFXC.set_movement(0, 1)
        FFX_memory.waitFrames(30 * 5)
        FFXC.set_neutral()
    if Gamestate == "Luca" and StepCounter == 1: # Approaching Luca via boat
        FFX_LoadGame.loadSaveNum(112)
    if Gamestate == "Luca" and StepCounter == 5: # Approaching Luca via boat
        FFX_LoadGame.loadSaveNum(5)
    if Gamestate == "Miihen" and StepCounter == 1: #After the talk with Auron
        #FFX_LoadGame.loadSaveNum(26) #W/O laughing scene
        FFX_LoadGame.loadSaveNum(16) #With laughing scene
        #FFX_LoadGame.LoadMiihenStart()
        FFX_LoadGame.LoadMiihenStart_Laugh()
        #FFX_memory.setEncounterRate(0)
    if Gamestate == "MRR" and StepCounter == 1: #Mi'ihen North after meeting Seymour
        
        FFX_LoadGame.loadSaveNum(38)
        FFX_memory.setGilvalue(4000) #Fixes a low gil state for this save file.
        FFX_LoadGame.LoadMRR()
    if Gamestate == "Djose" and StepCounter == 1: # Aftermath, after talking to Seymour and then Auron
        FFX_LoadGame.loadSaveNum(27)
        FFX_LoadGame.AfterGui()
        #FFX_memory.setEncounterRate(0)
    if Gamestate == "Moonflow" and StepCounter == 2: #North bank, before Rikku
        FFX_LoadGame.loadSaveNum(2)
        FFX_LoadGame.moonflow2()
    if Gamestate == "Guadosalam" and StepCounter == 2: #After the Farplane
        FFX_LoadGame.loadSaveNum(3)
        FFX_LoadGame.loadGuadoSkip()
    if Gamestate == "Macalania" and StepCounter == 1: #1 = south, 2 = north
        FFX_LoadGame.loadSaveNum(9)
    if Gamestate == "Macalania" and StepCounter == 2: #1 = south, 2 = north
        FFX_LoadGame.loadSaveNum(7)
    if Gamestate == "Macalania" and StepCounter == 4: #Right before Jyscal skip
        FFX_LoadGame.loadSaveNum(10) #No remedy in inventory, likely game over.
        FFX_LoadGame.loadMacTemple()
    if Gamestate == "Macalania" and StepCounter == 6: #Outside temple, before escaping.
        FFX_LoadGame.loadSaveNum(41)
        FFX_LoadGame.loadMacTemple2()
    if Gamestate == "Home" and StepCounter == 1:
        FFX_LoadGame.loadSaveNum(60)
    if Gamestate == "Home" and StepCounter == 2:
        FFX_LoadGame.loadSaveNum(11)
    if Gamestate == "rescueYuna" and StepCounter == 1: # Airship, first movement.
        #FFX_LoadGame.loadSaveNum(55) #Blitz Win, normal save.
        FFX_LoadGame.loadSaveNum(56) #Blitz Win, save less speed/power spheres
    if Gamestate == "rescueYuna" and StepCounter == 2: # Bevelle trials
        FFX_LoadGame.loadSaveNum(15)
    if Gamestate == "rescueYuna" and StepCounter == 5: # Highbridge before Seymour Natus
        #FFX_LoadGame.loadSaveNum(42) #Regular
        FFX_LoadGame.loadSaveNum(67) #Nemesis
    if Gamestate == "Gagazet" and StepCounter == 1: # Just before Calm Lands
        FFX_LoadGame.loadSaveNum(43)
        FFX_LoadGame.loadCalm()
        gameVars.setBlitzWin(True)
    if Gamestate == "Gagazet" and StepCounter == 2: # NE armor save
        FFX_LoadGame.loadSaveNum(57)
    if Gamestate == "Gagazet" and StepCounter == 3: # Gagazet gates, after B&Y
        #FFX_LoadGame.loadSaveNum(138) #Blitz Win
        FFX_LoadGame.loadSaveNum(53) #Blitz Loss
        gameVars.endGameVersionSet(3)
        FFX_LoadGame.loadGagaGates()
    if Gamestate == "Gagazet" and StepCounter == 6: # After the dream
        #FFX_LoadGame.loadSaveNum(47)
        #gameVars.endGameVersionSet(4)
        FFX_LoadGame.loadSaveNum(52)
        gameVars.endGameVersionSet(3)
        FFX_LoadGame.loadGagazetDream()
    if Gamestate == "Gagazet" and StepCounter == 10: # Calm Lands, but Nemesis version
        FFX_LoadGame.loadSaveNum(43)
        FFX_LoadGame.loadCalm()
    if Gamestate == "Gagazet" and StepCounter == 11: # Calm Lands, but Nemesis version
        FFX_LoadGame.loadSaveNum(64)
        FFXC.set_movement(1, 0)
        FFX_memory.waitFrames(60)
        FFXC.set_movement(0, 1)
        FFX_memory.waitFrames(60)
        FFXC.set_neutral()
        import FFX_menu
        FFX_menu.prepCalmLands()
    if Gamestate == "Zanarkand" and StepCounter == 1: # Intro scene revisited
        FFX_LoadGame.loadOffset(19)
        FFX_LoadGame.zanEntrance()
    if Gamestate == "Zanarkand" and StepCounter == 2: # Just before the trials.
        FFX_LoadGame.loadOffset(35)
        FFX_LoadGame.zanTrials()
    if Gamestate == "Zanarkand" and StepCounter == 3: # After trials, before boss
        FFX_LoadGame.loadSaveNum(45)
        gameVars.endGameVersionSet(4)
        #FFX_LoadGame.zanTrials()
    if Gamestate == "Zanarkand" and StepCounter == 4: # After Sanctuary Keeper
        FFX_LoadGame.loadSaveNum(44)
    if Gamestate == "Zanarkand" and StepCounter == 5: # After Yunalesca
        FFX_LoadGame.loadSaveNum(48)
        specialZanLoad = True
    if Gamestate == "Sin" and StepCounter == 2: #Save sphere on the Highbridge before talking to Shedinja
        #FFX_LoadGame.loadSaveNum(49)
        FFX_LoadGame.loadSaveNum(70) #Nemesis logic, double friend sphere drops from B&Y
        while FFX_memory.oakaGilCursor() != 20:
            if FFX_memory.userControl():
                import FFX_targetPathing
                FFX_targetPathing.setMovement([-251,340])
            else:
                FFXC.set_neutral()
            FFX_Xbox.menuB()
        FFX_memory.checkNEArmor()
    if Gamestate == "Sin" and StepCounter == 3: #Start of "Sea of Sorrows" section
        FFX_LoadGame.loadSaveNum(50)
    if Gamestate == "Sin" and StepCounter == 4: #Before point of no return
        #This save has zombiestrike weapons for all except Kimahri
        #Please use for egg hunt and zombie weapon testing.
        FFX_LoadGame.loadSaveNum(51)
        gameVars.setZombie(5)
        FFX_LoadGame.loadEggHunt()
    
    #Nemesis run loads
    if Gamestate == "Nem_Farm" and StepCounter == 1:
        FFX_LoadGame.loadSaveNum(66)
    if Gamestate == "Nem_Farm" and StepCounter == 2:
        FFX_LoadGame.loadSaveNum(69)
    if Gamestate == "Nem_Farm" and StepCounter == 3:
        FFX_LoadGame.loadSaveNum(84)
        gameVars.setNemChecpointAP(3) #See FFX_nem_menu
        #import FFX_nem_arenaPrep
        FFX_nem_arenaPrep.arenaReturn()
    if Gamestate == "Nem_Farm" and StepCounter == 5:
        FFX_LoadGame.loadSaveNum(71)
    if Gamestate == "Nem_Farm" and StepCounter == 6:
        FFX_LoadGame.loadSaveNum(72)
    if Gamestate == "Nem_Farm" and StepCounter == 8:
        FFX_LoadGame.loadSaveNum(73)
    if Gamestate == "Nem_Farm" and StepCounter == 9:
        FFX_LoadGame.loadSaveNum(75)
        gameVars.setNemChecpointAP(3) #See FFX_nem_menu
    if Gamestate == "Nem_Farm" and StepCounter == 14:
        FFX_LoadGame.loadSaveNum(76)
        gameVars.setNemChecpointAP(11) #See FFX_nem_menu
    if Gamestate == "Nem_Farm" and StepCounter == 17:
        FFX_LoadGame.loadSaveNum(77)
        gameVars.setNemChecpointAP(20) #See FFX_nem_menu
    if Gamestate == "Nem_Farm" and StepCounter == 21:
        FFX_LoadGame.loadSaveNum(79)
        FFX_nem_arenaPrep.arenaReturn()
        gameVars.setNemChecpointAP(27) #See FFX_nem_menu
    if Gamestate == "Nem_Farm" and StepCounter == 22:
        FFX_LoadGame.loadSaveNum(82)
        import FFX_nem_menu
        FFX_nem_menu.rikkuHaste()
        gameVars.setNemChecpointAP(30) #See FFX_nem_menu
    if Gamestate == "Nem_Farm" and StepCounter == 23:
        FFX_LoadGame.loadSaveNum(80)
        gameVars.setNemChecpointAP(30) #See FFX_nem_menu
    if Gamestate == "Nem_Farm" and StepCounter == 24:
        FFX_LoadGame.loadSaveNum(81)
        gameVars.setNemChecpointAP(30)
        gameVars.setNemChecpointAP(30) #See FFX_nem_menu
    if Gamestate == "Nem_Farm" and StepCounter == 20:
        FFX_LoadGame.loadSaveNum(85)
        gameVars.setNemChecpointAP(30)
    
    if Gamestate == "Nem_Farm":
        FFX_memory.checkNEArmor()
    

#Movement files - moved to FFX_compileAll.py

#try:
rikkucharged = 0

while Gamestate != "End":

    #Blitzball testing logic
    if Gamestate == "Luca" and StepCounter == 3:
        FFX_DreamZan.NewGame(Gamestate)

        FFX_Logs.writeLog("Loading to a specific gamestate.\n")
        FFX_LoadGame.loadSaveNum(37)
        #FFX_memory.setRNG2()

        
    
    if rngSeedNum >= 256:
        Gamestate = "End"

    #Start of the game, start of Dream Zanarkand section
    if Gamestate == "none" and StepCounter == 1:
        reportGamestate()
        FFX_DreamZan.NewGame(Gamestate)

        gameVars.setStartVars()
        Gamestate = "DreamZan"
        FFX_memory.waitFrames(30 * 0.5)
        FFX_DreamZan.NewGame2()
        startTime = FFX_Logs.timeStamp()
        print("Timer starts now.")
        FFX_DreamZan.listenStory()
        rngSeed = FFX_memory.rngSeed()
        print("---RNG seed: ", rngSeed)
        FFX_Logs.nextStats(rngSeed)
        FFX_Logs.writeStats("RNG seed:")
        FFX_Logs.writeStats(rngSeed)
        FFX_Logs.writeStats("Start time:")
        FFX_Logs.writeStats(str(startTime))
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
        if rngSeedNum == 255:
            StepCounter = 3
        elif rngReviewOnly == True and rngSeedNum - rngSeedOrig < maxLoops: # Used to run multiple tests via a single execution
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
            if rngSeedNum in rngSelectArray:
                while rngSeedNum in rngSelectArray:
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
        print("------Blitz Start")
        FFX_Blitz.blitzMain(forceBlitzWin)
        print("------Blitz End")
        if not gameVars.csr():
            FFX_Xbox.awaitSave()
        
        if blitzTesting == True: # Used to run multiple tests, Blitzball only
            FFXC.set_neutral()
            print("------------------------------------------")
            print("------------------------------------------")
            print("Resetting")
            print("------------------------------------------")
            print("------------------------------------------")
            FFX_Screen.awaitTurn()
            import FFX_Reset
            #FFX_memory.clickToControl()
            StepCounter = 3
            
            
            #FFX_Logs.writeStats("Test duration:")
            #FFX_Logs.writeStats(totalTime)
            FFX_memory.waitFrames(30 * 2)

            FFX_Reset.resetToMainMenu()
            time.sleep(3)
        else:
            print("------------------------------------------")
            print("------------------------------------------")
            print("Post-Blitz")
            print("------------------------------------------")
            print("------------------------------------------")
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
        
        if rngSeedNum == 255:
            Gamestate = "MRR"
            StepCounter = 1
        elif rngReviewOnly == True and rngSeedNum - rngSeedOrig < maxLoops: # Used to run multiple tests via a single execution
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
        reportGamestate()
        status = FFX_ThunderPlains.southPathing()
        StepCounter = 2

    if Gamestate == "ThunderPlains" and StepCounter == 2:
        FFX_ThunderPlains.agency()
        StepCounter = 3

    if Gamestate == "ThunderPlains" and StepCounter == 3:
        FFX_ThunderPlains.northPathing()
        Gamestate = "Macalania"
        StepCounter = 1

    if Gamestate == "Macalania" and StepCounter == 1:
        reportGamestate()
        FFX_mWoods.arrival(False)
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
        #Gamestate = "End" # Used for testing only.

    if Gamestate == "Home" and StepCounter == 1:
        reportGamestate()
        FFX_home.desert()
        StepCounter = 2
        #Gamestate = "manualBreak" # Used for testing only.

    if Gamestate == "Home" and StepCounter == 2:
        reportGamestate()
        FFX_home.findSummoners()
        StepCounter = 1
        Gamestate = "rescueYuna"
        #Gamestate = "manualBreak" # Used for testing only.

    if Gamestate == "rescueYuna" and StepCounter == 1:
        reportGamestate()
        FFX_rescueYuna.preEvrae()
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
        Gamestate = "Gagazet"
        if gameVars.nemesis():
            StepCounter = 10
        else:
            StepCounter = 1

    if Gamestate == "Gagazet" and StepCounter == 1:
        reportGamestate()
        FFX_Gagazet.calmLands()
        FFX_Gagazet.defenderX()
        StepCounter = 2
        
    if Gamestate == "Gagazet" and StepCounter == 2:
        reportGamestate()
        if gameVars.tryForNE():
            import FFX_neArmor
            print("Mark 1")
            FFX_neArmor.toHiddenCave()
            print("Mark 2")
            FFX_neArmor.dropHunt()
            print("Mark 3")
            FFX_neArmor.returnToGagazet()
        StepCounter = 3

    if Gamestate == "Gagazet" and StepCounter == 3:
        reportGamestate()
        FFX_Gagazet.toTheRonso()
        FFX_Gagazet.gagazetGates()
        StepCounter = 4
        
    if Gamestate == "Gagazet" and StepCounter == 4:
        reportGamestate()
        FFX_Gagazet.Flux()
        StepCounter = 5
        
    if Gamestate == "Gagazet" and StepCounter == 5:
        reportGamestate()
        FFX_Gagazet.dream()
        StepCounter = 6

    if Gamestate == "Gagazet" and StepCounter == 6:
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
        StepCounter = 5

    if Gamestate == "Zanarkand" and StepCounter == 5:
        FFX_Zanarkand.post_Yunalesca()
        StepCounter = 1
        Gamestate = "Sin"
    
    if Gamestate == "Sin" and StepCounter == 1:
        reportGamestate()
        FFX_Sin.makingPlans()
        StepCounter = 2

    if Gamestate == "Sin" and StepCounter == 2:
        reportGamestate()
        print("Test 1")
        FFX_Sin.Shedinja()
        print("Test 2")
        FFX_Sin.facingSin()
        print("Test 3")
        if gameVars.nemesis():
            Gamestate = "Nem_Farm"
            StepCounter = 1
        else:
            StepCounter = 3

    if Gamestate == "Sin" and StepCounter == 3:
        reportGamestate()
        FFX_Sin.insideSin()
        StepCounter = 4
    
    if Gamestate == "Sin" and StepCounter == 4:
        FFX_Sin.eggHunt(autoEggHunt)
        if gameVars.nemesis():
            FFX_Battle.BFA_nem()
        else:
            FFX_Battle.BFA()
            FFX_Battle.yuYevon()
        Gamestate = "End"
        
    #Nemesis logic only:
    if Gamestate == "Gagazet" and StepCounter == 10:
        #FFX_nemesisChanges.calmLands()
        FFX_nemesisChanges.calmLands_1()
        #StepCounter += 1
        StepCounter = 12
    
    if Gamestate == "Gagazet" and StepCounter == 11:
        FFX_nemesisChanges.remiemRaces()
        StepCounter += 1
        
    if Gamestate == "Gagazet" and StepCounter == 12:
        #FFX_nemesisChanges.templeToArena()
        print("MAAAAARK")
        FFX_memory.awaitControl()
        FFX_nemesisChanges.arenaPurchase()
        FFX_Gagazet.defenderX()
        StepCounter = 2
    
    if Gamestate == "Nem_Farm" and StepCounter == 1:
        reportGamestate()
        FFX_nem_arenaPrep.transition()
        while not FFX_nem_arenaPrep.tPlains(capNum=1):
            pass
        StepCounter = 2
        
    if Gamestate == "Nem_Farm" and StepCounter == 2:
        reportGamestate()
        while not FFX_nem_arenaPrep.calm(capNum=1,airshipReturn=False):
            pass
        StepCounter = 3
        
    if Gamestate == "Nem_Farm" and StepCounter == 3:
        reportGamestate()
        FFX_nem_arenaPrep.kilikaShop()
        StepCounter = 4
    
    if Gamestate == "Nem_Farm" and StepCounter == 4:
        reportGamestate()
        FFX_nem_arenaPrep.besaidFarm(capNum=1)
        StepCounter = 5
        
    if Gamestate == "Nem_Farm" and StepCounter == 5:
        reportGamestate()
        FFX_nem_arenaPrep.kilikaFarm(capNum=1)
        StepCounter = 6
    
    if Gamestate == "Nem_Farm" and StepCounter == 6:
        reportGamestate()
        FFX_nem_arenaPrep.miihenFarm(capNum=1)
        StepCounter = 7
    
    if Gamestate == "Nem_Farm" and StepCounter == 7:
        reportGamestate()
        FFX_nem_arenaPrep.mrrFarm(capNum=1)
        StepCounter = 8
    
    if Gamestate == "Nem_Farm" and StepCounter == 8:
        reportGamestate()
        FFX_nem_arenaPrep.apToXP()
        StepCounter = 9
    
    if Gamestate == "Nem_Farm" and StepCounter == 9:
        reportGamestate()
        FFX_nem_arenaPrep.besaidFarm(capNum=10)
        StepCounter = 10
        
    if Gamestate == "Nem_Farm" and StepCounter == 10:
        reportGamestate()
        FFX_nem_arenaPrep.kilikaFarm(capNum=10)
        StepCounter = 11
    
    if Gamestate == "Nem_Farm" and StepCounter == 11:
        reportGamestate()
        FFX_nem_arenaPrep.miihenFarm(capNum=10)
        StepCounter = 12
    
    if Gamestate == "Nem_Farm" and StepCounter == 12:
        reportGamestate()
        FFX_nem_arenaPrep.mrrFarm(capNum=10)
        StepCounter = 13
    
    if Gamestate == "Nem_Farm" and StepCounter == 13:
        reportGamestate()
        FFX_nem_arenaPrep.djoseFarm(capNum=10)
        StepCounter = 14
    
    if Gamestate == "Nem_Farm" and StepCounter == 14:
        reportGamestate()
        FFX_nem_arenaPrep.tPlains(capNum=10,autoHaste=True)
        StepCounter = 15
    
    if Gamestate == "Nem_Farm" and StepCounter == 15:
        reportGamestate()
        FFX_nem_arenaPrep.macWoods(capNum=10)
        StepCounter = 16
        
    if Gamestate == "Nem_Farm" and StepCounter == 16:
        reportGamestate()
        FFX_nem_arenaPrep.bikanel(capNum=10)
        StepCounter = 17
    
    if Gamestate == "Nem_Farm" and StepCounter == 17:
        reportGamestate()
        FFX_nem_arenaPrep.arenaReturn()
        FFX_nem_arenaPrep.autoPhoenix()
        StepCounter = 18
    
    if Gamestate == "Nem_Farm" and StepCounter == 18:
        reportGamestate()
        FFX_nem_arenaPrep.stolenFaythCave()
        StepCounter = 19
    
    if Gamestate == "Nem_Farm" and StepCounter == 19:
        reportGamestate()
        FFX_nem_arenaPrep.gagazet1()
        FFX_nem_arenaPrep.gagazet2()
        FFX_nem_arenaPrep.gagazet3()
        #Gamestate = "End" #Testing only
        StepCounter = 20
    
    if Gamestate == "Nem_Farm" and StepCounter == 20:
        reportGamestate()
        FFX_nem_arenaPrep.calm(capNum=10,airshipReturn = False)
        StepCounter = 21
    
    if Gamestate == "Nem_Farm" and StepCounter == 21:
        reportGamestate()
        FFX_nem_arenaPrep.oneMpWeapon()
        StepCounter = 22
        
    if Gamestate == "Nem_Farm" and StepCounter == 22:
        reportGamestate()
        FFX_nem_arenaPrep.insideSin(capNum=10)
        StepCounter = 23
        
    if Gamestate == "Nem_Farm" and StepCounter == 23:
        reportGamestate()
        FFX_nem_arenaPrep.unlockOmega()
        FFX_nem_arenaPrep.omegaRuins()
        StepCounter = 24
    
    if Gamestate == "Nem_Farm" and StepCounter == 24:
        FFX_nem_arenaPrep.kilikaFinalShop()
        #FFX_nem_arenaPrep.rinEquipDump(buyWeapon=True)
        StepCounter = 25
    
    if Gamestate == "Nem_Farm" and StepCounter == 25:
        FFX_nem_arenaPrep.arenaReturn()
        FFX_nem_arenaPrep.finalWeapon()
        Gamestate = "Nem_Arena"
        StepCounter = 1
    
    if Gamestate == "Nem_Arena" and StepCounter == 1:
        FFX_nem_arenaBattles.battles1()
        gameVars.printArenaStatus()
        StepCounter = 2
    
    if Gamestate == "Nem_Arena" and StepCounter == 2:
        FFX_nem_arenaBattles.battles2()
        gameVars.printArenaStatus()
        StepCounter = 3
    
    if Gamestate == "Nem_Arena" and StepCounter == 3:
        FFX_nem_arenaBattles.juggernautFarm()
        gameVars.printArenaStatus()
        StepCounter = 4
    
    if Gamestate == "Nem_Arena" and StepCounter == 4:
        FFX_nem_arenaBattles.battles3()
        gameVars.printArenaStatus()
        StepCounter = 5
    
    if Gamestate == "Nem_Arena" and StepCounter == 5:
        FFX_nem_arenaBattles.battles4()
        gameVars.printArenaStatus()
        StepCounter = 6
    
    if Gamestate == "Nem_Arena" and StepCounter == 6:
        FFX_nem_arenaBattles.nemesisBattle()
        StepCounter = 7
    
    if Gamestate == "Nem_Arena" and StepCounter == 7:
        FFX_nem_arenaBattles.returnToSin()
        Gamestate = "Sin"
        StepCounter = 3
    
    print("--------------------------------")
    print("Looping")
    print(Gamestate, " | ", StepCounter)
    print("--------------------------------")

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

if FFX_memory.getStoryProgress() > 3210:
    totalTime = endTime - startTime
    FFX_Logs.writeStats("Total time:")
    FFX_Logs.writeStats(str(totalTime))
    print("The game duration was: ", str(totalTime))
    print("This duration is intended for comparison reference only, not as a true timer.")
    print("Please do not use this as your submitted time.")
    FFX_memory.waitFrames(30)
    print("--------")
    print("In order to conform with speed run standards,")
    FFX_memory.waitFrames(60)
    print("we now wait until the end of the credits and stuff")
    FFX_memory.waitFrames(60)
    print("and then will open up the list of saves.")
    FFX_memory.waitFrames(60)
    print("This will show the autosave values, which conforms to the speed run rules.")


    while FFX_memory.getMap() != 23:
        if FFX_memory.getMap() in [292,349]:
            FFX_Xbox.tapStart()
        elif FFX_memory.cutsceneSkipPossible():
            FFX_Xbox.skipScene()
    FFX_memory.waitFrames(180)
    while not FFX_memory.saveMenuOpen():
        FFX_Xbox.tapB()

FFX_memory.end()

print("Automation complete. Unplugging controller.")
import Reset_Controller
print("Unplugging complete. Shutting it down! Have a great day!")
