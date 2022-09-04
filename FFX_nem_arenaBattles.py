import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_nem_menu
import FFX_nem_arenaSelect
import FFX_memory
import FFX_targetPathNem
import FFX_vars
import FFX_Reset
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()

#The following functions extend the regular Bahamut run. Arena battles sections.

def saveGame(firstSave=False):
    while not FFX_targetPathNem.setMovement([-6,-27]):
        pass
    while not FFX_targetPathNem.setMovement([-2,-2]):
        pass
    print("Arena - Touch Save Sphere, and actually save")
    FFXC = FFX_Xbox.controllerHandle()
    FFXC.set_neutral()
    ssDetails = FFX_memory.getSaveSphereDetails()
    
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
    FFX_memory.waitFrames(30)
    FFX_Xbox.tapB()
    FFX_memory.waitFrames(10)
    
    print("Controller is now neutral. Attemption to open save menu.")
    while not FFX_memory.saveMenuOpen():
        pass
    print("Save menu is open.")
    FFX_memory.waitFrames(9)
    if not firstSave:
        FFX_Xbox.menuDown()
        FFX_Xbox.menuB()
        FFX_Xbox.menuLeft()
    FFX_Xbox.menuB() #Select the save file
    FFX_Xbox.menuB() #Confirm the save
    FFX_memory.waitFrames(90)
    FFX_Xbox.menuA() #Back out
    FFX_Xbox.menuA() #Back out
    FFX_Xbox.menuA() #Back out
    FFX_Xbox.menuA() #Back out
    
    print("Menu now closed. Back to the battles.")
    FFX_memory.clearSaveMenuCursor()
    FFX_memory.clearSaveMenuCursor2()
    while not FFX_targetPathNem.setMovement([-6,-27]):
        pass
    while not FFX_targetPathNem.setMovement([2,-25]):
        pass

def touchSave(realSave=False):
    while not FFX_targetPathNem.setMovement([-6,-27]):
        pass
    while not FFX_targetPathNem.setMovement([-2,-2]):
        pass
    FFX_memory.touchSaveSphere()
    while not FFX_targetPathNem.setMovement([-6,-27]):
        pass
    while not FFX_targetPathNem.setMovement([2,-25]):
        pass
    arenaNPC()

def airShipDestination(destNum=0): #Default to Sin.
    while FFX_memory.getMap() != 382:
        if FFX_memory.userControl():
            FFX_targetPathNem.setMovement([-251,340])
        else:
            FFXC.set_neutral()
        FFX_Xbox.menuB()
    while FFX_memory.diagProgressFlag() != 4:
        FFX_Xbox.menuB()
    print("Destination select on screen now.")
    while FFX_memory.mapCursor() != destNum:
        if destNum < 8:
            FFX_Xbox.tapDown()
        else:
            FFX_Xbox.tapUp()
    FFX_Xbox.tapB()
    FFX_memory.waitFrames(2)
    FFX_Xbox.tapB()
    FFX_memory.clickToControl3()

