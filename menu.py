import memory.main
import menuGrid
import vars
import xbox

gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def gridUp():
    menuGrid.gridUp()


def gridDown():
    menuGrid.gridDown()


def gridLeft():
    menuGrid.gridLeft()


def gridRight():
    menuGrid.gridRight()


def awaitMove():
    print("Sphere Grid: Waiting for Move command to be highlighted")
    while not memory.main.sGridActive():
        print("The Sphere Grid isn't even open! Awaiting manual recovery.")
        memory.main.waitFrames(30 * 1)
    complete = False
    while not complete:
        menuVal = memory.main.sGridMenu()
        if menuVal == 11 or menuVal == 255:
            xbox.menuB()
        elif menuVal == 7:
            cursorLoc = memory.main.cursorLocation()
            if cursorLoc[0] == 51 or cursorLoc[1] == 243:
                xbox.menuUp()
            xbox.menuB()
            complete = True
            memory.main.waitFrames(30 * 0.25)
    print("Move command highlighted. Good to go.")


def awaitUse():
    print("Sphere Grid: Waiting for Use command to be highlighted")
    while not memory.main.sGridActive():
        print("The Sphere Grid isn't even open! Awaiting manual recovery.")
        memory.main.waitFrames(30 * 1)
    complete = False
    while not complete:
        menuVal = memory.main.sGridMenu()
        print("Menu value:", menuVal)
        if menuVal == 7:
            cursorLoc = memory.main.cursorLocation()
            if cursorLoc[0] == 102 or cursorLoc[1] == 14:
                xbox.menuDown()
            xbox.menuB()
            complete = True
            memory.main.waitFrames(30 * 0.25)
        else:
            xbox.menuB()
    print("Use command highlighted. Good to go.")


def awaitQuitSG():
    print("Sphere Grid: attempting to quit")
    while memory.main.sGridActive():
        menuVal = memory.main.sGridMenu()
        if menuVal == 255:
            xbox.menuA()
        elif menuVal == 11:
            xbox.menuB()
        else:
            xbox.menuA()
    print("Back to the main menu")


def autoSortItems(manual='n'):
    memory.main.openMenu()
    xbox.menuDown()
    xbox.menuB()
    memory.main.waitFrames(12)
    xbox.menuA()
    memory.main.waitFrames(12)
    xbox.menuRight()
    memory.main.waitFrames(12)
    xbox.menuB()
    memory.main.waitFrames(12)
    xbox.menuRight()
    memory.main.waitFrames(12)
    xbox.menuB()
    xbox.menuB()
    xbox.menuB()
    if manual == 'y':
        xbox.menuLeft()
        xbox.menuB()
    elif manual == 'n':
        memory.main.closeMenu()
    else:
        memory.main.closeMenu()


def autoSortEquipment(manual='n'):
    memory.main.openMenu()
    xbox.menuDown()
    xbox.menuB()
    memory.main.waitFrames(12)
    xbox.menuA()
    memory.main.waitFrames(12)
    xbox.menuRight()
    xbox.menuRight()
    memory.main.waitFrames(12)
    xbox.menuB()
    memory.main.waitFrames(12)
    xbox.menuRight()
    xbox.menuB()
    xbox.menuB()
    xbox.menuB()
    if manual == 'y':
        xbox.menuLeft()
        xbox.menuB()
    elif manual == 'n':
        memory.main.closeMenu()
    else:
        memory.main.closeMenu()


def shortAeons():
    memory.main.printMemoryLog()
    memory.main.openMenu()
    cursorTarget = 4
    print("Aiming at", cursorTarget)
    while memory.main.getMenuCursorPos() != cursorTarget:
        print(memory.main.getMenuCursorPos())
        xbox.tapUp()
    while memory.main.menuNumber() == 5:
        xbox.tapB()
    while memory.main.configCursor() != 5:
        xbox.tapUp()
    while memory.main.configAeonCursorColumn() != 1:
        xbox.tapRight()
    while memory.main.configCursor() != 3:
        xbox.tapUp()
    while memory.main.configCursorColumn() != 1:
        xbox.tapRight()
    memory.main.closeMenu()


def Liki():
    print("Menu - SS Liki")
    openGrid(character=0)
    memory.main.waitFrames(10)

    # Move to the Def node just to the left
    print("Sphere grid on Tidus, learn Cheer and Str +1")
    menuGrid.moveFirst()
    gridUp()
    gridUp()
    if memory.main.getTidusSlvl() >= 3:
        gridLeft()
        menuGrid.moveAndUse()
        menuGrid.selSphere('power', 'left')
        menuGrid.useAndUseAgain()  # Str +1 node
    menuGrid.selSphere('ability', 'none')  # Cheer
    xbox.menuB()
    menuGrid.useAndQuit()
    xbox.menuA()


def woodsMenuing():
    # Tidus learning Flee
    openGrid(character=0)
    xbox.menuB()
    xbox.menuB()  # Sphere grid on Tidus
    menuGrid.moveFirst()
    startNode = memory.main.sGridNodeSelected()[0]
    if startNode == 242:
        agiNeed = 2
    else:
        agiNeed = 3

    menuGrid.gridLeft()
    if agiNeed == 3:
        menuGrid.gridLeft()
    fullMenu = False
    if memory.main.getTidusSlvl() >= agiNeed:
        fullMenu = True
        menuGrid.gridLeft()

    menuGrid.moveAndUse()
    menuGrid.selSphere('ability', 'none')
    if fullMenu:
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('speed', 'none')
        gameVars.completeFullKilikMenu()
    menuGrid.useAndQuit()
    # Reorder the party

    memory.main.fullPartyFormat('kilikawoods1', fullMenuClose=False)
    equipScout(fullMenuClose=True)


def Geneaux():
    openGrid(character=0)

    menuGrid.moveFirst()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed', 'none')
    menuGrid.useAndQuit()
    memory.main.closeMenu()


def LucaWorkers():
    openGrid(character=0)

    menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    gridDown()
    gridDown()
    gridRight()

    menuGrid.moveAndUse()
    print("+++ sGridNodes:", memory.main.sGridNodeSelected())
    if memory.main.sGridNodeSelected()[0] == 2:
        print("No early haste")
        earlyHaste = 0
    else:
        print("Early haste, can haste for Oblitzerator")
        earlyHaste = 1
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('mana', 'none')
    if earlyHaste == 1:
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('ability', 'none')  # Haste

    menuGrid.useAndQuit()
    memory.main.closeMenu()
    return earlyHaste


