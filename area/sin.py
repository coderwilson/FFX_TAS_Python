import xbox
import battle
import menu
import memory
import zzairShipPath
import targetPathing
import zz_eggHuntAuto
import vars
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def makingPlans():
    memory.clickToControl3()
    print("Final Push! Let's get this show on the road!!! (Highbridge)")

    # Start by touching the save sphere
    while not targetPathing.setMovement([-267, 347]):
        pass

    target = [[-242, 312], [-239, 258], [-243, 145], [-243, 10]]
    checkpoint = 0
    while memory.getMap() == 194:
        if memory.userControl():
            if targetPathing.setMovement(target[checkpoint]):
                checkpoint += 1

    zzairShipPath.airShipPath(2)  # Talk to Yuna/Kimahri
    FFXC.set_neutral()


def Shedinja():
    print("The hymn is the key")
    while memory.getMap() != 382:
        print("Mark 1")
        xbox.tapB()
    while not memory.diagProgressFlag() in [4, 255]:
        print("Mark 2")
        xbox.tapB()
    while memory.mapCursor() != 10:
        print("The destination is the key")
        memory.menuDirection(memory.mapCursor(), 10, 13)
    memory.clickToControl()

    memory.awaitControl()
    print("Moving to Shedinja")
    FFXC.set_movement(1, 1)
    memory.waitFrames(45)
    FFXC.set_movement(0, 1)
    memory.awaitEvent()

    FFXC.set_neutral()
    if not gameVars.csr():
        memory.clickToDiagProgress(100)
    memory.clickToDiagProgress(76)  # Have you found a way? Well?
    memory.waitFrames(20)
    xbox.tapDown()
    xbox.menuB()  # We fight Yu Yevon.

    memory.clickToDiagProgress(74)
    memory.clickToDiagProgress(28)
    memory.clickToControl3()


def exitCockpit():
    print("Attempting to exit cockpit")
    while memory.getMap() != 265:
        if memory.userControl():
            tidusCoords = memory.getCoords()
            if tidusCoords[1] > 318:
                targetPathing.setMovement([-244, 315])
            else:
                FFXC.set_movement(0, -1)
        else:
            FFXC.set_neutral()


def facingSin():
    while not targetPathing.setMovement([-245, 321]):
        pass

    while memory.userControl():
        targetPathing.setMovement([-256, 342])
        xbox.tapB()
        memory.waitFrames(1)

    FFXC.set_neutral()

    if gameVars.csr():
        memory.clickToControl()
    else:
        # Gets us through the Airship destination menu.
        xbox.SkipDialog(15)
        while not memory.userControl():
            if memory.menuOpen() or memory.diagSkipPossible():
                xbox.tapB()
            elif memory.cutsceneSkipPossible():
                xbox.tapB()

    if memory.getMap() in [255, 374]:
        exitCockpit()
    FFXC.set_neutral()

    zzairShipPath.airShipPath(3)
    battle.SinArms()
    memory.clickToControl()
    print("To the deck, talk to Yuna")
    if memory.getMap() in [255, 374]:
        exitCockpit()
    FFXC.set_neutral()
    memory.clickToControl()

    zzairShipPath.airShipPath(4)
    FFXC.set_neutral()
    memory.clickToControl()

    print("To the deck, Sin's face battle.")
    if memory.getMap() in [255, 374]:
        exitCockpit()
    FFXC.set_neutral()
    zzairShipPath.airShipPath(5)
    battle.SinFace()
    print("End of battle with Sin's face.")


def insideSin():
    while memory.getMap() != 203:  # Skip dialog and run to the sea of sorrows map
        if memory.cutsceneSkipPossible():
            FFXC.set_neutral()
            memory.waitFrames(3)
            xbox.skipScene()
        else:
            FFXC.set_movement(0, -1)
            xbox.tapB()
    FFXC.set_neutral()

    if memory.overdriveState2()[6] != 100 and gameVars.getNEAzone() == 3:
        reEquipNE = True
        memory.fullPartyFormat('rikku', fullMenuClose=False)
        menu.equipArmor(character=gameVars.neArmor(), ability=99)
    else:
        reEquipNE = False
        memory.fullPartyFormat('yuna', fullMenuClose=False)
    memory.closeMenu()

    checkpoint = 0
    while memory.getMap() != 324:  # All the way to the egg hunt.
        if memory.userControl():
            # Events
            if memory.getMap() == 296:  # Seymour battle
                print("We've reached the Seymour screen.")
                memory.fullPartyFormat('yuna')
                FFXC.set_movement(0, 1)
                memory.waitFrames(30 * 5)
                FFXC.set_neutral()
                battle.omnis()
                memory.clickToControl()
            elif checkpoint < 41 and memory.getMap() == 204:
                checkpoint = 41
            elif checkpoint < 68 and memory.getMap() == 327:
                checkpoint = 68

            # General Pathing
            elif targetPathing.setMovement(targetPathing.insideSin(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.battleActive() and memory.turnReady():
                battle.chargeRikkuOD()
                if reEquipNE and memory.overdriveState2()[6] == 100:
                    reEquipNE = False
                    memory.clickToControl()
                    memory.fullPartyFormat('yuna', fullMenuClose=False)
                    menu.equipArmor(
                        character=gameVars.neArmor(), ability=0x801D)
            elif memory.menuOpen():
                xbox.tapB()


def eggHunt(autoEggHunt):
    # Done with pathing, now for egg hunt.
    while not memory.userControl():
        FFXC.set_movement(-1, -1)
    memory.waitFrames(30 * 0.5)
    if autoEggHunt:
        zz_eggHuntAuto.engage()
    else:
        print("Start of egg hunt. User control expected.")
        waitCount = 0
        while memory.getMap() != 325:
            memory.waitFrames(30 * 1)
            waitCount += 1
            if waitCount % 10 == 0:
                print("Still waiting on user to do this section. ", waitCount / 10)
    print("Done with the egg hunt. Final prep for BFA.")
    if gameVars.nemesis():
        menu.equipWeapon(character=0, ability=0x8019, fullMenuClose=True)
        FFXC.set_movement(1, 1)
        memory.waitFrames(5)
        memory.awaitEvent()
        FFXC.set_neutral()
    else:
        if gameVars.zombieWeapon() != 255 and gameVars.zombieWeapon() not in [0, 1, 2]:
            menu.equipWeapon(
                character=gameVars.zombieWeapon(), ability=0x8032, fullMenuClose=False)
        menu.BFA()
