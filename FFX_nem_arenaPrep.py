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
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()

#The following functions extend the regular Bahamut run. Farming sections.

def autoLife():
    while not (FFX_memory.turnReady() and FFX_Screen.turnTidus()):
        if FFX_memory.turnReady():
            if FFX_Screen.turnAeon():
                FFX_Battle.attack('none')
            elif not FFX_Screen.turnTidus():
                FFX_Battle.defend()
    while FFX_memory.battleMenuCursor() != 22:
        if FFX_Screen.turnTidus() == False:
            print("Attempting Auto-life, but it's not Tidus's turn")
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

def airShipDestination(destNum=0, forceOmega=False): #Default to Besaid. Maybe based on map number?
    if gameVars.csr():
        if destNum >= 13: #Adjust for Besaid and Kilika locations
            if forceOmega:
                destNum += 4
            else:
                destNum += 5
        elif destNum >= 5: #Adjust for Mushroom Rock flight path
            destNum += 4
        elif destNum >= 2: #Adjust for Omega
            destNum += 3
    
    while not FFX_memory.getMap() in [382,999]:
        if FFX_memory.userControl():
            FFX_targetPathNem.setMovement([-251,340])
        else:
            FFXC.set_neutral()
        FFX_Xbox.menuB()
    while FFX_memory.diagProgressFlag() != 4:
        FFX_Xbox.tapB()
    print("Destination select on screen now.")
    while FFX_memory.mapCursor() != destNum:
        if destNum < 8:
            FFX_Xbox.tapDown()
        else:
            FFX_Xbox.tapUp()
    FFX_Xbox.tapB()
    FFX_memory.waitFrames(2)
    FFX_Xbox.tapB()
    while not FFX_memory.userControl():
        if FFX_memory.cutsceneSkipPossible():
            FFX_Xbox.skipScene()
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()

def unlockOmega():
    if gameVars.csr():
        return
        
    while not FFX_memory.getMap() in [382,999]:
        if FFX_memory.userControl():
            FFX_targetPathNem.setMovement([-251,340])
        else:
            FFXC.set_neutral()
        if FFX_memory.diagProgressFlag() == 4:
            FFX_Xbox.menuA()
        else:
            FFX_Xbox.menuB()
    while FFX_memory.diagProgressFlag() != 3:
        FFX_Xbox.tapUp()
    while FFX_memory.diagProgressFlag() != 0:
        FFX_Xbox.tapB()
    
    while FFX_memory.diagProgressFlag() == 0:
        print(FFX_memory.getCoords())
        if FFX_memory.getCoords()[0] < 65:
            FFXC.set_value("Dpad", 8)
        if FFX_memory.getCoords()[0] < 70:
            FFX_nem_menu.gridRight()
        elif FFX_memory.getCoords()[0] > 78:
            FFXC.set_value("Dpad", 4)
        elif FFX_memory.getCoords()[0] > 73:
            FFX_nem_menu.gridLeft()
        elif FFX_memory.getCoords()[1] > -28:
            FFXC.set_value("Dpad", 2)
        elif FFX_memory.getCoords()[1] > -34:
            FFX_nem_menu.gridDown()
        elif FFX_memory.getCoords()[1] < -40:
            FFXC.set_value("Dpad", 1)
        elif FFX_memory.getCoords()[1] < -37:
            FFX_nem_menu.gridUp()
        else:
            FFX_Xbox.menuB()
    FFX_memory.waitFrames(30)
    FFX_Xbox.menuB()
    while not FFX_memory.getMap() in [194,374]:
        FFX_Xbox.menuA()

def getSaveSphereDetails():
    mapVal = FFX_memory.getMap()
    storyVal = FFX_memory.getStoryProgress()
    print("Map and story: ", mapVal, " | ", storyVal)
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
                #print("Cursor test: ", FFX_memory.saveMenuCursor())
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

def battleFarmAll(apCpLimit:int=255, yunaAttack = True, faythCave=True):
    print("### Battle Start: ", FFX_memory.getBattleNum())
    FFXC.set_neutral()
    if faythCave==True and FFX_memory.battleType() == 2:
        FFX_Screen.awaitTurn()
        FFX_Battle.fleeAll()
    else:
        while FFX_memory.battleActive():
            if FFX_memory.turnReady():
                if FFX_Screen.turnTidus():
                    if FFX_memory.getBattleNum() in [154,156,164]:
                        #Confusion is a dumb mechanic in this game.
                        FFX_Battle.attackByNum(22,'l')
                    elif FFX_memory.getBattleNum() == 281:
                        FFX_Battle.attackByNum(22,'r')
                    elif FFX_memory.getBattleNum() == 283:
                        FFX_Battle.attackByNum(21,'u')
                    elif FFX_memory.getBattleNum() == 284:
                        FFX_Battle.attackByNum(23,'d')
                    else:
                        FFX_Battle.attack('none')
                elif FFX_Screen.turnYuna():
                    if yunaAttack:
                        if FFX_memory.getBattleNum() in [154,156,164]:
                            #Confusion is a dumb mechanic in this game.
                            FFX_Battle.attackByNum(22,'l')
                        elif FFX_memory.getBattleNum() == 281:
                            FFX_Battle.attackByNum(21,'l')
                        elif FFX_memory.getBattleNum() == 283:
                            FFX_Battle.attackByNum(22,'d')
                        elif FFX_memory.getBattleNum() == 284:
                            FFX_Battle.attackByNum(22,'d')
                        else:
                            FFX_Battle.attack('none')
                    else:
                        FFX_Battle.escapeOne()
                elif FFX_Screen.turnRikku() or FFX_Screen.turnWakka():
                    if not FFX_Battle.checkTidusOk():
                        FFX_Battle.escapeOne()
                    else:
                        FFX_Battle.defend()
                else:
                    FFX_Battle.escapeOne()
    FFX_memory.clickToControl()
    FFX_nem_menu.performNextGrid(limit=apCpLimit)
    if float(FFX_memory.getHP()[0]) / float(FFX_memory.getMaxHP()[0]) < 0.4:
        FFX_Battle.healUp(3)

def advancedCompleteCheck():
    battleNum = FFX_memory.getBattleNum()
    arenaArray = FFX_memory.arenaArray()
    #Common monsters
    if False:
        pass
    
    #Inside Sin
    elif battleNum == 374: #Ahriman
        print("For this battle, count: ", arenaArray[37])
        if arenaArray[37] == 10:
            return True
    elif battleNum in [375,380]: #Exoray (with a bonus Ahriman)
        print("For this battle, count: ", arenaArray[93])
        if arenaArray[93] == 10 and arenaArray[37] == 10:
            return True
    elif battleNum in [376,381]: #Adamantoise
        print("For this battle, count: ", arenaArray[81])
        if arenaArray[81] == 10:
            return True
    elif battleNum in [377,382]: #Both kinds of Gemini
        print("For this battle, count: ", arenaArray[77])
        print("For this battle, count: ", arenaArray[78])
        if arenaArray[77] == 10 and arenaArray[78] == 10:
            return True
    elif battleNum in [378,384]: #Behemoth King
        print("For this battle, count: ", arenaArray[70])
        if arenaArray[70] == 10:
            return True
    elif battleNum == 383: #Demonolith
        print("For this battle, count: ", arenaArray[75])
        if arenaArray[75] == 10:
            return True
    elif battleNum == 385: #Great Malboro
        print("For this battle, count: ", arenaArray[56])
        if arenaArray[56] == 10:
            return True
    elif battleNum == 386: #Barbatos
        print("For this battle, count: ", arenaArray[90])
        if arenaArray[90] == 10:
            return True
    elif battleNum == 387: #Wraith
        print("For this battle, count: ", arenaArray[97])
        if arenaArray[97] == 10:
            return True
        
    #Omega dungeon
    elif battleNum == 421: #Master Coeurl and Floating Death
        print("For this battle, count: ", arenaArray[74])
        print("For this battle, count: ", arenaArray[102])
        if arenaArray[74] == 10 and arenaArray[102] == 10:
            return True
    elif battleNum == 422: #Halma and Spirit
        print("For this battle, count: ", arenaArray[96])
        print("For this battle, count: ", arenaArray[101])
        if arenaArray[96] == 10 and arenaArray[101] == 10:
            return True
    elif battleNum == 423: #Zaurus and Floating Death
        print("For this battle, count: ", arenaArray[100])
        print("For this battle, count: ", arenaArray[102])
        if arenaArray[100] == 10 and arenaArray[102] == 10:
            return True
    elif battleNum == 424: #Black Element and Spirit
        print("For this battle, count: ", arenaArray[67])
        print("For this battle, count: ", arenaArray[96])
        if arenaArray[67] == 10 and arenaArray[96] == 10:
            return True
    elif battleNum == 425: #Varuna
        print("For this battle, count: ", arenaArray[82])
        if arenaArray[82] == 10:
            return True
    elif battleNum == 426: #Master Tonberry
        print("For this battle, count: ", arenaArray[99])
        if arenaArray[99] == 10:
            return True
    elif battleNum == 428: #Machea (blade thing)
        print("For this battle, count: ", arenaArray[103])
        if arenaArray[103] == 10:
            return True
    elif battleNum == 430: #Demonolith x2
        print("For this battle, count: ", arenaArray[75])
        if arenaArray[75] == 10:
            return True
    elif battleNum in [432,433,434,435,436]: #Just Zaurus
        print("For this battle, count: ", arenaArray[100])
        if arenaArray[100] == 10:
            return True
    elif battleNum == 437: #Puroboros
        print("For this battle, count: ", arenaArray[95])
        if arenaArray[95] == 10:
            return True
    elif battleNum == 438: #Wraith
        print("For this battle, count: ", arenaArray[97])
        if arenaArray[97] == 10:
            return True
    
    
    #Other
    if battleNum in [429,445]:
        #Rock monsters, just leave.
        return True
    if battleNum == 383:
        #Demonolith inside Sin, not worth.
        return True
    if battleNum == 427:
        #Adamantoise in Omega, dealt with inside Sin
        return True
    
    return False

