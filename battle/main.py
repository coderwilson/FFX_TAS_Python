import xbox
import screen
import logs
import memory.main
from memory.main import s32
import vars
import rngTrack
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def tapTargeting():
    print("In Tap Targeting", not memory.main.mainBattleMenu(),
          memory.main.battleActive())
    while (not memory.main.mainBattleMenu()) and memory.main.battleActive():
        xbox.tapB()
    print("Done", not memory.main.mainBattleMenu(), memory.main.battleActive())


def valeforOD(sinFin=0, version=0):
    memory.main.waitFrames(6)
    while memory.main.mainBattleMenu():
        xbox.tapLeft()
    print("Overdrive:", version)
    if version == 1:
        while memory.main.battleCursor2() != 1:
            xbox.tapDown()
    while memory.main.otherBattleMenu():
        xbox.tapB()  # Energy Blast
    if sinFin == 1:
        xbox.tapDown()
        xbox.tapLeft()
    tapTargeting()


def defend():
    print("Defending")
    for _ in range(5):
        xbox.tapY()


def tidusFlee():
    if memory.main.battleActive():
        print("Tidus Flee (or similar command pattern)")
        while memory.main.battleMenuCursor() != 20:
            if memory.main.battleMenuCursor() == 255:
                xbox.tapUp()
            elif memory.main.battleMenuCursor() == 1:
                xbox.tapUp()
            elif memory.main.battleMenuCursor() > 20:
                xbox.tapUp()
            else:
                xbox.tapDown()
            if memory.main.otherBattleMenu():
                xbox.tapA()
        print("Out")
        while not memory.main.otherBattleMenu():
            xbox.tapB()
        _navigate_to_position(0)
        while memory.main.otherBattleMenu():
            xbox.tapB()
        tapTargeting()


def yunaCureOmnis():
    while memory.main.battleMenuCursor() != 22:
        if not screen.turnYuna():
            print("Attempting Cure, but it's not Yunas turn")
            return
        if memory.main.battleMenuCursor() == 1:
            xbox.tapUp()
        else:
            xbox.tapDown()
    while not memory.main.otherBattleMenu():
        xbox.tapB()
    _navigate_to_position(0)
    while memory.main.otherBattleMenu():
        xbox.tapB()
    while memory.main.battleTargetId() <= 20:
        if memory.main.battleTargetId() < 20:
            xbox.tapDown()
        elif memory.main.battleTargetId() == 20:
            xbox.tapLeft()
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()


def tidusHaste(direction, character=255):
    direction = direction.lower()
    while memory.main.battleMenuCursor() != 22:
        if not screen.turnTidus():
            print("Attempting Haste, but it's not Tidus' turn")
            xbox.tapUp()
            xbox.tapUp()
            return
        if memory.main.battleMenuCursor() == 1:
            xbox.tapUp()
        else:
            xbox.tapDown()
    while not memory.main.otherBattleMenu():
        xbox.tapB()
    _navigate_to_position(0)
    while memory.main.otherBattleMenu():
        xbox.tapB()
    if character != 255:
        direction = 'l'
        if character < 20:
            while character != memory.main.battleTargetId():
                if direction == 'l':
                    xbox.tapLeft()
                    if memory.main.battleTargetId() >= 20:
                        xbox.tapRight()
                        direction = 'd'
                else:
                    xbox.tapDown()
                    if memory.main.battleTargetId() >= 20:
                        xbox.tapUp()
                        direction = 'l'
        else:
            while character != memory.main.battleTargetId():
                if direction == 'l':
                    xbox.tapLeft()
                    if memory.main.battleTargetId() < 20:
                        xbox.tapRight()
                        direction = 'd'
                else:
                    xbox.tapDown()
                    if memory.main.battleTargetId() < 20:
                        xbox.tapUp()
                        direction = 'l'
    elif direction == 'left':
        xbox.tapLeft()
    elif direction == 'right':
        xbox.tapRight()
    elif direction == 'up':
        xbox.tapUp()
    elif direction == 'down':
        xbox.tapDown()
    tapTargeting()


def lateHaste(direction):
    tidusHaste(direction)


def useSkill(position: int = 0, target: int = 20):
    print("Using skill in position:", position)
    while memory.main.battleMenuCursor() != 19:
        print(memory.main.battleMenuCursor())
        if memory.main.battleMenuCursor() == 255:
            pass
        elif memory.main.battleMenuCursor() == 1:
            xbox.tapUp()
        elif memory.main.battleMenuCursor() > 19:
            xbox.tapUp()
        else:
            xbox.tapDown()
    while not memory.main.otherBattleMenu():
        xbox.tapB()
    _navigate_to_position(position)
    while memory.main.otherBattleMenu():
        xbox.tapB()
    if target != 20:
        direction = 'l'
        while memory.main.battleTargetId() != target:
            if direction == 'l':
                xbox.tapLeft()
                if memory.main.battleTargetId() < 20:
                    xbox.tapRight()
                    direction = 'd'
            else:
                xbox.tapDown()
                if memory.main.battleTargetId() < 20:
                    xbox.tapUp()
                    direction = 'l'
    tapTargeting()


def useSpecial(position, target: int = 20, direction: int = 'u'):
    print("Using skill in position:", position)
    while memory.main.battleMenuCursor() != 20:
        print(memory.main.battleMenuCursor())
        if memory.main.battleMenuCursor() == 255:
            pass
        elif memory.main.battleMenuCursor() == 1:
            xbox.tapUp()
        elif memory.main.battleMenuCursor() > 20:
            xbox.tapUp()
        else:
            xbox.tapDown()
    while not memory.main.otherBattleMenu():
        xbox.tapB()
    _navigate_to_position(position)
    while memory.main.otherBattleMenu():
        xbox.tapB()

    if memory.main.battleTargetId() != target:
        while memory.main.battleTargetId() != target:
            if direction == 'r':
                xbox.tapRight()
                if memory.main.battleTargetId() < 20:
                    xbox.tapLeft()
                    direction = 'u'
            else:
                xbox.tapUp()
                if memory.main.battleTargetId() < 20:
                    xbox.tapDown()
                    direction = 'r'
    tapTargeting()


def auronOD(style="dragon fang"):
    while not memory.main.otherBattleMenu():
        xbox.tapLeft()
    while not memory.main.interiorBattleMenu():
        xbox.tapB()
    print("Style:", style)
    # Doing the actual overdrive
    if style == "dragon fang":
        _navigate_to_position(0, battleCursor=memory.main.battleCursor3)
        while not memory.main.auronOverdriveActive():
            xbox.tapB()
        print("Starting")
        for i in range(2):  # Do it twice in case there's a miss on the first one.
            FFXC.set_value('Dpad', 2)  # down
            memory.main.waitFrames(1)
            FFXC.set_value('Dpad', 0)
            FFXC.set_value('Dpad', 4)  # left
            memory.main.waitFrames(1)
            FFXC.set_value('Dpad', 0)
            FFXC.set_value('Dpad', 1)  # up
            memory.main.waitFrames(1)
            FFXC.set_value('Dpad', 0)
            FFXC.set_value('Dpad', 8)  # right
            memory.main.waitFrames(1)
            FFXC.set_value('Dpad', 0)
            FFXC.set_value('BtnShoulderL', 1)
            memory.main.waitFrames(1)
            FFXC.set_value('BtnShoulderL', 0)
            FFXC.set_value('BtnShoulderR', 1)
            memory.main.waitFrames(1)
            FFXC.set_value('BtnShoulderR', 0)
            FFXC.set_value('BtnA', 1)
            memory.main.waitFrames(1)
            FFXC.set_value('BtnA', 0)
            FFXC.set_value('BtnB', 1)
            memory.main.waitFrames(1)
            FFXC.set_value('BtnB', 0)
    elif style == "shooting star":
        _navigate_to_position(1, battleCursor=memory.main.battleCursor3)
        while not memory.main.auronOverdriveActive():
            xbox.tapB()
        for i in range(2):  # Do it twice in case there's a miss on the first one.
            FFXC.set_value('BtnY', 1)
            memory.main.waitFrames(1)
            FFXC.set_value('BtnY', 0)
            FFXC.set_value('BtnA', 1)
            memory.main.waitFrames(1)
            FFXC.set_value('BtnA', 0)
            FFXC.set_value('BtnX', 1)
            memory.main.waitFrames(1)
            FFXC.set_value('BtnX', 0)
            FFXC.set_value('BtnB', 1)
            memory.main.waitFrames(1)
            FFXC.set_value('BtnB', 0)
            FFXC.set_value('Dpad', 4)  # left
            memory.main.waitFrames(1)
            FFXC.set_value('Dpad', 0)
            FFXC.set_value('Dpad', 8)  # right
            memory.main.waitFrames(1)
            FFXC.set_value('Dpad', 0)
            FFXC.set_value('BtnB', 1)
            memory.main.waitFrames(1)
            FFXC.set_value('BtnB', 0)


def tidusOD(direction=None, version: int = 0, character=99):
    print("Tidus overdrive activating")
    while not memory.main.otherBattleMenu():
        xbox.tapLeft()
    while not memory.main.interiorBattleMenu():
        xbox.tapB()
    if version == 1:
        memory.main.waitFrames(6)
        xbox.menuRight()
    while memory.main.interiorBattleMenu():
        xbox.tapB()
    if character != 99 and memory.main.getEnemyCurrentHP()[character - 20] != 0:
        while character != memory.main.battleTargetId() and memory.main.getEnemyCurrentHP()[character - 20] != 0:
            xbox.tapLeft()
    elif direction:
        if direction == 'left':
            xbox.tapLeft()

    while not memory.main.overdriveMenuActive():
        xbox.tapB()
    memory.main.waitFrames(12)
    print("Hit Overdrive")
    xbox.tapB()  # First try pog
    memory.main.waitFrames(8)
    xbox.tapB()  # Extra attempt in case of miss
    memory.main.waitFrames(9)
    xbox.tapB()  # Extra attempt in case of miss
    memory.main.waitFrames(10)
    xbox.tapB()  # Extra attempt in case of miss
    memory.main.waitFrames(11)
    xbox.tapB()  # Extra attempt in case of miss
    memory.main.waitFrames(12)
    xbox.tapB()  # Extra attempt in case of miss


def tidusODSeymour():
    print("Tidus overdrive activating")
    screen.awaitTurn()
    tidusOD('left')


def yunaOD(aeonNum: int = 5):
    print("Awaiting Yunas turn")
    while not screen.turnYuna():
        if memory.main.turnReady():
            defend()
    while not memory.main.otherBattleMenu():
        xbox.tapLeft()
    while not memory.main.interiorBattleMenu():
        xbox.tapB()
    while not memory.main.battleCursor3() == aeonNum:
        if aeonNum > memory.main.battleCursor3():
            xbox.tapDown()
        else:
            xbox.tapUp()
        memory.main.waitFrames(2)
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()


def yojimboOD(gilValue: int = 263000):
    print("Yojimbo overdrive")
    screen.awaitTurn()
    if not screen.turnAeon():
        return
    while memory.main.battleMenuCursor() != 35:
        xbox.tapUp()
    memory.main.waitFrames(6)
    xbox.menuB()
    print("Selecting amount")
    memory.main.waitFrames(15)
    xbox.tapLeft()
    xbox.tapLeft()
    xbox.tapLeft()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapLeft()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapLeft()
    xbox.tapUp()
    xbox.tapUp()
    print("Amount selected")
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()
    return


def remedy(character: int, direction: str):
    print("Remedy")
    if memory.main.getThrowItemsSlot(15) < 250:
        itemnum = 15
    else:
        itemnum = -1
    if itemnum > 0:
        _useHealingItem(character, direction, itemnum)
        return 1
    else:
        print("No restorative items available")
        return 0


def revive(itemNum=6, reportForRNG=False):
    print("Using Phoenix Down")
    if reportForRNG:
        logs.writeRNGTrack("Reviving character")
        logs.writeRNGTrack("Battle: " + str(memory.main.getEncounterID()))
        logs.writeRNGTrack(
            "Story flag: " + str(memory.main.getStoryProgress()))
    if memory.main.getThrowItemsSlot(itemNum) > 250:
        attack('none')
        return
    while not memory.main.mainBattleMenu():
        pass
    while memory.main.battleMenuCursor() != 1:
        xbox.tapDown()
    while memory.main.mainBattleMenu():
        xbox.tapB()
    itemPos = memory.main.getThrowItemsSlot(itemNum)
    _navigate_to_position(itemPos)
    while memory.main.otherBattleMenu():
        xbox.tapB()
    tapTargeting()


def reviveTarget(itemNum=6, target=0):
    direction = 'l'
    print("Using Phoenix Down")
    if memory.main.getThrowItemsSlot(itemNum) > 250:
        fleeAll()
        return
    while not memory.main.mainBattleMenu():
        pass
    while memory.main.battleMenuCursor() != 1:
        xbox.tapDown()
    while memory.main.mainBattleMenu():
        xbox.tapB()
    itemPos = memory.main.getThrowItemsSlot(itemNum)
    _navigate_to_position(itemPos)
    while memory.main.otherBattleMenu():
        xbox.tapB()

    # Select target - default to Tidus
    if memory.main.battleTargetId() != 0:
        while memory.main.battleTargetId() != 0:
            if direction == 'l':
                xbox.tapLeft()
                if memory.main.battleTargetId() >= 20:
                    xbox.tapRight()
                    direction = 'u'
            else:
                xbox.tapUp()
                if memory.main.battleTargetId() >= 20:
                    xbox.tapDown()
                    direction = 'l'
    tapTargeting()


def reviveAll():
    revive(itemNum=7)


def Ammes():
    BattleComplete = 0
    countAttacks = 0
    tidusODflag = False

    while BattleComplete != 1:
        if memory.main.turnReady():
            if not tidusODflag and screen.turnTidus() and memory.main.getOverdriveBattle(0) == 100:
                tidusOD()
                tidusODflag = True
            else:
                print("Attacking Sinspawn Ammes")
                attack('none')
                countAttacks += 1
        if memory.main.userControl():
            BattleComplete = 1
            print("Ammes battle complete")


def Tanker():
    print("Fight start: Tanker")
    countAttacks = 0
    tidusCount = 0
    auronCount = 0
    xbox.clickToBattle()

    while not memory.main.battleComplete():
        if memory.main.turnReady():
            if screen.turnTidus():
                tidusCount += 1
                if tidusCount < 4:
                    xbox.weapSwap(0)
                else:
                    attack('none')
                    countAttacks += 1
            elif screen.turnAuron():
                auronCount += 1
                if auronCount < 2:
                    attackSelfTanker()
                else:
                    attack('none')
                    countAttacks += 1
        elif memory.main.diagSkipPossible():
            xbox.tapB()


def Klikk():
    print("Fight start: Klikk")
    klikkAttacks = 0
    klikkRevives = 0
    stealCount = 0
    while not memory.main.battleComplete(): #AKA end of battle screen
        if memory.main.turnReady():
            BattleHP = memory.main.getBattleHP()
            if BattleHP[0] == 0:
                revive()
                klikkRevives += 1
            elif screen.turnTidus():
                if BattleHP[0] == 0 and memory.main.getEnemyCurrentHP()[0] > 125:
                    usePotionCharacter(0, 'l')
                else:
                    attack('none')
                klikkAttacks += 1
            elif screen.turnRikku():
                grenadeCount = memory.main.getItemCountSlot(
                    memory.main.getItemSlot(35))
                if BattleHP[0] < 120 and not (memory.main.getNextTurn() == 0 and memory.main.getEnemyCurrentHP()[0] <= 181) \
                        and not memory.main.rngSeed() == 160:
                    usePotionCharacter(0, 'l')
                    klikkRevives += 1
                elif memory.main.getEnemyCurrentHP()[0] < 58:
                    attack('none')
                    klikkAttacks += 1
                elif grenadeCount < 6 and memory.main.nextSteal(stealCount=stealCount):
                    print("Attempting to steal from Klikk")
                    Steal()
                    stealCount += 1
                else:
                    attack('none')
                    klikkAttacks += 1
        else:
            if memory.main.diagSkipPossible():
                xbox.tapB()
    print("Klikk fight complete")
    print(memory.main.getMap())
    while not (memory.main.getMap() == 71 and memory.main.userControl() and memory.main.getCoords()[1] < 15):
        #print(memory.main.getMap())
        if gameVars.csr():
            FFXC.set_value("BtnB", 1)
        else:
            xbox.tapB()  # Maybe not skippable dialog, but whatever.
    FFXC.set_neutral()
    memory.main.waitFrames(1)

def getAdvances(tros=True, report=False):
    import rngTrack
    tStrikeResults, yellows = rngTrack.tStrikeTracking(
        tros=tros, report=report)
    if tStrikeResults[0] >= 1 and not yellows[0]:
        advances = 0
    elif tStrikeResults[1] >= 1 and not yellows[1]:
        advances = 1
    elif tStrikeResults[2] >= 1 and not yellows[2]:
        advances = 2
    elif tStrikeResults[1] > tStrikeResults[0]:
        advances = 1
    elif tStrikeResults[2] > tStrikeResults[1]:
        advances = 2
    else:
        advances = 0
    gameVars.setYellows(yellows[advances])
    print("#############################################")
    print("### Advances updated:", tStrikeResults,
          "|", yellows, "|", advances, "###")
    print("#############################################")
    return advances


def Tros():
    FFXC = xbox.controllerHandle()
    logs.openRNGTrack()
    print("Fight start: Tros")
    FFXC.set_neutral()
    battleClock = 0
    Attacks = 0
    Revives = 0
    Grenades = 0
    Steals = 0
    advances = 0
    while not memory.main.turnReady():
        pass

    while memory.main.battleActive():  # AKA end of battle screen
        if memory.main.diagSkipPossible():
            xbox.tapB()
        elif memory.main.turnReady():
            battleClock += 1
            print("Battle clock:", battleClock)
            trosPos = 2
            print("Determining Tros position")
            while trosPos == 2 and not memory.main.battleComplete():
                # Two for "not yet determined". Maybe can be HP-based instead?
                camera = memory.main.getCamera()
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

            # Assuming battle is not complete:
            if memory.main.battleActive():
                partyHP = memory.main.getBattleHP()
                # Someone requires reviving.
                if partyHP[0] == 0 or partyHP[1] == 0:
                    print("Tros: Someone fainted.")
                    revive()
                    Revives += 1
                elif screen.turnRikku():
                    print("Rikku turn")
                    grenadeSlot = memory.main.getItemSlot(35)
                    grenadeCount = memory.main.getItemCountSlot(grenadeSlot)
                    print("------------------------------")
                    print("Current grenade count:", grenadeCount)
                    print("Grenades used:", Grenades)
                    print("------------------------------")
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
                        if trosPos != 1 and advances in [1, 2]:
                            Steal()
                            Steals += 1
                        else:
                            grenadeSlot = memory.main.getUseItemsSlot(35)
                            useItem(grenadeSlot, 'none')
                            Grenades += 1
                elif screen.turnTidus():
                    print("Tidus turn")
                    if trosPos == 1 and memory.main.getBattleHP()[1] < 200 and memory.main.getEnemyCurrentHP()[0] > 800:
                        usePotionCharacter(6, 'l')
                    elif trosPos == 1 or memory.main.getEnemyCurrentHP()[0] < 300:
                        defend()
                    else:
                        attack('none')
                        Attacks += 1

    print("Tros battle complete.")
    memory.main.clickToControl()


def piranhas():
    encounterID = memory.main.getEncounterID()
    print("#########Seed:", memory.main.rngSeed())
    # 11 = two piranhas
    # 12 = three piranhas with one being a triple formation (takes two hits)
    # 13 = four piranhas
    while not memory.main.turnReady():
        pass
    while memory.main.battleActive():
        if memory.main.turnReady():
            if memory.main.rngSeed() == 105:
                attack('none')
            elif encounterID == 11 or (encounterID == 12 and memory.main.battleType() == 1):
                attack('none')
            else:
                escapeAll()
    memory.main.clickToControl()


def besaid():
    print("Fight start: Besaid battle")
    FFXC.set_neutral()
    while not memory.main.turnReady():
        pass
    battleFormat = memory.main.getEncounterID()
    print("Besaid battle format number:", battleFormat)
    while memory.main.battleActive():  # AKA end of battle screen
        if memory.main.turnReady():
            enemyHP = memory.main.getEnemyCurrentHP()
            print("Enemy HP:", enemyHP)
            if screen.turnYuna():
                buddySwapWakka()
            elif screen.turnLulu():
                thunderTarget(22, 'l')
            elif screen.turnWakka():
                attackByNum(20, direction='r')
            elif screen.turnTidus():
                attackByNum(21, direction='r')

    memory.main.clickToControl()


def SinFin():
    print("Fight start: Sin's Fin")
    screen.awaitTurn()
    finTurns = 0
    kimTurn = False
    complete = False
    while not complete:
        if memory.main.turnReady():
            finTurns += 1
            print("Determining first turn.")
            if screen.turnTidus():
                defend()
                print("Tidus defend")
            elif screen.turnYuna():
                buddySwapLulu()  # Yuna out, Lulu in
                thunderTarget(target=23, direction='r')
            elif screen.turnKimahri():
                lancetTarget(target=23, direction='r')
                kimTurn = True
            elif screen.turnLulu():
                thunderTarget(target=23, direction='r')
            else:
                defend()
        if finTurns >= 3 and kimTurn:
            complete = True

    print("First few turns are complete. Now for the rest of the fight.")
    # After the first two turns, the rest of the fight is pretty much scripted.
    turnCounter = 0
    while not memory.main.battleComplete():
        if memory.main.turnReady():
            turnCounter += 1
            if screen.turnKimahri():
                screen.awaitTurn()
                lancetTarget(23, 'r')
            elif screen.turnLulu():
                thunderTarget(23, 'r')
            elif screen.turnTidus():
                if turnCounter < 4:
                    defend()
                    memory.main.waitFrames(30 * 0.2)
                else:
                    buddySwapYuna()
                    aeonSummon(0)
            elif screen.turnAeon():
                valeforOD(sinFin=1)
                print("Valefor energy blast")
    print("Sin's Fin fight complete")
    xbox.clickToBattle()


def Echuilles():
    print("Fight start: Sinspawn Echuilles")
    screen.awaitTurn()
    print("Sinspawn Echuilles fight start")
    logs.writeRNGTrack("######################################")
    logs.writeRNGTrack("Echuilles start")
    logs.writeRNGTrack(memory.main.rng10Array(arrayLen=1))

    tidusCounter = 0
    while not memory.main.turnReady():
        pass
    while memory.main.battleActive():  # AKA end of battle screen
        if memory.main.turnReady():
            if screen.faintCheck() > 0:
                revive()
            elif screen.turnTidus():
                tidusCounter += 1
                if tidusCounter <= 2:
                    print("Cheer")
                    tidusFlee()  # performs cheer command
                elif memory.main.getOverdriveBattle(0) == 100 and memory.main.getEnemyCurrentHP()[0] <= 730:
                    print("Overdrive")
                    tidusOD()
                else:
                    print("Tidus attack")
                    attack('none')
            elif screen.turnWakka():
                if tidusCounter == 1:# and memory.main.rngSeed() != 160:
                    print("Dark Attack")
                    useSkill(0)  # Dark Attack
                #elif memory.main.getEnemyCurrentHP()[0] <= 558:
                #    print("Ready for Tidus Overdrive. Wakka defends.")
                #    defend()
                else:
                    print("Wakka attack")
                    attack('none')
    print("Battle is complete. Now awaiting control.")
    while not memory.main.userControl():
        if memory.main.cutsceneSkipPossible():
            xbox.skipScene()
        elif memory.main.menuOpen() or memory.main.diagSkipPossible():
            xbox.tapB()
    logs.writeRNGTrack("######################################")
    logs.writeRNGTrack("Echuilles end")
    logs.writeRNGTrack(memory.main.rng10Array(arrayLen=1))


def lancetTutorial():
    print("Fight start: Lancet tutorial fight (Kilika)")
    xbox.clickToBattle()
    lancet('none')

    while not memory.main.turnReady():
        pass
    while memory.main.battleActive():  # AKA end of battle screen
        if memory.main.turnReady():
            if screen.turnTidus():
                attack('none')
            elif screen.turnKimahri():
                buddySwapYuna()
                defend()
            elif screen.turnLulu():
                fire('none')
            else:
                defend()
    memory.main.clickToControl()


