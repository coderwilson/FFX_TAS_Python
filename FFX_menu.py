import time
import FFX_Xbox
import FFX_Screen
import FFX_menuGrid
import FFX_Logs
import FFX_memory

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

def gridUp():
    FFX_menuGrid.gridUp()

def gridDown():
    FFX_menuGrid.gridDown()

def gridLeft():
    FFX_menuGrid.gridLeft()

def gridRight():
    FFX_menuGrid.gridRight()

def awaitMove():
    print("Sphere Grid: Waiting for Move command to be highlighted")
    while FFX_memory.sGridActive() == False:
        print("The Sphere Grid isn't even open! Awaiting manual recovery.")
        time.sleep(1)
    complete = False
    while complete == False:
        menuVal = FFX_memory.sGridMenu()
        if menuVal == 11 or menuVal == 255:
            FFX_Xbox.menuB()
        elif menuVal == 7:
            cursorLoc = FFX_memory.cursorLocation()
            if cursorLoc[0] == 51 or cursorLoc[1] == 243:
                FFX_Xbox.menuUp()
            FFX_Xbox.menuB()
            complete = True
            time.sleep(0.25)
    print("Move command highlighted. Good to go.")

def awaitUse():
    print("Sphere Grid: Waiting for Use command to be highlighted")
    while FFX_memory.sGridActive() == False:
        print("The Sphere Grid isn't even open! Awaiting manual recovery.")
        time.sleep(1)
    complete = False
    while complete == False:
        menuVal = FFX_memory.sGridMenu()
        print("Menu value: ", menuVal)
        if menuVal == 7:
            cursorLoc = FFX_memory.cursorLocation()
            if cursorLoc[0] == 102 or cursorLoc[1] == 14:
                FFX_Xbox.menuDown()
            FFX_Xbox.menuB()
            complete = True
            time.sleep(0.25)
        else:
            FFX_Xbox.menuB()
    print("Use command highlighted. Good to go.")

def awaitQuitSG():
    print("Sphere Grid: attempting to quit")
    while FFX_memory.sGridActive():
        menuVal = FFX_memory.sGridMenu()
        if menuVal == 255:
            FFX_Xbox.menuA()
        elif menuVal == 11:
            FFX_Xbox.menuB()
        else:
            FFX_Xbox.menuA()
    print("Back to the main menu")

def autoSortItems_New(manual, menusize):

    while not FFX_memory.menuOpen():
        openMenu()

    currentmenuposition = FFX_memory.getMenuCursorPos()

    targetmenuposition = 1
    menudistance = abs(targetmenuposition - currentmenuposition)

    if menudistance < (menusize / 2 - 1):
        for i in range(menudistance):
            if targetmenuposition > currentmenuposition:
                FFX_Xbox.menuDown()
            else:
                FFX_Xbox.menuUp()
    else:
        for i in range(menusize - menudistance):
            if targetmenuposition > currentmenuposition:
                FFX_Xbox.menuUp()
            else:
                FFX_Xbox.menuDown()

    FFX_Xbox.menuB()
    time.sleep(0.4)
    FFX_Xbox.menuA()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    time.sleep(0.4)
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    time.sleep(0.4)
    if manual == 'y':
        FFX_Xbox.menuLeft()
        FFX_Xbox.menuB()
    elif manual == 'n':
        FFX_Xbox.menuA()
        FFX_Xbox.menuA()
        #FFX_memory.closeMenu()
    else:
        FFX_Xbox.menuA()
        FFX_Xbox.menuA()
        #FFX_memory.closeMenu()
    return 2

def autoSortItems(manual):
    FFX_memory.openMenu()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.4)
    FFX_Xbox.menuA()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    time.sleep(0.4)
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    if manual == 'y':
        FFX_Xbox.menuLeft()
        FFX_Xbox.menuB()
    elif manual == 'n':
        FFX_memory.closeMenu()
    else:
        FFX_memory.closeMenu()

def Liki():
    print("Menu - SS Liki")
    openGrid(character=0)
    FFX_memory.waitFrames(10)
    
    #Move to the Def node just to the left
    print("Sphere grid on Tidus, learn Cheer and Str +1")
    FFX_menuGrid.moveFirst()
    gridUp()
    gridUp()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    
    #Activate Str and Cheeer nodes
    FFX_menuGrid.selSphere('power','d','left')
    FFX_menuGrid.useAndUseAgain() #Str +1 node
    FFX_menuGrid.selSphere('ability','d','none') # Cheer
    FFX_Xbox.menuB()
    FFX_menuGrid.useAndQuit()
    FFX_Xbox.menuA()