def advancedBattleLogic():
    print("### Battle Start: ", FFX_memory.getBattleNum())
    print("### Ambush flag (2 is bad): ", FFX_memory.battleType())
    autoLifeUsed = False
    FFXC.set_neutral()
    
    if FFX_memory.battleType() == 2:
        print(">>>>Ambushed! Escaping!")
        FFX_Battle.tidusFlee()
    elif advancedCompleteCheck():
        print(">>>>Complete collecting this monster.")
        FFX_Battle.tidusFlee()
    else:
        if FFX_memory.getBattleNum() == 449:
            #Omega himself, not yet working.
            aeonComplete = False
            while FFX_memory.battleActive():
                if FFX_memory.turnReady():
                    if FFX_Screen.turnRikku():
                        if not aeonComplete:
                            FFX_Battle.buddySwapYuna()
                            FFX_Battle.aeonSummon(4)
                        else:
                            FFX_Battle.defend()
                    elif FFX_Screen.turnYuna():
                        FFX_Battle.buddySwapRikku()
                    elif FFX_Screen.turnTidus():
                        FFX_Battle.useSkill(1) #Quick hit
                    else:
                        FFX_Battle.defend()
        else:
            print("---Regular battle:", FFX_memory.getBattleNum())
            sleepPowder = False
            while FFX_memory.battleActive():
                battleNum = FFX_memory.getBattleNum()
                if FFX_memory.turnReady():
                    if battleNum in [442]:
                        #Damned malboros in Omega
                        FFX_Battle.buddySwapYuna()
                        FFX_Battle.aeonSummon(4)
                        FFX_Battle.attack('none')
                    elif FFX_Screen.turnTidus():
                        if FFX_memory.getBattleNum() in [386] and not autoLifeUsed:
                            autoLife()
                            autoLifeUsed = True
                        elif battleNum == 383 and FFX_memory.getEnemyCurrentHP()[0] > 9999:
                            if FFX_memory.getUseItemsSlot(41) < 100:
                                FFX_Battle.useItemTidus(FFX_memory.getUseItemsSlot(41))
                            else:
                                FFX_Battle.useSkill(1)
                        elif battleNum == 426 and FFX_memory.getEnemyCurrentHP()[0] > 9999:
                            if FFX_memory.getUseItemsSlot(41) < 100:
                                FFX_Battle.useItemTidus(FFX_memory.getUseItemsSlot(41))
                            else:
                                FFX_Battle.useSkill(1)
                        elif battleNum == 430 and FFX_memory.getEnemyCurrentHP()[0] > 9999:
                            if FFX_memory.getUseItemsSlot(41) < 100:
                                FFX_Battle.useItemTidus(FFX_memory.getUseItemsSlot(41))
                            else:
                                FFX_Battle.useSkill(1)
                        elif battleNum == 437 and FFX_memory.getEnemyCurrentHP()[0] > 9999:
                            if FFX_memory.getUseItemsSlot(41) < 100:
                                FFX_Battle.useItemTidus(FFX_memory.getUseItemsSlot(41))
                            else:
                                FFX_Battle.useSkill(1)
                        elif battleNum == 431:
                            FFX_Battle.tidusFlee()
                        else:
                            FFX_Battle.useSkill(1) #Quick hit
                    elif FFX_Screen.turnRikku():
                        if battleNum in [377,382]:
                            print("Shining Gems for Gemini, better to save other items for other enemies.")
                            #Double Gemini, two different locations
                            if FFX_memory.getUseItemsSlot(42) < 100:
                                FFX_Battle.useItem(FFX_memory.getUseItemsSlot(42), rikkuFlee=True)
                            else:
                                FFX_Battle.defend()
                        elif battleNum == 386:
                            #Armor bomber guys
                            if FFX_memory.getUseItemsSlot(41) < 100:
                                FFX_Battle.useItem(FFX_memory.getUseItemsSlot(41), rikkuFlee=True)
                            else:
                                FFX_Battle.defend()
                        elif battleNum in [383,430]:
                            #Demonolith
                            if FFX_memory.getUseItemsSlot(41) < 100:
                                FFX_Battle.useItem(FFX_memory.getUseItemsSlot(41), rikkuFlee=True)
                            else:
                                FFX_Battle.defend()
                        elif battleNum == 422:
                            #Provoke on Spirit
                            FFX_Battle.useSpecial(position=3, target=21, direction='u')
                            if FFX_memory.getUseItemsSlot(41) < 100:
                                FFX_Battle.useItem(FFX_memory.getUseItemsSlot(41), rikkuFlee=True)
                            else:
                                FFX_Battle.defend()
                        elif battleNum == 424:
                            #Provoke on Spirit
                            FFX_Battle.useSpecial(position=3, target=21, direction='r')
                        elif battleNum == 425 and FFX_memory.getEnemyCurrentHP()[0] > 9999:
                            #Varuna, use purifying salt to remove haste
                            FFX_Battle.useItem(FFX_memory.getUseItemsSlot(63), rikkuFlee=True) #Safety potions are fun.
                        elif battleNum == 426:
                            #Master Tonberry
                            if not sleepPowder:
                                FFX_Battle.useItem(FFX_memory.getUseItemsSlot(37), rikkuFlee=True)
                            else:
                                if FFX_memory.getUseItemsSlot(41) < 100:
                                    FFX_Battle.useItemTidus(FFX_memory.getUseItemsSlot(41))
                                else:
                                    FFX_Battle.defend()
                        elif battleNum == 431:
                            FFX_Battle.tidusFlee()
                        elif battleNum == 437 and FFX_memory.getEnemyCurrentHP()[0] > 9999:
                            if not sleepPowder:
                                FFX_Battle.useItem(FFX_memory.getUseItemsSlot(37), rikkuFlee=True)
                            else:
                                if FFX_memory.getUseItemsSlot(41) < 100:
                                    FFX_Battle.useItemTidus(FFX_memory.getUseItemsSlot(41))
                                else:
                                    FFX_Battle.defend()
                        else:
                            FFX_Battle.defend()
                    else:
                        FFX_Battle.defend()
    FFX_memory.clickToControl()
    FFX_memory.fullPartyFormat('initiative')
    FFX_nem_menu.performNextGrid()
    if float(FFX_memory.getHP()[0]) / float(FFX_memory.getMaxHP()[0]) < 0.3:
        FFX_Battle.healUp(3)

def bribeBattle(spareChangeValue:int=12000):
    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            if FFX_Screen.turnLulu():
                while FFX_memory.battleMenuCursor() != 20:
                    if FFX_memory.battleMenuCursor() == 0:
                        FFX_Xbox.tapDown()
                    else:
                        FFX_Xbox.tapUp()
                    if gameVars.usePause():
                        FFX_memory.waitFrames(6)
                FFX_memory.waitFrames(8)
                FFX_Xbox.tapB()
                FFX_memory.waitFrames(8)
                FFX_Xbox.tapB()
                FFX_memory.waitFrames(8)
                FFX_Battle.calculateSpareChangeMovement(spareChangeValue)
                while FFX_memory.spareChangeOpen():
                    FFX_Xbox.tapB()
                FFX_Xbox.tapB()
                FFX_Xbox.tapB()
            else:
                FFX_Battle.buddySwapLulu()
    print("Battle is complete.")
    while not FFX_memory.menuOpen():
        pass
    FFXC.set_value("BtnB", 1)
    FFX_memory.waitFrames(150)
    FFXC.set_value("BtnB", 0)
    print("Now back in control.")

def arenaNPC():
    FFX_memory.awaitControl()
    if FFX_memory.getMap() != 307:
        return
    while not (FFX_memory.diagProgressFlag() == 74 and FFX_memory.diagSkipPossible()):
        if FFX_memory.userControl():
            if FFX_memory.getCoords()[1] > -12:
                FFXC.set_movement(0,-1)
                FFX_memory.waitFrames(1)
            else:
                FFX_targetPathNem.setMovement([2,-15])
                FFX_Xbox.tapB()
        else:
            FFXC.set_neutral()
            if FFX_memory.diagProgressFlag() == 59:
                FFX_Xbox.menuA()
                FFX_Xbox.menuA()
                FFX_Xbox.menuA()
                FFX_Xbox.tapB()
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    print("Mark 1")
    FFX_memory.waitFrames(30) #This buffer can be improved later.
    print("Mark 2")

