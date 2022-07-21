import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_memory
import FFX_targetPathing
import FFX_vars
import math
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

def desert():
    FFX_memory.clickToControl()
    
    #Speed sphere stuff. Improve this later.
    needSpeed = False
    if FFX_memory.getSpeed() < 5:
        needSpeed = True
        #FFX_memory.setSpeed(9)
        #Reprogram battle logic to throw some kind of grenades.
    
    #Same for Power spheres
    if gameVars.nemesis():
        if FFX_memory.getPower() >= 26 or (FFX_memory.getSpeed() < 9 and FFX_memory.getPower() >= (20 + math.ceil((9 - FFX_memory.getSpeed()) / 2))) or (FFX_memory.getSpeed() >= 9 and FFX_memory.getPower() >= 20):
            needPower = False
        else:
            needPower = True
        
    elif FFX_memory.getPower() >= 18 or (FFX_memory.getSpeed() < 9 and FFX_memory.getPower() >= (14 + math.ceil((9 - FFX_memory.getSpeed()) / 2))) or (FFX_memory.getSpeed() >= 9 and FFX_memory.getPower() >= 14):
        needPower = False
    else:
        needPower = True
    
    #Logic for finding Teleport Spheres x2 (only chest in this area)
    teleSlot = FFX_memory.getItemSlot(98)
    if teleSlot == 255:
        teleCount = 0
    else:
        teleCount = FFX_memory.getItemCountSlot(teleSlot)
    
    
    chargeState = False #Rikku charge, speed spheres
    #Bomb cores, sleeping powders, smoke bombs, silence grenades
    stealItems = [0,0,0,0]
    itemsNeeded = 0
    
    #Now to figure out how many items we need.
    stealItems = FFX_Battle.updateStealItemsDesert()
    #if stealItems[0] == 2: #Bomb Cores aren't working right.
    #    itemsNeeded = 5 - (stealItems[1] + stealItems[2] + stealItems[3])
    #else:
    #    itemsNeeded = 7 - (stealItems[1] + stealItems[2] + stealItems[3])
    itemsNeeded = 8 - (stealItems[1] + stealItems[2] + stealItems[3])
    
    FFX_menu.equipSonicSteel()
    FFX_memory.closeMenu()
    
    checkpoint = 0
    firstFormat = False
    sandy1 = False
    while FFX_memory.getMap() != 130:
        if FFX_memory.userControl():
            #Map changes
            if checkpoint == 9:
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 11 and len(FFX_memory.getOrderSeven()) > 4:
                checkpoint += 1
            elif checkpoint < 39 and FFX_memory.getMap() == 137:
                checkpoint = 39
            elif checkpoint < 50 and FFX_memory.getMap() == 138:
                checkpoint = 50
            
            #Nemesis stuff
            elif checkpoint == 47 and gameVars.nemesis():
                checkpoint = 70
            elif checkpoint == 72:
                FFXC.set_neutral()
                FFX_memory.waitFrames(6)
                FFXC.set_movement(-1,0)
                FFX_memory.waitFrames(4)
                FFXC.set_neutral()
                FFX_memory.waitFrames(6)
                if FFX_memory.userControl():
                    FFX_Xbox.tapB()
                    FFX_memory.waitFrames(2)
                    FFX_memory.clickToControl()
                    checkpoint += 1
            elif checkpoint == 74:
                FFXC.set_neutral()
                FFX_memory.waitFrames(6)
                FFXC.set_movement(-1,0)
                FFX_memory.waitFrames(4)
                FFXC.set_neutral()
                FFX_memory.waitFrames(6)
                if FFX_memory.userControl():
                    FFX_Xbox.tapB()
                    FFX_memory.waitFrames(2)
                    FFX_memory.clickToControl()
                    checkpoint += 1
            elif checkpoint == 76:
                checkpoint = 48
            
            #Other events
            elif checkpoint == 2 or checkpoint == 24: #Save sphere
                FFXC.set_neutral()
                FFX_memory.waitFrames(30 * 0.2)
                FFX_memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 53:
                print("Going for first Sandragora and chest")
                teleSlot = FFX_memory.getItemSlot(98)
                if teleSlot == 255 or teleCount == FFX_memory.getItemCountSlot(teleSlot):
                    FFX_targetPathing.setMovement([-44,446])
                    FFX_Xbox.tapB()
                else:
                    checkpoint += 1
                    print("Checkpoint reached: ", checkpoint)
            elif checkpoint == 12 and firstFormat == False:
                firstFormat = True
                FFX_memory.fullPartyFormat('desert9')
                
            #Sandragora skip logic
            elif checkpoint == 57:
                #FFXC.set_neutral()
                #FFX_memory.waitFrames(10)
                checkpoint += 1
            elif checkpoint == 60:
                if FFX_memory.getCoords()[1] < 810:
                    FFXC.set_movement(0,1)
                else:
                    FFXC.set_neutral()
                    checkpoint += 1
            elif checkpoint == 61:
                if FFX_memory.getCoords()[1] < 810:
                    #Accidentally encountered Sandragora, must re-position.
                    checkpoint -= 2
                elif FFX_memory.getCoords()[1] < 840:
                    FFXC.set_neutral()
                else:
                    checkpoint += 1
            
            #After Sandy2 logic
            elif checkpoint == 64:
                if itemsNeeded >= 1: #Cannot move on if we're short on throwable items
                    checkpoint -= 2
                elif needSpeed == True: #Cannot move on if we're short on speed spheres
                    checkpoint -= 2
                else:
                    checkpoint += 1
            
            #General pathing
            elif FFX_memory.userControl():
                if FFX_targetPathing.setMovement(FFX_targetPathing.desert(checkpoint)) == True:
                    checkpoint += 1
                    print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible() and not FFX_memory.battleActive():
                FFX_Xbox.menuB()
            if FFX_memory.battleActive(): #Lots of battle logic here.
                FFX_Xbox.clickToBattle()
                if checkpoint < 7 and FFX_memory.getBattleNum() == 197: #First battle in desert
                    FFX_Battle.zu()
                elif FFX_memory.getBattleNum() == 234: #Sandragora logic
                    print("Sandragora fight")
                    if checkpoint < 55:
                        if sandy1 == False:
                            FFX_Battle.sandragora(1)
                            sandy1 = True
                        else:
                            FFX_Battle.fleeAll()
                    else:
                        FFX_Battle.sandragora(2)
                else:
                    FFX_Battle.bikanelBattleLogic([chargeState, needSpeed, needPower, itemsNeeded])
                
                #After-battle logic
                FFX_memory.clickToControl()
                
                #First, check and update party format.
                if checkpoint > 10:
                    if checkpoint < 23 and checkpoint > 10:
                        FFX_memory.fullPartyFormat('desert9')
                    elif chargeState == False:
                        FFX_memory.fullPartyFormat('desert1')
                    elif needPower == True:
                        FFX_memory.fullPartyFormat('desert1')
                    elif needSpeed == True:
                        FFX_memory.fullPartyFormat('desert1')
                    elif itemsNeeded >= 1:
                        FFX_memory.fullPartyFormat('desert1')
                    else: #Catchall
                        FFX_memory.fullPartyFormat('desert1')
                        #formerly desert2, but it works out better to have Kimahri in the fourth slot
                
                #Next, figure out how many items we need.
                stealItems = FFX_Battle.updateStealItemsDesert()
                print("-----------------------------")
                print("Items status: ", stealItems)
                print("-----------------------------")
                itemsNeeded = 8 - sum(stealItems)
                
                #Finally, check for other factors and report to console.
                if FFX_memory.overdriveState()[6] == 100:
                    chargeState = True
                #if FFX_memory.getSpeed() >= 5:
                if FFX_memory.getSpeed() >= 9:
                    needSpeed = False
                if gameVars.nemesis():
                    if FFX_memory.getPower() >= 26 or (FFX_memory.getSpeed() < 9 and FFX_memory.getPower() >= (20 + math.ceil((9 - FFX_memory.getSpeed()) / 2))) or (FFX_memory.getSpeed() >= 9 and FFX_memory.getPower() >= 20):
                        needPower = False
                    else:
                        needPower = True
                elif FFX_memory.getPower() >= 18 or (FFX_memory.getSpeed() < 9 and FFX_memory.getPower() >= (14 + math.ceil((9 - FFX_memory.getSpeed()) / 2))) or (FFX_memory.getSpeed() >= 9 and FFX_memory.getPower() >= 14):
                #if FFX_memory.getPower() >= 23:
                    needPower = False
                print("-----------------------------Flag statuses")
                print("Rikku is charged up: ", chargeState)
                print("Need more Speed spheres: ", needSpeed)
                print("Need more Power spheres: ", needPower)
                print("Number of additional items needed before Home: ", itemsNeeded)
                print("-----------------------------Flag statuses (end)")
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