def getSaveSphereDetails():
    mapVal = FFX_memory.getMap()
    storyVal = FFX_memory.getStoryProgress()
    print("Map and story:", mapVal, "|", storyVal)
    x = 0
    y = 0
    diag = 0
    if mapVal == 322:
        #Inside Sin, next to airship
        x = 225
        y = -250
        diag = 15
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
    if mapVal == 307:
        #Monster Arena
        x = 4
        y = 5
        diag = 166
    if mapVal == 98:
        #Kilika docks
        x = 46
        y = -252
        diag = 34
    if mapVal == 92:
        #MRR start
        x = -1
        y = -740
        diag = 43
    if mapVal == 266:
        #Calm Lands Gorge
        x = -310
        y = 190
        diag = 43
    if mapVal == 82:
        #Djose temple
        x = 100
        y = -240
        diag = 89
    if mapVal == 221:
        #Macalania Woods, near Spherimorph
        x = 197
        y = -120
        diag = 23
    if mapVal == 137:
        #Bikanel Desert
        x = -15
        y = 240
        diag = 31
    if mapVal == 313:
        #Zanarkand campfire
        x = 135
        y = -1
        diag = 4
    if mapVal == 327:
        #Sin, end zone
        x = -37
        y = -508
        diag = 10
    if mapVal == 258:
        #Omega (only used in Nemesis)
        x = -112
        y = -1066
        diag = 23
    
    print("Values: [", x, ",", y, "] -", diag)
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
    
    while not FFX_memory.getMap() in [194,374]:
        if FFX_memory.getMap() == 307 and FFX_memory.getCoords()[1] < -5:
            while not FFX_targetPathNem.setMovement([-4,-21]):
                pass
            while not FFX_targetPathNem.setMovement([-2,-2]):
                pass
        else:
            FFXC.set_neutral()
            if FFX_memory.saveMenuOpen():
                FFX_Xbox.tapA()
            elif FFX_memory.diagProgressFlag() == ssDetails[2]:
                #print("Cursor test:", FFX_memory.saveMenuCursor())
                if FFX_memory.saveMenuCursor() != 1:
                    FFX_Xbox.menuDown()
                else:
                    FFX_Xbox.menuB()
            elif FFX_memory.userControl():
                FFX_targetPathNem.setMovement([ssDetails[0], ssDetails[1]])
                FFX_Xbox.menuB()
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.menuB()
            FFX_memory.waitFrames(4)
    print("Return to Airship Complete.")
    FFX_memory.clearSaveMenuCursor()
    FFX_memory.clearSaveMenuCursor2()

def aeonStart():
    FFX_Screen.awaitTurn()
    FFX_Battle.buddySwapYuna()
    FFX_Battle.aeonSummon(4)
    while not FFX_Screen.turnTidus():
        if FFX_memory.turnReady():
            if FFX_Screen.turnAeon():
                FFX_Battle.attack('none')
            else:
                FFX_Battle.defend()

def yojimboBattle():
    #Incomplete
    FFX_Screen.awaitTurn()
    if not 1 in FFX_memory.getActiveBattleFormation():
        FFX_Battle.buddySwapYuna()
    print("+Yuna Overdrive to summon Yojimbo")
    FFX_Battle.yunaOD()
    print("+Pay the man")
    FFX_Battle.yojimboOD()
    FFX_memory.waitFrames(90)
    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            if FFX_Screen.turnTidus():
                FFX_Battle.tidusFlee()
            elif FFX_Screen.turnAeon():
                FFX_Xbox.SkipDialog(2)
            else:
                FFX_Battle.defend()
    
    #After battle stuff
    while not FFX_memory.menuOpen():
        FFX_Xbox.tapB()
    print("Battle is complete.")
    FFXC.set_value('BtnB', 1)
    FFX_memory.waitFrames(180)
    FFXC.set_neutral()
    FFX_memory.waitFrames(2)
    
    return FFX_memory.battleArenaResults()

def autoLife():
    while not (FFX_memory.turnReady() and FFX_Screen.turnTidus()):
        if FFX_memory.turnReady():
            if FFX_Screen.turnAeon():
                FFX_Battle.attack('none')
            elif not FFX_Screen.turnTidus():
                FFX_Battle.defend()
    while FFX_memory.battleMenuCursor() != 22:
        if FFX_Screen.turnTidus() == False:
            print("Attempting Haste, but it's not Tidus's turn")
            FFX_Xbox.tapUp()
            FFX_Xbox.tapUp()
            return
        if FFX_memory.battleMenuCursor() == 1:
            FFX_Xbox.tapUp()
        else:
            FFX_Xbox.tapDown()
    while not FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    FFX_Battle._navigate_to_position(1)
    while FFX_memory.otherBattleMenu():
        FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()
    FFX_Xbox.tapB()