def arenaReturn():
    airShipDestination(destNum=12)
    #FFX_menu.equipArmor(character=gameVars.neArmor(),ability=0x801D)
    
    checkpoint = 0
    while FFX_memory.getMap() != 307:
        if FFX_memory.userControl():
            if checkpoint == 2:
                while FFX_memory.userControl():
                    FFX_targetPathNem.setMovement([-641,-268])
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                checkpoint += 1
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.arenaReturn(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

def transition():
    FFX_memory.clickToControl()
    returnToAirship()
    FFX_memory.awaitControl()
    FFX_menu.addAbility(owner=0, equipment_type=0, ability_array=[0x807A,255,255,255], ability_index=0x8001, slotcount=2, navigateToEquipMenu=True, fullMenuClose=True)

def kilikaShop():
    arenaNPC()
    FFX_Xbox.tapA()
    FFX_Xbox.tapB()
    FFX_memory.waitFrames(60)
    arenaNPC()
    FFX_Xbox.tapA()
    FFX_Xbox.tapB()
    arenaNPC()
    #FFX_Xbox.tapDown()
    #FFX_Xbox.tapDown()
    #FFX_Xbox.tapB()
    #FFX_memory.waitFrames(30)
    #FFX_Xbox.tapB() #Buy
    #FFX_memory.waitFrames(30)
    #getEquipment(equip=False) #Tidus second catcher weapon
    #FFX_Xbox.menuA()
    #FFX_memory.waitFrames(30)
    #FFX_Xbox.menuA()
    #FFX_memory.waitFrames(30)
    FFX_Xbox.menuA()
    FFX_Xbox.tapB() #Exit
    FFX_memory.waitFrames(60)
    while not FFX_targetPathNem.setMovement([-6,-23]):
        pass
    while not FFX_targetPathNem.setMovement([0,-3]):
        pass
    returnToAirship()
    FFX_memory.awaitControl()
    #FFX_menu.equipWeapon(character=0,ability=0x807A, fullMenuClose=False)
    airShipDestination(destNum=2)
    while not FFX_targetPathNem.setMovement([-25,-246]):
        pass
    while not FFX_targetPathNem.setMovement([-47,-209]):
        pass
    while not FFX_targetPathNem.setMovement([-91,-199]):
        pass
    while not FFX_targetPathNem.setMovement([-108,-169]):
        pass
    while FFX_memory.userControl():
        FFXC.set_movement(-1,0)
        FFX_Xbox.tapB()
    FFXC.set_neutral() #Now talking to vendor
    FFX_memory.waitFrames(60)
    FFX_Xbox.tapB() #Intro dialog
    FFX_memory.waitFrames(60)
    FFX_Xbox.tapB() #Buy equipment
    FFX_memory.waitFrames(60)
    #getEquipment(equip=False) #Weapon for Yuna
    FFX_Xbox.tapDown()
    FFX_Xbox.tapDown()
    FFX_Xbox.tapDown()
    FFX_Xbox.tapDown()
    FFX_Xbox.tapDown()
    FFX_Xbox.tapDown()
    getEquipment(equip=True) #Weapon for Rikku
    FFX_Xbox.tapDown()
    getEquipment(equip=True) #Armor for Tidus
    FFX_Xbox.tapDown()
    getEquipment(equip=True) #Armor for Yuna
    FFX_Xbox.tapDown()
    getEquipment(equip=True) #Armor for Wakka
    FFX_Xbox.tapDown()
    FFX_Xbox.tapDown()
    FFX_Xbox.tapDown()
    getEquipment(equip=True) #Armor for Wakka
    FFX_Xbox.tapDown()
    getEquipment(equip=True) #Armor for Rikku
    FFX_memory.closeMenu()
    FFX_menu.addAbility(owner=6, equipment_type=0, ability_array=[0x800B,0x8000,255,255], ability_index=0x8001, slotcount=4, navigateToEquipMenu=True, fullMenuClose=True)
    FFX_menu.addAbility(owner=0, equipment_type=1, ability_array=[0x8072,255,255,255], ability_index=0x8056, slotcount=4, navigateToEquipMenu=True, fullMenuClose=True)
    
    while not FFX_targetPathNem.setMovement([-91,-199]):
        pass
    while not FFX_targetPathNem.setMovement([-47,-209]):
        pass
    while not FFX_targetPathNem.setMovement([-25,-246]):
        pass
    while not FFX_targetPathNem.setMovement([29,-252]):
        pass
    returnToAirship()

def apToXP(): #Calm Lands purchases
    arenaReturn()
    arenaNPC()
    FFX_Xbox.tapA()
    FFX_Xbox.tapB()
    arenaNPC()
    FFX_Xbox.tapA()
    FFX_Xbox.tapB()
    arenaNPC()
    FFX_Xbox.tapA()
    FFX_Xbox.tapB()
    arenaNPC()
    FFX_Xbox.tapA()
    FFX_Xbox.tapB()
    arenaNPC()
    FFX_Xbox.tapDown()
    FFX_Xbox.tapDown()
    FFX_Xbox.tapB()
    FFX_memory.waitFrames(60)
    FFX_Xbox.tapB()
    FFX_memory.waitFrames(6)
    FFX_Xbox.tapB()
    FFX_memory.waitFrames(6)
    FFX_Xbox.tapUp()
    FFX_Xbox.tapB()
    FFX_memory.waitFrames(6)
    FFX_Xbox.tapUp()
    FFX_Xbox.tapB()
    print("Now to sell items.")
    FFX_memory.waitFrames(6)
    FFX_Xbox.menuA()
    FFX_memory.waitFrames(6)
    FFX_Xbox.tapRight()
    FFX_Xbox.menuB()
    print("Should now be attempting to sell items.")
    FFX_menu.sellAll()
    FFX_Xbox.menuA()
    FFX_memory.waitFrames(60)
    FFX_Xbox.tapA()
    FFX_memory.waitFrames(60)
    FFX_Xbox.tapA()
    FFX_memory.waitFrames(60)
    FFX_Xbox.tapA()
    FFX_Xbox.tapB()
    FFX_menu.autoSortEquipment(manual='n')
    FFX_menu.addAbility(owner=0, equipment_type=0, ability_array=[0x807A,255,255,255], ability_index=0x8011, slotcount=2, navigateToEquipMenu=True, exitOutOfCurrentWeapon=True, closeMenu=True, fullMenuClose=False)
    FFX_menu.equipWeapon(character=0, ability=0x8011)
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_menu.tidusSlayer()
    
    FFX_memory.awaitControl()
    FFXC.set_movement(-1,0)
    FFX_memory.waitFrames(30)
    returnToAirship()

def farmFeathers():
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=7,monsterIndex=5)
    FFX_memory.waitFrames(1)
    waitCounter = 0
    while FFX_memory.battleActive():
        if FFX_memory.turnReady():
            if FFX_Screen.turnRikku():
                print("+++ Qactar steal command")
                FFX_Battle.Steal()
                print("+++ Qactar steal command done")
            elif FFX_Screen.turnTidus():
                print("+++ Qactar flee command")
                FFX_Battle.tidusFlee()
                print("+++ Qactar flee command done")
            else:
                print("+++ Qactar defend command")
                FFX_Battle.defend()
                print("+++ Qactar defend command done")
        waitCounter += 1
        if waitCounter % 10 == 0:
            print("Waiting for next turn: ", waitCounter)
    print("Battle is complete.")
    
    while not FFX_memory.menuOpen():
        pass
    #FFX_memory.waitFrames(300)
    
    FFXC.set_value("BtnB", 1)
    FFX_memory.waitFrames(150)
    FFXC.set_value("BtnB", 0)
    print("Now back in control.")
    FFX_nem_arenaSelect.arenaMenuSelect(4)

