import battle.main
import memory.main
import screen
import xbox

FFXC = xbox.controllerHandle()


def auron(style="dragon fang"):
    while not memory.main.otherBattleMenu():
        xbox.tapLeft()
    while not memory.main.interiorBattleMenu():
        xbox.tapB()
    print("Style:", style)
    # Doing the actual overdrive
    if style == "dragon fang":
        battle.main._navigate_to_position(0, battleCursor=memory.main.battleCursor3)
        while not memory.main.auronOverdriveActive():
            xbox.tapB()
        print("Starting")
        for i in range(2):  # Do it twice in case there's a miss on the first one.
            FFXC.set_value('Dpad', 2)  # down
            memory.main.waitFrames(1)
            FFXC.set_value('Dpad', 0)
            FFXC.set_value('Dpad', 4)  # left
            memory.main.waitFrames(1)
            FFXC.set_value('Dpad', 0)
            FFXC.set_value('Dpad', 1)  # up
            memory.main.waitFrames(1)
            FFXC.set_value('Dpad', 0)
            FFXC.set_value('Dpad', 8)  # right
            memory.main.waitFrames(1)
            FFXC.set_value('Dpad', 0)
            FFXC.set_value('BtnShoulderL', 1)
            memory.main.waitFrames(1)
            FFXC.set_value('BtnShoulderL', 0)
            FFXC.set_value('BtnShoulderR', 1)
            memory.main.waitFrames(1)
            FFXC.set_value('BtnShoulderR', 0)
            FFXC.set_value('BtnA', 1)
            memory.main.waitFrames(1)
            FFXC.set_value('BtnA', 0)
            FFXC.set_value('BtnB', 1)
            memory.main.waitFrames(1)
            FFXC.set_value('BtnB', 0)
    elif style == "shooting star":
        battle.main._navigate_to_position(1, battleCursor=memory.main.battleCursor3)
        while not memory.main.auronOverdriveActive():
            xbox.tapB()
        for i in range(2):  # Do it twice in case there's a miss on the first one.
            FFXC.set_value('BtnY', 1)
            memory.main.waitFrames(1)
            FFXC.set_value('BtnY', 0)
            FFXC.set_value('BtnA', 1)
            memory.main.waitFrames(1)
            FFXC.set_value('BtnA', 0)
            FFXC.set_value('BtnX', 1)
            memory.main.waitFrames(1)
            FFXC.set_value('BtnX', 0)
            FFXC.set_value('BtnB', 1)
            memory.main.waitFrames(1)
            FFXC.set_value('BtnB', 0)
            FFXC.set_value('Dpad', 4)  # left
            memory.main.waitFrames(1)
            FFXC.set_value('Dpad', 0)
            FFXC.set_value('Dpad', 8)  # right
            memory.main.waitFrames(1)
            FFXC.set_value('Dpad', 0)
            FFXC.set_value('BtnB', 1)
            memory.main.waitFrames(1)
            FFXC.set_value('BtnB', 0)


def kimahri(pos):
    print("Kimahri using Overdrive, pos -", pos)
    while not memory.main.otherBattleMenu():
        xbox.tapLeft()
    while memory.main.otherBattleMenu():
        xbox.tapB()
    battle.main._navigate_to_position(pos, battleCursor=memory.main.battleCursor3)
    while memory.main.interiorBattleMenu():
        xbox.tapB()
    battle.main.tapTargeting()


def tidus(direction=None, version: int = 0, character=99):
    print("Tidus overdrive activating")
    while not memory.main.otherBattleMenu():
        xbox.tapLeft()
    while not memory.main.interiorBattleMenu():
        xbox.tapB()
    if version == 1:
        memory.main.waitFrames(6)
        xbox.menuRight()
    while memory.main.interiorBattleMenu():
        xbox.tapB()
    if character != 99 and memory.main.getEnemyCurrentHP()[character - 20] != 0:
        while character != memory.main.battleTargetId() and memory.main.getEnemyCurrentHP()[character - 20] != 0:
            xbox.tapLeft()
    elif direction:
        if direction == 'left':
            xbox.tapLeft()

    while not memory.main.overdriveMenuActive():
        xbox.tapB()
    memory.main.waitFrames(12)
    print("Hit Overdrive")
    xbox.tapB()  # First try pog
    memory.main.waitFrames(8)
    xbox.tapB()  # Extra attempt in case of miss
    memory.main.waitFrames(9)
    xbox.tapB()  # Extra attempt in case of miss
    memory.main.waitFrames(10)
    xbox.tapB()  # Extra attempt in case of miss
    memory.main.waitFrames(11)
    xbox.tapB()  # Extra attempt in case of miss
    memory.main.waitFrames(12)
    xbox.tapB()  # Extra attempt in case of miss


def valefor(sinFin=0, version=0):
    memory.main.waitFrames(6)
    while memory.main.mainBattleMenu():
        xbox.tapLeft()
    print("Overdrive:", version)
    if version == 1:
        while memory.main.battleCursor2() != 1:
            xbox.tapDown()
    while memory.main.otherBattleMenu():
        xbox.tapB()  # Energy Blast
    if sinFin == 1:
        xbox.tapDown()
        xbox.tapLeft()
    battle.main.tapTargeting()


def wakka():
    print("Wakka overdrive activating")
    while not memory.main.otherBattleMenu():
        xbox.tapLeft()
    while not memory.main.interiorBattleMenu():
        xbox.tapB()
    while memory.main.interiorBattleMenu():
        xbox.tapB()

    memory.main.waitFrames(1)
    xbox.tapB()

    while memory.main.overdriveMenuActiveWakka() == 0:
        pass
    memory.main.waitFrames(76)
    print("Hit Overdrive")
    xbox.tapB()  # First reel
    memory.main.waitFrames(13)
    xbox.tapB()  # Second reel
    memory.main.waitFrames(5)
    xbox.tapB()  # Third reel


def yojimbo(gilValue: int = 263000):
    print("Yojimbo overdrive")
    screen.awaitTurn()
    if not screen.turnAeon():
        return
    while memory.main.battleMenuCursor() != 35:
        xbox.tapUp()
    memory.main.waitFrames(6)
    xbox.menuB()
    print("Selecting amount")
    memory.main.waitFrames(15)
    xbox.tapLeft()
    xbox.tapLeft()
    xbox.tapLeft()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapLeft()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapUp()
    xbox.tapLeft()
    xbox.tapUp()
    xbox.tapUp()
    print("Amount selected")
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()
    return


def yuna(aeonNum: int = 5):
    print("Awaiting Yunas turn")
    while not screen.turnYuna():
        if memory.main.turnReady():
            battle.main.defend()
    while not memory.main.otherBattleMenu():
        xbox.tapLeft()
    while not memory.main.interiorBattleMenu():
        xbox.tapB()
    while not memory.main.battleCursor3() == aeonNum:
        if aeonNum > memory.main.battleCursor3():
            xbox.tapDown()
        else:
            xbox.tapUp()
        memory.main.waitFrames(2)
    xbox.tapB()
    xbox.tapB()
    xbox.tapB()
