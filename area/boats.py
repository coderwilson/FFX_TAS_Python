import logging

import battle.boss
import battle.main
import memory.main
import menu
import pathing
import vars
import xbox
from paths import BoatsLiki, BoatsWinno

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()
FFXC = xbox.controller_handle()


def boat_dance():
    logger.info("No dancing this time")
    memory.main.wait_frames(30 * 50)


def ss_liki_story():
    path = [
        [28,63],
        [36,-43],
        [14,-67],
        [8,-56],
        [10,-1],  # Lower decks
        [-8,77],
        [-10,95],  # Engine room
        [-53,-74],
        [-49,-100],  # Lower decks
        [1,60],
        [12,69],
        [15,150],  # Upper Deck
        [26,-62],
        [42,-37],
        [58,69],
        [63,88],
        [-2,84]
    ]

    # This adds in story elements we previously took out.
    checkpoint = 0
    while checkpoint < len(path):
        if memory.main.user_control():
            # events
            if checkpoint == 4 and memory.main.get_map() == 148:
                checkpoint += 1
            elif checkpoint == 6:
                pathing.approach_coords([-10,100], click_through=False)
                FFXC.set_neutral()
                xbox.menu_b()
                xbox.menu_b()
                xbox.menu_b()
                xbox.menu_b()
                xbox.menu_b()
                memory.main.await_control()
                memory.main.check_near_actors()
                pathing.approach_actor_by_id(8541)
                #pathing.approach_actor_by_id(20491)  # Primer
                logger.info("I'm on a chocobo! You're on a chocobo!")
                checkpoint += 1
            elif checkpoint == 8 and memory.main.get_map() == 148:
                checkpoint += 1
            elif checkpoint == 11 and memory.main.get_map() == 301:
                checkpoint += 1

            # General pathing
            elif pathing.set_movement(path[checkpoint]):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")

        else:
            FFXC.set_neutral()
    memory.main.check_near_actors(max_dist=80)
    pathing.approach_actor_by_id(5)



