import FFX_memory
import FFX_Screen
import FFX_Battle
import FFX_targetPathing
import time

import FFX_Xbox
FFXC = FFX_Xbox.controllerHandle()

def airShipPath(version):
    FFX_memory.clickToControl()
    
    complete = False
    checkpoint = 0
    while complete == False:
        if FFX_memory.userControl():
            #print("Checkpoint: ", checkpoint)
            #Map changes
            if checkpoint == 2:
                FFX_memory.clickToEventTemple(3)
                checkpoint += 1
            elif checkpoint < 6 and FFX_memory.getMap() == 351: #Screen with Isaaru
                checkpoint = 6
            elif checkpoint < 9 and FFX_memory.getMap() == 211: #Gallery screen (includes lift screens)
                checkpoint = 9
                #Optional save sphere can be touched here.
                #Should not be necessary, we should be touching save sphere in Home
            elif checkpoint == 14 and version == 2:
                print("Talking to Yuna/Kimahri in the gallery")
                checkpoint = 23
                print("Checkpoint update: ", checkpoint)
            elif checkpoint == 16:
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 18:
                FFXC.set_neutral()
                FFX_Xbox.SkipDialog(1)
                FFX_memory.awaitControl()
                checkpoint += 1
            
            #Return trip map changes
            elif checkpoint == 24:
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint in [31,34]:
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 37:
                FFX_memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 40:
                FFX_memory.clickToEventTemple(7)
                complete = True
            
            #Complete states
            elif checkpoint == 19 and version == 1:
                print("Pre-Evrae pathing")
                FFXC.set_movement(0, 1)
                time.sleep(3)
                FFXC.set_neutral()
                complete = True
            elif checkpoint == 19 and version == 3:
                print("Sin's Arms")
                FFXC.set_movement(0, 1)
                time.sleep(3)
                FFXC.set_neutral()
                while not FFX_memory.battleActive():
                    if FFX_memory.diagSkipPossible():
                        FFX_Xbox.tapB()
                    elif FFX_memory.cutsceneSkipPossible():
                        FFX_Xbox.skipScene()
                complete = True
            elif checkpoint == 19 and version == 4:
                print("Straight to the deck, talking to Yuna.")
                FFXC.set_movement(0, 1)
                time.sleep(3)
                FFXC.set_neutral()
                FFX_memory.awaitControl()
                FFX_targetPathing.setMovement([-2,-15])
                time.sleep(0.5)
                while FFX_memory.userControl():
                    FFX_targetPathing.setMovement([-2,-15])
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                while not FFX_memory.userControl():
                    if FFX_memory.diagSkipPossible():
                        FFX_Xbox.tapB()
                    elif FFX_memory.cutsceneSkipPossible():
                        FFX_Xbox.skipScene()
                complete = True
            elif checkpoint == 19 and version == 5:
                print("Again to the deck, three skips.")
                FFXC.set_movement(0, 1)
                time.sleep(3)
                FFXC.set_neutral()
                while not FFX_memory.battleActive():
                    if FFX_memory.diagSkipPossible():
                        FFX_Xbox.tapB()
                    elif FFX_memory.cutsceneSkipPossible():
                        FFX_Xbox.skipScene()
                complete = True
            elif checkpoint == 19 and version == 6:
                print("Sin's Face")
                FFXC.set_movement(0, 1)
                time.sleep(3)
                FFXC.set_neutral()
                complete = True
            
            
            #General Pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.airShip(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                FFX_Battle.fleeAll()
            elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    
    print("End of section, Airship pathing")

def notes():
    if version == 1:
        print("Pre-Evrae pathing")
        checkpoint = 60
    elif version == 2:
        print("Talking to Yuna/Kimahri in the gallery")
        checkpoint = 120
    elif version == 3:
        print("Straight to the deck, three skips.")
        checkpoint = 150
    elif version == 4:
        print("Straight to the deck, talking to Yuna.")
        checkpoint = 180
    elif version == 5:
        print("Final pathing. Sin's face.")
        checkpoint = 200
    elif version == 6:
        print("Final pathing. Sin's face.")
        checkpoint = 70
    else:
        print("Something maybe went wrong?")