def KilikaWoods(valeforCharge=True, bestCharge: int = 99, nextBattle=[]):
    print("Fight start: Kilika battle")
    print("Formation:", nextBattle)
    skipCharge = False
    turnCounter = 0
    encID = memory.main.getEncounterID()
    print("Charge values:")
    print(memory.main.overdriveState())
    screen.awaitTurn()

    FFXC.set_neutral()

    # These battles we want nothing to do with.
    if encID == 32:
        skipCharge = True
    # Only occurs if no best charge possible in the first three battles.
    elif bestCharge == 99:
        bestCharge = encID

    print("Kilika battle")
    aeonTurn = False
    yunaWent = False
    while not memory.main.turnReady():
        pass
    while memory.main.battleActive():  # AKA end of battle screen
        if not valeforCharge and not skipCharge and bestCharge == nextBattle:  # Still to charge Valefor
            if memory.main.turnReady():
                print("------------------------------")
                print("Battle Turn")
                print("Battle Number:", encID)
                print("Valefor charge state:", valeforCharge)
                print("skipCharge state:", skipCharge)
                turnCounter += 1
                if not (0 in memory.main.getActiveBattleFormation() and checkCharacterOk(0)) and not screen.turnAeon():
                    fleeAll()
                elif turnCounter > 7:
                    fleeAll()
                    break
                elif screen.faintCheck():
                    revive()
                elif screen.turnKimahri() or screen.turnLulu():
                    if memory.main.getBattleCharSlot(4) >= 3:
                        buddySwapWakka()
                    elif memory.main.getBattleCharSlot(0) >= 3:
                        buddySwapTidus()
                    else:
                        buddySwapYuna()
                elif encID == 31:  # Working just fine.
                    print("Logic for battle number 31")
                    if screen.turnTidus():
                        attack('none')
                    elif screen.turnYuna():
                        aeonSummon(0)
                        screen.awaitTurn()
                        if not aeonTurn:
                            aeonTurn = True
                            if memory.main.getNextTurn() < 20:
                                aeonShield()
                        aeonBoost()
                        screen.awaitTurn()
                        aeonBoost()
                        screen.awaitTurn()
                        aeonSpell(2)
                    elif screen.turnAeon():
                        aeonSpellDirection(2, 'right')
                    else:
                        defend()
                elif encID == 33:
                    print("Logic for battle number 33")
                    if screen.turnYuna():

                        aeonSummon(0)
                        screen.awaitTurn()
                        if not aeonTurn:
                            aeonTurn = True
                            if memory.main.getNextTurn() < 20:
                                aeonShield()
                        aeonBoost()
                        screen.awaitTurn()
                        aeonSpellDirection(1, 'left')
                    elif screen.turnAeon():
                        aeonSpell(2)
                    else:
                        defend()

                elif encID == 34:
                    print("Logic for battle number 34")
                    if screen.turnTidus():
                        attack('none')
                    elif screen.turnYuna():
                        aeonSummon(0)
                        screen.awaitTurn()
                        if not aeonTurn:
                            aeonTurn = True
                            if memory.main.getNextTurn() < 20:
                                aeonShield()
                        aeonBoost()
                        screen.awaitTurn()
                        aeonSpellDirection(1, 'right')
                    elif screen.turnAeon():
                        aeonSpell2(2, 'left')
                    else:
                        defend()
                elif encID == 35:
                    print("Logic for battle number 35")
                    if screen.turnTidus():
                        defend()
                    elif screen.turnYuna():
                        aeonSummon(0)
                        screen.awaitTurn()
                        if not aeonTurn:
                            aeonTurn = True
                            if memory.main.getNextTurn() < 20:
                                aeonShield()
                        aeonBoost()
                        screen.awaitTurn()
                        sonicWings()
                        screen.awaitTurn()
                        aeonSpell(0)
                    elif screen.turnAeon():
                        aeonSpell(0)
                    else:
                        defend()
                elif encID == 37:
                    print("Logic for battle number 37 - two bees and a plant thingey")
                    if screen.turnTidus():
                        attack('none')
                    elif screen.turnYuna():
                        aeonSummon(0)
                        screen.awaitTurn()
                        if not aeonTurn:
                            aeonTurn = True
                            if memory.main.getNextTurn() < 20:
                                aeonShield()
                        aeonSpellDirection(1, 'right')
                        screen.awaitTurn()
                        aeonSpellDirection(1, 'right')
                    elif screen.turnAeon():
                        while not memory.main.battleComplete():
                            if memory.main.turnReady():
                                aeonSpell(0)
                    else:
                        defend()
                else:
                    skipCharge = True
                    print("Not going to charge Valefor. Battle num:", encID)
        else:
            if memory.main.turnReady():
                print("------------------------------")
                print("Battle Turn")
                print("Battle Number:", encID)
                print("Valefor charge state:", valeforCharge)
                print("skipCharge state:", skipCharge)
                turnCounter += 1
                if not (0 in memory.main.getActiveBattleFormation() and checkCharacterOk(0)) and not screen.turnAeon():
                    fleeAll()
                elif turnCounter > 7:
                    fleeAll()
                    break
                elif screen.faintCheck():
                    revive()
                elif memory.main.getSpeed() >= 16:
                    fleeAll()
                elif screen.turnKimahri():
                    if memory.main.getBattleCharSlot(4) >= 3:
                        buddySwapWakka()
                    elif memory.main.getBattleCharSlot(0) >= 3:
                        buddySwapTidus()
                    else:
                        buddySwapYuna()
                elif screen.turnLulu() and encID != 37:
                    if memory.main.getBattleCharSlot(4) >= 3:
                        buddySwapWakka()
                    elif memory.main.getBattleCharSlot(0) >= 3:
                        buddySwapTidus()
                    else:
                        buddySwapYuna()
                elif encID == 31:
                    if screen.turnTidus():
                        if turnCounter < 4:
                            attackByNum(num=20, direction='l')
                        #If Wakka crit, we can use that instead. Slightly faster.
                        else:
                            fleeAll()
                    elif screen.turnWakka() and memory.main.getEnemyCurrentHP()[0] != 0:
                        attackByNum(num=20, direction='l')
                    else:
                        defend()
                elif encID == 32:
                    if screen.turnTidus():
                        if turnCounter < 4:
                            attackByNum(20, 'r')
                        else:
                            fleeAll()
                    elif screen.turnWakka():
                        attackByNum(21, 'r')
                    else:
                        defend()
                elif encID == 33:
                    if screen.turnTidus():
                        if turnCounter < 4:
                            defend()
                        else:
                            fleeAll()
                    elif screen.turnWakka():
                        attackByNum(21, 'r')
                    else:
                        defend()
                elif encID == 34:
                    if screen.turnTidus():
                        if turnCounter < 4:
                            attack('none')
                        else:
                            fleeAll()
                    elif screen.turnWakka():
                        attackByNum(22, 'r')
                    else:
                        defend()
                elif encID == 35 or encID == 36:
                    fleeAll()
                elif encID == 37:
                    if memory.main.getSpeed() >= 16:
                        fleeAll()
                    elif yunaWent:
                        fleeAll()
                    elif screen.turnWakka() and memory.main.getEnemyCurrentHP()[2] != 0:
                        attackByNum(22, 'l')
                        yunaWent = True
                    elif screen.turnYuna():
                        buddySwapLulu()
                        thunderTarget(target=21, direction='l')
                    else:
                        defend()
    FFXC.set_neutral()
    memory.main.clickToControl()  # Rewards screen
    hpCheck = memory.main.getHP()
    if hpCheck[0] < 250 or hpCheck[1] < 250 or hpCheck[4] < 250:
        healUp(3)
    else:
        print("No need to heal up. Moving onward.")
    if not valeforCharge and memory.main.overdriveState()[8] == 20:
        valeforCharge = True
    print("Returning Valefor Charge value:", valeforCharge)
    return valeforCharge


def sonicWings():
    print("Valefor attempting to use Sonic Wings - 1")
    while memory.main.battleMenuCursor() != 204:
        if memory.main.battleMenuCursor() == 203:
            xbox.tapDown()
        else:
            xbox.tapUp()
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()
    print("Valefor attempting to use Sonic Wings - 2")


def Geneaux():
    print("Fight start: Sinspawn Geneaux")
    xbox.clickToBattle()

    if screen.turnTidus():
        attack('none')
    elif screen.turnYuna():
        buddySwapKimahri()
        attack('none')
        while not screen.turnTidus():
            defend()
        while screen.turnTidus():
            defend()
        buddySwapYuna()
    screen.awaitTurn()
    aeonSummon(0)  # Summon Valefor
    screen.awaitTurn()
    valeforOD()

    while not memory.main.battleComplete():  # AKA end of battle screen
        if memory.main.diagSkipPossible():
            xbox.tapB()
        elif memory.main.turnReady():
            print("Valefor casting Fire")
            aeonSpell(0)
        else:
            FFXC.set_neutral()
    print("Battle Complete")
    memory.main.clickToControl()


def LucaWorkers():
    print("Fight start: Workers in Luca")
    xbox.clickToBattle()

    while not memory.main.turnReady():
        pass
    while memory.main.battleActive():  # AKA end of battle screen
        if memory.main.turnReady():
            if screen.turnKimahri() or screen.turnTidus():
                if screen.faintCheck() >= 1:
                    revive()
                else:
                    defend()
            if screen.turnLulu():
                thunder('none')
        elif memory.main.diagSkipPossible():
            xbox.tapB()  # Clicking to get through the battle faster
    memory.main.clickToControl()


def LucaWorkers2(earlyHaste):
    print("Fight start: Workers in Luca")
    hasted = False
    xbox.clickToBattle()

    while not memory.main.turnReady():
        pass
    while memory.main.battleActive():  # AKA end of battle screen
        if memory.main.turnReady():
            if screen.faintCheck() >= 1:
                revive()
            elif earlyHaste >= 1:
                if screen.turnTidus() and not hasted:
                    tidusHaste('left', character=5)
                    hasted = True
                elif screen.turnLulu():
                    thunder('none')
                else:
                    defend()
            elif memory.main.lucaWorkersBattleID() in [44, 35]:
                if screen.turnTidus():
                    attack('none')
                elif screen.turnKimahri():
                    if memory.main.getEnemyCurrentHP().count(0) == 1 and memory.main.getOverdriveBattle(3) == 100 and memory.main.getEnemyCurrentHP()[0] > 80:
                        kimahriOD(1)
                    else:
                        attack('none')
                elif screen.turnLulu():
                    thunder('right')
            else:
                if screen.turnLulu():
                    thunder('none')
                else:
                    defend()
        elif memory.main.diagSkipPossible():
            xbox.tapB()  # Clicking to get through the battle faster
    memory.main.clickToControl()


def Oblitzerator(earlyHaste):
    print("Fight start: Oblitzerator")
    xbox.clickToBattle()
    crane = 0

    if earlyHaste >= 1:
        # First turn is always Tidus. Haste Lulu if we've got the levels.
        tidusHaste(direction='left', character=5)

    while not memory.main.battleComplete():  # AKA end of battle screen
        if memory.main.turnReady():
            if crane < 3:
                if screen.turnLulu():
                    crane += 1
                    thunderTarget(target=21, direction='r')
                else:
                    defend()
            elif crane == 3:
                if screen.turnTidus():
                    crane += 1
                    while memory.main.mainBattleMenu():
                        xbox.tapLeft()
                    while memory.main.battleCursor2() != 1:
                        xbox.tapDown()
                    while memory.main.otherBattleMenu():
                        xbox.tapB()
                    tapTargeting()
                elif screen.turnLulu():
                    thunder('none')
                else:
                    defend()
            else:
                if screen.turnLulu():
                    thunder('none')
                elif screen.turnTidus():
                    attackOblitzEnd()
                else:
                    defend()
        elif memory.main.diagSkipPossible():
            xbox.tapB()
    print("End of fight, Oblitzerator")
    memory.main.clickToControl()
    # logs.writeStats("RNG02 after battle:")
    # logs.writeStats(memory.s32(memory.rng02()))


def afterBlitz1(earlyHaste):
    print("Fight start: After Blitzball (the fisheys)")
    print(earlyHaste)
    if earlyHaste != -1:
        screen.awaitTurn()

        # Tidus haste self
        tidusHaste('none')
    wakkaTurns = 0

    while not memory.main.battleComplete():
        if memory.main.turnReady():
            print("Enemy HP:", memory.main.getEnemyCurrentHP())
            if screen.turnTidus():
                attack('none')
            else:
                wakkaTurns += 1
                hpValues = memory.main.getBattleHP()
                if wakkaTurns < 3:
                    attackByNum(22, 'l')
                elif hpValues[1] < 200:  # Tidus HP
                    usePotionCharacter(0, 'u')
                elif hpValues[0] < 100:  # Wakka HP
                    usePotionCharacter(4, 'u')
                else:
                    defend()


def afterBlitz3(earlyHaste):
    print("Ready to take on Garuda")
    print(earlyHaste)
    # Wakka dark attack, or Auron power break
    screen.awaitTurn()
    tidusTurn = 0
    darkAttack = False
    while not memory.main.turnReady():
        pass
    while memory.main.battleActive():
        hpValues = memory.main.getBattleHP()
        if screen.turnAuron():
            attack('none')
        elif screen.turnTidus():
            if tidusTurn == 0:
                tidusHaste('d', character=2)
                tidusTurn += 1
            elif tidusTurn == 1:
                attack('none')
                tidusTurn += 1
            elif hpValues[0] < 202:
                usePotionCharacter(2, 'u')
            else:
                defend()
        elif screen.turnWakka():
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
    memory.main.waitFrames(30 * 4)
    FFXC.set_value('BtnB', 0)
    print("Battle complete (Garuda)")
    # Get to control
    while not memory.main.userControl():
        if memory.main.cutsceneSkipPossible():
            while not memory.main.diagProgressFlag() == 1:
                if memory.main.cutsceneSkipPossible():
                    xbox.skipScene()
            if gameVars.csr():
                memory.main.waitFrames(60)
            else:
                xbox.awaitSave(index=1)
        elif memory.main.diagSkipPossible() or memory.main.menuOpen():
            xbox.tapB()


def afterBlitz3LateHaste(earlyHaste):
    print("Ready to take on Zu")
    print(earlyHaste)
    # Wakka dark attack, or Auron power break
    screen.awaitTurn()
    if screen.turnAuron():
        print("Auron's turn")
        useSkill(0)
    elif screen.turnTidus():
        print("Tidus' turn")
        if earlyHaste != -1:
            tidusHaste('up')
        else:
            attack('none')
    else:
        print("Wakkas turn")
        useSkill(0)
    screen.awaitTurn()
    if screen.turnAuron():
        useSkill(0)
    elif screen.turnTidus():
        if earlyHaste != -1:
            tidusHaste('up')
        else:
            attack('none')
    else:
        useSkill(0)
    screen.awaitTurn()
    if screen.turnAuron():
        useSkill(0)
    else:
        useSkill(0)

    while not memory.main.turnReady():
        pass
    while memory.main.battleActive():
        if memory.main.turnReady():
            if screen.faintCheck() > 0:
                revive()
            else:
                attack('none')
    FFXC.set_value('BtnB', 1)
    memory.main.waitFrames(30 * 4)
    FFXC.set_value('BtnB', 0)
    print("Battle complete (Garuda)")
    # Get to control
    while not memory.main.userControl():
        if memory.main.cutsceneSkipPossible():
            while not memory.main.diagProgressFlag() == 1:
                if memory.main.cutsceneSkipPossible():
                    xbox.skipScene()
            if gameVars.csr():
                memory.main.waitFrames(60)
            else:
                xbox.awaitSave(index=1)
        elif memory.main.diagSkipPossible() or memory.main.menuOpen():
            xbox.tapB()


def MiihenRoad(selfDestruct=False):
    print("Fight start: Mi'ihen Road")
    print("Mi'ihen battle. Self-destruct: ", gameVars.selfDestructGet())
    battle = memory.main.getEncounterID()

    while not memory.main.battleComplete():  # AKA end of battle screen
        if memory.main.battleType() == 2 and not checkTidusOk():
            print("Looks like we got ambushed. Skipping this battle.")
            fleeAll()
            break
        if memory.main.turnReady():
            if screen.turnTidus():
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
    while not memory.main.userControl():
        FFXC.set_value('BtnB', 1)
        memory.main.waitFrames(2)
        FFXC.set_value('BtnB', 0)
        memory.main.waitFrames(3)
    hpCheck = memory.main.getHP()
    print("------------------ HP check:", hpCheck)
    if hpCheck[0] < 520 or hpCheck[2] < 900 or hpCheck[4] < 800:
        memory.main.fullPartyFormat('kilikawoods1', fullMenuClose=False)
        healUp()
    else:
        print("No need to heal up. Moving onward.")
        memory.main.fullPartyFormat('kilikawoods1')

    print("selfDestruct flag:", gameVars.selfDestructGet())


def chocoEater():
    print("Fight start: Chocobo Eater")
    rng44Last = memory.main.rngFromIndex(44)
    turns = 0
    chocoTarget = 255
    chocoNext = False
    chocoHaste = False
    screen.awaitTurn()
    charHpLast = memory.main.getBattleHP()
    
    #If chocobo doesn't take the second turn, that means it out-sped Tidus.
    if memory.main.getNextTurn() != 20:
        if memory.main.rngFromIndex(44) == rng44Last:
            # Eater did not take an attack, but did take first turn. Should register as true.
            chocoNext = True
    
    while memory.main.battleActive():
        if memory.main.turnReady():
            if chocoNext == True:
                chocoNext = False
                if memory.main.getBattleHP() != charHpLast: #We took damage
                    pass
                elif memory.main.rngFromIndex(44) != rng44Last: #Chocobo eater attacked, covers miss
                    pass
                elif chocoTarget == 255 and 1 not in memory.main.getActiveBattleFormation():
                    chocoIndex = memory.main.actorIndex(actorNum=4200)
                    print("#####  Chocobo index: ", chocoIndex)
                    chocoAngle = memory.main.getActorAngle(chocoIndex)
                    if chocoAngle > 0.25:
                        print("#####  Chocobo angle: ", chocoAngle)
                        print("#####  Selecting friendly target 2")
                        chocoTarget = memory.main.getActiveBattleFormation()[0]
                    elif chocoAngle < -0.25:
                        print("#####  Chocobo angle: ", chocoAngle)
                        print("#####  Selecting friendly target 0")
                        chocoTarget = memory.main.getActiveBattleFormation()[2]
                    else:
                        print("#####  No Angle, using last hp's: ", charHpLast)
                        print("#####  Selecting friendly target 1")
                        chocoTarget = memory.main.getActiveBattleFormation()[1]
            turns += 1
            if chocoTarget == memory.main.getBattleCharTurn():
                if 1 not in memory.main.getActiveBattleFormation():
                    buddySwapYuna()
                    attackByNum(1)
                    chocoTarget = 255
            if memory.main.getNextTurn() == 20:
                chocoNext = True
                charHpLast = memory.main.getBattleHP()
                rng44Last = memory.main.rngFromIndex(44)
            if chocoTarget != 255:
                print("#####  Target for You're Next attack: ", chocoTarget)
            
            # Only if two people are down, very rare but for safety.
            if screen.faintCheck() > 1:
                print("Attempting revive")
                revive()
            #elif 0 not in memory.main.getActiveBattleFormation():
                #Doesn't work - it still hits Tidus if he swapped out and back in (instead of Yuna).
            #    buddySwapTidus()
            elif 1 in memory.main.getActiveBattleFormation() and not chocoHaste and memory.main.getBattleCharTurn() == 0:
                tidusHaste(direction='l', character=20) #After Yuna in, haste choco eater.
                chocoHaste = True
            else:
                print("Attempting defend")
                defend()
        elif memory.main.diagSkipPossible():
            print("Skipping dialog")
            xbox.tapB()
    # logs.writeStats("Chocobo eater turns:")
    # logs.writeStats(str(turns))
    print("Chocobo Eater battle complete.")


def aeonShield():
    print("Aeon Shield function")
    screen.awaitTurn()
    memory.main.waitFrames(6)
    while not memory.main.otherBattleMenu():
        xbox.tapRight()
    if gameVars.usePause():
        memory.main.waitFrames(2)
    while memory.main.otherBattleMenu():
        if memory.main.battleCursor2() == 0:
            xbox.tapB()
        else:
            xbox.tapUp()
    tapTargeting()


def aeonBoost():
    print("Aeon Boost function")
    screen.awaitTurn()
    memory.main.waitFrames(6)
    while not memory.main.otherBattleMenu():
        xbox.tapRight()
    if gameVars.usePause():
        memory.main.waitFrames(2)
    while memory.main.otherBattleMenu():
        if memory.main.battleCursor2() == 1:
            xbox.tapB()
        elif memory.main.battleCursor2() == 0:
            xbox.tapDown()
        else:
            xbox.tapUp()
    tapTargeting()


def aeonDismiss():
    print("Aeon Dismiss function")
    screen.awaitTurn()
    memory.main.waitFrames(6)
    while not memory.main.otherBattleMenu():
        xbox.tapRight()
    if gameVars.usePause():
        memory.main.waitFrames(2)
    while memory.main.otherBattleMenu():
        if memory.main.battleCursor2() == 2:
            xbox.tapB()
        else:
            xbox.tapDown()
    tapTargeting()


def mrrTarget():
    encID = memory.main.getEncounterID()
    if encID == 96:
        attackByNum(22, 'r')
    elif encID == 97:
        attackByNum(20, 'r')
    elif encID == 98:
        lancetTarget(target=21, direction='d')
    elif encID == 101:
        lancetTarget(target=21, direction='l')
    elif encID in [100, 110]:
        attackByNum(22, 'l')
    elif encID in [102, 112, 113]:
        attackByNum(20, 'l')
    elif encID in [109, 111]:
        lancetTarget(target=20, direction='l')
    else:
        defend()
    return memory.main.nextCrit(character=3, charLuck=18, enemyLuck=15)


def MRRbattle(status):
    gameVars = vars.varsHandle()
    # Yuna complete, Kimahri complete, Valefor overdrive, Battle counter, Yuna level up complete, Yuna grid, phase
    print("------------------------------")
    print("------------------------------")
    print("Fight start: MRR")
    battle = memory.main.getEncounterID()
    print("Battle number:", battle)
    # nextCritKim = memory.nextCrit(character=3, charLuck=18, enemyLuck=15)

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
    screen.awaitTurn()

    aeonTurn = 0

    # If we're ambushed and take too much damage, this will trigger first.
    hpArray = memory.main.getBattleHP()
    hpTotal = hpArray[0] + hpArray[1] + hpArray[2]
    # Final charging for Yuna is a lower overall party HP
    if hpTotal < 1800 and status[5] != 2:
        print("------------We got ambushed. Not going to attempt to recover.")
        fleeAll()
    elif screen.faintCheck() >= 1:
        print("------------Someone is dead from the start of battle. Just get out.")
        fleeAll()
    elif checkPetrify():
        print("------------Someone has been petrified which messes up the battle logic. Escaping.")
        fleeAll()
    elif battle == 102:  # Garuda, flee no matter what.
        fleeAll()
    elif status[5] == 0:  # Phase zero - use Valefor overdrive to overkill for levels
        if status[3] < 3 and memory.main.rngSeed() != 160:  # Battle number (zero-index)
            if battle == 100 or battle == 101:  # The two battles with Funguar
                while memory.main.battleActive():  # end of battle screen
                    if memory.main.turnReady():
                        if checkPetrify():
                            print("------------Someone has been petrified which messes up the battle logic. Escaping.")
                            fleeAll()
                        elif screen.turnTidus():
                            buddySwapKimahri()
                        elif screen.turnKimahri():
                            # if nextCritKim > 9 - status[3] and nextCritKim < 23 - (status[3] * 2):
                            #    nextCritKim = mrrTarget()
                            # else:
                            defend()
                        elif screen.turnWakka():
                            defend()
                        else:
                            buddySwapYuna()
                            aeonSummon(0)
                            screen.awaitTurn()
                            valeforOD(version=1)
                            status[2] = 1
                            status[5] = 1
            else:
                fleeAll()
        else:  # Starting with fourth battle, overdrive on any battle that isn't Garuda.
            while memory.main.battleActive():  # end of battle screen
                if memory.main.turnReady():
                    if checkPetrify():
                        print("------------Someone has been petrified which messes up the battle logic. Escaping.")
                        fleeAll()
                    elif screen.turnTidus():
                        buddySwapKimahri()
                    elif screen.turnKimahri():
                        # if nextCritKim > 9 - status[3] and nextCritKim < 23 - (status[3] * 2):
                        #     nextCritKim = mrrTarget()
                        # else:
                        defend()
                    elif screen.turnWakka():
                        defend()
                    else:
                        buddySwapYuna()
                        aeonSummon(0)
                        screen.awaitTurn()
                        valeforOD(version=1)
                        status[2] = 1
                        status[5] = 1
    elif status[5] == 1:  # Next need to recharge Valefor
        valeforChargeComplete = True
        if memory.main.battleType() == 1:
            for _ in range(3):
                screen.awaitTurn()
                defend()
        if battle == 96:  # Gandarewa, Red Element, Raptor (camera front)
            wakkaTurns = 0
            while memory.main.battleActive():  # end of battle screen
                if memory.main.turnReady():
                    if checkPetrify():
                        print("Someone is pretrified. Escaping battle.")
                        fleeAll()
                        valeforChargeComplete = False
                    else:
                        print("No petrify issues.")
                        if screen.turnTidus():
                            buddySwapKimahri()
                            nextCritKim = mrrTarget()
                        elif screen.turnWakka():
                            wakkaTurns += 1
                            if wakkaTurns == 1:
                                attackByNum(21, 'l')
                            else:
                                buddySwapYuna()
                                aeonSummon(0)
                        elif screen.turnAuron():
                            attackByNum(22, 'r')
                        elif screen.turnKimahri():
                            buddySwapYuna()
                            aeonSummon(0)
                        elif screen.turnAeon():
                            if aeonTurn == 0 and memory.main.getNextTurn() < 19:
                                aeonBoost()
                                aeonTurn = 1
                            elif aeonTurn < 2:
                                aeonBoost()
                                screen.awaitTurn()
                                attack('none')
                                aeonTurn = 2
                            else:
                                aeonSpell2(3, 'none')
        elif battle == 97:  # Lamashtu, Gandarewa, Red Element (camera front)
            while memory.main.battleActive():  # end of battle screen
                if memory.main.turnReady():
                    if checkPetrify():
                        print("------------Someone has been petrified which messes up the battle logic. Escaping.")
                        fleeAll()
                    elif screen.turnTidus():
                        buddySwapKimahri()
                        nextCritKim = mrrTarget()
                    elif screen.turnWakka():
                        defend()
                    elif screen.turnAuron():
                        attack('none')
                    elif screen.turnKimahri():
                        buddySwapYuna()
                        aeonSummon(0)
                    elif screen.turnAeon():
                        if aeonTurn == 0 and memory.main.getNextTurn() < 19:
                            screen.awaitTurn()
                            aeonBoost()
                            aeonTurn = 1
                        elif aeonTurn < 2:
                            aeonSpell(2)
                            screen.awaitTurn()
                            aeonBoost()
                            aeonTurn = 2
                        else:
                            aeonSpell(3)
        elif battle == 98:  # Raptor, Red Element, Gandarewa (camera side)
            while memory.main.battleActive():  # end of battle screen
                if memory.main.turnReady():
                    if checkPetrify():
                        print("Someone is pretrified. Escaping battle.")
                        fleeAll()
                        valeforChargeComplete = False
                    else:
                        print("No petrify issues.")
                        if screen.turnTidus():
                            buddySwapKimahri()
                        elif screen.turnKimahri():
                            nextCritKim = mrrTarget()
                        elif screen.turnWakka():
                            attack('none')
                        elif screen.turnAuron():
                            buddySwapYuna()
                            aeonSummon(0)
                        elif screen.turnAeon():
                            if aeonTurn == 0 and memory.main.getNextTurn() < 19:
                                aeonBoost()
                                aeonTurn = 1
                            elif aeonTurn < 2:
                                aeonSpell2(2, 'right')
                                screen.awaitTurn()
                                aeonBoost()
                                aeonTurn = 2
                            else:
                                aeonSpell2(3, 'right')
        # battle 99 is never used.
        elif battle == 100:  # Raptor, Funguar, Red Element (camera front)
            while memory.main.battleActive():  # end of battle screen
                if memory.main.turnReady():
                    if checkPetrify():
                        print("Someone is pretrified. Escaping battle.")
                        fleeAll()
                        valeforChargeComplete = False
                    else:
                        print("No petrify issues.")
                        if screen.turnTidus():
                            buddySwapKimahri()
                            # if nextCritKim > 9 - status[3] and nextCritKim < 23 - (status[3] * 2):
                            #     nextCritKim = mrrTarget()
                            # else:
                            defend()
                        elif screen.turnWakka():
                            attack('none')
                        elif memory.main.getEnemyCurrentHP()[0] != 0:
                            buddySwapTidus()
                            fleeAll()
                            valeforChargeComplete = False
                        elif screen.turnAuron():
                            buddySwapYuna()
                            aeonSummon(0)
                        elif screen.turnAeon():
                            if aeonTurn == 0 and memory.main.getNextTurn() < 19:
                                screen.awaitTurn()
                                aeonBoost()
                                aeonTurn = 1
                            elif aeonTurn < 2:
                                aeonSpell(0)
                                screen.awaitTurn()
                                aeonBoost()
                                aeonTurn = 2
                            else:
                                aeonSpell(3)
        # Funguar, Red Element, Gandarewa (camera reverse angle)
        elif battle == 101:
            while memory.main.battleActive():  # end of battle screen
                if memory.main.turnReady():
                    if checkPetrify():
                        print("------------Someone has been petrified which messes up the battle logic. Escaping.")
                        fleeAll()
                    elif screen.turnTidus():
                        buddySwapKimahri()
                        nextCritKim = mrrTarget()
                    elif screen.turnWakka():
                        attackByNum(22, 'l')
                    elif memory.main.getEnemyCurrentHP()[2] != 0:
                        buddySwapTidus()
                        fleeAll()
                        valeforChargeComplete = False
                    elif screen.turnAuron():
                        buddySwapYuna()
                        aeonSummon(0)
                    elif screen.turnAeon():
                        if aeonTurn == 0 and memory.main.getNextTurn() < 19:
                            aeonBoost()
                            aeonTurn = 1
                        elif aeonTurn < 2:
                            aeonSpell(0)
                            screen.awaitTurn()
                            aeonBoost()
                            aeonTurn = 2
                        else:
                            aeonSpell(3)
        if valeforChargeComplete:
            status[5] = 2  # Phase 2, final phase to level up Kimahri and Yuna
            status[2] = 2  # Valefor is charged flag.
    elif status[5] == 2:  # Last phase is to level Yuna and Kimahri
        # Both Yuna and Kimahri have levels, good to go.
        if status[0] == 1 and status[1] == 1:
            status[5] = 3
            while memory.main.battleActive():  # end of battle screen
                if memory.main.turnReady():
                    fleeAll()
        else:
            # Wakka attack Raptors and Gandarewas for Yuna AP.
            yunaTurnCount = 0
            while memory.main.battleActive():  # end of battle screen
                if memory.main.turnReady():
                    if checkPetrify():
                        print("------------Someone has been petrified which messes up the battle logic. Escaping.")
                        fleeAll()
                    elif screen.turnTidus():
                        tidusFlee()
                    elif screen.faintCheck() >= 1:
                        buddySwapTidus()
                    elif screen.turnKimahri():
                        if memory.main.getKimahriSlvl() >= 6 and yunaTurnCount:
                            # if nextCritKim > 9 - status[3] and nextCritKim < 23 - (status[3] * 2):
                            #     nextCritKim = mrrTarget()
                            # else:
                            fleeAll()
                        else:
                            defend()
                    elif screen.turnYuna():
                        yunaTurnCount += 1
                        if yunaTurnCount == 1:
                            defend()
                        else:
                            fleeAll()
                    elif screen.turnWakka():
                        if battle == 96 or battle == 97 or battle == 101:
                            if battle == 101:
                                attackByNum(22, 'l')
                            else:
                                attackByNum(21, 'l')
                        elif battle == 98 or battle == 100:
                            attack('none')
                        else:
                            fleeAll()
                    else:  # Should not occur, but you never know.
                        buddySwapTidus()
    else:  # Everything is done.
        fleeAll()
    print("+++")
    print(gameVars.wakkaLateMenu())
    print("+++")
    # OK the battle should be complete now. Let's do some wrap-up stuff.
    wrapUp()

    # Check on sphere levels for our two heroes
    if status[0] == 0:
        if memory.main.getSLVLYuna() > 573:
            status[0] = 1
    if status[1] == 0:
        if memory.main.getSLVLKim() >= 495:
            status[1] = 1
    if status[5] == 2:  # Last phase is to level Yuna and Kimahri
        # Both Yuna and Kimahri have levels, good to go.
        if status[0] == 1 and status[1] == 1:
            status[5] = 3

    if status[5] == 3:
        memory.main.fullPartyFormat('mrr1', fullMenuClose=False)
    elif status[5] == 2:  # Still levelling Yuna or Kimahri
        memory.main.fullPartyFormat('mrr2', fullMenuClose=False)
        print("Yuna in front party, trying to get some more experience.")
    else:
        memory.main.fullPartyFormat('mrr1', fullMenuClose=False)

    # Now checking health values
    hpCheck = memory.main.getHP()
    print("HP values:", hpCheck)
    if status[5] == 2:
        healUp(3, fullMenuClose=False)
    elif hpCheck != [520, 475, 1030, 644, 818, 380]:
        healUp(fullMenuClose=False)
    # donezo. Back to the main path.
    print("Clean-up is now complete.")
    return status


