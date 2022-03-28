import time
import math
import FFX_Xbox
import FFX_Screen
import FFX_menuGrid
import FFX_Logs
import FFX_memory
import FFX_vars
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

def gridUp():
    FFX_menuGrid.gridUp()

def gridDown():
    FFX_menuGrid.gridDown()

def gridLeft():
    FFX_menuGrid.gridLeft()

def gridRight():
    FFX_menuGrid.gridRight()

def awaitMove():
    print("Sphere Grid: Waiting for Move command to be highlighted")
    while FFX_memory.sGridActive() == False:
        print("The Sphere Grid isn't even open! Awaiting manual recovery.")
        FFX_memory.waitFrames(30 * 1)
    complete = False
    while complete == False:
        menuVal = FFX_memory.sGridMenu()
        if menuVal == 11 or menuVal == 255:
            FFX_Xbox.menuB()
        elif menuVal == 7:
            cursorLoc = FFX_memory.cursorLocation()
            if cursorLoc[0] == 51 or cursorLoc[1] == 243:
                FFX_Xbox.menuUp()
            FFX_Xbox.menuB()
            complete = True
            FFX_memory.waitFrames(30 * 0.25)
    print("Move command highlighted. Good to go.")

def awaitUse():
    print("Sphere Grid: Waiting for Use command to be highlighted")
    while FFX_memory.sGridActive() == False:
        print("The Sphere Grid isn't even open! Awaiting manual recovery.")
        FFX_memory.waitFrames(30 * 1)
    complete = False
    while complete == False:
        menuVal = FFX_memory.sGridMenu()
        print("Menu value: ", menuVal)
        if menuVal == 7:
            cursorLoc = FFX_memory.cursorLocation()
            if cursorLoc[0] == 102 or cursorLoc[1] == 14:
                FFX_Xbox.menuDown()
            FFX_Xbox.menuB()
            complete = True
            FFX_memory.waitFrames(30 * 0.25)
        else:
            FFX_Xbox.menuB()
    print("Use command highlighted. Good to go.")

def awaitQuitSG():
    print("Sphere Grid: attempting to quit")
    while FFX_memory.sGridActive():
        menuVal = FFX_memory.sGridMenu()
        if menuVal == 255:
            FFX_Xbox.menuA()
        elif menuVal == 11:
            FFX_Xbox.menuB()
        else:
            FFX_Xbox.menuA()
    print("Back to the main menu")


def autoSortItems(manual):
    FFX_memory.openMenu()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(30 * 0.4)
    FFX_Xbox.menuA()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(30 * 0.4)
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    if manual == 'y':
        FFX_Xbox.menuLeft()
        FFX_Xbox.menuB()
    elif manual == 'n':
        FFX_memory.closeMenu()
    else:
        FFX_memory.closeMenu()

def shortAeons():
    FFX_memory.printMemoryLog()
    gameVars = FFX_vars.varsHandle()
    FFX_memory.openMenu()
    cursorTarget = 4
    print("Aiming at ", cursorTarget)
    while FFX_memory.getMenuCursorPos() != cursorTarget:
        print(FFX_memory.getMenuCursorPos())
        FFX_Xbox.tapUp()
    while FFX_memory.menuNumber() == 5:
        FFX_Xbox.tapB()
    while FFX_memory.configCursor() != 5:
        FFX_Xbox.tapUp()
    while FFX_memory.configAeonCursorColumn() != 1:
        FFX_Xbox.tapRight()
    while FFX_memory.configCursor() != 3:
        FFX_Xbox.tapUp()
    while FFX_memory.configCursorColumn() != 1:
        FFX_Xbox.tapRight()
    FFX_memory.closeMenu()

def Liki():
    print("Menu - SS Liki")
    openGrid(character=0)
    FFX_memory.waitFrames(10)
    
    #Move to the Def node just to the left
    print("Sphere grid on Tidus, learn Cheer and Str +1")
    FFX_menuGrid.moveFirst()
    gridUp()
    gridUp()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    
    #Activate Str and Cheeer nodes
    FFX_menuGrid.selSphere('power','d','left')
    FFX_menuGrid.useAndUseAgain() #Str +1 node
    FFX_menuGrid.selSphere('ability','d','none') # Cheer
    FFX_Xbox.menuB()
    FFX_menuGrid.useAndQuit()
    FFX_Xbox.menuA()

def Geneaux():
    openGrid(character=0)
    
    FFX_menuGrid.moveFirst()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def LucaWorkers():
    openGrid(character=0)
    
    FFX_menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    gridDown()
    gridDown()
    gridRight()
    
    FFX_menuGrid.moveAndUse()
    print("+++ sGridNodes: ", FFX_memory.sGridNodeSelected())
    if FFX_memory.sGridNodeSelected()[0] == 2:
        print("No early haste")
        earlyHaste = 0
    else:
        print("Early haste, can haste for Oblitzerator")
        earlyHaste = 1
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('mana','d','none')
    if earlyHaste == 1:
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('ability','d','none') # Haste
        
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()
    return earlyHaste

