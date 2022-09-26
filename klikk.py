import logs
import area.dreamZan
import xbox
import memory.main
import vars
import reset
import loadGame
import targetPathing
gameVars = vars.varsHandle()
gameVars.setStartVars()

memory.main.start()
# Plug in controller
FFXC = xbox.controllerHandle()

area.dreamZan.NewGame("Klikk testing")
loadGame.loadSaveNum(101)
memory.main.awaitControl()
while memory.main.userControl():
    targetPathing.setMovement([0, 0])
    if memory.main.getCoords()[0] > -40:
        xbox.tapB()
area.baaj.Klikk_fight()

reset.midRunReset(landRun=False, startTime=logs.timeStamp())
