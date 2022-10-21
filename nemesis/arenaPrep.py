import battle.boss
import battle.main
import memory.main
import nemesis.arenaSelect
import nemesis.menu
import nemesis.targetPath
import rngTrack
import screen
import vars
import xbox

gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()

# The following functions extend the regular Bahamut run. Farming sections.


def autoLife():
    while not (memory.main.turnReady() and screen.turnTidus()):
        if memory.main.turnReady():
            if screen.turnAeon():
                battle.main.attack("none")
            elif not screen.turnTidus():
                battle.main.defend()
    while memory.main.battleMenuCursor() != 22:
        if screen.turnTidus() == False:
            print("Attempting Auto-life, but it's not Tidus's turn")
            xbox.tapUp()
            xbox.tapUp()
            return
        if memory.main.battleMenuCursor() == 1:
            xbox.tapUp()
        else:
            xbox.tapDown()
    while not memory.main.otherBattleMenu():
        xbox.tapB()
    memory.main._navigate_to_position(1)
    while memory.main.otherBattleMenu():
        xbox.tapB()
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()


# Default to Besaid. Maybe based on map number?
def airShipDestination(destNum=0, forceOmega=False):
    if gameVars.csr():
        if destNum >= 13:  # Adjust for Besaid and Kilika locations
            if forceOmega:
                destNum += 4
            else:
                destNum += 5
        elif destNum >= 5:  # Adjust for Mushroom Rock flight path
            destNum += 4
        elif destNum >= 2:  # Adjust for Omega
            destNum += 3

    while not memory.main.getMap() in [382, 999]:
        if memory.main.userControl():
            nemesis.targetPath.setMovement([-251, 340])
        else:
            FFXC.set_neutral()
        xbox.menuB()
    while memory.main.diagProgressFlag() != 4:
        xbox.tapB()
    print("Destination select on screen now.")
    while memory.main.mapCursor() != destNum:
        if destNum < 8:
            xbox.tapDown()
        else:
            xbox.tapUp()
    xbox.tapB()
    memory.main.waitFrames(2)
    xbox.tapB()
    while not memory.main.userControl():
        if memory.main.cutsceneSkipPossible():
            xbox.skipScene()
        elif memory.main.diagSkipPossible():
            xbox.tapB()


def unlockOmega():
    if gameVars.csr():
        return

    while not memory.main.getMap() in [382, 999]:
        if memory.main.userControl():
            nemesis.targetPath.setMovement([-251, 340])
        else:
            FFXC.set_neutral()
        if memory.main.diagProgressFlag() == 4:
            xbox.menuA()
        else:
            xbox.menuB()
    while memory.main.diagProgressFlag() != 3:
        xbox.tapUp()
    while memory.main.diagProgressFlag() != 0:
        xbox.tapB()

    while memory.main.diagProgressFlag() == 0:
        print(memory.main.getCoords())
        if memory.main.getCoords()[0] < 65:
            FFXC.set_value("Dpad", 8)
        if memory.main.getCoords()[0] < 70:
            nemesis.menu.gridRight()
        elif memory.main.getCoords()[0] > 78:
            FFXC.set_value("Dpad", 4)
        elif memory.main.getCoords()[0] > 73:
            nemesis.menu.gridLeft()
        elif memory.main.getCoords()[1] > -28:
            FFXC.set_value("Dpad", 2)
        elif memory.main.getCoords()[1] > -34:
            nemesis.menu.gridDown()
        elif memory.main.getCoords()[1] < -40:
            FFXC.set_value("Dpad", 1)
        elif memory.main.getCoords()[1] < -37:
            nemesis.menu.gridUp()
        else:
            xbox.menuB()
    memory.main.waitFrames(30)
    xbox.menuB()
    while not memory.main.getMap() in [194, 374]:
        xbox.menuA()


def getSaveSphereDetails():
    return memory.main.getSaveSphereDetails()


def getSaveSphereDetails_old():
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
    if mapVal == 259:
        # Gagazet (only used in Nemesis)
        x = -59
        y = 99
        diag = 219
    if mapVal == 128:
        # MRR upper lift (only used in Nemesis)
        x = 230
        y = 140
        diag = 68

    print("Values: [", x, ",", y, "] - ", diag)
    return [x, y, diag]


def returnToAirship():
    print("Attempting Return to Airship")

    ssDetails = getSaveSphereDetails()

    if memory.main.getMap() == 307:  # Monster arena
        while not nemesis.targetPath.setMovement([-4, -3]):
            pass

    if memory.main.getMap() == 263:  # Thunder plains
        while not nemesis.targetPath.setMovement([-39, -18]):
            pass

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


def battleFarmAll(apCpLimit: int = 255, yunaAttack=True, faythCave=True):
    print("### Battle Start:", memory.main.getEncounterID())
    FFXC.set_neutral()
    if faythCave == True and memory.main.battleType() == 2:
        screen.awaitTurn()
        battle.main.fleeAll()
    else:
        while memory.main.battleActive():
            if memory.main.turnReady():
                if screen.turnTidus():
                    if memory.main.getEncounterID() in [154, 156, 164]:
                        # Confusion is a dumb mechanic in this game.
                        battle.main.attackByNum(22, "l")
                    elif memory.main.getEncounterID() == 281:
                        battle.main.attackByNum(22, "r")
                    elif memory.main.getEncounterID() == 283:
                        battle.main.attackByNum(21, "u")
                    elif memory.main.getEncounterID() == 284:
                        battle.main.attackByNum(23, "d")
                    else:
                        battle.main.attack("none")
                elif screen.turnYuna():
                    if yunaAttack:
                        if memory.main.getEncounterID() in [154, 156, 164]:
                            # Confusion is a dumb mechanic in this game.
                            battle.main.attackByNum(22, "l")
                        elif memory.main.getEncounterID() == 281:
                            battle.main.attackByNum(21, "l")
                        elif memory.main.getEncounterID() == 283:
                            battle.main.attackByNum(22, "d")
                        elif memory.main.getEncounterID() == 284:
                            battle.main.attackByNum(22, "d")
                        else:
                            battle.main.attack("none")
                    else:
                        battle.main.escapeOne()
                elif screen.turnRikku() or screen.turnWakka():
                    if not battle.main.checkTidusOk():
                        battle.main.escapeOne()
                    elif memory.main.getEncounterID() == 219:
                        battle.main.escapeOne()
                    else:
                        battle.main.defend()
                else:
                    battle.main.escapeOne()
    memory.main.clickToControl()
    if float(memory.main.getHP()[0]) / float(memory.main.getMaxHP()[0]) < 0.4:
        battle.main.healUp(3)
    nemesis.menu.performNextGrid(limit=apCpLimit)


def advancedCompleteCheck():
    encounterID = memory.main.getEncounterID()
    arenaArray = memory.main.arenaArray()
    # Common monsters
    if False:
        pass

    # Inside Sin
    elif encounterID == 374:  # Ahriman
        print("For this battle, count:", arenaArray[37])
        if arenaArray[37] == 10:
            return True
    elif encounterID in [375, 380]:  # Exoray (with a bonus Ahriman)
        print("For this battle, count:", arenaArray[93])
        if arenaArray[93] == 10 and arenaArray[37] == 10:
            return True
    elif encounterID in [376, 381]:  # Adamantoise
        print("For this battle, count:", arenaArray[81])
        if arenaArray[81] == 10:
            return True
    elif encounterID in [377, 382]:  # Both kinds of Gemini
        print("For this battle, count:", arenaArray[77])
        print("For this battle, count:", arenaArray[78])
        if arenaArray[77] == 10 and arenaArray[78] == 10:
            return True
    elif encounterID in [378, 384]:  # Behemoth King
        print("For this battle, count:", arenaArray[70])
        if arenaArray[70] == 10:
            return True
    elif encounterID == 383:  # Demonolith
        print("For this battle, count:", arenaArray[75])
        if arenaArray[75] == 10:
            return True
    elif encounterID == 385:  # Great Malboro
        print("For this battle, count:", arenaArray[56])
        if arenaArray[56] == 10:
            return True
    elif encounterID == 386:  # Barbatos
        print("For this battle, count:", arenaArray[90])
        if arenaArray[90] == 10:
            return True
    elif encounterID == 387:  # Wraith
        print("For this battle, count:", arenaArray[97])
        if arenaArray[97] == 10:
            return True

    # Omega dungeon
    elif encounterID == 421:  # Master Coeurl and Floating Death
        print("For this battle, count:", arenaArray[74])
        print("For this battle, count:", arenaArray[102])
        if arenaArray[74] == 10 and arenaArray[102] == 10:
            return True
    elif encounterID == 422:  # Halma and Spirit
        print("For this battle, count:", arenaArray[96])
        print("For this battle, count:", arenaArray[101])
        if arenaArray[96] == 10 and arenaArray[101] == 10:
            return True
    elif encounterID == 423:  # Zaurus and Floating Death
        print("For this battle, count:", arenaArray[100])
        print("For this battle, count:", arenaArray[102])
        if arenaArray[100] == 10 and arenaArray[102] == 10:
            return True
    elif encounterID == 424:  # Black Element and Spirit
        print("For this battle, count:", arenaArray[67])
        print("For this battle, count:", arenaArray[96])
        if arenaArray[67] == 10 and arenaArray[96] == 10:
            return True
    elif encounterID == 425:  # Varuna
        print("For this battle, count:", arenaArray[82])
        if arenaArray[82] == 10:
            return True
    elif encounterID == 426:  # Master Tonberry
        print("For this battle, count:", arenaArray[99])
        if arenaArray[99] == 10:
            return True
    elif encounterID == 428:  # Machea (blade thing)
        print("For this battle, count:", arenaArray[103])
        if arenaArray[103] == 10:
            return True
    elif encounterID == 430:  # Demonolith x2
        print("For this battle, count:", arenaArray[75])
        if arenaArray[75] == 10:
            return True
    elif encounterID in [432, 433, 434, 435, 436]:  # Just Zaurus
        print("For this battle, count:", arenaArray[100])
        if arenaArray[100] == 10:
            return True
    elif encounterID == 437:  # Puroboros
        print("For this battle, count:", arenaArray[95])
        if arenaArray[95] == 10:
            return True
    elif encounterID == 438:  # Wraith
        print("For this battle, count:", arenaArray[97])
        if arenaArray[97] == 10:
            return True

    # Other
    if encounterID in [429, 445]:
        # Rock monsters, just leave.
        return True
    if encounterID == 383:
        # Demonolith inside Sin, not worth.
        return True
    if encounterID == 427:
        # Adamantoise in Omega, dealt with inside Sin
        return True

    return False


