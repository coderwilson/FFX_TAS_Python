import FFX_Xbox
import FFX_Screen
import time
import FFX_Logs
import FFX_memory

FFXC = FFX_Xbox.FFXC


def defend():
    FFXC.set_value('BtnY', 1)
    time.sleep(0.035)
    FFXC.set_value('BtnY', 0)
    time.sleep(0.035)
    FFXC.set_value('BtnY', 1)
    time.sleep(0.035)
    FFXC.set_value('BtnY', 0)
    time.sleep(0.035)
    print("Defend command")
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    time.sleep(0.8)


def tidusFlee():
    print("Tidus Flee (or similar command pattern)")
    while FFX_memory.battleMenuCursor() != 20:
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
    FFX_Xbox.SkipDialog(1.5)

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
        if FFX_memory.battleScreen():
            return
        elif FFX_Screen.BattleComplete():
            return
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
    while FFX_memory.battleScreen():
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
        if FFX_memory.battleScreen():
            return
        elif FFX_Screen.BattleComplete():
            return
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
    while FFX_memory.battleMenuCursor() != 1:
        FFX_Xbox.menuDown()
    FFX_Xbox.menuB()  # Item menu open.
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
    BattleComplete = 0
    countAttacks = 0
    countRevives = 0

    while BattleComplete == 0:
        if FFX_memory.battleScreen():
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

    while BattleComplete == 0:
        if FFX_memory.battleScreen():
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
            FFX_Logs.writeStats("Sinspawn Ammes. Attacks:")
            FFX_Logs.writeStats(str(countAttacks))


def Tanker():
    FFX_Logs.writeLog("Fight start: Tanker")
    BattleComplete = 0
    countAttacks = 0
    countRevives = 0
    tidusCount = 0
    auronCount = 0
    FFX_Screen.clickToBattle()

    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
            if FFX_Screen.turnTidus():
                tidusCount += 1
                if tidusCount < 4:
                    FFX_Xbox.weapSwap(0)
                    time.sleep(0.5)
                else:
                    attack('none')
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
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
    while not FFX_memory.userControl():
        #print("Skip cutscene")
        FFXC.set_value('BtnX', 1)
        FFXC.set_value('BtnB', 1)
        time.sleep(0.035)
        FFXC.set_value('BtnX', 0)
        FFXC.set_value('BtnB', 0)
        time.sleep(0.035)
    FFX_Logs.writeStats("Tanker. Attacks:")
    FFX_Logs.writeStats(str(countAttacks))

def Klikk():
    rikkuSteal = 0
    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
            BattleHP = FFX_memory.getBattleHP()
            if BattleHP[1] == 0 or BattleHP[2] == 0:
                revive()
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
                else:
                    attack('none')
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
                else:
                    attack('none')
        else:
            FFX_Xbox.menuB()
    print("Klikk fight complete")
    FFX_memory.clickToControl()  # Maybe not skippable dialog, but whatever.


def Tros():
    FFX_Logs.writeLog("Fight start: Tros")
    BattleComplete = 0
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    battleClock = 0
    countAttacks = 0
    countRevives = 0
    countGrenades = 0
    countSteals = 0
    countDefends = 0
    countHeals = 0

    while BattleComplete == 0:
        if FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
        elif FFX_memory.otherBattleMenu():
            FFX_Xbox.menuA()
        elif FFX_memory.battleScreen():
            battleClock += 1
            print("Battle clock:", battleClock)
            trosPos = 2
            print("Determining Tros position")
            while trosPos == 2:  # Two for "not yet determined".
                camera = FFX_memory.getCamera()
                # First, determine position of Tros
                if camera[0] > 2:
                    trosPos = 0  # Zero for cannot attack.
                    print("Tros is long-range. Cannot attack.")
                elif camera[0] < -2:
                    trosPos = 0  # Zero for cannot attack.
                    print("Tros is long-range. Cannot attack.")
                else:
                    trosPos = 1  # One for "Close range, can be attacked.
                    print("Tros is short-range.")

            partyHP = FFX_memory.getBattleHP()
            if partyHP[1] == 0 or partyHP[2] == 0:  # Someone requires reviving.
                print("Tros: Someone fainted.")
                revive()
            elif FFX_Screen.turnRikkuRed():
                if battleClock < 3:
                    grenadeSlot = FFX_memory.getUseItemsSlot(35)
                    if FFX_memory.getItemCountSlot(grenadeSlot) < 6:
                        print("Rikku's first turn. Steal.")
                        Steal()
                        time.sleep(0.5)
                    else:
                        print("Already have enough grenades. Hopping to it.")
                        FFX_Xbox.menuDown()
                        FFX_Xbox.menuB()
                        time.sleep(0.4)
                        FFX_Xbox.menuRight()
                        FFX_Xbox.SkipDialog(2)
                else:
                    FFX_Xbox.menuDown()
                    FFX_Xbox.menuB()
                    time.sleep(0.4)
                    FFX_Xbox.menuRight()
                    FFX_Xbox.menuB()
                    time.sleep(0.4)
                    if FFX_Screen.PixelTestTol(190, 713, (205, 205, 205), 5):
                        print("Throwing a grenade")
                        FFX_Xbox.menuB()
                        FFX_Xbox.menuB()
                        countGrenades += 1
                    elif trosPos == 1:
                        print("Out of grenades. Stealing instead.")
                        FFX_Xbox.menuA()
                        time.sleep(0.2)
                        FFX_Xbox.menuLeft()
                        FFX_Xbox.menuB()
                        FFX_Xbox.menuB()
                        time.sleep(0.2)
                        countSteals += 1
                    else:
                        print("Out of grenades at range. Skipping turn.")
                        FFX_Xbox.menuA()
                        time.sleep(0.2)
                        FFX_Xbox.menuA()
                        time.sleep(0.2)
                        defend()
                        countDefends += 1
            elif FFX_Screen.turnTidus():
                if battleClock < 3:
                    print("Tros: Tidus attacking.")
                    attack('none')
                elif trosPos == 0:
                    print("Tros: Tidus at range. Defend.")
                    defend()
                elif trosPos == 1:
                    print("Tros: Tidus in range. Attack.")
                    attack('none')
                else:
                    print("Something went wrong. Deferring this turn.")
                    battleClock -= 1

        elif FFX_Screen.BattleComplete():
            FFX_memory.clickToControl()
            BattleComplete = 1
            FFX_Logs.writeStats("Tros Attacks:")
            FFX_Logs.writeStats(str(countAttacks))
            FFX_Logs.writeStats("Tros Revives:")
            FFX_Logs.writeStats(str(countRevives))
            FFX_Logs.writeStats("Tros Grenades:")
            FFX_Logs.writeStats(str(countGrenades))
            FFX_Logs.writeStats("Tros Steals:")
            FFX_Logs.writeStats(str(countSteals))
            FFX_Logs.writeStats("Tros Turns defending:")
            FFX_Logs.writeStats(str(countDefends))
            FFX_Logs.writeStats("Tros Turns healing (potions):")
            FFX_Logs.writeStats(str(countHeals))


def besaid():
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    battleFormat = FFX_memory.getBattleNum()
    print("Besaid battle format number: ", battleFormat)
    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
            if FFX_Screen.turnYuna():
                buddySwap(1)
            elif FFX_Screen.turnLulu():
                if battleFormat == 26:
                    fire('none')
                else:
                    thunder('none')
            elif FFX_Screen.turnWakka():
                attack('none')
            elif FFX_Screen.turnTidus():
                if battleFormat == 27:
                    attack('right')
                elif battleFormat == 23:
                    defend()
                else:
                    attack('right')

    FFX_memory.clickToControl()


def SinFin():
    FFX_Logs.writeLog("Fight start: Sin's Fin")
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
        if FFX_memory.battleScreen():
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
    FFX_Screen.clickToBattle()

def Echuilles():
    FFX_Logs.writeLog("Fight start: Sinspawn Echuilles")
    FFX_Screen.awaitTurn()
    print("Sinspawn Echuilles fight start")

    tidusCounter = 0
    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
            if FFX_Screen.faintCheck() > 0:
                revive()
            elif FFX_Screen.turnTidus():
                tidusCounter += 1
                if tidusCounter <= 2:
                    print("Cheer")
                    tidusFlee()  # performs cheer command
                elif tidusCounter == 6:
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
    FFXC.set_value('BtnB', 1)
    time.sleep(17)
    FFXC.set_value('BtnB', 0)
    FFX_Xbox.skipScene()

def lancetTutorial():
    FFX_Logs.writeLog("Fight start: Lancet tutorial fight (Kilika)")
    FFX_Screen.clickToBattle()
    lancet('none')

    turn1 = 0
    turn2 = 0
    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
            if FFX_Screen.turnTidus():
                attack('none')
            elif FFX_Screen.turnKimahri():
                buddySwap(1)
                defend()
            elif FFX_Screen.turnLulu():
                fire('none')
            else:
                defend()
    FFXC.set_value('BtnB', 1)
    time.sleep(2)
    FFXC.set_value('BtnB', 0)


