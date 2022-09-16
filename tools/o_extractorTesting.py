import area.moonflow as moonflow
import memory
import xbox
import area.dreamZan as dreamZan
import loadGame
FFXC = xbox.controllerHandle()

memory.start()
Gamestate = "none"
StepCounter = 1

dreamZan.NewGame("Extractor testing")
loadGame.loadSaveNum(96)
memory.awaitControl()
FFXC.set_movement(1, -1)
memory.awaitEvent()
FFXC.set_neutral()
memory.awaitControl()

moonflow.southBank(checkpoint=2)
memory.clickToControl()

memory.end()

print("--------------------------")
print("Program - end")
print("--------------------------")