def advancedBattleLogic():
    print("### Battle Start:", memory.main.getEncounterID())
    print("### Ambush flag (2 is bad):", memory.main.battleType())
    while not memory.main.turnReady():
        pass
    autoLifeUsed = False
    FFXC.set_neutral()

    if memory.main.battleType() == 2:
        print(">>>>Ambushed! Escaping!")
        battle.main.tidusFlee()
    elif advancedCompleteCheck():
        print(">>>>Complete collecting this monster.")
        battle.main.tidusFlee()
    else:
        if memory.main.getEncounterID() == 449:
            # Omega himself, not yet working.
            aeonComplete = False
            while memory.main.battleActive():
                if memory.main.turnReady():
                    if screen.turnRikku():
                        if not aeonComplete:
                            battle.main.buddySwapYuna()
                            battle.main.aeonSummon(4)
                        else:
                            battle.main.defend()
                    elif screen.turnYuna():
                        battle.main.buddySwapRikku()
                    elif screen.turnTidus():
                        battle.main.useSkill(1)  # Quick hit
                    else:
                        battle.main.defend()
        else:
            print("---Regular battle:", memory.main.getEncounterID())
            sleepPowder = False
            while memory.main.battleActive():
                encounterID = memory.main.getEncounterID()
                if memory.main.turnReady():
                    if encounterID in [442]:
                        # Damned malboros in Omega
                        battle.main.buddySwapYuna()
                        battle.main.aeonSummon(4)
                        battle.main.attack("none")
                    elif screen.turnTidus():
                        if memory.main.getEncounterID() in [386] and not autoLifeUsed:
                            autoLife()
                            autoLifeUsed = True
                        elif (
                            encounterID == 383
                            and memory.main.getEnemyCurrentHP()[0] > 9999
                        ):
                            if memory.main.getUseItemsSlot(41) < 100:
                                battle.main.useItemTidus(
                                    memory.main.getUseItemsSlot(41)
                                )
                            else:
                                battle.main.useSkill(1)
                        elif (
                            encounterID == 426
                            and memory.main.getEnemyCurrentHP()[0] > 9999
                        ):
                            if memory.main.getUseItemsSlot(41) < 100:
                                battle.main.useItemTidus(
                                    memory.main.getUseItemsSlot(41)
                                )
                            else:
                                battle.main.useSkill(1)
                        elif (
                            encounterID == 430
                            and memory.main.getEnemyCurrentHP()[0] > 9999
                        ):
                            if memory.main.getUseItemsSlot(41) < 100:
                                battle.main.useItemTidus(
                                    memory.main.getUseItemsSlot(41)
                                )
                            else:
                                battle.main.useSkill(1)
                        elif (
                            encounterID == 437
                            and memory.main.getEnemyCurrentHP()[0] > 9999
                        ):
                            if memory.main.getUseItemsSlot(41) < 100:
                                battle.main.useItemTidus(
                                    memory.main.getUseItemsSlot(41)
                                )
                            else:
                                battle.main.useSkill(1)
                        elif encounterID == 431:
                            battle.main.tidusFlee()
                        else:
                            battle.main.useSkill(1)  # Quick hit
                    elif screen.turnRikku():
                        if encounterID in [377, 382]:
                            print(
                                "Shining Gems for Gemini, better to save other items for other enemies."
                            )
                            # Double Gemini, two different locations
                            if memory.main.getUseItemsSlot(42) < 100:
                                battle.main.useItem(
                                    memory.main.getUseItemsSlot(42), rikkuFlee=False
                                )
                            else:
                                battle.main.defend()
                        elif encounterID == 386:
                            # Armor bomber guys
                            if memory.main.getUseItemsSlot(41) < 100:
                                battle.main.useItem(
                                    memory.main.getUseItemsSlot(41), rikkuFlee=False
                                )
                            else:
                                battle.main.defend()
                        elif encounterID in [430]:
                            # Demonolith
                            if memory.main.getUseItemsSlot(41) < 100:
                                battle.main.useItem(
                                    memory.main.getUseItemsSlot(41), rikkuFlee=False
                                )
                            else:
                                battle.main.defend()
                        elif encounterID == 422:
                            # Provoke on Spirit
                            battle.main.useSpecial(position=3, target=21, direction="u")
                            if memory.main.getUseItemsSlot(41) < 100:
                                battle.main.useItem(
                                    memory.main.getUseItemsSlot(41), rikkuFlee=False
                                )
                            else:
                                battle.main.defend()
                        elif encounterID == 424:
                            # Provoke on Spirit
                            battle.main.useSpecial(position=3, target=21, direction="r")
                        elif (
                            encounterID == 425
                            and memory.main.getEnemyCurrentHP()[0] > 9999
                        ):
                            # Varuna, use purifying salt to remove haste
                            # Safety potions are fun.
                            battle.main.useItem(
                                memory.main.getUseItemsSlot(63), rikkuFlee=False
                            )
                        elif encounterID == 426:
                            # Master Tonberry
                            if not sleepPowder:
                                battle.main.useItem(
                                    memory.main.getUseItemsSlot(37), rikkuFlee=False
                                )
                            else:
                                if memory.main.getUseItemsSlot(41) < 100:
                                    battle.main.useItemTidus(
                                        memory.main.getUseItemsSlot(41)
                                    )
                                else:
                                    battle.main.defend()
                        elif encounterID == 431:
                            battle.main.tidusFlee()
                        elif (
                            encounterID == 437
                            and memory.main.getEnemyCurrentHP()[0] > 9999
                        ):
                            if not sleepPowder:
                                battle.main.useItem(
                                    memory.main.getUseItemsSlot(37), rikkuFlee=False
                                )
                            else:
                                if memory.main.getUseItemsSlot(41) < 100:
                                    battle.main.useItemTidus(
                                        memory.main.getUseItemsSlot(41)
                                    )
                                else:
                                    battle.main.defend()
                        else:
                            battle.main.defend()
                    else:
                        battle.main.defend()
    memory.main.clickToControl()
    memory.main.fullPartyFormat("initiative")
    nemesis.menu.performNextGrid()
    if float(memory.main.getHP()[0]) / float(memory.main.getMaxHP()[0]) < 0.3:
        battle.main.healUp(3)


def bribeBattle(spareChangeValue: int = 12000):
    while memory.main.battleActive():
        if memory.main.turnReady():
            if screen.turnLulu():
                while memory.main.battleMenuCursor() != 20:
                    if memory.main.battleMenuCursor() == 0:
                        xbox.tapDown()
                    else:
                        xbox.tapUp()
                    if gameVars.usePause():
                        memory.main.waitFrames(6)
                memory.main.waitFrames(8)
                xbox.tapB()
                memory.main.waitFrames(8)
                xbox.tapB()
                memory.main.waitFrames(8)
                memory.main.calculateSpareChangeMovement(spareChangeValue)
                while memory.main.spareChangeOpen():
                    xbox.tapB()
                xbox.tapB()
                xbox.tapB()
            else:
                battle.main.buddySwapLulu()
    print("Battle is complete.")
    while not memory.main.menuOpen():
        pass
    FFXC.set_value("BtnB", 1)
    memory.main.waitFrames(150)
    FFXC.set_value("BtnB", 0)
    print("Now back in control.")


def arenaNPC():
    memory.main.awaitControl()
    if memory.main.getMap() != 307:
        return
    while not (memory.main.diagProgressFlag() == 74 and memory.main.diagSkipPossible()):
        if memory.main.userControl():
            if memory.main.getCoords()[1] > -12:
                FFXC.set_movement(0, -1)
                memory.main.waitFrames(1)
            else:
                nemesis.targetPath.setMovement([2, -15])
                xbox.tapB()
        else:
            FFXC.set_neutral()
            if memory.main.diagProgressFlag() == 59:
                xbox.menuA()
                xbox.menuA()
                xbox.menuA()
                xbox.tapB()
            elif memory.main.diagSkipPossible():
                xbox.tapB()
    print("Mark 1")
    memory.main.waitFrames(30)  # This buffer can be improved later.
    print("Mark 2")


def arenaReturn(checkpoint: int = 0):
    if checkpoint == 0:
        airShipDestination(destNum=12)
    # nemesis.menu.equipArmor(character=gameVars.neArmor(),ability=0x801D)

    while memory.main.getMap() != 307:
        if memory.main.userControl():
            if checkpoint == 2:
                while memory.main.userControl():
                    nemesis.targetPath.setMovement([-641, -268])
                    xbox.tapB()
                FFXC.set_neutral()
                checkpoint += 1
            elif nemesis.targetPath.setMovement(
                nemesis.targetPath.arenaReturn(checkpoint)
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()


def transition():
    memory.main.clickToControl()
    returnToAirship()
    memory.main.awaitControl()
    nemesis.menu.addAbility(
        owner=0,
        equipment_type=0,
        ability_array=[0x807A, 255, 255, 255],
        ability_index=0x8001,
        slotcount=2,
        navigateToEquipMenu=True,
        fullMenuClose=True,
    )


def kilikaShop():
    arenaNPC()
    xbox.tapA()
    xbox.tapB()
    memory.main.waitFrames(60)
    arenaNPC()
    xbox.tapA()
    xbox.tapB()
    arenaNPC()
    # xbox.tapDown()
    # xbox.tapDown()
    # xbox.tapB()
    # memory.waitFrames(30)
    # xbox.tapB() #Buy
    # memory.waitFrames(30)
    # getEquipment(equip=False) #Tidus second catcher weapon
    # xbox.menuA()
    # memory.waitFrames(30)
    # xbox.menuA()
    # memory.waitFrames(30)
    xbox.menuA()
    xbox.tapB()  # Exit
    memory.main.waitFrames(60)
    while not nemesis.targetPath.setMovement([-6, -23]):
        pass
    while not nemesis.targetPath.setMovement([0, -3]):
        pass
    returnToAirship()
    memory.main.awaitControl()
    # nemesis.menu.equipWeapon(character=0,ability=0x807A, fullMenuClose=False)
    airShipDestination(destNum=2)
    while not nemesis.targetPath.setMovement([-25, -246]):
        pass
    while not nemesis.targetPath.setMovement([-47, -209]):
        pass
    while not nemesis.targetPath.setMovement([-91, -199]):
        pass
    while not nemesis.targetPath.setMovement([-108, -169]):
        pass
    while memory.main.userControl():
        FFXC.set_movement(-1, 0)
        xbox.tapB()
    FFXC.set_neutral()  # Now talking to vendor
    memory.main.waitFrames(60)
    xbox.tapB()  # Intro dialog
    memory.main.waitFrames(60)
    xbox.tapB()  # Buy equipment
    memory.main.waitFrames(60)
    # getEquipment(equip=False) #Weapon for Yuna
    xbox.tapDown()
    xbox.tapDown()
    xbox.tapDown()
    xbox.tapDown()
    xbox.tapDown()
    xbox.tapDown()
    getEquipment(equip=True)  # Weapon for Rikku
    xbox.tapDown()
    getEquipment(equip=True)  # Armor for Tidus
    xbox.tapDown()
    getEquipment(equip=True)  # Armor for Yuna
    xbox.tapDown()
    getEquipment(equip=True)  # Armor for Wakka
    xbox.tapDown()
    xbox.tapDown()
    xbox.tapDown()
    getEquipment(equip=True)  # Armor for Wakka
    xbox.tapDown()
    getEquipment(equip=True)  # Armor for Rikku
    memory.main.closeMenu()
    nemesis.menu.addAbility(
        owner=6,
        equipment_type=0,
        ability_array=[0x800B, 0x8000, 255, 255],
        ability_index=0x8001,
        slotcount=4,
        navigateToEquipMenu=True,
        fullMenuClose=True,
    )
    nemesis.menu.addAbility(
        owner=0,
        equipment_type=1,
        ability_array=[0x8072, 255, 255, 255],
        ability_index=0x8056,
        slotcount=4,
        navigateToEquipMenu=True,
        fullMenuClose=True,
    )

    while not nemesis.targetPath.setMovement([-91, -199]):
        pass
    while not nemesis.targetPath.setMovement([-47, -209]):
        pass
    while not nemesis.targetPath.setMovement([-25, -246]):
        pass
    while not nemesis.targetPath.setMovement([29, -252]):
        pass
    returnToAirship()


def odToAP():  # Calm Lands purchases
    arenaReturn()
    arenaNPC()
    xbox.tapA()
    xbox.tapB()
    arenaNPC()
    xbox.tapA()
    xbox.tapB()
    arenaNPC()
    xbox.tapA()
    xbox.tapB()
    arenaNPC()
    xbox.tapA()
    xbox.tapB()
    arenaNPC()
    xbox.tapDown()
    xbox.tapDown()
    xbox.tapB()
    memory.main.waitFrames(60)
    xbox.tapB()
    memory.main.waitFrames(6)
    xbox.tapB()
    memory.main.waitFrames(6)
    xbox.tapUp()
    xbox.tapB()
    memory.main.waitFrames(6)
    xbox.tapUp()
    xbox.tapB()
    print("Now to sell items.")
    memory.main.waitFrames(6)
    xbox.menuA()
    memory.main.waitFrames(6)
    xbox.tapRight()
    xbox.menuB()
    print("Should now be attempting to sell items.")
    nemesis.menu.sellAll()
    xbox.menuA()
    memory.main.waitFrames(60)
    xbox.tapA()
    memory.main.waitFrames(60)
    xbox.tapA()
    memory.main.waitFrames(60)
    xbox.tapA()
    xbox.tapB()
    nemesis.menu.autoSortEquipment(manual="n")
    nemesis.menu.addAbility(
        owner=0,
        equipment_type=0,
        ability_array=[0x807A, 255, 255, 255],
        ability_index=0x8011,
        slotcount=2,
        navigateToEquipMenu=True,
        exitOutOfCurrentWeapon=True,
        closeMenu=True,
        fullMenuClose=False,
    )
    nemesis.menu.equipWeapon(character=0, ability=0x8011)
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    nemesis.menu.tidusSlayer()

    memory.main.awaitControl()
    FFXC.set_movement(-1, 0)
    memory.main.waitFrames(30)
    returnToAirship()


def farmFeathers():
    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=7, monsterIndex=5)
    memory.main.waitFrames(1)
    waitCounter = 0
    while memory.main.battleActive():
        if memory.main.turnReady():
            if screen.turnRikku():
                print("+++ Qactar steal command")
                battle.main.Steal()
                print("+++ Qactar steal command done")
            elif screen.turnTidus():
                print("+++ Qactar flee command")
                battle.main.tidusFlee()
                print("+++ Qactar flee command done")
            else:
                print("+++ Qactar defend command")
                battle.main.defend()
                print("+++ Qactar defend command done")
        waitCounter += 1
        if waitCounter % 10 == 0:
            print("Waiting for next turn: ", waitCounter)
    print("Battle is complete.")

    while not memory.main.menuOpen():
        pass
    # memory.waitFrames(300)

    FFXC.set_value("BtnB", 1)
    memory.main.waitFrames(150)
    FFXC.set_value("BtnB", 0)
    print("Now back in control.")
    nemesis.arenaSelect.arenaMenuSelect(4)


