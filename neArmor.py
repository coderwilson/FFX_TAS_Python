import xbox
import menu
import memory.main
import battle.main
import logs
import targetPathing
import vars
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def toHiddenCave():
    memory.main.fullPartyFormat('rikku')
    memory.main.printManipInfo()
    firstSave = False
    checkpoint = 0
    prepBattles = 0
    while memory.main.getMap() != 56:
        if memory.main.userControl():
            if checkpoint < 5 and memory.main.getMap() == 266:
                checkpoint = 5
            if checkpoint == 6 and not firstSave:
                if memory.main.getTidusMP() < 8:
                    memory.main.touchSaveSphere()
                firstSave = True
            if checkpoint == 8 and (memory.main.nextChanceRNG12() >= 1 or memory.main.nextChanceRNG10() >= 1) \
                    and memory.main.rngSeed() != 31:
                checkpoint -= 2
            if checkpoint == 8 and memory.main.nextChanceRNG12() >= 1 and memory.main.rngSeed() == 31:
                checkpoint -= 2
            elif checkpoint == 9:
                FFXC.set_movement(-1, 1)
            elif targetPathing.setMovement(targetPathing.neApproach(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                if memory.main.nextChanceRNG12() >= 1:
                    if memory.main.nextChanceRNG10() != 0:
                        memory.main.advanceRNG10(memory.main.nextChanceRNG10())
                    else:
                        memory.main.advanceRNG12()
                elif memory.main.nextChanceRNG10() >= 1:
                    memory.main.advanceRNG10(memory.main.nextChanceRNG10())
                else:
                    battle.main.fleeAll()
                prepBattles += 1
                memory.main.fullPartyFormat('rikku')
                memory.main.touchSaveSphere()
                memory.main.printManipInfo()
            elif memory.main.diagSkipPossible() or memory.main.menuOpen():
                xbox.tapB()
    logs.writeStats("NEA extra manip battles:")
    logs.writeStats(prepBattles)


def dropHunt():
    print("Now in the cave. Ready to try to get the NE armor.")
    memory.main.fullPartyFormat('rikku')

    # Prep work:
    goGreen = False
    nextGreen = memory.main.nextChanceRNG01(version='green')[0][0]
    nextWhite = memory.main.nextChanceRNG01()[0][0]
    if nextGreen < nextWhite and memory.main.nextChanceRNG10() == 0:
        if nextGreen >= 2:
            goGreen = True

    memory.main.printManipInfo()
    print("#####################")
    print("#####################")
    print("#####################")
    if goGreen:
        memory.main.nextChanceRNG01(version='green')
    else:
        memory.main.nextChanceRNG01()
    checkpoint = 0
    preGhostBattles = 0
    while gameVars.neArmor() == 255:
        if memory.main.userControl():
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
            if memory.main.battleActive():
                if memory.main.nextChanceRNG12() == 0:
                    if memory.main.getEncounterID() in [319, 323]:
                        battle.main.ghostKill()
                    else:
                        if memory.main.nextChanceRNG10() != 0:
                            memory.main.advanceRNG10(
                                memory.main.nextChanceRNG10())
                        else:
                            battle.main.fleeAll()
                        memory.main.clickToControl3()
                    memory.main.checkNEArmor()
                else:
                    if memory.main.nextChanceRNG10() != 0:
                        memory.main.advanceRNG10(memory.main.nextChanceRNG10())
                    else:
                        memory.main.advanceRNG12()
                    memory.main.clickToControl3()
                battle.main.healUp(fullMenuClose=True)
                if gameVars.neArmor() == 255:
                    memory.main.fullPartyFormat('rikku')
                    nextGreen = memory.main.nextChanceRNG01(version='green')[
                        0][0]
                    nextWhite = memory.main.nextChanceRNG01()[0][0]
                    if not goGreen and nextGreen < nextWhite and memory.main.nextChanceRNG10() == 0:
                        if nextGreen >= 2:
                            goGreen = True
                    memory.main.printManipInfo()
                    if goGreen:
                        memory.main.nextChanceRNG01(version='green')
                    else:
                        memory.main.nextChanceRNG01()
                    preGhostBattles += 1
            elif memory.main.diagSkipPossible() or memory.main.menuOpen():
                xbox.tapB()
    print("The NE armor hunt is complete. Char:", gameVars.neArmor())
    logs.writeStats("Pre-Ghost flees:")
    logs.writeStats(preGhostBattles)
    logs.writeStats("NEA char:")
    logs.writeStats(gameVars.neArmor())


def returnToGagazet():
    unequip = False
    if memory.main.getCoords()[0] > 300:
        goGreen = True
        menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
        if memory.main.overdriveState2()[6] != 100:
            unequip = True
    else:
        goGreen = False
        if memory.main.overdriveState2()[6] == 100:
            menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)

    checkpoint = 0
    while memory.main.getMap() != 259:
        if memory.main.userControl():
            if goGreen:
                if checkpoint == 10:
                    goGreen = False
                    checkpoint = 0
                elif targetPathing.setMovement(targetPathing.neReturnGreen(checkpoint)):
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
            elif checkpoint < 1 and memory.main.getMap() == 266:
                checkpoint = 1
            elif checkpoint == 2 and unequip:
                menu.equipArmor(character=gameVars.neArmor(), ability=99)
                unequip = False
            elif checkpoint == 2:
                memory.main.touchSaveSphere()
                checkpoint += 1
            elif checkpoint < 7 and memory.main.getMap() == 279:
                checkpoint = 7
            elif targetPathing.setMovement(targetPathing.neReturn(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                battle.main.fleeAll()
            elif memory.main.diagSkipPossible() or memory.main.menuOpen():
                xbox.tapB()
