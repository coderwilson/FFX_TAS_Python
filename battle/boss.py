import battle.main
import logs
import memory.main
import screen
import vars
import xbox

FFXC = xbox.controllerHandle()
gameVars = vars.varsHandle()


def ammes():
    BattleComplete = 0
    countAttacks = 0
    tidusODflag = False

    while BattleComplete != 1:
        if memory.main.turnReady():
            if (
                not tidusODflag
                and screen.turnTidus()
                and memory.main.getOverdriveBattle(0) == 100
            ):
                battle.overdrive.tidus()
                tidusODflag = True
            else:
                print("Attacking Sinspawn Ammes")
                battle.main.attack("none")
                countAttacks += 1
        if memory.main.userControl():
            BattleComplete = 1
            print("Ammes battle complete")


def tanker():
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
                    battle.main.attack("none")
                    countAttacks += 1
            elif screen.turnAuron():
                auronCount += 1
                if auronCount < 2:
                    battle.main.attackSelfTanker()
                else:
                    battle.main.attack("none")
                    countAttacks += 1
        elif memory.main.diagSkipPossible():
            xbox.tapB()


def klikk():
    print("Fight start: Klikk")
    klikkAttacks = 0
    klikkRevives = 0
    stealCount = 0
    while not memory.main.battleComplete():  # AKA end of battle screen
        if memory.main.turnReady():
            BattleHP = memory.main.getBattleHP()
            if BattleHP[0] == 0:
                battle.main.revive()
                klikkRevives += 1
            elif screen.turnTidus():
                if BattleHP[0] == 0 and memory.main.getEnemyCurrentHP()[0] > 125:
                    battle.main.usePotionCharacter(0, "l")
                else:
                    battle.main.attack("none")
                klikkAttacks += 1
            elif screen.turnRikku():
                grenadeCount = memory.main.getItemCountSlot(memory.main.getItemSlot(35))
                if (
                    BattleHP[0] < 120
                    and not (
                        memory.main.getNextTurn() == 0
                        and memory.main.getEnemyCurrentHP()[0] <= 181
                    )
                    and not memory.main.rngSeed() == 160
                ):
                    battle.main.usePotionCharacter(0, "l")
                    klikkRevives += 1
                elif memory.main.getEnemyCurrentHP()[0] < 58:
                    battle.main.attack("none")
                    klikkAttacks += 1
                elif grenadeCount < 6 and memory.main.nextSteal(stealCount=stealCount):
                    print("Attempting to steal from Klikk")
                    battle.main.Steal()
                    stealCount += 1
                else:
                    battle.main.attack("none")
                    klikkAttacks += 1
        else:
            if memory.main.diagSkipPossible():
                xbox.tapB()
    print("Klikk fight complete")
    print(memory.main.getMap())
    while not (
        memory.main.getMap() == 71
        and memory.main.userControl()
        and memory.main.getCoords()[1] < 15
    ):
        # print(memory.main.getMap())
        if gameVars.csr():
            FFXC.set_value("BtnB", 1)
        else:
            xbox.tapB()  # Maybe not skippable dialog, but whatever.
    FFXC.set_neutral()
    memory.main.waitFrames(1)


def tros():
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
                    battle.main.revive()
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
                            battle.main.defend()
                        else:
                            battle.main.Steal()
                            Steals += 1
                    elif grenadeCount == 0:
                        if trosPos == 1:
                            battle.main.defend()
                        else:
                            battle.main.Steal()
                            Steals += 1
                    else:
                        if trosPos != 1 and advances in [1, 2]:
                            battle.main.Steal()
                            Steals += 1
                        else:
                            grenadeSlot = memory.main.getUseItemsSlot(35)
                            battle.main.useItem(grenadeSlot, "none")
                            Grenades += 1
                elif screen.turnTidus():
                    print("Tidus turn")
                    if (
                        trosPos == 1
                        and memory.main.getBattleHP()[1] < 200
                        and memory.main.getEnemyCurrentHP()[0] > 800
                    ):
                        battle.main.usePotionCharacter(6, "l")
                    elif trosPos == 1 or memory.main.getEnemyCurrentHP()[0] < 300:
                        battle.main.defend()
                    else:
                        battle.main.attack("none")
                        Attacks += 1

    print("Tros battle complete.")
    memory.main.clickToControl()


def sinFin():
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
                battle.main.defend()
                print("Tidus defend")
            elif screen.turnYuna():
                battle.main.buddySwapLulu()  # Yuna out, Lulu in
                battle.main.thunderTarget(target=23, direction="r")
            elif screen.turnKimahri():
                battle.main.lancetTarget(target=23, direction="r")
                kimTurn = True
            elif screen.turnLulu():
                battle.main.thunderTarget(target=23, direction="r")
            else:
                battle.main.defend()
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
                battle.main.lancetTarget(23, "r")
            elif screen.turnLulu():
                battle.main.thunderTarget(23, "r")
            elif screen.turnTidus():
                if turnCounter < 4:
                    battle.main.defend()
                    memory.main.waitFrames(30 * 0.2)
                else:
                    battle.main.buddySwapYuna()
                    battle.main.aeonSummon(0)
            elif screen.turnAeon():
                battle.overdrive.valefor(sinFin=1)
                print("Valefor energy blast")
    print("Sin's Fin fight complete")
    xbox.clickToBattle()