def autoPhoenix():  # Calm Lands items
    nemesis.menu.autoSortEquipment()
    nemesis.menu.luluBribe()
    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=7, monsterIndex=0)
    bribeBattle()
    nemesis.arenaSelect.arenaMenuSelect(4)
    memory.main.fullPartyFormat("initiative")
    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=7, monsterIndex=0)
    bribeBattle()
    nemesis.arenaSelect.arenaMenuSelect(4)
    memory.main.fullPartyFormat("initiative")
    arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(1)
    nemesis.arenaSelect.startFight(areaIndex=7, monsterIndex=0)
    bribeBattle()
    nemesis.arenaSelect.arenaMenuSelect(4)
    memory.main.fullPartyFormat("initiative")
    arenaNPC()
    while memory.main.getItemCountSlot(memory.main.getItemSlot(7)) != 99:
        print("Trying to obtain mega-phoenix downs")
        nemesis.arenaSelect.arenaMenuSelect(4)
        arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(2)  # Equipment menu
    memory.main.waitFrames(90)
    xbox.tapRight()
    xbox.menuB()  # Sell
    nemesis.menu.sellAll()
    memory.main.waitFrames(3)
    xbox.tapA()
    memory.main.waitFrames(90)
    xbox.tapA()
    memory.main.waitFrames(90)
    xbox.tapA()
    xbox.tapB()
    nemesis.menu.autoSortEquipment()  # This to make sure equipment is in the right place
    nemesis.menu.addAbility(
        owner=4,
        equipment_type=1,
        ability_array=[0x8072, 255, 255, 255],
        ability_index=0x800A,
        slotcount=4,
        navigateToEquipMenu=True,
        exitOutOfCurrentWeapon=True,
        closeMenu=True,
        fullMenuClose=False,
    )

    memory.main.waitFrames(30)
    initArray = memory.main.checkAbility(ability=0x8002)
    print("Initiative weapons: ", initArray)
    if initArray[4]:
        nemesis.menu.addAbility(
            owner=6,
            equipment_type=1,
            ability_array=[0x8072, 255, 255, 255],
            ability_index=0x800A,
            slotcount=4,
            navigateToEquipMenu=True,
            exitOutOfCurrentWeapon=True,
            closeMenu=True,
            fullMenuClose=False,
        )
        nemesis.menu.equipWeapon(character=4, ability=0x8002)  # Initiative
        memory.main.closeMenu()
    else:
        nemesis.menu.addAbility(
            owner=6,
            equipment_type=1,
            ability_array=[0x8072, 255, 255, 255],
            ability_index=0x800A,
            slotcount=4,
            navigateToEquipMenu=True,
            exitOutOfCurrentWeapon=True,
            closeMenu=True,
            fullMenuClose=True,
        )
        memory.main.closeMenu()
        featherSlot = memory.main.getItemSlot(itemNum=54)
        if featherSlot == 255 or memory.main.getItemCountSlot(featherSlot) < 6:
            while featherSlot == 255 or memory.main.getItemCountSlot(featherSlot) < 6:
                farmFeathers()
                featherSlot = memory.main.getItemSlot(itemNum=54)
        nemesis.menu.addAbility(
            owner=6,
            equipment_type=0,
            ability_array=[0x800B, 0x8000, 0x8001, 255],
            ability_index=0x8002,
            slotcount=4,
            navigateToEquipMenu=True,
            exitOutOfCurrentWeapon=True,
            closeMenu=True,
            fullMenuClose=True,
        )

    FFXC.set_movement(-1, 0)
    memory.main.waitFrames(15)
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(15)
    FFXC.set_neutral()
    memory.main.fullPartyFormat("initiative")
    returnToAirship()

    # nemesis.menu.equipArmor(character=0,ability=0x8056) #Auto-Haste
    nemesis.menu.equipArmor(character=4, ability=0x800A)  # Auto-Phoenix
    nemesis.menu.equipArmor(character=6, ability=0x800A)  # Auto-Phoenix
    if not gameVars.neArmor() in [0, 4, 6]:
        nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=99)  # Unequip
    memory.main.closeMenu()


def restockDowns():
    print("Restocking phoenix downs")
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


def oneMpReady():
    print("Slot, Gambler:", memory.main.getItemSlot(41))
    if memory.main.getItemSlot(41) > 200:
        return False
    print("Count, Gambler:", memory.main.getItemCountSlot(memory.main.getItemSlot(41)))
    if memory.main.getItemCountSlot(memory.main.getItemSlot(41)) < 99:
        return False
    print("Slot, Salt:", memory.main.getItemSlot(63))
    if memory.main.getItemSlot(63) > 200:
        return False
    print("Count, Salt:", memory.main.getItemCountSlot(memory.main.getItemSlot(63)))
    if memory.main.getItemCountSlot(memory.main.getItemSlot(63)) < 20:
        return False
    return True


def oneMpWeapon():  # Break Damage Limit, or One MP cost
    nemesis.menu.autoSortEquipment()
    memory.main.fullPartyFormat("initiative")
    arenaNPC()
    print(
        "###Sleeping powder count:",
        memory.main.getItemCountSlot(memory.main.getItemSlot(37)),
    )
    while (
        memory.main.getItemSlot(37) > 200
        or memory.main.getItemCountSlot(memory.main.getItemSlot(37)) < 41
    ):
        nemesis.arenaSelect.arenaMenuSelect(1)
        nemesis.arenaSelect.startFight(areaIndex=7, monsterIndex=0)
        bribeBattle()
        nemesis.arenaSelect.arenaMenuSelect(4)
        memory.main.fullPartyFormat("initiative")
        arenaNPC()
        print(
            "###Sleeping powder count:",
            memory.main.getItemCountSlot(memory.main.getItemSlot(37)),
        )
    while not oneMpReady():
        print("Trying to obtain Gambler's Soul and Purifying Salt items")
        nemesis.arenaSelect.arenaMenuSelect(4)
        arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(2)
    memory.main.waitFrames(60)
    xbox.menuB()  # Buy
    memory.main.waitFrames(10)
    xbox.menuB()  # New Tidus capture weapon
    memory.main.waitFrames(10)
    xbox.tapUp()
    xbox.menuB()  # Confirm purchase
    memory.main.waitFrames(10)
    xbox.tapUp()
    xbox.menuB()  # Confirm equipping weapon

    memory.main.waitFrames(3)
    xbox.tapA()
    memory.main.waitFrames(30)
    xbox.tapA()
    memory.main.waitFrames(30)
    xbox.tapA()
    xbox.tapB()
    nemesis.menu.autoSortEquipment()  # This to make sure equipment is in the right place
    memory.main.closeMenu()
    nemesis.menu.addAbility(
        owner=0,
        equipment_type=0,
        ability_array=[0x807A, 255, 255, 255],
        ability_index=0x800D,
        slotcount=2,
        navigateToEquipMenu=True,
        exitOutOfCurrentWeapon=True,
        closeMenu=True,
        fullMenuClose=True,
    )
    restockDowns()
    nemesis.arenaSelect.arenaMenuSelect(4)

    FFXC.set_movement(-1, 0)
    memory.main.waitFrames(15)
    FFXC.set_movement(0, 1)
    memory.main.waitFrames(15)
    FFXC.set_neutral()
    returnToAirship()
    nemesis.menu.rikkuHaste()
    rinEquipDump()


def kilikaFinalShop():
    memory.main.awaitControl()
    rinEquipDump()
    nemesis.menu.autoSortEquipment()

    gilNeeded = 3500000 - memory.main.getGilvalue()
    weaponBuys = int(gilNeeded / 26150)
    weaponBuys += 1  # for safety

    airShipDestination(destNum=2)
    while not nemesis.targetPath.setMovement([-25, -246]):
        pass
    while not nemesis.targetPath.setMovement([-47, -209]):
        pass
    while not nemesis.targetPath.setMovement([-91, -199]):
        pass
    while not nemesis.targetPath.setMovement([-108, -169]):
        pass
    while memory.main.userControl():
        FFXC.set_movement(-1, 0)
        xbox.tapB()
    FFXC.set_neutral()  # Now talking to vendor
    memory.main.waitFrames(60)
    xbox.tapB()  # Intro dialog
    memory.main.waitFrames(60)
    xbox.tapB()  # Buy equipment
    memory.main.waitFrames(60)
    getEquipment(equip=True)  # Weapon for Tidus
    memory.main.waitFrames(60)
    xbox.tapDown()
    xbox.tapDown()
    xbox.tapDown()
    xbox.tapDown()
    xbox.tapDown()
    xbox.tapDown()
    xbox.tapDown()
    for x in range(weaponBuys):
        print("Buying armors, remaining - ", weaponBuys - x)
        memory.main.waitFrames(6)
        xbox.menuB()  # Purchase
        memory.main.waitFrames(6)
        xbox.menuUp()
        xbox.menuB()  # Confirm
        memory.main.waitFrames(6)
        xbox.menuB()  # Do not equip
    memory.main.waitFrames(6)
    memory.main.closeMenu()

    for y in range(weaponBuys):
        if y == 0:  # First one
            nemesis.menu.addAbility(
                owner=0,
                equipment_type=1,
                ability_array=[0x8072, 255, 255, 255],
                ability_index=0x8075,
                slotcount=4,
                navigateToEquipMenu=True,
                exitOutOfCurrentWeapon=True,
                closeMenu=False,
                fullMenuClose=False,
            )
        elif weaponBuys - y == 1:  # Last one
            nemesis.menu.addAbility(
                owner=0,
                equipment_type=1,
                ability_array=[0x8072, 255, 255, 255],
                ability_index=0x8075,
                slotcount=4,
                navigateToEquipMenu=True,
                exitOutOfCurrentWeapon=True,
                closeMenu=True,
                fullMenuClose=True,
            )
        else:
            nemesis.menu.addAbility(
                owner=0,
                equipment_type=1,
                ability_array=[0x8072, 255, 255, 255],
                ability_index=0x8075,
                slotcount=4,
                navigateToEquipMenu=False,
                exitOutOfCurrentWeapon=True,
                closeMenu=False,
                fullMenuClose=False,
            )

    while memory.main.userControl():
        FFXC.set_movement(-1, 0)
        xbox.tapB()
    FFXC.set_neutral()  # Now talking to vendor
    memory.main.waitFrames(60)
    xbox.tapB()  # Intro dialog
    memory.main.waitFrames(60)
    xbox.tapRight()
    xbox.tapB()  # Sell equipment
    nemesis.menu.sellAll()
    memory.main.closeMenu()

    while not nemesis.targetPath.setMovement([-91, -199]):
        pass
    while not nemesis.targetPath.setMovement([-47, -209]):
        pass
    while not nemesis.targetPath.setMovement([-25, -246]):
        pass
    while not nemesis.targetPath.setMovement([29, -252]):
        pass
    nemesis.menu.autoSortEquipment()
    returnToAirship()


def finalWeapon():
    arenaNPC()
    while memory.main.getItemCountSlot(memory.main.getItemSlot(53)) < 99:
        print("Trying to obtain Dark Matter for BDL weapon")
        nemesis.arenaSelect.arenaMenuSelect(4)
        arenaNPC()
    nemesis.arenaSelect.arenaMenuSelect(4)

    nemesis.menu.addAbility(
        owner=0,
        equipment_type=0,
        ability_array=[0x800B, 0x8000, 255, 255],
        ability_index=0x800D,
        slotcount=4,
        navigateToEquipMenu=True,
        exitOutOfCurrentWeapon=False,
        closeMenu=False,
        fullMenuClose=False,
    )
    nemesis.menu.addAbility(
        owner=0,
        equipment_type=0,
        ability_array=[0x800B, 0x8000, 0x800D, 255],
        ability_index=0x8019,
        slotcount=4,
        navigateToEquipMenu=False,
        exitOutOfCurrentWeapon=True,
        closeMenu=False,
        fullMenuClose=False,
    )
    # nemesis.menu.addAbility(owner=0, equipment_type=0, ability_array=[0x8064,255,255,255], ability_index=29, slotcount=4, navigateToEquipMenu=True, exitOutOfCurrentWeapon=False, closeMenu=False, fullMenuClose=False)
    # nemesis.menu.addAbility(owner=0, equipment_type=0, ability_array=[0x8064,0x800D,255,255], ability_index=33, slotcount=4, navigateToEquipMenu=True, exitOutOfCurrentWeapon=False, closeMenu=False, fullMenuClose=False)
    # nemesis.menu.addAbility(owner=0, equipment_type=0, ability_array=[0x8064,0x800D,0x800F,255], ability_index=35, slotcount=4, navigateToEquipMenu=False, exitOutOfCurrentWeapon=True, closeMenu=True, fullMenuClose=True)

    nemesis.menu.addAbility(
        owner=1,
        equipment_type=1,
        ability_array=[0x8072, 255, 255, 255],
        ability_index=0x800A,
        slotcount=4,
        navigateToEquipMenu=False,
        exitOutOfCurrentWeapon=True,
        closeMenu=True,
        fullMenuClose=True,
    )
    nemesis.menu.addAbility(
        owner=1,
        equipment_type=1,
        ability_array=[0x8072, 0x800A, 255, 255],
        ability_index=0x801D,
        slotcount=4,
        navigateToEquipMenu=True,
        exitOutOfCurrentWeapon=True,
        closeMenu=True,
        fullMenuClose=True,
    )
    memory.main.fullPartyFormat("kilikawoods1")


def rinEquipDump(buyWeapon=False):
    while not nemesis.targetPath.setMovement([-242, 298]):
        pass
    while not nemesis.targetPath.setMovement([-241, 211]):
        pass
    FFXC.set_movement(0, -1)
    while memory.main.userControl():
        pass
    while not nemesis.targetPath.setMovement([39, 53]):
        pass
    while memory.main.userControl():
        nemesis.targetPath.setMovement([28, 44])
        xbox.tapB()
    FFXC.set_neutral()
    memory.main.clickToDiagProgress(48)
    memory.main.waitFrames(10)
    xbox.tapB()
    memory.main.waitFrames(30)
    xbox.tapRight()
    xbox.menuB()

    nemesis.menu.sellAll()
    if buyWeapon:
        memory.main.waitFrames(60)
        xbox.menuRight()  # Removes any pop-ups
        memory.main.waitFrames(60)
        xbox.menuA()
        memory.main.waitFrames(60)
        xbox.menuLeft()
        memory.main.waitFrames(60)
        xbox.menuB()
        memory.main.waitFrames(60)
        xbox.menuB()
        memory.main.waitFrames(60)
        xbox.menuUp()
        memory.main.waitFrames(60)
        xbox.menuB()
        memory.main.waitFrames(60)
        xbox.menuUp()
        memory.main.waitFrames(60)
        xbox.menuB()
        memory.main.waitFrames(60)
    memory.main.closeMenu()
    memory.main.clickToControl3()
    while not nemesis.targetPath.setMovement([53, 110]):
        pass
    FFXC.set_movement(-1, -1)
    while memory.main.userControl():
        pass
    while not nemesis.targetPath.setMovement([-241, 223]):
        pass
    while not nemesis.targetPath.setMovement([-246, 329]):
        pass


