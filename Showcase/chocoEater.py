import time

import memory.main
import screen
import targetPathing
import xbox

FFXC = xbox.controllerHandle()

def engage():
    checkpoint = 0
    input("Confirm that CSR is running!!!")
    while not memory.main.battleActive():
        if memory.main.userControl():
            pDownSlot = memory.main.getItemSlot(6)
            if memory.main.getMap() == 58:
                memory.main.fullPartyFormat('tidkimwak')
                FFXC.set_movement(0, 1)
                memory.main.awaitEvent()
                FFXC.set_neutral()
            #elif checkpoint == 2 and memory.main.getItemCountSlot(pDownSlot) >= 10:
            #    checkpoint = 4
            elif checkpoint in [2, 3]:
                checkpoint = 4
            elif checkpoint == 5:
                FFXC.set_movement(0, -1)
                memory.main.awaitEvent()
                FFXC.set_neutral()
                checkpoint = 4
            elif targetPathing.setMovement(targetPathing.miihenAgency(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diagSkipPossible():
                xbox.tapB()

def battle():
    memory.main.waitFrames(10)
    chocoIndex = memory.main.actorIndex(actorNum=4200)
    chocoCoords = memory.main.getActorCoords(actorNumber=chocoIndex)
    input("Ready 1")
    memory.main.chocoEaterFun(actorIndex=chocoIndex)
    input("Ready 2")
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()
    exit()