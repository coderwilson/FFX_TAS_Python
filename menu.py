import logging

import memory.main
import menu_grid
import vars
import xbox

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
    cursor_target = 4
    logger.debug(f"Aiming at {cursor_target}")
    while memory.main.get_menu_cursor_pos() != cursor_target:
        logger.debug(memory.main.get_menu_cursor_pos())
        xbox.tap_up()
    while memory.main.menu_number() == 5:
        xbox.tap_b()
    while memory.main.config_cursor() != 5:
        xbox.tap_up()
    while memory.main.config_aeon_cursor_column() != 1:
        xbox.tap_right()
    while memory.main.config_cursor() != 3:
        xbox.tap_up()
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
    start_node = memory.main.s_grid_node_selected()[0]
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
        game_vars.complete_full_kilik_menu()
    menu_grid.use_and_quit()
    # Reorder the party

    memory.main.full_party_format("kilikawoods1", full_menu_close=False)
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
    logger.debug(f"+++ s_grid_nodes: {memory.main.s_grid_node_selected()}")
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


def mrr_grid_1():
    logger.info("Menuing: start of MRR ")
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


def mrr_grid_2():
    if memory.main.get_slvl_wakka() >= 3:
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
        logger.debug("Not enough sphere levels yet.")


def mrr_grid_yuna():
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
    memory.main.full_party_format("battlesite")


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
    memory.main.click_to_diag_progress(74)
    memory.main.click_to_diag_progress(96)
    if memory.main.get_gil_value() < 10890:
        all_equipment = memory.main.all_equipment()
        other_slots = [
            i
            for i, handle in enumerate(all_equipment)
            if (i > 5 and handle.equip_status == 255 and not handle.is_brotherhood())
        ]
        for cur in other_slots:
            sell_weapon(cur)
            if memory.main.get_gil_value() >= 10890:
                break
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


def m_woods():
    while not memory.main.menu_open():
        xbox.tap_b()  # Talking through O'aka's conversation.
    memory.main.close_menu()
    buy_weapon(0, equip=True)
    memory.main.close_menu()


def m_lake_grid():
    open_grid(character=1)  # Start with Yuna
    menu_grid.move_first()
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
    menu_grid.move_first()

    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")

    menu_grid.use_shift_right("kimahri")  # And last is Yuna
    menu_grid.move_first()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
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
    menu_grid.use_and_quit()

    if game_vars.get_blitz_win():
        equip_weapon(character=0, special="brotherhood")
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

    memory.main.full_party_format("desert1")
    memory.main.close_menu()


def before_guards(item_to_use: int = 3):
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
    logger.debug("@@@@@")
    logger.debug(len(weapon_handles))
    logger.debug("@@@@@")
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
            xbox.tap_b()
        while not memory.main.menu_number() == 7:
            xbox.tap_b()

        target_pos = memory.main.get_character_index_in_main_menu(character)
        while memory.main.get_char_cursor_pos() != target_pos:
            memory.main.menu_direction(
                memory.main.get_char_cursor_pos(),
                target_pos,
                len(memory.main.get_order_seven()),
            )
        while memory.main.menu_number() != 26:
            xbox.tap_b()
    while not memory.main.equip_menu_open_from_char():
        xbox.tap_b()

    while memory.main.equip_weap_cursor() != weapon_num:
        if memory.main.equip_weap_cursor() < weapon_num:
            xbox.tap_down()
        else:
            xbox.tap_up()
    while memory.main.equip_menu_open_from_char():
        xbox.tap_b()

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
    memory.main.await_control()

    armor_handles = memory.main.armor_array_character(character)
    logger.debug("@@@@@")
    logger.debug(len(armor_handles))
    logger.debug("@@@@@")
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

    logger.debug(f"Armor is in slot {armor_num}")
    if memory.main.menu_number() != 26:
        if not memory.main.menu_open():
            memory.main.open_menu()
        while memory.main.get_menu_cursor_pos() != 4:
            memory.main.menu_direction(memory.main.get_menu_cursor_pos(), 4, 11)
        while memory.main.menu_number() == 5:
            xbox.tap_b()

        target_pos = memory.main.get_character_index_in_main_menu(character)
        while memory.main.get_char_cursor_pos() != target_pos:
            memory.main.menu_direction(
                memory.main.get_char_cursor_pos(),
                target_pos,
                len(memory.main.get_order_seven()),
            )
        memory.main.wait_frames(1)
        xbox.tap_b()
        memory.main.wait_frames(18)
        xbox.tap_down()
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
    grid_location = memory.main.s_grid_node_selected()
    # We have extra levels, changes the path slightly.
    if grid_location[0] != 242:
        grid_up()
        grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("mana", "none")

    menu_grid.use_shift_right("yuna")
    menu_grid.use_first()
    menu_grid.sel_sphere("tele", "up")
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
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")

    menu_grid.use_and_move()
    grid_left()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")

    menu_grid.use_and_move()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()


