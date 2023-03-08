import logging

import airship_pathing
import battle.boss
import battle.main
import egg_hunt
import memory.main
import menu
import pathing
import vars
import xbox
from paths import InsideSin
from players import Auron, Rikku, Tidus, Yuna

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def making_plans():
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
        logger.debug("Mark 1")
        xbox.tap_b()
    while memory.main.diag_progress_flag() not in [4, 255]:
        logger.debug("Mark 2")
        xbox.tap_b()
    while memory.main.map_cursor() != 10:
        logger.debug("The destination is the key")
        memory.main.menu_direction(memory.main.map_cursor(), 10, 13)
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
    memory.main.click_to_diag_progress(76)  # Have you found a way? Well?
    memory.main.wait_frames(20)
    xbox.tap_down()
    xbox.menu_b()  # We fight Yu Yevon.

    memory.main.click_to_diag_progress(74)
    memory.main.click_to_diag_progress(28)
    memory.main.click_to_control_3()


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
        xbox.skip_dialog(15)
        while not memory.main.user_control():
            if memory.main.menu_open() or memory.main.diag_skip_possible():
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


def inside_sin():
    logger.info("Moving to position next to save sphere")
    # while not pathing.set_movement([247, -237]):
    #    if memory.main.diag_skip_possible():
    #        xbox.tap_b()
    #    elif memory.main.menu_open():
    #        xbox.tap_b()
    # logger.info("Moving to next map")
    while memory.main.get_map() != 203:
        # Skip dialog and run to the sea of sorrows map
        if memory.main.cutscene_skip_possible():
            FFXC.set_neutral()
            memory.main.wait_frames(3)
            xbox.skip_scene()
        else:
            FFXC.set_movement(0, -1)
            xbox.tap_b()
    FFXC.set_neutral()
    logger.debug("Ready to start pathing")

    if memory.main.overdrive_state_2()[6] != 100 and game_vars.get_nea_zone() == 3:
        re_equip_ne = True
        memory.main.update_formation(Tidus, Rikku, Auron, full_menu_close=False)
        menu.equip_armor(character=game_vars.ne_armor(), ability=99)
    else:
        re_equip_ne = False
        memory.main.update_formation(Tidus, Yuna, Auron, full_menu_close=False)
    memory.main.close_menu()

    checkpoint = 0
    while memory.main.get_map() != 324:  # All the way to the egg hunt.
        if memory.main.user_control():
            # Events
            if memory.main.get_map() == 296:  # Seymour battle
                logger.info("We've reached the Seymour screen.")
                memory.main.update_formation(Tidus, Yuna, Auron)
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(30 * 5)
                FFXC.set_neutral()
                battle.boss.omnis()
                memory.main.click_to_control()
            elif checkpoint < 41 and memory.main.get_map() == 204:
                checkpoint = 41
            elif checkpoint < 68 and memory.main.get_map() == 327:
                checkpoint = 68

            # General Pathing
            elif pathing.set_movement(InsideSin.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active() and memory.main.turn_ready():
                battle.main.charge_rikku_od()
                if re_equip_ne and memory.main.overdrive_state_2()[6] == 100:
                    re_equip_ne = False
                    memory.main.click_to_control()
                    memory.main.update_formation(
                        Tidus, Yuna, Auron, full_menu_close=False
                    )
                    menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
            elif memory.main.menu_open():
                xbox.tap_b()


def execute_egg_hunt():
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
            menu.equip_weapon(
                character=game_vars.zombie_weapon(),
                ability=0x8032,
                full_menu_close=False,
            )
        menu.bfa()
