import FFX_Xbox
import FFX_Screen
import time
import FFX_Logs
import FFX_memory
import random
import FFX_vars
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

def tapTargeting():
    print("In Tap Targeting", not FFX_memory.mainBattleMenu(), FFX_memory.battleActive())
    while (not FFX_memory.mainBattleMenu()) and FFX_memory.battleActive():
        FFX_Xbox.tapB()
    print("Done", not FFX_memory.mainBattleMenu(), FFX_memory.battleActive())

def valeforOD(sinFin = 0, version = 0):
    FFX_memory.waitFrames(6)
    while FFX_memory.mainBattleMenu():
        FFX_Xbox.tapLeft()
    print("Overdrive: ", version)
    if version == 1:
        while FFX_memory.battleCursor2() != 1:
            FFX_Xbox.tapDown()
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()  # Energy Blast
    if sinFin == 1:
        FFX_Xbox.tapDown()
        FFX_Xbox.tapLeft()
    tapTargeting()

def defend():
    print("Defend command")
    for _ in range(5):
        FFX_Xbox.tapY()


def tidusFlee():
    if FFX_memory.battleActive():
        print("Tidus Flee (or similar command pattern)")
        while FFX_memory.battleMenuCursor() != 20:
            if FFX_memory.battleMenuCursor() == 255:
                FFX_Xbox.tapUp()
            elif FFX_memory.battleMenuCursor() == 1:
                FFX_Xbox.tapUp()
            elif FFX_memory.battleMenuCursor() > 20:
                FFX_Xbox.tapUp()
            else:
                FFX_Xbox.tapDown()
            if FFX_memory.otherBattleMenu():
                FFX_Xbox.tapA()
        print("Out")
        while not FFX_memory.otherBattleMenu():
            FFX_Xbox.tapB()
        _navigate_to_position(0)
        while FFX_memory.otherBattleMenu():
            FFX_Xbox.tapB()
        tapTargeting()

def tidusHaste(direction, character=255):
    direction = direction.lower()
    while FFX_memory.battleMenuCursor() != 22:
        if FFX_Screen.turnTidus() == False:
            print("Attempting Haste, but it's not Tidus's turn")
            FFX_Xbox.tapUp()
            FFX_Xbox.tapUp()
            return
        if FFX_memory.battleMenuCursor() == 1:
            FFX_Xbox.tapUp()
        else:
            FFX_Xbox.tapDown()
    while not FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    _navigate_to_position(0)
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    if character != 255:
        direction = 'l'
        while character != FFX_memory.battleTargetId():
            if direction == 'l':
                FFX_Xbox.tapLeft()
                if FFX_memory.battleTargetId() >= 20:
                    FFX_Xbox.tapRight()
                    direction = 'd'
            else:
                FFX_Xbox.tapDown()
                if FFX_memory.battleTargetId() >= 20:
                    FFX_Xbox.tapUp()
                    direction = 'l'
    elif direction == 'left':
        FFX_Xbox.tapLeft()
    elif direction == 'right':
        FFX_Xbox.tapRight()
    elif direction == 'up':
        FFX_Xbox.tapUp()
    elif direction == 'down':
        FFX_Xbox.tapDown()
    tapTargeting()

def tidusHasteLate(direction):
    tidusHaste(direction)

def lateHaste(direction):
    tidusHaste(direction)

def useSkill(position):
    print("Using skill in position: ", position)
    while FFX_memory.battleMenuCursor() != 19:
        print(FFX_memory.battleMenuCursor())
        if FFX_memory.battleMenuCursor() == 255:
            pass
        elif FFX_memory.battleMenuCursor() == 1:
            FFX_Xbox.tapUp()
        elif FFX_memory.battleMenuCursor() > 19:
            FFX_Xbox.tapUp()
        else:
            FFX_Xbox.tapDown()
    while not FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    _navigate_to_position(position)
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    tapTargeting()

def useSpecial(position, target:int=20, direction:int='u'):
    print("Using skill in position: ", position)
    while FFX_memory.battleMenuCursor() != 20:
        print(FFX_memory.battleMenuCursor())
        if FFX_memory.battleMenuCursor() == 255:
            pass
        elif FFX_memory.battleMenuCursor() == 1:
            FFX_Xbox.tapUp()
        elif FFX_memory.battleMenuCursor() > 20:
            FFX_Xbox.tapUp()
        else:
            FFX_Xbox.tapDown()
    while not FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    _navigate_to_position(position)
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    
    if FFX_memory.battleTargetId() != target:
        while FFX_memory.battleTargetId() != target:
            if direction == 'r':
                FFX_Xbox.tapRight()
                if FFX_memory.battleTargetId() < 20:
                    FFX_Xbox.tapLeft()
                    direction = 'u'
            else:
                FFX_Xbox.tapUp()
                if FFX_memory.battleTargetId() < 20:
                    FFX_Xbox.tapDown()
                    direction = 'r'
    tapTargeting()

def wakkaOD():
    print("Wakka overdrive activating")
    while not FFX_memory.otherBattleMenu():
        FFX_Xbox.tapLeft()
    FFX_Xbox.SkipDialog(2)
    
    FFX_memory.waitFrames(30 * 3) #Replace with memory reading later.
    FFX_Xbox.SkipDialog(4)


def auronOD(style="dragon fang"):
    while not FFX_memory.otherBattleMenu():
        FFX_Xbox.tapLeft()
    while not FFX_memory.interiorBattleMenu():
        FFX_Xbox.tapB()
    print("Style: ", style)
    #Doing the actual overdrive
    if style == "dragon fang":
        _navigate_to_position(0, battleCursor=FFX_memory.battleCursor3)        
        while not FFX_memory.auronOverdriveActive():
            FFX_Xbox.tapB()
        print("Starting")
        FFX_Xbox.tapDown()
        FFX_Xbox.tapLeft()
        FFX_Xbox.tapUp()
        FFX_Xbox.tapRight()
        FFX_Xbox.shoulderLeft()
        FFX_Xbox.shoulderRight()
        FFX_Xbox.tapA()
        FFX_Xbox.tapB()
    elif style == "shooting star":
        _navigate_to_position(1, battleCursor=FFX_memory.battleCursor3)        
        while not FFX_memory.auronOverdriveActive():
            FFX_Xbox.tapB()
        FFX_Xbox.tapY()
        FFX_Xbox.tapA()
        FFX_Xbox.tapX()
        FFX_Xbox.tapB()
        FFX_Xbox.tapLeft()
        FFX_Xbox.tapRight()
        FFX_Xbox.tapB()

def tidusOD(direction = None,version:int=0):
    print("Tidus overdrive activating")
    while not FFX_memory.otherBattleMenu():
        FFX_Xbox.tapLeft()
    while not FFX_memory.interiorBattleMenu():
        FFX_Xbox.tapB()
    if version == 1:
        FFX_memory.waitFrames(6)
        FFX_Xbox.menuRight()
    while FFX_memory.interiorBattleMenu():
        FFX_Xbox.tapB()
    if direction:
        if direction == 'left':
            FFX_Xbox.tapLeft()
    while not FFX_memory.overdriveMenuActive():
        FFX_Xbox.tapB()
    FFX_memory.waitFrames(12)
    print("Hit Overdrive")
    FFX_Xbox.tapB() #First try pog
    FFX_memory.waitFrames(8)
    FFX_Xbox.tapB() #Extra attempt in case of miss
    FFX_memory.waitFrames(9)
    FFX_Xbox.tapB() #Extra attempt in case of miss
    FFX_memory.waitFrames(10)
    FFX_Xbox.tapB() #Extra attempt in case of miss
    FFX_memory.waitFrames(11)
    FFX_Xbox.tapB() #Extra attempt in case of miss
    FFX_memory.waitFrames(12)
    FFX_Xbox.tapB() #Extra attempt in case of miss


def tidusODSeymour():
    print("Tidus overdrive activating")
    FFX_Screen.awaitTurn()
    tidusOD('left')

def yunaOD(aeonNum:int=5):
    print("Awaiting Yuna's turn")
    while not FFX_Screen.turnYuna():
        if FFX_memory.turnReady():
            defend()
    while not FFX_memory.otherBattleMenu():
        FFX_Xbox.tapLeft()
    while not FFX_memory.interiorBattleMenu():
        FFX_Xbox.tapB()
    while not FFX_memory.battleCursor3() == aeonNum:
        if aeonNum > FFX_memory.battleCursor3():
            FFX_Xbox.tapDown()
        else:
            FFX_Xbox.tapUp()
        FFX_memory.waitFrames(2)
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()

def yojimboOD(gilValue:int=263000):
    print("Yojimbo overdrive")
    FFX_Screen.awaitTurn()
    if not FFX_Screen.turnAeon():
        return
    while FFX_memory.battleMenuCursor() != 35:
        FFX_Xbox.tapUp()
    FFX_memory.waitFrames(6)
    FFX_Xbox.menuB()
    print("Selecting amount")
    FFX_memory.waitFrames(15)
    #calculateSpareChangeMovement(263000)
    #Calculate function not working
    FFX_Xbox.tapLeft()
    FFX_Xbox.tapLeft()
    FFX_Xbox.tapLeft()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapLeft()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapLeft()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    print("Amount selected")
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    return

def remedy(character: int, direction: str):
    print("Remedy")
    if FFX_memory.getThrowItemsSlot(15) < 250:
        itemnum = 15
        itemname = "Remedy"
    else:
        itemnum = -1
        itemname = "noitemfound"
    if itemnum > 0:
        _useHealingItem(character, direction, itemnum)
        return 1
    else:
        print("No restorative items available")
        return 0

def revive(itemNum = 6):
    print("Using Phoenix Down")
    if FFX_memory.getThrowItemsSlot(itemNum) > 250:
        attack('none')
        return
    while not FFX_memory.mainBattleMenu():
        pass
    while FFX_memory.battleMenuCursor() != 1:
        FFX_Xbox.tapDown()
    while FFX_memory.mainBattleMenu():
        FFX_Xbox.tapB()
    itemPos = FFX_memory.getThrowItemsSlot(itemNum)
    _navigate_to_position(itemPos)
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    tapTargeting()

def reviveTarget(itemNum = 6, target = 0):
    direction = 'l'
    print("Using Phoenix Down")
    if FFX_memory.getThrowItemsSlot(itemNum) > 250:
        fleeAll()
        return
    while not FFX_memory.mainBattleMenu():
        pass
    while FFX_memory.battleMenuCursor() != 1:
        FFX_Xbox.tapDown()
    while FFX_memory.mainBattleMenu():
        FFX_Xbox.tapB()
    itemPos = FFX_memory.getThrowItemsSlot(itemNum)
    _navigate_to_position(itemPos)
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    
    #Select target - default to Tidus
    if FFX_memory.battleTargetId() != 0:
        while FFX_memory.battleTargetId() != 0:
            if direction == 'l':
                FFX_Xbox.tapLeft()
                if FFX_memory.battleTargetId() >= 20:
                    FFX_Xbox.tapRight()
                    direction = 'u'
            else:
                FFX_Xbox.tapUp()
                if FFX_memory.battleTargetId() >= 20:
                    FFX_Xbox.tapDown()
                    direction = 'l'
    tapTargeting()


def reviveAll():
    revive(itemNum=7)

def selfPot():
    print("Self potion")
    FFX_Xbox.tapDown()
    FFX_Xbox.tapDown()
    FFX_Xbox.tapDown()
    FFX_Xbox.tapB()
    FFX_Xbox.SkipDialog(2)

def Ammes():
    FFX_Logs.writeLog("Fight start: Ammes")
    BattleComplete = 0
    countAttacks = 0
    countRevives = 0
    
    tidusODflag = False

    while BattleComplete != 1:
        if FFX_memory.turnReady():
            if tidusODflag == False and FFX_Screen.turnTidus() and FFX_memory.getOverdriveBattle(0) == 100:
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
                else:
                    attack('none')
                    countAttacks += 1
            elif FFX_Screen.turnAuron():
                auronCount += 1
                if auronCount < 2:
                    attackSelfTanker()
                else:
                    attack('none')
                    countAttacks += 1
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
    FFX_Logs.writeStats("Tanker Attacks:")
    FFX_Logs.writeStats(str(countAttacks))

def Klikk():
    print("Fight start: Klikk")
    klikkAttacks = 0
    klikkRevives = 0
    while not FFX_memory.battleComplete(): #AKA end of battle screen
        if FFX_memory.turnReady():
            BattleHP = FFX_memory.getBattleHP()
            if BattleHP[0] == 0:
                revive()
                klikkRevives += 1
            elif FFX_Screen.turnTidus():
                if BattleHP[0] == 0 and FFX_memory.getEnemyCurrentHP()[0] > 125:
                    usePotionCharacter(0, 'l')
                else:
                    attack('none')
                klikkAttacks += 1
            elif FFX_Screen.turnRikku():
                grenadeCount = FFX_memory.getItemCountSlot(FFX_memory.getItemSlot(35))
                if BattleHP[0] < 120 and not (FFX_memory.getNextTurn() == 0 and FFX_memory.getEnemyCurrentHP()[0] <= 181):
                    usePotionCharacter(0, 'l')
                    klikkRevives += 1  
                elif grenadeCount < 3:
                    print("Attempting to steal from Klikk")
                    Steal()
                elif FFX_memory.rngSeed() == 160 and grenadeCount < 4:
                    print("Attempting to steal from Klikk")
                    Steal()
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
    FFXC = FFX_Xbox.controllerHandle()
    if gameVars.csr():
        while not FFX_memory.menuOpen():
            FFX_Xbox.tapB()
        FFXC.set_value('BtnB', 1)
        FFX_memory.waitFrames(150) #Dial in further. Necessary to avoid save dialog.
        FFXC.set_neutral()
    else:
        FFX_memory.clickToControl()  # Maybe not skippable dialog, but whatever.

def Tros():
    FFXC = FFX_Xbox.controllerHandle()
    FFX_Logs.writeLog("Fight start: Tros")
    print("Fight start: Tros")
    FFXC.set_neutral()
    battleClock = 0
    Attacks = 0
    Revives = 0
    Grenades = 0
    Steals = 0
    
    while FFX_memory.battleActive(): #AKA end of battle screen
        if FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
        elif FFX_memory.turnReady():
            battleClock += 1
            print("Battle clock:", battleClock)
            trosPos = 2
            print("Determining Tros position")
            while trosPos == 2 and not FFX_memory.battleComplete():
                # Two for "not yet determined". Maybe can be HP-based instead?
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
            
            #Assuming battle is not complete:
            if FFX_memory.battleActive():
                partyHP = FFX_memory.getBattleHP()
                if partyHP[0] == 0 or partyHP[1] == 0:  # Someone requires reviving.
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
                    if trosPos == 1 and FFX_memory.getBattleHP()[1] < 200 and FFX_memory.getEnemyCurrentHP()[0] > 800:
                        usePotionCharacter(6, 'l')
                    elif trosPos == 1:
                        defend()
                    else:
                        attack('none')
                        Attacks += 1
    
    print("Tros battle complete.")
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
    print("#########Seed: ", FFX_memory.rngSeed())
    #11 = two pirhanas
    #12 = three pirhanas with one being a triple formation (takes two hits)
    #13 = four pirhanas
    
    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            if FFX_memory.rngSeed() == 105:
                attack('none')
            elif battleNum == 11 or (battleNum == 12 and FFX_memory.battleType() == 1):
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
                buddySwapWakka()
            elif FFX_Screen.turnLulu():
                thunderTarget(22, 'l')
            elif FFX_Screen.turnWakka():
                attackByNum(20, direction='r')
            elif FFX_Screen.turnTidus():
                attackByNum(21, direction='r')

    FFX_memory.clickToControl()


def SinFin():
    FFX_Logs.writeLog("Fight start: Sin's Fin")
    print("Fight start: Sin's Fin")
    FFX_Screen.awaitTurn()
    finTurns = 0
    kimTurn = False
    complete = False
    while complete == False:
        if FFX_memory.turnReady():
            finTurns += 1
            print("Determining first turn.")
            if FFX_Screen.turnTidus():
                defend()
                print("Tidus defend")
            elif FFX_Screen.turnYuna():
                buddySwapLulu() # Yuna out, Lulu in
                thunderTarget(target=23, direction='r')
            elif FFX_Screen.turnKimahri():
                lancetTarget(target=23, direction='r')
                kimTurn = True
            elif FFX_Screen.turnLulu():
                thunderTarget(target=23, direction='r')
            else:
                defend()
        if finTurns >= 3 and kimTurn == True:
            complete = True

    print("First few turns are complete. Now for the rest of the fight.")
    # After the first two turns, the rest of the fight is pretty much scripted.
    turnCounter = 0
    while not FFX_memory.battleComplete():
        if FFX_memory.turnReady():
            turnCounter += 1
            if FFX_Screen.turnKimahri():
                FFX_Screen.awaitTurn()
                lancetTarget(23, 'r')
            elif FFX_Screen.turnLulu():
                thunderTarget(23, 'r')
            elif FFX_Screen.turnTidus():
                if turnCounter < 4:
                    defend()
                    FFX_memory.waitFrames(30 * 0.2)
                else:
                    buddySwapYuna()
                    aeonSummon(0)
            elif FFX_Screen.turnAeon():
                valeforOD(sinFin = 1)
                print("Valefor energy blast")
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
                elif FFX_memory.getOverdriveBattle(0) == 100 and FFX_memory.getEnemyCurrentHP()[0] <= 558:
                    print("Overdrive")
                    tidusOD()
                else:
                    print("Tidus attack")
                    attack('none')
            elif FFX_Screen.turnWakka():
                if tidusCounter == 1 and FFX_memory.rngSeed() != 160:
                    print("Dark Attack")
                    useSkill(0)  #Dark Attack
                elif FFX_memory.getEnemyCurrentHP()[0] <= 558:
                    print("Ready for Tidus Overdrive. Wakka defends.")
                    defend()
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
                buddySwapYuna()
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
    
    FFXC.set_neutral()

    # if bNum == 31: #Lizard and Elemental, side
    # elif bNum == 32: #Lizard and Bee, front
    # elif bNum == 33: #Yellow and Bee, front
    # elif bNum == 34: #Lizard, Yellow, and Bee, front
    # elif bNum == 35: #Single Ragora, reverse
    # elif bNum == 36: #Two Ragoras, reverse
    # elif bNum == 37: #Ragora and two bees, reverse

    # These battles we want nothing to do with.
    if bNum == 32 or bNum == 36:
        skipCharge = True

    print("Kilika battle")
    aeonTurn = False
    yunaWent = False
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
                elif FFX_Screen.turnKimahri() or FFX_Screen.turnLulu():
                    if FFX_memory.getBattleCharSlot(4) >= 3:
                        buddySwapWakka()
                    elif FFX_memory.getBattleCharSlot(0) >= 3:
                        buddySwapTidus()
                    else:
                        buddySwapYuna()
                elif bNum == 31:  # Working just fine.
                    print("Logic for battle number 31")
                    currentCharge = True
                    if FFX_Screen.turnTidus():
                        attack('none')
                    elif FFX_Screen.turnYuna():
                        aeonSummon(0)
                        FFX_Screen.awaitTurn()
                        if aeonTurn == False:
                            aeonTurn = True
                            if FFX_memory.getNextTurn() < 20:
                                aeonShield()
                        aeonBoost()
                        FFX_Screen.awaitTurn()
                        aeonBoost()
                        FFX_Screen.awaitTurn()
                        aeonSpell(2)
                    elif FFX_Screen.turnAeon():
                        aeonSpellDirection(2, 'right')
                    else:
                        defend()
                elif bNum == 33:
                    print("Logic for battle number 33")
                    currentCharge = True
                    if FFX_Screen.turnYuna():
                        
                        aeonSummon(0)
                        FFX_Screen.awaitTurn()
                        if aeonTurn == False:
                            aeonTurn = True
                            if FFX_memory.getNextTurn() < 20:
                                aeonShield()
                        aeonBoost()
                        FFX_Screen.awaitTurn()
                        aeonSpellDirection(1, 'left')
                    elif FFX_Screen.turnAeon():
                        aeonSpell(2)
                        #valeforCharge = True
                    else:
                        defend()
                
                elif bNum == 34:
                    print("Logic for battle number 34")
                    currentCharge = True
                    if FFX_Screen.turnTidus():
                        attack('none')
                    elif FFX_Screen.turnYuna():
                        aeonSummon(0)
                        FFX_Screen.awaitTurn()
                        if aeonTurn == False:
                            aeonTurn = True
                            if FFX_memory.getNextTurn() < 20:
                                aeonShield()
                        aeonBoost()
                        FFX_Screen.awaitTurn()
                        aeonSpellDirection(1, 'right')
                    elif FFX_Screen.turnAeon():
                        aeonSpell2(2, 'left')
                    else:
                        defend()
                elif bNum == 35:
                    print("Logic for battle number 35")
                    currentCharge = True
                    if FFX_Screen.turnTidus():
                        defend()
                    elif FFX_Screen.turnYuna():
                        aeonSummon(0)
                        FFX_Screen.awaitTurn()
                        if aeonTurn == False:
                            aeonTurn = True
                            if FFX_memory.getNextTurn() < 20:
                                aeonShield()
                        aeonBoost()
                        FFX_Screen.awaitTurn()
                        sonicWings()
                        FFX_Screen.awaitTurn()
                        aeonSpell(0)
                    elif FFX_Screen.turnAeon():
                        aeonSpell(0)
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
                        if aeonTurn == False:
                            aeonTurn = True
                            if FFX_memory.getNextTurn() < 20:
                                aeonShield()
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
                    if FFX_memory.getBattleCharSlot(4) >= 3:
                        buddySwapWakka()
                    elif FFX_memory.getBattleCharSlot(0) >= 3:
                        buddySwapTidus()
                    else:
                        buddySwapYuna()
                elif FFX_Screen.turnLulu() and bNum != 37:
                    if FFX_memory.getBattleCharSlot(4) >= 3:
                        buddySwapWakka()
                    elif FFX_memory.getBattleCharSlot(0) >= 3:
                        buddySwapTidus()
                    else:
                        buddySwapYuna()
                elif bNum == 31:
                    if FFX_Screen.turnTidus():
                        if turnCounter < 4:
                            attack('none')
                        else:
                            fleeAll()
                    else:
                        defend()
                elif bNum == 32:
                    if FFX_Screen.turnTidus():
                        if turnCounter < 4:
                            attack('none')
                        else:
                            fleeAll()
                    elif FFX_Screen.turnWakka():
                        attackByNum(21,'r')
                    else:
                        defend()
                elif bNum == 33:
                    if FFX_Screen.turnTidus():
                        if turnCounter < 4:
                            defend()
                        else:
                            fleeAll()
                    elif FFX_Screen.turnWakka():
                        attackByNum(21,'r')
                    else:
                        defend()
                elif bNum == 34:
                    if FFX_Screen.turnTidus():
                        if turnCounter < 4:
                            attack('none')
                        else:
                            fleeAll()
                    elif FFX_Screen.turnWakka():
                        attackByNum(22,'r')
                    else:
                        defend()
                elif bNum == 35 or bNum == 36:
                    fleeAll()
                elif bNum == 37:
                    if FFX_Screen.turnWakka() and FFX_memory.getEnemyCurrentHP()[2] != 0:
                        attackByNum(22, 'l')
                    elif FFX_Screen.turnYuna() and not yunaWent:
                        yunaWent = True
                        defend()
                    elif yunaWent:
                        fleeAll()
                    else:
                        defend()

    FFX_memory.clickToControl()  # Rewards screen
    hpCheck = FFX_memory.getHP()
    if hpCheck[0] < 250 or hpCheck[1] < 250 or hpCheck[4] < 250:
        healUp(3)
    else:
        print("No need to heal up. Moving onward.")
    if valeforCharge == False and FFX_memory.overdriveState()[8] == 20:
        valeforCharge = True
    print("Returning Valefor Charge value: ", valeforCharge)
    return valeforCharge

