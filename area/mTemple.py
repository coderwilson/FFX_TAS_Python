import xbox
import screen
import battle
import menu
import memory
import targetPathing
import vars
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def approach():
    print("------------------------------Affection array:")
    print(memory.affectionArray())
    print("------------------------------")
    memory.clickToControl()
    print("Approaching Macalania Temple")

    checkpoint = 0
    while memory.getMap() != 106:
        if memory.userControl():
            # Map changes
            if checkpoint < 2 and memory.getMap() == 153:
                checkpoint = 2

            # General pathing
            elif targetPathing.setMovement(targetPathing.mTempleApproach(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()
    FFXC.set_neutral()


def arrival(doGrid=True):
    print("Starting Macalania Temple section")
    memory.awaitControl()
    if doGrid:
        menu.macTemple()

    # Movement:
    jyscalSkipStatus = False
    checkpoint = 0
    skipStatus = True
    while memory.getMap() != 80:
        if memory.userControl():
            # Main events
            if checkpoint == 1:
                FFXC.set_neutral()
                memory.waitFrames(30 * 0.2)
                memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 2 and gameVars.csr():
                checkpoint = 11
            elif checkpoint == 4:  # Talking to Trommell
                memory.clickToEventTemple(6)
                if memory.getCoords()[0] < 23.5:
                    memory.waitFrames(30 * 0.07)
                    FFXC.set_movement(1, 0)
                    memory.waitFrames(2)
                    FFXC.set_neutral()
                    memory.waitFrames(4)
                checkpoint += 1
            elif checkpoint == 5:  # Skip (new)
                print("Lining up for skip.")
                FFXC.set_movement(0, -1)
                memory.waitFrames(30 * 0.2)
                FFXC.set_neutral()
                while memory.getCoords()[1] < -101.5:
                    FFXC.set_value('Dpad', 8)
                    memory.waitFrames(2)
                    FFXC.set_value('Dpad', 0)
                    memory.waitFrames(5)

                print("Turning back")
                memory.waitFrames(3)
                FFXC.set_movement(-1, 0)
                memory.waitFrames(2)
                FFXC.set_neutral()
                memory.waitFrames(15)

                print("Now lined up. Here we go.")
                FFXC.set_movement(1, 0)
                memory.waitFrames(3)
                FFXC.set_value('BtnB', 1)
                memory.waitFrames(4)
                FFXC.set_value('BtnB', 0)
                memory.waitFrames(45)
                FFXC.set_neutral()
                checkpoint += 1
                memory.clickToControl3()
            elif checkpoint == 6:
                checkpoint = 11
            elif checkpoint == 11:
                print("Check if skip is online")
                if gameVars.csr():
                    jyscalSkipStatus = True
                    checkpoint += 1
                elif memory.getStoryProgress() < 1505:
                    jyscalSkipStatus = True
                    checkpoint += 1
                else:
                    jyscalSkipStatus = False
                    checkpoint = 20
                    skipStatus = False
                print("Jyscal Skip results:", skipStatus)
            elif checkpoint == 14 and gameVars.csr():
                FFXC.set_movement(0, 1)
                memory.awaitEvent()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 14:  # Pause so we don't mess up the skip
                if skipStatus:
                    FFXC.set_neutral()
                    xbox.SkipDialog(5)
                    FFXC.set_movement(0, -1)
                    memory.awaitEvent()
                    FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint < 16 and memory.getMap() == 239:
                checkpoint = 16

            # Recovery items
            elif checkpoint == 23:  # Door, Jyscal room
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 24:  # Back to the main room
                memory.clickToEventTemple(5)
                checkpoint += 1
            elif checkpoint == 27:
                checkpoint = 12

            # General pathing
            elif targetPathing.setMovement(targetPathing.templeFoyer(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()
    return jyscalSkipStatus


def startSeymourFight():
    memory.clickToControl()
    while not targetPathing.setMovement([9, -53]):
        pass  # Allows us to move to the Seymour fight.
    FFXC.set_movement(1, 0)
    memory.awaitEvent()
    FFXC.set_neutral()


def seymourFight():
    battle.seymourGuado()

    # Name for Shiva
    xbox.nameAeon("Shiva")

    memory.awaitControl()
    FFXC.set_movement(-1, -1)
    memory.waitFrames(30 * 0.4)
    FFXC.set_movement(-1, 0)
    memory.awaitEvent()
    FFXC.set_neutral()


def trials():
    memory.awaitControl()

    checkpoint = 0
    while memory.getMap() != 153:
        if memory.userControl():
            # CSR start point
            if checkpoint < 3 and gameVars.csr():
                checkpoint = 3

            # Map changes
            elif checkpoint < 2 and memory.getMap() == 239:
                checkpoint = 2

            # Spheres and Pedestals
            elif checkpoint == 2:
                memory.awaitControl()
                print("Activate the trials")
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 9:  # Push pedestal - 1
                FFXC.set_movement(1, 0)
                memory.awaitEvent()
                FFXC.set_neutral()
                memory.waitFrames(30 * 1)
                checkpoint += 1
            elif checkpoint == 13:  # Grab first Mac Sphere
                memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 17:  # Place first Mac Sphere
                memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 20:  # Push pedestal - 2
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 23:  # Grab glyph sphere
                memory.clickToEventTemple(2)
                checkpoint += 1
                print("Checkpoint:", checkpoint)
            elif checkpoint == 29:  # Push pedestal - 3
                FFXC.set_movement(1, 0)
                memory.awaitEvent()
                FFXC.set_neutral()
                memory.waitFrames(30 * 1)
                checkpoint += 1
            elif checkpoint == 32:  # Place Glyph sphere
                memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 39:  # Grab second Mac sphere
                memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 46:  # Place second Mac sphere
                memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 51:  # Grab third Mac sphere
                memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 53:  # Place third Mac sphere
                memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 58:  # End of trials
                memory.clickToEventTemple(0)
                memory.awaitControl()
                # Just to start the next set of dialog.
                memory.clickToEventTemple(4)

            # General pathing
            elif targetPathing.setMovement(targetPathing.mTempleTrials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()


def escape():
    memory.clickToControl()
    print("First, some menuing")
    menuDone = False
    if gameVars.nemesis():
        memory.fullPartyFormat('yuna', fullMenuClose=False)
    else:
        menu.afterSeymour()
        menuDone = True
        memory.fullPartyFormat('macalaniaescape', fullMenuClose=False)
    menu.equipSonicSteel(fullMenuClose=True)

    print("Now to escape the Guado")
    forceBattle = False

    checkpoint = 0
    while memory.getEncounterID() != 195:
        if memory.userControl():
            # Events
            if checkpoint == 2:
                memory.touchSaveSphere()
                checkpoint += 1
                print("Touching save sphere. Update checkpoint:", checkpoint)
            elif checkpoint == 18 and forceBattle:
                FFXC.set_neutral()

            # Map changes
            elif checkpoint < 19 and memory.getMap() == 192:
                checkpoint = 19
                print("Map change. Update checkpoint:", checkpoint)

            # General pathing
            elif targetPathing.setMovement(targetPathing.mTempleEscape(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.battleActive():
                screen.awaitTurn()
                if checkpoint < 19:
                    battle.fleeAll()
                    forceBattle = False
                elif not menuDone:
                    battle.escapeWithXP()
                    menu.afterSeymour()
                    menuDone = True
                    memory.fullPartyFormat('macalaniaescape')
                elif memory.getEncounterID() == 195:
                    break
                else:
                    battle.fleeAll()
            elif memory.menuOpen():
                xbox.tapB()
            elif memory.diagSkipPossible():
                xbox.tapB()

    print("Done pathing. Now for the Wendigo fight.")
    battle.wendigo()
    print("Wendigo fight over")


def underLake():
    memory.clickToControl()
    checkpoint = 0
    while memory.getMap() != 129:
        if memory.userControl():
            if checkpoint == 4:
                FFXC.set_movement(0, 1)
                memory.clickToEvent()
                FFXC.set_neutral()
                memory.clickToControl()
                FFXC.set_movement(0, 1)
                memory.waitFrames(2)
                memory.clickToEvent()
                FFXC.set_neutral()
                memory.clickToControl()
                checkpoint += 1
            elif checkpoint == 11:
                memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 15:
                while memory.userControl():
                    targetPathing.setMovement([-4, -8])
                    xbox.tapB()
                FFXC.set_neutral()
                memory.clickToControl3()
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.underMacTemple(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()
    FFXC.set_neutral()
    memory.clickToControl()


def underLake_old():
    memory.clickToControl()
    FFXC.set_movement(0, 1)
    memory.waitFrames(30 * 1)
    FFXC.set_movement(-1, 1)
    memory.waitFrames(30 * 0.8)
    FFXC.set_movement(1, 1)
    memory.waitFrames(30 * 1)
    FFXC.set_movement(0, 1)
    memory.clickToEvent()
    FFXC.set_neutral()

    memory.clickToControl()
    FFXC.set_movement(0, 1)
    memory.waitFrames(30 * 1.5)  # Approach Yuna
    FFXC.set_neutral()

    memory.clickToControl()
    while memory.getCoords()[1] > 110:
        FFXC.set_movement(-1, 1)
    while memory.getCoords()[1] > 85:
        FFXC.set_movement(1, 1)
    while memory.getCoords()[0] > -30:
        if memory.getCoords()[1] < 110:
            FFXC.set_movement(1, -1)
        else:
            FFXC.set_movement(1, 0)
    FFXC.set_movement(1, 0)
    memory.clickToEvent()  # Chest with Lv.2 Key Sphere
    FFXC.set_neutral()
    xbox.SkipDialog(0.2)
    memory.clickToControl()
    FFXC.set_movement(-1, 0)
    memory.waitFrames(30 * 0.25)
    while memory.getCoords()[0] < -5:
        FFXC.set_movement(-1, 1)
    FFXC.set_movement(0, 1)
    memory.waitFrames(30 * 1)  # To Auron
    xbox.SkipDialog(1.5)
    FFXC.set_movement(1, 0)
    xbox.SkipDialog(0.4)
    FFXC.set_movement(-1, 0)
    xbox.SkipDialog(0.4)
    FFXC.set_neutral()
    memory.clickToControl()

    while memory.getMap() != 129:
        FFXC.set_movement(0, -1)
        if memory.diagSkipPossible():
            xbox.tapB()
        elif memory.cutsceneSkipPossible():
            xbox.skipScene()
    FFXC.set_neutral()
    memory.clickToControl()
