import time
import math
import FFX_Xbox
import FFX_Screen
import FFX_menuGrid
import FFX_Logs
import FFX_memory
import FFX_vars
import FFX_menu
gameVars = FFX_vars.varsHandle()

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
        FFX_memory.waitFrames(30 * 1)
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
            FFX_memory.waitFrames(30 * 0.25)
    print("Move command highlighted. Good to go.")

def awaitUse():
    print("Sphere Grid: Waiting for Use command to be highlighted")
    while FFX_memory.sGridActive() == False:
        print("The Sphere Grid isn't even open! Awaiting manual recovery.")
        FFX_memory.waitFrames(30 * 1)
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
            FFX_memory.waitFrames(30 * 0.25)
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


def openGrid(character):
    try:
        FFXC.set_neutral()
    except:
        FFXC = FFX_Xbox.controllerHandle()
        FFXC.set_neutral()
    while not FFX_memory.sGridActive():
        #print("Attempting to open Sphere Grid")
        if FFX_memory.userControl() and not FFX_memory.menuOpen():
         #   print("Menu is not open at all")
            FFX_Xbox.tapY()
        elif FFX_memory.menuNumber() == 5: #Cursor on main menu
          #  print("Main menu cursor")
            while FFX_memory.getMenuCursorPos() != 0:
                FFX_memory.menuDirection(FFX_memory.getMenuCursorPos(), 0, 11)
           # print("Done with menu cursor")
            while FFX_memory.menuNumber() == 5:
                FFX_Xbox.tapB()
        elif FFX_memory.menuNumber() == 7: #Cursor selecting party member
            print("Selecting party member")
            target_pos = FFX_memory.getCharacterIndexInMainMenu(character)
            while FFX_memory.getCharCursorPos() != target_pos:
                if FFX_memory.getStoryProgress() == 2528: #After B&Y, party size is evaluated weird.
                    FFX_memory.menuDirection(FFX_memory.getCharCursorPos(), target_pos, 7)
                elif FFX_memory.partySize() < 3:
                    FFX_Xbox.menuDown()
                else:
                    #FFX_memory.menuDirection(FFX_memory.getCharCursorPos(), target_pos, FFX_memory.partySize())
                    #Not working. Use this instead.
                    FFX_memory.menuDirection(FFX_memory.getCharCursorPos(), target_pos, 7)
            while FFX_memory.menuNumber() == 7:
                FFX_Xbox.menuB()
            try:
                FFXC.set_neutral()
            except:
                FFXC = FFX_Xbox.controllerHandle()
                FFXC.set_neutral()
    try:
        FFXC.set_neutral()
    except:
        FFXC = FFX_Xbox.controllerHandle()
        FFXC.set_neutral()