def MRRmanip(kimMaxAdvance: int = 6):
    screen.awaitTurn()
    nextCritKim = memory.main.nextCrit(character=3, charLuck=18, enemyLuck=15)
    print("======== Next Kimahri crit:", nextCritKim)
    attemptManip = False
    if nextCritKim >= 3:
        kimTurn = True
    else:
        kimTurn = False
    while not memory.main.turnReady():
        pass
    while memory.main.battleActive():
        if memory.main.turnReady():
            nextCritKim = memory.main.nextCrit(character=3, charLuck=18, enemyLuck=15)
            print("||| Manip - Battle number:", memory.main.getEncounterID())
            print("||| Next Kimahri Crit vs Gui:", nextCritKim)
            if nextCritKim > kimMaxAdvance:
                fleeAll()
            elif kimTurn:
                attemptManip = True
                if 3 not in memory.main.getActiveBattleFormation():
                    buddySwapKimahri()
                elif screen.turnKimahri():
                    nextCritKim = mrrTarget()
                    kimTurn = False
                else:
                    defend()
            else:
                fleeAll()
    wrapUp()
    # Now checking health values
    hpCheck = memory.main.getHP()
    print("HP values:", hpCheck)
    if hpCheck != [520, 475, 1030, 644, 818, 380]:
        healUp(fullMenuClose=False)
    nextCritKim = memory.main.nextCrit(character=3, charLuck=18, enemyLuck=15)
    print("||| Manip - Battle number:", memory.main.getEncounterID())
    print("||| Next Kimahri Crit vs Gui:", nextCritKim)
    return attemptManip


def battleGui():
    print("Fight start: Sinspawn Gui")
    xbox.clickToBattle()
    print("Engaging Gui")
    print("##### Expecting crit: ", memory.main.nextCrit(character=3, charLuck=18, enemyLuck=15))
    wakkaTurn = False
    yunaTurn = False
    auronTurn = False
    tidusTurn = False
    aeonTurn = False
    kimahriCrit = False

    while not aeonTurn:
        if memory.main.turnReady():
            if screen.turnYuna():
                if not yunaTurn:
                    buddySwapAuron()
                    yunaTurn = True
                else:
                    aeonSummon(0)
            elif screen.turnWakka():
                if not wakkaTurn:
                    xbox.weapSwap(0)
                    wakkaTurn = True
                else:
                    buddySwapKimahri()
                    print("##### Expecting crit: ", memory.main.nextCrit(character=3, charLuck=18, enemyLuck=15))
            elif screen.turnKimahri():
                dmgBefore = memory.main.getEnemyCurrentHP()[0]
                kimahriOD(2)
                screen.awaitTurn()
                dmgAfter = memory.main.getEnemyCurrentHP()[0]
                damage = dmgBefore - dmgAfter
                print("Kimahri OD damage: ", damage)
                logs.writeStats("guiCrit:")
                if damage > 6000:
                    kimahriCrit = True
                    logs.writeStats("True")
                else:
                    logs.writeStats("False")
            elif screen.turnTidus():
                if not tidusTurn:
                    defend()
                    tidusTurn = True
                elif screen.faintCheck() > 0:
                    buddySwapKimahri()
                else:
                    buddySwapYuna()
            elif screen.turnAuron():
                if not auronTurn:
                    useSkill(0)
                    auronTurn = True
                elif screen.faintCheck() > 0:
                    buddySwapYuna()
                else:
                    defend()
            elif screen.turnAeon():
                valeforOD()
                aeonTurn = True

    screen.awaitTurn()
    nextHP = memory.main.getBattleHP()[0]
    lastHP = nextHP
    turn1 = False
    nextTurn = 20
    lastTurn = 20
    went = False
    while not memory.main.turnReady():
        pass
    while memory.main.battleActive():
        if memory.main.turnReady() and memory.main.getBattleCharTurn() == 8:
            nextHP = memory.main.getBattleHP()[0]
            lastTurn = nextTurn
            nextTurn = memory.main.getNextTurn()
            if went and kimahriCrit:
                aeonSpell(1)
            elif memory.main.getOverdriveBattle(8) == 20:
                print("------Overdriving")
                valeforOD()
                went = True
            elif not turn1:
                turn1 = True
                print("------Recharge unsuccessful. Attempting recovery.")
                aeonShield()
            elif lastTurn == 8:  # Valefor takes two turns in a row
                print("------Two turns in a row")
                aeonShield()
            elif nextHP > lastHP - 40 and not nextHP == lastHP:  # Gravity spell was used
                print("------Gravity was used")
                aeonShield()
            else:
                print("------Attack was just used. Now boost.")
                aeonBoost()
            lastHP = nextHP
        elif memory.main.turnReady() and memory.main.getBattleCharTurn() == 1:
            print("Yuna turn, something went wrong.")
        elif memory.main.turnReady() and memory.main.getBattleCharTurn() == 2:
            print("Auron turn, something went wrong.")
        elif memory.main.diagSkipPossible():
            xbox.tapB()
        elif screen.turnSeymour():
            break

    # In between battles
    memory.main.waitFrames(12)
    while not memory.main.turnReady():
        if memory.main.getStoryProgress() >= 865 and memory.main.cutsceneSkipPossible():
            memory.main.waitFrames(10)
            xbox.skipScene()
            print("Skipping scene")
        elif memory.main.diagSkipPossible() or memory.main.menuOpen():
            xbox.tapB()
    
    # Second Gui battle
    while memory.main.battleActive():
        turn = 1
        if memory.main.getOverdriveBattle(8) == 20 or memory.main.getOverdriveBattle(1) == 100:
            print("Special Fight")
            seymourTurn = 0
            while memory.main.battleActive():
                if screen.turnSeymour() and seymourTurn < 2:
                    seymourSpell(targetFace=False)
                    seymourTurn += 1
                elif screen.turnYuna() and seymourTurn >= 2:
                    print("Laser Time")
                    if memory.main.getOverdriveBattle(1) == 100:
                        while not memory.main.otherBattleMenu():
                            xbox.tapLeft()
                        while not memory.main.interiorBattleMenu():
                            xbox.tapB()
                        while memory.main.interiorBattleMenu():
                            xbox.tapB()
                    else:
                        aeonSummon(0)
                elif screen.turnAeon():
                    print("Firing")
                    valeforOD()
                else:
                    print("Defend")
                    defend()
        else:
            while memory.main.battleActive():
                if memory.main.turnReady():
                    if screen.turnSeymour():
                        seymourSpell(targetFace=True)
                    else:
                        defend()

    while not memory.main.userControl():
        if memory.main.cutsceneSkipPossible():
            print("Intentional delay to get the cutscene skip to work.")
            memory.main.waitFrames(2)
            xbox.skipSceneSpec()
            memory.main.waitFrames(60)
        elif memory.main.diagSkipPossible() or memory.main.menuOpen():
            xbox.tapB()

def djose(stoneBreath):
    print("Fight start: Djose road")
    while not memory.main.battleComplete():  # AKA end of battle screen
        encounterID = memory.main.getEncounterID()
        if memory.main.turnReady():
            if stoneBreath == 1:  # Stone Breath already learned
                print("Djose: Stone breath already learned.")
                fleeAll()
            else:  # Stone breath not yet learned
                if encounterID == 128 or encounterID == 134 or encounterID == 136:
                    print("Djose: Learning Stone Breath.")
                    lancetSwap('none')
                    stoneBreath = 1
                elif encounterID == 127:
                    print("Djose: Learning Stone Breath")
                    # One basilisk with two wasps
                    lancetSwap('up')
                    stoneBreath = 1
                    break
                else:
                    print("Djose: Cannot learn Stone Breath here.")
                    fleeAll()

    print("Mark 2")
    memory.main.clickToControl()
    print("Mark 3")
    partyHP = memory.main.getHP()
    print(partyHP)
    if partyHP[0] < 300 or partyHP[4] < 300:
        print("Djose: recovering HP")
        healUp(3)
    else:
        print("Djose: No need to heal.")
    memory.main.fullPartyFormat('djose')
    return stoneBreath


def wakkaOD():
    print("Wakka overdrive activating")
    while not memory.main.otherBattleMenu():
        xbox.tapLeft()
    while not memory.main.interiorBattleMenu():
        xbox.tapB()
    while memory.main.interiorBattleMenu():
        xbox.tapB()

    memory.main.waitFrames(1)
    xbox.tapB()

    while memory.main.overdriveMenuActiveWakka() == 0:
        pass
    memory.main.waitFrames(76)
    print("Hit Overdrive")
    xbox.tapB()  # First reel
    memory.main.waitFrames(13)
    xbox.tapB()  # Second reel
    memory.main.waitFrames(5)
    xbox.tapB()  # Third reel


def extractor():
    print("Fight start: Extractor")
    FFXC.set_neutral()

    screen.awaitTurn()
    tidusHaste('none')

    screen.awaitTurn()
    attack('none')  # Wakka attack

    screen.awaitTurn()
    tidusHaste('l', character=4)

    cheerCount = 0
    while not memory.main.battleComplete():  # AKA end of battle screen
        # First determine if cheers are needed.
        if gameVars.getLStrike() % 2 == 0 and cheerCount < 4:
            tidusCheer = True
        elif gameVars.getLStrike() % 2 == 1 and cheerCount < 1:
            tidusCheer = True
        else:
            tidusCheer = False
        # Then do the battle logic.
        if memory.main.specialTextOpen():
            xbox.tapB()
        elif memory.main.turnReady():
            if screen.faintCheck() > 0 and memory.main.getEnemyCurrentHP()[0] > 1100:
                revive()
            elif screen.turnTidus():
                print(memory.main.getActorCoords(3))
                if tidusCheer:
                    cheerCount += 1
                    cheer()
                elif memory.main.getEnemyCurrentHP()[0] < 1400 and not screen.faintCheck() \
                        and memory.main.getOverdriveBattle(4) == 100:
                    defend()
                else:
                    attack('none')
            else:
                if memory.main.rngSeed() == 31 and memory.main.getBattleHP()[1] < 250:

                    # This logic is specific for seed 31. Wakka is known to die on this seed if we don't heal.
                    if memory.main.getItemSlot(1) < 200:
                        print("Using hi-potion")
                        revive(itemNum=1)
                    elif memory.main.getItemSlot(2) < 200:
                        print("Using x-potion")
                        revive(itemNum=2)
                    elif memory.main.getItemSlot(8) < 200:
                        print("Using elixir")
                        revive(itemNum=8)
                    elif memory.main.getItemSlot(3) < 200:
                        print("Using mega-potion")
                        revive(itemNum=3)
                    elif memory.main.getItemSlot(0) < 200:
                        print("Using potion")
                        revive(itemNum=0)
                    else:
                        attack('none')
                elif memory.main.getEnemyCurrentHP()[0] < 1900 and memory.main.getOverdriveBattle(4) == 100:
                    wakkaOD()
                else:
                    attack('none')
        elif memory.main.diagSkipPossible():
            xbox.tapB()
    memory.main.clickToControl()


def mixTutorial():
    xbox.clickToBattle()
    Steal()
    xbox.clickToBattle()
    rikkuFullOD('tutorial')
    memory.main.clickToControl()


def thunderPlains(section):
    encID = memory.main.getEncounterID()
    nadeSlot = memory.main.getItemSlot(35)
    print("++Grenade Slot %d" % nadeSlot)
    nadeCount = memory.main.getItemCountSlot(nadeSlot)
    print("++Grenade count: %d" % nadeCount)
    print("++Speed sphere count: %d" % memory.main.getSpeed())
    useGrenades = nadeCount > 3 and memory.main.getSpeed() < 14
    print("++Use Grenades decision:", useGrenades)
    useNadeSlot = memory.main.getUseItemsSlot(35)
    lunarSlot = gameVars.getBlitzWin() or memory.main.getItemSlot(56) != 255
    lightSlot = memory.main.getItemSlot(57) != 255
    petrifySlot = memory.main.getItemSlot(49) != 255

    tidusturns = 0
    while not memory.main.turnReady():
        pass

    # Petrify check is not working. Requires review.
    if checkPetrify():
        print("------------Someone has been petrified which messes up the battle logic. Escaping.")
        fleeAll()
    elif encID in [152, 155, 162]:  # Any battle with Larvae
        if lunarSlot:
            # No longer need Lunar Curtain for Evrae fight, Blitz win logic.
            fleeAll()
        else:  # Blitz loss strat
            print("Battle with Larvae. Battle number:", encID)
            while not memory.main.battleComplete():
                if memory.main.turnReady():
                    if not lunarSlot and memory.main.turnReady():
                        if screen.turnTidus():
                            if tidusturns == 0:
                                buddySwapRikku()
                            else:
                                fleeAll()
                            tidusturns += 1
                        elif screen.turnRikku():
                            Steal()
                            lunarSlot = gameVars.getBlitzWin() or memory.main.getItemSlot(56) != 255
                        else:
                            buddySwapTidus()
                    else:
                        fleeAll()
    elif encID == 160:
        print("Battle with Iron Giant. Battle number:", encID)
        while not memory.main.battleComplete():
            screen.awaitTurn()
            if lightSlot:
                fleeAll()
            else:
                buddySwapRikku()
            while not memory.main.battleComplete():
                if screen.turnRikku():
                    if not lightSlot:
                        Steal()
                        lightSlot = memory.main.getItemSlot(57) != 255
                    elif memory.main.getOverdriveBattle(6) < 100:
                        attack('none')
                    else:
                        fleeAll()
                else:
                    if memory.main.getOverdriveBattle(6) < 100 and not checkRikkuOk():
                        escapeOne()
                    else:
                        fleeAll()
    elif encID == 161:
        print("Battle with Iron Giant and Buer monsters. Battle number:", encID)
        while not memory.main.battleComplete():
            screen.awaitTurn()
            if useGrenades or not lightSlot:
                buddySwapRikku()
                grenadeThrown = False
                while not memory.main.battleComplete():
                    if memory.main.turnReady():
                        if screen.turnRikku():
                            if useGrenades and not grenadeThrown:
                                print("Grenade Slot %d" % useNadeSlot)
                                useItem(useNadeSlot, 'none')
                                grenadeThrown = True
                            elif not lightSlot:
                                Steal()
                                lightSlot = memory.main.getItemSlot(57) != 255
                            elif memory.main.getOverdriveBattle(6) < 100:
                                attack('none')
                            else:
                                fleeAll()
                        else:
                            if not checkRikkuOk():
                                fleeAll()
                            elif memory.main.getOverdriveBattle(6) < 100:
                                escapeOne()
                            elif lightSlot and (not useGrenades or grenadeThrown):
                                fleeAll()
                            else:
                                defend()
            else:
                fleeAll()
    elif encID in [154, 156, 164] and useGrenades:
        print("Battle with random mobs including Buer. Battle number:", encID)
        while not memory.main.battleComplete():
            screen.awaitTurn()
            if useGrenades:
                buddySwapRikku()
                useItem(useNadeSlot, 'none')
            fleeAll()
    elif not gameVars.getBlitzWin() and not petrifySlot and encID in [153, 154, 163]:
        print("Grabbing petrify grenade. Blitz Loss only strat.")
        while not memory.main.battleComplete():
            if memory.main.turnReady():
                if encID in [153, 163]:
                    if screen.turnTidus():
                        buddySwapRikku()
                        screen.awaitTurn()
                        Steal()
                    else:
                        buddySwapTidus()
                        screen.awaitTurn()
                        fleeAll()
                else:
                    if screen.turnTidus():
                        buddySwapRikku()
                        screen.awaitTurn()
                        StealRight()
                    else:
                        buddySwapTidus()
                        screen.awaitTurn()
                        fleeAll()
    else:  # Nothing useful this battle. Moving on.
        fleeAll()

    print("Battle is ended - Thunder Plains")
    memory.main.clickToControl()
    memory.main.waitFrames(2)  # Allow lightning to attemt a strike
    if memory.main.dodgeLightning(gameVars.getLStrike()):
        print("Dodge")
        gameVars.setLStrike(memory.main.lStrikeCount())
    print("Checking party format and resolving if needed.")
    memory.main.fullPartyFormat('postbunyip', fullMenuClose=False)
    print("Party format is good. Now checking health values.")
    hpValues = memory.main.getHP()
    if hpValues[0] < 400 or hpValues[2] < 400 or hpValues[4] < 400 or hpValues[6] < 180:
        healUp()
    memory.main.closeMenu()
    print("Ready to continue onward.")


def mWoods(woodsVars):
    print("Logic depends on completion of specific goals. In Order:")
    print("Rikku charged, stolen Fish Scale, stolen Arctic Wind")
    print(woodsVars)
    encounterID = memory.main.getEncounterID()
    print("------------- Battle Start - Battle Number:", encounterID)
    while not memory.main.battleComplete():  # AKA end of battle screen
        if memory.main.turnReady():
            turnchar = memory.main.getBattleCharTurn()
            if not woodsVars[1] or not woodsVars[2]:
                if encounterID in [171, 172, 175]:
                    if 6 not in memory.main.getActiveBattleFormation():
                        if encounterID == 175 and memory.main.getUseItemsSlot(24) == 255:
                            buddySwapRikku()
                        elif encounterID in [171, 172] and memory.main.getUseItemsSlot(32) == 255:
                            buddySwapRikku()
                        else:
                            fleeAll()
                    elif checkPetrifyTidus() or not checkRikkuOk():
                        print("Tidus or Rikku incapacitated, fleeing")
                        fleeAll()
                    elif turnchar == 6:
                        if encounterID == 175 and memory.main.getUseItemsSlot(24) == 255:
                            print("Marker 2")
                            Steal()
                        elif encounterID == 172 and memory.main.getUseItemsSlot(32) == 255:
                            print("Marker 3")
                            StealDown()
                        elif encounterID == 171 and memory.main.getUseItemsSlot(32) == 255:
                            print("Marker 4")
                            StealRight()
                        elif memory.main.getOverdriveBattle(6) != 100:
                            print("Charging")
                            attackByNum(6, 'u')
                        else:
                            print("Escaping")
                            fleeAll()
                    else:
                        if woodsVars[0] or memory.main.getOverdriveBattle(6) == 100:
                            if encounterID in [171, 172] and memory.main.getUseItemsSlot(32) == 255:
                                escapeOne()
                            elif encounterID == 175 and memory.main.getUseItemsSlot(24) == 255:
                                escapeOne()
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
                elif 6 not in memory.main.getActiveBattleFormation():
                    buddySwapRikku()
                elif memory.main.getOverdriveBattle(6) == 100:
                    fleeAll()
                else:
                    escapeOne()
            else:
                fleeAll()

    print("Battle complete, now to deal with the aftermath.")
    memory.main.clickToControl3()
    print("M.woods, back in control")
    if memory.main.overdriveState()[6] == 100:
        woodsVars[0] = True
    if memory.main.getUseItemsSlot(32) != 255:
        woodsVars[1] = True
    if memory.main.getUseItemsSlot(24) != 255:
        woodsVars[2] = True
    print("Checking battle formation.")
    print("Party format is now good. Let's check health.")
    # Heal logic
    partyHP = memory.main.getHP()
    if partyHP[0] < 450 or partyHP[6] < 180 or partyHP[2] + partyHP[4] < 500:
        healUp()
    memory.main.closeMenu()
    print("And last, we'll update variables.")
    print("Rikku charged, stolen Fish Scale, stolen Arctic Wind")
    print(woodsVars)
    print("HP is good. Onward!")
    return woodsVars


def spheriSpellItemReady():
    if memory.main.getCharWeakness(20) == 1:
        if memory.main.getItemSlot(27) > 200:
            return False
    elif memory.main.getCharWeakness(20) == 2:
        if memory.main.getItemSlot(24) > 200:
            return False
    elif memory.main.getCharWeakness(20) == 4:
        if memory.main.getItemSlot(30) > 200:
            return False
    elif memory.main.getCharWeakness(20) == 8:
        if memory.main.getItemSlot(32) > 200:
            return False
    return True


