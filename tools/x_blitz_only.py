# currently unused file, should be removed if abandoned
import time

import area.dream_zan
import area.luca
import blitz
import load_game
import memory.main
import reset
import screen
import xbox

FFXC = xbox.controller_handle()


memory.main.start()

attempts = 0
success = 0
rng_root_array = [0] * 200
rng_success_array = [0] * 21
rng_mod_2_array = [0] * 200
rng_mod_3_array = [0] * 200
rng_mod_4_array = [0] * 200
rng_mod_5_array = [0] * 200
rng_mod_6_array = [0] * 200
rng_mod_7_array = [0] * 200
rng_mod_8_array = [0] * 200
rng_mod_9_array = [0] * 200
rng_mod_10_array = [0] * 200
rng_mod_11_array = [0] * 200
rng_mod_12_array = [0] * 200
rng_mod_13_array = [0] * 200
rng_mod_14_array = [0] * 200
rng_mod_15_array = [0] * 200
rng_mod_16_array = [0] * 200
rng_mod_17_array = [0] * 200
rng_mod_18_array = [0] * 200
rng_mod_19_array = [0] * 200
rng_mod_20_array = [0] * 200

while attempts < 20:
    area.dream_zan.new_game("BlitzballTesting")
    load_game.load_save_num(37)
    memory.main.reset_battle_end()
    rng_root_array[attempts] = memory.main.rng_02()
    offset = 1
    blitzoff_win = False

    # ---------This is the actual movement/code/logic/etc---------------

    rolled_array = memory.main.rng_02_array()

    area.luca.blitz_start()
    while not memory.main.blitz_clock() in [1, 2]:
        FFXC.set_neutral()
    while not (blitz.select_formation() or blitz.select_movement()):
        xbox.tap_y()

    FFXC.set_neutral()
    if blitz.select_movement():
        blitzoff_win = True
    else:
        blitzoff_win = False

    rng_mod_2_array[attempts] = rolled_array[offset] % 2
    rng_mod_3_array[attempts] = rolled_array[offset] % 3
    rng_mod_4_array[attempts] = rolled_array[offset] % 4
    rng_mod_5_array[attempts] = rolled_array[offset] % 5
    rng_mod_6_array[attempts] = rolled_array[offset] % 6
    rng_mod_7_array[attempts] = rolled_array[offset] % 7
    rng_mod_8_array[attempts] = rolled_array[offset] % 8
    rng_mod_9_array[attempts] = rolled_array[offset] % 9
    rng_mod_10_array[attempts] = rolled_array[offset] % 10
    rng_mod_11_array[attempts] = rolled_array[offset] % 11
    rng_mod_12_array[attempts] = rolled_array[offset] % 12
    rng_mod_13_array[attempts] = rolled_array[offset] % 13
    rng_mod_14_array[attempts] = rolled_array[offset] % 14
    rng_mod_15_array[attempts] = rolled_array[offset] % 15
    rng_mod_16_array[attempts] = rolled_array[offset] % 16
    rng_mod_17_array[attempts] = rolled_array[offset] % 17
    rng_mod_18_array[attempts] = rolled_array[offset] % 18
    rng_mod_19_array[attempts] = rolled_array[offset] % 19
    rng_mod_20_array[attempts] = rolled_array[offset] % 20

    if blitzoff_win and rng_mod_2_array[attempts]:
        rng_success_array[2] += 1
    elif not blitzoff_win and not rng_mod_2_array[attempts]:
        rng_success_array[2] += 1
    if blitzoff_win and rng_mod_3_array[attempts]:
        rng_success_array[3] += 1
    elif not blitzoff_win and not rng_mod_3_array[attempts]:
        rng_success_array[3] += 1
    if blitzoff_win and rng_mod_4_array[attempts]:
        rng_success_array[4] += 1
    elif not blitzoff_win and not rng_mod_4_array[attempts]:
        rng_success_array[4] += 1
    if blitzoff_win and rng_mod_5_array[attempts]:
        rng_success_array[5] += 1
    elif not blitzoff_win and not rng_mod_5_array[attempts]:
        rng_success_array[5] += 1
    if blitzoff_win and rng_mod_6_array[attempts]:
        rng_success_array[6] += 1
    elif not blitzoff_win and not rng_mod_6_array[attempts]:
        rng_success_array[6] += 1
    if blitzoff_win and rng_mod_7_array[attempts]:
        rng_success_array[7] += 1
    elif not blitzoff_win and not rng_mod_7_array[attempts]:
        rng_success_array[7] += 1
    if blitzoff_win and rng_mod_8_array[attempts]:
        rng_success_array[8] += 1
    elif not blitzoff_win and not rng_mod_8_array[attempts]:
        rng_success_array[8] += 1
    if blitzoff_win and rng_mod_9_array[attempts]:
        rng_success_array[9] += 1
    elif not blitzoff_win and not rng_mod_9_array[attempts]:
        rng_success_array[9] += 1
    if blitzoff_win and rng_mod_10_array[attempts]:
        rng_success_array[10] += 1
    elif not blitzoff_win and not rng_mod_10_array[attempts]:
        rng_success_array[10] += 1
    if blitzoff_win and rng_mod_11_array[attempts]:
        rng_success_array[11] += 1
    elif not blitzoff_win and not rng_mod_11_array[attempts]:
        rng_success_array[11] += 1
    if blitzoff_win and rng_mod_12_array[attempts]:
        rng_success_array[12] += 1
    elif not blitzoff_win and not rng_mod_12_array[attempts]:
        rng_success_array[12] += 1
    if blitzoff_win and rng_mod_13_array[attempts]:
        rng_success_array[13] += 1
    elif not blitzoff_win and not rng_mod_13_array[attempts]:
        rng_success_array[13] += 1
    if blitzoff_win and rng_mod_14_array[attempts]:
        rng_success_array[14] += 1
    elif not blitzoff_win and not rng_mod_14_array[attempts]:
        rng_success_array[14] += 1
    if blitzoff_win and rng_mod_15_array[attempts]:
        rng_success_array[15] += 1
    elif not blitzoff_win and not rng_mod_15_array[attempts]:
        rng_success_array[15] += 1
    if blitzoff_win and rng_mod_16_array[attempts]:
        rng_success_array[16] += 1
    elif not blitzoff_win and not rng_mod_16_array[attempts]:
        rng_success_array[16] += 1
    if blitzoff_win and rng_mod_17_array[attempts]:
        rng_success_array[17] += 1
    elif not blitzoff_win and not rng_mod_17_array[attempts]:
        rng_success_array[17] += 1
    if blitzoff_win and rng_mod_18_array[attempts]:
        rng_success_array[18] += 1
    elif not blitzoff_win and not rng_mod_18_array[attempts]:
        rng_success_array[18] += 1
    if blitzoff_win and rng_mod_19_array[attempts]:
        rng_success_array[19] += 1
    elif not blitzoff_win and not rng_mod_19_array[attempts]:
        rng_success_array[19] += 1
    if blitzoff_win and rng_mod_20_array[attempts]:
        rng_success_array[20] += 1
    elif not blitzoff_win and not rng_mod_20_array[attempts]:
        rng_success_array[20] += 1

    attempts += 1
    print("------------------------------")
    print("------------------------------")
    print("Attempts:", attempts)
    print("Success:", success)
    print("All attempts results:")
    print(rng_success_array)
    print("------------------------------")
    print("------------------------------")
    time.sleep(5)
    if blitzoff_win:
        success += 1

    # ---------End of the actual movement/code/logic/etc---------------

    if attempts < 20:
        print("Resetting.")

        memory.main.reset_blitz_menu_num()
        reset.reset_to_main_menu()
    else:
        print("Final Results:")
        print("------------------------------")
        print("------------------------------")
        print("Attempts:", attempts)
        print("Success:", success)
        print("All attempts results:")
        print(rng_success_array)
        print("------------------------------")
        print("------------------------------")

time.sleep(5)

memory.main.end()

time.sleep(5)
print("--------------------------")
print("Program - end")
print("--------------------------")