def yojimboDialog():
    print("Clicking until dialog box")
    while memory.main.diagProgressFlag():
        xbox.tapB()
    print("Dialog box online.")
    memory.main.waitFrames(60)
    xbox.tapUp()
    xbox.tapB()
    memory.main.clickToDiagProgress(5)
    memory.main.waitFrames(12)
    xbox.tapLeft()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapLeft()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapB()
    memory.main.waitFrames(12)  # Eff it, just pay the man!
    # memory.clickToDiagProgress(5) #150,001
    # memory.waitFrames(12)
    # Xbox.tapDown()
    # Xbox.tapDown()
    # xbox.tapLeft()
    # xbox.tapDown()
    # xbox.tapDown()
    # xbox.tapB()
    # memory.waitFrames(12)
    # memory.clickToDiagProgress(5) #138,001
    # memory.waitFrames(12)
    # xbox.tapUp()
    # xbox.tapUp()
    # xbox.tapLeft()
    # xbox.tapUp()
    # xbox.tapUp()
    # xbox.tapUp()
    # xbox.tapUp()
    # xbox.tapB()
    # memory.waitFrames(12)
    # memory.clickToDiagProgress(5) #170,001
    # memory.waitFrames(12)
    # xbox.tapLeft()
    # xbox.tapUp()
    # xbox.tapUp()
    # xbox.tapB()
    print("Fayth accepts the contract.")
    xbox.nameAeon("Yojimbo")
    print("Naming complete.")