# Process written by CrimsonInferno
def spherimorph():
    xbox.clickToBattle()

    FFXC.set_neutral()

    spellNum = 0
    tidusturns = 0
    rikkuturns = 0
    yunaTurn = False
    kimTurn = False
    while not memory.main.turnReady():
        pass
    while memory.main.battleActive():  # AKA end of battle screen
        if memory.main.turnReady():
            if gameVars.usePause():
                memory.main.waitFrames(2)
            turnchar = memory.main.getBattleCharTurn()
            partyHP = memory.main.getBattleHP()
            if turnchar == 0:
                if tidusturns == 0:
                    equipInBattle(equipType='armor', abilityNum=0x8028)
                elif tidusturns == 1:
                    defend()
                else:
                    buddySwapRikku()
                tidusturns += 1
            elif turnchar == 1:
                rikkuslotnum = memory.main.getBattleCharSlot(6)
                if rikkuslotnum < 3 and partyHP[rikkuslotnum] == 0:
                    revive()
                    yunaTurn = True
                elif not yunaTurn:
                    defend()
                    yunaTurn = True
                elif not spheriSpellItemReady():
                    if 5 not in memory.main.getActiveBattleFormation():
                        buddySwapLulu()
                    elif 6 not in memory.main.getActiveBattleFormation():
                        buddySwapRikku()
                    else:
                        defend()
                elif 6 not in memory.main.getActiveBattleFormation():
                    buddySwapRikku()
                else:
                    defend()
                    yunaTurn = True
            elif turnchar == 3:
                rikkuslotnum = memory.main.getBattleCharSlot(6)
                if rikkuslotnum < 3 and partyHP[rikkuslotnum] == 0:
                    revive()
                    kimTurn = True
                elif not kimTurn:
                    defend()
                    kimTurn = True
                elif 6 not in memory.main.getActiveBattleFormation():
                    buddySwapRikku()
                elif 5 not in memory.main.getActiveBattleFormation():
                    buddySwapLulu()
                else:
                    defend()
            elif turnchar == 5:
                if not spheriSpellItemReady():
                    if spellNum == 1:
                        ice()
                    elif spellNum == 2:
                        water()
                    elif spellNum == 3:
                        thunder()
                    else:
                        fire()
                    screen.awaitTurn()
                    if memory.main.getCharWeakness(20) == 1:
                        spellNum = 4  # Ice
                    elif memory.main.getCharWeakness(20) == 2:
                        spellNum = 1  # Fire
                    elif memory.main.getCharWeakness(20) == 4:
                        spellNum = 3  # Water
                    elif memory.main.getCharWeakness(20) == 8:
                        spellNum = 2  # Thunder
                elif 6 not in memory.main.getActiveBattleFormation():
                    buddySwapRikku()
                else:
                    defend()
            elif turnchar == 6:
                if rikkuturns == 0:
                    print("Throwing Grenade to check element")
                    grenadeslotnum = memory.main.getUseItemsSlot(35)
                    useItem(grenadeslotnum, "none")
                    if memory.main.getCharWeakness(20) == 1:
                        spellNum = 4  # Ice
                    elif memory.main.getCharWeakness(20) == 2:
                        spellNum = 1  # Fire
                    elif memory.main.getCharWeakness(20) == 4:
                        spellNum = 3  # Water
                    elif memory.main.getCharWeakness(20) == 8:
                        spellNum = 2  # Thunder

                    # spellNum = screen.spherimorphSpell()
                elif not spheriSpellItemReady():
                    if 5 not in memory.main.getActiveBattleFormation():
                        buddySwapLulu()
                    else:
                        defend()
                else:
                    print("Starting Rikkus overdrive")
                    # logs.writeStats("Spherimorph spell used:")
                    if spellNum == 1:
                        # ogs.writeStats("Fire")
                        print("Creating Ice")
                        rikkuFullOD('spherimorph1')
                    elif spellNum == 2:
                        # logs.writeStats("Water")
                        print("Creating Water")
                        rikkuFullOD('spherimorph2')
                    elif spellNum == 3:
                        # logs.writeStats("Thunder")
                        print("Creating Thunder")
                        rikkuFullOD('spherimorph3')
                    elif spellNum == 4:
                        # logs.writeStats("Ice")
                        print("Creating Fire")
                        rikkuFullOD('spherimorph4')

                rikkuturns += 1

    if not gameVars.csr():
        xbox.SkipDialog(5)


def negator():  # AKA crawler
    print("Starting battle with Crawler")
    xbox.clickToBattle()

    tidusturns = 0
    rikkuturns = 0
    kimahriturns = 0
    luluturns = 0
    yunaturns = 0

    while not memory.main.turnReady():
        pass
    while memory.main.battleActive():  # AKA end of battle screen
        FFXC.set_neutral()
        if memory.main.turnReady():
            turnchar = memory.main.getBattleCharTurn()
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
                    lightningmarbleslot = memory.main.getUseItemsSlot(30)
                    if rikkuturns < 1:
                        useItem(lightningmarbleslot, target=21)
                    else:
                        useItem(lightningmarbleslot, target=21)
                else:
                    print("Starting Rikkus overdrive")
                    rikkuFullOD('crawler')
                rikkuturns += 1
            elif turnchar == 3:
                if kimahriturns == 0:
                    lightningmarbleslot = memory.main.getUseItemsSlot(30)
                    useItem(lightningmarbleslot, target=21)
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
        elif memory.main.diagSkipPossible():
            xbox.tapB()

    memory.main.clickToControl()


def getAnimaItemSlot():
    useableSlot = memory.main.getUseItemsSlot(32)
    if useableSlot > 200:
        useableSlot = memory.main.getUseItemsSlot(30)
    if useableSlot > 200:
        useableSlot = memory.main.getUseItemsSlot(24)
    if useableSlot > 200:
        useableSlot = memory.main.getUseItemsSlot(27)
    if useableSlot > 200:
        useableSlot = 255
    return useableSlot


# Process written by CrimsonInferno
def seymourGuado_blitzWin():
    tidushaste = False
    kimahriconfused = False
    missbackup = False
    kimahridead = False
    tidusturns = 0
    yunaturns = 0
    kimahriturns = 0
    auronturns = 0
    wakkaturns = 0
    rikkuturns = 0
    animahits = 0
    animamiss = 0

    while not memory.main.turnReady():
        pass
    screen.awaitTurn()
    while memory.main.battleActive():  # AKA end of battle screen
        if memory.main.turnReady():
            turnchar = memory.main.getBattleCharTurn()
            for i in range(0, 3):
                if memory.main.getBattleHP()[i] == 0:
                    if memory.main.getBattleCharSlot(2) == i:
                        print("Auron is dead")
                    elif memory.main.getBattleCharSlot(3) == i:
                        print("Kimahri is dead")
                        kimahridead = True
                    elif memory.main.getBattleCharSlot(4) == i:
                        print("Wakka is dead")
            if turnchar == 0:
                nextHit = rngTrack.nextActionHitMiss(character=memory.main.getCurrentTurn(), enemy="anima")
                if tidusturns == 0:
                    print("Tidus Haste self")
                    tidusHaste('none')
                    tidushaste = True
                elif tidusturns == 1:
                    print("Talk to Seymour")
                    while not memory.main.otherBattleMenu():
                        xbox.tapLeft()
                    while memory.main.battleCursor2() != 1:
                        xbox.tapDown()
                    while memory.main.otherBattleMenu():
                        xbox.tapB()
                    xbox.tapLeft()
                    tapTargeting()
                elif tidusturns == 2:
                    defend()
                elif tidusturns == 3:
                    attack(direction="none")
                elif tidusturns == 4:
                    buddySwapWakka()
                elif animahits + animamiss == 3 and animamiss > 0 and not missbackup:
                    buddySwapLulu()
                elif animahits + animamiss == 3 and not nextHit:
                    buddySwapLulu()
                    animamiss += 1
                elif not tidushaste:
                    print("Tidus Haste self")
                    tidusHaste('none')
                    tidushaste = True
                elif animahits < 4:
                    oldHP = memory.main.getEnemyCurrentHP()[3]
                    attack(direction="none")
                    newHP = memory.main.getEnemyCurrentHP()[3]
                    if newHP < oldHP:
                        print("Hit Anima")
                        animahits += 1
                    else:
                        print("Miss Anima")
                        animamiss += 1
                else:
                    attack(direction="none")
                tidusturns += 1
                print("Tidus turns: %d" % tidusturns)
            elif turnchar == 1:
                if yunaturns == 0:
                    xbox.weapSwap(0)
                else:
                    buddySwapAuron()
                yunaturns += 1
                print("Yuna turn, complete")
            elif turnchar == 3:
                if kimahriconfused:
                    tidusposition = memory.main.getBattleCharSlot(0)
                    rikkuposition = memory.main.getBattleCharSlot(6)
                    if tidusposition >= 3:
                        buddySwapTidus()
                    elif rikkuposition >= 3:
                        buddySwapRikku()
                elif kimahriturns == 0:
                    kimahriOD(3)
                elif kimahriturns == 1:
                    Steal()
                elif animamiss > 0 and (not missbackup or screen.faintCheck() == 0):
                    xbox.weapSwap(0)
                else:
                    tidusposition = memory.main.getBattleCharSlot(0)
                    rikkuposition = memory.main.getBattleCharSlot(6)
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
                    print("Yuna confusion:", memory.main.confusedState(1))
                    print("Tidus confusion:", memory.main.confusedState(0))
                    print("Kimahri confusion:", memory.main.confusedState(3))
                    print("Auron confusion:", memory.main.confusedState(2))
                    if memory.main.confusedState(3):
                        remedy(character=3,
                               direction="l")
                        kimahriconfused = True
                    else:
                        defend()
                elif auronturns == 1:  # Stone Breath logic
                    defend()
                elif animamiss > 0 and (not missbackup or screen.faintCheck() == 0):
                    if kimahridead and rikkuturns == 0:
                        buddySwapRikku()
                    else:
                        xbox.weapSwap(1)
                else:
                    tidusposition = memory.main.getBattleCharSlot(0)
                    rikkuposition = memory.main.getBattleCharSlot(6)
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
                    xbox.weapSwap(0)
                elif animamiss > 0 and (not missbackup or screen.faintCheck() == 0):
                    if kimahridead and rikkuturns == 0:
                        buddySwapRikku()
                    else:
                        xbox.weapSwap(0)
                else:
                    tidusposition = memory.main.getBattleCharSlot(0)
                    rikkuposition = memory.main.getBattleCharSlot(6)
                    if tidusposition >= 3:
                        buddySwapTidus()
                    elif rikkuposition >= 3:
                        buddySwapRikku()
                    else:
                        defend()
                wakkaturns += 1
                print("Wakka turn, complete")
            elif turnchar == 6:
                if screen.faintCheck() == 2:
                    reviveAll()
                    missbackup = True
                    tidushaste = False
                elif animamiss > 0 and (not missbackup or screen.faintCheck() == 0):
                    if kimahridead and rikkuturns == 0:
                        Steal()
                    else:
                        if memory.main.getBattleCharSlot(0) >= 3:
                            buddySwapTidus()
                        elif memory.main.getBattleCharSlot(1) >= 3:
                            buddySwapYuna()
                        elif memory.main.getBattleCharSlot(5) >= 3:
                            buddySwapLulu()
                elif animahits < 4:
                    Steal()
                elif memory.main.getBattleHP()[memory.main.getBattleCharSlot(0)] == 0:
                    reviveTarget(target=0)
                else:
                    defend()
                rikkuturns += 1
                print("Rikku turn, complete")
            elif turnchar == 5:
                if not missbackup:
                    revive()
                    missbackup = True
                else:
                    tidusposition = memory.main.getBattleCharSlot(0)
                    rikkuposition = memory.main.getBattleCharSlot(6)
                    if tidusposition >= 3:
                        buddySwapTidus()
                    elif rikkuposition >= 3:
                        buddySwapRikku()
                    else:
                        defend()
                print("Lulu turn, complete")
            else:
                print("No turn. Holding for next action.")
        elif memory.main.diagSkipPossible():
            xbox.tapB()
            print("Diag skip")
    print("Battle summary screen")
    FFXC.set_value('BtnB', 1)
    memory.main.waitFrames(30 * 2.8)
    FFXC.set_value('BtnB', 0)


def seymourGuado_blitzLoss():
    screen.awaitTurn()

    tidushaste = False
    kimahriconfused = False
    missbackup = False
    kimahridead = False
    tidusturns = 0
    yunaturns = 0
    kimahriturns = 0
    wakkaturns = 0
    rikkuturns = 0
    animahits = 0
    animamiss = 0
    thrownItems = 0

    while not memory.main.battleComplete():  # AKA end of battle screen
        if memory.main.turnReady():
            turnchar = memory.main.getBattleCharTurn()
            for i in range(0, 3):
                if memory.main.getBattleHP()[i] == 0:
                    if memory.main.getBattleCharSlot(2) == i:
                        print("Auron is dead")
                    elif memory.main.getBattleCharSlot(3) == i:
                        print("Kimahri is dead")
                        kimahridead = True
                    elif memory.main.getBattleCharSlot(4) == i:
                        print("Wakka is dead")
            if turnchar == 0:
                if memory.main.getEnemyCurrentHP()[1] < 2999:
                    attack(direction="none")
                    print("Should be last attack of the fight.")
                elif tidusturns == 0:
                    print("Tidus Haste self")
                    tidusHaste('none')
                    tidushaste = True
                elif tidusturns == 1:
                    cheer()
                elif tidusturns == 2:
                    print("Talk to Seymour")
                    while not memory.main.otherBattleMenu():
                        xbox.tapLeft()
                    while memory.main.battleCursor2() != 1:
                        xbox.tapDown()
                    while memory.main.otherBattleMenu():
                        xbox.tapB()
                    xbox.tapLeft()
                    tapTargeting()
                elif tidusturns == 3:
                    print("Swap to Brotherhood")
                    equipInBattle(special='brotherhood')
                elif tidusturns == 4:
                    tidusODSeymour()
                elif tidusturns == 5:
                    buddySwapWakka()
                elif animahits + animamiss == 3 and animamiss > 0 and not missbackup:
                    buddySwapLulu()
                    defend()
                    missbackup = True
                elif not tidushaste:
                    print("Tidus Haste self")
                    tidusHaste('none')
                    tidushaste = True
                elif animahits < 4:
                    oldHP = memory.main.getEnemyCurrentHP()[3]
                    attack(direction="none")
                    newHP = memory.main.getEnemyCurrentHP()[3]
                    if newHP < oldHP:
                        print("Hit Anima")
                        animahits += 1
                    else:
                        print("Miss Anima")
                        animamiss += 1
                else:
                    print("Plain Attacking")
                    attack(direction="none")
                tidusturns += 1
                print("Tidus turns: %d" % tidusturns)
            elif turnchar == 1:
                if yunaturns == 0:
                    xbox.weapSwap(0)
                else:
                    buddySwapLulu()
                    screen.awaitTurn()
                    print("Confused states:")
                    print("Yuna confusion:", memory.main.confusedState(1))
                    print("Tidus confusion:", memory.main.confusedState(0))
                    print("Kimahri confusion:", memory.main.confusedState(3))
                    print("Auron confusion:", memory.main.confusedState(2))
                    if memory.main.confusedState(3):
                        remedy(character=3,
                               direction="l")
                        kimahriconfused = True
                    else:
                        xbox.weapSwap(0)
                yunaturns += 1
                print("Yuna turn, complete")
            elif turnchar == 5:
                if animahits == 0:
                    print("Confused states:")
                    print("Yuna confusion:", memory.main.confusedState(1))
                    print("Tidus confusion:", memory.main.confusedState(0))
                    print("Kimahri confusion:", memory.main.confusedState(3))
                    print("Lulu confusion:", memory.main.confusedState(5))
                    buddySwapRikku()
                    if memory.main.confusedState(0):
                        remedy(character=0, direction="l")
                    elif memory.main.confusedState(3):
                        remedy(character=3, direction="l")
                else:
                    buddySwapTidus()
                    attack(direction="none")
            elif turnchar == 3:
                if kimahriconfused:
                    tidusposition = memory.main.getBattleCharSlot(0)
                    rikkuposition = memory.main.getBattleCharSlot(6)
                    if tidusposition >= 3:
                        buddySwapTidus()
                    elif rikkuposition >= 3:
                        buddySwapRikku()
                    else:
                        defend()
                elif kimahriturns == 0:
                    print("Confused states:")
                    print("Yuna confusion:", memory.main.confusedState(1))
                    print("Tidus confusion:", memory.main.confusedState(0))
                    print("Kimahri confusion:", memory.main.confusedState(3))
                    print("Auron confusion:", memory.main.confusedState(2))
                    print("Lulu confusion:", memory.main.confusedState(5))
                    if memory.main.confusedState(0):
                        remedy(character=0, direction="l")
                    elif memory.main.confusedState(1):
                        remedy(character=1, direction="l")
                    elif memory.main.confusedState(5):
                        remedy(character=5, direction="l")
                    else:
                        defend()
                elif thrownItems < 2:
                    itemSlot = getAnimaItemSlot()
                    if itemSlot != 255:
                        useItem(itemSlot)
                    else:
                        Steal()
                    thrownItems += 1
                elif animamiss > 0 and (not missbackup or screen.faintCheck() == 0):
                    Steal()
                else:
                    tidusposition = memory.main.getBattleCharSlot(0)
                    rikkuposition = memory.main.getBattleCharSlot(6)
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
                    xbox.weapSwap(0)
                elif animamiss > 0 and (not missbackup or screen.faintCheck() == 0):
                    if kimahridead and rikkuturns < 2:
                        buddySwapRikku()
                    else:
                        xbox.weapSwap(0)
                else:
                    tidusposition = memory.main.getBattleCharSlot(0)
                    rikkuposition = memory.main.getBattleCharSlot(6)
                    if tidusposition >= 3:
                        buddySwapTidus()
                    elif rikkuposition >= 3:
                        buddySwapRikku()
                    else:
                        defend()
                wakkaturns += 1
                print("Wakka turn, complete")
            elif turnchar == 6:
                if screen.faintCheck() == 2:
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
                    tidusposition = memory.main.getBattleCharSlot(0)
                    if tidusposition >= 3:
                        buddySwapTidus()
                    elif animamiss > 0 and (not missbackup or screen.faintCheck() == 0):
                        Steal()
                    elif animahits < 4:
                        Steal()
                    elif memory.main.getBattleHP()[memory.main.getBattleCharSlot(0)] == 0:
                        reviveTarget(target=0)
                    else:
                        defend()
                rikkuturns += 1
                print("Rikku turn, complete")
            else:
                print("No turn. Holding for next action.")
        elif memory.main.diagSkipPossible():
            xbox.tapB()
            print("Diag skip")
    print("Battle summary screen")
    FFXC.set_value('BtnB', 1)
    memory.main.waitFrames(30 * 2.8)
    FFXC.set_value('BtnB', 0)


def seymourGuado():
    if gameVars.getBlitzWin():
        seymourGuado_blitzWin()
    else:
        seymourGuado_blitzLoss()


def escapeWithXP():
    rikkuItem = False
    if memory.main.getItemSlot(39) > 200:
        fleeAll()
    else:
        while not memory.main.turnReady():
            pass
        while memory.main.battleActive():
            if memory.main.turnReady():
                if screen.turnTidus():
                    if not rikkuItem:
                        equipInBattle(equipType='armor', abilityNum=0x8028)
                        screen.awaitTurn()
                        buddySwapRikku()
                    else:
                        attack('none')
                elif screen.turnRikku():
                    if not rikkuItem:
                        useItem(memory.main.getUseItemsSlot(39))
                        rikkuItem = True
                    else:
                        defend()
                elif screen.turnAuron():
                    attack('none')
                else:
                    buddySwapTidus()
    memory.main.clickToControl()


def fullheal(target: int, direction: str):
    print("Full Heal function")
    if memory.main.getThrowItemsSlot(2) < 255:
        itemnum = 2
        itemname = "X-Potion"
    elif memory.main.getThrowItemsSlot(8) < 255:
        itemnum = 8
        itemname = "Elixir"
    elif memory.main.getThrowItemsSlot(3) < 255:
        itemnum = 3
        itemname = "Mega-Potion"
        target = 255
    else:
        itemnum = -1
        itemname = "noitemfound"
    if itemnum >= 0:
        print("Using %s" % itemname)
        _useHealingItem(target, direction, itemnum)
        return 1

    else:
        print("No restorative items available")
        return 0


# Process written by CrimsonInferno
def wendigoresheal(turnchar: int, usepowerbreak: int, tidusmaxHP: int):
    print("Wendigo Res/Heal function")
    partyHP = memory.main.getBattleHP()
    if screen.faintCheck() == 2:
        print("2 Characters are dead")
        if memory.main.getThrowItemsSlot(7) < 255:
            reviveAll()
        elif memory.main.getThrowItemsSlot(6) < 255:
            revive()  # This should technically target tidus but need to update this logic
    # If just Tidus is dead revive him
    elif partyHP[memory.main.getBattleCharSlot(0)] == 0:
        print("Reviving tidus")
        revive()
    elif usepowerbreak:
        print("Swapping to Auron to Power Break")
        buddySwapAuron()
    # If tidus is less than max HP heal him
    elif partyHP[memory.main.getBattleCharSlot(0)] < tidusmaxHP:
        print("Tidus need healing")
        if fullheal(target=0,
                    direction="l") == 0:
            if screen.faintCheck():
                print("No healing available so reviving instead")
                if memory.main.getThrowItemsSlot(6) < 255:
                    revive()
                elif memory.main.getThrowItemsSlot(7) < 255:
                    reviveAll()
            else:
                defend()
    elif screen.faintCheck():
        print("Reviving non-Tidus")
        revive()
    else:
        return False

    return True


def wendigo():
    phase = 0
    YunaAP = False
    guadosteal = False
    powerbreak = False
    powerbreakused = False
    usepowerbreak = False
    tidushealself = False
    tidusmaxHP = 1520
    tidushaste = False
    luluSwap = False
    stopHealing = 2500

    screen.awaitTurn()

    while not memory.main.turnReady():
        pass
    while memory.main.battleActive():  # AKA end of battle screen
        if memory.main.turnReady():
            partyHP = memory.main.getBattleHP()
            turnchar = memory.main.getBattleCharTurn()

            if partyHP[memory.main.getBattleCharSlot(0)] == 0:
                print("Tidus is dead")
                tidushaste = False
                powerbreak = True
                usepowerbreak = powerbreak and not powerbreakused

            if turnchar == 1:
                print("Yunas Turn")
                # If Yuna still needs AP:
                if not YunaAP:
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
                    elif not 5 in memory.main.getActiveBattleFormation():
                        print("Swapping to Lulu")
                        luluSwap = True
                        buddySwapLulu()
                    elif not 6 in memory.main.getActiveBattleFormation():
                        buddySwapRikku()
                    else:
                        defend()
            elif turnchar == 0:
                print("Test 1")
                if not tidushaste:
                    print("Tidus Haste self")
                    tidusHaste('none')
                    tidushaste = True
                elif phase == 0:
                    print("Switch to Brotherhood")
                    equipInBattle(special='brotherhood')
                    phase += 1
                elif phase == 1:
                    print("Attack top Guado")
                    attackByNum(22, 'd')
                    phase += 1
                elif memory.main.getEnemyCurrentHP()[1] != 0 and screen.faintCheck() == 2:
                    print("2 Characters are dead")
                    tidushealself = True
                    if memory.main.getThrowItemsSlot(7) < 255:
                        reviveAll()
                    elif memory.main.getThrowItemsSlot(6) < 255:
                        revive()
                elif memory.main.getEnemyCurrentHP()[1] < 6000 and memory.main.getOverdriveBattle(0) == 100 and not gameVars.skipKilikaLuck():
                    tidusOD('left', character=21)
                elif tidushealself:
                    if partyHP[memory.main.getBattleCharSlot(0)] < tidusmaxHP:
                        print(
                            "Tidus just used Phoenix Down / Mega Phoenix so needs to heal himself")
                        if fullheal(target=0,
                                    direction="l") == 0:
                            if screen.faintCheck():
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
                memory.main.waitFrames(30 * 0.2)
            elif turnchar == 6:
                if phase == 2:
                    phase += 1
                    lightcurtainslot = memory.main.getUseItemsSlot(57)
                    if lightcurtainslot < 255:
                        print("Using Light Curtain on Tidus")
                        useItem(lightcurtainslot, target=0)
                    else:
                        print("No Light Curtain")
                        print("Swapping to Auron to Power Break")
                        buddySwapAuron()  # Swap for Auron
                        powerbreak = True
                        usepowerbreak = True
                elif memory.main.getEnemyCurrentHP()[1] < stopHealing:
                    defend()
                elif wendigoresheal(turnchar=turnchar, usepowerbreak=usepowerbreak, tidusmaxHP=tidusmaxHP) == 0:
                    if not guadosteal and memory.main.getEnemyCurrentHP().count(0) != 2:
                        Steal()
                        guadosteal = True
                    elif memory.main.getEnemyCurrentHP().count(0) == 2 and not luluSwap:
                        luluSwap = True
                        buddySwapLulu()
                    else:
                        defend()
            elif turnchar == 2:
                if usepowerbreak:
                    print("Using Power Break")
                    useSkill(position=0, target=21)
                    powerbreakused = True
                    usepowerbreak = False
                elif memory.main.getEnemyCurrentHP()[1] < stopHealing:
                    defend()
                elif wendigoresheal(turnchar=turnchar, usepowerbreak=usepowerbreak, tidusmaxHP=tidusmaxHP) == 0:
                    defend()
            else:
                if memory.main.getEnemyCurrentHP()[1] < stopHealing:
                    print("End of battle, no need to heal.")
                    defend()
                elif memory.main.getEnemyCurrentHP()[1] != 0:
                    if wendigoresheal(turnchar=turnchar, usepowerbreak=usepowerbreak, tidusmaxHP=tidusmaxHP) == 0:
                        defend()
                else:
                    defend()

def zu():
    screen.awaitTurn()
    attack('none')
    while not memory.main.battleComplete():
        if memory.main.turnReady():
            if memory.main.partySize() <= 2:
                defend()
            else:
                fleeAll()
        elif memory.main.diagSkipPossible():
            xbox.tapB()  # Skip Dialog
    memory.main.clickToControl()


