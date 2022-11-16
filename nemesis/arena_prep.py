import logging

import battle.boss
import battle.main
import memory.main
import menu
import nemesis.arena_select
import nemesis.menu
import nemesis.nemesis_pathing
import rng_track
import save_sphere
import screen
import vars
import xbox

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()
FFXC = xbox.controller_handle()
test_mode = False

# The following functions extend the regular Bahamut run. Farming sections.


def auto_life():
    while not (memory.main.turn_ready() and screen.turn_tidus()):
        if memory.main.turn_ready():
            if screen.turn_aeon():
                battle.main.attack("none")
            elif not screen.turn_tidus():
                battle.main.defend()
    while memory.main.battle_menu_cursor() != 22:
        if screen.turn_tidus() == False:
            logger.debug("Attempting Auto-life, but it's not Tidus's turn")
            xbox.tap_up()
            xbox.tap_up()
            return
        if memory.main.battle_menu_cursor() == 1:
            xbox.tap_up()
        else:
            xbox.tap_down()
    while not memory.main.other_battle_menu():
        xbox.tap_b()
    battle.main._navigate_to_position(1)
    while memory.main.other_battle_menu():
        xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()


# Default to Besaid. Maybe based on map number?
def air_ship_destination(dest_num=0, force_omega=False):
    if len(memory.main.all_equipment()) > 120:
        rin_equip_dump()
    while memory.main.get_coords()[0] < -257:
        nemesis.nemesis_pathing.set_movement([-258, 345])
    while not memory.main.get_map() in [382, 999]:
        if memory.main.user_control():
            nemesis.nemesis_pathing.set_movement([-251, 340])
        else:
            FFXC.set_neutral()
        xbox.menu_b()
    while memory.main.diag_progress_flag() != 4:
        xbox.tap_b()
    logger.debug("Destination select on screen now.")
    while memory.main.map_cursor() != dest_num:
        if dest_num < 8:
            xbox.tap_down()
        else:
            xbox.tap_up()
    xbox.tap_b()
    memory.main.wait_frames(2)
    xbox.tap_b()
    while not memory.main.user_control():
        if memory.main.cutscene_skip_possible():
            xbox.skip_scene()
        elif memory.main.diag_skip_possible():
            xbox.tap_b()
    if test_mode:
        memory.main.set_game_speed(set_val=1)


def unlock_omega():
    while not memory.main.get_map() in [382, 999]:
        if memory.main.user_control():
            nemesis.nemesis_pathing.set_movement([-251, 340])
        else:
            FFXC.set_neutral()
        if memory.main.diag_progress_flag() == 4:
            xbox.menu_a()
        else:
            xbox.menu_b()
    while memory.main.diag_progress_flag() != 3:
        xbox.tap_up()
    while memory.main.diag_progress_flag() != 0:
        xbox.tap_b()

    while memory.main.diag_progress_flag() == 0:
        logger.debug(f"{memory.main.get_coords()}")
        if memory.main.get_coords()[0] < 65:
            FFXC.set_value("d_pad", 8)
        elif memory.main.get_coords()[0] < 70:
            nemesis.menu.grid_right()
        elif memory.main.get_coords()[0] > 78:
            FFXC.set_value("d_pad", 4)
        elif memory.main.get_coords()[0] > 73:
            nemesis.menu.grid_left()
        elif memory.main.get_coords()[1] > -28:
            FFXC.set_value("d_pad", 2)
        elif memory.main.get_coords()[1] > -34:
            nemesis.menu.grid_down()
        elif memory.main.get_coords()[1] < -40:
            FFXC.set_value("d_pad", 1)
        elif memory.main.get_coords()[1] < -37:
            nemesis.menu.grid_up()
        else:
            xbox.menu_b()
    memory.main.wait_frames(30)
    xbox.menu_b()
    while not memory.main.get_map() in [194, 374]:
        xbox.menu_a()


def get_save_sphere_details():
    return memory.main.get_save_sphere_details()


def return_to_airship():
    logger.debug("Attempting Return to Airship")
    if test_mode:
        memory.main.set_game_speed(set_val=0)

    ss_details = get_save_sphere_details()

    if memory.main.get_map() == 307:  # Monster arena
        while not nemesis.nemesis_pathing.set_movement([-4, -3]):
            pass

    save_sphere.approach_save_sphere()
    FFXC.set_neutral()
    while memory.main.save_menu_cursor() != 1:
        FFXC.set_neutral()
        xbox.menu_down()
        memory.main.wait_frames(1)
    xbox.menu_b()
    memory.main.await_control()
    logger.debug("Return to Airship Complete.")
    memory.main.clear_save_menu_cursor()
    memory.main.clear_save_menu_cursor_2()


def battle_farm_all(ap_cp_limit: int = 255, yuna_attack=True, fayth_cave=True):
    logger.debug(f"Battle Start: {memory.main.get_encounter_id()}")
    FFXC.set_neutral()
    if fayth_cave == True and memory.main.battle_type() == 2:
        screen.await_turn()
        battle.main.flee_all()
    else:
        while memory.main.battle_active():
            if memory.main.turn_ready():
                if screen.turn_tidus():
                    if memory.main.get_encounter_id() in [154, 156, 164]:
                        # Confusion is a dumb mechanic in this game.
                        battle.main.attack_by_num(22, "l")
                    elif memory.main.get_encounter_id() == 281:
                        battle.main.attack_by_num(22, "r")
                    elif memory.main.get_encounter_id() == 283:
                        battle.main.attack_by_num(21, "u")
                    elif memory.main.get_encounter_id() == 284:
                        battle.main.attack_by_num(23, "d")
                    else:
                        battle.main.attack("none")
                elif screen.turn_yuna():
                    if yuna_attack:
                        if memory.main.get_encounter_id() in [154, 156, 164]:
                            # Confusion is a dumb mechanic in this game.
                            battle.main.attack_by_num(22, "l")
                        elif memory.main.get_encounter_id() == 281:
                            battle.main.attack_by_num(21, "l")
                        elif memory.main.get_encounter_id() == 283:
                            battle.main.attack_by_num(22, "d")
                        elif memory.main.get_encounter_id() == 284:
                            battle.main.attack_by_num(22, "d")
                        else:
                            battle.main.attack("none")
                    else:
                        battle.main.escape_one()
                elif screen.turn_rikku() or screen.turn_wakka():
                    if memory.main.battle_type() == 2:
                        battle.main.escape_one()
                    elif not battle.main.check_tidus_ok():
                        battle.main.escape_one()
                    elif memory.main.get_encounter_id() == 219:
                        battle.main.escape_one()
                    else:
                        battle.main.defend()
                else:
                    battle.main.escape_one()
    memory.main.click_to_control()
    if memory.main.get_hp()[0] < 1100:
        battle.main.heal_up(3)
    nemesis.menu.perform_next_grid(limit=ap_cp_limit)


def advanced_complete_check():
    encounter_id = memory.main.get_encounter_id()
    arena_array = memory.main.arena_array()
    # Common monsters
    if False:
        pass

    # Inside Sin
    elif encounter_id == 374:  # Ahriman
        logger.debug(f"For this battle, count:{arena_array[37]}")
        if arena_array[37] == 10:
            return True
    elif encounter_id in [375, 380]:  # Exoray (with a bonus Ahriman)
        logger.debug(f"For this battle, count:{arena_array[93]}")
        if arena_array[93] == 10 and arena_array[37] == 10:
            return True
    elif encounter_id in [376, 381]:  # Adamantoise
        logger.debug(f"For this battle, count:{arena_array[81]}")
        if arena_array[81] == 10:
            return True
    elif encounter_id in [377, 382]:  # Both kinds of Gemini
        logger.debug(f"For this battle, count:{arena_array[77]}")
        logger.debug(f"For this battle, count:{arena_array[78]}")
        if arena_array[77] == 10 and arena_array[78] == 10:
            return True
    elif encounter_id in [378, 384]:  # Behemoth King
        logger.debug(f"For this battle, count:{arena_array[70]}")
        if arena_array[70] == 10:
            return True
    elif encounter_id == 383:  # Demonolith
        logger.debug(f"For this battle, count:{arena_array[75]}")
        if arena_array[75] == 10:
            return True
    elif encounter_id == 385:  # Great Malboro
        logger.debug(f"For this battle, count:{arena_array[56]}")
        if arena_array[56] == 10:
            return True
    elif encounter_id == 386:  # Barbatos
        logger.debug(f"For this battle, count:{arena_array[90]}")
        if arena_array[90] == 10:
            return True
    elif encounter_id == 387:  # Wraith
        logger.debug(f"For this battle, count:{arena_array[97]}")
        if arena_array[97] == 10:
            return True

    # Omega dungeon
    elif encounter_id == 421:  # Master Coeurl and Floating Death
        logger.debug(f"For this battle, count:{arena_array[74]}")
        logger.debug(f"For this battle, count:{arena_array[102]}")
        if arena_array[74] == 10 and arena_array[102] == 10:
            return True
    elif encounter_id == 422:  # Halma and Spirit
        logger.debug(f"For this battle, count:{arena_array[96]}")
        logger.debug(f"For this battle, count:{arena_array[101]}")
        if arena_array[96] == 10 and arena_array[101] == 10:
            return True
    elif encounter_id == 423:  # Zaurus and Floating Death
        logger.debug(f"For this battle, count:{arena_array[100]}")
        logger.debug(f"For this battle, count:{arena_array[102]}")
        if arena_array[100] == 10 and arena_array[102] == 10:
            return True
    elif encounter_id == 424:  # Black Element and Spirit
        logger.debug(f"For this battle, count:{arena_array[67]}")
        logger.debug(f"For this battle, count:{arena_array[96]}")
        if arena_array[67] == 10 and arena_array[96] == 10:
            return True
    elif encounter_id == 425:  # Varuna
        logger.debug(f"For this battle, count:{arena_array[82]}")
        if arena_array[82] == 10:
            return True
    elif encounter_id == 426:  # Master Tonberry
        logger.debug(f"For this battle, count:{arena_array[99]}")
        if arena_array[99] == 10:
            return True
    elif encounter_id == 428:  # Machea (blade thing)
        logger.debug(f"For this battle, count:{arena_array[103]}")
        if arena_array[103] == 10:
            return True
    elif encounter_id == 430:  # Demonolith x2
        logger.debug(f"For this battle, count:{arena_array[75]}")
        if arena_array[75] == 10:
            return True
    elif encounter_id in [432, 433, 434, 435, 436]:  # Just Zaurus
        logger.debug(f"For this battle, count:{arena_array[100]}")
        if arena_array[100] == 10:
            return True
    elif encounter_id == 437:  # Puroboros
        logger.debug(f"For this battle, count:{arena_array[95]}")
        if arena_array[95] == 10:
            return True
    elif encounter_id == 438:  # Wraith
        logger.debug(f"For this battle, count:{arena_array[97]}")
        if arena_array[97] == 10:
            return True

    # Other
    if encounter_id in [429, 445]:
        # Rock monsters, just leave.
        return True
    if encounter_id == 383:
        # Demonolith inside Sin, not worth.
        return True
    if encounter_id == 427:
        # Adamantoise in Omega, dealt with inside Sin
        return True

    return False


