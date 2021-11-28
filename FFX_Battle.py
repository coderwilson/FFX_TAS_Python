import FFX_Xbox
import FFX_Screen
import time
import FFX_Logs
import FFX_memory

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC


def defend():
    print("Defend command")
    FFXC.set_value('BtnY', 1)
    time.sleep(0.035)
    FFXC.set_value('BtnY', 0)
    time.sleep(0.035)
    FFXC.set_value('BtnY', 1)
    time.sleep(0.035)
    FFXC.set_value('BtnY', 0)
    time.sleep(0.035)
    FFXC.set_value('BtnY', 1)
    time.sleep(0.035)
    FFXC.set_value('BtnY', 0)
    time.sleep(0.035)
    FFXC.set_value('BtnY', 1)
    time.sleep(0.035)
    FFXC.set_value('BtnY', 0)
    time.sleep(0.035)
    FFXC.set_value('BtnY', 1)
    time.sleep(0.035)
    FFXC.set_value('BtnY', 0)
    time.sleep(0.035)
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()


def tidusFlee():
    print("Tidus Flee (or similar command pattern)")
    if FFX_memory.otherBattleMenu():
        while FFX_memory.otherBattleMenu():
            FFX_Xbox.menuA()
    while FFX_memory.battleMenuCursor() != 20:
        print(FFX_memory.battleMenuCursor()) #Testing only
        if FFX_Screen.turnTidus() == False:
            break
        if FFX_memory.battleMenuCursor() == 255:
            time.sleep(0.01)
        elif FFX_memory.battleMenuCursor() == 1:
            FFX_Xbox.menuUp()
        elif FFX_memory.battleMenuCursor() > 20:
            FFX_Xbox.menuUp()
        else:
            FFX_Xbox.menuDown()
        FFXC.set_neutral()
        time.sleep(0.035)
    FFX_Xbox.SkipDialog(1.5)

def tidusHaste(direction):
    direction = direction.lower()
    while FFX_memory.battleMenuCursor() != 22:
        if FFX_Screen.turnTidus() == False:
            print("Attempting Haste, but it's not Tidus's turn")
            FFX_Xbox.menuUp()
            FFX_Xbox.menuUp()
            return
        if FFX_memory.battleMenuCursor() == 1:
            FFX_Xbox.menuUp()
        else:
            FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.3)
    FFX_Xbox.menuB()
    time.sleep(0.3)
    if direction == 'left':
        FFX_Xbox.menuLeft()
    if direction == 'right':
        FFX_Xbox.menuRight()
    if direction == 'up':
        FFX_Xbox.menuUp()
    if direction == 'down':
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    time.sleep(0.8)

def tidusHasteLate(direction):
    tidusHaste(direction)

def lateHaste(direction):
    tidusHaste(direction)

def useSkill(position):
    print("Using skill in position: ", position)
    while FFX_memory.battleMenuCursor() != 19:
        print(FFX_memory.battleMenuCursor())
        if FFX_memory.battleMenuCursor() == 255:
            time.sleep(0.01)
        elif FFX_memory.battleMenuCursor() == 1:
            FFX_Xbox.menuUp()
            time.sleep(0.1)
        elif FFX_memory.battleMenuCursor() > 19:
            FFX_Xbox.menuUp()
            time.sleep(0.1)
        else:
            FFX_Xbox.menuDown()
    if position == 0:
        FFX_Xbox.SkipDialog(1.5)
    else:
        FFX_Xbox.menuB()
        time.sleep(0.035)
        while FFX_memory.battleCursor2() != position:
            if position % 2 == 0 and FFX_memory.battleCursor2() % 2 == 1:
                FFX_Xbox.menuLeft()
            elif position % 2 == 1 and FFX_memory.battleCursor2() % 2 == 0:
                FFX_Xbox.menuRight()
            elif position > FFX_memory.battleCursor2():
                FFX_Xbox.menuDown()
            else:
                FFX_Xbox.menuUp()
    FFX_Xbox.SkipDialog(1)


def tidusOD():
    print("Tidus overdrive activating")
    while not FFX_memory.otherBattleMenu():
        FFX_Xbox.menuLeft()
    FFX_Xbox.SkipDialog(2)
    while not FFX_Screen.PixelTestTol(1239, 436, (191, 186, 208), 10):
        doNothing = True
    time.sleep(0.43)  # First try every time?
    FFX_Xbox.menuB()
    time.sleep(0.25)
    FFX_Xbox.menuB()
    time.sleep(0.3)
    FFX_Xbox.menuB()
    time.sleep(0.35)
    FFX_Xbox.menuB()


def tidusODSeymour():
    print("Tidus overdrive activating")
    FFX_Screen.awaitTurn()
    while not FFX_memory.otherBattleMenu():
        FFX_Xbox.menuLeft()
    time.sleep(0.8)
    FFX_Xbox.menuB()
    time.sleep(0.4)
    FFX_Xbox.menuB()
    time.sleep(0.4)
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuB()  # Activate overdrive
    time.sleep(0.4)
    while not FFX_Screen.PixelTestTol(1239, 436, (191, 186, 208), 10):
        doNothing = True
    time.sleep(0.43)  # First try every time?
    FFX_Xbox.menuB()
    time.sleep(0.25)
    FFX_Xbox.menuB()
    time.sleep(0.3)
    FFX_Xbox.menuB()
    time.sleep(0.3)
    FFX_Xbox.menuB()
    time.sleep(0.35)
    FFX_Xbox.menuB()
    time.sleep(0.35)
    FFX_Xbox.menuB()
    time.sleep(0.3)
    FFX_Xbox.menuB()
    time.sleep(0.25)
    FFX_Xbox.menuB()


def remedy(healerposition: int, targetposition: int, direction: str):
    print("Remedy")
    if FFX_memory.getThrowItemsSlot(15) < 255:
        itemnum = 15
        itemname = "Remedy"
    else:
        itemnum = -1
        itemname = "noitemfound"
    if itemnum >= 0:

        FFX_Logs.writeLog("Using %s" % itemname)
        print("Using %s" % itemname)
        if FFX_Screen.PixelTestTol(277, 726, (223, 223, 223), 5):
            FFX_Xbox.menuDown()
        else:
            while not FFX_Screen.PixelTestTol(276, 769, (218, 218, 218), 5):  # Item option isn't showing up
                if FFX_Screen.BattleComplete():
                    return
                FFX_Xbox.menuDown()
            while not FFX_Screen.PixelTestTol(130, 779, (165, 167, 165),
                                              5):  # Item option isn't selected (it's always last)
                if FFX_Screen.BattleComplete():
                    return
                FFX_Xbox.menuDown()
        FFX_Xbox.menuB()  # Item menu open.
        time.sleep(0.3)
        cursor = 1
        itemPos = FFX_memory.getThrowItemsSlot(itemnum)
        if itemPos % 2 == 0:
            FFX_Xbox.menuRight()
            cursor += 1
        if cursor == itemPos:
            FFX_Xbox.menuB()
        else:
            while cursor != itemPos:
                FFX_Xbox.menuDown()
                cursor += 2
            FFX_Xbox.menuB()
        print("Direction: ", direction)
        direction = direction.lower()
        if (targetposition - healerposition) % 3 == 1:
            if direction == "left":
                FFX_Xbox.menuLeft()
            elif direction == "right":
                FFX_Xbox.menuRight()
            elif direction == "up":
                FFX_Xbox.menuUp()
            elif direction == "down":
                FFX_Xbox.menuDown()
        elif (targetposition - healerposition) % 3 == 2:
            if direction == "left":
                FFX_Xbox.menuRight()
            elif direction == "right":
                FFX_Xbox.menuLeft()
            elif direction == "up":
                FFX_Xbox.menuDown()
            elif direction == "down":
                FFX_Xbox.menuUp()

        FFX_Xbox.menuB()
        FFX_Xbox.menuB()

        return 1

    else:
        print("No restorative items available")
        return 0


def revive():
    FFX_Logs.writeLog("Using Phoenix Down")
    print("Using Phoenix Down")
    if FFX_memory.getThrowItemsSlot(6) > 250:
        fleeAll()
        return
    while FFX_memory.battleMenuCursor() != 1:
        FFX_Xbox.menuDown()
    time.sleep(0.035)
    FFX_Xbox.menuB()  # Item menu open.
    time.sleep(0.035)
    itemPos = FFX_memory.getThrowItemsSlot(6) - 1
    while FFX_memory.battleCursor2() != itemPos:
        print(FFX_memory.battleCursor2()," | ", itemPos)
        if FFX_memory.battleCursor2() == 0:
            FFX_Xbox.menuDown()
        elif itemPos % 2 == 0 and FFX_memory.battleCursor2() % 2 == 1:
            FFX_Xbox.menuRight()
        elif itemPos % 2 == 1 and FFX_memory.battleCursor2() % 2 == 0:
            FFX_Xbox.menuLeft()
        elif itemPos > FFX_memory.battleCursor2():
            FFX_Xbox.menuDown()
        else:
            FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()


def reviveAll():
    FFX_Logs.writeLog("Using Mega Phoenix Down")
    print("Using Mega Phoenix Down")
    while FFX_memory.battleMenuCursor() != 1:
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()  # Item menu open.
    time.sleep(0.3)
    cursor = 1
    itemPos = FFX_memory.getThrowItemsSlot(7)
    if itemPos % 2 == 0:
        FFX_Xbox.menuRight()
        cursor += 1
    if cursor == itemPos:  # P.downs are in slot 2
        FFX_Xbox.menuB()
    else:
        while cursor != itemPos:  # If not slot 2, scroll down until we find phoenix downs.
            FFX_Xbox.menuDown()
            cursor += 2
        FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()


def FinishWithAttacksOnly():
    print("Finish with attacks only")
    BattleComplete = 0
    countAttacks = 0
    countRevives = 0

    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            if FFX_Screen.faintCheck() > 0:
                revive()
                countRevives += 1
            else:
                attack('none')
                countAttacks += 1
        if FFX_Screen.BattleComplete():
            print("Victory Screen")
            FFXC.set_value("BtnB", 1)
            time.sleep(2.4)
            FFXC.set_value("BtnB", 0)
            BattleComplete = 1
            FFX_Logs.writeStats("Attack-only battle. Attacks: " + str(countAttacks))
            FFX_Logs.writeStats("Attack-only battle. Revives: " + str(countRevives))


def selfPot():
    print("Self potion")
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.SkipDialog(2)


def Ammes():
    FFX_Logs.writeLog("Fight start: Ammes")
    BattleComplete = 0
    countAttacks = 0
    countRevives = 0

    tidusODflag = False

    while BattleComplete != 1:
        if FFX_memory.turnReady():
            if tidusODflag == False and FFX_Screen.turnTidus() and FFX_Screen.checkCharge(1):
                tidusOD()
                tidusODflag = True
            else:
                print("Attacking Sinspawn Ammes")
                attack('none')
                countAttacks += 1
        if FFX_memory.userControl():
            BattleComplete = 1
            print("Ammes battle complete")
            FFX_Logs.writeStats("Sinspawn Ammes Attacks:")
            FFX_Logs.writeStats(str(countAttacks))

def Tanker():
    FFX_Logs.writeLog("Fight start: Tanker")
    print("Fight start: Tanker")
    BattleComplete = 0
    countAttacks = 0
    tidusCount = 0
    auronCount = 0
    FFX_Xbox.clickToBattle()

    while not FFX_memory.battleComplete():
        if FFX_memory.turnReady():
            if FFX_Screen.turnTidus():
                tidusCount += 1
                if tidusCount < 4:
                    FFX_Xbox.weapSwap(0)
                    time.sleep(0.5)
                else:
                    attack('none')
                    countAttacks += 1
            elif FFX_Screen.turnAuron():
                auronCount += 1
                if auronCount < 2:
                    time.sleep(0.5)
                    FFX_Xbox.menuB()
                    time.sleep(0.1)
                    FFX_Xbox.menuDown()
                    FFX_Xbox.menuLeft()
                    FFX_Xbox.menuB()
                else:
                    attack('none')
                    countAttacks += 1
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
    FFX_Logs.writeStats("Tanker Attacks:")
    FFX_Logs.writeStats(str(countAttacks))

def Klikk():
    print("Fight start: Klikk")
    rikkuSteal = 0
    klikkAttacks = 0
    klikkRevives = 0
    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            BattleHP = FFX_memory.getBattleHP()
            if BattleHP[1] == 0 or BattleHP[2] == 0:
                revive()
                klikkRevives += 1
            elif FFX_Screen.turnTidus():
                if BattleHP[1] < 120:
                    FFX_Xbox.menuDown()
                    FFX_Xbox.menuDown()
                    FFX_Xbox.menuB()
                    time.sleep(0.4)
                    FFX_Xbox.menuB()
                    FFX_Xbox.menuB()
                    FFX_Xbox.menuB()
                    FFX_Xbox.menuB()
                    FFX_Xbox.menuB()
                    klikkRevives += 1
                else:
                    attack('none')
                    klikkAttacks += 1
            elif FFX_Screen.turnRikkuRed():
                if rikkuSteal == 0:
                    print("Attempting to steal from Klikk")
                    Steal()
                    rikkuSteal = 1
                elif BattleHP[2] < 110:
                    FFX_Xbox.menuDown()
                    FFX_Xbox.menuDown()
                    FFX_Xbox.menuB()
                    time.sleep(0.4)
                    FFX_Xbox.menuB()
                    FFX_Xbox.menuB()
                    FFX_Xbox.menuB()
                    FFX_Xbox.menuB()
                    FFX_Xbox.menuB()
                    klikkRevives += 1
                else:
                    attack('none')
                    klikkAttacks += 1
        else:
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    print("Klikk fight complete")
    FFX_Logs.writeStats("Klikk Attacks:")
    FFX_Logs.writeStats(str(klikkAttacks))
    FFX_Logs.writeStats("Klikk items used:")
    FFX_Logs.writeStats(str(klikkRevives))
    FFX_memory.clickToControl()  # Maybe not skippable dialog, but whatever.

def Tros():
    FFX_Logs.writeLog("Fight start: Tros")
    print("Fight start: Tros")
    FFXC.set_neutral()
    battleClock = 0
    Attacks = 0
    Revives = 0
    Grenades = 0
    Steals = 0
    
    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
        elif FFX_memory.turnReady():
            battleClock += 1
            print("Battle clock:", battleClock)
            trosPos = 2
            print("Determining Tros position")
            while trosPos == 2:  # Two for "not yet determined". Maybe can be HP-based instead?
                camera = FFX_memory.getCamera()
                # First, determine position of Tros
                if camera[0] > 2:
                    trosPos = 1  # One for cannot attack.
                    print("Tros is long-range. Cannot attack.")
                elif camera[0] < -2:
                    trosPos = 1  # One for cannot attack.
                    print("Tros is long-range. Cannot attack.")
                else:
                    trosPos = 0  # One for "Close range, can be attacked.
                    print("Tros is short-range.")
            partyHP = FFX_memory.getBattleHP()
            if partyHP[1] == 0 or partyHP[2] == 0:  # Someone requires reviving.
                print("Tros: Someone fainted.")
                revive()
                Revives += 1
            elif FFX_Screen.turnRikku():
                print("Rikku turn")
                grenadeSlot = FFX_memory.getItemSlot(35)
                grenadeCount = FFX_memory.getItemCountSlot(grenadeSlot)
                print("------------------------------------------------")
                print("Current grenade count: ", grenadeCount)
                print("Grenades used: ", Grenades)
                print("------------------------------------------------")
                totalNades = grenadeCount + Grenades
                if totalNades < 6:
                    if trosPos == 1:
                        defend()
                    else:
                        Steal()
                        Steals += 1
                elif grenadeCount == 0:
                    if trosPos == 1:
                        defend()
                    else:
                        Steal()
                        Steals += 1
                else:
                    print("MARK USE ITEM")
                    grenadeSlot = FFX_memory.getUseItemsSlot(35)
                    useItem(grenadeSlot,'none')
                    Grenades += 1
            elif FFX_Screen.turnTidus():
                print("Tidus turn")
                if trosPos == 1:
                    defend()
                else:
                    attack('none')
                    Attacks += 1
                
    FFX_memory.clickToControl()
    FFX_Logs.writeStats("Tros Attacks:")
    FFX_Logs.writeStats(str(Attacks))
    FFX_Logs.writeStats("Tros Revives:")
    FFX_Logs.writeStats(str(Revives))
    FFX_Logs.writeStats("Tros Grenades:")
    FFX_Logs.writeStats(str(Grenades))
    FFX_Logs.writeStats("Tros Steals:")
    FFX_Logs.writeStats(str(Steals))

def pirhanas():
    battleNum = FFX_memory.getBattleNum()
    #11 = two pirhanas
    #12 = three pirhanas with one being a triple formation (takes two hits)
    #13 = four pirhanas
    if battleNum == 11:
        attack('none')
    else:
        escapeAll()
    FFX_memory.clickToControl()

def besaid():
    print("Fight start: Besaid battle")
    FFXC.set_neutral()
    battleFormat = FFX_memory.getBattleNum()
    print("Besaid battle format number: ", battleFormat)
    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            enemyHP = FFX_memory.getEnemyCurrentHP()
            print("Enemy HP: ", enemyHP)
            if FFX_Screen.turnYuna():
                buddySwap(1)
            elif FFX_Screen.turnLulu():
                thunder('left')
            elif FFX_Screen.turnWakka():
                attack('none')
            elif FFX_Screen.turnTidus():
                if enemyHP[0] == 0:
                    attack('none')
                else:
                    attack('right')

    FFX_memory.clickToControl()


def SinFin():
    FFX_Logs.writeLog("Fight start: Sin's Fin")
    print("Fight start: Sin's Fin")
    FFX_Screen.awaitTurn()
    complete = 0
    while complete == 0:
        print("Determining first turn.")
        if FFX_Screen.turnTidus():
            print("Tidus taking first turn")
            defend()
            time.sleep(0.2)
            print("Tidus defend")

            FFX_Screen.awaitTurn()
            buddySwap(2)  # Yuna out, Lulu in
            thunder("right")
            complete = 1

        elif FFX_Screen.turnYuna():
            print("Yuna taking first turn")
            buddySwap(2)  # Yuna out, Lulu in
            thunder("right")

            FFX_Screen.awaitTurn()
            defend()
            time.sleep(0.2)
            print("Tidus defend")
            complete = 1

    print("First few turns are complete. Now for the rest of the fight.")
    # After the first two turns, the rest of the fight is pretty much scripted.
    turnCounter = 0
    complete = False
    while complete == False:
        if FFX_memory.turnReady():
            turnCounter += 1

            if FFX_Screen.turnKimahri():
                time.sleep(1)
                cam = FFX_memory.getCamera()
                if cam[0] < -2.1:
                    FFX_Screen.awaitTurn()
                    lancet('up')
                else:
                    FFX_Screen.awaitTurn()
                    lancet('right')
            elif FFX_Screen.turnLulu():
                thunder('up')
            elif FFX_Screen.turnTidus():
                if turnCounter < 4:
                    defend()
                    time.sleep(0.2)
                else:
                    buddySwap(2)
                    aeonSummon(0)
            elif FFX_Screen.turnAeon():
                FFX_Xbox.menuLeft()
                time.sleep(0.8)
                FFX_Xbox.menuB()  # Energy Blast
                # while not FFX_Screen.PixelTestTol(1366, 340, (101, 101, 101), 3):
                # print("Attempting to target boss")
                time.sleep(0.1)
                FFX_Xbox.menuRight()
                FFX_Xbox.menuUp()
                # time.sleep(0.05)
                time.sleep(0.15)
                FFX_Xbox.menuB()
                print("Valefor energy blast")
                complete = True
    time.sleep(10)
    print("Sin's Fin fight complete")
    FFX_Xbox.clickToBattle()

def Echuilles():
    FFX_Logs.writeLog("Fight start: Sinspawn Echuilles")
    print("Fight start: Sinspawn Echuilles")
    FFX_Screen.awaitTurn()
    print("Sinspawn Echuilles fight start")

    tidusCounter = 0
    while FFX_memory.battleActive(): #AKA end of battle screen
        if FFX_memory.turnReady():
            if FFX_Screen.faintCheck() > 0:
                revive()
            elif FFX_Screen.turnTidus():
                tidusCounter += 1
                if tidusCounter <= 2:
                    print("Cheer")
                    tidusFlee()  # performs cheer command
                elif FFX_memory.getOverdriveBattle(0) == 100:
                    print("Overdrive")
                    tidusOD()
                else:
                    print("Tidus attack")
                    attack('none')
            elif FFX_Screen.turnWakka():
                if tidusCounter == 1 or tidusCounter == 4:
                    print("Dark Attack")
                    useSkill(0)  #Dark Attack
                elif tidusCounter == 5:
                    print("Heal Tidus for safety")
                    FFX_Xbox.menuDown()
                    FFX_Xbox.menuDown()
                    FFX_Xbox.menuB()
                    time.sleep(0.3)
                    FFX_Xbox.menuB()
                    time.sleep(0.3)
                    FFX_Xbox.menuUp()
                    FFX_Xbox.menuB()
                else:
                    print("Wakka attack")
                    attack('none')
    print("Battle is complete. Now awaiting control.")
    while not FFX_memory.userControl():
        if FFX_memory.cutsceneSkipPossible():
            FFX_Xbox.skipScene()
        elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()

def lancetTutorial():
    FFX_Logs.writeLog("Fight start: Lancet tutorial fight (Kilika)")
    print("Fight start: Lancet tutorial fight (Kilika)")
    FFX_Xbox.clickToBattle()
    lancet('none')

    turn1 = 0
    turn2 = 0
    while FFX_memory.battleActive(): #AKA end of battle screen
        if FFX_memory.turnReady():
            if FFX_Screen.turnTidus():
                attack('none')
            elif FFX_Screen.turnKimahri():
                buddySwap(1)
                defend()
            elif FFX_Screen.turnLulu():
                fire('none')
            else:
                defend()
    FFX_memory.clickToControl()