def KilikaWoods(valeforCharge):
    FFX_Logs.writeLog("Fight start: Kilika general")
    BattleComplete = 0
    speedSpheres = 0
    currentCharge = False
    skipCharge = False
    turnCounter = 0
    bNum = FFX_memory.getBattleNum()
    preEmpt = FFX_Screen.PixelTestTol(1378, 271, (50, 52, 50), 5)

    FFXC.set_value('Dpad', 0)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)

    # if bNum == 31: #Lizard and Elemental, side
    # elif bNum == 32: #Lizard and Bee, front
    # elif bNum == 33: #Yellow and Bee, front
    # elif bNum == 34: #Lizard, Yellow, and Bee, front
    # elif bNum == 35: #Single Ragora, reverse
    # elif bNum == 36: #Two Ragoras, reverse
    # elif bNum == 37: #Ragora and two bees, reverse

    # These battles we want nothing to do with.
    if bNum == 32 or bNum == 35 or bNum == 36 or bNum == 37:
        skipCharge = True

    print("Kilika battle")
    while BattleComplete == 0:
        if valeforCharge == False and skipCharge == False:  # Still to charge Valefor
            if FFX_memory.battleScreen():
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
                    else:
                        defend()
                elif bNum == 33:  # Working just fine
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
                    else:
                        defend()
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
                        aeonSpell(0)
                    else:
                        defend()
                else:
                    skipCharge = True
                    print("Unexpected battle. Not going to charge Valefor.")
        else:
            if FFX_memory.battleScreen():
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
                            FFX_Xbox.tidusFlee()
                    else:
                        defend()
                elif bNum == 32:
                    if FFX_Screen.turnTidus():
                        if turnCounter < 4:
                            attack('none')
                        else:
                            FFX_Xbox.tidusFlee()
                    elif FFX_Screen.turnWakka():
                        attack('right')
                    else:
                        defend()
                elif bNum == 33:
                    if FFX_Screen.turnTidus():
                        if turnCounter < 4:
                            defend()
                        else:
                            FFX_Xbox.tidusFlee()
                    elif FFX_Screen.turnWakka():
                        attack('right')
                    else:
                        defend()
                elif bNum == 34:
                    if FFX_Screen.turnTidus():
                        if turnCounter < 4:
                            attack('none')
                        else:
                            FFX_Xbox.tidusFlee()
                    elif FFX_Screen.turnWakka():
                        attack('right')
                    else:
                        defend()
                elif bNum == 35 or bNum == 36:
                    if FFX_Screen.turnTidus():
                        FFX_Xbox.tidusFlee()
                    else:
                        defend()
                elif bNum == 37:
                    if FFX_Screen.turnTidus():
                        buddySwap(2)
                        thunder('left')
                    elif FFX_Screen.turnLulu():
                        buddySwap(2)
                        FFX_Xbox.tidusFlee()
                    elif FFX_Screen.turnWakka():
                        attack('left')
                    else:
                        defend()
        if FFX_Screen.BattleComplete():
            # speedSpheres = FFX_Screen.checkSpeed()
            # print("Speed spheres picked up: ",speedSpheres)
            # FFXC.set_value('BtnB', 1)
            # time.sleep(0.5)
            # FFXC.set_value('BtnB', 0)
            BattleComplete = 1

    FFX_memory.clickToControl()  # Rewards screen
    if currentCharge == True:
        valeforCharge = True
    hpCheck = FFX_memory.getHP()
    if hpCheck[0] < 250 or hpCheck[1] < 250 or hpCheck[4] < 250:
        healUp2(3)
    else:
        print("No need to heal up. Moving onward.")

    return valeforCharge


def Geneaux():
    FFX_Logs.writeLog("Fight start: Sinspawn Geneaux")
    FFX_Screen.awaitTurn()
    if FFX_Screen.turnYuna():
        buddySwap(1)
        defend()
        FFX_Screen.awaitTurn()
        attack('none')
        FFX_Screen.clickToBattle()
        buddySwap(1)
    else:
        attack('none')
        FFX_Screen.clickToBattle()
    aeonSummon(0)  # Summon Valefor
    FFX_Screen.awaitTurn()
    FFX_Xbox.menuLeft()
    time.sleep(0.8)
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()  # Lead off with Valefor overdrive

    valeforOD = 0
    skipCount = 0
    while not FFX_memory.userControl():
        if FFX_memory.battleScreen():
            print("Valefor casting Fire")
            aeonSpell(0)
        elif FFX_Screen.BattleComplete():
            FFX_Xbox.menuB()
    print("Battle Complete")


def LucaWorkers():
    FFX_Logs.writeLog("Fight start: Workers in Luca")
    BattleComplete = 0
    FFX_Screen.awaitTurn()

    while BattleComplete == 0:
        if FFX_Screen.BattleComplete():
            FFXC.set_value('BtnB', 1)
            time.sleep(2)
            FFXC.set_value('BtnB', 0)
            BattleComplete = 1
        elif FFX_memory.battleScreen():
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


def LucaWorkers2():
    FFX_Logs.writeLog("Fight start: Workers in Luca")
    BattleComplete = 0
    kimTurn = 0
    tidTurn = 0
    luluTurn = 0
    FFX_Screen.awaitTurn()

    while BattleComplete == 0:
        if FFX_Screen.BattleComplete():
            FFXC.set_value('BtnB', 1)
            time.sleep(2)
            FFXC.set_value('BtnB', 0)
            BattleComplete = 1
        elif FFX_memory.battleScreen():
            if FFX_Screen.turnKimahri():
                if FFX_Screen.faintCheck() >= 1:
                    revive()
                else:
                    kimTurn += 1
                    if kimTurn == 2:
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
                    elif kimTurn < 3:
                        attack('right')
                    else:
                        defend()
            elif FFX_Screen.turnTidus():
                if FFX_Screen.faintCheck() >= 1:
                    revive()
                else:
                    tidTurn += 1
                    if tidTurn < 3:
                        attack('right')
                    else:
                        defend()
            elif FFX_Screen.turnLulu():
                luluTurn += 1
                if luluTurn == 2 and kimTurn < 2:
                    FFX_Xbox.weapSwap(0)
                else:
                    thunder('none')
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()  # Clicking to get through the battle faster
    FFX_memory.clickToControl()


def Oblitzerator(earlyHaste):
    FFX_Logs.writeLog("Fight start: Oblitzerator")
    FFX_Screen.clickToBattle()
    crane = 0

    # if earlyHaste == 1:
    #    #First turn is always Tidus. Haste Lulu if we've got the levels.
    #    FFX_Xbox.tidusHaste('left')

    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
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
        else:
            FFX_Xbox.menuB()
    FFX_memory.clickToControl()

def afterBlitz():
    FFX_Logs.writeLog("Fight start: After Blitzball (the fisheys)")
    FFX_Screen.awaitTurn()

    # Tidus haste self
    FFX_Xbox.tidusHaste('none')
    wakkaTurns = 0

    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
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
                    if cam[0] > 1:
                        FFX_Xbox.menuUp()
                    else:
                        FFX_Xbox.menuRight()
                    FFX_Xbox.menuB()
                    print("Wakka healing Tidus for safety")
                else:
                    defend()
    FFXC.set_value('BtnB', 1)
    time.sleep(8)
    FFXC.set_value('BtnB', 0)
    FFX_Xbox.SkipDialog(8) # Quick dialog, "What's going on?"
    FFX_Xbox.skipScene()

    FFX_Screen.awaitTurn()
    attack('none') #Hardest boss in the game.
    print("Well that boss was difficult.")

    # Tidus haste self
    FFX_Xbox.SkipDialog(20)
    
    print("Ready to take on Zu")
    # Wakka dark attack, or Auron power break
    FFX_Screen.awaitTurn()
    if FFX_Screen.turnAuron():
        print("Auron's turn")
        useSkill(0)
    elif FFX_Screen.turnTidus():
        print("Tidus's turn")
        FFX_Xbox.tidusHaste('up')
    else:
        print("Wakka's turn")
        useSkill(0)
    FFX_Screen.awaitTurn()
    if FFX_Screen.turnAuron():
        useSkill(0)
    elif FFX_Screen.turnTidus():
        FFX_Xbox.tidusHaste('up')
    else:
        useSkill(0)
    FFX_Screen.awaitTurn()
    if FFX_Screen.turnAuron():
        useSkill(0)
    else:
        useSkill(0)

    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
            if FFX_Screen.faintCheck() > 0:
                revive()
            else:
                attack('none')
    FFXC.set_value('BtnB', 1)
    time.sleep(2)
    FFXC.set_value('BtnB', 0)


def MiihenRoad(selfDestruct):
    FFX_Logs.writeLog("Fight start: Mi'ihen Road")
    battle = FFX_memory.getBattleNum()

    hpArray = FFX_memory.getBattleHP()
    hpTotal = hpArray[1] + hpArray[2] + hpArray[3]
    if hpTotal < 1800:
        ambushed = True
    else:
        ambushed = False

    while not FFX_Screen.BattleComplete():
        if ambushed == True:
            print("Looks like we got ambushed. Skipping this battle.")
            fleeAll()
            break
        if FFX_memory.battleScreen():
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
    if hpCheck[0] < 520 or hpCheck[2] < 800 or hpCheck[4] < 400:
        healUp(3)
    else:
        print("No need to heal up. Moving onward.")
    print("selfDestruct flag: ", selfDestruct)
    return selfDestruct


def chocoEater():
    FFX_Logs.writeLog("Fight start: Chocobo Eater")
    FFX_Screen.awaitTurn()
    FFX_Xbox.tidusHaste('right')  # First turn, haste the chocobo eater
    turns = 0
    while not FFX_Screen.Minimap2():
        if FFX_memory.battleScreen():
            turns += 1
            if FFX_Screen.faintCheck() > 0:
                revive()
            else:
                defend()
        else:
            FFX_Xbox.menuB()
    FFX_Logs.writeStats("Chocobo eater turns:")
    FFX_Logs.writeStats(str(turns))


def aeonBoost():
    FFX_Screen.awaitTurn()
    FFX_Xbox.menuRight()
    time.sleep(0.6)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()