def echuilles():
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
                battle.main.revive()
            elif screen.turnTidus():
                tidusCounter += 1
                if tidusCounter <= 2:
                    print("Cheer")
                    battle.main.tidusFlee()  # performs cheer command
                elif (
                    memory.main.getOverdriveBattle(0) == 100
                    and memory.main.getEnemyCurrentHP()[0] <= 750
                ):
                    print("Overdrive")
                    battle.overdrive.tidus()
                else:
                    print("Tidus attack")
                    battle.main.attack("none")
            elif screen.turnWakka():
                if tidusCounter == 1:  # and memory.main.rngSeed() != 160:
                    print("Dark Attack")
                    battle.main.useSkill(0)  # Dark Attack
                # elif memory.main.getEnemyCurrentHP()[0] <= 558:
                #    print("Ready for Tidus Overdrive. Wakka defends.")
                #    defend()
                else:
                    print("Wakka attack")
                    battle.main.attack("none")
    print("Battle is complete. Now awaiting control.")
    while not memory.main.userControl():
        if memory.main.cutsceneSkipPossible():
            xbox.skipScene()
        elif memory.main.menuOpen() or memory.main.diagSkipPossible():
            xbox.tapB()
    logs.writeRNGTrack("######################################")
    logs.writeRNGTrack("Echuilles end")
    logs.writeRNGTrack(memory.main.rng10Array(arrayLen=1))


def geneaux():
    print("Fight start: Sinspawn Geneaux")
    xbox.clickToBattle()

    if screen.turnTidus():
        battle.main.attack("none")
    elif screen.turnYuna():
        battle.main.buddySwapKimahri()
        battle.main.attack("none")
        while not screen.turnTidus():
            battle.main.defend()
        while screen.turnTidus():
            battle.main.defend()
        battle.main.buddySwapYuna()
    screen.awaitTurn()
    battle.main.aeonSummon(0)  # Summon Valefor
    screen.awaitTurn()
    battle.overdrive.valefor()

    while not memory.main.battleComplete():  # AKA end of battle screen
        if memory.main.diagSkipPossible():
            xbox.tapB()
        elif memory.main.turnReady():
            print("Valefor casting Fire")
            battle.main.aeonSpell(0)
        else:
            FFXC.set_neutral()
    print("Battle Complete")
    memory.main.clickToControl()


def oblitzerator(earlyHaste):
    print("Fight start: Oblitzerator")
    xbox.clickToBattle()
    crane = 0

    if earlyHaste >= 1:
        # First turn is always Tidus. Haste Lulu if we've got the levels.
        battle.main.tidusHaste(direction="left", character=5)

    while not memory.main.battleComplete():  # AKA end of battle screen
        if memory.main.turnReady():
            if crane < 3:
                if screen.turnLulu():
                    crane += 1
                    battle.main.thunderTarget(target=21, direction="r")
                else:
                    battle.main.defend()
            elif crane == 3:
                if screen.turnTidus():
                    crane += 1
                    while memory.main.mainBattleMenu():
                        xbox.tapLeft()
                    while memory.main.battleCursor2() != 1:
                        xbox.tapDown()
                    while memory.main.otherBattleMenu():
                        xbox.tapB()
                    battle.main.tapTargeting()
                elif screen.turnLulu():
                    battle.main.thunder("none")
                else:
                    battle.main.defend()
            else:
                if screen.turnLulu():
                    battle.main.thunder("none")
                elif screen.turnTidus():
                    battle.main.attackOblitzEnd()
                else:
                    battle.main.defend()
        elif memory.main.diagSkipPossible():
            xbox.tapB()
    print("End of fight, Oblitzerator")
    memory.main.clickToControl()
    # logs.writeStats("RNG02 after battle:")
    # logs.writeStats(memory.s32(memory.rng02()))


def chocoboEater():
    print("Fight start: Chocobo Eater")
    rng44Last = memory.main.rngFromIndex(44)
    turns = 0
    chocoTarget = 255
    chocoNext = False
    chocoHaste = False
    screen.awaitTurn()
    charHpLast = memory.main.getBattleHP()

    # If chocobo doesn't take the second turn, that means it out-sped Tidus.
    if memory.main.getNextTurn() != 20:
        if memory.main.rngFromIndex(44) == rng44Last:
            # Eater did not take an attack, but did take first turn. Should register as true.
            chocoNext = True
    swappedYuna = False
    while memory.main.battleActive():
        if memory.main.turnReady():
            if chocoNext:
                chocoNext = False
                if memory.main.getBattleHP() != charHpLast:  # We took damage
                    pass
                elif (
                    memory.main.rngFromIndex(44) != rng44Last
                ):  # Chocobo eater attacked, covers miss
                    pass
                elif (
                    chocoTarget == 255
                    and 1 not in memory.main.getActiveBattleFormation()
                ):
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
                    battle.main.buddySwapYuna()
                    battle.main.attackByNum(1)
                    chocoTarget = 255
                    swappedYuna = True
            if memory.main.getNextTurn() == 20:
                chocoNext = True
                charHpLast = memory.main.getBattleHP()
                rng44Last = memory.main.rngFromIndex(44)
            if chocoTarget != 255:
                print("#####  Target for You're Next attack: ", chocoTarget)

            # Only if two people are down, very rare but for safety.
            if screen.faintCheck() >= 2:
                print("Attempting revive")
                if screen.turnKimahri():
                    if 0 not in memory.main.getActiveBattleFormation():
                        battle.main.buddySwapTidus()
                    elif 4 not in memory.main.getActiveBattleFormation():
                        battle.main.buddySwapWakka()
                    else:
                        battle.main.buddySwapAuron()
                battle.main.revive()
            # elif 0 not in memory.main.getActiveBattleFormation():
            # Doesn't work - it still hits Tidus if he swapped out and back in (instead of Yuna).
            #    buddySwapTidus()
            elif (
                swappedYuna
                and 0 not in memory.main.getActiveBattleFormation()
                and memory.main.deadstate(1)
                and not chocoHaste
            ):
                battle.main.buddySwapTidus()
            elif (
                1 in memory.main.getActiveBattleFormation()
                and not chocoHaste
                and memory.main.getBattleCharTurn() == 0
            ):
                battle.main.tidusHaste(
                    direction="l", character=20
                )  # After Yuna in, haste choco eater.
                chocoHaste = True
            else:
                print("Attempting defend")
                battle.main.defend()
        elif memory.main.diagSkipPossible():
            print("Skipping dialog")
            xbox.tapB()
    # logs.writeStats("Chocobo eater turns:")
    # logs.writeStats(str(turns))
    print("Chocobo Eater battle complete.")


