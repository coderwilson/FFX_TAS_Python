import battle.main
import battle.overdrive
import memory.main
import nemesis.arenaSelect
import nemesis.menu
import nemesis.targetPath
import reset
import screen
import vars
import xbox

gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()

# The following functions extend the regular Bahamut run. Arena battles sections.


def saveGame(firstSave=False):
    while not nemesis.targetPath.setMovement([-6, -27]):
        pass
    while not nemesis.targetPath.setMovement([-2, -2]):
        pass
    print("Arena - Touch Save Sphere, and actually save")
    FFXC = xbox.controllerHandle()
    FFXC.set_neutral()
    ssDetails = memory.main.getSaveSphereDetails()

    if memory.main.userControl():
        while memory.main.userControl():
            nemesis.targetPath.setMovement([ssDetails[0], ssDetails[1]])
            xbox.tapB()
            memory.main.waitFrames(1)
    try:
        FFXC.set_neutral()
    except:
        FFXC = xbox.controllerHandle()
        FFXC.set_neutral()
    memory.main.waitFrames(30)
    xbox.tapB()
    memory.main.waitFrames(10)

    print("Controller is now neutral. Attemption to open save nemesis.menu.")
    while not memory.main.saveMenuOpen():
        pass
    print("Save menu is open.")
    memory.main.waitFrames(9)
    if not firstSave:
        xbox.menuDown()
        xbox.menuB()
        xbox.menuLeft()
    xbox.menuB()  # Select the save file
    xbox.menuB()  # Confirm the save
    memory.main.waitFrames(90)
    xbox.menuA()  # Back out
    xbox.menuA()  # Back out
    xbox.menuA()  # Back out
    xbox.menuA()  # Back out

    print("Menu now closed. Back to the battles.")
    memory.main.clearSaveMenuCursor()
    memory.main.clearSaveMenuCursor2()
    while not nemesis.targetPath.setMovement([-6, -27]):
        pass
    while not nemesis.targetPath.setMovement([2, -25]):
        pass


def touchSave(realSave=False):
    while not nemesis.targetPath.setMovement([-6, -27]):
        pass
    while not nemesis.targetPath.setMovement([-2, -2]):
        pass
    memory.main.touchSaveSphere()
    while not nemesis.targetPath.setMovement([-6, -27]):
        pass
    while not nemesis.targetPath.setMovement([2, -25]):
        pass
    arenaNPC()


def airShipDestination(destNum=0):  # Default to Sin.
    while memory.main.getMap() != 382:
        if memory.main.userControl():
            nemesis.targetPath.setMovement([-251, 340])
        else:
            FFXC.set_neutral()
        xbox.menuB()
    while memory.main.diagProgressFlag() != 4:
        xbox.menuB()
    print("Destination select on screen now.")
    while memory.main.mapCursor() != destNum:
        if destNum < 8:
            xbox.tapDown()
        else:
            xbox.tapUp()
    xbox.tapB()
    memory.main.waitFrames(2)
    xbox.tapB()
    memory.main.clickToControl3()


def getSaveSphereDetails():
    mapVal = memory.main.getMap()
    storyVal = memory.main.getStoryProgress()
    print("Map:", mapVal, "| Story:", storyVal)
    x = 0
    y = 0
    diag = 0
    if mapVal == 322:
        # Inside Sin, next to airship
        x = 225
        y = -250
        diag = 15
    if mapVal == 19:
        # Besaid beach
        x = -310
        y = -475
        diag = 55
    if mapVal == 263:
        # Thunder Plains agency
        x = -30
        y = -10
        diag = 114
    if mapVal == 307:
        # Monster Arena
        x = 4
        y = 5
        diag = 166
    if mapVal == 98:
        # Kilika docks
        x = 46
        y = -252
        diag = 34
    if mapVal == 92:
        # MRR start
        x = -1
        y = -740
        diag = 43
    if mapVal == 266:
        # Calm Lands Gorge
        x = -310
        y = 190
        diag = 43
    if mapVal == 82:
        # Djose temple
        x = 100
        y = -240
        diag = 89
    if mapVal == 221:
        # Macalania Woods, near Spherimorph
        x = 197
        y = -120
        diag = 23
    if mapVal == 137:
        # Bikanel Desert
        x = -15
        y = 240
        diag = 31
    if mapVal == 313:
        # Zanarkand campfire
        x = 135
        y = -1
        diag = 4
    if mapVal == 327:
        # Sin, end zone
        x = -37
        y = -508
        diag = 10
    if mapVal == 258:
        # Omega (only used in Nemesis)
        x = -112
        y = -1066
        diag = 23

    print("Values: [", x, ",", y, "] - ", diag)
    return [x, y, diag]


