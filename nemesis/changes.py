import xbox
import battle.main as main
import menu
import memory.main as main
import nemesis.targetPath as targetPath
import vars
import area.gagazet as gagazet
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


# The following functions replace the default ones from the regular Bahamut run.

def arenaNPC():
    main.awaitControl()
    if main.getMap() != 307:
        return
    while not (main.diagProgressFlag() == 74 and main.diagSkipPossible()):
        if main.userControl():
            if main.getCoords()[1] > -12:
                FFXC.set_movement(0, -1)
                main.waitFrames(1)
            else:
                targetPath.setMovement([2, -15])
                xbox.tapB()
        else:
            FFXC.set_neutral()
            if main.diagProgressFlag() == 59:
                xbox.menuA()
                xbox.menuA()
                xbox.menuA()
                xbox.menuA()
                xbox.tapB()
            elif main.diagSkipPossible():
                xbox.tapB()
    main.waitFrames(3)


def nextRace():
    FFXC.set_neutral()
    main.clickToDiagProgress(28)
    main.waitFrames(9)
    xbox.tapB()


def calmLands():
    # Start chocobo races
    # memory.setGameSpeed(2)
    calmLands_1()
    
    FFXC.set_neutral()
    main.clickToDiagProgress(28)
    main.waitFrames(9)
    xbox.tapB()
    # memory.setGameSpeed(0)
    wobblyComplete = False
    while not wobblyComplete:
        wobblyComplete = chocoTame1()
    
    print("Wobbly Chocobo complete")
    # nextRace()
    # dodgerComplete = False
    # while not dodgerComplete:
    #     dodgerComplete = chocoTame2()

    # print("Dodger Chocobo complete")
    # nextRace()

    # hyperComplete = False
    # while not hyperComplete:
    #     hyperComplete = chocoTame3()

    # print("Hyper Chocobo complete")

    # catcherComplete = False
    # while not catcherComplete:
    #     catcherComplete = chocoTame4()

    print("Catcher Chocobo complete")

    toRemiem()