def bikanelBattleLogic(status):
    # status should be an array length 2
    # [rikkuCharged, speedNeeded, powerNeeded, itemsNeeded]
    encounterID = memory.main.getEncounterID()
    itemStolen = False
    itemThrown = False
    throwPower = False
    throwSpeed = False
    stealDirection = 'none'
    print("---------------Starting desert battle:", encounterID)

    # First, determine what the best case scenario is for each battle.
    if encounterID == 199:
        stealDirection = 'none'
        if status[1]:
            throwSpeed = True
        if status[2]:
            throwPower = True
    if encounterID == 200:
        stealDirection = 'none'
        if status[1]:
            throwSpeed = True
        if status[2]:
            throwPower = True
    if encounterID == 208:
        stealDirection = 'none'
        if status[1]:
            throwSpeed = True
        if status[2]:
            throwPower = True
    if encounterID == 209:
        stealDirection = 'right'
        if status[1]:
            throwSpeed = True
        if status[2]:
            throwPower = True
    if encounterID == 218:
        stealDirection = 'none'
        if status[2]:
            throwPower = True
    if encounterID == 221:
        stealDirection = 'up'
        if status[1]:
            throwSpeed = True
        if status[2]:
            throwPower = True
    if encounterID == 222:
        stealDirection = 'left'
        if status[2]:
            throwPower = True
    if encounterID == 226:
        stealDirection = 'none'

    zuBattles = [202, 211, 216, 225]
    if encounterID in zuBattles:  # Zu battles
        stealDirection = 'none'
    if encounterID == 217:  # Special Zu battle
        stealDirection = 'up'  # Not confirmed
    # Flee from these battles
    fleeBattles = [201, 203, 204, 205, 210, 212,
                   213, 215, 217, 219, 223, 224, 226, 227]

    # Next, determine what we want to do
    if encounterID in fleeBattles:
        if status[0]:
            battleGoal = 3  # Nothing to do here, we just want to flee.
        else:
            battleGoal = 2
    else:
        items = updateStealItemsDesert()
        if items[1] < 2:
            battleGoal = 0  # Steal an item
        elif items[1] == 0 and items[2] == 0:
            battleGoal = 0  # Steal an item
        # Extra items into power/speed
        elif status[3] <= -1 and (throwPower or throwSpeed):
            battleGoal = 1  # Throw an item
        elif status[3] > -1:
            # Steal to an excess of one item (so we can throw in future battles)
            battleGoal = 0
        elif not status[0]:
            battleGoal = 2  # Rikku still needs charging.
        else:
            battleGoal = 3  # Nothing to do but get to Home.

    # Then we take action.
    while not memory.main.battleComplete():
        if battleGoal == 0:  # Steal an item
            print("Looking to steal an item.")
            if memory.main.turnReady():
                if memory.main.getBattleCharTurn() == 0:
                    buddySwapKimahri()
                elif not itemStolen and (screen.turnKimahri() or screen.turnReady()):
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

                    # After stealing an item, what to do next?
                    if throwPower or throwSpeed:
                        battleGoal = 1
                    else:
                        battleGoal = 3
                elif not status[0]:
                    if memory.main.getBattleCharTurn() == 6:
                        attack('none')
                    else:
                        escapeOne()
                else:
                    buddySwapTidus()
                    screen.awaitTurn()
                    fleeAll()
        elif battleGoal == 1:  # Throw an item
            print("Throw item with Kimahri, everyone else escape.")
            if memory.main.turnReady():
                items = updateStealItemsDesert()
                if memory.main.getBattleCharTurn() == 0:
                    buddySwapKimahri()
                elif not itemThrown and (screen.turnKimahri() or screen.turnRikku()):
                    if items[2] >= 1:
                        itemToUse = 40
                    elif items[1] >= 1:
                        itemToUse = 37
                    elif items[3] >= 1:
                        itemToUse = 39
                    else:
                        itemToUse = 999

                    if itemToUse == 999:
                        escapeOne()
                    else:
                        useItem(memory.main.getUseItemsSlot(itemToUse), 'none')
                    itemThrown = True
                elif not status[0]:
                    if memory.main.getBattleCharTurn() == 6:
                        attack('none')
                    else:
                        escapeOne()
                else:
                    fleeAll()
        elif battleGoal == 2:  # Charge Rikku
            print("Attack/Steal with Rikku, everyone else escape.")
            if memory.main.turnReady():
                if memory.main.getBattleCharTurn() == 6:
                    attack('none')
                elif screen.turnAuron() and memory.main.getOverdriveBattle(2) != 100:
                    attackByNum(2)
                elif 6 in memory.main.getActiveBattleFormation():
                    escapeOne()
                else:
                    fleeAll()
        else:  # Charge Auron if needed, otherwise flee
            if memory.main.getOverdriveBattle(2) != 100:
                if screen.turnAuron():
                    attackByNum(2)
                else:
                    escapeOne()
            else:
                print("Flee all battles, nothing more to do.")
                fleeAll()


def updateStealItemsDesert():
    itemArray = [0, 0, 0, 0]
    # Bomb cores
    index = memory.main.getItemSlot(27)
    if index == 255:
        itemArray[0] = 0
    else:
        itemArray[0] = memory.main.getItemCountSlot(index)

    # Sleeping Powders
    index = memory.main.getItemSlot(37)
    if index == 255:
        itemArray[1] = 0
    else:
        itemArray[1] = memory.main.getItemCountSlot(index)

    # Smoke Bombs
    index = memory.main.getItemSlot(40)
    if index == 255:
        itemArray[2] = 0
    else:
        itemArray[2] = memory.main.getItemCountSlot(index)

    # Silence Grenades
    index = memory.main.getItemSlot(39)
    if index == 255:
        itemArray[3] = 0
    elif memory.main.getItemCountSlot(index) == 1:
        itemArray[3] = 0  # Save one for NEA manip
    else:
        itemArray[3] = memory.main.getItemCountSlot(index)

    return itemArray


def sandragora(version):
    screen.awaitTurn()
    if version != 1:  # Kimahri's turn
        fleeAll()
        memory.main.clickToControl()
    else:  # Auron's turn
        # Manip for NE armor
        if memory.main.battleType() == 2:
            while memory.main.battleType() == 2:
                print("Ambushed, swapping out.")
                fleeAll()
                memory.main.clickToControl()
                FFXC.set_movement(0, 1)
                memory.main.awaitEvent()
                FFXC.set_neutral()
                screen.awaitTurn()
        # elif FX_memory.rngSeed() == 31:
        #    print("Manipulating known seed 31")
        #    fleeAll()
        #    memory.clickToControl()
        #    FFXC.set_movement(0, 1)
        #    memory.awaitEvent()
        #    FFXC.set_neutral()
        #    screen.awaitTurn()
        else:
            print("DO NOT Swap odd/even seeds on RNG01")

        tidusHaste('l', character=2)
        screen.awaitTurn()
        if screen.turnKimahri() or screen.turnRikku():
            print("Kimahri/Rikku taking a spare turn. Just defend.")
            defend()
            screen.awaitTurn()
        print("Setting up Auron overdrive")
        auronOD(style="shooting star")
        memory.main.clickToControl()


def home1():
    FFXC.set_neutral()
    xbox.clickToBattle()
    print("Tidus vs Bombs")
    tidusHaste('none')
    while memory.main.battleActive():  # AKA end of battle screen
        if memory.main.turnReady():
            if screen.faintCheck() > 0:
                revive()
            elif screen.turnTidus():
                attack('none')
            elif screen.turnAuron() and memory.main.getEnemyCurrentHP()[0] != 0:
                attack('none')
            else:
                defend()
    print("Home 1 shows as fight complete.")
    memory.main.clickToControl()


def home2():
    xbox.clickToBattle()

    print("Kimahri vs dual horns")
    while memory.main.battleActive():  # AKA end of battle screen
        if memory.main.turnReady():

            if screen.turnKimahri():
                kimahriOD(3)
            elif memory.main.getBattleCharSlot(3) >= 3:
                buddySwapKimahri()  # Tidus for Kimahri
                lancetHome('none')
            else:
                defend()
    print("Home 2 shows as fight complete.")
    FFXC.set_neutral()
    memory.main.clickToControl()


def home3():
    xbox.clickToBattle()
    if memory.main.getUseItemsSlot(49) > 200:
        tidusHaste('none')
    else:
        while not screen.turnRikku():
            defend()
            xbox.clickToBattle()
            useItem(memory.main.getUseItemsSlot(49), 'none')

    rikkuItemThrown = 0
    while not memory.main.battleComplete():  # AKA end of battle screen
        if memory.main.turnReady():
            print("- Turn:")
            if screen.turnTidus():
                print("  Tidus")
                if memory.main.getUseItemsSlot(49) != 255:
                    defend()
                else:
                    attack('none')
            elif screen.turnRikku() and rikkuItemThrown < 1 and home3item() != 255:
                print("  Rikku")
                useItemSlot = home3item()
                useItem(useItemSlot, 'none')
                rikkuItemThrown += 1
            elif screen.faintCheck() > 0:
                print("  any, revive")
                revive()
            else:
                print("  any, defend")
                defend()
    FFXC.set_neutral()
    print("Home 3 shows as fight complete.")


def home3item():
    throwSlot = memory.main.getUseItemsSlot(49)  # Petrify Grenade
    if throwSlot != 255:
        return throwSlot
    throwSlot = memory.main.getUseItemsSlot(40)  # Smoke Bomb
    if throwSlot != 255:
        return throwSlot
    throwSlot = memory.main.getUseItemsSlot(39)  # Silence - for the Guado-face.
    if throwSlot != 255:
        return throwSlot
    return 255


def home4():
    xbox.clickToBattle()

    print("Kimahri vs Chimera")
    while memory.main.battleActive():  # AKA end of battle screen
        if memory.main.turnReady():
            if screen.turnKimahri():
                kimahriOD(4)
            elif memory.main.getBattleCharSlot(3) >= 3:
                buddySwapKimahri()  # Tidus for Kimahri
                lancetHome('none')
            else:
                defend()
    print("Home 4 shows as fight complete.")
    memory.main.clickToControl()


# Process written by CrimsonInferno
def Evrae():
    tidusPrep = 0
    tidusAttacks = 0
    rikkuTurns = 0
    kimahriTurns = 0
    lunarCurtain = False
    if memory.main.rngSeed() == 31:
        stealCount = 2
    else:
        stealCount = 0
    FFXC.set_neutral()
    # This gets us past the tutorial and all the dialog.
    xbox.clickToBattle()

    while memory.main.battleActive():  # AKA end of battle screen
        if memory.main.turnReady():
            turnchar = memory.main.getBattleCharTurn()
            print("Tidus prep turns:", tidusPrep)
            if turnchar == 0:
                print("Registering Tidus' turn")
                if gameVars.skipKilikaLuck():
                    if tidusPrep == 0:
                        tidusPrep = 1
                        tidusHaste('none')
                    elif tidusPrep in [1, 2]:
                        tidusPrep += 1
                        cheer()
                    elif tidusAttacks == 4 or memory.main.getEnemyCurrentHP()[0] <= 9999:
                        tidusAttacks += 1
                        tidusOD()
                    else:
                        tidusAttacks += 1
                        attack('none')
                elif gameVars.getBlitzWin():  # Blitz win logic
                    if tidusPrep == 0:
                        tidusPrep = 1
                        tidusHaste('none')
                    elif tidusPrep == 1:
                        tidusPrep += 1
                        cheer()
                    elif tidusPrep == 2 and rikkuTurns == 0:
                        tidusPrep += 1
                        equipInBattle(equipType='armor', abilityNum=0x8028)
                    elif tidusPrep == 2 and tidusAttacks == 2:
                        tidusPrep += 1
                        cheer()
                    else:
                        tidusAttacks += 1
                        attack('none')
                else:  # Blitz loss logic
                    if tidusPrep == 0:
                        tidusPrep = 1
                        tidusHaste('none')
                    elif tidusPrep <= 2:
                        tidusPrep += 1
                        cheer()
                    elif tidusPrep == 3:
                        print("Equip Baroque Sword.")
                        equipInBattle(special='baroque')
                        tidusPrep += 1
                    elif tidusAttacks == 4 and gameVars.skipKilikaLuck():
                        tidusAttacks += 1
                        tidusOD()
                    else:
                        tidusAttacks += 1
                        attack('none')
            elif turnchar == 6:
                print("Registering Rikkus turn")
                if rikkuTurns == 0:
                    rikkuTurns += 1
                    print("Rikku overdrive")
                    rikkuFullOD('Evrae')
                elif not gameVars.getBlitzWin() and not lunarCurtain:
                    print("Use Lunar Curtain")
                    lunarSlot = memory.main.getUseItemsSlot(56)
                    useItem(lunarSlot, direction='l', target=0)
                    lunarCurtain = True
                elif memory.main.getBattleHP()[memory.main.getBattleCharSlot(0)] < 1520 and (tidusAttacks < 3 or not gameVars.getBlitzWin()):
                    print("Rikku should attempt to heal a character.")
                    kimahriTurns += 1
                    if fullheal(target=0,
                                direction="d") == 0:
                        print("Restorative item not found.")
                        useItem(memory.main.getUseItemsSlot(20))
                    else:
                        print("Heal should be successful.")
                elif gameVars.skipKilikaLuck():
                    if memory.main.getUseItemsSlot(32) != 255:
                        throwSlot = memory.main.getUseItemsSlot(32)
                    elif memory.main.getUseItemsSlot(24) != 255:
                        throwSlot = memory.main.getUseItemsSlot(24)
                    elif memory.main.getUseItemsSlot(27) != 255:
                        throwSlot = memory.main.getUseItemsSlot(27)
                    else:
                        throwSlot = memory.main.getUseItemsSlot(30)
                    if throwSlot == 255:
                        Steal()
                    else:
                        useItem(throwSlot)
                else:
                    Steal()
                    stealCount += 1
            elif turnchar == 3:
                print("Registering Kimahri's turn")
                if not gameVars.getBlitzWin() and not lunarCurtain:
                    print("Use Lunar Curtain")
                    lunarSlot = memory.main.getUseItemsSlot(56)
                    useItem(lunarSlot, direction='l', target=0)
                    lunarCurtain = True
                elif memory.main.getBattleHP()[memory.main.getBattleCharSlot(0)] < 1520 and (tidusAttacks < 3 or not gameVars.getBlitzWin()):
                    print("Kimahri should attempt to heal a character.")
                    kimahriTurns += 1
                    if fullheal(target=0,
                                direction="u") == 0:
                        print("Restorative item not found.")
                        useItem(memory.main.getUseItemsSlot(20))
                    else:
                        print("Heal should be successful.")
                elif gameVars.skipKilikaLuck():
                    if memory.main.getUseItemsSlot(32) != 255:
                        throwSlot = memory.main.getUseItemsSlot(32)
                    elif memory.main.getUseItemsSlot(24) != 255:
                        throwSlot = memory.main.getUseItemsSlot(24)
                    elif memory.main.getUseItemsSlot(27) != 255:
                        throwSlot = memory.main.getUseItemsSlot(27)
                    else:
                        throwSlot = memory.main.getUseItemsSlot(30)
                    if throwSlot == 255:
                        Steal()
                    else:
                        useItem(throwSlot)
                else:
                    Steal()
                    stealCount += 1
        elif memory.main.diagSkipPossible():
            xbox.tapB()

    if not gameVars.csr():
        while not memory.main.cutsceneSkipPossible():
            if memory.main.menuOpen():
                xbox.tapB()
        xbox.skipSceneSpec()


def guards(groupNum, sleepingPowders):
    xbox.clickToBattle()
    throw_distiller = memory.main.getItemSlot(
        16) != 255 or memory.main.getItemSlot(18) != 255
    num_throws = 0
    hasted = False
    tidusWent = False
    if sleepingPowders:  # We have sleeping powders
        while not memory.main.battleComplete():  # AKA end of battle screen
            if groupNum in [1, 3]:
                if screen.turnTidus():
                    attack('none')
                elif throw_distiller:
                    if memory.main.getItemSlot(18) != 255:
                        _useHealingItem(itemID=18)
                    else:
                        _useHealingItem(itemID=16)
                    throw_distiller = False
                elif 6 in memory.main.getActiveBattleFormation() and memory.main.getBattleHP()[memory.main.getBattleCharSlot(6)] <= 120 \
                        and memory.main.getBattleHP()[memory.main.getBattleCharSlot(6)] != 0:
                    if memory.main.getItemSlot(0) != 255:
                        usePotionCharacter(6, 'r')
                    elif memory.main.getItemSlot(1) != 255:
                        _useHealingItem(num=6, direction='r', itemID=1)
                    else:
                        defend()
                else:
                    defend()
            elif groupNum in [2, 4]:
                if screen.turnTidus():
                    attack('none')
                elif (screen.turnRikku() or screen.turnKimahri()) and num_throws < 2:
                    silenceSlot = memory.main.getItemSlot(39)
                    if num_throws == 0 and memory.main.getUseItemsSlot(37) < 200:
                        useItem(memory.main.getUseItemsSlot(37))
                    else:
                        if memory.main.getUseItemsSlot(40) != 255:
                            useItem(memory.main.getUseItemsSlot(40))
                        elif silenceSlot != 255 and memory.main.getItemCountSlot(silenceSlot) > 1:
                            # Save one for later if possible
                            useItem(memory.main.getUseItemsSlot(39))
                        elif memory.main.getUseItemsSlot(37) != 255:
                            useItem(memory.main.getUseItemsSlot(37))
                        elif memory.main.getUseItemsSlot(27) != 255:
                            useItem(memory.main.getUseItemsSlot(27))
                        elif silenceSlot != 255:
                            # Throw last Silence grenade as a last resort.
                            useItem(memory.main.getUseItemsSlot(39))
                        else:
                            defend()
                    num_throws += 1
                else:
                    defend()
            elif groupNum == 5:
                if screen.faintCheck():
                    revive()
                elif screen.turnTidus():
                    if not hasted:
                        tidusHaste('left', character=6)
                        hasted = True
                    else:
                        attackByNum(22, 'r')
                elif screen.turnRikku() or screen.turnKimahri():
                    silenceSlot = memory.main.getItemSlot(39)
                    if num_throws < 2:
                        if memory.main.getUseItemsSlot(40) != 255:
                            useItem(memory.main.getUseItemsSlot(40))
                        elif silenceSlot != 255 and memory.main.getItemCountSlot(silenceSlot) > 1:
                            # Save one for later if possible
                            useItem(memory.main.getUseItemsSlot(39))
                        elif memory.main.getUseItemsSlot(37) != 255:
                            useItem(memory.main.getUseItemsSlot(37))
                        elif memory.main.getUseItemsSlot(27) != 255:
                            useItem(memory.main.getUseItemsSlot(27))
                        elif memory.main.getUseItemsSlot(39) != 255:
                            useItem(memory.main.getUseItemsSlot(39))
                        else:
                            defend()
                        num_throws += 1
                    else:
                        defend()
    else:  # We do not have sleeping powders
        while not memory.main.battleComplete():
            if groupNum in [1, 3]:
                if screen.turnTidus():
                    attack('none')
                elif throw_distiller:
                    if memory.main.getItemSlot(18) != 255:
                        _useHealingItem(itemID=18)
                    else:
                        _useHealingItem(itemID=16)
                    throw_distiller = False
                elif 6 in memory.main.getActiveBattleFormation() and memory.main.getBattleHP()[memory.main.getBattleCharSlot(6)] <= 120 \
                        and memory.main.getBattleHP()[memory.main.getBattleCharSlot(6)] != 0:
                    if memory.main.getItemSlot(0) != 255:
                        usePotionCharacter(6, 'r')
                    elif memory.main.getItemSlot(1) != 255:
                        _useHealingItem(num=6, direction='r', itemID=1)
                    else:
                        defend()
                else:
                    defend()
            elif groupNum in [2, 4]:
                if screen.turnTidus():
                    if not tidusWent:
                        buddySwapKimahri()
                        tidusWent = True
                    else:
                        attack('none')
                elif screen.turnKimahri() or screen.turnRikku():
                    silenceSlot = memory.main.getItemSlot(39)
                    if memory.main.getUseItemsSlot(40) != 255:
                        useItem(memory.main.getUseItemsSlot(40))
                    elif silenceSlot != 255 and memory.main.getItemCountSlot(silenceSlot) >= 2:
                        # Save one for later if possible
                        useItem(memory.main.getUseItemsSlot(39))
                    elif memory.main.getUseItemsSlot(37) != 255:
                        useItem(memory.main.getUseItemsSlot(37))
                    elif memory.main.getUseItemsSlot(27) != 255:
                        useItem(memory.main.getUseItemsSlot(27))
                    elif memory.main.getUseItemsSlot(39) != 255:
                        useItem(memory.main.getUseItemsSlot(39))
                    else:
                        defend()
                else:
                    defend()
            elif groupNum == 5:
                if screen.turnTidus():
                    if not tidusWent:
                        buddySwapRikku()
                        tidusWent = True
                    else:
                        attackByNum(22, 'l')
                elif screen.turnRikku() or screen.turnKimahri():
                    silenceSlot = memory.main.getItemSlot(39)
                    if num_throws < 2:
                        if memory.main.getUseItemsSlot(40) != 255:
                            useItem(memory.main.getUseItemsSlot(40))
                        elif silenceSlot != 255 and memory.main.getItemCountSlot(silenceSlot) > 1:
                            # Save one for later if possible
                            useItem(memory.main.getUseItemsSlot(39))
                        elif memory.main.getUseItemsSlot(37) != 255:
                            useItem(memory.main.getUseItemsSlot(37))
                        elif memory.main.getUseItemsSlot(27) != 255:
                            useItem(memory.main.getUseItemsSlot(27))
                        elif memory.main.getUseItemsSlot(39) != 255 and num_throws < 2:
                            useItem(memory.main.getUseItemsSlot(39))
                        else:
                            defend()
                    else:
                        defend()
                    num_throws += 1
                elif screen.turnKimahri():
                    buddySwapTidus()
                else:
                    defend()


def isaaru():
    xbox.clickToBattle()
    if memory.main.getEncounterID() < 258:
        gameVars.addRescueCount()

    while memory.main.battleActive():  # AKA end of battle screen
        if memory.main.turnReady():
            if screen.turnYuna():
                if memory.main.getEncounterID() in [257, 260]:
                    aeonSummon(2)  # Summon Ixion for Bahamut
                else:
                    aeonSummon(4)  # Summon Bahamut for other aeons
            else:
                attack('none')  # Aeon turn
        elif memory.main.diagSkipPossible():
            xbox.tapB()
    FFXC.set_value('BtnB', 1)
    memory.main.waitFrames(30 * 2.8)
    FFXC.set_value('BtnB', 0)


def altanaheal():
    direction = 'd'
    if memory.main.getThrowItemsSlot(2) < 255:
        itemnum = 2
        itemname = "X-Potion"
    elif memory.main.getThrowItemsSlot(8) < 255:
        itemnum = 8
        itemname = "Elixir"
    elif memory.main.getThrowItemsSlot(6) < 255:
        itemnum = 6
        itemname = "Phoenix Down"
    elif memory.main.getThrowItemsSlot(7) < 255:
        itemnum = 7
        itemname = "Phoenix Down"
    else:
        itemnum = -1
        itemname = "noitemfound"
    if itemnum >= 0:
        print("Using %s" % itemname)
        while not memory.main.turnReady():
            pass
        while memory.main.mainBattleMenu():
            if memory.main.battleMenuCursor() != 1:
                xbox.tapDown()
            else:
                xbox.tapB()
        while memory.main.mainBattleMenu():
            xbox.tapB()
        itemPos = memory.main.getThrowItemsSlot(itemnum)
        print("Position:", itemPos)
        _navigate_to_position(itemPos)
        while memory.main.otherBattleMenu():
            xbox.tapB()
        print("Direction:", direction)
        while not memory.main.targetingEnemy():
            if direction == 'l':
                xbox.tapLeft()
                if not memory.main.targetingEnemy():
                    print("Wrong battle line targeted.")
                    xbox.tapRight()
                    direction = 'u'
            elif direction == 'r':
                xbox.tapRight()
                if not memory.main.targetingEnemy():
                    print("Wrong battle line targeted.")
                    xbox.tapLeft()
                    direction = 'd'
            elif direction == 'u':
                xbox.tapUp()
                if not memory.main.targetingEnemy():
                    print("Wrong battle line targeted.")
                    xbox.tapDown()
                    direction = 'l'
            elif direction == 'd':
                xbox.tapDown()
                if not memory.main.targetingEnemy():
                    print("Wrong battle line targeted.")
                    xbox.tapUp()
                    direction = 'r'
        tapTargeting()
        return 1

    else:
        print("No restorative items available")
        return 0


def evraeAltana():
    xbox.clickToBattle()
    if memory.main.getEncounterID() == 266:
        print("Evrae Altana fight start")
        thrownItem = False
        while memory.main.battleActive():  # AKA end of battle screen
            if memory.main.turnReady():
                if memory.main.getItemSlot(18) != 255 and not thrownItem:
                    _useHealingItem(itemID=18)
                    thrownItem = True
                elif memory.main.getItemSlot(16) != 255 and not thrownItem:
                    _useHealingItem(itemID=16)
                    thrownItem = True
                else:
                    altanaheal()

    else:  # Just a regular group
        print("Not Evrae this time.")
        fleeAll()

    memory.main.clickToControl()


def attackHighbridge():
    if memory.main.getEncounterID() == 270:
        attackByNum(22, 'r')
    elif memory.main.getEncounterID() == 271:
        attackByNum(21, 'l')
    else:
        attack('none')


def seymourNatus():
    aeonSummoned = False
    while not memory.main.userControl():
        if memory.main.getEncounterID() == 272:  # Seymour Natus
            print("Seymour Natus engaged")
            while not memory.main.battleComplete():
                if memory.main.turnReady():
                    if screen.turnTidus():
                        if memory.main.getLuluSlvl() < 35 or gameVars.nemesis():
                            buddySwapLulu()
                            screen.awaitTurn()
                            xbox.weapSwap(0)
                        elif aeonSummoned:
                            tidusHaste('d', character=1)
                        else:
                            attack('none')
                    elif screen.turnLulu():
                        buddySwapTidus()
                        screen.awaitTurn()
                        xbox.tapUp()
                        attack('none')
                    elif screen.turnYuna():
                        if not aeonSummoned:
                            aeonSummon(4)
                            aeonSummoned = True
                        else:
                            aeonSummon(2)
                    elif screen.turnAeon():
                        xbox.SkipDialog(3)  # Finishes the fight.
                    else:
                        defend()
            return 1
        elif memory.main.getEncounterID() == 270:  # YAT-63 x2
            while memory.main.battleActive():
                if gameVars.completedRescueFights():
                    fleeAll()
                elif memory.main.turnReady():
                    if screen.turnTidus() or screen.turnYuna():
                        if memory.main.getEnemyCurrentHP().count(0) == 1:
                            fleeAll()
                            gameVars.addRescueCount()
                        else:
                            attackByNum(22, 'r')
                    else:
                        defend()
        elif memory.main.getEncounterID() == 269:  # YAT-63 with two guard guys
            while memory.main.battleActive():
                if gameVars.completedRescueFights():
                    fleeAll()
                elif memory.main.turnReady():
                    if screen.turnTidus() or screen.turnYuna():
                        if memory.main.getEnemyCurrentHP().count(0) == 1:
                            fleeAll()
                            gameVars.addRescueCount()
                        else:
                            attack('none')
                    else:
                        defend()
        elif memory.main.getEncounterID() == 271:  # one YAT-63, two YAT-99
            while memory.main.battleActive():
                if gameVars.completedRescueFights():
                    fleeAll()
                elif memory.main.turnReady():
                    if screen.turnTidus() or screen.turnYuna():
                        if memory.main.getEnemyCurrentHP().count(0) == 1:
                            fleeAll()
                            gameVars.addRescueCount()
                        else:
                            attackByNum(21, 'l')
                    else:
                        defend()
        if memory.main.menuOpen() or memory.main.diagSkipPossible():
            xbox.tapB()
    return 0


