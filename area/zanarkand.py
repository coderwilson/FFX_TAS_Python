import xbox
import screen
import battle.main
import menu
import logs
import memory.main
import targetPathing
import vars
import rngTrack
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def printNEAzone(battles: int):
    print("#### Charging Rikku zone:", gameVars.getNEAzone())
    print("#### This will take", battles, "number of battles (99 means unknown)")


def decideNEA(bonusAdvance: int = 0):
    import rngTrack
    maxBattles = 1
    zanOutdoors = rngTrack.comingBattles(area="zanarkand_(overpass)", battleCount=maxBattles, extraAdvances=bonusAdvance)
    zanIndoors = rngTrack.comingBattles(area="zanarkand_(dome)", battleCount=maxBattles, extraAdvances=bonusAdvance)
    seaSorrows = rngTrack.comingBattles(area="inside_sin_(front)", battleCount=maxBattles, extraAdvances=bonusAdvance + 6)

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
    memory.main.awaitControl()
    decideNEA()
    # Starts from the map just after the fireplace chat.
    reEquipNE = False
    if memory.main.overdriveState2()[6] != 100 and gameVars.getNEAzone() == 1:
        memory.main.fullPartyFormat('rikku', fullMenuClose=False)
        menu.equipArmor(character=gameVars.neArmor(), ability=99)
        reEquipNE = True

    gameVars.setSkipZanLuck(rngTrack.decideSkipZanLuck())
    logs.writeStats("Zanarkand Luck Skip:")
    logs.writeStats(gameVars.getSkipZanLuck())
    # gameVars.setSkipZanLuck(True) #For testing
    print("Outdoor Zanarkand pathing section")
    while memory.main.getMap() != 225:
        if memory.main.userControl():
            if memory.main.getCoords()[1] > -52:
                targetPathing.setMovement([103, -54])
            elif memory.main.getCoords()[0] < 172:
                targetPathing.setMovement([176, -118])
            else:
                FFXC.set_movement(-1, 1)
        else:
            FFXC.set_neutral()

    fortuneSlot = memory.main.getItemSlot(74)
    if fortuneSlot == 255:
        fortuneCount = 0
    else:
        fortuneCount = memory.main.getItemCountSlot(fortuneSlot)

    checkpoint = 0
    while memory.main.getMap() != 314:
        if memory.main.userControl():
            if checkpoint == 3 and gameVars.getSkipZanLuck():
                checkpoint = 5
            elif checkpoint == 4:  # First chest
                fortuneSlot = memory.main.getItemSlot(74)
                if fortuneSlot == 255:
                    fortuneCount = 0
                    FFXC.set_movement(-1, 1)
                    xbox.tapB()
                else:
                    if memory.main.getItemCountSlot(fortuneSlot) > fortuneCount:
                        checkpoint += 1
                        memory.main.clickToControl()
                    else:
                        FFXC.set_movement(-1, 1)
                        xbox.tapB()
            elif targetPathing.setMovement(targetPathing.zanarkandOutdoors(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()

            if screen.BattleScreen():
                battle.main.chargeRikkuOD()
                if reEquipNE and memory.main.overdriveState2()[6] == 100:
                    reEquipNE = False
                    memory.main.clickToControl()
                    memory.main.fullPartyFormat('yuna', fullMenuClose=False)
                    menu.equipArmor(
                        character=gameVars.neArmor(), ability=0x801D)
                    memory.main.closeMenu()
            elif memory.main.diagSkipPossible() and not memory.main.battleActive():
                xbox.tapB()
            elif memory.main.menuOpen():
                xbox.tapB()

    # Outside the dome
    print("Now approaching the Blitz dome.")
    print("Close observation will reveal this is the same blitz dome")
    print("as the one from the opening of the game.")
    while memory.main.getMap() != 222:
        FFXC.set_movement(0, 1)
        xbox.tapB()

    print("Start of Zanarkand Dome section")
    friendSlot = memory.main.getItemSlot(97)
    if friendSlot == 255:
        friendCount = 0
    else:
        friendCount = memory.main.getItemCountSlot(friendSlot)

    luckSlot = memory.main.getItemSlot(94)
    if luckSlot == 255:
        friendCount = 0
    else:
        luckCount = memory.main.getItemCountSlot(luckSlot)

    if memory.main.overdriveState2()[6] != 100 and gameVars.getNEAzone() == 2:
        memory.main.fullPartyFormat('rikku', fullMenuClose=False)
        menu.equipArmor(character=gameVars.neArmor(), ability=99)
        reEquipNE = True

    checkpoint = 0
    while memory.main.getMap() != 320:
        if memory.main.userControl():
            if checkpoint == 13:  # Second chest
                friendSlot = memory.main.getItemSlot(97)
                if friendSlot == 255:
                    friendCount = 0
                    targetPathing.setMovement([8, 90])
                    memory.main.waitFrames(1)
                    xbox.tapB()
                else:
                    if memory.main.getItemCountSlot(friendSlot) > friendCount:
                        checkpoint += 1
                        memory.main.clickToControl()
                    else:
                        targetPathing.setMovement([8, 90])
                        memory.main.waitFrames(1)
                        xbox.tapB()
            if checkpoint == 23 and gameVars.getSkipZanLuck():
                checkpoint = 25
            elif checkpoint == 24:  # Third chest
                luckSlot = memory.main.getItemSlot(94)
                if luckSlot == 255:
                    luckCount = 0
                    FFXC.set_movement(1, 1)
                    xbox.tapB()
                else:
                    if memory.main.getItemCountSlot(luckSlot) > luckCount:
                        checkpoint += 1
                        print("Updating checkpoint:", checkpoint)
                        memory.main.clickToControl()
                    else:
                        FFXC.set_movement(1, 1)
                        xbox.tapB()
            elif checkpoint == 29:  # Save sphere
                memory.main.touchSaveSphere()
                checkpoint += 1
            elif memory.main.getMap() == 316 and checkpoint < 21:  # Final room before trials
                print("Final room before trials")
                checkpoint = 21
            elif targetPathing.setMovement(targetPathing.zanarkandDome(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if screen.BattleScreen():
                battle.main.chargeRikkuOD()
                if reEquipNE and memory.main.overdriveState2()[6] == 100:
                    reEquipNE = False
                    memory.main.clickToControl()
                    memory.main.fullPartyFormat('yuna', fullMenuClose=False)
                    menu.equipArmor(
                        character=gameVars.neArmor(), ability=0x801D)
                    memory.main.closeMenu()
            elif memory.main.diagSkipPossible() and not memory.main.battleActive():
                xbox.tapB()
            elif memory.main.menuOpen():
                xbox.tapB()


def trials():
    checkpoint = 0
    while checkpoint < 89:
        checkpoint = trials0(checkpoint)
        checkpoint = trials1(checkpoint)
        checkpoint = trials2(checkpoint)
        checkpoint = trials3(checkpoint)
        checkpoint = trials4(checkpoint)


def trials0(checkpoint):
    memory.main.awaitControl()

    while checkpoint < 9:
        if memory.main.userControl():
            if checkpoint == 8:
                FFXC.set_movement(-1, 0)
                while memory.main.userControl():
                    xbox.tapB()
                FFXC.set_movement(0, 1)
                memory.main.waitFrames(30 * 0.2)
                memory.main.awaitControl()
                memory.main.waitFrames(30 * 1.3)
                FFXC.set_movement(0, 1)
                checkpoint += 1
            elif targetPathing.setMovement(targetPathing.zanarkandTrials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
    return checkpoint


def trials1(checkpoint):
    memory.main.awaitControl()

    while checkpoint < 31:
        if memory.main.userControl():
            if checkpoint == 20:
                FFXC.set_movement(-1, 1)
                memory.main.clickToEvent()
                FFXC.set_neutral()
                xbox.SkipDialog(0.5)
                memory.main.clickToControl3()
                checkpoint += 1
            elif checkpoint == 26 or checkpoint == 28:
                FFXC.set_movement(-1, -1)
                memory.main.clickToEvent()
                FFXC.set_neutral()
                xbox.SkipDialog(0.5)
                memory.main.clickToControl3()
                checkpoint += 1
            elif checkpoint == 30:
                FFXC.set_movement(0, 1)
                memory.main.awaitEvent()
                memory.main.waitFrames(30 * 0.2)
                FFXC.set_neutral()
                checkpoint += 1
            elif targetPathing.setMovement(targetPathing.zanarkandTrials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
    return checkpoint


def trials2(checkpoint):
    memory.main.awaitControl()

    while checkpoint < 49:
        if memory.main.userControl():
            if checkpoint == 46:
                FFXC.set_movement(1, 0)
                memory.main.clickToEvent()
                FFXC.set_neutral()
                xbox.SkipDialog(0.5)
                memory.main.clickToControl3()
                checkpoint += 1
            elif checkpoint == 48:
                FFXC.set_movement(-1, 1)
                memory.main.awaitEvent()
                memory.main.waitFrames(30 * 0.2)
                FFXC.set_neutral()
                checkpoint += 1
            elif targetPathing.setMovement(targetPathing.zanarkandTrials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
    return checkpoint


def trials3(checkpoint):
    memory.main.awaitControl()

    while checkpoint < 69:
        if memory.main.userControl():
            if checkpoint == 66:
                FFXC.set_movement(1, 0)
                memory.main.clickToEvent()
                FFXC.set_neutral()
                xbox.SkipDialog(0.7)
                memory.main.clickToControl3()
                checkpoint += 1
            elif checkpoint == 68:
                FFXC.set_movement(-1, 1)
                memory.main.awaitEvent()
                memory.main.waitFrames(30 * 0.2)
                FFXC.set_neutral()
                checkpoint += 1
            elif targetPathing.setMovement(targetPathing.zanarkandTrials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
    return checkpoint


def trials4(checkpoint):
    memory.main.awaitControl()

    while checkpoint < 89:
        if memory.main.userControl():
            if checkpoint == 81:
                FFXC.set_movement(0, 1)
                memory.main.clickToEvent()
                FFXC.set_neutral()
                xbox.SkipDialog(0.5)
                memory.main.clickToControl3()
                checkpoint += 1
            elif checkpoint == 87:
                while memory.main.userControl():
                    targetPathing.setMovement([141, 1])
                    xbox.tapB()
                FFXC.set_neutral()
                memory.main.clickToControl3()
                checkpoint += 1
            elif targetPathing.setMovement(targetPathing.zanarkandTrials(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
    FFXC.set_neutral()
    return checkpoint


def sanctuaryKeeper():
    ver = gameVars.endGameVersion()
    print("Now prepping for Sanctuary Keeper fight")

    if ver == 4:
        print("Pattern for four return spheres off of the B&Y fight")
        menu.skReturn()
    elif ver == 3:
        menu.skFriend()
    else:
        menu.skMixed()
    memory.main.fullPartyFormat('yuna')
    memory.main.closeMenu()

    while not targetPathing.setMovement([110, 20]):
        pass
    FFXC.set_movement(-1, 1)
    memory.main.awaitEvent()
    xbox.clickToBattle()
    if screen.turnTidus():
        battle.main.defend()
        xbox.clickToBattle()
    battle.main.aeonSummon(4)  # This is the whole fight. Kinda sad.
    while not memory.main.battleComplete():
        if memory.main.turnReady():
            print(memory.main.rngArrayFromIndex(index=43, arrayLen=4))
            battle.main.attack('none')
    memory.main.clickToControl()


def yunalesca():
    ver = gameVars.endGameVersion()
    while not targetPathing.setMovement([-2, -179]):
        if memory.main.diagSkipPossible():
            xbox.tapB()

    if ver == 4:
        print("Final pattern for four return spheres off of the B&Y fight")
        menu.skReturn2()
        memory.main.closeMenu()
    else:
        print("No further sphere gridding needed at this time.")

    print("Sphere grid is done. Moving on to storyline and eventually Yunalesca.")

    memory.main.touchSaveSphere()

    checkpoint = 0
    # Gets us to Yunalesca battle through multiple rooms.
    while not memory.main.battleActive():
        if memory.main.menuOpen():
            memory.main.closeMenu()
        elif memory.main.userControl():
            if checkpoint in [2, 4]:
                FFXC.set_movement(0, 1)
                memory.main.awaitEvent()
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
            elif targetPathing.setMovement(targetPathing.yunalesca(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            FFXC.set_value('BtnB', 1)
            FFXC.set_value('BtnA', 1)
            memory.main.waitFrames(1)
            FFXC.set_value('BtnB', 0)
            FFXC.set_value('BtnA', 0)
            memory.main.waitFrames(1)
    xbox.clickToBattle()
    battle.main.aeonSummon(4)  # Summon Bahamut and attack.
    memory.main.clickToControl()  # This does all the attacking and dialog skipping

    # Now to check for zombie strike and then report to logs.
    print("Ready to check for Zombiestrike")
    logs.writeStats("Zombiestrike:")
    logs.writeStats(gameVars.zombieWeapon())
    print("++Zombiestrike:")
    print("++", gameVars.zombieWeapon())


def post_Yunalesca(checkpoint=0):
    print("Heading back outside.")
    FFXC.set_neutral()
    if gameVars.nemesis():
        menu.equipWeapon(character=0, ability=0x807A, fullMenuClose=True)
    memory.main.waitFrames(2)
    while memory.main.getMap() != 194:
        if memory.main.userControl():
            if checkpoint < 2 and memory.main.getMap() == 319:  # Back to room before Yunalesca
                checkpoint = 2
                print("Checkpoint reached:", checkpoint)
            elif checkpoint < 4 and memory.main.getMap() == 318:  # Exit to room with the inert Aeon
                checkpoint = 4
                print("Checkpoint reached:", checkpoint)
            elif checkpoint == 7:
                memory.main.touchSaveSphere()
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
            elif checkpoint < 10 and memory.main.getMap() == 320:  # Back to larger of the puzzle rooms
                checkpoint = 10
                print("Checkpoint reached:", checkpoint)
            elif checkpoint < 18 and memory.main.getMap() == 316:  # Hallway before puzzle rooms
                checkpoint = 18
                print("Checkpoint reached:", checkpoint)
            elif checkpoint < 25 and memory.main.getMap() == 315:  # Hallway before puzzle rooms
                checkpoint = 25
                print("Checkpoint reached:", checkpoint)
            elif checkpoint == 26:
                FFXC.set_neutral()
            elif targetPathing.setMovement(targetPathing.yunalescaToAirship(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if screen.BattleScreen():
                battle.main.fleeAll()
            elif memory.main.diagSkipPossible() and not memory.main.battleActive():
                xbox.tapB()
            elif memory.main.cutsceneSkipPossible():
                print(memory.main.getCutsceneID())
                if memory.main.getCutsceneID() == (5673, 2850, 3):
                    memory.main.waitFrames(10)
                    xbox.skipScene()
