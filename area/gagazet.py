import battle.boss
import battle.main
import logs
import memory.main
import menu
import pathing
import rng_track
import screen
import vars
import xbox
import save_sphere

game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def check_gems():
    gemSlot = memory.main.get_item_slot(34)
    if gemSlot < 200:
        gems = memory.main.get_item_count_slot(gemSlot)
    else:
        gems = 0

    gemSlot = memory.main.get_item_slot(28)
    if gemSlot < 200:
        gems += memory.main.get_item_count_slot(gemSlot)
    print("Total gems:", gems)
    return gems


def calm_lands():
    memory.main.await_control()
    # Start by getting away from the save sphere
    memory.main.full_party_format("rikku", full_menu_close=True)
    battle.main.heal_up(full_menu_close=True)

    rng_track.print_manip_info()
    print("RNG10:", memory.main.rng_10())
    print("RNG12:", memory.main.rng_12())
    print("RNG13:", memory.main.rng_13())
    # Enter the cutscene where Yuna muses about ending her journey.
    while not (memory.main.get_coords()[1] >= -1650 and memory.main.user_control()):
        if memory.main.user_control():
            FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()

    checkpoint = 0
    while memory.main.get_map() != 279:
        if memory.main.user_control():
            if pathing.set_movement(pathing.calm_lands(checkpoint)):
                checkpoint += 1
                if checkpoint == 15:
                    if check_gems() < 2:
                        checkpoint -= 1
                        FFXC.set_movement(-1, -1)
                        memory.main.wait_frames(60)
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                battle.main.calm_lands_manip()
                memory.main.click_to_control_3()
                memory.main.full_party_format("rikku", full_menu_close=True)
                battle.main.heal_up(full_menu_close=True)
                rng_track.print_manip_info()
            elif memory.main.menu_open():
                xbox.tap_b()
            elif memory.main.diag_skip_possible():
                xbox.menu_b()


def defender_x():
    memory.main.await_control()
    menu.prep_calm_lands()
    memory.main.full_party_format("postbunyip")
    while not pathing.set_movement([67, -255]):
        pass
    FFXC.set_movement(0, 1)
    memory.main.await_event()
    FFXC.set_neutral()

    xbox.click_to_battle()
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if screen.turn_tidus():
                battle.main.buddy_swap_yuna()
            elif screen.turn_yuna():
                battle.main.aeon_summon(4)
            else:
                battle.main.attack("none")
    FFXC.set_movement(0, 1)
    memory.main.click_to_control()
    rng_track.print_manip_info()