def calmLandsGems():
    while not memory.main.turnReady():
        pass
    stealComplete = False
    if not memory.main.getEncounterID() in [273, 275, 281, 283]:
        fleeAll()
    else:
        while memory.main.battleActive():
            if memory.main.turnReady():
                if 3 not in memory.main.getActiveBattleFormation():
                    buddySwapKimahri()
                elif stealComplete:
                    fleeAll()
                elif screen.turnKimahri():
                    # Red element in center slot, with machina and dog
                    if memory.main.getEncounterID() == [273, 281]:
                        print("Grabbing a gem here.")
                        buddySwapKimahri()
                        StealLeft()
                    # Red element in top slot, with bee and tank
                    elif memory.main.getEncounterID() in [275, 283]:
                        print("Grabbing a gem here.")
                        buddySwapKimahri()
                        StealDown()
                    else:
                        defend()
                    stealComplete = True
                else:
                    defend()
    memory.main.clickToControl()


def gagazetPath():
    while not memory.main.turnReady():
        pass
    if memory.main.getEncounterID() == 337:
        while memory.main.battleActive():
            if memory.main.turnReady():
                if screen.turnRikku():
                    StealRight()
                else:
                    escapeOne()
    else:
        fleeAll()


def biranYenke():
    xbox.clickToBattle()
    Steal()

    # Nemesis logic
    if gameVars.nemesis():
        screen.awaitTurn()
        StealRight()

    screen.awaitTurn()
    gemSlot = memory.main.getUseItemsSlot(34)
    if gemSlot == 255:
        gemSlot = memory.main.getUseItemsSlot(28)
    useItem(gemSlot, 'none')

    xbox.clickToBattle()
    gemSlot = memory.main.getUseItemsSlot(34)
    if gemSlot == 255:
        gemSlot = memory.main.getUseItemsSlot(28)
    useItem(gemSlot, 'none')

    while not memory.main.userControl():
        xbox.tapB()

    retSlot = memory.main.getItemSlot(96)  # Return sphere
    friendSlot = memory.main.getItemSlot(97)  # Friend sphere

    if friendSlot == 255:  # Four return sphere method.
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
    yunaXP = memory.main.getSLVLYuna()
    xbox.clickToBattle()
    if gameVars.endGameVersion() == 3:
        bahamutSummoned = False
        while not memory.main.battleComplete():  # AKA end of battle screen
            if memory.main.turnReady():
                if screen.turnTidus():
                    buddySwapYuna()
                elif screen.turnYuna():
                    if not bahamutSummoned:
                        aeonSummon(4)
                        bahamutSummoned = True
                    else:
                        attack('none')
                elif screen.turnAeon():
                    if gameVars.getBlitzWin():
                        attack('none')
                    else:
                        impulse()
                elif screen.faintCheck() >= 1:
                    revive()
                else:
                    defend()
    else:
        while not memory.main.battleComplete():  # AKA end of battle screen
            if memory.main.turnReady():
                lastHP = memory.main.getEnemyCurrentHP()[0]
                print("Last HP")
                if screen.turnYuna():
                    print("Yunas turn. Stage:", stage)
                    if stage == 1:
                        attack('none')
                        stage += 1
                    elif stage == 2:
                        aeonSummon(4)
                        attack('none')
                        stage += 1
                    else:
                        attack('none')
                elif screen.turnTidus():
                    print("Tidus' turn. Stage:", stage)
                    if stage < 3:
                        tidusHaste('down', character=1)
                    elif lastHP > 3500:
                        attack('none')
                    else:
                        defend()
                elif screen.turnAuron():
                    print("Auron's turn. Swap for Rikku and overdrive.")
                    buddySwapRikku()
                    print("Rikku overdrive")
                    rikkuFullOD('Flux')
                else:
                    print("Non-critical turn. Defending.")
                    defend()
            elif memory.main.diagSkipPossible():
                xbox.tapB()
    memory.main.clickToControl()
    if memory.main.getSLVLYuna() - yunaXP == 15000:
        gameVars.fluxOverkillSuccess()
    print("------------------------------")
    print("Flux Overkill:", gameVars.fluxOverkill())
    print("Seymour Flux battle complete.")
    print("------------------------------")
    # time.sleep(60) #Testing only


def sKeeper():
    xbox.clickToBattle()
    print("Start of Sanctuary Keeper fight")
    if gameVars.endGameVersion() == 3 and gameVars.getBlitzWin():
        while not memory.main.battleComplete():
            if memory.main.turnReady():
                if screen.turnYuna():
                    aeonSummon(4)
                elif screen.turnAeon():
                    attack('none')
                else:
                    defend()
    else:
        armorBreak = False
        while not memory.main.battleComplete():
            if memory.main.turnReady():
                if screen.turnTidus():
                    useSkill(0)
                    armorBreak = True
                elif screen.turnYuna():
                    if armorBreak:
                        aeonSummon(4)
                    else:
                        defend()
                elif screen.turnAeon():
                    attack('none')
                else:
                    defend()
    memory.main.clickToControl()


def caveChargeRikku():
    while not memory.main.turnReady():
        pass
    while memory.main.battleActive():
        if memory.main.turnReady():
            if screen.turnRikku():
                attack('none')
            else:
                escapeOne()
    memory.main.clickToControl()


def gagazetCave(direction):
    screen.awaitTurn()
    attack(direction)
    fleeAll()


def _navigate_to_position(position, battleCursor=memory.main.battleCursor2):
    while battleCursor() == 255:
        pass
    if battleCursor() != position:
        print("Wrong position targeted", battleCursor() % 2, position % 2)
        while battleCursor() % 2 != position % 2:
            if battleCursor() < position:
                xbox.tapRight()
            else:
                xbox.tapLeft()
        while battleCursor() != position:
            print(battleCursor())
            if battleCursor() > position:
                xbox.tapUp()
            else:
                xbox.tapDown()


def useItem(slot: int, direction='none', target=255, rikkuFlee=False):
    print("Using items via the Use command")
    print("Item slot:", slot)
    print("Direction:", direction)
    while not memory.main.mainBattleMenu():
        pass
    print("Mark 1, turn is active.")
    while memory.main.battleMenuCursor() != 20:
        if not screen.turnRikku() and not screen.turnKimahri():
            return
        if memory.main.battleMenuCursor() in [0, 19]:
            xbox.tapDown()
        elif memory.main.battleMenuCursor() == 1:
            xbox.tapUp()
        elif memory.main.battleMenuCursor() > 20:
            xbox.tapUp()
        else:
            xbox.tapDown()
    if gameVars.usePause():
        memory.main.waitFrames(3)
    while memory.main.mainBattleMenu():
        xbox.tapB()
    if rikkuFlee:
        print("Mark 2, selecting 'Use' command in position", 2)
    else:
        print("Mark 2, selecting 'Use' command in position", 1)
    if rikkuFlee:
        _navigate_to_position(2)
    else:
        _navigate_to_position(1)
    if gameVars.usePause():
        memory.main.waitFrames(3)
    while memory.main.otherBattleMenu():
        xbox.tapB()
    print("Mark 3, navigating to item slot")
    _navigate_to_position(slot, memory.main.battleCursor3)
    if gameVars.usePause():
        memory.main.waitFrames(3)
    while memory.main.interiorBattleMenu():
        xbox.tapB()
    if target != 255:
        try:
            print("Targetting based on character number")
            if target >= 20 and memory.main.getEnemyCurrentHP()[target - 20] != 0:
                direction = 'l'
                while memory.main.battleTargetId() != target:
                    if memory.main.battleTargetId() < 20:
                        xbox.tapRight()
                        direction = 'u'
                    elif direction == 'u':
                        xbox.tapUp()
                    else:
                        xbox.tapLeft()
            elif target < 20 and target != 0:
                direction = 'l'
                while memory.main.battleTargetId() != target:
                    if memory.main.battleTargetId() >= 20:
                        xbox.tapRight()
                        direction = 'u'
                    elif direction == 'u':
                        xbox.tapUp()
                    else:
                        xbox.tapLeft()
            elif target == 0:
                direction = 'l'
                while memory.main.battleTargetId() != 0:
                    if memory.main.battleTargetId() >= 20:
                        xbox.tapRight()
                        direction = 'u'
                    elif direction == 'u':
                        xbox.tapUp()
                    else:
                        xbox.tapLeft()

            tapTargeting()
        except Exception:
            xbox.tapB()
            xbox.tapB()
            xbox.tapB()
            xbox.tapB()
            xbox.tapB()
            xbox.tapB()
    elif direction == 'none':
        print("No direction variation")
        tapTargeting()
    else:
        print("Direction variation:", direction)
        if direction == 'left':
            xbox.tapLeft()
        elif direction == 'right':
            xbox.tapRight()
        elif direction == 'up':
            xbox.tapUp()
        elif direction == 'down':
            xbox.tapDown()
        tapTargeting()


def useItemTidus(slot: int, direction='none', target=255):
    print("Using items via the Use command")
    print("Item slot:", slot)
    print("Direction:", direction)
    while not memory.main.mainBattleMenu():
        pass
    print("Mark 1")
    while memory.main.battleMenuCursor() != 20:
        if not screen.turnTidus():
            return
        if memory.main.battleMenuCursor() == 1:
            xbox.tapUp()
        elif memory.main.battleMenuCursor() > 20:
            xbox.tapUp()
        else:
            xbox.tapDown()
    if gameVars.usePause():
        memory.main.waitFrames(3)
    while memory.main.mainBattleMenu():
        xbox.tapB()
    if gameVars.usePause():
        memory.main.waitFrames(3)
    print("Mark 2")
    _navigate_to_position(2)
    while memory.main.otherBattleMenu():
        xbox.tapB()
    if gameVars.usePause():
        memory.main.waitFrames(3)
    print("Mark 3")
    _navigate_to_position(slot, memory.main.battleCursor3)
    if gameVars.usePause():
        memory.main.waitFrames(3)
    while memory.main.interiorBattleMenu():
        xbox.tapB()
    if target != 255:
        try:
            print("Targetting based on character number")
            if target >= 20 and memory.main.getEnemyCurrentHP()[target - 20] != 0:
                direction = 'l'
                while memory.main.battleTargetId() != target:
                    if memory.main.battleTargetId() < 20:
                        xbox.tapRight()
                        direction = 'u'
                    elif direction == 'u':
                        xbox.tapUp()
                    else:
                        xbox.tapLeft()
            elif target < 20 and target != 0:
                direction = 'l'
                while memory.main.battleTargetId() != target:
                    if memory.main.battleTargetId() >= 20:
                        xbox.tapRight()
                        direction = 'u'
                    elif direction == 'u':
                        xbox.tapUp()
                    else:
                        xbox.tapLeft()
            elif target == 0:
                direction = 'l'
                while memory.main.battleTargetId() != 0:
                    if memory.main.battleTargetId() >= 20:
                        xbox.tapRight()
                        direction = 'u'
                    elif direction == 'u':
                        xbox.tapUp()
                    else:
                        xbox.tapLeft()

            tapTargeting()
        except Exception:
            xbox.tapB()
            xbox.tapB()
            xbox.tapB()
            xbox.tapB()
            xbox.tapB()
            xbox.tapB()
    elif direction == 'none':
        print("No direction variation")
        tapTargeting()
    else:
        print("Direction variation:", direction)
        if direction == 'left':
            xbox.tapLeft()
        elif direction == 'right':
            xbox.tapRight()
        elif direction == 'up':
            xbox.tapUp()
        elif direction == 'down':
            xbox.tapDown()
        tapTargeting()


def cheer():
    print("Cheer command")
    while memory.main.battleMenuCursor() != 20:
        if not screen.turnTidus():
            return
        if memory.main.battleMenuCursor() == 0:
            xbox.tapDown()
        else:
            xbox.tapUp()
    while not memory.main.otherBattleMenu():
        xbox.tapB()
    _navigate_to_position(1)
    while memory.main.otherBattleMenu():
        xbox.tapB()
    tapTargeting()


def seymourSpell(targetFace=True):
    print("Seymour casting tier 2 spell")
    num = 21  # Should be the enemy number for the head
    if not memory.main.turnReady():
        print("Battle menu isn't up.")
        screen.awaitTurn()

    while memory.main.battleMenuCursor() != 21:
        print(memory.main.battleMenuCursor())
        if memory.main.battleMenuCursor() == 0:
            xbox.tapDown()
        else:
            xbox.tapUp()
    while memory.main.mainBattleMenu():
        xbox.tapB()  # Black magic
    print(memory.main.battleCursor2())
    _navigate_to_position(5)
    while memory.main.otherBattleMenu():
        xbox.tapB()

    if targetFace and memory.main.getEnemyCurrentHP()[1] != 0:  # Target head if alive.
        while memory.main.battleTargetId() != num:
            xbox.tapLeft()

    tapTargeting()


def _useHealingItem(num=None, direction='l', itemID=0):
    print("Healing character, ", num)
    direction = direction.lower()
    while not memory.main.turnReady():
        print("Battle menu isn't up.")
        pass
    while not memory.main.mainBattleMenu():
        pass
    while memory.main.battleMenuCursor() != 1:
        xbox.tapDown()
    while memory.main.mainBattleMenu():
        xbox.tapB()
    while not memory.main.otherBattleMenu():
        pass
    print(memory.main.battleCursor2())
    print(memory.main.getThrowItemsSlot(itemID))
    _navigate_to_position(memory.main.getThrowItemsSlot(itemID))
    while memory.main.otherBattleMenu():
        xbox.tapB()
    if num is not None:
        while memory.main.battleTargetId() != num:
            if direction == 'l':
                if memory.main.battleTargetId() >= 20:
                    print("Wrong battle line targeted.")
                    xbox.tapRight()
                    direction = 'u'
                else:
                    xbox.tapLeft()
            elif direction == 'r':
                if memory.main.battleTargetId() >= 20:
                    print("Wrong character targeted.")
                    xbox.tapLeft()
                    direction = 'd'
                else:
                    xbox.tapRight()
            elif direction == 'u':
                if memory.main.battleTargetId() >= 20:
                    print("Wrong character targeted.")
                    xbox.tapDown()
                    direction = 'l'
                else:
                    xbox.tapUp()
            elif direction == 'd':
                if memory.main.battleTargetId() >= 20:
                    print("Wrong character targeted.")
                    xbox.tapUp()
                    direction = 'r'
                else:
                    xbox.tapDown()
    tapTargeting()


def usePotionCharacter(num, direction):
    print("Healing character, ", num)
    _useHealingItem(num=num, direction=direction, itemID=0)


def attackByNum(num, direction='u'):
    if num < 20:
        friendlyTarget = True
    else:
        friendlyTarget = False
    print("Attacking specific character, ", num)
    direction = direction.lower()
    if not memory.main.turnReady():
        print("Battle menu isn't up.")
        while not memory.main.turnReady():
            # Waiting for battle menu to come up.
            pass
        # Make sure we actually have control
    if memory.main.battleMenuCursor() != 0 and memory.main.battleMenuCursor() != 216:
        while not memory.main.battleMenuCursor() in [0, 216]:
            xbox.tapUp()
            if screen.BattleComplete():
                return  # Safety
    while memory.main.mainBattleMenu():
        xbox.tapB()

    if not friendlyTarget and memory.main.getEnemyCurrentHP()[num - 20] != 0:
        while memory.main.battleTargetId() != num:
            if direction == 'l':
                if memory.main.battleTargetId() < 20:
                    direction = 'u'
                xbox.tapLeft()
            elif direction == 'r':
                if memory.main.battleTargetId() < 20:
                    direction = 'd'
                xbox.tapRight()
            elif direction == 'u':
                if memory.main.battleTargetId() < 20:
                    direction = 'l'
                xbox.tapUp()
            elif direction == 'd':
                if memory.main.battleTargetId() < 20:
                    direction = 'r'
                xbox.tapDown()
    elif friendlyTarget:
        while memory.main.battleTargetId() != num:
            if direction == 'l':
                if memory.main.battleTargetId() >= 20:
                    direction = 'u'
                xbox.tapLeft()
            elif direction == 'r':
                if memory.main.battleTargetId() >= 20:
                    direction = 'd'
                xbox.tapRight()
            elif direction == 'u':
                if memory.main.battleTargetId() >= 20:
                    direction = 'l'
                xbox.tapUp()
            elif direction == 'd':
                if memory.main.battleTargetId() >= 20:
                    direction = 'r'
                xbox.tapDown()
    tapTargeting()


def attackSelfTanker():
    print("Attacking specific character, Auron (self)")
    if not memory.main.turnReady():
        print("Battle menu isn't up.")
        while not memory.main.turnReady():
            # Waiting for battle menu to come up.
            pass
    if memory.main.battleMenuCursor() != 0 and memory.main.battleMenuCursor() != 216:
        while not memory.main.battleMenuCursor() in [0, 216]:
            xbox.tapUp()
            if screen.BattleComplete():
                return  # Safety
    while memory.main.mainBattleMenu():
        xbox.tapB()
    while memory.main.battleTargetId() != 2:
        if memory.main.battleTargetId() > 20:
            xbox.tapDown()
        else:
            xbox.tapLeft()
    tapTargeting()


def oblitzRngWait():
    rngValues = rngTrack.oblitzHistory()
    print(rngValues)
    lastRNG = memory.main.rngFromIndex(index=2)
    comingSeeds = memory.main.rngArrayFromIndex(index=2, arrayLen=15)
    seedNum = str(memory.main.rngSeed())
    print(comingSeeds)
    pos = 0
    countUnknowns = 0
    countKnowns = 0

    if seedNum not in rngValues:
        print("## No values for this RNG seed")
        firstResult = [comingSeeds[1], 9999, True, 1]
        secondResult = [comingSeeds[2], 9999, True, 2]
    else:
        print("## Scanning values for this RNG seed")
        if gameVars.loopBlitz():  # This will cause us to prefer results hunting
            print("### Looping on blitz, we will try a new value.")
            # Seed value, time to completion, Win/Loss, and position
            firstResult = [0, 10, True, 0]
            secondResult = [0, 10, True, 0]
        else:  # For full runs, take the best result.
            print("### This is a full run. Selecting best known result.")
            firstResult = [0, 9999, False, 0]
            secondResult = [0, 9999, False, 0]
        for i in range(len(comingSeeds)):
            print("Checking seed ", comingSeeds[i])
            # Set up duration and victory values
            if str(comingSeeds[i]) in rngValues[seedNum]:
                duration = int(rngValues[seedNum][str(comingSeeds[i])]['duration']) + pos
                print(duration)
                victory = bool(rngValues[seedNum][str(comingSeeds[i])]['victory'])
                print("Found result: ", [comingSeeds[i], duration, victory, pos])
                print(victory)
                countKnowns += 1
            elif gameVars.loopBlitz():
                print("No result, registering a preferred result while looping on Blitzball.")
                duration = 1 + pos
                victory = True
                countUnknowns += 1
            else:
                print("No result, registering an unknown result while attempting full run.")
                duration = 999 + pos
                victory = False
            #Fill as first two RNG values, then test against previously set RNG values until we've exhausted tests.
            if i == 0:
                pass
            elif firstResult[2] and not secondResult[2]:
                if duration < secondResult[1] and victory == True:
                    secondResult = [comingSeeds[i], duration, victory, pos]
                    print("Better Result for Second: ", pos, " - A")
                else:
                    print("Result for ", pos, " is not as good. - A")
            elif secondResult[2] and not firstResult[2]:
                if duration < firstResult[1] and victory == True:
                    firstResult = [comingSeeds[i], duration, victory, pos]
                    print("Better Result for First: ", pos, " - B")
                else:
                    print("Result for ", pos, " is not as good. - B")
            elif secondResult[1] < firstResult[1]:
                if duration < secondResult[1] and victory == True:
                    secondResult = [comingSeeds[i], duration, victory, pos]
                    print("Better Result for Second: ", pos, " - C")
                else:
                    print("Result for ", pos, " is not as good. - C")
            else:
                if duration < firstResult[1] and victory == True:
                    firstResult = [comingSeeds[i], duration, victory, pos]
                    print("Better Result for First: ", pos, " - D")
                else:
                    print("Result for ", pos, " is not as good. - D")
            pos += 1
    if countKnowns == 0 and not gameVars.loopBlitz():
        print("Could not find a known result.")
        best = secondResult
        best[0] = comingSeeds[1]
    elif countUnknowns == 0 and gameVars.loopBlitz():
        print("all values are known. Choosing a random value to test.")
        best = secondResult
        best[0] = comingSeeds[random(range(14))+1]
    elif firstResult[2] == 9999 and secondResult[2] != 9999:
        best=secondResult
    elif secondResult[2] == 9999 and firstResult[2] != 9999:
        best=firstResult
    elif firstResult[1] > secondResult[1]:
        best = secondResult
    else:
        best = firstResult
    logs.writeStats("Chosen Blitzball result:")
    logs.writeStats(best)
    
    nextRNG = lastRNG
    j = 0
    print("====================================")
    print("Desired results (RNG, duration, victory, waits):")
    print(best)
    print("====================================")
    # Now wait for one of the two results to come up
    while s32(nextRNG) != s32(best[0]) and j < 15:
        nextRNG = memory.main.rngFromIndex(index=2)
        if lastRNG != nextRNG:
            print(j, " | ", s32(nextRNG), " | ", s32(memory.main.rngFromIndex(index=2)), " | ", s32(best[0]))
            j += 1
            lastRNG = nextRNG
    print("====================================")
    print("Success. Attacking. ", j, " | ", nextRNG)
    gameVars.setOblitzRNG(value=nextRNG)
    return nextRNG


def attackOblitzEnd():
    print("Attack")
    if not memory.main.turnReady():
        while not memory.main.turnReady():
            pass
    while memory.main.mainBattleMenu():
        if not memory.main.battleMenuCursor() in [0, 203, 210, 216]:
            print(memory.main.battleMenuCursor(), ", Battle Menu Cursor")
            xbox.tapUp()
        elif screen.BattleComplete():
            return
        else:
            xbox.menuB()
    memory.main.waitFrames(1)
    rngWaitResults = oblitzRngWait()
    xbox.tapB()
    xbox.tapB()
    # logs.writeStats("RNG02 on attack:")
    # logs.writeStats(memory.s32(rngWaitResults))


def attack(direction="none"):
    print("Attack")
    direction = direction.lower()
    if not memory.main.turnReady():
        while not memory.main.turnReady():
            pass
    while memory.main.mainBattleMenu():
        if not memory.main.battleMenuCursor() in [0, 203, 210, 216]:
            print("Battle Menu Cursor:", memory.main.battleMenuCursor())
            xbox.tapUp()
        elif screen.BattleComplete():
            return
        else:
            xbox.tapB()
    if direction == "left":
        xbox.tapLeft()
    if direction == "right":
        xbox.tapRight()
    if direction == "r2":
        xbox.tapRight()
        xbox.tapRight()
    if direction == "r3":
        xbox.tapRight()
        xbox.tapRight()
        xbox.tapRight()
    if direction == "up":
        xbox.tapUp()
    if direction == "down":
        xbox.tapDown()
    tapTargeting()


def _steal(direction=None):
    if not memory.main.mainBattleMenu():
        while not memory.main.mainBattleMenu():
            pass
    while memory.main.battleMenuCursor() != 20:
        if not screen.turnRikku() and not screen.turnKimahri():
            return
        if memory.main.battleMenuCursor() == 1:
            xbox.tapUp()
        elif memory.main.battleMenuCursor() > 20:
            xbox.tapUp()
        else:
            xbox.tapDown()
    while not memory.main.otherBattleMenu():
        xbox.tapB()
    _navigate_to_position(0)
    print(memory.main.otherBattleMenu())
    while memory.main.otherBattleMenu():
        xbox.tapB()  # Use the Steal
    print(memory.main.otherBattleMenu())
    if direction == 'down':
        xbox.tapDown()
    elif direction == 'up':
        xbox.tapUp()
    elif direction == 'right':
        xbox.tapRight()
    elif direction == 'left':
        xbox.tapLeft()
    print("Firing steal")
    tapTargeting()


def Steal():
    print("Steal")
    if not memory.main.getEncounterID() in [273, 274, 276, 279, 281, 282, 284, 289]:
        _steal()
    elif memory.main.getEncounterID() in [273, 281]:
        _steal('left')
    elif memory.main.getEncounterID() in [276, 279, 289]:
        _steal('up')
    else:
        _steal()


def StealDown():
    print("Steal Down")
    _steal('down')


def StealUp():
    print("Steal Up")
    _steal('up')


def StealRight():
    print("Steal Right")
    _steal('right')


def StealLeft():
    print("Steal Left")
    _steal('left')


def stealAndAttack():
    print("Steal/Attack function")
    FFXC.set_neutral()
    screen.awaitTurn()
    while not memory.main.battleComplete():
        if memory.main.turnReady():
            if screen.turnRikku():
                grenadeSlot = memory.main.getItemSlot(35)
                grenadeCount = memory.main.getItemCountSlot(grenadeSlot)
                if grenadeCount < 5:
                    Steal()
                else:
                    attack('none')
            if screen.turnTidus():
                attack('none')
        elif memory.main.otherBattleMenu():
            xbox.tapB()
    memory.main.clickToControl()


def stealAndAttackPreTros():
    print("Steal/Attack function before Tros")
    turnCounter = 0
    advances = getAdvances(tros=False)
    FFXC.set_neutral()
    while not memory.main.battleComplete():
        if memory.main.turnReady():
            if screen.turnRikku():
                turnCounter += 1
                if turnCounter == 1:
                    grenadeSlot = memory.main.getItemSlot(35)
                    grenadeCount = memory.main.getItemCountSlot(grenadeSlot)
                    if grenadeCount < 5:
                        Steal()
                    elif advances in [1, 2]:
                        Steal()
                        advances = getAdvances(tros=False)
                    else:
                        attack('none')
                elif turnCounter == 2:
                    grenadeSlot = memory.main.getItemSlot(35)
                    grenadeCount = memory.main.getItemCountSlot(grenadeSlot)
                    if grenadeCount < 6:
                        Steal()
                    elif advances in [1, 2]:
                        Steal()
                        advances = getAdvances(tros=False)
                    else:
                        attack('none')
                else:
                    attack('none')
            if screen.turnTidus():
                attack('none')
        elif memory.main.otherBattleMenu():
            xbox.tapB()
    memory.main.clickToControl()


