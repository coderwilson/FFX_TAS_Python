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

def awaitMove_old():
    print("Sphere Grid: Waiting for Move command to be highlighted")
    complete = 0
    count = 1
    time.sleep(0.2)
    while complete == 0:
        time.sleep(0.1)
        count += 1
        if FFX_Screen.PixelTest(246,385,(255, 213, 0)):
            if count % 100 == 0:
                print("Confirm, sphere grid is open.")
            if FFX_Screen.PixelTest(177,505,(141, 141, 141)): #Use is highlighted
                FFX_Xbox.menuUp()
            elif FFX_Screen.PixelTestTol(373,765,(255, 255, 255),5): #Menu isn't open
                FFX_Xbox.menuB()
            elif FFX_Screen.PixelTestTol(503,457,(212, 212, 212),5): #Never finished moving
                FFX_Xbox.menuB()
            elif FFX_Screen.PixelTestTol(177,460,(153, 153, 153),2): #Move is highlighted
                complete = 1
        else:
            if count % 100 == 0:
                print("await Move")
                print("You're on the wrong screen for some reason.")
    print("Moving in the sphere grid")

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

def awaitUse_old():
    complete = 0
    count = 1
    print("Sphere Grid: Waiting for Use command to be highlighted")
    time.sleep(0.2)
    while complete == 0:
        count += 1
        if FFX_Screen.PixelTest(246,385,(255, 213, 0)):
            if count % 100 == 0:
                print("Confirm, sphere grid is open.")
            if FFX_Screen.PixelTest(177,505,(141, 141, 141)): #Use is highlighted
                complete = 1
            elif FFX_Screen.PixelTestTol(373,765,(255, 255, 255),5): #Menu isn't open
                FFX_Xbox.menuB()
            elif FFX_Screen.PixelTestTol(177,460,(153, 153, 153),5): #Move is highlighted
                FFX_Xbox.menuDown()
            elif FFX_Screen.PixelTestTol(503,457,(212, 212, 212),5): #Never finished moving
                FFX_Xbox.menuB()
        else:
            if count % 100 == 0:
                print("await use")
                print("You're on the wrong screen for some reason.")
    print("Using items, sphere grid")

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

def awaitQuitSG_old():
    complete = 0
    count = 1
    print("Sphere Grid: attempting to quit the grid")
    time.sleep(0.2)
    while complete == 0:
        count += 1
        if FFX_Screen.PixelTest(246,385,(255, 213, 0)):
            if count % 100 == 0:
                print("Confirm, sphere grid is open.")
            if FFX_Screen.PixelTest(177,505,(141, 141, 141)): #Use is highlighted
                FFX_Xbox.menuA()
            elif FFX_Screen.PixelTestTol(373,765,(255, 255, 255),5): #Menu isn't open
                FFX_Xbox.menuA()
            elif FFX_Screen.PixelTestTol(177,460,(153, 153, 153),5): #Move is highlighted
                FFX_Xbox.menuA()
            elif FFX_Screen.PixelTestTol(489,457,(212, 212, 212),5): #Ready to quit
                FFX_Xbox.menuB()
                complete = 1
        else:
            if count % 100 == 0:
                print("Quitting Grid")
                print("You aren't even in the grid for some reason.")
    print("Quitting sphere grid is complete.")

def moveFirst():
    print("First - moving")
    #time.sleep(0.8)
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuUp()
    awaitMove()
    #time.sleep(0.5)
    #FFX_Xbox.menuB()
    #time.sleep(0.1)

def useFirst():
    print("First - using sphere")
    #time.sleep(0.8)
    #FFX_Xbox.menuB()
    #time.sleep(0.05)
    #FFX_Xbox.menuDown()
    #time.sleep(0.05)
    awaitUse()
    #FFX_Xbox.menuB()
    #time.sleep(0.1)

def moveAndUse():
    FFX_Xbox.menuB()
    time.sleep(0.1)
    FFX_Xbox.menuB()
    awaitUse()
    #time.sleep(0.1)
    #FFX_Xbox.menuB()
    #time.sleep(0.1)

def useAndUseAgain():
    time.sleep(0.1)
    FFX_Xbox.menuB()
    #time.sleep(2.4)
    #FFX_Xbox.menuB()
    awaitUse()
    #time.sleep(0.1)
    #FFX_Xbox.menuB()
    #time.sleep(0.1)

