import logging

import battle.boss
import battle.main
import logs
import memory.main
import menu
import pathing
import rng_track
import save_sphere
import screen
import vars
import xbox
from paths import (
    CalmLands,
    CalmLandsNemesis,
    DefenderX,
    GagazetCave,
    GagazetDreamSeq,
    GagazetPeak,
    GagazetPostDream,
    GagazetSnow,
    KelkRonso,
    SeymourFlux,
)
from players import Auron, CurrentPlayer, Kimahri, Rikku, Tidus, Wakka, Yuna
from area.ne_armor import next_green
from json_ai_files.write_seed import write_big_text

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()
if game_vars.nemesis():
    import nemesis.changes
from nemesis.changes import gagazet_lv_4_chest

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


def calm_lands(checkpoint = 0):
    memory.main.await_control()
    # Start by getting away from the save sphere
    if memory.main.get_map() == 329:
        while memory.main.get_map() != 223:
            coords = memory.main.get_coords()
            if coords[1] < (5.5714 * coords[0]) + 122.43:
                pathing.set_movement([35,200])
            else:
                pathing.set_movement([-3,-5])
    FFXC.set_neutral()
    needed_levels = game_vars.get_calm_levels_needed()
    if game_vars.story_mode():
        needed_levels += 1
    
    memory.main.update_formation(Tidus, Rikku, Auron, full_menu_close=False)
    battle.main.heal_up(full_menu_close=True)
    
    # Determine variables for the path forward.
    routes, best = rng_track.purifico_to_nea(stage=2)
    half = int(len(routes)/2)
    game_vars.set_def_x_drop(bool((best % 4) >= 2))
    game_vars.set_nea_after_bny(bool(best >= half))
    if (not 2 in routes) and (not 1 in routes):
        game_vars.set_nea_ignore(True)
    #logger.manip(f"X drop: {game_vars.get_def_x_drop()}, Ronso first: {game_vars.get_nea_after_bny()}")

    #rng_track.print_manip_info(pre_x= True)
    # Enter the cutscene where Yuna muses about ending her journey.
    while not (memory.main.get_coords()[1] >= -1650 and memory.main.user_control()):
        if memory.main.user_control():
            FFXC.set_movement(0, 1)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()

    dest_map = 279
    if game_vars.nemesis() and checkpoint == 0:
        dest_map = 307
    while memory.main.get_map() != dest_map:
        if memory.main.user_control():
            if game_vars.nemesis():
                if pathing.set_movement(CalmLandsNemesis.execute(checkpoint)):
                    checkpoint += 1
                    if checkpoint == 15:
                        if check_gems() < 2 or memory.main.get_yuna_slvl() < needed_levels:
                            checkpoint -= 1
                            FFXC.set_movement(-1, -1)
                            memory.main.wait_frames(60)
                        elif game_vars.get_def_x_drop() and memory.main.next_chance_rng_10() != 0:
                            checkpoint -= 1
                            FFXC.set_movement(-1, -1)
                            memory.main.wait_frames(60)
                    logger.debug(f"Checkpoint {checkpoint}")
            else:
                if pathing.set_movement(CalmLands.execute(checkpoint)):
                    checkpoint += 1
                    if checkpoint == 15:
                        if check_gems() < 2 or memory.main.get_yuna_slvl() < needed_levels:
                            checkpoint -= 1
                            FFXC.set_movement(-1, -1)
                            memory.main.wait_frames(60)
                        elif game_vars.get_def_x_drop() and memory.main.next_chance_rng_10() != 0:
                            checkpoint -= 1
                            FFXC.set_movement(-1, -1)
                            memory.main.wait_frames(60)
                    logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if screen.battle_screen():
                enc_id = memory.main.get_encounter_id()
                if check_gems() < 2 and enc_id in [273,275,281,283]:
                    battle.main.calm_lands_gems()
                elif game_vars.mrr_skip_val() and memory.main.get_yuna_slvl() < needed_levels:
                    # We expect to be under levelled on Battle Site logic.
                    battle.main.calm_impulse()
                elif memory.main.get_yuna_slvl() < needed_levels:
                    # This is to catch if we are under level for some other reason. Needs improvement.
                    battle.main.calm_impulse()
                else:
                    battle.main.calm_lands_manip()
                memory.main.click_to_control_3()
                memory.main.update_formation(Tidus, Rikku, Auron, full_menu_close=True)
                battle.main.heal_up(full_menu_close=True)
                #rng_track.print_manip_info(pre_x= True)
            elif memory.main.menu_open():
                xbox.tap_confirm()
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.menu_b()
            

            # Let's report after battle the big text on screen.
            if check_gems() < 2:
                report_str = f"Need to steal {2 - check_gems()} gem(s)."
            elif game_vars.get_nea_ignore():
                report_str = "Skipping NEA"
            else:
                report_str = "NEA: "
                if game_vars.get_nea_after_bny():
                    report_str += "After Ronso, "
                else:
                    report_str += "Before Ronso, "
                if game_vars.get_def_x_drop():
                    report_str += "yes drop on X"
                else:
                    report_str += "no drop on X"
                report_str += f"\nDrop Alignment: {memory.main.next_chance_rng_10()}"

            write_big_text(report_str)


