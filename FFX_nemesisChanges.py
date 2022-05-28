import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory
import FFX_targetPathNem
import FFX_vars
import FFX_Gagazet
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()

#The following functions replace the default ones from the regular Bahamut run.

def arenaNPC():
    FFX_memory.awaitControl()
    if FFX_memory.getMap() != 307:
        return
    while not (FFX_memory.diagProgressFlag() == 74 and FFX_memory.diagSkipPossible()):
        if FFX_memory.userControl():
            if FFX_memory.getCoords()[1] > -12:
                FFXC.set_movement(0,-1)
                FFX_memory.waitFrames(1)
            else:
                FFX_targetPathNem.setMovement([2,-15])
                FFX_Xbox.tapB()
        else:
            FFXC.set_neutral()
            if FFX_memory.diagProgressFlag() == 59:
                FFX_Xbox.menuA()
                FFX_Xbox.menuA()
                FFX_Xbox.menuA()
                FFX_Xbox.menuA()
                FFX_Xbox.tapB()
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    FFX_memory.waitFrames(3)

def nextRace():
    FFXC.set_neutral()
    FFX_memory.clickToDiagProgress(28)
    FFX_memory.waitFrames(9)
    FFX_Xbox.tapB()

def calmLands():
    #Start chocobo races
    #FFX_memory.setGameSpeed(2)
    calmLands_1()
    
    FFXC.set_neutral()
    FFX_memory.clickToDiagProgress(28)
    FFX_memory.waitFrames(9)
    FFX_Xbox.tapB()
    #FFX_memory.setGameSpeed(0)
    wobblyComplete = False
    while not wobblyComplete:
        wobblyComplete = chocoTame1()
    
    print("Wobbly Chocobo complete")
    #nextRace()
    #dodgerComplete = False
    #while not dodgerComplete:
    #    dodgerComplete = chocoTame2()
    
    #print("Dodger Chocobo complete")
    #nextRace()
    
    #hyperComplete = False
    #while not hyperComplete:
    #    hyperComplete = chocoTame3()
    
    #print("Hyper Chocobo complete")
    
    #catcherComplete = False
    #while not catcherComplete:
    #    catcherComplete = chocoTame4()
    
    print("Catcher Chocobo complete")
    
    toRemiem()

