import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_memory
import FFX_targetPathing
import FFX_vars
import FFX_Logs
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC


def boatDance():
    print("No dancing this time")
    FFX_memory.waitFrames(30 * 50)


def ssLiki():
    checkpoint = 0
    while FFX_memory.getMap() != 43:
        if FFX_memory.userControl():
            # events
            if checkpoint == 1:  # Group surrounding Yuna
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 3:  # Talk to Wakka
                FFX_memory.clickToEventTemple(3)
                print("Ready for SS Liki menu - (var) ",
                      gameVars.earlyTidusGrid())
                if not gameVars.earlyTidusGrid():
                    FFX_menu.Liki()
                    FFX_memory.closeMenu()
                checkpoint += 1

            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.liki(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif FFX_memory.cutsceneSkipPossible():
                FFX_Xbox.skipScene()
            elif FFX_memory.battleActive():
                print("Ready to start fight with Sin's Fin")
                FFX_Battle.SinFin()
                print("Sin's Fin fight complete. Waiting for next fight")
                FFX_Battle.Echuilles()
                print("Sinspawn Echuilles fight complete")


def get_digit(number, n):
    return number // 10**n % 10


def _set_index_to_value(index, value, power):
    while FFX_memory.oakaGilCursor() != index:
        if FFX_memory.oakaGilCursor() < index:
            FFX_Xbox.tapRight()
        else:
            FFX_Xbox.tapLeft()
    while get_digit(FFX_memory.oakaGilAmount(), power) != value:
        if get_digit(FFX_memory.oakaGilAmount(), power) < value:
            FFX_Xbox.tapUp()
        else:
            FFX_Xbox.tapDown()


def ssWinno():
    FFX_memory.clickToControl()
    FFX_Logs.writeStats("Winno Speed Count:")
    FFX_Logs.writeStats(FFX_memory.getSpeed())

    while FFX_memory.userControl():
        FFX_targetPathing.setMovement([28, -36]) #Through first door
    #FFXC.set_movement(1, -1)
    FFX_memory.waitFrames(2)
    FFX_memory.clickToControl()
    FFXC.set_movement(1, -1)
    FFX_memory.waitFrames(2)

    # Talk to O'akaXXIII
    oakaCoords = [FFX_memory.getActorCoords(
        1)[0], FFX_memory.getActorCoords(1)[1]]
    while FFX_memory.userControl():
        FFX_targetPathing.setMovement(oakaCoords)
        FFX_Xbox.tapB()
        FFX_memory.waitFrames(3)
        oakaCoords = [FFX_memory.getActorCoords(
            1)[0], FFX_memory.getActorCoords(1)[1]]
    FFXC.set_neutral()
    while FFX_memory.oakaInterface() != 12:
        FFX_Xbox.tapB()
    print("Setting Hundreds")
    _set_index_to_value(5, 0, 2)
    print("Setting Thousands")
    _set_index_to_value(4, 1, 3)
    print("Setting Zeroes")
    _set_index_to_value(7, 1, 0)
    while FFX_memory.oakaInterface() != 0:
        FFX_Xbox.tapB()
    while FFX_memory.shopMenuDialogueRow() != 1:
        FFX_Xbox.tapDown()
    FFX_Xbox.tapB()
    FFX_memory.clickToControl3()


def ssWinno2():
    # To the deck
    FFX_memory.awaitControl()
    checkpoint = 0

    while FFX_memory.getStoryProgress() < 395:
        if FFX_memory.userControl():
            if checkpoint < 2 and FFX_memory.getMap() == 94:
                checkpoint = 2
            elif checkpoint == 6:
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint < 11 and FFX_memory.getStoryProgress() == 385:
                checkpoint = 11
            elif checkpoint == 11:
                jechtShot()
                checkpoint += 1
            elif FFX_targetPathing.setMovement(FFX_targetPathing.winno(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    if not gameVars.csr():
        FFX_memory.clickToDiagProgress(142)
        FFX_Xbox.clearSavePopup(0)


def jechtShotSuccess():
    FFXC.set_value('Dpad', 1)  # Up
    FFX_Xbox.tapB()
    FFXC.set_neutral()
    FFXC.set_value('Dpad', 1)  # Up
    FFXC.set_value('Dpad', 8)  # Right
    FFX_Xbox.tapB()
    FFXC.set_neutral()
    FFXC.set_value('Dpad', 8)  # Right
    FFX_Xbox.tapB()
    FFXC.set_neutral()
    FFXC.set_value('Dpad', 8)  # Right
    FFXC.set_value('Dpad', 2)  # Down
    FFX_Xbox.tapB()
    FFXC.set_neutral()
    FFXC.set_value('Dpad', 2)  # Down
    FFX_Xbox.tapB()
    FFXC.set_neutral()
    FFXC.set_value('Dpad', 2)  # Down
    FFXC.set_value('Dpad', 4)  # Left
    FFX_Xbox.tapB()
    FFXC.set_neutral()
    FFXC.set_value('Dpad', 4)  # Left
    FFX_Xbox.tapB()
    FFXC.set_neutral()
    FFXC.set_value('Dpad', 4)  # Left
    FFXC.set_value('Dpad', 1)  # Up
    FFX_Xbox.tapB()
    FFXC.set_neutral()
    FFX_Xbox.tapB()


def jechtShot():
    # Jecht shot tutorial
    print("Ready for Jecht Shot")
    FFX_memory.clickToDiagProgress(96)
    while FFX_memory.diagProgressFlag() != 100:
        if FFX_memory.diagProgressFlag() == 97:
            FFXC.set_value('Dpad', 1)  # Up
            FFXC.set_value('Dpad', 8)  # Right
            FFX_Xbox.tapB()
        elif FFX_memory.diagProgressFlag() == 98:
            FFXC.set_value('Dpad', 4)  # Left
            FFX_Xbox.tapB()
        elif FFX_memory.diagProgressFlag() == 99:
            FFXC.set_value('Dpad', 2)  # Down
            FFXC.set_value('Dpad', 8)  # Right
            FFX_Xbox.tapB()
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
        FFXC.set_neutral()

    # Failure logic
    FFX_Xbox.SkipDialog(2)
    print("End Jecht Shot")
    print("We are intentionally failing the Jecht shot. Save the frames!")

    # Success logic
    # for i in range(15):
    #    jechtShotSuccess()
    # Does not work with CSR version 1.2.0