def desert1():
    print("desert1 function no longer used.")

def findSummoners():
    print("Desert complete. Starting Home section")
    FFX_menu.homeGrid()
    
    checkpoint = 0
    while FFX_memory.getMap() != 261:
        if FFX_memory.userControl():
            #events
            if checkpoint == 7:
                FFXC.set_neutral()
                FFX_memory.touchSaveSphere()
                
                checkpoint += 1
            elif checkpoint < 12 and FFX_memory.getMap() == 276:
                checkpoint = 12
            elif checkpoint < 18 and FFX_memory.getMap() == 280:
                checkpoint = 19
            elif checkpoint == 34 and gameVars.nemesis():
                checkpoint = 60
            elif checkpoint == 63:
                FFX_memory.clickToEventTemple(6)
                checkpoint = 35
            elif checkpoint in [81,82,83] and FFX_memory.getMap() == 286: #Bonus room, blitzLoss only
                checkpoint = 84
            elif checkpoint == 86:
                FFXC.set_movement(0, 1)
                FFX_memory.clickToEvent()
                FFXC.set_neutral()
                FFX_memory.waitFrames(15)
                FFX_Xbox.tapB()
                FFX_memory.waitFrames(15)
                FFX_Xbox.tapLeft()
                FFX_Xbox.tapLeft()
                FFX_Xbox.tapB()
                FFX_memory.waitFrames(15)
                FFX_Xbox.tapLeft()
                FFX_Xbox.tapLeft()
                FFX_Xbox.tapLeft()
                FFX_Xbox.tapLeft()
                FFX_Xbox.tapB()
                FFX_memory.waitFrames(15)
                FFX_Xbox.tapRight()
                FFX_Xbox.tapRight()
                FFX_Xbox.tapRight()
                FFX_Xbox.tapRight()
                FFX_Xbox.tapB()
                FFX_memory.clickToControl()
                FFXC.set_movement(1, -1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 88:
                checkpoint = 21
            elif checkpoint == 20:
                if gameVars.getBlitzWin():
                    checkpoint = 21
                else:
                    checkpoint = 81
            #elif checkpoint < 27 and FFX_memory.getMap() == 280:
            #    checkpoint = 27
            elif checkpoint == 31 and not gameVars.csr():
                FFX_memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 39:
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 42:
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 45:
                FFX_memory.clickToEventTemple(1)
                checkpoint += 1
            elif FFX_targetPathing.setMovement(FFX_targetPathing.Home(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                if FFX_memory.getBattleNum() == 417:
                    print("Home, battle 1")
                    FFX_Battle.home1()
                elif FFX_memory.getBattleNum() == 419:
                    if FFX_memory.getMap() == 280:
                        print("Home, battle 2")
                        FFX_Battle.home2()
                        FFX_memory.fullPartyFormat('desert1')
                    else:
                        print("Home, bonus battle for Blitz loss")
                        FFX_Battle.home3()
                elif FFX_memory.getBattleNum() == 420:
                    print("Home, final battle")
                    FFX_Battle.home4()
                    FFX_memory.fullPartyFormat('evrae')
                else:
                    print("Flee from battle: ", FFX_memory.getBattleNum())
                    FFX_Battle.fleeAll()
            elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    print("Let's go get that airship!")
    FFXC.set_neutral()
    if not gameVars.csr():
        FFX_memory.clickToDiagProgress(27)
        #FFX_memory.waitFrames(30)
        #FFX_Xbox.tapB()
        while not FFX_memory.cutsceneSkipPossible():
            FFX_Xbox.tapB()
        FFX_Xbox.skipScene()
        FFX_memory.clickToDiagProgress(105)
        FFX_memory.waitFrames(15)
        FFX_Xbox.tapB()
        FFX_memory.waitFrames(15)
        FFX_Xbox.skipScene()
    
    while not FFX_memory.userControl():
        if FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
        elif FFX_memory.cutsceneSkipPossible():
            FFX_Xbox.skipScene()
    print("Airship is good to go. Now for Yuna.")