def ss_liki():
    if game_vars.story_mode():
        ss_liki_story()
    checkpoint = 0
    while memory.main.get_map() != 43:
        if memory.main.user_control():
            # events
            if checkpoint == 1:  # Group surrounding Yuna
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 3:  # Talk to Wakka
                memory.main.click_to_event_temple(3)
                logger.info(f"Ready for SS Liki menu: {game_vars.early_tidus_grid()}")
                if not game_vars.early_tidus_grid():
                    menu.liki()
                    memory.main.close_menu()
                checkpoint += 1

            # General pathing
            elif pathing.set_movement(BoatsLiki.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")

        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() or memory.main.menu_open():
                if not game_vars.story_mode():
                    xbox.tap_b()
            elif memory.main.cutscene_skip_possible():
                xbox.skip_scene()
            elif memory.main.battle_active():
                logger.info("Ready to start fight with Sin's Fin")
                battle.boss.sin_fin()
                logger.info("Sin's Fin fight complete. Waiting for next fight")
                battle.boss.echuilles()
                logger.info("Sinspawn Echuilles fight complete")


def ss_winno():
    logger.info("Winno section 1 (regular)")
    memory.main.click_to_control()
    # logs.write_stats("Winno Speed Count:")
    # logs.write_stats(memory.get_speed())

    while not memory.main.get_map() in [94,372]:
        if memory.main.user_control():
            if memory.main.get_map() == 167:
                pathing.set_movement([28, -36])  # Through first door
            elif memory.main.get_map() == 237:
                pathing.set_movement([17, 90])  # Stairs to the main deck.
            else:
                logger.warning(f"Cannot determine map: {memory.main.get_map()}")
    FFXC.set_neutral()


def ss_winno_2_story():
    logger.info("Winno section 2 (story mode)")
    path = [
        [18,-117],
        [-20,-100],  # Approach Yuna
        [-37,-75],
        [-50,-47],
        [-50,-67],
        [-40,-67],
        [-14,-67],
        [4,-67],
        [16,-67],
        [0,0],  # Approach Wakka
        [16,-86],
        [16,-67],
        [4,-67],
        [-14,-67],
        [-31,-65],
        [-44,-41],
        [-43,-5],
        [-35,92]
        
    ]

    # This adds in story elements we previously took out.
    memory.main.click_to_control()
    memory.main.wait_frames(2)
    checkpoint = 0
    while checkpoint < len(path):
        if memory.main.user_control():
            # events
            if checkpoint == 1:
                pathing.approach_actor_by_id(2)
                checkpoint += 1
            elif checkpoint == 9:
                pathing.approach_actor_by_id(5)
                checkpoint += 1

            # General pathing
            elif pathing.set_movement(path[checkpoint]):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")

        else:
            FFXC.set_neutral()
    pathing.approach_coords([0,163], click_through=False)
    jecht_shot()
    ss_winno_2(checkpoint=12)



def ss_winno_2(checkpoint = 0):
    # On the deck
    logger.info("Winno section 2 (regular)")
    while memory.main.get_story_progress() < 395:
        if memory.main.user_control():
            if checkpoint < 2 and memory.main.get_map() == 94:
                checkpoint = 2
            elif checkpoint == 6:
                memory.main.click_to_event_temple(2)
                checkpoint += 1
            elif checkpoint < 11 and memory.main.get_story_progress() == 385:
                checkpoint = 11
            elif checkpoint == 11:
                jecht_shot()
                checkpoint += 1
            elif pathing.set_movement(BoatsWinno.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_b()
    if not game_vars.csr():
        memory.main.click_to_diag_progress(142)
        xbox.clear_save_popup(0)


def jecht_shot_success():
    FFXC.set_value("d_pad", 1)  # Up
    xbox.tap_b()
    FFXC.set_neutral()
    FFXC.set_value("d_pad", 1)  # Up
    FFXC.set_value("d_pad", 8)  # Right
    xbox.tap_b()
    FFXC.set_neutral()
    FFXC.set_value("d_pad", 8)  # Right
    xbox.tap_b()
    FFXC.set_neutral()
    FFXC.set_value("d_pad", 8)  # Right
    FFXC.set_value("d_pad", 2)  # Down
    xbox.tap_b()
    FFXC.set_neutral()
    FFXC.set_value("d_pad", 2)  # Down
    xbox.tap_b()
    FFXC.set_neutral()
    FFXC.set_value("d_pad", 2)  # Down
    FFXC.set_value("d_pad", 4)  # Left
    xbox.tap_b()
    FFXC.set_neutral()
    FFXC.set_value("d_pad", 4)  # Left
    xbox.tap_b()
    FFXC.set_neutral()
    FFXC.set_value("d_pad", 4)  # Left
    FFXC.set_value("d_pad", 1)  # Up
    xbox.tap_b()
    FFXC.set_neutral()
    xbox.tap_b()


def jecht_shot():
    # Jecht shot tutorial
    logger.info("Ready for Jecht Shot")
    if game_vars.story_mode():
        memory.main.click_to_diag_progress(89)
        while memory.main.diag_progress_flag() != 97:
            xbox.tap_b()
    else:
        memory.main.click_to_diag_progress(96)
    while memory.main.diag_progress_flag() != 100:
        if memory.main.diag_progress_flag() == 97:
            FFXC.set_value("d_pad", 1)  # Up
            FFXC.set_value("d_pad", 8)  # Right
            xbox.tap_b()
        elif memory.main.diag_progress_flag() == 98:
            FFXC.set_value("d_pad", 4)  # Left
            xbox.tap_b()
        elif memory.main.diag_progress_flag() == 99:
            FFXC.set_value("d_pad", 2)  # Down
            FFXC.set_value("d_pad", 8)  # Right
            xbox.tap_b()
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
        FFXC.set_neutral()
        if game_vars.story_mode():
            xbox.tap_confirm()
            xbox.tap_confirm()
            xbox.tap_confirm()
            xbox.tap_confirm()
            xbox.tap_confirm()

    if game_vars.story_mode():
        # Success logic
        for i in range(15):
            jecht_shot_success()
        # Does not work with CSR version 1.2.0 or beyond. Only with CSR turned off.
    else:
        # Failure logic
        xbox.skip_dialog(2)
        logger.info("End Jecht Shot")
        logger.info("We are intentionally failing the Jecht shot. Save the frames!")
