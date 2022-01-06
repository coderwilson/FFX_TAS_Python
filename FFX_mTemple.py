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

def approach(blitzWin):
    print("------------------------------------------Affection array:")
    print(FFX_memory.affectionArray())
    print("------------------------------------------")
    FFX_memory.clickToControl()
    print("Approaching Macalania Temple")
    
    checkpoint = 0
    while FFX_memory.getMap() != 106:
        if FFX_memory.userControl():
            #Map changes
            if checkpoint < 2 and FFX_memory.getMap() == 153:
                checkpoint = 2
            
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.mTempleApproach(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    FFXC.set_neutral()
    FFX_menu.macTemple(blitzWin)

def arrival(blitzWin):
    print("Starting Macalania Temple section")
    FFX_memory.awaitControl()
    #if FFX_memory.getPower() < 26:
    #    FFX_memory.setPower(26) #Need 34 total from here forward. 2 from Wendigo and 6 from bombs. 26 needed here.
    
    #Movement:
    jyscalSkipStatus = False
    checkpoint = 0
    skipStatus = True
    while FFX_memory.getMap() != 80:
        if FFX_memory.userControl():
            #Main events
            if checkpoint == 1:
                FFXC.set_neutral()
                FFX_memory.waitFrames(30 * 0.2)
                FFX_Xbox.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 4: #Talking to Trommell
                FFX_memory.clickToEventTemple(6)
                if FFX_memory.getCoords()[0] < 23.5:
                    FFX_memory.waitFrames(30 * 0.07)
                    FFXC.set_movement(1, 0)
                    FFX_memory.waitFrames(30 * 0.035)
                    FFXC.set_neutral()
                    FFX_memory.waitFrames(30 * 0.4)
                checkpoint += 1
            elif checkpoint == 5: #Skip (new)
                print("Lining up for skip.")
                FFXC.set_movement(0, -1)
                FFX_memory.waitFrames(30 * 0.2)
                FFXC.set_neutral()
                while FFX_memory.getCoords()[1] < -101.5:
                    FFXC.set_value('Dpad', 8)
                    FFX_memory.waitFrames(30 * 0.035)
                    FFXC.set_value('Dpad', 0)
                    FFX_memory.waitFrames(30 * 0.09)
                
                print("Turning back")
                FFX_memory.waitFrames(30 * 0.4)
                FFXC.set_movement(-1, 0)
                FFX_memory.waitFrames(30 * 0.035)
                FFXC.set_neutral()
                FFX_memory.waitFrames(30 * 0.4)
                
                print("Now lined up. Here we go.")
                FFXC.set_movement(1, 0)
                FFX_memory.waitFrames(30 * 0.08)
                FFXC.set_value('BtnB', 1)
                FFX_memory.waitFrames(30 * 0.1)
                FFXC.set_value('BtnB', 0)
                FFX_memory.waitFrames(30 * 1.5)
                FFXC.set_neutral()
                checkpoint += 1
                FFX_memory.clickToControl3()
            
            elif checkpoint == 8: #Open chest
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
                
            elif checkpoint == 11:
                print("Check if skip is online")
                if FFX_memory.getStoryProgress() < 1505:
                    jyscalSkipStatus = True
                    checkpoint += 1
                else:
                    jyscalSkipStatus = False
                    checkpoint = 20
                    skipStatus = False
                print("Jyscal Skip results: ", skipStatus)
            elif checkpoint == 14: #Pause so we don't mess up the skip
                if skipStatus == True:
                    FFXC.set_neutral()
                    #while FFX_memory.getCamera()[3] > -20:
                    #    FFX_Xbox.tapB()
                    FFX_Xbox.SkipDialog(5)
                    FFXC.set_movement(0, -1)
                    FFX_memory.awaitEvent()
                    FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint < 16 and FFX_memory.getMap() == 239:
                checkpoint = 16
            
            #Recovery items
            elif checkpoint == 23: #Door, Jyscal room
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 24: #Back to the main room
                FFX_memory.clickToEventTemple(5)
                checkpoint += 1
            elif checkpoint == 27:
                checkpoint = 12
            
            
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.templeFoyer(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    return jyscalSkipStatus

def startSeymourFight():
    FFX_memory.clickToControl()
    while FFX_targetPathing.setMovement([9, -53]) == False:
        doNothing = True #Allows us to move to the Seymour fight.
    FFXC.set_movement(1, 0)
    FFX_memory.awaitEvent()
    FFXC.set_neutral()

def seymourFight():
    
    FFX_Battle.seymourGuado()
    
    #Name for Shiva
    FFX_Xbox.nameAeon()
    
    #FFX_memory.waitFrames(30 * 1)
    #FFX_Xbox.menuB()
    #FFX_memory.waitFrames(30 * 0.2)
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuB()
    
    FFX_memory.awaitControl()
    FFXC.set_movement(-1, -1)
    FFX_memory.waitFrames(30 * 0.4)
    FFXC.set_movement(-1, 0)
    FFX_memory.waitFrames(30 * 4.5)
    FFXC.set_neutral()

def trials():
    FFX_memory.awaitControl()
    
    checkpoint = 0
    while FFX_memory.getMap() != 153:
        if FFX_memory.userControl():
            #Map changes
            if checkpoint < 2 and FFX_memory.getMap() == 239:
                checkpoint = 2
            
            #Spheres and Pedestols
            elif checkpoint == 2:
                FFX_memory.awaitControl()
                print("Activate the trials")
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 9: #Push pedestol - 1
                FFXC.set_movement(1, 0)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_memory.waitFrames(30 * 1)
                checkpoint += 1
            elif checkpoint == 13: # Grab first Mac Sphere
                FFX_memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 17: # Place first Mac Sphere
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 20: # Grab glyph sphere
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 24: #Push pedestol - 2
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 29: #Push pedestol - 3
                FFXC.set_movement(1, 0)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_memory.waitFrames(30 * 1)
                checkpoint += 1
            elif checkpoint == 32: # Place Glyph sphere
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 39: # Grab second Mac sphere
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 46: # Place second Mac sphere
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 51: # Grab third Mac sphere
                FFX_memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 53: # Place third Mac sphere
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 58: # End of trials
                FFX_memory.clickToEventTemple(0)
                FFX_memory.awaitControl()
                FFX_memory.clickToEventTemple(4) #Just to start the next set of dialog.
            
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.mTempleTrials(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()

def escape():
    FFX_memory.clickToControl()
    print("First, some menuing")
    FFX_menu.afterSeymour()
    FFX_memory.fullPartyFormat('macalaniaescape')
    
    print("Now to escape the Guado")
    
    checkpoint = 0
    while FFX_memory.getBattleNum() != 195:
        if FFX_memory.userControl():
            #Events
            if checkpoint == 2:
                FFX_Xbox.touchSaveSphere()
                checkpoint += 1
                print("Touching save sphere. Update checkpoint: ", checkpoint)
            
            #Map changes
            elif checkpoint < 19 and FFX_memory.getMap() == 192:
                checkpoint = 19
                print("Map change. Update checkpoint: ", checkpoint)
            
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.mTempleEscape(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                FFX_Screen.awaitTurn()
                if FFX_memory.getBattleNum() == 195:
                    break
                else:
                    FFX_Battle.fleeAll()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    
    print("Done pathing. Now for the Wendigo fight.")
    FFX_Battle.wendigo()
    print("Wendigo fight over")

def wendigoFight():
    print("wendigoFight function is no longer used.")

def underLake():
    FFX_memory.clickToControl()
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_movement(-1, 1)
    FFX_memory.waitFrames(30 * 0.8)
    FFXC.set_movement(1, 1)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_movement(0, 1)
    FFX_memory.clickToEvent()
    FFXC.set_neutral()
    
    FFX_memory.clickToControl()
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 1.5) #Approach Yuna
    FFXC.set_neutral()
    
    FFX_memory.clickToControl()
    while FFX_memory.getCoords()[1] > 110:
        FFXC.set_movement(-1, 1)
    while FFX_memory.getCoords()[1] > 85:
        FFXC.set_movement(1, 1)
    while FFX_memory.getCoords()[0] > -30:
        if FFX_memory.getCoords()[1] < 110:
            FFXC.set_movement(1, -1)
        else:
            FFXC.set_movement(1, 0)
    FFXC.set_movement(1, 0)
    FFX_memory.clickToEvent() #Chest with Lv.2 Key Sphere
    FFXC.set_neutral()
    FFX_Xbox.SkipDialog(0.2)
    FFX_memory.clickToControl()
    FFXC.set_movement(-1, 0)
    FFX_memory.waitFrames(30 * 0.25)
    while FFX_memory.getCoords()[0] < -5:
        FFXC.set_movement(-1, 1)
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 1) #To Auron
    FFX_Xbox.SkipDialog(1.5)
    FFXC.set_movement(1, 0)
    FFX_Xbox.SkipDialog(0.4)
    FFXC.set_movement(-1, 0)
    FFX_Xbox.SkipDialog(0.4)
    FFXC.set_neutral()
    FFX_memory.clickToControl()
    
    FFXC.set_movement(0, -1)
    FFX_memory.waitFrames(30 * 3)
    FFXC.set_neutral()
    FFX_memory.waitFrames(30 * 10)
    FFX_Xbox.skipScene()