def basicQuickAttacks(megaPhoenix = False, odVersion:int=0, yunaAutos=False):
    print("### Battle Start:", FFX_memory.getEncounterID())
    FFXC.set_neutral()
    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            if FFX_Screen.turnTidus():
                if megaPhoenix and FFX_Screen.faintCheck() >= 2:
                    FFX_Battle.revive(itemNum = 7)
                elif FFX_memory.getOverdriveBattle(0) == 100:
                    FFX_Battle.tidusOD(version=odVersion)
                else:
                    FFX_Battle.useSkill(1) #Quick hit
            elif FFX_Screen.turnAeon():
                FFX_Battle.attack('none')
            else:
                FFX_Battle.defend()
    
    #After battle stuff
    while not FFX_memory.menuOpen():
        FFX_Xbox.tapB()
    FFXC.set_value('BtnB', 1)
    FFX_memory.waitFrames(150)
    FFXC.set_neutral()
    FFX_memory.waitFrames(2)
    return FFX_memory.battleArenaResults()

def basicAttack(megaPhoenix = False, odVersion:int=0,useOD=False, yunaAutos=False):
    print("### Battle Start:", FFX_memory.getEncounterID())
    FFXC.set_neutral()
    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            if FFX_Screen.turnTidus():
                if megaPhoenix and FFX_Screen.faintCheck() >= 2:
                    FFX_Battle.revive(itemNum = 7)
                elif useOD and FFX_memory.getOverdriveBattle(0) == 100:
                    FFX_Battle.tidusOD(version=odVersion)
                else:
                    FFX_Battle.attack('none')
            elif FFX_Screen.turnYuna() and yunaAutos:
                attack('none')
            elif FFX_Screen.turnAeon():
                attack('none')
            else:
                FFX_Battle.defend()
    
    #After battle stuff
    while not FFX_memory.menuOpen():
        FFX_Xbox.tapB()
    FFXC.set_value('BtnB', 1)
    FFX_memory.waitFrames(150)
    FFXC.set_neutral()
    FFX_memory.waitFrames(2)
    return FFX_memory.battleArenaResults()

def arenaNPC():
    if FFX_memory.getMap() != 307:
        return
    while not (FFX_memory.diagProgressFlag() == 74 and FFX_memory.diagSkipPossible()):
        if FFX_memory.userControl():
            if FFX_memory.getCoords()[1] > -15:
                print("Wrong position, moving away from sphere")
                while not FFX_targetPathNem.setMovement([-6,-27]):
                    pass
                while not FFX_targetPathNem.setMovement([2,-25]):
                    pass
            else:
                print("Engaging NPC")
                FFX_targetPathNem.setMovement([5,-12])
                FFX_Xbox.tapB()
        else:
            FFXC.set_neutral()
            if FFX_memory.diagProgressFlag() == 59:
                FFX_Xbox.menuA()
                FFX_Xbox.menuA()
                FFX_Xbox.menuA()
                FFX_Xbox.tapB()
            elif FFX_memory.diagSkipPossible() and not FFX_memory.diagProgressFlag() == 74:
                FFX_Xbox.tapB()
    print("Mark 1")
    FFX_memory.waitFrames(30) #This buffer can be improved later.
    print("Mark 2")

def restockDowns():
    print("Restocking phoenix downs")
    if FFX_memory.getItemCountSlot(FFX_memory.getItemSlot(6)) >= 80:
        print("Restock not needed. Disregard.")
        return
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(3)
    FFX_memory.waitFrames(60)
    FFX_Xbox.tapB()
    FFX_memory.waitFrames(6)
    while FFX_memory.equipBuyRow() != 2:
        if FFX_memory.equipBuyRow() < 2:
            FFX_Xbox.tapDown()
        else:
            FFX_Xbox.tapUp()
    FFX_Xbox.tapB()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapB()
    FFX_memory.waitFrames(6)
    FFX_Xbox.menuA()
    FFX_memory.waitFrames(6)
    FFX_Xbox.menuA()

