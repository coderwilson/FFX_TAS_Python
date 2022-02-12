import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_memory
import FFX_targetPathing
import FFX_vars
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

def southPathing(status):
    FFX_memory.clickToControl()
    
    gameVars.setLStrike(FFX_memory.lStrikeCount())
    
    speedcount = FFX_memory.getSpeed()
    if speedcount >= 14:
        status[3] = True
    
    FFX_memory.fullPartyFormat('postbunyip')
    FFX_memory.closeMenu()
    lStrikeCount = FFX_memory.lStrikeCount()
    
    checkpoint = 0
    while FFX_memory.getMap() != 256:
        if FFX_memory.userControl():
            #Lightning dodging
            if FFX_memory.dodgeLightning(gameVars.getLStrike()):
                print("Dodge")
                gameVars.setLStrike(FFX_memory.lStrikeCount())
            
            #General pathing
            elif FFX_memory.userControl():
                if FFX_targetPathing.setMovement(FFX_targetPathing.tPlainsSouth(checkpoint)) == True:
                    checkpoint += 1
                    print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible() and not FFX_memory.battleActive():
                FFX_Xbox.menuB()
            if FFX_Screen.BattleScreen():
                status = FFX_Battle.thunderPlains(status, 1)
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
    
    FFX_memory.awaitControl()
    FFXC.set_movement(0, 1)
    FFX_memory.waitFrames(30 * 0.5)
    FFXC.set_movement(-1, 1)
    while not FFX_memory.getMap() == 263:
        if FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
    FFXC.set_neutral()
    complete = 1

    return status

def agencyShop():
    speedCount = FFX_memory.getSpeed()
    
    
    speedNeeded = max(0, min(2, 14 - speedCount)) #15 plus two (Spherimorph, Flux), minus 1 because it starts on 1
    grenade_slot = FFX_memory.getItemSlot(35)
    if grenade_slot == 255:
        cur_grenades = 0
    else:
        cur_grenades = FFX_memory.getItemCountSlot(grenade_slot)
    total_grenades_needed = 3 + speedNeeded - cur_grenades
    if total_grenades_needed:
        FFX_memory.clickToDiagProgress(92)
        while FFX_memory.blitzCharSelectCursor() != 2:
            FFX_Xbox.tapDown()
        while not FFX_memory.itemShopMenu() == 7:
            FFX_Xbox.tapB()
        while not FFX_memory.itemShopMenu() == 10:
            FFX_Xbox.tapB()
        while FFX_memory.equipBuyRow() != 6:
            if FFX_memory.equipBuyRow() < 6:
                FFX_Xbox.tapDown()
            else:
                FFX_Xbox.tapUp()
        while not FFX_memory.itemShopMenu() == 16:
            FFX_Xbox.tapB()
        while FFX_memory.purchasingAmountItems() != total_grenades_needed:
            if FFX_memory.purchasingAmountItems() < total_grenades_needed:
                FFX_Xbox.tapRight()
            else:
                FFX_Xbox.tapLeft()
        while not FFX_memory.itemShopMenu() == 10:
            FFX_Xbox.tapB()
        FFX_memory.closeMenu()
    
    #Next, Grab Auron's weapon
    FFX_Xbox.SkipDialog(0.1)
    FFXC.set_neutral()
    FFX_memory.clickToDiagProgress(90)
    FFX_memory.clickToDiagProgress(92)
    while FFX_memory.blitzCharSelectCursor() != 1:
        FFX_Xbox.tapDown()
    all_equipment = FFX_memory.allEquipment()    
    tidus_longsword = [i for i, handle in enumerate(all_equipment) if (handle.abilities() == [255, 255, 255, 255] and handle.owner() == 0)][0]
    print("Tidus Longsword in slot: ", tidus_longsword)
    auron_katana = [i for i, handle in enumerate(all_equipment) if (handle.abilities() == [0x800B, 255, 255, 255] and handle.owner() == 2)][0]
    print("Auron Katana in slot: ", auron_katana)
    other_slots = [i for i, handle in enumerate(all_equipment) if (i not in [tidus_longsword, auron_katana] and handle.equipStatus == 255)]
    print("Sellable Items in : ", other_slots)
    FFX_menu.sellWeapon(tidus_longsword)
    FFX_menu.sellWeapon(auron_katana)
    if gameVars.getBlitzWin() and FFX_memory.getGilvalue() < 8725:
        for loc in other_slots:
            FFX_menu.sellWeapon(loc)
            if FFX_memory.getGilvalue() >= 8725: break
    elif not gameVars.getBlitzWin() and FFX_memory.getGilvalue() < 9550:
        for loc in other_slots:
            FFX_menu.sellWeapon(loc)
            if FFX_memory.getGilvalue() >= 9550: break
    if not gameVars.getBlitzWin():
        FFX_menu.buyWeapon(0, equip=False)
    FFX_menu.buyWeapon(5, equip=False)
    FFX_memory.closeMenu()

