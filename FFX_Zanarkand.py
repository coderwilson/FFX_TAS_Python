import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory
import FFX_targetPathing
import FFX_vars
gameVars = FFX_vars.varsHandle()

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC
 
def arrival():
    FFX_memory.awaitControl()
    #Starts from the map just after the fireplace chat.
    FFX_memory.fullPartyFormat('kimahri')
    
    print("Outdoor Zanarkand pathing section")
    while FFX_memory.getMap() != 225:
        if FFX_memory.userControl():
            if FFX_memory.getCoords()[1] > -52:
                FFX_targetPathing.setMovement([103,-54])
            elif FFX_memory.getCoords()[0] < 172:
                FFX_targetPathing.setMovement([176,-118])
            else:
                FFXC.set_movement(-1, 1)
        else:
            FFXC.set_neutral()
    
    fortuneSlot = FFX_memory.getItemSlot(74)
    if fortuneSlot == 255:
        fortuneCount = 0
    else:
        fortuneCount = FFX_memory.getItemCountSlot(fortuneSlot)
    
    checkpoint = 0
    while FFX_memory.getMap() != 314:
        if FFX_memory.userControl():
            if checkpoint == 4: #First chest
                fortuneSlot = FFX_memory.getItemSlot(74)
                if fortuneSlot == 255:
                    fortuneCount = 0
                    FFXC.set_movement(-1, 1)
                    FFX_Xbox.tapB()
                else:
                    if FFX_memory.getItemCountSlot(fortuneSlot) > fortuneCount:
                        checkpoint += 1
                        FFX_memory.clickToControl()
                    else:
                        FFXC.set_movement(-1, 1)
                        FFX_Xbox.tapB()
            elif FFX_targetPathing.setMovement(FFX_targetPathing.zanarkandOutdoors(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_Screen.BattleScreen():
                FFX_Battle.fleeAll()
            elif FFX_memory.diagSkipPossible() and not FFX_memory.battleActive():
                FFX_Xbox.tapB()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
    
    #Outside the dome
    print("Now approaching the Blitz dome.")
    print("Close observation will reveal this is the same blitz dome")
    print("as the one from the opening of the game.")
    while FFX_memory.getMap() != 222:
        FFXC.set_movement(0, 1)
        FFX_Xbox.tapB()
    
    print("Start of Zanarkand Dome section")
    friendSlot = FFX_memory.getItemSlot(97)
    if friendSlot == 255:
        friendCount = 0
    else:
        friendCount = FFX_memory.getItemCountSlot(friendSlot)
    
    luckSlot = FFX_memory.getItemSlot(94)
    if luckSlot == 255:
        friendCount = 0
    else:
        luckCount = FFX_memory.getItemCountSlot(luckSlot)
    
    checkpoint = 0
    while FFX_memory.getMap() != 320:
        if FFX_memory.userControl():
            if checkpoint == 13: #Second chest
                friendSlot = FFX_memory.getItemSlot(97)
                if friendSlot == 255:
                    friendCount = 0
                    FFX_targetPathing.setMovement([8,90])
                    FFX_memory.waitFrames(1)
                    FFX_Xbox.tapB()
                else:
                    if FFX_memory.getItemCountSlot(friendSlot) > friendCount:
                        checkpoint += 1
                        FFX_memory.clickToControl()
                    else:
                        FFX_targetPathing.setMovement([8,90])
                        FFX_memory.waitFrames(1)
                        FFX_Xbox.tapB()
            elif checkpoint == 24: #Third chest
                luckSlot = FFX_memory.getItemSlot(94)
                if luckSlot == 255:
                    luckCount = 0
                    FFXC.set_movement(1, 1)
                    FFX_Xbox.tapB()
                else:
                    if FFX_memory.getItemCountSlot(luckSlot) > luckCount:
                        checkpoint += 1
                        print("Updating checkpoint: ", checkpoint)
                        FFX_memory.clickToControl()
                    else:
                        FFXC.set_movement(1, 1)
                        FFX_Xbox.tapB()
            elif checkpoint == 29: #Save sphere
                FFXC.set_movement(0, 1)
                FFX_memory.waitFrames(30 * 0.2)
                FFX_Xbox.tapB()
                FFXC.set_neutral()
                FFX_memory.waitFrames(30 * 1)
                FFX_Xbox.menuA()
                FFX_Xbox.tapB()
                checkpoint += 1
                FFXC.set_movement(1, 0)
                FFX_memory.waitFrames(30 * 0.6)
            elif FFX_memory.getMap() == 316 and checkpoint < 21: #Final room before trials
                print("Final room before trials")
                checkpoint = 21
            elif FFX_targetPathing.setMovement(FFX_targetPathing.zanarkandDome(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_Screen.BattleScreen():
                FFX_Battle.fleeAll()
            elif FFX_memory.diagSkipPossible() and not FFX_memory.battleActive():
                FFX_Xbox.tapB()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()

def trials():
    FFX_memory.fullPartyFormat('yuna')
    
    checkpoint = 0
    while checkpoint < 89:
        checkpoint = trials0(checkpoint)
        checkpoint = trials1(checkpoint)
        checkpoint = trials2(checkpoint)
        checkpoint = trials3(checkpoint)
        checkpoint = trials4(checkpoint)

def trials0(checkpoint):
    FFX_memory.awaitControl()
    
    while checkpoint < 9:
        if FFX_memory.userControl():
            if checkpoint == 8:
                FFXC.set_movement(-1, 0)
                while FFX_memory.userControl():
                    FFX_Xbox.tapB()
                FFXC.set_movement(0, 1)
                FFX_memory.waitFrames(30 * 0.2)
                FFX_memory.awaitControl()
                FFX_memory.waitFrames(30 * 1.3)
                FFXC.set_movement(0, 1)
                checkpoint += 1
            elif FFX_targetPathing.setMovement(FFX_targetPathing.zanarkandTrials(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
    return checkpoint

def trials1(checkpoint):
    FFX_memory.awaitControl()
    
    while checkpoint < 31:
        if FFX_memory.userControl():
            if checkpoint == 20:
                FFXC.set_movement(-1, 1)
                FFX_memory.clickToEvent()
                FFXC.set_neutral()
                FFX_Xbox.SkipDialog(0.5)
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 26 or checkpoint == 28:
                FFXC.set_movement(-1, -1)
                FFX_memory.clickToEvent()
                FFXC.set_neutral()
                FFX_Xbox.SkipDialog(0.5)
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 30:
                FFXC.set_movement(0, 1)
                FFX_memory.awaitEvent()
                FFX_memory.waitFrames(30 * 0.2)
                FFXC.set_neutral()
                checkpoint += 1
            elif FFX_targetPathing.setMovement(FFX_targetPathing.zanarkandTrials(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
    return checkpoint

def trials2(checkpoint):
    FFX_memory.awaitControl()
    
    while checkpoint < 49:
        if FFX_memory.userControl():
            if checkpoint == 46:
                FFXC.set_movement(1, 0)
                FFX_memory.clickToEvent()
                FFXC.set_neutral()
                FFX_Xbox.SkipDialog(0.5)
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 48:
                FFXC.set_movement(-1, 1)
                FFX_memory.awaitEvent()
                FFX_memory.waitFrames(30 * 0.2)
                FFXC.set_neutral()
                checkpoint += 1
            elif FFX_targetPathing.setMovement(FFX_targetPathing.zanarkandTrials(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
    return checkpoint

def trials3(checkpoint):
    FFX_memory.awaitControl()
    
    while checkpoint < 69:
        if FFX_memory.userControl():
            if checkpoint == 66:
                FFXC.set_movement(1, 0)
                FFX_memory.clickToEvent()
                FFXC.set_neutral()
                FFX_Xbox.SkipDialog(0.7)
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 68:
                FFXC.set_movement(-1, 1)
                FFX_memory.awaitEvent()
                FFX_memory.waitFrames(30 * 0.2)
                FFXC.set_neutral()
                checkpoint += 1
            elif FFX_targetPathing.setMovement(FFX_targetPathing.zanarkandTrials(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
    return checkpoint

def trials4(checkpoint):
    FFX_memory.awaitControl()
    
    while checkpoint < 89:
        if FFX_memory.userControl():
            if checkpoint == 81:
                FFXC.set_movement(0, 1)
                FFX_memory.clickToEvent()
                FFXC.set_neutral()
                FFX_Xbox.SkipDialog(0.5)
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif checkpoint == 87:
                FFXC.set_movement(1, 0)
                FFX_memory.clickToEvent()
                FFXC.set_neutral()
                FFX_Xbox.SkipDialog(0.5)
                FFX_memory.clickToControl3()
                checkpoint += 1
            elif FFX_targetPathing.setMovement(FFX_targetPathing.zanarkandTrials(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
    FFXC.set_neutral()
    return checkpoint

def sanctuaryKeeper():
    ver = gameVars.endGameVersion()
    print("Now prepping for Sanctuary Keeper fight")
    
    FFX_Logs.writeStats("Sanctuary Keeper sphere grid, pattern: " + str(ver))
    
    if ver == 4:
        FFX_Logs.writeLog("Starting pattern, FFX_menu.skReturn()")
        print("Pattern for four return spheres off of the B&Y fight")
        FFX_menu.skReturn()
    elif ver == 3:
        FFX_Logs.writeLog("Starting pattern, FFX_menu.skFriend()")
        FFX_menu.skFriend()
    else:
        FFX_Logs.writeLog("Starting pattern, FFX_menu.skMixed()")
        FFX_menu.skMixed()
    
    FFX_memory.fullPartyFormat('yuna')
    
    FFXC.set_movement(-1, 1)
    FFX_memory.waitFrames(30 * 4)
    FFX_Xbox.clickToBattle()
    if FFX_Screen.turnTidus():
        FFX_Battle.defend()
        FFX_Xbox.clickToBattle()
    FFX_Battle.aeonSummon(4) #This is the whole fight. Kinda sad.
    FFX_memory.clickToControl()

def yunalesca():
    ver = gameVars.endGameVersion()
    while not FFX_targetPathing.setMovement([-2,-179]):
        if FFX_memory.diagSkipPossible():
            FFX_Xbox.tapB()
    
    if ver == 4:
        print("Final pattern for four return spheres off of the B&Y fight")
        FFX_menu.skReturn2()
        FFX_memory.closeMenu()
    else:
        print("No further sphere gridding needed at this time.")
    
    print("Sphere grid is done. Moving on to storyline and eventually Yunalesca.")
    
    FFX_memory.touchSaveSphere()
    
    checkpoint = 0
    while not FFX_memory.battleActive(): #Gets us to Yunalesca battle through multiple rooms.
        if FFX_memory.menuOpen():
            FFX_memory.closeMenu()
        elif FFX_memory.userControl():
            if checkpoint in [2,4]:
                FFXC.set_movement(0, 1)
                FFX_memory.awaitEvent()
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
            elif FFX_targetPathing.setMovement(FFX_targetPathing.yunalesca(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            FFXC.set_value('BtnB',1)
            FFXC.set_value('BtnA',1)
            FFX_memory.waitFrames(1)
            FFXC.set_value('BtnB',0)
            FFXC.set_value('BtnA',0)
            FFX_memory.waitFrames(1)
    FFX_Xbox.clickToBattle()
    FFX_Battle.aeonSummon(4) #Summon Bahamut and attack.
    FFX_memory.clickToControl() #This does all the attacking and dialog skipping
    
    #Now to check for zombie strike and then report to logs.
    print("Ready to check for Zomibe Strike")
    if FFX_memory.checkZombieStrike():
        FFX_Logs.writeStats("Zombiestrike True:")
        FFX_Logs.writeStats(gameVars.zombieWeapon())
    else:
        FFX_Logs.writeStats("Zombiestrike False:")
        FFX_Logs.writeStats(gameVars.zombieWeapon())
    print("++Zombiestrike:")
    print("++",gameVars.zombieWeapon())
    
    print("Heading back outside.")
    FFXC.set_neutral()
    FFX_memory.waitFrames(2)
    checkpoint = 0
    while FFX_memory.getMap() != 194:
        if FFX_memory.userControl():
            if checkpoint < 2 and FFX_memory.getMap() == 319: #Back to room before Yunalesca
                checkpoint = 2
                print("Checkpoint reached: ", checkpoint)
            elif checkpoint < 4 and FFX_memory.getMap() == 318: #Exit to room with the inert Aeon
                checkpoint = 4
                print("Checkpoint reached: ", checkpoint)
            elif checkpoint < 9 and FFX_memory.getMap() == 320: #Back to larger of the puzzle rooms
                checkpoint = 9
                print("Checkpoint reached: ", checkpoint)
            elif checkpoint < 17 and FFX_memory.getMap() == 316: #Hallway before puzzle rooms
                checkpoint = 17
                print("Checkpoint reached: ", checkpoint)
            elif checkpoint < 24 and FFX_memory.getMap() == 315: #Hallway before puzzle rooms
                checkpoint = 24
                print("Checkpoint reached: ", checkpoint)
            elif checkpoint == 25:
                FFXC.set_neutral()
                FFX_Xbox.SkipDialog(17)
                FFX_Xbox.skipScene()
                FFX_memory.clickToControl()
            elif FFX_targetPathing.setMovement(FFX_targetPathing.yunalescaToAirship(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_Screen.BattleScreen():
                FFX_Battle.fleeAll()
            elif FFX_memory.diagSkipPossible() and not FFX_memory.battleActive():
                FFX_Xbox.tapB()

