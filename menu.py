import memory.main
import menuGrid
import vars
import xbox

gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def grid_up():
    menuGrid.grid_up()


def grid_down():
    menuGrid.grid_down()


def grid_left():
    menuGrid.grid_left()


def grid_right():
    menuGrid.grid_right()


def await_move():
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


def await_use():
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


def await_quit_sg():
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


def auto_sort_items(manual="n"):
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
    if manual == "y":
        xbox.menuLeft()
        xbox.menuB()
    elif manual == "n":
        memory.main.closeMenu()
    else:
        memory.main.closeMenu()


def auto_sort_equipment(manual="n"):
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
    if manual == "y":
        xbox.menuLeft()
        xbox.menuB()
    elif manual == "n":
        memory.main.closeMenu()
    else:
        memory.main.closeMenu()


def short_aeons():
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


def liki():
    print("Menu - SS Liki")
    open_grid(character=0)
    memory.main.waitFrames(10)

    # Move to the Def node just to the left
    print("Sphere grid on Tidus, learn Cheer and Str +1")
    menuGrid.move_first()
    grid_up()
    grid_up()
    if memory.main.getTidusSlvl() >= 3:
        grid_left()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("power", "left")
        menuGrid.use_and_use_again()  # Str +1 node
    menuGrid.sel_sphere("ability", "none")  # Cheer
    xbox.menuB()
    menuGrid.use_and_quit()
    xbox.menuA()


def woods_menuing():
    # Tidus learning Flee
    open_grid(character=0)
    xbox.menuB()
    xbox.menuB()  # Sphere grid on Tidus
    menuGrid.move_first()
    startNode = memory.main.sGridNodeSelected()[0]
    if startNode == 242:
        agiNeed = 2
    else:
        agiNeed = 3

    menuGrid.grid_left()
    if agiNeed == 3:
        menuGrid.grid_left()
    fullMenu = False
    if memory.main.getTidusSlvl() >= agiNeed:
        fullMenu = True
        menuGrid.grid_left()

    menuGrid.move_and_use()
    menuGrid.sel_sphere("ability", "none")
    if fullMenu:
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("speed", "none")
        gameVars.completeFullKilikMenu()
    menuGrid.use_and_quit()
    # Reorder the party

    memory.main.fullPartyFormat("kilikawoods1", fullMenuClose=False)
    equip_scout(full_menu_close=True)


def geneaux():
    open_grid(character=0)

    menuGrid.move_first()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_quit()
    memory.main.closeMenu()


def luca_workers():
    open_grid(character=0)

    menuGrid.move_first()
    grid_right()
    grid_right()
    grid_right()
    grid_down()
    grid_down()
    grid_right()

    menuGrid.move_and_use()
    print("+++ sGridNodes:", memory.main.sGridNodeSelected())
    if memory.main.sGridNodeSelected()[0] == 2:
        print("No early haste")
        earlyHaste = 0
    else:
        print("Early haste, can haste for Oblitzerator")
        earlyHaste = 1
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("mana", "none")
    if earlyHaste == 1:
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("ability", "none")  # Haste

    menuGrid.use_and_quit()
    memory.main.closeMenu()
    return earlyHaste


def late_haste():
    open_grid(character=0)
    menuGrid.move_first()
    grid_right()
    grid_down()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("ability", "none")  # Haste
    menuGrid.use_and_quit()


def mrr_grid_1():
    print("Menuing: start of MRR ")
    open_grid(character=4)
    menuGrid.move_first()
    grid_right()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    print("Determining state of Wakka late menu")
    if memory.main.getSLVLWakka() < 3:
        wakkaLateMenu = True
        print("Deferring Wakkas remaining grid for later.")
    else:
        wakkaLateMenu = False
        print("Completing Wakkas remaining grid now.")
        menuGrid.use_and_move()
        grid_down()
        grid_down()
        grid_right()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("power", "none")
    print("Wakka late menu (before):", wakkaLateMenu)

    menuGrid.use_and_quit()

    memory.main.closeMenu()

    gameVars.wakkaLateMenuSet(wakkaLateMenu)