def KilikaWoods(valeforCharge):
    FFX_Logs.writeLog("Fight start: Kilika general")
    print("Fight start: Kilika battle")
    BattleComplete = 0
    speedSpheres = 0
    currentCharge = False
    skipCharge = False
    turnCounter = 0
    bNum = FFX_memory.getBattleNum()
    print("Charge values:")
    print(FFX_memory.overdriveState())
    FFX_Screen.awaitTurn()
    preEmpt = FFX_Screen.PixelTestTol(1378, 271, (50, 52, 50), 5)

    FFXC.set_neutral()

    # if bNum == 31: #Lizard and Elemental, side
    # elif bNum == 32: #Lizard and Bee, front
    # elif bNum == 33: #Yellow and Bee, front
    # elif bNum == 34: #Lizard, Yellow, and Bee, front
    # elif bNum == 35: #Single Ragora, reverse
    # elif bNum == 36: #Two Ragoras, reverse
    # elif bNum == 37: #Ragora and two bees, reverse

    # These battles we want nothing to do with.
    if bNum == 32 or bNum == 35 or bNum == 36:
        skipCharge = True

    print("Kilika battle")
    while FFX_memory.battleActive(): #AKA end of battle screen
        if valeforCharge == False and skipCharge == False:  # Still to charge Valefor
            if FFX_memory.turnReady():
                print("--------------------------------")
                print("Battle Turn")
                print("Battle Number: ", bNum)
                print("Valefor charge state: ", valeforCharge)
                print("skipCharge state: ", skipCharge)
                turnCounter += 1
                if turnCounter > 7:
                    fleeAll()
                    break
                elif FFX_Screen.faintCheck():
                    revive()
                elif FFX_Screen.turnKimahri():
                    buddySwap(1)
                elif FFX_Screen.turnLulu():
                    buddySwap(2)
                elif bNum == 31:  # Working just fine.
                    print("Logic for battle number 31")
                    currentCharge = True
                    if FFX_Screen.turnTidus():
                        attack('none')
                    elif FFX_Screen.turnYuna():
                        aeonSummon(0)
                        FFX_Screen.awaitTurn()
                        if preEmpt == True:
                            FFX_Xbox.menuRight()
                            FFX_Xbox.SkipDialog(2)
                            FFX_Screen.awaitTurn()
                        aeonBoost()
                        FFX_Screen.awaitTurn()
                        aeonBoost()
                        FFX_Screen.awaitTurn()
                        aeonSpell(2)
                    elif FFX_Screen.turnAeon():
                        aeonSpellDirection(2, 'right')
                        #valeforCharge = True
                    else:
                        defend()
                    #valeforCharge = True
                elif bNum == 33:
                    print("Logic for battle number 33")
                    currentCharge = True
                    if FFX_Screen.turnYuna():
                        time.sleep(0.2)
                        aeonSummon(0)
                        FFX_Screen.awaitTurn()
                        if preEmpt == True:
                            FFX_Xbox.menuRight()
                            FFX_Xbox.SkipDialog(2)
                            FFX_Screen.awaitTurn()
                        aeonBoost()
                        FFX_Screen.awaitTurn()
                        aeonSpellDirection(1, 'left')
                    elif FFX_Screen.turnAeon():
                        aeonSpell(2)
                        #valeforCharge = True
                    else:
                        defend()
                        time.sleep(0.2)
                elif bNum == 34:
                    print("Logic for battle number 34")
                    currentCharge = True
                    if FFX_Screen.turnTidus():
                        attack('none')
                    elif FFX_Screen.turnYuna():
                        aeonSummon(0)
                        FFX_Screen.awaitTurn()
                        if preEmpt == True:
                            FFX_Xbox.menuRight()
                            FFX_Xbox.SkipDialog(2)
                            FFX_Screen.awaitTurn()
                        aeonBoost()
                        FFX_Screen.awaitTurn()
                        aeonSpellDirection(1, 'right')
                    elif FFX_Screen.turnAeon():
                        aeonSpell2(2, 'left')
                        #valeforCharge = True
                    else:
                        defend()
                    #valeforCharge = True
                elif bNum == 37:
                    print("Logic for battle number 37 - two bees and a plant thingey")
                    currentCharge = True
                    if FFX_Screen.turnTidus():
                        attack('none')
                    elif FFX_Screen.turnYuna():
                        aeonSummon(0)
                        FFX_Screen.awaitTurn()
                        if preEmpt == True:
                            FFX_Xbox.menuRight()
                            FFX_Xbox.SkipDialog(2)
                            FFX_Screen.awaitTurn()
                        aeonSpellDirection(1, 'right')
                        FFX_Screen.awaitTurn()
                        aeonSpellDirection(1, 'right')
                    elif FFX_Screen.turnAeon():
                        while not FFX_memory.battleComplete():
                            if FFX_Screen.BattleScreen():
                                aeonSpell(0)
                        #valeforCharge = True
                    else:
                        defend()
                else:
                    skipCharge = True
                    print("Not going to charge Valefor. Battle num: ", bNum)
        else:
            if FFX_memory.turnReady():
                print("--------------------------------")
                print("Battle Turn")
                print("Battle Number: ", bNum)
                print("Valefor charge state: ", valeforCharge)
                print("skipCharge state: ", skipCharge)
                turnCounter += 1
                if turnCounter > 7:
                    fleeAll()
                    break
                elif FFX_Screen.faintCheck():
                    revive()
                elif FFX_Screen.turnKimahri():
                    buddySwap(1)
                elif FFX_Screen.turnLulu() and bNum != 37:
                    buddySwap(2)
                elif bNum == 31:
                    if FFX_Screen.turnTidus():
                        if turnCounter < 4:
                            attack('none')
                        else:
                            tidusFlee()
                    else:
                        defend()
                elif bNum == 32:
                    if FFX_Screen.turnTidus():
                        if turnCounter < 4:
                            attack('none')
                        else:
                            tidusFlee()
                    elif FFX_Screen.turnWakka():
                        attack('right')
                    else:
                        defend()
                elif bNum == 33:
                    if FFX_Screen.turnTidus():
                        if turnCounter < 4:
                            defend()
                        else:
                            tidusFlee()
                    elif FFX_Screen.turnWakka():
                        attack('right')
                    else:
                        defend()
                elif bNum == 34:
                    if FFX_Screen.turnTidus():
                        if turnCounter < 4:
                            attack('none')
                        else:
                            tidusFlee()
                    elif FFX_Screen.turnWakka():
                        attack('right')
                    else:
                        defend()
                elif bNum == 35 or bNum == 36:
                    if FFX_Screen.turnTidus():
                        tidusFlee()
                    else:
                        defend()
                elif bNum == 37:
                    if FFX_Screen.turnTidus():
                        buddySwap(2)
                        thunder('left')
                    elif FFX_Screen.turnLulu():
                        buddySwap(2)
                        tidusFlee()
                    elif FFX_Screen.turnWakka():
                        if FFX_memory.getEnemyCurrentHP()[2] != 0:
                            attack('left')
                        else:
                            defend()
                    else:
                        defend()

    FFX_memory.clickToControl()  # Rewards screen
    hpCheck = FFX_memory.getHP()
    if hpCheck[0] < 250 or hpCheck[1] < 250 or hpCheck[4] < 250:
        healUp2(3)
    else:
        print("No need to heal up. Moving onward.")
    if valeforCharge == False and FFX_memory.overdriveState()[8] == 20:
        valeforCharge = True
    print("Returning Valefor Charge value: ", valeforCharge)
    return valeforCharge

def Geneaux():
    FFX_Logs.writeLog("Fight start: Sinspawn Geneaux")
    print("Fight start: Sinspawn Geneaux")
    FFX_Xbox.clickToBattle()
    if not FFX_Screen.turnTidus():
        while not FFX_Screen.turnTidus():
            if FFX_memory.turnReady():
                defend()
    
    attack('none')
    
    FFX_Xbox.clickToBattle()
    if not FFX_Screen.turnYuna():
        while not FFX_Screen.turnYuna():
            if FFX_memory.turnReady():
                defend()
    
    FFX_Screen.awaitTurn()
    aeonSummon(0) # Summon Valefor
    FFX_Screen.awaitTurn()
    FFX_Xbox.menuLeft()
    time.sleep(0.8)
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()  # Lead off with Valefor overdrive

    valeforOD = 0
    skipCount = 0
    while FFX_memory.battleComplete() == False: #AKA end of battle screen
        pos = FFX_memory.getCoords()
        if FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
        elif FFX_memory.turnReady():
            print("Valefor casting Fire")
            aeonSpell(0)
        elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
        elif FFX_memory.userControl():
            if pos[1] > ((-1.25 * pos[0]) + 543.17):
                FFXC.set_movement(-1, 1)
            else:
                FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()
    print("Battle Complete")
    FFX_memory.clickToControl()

def LucaWorkers():
    FFX_Logs.writeLog("Fight start: Workers in Luca")
    print("Fight start: Workers in Luca")
    BattleComplete = 0
    FFX_Xbox.clickToBattle()

    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            if FFX_Screen.turnKimahri() or FFX_Screen.turnTidus():
                if FFX_Screen.faintCheck() >= 1:
                    revive()
                else:
                    defend()
            if FFX_Screen.turnLulu():
                thunder('none')
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()  # Clicking to get through the battle faster
    FFX_memory.clickToControl()


def LucaWorkers2(earlyHaste):
    FFX_Logs.writeLog("Fight start: Workers in Luca")
    print("Fight start: Workers in Luca")
    BattleComplete = 0
    kimTurn = 0
    tidTurn = 0
    luluTurn = 0
    reviveCount = 0
    FFX_Xbox.clickToBattle()

    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            if earlyHaste == 0 and FFX_Screen.turnKimahri():
                if FFX_Screen.faintCheck() >= 1:
                    revive()
                    reviveCount += 1
                else:
                    kimTurn += 1
                    if kimTurn == 2:
                        enemyHP = FFX_memory.getEnemyCurrentHP()
                        print(enemyHP)
                        if enemyHP[1] > 80:
                            FFX_Xbox.menuLeft()  # Overdrive
                            time.sleep(0.8)
                            FFX_Xbox.menuB()  # Ronso Rage
                            time.sleep(0.4)
                            FFX_Xbox.menuRight()
                            FFX_Xbox.menuB()  # Seed Cannon
                            time.sleep(0.4)
                            FFX_Xbox.menuRight()
                            FFX_Xbox.menuB()  # Target the other guy
                            time.sleep(0.4)
                        elif enemyHP[1] >= 1:
                            attack('right')
                        else:
                            defend()
                    elif kimTurn < 3:
                        attack('right')
                    else:
                        defend()
            elif earlyHaste == 0 and FFX_Screen.turnTidus():
                if FFX_Screen.faintCheck() >= 1:
                    revive()
                else:
                    tidTurn += 1
                    if tidTurn < 3:
                        attack('right')
                    else:
                        defend()
            elif earlyHaste == 1 and tidTurn == 0:
                tidTurn += 1
                tidusHaste('left')
            elif FFX_Screen.turnLulu():
                luluTurn += 1
                if luluTurn == 2 and kimTurn < 2:
                    FFX_Xbox.weapSwap(0)
                else:
                    thunder('none')
            else:
                if FFX_Screen.faintCheck() >= 1:
                    revive()
                else:
                    defend()
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()  # Clicking to get through the battle faster
    FFX_Logs.writeStats('Workers revive count:')
    FFX_Logs.writeStats(reviveCount)
    FFX_memory.clickToControl()


def Oblitzerator(earlyHaste):
    FFX_Logs.writeLog("Fight start: Oblitzerator")
    print("Fight start: Oblitzerator")
    FFX_Xbox.clickToBattle()
    crane = 0

    if earlyHaste == 1:
        #First turn is always Tidus. Haste Lulu if we've got the levels.
        tidusHaste('left')

    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            if crane < 3:
                if FFX_Screen.turnLulu():
                    crane += 1
                    thunder('right')
                else:
                    defend()
            elif crane == 3:
                if FFX_Screen.turnTidus():
                    crane += 1
                    time.sleep(0.2)
                    FFX_Xbox.menuLeft()
                    time.sleep(0.8)
                    FFX_Xbox.menuDown()
                    FFX_Xbox.menuB()
                    FFX_Xbox.menuB()
                    FFX_Xbox.menuB()
                elif FFX_Screen.turnLulu():
                    thunder('none')
                else:
                    defend()
            else:
                if FFX_Screen.turnLulu():
                    thunder('none')
                elif FFX_Screen.turnTidus():
                    attack('none')
                else:
                    defend()
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
        #else:
            #print("Waiting for turn, Oblitzerator fight")
    print("End of fight, Oblitzerator")
    FFX_memory.clickToControl()

def afterBlitz1(earlyHaste):
    FFX_Logs.writeLog("Fight start: After Blitzball (the fisheys)")
    print("Fight start: After Blitzball (the fisheys)")
    print(earlyHaste)
    if earlyHaste != -1:
        FFX_Screen.awaitTurn()

        # Tidus haste self
        tidusHaste('none')
    wakkaTurns = 0

    while FFX_memory.battleComplete() == False:
        if FFX_memory.turnReady():
            print("Enemy HP: ", FFX_memory.getEnemyCurrentHP())
            if FFX_Screen.turnTidus():
                attack('none')
            else:
                wakkaTurns += 1
                hpValues = FFX_memory.getBattleHP()
                cam = FFX_memory.getCamera()
                if wakkaTurns < 3:
                    attack('up')
                elif hpValues[2] < 200:
                    while FFX_memory.battleMenuCursor() != 1:
                        FFX_Xbox.menuDown()
                    FFX_Xbox.menuB()
                    time.sleep(0.4)
                    FFX_Xbox.menuB()
                    time.sleep(0.1)
                    FFX_Xbox.menuUp()
                    FFX_Xbox.menuB()
                    print("Wakka healing Tidus for safety")
                else:
                    defend()

def afterBlitz3(earlyHaste):
    print("Ready to take on Zu")
    print(earlyHaste)
    # Wakka dark attack, or Auron power break
    FFX_Screen.awaitTurn()
    if FFX_Screen.turnAuron():
        print("Auron's turn")
        useSkill(0)
    elif FFX_Screen.turnTidus():
        print("Tidus's turn")
        if earlyHaste != -1:
            tidusHaste('up')
        else:
            attack('none')
    else:
        print("Wakka's turn")
        useSkill(0)
    FFX_Screen.awaitTurn()
    if FFX_Screen.turnAuron():
        useSkill(0)
    elif FFX_Screen.turnTidus():
        if earlyHaste != -1:
            tidusHaste('up')
        else:
            attack('none')
    else:
        useSkill(0)
    FFX_Screen.awaitTurn()
    if FFX_Screen.turnAuron():
        useSkill(0)
    else:
        useSkill(0)

    while not FFX_memory.menuOpen():
        if FFX_memory.turnReady():
            if FFX_Screen.faintCheck() > 0:
                revive()
            else:
                attack('none')
    FFXC.set_value('BtnB', 1)
    time.sleep(4)
    FFXC.set_value('BtnB', 0)
    print("Battle complete (Garuda)")
    #Get to control
    while not FFX_memory.userControl():
        if FFX_memory.cutsceneSkipPossible():
            FFX_Xbox.skipScene()
            FFX_Xbox.awaitSave()
        elif FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
            FFX_Xbox.tapB()

def MiihenRoad(selfDestruct):
    FFX_Logs.writeLog("Fight start: Mi'ihen Road")
    print("Fight start: Mi'ihen Road")
    battle = FFX_memory.getBattleNum()

    hpArray = FFX_memory.getBattleHP()
    hpTotal = hpArray[1] + hpArray[2] + hpArray[3]
    if hpTotal < 1800:
        ambushed = True
    else:
        ambushed = False

    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if ambushed == True:
            print("Looks like we got ambushed. Skipping this battle.")
            fleeAll()
            break
        if FFX_memory.turnReady():
            if FFX_Screen.turnTidus():
                print("Mi'ihen battle. Self-destruct: ", selfDestruct)
                if selfDestruct == 0:
                    if battle == 51 or battle == 64 or battle == 66 or battle == 87:
                        lancetSwap('none')
                        selfDestruct = 1
                        break
                    elif battle == 65 or battle == 84:
                        lancetSwap('right')
                        selfDestruct = 1
                        break
                    else:
                        tidusFlee()
                else:
                    tidusFlee()
            else:
                escapeOne()

    FFX_memory.clickToControl()
    hpCheck = FFX_memory.getHP()
    print("------------------ HP check: ", hpCheck)
    if hpCheck[0] < 520 or hpCheck[2] < 800 or hpCheck[4] < 400:
        healUp(3)
    else:
        print("No need to heal up. Moving onward.")
    
    FFX_memory.fullPartyFormat('miihen')
    print("selfDestruct flag: ", selfDestruct)
    return selfDestruct


def chocoEater():
    FFX_Logs.writeLog("Fight start: Chocobo Eater")
    print("Fight start: Chocobo Eater")
    FFX_Xbox.clickToBattle()
    tidusHaste('right')  # First turn, haste the chocobo eater
    turns = 0
    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            turns += 1
            if FFX_Screen.faintCheck() > 1: #Only if two people are down, very rare but for safety.
                print("Attempting revive")
                revive()
            else:
                print("Attempting defend")
                if FFX_memory.getNextTurn() > 10:
                    time.sleep(0.5) #Avoids a soft-lock, boss starts twerking.
                defend()
        elif FFX_memory.diagSkipPossible():
            print("Skipping dialog")
            FFX_Xbox.menuB()
    FFX_Logs.writeStats("Chocobo eater turns:")
    FFX_Logs.writeStats(str(turns))
    print("Chocobo Eater battle complete.")

def aeonBoost():
    print("Aeon Boost function")
    FFX_Screen.awaitTurn()
    FFX_Xbox.menuRight()
    time.sleep(0.6)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()