def sonicWings():
    print("Valefor attempting to use Sonic Wings - 1")
    while FFX_memory.battleMenuCursor() != 204:
        if FFX_memory.battleMenuCursor() == 203:
            FFX_Xbox.tapDown()
        else:
            FFX_Xbox.tapUp()
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    print("Valefor attempting to use Sonic Wings - 2")
    

def Geneaux():
    FFX_Logs.writeLog("Fight start: Sinspawn Geneaux")
    print("Fight start: Sinspawn Geneaux")
    FFX_Xbox.clickToBattle()
    
    if FFX_Screen.turnTidus():
        attack('none')
    elif FFX_Screen.turnYuna():
        buddySwapKimahri()
        attack('none')
        while not FFX_Screen.turnTidus():
            defend()
        while FFX_Screen.turnTidus():
            defend()
        buddySwapYuna()
    FFX_Screen.awaitTurn()
    aeonSummon(0) # Summon Valefor
    FFX_Screen.awaitTurn()
    valeforOD()

    skipCount = 0
    while FFX_memory.battleComplete() == False: #AKA end of battle screen
        if FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
        elif FFX_memory.turnReady():
            print("Valefor casting Fire")
            aeonSpell(0)
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
            FFX_Xbox.tapB()  # Clicking to get through the battle faster
    FFX_memory.clickToControl()


def LucaWorkers2(earlyHaste):
    FFX_Logs.writeLog("Fight start: Workers in Luca")
    print("Fight start: Workers in Luca")
    hasted = False
    FFX_Xbox.clickToBattle()

    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            if earlyHaste >= 1:
                if FFX_Screen.turnTidus() and not hasted:
                    tidusHaste('left', character=5)
                    hasted = True
                elif FFX_Screen.turnLulu():
                    thunder('none')
                else:
                    defend()
            elif FFX_memory.lucaWorkersBattleID() in [44, 35]:
                if FFX_Screen.turnTidus():
                    attack('none')
                elif FFX_Screen.turnKimahri():
                    if FFX_memory.getEnemyCurrentHP().count(0) == 1 and FFX_memory.getOverdriveBattle(3) == 100 and FFX_memory.getEnemyCurrentHP()[0] > 80:
                        kimahriOD(1)
                    else:
                        attack('none')
                elif FFX_Screen.turnLulu():
                    thunder('right')
            else:
                if FFX_Screen.turnLulu():
                    thunder('none')
                else:
                    defend()
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()  # Clicking to get through the battle faster
    FFX_memory.clickToControl()

def Oblitzerator(earlyHaste):
    FFX_Logs.writeLog("Fight start: Oblitzerator")
    print("Fight start: Oblitzerator")
    FFX_Xbox.clickToBattle()
    crane = 0

    if earlyHaste >= 1:
        #First turn is always Tidus. Haste Lulu if we've got the levels.
        tidusHaste(direction='left', character=5)

    while not FFX_memory.battleComplete(): #AKA end of battle screen
        if FFX_memory.turnReady():
            if crane < 3:
                if FFX_Screen.turnLulu():
                    crane += 1
                    if crane == 1:
                        thunder('right')
                    else:
                        thunder('none')
                else:
                    defend()
            elif crane == 3:
                if FFX_Screen.turnTidus():
                    crane += 1
                    while FFX_memory.mainBattleMenu():
                        FFX_Xbox.tapLeft()
                    while FFX_memory.battleCursor2() != 1:
                        FFX_Xbox.tapDown()
                    while FFX_memory.otherBattleMenu():
                        FFX_Xbox.tapB()
                    tapTargeting()
                elif FFX_Screen.turnLulu():
                    thunder('none')
                else:
                    defend()
            else:
                if FFX_Screen.turnLulu():
                    thunder('none')
                elif FFX_Screen.turnTidus():
                    attackOblitzEnd()
                else:
                    defend()
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
        #else:
            #print("Waiting for turn, Oblitzerator fight")
    print("End of fight, Oblitzerator")
    FFX_memory.clickToControl()
    FFX_Logs.writeStats("RNG02 after battle:")
    FFX_Logs.writeStats(FFX_memory.rng02())

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
                    attackByNum(22, 'l')
                elif hpValues[1] < 200: #Tidus HP
                    usePotionCharacter(0, 'u')
                elif hpValues[0] < 100: #Wakka HP
                    usePotionCharacter(4, 'u')
                #elif gameVars.getLStrike() >= 2:
                #    attack('none')
                else:
                    defend()

def afterBlitz3(earlyHaste):
    print("Ready to take on Zu")
    print(earlyHaste)
    # Wakka dark attack, or Auron power break
    FFX_Screen.awaitTurn()
    tidusTurn = 0
    darkAttack = False
    while FFX_memory.battleActive():
        hpValues = FFX_memory.getBattleHP()
        if FFX_Screen.turnAuron():
            attack('none')
        elif FFX_Screen.turnTidus():
            if tidusTurn == 0:
                tidusHaste('d',character=2)
                tidusTurn += 1
            elif tidusTurn == 1:
                attack('none')
                tidusTurn += 1
            elif hpValues[0] < 202:
                usePotionCharacter(2, 'u')
            else:
                attack('none')
                #defend()
        elif FFX_Screen.turnWakka():
            if hpValues[0] < 202:
                usePotionCharacter(2, 'u')
            elif hpValues[1] < 312 and tidusTurn < 2:
                usePotionCharacter(0, 'u')
            elif not darkAttack:
                useSkill(0)
                darkAttack = True
            else:
                defend()
    FFXC.set_value('BtnB', 1)
    FFX_memory.waitFrames(30 * 4)
    FFXC.set_value('BtnB', 0)
    print("Battle complete (Garuda)")
    #Get to control
    while not FFX_memory.userControl():
        if FFX_memory.cutsceneSkipPossible():
            while not FFX_memory.diagProgressFlag() == 1:
                if FFX_memory.cutsceneSkipPossible():
                    FFX_Xbox.skipScene()
            if gameVars.csr():
                FFX_memory.waitFrames(60)
            else:
                FFX_Xbox.awaitSave(index=1)
        elif FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
            FFX_Xbox.tapB()

def afterBlitz3LateHaste(earlyHaste):
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

    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            if FFX_Screen.faintCheck() > 0:
                revive()
            else:
                attack('none')
    FFXC.set_value('BtnB', 1)
    FFX_memory.waitFrames(30 * 4)
    FFXC.set_value('BtnB', 0)
    print("Battle complete (Garuda)")
    #Get to control
    while not FFX_memory.userControl():
        if FFX_memory.cutsceneSkipPossible():
            while not FFX_memory.diagProgressFlag() == 1:
                if FFX_memory.cutsceneSkipPossible():
                    FFX_Xbox.skipScene()
            if gameVars.csr():
                FFX_memory.waitFrames(60)
            else:
                FFX_Xbox.awaitSave(index=1)
        elif FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
            FFX_Xbox.tapB()


def MiihenRoad(selfDestruct=False):
    FFX_Logs.writeLog("Fight start: Mi'ihen Road")
    print("Fight start: Mi'ihen Road")
    battle = FFX_memory.getBattleNum()
    
    while not FFX_memory.battleComplete(): #AKA end of battle screen
        if FFX_memory.battleType() == 2 and not checkTidusOk():
            print("Looks like we got ambushed. Skipping this battle.")
            fleeAll()
            break
        if FFX_memory.turnReady():
            if FFX_Screen.turnTidus():
                print("Mi'ihen battle. Self-destruct: ", gameVars.selfDestructGet())
                if not gameVars.selfDestructGet():
                    if battle == 51 or battle == 64 or battle == 66 or battle == 87:
                        lancetSwap('none')
                        gameVars.selfDestructLearned()
                        break
                    elif battle == 65 or battle == 84:
                        lancetSwap('right')
                        gameVars.selfDestructLearned()
                        break
                    else:
                        fleeAll()
                else:
                    fleeAll()
            else:
                fleeAll()
    
    FFXC.set_movement(0, 1)
    while not FFX_memory.userControl():
        FFXC.set_value('BtnB',1)
        FFX_memory.waitFrames(2)
        FFXC.set_value('BtnB',0)
        FFX_memory.waitFrames(3)
    hpCheck = FFX_memory.getHP()
    print("------------------ HP check: ", hpCheck)
    if hpCheck[0] < 520 or hpCheck[2] < 900 or hpCheck[4] < 800:
        FFX_memory.fullPartyFormat('miihen', fullMenuClose=False)
        healUp()
    else:
        print("No need to heal up. Moving onward.")
        FFX_memory.fullPartyFormat('miihen')
    
    print("selfDestruct flag: ",gameVars.selfDestructGet())


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
            elif FFX_memory.getNextTurn() >= 20 and FFX_memory.getBattleHP()[FFX_memory.getBattleCharSlot(2)] == 0:
                print("Special defend to avoid soft lock")
                FFX_memory.waitFrames(90)
                defend()
            else:
                print("Attempting defend")
                defend()
        elif FFX_memory.diagSkipPossible():
            print("Skipping dialog")
            FFX_Xbox.tapB()
    FFX_Logs.writeStats("Chocobo eater turns:")
    FFX_Logs.writeStats(str(turns))
    print("Chocobo Eater battle complete.")

def aeonShield():
    print("Aeon Shield function")
    FFX_Screen.awaitTurn()
    FFX_memory.waitFrames(6)
    while not FFX_memory.otherBattleMenu():
        FFX_Xbox.tapRight()
    if gameVars.usePause():
        FFX_memory.waitFrames(2)
    while FFX_memory.otherBattleMenu():
        if FFX_memory.battleCursor2() == 0:
            FFX_Xbox.tapB()
        else:
            FFX_Xbox.tapUp()
    tapTargeting()

def aeonBoost():
    print("Aeon Boost function")
    FFX_Screen.awaitTurn()
    FFX_memory.waitFrames(6)
    while not FFX_memory.otherBattleMenu():
        FFX_Xbox.tapRight()
    if gameVars.usePause():
        FFX_memory.waitFrames(2)
    while FFX_memory.otherBattleMenu():
        if FFX_memory.battleCursor2() == 1:
            FFX_Xbox.tapB()
        elif FFX_memory.battleCursor2() == 0:
            FFX_Xbox.tapDown()
        else:
            FFX_Xbox.tapUp()
    tapTargeting()

def aeonDismiss():
    print("Aeon Dismiss function")
    FFX_Screen.awaitTurn()
    FFX_memory.waitFrames(6)
    while not FFX_memory.otherBattleMenu():
        FFX_Xbox.tapRight()
    if gameVars.usePause():
        FFX_memory.waitFrames(2)
    while FFX_memory.otherBattleMenu():
        if FFX_memory.battleCursor2() == 2:
            FFX_Xbox.tapB()
        else:
            FFX_Xbox.tapDown()
    tapTargeting()

def MRRbattle(status):
    gameVars = FFX_vars.varsHandle()
    #Yuna complete, Kimahri complete, Valefor overdrive, Battle counter, Yuna level up complete, Yuna grid, phase
    print("---------------------------------------------------------")
    print("---------------------------------------------------------")
    print("Fight start: MRR")
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
    aeonTurn = 0
    
    #If we're ambushed and take too much damage, this will trigger first.
    hpArray = FFX_memory.getBattleHP()
    hpTotal = hpArray[0] + hpArray[1] + hpArray[2]
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
        if status[3] < 3 and FFX_memory.rngSeed() != 160: #Battle number (zero-index)
            if battle == 100 or battle == 101: #The two battles with Funguar
                while not FFX_memory.menuOpen(): #end of battle screen
                    if FFX_Screen.BattleScreen():
                        if FFX_Screen.turnTidus():
                            buddySwapKimahri()
                        elif FFX_Screen.turnKimahri() or FFX_Screen.turnWakka():
                            defend()
                        else:
                            buddySwapYuna()
                            aeonSummon(0)
                            FFX_Screen.awaitTurn()
                            valeforOD(version=1)
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
                        buddySwapYuna()
                        aeonSummon(0)
                        FFX_Screen.awaitTurn()
                        valeforOD(version=1)
                        status[2] = 1
                        status[5] = 1
    elif status[5] == 1: #Next need to recharge Valefor
        valeforChargeComplete = True
        if FFX_memory.battleType() == 1:
            for _ in range(3):
                FFX_Screen.awaitTurn()
                defend()
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
                        attackByNum(22,'r')
                    elif FFX_Screen.turnWakka():
                        wakkaTurns += 1
                        if wakkaTurns == 1:
                            attackByNum(21,'l')
                        else:
                            buddySwapYuna()
                            aeonSummon(0)
                    elif FFX_Screen.turnAuron():
                        attackByNum(22, 'r')
                    elif FFX_Screen.turnKimahri():
                        buddySwapYuna()
                        aeonSummon(0)
                    elif FFX_Screen.turnAeon():
                        if aeonTurn == 0 and FFX_memory.getNextTurn() < 19:
                            aeonBoost()
                            aeonTurn = 1
                        elif aeonTurn < 2:
                            aeonBoost()
                            FFX_Screen.awaitTurn()
                            attack('none')
                            aeonTurn = 2
                        else:
                            aeonSpell2(3, 'none')
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
                        buddySwapYuna()
                        aeonSummon(0)
                    elif FFX_Screen.turnAeon():
                        if aeonTurn == 0 and FFX_memory.getNextTurn() < 19:
                            FFX_Screen.awaitTurn()
                            aeonBoost()
                            aeonTurn = 1
                        elif aeonTurn < 2:
                            aeonSpell(2)
                            FFX_Screen.awaitTurn()
                            aeonBoost()
                            aeonTurn = 2
                        else:
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
                        buddySwapYuna()
                        aeonSummon(0)
                    elif FFX_Screen.turnAeon():
                        if aeonTurn == 0 and FFX_memory.getNextTurn() < 19:
                            aeonBoost()
                            aeonTurn = 1
                        elif aeonTurn < 2:
                            aeonSpell2(2, 'right')
                            FFX_Screen.awaitTurn()
                            aeonBoost()
                            aeonTurn = 2
                        else:
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
                        buddySwapYuna()
                        aeonSummon(0)
                    elif FFX_Screen.turnAeon():
                        if aeonTurn == 0 and FFX_memory.getNextTurn() < 19:
                            FFX_Screen.awaitTurn()
                            aeonBoost()
                            aeonTurn = 1
                        elif aeonTurn < 2:
                            aeonSpell(0)
                            FFX_Screen.awaitTurn()
                            aeonBoost()
                            aeonTurn = 2
                        else:
                            aeonSpell(3)
        elif battle == 101: #Funguar, Red Element, Gandarewa (camera reverse angle)
            #Working, confirmed good
            while not FFX_memory.menuOpen(): #end of battle screen
                if FFX_Screen.BattleScreen():
                    if FFX_Screen.turnTidus():
                        buddySwapKimahri()
                        lancet('left')
                    elif FFX_Screen.turnWakka():
                        attackByNum(22,'l')
                    elif FFX_memory.getEnemyCurrentHP()[2] != 0:
                        buddySwapTidus()
                        fleeAll()
                        valeforChargeComplete = False
                    elif FFX_Screen.turnAuron():
                        buddySwapYuna()
                        aeonSummon(0)
                    elif FFX_Screen.turnAeon():
                        if aeonTurn == 0 and FFX_memory.getNextTurn() < 19:
                            aeonBoost()
                            aeonTurn = 1
                        elif aeonTurn < 2:
                            aeonSpell(0)
                            FFX_Screen.awaitTurn()
                            aeonBoost()
                            aeonTurn = 2
                        else:
                            aeonSpell(3)
        if valeforChargeComplete == True:
            status[5] = 2 #Phase 2, final phase to level up Kimahri and Yuna
            status[2] = 2 #Valefor is charged flag.
    elif status[5] == 2: #Last phase is to level Yuna and Kimahri
        if status[0] == 1 and status[1] == 1: #Both Yuna and Kimahri have levels, good to go.
            status[5] = 3
            while FFX_memory.menuOpen() != True:
                if FFX_Screen.BattleScreen():
                    fleeAll()
        else:
            #Wakka attack Raptors and Gandarewas for Yuna AP.
            yunaTurnCount = 0
            while not FFX_memory.battleComplete():
                if FFX_memory.turnReady():
                    if FFX_Screen.turnTidus():
                        tidusFlee()
                    elif FFX_Screen.faintCheck() >= 1:
                        buddySwapTidus()
                    elif FFX_Screen.turnKimahri():
                        if FFX_memory.getKimahriSlvl() >= 6 and yunaTurnCount:
                            fleeAll()
                        else:
                            defend()
                    elif FFX_Screen.turnYuna():
                        yunaTurnCount += 1
                        if yunaTurnCount == 1:
                            defend()
                        else:
                            fleeAll()
                    elif FFX_Screen.turnWakka():
                        if battle == 96 or battle == 97 or battle == 101:
                            if battle == 101:
                                attackByNum(22,'l')
                            else:
                                attackByNum(21,'l')
                        elif battle == 98 or battle == 100:
                            attack('none')
                        else:
                            fleeAll()
                    else: #Should not occur, but you never know.
                        buddySwapTidus()
    else: #Everything is done.
        fleeAll()
    print("+++")
    print(gameVars.wakkaLateMenu())
    print("+++")
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
        FFX_memory.fullPartyFormat('mrr1', fullMenuClose=False)
    elif status[5] == 2: #Still levelling Yuna or Kimahri
        FFX_memory.fullPartyFormat('mrr2', fullMenuClose=False)
        print("Yuna in front party, trying to get some more experience.")
    else:
        FFX_memory.fullPartyFormat('mrr1', fullMenuClose=False)
    
    #Now checking health values
    hpCheck = FFX_memory.getHP()
    print("HP values: ", hpCheck)
    if status[5] == 2:
        healUp(3, fullMenuClose=False)
    elif hpCheck != [520, 475, 1030, 644, 818, 380]:
        healUp(fullMenuClose=False)
    #donezo. Back to the main path.
    print("Clean-up is now complete.")
    return status

def battleGui():
    FFX_Logs.writeLog("Fight start: Sinspawn Gui")
    print("Fight start: Sinspawn Gui")
    FFX_Xbox.clickToBattle()
    print("Engaging Gui")
    wakkaTurn = False
    yunaTurn = False
    auronTurn = False
    tidusTurn = False
    kimTurn = False
    aeonTurn = False
    
    while aeonTurn == False:
        if FFX_memory.turnReady():
            if FFX_Screen.turnYuna():
                if yunaTurn == False:
                    buddySwapAuron()
                    yunaTurn = True
                else:
                    aeonSummon(0)
            elif FFX_Screen.turnWakka():
                if wakkaTurn == False:
                    FFX_Xbox.weapSwap(0)
                    wakkaTurn = True
                else:
                    buddySwapKimahri()
            elif FFX_Screen.turnKimahri():
                kimahriOD(2)
            elif FFX_Screen.turnTidus():
                if tidusTurn == False:
                    defend()
                    tidusTurn = True
                else:
                    buddySwapYuna()
            elif FFX_Screen.turnAuron():
                if auronTurn == False:
                    useSkill(0)
                    auronTurn = True
                else:
                    defend()
            elif FFX_Screen.turnAeon():
                valeforOD()
                aeonTurn = True
    
    FFX_Screen.awaitTurn()
    nextHP = FFX_memory.getBattleHP()[0]
    lastHP = nextHP
    turn1 = False
    nextTurn = 20
    lastTurn = 20
    while FFX_memory.battleActive():
        if FFX_memory.turnReady() and FFX_memory.getBattleCharTurn() == 8:
            nextHP = FFX_memory.getBattleHP()[0]
            lastTurn = nextTurn
            nextTurn = FFX_memory.getNextTurn()
            if FFX_memory.getOverdriveBattle(8) == 20:
                print("------Overdriving")
                valeforOD()
            elif turn1 == False:
                turn1 = True
                print("------Recharge unsuccessful. Attempting recovery.")                
                aeonShield()
            elif lastTurn == 8: #Valefor takes two turns in a row
                print("------Two turns in a row")                
                aeonShield()
            elif nextHP > lastHP - 40 and not nextHP == lastHP: #Gravity spell was used
                print("------Gravity was used")                
                aeonShield()
            else:
                print("------Attack was just used. Now boost.")
                aeonBoost()
            lastHP = nextHP
        elif FFX_memory.turnReady() and FFX_memory.getBattleCharTurn() == 1:
            print("Yuna turn, something went wrong.")
        elif FFX_memory.turnReady() and FFX_memory.getBattleCharTurn() == 2:
            print("Auron turn, something went wrong.")
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
        elif FFX_Screen.turnSeymour():
            break
    
    #In between battles
    while not FFX_memory.battleActive():
        if FFX_memory.getStoryProgress() >= 865 and FFX_memory.cutsceneSkipPossible():
            FFX_memory.waitFrames(12)
            FFX_Xbox.skipScene()
            print("Skipping scene")
        elif FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
            FFX_Xbox.tapB()
    
    #Second Gui battle
    FFX_Screen.awaitTurn()
    turn = 1
    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            if FFX_Screen.turnSeymour():
                seymourSpell()
            else:
                defend()
    
    while not FFX_memory.userControl():
        if FFX_memory.cutsceneSkipPossible():
            print("Intentional delay to get the cutscene skip to work.")
            FFX_memory.waitFrames(30 * 0.07)
            FFX_Xbox.skipSceneSpec()
            FFX_memory.waitFrames(30 * 2)
        elif FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
            FFX_Xbox.tapB()

