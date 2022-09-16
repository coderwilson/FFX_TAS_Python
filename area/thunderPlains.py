import xbox
import screen
import battle
import menu
import memory
import targetPathing
import vars
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def southPathing():
    memory.clickToControl()

    gameVars.setLStrike(memory.lStrikeCount())

    memory.fullPartyFormat('postbunyip')
    memory.closeMenu()
    count50 = 0
    checkpoint = 0
    while memory.getMap() != 256:
        if memory.userControl():
            # Lightning dodging
            if memory.dodgeLightning(gameVars.getLStrike()):
                gameVars.setLStrike(memory.lStrikeCount())
                if checkpoint == 34:
                    count50 += 1
                    print("Dodge:", count50)
            elif checkpoint == 2 and gameVars.nemesis():
                checkpoint = 20
            elif checkpoint == 21:
                # memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 25:
                while memory.userControl():
                    targetPathing.setMovement([-175, -487])
                    xbox.tapX()
                checkpoint += 1
            elif checkpoint == 33:
                while memory.userControl():
                    targetPathing.setMovement([205, 160])
                    xbox.tapX()
                checkpoint += 1
                print("Now ready to dodge some lightning.")
            elif checkpoint == 34:
                if count50 == 50:
                    checkpoint += 1
                else:  # Dodging fifty bolts.
                    FFXC.set_neutral()
            elif checkpoint == 39:  # Back to the normal path
                checkpoint = 10

            # General pathing
            elif memory.userControl():
                if targetPathing.setMovement(targetPathing.tPlainsSouth(checkpoint)):
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible() and not memory.battleActive():
                xbox.menuB()
            elif screen.BattleScreen():
                battle.thunderPlains(1)
            elif memory.menuOpen():
                xbox.tapB()

    memory.awaitControl()
    FFXC.set_movement(0, 1)
    memory.waitFrames(30 * 0.5)
    FFXC.set_movement(-1, 1)
    while not memory.getMap() == 263:
        if memory.diagSkipPossible():
            xbox.menuB()
    FFXC.set_neutral()
    menu.autoSortEquipment()


def agencyShop():
    speedCount = memory.getSpeed()

    # 15 plus two (Spherimorph, Flux), minus 1 because it starts on 1
    speedNeeded = max(0, min(2, 14 - speedCount))
    grenade_slot = memory.getItemSlot(35)
    if grenade_slot == 255:
        cur_grenades = 0
    else:
        cur_grenades = memory.getItemCountSlot(grenade_slot)
    total_grenades_needed = 3 + speedNeeded - cur_grenades
    memory.clickToDiagProgress(92)
    while memory.shopMenuDialogueRow() != 2:
        xbox.tapDown()  # Select "Got any items?"
    while not memory.itemShopMenu() == 7:
        xbox.tapB()  # Click through until items menu comes up
    while not memory.itemShopMenu() == 10:
        xbox.tapB()  # Select buy command

    # For safety (Wendigo is the worst), buying extra phoenix downs first.
    while memory.equipBuyRow() != 1:  # Buy some phoenix downs first
        if memory.equipBuyRow() < 1:
            xbox.tapDown()
        else:
            xbox.tapUp()
    while not memory.itemShopMenu() == 16:
        xbox.tapB()
    while memory.purchasingAmountItems() != 4:
        if memory.purchasingAmountItems() < 4:
            xbox.tapRight()
        else:
            xbox.tapLeft()
    while not memory.itemShopMenu() == 10:
        # Should result in +8 phoenix downs. Can be dialed in later.
        xbox.tapB()

    if total_grenades_needed:
        # Then buying grenades for multiple uses through the rest of the run.
        while memory.equipBuyRow() != 6:
            if memory.equipBuyRow() < 6:
                xbox.tapDown()
            else:
                xbox.tapUp()
        while not memory.itemShopMenu() == 16:
            xbox.tapB()
        while memory.purchasingAmountItems() != total_grenades_needed:
            if memory.purchasingAmountItems() < total_grenades_needed:
                xbox.tapRight()
            else:
                xbox.tapLeft()
        while not memory.itemShopMenu() == 10:
            xbox.tapB()
    memory.closeMenu()

    # Next, Grab Auron's weapon
    xbox.SkipDialog(0.1)
    FFXC.set_neutral()
    memory.clickToDiagProgress(90)
    memory.clickToDiagProgress(92)
    while memory.shopMenuDialogueRow() != 1:
        xbox.tapDown()
    all_equipment = memory.allEquipment()
    tidus_longsword = [i for i, handle in enumerate(all_equipment) if (
        handle.abilities() == [255, 255, 255, 255] and handle.owner() == 0)][0]
    print("Tidus Longsword in slot:", tidus_longsword)
    auron_katana = [i for i, handle in enumerate(all_equipment) if (
        handle.abilities() == [0x800B, 255, 255, 255] and handle.owner() == 2)][0]
    print("Auron Katana in slot:", auron_katana)
    other_slots = [i for i, handle in enumerate(all_equipment) if (
        i not in [tidus_longsword, auron_katana] and handle.equipStatus == 255 and not handle.isBrotherhood())]
    print("Sellable Items in :", other_slots)
    menu.sellWeapon(tidus_longsword)
    menu.sellWeapon(auron_katana)
    if gameVars.getBlitzWin() and memory.getGilvalue() < 8725:
        for loc in other_slots:
            menu.sellWeapon(loc)
            if memory.getGilvalue() >= 8725:
                break
    elif not gameVars.getBlitzWin() and memory.getGilvalue() < 9550:
        for loc in other_slots:
            menu.sellWeapon(loc)
            if memory.getGilvalue() >= 9550:
                break
    if not gameVars.getBlitzWin():
        menu.buyWeapon(0, equip=False)
    menu.buyWeapon(5, equip=False)
    memory.closeMenu()