def seymour_natus_blitz_win():
    open_grid(character=1)

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
    if game_vars.nemesis():
        grid_right()
        grid_down()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_move()
        grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    if game_vars.nemesis():
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    if game_vars.nemesis():
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_quit()


def seymour_natus_blitz_loss():
    open_grid(character=1)

    menu_grid.use_first()
    menu_grid.sel_sphere("tele", "left")
    menu_grid.use_and_use_again()

    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")

    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("friend", "left")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    if game_vars.nemesis():
        menu_grid.use_and_move()
        grid_up()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("mana", "none")

    menu_grid.use_and_move()

    grid_right()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    if game_vars.nemesis():
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_move()
    grid_right()
    grid_right()
    grid_right()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
    if game_vars.nemesis():
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_right()
    if game_vars.nemesis():
        grid_right()
        grid_down()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_move()
        grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "left")
    menu_grid.use_and_quit()


def prep_calm_lands():
    open_grid(character=1)
    if game_vars.get_blitz_win():
        menu_grid.move_first()
        grid_up()
        grid_up()
        if game_vars.nemesis():
            menu_grid.move_and_use()
            menu_grid.sel_sphere("mana", "none")
            menu_grid.use_and_move()
        grid_down()
        grid_down()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "none")
    else:
        menu_grid.move_first()
        if game_vars.nemesis():
            grid_up()
            grid_up()
            grid_left()
            menu_grid.move_and_use()
            menu_grid.sel_sphere("power", "none")
            menu_grid.use_and_move()
            grid_up()
        grid_right()
        grid_right()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_quit()
    memory.main.close_menu()