def returnToAirship():
    print("Attempting Return to Airship")

    ssDetails = getSaveSphereDetails()

    if memory.main.userControl():
        while memory.main.userControl():
            nemesis.targetPath.setMovement([ssDetails[0], ssDetails[1]])
            xbox.tapB()
            memory.main.waitFrames(1)
    try:
        FFXC.set_neutral()
    except:
        FFXC = xbox.controllerHandle()
        FFXC.set_neutral()
    FFXC.set_neutral()

    while not memory.main.getMap() in [194, 374]:
        if memory.main.getMap() == 307 and memory.main.getCoords()[1] < -5:
            while not nemesis.targetPath.setMovement([-4, -21]):
                pass
            while not nemesis.targetPath.setMovement([-2, -2]):
                pass
        else:
            FFXC.set_neutral()
            if memory.main.saveMenuOpen():
                xbox.tapA()
            elif memory.main.diagProgressFlag() == ssDetails[2]:
                # print("Cursor test:", memory.saveMenuCursor())
                if memory.main.saveMenuCursor() != 1:
                    xbox.menuDown()
                else:
                    xbox.menuB()
            elif memory.main.userControl():
                nemesis.targetPath.setMovement([ssDetails[0], ssDetails[1]])
                xbox.menuB()
            elif memory.main.diagSkipPossible():
                xbox.menuB()
            memory.main.waitFrames(4)
    print("Return to Airship Complete.")
    memory.main.clearSaveMenuCursor()
    memory.main.clearSaveMenuCursor2()


def aeonStart():
    screen.awaitTurn()
    battle.main.buddySwapYuna()
    battle.main.aeonSummon(4)
    while not screen.turnTidus():
        if memory.main.turnReady():
            if screen.turnAeon():
                battle.main.attack("none")
            else:
                battle.main.defend()


def yojimboBattle():
    # Incomplete
    screen.awaitTurn()
    if 1 not in memory.main.getActiveBattleFormation():
        battle.main.buddySwapYuna()
    print("+Yuna Overdrive to summon Yojimbo")
    battle.overdrive.yuna()
    print("+Pay the man")
    battle.overdrive.yojimbo()
    memory.main.waitFrames(90)
    while memory.main.battleActive():
        if memory.main.turnReady():
            if screen.turnTidus():
                battle.main.tidusFlee()
            elif screen.turnAeon():
                xbox.SkipDialog(2)
            else:
                battle.main.defend()

    # After battle stuff
    while not memory.main.menuOpen():
        xbox.tapB()
    print("Battle is complete.")
    FFXC.set_value("BtnB", 1)
    memory.main.waitFrames(180)
    FFXC.set_neutral()
    memory.main.waitFrames(2)

    return memory.main.battleArenaResults()


def autoLife():
    while not (memory.main.turnReady() and screen.turnTidus()):
        if memory.main.turnReady():
            if screen.turnAeon():
                battle.main.attack("none")
            elif not screen.turnTidus():
                battle.main.defend()
    while memory.main.battleMenuCursor() != 22:
        if not screen.turnTidus():
            print("Attempting Haste, but it's not Tidus's turn")
            xbox.tapUp()
            xbox.tapUp()
            return
        if memory.main.battleMenuCursor() == 1:
            xbox.tapUp()
        else:
            xbox.tapDown()
    while not memory.main.otherBattleMenu():
        xbox.tapB()
    battle.main._navigate_to_position(1)
    while memory.main.otherBattleMenu():
        xbox.tapB()
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()


def basicQuickAttacks(megaPhoenix=False, odVersion: int = 0, yunaAutos=False):
    print("### Battle Start:", memory.main.getEncounterID())
    FFXC.set_neutral()
    while memory.main.battleActive():
        if memory.main.turnReady():
            if screen.turnTidus():
                if megaPhoenix and screen.faintCheck() >= 2:
                    battle.main.revive(itemNum=7)
                elif memory.main.getOverdriveBattle(0) == 100:
                    battle.overdrive.tidus(version=odVersion)
                else:
                    battle.main.useSkill(1)  # Quick hit
            elif screen.turnAeon():
                battle.main.attack("none")
            else:
                battle.main.defend()

    # After battle stuff
    while not memory.main.menuOpen():
        xbox.tapB()
    FFXC.set_value("BtnB", 1)
    memory.main.waitFrames(150)
    FFXC.set_neutral()
    memory.main.waitFrames(2)
    return memory.main.battleArenaResults()