def castSpell(direction, spellID):
    if not screen.turnLulu():
        print("Lulu is not the current person. Deferring turn.")
        return
    while memory.main.battleMenuCursor() != 21:
        print(memory.main.battleMenuCursor())
        if memory.main.battleMenuCursor() == 0:
            xbox.tapDown()
        else:
            xbox.tapUp()
    while memory.main.mainBattleMenu():
        xbox.tapB()  # Black magic
    _navigate_to_position(spellID)
    while memory.main.otherBattleMenu():
        xbox.tapB()  # Cast the Spell
    direction = direction.lower()
    if direction == "right":
        xbox.tapRight()
    elif direction == "left":
        xbox.tapLeft()
    elif direction == "up":
        xbox.tapUp()
    elif direction == "down":
        xbox.tapDown()
    elif direction == "l2":
        xbox.tapLeft()
        xbox.tapLeft()
    elif direction == "rd":
        xbox.tapRight()
        xbox.tapDown()
    elif direction == "right2" or direction == "r2":
        xbox.tapRight()
        xbox.tapRight()
        xbox.tapDown()
    elif direction == "d2":
        xbox.tapDown()
        xbox.tapDown()
    elif not direction or direction == 'none':
        pass
    else:
        print("UNSURE DIRECTION:", direction)
        raise ValueError("Unsure direction")
    tapTargeting()


def thunder(direction="none"):
    print("Black magic - Thunder")
    castSpell(direction, 1)


def fire(direction="none"):
    print("Black magic - Fire")
    castSpell(direction, 0)


def water(direction="none"):
    print("Black magic - Water")
    castSpell(direction, 2)


def ice(direction="none"):
    print("Black magic - Ice")
    castSpell(direction, 3)


def thunderTarget(target, direction):
    print("Black magic - Thunder")
    if not screen.turnLulu():
        print("Lulu is not the current person. Deferring turn.")
        return
    direction = direction.lower()
    while memory.main.mainBattleMenu():
        if memory.main.battleMenuCursor() != 21:
            print(memory.main.battleMenuCursor())
            if memory.main.battleMenuCursor() == 0:
                xbox.tapDown()
            else:
                xbox.tapUp()
        else:
            xbox.tapB()
    print(memory.main.battleCursor2())
    _navigate_to_position(1)
    while memory.main.otherBattleMenu():
        xbox.tapB()  # Thunder
    while memory.main.battleTargetId() != target:
        if direction == 'l':
            if memory.main.battleTargetId() < 20:
                print("Wrong battle line targeted.")
                xbox.tapRight()
                direction = 'u'
            else:
                xbox.tapLeft()
        elif direction == 'r':
            if memory.main.battleTargetId() < 20:
                print("Wrong character targeted.")
                xbox.tapLeft()
                direction = 'd'
            else:
                xbox.tapRight()
        elif direction == 'u':
            if memory.main.battleTargetId() < 20:
                print("Wrong character targeted.")
                xbox.tapDown()
                direction = 'l'
            else:
                xbox.tapUp()
        elif direction == 'd':
            if memory.main.battleTargetId() < 20:
                print("Wrong character targeted.")
                xbox.tapUp()
                direction = 'r'
            else:
                xbox.tapDown()
    tapTargeting()


def aeonSummon(position):
    print("Summoning Aeon" + str(position))
    while not memory.main.mainBattleMenu():
        pass
    while memory.main.battleMenuCursor() != 23:
        if not screen.turnYuna():
            return
        if memory.main.battleMenuCursor() == 255:
            pass
        elif memory.main.battleMenuCursor() >= 1 and memory.main.battleMenuCursor() < 23:
            xbox.tapUp()
        else:
            xbox.tapDown()
    while memory.main.mainBattleMenu():
        xbox.tapB()
    while position != memory.main.battleCursor2():
        print(memory.main.battleCursor2())
        if memory.main.battleCursor2() < position:
            xbox.tapDown()
        else:
            xbox.tapUp()
    while memory.main.otherBattleMenu():
        xbox.tapB()
    aeonWaitTimer = 0
    while not memory.main.turnReady():
        if aeonWaitTimer % 10000 == 0:
            print("Waiting for Aeon's turn.", int(aeonWaitTimer % 10000))
        pass
        aeonWaitTimer += 1


def aeonSpell(position):
    aeonSpellDirection(position, None)


def aeonSpell2(position, direction):
    aeonSpellDirection(position, direction)


def aeonSpellDirection(position, direction):
    print("Aeon casting a spell. Special direction:", direction)
    while memory.main.battleMenuCursor() != 21:
        xbox.tapDown()
    while memory.main.mainBattleMenu():
        xbox.tapB()  # Black magic
    print("In Black Magic")
    _navigate_to_position(position)
    print(memory.main.otherBattleMenu())
    while memory.main.otherBattleMenu():
        xbox.tapB()  # Cast the Spell
    print(memory.main.otherBattleMenu())
    if direction == 'left':
        xbox.tapLeft()
    elif direction == 'right':
        xbox.tapRight()
    elif direction == 'up':
        xbox.tapUp()
    elif direction == 'down':
        xbox.tapDown()
    tapTargeting()
    print("Aeon casting spell")


def healUp(chars=3, *, fullMenuClose=True):
    print("Menuing, healing characters:", chars)
    if memory.main.getHP() == memory.main.getMaxHP():
        print("No need to heal. Exiting menu.")
        print(memory.main.menuNumber())
        if fullMenuClose:
            memory.main.closeMenu()
        else:
            if memory.main.menuOpen():
                memory.main.backToMainMenu()
        return
    if not memory.main.menuOpen():
        memory.main.openMenu()
    FFXC = xbox.controllerHandle()
    FFXC.set_neutral()
    while memory.main.getMenuCursorPos() != 2:
        print("Selecting Ability command -", memory.main.getMenuCursorPos())
        memory.main.menuDirection(memory.main.getMenuCursorPos(), 2, 11)
    while memory.main.menuNumber() == 5:
        print("Select Ability -", memory.main.menuNumber())
        xbox.tapB()
    print("Mark 1")
    target_pos = memory.main.getCharacterIndexInMainMenu(1)
    print(target_pos)
    while memory.main.getCharCursorPos() != target_pos:
        memory.main.menuDirection(memory.main.getCharCursorPos(
        ), target_pos, len(memory.main.getOrderSeven()))
    print("Mark 2")
    while memory.main.menuNumber() != 26:
        if memory.main.getMenu2CharNum() == 1:
            xbox.tapB()
        else:
            xbox.tapDown()
    while not memory.main.cureMenuOpen():
        xbox.tapB()
    character_positions = {
        0: memory.main.getCharFormationSlot(0),  # Tidus
        1: memory.main.getCharFormationSlot(1),  # Yuna
        2: memory.main.getCharFormationSlot(2),  # Auron
        3: memory.main.getCharFormationSlot(3),  # Kimahri
        4: memory.main.getCharFormationSlot(4),  # Wakka
        5: memory.main.getCharFormationSlot(5),  # Lulu
        6: memory.main.getCharFormationSlot(6)  # Rikku
    }
    print(character_positions)
    positions_to_characters = {val: key for key,
                               val in character_positions.items() if val != 255}
    print(positions_to_characters)
    maximal_hp = memory.main.getMaxHP()
    print("Max HP:", maximal_hp)
    current_hp = memory.main.getHP()
    for cur_position in range(len(positions_to_characters)):
        while current_hp[positions_to_characters[cur_position]] < maximal_hp[positions_to_characters[cur_position]]:
            print(current_hp)
            while memory.main.assignAbilityToEquipCursor() != cur_position:
                if memory.main.assignAbilityToEquipCursor() < cur_position:
                    xbox.tapDown()
                else:
                    xbox.tapUp()
            xbox.tapB()
            current_hp = memory.main.getHP()
        if current_hp == maximal_hp or memory.main.getYunaMP() < 4:
            break
    print("Healing complete. Exiting menu.")
    print(memory.main.menuNumber())
    if fullMenuClose:
        memory.main.closeMenu()
    else:
        memory.main.backToMainMenu()


def lancetSwap(direction):
    print("Lancet Swap function")
    # Assumption is formation: Tidus, Wakka, Auron, Kimahri, and Yuna in last slot.
    direction = direction.lower()
    buddySwapKimahri()

    lancet(direction)

    screen.awaitTurn()
    fleeAll()


def lancet(direction):
    print("Casting Lancet with variation:", direction)
    while memory.main.battleMenuCursor() != 20:
        if memory.main.battleMenuCursor() == 255:
            pass
        elif memory.main.battleMenuCursor() == 1:
            xbox.tapUp()
        elif memory.main.battleMenuCursor() > 20:
            xbox.tapUp()
        else:
            xbox.tapDown()
    while memory.main.mainBattleMenu():
        xbox.tapB()
    _navigate_to_position(0)
    while memory.main.otherBattleMenu():
        xbox.tapB()
    if direction == 'left':
        xbox.tapLeft()
    if direction == 'right':
        xbox.tapRight()
    if direction == 'up':
        xbox.tapUp()
    if direction == 'down':
        xbox.tapDown()
    tapTargeting()


def lancetTarget(target, direction):  # something
    print("Casting Lancet with variation:", direction)
    while memory.main.battleMenuCursor() != 20:
        if memory.main.battleMenuCursor() == 255:
            pass
        elif memory.main.battleMenuCursor() == 1:
            xbox.tapUp()
        elif memory.main.battleMenuCursor() > 20:
            xbox.tapUp()
        else:
            xbox.tapDown()
    while memory.main.mainBattleMenu():
        xbox.tapB()
    while memory.main.otherBattleMenu():
        xbox.tapB()
    retry = 0
    if memory.main.getEnemyCurrentHP()[target - 20] != 0:  # Only lancet living targets.
        while memory.main.battleTargetId() != target:
            if direction == 'l':
                if retry > 5:
                    retry = 0
                    print("Wrong battle line targeted.")
                    xbox.tapRight()
                    direction = 'u'
                    retry = 0
                else:
                    xbox.tapLeft()
            elif direction == 'r':
                if retry > 5:
                    retry = 0
                    print("Wrong character targeted.")
                    xbox.tapLeft()
                    direction = 'd'
                else:
                    xbox.tapRight()
            elif direction == 'u':
                if retry > 5:
                    retry = 0
                    print("Wrong character targeted.")
                    xbox.tapDown()
                    direction = 'l'
                else:
                    xbox.tapUp()
            elif direction == 'd':
                if retry > 5:
                    retry = 0
                    print("Wrong character targeted.")
                    xbox.tapUp()
                    direction = 'r'
                else:
                    xbox.tapDown()
            retry += 1

    tapTargeting()


def lancetHome(direction):
    print("Lancet (home) function")
    while memory.main.battleMenuCursor() != 20:
        if memory.main.battleMenuCursor() == 255:
            pass
        elif memory.main.battleMenuCursor() == 1:
            xbox.tapUp()
        elif memory.main.battleMenuCursor() > 20:
            xbox.tapUp()
        else:
            xbox.tapDown()
    while memory.main.mainBattleMenu():
        xbox.tapB()
    _navigate_to_position(2)
    while memory.main.otherBattleMenu():
        xbox.tapB()
    if direction == 'left':
        xbox.tapLeft()
    if direction == 'right':
        xbox.tapRight()
    if direction == 'up':
        xbox.tapUp()
    if direction == 'down':
        xbox.tapDown()
    tapTargeting()


def fleeAll():
    print("Attempting escape (all party members and end screen)")
    if memory.main.battleActive():
        while memory.main.battleActive():
            if memory.main.userControl():
                return
            if memory.main.turnReady():
                tidus_position = memory.main.getBattleCharSlot(0)
                print("Tidus Position:", tidus_position)
                if screen.turnTidus():
                    tidusFlee()
                elif tidus_position >= 3 and tidus_position != 255:
                    buddySwapTidus()
                elif not checkTidusOk() or tidus_position == 255 or memory.main.tidusEscapedState():
                    escapeOne()
                else:
                    defend()
    memory.main.clickToControl3()
    print("Flee complete")


def escapeAll():
    print("escapeAll function")
    while not screen.BattleComplete():
        if memory.main.turnReady():
            escapeOne()


def escapeAction():
    while memory.main.mainBattleMenu():
        if memory.main.battleComplete():
            break
        else:
            xbox.tapRight()
    print("In other battle menu")
    while memory.main.battleCursor2() != 2:
        if memory.main.battleComplete():
            break
        else:
            xbox.tapDown()
    print("Targeted Escape")
    while memory.main.otherBattleMenu():
        if memory.main.battleComplete():
            break
        else:
            xbox.tapB()
    if memory.main.battleActive():
        print("Selected Escaping")
        tapTargeting()

def escapeOne():
    print("##### The next character will escape:", rngTrack.nextActionEscape(character=memory.main.getCurrentTurn()))
    if not rngTrack.nextActionEscape(character=memory.main.getCurrentTurn()) and not memory.main.getEncounterID() == 26:
        if memory.main.getStoryProgress() < 154:
            print("Character cannot escape (Lagoon). Attacking instead.")
            attack('none')
        else:
            print("Character will not escape. Looking for a replacement.")
            replacement = 255
            replaceArray = memory.main.getBattleFormation()
            for i in range(len(replaceArray)):
                if replacement != 255:
                    pass
                elif replaceArray[i] == 255:
                    pass
                elif replaceArray[i] in memory.main.getActiveBattleFormation():
                    pass
                elif rngTrack.nextActionEscape(replaceArray[i]):
                    print("Character ", replaceArray[i], " can escape. Swapping.")
                    replacement = replaceArray[i]
                    buddySwap_char(replacement)
                    return escapeOne()
                else:
                    pass
            if replacement == 255:
                print("No character could be found.")
                if memory.main.getCurrentTurn() == 0:
                    tidusFlee()
                    return False
                elif memory.main.getCurrentTurn() == 1:
                    escapeAction()
                else:
                    attackByNum(num=memory.main.getCurrentTurn(), direction='u')
                    return False
    else:
        escapeAction()
        print("Attempting escape, one person")
        return True


def buddySwap_char(character):
    memory.main.waitFrames(6)
    print("Swapping characters (in battle) - by char num")
    position = memory.main.getBattleCharSlot(character)

    if position < 3:
        print("Cannot swap with character ", memory.main.nameFromNumber(character),
              ", that character is in the front party.")
        return
    else:
        while not memory.main.otherBattleMenu():
            xbox.lBumper()
        position -= 3
        reserveposition = position % 4
        print("Character is in position", reserveposition)
        if reserveposition == 3:  # Swap with last slot
            direction = 'up'
        else:
            direction = 'down'

        while reserveposition != memory.main.battleCursor2():
            if direction == 'down':
                xbox.tapDown()
            else:
                xbox.tapUp()

        while memory.main.otherBattleMenu():
            xbox.tapB()
        xbox.clickToBattle()
        screen.awaitTurn()
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
    print("Kimahri using Overdrive, pos -", pos)
    while not memory.main.otherBattleMenu():
        xbox.tapLeft()
    while memory.main.otherBattleMenu():
        xbox.tapB()
    _navigate_to_position(pos, battleCursor=memory.main.battleCursor3)
    while memory.main.interiorBattleMenu():
        xbox.tapB()
    tapTargeting()


def wrapUp():
    print("^^Wrapping up battle.")
    while not memory.main.userControl():
        if memory.main.menuOpen() or memory.main.diagSkipPossible():
            xbox.tapB()
        elif memory.main.turnReady():
            print("^^Still someone's turn. Could not wrap up battle.")
            return False
        else:
            pass
    print("^^Wrap up complete.")
    return True


def impulse(direction=None, targetFarLine=False):
    while memory.main.battleMenuCursor() != 217:
        if memory.main.battleMenuCursor() == 216:
            xbox.tapDown()
        else:
            xbox.tapUp()
    while not memory.main.otherBattleMenu():
        xbox.tapB()
    if direction == 'left':
        xbox.tapLeft()
    if targetFarLine:
        while not memory.main.battleLineTarget():
            xbox.tapLeft()
    tapTargeting()
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()


def SinArms():
    print("Fight start: Sin's Arms")
    # Area for improvement later. Multiple skippable FMVs
    xbox.clickToBattle()
    aeonSummon(4)
    while memory.main.battleActive():  # Arm1
        if memory.main.turnReady():
            impulse()
            xbox.tapB()
            xbox.tapB()
        else:
            xbox.tapB()

    xbox.SkipDialog(0.3)
    while not memory.main.battleActive():
        if memory.main.cutsceneSkipPossible():
            xbox.skipScene()
        elif memory.main.menuOpen() or memory.main.diagSkipPossible():
            xbox.tapB()

    aeonSummon(4)

    while memory.main.battleActive():  # Arm2
        if memory.main.turnReady():
            impulse()
            xbox.tapB()
            xbox.tapB()
        else:
            xbox.tapB()

    xbox.SkipDialog(0.3)
    while not memory.main.battleActive():
        if memory.main.cutsceneSkipPossible():
            xbox.skipScene()
        elif memory.main.menuOpen() or memory.main.diagSkipPossible():
            xbox.tapB()

    xbox.clickToBattle()  # Start of Sin Core
    aeonSummon(4)
    screen.awaitTurn()
    if gameVars.nemesis():
        while not memory.main.battleComplete():
            if memory.main.turnReady():
                attack('none')
    else:
        impulse(targetFarLine=True)
        xbox.tapB()
        xbox.tapB()

    while not memory.main.userControl():
        if memory.main.diagSkipPossible() or memory.main.menuOpen():
            xbox.tapB()
        elif memory.main.cutsceneSkipPossible():
            xbox.skipScene()
    print("Done with Sin's Arms section")


def SinFace():
    print("Fight start: Sin's Face")
    xbox.clickToBattle()
    FFXC.set_neutral()

    aeonFirstTurn = True
    while memory.main.battleActive():
        if memory.main.turnReady():
            if screen.turnYuna():
                aeonSummon(4)
            elif screen.turnAeon():
                if aeonFirstTurn:
                    impulse()
                    aeonFirstTurn = False
                else:
                    attack('none')
            else:
                defend()
        else:
            xbox.tapB()


def yojimbo():
    while not memory.main.turnReady():
        pass
    while memory.main.battleActive():
        if memory.main.turnReady():
            if screen.turnYuna():
                aeonSummon(4)
            elif screen.turnAeon():
                attack('none')
            else:
                defend()
        elif memory.main.diagSkipPossible():
            xbox.tapB()


def omnisItems():
    item1 = 99
    if memory.main.getItemSlot(32) < 200:
        item1 = 32
    elif memory.main.getItemSlot(30) < 200:
        item1 = 30
    elif memory.main.getItemSlot(27) < 200:
        item1 = 27
    else:
        item1 = 24

    if memory.main.getItemSlot(1) < 200:
        item2 = 1
    elif memory.main.getItemSlot(3) < 200:
        item2 = 3
    elif memory.main.getItemSlot(2) < 200:
        item2 = 2
    else:
        item2 = 7
    return [item1, item2]


def omnis():
    print("Fight start: Seymour Omnis")
    xbox.clickToBattle()
    defend()  # Yuna defends
    rikkuIn = False
    backupCure = False

    while memory.main.getEnemyMaxHP()[0] == memory.main.getEnemyCurrentHP()[0]:
        if memory.main.turnReady():
            if screen.turnTidus():
                useSkill(0)
            elif screen.turnAuron():
                buddySwapRikku()
                rikkuFullOD(battle='omnis')
                rikkuIn = True
            elif screen.turnYuna() and rikkuIn:
                if not backupCure:
                    yunaCureOmnis()
                    backupCure = True
                else:
                    equipInBattle(equipType='weap', abilityNum=0x8001, character=1)
            else:
                defend()

    print("Ready for aeon.")
    while not memory.main.battleComplete():  # AKA end of battle screen
        if memory.main.turnReady():
            print("Character turn:", memory.main.getBattleCharTurn())
            if screen.turnYuna():
                aeonSummon(4)
            elif screen.turnAeon():
                attack('none')
            elif screen.turnTidus():
                attack('none')
            else:
                defend()
        elif memory.main.diagSkipPossible():
            print("Skipping dialog maybe?")
            xbox.tapB()
    print("Should be done now.")
    memory.main.clickToControl()


def BFA_nem():
    FFXC.set_movement(1, 0)
    memory.main.waitFrames(30 * 0.4)
    FFXC.set_movement(1, 1)
    memory.main.waitFrames(30 * 3)
    FFXC.set_neutral()
    tidusFirstTurn = False

    xbox.clickToBattle()

    while memory.main.battleActive():
        if memory.main.turnReady():
            if screen.turnTidus():
                if tidusFirstTurn:
                    equipInBattle(equipType='weap',
                                  abilityNum=0x8019, character=0)
                    tidusFirstTurn = True
                else:
                    attack('none')
            else:
                defend()

    while memory.main.getStoryProgress() < 3400:  # End of game
        if memory.main.battleActive():
            if memory.main.turnReady():
                if screen.turnTidus():
                    if memory.main.getEncounterID() == 401 and memory.main.overdriveState2()[0] == 100:
                        tidusOD()
                    else:
                        attack('none')
                elif screen.turnYuna():
                    buddySwapWakka()
                elif screen.turnAuron():
                    buddySwapLulu()
                else:
                    defend()
        elif memory.main.cutsceneSkipPossible():
            memory.main.waitFrames(2)
            if memory.main.cutsceneSkipPossible():
                xbox.skipScene()
        elif memory.main.diagSkipPossible():
            xbox.tapB()


def BFA():
    if memory.main.getGilvalue() < 150000:
        swagMode = True
    else:
        swagMode = gameVars.yuYevonSwag()
    FFXC.set_movement(1, 0)
    memory.main.waitFrames(30 * 0.4)
    FFXC.set_movement(1, 1)
    memory.main.waitFrames(30 * 3)
    FFXC.set_neutral()

    xbox.clickToBattle()
    buddySwapRikku()
    if memory.main.overdriveState()[6] == 100:
        rikkuFullOD('bfa')
    else:
        useSkill(0)

    screen.awaitTurn()
    while memory.main.mainBattleMenu():
        xbox.tapLeft()
    while memory.main.battleCursor2() != 1:
        xbox.tapDown()
    while memory.main.otherBattleMenu():
        xbox.tapB()
    tapTargeting()
    buddySwapYuna()
    aeonSummon(4)

    # Bahamut finishes the battle.
    while memory.main.battleActive():
        xbox.tapB()

    # Skip the cutscene
    print("BFA down. Ready for Aeons")

    if not gameVars.csr():
        while not memory.main.cutsceneSkipPossible():
            xbox.tapB()
        xbox.skipScene()

    while memory.main.getStoryProgress() < 3380:
        if memory.main.turnReady():
            encounterID = memory.main.getEncounterID()
            print("Battle engaged. Battle number:", encounterID)
            if screen.turnYuna():
                if memory.main.battleMenuCursor() != 20:
                    while memory.main.battleMenuCursor() != 20:
                        if memory.main.battleMenuCursor() in [22, 1]:
                            xbox.tapUp()
                        else:
                            xbox.tapDown()
                while memory.main.mainBattleMenu():
                    xbox.tapB()
                while memory.main.otherBattleMenu():
                    xbox.tapB()
                print(memory.main.getEnemyMaxHP())
                aeon_hp = memory.main.getEnemyMaxHP()[0]
                if swagMode:
                    useGil = aeon_hp * 10
                elif aeon_hp % 1000 == 0:
                    useGil = aeon_hp * 10
                else:
                    useGil = (int(aeon_hp / 1000) + 1) * 10000
                print("#### USING GIL #### ", useGil)
                calculateSpareChangeMovement(useGil)
                while memory.main.spareChangeOpen():
                    xbox.tapB()
                while not memory.main.mainBattleMenu():
                    xbox.tapB()
            else:
                defend()
        elif not memory.main.battleActive():
            xbox.tapB()


def yuYevonItem():
    if memory.main.getItemSlot(6) < 200:
        return 6
    elif memory.main.getItemSlot(7) < 200:
        return 7
    elif memory.main.getItemSlot(8) < 200:
        return 8
    elif memory.main.getItemSlot(2) < 200:
        return 2
    elif memory.main.getItemSlot(1) < 200:
        return 1
    elif memory.main.getItemSlot(0) < 200:
        return 0
    else:
        return 99


def yuYevon():
    print("Ready for Yu Yevon.")
    screen.awaitTurn()  # No need for skipping dialog
    print("Awww such a sad final boss!")
    zombieAttack = False
    zaChar = gameVars.zombieWeapon()
    weapSwap = False
    while memory.main.getStoryProgress() < 3400:
        if memory.main.turnReady():
            print("-----------------------")
            print("-----------------------")
            print("zaChar:", zaChar)
            print("zombieAttack:", zombieAttack)
            print("weapSwap:", weapSwap)
            print("-----------------------")
            print("-----------------------")
            if zaChar == 1 and not zombieAttack:  # Yuna logic
                if not weapSwap and screen.turnYuna():
                    equipInBattle(equipType='weap',
                                  abilityNum=0x8032, character=1)
                    weapSwap = True
                elif screen.turnYuna():
                    attack('none')
                    zombieAttack = True
                elif weapSwap and not zombieAttack and screen.turnTidus():
                    xbox.weapSwap(0)
                else:
                    defend()
            elif zaChar == 0 and not zombieAttack:  # Tidus logic:
                if screen.turnYuna():
                    defend()
                elif screen.turnTidus() and not weapSwap:
                    equipInBattle(equipType='weap',
                                  abilityNum=0x8032, character=0)
                    weapSwap = True
                elif screen.turnTidus():
                    attack('none')
                    zombieAttack = True
                else:
                    defend()
            elif zaChar == 2 and not zombieAttack:  # Auron logic:
                if screen.turnYuna():
                    buddySwapAuron()
                elif screen.turnAuron() and not weapSwap:
                    equipInBattle(equipType='weap',
                                  abilityNum=0x8032, character=2)
                    weapSwap = True
                elif screen.turnAuron():
                    attack('none')
                    zombieAttack = True
                else:
                    defend()
            elif zaChar == 6 and not zombieAttack:  # Rikku logic:
                if screen.turnYuna() and not weapSwap:
                    # Piggy back off the weapSwap function
                    defend()
                    weapSwap = True
                elif screen.turnYuna():
                    xbox.weapSwap(0)
                elif screen.turnTidus():
                    tidusHaste('r', character=6)
                elif screen.turnRikku():
                    attack('none')
                    zombieAttack = True
                else:
                    defend()
            elif zombieAttack:  # Throw P.down to end game
                itemNum = yuYevonItem()
                if itemNum == 99:
                    attack('none')
                else:
                    while memory.main.battleMenuCursor() != 1:
                        xbox.tapDown()
                    while memory.main.mainBattleMenu():
                        xbox.tapB()
                    itemPos = memory.main.getThrowItemsSlot(itemNum)
                    _navigate_to_position(itemPos)
                    while memory.main.otherBattleMenu():
                        xbox.tapB()
                    while not memory.main.enemyTargetted():
                        xbox.tapUp()
                    tapTargeting()
                print("Phoenix Down on Yu Yevon. Good game.")
            elif screen.turnTidus() and zaChar == 255:
                # Tidus to use Zombie Strike ability
                useSkill(0)
                zombieAttack = True
            elif zaChar == 255 and not screen.turnTidus():
                # Non-Tidus char to defend so Tidus can use Zombie Strike ability
                defend()
            else:
                if memory.main.getBattleCharTurn() == zaChar:
                    attack('none')
                    zombieAttack = True
                elif memory.main.getBattleCharSlot(zaChar) >= 3:
                    buddySwap_char(zaChar)
                elif screen.turnTidus():
                    tidusHaste('l', character=zaChar)
                else:
                    defend()
        elif not memory.main.battleActive():
            xbox.tapB()