def gui():
    print("Fight start: Sinspawn Gui")
    xbox.clickToBattle()
    print("Engaging Gui")
    print(
        "##### Expecting crit: ",
        memory.main.nextCrit(character=3, charLuck=18, enemyLuck=15),
    )
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
                    battle.main.buddySwapAuron()
                    yunaTurn = True
                else:
                    battle.main.aeonSummon(0)
            elif screen.turnWakka():
                if not wakkaTurn:
                    xbox.weapSwap(0)
                    wakkaTurn = True
                else:
                    battle.main.buddySwapKimahri()
                    print(
                        "##### Expecting crit: ",
                        memory.main.nextCrit(character=3, charLuck=18, enemyLuck=15),
                    )
            elif screen.turnKimahri():
                dmgBefore = memory.main.getEnemyCurrentHP()[0]
                battle.overdrive.kimahri(2)
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
                    battle.main.defend()
                    tidusTurn = True
                elif screen.faintCheck() > 0:
                    battle.main.buddySwapKimahri()
                else:
                    battle.main.buddySwapYuna()
            elif screen.turnAuron():
                if not auronTurn:
                    battle.main.useSkill(0)
                    auronTurn = True
                elif screen.faintCheck() > 0:
                    battle.main.buddySwapYuna()
                else:
                    battle.main.defend()
            elif screen.turnAeon():
                battle.overdrive.valefor()
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
                battle.main.aeonSpell(1)
            elif memory.main.getOverdriveBattle(8) == 20:
                print("------Overdriving")
                battle.overdrive.valefor()
                went = True
            elif not turn1:
                turn1 = True
                print("------Recharge unsuccessful. Attempting recovery.")
                battle.main.aeonShield()
            elif lastTurn == 8:  # Valefor takes two turns in a row
                print("------Two turns in a row")
                battle.main.aeonShield()
            elif (
                nextHP > lastHP - 40 and not nextHP == lastHP
            ):  # Gravity spell was used
                print("------Gravity was used")
                battle.main.aeonShield()
            else:
                print("------Attack was just used. Now boost.")
                battle.main.aeonBoost()
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
    seymourTurn = 0
    if (
        memory.main.getOverdriveBattle(8) == 20
        or memory.main.getOverdriveBattle(1) == 100
    ):
        print("Gui2 - with extra Aeon overdrive")
        while memory.main.battleActive():
            if screen.turnSeymour() and seymourTurn < 2:
                battle.main.seymourSpell(targetFace=False)
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
                    battle.main.aeonSummon(0)
            elif screen.turnAeon():
                print("Firing")
                battle.overdrive.valefor()
            else:
                print("Defend")
                battle.main.defend()
    else:
        print("Gui2 - standard")
        while memory.main.battleActive():
            if memory.main.turnReady():
                if screen.turnSeymour():
                    battle.main.seymourSpell(targetFace=True)
                else:
                    battle.main.defend()

    while not memory.main.userControl():
        if memory.main.cutsceneSkipPossible():
            print("Intentional delay to get the cutscene skip to work.")
            memory.main.waitFrames(2)
            xbox.skipSceneSpec()
            memory.main.waitFrames(60)
        elif memory.main.diagSkipPossible() or memory.main.menuOpen():
            xbox.tapB()


