import battle.main
import logs
import memory.main
import menu
import rngTrack
import targetPathing
import vars
import xbox

gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()


def toHiddenCave():
    # Force manip NEA
    if gameVars.marathon_safety():
        if rngTrack.nea_track()[1] in [0, 1]:
            pass
        else:
            FFXC.set_neutral()
            print("===============")
            memory.main.waitFrames(9)
            print("===============")
            memory.main.waitFrames(9)
            print("== For marathon safety at RPGLB, we will now advance RNG.")
            memory.main.waitFrames(9)
            print(
                "== This is not part of the normal TAS, and is only for marathon safety."
            )
            memory.main.waitFrames(30)
            advanceCount = 0
            nextItem, preAdvance13 = rngTrack.item_to_be_dropped(enemy="ghost")
            while nextItem.equipmentType() != 1:
                print("Advance 12 - ", advanceCount)
                advanceCount += 1
                memory.main.advanceRNG12()
                nextItem, preAdvance13 = rngTrack.item_to_be_dropped(enemy="ghost")
            while not nextItem.hasAbility(0x801D):
                print("Advance 13 - ", advanceCount)
                advanceCount += 1
                memory.main.advanceRNG13()
                nextItem, preAdvance13 = rngTrack.item_to_be_dropped(enemy="ghost")

            if memory.main.nextChanceRNG10() > 10:
                print("Advance 10 - ", advanceCount)
                advanceCount += 1
                if memory.main.getItemSlot(39) == 255:
                    while memory.main.nextChanceRNG10() != 0:
                        memory.main.advanceRNG10()
                else:
                    while memory.main.nextChanceRNG10() > 4:
                        memory.main.advanceRNG10()
            print("== Complete.")
            memory.main.waitFrames(9)
            print("===============")
            memory.main.waitFrames(9)
            print("===============")
            memory.main.waitFrames(9)

    # Regular logic
    memory.main.fullPartyFormat("rikku")
    rngTrack.print_manip_info()
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
            _, nextDrop = rngTrack.nea_track()
            if checkpoint == 8 and (
                nextDrop >= 1 or memory.main.nextChanceRNG10() >= 9
            ):
                if not lastReport:
                    print("Need more advances before entering cave.")
                    lastReport = True
                checkpoint -= 2
            elif (
                checkpoint == 8
                and memory.main.getItemSlot(39) == 255
                and memory.main.nextChanceRNG10()
            ):
                if not lastReport:
                    print(
                        "Need more advances before entering cave (no silence grenade)"
                    )
                    lastReport = True
                checkpoint -= 2
            elif checkpoint == 9:
                FFXC.set_movement(-1, 1)
            elif targetPathing.set_movement(targetPathing.ne_approach(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                _, nextDrop = rngTrack.nea_track()
                lastReport = False
                print("### Starting manip battle")
                rngTrack.print_manip_info()
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
                memory.main.fullPartyFormat("rikku")
                memory.main.touchSaveSphere()
                rngTrack.print_manip_info()
            elif memory.main.diagSkipPossible() or memory.main.menuOpen():
                xbox.tapB()
    logs.write_stats("NEA extra manip battles:")
    logs.write_stats(prepBattles)


def nextGreen():
    nextGreen = memory.main.nextChanceRNG01(version="green")[0][0]
    nextWhite = memory.main.nextChanceRNG01()[0][0]
    print("## Next Ghost coming up:")
    print("## Green: ", nextGreen)
    print("## White: ", nextWhite)
    if nextGreen < nextWhite and memory.main.nextChanceRNG10() == 0:
        if nextGreen >= 2:
            goGreen = True


def dropHunt():
    print("Now in the cave. Ready to try to get the NE armor.")
    memory.main.fullPartyFormat("rikku")

    goGreen = nextGreen()

    rngTrack.print_manip_info()
    checkpoint = 0
    preGhostBattles = 0
    while gameVars.neArmor() == 255:
        if memory.main.userControl():
            if goGreen:
                if checkpoint == 15:
                    checkpoint -= 2
                elif targetPathing.set_movement(
                    targetPathing.ne_force_encounters_green(checkpoint)
                ):
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
            else:
                if targetPathing.set_movement(
                    targetPathing.ne_force_encounters_white(checkpoint)
                ):
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
                    battle.main.healUp(fullMenuClose=False)
                    memory.main.fullPartyFormat("rikku")
                    memory.main.closeMenu()

                    if nextGreen() and not goGreen:
                        goGreen = True
                    preGhostBattles += 1
            elif memory.main.diagSkipPossible() or memory.main.menuOpen():
                xbox.tapB()
    print("The NE armor hunt is complete. Char:", gameVars.neArmor())
    logs.write_stats("Pre-Ghost flees:")
    logs.write_stats(preGhostBattles)
    logs.write_stats("NEA char:")
    logs.write_stats(gameVars.neArmor())


def returnToGagazet():
    unequip = False
    if memory.main.getCoords()[0] > 300:
        goGreen = True
        menu.equip_armor(character=gameVars.neArmor(), ability=0x801D)
        if memory.main.overdriveState2()[6] != 100:
            unequip = True
    else:
        goGreen = False
        if memory.main.overdriveState2()[6] == 100:
            menu.equip_armor(character=gameVars.neArmor(), ability=0x801D)

    checkpoint = 0
    while memory.main.getMap() != 259:
        if memory.main.userControl():
            if goGreen:
                if checkpoint == 10:
                    goGreen = False
                    checkpoint = 0
                elif targetPathing.set_movement(
                    targetPathing.ne_return_green(checkpoint)
                ):
                    checkpoint += 1
                    print("Checkpoint reached:", checkpoint)
            elif checkpoint < 1 and memory.main.getMap() == 266:
                checkpoint = 1
            elif checkpoint == 2 and unequip:
                menu.equip_armor(character=gameVars.neArmor(), ability=99)
                unequip = False
            elif checkpoint == 2:
                memory.main.touchSaveSphere()
                checkpoint += 1
            elif checkpoint < 7 and memory.main.getMap() == 279:
                checkpoint = 7
            elif targetPathing.set_movement(targetPathing.ne_return(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battleActive():
                battle.main.fleeAll()
            elif memory.main.diagSkipPossible() or memory.main.menuOpen():
                xbox.tapB()
