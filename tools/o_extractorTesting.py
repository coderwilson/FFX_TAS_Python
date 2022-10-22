import area.dreamZan
import area.moonflow
import loadGame
import memory.main
import xbox

FFXC = xbox.controller_handle()

memory.main.start()
Gamestate = "none"
StepCounter = 1

area.dreamZan.new_game("Extractor testing")
loadGame.load_save_num(96)
memory.main.await_control()
FFXC.set_movement(1, -1)
memory.main.await_event()
FFXC.set_neutral()
memory.main.await_control()

area.moonflow.south_bank(checkpoint=2)
memory.main.click_to_control()

memory.main.end()

print("--------------------------")
print("Program - end")
print("--------------------------")