def lateHaste():
    openGrid(character=0)
    FFX_menuGrid.moveFirst()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('ability','d','none') # Haste
    FFX_menuGrid.useAndQuit()

def mrrGrid1():
    print("Menuing: start of MRR ")
    openGrid(character=4)
    FFX_menuGrid.moveFirst()
    gridRight()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    print("Determining state of Wakka late menu")
    #FFX_memory.waitFrames(30 * 60) #Use for testing only!
    if FFX_memory.getSLVLWakka() < 3:
        wakkaLateMenu = True
        print("Deferring Wakka's remaining grid for later.")
        #FFX_memory.waitFrames(30 * 60) #Use for testing only!
    else:
        wakkaLateMenu = False
        print("Completing Wakka's remaining grid now.")
        #FFX_memory.waitFrames(30 * 60) #Use for testing only!
        FFX_menuGrid.useAndMove()
        gridDown()
        gridDown()
        gridRight()
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('power','d','none')
    print("Wakka late menu (before): ", wakkaLateMenu)
    
    FFX_menuGrid.useAndQuit()
    
    FFX_memory.closeMenu()
    
    gameVars.wakkaLateMenuSet(wakkaLateMenu)

def mrrGrid2():
    #if gameVars.wakkaLateMenu():
    if FFX_memory.getSLVLWakka() >= 3:
        print("Catching up Wakka's sphere grid.")
        openGrid(character=4)
        
        FFX_menuGrid.moveFirst()
        gridRight()
        gridDown()
        gridDown()
        gridDown()
        gridRight()
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('power','d','none')
        FFX_menuGrid.useAndQuit()
        gameVars.wakkaLateMenuSet(False)
        print("Wakka late menu updated: ", gameVars.wakkaLateMenu())
    else:
        print("Not enough sphere levels yet.")