def battles1():
    if not FFX_memory.equippedArmorHasAbility(charNum=1, abilityNum=0x800A):
        FFX_menu.equipArmor(character=1,ability=0x800A, fullMenuClose=False)
    if not FFX_memory.equippedArmorHasAbility(charNum=4, abilityNum=0x800A):
        FFX_menu.equipArmor(character=4,ability=0x800A)
    FFX_memory.closeMenu()
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=0)
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=0)
    gameVars.arenaSuccess(arrayNum=0,index=0)
    restockDowns()
    
    checkYojimboPossible()
    
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=1)
    aeonStart()
    autoLife()
    while not basicQuickAttacks(megaPhoenix = True):
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(4)
        FFX_memory.fullPartyFormat('kilikawoods1')
        touchSave()
        arenaNPC()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=1)
        aeonStart()
        if FFX_Screen.turnTidus():
            autoLife()
    gameVars.arenaSuccess(arrayNum=0,index=1)
    restockDowns()
    FFX_nem_arenaSelect.arenaMenuSelect(4)
    FFX_memory.fullPartyFormat('kilikawoods1')
    FFX_menu.tidusSlayer(odPos=0)
    
    checkYojimboPossible()
    
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=2)
    while not basicQuickAttacks(yunaAutos=True):
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=2)
    gameVars.arenaSuccess(arrayNum=0,index=2)
    restockDowns()
    
    checkYojimboPossible()
    
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=3)
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=3)
    gameVars.arenaSuccess(arrayNum=0,index=3)
    restockDowns()
    
    checkYojimboPossible()
    
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=4)
    autoLife()
    while not basicQuickAttacks(megaPhoenix=True):
        print("Battle not completed successfully.")
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=4)
        autoLife()
    gameVars.arenaSuccess(arrayNum=0,index=4)
    restockDowns()
    
    checkYojimboPossible()
    
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=5)
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=5)
    gameVars.arenaSuccess(arrayNum=0,index=5)
    restockDowns()
    
    checkYojimboPossible()
    
    FFX_nem_arenaSelect.arenaMenuSelect(4)
    FFX_menu.tidusSlayer(odPos=2)
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=6)
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=6)
    gameVars.arenaSuccess(arrayNum=0,index=6)
    restockDowns()
    
    checkYojimboPossible()
    
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=7)
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=7)
    gameVars.arenaSuccess(arrayNum=0,index=7)
    restockDowns()
    
    checkYojimboPossible()
    
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=8)
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=8)
    gameVars.arenaSuccess(arrayNum=0,index=8)
    restockDowns()
    
    checkYojimboPossible()
    
    FFX_nem_arenaSelect.arenaMenuSelect(4)
    FFX_menu.tidusSlayer(odPos=0)
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=9)
    while not basicQuickAttacks(yunaAutos=True):
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=9)
    gameVars.arenaSuccess(arrayNum=0,index=9)
    restockDowns()
    
    checkYojimboPossible()
    
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=10)
    autoLife()
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=10)
        autoLife()
    gameVars.arenaSuccess(arrayNum=0,index=10)
    restockDowns()
    
    checkYojimboPossible()
    
def battles2():
    print("++Starting second section++")
    FFX_nem_arenaSelect.arenaMenuSelect(4)
    touchSave()
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=1)
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(4)
        touchSave()
        arenaNPC()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=1)
    gameVars.arenaSuccess(arrayNum=1,index=1)
    restockDowns()
    
    checkYojimboPossible()
    
    FFX_nem_arenaSelect.arenaMenuSelect(4)
    touchSave()
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=3)
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=3)
    gameVars.arenaSuccess(arrayNum=1,index=3)
    restockDowns()
    
    checkYojimboPossible()
    
    FFX_nem_arenaSelect.arenaMenuSelect(4)
    touchSave()
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=5)
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=5)
    gameVars.arenaSuccess(arrayNum=1,index=5)
    restockDowns()
    
    checkYojimboPossible()
    
    FFX_nem_arenaSelect.arenaMenuSelect(4)
    touchSave()
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=8)
    while not basicQuickAttacks():
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=8)
    gameVars.arenaSuccess(arrayNum=1,index=8)
    restockDowns()
    FFX_nem_arenaSelect.arenaMenuSelect(4)
    touchSave()
    
    checkYojimboPossible()