def teleportAndUse():
    time.sleep(0.1)
    FFX_Xbox.menuB()
    #time.sleep(6)
    #FFX_Xbox.menuB()
    awaitUse()
    #time.sleep(0.1)
    #FFX_Xbox.menuB()
    #time.sleep(0.1)

def teleportAndMove():
    time.sleep(0.1)
    FFX_Xbox.menuB()
    #time.sleep(6)
    #FFX_Xbox.menuB()
    #time.sleep(0.2)
    #FFX_Xbox.menuUp()
    #time.sleep(0.1)
    awaitMove()
    #time.sleep(0.1)
    #FFX_Xbox.menuB()
    #time.sleep(0.1)

def useAndMove():
    time.sleep(0.1)
    FFX_Xbox.menuB()
    #time.sleep(2.4)
    #FFX_Xbox.menuB()
    awaitUse()
    #time.sleep(0.1)
    #FFX_Xbox.menuUp()
    #time.sleep(0.1)
    #FFX_Xbox.menuB()
    #time.sleep(0.2)

def useAndQuit():
    time.sleep(0.1)
    FFX_Xbox.menuB()
    awaitQuitSG()
    time.sleep(0.3)

def useShiftMove(direction):
    direction = direction.lower()
    time.sleep(0.4)
    FFX_Xbox.menuB()
    time.sleep(2.4)
    if direction == 'left':
        FFX_Xbox.shoulderLeft()
    if direction == 'l2':
        FFX_Xbox.shoulderLeft()
        FFX_Xbox.shoulderLeft()
    if direction == 'l3':
        FFX_Xbox.shoulderLeft()
        FFX_Xbox.shoulderLeft()
        FFX_Xbox.shoulderLeft()
    if direction == 'right':
        FFX_Xbox.shoulderRight()
    if direction == 'r2':
        FFX_Xbox.shoulderRight()
        FFX_Xbox.shoulderRight()
    if direction == 'r3':
        FFX_Xbox.shoulderRight()
        FFX_Xbox.shoulderRight()
        FFX_Xbox.shoulderRight()
    time.sleep(0.1)
    FFX_Xbox.menuB()
    time.sleep(0.4)
    FFX_Xbox.menuUp()
    time.sleep(0.1)
    FFX_Xbox.menuB()
    time.sleep(0.1)

def useShiftUse(direction):
    direction = direction.lower()
    time.sleep(0.4)
    FFX_Xbox.menuB()
    time.sleep(2.4)
    if direction == 'left':
        FFX_Xbox.shoulderLeft()
    if direction == 'l2':
        FFX_Xbox.shoulderLeft()
        FFX_Xbox.shoulderLeft()
    if direction == 'l3':
        FFX_Xbox.shoulderLeft()
        FFX_Xbox.shoulderLeft()
        FFX_Xbox.shoulderLeft()
    if direction == 'right':
        FFX_Xbox.shoulderRight()
    if direction == 'r2':
        FFX_Xbox.shoulderRight()
        FFX_Xbox.shoulderRight()
    if direction == 'r3':
        FFX_Xbox.shoulderRight()
        FFX_Xbox.shoulderRight()
        FFX_Xbox.shoulderRight()
    time.sleep(0.1)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuDown()
    time.sleep(0.1)
    FFX_Xbox.menuB()
    time.sleep(0.1)

