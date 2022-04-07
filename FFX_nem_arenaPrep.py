import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_memory
import FFX_targetPathNem
import FFX_vars
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()

#The following functions extend the regular Bahamut run. Farming sections.

def airShipDestination(destNum=0): #Default to Besaid. Maybe based on map number?
    while FFX_memory.oakaGilCursor() != 20:
        if FFX_memory.userControl():
            FFX_targetPathNem.setMovement([-251,340])
        else:
            FFXC.set_neutral()
        FFX_Xbox.menuB()
    print("Destination select on screen now.")
    while FFX_memory.mapCursor() != destNum:
        FFX_memory.menuDirection(FFX_memory.mapCursor(), destNum, 13)
    FFX_Xbox.tapB()
    FFX_memory.waitFrames(2)
    FFX_Xbox.tapB()
    FFX_memory.awaitControl()

def getSaveSphereDetails():
    mapVal = FFX_memory.getMap()
    storyVal = FFX_memory.getStoryProgress()
    print("Map and story: ", mapVal, " | ", storyVal)
    x = 0
    y = 0
    diag = 0
    if mapVal == 19:
        #Besaid beach
        x = -310
        y = -475
        diag = 55
    if mapVal == 263:
        #Thunder Plains agency
        x = -30
        y = -10
        diag = 114
    
    print("Values: [", x, ",", y, "] - ", diag)
    return [x,y,diag]

def returnToAirship():
    print("Attempting Return to Airship")
    
    ssDetails = getSaveSphereDetails()
    
    if FFX_memory.userControl():
        while FFX_memory.userControl():
            FFX_targetPathNem.setMovement([ssDetails[0], ssDetails[1]])
            FFX_Xbox.tapB()
            FFX_memory.waitFrames(1)
    try:
        FFXC.set_neutral()
    except:
        FFXC = FFX_Xbox.controllerHandle()
        FFXC.set_neutral()
    FFXC.set_neutral()
    
    while FFX_memory.getMap() != 194:
        #print("|", FFX_memory.saveMenuCursor())
        #print("+", FFX_memory.saveMenuCursor2())
        if FFX_memory.saveMenuOpen():
            FFX_Xbox.tapA()
        elif FFX_memory.diagProgressFlag() == ssDetails[2]:
            #print("Cursor test: ", FFX_memory.saveMenuCursor())
            if FFX_memory.saveMenuCursor() != 1:
                FFX_Xbox.menuDown()
            else:
                FFX_Xbox.menuB()
        elif FFX_memory.userControl():
            FFX_Xbox.menuB()
        FFX_memory.waitFrames(4)
    print("Return to Airship Complete.")
    FFX_memory.clearSaveMenuCursor()
    FFX_memory.clearSaveMenuCursor2()

def battleFarmAll():
    print("Battle Start")
    FFXC.set_neutral()
    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            if FFX_Screen.turnTidus() or FFX_Screen.turnYuna():
                if FFX_memory.getBattleNum() in [154,156,164]:
                    #Confusion is a dumb mechanic in this game.
                    FFX_Battle.attackByNum(22,'l')
                else:
                    FFX_Battle.attack('none')
            else:
                FFX_Battle.escapeOne()
    FFX_memory.clickToControl()
    FFX_Battle.healUp(3)
  
def besaidFarm():
    airShipDestination(destNum=0)
    
    FFX_memory.fullPartyFormat('gauntlet',fullMenuClose=False)
    FFX_menu.equipWeapon(character=0,ability=0x807A, fullMenuClose=False)
    FFX_menu.equipWeapon(character=1,ability=0x807A, fullMenuClose=False)
    FFX_menu.equipArmor(character=gameVars.neArmor(),ability=99) #Unequip
    
    checkpoint = 0
    while not FFX_memory.getMap() == 194:
        if FFX_memory.userControl():
            if FFX_memory.arenaFarmCheck(zone="besaid",endGoal=1,report=False) and checkpoint < 15:
                checkpoint = 15
            elif checkpoint == 15 and not FFX_memory.arenaFarmCheck(zone="besaid",endGoal=1,report=False):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)
                
            elif checkpoint == 1:
                FFX_memory.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 11:
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 16 and FFX_memory.getMap() == 20:
                checkpoint += 1
            elif checkpoint == 25:
                FFX_memory.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 26:
                returnToAirship()
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.besaidFarm(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                battleFarmAll()
                FFX_memory.arenaFarmCheck(zone="besaid",endGoal=1,report=True)
            elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
   
def tPlains(capNum:int=1):
    airShipDestination(destNum=7)
    
    FFX_memory.fullPartyFormat('yuna',fullMenuClose=False)
    FFX_menu.equipWeapon(character=0,ability=0x807A, fullMenuClose=False)
    FFX_menu.equipWeapon(character=1,ability=0x807A, fullMenuClose=False)
    FFX_menu.equipArmor(character=gameVars.neArmor(),ability=99) #Unequip
    
    checkpoint = 0
    while not FFX_memory.getMap() == 194:
        if FFX_memory.userControl():
            if FFX_memory.dodgeLightning(gameVars.getLStrike()):
                print("Strike!")
                gameVars.setLStrike(FFX_memory.lStrikeCount())
            elif FFX_memory.arenaFarmCheck(zone="tPlains",endGoal=capNum,report=False) and checkpoint < 8:
                FFX_menu.equipArmor(character=gameVars.neArmor(),ability=0x801D)
                checkpoint = 8
            elif checkpoint == 9 and not FFX_memory.arenaFarmCheck(zone="tPlains",endGoal=capNum,report=False):
                checkpoint -= 2
            
            #Map changes:
            elif checkpoint == 1 and FFX_memory.getMap() == 256:
                checkpoint += 1
            elif checkpoint == 3 and FFX_memory.getMap() == 162:
                checkpoint += 1
            elif checkpoint == 11 and FFX_memory.getMap() == 256:
                checkpoint += 1
            elif checkpoint == 14:
                FFX_memory.clickToEventTemple(6)
                checkpoint += 1
            elif checkpoint == 16:
                returnToAirship()
                break
            
            #General pathing
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.tpFarm(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                battleFarmAll()
                FFX_memory.arenaFarmCheck(zone="tPlains",endGoal=capNum,report=True)
            elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    print("End of Thunder Plains section")

def calm(capNum:int=1):
    airShipDestination(destNum=11)
    FFX_menu.equipArmor(character=gameVars.neArmor(),ability=99) #Unequip
    
    checkpoint = 0
    while not FFX_memory.getMap() == 307:
        if FFX_memory.userControl():
            if FFX_memory.arenaFarmCheck(zone="calm",endGoal=capNum,report=False) and checkpoint < 7:
                FFX_menu.equipArmor(character=gameVars.neArmor(),ability=0x801D)
                checkpoint = 7
            elif checkpoint == 7 and not FFX_memory.arenaFarmCheck(zone="calm",endGoal=capNum,report=False):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.calm(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                battleFarmAll()
                FFX_memory.arenaFarmCheck(zone="calm",endGoal=capNum,report=True)
            elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