def autoPhoenix(): #Calm Lands items
    FFX_menu.autoSortEquipment()
    FFX_nem_menu.luluBribe()
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=7,monsterIndex=0)
    bribeBattle()
    FFX_nem_arenaSelect.arenaMenuSelect(4)
    FFX_memory.fullPartyFormat('initiative')
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=7,monsterIndex=0)
    bribeBattle()
    FFX_nem_arenaSelect.arenaMenuSelect(4)
    FFX_memory.fullPartyFormat('initiative')
    arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(1)
    FFX_nem_arenaSelect.startFight(areaIndex=7,monsterIndex=0)
    bribeBattle()
    FFX_nem_arenaSelect.arenaMenuSelect(4)
    FFX_memory.fullPartyFormat('initiative')
    arenaNPC()
    while FFX_memory.getItemCountSlot(FFX_memory.getItemSlot(7)) != 99:
        print("Trying to obtain mega-phoenix downs")
        FFX_nem_arenaSelect.arenaMenuSelect(4)
        arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(2) #Equipment menu
    FFX_memory.waitFrames(90)
    FFX_Xbox.tapRight()
    FFX_Xbox.menuB() #Sell
    FFX_menu.sellAll()
    FFX_memory.waitFrames(3)
    FFX_Xbox.tapA()
    FFX_memory.waitFrames(90)
    FFX_Xbox.tapA()
    FFX_memory.waitFrames(90)
    FFX_Xbox.tapA()
    FFX_Xbox.tapB()
    FFX_menu.autoSortEquipment() #This to make sure equipment is in the right place
    FFX_menu.addAbility(owner=4, equipment_type=1, ability_array=[0x8072,255,255,255], ability_index=0x800A, slotcount=4, navigateToEquipMenu=True, exitOutOfCurrentWeapon=True, closeMenu=True, fullMenuClose=False)
    
    FFX_memory.waitFrames(30)
    initArray = FFX_memory.checkAbility(ability = 0x8002)
    print("Initiative weapons: ", initArray)
    if initArray[4]:
        FFX_menu.addAbility(owner=6, equipment_type=1, ability_array=[0x8072,255,255,255], ability_index=0x800A, slotcount=4, navigateToEquipMenu=True, exitOutOfCurrentWeapon=True, closeMenu=True, fullMenuClose=False)
        FFX_menu.equipWeapon(character=4,ability=0x8002) #Initiative
        FFX_memory.closeMenu()
    else:
        FFX_menu.addAbility(owner=6, equipment_type=1, ability_array=[0x8072,255,255,255], ability_index=0x800A, slotcount=4, navigateToEquipMenu=True, exitOutOfCurrentWeapon=True, closeMenu=True, fullMenuClose=True)
        FFX_memory.closeMenu()
        featherSlot = FFX_memory.getItemSlot(itemNum=54)
        if featherSlot == 255 or FFX_memory.getItemCountSlot(featherSlot) < 6:
            while featherSlot == 255 or FFX_memory.getItemCountSlot(featherSlot) < 6:
                farmFeathers()
                featherSlot = FFX_memory.getItemSlot(itemNum=54)
        FFX_menu.addAbility(owner=6, equipment_type=0, ability_array=[0x800B,0x8000,0x8001,255], ability_index=0x8002, slotcount=4, navigateToEquipMenu=True, exitOutOfCurrentWeapon=True, closeMenu=True, fullMenuClose=True)
        
    
    FFXC.set_movement(-1,0)
    FFX_memory.waitFrames(15)
    FFXC.set_movement(0,1)
    FFX_memory.waitFrames(15)
    FFXC.set_neutral()
    FFX_memory.fullPartyFormat('initiative')
    returnToAirship()
    
    #FFX_menu.equipArmor(character=0,ability=0x8056) #Auto-Haste
    FFX_menu.equipArmor(character=4,ability=0x800A) #Auto-Phoenix
    FFX_menu.equipArmor(character=6,ability=0x800A) #Auto-Phoenix
    if not gameVars.neArmor() in [0,4,6]:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=99) #Unequip
    FFX_memory.closeMenu()

def restockDowns():
    print("Restocking phoenix downs")
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

def oneMpReady():
    print("Slot, Gambler:", FFX_memory.getItemSlot(41))
    if FFX_memory.getItemSlot(41) > 200:
        return False
    print("Count, Gambler:", FFX_memory.getItemCountSlot(FFX_memory.getItemSlot(41)))
    if FFX_memory.getItemCountSlot(FFX_memory.getItemSlot(41)) < 99:
        return False
    print("Slot, Salt:", FFX_memory.getItemSlot(63))
    if FFX_memory.getItemSlot(63) > 200:
        return False
    print("Count, Salt:", FFX_memory.getItemCountSlot(FFX_memory.getItemSlot(63)))
    if FFX_memory.getItemCountSlot(FFX_memory.getItemSlot(63)) < 20:
        return False
    return True

def oneMpWeapon(): #Break Damage Limit, or One MP cost
    FFX_menu.autoSortEquipment()
    FFX_memory.fullPartyFormat('initiative')
    arenaNPC()
    print("###Sleeping powder count:", FFX_memory.getItemCountSlot(FFX_memory.getItemSlot(37)))
    while FFX_memory.getItemSlot(37) > 200 or FFX_memory.getItemCountSlot(FFX_memory.getItemSlot(37)) < 41:
        FFX_nem_arenaSelect.arenaMenuSelect(1)
        FFX_nem_arenaSelect.startFight(areaIndex=7,monsterIndex=0)
        bribeBattle()
        FFX_nem_arenaSelect.arenaMenuSelect(4)
        FFX_memory.fullPartyFormat('initiative')
        arenaNPC()
        print("###Sleeping powder count:", FFX_memory.getItemCountSlot(FFX_memory.getItemSlot(37)))
    while not oneMpReady():
        print("Trying to obtain Gambler's Soul and Purifying Salt items")
        FFX_nem_arenaSelect.arenaMenuSelect(4)
        arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(2)
    FFX_memory.waitFrames(60)
    FFX_Xbox.menuB() #Buy
    FFX_memory.waitFrames(10)
    FFX_Xbox.menuB() #New Tidus capture weapon
    FFX_memory.waitFrames(10)
    FFX_Xbox.tapUp()
    FFX_Xbox.menuB() #Confirm purchase
    FFX_memory.waitFrames(10)
    FFX_Xbox.tapUp()
    FFX_Xbox.menuB() #Confirm equipping weapon
    
    FFX_memory.waitFrames(3)
    FFX_Xbox.tapA()
    FFX_memory.waitFrames(30)
    FFX_Xbox.tapA()
    FFX_memory.waitFrames(30)
    FFX_Xbox.tapA()
    FFX_Xbox.tapB()
    FFX_menu.autoSortEquipment() #This to make sure equipment is in the right place
    FFX_memory.closeMenu()
    FFX_menu.addAbility(owner=0, equipment_type=0, ability_array=[0x807A,255,255,255], ability_index=0x800D, slotcount=2, navigateToEquipMenu=True, exitOutOfCurrentWeapon=True, closeMenu=True, fullMenuClose=True)
    restockDowns()
    FFX_nem_arenaSelect.arenaMenuSelect(4)
    
    FFXC.set_movement(-1,0)
    FFX_memory.waitFrames(15)
    FFXC.set_movement(0,1)
    FFX_memory.waitFrames(15)
    FFXC.set_neutral()
    returnToAirship()
    FFX_nem_menu.rikkuHaste()
    rinEquipDump()

def kilikaFinalShop():
    FFX_memory.awaitControl()
    rinEquipDump()
    FFX_menu.autoSortEquipment()
    
    gilNeeded = 3500000 - FFX_memory.getGilvalue()
    weaponBuys = int(gilNeeded / 26150)
    weaponBuys += 1 # for safety
    
    
    airShipDestination(destNum=2)
    while not FFX_targetPathNem.setMovement([-25,-246]):
        pass
    while not FFX_targetPathNem.setMovement([-47,-209]):
        pass
    while not FFX_targetPathNem.setMovement([-91,-199]):
        pass
    while not FFX_targetPathNem.setMovement([-108,-169]):
        pass
    while FFX_memory.userControl():
        FFXC.set_movement(-1,0)
        FFX_Xbox.tapB()
    FFXC.set_neutral() #Now talking to vendor
    FFX_memory.waitFrames(60)
    FFX_Xbox.tapB() #Intro dialog
    FFX_memory.waitFrames(60)
    FFX_Xbox.tapB() #Buy equipment
    FFX_memory.waitFrames(60)
    getEquipment(equip=True) #Weapon for Tidus
    FFX_memory.waitFrames(60)
    FFX_Xbox.tapDown()
    FFX_Xbox.tapDown()
    FFX_Xbox.tapDown()
    FFX_Xbox.tapDown()
    FFX_Xbox.tapDown()
    FFX_Xbox.tapDown()
    FFX_Xbox.tapDown()
    for x in range(weaponBuys):
        print("Buying armors, remaining - ", weaponBuys - x)
        FFX_memory.waitFrames(6)
        FFX_Xbox.menuB() #Purchase
        FFX_memory.waitFrames(6)
        FFX_Xbox.menuUp()
        FFX_Xbox.menuB() #Confirm
        FFX_memory.waitFrames(6)
        FFX_Xbox.menuB() #Do not equip
    FFX_memory.waitFrames(6)
    FFX_memory.closeMenu()
    
    for y in range(weaponBuys):
        if y == 0: #First one
            FFX_menu.addAbility(owner=0, equipment_type=1, ability_array=[0x8072,255,255,255], ability_index=0x8075, slotcount=4, navigateToEquipMenu=True, exitOutOfCurrentWeapon=True, closeMenu=False, fullMenuClose=False)
        elif weaponBuys - y == 1: #Last one
            FFX_menu.addAbility(owner=0, equipment_type=1, ability_array=[0x8072,255,255,255], ability_index=0x8075, slotcount=4, navigateToEquipMenu=True, exitOutOfCurrentWeapon=True, closeMenu=True, fullMenuClose=True)
        else:
            FFX_menu.addAbility(owner=0, equipment_type=1, ability_array=[0x8072,255,255,255], ability_index=0x8075, slotcount=4, navigateToEquipMenu=False, exitOutOfCurrentWeapon=True, closeMenu=False, fullMenuClose=False)
    
    while FFX_memory.userControl():
        FFXC.set_movement(-1,0)
        FFX_Xbox.tapB()
    FFXC.set_neutral() #Now talking to vendor
    FFX_memory.waitFrames(60)
    FFX_Xbox.tapB() #Intro dialog
    FFX_memory.waitFrames(60)
    FFX_Xbox.tapRight()
    FFX_Xbox.tapB() #Sell equipment
    FFX_menu.sellAll()
    FFX_memory.closeMenu()
    
    while not FFX_targetPathNem.setMovement([-91,-199]):
        pass
    while not FFX_targetPathNem.setMovement([-47,-209]):
        pass
    while not FFX_targetPathNem.setMovement([-25,-246]):
        pass
    while not FFX_targetPathNem.setMovement([29,-252]):
        pass
    FFX_menu.autoSortEquipment()
    returnToAirship()

