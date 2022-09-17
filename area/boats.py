import xbox
import battle.main
import menu
import memory.main
import targetPathing
import vars
import logs
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def boatDance():
    print("No dancing this time")
    memory.main.waitFrames(30 * 50)


def ssLiki():
    checkpoint = 0
    while memory.main.getMap() != 43:
        if memory.main.userControl():
            # events
            if checkpoint == 1:  # Group surrounding Yuna
                memory.main.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 3:  # Talk to Wakka
                memory.main.clickToEventTemple(3)
                print("Ready for SS Liki menu - (var) ",
                      gameVars.earlyTidusGrid())
                if not gameVars.earlyTidusGrid():
                    menu.Liki()
                    memory.main.closeMenu()
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.liki(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible() or memory.main.menuOpen():
                xbox.tapB()
            elif memory.main.cutsceneSkipPossible():
                xbox.skipScene()
            elif memory.main.battleActive():
                print("Ready to start fight with Sin's Fin")
                battle.main.SinFin()
                print("Sin's Fin fight complete. Waiting for next fight")
                battle.main.Echuilles()
                print("Sinspawn Echuilles fight complete")


def get_digit(number, n):
    return number // 10**n % 10


def _set_index_to_value(index, value, power):
    while memory.main.oakaGilCursor() != index:
        if memory.main.oakaGilCursor() < index:
            xbox.tapRight()
        else:
            xbox.tapLeft()
    while get_digit(memory.main.oakaGilAmount(), power) != value:
        if get_digit(memory.main.oakaGilAmount(), power) < value:
            xbox.tapUp()
        else:
            xbox.tapDown()


def ssWinno():
    memory.main.clickToControl()
    # logs.writeStats("Winno Speed Count:")
    # logs.writeStats(memory.getSpeed())

    while memory.main.userControl():
        targetPathing.setMovement([28, -36])  # Through first door
    memory.main.waitFrames(2)
    memory.main.clickToControl()
    FFXC.set_movement(1, -1)
    memory.main.waitFrames(2)

    # Talk to O'akaXXIII
    oakaCoords = [memory.main.getActorCoords(
        1)[0], memory.main.getActorCoords(1)[1]]
    while memory.main.userControl():
        targetPathing.setMovement(oakaCoords)
        xbox.tapB()
        memory.main.waitFrames(3)
        oakaCoords = [memory.main.getActorCoords(
            1)[0], memory.main.getActorCoords(1)[1]]
    FFXC.set_neutral()
    while memory.main.oakaInterface() != 12:
        xbox.tapB()
    print("Setting Hundreds")
    _set_index_to_value(5, 0, 2)
    print("Setting Thousands")
    _set_index_to_value(4, 1, 3)
    print("Setting Zeroes")
    _set_index_to_value(7, 1, 0)
    while memory.main.oakaInterface() != 0:
        xbox.tapB()
    while memory.main.shopMenuDialogueRow() != 1:
        xbox.tapDown()
    xbox.tapB()
    memory.main.clickToControl3()


def ssWinno2():
    # To the deck
    memory.main.awaitControl()
    checkpoint = 0

    while memory.main.getStoryProgress() < 395:
        if memory.main.userControl():
            if checkpoint < 2 and memory.main.getMap() == 94:
                checkpoint = 2
            elif checkpoint == 6:
                memory.main.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint < 11 and memory.main.getStoryProgress() == 385:
                checkpoint = 11
            elif checkpoint == 11:
                jechtShot()
                checkpoint += 1
            elif targetPathing.setMovement(targetPathing.winno(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()
    if not gameVars.csr():
        memory.main.clickToDiagProgress(142)
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
    memory.main.clickToDiagProgress(96)
    while memory.main.diagProgressFlag() != 100:
        if memory.main.diagProgressFlag() == 97:
            FFXC.set_value('Dpad', 1)  # Up
            FFXC.set_value('Dpad', 8)  # Right
            xbox.tapB()
        elif memory.main.diagProgressFlag() == 98:
            FFXC.set_value('Dpad', 4)  # Left
            xbox.tapB()
        elif memory.main.diagProgressFlag() == 99:
            FFXC.set_value('Dpad', 2)  # Down
            FFXC.set_value('Dpad', 8)  # Right
            xbox.tapB()
        elif memory.main.diagSkipPossible():
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