def extractor():
    print("Fight start: Extractor")
    FFXC.set_neutral()

    screen.awaitTurn()
    battle.main.tidusHaste("none")

    screen.awaitTurn()
    battle.main.attack("none")  # Wakka attack

    screen.awaitTurn()
    battle.main.tidusHaste("l", character=4)

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
                battle.main.revive()
            elif screen.turnTidus():
                print(memory.main.getActorCoords(3))
                if tidusCheer:
                    cheerCount += 1
                    battle.main.cheer()
                elif (
                    memory.main.getEnemyCurrentHP()[0] < 1400
                    and not screen.faintCheck()
                    and memory.main.getOverdriveBattle(4) == 100
                ):
                    battle.main.defend()
                else:
                    battle.main.attack("none")
            else:
                if (
                    memory.main.getEnemyCurrentHP()[0] < 1900
                    and memory.main.getOverdriveBattle(4) == 100
                ):
                    battle.overdrive.wakka()
                else:
                    battle.main.attack("none")
        elif memory.main.diagSkipPossible():
            xbox.tapB()
    memory.main.clickToControl()


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
                    battle.main.equipInBattle(equipType="armor", abilityNum=0x8028)
                elif tidusturns == 1:
                    battle.main.defend()
                else:
                    battle.main.buddySwapRikku()
                tidusturns += 1
            elif turnchar == 1:
                rikkuslotnum = memory.main.getBattleCharSlot(6)
                if rikkuslotnum < 3 and partyHP[rikkuslotnum] == 0:
                    battle.main.revive()
                    yunaTurn = True
                elif not yunaTurn:
                    battle.main.defend()
                    yunaTurn = True
                elif not battle.main.spheriSpellItemReady():
                    if 5 not in memory.main.getActiveBattleFormation():
                        battle.main.buddySwapLulu()
                    elif 6 not in memory.main.getActiveBattleFormation():
                        battle.main.buddySwapRikku()
                    else:
                        battle.main.defend()
                elif 6 not in memory.main.getActiveBattleFormation():
                    battle.main.buddySwapRikku()
                else:
                    battle.main.defend()
                    yunaTurn = True
            elif turnchar == 3:
                rikkuslotnum = memory.main.getBattleCharSlot(6)
                if rikkuslotnum < 3 and partyHP[rikkuslotnum] == 0:
                    battle.main.revive()
                    kimTurn = True
                elif not kimTurn:
                    logs.writeRNGTrack("RNG11 before Spherimorph")
                    logs.writeRNGTrack(
                        memory.main.rngArrayFromIndex(index=11, arrayLen=30)
                    )
                    # if memory.main.nextStealRare(preAdvance=6):
                    # One each for Spherimorph, Negator, Crawler, and guados.
                    # Except we haven't learned Steal yet. That's no good.
                    #    _steal()
                    # else:
                    battle.main.defend()
                    kimTurn = True
                elif 6 not in memory.main.getActiveBattleFormation():
                    battle.main.buddySwapRikku()
                elif 5 not in memory.main.getActiveBattleFormation():
                    battle.main.buddySwapLulu()
                else:
                    battle.main.defend()
            elif turnchar == 5:
                if not battle.main.spheriSpellItemReady():
                    if spellNum == 1:
                        battle.main.ice()
                    elif spellNum == 2:
                        battle.main.water()
                    elif spellNum == 3:
                        battle.main.thunder()
                    else:
                        battle.main.fire()
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
                    battle.main.buddySwapRikku()
                else:
                    battle.main.defend()
            elif turnchar == 6:
                if rikkuturns == 0:
                    print("Throwing Grenade to check element")
                    grenadeslotnum = memory.main.getUseItemsSlot(35)
                    battle.main.useItem(grenadeslotnum, "none")
                    if memory.main.getCharWeakness(20) == 1:
                        spellNum = 4  # Ice
                    elif memory.main.getCharWeakness(20) == 2:
                        spellNum = 1  # Fire
                    elif memory.main.getCharWeakness(20) == 4:
                        spellNum = 3  # Water
                    elif memory.main.getCharWeakness(20) == 8:
                        spellNum = 2  # Thunder

                    # spellNum = screen.spherimorphSpell()
                elif not battle.main.spheriSpellItemReady():
                    if 5 not in memory.main.getActiveBattleFormation():
                        battle.main.buddySwapLulu()
                    else:
                        battle.main.defend()
                else:
                    print("Starting Rikkus overdrive")
                    # logs.writeStats("Spherimorph spell used:")
                    if spellNum == 1:
                        # ogs.writeStats("Fire")
                        print("Creating Ice")
                        battle.main.rikkuFullOD("spherimorph1")
                    elif spellNum == 2:
                        # logs.writeStats("Water")
                        print("Creating Water")
                        battle.main.rikkuFullOD("spherimorph2")
                    elif spellNum == 3:
                        # logs.writeStats("Thunder")
                        print("Creating Thunder")
                        battle.main.rikkuFullOD("spherimorph3")
                    elif spellNum == 4:
                        # logs.writeStats("Ice")
                        print("Creating Fire")
                        battle.main.rikkuFullOD("spherimorph4")

                rikkuturns += 1

    if not gameVars.csr():
        xbox.SkipDialog(5)