def lateHaste():
    openGrid(character=0)
    menuGrid.moveFirst()
    gridRight()
    gridDown()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('ability', 'none')  # Haste
    menuGrid.useAndQuit()


def mrrGrid1():
    print("Menuing: start of MRR ")
    openGrid(character=4)
    menuGrid.moveFirst()
    gridRight()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'none')
    print("Determining state of Wakka late menu")
    if memory.main.getSLVLWakka() < 3:
        wakkaLateMenu = True
        print("Deferring Wakkas remaining grid for later.")
    else:
        wakkaLateMenu = False
        print("Completing Wakkas remaining grid now.")
        menuGrid.useAndMove()
        gridDown()
        gridDown()
        gridRight()
        menuGrid.moveAndUse()
        menuGrid.selSphere('power', 'none')
    print("Wakka late menu (before):", wakkaLateMenu)

    menuGrid.useAndQuit()

    memory.main.closeMenu()

    gameVars.wakkaLateMenuSet(wakkaLateMenu)


def mrrGrid2():
    if memory.main.getSLVLWakka() >= 3:
        print("Catching up Wakkas sphere grid.")
        openGrid(character=4)

        menuGrid.moveFirst()
        gridRight()
        gridDown()
        gridDown()
        gridDown()
        gridRight()
        menuGrid.moveAndUse()
        menuGrid.selSphere('power', 'none')
        menuGrid.useAndQuit()
        gameVars.wakkaLateMenuSet(False)
        print("Wakka late menu updated:", gameVars.wakkaLateMenu())
    else:
        print("Not enough sphere levels yet.")