def MRRbattle(status):
    # status = [0, 0, 0, 0, 0]
    # Yuna complete, Kimahri complete, Valefor overdrive, Battle counter, Yuna level up complete]
    turnCounter = 0
    getOut = 0
    countAttacks = 0
    countRevives = 0
    basicTurn = 0
    turnCounter = 0
    preEmpt = False

    hpArray = FFX_memory.getBattleHP()
    hpTotal = hpArray[1] + hpArray[2] + hpArray[3]
    if hpTotal < 1800:
        basicTurn = 1
        print("We got ambushed. Not going to attempt to charge Valefor.")

    # Revisit this later. Hard-forcing us to skip the Valefor strat
    # if valDrive == 0:
    #    valDrive = 2

    if status[0] == 1 and status[1] == 1 and status[2] == 0:
        print("Yuna and Kimahri got levels somehow... OK no Valefor overdrive I guess.")
        valDrive = 2
    if status[4] > 1:
        status[2] = 2
    if status[2] == 2:
        if status[4] == 1:
            status[2] = 1
        else:
            basicTurn = 1

    if status[2] == 1:
        if FFX_Screen.PixelTestTol(1378, 277, (24, 27, 24), 5):
            preEmpt = True

    kimTurn = False
    yunaTurn = False
    chargePhase = False

    FFX_Logs.writeLog("Fight start: Mushroom Rock Road")
    if FFX_Screen.faintCheck() >= 1:
        print("Don't even bother checking which battle this is.")
        print("We got ambushed and are getting out of here.")
        fleeAll()
        getOut = 1
    else:
        battle = FFX_Screen.MRRbattle()
        FFX_Logs.writeLog("MRR battle, formation #" + str(battle))
        print("Battle has been engaged. Enemy formation: ", battle)
        print(status)
        while not FFX_Screen.BattleComplete():
            if FFX_memory.battleScreen():
                turnCounter += 1
                print(turnCounter)
                if turnCounter == 1 and not FFX_Screen.turnTidus():
                    getOut = 1
                if getOut == 0 and FFX_Screen.faintCheck() > 0 and turnCounter < 3:
                    getOut = 1
                if getOut == 0 and turnCounter > 11:
                    if FFX_Screen.turnAeon():
                        getOut = 0
                    elif battle > 2 and battle < 6:
                        getOut = 1
                    else:
                        getOut = 0
                if getOut == 1:
                    fleeAll()
                    break
                if battle == 0 or battle == 1 or battle == 9:
                    fleeAll()
                    break
                if status[2] == 0 and basicTurn == 0:
                    if battle == 2 or battle == 6 or battle == 7 or status[3] >= 3:
                        if battle == 1:
                            print("Can't overdrive on battle formation 1.")
                            fleeAll()
                            break
                        if FFX_Screen.turnKimahri():
                            kimTurn = True
                            defend()
                        elif FFX_Screen.turnWakka():
                            defend()
                        elif kimTurn == True:
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
                        else:
                            buddySwap(2)
                            defend()
                            kimTurn = True
                    else:
                        basicTurn = 1
                        turnCounter = 0
                elif chargePhase == True or (status[2] == 1 and basicTurn == 0 and status[4] == 1):

                    chargePhase = True
                    print(status)
                    # Yuna must have enough levels for this to trigger.
                    if battle == 3:  #
                        print("Battle 3 - we'll try to clear one monster and then charge Valefor")
                        if FFX_Screen.turnTidus():
                            buddySwap(2)
                            attack('right')  # Kimahri in for attack
                        elif FFX_Screen.turnAeon():
                            aeonSpell(3)  # Blizzard on red elemental and anything left over
                        else:
                            if preEmpt == True:
                                defend()
                                FFX_Screen.awaitTurn()
                                defend()
                                FFX_Screen.awaitTurn()
                            buddySwap(0)
                            aeonSummon(0)
                            FFX_Screen.awaitTurn()
                            FFX_Xbox.menuDown()
                            FFX_Xbox.menuDown()
                            FFX_Xbox.menuB()
                            time.sleep(0.6)
                            FFX_Xbox.menuB()
                            time.sleep(0.6)
                            FFX_Xbox.menuLeft()  # Screen reversed for aeon
                            FFX_Xbox.menuB()  # Fire on Lamashtu
                            time.sleep(0.5)
                            FFX_Screen.awaitTurn()
                            aeonBoost()
                            print("BOOOOOST")
                    elif battle == 5:  #
                        print("Battle 5 - Straight to it, no mucking around")
                        if FFX_Screen.turnTidus():
                            buddySwap(2)
                            FFX_Screen.awaitTurn()
                            defend()
                        elif FFX_Screen.turnAeon():
                            FFX_Xbox.menuDown()
                            FFX_Xbox.menuDown()
                            FFX_Xbox.menuB()
                            time.sleep(1)
                            FFX_Xbox.menuDown()
                            FFX_Xbox.menuRight()
                            FFX_Xbox.menuB()
                            time.sleep(1)
                            FFX_Xbox.menuLeft()
                            FFX_Xbox.menuB()
                            time.sleep(0.5)
                        else:
                            if preEmpt == True:
                                defend()
                                FFX_Screen.awaitTurn()
                                defend()
                                FFX_Screen.awaitTurn()
                                defend()
                                FFX_Screen.awaitTurn()
                            buddySwap(0)
                            aeonSummon(0)
                            FFX_Screen.awaitTurn()
                            FFX_Xbox.menuDown()
                            FFX_Xbox.menuDown()
                            FFX_Xbox.menuB()
                            time.sleep(1)
                            FFX_Xbox.menuDown()
                            FFX_Xbox.menuB()
                            time.sleep(1)
                            FFX_Xbox.menuRight()
                            FFX_Xbox.menuB()
                            time.sleep(0.5)
                            FFX_Screen.awaitTurn()
                            aeonBoost()
                    elif battle == 6:  #
                        print("Battle 6 - Kill off Gandyboy and then charge Valefor")
                        if FFX_Screen.turnTidus():
                            buddySwap(2)  # Swap for Kimahri
                            lancet('right')
                        elif FFX_Screen.turnWakka():
                            attack('right')
                        elif FFX_Screen.turnAuron():
                            if preEmpt == True:
                                defend()
                                FFX_Screen.awaitTurn()
                            buddySwap(0)
                            aeonSummon(0)
                            aeonSpell(0)  # Fire for Funguar
                            FFX_Screen.awaitTurn()
                            aeonBoost()
                            print("BOOOOOST")
                        elif FFX_Screen.turnAeon():
                            aeonSpell(3)  # Ice for red elemental
                    else:
                        # Catchall for any unexpected battle formations.
                        basicTurn = 1
                        turnCounter = 0
                        chargePhase = False
                elif status[0] == 1 and status[1] == 1:
                    print("Not yet charged, but no longer needing XP")
                    fleeAll()
                    break
                elif status[3] < 3:
                    print("Not yet ready to soak up levels. Just flee for now.")
                    fleeAll()
                    break
                else:
                    if battle == 2:
                        fleeAll()
                        break
                    elif battle == 3:  # done
                        if FFX_memory.partySize() == 2:
                            fleeAll()
                            break
                        if FFX_Screen.faintCheck():
                            revive()
                        if FFX_Screen.turnTidus():
                            buddySwap(2)
                            attack('right')
                        elif FFX_Screen.turnWakka():
                            attack('left')
                        elif FFX_Screen.turnKimahri():
                            buddySwap(0)
                            FFX_Xbox.weapSwap(0)
                        elif FFX_Screen.turnAuron():
                            attack('right')
                        elif FFX_Screen.turnYuna():
                            buddySwap(1)  # swap back to Auron
                            ice('none')
                        else:
                            defend()
                    elif battle == 4:  # done
                        if FFX_memory.partySize() == 2:
                            fleeAll()
                            break
                        if FFX_Screen.faintCheck() == 2:
                            fleeAll()
                            break
                        if FFX_Screen.faintCheck() == 1:
                            revive()
                        if FFX_Screen.turnTidus():
                            buddySwap(2)  # Swap for Kimahri
                            lancet('left')
                        elif FFX_Screen.turnWakka():
                            if turnCounter < 3:
                                attack('left')
                            else:
                                buddySwap(1)
                                ice('right')
                        elif FFX_Screen.turnAuron():
                            attack('none')
                        elif FFX_Screen.turnKimahri():
                            buddySwap(0)
                            defend()
                        elif FFX_Screen.turnLulu():
                            ice('none')
                        else:
                            defend()
                    elif battle == 5:  # done
                        if FFX_memory.partySize() == 2:
                            fleeAll()
                            break
                        if FFX_Screen.faintCheck() == 2:
                            fleeAll()
                            break
                        if FFX_Screen.faintCheck() == 1:
                            revive()
                        if FFX_Screen.turnTidus():
                            if turnCounter < 2:
                                buddySwap(2)  # Swap for Kimahri
                                lancet('down')
                            else:
                                attack('none')
                        elif FFX_Screen.turnWakka():
                            if turnCounter < 4:
                                attack('down')
                            else:
                                buddySwap(1)
                                ice('up')
                        elif FFX_Screen.turnKimahri():
                            buddySwap(0)
                            defend()
                        elif FFX_Screen.turnAuron():
                            buddySwap(2)  # Tidus back in
                            attack('none')
                        elif FFX_Screen.turnLulu():
                            ice('up')
                        else:
                            defend()
                    elif battle == 6:  # done
                        if FFX_memory.partySize() == 2:
                            fleeAll()
                            break
                        if FFX_Screen.faintCheck() == 2:
                            fleeAll()
                            break
                        if FFX_Screen.faintCheck() == 1:
                            revive()
                        if FFX_Screen.turnTidus():
                            buddySwap(2)  # Swap for Kimahri
                            lancet('right')
                        elif FFX_Screen.turnWakka():
                            if turnCounter < 3:
                                attack('right')
                            else:
                                buddySwap(2)  # swap for Tidus
                                fleeAll()
                                break
                        elif FFX_Screen.turnLulu() or FFX_Screen.turnKimahri():
                            buddySwap(0)  # swap for Yuna
                            aeonSummon(1)
                        elif FFX_Screen.turnAuron():
                            buddySwap(1)  # swap for Lulu
                            ice('left')
                        elif FFX_Screen.turnAeon():
                            attack('none')
                        else:
                            buddySwap(2)  # swap for Tidus
                            fleeAll()
                            break
                    elif battle == 7:  # done
                        if FFX_memory.partySize() == 2:
                            fleeAll()
                            break
                        if FFX_Screen.faintCheck() == 2:
                            fleeAll()
                            break
                        if FFX_Screen.faintCheck() == 1:
                            revive()
                        if FFX_Screen.turnTidus():
                            buddySwap(2)  # Swap for Kimahri
                            lancet('left')
                        elif FFX_Screen.turnWakka():
                            if turnCounter < 3:
                                attack('left')
                            else:
                                buddySwap(2)  # swap for Tidus
                                fleeAll()
                                break
                        elif FFX_Screen.turnKimahri():
                            buddySwap(0)
                            defend()
                        elif FFX_Screen.turnLulu():
                            buddySwap(2)
                            fleeAll()
                            break
                        elif FFX_Screen.turnAuron():
                            buddySwap(1)  # swap for Lulu
                            ice('right')
                        elif FFX_Screen.turnAeon():
                            attack('none')
                        else:
                            buddySwap(2)  # swap for Tidus
                            fleeAll()
                            break
                    elif battle == 8:
                        if FFX_Screen.turnTidus():
                            buddySwap(2)
                            defend()
                        elif FFX_Screen.turnAeon():
                            aeonSpell(0)
                        else:
                            buddySwap(0)
                            aeonSummon(1)
                            FFX_Screen.awaitTurn()
                            attack('none')
                    elif battle == 9:
                        fleeAll()
                        break
                    else:
                        fleeAll()
                        break
                    time.sleep(0.2)
    while not FFX_memory.userControl():
        if FFX_Screen.BattleComplete():
            FFX_Xbox.menuB()

    if chargePhase == True:
        print("We have charged Valefor back up.")
        status[2] = 2
        status[4] = battle
    print("Battle is complete. Now for clean-up.")
    # Fix party, then heal up.
    complete = 0
    while complete == 0:
        complete = FFX_Screen.mrrFormat()
    updateStatus = FFX_Screen.mrrCompletion(status)
    hpCheck = FFX_memory.getHP()
    print("HP values: ", hpCheck)
    if hpCheck[1] != 475:  # Yuna is low. Heal all.
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
    else:
        print("No need to heal up. Moving onward.")
        FFX_Xbox.menuA()
    print("Clean-up is now complete.")
    return updateStatus