def basicAttack(megaPhoenix=False, odVersion: int = 0, useOD=False, yunaAutos=False):
    print("### Battle Start:", memory.main.getEncounterID())
    FFXC.set_neutral()
    while memory.main.battleActive():
        if memory.main.turnReady():
            if screen.turnTidus():
                if megaPhoenix and screen.faintCheck() >= 2:
                    battle.main.revive(itemNum=7)
                elif useOD and memory.main.getOverdriveBattle(0) == 100:
                    battle.overdrive.tidus(version=odVersion)
                else:
                    battle.main.attack("none")
            elif screen.turnYuna() and yunaAutos:
                battle.attack("none")
            elif screen.turnAeon():
                battle.attack("none")
            else:
                battle.main.defend()

    # After battle stuff
    while not memory.main.menuOpen():
        xbox.tapB()
    FFXC.set_value("BtnB", 1)
    memory.main.waitFrames(150)
    FFXC.set_neutral()
    memory.main.waitFrames(2)
    return memory.main.battleArenaResults()


def arenaNPC():
    if memory.main.getMap() != 307:
        return
    while not (memory.main.diagProgressFlag() == 74 and memory.main.diagSkipPossible()):
        if memory.main.userControl():
            if memory.main.getCoords()[1] > -15:
                print("Wrong position, moving away from sphere")
                while not nemesis.targetPath.setMovement([-6, -27]):
                    pass
                while not nemesis.targetPath.setMovement([2, -25]):
                    pass
            else:
                print("Engaging NPC")
                nemesis.targetPath.setMovement([5, -12])
                xbox.tapB()
        else:
            FFXC.set_neutral()
            if memory.main.diagProgressFlag() == 59:
                xbox.menuA()
                xbox.menuA()
                xbox.menuA()
                xbox.tapB()
            elif (
                memory.main.diagSkipPossible()
                and not memory.main.diagProgressFlag() == 74
            ):
                xbox.tapB()
    print("Mark 1")
    memory.main.waitFrames(30)  # This buffer can be improved later.
    print("Mark 2")


def restockDowns():
    print("Restocking phoenix downs")
    if memory.main.getItemCountSlot(memory.main.getItemSlot(6)) >= 80:
        print("Restock not needed. Disregard.")
        return
    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(3)
    memory.main.waitFrames(60)
    xbox.tapB()
    memory.main.waitFrames(6)
    while memory.main.equipBuyRow() != 2:
        if memory.main.equipBuyRow() < 2:
            xbox.tapDown()
        else:
            xbox.tapUp()
    xbox.tapB()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapB()
    memory.main.waitFrames(6)
    xbox.menuA()
    memory.main.waitFrames(6)
    xbox.menuA()


def battles1():
    if not memory.main.equippedArmorHasAbility(charNum=1, abilityNum=0x800A):
        nemesis.menu.equipArmor(character=1, ability=0x800A, fullMenuClose=False)
    if not memory.main.equippedArmorHasAbility(charNum=4, abilityNum=0x800A):
        nemesis.menu.equipArmor(character=4, ability=0x800A)
    memory.main.closeMenu()
    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=0)
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=0)
    gameVars.arenaSuccess(arrayNum=0, index=0)
    restockDowns()

    checkYojimboPossible()

    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=1)
    aeonStart()
    autoLife()
    while not basicQuickAttacks(megaPhoenix=True):
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(4)
        memory.main.fullPartyFormat("kilikawoods1")
        touchSave()
        arenaNPC()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=1)
        aeonStart()
        if screen.turnTidus():
            autoLife()
    gameVars.arenaSuccess(arrayNum=0, index=1)
    restockDowns()
    nemesis.arenaSelect.arenaMenuSelect(4)
    memory.main.fullPartyFormat("kilikawoods1")
    nemesis.menu.tidusSlayer(odPos=0)

    checkYojimboPossible()

    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=2)
    while not basicQuickAttacks(yunaAutos=True):
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=2)
    gameVars.arenaSuccess(arrayNum=0, index=2)
    restockDowns()

    checkYojimboPossible()

    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=3)
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=3)
    gameVars.arenaSuccess(arrayNum=0, index=3)
    restockDowns()

    checkYojimboPossible()

    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=4)
    autoLife()
    while not basicQuickAttacks(megaPhoenix=True):
        print("Battle not completed successfully.")
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=4)
        autoLife()
    gameVars.arenaSuccess(arrayNum=0, index=4)
    restockDowns()

    checkYojimboPossible()

    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=5)
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=5)
    gameVars.arenaSuccess(arrayNum=0, index=5)
    restockDowns()

    checkYojimboPossible()

    nemesis.arenaSelect.arenaMenuSelect(4)
    nemesis.menu.tidusSlayer(odPos=2)
    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=6)
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=6)
    gameVars.arenaSuccess(arrayNum=0, index=6)
    restockDowns()

    checkYojimboPossible()

    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=7)
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=7)
    gameVars.arenaSuccess(arrayNum=0, index=7)
    restockDowns()

    checkYojimboPossible()

    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=8)
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=8)
    gameVars.arenaSuccess(arrayNum=0, index=8)
    restockDowns()

    checkYojimboPossible()

    nemesis.arenaSelect.arenaMenuSelect(4)
    nemesis.menu.tidusSlayer(odPos=0)
    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=9)
    while not basicQuickAttacks(yunaAutos=True):
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=9)
    gameVars.arenaSuccess(arrayNum=0, index=9)
    restockDowns()

    checkYojimboPossible()

    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=10)
    autoLife()
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=10)
        autoLife()
    gameVars.arenaSuccess(arrayNum=0, index=10)
    restockDowns()

    checkYojimboPossible()