def Geneaux():
    openGrid(character=0)
    
    FFX_menuGrid.moveFirst()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def LucaWorkers():
    openGrid(character=0)
    
    FFX_menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    gridDown()
    gridDown()
    gridRight()
    time.sleep(0.1)
    if FFX_memory.sGridNodeSelected()[0] == 2:
        print("No early haste")
        earlyHaste = 0
    else:
        print("Early haste, can haste for Oblitzerator")
        earlyHaste = 1
    
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('mana','d','none')
    if earlyHaste == 1:
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('ability','d','none') # Haste
        
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()
    return earlyHaste

def lateHaste():
    openGrid(character=0)
    FFX_menuGrid.moveFirst()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('ability','d','none') # Haste
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def afterBlitz():
    FFX_memory.openMenu()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.3)
    FFX_Xbox.menuA()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuB() #Manually sorting items
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Get the map out of the way
    FFX_memory.closeMenu()

def mrrGrid1():
    print("Menuing: start of MRR ")
    openGrid(character=4)
    FFX_menuGrid.moveFirst()
    gridRight()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    print("Determining state of Wakka late menu")
    #time.sleep(60) #Use for testing only!
    if FFX_memory.getSLVLWakka() < 3:
        wakkaLateMenu = True
        print("Deferring Wakka's remaining grid for later.")
        #time.sleep(60) #Use for testing only!
    else:
        wakkaLateMenu = False
        print("Completing Wakka's remaining grid now.")
        #time.sleep(60) #Use for testing only!
        FFX_menuGrid.useAndMove()
        gridDown()
        gridDown()
        gridRight()
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('power','d','none')
    print("Wakka late menu: ", wakkaLateMenu)
    
    FFX_menuGrid.useAndQuit()
    
    FFX_memory.closeMenu()
    
    return wakkaLateMenu

def mrrGrid2(wakkaLateMenu):
    if wakkaLateMenu != False:
        if FFX_memory.getSLVLWakka() >= 3:
            print("Catching up Wakka's sphere grid.")
            openGrid(character=4)
            
            FFX_menuGrid.moveFirst()
            gridDown()
            gridDown()
            gridRight()
            FFX_menuGrid.moveAndUse()
            FFX_menuGrid.selSphere('power','d','none')
            FFX_menuGrid.useAndQuit()
            FFX_memory.closeMenu()
            wakkaLateMenu = False
        else:
            print("Not enough sphere levels yet.")
    return wakkaLateMenu