def battleGui():
    FFX_Logs.writeLog("Fight start: Sinspawn Gui")
    FFX_Screen.clickToBattle()
    print("Engaging Gui")
    turns = 0
    phase = 1
    valeforFaint = False
    while turns < 3:
        if FFX_memory.battleScreen():
            turns += 1
            if FFX_Screen.turnTidus():
                defend()  # Tidus defends first turn
            if FFX_Screen.turnWakka():
                FFX_Xbox.weapSwap(0)
            if FFX_Screen.turnYuna():
                buddySwap(2)  # Auron in
                useSkill(0)  # Performs power break
            time.sleep(0.5)  # Avoids doubling up on any pattern
    if turns == 3:
        FFX_Screen.clickToBattle()
        turns += 1
        buddySwap(0)  # Switch Wakka for Kimahri
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
        FFX_Screen.clickToBattle()
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
    if turns == 5:
        while not FFX_Screen.turnSeymour():
            FFX_Screen.clickToBattle()
            if FFX_Screen.turnAeon() and FFX_Screen.checkCharge(1):
                # Ifrit with overdrive charged
                FFX_Xbox.menuLeft()
                time.sleep(0.8)
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()
                FFX_Xbox.menuB()  # Overdrive
                time.sleep(60)
                FFX_Screen.awaitPixel(1, 1, (255, 255, 255))
                time.sleep(2)
                FFX_Xbox.skipSceneSpec()
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
    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
            turn += 1
            if FFX_Screen.turnSeymour():
                while FFX_memory.battleMenuCursor() != 21:
                    FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                while FFX_memory.battleCursor2() != 4:
                    FFX_Xbox.menuDown()
                time.sleep(0.035)
                FFX_Xbox.menuB()
                if turn == 1:
                    FFX_Xbox.menuLeft()
                FFX_Xbox.menuB()
            else:
                defend()
    FFXC.set_value('BtnB', 1)
    time.sleep(2)
    FFXC.set_value('BtnB', 0)
    return valeforFaint


def djose(stoneBreath):
    FFX_Logs.writeLog("Fight start: Djose road")
    complete = 0
    while complete == 0:
        battleNum = FFX_memory.getBattleNum()
        #time.sleep(1)
        if FFX_Screen.BattleComplete():
            print("Djose: battle complete")
            FFX_memory.clickToControl()
            complete = 1
        elif FFX_memory.battleScreen():
            if stoneBreath == 1:  # Stone Breath already learned
                print("Djose: Stone breath already learned.")
                fleeAll()
                complete = 1
            if stoneBreath == 0:  # Stone breath not yet learned
                if battleNum == 128 or battleNum == 134 or battleNum == 136:
                    print("Djose: Learning Stone Breath.")
                    lancetSwapDjose('none')
                    complete = 1
                    stoneBreath = 1
                elif battleNum == 127:
                    print("Djose: Learning Stone Breath")
                    # One basilisk with two wasps
                    lancetSwapDjose('up')
                    complete = 1
                    stoneBreath = 1
                else:
                    print("Djose: Cannot learn Stone Breath here.")
                    fleeAll()
                    complete = 1

    FFX_memory.clickToControl()
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
    while complete == 0:
        if FFX_Screen.BattleComplete():
            FFXC.set_value('BtnB', 1)
            time.sleep(2)
            FFXC.set_value('BtnB', 0)
            complete = 1
        if FFX_memory.battleScreen():
            if FFX_Screen.turnTidus():
                tidusFlee()
            else:
                escapeOne()


def extractor():
    FFX_Logs.writeLog("Fight start: Extractor")
    FFX_Screen.clickToBattle()
    FFX_Xbox.tidusHaste('none')
    time.sleep(0.2)

    FFX_Screen.awaitTurn()
    attack('none')
    time.sleep(0.2)

    FFX_Screen.awaitTurn()
    FFX_Xbox.tidusHaste('left')
    time.sleep(0.2)

    tidusCheer = 0
    complete = 0
    while complete == 0:
        if FFX_memory.battleScreen():
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
            FFXC.set_value('BtnB', 1)
            time.sleep(0.035)
            FFXC.set_value('BtnB', 0)
            time.sleep(0.035)
    FFX_memory.clickToControl()


def mixTutorial():
    FFX_Logs.writeLog("Fight start: Mix Tutorial")
    FFX_Screen.clickToBattle()
    Steal()
    time.sleep(1)
    FFX_Screen.clickToBattle()
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
    FFX_Screen.clickToMap1()


def chargeRikku():
    FFX_Logs.writeLog("Fight start: Charging Rikku (before Guadosalam)")
    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
            if FFX_Screen.turnRikku():
                attack('none')
            else:
                escapeOne()
    FFX_Screen.clickToMap1()
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
    rikkucharge = 0

    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
            turnchar = FFX_memory.getBattleCharTurn()
            rikkucharge = FFX_memory.getOverdriveValue(6)
            if bNum == 152 or bNum == 155 or bNum == 162:  # Any battle with Larvae
                if startingstatus[2] == False:
                    if turnchar == 0:
                        if tidusturns == 0:
                            rikkuposition = FFX_memory.getBattleCharSlot(6)
                            buddySwap_new(rikkuposition)
                        else:
                            tidusFlee()
                        tidusturns += 1
                    elif turnchar == 6:
                        Steal()
                        status[2] = True
                    else:
                        tidusposition = FFX_memory.getBattleCharSlot(0)
                        buddySwap_new(tidusposition)
                elif turnchar == 0:
                    tidusFlee()
                else:
                    fleeAll()
            elif bNum == 160:
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
                        status[1] = True
                    else:
                        defend()
                elif turnchar == 0:
                    tidusFlee()
                else:
                    fleeAll()
            elif bNum == 161:
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
                            if wakkaHP > rikkuHP > 0 and rikkucharge < 100:
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
                            if wakkaHP > rikkuHP > 0 and rikkucharge < 100:
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
                            if wakkaHP > rikkuHP > 0 and rikkucharge < 100:
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
    FFX_memory.clickToControl()
    # FFX_Xbox.menuB() #In case lightning is incoming. Happens far too often.
    if rikkucharge == 100:
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

def thunderPlains_Old(status, section):
    bNum = FFX_memory.getBattleNum()
    nadeSlot = FFX_memory.getUseItemsSlot(35)
    nadeCount = FFX_memory.getItemCountSlot(nadeSlot)
    if nadeCount > 1:
        throwNades = True
    else:
        throwNades = False

    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
            if bNum == 152 or bNum == 155 or bNum == 162:  # Any battle with Larvae
                if status[2] == False:
                    if FFX_Screen.turnTidus():
                        buddySwap(1)
                        Steal()
                        status[2] = True
                    else:
                        buddySwap(1)
                        fleeAll()
                elif FFX_Screen.turnTidus():
                    fleeAll()
                else:
                    buddySwap(1)
                    fleeAll()
            elif bNum == 160:
                if status[1] == False:
                    if FFX_Screen.turnTidus():
                        buddySwap(1)
                        Steal()
                        status[1] = True
                    else:
                        buddySwap(1)
                        fleeAll()
                elif FFX_Screen.turnTidus():
                    fleeAll()
                else:
                    buddySwap(1)
                    fleeAll()
            elif bNum == 161:
                if status[1] == False:
                    if FFX_Screen.turnTidus():
                        buddySwap(1)
                        Steal()
                        status[1] = True
                    else:
                        buddySwap(1)
                        fleeAll()
                if throwNades == True and FFX_memory.getSpeed() < 15 and section == 2:
                    if FFX_Screen.turnTidus():
                        buddySwap(1)
                        useItem(1, 'none')
                    else:
                        buddySwap(1)
                        fleeAll()
                elif FFX_Screen.turnTidus():
                    fleeAll()
                else:
                    buddySwap(1)
                    fleeAll()
            elif throwNades == True and (bNum == 154 or bNum == 156 or bNum == 164):
                if FFX_memory.getSpeed() < 15 and section == 2:
                    if FFX_Screen.turnTidus():
                        buddySwap(1)
                        useItem(1, 'none')
                    else:
                        buddySwap(1)
                        fleeAll()
                elif FFX_Screen.turnTidus():
                    fleeAll()
                else:
                    buddySwap(1)
                    fleeAll()
            else:  # Nothing useful this battle. Moving on.
                fleeAll()
    FFX_memory.clickToControl()
    # FFX_Xbox.menuB() #In case lightning is incoming. Happens far too often.
    print("Status array, Rikku charge, Light curtain, and Lunar Curtain:")
    print(status)
    print("Checking party format and resolving if needed.")
    FFX_memory.fullPartyFormat('kimahri')
    print("Party format is good. Now checking health values.")
    hpValues = FFX_memory.getHP()
    if hpValues[0] < 700 or hpValues[2] < 1000:
        healUp(3)
    print("Ready to continue onward.")
    print("Plains variables: Rikku charged, stolen lunar curtain, stolen light curtain")
    print(status)
    return status


def thunderPlains_old2(rikkuCharge):
    FFX_Logs.writeLog("Fight start: Thunder Plains")
    print("Rikku steal, Tidus flee, Auron escape if needed")
    rikkuCharge = 0
    BattleComplete = 0
    while BattleComplete == 0:
        if FFX_memory.battleScreen():
            if FFX_Screen.turnRikku():
                Steal()
            elif FFX_Screen.turnTidus():
                if rikkuCharge == 1:
                    tidusFlee()
                elif FFX_memory.partySize() == 3 and FFX_Screen.checkCharge(2):
                    print("Rikku is now charged.")
                    rikkuCharge = 1
                    tidusFlee()
                    print("Tidus using Flee. Let's get out of here.")
                else:
                    print("Rikku is not yet charged.")
                    escapeOne()
            else:
                escapeOne()
        if FFX_Screen.BattleComplete():
            FFXC.set_value('BtnB', 1)
            time.sleep(1.8)
            FFXC.set_value('BtnB', 0)
            time.sleep(0.1)
            FFX_Xbox.menuB()
            BattleComplete = 1
    healUp(3)


