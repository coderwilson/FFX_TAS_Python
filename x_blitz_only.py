# currently unused file, should be removed if abandoned
import time

import area.luca
import blitz
import load_game
import memory.main
import reset
import xbox
import area.dream_zan
import save_sphere
from json_ai_files.write_seed import write_custom_message

FFXC = xbox.controller_handle()


memory.main.start()

attempts = 0
success = 0
result = False
if memory.main.get_map not in [23, 348, 349]:
    reset.reset_to_main_menu()
area.dream_zan.new_game("BlitzballTesting")
load_game.load_save_num(1)
memory.main.reset_battle_end()

while attempts < 1:
    # ---------This is the actual movement/code/logic/etc---------------

    # area.luca.blitz_start()
    save_sphere.approach_save_sphere()
    while memory.main.save_menu_cursor() != 2 and memory.main.save_menu_cursor_2() != 2:
        xbox.menu_down()
    xbox.menu_b()
    time.sleep(3)
    write_custom_message(f"Blitz game {attempts+1} of 1")
    result = blitz.blitz_main(False)

    attempts += 1
    # print("------------------------------")
    # print("Attempts:", attempts)
    # print("Success:", success)
    # print("All attempts results:")
    # print("------------------------------")
    time.sleep(3)
    save_sphere.touch_and_save(save_num=1)
    memory.main.close_menu()
    # if blitzoff_win:
    #    success += 1

    # ---------End of the actual movement/code/logic/etc---------------


reset.reset_no_battles()

memory.main.end()

time.sleep(5)
print("--------------------------")
print("Program - end")
print("--------------------------")