def jugFarmDone():
    print("||| Slot:", FFX_memory.getItemSlot(87))
    if FFX_memory.getItemSlot(87) > 250:
        return False
    else:
        print("Count:", FFX_memory.getItemCountSlot(FFX_memory.getItemSlot(87)))
        if FFX_memory.getItemCountSlot(FFX_memory.getItemSlot(87)) < 6:
            return False
    return True

def juggernautFarm():
    checkYojimboPossible()
    while not jugFarmDone():
        arenaNPC()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=12)
        autoLife()
        basicQuickAttacks(megaPhoenix=True,odVersion=1)
        restockDowns()
        checkYojimboPossible()
        FFX_nem_arenaSelect.arenaMenuSelect(4)
        touchSave()
    print("Good to go on strength spheres")
    gameVars.arenaSuccess(arrayNum=1,index=12)
    print("Starting menu to finish strength.")
    FFX_nem_arenaSelect.arenaMenuSelect(4)
    FFX_nem_menu.strBoost()
    print("Touch save sphere, and then good to go.")
    touchSave()
    
def battles3():
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=11)
    autoLife()
    while not basicQuickAttacks(megaPhoenix=True):
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=11)
        autoLife()
    gameVars.arenaSuccess(arrayNum=0,index=11)
    restockDowns()
    
    checkYojimboPossible()
    
    FFX_nem_arenaSelect.arenaMenuSelect(4)
    touchSave()
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=2)
    aeonStart()
    autoLife()
    while not basicAttack(useOD=False):
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(4)
        touchSave()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=2)
        autoLife()
    gameVars.arenaSuccess(arrayNum=1,index=2)
    restockDowns()
    
    checkYojimboPossible()
    
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=0)
    autoLife()
    while not basicQuickAttacks(megaPhoenix=True,odVersion=1):
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=0)
        autoLife()
    gameVars.arenaSuccess(arrayNum=1,index=0)
    restockDowns()
    
    checkYojimboPossible()
    
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=9)
    autoLife()
    while not basicQuickAttacks(megaPhoenix=True,odVersion=1):
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=9)
        autoLife()
    gameVars.arenaSuccess(arrayNum=1,index=9)
    restockDowns()
    
    checkYojimboPossible()
    
    FFX_nem_arenaSelect.arenaMenuSelect(4)
    touchSave()
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=10)
    autoLife()
    while not basicQuickAttacks(megaPhoenix=True,odVersion=1):
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=10)
        autoLife()
    gameVars.arenaSuccess(arrayNum=1,index=10)
    restockDowns()
    
    checkYojimboPossible()

def battles4():
    FFX_nem_arenaSelect.arenaMenuSelect(4)
    touchSave()
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=15,monsterIndex=0)
    autoLife()
    while not basicQuickAttacks(megaPhoenix=True,odVersion=1):
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=15,monsterIndex=0)
        autoLife()
    gameVars.arenaSuccess(arrayNum=2,index=0)
    restockDowns()
    
    checkYojimboPossible()
    FFX_nem_arenaSelect.arenaMenuSelect(4)
    touchSave()
    
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=15,monsterIndex=6)
    
    while not shinryuBattle():
        print("Battle not completed successfully.")
        restockDowns()
        FFX_nem_arenaSelect.arenaMenuSelect(4)
        touchSave()
        arenaNPC()
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=15,monsterIndex=6)
    
    gameVars.arenaSuccess(arrayNum=2,index=6)
    restockDowns()

