import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory
import FFX_targetPathing
import FFX_vars
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC
 
def arrival():
    print("Starting Guadosalam section")
    FFX_memory.clickToControl()
    
    FFXC.set_movement(-1, 1)
    FFX_memory.waitFrames(30 * 0.5)
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 3.5)
    FFXC.set_movement(1, 1)
    FFX_memory.waitFrames(30 * 0.2)
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 0.6)
    FFXC.set_neutral()
    
    FFX_memory.clickToControl3()
    FFXC.set_movement(0, -1)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_neutral()
    
    FFX_memory.clickToControl3()
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 2)
    FFXC.set_neutral() #Enter the room where we meet Seymour
    
    print("TestVar - ", gameVars.csr)
    if not gameVars.csr():
        FFX_memory.clickToControl3()
        while not FFX_targetPathing.setMovement([4,-114]):
            pass
        print("Mark1")
        #FFXC.set_movement(-1, 1)
        #FFX_memory.clickToEvent()
        while FFX_memory.userControl(): #Talk to Auron (first for affection)
            FFX_targetPathing.setMovement([18,-119])
            FFX_Xbox.tapB()
        FFXC.set_neutral()
        FFX_memory.clickToControl3()
        
        while not FFX_targetPathing.setMovement([-39,-77]):
            pass
        print("Mark2")
        #FFXC.set_movement(1, -1)
        #FFX_memory.clickToEvent()
        while FFX_memory.userControl(): #Start conversation with Wakka
            FFX_targetPathing.setMovement([-49,-61])
            FFX_Xbox.tapB()
        FFXC.set_neutral()
        FFX_memory.clickToControl3()
        
        while not FFX_targetPathing.setMovement([-13,-67]):
            pass
        print("Mark3")
        #FFXC.set_movement(-1, -1)
        #FFX_memory.clickToEvent()
        while FFX_memory.userControl(): #Lulu conversation
            FFX_targetPathing.setMovement([-11,-55])
            FFX_Xbox.tapB()
        FFXC.set_neutral()
        FFX_memory.clickToControl3()
        
        while not FFX_targetPathing.setMovement([15,-52]):
            pass
        while not FFX_targetPathing.setMovement([27,-37]):
            pass
        print("Mark4")
        while FFX_memory.userControl(): # Yuna's turn
            FFX_targetPathing.setMovement([39,-33])
            FFX_Xbox.tapB()
        FFXC.set_neutral()
        FFX_memory.clickToControl3()
        
        while not FFX_targetPathing.setMovement([22,-25]):
            pass
        print("Mark5")
        while FFX_memory.userControl(): #Start conversation with Rikku
            FFX_targetPathing.setMovement([8,-26])
            FFX_Xbox.tapB()
        FFXC.set_neutral()
        
        while not FFX_memory.cutsceneSkipPossible():
            FFX_Xbox.tapB()
        FFX_Xbox.skipStoredScene(3)
    print("Ready for next movement.")

