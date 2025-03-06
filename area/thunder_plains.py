import logging

from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

import battle.main
import memory.main
import menu
import pathing
import screen
import vars
import xbox
import save_sphere
from json_ai_files.write_seed import write_big_text
from paths import ThunderPlainsAgency, ThunderPlainsNorth, ThunderPlainsSouth
from players import Auron, Tidus, Wakka

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def south_pathing():
    if game_vars.story_mode():
        memory.main.wait_seconds(62)
    memory.main.click_to_control_3()
    next_enc_dist = memory.main.distance_to_encounter()
    #next_enc_dist = 380  # Testing only
    logger.warning(f"Next encounter distance: {next_enc_dist}")

    game_vars.set_l_strike(memory.main.l_strike_count())

    memory.main.update_formation(Tidus, Wakka, Auron)
    memory.main.close_menu()
    count50 = 0
    checkpoint = 0
    save_touched = False
    battle_count = 0

    with logging_redirect_tqdm():
        with tqdm(total=50) as pbar:
            while memory.main.get_map() != 256:
                if memory.main.user_control():
                    # Lightning dodging
                    if memory.main.dodge_lightning(game_vars.get_l_strike()):
                        game_vars.set_l_strike(memory.main.l_strike_count())
                        if checkpoint == 34:
                            count50 += 1
                            pbar.update(1)
                            write_big_text(f"Dodging {count50}/50")
                    elif checkpoint == 2 and game_vars.nemesis():
                        checkpoint = 20
                    elif checkpoint == 3 and not save_touched:
                        if next_enc_dist in [380,390]:
                            while not memory.main.battle_active():
                                FFXC.set_movement(0,1)
                            FFXC.set_neutral()
                            battle.main.flee_all()
                            if memory.main.game_over():
                                return 999
                            battle.main.wrap_up()
                        save_sphere.touch_and_go()
                        save_touched = True
                    #elif checkpoint == 2 and not game_vars.get_blitz_win():
                    #    checkpoint = 20
                    elif checkpoint == 21:
                        memory.main.touch_save_sphere()
                        save_touched = True
                        checkpoint += 1
                    elif checkpoint == 25:
                        while memory.main.user_control():
                            pathing.set_movement([-175, -487])
                            xbox.tap_x()
                        checkpoint += 1
                    elif checkpoint == 33:
                        while memory.main.user_control():
                            pathing.set_movement([205, 160])
                            xbox.tap_x()
                        checkpoint += 1
                        logger.info("Now ready to dodge some lightning.")
                    elif checkpoint == 34:
                        if count50 == 50:
                            checkpoint += 1
                        else:  # Dodging fifty bolts.
                            FFXC.set_neutral()
                    elif checkpoint == 39:  # Back to the normal path
                        checkpoint = 10
                        write_big_text("")

                    # General pathing
                    elif memory.main.user_control():
                        if pathing.set_movement(ThunderPlainsSouth.execute(checkpoint)):
                            checkpoint += 1
                            logger.debug(f"Checkpoint {checkpoint}")
                            if checkpoint == 34:
                                write_big_text("Dodging 0/50")
                else:
                    FFXC.set_neutral()
                    if (
                        memory.main.diag_skip_possible()
                        and not memory.main.battle_active()
                        and not game_vars.story_mode()
                    ):
                        xbox.tap_confirm()
                    elif memory.main.battle_active():
                        result = battle.main.thunder_plains(
                            1, battle_count=battle_count
                        )
                        if not result:
                            return 999
                    elif memory.main.menu_open():
                        xbox.tap_b()
                    elif memory.main.game_over():
                        return 999

    memory.main.await_control()
    logger.warning("Outside agency")
    while not pathing.set_movement([-73, 14]):
        if memory.main.diag_skip_possible() and not game_vars.story_mode():
            xbox.menu_b()
    while not pathing.set_movement([-83, 29]):
        if memory.main.diag_skip_possible() and not game_vars.story_mode():
            xbox.menu_b()
    while not memory.main.get_map() == 263:
        FFXC.set_movement(-1, 1)
        if memory.main.diag_skip_possible() and not game_vars.story_mode():
            xbox.menu_b()
    FFXC.set_neutral()
    # menu.auto_sort_equipment()
    return battle_count