def defender_x():
    memory.main.await_control()
    menu.prep_calm_lands()
    memory.main.update_formation(Tidus, Wakka, Auron)
    while not pathing.set_movement([67, -255]):
        pass
    FFXC.set_movement(0, 1)
    rng_track.print_manip_info(pre_x=True)
    memory.main.await_event()
    FFXC.set_neutral()

    if game_vars.story_mode():
        while not memory.main.turn_ready():
            pass
    else:
        xbox.click_to_battle()
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if Tidus.is_turn():
                battle.main.buddy_swap(Yuna)
            elif Yuna.is_turn():
                battle.main.aeon_summon(4)
            else:
                CurrentPlayer().attack()
    FFXC.set_movement(0, 1)
    memory.main.click_to_control()
    rng_track.print_manip_info(pre_x=False)
    next_green()


def to_the_ronso(checkpoint: int = 2):
    if checkpoint < 6:
        while memory.main.get_map() != 259:
            if memory.main.user_control():
                if pathing.set_movement(DefenderX.execute(checkpoint)):
                    checkpoint += 1
                    logger.debug(f"Checkpoint {checkpoint}")
            else:
                FFXC.set_neutral()
                if memory.main.diag_skip_possible() and not game_vars.story_mode():
                    xbox.tap_confirm()
        checkpoint = 0

    # Now in screen with Ronso
    while memory.main.get_map() != 244:
        if memory.main.user_control():
            if pathing.set_movement(KelkRonso.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.turn_ready():
                battle.boss.biran_yenke()
                logger.warning(f"NE Armor check: {game_vars.ne_armor()}")
                if game_vars.ne_armor() == 255:
                    return
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()


def gagazet_climb(checkpoint: int = 0):
    # Should appear on the map just before the Ronso hymn
    write_big_text("")
    nea_equipped_start = True  # Do I need this?
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
    delay_grid = True
    logger.warning(f"Check Yuna Slvl: {memory.main.get_slvl_yuna()}")
    if memory.main.get_slvl_yuna() >= 4:
        delay_grid = False
        menu.after_ronso()
    elif game_vars.story_mode():
        nea_equipped_start = False
    else:
        nea_equipped_start = False

    logger.info("Gagazet path section")
    talk_wantz = False
    if game_vars.nemesis() or game_vars.story_mode():
        talk_wantz = True

    if nea_equipped_start:
        if game_vars.ne_armor() < 10:
            if not memory.main.equipped_armor_has_ability(
                char_num=game_vars.ne_armor(), ability_num=32797
            ):
                menu.equip_armor(character=game_vars.ne_armor(), ability=32797)
    else:
        if memory.main.overdrive_state()[6] == 100 or memory.main.get_item_slot(39) != 255:
            memory.main.update_formation(Tidus, Kimahri, Auron, full_menu_close=False)
        else:
            memory.main.update_formation(Tidus, Rikku, Auron, full_menu_close=False)
        if memory.main.equipped_armor_has_ability(
            char_num=game_vars.ne_armor(), ability_num=32797
        ):
            menu.equip_armor(character=game_vars.ne_armor(), ability=99)

    memory.main.close_menu()

    while memory.main.get_map() != 285:
        if memory.main.user_control():
            if checkpoint == 19 and talk_wantz:
                memory.main.check_near_actors()
                if pathing.approach_actor_by_id(8413):
                    while memory.main.diag_progress_flag() != 35:
                        if game_vars.nemesis():
                            xbox.tap_confirm()
                    memory.main.wait_seconds(1)
                    xbox.tap_a()
                    xbox.tap_b()
                    talk_wantz = False
            if checkpoint == 22 and game_vars.nemesis():
                gagazet_lv_4_chest()
                checkpoint += 1
            elif pathing.set_movement(GagazetSnow.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.menu_open():
                xbox.tap_confirm()
            elif memory.main.battle_active():
                # Charge Rikku until full, otherwise flee all
                if delay_grid:
                    battle.main.calm_impulse()
                    memory.main.click_to_control()
                    if memory.main.overdrive_state()[6] == 100:
                        memory.main.update_formation(Tidus, Kimahri, Auron, full_menu_close=False)
                    else:
                        memory.main.update_formation(Tidus, Rikku, Auron, full_menu_close=False)
                    if memory.main.get_slvl_yuna() >= 4:
                        menu.after_ronso()
                        delay_grid = False
                        if (
                            memory.main.overdrive_state_2()[6] == 100
                            and game_vars.ne_armor() != 255
                            and not game_vars.story_mode()
                        ):
                            menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                    else:
                        memory.main.close_menu()
                elif game_vars.story_mode() and memory.main.get_slvl_yuna() < 5:
                    # In story mode, we need extra levels to avoid soft lock later.
                    battle.main.calm_impulse()
                    memory.main.click_to_control()
                    memory.main.update_formation(Tidus, Rikku, Auron)
                elif memory.main.overdrive_state()[6] == 100 or memory.main.get_item_slot(39) < 100:
                    # Silence grenade negates the need for overdrive here.
                    battle.main.flee_all()
                    memory.main.click_to_control()
                else:
                    battle.main.gagazet_path()
                    memory.main.click_to_control()
                    if memory.main.overdrive_state()[6] == 100:
                        memory.main.update_formation(Tidus, Kimahri, Auron)
                    else:
                        memory.main.update_formation(Tidus, Rikku, Auron)
                    memory.main.click_to_control()
                    if (
                        memory.main.overdrive_state_2()[6] == 100
                        and game_vars.ne_armor() != 255
                    ):
                        menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
    logger.debug("Should now be on the map with Seymour Flux.")


def flux() -> bool:
    logger.info("Flux screen - ready for Seymour again.")
    logger.info(f"REMINDER, VERSION: {game_vars.end_game_version()}")
    FFXC.set_neutral()
    if game_vars.end_game_version() == 3:
        memory.main.update_formation(Tidus, Kimahri, Wakka)
    else:
        memory.main.update_formation(Tidus, Yuna, Auron)
    checkpoint = 0
    while checkpoint < 8:
        if memory.main.user_control():
            if checkpoint == 7:
                FFXC.set_movement(0, 1)
                FFXC.set_neutral()
                save_sphere.touch_and_go()
                checkpoint += 1
            # elif checkpoint == 8:
            #    while memory.main.user_control():
            #        FFXC.set_movement(1, 1)
            #    FFXC.set_neutral()
            elif pathing.set_movement(SeymourFlux.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                logger.info("Flux battle start")
                if not battle.boss.seymour_flux():
                    return False
                # FFXC.set_movement(0,1)
                memory.main.click_to_control()
                # Removed for Terra
                #if game_vars.end_game_version() != 3:
                #    menu.after_flux()
                memory.main.update_formation(Tidus, Kimahri, Auron)
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
            elif memory.main.menu_open():
                xbox.tap_confirm()
    return True


def dream(checkpoint: int = 0):
    logger.info("Start of dream segment.")
    if memory.main.get_map() == 285:
        while memory.main.get_map() == 285:
            pathing.set_movement([20,-680])
        FFXC.set_neutral()
    logger.info("Dream should be starting now.")
    memory.main.click_to_control()

    while memory.main.get_map() != 309:
        if memory.main.get_story_progress() == 2590:
            # Outdoors, before finding the kid.
            if memory.main.user_control():
                coords = memory.main.get_coords()
                # Outdoor map
                if coords[0] < -1 and coords[1] > 130:
                    pathing.set_movement([3,126])
                elif coords[0] < 20 and coords[1] > 12:
                    pathing.set_movement([12,10])
                elif coords[0] < 125:
                    pathing.set_movement([129,-1])
                elif coords[0] < 195:
                    pathing.set_movement([200,1])
                else:
                    pathing.set_movement([248,26])
        elif memory.main.get_story_progress() == 2595:
            # Indoors, entering the home.
            if memory.main.user_control():
                coords = memory.main.get_coords()
                if coords[1] < -15:
                    pathing.set_movement([62,-10])
                else:
                    pathing.set_movement([30,10])
            else:
                FFXC.set_neutral()
                if not game_vars.story_mode():
                    xbox.tap_confirm()
        elif memory.main.get_story_progress() == 2600:
            if memory.main.get_map() == 165:
                # Indoors, after talking to boy
                if memory.main.user_control():
                    coords = memory.main.get_coords()
                    if coords[0] < 60:
                        pathing.set_movement([62,-10])
                    elif coords[1] > -45:
                        pathing.set_movement([66,-48])
                    else:
                        pathing.set_movement([150,-48])
                else:
                    FFXC.set_neutral()
                    if not game_vars.story_mode():
                        xbox.tap_confirm()
            else:
                # Outdoors, go talk again.
                if memory.main.user_control():
                    coords = memory.main.get_coords()
                    if coords[1] > 12:
                        pathing.set_movement([226,3])
                    elif coords[0] < 235 and coords[1] > -24:
                        pathing.set_movement([237,-26])
                    elif coords[0] < 285:
                        pathing.set_movement([290,-26])
                    elif pathing.set_movement([315,-12]):
                        pathing.approach_coords([326,0],quick_return=True)
                else:
                    FFXC.set_neutral()
                    if not game_vars.story_mode():
                        xbox.tap_confirm()
    logger.info("Dream sequence over")
    memory.main.click_to_control()



def dream_old(checkpoint: int = 0):
    if game_vars.csr():
        while memory.main.get_map() != 309:
            FFXC.set_movement(1, 1)
    else:
        while not memory.main.cutscene_skip_possible():
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
            elif memory.main.user_control():
                FFXC.set_movement(1, 1)
        xbox.skip_scene()
    
    FFXC.set_neutral()
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
            elif pathing.set_movement(GagazetDreamSeq.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")

            # Start the final dialog
            if checkpoint == 25:
                xbox.tap_confirm()
        else:
            xbox.tap_confirm()  # Skip all dialog
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
            elif pathing.set_movement(GagazetPostDream.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
            elif memory.main.menu_open():
                xbox.tap_confirm()

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
                if game_vars.story_mode():
                    memory.main.wait_seconds(2)
                    xbox.tap_confirm()
                    xbox.tap_confirm()
                    xbox.tap_confirm()
                    xbox.tap_confirm()
                else:
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
                            xbox.tap_confirm()
                        elif (
                            memory.main.gt_inner_ring() < 0.1
                            and memory.main.gt_inner_ring() > -1.6
                        ):
                            xbox.tap_confirm()
                    elif (
                        memory.main.gt_outer_ring() < -0.7
                        and memory.main.gt_outer_ring() > -1.1
                    ):
                        if (
                            memory.main.gt_inner_ring() < 2.9
                            and memory.main.gt_inner_ring() > 1.3
                        ):
                            xbox.tap_confirm()
                        elif (
                            memory.main.gt_inner_ring() < 0.1
                            and memory.main.gt_inner_ring() > -1.6
                        ):
                            xbox.tap_confirm()

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
                FFXC.set_movement(-1, 1)

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
                memory.main.update_formation(Tidus, Yuna, Auron)
                checkpoint += 1

                # Determine drops from Yunalesca
                # logs.open_rng_track()
                # import rng_track
                # zombie_results = rng_track.zombie_track(report=True)
                # logs.write_rng_track("Final results:"+str(zombie_results))
            elif pathing.set_movement(GagazetCave.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if checkpoint == 35:
                if memory.main.diag_progress_flag() == 2:
                    logger.info("Second trial start")
                    if game_vars.csr():
                        logger.warning("Version 1")
                        FFXC.set_value("d_pad", 8)
                        memory.main.wait_frames(100)
                        FFXC.set_neutral()
                    else:
                        logger.warning("Version 2")
                        memory.main.wait_frames(90)
                        xbox.menu_b()
                        FFXC.set_value("d_pad", 8)
                        memory.main.wait_frames(90)
                    FFXC.set_neutral()
                    memory.main.click_to_control_dumb()
                    checkpoint += 1
                    logger.info("Second trial is complete")
                elif memory.main.diag_progress_flag() == 3:
                    logger.warning("Version 3")
                    # CSR second trial
                    FFXC.set_value("d_pad", 8)
                    memory.main.wait_frames(10)
                    FFXC.set_neutral()
                    memory.main.click_to_control_dumb()
                    checkpoint += 1
                elif memory.main.battle_active():
                    battle.main.flee_all()
                elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                    xbox.tap_confirm()
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
                xbox.tap_confirm()
            elif checkpoint == 6 or checkpoint == 54:
                if memory.main.battle_active():
                    battle.main.flee_all()
                elif memory.main.diag_skip_possible():
                    # So we don't override the second trial
                    xbox.tap_confirm()

    xbox.click_to_battle()
    battle.boss.s_keeper()


def wrap_up():
    logger.info("Cave section complete and Sanctuary Keeper is down.")
    logger.info("Now onward to Zanarkand.")

    checkpoint = 0
    while memory.main.get_map() != 132:
        if memory.main.get_map() == 381:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
        elif memory.main.user_control():
            if memory.main.get_map() == 312 and checkpoint < 6:
                logger.info("Move forward to next map. Final path before making camp.")
                checkpoint = 7
            elif checkpoint == 3:
                # Story progress:
                # - 2635 before hug
                # - 2650 after hug
                # - 2678 after the Mi'ihen scene
                if memory.main.get_story_progress() >= 2651:
                    checkpoint += 1
                    logger.debug(f"Checkpoint {checkpoint}")
                else:
                    pathing.set_movement([786, -819])
                    xbox.tap_confirm()
            elif checkpoint == 6:
                if memory.main.get_map() == 312:
                    logger.info("Final path before making camp.")
                    FFXC.set_neutral()
                    checkpoint += 1
                else:
                    FFXC.set_movement(1, 1)
            elif pathing.set_movement(GagazetPeak.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()

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
        logger.info(
            "Ah well, still have some time. Might as well shout out a few people."
        )
        memory.main.wait_frames(30 * sleep_time)
        logger.info(
            "First and most importantly, my wife for putting up with me "
            + " for two years through this project.",
        )
        memory.main.wait_frames(30 * sleep_time)
        logger.info("My wife is the best!")
        memory.main.wait_frames(30 * sleep_time)
        logger.info("Next, DwangoAC. He encouraged me to write my own code to do this.")
        memory.main.wait_frames(30 * sleep_time)
        logger.info(
            "And he put together the TASbot community which has been hugely helpful."
        )
        memory.main.wait_frames(30 * sleep_time)
        logger.info("Shout out to DwangoAC and the TASbot Community. You guys rock!!!")
        memory.main.wait_frames(30 * sleep_time)
        logger.info(
            "Specifically from the TASbot Community, Inverted "
            + "wrote the pathing logic for the Egg Hunt section.",
        )
        memory.main.wait_frames(30 * sleep_time)
        logger.info("You will see Inverted's work right before the final bosses.")
        memory.main.wait_frames(30 * sleep_time)
        logger.info("Next, some people from the FFX speedrunning community.")
        memory.main.wait_frames(30 * sleep_time)
        logger.info(
            "CrimsonInferno, current world record holder for this category. "
            + "Dude knows everything about this run!"
        )
        memory.main.wait_frames(30 * sleep_time)
        logger.info(
            "Crimson re-wrote a great many boss fights for this project. "
            + "From Spherimorph to Evrae Altana, and probably more."
        )
        memory.main.wait_frames(30 * sleep_time)
        logger.info(
            "Also, 'Rossy__' from the same community. "
            + "Rossy helped me find a great many things in memory."
        )
        memory.main.wait_frames(30 * sleep_time)
        logger.info(
            "He also taught me a number of things about memory scans, pointers, etc. "
            + "Dude is super smart."
        )
        memory.main.wait_frames(30 * sleep_time)
        logger.info("Peppy too. He has found a few key things in memory too.")
        memory.main.wait_frames(30 * sleep_time)
        logger.info(
            "And last, Mr Tyton from the FFX speedrun community "
            + "has re-written many pieces of my code."
        )
        memory.main.wait_frames(30 * sleep_time)
        logger.info(
            "He has also done a lot of optimizations I just couldn't get back to."
        )
        memory.main.wait_frames(30 * sleep_time)
        logger.info(
            "Legitimately Tyton pushed this project from decent towards "
            + "excellent when I was running out of steam."
        )
        memory.main.wait_frames(30 * sleep_time)
        logger.info("OK that wraps it up for this bit. I'll catch you when it's done.")
        memory.main.wait_frames(30 * sleep_time)

        memory.main.click_to_control()
        logger.info("OMG finally! Let's get to it! (Do kids say that any more?)")