def MRRbattle(status):
    #Yuna complete, Kimahri complete, Valefor overdrive, Battle counter, Yuna level up complete, Yuna grid, phase
    print("---------------------------------------------------------")
    print("---------------------------------------------------------")
    print("Fight start: MRR")
    time.sleep (0.5)
    battle = FFX_memory.getBattleNum()
    print("Battle number: ", battle)
    
    if battle == 102:
        print("Garuda battle, we want nothing to do with this.")
    elif status[5] == 0:
        print("If funguar present or more than three flees already, Valefor overdrive.")
    elif status[5] == 1:
        print("Now we're going to try to charge Valefor's overdrive again.")
    elif status[5] == 2:
        print("Yuna still needs levels.")
    else:
        print("Nothing else, going to flee.")
    FFX_Screen.awaitTurn()
    
    petrifiedstate = False
    petrifiedstate = checkPetrify()
    
    #If we're ambushed and take too much damage, this will trigger first.
    hpArray = FFX_memory.getBattleHP()
    hpTotal = hpArray[1] + hpArray[2] + hpArray[3]
    if hpTotal < 1800 and status[5] != 2: #Final charging for Yuna is a lower overall party HP
        print("------------We got ambushed. Not going to attempt to recover.")
        fleeAll()
    elif FFX_Screen.faintCheck() >= 1:
        print("------------Someone is dead from the start of battle. Just get out.")
        fleeAll()
    elif petrifiedstate == True:
        print("------------Someone has been petrified which messes up the battle logic. Escaping.")
        fleeAll()
    elif battle == 102: #Garuda, flee no matter what.
        fleeAll()
    elif status[5] == 0: #Phase zero - use Valefor overdrive to overkill for levels
        if status[3] < 3: #Battle number (zero-index)
            if battle == 100 or battle == 101: #The two battles with Funguar
                while not FFX_memory.menuOpen(): #end of battle screen
                    if FFX_Screen.BattleScreen():
                        if FFX_Screen.turnTidus():
                            buddySwapKimahri()
                        elif FFX_Screen.turnKimahri() or FFX_Screen.turnWakka():
                            defend()
                        else:
                            buddySwap(0)
                            aeonSummon(0)
                            FFX_Screen.awaitTurn()
                            while not FFX_Screen.PixelTestTol(219, 684, (221, 221, 221), 5):
                                FFX_Xbox.menuLeft()
                            time.sleep(0.4)
                            FFX_Xbox.menuDown()
                            FFX_Xbox.menuB()
                            FFX_Xbox.menuB()
                            FFX_Xbox.menuB()
                            status[2] = 1
                            status[5] = 1
            else:
                fleeAll()
        else: #Starting with fourth battle, overdrive on any battle that isn't Garuda.
            while not FFX_memory.menuOpen(): #end of battle screen
                if FFX_Screen.BattleScreen():
                    if FFX_Screen.turnTidus():
                        buddySwapKimahri()
                    if FFX_Screen.turnKimahri() or FFX_Screen.turnWakka():
                        defend()
                    else:
                        buddySwap(0)
                        aeonSummon(0)
                        FFX_Screen.awaitTurn()
                        while not FFX_Screen.PixelTestTol(219, 684, (221, 221, 221), 5):
                            FFX_Xbox.menuLeft()
                        time.sleep(0.4)
                        FFX_Xbox.menuDown()
                        FFX_Xbox.menuB()
                        FFX_Xbox.menuB()
                        FFX_Xbox.menuB()
                        status[2] = 1
                        status[5] = 1
    elif status[5] == 1: #Next need to recharge Valefor
        valeforChargeComplete = True
        if battle == 96: #Gandarewa, Red Element, Raptor (camera front)
            #Working, confirmed good
            wakkaTurns = 0
            while not FFX_memory.menuOpen(): #end of battle screen
                if FFX_Screen.BattleScreen():
                    if checkPetrify():
                        print("Someone is pretrified. Escaping battle.")
                        fleeAll()
                        valeforChargeComplete = False
                    else:
                        print("No petrify issues.")
                    if FFX_Screen.turnTidus():
                        buddySwapKimahri()
                        attack('right')
                    elif FFX_Screen.turnWakka():
                        wakkaTurns += 1
                        if wakkaTurns == 1:
                            attack('left')
                        else:
                            buddySwap(0)
                            aeonSummon(0)
                            FFX_Screen.awaitTurn()
                            aeonBoost()
                            FFX_Screen.awaitTurn()
                            enemyHP = FFX_memory.getEnemyCurrentHP()
                            if enemyHP[1] == 0 and enemyHP[2] == 0:
                                FFX_Xbox.SkipDialog(1)
                    elif FFX_Screen.turnAuron():
                        attack('right')
                    elif FFX_Screen.turnKimahri():
                        buddySwap(0)
                        aeonSummon(0)
                        FFX_Screen.awaitTurn()
                        aeonBoost()
                        FFX_Screen.awaitTurn()
                        if FFX_memory.getEnemyCurrentHP()[1] == 0:
                            FFX_Xbox.SkipDialog(2)
                    elif FFX_Screen.turnAeon():
                        aeonSpell2(3, 'right')
        elif battle == 97: #Lamashtu, Gandarewa, Red Element (camera front)
            while not FFX_memory.menuOpen(): #end of battle screen
                if FFX_Screen.BattleScreen():
                    if FFX_Screen.turnTidus():
                        buddySwapKimahri()
                        attack('none')
                    elif FFX_Screen.turnWakka():
                        defend()
                    elif FFX_Screen.turnAuron():
                        attack('none')
                    elif FFX_Screen.turnKimahri():
                        buddySwap(0)
                        aeonSummon(0)
                        FFX_Screen.awaitTurn()
                        aeonSpell(2)
                        FFX_Screen.awaitTurn()
                        aeonBoost()
                    elif FFX_Screen.turnAeon():
                        aeonSpell(3)
        elif battle == 98: #Raptor, Red Element, Gandarewa (camera side)
            #Working, confirmed good
            while not FFX_memory.menuOpen(): #end of battle screen
                if FFX_Screen.BattleScreen():
                    if checkPetrify():
                        print("Someone is pretrified. Escaping battle.")
                        fleeAll()
                        valeforChargeComplete = False
                    else:
                        print("No petrify issues.")
                    if FFX_Screen.turnTidus():
                        buddySwapKimahri()
                    elif FFX_Screen.turnKimahri():
                        lancet('down')
                    elif FFX_Screen.turnWakka():
                        attack('none')
                    elif FFX_Screen.turnAuron():
                        buddySwap(0)
                        aeonSummon(0)
                        FFX_Screen.awaitTurn()
                        aeonSpell2(2, 'right')
                        aeonBoost()
                    elif FFX_Screen.turnAeon():
                        aeonSpell2(3, 'right')
        #battle 99 is never used.
        elif battle == 100: #Raptor, Funguar, Red Element (camera front)
            #Working, confirmed good
            while not FFX_memory.menuOpen(): #end of battle screen
                if FFX_Screen.BattleScreen():
                    if checkPetrify():
                        print("Someone is pretrified. Escaping battle.")
                        fleeAll()
                        valeforChargeComplete = False
                    else:
                        print("No petrify issues.")
                    if FFX_Screen.turnTidus():
                        buddySwapKimahri()
                        defend()
                    elif FFX_Screen.turnWakka():
                        attack('none')
                    elif FFX_memory.getEnemyCurrentHP()[0] != 0:
                        buddySwapTidus()
                        fleeAll()
                        valeforChargeComplete = False
                    elif FFX_Screen.turnAuron():
                        buddySwap(0)
                        aeonSummon(0)
                        FFX_Screen.awaitTurn()
                        aeonSpell(0)
                        FFX_Screen.awaitTurn()
                        aeonBoost()
                    elif FFX_Screen.turnAeon():
                        aeonSpell(3)
        elif battle == 101: #Funguar, Red Element, Gandarewa (camera reverse angle)
            #Working, confirmed good
            while not FFX_memory.menuOpen(): #end of battle screen
                if FFX_Screen.BattleScreen():
                    if FFX_Screen.turnTidus():
                        buddySwapKimahri()
                        lancet('left')
                    elif FFX_Screen.turnWakka():
                        attack('left')
                    elif FFX_memory.getEnemyCurrentHP()[2] != 0:
                        buddySwapTidus()
                        fleeAll()
                        valeforChargeComplete = False
                    elif FFX_Screen.turnAuron():
                        buddySwap(0)
                        aeonSummon(0)
                        FFX_Screen.awaitTurn()
                        aeonSpell(0)
                        FFX_Screen.awaitTurn()
                        aeonBoost()
                    elif FFX_Screen.turnAeon():
                        aeonSpell(3)
        if valeforChargeComplete == True:
            status[5] = 2 #Phase 2, final phase to level up Kimahri and Yuna
            status[2] = 2 #Valefor is charged flag.
    elif status[5] == 2: #Last phase is to level Yuna and Kimahri
        if status[0] == 1 and status[1] == 1: #Both Yuna and Kimahri have levels, good to go.
            status[5] = 3
            while FFX_memory.menuOpen() != True:
                if FFX_Screen.BattleScreen():
                    if FFX_Screen.turnTidus():
                        tidusFlee()
                    else:
                        buddySwapTidus()
        else:
            #Wakka attack Raptors and Gandarewas for Yuna AP.
            yunaTurnCount = 0
            while FFX_memory.menuOpen() != True:
                if FFX_Screen.BattleScreen():
                    if FFX_Screen.turnTidus():
                        tidusFlee()
                    elif FFX_Screen.faintCheck() >= 1:
                        buddySwapTidus()
                    elif FFX_Screen.turnKimahri():
                        defend()
                    elif FFX_Screen.turnYuna():
                        yunaTurnCount += 1
                        if yunaTurnCount == 1:
                            defend()
                        else:
                            buddySwapTidus()
                    elif FFX_Screen.turnWakka():
                        if battle == 96 or battle == 97 or battle == 101:
                            attack('left')
                        elif battle == 98 or battle == 100:
                            attack('none')
                        else:
                            buddySwapTidus()
                        time.sleep(0.2)
                    else: #Should not occur, but you never know.
                        buddySwapTidus()
                    time.sleep(0.5)
    else: #Everything is done.
        fleeAll()
    
    #OK the battle should be complete now. Let's do some wrap-up stuff.
    wrapUp()
    
    #Check on sphere levels for our two heroes
    if status[0] == 0:
        if FFX_memory.getSLVLYuna() > 573:
            status[0] = 1
    if status[1] == 0:
        if FFX_memory.getSLVLKim() >= 495:
            status[1] = 1
    if status[5] == 2: #Last phase is to level Yuna and Kimahri
        if status[0] == 1 and status[1] == 1: #Both Yuna and Kimahri have levels, good to go.
            status[5] = 3
    
    if status[5] == 3:
        FFX_memory.fullPartyFormat('mrr1')
    elif status[5] == 2: #Still levelling Yuna or Kimahri
        FFX_memory.fullPartyFormat('mrr2')
        print("Yuna in front party, trying to get some more experience.")
    else:
        FFX_memory.fullPartyFormat('mrr1')
    FFX_memory.closeMenu()
    
    #Now checking health values
    hpCheck = FFX_memory.getHP()
    print("HP values: ", hpCheck)
    if status[5] == 2:
        healUp(3)
    elif hpCheck[1] != 475:  # Yuna is low. Heal all.
        healUp(6)
    elif hpCheck[3] != 644:  # Kimahri missing HP
        healUp(5)
    elif hpCheck[5] != 380:  # Lulu low
        healUp(4)
    elif hpCheck[2] != 1030:  # Auron missing HP
        healUp(3)
    elif hpCheck[4] != 818:  # Wakka missing HP
        healUp(2)
    elif hpCheck[0] != 520:  # Tidus
        healUp(1)
    FFX_memory.closeMenu()
    #donezo. Back to the main path.
    print("Clean-up is now complete.")
    return status

def battleGui():
    FFX_Logs.writeLog("Fight start: Sinspawn Gui")
    print("Fight start: Sinspawn Gui")
    FFX_Xbox.clickToBattle()
    print("Engaging Gui")
    turns = 0
    phase = 1
    valeforFaint = False
    lastHP = 0
    while turns < 3:
        if FFX_memory.turnReady():
            turns += 1
            if FFX_Screen.turnTidus():
                defend()  # Tidus defends first turn
            if FFX_Screen.turnWakka():
                FFX_Xbox.weapSwap(0)
            if FFX_Screen.turnYuna():
                buddySwap(2)  # Auron in
                useSkill(0)  # Performs power break
            time.sleep(0.5)  # Avoids doubling up on any pattern
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
    if turns == 3:
        FFX_Xbox.clickToBattle()
        turns += 1
        buddySwap(0)  # Switch Wakka for Kimahri
        time.sleep(0.5)
        FFX_Xbox.menuLeft()
        time.sleep(0.8)
        FFX_Xbox.menuB()
        time.sleep(0.4)
        FFX_Xbox.menuDown()
        FFX_Xbox.menuB()
        time.sleep(0.2)
        FFX_Xbox.menuB()
        FFX_Xbox.menuB()
        FFX_Xbox.menuB()
        FFX_Xbox.menuB()  # Kimahri overdrive
        phase = 2
        time.sleep(1)
    if turns == 4:
        FFX_Xbox.clickToBattle()
        buddySwap(2)  # Tidus swap out for Yuna
        aeonSummon(0)  # summon Valefor
        FFX_Screen.awaitTurn()

        FFX_Xbox.menuLeft()
        time.sleep(0.8)
        FFX_Xbox.menuB()
        time.sleep(0.4)
        FFX_Xbox.menuB()
        time.sleep(0.2)
        FFX_Xbox.menuB()
        FFX_Xbox.menuB()
        FFX_Xbox.menuB()
        FFX_Xbox.menuB()  # Valefor overdrive on the body
        time.sleep(1)
        turns += 1
        lastHP = FFX_memory.getBattleHP()[1]
    
    FFX_Screen.awaitTurn()
    nextHP = FFX_memory.getBattleHP()[1]
    lastHP = nextHP
    nextTurn = 20
    lastTurn = 20
    while FFX_memory.battleActive():
        if FFX_memory.turnReady() and FFX_memory.getBattleCharTurn() == 8:
            nextHP = FFX_memory.getBattleHP()[1]
            lastTurn = nextTurn
            nextTurn = FFX_memory.getNextTurn()
            if FFX_Screen.checkCharge(1):
                print("------Overdriving")
                time.sleep(0.4)
                FFX_Xbox.menuLeft()
                time.sleep(0.8)
                FFX_Xbox.menuB()
                time.sleep(0.4)
                FFX_Xbox.menuB()
                time.sleep(0.2)
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()  # Valefor overdrive on the body
                time.sleep(1)
            elif lastTurn == 8: #Valefor takes two turns in a row
                print("------Two turns in a row")
                time.sleep(0.4)
                FFX_Xbox.menuRight() #Shield command
                FFX_Xbox.SkipDialog(1.2)
                time.sleep(1)
            elif nextHP > lastHP - 40 and not nextHP == lastHP: #Gravity spell was used
                print("------Gravity was used")
                time.sleep(0.4)
                FFX_Xbox.menuRight() #Shield command
                FFX_Xbox.SkipDialog(1.2)
                time.sleep(1)
            else:
                print("------Attack was just used. Now boost.")
                time.sleep(0.4)
                FFX_Xbox.menuRight() #Boost command
                time.sleep(0.8)
                FFX_Xbox.menuDown()
                FFX_Xbox.SkipDialog(1)
                time.sleep(1)
            lastHP = nextHP
        elif FFX_memory.turnReady() and FFX_memory.getBattleCharTurn() == 1:
            print("Yuna turn, something went wrong.")
            time.sleep(10)
        elif FFX_memory.turnReady() and FFX_memory.getBattleCharTurn() == 2:
            print("Auron turn, something went wrong.")
            time.sleep(10)
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
    time.sleep(1)
    
    #In between battles
    FFX_memory.clickToStoryProgress(865)
    print("Ready to skip cutscene")
    
    while not FFX_memory.battleActive():
        if FFX_memory.cutsceneSkipPossible():
            FFX_Xbox.skipScene()
            print("Skipping scene")
        if FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
            FFX_Xbox.tapB()
    
    #Second Gui battle
    FFX_Xbox.clickToBattle()
    turn = 1
    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            if FFX_Screen.turnSeymour():
                while FFX_memory.battleMenuCursor() != 21:
                    if FFX_memory.battleMenuCursor() == 22 or FFX_memory.battleMenuCursor() == 1:
                        FFX_Xbox.menuUp()
                    else:
                        FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                while FFX_memory.battleCursor2() < 4:
                    FFX_Xbox.menuDown()
                time.sleep(0.035)
                FFX_Xbox.menuB()
                if turn == 1:
                    time.sleep(0.035)
                    FFX_Xbox.menuLeft()
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()
                turn += 1
            else:
                defend()
    
    while not FFX_memory.userControl():
        if FFX_memory.cutsceneSkipPossible():
            print("Intentional delay to get the cutscene skip to work.")
            time.sleep(0.07)
            FFX_Xbox.skipSceneSpec()
            time.sleep(2)
        elif FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
            FFX_Xbox.tapB()

def oldLogic():
    if turns == 5:
        while not FFX_Screen.turnSeymour():
            FFX_Xbox.clickToBattle()
            if FFX_Screen.turnAeon() and FFX_Screen.checkCharge(1):
                # Ifrit with overdrive charged
                FFX_Xbox.menuLeft()
                time.sleep(0.8)
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()  # Overdrive
                FFX_memory.clickToStoryProgress(865)
                
                while not FFX_memory.cutsceneSkipPossible():
                    time.sleep(0.035)
                FFX_Xbox.skipScene()
            elif FFX_Screen.turnAeon() and not FFX_Screen.PixelTest(1472, 728, (255, 83, 0)):
                aeonSpell(0)
            elif FFX_Screen.turnAuron():
                buddySwap(1)  # Bring in Lulu
                fire('none')
            elif FFX_Screen.turnYuna():
                valeforFaint = True
                aeonSummon(1)
        phase = 3

    turn = 0
    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            turn += 1
            if FFX_Screen.turnSeymour():
                while FFX_memory.battleMenuCursor() != 21:
                    if FFX_memory.battleMenuCursor() == 22 or FFX_memory.battleMenuCursor() == 1:
                        FFX_Xbox.menuUp()
                    else:
                        FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                while FFX_memory.battleCursor2() < 4:
                    FFX_Xbox.menuDown()
                time.sleep(0.035)
                FFX_Xbox.menuB()
                if turn == 1:
                    time.sleep(0.035)
                    FFX_Xbox.menuLeft()
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()
            else:
                defend()
    FFXC.set_value('BtnB', 1)
    time.sleep(2)
    FFXC.set_value('BtnB', 0)
    return valeforFaint


def djose(stoneBreath):
    FFX_Logs.writeLog("Fight start: Djose road")
    print("Fight start: Djose road")
    complete = 0
    while not FFX_memory.menuOpen(): #AKA end of battle screen
        battleNum = FFX_memory.getBattleNum()
        if FFX_memory.turnReady():
            if stoneBreath == 1:  # Stone Breath already learned
                print("Djose: Stone breath already learned.")
                fleeAll()
            else:  # Stone breath not yet learned
                if battleNum == 128 or battleNum == 134 or battleNum == 136:
                    print("Djose: Learning Stone Breath.")
                    lancetSwapDjose('none')
                    stoneBreath = 1
                    break
                elif battleNum == 127:
                    print("Djose: Learning Stone Breath")
                    # One basilisk with two wasps
                    lancetSwapDjose('up')
                    stoneBreath = 1
                    break
                else:
                    print("Djose: Cannot learn Stone Breath here.")
                    fleeAll()

    print("Mark 2")
    FFX_memory.clickToControl()
    print("Mark 3")
    partyHP = FFX_memory.getHP()
    print(partyHP)
    if partyHP[0] < 300 or partyHP[4] < 300:
        print("Djose: recovering HP")
        healUp(3)
    else:
        print("Djose: No need to heal.")
    return stoneBreath


def fleePathing():
    FFX_Logs.writeLog("Fight start: Flee Pathing? When did I program this?")
    complete = 0
    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            if FFX_Screen.turnTidus():
                tidusFlee()
            else:
                escapeOne()


def extractor():
    FFX_Logs.writeLog("Fight start: Extractor")
    FFXC.set_neutral()
    FFX_Xbox.clickToBattle()
    tidusHaste('none')
    time.sleep(0.2)

    FFX_Screen.awaitTurn()
    attack('none')
    time.sleep(0.2)

    FFX_Screen.awaitTurn()
    tidusHaste('left')
    time.sleep(0.2)

    tidusCheer = 0
    complete = 0
    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.specialTextOpen():
            FFX_Xbox.menuB()
        elif FFX_memory.turnReady():
            if FFX_Screen.faintCheck() > 0:
                revive()
            elif FFX_Screen.turnTidus() and tidusCheer < 2:
                tidusCheer += 1
                cheer()
            else:
                attack('none')
        elif FFX_Screen.BattleComplete():
            complete = 1
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
    FFX_memory.clickToControl()


def mixTutorial():
    FFX_Logs.writeLog("Fight start: Mix Tutorial")
    FFX_Xbox.clickToBattle()
    Steal()
    time.sleep(1)
    FFX_Xbox.clickToBattle()
    FFX_Xbox.menuLeft()
    time.sleep(0.8)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()  # Throw some ability spheres at it.
    FFX_memory.clickToControl()


def chargeRikku():
    FFX_Logs.writeLog("Fight start: Charging Rikku (before Guadosalam)")
    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            if FFX_Screen.turnRikku():
                attack('none')
            else:
                escapeOne()
    FFX_memory.clickToControl()
    healUp(3)

def thunderPlains(status, section):
    bNum = FFX_memory.getBattleNum()
    nadeSlot = FFX_memory.getUseItemsSlot(35)
    print("Grenade Slot %d" % nadeSlot)

    startingstatus = []
    for i in range(len(status)):
        startingstatus.append(status[i])

    tidusturns = 0
    wakkaturns = 0
    auronturns = 0
    speedcount = FFX_memory.getSpeed()
    rikkucharge = FFX_memory.getOverdriveValue(6)
    
    petrifiedstate = False
    petrifiedstate = checkPetrify()

    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            print("Turn start - Thunder Plains")
            turnchar = FFX_memory.getBattleCharTurn()
            if petrifiedstate == True:
                print("------------Someone has been petrified which messes up the battle logic. Escaping.")
                fleeAll()
            elif bNum == 152 or bNum == 155 or bNum == 162:  # Any battle with Larvae
                fleeAll() #No longer need Lunar Curtain for Evrae fight.
                #print("Battle with Larvae. Battle number: ", bNum)
                #if startingstatus[2] == False:
                #    if turnchar == 0:
                #        if tidusturns == 0:
                #            rikkuposition = FFX_memory.getBattleCharSlot(6)
                #            buddySwap_new(rikkuposition)
                #        else:
                #            tidusFlee()
                #        tidusturns += 1
                #    elif turnchar == 6:
                #        Steal()
                #        status[2] = True
                #    else:
                #        tidusposition = FFX_memory.getBattleCharSlot(0)
                #        buddySwap_new(tidusposition)
                #elif turnchar == 0:
                #    tidusFlee()
                #else:
                #    fleeAll()
            elif bNum == 160:
                print("Battle with Iron Giant. Battle number: ", bNum)
                if startingstatus[1] == False:
                    if turnchar == 0:
                        if tidusturns == 0:
                            defend()
                        else:
                            tidusFlee()
                        tidusturns += 1
                    elif turnchar == 4:
                        rikkuposition = FFX_memory.getBattleCharSlot(6)
                        buddySwap_new(rikkuposition)
                    elif turnchar == 6:
                        Steal()
                        print("OMG something's happening!")
                        status[1] = True
                    else:
                        defend()
                elif turnchar == 0:
                    tidusFlee()
                else:
                    fleeAll()
            elif bNum == 161:
                print("Battle with Iron Giant. Battle number: ", bNum)
                if startingstatus[1] == False and FFX_memory.getStoryProgress == 1375:
                    if turnchar == 0:
                        if tidusturns == 0:
                            rikkuposition = FFX_memory.getBattleCharSlot(6)
                            buddySwap_new(rikkuposition)
                        else:
                            tidusFlee()
                        tidusturns += 1
                    elif turnchar == 4:
                        if wakkaturns == 0:
                            wakkaposition = FFX_memory.getBattleCharSlot(4)
                            rikkuposition = FFX_memory.getBattleCharSlot(6)
                            wakkaHP = FFX_memory.getBattleHP()[wakkaposition]
                            rikkuHP = FFX_memory.getBattleHP()[rikkuposition]
                            if wakkaHP > rikkuHP > 0 and FFX_memory.getOverdriveValue(6) < 100:
                                defend()
                            else:
                                tidusposition = FFX_memory.getBattleCharSlot(0)
                                buddySwap_new(tidusposition)
                        else:
                            tidusposition = FFX_memory.getBattleCharSlot(0)
                            buddySwap_new(tidusposition)
                        wakkaturns += 1
                    elif turnchar == 6:
                        Steal()
                        print("OMG something's happening!")
                        status[1] = True
                    elif turnchar == 2:
                        rikkuposition = FFX_memory.getBattleCharSlot(6)
                        rikkuHP = FFX_memory.getBattleHP()[rikkuposition]
                        if rikkuHP > 0:
                            defend()
                        else:
                            tidusposition = FFX_memory.getBattleCharSlot(0)
                            buddySwap_new(tidusposition)
                        auronturns += 1
                    else:
                        fleeAll()
                elif startingstatus[3] == False and speedcount < 14 and section == 2:
                    if turnchar == 0:
                        if tidusturns == 0:
                            rikkuposition = FFX_memory.getBattleCharSlot(6)
                            buddySwap_new(rikkuposition)
                        else:
                            tidusFlee()
                        tidusturns += 1
                    elif turnchar == 4:
                        if wakkaturns == 0:
                            wakkaposition = FFX_memory.getBattleCharSlot(4)
                            rikkuposition = FFX_memory.getBattleCharSlot(6)
                            wakkaHP = FFX_memory.getBattleHP()[wakkaposition]
                            rikkuHP = FFX_memory.getBattleHP()[rikkuposition]
                            if wakkaHP > rikkuHP > 0 and FFX_memory.getOverdriveValue(6) < 100:
                                defend()
                            else:
                                tidusposition = FFX_memory.getBattleCharSlot(0)
                                buddySwap_new(tidusposition)
                        else:
                            tidusposition = FFX_memory.getBattleCharSlot(0)
                            buddySwap_new(tidusposition)
                        wakkaturns += 1
                    elif turnchar == 6:
                        grenadeslot = FFX_memory.getUseItemsSlot(35)
                        print("Grenade Slot %d" % grenadeslot)
                        useItem(grenadeslot,'none')
                        status[3] = True
                        fleeAll()
                    elif turnchar == 2:
                        rikkuposition = FFX_memory.getBattleCharSlot(6)
                        rikkuHP = FFX_memory.getBattleHP()[rikkuposition]
                        if rikkuHP > 0:
                            defend()
                        else:
                            tidusposition = FFX_memory.getBattleCharSlot(0)
                            buddySwap_new(tidusposition)
                        auronturns += 1
                    else:
                        fleeAll()
                elif startingstatus[1] == False:
                    if turnchar == 0:
                        if tidusturns == 0:
                            rikkuposition = FFX_memory.getBattleCharSlot(6)
                            buddySwap_new(rikkuposition)
                        else:
                            tidusFlee()
                        tidusturns += 1
                    elif turnchar == 4:
                        if wakkaturns == 0:
                            wakkaposition = FFX_memory.getBattleCharSlot(4)
                            rikkuposition = FFX_memory.getBattleCharSlot(6)
                            wakkaHP = FFX_memory.getBattleHP()[wakkaposition]
                            rikkuHP = FFX_memory.getBattleHP()[rikkuposition]
                            if wakkaHP > rikkuHP > 0 and FFX_memory.getOverdriveValue(6) < 100:
                                defend()
                            else:
                                tidusposition = FFX_memory.getBattleCharSlot(0)
                                buddySwap_new(tidusposition)
                        else:
                            tidusposition = FFX_memory.getBattleCharSlot(0)
                            buddySwap_new(tidusposition)
                        wakkaturns += 1
                    elif turnchar == 6:
                        Steal()
                        status[1] = True
                    elif turnchar == 2:
                        rikkuposition = FFX_memory.getBattleCharSlot(6)
                        rikkuHP = FFX_memory.getBattleHP()[rikkuposition]
                        if rikkuHP > 0:
                            defend()
                        else:
                            tidusposition = FFX_memory.getBattleCharSlot(0)
                            buddySwap_new(tidusposition)
                        auronturns += 1
                    else:
                        fleeAll()
                elif turnchar == 0:
                    tidusFlee()
                else:
                    tidusposition = FFX_memory.getBattleCharSlot(0)
                    if tidusposition > 3:
                        buddySwap_new(tidusposition)
                    else:
                        fleeAll()
            elif bNum == 154 or bNum == 156 or bNum == 164:
                print("Battle with random mobs. Battle number: ", bNum)
                if startingstatus[3] == False and speedcount < 10 and section == 2 and FFX_memory.getStoryProgress == 1375:
                    if turnchar == 0:
                        if tidusturns == 0:
                            rikkuposition = FFX_memory.getBattleCharSlot(6)
                            buddySwap_new(rikkuposition)
                        else:
                            tidusFlee()
                        tidusturns += 1
                    elif turnchar == 4:
                        tidusposition = FFX_memory.getBattleCharSlot(0)
                        buddySwap_new(tidusposition)
                    elif turnchar == 6:
                        useItem(nadeSlot, 'none')
                        status[3] = True
                    else:
                        defend()
                elif tidusturns == 0:
                    tidusFlee()
                else:
                    fleeAll()
            else:  # Nothing useful this battle. Moving on.
                fleeAll()
    print("Battle is ended - Thunder Plains")
    FFX_memory.clickToControl()
    # FFX_Xbox.menuB() #In case lightning is incoming. Happens far too often.
    if FFX_memory.getOverdriveValue(6) == 100:
        status[0] = True
    print("Status array, Rikku charge, Light curtain, and Lunar Curtain:")
    print(status)
    print("Checking party format and resolving if needed.")
    FFX_memory.fullPartyFormat_New('postbunyip',11)
    while FFX_memory.menuOpen():
        FFX_Xbox.menuA()
    print("Party format is good. Now checking health values.")
    hpValues = FFX_memory.getHP()
    if hpValues[0] < 400 or hpValues[2] < 400 or hpValues[4] < 400 or hpValues[6] < 180:
        healUp_New(4, 11)
    print("Ready to continue onward.")
    print("Plains variables: Rikku charged, stolen lunar curtain, stolen light curtain")
    print(status)
    return status