def mWoods(woodsVars):
    FFX_Logs.writeLog("Fight start: Macalania Woods")
    print("Logic depends on completion of specific goals. In Order:")
    print("Rikku charged, stolen Fish Scale, stolen Arctic Wind")
    print(woodsVars)
    tidusIn = True
    battleNum = FFX_memory.getBattleNum()
    print("------------- Battle Start - Battle Number: ", battleNum)
    tidusturns = 0
    rikkucharge = 0
    FFX_Screen.awaitTurn()
    if FFX_Screen.turnTidus() == False:
        fleeAll()
    else:
        try:
            while not FFX_Screen.BattleComplete():
                if FFX_memory.battleScreen():
                    turnchar = FFX_memory.getBattleCharTurn()
                    rikkucharge = FFX_memory.getOverdriveValue(6)
                    if woodsVars[0] == False:  # Rikku needs charging.
                        if turnchar == 6:
                            if battleNum == 175 and woodsVars[2] == False:
                                Steal()
                            elif battleNum == 172 and woodsVars[1] == False:
                                StealDown()
                            elif battleNum == 171 and woodsVars[1] == False:
                                StealRight()
                            else:
                                attack('none')
                        else:
                            escapeOne()
                    elif woodsVars[1] == False or woodsVars[2] == False:
                        if battleNum == 175 and woodsVars[2] == False:
                            if turnchar == 0:
                                wakkasafe = FFX_memory.petrifiedstate(4) == False and FFX_memory.getBattleHP()[FFX_memory.getBattleCharSlot(4)] > 200
                                if tidusturns == 0 and wakkasafe == True:
                                    rikkuposition = FFX_memory.getBattleCharSlot(6)
                                    buddySwap_new(rikkuposition)
                                else:
                                    tidusFlee()
                                tidusturns += 1
                            elif turnchar == 4:
                                tidusposition = FFX_memory.getBattleCharSlot(0)
                                buddySwap_new(tidusposition)
                            elif turnchar == 6:
                                Steal()
                            else:
                                tidusposition = FFX_memory.getBattleCharSlot(0)
                                if tidusposition > 3:
                                    buddySwap_new(tidusposition)
                                else:
                                    fleeAll()
                        elif battleNum == 172 and woodsVars[1] == False:
                            if turnchar == 0:
                                wakkasafe = FFX_memory.petrifiedstate(4) == False and FFX_memory.getBattleHP()[
                                    FFX_memory.getBattleCharSlot(4)] > 200
                                if tidusturns == 0 and wakkasafe == True:
                                    rikkuposition = FFX_memory.getBattleCharSlot(6)
                                    buddySwap_new(rikkuposition)
                                else:
                                    tidusFlee()
                                tidusturns += 1
                            elif turnchar == 4:
                                tidusposition = FFX_memory.getBattleCharSlot(0)
                                buddySwap_new(tidusposition)
                            elif turnchar == 6:
                                StealDown()
                            else:
                                tidusposition = FFX_memory.getBattleCharSlot(0)
                                if tidusposition > 3:
                                    buddySwap_new(tidusposition)
                                else:
                                    fleeAll()
                        elif battleNum == 171 and woodsVars[1] == False:
                            if turnchar == 0:
                                wakkasafe = FFX_memory.petrifiedstate(4) == False and FFX_memory.getBattleHP()[
                                    FFX_memory.getBattleCharSlot(4)] > 200
                                if tidusturns == 0 and wakkasafe == True:
                                    rikkuposition = FFX_memory.getBattleCharSlot(6)
                                    buddySwap_new(rikkuposition)
                                else:
                                    tidusFlee()
                                tidusturns += 1
                            elif turnchar == 4:
                                tidusposition = FFX_memory.getBattleCharSlot(0)
                                buddySwap_new(tidusposition)
                            elif turnchar == 6:
                                StealRight()
                            else:
                                tidusposition = FFX_memory.getBattleCharSlot(0)
                                if tidusposition > 3:
                                    buddySwap_new(tidusposition)
                                else:
                                    fleeAll()
                        else:
                            tidusFlee()
                    else:
                        tidusFlee()
        except Exception as errMsg:
            print("An error occurred. Error message:")
            print(errMsg)
            fleeAll()

    print("Battle complete, now to deal with the aftermath.")
    FFX_memory.clickToControl3()
    if rikkucharge == 100:
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


def mWoods_Old(woodsVars):
    FFX_Logs.writeLog("Fight start: Macalania Woods")
    print("Logic depends on completion of specific goals. In Order:")
    print("Rikku charged, stolen Fish Scale, stolen Arctic Wind")
    try:
        print(woodsVars)
    except:
        print("Could not print woods vars.")
    stealAttempt = False
    tidusIn = True
    try:
        while not FFX_Screen.BattleComplete():
            if FFX_memory.battleScreen():
                if woodsVars[0] == False:  # Rikku needs charging.
                    if FFX_Screen.turnTidus():
                        buddySwap(1)
                        tidusIn = False
                        if FFX_Screen.checkCharge(1):
                            woodsVars[0] = True
                    if FFX_Screen.turnRikku():
                        if stealAttempt == False:
                            battleNum = FFX_memory.getBattleNum()
                            if battleNum == 175 and woodsVars[2] == False:
                                Steal()
                                stealAttempt = True
                            elif battleNum == 172 and woodsVars[1] == False:
                                StealDown()
                                stealAttempt = True
                            elif battleNum == 171 and woodsVars[1] == False:
                                StealRight()
                                stealAttempt = True
                            elif woodsVars[0] == True:
                                buddySwap(1)
                                fleeAll()
                            else:
                                attack('none')
                        elif woodsVars[0] == True and tidusIn == False:
                            buddySwap(1)
                            tidusIn == True
                            fleeAll()
                        else:
                            attack('down')
                    else:
                        escapeOne()
                elif stealAttempt == False and (woodsVars[1] == False or woodsVars[2] == False):
                    battleNum = FFX_memory.getBattleNum()
                    if battleNum == 171 and woodsVars[1] == False:
                        if FFX_Screen.turnTidus():
                            buddySwap(1)
                            FFX_Screen.awaitTurn()
                            StealRight()
                        else:
                            buddySwap(1)
                            fleeAll()
                    elif battleNum == 172 and woodsVars[1] == False:
                        if FFX_Screen.turnTidus():
                            buddySwap(1)
                            FFX_Screen.awaitTurn()
                            StealDown()
                        else:
                            buddySwap(1)
                            fleeAll()
                    elif battleNum == 175 and woodsVars[2] == False:
                        if FFX_Screen.turnTidus():
                            buddySwap(1)
                            FFX_Screen.awaitTurn()
                            Steal()
                        else:
                            buddySwap(1)
                            fleeAll()
                    else:
                        if tidusIn == False:
                            buddySwap(1)
                            tidusIn = True
                        fleeAll()
                else:
                    if tidusIn == False:
                        buddySwap(1)
                        tidusIn = True
                    fleeAll()
    except Exception as errMsg:
        print("An error occurred. Error message:")
        print(errMsg)
        fleeAll()

    print("Battle complete, now to deal with the aftermath.")
    if FFX_Screen.BattleComplete():
        FFX_memory.clickToControl()
    print("Checking battle formation.")
    FFX_memory.fullPartyFormat('kimahri')
    print("Party format is now good. Let's check health.")
    # Heal logic
    partyHP = FFX_memory.getHP()
    if partyHP[0] < 450 or partyHP[6] < 180:
        healUp(3)
    print("And last, we'll update variables.")
    if FFX_memory.getUseItemsSlot(32) != 255:
        woodsVars[1] = True
    if FFX_memory.getUseItemsSlot(24) != 255:
        woodsVars[2] = True
    print("Rikku charged, stolen Fish Scale, stolen Arctic Wind")
    print(woodsVars)
    print("HP is good. Onward!")
    return woodsVars


def mWoods_old2(woodsVars):
    # depreciated, do not use.
    FFX_Logs.writeLog("Fight start: Macalania Woods")
    print("Rikku steal, Tidus flee, Auron escape if needed.")
    BattleComplete = 0
    print("Variable check: ", woodsVars)
    while BattleComplete == 0:
        if FFX_memory.battleScreen():
            if FFX_Screen.turnTidus():
                time.sleep(0.5)
                if woodsVars[0] == 1:
                    print("Tidus using Flee. Let's get out of here.")
                    tidusFlee()
                else:
                    if FFX_memory.partySize() == 3 and FFX_Screen.checkCharge(2):
                        print("Rikku is now charged.")
                        woodsVars[0] = 1
                        tidusFlee()
                        print("Tidus using Flee. Let's get out of here.")
                    else:
                        print("Tidus using escape. Let's get out of here.")
                        escapeOne()
            elif FFX_Screen.turnRikku():
                if woodsVars[0] == 0:
                    if FFX_memory.partySize() == 3 and FFX_Screen.checkCharge(2):
                        print("Rikku is now charged.")
                        woodsVars[0] = 1
                if woodsVars[1] == 0 or woodsVars[2] == 0:
                    time.sleep(1)  # Allows us to identify the screen we're on.
                    print("Rikku still needs something.")
                    print(woodsVars)
                    if FFX_Screen.PixelTestTol(1069, 28, (49, 143, 164), 5) and woodsVars[1] == 0:  # Chimera confirmed
                        print("Chimera")
                        Steal()
                        while not FFX_memory.battleScreen():
                            if FFX_Screen.PixelTest(884, 91, (225, 225, 225)):
                                woodsVars[1] = 1
                    elif FFX_Screen.PixelTestTol(649, 10, (32, 85, 109), 5) and woodsVars[
                        2] == 0:  # One bee, two blue ele's confirmed
                        print("Double blue elemental")
                        StealDown()
                        while not FFX_memory.battleScreen():
                            if FFX_Screen.PixelTest(934, 94, (219, 219, 219)):
                                woodsVars[2] = 1
                    elif FFX_Screen.PixelTestTol(1132, 61, (52, 151, 170), 5) and woodsVars[
                        2] == 0:  # Blue ele with tanker and raptor confirmed
                        print("Single blue elemental")
                        StealRight()
                        while not FFX_memory.battleScreen():
                            if FFX_Screen.PixelTest(934, 94, (219, 219, 219)):
                                woodsVars[2] = 1
                    else:
                        print("Eh, nothing useful here.")
                        if woodsVars[0] == 0:
                            attack('none')
                        else:
                            escapeOne()
                else:
                    print("We're done with stealing here.")
                    print(woodsVars)
                    if woodsVars[0] == 0:
                        attack('none')
                    else:
                        escapeOne()
            elif FFX_Screen.turnAuron():
                if FFX_memory.partySize() == 3 and FFX_Screen.checkCharge(2):
                    print("Rikku is now charged.")
                    woodsVars[0] = 1
                escapeOne()
            time.sleep(0.1)
        if FFX_Screen.BattleComplete():
            FFXC.set_value('BtnB', 1)
            time.sleep(1.8)
            FFXC.set_value('BtnB', 0)
            BattleComplete = 1
    healUp(3)
    return woodsVars