def checkPetrify():
    # This function is always returning as if someone is petrified, needs review.
    for iterVar in range(7):
        print(iterVar)
        if memory.main.petrifiedstate(iterVar):
            print("Character ", iterVar, " is petrified.")
            return True
    print("Everyone looks good - no petrification")
    return False


def checkPetrifyTidus():
    return memory.main.petrifiedstate(0)


def rikkuODItems(slot):
    _navigate_to_position(slot, battleCursor=memory.main.RikkuODCursor1)


def rikkuFullOD(battle):
    # First, determine which items we are using
    if battle == 'tutorial':
        item1 = memory.main.getItemSlot(73)
        print("Ability sphere in slot:", item1)
        item2 = item1
    elif battle == 'Evrae':
        if gameVars.skipKilikaLuck():
            item1 = memory.main.getItemSlot(81)
            print("Lv1 sphere in slot:", item1)
            item2 = memory.main.getItemSlot(84)
            print("Lv4 sphere in slot:", item2)
        else:
            item1 = memory.main.getItemSlot(94)
            print("Luck sphere in slot:", item1)
            item2 = memory.main.getItemSlot(100)
            print("Map in slot:", item2)
    elif battle == 'Flux':
        item1 = memory.main.getItemSlot(35)
        print("Grenade in slot:", item1)
        item2 = memory.main.getItemSlot(85)
        print("HP Sphere in slot:", item2)
    elif battle == 'trio':
        item1 = 108
        item2 = 108
        print("Wings are in slot:", item1)
    elif battle == 'crawler':
        item1 = memory.main.getItemSlot(30)
        print("Lightning Marble in slot:", item1)
        item2 = memory.main.getItemSlot(85)
        print("Mdef Sphere in slot:", item2)
    elif battle == 'spherimorph1':
        item1 = memory.main.getItemSlot(24)
        print("Arctic Wind in slot:", item1)
        item2 = memory.main.getItemSlot(90)
        print("Mag Def Sphere in slot:", item2)
    elif battle == 'spherimorph2':
        item1 = memory.main.getItemSlot(32)
        print("Fish Scale in slot:", item1)
        item2 = memory.main.getItemSlot(90)
        print("Mag Sphere in slot:", item2)
    elif battle == 'spherimorph3':
        item1 = memory.main.getItemSlot(30)
        print("Lightning Marble in slot:", item1)
        item2 = memory.main.getItemSlot(90)
        print("Mag Sphere in slot:", item2)
    elif battle == 'spherimorph4':
        item1 = memory.main.getItemSlot(27)
        print("Bomb Core in slot:", item1)
        item2 = memory.main.getItemSlot(90)
        print("Mag Sphere in slot:", item2)
    elif battle == 'bfa':
        item1 = memory.main.getItemSlot(35)
        print("Grenade in slot:", item1)
        item2 = memory.main.getItemSlot(85)
        print("HP Sphere in slot:", item2)
    elif battle == 'shinryu':
        item1 = memory.main.getItemSlot(109)
        print("Gambler's Spirit in slot:", item1)
        item2 = memory.main.getItemSlot(58)
        print("Star Curtain in slot:", item2)
    elif battle == 'omnis':
        bothItems = omnisItems()
        print("Omnis items, many possible combinations.")
        item1 = memory.main.getItemSlot(bothItems[0])
        item2 = memory.main.getItemSlot(bothItems[1])

    if item1 > item2:
        item3 = item1
        item1 = item2
        item2 = item3

    # Now to enter commands

    while not memory.main.otherBattleMenu():
        xbox.tapLeft()

    while not memory.main.interiorBattleMenu():
        xbox.tapB()
    rikkuODItems(item1)
    while not memory.main.rikkuOverdriveItemSelectedNumber():
        xbox.tapB()
    rikkuODItems(item2)
    while memory.main.interiorBattleMenu():
        xbox.tapB()
    tapTargeting()


def equipInBattle(equipType='weap', abilityNum=0, character=0, special='none'):
    equipType = equipType.lower()
    while memory.main.mainBattleMenu():
        xbox.tapRight()
    if equipType == 'weap':
        equipHandles = memory.main.weaponArrayCharacter(character)
    else:
        while memory.main.battleCursor2() != 1:
            xbox.tapDown()
        equipHandles = memory.main.armorArrayCharacter(character)
    while memory.main.otherBattleMenu():
        xbox.tapB()

    print("@@@@@")
    print("Character:", character)
    print("Equipment type:", equipType)
    print("Number of items:", len(equipHandles))
    print("Special:", special)
    print("@@@@@")
    equipNum = 255
    i = 0
    while len(equipHandles) > 0:
        currentHandle = equipHandles.pop(0)
        print(currentHandle.abilities())
        if special == 'baroque':
            if currentHandle.abilities() == [0x8063, 255, 255, 255]:
                equipNum = i
        elif special == 'brotherhood':
            if currentHandle.abilities() == [32867, 32868, 32810, 32768]:
                equipNum = i
        elif abilityNum == 0:
            print("Equipping just the first available equipment.")
            equipNum = 0
        elif currentHandle.hasAbility(abilityNum):  # First Strike for example
            equipNum = i
        i += 1
    while memory.main.battleCursor3() != equipNum:
        print("'''Battle cursor 3:", memory.main.battleCursor3())
        print("'''equipNum:", equipNum)
        if memory.main.battleCursor3() < equipNum:
            xbox.tapDown()
        else:
            xbox.tapUp()
    while memory.main.interiorBattleMenu():
        xbox.tapB()

    print("Desired equipment is in slot ", equipNum)


def checkCharacterOk(charNum):
    if charNum not in memory.main.getActiveBattleFormation():
        return True
    return not any(func(charNum) for func in [memory.main.petrifiedstate, memory.main.confusedState, memory.main.deadstate, memory.main.berserkstate])


def checkTidusOk():
    return checkCharacterOk(0)


def checkRikkuOk():
    return checkCharacterOk(6)


def checkYunaOk():
    return checkCharacterOk(1)


def get_digit(number, n):
    return number // 10**n % 10


def calculateSpareChangeMovement(gilAmount):
    if gilAmount > memory.main.getGilvalue():
        gilAmount = memory.main.getGilvalue()
    gilAmount = min(gilAmount, 100000)
    position = {}
    gilCopy = gilAmount
    for index in range(0, 7):
        amount = get_digit(gilAmount, index)
        if amount > 5:
            gilAmount += 10**(index + 1)
        position[index] = amount
    print(position)
    for cur in range(6, -1, -1):
        if not position[cur]:
            continue
        while memory.main.spareChangeCursor() != cur:
            memory.main.sideToSideDirection(
                memory.main.spareChangeCursor(), cur, 6)
        target = position[cur]
        while get_digit(memory.main.spareChangeAmount(), cur) != target:
            if target > 5:
                xbox.tapDown()
            else:
                xbox.tapUp()
        if memory.main.spareChangeAmount() == gilCopy:
            return
    return


def chargeRikkuOD():
    print("#####Battle Number:", memory.main.getEncounterID())
    if memory.main.getOverdriveBattle(6) != 100 and memory.main.getEncounterID() in [360, 361, 376, 378, 381, 384, 386]:
        if (not memory.main.tidusEscapedState() and not checkTidusOk()) or not checkRikkuOk():
            print("Tidus or Rikku incapacitated, fleeing")
            print("--", not memory.main.tidusEscapedState())
            print("--", not checkTidusOk())
            print("--", not checkRikkuOk())
            fleeAll()
        else:
            while not memory.main.battleComplete():
                if memory.main.turnReady():
                    turnchar = memory.main.getBattleCharTurn()
                    if turnchar == 6:
                        attackByNum(6, direction='u')
                    elif memory.main.getOverdriveBattle(6) == 100:
                        fleeAll()
                    elif 6 not in memory.main.getActiveBattleFormation():
                        buddySwapRikku()
                    else:
                        escapeOne()
        memory.main.clickToControl3()
    else:
        fleeAll()


def faintCheckWithEscapes():
    faints = 0
    for x in range(3):
        if memory.main.getActiveBattleFormation()[x] == 255:
            pass
        elif memory.main.deadstate(memory.main.getActiveBattleFormation()[x]):
            faints += 1
    return faints


def checkGems():
    gemSlot = memory.main.getItemSlot(34)
    if gemSlot < 200:
        gems = memory.main.getItemCountSlot(gemSlot)
    else:
        gems = 0

    gemSlot = memory.main.getItemSlot(28)
    if gemSlot < 200:
        gems += memory.main.getItemCountSlot(gemSlot)
    print("Total gems:", gems)
    return gems


def calmLandsManip():
    print("++Battle number:", memory.main.getEncounterID())
    rng10nextChanceLow = memory.main.nextChanceRNG10(12)
    lowArray = [273, 275, 276, 281, 283, 284]
    rng10nextChanceMid = memory.main.nextChanceRNG10(60)
    midArray = [277, 279, 285, 287, 289, 290]
    rng10nextChanceHigh = memory.main.nextChanceRNG10(128)
    highArray = [278, 286, 288]
    if checkGems() < 2:
        print("++++ Gems: ", checkGems())
        print("++++ Calm Lands battle, need gems.")
        calmLandsGems()
    else:
        print("++++ Gems good. NEA manip logic.")
        advancePreX, advancePostX = rngTrack.neaTrack()  # returns integers
        if advancePreX != 0 and advancePostX != 0:  # Non-zero for both
            print("Not lined up for NEA")
            if rng10nextChanceLow == 0 and memory.main.getEncounterID() in lowArray:
                advanceRNG12()
            elif rng10nextChanceMid == 0 and memory.main.getEncounterID() in midArray:
                advanceRNG12()
            elif rng10nextChanceHigh == 0 and memory.main.getEncounterID() in highArray:
                advanceRNG12()
            else:  # If we can't advance on this battle, try to get the next "mid" level advance.
                print("Can't drop off of this battle.")
                advanceRNG10(rng10nextChanceMid)
        elif advancePostX == 0:  # Lined up for next drop NEA before defender X.
            print("The next equipment to drop will be NEA")
            if memory.main.getCoords()[0] > 1300:
                print("--Near Gagazet, just get off RNG10 equipment drop.")
                if memory.main.nextChanceRNG10() == 0:
                    advanceRNG10(1) # Gets us off of a drop on defender X - probably. :D
                    # Don't want to have Defender X drop an item
                else:
                    fleeAll()
            elif memory.main.nextChanceRNG10Calm():
                advanceRNG10(memory.main.nextChanceRNG10Calm())
            else:
                print("Lined up OK, ready for NEA. Just flee.")
                fleeAll()
        elif advancePreX == 0:
            print("The second equipment drop from now will be NEA.")
            if memory.main.nextChanceRNG10() != 0:
                advanceRNG10(memory.main.nextChanceRNG10())
                # Trying to get onto a good drop.
            else:
                print("Perfectly lined up pre-X. Just flee.")
                fleeAll()
        else:
            print("Fallback logic, not sure.")
            memory.main.waitFrames(180)
            fleeAll()

def calmLandsManip_old():
    print("++Battle number:", memory.main.getEncounterID())
    rng10nextChanceLow = memory.main.nextChanceRNG10(12)
    lowArray = [273, 275, 276, 281, 283, 284]
    rng10nextChanceMid = memory.main.nextChanceRNG10(60)
    midArray = [277, 279, 285, 287, 289, 290]
    rng10nextChanceHigh = memory.main.nextChanceRNG10(128)
    highArray = [278, 286, 288]
    if checkGems() < 2:
        print("++++ Gems: ", checkGems())
        print("++++ Calm Lands battle, looking for gems.")
        calmLandsGems()
    elif memory.main.rngSeed == 31 and memory.main.nextChanceRNG10() == 0 and memory.main.nextChanceRNG12() == 1:
        print("Specific logic for RNG seed 31, just drop item off of defender X")
        fleeAll()
    elif memory.main.nextChanceRNG12() != 0:
        print("Not ready for NE armor drop. Apply logic to try to drop something else.")
        # NE armor too far ahead. Need to drop armors.
        if rng10nextChanceLow == 0 and memory.main.getEncounterID() in lowArray:
            advanceRNG12()
        elif rng10nextChanceMid == 0 and memory.main.getEncounterID() in midArray:
            advanceRNG12()
        elif rng10nextChanceHigh == 0 and memory.main.getEncounterID() in highArray:
            advanceRNG12()
        else:  # Cycle mid chance as needed.
            print("Can't drop off of this battle.")
            advanceRNG10(rng10nextChanceMid)
    else:
        setupNext = memory.main.nextChanceRNG10Calm()
        if memory.main.getCoords()[0] > 1300:
            print("--Near Gagazet, just get off RNG10 equipment drop.")
            if memory.main.nextChanceRNG10() == 0:
                advanceRNG10(memory.main.nextChanceRNG10())
                # Don't want to have Defender X drop an item
        elif setupNext != 0:
            if setupNext < 25:
                print("++Still a ways. Try to set up for Defender X plus Wraith.")
                advanceRNG10(setupNext)
                # Try for perfect setup if it's not too far off.
            elif memory.main.nextChanceRNG10() == 0:
                print("++No perfect chance coming up. Going for regular chance.")
                advanceRNG10(memory.main.nextChanceRNG10())
            else:
                print("--Next perfect value is too far away. Moving on.")
                fleeAll()
        else:
            print("--Perfectly set up and good to go.")
            fleeAll()


def calmSteal():
    if memory.main.getEncounterID() == 313:
        _steal('down')
    elif memory.main.getEncounterID() == 289:
        _steal('up')
    elif memory.main.getEncounterID() == 314:
        _steal('right')
    else:
        _steal()


def advanceRNG10(numAdvances: int):
    escapeSuccessCount = 0
    print("#################")
    print("###RNG10 logic###")
    print("##    ", numAdvances, "      ##")
    print("##    ", screen.faintCheck(), "      ##")
    print("#################")
    while memory.main.battleActive():
        if memory.main.turnReady():
            print("+++Registering advances:", numAdvances)
            if memory.main.battleType() == 2:
                print("+++Registering ambush")
                fleeAll()
            elif memory.main.getEncounterID() == 321:
                print("+++Registering evil jar guy, fleeing.")
                fleeAll()
            elif memory.main.getEncounterID() == 287:
                print("+++Registering Anaconadeur - I am French!!! - fleeing")
                fleeAll()
            elif numAdvances >= 6:
                if escapeSuccessCount == 0:
                    if escapeOne():
                        escapeSuccessCount += 1
                elif faintCheckWithEscapes() == 2:
                    print("+++Registering two people down. Escaping.")
                    fleeAll()
                elif screen.turnKimahri() or screen.turnRikku():
                    print("+++Registering turn, steal character")
                    # Most convenient since overdrive is needed for Flux.
                    if numAdvances % 3 != 0:
                        calmSteal()
                        numAdvances -= 1
                    elif escapeSuccessCount == 0:
                        if escapeOne():
                            escapeSuccessCount += 1
                    else:
                        defend()
                elif 3 in memory.main.getBattleFormation() and 3 not in memory.main.getActiveBattleFormation() and numAdvances % 3 != 0:
                    buddySwapKimahri()
                elif escapeSuccessCount == 0:
                    if escapeOne():
                        escapeSuccessCount += 1
                else:
                    defend()
            elif numAdvances >= 3:
                if faintCheckWithEscapes() >= 1:
                    fleeAll()
                elif escapeSuccessCount == 0:
                    if escapeOne():
                        escapeSuccessCount += 1
                elif screen.turnRikku() and escapeSuccessCount == 1:
                    if escapeOne():
                        escapeSuccessCount += 1
                elif screen.turnKimahri():
                    print("+++Registering turn, steal character")
                    # Most convenient since overdrive is needed for Flux.
                    if numAdvances % 3 != 0:
                        calmSteal()
                        numAdvances -= 1
                    else:
                        defend()
                elif 3 in memory.main.getBattleFormation() and 3 not in memory.main.getActiveBattleFormation() and numAdvances % 3 != 0:
                    buddySwapKimahri()
                elif escapeSuccessCount in [0, 1]:
                    if escapeOne():
                        escapeSuccessCount += 1
                else:
                    defend()
            elif numAdvances in [1, 2]:
                print("+++Registering advances:", numAdvances)
                if screen.turnKimahri():
                    print("+++Registering turn, steal character")
                    calmSteal()
                    numAdvances -= 1
                elif 3 not in memory.main.getActiveBattleFormation():
                    buddySwapKimahri()
                elif screen.turnTidus():
                    fleeAll()
                elif 0 not in memory.main.getActiveBattleFormation():
                    buddySwapTidus()
                else:
                    defend()  # should not occur.
            else:  # any other scenarios, ready to advance.
                print("+++Registering no advances needed, forcing flee.")
                fleeAll()
    memory.main.clickToControl3()


def rng12Attack(tryImpulse=False):
    print("#################")
    print("###RNG12 logic (attack only) ###")
    print("#################")
    if screen.turnAeon():
        if memory.main.getEncounterID() in [283, 309, 313]:
            attackByNum(21, 'u')  # Second target
        elif memory.main.getEncounterID() in [284]:
            attackByNum(22, 'u')  # Third target
        elif memory.main.getEncounterID() in [275, 289]:
            attackByNum(21, 'r')  # Second target, aim right (aeon only)
        elif memory.main.getEncounterID() in [303]:
            attackByNum(21, 'l')  # Second target
        elif memory.main.getEncounterID() in [304]:
            attackByNum(23, 'u')  # fourth target
        elif memory.main.getEncounterID() in [314]:
            attackByNum(21, 'r')
        else:
            attack('none')
    else:  # Non-aeon logic, fix this later.
        attack('none')


def advanceRNG12():
    print("#################")
    print("###RNG12 logic (decision logic) ###")
    print("#################")
    attackCount = False
    aeonTurn = False
    useImpulse = False
    doubleDrop = False
    while memory.main.battleActive():
        if memory.main.getEncounterID() == 321:
            print("+++Registering evil jar guy")
            print("Aw hell naw, we want nothing to do with this guy! (evil jar guy)")
            fleeAll()
        elif memory.main.turnReady():
            preX, postX = rngTrack.neaTrack()
            if postX == 1:
                advances = 1
            elif memory.main.getMap() == 223:
                advances = preX
            else:
                advances = postX
            if screen.turnYuna():
                if aeonTurn:
                    fleeAll()
                else:
                    aeonSummon(4)
            elif screen.turnAeon():
                numEnemies = len(memory.main.getEnemyCurrentHP())
                print("+++ ", memory.main.getEnemyCurrentHP())
                print("+++ ", numEnemies)
                checkAhead = numEnemies * 3
                print("+++ ", checkAhead)
                aheadArray = memory.main.nextChanceRNG10Full()
                for h in range(checkAhead):
                    if h == 3:
                        pass
                    elif h % 3 != 0 and aheadArray[h]:
                        doubleDrop = True
                for i in range(7):
                    if aheadArray[i + checkAhead] and not attackCount:
                        useImpulse = True
                if not attackCount:
                    if memory.main.getEncounterID() in [314]:
                        impulse()
                        attackCount = True
                    elif advances >= 2:
                        impulse()
                        attackCount = True
                    elif advances == 1:
                        if useImpulse and not doubleDrop:
                            impulse()
                            attackCount = True
                        else:
                            attackCount = True
                            rng12Attack()
                    else:
                        aeonDismiss()
                else:
                    aeonDismiss()
                aeonTurn = True
            else:
                if aeonTurn:
                    fleeAll()
                elif 1 not in memory.main.getActiveBattleFormation():
                    buddySwapYuna()
                else:
                    defend()
    memory.main.clickToControl3()


def ghostKill():
    import rngTrack
    nextDrop, _ = rngTrack.itemToBeDropped()
    owner1 = nextDrop.equipOwner
    owner2 = nextDrop.equipOwnerAlt
    silenceSlotCheck = memory.main.getItemSlot(39)
    if silenceSlotCheck == 255:
        silenceSlot = 255
    else:
        silenceSlot = memory.main.getUseItemsSlot(39)
    tidusHasted = False
    
    if memory.main.nextChanceRNG10():
        tidusHasted = ghostAdvanceRNG10Silence(silenceSlot=silenceSlot, owner1=owner1, owner2=owner2)
        silenceSlot = 255 # will be used while prepping RNG10 anyway.
    
    if owner2 in [0, 4, 6]:
        print("Aeon kill results in NEA on char:", owner2)
        ghostKillAeon()
    elif silenceSlot > 200:
        print("No silence grenade, going with aeon kill: ", owner2)
        ghostKillAeon()
    elif owner1 in [0, 4, 6]:
        print("Any character kill results in NEA on char:", owner1)
        ghostKillAny(silenceSlot=silenceSlot, tidusHasted=tidusHasted)
    elif owner1 == 9:
        print("Has to be Tidus kill: ", owner1)
        ghostKillTidus(silenceSlot=silenceSlot, tidusHasted=tidusHasted)
    else:
        print("No way to get an optimal drop. Resorting to aeon: ", owner2)
        ghostKillAeon()

    memory.main.clickToControl3()

def ghostAdvanceRNG10Silence(silenceSlot:int, owner1:int, owner2:int):
    print("RNG10 is not aligned. Special logic to align.")
    # Premise is that we must have a silence grenade in inventory.
    # We should force extra manip in gorge if no silence grenade,
    # so should be guaranteed if this triggers.
    prefDrop = [0,4,6]
    silenceUsed = False
    tidusHasted = False
    while memory.main.nextChanceRNG10():
        if memory.main.turnReady():
            if silenceUsed == False:
                if not 6 in memory.main.getActiveBattleFormation():
                    buddySwapRikku()
                    useItem(slot=silenceSlot) # Throw silence grenade
                    silenceUsed = True
                elif not 3 in memory.main.getActiveBattleFormation():
                    buddySwapKimahri()
                    useItem(slot=silenceSlot) # Throw silence grenade
                    silenceUsed = True
                elif screen.turnRikku() or screen.turnKimahri():
                    useItem(slot=silenceSlot) # Throw silence grenade
                    silenceUsed = True
                else:
                    defend()
            #Next, put in preferred team
            elif owner2 in prefDrop or not owner1 in prefDrop: # prefer aeon kill
                if screen.turnRikku() or screen.turnKimahri():
                    Steal()
                elif not 6 in memory.main.getActiveBattleFormation():
                    buddySwapRikku()
                elif not 3 in memory.main.getActiveBattleFormation():
                    buddySwapKimahri()
                elif not 0 in memory.main.getActiveBattleFormation():
                    buddySwapTidus()
                else:
                    defend()
            else: #Will need a non-Aeon kill
                if not 6 in memory.main.getActiveBattleFormation():
                    buddySwapRikku()
                elif not 0 in memory.main.getActiveBattleFormation():
                    buddySwapTidus()
                elif not 3 in memory.main.getActiveBattleFormation() and memory.main.nextChanceRNG10() > 3:
                    buddySwapKimahri()
                elif not 1 in memory.main.getActiveBattleFormation() and memory.main.nextChanceRNG10() <= 3:
                    buddySwapYuna()
                elif screen.turnRikku() or screen.turnKimahri():
                    Steal()
                elif screen.turnTidus() and not tidusHasted:
                    tidusHasted = True
                    tidusHaste('none')
                elif memory.main.getEnemyCurrentHP()[0] > 3000:
                    attack()
                else:
                    defend()
    return tidusHasted
    print("RNG10 is now aligned.")

def ghostKillTidus(silenceSlot:int, selfHaste:bool):
    print("++Silence slot:", silenceSlot)
    while memory.main.battleActive():
        # Try to get NEA on Tidus
        if memory.main.turnReady():
            if 0 not in memory.main.getActiveBattleFormation():
                print("+++Get Tidus back in")
                buddySwapTidus()
            elif screen.turnTidus():
                if not selfHaste:
                    tidusHaste('none')
                    selfHaste = True
                elif memory.main.getEnemyCurrentHP()[0] <= 2800 and memory.main.getOverdriveBattle(0) == 100:
                    tidusOD()
                else:
                    attack('none')
            elif 1 not in memory.main.getActiveBattleFormation():
                print("+++Get Yuna in for extra smacks")
                buddySwapYuna()
            elif screen.turnYuna() and memory.main.getEnemyCurrentHP()[0] > 3000:
                attack('none')
            else:
                defend()

def ghostKillAny(silenceSlot:int, selfHaste:bool):
    yunaHaste = False
    itemThrown = silenceSlot >= 200
    print("++Silence slot:", silenceSlot)
    while memory.main.battleActive():
        if memory.main.turnReady():
            if 0 not in memory.main.getActiveBattleFormation():
                print("+++Get Tidus back in")
                buddySwapTidus()
            elif screen.turnTidus():
                if not selfHaste:
                    tidusHaste('none')
                    selfHaste = True
                elif 1 in memory.main.getActiveBattleFormation() and not yunaHaste \
                    and memory.main.getEnemyCurrentHP()[0] <= 6000:
                    tidusHaste(direction='l', character=1)
                    yunaHaste = True
                elif memory.main.getEnemyCurrentHP()[0] <= 2800 and memory.main.getOverdriveBattle(0) == 100:
                    tidusOD()
                else:
                    attack('none')
            elif 1 not in memory.main.getActiveBattleFormation():
                print("+++Get Yuna in for extra smacks")
                buddySwapYuna()
            elif screen.turnYuna():
                attack('none')
            else:
                defend()

def ghostKillAeon():
    while memory.main.battleActive():
        if memory.main.turnReady():
            if screen.turnAeon():
                attack('none')
            elif 1 not in memory.main.getActiveBattleFormation():
                buddySwapYuna()
            elif screen.turnYuna():
                aeonSummon(4)
            else:
                defend()