def mWoods(woodsVars):
    FFX_Logs.writeLog("Fight start: Macalania Woods")
    print("Logic depends on completion of specific goals. In Order:")
    print("Rikku charged, stolen Fish Scale, stolen Arctic Wind")
    print(woodsVars)
    tidusIn = True
    battleNum = FFX_memory.getBattleNum()
    print("------------- Battle Start - Battle Number: ", battleNum)
    tidusturns = 0
    wakkasafe = True
    FFX_Screen.awaitTurn()
    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            turnchar = FFX_memory.getBattleCharTurn()
            if checkPetrifyTidus() == True:
                fleeAll()
                break
            if woodsVars[0] == False:  # Rikku needs charging.
                print("Marker 1")
                if turnchar == 6:
                    if battleNum == 175 and woodsVars[2] == False:
                        print("Marker 2")
                        Steal()
                    elif battleNum == 172 and woodsVars[1] == False:
                        print("Marker 3")
                        StealDown()
                    elif battleNum == 171 and woodsVars[1] == False:
                        print("Marker 4")
                        StealRight()
                    else:
                        print("Marker 5")
                        attack('none')
                else:
                    print("Marker 6")
                    escapeOne()
            elif woodsVars[1] == False or woodsVars[2] == False:
                if battleNum == 175 and woodsVars[2] == False:
                    print("Marker 7")
                    if turnchar == 0:
                        #wakkasafe = FFX_memory.petrifiedstate(4) == False and FFX_memory.getBattleHP()[FFX_memory.getBattleCharSlot(4)] > 200
                        wakkaSafe = True
                        if tidusturns == 0 and wakkasafe == True:
                            rikkuposition = FFX_memory.getBattleCharSlot(6)
                            buddySwap_new(rikkuposition)
                        else:
                            tidusFlee()
                        tidusturns += 1
                    elif turnchar == 2:
                        tidusposition = FFX_memory.getBattleCharSlot(0)
                        if tidusposition > 2:
                            buddySwapTidus()
                        else:
                            escapeOne()
                    elif turnchar == 4:
                        tidusposition = FFX_memory.getBattleCharSlot(0)
                        buddySwap_new(tidusposition)
                    elif turnchar == 6:
                        Steal()
                    else:
                        print("Marker 8")
                        tidusposition = FFX_memory.getBattleCharSlot(0)
                        if tidusposition > 3:
                            buddySwap_new(tidusposition)
                        else:
                            escapeOne()
                elif battleNum == 172 and woodsVars[1] == False:
                    print("Marker 9")
                    if turnchar == 0:
                        #wakkasafe = FFX_memory.petrifiedstate(4) == False and FFX_memory.getBattleHP()[
                        #    FFX_memory.getBattleCharSlot(4)] > 200
                        wakkasafe = True #Something wrong with the original logic.
                        if tidusturns == 0 and wakkasafe == True:
                            rikkuposition = FFX_memory.getBattleCharSlot(6)
                            buddySwap_new(rikkuposition)
                        else:
                            tidusFlee()
                        tidusturns += 1
                    elif turnchar == 2:
                        tidusposition = FFX_memory.getBattleCharSlot(0)
                        if tidusposition > 2:
                            buddySwapTidus()
                        else:
                            escapeOne()
                    elif turnchar == 4:
                        tidusposition = FFX_memory.getBattleCharSlot(0)
                        buddySwap_new(tidusposition)
                    elif turnchar == 6:
                        StealDown()
                    else:
                        print("Marker 10")
                        tidusposition = FFX_memory.getBattleCharSlot(0)
                        if tidusposition > 3:
                            buddySwap_new(tidusposition)
                        else:
                            escapeOne()
                elif battleNum == 171 and woodsVars[1] == False:
                    print("Marker 11")
                    if turnchar == 0:
                        #wakkasafe = FFX_memory.petrifiedstate(4) == False and FFX_memory.getBattleHP()[
                        #    FFX_memory.getBattleCharSlot(4)] > 200
                        wakkasafe = True #Something wrong with the original logic.
                        if tidusturns == 0 and wakkasafe == True:
                            rikkuposition = FFX_memory.getBattleCharSlot(6)
                            buddySwap_new(rikkuposition)
                        else:
                            tidusFlee()
                        tidusturns += 1
                    elif turnchar == 2:
                        tidusposition = FFX_memory.getBattleCharSlot(0)
                        if tidusposition > 2:
                            buddySwapTidus()
                        else:
                            escapeOne()
                    elif turnchar == 4:
                        tidusposition = FFX_memory.getBattleCharSlot(0)
                        buddySwap_new(tidusposition)
                    elif turnchar == 6:
                        StealRight()
                    else:
                        print("Marker 12")
                        tidusposition = FFX_memory.getBattleCharSlot(0)
                        if tidusposition > 3:
                            buddySwap_new(tidusposition)
                        else:
                            escapeOne()
                else:
                    print("Marker 13")
                    tidusFlee()
            else:
                print("Marker 14")
                tidusFlee()

    print("Battle complete, now to deal with the aftermath.")
    FFX_memory.clickToControl3()
    if FFX_memory.overdriveState()[6] == 100:
        woodsVars[0] = True
    if FFX_memory.getUseItemsSlot(32) != 255:
        woodsVars[1] = True
    if FFX_memory.getUseItemsSlot(24) != 255:
        woodsVars[2] = True
    print("Checking battle formation.")
    if woodsVars[0] == True:
        if woodsVars[1] == True and woodsVars[2] == True:
            print("Party format: mwoodsdone")
            FFX_memory.fullPartyFormat_New("mwoodsdone", 11)
        else:
            FFX_memory.fullPartyFormat_New("mwoodsgotcharge", 11)
            print("Party format: mwoodsgotcharge")
    else:
        print("Party format: mwoodsneedcharge")
        FFX_memory.fullPartyFormat_New("mwoodsneedcharge", 11)
    print("Party format is now good. Let's check health.")
    # Heal logic
    partyHP = FFX_memory.getHP()
    if partyHP[0] < 450 or partyHP[6] < 180 or partyHP[2] + partyHP[4] < 500:
        healUp_New(4,11)
    print("And last, we'll update variables.")
    print("Rikku charged, stolen Fish Scale, stolen Arctic Wind")
    print(woodsVars)
    print("HP is good. Onward!")
    return woodsVars

# Process written by CrimsonInferno
def spherimorph():
    FFX_Logs.writeLog("Fight start: Spherimorph")
    FFX_Xbox.clickToBattle()

    FFXC.set_neutral()

    spellNum = 0
    tidusturns = 0
    rikkuturns = 0
    rikkuCounter = 0
    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            turnchar = FFX_memory.getBattleCharTurn()
            partyHP = FFX_memory.getBattleHP()
            if turnchar == 0:
                if tidusturns == 0:
                    FFX_Xbox.armorSwap(1)
                elif tidusturns == 1:
                    defend()
                else:
                    rikkuslotnum = FFX_memory.getBattleCharSlot(6)
                    buddySwap_new(rikkuslotnum)
                tidusturns += 1
            elif turnchar == 1:
                rikkuslotnum = FFX_memory.getBattleCharSlot(6)
                if rikkuslotnum < 4:
                    if partyHP[rikkuslotnum] == 0:
                        revive()
                    else:
                        defend()
                else:
                    defend()
            elif turnchar == 3:
                rikkuslotnum = FFX_memory.getBattleCharSlot(6)
                if rikkuslotnum < 4:
                    if partyHP[rikkuslotnum] == 0:
                        revive()
                    else:
                        defend()
                else:
                    defend()
            elif turnchar == 6:

                if rikkuturns == 0:
                    print("Throwing Grenade to check element")
                    grenadeslotnum = FFX_memory.getUseItemsSlot(35)
                    useItem(grenadeslotnum, "none")
                    time.sleep(2.5)
                    spellNum = FFX_Screen.spherimorphSpell()
                else:
                    print("Starting Rikku's overdrive")
                    while not FFX_Screen.PixelTestTol(306, 683, (223, 223, 223), 5):
                        FFX_Xbox.menuLeft()
                        rikkuCounter += 1
                        if rikkuCounter % 100 == 0:
                            print("Mark: pushing left for Rikku overdrive")
                    print("Mark: Overdrive ready")
                    time.sleep(0.3)
                    FFX_Xbox.menuB()
                    time.sleep(1)
                    FFX_Logs.writeStats("Spherimorph spell used:")
                    FFX_Logs.writeStats(str(spellNum))
                    if spellNum == 1:
                        FFX_Logs.writeStats("Creating Ice to counter Fire")
                        FFX_Logs.writeLog("Creating Ice to counter Fire")
                        print("Creating Ice")
                        FFX_memory.rikkuODItems('spherimorph1')
                    elif spellNum == 2:
                        FFX_Logs.writeStats("Creating Thunder to counter Water")
                        FFX_Logs.writeLog("Creating Thunder to counter Water")
                        print("Creating Water")
                        FFX_memory.rikkuODItems('spherimorph2')
                    elif spellNum == 3:
                        FFX_Logs.writeStats("Creating Water to counter Thunder")
                        FFX_Logs.writeLog("Creating Water to counter Thunder")
                        print("Creating Thunder")
                        FFX_memory.rikkuODItems('spherimorph3')
                    elif spellNum == 4:
                        FFX_Logs.writeStats("Creating Fire to counter Ice")
                        FFX_Logs.writeLog("Creating Fire to counter Ice")
                        print("Creating Fire")
                        FFX_memory.rikkuODItems('spherimorph4')

                    FFX_Xbox.menuB()  # Cast spell on Spherimorph
                    FFX_Xbox.menuB()  # Cast spell on Spherimorph
                    FFX_Xbox.menuB()  # Cast spell on Spherimorph

                rikkuturns += 1
            time.sleep(0.5)

    FFX_Xbox.SkipDialog(5)

#Process written by CrimsonInferno
def negator(): # AKA crawler
    FFX_Logs.writeLog("Fight start: Crawler/Negator")
    print("Starting battle with Crawler")
    FFX_Xbox.clickToBattle()
    # FFX_Screen.awaitTurn()

    marblesused = 0
    tidusturns = 0
    rikkuturns = 0
    kimahriturns = 0
    luluturns = 0
    yunaturns = 0

    while FFX_memory.battleActive(): #AKA end of battle screen
        FFXC.set_neutral()
        if FFX_memory.turnReady():
            turnchar = FFX_memory.getBattleCharTurn()
            if turnchar == 0:
                if tidusturns == 0:
                    print("Swapping Tidus for Rikku")
                    rikkuslotnum = FFX_memory.getBattleCharSlot(6)
                    buddySwap_new(rikkuslotnum)
                else:
                    defend()
                tidusturns += 1
            elif turnchar == 6:
                if luluturns < 2:
                    print("Using Lightning Marble")
                    time.sleep(0.2)
                    lightningmarbleslot = FFX_memory.getUseItemsSlot(30)
                    useItem(lightningmarbleslot, "left")
                else:
                    print("Starting Rikku's overdrive")
                    while not FFX_Screen.PixelTest(306, 683, (223, 223, 223)):
                        FFX_Xbox.menuLeft()
                    time.sleep(0.3)
                    FFX_Xbox.menuB()
                    time.sleep(1)
                    FFX_memory.rikkuODItems('crawler')
                    FFX_Xbox.menuB()
                    FFX_Xbox.menuB()  # Overdrive on boss, uses HP sphere or M.def sphere
                rikkuturns += 1
            elif turnchar == 3:
                if kimahriturns == 0:
                    lightningmarbleslot = FFX_memory.getUseItemsSlot(30)
                    useItem(lightningmarbleslot, "none")
                else:
                    yunaslotnum = FFX_memory.getBattleCharSlot(1)
                    buddySwap_new(yunaslotnum)
                kimahriturns += 1
            elif turnchar == 5:
                revive()
                luluturns += 1
            elif turnchar == 1:
                if yunaturns == 0:
                    defend()
                else:
                    tidusslotnum = FFX_memory.getBattleCharSlot(0)
                    buddySwap_new(tidusslotnum)
                yunaturns += 1
            else:
                defend()
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
    
    FFX_memory.clickToControl()

# Process written by CrimsonInferno
def seymourGuado():
    FFX_Logs.writeLog("Fight start: Seymour (Macalania)")
    FFX_Screen.awaitTurn()

    tidushaste = False
    kimahriconfused = False
    missbackup = False
    kimahridead = False
    aurondead = False
    wakkadead = False
    tidusturns = 0
    yunaturns = 0
    kimahriturns = 0
    auronturns = 0
    wakkaturns = 0
    rikkuturns = 0
    animahits = 0
    animamiss = 0

    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            turnchar = FFX_memory.getBattleCharTurn()
            for i in range(1, 4):
                if FFX_memory.getBattleHP()[i] == 0:
                    if FFX_memory.getBattleCharSlot(2) == i:
                        print("Auron is dead")
                        aurondead = True
                    elif FFX_memory.getBattleCharSlot(3) == i:
                        print("Kimahri is dead")
                        kimahridead = True
                    elif FFX_memory.getBattleCharSlot(4) == i:
                        print("Wakka is dead")
                        wakkadead = True
            if FFX_memory.getEnemyCurrentHP()[1] < 2999:
                attack('none')
                time.sleep(5)
                print("Should be last attack of the fight.")
            elif turnchar == 0:
                if tidusturns == 0:
                    print("Swap to Brotherhood")
                    FFX_Xbox.weapSwap(0)
                    time.sleep(0.5)
                elif tidusturns == 1:
                    print("Tidus Haste self")
                    tidusHaste('none')
                    tidushaste = True
                elif tidusturns == 2:
                    print("Talk to Seymour")
                    while not FFX_memory.otherBattleMenu():
                        FFX_Xbox.menuLeft()
                    while FFX_memory.battleCursor2() != 1:
                        FFX_Xbox.menuDown()
                    FFX_Xbox.menuB()
                    time.sleep(0.1)
                    FFX_Xbox.menuLeft()
                    FFX_Xbox.menuB()  # Tidus talk to Seymour
                    FFX_Xbox.SkipDialog(5.8)
                elif tidusturns == 3:
                    #time.sleep(0.5)
                    tidusODSeymour()
                elif tidusturns == 4:
                    wakkaposition = FFX_memory.getBattleCharSlot(4)
                    buddySwap_new(wakkaposition)
                elif animahits + animamiss == 3 and animamiss > 0 and missbackup == False:
                    luluposition = FFX_memory.getBattleCharSlot(5)
                    buddySwap_new(luluposition)
                elif tidushaste == False:
                    print("Tidus Haste self")
                    tidusHaste('none')
                    tidushaste = True
                elif animahits < 4:
                    oldHP = FFX_memory.getEnemyCurrentHP()[3]
                    attack('none')
                    time.sleep(1)
                    newHP = FFX_memory.getEnemyCurrentHP()[3]
                    if newHP < oldHP:
                        print("Hit Anima")
                        animahits += 1
                    else:
                        print("Miss Anima")
                        animamiss += 1
                else:
                    attack('none')
                tidusturns += 1
                print("Tidus turns: %d" % tidusturns)
            elif turnchar == 1:
                if yunaturns == 0:
                    FFX_Xbox.weapSwap(0)
                else:
                    auronslotnum = FFX_memory.getBattleCharSlot(2)
                    buddySwap_new(auronslotnum)
                yunaturns += 1
                print("Yuna turn, complete")
            elif turnchar == 3:
                if kimahriconfused == True:
                    tidusposition = FFX_memory.getBattleCharSlot(0)
                    rikkuposition = FFX_memory.getBattleCharSlot(6)
                    if tidusposition > 3:
                        buddySwap_new(tidusposition)
                    elif rikkuposition > 3:
                        buddySwap_new(rikkuposition)
                elif kimahriturns == 0:
                    print("Confused states:")
                    print("Yuna confusion: ", FFX_memory.confusedState(1))
                    print("Tidus confusion: ", FFX_memory.confusedState(0))
                    print("Kimahri confusion: ", FFX_memory.confusedState(3))
                    print("Auron confusion: ", FFX_memory.confusedState(2))
                    if FFX_memory.confusedState(0) == True:
                        kimahriposition = FFX_memory.getBattleCharSlot(3)
                        tidusposition = FFX_memory.getBattleCharSlot(0)
                        remedy(healerposition=kimahriposition,
                               targetposition=tidusposition,
                               direction="left")
                    elif FFX_memory.confusedState(1) == True:
                        kimahriposition = FFX_memory.getBattleCharSlot(3)
                        yunaposition = FFX_memory.getBattleCharSlot(1)
                        remedy(healerposition=kimahriposition,
                               targetposition=yunaposition,
                               direction="left")
                    else:
                        defend()
                elif kimahriturns == 1:
                    Steal()
                elif animamiss > 0 and (missbackup == False or FFX_Screen.faintCheck() == 0):
                    FFX_Xbox.weapSwap(0)
                else:
                    tidusposition = FFX_memory.getBattleCharSlot(0)
                    rikkuposition = FFX_memory.getBattleCharSlot(6)
                    if tidusposition > 3:
                        buddySwap_new(tidusposition)
                    elif rikkuposition > 3:
                        buddySwap_new(rikkuposition)
                    else:
                        Steal()
                kimahriturns += 1
                print("Kimahri turn, complete")
            elif turnchar == 2:
                if auronturns == 0:
                    print("Confused states:")
                    print("Yuna confusion: ", FFX_memory.confusedState(1))
                    print("Tidus confusion: ", FFX_memory.confusedState(0))
                    print("Kimahri confusion: ", FFX_memory.confusedState(3))
                    print("Auron confusion: ", FFX_memory.confusedState(2))
                    if FFX_memory.confusedState(3) == True:
                        auronposition = FFX_memory.getBattleCharSlot(2)
                        kimahriposition = FFX_memory.getBattleCharSlot(3)
                        remedy(healerposition=auronposition,
                               targetposition=kimahriposition,
                               direction="left")
                        kimahriconfused = True
                    else:
                        defend()
                elif animamiss > 0 and (missbackup == False or FFX_Screen.faintCheck() == 0):
                    if kimahridead == True and rikkuturns == 0:
                        rikkuposition = FFX_memory.getBattleCharSlot(6)
                        buddySwap_new(rikkuposition)
                    else:
                        FFX_Xbox.weapSwap(1)
                else:
                    tidusposition = FFX_memory.getBattleCharSlot(0)
                    rikkuposition = FFX_memory.getBattleCharSlot(6)
                    if tidusposition > 3:
                        buddySwap_new(tidusposition)
                    elif rikkuposition > 3:
                        buddySwap_new(rikkuposition)
                    else:
                        defend()
                auronturns += 1
                print("Auron turn, complete")
            elif turnchar == 4:
                if wakkaturns == 0:
                    FFX_Xbox.weapSwap(0)
                elif animamiss > 0 and (missbackup == False or FFX_Screen.faintCheck() == 0):
                    if kimahridead == True and rikkuturns == 0:
                        rikkuposition = FFX_memory.getBattleCharSlot(6)
                        buddySwap_new(rikkuposition)
                    else:
                        FFX_Xbox.weapSwap(0)
                else:
                    tidusposition = FFX_memory.getBattleCharSlot(0)
                    rikkuposition = FFX_memory.getBattleCharSlot(6)
                    if tidusposition > 3:
                        buddySwap_new(tidusposition)
                    elif rikkuposition > 3:
                        buddySwap_new(rikkuposition)
                    else:
                        defend()
                wakkaturns += 1
                print("Wakka turn, complete")
            elif turnchar == 6:
                if FFX_Screen.faintCheck() == 2:
                    reviveAll()
                    missbackup = True
                    tidushaste = False
                elif animamiss > 0 and (missbackup == False or FFX_Screen.faintCheck() == 0):
                    if kimahridead == True and rikkuturns == 0:
                        Steal()
                    else:
                        tidusposition = FFX_memory.getBattleCharSlot(0)
                        yunaposition = FFX_memory.getBattleCharSlot(1)
                        luluposition = FFX_memory.getBattleCharSlot(5)
                        for i in range(4, 8):
                            if FFX_memory.getBattleFormation()[i] not in [tidusposition, yunaposition, luluposition]:
                                swapposition = i
                                break
                        buddySwap_new(swapposition)
                elif animahits < 4:
                    Steal()
                else:
                    defend()
                rikkuturns += 1
                print("Rikku turn, complete")
            elif turnchar == 5:
                if missbackup == False:
                    revive()
                    missbackup = True
                else:
                    tidusposition = FFX_memory.getBattleCharSlot(0)
                    rikkuposition = FFX_memory.getBattleCharSlot(6)
                    if tidusposition > 3:
                        buddySwap_new(tidusposition)
                    elif rikkuposition > 3:
                        buddySwap_new(rikkuposition)
                    else:
                        defend()
                print("Lulu turn, complete")
            else:
                print("No turn. Holding for next action.")
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
            print("Diag skip")
    print("Battle summary screen")
    FFXC.set_value('BtnB', 1)
    time.sleep(2.8)
    FFXC.set_value('BtnB', 0)