def advanced_battle_logic():
    logger.debug(f"Battle Start: {memory.main.get_encounter_id()}")
    logger.debug(f"Ambush flag (2 is bad):{memory.main.battle_type()}")
    while not memory.main.turn_ready():
        pass
    auto_life_used = False
    FFXC.set_neutral()

    if memory.main.battle_type() == 2:
        logger.debug("Ambushed! Escaping!")
        battle.main.tidus_flee()
    elif advanced_complete_check():
        logger.debug("Complete collecting this monster.")
        battle.main.tidus_flee()
    else:
        if memory.main.get_encounter_id() == 449:
            # Omega himself, not yet working.
            aeon_complete = False
            while memory.main.battle_active():
                if memory.main.turn_ready():
                    if screen.turn_rikku():
                        if not aeon_complete:
                            battle.main.buddy_swap_yuna()
                            battle.main.aeon_summon(4)
                        else:
                            battle.main.defend()
                    elif screen.turn_yuna():
                        battle.main.buddy_swap_rikku()
                    elif screen.turn_tidus():
                        battle.main.use_skill(1)  # Quick hit
                    else:
                        battle.main.defend()
        else:
            logger.debug(f"Regular battle:{memory.main.get_encounter_id()}")
            sleep_powder = False
            while memory.main.battle_active():
                encounter_id = memory.main.get_encounter_id()
                if memory.main.turn_ready():
                    if encounter_id in [442]:
                        # Damned malboros in Omega
                        battle.main.buddy_swap_yuna()
                        battle.main.aeon_summon(4)
                        battle.main.attack("none")
                    elif screen.turn_tidus():
                        if (
                            memory.main.get_encounter_id() in [386]
                            and not auto_life_used
                        ):
                            auto_life()
                            auto_life_used = True
                        elif (
                            encounter_id == 383
                            and memory.main.get_enemy_current_hp()[0] > 9999
                        ):
                            if memory.main.get_use_items_slot(41) < 100:
                                battle.main.use_item_tidus(
                                    memory.main.get_use_items_slot(41)
                                )
                            else:
                                battle.main.use_skill(1)
                        elif (
                            encounter_id == 426
                            and memory.main.get_enemy_current_hp()[0] > 9999
                        ):
                            if memory.main.get_use_items_slot(41) < 100:
                                battle.main.use_item_tidus(
                                    memory.main.get_use_items_slot(41)
                                )
                            else:
                                battle.main.use_skill(1)
                        elif (
                            encounter_id == 430
                            and memory.main.get_enemy_current_hp()[0] > 9999
                        ):
                            if memory.main.get_use_items_slot(41) < 100:
                                battle.main.use_item_tidus(
                                    memory.main.get_use_items_slot(41)
                                )
                            else:
                                battle.main.use_skill(1)
                        elif (
                            encounter_id == 437
                            and memory.main.get_enemy_current_hp()[0] > 9999
                        ):
                            if memory.main.get_use_items_slot(41) < 100:
                                battle.main.use_item_tidus(
                                    memory.main.get_use_items_slot(41)
                                )
                            else:
                                battle.main.use_skill(1)
                        elif encounter_id == 431:
                            battle.main.tidus_flee()
                        else:
                            battle.main.use_skill(1)  # Quick hit
                    elif screen.turn_rikku():
                        if encounter_id in [377, 382]:
                            logger.debug(
                                "Shining Gems for Gemini, better to save other items for other enemies."
                            )
                            # Double Gemini, two different locations
                            if memory.main.get_use_items_slot(42) < 100:
                                battle.main.use_item(
                                    memory.main.get_use_items_slot(42), rikku_flee=True
                                )
                            else:
                                battle.main.defend()
                        elif encounter_id == 386:
                            # Armor bomber guys
                            if memory.main.get_use_items_slot(41) < 100:
                                battle.main.use_item(
                                    memory.main.get_use_items_slot(41), rikku_flee=True
                                )
                            else:
                                battle.main.defend()
                        elif encounter_id in [430]:
                            # Demonolith
                            if memory.main.get_use_items_slot(41) < 100:
                                battle.main.use_item(
                                    memory.main.get_use_items_slot(41), rikku_flee=True
                                )
                            else:
                                battle.main.defend()
                        elif encounter_id == 422:
                            # Provoke on Spirit
                            battle.main.use_special(
                                position=3, target=21, direction="u"
                            )
                            if memory.main.get_use_items_slot(41) < 100:
                                battle.main.use_item(
                                    memory.main.get_use_items_slot(41), rikku_flee=True
                                )
                            else:
                                battle.main.defend()
                        elif encounter_id == 424:
                            # Provoke on Spirit
                            battle.main.use_special(
                                position=3, target=21, direction="r"
                            )
                        elif (
                            encounter_id == 425
                            and memory.main.get_enemy_current_hp()[0] > 9999
                        ):
                            # Varuna, use purifying salt to remove haste
                            # Safety potions are fun.
                            battle.main.use_item(
                                memory.main.get_use_items_slot(63), rikku_flee=True
                            )
                        elif encounter_id == 426:
                            # Master Tonberry
                            if not sleep_powder:
                                battle.main.use_item(
                                    memory.main.get_use_items_slot(37), rikku_flee=True
                                )
                            else:
                                if memory.main.get_use_items_slot(41) < 100:
                                    battle.main.use_item_tidus(
                                        memory.main.get_use_items_slot(41)
                                    )
                                else:
                                    battle.main.defend()
                        elif encounter_id == 431:
                            battle.main.tidus_flee()
                        elif (
                            encounter_id == 437
                            and memory.main.get_enemy_current_hp()[0] > 9999
                        ):
                            if not sleep_powder:
                                battle.main.use_item(
                                    memory.main.get_use_items_slot(37), rikku_flee=True
                                )
                            else:
                                if memory.main.get_use_items_slot(41) < 100:
                                    battle.main.use_item_tidus(
                                        memory.main.get_use_items_slot(41)
                                    )
                                else:
                                    battle.main.defend()
                        else:
                            battle.main.defend()
                    else:
                        battle.main.escape_one()
    memory.main.click_to_control()
    memory.main.full_party_format("initiative")
    nemesis.menu.perform_next_grid()
    if memory.main.get_hp()[0] < 1100:
        battle.main.heal_up(3)


def bribe_battle(spare_change_value: int = 12000):
    logger.debug(f"value (2): {spare_change_value}")
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if screen.turn_lulu():
                while memory.main.battle_menu_cursor() != 20:
                    if memory.main.battle_menu_cursor() == 255:
                        xbox.tap_down()
                    elif memory.main.battle_menu_cursor() == 0:
                        xbox.tap_down()
                    else:
                        xbox.tap_up()
                while not memory.main.other_battle_menu():
                    xbox.tap_b()
                battle.main._navigate_to_position(0)
                while memory.main.other_battle_menu():
                    xbox.tap_b()
                battle.main.calculate_spare_change_movement(spare_change_value)

                while memory.main.spare_change_open():
                    xbox.tap_b()
                battle.main.tap_targeting()
            else:
                battle.main.buddy_swap_lulu()
    logger.debug("Battle is complete.")
    while not memory.main.menu_open():
        pass
    FFXC.set_value("btn_b", 1)
    memory.main.wait_frames(150)
    FFXC.set_value("btn_b", 0)
    logger.debug("Now back in control.")


def arena_npc():
    memory.main.await_control()
    if memory.main.get_map() != 307:
        return
    while not (
        memory.main.diag_progress_flag() == 74 and memory.main.diag_skip_possible()
    ):
        if memory.main.user_control():
            if memory.main.get_coords()[1] > -12:
                FFXC.set_movement(0, -1)
                memory.main.wait_frames(1)
            else:
                nemesis.nemesis_pathing.set_movement([2, -15])
                xbox.tap_b()
        else:
            FFXC.set_neutral()
            if memory.main.diag_progress_flag() == 59:
                xbox.menu_a()
                xbox.menu_a()
                xbox.menu_a()
                xbox.tap_b()
            elif memory.main.diag_skip_possible():
                xbox.tap_b()
    logger.debug("Mark 1")
    memory.main.wait_frames(3)  # This buffer can be improved later.
    logger.debug("Mark 2")


def arena_return(checkpoint: int = 0):
    if checkpoint == 0:
        air_ship_destination(dest_num=12)

    while memory.main.get_map() != 307:
        if memory.main.user_control():
            if checkpoint == 2:
                while memory.main.user_control():
                    nemesis.nemesis_pathing.set_movement([-641, -268])
                    xbox.tap_b()
                FFXC.set_neutral()
                checkpoint += 1
            elif nemesis.nemesis_pathing.set_movement(
                nemesis.nemesis_pathing.arena_return(checkpoint)
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()


def transition():
    memory.main.click_to_control()
    return_to_airship()
    memory.main.await_control()
    menu.add_ability(
        owner=0,
        equipment_type=0,
        ability_array=[0x807A, 255, 255, 255],
        ability_index=0x8001,
        slot_count=2,
        navigate_to_equip_menu=True,
        full_menu_close=True,
    )


def kilika_shop():
    arena_npc()
    xbox.tap_a()
    xbox.tap_b()
    memory.main.wait_frames(60)
    arena_npc()
    xbox.tap_a()
    xbox.tap_b()
    arena_npc()
    xbox.menu_a()
    xbox.tap_b()  # Exit
    memory.main.wait_frames(60)
    while not nemesis.nemesis_pathing.set_movement([-6, -23]):
        pass
    while not nemesis.nemesis_pathing.set_movement([0, -3]):
        pass
    return_to_airship()
    memory.main.await_control()
    rin_equip_dump()
    air_ship_destination(dest_num=2)
    while not nemesis.nemesis_pathing.set_movement([-25, -246]):
        pass
    while not nemesis.nemesis_pathing.set_movement([-47, -209]):
        pass
    while not nemesis.nemesis_pathing.set_movement([-91, -199]):
        pass
    while not nemesis.nemesis_pathing.set_movement([-108, -169]):
        pass
    while memory.main.user_control():
        FFXC.set_movement(-1, 0)
        xbox.tap_b()
    FFXC.set_neutral()  # Now talking to vendor
    memory.main.wait_frames(60)
    xbox.tap_b()  # Intro dialog
    memory.main.wait_frames(60)
    xbox.tap_b()  # Buy equipment
    memory.main.wait_frames(60)
    xbox.tap_down()
    xbox.tap_down()
    xbox.tap_down()
    xbox.tap_down()
    xbox.tap_down()
    xbox.tap_down()
    get_equipment(equip=True)  # Weapon for Rikku
    xbox.tap_down()
    get_equipment(equip=True)  # Armor for Tidus
    xbox.tap_down()
    get_equipment(equip=True)  # Armor for Yuna
    xbox.tap_down()
    get_equipment(equip=True)  # Armor for Wakka
    xbox.tap_down()
    xbox.tap_down()
    xbox.tap_down()
    get_equipment(equip=True)  # Armor for Wakka
    xbox.tap_down()
    get_equipment(equip=True)  # Armor for Rikku
    memory.main.close_menu()
    menu.add_ability(
        owner=6,
        equipment_type=0,
        ability_array=[0x800B, 0x8000, 255, 255],
        ability_index=0x8001,
        slot_count=4,
        navigate_to_equip_menu=True,
        full_menu_close=True,
    )
    menu.add_ability(
        owner=0,
        equipment_type=1,
        ability_array=[0x8072, 255, 255, 255],
        ability_index=0x8056,
        slot_count=4,
        navigate_to_equip_menu=True,
        full_menu_close=True,
    )

    while not nemesis.nemesis_pathing.set_movement([-91, -199]):
        pass
    while not nemesis.nemesis_pathing.set_movement([-47, -209]):
        pass
    while not nemesis.nemesis_pathing.set_movement([-25, -246]):
        pass
    while not nemesis.nemesis_pathing.set_movement([29, -252]):
        pass
    return_to_airship()


def od_to_ap():  # Calm Lands purchases
    arena_return()
    arena_npc()
    xbox.tap_a()
    xbox.tap_b()
    arena_npc()
    xbox.tap_a()
    xbox.tap_b()
    arena_npc()
    xbox.tap_a()
    xbox.tap_b()
    arena_npc()
    xbox.tap_a()
    xbox.tap_b()
    arena_npc()
    xbox.tap_down()
    xbox.tap_down()
    xbox.tap_b()
    memory.main.wait_frames(60)
    xbox.tap_b()
    memory.main.wait_frames(6)
    xbox.tap_b()
    memory.main.wait_frames(6)
    xbox.tap_up()
    xbox.tap_b()
    memory.main.wait_frames(6)
    xbox.tap_up()
    xbox.tap_b()
    logger.debug("Now to sell items.")
    memory.main.wait_frames(6)
    xbox.menu_a()
    memory.main.wait_frames(6)
    xbox.tap_right()
    xbox.menu_b()
    logger.debug("Should now be attempting to sell items.")
    menu.sell_all()
    xbox.menu_a()
    memory.main.wait_frames(60)
    xbox.tap_a()
    memory.main.wait_frames(60)
    xbox.tap_a()
    memory.main.wait_frames(60)
    xbox.tap_a()
    xbox.tap_b()
    menu.auto_sort_equipment(manual="n")
    menu.add_ability(
        owner=0,
        equipment_type=0,
        ability_array=[0x807A, 255, 255, 255],
        ability_index=0x8011,
        slot_count=2,
        navigate_to_equip_menu=True,
        exit_out_of_current_weapon=True,
        close_menu=True,
        full_menu_close=False,
    )
    menu.equip_weapon(character=0, ability=0x8011)
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    menu.tidus_slayer()

    memory.main.await_control()
    FFXC.set_movement(-1, 0)
    memory.main.wait_frames(30)
    return_to_airship()


def farm_feathers():
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=7, monster_index=5)
    memory.main.wait_frames(1)
    wait_counter = 0
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if screen.turn_rikku():
                logger.debug("Qactar steal command")
                battle.main.steal()
                logger.debug("Qactar steal command done")
            elif screen.turn_tidus():
                logger.debug("Qactar flee command")
                battle.main.tidus_flee()
                logger.debug("Qactar flee command done")
            else:
                logger.debug("Qactar defend command")
                battle.main.defend()
                logger.debug("Qactar defend command done")
        wait_counter += 1
        if wait_counter % 10 == 0:
            logger.debug(f"Waiting for next turn: {wait_counter}")
    logger.debug("Battle is complete.")

    while not memory.main.menu_open():
        pass

    FFXC.set_value("btn_b", 1)
    memory.main.wait_frames(150)
    FFXC.set_value("btn_b", 0)
    logger.debug("Now back in control.")
    nemesis.arena_select.arena_menu_select(4)