def finalWeapon():
    arenaNPC()
    while FFX_memory.getItemCountSlot(FFX_memory.getItemSlot(53)) < 99:
        print("Trying to obtain Dark Matter for BDL weapon")
        FFX_nem_arenaSelect.arenaMenuSelect(4)
        arenaNPC()
    FFX_nem_arenaSelect.arenaMenuSelect(4)
    
    FFX_menu.addAbility(owner=0, equipment_type=0, ability_array=[0x800B,0x8000,255,255], ability_index=0x800D, slotcount=4, navigateToEquipMenu=True, exitOutOfCurrentWeapon=False, closeMenu=False, fullMenuClose=False)
    FFX_menu.addAbility(owner=0, equipment_type=0, ability_array=[0x800B,0x8000,0x800D,255], ability_index=0x8019, slotcount=4, navigateToEquipMenu=False, exitOutOfCurrentWeapon=True, closeMenu=False, fullMenuClose=False)
    #FFX_menu.addAbility(owner=0, equipment_type=0, ability_array=[0x8064,255,255,255], ability_index=29, slotcount=4, navigateToEquipMenu=True, exitOutOfCurrentWeapon=False, closeMenu=False, fullMenuClose=False)
    #FFX_menu.addAbility(owner=0, equipment_type=0, ability_array=[0x8064,0x800D,255,255], ability_index=33, slotcount=4, navigateToEquipMenu=True, exitOutOfCurrentWeapon=False, closeMenu=False, fullMenuClose=False)
    #FFX_menu.addAbility(owner=0, equipment_type=0, ability_array=[0x8064,0x800D,0x800F,255], ability_index=35, slotcount=4, navigateToEquipMenu=False, exitOutOfCurrentWeapon=True, closeMenu=True, fullMenuClose=True)
    
    FFX_menu.addAbility(owner=1, equipment_type=1, ability_array=[0x8072,255,255,255], ability_index=0x800A, slotcount=4, navigateToEquipMenu=False, exitOutOfCurrentWeapon=True, closeMenu=True, fullMenuClose=True)
    FFX_menu.addAbility(owner=1, equipment_type=1, ability_array=[0x8072,0x800A,255,255], ability_index=0x801D, slotcount=4, navigateToEquipMenu=True, exitOutOfCurrentWeapon=True, closeMenu=True, fullMenuClose=True)
    FFX_memory.fullPartyFormat('kilikawoods1')

def rinEquipDump(buyWeapon=False):
    while not FFX_targetPathNem.setMovement([-242,298]):
        pass
    while not FFX_targetPathNem.setMovement([-241,211]):
        pass
    FFXC.set_movement(0,-1)
    while FFX_memory.userControl():
        pass
    while not FFX_targetPathNem.setMovement([39,53]):
        pass
    while FFX_memory.userControl():
        FFX_targetPathNem.setMovement([28,44])
        FFX_Xbox.tapB()
    FFXC.set_neutral()
    FFX_memory.clickToDiagProgress(48)
    FFX_memory.waitFrames(10)
    FFX_Xbox.tapB()
    FFX_memory.waitFrames(30)
    FFX_Xbox.tapRight()
    FFX_Xbox.menuB()
    
    FFX_menu.sellAll()
    if buyWeapon:
        FFX_memory.waitFrames(60)
        FFX_Xbox.menuRight() #Removes any pop-ups
        FFX_memory.waitFrames(60)
        FFX_Xbox.menuA()
        FFX_memory.waitFrames(60)
        FFX_Xbox.menuLeft()
        FFX_memory.waitFrames(60)
        FFX_Xbox.menuB()
        FFX_memory.waitFrames(60)
        FFX_Xbox.menuB()
        FFX_memory.waitFrames(60)
        FFX_Xbox.menuUp()
        FFX_memory.waitFrames(60)
        FFX_Xbox.menuB()
        FFX_memory.waitFrames(60)
        FFX_Xbox.menuUp()
        FFX_memory.waitFrames(60)
        FFX_Xbox.menuB()
        FFX_memory.waitFrames(60)
    FFX_memory.closeMenu()
    FFX_memory.clickToControl3()
    while not FFX_targetPathNem.setMovement([53,110]):
        pass
    FFXC.set_movement(-1,-1)
    while FFX_memory.userControl():
        pass
    while not FFX_targetPathNem.setMovement([-241,223]):
        pass
    while not FFX_targetPathNem.setMovement([-246,329]):
        pass

def yojimboDialog():
    print("Clicking until dialog box")
    while FFX_memory.diagProgressFlag():
        FFX_Xbox.tapB()
    print("Dialog box online.")
    FFX_memory.waitFrames(60)
    FFX_Xbox.tapUp()
    FFX_Xbox.tapB()
    FFX_memory.clickToDiagProgress(5)
    FFX_memory.waitFrames(12)
    FFX_Xbox.tapLeft()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapLeft()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapUp()
    FFX_Xbox.tapB()
    FFX_memory.waitFrames(12) #Eff it, just pay the man!
    #FFX_memory.clickToDiagProgress(5) #150,001
    #FFX_memory.waitFrames(12)
    #FFX_Xbox.tapDown()
    #FFX_Xbox.tapDown()
    #FFX_Xbox.tapLeft()
    #FFX_Xbox.tapDown()
    #FFX_Xbox.tapDown()
    #FFX_Xbox.tapB()
    #FFX_memory.waitFrames(12)
    #FFX_memory.clickToDiagProgress(5) #138,001
    #FFX_memory.waitFrames(12)
    #FFX_Xbox.tapUp()
    #FFX_Xbox.tapUp()
    #FFX_Xbox.tapLeft()
    #FFX_Xbox.tapUp()
    #FFX_Xbox.tapUp()
    #FFX_Xbox.tapUp()
    #FFX_Xbox.tapUp()
    #FFX_Xbox.tapB()
    #FFX_memory.waitFrames(12)
    #FFX_memory.clickToDiagProgress(5) #170,001
    #FFX_memory.waitFrames(12)
    #FFX_Xbox.tapLeft()
    #FFX_Xbox.tapUp()
    #FFX_Xbox.tapUp()
    #FFX_Xbox.tapB()
    print("Fayth accepts the contract.")
    FFX_Xbox.nameAeon("Yojimbo")
    print("Naming complete.")

def yojimbo():
    checkpoint = 0
    while not FFX_memory.getMap() in [194,374]:
        if FFX_memory.userControl():
            if checkpoint == 5:
                FFX_memory.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 9:
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 29 and FFX_memory.getCoords()[1] > 1800:
                checkpoint += 1
            elif checkpoint in [32,35]:
                FFXC.set_neutral()
                FFX_memory.waitFrames(12)
                if checkpoint == 32:
                    FFXC.set_movement(0,1)
                else:
                    FFXC.set_movement(0,-1)
                FFX_memory.waitFrames(2)
                FFXC.set_neutral()
                FFX_memory.waitFrames(12)
                FFX_Xbox.tapB()
                checkpoint += 1
            elif checkpoint == 33: #Talking to Fayth
                yojimboDialog()
                checkpoint += 1
            elif checkpoint == 39:
                FFX_memory.clickToEventTemple(3)
                checkpoint += 1
            elif checkpoint == 41:
                returnToAirship()
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.yojimbo(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                FFX_Battle.yojimbo()
                FFX_memory.clickToControl()
            elif checkpoint == 33: #Talking to Fayth
                yojimboDialog()
                checkpoint += 1
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

def besaidFarm(capNum:int=1):
    airShipDestination(destNum=1)
    
    if gameVars.neArmor() == 0:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=0x8056) #Auto-Haste
    else:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=99) #Unequip
    FFX_memory.arenaFarmCheck(zone="besaid",endGoal=capNum,report=True)
    checkpoint = 0
    while not FFX_memory.getMap() in [194,374]:
        if FFX_memory.userControl():
            if FFX_memory.arenaFarmCheck(zone="besaid",endGoal=capNum,report=False) and checkpoint < 15:
                checkpoint = 15
            elif checkpoint == 15 and not FFX_memory.arenaFarmCheck(zone="besaid",endGoal=capNum,report=False):
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
                if capNum == 10:
                    battleFarmAll(yunaAttack = False)
                else:
                    battleFarmAll()
                FFX_memory.arenaFarmCheck(zone="besaid",endGoal=capNum,report=True)
            elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

