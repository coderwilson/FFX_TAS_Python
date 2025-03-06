import logging

from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

import memory.main
from memory.main import equip_sell_row
import menu_grid
import vars
import xbox
from players import Auron, Rikku, Tidus, Wakka, Yuna, Lulu

game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()

logger = logging.getLogger(__name__)


def grid_up():
    menu_grid.grid_up()


def grid_down():
    menu_grid.grid_down()


def grid_left():
    menu_grid.grid_left()


def grid_right():
    menu_grid.grid_right()


def await_move():
    logger.debug("Sphere Grid: Waiting for Move command to be highlighted")
    while not memory.main.s_grid_active():
        logger.critical("The Sphere Grid isn't even open! Awaiting manual recovery.")
        memory.main.wait_frames(30 * 1)
    complete = False
    while not complete:
        menu_val = memory.main.s_grid_menu()
        if menu_val == 11 or menu_val == 255:
            xbox.menu_b()
        elif menu_val == 7:
            cursor_loc = memory.main.cursor_location()
            if cursor_loc[0] == 51 or cursor_loc[1] == 243:
                xbox.menu_up()
            xbox.menu_b()
            complete = True
            memory.main.wait_frames(30 * 0.25)
    logger.debug("Move command highlighted. Good to go.")


def await_use():
    logger.debug("Sphere Grid: Waiting for Use command to be highlighted")
    while not memory.main.s_grid_active():
        logger.critical("The Sphere Grid isn't even open! Awaiting manual recovery.")
        memory.main.wait_frames(30 * 1)
    complete = False
    while not complete:
        menu_val = memory.main.s_grid_menu()
        logger.debug(f"Menu value: {menu_val}")
        if menu_val == 7:
            cursor_loc = memory.main.cursor_location()
            if cursor_loc[0] == 102 or cursor_loc[1] == 14:
                xbox.menu_down()
            xbox.menu_b()
            complete = True
            memory.main.wait_frames(30 * 0.25)
        else:
            xbox.menu_b()
    logger.debug("Use command highlighted. Good to go.")


def await_quit_sg():
    logger.debug("Sphere Grid: attempting to quit")
    while memory.main.s_grid_active():
        menu_val = memory.main.s_grid_menu()
        if menu_val == 255:
            xbox.menu_a()
        elif menu_val == 11:
            xbox.menu_b()
        else:
            xbox.menu_a()
    logger.info("Back to the main menu")


def auto_sort_items(manual="n"):
    memory.main.open_menu()
    xbox.menu_down()
    xbox.menu_b()
    memory.main.wait_frames(12)
    xbox.menu_a()
    memory.main.wait_frames(12)
    xbox.menu_right()
    memory.main.wait_frames(12)
    xbox.menu_b()
    memory.main.wait_frames(12)
    xbox.menu_right()
    memory.main.wait_frames(12)
    xbox.menu_b()
    xbox.menu_b()
    xbox.menu_b()
    if manual == "y":
        xbox.menu_left()
        xbox.menu_b()
    elif manual == "n":
        memory.main.close_menu()
    else:
        memory.main.close_menu()


def auto_sort_equipment(manual="n"):
    memory.main.open_menu()
    xbox.menu_down()
    xbox.menu_b()
    memory.main.wait_frames(12)
    xbox.menu_a()
    memory.main.wait_frames(12)
    xbox.menu_right()
    xbox.menu_right()
    memory.main.wait_frames(12)
    xbox.menu_b()
    memory.main.wait_frames(12)
    xbox.menu_right()
    xbox.menu_b()
    xbox.menu_b()
    xbox.menu_b()
    if manual == "y":
        xbox.menu_left()
        xbox.menu_b()
    elif manual == "n":
        memory.main.close_menu()
    else:
        memory.main.close_menu()


def short_aeons():
    memory.main.print_memory_log()
    memory.main.open_menu()
    while memory.main.get_hp()[0] < memory.main.get_max_hp()[0]:
        xbox.tap_b()
    memory.main.back_to_main_menu()
    cursor_target = 4
    logger.debug(f"Aiming at {cursor_target}")
    while memory.main.get_menu_cursor_pos() != cursor_target:
        while memory.main.get_menu_cursor_pos() != cursor_target:
            logger.debug(memory.main.get_menu_cursor_pos())
            xbox.tap_up()
        memory.main.wait_frames(1)
    while memory.main.menu_number() == 5:
        xbox.tap_b()
    while memory.main.config_cursor() != 5:
        while memory.main.config_cursor() != 5:
            xbox.tap_up()
        memory.main.wait_frames(1)
    while memory.main.config_aeon_cursor_column() != 1:
        xbox.tap_right()
    while memory.main.config_cursor() != 3:
        while memory.main.config_cursor() != 3:
            xbox.tap_up()
        memory.main.wait_frames(1)
    while memory.main.config_cursor_column() != 1:
        xbox.tap_right()
    memory.main.close_menu()


def liki():
    logger.debug("Menu - SS Liki")
    open_grid(character=0)
    memory.main.wait_frames(10)

    # Move to the Def node just to the left
    logger.debug("Sphere grid on Tidus, learn Cheer and Str +1")
    menu_grid.move_first()
    grid_up()
    grid_up()
    if memory.main.get_tidus_slvl() >= 3:
        grid_left()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "left")
        menu_grid.use_and_use_again()  # Str +1 node
    menu_grid.sel_sphere("ability", "none")  # Cheer
    xbox.menu_b()
    menu_grid.use_and_quit()
    xbox.menu_a()


def woods_menuing():
    # Tidus learning Flee
    open_grid(character=0)
    xbox.menu_b()
    xbox.menu_b()  # Sphere grid on Tidus
    menu_grid.move_first()
    start_node = memory.main.s_grid_cursor_coords()[0]
    if start_node == 242:
        agi_need = 2
    else:
        agi_need = 3

    menu_grid.grid_left()
    if agi_need == 3:
        menu_grid.grid_left()
    full_menu = False
    if memory.main.get_tidus_slvl() >= agi_need:
        full_menu = True
        menu_grid.grid_left()

    menu_grid.move_and_use()
    menu_grid.sel_sphere("ability", "none")
    if full_menu:
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("speed", "none")
        game_vars.complete_full_kilika_menu()
    menu_grid.use_and_quit()
    # Reorder the party

    if game_vars.rng_seed_num() == 30:
        memory.main.update_formation(Tidus, Yuna, Wakka, full_menu_close=False)
    else:
        memory.main.update_formation(Tidus, Lulu, Wakka, full_menu_close=False)
    equip_scout(full_menu_close=True)


def geneaux():
    open_grid(character=0)

    menu_grid.move_first()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()


def luca_workers():
    open_grid(character=0)

    menu_grid.move_first()
    grid_right()
    grid_right()
    grid_right()
    grid_down()
    grid_down()
    grid_right()

    menu_grid.move_and_use()
    logger.debug(f"s_grid_nodes: {memory.main.s_grid_node_selected()}")
    if memory.main.s_grid_node_selected()[0] == 2:
        logger.info("No early haste")
        early_haste = 0
    else:
        logger.info("Early haste, can haste for Oblitzerator")
        early_haste = 1
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("mana", "none")
    if early_haste == 1:
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("ability", "none")  # Haste

    menu_grid.use_and_quit()
    memory.main.close_menu()
    return early_haste


def late_haste():
    open_grid(character=0)
    menu_grid.move_first()
    grid_right()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("ability", "none")  # Haste
    menu_grid.use_and_quit()


def mrr_grid_1_story():
    open_grid(character=4)
    menu_grid.move_first()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("lv1", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "up")
    wakka_late_menu = True

    menu_grid.use_and_quit()

    memory.main.close_menu()

    game_vars.wakka_late_menu_set(wakka_late_menu)