def after_ronso():
    if game_vars.end_game_version() != 3:
        memory.main.open_menu()
        yuna_first_strike()
        auron_first_strike()
        if not memory.main.equipped_weapon_has_ability(char_num=1, ability_num=0x8001):
            equip_weapon(character=1, ability=0x8001, full_menu_close=False)
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

    if game_vars.end_game_version() in [1, 2]:  # Two of each
        menu_grid.move_shift_left("yuna")
        menu_grid.use_first()
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

    elif game_vars.end_game_version() == 4:  # Four return spheres
        menu_grid.move_shift_left("yuna")
        menu_grid.use_first()
        if game_vars.get_blitz_win():
            menu_grid.sel_sphere("ret", "yunaspec")
        else:
            menu_grid.sel_sphere("ret", "d5")
        menu_grid.use_and_move()
        grid_left()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("Lv1", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("mana", "none")
        menu_grid.use_and_move()
        grid_right()
        grid_down()
        grid_right()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("speed", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")

    elif game_vars.end_game_version() == 3:  # Four friend spheres
        if game_vars.get_blitz_win():
            logger.debug("Four friend spheres, Blitz Win")
            menu_grid.move_shift_right("tidus")
            menu_grid.move_first()
            grid_right()
            grid_right()
            grid_right()
            grid_down()
            grid_right()
            grid_right()
            grid_right()
            menu_grid.move_shift_right("yuna")
            menu_grid.use_first()
            menu_grid.sel_sphere("friend", "after_by_spec")
            menu_grid.use_and_use_again()
            menu_grid.sel_sphere("power", "none")
            menu_grid.use_shift_left("tidus")
            menu_grid.move_first()
            grid_down()
            grid_left()
            grid_left()
            menu_grid.move_and_use()
            menu_grid.sel_sphere("ability", "none")
            menu_grid.move_shift_right("yuna")
        else:
            logger.debug("Four friend spheres, Blitz Loss")
            menu_grid.move_shift_right("tidus")
            menu_grid.move_first()
            grid_right()
            grid_right()
            grid_right()
            grid_down()
            grid_down()
            grid_down()
            grid_down()
            grid_down()
            grid_right()
            grid_down()
            menu_grid.move_and_use()
            menu_grid.sel_sphere("ability", "none")
            menu_grid.use_and_move()
            grid_right()
            grid_right()
            grid_down()
            menu_grid.move_shift_right("yuna")
            menu_grid.use_first()
            menu_grid.sel_sphere("friend", "after_by_spec")
            menu_grid.use_and_use_again()
            menu_grid.sel_sphere("power", "left")

        # Now to replicate the 2/2 split grid
        menu_grid.use_first()
        menu_grid.sel_sphere("friend", "d2")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_shift_left("Lulu")
        menu_grid.move_first()
        grid_up()
        grid_up()
        grid_up()
        grid_up()
        menu_grid.move_shift_right("Yuna")
        menu_grid.use_first()
        menu_grid.sel_sphere("friend", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("speed", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("speed", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")

        # Last, to get some Rikku stuff early.
        menu_grid.move_shift_right("Rikku")
        menu_grid.move_first()
        grid_down()
        grid_down()
        grid_down()
        grid_left()
        grid_left()
        grid_left()
        menu_grid.move_shift_right("Yuna")
        menu_grid.use_first()
        menu_grid.sel_sphere("friend", "l2")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("speed", "none")
        if game_vars.get_blitz_win():
            menu_grid.use_and_use_again()
            menu_grid.sel_sphere("mana", "none")
        menu_grid.use_and_move()
        grid_left()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("power", "none")

    menu_grid.use_and_quit()
    memory.main.close_menu()


def find_equipment_index(*, owner, equipment_type, ability_array=[], slot_count):
    equip_array = memory.main.all_equipment()
    logger.debug(
        f"Find equipment index, owner: {owner} type: {equipment_type} arr: {ability_array} slot_count: {slot_count}"
    )
    if not ability_array:
        ability_array = [255, 255, 255, 255]
    # auron baroque sword - [0x800B, 0x8063, 255, 255]
    logger.debug(f"Looking for: {ability_array}")
    for current_index, current_handle in enumerate(equip_array):
        logger.debug(
            f"Slot: {current_index} | Owner: {current_handle.owner()} | Abilities: {current_handle.abilities()} | Slots: {current_handle.slot_count()}"
        )
        if (
            current_handle.owner() == owner
            and current_handle.equipment_type() == equipment_type
            and current_handle.abilities() == ability_array
            and current_handle.slot_count() == slot_count
        ):
            logger.debug(f"Equipment found in slot: {current_index}")
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
            xbox.tap_b()
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
    while not memory.main.cure_menu_open():
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
        while memory.main.cure_menu_open():
            xbox.tap_a()
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
    logger.debug("Starting Auron")
    add_first_strike(
        owner=2,
        equipment_type=0,
        ability_array=[0x800B, 0x8063, 255, 255],
        slot_count=3,
        close_menu=True,
        full_menu_close=False,
        navigate_to_equip_menu=False,
    )
    logger.debug("Done with Auron")


def yuna_first_strike():
    logger.debug("Starting Yuna")
    if game_vars.nemesis():
        add_first_strike(
            owner=1,
            equipment_type=0,
            ability_array=[0x807A, 255, 255, 255],
            slot_count=2,
            close_menu=False,
            navigate_to_equip_menu=True,
        )
    else:
        add_first_strike(
            owner=1,
            equipment_type=0,
            slot_count=1,
            close_menu=False,
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
    xbox.tap_b()
    memory.main.wait_frames(10)
    xbox.menu_a()
    xbox.tap_right()
    xbox.menu_b()
    if od_pos == 2:
        xbox.menu_down()
    else:
        xbox.menu_up()
    xbox.menu_b()
    memory.main.close_menu()


def sell_all(nea=False):
    # Assume already on the sell items screen, index zero
    full_array = memory.main.all_equipment()
    sell_item = True
    xbox.menu_up()
    memory.main.wait_frames(9)
    while memory.main.equip_sell_row() + 1 < len(full_array):
        xbox.menu_down()
        memory.main.wait_frames(9)
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
        if full_array[memory.main.equip_sell_row()].abilities() == [
            0x8072,
            255,
            255,
            255,
        ]:
            # Unmodified armor from the Kilika vendor. Prevents selling Rikku/Wakka armors if they have them.
            if full_array[memory.main.equip_sell_row()].owner() in [1, 2, 4, 6]:
                sell_item = False
        if not nea and full_array[memory.main.equip_sell_row()].has_ability(0x801D):
            # No-Encounters
            sell_item = False
        if full_array[memory.main.equip_sell_row()].abilities() == [
            0x8063,
            0x8064,
            0x802A,
            0x8000,
        ]:
            # Brotherhood
            sell_item = False

        if sell_item:
            xbox.menu_b()
            xbox.tap_up()
            xbox.menu_b()
            memory.main.wait_frames(1)
        else:
            sell_item = True


def after_flux():
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
    open_grid(character=1)  # Yuna final grid

    menu_grid.use_first()

    if game_vars.end_game_version() == 3:
        menu_grid.sel_sphere("attribute", "none")
        menu_grid.use_and_use_again()
    else:
        menu_grid.sel_sphere("attribute", "l5")
        memory.main.wait_frames(30 * 0.07)
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("ret", "torikku")
        memory.main.wait_frames(30 * 0.07)
        menu_grid.use_and_move()
        grid_down()
        grid_down()
        grid_left()
        grid_down()
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
    if not game_vars.get_skip_zan_luck():
        menu_grid.use_and_use_again()  # Friend sphere to Lulu
        menu_grid.sel_sphere("luck", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("fortune", "none")
    if memory.main.get_power() >= 1:
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
    if memory.main.get_power() >= 1:
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_up()
    grid_up()
    grid_up()
    grid_up()
    menu_grid.move_and_use()
    if memory.main.get_power() >= 1:
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_quit()


def sk_mixed():
    open_grid(character=1)
    menu_grid.use_first()
    menu_grid.sel_sphere("ret", "r2")
    menu_grid.use_and_move()  # Return to Wakkas grid
    grid_left()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("mana", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("lv1", "none")
    if not game_vars.get_skip_zan_luck():
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("luck", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("fortune", "none")
    menu_grid.use_and_move()
    grid_right()
    grid_down()
    grid_right()
    menu_grid.move_and_use()
    if memory.main.get_power() >= 1:
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_move()
    grid_left()
    grid_left()
    menu_grid.move_and_use()
    if memory.main.get_power() >= 1:
        menu_grid.sel_sphere("power", "none")
        menu_grid.use_and_use_again()
    menu_grid.sel_sphere("speed", "none")
    if memory.main.get_power() >= 1:
        menu_grid.use_and_move()
        grid_down()
        menu_grid.move_and_use()
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
    if not game_vars.get_skip_zan_luck():
        open_grid(character=1)
        menu_grid.move_first()
        grid_down()
        grid_down()
        menu_grid.move_and_use()
        menu_grid.sel_sphere("luck", "none")
        menu_grid.use_and_use_again()
        menu_grid.sel_sphere("fortune", "none")
        menu_grid.use_and_quit()
    memory.main.close_menu()


def sk_return_2():
    open_grid(character=1)

    menu_grid.use_first()
    menu_grid.sel_sphere("ret", "aftersk")
    menu_grid.use_and_move()
    grid_right()
    grid_right()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("speed", "none")
    menu_grid.use_and_use_again()
    menu_grid.sel_sphere("power", "none")
    menu_grid.use_and_move()
    grid_down()
    menu_grid.move_and_use()
    menu_grid.sel_sphere("power", "none")
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
            elif i in [4, 6]:
                if memory.main.check_ability_armor(ability=0x800A)[i]:
                    equip_armor(character=i, ability=0x800A)  # Auto-Phoenix
                elif memory.main.check_ability_armor(ability=0x8072, slot_count=4)[i]:
                    equip_armor(character=i, ability=0x8072, slot_count=4)
                else:
                    equip_armor(character=i, ability=99)  # Remove equipment
            else:
                equip_armor(character=i, ability=99)  # Unequip