def djose(stoneBreath):
    FFX_Logs.writeLog("Fight start: Djose road")
    print("Fight start: Djose road")
    complete = 0
    while not FFX_memory.battleComplete(): #AKA end of battle screen
        battleNum = FFX_memory.getBattleNum()
        if FFX_memory.turnReady():
            if stoneBreath == 1:  # Stone Breath already learned
                print("Djose: Stone breath already learned.")
                fleeAll()
            else:  # Stone breath not yet learned
                if battleNum == 128 or battleNum == 134 or battleNum == 136:
                    print("Djose: Learning Stone Breath.")
                    lancetSwap('none')
                    stoneBreath = 1
                elif battleNum == 127:
                    print("Djose: Learning Stone Breath")
                    # One basilisk with two wasps
                    lancetSwap('up')
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
    print("Fight start: Extractor")
    FFXC.set_neutral()
    
    FFX_Screen.awaitTurn()
    tidusHaste('none')

    FFX_Screen.awaitTurn()
    attack('none') #Wakka attack

    FFX_Screen.awaitTurn()
    tidusHaste('l',character=4)

    cheerCount = 0
    while not FFX_memory.battleComplete(): #AKA end of battle screen
        #First determin if cheers are needed.
        if gameVars.getLStrike() % 2 == 0 and cheerCount < 4:
            tidusCheer = True
        elif gameVars.getLStrike() % 2 == 1 and cheerCount < 1:
            tidusCheer = True
        else:
            tidusCheer = False
        #Then do the battle logic.
        if FFX_memory.specialTextOpen():
            FFX_Xbox.tapB()
        elif FFX_memory.turnReady():
            if FFX_Screen.faintCheck() > 0:
                revive()
            elif FFX_Screen.turnTidus() and ((gameVars.getLStrike() % 2 == 0 and cheerCount < 4) or (gameVars.getLStrike() % 2 == 1 and cheerCount < 1)): 
                cheerCount += 1
                cheer()
            else:
                attack('none')
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
    FFX_memory.clickToControl()


def mixTutorial():
    FFX_Logs.writeLog("Fight start: Mix Tutorial")
    FFX_Xbox.clickToBattle()
    Steal()
    FFX_Xbox.clickToBattle()
    rikkuFullOD('tutorial')
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

def thunderPlains(section):
    bNum = FFX_memory.getBattleNum()
    nadeSlot = FFX_memory.getItemSlot(35)
    print("++Grenade Slot %d" % nadeSlot)
    nadeCount = FFX_memory.getItemCountSlot(nadeSlot)
    print("++Grenade count: %d" % nadeCount)
    print("++Speed sphere count: %d" % FFX_memory.getSpeed())
    useGrenades = nadeCount > 3 and FFX_memory.getSpeed() < 14
    print("++Use Grenades decision: ", useGrenades)
    useNadeSlot = FFX_memory.getUseItemsSlot(35)
    lunarSlot = gameVars.getBlitzWin() or FFX_memory.getItemSlot(56) != 255
    lightSlot = FFX_memory.getItemSlot(57) != 255
    petrifySlot = FFX_memory.getItemSlot(49) != 255
    
    tidusturns = 0
    wakkaturns = 0
    auronturns = 0
    rikkucharge = FFX_memory.getOverdriveValue(6)
    
    petrifiedstate = False
    petrifiedstate = checkPetrify()

    if petrifiedstate == True:
        print("------------Someone has been petrified which messes up the battle logic. Escaping.")
        fleeAll()
    elif bNum in [152, 155, 162]:  # Any battle with Larvae
        if lunarSlot:
            fleeAll() #No longer need Lunar Curtain for Evrae fight, Blitz win logic.
        else: #Blitz loss strat
            print("Battle with Larvae. Battle number: ", bNum)
            while not FFX_memory.battleComplete():
                if FFX_memory.turnReady():
                    if not lunarSlot and FFX_memory.turnReady():
                        if FFX_Screen.turnTidus():
                            if tidusturns == 0:
                                buddySwapRikku()
                            else:
                                fleeAll()
                            tidusturns += 1
                        elif FFX_Screen.turnRikku():
                            Steal()
                            lunarSlot = True
                        else:
                            buddySwapTidus()
                    else:
                        fleeAll()
    elif bNum == 160:
        print("Battle with Iron Giant. Battle number: ", bNum)
        while not FFX_memory.battleComplete():
            FFX_Screen.awaitTurn()
            if lightSlot:
                fleeAll()
            else:
                buddySwapRikku()
            while not FFX_memory.battleComplete():
                if FFX_Screen.turnRikku():
                    if not lightSlot:
                        Steal()
                        lightSlot = FFX_memory.getItemSlot(57) != 255
                    elif FFX_memory.getOverdriveBattle(6) < 100:
                        attack('none')
                    else:
                        fleeAll()
                else:
                    if FFX_memory.getOverdriveBattle(6) < 100 and not checkRikkuOk():
                        escapeOne()
                    else:
                        fleeAll()
    elif bNum == 161:
        print("Battle with Iron Giant and Buer monsters. Battle number: ", bNum)
        while not FFX_memory.battleComplete():
            FFX_Screen.awaitTurn()
            if useGrenades or not lightSlot:
                buddySwapRikku()
                grenadeThrown = False
                while not FFX_memory.battleComplete():
                    if FFX_memory.turnReady():
                        if FFX_Screen.turnRikku():
                            if useGrenades and not grenadeThrown:
                                print("Grenade Slot %d" % useNadeSlot)
                                useItem(useNadeSlot,'none')
                                grenadeThrown = True
                            elif not lightSlot:
                                Steal()
                                lightSlot = FFX_memory.getItemSlot(57) != 255
                            elif FFX_memory.getOverdriveBattle(6) < 100:
                                attack('none')
                            else:
                                fleeAll()
                        else:
                            if not checkRikkuOk():
                                fleeAll()
                            elif FFX_memory.getOverdriveBattle(6) < 100:
                                escapeOne()
                            elif lightSlot and (not useGrenades or grenadeThrown):
                                fleeAll()
                            else:
                                defend()
            else:
                fleeAll()
    elif bNum in [154, 156, 164] and useGrenades:
        print("Battle with random mobs including Buer. Battle number: ", bNum)
        while not FFX_memory.battleComplete():
            FFX_Screen.awaitTurn()
            if useGrenades:
                buddySwapRikku()
                useItem(useNadeSlot, 'none')
            fleeAll()
    elif not gameVars.getBlitzWin() and not petrifySlot and bNum in [153, 154, 163]:
        print("Grabbing petrify grenade. Blitz Loss only strat.")
        while not FFX_memory.battleComplete():
            if FFX_memory.turnReady():
                if bNum in [153,163]:
                    if FFX_Screen.turnTidus():
                        buddySwapRikku()
                        FFX_Screen.awaitTurn()
                        Steal()
                    else:
                        buddySwapTidus()
                        FFX_Screen.awaitTurn()
                        fleeAll()
                else:
                    if FFX_Screen.turnTidus():
                        buddySwapRikku()
                        FFX_Screen.awaitTurn()
                        StealRight()
                    else:
                        buddySwapTidus()
                        FFX_Screen.awaitTurn()
                        fleeAll()
    else:  # Nothing useful this battle. Moving on.
        fleeAll()
    
    print("Battle is ended - Thunder Plains")
    FFX_memory.clickToControl()
    FFX_memory.waitFrames(2) #Allow lightning to attemt a strike
    if FFX_memory.dodgeLightning(gameVars.getLStrike()):
        print("Dodge")
        gameVars.setLStrike(FFX_memory.lStrikeCount())
    print("Checking party format and resolving if needed.")
    FFX_memory.fullPartyFormat('postbunyip', fullMenuClose=False)
    print("Party format is good. Now checking health values.")
    hpValues = FFX_memory.getHP()
    if hpValues[0] < 400 or hpValues[2] < 400 or hpValues[4] < 400 or hpValues[6] < 180:
        healUp()
    FFX_memory.closeMenu()
    print("Ready to continue onward.")

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
    while not FFX_memory.battleComplete(): #AKA end of battle screen
        if FFX_memory.turnReady():
            turnchar = FFX_memory.getBattleCharTurn()
            if checkPetrifyTidus() or not checkRikkuOk():
                print("Tidus or Rikku incapacitated, fleeing")
                fleeAll()
            elif not woodsVars[1] or not woodsVars[2]:
                if battleNum in [171, 172, 175]:
                    if turnchar == 6:
                        if battleNum == 175 and FFX_memory.getUseItemsSlot(24) == 255:
                            print("Marker 2")
                            Steal()
                        elif battleNum == 172 and FFX_memory.getUseItemsSlot(32) == 255:
                            print("Marker 3")
                            StealDown()
                        elif battleNum == 171 and FFX_memory.getUseItemsSlot(32) == 255:
                            print("Marker 4")
                            StealRight()
                        elif not woodsVars[0] or FFX_memory.getOverdriveBattle(6) != 100:
                            print("Charging")
                            attack('none')
                        else:
                            print("Escaping")
                            fleeAll()
                    else:
                        if woodsVars[0] or FFX_memory.getOverdriveBattle(6) == 100:
                            if battleNum in [171, 172] and FFX_memory.getUseItemsSlot(32) == 255:
                                defend()
                            elif battleNum == 175 and FFX_memory.getUseItemsSlot(24) == 255:
                                defend()
                            else:
                                fleeAll()
                        else:
                            escapeOne()
                else:
                    print("Fleeing with ", turnchar)
                    fleeAll()
            elif not woodsVars[0]:
                if turnchar == 6:
                    attack('none')
                else:
                    if FFX_memory.getOverdriveBattle(6) == 100:
                        fleeAll()
                    else:
                        escapeOne()
            else:
                fleeAll()
                

    print("Battle complete, now to deal with the aftermath.")
    FFX_memory.clickToControl3()
    print("M.woods, back in control")
    if FFX_memory.overdriveState()[6] == 100:
        woodsVars[0] = True
    if FFX_memory.getUseItemsSlot(32) != 255:
        woodsVars[1] = True
    if FFX_memory.getUseItemsSlot(24) != 255:
        woodsVars[2] = True
    print("Checking battle formation.")
    if all(woodsVars):
        print("Party format: mwoodsdone")
        FFX_memory.fullPartyFormat("mwoodsdone", fullMenuClose=False)
    print("Party format is now good. Let's check health.")
    # Heal logic
    partyHP = FFX_memory.getHP()
    if partyHP[0] < 450 or partyHP[6] < 180 or partyHP[2] + partyHP[4] < 500:
        healUp()
    FFX_memory.closeMenu()
    print("And last, we'll update variables.")
    print("Rikku charged, stolen Fish Scale, stolen Arctic Wind")
    print(woodsVars)
    print("HP is good. Onward!")
    return woodsVars

def spheriSpellItemReady():
    if FFX_memory.getCharWeakness(20) == 1:
        spellNum = 4 #Ice
        if FFX_memory.getItemSlot(27) > 200:
            return False
    elif FFX_memory.getCharWeakness(20) == 2:
        spellNum = 1 #Fire
        if FFX_memory.getItemSlot(24) > 200:
            return False
    elif FFX_memory.getCharWeakness(20) == 4:
        spellNum = 3 #Water
        if FFX_memory.getItemSlot(30) > 200:
            return False
    elif FFX_memory.getCharWeakness(20) == 8:
        spellNum = 2 #Thunder
        if FFX_memory.getItemSlot(32) > 200:
            return False
    return True

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
            if gameVars.usePause():
                FFX_memory.waitFrames(2)
            turnchar = FFX_memory.getBattleCharTurn()
            partyHP = FFX_memory.getBattleHP()
            if turnchar == 0:
                if tidusturns == 0:
                    equipInBattle(equipType = 'armor', abilityNum = 0x8028)
                elif tidusturns == 1:
                    defend()
                elif not spheriSpellItemReady():
                    buddySwapLulu()
                    FFX_memory.waitFrames(6)
                    FFX_Screen.awaitTurn()
                else:
                    buddySwapRikku()
                tidusturns += 1
            elif turnchar == 1:
                rikkuslotnum = FFX_memory.getBattleCharSlot(6)
                if rikkuslotnum < 3:
                    if partyHP[rikkuslotnum] == 0:
                        revive()
                    else:
                        defend()
                elif FFX_memory.getBattleCharSlot(5) < 3 and rikkuslotnum >= 3:
                    buddySwapRikku()
                else:
                    defend()
            elif turnchar == 3:
                rikkuslotnum = FFX_memory.getBattleCharSlot(6)
                if rikkuslotnum < 3:
                    if partyHP[rikkuslotnum] == 0:
                        revive()
                    else:
                        defend()
                elif FFX_memory.getBattleCharSlot(5) < 3 and rikkuslotnum >= 3:
                    buddySwapRikku()
                else:
                    defend()
            elif turnchar == 5:
                if spellNum == 1:
                    fire()
                elif spellNum == 2:
                    ice()
                elif spellNum == 3:
                    thunder()
                else:
                    water()
                FFX_Screen.awaitTurn()
                if FFX_memory.getCharWeakness(20) == 1:
                    spellNum = 4 #Ice
                elif FFX_memory.getCharWeakness(20) == 2:
                    spellNum = 1 #Fire
                elif FFX_memory.getCharWeakness(20) == 4:
                    spellNum = 3 #Water
                elif FFX_memory.getCharWeakness(20) == 8:
                    spellNum = 2 #Thunder
                
            elif turnchar == 6:
                if rikkuturns == 0:
                    print("Throwing Grenade to check element")
                    grenadeslotnum = FFX_memory.getUseItemsSlot(35)
                    useItem(grenadeslotnum, "none")
                    if FFX_memory.getCharWeakness(20) == 1:
                        spellNum = 4 #Ice
                    elif FFX_memory.getCharWeakness(20) == 2:
                        spellNum = 1 #Fire
                    elif FFX_memory.getCharWeakness(20) == 4:
                        spellNum = 3 #Water
                    elif FFX_memory.getCharWeakness(20) == 8:
                        spellNum = 2 #Thunder
                        
                    #spellNum = FFX_Screen.spherimorphSpell()
                else:
                    print("Starting Rikku's overdrive")
                    FFX_Logs.writeStats("Spherimorph spell used:")
                    FFX_Logs.writeStats(str(spellNum))
                    if spellNum == 1:
                        FFX_Logs.writeStats("Creating Ice to counter Fire")
                        FFX_Logs.writeLog("Creating Ice to counter Fire")
                        print("Creating Ice")
                        rikkuFullOD('spherimorph1')
                    elif spellNum == 2:
                        FFX_Logs.writeStats("Creating Thunder to counter Water")
                        FFX_Logs.writeLog("Creating Thunder to counter Water")
                        print("Creating Water")
                        rikkuFullOD('spherimorph2')
                    elif spellNum == 3:
                        FFX_Logs.writeStats("Creating Water to counter Thunder")
                        FFX_Logs.writeLog("Creating Water to counter Thunder")
                        print("Creating Thunder")
                        rikkuFullOD('spherimorph3')
                    elif spellNum == 4:
                        FFX_Logs.writeStats("Creating Fire to counter Ice")
                        FFX_Logs.writeLog("Creating Fire to counter Ice")
                        print("Creating Fire")
                        rikkuFullOD('spherimorph4')


                rikkuturns += 1
    
    if not gameVars.csr():
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
                    buddySwapRikku()
                else:
                    defend()
                tidusturns += 1
            elif turnchar == 6:
                if luluturns < 2:
                    print("Using Lightning Marble")
                    lightningmarbleslot = FFX_memory.getUseItemsSlot(30)
                    if rikkuturns < 1:
                        useItem(lightningmarbleslot, target = 21)
                    else:
                        useItem(lightningmarbleslot, target = 21)
                else:
                    print("Starting Rikku's overdrive")
                    rikkuFullOD('crawler')
                rikkuturns += 1
            elif turnchar == 3:
                if kimahriturns == 0:
                    lightningmarbleslot = FFX_memory.getUseItemsSlot(30)
                    useItem(lightningmarbleslot, target = 21)
                else:
                    buddySwapYuna()
                kimahriturns += 1
            elif turnchar == 5:
                revive()
                luluturns += 1
            elif turnchar == 1:
                if yunaturns == 0:
                    defend()
                else:
                    buddySwapTidus()
                yunaturns += 1
            else:
                defend()
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
    
    FFX_memory.clickToControl()

def getAnimaItemSlot():
    useableSlot = FFX_memory.getUseItemsSlot(32)
    if useableSlot > 200:
        useableSlot = FFX_memory.getUseItemsSlot(30)
    if useableSlot > 200:
        useableSlot = FFX_memory.getUseItemsSlot(24)
    if useableSlot > 200:
        useableSlot = FFX_memory.getUseItemsSlot(27)
    if useableSlot > 200:
        useableSlot = 255
    return useableSlot

# Process written by CrimsonInferno
def seymourGuado_blitzWin():
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

    while not FFX_memory.battleComplete(): #AKA end of battle screen
        if FFX_memory.turnReady():
            turnchar = FFX_memory.getBattleCharTurn()
            for i in range(0, 3):
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
            if FFX_memory.getEnemyCurrentHP()[1] < 2999 and turnchar == 0:
                attack('none')
                print("Should be last attack of the fight.")
            elif turnchar == 0:
                if tidusturns == 0:
                    print("Swap to Brotherhood")
                    equipInBattle(special = 'brotherhood')
                elif tidusturns == 1:
                    print("Tidus Haste self")
                    tidusHaste('none')
                    tidushaste = True
                elif tidusturns == 2:
                    print("Talk to Seymour")
                    while not FFX_memory.otherBattleMenu():
                        FFX_Xbox.tapLeft()
                    while FFX_memory.battleCursor2() != 1:
                        FFX_Xbox.tapDown()
                    while FFX_memory.otherBattleMenu():
                        FFX_Xbox.tapB()
                    FFX_Xbox.tapLeft()
                    tapTargeting()
                elif tidusturns == 3:
                    tidusODSeymour()
                elif tidusturns == 4:
                    buddySwapWakka()
                elif animahits + animamiss == 3 and animamiss > 0 and missbackup == False:
                    buddySwapLulu()
                elif tidushaste == False:
                    print("Tidus Haste self")
                    tidusHaste('none')
                    tidushaste = True
                elif animahits < 4:
                    oldHP = FFX_memory.getEnemyCurrentHP()[3]
                    attack('none')
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
                    buddySwapAuron()
                yunaturns += 1
                print("Yuna turn, complete")
            elif turnchar == 3:
                if kimahriconfused == True:
                    tidusposition = FFX_memory.getBattleCharSlot(0)
                    rikkuposition = FFX_memory.getBattleCharSlot(6)
                    if tidusposition >= 3:
                        buddySwapTidus()
                    elif rikkuposition >= 3:
                        buddySwapRikku()
                elif kimahriturns == 0:
                    print("Confused states:")
                    print("Yuna confusion: ", FFX_memory.confusedState(1))
                    print("Tidus confusion: ", FFX_memory.confusedState(0))
                    print("Kimahri confusion: ", FFX_memory.confusedState(3))
                    print("Auron confusion: ", FFX_memory.confusedState(2))
                    if FFX_memory.confusedState(0) == True:
                        remedy(character = 0,
                               direction="l")
                    elif FFX_memory.confusedState(1) == True:
                        remedy(character = 1,
                               direction="l")
                    else:
                        defend()
                elif kimahriturns == 1:
                    Steal()
                elif animamiss > 0 and (missbackup == False or FFX_Screen.faintCheck() == 0):
                    FFX_Xbox.weapSwap(0)
                else:
                    tidusposition = FFX_memory.getBattleCharSlot(0)
                    rikkuposition = FFX_memory.getBattleCharSlot(6)
                    if tidusposition >= 3:
                        buddySwapTidus()
                    elif rikkuposition >= 3:
                        buddySwapRikku()
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
                        remedy(character = 3,
                               direction="l")
                        kimahriconfused = True
                    else:
                        defend()
                elif animamiss > 0 and (missbackup == False or FFX_Screen.faintCheck() == 0):
                    if kimahridead == True and rikkuturns == 0:
                        buddySwapRikku()
                    else:
                        FFX_Xbox.weapSwap(1)
                else:
                    tidusposition = FFX_memory.getBattleCharSlot(0)
                    rikkuposition = FFX_memory.getBattleCharSlot(6)
                    if tidusposition >= 3:
                        buddySwapTidus()
                    elif rikkuposition >= 3:
                        buddySwapRikku()
                    else:
                        defend()
                auronturns += 1
                print("Auron turn, complete")
            elif turnchar == 4:
                if wakkaturns == 0:
                    FFX_Xbox.weapSwap(0)
                elif animamiss > 0 and (missbackup == False or FFX_Screen.faintCheck() == 0):
                    if kimahridead == True and rikkuturns == 0:
                        buddySwapRikku()
                    else:
                        FFX_Xbox.weapSwap(0)
                else:
                    tidusposition = FFX_memory.getBattleCharSlot(0)
                    rikkuposition = FFX_memory.getBattleCharSlot(6)
                    if tidusposition >= 3:
                        buddySwapTidus()
                    elif rikkuposition >= 3:
                        buddySwapRikku()
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
                        if FFX_memory.getBattleCharSlot(0) >= 3:
                            buddySwapTidus()
                        elif FFX_memory.getBattleCharSlot(1) >= 3:
                            buddySwapYuna()
                        elif FFX_memory.getBattleCharSlot(5) >= 3:
                            buddySwapLulu()
                elif animahits < 4:
                    Steal()
                elif FFX_memory.getBattleHP()[FFX_memory.getBattleCharSlot(0)] == 0:
                    reviveTarget(target=0)
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
                    if tidusposition >= 3:
                        buddySwapTidus()
                    elif rikkuposition >= 3:
                        buddySwapRikku()
                    else:
                        defend()
                print("Lulu turn, complete")
            else:
                print("No turn. Holding for next action.")
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
            print("Diag skip")
    print("Battle summary screen")
    FFXC.set_value('BtnB', 1)
    FFX_memory.waitFrames(30 * 2.8)
    FFXC.set_value('BtnB', 0)

