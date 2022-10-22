import math

import battle.main
import memory.main
import menu
import targetPathing
import vars
import xbox

gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def checkSpheres():
    # Speed sphere stuff. Improve this later.
    needSpeed = False
    if memory.main.getSpeed() < 5:
        needSpeed = True
        # Reprogram battle logic to throw some kind of grenades.

    # Same for Power spheres
    if gameVars.nemesis():
        if (
            memory.main.getPower() >= 28
            or (
                memory.main.getSpeed() < 9
                and memory.main.getPower()
                >= (23 + math.ceil((9 - memory.main.getSpeed()) / 2))
            )
            or (memory.main.getSpeed() >= 9 and memory.main.getPower() >= 23)
        ):
            needPower = False
        else:
            needPower = True

    elif (
        memory.main.getPower() >= 19
        or (
            memory.main.getSpeed() < 9
            and memory.main.getPower()
            >= (15 + math.ceil((9 - memory.main.getSpeed()) / 2))
        )
        or (memory.main.getSpeed() >= 9 and memory.main.getPower() >= 15)
    ):
        needPower = False
    else:
        needPower = True
    return needSpeed, needPower


def desert():
    memory.main.clickToControl()

    needSpeed, needPower = checkSpheres()
    # Logic for finding Teleport Spheres x2 (only chest in this area)
    teleSlot = memory.main.getItemSlot(98)
    if teleSlot == 255:
        teleCount = 0
    else:
        teleCount = memory.main.getItemCountSlot(teleSlot)

    chargeState = memory.main.overdriveState()[6] == 100
    # Bomb cores, sleeping powders, smoke bombs, silence grenades
    stealItems = [0, 0, 0, 0]
    itemsNeeded = 0

    # Now to figure out how many items we need.
    stealItems = battle.main.updateStealItemsDesert()
    itemsNeeded = 7 - sum(stealItems)

    menu.equip_sonic_steel()
    memory.main.closeMenu()

    checkpoint = 0
    firstFormat = False
    sandy1 = False
    while memory.main.getMap() != 130:
        if memory.main.userControl():
            # Map changes
            if checkpoint == 9:
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 11 and len(memory.main.getOrderSeven()) > 4:
                checkpoint += 1
            elif checkpoint < 39 and memory.main.getMap() == 137:
                checkpoint = 39
            elif checkpoint < 50 and memory.main.getMap() == 138:
                checkpoint = 50

            # Nemesis stuff
            elif checkpoint == 47 and gameVars.nemesis():
                checkpoint = 70
            elif checkpoint == 72:
                FFXC.set_neutral()
                memory.main.waitFrames(6)
                FFXC.set_movement(-1, 0)
                memory.main.waitFrames(4)
                FFXC.set_neutral()
                memory.main.waitFrames(6)
                if memory.main.userControl():
                    xbox.tapB()
                    memory.main.waitFrames(2)
                    memory.main.clickToControl()
                    checkpoint += 1
            elif checkpoint == 74:
                FFXC.set_neutral()
                memory.main.waitFrames(6)
                FFXC.set_movement(-1, 0)
                memory.main.waitFrames(4)
                FFXC.set_neutral()
                memory.main.waitFrames(6)
                if memory.main.userControl():
                    xbox.tapB()
                    memory.main.waitFrames(2)
                    memory.main.clickToControl()
                    checkpoint += 1
            elif checkpoint == 76:
                checkpoint = 48

            # Other events
            elif checkpoint == 2 or checkpoint == 24:  # Save sphere
                FFXC.set_neutral()
                memory.main.waitFrames(30 * 0.2)
                memory.main.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 53:
                print("Going for first Sandragora and chest")
                teleSlot = memory.main.getItemSlot(98)
                if teleSlot == 255 or teleCount == memory.main.getItemCountSlot(
                    teleSlot
                ):
                    targetPathing.set_movement([-44, 446])
                    xbox.tapB()
                else:
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
            elif checkpoint == 12 and not firstFormat:
                firstFormat = True
                memory.main.fullPartyFormat("desert9")

            # Sandragora skip logic
            elif checkpoint == 57:
                checkpoint += 1
            elif checkpoint == 60:
                if (
                    memory.main.getCoords()[1] < 812
                ):  # Dialing in. 810 works 95%, but was short once.
                    FFXC.set_movement(0, 1)
                else:
                    FFXC.set_neutral()
                    checkpoint += 1
            elif checkpoint == 61:
                if memory.main.getCoords()[1] < 810:
                    # Accidentally encountered Sandragora, must re-position.
                    checkpoint -= 2
                elif memory.main.getCoords()[1] < 840:
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
            elif memory.main.userControl():
                if targetPathing.set_movement(targetPathing.desert(checkpoint)):
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible() and not memory.main.battleActive():
                xbox.menuB()
            if memory.main.battleActive():  # Lots of battle logic here.
                xbox.clickToBattle()
                if (
                    checkpoint < 7 and memory.main.getEncounterID() == 197
                ):  # First battle in desert
                    battle.main.zu()
                elif memory.main.getEncounterID() == 234:  # Sandragora logic
                    print("Sandragora fight")
                    if checkpoint < 55:
                        if not sandy1:
                            battle.main.sandragora(1)
                            sandy1 = True
                        else:
                            battle.main.fleeAll()
                    else:
                        battle.main.sandragora(2)
                        checkpoint = 58
                else:
                    battle.main.bikanelBattleLogic(
                        [chargeState, needSpeed, needPower, itemsNeeded],
                        sandyFightComplete=sandy1,
                    )

                # After-battle logic
                memory.main.clickToControl()

                # First, check and update party format.
                if checkpoint > 10:
                    if checkpoint < 23 and checkpoint > 10:
                        memory.main.fullPartyFormat("desert9")
                    elif not chargeState:
                        memory.main.fullPartyFormat("desert1")
                    elif needPower:
                        memory.main.fullPartyFormat("desert1")
                    elif needSpeed:
                        memory.main.fullPartyFormat("desert1")
                    elif itemsNeeded >= 1:
                        memory.main.fullPartyFormat("desert1")
                    else:  # Catchall
                        memory.main.fullPartyFormat("desert1")

                # Next, figure out how many items we need.
                stealItems = battle.main.updateStealItemsDesert()
                print("-----------------------------")
                print("Items status:", stealItems)
                print("-----------------------------")
                itemsNeeded = 7 - sum(stealItems)

                # Finally, check for other factors and report to console.
                chargeState = memory.main.overdriveState()[6] == 100
                needSpeed, needPower = checkSpheres()
                print("-----------------------------Flag statuses")
                print("Rikku is charged up:", chargeState)
                print("Need more Speed spheres:", needSpeed)
                print("Need more Power spheres:", needPower)
                print("Number of additional items needed before Home:", itemsNeeded)
                print("-----------------------------Flag statuses (end)")
            elif memory.main.diagSkipPossible():
                xbox.tapB()