def airShipPath_old(version):
    FFX_memory.clickToControl()
    
    checkpoint = 0
    lastCP = 0
    while checkpoint != 1000:
        if lastCP != checkpoint:
            print("Checkpoint: ", checkpoint)
            lastCP = checkpoint
        pos = FFX_memory.getCoords()
        if FFX_memory.userControl():
            if checkpoint == 0: #First room
                if pos[1] > 130:
                    checkpoint = 10
                else:
                    time.sleep(0.05)
                    FFXC.set_value('AxisLx', 1)
                    FFXC.set_value('AxisLy', -1)
            elif checkpoint == 10: #Rin's room
                if pos[0] > 60:
                    checkpoint = 20
                else:
                    time.sleep(0.05)
                    FFXC.set_value('AxisLy', -1)
                    if pos[1] > 80:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 20: #Isaaru's room
                if pos[0] < 1:
                    checkpoint = 30
                else:
                    time.sleep(0.05)
                    FFXC.set_value('AxisLy', -1)
                    if pos[1] < 70:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 30:
                if pos[1] < -90:
                    checkpoint = 40
                else:
                    time.sleep(0.05)
                    FFXC.set_value('AxisLy', -1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 40:
                if pos[0] < -30:
                    checkpoint = 50
                else:
                    time.sleep(0.05)
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', -1)
            elif checkpoint == 50:
                if pos[1] > -15:
                    if version == 1:
                        print("Pre-Evrae pathing")
                        checkpoint = 60
                    elif version == 2:
                        print("Talking to Yuna/Kimahri in the gallery")
                        checkpoint = 120
                    elif version == 3:
                        print("Straight to the deck, three skips.")
                        checkpoint = 150
                    elif version == 4:
                        print("Straight to the deck, talking to Yuna.")
                        checkpoint = 180
                    elif version == 5:
                        print("Final pathing. Sin's face.")
                        checkpoint = 200
                    elif version == 6:
                        print("Final pathing. Sin's face.")
                        checkpoint = 70
                    else:
                        print("Something maybe went wrong?")
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', 0)
                else:
                    time.sleep(0.05)
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            
            elif checkpoint == 60: #Pre-Evrae with items
                if pos[1] < -10:
                    checkpoint = 65
                else:
                    time.sleep(0.05)
                    FFXC.set_value('AxisLy', 1)
                    if pos[0] < -5:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            
             #Pre-Evrae with items
            elif checkpoint == 65:
                FFX_memory.awaitControl()
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.15)
                FFXC.set_value('AxisLy', 0)
                time.sleep(0.5)
                FFXC.set_value('AxisLx', 0)
                FFX_Xbox.SkipDialog(2.5) #Talk to Rin
                FFX_Screen.awaitPixel(600,408,(151, 151, 151))
                FFX_Xbox.menuB()
                time.sleep(1)
                FFX_Xbox.menuRight()
                time.sleep(0.5)
                FFX_Xbox.menuB()
                time.sleep(0.2)
                FFX_Xbox.menuB()
                time.sleep(0.2)
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB() #Sell old Tidus armor
                FFX_Xbox.menuA()
                time.sleep(0.1)
                FFX_Xbox.menuLeft()
                time.sleep(0.5)
                FFX_Xbox.menuB()
                time.sleep(0.2)
                FFX_Xbox.menuB()
                time.sleep(0.2)
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB() #Purchase Baroque sword
                time.sleep(0.1)
                FFX_Xbox.menuB() #Do not equip yet.
                FFX_Xbox.menuA()
                FFX_Xbox.menuA()
                
                FFX_memory.clickToControl()
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLx', 0)
                FFX_Xbox.SkipDialog(3)
                FFX_memory.awaitControl()
                FFX_Xbox.SkipDialog(5)
                FFXC.set_value('AxisLy', 0)
                checkpoint = 1000
                
            #Pre-Evrae, no items
            elif checkpoint == 70:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.5)
                FFXC.set_value('AxisLx', 0)
                SkipDialog(5)
                FFXC.set_value('AxisLy', 0)
                FFX_memory.awaitControl()
                
                FFXC.set_value('AxisLy', 1)
                time.sleep(2)
                FFXC.set_value('AxisLy', 0)
                
                checkpoint = 1000
            
            #Yuna/Kimahri in the gallery
            elif checkpoint == 120:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
                SkipDialog(2)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
                if FFX_memory.userControl():
                    print("Something went wrong. Trying the other way.")
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', -1)
                    SkipDialog(4)
                    FFXC.set_value('AxisLy', 0)
                    FFXC.set_value('AxisLx', 0)
                else:
                    checkpoint = 1000
                    FFX_memory.clickToControl()
            
            #Sin's arms
            elif checkpoint == 150:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.5)
                FFXC.set_value('AxisLx', 0)
                SkipDialog(4)
                FFXC.set_value('AxisLy', 0)
                FFX_memory.awaitControl()
                
                FFXC.set_value('AxisLy', 1)
                time.sleep(2)
                FFXC.set_value('AxisLy', 0)
                
                SkipDialog(64)
                skipScene()
                SkipDialog(6)
                skipScene()
                SkipDialog(26)
                skipScene()
                checkpoint = 1000
                
            #Yuna reflecting
            elif checkpoint == 180:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.5)
                FFXC.set_value('AxisLx', 0)
                SkipDialog(4)
                FFXC.set_value('AxisLy', 0)
                FFX_memory.awaitControl()
                
                FFXC.set_value('AxisLy', 1)
                time.sleep(2)
                FFXC.set_value('AxisLy', 0)
                
                FFX_memory.awaitControl()
                FFXC.set_value('AxisLx', -1)
                time.sleep(2.4)
                FFXC.set_value('AxisLy', 1)
                SkipDialog(0.5) #Hi Yuna. Let's have a quick chat.
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                SkipDialog(126)
                skipScene()
                checkpoint = 1000
                
            #Sin's face
            elif checkpoint == 200:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.5)
                FFXC.set_value('AxisLx', 0)
                SkipDialog(4)
                FFXC.set_value('AxisLy', 0)
                FFX_memory.awaitControl()
                
                FFXC.set_value('AxisLy', 1)
                time.sleep(2)
                FFXC.set_value('AxisLy', 0)
                time.sleep(6.5)
                skipScene()
                checkpoint = 1000
        elif FFX_Screen.BattleScreen():
            FFX_Battle.fleeAll()
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if FFX_memory.menuOpen():
                FFXC.set_value('BtnB', 1)
                time.sleep(0.035)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.035)
            elif checkpoint == 50:
                FFX_memory.clickToControl()