# Process written by CrimsonInferno
def fullheal(healerposition: int, targetposition: int, direction: str):
    print("Full Heal function")
    if FFX_memory.getThrowItemsSlot(2) < 255:
        itemnum = 2
        itemname = "X-Potion"
    elif FFX_memory.getThrowItemsSlot(8) < 255:
        itemnum = 8
        itemname = "Elixir"
    elif FFX_memory.getThrowItemsSlot(3) < 255:
        itemnum = 3
        itemname = "Mega-Potion"
    else:
        itemnum = -1
        itemname = "noitemfound"
    if itemnum >= 0:

        FFX_Logs.writeLog("Using %s" % itemname)
        print("Using %s" % itemname)
        while FFX_memory.battleMenuCursor() != 1:
            FFX_Xbox.menuDown()
        FFX_Xbox.menuB()  # Item menu open.
        time.sleep(0.3)
        cursor = 1
        itemPos = FFX_memory.getThrowItemsSlot(itemnum)
        if itemPos % 2 == 0:
            FFX_Xbox.menuRight()
            cursor += 1
        if cursor == itemPos:
            FFX_Xbox.menuB()
        else:
            while cursor != itemPos:
                FFX_Xbox.menuDown()
                cursor += 2
            FFX_Xbox.menuB()
        print("Direction: ", direction)
        direction = direction.lower()
        print("Target: ", targetposition)
        print("Healer: ", healerposition)
        if (targetposition - healerposition) % 3 == 1:
            if direction == "left":
                FFX_Xbox.menuLeft()
            elif direction == "right":
                FFX_Xbox.menuRight()
            elif direction == "up":
                FFX_Xbox.menuUp()
            elif direction == "down":
                FFX_Xbox.menuDown()
        elif (targetposition - healerposition) % 3 == 2:
            if direction == "left":
                FFX_Xbox.menuRight()
            elif direction == "right":
                FFX_Xbox.menuLeft()
            elif direction == "up":
                FFX_Xbox.menuDown()
            elif direction == "down":
                FFX_Xbox.menuUp()

        FFX_Xbox.menuB()
        FFX_Xbox.menuB()

        return 1

    else:
        print("No restorative items available")
        return 0


# Process written by CrimsonInferno
def wendigoresheal(turnchar: int, usepowerbreak: int, tidusmaxHP: int):
    print("Wendigo Res/Heal function")
    partyHP = FFX_memory.getBattleHP()
    if FFX_Screen.faintCheck() == 2:
        print("2 Characters are dead")
        if FFX_memory.getThrowItemsSlot(7) < 255:
            reviveAll()
        elif FFX_memory.getThrowItemsSlot(6) < 255:
            revive()  # This should technically target tidus but need to update this logic
    # If just Tidus is dead revive him
    elif partyHP[FFX_memory.getBattleCharSlot(0)] == 0:
        print("Reviving tidus")
        revive()
    elif usepowerbreak == True:
        print("Swapping to Auron to Power Break")
        swapposition = FFX_memory.getBattleCharSlot(2)
        buddySwap_new(swapposition)
    # If tidus is less than max HP heal him
    elif partyHP[FFX_memory.getBattleCharSlot(0)] < tidusmaxHP:
        print("Tidus need healing")
        if fullheal(healerposition=FFX_memory.getBattleCharSlot(turnchar),
                    targetposition=FFX_memory.getBattleCharSlot(0),
                    direction="left") == 0:
            if FFX_Screen.faintCheck():
                print("No healing available so reviving instead")
                revive()
            else:
                defend()
    elif FFX_Screen.faintCheck():
        print("Reviving non-Tidus")
        revive()
    else:
        return 0

    return 1


# Process written by CrimsonInferno
def wendigo():
    phase = 0
    curtain = False
    YunaAP = False
    guadosteal = False
    powerbreak = False
    powerbreakused = False
    usepowerbreak = False
    tidushealself = False
    tidusmaxHP = 1520
    tidusdied = False
    tidushaste = False
    FFX_Logs.writeLog("Fight start: Wendigo")
    
    FFX_Screen.awaitTurn()

    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            print("Test")
            partyHP = FFX_memory.getBattleHP()
            turnchar = FFX_memory.getBattleCharTurn()

            if partyHP[FFX_memory.getBattleCharSlot(0)] == 0:
                print("Tidus is dead")
                tidushaste = False
                powerbreak = True
                usepowerbreak = powerbreak and not powerbreakused

            if turnchar == 1:
                print("Yuna's Turn")
                # If Yuna still needs AP:
                if YunaAP == False:
                    print("Yuna still needs AP")
                    # If both other characters are dead Mega-Phoenix if available, otherwise PD
                    if wendigoresheal(turnchar=turnchar, usepowerbreak=usepowerbreak, tidusmaxHP=tidusmaxHP) == 0:
                        defend()
                    YunaAP = True
                # If Yuna has had a turn swap for Lulu
                else:
                    if usepowerbreak:
                        print("Swapping to Auron to Power Break")
                        swapindex = 2
                    else:
                        print("Swapping to Lulu")
                        swapindex = 5
                    swapposition = FFX_memory.getBattleCharSlot(swapindex)
                    buddySwap_new(swapposition)  # Swap for Lulu/Auron
            elif turnchar == 0:
                if tidushaste == False:
                    print("Tidus Haste self")
                    tidusHaste('none')
                    tidushaste = True
                elif phase == 0:
                    print("Switch to Brotherhood")
                    FFX_Xbox.weapSwap(0)
                    phase += 1
                elif phase == 1:
                    print("Attack top Guado")
                    while not FFX_memory.otherBattleMenu():
                        FFX_Xbox.menuB()
                    while FFX_memory.battleTargetId() != 22:
                        FFX_Xbox.menuDown()
                    FFX_Xbox.menuB()
                    FFX_Xbox.menuB()
                    phase += 1
                elif FFX_Screen.faintCheck() == 2:
                    print("2 Characters are dead")
                    tidushealself = True
                    if FFX_memory.getThrowItemsSlot(7) < 255:
                        reviveAll()
                    elif FFX_memory.getThrowItemsSlot(6) < 255:
                        revive()
                elif tidushealself == True:
                    if partyHP[FFX_memory.getBattleCharSlot(0)] < tidusmaxHP:
                        print("Tidus just used Phoenix Down / Mega Phoenix so needs to heal himself")
                        if fullheal(healerposition=FFX_memory.getBattleCharSlot(turnchar),
                                    targetposition=FFX_memory.getBattleCharSlot(0),
                                    direction="left") == 0:
                            if FFX_Screen.faintCheck():
                                print("No healing items so revive someone instead")
                                revive()
                            else:
                                print("No healing items so just go face")
                                attack('left')
                    else:
                        attack('left')
                    tidushealself = False
                else:
                    attack('left')
                time.sleep(0.2)
            elif turnchar == 6:
                if phase == 2:
                    phase += 1
                    lightcurtainslot = FFX_memory.getUseItemsSlot(57)
                    if lightcurtainslot < 255:
                        print("Using Light Curtain on Tidus")
                        if (FFX_memory.getBattleCharSlot(0) - FFX_memory.getBattleCharSlot(6)) % 3 == 1:
                            useItem(lightcurtainslot, 'left')
                        else:
                            useItem(lightcurtainslot, 'right')
                        curtain = True
                    else:
                        print("No Light Curtain")
                        print("Swapping to Auron to Power Break")
                        swapposition = FFX_memory.getBattleCharSlot(2)
                        buddySwap_new(swapposition)  # Swap for Auron
                        powerbreak = True
                        usepowerbreak = True
                elif wendigoresheal(turnchar=turnchar, usepowerbreak=usepowerbreak, tidusmaxHP=tidusmaxHP) == 0:
                    if guadosteal == False:
                        Steal()
                        guadosteal = True
                    else:
                        defend()
            elif turnchar == 2:
                if usepowerbreak == True:
                    print("Using Power Break")
                    FFX_Xbox.menuDown()
                    FFX_Xbox.menuB()
                    time.sleep(0.6)
                    FFX_Xbox.menuB()
                    time.sleep(0.6)
                    FFX_Xbox.menuLeft()
                    FFX_Xbox.menuB()  # Auron uses Armor Break
                    time.sleep(1)
                    powerbreakused = True
                    usepowerbreak = False
                else:
                    if wendigoresheal(turnchar=turnchar, usepowerbreak=usepowerbreak, tidusmaxHP=tidusmaxHP) == 0:
                        defend()
            else:
                if wendigoresheal(turnchar=turnchar, usepowerbreak=usepowerbreak, tidusmaxHP=tidusmaxHP) == 0:
                    defend()

def zu():
    while not FFX_memory.menuOpen():
        if FFX_Screen.BattleScreen():
            if FFX_memory.partySize() <= 2:
                defend()
            else:
                fleeAll()
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB() #Skip Dialog
    FFX_memory.clickToControl()

def bikanelBattleLogic(status):
    #status should be an array length 2
    #[rikkuCharged, speedNeeded, powerNeeded, itemsNeeded]
    battleNum = FFX_memory.getBattleNum()
    throwPower = False
    throwSpeed = False
    print("---------------Starting desert battle: ", battleNum)
    
    #First, determine what the best case scenario is for each battle.
    if battleNum == 199:
        stealDirection = 'none'
        if status[1] == True:
            throwSpeed = True
        if status[2] == True:
            throwPower = True
    if battleNum == 200:
        stealDirection = 'none'
        if status[1] == True:
            throwSpeed = True
        if status[2] == True:
            throwPower = True
    if battleNum == 208:
        stealDirection = 'none'
        if status[1] == True:
            throwSpeed = True
        if status[2] == True:
            throwPower = True
    if battleNum == 209:
        stealDirection = 'right'
        if status[1] == True:
            throwSpeed = True
        if status[2] == True:
            throwPower = True
    if battleNum == 218:
        stealDirection = 'none'
        if status[2] == True:
            throwPower = True
    if battleNum == 221:
        stealDirection = 'up'
        if status[1] == True:
            throwSpeed = True
        if status[2] == True:
            throwPower = True
    if battleNum == 222:
        stealDirection = 'left'
        if status[2] == True:
            throwPower = True
    
    zuBattles = [202, 211, 216, 225]
    if battleNum in zuBattles: #Zu battles
        stealDirection = 'none'
    if battleNum == 217: #Specal Zu battle
        stealDirection = 'up' #Not confirmed
    #Flee from these battles
    fleeBattles = [201, 203, 204, 205, 210, 212, 213, 215, 217, 219, 223, 224, 226, 227]
    
    #Next, determine what we want to do
    if battleNum in fleeBattles:
        battleGoal = 3 #Nothing to do here, we just want to flee.
    else:
        items = updateStealItemsDesert()
        if items[1] == 0 and items[2] == 0:
            battleGoal = 0 #Steal an item
        elif status[3] <= -1 and (throwPower == True or throwSpeed == True): #Extra items into power/speed
            battleGoal = 1 #Throw an item
        elif status[3] > -1:
            battleGoal = 0 #Steal to an excess of one item (so we can throw in future battles)
        elif status[0] == False:
            battleGoal = 2 #Rikku still needs charging.
        else:
            battleGoal = 3 #Nothing to do but get to Home.
        
    #Then we take action.
    if battleGoal == 0: #Steal an item
        print("Looking to steal an item.")
        while not FFX_memory.menuOpen():
            if FFX_memory.turnReady():
                if FFX_memory.getBattleCharTurn() == 0:
                    buddySwapKimahri()
                    FFX_Screen.awaitTurn()
                    if stealDirection == 'left':
                        StealLeft()
                    elif stealDirection == 'right':
                        StealRight()
                    elif stealDirection == 'up':
                        StealUp()
                    elif stealDirection == 'down':
                        StealDown()
                    else:
                        Steal()
                elif status[0] == False:
                    if FFX_memory.getBattleCharTurn() == 6:
                        attack('none')
                    else:
                        escapeOne()
                else:
                    buddySwapTidus()
                    FFX_Screen.awaitTurn()
                    fleeAll()
    elif battleGoal == 1: #Throw an item
        print("Throw item with Kimahri, everyone else escape.")
        while not FFX_memory.menuOpen():
            if FFX_memory.turnReady():
                if FFX_memory.getBattleCharTurn() == 0:
                    buddySwapKimahri()
                    FFX_Screen.awaitTurn()
                    
                    if items[2] >= 1:
                        itemToUse = 40
                    elif items[3] >= 1:
                        itemToUse = 39
                    else:
                        itemToUse = 37
                    
                    useItem(FFX_memory.getUseItemsSlot(itemToUse), 'none')
                else:
                    buddySwapTidus()
                    FFX_Screen.awaitTurn()
                    fleeAll()
    elif battleGoal == 2: #Charge Rikku
        print("Attack/Steal with Rikku, everyone else escape.")
        while not FFX_memory.menuOpen():
            if FFX_memory.turnReady():
                if FFX_memory.getBattleCharTurn() == 6:
                    attack('none')
                else:
                    escapeOne()
    elif battleGoal == 3: #Flee, nothing else.
        print("Flee all battles, nothing more to do.")
        fleeAll()

def updateStealItemsDesert():
    itemArray = [0,0,0,0]
    #Bomb cores
    index = FFX_memory.getItemSlot(27)
    if index == 255:
        itemArray[0] = 0
    else:
        itemArray[0] = FFX_memory.getItemCountSlot(index)
        
    #Sleeping Powders
    index = FFX_memory.getItemSlot(37)
    if index == 255:
        itemArray[1] = 0
    else:
        itemArray[1] = FFX_memory.getItemCountSlot(index)
        
    #Smoke Bombs
    index = FFX_memory.getItemSlot(40)
    if index == 255:
        itemArray[2] = 0
    else:
        itemArray[2] = FFX_memory.getItemCountSlot(index)
        
    #Silence Grenades
    index = FFX_memory.getItemSlot(39)
    if index == 255:
        itemArray[3] = 0
    else:
        itemArray[3] = FFX_memory.getItemCountSlot(index)
    
    return itemArray

def sandragora(version):
    FFX_Screen.awaitTurn()
    if version == 1: #Kimahri's turn
        tidusHaste('left')
        FFX_Screen.awaitTurn()
        if FFX_Screen.turnRikku():
            buddySwapKimahri()
            FFX_Screen.awaitTurn()
        print("Now Kimahri will use his overdrive.")
        kimahriOD(4)
        FFX_memory.clickToControl()
    else: #Auron's turn
        tidusHaste('down')
        FFX_Screen.awaitTurn()
        if FFX_Screen.turnKimahri() or FFX_Screen.turnRikku():
            print("Kimahri/Rikku taking a spare turn. Just defend.")
            defend()
            time.sleep(0.2)
            FFX_Screen.awaitTurn()
        print("Setting up Auron overdrive")
        FFX_Xbox.menuLeft()
        time.sleep(1)
        FFX_Xbox.menuB()
        time.sleep(0.5)
        FFX_Xbox.menuRight()
        FFX_Xbox.menuB()
        FFX_Xbox.menuB()
        odSuccess = True
        while not FFX_Screen.PixelTestTol(343, 369, (255, 157, 69), 20):
            if FFX_memory.turnReady():
                odSuccess = False
                break

        if odSuccess == True:
            time.sleep(0.4)
            # Overdrive pattern
            print("Auron Overdrive")
            FFX_Xbox.menuY()
            FFX_Xbox.menuA()
            FFX_Xbox.menuX()
            FFX_Xbox.menuB()
            FFX_Xbox.menuLeft()
            FFX_Xbox.menuRight()
            FFX_Xbox.menuB()
            print("Overdrive done")
            FFX_Screen.clickToMap1()

def bikanelCharge_old(chargeState):
    FFX_Logs.writeLog("Fight start: Charging Kimahri and Rikku, Bikanel")

    # chargeState = [False,False,tidusSwap]
    # test = FFX_Screen.desertCharge()
    # print(test)
    # chargeState[0] = test[0]
    # chargeState[1] = test[1]
    print("Starting battle with vars: ", chargeState)
    turns = 0
    if chargeState == [True, True]:
        print("Just flee the whole fight.")
        fleeAll()
    else:
        print("Continuing to charge Rikku and Kimahri.")
        while not FFX_memory.menuOpen(): #AKA end of battle screen
            if FFX_memory.turnReady():
                print("Battle screen.")
                turns += 1
                if FFX_Screen.turnLulu():
                    escapeOne()
                elif FFX_Screen.faintCheck() and not FFX_Screen.turnLulu():
                    revive()
                    print("Reviving character")
                elif FFX_Screen.turnTidus():
                    print("Turn Tidus")
                    escapeOne()
                    print("Attempting Escape")
                elif FFX_Screen.turnKimahri():
                    print("Kimahri's turn")
                    chargeState[1] = FFX_Screen.checkCharge(1)
                    if chargeState[1]:
                        escapeOne()
                        print("Attempting Escape")
                    else:
                        getHP = FFX_memory.getBattleHP()
                        if getHP[1] != 1244:
                            useItem(20, 'none')
                            print("Using an Al Bhed potion")
                        else:
                            print("No need to heal. Attacking to kill a turn.")
                            attack('none')
                elif FFX_Screen.turnRikku():
                    print("Turn Rikku")
                    chargeState[0] = FFX_Screen.checkCharge(1)
                    if chargeState[0]:
                        escapeOne()
                    else:
                        getHP = FFX_memory.getBattleHP()
                        if getHP[1] != 360:
                            useItem(20, 'none')
                            print("Using an Al Bhed potion")
                        else:
                            print("No need to heal. Attacking to kill a turn.")
                            attack('none')
                elif FFX_Screen.turnAuron():
                    escapeOne()
    FFX_memory.clickToControl()
    return chargeState

def desertSpeed_old(chargeState):
    battleNum = FFX_memory.getBattleNum()
    if battleNum == 199 or battleNum == 200 or \
            battleNum == 208 or battleNum == 209 or \
            battleNum == 221 or battleNum == 222:
        if FFX_memory.getUseItemsSlot(39) != 255:
            print("Throwing nades if Rikku is in the party.")
            FFX_Screen.awaitTurn()
            buddySwap(1)  # Tidus for Rikku
            FFX_Screen.awaitTurn()
            useItem(FFX_memory.getUseItemsSlot(39), 'none')

            while not FFX_memory.userControl():
                if FFX_memory.turnReady():
                    buddySwap(1)
                    FFX_Screen.awaitTurn()
                    tidusFlee()
                else:
                    FFX_Xbox.menuB()
        else:
            print("No grenades for picking up speed spheres. Resorting to memory 'fixing'")
            speed = FFX_memory.setSpeed(20)
            print("New speed value: ", speed)
    else:
        fleeAll()

    FFX_memory.desertFormat(chargeState[0])
    speedCount = FFX_memory.getSpeed()
    if speedCount >= 10:
        return False  # Speed spheres no longer needed.
    else:
        return True  # Still need speed spheres.

def desertFights_old(sandy):
    FFX_Logs.writeLog("Fight start: Bikanel, looking for Sandragoras")
    complete = 0
    turn = 1
    battleNum = FFX_memory.getBattleNum()
    FFX_Xbox.menuB()  # Check if this is one of the required fights.
    if battleNum == 234:
        if sandy == 0:
            print("First Sandragora")
            print("Tidus will use Haste on Kimahri")
            FFX_Xbox.menuA()
            FFX_Xbox.menuA()
            time.sleep(0.3)
            tidusHaste('left')
            FFX_Screen.awaitTurn()
            print("Now Kimahri will use his overdrive.")
            kimahriOD(4)
            FFX_Screen.clickToMap1()
        elif sandy == 1:
            print("Second Sandragora")
            print("Tidus will use Haste on Auron")
            FFX_Xbox.menuA()
            FFX_Xbox.menuA()
            time.sleep(0.5)
            tidusHaste('down')
            FFX_Screen.awaitTurn()
            if FFX_Screen.turnKimahri():
                print("Kimahri taking a spare turn. Just defend.")
                defend()
                time.sleep(0.2)
                FFX_Screen.awaitTurn()
            print("Setting up Auron overdrive")
            FFX_Xbox.menuLeft()
            time.sleep(1)
            FFX_Xbox.menuB()
            time.sleep(0.5)
            FFX_Xbox.menuRight()
            FFX_Xbox.menuB()
            FFX_Xbox.menuB()
            odSuccess = True
            while not FFX_Screen.PixelTestTol(343, 369, (255, 157, 69), 20):
                if FFX_memory.turnReady():
                    odSuccess = False
                    break

            if odSuccess == True:
                time.sleep(0.4)
                # Overdrive pattern
                print("Auron Overdrive")
                FFX_Xbox.menuY()
                FFX_Xbox.menuA()
                FFX_Xbox.menuX()
                FFX_Xbox.menuB()
                FFX_Xbox.menuLeft()
                FFX_Xbox.menuRight()
                FFX_Xbox.menuB()
                print("Overdrive done")
                FFX_Screen.clickToMap1()
        else:
            FFX_Xbox.menuA()
        sandy += 1
    else:
        FFX_Xbox.menuA()
        FFX_Xbox.menuA()
        time.sleep(0.5)
        fleeAll()
    return sandy


def home1():
    FFX_Logs.writeLog("Fight start: Home 1")
    FFXC.set_neutral()
    FFX_Xbox.clickToBattle()
    print("Tidus vs Bombs")
    tidusHaste('none')
    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            #print(FFX_memory.getEnemyCurrentHP())
            if FFX_Screen.faintCheck() > 0:
                revive()
            elif FFX_Screen.turnTidus():
                attack('none')
            elif FFX_Screen.turnAuron() and FFX_memory.getEnemyCurrentHP()[0] != 0:
                attack('none')
            else:
                defend()
    print("Home 1 shows as fight complete.")
    FFX_memory.clickToControl()