def battles2():
    print("++Starting second section++")
    nemesis.arenaSelect.arenaMenuSelect(4)
    touchSave()
    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=1)
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(4)
        touchSave()
        arenaNPC()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=1)
    gameVars.arenaSuccess(arrayNum=1, index=1)
    restockDowns()

    checkYojimboPossible()

    nemesis.arenaSelect.arenaMenuSelect(4)
    touchSave()
    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=3)
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=3)
    gameVars.arenaSuccess(arrayNum=1, index=3)
    restockDowns()

    checkYojimboPossible()

    nemesis.arenaSelect.arenaMenuSelect(4)
    touchSave()
    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=5)
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=5)
    gameVars.arenaSuccess(arrayNum=1, index=5)
    restockDowns()

    checkYojimboPossible()

    nemesis.arenaSelect.arenaMenuSelect(4)
    touchSave()
    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=8)
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=8)
    gameVars.arenaSuccess(arrayNum=1, index=8)
    restockDowns()
    nemesis.arenaSelect.arenaMenuSelect(4)
    touchSave()

    checkYojimboPossible()


def jugFarmDone():
    print("||| Slot: ", memory.main.getItemSlot(87))
    if memory.main.getItemSlot(87) > 250:
        return False
    else:
        print("Count: ", memory.main.getItemCountSlot(memory.main.getItemSlot(87)))
        if memory.main.getItemCountSlot(memory.main.getItemSlot(87)) < 6:
            return False
    return True


def juggernautFarm():
    checkYojimboPossible()
    while not jugFarmDone():
        arenaNPC()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=12)
        autoLife()
        basicQuickAttacks(megaPhoenix=True, odVersion=1)
        restockDowns()
        checkYojimboPossible()
        nemesis.arenaSelect.arenaMenuSelect(4)
        touchSave()
    print("Good to go on strength spheres")
    gameVars.arenaSuccess(arrayNum=1, index=12)
    print("Starting menu to finish strength.")
    nemesis.arenaSelect.arenaMenuSelect(4)
    nemesis.menu.strBoost()
    print("Touch save sphere, and then good to go.")
    touchSave()


def battles3():
    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=11)
    autoLife()
    while not basicQuickAttacks(megaPhoenix=True):
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=11)
        autoLife()
    gameVars.arenaSuccess(arrayNum=0, index=11)
    restockDowns()

    checkYojimboPossible()

    nemesis.arenaSelect.arenaMenuSelect(4)
    touchSave()
    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=2)
    aeonStart()
    autoLife()
    while not basicAttack(useOD=False):
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(4)
        touchSave()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=2)
        autoLife()
    gameVars.arenaSuccess(arrayNum=1, index=2)
    restockDowns()

    checkYojimboPossible()

    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=0)
    autoLife()
    while not basicQuickAttacks(megaPhoenix=True, odVersion=1):
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=0)
        autoLife()
    gameVars.arenaSuccess(arrayNum=1, index=0)
    restockDowns()

    checkYojimboPossible()

    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=9)
    autoLife()
    while not basicQuickAttacks(megaPhoenix=True, odVersion=1):
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=9)
        autoLife()
    gameVars.arenaSuccess(arrayNum=1, index=9)
    restockDowns()

    checkYojimboPossible()

    nemesis.arenaSelect.arenaMenuSelect(4)
    touchSave()
    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=10)
    autoLife()
    while not basicQuickAttacks(megaPhoenix=True, odVersion=1):
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=10)
        autoLife()
    gameVars.arenaSuccess(arrayNum=1, index=10)
    restockDowns()

    checkYojimboPossible()