def afterSpeech(checkpoint = 0):
    FFX_memory.clickToControl() #Skips through the long cutscene
    print("Starting movement.")
    print("Starting checkpoint: ", checkpoint)
    
    if checkpoint == 0:
        FFX_memory.clickToEventTemple(4)
    
    while checkpoint != 34:
        #print(FFX_targetPathing.guadoStoryline(checkpoint))
        if FFX_memory.userControl():
            if checkpoint > 17 and checkpoint < 26 and FFX_memory.getMap() == 135:
                checkpoint = 26
            elif checkpoint == 1:
                FFX_memory.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint in [12,16,21,33]:
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 17:
                if not gameVars.csr():
                    FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 14:
                FFX_memory.clickToEventTemple(5)
                checkpoint += 1
            elif checkpoint == 23:
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 25:
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
                
            elif FFX_targetPathing.setMovement(FFX_targetPathing.guadoStoryline(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

def guadoSkip():
    FFX_memory.clickToControl()
    FFXC.set_movement(-1, -1)
    pos = FFX_memory.getCoords()
    while pos[0] > -85:
        pos = FFX_memory.getCoords()
        
    if gameVars.csr():
        checkpoint = 2
    else:
        FFXC.set_movement(0, 1)
        FFX_Xbox.SkipDialog(0.8) #Talk to the walking guado
        FFXC.set_neutral()
        FFX_memory.waitFrames(30 * 2.6)
        FFX_Xbox.menuB() #Close dialog
        FFX_memory.waitFrames(30 * 0.2)
        FFXC.set_movement(0, 1)
        print("Past walking guado")
        while pos[1] < 50:
            pos = FFX_memory.getCoords()
        FFXC.set_movement(1, 0)
        print("Angle right")
        while pos[0] < -44:
            pos = FFX_memory.getCoords()
        FFXC.set_movement(1, -1)
        print("Towards position")
        while pos[0] < 9:
            pos = FFX_memory.getCoords()
        FFXC.set_movement(0, -1)
        print("Adjustment 1")
        while pos[1] > -7.5:
            pos = FFX_memory.getCoords()
        FFXC.set_neutral()
        FFX_memory.waitFrames(5)
        
        pos = FFX_memory.getCoords()
        recovery = False
        print("Adjustment 2")
        while pos[0] > 8 and recovery == False:
            tidusPos = FFX_memory.getCoords()
            guadoPos = FFX_memory.getActorCoords(17)
            if abs(tidusPos[0] - guadoPos[0]) + abs(tidusPos[1] - guadoPos[1]) < 30:
                while FFX_memory.userControl():
                    FFX_targetPathing.setMovement(guadoPos[0], guadoPos[1])
                    FFX_Xbox.tapB()
                recovery = True
            else:
                FFXC.set_value('Dpad', 4)
                FFX_memory.waitFrames(3)
                FFXC.set_value('Dpad', 0)
                FFX_memory.waitFrames(5)
                pos = FFX_memory.getCoords()
        print("Adjustment 3")
        while pos[1] < -8.5 and recovery == False:
            tidusPos = FFX_memory.getCoords()
            guadoPos = FFX_memory.getActorCoords(17)
            if abs(tidusPos[0] - guadoPos[0]) + abs(tidusPos[1] - guadoPos[1]) < 30:
                while FFX_memory.userControl():
                    FFX_targetPathing.setMovement(guadoPos[0], guadoPos[1])
                    FFX_Xbox.tapB()
                recovery = True
            else:
                FFXC.set_value('Dpad', 1)
                FFX_memory.waitFrames(3)
                FFXC.set_value('Dpad', 0)
                FFX_memory.waitFrames(5)
                pos = FFX_memory.getCoords()
        
        FFX_memory.waitFrames(30 * 0.15)
        FFXC.set_movement(0, -1)
        FFX_memory.waitFrames(30 * 0.04)
        FFXC.set_neutral() #Face downward
        FFX_memory.waitFrames(4)
        skipActivate = False
        while not skipActivate and recovery == False:
            tidusPos = FFX_memory.getCoords()
            guadoPos = FFX_memory.getActorCoords(17)
            if abs(tidusPos[0] - guadoPos[0]) + abs(tidusPos[1] - guadoPos[1]) < 30:
                if guadoPos[0] < 10:
                    skipActivate = True
                    print("MARK")
                    FFX_Xbox.SkipDialog(0.5)
            elif pos[1] > -9:
                FFXC.set_value('Dpad', 2)
                FFX_memory.waitFrames(2)
                FFXC.set_value('Dpad', 0)
                FFX_memory.waitFrames(5)
                pos = FFX_memory.getCoords()
                
        
        if recovery == False:
            #Time limit for safety
            startTime = time.time()
            timeLimit = 8 #Max number of seconds that we will wait for the skip to occur.
            maxTime = startTime + timeLimit
        
            while FFX_memory.getCamera()[0] < 0.6: #Waiting for walking guado to push us into the door
                currentTime = time.time()
                if currentTime > maxTime:
                    print("Skip failed for some reason. Moving on without skip.")
                    break
            FFX_memory.waitFrames(30 * 0.035) #Guado potions good!
            FFX_Xbox.tapB()
        checkpoint = 0
    
    guadoSkipStatus = False
    while FFX_memory.getMap() != 140:
        if FFX_memory.userControl():
            if checkpoint == 5:
                print(FFX_memory.getCamera())
                if FFX_memory.getCamera()[1] < -10:
                    print("Guado skip success.")
                    if gameVars.csr():
                        guadoSkipStatus = False
                        checkpoint = 18
                    else:
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