def home2():
    FFX_Logs.writeLog("Fight start: Home 2")
    FFX_Xbox.clickToBattle()

    print("Kimahri vs dual horns")
    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            kimahriposition = FFX_memory.getBattleCharSlot(3)
            print(kimahriposition)
            if FFX_Screen.turnKimahri():
                kimahriOD(4)
            elif kimahriposition > 3:
                buddySwap_new(kimahriposition)  # Tidus for Kimahri
                time.sleep(0.2)
                lancetHome('none')
            else:
                defend()
    print("Home 2 shows as fight complete.")
    FFX_memory.clickToControl()
    FFX_memory.fullPartyFormat('desert1')

def home3():
    FFX_Logs.writeLog("Fight start: Home 3")
    FFX_Xbox.clickToBattle()
    time.sleep(1)
    randomFight = tidusFlee()
    complete = 0
    while complete == 0:
        if randomFight == 2:
            complete = 1
        else:
            FFX_memory.clickToControl()

            FFXC.set_movement(-1, -1)
            time.sleep(6)
            FFXC.set_neutral()
            FFX_Xbox.clickToBattle()
            randomFight = tidusFlee()

    print("Tidus vs dual horns")
    tidusHaste('none')

    FFX_Xbox.clickToBattle()
    if not FFX_Screen.turnTidus():
        while not FFX_Screen.turnTidus():
            defend()
            time.sleep(0.2)
            FFX_Xbox.clickToBattle()
    tidusOD()

    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            if FFX_Screen.turnTidus():
                attack('none')
            elif FFX_Screen.faintCheck() > 0:
                revive()
            elif FFX_Screen.turnKimahri():
                useItem(3, 'none')
            else:
                defend()
    print("Home 3 shows as fight complete.")
    FFX_memory.clickToControl()


def home4():
    FFX_Logs.writeLog("Fight start: Home 4")
    FFX_Xbox.clickToBattle()

    print("Kimahri vs Chimera")
    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            kimahriposition = FFX_memory.getBattleCharSlot(3)
            if FFX_Screen.turnKimahri():
                kimahriOD(5)
            elif kimahriposition > 3:
                buddySwap_new(kimahriposition)  # Tidus for Kimahri
                time.sleep(0.2)
                lancetHome('none')
            else:
                defend()
    print("Home 4 shows as fight complete.")
    FFX_memory.clickToControl()


# Process written by CrimsonInferno
def Evrae():
    FFX_Logs.writeLog("Fight start: Evrae")
    tidusPrep = 0
    tidusAttacks = 0
    rikkuTurns = 0
    kimahriTurns = 0
    lunarCurtain = False
    odComplete = [False, False]
    itemFinderCounter = 0
    FFXC.set_neutral()
    FFX_Xbox.clickToBattle()  # This gets us past the tutorial and all the dialog.

    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            turnchar = FFX_memory.getBattleCharTurn()
            print("Tidus prep turns: ", tidusPrep)
            # print("otherTurns: ", otherTurns)
            if turnchar == 0:
                print("Registering Tidus's turn")
                if tidusPrep == 0:
                    tidusPrep = 1
                    tidusHaste('none')
                elif tidusPrep == 1:
                    tidusPrep += 1
                    cheer()
                elif tidusPrep == 2 and rikkuTurns == 0:
                    FFX_Xbox.armorSwap(0)
                elif tidusPrep == 2 and tidusAttacks == 2:
                    tidusPrep += 1
                    cheer()
                else:
                    tidusAttacks += 1
                    attack('none')
            elif turnchar == 6:
                print("Registering Rikku's turn")
                if rikkuTurns == 0:
                    rikkuTurns += 1
                    print("Rikku overdrive")
                    while not FFX_Screen.PixelTest(306, 683, (223, 223, 223)):
                        FFX_Xbox.menuLeft()
                    time.sleep(0.4)
                    FFX_Xbox.menuB()
                    time.sleep(0.8)
                    FFX_memory.rikkuODItems('Evrae')

                    FFX_Xbox.menuB()  # Engage overdrive
                    FFX_Xbox.menuB()  # For safety
                else:
                    Steal()
            else:
                print("Registering Kimahri's turn")
                if FFX_memory.getBattleHP()[1] < 1520:
                    print("Kimahri should attempt to heal a character.")
                    kimahriTurns += 1
                    if fullheal(healerposition=FFX_memory.getBattleCharSlot(turnchar),
                                targetposition=FFX_memory.getBattleCharSlot(0),
                                direction="up") == 0:
                        print("Restorative item not found.")
                        Steal()
                    else:
                        print("Heal should be successful.")
                else:
                    print("No attempt to heal.")
                    Steal()
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
    FFXC.set_value('BtnB', 1)
    time.sleep(3.5)
    FFXC.set_value('BtnB', 0)

    while not FFX_memory.cutsceneSkipPossible():
        time.sleep(0.035)
    FFX_Xbox.skipSceneSpec()


def guards(groupNum):
    FFX_Logs.writeLog("Fight start: Bevelle Guards")
    rikkuHeal = False
    turnNum = 0
    rikkuTurns = 0
    items = [0,0,0,0]
    FFX_Xbox.clickToBattle()
    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            items = updateStealItemsDesert()
            if FFX_Screen.turnTidus():
                turnNum += 1
                if groupNum == 5 and turnNum == 1:
                    tidusHaste('left')
                else:
                    attack('none')
            elif FFX_Screen.turnKimahri():
                if groupNum == 5 and items[0] > 1:
                    enemyHP = FFX_memory.getEnemyCurrentHP()
                    if enemyHP[0] != 0:
                        useItem(FFX_memory.getUseItemsSlot(27), 'left')
                    else:
                        useItem(FFX_memory.getUseItemsSlot(27), 'none')
                elif groupNum in [2,4,5]:
                    if items[2] >= 1:
                        itemToUse = 40
                    elif items[3] >= 1:
                        itemToUse = 39
                    else:
                        itemToUse = 37
                    useItem(FFX_memory.getUseItemsSlot(itemToUse), 'none')
                else:
                    defend()
            elif FFX_Screen.turnRikku():
                rikkuTurns += 1
                if groupNum == 1:
                    defend()
                elif groupNum == 3:
                    if rikkuTurns == 1:
                        if FFX_memory.getUseItemsSlot(20) != 255:
                            useItem(FFX_memory.getUseItemsSlot(20), 'none')
                        else:
                            defend()
                    else:
                        defend()
                elif groupNum == 2 or groupNum == 4:
                    if items[1] >= 1:
                        itemToUse = 37
                    elif items[2] >= 1:
                        itemToUse = 40
                    elif items[3] >= 1:
                        itemToUse = 39
                    useItem(FFX_memory.getUseItemsSlot(itemToUse), 'none')
                else:
                    if rikkuTurns < 3:
                        if items[2] >= 1:
                            itemToUse = 40
                        elif items[3] >= 1:
                            itemToUse = 39
                        elif items[1] >= 1:
                            itemToUse = 37
                        useItem(FFX_memory.getUseItemsSlot(itemToUse), 'none')
                    else:
                        defend()
                
    while not FFX_memory.menuOpen():
        if FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
    FFXC.set_value('BtnB', 1)
    time.sleep(2.8)
    FFXC.set_value('BtnB', 0)


def guards_old(groupNum):
    FFX_Logs.writeLog("Fight start: Bevelle Guards")
    rikkuHeal = False
    turnNum = 0
    FFX_Xbox.clickToBattle()
    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            if FFX_Screen.turnTidus():
                turnNum += 1
                if turnNum == 1 and groupNum == 1:
                    attack('left')
                elif turnNum == 1 and groupNum == 3:
                    attack('down')
                elif turnNum == 1 and groupNum == 5:
                    attack('right')
                elif turnNum == 1 and (groupNum == 2 or groupNum == 4):
                    tidusHaste('none')
                elif turnNum == 2 and groupNum == 2:
                    attack('left')
                elif turnNum == 2 and groupNum == 4:
                    attack('up')
                else:
                    attack('none')
            elif groupNum == 5 and FFX_Screen.faintCheck() > 0:
                revive()
            elif FFX_Screen.turnRikku():
                if groupNum < 5 and rikkuHeal == False:
                    potSlot = FFX_memory.getUseItemsSlot(20)
                    useItem(potSlot, 'none')
                    rikkuHeal = True
                else:
                    defend()
            elif FFX_Screen.turnAuron():
                if groupNum == 5:
                    attack('none')
                else:
                    defend()

    while not FFX_memory.menuOpen():
        if FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
    FFXC.set_value('BtnB', 1)
    time.sleep(2.8)
    FFXC.set_value('BtnB', 0)


def isaaru():
    FFX_Logs.writeLog("Fight start: Isaaru (Via Purifico)")
    FFX_Xbox.clickToBattle()
    confirm = 0
    counter = 0
    while confirm == 0:
        counter += 1
        if FFX_memory.getBattleNum() >= 258 and FFX_memory.getBattleNum() <= 260:  # Now fighting Isaaru
            confirm = 2
        else:
            confirm = 1

    if confirm == 1: #Larvae battle
        aeonSummon(2)
        while FFX_memory.battleActive():
            FFXC.set_value('BtnB', 1)
            time.sleep(0.035)
            FFXC.set_value('BtnB', 0)
            time.sleep(0.035)
        time.sleep(0.5)
    else: #Isaaru/aeon battle
        while not FFX_memory.menuOpen():
            if FFX_memory.turnReady():
                if FFX_Screen.turnYuna():
                    if FFX_memory.getBattleNum() == 260:
                        aeonSummon(2)
                    else:
                        aeonSummon(4)
                else:
                    FFX_Xbox.SkipDialog(3)
                time.sleep(0.5)
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.menuB()
    FFXC.set_value('BtnB', 1)
    time.sleep(2.8)
    FFXC.set_value('BtnB', 0)
    
    confirm -= 1
    return confirm


def altanaheal():

    if FFX_memory.getThrowItemsSlot(2) < 255:
        itemnum = 2
        itemname = "X-Potion"
    elif FFX_memory.getThrowItemsSlot(8) < 255:
        itemnum = 8
        itemname = "Elixir"
    elif FFX_memory.getThrowItemsSlot(6) < 255:
        itemnum = 6
        itemname = "Phoenix Down"
    else:
        itemnum = -1
        itemname = "noitemfound"
    if itemnum >= 0:

        FFX_Logs.writeLog("Using %s" % itemname)
        print("Using %s" % itemname)
        if FFX_Screen.PixelTestTol(277, 726, (223, 223, 223), 5):
            FFX_Xbox.menuDown()
        else:
            while not FFX_Screen.PixelTestTol(276, 769, (218, 218, 218), 5):  # Item option isn't showing up
                if FFX_Screen.BattleComplete():
                    return
                FFX_Xbox.menuDown()
            while not FFX_Screen.PixelTestTol(130, 779, (165, 167, 165),
                                              5):  # Item option isn't selected (it's always last)
                if FFX_Screen.BattleComplete():
                    return
                FFX_Xbox.menuDown()
        FFX_Xbox.menuB()  # Item menu open.
        time.sleep(0.3)
        cursor = 1
        itemPos = FFX_memory.getThrowItemsSlot(itemnum)
        if itemPos % 2 == 0:
            FFX_Xbox.menuRight()
            cursor += 1
        if cursor == itemPos:
            FFX_Xbox.menuB()
        else:
            while cursor != itemPos:
                FFX_Xbox.menuDown()
                cursor += 2
            FFX_Xbox.menuB()

        FFX_Xbox.menuUp()
        FFX_Xbox.menuB()
        FFX_Xbox.menuB()

        return 1

    else:
        print("No restorative items available")
        return 0


def evraeAltana():
    FFX_Logs.writeLog("Fight start: Evrae Altana")    
    steal = 0
    gems = 1
    FFX_Xbox.clickToBattle()
    if FFX_memory.getBattleNum() == 266:
        print("Evrae Altana fight start")
        # Start by hasting Rikku.
        while not FFX_memory.menuOpen(): #AKA end of battle screen
            if FFX_memory.turnReady():
                time.sleep(0.2)
                altanaheal()

    else:  # Just a regular group
        print("Not Evrae this time.")
        fleeAll()
    
    FFX_memory.clickToControl()
    
    #print("Returning value: " + str(gems))
    #return gems

def seymourNatus():
    FFX_Logs.writeLog("Fight start: Seymour Natus")
    fight = 0
    turn = 0
    while not FFX_memory.userControl():
        if FFX_memory.getBattleNum() == 272:  # Seymour Natus
            print("Seymour Natus engaged")
            fight = 1
            while not FFX_memory.menuOpen():
                if FFX_memory.turnReady():
                    if FFX_Screen.turnTidus():
                        swapSlot = FFX_memory.getBattleCharSlot(5)
                        buddySwap_new(swapSlot)
                        FFX_Screen.awaitTurn()
                        FFX_Xbox.weapSwap(0)
                    elif FFX_Screen.turnLulu():
                        swapSlot = FFX_memory.getBattleCharSlot(0)
                        buddySwap_new(swapSlot)
                        FFX_Screen.awaitTurn()
                        attack('none')
                    elif FFX_Screen.turnYuna():
                        aeonSummon(4)
                    elif FFX_Screen.turnAeon():
                        FFX_Xbox.SkipDialog(3) #Finishes the fight.
            return 1
            #if FFX_memory.diagSkipPossible():
            #    FFX_Xbox.menuB()  # In case there's any dialog skipping
        elif FFX_memory.getBattleNum() == 270:  # YAT-63 x2
            fight = 4
            while FFX_memory.battleActive():
                if FFX_memory.turnReady():
                    if FFX_Screen.turnTidus():
                        if turn == 0:
                            turn += 1
                            attack('r3')
                        else:
                            tidusFlee()
                    elif FFX_Screen.turnYuna():
                        attack('r3')
                    elif FFX_Screen.turnAuron():
                        defend()
        elif FFX_memory.getBattleNum() == 269:  # YAT-63 with two guard guys
            fight = 3
            while FFX_memory.battleActive():
                if FFX_memory.turnReady():
                    if FFX_Screen.turnTidus():
                        if turn == 0:
                            turn += 1
                            attack('none')
                        else:
                            tidusFlee()
                    elif FFX_Screen.turnYuna():
                        attack('none')
                    elif FFX_Screen.turnAuron():
                        defend()
        elif FFX_memory.getBattleNum() == 271:  # one YAT-63, two YAT-99
            fight = 2
            while FFX_memory.battleActive():
                if FFX_memory.turnReady():
                    if FFX_Screen.turnTidus():
                        if turn == 0:
                            turn += 1
                            attack('r2')
                        else:
                            tidusFlee()
                    elif FFX_Screen.turnYuna():
                        attack('r2')
                    elif FFX_Screen.turnAuron():
                        defend()
        if FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
            FFXC.set_value('BtnB', 1)
            time.sleep(0.035)
            FFXC.set_value('BtnB', 0)
            time.sleep(0.035)
    return 0

def calmLands(itemSteal):
    FFX_Logs.writeLog("Fight start: Calm Lands")
    steal = 0
    if itemSteal < 2:
        if FFX_Screen.PixelTestTol(1559, 274, (212, 192, 142), 5):  # Red element in center slot, with machina and dog
            print("Grabbing a gem here. This is gem number ", itemSteal + 1)
            tidusHaste('left')
            time.sleep(3)
            FFX_Screen.awaitTurn()
            StealLeft()
            steal += 1
        elif FFX_Screen.PixelTestTol(174, 6, (169, 133, 85), 5):  # Red element in top slot, with bee and tank
            print("Grabbing a gem here. This is gem number ", itemSteal + 1)
            tidusHaste('up')
            time.sleep(3)
            FFX_Screen.awaitTurn()
            StealDown()
            steal += 1
    fleeAll()
    FFX_memory.clickToControl()
    hpPool = FFX_memory.getHP()
    if hpPool[0] != 1520 or hpPool[2] != 1030 or hpPool[3] != 1244:
        healUp(3)
    return steal

def gagazetPath():
    if FFX_memory.getBattleNum() == 337:
        while not FFX_memory.menuOpen():
            if FFX_Screen.BattleScreen():
                if FFX_Screen.turnRikku():
                    StealRight()
                else:
                    escapeOne()
    else:
        fleeAll()

def biranYenke():
    FFX_Logs.writeLog("Fight start: Biran and Yenke")
    FFX_Xbox.clickToBattle()
    Steal()

    FFX_Screen.awaitTurn()
    gemSlot = FFX_memory.getUseItemsSlot(34)
    if gemSlot == 255:
        gemSlot = FFX_memory.getUseItemsSlot(28)
    useItem(gemSlot, 'none')

    FFX_Xbox.clickToBattle()
    gemSlot = FFX_memory.getUseItemsSlot(34)
    if gemSlot == 255:
        gemSlot = FFX_memory.getUseItemsSlot(28)
    useItem(gemSlot, 'none')

    while not FFX_memory.userControl():
        FFXC.set_value('BtnB', 1)
        time.sleep(0.035)
        FFXC.set_value('BtnB', 0)
        time.sleep(0.035)
    
    retSlot = FFX_memory.getItemSlot(96) #Return sphere
    friendSlot = FFX_memory.getItemSlot(97) #Friend sphere
    
    if friendSlot == 255: #Four return sphere method.
        print("Double return sphere drops.")
        endGameVersion = 4
    elif retSlot == 255:
        print("Double friend sphere, effective game over. :( ")
        endGameVersion = 3
    else:
        print("Split items between friend and return spheres.")
        endGameVersion = 1
    
    return endGameVersion
    
def oldEndGameVersionLogic():
    if FFX_Screen.PixelTestTol(341, 315, (156, 197, 207), 5):
        print("Split decision")
        if FFX_Screen.PixelTest(511, 310, (222, 222, 222)):
            print("Friend sphere is first")
            endGameVersion = 1
        else:
            print("Return sphere is first")
            endGameVersion = 2
    elif FFX_Screen.PixelTestTol(502, 240, (222, 222, 222), 5):
        print("Double friend sphere, effective game over. :( ")
        endGameVersion = 3
    else:
        print("Double return sphere.")
        endGameVersion = 4
    return endGameVersion


def seymourFlux():
    stage = 1
    print("Start: Seymour Flux battle")
    FFX_Xbox.clickToBattle()
    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            if FFX_Screen.turnYuna():
                print("Yuna's turn. Stage: ", stage)
                if stage == 1:
                    attack('none')
                    stage += 1
                elif stage == 2:
                    aeonSummon(4)
                    attack('none')
                    stage += 1
                else:
                    attack('none')
            elif FFX_Screen.turnTidus():
                print("Tidus's turn. Stage: ", stage)
                if stage < 3:
                    tidusHaste('down')
                else:
                    attack('none')
            elif FFX_Screen.turnAuron():
                print("Auron's turn. Swap for Rikku and overdrive.")
                buddySwap(1)
                print("Rikku overdrive")
                while not FFX_Screen.PixelTest(306, 683, (223, 223, 223)):
                    FFX_Xbox.menuLeft()
                time.sleep(0.2)
                FFX_Xbox.menuB()
                time.sleep(0.5)
                FFX_memory.rikkuODItems('Flux')

                FFX_Xbox.menuB()  # Engage overdrive
                FFX_Xbox.menuB()  # For safety
            else:
                print("Non-critical turn. Defending.")
                defend()
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
    print("Seymour Flux battle complete.")
    FFX_memory.clickToControl()

def sKeeper():
    if FFX_memory.getBattleNum() == 355:
        print("Start of Sanctuary Keeper fight")
        FFX_Xbox.clickToBattle()
        FFX_Xbox.weapSwap(0)

        FFX_Screen.awaitTurn()
        FFX_Xbox.menuDown()
        FFX_Xbox.menuB()
        time.sleep(0.6)
        FFX_Xbox.menuRight()
        FFX_Xbox.menuB()
        FFX_Xbox.menuB()
        FFX_Xbox.menuB()  # Perform armor break

        FFX_Screen.awaitTurn()
        defend()  # Auron defends
        FFX_Screen.awaitTurn()
        aeonSummon(4)
        FFX_memory.clickToControl()
        return 1
    else:
        fleeLateGame()
        return 0


def gagazetCave(direction):
    FFX_Screen.awaitTurn()
    attack(direction)
    
    fleeAll()

def useItem(slot: int, direction):
    slot -= 1 #This allows us to index at 1 instead of 0 for the programmer's sake.
    FFX_Logs.writeLog("Using items via the Use command")
    print("Using items via the Use command")
    print("Item slot: ", slot)
    print("Direction: ", direction)
    while FFX_memory.battleMenuCursor() != 20:
        if FFX_Screen.turnRikku() == True or FFX_Screen.turnKimahri() == True:
            doNothing = True
        else:
            return
        if FFX_memory.battleMenuCursor() == 255:
            time.sleep(0.01)
        elif FFX_memory.battleMenuCursor() == 1:
            FFX_Xbox.menuUp()
            time.sleep(0.1)
        elif FFX_memory.battleMenuCursor() > 20:
            FFX_Xbox.menuUp()
            time.sleep(0.1)
        else:
            FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    while FFX_memory.battleCursor2() != 1:
        if FFX_memory.battleCursor2() == 0:
            FFX_Xbox.menuRight()
        else:
            FFX_Xbox.menuLeft()
    print("Item slot: ", slot)
    print("Direction: ", direction)
    if slot == 0 and direction == 'none':
        print("Basic method, nothing fancy.")
        FFX_Xbox.SkipDialog(1.5)
    else:
        FFX_Xbox.menuB()
        time.sleep(0.035)
        if slot == 0:
            print("Slot zero")
            time.sleep(0.2)
            FFX_Xbox.menuB()
        else:
            print("Slot (not) zero")
            while FFX_memory.battleCursor3() != slot:
                if FFX_memory.battleCursor3() % 2 != slot % 2:
                    FFX_Xbox.menuRight()
                elif FFX_memory.battleCursor3() < slot:
                    FFX_Xbox.menuDown()
                else:
                    FFX_Xbox.menuUp()
            FFX_Xbox.menuB()
        if direction == 'none':
            print("No direction variation")
            FFX_Xbox.SkipDialog(0.5)
        else:
            print("Direction variation: ", direction)
            time.sleep(0.2)
            if direction == 'left':
                FFX_Xbox.menuLeft()
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()
            elif direction == 'right':
                FFX_Xbox.menuRight()
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()
            elif direction == 'up':
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()
            elif direction == 'down':
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()

