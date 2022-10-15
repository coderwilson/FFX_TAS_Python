import battle.main
import memory.main
import menu
import screen
import targetPathing
import vars
import xbox

FFXC = xbox.controllerHandle()
gameVars = vars.varsHandle()


def Entrance():
    memory.main.awaitControl()
    print("Starting Baaj exterior area")
    FFXC.set_neutral()
    menu.shortAeons()

    # Now back into the water
    checkpoint = 0
    while not memory.main.battleActive():
        if memory.main.userControl():
            if checkpoint == 6:
                memory.main.clickToEventTemple(0)
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.baajRamp(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()

    FFXC.set_neutral()

    # Battles
    while memory.main.getStoryProgress() < 48:
        if screen.BattleScreen():
            if memory.main.getEncounterID() == 2:
                battle.main.attack('none')
            else:
                battle.main.defend()
        elif memory.main.diagSkipPossible():
            xbox.menuB()

    # Out of the frying pan, into the furnace
    memory.main.clickToControl()
    print("Hallway before main puzzle.")
    checkpoint = 0
    while memory.main.getMap() != 63:
        if memory.main.userControl():
            if checkpoint == 9:
                FFXC.set_movement(-1, 1)
                memory.main.awaitEvent()
                FFXC.set_neutral()
            # General pathing
            elif targetPathing.setMovement(targetPathing.baajHallway(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()


def Baaj_puzzle():
    memory.main.clickToControl()
    print("Ready for the main puzzle.")
    checkpoint = 0
    while not memory.main.battleActive():
        if memory.main.userControl():
            # Events
            if checkpoint == 3:
                memory.main.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 5:  # Flint room
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 6:  # Obtain Flint
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 7:  # Exit Flint room
                memory.main.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 12:  # Bouquet hallway
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 21:  # Withered bouquet
                memory.main.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 32:  # Back to main room
                memory.main.clickToEventTemple(2)
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
            if memory.main.diagSkipPossible():
                xbox.tapB()


def Klikk_fight():
    # Before Rikku shows up, we're just going to spam the B button. Simple.
    FFXC.set_neutral()
    while not screen.turnRikku():
        xbox.tapB()

    xbox.clickToBattle()
    battle.main.useItem(0, 'none')  # Tidus self-potion
    screen.awaitTurn()
    battle.main.Klikk()


def distance(n1, n2):
    try:
        player1 = memory.main.getActorCoords(actorNumber=n1)
        player2 = memory.main.getActorCoords(actorNumber=n2)
        return (abs(player1[1] - player2[1]) + abs(player1[0] - player2[0]))
    except Exception as x:
        print("Exception:", x)
        return 999


def ABboat1():
    print("Start of Al Bhed boat section.")
    print("Control restored.")
    print("On the boat!")
    while memory.main.getActorCoords(actorNumber=0)[0] > -50:
        rikkuNum = memory.main.actorIndex(actorNum=41)
        target = memory.main.getActorCoords(actorNumber=rikkuNum)
        targetPathing.setMovement(target)
        if distance(0, rikkuNum) < 10:
            xbox.tapB()
        elif memory.main.menuOpen():
            xbox.menuA()
            xbox.menuB()
    print("In the water!")
    FFXC.set_value('BtnA', 1)
    while not memory.main.userControl():
        FFXC.set_value('BtnB', 1)
        memory.main.waitFrames(1)
        FFXC.set_value('BtnB', 0)
        memory.main.waitFrames(1)
    FFXC.set_value('BtnA', 1)
    FFXC.set_movement(-1, -1)
    memory.main.waitFrames(20)

    while memory.main.getMap() != 288:
        FFXC.set_value('BtnA', 1)
        FFXC.set_movement(0, -1)
        if memory.main.battleActive():
            FFXC.set_neutral()
            print("Battle Start (Al Bhed swimming section)")
            battle.main.stealAndAttack()
            print("Battle End (Al Bhed swimming section)")
        elif memory.main.menuOpen() or memory.main.diagSkipPossible():
            print("Battle Complete screen")
            xbox.tapB()


def ABswimming1():
    print("Swimming down from the boat")
    while memory.main.getMap() != 288:
        if memory.main.userControl():
            targetPathing.setMovement([-300, -300])
            FFXC.set_value('BtnA', 1)
        else:
            FFXC.set_neutral()
            if screen.BattleScreen():
                print("Battle Start (Al Bhed swimming section)")
                battle.main.stealAndAttack()
                print("Battle End (Al Bhed swimming section)")
            elif memory.main.menuOpen():
                print("Battle Complete screen")
                xbox.menuB()

    FFXC.set_neutral()
    print("Swimming towards airship")
    while memory.main.getMap() != 64:
        pos = memory.main.getCoords()
        if memory.main.userControl():
            if memory.main.getMap() == 71:
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
                battle.main.stealAndAttack()
                print("Battle End (Al Bhed swimming section)")
            elif memory.main.menuOpen():
                print("Battle Complete screen")
                xbox.menuB()


def ABswimming2():
    # Quick heal-up to make sure we're full HP on Rikku
    memory.main.awaitControl()
    FFXC.set_movement(1, -1)
    FFXC.set_value('BtnA', 1)
    memory.main.touchSaveSphere()

    memory.main.clearSaveMenuCursor2()
    # Now to get to it
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 1)
    memory.main.clickToEvent()
    memory.main.waitFrames(30 * 0.2)
    memory.main.awaitControl()

    pos = memory.main.getCoords()
    while memory.main.userControl():
        if pos[1] < 135:
            FFXC.set_movement(1, 1)
        else:
            FFXC.set_movement(0, 1)

        pos = memory.main.getCoords()
    FFXC.set_neutral()

    screen.awaitTurn()
    # Final group of Piranhas
    battle.main.stealAndAttackPreTros()
    memory.main.awaitControl()
    FFXC.set_movement(0, 1)
    print("Technical Support Tidus")
    xbox.SkipDialog(2)
    FFXC.set_movement(0, 0)
    memory.main.clickToControl()
    while not memory.main.battleActive():
        FFXC.set_movement(0, -1)
    print("Engaging Tros")
    FFXC.set_neutral()

    # Tros fight
    xbox.clickToBattle()
    battle.main.Tros()

    FFXC.set_neutral()
    while memory.main.getStoryProgress() < 111:
        if memory.main.userControl():
            if memory.main.diagProgressFlag() == 109 and not memory.main.userControl():
                FFXC.set_neutral()
                if memory.main.saveMenuCursor2() == 0:
                    xbox.tapA()
                else:
                    xbox.tapB()
                memory.main.waitFrames(4)
            elif memory.main.getMap() == 64:
                if memory.main.getCoords()[0] < -4:
                    targetPathing.setMovement([-2, 47])
                else:
                    targetPathing.setMovement([73, 1])
            elif memory.main.getMap() == 380:
                targetPathing.setMovement([700, 300])
            elif memory.main.getMap() == 71:
                rikkuNum = memory.main.actorIndex(actorNum=41)
                targetPathing.setMovement(memory.main.getActorCoords(rikkuNum))
                if distance(0, rikkuNum) < 30:
                    xbox.tapB()
        else:
            FFXC.set_neutral()
            if memory.main.diagProgressFlag() == 109:
                memory.main.csrBaajSaveClear()
            elif memory.main.diagSkipPossible() and not gameVars.csr():
                xbox.tapB()

    print("Should now be ready for Besaid")

    if not gameVars.csr():
        xbox.clearSavePopup(0)