def mrrGridYuna():
    print("Yuna levels good to level up.")
    openGrid(character=1)
    menuGrid.useFirst()  # Sphere grid on Yuna first
    menuGrid.selSphere('magic', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('mana', 'none')
    menuGrid.useAndMove()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('mana', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('mana', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('mana', 'none')
    menuGrid.useAndQuit()


def battleSiteGrid():
    print("Doing the menu stuff")
    openGrid(character=1)
    menuGrid.moveFirst()
    gridLeft()
    gridDown()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('mana', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed', 'none')

    menuGrid.useShiftLeft('Kimahri')  # Sphere grid on Kimahri
    menuGrid.moveFirst()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndMove()
    gridLeft()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndMove()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndQuit()

    # Wakkas weapon
    if gameVars.getLStrike() >= 2:
        equipWeapon(character=4, ability=0x8026, fullMenuClose=False)
    else:
        equipWeapon(character=4, fullMenuClose=False)
    memory.main.fullPartyFormat('battleSite')


def _navigate_to_position(position, battleCursor):
    while battleCursor() == 255:
        pass
    if battleCursor() != position:
        print("Wrong position targeted", battleCursor() % 2, position % 2)
        while battleCursor() % 2 != position % 2:
            if battleCursor() % 2 < position % 2:
                xbox.tapRight()
            else:
                xbox.tapLeft()
        while battleCursor() != position:
            print(battleCursor())
            if battleCursor() > position:
                xbox.tapUp()
            else:
                xbox.tapDown()


def battleSiteOaka1():
    memory.main.clickToDiagProgress(96)
    while memory.main.shopMenuDialogueRow() != 1:
        xbox.tapDown()
    while memory.main.itemShopMenu() != 7:
        xbox.tapB()
    while memory.main.assignAbilityToEquipCursor() != 1:
        xbox.tapRight()
    while memory.main.itemShopMenu() != 21:
        xbox.tapB()
        if gameVars.usePause():
            memory.main.waitFrames(2)

    itemOrder = memory.main.getItemsOrder()
    if memory.main.rngSeed() != 160:
        items_to_sell = [(i, v)
                         for i, v in enumerate(itemOrder) if v in [0, 1, 2, 8]]
    else:
        items_to_sell = [(i, v)
                         for i, v in enumerate(itemOrder) if v in [0, 1, 2]]
    print(items_to_sell)
    for slot, cur_item in items_to_sell:
        print(slot, cur_item)
        _navigate_to_position(slot, memory.main.equipSellRow)
        cur_amount = memory.main.getItemCountSlot(slot)
        if memory.main.rngSeed() == 160:
            amount_to_sell = max(cur_amount - {0: 0, 1: 0, 2: 0}[cur_item], 0)
        else:
            amount_to_sell = max(
                cur_amount - {0: 0, 1: 0, 2: 0, 8: 0}[cur_item], 0)
        print("Selling from", cur_amount, "to", amount_to_sell)
        while memory.main.itemShopMenu() != 27:
            xbox.tapB()
        while memory.main.equipBuyRow() != amount_to_sell:
            if cur_amount == amount_to_sell:
                xbox.tapUp()
            elif memory.main.equipBuyRow() < amount_to_sell:
                xbox.tapRight()
            else:
                xbox.tapLeft()
        while memory.main.itemShopMenu() != 21:
            xbox.tapB()
    memory.main.closeMenu()


def battleSiteOaka2():
    memory.main.clickToDiagProgress(74)
    memory.main.clickToDiagProgress(96)
    if memory.main.getGilvalue() < 10890:
        all_equipment = memory.main.allEquipment()
        other_slots = [i for i, handle in enumerate(all_equipment) if (
            i > 5 and handle.equipStatus == 255 and not handle.isBrotherhood())]
        for cur in other_slots:
            sellWeapon(cur)
            if memory.main.getGilvalue() >= 10890:
                break
    buyWeapon(2, equip=True)
    memory.main.closeMenu()


def buyWeapon(location, equip=False):
    while not memory.main.menuOpen():
        xbox.tapB()
    if memory.main.equipShopMenu() != 12:
        while memory.main.equipShopMenu() != 9:
            xbox.tapA()
        while memory.main.itemMenuRow() != 0:
            xbox.tapLeft()
        while memory.main.equipShopMenu() != 12:
            xbox.tapB()
    while memory.main.equipBuyRow() != location:
        if memory.main.equipBuyRow() < location:
            xbox.tapDown()
        else:
            xbox.tapUp()
    while memory.main.equipShopMenu() != 18:
        xbox.tapB()
    while memory.main.equipConfirmationRow() != 1:
        pass
    while memory.main.equipConfirmationRow() != 0:
        xbox.tapUp()
    while memory.main.equipShopMenu() != 22:
        xbox.tapB()
    if equip:
        while memory.main.equipSellRow() != 1:
            pass
        while memory.main.equipSellRow() != 0:
            xbox.tapUp()
    while memory.main.equipShopMenu() != 12:
        xbox.tapB()


def sellWeapon(location):
    while not memory.main.menuOpen():
        xbox.tapB()
    if memory.main.equipShopMenu() != 25:
        while memory.main.equipShopMenu() != 9:
            xbox.tapA()
        while memory.main.itemMenuRow() != 1:
            xbox.tapRight()
        while memory.main.equipShopMenu() != 25:
            xbox.tapB()
    while memory.main.equipSellRow() != location:
        if memory.main.equipSellRow() < location:
            xbox.tapDown()
        else:
            xbox.tapUp()
    while memory.main.equipShopMenu() != 31:
        xbox.tapB()
    while memory.main.equipConfirmationRow() != 1:
        pass
    while memory.main.equipConfirmationRow() != 0:
        xbox.tapUp()
    print("Selling")
    while memory.main.equipShopMenu() != 25:
        xbox.tapB()


def djoseTemple():
    openGrid(character=0)

    # Sphere grid Tidus
    menuGrid.moveFirst()
    gridUp()
    gridUp()
    gridUp()
    menuGrid.moveAndUse()  # Move to Str sphere near Lv.2 lock
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndUseAgain()  # Str +1
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndUseAgain()  # HP +200
    menuGrid.selSphere('speed', 'none')
    # Now sphere grid on Wakka

    if memory.main.getSLVLWakka() >= 5:
        menuGrid.useShiftRight('wakka')  # Agi +2
        menuGrid.moveFirst()

        gridRight()
        gridLeft()
        gridLeft()
        menuGrid.moveAndUse()
        menuGrid.selSphere('power', 'up')
    menuGrid.useAndQuit()
    memory.main.closeMenu()


def mWoods():
    while not memory.main.menuOpen():
        xbox.tapB()  # Talking through O'aka's conversation.
    memory.main.closeMenu()
    buyWeapon(0, equip=True)
    memory.main.closeMenu()


def mLakeGrid():
    openGrid(character=1)  # Start with Yuna
    menuGrid.moveFirst()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    menuGrid.moveAndUse()
    xbox.menuDown()
    xbox.menuDown()
    xbox.menuDown()
    menuGrid.selSphere('Lv2', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndMove()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndMove()
    gridUp()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed', 'none')
    menuGrid.useShiftLeft('rikku')  # Shift to Rikku
    menuGrid.moveFirst()

    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed', 'none')

    menuGrid.useShiftRight('kimahri')  # And last is Yuna
    menuGrid.moveFirst()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('Lv1', 'none')
    menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('Lv1', 'none')
    menuGrid.useAndMove()
    gridUp()
    gridUp()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('ability', 'none')  # Steal
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('ability', 'none')  # Use
    menuGrid.useAndQuit()
    memory.main.closeMenu()


def macTemple():
    openGrid(character=0)

    menuGrid.useFirst()
    menuGrid.selSphere('Lv2', 'none')
    menuGrid.useAndMove()
    gridRight()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndMove()
    gridUp()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndMove()
    gridRight()
    gridRight()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed', 'none')
    menuGrid.useAndMove()
    gridRight()
    gridRight()
    if gameVars.getBlitzWin():
        menuGrid.moveAndUse()
        menuGrid.selSphere('strength', 'none')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('power', 'none')
        menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    if gameVars.nemesis():
        gridUp()
        gridLeft()
        gridUp()
        menuGrid.moveAndUse()
        menuGrid.selSphere('strength', 'none')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('power', 'none')
        menuGrid.useAndMove()
        gridDown()
        gridRight()
        gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndMove()
    if gameVars.nemesis():
        gridRight()
        gridDown()
        menuGrid.moveAndUse()
        menuGrid.selSphere('strength', 'none')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('power', 'none')
        menuGrid.useAndMove()
        gridLeft()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'none')
    if gameVars.nemesis():
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('strength', 'none')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('power', 'none')
    menuGrid.useAndQuit()

    if gameVars.getBlitzWin():
        equipWeapon(character=0, special='brotherhood')
    memory.main.closeMenu()


def afterSeymour():
    openGrid(character=0)
    menuGrid.moveFirst()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power', 'none')
    if gameVars.nemesis():
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('mp', 'none')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('mana', 'none')
    menuGrid.useAndMove()
    gridUp()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed', 'none')
    if gameVars.nemesis():
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('mp', 'none')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('mana', 'none')
    menuGrid.useAndQuit()
    memory.main.closeMenu()


def homeGrid():
    openGrid(character=0)
    menuGrid.moveFirst()
    gridDown()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndQuit()

    memory.main.fullPartyFormat('desert1')
    memory.main.closeMenu()


def beforeGuards(itemToUse: int = 3):
    while not memory.main.menuOpen():
        memory.main.openMenu()

    while memory.main.getMenuCursorPos() != 1:
        memory.main.menuDirection(memory.main.getMenuCursorPos(), 1, 11)
    while memory.main.menuNumber() != 26:
        xbox.tapB()
    megaPotSlot = memory.main.getItemSlot(itemToUse)
    column = megaPotSlot % 2
    row = (megaPotSlot - column) / 2
    print(megaPotSlot, column, row)

    while memory.main.itemMenuColumn() != column:
        if memory.main.itemMenuColumn() > column:
            xbox.tapLeft()
        else:
            xbox.tapRight()
    while memory.main.itemMenuRow() != row:
        if memory.main.itemMenuRow() < row:
            xbox.tapDown()
        else:
            xbox.tapUp()

    while memory.main.itemMenuNumber() != 13:
        xbox.tapB()
    current_hp = memory.main.getHP()
    maximal_hp = memory.main.getMaxHP()
    while current_hp != maximal_hp:
        xbox.tapB()
        current_hp = memory.main.getHP()


def sortItems(fullMenuClose=True):
    while not memory.main.menuOpen():
        memory.main.openMenu()
    while memory.main.getMenuCursorPos() != 1:
        memory.main.menuDirection(memory.main.getMenuCursorPos(), 1, 11)
    while memory.main.menuNumber() != 26:
        xbox.tapB()
    while memory.main.itemMenuNumber() != 53:
        xbox.tapA()
    while memory.main.assignAbilityToEquipCursor() != 1:
        xbox.tapRight()
    while memory.main.itemMenuNumber() != 25:
        xbox.tapB()
    while memory.main.equipBuyRow() != 1:
        xbox.tapRight()
    xbox.tapB()
    if fullMenuClose:
        memory.main.closeMenu()
    else:
        memory.main.backToMainMenu()


def equipWeapon(*, character, ability=None, fullMenuClose=True, special='none'):
    print("Equipping Weapon with ability ", ability)
    memory.main.awaitControl()

    weaponHandles = memory.main.weaponArrayCharacter(character)
    print("@@@@@")
    print(len(weaponHandles))
    print("@@@@@")
    weaponNum = 255

    abilityarray = []
    if not ability:
        abilityarray = []
    elif isinstance(ability, int):
        abilityarray = [ability]
    elif isinstance(ability, list):
        abilityarray = ability

    for index, currentWeapon in enumerate(weaponHandles):
        if special == 'brotherhood':
            if currentWeapon.abilities() == [0x8063, 0x8064, 0x802A, 0x8000]:
                weaponNum = index
                break
        elif special == 'brotherhoodearly':
            if currentWeapon.abilities() == [0x8063, 255, 255, 255] and currentWeapon.slotCount() == 4:
                weaponNum = index
                break
        elif not abilityarray and currentWeapon.abilities() == [255, 255, 255, 255]:
            weaponNum = index
            break
        elif all(currentWeapon.hasAbility(cur_ability) for cur_ability in abilityarray):
            weaponNum = index
            break
    print("Weapon is in slot ", weaponNum)
    if weaponNum == 255:
        if fullMenuClose:
            memory.main.closeMenu()
        else:
            memory.main.backToMainMenu()
        return False  # Item is no in inventory.

    if memory.main.menuNumber() != 26:
        if not memory.main.menuOpen():
            memory.main.openMenu()
        while memory.main.getMenuCursorPos() != 4:
            memory.main.menuDirection(memory.main.getMenuCursorPos(), 4, 11)
        while memory.main.menuNumber() == 5:
            xbox.tapB()

        target_pos = memory.main.getCharacterIndexInMainMenu(character)
        while memory.main.getCharCursorPos() != target_pos:
            memory.main.menuDirection(memory.main.getCharCursorPos(
            ), target_pos, len(memory.main.getOrderSeven()))
        while memory.main.menuNumber() != 26:
            xbox.tapB()
    while not memory.main.equipMenuOpenFromChar():
        xbox.tapB()

    while memory.main.equipWeapCursor() != weaponNum:
        if memory.main.equipWeapCursor() < weaponNum:
            xbox.tapDown()
        else:
            xbox.tapUp()
    while memory.main.equipMenuOpenFromChar():
        xbox.tapB()

    if fullMenuClose:
        memory.main.closeMenu()
    else:
        memory.main.backToMainMenu()

    return True


def equipSonicSteel(fullMenuClose=True):
    return equipWeapon(character=0, ability=32769, fullMenuClose=fullMenuClose)


def equipScout(fullMenuClose=True):
    return equipWeapon(character=4, ability=0x8022, fullMenuClose=fullMenuClose)


def equipArmor(*, character, ability=255, slotCount=99, fullMenuClose=True):
    print("Equipping Armor with ability ", ability)
    memory.main.awaitControl()

    armorHandles = memory.main.armorArrayCharacter(character)
    print("@@@@@")
    print(len(armorHandles))
    print("@@@@@")
    if ability == 99:
        armorNum = len(armorHandles)
    elif len(armorHandles) != 0:
        armorNum = 255

        abilityarray = []
        if not ability:
            abilityarray = []
        elif isinstance(ability, int):
            abilityarray = [ability]
        elif isinstance(ability, list):
            abilityarray = ability
        for index, currentArmor in enumerate(armorHandles):
            if not abilityarray and currentArmor.abilities() == [255, 255, 255, 255]:
                armorNum = index
                break
            elif all(currentArmor.hasAbility(cur_ability) for cur_ability in abilityarray):
                if slotCount != 99:
                    if slotCount == currentArmor.slotCount():
                        armorNum = index
                        break
                else:
                    armorNum = index
                    break
        if armorNum == 255:
            armorNum = len(armorHandles) + 1
    else:
        armorNum = 0

    print("Armor is in slot ", armorNum)
    if memory.main.menuNumber() != 26:
        if not memory.main.menuOpen():
            memory.main.openMenu()
        while memory.main.getMenuCursorPos() != 4:
            memory.main.menuDirection(memory.main.getMenuCursorPos(), 4, 11)
        while memory.main.menuNumber() == 5:
            xbox.tapB()

        target_pos = memory.main.getCharacterIndexInMainMenu(character)
        while memory.main.getCharCursorPos() != target_pos:
            memory.main.menuDirection(memory.main.getCharCursorPos(
            ), target_pos, len(memory.main.getOrderSeven()))
        memory.main.waitFrames(1)
        xbox.tapB()
        memory.main.waitFrames(18)
        xbox.tapDown()
        while memory.main.menuNumber() != 26:
            xbox.tapB()
    while not memory.main.equipMenuOpenFromChar():
        xbox.tapB()

    while memory.main.equipWeapCursor() != armorNum:
        if memory.main.equipWeapCursor() < armorNum:
            xbox.tapDown()
        else:
            xbox.tapUp()
    while memory.main.equipMenuOpenFromChar():
        if memory.main.assignAbilityToEquipCursor() == 1:
            xbox.tapUp()
        else:
            xbox.tapB()
        memory.main.waitFrames(2)

    if fullMenuClose:
        memory.main.closeMenu()
    else:
        memory.main.backToMainMenu()

    return True


def viaPurifico():
    openGrid(character=2)  # Auron

    menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('Lv2', 'none')
    menuGrid.useAndMove()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('Lv2', 'none')
    menuGrid.useAndMove()
    gridUp()
    gridUp()
    memory.main.waitFrames(30 * 0.3)
    gridLocation = memory.main.sGridNodeSelected()
    # We have extra levels, changes the path slightly.
    if gridLocation[0] != 242:
        gridUp()
        gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('mana', 'none')

    menuGrid.useShiftRight('yuna')
    menuGrid.useFirst()
    menuGrid.selSphere('tele', 'up')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('mana', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power', 'none')

    menuGrid.useAndMove()
    gridRight()
    gridRight()
    gridRight()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('mana', 'none')

    menuGrid.useAndMove()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power', 'none')

    menuGrid.useAndMove()
    gridLeft()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('mana', 'none')
    menuGrid.useAndMove()
    gridLeft()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power', 'none')

    menuGrid.useAndMove()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndQuit()
    memory.main.closeMenu()


def seymourNatusBlitzWin():
    openGrid(character=1)

    menuGrid.useFirst()
    menuGrid.selSphere('tele', 'up2')
    menuGrid.useAndUseAgain()

    menuGrid.selSphere('power', 'none')  # Str
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power', 'none')  # Str
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power', 'none')  # Def +3

    menuGrid.useAndMove()
    if gameVars.nemesis():
        gridUp()
        gridUp()
        gridLeft()
        menuGrid.moveAndUse()
        menuGrid.selSphere('power', 'none')
        menuGrid.useAndMove()
        gridUp()
        gridDown()
        gridDown()
    else:
        gridLeft()
        gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power', 'none')

    menuGrid.useAndMove()
    if gameVars.nemesis():
        gridRight()
        gridDown()
        menuGrid.moveAndUse()
        menuGrid.selSphere('power', 'none')
        menuGrid.useAndMove()
        gridLeft()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'none')
    if gameVars.nemesis():
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('power', 'none')
    menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'none')
    if gameVars.nemesis():
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('mana', 'none')
    menuGrid.useAndQuit()


def seymourNatusBlitzLoss():
    openGrid(character=1)

    menuGrid.useFirst()
    menuGrid.selSphere('tele', 'left')
    menuGrid.useAndUseAgain()

    menuGrid.selSphere('power', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power', 'none')

    menuGrid.useAndUseAgain()
    menuGrid.selSphere('friend', 'left')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power', 'none')
    if gameVars.nemesis():
        menuGrid.useAndMove()
        gridUp()
        menuGrid.moveAndUse()
        menuGrid.selSphere('mana', 'none')

    menuGrid.useAndMove()

    gridRight()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'none')
    if gameVars.nemesis():
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('mana', 'none')
    menuGrid.useAndMove()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'none')
    if gameVars.nemesis():
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('power', 'none')
    menuGrid.useAndMove()
    gridRight()
    if gameVars.nemesis():
        gridRight()
        gridDown()
        menuGrid.moveAndUse()
        menuGrid.selSphere('power', 'none')
        menuGrid.useAndMove()
        gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'left')
    menuGrid.useAndQuit()


def prepCalmLands():
    openGrid(character=1)
    if gameVars.getBlitzWin():
        menuGrid.moveFirst()
        gridUp()
        gridUp()
        if gameVars.nemesis():
            menuGrid.moveAndUse()
            menuGrid.selSphere('mana', 'none')
            menuGrid.useAndMove()
        gridDown()
        gridDown()
        menuGrid.moveAndUse()
        menuGrid.selSphere('power', 'none')
    else:
        menuGrid.moveFirst()
        if gameVars.nemesis():
            gridUp()
            gridUp()
            gridLeft()
            menuGrid.moveAndUse()
            menuGrid.selSphere('power', 'none')
            menuGrid.useAndMove()
            gridUp()
        gridRight()
        gridRight()
        menuGrid.moveAndUse()
        menuGrid.selSphere('power', 'none')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('power', 'none')
    menuGrid.useAndQuit()
    memory.main.closeMenu()


def afterRonso():
    if gameVars.endGameVersion() != 3:
        memory.main.openMenu()
        yunaFirstStrike()
        auronFirstStrike()
        if not memory.main.equippedWeaponHasAbility(charNum=1, abilityNum=0x8001):
            equipWeapon(character=1, ability=0x8001, fullMenuClose=False)
        if not memory.main.equippedWeaponHasAbility(charNum=2, abilityNum=0x8001):
            equipWeapon(character=2, ability=0x8001, fullMenuClose=False)
        if gameVars.usePause():
            memory.main.waitFrames(5)

    openGrid(character=5)
    menuGrid.moveFirst()
    gridUp()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('Lv2', 'none')
    menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('Lv3', 'none')
    menuGrid.useAndMove()
    gridRight()
    gridDown()
    gridDown()

    if gameVars.endGameVersion() in [1, 2]:  # Two of each
        menuGrid.moveShiftLeft('yuna')
        menuGrid.useFirst()
        menuGrid.selSphere('friend', 'd2')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('power', 'none')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('power', 'none')
        menuGrid.useShiftRight('Lulu')
        menuGrid.moveFirst()
        gridUp()
        gridUp()
        gridUp()
        gridUp()
        menuGrid.moveShiftLeft('Yuna')
        menuGrid.useFirst()
        menuGrid.selSphere('friend', 'none')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('speed', 'none')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('speed', 'none')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('power', 'none')

    elif gameVars.endGameVersion() == 4:  # Four return spheres
        menuGrid.moveShiftLeft('yuna')
        menuGrid.useFirst()
        if gameVars.getBlitzWin():
            menuGrid.selSphere('ret', 'yunaspec')
        else:
            menuGrid.selSphere('ret', 'd5')
        menuGrid.useAndMove()
        gridLeft()
        menuGrid.moveAndUse()
        menuGrid.selSphere('Lv1', 'none')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('mana', 'none')
        menuGrid.useAndMove()
        gridRight()
        gridDown()
        gridRight()
        menuGrid.moveAndUse()
        menuGrid.selSphere('speed', 'none')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('power', 'none')

    elif gameVars.endGameVersion() == 3:  # Four friend spheres
        if gameVars.getBlitzWin():
            print("Four friend spheres, Blitz Win")
            menuGrid.moveShiftRight('tidus')
            menuGrid.moveFirst()
            gridRight()
            gridRight()
            gridRight()
            gridDown()
            gridRight()
            gridRight()
            gridRight()
            menuGrid.moveShiftRight('yuna')
            menuGrid.useFirst()
            menuGrid.selSphere('friend', 'afterBYSpec')
            menuGrid.useAndUseAgain()
            menuGrid.selSphere('power', 'none')
            menuGrid.useShiftLeft('tidus')
            menuGrid.moveFirst()
            gridDown()
            gridLeft()
            gridLeft()
            menuGrid.moveAndUse()
            menuGrid.selSphere('ability', 'none')
            menuGrid.moveShiftRight('yuna')
        else:
            print("Four friend spheres, Blitz Loss")
            menuGrid.moveShiftRight('tidus')
            menuGrid.moveFirst()
            gridRight()
            gridRight()
            gridRight()
            gridDown()
            gridDown()
            gridDown()
            gridDown()
            gridDown()
            gridRight()
            gridDown()
            menuGrid.moveAndUse()
            menuGrid.selSphere('ability', 'none')
            menuGrid.useAndMove()
            gridRight()
            gridRight()
            gridDown()
            menuGrid.moveShiftRight('yuna')
            menuGrid.useFirst()
            menuGrid.selSphere('friend', 'afterBYSpec')
            menuGrid.useAndUseAgain()
            menuGrid.selSphere('power', 'left')

        # Now to replicate the 2/2 split grid
        menuGrid.useFirst()
        menuGrid.selSphere('friend', 'd2')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('power', 'none')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('power', 'none')
        menuGrid.useShiftLeft('Lulu')
        menuGrid.moveFirst()
        gridUp()
        gridUp()
        gridUp()
        gridUp()
        menuGrid.moveShiftRight('Yuna')
        menuGrid.useFirst()
        menuGrid.selSphere('friend', 'none')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('speed', 'none')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('speed', 'none')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('power', 'none')

        # Last, to get some Rikku stuff early.
        menuGrid.moveShiftRight('Rikku')
        menuGrid.moveFirst()
        gridDown()
        gridDown()
        gridDown()
        gridLeft()
        gridLeft()
        gridLeft()
        menuGrid.moveShiftRight('Yuna')
        menuGrid.useFirst()
        menuGrid.selSphere('friend', 'l2')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('speed', 'none')
        if gameVars.getBlitzWin():
            menuGrid.useAndUseAgain()
            menuGrid.selSphere('mana', 'none')
        menuGrid.useAndMove()
        gridLeft()
        menuGrid.moveAndUse()
        menuGrid.selSphere('power', 'none')

    menuGrid.useAndQuit()
    memory.main.closeMenu()


def findEquipmentIndex(*, owner, equipment_type, ability_array=[], slotcount):
    equipArray = memory.main.allEquipment()
    print(owner, equipment_type, ability_array, slotcount)
    if not ability_array:
        ability_array = [255, 255, 255, 255]
    # auron baroque sword - [0x800B, 0x8063, 255, 255]
    print("Looking for:", ability_array)
    for current_index, currentHandle in enumerate(equipArray):
        print("Slot:", current_index, " | Owner:", currentHandle.owner(
        ), " | Abilities:", currentHandle.abilities(), " | Slots:", currentHandle.slotCount())
        if currentHandle.owner() == owner and currentHandle.equipmentType() == equipment_type \
                and currentHandle.abilities() == ability_array \
                and currentHandle.slotCount() == slotcount:
            print("Equipment found in slot:", current_index)
            return current_index


def abilityToCustomizeRef(ability_index):
    if memory.main.customizeMenuArray()[memory.main.assignAbilityToEquipCursor()] == ability_index:
        return True
    return False


def addAbility(*, owner, equipment_type, ability_array=[], ability_index=255, slotcount, navigateToEquipMenu=False, exitOutOfCurrentWeapon=True, closeMenu=True, fullMenuClose=True):
    if navigateToEquipMenu:
        if not memory.main.menuOpen():
            memory.main.openMenu()
        while memory.main.getMenuCursorPos() != 8:
            memory.main.menuDirection(memory.main.getMenuCursorPos(), 8, 11)
        while memory.main.menuNumber() == 5:
            xbox.tapB()
    item_to_modify = findEquipmentIndex(
        owner=owner, equipment_type=equipment_type, ability_array=ability_array, slotcount=slotcount)
    while memory.main.itemMenuRow() != item_to_modify:
        if memory.main.itemMenuRow() < item_to_modify:
            if item_to_modify - memory.main.itemMenuRow() > 9:
                xbox.TriggerR()
            else:
                xbox.tapDown()
        else:
            if memory.main.itemMenuRow() - item_to_modify > 5 and memory.main.itemMenuRow() > 8:
                xbox.TriggerL()
            else:
                xbox.tapUp()
    while not memory.main.cureMenuOpen():
        xbox.tapB()
    while not abilityToCustomizeRef(ability_index):  # Find the right ability
        xbox.tapDown()
        if gameVars.usePause():
            memory.main.waitFrames(3)
    while memory.main.informationActive():
        xbox.tapB()
    while memory.main.equipBuyRow() != 1:
        pass
    while memory.main.equipBuyRow() != 0:
        xbox.tapUp()
    while not memory.main.informationActive():
        xbox.tapB()
    if exitOutOfCurrentWeapon:
        while memory.main.cureMenuOpen():
            xbox.tapA()
    if closeMenu:
        if fullMenuClose:
            memory.main.closeMenu()
        else:
            memory.main.backToMainMenu()


def addFirstStrike(*, owner, equipment_type, ability_array=[], slotcount, navigateToEquipMenu=False, exitOutOfCurrentWeapon=True, closeMenu=True, fullMenuClose=True):
    addAbility(owner=owner, equipment_type=equipment_type, ability_array=ability_array, ability_index=0x8001, slotcount=slotcount,
               navigateToEquipMenu=navigateToEquipMenu, exitOutOfCurrentWeapon=exitOutOfCurrentWeapon, closeMenu=closeMenu, fullMenuClose=fullMenuClose)


def auronFirstStrike():
    print("Starting Auron")
    addFirstStrike(owner=2, equipment_type=0, ability_array=[
                   0x800B, 0x8063, 255, 255], slotcount=3, closeMenu=True, fullMenuClose=False, navigateToEquipMenu=False)
    print("Done with Auron")


def yunaFirstStrike():
    print("Starting Yuna")
    if gameVars.nemesis():
        addFirstStrike(owner=1, equipment_type=0, ability_array=[
                       0x807A, 255, 255, 255], slotcount=2, closeMenu=False, navigateToEquipMenu=True)
    else:
        addFirstStrike(owner=1, equipment_type=0, slotcount=1,
                       closeMenu=False, navigateToEquipMenu=True)
    print("Done with Yuna")


def tidusSlayer(odPos: int = 2):
    if not memory.main.menuOpen():
        memory.main.openMenu()
    while memory.main.getMenuCursorPos() != 3:
        xbox.tapDown()
    while memory.main.menuNumber() == 5:
        xbox.tapB()
    memory.main.waitFrames(10)
    xbox.tapB()
    memory.main.waitFrames(10)
    xbox.menuA()
    xbox.tapRight()
    xbox.menuB()
    if odPos == 2:
        xbox.menuDown()
    else:
        xbox.menuUp()
    xbox.menuB()
    memory.main.closeMenu()


def sellAll(NEA=False):
    # Assume already on the sell items screen, index zero
    fullArray = memory.main.allEquipment()
    sellItem = True
    xbox.menuUp()
    memory.main.waitFrames(9)
    while memory.main.equipSellRow() + 1 < len(fullArray):
        xbox.menuDown()
        memory.main.waitFrames(9)
        if fullArray[memory.main.equipSellRow()].isEquipped() != 255:
            # Currently equipped
            sellItem = False
        if fullArray[memory.main.equipSellRow()].isEquipped() == 0:
            # Currently equipped
            sellItem = False
        if fullArray[memory.main.equipSellRow()].hasAbility(0x8056):
            # Auto-haste
            sellItem = False
        if fullArray[memory.main.equipSellRow()].hasAbility(0x8001):
            # First Strike
            sellItem = False
        if fullArray[memory.main.equipSellRow()].abilities() == [0x8072, 255, 255, 255]:
            # Unmodified armor from the Kilika vendor. Prevents selling Rikku/Wakka armors if they have them.
            if fullArray[memory.main.equipSellRow()].owner() in [1, 2, 4, 6]:
                sellItem = False
        if not NEA and fullArray[memory.main.equipSellRow()].hasAbility(0x801D):
            # No-Encounters
            sellItem = False
        if fullArray[memory.main.equipSellRow()].abilities() == [0x8063, 0x8064, 0x802A, 0x8000]:
            # Brotherhood
            sellItem = False

        if sellItem:
            xbox.menuB()
            xbox.tapUp()
            xbox.menuB()
            memory.main.waitFrames(1)
        else:
            sellItem = True


def afterFlux():
    openGrid(character=0)

    # Sphere grid on Tidus
    menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('ability', 'none')
    menuGrid.useAndQuit()


def gagazetCave():
    # Occurs after swimming
    memory.main.openMenu()
    xbox.menuUp()
    xbox.menuUp()
    xbox.menuUp()
    xbox.menuUp()
    xbox.menuB()
    xbox.menuUp()
    xbox.menuB()
    xbox.menuDown()
    xbox.menuDown()
    xbox.menuB()  # Yuna to slot 2
    xbox.menuDown()
    xbox.menuB()
    xbox.menuDown()
    xbox.menuDown()
    xbox.menuB()  # Auron to slot 3
    memory.main.closeMenu()


def zombieStrikeBackup():
    openGrid(character=0)

    menuGrid.moveFirst()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('lv4', 'none')
    menuGrid.useAndMove()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('ability', 'none')
    menuGrid.useAndQuit()


def BFA():
    openGrid(character=1)  # Yuna final grid

    menuGrid.useFirst()

    if gameVars.endGameVersion() == 3:
        menuGrid.selSphere('attribute', 'none')
        menuGrid.useAndUseAgain()
    else:
        menuGrid.selSphere('attribute', 'l5')
        memory.main.waitFrames(30 * 0.07)
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('ret', 'torikku')
        memory.main.waitFrames(30 * 0.07)
        menuGrid.useAndMove()
        gridDown()
        gridDown()
        gridLeft()
        gridDown()
        menuGrid.moveAndUse()
        menuGrid.selSphere('speed', 'none')
        menuGrid.useAndMove()
        gridDown()
        gridDown()
        gridDown()
        menuGrid.moveAndUse()
    menuGrid.selSphere('ability', 'none')
    menuGrid.useAndMove()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed', 'left')

    if gameVars.endGameVersion() == 3:
        menuGrid.useAndMove()
        gridRight()  # Not sure exactly
        gridRight()
        gridRight()
        gridRight()
        gridRight()
        gridRight()
        gridRight()
        menuGrid.moveAndUse()
        menuGrid.selSphere('speed', 'none')
        menuGrid.useAndMove()
        gridDown()
        menuGrid.moveAndUse()
        menuGrid.selSphere('speed', 'none')

    if memory.main.overdriveState()[6] != 100:
        menuGrid.useShiftLeft('Rikku')
        menuGrid.useFirst()
        menuGrid.selSphere('skill', 'up')

    if gameVars.zombieWeapon() == 255:
        menuGrid.useShiftLeft('tidus')
        menuGrid.moveFirst()
        gridUp()
        gridUp()
        gridUp()
        gridUp()
        gridUp()
        menuGrid.moveAndUse()
        menuGrid.selSphere('lv4', 'none')
        menuGrid.useAndMove()
        gridUp()
        menuGrid.moveAndUse()
        menuGrid.selSphere('ability', 'none')
    menuGrid.useAndQuit()
    memory.main.closeMenu()


def skReturn():
    openGrid(character=1)
    menuGrid.useFirst()
    menuGrid.selSphere('friend', 'd2')
    if not gameVars.getSkipZanLuck():
        menuGrid.useAndUseAgain()  # Friend sphere to Lulu
        menuGrid.selSphere('luck', 'none')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('fortune', 'none')
    if memory.main.getPower() >= 1:
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('power', 'none')
    if memory.main.getPower() >= 1:
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('power', 'none')
    menuGrid.useAndMove()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    menuGrid.moveAndUse()
    if memory.main.getPower() >= 1:
        menuGrid.selSphere('power', 'none')
        menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed', 'none')
    menuGrid.useAndQuit()


def skMixed():
    openGrid(character=1)
    menuGrid.useFirst()
    menuGrid.selSphere('ret', 'r2')
    menuGrid.useAndMove()  # Return to Wakkas grid
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('mana', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('lv1', 'none')
    if not gameVars.getSkipZanLuck():
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('luck', 'none')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('fortune', 'none')
    menuGrid.useAndMove()
    gridRight()
    gridDown()
    gridRight()
    menuGrid.moveAndUse()
    if memory.main.getPower() >= 1:
        menuGrid.selSphere('power', 'none')
        menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed', 'none')
    menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    menuGrid.moveAndUse()
    if memory.main.getPower() >= 1:
        menuGrid.selSphere('power', 'none')
        menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed', 'none')
    if memory.main.getPower() >= 1:
        menuGrid.useAndMove()
        gridDown()
        menuGrid.moveAndUse()
        menuGrid.selSphere('power', 'none')
    menuGrid.useAndQuit()


def skFriend():
    # First to do the First Strike stuff we couldn't do earlier.
    memory.main.openMenu()
    yunaFirstStrike()
    auronFirstStrike()
    if not memory.main.equippedWeaponHasAbility(charNum=1, abilityNum=0x8001):
        equipWeapon(character=1, ability=0x8001, fullMenuClose=False)
    if not memory.main.equippedWeaponHasAbility(charNum=2, abilityNum=0x8001):
        equipWeapon(character=2, ability=0x8001, fullMenuClose=False)
    if gameVars.usePause():
        memory.main.waitFrames(5)

    # Now sphere grid
    if not gameVars.getSkipZanLuck():
        openGrid(character=1)
        menuGrid.moveFirst()
        gridDown()
        gridDown()
        menuGrid.moveAndUse()
        menuGrid.selSphere('luck', 'none')
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('fortune', 'none')
        menuGrid.useAndQuit()
    memory.main.closeMenu()


def skReturn2():
    openGrid(character=1)

    menuGrid.useFirst()
    menuGrid.selSphere('ret', 'aftersk')
    menuGrid.useAndMove()
    gridRight()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed', 'none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndMove()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power', 'none')
    menuGrid.useAndQuit()


def openGrid(character):
    FFXC = xbox.controllerHandle()
    try:
        FFXC.set_neutral()
    except Exception:
        FFXC.set_neutral()
    while not memory.main.sGridActive():
        if memory.main.userControl() and not memory.main.menuOpen():
            xbox.tapY()
        elif memory.main.menuNumber() == 5:  # Cursor on main menu
            while memory.main.getMenuCursorPos() != 0:
                memory.main.menuDirection(memory.main.getMenuCursorPos(), 0, 11)
            while memory.main.menuNumber() == 5:
                xbox.tapB()
        elif memory.main.menuNumber() == 7:  # Cursor selecting party member
            print("Selecting party member")
            target_pos = memory.main.getCharacterIndexInMainMenu(character)
            while memory.main.getCharCursorPos() != target_pos:
                # After B&Y, party size is evaluated weird.
                if memory.main.getStoryProgress() == 2528:
                    memory.main.menuDirection(
                        memory.main.getCharCursorPos(), target_pos, 7)
                elif memory.main.partySize() < 3:
                    xbox.menuDown()
                else:
                    memory.main.menuDirection(
                        memory.main.getCharCursorPos(), target_pos, 7)
            while memory.main.menuNumber() == 7:
                xbox.menuB()
            try:
                FFXC.set_neutral()
            except Exception:
                FFXC = xbox.controllerHandle()
                FFXC.set_neutral()
    try:
        FFXC.set_neutral()
    except Exception:
        FFXC = xbox.controllerHandle()
        FFXC.set_neutral()

# ------------------------------
# Nemesis menus


def arenaPurchase1():
    memory.main.waitFrames(60)
    xbox.tapB()
    memory.main.waitFrames(15)
    xbox.tapB()  # Tidus catcher
    memory.main.waitFrames(15)
    xbox.tapUp()
    xbox.tapB()  # Confirm
    memory.main.waitFrames(15)
    xbox.tapB()  # Do not equip
    memory.main.waitFrames(15)
    xbox.tapDown()
    xbox.tapB()  # Yuna catcher
    memory.main.waitFrames(15)
    xbox.tapUp()
    xbox.tapB()  # Confirm
    memory.main.waitFrames(15)
    xbox.tapUp()
    xbox.tapB()  # Do equip
    memory.main.waitFrames(15)
    xbox.tapA()
    memory.main.waitFrames(15)
    xbox.tapA()
    memory.main.waitFrames(15)
    xbox.tapUp()
    xbox.tapA()
    memory.main.waitFrames(15)
    xbox.tapB()
    memory.main.waitFrames(60)


def removeAllNEA():
    for i in range(7):
        if memory.main.equippedArmorHasAbility(charNum=i):  # Defaults to NEA
            if i == 0:
                if memory.main.checkAbilityArmor(ability=0x8056)[i]:
                    equipArmor(character=i, ability=0x8056)  # Auto-Haste
                else:
                    equipArmor(character=i, ability=99)  # Remove equipment
            elif i in [4, 6]:
                if memory.main.checkAbilityArmor(ability=0x801D)[i]:
                    equipArmor(character=i, ability=0x801D)  # Auto-Phoenix
                elif memory.main.checkAbilityArmor(ability=0x8072, slotCount=4)[i]:
                    equipArmor(character=i, ability=0x8072, slotCount=4)
                else:
                    equipArmor(character=i, ability=99)  # Remove equipment
            else:
                equipArmor(character=i, ability=99)  # Unequip