def seymourGuado_blitzLoss():
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
    thrownItems = 0

    while not FFX_memory.battleComplete(): #AKA end of battle screen
        if FFX_memory.turnReady():
            turnchar = FFX_memory.getBattleCharTurn()
            for i in range(0, 3):
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
            if turnchar == 0:
                if FFX_memory.getEnemyCurrentHP()[1] < 2999:
                    attack('none')
                    print("Should be last attack of the fight.")
                elif tidusturns == 0:
                    print("Tidus Haste self")
                    tidusHaste('none')
                    tidushaste = True
                elif tidusturns == 1:
                    cheer()
                elif tidusturns == 2:
                    print("Talk to Seymour")
                    while not FFX_memory.otherBattleMenu():
                        FFX_Xbox.tapLeft()
                    while FFX_memory.battleCursor2() != 1:
                        FFX_Xbox.tapDown()
                    while FFX_memory.otherBattleMenu():
                        FFX_Xbox.tapB()
                    FFX_Xbox.tapLeft()
                    tapTargeting()
                elif tidusturns == 3:
                    print("Swap to Brotherhood")
                    equipInBattle(special = 'brotherhood')
                elif tidusturns == 4:
                    tidusODSeymour()
                elif tidusturns == 5:
                    buddySwapWakka()
                elif animahits + animamiss == 3 and animamiss > 0 and missbackup == False:
                    buddySwapLulu()
                    defend()
                    missbackup = True
                elif tidushaste == False:
                    print("Tidus Haste self")
                    tidusHaste('none')
                    tidushaste = True
                elif animahits < 4:
                    oldHP = FFX_memory.getEnemyCurrentHP()[3]
                    attack('none')
                    newHP = FFX_memory.getEnemyCurrentHP()[3]
                    if newHP < oldHP:
                        print("Hit Anima")
                        animahits += 1
                    else:
                        print("Miss Anima")
                        animamiss += 1
                else:
                    print("Plain Attacking")
                    attack('none')
                tidusturns += 1
                print("Tidus turns: %d" % tidusturns)
            elif turnchar == 1:
                if yunaturns == 0:
                    FFX_Xbox.weapSwap(0)
                else:
                    buddySwapLulu()
                    FFX_Screen.awaitTurn()
                    FFX_Xbox.weapSwap(0)
                yunaturns += 1
                print("Yuna turn, complete")
            elif turnchar == 5:
                if animahits == 0:
                    print("Confused states:")
                    print("Yuna confusion: ", FFX_memory.confusedState(1))
                    print("Tidus confusion: ", FFX_memory.confusedState(0))
                    print("Kimahri confusion: ", FFX_memory.confusedState(3))
                    print("Lulu confusion: ", FFX_memory.confusedState(5))
                    buddySwapRikku()
                    if FFX_memory.confusedState(0) == True:
                        remedy(character = 0,direction="l")
                    elif FFX_memory.confusedState(3):
                        remedy(character = 3, direction="l")
                else:
                    buddySwapTidus()
                    attack('none')
            elif turnchar == 3:
                if kimahriconfused == True:
                    tidusposition = FFX_memory.getBattleCharSlot(0)
                    rikkuposition = FFX_memory.getBattleCharSlot(6)
                    if tidusposition >= 3:
                        buddySwapTidus()
                    elif rikkuposition >= 3:
                        buddySwapRikku()
                    else:
                        defend()
                elif kimahriturns == 0:
                    print("Confused states:")
                    print("Yuna confusion: ", FFX_memory.confusedState(1))
                    print("Tidus confusion: ", FFX_memory.confusedState(0))
                    print("Kimahri confusion: ", FFX_memory.confusedState(3))
                    print("Auron confusion: ", FFX_memory.confusedState(2))
                    print("Lulu confusion: ", FFX_memory.confusedState(5))
                    if FFX_memory.confusedState(0) == True:
                        remedy(character = 0,direction="l")
                    elif FFX_memory.confusedState(1) == True:
                        remedy(character = 1,direction="l")
                    elif FFX_memory.confusedState(5) == True:
                        remedy(character = 5,direction="l")
                    else:
                        defend()
                elif thrownItems < 2:
                    itemSlot = getAnimaItemSlot()
                    if itemSlot != 255:
                        useItem(itemSlot)
                    else:
                        Steal()
                    thrownItems += 1
                elif animamiss > 0 and (missbackup == False or FFX_Screen.faintCheck() == 0):
                    Steal()
                else:
                    tidusposition = FFX_memory.getBattleCharSlot(0)
                    rikkuposition = FFX_memory.getBattleCharSlot(6)
                    if tidusposition >= 3:
                        buddySwapTidus()
                    elif rikkuposition >= 3:
                        buddySwapRikku()
                    else:
                        Steal()
                kimahriturns += 1
                print("Kimahri turn, complete")
            elif turnchar == 4:
                if wakkaturns == 0:
                    FFX_Xbox.weapSwap(0)
                elif animamiss > 0 and (missbackup == False or FFX_Screen.faintCheck() == 0):
                    if kimahridead == True and rikkuturns < 2:
                        buddySwapRikku()
                    else:
                        FFX_Xbox.weapSwap(0)
                else:
                    tidusposition = FFX_memory.getBattleCharSlot(0)
                    rikkuposition = FFX_memory.getBattleCharSlot(6)
                    if tidusposition >= 3:
                        buddySwapTidus()
                    elif rikkuposition >= 3:
                        buddySwapRikku()
                    else:
                        defend()
                wakkaturns += 1
                print("Wakka turn, complete")
            elif turnchar == 6:
                if FFX_Screen.faintCheck() == 2:
                    reviveAll()
                    missbackup = True
                    tidushaste = False
                elif thrownItems < 2:
                    itemSlot = getAnimaItemSlot()
                    if itemSlot != 255:
                        useItem(itemSlot)
                    else:
                        Steal()
                    thrownItems += 1
                else:
                    tidusposition = FFX_memory.getBattleCharSlot(0)
                    if tidusposition >= 3:
                        buddySwapTidus()
                    elif animamiss > 0 and (missbackup == False or FFX_Screen.faintCheck() == 0):
                        Steal()
                    elif animahits < 4:
                        Steal()
                    elif FFX_memory.getBattleHP()[FFX_memory.getBattleCharSlot(0)] == 0:
                        reviveTarget(target=0)
                    else:
                        defend()
                rikkuturns += 1
                print("Rikku turn, complete")
            else:
                print("No turn. Holding for next action.")
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
            print("Diag skip")
    print("Battle summary screen")
    FFXC.set_value('BtnB', 1)
    FFX_memory.waitFrames(30 * 2.8)
    FFXC.set_value('BtnB', 0)

def seymourGuado_nemesis():
    FFX_Screen.awaitTurn()
    tidusHaste('none')
    FFX_Screen.awaitTurn()
    equipInBattle(special = 'brotherhood')
    FFX_memory.waitFrames(5)
    FFX_Screen.awaitTurn()
    tidusODSeymour()
    FFX_Screen.awaitTurn()
    yunaDefend = False
    while not FFX_Screen.turnTidus():
        if FFX_memory.turnReady():
            if FFX_Screen.turnYuna():
                if not yunaDefend:
                    FFX_Xbox.weapSwap(0)
                    yunaDefend = True
                else:
                    buddySwapAuron()
                    equipInBattle(abilityNum = 0x8002, character = 2)
            elif FFX_Screen.turnKimahri():
                Steal()
            elif FFX_Screen.turnLulu():
                buddySwapAuron()
            else:
                defend()
    FFX_Screen.awaitTurn()
    buddySwapWakka()
    FFX_Xbox.weapSwap(0)
    #Anima uses Pain
    FFX_Screen.awaitTurn()
    buddySwapTidus()
    attack('none')
    
    while not FFX_memory.battleComplete(): #AKA end of battle screen
        if FFX_memory.turnReady():
            if FFX_Screen.turnTidus():
                attack('none')
            elif FFX_Screen.turnRikku():
                Steal()
            elif FFX_Screen.turnLulu():
                buddySwapRikku()
            else:
                buddySwapLulu()
                FFX_Xbox.weapSwap(0)
    print("Battle summary screen")
    FFXC.set_value('BtnB', 1)
    FFX_memory.waitFrames(30 * 2.8)
    FFXC.set_value('BtnB', 0)

def seymourGuado():
    #if gameVars.nemesis():
    #    seymourGuado_nemesis()
    if gameVars.getBlitzWin():
        seymourGuado_blitzWin()
    else:
        seymourGuado_blitzLoss()

def escapeWithXP():
    rikkuItem = False
    if FFX_memory.getItemSlot(39) > 200:
        fleeAll()
    else:
        while FFX_memory.battleActive():
            if FFX_memory.turnReady():
                if FFX_Screen.turnTidus():
                    if not rikkuItem:
                        equipInBattle(equipType = 'armor', abilityNum = 0x8028)
                        FFX_Screen.awaitTurn()
                        buddySwapRikku()
                    else:
                        attack('none')
                elif FFX_Screen.turnRikku():
                    if not rikkuItem:
                        useItem(FFX_memory.getUseItemsSlot(39))
                        rikkuItem = True
                    else:
                        defend()
                elif FFX_Screen.turnAuron():
                    attack('none')
                else:
                    buddySwapTidus()
    FFX_memory.clickToControl()

def fullheal(target: int, direction: str):
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
        target=255
    else:
        itemnum = -1
        itemname = "noitemfound"
    if itemnum >= 0:
        FFX_Logs.writeLog("Using %s" % itemname)
        print("Using %s" % itemname)
        _useHealingItem(target, direction, itemnum)
        return 1

    else:
        print("No restorative items available")
        return 0


# Process written by CrimsonInferno
def wendigoresheal(turnchar: int, usepowerbreak: int, tidusmaxHP: int):
    print("Wendigo Res/Heal function")
    if FFX_memory.getEnemyCurrentHP().count(0) == 2 and FFX_memory.getNextTurn() < 20:
        return 0
    healCount = 0
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
        buddySwapAuron()
    # If tidus is less than max HP heal him
    elif partyHP[FFX_memory.getBattleCharSlot(0)] < tidusmaxHP:
        print("Tidus need healing")
        if fullheal(target = 0,
                    direction="l") == 0:
            if FFX_Screen.faintCheck():
                print("No healing available so reviving instead")
                if FFX_memory.getThrowItemsSlot(6) < 255:
                    revive()
                elif FFX_memory.getThrowItemsSlot(7) < 255:
                    reviveAll()
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
    luluSwap = False
    FFX_Logs.writeLog("Fight start: Wendigo")
    
    FFX_Screen.awaitTurn()

    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
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
                        buddySwapAuron()
                    else:
                        print("Swapping to Lulu")
                        luluSwap = True
                        buddySwapLulu()
            elif turnchar == 0:
                print("Test 1")
                if tidushaste == False:
                    print("Tidus Haste self")
                    tidusHaste('none')
                    tidushaste = True
                elif phase == 0:
                    print("Switch to Brotherhood")
                    equipInBattle(special = 'brotherhood')
                    phase += 1
                elif phase == 1:
                    print("Attack top Guado")
                    attackByNum(22, 'd')
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
                        if fullheal(target = 0,
                                    direction="l") == 0:
                            if FFX_Screen.faintCheck():
                                print("No healing items so revive someone instead")
                                revive()
                            else:
                                print("No healing items so just go face")
                                attackByNum(21, 'l')
                    else:
                        print("No need to heal. Ver 1")
                        attackByNum(21, 'l')
                    tidushealself = False
                else:
                    print("No need to heal. Ver 2")
                    attackByNum(21, 'l')
                FFX_memory.waitFrames(30 * 0.2)
            elif turnchar == 6:
                if phase == 2:
                    phase += 1
                    lightcurtainslot = FFX_memory.getUseItemsSlot(57)
                    if lightcurtainslot < 255:
                        print("Using Light Curtain on Tidus")
                        useItem(lightcurtainslot, target = 0)
                        curtain = True
                    else:
                        print("No Light Curtain")
                        print("Swapping to Auron to Power Break")
                        buddySwapAuron()  # Swap for Auron
                        powerbreak = True
                        usepowerbreak = True
                elif wendigoresheal(turnchar=turnchar, usepowerbreak=usepowerbreak, tidusmaxHP=tidusmaxHP) == 0:
                    if guadosteal == False and FFX_memory.getEnemyCurrentHP().count(0) != 2:
                        Steal()
                        guadosteal = True
                    elif FFX_memory.getEnemyCurrentHP().count(0) == 2 and not luluSwap:
                        luluSwap = True
                        buddySwapLulu()
                    else:
                        defend()
            elif turnchar == 2:
                if usepowerbreak == True:
                    print("Using Power Break")
                    FFX_Xbox.tapDown()
                    FFX_Xbox.tapB()
                    FFX_memory.waitFrames(30 * 0.6)
                    FFX_Xbox.tapB()
                    FFX_memory.waitFrames(30 * 0.6)
                    FFX_Xbox.tapLeft()
                    FFX_Xbox.tapB()  # Auron uses Armor Break
                    FFX_memory.waitFrames(30 * 1)
                    powerbreakused = True
                    usepowerbreak = False
                else:
                    if wendigoresheal(turnchar=turnchar, usepowerbreak=usepowerbreak, tidusmaxHP=tidusmaxHP) == 0:
                        defend()
            else:
                if wendigoresheal(turnchar=turnchar, usepowerbreak=usepowerbreak, tidusmaxHP=tidusmaxHP) == 0:
                    defend()

def zu():
    FFX_Screen.awaitTurn()
    attack('none')
    while not FFX_memory.battleComplete():
        if FFX_Screen.BattleScreen():
            if FFX_memory.partySize() <= 2:
                defend()
            else:
                fleeAll()
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB() #Skip Dialog
    FFX_memory.clickToControl()

def bikanelBattleLogic(status):
    #status should be an array length 2
    #[rikkuCharged, speedNeeded, powerNeeded, itemsNeeded]
    battleNum = FFX_memory.getBattleNum()
    itemStolen = False
    itemThrown = False
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
        if status[0]:
            battleGoal = 3 #Nothing to do here, we just want to flee.
        else:
            battleGoal = 2
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
    while not FFX_memory.battleComplete():
        if battleGoal == 0: #Steal an item
            print("Looking to steal an item.")
            if FFX_memory.turnReady():
                if FFX_memory.getBattleCharTurn() == 0:
                    buddySwapKimahri()
                elif itemStolen == False and (FFX_Screen.turnKimahri() or FFX_Screen.turnReady()):
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
                    
                    #After stealing an item, what to do next?
                    if throwPower == True or throwSpeed == True:
                        battleGoal = 1
                    else:
                        battleGoal = 3
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
            if FFX_memory.turnReady():
                if FFX_memory.getBattleCharTurn() == 0:
                    buddySwapKimahri()
                elif not itemThrown and (FFX_Screen.turnKimahri() or FFX_Screen.turnRikku()):
                    if items[2] >= 1:
                        itemToUse = 40
                    elif items[3] >= 1:
                        itemToUse = 39
                    else:
                        itemToUse = 37
                    
                    useItem(FFX_memory.getUseItemsSlot(itemToUse), 'none')
                    itemThrown = True
                elif status[0] == False:
                    if FFX_memory.getBattleCharTurn() == 6:
                        attack('none')
                    else:
                        escapeOne()
                else:
                    fleeAll()
        elif battleGoal == 2: #Charge Rikku
            print("Attack/Steal with Rikku, everyone else escape.")
            if FFX_memory.turnReady():
                if FFX_memory.getBattleCharTurn() == 6:
                    attack('none')
                elif 6 in FFX_memory.getActiveBattleFormation():
                    escapeOne()
                else:
                    fleeAll()
        else: #Flee, nothing else.
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

def sandyManip() -> bool:
    if gameVars.getBlitzWin():
        blitzBuffer = 31
    else:
        blitzBuffer = 32
    whiteVals = FFX_memory.nextChanceRNG01()
    greenVals = FFX_memory.nextChanceRNG01(version='green')
    
    whiteOdd = whiteVals[0]
    whiteEven = whiteVals[1]
    greenOdd = greenVals[0]
    greenEven = greenVals[1]
    
    x = 0
    while x < len(whiteOdd):
        if whiteOdd[x] < blitzBuffer:
            whiteOdd.remove(whiteOdd[x])
        else:
            x+= 1
    x = 0
    while x < len(whiteEven):
        if whiteEven[x] < blitzBuffer:
            whiteEven.remove(whiteEven[x])
        else:
            x+= 1
    x = 0
    blitzBuffer += 2
    while x < len(greenOdd):
        if greenOdd[x] < blitzBuffer:
            greenOdd.remove(greenOdd[x])
        else:
            x+= 1
    x = 0
    while x < len(greenEven):
        if greenEven[x] < blitzBuffer:
            greenEven.remove(greenEven[x])
        else:
            x+= 1
    #If the lowest Even value is less than the lowest Odd value, worth switching.
    return min(greenEven[0], whiteEven[0]) < min(greenOdd[0], whiteOdd[0])

