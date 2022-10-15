import area.dreamZan
import area.moonflow
import loadGame
import memory.main as main
import xbox

FFXC = xbox.controllerHandle()

main.start()
Gamestate = "none"
StepCounter = 1

area.dreamZan.NewGame("Extractor testing")
loadGame.loadSaveNum(96)
main.awaitControl()
FFXC.set_movement(1, -1)
main.awaitEvent()
FFXC.set_neutral()
main.awaitControl()

area.moonflow.southBank(checkpoint=2)
main.clickToControl()

main.end()

print("--------------------------")
print("Program - end")
print("--------------------------")