def to_the_ronso():
    checkpoint = 2
    while memory.main.get_map() != 259:
        if memory.main.user_control():
            if pathing.set_movement(pathing.defender_x(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()

    # Now in screen with Ronso
    checkpoint = 0
    while memory.main.get_map() != 244:
        if memory.main.user_control():
            if pathing.set_movement(pathing.kelk_ronso(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.turn_ready():
                battle.boss.biran_yenke()
                if game_vars.ne_armor() == 255:
                    return
            elif memory.main.diag_skip_possible():
                xbox.tap_b()


def gagazet_gates():
    # Should appear on the map just before the Ronso hymn
    endVer = game_vars.end_game_version()
    print("Grid version: " + str(endVer))
    logs.write_stats("B&Y Return spheres:")
    if endVer == 4:
        logs.write_stats("4")
    elif endVer == 3:
        logs.write_stats("0")
    else:
        logs.write_stats("2")
    memory.main.await_control()
    if memory.main.overdrive_state()[6] == 100:
        memory.main.full_party_format("kimahri", full_menu_close=False)
    else:
        memory.main.full_party_format("rikku", full_menu_close=False)
    menu.after_ronso()
    memory.main.close_menu()  # just in case

    print("Gagazet path section")
    checkpoint = 0
    while memory.main.get_map() != 285:
        if memory.main.user_control():
            if pathing.set_movement(pathing.gagazet_snow(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.menu_open():
                xbox.tap_b()
            elif memory.main.battle_active():
                # Charge Rikku until full, otherwise flee all
                if memory.main.overdrive_state()[6] == 100:
                    battle.main.flee_all()
                    memory.main.click_to_control()
                else:
                    battle.main.gagazet_path()
                    memory.main.click_to_control()
                    if memory.main.overdrive_state()[6] == 100:
                        memory.main.full_party_format("kimahri")
                    else:
                        memory.main.full_party_format("rikku")
                memory.main.click_to_control()
                if (
                    memory.main.overdrive_state_2()[6] == 100
                    and game_vars.ne_armor() != 255
                ):
                    menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
            elif memory.main.diag_skip_possible():
                xbox.tap_b()
    print("Should now be on the map with Seymour Flux.")


def flux():
    print("Flux screen - ready for Seymour again.")
    FFXC.set_neutral()
    if game_vars.end_game_version() != 3:
        memory.main.full_party_format("yuna")
    checkpoint = 0
    while memory.main.get_map() != 309:
        if memory.main.user_control():
            if checkpoint == 7:
                FFXC.set_movement(0, 1)
                FFXC.set_neutral()
                save_sphere.touch_and_go()
                checkpoint += 1
            elif checkpoint == 8:
                while memory.main.user_control():
                    FFXC.set_movement(1, 1)
                FFXC.set_neutral()
            elif pathing.set_movement(pathing.flux(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                print("Flux battle start")
                battle.boss.seymour_flux()
                # FFXC.set_movement(0,1)
                memory.main.click_to_control_3()
                if game_vars.end_game_version() != 3:
                    menu.after_flux()
                memory.main.full_party_format("kimahri")
            elif memory.main.diag_skip_possible():
                xbox.tap_b()
            elif memory.main.menu_open():
                xbox.tap_b()
    if not game_vars.csr():
        while not memory.main.cutscene_skip_possible():
            if memory.main.diag_skip_possible():
                xbox.tap_b()
        xbox.skip_scene()


def dream(checkpoint: int = 0):
    memory.main.click_to_control()
    print("*********")
    print("Dream sequence")
    print("*********")
    memory.main.wait_frames(3)

    while memory.main.get_map() != 309:
        if memory.main.user_control():
            if checkpoint == 11:
                FFXC.set_movement(-1, 1)
                memory.main.await_event()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 15:
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 19:
                FFXC.set_movement(-1, -1)
                memory.main.await_event()
                FFXC.set_neutral()
                checkpoint += 1
            elif pathing.set_movement(pathing.gagazet_dream_seq(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)

            # Start the final dialog
            if checkpoint == 25:
                xbox.tap_b()
        else:
            xbox.tap_b()  # Skip all dialog
    print("*********")
    print("Dream sequence over")
    print("*********")


def cave():
    checkpoint = 0

    while memory.main.get_map() != 272:
        if memory.main.user_control():
            if memory.main.get_map() == 309 and memory.main.get_coords()[0] > 1160:
                FFXC.set_movement(0.5, 1)
                memory.main.wait_frames(3)
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(6)
            elif pathing.set_movement(pathing.gagazet_post_dream(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
            elif memory.main.menu_open():
                xbox.tap_b()

    memory.main.await_control()
    print("Gagazet cave section")

    checkpoint = 0
    powerNeeded = 6
    while memory.main.get_map() != 311:
        if memory.main.user_control():
            if checkpoint == 7:
                if memory.main.get_map() == 310:
                    print("Now in the trials map.")
                    checkpoint += 1
                else:
                    print("Into swimming map, first trial.")
                    FFXC.set_movement(0, 1)
                    memory.main.wait_frames(30 * 0.5)
            elif checkpoint == 12:
                print("Trial 1 - Let's Go!!!")
                while memory.main.user_control():
                    FFXC.set_movement(0, 1)
                FFXC.set_neutral()

                print("Now the trial has started.")
                xbox.skip_dialog(2)

                # Need logic here for when to start the trial

                FFXC.set_neutral()
                while not memory.main.user_control():
                    if (
                        memory.main.gt_outer_ring() < 2.3
                        and memory.main.gt_outer_ring() > 2.05
                    ):
                        if (
                            memory.main.gt_inner_ring() < 2.9
                            and memory.main.gt_inner_ring() > 1.3
                        ):
                            xbox.tap_b()
                        elif (
                            memory.main.gt_inner_ring() < 0.1
                            and memory.main.gt_inner_ring() > -1.6
                        ):
                            xbox.tap_b()
                    elif (
                        memory.main.gt_outer_ring() < -0.7
                        and memory.main.gt_outer_ring() > -1.1
                    ):
                        if (
                            memory.main.gt_inner_ring() < 2.9
                            and memory.main.gt_inner_ring() > 1.3
                        ):
                            xbox.tap_b()
                        elif (
                            memory.main.gt_inner_ring() < 0.1
                            and memory.main.gt_inner_ring() > -1.6
                        ):
                            xbox.tap_b()

                print("First trial complete")
                checkpoint += 1
            elif checkpoint == 17:
                if memory.main.get_map() == 272:
                    print("Leaving the trials map.")
                    checkpoint += 1
                else:
                    print("Back to main map after first trial.")
                    FFXC.set_movement(0, -1)
                    memory.main.wait_frames(30 * 0.5)
            elif checkpoint == 29:
                if memory.main.get_map() == 310:
                    print("Now in the trials map.")
                    checkpoint += 1
                else:
                    print("Into swimming map, second trial.")
                    FFXC.set_movement(0, 1)
                    memory.main.wait_frames(30 * 0.5)
            elif checkpoint == 35:
                if memory.main.user_control():
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_neutral()

            elif checkpoint == 42:
                print("Out of swimming map, second trial.")
                if memory.main.get_map() == 272:
                    print("Leaving the trials map.")
                    checkpoint += 1
                else:
                    FFXC.set_movement(0, -1)
                    memory.main.wait_frames(30 * 0.5)
            elif checkpoint == 59:  # Just before sanctuary keeper
                FFXC.set_neutral()
                print("Prepping for Sanctuary Keeper")
                memory.main.full_party_format("yuna")
                checkpoint += 1

                # Determine drops from Yunalesca
                # logs.openRNGTrack()
                # import rngTrack
                # zombieResults = rngTrack.zombieTrack(report=True)
                # logs.writeRNGTrack("Final results:"+str(zombieResults))
            elif pathing.set_movement(pathing.gagazet_cave(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if checkpoint == 35:
                if memory.main.diag_progress_flag() == 2:
                    print("Second trial start")
                    memory.main.wait_frames(90)
                    xbox.menu_b()
                    memory.main.wait_frames(45)
                    FFXC.set_value("Dpad", 8)
                    memory.main.wait_frames(45)
                    FFXC.set_neutral()
                    memory.main.click_to_control_dumb()
                    checkpoint += 1
                    print("Second trial is complete")
                elif memory.main.diag_progress_flag() == 3:
                    # CSR second trial
                    memory.main.wait_frames(10)
                    FFXC.set_value("Dpad", 8)
                    memory.main.wait_frames(45)
                    FFXC.set_neutral()
                    memory.main.click_to_control_dumb()
                    checkpoint += 1
                elif memory.main.battle_active():
                    battle.main.flee_all()
                elif memory.main.diag_skip_possible() or memory.main.menu_open():
                    xbox.tap_b()
            elif memory.main.battle_active():
                if memory.main.get_power() < powerNeeded:
                    if memory.main.get_encounter_id() == 351:
                        # Two maelstroms and a splasher
                        battle.main.gagazet_cave("down")
                    elif memory.main.get_encounter_id() == 353:
                        # Two glowey guys, two splashers.
                        battle.main.gagazet_cave("right")
                    elif memory.main.get_encounter_id() == 354:
                        # Four groups of splashers
                        battle.main.gagazet_cave("none")
                    elif memory.main.overdrive_state_2()[6] != 100:
                        if memory.main.get_encounter_id() in [351, 352, 353, 354]:
                            battle.main.cave_charge_rikku()
                        else:
                            battle.main.flee_all()
                    else:
                        battle.main.flee_all()
                else:
                    battle.main.flee_all()
            elif memory.main.menu_open():
                xbox.tap_b()
            elif checkpoint == 6 or checkpoint == 54:
                if memory.main.battle_active():
                    battle.main.flee_all()
                elif memory.main.diag_skip_possible():
                    # So we don't override the second trial
                    xbox.tap_b()

    xbox.click_to_battle()
    battle.boss.s_keeper()


def wrap_up():
    print("Cave section complete and Sanctuary Keeper is down.")
    print("Now onward to Zanarkand.")

    checkpoint = 0
    while memory.main.get_map() != 132:
        if memory.main.user_control():
            if memory.main.get_map() == 312 and checkpoint < 6:
                print("Move forward to next map. Final path before making camp.")
                checkpoint = 7
            elif checkpoint == 3:
                # Story progress - 2635 before hug, 2650 after hug, 2678 after the Mi'ihen scene
                while memory.main.get_story_progress() < 2651:
                    pathing.set_movement([786, -819])
                    xbox.tap_b()
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
            elif checkpoint == 6:
                if memory.main.get_map() == 312:
                    print("Final path before making camp.")
                    FFXC.set_neutral()
                    checkpoint += 1
                else:
                    FFXC.set_movement(1, 1)
            elif pathing.set_movement(pathing.gagazet_peak(checkpoint)):
                checkpoint += 1
                print("Checkpoint reached:", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()

    # Resting point before Zanarkand
    FFXC.set_neutral()
    memory.main.await_control()
    memory.main.wait_frames(30 * 0.07)

    if not game_vars.csr():
        FFXC.set_movement(0, 1)  # Start of the sadness cutscene.
        memory.main.await_event()
        FFXC.set_neutral()

        sleepTime = 4
        print("Sadness cutscene")
        memory.main.wait_frames(30 * sleepTime)
        print("This is gunna be a while.")
        memory.main.wait_frames(30 * sleepTime)
        print("Maybe you should go get a drink or something.")
        memory.main.wait_frames(30 * sleepTime)
        print("Like... what even is this???")
        memory.main.wait_frames(30 * sleepTime)
        print("I just")
        memory.main.wait_frames(30 * sleepTime)
        print("I just can't")
        memory.main.wait_frames(30 * sleepTime)
        print("Do you realize that some poor soul")
        memory.main.wait_frames(30 * sleepTime)
        print("not only wrote the entire program for this by himself")
        memory.main.wait_frames(30 * sleepTime)
        print("And then wasted ten minutes to put in this ridiculous dialog?")
        memory.main.wait_frames(30 * sleepTime)
        print("Talk about not having a life.")
        memory.main.wait_frames(30 * sleepTime)
        print("Ah well, still have some time. Might as well shout out a few people.")
        memory.main.wait_frames(30 * sleepTime)
        print(
            "First and most importantly, my wife for putting up with me for two years through this project.",
        )
        memory.main.wait_frames(30 * sleepTime)
        print("My wife is the best!")
        memory.main.wait_frames(30 * sleepTime)
        print("Next, DwangoAC. He encouraged me to write my own code to do this.")
        memory.main.wait_frames(30 * sleepTime)
        print("And he put together the TASbot community which has been hugely helpful.")
        memory.main.wait_frames(30 * sleepTime)
        print("Shout out to DwangoAC and the TASbot Community. You guys rock!!!")
        memory.main.wait_frames(30 * sleepTime)
        print(
            "Specifically from the TASbot Community, Inverted wrote the pathing logic for the Egg Hunt section.",
        )
        memory.main.wait_frames(30 * sleepTime)
        print("You will see Inverted's work right before the final bosses.")
        memory.main.wait_frames(30 * sleepTime)
        print("Next, some people from the FFX speedrunning community.")
        memory.main.wait_frames(30 * sleepTime)
        print(
            "CrimsonInferno, current world record holder for this category. Dude knows everything about this run!"
        )
        memory.main.wait_frames(30 * sleepTime)
        print(
            "Crimson re-wrote a great many boss fights for this project. From Spherimorph to Evrae Altana, and probably more."
        )
        memory.main.wait_frames(30 * sleepTime)
        print(
            "Also, 'Rossy__' from the same community. Rossy helped me find a great many things in memory."
        )
        memory.main.wait_frames(30 * sleepTime)
        print(
            "He also taught me a number of things about memory scans, pointers, etc. Dude is super smart."
        )
        memory.main.wait_frames(30 * sleepTime)
        print("Peppy too. He has found a few key things in memory too.")
        memory.main.wait_frames(30 * sleepTime)
        print(
            "And last, Mr Tyton from the FFX speedrun community has re-written many pieces of my code."
        )
        memory.main.wait_frames(30 * sleepTime)
        print("He has also done a lot of optimizations I just couldn't get back to.")
        memory.main.wait_frames(30 * sleepTime)
        print(
            "Legitimately Tyton pushed this project from decent towards excellent when I was running out of steam."
        )
        memory.main.wait_frames(30 * sleepTime)
        print("OK that wraps it up for this bit. I'll catch you when it's done.")
        memory.main.wait_frames(30 * sleepTime)

        memory.main.click_to_control()
        print("OMG finally! Let's get to it! (Do kids say that any more?)")
        FFXC.set_movement(0, 1)
        memory.main.wait_frames(30 * 1)
        FFXC.set_movement(-1, 1)
        memory.main.await_event()
        FFXC.set_neutral()
        memory.main.wait_frames(30 * 0.2)