def sandragora(version):
    FFX_Screen.awaitTurn()
    if version == 1: #Kimahri's turn
        if FFX_memory.getBattleCharSlot(3) >= 3:
            buddySwapKimahri()
        else:
            tidusHaste('l',character=3)
        FFX_Screen.awaitTurn()
        print("Now Kimahri will use his overdrive.")
        kimahriOD(3)
        FFX_memory.clickToControl()
    else: #Auron's turn
        #Manip for NE armor
        if FFX_memory.battleType() == 2:
            while FFX_memory.battleType() == 2:
                print("Ambushed, swapping out.")
                fleeAll()
                FFX_memory.clickToControl()
                FFXC.set_movement(0, 1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_Screen.awaitTurn()
        elif FFX_memory.rngSeed() == 31:
                print("Manipulating known seed 31")
                fleeAll()
                FFX_memory.clickToControl()
                FFXC.set_movement(0, 1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_Screen.awaitTurn()
        else:
            print("DO NOT Swap odd/even seeds on RNG01")
    
        tidusHaste('d',character=2)
        FFX_Screen.awaitTurn()
        if FFX_Screen.turnKimahri() or FFX_Screen.turnRikku():
            print("Kimahri/Rikku taking a spare turn. Just defend.")
            defend()
            FFX_Screen.awaitTurn()
        print("Setting up Auron overdrive")
        auronOD(style="shooting star")
        FFX_memory.clickToControl()

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
            
            if FFX_Screen.turnKimahri():
                kimahriOD(3)
            elif FFX_memory.getBattleCharSlot(3) >= 3:
                buddySwapKimahri()  # Tidus for Kimahri
                lancetHome('none')
            else:
                defend()
    print("Home 2 shows as fight complete.")
    FFXC.set_neutral()
    FFX_memory.clickToControl()

def home3():
    FFX_Logs.writeLog("Fight start: Home 3")
    #equipBrotherhood = False
    FFX_Xbox.clickToBattle()
    if FFX_memory.getUseItemsSlot(49) > 200:
        tidusHaste('none')
    else:
        while not FFX_Screen.turnRikku():
            defend()
            FFX_Xbox.clickToBattle()
            useItem(FFX_memory.getUseItemsSlot(49), 'none')
        
    
    rikkuItemThrown = 0
    while not FFX_memory.battleComplete(): #AKA end of battle screen
        if FFX_memory.turnReady():
            print("---------Turn:")
            if FFX_Screen.turnTidus():
                print("---------Tidus")
                if FFX_memory.getUseItemsSlot(49) != 255:
                    defend()
                #elif not equipBrotherhood:
                    #equipInBattle(special = 'brotherhood')
                    #equipBrotherhood = True
                else:
                    attack('none')
            elif FFX_Screen.turnRikku() and rikkuItemThrown < 1 and home3item() != 255:
                print("---------Rikku")
                useItemSlot = home3item()
                useItem(useItemSlot, 'none')
                rikkuItemThrown += 1
            elif FFX_Screen.faintCheck() > 0:
                print("---------any, revive")
                revive()
            else:
                print("---------any, defend")
                defend()
    FFXC.set_neutral()
    print("Home 3 shows as fight complete.")

def home3item():
    throwSlot = FFX_memory.getUseItemsSlot(49) #Petrify Grenade
    if throwSlot != 255:
        return throwSlot
    throwSlot = FFX_memory.getUseItemsSlot(40) #Smoke Bomb
    if throwSlot != 255:
        return throwSlot
    throwSlot = FFX_memory.getUseItemsSlot(39) #Silence - for the Guado-face.
    if throwSlot != 255:
        return throwSlot
    return 255

def home4():
    FFX_Logs.writeLog("Fight start: Home 4")
    FFX_Xbox.clickToBattle()

    print("Kimahri vs Chimera")
    while not FFX_memory.menuOpen(): #AKA end of battle screen
        if FFX_memory.turnReady():
            if FFX_Screen.turnKimahri():
                kimahriOD(4)
            elif FFX_memory.getBattleCharSlot(3) >= 3:
                buddySwapKimahri()  # Tidus for Kimahri
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

    while FFX_memory.battleActive(): #AKA end of battle screen
        if FFX_memory.turnReady():
            turnchar = FFX_memory.getBattleCharTurn()
            print("Tidus prep turns: ", tidusPrep)
            # print("otherTurns: ", otherTurns)
            if turnchar == 0:
                print("Registering Tidus's turn")
                if gameVars.getBlitzWin(): #Blitz win logic
                    if tidusPrep == 0:
                        tidusPrep = 1
                        tidusHaste('none')
                    elif tidusPrep == 1:
                        tidusPrep += 1
                        cheer()
                    elif tidusPrep == 2 and rikkuTurns == 0:
                        equipInBattle(equipType = 'armor', abilityNum = 0x8028)
                    elif tidusPrep == 2 and tidusAttacks == 2:
                        tidusPrep += 1
                        cheer()
                    else:
                        tidusAttacks += 1
                        attack('none')
                else: #Blitz loss logic
                    if tidusPrep == 0:
                        tidusPrep = 1
                        tidusHaste('none')
                    elif tidusPrep <= 2:
                        tidusPrep += 1
                        cheer()
                    elif tidusPrep == 3:
                        print("Equip Baroque Sword.")
                        equipInBattle(special = 'baroque')
                        tidusPrep += 1
                    else:
                        tidusAttacks += 1
                        attack('none')
            elif turnchar == 6:
                print("Registering Rikku's turn")
                if rikkuTurns == 0:
                    rikkuTurns += 1
                    print("Rikku overdrive")
                    rikkuFullOD('Evrae')
                elif not gameVars.getBlitzWin() and not lunarCurtain:
                    print("Use Lunar Curtain")
                    lunarSlot = FFX_memory.getUseItemsSlot(56)
                    useItem(lunarSlot, direction='l', target=0)
                    lunarCurtain = True
                elif FFX_memory.getBattleHP()[FFX_memory.getBattleCharSlot(0)] < 1520 and tidusAttacks < 3:
                    print("Rikku should attempt to heal a character.")
                    kimahriTurns += 1
                    if fullheal(target = 0,
                                direction="d") == 0:
                        print("Restorative item not found.")
                        useItem(FFX_memory.getUseItemsSlot(20))
                    else:
                        print("Heal should be successful.")
                else:
                    Steal()
            elif turnchar == 3:
                print("Registering Kimahri's turn")
                if not gameVars.getBlitzWin() and not lunarCurtain:
                    print("Use Lunar Curtain")
                    lunarSlot = FFX_memory.getUseItemsSlot(56)
                    useItem(lunarSlot, direction='l', target=0)
                    lunarCurtain = True
                elif FFX_memory.getBattleHP()[FFX_memory.getBattleCharSlot(0)] < 1520 and tidusAttacks < 3:
                    print("Kimahri should attempt to heal a character.")
                    kimahriTurns += 1
                    if fullheal(target = 0,
                                direction="u") == 0:
                        print("Restorative item not found.")
                        useItem(FFX_memory.getUseItemsSlot(20))
                    else:
                        print("Heal should be successful.")
                else:
                    Steal()
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
    
    if not gameVars.csr():
        while not FFX_memory.cutsceneSkipPossible():
            if FFX_memory.menuOpen():
                FFX_Xbox.tapB()
        FFX_Xbox.skipSceneSpec()


def guards(groupNum, sleepingPowders):
    FFX_Logs.writeLog("Fight start: Bevelle Guards")
    rikkuHeal = False
    turnNum = 0
    rikkuTurns = 0
    items = updateStealItemsDesert()
    FFX_Xbox.clickToBattle()
    throw_distiller = FFX_memory.getItemSlot(16) != 255 or FFX_memory.getItemSlot(18) != 255
    num_throws = 0
    hasted = False
    tidusWent = False
    if sleepingPowders: # We have sleeping powders
        while not FFX_memory.battleComplete(): #AKA end of battle screen
            if groupNum in [1, 3]:
                if FFX_Screen.turnTidus():
                    attack('none')
                elif throw_distiller:
                    if FFX_memory.getItemSlot(18) != 255:
                        _useHealingItem(itemID=18)
                    else:
                        _useHealingItem(itemID=16)
                    throw_distiller = False
                elif 6 in FFX_memory.getActiveBattleFormation() and FFX_memory.getBattleHP()[FFX_memory.getBattleCharSlot(6)] <= 120 \
                    and FFX_memory.getBattleHP()[FFX_memory.getBattleCharSlot(6)] != 0:
                    if FFX_memory.getItemSlot(0) != 255:
                        usePotionCharacter(6, 'r')
                    elif FFX_memory.getItemSlot(1) != 255:
                        _useHealingItem(num=6, direction='r', itemID=1)
                    else:
                        defend()
                else:
                    defend()
            elif groupNum in [2, 4]:
                if FFX_Screen.turnTidus():
                    attack('none')
                elif FFX_Screen.turnRikku() or FFX_Screen.turnKimahri() and num_throws < 2:
                    silenceSlot = FFX_memory.getUseItemsSlot(39)
                    if num_throws == 0:
                        useItem(FFX_memory.getUseItemsSlot(37))
                    else:
                        if FFX_memory.getUseItemsSlot(40) != 255:
                            useItem(FFX_memory.getUseItemsSlot(40))
                        elif FFX_memory.getUseItemsSlot(27) != 255:
                            useItem(FFX_memory.getUseItemsSlot(27))
                        elif silenceSlot != 255 and FFX_memory.getItemCountSlot(silenceSlot) > 1:
                            #Save one for later if possible
                            useItem(FFX_memory.getUseItemsSlot(39))
                        elif FFX_memory.getUseItemsSlot(37) != 255:
                            useItem(FFX_memory.getUseItemsSlot(37))
                        elif silenceSlot != 255:
                            #Throw last Silence grenade as a last resort.
                            useItem(FFX_memory.getUseItemsSlot(39))
                    num_throws += 1
                else:
                    defend()
            elif groupNum == 5:
                if FFX_Screen.faintCheck():
                    revive()
                elif FFX_Screen.turnTidus():
                    if not hasted:
                        tidusHaste('left', character=6)
                        hasted = True
                    else:
                        attackByNum(22,'r')
                elif FFX_Screen.turnRikku() or FFX_Screen.turnKimahri():
                    silenceSlot = FFX_memory.getUseItemsSlot(39)
                    if FFX_memory.getUseItemsSlot(37) != 255:
                        useItem(FFX_memory.getUseItemsSlot(37))
                    elif FFX_memory.getUseItemsSlot(40) != 255:
                        useItem(FFX_memory.getUseItemsSlot(40))
                    elif FFX_memory.getUseItemsSlot(27) != 255:
                        useItem(FFX_memory.getUseItemsSlot(27))
                    elif FFX_memory.getUseItemsSlot(39) != 255:
                        useItem(FFX_memory.getUseItemsSlot(39))
                    elif silenceSlot != 255 and FFX_memory.getItemCountSlot(silenceSlot) > 1:
                        #Save one for later if possible
                        useItem(FFX_memory.getUseItemsSlot(39))
                    else:
                        defend()
        FFX_memory.clickToControl()
    else: # We do not have sleeping powders
        while not FFX_memory.battleComplete():
            if groupNum in [1, 3]:
                if FFX_Screen.turnTidus():
                    attack('none')
                elif throw_distiller:
                    if FFX_memory.getItemSlot(18) != 255:
                        _useHealingItem(itemID=18)
                    else:
                        _useHealingItem(itemID=16)
                    throw_distiller = False
                elif 6 in FFX_memory.getActiveBattleFormation() and FFX_memory.getBattleHP()[FFX_memory.getBattleCharSlot(6)] <= 120 \
                    and FFX_memory.getBattleHP()[FFX_memory.getBattleCharSlot(6)] !=0:
                    if FFX_memory.getItemSlot(0) != 255:
                        usePotionCharacter(6, 'r')
                    elif FFX_memory.getItemSlot(1) != 255:
                        _useHealingItem(num=6, direction='r', itemID=1)
                    else:
                        defend()
                else:
                    defend()
            elif groupNum in [2, 4]:
                if FFX_Screen.turnTidus():
                    if not tidusWent:
                        buddySwapKimahri()
                        tidusWent = True
                    else:
                        attack('none')
                elif FFX_Screen.turnKimahri():
                    if FFX_memory.getUseItemsSlot(40) != 255:
                        useItem(FFX_memory.getUseItemsSlot(40))
                    elif FFX_memory.getUseItemsSlot(27) != 255:
                        useItem(FFX_memory.getUseItemsSlot(27))
                    elif FFX_memory.getUseItemsSlot(39) != 255:
                        useItem(FFX_memory.getUseItemsSlot(39))
                elif FFX_Screen.turnRikku():
                    buddySwapTidus()
                else:
                    defend()
            elif groupNum == 5:
                if FFX_Screen.turnTidus():
                    if not tidusWent:
                        buddySwapRikku()
                        tidusWent = True
                    else:
                        attackByNum(22, 'l')
                elif FFX_Screen.turnRikku():
                    if FFX_memory.getUseItemsSlot(40) != 255:
                        useItem(FFX_memory.getUseItemsSlot(40))
                    elif FFX_memory.getUseItemsSlot(27) != 255:
                        useItem(FFX_memory.getUseItemsSlot(27))
                    elif FFX_memory.getUseItemsSlot(39) != 255:
                        useItem(FFX_memory.getUseItemsSlot(39))
                    elif FFX_Screen.faintCheck() >= 1:
                        revive()
                    else:
                        defend()
                elif FFX_Screen.turnKimahri():
                    buddySwapTidus()
                else:
                    defend()
        FFX_memory.clickToControl()
        if groupNum == 2:
            FFX_memory.fullPartyFormat('guards_lulu')
        else:
            FFX_memory.fullPartyFormat('guards_no_lulu')

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
        gameVars.addRescueCount()
        aeonSummon(2)
        while FFX_memory.battleActive():
            FFX_Xbox.tapB()
    else: #Isaaru/aeon battle
        while not FFX_memory.menuOpen():
            if FFX_memory.turnReady():
                if FFX_Screen.turnYuna():
                    if FFX_memory.getBattleNum() == 260:
                        aeonSummon(2)
                    else:
                        aeonSummon(4)
                else:
                    attack('none')
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    FFXC.set_value('BtnB', 1)
    FFX_memory.waitFrames(30 * 2.8)
    FFXC.set_value('BtnB', 0)
    
    confirm -= 1
    return confirm


def altanaheal():
    direction = 'd'
    if FFX_memory.getThrowItemsSlot(2) < 255:
        itemnum = 2
        itemname = "X-Potion"
    elif FFX_memory.getThrowItemsSlot(8) < 255:
        itemnum = 8
        itemname = "Elixir"
    elif FFX_memory.getThrowItemsSlot(6) < 255:
        itemnum = 6
        itemname = "Phoenix Down"
    elif FFX_memory.getThrowItemsSlot(7) < 255:
        itemnum = 7
        itemname = "Phoenix Down"
    else:
        itemnum = -1
        itemname = "noitemfound"
    if itemnum >= 0:
        FFX_Logs.writeLog("Using %s" % itemname)
        print("Using %s" % itemname)
        while not FFX_memory.turnReady():
            pass
        while FFX_memory.mainBattleMenu():
            if FFX_memory.battleMenuCursor() != 1:
                FFX_Xbox.tapDown()
            else:
                FFX_Xbox.tapB()
        while FFX_memory.mainBattleMenu():
            FFX_Xbox.tapB()
        itemPos = FFX_memory.getThrowItemsSlot(itemnum)
        print("Position: ", itemPos)
        _navigate_to_position(itemPos)
        while FFX_memory.otherBattleMenu():
            FFX_Xbox.tapB()
        print("Direction: ", direction)
        while not FFX_memory.targetingEnemy():
            if direction == 'l':
                FFX_Xbox.tapLeft()
                if not FFX_memory.targetingEnemy():
                    print("Wrong battle line targetted.")
                    FFX_Xbox.tapRight()
                    direction = 'u'
            elif direction == 'r':
                FFX_Xbox.tapRight()
                if not FFX_memory.targetingEnemy():
                    print("Wrong battle line targetted.")
                    FFX_Xbox.tapLeft()
                    direction = 'd'
            elif direction == 'u':
                FFX_Xbox.tapUp()
                if not FFX_memory.targetingEnemy():
                    print("Wrong battle line targetted.")
                    FFX_Xbox.tapDown()
                    direction = 'l'
            elif direction == 'd':
                FFX_Xbox.tapDown()
                if not FFX_memory.targetingEnemy():
                    print("Wrong battle line targetted.")
                    FFX_Xbox.tapUp()
                    direction = 'r'
        tapTargeting()
        return 1

    else:
        print("No restorative items available")
        return 0


def evraeAltana():
    FFX_Logs.writeLog("Fight start: Evrae Altana")
    FFX_Xbox.clickToBattle()
    if FFX_memory.getBattleNum() == 266:
        print("Evrae Altana fight start")
        thrownItem = False
        while not FFX_memory.battleComplete(): #AKA end of battle screen
            if FFX_memory.turnReady():
                if FFX_memory.getItemSlot(18) != 255 and not thrownItem:
                    _useHealingItem(itemID=18)
                    thrownItem = True
                elif FFX_memory.getItemSlot(18) != 255 and not thrownItem:
                    _useHealingItem(itemID=16)
                    thrownItem = True
                else:
                    altanaheal()

    else:  # Just a regular group
        print("Not Evrae this time.")
        fleeAll()
    
    FFX_memory.clickToControl()

def attackHighbridge():
    if FFX_memory.getBattleNum() == 270:
        attackByNum(22, 'r')
    elif FFX_memory.getBattleNum() == 271:
        attackByNum(21, 'l')
    else:
        attack('none')

def seymourNatus_neTesting():
    FFX_Logs.writeLog("Fight start: Highbridge")
    fight = 0
    turn = 0
    aeonSummoned = False
    rng12Manip = FFX_memory.nextChanceRNG12(beforeNatus=True)
    rng10Next = FFX_memory.nextChanceRNG10(30)
    while FFX_memory.battleActive():
        if FFX_memory.getBattleNum() == 272:  # Seymour Natus
            print("Seymour Natus engaged")
            while not FFX_memory.menuOpen():
                if FFX_memory.turnReady() and not aeonSummoned:
                    if FFX_Screen.turnTidus():
                        if FFX_memory.getLuluSlvl() < 35:
                            buddySwapLulu()
                            FFX_Screen.awaitTurn()
                            FFX_Xbox.weapSwap(0)
                        else:
                            attack('none')
                    elif FFX_Screen.turnLulu():
                        buddySwapTidus()
                        FFX_Screen.awaitTurn()
                        FFX_Xbox.tapUp()
                        attack('none')
                    elif FFX_Screen.turnYuna():
                        aeonSummon(4)
                        aeonSummoned = True
                    elif FFX_Screen.turnAeon():
                        FFX_Xbox.SkipDialog(3) #Finishes the fight
                elif FFX_memory.turnReady():
                    attack('none')
            return 1
        else:
            if rng12Manip == 0:
                if FFX_memory.noChanceX3RNG10Highbridge():
                    advanceRNG12()
                elif FFX_memory.nextChanceRNG10(30) >= 1:
                    if FFX_Screen.turnTidus() or FFX_Screen.turnYuna():
                        attackHighbridge()
                    else:
                        fleeAll()
                else:
                    buddySwapRikku()
                    Steal()
                    fleeAll()
            elif rng12Manip >= 1 and rng10Next == 0:
                advanceRNG12()
            else:
                advanceRNG10(FFX_memory.nextChanceRNG10(30))
    
    FFX_memory.clickToControl()    
    FFX_memory.printManipInfo()    
    return 0

def seymourNatus():
    FFX_Logs.writeLog("Fight start: Seymour Natus")
    fight = 0
    turn = 0
    aeonSummoned = False
    while not FFX_memory.userControl():
        if FFX_memory.getBattleNum() == 272:  # Seymour Natus
            print("Seymour Natus engaged")
            fight = 1
            while not FFX_memory.menuOpen():
                if FFX_memory.turnReady() and not aeonSummoned:
                    if FFX_Screen.turnTidus():
                        if FFX_memory.getLuluSlvl() < 35:
                            buddySwapLulu()
                            FFX_Screen.awaitTurn()
                            FFX_Xbox.weapSwap(0)
                        else:
                            attack('none')
                    elif FFX_Screen.turnLulu():
                        buddySwapTidus()
                        FFX_Screen.awaitTurn()
                        FFX_Xbox.tapUp()
                        attack('none')
                    elif FFX_Screen.turnYuna():
                        aeonSummon(4)
                        aeonSummoned = True
                    elif FFX_Screen.turnAeon():
                        FFX_Xbox.SkipDialog(3) #Finishes the fight.
                elif FFX_memory.turnReady():
                    attack('none')
            return 1
            #if FFX_memory.diagSkipPossible():
            #    FFX_Xbox.tapB()  # In case there's any dialog skipping
        elif FFX_memory.getBattleNum() == 270:  # YAT-63 x2
            fight = 4
            while FFX_memory.battleActive():
                if gameVars.completedRescueFights():
                    fleeAll()
                elif FFX_memory.turnReady():
                    if FFX_Screen.turnTidus() or FFX_Screen.turnYuna():
                        if FFX_memory.getEnemyCurrentHP().count(0) == 1:
                            fleeAll()
                            gameVars.addRescueCount()
                        else:
                            attackByNum(22, 'r')                       
                    else:
                        defend()
        elif FFX_memory.getBattleNum() == 269:  # YAT-63 with two guard guys
            fight = 3
            while FFX_memory.battleActive():
                if gameVars.completedRescueFights():
                    fleeAll()
                elif FFX_memory.turnReady():
                    if FFX_Screen.turnTidus() or FFX_Screen.turnYuna():
                        if FFX_memory.getEnemyCurrentHP().count(0) == 1:
                            fleeAll()
                            gameVars.addRescueCount()
                        else:
                            attack('none')                        
                    else:
                        defend()
        elif FFX_memory.getBattleNum() == 271:  # one YAT-63, two YAT-99
            fight = 2
            while FFX_memory.battleActive():
                if gameVars.completedRescueFights():
                    fleeAll()
                elif FFX_memory.turnReady():
                    if FFX_Screen.turnTidus() or FFX_Screen.turnYuna():
                        if FFX_memory.getEnemyCurrentHP().count(0) == 1:
                            fleeAll()
                            gameVars.addRescueCount()
                        else:
                            attackByNum(21, 'l')                       
                    else:
                        defend()
        if FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()            
    return 0

def calmLandsGems():
    FFX_Logs.writeLog("Fight start: Calm Lands Gems")
    print(FFX_memory.getBattleNum())
    print(FFX_memory.getBattleNum())
    print(FFX_memory.getBattleNum())
    FFX_Screen.awaitTurn()
    if FFX_memory.getBattleNum() == [273,281]:  # Red element in center slot, with machina and dog
        print("Grabbing a gem here.")
        buddySwapKimahri()
        StealLeft()
    elif FFX_memory.getBattleNum() in [275,283]:  # Red element in top slot, with bee and tank
        print("Grabbing a gem here.")
        buddySwapKimahri()
        StealDown()
    fleeAll()
    FFX_memory.clickToControl()

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
    
    #Nemesis logic
    if gameVars.nemesis():
        FFX_Screen.awaitTurn()
        StealRight()

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
        FFX_Xbox.tapB()
    
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
    
    gameVars.endGameVersionSet(endGameVersion)

def seymourFlux():
    stage = 1
    print("Start: Seymour Flux battle")
    yunaXP = FFX_memory.getSLVLYuna()
    FFX_Xbox.clickToBattle()
    if gameVars.endGameVersion() == 3:
        bahamutSummoned = False
        while not FFX_memory.battleComplete(): #AKA end of battle screen
            if FFX_memory.turnReady():
                if FFX_Screen.turnTidus():
                    buddySwapYuna()
                elif FFX_Screen.turnYuna():
                    if bahamutSummoned == False:
                        aeonSummon(4)
                        bahamutSummoned = True
                    else:
                        attack('none')
                elif FFX_Screen.turnAeon():
                    if gameVars.getBlitzWin():
                        attack('none')
                    else:
                        impulse()
                elif FFX_Screen.faintCheck() >= 1:
                    revive()
                else:
                    defend()
    else:
        while not FFX_memory.battleComplete(): #AKA end of battle screen
            if FFX_memory.turnReady():
                lastHP = FFX_memory.getEnemyCurrentHP()[0]
                print("Last HP")
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
                        tidusHaste('down', character=1)
                    elif lastHP > 3500:
                        attack('none')
                    else:
                        defend()
                elif FFX_Screen.turnAuron():
                    print("Auron's turn. Swap for Rikku and overdrive.")
                    buddySwapRikku()
                    print("Rikku overdrive")
                    rikkuFullOD('Flux')
                else:
                    print("Non-critical turn. Defending.")
                    defend()
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    FFX_memory.clickToControl()
    if FFX_memory.getSLVLYuna() - yunaXP == 15000:
        gameVars.fluxOverkillSuccess()
    print("------------------------------------")
    print("------------------------------------")
    print("Flux Overkill: ", gameVars.fluxOverkill())
    print("Seymour Flux battle complete.")
    print("------------------------------------")
    print("------------------------------------")
    #time.sleep(60) #Testing only

def sKeeper():
    FFX_Xbox.clickToBattle()
    print("Start of Sanctuary Keeper fight")
    if gameVars.endGameVersion() == 3 and gameVars.getBlitzWin():
        while not FFX_memory.battleComplete():
            if FFX_memory.turnReady():
                if FFX_Screen.turnYuna():
                    aeonSummon(4)
                elif FFX_Screen.turnAeon():
                    attack('none')
                else:
                    defend()
    else:
        armorBreak = False
        while not FFX_memory.battleComplete():
            if FFX_memory.turnReady():
                if FFX_Screen.turnTidus():
                    useSkill(0)
                    armorBreak = True
                elif FFX_Screen.turnYuna():
                    if armorBreak:
                        aeonSummon(4)
                    else:
                        defend()
                elif FFX_Screen.turnAeon():
                    attack('none')
                else:
                    defend()
    FFX_memory.clickToControl()

def caveChargeRikku():
    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            if FFX_Screen.turnRikku():
                attack('none')
            else:
                escapeOne()
    FFX_memory.clickToControl()

def gagazetCave(direction):
    FFX_Screen.awaitTurn()
    attack(direction)
    fleeAll()

def _navigate_to_position(position, battleCursor = FFX_memory.battleCursor2):
    while battleCursor() == 255:
        pass
    if battleCursor() != position:
        print("Wrong position targetted", battleCursor() % 2, position % 2)
        while battleCursor() % 2 != position % 2:
            if battleCursor() < position:
                FFX_Xbox.tapRight()
            else:
                FFX_Xbox.tapLeft()
        while battleCursor() != position:
            print(battleCursor())
            if battleCursor() > position:
                FFX_Xbox.tapUp()
            else:
                FFX_Xbox.tapDown()

def useItem(slot: int, direction = 'none', target = 255, rikkuFlee=False):
    FFX_Logs.writeLog("Using items via the Use command")
    print("Using items via the Use command")
    print("Item slot: ", slot)
    print("Direction: ", direction)
    while not FFX_memory.mainBattleMenu():
        pass
    print("Mark 1")
    while FFX_memory.battleMenuCursor() != 20:
        if FFX_Screen.turnRikku() == False and FFX_Screen.turnKimahri() == False:
            return
        if FFX_memory.battleMenuCursor() == 1:
            FFX_Xbox.tapUp()
        elif FFX_memory.battleMenuCursor() > 20:
            FFX_Xbox.tapUp()
        else:
            FFX_Xbox.tapDown()
    while FFX_memory.mainBattleMenu():
        FFX_Xbox.tapB()
    print("Mark 2")
    if rikkuFlee:
        _navigate_to_position(2)
    else:
        _navigate_to_position(1)
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    print("Mark 3")
    _navigate_to_position(slot, FFX_memory.battleCursor3)
    while FFX_memory.interiorBattleMenu():
        FFX_Xbox.tapB()
    if target != 255:
        try:
            print("Targetting based on character number")
            if target >= 20 and FFX_memory.getEnemyCurrentHP()[target - 20] != 0:
                direction = 'l'
                while FFX_memory.battleTargetId() != target:
                    if FFX_memory.battleTargetId() < 20:
                        FFX_Xbox.tapRight()
                        direction = 'u'
                    elif direction == 'u':
                        FFX_Xbox.tapUp()
                    else:
                        FFX_Xbox.tapLeft()
            elif target < 20 and target != 0:
                direction = 'l'
                while FFX_memory.battleTargetId() != target:
                    if FFX_memory.battleTargetId() >= 20:
                        FFX_Xbox.tapRight()
                        direction = 'u'
                    elif direction == 'u':
                        FFX_Xbox.tapUp()
                    else:
                        FFX_Xbox.tapLeft()
            elif target == 0:
                direction = 'l'
                while FFX_memory.battleTargetId() != 0:
                    if FFX_memory.battleTargetId() >= 20:
                        FFX_Xbox.tapRight()
                        direction = 'u'
                    elif direction == 'u':
                        FFX_Xbox.tapUp()
                    else:
                        FFX_Xbox.tapLeft()
                        
            tapTargeting()
        except:
            FFX_Xbox.tapB()
            FFX_Xbox.tapB()
            FFX_Xbox.tapB()
            FFX_Xbox.tapB()
            FFX_Xbox.tapB()
            FFX_Xbox.tapB()
    elif direction == 'none':
        print("No direction variation")
        tapTargeting()
    else:
        print("Direction variation: ", direction)
        if direction == 'left':
            FFX_Xbox.tapLeft()
        elif direction == 'right':
            FFX_Xbox.tapRight()
        elif direction == 'up':
            FFX_Xbox.tapUp()
        elif direction == 'down':
            FFX_Xbox.tapDown()
        tapTargeting()

def useItemTidus(slot: int, direction = 'none', target = 255):
    FFX_Logs.writeLog("Using items via the Use command")
    print("Using items via the Use command")
    print("Item slot: ", slot)
    print("Direction: ", direction)
    while not FFX_memory.mainBattleMenu():
        pass
    print("Mark 1")
    while FFX_memory.battleMenuCursor() != 20:
        if FFX_Screen.turnTidus() == False:
            return
        if FFX_memory.battleMenuCursor() == 1:
            FFX_Xbox.tapUp()
        elif FFX_memory.battleMenuCursor() > 20:
            FFX_Xbox.tapUp()
        else:
            FFX_Xbox.tapDown()
    while FFX_memory.mainBattleMenu():
        FFX_Xbox.tapB()
    print("Mark 2")
    _navigate_to_position(2)
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    print("Mark 3")
    _navigate_to_position(slot, FFX_memory.battleCursor3)
    while FFX_memory.interiorBattleMenu():
        FFX_Xbox.tapB()
    if target != 255:
        try:
            print("Targetting based on character number")
            if target >= 20 and FFX_memory.getEnemyCurrentHP()[target - 20] != 0:
                direction = 'l'
                while FFX_memory.battleTargetId() != target:
                    if FFX_memory.battleTargetId() < 20:
                        FFX_Xbox.tapRight()
                        direction = 'u'
                    elif direction == 'u':
                        FFX_Xbox.tapUp()
                    else:
                        FFX_Xbox.tapLeft()
            elif target < 20 and target != 0:
                direction = 'l'
                while FFX_memory.battleTargetId() != target:
                    if FFX_memory.battleTargetId() >= 20:
                        FFX_Xbox.tapRight()
                        direction = 'u'
                    elif direction == 'u':
                        FFX_Xbox.tapUp()
                    else:
                        FFX_Xbox.tapLeft()
            elif target == 0:
                direction = 'l'
                while FFX_memory.battleTargetId() != 0:
                    if FFX_memory.battleTargetId() >= 20:
                        FFX_Xbox.tapRight()
                        direction = 'u'
                    elif direction == 'u':
                        FFX_Xbox.tapUp()
                    else:
                        FFX_Xbox.tapLeft()
                        
            tapTargeting()
        except:
            FFX_Xbox.tapB()
            FFX_Xbox.tapB()
            FFX_Xbox.tapB()
            FFX_Xbox.tapB()
            FFX_Xbox.tapB()
            FFX_Xbox.tapB()
    elif direction == 'none':
        print("No direction variation")
        tapTargeting()
    else:
        print("Direction variation: ", direction)
        if direction == 'left':
            FFX_Xbox.tapLeft()
        elif direction == 'right':
            FFX_Xbox.tapRight()
        elif direction == 'up':
            FFX_Xbox.tapUp()
        elif direction == 'down':
            FFX_Xbox.tapDown()
        tapTargeting()

def cheer():
    FFX_Logs.writeLog("Cheer command")
    print("Cheer command")
    while FFX_memory.battleMenuCursor() != 20:
        if FFX_Screen.turnTidus() == False:
            return
        if FFX_memory.battleMenuCursor() == 0:
            FFX_Xbox.tapDown()
        else:
            FFX_Xbox.tapUp()
    while not FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    _navigate_to_position(1)
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    tapTargeting()


def seymourSpell():
    print("Seymour casting tier 2 spell")
    num = 21 #Should be the enemy number for the head
    if not FFX_memory.turnReady():
        print("Battle menu isn't up.")
        FFX_Screen.awaitTurn()
    
    while FFX_memory.battleMenuCursor() != 21:
        print(FFX_memory.battleMenuCursor())
        if FFX_memory.battleMenuCursor() == 0:
            FFX_Xbox.tapDown()
        else:
            FFX_Xbox.tapUp()
    while FFX_memory.mainBattleMenu():
        FFX_Xbox.tapB()  # Black magic
    print(FFX_memory.battleCursor2())
    _navigate_to_position(5)
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    
    if FFX_memory.getEnemyCurrentHP()[num - 20] != 0: #Target head if alive.
        while FFX_memory.battleTargetId() != num:
            FFX_Xbox.tapLeft()
            
    tapTargeting()

def _useHealingItem(num=None, direction='l', itemID=0):
    print("Healing character, ", num)
    direction = direction.lower()
    while not FFX_memory.turnReady():
        print("Battle menu isn't up.")
        pass
    while not FFX_memory.mainBattleMenu():
        pass
    while FFX_memory.battleMenuCursor() != 1:
        FFX_Xbox.tapDown()
    while FFX_memory.mainBattleMenu():
        FFX_Xbox.tapB()
    while not FFX_memory.otherBattleMenu():
        pass
    print(FFX_memory.battleCursor2())
    print(FFX_memory.getThrowItemsSlot(itemID))
    _navigate_to_position(FFX_memory.getThrowItemsSlot(itemID))
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    if num is not None:
        while FFX_memory.battleTargetId() != num:
            if direction == 'l':
                if FFX_memory.battleTargetId() >= 20:
                    print("Wrong battle line targetted.")
                    FFX_Xbox.tapRight()
                    direction = 'u'
                else:
                    FFX_Xbox.tapLeft()
            elif direction == 'r':
                if FFX_memory.battleTargetId() >= 20:
                    print("Wrong character targetted.")
                    FFX_Xbox.tapLeft()
                    direction = 'd'
                else:
                    FFX_Xbox.tapRight()
            elif direction == 'u':
                if FFX_memory.battleTargetId() >= 20:
                    print("Wrong character targetted.")
                    FFX_Xbox.tapDown()
                    direction = 'l'
                else:
                    FFX_Xbox.tapUp()
            elif direction == 'd':
                if FFX_memory.battleTargetId() >= 20:
                    print("Wrong character targetted.")
                    FFX_Xbox.tapUp()
                    direction = 'r'
                else:
                    FFX_Xbox.tapDown()
    tapTargeting()

def usePotionCharacter(num, direction):
    print("Healing character, ", num)
    _useHealingItem(num=num, direction=direction, itemID=0)

def attackByNum(num, direction='u'):
    print("Attacking specific character, ", num)
    direction = direction.lower()
    if not FFX_memory.turnReady():
        print("Battle menu isn't up.")
        while not FFX_memory.turnReady():
            #Waiting for battle menu to come up.
            pass
         #Make sure we actually have control
    if FFX_memory.battleMenuCursor() != 0 and FFX_memory.battleMenuCursor() != 216:
        while not FFX_memory.battleMenuCursor() in [0, 216]:
            FFX_Xbox.tapUp()
            if FFX_Screen.BattleComplete():
                return #Safety
    while FFX_memory.mainBattleMenu():
        FFX_Xbox.tapB()
    
    if FFX_memory.getEnemyCurrentHP()[num - 20] != 0:
        while FFX_memory.battleTargetId() != num:
            if direction == 'l':
                if FFX_memory.battleTargetId() < 20:
                    direction = 'u'
                FFX_Xbox.tapLeft()
            elif direction == 'r':
                if FFX_memory.battleTargetId() < 20:
                    direction = 'd'
                FFX_Xbox.tapRight()
            elif direction == 'u':
                if FFX_memory.battleTargetId() < 20:
                    direction = 'l'
                FFX_Xbox.tapUp()
            elif direction == 'd':
                if FFX_memory.battleTargetId() < 20:
                    direction = 'r'
                FFX_Xbox.tapDown()
    tapTargeting()

def attackSelfTanker():
    print("Attacking specific character, Auron (self)")
    if not FFX_memory.turnReady():
        print("Battle menu isn't up.")
        while not FFX_memory.turnReady():
            #Waiting for battle menu to come up.
            pass
    if FFX_memory.battleMenuCursor() != 0 and FFX_memory.battleMenuCursor() != 216:
        while not FFX_memory.battleMenuCursor() in [0, 216]:
            FFX_Xbox.tapUp()
            if FFX_Screen.BattleComplete():
                return #Safety
    while FFX_memory.mainBattleMenu():
        FFX_Xbox.tapB()
    while FFX_memory.battleTargetId() != 2:
        if FFX_memory.battleTargetId() > 20:
            FFX_Xbox.tapDown()
        else:
            FFX_Xbox.tapLeft()
    tapTargeting()

def oblitzRngWait():
    if FFX_memory.rngSeed() != 31:
        return False
    if gameVars.usePause():
        fullRngList = [-936146351, 783164740, -433527773, 298578755, 1709935847, -928539788, 566589561, -348814187, -1953896653, 1467711668, 2021978880, 1051281977, 58046422, -49080059, 832181030, -582803672, -919546980, -944931993, -1691878525, -676599964, 190150946, -635005377, -1472231111, 980825690, 1748967869, 2131880750, -1777695758, -577305152, 1072229501, -263086907, 735722232, 98610709, -787863605, 1876162930, 253163151, -55561781, -2116790766, -457792397, -1960937765, 1900305980, 332190114, -291030536, 2095135700, -257601274, -1516062954, -556593345, 155185062, -1916624866, 681247051, 1163128705, 1006522324, -1935370802, -1045783984, 580455735, 1033351229, -1450036323, -596521206, 617577836, 1377642898, -1003061117, -2069128403, 174192090, -1279316923, 794425718, -5042938, 1503882547, 763110694, 1061375372, -1891856333, 1081850723, -359912819, -2134745985, -402660695, -716858602, 1523757657, -803832703, 1358833959, -144149980, -1013659464, 1361125441, 1782454472, 1280391322, -855716004, -1309857057, 501223935, -1719675399, -323599442, -1165299850, 1169366007, -1831316087, 849721475, -1666466051, 248624608, 1955148740, 1312079881, 556171044, -124467772, 674570695]
        goodRngList = [-1472231111, 980825690, 1782454472]
        # 980825690 > 2131880750 is not so good.
        # 980825690 > 1748967869 is not so good.
    else:
        goodRngList = [0]
    
    waitCounter = 0
    lastRng02 = FFX_memory.rng02()
    FFX_Logs.writeStats("====================================")
    while waitCounter != 100 and not FFX_memory.s32(FFX_memory.rng02()) in goodRngList:
        print(waitCounter, " | ", FFX_memory.s32(lastRng02))
        if FFX_memory.s32(FFX_memory.rng02()) != FFX_memory.s32(lastRng02):
            FFX_Logs.writeStats(str(waitCounter) + " | " + str(FFX_memory.s32(FFX_memory.rng02())))
            lastRng02 = FFX_memory.rng02()
            waitCounter += 1
    FFX_Logs.writeStats("====================================")
    if waitCounter < 100:
        return True
    return False

def attackOblitzEnd():
    print("Attack")
    if not FFX_memory.turnReady():
        while not FFX_memory.turnReady():
            pass
    while FFX_memory.mainBattleMenu():
        if not FFX_memory.battleMenuCursor() in [0, 203, 210, 216]:
            print(FFX_memory.battleMenuCursor(), ", Battle Menu Cursor")
            FFX_Xbox.tapUp()
        elif FFX_Screen.BattleComplete():
            return
        else:
            FFX_Xbox.menuB()
    FFX_memory.waitFrames(1)
    rngWaitResults = oblitzRngWait()
    FFX_memory.waitFrames(1)
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    print("Oblitz RNG wait results: ", oblitzRngWait)
    FFX_Logs.writeStats("RNG02 on attack:")
    FFX_Logs.writeStats(FFX_memory.s32(FFX_memory.rng02()))

def attack(direction="none"):
    print("Attack")
    direction = direction.lower()
    if not FFX_memory.turnReady():
        while not FFX_memory.turnReady():
            pass
    while FFX_memory.mainBattleMenu():
        if not FFX_memory.battleMenuCursor() in [0, 203, 210, 216]:
            print(FFX_memory.battleMenuCursor(), ", Battle Menu Cursor")
            FFX_Xbox.tapUp()
        elif FFX_Screen.BattleComplete():
            return
        else:
            FFX_Xbox.tapB()
    if direction == "left":
        FFX_Xbox.tapLeft()
    if direction == "right":
        FFX_Xbox.tapRight()
    if direction == "r2":
        FFX_Xbox.tapRight()
        FFX_Xbox.tapRight()
    if direction == "r3":
        FFX_Xbox.tapRight()
        FFX_Xbox.tapRight()
        FFX_Xbox.tapRight()
    if direction == "up":
        FFX_Xbox.tapUp()
    if direction == "down":
        FFX_Xbox.tapDown()
    tapTargeting()

def _steal(direction=None):
    if not FFX_memory.mainBattleMenu():
        while not FFX_memory.mainBattleMenu():
            pass
    while FFX_memory.battleMenuCursor() != 20:
        if FFX_Screen.turnRikku() == False and FFX_Screen.turnKimahri() == False:
            return            
        if FFX_memory.battleMenuCursor() == 1:
            FFX_Xbox.tapUp()
        elif FFX_memory.battleMenuCursor() > 20:
            FFX_Xbox.tapUp()
        else:
            FFX_Xbox.tapDown()
    while not FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    _navigate_to_position(0)
    print(FFX_memory.otherBattleMenu())
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()  # Use the Steal
    print(FFX_memory.otherBattleMenu())
    if direction == 'down':
        FFX_Xbox.tapDown()
    elif direction == 'up':
        FFX_Xbox.tapUp()
    elif direction == 'right':
        FFX_Xbox.tapRight()
    elif direction == 'left':
        FFX_Xbox.tapLeft()    
    print("Firing steal")
    tapTargeting()

def Steal():
    FFX_Logs.writeLog("Basic Steal command")
    print("Steal")
    if not FFX_memory.getBattleNum() in [273,274,276,279,281,282,284,289]:
        _steal()
    elif FFX_memory.getBattleNum() in [273,281]:
        _steal('left')
    elif FFX_memory.getBattleNum() in [276,279,289]:
        _steal('up')
    else:
        _steal()

def StealDown():
    FFX_Logs.writeLog("Steal, but press Down")
    print("Steal Down")
    _steal('down')

def StealUp():
    FFX_Logs.writeLog("Steal, but press Up")
    print("Steal Up")
    _steal('up')


def StealRight():
    FFX_Logs.writeLog("Steal, but press Right")
    print("Steal Right")
    _steal('right')


def StealLeft():
    FFX_Logs.writeLog("Steal, but press Left")
    print("Steal Left")
    _steal('left')


def stealAndAttack():
    print("Steal/Attack function")
    FFXC.set_neutral()
    FFX_Screen.awaitTurn()
    while not FFX_memory.battleComplete(): 
        if FFX_memory.turnReady():
            if FFX_Screen.turnRikku():
                grenadeSlot = FFX_memory.getItemSlot(35)
                grenadeCount = FFX_memory.getItemCountSlot(grenadeSlot)
                if grenadeCount < 6:
                    Steal()
                else:
                    attack('none')
            if FFX_Screen.turnTidus():
                attack('none')
        elif FFX_memory.otherBattleMenu():
            FFX_Xbox.tapB()
    FFX_memory.clickToControl()


def stealAndAttackPreTros():
    print("Steal/Attack function before Tros")
    BattleComplete = 0
    turnCounter = 0
    FFXC.set_neutral()
    while not FFX_memory.battleComplete():
        if FFX_memory.turnReady():
            if FFX_Screen.turnRikkuRed():
                turnCounter += 1
                if turnCounter == 1:
                    grenadeSlot = FFX_memory.getItemSlot(35)
                    grenadeCount = FFX_memory.getItemCountSlot(grenadeSlot)
                    if grenadeCount < 6:
                        Steal()
                    else:
                        attack('none')
                if turnCounter == 2:
                    grenadeSlot = FFX_memory.getItemSlot(35)
                    grenadeCount = FFX_memory.getItemCountSlot(grenadeSlot)
                    if grenadeCount < 6:
                        StealDown()
                    else:
                        attack('none')
                else:
                    attack('none')
            if FFX_Screen.turnTidus():
                attack('none')
        elif FFX_memory.otherBattleMenu():
            FFX_Xbox.tapB()
    FFX_memory.clickToControl()


def castSpell(direction, spellID):
    if FFX_Screen.turnLulu() == False:
        print("Lulu is not the current person. Deferring turn.")
        return
    while FFX_memory.battleMenuCursor() != 21:
        print(FFX_memory.battleMenuCursor())
        if FFX_memory.battleMenuCursor() == 0:
            FFX_Xbox.tapDown()
        else:
            FFX_Xbox.tapUp()
    while FFX_memory.mainBattleMenu():
        FFX_Xbox.tapB()  # Black magic
    _navigate_to_position(spellID)
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()  # Cast the Spell
    direction = direction.lower()
    if direction == "right":
        FFX_Xbox.tapRight()
    elif direction == "left":
        FFX_Xbox.tapLeft()
    elif direction == "up":
        FFX_Xbox.tapUp()
    elif direction == "down":
        FFX_Xbox.tapDown()
    elif direction == "l2":
        FFX_Xbox.tapLeft()
        FFX_Xbox.tapLeft()
    elif direction == "rd":
        FFX_Xbox.tapRight()
        FFX_Xbox.tapDown()
    elif direction == "right2" or direction == "r2":
        FFX_Xbox.tapRight()
        FFX_Xbox.tapRight()
        FFX_Xbox.tapDown()
    elif direction == "d2":
        FFX_Xbox.tapDown()
        FFX_Xbox.tapDown()
    elif not direction or direction == 'none':
        pass
    else:
        print("UNSURE DIRECTION: ", direction)
        raise ValueError("Unsure direction")
    tapTargeting()

    

def thunder(direction="none"):
    FFX_Logs.writeLog("Lulu cast Thunder")
    print("Black magic - Thunder")
    castSpell(direction, 1)


def fire(direction="none"):
    FFX_Logs.writeLog("Lulu cast Fire")
    print("Black magic - Fire")
    castSpell(direction, 0)
 

def water(direction="none"):
    FFX_Logs.writeLog("Lulu cast Water")
    print("Black magic - Water")
    castSpell(direction, 2)


def ice(direction="none"):
    FFX_Logs.writeLog("Lulu cast Ice")
    print("Black magic - Ice")
    castSpell(direction, 3)

def thunderTarget(target, direction):
    FFX_Logs.writeLog("Lulu cast Thunder")
    print("Black magic - Thunder")
    if FFX_Screen.turnLulu() == False:
        print("Lulu is not the current person. Deferring turn.")
        return
    direction = direction.lower()
    while FFX_memory.mainBattleMenu():
        if FFX_memory.battleMenuCursor() != 21:
            print(FFX_memory.battleMenuCursor())
            if FFX_memory.battleMenuCursor() == 0:
                FFX_Xbox.tapDown()
            else:
                FFX_Xbox.tapUp()
        else:
            FFX_Xbox.tapB()
    print(FFX_memory.battleCursor2())
    _navigate_to_position(1)
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()  # Thunder
    while FFX_memory.battleTargetId() != target:
        if direction == 'l':
            if FFX_memory.battleTargetId() < 20:
                print("Wrong battle line targetted.")
                FFX_Xbox.tapRight()
                direction = 'u'
            else:
                FFX_Xbox.tapLeft()
        elif direction == 'r':
            if FFX_memory.battleTargetId() < 20:
                print("Wrong character targetted.")
                FFX_Xbox.tapLeft()
                direction = 'd'
            else:
                FFX_Xbox.tapRight()
        elif direction == 'u':
            if FFX_memory.battleTargetId() < 20:
                print("Wrong character targetted.")
                FFX_Xbox.tapDown()
                direction = 'l'
            else:
                FFX_Xbox.tapUp()
        elif direction == 'd':
            if FFX_memory.battleTargetId() < 20:
                print("Wrong character targetted.")
                FFX_Xbox.tapUp()
                direction = 'r'
            else:
                FFX_Xbox.tapDown()
    tapTargeting()


def aeonSummon(position):
    FFX_Logs.writeLog("Aeon is being summoned. " + str(position) + "")
    print("Aeon is being summoned. " + str(position) + "")
    while not FFX_memory.mainBattleMenu():
        pass
    while FFX_memory.battleMenuCursor() != 23:
        if FFX_Screen.turnYuna() == False:
            return
        if FFX_memory.battleMenuCursor() == 255:
            pass
        elif FFX_memory.battleMenuCursor() >= 1 and FFX_memory.battleMenuCursor() < 23:
            FFX_Xbox.tapUp()
        else:
            FFX_Xbox.tapDown()
    while FFX_memory.mainBattleMenu():
        FFX_Xbox.tapB()
    while position != FFX_memory.battleCursor2():
        print(FFX_memory.battleCursor2())
        if FFX_memory.battleCursor2() < position:
            FFX_Xbox.tapDown()
        else:
            FFX_Xbox.tapUp()
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    aeonWaitTimer = 0
    while not FFX_memory.turnReady():
        if aeonWaitTimer % 10000 == 0:
            print("Waiting for Aeon's turn. ", int(aeonWaitTimer % 10000))
        pass
        aeonWaitTimer += 1


def aeonSpell(position):
    aeonSpellDirection(position, None)


def aeonSpell2(position, direction):
    aeonSpellDirection(position, direction)


def aeonSpellDirection(position, direction):
    FFX_Logs.writeLog("Aeon casting a spell. Special direction: " + str(direction))
    print("Aeon casting a spell. Special direction: ", direction)
    while FFX_memory.battleMenuCursor() != 21:
        FFX_Xbox.tapDown()
    while FFX_memory.mainBattleMenu():
        FFX_Xbox.tapB()  # Black magic
    print("In Black Magic")
    _navigate_to_position(position)
    print(FFX_memory.otherBattleMenu())
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()  # Cast the Spell
    print(FFX_memory.otherBattleMenu())
    if direction == 'left':
        FFX_Xbox.tapLeft()
    elif direction == 'right':
        FFX_Xbox.tapRight()
    elif direction == 'up':
        FFX_Xbox.tapUp()
    elif direction == 'down':
        FFX_Xbox.tapDown()
    tapTargeting()
    print("Aeon casting spell")


def healUp_New(chars, menusize):
    healUp(chars)

def healUp(chars=3, *, fullMenuClose=True):
    FFX_Logs.writeLog("Healing characters post-battle")
    print("Menuing, healing characters: ", chars)
    if FFX_memory.getHP() == FFX_memory.getMaxHP():
        print("No need to heal. Exiting menu.")
        print(FFX_memory.menuNumber())
        if fullMenuClose:
            FFX_memory.closeMenu()
        else:
            if FFX_memory.menuOpen():
                FFX_memory.backToMainMenu()
        return
    if not FFX_memory.menuOpen():
        FFX_memory.openMenu()
    FFXC = FFX_Xbox.controllerHandle()
    FFXC.set_neutral()
    while FFX_memory.getMenuCursorPos() != 2:
        print("Selecting Ability command - ", FFX_memory.getMenuCursorPos())
        FFX_memory.menuDirection(FFX_memory.getMenuCursorPos(), 2, 11)
    while FFX_memory.menuNumber() == 5:
        print("Select Ability - ", FFX_memory.menuNumber())
        FFX_Xbox.tapB()
    print("Mark 1")
    target_pos = FFX_memory.getCharacterIndexInMainMenu(1)
    print(target_pos)
    while FFX_memory.getCharCursorPos() != target_pos:
        FFX_memory.menuDirection(FFX_memory.getCharCursorPos(), target_pos, len(FFX_memory.getOrderSeven()))
    print("Mark 2")
    while FFX_memory.menuNumber() != 26:
        if FFX_memory.getMenu2CharNum() == 1:
            FFX_Xbox.tapB()
        else:
            FFX_Xbox.tapDown()
    while not FFX_memory.cureMenuOpen():
        FFX_Xbox.tapB()
    character_positions = {
        0 : FFX_memory.getCharFormationSlot(0), # Tidus
        1 : FFX_memory.getCharFormationSlot(1), # Yuna
        2 : FFX_memory.getCharFormationSlot(2), # Auron
        3 : FFX_memory.getCharFormationSlot(3), # Kimahri
        4 : FFX_memory.getCharFormationSlot(4), # Wakka
        5 : FFX_memory.getCharFormationSlot(5), # Lulu
        6 : FFX_memory.getCharFormationSlot(6) # Rikku
    }
    print(character_positions)
    positions_to_characters = { val : key for key, val in character_positions.items() if val != 255 }
    print(positions_to_characters)
    maximal_hp = FFX_memory.getMaxHP()
    print("Max HP: ", maximal_hp)
    current_hp = FFX_memory.getHP()
    for cur_position in range(len(positions_to_characters)):
        while current_hp[positions_to_characters[cur_position]] < maximal_hp[positions_to_characters[cur_position]]:
            print(current_hp)
            prev_hp = current_hp[positions_to_characters[cur_position]]
            while FFX_memory.assignAbilityToEquipCursor() != cur_position:
                if FFX_memory.assignAbilityToEquipCursor() < cur_position:
                    FFX_Xbox.tapDown()
                else:
                    FFX_Xbox.tapUp()
            FFX_Xbox.tapB()
            current_hp = FFX_memory.getHP()
        if current_hp == maximal_hp or FFX_memory.getYunaMP() < 4: break
    print("Healing complete. Exiting menu.")
    print(FFX_memory.menuNumber())
    if fullMenuClose:
        FFX_memory.closeMenu()
    else:
        FFX_memory.backToMainMenu()

def healUpMiihen(chars):
    healUp(chars)


def lancetSwap(direction):
    print("Lancet Swap function")
    # Assumption is formation: Tidus, Wakka, Auron, Kimahri, and Yuna in last slot.
    direction = direction.lower()
    buddySwapKimahri()

    lancet(direction)
    
    FFX_Screen.awaitTurn()
    fleeAll()

def lancet(direction):
    print("Casting Lancet with variation: ", direction)
    while FFX_memory.battleMenuCursor() != 20:
        if FFX_memory.battleMenuCursor() == 255:
            pass
        elif FFX_memory.battleMenuCursor() == 1:
            FFX_Xbox.tapUp()
        elif FFX_memory.battleMenuCursor() > 20:
            FFX_Xbox.tapUp()
        else:
            FFX_Xbox.tapDown()
    while FFX_memory.mainBattleMenu():
        FFX_Xbox.tapB()
    _navigate_to_position(0)
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    if direction == 'left':
        FFX_Xbox.tapLeft()
    if direction == 'right':
        FFX_Xbox.tapRight()
    if direction == 'up':
        FFX_Xbox.tapUp()
    if direction == 'down':
        FFX_Xbox.tapDown()
    tapTargeting()

def lancetTarget(target, direction):
    print("Casting Lancet with variation: ", direction)
    while FFX_memory.battleMenuCursor() != 20:
        if FFX_memory.battleMenuCursor() == 255:
            pass
        elif FFX_memory.battleMenuCursor() == 1:
            FFX_Xbox.tapUp()
        elif FFX_memory.battleMenuCursor() > 20:
            FFX_Xbox.tapUp()
        else:
            FFX_Xbox.tapDown()
    while FFX_memory.mainBattleMenu():
        FFX_Xbox.tapB()
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    retry = 0
    while FFX_memory.battleTargetId() != target:
        if direction == 'l':
            if retry > 5:
                retry = 0
                print("Wrong battle line targetted.")
                FFX_Xbox.tapRight()
                direction = 'u'
                retry = 0
            else:
                FFX_Xbox.tapLeft()
        elif direction == 'r':
            if retry > 5:
                retry = 0
                print("Wrong character targetted.")
                FFX_Xbox.tapLeft()
                direction = 'd'
            else:
                FFX_Xbox.tapRight()
        elif direction == 'u':
            if retry > 5:
                retry = 0
                print("Wrong character targetted.")
                FFX_Xbox.tapDown()
                direction = 'l'
            else:
                FFX_Xbox.tapUp()
        elif direction == 'd':
            if retry > 5:
                retry = 0
                print("Wrong character targetted.")
                FFX_Xbox.tapUp()
                direction = 'r'
            else:
                FFX_Xbox.tapDown()
        retry += 1
    
    tapTargeting()

def lancetHome(direction):
    print("Lancet (home) function")
    while FFX_memory.battleMenuCursor() != 20:
        if FFX_memory.battleMenuCursor() == 255:
            pass
        elif FFX_memory.battleMenuCursor() == 1:
            FFX_Xbox.tapUp()
        elif FFX_memory.battleMenuCursor() > 20:
            FFX_Xbox.tapUp()
        else:
            FFX_Xbox.tapDown()
    while FFX_memory.mainBattleMenu():
        FFX_Xbox.tapB()
    _navigate_to_position(2)
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    if direction == 'left':
        FFX_Xbox.tapLeft()
    if direction == 'right':
        FFX_Xbox.tapRight()
    if direction == 'up':
        FFX_Xbox.tapUp()
    if direction == 'down':
        FFX_Xbox.tapDown()
    tapTargeting()

def checkTidusOk():
    return not any(func(0) for func in [FFX_memory.petrifiedstate, FFX_memory.confusedState, \
        FFX_memory.deadstate, FFX_memory.berserkstate])

def checkYunaOk():
    return not any(func(1) for func in [FFX_memory.petrifiedstate, FFX_memory.confusedState, \
        FFX_memory.deadstate, FFX_memory.berserkstate])

def fleeAll():
    FFX_Logs.writeLog("Fleeing from battle, prior to Mt Gagazet")
    print("Attempting escape (all party members and end screen)")
    if FFX_memory.battleActive():
        while FFX_memory.battleActive():
            if FFX_memory.userControl():
                return
            if FFX_memory.turnReady():
                tidus_position =  FFX_memory.getBattleCharSlot(0)
                print("Tidus Position: ", tidus_position)
                if FFX_Screen.turnTidus():
                    tidusFlee()
                elif checkTidusOk() and tidus_position >= 3 and tidus_position != 255:
                    buddySwapTidus()
                elif not checkTidusOk() or tidus_position == 255 or FFX_memory.tidusEscapedState():
                    escapeOne()
                else:
                    defend()  
    FFX_memory.clickToControl3()
    print("Flee complete")

def fleeLateGame():
    fleeAll()

def escapeAll():
    print("escapeAll function")
    while not FFX_Screen.BattleComplete():
        if FFX_memory.turnReady():
            escapeOne()

def escapeOne():
    FFX_Logs.writeLog("Character attempting escape")
    print("Attempting escape, one person")
    while FFX_memory.mainBattleMenu():
        if FFX_memory.battleComplete():
            break
        else:
            FFX_Xbox.tapRight()
    print("In other battle menu")
    while FFX_memory.battleCursor2() != 2:
        if FFX_memory.battleComplete():
            break
        else:
            FFX_Xbox.tapDown()
    print("Targeted Escape")
    while FFX_memory.otherBattleMenu():
        if FFX_memory.battleComplete():
            break
        else:
            FFX_Xbox.tapB()
    if FFX_memory.battleActive():
        print("Selected Escaping")
        tapTargeting()

def buddySwap_char(character):
    FFX_memory.waitFrames(6)
    FFX_Logs.writeLog("Swapping characters (in battle)")
    print("Swapping characters (in battle) - by char num")
    position = FFX_memory.getBattleCharSlot(character)
    
    #Special logic for after selfDestruct
    if FFX_memory.getBattleNum() == 116 and character == 1:
        position += 1
    
    if position < 3:
        print("Cannot swap with character ", FFX_memory.nameFromNumber(character), \
            ", that character is in the front party.")
        return
    else:
        while not FFX_memory.otherBattleMenu():
            FFX_Xbox.lBumper()
        position -= 3
        reserveposition = position % 4
        print("Character is in position ", reserveposition)
        if reserveposition == 3:  # Swap with last slot
            direction = 'up'
        else:
            direction = 'down'
        
        while reserveposition != FFX_memory.battleCursor2():
            if direction == 'down':
                FFX_Xbox.tapDown()
            else:
                FFX_Xbox.tapUp()
                
        while FFX_memory.otherBattleMenu():
            FFX_Xbox.tapB()
        FFX_Xbox.clickToBattle()
        FFX_Screen.awaitTurn()
        return

def buddySwapTidus():
    print("++Swapping in Tidus")
    buddySwap_char(0)

def buddySwapYuna():
    print("++Swapping in Yuna")
    buddySwap_char(1)

def buddySwapAuron():
    print("++Swapping in Auron")
    buddySwap_char(2)

def buddySwapKimahri():
    print("++Swapping in Kimahri")
    buddySwap_char(3)

def buddySwapWakka():
    print("++Swapping in Wakka")
    buddySwap_char(4)

def buddySwapLulu():
    print("++Swapping in Lulu")
    buddySwap_char(5)

def buddySwapRikku():
    print("++Swapping in Rikku")
    buddySwap_char(6)

def kimahriOD(pos):
    FFX_Logs.writeLog("Kimahri using Overdrive")
    print("Kimahri using Overdrive, pos - ", pos)
    while not FFX_memory.otherBattleMenu():
        FFX_Xbox.tapLeft()
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    _navigate_to_position(pos, battleCursor=FFX_memory.battleCursor3)
    while FFX_memory.interiorBattleMenu():
        FFX_Xbox.tapB()
    tapTargeting()

def wrapUp():
    print("^^Wrapping up battle.")
    while not FFX_memory.userControl():
        if FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
        elif FFX_memory.turnReady():
            print("^^Still someone's turn. Could not wrap up battle.")
            return False
        else:
            pass
    print("^^Wrap up complete.")
    return True

def impulse(direction=None, targetFarLine=False):
    while FFX_memory.battleMenuCursor() != 217:
        if FFX_memory.battleMenuCursor() == 216:
            FFX_Xbox.tapDown()
        else:
            FFX_Xbox.tapUp()
    while not FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    if direction == 'left':
        FFX_Xbox.tapLeft()
    if targetFarLine:
        while not FFX_memory.battleLineTarget():
            FFX_Xbox.tapLeft()
    tapTargeting()
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()

def SinArms():
    FFX_Logs.writeLog("Fight start: Sin's Arms")
    print("Fight start: Sin's Arms")
    # Area for improvement later. Multiple skippable FMVs
    FFX_Xbox.clickToBattle()
    aeonSummon(4)
    while FFX_memory.battleActive(): #Arm1
        if FFX_memory.turnReady():
            impulse()
            FFX_Xbox.tapB()
            FFX_Xbox.tapB()
        else:
            FFX_Xbox.tapB()
    
    FFX_Xbox.SkipDialog(0.3)
    while not FFX_memory.battleActive():
        if FFX_memory.cutsceneSkipPossible():
            FFX_Xbox.skipScene()
        elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
    
    aeonSummon(4)

    while FFX_memory.battleActive(): #Arm2
        if FFX_memory.turnReady():
            impulse()
            FFX_Xbox.tapB()
            FFX_Xbox.tapB()
        else:
            FFX_Xbox.tapB()
    
    FFX_Xbox.SkipDialog(0.3)
    while not FFX_memory.battleActive():
        if FFX_memory.cutsceneSkipPossible():
            FFX_Xbox.skipScene()
        elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()

    FFX_Xbox.clickToBattle() #Start of Sin Core
    aeonSummon(4)
    FFX_Screen.awaitTurn()
    if gameVars.nemesis():
        while not FFX_memory.battleComplete():
            if FFX_memory.turnReady():
                attack('none')
    else:
        impulse(targetFarLine=True)
        FFX_Xbox.tapB()
        FFX_Xbox.tapB()
    
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
    
    aeonFirstTurn = True
    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            if FFX_Screen.turnYuna():
                aeonSummon(4)
            elif FFX_Screen.turnAeon():
                if aeonFirstTurn:
                    impulse()
                    aeonFirstTurn = False
                else:
                    attack('none')
            else:
                defend()
        else:
            FFX_Xbox.tapB()

def yojimbo():
    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            if FFX_Screen.turnYuna():
                aeonSummon(4)
            elif FFX_Screen.turnAeon():
                attack('none')
            else:
                defend()
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()

def omnis():
    FFX_Logs.writeLog("Fight start: Seymour Omnis")
    print("Fight start: Seymour Omnis")
    FFX_Xbox.clickToBattle()
    defend() #Yuna defends
    
    while FFX_memory.getEnemyMaxHP()[0] == FFX_memory.getEnemyCurrentHP()[0]:
        if FFX_memory.turnReady():
            if FFX_Screen.turnTidus():
                useSkill(0)
            else:
                defend()
    
    print("Ready for aeon.")
    while not FFX_memory.battleComplete(): #AKA end of battle screen
        if FFX_memory.turnReady():
            print("Character turn: ",FFX_memory.getBattleCharTurn())
            if FFX_Screen.turnYuna():
                aeonSummon(4)
            elif FFX_Screen.turnAeon():
                attack('none')
            elif FFX_Screen.turnTidus():
                attack('none')
            else:
                defend()
        elif FFX_memory.diagSkipPossible():
            print("Skipping dialog maybe?")
            FFX_Xbox.tapB()
    print("Should be done now.")
    FFX_memory.clickToControl()

def BFA_nem():
    FFXC.set_movement(1, 0)
    FFX_memory.waitFrames(30 * 0.4)
    FFXC.set_movement(1, 1)
    FFX_memory.waitFrames(30 * 3)
    FFXC.set_neutral()
    tidusFirstTurn=False
    
    FFX_Logs.writeLog("Fight start: BFA and final boss")
    FFX_Xbox.clickToBattle()
    
    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            if FFX_Screen.turnTidus():
                if tidusFirstTurn:
                    equipInBattle(equipType = 'weap', abilityNum = 0x8019, character = 0)
                    tidusFirstTurn=True
                else:
                    attack('none')
            else:
                defend()
    
    while FFX_memory.getStoryProgress() < 3400: #End of game
        if FFX_memory.battleActive():
            if FFX_memory.turnReady():
                if FFX_Screen.turnTidus():
                    if FFX_memory.getBattleNum() == 401 and FFX_memory.overdriveState2()[0] == 100:
                        tidusOD()
                    else:
                        attack('none')
                elif FFX_Screen.turnYuna():
                    buddySwapWakka()
                elif FFX_Screen.turnAuron():
                    buddySwapLulu()
                else:
                    defend()
        elif FFX_memory.cutsceneSkipPossible():
            FFX_memory.waitFrames(2)
            if FFX_memory.cutsceneSkipPossible():
                FFX_Xbox.skipScene()
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
    
def BFA():
    FFXC.set_movement(1, 0)
    FFX_memory.waitFrames(30 * 0.4)
    FFXC.set_movement(1, 1)
    FFX_memory.waitFrames(30 * 3)
    FFXC.set_neutral()
    
    FFX_Logs.writeLog("Fight start: BFA and final boss")
    FFX_Xbox.clickToBattle()
    buddySwapRikku()
    if FFX_memory.overdriveState()[6] == 100:
        rikkuFullOD('bfa')
    else:
        useSkill(0)

    FFX_Screen.awaitTurn()
    while FFX_memory.mainBattleMenu():
        FFX_Xbox.tapLeft()
    while FFX_memory.battleCursor2() != 1:
        FFX_Xbox.tapDown()
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    tapTargeting()
    buddySwapYuna()
    aeonSummon(4)
    
    #Bahamut finishes the battle.
    while FFX_memory.battleActive():
        FFX_Xbox.tapB()

    #Skip the cutscene
    print("BFA down. Ready for Aeons")
    
    if not gameVars.csr():
        while not FFX_memory.cutsceneSkipPossible():
            FFX_Xbox.tapB()
        FFX_Xbox.skipScene()
    
    while FFX_memory.getStoryProgress() < 3380:
        if FFX_memory.turnReady():
            battleNum = FFX_memory.getBattleNum()
            print("Battle engaged. Battle number: ", battleNum)
            if FFX_Screen.turnYuna():
                if FFX_memory.battleMenuCursor() != 20:
                    while FFX_memory.battleMenuCursor() != 20:
                        if FFX_memory.battleMenuCursor() in [22,1]:
                            FFX_Xbox.tapUp()
                        else:
                            FFX_Xbox.tapDown()
                while FFX_memory.mainBattleMenu():
                    FFX_Xbox.tapB()
                while FFX_memory.otherBattleMenu():
                    FFX_Xbox.tapB()
                print(FFX_memory.getEnemyMaxHP())
                calculateSpareChangeMovement(FFX_memory.getEnemyMaxHP()[0]*10)
                while FFX_memory.spareChangeOpen():
                    FFX_Xbox.tapB()
                while not FFX_memory.mainBattleMenu():
                    FFX_Xbox.tapB()
            else:
                defend()
        elif FFX_memory.battleActive() == False:
            FFX_Xbox.tapB()

def yuYevon():
    print("Ready for Yu Yevon.")
    FFX_Screen.awaitTurn()  # No need for skipping dialog
    print("Awww such a sad final boss!")
    zombieAttack = False
    zaChar = gameVars.zombieWeapon()
    #if zaChar in [0,1,2,6]:
    weapSwap = False
    story = FFX_memory.getStoryProgress()
    while story < 3400:
        if FFX_memory.turnReady():
            print("-----------------------")
            print("-----------------------")
            print("zaChar: ", zaChar)
            print("zombieAttack: ", zombieAttack)
            print("weapSwap: ", weapSwap)
            print("-----------------------")
            print("-----------------------")
            if zaChar == 1 and not zombieAttack: #Yuna logic
                if weapSwap == False and FFX_Screen.turnYuna():
                    equipInBattle(equipType = 'weap', abilityNum = 0x8032, character = 1)
                    weapSwap = True
                elif FFX_Screen.turnYuna():
                    attack('none')
                    zombieAttack = True
                elif weapSwap == True and zombieAttack == False and FFX_Screen.turnTidus():
                    FFX_Xbox.weapSwap(0)
                else:
                    defend()
            elif zaChar == 0 and not zombieAttack: #Tidus logic:
                if FFX_Screen.turnYuna():
                    defend()
                elif FFX_Screen.turnTidus() and not weapSwap:
                    equipInBattle(equipType = 'weap', abilityNum = 0x8032, character = 0)
                    weapSwap = True
                elif FFX_Screen.turnTidus():
                    attack('none')
                    zombieAttack = True
                else:
                    defend()
            elif zaChar == 2 and not zombieAttack: #Auron logic:
                if FFX_Screen.turnYuna():
                    buddySwapAuron()
                elif FFX_Screen.turnAuron() and not weapSwap:
                    equipInBattle(equipType = 'weap', abilityNum = 0x8032, character = 2)
                    weapSwap = True
                elif FFX_Screen.turnAuron():
                    attack('none')
                    zombieAttack = True
                else:
                    defend()
            elif zaChar == 6 and not zombieAttack: #Rikku logic:
                if FFX_Screen.turnYuna() and not weapSwap:
                    #Piggy back off the weapSwap function
                    defend()
                    weapSwap = True
                elif FFX_Screen.turnYuna():
                    FFX_Xbox.weapSwap(0)
                elif FFX_Screen.turnTidus():
                    tidusHaste('r', character=6)
                elif FFX_Screen.turnRikku():
                    attack('none')
                    zombieAttack = True
                else:
                    defend()
            elif zombieAttack: #Throw P.down to end game
                while FFX_memory.battleMenuCursor() != 1:
                    FFX_Xbox.tapDown()
                while FFX_memory.mainBattleMenu():
                    FFX_Xbox.tapB()
                itemPos = FFX_memory.getThrowItemsSlot(6)
                _navigate_to_position(itemPos)
                while FFX_memory.otherBattleMenu():
                    FFX_Xbox.tapB()
                while FFX_memory.battleTargetId() < 20:
                    FFX_Xbox.tapUp()
                tapTargeting()
                print("Phoenix Down on Yu Yevon. Good game.")
            elif FFX_Screen.turnTidus() and zaChar == 255:
                #Tidus to use Zombie Strike ability
                useSkill(0)
                zombieAttack = True
            elif zaChar == 255 and not FFX_Screen.turnTidus():
                #Non-Tidus char to defend so Tidus can use Zombie Strike ability
                defend()
            else:
                if FFX_memory.getBattleCharTurn() == zaChar:
                    attack('none')
                    zombieAttack = True
                elif FFX_memory.getBattleCharSlot(zaChar) >= 3:
                    buddySwap_char(zaChar)
                elif FFX_Screen.turnTidus():
                    tidusHaste('l', character = zaChar)
                else:
                    defend()
        elif FFX_memory.battleActive() == False:
            FFX_Xbox.tapB()
        story = FFX_memory.getStoryProgress()
    

def checkPetrify():
    for iterVar in range(7):
        if FFX_memory.petrifiedstate(iterVar):
            return True
    return False
    
def checkPetrifyTidus():
    return FFX_memory.petrifiedstate(0)

def rikkuODItems(slot):
    _navigate_to_position(slot, battleCursor=FFX_memory.RikkuODCursor1)

def rikkuFullOD(battle):
    #First, determine which items we are using
    if battle == 'tutorial':
        item1 = FFX_memory.getItemSlot(73)
        print("Ability sphere in slot: ", item1)
        item2 = item1
    elif battle == 'Evrae':
        item1 = FFX_memory.getItemSlot(94)
        print("Luck sphere in slot: ", item1)
        item2 = FFX_memory.getItemSlot(100)
        print("Map in slot: ", item2)
    elif battle == 'Flux':
        item1 = FFX_memory.getItemSlot(35)
        print("Grenade in slot: ", item1)
        item2 = FFX_memory.getItemSlot(85)
        print("HP Sphere in slot: ", item2)
    elif battle == 'trio':
        item1 = 108
        item2 = 108
        print("Wings are in slot: ", item1)
    elif battle == 'crawler':
        item1 = FFX_memory.getItemSlot(30)
        print("Lightning Marble in slot: ", item1)
        item2 = FFX_memory.getItemSlot(85)
        print("Mdef Sphere in slot: ", item2)
    elif battle == 'spherimorph1':
        item1 = FFX_memory.getItemSlot(24)
        print("Arctic Wind in slot: ", item1)
        item2 = FFX_memory.getItemSlot(90)
        print("Mag Def Sphere in slot: ", item2)
    elif battle == 'spherimorph2':
        item1 = FFX_memory.getItemSlot(32)
        print("Fish Scale in slot: ", item1)
        item2 = FFX_memory.getItemSlot(90)
        print("Mag Sphere in slot: ", item2)
    elif battle == 'spherimorph3':
        item1 = FFX_memory.getItemSlot(30)
        print("Lightning Marble in slot: ", item1)
        item2 = FFX_memory.getItemSlot(90)
        print("Mag Sphere in slot: ", item2)
    elif battle == 'spherimorph4':
        item1 = FFX_memory.getItemSlot(27)
        print("Bomb Core in slot: ", item1)
        item2 = FFX_memory.getItemSlot(90)
        print("Mag Sphere in slot: ", item2)
    elif battle == 'bfa':
        item1 = FFX_memory.getItemSlot(35)
        print("Grenade in slot: ", item1)
        item2 = FFX_memory.getItemSlot(85)
        print("HP Sphere in slot: ", item2)
    elif battle == 'shinryu':
        item1 = FFX_memory.getItemSlot(109)
        print("Gambler's Spirit in slot: ", item1)
        item2 = FFX_memory.getItemSlot(58)
        print("Star Curtain in slot: ", item2)

    if item1 > item2:
        item3 = item1
        item1 = item2
        item2 = item3
    
    #Now to enter commands
    
    while not FFX_memory.otherBattleMenu():
        FFX_Xbox.tapLeft()
        
    while not FFX_memory.interiorBattleMenu():
        FFX_Xbox.tapB()
    rikkuODItems(item1)
    while not FFX_memory.rikkuOverdriveItemSelectedNumber():
        FFX_Xbox.tapB()
    rikkuODItems(item2)
    while FFX_memory.interiorBattleMenu():
        FFX_Xbox.tapB()
    tapTargeting()

def equipInBattle(equipType = 'weap', abilityNum = 0, character = 0, special = 'none'):
    equipType = equipType.lower()
    while FFX_memory.mainBattleMenu():
        FFX_Xbox.tapRight()
    if equipType == 'weap':
        equipHandles = FFX_memory.weaponArrayCharacter(character)
    else:
        while FFX_memory.battleCursor2() != 1:
            FFX_Xbox.tapDown()
        equipHandles = FFX_memory.armorArrayCharacter(character)
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    
    print("@@@@@")
    print("Character ", character)
    print("Equipment type: ", equipType)
    print("Number of items: ", len(equipHandles))
    print("Special: ", special)
    print("@@@@@")
    equipNum = 255
    i = 0
    while len(equipHandles) > 0:
        currentHandle = equipHandles.pop(0)
        print(currentHandle.abilities())
        if special == 'baroque':
            if currentHandle.abilities() == [0x8063,255,255,255]:
                equipNum = i
        elif special == 'brotherhood':
            if currentHandle.abilities() == [32867,32868,32810,32768]:
                equipNum = i
        elif abilityNum == 0:
            print("Equipping just the first available equipment.")
            equipNum = 0
        elif currentHandle.hasAbility(abilityNum): #First Strike for example
            equipNum = i
        i += 1
    while FFX_memory.battleCursor3() != equipNum:
        print("'''Battle cursor 3: ", FFX_memory.battleCursor3())
        print("'''equipNum: ", equipNum)
        if FFX_memory.battleCursor3() < equipNum:
            FFX_Xbox.tapDown()
        else:
            FFX_Xbox.tapUp()
    while FFX_memory.interiorBattleMenu():
        FFX_Xbox.tapB()
    
    print("Desired equipment is in slot ", equipNum)

def checkCharacterOk(charNum):
    return not any(func(charNum) for func in [FFX_memory.petrifiedstate, FFX_memory.confusedState, FFX_memory.deadstate, FFX_memory.berserkstate])
    
def checkTidusOk():
    return checkCharacterOk(0)
    
def checkRikkuOk():
    return checkCharacterOk(6)
    
def get_digit(number, n):
    return number // 10**n % 10
    
def calculateSpareChangeMovement(gilAmount):
    if gilAmount > FFX_memory.getGilvalue():
        gilAmount = FFX_memory.getGilvalue()
    gilAmount = min(gilAmount, 100000)
    position = {}
    gilCopy = gilAmount
    for index in range(0, 7):
        amount = get_digit(gilAmount, index)
        if amount > 5:
            gilAmount += 10**(index+1)
        position[index] = amount
    print(position)
    for cur in range(6, -1, -1):
        if not position[cur]: continue
        while FFX_memory.spareChangeCursor() != cur:
            FFX_memory.sideToSideDirection(FFX_memory.spareChangeCursor(), cur, 6)
        target = position[cur]
        while get_digit(FFX_memory.spareChangeAmount(), cur) != target:
            if target > 5:
                FFX_Xbox.tapDown()
            else:
                FFX_Xbox.tapUp()
        if FFX_memory.spareChangeAmount() == gilCopy:
            return
    return

def chargeRikkuOD():
    if FFX_memory.getOverdriveBattle(6) != 100 and FFX_memory.getBattleNum() in [360, 361, 378, 384]:
        if checkPetrifyTidus() or not checkRikkuOk():
            print("Tidus or Rikku incapacitated, fleeing")
            fleeAll()
        else:
            while not FFX_memory.battleComplete():
                if FFX_memory.turnReady():
                    turnchar = FFX_memory.getBattleCharTurn()
                    if turnchar == 6:
                        attack('none')
                    elif FFX_memory.getOverdriveBattle(6) == 100:
                        fleeAll()
                    else:
                        escapeOne()
            FFX_memory.clickToControl3()
            if FFX_memory.overdriveState()[6] == 100:
                FFX_memory.fullPartyFormat('kimahri')
            else:
                healUp()
    else:   
        fleeAll()            

def farmDome():
    if FFX_memory.getBattleNum() in [361, 364, 366]:
        if FFX_memory.battleType() == 2:
            fleeAll()
        elif FFX_memory.getBattleNum() == 361: # Defender Z
            while not FFX_memory.battleComplete():
                if FFX_Screen.turnYuna():
                    aeonSummon(4)
                elif FFX_Screen.turnAeon():
                    attack('none')
                else:
                    defend()
            gameVars.addYTKFarm()
            gameVars.addYTKFarm()
        elif FFX_memory.getBattleNum() in [364, 365, 366]: # YAT-97	YKT-11	YAT-97
            while not FFX_memory.battleComplete():
                if 0 in FFX_memory.getEnemyCurrentHP() or not checkTidusOk() or not checkYunaOk():
                    fleeAll()
                elif FFX_Screen.turnYuna():
                    attack('left' if FFX_memory.getBattleNum() == 366 else 'none')
                elif FFX_Screen.turnTidus():
                    attack('left' if FFX_memory.getBattleNum() == 366 else 'none')
                else:
                    defend()
            gameVars.addYTKFarm()
        FFX_memory.clickToControl3()
        if gameVars.completedYTKFarm():
            gameVars.fluxOverkillSuccess()
            if FFX_memory.overdriveState()[6] != 100:
                FFX_memory.fullPartyFormat('rikku')
            else: 
                FFX_memory.fullPartyFormat('kimahri')
        else:
            healUp()
    else:
        fleeAll()

def faintCheckWithEscapes():
    for x in range(3):
        if FFX_memory.deadstate(FFX_memory.getBattleFormation()[x]):
            return True
    return False

def checkGems():
    gemSlot = FFX_memory.getItemSlot(34)
    if gemSlot < 200:
        gems = FFX_memory.getItemCountSlot(gemSlot)
    else:
        gems = 0
    
    gemSlot = FFX_memory.getItemSlot(28)
    if gemSlot < 200:
        gems += FFX_memory.getItemCountSlot(gemSlot)
    print("Total gems: ", gems)
    return gems

def calmLandsManip():
    print("++Battle number: ", FFX_memory.getBattleNum())
    rng10nextChanceLow = FFX_memory.nextChanceRNG10(12)
    lowArray = [273,275,276,281,283,284]
    rng10nextChanceMid = FFX_memory.nextChanceRNG10(60)
    midArray = [277,279,285,287,289,290]
    rng10nextChanceHigh = FFX_memory.nextChanceRNG10(128)
    highArray = [278,286,288]
    
    if checkGems() < 2:
        print("++Calm Lands battle, looking for gems.")
        calmLandsGems()
    #elif FFX_memory.nextChanceRNG13() == 1 and FFX_memory.nextChanceRNG12() == 1:
    #    if FFX_memory.nextChanceRNG10() != 3:
    #        advanceRNG10(FFX_memory.nextChanceRNG10Calm2())
    #    else:
    #        fleeAll()
    elif FFX_memory.nextChanceRNG12() != 0:
        print("Not ready for NE armor drop. Apply logic to try to drop something else.")
        #NE armor too far ahead. Need to drop armors.
        if rng10nextChanceLow == 0 and FFX_memory.getBattleNum() in lowArray:
            advanceRNG12()
        elif rng10nextChanceMid == 0 and FFX_memory.getBattleNum() in midArray:
            advanceRNG12()
        elif rng10nextChanceHigh == 0 and FFX_memory.getBattleNum() in highArray:
            advanceRNG12()
        else: #Cycle mid chance as needed.
            print("Can't drop off of this battle.")
            advanceRNG10(rng10nextChanceMid)
    else:
        setupNext = FFX_memory.nextChanceRNG10Calm()
        if FFX_memory.getCoords()[0] > 1000:
            print("--Near Gagazet, just get off RNG10 equipment drop.")
            if FFX_memory.nextChanceRNG10() == 0:
                advanceRNG10(FFX_memory.nextChanceRNG10())
                #Don't want to have Defender X drop an item
        elif setupNext!= 0:
            if setupNext < 25:
                print("++Still a ways. Try to set up for Defender X plus Wraith.")
                advanceRNG10(setupNext)
                #Try for perfect setup if it's not too far off.
            elif FFX_memory.nextChanceRNG10() == 0:
                print("++No perfect chance coming up. Going for regular chance.")
                advanceRNG10(FFX_memory.nextChanceRNG10())
            else:
                print("--Next perfect value is too far away. Moving on.")
                fleeAll()
        else:
            print("--Perfectly set up and good to go.")
            fleeAll()
            #FFX_memory.setEncounterRate(0) #Testing only
    FFX_memory.clickToControl3()
    FFX_memory.fullPartyFormat('yuna',fullMenuClose=False)
    healUp(fullMenuClose=True)
    FFX_memory.printManipInfo()

def advanceRNG10Ghost(numAdvances:int):
    silenceGrenade = False
    hasteRikku = False
    hasteSelf = False
    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            if numAdvances >= 1:
                if FFX_Screen.faintCheck():
                    revive()
                elif FFX_Screen.turnRikku():
                    if not silenceGrenade:
                        useItem()
                        silenceGrenade = True
                    else:
                        Steal()
                        numAdvances -= 1
                elif FFX_Screen.turnKimahri():
                    Steal()
                    numAdvances -= 1
                elif not 6 in FFX_memory.getActiveBattleFormation():
                    buddySwapRikku()
                elif not 3 in FFX_memory.getActiveBattleFormation():
                    buddySwapKimahri()
                elif FFX_Screen.turnTidus():
                    if not hasteRikku:
                        tidusHaste(direction='l', character=6)
                        hasteRikku = True
                    elif FFX_memory.getEnemyCurrentHP()[0] > 5000:
                        attack('none')
                    elif not hasteSelf:
                        tidusHaste(direction='l', character=0)
                        hasteSelf = True
                    else:
                        defend()
                elif not 0 in FFX_memory.getActiveBattleFormation():
                    buddySwapTidus()
                else:
                    defend()
            else:
                if FFX_Screen.turnTidus():
                    attack('none')
                elif FFX_Screen.faintCheck():
                    revive()
                elif FFX_Screen.turnYuna() and FFX_memory.getEnemyCurrentHP()[0] > 5000:
                    attack('none')
                elif not 1 in FFX_memory.getActiveBattleFormation():
                    buddySwapYuna()
                else:
                    defend()

def advanceRNG10(numAdvances:int):
    advanceComplete = False
    print("#################")
    print("###RNG10 logic###")
    print("##    ", numAdvances, "      ##")
    print("#################")
    while FFX_memory.battleActive():
        if FFX_memory.battleType() == 2:
            fleeAll()
        elif FFX_memory.getBattleNum() == 321:
            print("Aw hell naw, we want nothing to do with this guy! (evil jar guy)")
            fleeAll()
        elif FFX_memory.getBattleNum() == 319:
            advanceRNG10Ghost(numAdvances)
        elif numAdvances in [1,2] and FFX_memory.getNextTurn() < 20 and FFX_memory.getBattleNum() != 287:
            if FFX_memory.turnReady():
                if not advanceComplete:
                    if FFX_Screen.turnRikku() or FFX_Screen.turnKimahri():
                        if FFX_memory.getBattleNum() == 313:
                            _steal('down')
                        elif FFX_memory.getBattleNum() == 314:
                            _steal('right')
                        else:
                            _steal()
                        advanceComplete = True
                    elif FFX_memory.getBattleCharSlot(6) >= 3:
                        buddySwapRikku()
                    elif FFX_memory.getBattleCharSlot(3) >= 3:
                        buddySwapKimahri()
                    else:
                        defend()
                else:
                    fleeAll()
        elif numAdvances >= 3:
            if FFX_memory.turnReady():
                if FFX_Screen.faintCheck() >= 1:
                    fleeAll()
                elif FFX_Screen.turnRikku():
                    #Most convenient since overdrive is needed for Flux.
                    defend()
                elif FFX_Screen.turnTidus():
                    buddySwapRikku()
                else:
                    defend()
        else: #any other scenarios, ready to advance.
            fleeAll()
    FFX_memory.clickToControl()
    healUp(3)

def advanceRNG12():
    attackCount = False
    if FFX_memory.battleActive():
        aeonTurn = False
        while FFX_memory.battleActive():
            if FFX_memory.turnReady():
                advances = FFX_memory.nextChanceRNG12()
                if FFX_Screen.turnYuna():
                    if aeonTurn:
                        fleeAll()
                    else:
                        aeonSummon(4)
                elif FFX_Screen.turnAeon():
                    if advances == 0:
                        print("GTFO this battle.")
                        aeonDismiss()
                    elif advances >= 2:
                        impulse()
                    elif advances == 1 and not attackCount:
                        impulse()
                        #attackCount = True
                        #attack('none')
                    else:
                        impulse()
                        #aeonDismiss()
                    aeonTurn = True
                else:
                    if aeonTurn:
                        fleeAll()
                    elif FFX_memory.getBattleCharSlot(1) >= 3:
                        buddySwapYuna()
                    else:
                        defend()
        FFX_memory.clickToControl3()
        #FFX_memory.fullPartyFormat('rikku')
    if FFX_memory.getMap() == 223:
        healUp(3)

def ghostKill():
    silenceSlot = FFX_memory.getUseItemsSlot(39)
    itemThrown = False
    print("++Silence slot: ", silenceSlot)
    while FFX_memory.battleActive():
        if silenceSlot < 200:
            #Try to get NEA on Tidus
            if FFX_memory.turnReady():
                if FFX_Screen.turnTidus():
                    if not itemThrown:
                        buddySwapRikku()
                        FFX_Screen.awaitTurn()
                        useItem(silenceSlot)
                        itemThrown = True
                    else:
                        attack('none')
                elif FFX_Screen.turnRikku():
                    buddySwapTidus()
                    FFX_Screen.awaitTurn()
                    tidusHaste('none')
                elif FFX_Screen.turnKimahri():
                    buddySwapYuna()
                elif FFX_Screen.turnYuna():
                    if FFX_memory.getEnemyCurrentHP()[0] > 3000:
                        attack('none')
                    else:
                        defend()
                else:
                    defend()
        else:
            if FFX_memory.turnReady():
                if FFX_memory.getBattleNum() in [319,323]:
                    if FFX_Screen.turnYuna():
                        aeonSummon(4)
                    elif FFX_Screen.turnAeon():
                        attack('none')
                    elif FFX_memory.getBattleCharSlot(1) >= 3:
                        buddySwapYuna()
                    else:
                        defend()
                else:
                    fleeAll()
    FFX_memory.clickToControl3()
    healUp(3)