def findSummoners():
    print("Desert complete. Starting Home section")
    menu.home_grid()

    checkpoint = 0
    while memory.main.getMap() != 261:
        if memory.main.userControl():
            # events
            if checkpoint == 7:
                FFXC.set_neutral()
                memory.main.touchSaveSphere()

                checkpoint += 1
            elif checkpoint < 12 and memory.main.getMap() == 276:
                checkpoint = 12
            elif checkpoint < 18 and memory.main.getMap() == 280:
                checkpoint = 19
            elif checkpoint == 34 and gameVars.nemesis():
                checkpoint = 60
            elif checkpoint == 34 and gameVars.skipKilikaLuck():
                checkpoint = 60
            elif checkpoint == 63:
                memory.main.clickToEventTemple(6)
                checkpoint = 35
            # Bonus room, blitzLoss only
            elif checkpoint in [81, 82, 83] and memory.main.getMap() == 286:
                checkpoint = 84
            elif checkpoint == 86:
                FFXC.set_movement(0, 1)
                memory.main.clickToEvent()
                FFXC.set_neutral()
                memory.main.waitFrames(15)
                xbox.tapB()
                memory.main.waitFrames(15)
                xbox.tapLeft()
                xbox.tapLeft()
                xbox.tapB()
                memory.main.waitFrames(15)
                xbox.tapLeft()
                xbox.tapLeft()
                xbox.tapLeft()
                xbox.tapLeft()
                xbox.tapB()
                memory.main.waitFrames(15)
                xbox.tapRight()
                xbox.tapRight()
                xbox.tapRight()
                xbox.tapRight()
                xbox.tapB()
                memory.main.clickToControl()
                FFXC.set_movement(1, -1)
                memory.main.awaitEvent()
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
                memory.main.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 39:
                memory.main.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 42:
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 45:
                memory.main.clickToEventTemple(1)
                checkpoint += 1
            elif targetPathing.set_movement(targetPathing.home(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                if memory.main.getEncounterID() == 417:
                    print("Home, battle 1")
                    battle.main.home1()
                elif memory.main.getEncounterID() == 419:
                    if memory.main.getMap() == 280:
                        print("Home, battle 2")
                        battle.main.home2()
                        memory.main.fullPartyFormat("desert1")
                    else:
                        print("Home, bonus battle for Blitz loss")
                        battle.main.home3()
                elif memory.main.getEncounterID() == 420:
                    print("Home, final battle")
                    battle.main.home4()
                    memory.main.fullPartyFormat("evrae")
                else:
                    print("Flee from battle:", memory.main.getEncounterID())
                    battle.main.fleeAll()
            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()
    print("Let's go get that airship!")
    FFXC.set_neutral()
    if not gameVars.csr():
        memory.main.clickToDiagProgress(27)
        while not memory.main.cutsceneSkipPossible():
            xbox.tapB()
        xbox.skipScene()
        memory.main.clickToDiagProgress(105)
        memory.main.waitFrames(15)
        xbox.tapB()
        memory.main.waitFrames(15)
        xbox.skipScene()

    while not memory.main.userControl():
        if memory.main.diagSkipPossible():
            xbox.tapB()
        elif memory.main.cutsceneSkipPossible():
            xbox.skipScene()
    print("Airship is good to go. Now for Yuna.")
