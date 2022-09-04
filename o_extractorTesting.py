import FFX_Moonflow
import FFX_memory
import FFX_Xbox
import FFX_DreamZan
import FFX_LoadGame
FFXC = FFX_Xbox.controllerHandle()

FFX_memory.start()
Gamestate = "none"
StepCounter = 1

FFX_DreamZan.NewGame("Extractor testing")
FFX_LoadGame.loadSaveNum(96)
FFX_memory.awaitControl()
FFXC.set_movement(1, -1)
FFX_memory.awaitEvent()
FFXC.set_neutral()
FFX_memory.awaitControl()

FFX_Moonflow.southBank(checkpoint=2)
FFX_memory.clickToControl()

FFX_memory.end()

print("--------------------------")
print("Program - end")
print("--------------------------")
