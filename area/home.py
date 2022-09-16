import xbox
import battle
import menu
import memory
import targetPathing
import vars
import math
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def checkSpheres():
    # Speed sphere stuff. Improve this later.
    needSpeed = False
    if memory.getSpeed() < 5:
        needSpeed = True
        # Reprogram battle logic to throw some kind of grenades.

    # Same for Power spheres
    if gameVars.nemesis():
        if memory.getPower() >= 28 or (memory.getSpeed() < 9 and memory.getPower() >= (23 + math.ceil((9 - memory.getSpeed()) / 2))) or (memory.getSpeed() >= 9 and memory.getPower() >= 23):
            needPower = False
        else:
            needPower = True

    elif memory.getPower() >= 19 or (memory.getSpeed() < 9 and memory.getPower() >= (15 + math.ceil((9 - memory.getSpeed()) / 2))) or (memory.getSpeed() >= 9 and memory.getPower() >= 15):
        needPower = False
    else:
        needPower = True
    return needSpeed, needPower


def desert():
    memory.clickToControl()

    needSpeed, needPower = checkSpheres()
    # Logic for finding Teleport Spheres x2 (only chest in this area)
    teleSlot = memory.getItemSlot(98)
    if teleSlot == 255:
        teleCount = 0
    else:
        teleCount = memory.getItemCountSlot(teleSlot)

    chargeState = memory.overdriveState()[6] == 100
    # Bomb cores, sleeping powders, smoke bombs, silence grenades
    stealItems = [0, 0, 0, 0]
    itemsNeeded = 0

    # Now to figure out how many items we need.
    stealItems = battle.updateStealItemsDesert()
    itemsNeeded = 8 - (stealItems[1] + stealItems[2] + stealItems[3])

    menu.equipSonicSteel()
    memory.closeMenu()

    checkpoint = 0
    firstFormat = False
    sandy1 = False
    while memory.getMap() != 130:
        if memory.userControl():
            # Map changes
            if checkpoint == 9:
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 11 and len(memory.getOrderSeven()) > 4:
                checkpoint += 1
            elif checkpoint < 39 and memory.getMap() == 137:
                checkpoint = 39
            elif checkpoint < 50 and memory.getMap() == 138:
                checkpoint = 50

            # Nemesis stuff
            elif checkpoint == 47 and gameVars.nemesis():
                checkpoint = 70
            elif checkpoint == 72:
                FFXC.set_neutral()
                memory.waitFrames(6)
                FFXC.set_movement(-1, 0)
                memory.waitFrames(4)
                FFXC.set_neutral()
                memory.waitFrames(6)
                if memory.userControl():
                    xbox.tapB()
                    memory.waitFrames(2)
                    memory.clickToControl()
                    checkpoint += 1
            elif checkpoint == 74:
                FFXC.set_neutral()
                memory.waitFrames(6)
                FFXC.set_movement(-1, 0)
                memory.waitFrames(4)
                FFXC.set_neutral()
                memory.waitFrames(6)
                if memory.userControl():
                    xbox.tapB()
                    memory.waitFrames(2)
                    memory.clickToControl()
                    checkpoint += 1
            elif checkpoint == 76:
                checkpoint = 48

            # Other events
            elif checkpoint == 2 or checkpoint == 24:  # Save sphere
                FFXC.set_neutral()
                memory.waitFrames(30 * 0.2)
                memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 53:
                print("Going for first Sandragora and chest")
                teleSlot = memory.getItemSlot(98)
                if teleSlot == 255 or teleCount == memory.getItemCountSlot(teleSlot):
                    targetPathing.setMovement([-44, 446])
                    xbox.tapB()
                else:
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
            elif checkpoint == 12 and not firstFormat:
                firstFormat = True
                memory.fullPartyFormat('desert9')

            # Sandragora skip logic
            elif checkpoint == 57:
                checkpoint += 1
            elif checkpoint == 60:
                if memory.getCoords()[1] < 812:  # Dialing in. 810 works 95%, but was short once.
                    FFXC.set_movement(0, 1)
                else:
                    FFXC.set_neutral()
                    checkpoint += 1
            elif checkpoint == 61:
                if memory.getCoords()[1] < 810:
                    # Accidentally encountered Sandragora, must re-position.
                    checkpoint -= 2
                elif memory.getCoords()[1] < 840:
                    FFXC.set_neutral()
                else:
                    checkpoint += 1

            # After Sandy2 logic
            elif checkpoint == 64:
                if itemsNeeded >= 1:  # Cannot move on if we're short on throwable items
                    checkpoint -= 2
                elif needSpeed:  # Cannot move on if we're short on speed spheres
                    checkpoint -= 2
                else:
                    checkpoint += 1

            # General pathing
            elif memory.userControl():
                if targetPathing.setMovement(targetPathing.desert(checkpoint)):
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible() and not memory.battleActive():
                xbox.menuB()
            if memory.battleActive():  # Lots of battle logic here.
                xbox.clickToBattle()
                if checkpoint < 7 and memory.getEncounterID() == 197:  # First battle in desert
                    battle.zu()
                elif memory.getEncounterID() == 234:  # Sandragora logic
                    print("Sandragora fight")
                    if checkpoint < 55:
                        if not sandy1:
                            battle.sandragora(1)
                            sandy1 = True
                        else:
                            battle.fleeAll()
                    else:
                        battle.sandragora(2)
                        checkpoint = 58
                else:
                    battle.bikanelBattleLogic(
                        [chargeState, needSpeed, needPower, itemsNeeded])

                # After-battle logic
                memory.clickToControl()

                # First, check and update party format.
                if checkpoint > 10:
                    if checkpoint < 23 and checkpoint > 10:
                        memory.fullPartyFormat('desert9')
                    elif not chargeState:
                        memory.fullPartyFormat('desert1')
                    elif needPower:
                        memory.fullPartyFormat('desert1')
                    elif needSpeed:
                        memory.fullPartyFormat('desert1')
                    elif itemsNeeded >= 1:
                        memory.fullPartyFormat('desert1')
                    else:  # Catchall
                        memory.fullPartyFormat('desert1')

                # Next, figure out how many items we need.
                stealItems = battle.updateStealItemsDesert()
                print("-----------------------------")
                print("Items status:", stealItems)
                print("-----------------------------")
                itemsNeeded = 8 - sum(stealItems)

                # Finally, check for other factors and report to console.
                chargeState = memory.overdriveState()[6] == 100
                needSpeed, needPower = checkSpheres()
                print("-----------------------------Flag statuses")
                print("Rikku is charged up:", chargeState)
                print("Need more Speed spheres:", needSpeed)
                print("Need more Power spheres:", needPower)
                print("Number of additional items needed before Home:", itemsNeeded)
                print("-----------------------------Flag statuses (end)")
            elif memory.diagSkipPossible():
                xbox.tapB()


