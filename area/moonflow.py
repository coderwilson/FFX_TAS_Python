import xbox
import screen
import battle
import memory
import targetPathing
import vars
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def arrival():
    print("Starting Moonflow section")

    checkpoint = 0
    while memory.getMap() != 235:
        if memory.userControl():
            # Chests
            if checkpoint == 2:  # Gil outside Djose temple
                print("Djose gil chest")
                FFXC.set_movement(-1, 1)
                xbox.SkipDialog(1)
                FFXC.set_movement(1, -1)
                memory.clickToControl()
                checkpoint += 1
            elif checkpoint == 43:  # Moonflow chest
                if memory.getItemSlot(90) < 200:
                    checkpoint += 1
                else:
                    targetPathing.setMovement([-1796, -480])
                    xbox.tapB()

            # Map changes
            elif checkpoint < 6 and memory.getMap() == 76:
                checkpoint = 6
            elif checkpoint < 11 and memory.getMap() == 93:
                checkpoint = 11
            elif checkpoint < 14 and memory.getMap() == 75:
                checkpoint = 14
            elif checkpoint < 49 and memory.getMap() == 105:
                checkpoint = 49
            elif checkpoint < 54 and memory.getStoryProgress() == 1045:
                checkpoint = 54
                print("Updating checkpoint based on story/map progress:", checkpoint)
            elif checkpoint == 54 and memory.getMap() == 188:
                checkpoint = 55
                print("Updating checkpoint based on story/map progress:", checkpoint)

            # General pathing
            elif targetPathing.setMovement(targetPathing.moonflow(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if screen.BattleScreen():
                battle.fleeAll()
            elif memory.menuOpen():
                xbox.tapB()
            elif memory.diagSkipPossible():
                xbox.tapB()
    print("End of approaching section, should now be talking to Lucille/Elma/etc.")


def southBank(checkpoint: int = 0):
    # Arrive at the south bank of the moonflow.
    print("South bank, Save sphere screen")

    memory.clickToControl3()  # "Where there's a will, there's a way."
    FFXC.set_movement(1, -1)
    memory.waitFrames(30 * 1)
    FFXC.set_neutral()

    memory.clickToControl3()
    partyHP = memory.getHP()
    if partyHP[4] < 800:
        battle.healUp(2)
    elif partyHP[0] < 700:
        battle.healUp(1)
    memory.closeMenu()

    while not memory.battleActive():
        if memory.userControl():
            if checkpoint == 4:
                FFXC.set_neutral()
                memory.clickToEvent()
                memory.waitFrames(18)
                xbox.menuB()  # Ride ze Shoopuff?
                memory.waitFrames(10)
                xbox.menuDown()
                xbox.menuB()  # All aboardz!
                xbox.SkipDialog(3)  # Just to clear some dialog

            elif targetPathing.setMovement(targetPathing.moonflowBankSouth(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()

    battle.extractor()


def northBank():
    memory.clickToControl3()
    FFXC.set_movement(-1, 0)
    memory.awaitEvent()
    memory.waitFrames(30 * 1)
    memory.awaitControl()
    memory.waitFrames(30 * 1.5)
    if gameVars.csr():
        FFXC.set_movement(-1, 1)
        memory.waitFrames(4)
    else:
        memory.clickToEvent()  # Talk to Auron
        FFXC.set_neutral()
        memory.waitFrames(30 * 0.3)
        memory.clickToControl3()
    FFXC.set_movement(-1, 0)
    memory.waitFrames(30 * 0.5)
    memory.awaitEvent()
    FFXC.set_neutral()
    memory.waitFrames(30 * 0.5)

    checkpoint = 0
    print("Miihen North Bank pattern. Starts after talking to Auron.")
    while memory.getMap() != 135:
        if memory.userControl():
            if checkpoint == 7:  # Rikku steal/mix tutorial
                FFXC.set_movement(1, 1)
                memory.awaitEvent()
                FFXC.set_neutral()
                battle.mixTutorial()
                memory.fullPartyFormat("postbunyip")
                memory.closeMenu()
                checkpoint += 1
            elif memory.getStoryProgress() >= 1085 and checkpoint < 4:
                checkpoint = 4
                print("Rikku scene, updating checkpoint:", checkpoint)

            # Map changes
            elif checkpoint < 2 and memory.getMap() == 109:
                checkpoint = 2
            elif checkpoint < 12 and memory.getMap() == 97:
                checkpoint = 12

            # General pathing
            elif targetPathing.setMovement(targetPathing.moonflowBankNorth(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if screen.BattleScreen():
                battle.fleeAll()
            elif memory.diagSkipPossible() and not memory.battleActive():
                xbox.tapB()
            elif memory.menuOpen():
                xbox.tapB()
