import logging

import airship_pathing
import battle.boss
import battle.main
import egg_hunt
import memory.main
import menu
import pathing
import save_sphere
import vars
import xbox
from paths import InsideSin
from players import Auron, Rikku, Tidus, Yuna, Bahamut, Wakka, CurrentPlayer

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def making_plans():
    # This weird logic allows story mode to work without messing with regular logic.
    memory.main.click_to_diag_progress(210)
    memory.main.click_to_control_3()
    logger.info("Final Push! Let's get this show on the road!!! (Highbridge)")

    # Start by touching the save sphere
    while not pathing.set_movement([-267, 347]):
        pass

    target = [[-242, 312], [-239, 258], [-243, 145], [-243, 10]]
    checkpoint = 0
    while memory.main.get_map() == 194:
        if memory.main.user_control():
            if pathing.set_movement(target[checkpoint]):
                checkpoint += 1

    airship_pathing.air_ship_path(2)  # Talk to Yuna/Kimahri
    FFXC.set_neutral()


def shedinja():  # shelinda
    logger.info("The hymn is the key")
    while memory.main.get_map() != 382:
        if not game_vars.story_mode():
            xbox.tap_confirm()
    logger.debug("Mark 1")
    while memory.main.diag_progress_flag() not in [4, 255]:
        xbox.tap_confirm()
    logger.debug("Mark 2")
    while memory.main.map_cursor() != 10:
        logger.debug("The destination is the key")
        memory.main.menu_direction(memory.main.map_cursor(), 10, 13)
    logger.debug("Mark 3")
    memory.main.click_to_control_dumb()

    memory.main.await_control()
    logger.info("Moving to Shedinja")
    FFXC.set_movement(1, 1)
    memory.main.wait_frames(45)
    FFXC.set_movement(0, 1)
    memory.main.await_event()

    FFXC.set_neutral()
    if not game_vars.csr():
        memory.main.click_to_diag_progress(100)
    memory.main.click_to_diag_progress(75)  # Have you found a way? Well?
    if game_vars.story_mode():
        memory.main.wait_seconds(10)
        xbox.tap_confirm()
    memory.main.click_to_diag_progress(76)  # Have you found a way? Well?
    memory.main.wait_frames(10)
    xbox.tap_down()
    xbox.menu_b()  # We fight Yu Yevon.

    if not game_vars.csr():
        memory.main.click_to_diag_progress(74)
        memory.main.click_to_diag_progress(28)
        memory.main.click_to_control()
    memory.main.await_control()
    low_speed_sphere_check()


def low_speed_sphere_check():
    speed_needed = 2  # Minimum need before BFA
    if memory.main.get_speed() >= speed_needed:
        logger.manip(f"Good on speed spheres, moving straight onward. {memory.main.get_speed()}/{speed_needed}")
        return
    elif game_vars.nemesis():
        logger.manip("No speed sphere check on Nemesis route.")
    logger.manip(f"Short on speed spheres. {memory.main.get_speed()}/{speed_needed}. Initiating recovery.")
    from nemesis.arena_prep import air_ship_destination, return_to_airship
    from paths.destro_spheres import besaid_destro_sphere
    #air_ship_destination(dest_num=2)
    pathing.approach_actor_by_id(actor_id=8449)
    while memory.main.get_map() != 382:
        xbox.tap_confirm()
    memory.main.wait_frames(150)
    xbox.tap_confirm()
    memory.main.wait_frames(9)
    xbox.tap_down()
    xbox.tap_confirm()
    memory.main.wait_frames(9)
    xbox.tap_confirm()
    memory.main.await_control()
    memory.main.update_formation(Tidus, Yuna, Wakka, full_menu_close=False)
    menu.remove_all_nea()
    
    # This section borrowed and updated from the showcase.
    checkpoint = 14
    current_map = memory.main.get_map()
    while memory.main.get_map() != 22:
        if current_map != memory.main.get_map():
            checkpoint += 1
            current_map = memory.main.get_map()
        if memory.main.user_control():
            if pathing.set_movement(besaid_destro_sphere.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
    
    points = [
        [451,184],
        [435,153]
    ]
    while memory.main.get_map() == 22:
        if memory.main.user_control():
            if memory.main.get_speed() < speed_needed:
                if pathing.set_movement(points[checkpoint%2]):
                    checkpoint += 1
                    logger.debug(f"Checkpoint {checkpoint}")
            else:
                pathing.set_movement([500,250])
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                while memory.main.battle_active():
                    if memory.main.turn_ready():
                        CurrentPlayer().attack()
                battle.main.wrap_up()
    memory.main.await_control()
    menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)

    checkpoint = 27
    while checkpoint != 19:
        if memory.main.user_control():
            if pathing.set_movement(besaid_destro_sphere.execute(checkpoint)):
                checkpoint -= 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
    FFXC.set_movement(0,-1)
    memory.main.await_event()
    FFXC.set_neutral()
    memory.main.await_control()
    return_to_airship()

    pass