def crawler():
    print("Starting battle with Crawler")
    xbox.clickToBattle()

    if memory.main.nextStealRare(preAdvance=5):
        # One each for two Negators, Crawler, and guados.
        battle.main.negator_with_steal()
    else:
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
                        battle.main.buddySwapRikku()
                    else:
                        battle.main.defend()
                    tidusturns += 1
                elif turnchar == 6:
                    if luluturns < 2:
                        print("Using Lightning Marble")
                        lightningmarbleslot = memory.main.getUseItemsSlot(30)
                        if rikkuturns < 1:
                            battle.main.useItem(lightningmarbleslot, target=21)
                        else:
                            battle.main.useItem(lightningmarbleslot, target=21)
                    else:
                        print("Starting Rikkus overdrive")
                        battle.main.rikkuFullOD("crawler")
                    rikkuturns += 1
                elif turnchar == 3:
                    if kimahriturns == 0:
                        lightningmarbleslot = memory.main.getUseItemsSlot(30)
                        battle.main.useItem(lightningmarbleslot, target=21)
                    else:
                        battle.main.buddySwapYuna()
                    kimahriturns += 1
                elif turnchar == 5:
                    battle.main.revive()
                    luluturns += 1
                elif turnchar == 1:
                    if yunaturns == 0:
                        battle.main.defend()
                    else:
                        battle.main.buddySwapTidus()
                    yunaturns += 1
                else:
                    battle.main.defend()
            elif memory.main.diagSkipPossible():
                xbox.tapB()

    memory.main.clickToControl()


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

    screen.awaitTurn()

    while not memory.main.turnReady():
        pass
    while memory.main.battleActive():  # AKA end of battle screen
        if memory.main.turnReady():
            partyHP = memory.main.getBattleHP()
            turnchar = memory.main.getBattleCharTurn()
            tidusSlot = memory.main.getBattleCharSlot(0)

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
                    if (
                        battle.main.wendigoresheal(
                            turnchar=turnchar,
                            usepowerbreak=usepowerbreak,
                            tidusmaxHP=tidusmaxHP,
                        )
                        == 0
                    ):
                        xbox.weapSwap(0)
                    YunaAP = True
                # If Yuna has had a turn swap for Lulu
                else:
                    if 5 not in memory.main.getActiveBattleFormation():
                        print("Swapping to Lulu")
                        battle.main.buddySwapLulu()
                    elif 6 not in memory.main.getActiveBattleFormation():
                        battle.main.buddySwapRikku()
                    else:
                        xbox.weapSwap(0)
            elif turnchar == 0:
                if not tidushaste:
                    print("Tidus Haste self")
                    battle.main.tidusHaste("none")
                    tidushaste = True
                elif phase == 0:
                    print("Switch to Brotherhood")
                    battle.main.equipInBattle(special="brotherhood")
                    phase += 1
                elif phase == 1:
                    print("Attack top Guado")
                    battle.main.attackByNum(22, "d")
                    phase += 1
                elif (
                    memory.main.getEnemyCurrentHP()[1] != 0 and screen.faintCheck() == 2
                ):
                    print("2 Characters are dead")
                    tidushealself = True
                    if memory.main.getThrowItemsSlot(7) < 255:
                        battle.main.reviveAll()
                    elif memory.main.getThrowItemsSlot(6) < 255:
                        battle.main.revive()
                elif (
                    memory.main.getEnemyCurrentHP()[1] < 6000
                    and memory.main.getOverdriveBattle(0) == 100
                    and not gameVars.skipKilikaLuck()
                ):
                    battle.overdrive.tidus("left", character=21)
                elif tidushealself:
                    if partyHP[memory.main.getBattleCharSlot(0)] < tidusmaxHP:
                        print(
                            "Tidus just used Phoenix Down / Mega Phoenix so needs to heal himself"
                        )
                        if battle.main.fullheal(target=0, direction="l") == 0:
                            if screen.faintCheck():
                                print("No healing items so revive someone instead")
                                battle.main.revive()
                            else:
                                print("No healing items so just go face")
                                battle.main.attackByNum(21, "l")
                    else:
                        print("No need to heal. Ver 1")
                        battle.main.attackByNum(21, "l")
                    tidushealself = False
                else:
                    print("No need to heal. Ver 2")
                    battle.main.attackByNum(21, "l")
                memory.main.waitFrames(30 * 0.2)
            elif turnchar == 6:
                if phase == 2:
                    phase += 1
                    lightcurtainslot = memory.main.getUseItemsSlot(57)
                    if lightcurtainslot < 255:
                        print("Using Light Curtain on Tidus")
                        battle.main.useItem(lightcurtainslot, target=0)
                    else:
                        print("No Light Curtain")
                        print("Swapping to Auron to Power Break")
                        battle.main.buddySwapAuron()  # Swap for Auron
                        powerbreak = True
                        usepowerbreak = True
                # elif memory.main.getEnemyCurrentHP()[1] < stopHealing:
                #    defend()
                elif (
                    battle.main.wendigoresheal(
                        turnchar=turnchar,
                        usepowerbreak=usepowerbreak,
                        tidusmaxHP=tidusmaxHP,
                    )
                    == 0
                ):
                    if not guadosteal and memory.main.getEnemyCurrentHP().count(0) != 2:
                        battle.main.Steal()
                        guadosteal = True
                    # elif memory.main.getEnemyCurrentHP().count(0) == 2 and not 5 in memory.main.getActiveBattleFormation():
                    #    buddySwapLulu()
                    else:
                        battle.main.defend()
            elif turnchar == 2:
                if usepowerbreak:
                    print("Using Power Break")
                    battle.main.useSkill(position=0, target=21)
                    powerbreakused = True
                    usepowerbreak = False
                # elif memory.main.getEnemyCurrentHP()[1] < stopHealing and memory.main.getBattleHP()[tidusSlot] != 0:
                #    defend()
                elif (
                    battle.main.wendigoresheal(
                        turnchar=turnchar,
                        usepowerbreak=usepowerbreak,
                        tidusmaxHP=tidusmaxHP,
                    )
                    == 0
                ):
                    battle.main.buddySwapKimahri()
            elif turnchar == 5:
                if (
                    battle.main.wendigoresheal(
                        turnchar=turnchar,
                        usepowerbreak=usepowerbreak,
                        tidusmaxHP=tidusmaxHP,
                    )
                    == 0
                ):
                    xbox.weapSwap(0)
            else:
                if (
                    usepowerbreak
                    and not powerbreakused
                    and 2 not in memory.main.getActiveBattleFormation()
                ):
                    print("Swapping to Auron to Power Break")
                    battle.main.buddySwapAuron()
                # if memory.main.getEnemyCurrentHP()[1] < stopHealing and memory.main.getBattleHP()[tidusSlot] != 0:
                #    print("End of battle, no need to heal.")
                #    defend()
                elif (
                    memory.main.getEnemyCurrentHP()[1] != 0
                    and memory.main.getBattleHP()[tidusSlot] != 0
                ):
                    if (
                        battle.main.wendigoresheal(
                            turnchar=turnchar,
                            usepowerbreak=usepowerbreak,
                            tidusmaxHP=tidusmaxHP,
                        )
                        == 0
                    ):
                        battle.main.defend()
                else:
                    battle.main.defend()