# Process written by CrimsonInferno
def spherimorph():
    FFX_Logs.writeLog("Fight start: Spherimorph")
    FFX_Screen.clickToBattle()

    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('Dpad', 0)

    spellNum = 0
    tidusturns = 0
    rikkuturns = 0
    rikkuCounter = 0
    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
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
                # FFXC.set_value('AxisLx', 0)
                # FFXC.set_value('AxisLy', 0)
                # FFXC.set_value('Dpad', 0)

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

    FFXC.set_value('BtnB', 1)
    time.sleep(2)
    FFXC.set_value('BtnB', 0)


def spherimorph_old():
    FFX_Logs.writeLog("Fight start: Spherimorph")

    # Gameplan:
    # Formation starts as Auron Rikku Tidus
    # Rikku will swap for Kimahri, he lancets until the end of the fight.
    # Auron does not swap until the others have gone around the loop.

    # Tidus defends and then swaps for Yuna and defends
    # Yuna swaps for Lulu and defends
    # Lulu swaps for Tidus who defends
    # After that is complete, Auron swaps for Rikku who overdrives.

    FFX_Screen.clickToBattle()
    defend()  # Tidus defend
    print("Phase 1, setting up for Rikku to overdrive to victory")
    complete = 0
    spellNum = 0
    kimXP = 0
    luluXP = 0
    while complete == 0:
        if FFX_memory.battleScreen():
            if FFX_Screen.turnTidus():
                buddySwap(0)  # Tidus swap with Yuna.
                FFX_Screen.awaitTurn()
                defend()
            elif FFX_Screen.turnRikku():
                buddySwap(1)
                FFX_Screen.awaitTurn()
                lancet('none')  # Rikku for Kimahri, attack once
                kimXP = 1
            elif FFX_Screen.turnAuron():
                attack('none')
                time.sleep(0.8)
                spellNum = FFX_Screen.spherimorphSpell()
                print("Spell: ", spellNum)
            elif FFX_Screen.turnYuna():
                buddySwap(3)
                FFX_Screen.awaitTurn()
                defend()  # Yuna swap out for Lulu, defend
            elif FFX_Screen.turnLulu():
                defend()
        if spellNum != 0 and kimXP == 1:
            complete = 1

    print("Phase 2, get the last character XP needed and then Rikku overdrive")
    complete = 0
    rikkuCounter = 0
    tidusXP = 0
    while not complete == 1:
        FFXC.set_value('AxisLx', 0)
        FFXC.set_value('AxisLy', 0)
        FFXC.set_value('Dpad', 0)
        if FFX_Screen.BattleComplete():
            complete = 1
            FFXC.set_value('BtnB', 1)
            time.sleep(2)
            FFXC.set_value('BtnB', 0)
        elif FFX_memory.battleScreen():
            if FFX_Screen.turnKimahri():
                lancet('none')
            elif FFX_Screen.turnYuna():
                buddySwap(3)
                defend()  # Yuna swap out for Lulu, defend
            elif FFX_Screen.turnLulu():
                buddySwap(0)  # Tidus back in.
                defend()
                tidusXP = 1
            elif FFX_Screen.turnAuron():
                if tidusXP == 1:
                    buddySwap(1)
                    print("Swap done")
                else:
                    defend()
            elif FFX_Screen.turnTidus():
                defend()
            elif FFX_Screen.turnRikku():
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('Dpad', 0)
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
            time.sleep(0.5)


# Process written by CrimsonInferno
def negator():  # AKA crawler
    FFX_Logs.writeLog("Fight start: Crawler/Negator")
    print("Starting battle with Crawler")
    FFX_Screen.clickToBattle()
    # FFX_Screen.awaitTurn()

    marblesused = 0
    tidusturns = 0
    rikkuturns = 0
    kimahriturns = 0
    luluturns = 0
    yunaturns = 0

    while not FFX_Screen.BattleComplete():
        FFXC.set_value('AxisLx', 0)
        FFXC.set_value('AxisLy', 0)
        FFXC.set_value('Dpad', 0)
        if FFX_memory.battleScreen():
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

    FFXC.set_value('BtnB', 1)
    time.sleep(2)
    FFXC.set_value('BtnB', 0)

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

    while not FFX_memory.menuOpen():
        if FFX_memory.battleScreen():
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
                    FFX_Xbox.tidusHaste('none')
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
                    FFX_Xbox.tidusHaste('none')
                    tidushaste = True
                elif animahits < 4:
                    oldHP = FFX_memory.getEnemyCurrentHP()[3]
                    attack('none')
                    time.sleep(1.5)
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


# Process written by CrimsonInferno
def wendigoresheal(turnchar: int, usepowerbreak: int, tidusmaxHP: int):
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

    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
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
                    FFX_Xbox.tidusHaste('none')
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
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()  # Effectively clicking to battle and after battle dialog.

def bikanelCharge(chargeState):
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
        while not FFX_Screen.BattleComplete():
            if FFX_memory.battleScreen():
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
                            useItem('abPot', 'none')
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
                            useItem('abPot', 'none')
                            print("Using an Al Bhed potion")
                        else:
                            print("No need to heal. Attacking to kill a turn.")
                            attack('none')
                elif FFX_Screen.turnAuron():
                    escapeOne()
    FFX_memory.clickToControl()
    return chargeState

def desertSpeed(chargeState):
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
                if FFX_memory.battleScreen():
                    buddySwap(1)
                    FFX_Screen.awaitTurn()
                    FFX_Xbox.tidusFlee()
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

def desertFights(sandy):
    FFX_Logs.writeLog("Fight start: Kilika, looking for Sandragoras")
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
            FFX_Xbox.tidusHaste('left')
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
            FFX_Xbox.tidusHaste('down')
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
                if FFX_memory.battleScreen():
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
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    FFX_Screen.clickToBattle()
    print("Tidus vs Bombs")
    FFX_Xbox.tidusHaste('none')
    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
            if FFX_Screen.faintCheck() > 0:
                revive()
            elif FFX_Screen.turnTidus():
                FFX_Screen.awaitTurn()
                attack('none')
            else:
                defend()
    FFX_memory.clickToControl()


def home2():
    FFX_Logs.writeLog("Fight start: Home 2")
    FFX_Screen.clickToBattle()
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()

    print("Kimahri vs dual horns")
    buddySwap(1)  # Tidus for Kimahri
    lancetHome('none')
    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
            if FFX_Screen.turnKimahri():
                kimahriOD(4)
            else:
                defend()
    FFX_memory.clickToControl()
    FFX_Screen.openMenu()
    time.sleep(1)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()


def home3():
    FFX_Logs.writeLog("Fight start: Home 3")
    FFX_Screen.clickToBattle()
    randomFight = tidusFlee()
    complete = 0
    while complete == 0:
        if randomFight == 2:
            complete = 1
        else:
            FFX_Screen.clickToMap1()

            FFXC.set_value('AxisLy', -1)
            FFXC.set_value('AxisLx', -1)
            time.sleep(6)
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('AxisLx', 0)
            FFX_Screen.clickToBattle()
            randomFight = tidusFlee()

    print("Tidus vs dual horns")
    FFX_Xbox.tidusHaste('none')

    FFX_Screen.clickToBattle()
    if not FFX_Screen.turnTidus():
        while not FFX_Screen.turnTidus():
            defend()
            time.sleep(0.2)
            FFX_Screen.clickToBattle()
    tidusOD()

    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
            if FFX_Screen.turnTidus():
                attack('none')
            elif FFX_Screen.faintCheck() > 0:
                revive()
            elif FFX_Screen.turnKimahri():
                useItem(3, 'none')
            else:
                defend()
    FFX_memory.clickToControl()


def home4():
    FFX_Logs.writeLog("Fight start: Home 4")
    FFX_Screen.clickToBattle()

    print("Kimahri vs Chimera")
    buddySwap(1)  # Tidus for Kimahri
    time.sleep(0.2)
    lancetHome('none')
    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
            if FFX_Screen.turnKimahri():
                kimahriOD(5)
            else:
                defend()
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
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.clickToBattle()  # This gets us past the tutorial and all the dialog.

    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
            turnchar = FFX_memory.getBattleCharTurn()
            print("Tidus prep turns: ", tidusPrep)
            # print("otherTurns: ", otherTurns)
            if turnchar == 0:
                print("Registering Tidus's turn")
                if tidusPrep == 0:
                    tidusPrep = 1
                    FFX_Xbox.tidusHaste('none')
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
    while not FFX_memory.menuOpen():
        if FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
    FFXC.set_value('BtnB', 1)
    time.sleep(3)
    FFXC.set_value('BtnB', 0)

    time.sleep(4)
    FFX_Xbox.skipSceneSpec()


