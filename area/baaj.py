import xbox
import screen
import battle
import memory
import targetPathing
import menu
import vars

FFXC = xbox.controllerHandle()
gameVars = vars.varsHandle()


def Entrance():
    memory.awaitControl()
    print("Starting Baaj exterior area")
    FFXC.set_neutral()
    menu.shortAeons()

    # Now back into the water
    checkpoint = 0
    while not memory.battleActive():
        if memory.userControl():
            if checkpoint == 6:
                memory.clickToEventTemple(0)
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.baajRamp(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()

    FFXC.set_neutral()

    # Battles
    while memory.getStoryProgress() < 48:
        if screen.BattleScreen():
            if memory.getEncounterID() == 2:
                battle.attack('none')
            else:
                battle.defend()
        elif memory.diagSkipPossible():
            xbox.menuB()

    # Out of the frying pan, into the furnace
    memory.clickToControl()
    print("Hallway before main puzzle.")
    checkpoint = 0
    while memory.getMap() != 63:
        if memory.userControl():
            if checkpoint == 9:
                FFXC.set_movement(-1, 1)
                memory.awaitEvent()
                FFXC.set_neutral()
            # General pathing
            elif targetPathing.setMovement(targetPathing.baajHallway(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()


def Baaj_puzzle():
    memory.clickToControl()
    print("Ready for the main puzzle.")
    checkpoint = 0
    while not memory.battleActive():
        if memory.userControl():
            # Events
            if checkpoint == 3:
                memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 5:  # Flint room
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 6:  # Obtain Flint
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 7:  # Exit Flint room
                memory.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 12:  # Bouquet hallway
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 21:  # Withered bouquet
                memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 32:  # Back to main room
                memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 33:  # To the fireplace
                targetPathing.setMovement([1, 1])
                xbox.menuB()

            # General pathing
            elif targetPathing.setMovement(targetPathing.baajPuzzle(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()


def Klikk_fight():
    # Before Rikku shows up, we're just going to spam the B button. Simple.
    FFXC.set_neutral()
    while not screen.turnRikku():
        xbox.tapB()

    xbox.clickToBattle()
    battle.useItem(0, 'none')  # Tidus self-potion
    screen.awaitTurn()
    battle.Klikk()


def distance(n1, n2):
    try:
        player1 = memory.getActorCoords(actorNumber=n1)
        player2 = memory.getActorCoords(actorNumber=n2)
        return (abs(player1[1] - player2[1]) + abs(player1[0] - player2[0]))
    except Exception as x:
        print("Exception:", x)
        return 999


def ABboat1():
    print("Start of Al Bhed boat section.")
    # memory.awaitControl()
    # if gameVars.csr():
    #     memory.waitFrames(45)
    # memory.clearSaveMenuCursor2()
    # FFXC.set_neutral()
    print("Control restored.")
    print("On the boat!")
    while memory.getActorCoords(actorNumber=0)[0] > -50:
        rikkuNum = memory.actorIndex(actorNum=41)
        target = memory.getActorCoords(actorNumber=rikkuNum)
        targetPathing.setMovement(target)
        if distance(0, rikkuNum) < 10:
            xbox.tapB()
        elif memory.menuOpen():
            xbox.menuA()
            xbox.menuB()
    print("In the water!")
    FFXC.set_value('BtnA', 1)
    FFXC.set_movement(-1, -1)
    memory.waitFrames(20)

    while memory.getMap() != 288:
        FFXC.set_value('BtnA', 1)
        FFXC.set_movement(0, -1)
        if memory.battleActive():
            FFXC.set_neutral()
            print("Battle Start (Al Bhed swimming section)")
            battle.stealAndAttack()
            print("Battle End (Al Bhed swimming section)")
        elif memory.menuOpen() or memory.diagSkipPossible():
            print("Battle Complete screen")
            xbox.tapB()


def ABswimming1():
    print("Swimming down from the boat")
    while memory.getMap() != 288:
        if memory.userControl():
            targetPathing.setMovement([-300, -300])
            FFXC.set_value('BtnA', 1)
        else:
            FFXC.set_neutral()
            if screen.BattleScreen():
                print("Battle Start (Al Bhed swimming section)")
                battle.stealAndAttack()
                print("Battle End (Al Bhed swimming section)")
            elif memory.menuOpen():
                print("Battle Complete screen")
                xbox.menuB()

    FFXC.set_neutral()
    print("Swimming towards airship")
    while memory.getMap() != 64:
        pos = memory.getCoords()
        if memory.userControl():
            if memory.getMap() == 71:
                FFXC.set_movement(0, -1)
                FFXC.set_value('BtnA', 1)
            else:
                FFXC.set_value('BtnA', 0)
                if pos[1] > -230:
                    targetPathing.setMovement([-343, -284])
                elif pos[1] > -410:
                    targetPathing.setMovement([-421, -463])
                else:
                    FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()
            if screen.BattleScreen():
                print("Battle Start (Al Bhed swimming section)")
                battle.stealAndAttack()
                print("Battle End (Al Bhed swimming section)")
            elif memory.menuOpen():
                print("Battle Complete screen")
                xbox.menuB()


def ABswimming2():
    # Quick heal-up to make sure we're full HP on Rikku
    memory.awaitControl()
    FFXC.set_movement(1, -1)
    FFXC.set_value('BtnA', 1)
    memory.touchSaveSphere()

    memory.clearSaveMenuCursor2()
    # Now to get to it
    FFXC.set_movement(0, 1)
    memory.waitFrames(30 * 1)
    memory.clickToEvent()
    memory.waitFrames(30 * 0.2)
    memory.awaitControl()

    pos = memory.getCoords()
    while memory.userControl():
        if pos[1] < 135:
            FFXC.set_movement(1, 1)
        else:
            FFXC.set_movement(0, 1)

        pos = memory.getCoords()
    FFXC.set_neutral()

    screen.awaitTurn()
    # Final group of Piranhas
    battle.stealAndAttackPreTros()
    memory.awaitControl()
    FFXC.set_movement(0, 1)
    print("Technical Support Tidus")
    xbox.SkipDialog(2)
    FFXC.set_movement(0, 0)
    memory.clickToControl()
    while not memory.battleActive():
        FFXC.set_movement(0, -1)
    print("Engaging Tros")
    FFXC.set_neutral()

    # Tros fight
    xbox.clickToBattle()
    battle.Tros()

    FFXC.set_neutral()
    while memory.getStoryProgress() < 111:
        if memory.userControl():
            if memory.diagProgressFlag() == 109 and not memory.userControl():
                FFXC.set_neutral()
                if memory.saveMenuCursor2() == 0:
                    xbox.tapA()
                else:
                    xbox.tapB()
                memory.waitFrames(4)
            elif memory.getMap() == 64:
                if memory.getCoords()[0] < -4:
                    targetPathing.setMovement([-2, 47])
                else:
                    targetPathing.setMovement([73, 1])
            elif memory.getMap() == 380:
                targetPathing.setMovement([700, 300])
            elif memory.getMap() == 71:
                rikkuNum = memory.actorIndex(actorNum=41)
                targetPathing.setMovement(memory.getActorCoords(rikkuNum))
                if distance(0, rikkuNum) < 30:
                    xbox.tapB()
        else:
            FFXC.set_neutral()
            if memory.diagProgressFlag() == 109:
                memory.csrBaajSaveClear()
            elif memory.diagSkipPossible() and not gameVars.csr():
                xbox.tapB()

    print("Should now be ready for Besaid")

    if not gameVars.csr():
        xbox.clearSavePopup(0)