def exit_cockpit():
    logger.info("Attempting to exit cockpit")
    while memory.main.get_map() != 265:
        if memory.main.user_control():
            tidus_coords = memory.main.get_coords()
            if tidus_coords[1] > 318:
                pathing.set_movement([-244, 315])
            else:
                FFXC.set_movement(0, -1)
        else:
            FFXC.set_neutral()


def facing_sin():
    while not pathing.set_movement([-245, 321]):
        pass

    while memory.main.user_control():
        pathing.set_movement([-256, 342])
        xbox.tap_b()
        memory.main.wait_frames(1)

    FFXC.set_neutral()

    if game_vars.csr():
        memory.main.click_to_control_dumb()
    else:
        # Gets us through the Airship destination menu.
        if game_vars.story_mode():
            memory.main.wait_seconds(15)
            xbox.tap_confirm()
            memory.main.wait_seconds(2)
            xbox.tap_confirm()
            memory.main.wait_seconds(2)
            xbox.tap_confirm()

        else:
            xbox.skip_dialog(15)
        while not memory.main.user_control():
            if memory.main.menu_open():
                xbox.tap_b()
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                xbox.tap_b()

    if memory.main.get_map() in [255, 374]:
        exit_cockpit()
    FFXC.set_neutral()

    airship_pathing.air_ship_path(3)
    battle.main.sin_arms()
    memory.main.click_to_control()
    logger.info("To the deck, talk to Yuna")
    if memory.main.get_map() in [255, 374]:
        exit_cockpit()
    FFXC.set_neutral()
    memory.main.click_to_control()

    airship_pathing.air_ship_path(4)
    FFXC.set_neutral()
    memory.main.click_to_control()

    logger.info("To the deck, Sin's face battle.")
    if memory.main.get_map() in [255, 374]:
        exit_cockpit()
    FFXC.set_neutral()
    airship_pathing.air_ship_path(5)
    battle.main.sin_face()
    logger.info("End of battle with Sin's face.")


