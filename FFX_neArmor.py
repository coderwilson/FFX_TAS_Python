import FFX_Xbox
import FFX_Screen
import FFX_menu
import FFX_memory
import FFX_Battle
import FFX_Logs
import FFX_targetPathing
import FFX_vars
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()


def toHiddenCave():
    FFX_memory.fullPartyFormat('rikku')
    FFX_memory.printManipInfo()
    firstSave = False
    checkpoint = 0
    prepBattles = 0
    while FFX_memory.getMap() != 56:
        # print(FFX_memory.getMap())
        if FFX_memory.userControl():
            if checkpoint < 5 and FFX_memory.getMap() == 266:
                checkpoint = 5
            if checkpoint == 6 and not firstSave:
                if FFX_memory.getTidusMP() < 8:
                    FFX_memory.touchSaveSphere()
                firstSave = True
            if checkpoint == 8 and (FFX_memory.nextChanceRNG12() >= 1 or FFX_memory.nextChanceRNG10() >= 1) \
                    and FFX_memory.rngSeed() != 31:
                checkpoint -= 2
            if checkpoint == 8 and FFX_memory.nextChanceRNG12() >= 1 and FFX_memory.rngSeed() == 31:
                checkpoint -= 2
            elif checkpoint == 9:
                FFXC.set_movement(-1, 1)
            elif FFX_targetPathing.setMovement(FFX_targetPathing.neApproach(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                if FFX_memory.nextChanceRNG12() >= 1:
                    if FFX_memory.nextChanceRNG10() != 0:
                        FFX_Battle.advanceRNG10(FFX_memory.nextChanceRNG10())
                    else:
                        FFX_Battle.advanceRNG12()
                elif FFX_memory.nextChanceRNG10() >= 1:
                    FFX_Battle.advanceRNG10(FFX_memory.nextChanceRNG10())
                else:
                    FFX_Battle.fleeAll()
                prepBattles += 1
                FFX_memory.fullPartyFormat('rikku')
                FFX_memory.touchSaveSphere()
                FFX_memory.printManipInfo()
            elif FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
                FFX_Xbox.tapB()
    FFX_Logs.writeStats("NEA extra manip battles:")
    FFX_Logs.writeStats(prepBattles)


def dropHunt():
    print("Now in the cave. Ready to try to get the NE armor.")
    # FFX_memory.setEncounterRate(1) #Testing only
    FFX_memory.fullPartyFormat('rikku')

    # Prep work:
    goGreen = False
    nextGreen = FFX_memory.nextChanceRNG01(version='green')[0][0]
    nextWhite = FFX_memory.nextChanceRNG01()[0][0]
    if nextGreen < nextWhite and FFX_memory.nextChanceRNG10() == 0:
        if nextGreen >= 2:
            goGreen = True

    FFX_memory.printManipInfo()
    print("#####################")
    print("#####################")
    print("#####################")
    print("#####################")
    print("#####################")
    if goGreen:
        FFX_memory.nextChanceRNG01(version='green')
    else:
        FFX_memory.nextChanceRNG01()
    checkpoint = 0
    preGhostBattles = 0
    while gameVars.neArmor() == 255:
        if FFX_memory.userControl():
            if goGreen:
                if checkpoint == 15:
                    checkpoint -= 2
                elif FFX_targetPathing.setMovement(FFX_targetPathing.neForceEncountersGreen(checkpoint)) == True:
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
            else:
                if FFX_targetPathing.setMovement(FFX_targetPathing.neForceEncountersWhite(checkpoint)) == True:
                    checkpoint += 1
                    if checkpoint % 2 == 0 and not goGreen:
                        checkpoint = 0
                    print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                if FFX_memory.nextChanceRNG12() == 0:
                    if FFX_memory.getBattleNum() in [319, 323]:
                        FFX_Battle.ghostKill()
                    else:
                        if FFX_memory.nextChanceRNG10() != 0:
                            FFX_Battle.advanceRNG10(
                                FFX_memory.nextChanceRNG10())
                        else:
                            FFX_Battle.fleeAll()
                        FFX_memory.clickToControl3()
                    FFX_memory.checkNEArmor()
                else:
                    if FFX_memory.nextChanceRNG10() != 0:
                        FFX_Battle.advanceRNG10(FFX_memory.nextChanceRNG10())
                    else:
                        FFX_Battle.advanceRNG12()
                    FFX_memory.clickToControl3()
                FFX_Battle.healUp(fullMenuClose=True)
                if gameVars.neArmor() == 255:
                    FFX_memory.fullPartyFormat('rikku')
                    nextGreen = FFX_memory.nextChanceRNG01(version='green')[
                        0][0]
                    nextWhite = FFX_memory.nextChanceRNG01()[0][0]
                    if not goGreen and nextGreen < nextWhite and FFX_memory.nextChanceRNG10() == 0:
                        if nextGreen >= 2:
                            goGreen = True
                    FFX_memory.printManipInfo()
                    if goGreen:
                        FFX_memory.nextChanceRNG01(version='green')
                    else:
                        FFX_memory.nextChanceRNG01()
                    preGhostBattles += 1
            elif FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
                FFX_Xbox.tapB()
    print("The NE armor hunt is complete. Char:", gameVars.neArmor())
    FFX_Logs.writeStats("Pre-Ghost battles:")
    FFX_Logs.writeStats(preGhostBattles)
    FFX_Logs.writeStats("NEA char:")
    FFX_Logs.writeStats(gameVars.neArmor())


def returnToGagazet():
    unequip = False
    if FFX_memory.getCoords()[0] > 300:
        goGreen = True
        FFX_menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)
        if FFX_memory.overdriveState2()[6] != 100:
            unequip = True
    else:
        goGreen = False
        if FFX_memory.overdriveState2()[6] == 100:
            FFX_menu.equipArmor(character=gameVars.neArmor(), ability=0x801D)

    checkpoint = 0
    while FFX_memory.getMap() != 259:
        if FFX_memory.userControl():
            if goGreen == True:
                if checkpoint == 10:
                    goGreen = False
                    checkpoint = 0
                elif FFX_targetPathing.setMovement(FFX_targetPathing.neReturnGreen(checkpoint)) == True:
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
            elif checkpoint < 1 and FFX_memory.getMap() == 266:
                checkpoint = 1
            elif checkpoint == 2 and unequip:
                FFX_menu.equipArmor(character=gameVars.neArmor(), ability=99)
                unequip = False
            elif checkpoint == 2:
                FFX_memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint < 7 and FFX_memory.getMap() == 279:
                checkpoint = 7
            elif FFX_targetPathing.setMovement(FFX_targetPathing.neReturn(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                FFX_Battle.fleeAll()
            elif FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
                FFX_Xbox.tapB()
