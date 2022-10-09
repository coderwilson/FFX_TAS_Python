import xbox
import menu
import memory.main
import battle.main
import logs
import targetPathing
import vars
import rngTrack
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def toHiddenCave():
    memory.main.fullPartyFormat('rikku')
    rngTrack.printManipInfo()
    lastReport = False
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
            _, nextDrop = rngTrack.neaTrack()
            if checkpoint == 8 and (nextDrop >= 1 or memory.main.nextChanceRNG10() >= 9):
                if not lastReport:
                    print("Need more advances before entering cave.")
                    lastReport = True
                checkpoint -= 2
            elif checkpoint == 8 and memory.main.getItemSlot(39) == 255 and memory.main.nextChanceRNG10():
                if not lastReport:
                    print("Need more advances before entering cave (no silence grenade)")
                    lastReport = True
                checkpoint -= 2
            elif checkpoint == 9:
                FFXC.set_movement(-1, 1)
            elif targetPathing.setMovement(targetPathing.neApproach(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                _, nextDrop = rngTrack.neaTrack()
                lastReport = False
                print("### Starting manip battle")
                rngTrack.printManipInfo()
                memory.main.waitFrames(2)
                if nextDrop >= 1:
                    if memory.main.nextChanceRNG10() != 0:
                        battle.main.advanceRNG10(memory.main.nextChanceRNG10())
                    else:
                        battle.main.advanceRNG12()
                elif memory.main.nextChanceRNG10():
                    battle.main.advanceRNG10(memory.main.nextChanceRNG10())
                else:
                    print("Failed to determine next steps, requires dev review.")
                    print("RNG10: ", memory.main.nextChanceRNG10())
                    print("RNG12: ", memory.main.nextChanceRNG12())
                    battle.main.fleeAll()
                prepBattles += 1
                memory.main.fullPartyFormat('rikku')
                memory.main.touchSaveSphere()
                rngTrack.printManipInfo()
            elif memory.main.diagSkipPossible() or memory.main.menuOpen():
                xbox.tapB()
    logs.writeStats("NEA extra manip battles:")
    logs.writeStats(prepBattles)

def nextGreen():
    nextGreen = memory.main.nextChanceRNG01(version='green')[0][0]
    nextWhite = memory.main.nextChanceRNG01()[0][0]
    print("## Next Ghost coming up:")
    print("## Green: ", nextGreen)
    print("## White: ", nextWhite)
    if nextGreen < nextWhite and memory.main.nextChanceRNG10() == 0:
        if nextGreen >= 2:
            goGreen = True

def dropHunt():
    print("Now in the cave. Ready to try to get the NE armor.")
    memory.main.fullPartyFormat('rikku')

    goGreen = nextGreen()

    rngTrack.printManipInfo()
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
                if memory.main.getEncounterID() in [319, 323]:
                    battle.main.ghostKill()
                else:
                    battle.main.fleeAll()
                memory.main.clickToControl3()
                memory.main.checkNEArmor()
                if gameVars.neArmor() == 255:
                    #battle.main.healUp(fullMenuClose=False)
                    memory.main.fullPartyFormat('rikku')
                    
                    if nextGreen() and not goGreen:
                        goGreen = True
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