#------------------------------------------------------------
# Nemesis Control functions
def performNextGrid(limit:int=255):
    #Conditions to hard disregard further evaluations.
    if gameVars.nemCheckpointAP() == 0:
        return False
    if gameVars.nemCheckpointAP() > limit:
        return False
    
    #If the above checks are passed, check Tidus level and do sphere grid.
    if FFX_memory.getTidusSlvl() >= nextAPneeded(gameVars.nemCheckpointAP()):
        print("Attemping Nemesis Grid #", gameVars.nemCheckpointAP())
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
        elif gameVars.nemCheckpointAP() == 27:
            nemGridding27()
        else:
            print("----------------------------")
            print("End of sphere grid, no further grid logic programmed.")
            print("----------------------------")
            gameVars.setNemChecpointAP(gameVars.nemCheckpointAP() - 1) #Decrement
        gameVars.setNemChecpointAP(gameVars.nemCheckpointAP() + 1) #Increment
    
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
    if FFX_memory.getPower() < 4 or FFX_memory.getSpeed() < 4:
        gameVars.setNemChecpointAP(value=0)
        return
    #Requires X levels
    FFX_menu.autoSortItems()
    openGrid(character=0)
    FFX_menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    #FFX_menuGrid.selSphere('power','d','none') #HP sphere
    #FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('lv3','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridRight()
    gridRight()
    #FFX_menuGrid.moveAndUse()
    #FFX_menuGrid.selSphere('power','d','none')
    #FFX_menuGrid.useAndMove()
    gridRight()
    #FFX_menuGrid.moveAndUse()
    #FFX_menuGrid.selSphere('power','d','none')
    #FFX_menuGrid.useAndMove()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding2():
    #Requires 2 levels
    openGrid(character=0)
    FFX_menuGrid.moveFirst()
    gridRight()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding3():
    #Starts between the two accuracy nodes, top right of the grid.
    #Requires 13 levels to perform.
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    #FFX_menuGrid.selSphere('power','d','none')
    #FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridDown()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    #FFX_menuGrid.selSphere('hp','d','none')
    #FFX_menuGrid.useAndUseAgain()
    #FFX_menuGrid.selSphere('power','d','none')
    #FFX_menuGrid.useAndUseAgain()
    #FFX_menuGrid.selSphere('power','d','none')
    #FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding4():
    #Starts on created HP node, just north of Auron.
    #Requires 11 levels to perform.
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridLeft()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    #FFX_menuGrid.selSphere('power','d','none')
    #FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridDown()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','right')
    #FFX_menuGrid.useAndUseAgain()
    #FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding5():
    #Starts west of Auron.
    #Requires 11 levels to perform.
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','left')
    #FFX_menuGrid.useAndUseAgain()
    #FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','down')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding6():
    #Starts east of Auron, on an HP node in the right corner.
    #Requires 9 levels to perform.
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridLeft()
    gridLeft()
    gridDown()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('mana','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridLeft()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','left')
    #FFX_menuGrid.useAndUseAgain()
    #FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','right')
    #FFX_menuGrid.useAndUseAgain()
    #FFX_menuGrid.selSphere('power','d','none')
    if gameVars.endGameVersion() == 2:
        FFX_menuGrid.useAndUseAgain()
        FFX_menuGrid.selSphere('lv1','d','none')
    #FFX_menuGrid.useAndUseAgain()
    #FFX_menuGrid.selSphere('hp','d','none')
    #FFX_menuGrid.useAndUseAgain()
    #FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding7():
    #Starts in the center of the circle, near end of any% grid.
    #Requires 9 levels to perform.
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridRight()
    gridDown()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('mana','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','none')
    #FFX_menuGrid.useAndUseAgain()
    #FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    #FFX_menuGrid.useAndUseAgain()
    #FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding8():
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridDown()
    gridRight()
    gridRight()
    gridRight()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    gridLeft()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('lv1','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridUp()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding9(): #Ends near Wakka
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridDown()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    gridDown()
    gridDown()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridRight()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding10(): #Starts near Wakka
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('lv2','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridRight()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('lv2','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridDown()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('lv4','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('lv4','d','none')
    FFX_menuGrid.useAndMove()
    FFXC.set_movement(1,-1)
    FFX_memory.waitFrames(30)
    FFXC.set_movement(0,0)
    FFXC.set_neutral()
    FFX_memory.waitFrames(6)
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('lv4','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding11(): #Back from Ultima to Wakka's grid
    openGrid(0)
    FFX_menuGrid.moveFirst()
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
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('lv1','d','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding12(): #Through Kimahri's grid to Rikku's.
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridLeft()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridLeft()
    gridUp()
    gridUp()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('ability','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('ability','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding13(): #Start on the Steal command
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridRight()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','right')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding14():
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridLeft()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('mana','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('mana','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding15(): #Weird off-shoot with the three +1 strength nodes
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','right')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','right')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','left')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridDown()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding16():
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridUp()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridDown()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding17(): #Ends near Lulu
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridDown()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('mana','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding18(): #All the way back to Kimahri grid
    openGrid(0)
    FFX_menuGrid.moveFirst()
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
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding19():
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridUp()
    gridUp()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','left')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('lv1','d','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    gridUp()
    gridLeft()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding20(): #Starts next to Haste node
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    gridDown()
    FFX_menuGrid.moveAndUse() #Into Auron's grid
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding21(): #Auron's grid back to Tidus
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridLeft()
    gridUp()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    gridLeft()
    gridUp()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding22():
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridLeft()
    gridDown()
    gridDown()
    gridDown()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    gridUp()
    gridLeft()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridLeft()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('lv3','d','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding23():
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridRight()
    gridDown()
    gridDown()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding24():
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridLeft()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridLeft()
    gridUp()
    gridLeft()
    gridLeft()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridRight()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding25(): #End Tidus grid, Quick Hit
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridUp()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('speed','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('lv3','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridDown()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('ability','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('lv3','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def nemGridding26(): #Backtrack to Auto-life, or can go through Yuna's grid on refactor.
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    gridUp()
    gridRight()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('lv4','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridRight()
    gridUp()
    gridUp()
    gridRight()
    gridRight()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('lv4','d','none')
    FFX_menuGrid.useAndMove()
    gridLeft()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('ability','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def luluBribe():
    openGrid(5)
    FFX_menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    gridRight()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('ability','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def rikkuHaste():
    openGrid(character=6)
    
    FFX_menuGrid.moveFirst()
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
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('ability','d','aftersk')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def rikkuProvoke():
    openGrid(6)
    FFX_menuGrid.moveFirst()
    gridUp()
    gridUp()
    gridUp()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('ability','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()

def strBoost():
    openGrid(0)
    FFX_menuGrid.moveFirst()
    gridRight()
    gridRight()
    gridUp()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('strength','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('strength','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('strength','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndMove()
    gridDown()
    gridLeft()
    gridDown()
    gridDown()
    FFX_menuGrid.moveAndUse()
    FFX_menuGrid.selSphere('strength','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('strength','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('strength','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndUseAgain()
    FFX_menuGrid.selSphere('power','d','none')
    FFX_menuGrid.useAndQuit()
    FFX_memory.closeMenu()