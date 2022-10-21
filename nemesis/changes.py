import area.gagazet
import battle.main
import memory.main
import nemesis.targetPath
import vars
import xbox

gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


# The following functions replace the default ones from the regular Bahamut run.


def arenaNPC():
    memory.main.awaitControl()
    if memory.main.getMap() != 307:
        return
    while not (memory.main.diagProgressFlag() == 74 and memory.main.diagSkipPossible()):
        if memory.main.userControl():
            if memory.main.getCoords()[1] > -12:
                FFXC.set_movement(0, -1)
                memory.main.waitFrames(1)
            else:
                nemesis.targetPath.setMovement([2, -15])
                xbox.tapB()
        else:
            FFXC.set_neutral()
            if memory.main.diagProgressFlag() == 59:
                xbox.menuA()
                xbox.menuA()
                xbox.menuA()
                xbox.menuA()
                xbox.tapB()
            elif memory.main.diagSkipPossible():
                xbox.tapB()
    memory.main.waitFrames(3)


def nextRace():
    FFXC.set_neutral()
    memory.main.clickToDiagProgress(28)
    memory.main.waitFrames(9)
    xbox.tapB()


def calmLands():
    # Start chocobo races
    # memory.setGameSpeed(2)
    calmLands_1()

    FFXC.set_neutral()
    memory.main.clickToDiagProgress(28)
    memory.main.waitFrames(9)
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
    # Enter the cutscene that starts Calm Lands
    memory.main.fullPartyFormat("yuna", fullMenuClose=True)
    while not (memory.main.getCoords()[1] >= -1650 and memory.main.userControl()):
        if memory.main.userControl():
            FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()

    # Now head to the chocobo lady.
    # memory.setEncounterRate(0) #Testing only
    checkpoint = 0
    while memory.main.getMap() != 307:
        if memory.main.userControl():
            # if checkpoint == 10:
            #     if area.gagazet.checkGems() < 2:
            #         checkpoint -= 2
            if (
                nemesis.targetPath.setMovement(
                    nemesis.targetPath.calmLands1(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                if area.gagazet.checkGems() < 2:
                    battle.main.calmLandsGems()
                else:
                    battle.main.calmLandsManip()
                memory.main.fullPartyFormat("yuna")
            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()

    print("Now talk to NPC")
    # arenaNPC()
    # arenaPurchase()
    # memory.waitFrames(6)
    # xbox.tapB() #I want to ride a chocobo.


def chocoTame1():
    memory.main.clickToDiagProgress(43)
    while not memory.main.diagProgressFlag() in [44, 74]:
        angle = memory.main.getActorAngle(0)
        # print("Angle: ", retVal)
        position = memory.main.getActorCoords(0)
        # print("Position: ", position)
        if position[0] < -110:  # Need to move right
            if angle > 1.4:
                FFXC.set_value("Dpad", 8)
            elif angle < 1.2:
                FFXC.set_value("Dpad", 4)
            else:
                FFXC.set_value("Dpad", 0)
        elif position[0] > -60:  # Need to move left
            if angle > 1.8:
                FFXC.set_value("Dpad", 8)
            elif angle < 1.6:
                FFXC.set_value("Dpad", 4)
            else:
                FFXC.set_value("Dpad", 0)
        else:
            if angle > 1.6:  # Stay straight
                FFXC.set_value("Dpad", 8)
            elif angle < 1.4:
                FFXC.set_value("Dpad", 4)
            else:
                FFXC.set_value("Dpad", 0)
    FFXC.set_neutral()

    while not memory.main.diagProgressFlag() in [51, 69, 74]:
        # 51 is success
        xbox.tapB()
    if memory.main.diagProgressFlag() == 51:  # Success
        memory.main.clickToDiagProgress(77)
        memory.main.waitFrames(12)
        xbox.tapDown()  # Up for next race, down for quit
        xbox.tapB()
        # memory.waitFrames(20)
        xbox.tapUp()
        xbox.tapB()
        return True
    else:
        memory.main.clickToDiagProgress(76)
        memory.main.waitFrames(12)
        xbox.tapB()
        return False


def chocoTame2():
    memory.main.clickToDiagProgress(43)
    checkpoint = 0
    while not memory.main.diagProgressFlag() in [44, 74]:
        angle = memory.main.getActorAngle(0)
        position = memory.main.getActorCoords(0)

        if (
            position[1] > -1360 and checkpoint == 0
        ):  # Start off aiming right to manip balls
            checkpoint += 1
            FFXC.set_value("Dpad", 8)  # Right
            memory.main.waitFrames(5)
            FFXC.set_value("Dpad", 0)
        if position[1] > -1200 and checkpoint == 1:  # Slight left
            checkpoint += 1
            FFXC.set_value("Dpad", 4)  # Left
            memory.main.waitFrames(11)
            FFXC.set_value("Dpad", 0)
        if position[1] > -1000 and checkpoint == 2:  # Straighten out
            checkpoint += 1
            FFXC.set_value("Dpad", 8)  # Right
            memory.main.waitFrames(7)
            FFXC.set_value("Dpad", 0)
        if position[1] > -800 and checkpoint == 3:  # Juke right
            checkpoint += 1
            FFXC.set_value("Dpad", 8)  # Right
            memory.main.waitFrames(5)
            FFXC.set_value("Dpad", 0)
        if position[1] > -650 and checkpoint == 4:  # Back to the left
            checkpoint += 1
            FFXC.set_value("Dpad", 4)  # Left
            memory.main.waitFrames(11)
            FFXC.set_value("Dpad", 0)
        if position[1] > -550 and checkpoint == 5:  # Straighten out
            checkpoint += 1
            FFXC.set_value("Dpad", 8)  # Right
            memory.main.waitFrames(6)
            FFXC.set_value("Dpad", 0)
        if position[1] > -450 and checkpoint == 6:  # Juke right again
            checkpoint += 1
            FFXC.set_value("Dpad", 8)
            memory.main.waitFrames(6)
            FFXC.set_value("Dpad", 0)
        if position[1] > -250 and checkpoint == 7:  # Straighten out
            checkpoint += 1
            FFXC.set_value("Dpad", 4)
            memory.main.waitFrames(14)
            FFXC.set_value("Dpad", 0)
        if position[1] > -90 and checkpoint == 8:  # The final juke!
            checkpoint += 1
            FFXC.set_value("Dpad", 8)
            memory.main.waitFrames(13)
            FFXC.set_value("Dpad", 0)
    FFXC.set_neutral()

    while not memory.main.diagProgressFlag() in [54, 69, 77]:
        # 54 is success
        xbox.tapB()
    if memory.main.diagProgressFlag() == 54:  # Success
        memory.main.clickToDiagProgress(77)
        memory.main.waitFrames(12)
        xbox.tapUp()
        xbox.tapB()
        memory.main.waitFrames(30)
        xbox.tapUp()
        xbox.tapB()
        return True
    else:
        memory.main.clickToDiagProgress(77)
        memory.main.waitFrames(12)
        xbox.tapB()
        return False


def chocoTame3():
    memory.main.clickToDiagProgress(43)
    checkpoint = 0
    while not memory.main.diagProgressFlag() in [44, 74]:
        position = memory.main.getActorCoords(0)
        if position[1] > -1370 and checkpoint == 0:
            checkpoint += 1
            FFXC.set_value("Dpad", 4)  # Left
            memory.main.waitFrames(3)
            FFXC.set_value("Dpad", 0)
        if position[1] > -1200 and checkpoint == 1:
            checkpoint += 1
            FFXC.set_value("Dpad", 8)  # Right
            memory.main.waitFrames(10)
            FFXC.set_value("Dpad", 0)
        if position[1] > -1100 and checkpoint == 2:
            checkpoint += 1
            FFXC.set_value("Dpad", 4)
            memory.main.waitFrames(12)
            FFXC.set_value("Dpad", 0)
        if position[1] > -1040 and checkpoint == 3:
            checkpoint += 1
            FFXC.set_value("Dpad", 8)
            memory.main.waitFrames(9)
            FFXC.set_value("Dpad", 0)
        if position[1] > -950 and checkpoint == 4:
            checkpoint += 1
            FFXC.set_value("Dpad", 4)
            memory.main.waitFrames(12)
            FFXC.set_value("Dpad", 0)
        if position[1] > -700 and checkpoint == 5:
            checkpoint += 1
            FFXC.set_value("Dpad", 8)
            memory.main.waitFrames(12)
            FFXC.set_value("Dpad", 0)
        if position[1] > -600 and checkpoint == 6:
            checkpoint += 1
            FFXC.set_value("Dpad", 4)
            memory.main.waitFrames(12)
            FFXC.set_value("Dpad", 0)
        if position[1] > -500 and checkpoint == 7:
            checkpoint += 1
            FFXC.set_value("Dpad", 4)
            memory.main.waitFrames(6)
            FFXC.set_value("Dpad", 0)
        if position[1] > -400 and checkpoint == 8:
            checkpoint += 1
            FFXC.set_value("Dpad", 8)
            memory.main.waitFrames(16)
            FFXC.set_value("Dpad", 0)
        if position[1] > -250 and checkpoint == 9:
            checkpoint += 1
            FFXC.set_value("Dpad", 4)
            memory.main.waitFrames(16)
            FFXC.set_value("Dpad", 0)
        # Still dialing in on this one.
        if position[1] > -120 and checkpoint == 10:
            checkpoint += 1
            FFXC.set_value("Dpad", 8)
            memory.main.waitFrames(16)
            FFXC.set_value("Dpad", 0)
        if position[1] > -20 and checkpoint == 11:
            checkpoint += 1
            FFXC.set_value("Dpad", 4)
            memory.main.waitFrames(10)
            FFXC.set_value("Dpad", 0)
    FFXC.set_neutral()

    while not memory.main.diagProgressFlag() in [56, 69, 77]:
        # 56 is success
        xbox.tapB()
    if memory.main.diagProgressFlag() == 56:  # Success
        memory.main.clickToDiagProgress(77)
        memory.main.waitFrames(12)
        xbox.tapDown()  # Up for something else, down for done.
        xbox.tapB()
        memory.main.waitFrames(30)
        # xbox.tapUp()
        # xbox.tapB()
        return True
    else:
        memory.main.clickToDiagProgress(77)
        memory.main.waitFrames(12)
        xbox.tapB()
        return False


def chocoTame4():
    print("START - CATCHER CHOCOBO")
    memory.main.clickToDiagProgress(43)
    checkpoint = 0
    while not memory.main.diagProgressFlag() in [44, 67]:
        angle = memory.main.getActorAngle(0)
        position = memory.main.getActorCoords(0)
        print("User control")
        """
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
    """
    print("Race complete.")
    FFXC.set_neutral()

    while not memory.main.diagProgressFlag() in [67, 77]:
        # 67 is 0:00.0 run
        xbox.tapB()
    if memory.main.diagProgressFlag() == 67:  # Success
        print("Great run! Perfect score!")
        memory.main.clickToDiagProgress(77)
        memory.main.waitFrames(12)
        xbox.tapDown()
        xbox.tapB()
        return True
    else:
        memory.main.clickToDiagProgress(77)
        memory.main.waitFrames(12)
        xbox.tapB()
        return False


def toRemiem():
    memory.main.clickToControl()
    while memory.main.userControl():
        nemesis.targetPath.setMovement([-1565, 434])
        xbox.tapB()
        print("Near chocobo lady")
    FFXC.set_neutral()
    memory.main.clickToControl3()

    checkpoint = 0
    while checkpoint < 35:
        if memory.main.userControl():
            if memory.main.getMap() == 290 and checkpoint < 13:
                checkpoint = 13

            elif checkpoint == 10:
                print("Feather")
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 27:
                print("Orb thing")
                while memory.main.userControl():
                    nemesis.targetPath.setMovement([770, 631])
                    xbox.tapB()
                memory.main.clickToControl3()
                checkpoint += 1
            elif (
                nemesis.targetPath.setMovement(nemesis.targetPath.toRemiem(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)


def remiemRaces():
    print("Ready to start races")
    chocoRace1()
    print("Celestial Weapon obtained.")
    # chocoRace2()
    # print("Obtained")
    # chocoRace3()
    # print("Something obtained")
    print("Now heading back to the monster arena.")


def chocoRace1():
    while memory.main.userControl():
        nemesis.targetPath.setMovement([790, 60])
        xbox.tapB()
    FFXC.set_neutral()
    memory.main.clickToControl()
    checkpoint = 0
    while checkpoint != 37:
        if memory.main.userControl():
            if (
                nemesis.targetPath.setMovement(nemesis.targetPath.race1(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                battle.main.fleeAll()
            else:
                xbox.tapB()
    FFXC.set_movement(-1, 1)
    memory.main.waitFrames(10)
    FFXC.set_neutral()
    memory.main.clickToControl3()


def chocoRace2():
    FFXC.set_neutral()
    memory.main.clickToControl()
    while memory.main.userControl():
        nemesis.targetPath.setMovement([790, 60])
        xbox.tapB()
    FFXC.set_neutral()
    checkpoint = 0
    while checkpoint != 38:
        if memory.main.userControl():
            if checkpoint == 11:
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            if checkpoint == 17:
                memory.main.clickToEventTemple(5)
                checkpoint += 1
            if checkpoint == 22:
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            if (
                nemesis.targetPath.setMovement(nemesis.targetPath.race2(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                battle.main.fleeAll()
            else:
                xbox.tapB()
    FFXC.set_movement(-1, 1)
    memory.main.waitFrames(10)
    FFXC.set_neutral()
    memory.main.clickToControl3()


def chocoRace3():
    FFXC.set_neutral()
    memory.main.clickToControl()
    while memory.main.userControl():
        nemesis.targetPath.setMovement([790, 60])
        xbox.tapB()
    FFXC.set_neutral()
    checkpoint = 0
    while checkpoint != 44:
        if memory.main.userControl():
            if checkpoint == 11:
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            if checkpoint == 17:
                memory.main.clickToEventTemple(5)
                checkpoint += 1
            if checkpoint == 22:
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            if checkpoint == 27:
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            if checkpoint == 39:
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            # if checkpoint == 42: #Since it's not tight enough movement yet
            #     FFXC.set_neutral()
            #     memory.waitFrames(120)
            #     memory.clickToControl3()
            #     break
            if (
                nemesis.targetPath.setMovement(nemesis.targetPath.race3(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                battle.main.fleeAll()
            else:
                xbox.tapB()
    FFXC.set_movement(-1, 1)
    memory.main.waitFrames(60)
    FFXC.set_neutral()
    memory.main.clickToControl3()


def templeToArena():
    memory.main.clickToControl3()
    checkpoint = 0
    while memory.main.getMap() != 307:
        if memory.main.userControl():
            if memory.main.getMap() == 223 and checkpoint < 18:
                checkpoint = 18

            elif checkpoint == 20:
                while memory.main.userControl():
                    nemesis.targetPath.setMovement([1261, -1238])
                    xbox.tapB()
                FFXC.set_neutral()
                memory.main.clickToControl()
                checkpoint += 1

            elif checkpoint == 24:
                print("Feather")
                while memory.main.userControl():
                    nemesis.targetPath.setMovement([1101, -940])
                    xbox.tapB()
                FFXC.set_neutral()
                memory.main.awaitControl()
                checkpoint += 1
            elif (
                nemesis.targetPath.setMovement(
                    nemesis.targetPath.leaveRemiem(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)


def arenaPurchase():
    memory.main.clickToControl()

    print("Straight forward to the guy")
    FFXC.set_movement(0, 1)
    memory.main.clickToEvent()
    FFXC.set_neutral()
    print("Now for dialog")
    memory.main.clickToDiagProgress(65)
    print("Select Sure")
    memory.main.waitFrames(15)
    xbox.tapDown()
    xbox.tapB()
    memory.main.clickToDiagProgress(73)
    memory.main.waitFrames(15)
    # xbox.tapUp()
    xbox.tapB()  # Let's see your weapons
    # memory.waitFrames(9000)
    nemesis.menu.arenaPurchase1()
    # Sell all undesirable equipment
    # Purchase the following weapons:
    # -Tidus x4
    # -Yuna x1

    # ---Done buying.
    memory.main.awaitControl()
    memory.main.waitFrames(2)
    FFXC.set_movement(0, -1)
    memory.main.awaitEvent()  # Exit the arena map
    FFXC.set_neutral()
    memory.main.awaitControl()

    checkpoint = 0
    while memory.main.getMap() != 279:
        if memory.main.userControl():
            if checkpoint == 7 and area.gagazet.checkGems() < 2:
                checkpoint -= 2
            elif (
                nemesis.targetPath.setMovement(
                    nemesis.targetPath.calmLands2(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                if area.gagazet.checkGems() < 2:
                    battle.main.calmLandsGems()
                else:
                    battle.main.calmLandsManip()
                memory.main.fullPartyFormat("yuna")
            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()


def arenaPurchaseWithChocobo():
    while memory.main.userControl():  # Back onto chocobo
        nemesis.targetPath.setMovement([1347, -69])
        xbox.tapB()

    while not nemesis.targetPath.setMovement([1488, 778]):
        pass
    while not nemesis.targetPath.setMovement([1545, 1088]):
        pass
    while not memory.main.getMap() == 279:
        nemesis.targetPath.setMovement([1700, 1200])

    memory.main.fullPartyFormat("kimahri")