def agency_shop():
    speed_count = memory.main.get_speed()

    # 15 plus two (Spherimorph, Flux), minus 1 because it starts on 1
    speed_needed = max(0, min(2, 14 - speed_count))
    grenade_slot = memory.main.get_item_slot(35)
    if grenade_slot == 255:
        cur_grenades = 0
    else:
        cur_grenades = memory.main.get_item_count_slot(grenade_slot)
    total_grenades_needed = 3 + speed_needed - cur_grenades
    # Don't panic if we have more grenades than expected.
    if total_grenades_needed < 0:
        total_grenades_needed = 0
    if game_vars.story_mode():
        memory.main.wait_seconds(1)
        xbox.tap_confirm()
    else:
        memory.main.click_to_diag_progress(92)
    while memory.main.shop_menu_dialogue_row() != 2:
        xbox.tap_down()  # Select "Got any items?"
    while not memory.main.item_shop_menu() == 7:
        xbox.menu_b()  # Click through until items menu comes up
    while not memory.main.item_shop_menu() == 10:
        xbox.menu_b()  # Select buy command

    # For safety (Wendigo is the worst), buying extra phoenix downs first.
    while memory.main.equip_buy_row() != 1:  # Buy some phoenix downs first
        if memory.main.equip_buy_row() < 1:
            xbox.tap_down()
        else:
            xbox.tap_up()
    while not memory.main.item_shop_menu() == 16:
        xbox.tap_b()
    while memory.main.purchasing_amount_items() != 4:
        if memory.main.purchasing_amount_items() < 4:
            xbox.tap_right()
        else:
            xbox.tap_left()
    while not memory.main.item_shop_menu() == 10:
        # Should result in +8 phoenix downs. Can be dialed in later.
        xbox.tap_b()

    if total_grenades_needed:
        # Then buying grenades for multiple uses through the rest of the run.
        while memory.main.equip_buy_row() != 6:
            if memory.main.equip_buy_row() < 6:
                xbox.tap_down()
            else:
                xbox.tap_up()
        while not memory.main.item_shop_menu() == 16:
            xbox.tap_b()
        while memory.main.purchasing_amount_items() != total_grenades_needed:
            if memory.main.purchasing_amount_items() < total_grenades_needed:
                xbox.tap_right()
            else:
                xbox.tap_left()
        while not memory.main.item_shop_menu() == 10:
            xbox.tap_b()
    memory.main.close_menu()


def agency_shop_part_2():  # We'll grab Auron's weapon from O'aka, Macalania Woods
    # Next, Grab Auron's weapon
    xbox.skip_dialog(0.1)
    FFXC.set_neutral()
    memory.main.click_to_diag_progress(90)
    memory.main.click_to_diag_progress(92)
    while memory.main.shop_menu_dialogue_row() != 1:
        xbox.tap_down()
    all_equipment = memory.main.all_equipment()
    tidus_longsword = [
        i
        for i, handle in enumerate(all_equipment)
        if (handle.abilities() == [255, 255, 255, 255] and handle.owner() == 0)
    ][0]
    logger.debug(f"Tidus Longsword in slot: {tidus_longsword}")
    auron_katana = [
        i
        for i, handle in enumerate(all_equipment)
        if (handle.abilities() == [0x800B, 255, 255, 255] and handle.owner() == 2)
    ][0]
    logger.debug(f"Auron Katana in slot: {auron_katana}")
    other_slots = [
        i
        for i, handle in enumerate(all_equipment)
        if (
            i not in [tidus_longsword, auron_katana]
            and handle.equip_status == 255
            and not handle.is_brotherhood()
        )
    ]
    logger.debug(f"Sellable Items in slot: {other_slots}")
    menu.sell_weapon(tidus_longsword)
    # menu.sell_weapon(auron_katana)
    if game_vars.get_blitz_win() and memory.main.get_gil_value() < 8725:
        for loc in other_slots:
            menu.sell_weapon(loc)
            if memory.main.get_gil_value() >= 8725:
                break
    elif not game_vars.get_blitz_win() and memory.main.get_gil_value() < 9550:
        for loc in other_slots:
            menu.sell_weapon(loc)
            if memory.main.get_gil_value() >= 9550:
                break
    if not game_vars.get_blitz_win():
        menu.buy_weapon(0, equip=False)
    menu.buy_weapon(5, equip=False)
    memory.main.close_menu()