def airShipReturn():
    print("Conversation with Yuna/Kimahri.")
    FFX_memory.clickToControl()
    
    pos = FFX_memory.getCoords()
    print("Ready to run back to the cockpit.")
    while pos[1] > -90: #Leaving Yuna/Kimahri, heading back down.
        FFXC.set_value('AxisLy', -1)
        FFXC.set_value('AxisLx', 0)
        pos = FFX_memory.getCoords()
    print("Turn East")
    while pos[0] < -1:
        FFXC.set_value('AxisLx', 1)
        FFXC.set_value('AxisLy', 0)
        pos = FFX_memory.getCoords()
    print("Turn North")
    while FFX_memory.userControl():
        FFXC.set_value('AxisLx', 0)
        FFXC.set_value('AxisLy', 1)
        pos = FFX_memory.getCoords()
        
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.awaitControl()
    
    while FFX_memory.userControl():
        FFXC.set_value('AxisLx', 0)
        FFXC.set_value('AxisLy', 1)
        
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.awaitControl()
    
    while FFX_memory.userControl():
        pos = FFX_memory.getCoords()
        time.sleep(0.05)
        FFXC.set_value('AxisLy', 1)
        if pos[0] < -1:
            FFXC.set_value('AxisLx', 1)
        else:
            FFXC.set_value('AxisLx', 0)
            
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(1.2)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.5)
    
    while FFX_memory.userControl():
        FFXC.set_value('AxisLy', 1)
        FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
