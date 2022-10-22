import battle.boss
import battle.main
import memory.main
import menu
import targetPathing
import vars
import xbox
import zz_eggHuntAuto
import zzairShipPath

gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def makingPlans():
    memory.main.clickToControl3()
    print("Final Push! Let's get this show on the road!!! (Highbridge)")

    # Start by touching the save sphere
    while not targetPathing.set_movement([-267, 347]):
        pass

    target = [[-242, 312], [-239, 258], [-243, 145], [-243, 10]]
    checkpoint = 0
    while memory.main.getMap() == 194:
        if memory.main.userControl():
            if targetPathing.set_movement(target[checkpoint]):
                checkpoint += 1

    zzairShipPath.airShipPath(2)  # Talk to Yuna/Kimahri
    FFXC.set_neutral()


def Shedinja():
    print("The hymn is the key")
    while memory.main.getMap() != 382:
        print("Mark 1")
        xbox.tapB()
    while not memory.main.diagProgressFlag() in [4, 255]:
        print("Mark 2")
        xbox.tapB()
    while memory.main.mapCursor() != 10:
        print("The destination is the key")
        memory.main.menuDirection(memory.main.mapCursor(), 10, 13)
    memory.main.clickToControl()

    memory.main.awaitControl()
    print("Moving to Shedinja")
    FFXC.set_movement(1, 1)
    memory.main.waitFrames(45)
    FFXC.set_movement(0, 1)
    memory.main.awaitEvent()

    FFXC.set_neutral()
    if not gameVars.csr():
        memory.main.clickToDiagProgress(100)
    memory.main.clickToDiagProgress(76)  # Have you found a way? Well?
    memory.main.waitFrames(20)
    xbox.tapDown()
    xbox.menuB()  # We fight Yu Yevon.

    memory.main.clickToDiagProgress(74)
    memory.main.clickToDiagProgress(28)
    memory.main.clickToControl3()


def exitCockpit():
    print("Attempting to exit cockpit")
    while memory.main.getMap() != 265:
        if memory.main.userControl():
            tidusCoords = memory.main.getCoords()
            if tidusCoords[1] > 318:
                targetPathing.set_movement([-244, 315])
            else:
                FFXC.set_movement(0, -1)
        else:
            FFXC.set_neutral()


def facingSin():
    while not targetPathing.set_movement([-245, 321]):
        pass

    while memory.main.userControl():
        targetPathing.set_movement([-256, 342])
        xbox.tapB()
        memory.main.waitFrames(1)

    FFXC.set_neutral()

    if gameVars.csr():
        memory.main.clickToControl()
    else:
        # Gets us through the Airship destination menu.
        xbox.SkipDialog(15)
        while not memory.main.userControl():
            if memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()
            elif memory.main.cutsceneSkipPossible():
                xbox.tapB()

    if memory.main.getMap() in [255, 374]:
        exitCockpit()
    FFXC.set_neutral()

    zzairShipPath.airShipPath(3)
    battle.main.SinArms()
    memory.main.clickToControl()
    print("To the deck, talk to Yuna")
    if memory.main.getMap() in [255, 374]:
        exitCockpit()
    FFXC.set_neutral()
    memory.main.clickToControl()

    zzairShipPath.airShipPath(4)
    FFXC.set_neutral()
    memory.main.clickToControl()

    print("To the deck, Sin's face battle.")
    if memory.main.getMap() in [255, 374]:
        exitCockpit()
    FFXC.set_neutral()
    zzairShipPath.airShipPath(5)
    battle.main.SinFace()
    print("End of battle with Sin's face.")


def insideSin():
    while memory.main.getMap() != 203:  # Skip dialog and run to the sea of sorrows map
        if memory.main.cutsceneSkipPossible():
            FFXC.set_neutral()
            memory.main.waitFrames(3)
            xbox.skipScene()
        else:
            FFXC.set_movement(0, -1)
            xbox.tapB()
    FFXC.set_neutral()

    if memory.main.overdriveState2()[6] != 100 and gameVars.getNEAzone() == 3:
        reEquipNE = True
        memory.main.fullPartyFormat("rikku", fullMenuClose=False)
        menu.equip_armor(character=gameVars.neArmor(), ability=99)
    else:
        reEquipNE = False
        memory.main.fullPartyFormat("yuna", fullMenuClose=False)
    memory.main.closeMenu()

    checkpoint = 0
    while memory.main.getMap() != 324:  # All the way to the egg hunt.
        if memory.main.userControl():
            # Events
            if memory.main.getMap() == 296:  # Seymour battle
                print("We've reached the Seymour screen.")
                memory.main.fullPartyFormat("yuna")
                FFXC.set_movement(0, 1)
                memory.main.waitFrames(30 * 5)
                FFXC.set_neutral()
                battle.boss.omnis()
                memory.main.clickToControl()
            elif checkpoint < 41 and memory.main.getMap() == 204:
                checkpoint = 41
            elif checkpoint < 68 and memory.main.getMap() == 327:
                checkpoint = 68

            # General Pathing
            elif targetPathing.set_movement(targetPathing.inside_sin(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive() and memory.main.turnReady():
                battle.main.chargeRikkuOD()
                if reEquipNE and memory.main.overdriveState2()[6] == 100:
                    reEquipNE = False
                    memory.main.clickToControl()
                    memory.main.fullPartyFormat("yuna", fullMenuClose=False)
                    menu.equip_armor(character=gameVars.neArmor(), ability=0x801D)
            elif memory.main.menuOpen():
                xbox.tapB()


def eggHunt(autoEggHunt):
    # Done with pathing, now for egg hunt.
    while not memory.main.userControl():
        FFXC.set_movement(-1, -1)
    memory.main.waitFrames(30 * 0.5)
    if autoEggHunt:
        zz_eggHuntAuto.engage()
    else:
        print("Start of egg hunt. User control expected.")
        waitCount = 0
        while memory.main.getMap() != 325:
            memory.main.waitFrames(30 * 1)
            waitCount += 1
            if waitCount % 10 == 0:
                print("Still waiting on user to do this section. ", waitCount / 10)
    print("Done with the egg hunt. Final prep for BFA.")
    if gameVars.nemesis():
        menu.equip_weapon(character=0, ability=0x8019, full_menu_close=True)
        FFXC.set_movement(1, 1)
        memory.main.waitFrames(5)
        memory.main.awaitEvent()
        FFXC.set_neutral()
    else:
        if gameVars.zombieWeapon() != 255 and gameVars.zombieWeapon() not in [0, 1, 2]:
            menu.equip_weapon(
                character=gameVars.zombieWeapon(), ability=0x8032, full_menu_close=False
            )
        menu.bfa()
