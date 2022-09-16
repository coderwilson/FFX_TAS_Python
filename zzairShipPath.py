import xbox
import memory
import battle
import targetPathing
import math
import vars
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def airShipPath(version):
    memory.clickToControl()
    distillerPurchase = False

    complete = False
    checkpoint = 0
    while not complete:
        if memory.userControl():
            # Map changes
            if checkpoint == 2:
                memory.clickToEventTemple(3)
                checkpoint += 1
            elif version == 1 and not distillerPurchase and checkpoint == 5 and \
                    (memory.getSpeed() < 9 or memory.getPower() < 23):

                # Tyton to update this with the actual purchase.
                while memory.diagProgressFlag() != 44:
                    if memory.userControl():
                        targetPathing.setMovement([-6, 6])
                        xbox.tapB()
                    else:
                        FFXC.set_neutral()
                        if memory.battleActive():
                            battle.fleeAll()
                        elif memory.menuOpen():
                            xbox.tapB()
                FFXC.set_neutral()
                memory.clickToDiagProgress(48)
                while memory.airshipShopDialogueRow() != 1:
                    xbox.tapDown()
                while not memory.itemShopMenu() == 7:
                    xbox.tapB()  # Click through until items menu comes up
                while not memory.itemShopMenu() == 10:
                    xbox.tapB()  # Select buy command
                if memory.getPower() < 23:
                    while memory.equipBuyRow() != 7:
                        if memory.equipBuyRow() < 7:
                            xbox.tapDown()
                        else:
                            xbox.tapUp()
                    while not memory.itemShopMenu() == 16:
                        xbox.tapB()
                    while memory.purchasingAmountItems() != min(math.ceil((23 - memory.getPower()) / 2), 3):
                        if memory.purchasingAmountItems() < min(math.ceil((23 - memory.getPower()) / 2), 3):
                            xbox.tapRight()
                        else:
                            xbox.tapLeft()
                    while not memory.itemShopMenu() == 10:
                        xbox.tapB()
                if memory.getSpeed() < 9:
                    while memory.equipBuyRow() != 9:
                        if memory.equipBuyRow() < 9:
                            xbox.tapDown()
                        else:
                            xbox.tapUp()
                    while not memory.itemShopMenu() == 16:
                        xbox.tapB()
                    while memory.purchasingAmountItems() != min(math.ceil((9 - memory.getSpeed()) / 2), 2):
                        if memory.purchasingAmountItems() < min(math.ceil((9 - memory.getSpeed()) / 2), 2):
                            xbox.tapRight()
                        else:
                            xbox.tapLeft()
                    while not memory.itemShopMenu() == 10:
                        xbox.tapB()
                memory.closeMenu()
                memory.clickToControl3()
                distillerPurchase = True
            elif checkpoint < 6 and memory.getMap() == 351:  # Screen with Isaaru
                checkpoint = 6
            elif checkpoint < 9 and memory.getMap() == 211:  # Gallery screen (includes lift screens)
                checkpoint = 9
                # Optional save sphere can be touched here.
                # Should not be necessary, we should be touching save sphere in Home
            elif checkpoint == 14 and version == 2:
                print("Talking to Yuna/Kimahri in the gallery")
                checkpoint = 23
                print("Checkpoint update:", checkpoint)
            elif checkpoint == 16:
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 18:
                FFXC.set_neutral()
                xbox.SkipDialog(1)
                memory.awaitControl()
                checkpoint += 1
            elif checkpoint == 24:
                memory.clickToEventTemple(7)
                checkpoint += 1

            # Return trip map changes
            elif checkpoint in [32, 34]:  # Formerly included 13
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 37:
                memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 40:
                memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint in [43, 44] and not gameVars.csr():
                checkpoint = 45
            elif checkpoint == 44:  # Talk to Cid
                while memory.userControl():
                    targetPathing.setMovement([-250, 339])
                    xbox.tapB()
                FFXC.set_neutral()
                complete = True
            elif checkpoint == 46:  # Talk to Cid
                while memory.userControl():
                    targetPathing.setMovement([-230, 366])
                    xbox.tapB()
                FFXC.set_neutral()
                complete = True

            # Complete states
            elif checkpoint == 19 and version == 1:
                print("Pre-Evrae pathing")
                FFXC.set_movement(0, 1)
                memory.waitFrames(30 * 3)
                FFXC.set_neutral()
                complete = True
            elif checkpoint == 19 and version == 3:
                print("Sin's Arms")
                FFXC.set_movement(0, 1)
                memory.waitFrames(30 * 3)
                FFXC.set_neutral()
                while not memory.battleActive():
                    if memory.diagSkipPossible():
                        xbox.tapB()
                    elif memory.cutsceneSkipPossible():
                        xbox.skipScene()
                complete = True
            elif checkpoint == 19 and version == 4:
                print("Straight to the deck, talking to Yuna.")
                FFXC.set_movement(0, 1)
                memory.waitFrames(30 * 3)
                FFXC.set_neutral()
                memory.awaitControl()
                targetPathing.setMovement([-2, -15])
                memory.waitFrames(30 * 0.5)
                while memory.userControl():
                    targetPathing.setMovement([-2, -15])
                    xbox.tapB()
                FFXC.set_neutral()
                while not memory.userControl():
                    if memory.diagSkipPossible():
                        xbox.tapB()
                    elif memory.cutsceneSkipPossible():
                        xbox.skipScene()
                complete = True
            elif checkpoint == 19 and version == 5:
                print("Again to the deck, three skips.")
                FFXC.set_movement(0, 1)
                memory.waitFrames(30 * 3)
                FFXC.set_neutral()
                while not memory.battleActive():
                    if memory.diagSkipPossible():
                        xbox.tapB()
                    elif memory.cutsceneSkipPossible():
                        xbox.skipScene()
                complete = True
            elif checkpoint == 19 and version == 6:
                print("Sin's Face")
                FFXC.set_movement(0, 1)
                memory.waitFrames(30 * 3)
                FFXC.set_neutral()
                complete = True

            # General Pathing
            elif targetPathing.setMovement(targetPathing.airShip(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.battleActive():
                battle.fleeAll()
            elif memory.menuOpen() or memory.diagSkipPossible():
                print("Mark")
                xbox.tapB()

    print("End of section, Airship pathing")


def airShipReturn():
    print("Conversation with Yuna/Kimahri.")
    memory.clickToControl()

    pos = memory.getCoords()
    print("Ready to run back to the cockpit.")
    while pos[1] > -90:  # Leaving Yuna/Kimahri, heading back down.
        FFXC.set_value('AxisLy', -1)
        FFXC.set_value('AxisLx', 0)
        pos = memory.getCoords()
    print("Turn East")
    while pos[0] < -1:
        FFXC.set_value('AxisLx', 1)
        FFXC.set_value('AxisLy', 0)
        pos = memory.getCoords()
    print("Turn North")
    while memory.userControl():
        FFXC.set_value('AxisLx', 0)
        FFXC.set_value('AxisLy', 1)
        pos = memory.getCoords()

    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    memory.awaitControl()

    while memory.userControl():
        FFXC.set_value('AxisLx', 0)
        FFXC.set_value('AxisLy', 1)

    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    memory.awaitControl()

    while memory.userControl():
        pos = memory.getCoords()
        memory.waitFrames(30 * 0.05)
        FFXC.set_value('AxisLy', 1)
        if pos[0] < -1:
            FFXC.set_value('AxisLx', 1)
        else:
            FFXC.set_value('AxisLx', 0)

    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    memory.awaitControl()
    FFXC.set_value('AxisLy', 1)
    memory.waitFrames(30 * 1.2)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', -1)
    memory.waitFrames(30 * 0.5)

    while memory.userControl():
        FFXC.set_value('AxisLy', 1)
        FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