def battles4():
    nemesis.arenaSelect.arenaMenuSelect(4)
    touchSave()
    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=15, monsterIndex=0)
    autoLife()
    while not basicQuickAttacks(megaPhoenix=True, odVersion=1):
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=15, monsterIndex=0)
        autoLife()
    gameVars.arenaSuccess(arrayNum=2, index=0)
    restockDowns()

    checkYojimboPossible()
    nemesis.arenaSelect.arenaMenuSelect(4)
    touchSave()

    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=15, monsterIndex=6)

    while not shinryuBattle():
        print("Battle not completed successfully.")
        restockDowns()
        nemesis.arenaSelect.arenaMenuSelect(4)
        touchSave()
        arenaNPC()
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=15, monsterIndex=6)

    gameVars.arenaSuccess(arrayNum=2, index=6)
    restockDowns()


def itemDump():
    nemesis.arenaSelect.arenaMenuSelect(2)
    memory.main.waitFrames(90)
    xbox.menuRight()
    xbox.menuB()
    nemesis.menu.sellAll(NEA=True)
    xbox.menuA()
    xbox.menuA()
    xbox.menuA()
    xbox.menuA()


def quickResetLogic():
    reset.resetToMainMenu()
    memory.ain.waitFrames(90)
    while memory.main.getMap() != 23:
        FFXC.set_value("BtnStart", 1)
        memory.main.waitFrames(2)
        FFXC.set_value("BtnStart", 0)
        memory.main.waitFrames(2)
    memory.main.waitFrames(60)
    xbox.menuB()
    memory.main.waitFrames(60)
    xbox.menuDown()
    xbox.menuB()
    xbox.menuB()
    FFXC.set_neutral()
    gameVars.printArenaStatus()
    memory.main.waitFrames(30)


def checkYojimboPossible():
    if memory.main.overdriveState2()[1] < 100:
        return False
    if memory.main.overdriveState2()[1] == 100 and memory.main.getGilvalue() < 300000:
        itemDump()

    if memory.main.overdriveState2()[1] == 100 and memory.main.getGilvalue() >= 300000:
        # Save game in preparation for the Yojimbo attempt
        memory.main.waitFrames(20)
        nemesis.arenaSelect.arenaMenuSelect(4)
        memory.main.fullPartyFormat("kilikawoods1")
        if gameVars.yojimboGetIndex() == 1:
            saveGame(firstSave=True)
        else:
            saveGame(firstSave=False)

        # Now attempt to get Zanmato until successful, no re-saving.
        while not battles5(gameVars.yojimboGetIndex()):
            quickResetLogic()
        return True
    else:
        return False


def shinryuBattle():
    rikkuFirstTurn = False
    rikkuDriveComplete = False
    screen.awaitTurn()
    while memory.main.battleActive():
        if memory.main.turnReady():
            if screen.turnRikku():
                if not rikkuFirstTurn:
                    battle.main.defend()
                elif rikkuDriveComplete:
                    battle.main._useHealingItem(itemID=9)
                else:
                    battle.main.rikkuFullOD("shinryu")
                    rikkuDriveComplete = True
            elif screen.turnTidus():
                if memory.main.getOverdriveBattle(0) == 100:
                    battle.overdrive.tidus(version=1)
                elif rikkuDriveComplete and not memory.main.autoLifeState():
                    autoLife()
                else:
                    battle.main.attack("none")
            else:
                battle.main.defend()

    # After battle stuff
    while not memory.main.menuOpen():
        xbox.tapB()
    FFXC.set_value("BtnB", 1)
    memory.main.waitFrames(150)
    FFXC.set_neutral()
    memory.main.waitFrames(2)
    return memory.main.battleArenaResults()


