import xbox
import menuGrid
import memory
import vars
import menu
gameVars = vars.varsHandle()

FFXC = xbox.controllerHandle()

def gridUp():
    menuGrid.gridUp()

def gridDown():
    menuGrid.gridDown()

def gridLeft():
    menuGrid.gridLeft()

def gridRight():
    menuGrid.gridRight()

def awaitMove():
    print("Sphere Grid: Waiting for Move command to be highlighted")
    while memory.sGridActive() == False:
        print("The Sphere Grid isn't even open! Awaiting manual recovery.")
        memory.waitFrames(30 * 1)
    complete = False
    while complete == False:
        menuVal = memory.sGridMenu()
        if menuVal == 11 or menuVal == 255:
            xbox.menuB()
        elif menuVal == 7:
            cursorLoc = memory.cursorLocation()
            if cursorLoc[0] == 51 or cursorLoc[1] == 243:
                xbox.menuUp()
            xbox.menuB()
            complete = True
            memory.waitFrames(30 * 0.25)
    print("Move command highlighted. Good to go.")

def awaitUse():
    print("Sphere Grid: Waiting for Use command to be highlighted")
    while memory.sGridActive() == False:
        print("The Sphere Grid isn't even open! Awaiting manual recovery.")
        memory.waitFrames(30 * 1)
    complete = False
    while complete == False:
        menuVal = memory.sGridMenu()
        print("Menu value: ", menuVal)
        if menuVal == 7:
            cursorLoc = memory.cursorLocation()
            if cursorLoc[0] == 102 or cursorLoc[1] == 14:
                xbox.menuDown()
            xbox.menuB()
            complete = True
            memory.waitFrames(30 * 0.25)
        else:
            xbox.menuB()
    print("Use command highlighted. Good to go.")

def awaitQuitSG():
    print("Sphere Grid: attempting to quit")
    while memory.sGridActive():
        menuVal = memory.sGridMenu()
        if menuVal == 255:
            xbox.menuA()
        elif menuVal == 11:
            xbox.menuB()
        else:
            xbox.menuA()
    print("Back to the main menu")


def openGrid(character):
    try:
        FFXC.set_neutral()
    except:
        FFXC = xbox.controllerHandle()
        FFXC.set_neutral()
    while not memory.sGridActive():
        #print("Attempting to open Sphere Grid")
        if memory.userControl() and not memory.menuOpen():
         #   print("Menu is not open at all")
            xbox.tapY()
        elif memory.menuNumber() == 5: #Cursor on main menu
          #  print("Main menu cursor")
            while memory.getMenuCursorPos() != 0:
                memory.menuDirection(memory.getMenuCursorPos(), 0, 11)
           # print("Done with menu cursor")
            while memory.menuNumber() == 5:
                xbox.tapB()
        elif memory.menuNumber() == 7: #Cursor selecting party member
            print("Selecting party member")
            target_pos = memory.getCharacterIndexInMainMenu(character)
            while memory.getCharCursorPos() != target_pos:
                if memory.getStoryProgress() == 2528: #After B&Y, party size is evaluated weird.
                    memory.menuDirection(memory.getCharCursorPos(), target_pos, 7)
                elif memory.partySize() < 3:
                    xbox.menuDown()
                else:
                    # memory.menuDirection(memory.getCharCursorPos(), target_pos, memory.partySize())
                    # Not working. Use this instead.
                    memory.menuDirection(memory.getCharCursorPos(), target_pos, 7)
            while memory.menuNumber() == 7:
                xbox.menuB()
            try:
                FFXC.set_neutral()
            except:
                FFXC = xbox.controllerHandle()
                FFXC.set_neutral()
    try:
        FFXC.set_neutral()
    except:
        FFXC = xbox.controllerHandle()
        FFXC.set_neutral()

