import datetime

import logs
import memory.main
import vars
import xbox

gameVars = vars.vars_handle()

FFXC = xbox.controller_handle()


def mid_run_reset(land_run: bool = False, start_time=datetime.datetime.now()):
    if land_run:
        endTime = logs.time_stamp()
        totalTime = endTime - start_time
        logs.write_stats("Total time:")
        logs.write_stats(str(totalTime))
        print("The game duration was:", str(totalTime))
        print(
            "This duration is intended for comparison reference only, not as a true timer."
        )
        print("Please do not use this as your submitted time.")
        memory.main.wait_frames(30)
        print("--------")
        print("In order to conform with speedrun standards,")
        memory.main.wait_frames(60)
        print("we now wait until the end of the credits and stuff")
        memory.main.wait_frames(60)
        print("and then will open up the list of saves.")
        memory.main.wait_frames(60)
        print(
            "This will show the autosave values, which conforms to the speedrun rules."
        )
        # Bring up auto-save
        while memory.main.get_map() != 23:
            if memory.main.get_map() in [348, 349]:
                xbox.tap_start()
            elif memory.main.cutscene_skip_possible():
                xbox.skip_scene()
        memory.main.wait_frames(180)
        while not memory.main.save_menu_open():
            xbox.tap_b()
        memory.main.wait_frames(180)
        xbox.menu_a()
        xbox.menu_a()
        xbox.menu_a()
    else:
        memory.main.wait_frames(60)
        reset_to_main_menu()

    # Now to re-start
    gameVars.set_start_vars()
    rngSeed = memory.main.rng_seed()
    if land_run:
        rngSeed += 0
        if rngSeed == 256:
            rngSeed = 0
    logs.reset_stats_log()
    logs.next_stats(rngSeed)  # Start next stats file
    if gameVars.use_set_seed():
        memory.main.set_rng_seed(rngSeed)
    print("-------------This game will be using RNG seed:", rngSeed)
    logs.next_stats(rngSeed)
    logs.write_stats("RNG seed:")
    logs.write_stats(rngSeed)
    Gamestate = "none"
    StepCounter = 1

    return Gamestate, StepCounter


def reset_to_main_menu():
    FFXC.set_neutral()
    if memory.main.get_story_progress() <= 8:
        memory.main.wait_frames(30 * 0.07)
        while not memory.main.get_map() in [23, 348, 349]:
            print("----------Attempting reset")
            print("FFX map:", memory.main.get_map())
            print("----------")
            memory.main.set_map_reset()
            memory.main.wait_frames(30 * 0.1)
            memory.main.force_map_load()
            memory.main.wait_frames(30 * 1)
    elif memory.main.battle_active():
        print("Battle is active. Forcing battle to end so we can soft reset.")
        while not memory.main.turn_ready():
            xbox.menu_a()
        memory.main.reset_battle_end()
        while not memory.main.get_map() in [23, 348, 349]:
            xbox.menu_b()

    else:
        memory.main.wait_frames(30 * 0.07)
        while not memory.main.get_map() in [23, 348, 349]:
            print("----------Attempting reset")
            print("FFX map:", memory.main.get_map())
            print("----------")
            memory.main.set_map_reset()
            memory.main.wait_frames(30 * 0.1)
            memory.main.force_map_load()
            memory.main.wait_frames(30 * 1)
    print("Resetting")