def findSummoners():
    print("Desert complete. Starting Home section")
    menu.homeGrid()

    checkpoint = 0
    while memory.getMap() != 261:
        if memory.userControl():
            # events
            if checkpoint == 7:
                FFXC.set_neutral()
                memory.touchSaveSphere()

                checkpoint += 1
            elif checkpoint < 12 and memory.getMap() == 276:
                checkpoint = 12
            elif checkpoint < 18 and memory.getMap() == 280:
                checkpoint = 19
            elif checkpoint == 34 and gameVars.nemesis():
                checkpoint = 60
            elif checkpoint == 34 and gameVars.skipKilikaLuck():
                checkpoint = 60
            elif checkpoint == 63:
                memory.clickToEventTemple(6)
                checkpoint = 35
            # Bonus room, blitzLoss only
            elif checkpoint in [81, 82, 83] and memory.getMap() == 286:
                checkpoint = 84
            elif checkpoint == 86:
                FFXC.set_movement(0, 1)
                memory.clickToEvent()
                FFXC.set_neutral()
                memory.waitFrames(15)
                xbox.tapB()
                memory.waitFrames(15)
                xbox.tapLeft()
                xbox.tapLeft()
                xbox.tapB()
                memory.waitFrames(15)
                xbox.tapLeft()
                xbox.tapLeft()
                xbox.tapLeft()
                xbox.tapLeft()
                xbox.tapB()
                memory.waitFrames(15)
                xbox.tapRight()
                xbox.tapRight()
                xbox.tapRight()
                xbox.tapRight()
                xbox.tapB()
                memory.clickToControl()
                FFXC.set_movement(1, -1)
                memory.awaitEvent()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 88:
                checkpoint = 21
            elif checkpoint == 20:
                if gameVars.getBlitzWin():
                    checkpoint = 21
                else:
                    checkpoint = 81
            elif checkpoint == 31 and not gameVars.csr():
                memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 39:
                memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 42:
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 45:
                memory.clickToEventTemple(1)
                checkpoint += 1
            elif targetPathing.setMovement(targetPathing.Home(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.battleActive():
                if memory.getEncounterID() == 417:
                    print("Home, battle 1")
                    battle.home1()
                elif memory.getEncounterID() == 419:
                    if memory.getMap() == 280:
                        print("Home, battle 2")
                        battle.home2()
                        memory.fullPartyFormat('desert1')
                    else:
                        print("Home, bonus battle for Blitz loss")
                        battle.home3()
                elif memory.getEncounterID() == 420:
                    print("Home, final battle")
                    battle.home4()
                    memory.fullPartyFormat('evrae')
                else:
                    print("Flee from battle:", memory.getEncounterID())
                    battle.fleeAll()
            elif memory.menuOpen() or memory.diagSkipPossible():
                xbox.tapB()
    print("Let's go get that airship!")
    FFXC.set_neutral()
    if not gameVars.csr():
        memory.clickToDiagProgress(27)
        while not memory.cutsceneSkipPossible():
            xbox.tapB()
        xbox.skipScene()
        memory.clickToDiagProgress(105)
        memory.waitFrames(15)
        xbox.tapB()
        memory.waitFrames(15)
        xbox.skipScene()

    while not memory.userControl():
        if memory.diagSkipPossible():
            xbox.tapB()
        elif memory.cutsceneSkipPossible():
            xbox.skipScene()
    print("Airship is good to go. Now for Yuna.")
