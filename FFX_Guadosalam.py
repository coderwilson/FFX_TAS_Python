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
 
def arrival():
    print("Starting Guadosalam section")
    FFX_memory.clickToControl()
    
    FFXC.set_movement(-1, 1)
    time.sleep(0.5)
    FFXC.set_movement(0, 1)
    time.sleep(3.5)
    FFXC.set_movement(1, 1)
    time.sleep(0.2)
    FFXC.set_movement(0, 1)
    time.sleep(0.6)
    FFXC.set_neutral()
    
    FFX_memory.clickToControl3()
    FFXC.set_movement(0, -1)
    time.sleep(1)
    FFXC.set_neutral()
    
    FFX_memory.clickToControl3()
    FFXC.set_movement(0, 1)
    time.sleep(2)
    FFXC.set_neutral() #Enter the room where we meet Seymour
    
    FFX_memory.clickToControl3()
    FFXC.set_movement(0, 1)
    time.sleep(1)
    FFX_memory.clickToEvent() #Talk to Auron (first for affection)
    FFXC.set_neutral()
    FFX_memory.clickToControl3()
    
    FFXC.set_movement(1, -1)
    time.sleep(0.7)
    FFXC.set_movement(0, -1)
    FFX_memory.clickToEvent() #Start conversation with Wakka
    FFXC.set_neutral()
    FFX_memory.clickToControl3()
    
    FFXC.set_movement(-1, 0)
    time.sleep(0.4)
    FFX_memory.clickToEvent() #Lulu conversation
    FFXC.set_neutral()
    FFX_memory.clickToControl3()
    
    FFXC.set_movement(-1, 0)
    time.sleep(0.5)
    FFXC.set_movement(-1, -1)
    time.sleep(0.25)
    FFXC.set_movement(0, 1)
    FFX_memory.clickToEvent() # Yuna's turn
    time.sleep(0.2)
    FFXC.set_neutral()
    FFX_memory.clickToControl3()
    
    FFXC.set_movement(0, -1)
    time.sleep(0.3)
    FFX_memory.clickToEvent() #Start conversation with Rikku
    FFXC.set_neutral()
    FFX_Xbox.SkipDialog(66) #Seymour/Trommell
    FFX_Xbox.skipStoredScene(10)

def afterSpeech():
    FFX_memory.clickToControl() #Skips through the long cutscene
    FFX_menu.guadoRikku()
    FFXC.set_movement(0, -1)
    time.sleep(8) #Out of the room and to the party
    FFXC.set_neutral()
    
    FFX_memory.clickToControl()
    FFXC.set_movement(-1, 0)
    time.sleep(1.25)
    FFXC.set_movement(0, -1)
    time.sleep(3)
    FFXC.set_movement(1, 0)
    time.sleep(0.7)
    FFXC.set_movement(1, 1)
    time.sleep(5)
    FFXC.set_neutral()
    
    FFX_memory.awaitControl() #Doorway to the Farplane
    FFXC.set_movement(-1, 1)
    time.sleep(0.4)
    FFXC.set_movement(-1, 0)
    time.sleep(0.2)
    FFXC.set_neutral()
    FFX_Xbox.menuB()
    time.sleep(2)
    FFX_Xbox.menuB() #Open the chest
    FFXC.set_movement(0, 1)
    time.sleep(4)
    FFXC.set_neutral()
    
    FFX_memory.awaitControl() #Approach party
    FFXC.set_movement(0, 1)
    time.sleep(1)
    FFXC.set_neutral()
    
    FFX_memory.clickToControl() #Enter discussion farplane with Auron and Rikku
    FFXC.set_movement(0, 1)
    time.sleep(2)
    FFXC.set_neutral()
    
    FFX_memory.clickToControl() #Finish with Auron/Rikku, and head to farplane
    FFXC.set_movement(-1, 1)
    time.sleep(2)
    FFXC.set_neutral()
    
    FFX_memory.clickToControl() # Farplane, green square
    FFXC.set_movement(1, -1)
    time.sleep(0.5)
    FFXC.set_movement(1, 0)
    time.sleep(2)
    FFXC.set_neutral()
    
    FFX_memory.clickToControl() # Farplane, green square
    FFXC.set_movement(-1, 1)
    time.sleep(2)
    FFXC.set_neutral()

