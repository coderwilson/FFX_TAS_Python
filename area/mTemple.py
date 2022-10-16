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


def approach(doGrid=True):
    print("------------------------------Affection array:")
    print(memory.main.affectionArray())
    print("------------------------------")
    memory.main.clickToControl()
    print("Approaching Macalania Temple")

    checkpoint = 0
    while memory.main.getMap() != 106:
        if memory.main.userControl():
            # Map changes
            if checkpoint < 2 and memory.main.getMap() == 153:
                checkpoint = 2

            # General pathing
            elif targetPathing.setMovement(targetPathing.mTempleApproach(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()
    FFXC.set_neutral()
    memory.main.awaitControl()
    if doGrid:
        menu.macTemple()
    memory.main.touchSaveSphere()


def arrival():
    print("Starting Macalania Temple section")

    # Movement:
    jyscalSkipStatus = False
    checkpoint = 0
    skipStatus = True
    while memory.main.getMap() != 80:
        if memory.main.userControl():
            # Main events
            if checkpoint == 1:
                #FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 2 and gameVars.csr():
                checkpoint = 11
            elif checkpoint == 4:  # Talking to Trommell
                memory.main.clickToEventTemple(6)
                if memory.main.getCoords()[0] < 23.5:
                    memory.main.waitFrames(30 * 0.07)
                    FFXC.set_movement(1, 0)
                    memory.main.waitFrames(2)
                    FFXC.set_neutral()
                    memory.main.waitFrames(4)
                checkpoint += 1
            elif checkpoint == 5:  # Skip (new)
                print("Lining up for skip.")
                FFXC.set_movement(0, -1)
                memory.main.waitFrames(30 * 0.2)
                FFXC.set_neutral()
                while memory.main.getCoords()[1] < -101.5:
                    FFXC.set_value('Dpad', 8)
                    memory.main.waitFrames(2)
                    FFXC.set_value('Dpad', 0)
                    memory.main.waitFrames(5)

                print("Turning back")
                memory.main.waitFrames(3)
                FFXC.set_movement(-1, 0)
                memory.main.waitFrames(2)
                FFXC.set_neutral()
                memory.main.waitFrames(15)

                print("Now lined up. Here we go.")
                FFXC.set_movement(1, 0)
                memory.main.waitFrames(3)
                FFXC.set_value('BtnB', 1)
                memory.main.waitFrames(4)
                FFXC.set_value('BtnB', 0)
                memory.main.waitFrames(45)
                FFXC.set_neutral()
                checkpoint += 1
                memory.main.clickToControl3()
            elif checkpoint == 6:
                checkpoint = 11
            elif checkpoint == 11:
                print("Check if skip is online")
                if gameVars.csr():
                    jyscalSkipStatus = True
                    checkpoint += 1
                elif memory.main.getStoryProgress() < 1505:
                    jyscalSkipStatus = True
                    checkpoint += 1
                else:
                    jyscalSkipStatus = False
                    checkpoint = 20
                    skipStatus = False
                print("Jyscal Skip results:", skipStatus)
            elif checkpoint == 14 and gameVars.csr():
                FFXC.set_movement(0, 1)
                memory.main.awaitEvent()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 14:  # Pause so we don't mess up the skip
                if skipStatus:
                    FFXC.set_neutral()
                    xbox.SkipDialog(5)
                    FFXC.set_movement(0, -1)
                    memory.main.awaitEvent()
                    FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint < 16 and memory.main.getMap() == 239:
                checkpoint = 16

            # Recovery items
            elif checkpoint == 23:  # Door, Jyscal room
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 24:  # Back to the main room
                memory.main.clickToEventTemple(5)
                checkpoint += 1
            elif checkpoint == 27:
                checkpoint = 12

            # General pathing
            elif targetPathing.setMovement(targetPathing.templeFoyer(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()
    return jyscalSkipStatus


def startSeymourFight():
    memory.main.clickToControl()
    while not targetPathing.setMovement([9, -53]):
        pass  # Allows us to move to the Seymour fight.
    FFXC.set_movement(1, 0)
    memory.main.awaitEvent()
    FFXC.set_neutral()


def seymourFight():
    battle.main.seymourGuado()

    # Name for Shiva
    xbox.nameAeon("Shiva")

    memory.main.awaitControl()
    FFXC.set_movement(-1, -1)
    memory.main.waitFrames(30 * 0.4)
    FFXC.set_movement(-1, 0)
    memory.main.awaitEvent()
    FFXC.set_neutral()


def trials():
    memory.main.awaitControl()

    checkpoint = 0
    while memory.main.getMap() != 153:
        if memory.main.userControl():
            # CSR start point
            if checkpoint < 3 and gameVars.csr():
                checkpoint = 3

            # Map changes
            elif checkpoint < 2 and memory.main.getMap() == 239:
                checkpoint = 2

            # Spheres and Pedestals
            elif checkpoint == 2:
                memory.main.awaitControl()
                print("Activate the trials")
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 9:  # Push pedestal - 1
                FFXC.set_movement(1, 0)
                memory.main.awaitEvent()
                FFXC.set_neutral()
                memory.main.waitFrames(30 * 1)
                checkpoint += 1
            elif checkpoint == 13:  # Grab first Mac Sphere
                memory.main.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 17:  # Place first Mac Sphere
                memory.main.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 20:  # Push pedestal - 2
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 23:  # Grab glyph sphere
                memory.main.clickToEventTemple(2)
                checkpoint += 1
                print("Checkpoint:", checkpoint)
            elif checkpoint == 29:  # Push pedestal - 3
                FFXC.set_movement(1, 0)
                memory.main.awaitEvent()
                FFXC.set_neutral()
                memory.main.waitFrames(30 * 1)
                checkpoint += 1
            elif checkpoint == 32:  # Place Glyph sphere
                memory.main.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 39:  # Grab second Mac sphere
                memory.main.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 46:  # Place second Mac sphere
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 51:  # Grab third Mac sphere
                memory.main.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 53:  # Place third Mac sphere
                memory.main.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 58:  # End of trials
                memory.main.clickToEventTemple(0)
                memory.main.awaitControl()
                # Just to start the next set of dialog.
                memory.main.clickToEventTemple(4)

            # General pathing
            elif targetPathing.setMovement(targetPathing.mTempleTrials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()


def escape():
    memory.main.clickToControl()
    print("First, some menuing")
    menuDone = False
    if gameVars.nemesis():
        memory.main.fullPartyFormat('yuna', fullMenuClose=False)
    else:
        menu.afterSeymour()
        menuDone = True
        memory.main.fullPartyFormat('macalaniaescape', fullMenuClose=False)
    menu.equipSonicSteel(fullMenuClose=True)

    print("Now to escape the Guado")
    forceBattle = False

    checkpoint = 0
    while memory.main.getEncounterID() != 195:
        if memory.main.userControl():
            # Events
            if checkpoint == 2:
                memory.main.touchSaveSphere()
                checkpoint += 1
                print("Touching save sphere. Update checkpoint:", checkpoint)
            elif checkpoint == 18 and forceBattle:
                FFXC.set_neutral()

            # Map changes
            elif checkpoint < 19 and memory.main.getMap() == 192:
                checkpoint = 19
                print("Map change. Update checkpoint:", checkpoint)

            # General pathing
            elif targetPathing.setMovement(targetPathing.mTempleEscape(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                screen.awaitTurn()
                if checkpoint < 19:
                    battle.main.fleeAll()
                    forceBattle = False
                elif not menuDone:
                    battle.main.escapeWithXP()
                    menu.afterSeymour()
                    menuDone = True
                    memory.main.fullPartyFormat('macalaniaescape')
                elif memory.main.getEncounterID() == 195:
                    break
                else:
                    battle.main.fleeAll()
            elif memory.main.menuOpen():
                xbox.tapB()
            elif memory.main.diagSkipPossible():
                xbox.tapB()

    print("Done pathing. Now for the Wendigo fight.")
    battle.boss.wendigo()
    print("Wendigo fight over")


def underLake():
    memory.main.clickToControl()
    checkpoint = 0
    while memory.main.getMap() != 129:
        if memory.main.userControl():
            if checkpoint == 4:
                FFXC.set_movement(0, 1)
                memory.main.clickToEvent()
                FFXC.set_neutral()
                memory.main.clickToControl()
                FFXC.set_movement(0, 1)
                memory.main.waitFrames(2)
                memory.main.clickToEvent()
                FFXC.set_neutral()
                memory.main.clickToControl()
                checkpoint += 1
            elif checkpoint == 11:
                memory.main.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 15:
                while memory.main.userControl():
                    targetPathing.setMovement([-4, -8])
                    xbox.tapB()
                FFXC.set_neutral()
                memory.main.clickToControl3()
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.underMacTemple(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()
    FFXC.set_neutral()
    memory.main.clickToControl()


def underLake_old():
    memory.main.clickToControl()
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 1)
    FFXC.set_movement(-1, 1)
    memory.main.waitFrames(30 * 0.8)
    FFXC.set_movement(1, 1)
    memory.main.waitFrames(30 * 1)
    FFXC.set_movement(0, 1)
    memory.main.clickToEvent()
    FFXC.set_neutral()

    memory.main.clickToControl()
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 1.5)  # Approach Yuna
    FFXC.set_neutral()

    memory.main.clickToControl()
    while memory.main.getCoords()[1] > 110:
        FFXC.set_movement(-1, 1)
    while memory.main.getCoords()[1] > 85:
        FFXC.set_movement(1, 1)
    while memory.main.getCoords()[0] > -30:
        if memory.main.getCoords()[1] < 110:
            FFXC.set_movement(1, -1)
        else:
            FFXC.set_movement(1, 0)
    FFXC.set_movement(1, 0)
    memory.main.clickToEvent()  # Chest with Lv.2 Key Sphere
    FFXC.set_neutral()
    xbox.SkipDialog(0.2)
    memory.main.clickToControl()
    FFXC.set_movement(-1, 0)
    memory.main.waitFrames(30 * 0.25)
    while memory.main.getCoords()[0] < -5:
        FFXC.set_movement(-1, 1)
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 1)  # To Auron
    xbox.SkipDialog(1.5)
    FFXC.set_movement(1, 0)
    xbox.SkipDialog(0.4)
    FFXC.set_movement(-1, 0)
    xbox.SkipDialog(0.4)
    FFXC.set_neutral()
    memory.main.clickToControl()

    while memory.main.getMap() != 129:
        FFXC.set_movement(0, -1)
        if memory.main.diagSkipPossible():
            xbox.tapB()
        elif memory.main.cutsceneSkipPossible():
            xbox.skipScene()
    FFXC.set_neutral()
    memory.main.clickToControl()