def itemDump():
    FFX_nem_arenaSelect.arenaMenuSelect(2)
    FFX_memory.waitFrames(90)
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    FFX_menu.sellAll(NEA=True)
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()

def quickResetLogic():
    FFX_Reset.resetToMainMenu()
    FFX_memory.waitFrames(90)
    while FFX_memory.getMap() != 23:
        FFXC.set_value('BtnStart', 1)
        FFX_memory.waitFrames(2)
        FFXC.set_value('BtnStart', 0)
        FFX_memory.waitFrames(2)
    FFX_memory.waitFrames(60)
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(60)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFXC.set_neutral()
    gameVars.printArenaStatus()
    FFX_memory.waitFrames(30)

def checkYojimboPossible():
    if FFX_memory.overdriveState2()[1] < 100:
        return False
    if FFX_memory.overdriveState2()[1] == 100 and FFX_memory.getGilvalue() < 300000:
        itemDump()
    
    if FFX_memory.overdriveState2()[1] == 100 and FFX_memory.getGilvalue() >= 300000:
        #Save game in preparation for the Yojimbo attempt
        FFX_memory.waitFrames(20)
        FFX_nem_arenaSelect.arenaMenuSelect(4)
        FFX_memory.fullPartyFormat('kilikawoods1')
        if gameVars.yojimboGetIndex() == 1:
            saveGame(firstSave=True)
        else:
            saveGame(firstSave=False)
            
        #Now attempt to get Zanmato until successful, no re-saving.
        while not battles5(gameVars.yojimboGetIndex()):
            quickResetLogic()
        return True
    else:
        return False

def shinryuBattle():
    rikkuFirstTurn=False
    rikkuDriveComplete=False
    FFX_Screen.awaitTurn()
    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            if FFX_Screen.turnRikku():
                if rikkuFirstTurn == False:
                    FFX_Battle.defend()
                elif rikkuDriveComplete:
                    FFX_Battle._useHealingItem(itemID=9)
                else:
                    FFX_Battle.rikkuFullOD('shinryu')
                    rikkuDriveComplete=True
            elif FFX_Screen.turnTidus():
                if FFX_memory.getOverdriveBattle(0) == 100:
                    FFX_Battle.tidusOD(version=1)
                elif rikkuDriveComplete and not FFX_memory.autoLifeState():
                    autoLife()
                else:
                    FFX_Battle.attack('none')
            else:
                FFX_Battle.defend()
    
    #After battle stuff
    while not FFX_memory.menuOpen():
        FFX_Xbox.tapB()
    FFXC.set_value('BtnB', 1)
    FFX_memory.waitFrames(150)
    FFXC.set_neutral()
    FFX_memory.waitFrames(2)
    return FFX_memory.battleArenaResults()

