import pyxinput
import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_memory
import FFX_targetPathing

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

def NamingTidus_slow():
    #Clear Tidus
    time.sleep(0.1)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB() # Delete all but T
    
    #Replace with TAS
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB() # A
    FFX_Xbox.menuDown()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB() # S
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() # Confirm
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() # Confirm again

def NamingTidus():
    FFX_Xbox.menuB() # Confirm
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() # Confirm again

def NewGame(Gamestate):
    print("Starting the game")
    print("Gamestate: ", Gamestate)
    #time.sleep(20)
    
    #Old version
    #FFXC.set_movement(0, 1)
    #time.sleep(0.1)
    #FFXC.set_neutral()
    #FFXC.set_value('BtnB', 1)
    #time.sleep(0.1)
    #FFXC.set_value('BtnB', 0)
    
    #New version
    gameModeSelected = False
    while gameModeSelected == False:
        if FFX_memory.getMap() != 23:
            FFXC.set_value('BtnStart', 1)
            time.sleep(0.035)
            FFXC.set_value('BtnStart', 0)
            time.sleep(0.035)
        elif Gamestate != 'none':
            time.sleep(3)
            if FFX_memory.cursorLocation()[1] == 176:
                if FFX_memory.NewGameCursor() == 0:
                    FFX_Xbox.menuDown()
                else:
                    time.sleep(0.07)
                    FFX_Xbox.menuB()
                    gameModeSelected = True
        else:
            time.sleep(0.2)
            if FFX_memory.cursorLocation()[1] == 176:
                if FFX_memory.NewGameCursor() == 1:
                    FFX_Xbox.menuUp()
                else:
                    #time.sleep(2)
                    FFX_Xbox.menuB()
                    gameModeSelected = True
            else:
                FFX_Xbox.menuB()
    
def NewGame2():
    #New game selected. Next, select options.
    time.sleep(4)
    print("Default Sphere Grid")
    FFX_Xbox.menuB()
    time.sleep(1)
    print("Confirm sphere grid")
    FFX_Xbox.menuB()
    time.sleep(1)
    print("Orchestrated soundtrack.")
    FFX_Xbox.menuB()
    time.sleep(1)
    print("Confirm Orchestrated soundtrack.")
    FFX_Xbox.menuB()