def agency():
    #Arrive at the travel agency
    FFX_memory.clickToControl3()
    checkpoint = 0
    
    while FFX_memory.getMap() != 162:
        if FFX_memory.userControl():
            if checkpoint == 1:
                while not FFX_memory.diagSkipPossible():
                    FFX_targetPathing.setMovement([2,-31])
                    FFX_Xbox.tapB()
                    FFX_memory.waitFrames(3)
                FFXC.set_neutral()
                agencyShop()
                checkpoint += 1
            elif checkpoint == 4:
                FFXC.set_movement(0, 1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 7:
                kimahriAffection = FFX_memory.affectionArray()[3]
                print("Kimahri affection, ", kimahriAffection)
                while FFX_memory.affectionArray()[3] == kimahriAffection:
                    FFX_targetPathing.setMovement([27, -44])
                    FFX_Xbox.tapB()
                print("Updated, full affection array:")
                print(FFX_memory.affectionArray())
                checkpoint += 1
            elif checkpoint == 8:
                while not FFX_memory.getMap() == 256:
                    FFX_targetPathing.setMovement([3, -52])
                    FFX_Xbox.tapB()
                checkpoint += 1
            elif checkpoint == 10:
                FFXC.set_movement(0, 1)
                FFX_memory.clickToEvent()
            
            elif FFX_targetPathing.setMovement(FFX_targetPathing.tPlainsAgency(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    
def northPathing(status):
    FFX_memory.clickToControl()
    
    lStrikeCount = FFX_memory.lStrikeCount()
    
    checkpoint = 0
    while FFX_memory.getMap() != 110:
        if FFX_memory.userControl():
            #Lightning dodging
            if FFX_memory.dodgeLightning(lStrikeCount):
                print("Dodge")
                lStrikeCount = FFX_memory.lStrikeCount()
            elif checkpoint == 12 and status[4] == False and status[2] == False:
                checkpoint = 10
            
            #General pathing
            elif FFX_memory.userControl():
                if FFX_targetPathing.setMovement(FFX_targetPathing.tPlainsNorth(checkpoint)) == True:
                    checkpoint += 1
                    print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible() and not FFX_memory.battleActive():
                FFX_Xbox.menuB()
            if FFX_Screen.BattleScreen():
                status = FFX_Battle.thunderPlains(status, 1)
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
    
    FFXC.set_neutral()
    FFX_memory.awaitControl()
    print("Thunder Plains North complete. Moving up to the Macalania save sphere.")
    if not gameVars.csr():
        FFXC.set_movement(0, 1)
        FFX_Xbox.SkipDialog(6)
        FFXC.set_neutral()
        
        FFX_memory.clickToControl3() # Conversation with Auron about Yuna being hard to guard.
        
        FFXC.set_movement(1, 1)
        FFX_memory.waitFrames(30 * 2)
        FFXC.set_movement(0, 1)
        FFX_Xbox.SkipDialog(6)
        FFXC.set_neutral() #Approaching the party
    
    else:
        while not FFX_targetPathing.setMovement([258,-7]):
            pass

    return status
