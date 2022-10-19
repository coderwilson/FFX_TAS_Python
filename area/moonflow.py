import battle.boss
import battle.main
import memory.main
import menu
import screen
import targetPathing
import vars
import xbox

gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def arrival():
    print("Starting Moonflow section")

    checkpoint = 0
    while memory.main.getMap() != 235:
        if memory.main.userControl():
            # Chests
            if checkpoint == 2:  # Gil outside Djose temple
                print("Djose gil chest")
                FFXC.set_movement(-1, 1)
                xbox.SkipDialog(1)
                FFXC.set_movement(1, -1)
                memory.main.clickToControl()
                checkpoint += 1
            elif checkpoint == 43:  # Moonflow chest
                if memory.main.getItemSlot(90) < 200:
                    checkpoint += 1
                else:
                    targetPathing.setMovement([-1796, -480])
                    xbox.tapB()

            # Map changes
            elif checkpoint < 6 and memory.main.getMap() == 76:
                checkpoint = 6
            elif checkpoint < 11 and memory.main.getMap() == 93:
                checkpoint = 11
            elif checkpoint < 14 and memory.main.getMap() == 75:
                checkpoint = 14
            elif checkpoint < 49 and memory.main.getMap() == 105:
                checkpoint = 49
            elif checkpoint < 54 and memory.main.getStoryProgress() == 1045:
                checkpoint = 54
                print("Updating checkpoint based on story/map progress:", checkpoint)
            elif checkpoint == 54 and memory.main.getMap() == 188:
                checkpoint = 55
                print("Updating checkpoint based on story/map progress:", checkpoint)

            # General pathing
            elif targetPathing.setMovement(targetPathing.moonflow(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if screen.BattleScreen():
                battle.main.fleeAll()
            elif memory.main.menuOpen():
                xbox.tapB()
            elif memory.main.diagSkipPossible():
                xbox.tapB()
    print("End of approaching section, should now be talking to Lucille/Elma/etc.")


def southBank(checkpoint: int = 0):
    # Arrive at the south bank of the moonflow.
    print("South bank, Save sphere screen")

    memory.main.clickToControl3()  # "Where there's a will, there's a way."
    FFXC.set_movement(1, -1)
    memory.main.waitFrames(30 * 1)
    FFXC.set_neutral()

    memory.main.clickToControl3()
    partyHP = memory.main.getHP()
    if partyHP[4] < 800:
        battle.main.healUp(2)
    elif partyHP[0] < 700:
        battle.main.healUp(1)
    memory.main.closeMenu()

    while not memory.main.battleActive():
        if memory.main.userControl():
            if checkpoint == 4:
                FFXC.set_neutral()
                memory.main.clickToEvent()
                memory.main.waitFrames(18)
                xbox.menuB()  # Ride ze Shoopuff?
                memory.main.waitFrames(10)
                xbox.menuDown()
                xbox.menuB()  # All aboardz!
                xbox.SkipDialog(3)  # Just to clear some dialog

            elif targetPathing.setMovement(targetPathing.moonflowBankSouth(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()

    battle.boss.extractor()


def northBank():
    memory.main.clickToControl3()
    FFXC.set_movement(-1, 0)
    memory.main.awaitEvent()
    memory.main.waitFrames(30 * 1)
    memory.main.awaitControl()
    if gameVars.csr():
        memory.main.waitFrames(10)
        FFXC.set_movement(-1, -0.7)
        memory.main.waitFrames(6)
        FFXC.set_movement(-1, 0)
        memory.main.awaitEvent()
    else:
        memory.main.waitFrames(45)
        memory.main.clickToEvent()  # Talk to Auron
        FFXC.set_neutral()
        memory.main.waitFrames(9)
        memory.main.clickToControl3()
    FFXC.set_movement(-1, 0)
    memory.main.waitFrames(15)
    memory.main.awaitEvent()
    FFXC.set_neutral()
    memory.main.waitFrames(15)
    if gameVars.getLStrike() % 2 == 1:
        menu.equipWeapon(character=0, special='brotherhoodearly')

    checkpoint = 0
    print("Miihen North Bank pattern. Starts after talking to Auron.")
    while memory.main.getMap() != 135:
        if memory.main.userControl():
            if checkpoint == 7:  # Rikku steal/mix tutorial
                FFXC.set_movement(1, 1)
                memory.main.awaitEvent()
                FFXC.set_neutral()
                battle.main.mixTutorial()
                memory.main.fullPartyFormat("postbunyip")
                memory.main.closeMenu()
                checkpoint += 1
            elif memory.main.getStoryProgress() >= 1085 and checkpoint < 4:
                checkpoint = 4
                print("Rikku scene, updating checkpoint:", checkpoint)

            # Map changes
            elif checkpoint < 2 and memory.main.getMap() == 109:
                checkpoint = 2
            elif checkpoint < 12 and memory.main.getMap() == 97:
                checkpoint = 12

            # General pathing
            elif targetPathing.setMovement(targetPathing.moonflowBankNorth(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if screen.BattleScreen():
                battle.main.fleeAll()
            elif memory.main.diagSkipPossible() and not memory.main.battleActive():
                xbox.tapB()
            elif memory.main.menuOpen():
                xbox.tapB()