def auto_phoenix():  # Calm Lands items
    menu.auto_sort_equipment()
    nemesis.menu.lulu_bribe()
    memory.main.full_party_format("initiative")
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=7, monster_index=0)
    bribe_battle()
    nemesis.arena_select.arena_menu_select(4)
    memory.main.full_party_format("initiative")
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=7, monster_index=0)
    bribe_battle()
    nemesis.arena_select.arena_menu_select(4)
    memory.main.full_party_format("initiative")
    arena_npc()
    nemesis.arena_select.arena_menu_select(1)
    nemesis.arena_select.start_fight(area_index=7, monster_index=0)
    bribe_battle()
    nemesis.arena_select.arena_menu_select(4)
    memory.main.full_party_format("initiative")
    arena_npc()
    while memory.main.get_item_count_slot(memory.main.get_item_slot(7)) != 99:
        logger.debug("Trying to obtain mega-phoenix downs")
        nemesis.arena_select.arena_menu_select(4)
        arena_npc()
    nemesis.arena_select.arena_menu_select(2)  # Equipment menu
    memory.main.wait_frames(90)
    xbox.tap_right()
    xbox.menu_b()  # Sell
    menu.sell_all()
    memory.main.wait_frames(3)
    xbox.tap_a()
    memory.main.wait_frames(90)
    xbox.tap_a()
    memory.main.wait_frames(90)
    xbox.tap_a()
    xbox.tap_b()
    menu.auto_sort_equipment()  # This to make sure equipment is in the right place
    menu.add_ability(
        owner=4,
        equipment_type=1,
        ability_array=[0x8072, 255, 255, 255],
        ability_index=0x800A,
        slot_count=4,
        navigate_to_equip_menu=True,
        exit_out_of_current_weapon=True,
        close_menu=True,
        full_menu_close=False,
    )

    memory.main.wait_frames(30)
    init_array = memory.main.check_ability(ability=0x8002)
    logger.debug(f"Initiative weapons: {init_array}")
    if init_array[4]:
        menu.add_ability(
            owner=6,
            equipment_type=1,
            ability_array=[0x8072, 255, 255, 255],
            ability_index=0x800A,
            slot_count=4,
            navigate_to_equip_menu=True,
            exit_out_of_current_weapon=True,
            close_menu=True,
            full_menu_close=False,
        )
        menu.equip_weapon(character=4, ability=0x8002)  # Initiative
        memory.main.close_menu()
    else:
        menu.add_ability(
            owner=6,
            equipment_type=1,
            ability_array=[0x8072, 255, 255, 255],
            ability_index=0x800A,
            slot_count=4,
            navigate_to_equip_menu=True,
            exit_out_of_current_weapon=True,
            close_menu=True,
            full_menu_close=True,
        )
        memory.main.close_menu()
        feather_slot = memory.main.get_item_slot(item_num=54)
        if feather_slot == 255 or memory.main.get_item_count_slot(feather_slot) < 6:
            while (
                feather_slot == 255 or memory.main.get_item_count_slot(feather_slot) < 6
            ):
                farm_feathers()
                feather_slot = memory.main.get_item_slot(item_num=54)
        menu.add_ability(
            owner=6,
            equipment_type=0,
            ability_array=[0x800B, 0x8000, 0x8001, 255],
            ability_index=0x8002,
            slot_count=4,
            navigate_to_equip_menu=True,
            exit_out_of_current_weapon=True,
            close_menu=True,
            full_menu_close=True,
        )

    FFXC.set_movement(-1, 0)
    memory.main.wait_frames(15)
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(15)
    FFXC.set_neutral()
    memory.main.full_party_format("initiative")
    return_to_airship()

    menu.equip_armor(character=4, ability=0x800A)  # Auto-Phoenix
    menu.equip_armor(character=6, ability=0x800A)  # Auto-Phoenix
    if not game_vars.ne_armor() in [0, 4, 6]:
        menu.equip_armor(character=game_vars.ne_armor(), ability=99)  # Unequip
    memory.main.close_menu()


def restock_downs():
    logger.debug("Restocking phoenix downs")
    arena_npc()
    nemesis.arena_select.arena_menu_select(3)
    memory.main.wait_frames(60)
    xbox.tap_b()
    memory.main.wait_frames(6)
    while memory.main.equip_buy_row() != 2:
        if memory.main.equip_buy_row() < 2:
            xbox.tap_down()
        else:
            xbox.tap_up()
    xbox.tap_b()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_b()
    memory.main.wait_frames(6)
    xbox.menu_a()
    memory.main.wait_frames(6)
    xbox.menu_a()


def one_mp_ready():
    logger.debug(f"Slot, Gambler:{memory.main.get_item_slot(41)}")
    if memory.main.get_item_slot(41) > 200:
        return False
    logger.debug(
        f"Count, Gambler:{memory.main.get_item_count_slot(memory.main.get_item_slot(41))}"
    )
    if memory.main.get_item_count_slot(memory.main.get_item_slot(41)) < 99:
        return False
    logger.debug(f"Slot, Salt:{memory.main.get_item_slot(63)}")
    if memory.main.get_item_slot(63) > 200:
        return False
    logger.debug(
        f"Count, Salt:{memory.main.get_item_count_slot(memory.main.get_item_slot(63))}"
    )
    if memory.main.get_item_count_slot(memory.main.get_item_slot(63)) < 20:
        return False
    return True


def tonberry_levels_battle():
    screen.await_turn()
    tidus_turn = False
    while memory.main.battle_active():
        if memory.main.turn_ready():
            if screen.turn_tidus():
                if tidus_turn == True:
                    battle.main.tidus_flee()
                elif memory.main.get_overdrive_battle(character=0):
                    battle.overdrive.tidus()
                else:
                    battle.main.attack()
                tidus_turn = True
            else:
                battle.main.defend()

    logger.debug("Battle is complete.")
    while not memory.main.menu_open():
        pass
    FFXC.set_value("btn_b", 1)
    memory.main.wait_frames(150)
    FFXC.set_value("btn_b", 0)
    logger.debug("Now back in control.")


def one_mp_weapon(force_levels: int = 27):  # Break Damage Limit, or One MP cost
    menu.auto_sort_equipment()
    memory.main.full_party_format("initiative")
    restock_downs()
    nemesis.arena_select.arena_menu_select(4)
    # Set up for levelling if we are low
    if force_levels > game_vars.nem_checkpoint_ap():
        # Set overdrive mode
        menu.tidus_slayer(od_pos=0)
    logger.debug(
        f"Sleeping powder count:{memory.main.get_item_count_slot(memory.main.get_item_slot(37))}"
    )
    while (
        memory.main.get_item_slot(37) > 200
        or memory.main.get_item_count_slot(memory.main.get_item_slot(37)) < 41
    ):
        arena_npc()
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=7, monster_index=0)
        bribe_battle()
        nemesis.arena_select.arena_menu_select(4)
        memory.main.full_party_format("initiative")
        logger.debug(
            f"Sleeping powder count:{memory.main.get_item_count_slot(memory.main.get_item_slot(37))}"
        )
    while not one_mp_ready():
        logger.debug("Trying to obtain Gambler's Soul and Purifying Salt items")
        arena_npc()
        nemesis.arena_select.arena_menu_select(4)

    # Lv.4 key sphere recovery logic
    if (
        memory.main.get_item_slot(84) == 255
        or memory.main.get_item_count_slot(memory.main.get_item_slot(84)) == 1
    ):
        while (
            memory.main.get_item_slot(84) == 255
            or memory.main.get_item_count_slot(memory.main.get_item_slot(84)) == 1
        ):
            arena_npc()
            logger.debug("Need Lv.4 key sphere for sphere grid")
            nemesis.arena_select.arena_menu_select(1)
            nemesis.arena_select.start_fight(area_index=8, monster_index=7)
            bribe_battle(spare_change_value=245000)
            nemesis.arena_select.arena_menu_select(4)
            memory.main.full_party_format("initiative")
    else:
        logger.debug("Good on Lv.4 key spheres for sphere grid")
    if (
        memory.main.get_item_slot(84) == 255
        or memory.main.get_item_count_slot(memory.main.get_item_slot(84)) == 1
    ):
        arena_npc()
        logger.debug("Need Lv.4 key sphere for sphere grid")
        nemesis.arena_select.arena_menu_select(1)
        nemesis.arena_select.start_fight(area_index=8, monster_index=7)
        bribe_battle(spare_change_value=196000)
        nemesis.arena_select.arena_menu_select(4)
        memory.main.full_party_format("initiative")
    else:
        logger.debug("Good on Lv.4 key spheres for sphere grid")

    # Finish leveling before we make a 1mp weapon
    if force_levels > game_vars.nem_checkpoint_ap():
        while (
            memory.main.get_item_slot(46) == 255
            or memory.main.get_item_count_slot(memory.main.get_item_slot(46)) < 40
        ):
            arena_npc()
            nemesis.arena_select.arena_menu_select(4)
        while force_levels > game_vars.nem_checkpoint_ap():
            arena_npc()
            nemesis.arena_select.arena_menu_select(1)
            nemesis.arena_select.start_fight(area_index=13, monster_index=9)
            tonberry_levels_battle()
            nemesis.arena_select.arena_menu_select(4)
            nemesis.menu.perform_next_grid()
        menu.tidus_slayer(od_pos=0)

    arena_npc()
    nemesis.arena_select.arena_menu_select(2)

    # Now ready to make item
    memory.main.wait_frames(60)
    xbox.menu_b()  # Buy
    memory.main.wait_frames(10)
    xbox.menu_b()  # New Tidus capture weapon
    memory.main.wait_frames(10)
    xbox.tap_up()
    xbox.menu_b()  # Confirm purchase
    memory.main.wait_frames(10)
    xbox.tap_up()
    xbox.menu_b()  # Confirm equipping weapon

    memory.main.wait_frames(3)
    xbox.tap_a()
    memory.main.wait_frames(30)
    xbox.tap_a()
    memory.main.wait_frames(30)
    xbox.tap_a()
    xbox.tap_b()
    menu.auto_sort_equipment()  # This to make sure equipment is in the right place
    memory.main.close_menu()
    menu.add_ability(
        owner=0,
        equipment_type=0,
        ability_array=[0x807A, 255, 255, 255],
        ability_index=0x800D,
        slot_count=2,
        navigate_to_equip_menu=True,
        exit_out_of_current_weapon=True,
        close_menu=True,
        full_menu_close=True,
    )
    FFXC.set_movement(-1, 0)
    memory.main.wait_frames(15)
    FFXC.set_movement(0, 1)
    memory.main.wait_frames(15)
    FFXC.set_neutral()
    return_to_airship()
    nemesis.menu.rikku_haste()


def kilika_gil_farm(armor_buys: int):
    xbox.tap_down()
    xbox.tap_down()
    xbox.tap_down()
    xbox.tap_down()
    xbox.tap_down()
    xbox.tap_down()
    xbox.tap_down()
    for x in range(armor_buys):
        logger.debug(f"Buying armors, remaining - {armor_buys - x}")
        memory.main.wait_frames(6)
        xbox.menu_b()  # Purchase
        memory.main.wait_frames(6)
        xbox.menu_up()
        xbox.menu_b()  # Confirm
        memory.main.wait_frames(6)
        xbox.menu_b()  # Do not equip
    memory.main.wait_frames(6)
    memory.main.close_menu()

    for y in range(armor_buys):
        if y == 0:  # First one
            menu.add_ability(
                owner=0,
                equipment_type=1,
                ability_array=[0x8072, 255, 255, 255],
                ability_index=0x8075,
                slot_count=4,
                navigate_to_equip_menu=True,
                exit_out_of_current_weapon=True,
                close_menu=False,
                full_menu_close=False,
            )
        else:
            menu.add_ability(
                owner=0,
                equipment_type=1,
                ability_array=[0x8072, 255, 255, 255],
                ability_index=0x8075,
                slot_count=4,
                navigate_to_equip_menu=False,
                exit_out_of_current_weapon=True,
                close_menu=False,
                full_menu_close=False,
            )
    memory.main.close_menu()
    memory.main.wait_frames(9)
    while memory.main.user_control():
        FFXC.set_movement(-1, 0)
        xbox.tap_b()
    FFXC.set_neutral()  # Now talking to vendor
    memory.main.wait_frames(60)
    xbox.tap_b()  # Intro dialog
    memory.main.wait_frames(60)
    xbox.tap_right()
    xbox.tap_b()  # Sell equipment
    menu.sell_all()
    memory.main.wait_frames(10)
    xbox.tap_a()