def calmLands_1():
    #Enter the cutscene that starts Calm Lands
    main.fullPartyFormat('yuna', fullMenuClose=True)
    while not (main.getCoords()[1] >= -1650 and main.userControl()):
        if main.userControl():
            FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()
            if main.diagSkipPossible():
                xbox.tapB()
    
    # Now head to the chocobo lady.
    # memory.setEncounterRate(0) #Testing only
    checkpoint = 0
    while main.getMap() != 307:
        if main.userControl():
            # if checkpoint == 10:
            #     if gagazet.checkGems() < 2:
            #         checkpoint -= 2
            if targetPath.setMovement(targetPath.calmLands1(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if main.battleActive():
                if gagazet.checkGems() < 2:
                    main.calmLandsGems()
                else:
                    main.calmLandsManip()
                main.fullPartyFormat('yuna')
            elif main.menuOpen() or main.diagSkipPossible():
                xbox.tapB()
    
    print("Now talk to NPC")
    # arenaNPC()
    # arenaPurchase()
    # memory.waitFrames(6)
    # xbox.tapB() #I want to ride a chocobo.


def chocoTame1():
    main.clickToDiagProgress(43)
    while not main.diagProgressFlag() in [44, 74]:
        angle = main.getActorAngle(0)
        # print("Angle: ", retVal)
        position = main.getActorCoords(0)
        # print("Position: ", position)
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
    
    while not main.diagProgressFlag() in [51, 69, 74]:
        # 51 is success
        xbox.tapB()
    if main.diagProgressFlag() == 51: #Success
        main.clickToDiagProgress(77)
        main.waitFrames(12)
        xbox.tapDown() #Up for next race, down for quit
        xbox.tapB()
        # memory.waitFrames(20)
        xbox.tapUp()
        xbox.tapB()
        return True
    else:
        main.clickToDiagProgress(76)
        main.waitFrames(12)
        xbox.tapB()
        return False

def chocoTame2():
    main.clickToDiagProgress(43)
    checkpoint = 0
    while not main.diagProgressFlag() in [44,74]:
        angle = main.getActorAngle(0)
        position = main.getActorCoords(0)
        
        if position[1] > -1360 and checkpoint == 0: #Start off aiming right to manip balls
            checkpoint += 1
            FFXC.set_value('Dpad', 8) #Right
            main.waitFrames(5)
            FFXC.set_value('Dpad', 0)
        if position[1] > -1200 and checkpoint == 1: #Slight left
            checkpoint += 1
            FFXC.set_value('Dpad', 4) #Left
            main.waitFrames(11)
            FFXC.set_value('Dpad', 0)
        if position[1] > -1000 and checkpoint == 2: #Straighten out
            checkpoint += 1
            FFXC.set_value('Dpad', 8) #Right
            main.waitFrames(7)
            FFXC.set_value('Dpad', 0)
        if position[1] > -800 and checkpoint == 3: #Juke right
            checkpoint += 1
            FFXC.set_value('Dpad', 8) #Right
            main.waitFrames(5)
            FFXC.set_value('Dpad', 0)
        if position[1] > -650 and checkpoint == 4: #Back to the left
            checkpoint += 1
            FFXC.set_value('Dpad', 4) #Left
            main.waitFrames(11)
            FFXC.set_value('Dpad', 0)
        if position[1] > -550 and checkpoint == 5: #Straighten out
            checkpoint += 1
            FFXC.set_value('Dpad', 8) #Right
            main.waitFrames(6)
            FFXC.set_value('Dpad', 0)
        if position[1] > -450 and checkpoint == 6: #Juke right again
            checkpoint += 1
            FFXC.set_value('Dpad', 8)
            main.waitFrames(6)
            FFXC.set_value('Dpad', 0)
        if position[1] > -250 and checkpoint == 7: #Straighten out
            checkpoint += 1
            FFXC.set_value('Dpad', 4)
            main.waitFrames(14)
            FFXC.set_value('Dpad', 0)
        if position[1] > -90 and checkpoint == 8: #The final juke!
            checkpoint += 1
            FFXC.set_value('Dpad', 8)
            main.waitFrames(13)
            FFXC.set_value('Dpad', 0)
    FFXC.set_neutral()

    while not main.diagProgressFlag() in [54,69,77]:
        #54 is success
        xbox.tapB()
    if main.diagProgressFlag() == 54: #Success
        main.clickToDiagProgress(77)
        main.waitFrames(12)
        xbox.tapUp()
        xbox.tapB()
        main.waitFrames(30)
        xbox.tapUp()
        xbox.tapB()
        return True
    else:
        main.clickToDiagProgress(77)
        main.waitFrames(12)
        xbox.tapB()
        return False

def chocoTame3():
    main.clickToDiagProgress(43)
    checkpoint = 0
    while not main.diagProgressFlag() in [44,74]:
        position = main.getActorCoords(0)
        if position[1] > -1370 and checkpoint == 0:
            checkpoint += 1
            FFXC.set_value('Dpad', 4) #Left
            main.waitFrames(3)
            FFXC.set_value('Dpad', 0)
        if position[1] > -1200 and checkpoint == 1:
            checkpoint += 1
            FFXC.set_value('Dpad', 8) #Right
            main.waitFrames(10)
            FFXC.set_value('Dpad', 0)
        if position[1] > -1100 and checkpoint == 2:
            checkpoint += 1
            FFXC.set_value('Dpad', 4)
            main.waitFrames(12)
            FFXC.set_value('Dpad', 0)
        if position[1] > -1040 and checkpoint == 3:
            checkpoint += 1
            FFXC.set_value('Dpad', 8)
            main.waitFrames(9)
            FFXC.set_value('Dpad', 0)
        if position[1] > -950 and checkpoint == 4:
            checkpoint += 1
            FFXC.set_value('Dpad', 4)
            main.waitFrames(12)
            FFXC.set_value('Dpad', 0)
        if position[1] > -700 and checkpoint == 5:
            checkpoint += 1
            FFXC.set_value('Dpad', 8)
            main.waitFrames(12)
            FFXC.set_value('Dpad', 0)
        if position[1] > -600 and checkpoint == 6:
            checkpoint += 1
            FFXC.set_value('Dpad', 4)
            main.waitFrames(12)
            FFXC.set_value('Dpad', 0)
        if position[1] > -500 and checkpoint == 7:
            checkpoint += 1
            FFXC.set_value('Dpad', 4)
            main.waitFrames(6)
            FFXC.set_value('Dpad', 0)
        if position[1] > -400 and checkpoint == 8:
            checkpoint += 1
            FFXC.set_value('Dpad', 8)
            main.waitFrames(16)
            FFXC.set_value('Dpad', 0)
        if position[1] > -250 and checkpoint == 9:
            checkpoint += 1
            FFXC.set_value('Dpad', 4)
            main.waitFrames(16)
            FFXC.set_value('Dpad', 0)
        if position[1] > -120 and checkpoint == 10: #Still dialing in on this one.
            checkpoint += 1
            FFXC.set_value('Dpad', 8)
            main.waitFrames(16)
            FFXC.set_value('Dpad', 0)
        if position[1] > -20 and checkpoint == 11:
            checkpoint += 1
            FFXC.set_value('Dpad', 4)
            main.waitFrames(10)
            FFXC.set_value('Dpad', 0)
    FFXC.set_neutral()

    while not main.diagProgressFlag() in [56, 69, 77]:
        # 56 is success
        xbox.tapB()
    if main.diagProgressFlag() == 56:  # Success
        main.clickToDiagProgress(77)
        main.waitFrames(12)
        xbox.tapDown() #Up for something else, down for done.
        xbox.tapB()
        main.waitFrames(30)
        # xbox.tapUp()
        # xbox.tapB()
        return True
    else:
        main.clickToDiagProgress(77)
        main.waitFrames(12)
        xbox.tapB()
        return False

def chocoTame4():
    print("START - CATCHER CHOCOBO")
    main.clickToDiagProgress(43)
    checkpoint = 0
    while not main.diagProgressFlag() in [44,67]:
        angle = main.getActorAngle(0)
        position = main.getActorCoords(0)
        print("User control")
        '''
        if position[1] > -1360 and checkpoint == 0: #Start off aiming right to manip balls
            checkpoint += 1
            FFXC.set_value('Dpad', 8) #Right
            memory.waitFrames(5)
            FFXC.set_value('Dpad', 0)
        if position[1] > -1200 and checkpoint == 1: #Slight left
            checkpoint += 1
            FFXC.set_value('Dpad', 4)#Left
            memory.waitFrames(10)
            FFXC.set_value('Dpad', 0)
        if position[1] > -770 and checkpoint == 3: #Left between balls
            checkpoint += 1
            FFXC.set_value('Dpad', 4)#Left
            memory.waitFrames(10)
            FFXC.set_value('Dpad', 0)
        if position[1] > -600 and checkpoint == 4: #Straighten out
            checkpoint += 1
            FFXC.set_value('Dpad', 8) #Right
            memory.waitFrames(6)
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

    while not main.diagProgressFlag() in [67,77]:
        #67 is 0:00.0 run
        xbox.tapB()
    if main.diagProgressFlag() == 67: #Success
        print("Great run! Perfect score!")
        main.clickToDiagProgress(77)
        main.waitFrames(12)
        xbox.tapDown()
        xbox.tapB()
        return True
    else:
        main.clickToDiagProgress(77)
        main.waitFrames(12)
        xbox.tapB()
        return False

def toRemiem():
    main.clickToControl()
    while main.userControl():
        targetPath.setMovement([-1565,434])
        xbox.tapB()
        print("Near chocobo lady")
    FFXC.set_neutral()
    main.clickToControl3()
    
    checkpoint = 0
    while checkpoint < 35:
        if main.userControl():
            if main.getMap() == 290 and checkpoint < 13:
                checkpoint = 13
            
            elif checkpoint == 10:
                print("Feather")
                main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 27:
                print("Orb thing")
                while main.userControl():
                    targetPath.setMovement([770,631])
                    xbox.tapB()
                main.clickToControl3()
                checkpoint += 1
            elif targetPath.setMovement(targetPath.toRemiem(checkpoint)) == True:
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
    while main.userControl():
        targetPath.setMovement([790,60])
        xbox.tapB()
    FFXC.set_neutral()
    main.clickToControl()
    checkpoint = 0
    while checkpoint != 37:
        if main.userControl():
            if targetPath.setMovement(targetPath.race1(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if main.battleActive():
                main.fleeAll()
            else:
                xbox.tapB()
    FFXC.set_movement(-1,1)
    main.waitFrames(10)
    FFXC.set_neutral()
    main.clickToControl3()

def chocoRace2():
    FFXC.set_neutral()
    main.clickToControl()
    while main.userControl():
        targetPath.setMovement([790,60])
        xbox.tapB()
    FFXC.set_neutral()
    checkpoint = 0
    while checkpoint != 38:
        if main.userControl():
            if checkpoint == 11:
                main.clickToEventTemple(0)
                checkpoint += 1
            if checkpoint == 17:
                main.clickToEventTemple(5)
                checkpoint += 1
            if checkpoint == 22:
                main.clickToEventTemple(0)
                checkpoint += 1
            if targetPath.setMovement(targetPath.race2(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if main.battleActive():
                main.fleeAll()
            else:
                xbox.tapB()
    FFXC.set_movement(-1,1)
    main.waitFrames(10)
    FFXC.set_neutral()
    main.clickToControl3()

def chocoRace3():
    FFXC.set_neutral()
    main.clickToControl()
    while main.userControl():
        targetPath.setMovement([790,60])
        xbox.tapB()
    FFXC.set_neutral()
    checkpoint = 0
    while checkpoint != 44:
        if main.userControl():
            if checkpoint == 11:
                main.clickToEventTemple(0)
                checkpoint += 1
            if checkpoint == 17:
                main.clickToEventTemple(5)
                checkpoint += 1
            if checkpoint == 22:
                main.clickToEventTemple(0)
                checkpoint += 1
            if checkpoint == 27:
                main.clickToEventTemple(0)
                checkpoint += 1
            if checkpoint == 39:
                main.clickToEventTemple(0)
                checkpoint += 1
            # if checkpoint == 42: #Since it's not tight enough movement yet
            #     FFXC.set_neutral()
            #     memory.waitFrames(120)
            #     memory.clickToControl3()
            #     break
            if targetPath.setMovement(targetPath.race3(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if main.battleActive():
                main.fleeAll()
            else:
                xbox.tapB()
    FFXC.set_movement(-1,1)
    main.waitFrames(60)
    FFXC.set_neutral()
    main.clickToControl3()

def templeToArena():
    main.clickToControl3()
    checkpoint = 0
    while main.getMap() != 307:
        if main.userControl():
            if main.getMap() == 223 and checkpoint < 18:
                checkpoint = 18
            
            elif checkpoint == 20:
                while main.userControl():
                    targetPath.setMovement([1261,-1238])
                    xbox.tapB()
                FFXC.set_neutral()
                main.clickToControl()
                checkpoint += 1
            
            elif checkpoint == 24:
                print("Feather")
                while main.userControl():
                    targetPath.setMovement([1101,-940])
                    xbox.tapB()
                FFXC.set_neutral()
                main.awaitControl()
                checkpoint += 1
            elif targetPath.setMovement(targetPath.leaveRemiem(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)

def arenaPurchase():
    main.clickToControl()
    
    print("Straight forward to the guy")
    FFXC.set_movement(0, 1)
    main.clickToEvent()
    FFXC.set_neutral()
    print("Now for dialog")
    main.clickToDiagProgress(65)
    print("Select Sure")
    main.waitFrames(15)
    xbox.tapDown()
    xbox.tapB()
    main.clickToDiagProgress(73)
    main.waitFrames(15)
    # xbox.tapUp()
    xbox.tapB()  # Let's see your weapons
    # memory.waitFrames(9000)
    menu.arenaPurchase1()
    # Sell all undesirable equipment
    # Purchase the following weapons:
    # -Tidus x4
    # -Yuna x1
        
    #---Done buying.
    main.awaitControl()
    main.waitFrames(2)
    FFXC.set_movement(0, -1)
    main.awaitEvent() #Exit the arena map
    FFXC.set_neutral()
    main.awaitControl()
    
    checkpoint = 0
    while main.getMap() != 279:
        if main.userControl():
            if checkpoint == 7 and gagazet.checkGems() < 2:
                checkpoint -= 2
            elif targetPath.setMovement(targetPath.calmLands2(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if main.battleActive():
                if gagazet.checkGems() < 2:
                    main.calmLandsGems()
                else:
                    main.calmLandsManip()
                main.fullPartyFormat('yuna')
            elif main.menuOpen() or main.diagSkipPossible():
                xbox.tapB()
    

def arenaPurchaseWithChocobo():
    while main.userControl(): #Back onto chocobo
        targetPath.setMovement([1347,-69])
        xbox.tapB()
    
    while not targetPath.setMovement([1488,778]):
        pass
    while not targetPath.setMovement([1545,1088]):
        pass
    while not main.getMap() == 279:
        targetPath.setMovement([1700,1200])
    
    main.fullPartyFormat('kimahri')