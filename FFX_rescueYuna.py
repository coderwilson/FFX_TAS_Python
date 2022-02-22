import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory
import FFX_menu
import FFX_targetPathing
import FFX_zzairShipPath
import FFX_vars
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

def preEvrae():
    FFXC.set_neutral()
    FFX_memory.clickToControl()
    print("Starting first Airship section")
    checkpoint = 0
    while checkpoint < 19:
        if FFX_memory.userControl():
            if checkpoint < 4 and FFX_memory.getMap() == 265:
                FFX_memory.awaitControl()
                FFX_memory.clickToEventTemple(7)
                checkpoint = 4
            elif checkpoint == 9:
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 13:
                FFX_memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 18:
                FFX_memory.clickToEventTemple(4)
                checkpoint += 1
            
            elif FFX_targetPathing.setMovement(FFX_targetPathing.rescueAirship(checkpoint)) == True:
                    checkpoint += 1
                    print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

    FFX_zzairShipPath.airShipPath(1)

def guards():
    FFX_memory.clickToControl() 
    if not gameVars.getBlitzWin():
        FFX_menu.equipSonicSteel()
    
    #Need to add here, use Mega Potion
    if FFX_memory.getItemSlot(3) < 200:
        FFX_menu.beforeGuards()
    
    guardNum = 1
    while guardNum < 6:
        if FFX_memory.userControl():
            FFX_targetPathing.setMovement([0, -200])
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                FFX_Battle.guards(guardNum)
                guardNum += 1
            elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    
    if not gameVars.csr():
        FFX_Xbox.SkipDialog(126)
        FFX_Xbox.skipStoredScene(10)
        FFX_Xbox.SkipDialog(2)
    
    while not FFX_memory.userControl():
        if FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
            FFX_Xbox.tapB()
        elif FFX_memory.cutsceneSkipPossible():
            FFX_Xbox.skipScene()
    
    FFX_memory.clickToEventTemple(6) #Take the spiral lift down
    
    while not FFX_targetPathing.setMovement([-110,0]):
        pass
    FFX_memory.clickToEventTemple(0) #Through the water door
    
    checkpoint = 0
    while checkpoint < 8:
        if FFX_memory.userControl():
            #Map changes
            if checkpoint < 2 and FFX_memory.getMap() == 182:
                checkpoint = 2
            #print("Checkpoint: ", checkpoint)
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.bevellePreTrials(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            
            #Map changes
            elif checkpoint < 2 and FFX_memory.getMap() == 182:
                checkpoint = 2

def trials():
    print("Starting Bevelle trials section.")
    
    checkpoint = 0
    testCounter = 0
    while checkpoint < 53:
        if FFX_memory.userControl():
            #Map changes
            if checkpoint < 2 and FFX_memory.getMap() == 306:
                checkpoint = 2
            
            #Spheres, Pedestols, and gliding across glowing paths.
            elif checkpoint == 3: #Pedestol that starts it all.
                FFXC.set_movement(0, 1)
                FFX_memory.awaitEvent() #Pedestol - START!!!
                FFXC.set_neutral()
                
                while not FFX_memory.userControl():
                    if FFX_memory.getActorCoords(0)[1] < -100:
                        if FFX_memory.btBiDirection() == 1:
                            FFXC.set_value('BtnB', 1)
                        else:
                            FFXC.set_value('BtnB', 0)
                    elif FFX_memory.getActorCoords(0)[1] > 30 and FFX_memory.getActorCoords(0)[1] < 90:
                        FFXC.set_value('BtnB', 1)
                    else:
                        FFXC.set_value('BtnB', 0)
                FFXC.set_neutral()
                if FFX_memory.getActorCoords(0)[0] < -20:
                    print("Correct alcove. Moving on with swiftness.")
                    checkpoint += 2
                else:
                    print("Incorrect alcove. Recovering.")
                    checkpoint += 1
            elif checkpoint == 4: #Recovery
                FFXC.set_movement(1, 0)
                FFX_memory.waitFrames(30 * 1.5)
                FFXC.set_movement(-1, 0)
                FFX_memory.waitFrames(30 * 1.5)
                FFXC.set_neutral()
                FFX_memory.waitFrames(30 * 10.5)
                
                FFX_Xbox.SkipDialog(2)
                FFX_memory.waitFrames(30 * 3)
                cam = FFX_memory.getCamera()
                while cam[2] < -69:
                    cam = FFX_memory.getCamera()
                FFX_Xbox.SkipDialog(2)
                FFX_memory.awaitControl()
                if FFX_memory.getCoords()[0] < -10:
                    print("Correct alcove. Moving on with swiftness.")
                    checkpoint += 1
                else:
                    print("Incorrect alcove. Recovering.")
            elif checkpoint == 7: #First Bevelle sphere, and then more gliding.
                print("Bevelle sphere")
                FFX_memory.clickToEventTemple(7)
                while FFX_memory.getActorCoords(0)[0] < -25:
                    FFXC.set_movement(0, -1)
                    if not FFX_memory.userControl():
                        FFX_Xbox.menuB()
                FFXC.set_neutral()
                print("Mark 1")
                FFX_memory.waitFrames(30 * 1)
                FFXC.set_value('BtnB', 1)
                print("Mark 2")
                FFX_memory.awaitControl()
                print("Mark 3")
                FFXC.set_value('BtnB', 0)
                checkpoint += 1
            elif checkpoint == 10: #Insert Bevelle sphere. Activate lower areas.
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 13: #Down to the lower areas.
                FFXC.set_neutral()
                FFX_memory.waitFrames(2)
                FFXC.set_movement(-1, 0)
                FFX_memory.waitFrames(30 * 2)
                FFXC.set_neutral()
                
                while not FFX_memory.userControl():
                    if FFX_memory.getActorCoords(0)[0] < 40:
                        if FFX_memory.getActorCoords(0)[1] > 100 or FFX_memory.getActorCoords(0)[1] < 10:
                            FFXC.set_value('BtnB', 1)
                        else:
                            FFXC.set_value('BtnB', 0)
                
                    elif FFX_memory.getActorCoords(0)[1] < -30:
                        if FFX_memory.btBiDirection() == 1 and FFX_memory.btTriDirectionMain() == 0:
                            FFX_Xbox.menuB()
                            FFX_memory.waitFrames(15)
                    else:
                        if FFX_memory.getActorCoords(0)[1] > 293 and FFX_memory.getActorCoords(0)[1] < 432:
                            FFXC.set_value('BtnB', 1)
                        else:
                            FFXC.set_value('BtnB', 0)
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 16: #Take Glyph sphere from second alcove
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 18: #To third alcove
                FFXC.set_movement(1, -1)
                FFX_memory.waitFrames(30 * 2)
                FFXC.set_neutral()
                FFX_memory.waitFrames(30 * 2)
                while not FFX_memory.userControl():
                    if FFX_memory.getActorCoords(0)[0] < 40:
                        if FFX_memory.getActorCoords(0)[1] > 100 or FFX_memory.getActorCoords(0)[1] < 10:
                            FFXC.set_value('BtnB', 1)
                        else:
                            FFXC.set_value('BtnB', 0)
                
                    elif FFX_memory.getActorCoords(0)[1] > 425:
                        FFXC.set_value('BtnB', 1)
                    elif FFX_memory.getActorCoords(0)[1] < -30 and \
                        FFX_memory.btBiDirection() == 0 and FFX_memory.btTriDirectionMain() == 0:
                            FFX_Xbox.menuB()
                            FFX_memory.waitFrames(15)
                    else:
                        FFXC.set_value('BtnB', 0)
                FFX_memory.clickToEventTemple(0) #Go ahead and insert Glyph sphere.
                checkpoint += 1
            elif checkpoint == 22: #Remove Bevelle sphere
                FFX_memory.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 24: #Insert Bevelle sphere
                FFX_memory.clickToEventTemple(5)
                checkpoint += 1
            elif checkpoint == 28: #Take Glyph sphere
                FFXC.set_neutral()
                FFX_memory.waitFrames(30 * 0.07)
                FFX_memory.clickToEvent()
                FFX_memory.waitFrames(30 * 0.035)
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 32: #Insert Glyph sphere
                while FFX_memory.userControl():
                    FFX_targetPathing.setMovement([450,525])
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 34: #Take Destro sphere
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 37: #Insert Destro sphere
                FFXC.set_neutral()
                FFX_memory.waitFrames(30 * 0.1)
                FFXC.set_movement(0, 1)
                FFX_memory.waitFrames(30 * 0.07)
                FFXC.set_neutral()
                FFX_Xbox.SkipDialog(1)
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 39: #Take Bevelle sphere
                FFX_memory.clickToEventTemple(5)
                checkpoint += 1
            elif checkpoint == 41: #back on the track.
                FFXC.set_movement(0, -1)
                FFX_memory.waitFrames(30 * 3)
                FFXC.set_neutral()
                
                
                FFX_memory.waitFrames(30 * 10)
                while not FFX_memory.userControl():
                    if FFX_memory.getActorCoords(0)[0] < 40:
                        if FFX_memory.getActorCoords(0)[1] > 100 or FFX_memory.getActorCoords(0)[1] < 10:
                            FFXC.set_value('BtnB', 1)
                        else:
                            FFXC.set_value('BtnB', 0)
                
                    elif FFX_memory.getActorCoords(0)[1] < -30:
                        if FFX_memory.btBiDirection() == 1 and FFX_memory.btTriDirectionMain() == 0:
                            FFX_Xbox.menuB()
                            FFX_memory.waitFrames(15)
                    elif FFX_memory.getActorCoords(0)[1] > 250 and FFX_memory.getActorCoords(0)[1] < 450:
                        FFXC.set_value('BtnB', 1)
                    else:
                        FFXC.set_value('BtnB', 0)
                FFXC.set_neutral()
                print("Arriving in the second alcove again.")
                checkpoint += 1
            elif checkpoint == 43: #Place Bevelle sphere (second alcove)
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 47: #Take Destro sphere
                FFXC.set_movement(1, -1)
                FFX_memory.waitFrames(30 * 0.1)
                FFXC.set_neutral()
                FFX_Xbox.SkipDialog(1)
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 50: #Insert Destro sphere
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 52: #Back on track, to the exit
                FFXC.set_movement(1, -1)
                FFX_memory.waitFrames(30 * 2)
                FFXC.set_neutral()
                FFX_memory.waitFrames(30 * 19)
                while not FFX_memory.userControl():
                    if FFX_memory.getActorCoords(0)[0] < 40:
                        if FFX_memory.getActorCoords(0)[1] > 100 or FFX_memory.getActorCoords(0)[1] < 10:
                            FFXC.set_value('BtnB', 1)
                        else:
                            FFXC.set_value('BtnB', 0)
                
                    elif FFX_memory.getActorCoords(0)[1] < -30:
                        if FFX_memory.btBiDirection() == 0 and FFX_memory.btTriDirectionMain() == 0:
                            FFX_Xbox.menuB()
                            FFX_memory.waitFrames(15)
                    else:
                        if FFX_memory.getActorCoords(0)[1] < 250:
                            FFXC.set_value('BtnB', 1)
                        else:
                            FFXC.set_value('BtnB', 0)
                FFXC.set_neutral()
                FFX_memory.awaitControl()
                FFXC.set_movement(0, -1)
                FFX_memory.waitFrames(30 * 2)
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 58:
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
                
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.bevelleTrials(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            #print("No control")
            #FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            if checkpoint < 3:
                FFXC.set_neutral()

    FFXC.set_neutral()

def trialsEnd():
    checkpoint = 53
    testCounter = 0
    while FFX_memory.getMap() != 226:
        if FFX_memory.userControl():
            if FFX_targetPathing.setMovement(FFX_targetPathing.bevelleTrials(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
        elif checkpoint == 58:
            FFX_memory.clickToEventTemple(2)
            checkpoint += 1
        else:
            FFXC.set_neutral()
                
    FFXC.set_neutral()
    
    #Name for Bahamut
    FFX_Xbox.nameAeon()
    if not gameVars.csr():
        FFX_Xbox.awaitSave(index=29)

def ViaPurifico():
    FFX_memory.clickToControl()
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 3)
    FFXC.set_movement(1, 1)
    FFX_memory.waitFrames(30 * 0.15)
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 5)
    FFXC.set_neutral()
    
    if not gameVars.csr():
        FFX_memory.waitFrames(30 * 5.7) #Wait for the right direction
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 2)
    FFXC.set_neutral()
    
    FFX_memory.clickToControl()
    FFX_menu.viaPurifico()
    
    complete = 0
    while complete == 0:
        if FFX_memory.userControl():
            if FFX_memory.getSLVLYuna() < 15 and FFX_memory.getCoords()[1] > 1460:
                FFXC.set_movement(0, -1)
                FFX_memory.waitFrames(30 * 2)
            else:
                FFXC.set_movement(0, 1)
        elif FFX_Screen.BattleScreen():
            complete = FFX_Battle.isaaru()
        else:
            FFXC.set_neutral()
            FFX_Xbox.tapB()

def evraeAltana():
    FFX_memory.clickToControl()
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 2)
    FFXC.set_neutral()
    
    checkpoint = 0
    lastCP = 0
    while checkpoint < 100:
        if lastCP != checkpoint:
            print("Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        if FFX_memory.getStoryProgress() > 2220:
            print("End of Evrae Altana section.")
            FFXC.set_neutral()
            checkpoint = 100
        if FFX_memory.userControl():
            pos = FFX_memory.getCoords()
            cam = FFX_memory.getCamera()
            if checkpoint == 0:
                if pos[1] > -1550 and cam[0] > 0.5:
                    checkpoint = 10
                else:
                    FFXC.set_movement(0, 1)
            elif checkpoint == 10:
                if pos[1] > -1490:
                    checkpoint = 20
                else:
                    FFXC.set_movement(1, 0)
            elif checkpoint == 20:
                if pos[0] < 1050:
                    checkpoint = 30
                if pos[1] < -1470:
                    FFXC.set_movement(1, 1)
                elif pos[1] > -1365:
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(0, 1)
            elif checkpoint == 30:
                if pos[0] < 625:
                    checkpoint = 40
                if pos[1] < -1410:
                    FFXC.set_movement(1, 1)
                elif pos[1] > -1377:
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(0, 1)
            
            elif checkpoint == 40: #Diagonal with swinging camera
                if pos[1] > -540:
                    checkpoint = 50
                if pos[1] < ((-9.83 * pos[0]) + 4840):
                    FFXC.set_movement(1, 1)
                else:
                    FFXC.set_movement(0, 1)
            elif checkpoint == 50:
                if pos[1] > -310:
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(0, 1)
        elif FFX_Screen.BattleScreen():
            FFX_Battle.evraeAltana()
        elif FFX_Screen.BattleComplete():
            FFX_Xbox.menuB()
        else:
            FFXC.set_neutral()
            if checkpoint == 50:
                FFX_Xbox.tapB()
    return 0
    
def seymourNatus():
    FFX_memory.clickToControl()
    
    if gameVars.getBlitzWin():
        FFX_menu.seymourNatusBlitzWin()
    else:
        FFX_menu.seymourNatusBlitzLoss()
    
    FFX_memory.fullPartyFormat('highbridge')
    complete = 0
    while complete == 0:
        if FFX_memory.userControl():
            FFX_targetPathing.setMovement(FFX_targetPathing.seymourNatus())
        else:
            FFXC.set_neutral()
            if FFX_Screen.BattleScreen():
                print("Battle Start")
                complete = FFX_Battle.seymourNatus()
    
    #Movement for make-out scene
    FFX_memory.clickToControl()
    
    checkpoint = 0
    while checkpoint < 13:
        if FFX_memory.userControl():
            #Events and map changes
            if checkpoint == 1 or checkpoint == 3:
                FFX_memory.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 5:
                print("Checkpoint 5")
                FFXC.set_movement(-1, 0)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_memory.waitFrames(3)
                checkpoint += 1
            elif checkpoint == 6:
                print("Checkpoint 6")
                if not gameVars.csr():
                    FFX_memory.clickToEventTemple(3)
                checkpoint += 1
            elif checkpoint == 8:
                print("Checkpoint 8")
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 12:
                print("Checkpoint 12")
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            
            elif FFX_targetPathing.setMovement(FFX_targetPathing.sutekiDaNe(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            elif FFX_memory.cutsceneSkipPossible():
                FFX_Xbox.skipScene()