def mrr_grid_1():
    logger.info("Menuing: start of MRR ")
    if game_vars.story_mode():
        mrr_grid_1_story()
        return
    open_grid(character=4)
    menu_grid.move_first()
    grid_right()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    logger.debug("Determining state of Wakka late menu")
    if memory.main.get_slvl_wakka() < 3:
        wakka_late_menu = True
        logger.debug("Deferring Wakkas remaining grid for later.")
    else:
        wakka_late_menu = False
        logger.debug("Completing Wakkas remaining grid now.")
        menu_grid.use_and_move()
        grid_down()
        grid_down()
        grid_right()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "none")
    logger.debug(f"Wakka late menu (before): {wakka_late_menu}")

    menu_grid.use_and_quit()

    memory.main.close_menu()

    game_vars.wakka_late_menu_set(wakka_late_menu)


def mrr_grid_2_story():
    if memory.main.get_slvl_wakka() >= 3:
        logger.debug("Catching up Wakkas sphere grid.")
        open_grid(character=4)

        menu_grid.move_first()
        grid_left()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "left")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_quit()
        game_vars.wakka_late_menu_set(False)
        logger.debug(f"Wakka late menu updated: {game_vars.wakka_late_menu()}")
    else:
        logger.debug("Wakka: Not enough sphere levels yet.")


def mrr_grid_2():
    if game_vars.story_mode():
        mrr_grid_2_story()
        return
    if memory.main.get_slvl_wakka() >= 7:
        logger.debug("Catching up Wakkas sphere grid.")
        open_grid(character=4)

        menu_grid.move_first()
        grid_right()
        grid_down()
        grid_down()
        grid_down()
        grid_right()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_quit()
        game_vars.wakka_late_menu_set(False)
        logger.debug(f"Wakka late menu updated: {game_vars.wakka_late_menu()}")
    else:
        logger.debug("Wakka: Not enough sphere levels yet.")