def calmLands_1():
    #Enter the cutscene that starts Calm Lands
    FFX_memory.fullPartyFormat('yuna', fullMenuClose=False)
    FFX_menu.prepCalmLands()
    while not (FFX_memory.getCoords()[1] >= -1650 and FFX_memory.userControl()):
        if FFX_memory.userControl():
            FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    
    #Now head to the chocobo lady.
    #FFX_memory.setEncounterRate(0) #Testing only
    checkpoint = 0
    while FFX_memory.getMap() != 307:
        if FFX_memory.userControl():
            #if checkpoint == 10:
            #    if FFX_Gagazet.checkGems() < 2:
            #        checkpoint -= 2
            if FFX_targetPathNem.setMovement(FFX_targetPathNem.calmLands1(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                if FFX_Gagazet.checkGems() < 2:
                    FFX_Battle.calmLandsGems()
                else:
                    FFX_Battle.calmLandsManip()
                FFX_memory.fullPartyFormat('yuna')
            elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    
    print("Now talk to NPC")
    #arenaNPC()
    #arenaPurchase()
    #FFX_memory.waitFrames(6)
    #FFX_Xbox.tapB() #I want to ride a chocobo.

def chocoTame1():
    FFX_memory.clickToDiagProgress(43)
    while not FFX_memory.diagProgressFlag() in [44,74]:
        angle = FFX_memory.getActorAngle(0)
        #print("Angle: ", retVal)
        position = FFX_memory.getActorCoords(0)
        #print("Position: ", position)
        if position[0] < -110: #Need to move right
            if angle > 1.4:
                FFXC.set_value('Dpad', 8)
            elif angle < 1.2:
                FFXC.set_value('Dpad', 4)
            else:
                FFXC.set_value('Dpad', 0)
        elif position[0] > -60: #Need to move left
            if angle > 1.8:
                FFXC.set_value('Dpad', 8)
            elif angle < 1.6:
                FFXC.set_value('Dpad', 4)
            else:
                FFXC.set_value('Dpad', 0)
        else:
            if angle > 1.6: #Stay straight
                FFXC.set_value('Dpad', 8)
            elif angle < 1.4:
                FFXC.set_value('Dpad', 4)
            else:
                FFXC.set_value('Dpad', 0)
    FFXC.set_neutral()
    
    while not FFX_memory.diagProgressFlag() in [51,69,74]:
        #51 is success
        FFX_Xbox.tapB()
    if FFX_memory.diagProgressFlag() == 51: #Success
        FFX_memory.clickToDiagProgress(77)
        FFX_memory.waitFrames(12)
        FFX_Xbox.tapDown() #Up for next race, down for quit
        FFX_Xbox.tapB()
        #FFX_memory.waitFrames(20)
        FFX_Xbox.tapUp()
        FFX_Xbox.tapB()
        return True
    else:
        FFX_memory.clickToDiagProgress(76)
        FFX_memory.waitFrames(12)
        FFX_Xbox.tapB()
        return False

def chocoTame2():
    FFX_memory.clickToDiagProgress(43)
    checkpoint = 0
    while not FFX_memory.diagProgressFlag() in [44,74]:
        angle = FFX_memory.getActorAngle(0)
        position = FFX_memory.getActorCoords(0)
        
        if position[1] > -1360 and checkpoint == 0: #Start off aiming right to manip balls
            checkpoint += 1
            FFXC.set_value('Dpad', 8) #Right
            FFX_memory.waitFrames(5)
            FFXC.set_value('Dpad', 0)
        if position[1] > -1200 and checkpoint == 1: #Slight left
            checkpoint += 1
            FFXC.set_value('Dpad', 4) #Left
            FFX_memory.waitFrames(11)
            FFXC.set_value('Dpad', 0)
        if position[1] > -1000 and checkpoint == 2: #Straighten out
            checkpoint += 1
            FFXC.set_value('Dpad', 8) #Right
            FFX_memory.waitFrames(7)
            FFXC.set_value('Dpad', 0)
        if position[1] > -800 and checkpoint == 3: #Juke right
            checkpoint += 1
            FFXC.set_value('Dpad', 8) #Right
            FFX_memory.waitFrames(5)
            FFXC.set_value('Dpad', 0)
        if position[1] > -650 and checkpoint == 4: #Back to the left
            checkpoint += 1
            FFXC.set_value('Dpad', 4) #Left
            FFX_memory.waitFrames(11)
            FFXC.set_value('Dpad', 0)
        if position[1] > -550 and checkpoint == 5: #Straighten out
            checkpoint += 1
            FFXC.set_value('Dpad', 8) #Right
            FFX_memory.waitFrames(6)
            FFXC.set_value('Dpad', 0)
        if position[1] > -450 and checkpoint == 6: #Juke right again
            checkpoint += 1
            FFXC.set_value('Dpad', 8)
            FFX_memory.waitFrames(6)
            FFXC.set_value('Dpad', 0)
        if position[1] > -250 and checkpoint == 7: #Straighten out
            checkpoint += 1
            FFXC.set_value('Dpad', 4)
            FFX_memory.waitFrames(14)
            FFXC.set_value('Dpad', 0)
        if position[1] > -90 and checkpoint == 8: #The final juke!
            checkpoint += 1
            FFXC.set_value('Dpad', 8)
            FFX_memory.waitFrames(13)
            FFXC.set_value('Dpad', 0)
    FFXC.set_neutral()

    while not FFX_memory.diagProgressFlag() in [54,69,77]:
        #54 is success
        FFX_Xbox.tapB()
    if FFX_memory.diagProgressFlag() == 54: #Success
        FFX_memory.clickToDiagProgress(77)
        FFX_memory.waitFrames(12)
        FFX_Xbox.tapUp()
        FFX_Xbox.tapB()
        FFX_memory.waitFrames(30)
        FFX_Xbox.tapUp()
        FFX_Xbox.tapB()
        return True
    else:
        FFX_memory.clickToDiagProgress(77)
        FFX_memory.waitFrames(12)
        FFX_Xbox.tapB()
        return False

def chocoTame3():
    FFX_memory.clickToDiagProgress(43)
    checkpoint = 0
    while not FFX_memory.diagProgressFlag() in [44,74]:
        position = FFX_memory.getActorCoords(0)
        if position[1] > -1370 and checkpoint == 0:
            checkpoint += 1
            FFXC.set_value('Dpad', 4) #Left
            FFX_memory.waitFrames(3)
            FFXC.set_value('Dpad', 0)
        if position[1] > -1200 and checkpoint == 1:
            checkpoint += 1
            FFXC.set_value('Dpad', 8) #Right
            FFX_memory.waitFrames(10)
            FFXC.set_value('Dpad', 0)
        if position[1] > -1100 and checkpoint == 2:
            checkpoint += 1
            FFXC.set_value('Dpad', 4)
            FFX_memory.waitFrames(12)
            FFXC.set_value('Dpad', 0)
        if position[1] > -1040 and checkpoint == 3:
            checkpoint += 1
            FFXC.set_value('Dpad', 8)
            FFX_memory.waitFrames(9)
            FFXC.set_value('Dpad', 0)
        if position[1] > -950 and checkpoint == 4:
            checkpoint += 1
            FFXC.set_value('Dpad', 4)
            FFX_memory.waitFrames(12)
            FFXC.set_value('Dpad', 0)
        if position[1] > -700 and checkpoint == 5:
            checkpoint += 1
            FFXC.set_value('Dpad', 8)
            FFX_memory.waitFrames(12)
            FFXC.set_value('Dpad', 0)
        if position[1] > -600 and checkpoint == 6:
            checkpoint += 1
            FFXC.set_value('Dpad', 4)
            FFX_memory.waitFrames(12)
            FFXC.set_value('Dpad', 0)
        if position[1] > -500 and checkpoint == 7:
            checkpoint += 1
            FFXC.set_value('Dpad', 4)
            FFX_memory.waitFrames(6)
            FFXC.set_value('Dpad', 0)
        if position[1] > -400 and checkpoint == 8:
            checkpoint += 1
            FFXC.set_value('Dpad', 8)
            FFX_memory.waitFrames(16)
            FFXC.set_value('Dpad', 0)
        if position[1] > -250 and checkpoint == 9:
            checkpoint += 1
            FFXC.set_value('Dpad', 4)
            FFX_memory.waitFrames(16)
            FFXC.set_value('Dpad', 0)
        if position[1] > -120 and checkpoint == 10: #Still dialing in on this one.
            checkpoint += 1
            FFXC.set_value('Dpad', 8)
            FFX_memory.waitFrames(16)
            FFXC.set_value('Dpad', 0)
        if position[1] > -20 and checkpoint == 11:
            checkpoint += 1
            FFXC.set_value('Dpad', 4)
            FFX_memory.waitFrames(10)
            FFXC.set_value('Dpad', 0)
    FFXC.set_neutral()

    while not FFX_memory.diagProgressFlag() in [56,69,77]:
        #56 is success
        FFX_Xbox.tapB()
    if FFX_memory.diagProgressFlag() == 56: #Success
        FFX_memory.clickToDiagProgress(77)
        FFX_memory.waitFrames(12)
        FFX_Xbox.tapDown() #Up for something else, down for done.
        FFX_Xbox.tapB()
        FFX_memory.waitFrames(30)
        #FFX_Xbox.tapUp()
        #FFX_Xbox.tapB()
        return True
    else:
        FFX_memory.clickToDiagProgress(77)
        FFX_memory.waitFrames(12)
        FFX_Xbox.tapB()
        return False

def chocoTame4():
    print("START - CATCHER CHOCOBO")
    FFX_memory.clickToDiagProgress(43)
    checkpoint = 0
    while not FFX_memory.diagProgressFlag() in [44,67]:
        angle = FFX_memory.getActorAngle(0)
        position = FFX_memory.getActorCoords(0)
        print("User control")
        '''
        if position[1] > -1360 and checkpoint == 0: #Start off aiming right to manip balls
            checkpoint += 1
            FFXC.set_value('Dpad', 8) #Right
            FFX_memory.waitFrames(5)
            FFXC.set_value('Dpad', 0)
        if position[1] > -1200 and checkpoint == 1: #Slight left
            checkpoint += 1
            FFXC.set_value('Dpad', 4)#Left
            FFX_memory.waitFrames(10)
            FFXC.set_value('Dpad', 0)
        if position[1] > -770 and checkpoint == 3: #Left between balls
            checkpoint += 1
            FFXC.set_value('Dpad', 4)#Left
            FFX_memory.waitFrames(10)
            FFXC.set_value('Dpad', 0)
        if position[1] > -600 and checkpoint == 4: #Straighten out
            checkpoint += 1
            FFXC.set_value('Dpad', 8) #Right
            FFX_memory.waitFrames(6)
            FFXC.set_value('Dpad', 0)
        if position[1] > -100:
            if position[0] > -40:
                FFXC.set_value('Dpad', 4)#Left
            elif position[0] < -100:
                FFXC.set_value('Dpad', 8) #Right
            elif angle > 1.7:
                FFXC.set_value('Dpad', 8) #Right
            elif angle < 1.3:
                FFXC.set_value('Dpad', 4)#Left
            else:
                FFXC.set_value('Dpad', 0)
    '''
    print("Race complete.")
    FFXC.set_neutral()

    while not FFX_memory.diagProgressFlag() in [67,77]:
        #67 is 0:00.0 run
        FFX_Xbox.tapB()
    if FFX_memory.diagProgressFlag() == 67: #Success
        print("Great run! Perfect score!")
        FFX_memory.clickToDiagProgress(77)
        FFX_memory.waitFrames(12)
        FFX_Xbox.tapDown()
        FFX_Xbox.tapB()
        return True
    else:
        FFX_memory.clickToDiagProgress(77)
        FFX_memory.waitFrames(12)
        FFX_Xbox.tapB()
        return False

def toRemiem():
    FFX_memory.clickToControl()
    while FFX_memory.userControl():
        FFX_targetPathNem.setMovement([-1565,434])
        FFX_Xbox.tapB()
        print("Near chocobo lady")
    FFXC.set_neutral()
    FFX_memory.clickToControl3()
    
    checkpoint = 0
    while checkpoint < 35:
        if FFX_memory.userControl():
            if FFX_memory.getMap() == 290 and checkpoint < 13:
                checkpoint = 13
            
            elif checkpoint == 10:
                print("Feather")
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 27:
                print("Orb thing")
                while FFX_memory.userControl():
                    FFX_targetPathNem.setMovement([770,631])
                    FFX_Xbox.tapB()
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.toRemiem(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)

def remiemRaces():
    print("Ready to start races")
    chocoRace1()
    print("Celestial Weapon obtained.")
    #chocoRace2()
    #print("Obtained")
    #chocoRace3()
    #print("Something obtained")
    print("Now heading back to the monster arena.")

def chocoRace1():
    while FFX_memory.userControl():
        FFX_targetPathNem.setMovement([790,60])
        FFX_Xbox.tapB()
    FFXC.set_neutral()
    FFX_memory.clickToControl()
    checkpoint = 0
    while checkpoint != 37:
        if FFX_memory.userControl():
            if FFX_targetPathNem.setMovement(FFX_targetPathNem.race1(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                FFX_Battle.fleeAll()
            else:
                FFX_Xbox.tapB()
    FFXC.set_movement(-1,1)
    FFX_memory.waitFrames(10)
    FFXC.set_neutral()
    FFX_memory.clickToControl3()

def chocoRace2():
    FFXC.set_neutral()
    FFX_memory.clickToControl()
    while FFX_memory.userControl():
        FFX_targetPathNem.setMovement([790,60])
        FFX_Xbox.tapB()
    FFXC.set_neutral()
    checkpoint = 0
    while checkpoint != 38:
        if FFX_memory.userControl():
            if checkpoint == 11:
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            if checkpoint == 17:
                FFX_memory.clickToEventTemple(5)
                checkpoint += 1
            if checkpoint == 22:
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            if FFX_targetPathNem.setMovement(FFX_targetPathNem.race2(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                FFX_Battle.fleeAll()
            else:
                FFX_Xbox.tapB()
    FFXC.set_movement(-1,1)
    FFX_memory.waitFrames(10)
    FFXC.set_neutral()
    FFX_memory.clickToControl3()

def chocoRace3():
    FFXC.set_neutral()
    FFX_memory.clickToControl()
    while FFX_memory.userControl():
        FFX_targetPathNem.setMovement([790,60])
        FFX_Xbox.tapB()
    FFXC.set_neutral()
    checkpoint = 0
    while checkpoint != 44:
        if FFX_memory.userControl():
            if checkpoint == 11:
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            if checkpoint == 17:
                FFX_memory.clickToEventTemple(5)
                checkpoint += 1
            if checkpoint == 22:
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            if checkpoint == 27:
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            if checkpoint == 39:
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            #if checkpoint == 42: #Since it's not tight enough movement yet
            #    FFXC.set_neutral()
            #    FFX_memory.waitFrames(120)
            #    FFX_memory.clickToControl3()
            #    break
            if FFX_targetPathNem.setMovement(FFX_targetPathNem.race3(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                FFX_Battle.fleeAll()
            else:
                FFX_Xbox.tapB()
    FFXC.set_movement(-1,1)
    FFX_memory.waitFrames(60)
    FFXC.set_neutral()
    FFX_memory.clickToControl3()

def templeToArena():
    FFX_memory.clickToControl3()
    checkpoint = 0
    while FFX_memory.getMap() != 307:
        if FFX_memory.userControl():
            if FFX_memory.getMap() == 223 and checkpoint < 18:
                checkpoint = 18
            
            elif checkpoint == 20:
                while FFX_memory.userControl():
                    FFX_targetPathNem.setMovement([1261,-1238])
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                FFX_memory.clickToControl()
                checkpoint += 1
            
            elif checkpoint == 24:
                print("Feather")
                while FFX_memory.userControl():
                    FFX_targetPathNem.setMovement([1101,-940])
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                FFX_memory.awaitControl()
                checkpoint += 1
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.leaveRemiem(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)

def arenaPurchase():
    FFX_memory.clickToControl()
    
    print("Straight forward to the guy")
    FFXC.set_movement(0, 1)
    FFX_memory.clickToEvent()
    FFXC.set_neutral()
    print("Now for dialog")
    FFX_memory.clickToDiagProgress(65)
    print("Select Sure")
    FFX_memory.waitFrames(15)
    FFX_Xbox.tapDown()
    FFX_Xbox.tapB()
    FFX_memory.clickToDiagProgress(73)
    FFX_memory.waitFrames(15)
    #FFX_Xbox.tapUp()
    FFX_Xbox.tapB() #Let's see your weapons
    #FFX_memory.waitFrames(9000)
    FFX_menu.arenaPurchase1()
    #Sell all undesirable equipment
    #Purchase the following weapons:
    #-Tidus x4
    #-Yuna x1
        
    #---Done buying.
    FFX_memory.awaitControl()
    FFX_memory.waitFrames(2)
    FFXC.set_movement(0, -1)
    FFX_memory.awaitEvent() #Exit the arena map
    FFXC.set_neutral()
    FFX_memory.awaitControl()
    
    checkpoint = 0
    while FFX_memory.getMap() != 279:
        if FFX_memory.userControl():
            if checkpoint == 7 and FFX_Gagazet.checkGems() < 2:
                checkpoint -= 2
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.calmLands2(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                if FFX_Gagazet.checkGems() < 2:
                    FFX_Battle.calmLandsGems()
                else:
                    FFX_Battle.calmLandsManip()
                FFX_memory.fullPartyFormat('yuna')
            elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    

def arenaPurchaseWithChocobo():
    while FFX_memory.userControl(): #Back onto chocobo
        FFX_targetPathNem.setMovement([1347,-69])
        FFX_Xbox.tapB()
    
    while not FFX_targetPathNem.setMovement([1488,778]):
        pass
    while not FFX_targetPathNem.setMovement([1545,1088]):
        pass
    while not FFX_memory.getMap() == 279:
        FFX_targetPathNem.setMovement([1700,1200])
    
    FFX_memory.fullPartyFormat('kimahri')