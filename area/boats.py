import xbox
import battle
import menu
import memory
import targetPathing
import vars
import logs
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def boatDance():
    print("No dancing this time")
    memory.waitFrames(30 * 50)


def ssLiki():
    checkpoint = 0
    while memory.getMap() != 43:
        if memory.userControl():
            # events
            if checkpoint == 1:  # Group surrounding Yuna
                memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 3:  # Talk to Wakka
                memory.clickToEventTemple(3)
                print("Ready for SS Liki menu - (var) ",
                      gameVars.earlyTidusGrid())
                if not gameVars.earlyTidusGrid():
                    menu.Liki()
                    memory.closeMenu()
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.liki(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible() or memory.menuOpen():
                xbox.tapB()
            elif memory.cutsceneSkipPossible():
                xbox.skipScene()
            elif memory.battleActive():
                print("Ready to start fight with Sin's Fin")
                battle.SinFin()
                print("Sin's Fin fight complete. Waiting for next fight")
                battle.Echuilles()
                print("Sinspawn Echuilles fight complete")


def get_digit(number, n):
    return number // 10**n % 10


def _set_index_to_value(index, value, power):
    while memory.oakaGilCursor() != index:
        if memory.oakaGilCursor() < index:
            xbox.tapRight()
        else:
            xbox.tapLeft()
    while get_digit(memory.oakaGilAmount(), power) != value:
        if get_digit(memory.oakaGilAmount(), power) < value:
            xbox.tapUp()
        else:
            xbox.tapDown()


def ssWinno():
    memory.clickToControl()
    # logs.writeStats("Winno Speed Count:")
    # logs.writeStats(memory.getSpeed())

    while memory.userControl():
        targetPathing.setMovement([28, -36])  # Through first door
    memory.waitFrames(2)
    memory.clickToControl()
    FFXC.set_movement(1, -1)
    memory.waitFrames(2)

    # Talk to O'akaXXIII
    oakaCoords = [memory.getActorCoords(
        1)[0], memory.getActorCoords(1)[1]]
    while memory.userControl():
        targetPathing.setMovement(oakaCoords)
        xbox.tapB()
        memory.waitFrames(3)
        oakaCoords = [memory.getActorCoords(
            1)[0], memory.getActorCoords(1)[1]]
    FFXC.set_neutral()
    while memory.oakaInterface() != 12:
        xbox.tapB()
    print("Setting Hundreds")
    _set_index_to_value(5, 0, 2)
    print("Setting Thousands")
    _set_index_to_value(4, 1, 3)
    print("Setting Zeroes")
    _set_index_to_value(7, 1, 0)
    while memory.oakaInterface() != 0:
        xbox.tapB()
    while memory.shopMenuDialogueRow() != 1:
        xbox.tapDown()
    xbox.tapB()
    memory.clickToControl3()


def ssWinno2():
    # To the deck
    memory.awaitControl()
    checkpoint = 0

    while memory.getStoryProgress() < 395:
        if memory.userControl():
            if checkpoint < 2 and memory.getMap() == 94:
                checkpoint = 2
            elif checkpoint == 6:
                memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint < 11 and memory.getStoryProgress() == 385:
                checkpoint = 11
            elif checkpoint == 11:
                jechtShot()
                checkpoint += 1
            elif targetPathing.setMovement(targetPathing.winno(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()
    if not gameVars.csr():
        memory.clickToDiagProgress(142)
        xbox.clearSavePopup(0)


def jechtShotSuccess():
    FFXC.set_value('Dpad', 1)  # Up
    xbox.tapB()
    FFXC.set_neutral()
    FFXC.set_value('Dpad', 1)  # Up
    FFXC.set_value('Dpad', 8)  # Right
    xbox.tapB()
    FFXC.set_neutral()
    FFXC.set_value('Dpad', 8)  # Right
    xbox.tapB()
    FFXC.set_neutral()
    FFXC.set_value('Dpad', 8)  # Right
    FFXC.set_value('Dpad', 2)  # Down
    xbox.tapB()
    FFXC.set_neutral()
    FFXC.set_value('Dpad', 2)  # Down
    xbox.tapB()
    FFXC.set_neutral()
    FFXC.set_value('Dpad', 2)  # Down
    FFXC.set_value('Dpad', 4)  # Left
    xbox.tapB()
    FFXC.set_neutral()
    FFXC.set_value('Dpad', 4)  # Left
    xbox.tapB()
    FFXC.set_neutral()
    FFXC.set_value('Dpad', 4)  # Left
    FFXC.set_value('Dpad', 1)  # Up
    xbox.tapB()
    FFXC.set_neutral()
    xbox.tapB()


def jechtShot():
    # Jecht shot tutorial
    print("Ready for Jecht Shot")
    memory.clickToDiagProgress(96)
    while memory.diagProgressFlag() != 100:
        if memory.diagProgressFlag() == 97:
            FFXC.set_value('Dpad', 1)  # Up
            FFXC.set_value('Dpad', 8)  # Right
            xbox.tapB()
        elif memory.diagProgressFlag() == 98:
            FFXC.set_value('Dpad', 4)  # Left
            xbox.tapB()
        elif memory.diagProgressFlag() == 99:
            FFXC.set_value('Dpad', 2)  # Down
            FFXC.set_value('Dpad', 8)  # Right
            xbox.tapB()
        elif memory.diagSkipPossible():
            xbox.tapB()
        FFXC.set_neutral()

    # Failure logic
    xbox.SkipDialog(2)
    print("End Jecht Shot")
    print("We are intentionally failing the Jecht shot. Save the frames!")

    # Success logic
    # for i in range(15):
    #    jechtShotSuccess()
    # Does not work with CSR version 1.2.0