def agency():
    logger.info("Arriving at travel agency")
    # Arrive at the travel agency
    memory.main.click_to_control()
    checkpoint = 0

    while memory.main.get_map() != 162:
        str_count = memory.main.get_item_count_slot(memory.main.get_item_slot(87))
        if memory.main.user_control():
            if checkpoint == 1:
                while not memory.main.diag_skip_possible():
                    pathing.set_movement([2, -31])
                    xbox.tap_b()
                    memory.main.wait_frames(3)
                FFXC.set_neutral()
                agency_shop()
                checkpoint += 1
            elif checkpoint == 4:
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                FFXC.set_neutral()
                memory.main.click_to_control()
                checkpoint += 1
            elif checkpoint == 7:
                if not game_vars.csr():
                    kimahri_affection = memory.main.affection_array()[3]
                    logger.debug(f"Kimahri affection, {kimahri_affection}")
                    while memory.main.affection_array()[3] == kimahri_affection:
                        pathing.set_movement([27, -44])
                        xbox.tap_b()
                    logger.debug("Updated, full affection array:")
                    logger.debug(memory.main.affection_array())
                checkpoint += 1
            elif checkpoint == 8:
                while memory.main.user_control():
                    pathing.set_movement([3, -52])
                    xbox.tap_b()
                FFXC.set_neutral()
                memory.main.click_to_control()
                if game_vars.nemesis():
                    # Back in and out to spawn the chest
                    FFXC.set_movement(-1, 1)
                    while memory.main.get_map() != 263:
                        pass
                    FFXC.set_neutral()
                    memory.main.wait_frames(3)
                    while memory.main.get_map() != 256:
                        pathing.set_movement([3, -150])
                        xbox.tap_b()
                    FFXC.set_neutral()
                    memory.main.await_control()
                checkpoint += 1
            elif (
                checkpoint == 9
                and game_vars.nemesis()
                and str_count < 3
            ):
                pathing.set_movement([-73, 45])
                xbox.tap_b()
            elif checkpoint == 11:
                #game_vars.set_blitz_win(value=True)
                FFXC.set_movement(0, 1)
                memory.main.click_to_event()

            elif pathing.set_movement(ThunderPlainsAgency.execute(checkpoint)):
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not game_vars.story_mode():
                xbox.tap_confirm()
            elif checkpoint in [9,11]:
                xbox.tap_confirm()


def north_pathing(battle_count: int):
    memory.main.click_to_control()
    menu.equip_armor(character=0, ability=0x8028)

    l_strike_count = memory.main.l_strike_count()
    lunar_slot = memory.main.get_item_slot(56) != 255

    checkpoint = 0
    while memory.main.get_map() != 110:
        if memory.main.user_control():
            # Lightning dodging
            if memory.main.dodge_lightning(l_strike_count):
                logger.debug("Dodge")
                l_strike_count = memory.main.l_strike_count()
            elif game_vars.csr() and checkpoint == 14:
                checkpoint = 24
            elif checkpoint == 17 and not game_vars.get_blitz_win() and not lunar_slot:
                checkpoint -= 2
                logger.debug(f"No lunar curtain. Checkpoint {checkpoint}")

            # General pathing
            elif memory.main.user_control():
                if pathing.set_movement(ThunderPlainsNorth.execute(checkpoint)):
                    checkpoint += 1
                    logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible() and not memory.main.battle_active() and not game_vars.story_mode():
                xbox.menu_b()
            if memory.main.battle_active():
                result = battle.main.thunder_plains(1, battle_count=battle_count)
                if not result:
                    return False
                lunar_slot = memory.main.get_item_slot(56) != 255
            elif memory.main.menu_open():
                xbox.tap_b()
            elif memory.main.game_over():
                return False

    FFXC.set_neutral()
    memory.main.await_control()
    logger.info("Thunder Plains North complete. Moving to the Macalania save sphere.")
    if not game_vars.csr() and not game_vars.story_mode():
        FFXC.set_movement(0, 1)
        xbox.skip_dialog(6)
        FFXC.set_neutral()

        # Conversation with Auron about Yuna being hard to guard.
        memory.main.click_to_control_3()

        FFXC.set_movement(1, 1)
        memory.main.wait_frames(30 * 2)
        FFXC.set_movement(0, 1)
        xbox.skip_dialog(6)
        FFXC.set_neutral()  # Approaching the party

    else:
        while not pathing.set_movement([258, -7]):
            pass
    return True