def guards(groupNum):
    FFX_Logs.writeLog("Fight start: Bevelle Guards")
    rikkuHeal = False
    turnNum = 0
    FFX_memory.awaitControl()
    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
            if FFX_Screen.turnTidus():
                turnNum += 1
                if turnNum == 1 and groupNum == 1:
                    attack('left')
                elif turnNum == 1 and groupNum == 3:
                    attack('down')
                elif turnNum == 1 and groupNum == 5:
                    attack('right')
                elif turnNum == 1 and (groupNum == 2 or groupNum == 4):
                    FFX_Xbox.tidusHaste('none')
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
                    useItem('abPot', 'none')
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
    FFX_Screen.clickToBattle()
    confirm = 0
    counter = 0
    while confirm == 0:
        counter += 1
        if FFX_memory.getBattleNum() >= 258 and FFX_memory.getBattleNum() <= 260:  # Now fighting Isaaru
            confirm = 2
        else:
            confirm = 1

    if confirm == 1:
        aeonSummon(2)
        time.sleep(0.5)
        while not FFX_Screen.BattleComplete():
            if FFX_memory.battleScreen():
                attack('none')
    else:
        while not FFX_Screen.BattleComplete():
            if FFX_memory.battleScreen():
                if FFX_Screen.turnYuna():
                    if FFX_memory.getBattleNum() == 260:
                        aeonSummon(2)
                    else:
                        aeonSummon(4)
                elif FFX_Screen.turnAeon():
                    attack('none')
                time.sleep(0.2)
            else:
                FFX_Xbox.menuB()

    while not FFX_memory.menuOpen():
        if FFX_memory.diagSkipPossible():
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
    evraeFight = tidusFlee()
    steal = 0
    gems = 1
    time.sleep(0.2)
    print(FFX_Screen.PixelValue(190, 705))
    print("(139, 139, 139) expected for Evrae")

    if evraeFight == 2:
        print("Evrae Altana fight start")
        # Start by hasting Rikku.
        while not FFX_Screen.BattleComplete():
            if FFX_memory.battleScreen():
                time.sleep(0.2)
                altanaheal()
        FFXC.set_value('BtnB', 1)
        time.sleep(2)
        FFXC.set_value('BtnB', 0)

    else:  # Just a regular group
        print("Not Evrae this time.")
        fleeAll()

    print("Returning value: " + str(gems))
    return gems

def seymourNatus():
    FFX_Logs.writeLog("Fight start: Seymour Natus")
    complete = 0
    fight = 0
    turn = 0
    summonDone = 0
    if FFX_memory.getBattleNum() == 272:  # Seymour Natus
        print("Seymour Natus engaged")
        fight = 1
        while not FFX_Screen.BattleComplete():
            if FFX_memory.battleScreen():
                if FFX_Screen.turnYuna() and summonDone == 0:
                    aeonSummon(4)
                    summonDone = 1
                else:
                    attack('none')
            else:
                FFX_Xbox.menuB()  # In case there's any dialog skipping
    elif FFX_memory.getBattleNum() == 270:  # YAT-63 x2
        fight = 4
        while complete == 0:
            if FFX_memory.battleScreen():
                if FFX_Screen.turnTidus():
                    if turn == 0:
                        turn += 1
                        attack('r3')
                    else:
                        tidusFlee()
                elif FFX_Screen.turnYuna():
                    attack('r3')
                else:
                    defend()
            elif FFX_Screen.BattleComplete():
                complete = 1
    elif FFX_memory.getBattleNum() == 269:  # YAT-63 with two guard guys
        fight = 3
        while complete == 0:
            if FFX_memory.battleScreen():
                if FFX_Screen.turnTidus():
                    if turn == 0:
                        turn += 1
                        attack('none')
                    else:
                        tidusFlee()
                elif FFX_Screen.turnYuna():
                    attack('none')
                else:
                    defend()
            elif FFX_Screen.BattleComplete():
                complete = 1
    elif FFX_memory.getBattleNum() == 271:  # one YAT-63, two YAT-99
        fight = 2
        while complete == 0:
            if FFX_memory.battleScreen():
                if FFX_Screen.turnTidus():
                    if turn == 0:
                        turn += 1
                        attack('r2')
                    else:
                        tidusFlee()
                elif FFX_Screen.turnYuna():
                    attack('r2')
                else:
                    defend()
            elif FFX_Screen.BattleComplete():
                complete = 1
    while not FFX_memory.menuOpen():
        if FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
    FFXC.set_value('BtnB', 1)
    time.sleep(3)
    FFXC.set_value('BtnB', 0)
    if fight == 1:
        return 1
    else:
        return 0


def calmLands(itemSteal):
    FFX_Logs.writeLog("Fight start: Calm Lands")
    steal = 0
    if itemSteal < 2:
        if FFX_Screen.PixelTestTol(1559, 274, (212, 192, 142), 5):  # Red element in center slot, with machina and dog
            print("Grabbing a gem here. This is gem number ", itemSteal + 1)
            FFX_Xbox.tidusHaste('left')
            time.sleep(3)
            FFX_Screen.awaitTurn()
            StealLeft()
            steal += 1
        elif FFX_Screen.PixelTestTol(174, 6, (169, 133, 85), 5):  # Red element in top slot, with bee and tank
            print("Grabbing a gem here. This is gem number ", itemSteal + 1)
            FFX_Xbox.tidusHaste('up')
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


def biranYenke():
    FFX_Logs.writeLog("Fight start: Biran and Yenke")
    FFX_Screen.clickToBattle()
    Steal()

    FFX_Screen.awaitTurn()
    gemSlot = FFX_memory.getUseItemsSlot(34)
    if gemSlot == 255:
        gemSlot = FFX_memory.getUseItemsSlot(28)
    useItem(gemSlot, 'none')

    FFX_Screen.clickToBattle()
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
    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
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
                    FFX_Xbox.tidusHaste('down')
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
        else:
            FFX_Xbox.menuB()
    print("Seymour Flux battle complete.")
    FFX_memory.clickToControl()


def seymourFlux_old():
    stage = 0
    # Two possible orders for the bosses. Either Seymour or the assistant will go first. Pixel is slightly different.
    FFX_Logs.writeLog("Fight start: Seymour Flux")
    print("Fight start: Seymour Flux")
    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
            if FFX_Screen.turnYuna():
                if stage == 0:
                    attack('none')
                elif stage == 1:
                    aeonSummon(4)
                    tidusFlee()  # Bahamut uses Impulse
                    stage += 1
                elif stage == 2:
                    aeonSummon(2)
                    tidusFlee()  # same pattern as Aerospark
                    stage += 1
                else:
                    attack('none')
            elif FFX_Screen.turnTidus():
                if stage == 0:
                    FFX_Xbox.lateHaste('down')
                    stage += 1
                elif stage == 3:
                    stage += 1
                    FFX_Xbox.menuDown()
                    FFX_Xbox.menuDown()
                    FFX_Xbox.menuDown()
                    FFX_Xbox.menuB()
                    time.sleep(0.5)
                    FFX_Xbox.menuB()
                    time.sleep(0.5)
                    FFX_Xbox.menuB()  # Haste self
                    time.sleep(0.5)
                elif stage == 4:
                    stage += 1
                    tidusOD()
                else:
                    attack('none')
            elif FFX_Screen.turnAuron():
                attack('none')
        else:
            FFX_Xbox.menuB()
    FFX_Logs.writeStats("Quick Flux")
    if stage == 1:
        FFX_Logs.writeStats("Yes")
        print("Quick Seymour Flux fight achieved. AKA Bahamut crit (end on Bahamut)")
    elif stage == 1:
        FFX_Logs.writeStats("Yes")
        print("Quick Seymour Flux fight achieved. AKA Bahamut crit (end on Ixion)")
    else:
        FFX_Logs.writeStats("No")
        print("No quick Seymour Flux fight this time.")
    FFX_memory.clickToControl()


def sKeeper():
    if FFX_memory.getBattleNum() == 355:
        print("Start of Sanctuary Keeper fight")
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
        FFX_Screen.clickToMap1()
        return 1
    else:
        fleeLateGame()
        return 0


def gagazetCave():
    FFX_Logs.writeLog("Fight start: Gagazet Cave")
    FFX_Xbox.menuB()
    time.sleep(1)

    if FFX_Screen.PixelTestTol(1380, 206, (153, 46, 10), 5):  # Ambush
        print("Ambushed, getting out of this fight")
        FFX_Xbox.menuA()
    elif FFX_Screen.PixelTestTol(272, 91, (225, 225, 225), 5):  # E1E1E1
        FFX_Xbox.menuRight()
        FFX_Xbox.menuB()
    elif FFX_Screen.PixelTestTol(254, 114, (154, 154, 154), 5):  # E1E1E1
        FFX_Xbox.menuLeft()
        FFX_Xbox.menuB()
    else:
        FFX_Xbox.menuA()
    fleeLateGame()


def useItem(slot, direction):
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
    if not FFX_memory.battleScreen():
        print("Battle menu isn't up.")
        return
    if FFX_memory.battleMenuCursor() != 0:
        while FFX_memory.battleMenuCursor() != 0:
            FFX_Xbox.menuUp()
            if FFX_Screen.BattleComplete():
                return
    if direction == 'none':
        print("Diag skipping to success.")
        FFX_Xbox.SkipDialog(1.1)
    else:
        print("Directional pattern.")
        while not FFX_memory.otherBattleMenu():
            FFX_Xbox.menuB()
            if FFX_Screen.BattleComplete():
                return
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
    while not FFX_Screen.BattleComplete():
        FFXC.set_value('BtnB', 1)
        time.sleep(0.035)
        FFXC.set_value('BtnB', 0)
        time.sleep(0.035)

def Steal():
    FFX_Logs.writeLog("Basic Steal command")
    print("Steal")
    while FFX_memory.battleMenuCursor() != 20:
        if FFX_memory.battleMenuCursor() == 255:
            time.sleep(0.01)
        elif FFX_memory.battleMenuCursor() == 0:
            FFX_Xbox.menuDown()
        else:
            FFX_Xbox.menuUp()
    FFX_Xbox.SkipDialog(1.5)

def StealDown():
    FFX_Logs.writeLog("Steal, but press Down")
    print("Steal Down")
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
    time.sleep(0.4)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.2)


def StealRight():
    FFX_Logs.writeLog("Steal, but press Right")
    print("Steal Right")
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
    time.sleep(0.4)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    time.sleep(0.2)


def StealLeft():
    FFX_Logs.writeLog("Steal, but press Left")
    print("Steal Left")
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
    time.sleep(0.4)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuB()
    time.sleep(0.2)