#------------------------------------------------------------
# Nemesis Control functions
def performNextGrid(limit:int=255):
    #Conditions to hard disregard further evaluations.
    print("###   Next Version: ", gameVars.nemCheckpointAP())
    print("### Current S.lvls: ", memory.getTidusSlvl())
    print("### Needed  S.lvls: ", nextAPneeded(gameVars.nemCheckpointAP()))
    if limit != 255:
        print("###          Limit: ", limit)
    if gameVars.nemCheckpointAP() == 0:
        print("###Something wrong: ", gameVars.nemCheckpointAP())
        return False
    if gameVars.nemCheckpointAP() > limit:
        print("### Limit exceeded: ", limit)
        return False
    
    #If the above checks are passed, check Tidus level and do sphere grid.
    if memory.getTidusSlvl() >= nextAPneeded(gameVars.nemCheckpointAP()):
        print("##### Attemping Nemesis Grid #", gameVars.nemCheckpointAP())
        if gameVars.nemCheckpointAP() == 1:
            nemGridding1()
        elif gameVars.nemCheckpointAP() == 2:
            nemGridding2()
        elif gameVars.nemCheckpointAP() == 3:
            nemGridding3()
        elif gameVars.nemCheckpointAP() == 4:
            nemGridding4()
        elif gameVars.nemCheckpointAP() == 5:
            nemGridding5()
        elif gameVars.nemCheckpointAP() == 6:
            nemGridding6()
        elif gameVars.nemCheckpointAP() == 7:
            nemGridding7()
        elif gameVars.nemCheckpointAP() == 8:
            nemGridding8()
        elif gameVars.nemCheckpointAP() == 9:
            nemGridding9()
        elif gameVars.nemCheckpointAP() == 10:
            nemGridding10()
        elif gameVars.nemCheckpointAP() == 11:
            nemGridding11()
        elif gameVars.nemCheckpointAP() == 12:
            nemGridding12()
        elif gameVars.nemCheckpointAP() == 13:
            nemGridding13()
        elif gameVars.nemCheckpointAP() == 14:
            nemGridding14()
        elif gameVars.nemCheckpointAP() == 15:
            nemGridding15()
        elif gameVars.nemCheckpointAP() == 16:
            nemGridding16()
        elif gameVars.nemCheckpointAP() == 17:
            nemGridding17()
        elif gameVars.nemCheckpointAP() == 18:
            nemGridding18()
        elif gameVars.nemCheckpointAP() == 19:
            nemGridding19()
        elif gameVars.nemCheckpointAP() == 20:
            nemGridding20()
        elif gameVars.nemCheckpointAP() == 21:
            nemGridding21()
        elif gameVars.nemCheckpointAP() == 22:
            nemGridding22()
        elif gameVars.nemCheckpointAP() == 23:
            nemGridding23()
        elif gameVars.nemCheckpointAP() == 24:
            nemGridding24()
        elif gameVars.nemCheckpointAP() == 25:
            nemGridding25()
        elif gameVars.nemCheckpointAP() == 26:
            nemGridding26()
        else:
            print("----------------------------")
            print("End of sphere grid, no further grid logic programmed.")
            print("----------------------------")
            gameVars.setNemCheckpointAP(gameVars.nemCheckpointAP() - 1)  # Decrement
        gameVars.setNemCheckpointAP(gameVars.nemCheckpointAP() + 1)  # Increment
    # else:
        # print("###Not enough Slvl:", memory.getTidusSlvl() - nextAPneeded(gameVars.nemCheckpointAP()))
        

def nextAPneeded(checkpoint):
    if checkpoint == 1:
        return 13
    if checkpoint == 2:
        return 2
    if checkpoint == 3:
        return 13
    if checkpoint == 4:
        return 11
    if checkpoint == 5:
        return 11
    if checkpoint == 6:
        return 9
    if checkpoint == 7:
        return 9
    if checkpoint == 8:
        return 21
    if checkpoint == 9:
        return 22
    if checkpoint == 10:
        return 18
    if checkpoint == 11:
        return 14
    if checkpoint == 12:
        return 18
    if checkpoint == 13:
        return 4
    if checkpoint == 14:
        return 17
    if checkpoint == 15:
        return 18
    if checkpoint == 16:
        return 10
    if checkpoint == 17:
        return 25
    if checkpoint == 18:
        return 26
    if checkpoint == 19:
        return 17
    if checkpoint == 20:
        return 19
    if checkpoint == 21:
        return 19
    if checkpoint == 22:
        return 24
    if checkpoint == 23:
        return 11
    if checkpoint == 24:
        return 22
    if checkpoint == 25:
        return 22
    if checkpoint == 26:
        return 42
    return 100 #If no further grids are possible, continue indefinitely.

#------------------------------------------------------------
# Nemesis menus