def mrrGridYuna():
    print("Yuna levels good to level up.")
    openGrid(character=1)
    FFX_menuGrid.useFirst() #Sphere grid on Yuna first
    FFX_menuGrid.selSphere('magic','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('mana','u','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('mana','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('mana','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('mana','d','none')
    FFX_menuGrid.useAndQuit()

def battleSiteGrid():
    print("Doing the menu stuff")
    openGrid(character=1)
    FFX_menuGrid.moveFirst()
    gridLeft()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('mana','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    
    FFX_menuGrid.useShiftLeft('Kimahri') #Sphere grid on Kimahri
    FFX_menuGrid.moveFirst()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndQuit()
    
    #Sort items
    #sortItems(fullMenuClose=False)
    
    #Wakka's weapon
    if gameVars.getLStrike() >= 2:
        equipWeapon(character=4, ability=0x8026, fullMenuClose=False)
    else:
        equipWeapon(character=4, fullMenuClose=False)
    FFX_memory.fullPartyFormat('battleSite')

def _navigate_to_position(position, battleCursor):
    while battleCursor() == 255:
        pass
    if battleCursor() != position:
        print("Wrong position targetted", battleCursor() % 2, position % 2)
        while battleCursor() % 2 != position % 2:
            if battleCursor() % 2 < position % 2:
                FFX_Xbox.tapRight()
            else:
                FFX_Xbox.tapLeft()
        while battleCursor() != position:
            print(battleCursor())
            if battleCursor() > position:
                FFX_Xbox.tapUp()
            else:
                FFX_Xbox.tapDown()

def battleSiteOaka1():
    FFX_memory.clickToDiagProgress(96)
    while FFX_memory.shopMenuDialogueRow() != 1:
        FFX_Xbox.tapDown()
    while FFX_memory.itemShopMenu() != 7:
        FFX_Xbox.tapB()
    while FFX_memory.assignAbilityToEquipCursor() != 1:
        FFX_Xbox.tapRight()
    while FFX_memory.itemShopMenu() != 21:
        FFX_Xbox.tapB()
        if gameVars.usePause():
            FFX_memory.waitFrames(2)
    
    itemOrder = FFX_memory.getItemsOrder()
    items_to_sell = [(i, v) for i, v in enumerate(itemOrder) if v in [0, 1, 2, 8]]
    print(items_to_sell)
    for slot, cur_item in items_to_sell:
        print(slot, cur_item)
        _navigate_to_position(slot, FFX_memory.equipSellRow)
        cur_amount = FFX_memory.getItemCountSlot(slot)
        amount_to_sell = max(cur_amount - {0:0, 1:0, 2:0, 8:0}[cur_item], 0)
        print("Selling from ", cur_amount, " to ", amount_to_sell)
        while FFX_memory.itemShopMenu() != 27:
            FFX_Xbox.tapB()
        while FFX_memory.equipBuyRow() != amount_to_sell:
            if cur_amount == amount_to_sell:
                FFX_Xbox.tapUp()
            elif FFX_memory.equipBuyRow() < amount_to_sell:
                FFX_Xbox.tapRight()
            else:
                FFX_Xbox.tapLeft()
        while FFX_memory.itemShopMenu() != 21:
            FFX_Xbox.tapB()    
    FFX_memory.closeMenu()

def battleSiteOaka2():
    FFX_memory.clickToDiagProgress(74)
    FFX_memory.clickToDiagProgress(96)
    if FFX_memory.getGilvalue() < 10890:
        all_equipment = FFX_memory.allEquipment() 
        other_slots = [i for i, handle in enumerate(all_equipment) if (i > 5 and handle.equipStatus == 255 and not handle.isBrotherhood())]
        for cur in other_slots:
            sellWeapon(cur)
            if FFX_memory.getGilvalue() >= 10890: break
    buyWeapon(2, equip=True)    
    FFX_memory.closeMenu()

def buyWeapon(location, equip=False):
    while not FFX_memory.menuOpen():
        FFX_Xbox.tapB()
    if FFX_memory.equipShopMenu() != 12:
        while FFX_memory.equipShopMenu() != 9:
            FFX_Xbox.tapA()
        while FFX_memory.itemMenuRow() != 0:
            FFX_Xbox.tapLeft()
        while FFX_memory.equipShopMenu() != 12:
            FFX_Xbox.tapB()
    while FFX_memory.equipBuyRow() != location:
        if FFX_memory.equipBuyRow() < location:
            FFX_Xbox.tapDown()
        else:
            FFX_Xbox.tapUp()
    while FFX_memory.equipShopMenu() != 18:
        FFX_Xbox.tapB()
    while FFX_memory.equipConfirmationRow() != 1:
        pass
    while FFX_memory.equipConfirmationRow() != 0:
        FFX_Xbox.tapUp()
    while FFX_memory.equipShopMenu() != 22:
        FFX_Xbox.tapB()
    if equip:
        while FFX_memory.equipSellRow() != 1:
            pass
        while FFX_memory.equipSellRow() != 0:
            FFX_Xbox.tapUp()
    while FFX_memory.equipShopMenu() != 12:
        FFX_Xbox.tapB()

def sellWeapon(location):
    while not FFX_memory.menuOpen():
        FFX_Xbox.tapB()
    if FFX_memory.equipShopMenu() != 25:    
        while FFX_memory.equipShopMenu() != 9:
            FFX_Xbox.tapA()
        while FFX_memory.itemMenuRow() != 1:
            FFX_Xbox.tapRight()
        while FFX_memory.equipShopMenu() != 25:
            FFX_Xbox.tapB()
    while FFX_memory.equipSellRow() != location:
        if FFX_memory.equipSellRow() < location:
            FFX_Xbox.tapDown()
        else:
            FFX_Xbox.tapUp()
    while FFX_memory.equipShopMenu() != 31:
        FFX_Xbox.tapB()
    while FFX_memory.equipConfirmationRow() != 1:
        pass
    while FFX_memory.equipConfirmationRow() != 0:
        FFX_Xbox.tapUp()
    print("Selling")
    while FFX_memory.equipShopMenu() != 25:
        FFX_Xbox.tapB()
    
    

def djoseTemple():
    openGrid(character=0)
    
    #Sphere grid Tidus
    FFX_menuGrid.moveFirst()
    gridUp()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse() #Move to Str sphere near Lv.2 lock
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain() #Str +1
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain() #HP +200
    FFX_menuGrid.selSphere('speed','d','none')
    #Now sphere grid on Wakka
    
    if FFX_memory.getSLVLWakka() >= 5:
        FFX_menuGrid.useShiftRight('wakka') #Agi +2
        FFX_menuGrid.moveFirst()
        
        gridRight()
        gridLeft()
        gridLeft()
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('power','u','up')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def mWoods():
    while not FFX_memory.menuOpen():
        FFX_Xbox.tapB() #Talking through O'aka's conversation.
    FFX_memory.closeMenu()
    buyWeapon(0, equip=True)
    FFX_memory.closeMenu()

def mLakeGrid():
    openGrid(character=1) #Start with Yuna
    FFX_menuGrid.moveFirst()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_menuGrid.selSphere('Lv2','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useShiftLeft('rikku') #Shift to Rikku
    FFX_menuGrid.moveFirst()
    
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','u','none')
    
    FFX_menuGrid.useShiftRight('kimahri') #And last is Yuna
    FFX_menuGrid.moveFirst()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('Lv1','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('Lv1','d','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('ability','u','none') #Steal
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('ability','u','none') #Use
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def macTemple():
    openGrid(character=0)
    
    FFX_menuGrid.useFirst()
    FFX_menuGrid.selSphere('Lv2','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridRight()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridRight()
    if gameVars.getBlitzWin() == True:
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('strength','d','none')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('power','u','none')
        FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def afterSeymour():
    openGrid(character=0)
    FFX_menuGrid.moveFirst()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power', 'd', 'none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power', 'u', 'none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed', 'd', 'none')
    FFX_menuGrid.useAndQuit()
    equipSonicSteel(fullMenuClose=False)

def homeGrid():
    openGrid(character=0)
    FFX_menuGrid.moveFirst()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndQuit()
    
    FFX_memory.fullPartyFormat('desert1')
    FFX_memory.closeMenu()
    

def beforeGuards():
    while not FFX_memory.menuOpen():
        FFX_memory.openMenu()
        
    while FFX_memory.getMenuCursorPos() != 1:
        FFX_memory.menuDirection(FFX_memory.getMenuCursorPos(), 1, 11)
    while FFX_memory.menuNumber() != 26:
        FFX_Xbox.tapB()
    megaPotSlot = FFX_memory.getItemSlot(3)
    column = megaPotSlot % 2
    row = (megaPotSlot-column) / 2
    print(megaPotSlot, column, row)
    
    while FFX_memory.itemMenuColumn() != column:
        if FFX_memory.itemMenuColumn() > column:
            FFX_Xbox.tapLeft()
        else:
            FFX_Xbox.tapRight()
    while FFX_memory.itemMenuRow() != row:
        if FFX_memory.itemMenuRow() < row:
            FFX_Xbox.tapDown()
        else:
            FFX_Xbox.tapUp()
            
    while FFX_memory.itemMenuNumber() != 13:
        FFX_Xbox.tapB()
    current_hp = FFX_memory.getHP()
    maximal_hp = FFX_memory.getMaxHP()
    while current_hp != maximal_hp:
        FFX_Xbox.tapB()
        current_hp = FFX_memory.getHP()
    
def sortItems(fullMenuClose=True):
    while not FFX_memory.menuOpen():
        FFX_memory.openMenu()
    while FFX_memory.getMenuCursorPos() != 1:
        FFX_memory.menuDirection(FFX_memory.getMenuCursorPos(), 1, 11)
    while FFX_memory.menuNumber() != 26:
        FFX_Xbox.tapB()
    while FFX_memory.itemMenuNumber() != 53:
        FFX_Xbox.tapA()
    while FFX_memory.assignAbilityToEquipCursor() != 1:
        FFX_Xbox.tapRight()
    while FFX_memory.itemMenuNumber() != 25:
        FFX_Xbox.tapB()
    while FFX_memory.equipBuyRow() != 1:
        FFX_Xbox.tapRight()
    FFX_Xbox.tapB()
    if fullMenuClose:
        FFX_memory.closeMenu()
    else:
        FFX_memory.backToMainMenu()    
    
        

def equipWeapon(*, character, ability=None, fullMenuClose=True):
    print("Equipping Weapon with ability ", ability)
    FFX_memory.awaitControl()
    gameVars = FFX_vars.varsHandle()
    
    weaponHandles = FFX_memory.weaponArrayCharacter(character)
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
        if not abilityarray and currentWeapon.abilities() == [255,255,255,255]:
            weaponNum = index
            break
        elif all(currentWeapon.hasAbility(cur_ability) for cur_ability in abilityarray):
            weaponNum = index
            break
    print("Weapon is in slot ", weaponNum)
    if weaponNum == 255:
        if fullMenuClose:
            FFX_memory.closeMenu()
        else:
            FFX_memory.backToMainMenu()
        return False #Item is no in inventory.
    
    if FFX_memory.menuNumber() != 26:
        if not FFX_memory.menuOpen():
            FFX_memory.openMenu()
        while FFX_memory.getMenuCursorPos() != 4:
            FFX_memory.menuDirection(FFX_memory.getMenuCursorPos(), 4, 11)
        while FFX_memory.menuNumber() == 5:
            FFX_Xbox.tapB()
                
        target_pos = FFX_memory.getCharacterIndexInMainMenu(character)
        while FFX_memory.getCharCursorPos() != target_pos:
            FFX_memory.menuDirection(FFX_memory.getCharCursorPos(), target_pos, len(FFX_memory.getOrderSeven()))
        while FFX_memory.menuNumber() != 26:
            FFX_Xbox.tapB()
    while not FFX_memory.equipMenuOpenFromChar():
        FFX_Xbox.tapB()
    
    while FFX_memory.equipWeapCursor() != weaponNum:
        if FFX_memory.equipWeapCursor() < weaponNum:
            FFX_Xbox.tapDown()
        else:
            FFX_Xbox.tapUp()
    while FFX_memory.equipMenuOpenFromChar():
        FFX_Xbox.tapB()
    
    if fullMenuClose:
        FFX_memory.closeMenu()
    else:
        FFX_memory.backToMainMenu()

    return True

def equipSonicSteel(fullMenuClose=True):
    return equipWeapon(character=0, ability=32769, fullMenuClose=fullMenuClose)
    
def equipScout(fullMenuClose=True):
    return equipWeapon(character=4, ability=0x8022, fullMenuClose=fullMenuClose)

def equipArmor(*, character, ability=255, fullMenuClose=True):
    print("Equipping Armor with ability ", ability)
    FFX_memory.awaitControl()
    gameVars = FFX_vars.varsHandle()
    
    armorHandles = FFX_memory.armorArrayCharacter(character)
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
            if not abilityarray and currentArmor.abilities() == [255,255,255,255]:
                armorNum = index
                break
            elif all(currentArmor.hasAbility(cur_ability) for cur_ability in abilityarray):
                armorNum = index
                break
        if armorNum == 255:
            armorNum = len(armorHandles) + 1
    else:
        armorNum = 0
    
    print("Armor is in slot ", armorNum)
    if FFX_memory.menuNumber() != 26:
        if not FFX_memory.menuOpen():
            FFX_memory.openMenu()
        while FFX_memory.getMenuCursorPos() != 4:
            FFX_memory.menuDirection(FFX_memory.getMenuCursorPos(), 4, 11)
        while FFX_memory.menuNumber() == 5:
            FFX_Xbox.tapB()
                
        target_pos = FFX_memory.getCharacterIndexInMainMenu(character)
        while FFX_memory.getCharCursorPos() != target_pos:
            FFX_memory.menuDirection(FFX_memory.getCharCursorPos(), target_pos, len(FFX_memory.getOrderSeven()))
        FFX_memory.waitFrames(1)
        FFX_Xbox.tapB()
        FFX_memory.waitFrames(18)
        FFX_Xbox.tapDown()
        while FFX_memory.menuNumber() != 26:
            FFX_Xbox.tapB()
    while not FFX_memory.equipMenuOpenFromChar():
        FFX_Xbox.tapB()
    
    while FFX_memory.equipWeapCursor() != armorNum:
        if FFX_memory.equipWeapCursor() < armorNum:
            FFX_Xbox.tapDown()
        else:
            FFX_Xbox.tapUp()
    while FFX_memory.equipMenuOpenFromChar():
        if FFX_memory.assignAbilityToEquipCursor() == 1:
            FFX_Xbox.tapUp()
        else:
            FFX_Xbox.tapB()
        FFX_memory.waitFrames(2)
    
    if fullMenuClose:
        FFX_memory.closeMenu()
    else:
        FFX_memory.backToMainMenu()

    return True

def viaPurifico():
    openGrid(character=2) #Auron
    
    FFX_menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('Lv2','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('Lv2','d','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    FFX_memory.waitFrames(30 * 0.3)
    gridLocation = FFX_memory.sGridNodeSelected()
    if gridLocation[0] != 242: #We have extra levels, changes the path slightly.
        gridUp()
        gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('mana','u','none')
    
    FFX_menuGrid.useShiftRight('yuna')
    FFX_menuGrid.useFirst()
    FFX_menuGrid.selSphere('tele','d','up')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('mana','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    
    FFX_menuGrid.useAndMove()
    gridRight()
    gridRight()
    gridRight()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('mana','d','none')
    
    FFX_menuGrid.useAndMove()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridLeft()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    
    FFX_menuGrid.useAndMove()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def seymourNatusBlitzWin():
    openGrid(character=1)
    
    FFX_menuGrid.useFirst()
    FFX_menuGrid.selSphere('tele','d','up2')
    FFX_menuGrid.useAndUseAgain()
    
    FFX_menuGrid.selSphere('power','u','none') #Str
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none') #Str
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none') #Def +3
    
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    
    FFX_menuGrid.useAndMove()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndQuit()

def seymourNatusBlitzLoss():
    openGrid(character=1)
    
    FFX_menuGrid.useFirst()
    FFX_menuGrid.selSphere('tele','d','left')
    FFX_menuGrid.useAndUseAgain()
    
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','none')
    
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('friend','d','left')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndMove()
    
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','left')
    FFX_menuGrid.useAndQuit()

def prepCalmLands():
    openGrid(character=1)
    if gameVars.getBlitzWin() == True:
        FFX_menuGrid.moveFirst()
        gridUp()
        gridUp()
        gridDown()
        gridDown()
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('power','d','none')
    else:
        FFX_menuGrid.moveFirst()
        gridRight()
        gridRight()
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('power','d','none')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndQuit()

def afterRonso():
    if gameVars.endGameVersion() != 3:
        FFX_memory.openMenu()
        yunaFirstStrike()
        auronFirstStrike()
        equipWeapon(character=2, ability=0x8001, fullMenuClose=False)
        if gameVars.usePause():
            FFX_memory.waitFrames(5)
    
    openGrid(character=5)
    FFX_menuGrid.moveFirst()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('Lv2','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('Lv3','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridDown()
    gridDown()
    
    if gameVars.endGameVersion() in [1,2]: #Two of each
        FFX_menuGrid.moveShiftRight('yuna')
        FFX_menuGrid.useFirst()
        FFX_menuGrid.selSphere('friend','d','d2')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('power','u','none')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('power','u','none')
        FFX_menuGrid.useShiftLeft('Lulu')
        FFX_menuGrid.moveFirst()
        gridUp()
        gridUp()
        gridUp()
        gridUp()
        FFX_menuGrid.moveShiftRight('Yuna')
        FFX_menuGrid.useFirst()
        FFX_menuGrid.selSphere('friend','d','none')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('speed','u','none')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('speed','u','none')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('power','u','none')
    
    elif gameVars.endGameVersion() == 4: #Four return spheres
        FFX_menuGrid.moveShiftRight('yuna')
        FFX_menuGrid.useFirst()
        if gameVars.getBlitzWin() == True:
            FFX_menuGrid.selSphere('ret','d','yunaspec')
        else:
            FFX_menuGrid.selSphere('ret','d','d5')
        FFX_menuGrid.useAndMove()
        gridLeft()
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('Lv1','d','none')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('mana','u','none')
        FFX_menuGrid.useAndMove()
        gridRight()
        gridDown()
        gridRight()
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('speed','d','none')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('power','u','none')

    elif gameVars.endGameVersion() == 3: #Four friend spheres
        if gameVars.getBlitzWin():
            print("Four friend spheres, Blitz Win")
            FFX_menuGrid.moveShiftRight('tidus')
            FFX_menuGrid.moveFirst()
            gridRight()
            gridRight()
            gridRight()
            gridDown()
            gridRight()
            gridRight()
            gridRight()
            FFX_menuGrid.moveShiftRight('yuna')
            FFX_menuGrid.useFirst()
            FFX_menuGrid.selSphere('friend','d','afterBYSpec')
            FFX_menuGrid.useAndUseAgain()
            FFX_menuGrid.selSphere('power','u','none')
            FFX_menuGrid.useShiftLeft('tidus')
            FFX_menuGrid.moveFirst()
            gridDown()
            gridLeft()
            gridLeft()
            FFX_menuGrid.moveAndUse()
            FFX_menuGrid.selSphere('ability','d','none')
            FFX_menuGrid.moveShiftRight('yuna')
        else:
            print("Four friend spheres, Blitz Loss")
            FFX_menuGrid.moveShiftRight('tidus')
            FFX_menuGrid.moveFirst()
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
            FFX_menuGrid.moveAndUse()
            FFX_menuGrid.selSphere('ability','d','none')
            FFX_menuGrid.useAndMove()
            gridRight()
            gridRight()
            gridDown()
            FFX_menuGrid.moveShiftRight('yuna')
            FFX_menuGrid.useFirst()
            FFX_menuGrid.selSphere('friend','d','afterBYSpec')
            FFX_menuGrid.useAndUseAgain()
            FFX_menuGrid.selSphere('power','u','left')
        
        #Now to replicate the 2/2 split grid
        FFX_menuGrid.useFirst()
        FFX_menuGrid.selSphere('friend','d','d2')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('power','u','none')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('power','u','none')
        FFX_menuGrid.useShiftLeft('Lulu')
        FFX_menuGrid.moveFirst()
        gridUp()
        gridUp()
        gridUp()
        gridUp()
        FFX_menuGrid.moveShiftRight('Yuna')
        FFX_menuGrid.useFirst()
        FFX_menuGrid.selSphere('friend','d','none')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('speed','u','none')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('speed','u','none')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('power','u','none')
        
        #Last, to get some Rikku stuff early.
        FFX_menuGrid.moveShiftRight('Rikku')
        FFX_menuGrid.moveFirst()
        gridDown()
        gridDown()
        gridDown()
        gridLeft()
        gridLeft()
        gridLeft()
        FFX_menuGrid.moveShiftRight('Yuna')
        FFX_menuGrid.useFirst()
        FFX_menuGrid.selSphere('friend','d','l2')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('speed','u','none')
        if gameVars.getBlitzWin():
            FFX_menuGrid.useAndUseAgain()
            FFX_menuGrid.selSphere('mana','u','none')
        FFX_menuGrid.useAndMove()
        gridLeft()
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('power','u','none')
    
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def findEquipmentIndex(*, owner, equipment_type, ability_array=[], slotcount):
    equipArray = FFX_memory.allEquipment()
    print(owner, equipment_type, ability_array, slotcount)
    if not ability_array:
        ability_array = [255, 255, 255, 255]
    # auron baroque sword - [0x800B, 0x8063, 255, 255]
    print("Looking for: ", ability_array)
    for current_index, currentHandle in enumerate(equipArray):
        print("Slot: ", current_index, " | Owner: ", currentHandle.owner(), " | Abilities: ", currentHandle.abilities(), " | Slots: ",  currentHandle.slotCount())
        if currentHandle.owner() == owner and currentHandle.equipmentType() == equipment_type \
            and currentHandle.abilities() == ability_array \
            and currentHandle.slotCount() == slotcount:
            print("Equipment found in slot: ", current_index)
            return current_index

def addAbility(*, owner, equipment_type, ability_array=[], ability_index, slotcount, navigateToEquipMenu=False, exitOutOfCurrentWeapon=True, closeMenu=True, fullMenuClose=True):
    if navigateToEquipMenu:
        if not FFX_memory.menuOpen():
            FFX_memory.openMenu()
        while FFX_memory.getMenuCursorPos() != 8:
            FFX_memory.menuDirection(FFX_memory.getMenuCursorPos(), 8, 11)
        while FFX_memory.menuNumber() == 5:
            FFX_Xbox.tapB()
    item_to_modify = findEquipmentIndex(owner=owner, equipment_type=equipment_type, ability_array=ability_array, slotcount=slotcount)
    while FFX_memory.itemMenuRow() != item_to_modify:
        if FFX_memory.itemMenuRow() < item_to_modify:
            if item_to_modify - FFX_memory.itemMenuRow() > 5:
                FFX_Xbox.TriggerR()
            else:
                FFX_Xbox.tapDown()
        else:
            if FFX_memory.itemMenuRow() - item_to_modify > 5 and FFX_memory.itemMenuRow() > 8:
                FFX_Xbox.TriggerL()
            else:
                FFX_Xbox.tapUp()
    while not FFX_memory.cureMenuOpen():
        FFX_Xbox.tapB()
    while FFX_memory.assignAbilityToEquipCursor() != ability_index:
        if FFX_memory.assignAbilityToEquipCursor() < ability_index:
            FFX_Xbox.tapDown() 
        else:
            FFX_Xbox.tapUp()
    while FFX_memory.informationActive():
        FFX_Xbox.tapB()
    while FFX_memory.equipBuyRow() != 1:
        pass
    while FFX_memory.equipBuyRow() != 0:
        FFX_Xbox.tapUp()
    while not FFX_memory.informationActive():
        FFX_Xbox.tapB()
    if exitOutOfCurrentWeapon:
        while FFX_memory.cureMenuOpen():
            FFX_Xbox.tapA()
    if closeMenu:
        if fullMenuClose:
            FFX_memory.closeMenu()
        else:
            FFX_memory.backToMainMenu()
            
            
def addFirstStrike(*, owner, equipment_type, ability_array=[], slotcount, navigateToEquipMenu=False, exitOutOfCurrentWeapon=True, closeMenu=True, fullMenuClose=True):
    addAbility(owner=owner, equipment_type=equipment_type, ability_array=ability_array, ability_index=2, slotcount=slotcount, navigateToEquipMenu=navigateToEquipMenu, exitOutOfCurrentWeapon=exitOutOfCurrentWeapon, closeMenu=closeMenu, fullMenuClose=fullMenuClose)
    

def auronFirstStrike():
    print("Starting Auron")
    addFirstStrike(owner=2, equipment_type=0, ability_array=[0x800B, 0x8063, 255, 255], slotcount=3, closeMenu=True, fullMenuClose=False, navigateToEquipMenu=False)
    print("Done with Auron")

def yunaFirstStrike():
    print("Starting Yuna")
    addFirstStrike(owner=1, equipment_type=0, slotcount=1, closeMenu=False, navigateToEquipMenu=True)
    print("Done with Yuna")

def afterFlux():
    openGrid(character=0)
    
    #Sphere grid on Tidus
    FFX_menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('ability','d','none')
    FFX_menuGrid.useAndQuit()

def gagazetCave():
    #Occurs after swimming
    FFX_memory.openMenu()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Yuna to slot 2
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Auron to slot 3
    FFX_memory.closeMenu()

def zombieStrikeBackup():
    openGrid(character=0)
    
    FFX_menuGrid.moveFirst()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('lv4','d','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('ability','u','none')
    FFX_menuGrid.useAndQuit()
    #FFX_memory.closeMenu()



def BFA():
    openGrid(character=1) #Yuna final grid
    
    FFX_menuGrid.useFirst()
    
    if gameVars.endGameVersion() == 3:
        FFX_menuGrid.selSphere('attribute','d','none')
        FFX_menuGrid.useAndUseAgain()
    else:
        FFX_menuGrid.selSphere('attribute','d','l5')
        FFX_memory.waitFrames(30 * 0.07)
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('ret','d','torikku')
        FFX_memory.waitFrames(30 * 0.07)
        FFX_menuGrid.useAndMove()
        gridDown()
        gridDown()
        gridLeft()
        gridDown()
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('speed','u','none')
        FFX_menuGrid.useAndMove()
        gridDown()
        gridDown()
        gridDown()
        FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('ability','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','u','left')
    
    if gameVars.endGameVersion() == 3:
        FFX_menuGrid.useAndMove()
        #time.sleep(60) #Two minute buffer to figure out what we're doing.
        gridRight() #Not sure exactly
        gridRight()
        gridRight()
        gridRight()
        gridRight()
        gridRight()
        gridRight()
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('speed','u','none')
        FFX_menuGrid.useAndMove()
        gridDown()
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('speed','u','none')
    
    if FFX_memory.overdriveState()[6] != 100:
        FFX_menuGrid.useShiftLeft('Rikku')
        FFX_menuGrid.useFirst()
        FFX_menuGrid.selSphere('skill','d','up')
    
    if gameVars.zombieWeapon() == 255:
        FFX_menuGrid.useShiftLeft('tidus')
        FFX_menuGrid.moveFirst()
        gridUp()
        gridUp()
        gridUp()
        gridUp()
        gridUp()
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('lv4','d','none')
        FFX_menuGrid.useAndMove()
        gridUp()
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('ability','u','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def skReturn():
    openGrid(character=1)
    FFX_menuGrid.useFirst()
    FFX_menuGrid.selSphere('friend','d','d2')
    FFX_menuGrid.useAndUseAgain() #Friend sphere to Lulu
    FFX_menuGrid.selSphere('luck','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('fortune','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndQuit()

def skMixed():
    openGrid(character=1)
    FFX_menuGrid.useFirst()
    FFX_menuGrid.selSphere('ret','d','r2')
    FFX_menuGrid.useAndMove() #Return to Wakka's grid
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('mana','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('lv1','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('luck','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('fortune','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridDown()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndQuit()

def skFriend():
    #First to do the First Strike stuff we couldn't do earlier.
    FFX_memory.openMenu()
    yunaFirstStrike()
    auronFirstStrike()
    equipWeapon(character=2, ability=0x8001, fullMenuClose=False)
    if gameVars.usePause():
        FFX_memory.waitFrames(5)
    
    #Now sphere grid
    openGrid(character=1)
    FFX_menuGrid.moveFirst()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('luck','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('fortune','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def skReturn2():
    openGrid(character=1)
    
    FFX_menuGrid.useFirst()
    FFX_menuGrid.selSphere('ret','d','aftersk')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndQuit()


def openGrid(character):
    try:
        FFXC.set_neutral()
    except:
        FFXC = FFX_Xbox.controllerHandle()
        FFXC.set_neutral()
    while not FFX_memory.sGridActive():
        #print("Attempting to open Sphere Grid")
        if FFX_memory.userControl() and not FFX_memory.menuOpen():
         #   print("Menu is not open at all")
            FFX_Xbox.tapY()
        elif FFX_memory.menuNumber() == 5: #Cursor on main menu
          #  print("Main menu cursor")
            while FFX_memory.getMenuCursorPos() != 0:
                FFX_memory.menuDirection(FFX_memory.getMenuCursorPos(), 0, 11)
           # print("Done with menu cursor")
            while FFX_memory.menuNumber() == 5:
                FFX_Xbox.tapB()
        elif FFX_memory.menuNumber() == 7: #Cursor selecting party member
            print("Selecting party member")
            target_pos = FFX_memory.getCharacterIndexInMainMenu(character)
            while FFX_memory.getCharCursorPos() != target_pos:
                if FFX_memory.getStoryProgress() == 2528: #After B&Y, party size is evaluated weird.
                    FFX_memory.menuDirection(FFX_memory.getCharCursorPos(), target_pos, 7)
                elif FFX_memory.partySize() < 3:
                    FFX_Xbox.menuDown()
                else:
                    #FFX_memory.menuDirection(FFX_memory.getCharCursorPos(), target_pos, FFX_memory.partySize())
                    #Not working. Use this instead.
                    FFX_memory.menuDirection(FFX_memory.getCharCursorPos(), target_pos, 7)
            while FFX_memory.menuNumber() == 7:
                FFX_Xbox.menuB()
            try:
                FFXC.set_neutral()
            except:
                FFXC = FFX_Xbox.controllerHandle()
                FFXC.set_neutral()
    try:
        FFXC.set_neutral()
    except:
        FFXC = FFX_Xbox.controllerHandle()
        FFXC.set_neutral()