def guadoSkip():
    FFX_memory.clickToControl()
    print("Prepping for Guado skip")
    print("Affection array:")
    print(FFX_memory.affectionArray())
    FFXC.set_movement(0, -1)
    time.sleep(0.8)
    FFXC.set_movement(-1, -1)
    time.sleep(3.5)
    FFXC.set_movement(0, 1)
    time.sleep(1.7)
    FFXC.set_movement(1, 1)
    time.sleep(1.5)
    FFXC.set_movement(1, 0)
    time.sleep(1)
    FFXC.set_neutral() #Approach the party
    
    time.sleep(0.5)
    FFX_memory.clickToControl()
    FFXC.set_movement(-1, -1)
    pos = FFX_memory.getCoords()
    while pos[0] > -85:
        pos = FFX_memory.getCoords()
        
    FFXC.set_movement(0, 1)
    FFX_Xbox.SkipDialog(0.8) #Talk to the walking guado
    FFXC.set_neutral()
    time.sleep(2.6)
    FFX_Xbox.menuB() #Close dialog
    time.sleep(0.2)
    FFXC.set_movement(0, 1)
    while pos[1] < 50:
        pos = FFX_memory.getCoords()
    FFXC.set_movement(1, 0)
    while pos[0] < -44:
        pos = FFX_memory.getCoords()
    
    FFXC.set_movement(1, -1)
    time.sleep(1.48)
    FFXC.set_movement(0, -1)
    time.sleep(0.1)
    FFXC.set_neutral()
    pos = FFX_memory.getCoords()
    
    while pos[0] > 8:
        FFXC.set_value('Dpad', 8)
        time.sleep(0.07)
        FFXC.set_value('Dpad', 0)
        time.sleep(0.105)
        pos = FFX_memory.getCoords()
    while pos[1] < -8.5:
        FFXC.set_value('Dpad', 1)
        time.sleep(0.06)
        FFXC.set_value('Dpad', 0)
        time.sleep(0.09)
        pos = FFX_memory.getCoords()
    
    time.sleep(0.15)
    FFXC.set_movement(0, -1)
    time.sleep(0.04)
    FFXC.set_neutral() #Face downward
    FFX_memory.getCoords()
    time.sleep(0.3)
    val = FFX_Screen.PixelValue(951,568)
    while FFX_Screen.PixelTestTol(951,568,val,10): #Pixel on the door behind us. If it changes, the guado is here.
        doNothing = True
    print("MARK")
    time.sleep(0.26)
    #time.sleep(0.4)
    FFX_Xbox.SkipDialog(0.5)
    
    while not FFX_Screen.PixelTest(995,768,(222, 222, 222)): #Dialog with the running guado
        FFX_Xbox.tapB()
        
    #Time limit for safety
    startTime = time.time()
    timeLimit = 6 #Max number of seconds that we will wait for the skip to occur.
    maxTime = startTime + timeLimit
    
    
    while FFX_memory.getCamera()[0] < 0.6: #Waiting for walking guado to push us into the door
        currentTime = time.time()
        if currentTime > maxTime:
            print("Skip failed for some reason. Moving on without skip.")
            break
    time.sleep(0.035) #Guado potions good!
    FFX_Xbox.tapB()
    
    guadoSkipStatus = False
    checkpoint = 0
    while FFX_memory.getMap() != 140:
        if FFX_memory.userControl():
            if checkpoint == 5:
                if FFX_memory.getCamera()[0] > 0.6:
                    print("Guado skip success.")
                    guadoSkipStatus = True
                    checkpoint += 1
                else:
                    print("Guado skip fail. Back-up strats.")
                    guadoSkipStatus = False
                    checkpoint = 18
            elif checkpoint == 21: #Shelinda conversation
                print("Shelinda")
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 24: #Back to party
                print("Back to party")
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            
            #General pathing
            elif FFX_memory.userControl():
                if FFX_targetPathing.setMovement(FFX_targetPathing.guadoSkip(checkpoint)) == True:
                    checkpoint += 1
                    print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    FFXC.set_neutral()
    return guadoSkipStatus
