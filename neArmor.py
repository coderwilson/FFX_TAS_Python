import xbox
import menu
import memory
import battle
import logs
import targetPathing
import vars
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def toHiddenCave():
    memory.fullPartyFormat('rikku')
    memory.printManipInfo()
    firstSave = False
    checkpoint = 0
    prepBattles = 0
    while memory.getMap() != 56:
        if memory.userControl():
            if checkpoint < 5 and memory.getMap() == 266:
                checkpoint = 5
            if checkpoint == 6 and not firstSave:
                if memory.getTidusMP() < 8:
                    memory.touchSaveSphere()
                firstSave = True
            if checkpoint == 8 and (memory.nextChanceRNG12() >= 1 or memory.nextChanceRNG10() >= 1) \
                    and memory.rngSeed() != 31:
                checkpoint -= 2
            if checkpoint == 8 and memory.nextChanceRNG12() >= 1 and memory.rngSeed() == 31:
                checkpoint -= 2
            elif checkpoint == 9:
                FFXC.set_movement(-1, 1)
            elif targetPathing.setMovement(targetPathing.neApproach(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.battleActive():
                if memory.nextChanceRNG12() >= 1:
                    if memory.nextChanceRNG10() != 0:
                        battle.advanceRNG10(memory.nextChanceRNG10())
                    else:
                        battle.advanceRNG12()
                elif memory.nextChanceRNG10() >= 1:
                    battle.advanceRNG10(memory.nextChanceRNG10())
                else:
                    battle.fleeAll()
                prepBattles += 1
                memory.fullPartyFormat('rikku')
                memory.touchSaveSphere()
                memory.printManipInfo()
            elif memory.diagSkipPossible() or memory.menuOpen():
                xbox.tapB()
    logs.writeStats("NEA extra manip battles:")
    logs.writeStats(prepBattles)


def dropHunt():
    print("Now in the cave. Ready to try to get the NE armor.")
    memory.fullPartyFormat('rikku')

    # Prep work:
    goGreen = False
    nextGreen = memory.nextChanceRNG01(version='green')[0][0]
    nextWhite = memory.nextChanceRNG01()[0][0]
    if nextGreen < nextWhite and memory.nextChanceRNG10() == 0:
        if nextGreen >= 2:
            goGreen = True

    memory.printManipInfo()
    print("#####################")
    print("#####################")
    print("#####################")
    if goGreen:
        memory.nextChanceRNG01(version='green')
    else:
        memory.nextChanceRNG01()
    checkpoint = 0
    preGhostBattles = 0
    while gameVars.neArmor() == 255:
        if memory.userControl():
            if goGreen:
                if checkpoint == 15:
                    checkpoint -= 2
                elif targetPathing.setMovement(targetPathing.neForceEncountersGreen(checkpoint)):
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
            else:
                if targetPathing.setMovement(targetPathing.neForceEncountersWhite(checkpoint)):
                    checkpoint += 1
                    if checkpoint % 2 == 0 and not goGreen:
                        checkpoint = 0
                    print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.battleActive():
                if memory.nextChanceRNG12() == 0:
                    if memory.getEncounterID() in [319, 323]:
                        battle.ghostKill()
                    else:
                        if memory.nextChanceRNG10() != 0:
                            battle.advanceRNG10(
                                memory.nextChanceRNG10())
                        else:
                            battle.fleeAll()
                        memory.clickToControl3()
                    memory.checkNEArmor()
                else:
                    if memory.nextChanceRNG10() != 0:
                        battle.advanceRNG10(memory.nextChanceRNG10())
                    else:
                        battle.advanceRNG12()
                    memory.clickToControl3()
                battle.healUp(fullMenuClose=True)
                if gameVars.neArmor() == 255:
                    memory.fullPartyFormat('rikku')
                    nextGreen = memory.nextChanceRNG01(version='green')[
                        0][0]
                    nextWhite = memory.nextChanceRNG01()[0][0]
                    if not goGreen and nextGreen < nextWhite and memory.nextChanceRNG10() == 0:
                        if nextGreen >= 2:
                            goGreen = True
                    memory.printManipInfo()
                    if goGreen:
                        memory.nextChanceRNG01(version='green')
                    else:
                        memory.nextChanceRNG01()
                    preGhostBattles += 1
            elif memory.diagSkipPossible() or memory.menuOpen():
                xbox.tapB()
    print("The NE armor hunt is complete. Char:", gameVars.neArmor())
    logs.writeStats("Pre-Ghost flees:")
    logs.writeStats(preGhostBattles)
    logs.writeStats("NEA char:")
    logs.writeStats(gameVars.neArmor())


def returnToGagazet():
    unequip = False
    if memory.getCoords()[0] > 300:
        goGreen = True
        menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
        if memory.overdriveState2()[6] != 100:
            unequip = True
    else:
        goGreen = False
        if memory.overdriveState2()[6] == 100:
            menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)

    checkpoint = 0
    while memory.getMap() != 259:
        if memory.userControl():
            if goGreen:
                if checkpoint == 10:
                    goGreen = False
                    checkpoint = 0
                elif targetPathing.setMovement(targetPathing.neReturnGreen(checkpoint)):
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
            elif checkpoint < 1 and memory.getMap() == 266:
                checkpoint = 1
            elif checkpoint == 2 and unequip:
                menu.equipArmor(character=gameVars.neArmor(), ability=99)
                unequip = False
            elif checkpoint == 2:
                memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint < 7 and memory.getMap() == 279:
                checkpoint = 7
            elif targetPathing.setMovement(targetPathing.neReturn(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.battleActive():
                battle.fleeAll()
            elif memory.diagSkipPossible() or memory.menuOpen():
                xbox.tapB()