def battles5(completionVersion: int):
    print("Yojimbo battle number: ", completionVersion)
    if completionVersion >= 12 and completionVersion != 99:
        return True  # These battles are complete at this point.
    yojimboSuccess = False

    # Now for the Yojimbo section
    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)

    # Battles here
    if completionVersion == 1:
        nemesis.arenaSelect.startFight(areaIndex=15, monsterIndex=1)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=2, index=1)
            yojimboSuccess = True

    elif completionVersion == 2:
        nemesis.arenaSelect.startFight(areaIndex=15, monsterIndex=2)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=2, index=2)
            yojimboSuccess = True

    elif completionVersion == 3:
        nemesis.arenaSelect.startFight(areaIndex=15, monsterIndex=3)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=2, index=3)
            yojimboSuccess = True

    elif completionVersion == 4:
        nemesis.arenaSelect.startFight(areaIndex=15, monsterIndex=4)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=2, index=4)
            yojimboSuccess = True

    elif completionVersion == 5:
        nemesis.arenaSelect.startFight(areaIndex=15, monsterIndex=5)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=2, index=5)
            yojimboSuccess = True

    elif completionVersion == 6:
        nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=12)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=0, index=12)
            yojimboSuccess = True

    elif completionVersion == 7:
        nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=13)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=1, index=13)
            yojimboSuccess = True

    elif completionVersion == 8:
        nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=11)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=1, index=11)
            yojimboSuccess = True

    elif completionVersion == 9:
        nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=7)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=1, index=7)
            yojimboSuccess = True

    elif completionVersion == 10:
        nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=6)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=1, index=6)
            yojimboSuccess = True

    elif completionVersion == 11:
        nemesis.arenaSelect.startFight(areaIndex=14, monsterIndex=4)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=1, index=4)
            yojimboSuccess = True

    elif completionVersion == 99:  # Nemesis
        nemesis.arenaSelect.startFight(areaIndex=15, monsterIndex=7)
        if yojimboBattle():
            memory.main.clickToDiagProgress(2)
            memory.main.clickToControl3()
            return True
        else:
            return False

    # Wrap up decisions
    if yojimboSuccess:
        gameVars.yojimboIncrementIndex()
        if completionVersion != 99:
            restockDowns()
        return True
    else:
        nemesis.arenaSelect.arenaMenuSelect(4)
        return False


def rechargeYuna():
    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=13, monsterIndex=9)
    screen.awaitTurn()
    while memory.main.battleActive():
        if memory.main.turnReady():
            if screen.turnYuna():
                battle.main.attack("none")
            else:
                battle.main.escapeOne()


def nemesisBattle():
    if gameVars.yojimboGetIndex() < 12:
        nemesis.arenaSelect.arenaMenuSelect(4)
        touchSave()
        while gameVars.yojimboGetIndex() < 12:
            # If Yuna is charged, do next battle. Otherwise charge.
            if memory.main.overdriveState2()[1] == 100:
                battles5(gameVars.yojimboGetIndex())
            else:
                rechargeYuna()
            nemesis.arenaSelect.arenaMenuSelect(4)
            touchSave()

    if memory.main.overdriveState2()[1] != 100:
        rechargeYuna()
    if memory.main.getGilvalue() < 300000:
        nemesis.arenaSelect.arenaMenuSelect(4)
        nemesis.menu.autoSortEquipment()
        # nemesis.menu.autoSortItems()
        arenaNPC()
        nemesis.arenaSelect.arenaMenuSelect(2)
        memory.main.waitFrames(90)
        xbox.menuRight()
        xbox.menuB()
        nemesis.menu.sellAll()
        xbox.menuA()
        xbox.menuA()
        xbox.menuA()
        xbox.menuA()
        xbox.menuA()
        xbox.menuA()
        xbox.menuA()
    nemesis.arenaSelect.arenaMenuSelect(4)
    memory.main.fullPartyFormat("kilikawoods1")
    saveGame(firstSave=False)
    while not battles5(completionVersion=99):
        quickResetLogic()
    # nemesis.nemesis.arenaSelect.arenaMenuSelect(4)


def returnToSin():
    FFXC = xbox.controllerHandle()
    while not nemesis.targetPath.setMovement([-6, -27]):
        pass
    while not nemesis.targetPath.setMovement([-2, -2]):
        pass
    returnToAirship()

    nemesis.menu.equipWeapon(character=0, ability=0x8001, fullMenuClose=True)
    airShipDestination(destNum=0)
    memory.main.awaitControl()
    FFXC.set_movement(0, -1)
    memory.main.waitFrames(2)
    memory.main.awaitEvent()
    FFXC.set_neutral()