def stealAndAttack():
    BattleComplete = 0
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    while BattleComplete == 0:
        if FFX_memory.battleScreen():
            if FFX_Screen.turnRikku():
                Steal()
            if FFX_Screen.turnTidus():
                attack('none')
        if FFX_Screen.BattleComplete():
            FFXC.set_value('BtnB', 1)
            time.sleep(2.1)
            FFXC.set_value('BtnB', 0)
            BattleComplete = 1


def stealAndAttackPreTros():
    BattleComplete = 0
    turnCounter = 0
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    while BattleComplete == 0:
        if FFX_memory.battleScreen():
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
        if FFX_Screen.BattleComplete():
            FFXC.set_value('BtnB', 1)
            time.sleep(2.5)
            FFXC.set_value('BtnB', 0)
            BattleComplete = 1


def valeforFire():
    BattleComplete = 0
    while BattleComplete == 0:
        if FFX_memory.battleScreen():
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
    while FFX_memory.battleMenuCursor() != 23:
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
    FFX_Xbox.menuB()  # Cast whatever spell is chosen
    FFX_Xbox.menuB()  # Cast whatever spell is chosen
    FFX_Xbox.menuB()  # Cast whatever spell is chosen
    print("Aeon casting spell")
    time.sleep(0.2)


def aeonSpell2(position, direction):
    FFX_Logs.writeLog("Aeon casting a spell.")
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
    FFX_Logs.writeLog("Aeon casting a spell.")
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
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    if not FFX_memory.menuOpen():
        FFX_Screen.openMenu()

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
    while not FFX_Screen.MinimapAny():
        FFX_Xbox.menuA()


def healUp(chars):
    FFX_Logs.writeLog("Healing characters post-battle")
    print("Menuing, healing characters: ", chars)
    FFXC.set_value('AxisLy', 0)
    FFXC.set_value('AxisLx', 0)
    if not FFX_memory.menuOpen():
        FFX_Screen.openMenu()
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
    while not FFX_Screen.MinimapAny():
        FFX_Xbox.menuA()


def healUp2(chars):
    FFX_Logs.writeLog("Healing characters post-battle")
    print("Menuing, healing characters: ", chars)
    if not FFX_memory.menuOpen():
        FFX_Screen.openMenu()
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
    while not FFX_Screen.MinimapAny():
        FFX_Xbox.menuA()


def healUpNoCombat(chars):
    FFX_Logs.writeLog("Healing characters post-battle")
    print("Menuing, healing characters: ", chars)
    if FFX_memory.menuOpen() and FFX_memory.userControl() == False:
        FFX_memory.clickToControl() # After-battle screen is still open.
    FFX_Screen.openMenu()
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
    #FFX_Screen.clickToBattle()  # Just to get to the battle summary scene
    FFX_memory.clickToControl()
    # Now to recover the formation
    FFX_memory.openMenu()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    if swapPos == 2:
        FFX_Xbox.menuB()  # Tidus to 1, Kimahri to 2
        FFX_Xbox.menuB()
        FFX_Xbox.menuDown()
    elif swapPos == 3:
        FFX_Xbox.menuDown()
        FFX_Xbox.menuB()  # Tidus to 1, Kimahri to 3
        FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()  # Kimahri to 4, Wakka to 2 or Auron to 3
    FFX_memory.closeMenu()


def lancetSwapDjose(direction):
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
    FFX_memory.closeMenu()


def lancet(direction):
    print("Casting Lancet with variation: ", direction)
    while FFX_memory.battleMenuCursor() != 20:
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


def lancetHome(direction):
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

def fleeAll():
    FFX_Logs.writeLog("Fleeing from battle, prior to Mt Gagazet")
    print("Attempting escape (all party members and end screen)")
    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
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
        if FFX_memory.battleScreen():
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
    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
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
    FFX_Screen.clickToBattle()
    FFX_Screen.awaitTurn()


def buddySwap_new(position):
    FFX_Logs.writeLog("Swapping characters (in battle)")
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
    FFX_Screen.clickToBattle()
    FFX_Screen.awaitTurn()

def buddySwapTidus():
    FFX_Logs.writeLog("Swapping characters (in battle)")
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
            FFX_Xbox.menuB()
        elif FFX_memory.battleScreen():
            return False
    return True

def SinArms():
    FFX_Logs.writeLog("Fight start: Sin's Arms")
    # Area for improvement later. Multiple skippable FMVs
    FFX_Screen.clickToBattle()
    aeonSummon(4)

    FFX_Screen.awaitTurn()
    tidusFlee()

    while not FFX_Screen.BattleComplete():  # Arm 1
        if FFX_memory.battleScreen():
            tidusFlee()  # Impulse
            FFX_Xbox.SkipDialog(21)
            FFX_Xbox.skipScene()
        else:
            FFX_Xbox.menuB()
    wrapUp()

    FFX_Screen.awaitTurn()
    aeonSummon(4)

    while not FFX_Screen.BattleComplete():  # Arm 2
        if FFX_memory.battleScreen():
            tidusFlee()  # Impulse
        else:
            FFX_Xbox.menuB()

    # FFX_Xbox.SkipDialog(27) #Skip 1
    # FFX_Xbox.skipScene()
    # FFX_Xbox.SkipDialog(10)
    # FFX_Xbox.skipScene() #Skip two

    wrapUp()

    FFX_Screen.clickToBattle()
    aeonSummon(4)
    FFX_Screen.awaitTurn()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuB()  # Impulse on Core

    time.sleep(29)
    FFX_Xbox.skipScene()  # Skip the falling scene

def SinFace():
    FFX_Logs.writeLog("Fight start: Sin's Face")
    FFX_Screen.clickToBattle()
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    complete = 0
    while complete == 0:
        if FFX_memory.battleScreen():
            if FFX_Screen.turnYuna():
                aeonSummon(4)
                FFX_Screen.awaitTurn()
                tidusFlee() # Impulse
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
    FFX_Screen.clickToBattle()
    defend()

    FFX_Screen.awaitTurn()
    print("Going for armor break.")
    useSkill(0)

    FFX_Screen.awaitTurn()
    if FFX_memory.getEnemyMaxHP()[0] == FFX_memory.getEnemyCurrentHP()[0]:
        print("Missing on armor break is stupid. Don't worry, I can 'fix' this.")
        FFX_memory.setEnemyCurrentHP(0,20)
    print("Ready for next step.")
    while not FFX_Screen.BattleComplete():
        if FFX_memory.battleScreen():
            print("Character turn: ",FFX_memory.getBattleCharTurn())
            if FFX_Screen.turnYuna():
                aeonSummon(4)
            elif FFX_Screen.turnAeon():
                attack2()
            else:
                defend()
        elif FFX_memory.diagSkipPossible():
            print("Skipping dialog maybe?")
            FFX_Xbox.menuB()
    print("Should be done now.")
    FFX_memory.clickToControl()

def BFA():
    FFX_Logs.writeLog("Fight start: BFA and final boss")
    FFX_Screen.clickToBattle()
    buddySwap(2)
    tidusFlee()  # Armor break

    FFX_Screen.awaitTurn()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuLeft()
    time.sleep(0.8)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()

    FFX_Screen.clickToBattle()
    buddySwap(2)
    aeonSummon(4)

    FFX_Screen.awaitTurn()
    attack('none')

    FFX_Screen.clickToBattle()
    attack2()  # Finishes off BFA
    print("This will finish BFA. Next to skip the crying scene.")

    time.sleep(77.7)  # Need to dial in
    print("Skip, mark!")
    FFX_Xbox.skipScene()

    print("BFA down. Ready for Aeons")
    while FFX_memory.getStoryProgress() < 3380:
        if FFX_memory.battleScreen():
            battleNum = FFX_memory.getBattleNum()
            print("Battle engaged. Battle number: ", battleNum)
            FFX_Xbox.menuDown()
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
        else:
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
        if FFX_memory.battleScreen():
            if zombieAttack == 1:
                pDownSlot = FFX_memory.getThrowItemsSlot(6)
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                time.sleep(0.8)
                if pDownSlot != 1:
                    while pDownSlot != 1:
                        if pDownSlot % 2 == 0:
                            FFX_Xbox.menuRight()
                            pDownSlot -= 1
                        else:
                            FFX_Xbox.menuDown()
                            pDownSlot -= 2
                FFX_Xbox.menuB()
                time.sleep(0.1)
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
                print("Phoenix Down on Yu Yevon. Good game.")
            elif FFX_Screen.turnTidus():
                time.sleep(0.3)
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                time.sleep(0.5)
                FFX_Xbox.menuB()
                time.sleep(0.5)
                FFX_Xbox.menuB()
                time.sleep(0.5)
                zombieAttack = 1
            else:
                defend()
        story = FFX_memory.getStoryProgress()

def BFA_TASonly(finalHit):
    FFX_Logs.writeLog("Fight start: BFA and final boss")
    FFX_Screen.clickToBattle()
    FFX_memory.setEnemyCurrentHP(0, 10)
    attack('none')
    
    FFX_Screen.awaitTurn()
    FFX_memory.setEnemyCurrentHP(0, 10)
    attack('none')
    
    while FFX_Screen.BattleComplete == False:
        time.sleep(0.035)
    time.sleep(77.7)
    print("Mark")
    FFX_Xbox.skipScene()
    
    FFX_Screen.clickToBattle()
    print("The final hit will be performed by ", FFX_memory.nameFromNumber(finalHit))
    print("The final hit will be performed by ", FFX_memory.nameFromNumber(finalHit))
    print("The final hit will be performed by ", FFX_memory.nameFromNumber(finalHit))
    if finalHit != 0: #Tidus
        if finalHit == 1: #Yuna
            while not FFX_Screen.turnYuna():
                defend()
        elif finalHit == 2: #Auron
            while not FFX_Screen.turnAuron():
                defend()
        elif finalHit == 3: #Kimahri
            buddySwap(2)
        elif finalHit == 4: #Wakka
            buddySwap(1)
        elif finalHit == 5: #Lulu
            buddySwap(3)
        elif finalHit == 6: #Mystery Girl
            buddySwap(0)
        time.sleep(0.5)
    FFX_Screen.awaitTurn()
    FFX_memory.setEnemyCurrentHP(0, 3)
    attack('none')
    
def oldYYTasLogic():
    # Yu Yevon
    story = FFX_memory.getStoryProgress()
    while story < 3400:
        if FFX_memory.battleScreen():
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