def useItem_old(slot, direction):
    FFX_Logs.writeLog("Using items via the Use command")
    print("Using items via the Use command")
    direction = direction.lower()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.4)
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    time.sleep(0.4)
    if slot == 'abPot':
        FFX_Screen.abPotPos(0)
    elif slot == 'lunar':
        if FFX_Screen.PixelTestTol(177, 706, (167, 163, 221), 5):
            print("Lunar in first slot.")
        else:
            print("Lunar in second slot.")
            FFX_Xbox.menuRight()
    else:
        if slot % 2 == 0:
            FFX_Xbox.menuRight()
            slot -= 1
        if slot > 1:
            while slot > 1:
                FFX_Xbox.menuDown()
                slot -= 2
    time.sleep(0.05)
    FFX_Xbox.menuB()

    if direction == 'left':
        FFX_Xbox.menuLeft()
    if direction == 'right':
        FFX_Xbox.menuRight()
    if direction == 'up':
        FFX_Xbox.menuUp()
    if direction == 'down':
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.3)


def cheer():
    FFX_Logs.writeLog("Cheer command")
    print("Cheer command")
    while FFX_memory.battleMenuCursor() != 20:
        if FFX_Screen.turnTidus() == False:
            return
        if FFX_memory.battleMenuCursor() == 0:
            FFX_Xbox.menuDown()
        else:
            FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    while FFX_memory.battleCursor2() != 1:
        if FFX_memory.battleCursor2() == 0:
            FFX_Xbox.menuRight()
        else:
            FFX_Xbox.menuUp()
    FFX_Xbox.SkipDialog(2)


def attack(direction):
    FFX_Logs.writeLog("Basic Attack")
    print("Attack")
    direction = direction.lower()
    if not FFX_memory.turnReady():
        print("Battle menu isn't up.")
        while not FFX_memory.turnReady():
            #Waiting for battle menu to come up.
            time.sleep(0.035)
    if FFX_memory.battleMenuCursor() != 0 and FFX_memory.battleMenuCursor() != 216:
        while FFX_memory.battleMenuCursor() != 0:
            FFX_Xbox.menuUp()
            if FFX_Screen.BattleComplete():
                return
    if direction == 'none':
        print("Diag skipping to success.")
        FFX_Xbox.SkipDialog(0.7)
    else:
        print("Directional pattern.")
        while not FFX_memory.otherBattleMenu():
            FFX_Xbox.menuB()
            if FFX_Screen.BattleComplete():
                return
        time.sleep(0.1)
        if direction == "left":
            FFX_Xbox.menuLeft()
        if direction == "right":
            FFX_Xbox.menuRight()
        if direction == "r2":
            FFX_Xbox.menuRight()
            FFX_Xbox.menuRight()
        if direction == "r3":
            FFX_Xbox.menuRight()
            FFX_Xbox.menuRight()
            FFX_Xbox.menuRight()
        if direction == "up":
            FFX_Xbox.menuUp()
        if direction == "down":
            FFX_Xbox.menuDown()
        FFX_Xbox.menuB()
        FFX_Xbox.menuB()
    time.sleep(0.5)

def attack2():
    FFX_Logs.writeLog("Special Attack")
    print("Special Attack")
    while not FFX_memory.menuOpen():
        FFXC.set_value('BtnB', 1)
        time.sleep(0.035)
        FFXC.set_value('BtnB', 0)
        time.sleep(0.035)

def Steal():
    FFX_Logs.writeLog("Basic Steal command")
    print("Steal")
    if not FFX_memory.turnReady():
        while not FFX_memory.turnReady():
            time.sleep(0.035)
    while FFX_memory.battleMenuCursor() != 20:
        if FFX_Screen.turnRikku() == True or FFX_Screen.turnKimahri() == True:
            doNothing = True
        else:
            return
        if FFX_memory.battleMenuCursor() == 255:
            time.sleep(0.01)
        elif FFX_memory.battleMenuCursor() == 0:
            FFX_Xbox.menuDown()
        else:
            FFX_Xbox.menuUp()
    FFX_Xbox.SkipDialog(1)

def StealDown():
    FFX_Logs.writeLog("Steal, but press Down")
    print("Steal Down")
    while FFX_memory.battleMenuCursor() != 20:
        if FFX_Screen.turnRikku() == True or FFX_Screen.turnKimahri() == True:
            doNothing = True
        else:
            return
        if FFX_memory.battleMenuCursor() == 255:
            time.sleep(0.01)
        elif FFX_memory.battleMenuCursor() == 1:
            FFX_Xbox.menuUp()
        elif FFX_memory.battleMenuCursor() > 20:
            FFX_Xbox.menuUp()
        else:
            FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.4)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuDown()
    FFX_Xbox.SkipDialog(1)

def StealUp():
    FFX_Logs.writeLog("Steal, but press Up")
    print("Steal Down")
    while FFX_memory.battleMenuCursor() != 20:
        if FFX_Screen.turnRikku() == True or FFX_Screen.turnKimahri() == True:
            doNothing = True
        else:
            return
        if FFX_memory.battleMenuCursor() == 255:
            time.sleep(0.01)
        elif FFX_memory.battleMenuCursor() == 1:
            FFX_Xbox.menuUp()
        elif FFX_memory.battleMenuCursor() > 20:
            FFX_Xbox.menuUp()
        else:
            FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.4)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuUp()
    FFX_Xbox.SkipDialog(1)


def StealRight():
    FFX_Logs.writeLog("Steal, but press Right")
    print("Steal Right")
    while FFX_memory.battleMenuCursor() != 20:
        if FFX_Screen.turnRikku() == True or FFX_Screen.turnKimahri() == True:
            doNothing = True
        else:
            return
        if FFX_memory.battleMenuCursor() == 255:
            time.sleep(0.01)
        elif FFX_memory.battleMenuCursor() == 1:
            FFX_Xbox.menuUp()
        elif FFX_memory.battleMenuCursor() > 20:
            FFX_Xbox.menuUp()
        else:
            FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.4)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuRight()
    FFX_Xbox.SkipDialog(1)


def StealLeft():
    FFX_Logs.writeLog("Steal, but press Left")
    print("Steal Left")
    while FFX_memory.battleMenuCursor() != 20:
        if FFX_Screen.turnRikku() == True or FFX_Screen.turnKimahri() == True:
            doNothing = True
        else:
            return
        if FFX_memory.battleMenuCursor() == 255:
            time.sleep(0.01)
        elif FFX_memory.battleMenuCursor() == 1:
            FFX_Xbox.menuUp()
        elif FFX_memory.battleMenuCursor() > 20:
            FFX_Xbox.menuUp()
        else:
            FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.4)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuLeft()
    FFX_Xbox.SkipDialog(1)


def stealAndAttack():
    print("Steal/Attack function")
    BattleComplete = 0
    FFXC.set_neutral()
    while not FFX_memory.menuOpen():
        if FFX_memory.turnReady():
            if FFX_Screen.turnRikku():
                Steal()
            if FFX_Screen.turnTidus():
                attack('none')
        elif FFX_memory.menuOpen():
            FFXC.set_value('BtnB', 1)
            time.sleep(2.5)
            FFXC.set_value('BtnB', 0)
            BattleComplete = 1
        elif FFX_memory.otherBattleMenu():
            FFX_Xbox.menuB()
    FFX_memory.clickToControl()


def stealAndAttackPreTros():
    print("Steal/Attack function before Tros")
    BattleComplete = 0
    turnCounter = 0
    FFXC.set_neutral()
    while not FFX_memory.menuOpen():
        if FFX_memory.turnReady():
            if FFX_Screen.turnRikkuRed():
                turnCounter += 1
                if turnCounter == 1:
                    Steal()
                if turnCounter == 2:
                    StealDown()
                else:
                    attack('none')
            if FFX_Screen.turnTidus():
                attack('none')
        elif FFX_memory.otherBattleMenu():
            FFX_Xbox.menuB()
    FFX_memory.clickToControl()


def valeforFire():
    print("Valefor Fire function")
    BattleComplete = 0
    while BattleComplete == 0:
        if FFX_memory.turnReady():
            print("Valefor casting fire")
            FFX_Xbox.menuDown()
            FFX_Xbox.menuDown()
            FFX_Xbox.menuB()
            FFX_Xbox.menuB()
            FFX_Xbox.menuB()
            FFX_Xbox.menuB()
            FFX_Xbox.menuB()
            FFX_Xbox.menuB()
            FFX_Xbox.menuB()  # Make sure we press the button
        if FFX_Screen.BattleComplete():
            FFXC.set_value('BtnB', 1)
            time.sleep(2.5)
            FFXC.set_value('BtnB', 0)
            BattleComplete = 1


def thunder(direction):
    FFX_Logs.writeLog("Lulu cast Thunder")
    print("Black magic - Thunder")
    if FFX_Screen.turnLulu() == False:
        print("Lulu is not the current person. Deferring turn.")
        return
    direction = direction.lower()
    while FFX_memory.battleMenuCursor() != 21:
        if FFX_memory.battleMenuCursor() == 0:
            FFX_Xbox.menuDown()
        else:
            FFX_Xbox.menuUp()
    FFX_Xbox.menuB()  # Black magic
    while FFX_memory.battleCursor2() != 1:
        if FFX_memory.battleCursor2() % 2 == 0:
            FFX_Xbox.menuRight()
        elif FFX_memory.battleCursor2() > 1:
            FFX_Xbox.menuUp()
        else:
            FFX_Xbox.menuDown()
    FFX_Xbox.menuB()  # Thunder
    if direction == "right":
        FFX_Xbox.menuRight()
    elif direction == "left":
        FFX_Xbox.menuLeft()
    elif direction == "l2":
        FFX_Xbox.menuLeft()
        FFX_Xbox.menuLeft()
    elif direction == "up":
        FFX_Xbox.menuUp()
    elif direction == "down":
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()  # Cast Thunder on Sin's Fin
    FFX_Xbox.menuA()

def fire(direction):
    FFX_Logs.writeLog("Lulu cast Fire")
    print("Black magic - Fire")
    if FFX_Screen.turnLulu() == False:
        print("Lulu is not the current person. Deferring turn.")
        return
    direction = direction.lower()
    while FFX_memory.battleMenuCursor() != 21:
        if FFX_memory.battleMenuCursor() == 0:
            FFX_Xbox.menuDown()
        else:
            FFX_Xbox.menuUp()
    FFX_Xbox.menuB()  # Black magic
    if FFX_memory.battleCursor2() != 0:
        print("Wrong spell targetted")
        while FFX_memory.battleCursor2() != 0:
            if FFX_memory.battleCursor2() % 2 == 1:
                FFX_Xbox.menuLeft()
            elif FFX_memory.battleCursor2() > 0:
                FFX_Xbox.menuUp()
    print("Correct spell targetted.")
    time.sleep(0.5)
    FFX_Xbox.menuB()  # Fire
    if direction == "right":
        FFX_Xbox.menuRight()
    elif direction == "left":
        FFX_Xbox.menuLeft()
    elif direction == "up":
        FFX_Xbox.menuUp()
    elif direction == "down":
        FFX_Xbox.menuDown()
    elif direction == "rd":
        FFX_Xbox.menuRight()
        FFX_Xbox.menuDown()
    time.sleep(0.05)
    FFX_Xbox.menuB()  # Cast Fire
    


def water(direction):
    FFX_Logs.writeLog("Lulu cast Water")
    print("Black magic - Water")
    if FFX_Screen.turnLulu() == False:
        print("Lulu is not the current person. Deferring turn.")
        return
    direction = direction.lower()
    while FFX_memory.battleMenuCursor() != 21:
        if FFX_memory.battleMenuCursor() == 0:
            FFX_Xbox.menuDown()
        else:
            FFX_Xbox.menuUp()
    FFX_Xbox.menuB()  # Black magic
    while FFX_memory.battleCursor2() != 2:
        if FFX_memory.battleCursor2() % 2 == 1:
            FFX_Xbox.menuLeft()
        elif FFX_memory.battleCursor2() > 2:
            FFX_Xbox.menuUp()
        else:
            FFX_Xbox.menuDown()
    FFX_Xbox.menuB()  # Water
    if direction == "right":
        FFX_Xbox.menuRight()
    elif direction == "right2":
        FFX_Xbox.menuRight()
        FFX_Xbox.menuRight()
    elif direction == "left":
        FFX_Xbox.menuLeft()
    elif direction == "up":
        FFX_Xbox.menuUp()
    elif direction == "down":
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()  # Cast Water
    if FFX_Screen.PixelTestTol(800, 709, (133, 133, 133), 5):
        FFX_Xbox.menuA()
        time.sleep(0.5)
        escapeOne()
    else:
        print("Lulu Water")


def ice(direction):
    FFX_Logs.writeLog("Lulu cast Ice")
    print("Black magic - Ice")
    if FFX_Screen.turnLulu() == False:
        print("Lulu is not the current person. Deferring turn.")
        return
    direction = direction.lower()
    while FFX_memory.battleMenuCursor() != 21:
        if FFX_memory.battleMenuCursor() == 0:
            FFX_Xbox.menuDown()
        else:
            FFX_Xbox.menuUp()
    FFX_Xbox.menuB()  # Black magic
    while FFX_memory.battleCursor2() != 3:
        if FFX_memory.battleCursor2() % 2 == 0:
            FFX_Xbox.menuRight()
        elif FFX_memory.battleCursor2() > 3:
            FFX_Xbox.menuUp()
        else:
            FFX_Xbox.menuDown()
    FFX_Xbox.menuB()  # Ice
    if direction == "right":
        FFX_Xbox.menuRight()
    elif direction == "r2":
        FFX_Xbox.menuRight()
        FFX_Xbox.menuRight()
    elif direction == "left":
        FFX_Xbox.menuLeft()
    elif direction == "up":
        FFX_Xbox.menuUp()
    elif direction == "down":
        FFX_Xbox.menuDown()
    elif direction == "d2":
        FFX_Xbox.menuDown()
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()  # Cast Ice
    if FFX_Screen.PixelTestTol(800, 709, (133, 133, 133), 5):
        FFX_Xbox.menuA()
        time.sleep(0.5)
        escapeOne()
    else:
        print("Lulu Ice")


def aeonSummon(position):
    FFX_Logs.writeLog("Aeon is being summoned. " + str(position) + "")
    print("Aeon is being summoned. " + str(position) + "")
    while FFX_memory.battleMenuCursor() != 23:
        if FFX_Screen.turnYuna() == False:
            return
        if FFX_memory.battleMenuCursor() == 255:
            time.sleep(0.01)
        elif FFX_memory.battleMenuCursor() >= 1 and FFX_memory.battleMenuCursor() < 23:
            FFX_Xbox.menuUp()
        else:
            FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    if position == 0:
        FFX_Xbox.SkipDialog(2)
    else:
        time.sleep(0.5)
        if position > 0:
            while position > 0:
                position -= 1
                FFX_Xbox.menuDown()
                # time.sleep(0.05)
        FFX_Xbox.menuB()
        FFX_Xbox.menuB()
        FFX_Xbox.menuB()
        time.sleep(1)
        FFX_Screen.awaitTurn()


def aeonSpell(position):
    FFX_Logs.writeLog("Aeon casting a spell.")
    print("Aeon casting a spell.")
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()  # Black magic
    if position == 0:
        FFX_Xbox.SkipDialog(1.3)
    else:
        time.sleep(0.4)
        if position == 1:
            FFX_Xbox.menuRight()
        elif position == 2:
            FFX_Xbox.menuDown()
        elif position == 3:
            FFX_Xbox.menuRight()
            FFX_Xbox.menuDown()
        FFX_Xbox.menuB()  # Cast whatever spell is chosen
        FFX_Xbox.menuB()  # Cast whatever spell is chosen
        FFX_Xbox.menuB()  # Cast whatever spell is chosen
        FFX_Xbox.menuB()  # Cast whatever spell is chosen
    time.sleep(0.2)


def aeonSpell2(position, direction):
    FFX_Logs.writeLog("Aeon casting a spell.")
    print("Aeon casting a spell. (2)")
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()  # Black magic
    time.sleep(0.4)
    if position == 1:
        FFX_Xbox.menuRight()
    elif position == 2:
        FFX_Xbox.menuDown()
    elif position == 3:
        FFX_Xbox.menuRight()
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()  # Cast whatever spell is chosen
    time.sleep(0.1)
    if direction == 'right':
        FFX_Xbox.menuRight()
    if direction == 'left':
        FFX_Xbox.menuLeft()
    if direction == 'up':
        FFX_Xbox.menuUp()
    if direction == 'down':
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()  # Cast whatever spell is chosen
    FFX_Xbox.menuB()  # Cast whatever spell is chosen
    FFX_Xbox.menuB()  # Cast whatever spell is chosen
    print("Aeon casting spell")
    time.sleep(0.2)


def aeonSpellDirection(position, direction):
    FFX_Logs.writeLog("Aeon casting a spell. Special direction: " + str(direction))
    print("Aeon casting a spell. Special direction: ", direction)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()  # Black magic
    time.sleep(0.4)
    if position == 1:
        FFX_Xbox.menuRight()
    elif position == 2:
        FFX_Xbox.menuDown()
    elif position == 3:
        FFX_Xbox.menuRight()
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()  # Cast whatever spell is chosen
    time.sleep(0.2)
    if direction == 'left':
        FFX_Xbox.menuLeft()
    if direction == 'right':
        FFX_Xbox.menuRight()
    if direction == 'up':
        FFX_Xbox.menuUp()
    if direction == 'down':
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()  # Cast whatever spell is chosen
    FFX_Xbox.menuB()  # Cast whatever spell is chosen
    FFX_Xbox.menuB()  # Cast whatever spell is chosen
    print("Aeon casting spell")
    time.sleep(0.2)

def healUp_New(chars, menusize):
    FFX_Logs.writeLog("Healing characters post-battle")
    print("Menuing, healing characters: ", chars)
    FFXC.set_neutral()
    if not FFX_memory.menuOpen():
        FFX_memory.openMenu()

    currentmenuposition = FFX_memory.getMenuCursorPos()

    targetmenuposition = 2
    menudistance = abs(targetmenuposition - currentmenuposition)

    if menudistance < (menusize / 2 - 1):
        for i in range(menudistance):
            if targetmenuposition > currentmenuposition:
                FFX_Xbox.menuDown()
            else:
                FFX_Xbox.menuUp()
    else:
        for i in range(menusize - menudistance):
            if targetmenuposition > currentmenuposition:
                FFX_Xbox.menuUp()
            else:
                FFX_Xbox.menuDown()

    FFX_Xbox.menuB()
    time.sleep(0.2)

    for i in range(len(FFX_memory.getOrderSeven())):
        currentcharpos = FFX_memory.getCharCursorPos()
        print("Cursor Pos: %d" % currentcharpos)
        print("Character Index: %d" % FFX_memory.getOrderSeven()[currentcharpos])
        if FFX_memory.getOrderSeven()[currentcharpos] == 1:
            break
        FFX_Xbox.menuDown()
    time.sleep(0.2)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuB()
    pos = 1
    time.sleep(0.2)
    FFX_Xbox.menuB()
    while pos < chars:
        pos += 1
        FFX_Xbox.menuDown()
        FFX_Xbox.menuB()
    print("Healing complete. Exiting menu.")
    FFX_memory.closeMenu()


def healUp(chars):
    FFX_Logs.writeLog("Healing characters post-battle")
    FFXC.set_neutral()
    print("Menuing, healing characters: ", chars)
    if not FFX_memory.menuOpen():
        FFX_memory.openMenu()
    pos = 1
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    print("Mark 1")
    yunaPos = FFX_memory.getCharFormationSlot(1)
    order = FFX_memory.getOrderSeven()
    partyMembers = len(order)
    if FFX_memory.getCharCursorPos() != yunaPos:
        while FFX_memory.getCharCursorPos() != yunaPos:
            FFX_memory.menuDirection(FFX_memory.getCharCursorPos(), yunaPos, partyMembers)
    print("Mark 2")
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuB()
    while pos < chars:
        pos += 1
        FFX_Xbox.menuDown()
        FFX_Xbox.menuB()
    print("Healing complete. Exiting menu.")
    FFX_memory.closeMenu()

def healUp2(chars):
    FFX_Logs.writeLog("Healing characters post-battle")
    print("Menuing, healing characters: ", chars)
    if not FFX_memory.menuOpen():
        FFX_memory.openMenu()
    pos = 1
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuB()
    while pos < chars:
        pos += 1
        FFX_Xbox.menuDown()
        FFX_Xbox.menuB()
    print("Healing complete. Exiting menu.")
    FFX_memory.closeMenu()

def healUpNoCombat(chars):
    FFX_Logs.writeLog("Healing characters post-battle")
    print("Menuing, healing characters: ", chars)
    if FFX_memory.menuOpen() and FFX_memory.userControl() == False:
        FFX_memory.clickToControl() # After-battle screen is still open.
    FFX_memory.openMenu()
    pos = 1
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    if chars <= 7:
        FFX_Xbox.menuUp()
    else:
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuB()
    while pos < chars:
        pos += 1
        FFX_Xbox.menuDown()
        FFX_Xbox.menuB()
    print("Healing complete. Exiting menu.")
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()


def lancetSwap(direction):
    print("Lancet Swap function")
    # Assumption is formation: Tidus, Wakka, Auron, Kimahri, and Yuna in last slot.
    direction = direction.lower()
    buddySwapKimahri()

    while FFX_memory.battleMenuCursor() != 20:
        if FFX_memory.battleMenuCursor() == 255:
            time.sleep(0.01)
        elif FFX_memory.battleMenuCursor() == 1:
            FFX_Xbox.menuUp()
        elif FFX_memory.battleMenuCursor() > 20:
            FFX_Xbox.menuUp()
        else:
            FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    if direction == 'none':
        FFX_Xbox.SkipDialog(2)
    else:
        time.sleep(0.5)
        FFX_Xbox.menuB()
        time.sleep(0.05)
        if direction == 'left':
            FFX_Xbox.menuLeft()
        if direction == 'right':
            FFX_Xbox.menuRight()
        if direction == 'up':
            FFX_Xbox.menuUp()
        if direction == 'down':
            FFX_Xbox.menuDown()
        FFX_Xbox.menuB()
    swapPos = 0
    FFX_Screen.awaitTurn()
    if FFX_Screen.turnWakka():
        swapPos = 2
    elif FFX_Screen.turnAuron():
        swapPos = 3
    buddySwapTidus()
    tidusFlee()
    #FFX_Xbox.clickToBattle()  # Just to get to the battle summary scene
    FFX_memory.clickToControl()

def lancetSwapDjose(direction):
    print("Lancet Swap function - Djose")
    # Assumption is formation: Tidus, Wakka, Auron, Kimahri, and Yuna in last slot.
    direction = direction.lower()
    buddySwapKimahri()

    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.6)
    FFX_Xbox.menuB()
    time.sleep(0.05)
    if direction == 'left':
        FFX_Xbox.menuLeft()
    if direction == 'right':
        FFX_Xbox.menuRight()
    if direction == 'up':
        FFX_Xbox.menuUp()
    if direction == 'down':
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    
    print("Lancet complete.")
    FFX_Screen.awaitTurn()
    print("Swapping in Tidus")
    buddySwapTidus()
    print("Tidus is in.")
    FFX_Screen.awaitTurn()
    print("Tidus use Flee")
    tidusFlee()
    print("Flee complete")
    FFX_memory.clickToControl()

    # Now to recover the formation
    FFX_memory.fullPartyFormat_New('djose', 10)
    print("Mark!")
    FFX_memory.closeMenu()
    print("Done with reformatting via Lancet Swap function.")

