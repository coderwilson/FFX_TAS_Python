import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory
import FFX_targetPathing
import FFX_vars
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()


def printNEAzone(battles: int):
    print("#### Charging Rikku zone:", gameVars.getNEAzone())
    print("#### This will take", battles, "number of battles (99 means unknown)")


def decideNEA(bonusAdvance: int = 0):
    import FFX_rngTrack
    maxBattles = 1
    zanOutdoors = FFX_rngTrack.comingBattles(area="zanarkand_(overpass)", battleCount=maxBattles, extraAdvances=bonusAdvance)
    zanIndoors = FFX_rngTrack.comingBattles(area="zanarkand_(dome)", battleCount=maxBattles, extraAdvances=bonusAdvance)
    seaSorrows = FFX_rngTrack.comingBattles(area="inside_sin_(front)", battleCount=maxBattles, extraAdvances=bonusAdvance + 6)

    for i in range(maxBattles):
        if "behemoth" in zanOutdoors[i]:
            gameVars.setNEAzone(1)
            printNEAzone(i + 1)
            return
        elif "defender_z" in zanIndoors[i]:
            gameVars.setNEAzone(2)
            printNEAzone(i + 1)
            return
        elif "behemoth_king" in seaSorrows[i]:
            gameVars.setNEAzone(3)
            printNEAzone(i + 1)
            return
        elif "adamantoise" in seaSorrows[i]:
            gameVars.setNEAzone(3)
            printNEAzone(i + 1)
            return
    # If we won't get it in next five per zone, default to Inside Sin. The most possible battles there.
    gameVars.setNEAzone(99)
    printNEAzone(99)
    return