def mrr_grid_yuna():
    # Removed thanks to Terra skip, only done during story mode.
    if game_vars.story_mode():
        logger.debug("Yuna levels good to level up.")
        open_grid(character=1)
        menu_grid.use_first()  # Sphere grid on Yuna first
        menu_grid.sel_sphere("magic", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("mana", "none")
        menu_grid.use_and_move()
        grid_right()
        grid_right()
        grid_right()
        grid_right()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("mana", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("mana", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("mana", "none")
        menu_grid.use_and_quit()
    


def battle_site_grid():
    logger.debug("Doing the menu stuff")
    if game_vars.story_mode():
        # Removed if doing to Terra skip
        open_grid(character=1)
        menu_grid.move_first()
        grid_left()
        grid_down()
        grid_down()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("mana", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("speed", "none")

        menu_grid.use_shift_left("Kimahri")  # Sphere grid on Kimahri
    
    else:
        open_grid(character=3)
    menu_grid.move_first()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_quit()

    # Wakkas weapon
    if game_vars.get_l_strike() >= 2:
        equip_weapon(character=4, ability=0x8026, full_menu_close=False)
    else:
        equip_weapon(character=4, full_menu_close=False)
    memory.main.update_formation(Yuna, Wakka, Tidus)


def _navigate_to_position(position, battle_cursor):
    while battle_cursor() == 255:
        pass
    if battle_cursor() != position:
        logger.debug(f"Wrong position targeted {battle_cursor() % 2} {position % 2}")
        while battle_cursor() % 2 != position % 2:
            if battle_cursor() % 2 < position % 2:
                xbox.tap_right()
            else:
                xbox.tap_left()
        while battle_cursor() != position:
            logger.debug(battle_cursor())
            if battle_cursor() > position:
                xbox.tap_up()
            else:
                xbox.tap_down()


def battle_site_equip_sort():
    memory.main.open_menu()
    while memory.main.get_menu_cursor_pos() != 1:
        memory.main.menu_direction(memory.main.get_menu_cursor_pos(), 1, 11)
    xbox.tap_confirm()
    memory.main.wait_frames(15)
    xbox.tap_back()
    memory.main.wait_frames(3)
    xbox.tap_right()
    xbox.tap_right()
    xbox.tap_confirm()  # Equipment
    memory.main.wait_frames(15)
    xbox.tap_right()
    xbox.tap_confirm()  # Auto sort
    memory.main.close_menu()


def battle_site_oaka_1():
    memory.main.click_to_diag_progress(96)
    while memory.main.shop_menu_dialogue_row() != 1:
        xbox.tap_down()
    while memory.main.item_shop_menu() != 7:
        xbox.tap_b()
    while memory.main.assign_ability_to_equip_cursor() != 1:
        xbox.tap_right()
    while memory.main.item_shop_menu() != 21:
        xbox.tap_b()
        if game_vars.use_pause():
            memory.main.wait_frames(2)

    
    item_order = memory.main.get_items_order()
    if memory.main.rng_seed() != 160:
        items_to_sell = [(i, v) for i, v in enumerate(item_order) if v in [0, 1, 2, 8]]
    else:
        items_to_sell = [(i, v) for i, v in enumerate(item_order) if v in [0, 1, 2]]
    logger.debug(items_to_sell)
    for slot, cur_item in items_to_sell:
        logger.debug(f"{slot} {cur_item}")
        _navigate_to_position(slot, memory.main.equip_sell_row)
        cur_amount = memory.main.get_item_count_slot(slot)
        if memory.main.rng_seed() == 160:
            amount_to_sell = max(cur_amount - {0: 0, 1: 0, 2: 0}[cur_item], 0)
        else:
            amount_to_sell = max(cur_amount - {0: 0, 1: 0, 2: 0, 8: 0}[cur_item], 0)
        logger.debug(f"Selling from {cur_amount} to {amount_to_sell}")
        while memory.main.item_shop_menu() != 27:
            xbox.tap_b()
        while memory.main.equip_buy_row() != amount_to_sell:
            if cur_amount == amount_to_sell:
                xbox.tap_up()
            elif memory.main.equip_buy_row() < amount_to_sell:
                xbox.tap_right()
            else:
                xbox.tap_left()
        while memory.main.item_shop_menu() != 21:
            xbox.tap_b()
    
    memory.main.close_menu()


def battle_site_oaka_2():
    FFXC.set_neutral()
    logger.debug("Engage O'aka again")
    memory.main.click_to_diag_progress(74)
    memory.main.click_to_diag_progress(96)
    if memory.main.get_gil_value() < 10890:
        logger.warning("Ready to start selling.")

        from pathing import approach_actor_by_id
        from memory.main import wait_seconds
        approach_actor_by_id(8410)
        FFXC.set_neutral()
        memory.main.wait_seconds(5)
        xbox.tap_confirm()
        memory.main.wait_seconds(3)
        xbox.tap_right()
        xbox.tap_confirm()
        memory.main.wait_seconds(1)
        #logger.debug("Returning for test mode.")
        #quit()
        #exit()
        sell_all(tstrike=False, gil_need=10890)
        logger.warning("Sell complete")
        #all_equipment = memory.main.all_equipment()
        #other_slots = [
        #    i
        #    for i, handle in enumerate(all_equipment)
        #    if (i > 5 and handle.equip_status == 255 and not handle.is_brotherhood())
        #]
        #for cur in other_slots:
        #    sell_weapon(cur)
        #    if memory.main.get_gil_value() >= 10890:
        #        break
    buy_weapon(2, equip=True)
    memory.main.close_menu()


def buy_weapon(location, equip=False):
    while not memory.main.menu_open():
        xbox.tap_b()
    if memory.main.equip_shop_menu() != 12:
        while memory.main.equip_shop_menu() != 9:
            xbox.tap_a()
        while memory.main.item_menu_row() != 0:
            xbox.tap_left()
        while memory.main.equip_shop_menu() != 12:
            xbox.tap_b()
    while memory.main.equip_buy_row() != location:
        if memory.main.equip_buy_row() < location:
            xbox.tap_down()
        else:
            xbox.tap_up()
    while memory.main.equip_shop_menu() != 18:
        xbox.tap_b()
    while memory.main.equip_confirmation_row() != 1:
        pass
    while memory.main.equip_confirmation_row() != 0:
        xbox.tap_up()
    while memory.main.equip_shop_menu() != 22:
        xbox.tap_b()
    if equip:
        while memory.main.equip_sell_row() != 1:
            pass
        while memory.main.equip_sell_row() != 0:
            xbox.tap_up()
    while memory.main.equip_shop_menu() != 12:
        xbox.tap_b()


def sell_weapon(location):
    while not memory.main.menu_open():
        xbox.tap_b()
    if memory.main.equip_shop_menu() != 25:
        while memory.main.equip_shop_menu() != 9:
            xbox.tap_a()
        while memory.main.item_menu_row() != 1:
            xbox.tap_right()
        while memory.main.equip_shop_menu() != 25:
            xbox.tap_b()
    while memory.main.equip_sell_row() != location:
        if memory.main.equip_sell_row() < location:
            xbox.tap_down()
        else:
            xbox.tap_up()
    while memory.main.equip_shop_menu() != 31:
        xbox.tap_b()
    while memory.main.equip_confirmation_row() != 1:
        pass
    while memory.main.equip_confirmation_row() != 0:
        xbox.tap_up()
    logger.debug("Selling")
    while memory.main.equip_shop_menu() != 25:
        xbox.tap_b()


def djose_temple():
    if not game_vars.mrr_skip_val():
        open_grid(character=4)
        menu_grid.move_first()
        grid_right()
        grid_left()
        grid_left()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "up")
        menu_grid.use_and_quit()
        memory.main.close_menu()
    elif game_vars.skip_kilika_luck():
        return
    elif memory.main.get_slvl_wakka() >= 7:
        open_grid(character=4)
        menu_grid.move_first()

        grid_right()
        grid_right()
        grid_right()
        grid_right()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_quit()
        memory.main.close_menu()
    elif memory.main.get_slvl_wakka() == 6:
        open_grid(character=4)
        menu_grid.move_first()

        grid_left()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("Lv1", "none")
        menu_grid.use_and_move()
        grid_left()
        grid_left()
        grid_left()
        grid_left()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_quit()
        memory.main.close_menu()


def djose_temple_old():
    open_grid(character=0)

    # Sphere grid Tidus
    menu_grid.move_first()
    grid_up()
    grid_up()
    grid_up()
    menu_grid.move_and_use()  # Move to Str sphere near Lv.2 lock
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()  # Str +1
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()  # HP +200
    menu_grid.sel_sphere("speed", "none")
    # Now sphere grid on Wakka

    if memory.main.get_slvl_wakka() >= 5:
        menu_grid.use_shift_right("wakka")  # Agi +2
        menu_grid.move_first()

        grid_right()
        grid_left()
        grid_left()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "up")
    menu_grid.use_and_quit()
    memory.main.close_menu()


def kimahri_terra():
    open_grid(character=3)
    menu_grid.move_first()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    #menu_grid.sel_sphere("speed", "none")
    #menu_grid.use_and_use_again()
    menu_grid.sel_sphere("Lv1", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("Lv1", "none")
    menu_grid.use_and_move()
    grid_up()
    grid_up()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("ability", "none")  # Steal
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("ability", "none")  # Use
    menu_grid.use_and_quit()
    memory.main.close_menu()


def t_plains_terra_skip():
    open_grid(character=0)

    # Sphere grid Tidus
    menu_grid.move_first()
    grid_right()
    grid_up()
    menu_grid.move_and_use()  # Move to Str sphere near Lv.2 lock
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()  # Str +1
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()  # HP +200
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()


def yuna_terra_skip_recover():
    # No longer performed.
    '''
    open_grid(character=1)
    menu_grid.move_first()  # Sphere grid on Yuna first
    # Removed due to Terra skip
    # menu_grid.sel_sphere("magic", "none")
    # menu_grid.use_and_use_again()
    # menu_grid.sel_sphere("mana", "none")
    # menu_grid.use_and_move()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    grid_down()
    grid_down()
    grid_down()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    # menu_grid.use_and_quit()
    '''


def m_woods():
    while not memory.main.menu_open():
        xbox.tap_confirm()  # Talking through O'aka's conversation.
    if memory.main.get_gil_value() < 15400:
        memory.main.close_menu()
        if game_vars.story_mode():
            memory.main.wait_seconds(5)
            xbox.tap_confirm()
        else:
            memory.main.click_to_diag_progress(14)
            memory.main.click_to_diag_progress(12)
        while not memory.main.menu_open():
            xbox.tap_confirm()
        if memory.main.get_gil_value() < 11550:
            memory.main.wait_frames(8)
            xbox.menu_right()
            xbox.menu_b()
            memory.main.wait_frames(3)
            sell_all(gil_need=11550)
            xbox.menu_a()
            memory.main.wait_frames(10)
            xbox.menu_left()
            memory.main.wait_frames(2)
    buy_weapon(0, equip=True)
    buy_weapon(3, equip=True)
    memory.main.close_menu()


def m_lake_grid():
    '''
    open_grid(character=1)  # Start with Yuna
    menu_grid.move_first()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    grid_down()
    grid_down()
    grid_down()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    menu_grid.move_and_use()
    xbox.menu_down()
    xbox.menu_down()
    xbox.menu_down()
    menu_grid.sel_sphere("Lv2", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_up()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_shift_left("rikku")  # Shift to Rikku
    '''
    open_grid(character=6)  # With Terra skip, just do Rikku and Kimahri.
    menu_grid.move_first()

    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")

    menu_grid.use_shift_right("kimahri")  # And last is Kimahri (removed for Terra skip)
    menu_grid.move_first()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    #menu_grid.sel_sphere("speed", "none")
    #menu_grid.use_and_use_again()
    menu_grid.sel_sphere("Lv1", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("Lv1", "none")
    menu_grid.use_and_move()
    grid_up()
    grid_up()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("ability", "none")  # Steal
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("ability", "none")  # Use
    menu_grid.use_and_quit()
    memory.main.close_menu()


def mac_temple():
    open_grid(character=0)
    menu_grid.use_first()

    menu_grid.sel_sphere("Lv2", "none")
    menu_grid.use_and_move()
    grid_right()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_up()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_right()
    grid_right()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_right()
    grid_right()
    if game_vars.get_blitz_win():
        menu_grid.move_and_use()
        menu_grid.sel_sphere("strength", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_move()
    grid_left()
    grid_left()
    if game_vars.nemesis():
        grid_up()
        grid_left()
        grid_up()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("strength", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "right")
        menu_grid.use_and_move()
        grid_down()
        grid_right()
        grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    if game_vars.nemesis():
        grid_right()
        grid_down()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("strength", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_move()
        grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    if game_vars.nemesis():
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("strength", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
    
    if not game_vars.story_mode():
        # Add Kimahri for terra skip.
        menu_grid.use_shift_left("Kimahri")
        menu_grid.move_first()
        grid_down()
        grid_down()
        grid_down()
        grid_down()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "none")  # Should be HP +200
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("speed", "none")  # Should be speed +4
    
    
    menu_grid.use_and_quit()

    # if game_vars.get_blitz_win():
    # Should be equipped from Crawler fight.
    #    equip_weapon(character=0, special="brotherhood")
    memory.main.close_menu()


def after_seymour():
    open_grid(character=0)
    menu_grid.move_first()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    if game_vars.nemesis():
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("mp", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_move()
    grid_up()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    if game_vars.nemesis():
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("mp", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()


def home_grid():
    open_grid(character=0)
    menu_grid.move_first()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_quit()



def overworld_use_item(item_to_use: int = 3):
    while not memory.main.menu_open():
        memory.main.open_menu()

    while memory.main.get_menu_cursor_pos() != 1:
        memory.main.menu_direction(memory.main.get_menu_cursor_pos(), 1, 11)
    while memory.main.menu_number() != 26:
        xbox.tap_b()
    mega_pot_slot = memory.main.get_item_slot(item_to_use)
    column = mega_pot_slot % 2
    row = (mega_pot_slot - column) / 2
    logger.debug(f"mega_pot_slot: {mega_pot_slot} column: {column} row: {row}")

    while memory.main.item_menu_column() != column:
        if memory.main.item_menu_column() > column:
            xbox.tap_left()
        else:
            xbox.tap_right()
    while memory.main.item_menu_row() != row:
        if memory.main.item_menu_row() < row:
            xbox.tap_down()
        else:
            xbox.tap_up()

    while memory.main.item_menu_number() != 13:
        xbox.tap_b()
    current_hp = memory.main.get_hp()
    maximal_hp = memory.main.get_max_hp()
    while current_hp != maximal_hp:
        xbox.tap_b()
        current_hp = memory.main.get_hp()


def sort_items(full_menu_close=True):
    while not memory.main.menu_open():
        memory.main.open_menu()
    while memory.main.get_menu_cursor_pos() != 1:
        memory.main.menu_direction(memory.main.get_menu_cursor_pos(), 1, 11)
    while memory.main.menu_number() != 26:
        xbox.tap_b()
    while memory.main.item_menu_number() != 53:
        xbox.tap_a()
    while memory.main.assign_ability_to_equip_cursor() != 1:
        xbox.tap_right()
    while memory.main.item_menu_number() != 25:
        xbox.tap_b()
    while memory.main.equip_buy_row() != 1:
        xbox.tap_right()
    xbox.tap_b()
    if full_menu_close:
        memory.main.close_menu()
    else:
        memory.main.back_to_main_menu()


def equip_weapon(*, character, ability=None, full_menu_close=True, special="none"):
    logger.debug(f"Equipping Weapon with ability {ability}")
    memory.main.await_control()

    weapon_handles = memory.main.weapon_array_character(character)
    #logger.debug(len(weapon_handles))
    for i in range(len(weapon_handles)):
        logger.debug(weapon_handles[i].abilities())
    weapon_num = 255

    abilityarray = []
    if not ability:
        abilityarray = []
    elif isinstance(ability, int):
        abilityarray = [ability]
    elif isinstance(ability, list):
        abilityarray = ability

    for index, current_weapon in enumerate(weapon_handles):
        if special == "brotherhood":
            if current_weapon.abilities() == [0x8063, 0x8064, 0x802A, 0x8000]:
                weapon_num = index
                break
        elif special == "brotherhoodearly":
            if (
                current_weapon.abilities() == [0x8063, 255, 255, 255]
                and current_weapon.slot_count() == 4
            ):
                weapon_num = index
                break
        elif not abilityarray and current_weapon.abilities() == [255, 255, 255, 255]:
            weapon_num = index
            break
        elif all(
            current_weapon.has_ability(cur_ability) for cur_ability in abilityarray
        ):
            weapon_num = index
            break
    logger.debug(f"Weapon is in slot {weapon_num}")
    if weapon_num == 255:
        if full_menu_close:
            memory.main.close_menu()
        else:
            memory.main.back_to_main_menu()
        return False  # Item is no in inventory.

    if memory.main.menu_number() != 26:
        if not memory.main.menu_open():
            memory.main.open_menu()
        while memory.main.get_menu_cursor_pos() != 4:
            memory.main.menu_direction(memory.main.get_menu_cursor_pos(), 4, 11)
        while memory.main.menu_number() == 5:
            xbox.menu_b()
        while not memory.main.menu_number() == 7:
            xbox.menu_b()

        target_pos = memory.main.get_character_index_in_main_menu(character)
        while memory.main.get_char_cursor_pos() != target_pos:
            while memory.main.get_char_cursor_pos() != target_pos:
                memory.main.menu_direction(
                    memory.main.get_char_cursor_pos(),
                    target_pos,
                    len(memory.main.get_order_seven()),
                )
            memory.main.wait_frames(1)
        while memory.main.menu_number() != 26:
            xbox.menu_b()
    while not memory.main.equip_menu_open_from_char():
        xbox.menu_b()

    while memory.main.equip_weap_cursor() != weapon_num:
        if memory.main.equip_weap_cursor() < weapon_num:
            xbox.tap_down()
        else:
            xbox.tap_up()
        if memory.main.equip_weap_cursor() == weapon_num:
            memory.main.wait_frames(2)
    while memory.main.equip_menu_open_from_char():
        xbox.menu_b()

    if full_menu_close:
        memory.main.close_menu()
    else:
        memory.main.back_to_main_menu()

    return True


def equip_sonic_steel(full_menu_close=True):
    return equip_weapon(character=0, ability=32769, full_menu_close=full_menu_close)


def equip_scout(full_menu_close=True):
    return equip_weapon(character=4, ability=0x8022, full_menu_close=full_menu_close)


def equip_armor(*, character, ability=255, slot_count=99, full_menu_close=True):
    logger.debug(f"Equipping Armor with ability {ability}")
    if character == 255:
        return
    memory.main.await_control()

    armor_handles = memory.main.armor_array_character(character)
    logger.debug(len(armor_handles))
    if ability == 99:
        armor_num = len(armor_handles)
    elif len(armor_handles) != 0:
        armor_num = 255

        abilityarray = []
        if not ability:
            abilityarray = []
        elif isinstance(ability, int):
            abilityarray = [ability]
        elif isinstance(ability, list):
            abilityarray = ability
        for index, current_armor in enumerate(armor_handles):
            if not abilityarray and current_armor.abilities() == [255, 255, 255, 255]:
                armor_num = index
                break
            elif all(
                current_armor.has_ability(cur_ability) for cur_ability in abilityarray
            ):
                if slot_count != 99:
                    if slot_count == current_armor.slot_count():
                        armor_num = index
                        break
                else:
                    armor_num = index
                    break
        if armor_num == 255:
            armor_num = len(armor_handles) + 1
    else:
        armor_num = 0

    # logger.debug(f"Armor is in slot {armor_num}")
    if memory.main.menu_number() != 26:
        if not memory.main.menu_open():
            memory.main.open_menu()
        while memory.main.get_menu_cursor_pos() != 4:
            memory.main.menu_direction(memory.main.get_menu_cursor_pos(), 4, 11)
        while memory.main.menu_number() == 5:
            xbox.tap_b()

        target_pos = memory.main.get_character_index_in_main_menu(character)
        while memory.main.get_char_cursor_pos() != target_pos:
            while memory.main.get_char_cursor_pos() != target_pos:
                memory.main.menu_direction(
                    memory.main.get_char_cursor_pos(),
                    target_pos,
                    len(memory.main.get_order_seven()),
                )
            if memory.main.get_char_cursor_pos() == target_pos:
                memory.main.wait_frames(2)
        memory.main.wait_frames(1)
        xbox.menu_b()
        memory.main.wait_frames(9)
        while memory.main.weapon_armor_cursor() != 1:
            while memory.main.weapon_armor_cursor() != 1:
                xbox.tap_down()
            memory.main.wait_frames(2)
        while memory.main.menu_number() != 26:
            xbox.tap_b()
    while not memory.main.equip_menu_open_from_char():
        xbox.tap_b()

    while memory.main.equip_weap_cursor() != armor_num:
        if memory.main.equip_weap_cursor() < armor_num:
            xbox.tap_down()
        else:
            xbox.tap_up()
    while memory.main.equip_menu_open_from_char():
        if memory.main.assign_ability_to_equip_cursor() == 1:
            xbox.tap_up()
        else:
            xbox.tap_b()
        memory.main.wait_frames(2)

    if full_menu_close:
        memory.main.close_menu()
    else:
        memory.main.back_to_main_menu()

    return True


def via_from_battle_site():
    # This assumes pass from parent function via_purifico()
    # It should only be called after Yuna is active on the grid.
    # It assumes we performed gridding before fighting Gui.
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("Lv2", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_up()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")


def via_purifico():
    open_grid(character=2)  # Auron

    menu_grid.move_first()
    grid_right()
    grid_right()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("Lv2", "none")
    menu_grid.use_and_move()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("Lv2", "none")
    menu_grid.use_and_move()
    grid_up()
    grid_up()
    memory.main.wait_frames(30 * 0.3)
    grid_location = memory.main.s_grid_cursor_coords()
    # We have extra levels, changes the path slightly.
    if grid_location != [789,-485]:
        grid_up()
        grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("mana", "none")

    menu_grid.use_shift_right("yuna")  # Switch to Yuna
    #menu_grid.use_first()
    
    # This section updated for terra skip.
    menu_grid.move_first()
    if not game_vars.mrr_skip_val():
        via_from_battle_site()
    
    else:
        grid_up()
        grid_up()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("Lv4", "none")
        menu_grid.use_and_move()
        grid_right()
        grid_right()
        grid_right()
        grid_right()
        grid_left()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
    
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("tele", "up")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("magic", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")

    menu_grid.use_and_move()
    grid_right()
    grid_right()
    grid_right()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("mana", "none")

    menu_grid.use_and_move()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("mana", "none")  # Terra. Used to be str+4

    menu_grid.use_and_move()
    grid_left()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")

    menu_grid.use_and_move()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")

    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("Lv1", "none")
    
    need_completion = True
    if game_vars.mrr_skip_val():
        need_completion = False
        menu_grid.use_and_move()
        grid_right()
        grid_down()
        grid_right()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("speed", "none")
        menu_grid.use_and_move()
        grid_left()
        grid_left()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_move()
        grid_down()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("speed", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("mana", "none")
        
    menu_grid.use_and_quit()
    memory.main.close_menu()
    return need_completion


def via_purifico_noTerra_recovery():
    memory.main.click_to_control_3()
    open_grid(character=1)  # Yuna

    menu_grid.move_first()
    grid_right()
    grid_down()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("mana", "none")
        
    menu_grid.use_and_quit()
    memory.main.close_menu()




def seymour_natus_blitz_win():
    open_grid(character=1)
    yuna_levels = memory.main.get_yuna_slvl()
    logger.warning(f"Sphere levels: {yuna_levels}")
    if yuna_levels <= 9:
        game_vars.update_calm_levels_needed(5)

    menu_grid.use_first()
    menu_grid.sel_sphere("tele", "up2")
    menu_grid.use_and_use_again()

    menu_grid.sel_sphere("power", "none")  # Str
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")  # Str
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")  # Def +3

    menu_grid.use_and_move()
    if game_vars.nemesis():
        grid_up()
        grid_up()
        grid_left()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_move()
        grid_up()
        grid_down()
        grid_down()
    else:
        grid_left()
        grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")

    menu_grid.use_and_move()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    
    if game_vars.nemesis():
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
    
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
        
    '''
    # Removed for Terra skip
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    if game_vars.nemesis() or game_vars.story_mode():
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("mana", "none")
    '''
    menu_grid.use_and_quit()
    memory.main.close_menu()


def seymour_natus_blitz_loss():
    open_grid(character=1)
    yuna_levels = memory.main.get_yuna_slvl()
    logger.warning(f"Sphere levels: {yuna_levels}")
    if yuna_levels <= 9:
        game_vars.update_calm_levels_needed(5)

    menu_grid.use_first()
    menu_grid.sel_sphere("tele", "left")  # Str+4 by mental break
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("friend", "up")  # next to Str+4 and Agi+2
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    
    menu_grid.use_and_move()
    grid_right()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")

    menu_grid.use_and_move()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    
    menu_grid.use_and_move()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")

    menu_grid.use_and_quit()
    memory.main.close_menu()


def prep_calm_lands():
    open_grid(character=1)
    yuna_levels = memory.main.get_yuna_slvl()
    logger.warning(f"Sphere levels: {yuna_levels}")
    if game_vars.get_blitz_win():
        menu_grid.move_first()
        
        # Update for Terra Skip logic
        grid_left()
    
        if game_vars.nemesis():
            menu_grid.move_and_use()
            menu_grid.sel_sphere("power", "none")
            menu_grid.use_and_move()
        grid_left()
        grid_left()
        grid_left()
        menu_grid.move_and_use()
        if game_vars.story_mode():
            memory.main.wait_frames(9)
            logger.warning(memory.main.s_grid_cursor_coords())
        menu_grid.sel_sphere("power", "none")
        
    else:
        menu_grid.move_first()
        '''
        if game_vars.nemesis() or game_vars.story_mode():
            grid_up()
            grid_up()
            grid_left()
            menu_grid.move_and_use()
            menu_grid.sel_sphere("power", "none")
            menu_grid.use_and_move()
            grid_up()
        '''
        grid_left()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()


def after_ronso():
    memory.main.open_menu()
    if game_vars.end_game_version() != 3:
        yuna_first_strike()
        if game_vars.end_game_version() == 4:
            auron_first_strike()
        if not memory.main.equipped_weapon_has_ability(char_num=1, ability_num=0x8001):
            equip_weapon(character=1, ability=0x8001, full_menu_close=False)
        if game_vars.end_game_version() == 4:
            if not memory.main.equipped_weapon_has_ability(char_num=2, ability_num=0x8001):
                equip_weapon(character=2, ability=0x8001, full_menu_close=False)
        if game_vars.use_pause():
            memory.main.wait_frames(5)

    open_grid(character=5)
    menu_grid.move_first()
    grid_up()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("Lv2", "none")
    menu_grid.use_and_move()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("Lv3", "none")
    menu_grid.use_and_move()
    grid_right()
    grid_down()
    grid_down()
    
    if not game_vars.get_blitz_win():
        # Divert blitz loss logic to its own function.
        after_ronso_blitz_loss()
    
    else:
        # Terra add, removed earlier.
        menu_grid.move_shift_left("yuna")
        if game_vars.nemesis():
            menu_grid.use_first()
            menu_grid.sel_sphere("mana", "left")
            menu_grid.use_and_move()
        else:
            menu_grid.move_first()
        while memory.main.s_grid_cursor_coords()[0] > 140:
            grid_left()  # Move to empty node left of HP, or filled with MP in nem route
        if game_vars.nemesis():
            while memory.main.s_grid_cursor_coords()[1] > -1204:
                grid_up()
            menu_grid.move_and_use()
            menu_grid.sel_sphere("mana", "none")
            menu_grid.use_and_move()
        
        while memory.main.s_grid_cursor_coords() != [-30,-1100]:
            if memory.main.s_grid_cursor_coords()[0] > -30:
                grid_left()
            elif memory.main.s_grid_cursor_coords()[1] < -1100:
                grid_down()
            else:
                grid_up()
            #memory.main.wait_frames(6)
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("speed", "none")
        # End Terra add

        if game_vars.end_game_version() == 3:  # Four friend spheres
            menu_grid.use_shift_right("Kimahri")
            menu_grid.move_first()
            grid_down()
            grid_down()
            menu_grid.move_shift_right("Tidus")
            menu_grid.move_first()
            grid_right()
            grid_right()
            grid_right()
            grid_down()
            grid_right()
            grid_right()
            grid_right()
            menu_grid.move_shift_right("Yuna")
            menu_grid.use_first()
            menu_grid.sel_sphere("friend", "none")
            menu_grid.use_and_use_again()
            menu_grid.sel_sphere("power", "none")
        
        # With Terra skip, this logic is now performed for three of four versions.
        if game_vars.end_game_version() in [1, 2, 3]:  # Two of each
            menu_grid.use_and_use_again()
            menu_grid.sel_sphere("friend", "d2")
            menu_grid.use_and_use_again()
            menu_grid.sel_sphere("power", "none")
            menu_grid.use_and_use_again()
            menu_grid.sel_sphere("power", "none")
            menu_grid.use_shift_right("Lulu")
            menu_grid.move_first()
            grid_up()
            grid_up()
            grid_up()
            grid_up()
            menu_grid.move_shift_left("Yuna")
            menu_grid.use_first()
            menu_grid.sel_sphere("friend", "none")
            menu_grid.use_and_use_again()
            menu_grid.sel_sphere("speed", "none")
            menu_grid.use_and_use_again()
            menu_grid.sel_sphere("speed", "none")
            menu_grid.use_and_use_again()
            menu_grid.sel_sphere("power", "none")
        
        if game_vars.end_game_version() == 3:  # Four friend spheres
            # And finally, last of x4 friend spheres to Kimahri
            menu_grid.use_and_use_again()
            menu_grid.sel_sphere("friend", "down")
            menu_grid.use_and_use_again()
            menu_grid.sel_sphere("speed", "none")
            
        # Finally, with Terra, we need armor break.
        menu_grid.use_shift_left("Tidus")
        logger.debug(f"Check version: {game_vars.end_game_version()}")
        if game_vars.end_game_version() == 4:
            menu_grid.move_first()
            grid_right()
            grid_right()
            grid_right()
            grid_down()
            grid_down()
            grid_down()
            grid_down()
            grid_down()
        elif game_vars.end_game_version() == 3:
            menu_grid.move_first()
            grid_down()
            grid_left()
            grid_left()
        else:
            menu_grid.use_first()
            menu_grid.sel_sphere("ret", "tidusver2")
            menu_grid.use_and_move()
            grid_down()
            grid_left()
            grid_left()
    
        # All converge to obtain armor break
        menu_grid.move_and_use()
        menu_grid.sel_sphere("ability", "none")
        
        menu_grid.use_and_quit()
        memory.main.close_menu()

def after_ronso_blitz_loss():
    # Added post Terra
    if game_vars.end_game_version() == 3:
        menu_grid.move_shift_right("Kimahri")
        menu_grid.move_first()
        grid_down()
        grid_down()
        menu_grid.move_shift_right("Tidus")
        menu_grid.move_first()
        grid_right()
        grid_right()
        grid_right()
        grid_down()
        grid_right()
        grid_right()
        grid_right()
        grid_down()
        grid_left()
        grid_left()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("ability", "none")
        menu_grid.use_and_move()
        grid_right()
        grid_down()
        grid_right()
        grid_right()
        grid_down()
        menu_grid.move_shift_right("Yuna")
        menu_grid.move_first()
        grid_right()
        grid_right()
        grid_right()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("friend", "up")  # To Tidus
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "left")
    elif game_vars.end_game_version() == 4:
        menu_grid.move_shift_right("Yuna")
        menu_grid.use_first()
        menu_grid.sel_sphere("ret", "up")
        menu_grid.use_and_move()
        grid_right()
        grid_right()
        grid_right()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")

    else:
        menu_grid.move_shift_right("Yuna")
        menu_grid.move_first()
        grid_right()
        grid_right()
        grid_right()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
    
    # Merge for any drops, Return < 4.
    if game_vars.end_game_version() in [1,2,3]:
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("friend", "d2")  # To Lulu
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_shift_right("Lulu")
        menu_grid.move_first()
        grid_up()
        grid_up()
        grid_up()
        grid_up()
        menu_grid.move_shift_left("Yuna")
        menu_grid.use_first()
        menu_grid.sel_sphere("friend", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("speed", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("speed", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
    
    if game_vars.end_game_version() == 3:
        # Grab agility near Kimahri
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("friend", "down")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("speed", "none")
        menu_grid.move_shift_right("Tidus")
        menu_grid.move_first()
        grid_right()
        grid_left()
        grid_left()
        grid_up()
        grid_left()
        menu_grid.move_and_quit()
    else:
        # Tidus armor break
        menu_grid.move_shift_right("Tidus")
        menu_grid.move_first()
        grid_right()
        grid_right()
        grid_right()
        grid_down()
        grid_down()
        grid_down()
        grid_down()
        grid_down()
        grid_down()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("ability", "none")
        menu_grid.use_and_quit()
    memory.main.close_menu()



def find_equipment_index(*, owner, equipment_type, ability_array=[], slot_count):
    equip_array = memory.main.all_equipment()
    if not ability_array:
        ability_array = [255, 255, 255, 255]
    for current_index, current_handle in enumerate(equip_array):
        if (
            current_handle.owner() == owner
            and current_handle.equipment_type() == equipment_type
            and current_handle.abilities() == ability_array
            and current_handle.slot_count() == slot_count
        ):
            return current_index


def ability_to_customize_ref(ability_index):
    if (
        memory.main.customize_menu_array()[memory.main.assign_ability_to_equip_cursor()]
        == ability_index
    ):
        return True
    return False


def add_ability(
    *,
    owner,
    equipment_type,
    ability_array=[],
    ability_index=255,
    slot_count,
    navigate_to_equip_menu=False,
    exit_out_of_current_weapon=True,
    close_menu=True,
    full_menu_close=True,
):
    if navigate_to_equip_menu:
        if not memory.main.menu_open():
            memory.main.open_menu()
        while memory.main.get_menu_cursor_pos() != 8:
            memory.main.menu_direction(memory.main.get_menu_cursor_pos(), 8, 11)
        while memory.main.menu_number() == 5:
            xbox.menu_b()
    item_to_modify = find_equipment_index(
        owner=owner,
        equipment_type=equipment_type,
        ability_array=ability_array,
        slot_count=slot_count,
    )
    while memory.main.item_menu_row() != item_to_modify:
        if memory.main.item_menu_row() < item_to_modify:
            if item_to_modify - memory.main.item_menu_row() > 9:
                xbox.trigger_r()
            else:
                xbox.tap_down()
        else:
            if (
                memory.main.item_menu_row() - item_to_modify > 5
                and memory.main.item_menu_row() > 8
            ):
                xbox.trigger_l()
            else:
                xbox.tap_up()
    while not memory.main.heal_menu_open():
        xbox.tap_b()
    while not ability_to_customize_ref(ability_index):  # Find the right ability
        xbox.tap_down()
        if game_vars.use_pause():
            memory.main.wait_frames(3)
    while memory.main.information_active():
        xbox.tap_b()
    while memory.main.equip_buy_row() != 1:
        pass
    while memory.main.equip_buy_row() != 0:
        xbox.tap_up()
    while not memory.main.information_active():
        xbox.tap_b()
    if exit_out_of_current_weapon:
        while memory.main.heal_menu_open():
            xbox.menu_a()
            memory.main.wait_frames(1)
    if close_menu:
        if full_menu_close:
            memory.main.close_menu()
        else:
            memory.main.back_to_main_menu()


def add_first_strike(
    *,
    owner,
    equipment_type,
    ability_array=[],
    slot_count,
    navigate_to_equip_menu=False,
    exit_out_of_current_weapon=True,
    close_menu=True,
    full_menu_close=True,
):
    add_ability(
        owner=owner,
        equipment_type=equipment_type,
        ability_array=ability_array,
        ability_index=0x8001,
        slot_count=slot_count,
        navigate_to_equip_menu=navigate_to_equip_menu,
        exit_out_of_current_weapon=exit_out_of_current_weapon,
        close_menu=close_menu,
        full_menu_close=full_menu_close,
    )


def auron_first_strike():
    logger.debug("Starting Auron First Strike")
    close_out = False
    if game_vars.end_game_version() == 4:
        close_out = True
    add_first_strike(
        owner=2,
        equipment_type=0,
        ability_array=[0x800B, 0x8063, 255, 255],
        slot_count=3,
        close_menu=True,
        full_menu_close=close_out,
        navigate_to_equip_menu= not close_out,
    )
    logger.debug("Done with Auron")


def yuna_first_strike():
    logger.debug("Starting Yuna")
    close_out = False
    if game_vars.end_game_version() != 4:
        close_out = True
    if game_vars.nemesis():
        add_first_strike(
            owner=1,
            equipment_type=0,
            ability_array=[0x807A, 255, 255, 255],
            slot_count=2,
            close_menu=close_out,
            navigate_to_equip_menu=True,
        )
    else:
        add_first_strike(
            owner=1,
            equipment_type=0,
            slot_count=1,
            close_menu=close_out,
            navigate_to_equip_menu=True,
        )
    logger.debug("Done with Yuna")


def tidus_slayer(od_pos: int = 2):
    if not memory.main.menu_open():
        memory.main.open_menu()
    while memory.main.get_menu_cursor_pos() != 3:
        xbox.tap_down()
    while memory.main.menu_number() == 5:
        xbox.tap_b()
    memory.main.wait_frames(10)

    # Select Tidus
    while memory.main.get_menu_2_char_num() != 0:
        while memory.main.get_menu_2_char_num() != 0:
            logger.warning(f"Cursor check: {memory.main.get_menu_2_char_num()}")
            xbox.tap_down()
        memory.main.wait_frames(3)
    xbox.tap_b()
    memory.main.wait_frames(10)

    # Change overdrive mode
    xbox.menu_a()
    xbox.tap_right()
    xbox.menu_b()
    xbox.menu_up()
    xbox.menu_up()
    xbox.menu_left()
    
    if od_pos == 2:
        xbox.menu_down()
    elif od_pos == 1:
        xbox.menu_right()
    elif od_pos == 5:
        memory.main.wait_frames(20)
        xbox.menu_right()
        xbox.menu_down()
        xbox.menu_down()

    else:
        xbox.menu_up()
    xbox.menu_b()
    memory.main.close_menu()
    # memory.main.wait_frames(90)  # Testing


def sell_all(nea: bool = False, tstrike: bool = True, gil_need: int = None):
    # Assume already on the sell items screen, index zero
    full_array = memory.main.all_equipment()
    sell_item = True
    sell_row = memory.main.equip_sell_row()  # Starts with first non-equipped equipment.

    with logging_redirect_tqdm():
        with tqdm(total=len(full_array)) as pbar:
            while memory.main.equip_sell_row() + 1 < len(full_array):
                while sell_row != memory.main.equip_sell_row():
                    if sell_row < memory.main.equip_sell_row():
                        xbox.tap_up()
                    else:
                        xbox.tap_down()
                    memory.main.wait_frames(1)
                if memory.main.equip_sell_row() > 8:
                    memory.main.wait_frames(11)
                if full_array[memory.main.equip_sell_row()].is_equipped() != 255:
                    # Currently equipped
                    sell_item = False
                if full_array[memory.main.equip_sell_row()].is_equipped() == 0:
                    # Currently equipped
                    sell_item = False
                if full_array[memory.main.equip_sell_row()].has_ability(0x8056):
                    # Auto-haste
                    sell_item = False
                if full_array[memory.main.equip_sell_row()].has_ability(0x8001):
                    # First Strike
                    sell_item = False
                if full_array[memory.main.equip_sell_row()].has_ability(0x800A):
                    # Auto-Phoenix
                    sell_item = False
                if full_array[memory.main.equip_sell_row()].abilities() == [
                    0x8072,
                    255,
                    255,
                    255,
                ]:
                    # Unmodified armor from the Kilika vendor.
                    # Prevents selling Rikku/Wakka armors if they have them.
                    if full_array[memory.main.equip_sell_row()].owner() in [1, 2, 4, 6]:
                        sell_item = False
                if not nea and full_array[memory.main.equip_sell_row()].has_ability(
                    0x801D
                ):
                    # No-Encounters
                    sell_item = False
                if (
                    not tstrike
                    and full_array[memory.main.equip_sell_row()].has_ability(0x801D)
                    and full_array[memory.main.equip_sell_row()].get_equip_owner()
                    in [0, 4]
                ):
                    sell_item = False  # Don't sell thunder strikes for Tidus/Wakka
                if full_array[memory.main.equip_sell_row()].abilities() == [
                    0x8063,
                    0x8064,
                    0x802A,
                    0x8000,
                ]:
                    # Brotherhood
                    sell_item = False
                if full_array[memory.main.equip_sell_row()].abilities() == [
                    32793, 32783, 32772, 32773,
                ]:
                    # Brotherhood
                    sell_item = False

                if sell_item:
                    xbox.menu_b()
                    memory.main.wait_frames(4)
                    xbox.tap_up()
                    xbox.menu_b()
                    memory.main.wait_frames(4)
                    if memory.main.equipment_sell_prompt_open():
                        xbox.menu_a()
                        memory.main.wait_frames(6)
                    if game_vars.use_pause():
                        memory.main.wait_frames(2)
                else:
                    sell_item = True

                pbar.update(1)
                if gil_need is not None and memory.main.get_gil_value() > gil_need:
                    return
                else:
                    sell_row += 1


def after_flux():  # Possibly no longer used. Needs review.
    open_grid(character=0)

    # Sphere grid on Tidus
    menu_grid.move_first()
    grid_right()
    grid_right()
    grid_right()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("ability", "none")
    menu_grid.use_and_quit()


def gagazet_cave():
    # Occurs after swimming
    memory.main.open_menu()
    xbox.menu_up()
    xbox.menu_up()
    xbox.menu_up()
    xbox.menu_up()
    xbox.menu_b()
    xbox.menu_up()
    xbox.menu_b()
    xbox.menu_down()
    xbox.menu_down()
    xbox.menu_b()  # Yuna to slot 2
    xbox.menu_down()
    xbox.menu_b()
    xbox.menu_down()
    xbox.menu_down()
    xbox.menu_b()  # Auron to slot 3
    memory.main.close_menu()


def zombie_strike_backup():
    open_grid(character=0)

    menu_grid.move_first()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("lv4", "none")
    menu_grid.use_and_move()
    grid_up()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("ability", "none")
    menu_grid.use_and_quit()


def bfa():
    logger.debug(f"Version reminder: {game_vars.end_game_version()}")
    open_grid(character=1)  # Yuna final grid
    if game_vars.end_game_version() in [1,2,4]:
        menu_grid.move_first()
        grid_down()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("speed", "none")
        menu_grid.use_and_move()
        grid_pos = memory.main.s_grid_cursor_coords()
        while grid_pos[0] > -885:
            grid_left()
            logger.debug(f"(A): {grid_pos}")
            grid_pos = memory.main.s_grid_cursor_coords()
        memory.main.wait_frames(6)
        while grid_pos != [-888,643]:
            if grid_pos == [-848,603]:
                grid_left()
            elif grid_pos == [-888,563]:
                grid_left()
            elif grid_pos == [-922,529]:
                grid_left()
            elif grid_pos == [-952,603]:
                grid_down()
            elif grid_pos == [-922,678]:
                grid_right()
            else:
                logger.warning(f"Warning!!! Grid not identified: {grid_pos}")
            memory.main.wait_frames(6)
            grid_pos = memory.main.s_grid_cursor_coords()
            logger.debug(f"(B): {grid_pos}")


        menu_grid.move_and_use()
        menu_grid.sel_sphere("speed", "left")
        menu_grid.use_and_move()
        grid_up()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("ability", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("attribute", "none")
    else:
        menu_grid.use_first()
        menu_grid.sel_sphere("attribute", "right")
        #if game_vars.get_blitz_win():
        #    menu_grid.use_and_use_again()
        #    menu_grid.sel_sphere("ability", "none")
        menu_grid.use_and_move()
        grid_left()
        grid_left()
        grid_left()
        grid_down()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("speed", "none")
        menu_grid.use_and_move()
        grid_down()
        grid_right()
        grid_right()
        grid_right()
        grid_right()
        grid_right()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("speed", "none")
    
    if game_vars.zombie_weapon() == 255:
        menu_grid.use_shift_left("tidus")
        menu_grid.move_first()
        grid_up()
        grid_up()
        grid_up()
        grid_up()
        grid_up()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("lv4", "none")
        menu_grid.use_and_move()
        grid_up()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("ability", "none")


    if memory.main.overdrive_state()[6] != 100:
        menu_grid.use_shift_left("Rikku")
        menu_grid.use_first()
        menu_grid.sel_sphere("skill", "up")


    menu_grid.use_and_quit()
    memory.main.close_menu()

def bfa_pre_Terra():
    open_grid(character=1)  # Yuna final grid

    menu_grid.use_first()

    if game_vars.end_game_version() == 3:
        menu_grid.sel_sphere("attribute", "none")
        menu_grid.use_and_use_again()
    else:
        menu_grid.sel_sphere("attribute", "l8")
        memory.main.wait_frames(30 * 0.07)
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("ret", "torikku")
        memory.main.wait_frames(30 * 0.07)
        menu_grid.use_and_move()
        grid_down()
        grid_down()
        grid_left()
        grid_left()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("speed", "none")
        menu_grid.use_and_move()
        grid_down()
        grid_down()
        grid_down()
        menu_grid.move_and_use()
    menu_grid.sel_sphere("ability", "none")
    menu_grid.use_and_move()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "left")

    if game_vars.end_game_version() == 3:
        menu_grid.use_and_move()
        grid_right()  # Not sure exactly
        grid_right()
        grid_right()
        grid_right()
        grid_right()
        grid_right()
        grid_right()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("speed", "none")
        menu_grid.use_and_move()
        grid_down()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("speed", "none")

    if memory.main.overdrive_state()[6] != 100:
        menu_grid.use_shift_left("Rikku")
        menu_grid.use_first()
        menu_grid.sel_sphere("skill", "up")

    if game_vars.zombie_weapon() == 255:
        menu_grid.use_shift_left("tidus")
        menu_grid.move_first()
        grid_up()
        grid_up()
        grid_up()
        grid_up()
        grid_up()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("lv4", "none")
        menu_grid.use_and_move()
        grid_up()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("ability", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()


def sk_return():
    open_grid(character=1)
    menu_grid.use_first()
    menu_grid.sel_sphere("friend", "d2")
    menu_grid.use_and_use_again()  # Friend sphere to Lulu
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_up()
    grid_up()
    grid_right()
    
    # New with Terra
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    
    if not game_vars.get_skip_zan_luck():
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("luck", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("fortune", "none")
    
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("ret", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("ret", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_quit()


def sk_mixed():
    memory.main.open_menu()
    auron_first_strike()
    if not memory.main.equipped_weapon_has_ability(char_num=2, ability_num=0x8001):
        equip_weapon(character=2, ability=0x8001, full_menu_close=False)
    if game_vars.use_pause():
        memory.main.wait_frames(5)
    open_grid(character=1)
    menu_grid.use_first()
    menu_grid.sel_sphere("bmag", "left_up")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("ret", "up")
    
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    if not game_vars.get_skip_zan_luck():
        menu_grid.sel_sphere("luck", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("fortune", "none")
        menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    
    menu_grid.use_and_move()
    grid_down()
    grid_down()
    #grid_down()
    #grid_down()
    grid_left()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    
    
    menu_grid.use_and_quit()


def sk_friend():
    # First to do the First Strike stuff we couldn't do earlier.
    memory.main.open_menu()
    yuna_first_strike()
    auron_first_strike()
    if not memory.main.equipped_weapon_has_ability(char_num=1, ability_num=0x8001):
        equip_weapon(character=1, ability=0x8001, full_menu_close=False)
    if not memory.main.equipped_weapon_has_ability(char_num=2, ability_num=0x8001):
        equip_weapon(character=2, ability=0x8001, full_menu_close=False)
    if game_vars.use_pause():
        memory.main.wait_frames(5)

    # Now sphere grid
    open_grid(character=1)
    menu_grid.move_first()
    grid_down()
    grid_down()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    grid_right()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("ability", "none")  # Spare Change
    if not game_vars.get_skip_zan_luck():
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("luck", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("fortune", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()


def sk_return_2():
    open_grid(character=1)

    menu_grid.use_first()
    menu_grid.sel_sphere("bmag", "up")
    menu_grid.use_and_use_again()
    if game_vars.get_skip_zan_luck():
        menu_grid.sel_sphere("ret", "left_down")
    else:  # Battle Site adjustment
        menu_grid.sel_sphere("ret", "up")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("mana", "none")
    
    menu_grid.use_and_quit()


def open_grid(character):
    try:
        FFXC.set_neutral()
    except Exception:
        FFXC.set_neutral()
    while not memory.main.s_grid_active():
        if memory.main.user_control() and not memory.main.menu_open():
            xbox.tap_y()
        elif memory.main.menu_number() == 5:  # Cursor on main menu
            while memory.main.get_menu_cursor_pos() != 0:
                memory.main.menu_direction(memory.main.get_menu_cursor_pos(), 0, 11)
            while memory.main.menu_number() == 5:
                xbox.tap_b()
        elif memory.main.menu_number() == 7:  # Cursor selecting party member
            logger.debug("Selecting party member")
            target_pos = memory.main.get_character_index_in_main_menu(character)
            while memory.main.get_char_cursor_pos() != target_pos:
                while memory.main.get_char_cursor_pos() != target_pos:
                    # After B&Y, party size is evaluated weird.
                    if memory.main.get_story_progress() == 2528:
                        memory.main.menu_direction(
                            memory.main.get_char_cursor_pos(), target_pos, 7
                        )
                    elif memory.main.party_size() < 3:
                        xbox.menu_down()
                    else:
                        memory.main.menu_direction(
                            memory.main.get_char_cursor_pos(), target_pos, 7
                        )
                memory.main.wait_frames(1)
            while memory.main.menu_number() == 7:
                xbox.menu_b()
            try:
                FFXC.set_neutral()
            except Exception:
                FFXC.set_neutral()
    try:
        FFXC.set_neutral()
    except Exception:
        FFXC.set_neutral()
    if character != memory.main.s_grid_char():
        while character != memory.main.s_grid_char():
            # Recovers if we opened the grid on the wrong character.
            xbox.shoulder_left()


# ------------------------------
# Nemesis menus


def arena_purchase_1():
    memory.main.wait_frames(60)
    xbox.tap_b()
    memory.main.wait_frames(15)
    xbox.tap_b()  # Tidus catcher
    memory.main.wait_frames(15)
    xbox.tap_up()
    xbox.tap_b()  # Confirm
    memory.main.wait_frames(15)
    xbox.tap_b()  # Do not equip
    memory.main.wait_frames(15)
    xbox.tap_down()
    xbox.tap_b()  # Yuna catcher
    memory.main.wait_frames(15)
    xbox.tap_up()
    xbox.tap_b()  # Confirm
    memory.main.wait_frames(15)
    xbox.tap_up()
    xbox.tap_b()  # Do equip
    memory.main.wait_frames(15)
    xbox.tap_a()
    memory.main.wait_frames(15)
    xbox.tap_a()
    memory.main.wait_frames(15)
    xbox.tap_up()
    xbox.tap_a()
    memory.main.wait_frames(15)
    xbox.tap_b()
    memory.main.wait_frames(60)


def remove_all_nea():
    for i in range(7):
        if memory.main.equipped_armor_has_ability(char_num=i):  # Defaults to NEA
            if i == 0:
                if memory.main.check_ability_armor(ability=0x8056)[i]:
                    equip_armor(character=i, ability=0x8056)  # Auto-Haste
                else:
                    equip_armor(character=i, ability=99)  # Remove equipment
            elif i == 4:
                if memory.main.check_ability_armor(ability=0x800A)[i]:
                    equip_armor(character=i, ability=0x800A)  # Auto-Phoenix
                elif memory.main.check_ability_armor(ability=0x8072, slot_count=4)[i]:
                    equip_armor(character=i, ability=0x8072, slot_count=4) # HP +5% (purchased)
                else:
                    equip_armor(character=i, ability=99)  # Remove equipment
            elif i == 1 and memory.main.check_ability_armor(ability=0x800A)[i]:
                equip_armor(character=i, ability=0x800A)  # Auto-Phoenix
            else:
                equip_armor(character=i, ability=99)  # Unequip