def nemGridding1():
    if memory.getPower() < 4 or memory.getSpeed() < 4:
        gameVars.setNemCheckpointAP(value=0)
        return
    #Requires X levels
    menu.autoSortItems()
    openGrid(character=0)
    menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    menuGrid.moveAndUse()
    # menuGrid.selSphere('power','none') #HP sphere
    # menuGrid.useAndUseAgain()
    menuGrid.selSphere('lv3','none')
    menuGrid.useAndMove()
    gridRight()
    gridRight()
    gridRight()
    # menuGrid.moveAndUse()
    # menuGrid.selSphere('power','none')
    # menuGrid.useAndMove()
    gridRight()
    # menuGrid.moveAndUse()
    # menuGrid.selSphere('power','none')
    # menuGrid.useAndMove()
    gridRight()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding2():
    #Requires 2 levels
    openGrid(character=0)
    menuGrid.moveFirst()
    gridRight()
    gridUp()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding3():
    #Starts between the two accuracy nodes, top right of the grid.
    #Requires 13 levels to perform.
    openGrid(0)
    menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    gridDown()
    gridDown()
    menuGrid.moveAndUse()
    # menuGrid.selSphere('power','none')
    # menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridDown()
    gridLeft()
    menuGrid.moveAndUse()
    # menuGrid.selSphere('hp','none')
    # menuGrid.useAndUseAgain()
    # menuGrid.selSphere('power','none')
    # menuGrid.useAndUseAgain()
    # menuGrid.selSphere('power','none')
    # menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding4():
    #Starts on created HP node, just north of Auron.
    #Requires 11 levels to perform.
    openGrid(0)
    menuGrid.moveFirst()
    gridLeft()
    gridLeft()
    menuGrid.moveAndUse()
    # menuGrid.selSphere('power','none')
    # menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridLeft()
    gridDown()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','right')
    # menuGrid.useAndUseAgain()
    # menuGrid.selSphere('power','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding5():
    #Starts west of Auron.
    #Requires 11 levels to perform.
    openGrid(0)
    menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','left')
    # menuGrid.useAndUseAgain()
    # menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridUp()
    gridRight()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','down')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding6():
    #Starts east of Auron, on an HP node in the right corner.
    #Requires 9 levels to perform.
    openGrid(0)
    menuGrid.moveFirst()
    gridLeft()
    gridLeft()
    gridDown()
    gridDown()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('mana','none')
    menuGrid.useAndMove()
    gridDown()
    gridLeft()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','left')
    # menuGrid.useAndUseAgain()
    # menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridDown()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','right')
    # menuGrid.useAndUseAgain()
    # menuGrid.selSphere('power','none')
    if gameVars.endGameVersion() in [1,2]:
        menuGrid.useAndUseAgain()
        menuGrid.selSphere('lv1','none')
    # menuGrid.useAndUseAgain()
    # menuGrid.selSphere('hp','none')
    # menuGrid.useAndUseAgain()
    # menuGrid.selSphere('power','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding7():
    #Starts in the center of the circle, near end of any% grid.
    #Requires 9 levels to perform.
    openGrid(0)
    menuGrid.moveFirst()
    gridRight()
    gridDown()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('mana','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','none')
    # menuGrid.useAndUseAgain()
    # menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridRight()
    gridDown()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    # menuGrid.useAndUseAgain()
    # menuGrid.selSphere('power','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding8():
    openGrid(0)
    menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridDown()
    gridRight()
    gridRight()
    gridRight()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridUp()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridUp()
    gridUp()
    gridLeft()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('lv1','none')
    menuGrid.useAndMove()
    gridRight()
    gridUp()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding9(): #Ends near Wakka
    openGrid(0)
    menuGrid.moveFirst()
    gridDown()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    gridDown()
    gridDown()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridDown()
    gridRight()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridDown()
    gridRight()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding10(): #Starts near Wakka
    openGrid(0)
    menuGrid.moveFirst()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('lv2','none')
    menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridRight()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('lv2','none')
    menuGrid.useAndMove()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridRight()
    gridDown()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridLeft()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('lv4','none')
    menuGrid.useAndMove()
    gridDown()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('lv4','none')
    menuGrid.useAndMove()
    FFXC.set_movement(1,-1)
    memory.waitFrames(30)
    FFXC.set_movement(0,0)
    FFXC.set_neutral()
    memory.waitFrames(6)
    menuGrid.moveAndUse()
    menuGrid.selSphere('lv4','none')
    menuGrid.useAndMove()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding11(): #Back from Ultima to Wakka's grid
    openGrid(0)
    menuGrid.moveFirst()
    gridLeft()
    gridUp()
    gridUp()
    gridUp()
    gridLeft()
    gridUp()
    gridUp()
    gridLeft()
    gridUp()
    gridUp()
    gridUp()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('lv1','none')
    menuGrid.useAndMove()
    gridUp()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding12(): #Through Kimahri's grid to Rikku's.
    openGrid(0)
    menuGrid.moveFirst()
    gridLeft()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridLeft()
    gridUp()
    gridUp()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('ability','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('ability','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding13(): #Start on the Steal command
    openGrid(0)
    menuGrid.moveFirst()
    gridRight()
    gridDown()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','right')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding14():
    openGrid(0)
    menuGrid.moveFirst()
    gridLeft()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('mana','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('mana','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding15(): #Weird off-shoot with the three +1 strength nodes
    openGrid(0)
    menuGrid.moveFirst()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridRight()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','right')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','right')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','left')
    menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridDown()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridRight()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding16():
    openGrid(0)
    menuGrid.moveFirst()
    gridUp()
    gridUp()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridDown()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding17(): #Ends near Lulu
    openGrid(0)
    menuGrid.moveFirst()
    gridDown()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('mana','none')
    menuGrid.useAndMove()
    gridDown()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridRight()
    gridDown()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding18(): #All the way back to Kimahri grid
    openGrid(0)
    menuGrid.moveFirst()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding19():
    openGrid(0)
    menuGrid.moveFirst()
    gridUp()
    gridUp()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','left')
    menuGrid.useAndMove()
    gridRight()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('lv1','none')
    menuGrid.useAndMove()
    gridUp()
    gridUp()
    gridUp()
    gridLeft()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridRight()
    gridRight()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding20(): #Starts next to Haste node
    openGrid(0)
    menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    gridDown()
    menuGrid.moveAndUse() #Into Auron's grid
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridRight()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding21(): #Auron's grid back to Tidus
    openGrid(0)
    menuGrid.moveFirst()
    gridLeft()
    gridUp()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    gridUp()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding22():
    openGrid(0)
    menuGrid.moveFirst()
    gridLeft()
    gridDown()
    gridDown()
    gridDown()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridUp()
    gridUp()
    gridUp()
    gridLeft()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridLeft()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridDown()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('lv3','none')
    menuGrid.useAndMove()
    gridUp()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding23():
    openGrid(0)
    menuGrid.moveFirst()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridDown()
    gridRight()
    gridDown()
    gridDown()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding24():
    openGrid(0)
    menuGrid.moveFirst()
    gridLeft()
    gridDown()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridUp()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridUp()
    gridLeft()
    gridLeft()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridRight()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding25(): #End Tidus grid, Quick Hit
    openGrid(0)
    menuGrid.moveFirst()
    gridUp()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndMove()
    gridDown()
    gridRight()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('speed','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('lv3','none')
    menuGrid.useAndMove()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridLeft()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('ability','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('lv3','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def nemGridding26(): #Backtrack to Auto-life, or can go through Yuna's grid on refactor.
    openGrid(0)
    menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    gridUp()
    gridRight()
    gridUp()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('lv4','none')
    menuGrid.useAndMove()
    gridDown()
    gridRight()
    gridUp()
    gridUp()
    gridRight()
    gridRight()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('power','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridDown()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('lv4','none')
    menuGrid.useAndMove()
    gridLeft()
    menuGrid.moveAndUse()
    menuGrid.selSphere('ability','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def luluBribe():
    openGrid(5)
    menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    menuGrid.moveAndUse()
    menuGrid.selSphere('ability','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def rikkuHaste():
    openGrid(character=6)
    
    menuGrid.moveFirst()
    if gameVars.endGameVersion() == 3:
        gridUp()
        gridUp()
        gridRight()
        gridUp()
        gridUp()
        gridUp()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    gridRight()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    gridLeft()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('ability','aftersk')
    menuGrid.useAndQuit()
    memory.closeMenu()

def rikkuProvoke():
    openGrid(6)
    menuGrid.moveFirst()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('ability','none')
    menuGrid.useAndQuit()
    memory.closeMenu()

def strBoost():
    openGrid(0)
    menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridUp()
    menuGrid.moveAndUse()
    menuGrid.selSphere('strength','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('strength','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('strength','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','none')
    menuGrid.useAndMove()
    gridDown()
    gridLeft()
    gridDown()
    gridDown()
    menuGrid.moveAndUse()
    menuGrid.selSphere('strength','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('strength','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('strength','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','none')
    menuGrid.useAndUseAgain()
    menuGrid.selSphere('power','none')
    menuGrid.useAndQuit()
    memory.closeMenu()