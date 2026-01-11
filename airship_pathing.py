import logging
import math

import battle.main
import memory.main
import pathing
import vars
import xbox
from paths import Airship
from json_ai_files.write_seed import write_big_text

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def air_ship_path(version, checkpoint:int = 0):
    memory.main.click_to_control()
    distiller_purchase = False
    mana_need = 7
    power_need = 24  # 28 minus four per the guide.
    speed_need = 10
    if game_vars.nemesis() or game_vars.platinum():
        power_need += 6
        speed_need -= 3

    complete = False
    while not complete:
        if memory.main.user_control():
            # Map changes
            if checkpoint == 2:
                memory.main.click_to_event_temple(3)
                checkpoint += 1
            elif (
                version == 1
                and not distiller_purchase
                and checkpoint == 5
                and (
                    memory.main.get_speed() < speed_need or
                    memory.main.get_power() < power_need or
                    memory.main.get_mana() < mana_need
                )
            ):
                dist_msg = "Rin sphere check:\n"
                dist_msg += f"Power: {memory.main.get_power()}/{power_need}\n"
                dist_msg += f"Speed: {memory.main.get_speed()}/{speed_need}\n"
                dist_msg += f"Mana: {memory.main.get_mana()}/{mana_need}"
                write_big_text(dist_msg)
                while memory.main.diag_progress_flag() != 44:
                    if memory.main.user_control():
                        pathing.set_movement([-6, 6])
                        xbox.menu_b()
                    else:
                        FFXC.set_neutral()
                        if memory.main.battle_active():
                            battle.main.flee_all()
                        elif memory.main.menu_open():
                            xbox.menu_b()
                FFXC.set_neutral()
                memory.main.click_to_diag_progress(48)
                while memory.main.airship_shop_dialogue_row() != 1:
                    xbox.tap_down()
                while not memory.main.item_shop_menu() == 7:
                    xbox.menu_b()  # Click through until items menu comes up
                while not memory.main.item_shop_menu() == 10:
                    xbox.menu_b()  # Select buy command


                #  Power spheres
                if memory.main.get_power() < power_need:
                    while memory.main.equip_buy_row() != 7:
                        if memory.main.equip_buy_row() < 7:
                            xbox.tap_down()
                        else:
                            xbox.tap_up()
                    while not memory.main.item_shop_menu() == 16:
                        xbox.menu_b()
                    while memory.main.purchasing_amount_items() != min(
                        math.ceil((power_need - memory.main.get_power()) / 2), 3
                    ):
                        if memory.main.purchasing_amount_items() < min(
                            math.ceil((power_need - memory.main.get_power()) / 2), 3
                        ):
                            xbox.tap_right()
                        else:
                            xbox.tap_left()
                    xbox.menu_b()

                #  Mana spheres
                if memory.main.get_mana() < mana_need:
                    while memory.main.equip_buy_row() != 8:
                        if memory.main.equip_buy_row() < 8:
                            xbox.tap_down()
                        else:
                            xbox.tap_up()
                    while not memory.main.item_shop_menu() == 16:
                        xbox.tap_b()
                    while memory.main.purchasing_amount_items() != min(
                        math.ceil((mana_need - memory.main.get_mana()) / 2), 3
                    ):
                        if memory.main.purchasing_amount_items() < min(
                            math.ceil((mana_need - memory.main.get_mana()) / 2), 3
                        ):
                            xbox.tap_right()
                        else:
                            xbox.tap_left()
                    xbox.menu_b()

                #  Speed spheres
                if memory.main.get_speed() < speed_need:
                    while memory.main.equip_buy_row() != 9:
                        if memory.main.equip_buy_row() < 9:
                            xbox.tap_down()
                        else:
                            xbox.tap_up()
                    while not memory.main.item_shop_menu() == 16:
                        xbox.tap_b()
                    while memory.main.purchasing_amount_items() != min(
                        math.ceil((speed_need - memory.main.get_speed()) / 2), 3
                    ):
                        if memory.main.purchasing_amount_items() < min(
                            math.ceil((speed_need - memory.main.get_speed()) / 2), 3
                        ):
                            xbox.tap_right()
                        else:
                            xbox.tap_left()
                    xbox.menu_b()

                
                #  Done purchasing
                memory.main.close_menu()
                memory.main.click_to_control_3()
                distiller_purchase = True
            elif checkpoint < 6 and memory.main.get_map() == 351:  # Screen with Isaaru
                checkpoint = 6
            elif (
                checkpoint < 9 and memory.main.get_map() == 211
            ):  # Gallery screen (includes lift screens)
                checkpoint = 9
                # Optional save sphere can be touched here.
                # Should not be necessary, we should be touching save sphere in Home
            elif checkpoint == 14 and version == 2:
                logger.info("Talking to Yuna/Kimahri in the gallery")
                checkpoint = 23
                logger.debug(f"Checkpoint update: {checkpoint}")
            elif checkpoint == 16:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 18:
                #logger.debug(memory.main.get_camera())
                #while memory.main.get_camera()[2] < -95:
                #    pathing.set_movement([1,-10])
                #    #if not (game_vars.story_mode() and memory.main.diag_skip_possible()):
                #    xbox.tap_confirm()
                #FFXC.set_neutral()
                checkpoint = 19
                logger.debug(f"Forced checkpoint update: {checkpoint}")
            #elif checkpoint == 18:
            #    FFXC.set_neutral()
            #    xbox.skip_dialog(1)
            #    memory.main.await_control()
            #    checkpoint += 1
            elif checkpoint == 24:
                memory.main.click_to_event_temple(7, story_mode_dialog=True)
                checkpoint += 1

            # Return trip map changes
            elif checkpoint in [32, 34]:  # Formerly included 13
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 37:
                memory.main.click_to_event_temple(1)
                checkpoint += 1
            elif checkpoint == 40:
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint in [43, 44] and not game_vars.csr():
                checkpoint = 45
            elif checkpoint == 44:  # Talk to Cid
                while memory.main.user_control():
                    pathing.set_movement([-250, 339])
                    xbox.tap_b()
                FFXC.set_neutral()
                complete = True
            elif checkpoint == 46:  # Talk to Cid
                if memory.main.get_story_progress() < 3000:
                    while memory.main.user_control():
                        pathing.set_movement([-230, 366])
                        xbox.tap_b()
                    FFXC.set_neutral()
                else:
                    FFXC.set_neutral()
                complete = True

            # Complete states
            elif checkpoint == 19:
                map = memory.main.get_map()
                while map == memory.main.get_map():
                    coords = memory.main.get_actor_coords(0)
                    cam = memory.main.get_camera()
                    if memory.main.user_control():
                        pathing.set_movement([1,100])
                        if coords[1] > -20 and coords[1] < -5:
                            xbox.tap_confirm()
                        
                    else:
                        if memory.main.diag_skip_possible() and not game_vars.story_mode():
                            xbox.tap_confirm()
                        elif memory.main.cutscene_skip_possible():
                            xbox.skip_scene()
                FFXC.set_neutral()
                '''
                if version == 1:
                    logger.info("Evrae battle, includes skip for tutorial.")
                    if game_vars.story_mode():
                        memory.main.click_to_diag_progress(4)
                        memory.main.wait_seconds(15)
                        xbox.tap_confirm()
                        memory.main.wait_seconds(2)
                        xbox.tap_confirm()
                        xbox.click_to_battle()
                    else:
                        xbox.click_to_battle()
                '''
                if version in [3,5,6]:
                    logger.info(f"Expecting start of battle. Version {version}")
                    while not memory.main.battle_active():
                        if memory.main.diag_skip_possible() and not game_vars.story_mode():
                            xbox.tap_confirm()
                        elif memory.main.cutscene_skip_possible():
                            xbox.skip_scene()
                elif version == 4:
                    logger.info("Approach Yuna for conversation")
                    memory.main.await_control()
                    pathing.approach_coords([0,-17])
                    while not memory.main.user_control():
                        if memory.main.diag_skip_possible() and not game_vars.story_mode():
                            xbox.tap_confirm()
                        elif memory.main.cutscene_skip_possible():
                            xbox.skip_scene()
                complete = True

            # General Pathing
            elif pathing.set_movement(Airship.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle.main.flee_all()
            elif memory.main.menu_open():
                xbox.tap_confirm()
            elif memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
            elif checkpoint == 42 and memory.main.diag_progress_flag() == 210:
                xbox.tap_confirm()
    write_big_text("")
    logger.info("End of section, Airship pathing")


def air_ship_return():  # DO NOT USE THIS! FUNCTION IS BROKEN!!!
    logger.info("Conversation with Yuna/Kimahri.")
    memory.main.click_to_control()

    pos = memory.main.get_coords()
    logger.info("Ready to run back to the cockpit.")
    while pos[1] > -90:  # Leaving Yuna/Kimahri, heading back down.
        FFXC.set_value("axis_ly", -1)
        FFXC.set_value("axis_lx", 0)
        pos = memory.main.get_coords()
    logger.debug("Turn East")
    while pos[0] < -1:
        FFXC.set_value("axis_lx", 1)
        FFXC.set_value("axis_ly", 0)
        pos = memory.main.get_coords()
    logger.debug("Turn North")
    while memory.main.user_control():
        FFXC.set_value("axis_lx", 0)
        FFXC.set_value("axis_ly", 1)
        pos = memory.main.get_coords()

    FFXC.set_value("axis_ly", 0)
    FFXC.set_value("axis_lx", 0)
    memory.main.await_control()

    while memory.main.user_control():
        FFXC.set_value("axis_lx", 0)
        FFXC.set_value("axis_ly", 1)

    FFXC.set_value("axis_ly", 0)
    FFXC.set_value("axis_lx", 0)
    memory.main.await_control()

    while memory.main.user_control():
        pos = memory.main.get_coords()
        memory.main.wait_frames(30 * 0.05)
        FFXC.set_value("axis_ly", 1)
        if pos[0] < -1:
            FFXC.set_value("axis_lx", 1)
        else:
            FFXC.set_value("axis_lx", 0)

    FFXC.set_value("axis_ly", 0)
    FFXC.set_value("axis_lx", 0)
    memory.main.await_control()
    FFXC.set_value("axis_ly", 1)
    memory.main.wait_frames(30 * 1.2)
    FFXC.set_value("axis_ly", 0)
    FFXC.set_value("axis_lx", -1)
    memory.main.wait_frames(30 * 0.5)

    while memory.main.user_control():
        FFXC.set_value("axis_ly", 1)
        FFXC.set_value("axis_lx", -1)
    FFXC.set_value("axis_ly", 0)
    FFXC.set_value("axis_lx", 0)