def listenStory(gameLength):
    time.sleep(5)
    x = 0
    print("Skipping intro scene, we'll watch this properly in about 8 hours.")
    for x in range(100):
        FFXC.set_value('BtnBack', 1)
        time.sleep(0.035)
        FFXC.set_value('BtnBack', 0)
        time.sleep(0.035)
    print("End skip mashing")
    FFX_memory.awaitControl()
    
    skips = 0
    checkpoint = 0
    while FFX_memory.getBattleNum() != 414: #Sinspawn Ammes
        if FFX_memory.userControl():
            #Events
            if checkpoint == 2:
                while FFX_memory.userControl():
                    FFXC.set_movement(0, -1)
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                
                #Name Tidus
                FFX_Xbox.nameAeon()
                
                checkpoint += 1
            elif checkpoint == 4:
                while FFX_memory.userControl():
                    FFXC.set_movement(0, -1)
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                time.sleep(0.2)
                while not FFX_memory.userControl():
                    if FFX_memory.diagSkipPossible():
                        FFX_Xbox.tapB()
                print("Done clicking")
                checkpoint += 1
            elif checkpoint < 6 and FFX_memory.getStoryProgress() >= 5:
                checkpoint = 6
            elif checkpoint < 11 and FFX_memory.getMap() == 371:
                checkpoint = 11
            elif checkpoint < 15 and FFX_memory.getMap() == 370:
                checkpoint = 15
            elif checkpoint == 17: #Don't cry.
                while FFX_memory.userControl():
                    FFXC.set_movement(1, -1)
                FFXC.set_neutral()
                checkpoint += 1
        
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.tidusHome(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            elif FFX_memory.cutsceneSkipPossible():
                skips += 1
                if skips == 3:
                    time.sleep(5)
                    FFXC.set_value('BtnStart', 1) #Generate button to skip later
                    time.sleep(0.35)
                    FFXC.set_value('BtnStart', 0)
                    time.sleep(5)
                else:
                    FFX_Xbox.skipScene()

def listenStory_old(gameLength):
    #Skip cutscene (multiple presses)
    time.sleep(9)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 1)
    time.sleep(0.05)
    FFXC.set_value('BtnBack', 0)
    time.sleep(0.05)
    
    #Talk to kids
    FFX_memory.awaitControl()
    FFXC.set_movement(0, -1)
    while FFX_memory.userControl():
        pos = FFX_memory.getCoords()
        if pos[0] > 45 and pos[1] > 2:
            FFXC.set_movement(1, 0)
        else:
            FFXC.set_neutral()
        if pos[0] < 35:
            FFX_Xbox.menuB()
    FFXC.set_neutral()
    
    #Name Tidus (custom function in this library. Can be changed later.
    FFX_Screen.awaitPixel(316,374,(224, 182, 138))
    NamingTidus()
    
    #Now to talk to the ladies.
    #FFX_Screen.awaitPixel(1554,657,(255, 192, 210))
    FFX_memory.awaitControl()
    FFXC.set_movement(1, 0)
    time.sleep(0.5)
    FFX_Xbox.SkipDialog( 2 )
    FFXC.set_neutral()
    
    #Leave house area
    FFX_memory.awaitControl()
    #time.sleep(30)
    FFXC.set_movement(0, -1)
    time.sleep(6)
    FFXC.set_neutral()
    
    #Zanar talks to himself.
    FFX_memory.awaitControl()
    #time.sleep(74)
    FFXC.set_movement(1, 1)
    time.sleep(0.4)
    FFXC.set_movement(0, 1)
    while FFX_memory.getMap() != 371:
        time.sleep(0.05)
    
    FFXC.set_neutral()
    #Front of the Blitz dome
    FFX_memory.clickToControl()
    time.sleep(0.15)
    FFXC.set_movement(0, 1)
    FFX_Xbox.SkipDialog(0.3)
    while FFX_memory.getStoryProgress() < 6:
        if FFX_memory.userControl():
            if FFX_memory.getCoords()[0] > 2:
                FFXC.set_movement(1, 1)
            elif FFX_memory.getCoords()[0] < -10:
                FFXC.set_movement(-1, 1)
            else:
                FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()
            FFX_Xbox.menuB()
    
    #Skip blitball scene
    time.sleep(2.9)
    FFX_Xbox.skipScene()
    
    #Run to Auron
    FFX_memory.awaitControl()
    #FFX_memory.awaitControl()
    FFXC.set_movement(1, -1)
    time.sleep(0.4)
    FFXC.set_movement(0, -1)
    time.sleep(0.3)
    while FFX_memory.getStoryProgress() < 10:
        if FFX_memory.userControl():
            pos = FFX_memory.getCoords()
            if pos[1] < ((8.43 * pos[0]) + 805.14):
                FFXC.set_movement(1, -1)
            elif pos[1] > ((8.43 * pos[0]) + 835):
                FFXC.set_movement(-1, -1)
            else:
                FFXC.set_movement(0, -1)
        else:
            FFXC.set_neutral()
            FFX_Xbox.menuB()
    
    FFXC.set_neutral()
    
    #Two possible cutscene skips, possible to save 8~10 seconds
    waitCounter = 0
    while FFX_memory.getMap() != 389:
        waitCounter += 1
        if waitCounter % 100000 == 0:
            print("Waiting for time to stop freezing. ", waitCounter / 100000)
    print("OK time has returned to normal. Now timing for skip.")
    
    time.sleep(16.4)
    FFX_Xbox.skipScene()
    time.sleep(23)
    FFXC.set_value('BtnStart', 1) #Generate button to skip a later scene ("This is your story")
    time.sleep(0.1)
    FFXC.set_value('BtnStart', 0)
    
    #Just to make sure...
    FFXC.set_neutral()

def ammesBattle_testing():
    FFX_Xbox.clickToBattle()
    FFX_Battle.defend()
    
    #Auron overdrive tutorial
    while not FFX_Screen.PixelTest(724,314,(234, 196, 0)):
        FFX_Xbox.tapB()
    FFX_Xbox.clickToBattle()
    
    while not FFX_memory.otherBattleMenu():
        FFX_Xbox.menuLeft()
    FFX_Xbox.SkipDialog(3) #Initiate overdrive
    print("Frame Counter: ", FFX_memory.getFrameCount())
    time.sleep(1) #Static delay, the same every time.
    print("Frame Counter: ", FFX_memory.getFrameCount())
    
    #Doing the actual overdrive
    FFXC.set_value('Dpad', 2)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    time.sleep(0.04)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    FFXC.set_value('Dpad', 0)
    time.sleep(0.04)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    FFXC.set_value('Dpad', 4)
    time.sleep(0.04)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    FFXC.set_value('Dpad', 0)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    time.sleep(0.04)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    FFXC.set_value('Dpad', 1)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    time.sleep(0.04)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    FFXC.set_value('Dpad', 0)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    time.sleep(0.04)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    FFXC.set_value('Dpad', 8)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    time.sleep(0.04)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    FFXC.set_value('Dpad', 0)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    time.sleep(0.04)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    FFXC.set_value('BtnShoulderL', 1)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    time.sleep(0.04)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    FFXC.set_value('BtnShoulderL', 0)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    time.sleep(0.04)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    FFXC.set_value('BtnShoulderR', 1)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    time.sleep(0.04)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    FFXC.set_value('BtnShoulderR', 0)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    time.sleep(0.04)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    FFXC.set_value('BtnA', 1)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    time.sleep(0.04)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    FFXC.set_value('BtnA', 0)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    time.sleep(0.04)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    FFXC.set_value('BtnB', 1)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    time.sleep(0.04)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    FFXC.set_value('BtnB', 0)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    time.sleep(2)
    print("Frame Counter: ", FFX_memory.getFrameCount())
    time.sleep(90)


