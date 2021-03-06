import pyxinput
import time
import FFX_memory
import FFX_Xbox
import FFX_DreamZan
import FFX_Battle
import FFX_Screen
import FFX_core
import FFX_Reset
import FFX_LoadGame
FFXC = FFX_Xbox.controllerHandle()
import FFX_Moonflow

FFX_memory.start()
Gamestate = "none"
StepCounter = 1

FFX_DreamZan.NewGame("Extractor testing")
FFX_LoadGame.loadSaveNum(96)
FFX_memory.awaitControl()
FFXC.set_movement(1,-1)
FFX_memory.awaitEvent()
FFXC.set_neutral()
FFX_memory.awaitControl()

FFX_Moonflow.southBank(checkpoint=2)
FFX_memory.clickToControl()

FFX_memory.end()

print("--------------------------")
print("Program - end")
print("--------------------------")