def kilika_final_shop():
    memory.main.await_control()
    rin_equip_dump(sell_nea=True)
    menu.auto_sort_equipment()

    air_ship_destination(dest_num=2)
    while not nemesis.nemesis_pathing.set_movement([-25, -246]):
        pass
    while not nemesis.nemesis_pathing.set_movement([-47, -209]):
        pass
    while not nemesis.nemesis_pathing.set_movement([-91, -199]):
        pass
    while not nemesis.nemesis_pathing.set_movement([-108, -169]):
        pass
    while memory.main.user_control():
        FFXC.set_movement(-1, 0)
        xbox.tap_b()
    FFXC.set_neutral()  # Now talking to vendor
    memory.main.wait_frames(60)
    xbox.tap_b()  # Intro dialog
    memory.main.wait_frames(60)
    xbox.tap_b()  # Buy equipment
    memory.main.wait_frames(60)
    get_equipment(equip=True)  # Weapon for Tidus
    memory.main.wait_frames(6)

    gil_needed = 3500000 - memory.main.get_gil_value()
    # Get minimum needed, plus one for safety. Max 99 total.
    armor_buys = min(int(gil_needed / 26150), 98) + 1
    can_afford = int(memory.main.get_gil_value() / 2250)

    while armor_buys >= 1:
        kilika_gil_farm(min(armor_buys, can_afford))
        armor_buys = int(max(armor_buys - can_afford, 0))
        can_afford = int(memory.main.get_gil_value() / 2250)
        if armor_buys >= 1:
            memory.main.wait_frames(10)
            xbox.menu_left()
            xbox.menu_b()
    memory.main.close_menu()

    while not nemesis.nemesis_pathing.set_movement([-91, -199]):
        pass
    while not nemesis.nemesis_pathing.set_movement([-47, -209]):
        pass
    while not nemesis.nemesis_pathing.set_movement([-25, -246]):
        pass
    while not nemesis.nemesis_pathing.set_movement([29, -252]):
        pass
    menu.auto_sort_equipment()
    return_to_airship()


def final_weapon():
    arena_npc()
    while memory.main.get_item_count_slot(memory.main.get_item_slot(53)) < 99:
        logger.debug("Trying to obtain Dark Matter for BDL weapon")
        nemesis.arena_select.arena_menu_select(4)
        arena_npc()
    nemesis.arena_select.arena_menu_select(4)

    menu.add_ability(
        owner=0,
        equipment_type=0,
        ability_array=[0x800B, 0x8000, 255, 255],
        ability_index=0x800D,
        slot_count=4,
        navigate_to_equip_menu=True,
        exit_out_of_current_weapon=False,
        close_menu=False,
        full_menu_close=False,
    )
    menu.add_ability(
        owner=0,
        equipment_type=0,
        ability_array=[0x800B, 0x8000, 0x800D, 255],
        ability_index=0x8019,
        slot_count=4,
        navigate_to_equip_menu=False,
        exit_out_of_current_weapon=True,
        close_menu=False,
        full_menu_close=False,
    )

    menu.add_ability(
        owner=1,
        equipment_type=1,
        ability_array=[0x8072, 255, 255, 255],
        ability_index=0x800A,
        slot_count=4,
        navigate_to_equip_menu=True,
        exit_out_of_current_weapon=False,
        close_menu=False,
        full_menu_close=False,
    )
    menu.add_ability(
        owner=1,
        equipment_type=1,
        ability_array=[0x8072, 0x800A, 255, 255],
        ability_index=0x801D,
        slot_count=4,
        navigate_to_equip_menu=False,
        exit_out_of_current_weapon=True,
        close_menu=True,
        full_menu_close=False,
    )
    menu.equip_weapon(character=0, ability=0x8019)  # BDL (one MP)
    memory.main.full_party_format("kilikawoods1")


def rin_equip_dump(buy_weapon=False, sell_nea=False):
    while not nemesis.nemesis_pathing.set_movement([-242, 298]):
        pass
    while not nemesis.nemesis_pathing.set_movement([-243, 160]):
        pass
    FFXC.set_movement(0, -1)
    while memory.main.user_control():
        pass
    while not nemesis.nemesis_pathing.set_movement([39, 53]):
        pass
    while memory.main.user_control():
        nemesis.nemesis_pathing.set_movement([28, 44])
        xbox.tap_b()
    FFXC.set_neutral()
    memory.main.click_to_diag_progress(48)
    memory.main.wait_frames(10)
    xbox.tap_b()
    memory.main.wait_frames(30)
    xbox.tap_right()
    xbox.menu_b()

    menu.sell_all(nea=sell_nea)
    if buy_weapon:
        memory.main.wait_frames(60)
        xbox.menu_right()  # Removes any pop-ups
        memory.main.wait_frames(60)
        xbox.menu_a()
        memory.main.wait_frames(60)
        xbox.menu_left()
        memory.main.wait_frames(60)
        xbox.menu_b()
        memory.main.wait_frames(60)
        xbox.menu_b()
        memory.main.wait_frames(60)
        xbox.menu_up()
        memory.main.wait_frames(60)
        xbox.menu_b()
        memory.main.wait_frames(60)
        xbox.menu_up()
        memory.main.wait_frames(60)
        xbox.menu_b()
        memory.main.wait_frames(60)
    memory.main.close_menu()
    memory.main.click_to_control_dumb()
    while not nemesis.nemesis_pathing.set_movement([53, 110]):
        pass
    FFXC.set_movement(-1, -1)
    while memory.main.user_control():
        pass
    while not nemesis.nemesis_pathing.set_movement([-241, 223]):
        pass
    while not nemesis.nemesis_pathing.set_movement([-246, 329]):
        pass


def yojimbo_dialog():
    logger.debug("Clicking until dialog box")
    while memory.main.diag_progress_flag():
        xbox.tap_b()
    logger.debug("Dialog box online.")
    memory.main.wait_frames(60)
    xbox.tap_up()
    xbox.tap_b()
    memory.main.click_to_diag_progress(5)
    memory.main.wait_frames(12)
    xbox.tap_left()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_left()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_b()
    memory.main.wait_frames(12)  # Eff it, just pay the man!
    logger.debug("Fayth accepts the contract.")
    xbox.name_aeon("Yojimbo")
    logger.debug("Naming complete.")