# Process written by CrimsonInferno
def evrae():
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
                        battle.main.tidusHaste("none")
                    elif tidusPrep in [1, 2]:
                        tidusPrep += 1
                        battle.main.cheer()
                    elif (
                        tidusAttacks == 4 or memory.main.getEnemyCurrentHP()[0] <= 9999
                    ):
                        tidusAttacks += 1
                        battle.overdrive.tidus()
                    else:
                        tidusAttacks += 1
                        battle.main.attack("none")
                elif gameVars.getBlitzWin():  # Blitz win logic
                    if tidusPrep == 0:
                        tidusPrep = 1
                        battle.main.tidusHaste("none")
                    elif tidusPrep == 1:
                        tidusPrep += 1
                        battle.main.cheer()
                    elif tidusPrep == 2 and rikkuTurns == 0:
                        tidusPrep += 1
                        battle.main.equipInBattle(equipType="armor", abilityNum=0x8028)
                    elif tidusPrep == 2 and tidusAttacks == 2:
                        tidusPrep += 1
                        battle.main.cheer()
                    else:
                        tidusAttacks += 1
                        battle.main.attack("none")
                else:  # Blitz loss logic
                    if tidusPrep == 0:
                        tidusPrep = 1
                        battle.main.tidusHaste("none")
                    elif tidusPrep <= 2:
                        tidusPrep += 1
                        battle.main.cheer()
                    elif tidusPrep == 3:
                        print("Equip Baroque Sword.")
                        battle.main.equipInBattle(special="baroque")
                        tidusPrep += 1
                    elif tidusAttacks == 4 and gameVars.skipKilikaLuck():
                        tidusAttacks += 1
                        battle.overdrive.tidus()
                    else:
                        tidusAttacks += 1
                        battle.main.attack("none")
            elif turnchar == 6:
                print("Registering Rikkus turn")
                if rikkuTurns == 0:
                    rikkuTurns += 1
                    print("Rikku overdrive")
                    battle.main.rikkuFullOD("Evrae")
                elif not gameVars.getBlitzWin() and not lunarCurtain:
                    print("Use Lunar Curtain")
                    lunarSlot = memory.main.getUseItemsSlot(56)
                    battle.main.useItem(lunarSlot, direction="l", target=0)
                    lunarCurtain = True
                elif memory.main.getBattleHP()[
                    memory.main.getBattleCharSlot(0)
                ] < 1520 and (tidusAttacks < 3 or not gameVars.getBlitzWin()):
                    print("Rikku should attempt to heal a character.")
                    kimahriTurns += 1
                    if battle.main.fullheal(target=0, direction="d") == 0:
                        print("Restorative item not found.")
                        battle.main.useItem(memory.main.getUseItemsSlot(20))
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
                        battle.main.Steal()
                    else:
                        battle.main.useItem(throwSlot)
                else:
                    battle.main.Steal()
                    stealCount += 1
            elif turnchar == 3:
                print("Registering Kimahri's turn")
                if not gameVars.getBlitzWin() and not lunarCurtain:
                    print("Use Lunar Curtain")
                    lunarSlot = memory.main.getUseItemsSlot(56)
                    battle.main.useItem(lunarSlot, direction="l", target=0)
                    lunarCurtain = True
                elif memory.main.getBattleHP()[
                    memory.main.getBattleCharSlot(0)
                ] < 1520 and (tidusAttacks < 3 or not gameVars.getBlitzWin()):
                    print("Kimahri should attempt to heal a character.")
                    kimahriTurns += 1
                    if battle.main.fullheal(target=0, direction="u") == 0:
                        print("Restorative item not found.")
                        battle.main.useItem(memory.main.getUseItemsSlot(20))
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
                        battle.main.Steal()
                    else:
                        battle.main.useItem(throwSlot)
                else:
                    battle.main.Steal()
                    stealCount += 1
        elif memory.main.diagSkipPossible():
            xbox.tapB()

    if not gameVars.csr():
        while not memory.main.cutsceneSkipPossible():
            if memory.main.menuOpen():
                xbox.tapB()
        xbox.skipSceneSpec()


def isaaru():
    xbox.clickToBattle()
    if memory.main.getEncounterID() < 258:
        gameVars.addRescueCount()

    while memory.main.battleActive():  # AKA end of battle screen
        if memory.main.turnReady():
            if screen.turnYuna():
                if memory.main.getEncounterID() in [257, 260]:
                    battle.main.aeonSummon(2)  # Summon Ixion for Bahamut
                else:
                    battle.main.aeonSummon(4)  # Summon Bahamut for other aeons
            else:
                battle.main.attack("none")  # Aeon turn
        elif memory.main.diagSkipPossible():
            xbox.tapB()
    FFXC.set_value("BtnB", 1)
    memory.main.waitFrames(30 * 2.8)
    FFXC.set_value("BtnB", 0)


def evraeAltana():
    xbox.clickToBattle()
    if memory.main.getEncounterID() != 266:
        print("Not Evrae this time.")
        battle.main.fleeAll()
    else:
        print("Evrae Altana fight start")
        if memory.main.nextStealRare():
            battle.main.evraeAltanaSteal()
        else:
            print("=======================================")
            print("Next steal will crit, do not steal.")
            print("=======================================")
        thrownItem = False
        while memory.main.battleActive():  # AKA end of battle screen
            if memory.main.turnReady():
                if memory.main.getItemSlot(18) != 255 and not thrownItem:
                    battle.main._useHealingItem(itemID=18)
                    thrownItem = True
                elif memory.main.getItemSlot(16) != 255 and not thrownItem:
                    battle.main._useHealingItem(itemID=16)
                    thrownItem = True
                else:
                    battle.main.altanaheal()

    memory.main.clickToControl()


def seymourNatus():
    aeonSummoned = False
    while not memory.main.userControl():
        if memory.main.getEncounterID() == 272:  # Seymour Natus
            print("Seymour Natus engaged")
            while not memory.main.battleComplete():
                if memory.main.turnReady():
                    if screen.turnTidus():
                        if memory.main.getLuluSlvl() < 35 or gameVars.nemesis():
                            battle.main.buddySwapLulu()
                            screen.awaitTurn()
                            xbox.weapSwap(0)
                        elif aeonSummoned:
                            battle.main.tidusHaste("d", character=1)
                        else:
                            battle.main.attack("none")
                    elif screen.turnLulu():
                        battle.main.buddySwapTidus()
                        screen.awaitTurn()
                        xbox.tapUp()
                        battle.main.attack("none")
                    elif screen.turnYuna():
                        if not aeonSummoned:
                            battle.main.aeonSummon(4)
                            aeonSummoned = True
                        else:
                            battle.main.aeonSummon(2)
                    elif screen.turnAeon():
                        xbox.SkipDialog(3)  # Finishes the fight.
                    else:
                        battle.main.defend()
            return 1
        elif memory.main.getEncounterID() == 270:  # YAT-63 x2
            while memory.main.battleActive():
                if gameVars.completedRescueFights():
                    battle.main.fleeAll()
                elif memory.main.turnReady():
                    if screen.turnTidus() or screen.turnYuna():
                        if memory.main.getEnemyCurrentHP().count(0) == 1:
                            battle.main.fleeAll()
                            gameVars.addRescueCount()
                        else:
                            battle.main.attackByNum(22, "r")
                    else:
                        battle.main.defend()
        elif memory.main.getEncounterID() == 269:  # YAT-63 with two guard guys
            while memory.main.battleActive():
                if gameVars.completedRescueFights():
                    battle.main.fleeAll()
                elif memory.main.turnReady():
                    if screen.turnTidus() or screen.turnYuna():
                        if memory.main.getEnemyCurrentHP().count(0) == 1:
                            battle.main.fleeAll()
                            gameVars.addRescueCount()
                        else:
                            battle.main.attack("none")
                    else:
                        battle.main.defend()
        elif memory.main.getEncounterID() == 271:  # one YAT-63, two YAT-99
            while memory.main.battleActive():
                if gameVars.completedRescueFights():
                    battle.main.fleeAll()
                elif memory.main.turnReady():
                    if screen.turnTidus() or screen.turnYuna():
                        if memory.main.getEnemyCurrentHP().count(0) == 1:
                            battle.main.fleeAll()
                            gameVars.addRescueCount()
                        else:
                            battle.main.attackByNum(21, "l")
                    else:
                        battle.main.defend()
        if memory.main.menuOpen() or memory.main.diagSkipPossible():
            xbox.tapB()
    return 0


