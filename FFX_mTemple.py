import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory
import FFX_targetPathing
import FFX_vars
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC


def approach():
    print("------------------------------Affection array:")
    print(FFX_memory.affectionArray())
    print("------------------------------")
    FFX_memory.clickToControl()
    print("Approaching Macalania Temple")

    checkpoint = 0
    while FFX_memory.getMap() != 106:
        if FFX_memory.userControl():
            # Map changes
            if checkpoint < 2 and FFX_memory.getMap() == 153:
                checkpoint = 2

            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.mTempleApproach(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    FFXC.set_neutral()


def arrival(doGrid=True):
    print("Starting Macalania Temple section")
    FFX_memory.awaitControl()
    if doGrid:
        FFX_menu.macTemple()

    # Movement:
    jyscalSkipStatus = False
    checkpoint = 0
    skipStatus = True
    while FFX_memory.getMap() != 80:
        if FFX_memory.userControl():
            # Main events
            if checkpoint == 1:
                FFXC.set_neutral()
                FFX_memory.waitFrames(30 * 0.2)
                FFX_memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 2 and gameVars.csr():
                checkpoint = 11
            elif checkpoint == 4:  # Talking to Trommell
                FFX_memory.clickToEventTemple(6)
                if FFX_memory.getCoords()[0] < 23.5:
                    FFX_memory.waitFrames(30 * 0.07)
                    FFXC.set_movement(1, 0)
                    FFX_memory.waitFrames(2)
                    FFXC.set_neutral()
                    FFX_memory.waitFrames(4)
                checkpoint += 1
            elif checkpoint == 5:  # Skip (new)
                print("Lining up for skip.")
                FFXC.set_movement(0, -1)
                FFX_memory.waitFrames(30 * 0.2)
                FFXC.set_neutral()
                while FFX_memory.getCoords()[1] < -101.5:
                    FFXC.set_value('Dpad', 8)
                    FFX_memory.waitFrames(2)
                    FFXC.set_value('Dpad', 0)
                    FFX_memory.waitFrames(5)

                print("Turning back")
                FFX_memory.waitFrames(3)
                FFXC.set_movement(-1, 0)
                FFX_memory.waitFrames(2)
                FFXC.set_neutral()
                FFX_memory.waitFrames(15)

                print("Now lined up. Here we go.")
                FFXC.set_movement(1, 0)
                FFX_memory.waitFrames(3)
                FFXC.set_value('BtnB', 1)
                FFX_memory.waitFrames(4)
                FFXC.set_value('BtnB', 0)
                FFX_memory.waitFrames(45)
                FFXC.set_neutral()
                checkpoint += 1
                FFX_memory.clickToControl3()
            elif checkpoint == 6:
                checkpoint = 11
            elif checkpoint == 11:
                print("Check if skip is online")
                if gameVars.csr():
                    jyscalSkipStatus = True
                    checkpoint += 1
                elif FFX_memory.getStoryProgress() < 1505:
                    jyscalSkipStatus = True
                    checkpoint += 1
                else:
                    jyscalSkipStatus = False
                    checkpoint = 20
                    skipStatus = False
                print("Jyscal Skip results:", skipStatus)
            elif checkpoint == 14 and gameVars.csr():
                FFXC.set_movement(0, 1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 14:  # Pause so we don't mess up the skip
                if skipStatus == True:
                    FFXC.set_neutral()
                    # while FFX_memory.getCamera()[3] > -20:
                    #    FFX_Xbox.tapB()
                    FFX_Xbox.SkipDialog(5)
                    FFXC.set_movement(0, -1)
                    FFX_memory.awaitEvent()
                    FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint < 16 and FFX_memory.getMap() == 239:
                checkpoint = 16

            # Recovery items
            elif checkpoint == 23:  # Door, Jyscal room
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 24:  # Back to the main room
                FFX_memory.clickToEventTemple(5)
                checkpoint += 1
            elif checkpoint == 27:
                checkpoint = 12

            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.templeFoyer(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    return jyscalSkipStatus


def startSeymourFight():
    FFX_memory.clickToControl()
    while FFX_targetPathing.setMovement([9, -53]) == False:
        doNothing = True  # Allows us to move to the Seymour fight.
    FFXC.set_movement(1, 0)
    FFX_memory.awaitEvent()
    FFXC.set_neutral()


def seymourFight():
    FFX_Battle.seymourGuado()

    # Name for Shiva
    FFX_Xbox.nameAeon("Shiva")

    #FFX_memory.waitFrames(30 * 1)
    # FFX_Xbox.menuB()
    #FFX_memory.waitFrames(30 * 0.2)
    # FFX_Xbox.menuUp()
    # FFX_Xbox.menuB()

    FFX_memory.awaitControl()
    FFXC.set_movement(-1, -1)
    FFX_memory.waitFrames(30 * 0.4)
    FFXC.set_movement(-1, 0)
    FFX_memory.awaitEvent()
    FFXC.set_neutral()


def trials():
    FFX_memory.awaitControl()

    checkpoint = 0
    while FFX_memory.getMap() != 153:
        if FFX_memory.userControl():
            # CSR start point
            if checkpoint < 3 and gameVars.csr():
                checkpoint = 3

            # Map changes
            elif checkpoint < 2 and FFX_memory.getMap() == 239:
                checkpoint = 2

            #Spheres and Pedestals
            elif checkpoint == 2:
                FFX_memory.awaitControl()
                print("Activate the trials")
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 9:  # Push pedestal - 1
                FFXC.set_movement(1, 0)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_memory.waitFrames(30 * 1)
                checkpoint += 1
            elif checkpoint == 13:  # Grab first Mac Sphere
                FFX_memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 17:  # Place first Mac Sphere
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 20:  # Push pedestal - 2
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 23:  # Grab glyph sphere
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
                print("Checkpoint:", checkpoint)
            elif checkpoint == 29:  # Push pedestal - 3
                FFXC.set_movement(1, 0)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_memory.waitFrames(30 * 1)
                checkpoint += 1
            elif checkpoint == 32:  # Place Glyph sphere
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 39:  # Grab second Mac sphere
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 46:  # Place second Mac sphere
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 51:  # Grab third Mac sphere
                FFX_memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 53:  # Place third Mac sphere
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 58:  # End of trials
                FFX_memory.clickToEventTemple(0)
                FFX_memory.awaitControl()
                # Just to start the next set of dialog.
                FFX_memory.clickToEventTemple(4)

            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.mTempleTrials(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()


def escape():
    FFX_memory.clickToControl()
    print("First, some menuing")
    menuDone = False
    if gameVars.nemesis():
        FFX_memory.fullPartyFormat('yuna', fullMenuClose=False)
    else:
        FFX_menu.afterSeymour()
        menuDone = True
        FFX_memory.fullPartyFormat('macalaniaescape', fullMenuClose=False)
    FFX_menu.equipSonicSteel(fullMenuClose=True)

    print("Now to escape the Guado")
    forceBattle = False
    # if FFX_memory.rngSeed() == 31:
    #    forceBattle = True

    checkpoint = 0
    while FFX_memory.getBattleNum() != 195:
        if FFX_memory.userControl():
            # Events
            if checkpoint == 2:
                FFX_memory.touchSaveSphere()
                checkpoint += 1
                print("Touching save sphere. Update checkpoint:", checkpoint)
            elif checkpoint == 18 and forceBattle:
                FFXC.set_neutral()

            # Map changes
            elif checkpoint < 19 and FFX_memory.getMap() == 192:
                checkpoint = 19
                print("Map change. Update checkpoint:", checkpoint)

            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.mTempleEscape(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                FFX_Screen.awaitTurn()
                if checkpoint < 19:
                    FFX_Battle.fleeAll()
                    forceBattle = False
                elif not menuDone:
                    FFX_Battle.escapeWithXP()
                    FFX_menu.afterSeymour()
                    menuDone = True
                    FFX_memory.fullPartyFormat('macalaniaescape')
                elif FFX_memory.getBattleNum() == 195:
                    break
                else:
                    FFX_Battle.fleeAll()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

    print("Done pathing. Now for the Wendigo fight.")
    FFX_Battle.wendigo()
    print("Wendigo fight over")


def underLake():
    FFX_memory.clickToControl()
    checkpoint = 0
    while FFX_memory.getMap() != 129:
        if FFX_memory.userControl():
            if checkpoint == 4:
                FFXC.set_movement(0, 1)
                FFX_memory.clickToEvent()
                FFXC.set_neutral()
                FFX_memory.clickToControl()
                FFXC.set_movement(0, 1)
                FFX_memory.waitFrames(2)
                FFX_memory.clickToEvent()
                FFXC.set_neutral()
                FFX_memory.clickToControl()
                checkpoint += 1
            elif checkpoint == 11:
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 15:
                while FFX_memory.userControl():
                    FFX_targetPathing.setMovement([-4, -8])
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                FFX_memory.clickToControl3()
                checkpoint += 1

            # General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.underMacTemple(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
            # elif FFX_memory.cutsceneSkipPossible():
            #    FFX_Xbox.skipScene()
    FFXC.set_neutral()
    FFX_memory.clickToControl()


def underLake_old():
    FFX_memory.clickToControl()
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_movement(-1, 1)
    FFX_memory.waitFrames(30 * 0.8)
    FFXC.set_movement(1, 1)
    FFX_memory.waitFrames(30 * 1)
    FFXC.set_movement(0, 1)
    FFX_memory.clickToEvent()
    FFXC.set_neutral()

    FFX_memory.clickToControl()
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 1.5)  # Approach Yuna
    FFXC.set_neutral()

    FFX_memory.clickToControl()
    while FFX_memory.getCoords()[1] > 110:
        FFXC.set_movement(-1, 1)
    while FFX_memory.getCoords()[1] > 85:
        FFXC.set_movement(1, 1)
    while FFX_memory.getCoords()[0] > -30:
        if FFX_memory.getCoords()[1] < 110:
            FFXC.set_movement(1, -1)
        else:
            FFXC.set_movement(1, 0)
    FFXC.set_movement(1, 0)
    FFX_memory.clickToEvent()  # Chest with Lv.2 Key Sphere
    FFXC.set_neutral()
    FFX_Xbox.SkipDialog(0.2)
    FFX_memory.clickToControl()
    FFXC.set_movement(-1, 0)
    FFX_memory.waitFrames(30 * 0.25)
    while FFX_memory.getCoords()[0] < -5:
        FFXC.set_movement(-1, 1)
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 1)  # To Auron
    FFX_Xbox.SkipDialog(1.5)
    FFXC.set_movement(1, 0)
    FFX_Xbox.SkipDialog(0.4)
    FFXC.set_movement(-1, 0)
    FFX_Xbox.SkipDialog(0.4)
    FFXC.set_neutral()
    FFX_memory.clickToControl()

    while FFX_memory.getMap() != 129:
        FFXC.set_movement(0, -1)
        if FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
        elif FFX_memory.cutsceneSkipPossible():
            FFX_Xbox.skipScene()
    FFXC.set_neutral()
    FFX_memory.clickToControl()