def arrival():
    FFX_memory.awaitControl()
    decideNEA()
    # Starts from the map just after the fireplace chat.
    reEquipNE = False
    if FFX_memory.overdriveState2()[6] != 100 and gameVars.getNEAzone() == 1:
        FFX_memory.fullPartyFormat('rikku', fullMenuClose=False)
        FFX_menu.equipArmor(character=gameVars.neArmor(), ability=99)
        reEquipNE = True

    print("Outdoor Zanarkand pathing section")
    while FFX_memory.getMap() != 225:
        if FFX_memory.userControl():
            if FFX_memory.getCoords()[1] > -52:
                FFX_targetPathing.setMovement([103, -54])
            elif FFX_memory.getCoords()[0] < 172:
                FFX_targetPathing.setMovement([176, -118])
            else:
                FFXC.set_movement(-1, 1)
        else:
            FFXC.set_neutral()

    fortuneSlot = FFX_memory.getItemSlot(74)
    if fortuneSlot == 255:
        fortuneCount = 0
    else:
        fortuneCount = FFX_memory.getItemCountSlot(fortuneSlot)

    checkpoint = 0
    while FFX_memory.getMap() != 314:
        if FFX_memory.userControl():
            if checkpoint == 4:  # First chest
                fortuneSlot = FFX_memory.getItemSlot(74)
                if fortuneSlot == 255:
                    fortuneCount = 0
                    FFXC.set_movement(-1, 1)
                    FFX_Xbox.tapB()
                else:
                    if FFX_memory.getItemCountSlot(fortuneSlot) > fortuneCount:
                        checkpoint += 1
                        FFX_memory.clickToControl()
                    else:
                        FFXC.set_movement(-1, 1)
                        FFX_Xbox.tapB()
            elif FFX_targetPathing.setMovement(FFX_targetPathing.zanarkandOutdoors(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()

            if FFX_Screen.BattleScreen():
                FFX_Battle.chargeRikkuOD()
                if reEquipNE and FFX_memory.overdriveState2()[6] == 100:
                    reEquipNE = False
                    FFX_memory.clickToControl()
                    FFX_memory.fullPartyFormat('yuna', fullMenuClose=False)
                    FFX_menu.equipArmor(
                        character=gameVars.neArmor(), ability=0x801D)
                    FFX_memory.closeMenu()
            elif FFX_memory.diagSkipPossible() and not FFX_memory.battleActive():
                FFX_Xbox.tapB()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()

    # Outside the dome
    print("Now approaching the Blitz dome.")
    print("Close observation will reveal this is the same blitz dome")
    print("as the one from the opening of the game.")
    while FFX_memory.getMap() != 222:
        FFXC.set_movement(0, 1)
        FFX_Xbox.tapB()

    print("Start of Zanarkand Dome section")
    friendSlot = FFX_memory.getItemSlot(97)
    if friendSlot == 255:
        friendCount = 0
    else:
        friendCount = FFX_memory.getItemCountSlot(friendSlot)

    luckSlot = FFX_memory.getItemSlot(94)
    if luckSlot == 255:
        friendCount = 0
    else:
        luckCount = FFX_memory.getItemCountSlot(luckSlot)

    if FFX_memory.overdriveState2()[6] != 100 and gameVars.getNEAzone() == 2:
        FFX_memory.fullPartyFormat('rikku', fullMenuClose=False)
        FFX_menu.equipArmor(character=gameVars.neArmor(), ability=99)
        reEquipNE = True

    checkpoint = 0
    while FFX_memory.getMap() != 320:
        if FFX_memory.userControl():
            if checkpoint == 13:  # Second chest
                friendSlot = FFX_memory.getItemSlot(97)
                if friendSlot == 255:
                    friendCount = 0
                    FFX_targetPathing.setMovement([8, 90])
                    FFX_memory.waitFrames(1)
                    FFX_Xbox.tapB()
                else:
                    if FFX_memory.getItemCountSlot(friendSlot) > friendCount:
                        checkpoint += 1
                        FFX_memory.clickToControl()
                    else:
                        FFX_targetPathing.setMovement([8, 90])
                        FFX_memory.waitFrames(1)
                        FFX_Xbox.tapB()
            elif checkpoint == 24:  # Third chest
                luckSlot = FFX_memory.getItemSlot(94)
                if luckSlot == 255:
                    luckCount = 0
                    FFXC.set_movement(1, 1)
                    FFX_Xbox.tapB()
                else:
                    if FFX_memory.getItemCountSlot(luckSlot) > luckCount:
                        checkpoint += 1
                        print("Updating checkpoint:", checkpoint)
                        FFX_memory.clickToControl()
                    else:
                        FFXC.set_movement(1, 1)
                        FFX_Xbox.tapB()
            elif checkpoint == 29:  # Save sphere
                FFX_memory.touchSaveSphere()
                checkpoint += 1
            elif FFX_memory.getMap() == 316 and checkpoint < 21:  # Final room before trials
                print("Final room before trials")
                checkpoint = 21
            elif FFX_targetPathing.setMovement(FFX_targetPathing.zanarkandDome(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_Screen.BattleScreen():
                FFX_Battle.chargeRikkuOD()
                if reEquipNE and FFX_memory.overdriveState2()[6] == 100:
                    reEquipNE = False
                    FFX_memory.clickToControl()
                    FFX_memory.fullPartyFormat('yuna', fullMenuClose=False)
                    FFX_menu.equipArmor(
                        character=gameVars.neArmor(), ability=0x801D)
                    FFX_memory.closeMenu()
            elif FFX_memory.diagSkipPossible() and not FFX_memory.battleActive():
                FFX_Xbox.tapB()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()


def trials():
    checkpoint = 0
    while checkpoint < 89:
        checkpoint = trials0(checkpoint)
        checkpoint = trials1(checkpoint)
        checkpoint = trials2(checkpoint)
        checkpoint = trials3(checkpoint)
        checkpoint = trials4(checkpoint)


def trials0(checkpoint):
    FFX_memory.awaitControl()

    while checkpoint < 9:
        if FFX_memory.userControl():
            if checkpoint == 8:
                FFXC.set_movement(-1, 0)
                while FFX_memory.userControl():
                    FFX_Xbox.tapB()
                FFXC.set_movement(0, 1)
                FFX_memory.waitFrames(30 * 0.2)
                FFX_memory.awaitControl()
                FFX_memory.waitFrames(30 * 1.3)
                FFXC.set_movement(0, 1)
                checkpoint += 1
            elif FFX_targetPathing.setMovement(FFX_targetPathing.zanarkandTrials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
    return checkpoint


def trials1(checkpoint):
    FFX_memory.awaitControl()

    while checkpoint < 31:
        if FFX_memory.userControl():
            if checkpoint == 20:
                FFXC.set_movement(-1, 1)
                FFX_memory.clickToEvent()
                FFXC.set_neutral()
                FFX_Xbox.SkipDialog(0.5)
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 26 or checkpoint == 28:
                FFXC.set_movement(-1, -1)
                FFX_memory.clickToEvent()
                FFXC.set_neutral()
                FFX_Xbox.SkipDialog(0.5)
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 30:
                FFXC.set_movement(0, 1)
                FFX_memory.awaitEvent()
                FFX_memory.waitFrames(30 * 0.2)
                FFXC.set_neutral()
                checkpoint += 1
            elif FFX_targetPathing.setMovement(FFX_targetPathing.zanarkandTrials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
    return checkpoint


def trials2(checkpoint):
    FFX_memory.awaitControl()

    while checkpoint < 49:
        if FFX_memory.userControl():
            if checkpoint == 46:
                FFXC.set_movement(1, 0)
                FFX_memory.clickToEvent()
                FFXC.set_neutral()
                FFX_Xbox.SkipDialog(0.5)
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 48:
                FFXC.set_movement(-1, 1)
                FFX_memory.awaitEvent()
                FFX_memory.waitFrames(30 * 0.2)
                FFXC.set_neutral()
                checkpoint += 1
            elif FFX_targetPathing.setMovement(FFX_targetPathing.zanarkandTrials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
    return checkpoint


def trials3(checkpoint):
    FFX_memory.awaitControl()

    while checkpoint < 69:
        if FFX_memory.userControl():
            if checkpoint == 66:
                FFXC.set_movement(1, 0)
                FFX_memory.clickToEvent()
                FFXC.set_neutral()
                FFX_Xbox.SkipDialog(0.7)
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 68:
                FFXC.set_movement(-1, 1)
                FFX_memory.awaitEvent()
                FFX_memory.waitFrames(30 * 0.2)
                FFXC.set_neutral()
                checkpoint += 1
            elif FFX_targetPathing.setMovement(FFX_targetPathing.zanarkandTrials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
    return checkpoint


def trials4(checkpoint):
    FFX_memory.awaitControl()

    while checkpoint < 89:
        if FFX_memory.userControl():
            if checkpoint == 81:
                FFXC.set_movement(0, 1)
                FFX_memory.clickToEvent()
                FFXC.set_neutral()
                FFX_Xbox.SkipDialog(0.5)
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 87:
                while FFX_memory.userControl():
                    FFX_targetPathing.setMovement([141, 1])
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif FFX_targetPathing.setMovement(FFX_targetPathing.zanarkandTrials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
    FFXC.set_neutral()
    return checkpoint


def sanctuaryKeeper():
    ver = gameVars.endGameVersion()
    print("Now prepping for Sanctuary Keeper fight")

    if ver == 4:
        print("Pattern for four return spheres off of the B&Y fight")
        FFX_menu.skReturn()
    elif ver == 3:
        FFX_menu.skFriend()
    else:
        FFX_menu.skMixed()
    FFX_memory.fullPartyFormat('yuna')
    FFX_memory.closeMenu()

    while not FFX_targetPathing.setMovement([110, 20]):
        pass
    FFXC.set_movement(-1, 1)
    FFX_memory.awaitEvent()
    FFX_Xbox.clickToBattle()
    if FFX_Screen.turnTidus():
        FFX_Battle.defend()
        FFX_Xbox.clickToBattle()
    FFX_Battle.aeonSummon(4)  # This is the whole fight. Kinda sad.
    FFX_memory.clickToControl()


def yunalesca():
    ver = gameVars.endGameVersion()
    while not FFX_targetPathing.setMovement([-2, -179]):
        if FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()

    if ver == 4:
        print("Final pattern for four return spheres off of the B&Y fight")
        FFX_menu.skReturn2()
        FFX_memory.closeMenu()
    else:
        print("No further sphere gridding needed at this time.")

    print("Sphere grid is done. Moving on to storyline and eventually Yunalesca.")

    FFX_memory.touchSaveSphere()

    checkpoint = 0
    # Gets us to Yunalesca battle through multiple rooms.
    while not FFX_memory.battleActive():
        if FFX_memory.menuOpen():
            FFX_memory.closeMenu()
        elif FFX_memory.userControl():
            if checkpoint in [2, 4]:
                FFXC.set_movement(0, 1)
                FFX_memory.awaitEvent()
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
            elif FFX_targetPathing.setMovement(FFX_targetPathing.yunalesca(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            FFXC.set_value('BtnB', 1)
            FFXC.set_value('BtnA', 1)
            FFX_memory.waitFrames(1)
            FFXC.set_value('BtnB', 0)
            FFXC.set_value('BtnA', 0)
            FFX_memory.waitFrames(1)
    FFX_Xbox.clickToBattle()
    FFX_Battle.aeonSummon(4)  # Summon Bahamut and attack.
    FFX_memory.clickToControl()  # This does all the attacking and dialog skipping

    # Now to check for zombie strike and then report to logs.
    print("Ready to check for Zombiestrike")
    FFX_Logs.writeStats("Zombiestrike:")
    FFX_Logs.writeStats(gameVars.zombieWeapon())
    print("++Zombiestrike:")
    print("++", gameVars.zombieWeapon())


def post_Yunalesca(checkpoint=0):
    print("Heading back outside.")
    FFXC.set_neutral()
    if gameVars.nemesis():
        FFX_menu.equipWeapon(character=0, ability=0x807A, fullMenuClose=True)
    FFX_memory.waitFrames(2)
    while FFX_memory.getMap() != 194:
        if FFX_memory.userControl():
            if checkpoint < 2 and FFX_memory.getMap() == 319:  # Back to room before Yunalesca
                checkpoint = 2
                print("Checkpoint reached:", checkpoint)
            elif checkpoint < 4 and FFX_memory.getMap() == 318:  # Exit to room with the inert Aeon
                checkpoint = 4
                print("Checkpoint reached:", checkpoint)
            elif checkpoint == 7:
                FFX_memory.touchSaveSphere()
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
            elif checkpoint < 10 and FFX_memory.getMap() == 320:  # Back to larger of the puzzle rooms
                checkpoint = 10
                print("Checkpoint reached:", checkpoint)
            elif checkpoint < 18 and FFX_memory.getMap() == 316:  # Hallway before puzzle rooms
                checkpoint = 18
                print("Checkpoint reached:", checkpoint)
            elif checkpoint < 25 and FFX_memory.getMap() == 315:  # Hallway before puzzle rooms
                checkpoint = 25
                print("Checkpoint reached:", checkpoint)
            elif checkpoint == 26:
                FFXC.set_neutral()
            elif FFX_targetPathing.setMovement(FFX_targetPathing.yunalescaToAirship(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_Screen.BattleScreen():
                FFX_Battle.fleeAll()
            elif FFX_memory.diagSkipPossible() and not FFX_memory.battleActive():
                FFX_Xbox.tapB()
            elif FFX_memory.cutsceneSkipPossible():
                print(FFX_memory.getCutsceneID())
                if FFX_memory.getCutsceneID() == (5673, 2850, 3):
                    FFX_memory.waitFrames(10)
                    FFX_Xbox.skipScene()