def ammesBattle():
    FFX_Xbox.clickToBattle()
    FFX_Battle.defend()
    
    while FFX_memory.battleActive():
        FFX_Xbox.tapB()
    time.sleep(0.5) #Just for no overlap
    FFX_Xbox.clickToBattle()
    
    #Auron overdrive tutorial
    while not FFX_memory.otherBattleMenu():
        FFX_Xbox.menuLeft()
    FFX_Xbox.SkipDialog(3) #Initiate overdrive
    time.sleep(1) #Static delay, the same every time.
    
    #Doing the actual overdrive
    FFXC.set_value('Dpad', 2)
    time.sleep(0.04)
    FFXC.set_value('Dpad', 0)
    time.sleep(0.04)
    FFXC.set_value('Dpad', 4)
    time.sleep(0.04)
    FFXC.set_value('Dpad', 0)
    time.sleep(0.04)
    FFXC.set_value('Dpad', 1)
    time.sleep(0.04)
    FFXC.set_value('Dpad', 0)
    time.sleep(0.04)
    FFXC.set_value('Dpad', 8)
    time.sleep(0.04)
    FFXC.set_value('Dpad', 0)
    time.sleep(0.04)
    FFXC.set_value('BtnShoulderL', 1)
    time.sleep(0.04)
    FFXC.set_value('BtnShoulderL', 0)
    time.sleep(0.04)
    FFXC.set_value('BtnShoulderR', 1)
    time.sleep(0.04)
    FFXC.set_value('BtnShoulderR', 0)
    time.sleep(0.04)
    FFXC.set_value('BtnA', 1)
    time.sleep(0.04)
    FFXC.set_value('BtnA', 0)
    time.sleep(0.04)
    FFXC.set_value('BtnB', 1)
    time.sleep(0.04)
    FFXC.set_value('BtnB', 0)
    time.sleep(2)

def AfterAmmes():
    FFX_memory.clickToControl()
    checkpoint = 0
    
    while FFX_memory.getMap() != 49:
        if FFX_memory.userControl():
            #Map changes and events
            if checkpoint == 6: #Save sphere
                FFXC.set_neutral()
                time.sleep(0.2)
                FFX_Xbox.menuB()
                time.sleep(1)
                FFX_Xbox.menuB()
                time.sleep(1)
                FFX_Xbox.menuA()
                FFX_Xbox.menuB()
                checkpoint += 1
            elif checkpoint < 9 and FFX_memory.getStoryProgress() >= 20: #Swim to Jecht
                checkpoint = 9
            elif checkpoint < 11 and FFX_memory.getStoryProgress() >= 30: #Towards Baaj temple
                checkpoint = 11
            
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.allStartsHere(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.turnReady():
                FFX_Battle.Tanker()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            elif FFX_memory.cutsceneSkipPossible():
                FFX_Xbox.skipStoredScene(3)

def SwimToJecht() :
    #FFX_memory.awaitControl()
    
    #time.sleep(1.5)
    print("Swimming to Jecht")
    
    FFXC.set_value('BtnA', 1)
    FFXC.set_movement(-1, -1)
    time.sleep(8)
    while FFX_memory.userControl():
        FFXC.set_movement(-1, 1)
    
    FFXC.set_neutral()
    FFXC.set_value('BtnA', 0)
    print("We've now reached Jecht.")
    FFX_Xbox.SkipDialog(5)
    
    #Next, swim to Baaj temple
    FFX_memory.clickToControl()
    FFXC.set_movement(1, 0)
    time.sleep(1)
    FFXC.set_movement(1, 1)
    time.sleep(0.6)
    FFXC.set_movement(0, 1)
    time.sleep(5)
    FFXC.set_movement(-1, 1)
    time.sleep(1)
    FFXC.set_movement(0, 1)
    time.sleep(14)
    FFXC.set_movement(-1, 1)
    time.sleep(1.5) # Line up with stairs
    
    FFXC.set_movement(0, 1)
    #time.sleep(600)
    time.sleep(3)
    
    while FFX_memory.getMap() == 48:
        pos = FFX_memory.getCoords()
        if pos[1] < 550:
            if pos[0] < -5:
                FFXC.set_movement(1, 1)
            elif pos[0] > 5:
                FFXC.set_movement(-1, 1)
            else:
                FFXC.set_movement(0, 1)
        else:
            if pos[1] > ((-1.00 * pos[0]) + 577.00):
                FFXC.set_movement(-1, 1)
            else:
                FFXC.set_movement(0, 1)
    
    FFXC.set_neutral()
    time.sleep(0.3)