def agency():
    # Arrive at the travel agency
    memory.clickToControl3()
    checkpoint = 0

    while memory.getMap() != 162:
        strCount = memory.getItemCountSlot(memory.getItemSlot(87))
        if memory.userControl():
            if checkpoint == 1:
                while not memory.diagSkipPossible():
                    targetPathing.setMovement([2, -31])
                    xbox.tapB()
                    memory.waitFrames(3)
                FFXC.set_neutral()
                agencyShop()
                checkpoint += 1
            elif checkpoint == 4:
                FFXC.set_movement(0, 1)
                memory.awaitEvent()
                FFXC.set_neutral()
                memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 7:
                if not gameVars.csr():
                    kimahriAffection = memory.affectionArray()[3]
                    print("Kimahri affection, ", kimahriAffection)
                    while memory.affectionArray()[3] == kimahriAffection:
                        targetPathing.setMovement([27, -44])
                        xbox.tapB()
                    print("Updated, full affection array:")
                    print(memory.affectionArray())
                checkpoint += 1
            elif checkpoint == 8:
                while not memory.getMap() == 256:
                    targetPathing.setMovement([3, -52])
                    xbox.tapB()
                memory.clickToControl()
                if gameVars.nemesis():
                    # Back in and out to spawn the chest
                    FFXC.set_movement(-1, 1)
                    while memory.getMap() != 263:
                        pass
                    FFXC.set_neutral()
                    memory.waitFrames(3)
                    while memory.getMap() != 256:
                        targetPathing.setMovement([3, -150])
                        xbox.tapB()
                    FFXC.set_neutral()
                    memory.awaitControl()
                checkpoint += 1
            elif checkpoint == 9 and gameVars.nemesis() and strCount < 3:
                targetPathing.setMovement([-73, 45])
                xbox.tapB()
            elif checkpoint == 11:
                FFXC.set_movement(0, 1)
                memory.clickToEvent()

            elif targetPathing.setMovement(targetPathing.tPlainsAgency(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible():
                xbox.tapB()


def northPathing():
    memory.clickToControl()

    lStrikeCount = memory.lStrikeCount()
    lunarSlot = memory.getItemSlot(56) != 255

    checkpoint = 0
    while memory.getMap() != 110:
        if memory.userControl():
            # Lightning dodging
            if memory.dodgeLightning(lStrikeCount):
                print("Dodge")
                lStrikeCount = memory.lStrikeCount()
            elif gameVars.csr() and checkpoint == 14:
                checkpoint = 16
            elif checkpoint == 17 and not gameVars.getBlitzWin() and not lunarSlot:
                checkpoint -= 2
                print("No lunar curtain. Checkpoint:", checkpoint)

            # General pathing
            elif memory.userControl():
                if targetPathing.setMovement(targetPathing.tPlainsNorth(checkpoint)):
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.diagSkipPossible() and not memory.battleActive():
                xbox.menuB()
            if screen.BattleScreen():
                battle.thunderPlains(1)
                lunarSlot = memory.getItemSlot(56) != 255
            elif memory.menuOpen():
                xbox.tapB()

    FFXC.set_neutral()
    memory.awaitControl()
    print("Thunder Plains North complete. Moving up to the Macalania save sphere.")
    if not gameVars.csr():
        FFXC.set_movement(0, 1)
        xbox.SkipDialog(6)
        FFXC.set_neutral()

        # Conversation with Auron about Yuna being hard to guard.
        memory.clickToControl3()

        FFXC.set_movement(1, 1)
        memory.waitFrames(30 * 2)
        FFXC.set_movement(0, 1)
        xbox.SkipDialog(6)
        FFXC.set_neutral()  # Approaching the party

    else:
        while not targetPathing.setMovement([258, -7]):
            pass