def inside_sin(checkpoint = 0):
    rikku_charge = False
    yuna_xp = False
    if checkpoint < 41:
        yuna_needs_levels = 15
    else:
        yuna_needs_levels = 19
    touch_save = False
    if checkpoint == 0 and memory.main.get_map() != 296:
        logger.info("Moving to position next to save sphere")
        while not pathing.set_movement([247, -237]):
            if memory.main.cutscene_skip_possible():
                FFXC.set_neutral()
                memory.main.wait_frames(3)
                xbox.skip_scene()
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_b()
            elif memory.main.menu_open():
                xbox.tap_b()
        logger.info("Moving to next map")
        while memory.main.get_map() != 203:
            # Skip dialog and run to the sea of sorrows map
            FFXC.set_movement(0, -1)
            xbox.tap_b()
        FFXC.set_neutral()
        logger.debug("Ready to start pathing")

    if memory.main.overdrive_state_2()[6] != 100 and game_vars.get_nea_zone() == 3:
        re_equip_ne = True
        rikku_charge = True
        memory.main.update_formation(Tidus, Rikku, Auron, full_menu_close=False)
        menu.equip_armor(character=game_vars.ne_armor(), ability=99)
    elif memory.main.get_yuna_slvl() < yuna_needs_levels:
        yuna_xp = True
        touch_save = True
        #memory.main.update_formation(Tidus, Rikku, Auron, full_menu_close=False)
        #menu.equip_armor(character=game_vars.ne_armor(), ability=99)
    else:
        re_equip_ne = False
        memory.main.update_formation(Tidus, Yuna, Auron, full_menu_close=False)
    memory.main.close_menu()
    
    while memory.main.get_map() != 327:  # All the way to the final save sphere
        if memory.main.user_control():
            # Events
            if memory.main.get_map() == 296:  # Seymour battle
                logger.info("We've reached the Seymour screen.")
                FFXC.set_neutral()
                memory.main.click_to_control()
                memory.main.update_formation(Tidus, Yuna, Auron)
                while not memory.main.battle_active():
                    pathing.set_movement([0,10])
                FFXC.set_neutral()
                if not battle.boss.omnis():
                    logger.error("Seymour battle failed.")
                    return False
                memory.main.click_to_control()
                
                if memory.main.get_yuna_slvl() < yuna_needs_levels:
                    yuna_xp = True
                    touch_save = True
                    memory.main.update_formation(Tidus, Rikku, Auron, full_menu_close=False)
                    menu.equip_armor(character=game_vars.ne_armor(), ability=99)
                return True
            elif checkpoint < 41 and memory.main.get_map() == 204:
                checkpoint = 41
            elif checkpoint < 68 and memory.main.get_map() == 327:
                checkpoint = 68
            elif checkpoint == 69 and touch_save:
                save_sphere.touch_and_go()
                touch_save = False
            
            # Recover from elevator soft lock
            elif memory.main.get_actor_coords(0)[2] < -25:
                logger.debug(f"Elevator scenario identified. Recovering.")
                while not pathing.set_movement([57,-182]):
                    pass
                while not pathing.set_movement([46,-190.5]):
                    pass
                FFXC.set_neutral()
                memory.main.wait_seconds(2)

            # General Pathing
            elif pathing.set_movement(InsideSin.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active() and memory.main.turn_ready():
                logger.debug(f"Encounter check: == {memory.main.get_encounter_id()}")
                if rikku_charge:  # and memory.main.overdrive_state_2()[6] == 100:
                    battle.main.charge_rikku_od()
                    rikku_charge = False
                    memory.main.click_to_control()
                    memory.main.update_formation(
                        Tidus, Yuna, Auron, full_menu_close=False
                    )
                    if not yuna_xp:
                        menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                elif yuna_xp and not memory.main.get_encounter_id() in [376,378,381,384,386]:
                    battle.main.calm_impulse()
                    memory.main.click_to_control()
                    memory.main.update_formation(
                        Tidus, Yuna, Auron, full_menu_close=False
                    )
                    if memory.main.get_yuna_slvl() >= yuna_needs_levels:
                        yuna_xp = False
                        menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                    memory.main.close_menu()
                else:
                    battle.main.flee_all()
            elif memory.main.menu_open():
                xbox.tap_b()
    while not pathing.set_movement([-63,-525]):
        pass
    return True


def execute_egg_hunt():
    #FFXC.set_neutral()
    logger.warning(f"Aeon HP: {Bahamut.hp()}")
    #memory.main.wait_seconds(3)
    #quit()
    #exit()
    if Bahamut.hp() < 2600:
        save_sphere.touch_and_go()
    else:
        save_sphere.touch_and_go()

    while memory.main.get_map() == 327:
        coords = memory.main.get_coords()
        if coords[0] < -18:
            pathing.set_movement([-10,-500])
        elif coords[1] < -455:
            pathing.set_movement([0,-450])
        else:
            pathing.set_movement([0,-100])

    # Done with pathing, now for egg hunt.
    while not memory.main.user_control():
        FFXC.set_movement(-1, -1)
    memory.main.wait_frames(30 * 0.5)
    egg_hunt.engage()
    logger.info("Done with the egg hunt. Final prep for BFA.")
    if game_vars.nemesis():
        menu.equip_weapon(character=0, ability=0x8019, full_menu_close=True)
        FFXC.set_movement(1, 1)
        memory.main.wait_frames(5)
        memory.main.await_event()
        FFXC.set_neutral()
    else:
        if game_vars.zombie_weapon() != 255 and game_vars.zombie_weapon() not in [
            0,
            1,
            2,
        ]:
            logger.info(
                f"Character: {game_vars.zombie_weapon()}, equipping zombie weapon."
            )
            menu.equip_weapon(
                character=game_vars.zombie_weapon(),
                ability=0x8032,
                full_menu_close=False,
            )
        menu.bfa()