def moveShiftUse(direction):
    direction = direction.lower()
    time.sleep(0.4)
    FFX_Xbox.menuB()
    FFX_Screen.awaitPixel(178,548,(143, 143, 143))
    FFX_Xbox.menuB()
    time.sleep(0.2)
    if direction == 'left':
        FFX_Xbox.shoulderLeft()
    if direction == 'l2':
        FFX_Xbox.shoulderLeft()
        FFX_Xbox.shoulderLeft()
    if direction == 'l3':
        FFX_Xbox.shoulderLeft()
        FFX_Xbox.shoulderLeft()
        FFX_Xbox.shoulderLeft()
    if direction == 'right':
        FFX_Xbox.shoulderRight()
    if direction == 'r2':
        FFX_Xbox.shoulderRight()
        FFX_Xbox.shoulderRight()
    if direction == 'r3':
        FFX_Xbox.shoulderRight()
        FFX_Xbox.shoulderRight()
        FFX_Xbox.shoulderRight()
    time.sleep(0.1)
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuDown()
    time.sleep(0.1)
    FFX_Xbox.menuB()
    time.sleep(0.1)


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
    FFX_memory.openMenu()
    FFX_memory.waitFrames(30)
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuB()
    #time.sleep(0.2)
    #FFX_Xbox.menuA()
    #FFX_Xbox.menuRight()
    #FFX_Xbox.menuB()
    #time.sleep(0.2)
    #FFX_Xbox.menuRight()
    #FFX_Xbox.menuB() #Autosort items
    
    #FFX_Xbox.menuA()
    #FFX_Xbox.menuA()
    #FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_memory.waitFrames(10)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Sphere grid with Tidus
    FFX_memory.waitFrames(10)
    
    #Move to the Def node just to the left
    print("Sphere grid on Tidus, learn Cheer and Str +1")
    FFX_menuGrid.useShiftRight('tidus') #Shift to Rikku
    FFX_menuGrid.moveFirst()
    gridUp()
    gridUp()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    
    #Activate Str and Cheeer nodes
    FFX_menuGrid.selSphere('power','d','left')
    useAndUseAgain() #Str +1 node
    FFX_menuGrid.selSphere('ability','d','none') # Cheer
    FFX_Xbox.menuB()
    useAndQuit()
    FFX_Xbox.menuA()

def Geneaux():
    FFX_memory.openMenu()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    
    FFX_menuGrid.moveFirst()
    gridLeft()
    #gridLeft()
    #gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    #FFX_menuGrid.useAndUseAgain()
    #FFX_menuGrid.selSphere('ability','d','none') #Flee
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def LucaOaka(): #unused
    FFX_memory.openMenu()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.3)
    FFX_Xbox.menuA()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    time.sleep(0.3)
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    FFX_memory.closeMenu()

def LucaWorkers():
    FFX_memory.openMenu()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Sphere grid on Tidus
    
    FFX_menuGrid.useShiftRight('Tidus')
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
    useAndUseAgain()
    FFX_menuGrid.selSphere('mana','d','none')
    if earlyHaste == 1:
        useAndUseAgain()
        FFX_menuGrid.selSphere('ability','d','none') # Haste
        
    useAndQuit()
    FFX_memory.closeMenu()
    return earlyHaste

