import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_menuGrid
import FFX_memory
import FFX_Logs
import FFX_targetPathing
import FFX_vars

FFXC = FFX_Xbox.controllerHandle()
gameVars = FFX_vars.varsHandle()
#FFXC = FFX_Xbox.FFXC

def arrival():
    print("Arrived at Kilika docks.")
    FFX_memory.clickToControl()
    
    checkpoint = 0
    while FFX_memory.getMap() != 18:
        if FFX_memory.userControl():
            #events
            if checkpoint == 4: #Move into Yuna's dance
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            if checkpoint == 6: #Move into Yuna's dance
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 8: #Exit the inn
                FFXC.set_movement(-1, -1) #Can be improved, there's a tiny ledge to get stuck on.
                FFX_memory.awaitEvent()
                FFX_memory.waitFrames(5)
                FFX_memory.awaitControl()
                checkpoint += 1
            elif checkpoint == 12: #Back to first map
                FFX_memory.clickToEventTemple(3)
                checkpoint += 1
            elif checkpoint == 16: #Talking to Wakka
                FFX_memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 18: #Back to the map with the inn
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.Kilika1(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
                
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.menuB()
            elif FFX_memory.cutsceneSkipPossible():
                FFX_Xbox.skipSceneSpec()
                
            #Map changes
            elif checkpoint < 7 and FFX_memory.getMap() == 152:
                checkpoint = 7

def forest1():
    kilikaBattles = 0
    optimalBattles = 0
    
    valeforCharge = False
    checkpoint = 0
    while FFX_memory.getMap() != 108: #All the way into the trials
        if FFX_memory.userControl():
            if checkpoint == 48 or checkpoint == 49:
                #print("Valefor charge state: ", valeforCharge)
                if valeforCharge == True:
                    checkpoint = 50
            if checkpoint == 50 and valeforCharge == False:
                checkpoint = 48
            
            #events
            if checkpoint == 6: #Chest with Wakka's weapon Scout
                FFX_memory.clickToEventTemple(0)
                woodsMenuing()
                checkpoint += 1
            elif checkpoint == 31: #Luck sphere chest
                luckSlot = FFX_memory.getItemSlot(94)
                if luckSlot == 255:
                    FFX_targetPathing.setMovement([-250,200])
                    FFX_Xbox.tapB()
                else:
                    checkpoint += 1
            elif checkpoint == 52:
                FFXC.set_neutral()
                FFX_memory.waitFrames(5)
                FFXC.set_movement(1, 0)
                FFX_memory.waitFrames(2)
                FFXC.set_neutral()
                FFX_memory.waitFrames(4)
                FFX_memory.touchSaveSphere()
                FFX_menu.Geneaux()
                checkpoint += 1
            elif checkpoint == 63 and not gameVars.csr(): #Lord O'holland
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 63 and gameVars.csr():
                #FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 67: #Into the trials
                FFXC.set_movement(0, 1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_memory.clickToControl()
                checkpoint += 1
            
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.Kilika2(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
                
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                if checkpoint < 3:
                    FFX_Battle.lancetTutorial()
                elif checkpoint > 50:
                    FFX_Battle.Geneaux()
                else:
                    valeforCharge = FFX_Battle.KilikaWoods(valeforCharge)
                    kilikaBattles += 1
                    if FFX_memory.getBattleNum() in [32, 34, 37]:
                        optimalBattles += 1
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
                
            #Map changes
            elif checkpoint < 51 and FFX_memory.getMap() == 65: #Stairs
                checkpoint = 51
            elif checkpoint < 59 and FFX_memory.getMap() == 78: #Temple Entrance
                checkpoint = 59
            elif checkpoint < 61 and FFX_memory.getMap() == 96: #Temple interior
                checkpoint = 61
    FFX_Logs.writeStats("Kilika battles (North):")
    FFX_Logs.writeStats(str(kilikaBattles))
    FFX_Logs.writeStats("Kilika optimal battles (North):")
    FFX_Logs.writeStats(str(optimalBattles))

def woodsMenuing():
    #Tidus learning Flee
    FFX_menu.openGrid(character=0)
    FFX_Xbox.menuB()
    FFX_Xbox.menuB() #Sphere grid on Tidus
    FFX_menuGrid.moveFirst()
    FFX_menuGrid.gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('ability', 'd', 'none')
    FFX_menuGrid.useAndQuit()
    #Reorder the party
    
    FFX_memory.fullPartyFormat('kilikawoods1', fullMenuClose=False)
    FFX_menu.equipScout(fullMenuClose=True)

def forest2():
    print("forest2 function no longer used")

def Geneaux():
    print("Geneaux function no longer used")

def trials():
    FFX_memory.clickToControl()
    checkpoint = 0
    while FFX_memory.getMap() != 18:
        if FFX_memory.userControl():
            #Spheres and glyphs
            if checkpoint == 2: #First sphere
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 5: #Insert and remove, opens door
                FFX_memory.clickToEventTemple(0)
                FFX_memory.waitFrames(30 * 0.07)
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 9: #Insert and remove, generate glyph
                FFX_memory.clickToEventTemple(0)
                FFX_memory.waitFrames(30 * 0.07)
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 11: #Put the sphere out of the way
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 13: #Touch glyph
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 18: #Kilika sphere (in the way)
                FFX_memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 25: #Kilika sphere (now out of the way)
                FFX_memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 27: #Glyph sphere
                while not FFX_memory.diagSkipPossible():
                    FFX_targetPathing.setMovement([-19, -30])
                    FFX_Xbox.tapB()
                    FFX_memory.waitFrames(6)
                FFXC.set_neutral()
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 33: #Insert Glyph sphere
                FFX_memory.clickToEventTemple(1)
                checkpoint += 1
            elif checkpoint == 39: #Pick up last Kilika sphere
                FFX_memory.clickToEventTemple(2)
                checkpoint += 1
            elif checkpoint == 50: #Insert and remove, opens door
                FFX_memory.clickToEventTemple(0)
                FFX_memory.waitFrames(30 * 0.07)
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 53 and gameVars.csr():
                FFX_memory.awaitControl()
                FFXC.set_movement(0, 1)
                FFX_memory.waitFrames(2)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_Xbox.nameAeon() #Set Ifrit name
                checkpoint = 55
            elif checkpoint == 54 and not gameVars.csr(): #Talk to Wakka
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 56: #Leave inner sanctum
                FFXC.set_movement(0, -1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_Xbox.nameAeon() #Set Ifrit name
                checkpoint += 1
            elif checkpoint == 57: #Leaving the temple
                FFX_memory.clickToEventTemple(4)
                checkpoint += 1
        
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.KilikaTrials(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
                
            #Map changes
            elif checkpoint < 53 and FFX_memory.getMap() == 45: #Inner sanctum
                checkpoint = 53

def forest3():
    #First, re-order the party
    FFX_memory.fullPartyFormat('kilika')
    kilikaBattles = 0
    optimalBattles = 0
    checkpoint = 0
    while checkpoint < 40: #All the way to the boats
        if FFX_memory.userControl():
            #Events
            if checkpoint == 39:
                FFXC.set_movement(0, -1)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_Xbox.SkipDialog(0.3)
                FFX_memory.clickToControl3()
                checkpoint += 1
            
            #General pathing
            elif FFX_targetPathing.setMovement(FFX_targetPathing.Kilika3(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                FFX_Battle.KilikaWoods(True)
                kilikaBattles += 1
                if FFX_memory.getBattleNum() in [32, 34, 37]:
                    optimalBattles += 1
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
                
            #Map changes
            elif checkpoint < 30 and FFX_memory.getMap() == 46: #Exit woods
                checkpoint = 30
            elif checkpoint < 37 and FFX_memory.getMap() == 16: #Map with boat
                checkpoint = 37
    FFX_Logs.writeStats("Kilika battles (South):")
    FFX_Logs.writeStats(str(kilikaBattles))
    FFX_Logs.writeStats("Kilika optimal battles (South):")
    FFX_Logs.writeStats(str(optimalBattles))

def departure():
    print("departure function no longer used")