def mrrGridYuna():
    print("Yuna levels good to level up.")
    openGrid(character=1)
    FFX_menuGrid.useFirst() #Sphere grid on Yuna first
    FFX_menuGrid.selSphere('magic','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('mana','u','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('mana','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('mana','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('mana','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_Xbox.menuA()

def battleSiteGrid():
    print("Doing the menu stuff")
    openGrid(character=1)
    FFX_menuGrid.moveFirst()
    gridLeft()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('mana','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    
    FFX_menuGrid.useShiftLeft('Kimahri') #Sphere grid on Kimahri
    FFX_menuGrid.moveFirst()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndQuit()
    
    #Sort items
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(15)
    FFX_Xbox.menuA()
    FFX_memory.waitFrames(15)
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(15)
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(15)
    FFX_Xbox.menuA()
    FFX_memory.waitFrames(15)
    FFX_Xbox.menuA()
    FFX_memory.waitFrames(15)
    
    #Wakka's weapon
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Equip
    wakkaPos = FFX_memory.getCharFormationSlot(4)
    if FFX_memory.getCharCursorPos() != wakkaPos:
        while FFX_memory.getCharCursorPos() != wakkaPos:
            FFX_Xbox.menuDown()
            FFX_memory.waitFrames(1)
    FFX_memory.waitFrames(30)
    FFX_Xbox.menuB() #Wakka
    FFX_memory.waitFrames(30)
    FFX_Xbox.menuB() #Weapon
    FFX_memory.waitFrames(30)
    FFX_Xbox.menuB() #Back to default.
    FFX_memory.waitFrames(30)
    
    FFX_memory.closeMenu()
    FFX_memory.fullPartyFormat('battleSite')

def battleSiteOaka1():
    FFX_memory.clickToDiagProgress(96)
    FFX_memory.waitFrames(12)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Items
    FFX_memory.waitFrames(30)
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB() #Sell
    
    itemOrder = FFX_memory.getItemsOrder()
    itemCursor = 1
    while itemOrder[itemCursor] != 70: #Don't sell anything Power Sphere or after.
        if itemOrder[itemCursor] == 3:
            print("Keep Mega-Potions")
        elif itemOrder[itemCursor] == 6:
            print("Keep Phoenix Downs.")
        else: #Sell all except for Mega Potions and Phoenix Downs.
            FFX_Xbox.menuB()
            FFX_Xbox.menuUp()
            if FFX_memory.getItemCountSlot(itemCursor) > 10:
                FFX_Xbox.menuUp()
            FFX_Xbox.menuB() #Sell this item
        if itemOrder[itemCursor + 1] == 70:
            print("Done with selling items.")
        elif itemCursor % 2 == 1:
            FFX_Xbox.menuRight()
        else:
            FFX_Xbox.menuLeft()
            FFX_Xbox.menuDown()
        itemCursor += 1
    
    FFX_memory.closeMenu()

def battleSiteOaka2():
    FFX_memory.clickToDiagProgress(74)
    FFX_memory.clickToDiagProgress(96)
    while not FFX_memory.menuOpen():
        FFX_Xbox.menuB()
        FFX_memory.waitFrames(20)
    FFX_memory.waitFrames(20)
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB() #Sell
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    
    while FFX_memory.getGilvalue() < 10890:
        FFX_Xbox.menuDown()
        FFX_memory.waitFrames(6)
        FFX_Xbox.menuB()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuB()
        FFX_Xbox.menuRight()
    FFX_Xbox.menuA()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() #Purchase Sentry
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() #Equip Sentry
    #FFX_Xbox.menuA()
    #FFX_Xbox.menuA()
    
    #Re-sort items - should be Mega Potions first slot, followed by Phoenix Downs
    #FFX_memory.openMenu()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuB()
    #FFX_memory.waitFrames(6)
    #FFX_Xbox.menuA()
    #FFX_Xbox.menuRight()
    #FFX_Xbox.menuB()
    #FFX_memory.waitFrames(6)
    #FFX_Xbox.menuRight()
    #FFX_Xbox.menuB()
    
    FFX_memory.closeMenu()

def djoseFormation():
    goal = [255,0,4,2,3,255,5,1]
    print("Checking formation. Should be: ", goal)
    current = FFX_memory.getOrder()
    if current != goal:
        FFX_memory.openMenu()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuB() #Formation option
        
        #If Valefor did not faint, formation should be: Y A K T W L
        #Otherwise formation should be: Y L K T A W
        
        #The end goal is: T W A K L Y
        #Numerically, the end goal is 0,4,2,3,5,1
        
        #Note, goal[0] is unused because I prefer to count from 1.
        #255 is an empty slot in FFX code.
        
        character = 0
        cursor = 1
        while current != goal:
            if current[cursor] != goal[cursor]:
                character = goal[cursor]
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                cursor += 1
                if cursor > 6:
                    cursor = 1
                while current[cursor] != character:
                    FFX_Xbox.menuDown()
                    cursor += 1
                    if cursor > 6:
                        cursor = 1
                FFX_Xbox.menuB()
            else:
                FFX_Xbox.menuDown()
                cursor += 1
                if cursor > 6:
                    cursor = 1
            current = FFX_memory.getOrder()
        
        #if vFaint == False:
        #    FFX_Xbox.menuB()
        #    FFX_Xbox.menuUp()
        #    FFX_Xbox.menuB() #Yuna to 6, Lulu to 1 for now
        #    FFX_Xbox.menuUp()
        #    FFX_Xbox.menuB()
        #    FFX_Xbox.menuUp()
        #    FFX_Xbox.menuB() #Wakka to 4, Tidus to 5
        #    FFX_Xbox.menuB()
        #    FFX_Xbox.menuUp()
        #    FFX_Xbox.menuB() #Wakka to 3, Kimahri to 4
        #    FFX_Xbox.menuB()
        #    FFX_Xbox.menuUp()
        #    FFX_Xbox.menuB() #Wakka to 2, Auron to 3
        #    FFX_Xbox.menuUp()
        #    FFX_Xbox.menuB()
        #    FFX_Xbox.menuUp()
        #    FFX_Xbox.menuUp()
        #    FFX_Xbox.menuB() #Lulu to 5, Tidus to 1
        #else:
        #    FFX_Xbox.menuB()
        #    FFX_Xbox.menuUp()
        #    FFX_Xbox.menuB() #Yuna to 6, Wakka to 1 for now
        #    FFX_Xbox.menuUp()
        #    FFX_Xbox.menuB()
        #    FFX_Xbox.menuUp()
        #    FFX_Xbox.menuUp()
        #    FFX_Xbox.menuB() #Auron to 3, Kimahri to 5
        #    #now W L A T K Y
        #    #The end goal is: T W A K L Y
        #    FFX_Xbox.menuDown()
        #    FFX_Xbox.menuB()
        #    FFX_Xbox.menuDown()
        #    FFX_Xbox.menuB() #Tidus to 5, Kimahri to 4
        #    FFX_Xbox.menuB()
        #    FFX_Xbox.menuUp()
        #    FFX_Xbox.menuUp()
        #    FFX_Xbox.menuUp()
        #    FFX_Xbox.menuB() #Tidus to 2, Lulu to 5
        #    FFX_Xbox.menuB()
        #    FFX_Xbox.menuUp()
        #    FFX_Xbox.menuB() #Tidus to 1, Wakka to 2
            
        FFX_memory.closeMenu()

def djoseTemple():
    openGrid(character=0)
    
    #Sphere grid Tidus
    FFX_menuGrid.moveFirst()
    gridUp()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse() #Move to Str sphere near Lv.2 lock
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain() #Str +1
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain() #HP +200
    FFX_menuGrid.selSphere('speed','d','none')
    #Now sphere grid on Wakka
    
    if FFX_memory.getSLVLWakka() >= 5:
        FFX_menuGrid.useShiftRight('wakka') #Agi +2
        FFX_menuGrid.moveFirst()
        
        gridRight()
        gridLeft()
        gridLeft()
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('power','u','up')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def moonflowWakkaWeap():
    FFX_memory.openMenu()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.3)
    FFX_Xbox.menuB()
    time.sleep(0.15)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()

def moonflowRikku():
    FFX_memory.openMenu()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() #Formation
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Yuna to 7, Auron to 3
    FFX_memory.closeMenu()

def guadoRikku():
    FFX_memory.openMenu()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() #Formation
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Rikku to 2, Wakka to 4
    FFX_memory.closeMenu()

def plainsArmor():
    FFX_memory.openMenu()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Equip
    time.sleep(0.2)
    FFX_Xbox.menuB() #Tidus
    time.sleep(0.2)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Armor
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() #Lightningproof armor
    
    FFX_memory.closeMenu()

def mWoods():
    FFX_memory.awaitControl()
    FFXC.set_movement(0, 1)
    time.sleep(0.8)
    FFXC.set_movement(-1, 1)
    time.sleep(0.5)
    FFXC.set_movement(0, 1)
    FFX_memory.clickToEvent()
    FFXC.set_neutral()
    while not FFX_memory.menuOpen():
        FFX_Xbox.menuB() #Talking through O'aka's conversation.
    
    FFX_memory.closeMenu()
    #autoSortItems('n')
    
    FFXC.set_movement(0, 1)
    FFX_memory.clickToEvent()
    FFXC.set_neutral()
    FFX_memory.waitFrames(30)
    FFX_Xbox.menuB() #Talk to O'aka again
    FFX_memory.waitFrames(30)
    if FFX_memory.getGilvalue() < 9100: #Memory hack, we must fix this later.
        FFX_memory.setGilValue(9999999)
    FFX_Xbox.menuB() #Talk to O'aka once again
    while not FFX_memory.menuOpen():
        FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuB() #Buy
    time.sleep(0.2)
    FFX_Xbox.menuB() #Sonic Steel
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() #confirm
    time.sleep(0.05)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() #equip
    FFX_memory.closeMenu()

def mLakeGrid():
    openGrid(character=1) #Start with Yuna
    FFX_menuGrid.moveFirst()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_menuGrid.selSphere('Lv2','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useShiftLeft('rikku') #Shift to Rikku
    FFX_menuGrid.moveFirst()
    
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','u','none')
    
    FFX_menuGrid.useShiftRight('kimahri') #And last is Yuna
    FFX_menuGrid.moveFirst()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('Lv1','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('Lv1','d','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('ability','u','none') #Steal
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('ability','u','none') #Use
    FFX_menuGrid.useAndQuit()
    
    #Heal up
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuB()
    #time.sleep(0.6)
    #FFX_Xbox.menuB()
    #time.sleep(0.6)
    #FFX_Xbox.menuB()
    #time.sleep(0.6)
    #FFX_Xbox.menuB() #Tidus
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuB() #Kimahri
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuDown() #Skip Rikku
    #FFX_Xbox.menuB() #Wakka
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuB() #Auron
    #FFX_Xbox.menuB() #No need to heal Yuna or Lulu
    #FFX_Xbox.menuA()
    #FFX_Xbox.menuA()
    
    #Formation
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuB() #Wakka to 3, Rikku to 4
    FFX_memory.closeMenu()

def macTemple(blitzWin):
    openGrid(character=0)
    
    FFX_menuGrid.useFirst()
    FFX_menuGrid.selSphere('Lv2','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridRight()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridRight()
    if blitzWin == True:
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('strength','d','none')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('power','u','none')
        FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def afterSeymour():
    openGrid(character=0)
    FFX_menuGrid.moveFirst()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power', 'd', 'none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power', 'u', 'none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed', 'd', 'none')
    FFX_menuGrid.useAndQuit()
    currentmenuposition = 1
    #currentmenuposition = autoSortItems_New('n', 11)
    currentmenuposition = equipSonicSteel()
    #currentmenuposition = FFX_memory.fullPartyFormat_New('macalaniaescape',11)
    FFX_memory.closeMenu()

def homeGrid():
    openGrid(character=0)
    FFX_menuGrid.moveFirst()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndQuit()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuB() #Formation
    #FFX_Xbox.menuB() #Tidus
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuB() #Tidus to slot 1, Auron to 3
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuB() #Wakka to 2, Kimahri to 4
    FFX_memory.closeMenu()
    #itemPos(20,9)

def homeHeal(): #Hi-Potions on front three.
    FFX_memory.openMenu()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.4)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_memory.closeMenu()

def weddingPrep():
    #itemPos(56, 7) #Make sure Lunar Curtain is in slot 7
    #itemPos(8, 8) #Elixir in slot 8
    #FFX_memory.openMenu()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuB() #Tidus to 1, Kimahri to 4
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuB() #Kimahri to 3, Auron to 4
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuB() #Rikku to 2, Wakka to 5
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuB() #Wakka to 5, Lulu to 6 (maybe remove this if the formation is wrong later)
    
    #FFX_memory.closeMenu()
    
    #Doesn't matter about Rikku's overdrive, that will auto sort.
    print("Wedding prep function is no longer used.")

def beforeGuards(): #Incomplete
    FFX_memory.clickToControl()
    FFX_memory.openMenu()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Items
    time.sleep(0.8)
    FFX_Xbox.menuA()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB() #
    time.sleep(0.4)
    FFX_Xbox.menuB()

def equipSonicSteel_Old(menusize):
    print("Equipping Sonic Steel")
    FFX_memory.awaitControl()
    while not FFX_memory.menuOpen():
        FFX_memory.openMenu()
    currentmenuposition = FFX_memory.getMenuCursorPos()
    targetmenuposition = 4
    menudistance = abs(targetmenuposition - currentmenuposition)

    if menudistance < menusize / 2:
        for i in range(menudistance):
            if targetmenuposition > currentmenuposition:
                FFX_Xbox.menuDown()
            else:
                FFX_Xbox.menuUp()
    else:
        for i in range(menusize - menudistance):
            if targetmenuposition > currentmenuposition:
                FFX_Xbox.menuUp()
            else:
                FFX_Xbox.menuDown()

    FFX_Xbox.menuB()
    time.sleep(0.5)
    FFX_Xbox.menuB()  # Tidus
    time.sleep(0.5)
    FFX_Xbox.menuB()  # Weapon
    time.sleep(0.5)
    FFX_Xbox.menuDown()
    time.sleep(0.05)
    #while not FFX_Screen.PixelTestTol(1058, 517, (220, 220, 220), 5):
    #    FFX_Xbox.menuDown()
    #    time.sleep(0.05)
    FFX_Xbox.menuB()
    time.sleep(0.1)
    FFX_Xbox.menuA()

    return 5

def equipSonicSteel():
    print("Equipping Sonic Steel")
    FFX_memory.awaitControl()
    while not FFX_memory.menuOpen():
        FFX_memory.openMenu()
    
    while FFX_memory.getMenuCursorPos() != 4:
        FFX_Xbox.menuDown()

    FFX_Xbox.menuB()
    FFX_memory.waitFrames(15)
    FFX_Xbox.menuB()  # Tidus
    FFX_memory.waitFrames(15)
    FFX_Xbox.menuB()  # Weapon
    FFX_memory.waitFrames(15)
    
    weaponHandles = FFX_memory.weaponArrayCharacter(0)
    weaponNum = 255
    while len(weaponHandles) > 0:
        currentHandle = weaponHandles.pop(0)
        if currentHandle.hasAbility(32769): #First Strike
            weaponNum = id
    
    if weaponNum == 255:
        return False #Item is no in inventory.
    
    while FFX_memory.equipWeapCursor() != weaponNum:
        if FFX_memory.equipWeapCursor() < weaponNum:
            FFX_Xbox.tapDown()
        else:
            FFX_Xbox.tapUp()
        FFX_memory.waitFrames(1)
    
    FFX_memory.waitFrames(1)
    FFX_memory.waitFrames(1)
    FFX_Xbox.menuA()
    FFX_memory.waitFrames(12)

    return 5

def equipSonicSteel_old2():
    print("Equipping Sonic Steel")
    FFX_memory.awaitControl()
    FFX_memory.openMenu()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Equip
    time.sleep(0.5)
    FFX_Xbox.menuB() #Tidus
    time.sleep(0.5)
    FFX_Xbox.menuB() #Weapon
    time.sleep(0.5)
    FFX_Xbox.menuDown()
    time.sleep(0.05)
    while not FFX_Screen.PixelTestTol(1058,517,(220, 220, 220),5):
        FFX_Xbox.menuDown()
        time.sleep(0.05)
    FFX_Xbox.menuB()
    FFX_memory.closeMenu()

def viaPurifico():
    openGrid(character=2) #Auron
    
    FFX_menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('Lv2','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('Lv2','d','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    time.sleep(0.3)
    gridLocation = FFX_memory.sGridNodeSelected()
    if gridLocation[0] != 242: #We have extra levels, changes the path slightly.
        gridUp()
        gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('mana','u','none')
    
    FFX_menuGrid.useShiftRight('yuna')
    FFX_menuGrid.useFirst()
    FFX_menuGrid.selSphere('tele','d','up')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('mana','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    
    FFX_menuGrid.useAndMove()
    gridRight()
    gridRight()
    gridRight()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('mana','d','none')
    
    FFX_menuGrid.useAndMove()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridLeft()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    
    FFX_menuGrid.useAndMove()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def seymourNatusBlitzWin():
    openGrid(character=1)
    
    FFX_menuGrid.useFirst()
    FFX_menuGrid.selSphere('tele','d','up2')
    FFX_menuGrid.useAndUseAgain()
    
    FFX_menuGrid.selSphere('power','u','none') #Str
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none') #Str
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none') #Def +3
    
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    
    FFX_menuGrid.useAndMove()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndQuit()
    
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_memory.closeMenu()

def seymourNatusBlitzLoss():
    openGrid(character=1)
    
    FFX_menuGrid.useFirst()
    FFX_menuGrid.selSphere('tele','d','none')
    gridLeft()
    FFX_menuGrid.useAndUseAgain()
    
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','none')
    
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('friend','d','none')
    gridUp()
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndMove()
    
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','left')
    FFX_menuGrid.useAndQuit()
    
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_memory.closeMenu()

def prepCalmLands(blitzWin):
    openGrid(character=1)
    if blitzWin == True:
        FFX_menuGrid.moveFirst()
        gridUp()
        gridUp()
        gridDown()
        gridDown()
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('power','d','none')
    else:
        FFX_menuGrid.moveFirst()
        gridRight()
        gridRight()
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('power','d','none')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def afterRonso(ver, blitzWin):
    openGrid(character=5)
    FFX_menuGrid.moveFirst()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('Lv2','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('Lv3','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridDown()
    gridDown()
    FFX_menuGrid.moveShiftRight('Yuna')
    FFX_menuGrid.useFirst()
    
    if ver == 1 or ver == 2: #Two of each
        FFX_menuGrid.selSphere('friend','d','d2')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('power','u','none')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('power','u','none')
        FFX_menuGrid.useShiftLeft('Lulu')
        FFX_menuGrid.moveFirst()
        gridUp()
        gridUp()
        gridUp()
        gridUp()
        FFX_menuGrid.moveShiftRight('Yuna')
        FFX_menuGrid.useFirst()
        FFX_menuGrid.selSphere('friend','d','none')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('speed','u','none')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('speed','u','none')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('power','u','none')
    
    if ver == 4: #Four return spheres
        if blitzWin == True:
            FFX_menuGrid.selSphere('ret','d','yunaspec')
            FFX_menuGrid.selSphere('ret','d','d5')
        FFX_menuGrid.useAndMove()
        gridLeft()
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('Lv1','d','none')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('mana','u','none')
        FFX_menuGrid.useAndMove()
        gridRight()
        gridRight()
        gridDown()
        FFX_menuGrid.moveAndUse()
        FFX_menuGrid.selSphere('speed','d','none')
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('power','u','none')
    
    #Tidus armor break
    #Changing - doing this after Flux. We can grab ZombieStrike at that time as well.
    #FFX_menuGrid.useShiftRight('Tidus')
    #FFX_menuGrid.moveFirst()
    #gridRight()
    #gridRight()
    #gridRight()
    #gridDown()
    #gridDown()
    #gridDown()
    #gridDown()
    #gridDown()
    #FFX_menuGrid.moveAndUse()
    #FFX_menuGrid.selSphere('ability','d','none')
    FFX_menuGrid.useAndQuit()
        
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuB()
    
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuB() #Formation done
    #time.sleep(0.5)
    #FFX_Xbox.menuA()
    #time.sleep(0.5)
    #FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.3)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.3)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #First strike for Yuna
    time.sleep(0.3)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Confirm first strike on weapon
    time.sleep(0.3)
    FFX_Xbox.menuB()
    FFX_memory.closeMenu()

def beforeFlux():
    FFX_memory.openMenu()
    
    #Customizing Auron's weapon
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    time.sleep(0.5)
    
    complete = 0
    while complete == 0:
        if FFX_Screen.imgSearch('shimmerBlade2.JPG', 0.95):
            FFX_Xbox.menuB()
            time.sleep(0.5)
            FFX_Xbox.menuDown()
            FFX_Xbox.menuDown()
            FFX_Xbox.menuB()
            time.sleep(0.2)
            FFX_Xbox.menuUp()
            FFX_Xbox.menuB()
            time.sleep(0.2)
            FFX_Xbox.menuB()
            FFX_Xbox.menuA()
            FFX_Xbox.menuA()
            
            complete = 1
        else:
            FFX_Xbox.menuDown()
            time.sleep(0.05)
            
    #Next, fix formation, since it's on the way.
    FFX_Xbox.menuUp()
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuA()
    
    #Now to equip the weapon
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() #Equip
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Auron
    time.sleep(0.2)
    FFX_Xbox.menuB() #Weapons
    time.sleep(0.2)
    while not FFX_Screen.imgSearch('shimmerBlade3.JPG', 0.95):
        FFX_Xbox.menuDown()
        time.sleep(0.05)
    FFX_Xbox.menuB()
    FFX_memory.closeMenu()

def afterFlux():
    openGrid(character=0)
    
    #Sphere grid on Tidus
    FFX_menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('Lv4','d','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('ability','u','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('ability','d','none')
    FFX_menuGrid.useAndQuit()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuB() #Swap position 7 and 3
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuB() #Swap 7 and 2. This should put Tidus first, Auron third, and Yuna in slot 7.
    FFX_memory.closeMenu()

def gagazetCave():
    #Occurs after swimming
    FFX_memory.openMenu()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Yuna to slot 2
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Auron to slot 3
    FFX_memory.closeMenu()

def endGameSwap():
    formation = FFX_memory.getOrder()
    if formation[2] == 1:
        FFX_memory.openMenu()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuB()
        FFX_Xbox.menuDown()
        FFX_Xbox.menuB()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuB() #Yuna from position 2 to 7
        FFX_memory.closeMenu()

def endGameSwap2():
    formation = FFX_memory.getOrder()
    if formation[7] == 1:
        FFX_memory.openMenu()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuB()
        FFX_Xbox.menuDown()
        FFX_Xbox.menuB()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuB() #Yuna from position 7 to 2
        FFX_memory.closeMenu()

def BFA():
    openGrid(character=1) #Yuna final grid
    
    FFX_menuGrid.useFirst()
    FFX_menuGrid.selSphere('attribute','d','l5')
    time.sleep(0.07)
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('ret','d','torikku')
    time.sleep(0.07)
    FFX_menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridLeft()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','u','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('ability','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','u','left')
    FFX_menuGrid.useShiftLeft('Kimahri')
    FFX_menuGrid.useFirst()
    FFX_menuGrid.selSphere('skill','d','up')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def skReturn():
    openGrid(character=1)
    FFX_menuGrid.useFirst()
    FFX_menuGrid.selSphere('friend','d','d2')
    FFX_menuGrid.useAndUseAgain() #Friend sphere to Lulu
    FFX_menuGrid.selSphere('luck','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('fortune','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_Xbox.menuA()

def skMixed():
    openGrid(character=1)
    FFX_menuGrid.useFirst()
    FFX_menuGrid.selSphere('ret','d','r2')
    FFX_menuGrid.useAndMove() #Return to Wakka's grid
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('mana','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('lv1','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('luck','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('fortune','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridDown()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndQuit()
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()

def skFriend(): #incomplete / game over
    print("Not yet programmed")

def skReturn2():
    openGrid(character=1)
    
    FFX_menuGrid.useFirst()
    FFX_menuGrid.selSphere('ret','d','aftersk')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndQuit()

def itemPos(item, pos):
    counter = 0
    cursor = 1
    currentSlot = FFX_memory.getItemSlot(item)
    if currentSlot == pos:
        print("Item is already in the correct slot. Item number: ", item)
        return
    if currentSlot == 0: #This is a hard run killer.
        while currentSlot == 0:
            counter += 1
            print("You are missing a critical item and are unable to proceed. Message: ", counter)
            print("Item number: ", item)
            time.sleep(10)
    FFX_memory.openMenu()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.8)
    FFX_Xbox.menuA()
    time.sleep(0.2)
    FFX_Xbox.menuRight()
    time.sleep(0.2)
    FFX_Xbox.menuB() #Sort
    time.sleep(0.6)
    FFX_Xbox.menuB() #Manual
    
    item1 = currentSlot
    item2 = pos
    
    if item1 > item2: #Quick bubble sort
        item3 = item2
        item2 = item1
        item1 = item3
    
    print("Swapping items: ", item1, " | ", item2)
    
    if item1 % 2 == 0: #First item is in the right-hand column
        FFX_Xbox.menuRight()
        cursor += 1
    
    while cursor < item1:
        FFX_Xbox.menuDown()
        cursor += 2
    
    #time.sleep(10) #Testing purposes only
    FFX_Xbox.menuB() #We should now have selected the first item.
    #time.sleep(0.4)
    
    if item1 % 2 != item2 % 2: #First and second items are on different columns
        print("Items are in opposing columns. Switching columns.")
        if item1 % 2 == 0:
            FFX_Xbox.menuLeft()
            FFX_Xbox.menuDown()
        else:
            FFX_Xbox.menuRight()
        cursor += 1
    
    if cursor == item2:
        #time.sleep(10) #Testing purposes only
        FFX_Xbox.menuB() #Cursor starts on item 2. Only occurs if opposite columns.
    else:
        while cursor < item2:
            FFX_Xbox.menuDown()
            cursor += 2
        #time.sleep(10) #Testing purposes only
        FFX_Xbox.menuB() #Cursor is now on item 2.
    
    time.sleep(0.4)
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()





def openGrid(character):
    while not FFX_memory.sGridActive():
        #print("Attempting to open Sphere Grid")
        if FFX_memory.userControl() and not FFX_memory.menuOpen():
            #print("Menu is not open at all")
            FFX_Xbox.tapY()
        elif FFX_memory.menuNumber() == 5: #Cursor on main menu
            #print("Main menu cursor")
            if FFX_memory.getMenuCursorPos() != 0:
                while FFX_memory.getMenuCursorPos() != 0:
                    FFX_Xbox.menuUp()
            FFX_Xbox.menuB()
            FFX_memory.waitFrames(1)
        elif FFX_memory.menuNumber() == 7: #Cursor selecting party member
            #print("Selecting party member")
            if FFX_memory.getMenu2CharNum() != character:
                while FFX_memory.getMenu2CharNum() != character:
                    FFX_Xbox.menuDown()
            FFX_Xbox.menuB()
            try:
                FFXC.set_neutral()
            except:
                FFXC = FFX_Xbox.controllerHandle()
                FFXC.set_neutral()
            FFX_memory.waitFrames(3)
