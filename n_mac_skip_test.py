# Libraries and Core Files
import random
import sys

import area.baaj
import area.besaid
import area.boats
import area.djose
import area.dreamZan
import area.gagazet
import area.guadosalam
import area.home
import area.kilika
import area.luca
import area.miihen
import area.moonflow
import area.MRR
import area.mTemple
import area.mWoods
import area.rescueYuna
import area.sin
import area.thunderPlains
import area.zanarkand
import battle.boss
import battle.main
import blitz
import logs
import memory.main
import reset
import screen
import vars
import xbox
import targetPathing
import loadGame

gameVars = vars.varsHandle()
gameVars.setStartVars()

# Plug in controller
FFXC = xbox.controllerHandle()
Gamestate = "Macalania"
StepCounter = 1 # x9
while not memory.main.start():
    pass

if memory.main.getMap in [23, 348, 349]:
    pass
else:
    reset.resetToMainMenu()


if Gamestate != "none":
    if not (Gamestate == "Luca" and StepCounter == 3):
        area.dreamZan.NewGame(Gamestate)
    import loadGame
    if Gamestate == "Macalania" and StepCounter == 1:  # 1 = south, 2 = north
        loadGame.loadSaveNum(9)
    if Gamestate == "Macalania" and StepCounter == 2:  # 1 = south, 2 = north
        loadGame.loadSaveNum(7)

# Approach the position
prep_step = [[303,34],[284,104],[222,160],[209,170]]
for i in range(len(prep_step)):
    while not targetPathing.setMovement(prep_step[i]):
        if memory.main.diagSkipPossible():
            xbox.tapB()
FFXC.set_neutral()
memory.main.waitFrames(30)
# Into position
while not targetPathing.setMovement([190,180]):
    memory.main.waitFrames(2)
    FFXC.set_neutral()
    memory.main.waitFrames(6)

print("Position Ready")
FFXC.set_neutral()
memory.main.waitFrames(30)

# Angle
FFXC.set_movement(-1,-1)
memory.main.waitFrames(1)
FFXC.set_neutral()
print("Angle Ready")
memory.main.waitFrames(40)

# Engage
FFXC.set_movement(1,1)
memory.main.waitFrames(2)
xbox.tapB()
memory.main.waitFrames(5)
FFXC.set_neutral()
memory.main.waitFrames(60)