def kilikaFarm(capNum:int=1):
    airShipDestination(destNum=2)
    if gameVars.neArmor() == 0:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=0x8056) #Auto-Haste
    else:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=99) #Unequip
    
    checkpoint = 0
    while not FFX_memory.getMap() in [194,374]:
        if FFX_memory.userControl():
            if FFX_memory.arenaFarmCheck(zone="kilika",endGoal=capNum,report=False) and checkpoint < 14:
                checkpoint = 14
            elif checkpoint == 14 and not FFX_memory.arenaFarmCheck(zone="kilika",endGoal=capNum,report=False):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)
                
            elif checkpoint == 4:
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 11:
                FFX_memory.clickToEventTemple(0)
                FFX_memory.arenaFarmCheck(zone="kilika",endGoal=10,report=True)
                checkpoint += 1
            elif checkpoint == 14 and FFX_memory.getMap() == 47:
                checkpoint += 1
            elif checkpoint == 21:
                FFX_memory.clickToEventTemple(3)
                checkpoint += 1
            elif checkpoint == 25:
                returnToAirship()
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.kilikaFarm(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                if capNum == 10:
                    battleFarmAll(yunaAttack = False)
                else:
                    battleFarmAll()
                FFX_memory.arenaFarmCheck(zone="kilika",endGoal=capNum,report=True)
            elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
   
def miihenFarm(capNum:int=1):
    airShipDestination(destNum=4)
    if gameVars.neArmor() == 0:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=0x8056) #Auto-Haste
    else:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=99) #Unequip
    
    checkpoint = 0
    while FFX_memory.getMap() != 79:
        if FFX_memory.userControl():
            #print(checkpoint)
            #if FFX_memory.getMap() == 171:
            #    if FFX_memory.getCoords()[0] > -2:
            #        FFXC.set_movement(-1,-1)
            #    else:
            #        FFXC.set_movement(-0.5,-1)
            if FFX_memory.arenaFarmCheck(zone="miihen1",endGoal=capNum,report=False) and checkpoint in [28,29]:
                checkpoint = 30
            elif checkpoint == 31 and not FFX_memory.arenaFarmCheck(zone="miihen1",endGoal=capNum,report=False):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)
                
            elif checkpoint == 2:
                FFX_memory.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 8:
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
                FFX_memory.arenaFarmCheck(zone="miihen1",endGoal=capNum,report=True)
            elif checkpoint == 18 and FFX_memory.getMap() == 116:
                checkpoint += 1
            elif checkpoint in [31,42] and FFX_memory.getMap() == 59:
                checkpoint += 1
            elif checkpoint in [34,47]:
                FFX_memory.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 39:
                FFX_memory.clickToEventTemple(4)
                checkpoint += 1
            elif FFX_memory.arenaFarmCheck(zone="miihen2",endGoal=capNum,report=False) and checkpoint < 41:
                checkpoint = 41
            elif checkpoint == 42 and not FFX_memory.arenaFarmCheck(zone="miihen2",endGoal=capNum,report=False):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)
            elif checkpoint == 50:
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.miihenFarm(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                if FFX_memory.getBattleNum() == 78 and FFX_memory.arenaArray()[34] == 10:
                    #Two eyeballs of doom.
                    FFX_Battle.fleeAll()
                else:
                    if capNum == 10:
                        battleFarmAll(yunaAttack = False)
                    else:
                        battleFarmAll()
                
                if checkpoint < 32:
                    FFX_memory.arenaFarmCheck(zone="miihen1",endGoal=capNum,report=True)
                else:
                    FFX_memory.arenaFarmCheck(zone="miihen2",endGoal=capNum,report=True)
            elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

def mrrFarm(capNum:int=1):
    #Unlike other sections, MRR is expected to zone in from the Mi'ihen area and not the airship.
    FFX_menu.equipArmor(character=gameVars.neArmor(),ability=0x801D)
    while not FFX_targetPathNem.setMovement([-45,-733]): #Close to magus sisters
        pass
    while not FFX_targetPathNem.setMovement([-61,-692]): #Past magus sisters
        pass
    while not FFX_targetPathNem.setMovement([-19,-528]): #Through Clasko trigger
        pass
    while not FFX_targetPathNem.setMovement([-145,-460]): #Past O'aka's spot
        pass
    while not FFX_targetPathNem.setMovement([-219,-408]): #Past O'aka's spot
        pass
    while FFX_memory.getMap() != 92:
        FFXC.set_movement(1,1)
    
    #OK now ready to do farming.
    if gameVars.neArmor() == 0:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=0x8056) #Auto-Haste
    else:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=99) #Unequip
    FFX_memory.arenaFarmCheck(zone="mrr",endGoal=capNum,report=True)
    checkpoint = 0
    while not FFX_memory.getMap() in [194,374]:
        if FFX_memory.userControl():
            if FFX_memory.arenaFarmCheck(zone="mrr",endGoal=capNum,report=False) and checkpoint < 2:
                checkpoint = 2
            elif checkpoint == 3 and not FFX_memory.arenaFarmCheck(zone="mrr",endGoal=capNum,report=False):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)
            
            elif checkpoint == 4:
                returnToAirship()
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.mrrFarm(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                if capNum == 10:
                    battleFarmAll(yunaAttack = False)
                else:
                    battleFarmAll()
                FFX_memory.arenaFarmCheck(zone="mrr",endGoal=capNum,report=True)
            elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

def djoseFarm(capNum:int=10):
    rinEquipDump()
    airShipDestination(destNum=5)
    
    if gameVars.neArmor() == 0:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=0x8056) #Auto-Haste
    else:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=99) #Unequip
    
    checkpoint = 0
    while not FFX_memory.getMap() in [194,374]:
        if FFX_memory.userControl():
            if FFX_memory.arenaFarmCheck(zone="djose1",endGoal=capNum,report=False) and checkpoint < 24:
                checkpoint = 24
            elif checkpoint == 24 and not FFX_memory.arenaFarmCheck(zone="djose1",endGoal=capNum,report=False):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)
            if FFX_memory.arenaFarmCheck(zone="djose2",endGoal=capNum,report=False) and checkpoint < 27:
                checkpoint = 27
            elif checkpoint == 27 and not FFX_memory.arenaFarmCheck(zone="djose2",endGoal=capNum,report=False):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)
                
            elif checkpoint == 7:
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif checkpoint == 24 and FFX_memory.getMap() == 75:
                checkpoint += 1
            elif checkpoint == 27 and FFX_memory.getMap() == 93:
                checkpoint += 1
            elif checkpoint == 30 and FFX_memory.getMap() == 76:
                checkpoint += 1
            elif checkpoint == 35:
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 37:
                returnToAirship()
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.djoseFarm(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                battleFarmAll(yunaAttack=False)
                if FFX_memory.getHP()[0] < 800:
                    FFX_Battle.healUp(3)
                if checkpoint < 25:
                    FFX_memory.arenaFarmCheck(zone="djose1",endGoal=capNum,report=True)
                else:
                    FFX_memory.arenaFarmCheck(zone="djose2",endGoal=capNum,report=True)
            elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

def tPlains(capNum:int=1,autoHaste:bool=False):
    rinEquipDump()
    airShipDestination(destNum=8)
    
    FFX_memory.fullPartyFormat('yuna',fullMenuClose=False)
    FFX_menu.equipWeapon(character=1,ability=0x807A, fullMenuClose=False)
    if gameVars.neArmor() == 0 and autoHaste:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=0x8056) #Auto-Haste
    else:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=99) #Unequip
    
    checkpoint = 0
    while not FFX_memory.getMap() in [194,374]:
        if FFX_memory.userControl():
            if FFX_memory.dodgeLightning(gameVars.getLStrike()):
                print("Strike!")
                gameVars.setLStrike(FFX_memory.lStrikeCount())
            elif FFX_memory.arenaFarmCheck(zone="tPlains",endGoal=capNum,report=False) and checkpoint < 8:
                FFX_menu.equipArmor(character=gameVars.neArmor(),ability=0x801D)
                checkpoint = 8
            elif FFX_memory.getYunaMP() < 30 and checkpoint < 8:
                checkpoint = 8
            elif checkpoint == 9 and not FFX_memory.arenaFarmCheck(zone="tPlains",endGoal=capNum,report=False) \
                and FFX_memory.getYunaMP() >= 30:
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
            
            #General pathing
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.tpFarm(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                if capNum == 10:
                    battleFarmAll(yunaAttack = False)
                else:
                    battleFarmAll()
                FFX_memory.arenaFarmCheck(zone="tPlains",endGoal=capNum,report=True)
            elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    print("End of Thunder Plains section")
    return FFX_memory.arenaFarmCheck(zone="tPlains",endGoal=capNum,report=False)

def macWoods(capNum:int=10):
    airShipDestination(destNum=9)
    
    if gameVars.neArmor() == 0:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=0x8056) #Auto-Haste
    else:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=99) #Unequip
    
    checkpoint = 0
    while not FFX_memory.getMap() in [194,374]:
        if FFX_memory.userControl():
            if FFX_memory.arenaFarmCheck(zone="macLake",endGoal=capNum,report=False) and checkpoint < 6:
                checkpoint = 6
            elif checkpoint == 6 and not FFX_memory.arenaFarmCheck(zone="macLake",endGoal=capNum,report=False):
                checkpoint -= 2
            if FFX_memory.arenaFarmCheck(zone="macWoods",endGoal=capNum,report=False) and checkpoint < 14:
                checkpoint = 14
            elif checkpoint == 14 and not FFX_memory.arenaFarmCheck(zone="macWoods",endGoal=capNum,report=False):
                checkpoint -= 2
            
            #Map changes:
            elif checkpoint == 2:
                FFX_memory.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 6 and FFX_memory.getMap() == 221:
                checkpoint += 1
            elif checkpoint == 11 and FFX_memory.getMap() == 242:
                checkpoint += 1
            elif checkpoint == 14 and FFX_memory.getMap() == 221:
                checkpoint += 1
            elif checkpoint == 15:
                returnToAirship()
            
            #General pathing
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.macFarm(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                battleFarmAll(yunaAttack = False)
                if checkpoint < 7:
                    FFX_memory.arenaFarmCheck(zone="macLake",endGoal=capNum,report=True)
                else:
                    FFX_memory.arenaFarmCheck(zone="macWoods",endGoal=capNum,report=True)
            elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

def bikanel(capNum:int=10):
    airShipDestination(destNum=10)
    
    if gameVars.neArmor() == 0:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=0x8056) #Auto-Haste
    else:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=99) #Unequip
    
    checkpoint = 0
    while not FFX_memory.getMap() in [194,374]:
        if FFX_memory.userControl():
            if FFX_memory.arenaFarmCheck(zone="bikanel1",endGoal=capNum,report=False) and checkpoint < 30:
                checkpoint = 30
            elif checkpoint == 30 and not FFX_memory.arenaFarmCheck(zone="bikanel1",endGoal=capNum,report=False):
                checkpoint -= 2
            if FFX_memory.arenaFarmCheck(zone="bikanel2",endGoal=capNum,report=False) and checkpoint == 33:
                checkpoint = 34
            elif checkpoint == 35 and not FFX_memory.arenaFarmCheck(zone="bikanel2",endGoal=capNum,report=False):
                checkpoint -= 2
            
            #Map changes:
            elif checkpoint == 5 and FFX_memory.getMap() == 136:
                checkpoint += 1
            elif checkpoint == 22 and FFX_memory.getMap() == 137:
                checkpoint += 1
            elif checkpoint == 35:
                returnToAirship()
            
            #General pathing
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.bikanelFarm(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                battleFarmAll(yunaAttack = False)
                if checkpoint < 30:
                    FFX_memory.arenaFarmCheck(zone="bikanel1",endGoal=capNum,report=True)
                else:
                    FFX_memory.arenaFarmCheck(zone="bikanel2",endGoal=capNum,report=True)
            elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    initArray = FFX_memory.checkAbility(ability = 0x8002)
    if initArray[4]:
        FFX_menu.equipWeapon(character=4,ability=0x8002) #Initiative
        FFX_memory.fullPartyFormat('initiative')

def calm(capNum:int=1,autoHaste = False,airshipReturn = True):
    airShipDestination(destNum=12)
    if capNum == 1:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=99)
    elif gameVars.neArmor() == 0:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=0x8056) #Auto-Haste
    elif gameVars.neArmor() in [4,6]:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=0x801D) #Auto-Phoenix
    else:
        FFX_menu.equipArmor(character=gameVars.neArmor(),ability=99) #Unequip
    
    neArmor = False
    
    checkpoint = 0
    while not FFX_memory.getMap() == 307:
        if FFX_memory.userControl():
            if not neArmor and FFX_memory.getYunaMP() < 30:
                FFX_menu.equipArmor(character=gameVars.neArmor(),ability=0x801D)
                neArmor = True
            if FFX_memory.arenaFarmCheck(zone="calm",endGoal=capNum,report=False) and checkpoint < 5:
                checkpoint = 5
            elif checkpoint == 5 and not FFX_memory.arenaFarmCheck(zone="calm",endGoal=capNum,report=False):
                checkpoint -= 2
            elif FFX_memory.arenaFarmCheck(zone="calm2",endGoal=capNum,report=False) and checkpoint in [8,9]:
                checkpoint = 10
            elif checkpoint == 10 and not FFX_memory.arenaFarmCheck(zone="calm2",endGoal=capNum,report=False):
                checkpoint -= 2
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.calm(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            allCounts = FFX_memory.arenaArray()
            if FFX_memory.battleActive():
                if FFX_memory.getBattleNum() == 281 and gameVars.nemCheckpointAP() < 8:
                    if min(allCounts[13], allCounts[19]) >= capNum:
                        FFX_Battle.fleeAll()
                    else:
                        battleFarmAll()
                elif FFX_memory.getBattleNum() == 283 and gameVars.nemCheckpointAP() < 8:
                    if min(allCounts[4], allCounts[19],allCounts[33]) >= capNum:
                        FFX_Battle.fleeAll()
                    else:
                        battleFarmAll()
                elif FFX_memory.getBattleNum() == 284 and allCounts[33] >= capNum and gameVars.nemCheckpointAP() < 8:
                    FFX_Battle.fleeAll()
                else:
                    if capNum == 10:
                        battleFarmAll(yunaAttack = False)
                    else:
                        battleFarmAll()
                if checkpoint < 6:
                    FFX_memory.arenaFarmCheck(zone='calm',endGoal=capNum,report=True)
                else:
                    FFX_memory.arenaFarmCheck(zone='calm2',endGoal=capNum,report=True)
                
            elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    if not FFX_memory.arenaFarmCheck(zone='calm3',endGoal=capNum,report=False):
        returnToAirship()
    elif airshipReturn:
        returnToAirship()
    return FFX_memory.arenaFarmCheck(zone='calm3',endGoal=capNum,report=False)

def gagazet1(capNum:int=10):
    rinEquipDump()
    airShipDestination(destNum=13)
    FFX_menu.removeAllNEA()
    checkpoint = 0
    while not (FFX_memory.getMap() == 259 and checkpoint == 20):
        if FFX_memory.userControl():
            if FFX_memory.arenaFarmCheck(zone="gagazet1",endGoal=capNum,report=False) and checkpoint < 12:
                checkpoint = 12
            elif checkpoint == 12 and not FFX_memory.arenaFarmCheck(zone="gagazet1",endGoal=capNum,report=False):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)
                
            elif checkpoint == 2:
                while FFX_memory.userControl():
                    FFXC.set_movement(1,1)
                FFXC.set_neutral()
                FFX_memory.waitFrames(90)
                FFX_Xbox.tapDown()
                FFX_Xbox.tapB()
                FFX_memory.awaitControl()
                checkpoint += 1
            elif checkpoint == 9 and FFX_memory.getMap() == 310:
                checkpoint += 1
            elif checkpoint == 12 and FFX_memory.getMap() == 272:
                checkpoint += 1
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.gagazet1(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                if capNum == 10:
                    battleFarmAll(yunaAttack = False)
                else:
                    battleFarmAll()
                FFX_memory.arenaFarmCheck(zone="gagazet1",endGoal=capNum,report=True)
            elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    print("Done with Swimmers, now ready for Path")

def gagazet2(capNum:int=10):
    if FFX_memory.getMap() in [194,374]:
        airShipDestination(destNum=13)
    
    FFX_menu.removeAllNEA()
    checkpoint = 0
    while not checkpoint == 11:
        if FFX_memory.userControl():
            if FFX_memory.arenaFarmCheck(zone="gagazet2",endGoal=capNum,report=False) and checkpoint < 7:
                checkpoint = 7
            elif checkpoint == 7 and not FFX_memory.arenaFarmCheck(zone="gagazet2",endGoal=capNum,report=False):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)
                
            elif checkpoint == 4 and FFX_memory.getMap() == 244:
                checkpoint += 1
            elif checkpoint == 7 and FFX_memory.getMap() == 259:
                checkpoint += 1
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.gagazet2(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                battleFarmAll()
                FFX_memory.arenaFarmCheck(zone="gagazet2",endGoal=capNum,report=True)
            elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    print("Done with Path now ready for Zanarkand")

def gagazet3(capNum:int=10):
    if FFX_memory.getMap() in [194,374]:
        airShipDestination(destNum=13)
    
    FFX_menu.removeAllNEA()
    checkpoint = 0
    while not FFX_memory.getMap() in [194,374]:
        if FFX_memory.userControl():
            if FFX_memory.arenaFarmCheck(zone="gagazet3",endGoal=capNum,report=False) and checkpoint < 8:
                checkpoint = 8
            elif checkpoint == 8 and not FFX_memory.arenaFarmCheck(zone="gagazet3",endGoal=capNum,report=False):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)
                
            elif checkpoint == 2:
                while FFX_memory.userControl():
                    FFXC.set_movement(1,1)
                FFXC.set_neutral()
                FFX_memory.waitFrames(90)
                FFX_Xbox.tapDown()
                FFX_Xbox.tapDown()
                FFX_Xbox.tapDown()
                FFX_Xbox.tapB()
                FFX_memory.awaitControl()
                checkpoint += 1
            elif checkpoint == 5 and FFX_memory.getMap() == 225:
                checkpoint += 1
            elif checkpoint == 8 and FFX_memory.getMap() == 313:
                checkpoint += 1
            elif checkpoint == 11:
                returnToAirship()
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.gagazet3(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                if capNum == 10:
                    battleFarmAll(yunaAttack = False)
                else:
                    battleFarmAll()
                FFX_memory.arenaFarmCheck(zone="gagazet3",endGoal=capNum,report=True)
            elif FFX_memory.menuOpen() or FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()
    print("All of Gagazet complete")
    rinEquipDump()

def stolenFaythCave(capNum:int=10):
    airShipDestination(destNum=13)
    FFX_menu.removeAllNEA()
    
    checkpoint = 0
    while not FFX_memory.getMap() in [194,374]:
        if FFX_memory.userControl():
            if FFX_memory.arenaFarmCheck(zone="stolenfayth1",endGoal=capNum,report=False) and checkpoint < 33:
                checkpoint = 33
            elif checkpoint == 33 and not FFX_memory.arenaFarmCheck(zone="stolenfayth1",endGoal=capNum,report=False):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)
            elif FFX_memory.arenaFarmCheck(zone="stolenfayth2",endGoal=capNum,report=False) and checkpoint < 41:
                checkpoint = 41
            elif checkpoint == 41 and not FFX_memory.arenaFarmCheck(zone="stolenfayth2",endGoal=capNum,report=False):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)
            #elif checkpoint > 26 and FFX_memory.getCoords()[1] < 300:
            #    checkpoint = 22
            elif checkpoint in [5,14]:
                FFX_memory.clickToEventTemple(4)
                checkpoint += 1
            elif checkpoint == 19:
                FFX_memory.clickToEventTemple(7)
                checkpoint += 1
            elif FFX_memory.arenaFarmCheck(zone="stolenfayth3",endGoal=capNum,report=False) and checkpoint < 2:
                checkpoint = 52
            elif checkpoint == 52 and not FFX_memory.arenaFarmCheck(zone="stolenfayth3",endGoal=capNum,report=False):
                checkpoint -= 2
            elif checkpoint in [42,45]:
                FFXC.set_neutral()
                FFX_memory.waitFrames(12)
                if checkpoint == 42:
                    FFXC.set_movement(0,1)
                else:
                    FFXC.set_movement(0,-1)
                FFX_memory.waitFrames(2)
                FFXC.set_neutral()
                FFX_memory.waitFrames(12)
                FFX_Xbox.tapB()
                checkpoint += 1
            elif checkpoint == 43: #Talking to Fayth
                yojimboDialog()
                checkpoint += 1
            elif checkpoint == 49:
                FFX_memory.clickToEventTemple(3)
                checkpoint += 1
            elif checkpoint == 52:
                returnToAirship()
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.yojimbo(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                if FFX_memory.getBattleNum() in[321,329]:
                    #Do not engage the jar boys.
                    FFX_Battle.fleeAll()
                elif FFX_memory.getBattleNum() == 327 and FFX_memory.arenaFarmCheck(zone="justtonberry",endGoal=capNum,report=False):
                    #No need to die extra times on tonberries.
                    FFX_Battle.fleeAll()
                else:
                    battleFarmAll(faythCave=True)
                
                if checkpoint < 35:
                    FFX_memory.arenaFarmCheck(zone="stolenfayth1",endGoal=capNum,report=True)
                elif checkpoint < 43:
                    FFX_memory.arenaFarmCheck(zone="stolenfayth2",endGoal=capNum,report=True)
                else:
                    FFX_memory.arenaFarmCheck(zone="stolenfayth3",endGoal=capNum,report=True)
                FFX_memory.clickToControl()
            elif checkpoint == 43: #Talking to Fayth
                yojimboDialog()
                checkpoint += 1
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

def insideSin(capNum:int=10):
    airShipDestination(destNum=0)
    FFX_menu.removeAllNEA()
    
    while FFX_memory.getMap() != 203:
        FFXC.set_movement(0,-1)
    FFXC.set_neutral()
    
    checkpoint = 0
    while not FFX_memory.getMap() in [194,374]:
        if FFX_memory.userControl():
            #Events
            if FFX_memory.getMap() == 296: #Seymour battle
                print("We've reached the Seymour screen.")
                FFX_memory.fullPartyFormat('yuna')
                FFXC.set_movement(0, 1)
                FFX_memory.waitFrames(30 * 5)
                FFXC.set_neutral()
                FFX_Battle.omnis()
                FFX_memory.clickToControl()
                FFX_memory.fullPartyFormat('initiative')
            
            #End of first area logic
            elif FFX_memory.arenaFarmCheck(zone="sin1",endGoal=capNum,report=False) and checkpoint in [38,39]:
                checkpoint = 40
            elif checkpoint == 40 and not FFX_memory.arenaFarmCheck(zone="sin1",endGoal=capNum,report=False):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)
            elif checkpoint < 41 and FFX_memory.getMap() == 204:
                checkpoint = 41
            
            #End of second area logic
            elif FFX_memory.arenaFarmCheck(zone="sin2",endGoal=capNum,report=False) and checkpoint < 67:
                checkpoint = 67
            elif checkpoint == 67 and not FFX_memory.arenaFarmCheck(zone="sin2",endGoal=capNum,report=False):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)
            elif checkpoint < 68 and FFX_memory.getMap() == 327:
                checkpoint = 68
            elif checkpoint == 69:
                returnToAirship()
            elif checkpoint >= 65 and FFX_memory.getTidusMP() < 20: #Tidus low on MP
                FFX_targetPathNem.setMovement([550,485])
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                FFX_memory.waitFrames(3)
                FFX_memory.awaitControl()
                FFX_memory.touchSaveSphere()
                FFX_targetPathNem.setMovement([-200,-525])
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                checkpoint = 66
            
            #General Pathing
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.sin(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                FFX_Screen.awaitTurn()
                advancedBattleLogic()
                if checkpoint < 40:
                    print("Ahrimans only:")
                    FFX_memory.arenaFarmCheck(zone="sin1",endGoal=capNum,report=True)
                else:
                    FFX_memory.arenaFarmCheck(zone="sin2",endGoal=capNum,report=True)
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()

def omegaRuins(capNum:int=10):
    FFX_nem_menu.rikkuProvoke()
    FFX_menu.removeAllNEA()
    
    #rinEquipDump()
    #FFX_menu.autoSortEquipment()
    airShipDestination(destNum=13, forceOmega=True)
    
    checkpoint = 0
    while not FFX_memory.getMap() in [194,374]:
        if FFX_memory.userControl():
            if FFX_memory.arenaFarmCheck(zone="omega",endGoal=capNum,report=False) and checkpoint < 2:
                checkpoint = 2
            elif checkpoint == 2 and not FFX_memory.arenaFarmCheck(zone="omega",endGoal=capNum,report=False):
                checkpoint -= 2
                print("Checkpoint reached: ", checkpoint)
            elif FFX_memory.getTidusMP() < 20:
                FFX_memory.touchSaveSphere()
            elif checkpoint == 3:
                returnToAirship()
            elif FFX_targetPathNem.setMovement(FFX_targetPathNem.omega(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                advancedBattleLogic()
                FFX_memory.arenaFarmCheck(zone="omega",endGoal=capNum,report=True)
                FFX_memory.clickToControl()
            elif FFX_memory.diagSkipPossible() or FFX_memory.menuOpen():
                FFX_Xbox.tapB()
    
    #Keep this so we can add in the Omega kill later.
    #if gameVars.neArmor() == 0:
    #    FFX_menu.equipArmor(character=gameVars.neArmor(),ability=0x8056) #Auto-Haste
    #elif gameVars.neArmor() in [4,6]:
    #    FFX_menu.equipArmor(character=gameVars.neArmor(),ability=0x800A) #Auto-Phoenix
    #else:
    #    FFX_menu.equipArmor(character=gameVars.neArmor(),ability=99) #Unequip

def getEquipment(equip=True):
    FFX_memory.waitFrames(20)
    FFX_Xbox.tapB()
    FFX_memory.waitFrames(5)
    FFX_Xbox.tapUp()
    FFX_Xbox.tapB()
    FFX_memory.waitFrames(5)
    if equip == True:
        FFX_Xbox.tapUp()
    FFX_Xbox.tapB() #Equip weapon for Rikku
    FFX_memory.waitFrames(5)

def otherStuff():
    arenaNPC()
    FFX_Xbox.tapB()
    returnToAirship()