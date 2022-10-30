import area.dream_zan
import area.moonflow
import load_game
import memory.main
import xbox

FFXC = xbox.controller_handle()

memory.main.start()
Gamestate = "none"
step_counter = 1

area.dream_zan.new_game("Extractor testing")
load_game.load_save_num(96)
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