def mrr_grid_2():
    if memory.main.getSLVLWakka() >= 3:
        print("Catching up Wakkas sphere grid.")
        open_grid(character=4)

        menuGrid.move_first()
        grid_right()
        grid_down()
        grid_down()
        grid_down()
        grid_right()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("power", "none")
        menuGrid.use_and_quit()
        gameVars.wakkaLateMenuSet(False)
        print("Wakka late menu updated:", gameVars.wakkaLateMenu())
    else:
        print("Not enough sphere levels yet.")


def mrr_grid_yuna():
    print("Yuna levels good to level up.")
    open_grid(character=1)
    menuGrid.use_first()  # Sphere grid on Yuna first
    menuGrid.sel_sphere("magic", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("mana", "none")
    menuGrid.use_and_move()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("mana", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("mana", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("mana", "none")
    menuGrid.use_and_quit()


def battle_site_grid():
    print("Doing the menu stuff")
    open_grid(character=1)
    menuGrid.move_first()
    grid_left()
    grid_down()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("mana", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")

    menuGrid.use_shift_left("Kimahri")  # Sphere grid on Kimahri
    menuGrid.move_first()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_left()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_quit()

    # Wakkas weapon
    if gameVars.getLStrike() >= 2:
        equip_weapon(character=4, ability=0x8026, full_menu_close=False)
    else:
        equip_weapon(character=4, full_menu_close=False)
    memory.main.fullPartyFormat("battleSite")


def _navigate_to_position(position, battle_cursor):
    while battle_cursor() == 255:
        pass
    if battle_cursor() != position:
        print("Wrong position targeted", battle_cursor() % 2, position % 2)
        while battle_cursor() % 2 != position % 2:
            if battle_cursor() % 2 < position % 2:
                xbox.tapRight()
            else:
                xbox.tapLeft()
        while battle_cursor() != position:
            print(battle_cursor())
            if battle_cursor() > position:
                xbox.tapUp()
            else:
                xbox.tapDown()


def battle_site_oaka_1():
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
        items_to_sell = [(i, v) for i, v in enumerate(itemOrder) if v in [0, 1, 2, 8]]
    else:
        items_to_sell = [(i, v) for i, v in enumerate(itemOrder) if v in [0, 1, 2]]
    print(items_to_sell)
    for slot, cur_item in items_to_sell:
        print(slot, cur_item)
        _navigate_to_position(slot, memory.main.equipSellRow)
        cur_amount = memory.main.getItemCountSlot(slot)
        if memory.main.rngSeed() == 160:
            amount_to_sell = max(cur_amount - {0: 0, 1: 0, 2: 0}[cur_item], 0)
        else:
            amount_to_sell = max(cur_amount - {0: 0, 1: 0, 2: 0, 8: 0}[cur_item], 0)
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


def battle_site_oaka_2():
    memory.main.clickToDiagProgress(74)
    memory.main.clickToDiagProgress(96)
    if memory.main.getGilvalue() < 10890:
        all_equipment = memory.main.allEquipment()
        other_slots = [
            i
            for i, handle in enumerate(all_equipment)
            if (i > 5 and handle.equipStatus == 255 and not handle.isBrotherhood())
        ]
        for cur in other_slots:
            sell_weapon(cur)
            if memory.main.getGilvalue() >= 10890:
                break
    buy_weapon(2, equip=True)
    memory.main.closeMenu()


def buy_weapon(location, equip=False):
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


def sell_weapon(location):
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


def djose_temple():
    open_grid(character=0)

    # Sphere grid Tidus
    menuGrid.move_first()
    grid_up()
    grid_up()
    grid_up()
    menuGrid.move_and_use()  # Move to Str sphere near Lv.2 lock
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()  # Str +1
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()  # HP +200
    menuGrid.sel_sphere("speed", "none")
    # Now sphere grid on Wakka

    if memory.main.getSLVLWakka() >= 5:
        menuGrid.use_shift_right("wakka")  # Agi +2
        menuGrid.move_first()

        grid_right()
        grid_left()
        grid_left()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("power", "up")
    menuGrid.use_and_quit()
    memory.main.closeMenu()


def m_woods():
    while not memory.main.menuOpen():
        xbox.tapB()  # Talking through O'aka's conversation.
    memory.main.closeMenu()
    buy_weapon(0, equip=True)
    memory.main.closeMenu()


def m_lake_grid():
    open_grid(character=1)  # Start with Yuna
    menuGrid.move_first()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    menuGrid.move_and_use()
    xbox.menuDown()
    xbox.menuDown()
    xbox.menuDown()
    menuGrid.sel_sphere("Lv2", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_up()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_shift_left("rikku")  # Shift to Rikku
    menuGrid.move_first()

    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")

    menuGrid.use_shift_right("kimahri")  # And last is Yuna
    menuGrid.move_first()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("Lv1", "none")
    menuGrid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("Lv1", "none")
    menuGrid.use_and_move()
    grid_up()
    grid_up()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("ability", "none")  # Steal
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("ability", "none")  # Use
    menuGrid.use_and_quit()
    memory.main.closeMenu()


def mac_temple():
    open_grid(character=0)

    menuGrid.use_first()
    menuGrid.sel_sphere("Lv2", "none")
    menuGrid.use_and_move()
    grid_right()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_up()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_right()
    grid_right()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_right()
    grid_right()
    if gameVars.getBlitzWin():
        menuGrid.move_and_use()
        menuGrid.sel_sphere("strength", "none")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("power", "none")
        menuGrid.use_and_move()
    grid_left()
    grid_left()
    if gameVars.nemesis():
        grid_up()
        grid_left()
        grid_up()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("strength", "none")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("power", "none")
        menuGrid.use_and_move()
        grid_down()
        grid_right()
        grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    if gameVars.nemesis():
        grid_right()
        grid_down()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("strength", "none")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("power", "none")
        menuGrid.use_and_move()
        grid_left()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    if gameVars.nemesis():
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("strength", "none")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_quit()

    if gameVars.getBlitzWin():
        equip_weapon(character=0, special="brotherhood")
    memory.main.closeMenu()


def after_seymour():
    open_grid(character=0)
    menuGrid.move_first()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    if gameVars.nemesis():
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("mp", "none")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("mana", "none")
    menuGrid.use_and_move()
    grid_up()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    if gameVars.nemesis():
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("mp", "none")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("mana", "none")
    menuGrid.use_and_quit()
    memory.main.closeMenu()


def home_grid():
    open_grid(character=0)
    menuGrid.move_first()
    grid_down()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_quit()

    memory.main.fullPartyFormat("desert1")
    memory.main.closeMenu()


def before_guards(item_to_use: int = 3):
    while not memory.main.menuOpen():
        memory.main.openMenu()

    while memory.main.getMenuCursorPos() != 1:
        memory.main.menuDirection(memory.main.getMenuCursorPos(), 1, 11)
    while memory.main.menuNumber() != 26:
        xbox.tapB()
    megaPotSlot = memory.main.getItemSlot(item_to_use)
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


def sort_items(full_menu_close=True):
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
    if full_menu_close:
        memory.main.closeMenu()
    else:
        memory.main.backToMainMenu()


def equip_weapon(*, character, ability=None, full_menu_close=True, special="none"):
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
        if special == "brotherhood":
            if currentWeapon.abilities() == [0x8063, 0x8064, 0x802A, 0x8000]:
                weaponNum = index
                break
        elif special == "brotherhoodearly":
            if (
                currentWeapon.abilities() == [0x8063, 255, 255, 255]
                and currentWeapon.slotCount() == 4
            ):
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
        if full_menu_close:
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
            memory.main.menuDirection(
                memory.main.getCharCursorPos(),
                target_pos,
                len(memory.main.getOrderSeven()),
            )
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

    if full_menu_close:
        memory.main.closeMenu()
    else:
        memory.main.backToMainMenu()

    return True


def equip_sonic_steel(full_menu_close=True):
    return equip_weapon(character=0, ability=32769, full_menu_close=full_menu_close)


def equip_scout(full_menu_close=True):
    return equip_weapon(character=4, ability=0x8022, full_menu_close=full_menu_close)


def equip_armor(*, character, ability=255, slot_count=99, full_menu_close=True):
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
            elif all(
                currentArmor.hasAbility(cur_ability) for cur_ability in abilityarray
            ):
                if slot_count != 99:
                    if slot_count == currentArmor.slotCount():
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
            memory.main.menuDirection(
                memory.main.getCharCursorPos(),
                target_pos,
                len(memory.main.getOrderSeven()),
            )
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

    if full_menu_close:
        memory.main.closeMenu()
    else:
        memory.main.backToMainMenu()

    return True


def via_purifico():
    open_grid(character=2)  # Auron

    menuGrid.move_first()
    grid_right()
    grid_right()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("Lv2", "none")
    menuGrid.use_and_move()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("Lv2", "none")
    menuGrid.use_and_move()
    grid_up()
    grid_up()
    memory.main.waitFrames(30 * 0.3)
    gridLocation = memory.main.sGridNodeSelected()
    # We have extra levels, changes the path slightly.
    if gridLocation[0] != 242:
        grid_up()
        grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("mana", "none")

    menuGrid.use_shift_right("yuna")
    menuGrid.use_first()
    menuGrid.sel_sphere("tele", "up")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("mana", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")

    menuGrid.use_and_move()
    grid_right()
    grid_right()
    grid_right()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("mana", "none")

    menuGrid.use_and_move()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")

    menuGrid.use_and_move()
    grid_left()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("mana", "none")
    menuGrid.use_and_move()
    grid_left()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")

    menuGrid.use_and_move()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_quit()
    memory.main.closeMenu()


def seymour_natus_blitz_win():
    open_grid(character=1)

    menuGrid.use_first()
    menuGrid.sel_sphere("tele", "up2")
    menuGrid.use_and_use_again()

    menuGrid.sel_sphere("power", "none")  # Str
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")  # Str
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")  # Def +3

    menuGrid.use_and_move()
    if gameVars.nemesis():
        grid_up()
        grid_up()
        grid_left()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("power", "none")
        menuGrid.use_and_move()
        grid_up()
        grid_down()
        grid_down()
    else:
        grid_left()
        grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")

    menuGrid.use_and_move()
    if gameVars.nemesis():
        grid_right()
        grid_down()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("power", "none")
        menuGrid.use_and_move()
        grid_left()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    if gameVars.nemesis():
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    if gameVars.nemesis():
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("mana", "none")
    menuGrid.use_and_quit()


def seymour_natus_blitz_loss():
    open_grid(character=1)

    menuGrid.use_first()
    menuGrid.sel_sphere("tele", "left")
    menuGrid.use_and_use_again()

    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")

    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("friend", "left")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    if gameVars.nemesis():
        menuGrid.use_and_move()
        grid_up()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("mana", "none")

    menuGrid.use_and_move()

    grid_right()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    if gameVars.nemesis():
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("mana", "none")
    menuGrid.use_and_move()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    if gameVars.nemesis():
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_right()
    if gameVars.nemesis():
        grid_right()
        grid_down()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("power", "none")
        menuGrid.use_and_move()
        grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "left")
    menuGrid.use_and_quit()


def prep_calm_lands():
    open_grid(character=1)
    if gameVars.getBlitzWin():
        menuGrid.move_first()
        grid_up()
        grid_up()
        if gameVars.nemesis():
            menuGrid.move_and_use()
            menuGrid.sel_sphere("mana", "none")
            menuGrid.use_and_move()
        grid_down()
        grid_down()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("power", "none")
    else:
        menuGrid.move_first()
        if gameVars.nemesis():
            grid_up()
            grid_up()
            grid_left()
            menuGrid.move_and_use()
            menuGrid.sel_sphere("power", "none")
            menuGrid.use_and_move()
            grid_up()
        grid_right()
        grid_right()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("power", "none")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_quit()
    memory.main.closeMenu()


def after_ronso():
    if gameVars.endGameVersion() != 3:
        memory.main.openMenu()
        yuna_first_strike()
        auron_first_strike()
        if not memory.main.equippedWeaponHasAbility(charNum=1, abilityNum=0x8001):
            equip_weapon(character=1, ability=0x8001, full_menu_close=False)
        if not memory.main.equippedWeaponHasAbility(charNum=2, abilityNum=0x8001):
            equip_weapon(character=2, ability=0x8001, full_menu_close=False)
        if gameVars.usePause():
            memory.main.waitFrames(5)

    open_grid(character=5)
    menuGrid.move_first()
    grid_up()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("Lv2", "none")
    menuGrid.use_and_move()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("Lv3", "none")
    menuGrid.use_and_move()
    grid_right()
    grid_down()
    grid_down()

    if gameVars.endGameVersion() in [1, 2]:  # Two of each
        menuGrid.move_shift_left("yuna")
        menuGrid.use_first()
        menuGrid.sel_sphere("friend", "d2")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("power", "none")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("power", "none")
        menuGrid.use_shift_right("Lulu")
        menuGrid.move_first()
        grid_up()
        grid_up()
        grid_up()
        grid_up()
        menuGrid.move_shift_left("Yuna")
        menuGrid.use_first()
        menuGrid.sel_sphere("friend", "none")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("speed", "none")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("speed", "none")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("power", "none")

    elif gameVars.endGameVersion() == 4:  # Four return spheres
        menuGrid.move_shift_left("yuna")
        menuGrid.use_first()
        if gameVars.getBlitzWin():
            menuGrid.sel_sphere("ret", "yunaspec")
        else:
            menuGrid.sel_sphere("ret", "d5")
        menuGrid.use_and_move()
        grid_left()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("Lv1", "none")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("mana", "none")
        menuGrid.use_and_move()
        grid_right()
        grid_down()
        grid_right()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("speed", "none")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("power", "none")

    elif gameVars.endGameVersion() == 3:  # Four friend spheres
        if gameVars.getBlitzWin():
            print("Four friend spheres, Blitz Win")
            menuGrid.move_shift_right("tidus")
            menuGrid.move_first()
            grid_right()
            grid_right()
            grid_right()
            grid_down()
            grid_right()
            grid_right()
            grid_right()
            menuGrid.move_shift_right("yuna")
            menuGrid.use_first()
            menuGrid.sel_sphere("friend", "afterBYSpec")
            menuGrid.use_and_use_again()
            menuGrid.sel_sphere("power", "none")
            menuGrid.use_shift_left("tidus")
            menuGrid.move_first()
            grid_down()
            grid_left()
            grid_left()
            menuGrid.move_and_use()
            menuGrid.sel_sphere("ability", "none")
            menuGrid.move_shift_right("yuna")
        else:
            print("Four friend spheres, Blitz Loss")
            menuGrid.move_shift_right("tidus")
            menuGrid.move_first()
            grid_right()
            grid_right()
            grid_right()
            grid_down()
            grid_down()
            grid_down()
            grid_down()
            grid_down()
            grid_right()
            grid_down()
            menuGrid.move_and_use()
            menuGrid.sel_sphere("ability", "none")
            menuGrid.use_and_move()
            grid_right()
            grid_right()
            grid_down()
            menuGrid.move_shift_right("yuna")
            menuGrid.use_first()
            menuGrid.sel_sphere("friend", "afterBYSpec")
            menuGrid.use_and_use_again()
            menuGrid.sel_sphere("power", "left")

        # Now to replicate the 2/2 split grid
        menuGrid.use_first()
        menuGrid.sel_sphere("friend", "d2")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("power", "none")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("power", "none")
        menuGrid.use_shift_left("Lulu")
        menuGrid.move_first()
        grid_up()
        grid_up()
        grid_up()
        grid_up()
        menuGrid.move_shift_right("Yuna")
        menuGrid.use_first()
        menuGrid.sel_sphere("friend", "none")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("speed", "none")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("speed", "none")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("power", "none")

        # Last, to get some Rikku stuff early.
        menuGrid.move_shift_right("Rikku")
        menuGrid.move_first()
        grid_down()
        grid_down()
        grid_down()
        grid_left()
        grid_left()
        grid_left()
        menuGrid.move_shift_right("Yuna")
        menuGrid.use_first()
        menuGrid.sel_sphere("friend", "l2")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("speed", "none")
        if gameVars.getBlitzWin():
            menuGrid.use_and_use_again()
            menuGrid.sel_sphere("mana", "none")
        menuGrid.use_and_move()
        grid_left()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("power", "none")

    menuGrid.use_and_quit()
    memory.main.closeMenu()


def find_equipment_index(*, owner, equipment_type, ability_array=[], slotcount):
    equipArray = memory.main.allEquipment()
    print(owner, equipment_type, ability_array, slotcount)
    if not ability_array:
        ability_array = [255, 255, 255, 255]
    # auron baroque sword - [0x800B, 0x8063, 255, 255]
    print("Looking for:", ability_array)
    for current_index, currentHandle in enumerate(equipArray):
        print(
            "Slot:",
            current_index,
            " | Owner:",
            currentHandle.owner(),
            " | Abilities:",
            currentHandle.abilities(),
            " | Slots:",
            currentHandle.slotCount(),
        )
        if (
            currentHandle.owner() == owner
            and currentHandle.equipmentType() == equipment_type
            and currentHandle.abilities() == ability_array
            and currentHandle.slotCount() == slotcount
        ):
            print("Equipment found in slot:", current_index)
            return current_index


def ability_to_customize_ref(ability_index):
    if (
        memory.main.customizeMenuArray()[memory.main.assignAbilityToEquipCursor()]
        == ability_index
    ):
        return True
    return False


def add_ability(
    *,
    owner,
    equipment_type,
    ability_array=[],
    ability_index=255,
    slotcount,
    navigateToEquipMenu=False,
    exitOutOfCurrentWeapon=True,
    closeMenu=True,
    fullMenuClose=True
):
    if navigateToEquipMenu:
        if not memory.main.menuOpen():
            memory.main.openMenu()
        while memory.main.getMenuCursorPos() != 8:
            memory.main.menuDirection(memory.main.getMenuCursorPos(), 8, 11)
        while memory.main.menuNumber() == 5:
            xbox.tapB()
    item_to_modify = find_equipment_index(
        owner=owner,
        equipment_type=equipment_type,
        ability_array=ability_array,
        slotcount=slotcount,
    )
    while memory.main.itemMenuRow() != item_to_modify:
        if memory.main.itemMenuRow() < item_to_modify:
            if item_to_modify - memory.main.itemMenuRow() > 9:
                xbox.TriggerR()
            else:
                xbox.tapDown()
        else:
            if (
                memory.main.itemMenuRow() - item_to_modify > 5
                and memory.main.itemMenuRow() > 8
            ):
                xbox.TriggerL()
            else:
                xbox.tapUp()
    while not memory.main.cureMenuOpen():
        xbox.tapB()
    while not ability_to_customize_ref(ability_index):  # Find the right ability
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


def add_first_strike(
    *,
    owner,
    equipment_type,
    ability_array=[],
    slotcount,
    navigateToEquipMenu=False,
    exitOutOfCurrentWeapon=True,
    closeMenu=True,
    fullMenuClose=True
):
    add_ability(
        owner=owner,
        equipment_type=equipment_type,
        ability_array=ability_array,
        ability_index=0x8001,
        slotcount=slotcount,
        navigateToEquipMenu=navigateToEquipMenu,
        exitOutOfCurrentWeapon=exitOutOfCurrentWeapon,
        closeMenu=closeMenu,
        fullMenuClose=fullMenuClose,
    )


def auron_first_strike():
    print("Starting Auron")
    add_first_strike(
        owner=2,
        equipment_type=0,
        ability_array=[0x800B, 0x8063, 255, 255],
        slotcount=3,
        closeMenu=True,
        fullMenuClose=False,
        navigateToEquipMenu=False,
    )
    print("Done with Auron")


def yuna_first_strike():
    print("Starting Yuna")
    if gameVars.nemesis():
        add_first_strike(
            owner=1,
            equipment_type=0,
            ability_array=[0x807A, 255, 255, 255],
            slotcount=2,
            closeMenu=False,
            navigateToEquipMenu=True,
        )
    else:
        add_first_strike(
            owner=1,
            equipment_type=0,
            slotcount=1,
            closeMenu=False,
            navigateToEquipMenu=True,
        )
    print("Done with Yuna")


def tidus_slayer(od_pos: int = 2):
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
    if od_pos == 2:
        xbox.menuDown()
    else:
        xbox.menuUp()
    xbox.menuB()
    memory.main.closeMenu()


def sell_all(nea=False):
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
        if not nea and fullArray[memory.main.equipSellRow()].hasAbility(0x801D):
            # No-Encounters
            sellItem = False
        if fullArray[memory.main.equipSellRow()].abilities() == [
            0x8063,
            0x8064,
            0x802A,
            0x8000,
        ]:
            # Brotherhood
            sellItem = False

        if sellItem:
            xbox.menuB()
            xbox.tapUp()
            xbox.menuB()
            memory.main.waitFrames(1)
        else:
            sellItem = True


def after_flux():
    open_grid(character=0)

    # Sphere grid on Tidus
    menuGrid.move_first()
    grid_right()
    grid_right()
    grid_right()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("ability", "none")
    menuGrid.use_and_quit()


def gagazet_cave():
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


def zombie_strike_backup():
    open_grid(character=0)

    menuGrid.move_first()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("lv4", "none")
    menuGrid.use_and_move()
    grid_up()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("ability", "none")
    menuGrid.use_and_quit()


def bfa():
    open_grid(character=1)  # Yuna final grid

    menuGrid.use_first()

    if gameVars.endGameVersion() == 3:
        menuGrid.sel_sphere("attribute", "none")
        menuGrid.use_and_use_again()
    else:
        menuGrid.sel_sphere("attribute", "l5")
        memory.main.waitFrames(30 * 0.07)
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("ret", "torikku")
        memory.main.waitFrames(30 * 0.07)
        menuGrid.use_and_move()
        grid_down()
        grid_down()
        grid_left()
        grid_down()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("speed", "none")
        menuGrid.use_and_move()
        grid_down()
        grid_down()
        grid_down()
        menuGrid.move_and_use()
    menuGrid.sel_sphere("ability", "none")
    menuGrid.use_and_move()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "left")

    if gameVars.endGameVersion() == 3:
        menuGrid.use_and_move()
        grid_right()  # Not sure exactly
        grid_right()
        grid_right()
        grid_right()
        grid_right()
        grid_right()
        grid_right()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("speed", "none")
        menuGrid.use_and_move()
        grid_down()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("speed", "none")

    if memory.main.overdriveState()[6] != 100:
        menuGrid.use_shift_left("Rikku")
        menuGrid.use_first()
        menuGrid.sel_sphere("skill", "up")

    if gameVars.zombieWeapon() == 255:
        menuGrid.use_shift_left("tidus")
        menuGrid.move_first()
        grid_up()
        grid_up()
        grid_up()
        grid_up()
        grid_up()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("lv4", "none")
        menuGrid.use_and_move()
        grid_up()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("ability", "none")
    menuGrid.use_and_quit()
    memory.main.closeMenu()


def sk_return():
    open_grid(character=1)
    menuGrid.use_first()
    menuGrid.sel_sphere("friend", "d2")
    if not gameVars.getSkipZanLuck():
        menuGrid.use_and_use_again()  # Friend sphere to Lulu
        menuGrid.sel_sphere("luck", "none")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("fortune", "none")
    if memory.main.getPower() >= 1:
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("power", "none")
    if memory.main.getPower() >= 1:
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    menuGrid.move_and_use()
    if memory.main.getPower() >= 1:
        menuGrid.sel_sphere("power", "none")
        menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_quit()


def sk_mixed():
    open_grid(character=1)
    menuGrid.use_first()
    menuGrid.sel_sphere("ret", "r2")
    menuGrid.use_and_move()  # Return to Wakkas grid
    grid_left()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("mana", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("lv1", "none")
    if not gameVars.getSkipZanLuck():
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("luck", "none")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("fortune", "none")
    menuGrid.use_and_move()
    grid_right()
    grid_down()
    grid_right()
    menuGrid.move_and_use()
    if memory.main.getPower() >= 1:
        menuGrid.sel_sphere("power", "none")
        menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_move()
    grid_left()
    grid_left()
    menuGrid.move_and_use()
    if memory.main.getPower() >= 1:
        menuGrid.sel_sphere("power", "none")
        menuGrid.use_and_use_again()
    menuGrid.sel_sphere("speed", "none")
    if memory.main.getPower() >= 1:
        menuGrid.use_and_move()
        grid_down()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_quit()


def sk_friend():
    # First to do the First Strike stuff we couldn't do earlier.
    memory.main.openMenu()
    yuna_first_strike()
    auron_first_strike()
    if not memory.main.equippedWeaponHasAbility(charNum=1, abilityNum=0x8001):
        equip_weapon(character=1, ability=0x8001, full_menu_close=False)
    if not memory.main.equippedWeaponHasAbility(charNum=2, abilityNum=0x8001):
        equip_weapon(character=2, ability=0x8001, full_menu_close=False)
    if gameVars.usePause():
        memory.main.waitFrames(5)

    # Now sphere grid
    if not gameVars.getSkipZanLuck():
        open_grid(character=1)
        menuGrid.move_first()
        grid_down()
        grid_down()
        menuGrid.move_and_use()
        menuGrid.sel_sphere("luck", "none")
        menuGrid.use_and_use_again()
        menuGrid.sel_sphere("fortune", "none")
        menuGrid.use_and_quit()
    memory.main.closeMenu()


def sk_return_2():
    open_grid(character=1)

    menuGrid.use_first()
    menuGrid.sel_sphere("ret", "aftersk")
    menuGrid.use_and_move()
    grid_right()
    grid_right()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("speed", "none")
    menuGrid.use_and_use_again()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_move()
    grid_down()
    menuGrid.move_and_use()
    menuGrid.sel_sphere("power", "none")
    menuGrid.use_and_quit()


def open_grid(character):
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
                        memory.main.getCharCursorPos(), target_pos, 7
                    )
                elif memory.main.partySize() < 3:
                    xbox.menuDown()
                else:
                    memory.main.menuDirection(
                        memory.main.getCharCursorPos(), target_pos, 7
                    )
            while memory.main.menuNumber() == 7:
                xbox.menuB()
            try:
                FFXC.set_neutral()
            except Exception:
                FFXC.set_neutral()
    try:
        FFXC.set_neutral()
    except Exception:
        FFXC.set_neutral()


# ------------------------------
# Nemesis menus


def arena_purchase_1():
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


def remove_all_nea():
    for i in range(7):
        if memory.main.equippedArmorHasAbility(charNum=i):  # Defaults to NEA
            if i == 0:
                if memory.main.checkAbilityArmor(ability=0x8056)[i]:
                    equip_armor(character=i, ability=0x8056)  # Auto-Haste
                else:
                    equip_armor(character=i, ability=99)  # Remove equipment
            elif i in [4, 6]:
                if memory.main.checkAbilityArmor(ability=0x801D)[i]:
                    equip_armor(character=i, ability=0x801D)  # Auto-Phoenix
                elif memory.main.checkAbilityArmor(ability=0x8072, slotCount=4)[i]:
                    equip_armor(character=i, ability=0x8072, slot_count=4)
                else:
                    equip_armor(character=i, ability=99)  # Remove equipment
            else:
                equip_armor(character=i, ability=99)  # Unequip