def biranYenke():
    xbox.clickToBattle()
    battle.main.Steal()

    # Nemesis logic
    if gameVars.nemesis():
        screen.awaitTurn()
        battle.main.StealRight()

    screen.awaitTurn()
    gemSlot = memory.main.getUseItemsSlot(34)
    if gemSlot == 255:
        gemSlot = memory.main.getUseItemsSlot(28)
    battle.main.useItem(gemSlot, "none")

    xbox.clickToBattle()
    gemSlot = memory.main.getUseItemsSlot(34)
    if gemSlot == 255:
        gemSlot = memory.main.getUseItemsSlot(28)
    battle.main.useItem(gemSlot, "none")

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
    bahamut_crit = memory.main.nextCrit(character=7, charLuck=17, enemyLuck=15)
    print("Next Aeon Crit:", bahamut_crit)
    yunaXP = memory.main.getSLVLYuna()
    xbox.clickToBattle()
    if bahamut_crit == 2:
        while not memory.main.battleComplete():
            if memory.main.turnReady():
                if screen.turnAeon():
                    battle.main.attack("none")
                elif screen.turnYuna():
                    battle.main.aeonSummon(4)
                else:
                    battle.main.defend()
    elif gameVars.endGameVersion() == 3:
        bahamutSummoned = False
        while not memory.main.battleComplete():  # AKA end of battle screen
            if memory.main.turnReady():
                if screen.turnTidus():
                    battle.main.buddySwapYuna()
                elif screen.turnYuna():
                    if not bahamutSummoned:
                        battle.main.aeonSummon(4)
                        bahamutSummoned = True
                    else:
                        battle.main.attack("none")
                elif screen.turnAeon():
                    if gameVars.getBlitzWin():
                        battle.main.attack("none")
                    else:
                        battle.main.impulse()
                elif screen.faintCheck() >= 1:
                    battle.main.revive()
                else:
                    battle.main.defend()
    else:
        while not memory.main.battleComplete():  # AKA end of battle screen
            if memory.main.turnReady():
                lastHP = memory.main.getEnemyCurrentHP()[0]
                print("Last HP")
                if screen.turnYuna():
                    print("Yunas turn. Stage:", stage)
                    if stage == 1:
                        battle.main.attack("none")
                        stage += 1
                    elif stage == 2:
                        battle.main.aeonSummon(4)
                        battle.main.attack("none")
                        stage += 1
                    else:
                        battle.main.attack("none")
                elif screen.turnTidus():
                    print("Tidus' turn. Stage:", stage)
                    if stage < 3:
                        battle.main.tidusHaste("down", character=1)
                    elif lastHP > 3500:
                        battle.main.attack("none")
                    else:
                        battle.main.defend()
                elif screen.turnAuron():
                    print("Auron's turn. Swap for Rikku and overdrive.")
                    battle.main.buddySwapRikku()
                    print("Rikku overdrive")
                    battle.main.rikkuFullOD("Flux")
                else:
                    print("Non-critical turn. Defending.")
                    battle.main.defend()
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
    bahamut_crit = memory.main.nextCrit(character=7, charLuck=17, enemyLuck=15)
    print("Next Aeon Crit:", bahamut_crit)
    xbox.clickToBattle()
    bahamut_crit = memory.main.nextCrit(character=7, charLuck=17, enemyLuck=15)
    print("Next Aeon Crit:", bahamut_crit)
    if bahamut_crit == 2 or bahamut_crit == 7:
        while not memory.main.battleComplete():
            if memory.main.turnReady():
                bahamut_crit = memory.main.nextCrit(
                    character=7, charLuck=17, enemyLuck=15
                )
                print("Next Aeon Crit:", bahamut_crit)
                if screen.turnAeon():
                    battle.main.attack("none")
                elif screen.turnYuna():
                    battle.main.aeonSummon(4)
                else:
                    battle.main.defend()
    elif gameVars.endGameVersion() == 3 and gameVars.getBlitzWin():
        while not memory.main.battleComplete():
            if memory.main.turnReady():
                bahamut_crit = memory.main.nextCrit(
                    character=7, charLuck=17, enemyLuck=15
                )
                print("Next Aeon Crit:", bahamut_crit)
                if screen.turnYuna():
                    battle.main.aeonSummon(4)
                elif screen.turnAeon():
                    battle.main.attack("none")
                else:
                    battle.main.defend()
    else:
        armorBreak = False
        while not memory.main.battleComplete():
            if memory.main.turnReady():
                bahamut_crit = memory.main.nextCrit(
                    character=7, charLuck=17, enemyLuck=15
                )
                print("Next Aeon Crit:", bahamut_crit)
                if screen.turnTidus():
                    battle.main.useSkill(0)
                    armorBreak = True
                elif screen.turnYuna():
                    if armorBreak:
                        battle.main.aeonSummon(4)
                    else:
                        battle.main.defend()
                elif screen.turnAeon():
                    battle.main.attack("none")
                else:
                    battle.main.defend()
    memory.main.clickToControl()


