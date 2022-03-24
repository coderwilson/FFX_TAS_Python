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
    FFX_memory.fullPartyFormat('Kimahri')
    FFX_memory.printManipInfo()
    checkpoint = 0
    while FFX_memory.getMap() != 56:
        #print(FFX_memory.getMap())
        if FFX_memory.userControl():
            if checkpoint < 5 and FFX_memory.getMap() == 266:
                checkpoint = 5
            if checkpoint == 8 and FFX_memory.nextChanceRNG12() >= 1:
                checkpoint -= 2
            elif checkpoint == 9:
                FFXC.set_movement(-1, 1)
            elif FFX_targetPathing.setMovement(FFX_targetPathing.neApproach(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                if FFX_memory.nextChanceRNG12() >= 1:
                    FFX_Battle.advanceRNG12()
                else:
                    FFX_Battle.fleeAll()
                FFX_memory.fullPartyFormat('Kimahri')
                FFX_memory.printManipInfo()
            elif FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
                FFX_Xbox.tapB()
        

def dropHunt():
    print("Now in the cave. Ready to try to get the NE armor.")
    FFX_memory.setEncounterRate(1) #Testing only
    FFX_memory.fullPartyFormat('Kimahri')
    FFX_memory.printManipInfo()
    checkpoint = 0
    while gameVars.neArmor() == 255:
        if FFX_memory.userControl():
            if FFX_targetPathing.setMovement(FFX_targetPathing.neForceEncounters(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                if FFX_memory.nextChanceRNG12() == 0 and FFX_memory.nextChanceRNG10() == 0:
                    FFX_Battle.ghostKill()
                    FFX_memory.checkNEArmor()
                else:
                    FFX_Battle.advanceRNG10(FFX_memory.nextChanceRNG10())
                FFX_Battle.healUp(fullMenuClose=True)
                if gameVars.neArmor() == 255:
                    FFX_memory.fullPartyFormat('Kimahri')
                    FFX_memory.printManipInfo()
            elif FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
                FFX_Xbox.tapB()
    print("The NE armor hunt is complete.")

def returnToGagazet():
    checkpoint = 0
    FFX_menu.equipArmor(character=gameVars.neArmor(),ability=0x801D)
    while FFX_memory.getMap() != 259:
        if FFX_memory.userControl():
            if checkpoint < 1 and FFX_memory.getMap() == 266:
                checkpoint = 1
            elif checkpoint == 2:
                FFX_memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint < 7 and FFX_memory.getMap() == 279:
                checkpoint = 7
            elif FFX_targetPathing.setMovement(FFX_targetPathing.neReturn(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                FFX_Battle.fleeAll()
            elif FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
                FFX_Xbox.tapB()
    