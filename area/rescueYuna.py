import xbox
import screen
import battle.main
import menu
import memory.main
import targetPathing
import zzairShipPath
import vars
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def preEvrae():
    FFXC.set_neutral()
    memory.main.clickToControl()
    print("Starting first Airship section")
    checkpoint = 0
    while checkpoint < 19:
        if memory.main.userControl():
            if checkpoint < 4 and memory.main.getMap() == 265:
                memory.main.awaitControl()
                memory.main.clickToEventTemple(7)
                checkpoint = 4
            elif checkpoint == 9:
                memory.main.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 13:
                memory.main.touchSaveSphere()
                memory.main.fullPartyFormat('evrae')
                checkpoint += 1
            elif checkpoint == 18:
                memory.main.clickToEventTemple(4)
                checkpoint += 1

            elif targetPathing.setMovement(targetPathing.rescueAirship(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()

    zzairShipPath.airShipPath(1)


def guards():
    print("Start, Guards")
    memory.main.clickToControl()

    if not gameVars.getBlitzWin():
        menu.equipSonicSteel(fullMenuClose=False)

    sleepingPowders = memory.main.getItemSlot(37) != 255
    if not sleepingPowders:
        if memory.main.getLuluSlvl() < 35:
            memory.main.fullPartyFormat('guards_lulu', fullMenuClose=False)
        else:
            memory.main.fullPartyFormat('guards_no_lulu', fullMenuClose=False)
    if memory.main.getItemSlot(3) < 200 and memory.main.getHP() != memory.main.getMaxHP():
        menu.beforeGuards()
    memory.main.closeMenu()
    memory.main.waitFrames(2)

    guardNum = 1
    while memory.main.getMap() != 182:
        if memory.main.userControl():
            if memory.main.getMap() == 180:
                memory.main.clickToEventTemple(6)  # Take the spiral lift down
            elif memory.main.getMap() == 181:
                while not targetPathing.setMovement([-110, 0]):
                    pass
                memory.main.clickToEventTemple(0)  # Through the water door
            else:
                targetPathing.setMovement([0, -200])
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                battle.main.guards(guardNum, sleepingPowders)
                if guardNum == 2:
                    memory.main.clickToControl()
                    memory.main.fullPartyFormat('guards_lulu')
                elif guardNum == 5:
                    pass
                else:
                    memory.main.clickToControl()
                    memory.main.fullPartyFormat('guards_no_lulu')
                guardNum += 1
            elif memory.main.menuOpen():
                xbox.tapB()
            elif memory.main.cutsceneSkipPossible():
                if memory.main.diagProgressFlag() == 12:
                    xbox.tapX()
                else:
                    xbox.skipScene()
            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()
    print("-------End of Bevelle guards")

    checkpoint = 0
    while checkpoint < 8:
        if memory.main.userControl():
            # Map changes
            if checkpoint < 2 and memory.main.getMap() == 182:
                checkpoint = 2
            # General pathing
            elif targetPathing.setMovement(targetPathing.bevellePreTrials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()

            # Map changes
            elif checkpoint < 2 and memory.main.getMap() == 182:
                checkpoint = 2


def trials():
    print("Starting Bevelle trials section.")

    checkpoint = 0
    while checkpoint < 53:
        if memory.main.userControl():
            # Map changes
            if checkpoint < 2 and memory.main.getMap() == 306:
                checkpoint = 2

            # Spheres, Pedestals, and gliding across glowing paths.
            elif checkpoint == 3:  # Pedestal that starts it all.
                FFXC.set_movement(0, 1)
                memory.main.awaitEvent()  # Pedestal - START!!!
                FFXC.set_neutral()

                while not memory.main.userControl():
                    if memory.main.getActorCoords(0)[1] < -100:
                        if memory.main.btBiDirection() == 1:
                            FFXC.set_value('BtnB', 1)
                        else:
                            FFXC.set_value('BtnB', 0)
                    elif memory.main.getActorCoords(0)[1] > 30 and memory.main.getActorCoords(0)[1] < 90:
                        FFXC.set_value('BtnB', 1)
                    else:
                        FFXC.set_value('BtnB', 0)
                FFXC.set_neutral()
                if memory.main.getActorCoords(0)[0] < -20:
                    print("Correct alcove. Moving on with swiftness.")
                    checkpoint += 2
                else:
                    print("Incorrect alcove. Recovering.")
                    checkpoint += 1
            elif checkpoint == 4:  # Recovery
                FFXC.set_movement(1, 0)
                memory.main.waitFrames(30 * 1.5)
                FFXC.set_movement(-1, 0)
                memory.main.waitFrames(30 * 1.5)
                FFXC.set_neutral()
                memory.main.waitFrames(30 * 10.5)

                xbox.SkipDialog(2)
                memory.main.waitFrames(30 * 3)
                cam = memory.main.getCamera()
                while cam[2] < -69:
                    cam = memory.main.getCamera()
                xbox.SkipDialog(2)
                memory.main.awaitControl()
                if memory.main.getCoords()[0] < -10:
                    print("Correct alcove. Moving on with swiftness.")
                    checkpoint += 1
                else:
                    print("Incorrect alcove. Recovering.")
            elif checkpoint == 7:  # First Bevelle sphere, and then more gliding.
                print("Bevelle sphere")
                memory.main.clickToEventTemple(7)
                while memory.main.getActorCoords(0)[0] < -25:
                    FFXC.set_movement(0, -1)
                    if not memory.main.userControl():
                        xbox.menuB()
                FFXC.set_neutral()
                print("Mark 1")
                memory.main.waitFrames(30 * 1)
                FFXC.set_value('BtnB', 1)
                print("Mark 2")
                memory.main.awaitControl()
                print("Mark 3")
                FFXC.set_value('BtnB', 0)
                checkpoint += 1
            elif checkpoint == 10:  # Insert Bevelle sphere. Activate lower areas.
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 13:  # Down to the lower areas.
                FFXC.set_neutral()
                memory.main.waitFrames(2)
                FFXC.set_movement(-1, 0)
                memory.main.waitFrames(30 * 2)
                FFXC.set_neutral()

                while not memory.main.userControl():
                    if memory.main.getActorCoords(0)[0] < 40:
                        if memory.main.getActorCoords(0)[1] > 100 or memory.main.getActorCoords(0)[1] < 10:
                            FFXC.set_value('BtnB', 1)
                        else:
                            FFXC.set_value('BtnB', 0)

                    elif memory.main.getActorCoords(0)[1] < -10:
                        if memory.main.btBiDirection() == 1 and memory.main.btTriDirectionMain() == 0:
                            memory.main.waitFrames(2)
                            if memory.main.btBiDirection() == 1 and memory.main.btTriDirectionMain() == 0:
                                xbox.menuB()
                                memory.main.waitFrames(20)
                    else:
                        if memory.main.getActorCoords(0)[1] > 293 and memory.main.getActorCoords(0)[1] < 432:
                            FFXC.set_value('BtnB', 1)
                        else:
                            FFXC.set_value('BtnB', 0)
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 16:  # Take Glyph sphere from second alcove
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 18:  # To third alcove
                FFXC.set_movement(1, -1)
                memory.main.waitFrames(30 * 2)
                FFXC.set_neutral()
                memory.main.waitFrames(30 * 2)
                while not memory.main.userControl():
                    if memory.main.getActorCoords(0)[0] < 40:
                        if memory.main.getActorCoords(0)[1] > 100 or memory.main.getActorCoords(0)[1] < 10:
                            FFXC.set_value('BtnB', 1)
                        else:
                            FFXC.set_value('BtnB', 0)

                    elif memory.main.getActorCoords(0)[1] > 425:
                        FFXC.set_value('BtnB', 1)
                    elif memory.main.getActorCoords(0)[1] < -30 and \
                            memory.main.btBiDirection() == 0 and memory.main.btTriDirectionMain() == 0:
                        memory.main.waitFrames(2)
                        if memory.main.btBiDirection() == 0 and memory.main.btTriDirectionMain() == 0:
                            xbox.menuB()
                            memory.main.waitFrames(20)
                    else:
                        FFXC.set_value('BtnB', 0)
                # Go ahead and insert Glyph sphere.
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 22:  # Remove Bevelle sphere
                memory.main.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 24:  # Insert Bevelle sphere
                memory.main.clickToEventTemple(5)
                checkpoint += 1
            elif checkpoint == 28:  # Take Glyph sphere
                FFXC.set_neutral()
                memory.main.waitFrames(30 * 0.07)
                memory.main.clickToEvent()
                memory.main.waitFrames(30 * 0.035)
                memory.main.clickToControl3()
                checkpoint += 1
            elif checkpoint == 32:  # Insert Glyph sphere
                while memory.main.userControl():
                    targetPathing.setMovement([450, 525])
                    xbox.tapB()
                FFXC.set_neutral()
                memory.main.clickToControl3()
                checkpoint += 1
            elif checkpoint == 34:  # Take Destro sphere
                memory.main.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 37:  # Insert Destro sphere
                FFXC.set_neutral()
                memory.main.waitFrames(30 * 0.1)
                FFXC.set_movement(0, 1)
                memory.main.waitFrames(30 * 0.07)
                FFXC.set_neutral()
                xbox.SkipDialog(1)
                memory.main.clickToControl3()
                checkpoint += 1
            elif checkpoint == 39:  # Take Bevelle sphere
                memory.main.clickToEventTemple(5)
                checkpoint += 1
            elif checkpoint == 41:  # back on the track.
                FFXC.set_movement(0, -1)
                memory.main.waitFrames(30 * 3)
                FFXC.set_neutral()

                memory.main.waitFrames(30 * 10)
                while not memory.main.userControl():
                    if memory.main.getActorCoords(0)[0] < 40:
                        if memory.main.getActorCoords(0)[1] > 100 or memory.main.getActorCoords(0)[1] < 10:
                            FFXC.set_value('BtnB', 1)
                        else:
                            FFXC.set_value('BtnB', 0)

                    elif memory.main.getActorCoords(0)[1] < -30:
                        if memory.main.btBiDirection() == 1 and memory.main.btTriDirectionMain() == 0:
                            memory.main.waitFrames(2)
                            if memory.main.btBiDirection() == 1 and memory.main.btTriDirectionMain() == 0:
                                xbox.menuB()
                                memory.main.waitFrames(20)
                    elif memory.main.getActorCoords(0)[1] > 250 and memory.main.getActorCoords(0)[1] < 450:
                        FFXC.set_value('BtnB', 1)
                    else:
                        FFXC.set_value('BtnB', 0)
                FFXC.set_neutral()
                print("Arriving in the second alcove again.")
                checkpoint += 1
            elif checkpoint == 43:  # Place Bevelle sphere (second alcove)
                memory.main.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 47:  # Take Destro sphere
                FFXC.set_movement(1, -1)
                memory.main.waitFrames(30 * 0.1)
                FFXC.set_neutral()
                xbox.SkipDialog(1)
                memory.main.clickToControl3()
                checkpoint += 1
            elif checkpoint == 50:  # Insert Destro sphere
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 52:  # Back on track, to the exit
                FFXC.set_movement(1, -1)
                memory.main.waitFrames(30 * 2)
                FFXC.set_neutral()
                memory.main.waitFrames(30 * 19)
                while not memory.main.userControl():
                    if memory.main.getActorCoords(0)[0] < 40:
                        if memory.main.getActorCoords(0)[1] > 100 or memory.main.getActorCoords(0)[1] < 10:
                            FFXC.set_value('BtnB', 1)
                        else:
                            FFXC.set_value('BtnB', 0)

                    elif memory.main.getActorCoords(0)[1] < -30:
                        if memory.main.btBiDirection() == 0 and memory.main.btTriDirectionMain() == 0:
                            memory.main.waitFrames(2)
                            if memory.main.btBiDirection() == 0 and memory.main.btTriDirectionMain() == 0:
                                xbox.menuB()
                                memory.main.waitFrames(20)
                    else:
                        if memory.main.getActorCoords(0)[1] < 250:
                            FFXC.set_value('BtnB', 1)
                        else:
                            FFXC.set_value('BtnB', 0)
                FFXC.set_neutral()
                memory.main.awaitControl()
                FFXC.set_movement(0, -1)
                memory.main.waitFrames(30 * 2)
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 58:
                memory.main.clickToEventTemple(2)
                checkpoint += 1

            # General pathing
            elif targetPathing.setMovement(targetPathing.bevelleTrials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            if memory.main.diagSkipPossible():
                xbox.tapB()
            if checkpoint < 3:
                FFXC.set_neutral()

    FFXC.set_neutral()


def trialsEnd():
    checkpoint = 53
    while memory.main.getMap() != 226:
        if memory.main.userControl():
            if targetPathing.setMovement(targetPathing.bevelleTrials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        elif memory.main.diagSkipPossible():
            xbox.tapB()
        elif checkpoint == 58:
            memory.main.clickToEventTemple(2)
            checkpoint += 1
        else:
            FFXC.set_neutral()

    FFXC.set_neutral()

    # Name for Bahamut
    xbox.nameAeon("Bahamut")
    if not gameVars.csr():
        xbox.awaitSave(index=29)


def ViaPurifico():
    memory.main.clickToControl()
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 3)
    FFXC.set_movement(1, 1)
    memory.main.waitFrames(30 * 0.15)
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 5)
    FFXC.set_neutral()

    if not gameVars.csr():
        memory.main.waitFrames(30 * 5.7)  # Wait for the right direction
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 2)
    FFXC.set_neutral()

    memory.main.clickToControl()
    menu.viaPurifico()

    while memory.main.getMap() != 209:  # Map number for Altana
        if memory.main.userControl():
            if memory.main.getSLVLYuna() < 15 and memory.main.getCoords()[1] > 1460:
                FFXC.set_movement(0, -1)
                memory.main.waitFrames(30 * 2)
            else:
                FFXC.set_movement(0, 1)
        elif screen.BattleScreen():
            battle.main.isaaru()
        else:
            FFXC.set_neutral()
            xbox.tapB()


def evraeAltana():
    memory.main.clickToControl()
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(30 * 2)
    FFXC.set_neutral()

    checkpoint = 0
    lastCP = 0
    while checkpoint < 100:
        if lastCP != checkpoint:
            print("Checkpoint reached:", checkpoint)
            lastCP = checkpoint
        if memory.main.getStoryProgress() > 2220:
            print("End of Evrae Altana section.")
            FFXC.set_neutral()
            checkpoint = 100
        if memory.main.userControl():
            pos = memory.main.getCoords()
            cam = memory.main.getCamera()
            if checkpoint == 0:
                if pos[1] > -1550 and cam[0] > 0.5:
                    checkpoint = 10
                else:
                    FFXC.set_movement(0, 1)
            elif checkpoint == 10:
                if pos[1] > -1490:
                    checkpoint = 20
                else:
                    FFXC.set_movement(1, 0)
            elif checkpoint == 20:
                if pos[0] < 1050:
                    checkpoint = 30
                if pos[1] < -1470:
                    FFXC.set_movement(1, 1)
                elif pos[1] > -1365:
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(0, 1)
            elif checkpoint == 30:
                if pos[0] < 625:
                    checkpoint = 40
                if pos[1] < -1410:
                    FFXC.set_movement(1, 1)
                elif pos[1] > -1377:
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(0, 1)

            elif checkpoint == 40:  # Diagonal with swinging camera
                if pos[1] > -540:
                    checkpoint = 50
                if pos[1] < ((-9.83 * pos[0]) + 4840):
                    FFXC.set_movement(1, 1)
                else:
                    FFXC.set_movement(0, 1)
            elif checkpoint == 50:
                if pos[1] > -310:
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_movement(0, 1)
        elif screen.BattleScreen():
            battle.main.evraeAltana()
            memory.main.printManipInfo()
        elif screen.BattleComplete():
            xbox.menuB()
        else:
            FFXC.set_neutral()
            if checkpoint == 50:
                xbox.tapB()
    return 0


def seymourNatus():
    memory.main.clickToControl()

    if gameVars.getBlitzWin():
        menu.seymourNatusBlitzWin()
    else:
        menu.seymourNatusBlitzLoss()

    memory.main.fullPartyFormat('highbridge')
    memory.main.touchSaveSphere()
    complete = 0
    while complete == 0:
        if memory.main.userControl():
            targetPathing.setMovement([2, memory.main.getCoords()[1] - 50])
        else:
            FFXC.set_neutral()
            if screen.BattleScreen():
                print("Battle Start")
                if memory.main.battleType() == 2:
                    battle.main.fleeAll()
                else:
                    complete = battle.main.seymourNatus()
                    memory.main.printManipInfo()

    # Movement for make-out scene
    memory.main.clickToControl()

    checkpoint = 0
    while checkpoint < 13:
        if memory.main.userControl():
            # Events and map changes
            if checkpoint == 1 or checkpoint == 3:
                memory.main.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 5:
                print("Checkpoint 5")
                FFXC.set_movement(-1, 0)
                memory.main.awaitEvent()
                FFXC.set_neutral()
                memory.main.waitFrames(3)
                checkpoint += 1
            elif checkpoint == 6:
                print("Checkpoint 6")
                if not gameVars.csr():
                    memory.main.clickToEventTemple(3)
                checkpoint += 1
            elif checkpoint == 8:
                print("Checkpoint 8")
                memory.main.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 12:
                print("Checkpoint 12")
                memory.main.clickToEventTemple(0)
                checkpoint += 1

            elif targetPathing.setMovement(targetPathing.sutekiDaNe(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()
            elif memory.main.cutsceneSkipPossible():
                xbox.skipScene()