def omnis():
    print("Fight start: Seymour Omnis")
    xbox.clickToBattle()
    battle.main.defend()  # Yuna defends
    rikkuIn = False
    backupCure = False

    while memory.main.getEnemyMaxHP()[0] == memory.main.getEnemyCurrentHP()[0]:
        if memory.main.turnReady():
            if screen.turnTidus():
                battle.main.useSkill(0)
            elif screen.turnAuron():
                battle.main.buddySwapRikku()
                battle.main.rikkuFullOD(battle="omnis")
                rikkuIn = True
            elif screen.turnYuna() and rikkuIn:
                if not backupCure:
                    battle.main.yunaCureOmnis()
                    backupCure = True
                else:
                    battle.main.equipInBattle(
                        equipType="weap", abilityNum=0x8001, character=1
                    )
            else:
                battle.main.defend()

    print("Ready for aeon.")
    while not memory.main.battleComplete():  # AKA end of battle screen
        if memory.main.turnReady():
            print("Character turn:", memory.main.getBattleCharTurn())
            if screen.turnYuna():
                battle.main.aeonSummon(4)
            elif screen.turnAeon():
                battle.main.attack("none")
            elif screen.turnTidus():
                battle.main.attack("none")
            else:
                battle.main.defend()
        elif memory.main.diagSkipPossible():
            print("Skipping dialog maybe?")
            xbox.tapB()
    print("Should be done now.")
    memory.main.clickToControl()


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
    battle.main.buddySwapRikku()
    if memory.main.overdriveState()[6] == 100:
        battle.main.rikkuFullOD("bfa")
    else:
        battle.main.useSkill(0)

    screen.awaitTurn()
    while memory.main.mainBattleMenu():
        xbox.tapLeft()
    while memory.main.battleCursor2() != 1:
        xbox.tapDown()
    while memory.main.otherBattleMenu():
        xbox.tapB()
    battle.main.tapTargeting()
    battle.main.buddySwapYuna()
    battle.main.aeonSummon(4)

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
                battle.main.calculateSpareChangeMovement(useGil)
                while memory.main.spareChangeOpen():
                    xbox.tapB()
                while not memory.main.mainBattleMenu():
                    xbox.tapB()
            else:
                battle.main.defend()
        elif not memory.main.battleActive():
            xbox.tapB()


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
                    battle.main.equipInBattle(
                        equipType="weap", abilityNum=0x8032, character=1
                    )
                    weapSwap = True
                elif screen.turnYuna():
                    battle.main.attack("none")
                    zombieAttack = True
                elif weapSwap and not zombieAttack and screen.turnTidus():
                    xbox.weapSwap(0)
                else:
                    battle.main.defend()
            elif zaChar == 0 and not zombieAttack:  # Tidus logic:
                if screen.turnYuna():
                    battle.main.defend()
                elif screen.turnTidus() and not weapSwap:
                    battle.main.equipInBattle(
                        equipType="weap", abilityNum=0x8032, character=0
                    )
                    weapSwap = True
                elif screen.turnTidus():
                    battle.main.attack("none")
                    zombieAttack = True
                else:
                    battle.main.defend()
            elif zaChar == 2 and not zombieAttack:  # Auron logic:
                if screen.turnYuna():
                    battle.main.buddySwapAuron()
                elif screen.turnAuron() and not weapSwap:
                    battle.main.equipInBattle(
                        equipType="weap", abilityNum=0x8032, character=2
                    )
                    weapSwap = True
                elif screen.turnAuron():
                    battle.main.attack("none")
                    zombieAttack = True
                else:
                    battle.main.defend()
            elif zaChar == 6 and not zombieAttack:  # Rikku logic:
                if screen.turnYuna() and not weapSwap:
                    # Piggy back off the weapSwap function
                    battle.main.defend()
                    weapSwap = True
                elif screen.turnYuna():
                    xbox.weapSwap(0)
                elif screen.turnTidus():
                    battle.main.tidusHaste("r", character=6)
                elif screen.turnRikku():
                    battle.main.attack("none")
                    zombieAttack = True
                else:
                    battle.main.defend()
            elif zombieAttack:  # Throw P.down to end game
                itemNum = battle.main.yuYevonItem()
                if itemNum == 99:
                    battle.main.attack("none")
                else:
                    while memory.main.battleMenuCursor() != 1:
                        xbox.tapDown()
                    while memory.main.mainBattleMenu():
                        xbox.tapB()
                    itemPos = memory.main.getThrowItemsSlot(itemNum)
                    battle.main._navigate_to_position(itemPos)
                    while memory.main.otherBattleMenu():
                        xbox.tapB()
                    while not memory.main.enemyTargetted():
                        xbox.tapUp()
                    battle.main.tapTargeting()
                print("Phoenix Down on Yu Yevon. Good game.")
            elif screen.turnTidus() and zaChar == 255:
                # Tidus to use Zombie Strike ability
                battle.main.useSkill(0)
                zombieAttack = True
            elif zaChar == 255 and not screen.turnTidus():
                # Non-Tidus char to defend so Tidus can use Zombie Strike ability
                battle.main.defend()
            else:
                if memory.main.getBattleCharTurn() == zaChar:
                    battle.main.attack("none")
                    zombieAttack = True
                elif memory.main.getBattleCharSlot(zaChar) >= 3:
                    battle.main.buddySwap_char(zaChar)
                elif screen.turnTidus():
                    battle.main.tidusHaste("l", character=zaChar)
                else:
                    battle.main.defend()
        elif not memory.main.battleActive():
            xbox.tapB()