def yojimbo():
    checkpoint = 0
    while not memory.main.getMap() in [194, 374]:
        if memory.main.userControl():
            if checkpoint == 5:
                memory.main.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 9:
                memory.main.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 29 and memory.main.getCoords()[1] > 1800:
                checkpoint += 1
            elif checkpoint in [32, 35]:
                FFXC.set_neutral()
                memory.main.waitFrames(12)
                if checkpoint == 32:
                    FFXC.set_movement(0, 1)
                else:
                    FFXC.set_movement(0, -1)
                memory.main.waitFrames(2)
                FFXC.set_neutral()
                memory.main.waitFrames(12)
                xbox.tapB()
                checkpoint += 1
            elif checkpoint == 33:  # Talking to Fayth
                yojimboDialog()
                checkpoint += 1
            elif checkpoint == 39:
                memory.main.clickToEventTemple(3)
                checkpoint += 1
            elif checkpoint == 41:
                returnToAirship()
            elif (
                nemesis.targetPath.setMovement(nemesis.targetPath.yojimbo(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                battle.main.yojimbo()
                memory.main.clickToControl()
            elif checkpoint == 33:  # Talking to Fayth
                yojimboDialog()
                checkpoint += 1
            elif memory.main.diagSkipPossible():
                xbox.tapB()


def besaidFarm(capNum: int = 1):
    airShipDestination(destNum=1)
    nemesis.menu.removeAllNEA()

    memory.main.arenaFarmCheck(zone="besaid", endGoal=capNum, report=True)
    checkpoint = 0
    while not memory.main.getMap() in [194, 374]:
        if memory.main.userControl():
            if (
                memory.main.arenaFarmCheck(zone="besaid", endGoal=capNum, report=False)
                and checkpoint < 15
            ):
                checkpoint = 15
            elif checkpoint == 15 and not memory.main.arenaFarmCheck(
                zone="besaid", endGoal=capNum, report=False
            ):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)

            elif checkpoint == 1:
                memory.main.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 11:
                memory.main.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 16 and memory.main.getMap() == 20:
                checkpoint += 1
            elif checkpoint == 25:
                memory.main.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 26:
                returnToAirship()
            elif (
                nemesis.targetPath.setMovement(
                    nemesis.targetPath.besaidFarm(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                if capNum == 10:
                    battleFarmAll(yunaAttack=False)
                else:
                    battleFarmAll()
                memory.main.arenaFarmCheck(zone="besaid", endGoal=capNum, report=True)
            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()


def kilikaFarm(capNum: int = 1):
    airShipDestination(destNum=2)
    nemesis.menu.removeAllNEA()

    checkpoint = 0
    while not memory.main.getMap() in [194, 374]:
        if memory.main.userControl():
            if (
                memory.main.arenaFarmCheck(zone="kilika", endGoal=capNum, report=False)
                and checkpoint < 14
            ):
                checkpoint = 14
            elif checkpoint == 14 and not memory.main.arenaFarmCheck(
                zone="kilika", endGoal=capNum, report=False
            ):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)

            elif checkpoint == 4:
                memory.main.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 11:
                memory.main.clickToEventTemple(0)
                memory.main.arenaFarmCheck(zone="kilika", endGoal=10, report=True)
                checkpoint += 1
            elif checkpoint == 14 and memory.main.getMap() == 47:
                checkpoint += 1
            elif checkpoint == 21:
                memory.main.clickToEventTemple(3)
                checkpoint += 1
            elif checkpoint == 25:
                returnToAirship()
            elif (
                nemesis.targetPath.setMovement(
                    nemesis.targetPath.kilikaFarm(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                if capNum == 10:
                    battleFarmAll(yunaAttack=False)
                else:
                    battleFarmAll()
                memory.main.arenaFarmCheck(zone="kilika", endGoal=capNum, report=True)
            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()


def miihenNext(endGoal: int):
    next1 = rngTrack.comingBattles(area="mi'ihen_(newroad)", battleCount=2)[0]
    next2 = rngTrack.comingBattles(area="old_road", battleCount=2)[0]
    next3 = rngTrack.comingBattles(area="clasko_skip_screen", battleCount=2)[0]
    next4 = rngTrack.comingBattles(area="mrr_-_valley", battleCount=2)[0]
    next6 = rngTrack.comingBattles(area="mrr_-_precipice", battleCount=2)[0]
    farmArray1 = memory.main.arenaFarmCheck(
        zone="miihen", endGoal=endGoal, returnArray=True
    )
    farmArray2 = memory.main.arenaFarmCheck(
        zone="mrr", endGoal=endGoal, returnArray=True
    )

    if memory.main.getYunaMP() < 30:
        return 8
    if memory.main.arenaFarmCheck(zone="miihen", endGoal=endGoal):
        print("=======================")
        print("Next battles:")
        print(next4)
        print(next6)
        print(farmArray2)
        print("=======================")

        if memory.main.arenaFarmCheck(zone="mrr", endGoal=endGoal):
            return 9  # Ready to move on
        elif "garuda" in next6:
            return 6
        elif "garuda" in next4:
            return 5
        elif farmArray2[3] < endGoal and "lamashtu" in next4:
            return 5
        elif memory.main.getMap() == 128:
            return 6
        else:
            return 5

    print("=======================")
    print("Next battles:")
    print(next1)
    print(next2)
    print(next3)
    print(next4)
    print(farmArray1)
    print(farmArray2)
    print("=======================")

    if farmArray2[2] < endGoal and "garuda" in next4:
        return 4
    if farmArray1[0] < endGoal and "raldo" in next1:
        return 1
    if farmArray1[1] < endGoal and "mi'ihen_fang" in next1:
        return 1
    if farmArray1[7] < endGoal and "white_element" in next1:
        return 1
    if farmArray2[3] < endGoal and "lamashtu" in next4:
        return 4
    if farmArray1[2] < endGoal and "thunder_flan" in next2:
        return 2
    if farmArray1[2] < endGoal and "thunder_flan" in next3:
        return 3
    if farmArray1[3] < endGoal and "ipiria" in next2:
        return 2
    if farmArray1[3] < endGoal and "ipiria" in next3:
        return 3
    if farmArray1[4] < endGoal and "floating_eye" in next2:
        return 2
    if farmArray1[4] < endGoal and "floating_eye" in next3:
        return 3
    if farmArray1[5] < endGoal and "dual_horn" in next2:
        return 2
    if farmArray1[5] < endGoal and "dual_horn" in next3:
        return 3
    if farmArray1[6] < endGoal and "vouivre" in next2:
        return 2
    if farmArray1[6] < endGoal and "vouivre" in next3:
        return 3
    if farmArray1[8] < endGoal and "bomb" in next2:
        return 2
    if farmArray1[8] < endGoal and "bomb" in next3:
        return 3

    print("Couldn't find a special case")
    if memory.main.getMap() == 128:
        return 6
    if memory.main.getMap() == 92:
        if memory.main.arenaFarmCheck(zone="miihen", endGoal=endGoal):
            return 5
        else:
            return 4
    if memory.main.getMap() == 79:
        return 3
    if memory.main.getMap() == 116:
        return 2
    return 1


def miihenFarm(capNum: int = 1):
    airShipDestination(destNum=4)
    nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
    neArmor = True
    prefArea = miihenNext(endGoal=capNum)
    print("Next area: ", prefArea)
    memory.main.fullPartyFormat("initiative")

    checkpoint = 0
    lastCP = checkpoint
    while not memory.main.getMap() in [194, 374]:
        if memory.main.userControl():
            # Checkpoint notify
            if lastCP != checkpoint:
                print("Checkpoint reached: ", checkpoint)
                lastCP = checkpoint
            if checkpoint == 92:
                FFXC.set_neutral()
                while memory.main.userControl():
                    xbox.tapB()
                checkpoint = 144
            # Map changes
            if checkpoint == 2:
                memory.main.clickToEventTemple(4)
                checkpoint += 1
            if checkpoint == 8:
                memory.main.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 18 and memory.main.getMap() == 116:
                checkpoint += 1
            # Map between Miihen and MRR
            elif checkpoint in [31, 42, 72] and memory.main.getMap() == 59:
                checkpoint += 1
            elif checkpoint in [38, 39] and memory.main.getMap() == 116:  # Area 2 map
                checkpoint = 40
            elif checkpoint in [50, 63] and memory.main.getMap() == 79:  # Clasko map
                # FFXC.set_neutral()
                # memory.waitFrames(6)
                checkpoint += 1
            elif checkpoint == 60 and memory.main.getMap() == 92:  # MRR lower map
                checkpoint += 1
            elif checkpoint == 79 and memory.main.getMap() == 116:  # Highroad
                checkpoint = 29

            # Save Sphere / Exit logic
            if checkpoint in [47, 61, 62, 63, 164] and prefArea in [8, 9]:
                if prefArea == 8:
                    memory.main.touchSaveSphere()
                    prefArea = miihenNext(endGoal=capNum)
                    print("Next area: ", prefArea)
                else:
                    returnToAirship()

            # Farming logic
            elif checkpoint == 28 and prefArea == 1 and neArmor:
                nemesis.menu.removeAllNEA()
                miihenNext(endGoal=capNum)
                print("Next area: ", prefArea)
                neArmor = False
            elif checkpoint in [31, 80] and prefArea == 1:  # Farm in area 1
                checkpoint = 29
            elif checkpoint == 42 and prefArea == 2:  # Farm in area 2
                checkpoint = 40
            elif checkpoint in [53, 60, 72] and prefArea == 3:  # Farm in area 3
                checkpoint -= 2
            elif checkpoint == 63 and prefArea == 4:  # Farm in area 4
                checkpoint -= 2
            elif checkpoint == 33 and prefArea >= 3:  # Skip from zone 1 to zone >= 3
                checkpoint = 46
            elif checkpoint in [51, 52, 53] and prefArea <= 2:
                checkpoint = 72
            elif checkpoint == 77 and prefArea == 2:
                checkpoint = 34
            elif checkpoint in [48, 53] and prefArea >= 4 and not neArmor:
                nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
                neArmor = True
            elif checkpoint == 59 and prefArea in [4, 5] and neArmor:
                nemesis.menu.removeAllNEA()
                miihenNext(endGoal=capNum)
                print("Next area: ", prefArea)
                neArmor = False
            elif checkpoint in [63, 64] and prefArea in [1, 2] and not neArmor:
                nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
                neArmor = True
            elif checkpoint in [32, 42, 73] and prefArea in [1, 2, 3] and neArmor:
                nemesis.menu.removeAllNEA()
                miihenNext(endGoal=capNum)
                print("Next area: ", prefArea)
                neArmor = False
            elif checkpoint == 151 and not neArmor:
                nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
                neArmor = True

            # Garuda late farming logic
            elif checkpoint in [61, 62, 63] and prefArea >= 5:
                checkpoint = 100
            elif checkpoint in [104, 146, 158]:
                FFXC.set_neutral()
                memory.main.clickToEvent()
                checkpoint += 1
            elif (
                checkpoint > 99
                and checkpoint < 144
                and prefArea in [6, 8, 9]
                and not neArmor
            ):
                nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
                neArmor = True
            elif checkpoint > 99 and checkpoint >= 144 and prefArea == 6 and neArmor:
                nemesis.menu.removeAllNEA()
                miihenNext(endGoal=capNum)
                print("Next area: ", prefArea)
                neArmor = False
            elif checkpoint == 145 and prefArea == 5:
                checkpoint -= 2
                if neArmor:
                    nemesis.menu.removeAllNEA()
                    miihenNext(endGoal=capNum)
                    print("Next area: ", prefArea)
                    neArmor = False
            elif checkpoint == 150 and prefArea == 6:
                checkpoint -= 2
                if neArmor:
                    nemesis.menu.removeAllNEA()
                    miihenNext(endGoal=capNum)
                    print("Next area: ", prefArea)
                    neArmor = False

            elif checkpoint in [148, 149, 150] and prefArea == 5:
                checkpoint = 90
            # elif checkpoint == 94:
            #    checkpoint = 144

            elif (
                nemesis.targetPath.setMovement(
                    nemesis.targetPath.miihenFarm(checkpoint)
                )
                == True
            ):
                checkpoint += 1
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                if (
                    memory.main.getEncounterID() == 78
                    and memory.main.arenaArray()[34] == 10
                ):
                    battle.main.fleeAll()
                else:
                    if capNum == 10:
                        battleFarmAll(yunaAttack=False)
                    else:
                        battleFarmAll()
                prefArea = miihenNext(endGoal=capNum)
                print("Next area: ", prefArea)
                memory.main.fullPartyFormat("initiative")
            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()


def miihenFarm_old(capNum: int = 1):
    airShipDestination(destNum=4)
    if gameVars.neArmor() == 0:
        nemesis.menu.equipArmor(
            character=gameVars.neArmor(), ability=0x8056
        )  # Auto-Haste
    else:
        nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=99)  # Unequip

    checkpoint = 0
    while memory.main.getMap() != 79:
        if memory.main.userControl():
            # print(checkpoint)
            # if memory.getMap() == 171:
            #    if memory.getCoords()[0] > -2:
            #        FFXC.set_movement(-1,-1)
            #    else:
            #        FFXC.set_movement(-0.5,-1)
            if memory.main.arenaFarmCheck(
                zone="miihen1", endGoal=capNum, report=False
            ) and checkpoint in [28, 29]:
                checkpoint = 30
            elif checkpoint == 31 and not memory.main.arenaFarmCheck(
                zone="miihen1", endGoal=capNum, report=False
            ):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)

            elif checkpoint == 2:
                memory.main.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 8:
                memory.main.clickToEventTemple(0)
                checkpoint += 1
                memory.main.arenaFarmCheck(zone="miihen1", endGoal=capNum, report=True)
            elif checkpoint == 18 and memory.main.getMap() == 116:
                checkpoint += 1
            elif checkpoint in [31, 42] and memory.main.getMap() == 59:
                checkpoint += 1
            elif checkpoint in [34, 47]:
                memory.main.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 39:
                memory.main.clickToEventTemple(4)
                checkpoint += 1
            elif (
                memory.main.arenaFarmCheck(zone="miihen2", endGoal=capNum, report=False)
                and checkpoint < 41
            ):
                checkpoint = 41
            elif checkpoint == 42 and not memory.main.arenaFarmCheck(
                zone="miihen2", endGoal=capNum, report=False
            ):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)
            elif checkpoint == 50:
                memory.main.clickToEventTemple(0)
                checkpoint += 1

            elif (
                nemesis.targetPath.setMovement(
                    nemesis.targetPath.miihenFarm(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                if (
                    memory.main.getEncounterID() == 78
                    and memory.main.arenaArray()[34] == 10
                ):
                    battle.main.fleeAll()
                else:
                    if capNum == 10:
                        battleFarmAll(yunaAttack=False)
                    else:
                        battleFarmAll()

                if checkpoint < 32:
                    memory.main.arenaFarmCheck(
                        zone="miihen1", endGoal=capNum, report=True
                    )
                else:
                    memory.main.arenaFarmCheck(
                        zone="miihen2", endGoal=capNum, report=True
                    )
            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()


def mrrFarm(capNum: int = 1):
    print("No longer used, now a part of the Mi'ihen farm")


def mrrFarm_old(capNum: int = 1):
    # Unlike other sections, MRR is expected to zone in from the Mi'ihen area and not the airship.
    nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
    while not nemesis.targetPath.setMovement([-45, -733]):  # Close to magus sisters
        pass
    while not nemesis.targetPath.setMovement([-61, -692]):  # Past magus sisters
        pass
    while not nemesis.targetPath.setMovement([-19, -528]):  # Through Clasko trigger
        pass
    while not nemesis.targetPath.setMovement([-145, -460]):  # Past O'aka's spot
        pass
    while not nemesis.targetPath.setMovement([-219, -408]):  # Past O'aka's spot
        pass
    while memory.main.getMap() != 92:
        FFXC.set_movement(1, 1)

    # OK now ready to do farming.
    nemesis.menu.removeAllNEA()
    memory.main.arenaFarmCheck(zone="mrr", endGoal=capNum, report=True)
    checkpoint = 0
    while not memory.main.getMap() in [194, 374]:
        if memory.main.userControl():
            if (
                memory.main.arenaFarmCheck(zone="mrr", endGoal=capNum, report=False)
                and checkpoint < 2
            ):
                checkpoint = 2
            elif checkpoint == 3 and not memory.main.arenaFarmCheck(
                zone="mrr", endGoal=capNum, report=False
            ):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)

            elif checkpoint == 4:
                returnToAirship()
            elif (
                nemesis.targetPath.setMovement(nemesis.targetPath.mrrFarm(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                if capNum == 10:
                    battleFarmAll(yunaAttack=False)
                else:
                    battleFarmAll()
                memory.main.arenaFarmCheck(zone="mrr", endGoal=capNum, report=True)
            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()


def djoseNext(endGoal: int):
    next1 = rngTrack.comingBattles(area="djose_highroad_(back_half)", battleCount=2)[0]
    next2 = rngTrack.comingBattles(area="moonflow_(south)", battleCount=2)[0]
    farmArray = memory.main.arenaFarmCheck(
        zone="djose", endGoal=endGoal, returnArray=True
    )

    print("=======================")
    print("Next battles:")
    print(next1)
    print(next2)
    print(farmArray)
    print("=======================")

    if memory.main.getYunaMP() < 30:
        return 3
    if farmArray[3] < endGoal and "simurgh" in next1:
        return 1
    if farmArray[6] < endGoal and "ochu" in next2:
        return 2
    if farmArray[4] < endGoal and "bite_bug" in next2:
        return 2
    if farmArray[4] < endGoal and "bite_bug" in next1:
        return 1
    if farmArray[5] < endGoal and "basilisk" in next1:
        return 1
    if farmArray[2] < endGoal and "snow_flan" in next1:
        return 1
    if farmArray[2] < endGoal and "snow_flan" in next2:
        return 2
    if farmArray[1] < endGoal and "garm" in next1:
        return 1
    if farmArray[1] < endGoal and "garm" in next2:
        return 2
    if farmArray[0] < endGoal and "bunyip_2" in next1:
        return 1
    if farmArray[0] < endGoal and "bunyip_2" in next2:
        return 2
    if memory.main.arenaFarmCheck(zone="djose", endGoal=endGoal):
        return 4
    print("Couldn't find a special case")
    return 1


def djoseFarm(capNum: int = 10):
    rinEquipDump()
    airShipDestination(destNum=5)
    nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
    neArmor = True
    prefArea = djoseNext(endGoal=capNum)
    print("Next area: ", prefArea)
    memory.main.fullPartyFormat("initiative")

    checkpoint = 0
    lastCP = 0
    while not memory.main.getMap() in [194, 374]:
        if lastCP != checkpoint:
            print("Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        if memory.main.userControl():
            # Map changes
            if checkpoint in [7, 27, 45] and memory.main.getMap() == 93:
                checkpoint += 1
            elif checkpoint == 24 and memory.main.getMap() == 75:
                checkpoint += 1
            elif checkpoint in [30, 39] and memory.main.getMap() == 76:
                checkpoint += 1
            elif checkpoint == 35 and memory.main.getMap() == 82:
                checkpoint += 1
            # Reset/End logic
            elif checkpoint == 37:
                if prefArea == 3:
                    memory.main.touchSaveSphere()
                    checkpoint += 1
                else:
                    returnToAirship()

            # Farming logic
            if prefArea in [3, 4] and not neArmor:
                nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
                neArmor = True
            elif checkpoint in [21, 45] and prefArea == 1 and neArmor:
                nemesis.menu.removeAllNEA()
                neArmor = False
            elif checkpoint == 25 and neArmor:
                nemesis.menu.removeAllNEA()
                neArmor = False
            elif checkpoint in [24, 28] and prefArea == 1:
                checkpoint = 22
            elif checkpoint == 27 and prefArea == 2:
                checkpoint -= 2
            elif checkpoint in [22, 23] and prefArea != 1:
                if prefArea == 2:
                    checkpoint = 24
                else:
                    checkpoint = 28
            elif checkpoint in [25, 26] and prefArea != 2:
                checkpoint = 27
            elif checkpoint == 47:
                checkpoint = 21

            elif (
                nemesis.targetPath.setMovement(nemesis.targetPath.djoseFarm(checkpoint))
                == True
            ):
                checkpoint += 1
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                battleFarmAll(yunaAttack=False)
                if memory.main.getHP()[0] < 800:
                    battle.main.healUp(3)
                prefArea = djoseNext(endGoal=capNum)
                print("Next area:", prefArea)
            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()


def plainsNext(endGoal: int):
    next1 = rngTrack.comingBattles(
        area="thunder_plains_(north)_(1_stone)", battleCount=2
    )[0]
    next2 = rngTrack.comingBattles(
        area="thunder_plains_(south)_(2_stones)", battleCount=2
    )[0]
    farmArray = memory.main.arenaFarmCheck(
        zone="tplains", endGoal=endGoal, returnArray=True
    )

    print("=======================")
    print("Next battles:")
    print(next1)
    print(next2)
    print(farmArray)
    print("=======================")

    if memory.main.getYunaMP() < 30:
        return 4
    if farmArray[5] < endGoal and "iron_giant" in next1:
        return 1
    if farmArray[5] < endGoal and "iron_giant" in next2:
        return 2
    if farmArray[6] < endGoal and "qactuar" in next1:
        return 1
    if farmArray[6] < endGoal and "qactuar" in next2:
        return 2
    if farmArray[1] < endGoal and "melusine" in next1:
        return 1
    if farmArray[1] < endGoal and "melusine" in next2:
        return 2
    if farmArray[7] < endGoal and "larva" in next1:
        return 1
    if farmArray[7] < endGoal and "larva" in next2:
        return 2
    if farmArray[4] < endGoal and "gold_element" in next1:
        return 1
    if farmArray[4] < endGoal and "gold_element" in next2:
        return 2
    if farmArray[2] < endGoal and "buer" in next1:
        return 1
    if farmArray[2] < endGoal and "buer" in next2:
        return 2
    if farmArray[3] < endGoal and "kusariqqu" in next1:
        return 1
    if farmArray[3] < endGoal and "kusariqqu" in next2:
        return 2
    if farmArray[0] < endGoal and "aerouge" in next1:
        return 1
    if farmArray[0] < endGoal and "aerouge" in next2:
        return 2
    if memory.main.getYunaMP() < 30:
        return 3
    if memory.main.arenaFarmCheck(zone="tplains", endGoal=endGoal):
        return 4
    print("Couldn't find a special case")
    if memory.main.getMap() == 162:
        return 1
    else:
        return 2


def tPlains(capNum: int = 1, autoHaste: bool = False):
    rinEquipDump()
    airShipDestination(destNum=8)
    nemesis.menu.removeAllNEA()
    prefArea = plainsNext(endGoal=capNum)
    print("Next area: ", prefArea)
    neEquip = False

    checkpoint = 0
    while not memory.main.getMap() in [194, 374]:
        if memory.main.userControl():
            if memory.main.dodgeLightning(gameVars.getLStrike()):
                print("Strike!")
                gameVars.setLStrike(memory.main.lStrikeCount())
            if prefArea in [3, 4] and not neEquip:
                nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
                neEquip = True
                if checkpoint in [4, 5]:
                    checkpoint = 6
                if checkpoint in [9, 10]:
                    checkpoint = 11
            elif checkpoint in [8, 12] and prefArea in [3, 4]:
                checkpoint = 20
                print("Back to agency", checkpoint)
            elif checkpoint in [6, 14, 15, 16] and prefArea == 1:
                checkpoint = 4
                print("Backtrack: ", checkpoint)
            elif checkpoint == 11 and prefArea == 2:
                checkpoint -= 2
                print("Backtrack: ", checkpoint)
            elif checkpoint in [4, 5] and prefArea == 2:
                checkpoint = 6
                print("Forward: ", checkpoint)
            elif checkpoint in [9, 10] and prefArea == 1:
                checkpoint = 11
                print("Forward: ", checkpoint)
            # From start, can go straight to south.
            elif checkpoint == 2 and prefArea == 2:
                checkpoint = 7
                print("Direct to South: ", checkpoint)

            # Map changes:
            if checkpoint in [1, 6, 11] and memory.main.getMap() == 256:
                checkpoint += 1
                print("Map change: ", checkpoint)
            if checkpoint in [3, 13] and memory.main.getMap() == 162:
                checkpoint += 1
                print("Map change: ", checkpoint)
            if checkpoint == 8 and memory.main.getMap() == 140:
                checkpoint += 1
                print("Map change: ", checkpoint)
            if checkpoint == 21 and memory.main.getMap() == 263:
                checkpoint += 1
                print("Map change: ", checkpoint)
            if checkpoint == 23:
                if prefArea == 3:
                    memory.main.touchSaveSphere()
                    nemesis.menu.removeAllNEA()
                    neEquip = False
                    prefArea = plainsNext(endGoal=capNum)
                    print("Next area: ", prefArea)
                    checkpoint = 0
                else:
                    returnToAirship()

            # General pathing
            elif (
                nemesis.targetPath.setMovement(nemesis.targetPath.tpFarm(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                if capNum == 10:
                    battleFarmAll(yunaAttack=False)
                else:
                    battleFarmAll()
                battle.main.healUp(3)
                prefArea = plainsNext(endGoal=capNum)
                print("Next area:", prefArea)
                memory.main.arenaFarmCheck(zone="tPlains", endGoal=capNum, report=True)
            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()
    print("End of Thunder Plains section")
    return memory.main.arenaFarmCheck(zone="tPlains", endGoal=capNum, report=False)


def tPlains_Old(capNum: int = 1, autoHaste: bool = False):
    rinEquipDump()
    airShipDestination(destNum=8)
    nemesis.menu.removeAllNEA()

    checkpoint = 0
    while not memory.main.getMap() in [194, 374]:
        if memory.main.userControl():
            if memory.main.dodgeLightning(gameVars.getLStrike()):
                print("Strike!")
                gameVars.setLStrike(memory.main.lStrikeCount())
            elif (
                memory.main.arenaFarmCheck(zone="tPlains", endGoal=capNum, report=False)
                and checkpoint < 8
            ):
                nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
                checkpoint = 8
            elif memory.main.getYunaMP() < 30 and checkpoint < 8:
                checkpoint = 8
            elif (
                checkpoint == 9
                and not memory.main.arenaFarmCheck(
                    zone="tPlains", endGoal=capNum, report=False
                )
                and memory.main.getYunaMP() >= 30
            ):
                checkpoint -= 2

            # Map changes:
            elif checkpoint == 1 and memory.main.getMap() == 256:
                checkpoint += 1
            elif checkpoint == 3 and memory.main.getMap() == 162:
                checkpoint += 1
            elif checkpoint == 11 and memory.main.getMap() == 256:
                checkpoint += 1
            elif checkpoint == 14:
                memory.main.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 16:
                returnToAirship()

            # General pathing
            elif (
                nemesis.targetPath.setMovement(nemesis.targetPath.tpFarm(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                if capNum == 10:
                    battleFarmAll(yunaAttack=False)
                else:
                    battleFarmAll()
                memory.main.arenaFarmCheck(zone="tPlains", endGoal=capNum, report=True)
            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()
    print("End of Thunder Plains section")
    return memory.main.arenaFarmCheck(zone="tPlains", endGoal=capNum, report=False)


def woodsNext(endGoal: int):
    next1 = rngTrack.comingBattles(area="lake_macalania", battleCount=2)[0]
    next2 = rngTrack.comingBattles(area="macalania_woods", battleCount=2)[0]
    farmArray1 = memory.main.arenaFarmCheck(
        zone="maclake", endGoal=endGoal, returnArray=True
    )
    farmArray2 = memory.main.arenaFarmCheck(
        zone="macwoods", endGoal=endGoal, returnArray=True
    )

    print("=======================")
    print("Next battles:")
    print(next1)
    print(next2)
    print(farmArray1)
    print(farmArray2)
    print("=======================")

    if memory.main.getYunaMP() < 30:
        return 4
    if farmArray2[4] < endGoal and "chimera" in next2:
        return 2
    if farmArray2[5] < endGoal and "xiphos" in next2:
        return 2
    if farmArray1[3] < endGoal and "evil_eye" in next1:
        return 1
    if farmArray1[0] < endGoal and "mafdet" in next1:
        return 1
    if memory.main.getYunaMP() < 30:
        return 3
    if memory.main.arenaFarmCheck(
        zone="maclake", endGoal=endGoal
    ) and memory.main.arenaFarmCheck(zone="macwoods", endGoal=endGoal):
        return 4
    print("Couldn't find a special case")
    return 2


def macWoods(capNum: int = 10):
    airShipDestination(destNum=9)
    nemesis.menu.removeAllNEA()
    prefArea = woodsNext(endGoal=capNum)
    print("Next area: ", prefArea)

    checkpoint = 0
    while not memory.main.getMap() in [194, 374]:
        if memory.main.userControl():
            if prefArea in [3, 4]:
                if checkpoint in [4, 5]:
                    checkpoint = 6
                elif checkpoint in [12, 13]:
                    checkpoint = 14
            elif checkpoint in [4, 5] and prefArea != 1:
                checkpoint = 6
            elif checkpoint in [6, 20] and prefArea == 1:
                checkpoint = 4
            elif checkpoint in [14] and prefArea == 2:
                checkpoint = 12

            # Map changes:
            if checkpoint in [2, 19] and memory.main.getMap() == 164:
                checkpoint += 1
            elif checkpoint in [6, 14] and memory.main.getMap() == 221:
                checkpoint += 1
            elif checkpoint == 11 and memory.main.getMap() == 242:
                checkpoint += 1
            elif checkpoint in [10, 15] and prefArea in [3, 4]:
                if prefArea == 3:
                    memory.main.touchSaveSphere()
                    prefArea = woodsNext(endGoal=capNum)
                    print("Next area: ", prefArea)
                    if prefArea == 1:
                        checkpoint = 15
                    else:
                        checkpoint = 10
                else:
                    returnToAirship()

            # General pathing
            elif (
                nemesis.targetPath.setMovement(nemesis.targetPath.macFarm(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                battleFarmAll(yunaAttack=False)
                prefArea = woodsNext(endGoal=capNum)
                print("Next area: ", prefArea)
            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()


def macWoods_old(capNum: int = 10):
    airShipDestination(destNum=9)
    nemesis.menu.removeAllNEA()

    checkpoint = 0
    while not memory.main.getMap() in [194, 374]:
        if memory.main.userControl():
            if (
                memory.main.arenaFarmCheck(zone="macLake", endGoal=capNum, report=False)
                and checkpoint < 6
            ):
                checkpoint = 6
            elif checkpoint == 6 and not memory.main.arenaFarmCheck(
                zone="macLake", endGoal=capNum, report=False
            ):
                checkpoint -= 2
            if (
                memory.main.arenaFarmCheck(
                    zone="macWoods", endGoal=capNum, report=False
                )
                and checkpoint < 14
            ):
                checkpoint = 14
            elif checkpoint == 14 and not memory.main.arenaFarmCheck(
                zone="macWoods", endGoal=capNum, report=False
            ):
                checkpoint -= 2

            # Map changes:
            elif checkpoint == 2:
                memory.main.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 6 and memory.main.getMap() == 221:
                checkpoint += 1
            elif checkpoint == 11 and memory.main.getMap() == 242:
                checkpoint += 1
            elif checkpoint == 14 and memory.main.getMap() == 221:
                checkpoint += 1
            elif checkpoint == 15:
                returnToAirship()

            # General pathing
            elif (
                nemesis.targetPath.setMovement(nemesis.targetPath.macFarm(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                battleFarmAll(yunaAttack=False)
                if checkpoint < 7:
                    memory.main.arenaFarmCheck(
                        zone="macLake", endGoal=capNum, report=True
                    )
                else:
                    memory.main.arenaFarmCheck(
                        zone="macWoods", endGoal=capNum, report=True
                    )
            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()


def bikanelNext(endGoal: int):
    next1 = rngTrack.comingBattles(area="sanubia_desert_(central)", battleCount=1)[0]
    next2 = rngTrack.comingBattles(area="sanubia_desert_(ruins)", battleCount=1)[0]
    next3 = rngTrack.comingBattles(area="sanubia_desert_(west)", battleCount=1)[0]
    farmArray = memory.main.arenaFarmCheck(
        zone="bikanel", endGoal=endGoal, returnArray=True
    )

    print("=======================")
    print("Next three battles:")
    print(next1)
    print(next2)
    print(next3)
    print("=======================")

    if memory.main.getYunaMP() < 30:
        return 4
    if farmArray[5] < endGoal and "cactuar" in next1:
        return 1
    if farmArray[5] < endGoal and "cactuar" in next2:
        return 2
    if farmArray[5] < endGoal and "cactuar" in next3:
        return 3
    if farmArray[4] < endGoal and "mushussu" in next1:
        return 1
    if farmArray[4] < endGoal and "mushussu" in next3:
        return 3
    if farmArray[3] < endGoal and "sand_worm" in next1:
        return 1
    if farmArray[3] < endGoal and "sand_worm" in next2:
        return 2
    if farmArray[3] < endGoal and "sand_worm" in next3:
        return 3
    if farmArray[2] < endGoal and "zu" in next1:
        return 1
    if farmArray[2] < endGoal and "zu" in next2:
        return 2
    if farmArray[2] < endGoal and "zu" in next3:
        return 3
    if farmArray[0] < endGoal and "sand_wolf" in next1:
        return 1
    if farmArray[0] < endGoal and "sand_wolf" in next2:
        return 2
    if farmArray[0] < endGoal and "sand_wolf" in next3:
        return 3
    if memory.main.arenaFarmCheck(zone="bikanel", endGoal=endGoal):
        return 4

    print("Could not find a desirable encounter.")
    if memory.main.getMap() == 138:
        return 3
    else:
        return 1  # Prefer zone 1 for remaining battles.


def bikanel(capNum: int = 10):
    airShipDestination(destNum=10)
    nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
    neArmor = True
    prefArea = bikanelNext(endGoal=capNum)
    print("Next area: ", prefArea)
    memory.main.fullPartyFormat("initiative")

    checkpoint = 0
    while not memory.main.getMap() in [194, 374]:
        if memory.main.userControl():
            # NEA stuff
            if prefArea == 4 and not neArmor:
                nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
                neArmor = True
            elif checkpoint in [27, 28] and prefArea != 1:
                checkpoint = 29
            elif checkpoint in [28, 29, 30] and prefArea in [1, 2] and neArmor:
                nemesis.menu.removeAllNEA()
                bikanelNext(endGoal=capNum)
                neArmor = False
            elif checkpoint < 33 and prefArea == 3 and not neArmor:
                nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
                neArmor = True
            elif checkpoint in [34, 35] and prefArea == 3 and neArmor:
                nemesis.menu.removeAllNEA()
                bikanelNext(endGoal=capNum)
                neArmor = False
            elif checkpoint in [34, 35] and prefArea != 3 and not neArmor:
                nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
                checkpoint = 36
                neArmor = True
            elif checkpoint == 40 and prefArea != 4:
                nemesis.menu.removeAllNEA()
                bikanelNext(endGoal=capNum)
                neArmor = False
                if prefArea == 1:
                    checkpoint = 28
                else:
                    checkpoint = 29

            # Checkpoint updates
            if prefArea == 1 and checkpoint in [29, 30]:
                checkpoint -= 2
            elif prefArea == 2 and checkpoint == 31:
                checkpoint -= 2
            elif prefArea == 3 and checkpoint == 36:
                checkpoint -= 2
            # Skip running into the next area. Straight to save sphere.
            elif prefArea == 4 and checkpoint < 31:
                checkpoint = 40

            # Map changes:
            if checkpoint == 5 and memory.main.getMap() == 136:
                checkpoint += 1
            elif checkpoint in [22, 36] and memory.main.getMap() == 137:
                checkpoint += 1
            elif checkpoint == 33 and memory.main.getMap() == 138:
                checkpoint += 1
            elif checkpoint == 44:
                returnToAirship()

            # General pathing
            elif (
                nemesis.targetPath.setMovement(
                    nemesis.targetPath.bikanelFarm(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                battleFarmAll(yunaAttack=False)
                memory.main.arenaFarmCheck(zone="bikanel", endGoal=capNum, report=True)
                hpCheck = memory.main.getHP()
                if hpCheck[0] < 800:
                    battle.main.healUp(3)
                prefArea = bikanelNext(endGoal=capNum)
                print("Next area: ", prefArea)
            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()
    initArray = memory.main.checkAbility(ability=0x8002)
    if initArray[4]:
        nemesis.menu.equipWeapon(character=4, ability=0x8002)  # Initiative
        memory.main.fullPartyFormat("initiative")


def calmNext(endGoal: int, forceLevels: int):
    next1 = rngTrack.comingBattles(area="calm_lands_(south)", battleCount=1)[0]
    next2 = rngTrack.comingBattles(
        area="calm_lands_(central-north-east)", battleCount=1
    )[0]
    next3 = rngTrack.comingBattles(area="calm_lands_(north-west)", battleCount=1)[0]
    farmArray = memory.main.arenaFarmCheck(
        zone="calm", endGoal=endGoal, returnArray=True
    )

    print("=======================")
    print("Next three battles:")
    print(next1)
    print(next2)
    print(next3)
    print("=======================")

    if memory.main.getYunaMP() < 30:
        return 4
    if farmArray[4] < endGoal and "malboro" in next2:
        return 2
    if farmArray[4] < endGoal and "malboro" in next3:
        return 3
    if farmArray[0] < endGoal and "shred" in next1:
        return 1
    if farmArray[0] < endGoal and "shred" in next2:
        return 2
    if farmArray[0] < endGoal and "shred" in next3:
        return 3
    if farmArray[8] < endGoal and "anacondaur" in next1:
        return 1
    if farmArray[8] < endGoal and "anacondaur" in next2:
        return 2
    if farmArray[8] < endGoal and "anacondaur" in next3:
        return 3
    if farmArray[5] < endGoal and "ogre" in next1:
        return 1
    if farmArray[5] < endGoal and "ogre" in next2:
        return 2
    if farmArray[5] < endGoal and "ogre" in next3:
        return 3
    if farmArray[6] < endGoal and "chimera_brain" in next1:
        return 1
    if farmArray[6] < endGoal and "chimera_brain" in next2:
        return 2
    if farmArray[6] < endGoal and "chimera_brain" in next3:
        return 3
    if farmArray[7] < endGoal and "coeurl" in next1:
        return 1
    if farmArray[7] < endGoal and "coeurl" in next2:
        return 2
    if farmArray[7] < endGoal and "coeurl" in next3:
        return 3
    if memory.main.arenaFarmCheck(zone="calm", endGoal=endGoal):
        if memory.main.getYunaMP() < 30:
            return 9
        if forceLevels > gameVars.nemCheckpointAP():
            print("== Area complete, but need more levels ==")
            # Need extra AP to reach Quick Attack
            # Overdrive > AP gives us the most per kill.
            if len(next3) > len(next2) and len(next3) > len(next1):
                return 3
            if len(next1) > len(next2) and len(next1) > len(next3):
                return 1
            return 2
        return 9
    return 2


def calm(capNum: int = 1, autoHaste=False, airshipReturn=True, forceLevels=0):
    airShipDestination(destNum=12)
    nemesis.menu.removeAllNEA()
    neArmor = False
    prefArea = calmNext(endGoal=capNum, forceLevels=forceLevels)
    print("Next area: ", prefArea)

    neArmor = False

    checkpoint = 0
    while not memory.main.getMap() == 307:
        if memory.main.userControl():
            if not neArmor and prefArea == 9:
                nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
                neArmor = True
            elif prefArea == 9 and not neArmor:
                nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
                neArmor = True

            if prefArea == 1 and checkpoint in [4, 5, 10]:
                checkpoint = 2
            elif prefArea in [2, 3, 4, 5, 6] and prefArea == 9:
                checkpoint = 10
            elif prefArea == 2 and checkpoint == 9:
                checkpoint = 4
            elif prefArea == 3 and checkpoint == 8:
                checkpoint = 6
            elif checkpoint in [6, 7] and prefArea != 3:
                checkpoint = 8
            elif checkpoint == 10:  # Ride the bird back to arena
                arenaReturn(checkpoint=1)

            elif (
                nemesis.targetPath.setMovement(nemesis.targetPath.calmFarm(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            allCounts = memory.main.arenaArray()
            if memory.main.battleActive():
                if (
                    memory.main.getEncounterID() == 281
                    and gameVars.nemCheckpointAP() < 8
                ):
                    if min(allCounts[13], allCounts[19]) >= capNum:
                        battle.main.fleeAll()
                    else:
                        battleFarmAll()
                elif (
                    memory.main.getEncounterID() == 283
                    and gameVars.nemCheckpointAP() < 8
                ):
                    if min(allCounts[4], allCounts[19], allCounts[33]) >= capNum:
                        battle.main.fleeAll()
                    else:
                        battleFarmAll()
                elif (
                    memory.main.getEncounterID() == 284
                    and allCounts[33] >= capNum
                    and gameVars.nemCheckpointAP() < 8
                ):
                    battle.main.fleeAll()
                else:
                    if capNum == 10:
                        battleFarmAll(yunaAttack=False)
                    else:
                        battleFarmAll()
                battle.main.healUp(3)
                prefArea = calmNext(endGoal=capNum, forceLevels=forceLevels)
                print("Next area: ", prefArea)
                memory.main.arenaFarmCheck(zone="calm", endGoal=capNum, report=True)

            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()
    if airshipReturn:
        returnToAirship()
    if forceLevels > gameVars.nemCheckpointAP():
        return False
    return memory.main.arenaFarmCheck(zone="calm", endGoal=capNum, report=False)


def calm_old(capNum: int = 1, autoHaste=False, airshipReturn=True):
    airShipDestination(destNum=12)
    nemesis.menu.removeAllNEA()

    neArmor = False

    checkpoint = 0
    while not memory.main.getMap() == 307:
        if memory.main.userControl():
            if not neArmor and memory.main.getYunaMP() < 30:
                nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
                neArmor = True
            if (
                memory.main.arenaFarmCheck(zone="calm", endGoal=capNum, report=False)
                and checkpoint < 5
            ):
                checkpoint = 5
            elif checkpoint == 5 and not memory.main.arenaFarmCheck(
                zone="calm", endGoal=capNum, report=False
            ):
                checkpoint -= 2
            elif memory.main.arenaFarmCheck(
                zone="calm2", endGoal=capNum, report=False
            ) and checkpoint in [8, 9]:
                checkpoint = 10
            elif checkpoint == 10 and not memory.main.arenaFarmCheck(
                zone="calm2", endGoal=capNum, report=False
            ):
                checkpoint -= 2
            elif (
                nemesis.targetPath.setMovement(nemesis.targetPath.calm(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            allCounts = memory.main.arenaArray()
            if memory.main.battleActive():
                if (
                    memory.main.getEncounterID() == 281
                    and gameVars.nemCheckpointAP() < 8
                ):
                    if min(allCounts[13], allCounts[19]) >= capNum:
                        battle.main.fleeAll()
                    else:
                        battleFarmAll()
                elif (
                    memory.main.getEncounterID() == 283
                    and gameVars.nemCheckpointAP() < 8
                ):
                    if min(allCounts[4], allCounts[19], allCounts[33]) >= capNum:
                        battle.main.fleeAll()
                    else:
                        battleFarmAll()
                elif (
                    memory.main.getEncounterID() == 284
                    and allCounts[33] >= capNum
                    and gameVars.nemCheckpointAP() < 8
                ):
                    battle.main.fleeAll()
                else:
                    if capNum == 10:
                        battleFarmAll(yunaAttack=False)
                    else:
                        battleFarmAll()
                battle.main.healUp(3)
                if checkpoint < 6:
                    memory.main.arenaFarmCheck(zone="calm", endGoal=capNum, report=True)
                else:
                    memory.main.arenaFarmCheck(
                        zone="calm2", endGoal=capNum, report=True
                    )

            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()
    if not memory.main.arenaFarmCheck(zone="calm3", endGoal=capNum, report=False):
        returnToAirship()
    elif airshipReturn:
        returnToAirship()
    return memory.main.arenaFarmCheck(zone="calm3", endGoal=capNum, report=False)


def gagazetNext(endGoal: int):
    next1 = rngTrack.comingBattles(area="gagazet_(mountain)", battleCount=2)[0]
    next2 = rngTrack.comingBattles(area="gagazet_(cave)", battleCount=2)[0]
    next3 = rngTrack.comingBattles(area="zanarkand_(overpass)", battleCount=2)[0]
    next4 = rngTrack.comingBattles(area="gagazet_(underwater)", battleCount=2)[0]
    farmArray = memory.main.arenaFarmCheck(
        zone="gagazet", endGoal=endGoal, returnArray=True
    )

    print("=======================")
    print("Next battles:")
    print(next1)
    print(next2)
    print(next3)
    print(next4)
    print(farmArray)
    print("=======================")

    if memory.main.getYunaMP() < 30:
        return 8
    if farmArray[0] < endGoal and "bandersnatch" in next2:
        return 2
    if farmArray[0] < endGoal and "bandersnatch" in next1:
        return 1
    if farmArray[9] < endGoal and "behemoth" in next2:
        return 2
    if farmArray[9] < endGoal and "behemoth" in next3:
        return 3
    if farmArray[1] < endGoal and "dark_flan" in next2:
        return 2
    if farmArray[1] < endGoal and "dark_flan" in next3:
        return 3
    if farmArray[10] < endGoal and "mandragora" in next2:
        return 2
    if farmArray[10] < endGoal and "mandragora" in next3:
        return 3
    if farmArray[6] < endGoal and "grendel" in next2:
        return 2
    if farmArray[6] < endGoal and "grendel" in next3:
        return 3
    if farmArray[2] < endGoal and "ahriman" in next2:
        return 2
    if farmArray[2] < endGoal and "ahriman" in next3:
        return 3
    if farmArray[7] < endGoal and "bashura" in next2:
        return 2
    if farmArray[7] < endGoal and "bashura" in next3:
        return 3
    if farmArray[11] < endGoal and "grenade" in next1:
        return 1
    if farmArray[3] < endGoal and "grat" in next1:
        return 1
    if farmArray[4] < endGoal and "achelous" in next4:
        return 4
    if farmArray[5] < endGoal and "maelspike" in next4:
        return 4
    if farmArray[8] < endGoal and "maelspike" in next4:
        return 4
    if farmArray[4] < endGoal and "splasher_3" in next4:
        return 4
    if memory.main.arenaFarmCheck(zone="gagazet", endGoal=endGoal):
        return 9
    print("Couldn't find a special case")
    if memory.main.getMap() == 225:
        return 3
    elif memory.main.getMap() == 244:
        return 1
    elif memory.main.getMap() == 310:
        return 4
    else:
        return 2


def gagazet(capNum: int = 10):
    rinEquipDump()
    airShipDestination(destNum=13)
    prefArea = gagazetNext(endGoal=capNum)
    if prefArea == 4:
        nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
        neArmor = True
    else:
        nemesis.menu.removeAllNEA()
        neArmor = False
    print("Next area: ", prefArea)

    lastCP = 0
    checkpoint = 0
    while not memory.main.getMap() in [194, 374]:
        if lastCP != checkpoint:
            print("+++ Checkpoint reached: ", checkpoint)
            lastCP = checkpoint
        if memory.main.userControl():
            # Map changes
            if checkpoint == 9 and memory.main.getMap() == 310:
                checkpoint += 1
            elif checkpoint == 12 and memory.main.getMap() == 272:
                checkpoint += 1
            elif checkpoint in [23, 27] and memory.main.getMap() == 225:
                checkpoint = 24
            elif checkpoint == 26 and memory.main.getMap() == 313:
                checkpoint += 1
            elif checkpoint == 34 and memory.main.getMap() == 244:
                checkpoint += 1
            elif checkpoint == 37 and memory.main.getMap() == 259:
                checkpoint += 1
            if checkpoint in [20, 21, 22, 29, 30] and memory.main.getMap() == 259:
                if prefArea in [8, 9]:
                    checkpoint = 41
                else:
                    checkpoint = 1
                print("-- Reminder, next area: ", prefArea)

            # Portal Combat
            if checkpoint == 2:
                while memory.main.userControl():
                    FFXC.set_movement(1, 1)
                FFXC.set_neutral()
                memory.main.waitFrames(30)
                if prefArea in [2, 4]:
                    xbox.tapDown()
                    checkpoint = 3
                else:
                    xbox.tapUp()
                    xbox.tapUp()
                    checkpoint = 22
                xbox.tapB()
                memory.main.awaitControl()
                print("Updated checkpoint: ", checkpoint)
            if checkpoint == 21:
                while memory.main.userControl():
                    FFXC.set_movement(0, -1)
                FFXC.set_neutral()
                memory.main.clickToControl()
                memory.main.awaitControl()
                if prefArea in [8, 9]:
                    checkpoint = 41
                else:
                    checkpoint = 1
            elif checkpoint == 29:
                FFXC.set_movement(0, -1)
                memory.main.waitFrames(3)
                xbox.tapB()
                xbox.tapB()
                FFXC.set_neutral()
                if prefArea in [8, 9]:
                    checkpoint = 41
                else:
                    checkpoint = 1
                # print("Updated checkpoint: ", checkpoint)

            # Branches, decisions
            if checkpoint in [0, 1] and prefArea == 1:  # Straight to mountain path
                checkpoint = 30
            elif checkpoint == 40 and not prefArea in [8, 9]:
                checkpoint = 1
            elif prefArea == 1 and checkpoint == 37:
                checkpoint -= 2
            elif prefArea == 2 and checkpoint in [4, 20]:
                checkpoint = 18
            elif prefArea == 3 and checkpoint == 26:
                checkpoint -= 2
            elif prefArea == 4 and checkpoint == 12:
                checkpoint -= 2

            # Escapes for moving onward
            if checkpoint in [35, 36] and prefArea != 1:
                checkpoint = 37
            elif checkpoint in [18, 19] and prefArea != 2:
                if prefArea == 4:
                    checkpoint = 3
                else:
                    checkpoint = 20
            elif checkpoint in [24, 25] and prefArea != 3:
                checkpoint = 26
            elif checkpoint in [10, 11] and prefArea != 4:
                checkpoint = 12

            # NEA decisions
            if neArmor == True and checkpoint in [9, 17]:
                nemesis.menu.removeAllNEA()
                neArmor = False
            elif neArmor == False and checkpoint == 4:
                nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
                neArmor = True
            elif neArmor == False and checkpoint == 13 and prefArea != 2:
                nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
                neArmor = True

            # End decisions
            if checkpoint == 43:
                if prefArea == 8:
                    memory.main.touchSaveSphere()
                    checkpoint = 0
                else:
                    returnToAirship()
            elif (
                nemesis.targetPath.setMovement(nemesis.targetPath.gagazet(checkpoint))
                == True
            ):
                checkpoint += 1
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                if capNum == 10:
                    battleFarmAll(yunaAttack=False)
                else:
                    battleFarmAll()
                prefArea = gagazetNext(endGoal=capNum)
                print("Next area: ", prefArea)
            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()
    print("Done with Swimmers, now ready for Path")


def gagazet1(capNum: int = 10):  # No longer used
    rinEquipDump()
    airShipDestination(destNum=13)
    nemesis.menu.removeAllNEA()
    checkpoint = 0
    while not (memory.main.getMap() == 259 and checkpoint == 20):
        if memory.main.userControl():
            if (
                memory.main.arenaFarmCheck(
                    zone="gagazet1", endGoal=capNum, report=False
                )
                and checkpoint < 12
            ):
                checkpoint = 12
            elif checkpoint == 12 and not memory.main.arenaFarmCheck(
                zone="gagazet1", endGoal=capNum, report=False
            ):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)

            elif checkpoint == 2:
                while memory.main.userControl():
                    FFXC.set_movement(1, 1)
                FFXC.set_neutral()
                memory.main.waitFrames(90)
                xbox.tapDown()
                xbox.tapB()
                memory.main.awaitControl()
                checkpoint += 1
            elif checkpoint == 9 and memory.main.getMap() == 310:
                checkpoint += 1
            elif checkpoint == 12 and memory.main.getMap() == 272:
                checkpoint += 1
            elif (
                nemesis.targetPath.setMovement(nemesis.targetPath.gagazet1(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                if capNum == 10:
                    battleFarmAll(yunaAttack=False)
                else:
                    battleFarmAll()
                memory.main.arenaFarmCheck(zone="gagazet1", endGoal=capNum, report=True)
            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()
    print("Done with Swimmers, now ready for Path")


def gagazet2(capNum: int = 10):  # No longer used
    if memory.main.getMap() in [194, 374]:
        airShipDestination(destNum=13)

    nemesis.menu.removeAllNEA()
    checkpoint = 0
    while not checkpoint == 11:
        if memory.main.userControl():
            if (
                memory.main.arenaFarmCheck(
                    zone="gagazet2", endGoal=capNum, report=False
                )
                and checkpoint < 7
            ):
                checkpoint = 7
            elif checkpoint == 7 and not memory.main.arenaFarmCheck(
                zone="gagazet2", endGoal=capNum, report=False
            ):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)

            elif checkpoint == 4 and memory.main.getMap() == 244:
                checkpoint += 1
            elif checkpoint == 7 and memory.main.getMap() == 259:
                checkpoint += 1
            elif (
                nemesis.targetPath.setMovement(nemesis.targetPath.gagazet2(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                battleFarmAll()
                memory.main.arenaFarmCheck(zone="gagazet2", endGoal=capNum, report=True)
            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()
    print("Done with Path now ready for Zanarkand")


def gagazet3(capNum: int = 10):  # No longer used
    if memory.main.getMap() in [194, 374]:
        airShipDestination(destNum=13)

    nemesis.menu.removeAllNEA()
    checkpoint = 0
    while not memory.main.getMap() in [194, 374]:
        if memory.main.userControl():
            if (
                memory.main.arenaFarmCheck(
                    zone="gagazet3", endGoal=capNum, report=False
                )
                and checkpoint < 8
            ):
                checkpoint = 8
            elif checkpoint == 8 and not memory.main.arenaFarmCheck(
                zone="gagazet3", endGoal=capNum, report=False
            ):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)

            elif checkpoint == 2:
                while memory.main.userControl():
                    FFXC.set_movement(1, 1)
                FFXC.set_neutral()
                memory.main.waitFrames(90)
                xbox.tapDown()
                xbox.tapDown()
                xbox.tapDown()
                xbox.tapB()
                memory.main.awaitControl()
                checkpoint += 1
            elif checkpoint == 5 and memory.main.getMap() == 225:
                checkpoint += 1
            elif checkpoint == 8 and memory.main.getMap() == 313:
                checkpoint += 1
            elif checkpoint == 11:
                returnToAirship()
            elif (
                nemesis.targetPath.setMovement(nemesis.targetPath.gagazet3(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                if capNum == 10:
                    battleFarmAll(yunaAttack=False)
                else:
                    battleFarmAll()
                memory.main.arenaFarmCheck(zone="gagazet3", endGoal=capNum, report=True)
            elif memory.main.menuOpen() or memory.main.diagSkipPossible():
                xbox.tapB()
    print("All of Gagazet complete")
    rinEquipDump()


def faythNext(endGoal: int):
    next1 = rngTrack.comingBattles(area="cave_(white_zone)", battleCount=1)[0]
    next2 = rngTrack.comingBattles(area="cave_(green_zone)", battleCount=1)[0]
    farmArray = memory.main.arenaFarmCheck(
        zone="stolenfayth", endGoal=endGoal, returnArray=True
    )

    print("=======================")
    print("Next battles:")
    print("green: ", next2)
    print("white: ", next1)
    print("zone: ", farmArray)
    print("=======================")

    if farmArray[8] < endGoal and "tonberry" in next2:
        return 2
    if farmArray[4] < endGoal and "nidhogg" in next1:
        return 1
    if farmArray[4] < endGoal and "nidhogg" in next2:
        return 2
    if farmArray[7] < endGoal and "thorn" in next1:
        return 1
    if farmArray[2] < endGoal and "ghost" in next1:
        return 1
    if farmArray[2] < endGoal and "ghost" in next2:
        return 2
    if farmArray[3] < endGoal and "valaha" in next1:
        return 1
    if farmArray[3] < endGoal and "valaha" in next2:
        return 2
    if farmArray[0] < endGoal and "imp" in next1:
        return 1
    if farmArray[0] < endGoal and "imp" in next2:
        return 2
    if farmArray[1] < endGoal and "yowie" in next1:
        return 1
    if farmArray[1] < endGoal and "yowie" in next2:
        return 2
    if "coeurl" in next1:
        return 1
    if "coeurl" in next2:
        return 2
    if "malboro" in next1:
        return 1
    if "malboro" in next2:
        return 2
    if "magic_urn" in next1:  # Try to avoid urn
        return 2
    if "magic_urn" in next2:  # Try to avoid urn
        return 1
    if memory.main.arenaFarmCheck(zone="stolenfayth", endGoal=endGoal):
        return 4

    print("Could not find a desirable encounter.")
    return 1


def stolenFaythCave(capNum: int = 10):
    airShipDestination(destNum=13)
    if not memory.main.equippedWeaponHasAbility(
        charNum=gameVars.neArmor(), abilityNum=0x801D
    ):
        nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
    neArmor = True
    prefArea = faythNext(endGoal=capNum)
    print("Next area: ", prefArea)

    checkpoint = 0
    while not memory.main.getMap() in [194, 374]:
        if memory.main.userControl():
            if prefArea == 4 and checkpoint in [25, 26, 27, 28, 29]:
                checkpoint = 30
                memory.main.fullPartyFormat("initiative")
                nemesis.menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
                neArmor = True
            elif prefArea in [1, 2, 3] and checkpoint in [25, 27] and neArmor:
                nemesis.menu.removeAllNEA()
                neArmor = False
            elif checkpoint in [5, 14, 59]:
                memory.main.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 19:
                memory.main.clickToEventTemple(7)
                checkpoint += 1
            elif prefArea == 1 and checkpoint in [27, 28, 29]:
                checkpoint = 25
            elif prefArea == 2 and checkpoint == 25:
                checkpoint = 26
            elif prefArea == 2 and checkpoint == 30:
                checkpoint = 27
            elif checkpoint in [52, 53]:  # Glyph and Yojimbo
                FFXC.set_neutral()
                memory.main.waitFrames(5)
                FFXC.set_movement(0, 1)
                memory.main.waitFrames(2)
                FFXC.set_neutral()
                memory.main.waitFrames(5)
                xbox.tapB()
                memory.main.waitFrames(5)
                yojimboDialog()
                checkpoint = 54
            elif checkpoint == 55:  # Back to entrance
                FFXC.set_neutral()
                memory.main.waitFrames(5)
                FFXC.set_movement(0, -1)
                memory.main.waitFrames(2)
                FFXC.set_neutral()
                memory.main.waitFrames(5)
                xbox.tapB()
                memory.main.waitFrames(5)
                checkpoint += 1
            elif checkpoint == 62:
                returnToAirship()
            elif (
                nemesis.targetPath.setMovement(nemesis.targetPath.yojimbo(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                if memory.main.getEncounterID() in [321, 329]:
                    # Do not engage the jar boys.
                    battle.main.fleeAll()
                elif memory.main.getEncounterID() == 327 and memory.main.arenaFarmCheck(
                    zone="justtonberry", endGoal=capNum, report=False
                ):
                    # No need to die extra times on tonberries.
                    battle.main.fleeAll()
                else:
                    battleFarmAll(faythCave=True)

                memory.main.clickToControl()
                hpCheck = memory.main.getHP()
                if hpCheck[0] < 795:
                    battle.main.healUp(3)
                prefArea = faythNext(endGoal=capNum)
                print("Next area: ", prefArea)
            elif memory.main.diagSkipPossible():
                xbox.tapB()


def insideSin(capNum: int = 10):
    airShipDestination(destNum=0)
    nemesis.menu.removeAllNEA()

    while memory.main.getMap() != 203:
        FFXC.set_movement(0, -1)
    FFXC.set_neutral()

    checkpoint = 0
    while not memory.main.getMap() in [194, 374]:
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
                memory.main.fullPartyFormat("initiative")

            # End of first area logic
            elif memory.main.arenaFarmCheck(
                zone="sin1", endGoal=capNum, report=False
            ) and checkpoint in [38, 39]:
                checkpoint = 40
            elif checkpoint == 40 and not memory.main.arenaFarmCheck(
                zone="sin1", endGoal=capNum, report=False
            ):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)
            elif checkpoint < 41 and memory.main.getMap() == 204:
                checkpoint = 41

            # End of second area logic
            elif (
                memory.main.arenaFarmCheck(zone="sin2", endGoal=capNum, report=False)
                and checkpoint < 67
            ):
                checkpoint = 67
            elif checkpoint == 67 and not memory.main.arenaFarmCheck(
                zone="sin2", endGoal=capNum, report=False
            ):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)
            elif checkpoint < 68 and memory.main.getMap() == 327:
                checkpoint = 68
            elif checkpoint == 69:
                returnToAirship()
            elif checkpoint >= 65 and memory.main.getTidusMP() < 20:  # Tidus low on MP
                nemesis.targetPath.setMovement([550, 485])
                memory.main.awaitEvent()
                FFXC.set_neutral()
                memory.main.waitFrames(3)
                memory.main.awaitControl()
                memory.main.touchSaveSphere()
                nemesis.targetPath.setMovement([-200, -525])
                memory.main.awaitEvent()
                FFXC.set_neutral()
                checkpoint = 66

            # General Pathing
            elif (
                nemesis.targetPath.setMovement(nemesis.targetPath.sin(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                screen.awaitTurn()
                advancedBattleLogic()
                if checkpoint < 40:
                    print("Ahrimans only:")
                    memory.main.arenaFarmCheck(zone="sin1", endGoal=capNum, report=True)
                else:
                    memory.main.arenaFarmCheck(zone="sin2", endGoal=capNum, report=True)
            elif memory.main.menuOpen():
                xbox.tapB()


def omegaRuins(capNum: int = 10):
    nemesis.menu.rikkuProvoke()
    nemesis.menu.removeAllNEA()

    # rinEquipDump()
    # nemesis.menu.autoSortEquipment()
    airShipDestination(destNum=13, forceOmega=True)

    checkpoint = 0
    while not memory.main.getMap() in [194, 374]:
        if memory.main.userControl():
            if (
                memory.main.arenaFarmCheck(zone="omega", endGoal=capNum, report=False)
                and checkpoint < 2
            ):
                checkpoint = 2
            elif checkpoint == 2 and not memory.main.arenaFarmCheck(
                zone="omega", endGoal=capNum, report=False
            ):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)
            elif memory.main.getTidusMP() < 20:
                memory.main.touchSaveSphere()
            elif checkpoint == 3:
                returnToAirship()
            elif (
                nemesis.targetPath.setMovement(nemesis.targetPath.omega(checkpoint))
                == True
            ):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                advancedBattleLogic()
                memory.main.arenaFarmCheck(zone="omega", endGoal=capNum, report=True)
                memory.main.clickToControl()
            elif memory.main.diagSkipPossible() or memory.main.menuOpen():
                xbox.tapB()

    # Keep this so we can add in the Omega kill later.
    # if gameVars.neArmor() == 0:
    #    nemesis.menu.equipArmor(character=gameVars.neArmor(),ability=0x8056) #Auto-Haste
    # elif gameVars.neArmor() in [4,6]:
    #    nemesis.menu.equipArmor(character=gameVars.neArmor(),ability=0x800A) #Auto-Phoenix
    # else:
    #    nemesis.menu.equipArmor(character=gameVars.neArmor(),ability=99) #Unequip


def getEquipment(equip=True):
    memory.main.waitFrames(20)
    xbox.tapB()
    memory.main.waitFrames(5)
    xbox.tapUp()
    xbox.tapB()
    memory.main.waitFrames(5)
    if equip == True:
        xbox.tapUp()
    xbox.tapB()  # Equip weapon for Rikku
    memory.main.waitFrames(5)


def otherStuff():
    arenaNPC()
    xbox.tapB()
    returnToAirship()