def lateHaste(): #Now unused
    FFX_memory.openMenu()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_menuGrid.useShiftRight('tidus')
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
    FFX_memory.openMenu()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Sphere grid on Wakka
    FFX_menuGrid.useShiftRight('wakka')
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
            FFX_memory.openMenu()
            FFX_Xbox.menuB()
            FFX_Xbox.menuDown()
            FFX_Xbox.menuB()
            
            FFX_menuGrid.useShiftRight('wakka')
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
    FFX_memory.openMenu()
    FFX_Xbox.menuB()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_menuGrid.useShiftRight('yuna')
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
    FFX_memory.openMenu()
    FFX_Xbox.menuB()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    
    FFX_menuGrid.useShiftRight('Yuna')
    FFX_menuGrid.moveFirst()
    gridLeft()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('mana','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    
    FFX_menuGrid.useShiftLeft('Kimahri') #Sphere grid on Kimahri
    FFX_Xbox.menuB()
    time.sleep(0.5)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    while FFX_Screen.PixelTestTol(804,296,(94, 23, 68),5):
        FFX_menuGrid.gridRight()
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
    time.sleep(0.2)
    FFX_Xbox.menuA()
    time.sleep(0.2)
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    
    #Wakka's weapon
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Equip
    wakkaPos = FFX_memory.getCharFormationSlot(4)
    if FFX_memory.getCharCursorPos() != wakkaPos:
        while FFX_memory.getCharCursorPos() != wakkaPos:
            FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Wakka
    time.sleep(0.3)
    FFX_Xbox.menuB() #Weapon
    time.sleep(0.15)
    FFX_Xbox.menuB() #Back to default.
    
    FFX_memory.closeMenu()
    FFX_memory.fullPartyFormat('battleSite')

def battleSiteOaka1_old():
    print("Not yet thanks")
    FFX_Xbox.menuB()
    time.sleep(10) #Dial this in later
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Items
    time.sleep(1)
    
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB() #Sell
    
    itemOrder = FFX_memory.getItemsOrder()
    itemCursor = 1
    while itemOrder[itemCursor] != 6: #Don't sell anything Phoenix Down or after.
        if itemOrder[itemCursor] != 3: #Sell all except for Mega Potions
            FFX_Xbox.menuB()
            FFX_Xbox.menuUp()
            if FFX_memory.getItemCountSlot(itemCursor) > 10:
                FFX_Xbox.menuUp()
            FFX_Xbox.menuB() #Sell this item
        if itemOrder[itemCursor + 1] == 6:
            print("Done with selling items.")
        elif itemCursor % 2 == 1:
            FFX_Xbox.menuRight()
        else:
            FFX_Xbox.menuLeft()
            FFX_Xbox.menuDown()
        itemCursor += 1
    
    FFX_Xbox.menuA()
    FFX_Xbox.menuA() #Exit items menu

def battleSiteOaka1():
    print("Not yet thanks")
    time.sleep(1.7)
    FFX_Xbox.menuB()
    time.sleep(4)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Items
    time.sleep(1)
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
    FFX_Xbox.clickToPixel(676,520,(196,196,196))
    time.sleep(0.2)
    FFX_Xbox.menuB()
    time.sleep(1)
    
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
    
    while not ( FFX_Screen.PixelTest(800,830,(132, 130, 167)) and FFX_Screen.PixelTest(256,803,(154, 154, 154))):
        FFX_Xbox.menuDown()
        time.sleep(0.2)
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
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    
    #Re-sort items - should be Mega Potions first slot, followed by Phoenix Downs
    FFX_memory.openMenu()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuA()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    time.sleep(0.2)
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    
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
    FFX_memory.openMenu()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    
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
    FFX_Screen.awaitMap1()
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
    autoSortItems('n')
    
    FFX_Xbox.menuB() #Talk to O'aka again
    time.sleep(0.7)
    FFX_Xbox.menuB() #Talk to O'aka again
    FFX_Screen.awaitPixel(650,466,(154, 154, 154))
    time.sleep(0.1)
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuB() #Items
    #FFX_Screen.awaitPixel(365,152,(154, 154, 154))
    #time.sleep(0.1)
    #FFX_Xbox.menuRight()
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuDown()
    
    #pos = 3
    #print("Selling everything short of position ", itemScan[5])
    #while pos < itemScan[7]: #Sell any items not in the list of "need to have" items.
    #    if not (pos in itemScan):
    #        FFX_Xbox.menuB()
    #        FFX_Xbox.menuUp()
    #        FFX_Xbox.menuUp()
    #        FFX_Xbox.menuB()
    #    if itemScan[7] - pos != 1:
    #        if pos % 2 == 1:
    #            FFX_Xbox.menuRight()
    #        else:
    #            FFX_Xbox.menuLeft()
    #            FFX_Xbox.menuDown()
    #    pos += 1
    
    #itemOrder = FFX_memory.getItemsOrder()
    #itemCursor = 1
    #while itemOrder[itemCursor] != 70: #Don't sell anything Phoenix Down or after.
    #    if not (itemOrder[itemCursor] in [27,30,32,24,35,56,57,3,6,7,8]): #Sell all except for Mega Potions
    #        FFX_Xbox.menuB()
    #        FFX_Xbox.menuUp()
    #        if FFX_memory.getItemCountSlot(itemCursor) > 11:
    #            FFX_Xbox.menuUp()
    #        FFX_Xbox.menuB() #Sell all of this item, up to 21
    #    if itemOrder[itemCursor + 1] == 6:
    #        print("Done with selling items.")
    #    elif itemCursor % 2 == 1:
    #        FFX_Xbox.menuRight()
    #    else:
    #        FFX_Xbox.menuLeft()
    #        FFX_Xbox.menuDown()
    #    itemCursor += 1
    #0
    #FFX_memory.closeMenu() #Leave the selling items menu
    
    #FFX_memory.openMenu()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuB()
    #time.sleep(0.2)
    #FFX_Xbox.menuA()
    #FFX_Xbox.menuRight()
    #FFX_Xbox.menuB()
    #time.sleep(0.2)
    #FFX_Xbox.menuRight()
    #FFX_Xbox.menuB()
    
    #FFX_Xbox.menuLeft()
    #FFX_Xbox.menuB()
    
    #Sort red items to the top
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuDown()
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuRight()
    #FFX_Xbox.menuB() #Flip lightning marbles and bomb cores.
    
    #FFX_memory.closeMenu()
    
    #time.sleep(0.5)
    
    if FFX_memory.getGilvalue() < 9100:
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
    
def macManualSort_old():
    #Manual sorting in Macalania. No longer used here. May refactor later to a different slot.
    FFX_Xbox.menuDown()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuB()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB() #Mana Sphere to 4, Lightning Marble to 11
    
    FFX_Xbox.menuDown()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB() #Speed sphere to 5, Fish Scale to 12
    
    FFX_Xbox.menuDown()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuB()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB() #Ability Sphere to 6, Arctic Wind to 13
    
    FFX_Xbox.menuDown()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuB()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuB() #Fix Lunar and Light.
    FFX_Xbox.menuB()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuB() #Fix Bomb Core and Lightning Marble
    FFX_Xbox.menuB()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuB() #Fix Fish Scale and Arctic Wind
    
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Lunar to bottom
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuRight()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Light to bottom
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_Xbox.menuLeft()
    FFX_Xbox.menuB()
    
    FFX_memory.closeMenu()
    
    #time.sleep(0.5)
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
    FFX_memory.openMenu()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Sphere grid Kimahri
    FFX_menuGrid.useShiftRight('kimahri')
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
    FFX_menuGrid.useShiftRight('rikku') #Shift to Rikku
    FFX_menuGrid.moveFirst()
    
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','u','none')
    
    FFX_menuGrid.useShiftRight('yuna') #And last is Yuna
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
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','u','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
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
    FFX_memory.openMenu()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB() #Sphere grid Tidus
    
    FFX_menuGrid.useShiftRight('tidus')
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
    FFX_memory.openMenu()
    FFX_Xbox.menuB()  # Sphere grid on Tidus
    FFX_Xbox.menuB()  # Sphere grid on Tidus

    FFX_menuGrid.useShiftRight('Tidus')
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
    currentmenuposition = equipSonicSteel_New(11)
    #currentmenuposition = FFX_memory.fullPartyFormat_New('macalaniaescape',11)
    FFX_memory.closeMenu()

def homeGrid():
    FFX_memory.openMenu()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    FFX_menuGrid.useShiftRight('Tidus')
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

def equipSonicSteel_New(menusize):
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
    while not FFX_Screen.PixelTestTol(1058, 517, (220, 220, 220), 5):
        FFX_Xbox.menuDown()
        time.sleep(0.05)
    FFX_Xbox.menuB()
    time.sleep(0.1)
    FFX_Xbox.menuA()

    return 5

def equipSonicSteel():
    print("Equipping Sonic Steel")
    FFX_memory.awaitControl()
    FFX_memory.openMenu()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuB()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuB() #Formation fixed
    #FFX_Xbox.menuA()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp()
    #FFX_Xbox.menuUp() #Formation section is replaced.

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
    FFX_memory.openMenu()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Sphere grid on Auron
    
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
    FFX_memory.openMenu()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Sphere grid on Yuna
    
    FFX_menuGrid.useFirst()
    FFX_menuGrid.selSphere('tele','d','up2')
    FFX_menuGrid.useAndUseAgain()
    
    FFX_menuGrid.selSphere('power','u','none') #Str
    useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none') #Str
    useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none') #Def +3
    
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    useAndUseAgain()
    FFX_menuGrid.selSphere('power','u','none')
    useAndUseAgain()
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
    FFX_memory.openMenu()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Sphere grid on Yuna
    
    FFX_menuGrid.useFirst()
    FFX_menuGrid.selSphere('tele','d','none')
    gridLeft()
    FFX_menuGrid.useAndUseAgain()
    
    FFX_menuGrid.selSphere('power','u','none')
    useAndUseAgain()
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
    FFX_memory.openMenu()
    FFX_Xbox.menuB()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_menuGrid.useShiftRight('yuna')
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
    FFX_memory.openMenu()
    time.sleep(0.2)
    FFX_Xbox.menuB()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    
    FFX_menuGrid.moveShiftRight('Lulu')
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
    FFX_memory.openMenu()
    FFX_Xbox.menuB()
    FFX_Xbox.menuB()
    
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
    pattern = 0
    FFX_memory.openMenu()
    
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    
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
    FFX_memory.openMenu()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_menuGrid.useShiftLeft('Yuna')
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
    FFX_memory.openMenu()
    FFX_Xbox.menuB()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    FFX_menuGrid.useShiftLeft('Yuna')
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
    print("Sphere grid after Sanctuary Keeper fight")
    FFX_memory.openMenu()
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    
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



