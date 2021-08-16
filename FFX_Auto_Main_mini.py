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
Gamestate = "Macalania"
StepCounter = 1
#Gamestate = "Luca"
#StepCounter = 1
#Gamestate = "none"
#StepCounter = 1

#Game length. Full is the same as any%, short is about 35 minutes with memory manip.
#gameLength = "short"
gameLength = "full"
forceBlitzWin = True
autoEggHunt = False
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
    
    if Gamestate == "Macalania" and StepCounter == 1: #1 = south, 2 = north
        FFX_LoadGame.loadOffset(2) #Update this line to match the save file position. Position 0 would be the autosave.

#Movement files
#import FFX_DreamZan
if gameLength != "short":
    #import FFX_Baaj
    #import FFX_Besaid1
    #import FFX_Besaid2
    #import FFX_Boats
    #import FFX_Kilika
    #import FFX_Luca
    #import FFX_Blitz
    #import FFX_Miihen
    #import FFX_MRR
    #import FFX_Djose
    #import FFX_Moonflow
    #import FFX_Guadosalam
    #import FFX_ThunderPlains
    import FFX_mWoods
    import FFX_mTemple
    import FFX_home
    #import FFX_rescueYuna
    #import FFX_Gagazet
    #import FFX_Zanarkand
import FFX_Sin

if Gamestate == "Macalania" and StepCounter == 1:
    reportGamestate()
    FFX_mWoods.arrival()
    StepCounter = 2
    #Gamestate = "manualBreak" # Used for testing only.

if Gamestate == "Macalania" and StepCounter == 2:
    reportGamestate()
    FFX_mWoods.lakeRoad()
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
    StepCounter = 5

if Gamestate == "Macalania" and StepCounter == 5:
    reportGamestate()
    FFX_mTemple.trials()
    #Gamestate = "manualBreak" # Used for testing only.
    StepCounter = 6

if Gamestate == "Macalania" and StepCounter == 6:
    reportGamestate()
    FFX_mTemple.escape()
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

#print("Waiting for Yu Yevon to die.")
#time.sleep(6)
print("Time! The game is now over.")
endTime = FFX_Logs.timeStamp()
FFX_Logs.writeStats("End time:")
FFX_Logs.writeStats(str(endTime))

totalTime = endTime - startTime
FFX_Logs.writeStats("Total time:")
FFX_Logs.writeStats(str(totalTime))
print("The game duration was: ", str(totalTime))
time.sleep(10)


FFX_memory.end()

#print("Automation complete. Unplugging controller.")
#import Reset_Controller
#print("Unplugging complete. Shutting it down! Have a great day!")