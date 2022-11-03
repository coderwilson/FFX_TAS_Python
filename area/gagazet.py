import battle.boss
import battle.main
import logging
import logs
import memory.main
import menu
import pathing
import rng_track
import save_sphere
import screen
import vars
import xbox

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def check_gems():
    gem_slot = memory.main.get_item_slot(34)
    if gem_slot < 200:
        gems = memory.main.get_item_count_slot(gem_slot)
    else:
        gems = 0

    gem_slot = memory.main.get_item_slot(28)
    if gem_slot < 200:
        gems += memory.main.get_item_count_slot(gem_slot)
    logger.debug(f"Total gems: {gems}")
    return gems


def calm_lands():
    memory.main.await_control()
    # Start by getting away from the save sphere
    memory.main.full_party_format("rikku", full_menu_close=True)
    battle.main.heal_up(full_menu_close=True)

    rng_track.print_manip_info()
    logger.debug(f"RNG10: {memory.main.rng_10()}")
    logger.debug(f"RNG12: {memory.main.rng_12()}")
    logger.debug(f"RNG13: {memory.main.rng_13()}")
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
                logger.debug(f"Checkpoint reached: {checkpoint}")
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
                logger.debug(f"Checkpoint reached: {checkpoint}")
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
                logger.debug(f"Checkpoint reached: {checkpoint}")
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
    end_ver = game_vars.end_game_version()
    logger.debug(f"Grid version: {end_ver}")
    logs.write_stats("B&Y Return spheres:")
    if end_ver == 4:
        logs.write_stats("4")
    elif end_ver == 3:
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

    logger.info("Gagazet path section")
    checkpoint = 0
    while memory.main.get_map() != 285:
        if memory.main.user_control():
            if pathing.set_movement(pathing.gagazet_snow(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
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
    logger.debug("Should now be on the map with Seymour Flux.")


def flux():
    logger.info("Flux screen - ready for Seymour again.")
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
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                logger.info("Flux battle start")
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
    logger.info("Dream sequence")
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
                logger.debug(f"Checkpoint reached: {checkpoint}")

            # Start the final dialog
            if checkpoint == 25:
                xbox.tap_b()
        else:
            xbox.tap_b()  # Skip all dialog
    logger.info("Dream sequence over")


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
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()
            elif memory.main.menu_open():
                xbox.tap_b()

    memory.main.await_control()
    logger.info("Gagazet cave section")

    checkpoint = 0
    power_needed = 6
    while memory.main.get_map() != 311:
        if memory.main.user_control():
            if checkpoint == 7:
                if memory.main.get_map() == 310:
                    logger.debug("Now in the trials map.")
                    checkpoint += 1
                else:
                    logger.debug("Into swimming map, first trial.")
                    FFXC.set_movement(0, 1)
                    memory.main.wait_frames(30 * 0.5)
            elif checkpoint == 12:
                logger.info("Trial 1 - Let's Go!!!")
                while memory.main.user_control():
                    FFXC.set_movement(0, 1)
                FFXC.set_neutral()

                logger.debug("Now the trial has started.")
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

                logger.info("First trial complete")
                checkpoint += 1
            elif checkpoint == 17:
                if memory.main.get_map() == 272:
                    logger.info("Leaving the trials map.")
                    checkpoint += 1
                else:
                    logger.info("Back to main map after first trial.")
                    FFXC.set_movement(0, -1)
                    memory.main.wait_frames(30 * 0.5)
            elif checkpoint == 29:
                if memory.main.get_map() == 310:
                    logger.info("Now in the trials map.")
                    checkpoint += 1
                else:
                    logger.info("Into swimming map, second trial.")
                    FFXC.set_movement(0, 1)
                    memory.main.wait_frames(30 * 0.5)
            elif checkpoint == 35:
                if memory.main.user_control():
                    FFXC.set_movement(-1, 1)
                else:
                    FFXC.set_neutral()

            elif checkpoint == 42:
                logger.info("Out of swimming map, second trial.")
                if memory.main.get_map() == 272:
                    logger.info("Leaving the trials map.")
                    checkpoint += 1
                else:
                    FFXC.set_movement(0, -1)
                    memory.main.wait_frames(30 * 0.5)
            elif checkpoint == 59:  # Just before sanctuary keeper
                FFXC.set_neutral()
                logger.info("Prepping for Sanctuary Keeper")
                memory.main.full_party_format("yuna")
                checkpoint += 1

                # Determine drops from Yunalesca
                # logs.open_rng_track()
                # import rng_track
                # zombie_results = rng_track.zombie_track(report=True)
                # logs.write_rng_track("Final results:"+str(zombie_results))
            elif pathing.set_movement(pathing.gagazet_cave(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if checkpoint == 35:
                if memory.main.diag_progress_flag() == 2:
                    logger.info("Second trial start")
                    memory.main.wait_frames(90)
                    xbox.menu_b()
                    memory.main.wait_frames(45)
                    FFXC.set_value("d_pad", 8)
                    memory.main.wait_frames(45)
                    FFXC.set_neutral()
                    memory.main.click_to_control_dumb()
                    checkpoint += 1
                    logger.info("Second trial is complete")
                elif memory.main.diag_progress_flag() == 3:
                    # CSR second trial
                    memory.main.wait_frames(10)
                    FFXC.set_value("d_pad", 8)
                    memory.main.wait_frames(45)
                    FFXC.set_neutral()
                    memory.main.click_to_control_dumb()
                    checkpoint += 1
                elif memory.main.battle_active():
                    battle.main.flee_all()
                elif memory.main.diag_skip_possible() or memory.main.menu_open():
                    xbox.tap_b()
            elif memory.main.battle_active():
                if memory.main.get_power() < power_needed:
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
    logger.info("Cave section complete and Sanctuary Keeper is down.")
    logger.info("Now onward to Zanarkand.")

    checkpoint = 0
    while memory.main.get_map() != 132:
        if memory.main.user_control():
            if memory.main.get_map() == 312 and checkpoint < 6:
                logger.info("Move forward to next map. Final path before making camp.")
                checkpoint = 7
            elif checkpoint == 3:
                # Story progress - 2635 before hug, 2650 after hug, 2678 after the Mi'ihen scene
                while memory.main.get_story_progress() < 2651:
                    pathing.set_movement([786, -819])
                    xbox.tap_b()
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
            elif checkpoint == 6:
                if memory.main.get_map() == 312:
                    logger.info("Final path before making camp.")
                    FFXC.set_neutral()
                    checkpoint += 1
                else:
                    FFXC.set_movement(1, 1)
            elif pathing.set_movement(pathing.gagazet_peak(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
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

        sleep_time = 4
        logger.info("Sadness cutscene")
        memory.main.wait_frames(30 * sleep_time)
        logger.info("This is gunna be a while.")
        memory.main.wait_frames(30 * sleep_time)
        logger.info("Maybe you should go get a drink or something.")
        memory.main.wait_frames(30 * sleep_time)
        logger.info("Like... what even is this???")
        memory.main.wait_frames(30 * sleep_time)
        logger.info("I just")
        memory.main.wait_frames(30 * sleep_time)
        logger.info("I just can't")
        memory.main.wait_frames(30 * sleep_time)
        logger.info("Do you realize that some poor soul")
        memory.main.wait_frames(30 * sleep_time)
        logger.info("not only wrote the entire program for this by himself")
        memory.main.wait_frames(30 * sleep_time)
        logger.info("And then wasted ten minutes to put in this ridiculous dialog?")
        memory.main.wait_frames(30 * sleep_time)
        logger.info("Talk about not having a life.")
        memory.main.wait_frames(30 * sleep_time)
        logger.info("Ah well, still have some time. Might as well shout out a few people.")
        memory.main.wait_frames(30 * sleep_time)
        logger.info(
            "First and most importantly, my wife for putting up with me for two years through this project.",
        )
        memory.main.wait_frames(30 * sleep_time)
        logger.info("My wife is the best!")
        memory.main.wait_frames(30 * sleep_time)
        logger.info("Next, DwangoAC. He encouraged me to write my own code to do this.")
        memory.main.wait_frames(30 * sleep_time)
        logger.info("And he put together the TASbot community which has been hugely helpful.")
        memory.main.wait_frames(30 * sleep_time)
        logger.info("Shout out to DwangoAC and the TASbot Community. You guys rock!!!")
        memory.main.wait_frames(30 * sleep_time)
        logger.info(
            "Specifically from the TASbot Community, Inverted wrote the pathing logic for the Egg Hunt section.",
        )
        memory.main.wait_frames(30 * sleep_time)
        logger.info("You will see Inverted's work right before the final bosses.")
        memory.main.wait_frames(30 * sleep_time)
        logger.info("Next, some people from the FFX speedrunning community.")
        memory.main.wait_frames(30 * sleep_time)
        logger.info(
            "CrimsonInferno, current world record holder for this category. Dude knows everything about this run!"
        )
        memory.main.wait_frames(30 * sleep_time)
        logger.info(
            "Crimson re-wrote a great many boss fights for this project. From Spherimorph to Evrae Altana, and probably more."
        )
        memory.main.wait_frames(30 * sleep_time)
        logger.info(
            "Also, 'Rossy__' from the same community. Rossy helped me find a great many things in memory."
        )
        memory.main.wait_frames(30 * sleep_time)
        logger.info(
            "He also taught me a number of things about memory scans, pointers, etc. Dude is super smart."
        )
        memory.main.wait_frames(30 * sleep_time)
        logger.info("Peppy too. He has found a few key things in memory too.")
        memory.main.wait_frames(30 * sleep_time)
        logger.info(
            "And last, Mr Tyton from the FFX speedrun community has re-written many pieces of my code."
        )
        memory.main.wait_frames(30 * sleep_time)
        logger.info("He has also done a lot of optimizations I just couldn't get back to.")
        memory.main.wait_frames(30 * sleep_time)
        logger.info(
            "Legitimately Tyton pushed this project from decent towards excellent when I was running out of steam."
        )
        memory.main.wait_frames(30 * sleep_time)
        logger.info("OK that wraps it up for this bit. I'll catch you when it's done.")
        memory.main.wait_frames(30 * sleep_time)

        memory.main.click_to_control()
        logger.info("OMG finally! Let's get to it! (Do kids say that any more?)")
        FFXC.set_movement(0, 1)
        memory.main.wait_frames(30 * 1)
        FFXC.set_movement(-1, 1)
        memory.main.await_event()
        FFXC.set_neutral()
        memory.main.wait_frames(30 * 0.2)
