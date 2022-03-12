import FFX_memory
import FFX_Screen
import FFX_Battle
import FFX_targetPathing
import math
import time
import FFX_vars
gameVars = FFX_vars.varsHandle()

import FFX_Xbox
FFXC = FFX_Xbox.controllerHandle()

def airShipPath(version):
    FFX_memory.clickToControl()
    distillerPurchase = False
    
    complete = False
    checkpoint = 0
    while complete == False:
        if FFX_memory.userControl():
            #print(gameVars.csr()) #Testing only
            #print("Checkpoint: ", checkpoint)
            #Map changes
            if checkpoint == 2:
                FFX_memory.clickToEventTemple(3)
                checkpoint += 1
            elif version == 1 and distillerPurchase == False and checkpoint == 5 and \
                (FFX_memory.getSpeed() < 9 or FFX_memory.getPower() < 23):
                
                #Tyton to update this with the actual purchase.
                while FFX_memory.diagProgressFlag() != 44:
                    if FFX_memory.userControl():
                        FFX_targetPathing.setMovement([-6,6])
                        FFX_Xbox.tapB()
                    else:
                        FFXC.set_neutral()
                        if FFX_memory.battleActive():
                            FFX_Battle.fleeAll()
                        elif FFX_memory.menuOpen():
                            FFX_Xbox.tapB()
                FFXC.set_neutral()
                FFX_memory.clickToDiagProgress(48)
                while FFX_memory.airshipShopDialogueRow() != 1:
                    FFX_Xbox.tapDown()
                while not FFX_memory.itemShopMenu() == 7:
                    FFX_Xbox.tapB() #Click through until items menu comes up
                while not FFX_memory.itemShopMenu() == 10:
                    FFX_Xbox.tapB() #Select buy command
                if FFX_memory.getPower() < 23:
                    while FFX_memory.equipBuyRow() != 7:
                        if FFX_memory.equipBuyRow() < 7:
                            FFX_Xbox.tapDown()
                        else:
                            FFX_Xbox.tapUp()
                    while not FFX_memory.itemShopMenu() == 16:
                        FFX_Xbox.tapB()
                    while FFX_memory.purchasingAmountItems() != min(math.ceil((23 - FFX_memory.getPower()) / 2), 3):
                        if FFX_memory.purchasingAmountItems() < min(math.ceil((23 - FFX_memory.getPower()) / 2), 3):
                            FFX_Xbox.tapRight()
                        else:
                            FFX_Xbox.tapLeft()
                    while not FFX_memory.itemShopMenu() == 10:
                        FFX_Xbox.tapB()
                if FFX_memory.getSpeed() < 9:
                    while FFX_memory.equipBuyRow() != 9:
                        if FFX_memory.equipBuyRow() < 9:
                            FFX_Xbox.tapDown()
                        else:
                            FFX_Xbox.tapUp()
                    while not FFX_memory.itemShopMenu() == 16:
                        FFX_Xbox.tapB()
                    while FFX_memory.purchasingAmountItems() != min(math.ceil((9 - FFX_memory.getSpeed()) / 2), 2):
                        if FFX_memory.purchasingAmountItems() < min(math.ceil((9 - FFX_memory.getSpeed()) / 2), 2):
                            FFX_Xbox.tapRight()
                        else:
                            FFX_Xbox.tapLeft()
                    while not FFX_memory.itemShopMenu() == 10:
                        FFX_Xbox.tapB()
                FFX_memory.closeMenu()
                FFX_memory.clickToControl3()
                distillerPurchase = True
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
            elif checkpoint == 24:
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            
            #Return trip map changes
            elif checkpoint in [32,34]: #Formerly included 13
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 37:
                FFX_memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 40:
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint in [43,44] and not gameVars.csr():
                checkpoint = 45
            elif checkpoint == 44: #Talk to Cid
                while FFX_memory.userControl():
                    FFX_targetPathing.setMovement([-250,339])
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                complete = True
            elif checkpoint == 46: #Talk to Cid
                while FFX_memory.userControl():
                    FFX_targetPathing.setMovement([-230,366])
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                complete = True
            
            #Complete states
            elif checkpoint == 19 and version == 1:
                print("Pre-Evrae pathing")
                FFXC.set_movement(0, 1)
                FFX_memory.waitFrames(30 * 3)
                FFXC.set_neutral()
                complete = True
            elif checkpoint == 19 and version == 3:
                print("Sin's Arms")
                FFXC.set_movement(0, 1)
                FFX_memory.waitFrames(30 * 3)
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
                FFX_memory.waitFrames(30 * 3)
                FFXC.set_neutral()
                FFX_memory.awaitControl()
                FFX_targetPathing.setMovement([-2,-15])
                FFX_memory.waitFrames(30 * 0.5)
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
                FFX_memory.waitFrames(30 * 3)
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
                FFX_memory.waitFrames(30 * 3)
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
                print("Mark")
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
        FFX_memory.waitFrames(30 * 0.05)
        FFXC.set_value('AxisLy', 1)
        if pos[0] < -1:
            FFXC.set_value('AxisLx', 1)
        else:
            FFXC.set_value('AxisLx', 0)
            
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    FFX_memory.waitFrames(30 * 1.2)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', -1)
    FFX_memory.waitFrames(30 * 0.5)
    
    while FFX_memory.userControl():
        FFXC.set_value('AxisLy', 1)
        FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
