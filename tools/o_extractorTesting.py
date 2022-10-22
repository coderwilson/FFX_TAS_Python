import area.dreamZan
import area.moonflow
import loadGame
import memory.main
import xbox

FFXC = xbox.controllerHandle()

memory.main.start()
Gamestate = "none"
StepCounter = 1

area.dreamZan.NewGame("Extractor testing")
loadGame.load_save_num(96)
memory.main.awaitControl()
FFXC.set_movement(1, -1)
memory.main.awaitEvent()
FFXC.set_neutral()
memory.main.awaitControl()

area.moonflow.southBank(checkpoint=2)
memory.main.clickToControl()

memory.main.end()

print("--------------------------")
print("Program - end")
print("--------------------------")