def yojimbo():
    checkpoint = 0
    while not memory.main.get_map() in [194, 374]:
        if memory.main.user_control():
            if checkpoint == 5:
                memory.main.click_to_event_temple(4)
                checkpoint += 1
            elif checkpoint == 9:
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 29 and memory.main.get_coords()[1] > 1800:
                checkpoint += 1
            elif checkpoint in [32, 35]:
                FFXC.set_neutral()
                memory.main.wait_frames(12)
                if checkpoint == 32:
                    FFXC.set_movement(0, 1)
                else:
                    FFXC.set_movement(0, -1)
                memory.main.wait_frames(2)
                FFXC.set_neutral()
                memory.main.wait_frames(12)
                xbox.tap_b()
                checkpoint += 1
            elif checkpoint == 33:  # Talking to Fayth
                yojimbo_dialog()
                checkpoint += 1
            elif checkpoint == 39:
                memory.main.click_to_event_temple(3)
                checkpoint += 1
            elif checkpoint == 41:
                return_to_airship()
            elif (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.yojimbo(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle.main.yojimbo()
                memory.main.click_to_control()
            elif checkpoint == 33:  # Talking to Fayth
                yojimbo_dialog()
                checkpoint += 1
            elif memory.main.diag_skip_possible():
                xbox.tap_b()


def besaid_farm(cap_num: int = 1):
    air_ship_destination(dest_num=1)
    menu.remove_all_nea()

    memory.main.arena_farm_check(zone="besaid", end_goal=cap_num, report=True)
    checkpoint = 0
    while not memory.main.get_map() in [194, 374]:
        if memory.main.user_control():
            if (
                memory.main.arena_farm_check(
                    zone="besaid", end_goal=cap_num, report=False
                )
                and checkpoint < 15
            ):
                checkpoint = 15
            elif checkpoint == 15 and not memory.main.arena_farm_check(
                zone="besaid", end_goal=cap_num, report=False
            ):
                checkpoint -= 2
                logger.debug(f"Checkpoint reached: {checkpoint}")

            elif checkpoint == 1:
                memory.main.click_to_event_temple(4)
                checkpoint += 1
            elif checkpoint == 11:
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 16 and memory.main.get_map() == 20:
                checkpoint += 1
            elif checkpoint == 25:
                memory.main.click_to_event_temple(4)
                checkpoint += 1
            elif checkpoint == 26:
                return_to_airship()
            elif (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.besaid_farm(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                if cap_num == 10:
                    battle_farm_all(yuna_attack=False)
                else:
                    battle_farm_all()
                memory.main.arena_farm_check(
                    zone="besaid", end_goal=cap_num, report=True
                )
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()


def kilika_farm(cap_num: int = 1):
    air_ship_destination(dest_num=2)
    menu.remove_all_nea()

    checkpoint = 0
    while not memory.main.get_map() in [194, 374]:
        if memory.main.user_control():
            if (
                memory.main.arena_farm_check(
                    zone="kilika", end_goal=cap_num, report=False
                )
                and checkpoint < 14
            ):
                checkpoint = 14
            elif checkpoint == 14:
                if not memory.main.arena_farm_check(
                    zone="kilika", end_goal=cap_num, report=False
                ):
                    checkpoint -= 2
                    logger.debug(f"Checkpoint reached: {checkpoint}")
                else:
                    return_to_airship()
            elif checkpoint == 4:
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif checkpoint == 11:
                memory.main.click_to_event_temple(0)
                memory.main.arena_farm_check(zone="kilika", end_goal=10, report=True)
                checkpoint += 1
            elif checkpoint == 14 and memory.main.get_map() == 47:
                checkpoint += 1
            elif checkpoint == 21:
                memory.main.click_to_event_temple(3)
                checkpoint += 1
            elif checkpoint == 25:
                return_to_airship()
            elif (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.kilika_farm(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                if cap_num == 10:
                    battle_farm_all(yuna_attack=False)
                else:
                    battle_farm_all()
                memory.main.arena_farm_check(
                    zone="kilika", end_goal=cap_num, report=True
                )
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()


def miihen_next(end_goal: int):
    next1 = rng_track.coming_battles(area="mi'ihen_(newroad)", battle_count=2)[0]
    next2 = rng_track.coming_battles(area="old_road", battle_count=2)[0]
    next3 = rng_track.coming_battles(area="clasko_skip_screen", battle_count=2)[0]
    next4 = rng_track.coming_battles(area="mrr_-_valley", battle_count=2)[0]
    next6 = rng_track.coming_battles(area="mrr_-_precipice", battle_count=2)[0]
    farm_array1 = memory.main.arena_farm_check(
        zone="miihen", end_goal=end_goal, return_array=True
    )
    farm_array2 = memory.main.arena_farm_check(
        zone="mrr", end_goal=end_goal, return_array=True
    )

    if memory.main.get_yuna_mp() < 30:
        return 8
    if memory.main.arena_farm_check(zone="miihen", end_goal=end_goal):
        logger.debug("Next battles:")
        logger.debug(next4)
        logger.debug(next6)
        logger.debug(farm_array2)

        if memory.main.arena_farm_check(zone="mrr", end_goal=end_goal):
            return 9  # Ready to move on
        elif "garuda" in next6:
            return 6
        elif "garuda" in next4:
            return 5
        elif farm_array2[3] < end_goal and "lamashtu" in next4:
            return 5
        elif memory.main.get_map() == 128:
            return 6
        else:
            return 5

    logger.debug("Next battles:")
    logger.debug(next1)
    logger.debug(next2)
    logger.debug(next3)
    logger.debug(next4)
    logger.debug(farm_array1)
    logger.debug(farm_array2)

    if farm_array2[2] < end_goal and "garuda" in next4:
        return 4
    if farm_array1[0] < end_goal and "raldo" in next1:
        return 1
    if farm_array1[1] < end_goal and "mi'ihen_fang" in next1:
        return 1
    if farm_array1[7] < end_goal and "white_element" in next1:
        return 1
    if farm_array2[3] < end_goal and "lamashtu" in next4:
        return 4
    if farm_array1[2] < end_goal and "thunder_flan" in next2:
        return 2
    if farm_array1[2] < end_goal and "thunder_flan" in next3:
        return 3
    if farm_array1[3] < end_goal and "ipiria" in next2:
        return 2
    if farm_array1[3] < end_goal and "ipiria" in next3:
        return 3
    if farm_array1[4] < end_goal and "floating_eye" in next2:
        return 2
    if farm_array1[4] < end_goal and "floating_eye" in next3:
        return 3
    if farm_array1[5] < end_goal and "dual_horn" in next2:
        return 2
    if farm_array1[5] < end_goal and "dual_horn" in next3:
        return 3
    if farm_array1[6] < end_goal and "vouivre" in next2:
        return 2
    if farm_array1[6] < end_goal and "vouivre" in next3:
        return 3
    if farm_array1[8] < end_goal and "bomb" in next2:
        return 2
    if farm_array1[8] < end_goal and "bomb" in next3:
        return 3

    logger.debug("Couldn't find a special case")
    if memory.main.get_map() == 128:
        return 6
    if memory.main.get_map() == 92:
        if memory.main.arena_farm_check(zone="miihen", end_goal=end_goal):
            return 5
        else:
            return 4
    if memory.main.get_map() == 79:
        return 3
    if memory.main.get_map() == 116:
        return 2
    return 1


def miihen_farm(cap_num: int = 1):
    air_ship_destination(dest_num=4)
    menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    ne_armor = True
    pref_area = miihen_next(end_goal=cap_num)
    logger.debug(f"Next area: {pref_area}")
    memory.main.full_party_format("initiative")

    checkpoint = 0
    last_cp = checkpoint
    while not memory.main.get_map() in [194, 374]:
        # Checkpoint notify
        if last_cp != checkpoint:
            logger.debug(f"Checkpoint reached: {checkpoint}")
            last_cp = checkpoint
        if memory.main.user_control():
            if checkpoint == 92:
                FFXC.set_neutral()
                while memory.main.user_control():
                    xbox.tap_b()
                checkpoint = 144
            # Map changes
            if checkpoint == 2:
                memory.main.click_to_event_temple(4)
                checkpoint += 1
            if checkpoint == 8:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
            elif checkpoint == 18 and memory.main.get_map() == 116:
                checkpoint += 1
            # Map between Miihen and MRR
            elif checkpoint in [31, 42, 72] and memory.main.get_map() == 59:
                checkpoint += 1
            elif checkpoint in [38, 39] and memory.main.get_map() == 116:  # Area 2 map
                checkpoint = 40
            elif checkpoint in [50, 63] and memory.main.get_map() == 79:  # Clasko map
                checkpoint += 1
            elif checkpoint == 60 and memory.main.get_map() == 92:  # MRR lower map
                checkpoint += 1
            elif checkpoint == 79 and memory.main.get_map() == 116:  # Highroad
                checkpoint = 29

            # Save Sphere / Exit logic
            if checkpoint in [47, 61, 62, 63, 164] and pref_area in [8, 9]:
                if pref_area == 8:
                    save_sphere.touch_and_go()
                    pref_area = miihen_next(end_goal=cap_num)
                    logger.debug(f"Next area: {pref_area}")
                else:
                    return_to_airship()

            # Farming logic
            elif checkpoint == 28 and pref_area == 1 and ne_armor:
                menu.remove_all_nea()
                miihen_next(end_goal=cap_num)
                logger.debug(f"Next area: {pref_area}")
                ne_armor = False
            elif checkpoint in [31, 80] and pref_area == 1:  # Farm in area 1
                checkpoint = 29
            elif checkpoint == 42 and pref_area == 2:  # Farm in area 2
                checkpoint = 40
            elif checkpoint in [53, 60, 66] and pref_area == 3:  # Farm in area 3
                checkpoint -= 2
            elif checkpoint == 63 and pref_area == 4:  # Farm in area 4
                checkpoint -= 2
            elif checkpoint == 33 and pref_area >= 3:  # Skip from zone 1 to zone >= 3
                checkpoint = 46
            elif checkpoint in [51, 52, 53] and pref_area <= 2:
                checkpoint = 72
            elif checkpoint == 77 and pref_area == 2:
                checkpoint = 34
            elif checkpoint == 77 and pref_area >= 3:
                checkpoint = 46
            elif checkpoint == 67 and pref_area >= 4:
                checkpoint = 59
            elif checkpoint in [48, 53] and pref_area >= 4 and not ne_armor:
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                ne_armor = True
            elif checkpoint == 47 and pref_area == 1:
                checkpoint = 74
            elif checkpoint == 59 and pref_area in [4, 5] and ne_armor:
                menu.remove_all_nea()
                miihen_next(end_goal=cap_num)
                logger.debug(f"Next area: {pref_area}")
                ne_armor = False
            elif checkpoint in [63, 64] and pref_area in [1, 2] and not ne_armor:
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                ne_armor = True
            elif checkpoint in [32, 42, 73] and pref_area in [1, 2, 3] and ne_armor:
                menu.remove_all_nea()
                miihen_next(end_goal=cap_num)
                logger.debug(f"Next area: {pref_area}")
                ne_armor = False
            elif checkpoint == 151 and not ne_armor:
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                ne_armor = True
            elif checkpoint == 69 and pref_area != 3 and not ne_armor:
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                ne_armor = True

            # Garuda late farming logic
            elif checkpoint in [61, 62, 63] and pref_area >= 5:
                checkpoint = 100
            elif checkpoint == 146 and pref_area == 5:
                checkpoint -= 2
                if ne_armor:
                    menu.remove_all_nea()
                    miihen_next(end_goal=cap_num)
                    logger.debug(f"Next area: {pref_area}")
                    ne_armor = False
            elif checkpoint in [104, 146, 158]:
                FFXC.set_neutral()
                memory.main.click_to_event()
                checkpoint += 1
            elif (
                checkpoint > 99
                and checkpoint < 144
                and pref_area in [6, 8, 9]
                and not ne_armor
            ):
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                ne_armor = True
            elif checkpoint > 99 and checkpoint >= 144 and pref_area == 6 and ne_armor:
                menu.remove_all_nea()
                miihen_next(end_goal=cap_num)
                logger.debug(f"Next area: {pref_area}")
                ne_armor = False
            elif checkpoint == 150 and pref_area == 6:
                checkpoint -= 2
                if ne_armor:
                    menu.remove_all_nea()
                    miihen_next(end_goal=cap_num)
                    logger.debug(f"Next area: {pref_area}")
                    ne_armor = False

            elif checkpoint in [148, 149, 150] and pref_area == 5:
                checkpoint = 90

            elif (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.miihen_farm(checkpoint)
                )
                == True
            ):
                checkpoint += 1
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                if (
                    memory.main.get_encounter_id() == 78
                    and memory.main.arena_array()[34] == 10
                ):
                    battle.main.flee_all()
                else:
                    if cap_num == 10:
                        battle_farm_all(yuna_attack=False)
                    else:
                        battle_farm_all()
                pref_area = miihen_next(end_goal=cap_num)
                logger.debug(f"Next area: {pref_area}")
                memory.main.full_party_format("initiative")
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()


def miihen_farm_old(cap_num: int = 1):
    air_ship_destination(dest_num=4)
    if game_vars.ne_armor() == 0:
        menu.equip_armor(character=game_vars.ne_armor(), ability=0x8056)  # Auto-Haste
    else:
        menu.equip_armor(character=game_vars.ne_armor(), ability=99)  # Unequip

    checkpoint = 0
    while memory.main.get_map() != 79:
        if memory.main.user_control():
            if memory.main.arena_farm_check(
                zone="miihen1", end_goal=cap_num, report=False
            ) and checkpoint in [28, 29]:
                checkpoint = 30
            elif checkpoint == 31 and not memory.main.arena_farm_check(
                zone="miihen1", end_goal=cap_num, report=False
            ):
                checkpoint -= 2
                logger.debug(f"Checkpoint reached: {checkpoint}")

            elif checkpoint == 2:
                memory.main.click_to_event_temple(4)
                checkpoint += 1
            elif checkpoint == 8:
                memory.main.click_to_event_temple(0)
                checkpoint += 1
                memory.main.arena_farm_check(
                    zone="miihen1", end_goal=cap_num, report=True
                )
            elif checkpoint == 18 and memory.main.get_map() == 116:
                checkpoint += 1
            elif checkpoint in [31, 42] and memory.main.get_map() == 59:
                checkpoint += 1
            elif checkpoint in [34, 47]:
                save_sphere.touch_and_go()
                checkpoint += 1
            elif checkpoint == 39:
                memory.main.click_to_event_temple(4)
                checkpoint += 1
            elif (
                memory.main.arena_farm_check(
                    zone="miihen2", end_goal=cap_num, report=False
                )
                and checkpoint < 41
            ):
                checkpoint = 41
            elif checkpoint == 42 and not memory.main.arena_farm_check(
                zone="miihen2", end_goal=cap_num, report=False
            ):
                checkpoint -= 2
                logger.debug(f"Checkpoint reached: {checkpoint}")
            elif checkpoint == 50:
                memory.main.click_to_event_temple(0)
                checkpoint += 1

            elif (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.miihen_farm(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                if (
                    memory.main.get_encounter_id() == 78
                    and memory.main.arena_array()[34] == 10
                ):
                    battle.main.flee_all()
                else:
                    if cap_num == 10:
                        battle_farm_all(yuna_attack=False)
                    else:
                        battle_farm_all()

                if checkpoint < 32:
                    memory.main.arena_farm_check(
                        zone="miihen1", end_goal=cap_num, report=True
                    )
                else:
                    memory.main.arena_farm_check(
                        zone="miihen2", end_goal=cap_num, report=True
                    )
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()


def djose_next(end_goal: int):
    next1 = rng_track.coming_battles(area="djose_highroad_(back_half)", battle_count=2)[
        0
    ]
    next2 = rng_track.coming_battles(area="moonflow_(south)", battle_count=2)[0]
    farm_array = memory.main.arena_farm_check(
        zone="djose", end_goal=end_goal, return_array=True
    )

    logger.debug("Next battles:")
    logger.debug(next1)
    logger.debug(next2)
    logger.debug(farm_array)

    if memory.main.get_yuna_mp() < 30:
        return 3
    if farm_array[3] < end_goal and "simurgh" in next1:
        return 1
    if farm_array[6] < end_goal and "ochu" in next2:
        return 2
    if farm_array[4] < end_goal and "bite_bug" in next2:
        return 2
    if farm_array[4] < end_goal and "bite_bug" in next1:
        return 1
    if farm_array[5] < end_goal and "basilisk" in next1:
        return 1
    if farm_array[2] < end_goal and "snow_flan" in next1:
        return 1
    if farm_array[2] < end_goal and "snow_flan" in next2:
        return 2
    if farm_array[1] < end_goal and "garm" in next1:
        return 1
    if farm_array[1] < end_goal and "garm" in next2:
        return 2
    if farm_array[0] < end_goal and "bunyip_2" in next1:
        return 1
    if farm_array[0] < end_goal and "bunyip_2" in next2:
        return 2
    if memory.main.arena_farm_check(zone="djose", end_goal=end_goal):
        return 4
    logger.debug("Couldn't find a special case")
    return 1


def djose_farm(cap_num: int = 10):

    air_ship_destination(dest_num=5)
    memory.main.full_party_format("initiative")
    menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    ne_armor = True
    pref_area = djose_next(end_goal=cap_num)
    logger.debug(f"Next area: {pref_area}")
    memory.main.full_party_format("initiative")

    checkpoint = 0
    last_cp = 0
    while not memory.main.get_map() in [194, 374]:
        if last_cp != checkpoint:
            logger.debug(f"Checkpoint reached: {checkpoint}")
            last_cp = checkpoint
        if memory.main.user_control():
            # Map changes
            if checkpoint in [7, 27, 45] and memory.main.get_map() == 93:
                checkpoint += 1
            elif checkpoint == 24 and memory.main.get_map() == 75:
                checkpoint += 1
            elif checkpoint in [30, 39] and memory.main.get_map() == 76:
                checkpoint += 1
            elif checkpoint == 35 and memory.main.get_map() == 82:
                checkpoint += 1
            # Reset/End logic
            elif checkpoint == 37:
                if pref_area == 3:
                    save_sphere.touch_and_go()
                    checkpoint += 1
                else:
                    return_to_airship()

            # Farming logic
            if pref_area in [3, 4] and not ne_armor:
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                ne_armor = True
            elif checkpoint in [21, 45] and pref_area == 1 and ne_armor:
                menu.remove_all_nea()
                ne_armor = False
            elif checkpoint == 25 and ne_armor:
                menu.remove_all_nea()
                ne_armor = False
            elif checkpoint in [24, 28] and pref_area == 1:
                checkpoint = 22
            elif checkpoint == 27 and pref_area == 2:
                checkpoint -= 2
            elif checkpoint in [22, 23] and pref_area != 1:
                if pref_area == 2:
                    checkpoint = 24
                else:
                    checkpoint = 28
            elif checkpoint in [25, 26] and pref_area != 2:
                checkpoint = 27
            elif checkpoint == 47:
                checkpoint = 21

            elif (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.djose_farm(checkpoint)
                )
                == True
            ):
                checkpoint += 1
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle_farm_all(yuna_attack=False)
                if memory.main.get_hp()[0] < 1100:
                    battle.main.heal_up(3)
                pref_area = djose_next(end_goal=cap_num)
                logger.debug(f"Next area: {pref_area}")
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()


def plains_next(end_goal: int):
    next1 = rng_track.coming_battles(
        area="thunder_plains_(north)_(1_stone)", battle_count=2
    )[0]
    next2 = rng_track.coming_battles(
        area="thunder_plains_(south)_(2_stones)", battle_count=2
    )[0]
    farm_array = memory.main.arena_farm_check(
        zone="tplains", end_goal=end_goal, return_array=True
    )

    logger.debug("Next battles:")
    logger.debug(next1)
    logger.debug(next2)
    logger.debug(farm_array)

    if memory.main.get_yuna_mp() < 30:
        return 4
    if farm_array[5] < end_goal and "iron_giant" in next1:
        return 1
    if farm_array[5] < end_goal and "iron_giant" in next2:
        return 2
    if farm_array[6] < end_goal and "qactuar" in next1:
        return 1
    if farm_array[6] < end_goal and "qactuar" in next2:
        return 2
    if farm_array[1] < end_goal and "melusine" in next1:
        return 1
    if farm_array[1] < end_goal and "melusine" in next2:
        return 2
    if farm_array[7] < end_goal and "larva" in next1:
        return 1
    if farm_array[7] < end_goal and "larva" in next2:
        return 2
    if farm_array[4] < end_goal and "gold_element" in next1:
        return 1
    if farm_array[4] < end_goal and "gold_element" in next2:
        return 2
    if farm_array[2] < end_goal and "buer" in next1:
        return 1
    if farm_array[2] < end_goal and "buer" in next2:
        return 2
    if farm_array[3] < end_goal and "kusariqqu" in next1:
        return 1
    if farm_array[3] < end_goal and "kusariqqu" in next2:
        return 2
    if farm_array[0] < end_goal and "aerouge" in next1:
        return 1
    if farm_array[0] < end_goal and "aerouge" in next2:
        return 2
    if memory.main.get_yuna_mp() < 30:
        return 3
    if memory.main.arena_farm_check(zone="tplains", end_goal=end_goal):
        return 4
    logger.debug("Couldn't find a special case")
    if memory.main.get_map() == 162:
        return 1
    else:
        return 2


def t_plains(cap_num: int = 1, auto_haste: bool = False):

    air_ship_destination(dest_num=8)
    memory.main.full_party_format(front_line="yuna", full_menu_close=False)
    menu.remove_all_nea()
    memory.main.close_menu()
    pref_area = plains_next(end_goal=cap_num)
    logger.debug(f"Next area: {pref_area}")
    ne_equip = False

    checkpoint = 0
    while not memory.main.get_map() in [194, 374]:
        if memory.main.user_control():
            if memory.main.dodge_lightning(game_vars.get_l_strike()):
                logger.debug("Strike!")
                game_vars.set_l_strike(memory.main.l_strike_count())
            if pref_area in [3, 4] and not ne_equip:
                logger.debug(f"No Encounters armor on char: {game_vars.ne_armor()}")
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                ne_equip = True
                if checkpoint in [4, 5]:
                    checkpoint = 6
                if checkpoint in [9, 10]:
                    checkpoint = 11
            elif checkpoint in [8, 12] and pref_area in [3, 4]:
                checkpoint = 20
                logger.debug(f"Back to agency {checkpoint}")
            elif checkpoint in [6, 14, 15, 16] and pref_area == 1:
                checkpoint = 4
                logger.debug(f"Backtrack: {checkpoint}")
            elif checkpoint == 11 and pref_area == 2:
                checkpoint -= 2
                logger.debug(f"Backtrack: {checkpoint}")
            elif checkpoint in [4, 5] and pref_area == 2:
                checkpoint = 6
                logger.debug(f"Forward: {checkpoint}")
            elif checkpoint in [9, 10] and pref_area == 1:
                checkpoint = 11
                logger.debug(f"Forward: {checkpoint}")
            # From start, can go straight to south.
            elif checkpoint == 2 and pref_area == 2:
                checkpoint = 7
                logger.debug(f"Direct to South: {checkpoint}")

            # Map changes:
            if checkpoint in [1, 6, 11] and memory.main.get_map() == 256:
                checkpoint += 1
                logger.debug(f"Map change: {checkpoint}")
            if checkpoint in [3, 13] and memory.main.get_map() == 162:
                checkpoint += 1
                logger.debug(f"Map change: {checkpoint}")
            if checkpoint == 8 and memory.main.get_map() == 140:
                checkpoint += 1
                logger.debug(f"Map change: {checkpoint}")
            if checkpoint == 21 and memory.main.get_map() == 263:
                checkpoint += 1
                logger.debug(f"Map change: {checkpoint}")
            if checkpoint == 23:
                if pref_area == 3:
                    save_sphere.touch_and_go()
                    menu.remove_all_nea()
                    ne_equip = False
                    pref_area = plains_next(end_goal=cap_num)
                    logger.debug(f"Next area: {pref_area}")
                    checkpoint = 0
                else:
                    return_to_airship()

            # General pathing
            elif (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.tp_farm(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                if cap_num == 10:
                    battle_farm_all(yuna_attack=False)
                else:
                    battle_farm_all()
                battle.main.heal_up(3)
                memory.main.full_party_format("yuna")
                pref_area = plains_next(end_goal=cap_num)
                logger.debug(f"Next area:{pref_area}")
                memory.main.arena_farm_check(
                    zone="tPlains", end_goal=cap_num, report=True
                )
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()
    logger.debug("End of Thunder Plains section")
    return memory.main.arena_farm_check(zone="tPlains", end_goal=cap_num, report=False)


def t_plains_old(cap_num: int = 1, auto_haste: bool = False):

    air_ship_destination(dest_num=8)
    menu.remove_all_nea()

    checkpoint = 0
    while not memory.main.get_map() in [194, 374]:
        if memory.main.user_control():
            if memory.main.dodge_lightning(game_vars.get_l_strike()):
                logger.debug("Strike!")
                game_vars.set_l_strike(memory.main.l_strike_count())
            elif (
                memory.main.arena_farm_check(
                    zone="tPlains", end_goal=cap_num, report=False
                )
                and checkpoint < 8
            ):
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                checkpoint = 8
            elif memory.main.get_yuna_mp() < 30 and checkpoint < 8:
                checkpoint = 8
            elif (
                checkpoint == 9
                and not memory.main.arena_farm_check(
                    zone="tPlains", end_goal=cap_num, report=False
                )
                and memory.main.get_yuna_mp() >= 30
            ):
                checkpoint -= 2

            # Map changes:
            elif checkpoint == 1 and memory.main.get_map() == 256:
                checkpoint += 1
            elif checkpoint == 3 and memory.main.get_map() == 162:
                checkpoint += 1
            elif checkpoint == 11 and memory.main.get_map() == 256:
                checkpoint += 1
            elif checkpoint == 14:
                memory.main.click_to_event_temple(6)
                checkpoint += 1
            elif checkpoint == 16:
                return_to_airship()

            # General pathing
            elif (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.tp_farm(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                if cap_num == 10:
                    battle_farm_all(yuna_attack=False)
                else:
                    battle_farm_all()
                memory.main.arena_farm_check(
                    zone="tPlains", end_goal=cap_num, report=True
                )
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()
    logger.debug("End of Thunder Plains section")
    return memory.main.arena_farm_check(zone="tPlains", end_goal=cap_num, report=False)


def woods_next(end_goal: int):
    next1 = rng_track.coming_battles(area="lake_macalania", battle_count=2)[0]
    next2 = rng_track.coming_battles(area="macalania_woods", battle_count=2)[0]
    farm_array1 = memory.main.arena_farm_check(
        zone="maclake", end_goal=end_goal, return_array=True
    )
    farm_array2 = memory.main.arena_farm_check(
        zone="macwoods", end_goal=end_goal, return_array=True
    )

    logger.debug("Next battles:")
    logger.debug(next1)
    logger.debug(next2)
    logger.debug(farm_array1)
    logger.debug(farm_array2)

    if memory.main.get_yuna_mp() < 30:
        return 4
    if farm_array2[4] < end_goal and "chimera" in next2:
        return 2
    if farm_array2[5] < end_goal and "xiphos" in next2:
        return 2
    if farm_array1[3] < end_goal and "evil_eye" in next1:
        return 1
    if farm_array1[0] < end_goal and "mafdet" in next1:
        return 1
    if memory.main.get_yuna_mp() < 30:
        return 3
    if memory.main.arena_farm_check(
        zone="maclake", end_goal=end_goal
    ) and memory.main.arena_farm_check(zone="macwoods", end_goal=end_goal):
        return 4
    logger.debug("Couldn't find a special case")
    return 2


def mac_woods(cap_num: int = 10):
    air_ship_destination(dest_num=9)
    menu.remove_all_nea()
    pref_area = woods_next(end_goal=cap_num)
    logger.debug(f"Next area: {pref_area}")

    checkpoint = 0
    while not memory.main.get_map() in [194, 374]:
        if memory.main.user_control():
            if pref_area in [3, 4]:
                if checkpoint in [4, 5]:
                    checkpoint = 6
                elif checkpoint in [12, 13]:
                    checkpoint = 14
            elif checkpoint in [4, 5] and pref_area != 1:
                checkpoint = 6
            elif checkpoint in [6, 20] and pref_area == 1:
                checkpoint = 4
            elif checkpoint in [14] and pref_area == 2:
                checkpoint = 12

            # Map changes:
            if checkpoint in [2, 19] and memory.main.get_map() == 164:
                checkpoint += 1
            elif checkpoint in [6, 14] and memory.main.get_map() == 221:
                checkpoint += 1
            elif checkpoint == 11 and memory.main.get_map() == 242:
                checkpoint += 1
            elif checkpoint in [10, 15] and pref_area in [3, 4]:
                if pref_area == 3:
                    save_sphere.touch_and_go()
                    pref_area = woods_next(end_goal=cap_num)
                    logger.debug(f"Next area: {pref_area}")
                    if pref_area == 1:
                        checkpoint = 15
                    else:
                        checkpoint = 10
                else:
                    return_to_airship()

            # General pathing
            elif (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.mac_farm(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle_farm_all(yuna_attack=False)
                pref_area = woods_next(end_goal=cap_num)
                logger.debug(f"Next area: {pref_area}")
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()


def bikanel_next(end_goal: int):
    next1 = rng_track.coming_battles(area="sanubia_desert_(central)", battle_count=1)[0]
    next2 = rng_track.coming_battles(area="sanubia_desert_(ruins)", battle_count=1)[0]
    next3 = rng_track.coming_battles(area="sanubia_desert_(west)", battle_count=1)[0]
    farm_array = memory.main.arena_farm_check(
        zone="bikanel", end_goal=end_goal, return_array=True
    )

    logger.debug("Next three battles:")
    logger.debug(next1)
    logger.debug(next2)
    logger.debug(next3)

    if memory.main.get_yuna_mp() < 30:
        return 4
    if farm_array[5] < end_goal and "cactuar" in next1:
        return 1
    if farm_array[5] < end_goal and "cactuar" in next2:
        return 2
    if farm_array[5] < end_goal and "cactuar" in next3:
        return 3
    if farm_array[4] < end_goal and "mushussu" in next1:
        return 1
    if farm_array[4] < end_goal and "mushussu" in next3:
        return 3
    if farm_array[3] < end_goal and "sand_worm" in next1:
        return 1
    if farm_array[3] < end_goal and "sand_worm" in next2:
        return 2
    if farm_array[3] < end_goal and "sand_worm" in next3:
        return 3
    if farm_array[2] < end_goal and "zu" in next1:
        return 1
    if farm_array[2] < end_goal and "zu" in next2:
        return 2
    if farm_array[2] < end_goal and "zu" in next3:
        return 3
    if farm_array[0] < end_goal and "sand_wolf" in next1:
        return 1
    if farm_array[0] < end_goal and "sand_wolf" in next2:
        return 2
    if farm_array[0] < end_goal and "sand_wolf" in next3:
        return 3
    if memory.main.arena_farm_check(zone="bikanel", end_goal=end_goal):
        return 4

    logger.debug("Could not find a desirable encounter.")
    if memory.main.get_map() == 138:
        return 3
    else:
        return 1  # Prefer zone 1 for remaining battles.


def bikanel(cap_num: int = 10):
    air_ship_destination(dest_num=10)
    menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    ne_armor = True
    pref_area = bikanel_next(end_goal=cap_num)
    logger.debug(f"Next area: {pref_area}")
    memory.main.full_party_format("initiative")

    checkpoint = 0
    while not memory.main.get_map() in [194, 374]:
        if memory.main.user_control():
            # NEA stuff
            if pref_area == 4 and not ne_armor:
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                ne_armor = True
            elif checkpoint in [27, 28] and pref_area != 1:
                checkpoint = 29
            elif checkpoint in [28, 29, 30] and pref_area in [1, 2] and ne_armor:
                menu.remove_all_nea()
                bikanel_next(end_goal=cap_num)
                ne_armor = False
            elif checkpoint < 33 and pref_area == 3 and not ne_armor:
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                ne_armor = True
            elif checkpoint in [34, 35] and pref_area == 3 and ne_armor:
                menu.remove_all_nea()
                bikanel_next(end_goal=cap_num)
                ne_armor = False
            elif checkpoint in [34, 35] and pref_area != 3 and not ne_armor:
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                checkpoint = 36
                ne_armor = True
            elif checkpoint == 40 and pref_area != 4:
                menu.remove_all_nea()
                bikanel_next(end_goal=cap_num)
                ne_armor = False
                if pref_area == 1:
                    checkpoint = 28
                else:
                    checkpoint = 29

            # Checkpoint updates
            if pref_area == 1 and checkpoint in [29, 30]:
                checkpoint -= 2
            elif pref_area == 2 and checkpoint == 31:
                checkpoint -= 2
            elif pref_area == 3 and checkpoint == 36:
                checkpoint -= 2
            # Skip running into the next area. Straight to save sphere.
            elif pref_area == 4 and checkpoint < 31:
                checkpoint = 40

            # Map changes:
            if checkpoint == 5 and memory.main.get_map() == 136:
                checkpoint += 1
            elif checkpoint in [22, 36] and memory.main.get_map() == 137:
                checkpoint += 1
            elif checkpoint == 33 and memory.main.get_map() == 138:
                checkpoint += 1
            elif checkpoint == 44:
                return_to_airship()

            # General pathing
            elif (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.bikanel_farm(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                battle_farm_all(yuna_attack=False)
                memory.main.arena_farm_check(
                    zone="bikanel", end_goal=cap_num, report=True
                )
                hp_check = memory.main.get_hp()
                if hp_check[0] < 800:
                    battle.main.heal_up(3)
                pref_area = bikanel_next(end_goal=cap_num)
                logger.debug(f"Next area: {pref_area}")
                memory.main.full_party_format("initiative")
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()
    init_array = memory.main.check_ability(ability=0x8002)
    if init_array[4]:
        menu.equip_weapon(character=4, ability=0x8002)  # Initiative
        memory.main.full_party_format("initiative")


def calm_next(end_goal: int, force_levels: int):
    next1 = rng_track.coming_battles(area="calm_lands_(south)", battle_count=1)[0]
    next2 = rng_track.coming_battles(
        area="calm_lands_(central-north-east)", battle_count=1
    )[0]
    next3 = rng_track.coming_battles(area="calm_lands_(north-west)", battle_count=1)[0]
    farm_array = memory.main.arena_farm_check(
        zone="calm", end_goal=end_goal, return_array=True
    )

    logger.debug("Next three battles:")
    logger.debug(next1)
    logger.debug(next2)
    logger.debug(next3)

    if memory.main.get_yuna_mp() < 30:
        return 4
    if farm_array[4] < end_goal and "malboro" in next2:
        return 2
    if farm_array[4] < end_goal and "malboro" in next3:
        return 3
    if farm_array[0] < end_goal and "shred" in next1:
        return 1
    if farm_array[0] < end_goal and "shred" in next2:
        return 2
    if farm_array[0] < end_goal and "shred" in next3:
        return 3
    if farm_array[8] < end_goal and "anacondaur" in next1:
        return 1
    if farm_array[8] < end_goal and "anacondaur" in next2:
        return 2
    if farm_array[8] < end_goal and "anacondaur" in next3:
        return 3
    if farm_array[5] < end_goal and "ogre" in next1:
        return 1
    if farm_array[5] < end_goal and "ogre" in next2:
        return 2
    if farm_array[5] < end_goal and "ogre" in next3:
        return 3
    if farm_array[6] < end_goal and "chimera_brain" in next1:
        return 1
    if farm_array[6] < end_goal and "chimera_brain" in next2:
        return 2
    if farm_array[6] < end_goal and "chimera_brain" in next3:
        return 3
    if farm_array[7] < end_goal and "coeurl" in next1:
        return 1
    if farm_array[7] < end_goal and "coeurl" in next2:
        return 2
    if farm_array[7] < end_goal and "coeurl" in next3:
        return 3
    if memory.main.arena_farm_check(zone="calm", end_goal=end_goal):
        if memory.main.get_yuna_mp() < 30:
            return 9
        if force_levels > game_vars.nem_checkpoint_ap():
            logger.debug("Area complete, but need more levels")
            # Need extra AP to reach Quick Attack
            # Overdrive > AP gives us the most per kill.
            if len(next3) > len(next2) and len(next3) > len(next1):
                return 3
            if len(next1) > len(next2) and len(next1) > len(next3):
                return 1
            return 2
        return 9
    return 2


def calm(cap_num: int = 1, auto_haste=False, airship_return=True, force_levels=0):
    air_ship_destination(dest_num=12)
    menu.remove_all_nea()
    memory.main.full_party_format("yuna")
    ne_armor = False
    pref_area = calm_next(end_goal=cap_num, force_levels=force_levels)
    logger.debug(f"Next area: {pref_area}")

    ne_armor = False

    checkpoint = 0
    while not memory.main.get_map() == 307:
        if memory.main.user_control():
            if not ne_armor and pref_area == 9:
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                ne_armor = True
            elif pref_area == 9 and not ne_armor:
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                ne_armor = True

            if pref_area == 1 and checkpoint in [4, 5, 10]:
                checkpoint = 2
            elif pref_area in [2, 3, 4, 5, 6] and pref_area == 9:
                checkpoint = 10
            elif pref_area == 2 and checkpoint == 9:
                checkpoint = 4
            elif pref_area == 3 and checkpoint == 8:
                checkpoint = 6
            elif checkpoint in [6, 7] and pref_area != 3:
                checkpoint = 8
            elif checkpoint == 10:  # Ride the bird back to arena
                arena_return(checkpoint=1)

            elif (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.calm_farm(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            allCounts = memory.main.arena_array()
            if memory.main.battle_active():
                if (
                    memory.main.get_encounter_id() == 281
                    and game_vars.nem_checkpoint_ap() < 8
                ):
                    if min(allCounts[13], allCounts[19]) >= cap_num:
                        battle.main.flee_all()
                    else:
                        battle_farm_all()
                elif (
                    memory.main.get_encounter_id() == 283
                    and game_vars.nem_checkpoint_ap() < 8
                ):
                    if min(allCounts[4], allCounts[19], allCounts[33]) >= cap_num:
                        battle.main.flee_all()
                    else:
                        battle_farm_all()
                elif (
                    memory.main.get_encounter_id() == 284
                    and allCounts[33] >= cap_num
                    and game_vars.nem_checkpoint_ap() < 8
                ):
                    battle.main.flee_all()
                else:
                    if cap_num == 10:
                        battle_farm_all(yuna_attack=False)
                    else:
                        battle_farm_all()
                memory.main.full_party_format("yuna")
                battle.main.heal_up(3)
                pref_area = calm_next(end_goal=cap_num, force_levels=force_levels)
                logger.debug(f"Next area: {pref_area}")
                memory.main.arena_farm_check(zone="calm", end_goal=cap_num, report=True)

            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()
    if airship_return:
        return_to_airship()
    if force_levels > game_vars.nem_checkpoint_ap():
        return False
    return memory.main.arena_farm_check(zone="calm", end_goal=cap_num, report=False)


def calm_old(cap_num: int = 1, auto_haste=False, airship_return=True):
    air_ship_destination(dest_num=12)
    menu.remove_all_nea()

    ne_armor = False

    checkpoint = 0
    while not memory.main.get_map() == 307:
        if memory.main.user_control():
            if not ne_armor and memory.main.get_yuna_mp() < 30:
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                ne_armor = True
            if (
                memory.main.arena_farm_check(
                    zone="calm", end_goal=cap_num, report=False
                )
                and checkpoint < 5
            ):
                checkpoint = 5
            elif checkpoint == 5 and not memory.main.arena_farm_check(
                zone="calm", end_goal=cap_num, report=False
            ):
                checkpoint -= 2
            elif memory.main.arena_farm_check(
                zone="calm2", end_goal=cap_num, report=False
            ) and checkpoint in [8, 9]:
                checkpoint = 10
            elif checkpoint == 10 and not memory.main.arena_farm_check(
                zone="calm2", end_goal=cap_num, report=False
            ):
                checkpoint -= 2
            elif (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.calm(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            allCounts = memory.main.arena_array()
            if memory.main.battle_active():
                if (
                    memory.main.get_encounter_id() == 281
                    and game_vars.nem_checkpoint_ap() < 8
                ):
                    if min(allCounts[13], allCounts[19]) >= cap_num:
                        battle.main.flee_all()
                    else:
                        battle_farm_all()
                elif (
                    memory.main.get_encounter_id() == 283
                    and game_vars.nem_checkpoint_ap() < 8
                ):
                    if min(allCounts[4], allCounts[19], allCounts[33]) >= cap_num:
                        battle.main.flee_all()
                    else:
                        battle_farm_all()
                elif (
                    memory.main.get_encounter_id() == 284
                    and allCounts[33] >= cap_num
                    and game_vars.nem_checkpoint_ap() < 8
                ):
                    battle.main.flee_all()
                else:
                    if cap_num == 10:
                        battle_farm_all(yuna_attack=False)
                    else:
                        battle_farm_all()
                battle.main.heal_up(3)
                if checkpoint < 6:
                    memory.main.arena_farm_check(
                        zone="calm", end_goal=cap_num, report=True
                    )
                else:
                    memory.main.arena_farm_check(
                        zone="calm2", end_goal=cap_num, report=True
                    )

            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()
    if not memory.main.arena_farm_check(zone="calm3", end_goal=cap_num, report=False):
        return_to_airship()
    elif airship_return:
        return_to_airship()
    return memory.main.arena_farm_check(zone="calm3", end_goal=cap_num, report=False)


def gagazet_next(end_goal: int):
    next1 = rng_track.coming_battles(area="gagazet_(mountain)", battle_count=2)[0]
    next2 = rng_track.coming_battles(area="gagazet_(cave)", battle_count=2)[0]
    next3 = rng_track.coming_battles(area="zanarkand_(overpass)", battle_count=2)[0]
    next4 = rng_track.coming_battles(area="gagazet_(underwater)", battle_count=2)[0]
    farm_array = memory.main.arena_farm_check(
        zone="gagazet", end_goal=end_goal, return_array=True
    )

    logger.debug("Next battles:")
    logger.debug(next1)
    logger.debug(next2)
    logger.debug(next3)
    logger.debug(next4)
    logger.debug(farm_array)

    if memory.main.get_yuna_mp() < 30:
        return 8
    if farm_array[0] < end_goal and "bandersnatch" in next2:
        return 2
    if farm_array[0] < end_goal and "bandersnatch" in next1:
        return 1
    if farm_array[9] < end_goal and "behemoth" in next2:
        return 2
    if farm_array[9] < end_goal and "behemoth" in next3:
        return 3
    if farm_array[1] < end_goal and "dark_flan" in next2:
        return 2
    if farm_array[1] < end_goal and "dark_flan" in next3:
        return 3
    if farm_array[10] < end_goal and "mandragora" in next2:
        return 2
    if farm_array[10] < end_goal and "mandragora" in next3:
        return 3
    if farm_array[6] < end_goal and "grendel" in next2:
        return 2
    if farm_array[6] < end_goal and "grendel" in next3:
        return 3
    if farm_array[2] < end_goal and "ahriman" in next2:
        return 2
    if farm_array[2] < end_goal and "ahriman" in next3:
        return 3
    if farm_array[7] < end_goal and "bashura" in next2:
        return 2
    if farm_array[7] < end_goal and "bashura" in next3:
        return 3
    if farm_array[11] < end_goal and "grenade" in next1:
        return 1
    if farm_array[3] < end_goal and "grat" in next1:
        return 1
    if farm_array[4] < end_goal and "achelous" in next4:
        return 4
    if farm_array[5] < end_goal and "maelspike" in next4:
        return 4
    if farm_array[8] < end_goal and "maelspike" in next4:
        return 4
    if farm_array[4] < end_goal and "splasher_3" in next4:
        return 4
    if memory.main.arena_farm_check(zone="gagazet", end_goal=end_goal):
        return 9
    logger.debug("Couldn't find a special case")
    if memory.main.get_map() == 225:
        return 3
    elif memory.main.get_map() == 244:
        return 1
    elif memory.main.get_map() == 310:
        return 4
    else:
        return 2


def gagazet(cap_num: int = 10):
    rin_equip_dump()
    air_ship_destination(dest_num=13)
    pref_area = gagazet_next(end_goal=cap_num)

    # Check if we need the extra Lv.4 key sphere. False == needed.
    if (
        memory.main.get_item_slot(84) == 255
        or memory.main.get_item_count_slot(memory.main.get_item_slot(84)) == 1
    ):
        retrieved_sphere = False
    else:
        retrieved_sphere = True

    if pref_area == 4:
        menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
        ne_armor = True
    else:
        menu.remove_all_nea()
        ne_armor = False
    logger.debug(f"Next area: {pref_area}")

    last_cp = 0
    checkpoint = 0
    cp_forward = True
    while not memory.main.get_map() in [194, 374]:
        if last_cp != checkpoint:
            logger.debug(f"Checkpoint reached: {checkpoint}")
            last_cp = checkpoint
        if memory.main.user_control():
            # Map changes
            if checkpoint == 9 and memory.main.get_map() == 310:
                checkpoint += 1
            elif checkpoint == 12 and memory.main.get_map() == 272:
                checkpoint += 1
            elif checkpoint in [23, 27] and memory.main.get_map() == 225:
                checkpoint = 24
            elif checkpoint == 26 and memory.main.get_map() == 313:
                checkpoint += 1
            elif checkpoint == 34 and memory.main.get_map() == 244:
                checkpoint += 1
            elif not retrieved_sphere and checkpoint in [35, 36, 37] and pref_area != 1:
                checkpoint = 44
            elif checkpoint == 37 and memory.main.get_map() == 259:
                checkpoint += 1
            if checkpoint in [20, 21, 22, 29, 30] and memory.main.get_map() == 259:
                if pref_area in [8, 9]:
                    checkpoint = 41
                else:
                    checkpoint = 1

            # Portal Combat
            if checkpoint == 2:
                while memory.main.user_control():
                    FFXC.set_movement(1, 1)
                FFXC.set_neutral()
                memory.main.wait_frames(30)
                if pref_area in [2, 4]:
                    xbox.tap_down()
                    checkpoint = 3
                else:
                    xbox.tap_up()
                    xbox.tap_up()
                    checkpoint = 22
                xbox.tap_b()
                memory.main.await_control()
                logger.debug(f"Updated checkpoint: {checkpoint}")
            if checkpoint == 21:
                while memory.main.user_control():
                    FFXC.set_movement(0, -1)
                FFXC.set_neutral()
                memory.main.click_to_control()
                memory.main.await_control()
                if pref_area in [8, 9]:
                    checkpoint = 41
                else:
                    checkpoint = 1
            elif checkpoint == 29:
                FFXC.set_movement(0, -1)
                memory.main.wait_frames(3)
                xbox.tap_b()
                xbox.tap_b()
                FFXC.set_neutral()
                if pref_area in [8, 9]:
                    checkpoint = 41
                else:
                    checkpoint = 1

            # Branches, decisions
            if checkpoint in [0, 1] and pref_area == 1:  # Straight to mountain path
                checkpoint = 30
            elif checkpoint == 40 and not pref_area in [8, 9]:
                checkpoint = 1
            elif pref_area == 1 and checkpoint == 37:
                checkpoint -= 2
            elif pref_area == 2 and checkpoint in [4, 20]:
                checkpoint = 18
            elif pref_area == 3 and checkpoint == 26:
                checkpoint -= 2
            elif pref_area == 4 and checkpoint == 12:
                checkpoint -= 2

            # Escapes for moving onward
            if checkpoint in [35, 36] and pref_area != 1:
                checkpoint = 37
            elif checkpoint in [18, 19] and pref_area != 2:
                if pref_area == 4:
                    checkpoint = 3
                else:
                    checkpoint = 20
            elif checkpoint in [24, 25] and pref_area != 3:
                checkpoint = 26
            elif checkpoint in [10, 11] and pref_area != 4:
                checkpoint = 12

            # NEA decisions
            if ne_armor and checkpoint in [7, 19, 23, 33]:
                menu.remove_all_nea()
                ne_armor = False
            elif not ne_armor and checkpoint == 15 and pref_area != 2:
                # No need to re-equip while coming back from swimming
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                ne_armor = True
            elif not ne_armor and checkpoint in [4, 55]:
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                ne_armor = True
            elif checkpoint == 44:
                if not ne_armor and cp_forward:
                    menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                    ne_armor = True
                elif ne_armor and not cp_forward:
                    menu.remove_all_nea()
                    ne_armor = False
                    checkpoint = 35  # back on track
                    cp_forward = True  # back on track

            # Opening chest
            if checkpoint == 78:
                memory.main.click_to_event_temple(1)
                cp_forward = False
                retrieved_sphere = True
                checkpoint -= 1

            # End decisions
            if checkpoint == 43:
                if pref_area == 8:
                    save_sphere.touch_and_go()
                    checkpoint = 0
                else:
                    return_to_airship()
            elif (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.gagazet(checkpoint)
                )
                == True
            ):
                if cp_forward:
                    checkpoint += 1
                else:
                    checkpoint -= 1
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                if cap_num == 10:
                    battle_farm_all(yuna_attack=False)
                else:
                    battle_farm_all()
                pref_area = gagazet_next(end_goal=cap_num)
                logger.debug(f"Next area: {pref_area}")
            elif memory.main.menu_open() or memory.main.diag_skip_possible():
                xbox.tap_b()
    logger.debug("Done with Swimmers, now ready for Path")


def fayth_next(endGoal: int):
    next1 = rng_track.coming_battles(area="cave_(white_zone)", battle_count=1)[0]
    next2 = rng_track.coming_battles(area="cave_(green_zone)", battle_count=1)[0]
    farm_array = memory.main.arena_farm_check(
        zone="stolenfayth", end_goal=endGoal, return_array=True
    )

    logger.debug("Next battles:")
    logger.debug("green: ", next2)
    logger.debug("white: ", next1)
    logger.debug("zone: ", farm_array)

    if farm_array[8] < endGoal and "tonberry" in next2:
        return 2
    if farm_array[4] < endGoal and "nidhogg" in next1:
        return 1
    if farm_array[4] < endGoal and "nidhogg" in next2:
        return 2
    if farm_array[7] < endGoal and "thorn" in next1:
        return 1
    if farm_array[2] < endGoal and "ghost" in next1:
        return 1
    if farm_array[2] < endGoal and "ghost" in next2:
        return 2
    if farm_array[3] < endGoal and "valaha" in next1:
        return 1
    if farm_array[3] < endGoal and "valaha" in next2:
        return 2
    if farm_array[0] < endGoal and "imp" in next1:
        return 1
    if farm_array[0] < endGoal and "imp" in next2:
        return 2
    if farm_array[1] < endGoal and "yowie" in next1:
        return 1
    if farm_array[1] < endGoal and "yowie" in next2:
        return 2
    if "coeurl" in next1:
        return 1
    if "coeurl" in next2:
        return 2
    if "malboro" in next1:
        return 1
    if "malboro" in next2:
        return 2
    if "magic_urn" in next1:  # Try to avoid urn
        return 2
    if "magic_urn" in next2:  # Try to avoid urn
        return 1
    if memory.main.arena_farm_check(zone="stolenfayth", end_goal=endGoal):
        return 4

    logger.debug("Could not find a desirable encounter.")
    return 1


def stolen_fayth_cave(cap_num: int = 10):
    air_ship_destination(dest_num=13)
    if not memory.main.equipped_weapon_has_ability(
        char_num=game_vars.ne_armor(), ability_num=0x801D
    ):
        menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    ne_armor = True
    pref_area = fayth_next(endGoal=cap_num)
    logger.debug(f"Next area: {pref_area}")

    checkpoint = 0
    while not memory.main.get_map() in [194, 374]:
        if memory.main.user_control():
            if pref_area == 4 and checkpoint in [25, 26, 27, 28, 29]:
                checkpoint = 30
                memory.main.full_party_format("initiative")
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                ne_armor = True
            elif pref_area in [1, 2, 3] and checkpoint in [25, 27] and ne_armor:
                menu.remove_all_nea()
                ne_armor = False
            elif checkpoint in [5, 14, 59]:
                memory.main.click_to_event_temple(4)
                checkpoint += 1
            elif checkpoint == 19:
                memory.main.click_to_event_temple(7)
                checkpoint += 1
            elif pref_area == 1 and checkpoint in [27, 28, 29]:
                checkpoint = 25
            elif pref_area == 2 and checkpoint == 25:
                checkpoint = 26
            elif pref_area == 2 and checkpoint == 30:
                checkpoint = 27
            elif checkpoint in [52, 53]:  # Glyph and Yojimbo
                FFXC.set_neutral()
                memory.main.wait_frames(5)
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(2)
                FFXC.set_neutral()
                memory.main.wait_frames(5)
                xbox.tap_b()
                memory.main.wait_frames(5)
                yojimbo_dialog()
                checkpoint = 54
            elif checkpoint == 55:  # Back to entrance
                FFXC.set_neutral()
                memory.main.wait_frames(5)
                FFXC.set_movement(0, -1)
                memory.main.wait_frames(2)
                FFXC.set_neutral()
                memory.main.wait_frames(5)
                xbox.tap_b()
                memory.main.wait_frames(5)
                checkpoint += 1
            elif checkpoint == 62:
                return_to_airship()
            elif (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.yojimbo(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                if memory.main.get_encounter_id() in [321, 329]:
                    # Do not engage the jar boys.
                    battle.main.flee_all()
                elif (
                    memory.main.get_encounter_id() == 327
                    and memory.main.arena_farm_check(
                        zone="justtonberry", end_goal=cap_num, report=False
                    )
                ):
                    # No need to die extra times on tonberries.
                    battle.main.flee_all()
                else:
                    battle_farm_all(fayth_cave=True)

                memory.main.click_to_control()
                hp_check = memory.main.get_hp()
                if hp_check[0] < 795:
                    battle.main.heal_up(3)
                pref_area = fayth_next(endGoal=cap_num)
                logger.debug(f"Next area: {pref_area}")
            elif memory.main.diag_skip_possible():
                xbox.tap_b()


def inside_sin(cap_num: int = 10):
    air_ship_destination(dest_num=0)
    menu.remove_all_nea()

    while memory.main.get_map() != 203:
        FFXC.set_movement(0, -1)
    FFXC.set_neutral()

    checkpoint = 0
    while not memory.main.get_map() in [194, 374]:
        if memory.main.user_control():
            # Events
            if memory.main.get_map() == 296:  # Seymour battle
                logger.debug("We've reached the Seymour screen.")
                memory.main.full_party_format("yuna")
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(30 * 5)
                FFXC.set_neutral()
                battle.boss.omnis()
                memory.main.click_to_control()
                memory.main.full_party_format("initiative")

            # End of first area logic
            elif memory.main.arena_farm_check(
                zone="sin1", end_goal=cap_num, report=False
            ) and checkpoint in [38, 39]:
                checkpoint = 40
            elif checkpoint == 40 and not memory.main.arena_farm_check(
                zone="sin1", end_goal=cap_num, report=False
            ):
                checkpoint -= 2
                logger.debug(f"Checkpoint reached: {checkpoint}")
            elif checkpoint < 41 and memory.main.get_map() == 204:
                checkpoint = 41

            # End of second area logic
            elif (
                memory.main.arena_farm_check(
                    zone="sin2", end_goal=cap_num, report=False
                )
                and checkpoint < 67
            ):
                checkpoint = 67
            elif checkpoint == 67 and not memory.main.arena_farm_check(
                zone="sin2", end_goal=cap_num, report=False
            ):
                checkpoint -= 2
                logger.debug(f"Checkpoint reached: {checkpoint}")
            elif checkpoint < 68 and memory.main.get_map() == 327:
                checkpoint = 68
            elif checkpoint == 69:
                return_to_airship()
            elif (
                checkpoint >= 65 and memory.main.get_tidus_mp() < 20
            ):  # Tidus low on MP
                nemesis.nemesis_pathing.set_movement([550, 485])
                memory.main.await_event()
                FFXC.set_neutral()
                memory.main.wait_frames(3)
                memory.main.await_control()
                save_sphere.touch_and_go()
                nemesis.nemesis_pathing.set_movement([-200, -525])
                memory.main.await_event()
                FFXC.set_neutral()
                checkpoint = 66

            # General Pathing
            elif (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.sin(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                screen.await_turn()
                advanced_battle_logic()
                if checkpoint < 40:
                    logger.debug("Ahrimans only:")
                    memory.main.arena_farm_check(
                        zone="sin1", end_goal=cap_num, report=True
                    )
                else:
                    memory.main.arena_farm_check(
                        zone="sin2", end_goal=cap_num, report=True
                    )
            elif memory.main.menu_open():
                xbox.tap_b()


def omega_ruins(cap_num: int = 10):
    nemesis.menu.rikku_provoke()
    menu.remove_all_nea()

    air_ship_destination(dest_num=13, force_omega=True)

    checkpoint = 0
    while not memory.main.get_map() in [194, 374]:
        if memory.main.user_control():
            if (
                memory.main.arena_farm_check(
                    zone="omega", end_goal=cap_num, report=False
                )
                and checkpoint < 2
            ):
                checkpoint = 2
            elif checkpoint == 2 and not memory.main.arena_farm_check(
                zone="omega", end_goal=cap_num, report=False
            ):
                checkpoint -= 2
                logger.debug(f"Checkpoint reached: {checkpoint}")
            elif memory.main.get_tidus_mp() < 20:
                save_sphere.touch_and_go()
            elif checkpoint == 3:
                return_to_airship()
            elif (
                nemesis.nemesis_pathing.set_movement(
                    nemesis.nemesis_pathing.omega(checkpoint)
                )
                == True
            ):
                checkpoint += 1
                logger.debug(f"Checkpoint reached: {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active():
                advanced_battle_logic()
                memory.main.arena_farm_check(
                    zone="omega", end_goal=cap_num, report=True
                )
                memory.main.click_to_control()
            elif memory.main.diag_skip_possible() or memory.main.menu_open():
                xbox.tap_b()


def get_equipment(equip=True):
    memory.main.wait_frames(20)
    xbox.tap_b()
    memory.main.wait_frames(5)
    xbox.tap_up()
    xbox.tap_b()
    memory.main.wait_frames(5)
    if equip == True:
        xbox.tap_up()
    xbox.tap_b()  # Equip weapon for Rikku
    memory.main.wait_frames(5)


def other_stuff():
    arena_npc()
    xbox.tap_b()
    return_to_airship()