def battles5(completionVersion:int):
    print("Yojimbo battle number:", completionVersion)
    if completionVersion >= 12 and completionVersion != 99:
        return True #These battles are complete at this point.
    yojimboSuccess = False
    
    #Now for the Yojimbo section
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    
    #Battles here
    if completionVersion == 1:
        FFX_nem_arenaSelect.startFight(areaIndex=15,monsterIndex=1)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=2,index=1)
            yojimboSuccess = True
    
    elif completionVersion == 2:
        FFX_nem_arenaSelect.startFight(areaIndex=15,monsterIndex=2)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=2,index=2)
            yojimboSuccess = True
    
    elif completionVersion == 3:
        FFX_nem_arenaSelect.startFight(areaIndex=15,monsterIndex=3)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=2,index=3)
            yojimboSuccess = True
    
    elif completionVersion == 4:
        FFX_nem_arenaSelect.startFight(areaIndex=15,monsterIndex=4)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=2,index=4)
            yojimboSuccess = True
    
    elif completionVersion == 5:
        FFX_nem_arenaSelect.startFight(areaIndex=15,monsterIndex=5)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=2,index=5)
            yojimboSuccess = True
    
    elif completionVersion == 6:
        FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=12)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=0,index=12)
            yojimboSuccess = True
    
    elif completionVersion == 7:
        FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=13)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=1,index=13)
            yojimboSuccess = True
    
    elif completionVersion == 8:
        FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=11)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=1,index=11)
            yojimboSuccess = True
        
    elif completionVersion == 9:
        FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=7)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=1,index=7)
            yojimboSuccess = True
    
    elif completionVersion == 10:
        FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=6)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=1,index=6)
            yojimboSuccess = True
    
    
    elif completionVersion == 11:
        FFX_nem_arenaSelect.startFight(areaIndex=14,monsterIndex=4)
        if yojimboBattle():
            gameVars.arenaSuccess(arrayNum=1,index=4)
            yojimboSuccess = True
    
    
    elif completionVersion == 99: #Nemesis
        FFX_nem_arenaSelect.startFight(areaIndex=15,monsterIndex=7)
        if yojimboBattle():
            FFX_memory.clickToDiagProgress(2)
            FFX_memory.clickToControl3()
            return True
        else:
            return False
    
    
    #Wrap up decisions
    if yojimboSuccess == True:
        gameVars.yojimboIncrementIndex()
        if completionVersion != 99:
            restockDowns()
        return True
    else:
        FFX_nem_arenaSelect.arenaMenuSelect(4)
        return False

def rechargeYuna():
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=13,monsterIndex=9)
    FFX_Screen.awaitTurn()
    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            if FFX_Screen.turnYuna():
                FFX_Battle.attack('none')
            else:
                FFX_Battle.escapeOne()

def nemesisBattle():
    if gameVars.yojimboGetIndex() < 12:
        FFX_nem_arenaSelect.arenaMenuSelect(4)
        touchSave()
        while gameVars.yojimboGetIndex() < 12:
            #If Yuna is charged, do next battle. Otherwise charge.
            if FFX_memory.overdriveState2()[1] == 100:
                battles5(gameVars.yojimboGetIndex())
            else:
                rechargeYuna()
            FFX_nem_arenaSelect.arenaMenuSelect(4)
            touchSave()
                
    if FFX_memory.overdriveState2()[1] != 100:
        rechargeYuna()
    if FFX_memory.getGilvalue() < 300000:
        FFX_nem_arenaSelect.arenaMenuSelect(4)
        FFX_menu.autoSortEquipment()
        #FFX_menu.autoSortItems()
        arenaNPC()
        FFX_nem_arenaSelect.arenaMenuSelect(2)
        FFX_memory.waitFrames(90)
        FFX_Xbox.menuRight()
        FFX_Xbox.menuB()
        FFX_menu.sellAll()
        FFX_Xbox.menuA()
        FFX_Xbox.menuA()
        FFX_Xbox.menuA()
        FFX_Xbox.menuA()
        FFX_Xbox.menuA()
        FFX_Xbox.menuA()
        FFX_Xbox.menuA()
    FFX_nem_arenaSelect.arenaMenuSelect(4)
    FFX_memory.fullPartyFormat('kilikawoods1')
    saveGame(firstSave=False)
    while not battles5(completionVersion=99):
        quickResetLogic()
    #FFX_nem_arenaSelect.arenaMenuSelect(4)

def returnToSin():
    FFXC = FFX_Xbox.controllerHandle()
    while not FFX_targetPathNem.setMovement([-6,-27]):
        pass
    while not FFX_targetPathNem.setMovement([-2,-2]):
        pass
    returnToAirship()
    
    FFX_menu.equipWeapon(character=0, ability=0x8001, fullMenuClose=True)
    airShipDestination(destNum=0)
    FFX_memory.awaitControl()
    FFXC.set_movement(0,-1)
    FFX_memory.waitFrames(2)
    FFX_memory.awaitEvent()
    FFXC.set_neutral()