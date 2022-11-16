# currently unused file, should be removed if abandoned
import time

import area.dream_zan
import battle.main
import memory.main
import reset
import screen
import xbox

FFXC = xbox.FFXC

self_auto = True

attempts = 0
while attempts < 10:
    attempts += 1

    if self_auto is True:
        print("Starting egg-hunt-only program.")
        print("Waiting to initialize - waiting on New Game screen")
        # ---------- MAKE SURE THIS IS ON FOR A FRESH RUN --------------------
        area.dream_zan.new_game("rescue_yuna")
        print("Game start screen")

        # Initiate memory reading, after we know the game is open.
        memory.main.start()

        import load_game

        load_game.load_save_num(number=51)

        FFXC.set_value("axis_ly", 1)
        FFXC.set_value("axis_lx", 1)
        time.sleep(0.7)
        FFXC.set_value("axis_lx", 0)
        time.sleep(34)
        FFXC.set_value("axis_ly", 0)

        print("Start egg hunt only program")
        print("--------------------------No-control method")

        import egg_hunt

        egg_hunt.engage()
    else:
        # Initiate memory reading, after we know the game is open.
        print("Start egg hunt only program")
        print("--------------------------No-control method")
        memory.main.start()
        import logs

        logs.next_plot()
        wait_count = 0
        while memory.main.get_map() == 324:
            if memory.main.battle_active():
                print("GTFO battle.")
                battle.main.flee_all()
            elif memory.main.menu_open():
                xbox.menu_b()
            else:
                wait_count += 1
                if wait_count % 10 == 0:
                    print(wait_count)
                    cam = memory.main.get_camera()
                    logs.write_plot(str(cam[0]) + "," + str(cam[4]))
                else:
                    time.sleep(0.035)
                if wait_count > 10000:
                    break

    print("Allowing time for review.")
    time.sleep(35)
    print("Resetting.")
    memory.main.end()

    reset.reset_to_main_menu()