def lancet(direction):
    print("Casting Lancet with variation: ", direction)
    while FFX_memory.battleMenuCursor() != 20:
        if FFX_memory.battleMenuCursor() == 255:
            time.sleep(0.01)
        elif FFX_memory.battleMenuCursor() == 1:
            FFX_Xbox.menuUp()
        elif FFX_memory.battleMenuCursor() > 20:
            FFX_Xbox.menuUp()
        else:
            FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.3)
    FFX_Xbox.menuB()
    time.sleep(0.3)
    if direction == 'left':
        FFX_Xbox.menuLeft()
    if direction == 'right':
        FFX_Xbox.menuRight()
    if direction == 'up':
        FFX_Xbox.menuUp()
    if direction == 'down':
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(1) #To make sure we don't overlap turns


def lancetHome(direction):
    print("Lancet (home) function")
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.4)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.3)
    if direction == 'left':
        FFX_Xbox.menuLeft()
    if direction == 'right':
        FFX_Xbox.menuRight()
    if direction == 'up':
        FFX_Xbox.menuUp()
    if direction == 'down':
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(1) #To make sure we don't overlap turns

def fleeAll():
    FFX_Logs.writeLog("Fleeing from battle, prior to Mt Gagazet")
    print("Attempting escape (all party members and end screen)")
    while not FFX_memory.menuOpen():
        if FFX_memory.turnReady():
            if FFX_Screen.turnTidus():
                tidusFlee()
            else:
                while FFX_memory.mainBattleMenu():
                    FFX_Xbox.menuRight()
                while FFX_memory.battleCursor2() != 2:
                    FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()
            time.sleep(0.1)

def fleeLateGame():
    FFX_Logs.writeLog("Fleeing from battle, Gagazet and beyond")
    print("Attempting escape (all party members and end screen)")
    BattleComplete = 0
    while BattleComplete == 0:
        if FFX_memory.turnReady():
            if FFX_Screen.turnTidus():
                while FFX_memory.battleMenuCursor() != 20:
                    if FFX_memory.battleMenuCursor() == 255:
                        time.sleep(0.01)
                    elif FFX_memory.battleMenuCursor() == 1:
                        FFX_Xbox.menuUp()
                    elif FFX_memory.battleMenuCursor() > 20:
                        FFX_Xbox.menuUp()
                    else:
                        FFX_Xbox.menuDown()
                FFX_Xbox.SkipDialog(1.5)
            else:
                escapeOne()
        time.sleep(0.4)
        if FFX_Screen.BattleComplete():
            FFXC.set_value('BtnB', 1)
            time.sleep(1.8)
            FFXC.set_value('BtnB', 0)
            BattleComplete = 1

def escapeAll():
    print("escapeAll function")
    while not FFX_Screen.BattleComplete():
        if FFX_memory.turnReady():
            escapeOne()

def escapeOne():
    FFX_Logs.writeLog("Character attempting escape")
    print("Attempting escape, one person")
    while FFX_memory.mainBattleMenu():
        FFX_Xbox.menuRight()
    while FFX_memory.battleCursor2() != 2:
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()

def buddySwap(position):
    FFX_Logs.writeLog("Swapping characters (in battle)")
    print("Swapping characters (in battle)")
    while not FFX_Screen.PixelTestTol(324, 92, (223, 223, 223), 5):
        FFX_Xbox.lBumper()
    time.sleep(0.7)
    if position == 1:
        print(position)
    elif position == 0:  # Swap with last slot
        print(position)
        FFX_Xbox.menuUp()
    elif position == 2:
        FFX_Xbox.menuDown()
        print(position)
    elif position == 3:
        print(position)
        FFX_Xbox.menuDown()
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.6)
    FFX_Xbox.clickToBattle()
    FFX_Screen.awaitTurn()


def buddySwap_new(position):
    FFX_Logs.writeLog("Swapping characters (in battle)")
    print("Swapping characters (in battle) - 2")
    while not FFX_Screen.PixelTestTol(324, 92, (223, 223, 223), 5):
        FFX_Xbox.lBumper()
    time.sleep(0.7)
    reserveposition = (position - 3) % 4
    if reserveposition == 1:
        print(position)
    elif reserveposition == 0:  # Swap with last slot
        print(position)
        FFX_Xbox.menuUp()
    elif reserveposition == 2:
        FFX_Xbox.menuDown()
        print(position)
    elif reserveposition == 3:
        print(position)
        FFX_Xbox.menuDown()
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.6)
    FFX_Xbox.clickToBattle()
    FFX_Screen.awaitTurn()

def buddySwapTidus():
    FFX_Logs.writeLog("Swapping characters (in battle)")
    print("Swapping in Tidus for current character")
    while not FFX_Screen.PixelTestTol(324, 92, (223, 223, 223), 5):
        FFX_Xbox.lBumper()
    time.sleep(0.6)
    if FFX_Screen.PixelTestTol(197, 231, (244, 202, 146), 5):
        print("Tidus in slot 1")
    elif FFX_Screen.PixelTestTol(197, 325, (246, 203, 146), 5):
        print("Tidus in slot 2")
        FFX_Xbox.menuDown()
    elif FFX_Screen.PixelTestTol(197, 423, (244, 201, 146), 5):
        print("Tidus in slot 3")
        FFX_Xbox.menuDown()
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.3)
    FFX_Screen.awaitTurn()

def buddySwapKimahri():
    FFX_Logs.writeLog("Swapping characters (in battle)")
    print("Swapping in Kimahri for current character")
    while not FFX_Screen.PixelTestTol(324, 92, (223, 223, 223), 5):
        FFX_Xbox.lBumper()
    time.sleep(0.6)
    if FFX_Screen.PixelTestTol(215, 227, (163, 0, 16), 5):
        print("Kimahri in slot 1")
    elif FFX_Screen.PixelTestTol(217, 321, (162, 0, 16), 5):
        print("Kimahri in slot 2")
        FFX_Xbox.menuDown()
    elif FFX_Screen.PixelTestTol(218, 417, (160, 0, 16), 5):
        print("Kimahri in slot 3")
        FFX_Xbox.menuDown()
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.3)
    FFX_Screen.awaitTurn()

def buddySwapAuron():
    FFX_Logs.writeLog("Swapping characters (in battle)")
    print("Swapping in Auron for current character")
    while not FFX_Screen.PixelTestTol(324, 92, (223, 223, 223), 5):
        FFX_Xbox.lBumper()
    time.sleep(0.6)
    if FFX_Screen.PixelTestTol(197, 231, (136, 87, 53), 5):
        print("Auron in slot 1")
    elif FFX_Screen.PixelTestTol(197, 325, (108, 65, 37), 5):
        print("Auron in slot 2")
        FFX_Xbox.menuDown()
    elif FFX_Screen.PixelTestTol(197, 423, (233, 191, 141), 5):
        print("Auron in slot 3")
        FFX_Xbox.menuDown()
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.3)
    FFX_Screen.awaitTurn()

def kimahriOD(pos):
    FFX_Logs.writeLog("Kimahri using Overdrive")
    print("Kimahri using Overdrive")
    while not FFX_Screen.PixelTest(357, 704, (171, 171, 171)):
        FFX_Xbox.menuLeft()
    time.sleep(0.3)
    FFX_Xbox.menuB()
    time.sleep(0.3)

    if pos % 2 == 0:
        FFX_Xbox.menuRight()
        pos -= 1
    if pos > 1:
        while pos > 1:
            FFX_Xbox.menuDown()
            pos -= 2
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()

def wrapUp():
    while not FFX_memory.userControl():
        if FFX_memory.menuOpen():
            FFX_Xbox.tapB()
        elif FFX_memory.turnReady():
            return False
    return True

def SinArms():
    FFX_Logs.writeLog("Fight start: Sin's Arms")
    print("Fight start: Sin's Arms")
    # Area for improvement later. Multiple skippable FMVs
    FFX_Xbox.clickToBattle()
    aeonSummon(4)
    
    FFX_Screen.awaitTurn()
    time.sleep(0.07)
    FFX_Xbox.menuDown()
    FFX_Xbox.SkipDialog(2)

    while FFX_memory.battleActive(): #Arm1
        if FFX_memory.turnReady():
            FFX_Xbox.menuDown()
            FFX_Xbox.SkipDialog(2)
        else:
            FFX_Xbox.menuB()
    
    FFX_Xbox.SkipDialog(0.3)
    while not FFX_memory.battleActive():
        if FFX_memory.cutsceneSkipPossible():
            FFX_Xbox.skipScene()
        elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
    
    FFX_Xbox.clickToBattle()
    aeonSummon(4)

    while not FFX_memory.battleComplete(): #Arm2
        if FFX_memory.turnReady():
            FFX_Xbox.menuDown()
            FFX_Xbox.SkipDialog(2)
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()

    FFX_Xbox.SkipDialog(0.3)
    while not FFX_memory.battleActive():
        if FFX_memory.cutsceneSkipPossible():
            FFX_Xbox.skipScene()
        elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()

    FFX_Xbox.clickToBattle() #Start of Sin Core
    aeonSummon(4)
    FFX_Screen.awaitTurn()
    time.sleep(1)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuB()  # Impulse on Core
    
    while not FFX_memory.userControl():
        if FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
            FFX_Xbox.tapB()
        elif FFX_memory.cutsceneSkipPossible():
            FFX_Xbox.skipScene()
    print("Done with Sin's Arms section")

def SinFace():
    FFX_Logs.writeLog("Fight start: Sin's Face")
    print("Fight start: Sin's Face")
    FFX_Xbox.clickToBattle()
    FFXC.set_neutral()
    
    complete = 0
    while complete == 0:
        if FFX_memory.turnReady():
            if FFX_Screen.turnYuna():
                aeonSummon(4)
                FFX_Screen.awaitTurn()
                time.sleep(1)
                FFX_Xbox.menuDown()
                FFX_Xbox.SkipDialog(2)
            elif FFX_Screen.turnAeon():
                attack('none')
            else:
                defend()
        elif FFX_memory.getStoryProgress() == 3160:
            time.sleep(0.5)
            FFX_Xbox.skipScene()
            complete = 1
        else:
            FFX_Xbox.menuB()

def omnis():
    FFX_Logs.writeLog("Fight start: Seymour Omnis")
    print("Fight start: Seymour Omnis")
    FFX_Xbox.clickToBattle()
    #if seed == 31:
    #    attack('none')
    #else:
    #    defend()
    defend()

    FFX_Screen.awaitTurn()
    print("Going for armor break.")
    FFX_memory.printRNG36()
    useSkill(1)
    time.sleep(0.2)
    FFX_Screen.awaitTurn()
    
    if FFX_memory.getEnemyMaxHP()[0] == FFX_memory.getEnemyCurrentHP()[0]:
        print("Missing on armor break is stupid. Don't worry, I can 'fix' this.")
        FFX_memory.setEnemyCurrentHP(0,20)
    print("Ready for next step.")
    while not FFX_memory.battleComplete(): #AKA end of battle screen
        if FFX_memory.turnReady():
            print("Character turn: ",FFX_memory.getBattleCharTurn())
            if FFX_Screen.turnYuna():
                aeonSummon(4)
            elif FFX_Screen.turnAeon():
                attack('none')
            else:
                defend()
        elif FFX_memory.diagSkipPossible():
            print("Skipping dialog maybe?")
            FFX_Xbox.menuB()
    print("Should be done now.")
    FFX_memory.clickToControl()

def BFA():
    FFXC.set_movement(1, 0)
    time.sleep(0.4)
    FFXC.set_movement(1, 1)
    time.sleep(3)
    FFXC.set_neutral()
    
    FFX_Logs.writeLog("Fight start: BFA and final boss")
    FFX_Xbox.clickToBattle()
    buddySwap(2)
    useSkill(0)

    FFX_Screen.awaitTurn()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuLeft()
    time.sleep(0.8)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()

    FFX_Xbox.clickToBattle()
    buddySwap(2)
    aeonSummon(4)
    
    #Bahamut finishes the battle.
    while FFX_memory.battleActive():
        FFX_Xbox.tapB()

    #Skip the cutscene
    print("BFA down. Ready for Aeons")
    time.sleep(0.07)
    while not FFX_memory.cutsceneSkipPossible():
        FFX_Xbox.tapB()
    FFX_Xbox.skipScene()

    while FFX_memory.getStoryProgress() < 3380:
        if FFX_memory.turnReady():
            battleNum = FFX_memory.getBattleNum()
            print("Battle engaged. Battle number: ", battleNum)
            while FFX_memory.battleMenuCursor() != 20:
                if FFX_memory.battleMenuCursor() == 22 or FFX_memory.battleMenuCursor() == 1:
                    FFX_Xbox.menuUp()
                else:
                    FFX_Xbox.menuDown()
            FFX_Xbox.menuB()
            time.sleep(0.4)
            FFX_Xbox.menuB()
            time.sleep(0.4)
            FFX_Xbox.menuLeft()
            FFX_Xbox.menuLeft()
            FFX_Xbox.menuLeft()
            FFX_Xbox.menuLeft()
            FFX_Xbox.menuUp()
            FFX_Xbox.menuUp()
            # Valefor is 20k, no extra money needed. Valefor is 397
            if battleNum == 398 or battleNum == 399:  # Ifrit/Ixion
                FFX_Xbox.menuUp()
            elif battleNum == 400 or battleNum == 401:  # Shiva/Bahamut
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
            FFX_Xbox.menuB()
            FFX_Xbox.menuB()
            time.sleep(0.5)
        elif FFX_memory.battleActive() == False:
            FFXC.set_value('BtnB', 1)
            time.sleep(0.035)
            FFXC.set_value('BtnB', 0)
            time.sleep(0.035)
    print("Ready for Yu Yevon.")
    FFX_Screen.awaitTurn()  # No need for skipping dialog
    print("Awww such a sad final boss!")

    zombieAttack = 0
    story = FFX_memory.getStoryProgress()
    while story < 3400:
        if FFX_memory.turnReady():
            if zombieAttack == 1:
                while FFX_memory.battleMenuCursor() != 1:
                    FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                itemPos = FFX_memory.getThrowItemsSlot(6) - 1
                while FFX_memory.battleCursor2() != itemPos:
                    print(FFX_memory.battleCursor2()," | ", itemPos)
                    if FFX_memory.battleCursor2() == 0:
                        FFX_Xbox.menuDown()
                    elif itemPos % 2 == 0 and FFX_memory.battleCursor2() % 2 == 1:
                        FFX_Xbox.menuRight()
                    elif itemPos % 2 == 1 and FFX_memory.battleCursor2() % 2 == 0:
                        FFX_Xbox.menuLeft()
                    elif itemPos > FFX_memory.battleCursor2():
                        FFX_Xbox.menuDown()
                    else:
                        FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
                time.sleep(0.035)
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
                print("Phoenix Down on Yu Yevon. Good game.")
            elif FFX_Screen.turnTidus():
                useSkill(0)
                zombieAttack = 1
            else:
                defend()
        elif FFX_memory.battleActive() == False:
            FFXC.set_value('BtnB', 1)
            time.sleep(0.035)
            FFXC.set_value('BtnB', 0)
            time.sleep(0.035)
        story = FFX_memory.getStoryProgress()

def BFA_TASonly_unused():
    FFX_Logs.writeLog("Fight start: BFA and final boss")
    FFX_Xbox.clickToBattle()
    FFX_Xbox.menuDown()
    useItem(4, 'none')

    # Clear out the pagodas
    FFX_Xbox.clickToBattle()
    buddySwap(0)
    time.sleep(0.5)
    FFX_Xbox.menuLeft()
    time.sleep(1)
    FFX_Xbox.menuB()

    # Trio of Rikku's Broken Overdrive
    time.sleep(1)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuRight()
    FFX_Xbox.SkipDialog(3)

    # Then Tidus talk so we get a free Jecht turn
    FFX_Xbox.clickToBattle()
    time.sleep(0.5)
    FFX_Xbox.menuLeft()
    time.sleep(1)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.SkipDialog(2)

    while FFX_memory.getBattleNum() < 397:
        if FFX_Screen.BattleScreen():
            if FFX_Screen.turnYuna():
                defend()
            else:
                if FFX_Screen.turnTidus():
                    FFX_Xbox.menuDown()
                useItem(3, 'none')
        else:
            FFX_Xbox.menuB()

    # Yu Yevon
    story = FFX_memory.getStoryProgress()
    while story < 3400:
        if FFX_Screen.BattleScreen():
            if FFX_Screen.turnTidus():
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                time.sleep(0.5)
                FFX_Xbox.menuB()
                time.sleep(0.5)
                FFX_Xbox.menuB()
                time.sleep(0.5)  # Zombiestrike
                FFX_Xbox.menuB()
                time.sleep(0.5)
            else:
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                time.sleep(0.5)
                FFX_Xbox.menuB()  # Phoenix Down
                time.sleep(0.5)
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()  # Target Yu Yevon
                time.sleep(0.5)
        story = FFX_memory.getStoryProgress()


def oldYYTasLogic():
    # Yu Yevon
    story = FFX_memory.getStoryProgress()
    while story < 3400:
        if FFX_memory.turnReady():
            if FFX_Screen.turnTidus():
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                time.sleep(0.5)
                FFX_Xbox.menuB()
                time.sleep(0.5)
                FFX_Xbox.menuB()
                time.sleep(0.5)  # Zombiestrike
                FFX_Xbox.menuB()
                time.sleep(0.5)
            else:
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                time.sleep(0.5)
                FFX_Xbox.menuB()  # Phoenix Down
                time.sleep(0.5)
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()  # Target Yu Yevon
                time.sleep(0.5)
        story = FFX_memory.getStoryProgress()

def checkPetrify():
    iterVar = 0
    petrifiedstate = False
    for iterVar in range(7):
        if FFX_memory.petrifiedstate(iterVar):
            petrifiedstate = True
    return petrifiedstate
    
def checkPetrifyTidus():
    petrifiedstate = False
    if FFX_memory.petrifiedstate(0):
        petrifiedstate = True
    return petrifiedstate
    
def mrrFormat_unused():
    FFX_Logs.writeLog("Reformatting party")
    openMenu()
    time.sleep(0.2)
    if checkMRRForm() == 0:
        order = FFX_memory.getOrderSix()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuB()
        
        if order[0] != 0: #Tidus is not in the first slot
            print("Looking for Tidus")
            if order[1] == 0:
                print("Tidus in Second slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[1] = order[0]
                order[0] = 0
            elif order[2] == 0:
                print("Tidus in Third slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                order[2] = order[0]
                order[0] = 0
            elif order[3] == 0:
                print("Tidus in Fourth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                order[3] = order[0]
                order[0] = 0
            elif order[4] == 0:
                print("Tidus in Fifth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                order[4] = order[0]
                order[0] = 0
            elif order[5] == 0:
                print("Tidus in Sixth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                order[5] = order[0]
                order[0] = 0
        else:
            print("Tidus seems fine.")
            FFX_Xbox.menuDown()
        if order[1] != 4: #Wakka is not in the second slot
            print("Looking for Wakka")
            if order[2] == 4:
                print("Wakka in Third slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[2] = order[1]
                order[1] = 4
            elif order[3] == 4:
                print("Wakkain Fourth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                order[3] = order[1]
                order[1] = 4
            elif order[4] == 4:
                print("Wakka in Fifth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                order[4] = order[1]
                order[1] = 4
            elif order[5] == 4:
                print("Wakka in Sixth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                order[5] = order[1]
                order[1] = 4
        else:
            print("Wakka seems fine.")
            FFX_Xbox.menuDown()
        if order[2] != 2: #Auron, 3rd slot
            print("Looking for Auron")
            if order[3] == 2:
                print("Auron in fourth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[3] = order[2]
                order[2] = 2
            elif order[4] == 2:
                print("Auron in fifth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                order[4] = order[2]
                order[2] = 2
            elif order[5] == 2:
                print("Auron in sixth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                order[5] = order[2]
                order[2] = 2
            else:
                print("Something's wrong, can't find Lulu.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
        else:
            print("Auron seems fine.")
            FFX_Xbox.menuDown()
        if order[3] != 5: #Lulu, 4th slot
            print("Looking for Lulu")
            if order[4] == 5:
                print("Lulu in fifth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[4] = order[3]
                order[3] = 5
            elif order[5] == 5:
                print("Lulu in sixth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                order[5] = order[3]
                order[3] = 5
        else:
            print("Lulu seems fine.")
            FFX_Xbox.menuDown()
        if order[4] != 3: #Kimahri, 5th slot
            print("Swapping 5th and 6th slots")
            FFX_Xbox.menuB()
            FFX_Xbox.menuDown()
            FFX_Xbox.menuB()
            order[5] = order[4]
            order[4] = 3
        else:
            print("Lulu and Yuna seem fine.")
            
        
        FFX_Xbox.menuA()
        FFX_Xbox.menuDown()
        FFX_Xbox.menuDown()
        FFX_Xbox.menuDown()
    return checkMRRForm()

def checkMRRForm_unused():
    success = 1
    order = FFX_memory.getOrderSix()
    if order[0] != 0:
        print("Tidus is NOT first")
        success = 0
    else:
        print("Tidus is first")
    if order[1] != 4:
        print("Wakka is NOT second")
        success = 0
    else:
        print("Wakka is second")
    if order[2] != 2:
        print("Auron is not third.")
        success = 0
    else:
        print("Auron is third")
    if order[3] != 5:
        print("Lulu is not fourth.")
        success = 0
    else:
        print("Lulu is fourth")
    if order[4] != 3:
        print("Kimahri is not fifth.")
        success = 0
    else:
        print("Kimahri is fifth")
    if order[5] != 1:
        print("Yuna is not last.")
        success = 0
    else:
        print("Yuna is last")
    return success

#def clickToBattle():
#    FFX_Logs.writeLog("Clicking until it's someone's turn in battle")
#    print("Clicking until it's someone's turn in battle")
#    FFXC.set_neutral()
#    complete = 0
#    while complete == 0 :
#        if FFX_Screen.BattleScreen() or FFX_memory.userControl():
#            complete = 1
#        elif FFX_memory.battleActive() == False:
#            FFX_Xbox.menuB()
#        elif FFX_memory.diagSkipPossible():
#            FFX_Xbox.menuB()
