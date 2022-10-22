import time

import area.dreamZan
import battle.main
import memory.main
import reset
import screen
import xbox

FFXC = xbox.FFXC

selfAuto = True

attempts = 0
while attempts < 10:
    attempts += 1

    if selfAuto is True:
        print("Starting egg-hunt-only program.")
        print("Waiting to initialize - waiting on New Game screen")
        # ---------- MAKE SURE THIS IS ON FOR A FRESH RUN --------------------
        area.dreamZan.new_game("rescueYuna")
        print("Game start screen")
        screen.clear_mouse(0)

        # Initiate memory reading, after we know the game is open.
        memory.main.start()

        import loadGame

        loadGame.load_save_num(number=51)

        FFXC.set_value("AxisLy", 1)
        FFXC.set_value("AxisLx", 1)
        time.sleep(0.7)
        FFXC.set_value("AxisLx", 0)
        time.sleep(34)
        FFXC.set_value("AxisLy", 0)

        print("Start egg hunt only program")
        print("--------------------------No-control method")

        import zz_eggHuntAuto

        zz_eggHuntAuto.engage()
    else:
        # Initiate memory reading, after we know the game is open.
        print("Start egg hunt only program")
        print("--------------------------No-control method")
        memory.main.start()
        import logs

        logs.next_plot()
        waitCount = 0
        while memory.main.get_map() == 324:
            if memory.main.battle_active():
                print("GTFO battle.")
                battle.main.flee_all()
            elif memory.main.menu_open():
                xbox.menu_b()
            else:
                waitCount += 1
                if waitCount % 10 == 0:
                    print(waitCount)
                    cam = memory.main.get_camera()
                    logs.write_plot(str(cam[0]) + "," + str(cam[4]))
                else:
                    time.sleep(0.035)
                if waitCount > 10000:
                    break

    print("Allowing time for review.")
    time.sleep(35)
    print("Resetting.")
    memory.main.end()

    reset.reset_to_main_menu()
