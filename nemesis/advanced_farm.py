import logging


import battle.boss
import battle.main
import battle.utils
import memory.main
from memory.main import get_map
import menu
from area.platinum import grid_check_early, next_blitzball
import nemesis.menu
from nemesis.arena_prep import (
    rin_equip_dump,
    battle_farm_all,
    battle_farm_defer,
    advanced_battle_logic,
    yojimbo_dialog,
    arena_return,
    zan_ready
)
import nemesis.arena_select
from nemesis.arena_select import (
    navigate_to_airship_destination,
    arena_return,
    distill_spheres,
    return_to_airship
)
from nemesis.arena_battles import one_eye_battle,vidatu_farm
import pathing
import rng_track
import save_sphere
import vars
import xbox
from json_ai_files.write_seed import write_custom_message, write_big_text, current_big_text
from paths.nem import (
    BikanelFarm,
    CalmFarm,
    DjoseFarm,
    GagazetMtPathFarm,
    GagazetCaveFarm,
    ZanarkandFarm2,
    KilikaFarm,
    MacFarm,
    MiihenFarm,
    OmegaFarm,
    SinFarm,
    ThunderPlainsFarm,
    YojimboFarm,
)
from players import Lulu, Rikku, Tidus, Wakka, Yuna
from gamestate import game
import json

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()
FFXC = xbox.controller_handle()
test_mode = False


def next_zone_check(phase: int = 3, current_zone: str = "none", advances: int = 0):
    # best_zone made up of [monster, zone, priority]
    best_zone = ["none", "any", -1, 0]
    if phase == 1:
        f = open("nemesis\\phase_one_monsters.json")
    elif phase == 3:
        f = open("nemesis\\phase_three_monsters.json")
    elif phase == 4:
        f = open("nemesis\\phase_four_monsters.json")
    elif phase == 5:
        f = open("nemesis\\phase_five_monsters.json")
    elif phase == 6:
        f = open("nemesis\\phase_six_monsters.json")
    elif phase == 7:
        f = open("nemesis\\phase_seven_monsters.json")
    elif phase == 8:
        f = open("nemesis\\phase_eight_monsters.json")
    elif phase == 9:
        f = open("nemesis\\plat_pre_five_monsters.json")
    else:
        return best_zone
    mon_list = json.load(f)
    mon_array = mon_list.keys()
    if phase in [4, 6]:
        check_zone = rng_track.singles_battles(area="mrr_-_valley")[advances]
        if "garuda" in check_zone:
            if memory.main.arena_array()[40] < 10:
                v1 = "garuda"
                v2 = "mrr_-_valley"
                v3 = 999
                best_zone = [v1, v2, v3, advances]
                return best_zone

    for key in mon_array:
        check_zone = rng_track.singles_battles(area=mon_list[key]["zone1"])[
            advances * 2
        ]
        if mon_list[key]["zone2"] != "none":
            check_zone_2 = rng_track.singles_battles(area=mon_list[key]["zone2"])[
                advances * 2
            ]
        else:
            check_zone_2 = "none"
        if mon_list[key]["zone3"] != "none":
            check_zone_3 = rng_track.singles_battles(area=mon_list[key]["zone3"])[
                advances * 2
            ]
        else:
            check_zone_3 = "none"
        check_mon = mon_list[key]["num"]
        check_count = mon_list[key]["need"]
        if memory.main.arena_array()[check_mon] >= check_count:
            # Do not need to continue farming if enough are captured.
            pass
        elif key.lower() in check_zone:
            if (
                mon_list[key]["prio"] == best_zone[2]
                and mon_list[key]["zone1"] == current_zone
            ):
                # Current area has first precedence. Sticky zones.
                if memory.main.arena_array()[check_mon] < check_count:
                    v1 = key
                    v2 = mon_list[key]["zone1"]
                    v3 = mon_list[key]["prio"]
                    best_zone = [v1, v2, v3, advances]
            elif mon_list[key]["prio"] > best_zone[2]:
                # Higher prio areas take second precedent
                if memory.main.arena_array()[check_mon] < check_count:
                    v1 = key
                    v2 = mon_list[key]["zone1"]
                    v3 = mon_list[key]["prio"]
                    best_zone = [v1, v2, v3, advances]
        elif check_zone_2 == "none":
            pass
        elif key.lower() in check_zone_2:
            if (
                mon_list[key]["prio"] == best_zone[2]
                and mon_list[key]["zone1"] == current_zone
            ):
                # Current area has second precedence.
                if memory.main.arena_array()[check_mon] < check_count:
                    v1 = key
                    v2 = mon_list[key]["zone2"]
                    v3 = mon_list[key]["prio"]
                    best_zone = [v1, v2, v3, advances]
            elif mon_list[key]["prio"] > best_zone[2]:
                # Higher prio areas take precedent
                if memory.main.arena_array()[check_mon] < check_count:
                    v1 = key
                    v2 = mon_list[key]["zone2"]
                    v3 = mon_list[key]["prio"]
                    best_zone = [v1, v2, v3, advances]
        elif check_zone_3 == "none":
            pass
        elif key.lower() in check_zone_3:
            if (
                mon_list[key]["prio"] == best_zone[2]
                and mon_list[key]["zone1"] == current_zone
            ):
                # Current area has second precedence.
                if memory.main.arena_array()[check_mon] < check_count:
                    v1 = key
                    v2 = mon_list[key]["zone3"]
                    v3 = mon_list[key]["prio"]
                    best_zone = [v1, v2, v3, advances]
            elif mon_list[key]["prio"] > best_zone[2]:
                # Higher prio areas take precedent
                if memory.main.arena_array()[check_mon] < check_count:
                    v1 = key
                    v2 = mon_list[key]["zone3"]
                    v3 = mon_list[key]["prio"]
                    best_zone = [v1, v2, v3, advances]
            # If record does not surpass on the precedence list, do nothing.
    return best_zone


def choose_next_zone(last_zone: str, phase: int):
    check_zone = next_zone_check(phase=phase, current_zone=last_zone, advances=0)

    # First, check for a One-eye battle that would be useful
    if (
        game_vars.platinum() and
        check_zone[1] == "any" and
        memory.main.get_item_slot(107) != 255 and  # Door to tomorrow x10 for OD>AP
        memory.main.get_item_count_slot(memory.main.get_item_slot(107)) >= 10
    ):
        if (
            (game.state == "Nem_Farm" and game.step >= 10) or
            (game.state == "Platinum" and game.step >= 3)
        ):
            next_item_aeon,_ = rng_track.item_to_be_dropped(enemy="one-eye",kill_pref="aeon")
            next_item_char,_ = rng_track.item_to_be_dropped(enemy="one-eye")
            if (
                32787 in next_item_aeon.equip_abilities and
                next_item_aeon.slots == 3 and
                game_vars.plat_triple_ap_check()[next_item_aeon.equip_owner_alt] == False
            ):
                check_zone = ["aeon", "one-eye", next_item_aeon.equip_owner_alt, 0]
                return check_zone
            elif (
                32787 in next_item_char.equip_abilities and
                next_item_char.slots == 3 and
                next_item_char.equip_owner != 9 and
                game_vars.plat_triple_ap_check()[next_item_aeon.equip_owner] == False
            ):
                check_zone = ["any", "one-eye", next_item_aeon.equip_owner, 0]
                return check_zone

    # If no Plat% - Triple-AP weapon with three slots, proceed with the farm.
    sticky = path_get_info(zone=str(last_zone))["sticky"]
    if check_zone[1] != last_zone:
        # Logic to prefer staying in the same area over constant bouncing.
        temp1 = next_zone_check(phase=phase, current_zone=last_zone, advances=1)
        temp2 = next_zone_check(phase=phase, current_zone=last_zone, advances=2)
        temp3 = next_zone_check(phase=phase, current_zone=last_zone, advances=3)
        if zone_to_zone(last_zone, check_zone[1])[0]:
            pass
        elif temp1[1] == last_zone:
            check_zone = temp1
        elif zone_to_zone(last_zone, temp1[1])[0]:
            check_zone = temp1
        elif sticky == "True":
            if temp2[1] == last_zone:
                check_zone = temp2
            elif zone_to_zone(last_zone, temp2[1])[0]:
                check_zone = temp2
            elif temp3[1] == last_zone:
                check_zone = temp3
            elif zone_to_zone(last_zone, temp3[1])[0]:
                check_zone = temp3
    
    return check_zone

def complete_check(phase: int = 3):
    if phase == 1:
        f = open("nemesis\\phase_one_monsters.json")
    elif phase == 3:
        f = open("nemesis\\phase_three_monsters.json")
    elif phase == 4:
        f = open("nemesis\\phase_four_monsters.json")
    elif phase == 5:
        f = open("nemesis\\phase_five_monsters.json")
    elif phase == 6:
        f = open("nemesis\\phase_six_monsters.json")
    elif phase == 7:
        f = open("nemesis\\phase_seven_monsters.json")
    elif phase == 8:
        f = open("nemesis\\phase_eight_monsters.json")
    elif phase == 9:
        f = open("nemesis\\plat_pre_five_monsters.json")
    else:
        return False

    mon_list = json.load(f)
    mon_array = mon_list.keys()

    for key in mon_array:
        check_mon = mon_list[key]["num"]
        check_count = mon_list[key]["need"]
        if memory.main.arena_array()[check_mon] < check_count:
            return False
    return True


def report_remaining(phase: int = 3):
    # Prep phase
    if phase == 1:
        f = open("nemesis\\phase_one_monsters.json")
    elif phase == 3:
        f = open("nemesis\\phase_three_monsters.json")
    elif phase == 4:
        f = open("nemesis\\phase_four_monsters.json")
    elif phase == 5:
        f = open("nemesis\\phase_five_monsters.json")
    elif phase == 6:
        f = open("nemesis\\phase_six_monsters.json")
    elif phase == 7:
        f = open("nemesis\\phase_seven_monsters.json")
    elif phase == 8:
        f = open("nemesis\\phase_eight_monsters.json")
    elif phase == 9:
        f = open("nemesis\\plat_pre_five_monsters.json")
    else:
        return
    mon_list = json.load(f)
    mon_array = mon_list.keys()
    total_need = 0
    complete_count = 0
    logger.debug("==== Advanced Farm status ====")

    # Report each monster we haven't completed, and keep summary tallies.
    for key in mon_array:
        check_mon = mon_list[key]["num"]
        check_count = mon_list[key]["need"]
        area = mon_list[key]["zone1"]
        current_count = memory.main.arena_array()[check_mon]
        total_need += check_count
        complete_count += min(check_count, current_count)
        #if current_count < check_count:
        #    logger.debug(f"{key}: {current_count} / {check_count} | {area}")

    complete_percent = int(complete_count / total_need * 100)
    logger.info(f"== Total: {complete_count} / {total_need} | {complete_percent}%")
    logger.debug("==============================")
    if phase == 4:
        write_custom_message(f"Nemesis stage 4 farm {complete_percent}%\n" + \
            f"Three Stars for One MP weap\nStam Tonics for gil manip\n" + \
            f"{game.state} | {game.step}")
    if phase == 5:
        write_custom_message(f"Nemesis stage 5 farm {complete_percent}%\n" + \
            f"Substage 1 of 3\nOmega Dungeon\n" + \
            f"{game.state} | {game.step}")
    if phase == 6:
        write_custom_message(f"Nemesis stage 5 farm {complete_percent}%\n" + \
            f"Substage 2 of 3\nMi'ihen Rares\n" + \
            f"{game.state} | {game.step}")
    if phase == 7:
        write_custom_message(f"Nemesis stage ? farm {complete_percent}%\n" + \
            f"TBD\nTBD\n" + \
            f"{game.state} | {game.step}")
    if phase == 8:
        write_custom_message(f"Nemesis stage 5 farm {complete_percent}%\n" + \
            f"Substage 3 of 3\n{complete_percent}%" + \
            f"{game.state} | {game.step}")
    if phase == 9:
        write_custom_message(f"Nemesis stage 4.5 farm {complete_percent}%\n" + \
            f"Specific unlocks for Grid nodes\n{complete_percent}%" + \
            f"{game.state} | {game.step}")


def report_need_single(phase: int, mon_name: str):
    if phase == 1:
        f = open("nemesis\\phase_one_monsters.json")
    elif phase == 3:
        f = open("nemesis\\phase_three_monsters.json")
    elif phase == 4:
        f = open("nemesis\\phase_four_monsters.json")
    elif phase == 5:
        f = open("nemesis\\phase_five_monsters.json")
    elif phase == 6:
        f = open("nemesis\\phase_six_monsters.json")
    elif phase == 7:
        f = open("nemesis\\phase_seven_monsters.json")
    elif phase == 8:
        f = open("nemesis\\phase_eight_monsters.json")
    elif phase == 9:
        f = open("nemesis\\plat_pre_five_monsters.json")
    else:
        return 99
    try:
        mon_list = json.load(f)
        key = mon_list[mon_name]["num"]
        completed = memory.main.arena_array()[key]
        return [completed, mon_list[mon_name]["need"]]
    except Exception:
        return [0, 0]


def get_zone_int(zone: str) -> int:
    if "_sin_" in zone:
        print("Returning Sin")
        return 0
    if "kilika" in zone:
        return 2
    if "mi'ihen" in zone:
        return 4
    if "clasko" in zone:
        return 4
    if "old_road" in zone:
        return 4
    if "mrr" in zone:
        return 4
    if "djose" in zone:
        return 5
    if "moonflow" in zone:
        return 5
    if "thunder_plains" in zone:
        return 8
    if "macalania" in zone:
        return 9
    if "sanubia" in zone:
        return 10
    if "calm" in zone:
        return 12
    if "omega" in zone:
        return 13
    if "gagazet" in zone:
        return 14
    if "_zone" in zone:  # gorge and cave
        return 14
    if "zanarkand" in zone:
        return 15
    return 99


def get_zone_airship_name(zone: str) -> str:
    if "_sin_" in zone:
        return "Sin"
    if "kilika" in zone:
        return "Kilika"
    if "mi'ihen" in zone:
        return "Mi'ihen Highroad"
    if "clasko" in zone:
        return "Mi'ihen Highroad"
    if "old_road" in zone:
        return "Mi'ihen Highroad"
    if "mrr" in zone:
        return "Mi'ihen Highroad"
    if "djose" in zone:
        return "Djose"
    if "moonflow" in zone:
        return "Djose"
    if "thunder_plains" in zone:
        return "Thunder Plains"
    if "macalania" in zone:
        return "Macalania"
    if "sanubia" in zone:
        return "Bikanel"
    if "calm" in zone:
        return "Calm Lands"
    if "omega" in zone:
        return "Omega"
    if "gagazet" in zone:
        return "Gagazet"
    if "_zone" in zone:  # gorge and cave
        return "Gagazet"
    if "zanarkand" in zone:
        return "Zanarkand"
    return "ERROR"


def full_farm(phase: int):
    last_zone = "none"
    menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    adjacent = [False, "none", "none"]

    if phase == 5:
        yoj_unlock = True
    else:
        yoj_unlock = False
    if phase == 1:
        memory.main.update_formation(Tidus, Yuna, Lulu)
    elif phase == 3:
        memory.main.update_formation(Tidus, Yuna, Wakka)
    else:
        memory.main.update_formation(Tidus, Wakka, Rikku)
    check_zone = choose_next_zone(last_zone=last_zone, phase=phase)

    while not complete_check(phase=phase):
        logger.debug(f"Zone name (A): {check_zone[1]}")
        counts = report_need_single(phase=phase, mon_name=check_zone[0])
        logger.debug(f"Mon (A): {check_zone[0]}: {counts[0]}/{counts[1]}")
        if not memory.main.equipped_weapon_has_ability(char_num=0,ability_num=0x807A):
            # if game.state == "Nem_Farm" and game.step >= 10:
            #     menu.equip_weapon(character=0, ability=0x800D,full_menu_close=True)
            # else:
            menu.equip_weapon(character=0, ability=0x807A,full_menu_close=True)

        next_text = current_big_text()
        if len(next_text) != 0:
            if check_zone[1] == "any":
                next_text += f"\n - Next Zone: {check_zone[1]}"
                next_text += f"\n - General battle logic to advance RNG"
            else:
                next_text += f"\n - Next Zone: {check_zone[1]}"
                next_text += f"\n - Monster: {check_zone[0]}: {counts[0]}/{counts[1]}"
            write_big_text(next_text)

        if check_zone[1] == "any":
            if get_map() == 374:
                if phase == 5:
                    check_zone[1] = "omega_ruins_(sphere)"
                    last_zone = check_zone[1]
                else:
                    # If no other choice, default to Macalania. Most farms have something there.
                    check_zone[1] = "lake_macalania"
                    last_zone = check_zone[1]
            else:
                check_zone[1] = last_zone
        
        if check_zone[1] == "one-eye":
            if get_map() == 307:
                pass
            elif get_map() != 374:
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                return_to_airship()
            if get_map() == 374:
                arena_return()
            one_eye_battle(killer=check_zone[0],drops_for=check_zone[2],cap_weap=False)
            vidatu_farm()
            return_to_airship()
            memory.main.await_control()
            check_zone = choose_next_zone(last_zone="none", phase=phase)
        else:
            if get_map() == 374:
                logger.debug(f"P.down Slot: {memory.main.get_item_slot(6)}")
                logger.debug(
                    "P.down Count: "
                    + f"{memory.main.get_item_count_slot(memory.main.get_item_slot(6))}"
                )
                if memory.main.get_item_count_slot(memory.main.get_item_slot(6)) < 30:
                    rin_equip_dump(stock_downs=True)
                mana = memory.main.get_item_count_slot(memory.main.get_item_slot(17))
                if phase == 5 and mana < 4 and game_vars.platinum():
                    arena_return()
                    distill_spheres()
                    return_to_airship()
                zone_int = get_zone_int(zone=check_zone[1])
                zone_name = get_zone_airship_name(zone=check_zone[1])
                logger.debug(f"Landing in zone number {zone_int}")
                # air_ship_destination(dest_num=zone_int)
                navigate_to_airship_destination(destination_name=zone_name)
                report_remaining(phase=phase)
                counts = report_need_single(phase=phase, mon_name=check_zone[0])
                logger.info(f"Target (B): {check_zone[0]}: {counts[0]}/{counts[1]}")
                path_to_battle(zone=check_zone[1])
                menu.remove_all_nea()
            elif adjacent[0] and last_zone != check_zone[1]:
                logger.debug("=== Moving adjacent")
                path_to_battle(
                    zone=check_zone[1], checkpoint=adjacent[1], direction=adjacent[2]
                )
                menu.remove_all_nea()
            else:
                logger.debug("=== Staying in same zone")

            last_zone = check_zone[1]
            report_remaining(phase=phase)
            counts = report_need_single(phase=phase, mon_name=check_zone[0])
            logger.info(
                f"Target (C): {check_zone[0]}: {counts[0]}/{counts[1]} | {check_zone[3]}"
            )
            battle_start(zone=check_zone[1])
            check_zone = choose_next_zone(last_zone=last_zone, phase=phase)
            battle.main.wrap_up()
            report_remaining(phase=phase)
            if phase == 3:
                memory.main.update_formation(Tidus, Yuna, Wakka, full_menu_close=False)
            else:
                memory.main.update_formation(Tidus, Wakka, Rikku, full_menu_close=False)
            if memory.main.get_hp()[0] < 1100 and memory.main.get_map() != 310:
                # Low health, but not swimming
                battle.main.heal_up(3)
            memory.main.close_menu()
            if phase < 5:
                nemesis.menu.perform_next_grid()
            elif game_vars.platinum():
                grid_check_early()
            logger.info(f"Loop (C), phase {phase}")

            logger.debug(f"Zone name (D): {check_zone[1]}")
            counts = report_need_single(phase=phase, mon_name=check_zone[0])
            logger.debug(f"Mon (D): {check_zone[0]}: {counts[0]}/{counts[1]}")
            adjacent = zone_to_zone(last_zone, check_zone[1])
            logger.debug(f"Adjacent: {adjacent}")
            shadow_slot = memory.main.get_item_slot(41)
            if shadow_slot == 255:
                shadow_count = 0
            else:
                shadow_count = memory.main.get_item_count_slot(shadow_slot)
            if shadow_count < 8 and game.state == "Nem_Farm" and game.step >= 10:
                # Out of shadow gems
                logger.info("Out of shadow gems, let's go get some more.")
                path_to_save(zone=last_zone)
                return_to_airship()
                logger.warning("Attempting to return to arena.")
                arena_return()
                while shadow_count < 8:
                    nemesis.arena_select.arena_npc()
                    nemesis.arena_select.arena_menu_select(1)
                    nemesis.arena_select.start_fight(area_index=7, monster_index=4)
                    battle.main.shadow_gem_farm()
                    nemesis.arena_select.arena_menu_select(4)
                    shadow_slot = memory.main.get_item_slot(41)
                    if shadow_slot == 255:
                        shadow_count = 0
                    else:
                        shadow_count = memory.main.get_item_count_slot(shadow_slot)
                return_to_airship()
                return full_farm(phase=phase)
            mp_slot = memory.main.get_item_slot(86)
            if mp_slot == 255:
                mp_count = 0
            else:
                mp_count = memory.main.get_item_count_slot(mp_slot)
            
            # Optional report
            logger.debug(f"== Tidus: {memory.main.get_tidus_mp()} / {min(20,Tidus.max_mp())}")
            logger.debug(f"== Yuna: {memory.main.get_yuna_mp()} / {min(50,Yuna.max_mp())}")
            logger.debug(f"== Rikku: {memory.main.get_rikku_mp()} / {min(20,Rikku.max_mp())}")
            
            if mp_count < 4 and game.state == "Nem_Farm" and game.step >= 10 and game_vars.platinum():
                # Out of MP spheres
                logger.info("Low on MP spheres, let's go get some more.")
                path_to_save(zone=last_zone)
                return_to_airship()
                logger.warning("Attempting to return to arena.")
                arena_return()
                menu.equip_weapon(character=0, ability=32772,full_menu_close=True)  # Evade & Counter (Caldabolg)
                vidatu_farm()
                return_to_airship()
                menu.equip_weapon(character=0, ability=32781,full_menu_close=True)  # One MP cost (capture)
                return full_farm(phase=phase)
            elif (
                memory.main.get_tidus_mp() < min(20,Tidus.max_mp()) and
                memory.main.get_map() in [203,204]
            ):
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                logger.debug("== Out of mana for Tidus, returning to save sphere.")
                logger.debug(f"== Tidus: {memory.main.get_tidus_mp()} / {min(20,Tidus.max_mp())}")
                path_to_save(zone=last_zone)
                save_sphere.touch_and_go()
                last_zone = "inside_sin_(front)"
                check_zone = choose_next_zone(last_zone=last_zone, phase=phase)
                logger.warning(f"Sin Zones check: {last_zone} > {check_zone[1]}")
                adjacent = zone_to_zone(last_zone, check_zone[1])
                if check_zone[1] == last_zone:
                    menu.remove_all_nea()
            elif (
                memory.main.get_tidus_mp() < min(20,Tidus.max_mp()) or
                memory.main.get_yuna_mp() < min(50,Yuna.max_mp()) or
                memory.main.get_rikku_mp() < min(20,Rikku.max_mp())
            ):
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                logger.debug("== Out of mana, returning to save sphere.")
                logger.debug(f"== Tidus: {memory.main.get_tidus_mp()} / {min(20,Tidus.max_mp())}")
                logger.debug(f"== Yuna: {memory.main.get_yuna_mp()} / {min(50,Yuna.max_mp())}")
                logger.debug(f"== Rikku: {memory.main.get_rikku_mp()} / {min(20,Rikku.max_mp())}")
                path_to_save(zone=last_zone)
                force_save = phase == 5
                return_to_airship(extra_save=force_save)
                if game_vars.platinum():
                    if phase >= 5:
                        grid_check_early()
                    next_blitzball()
                    logger.info(f"Loop (B), phase {phase}")
                if len(memory.main.all_equipment()) > 150:
                    rin_equip_dump()
            elif adjacent[0]:
                if adjacent[3] == "True":
                    menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
            elif check_zone[1] != last_zone and check_zone[1] != "any":
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                logger.info(f"== Moving to zone: {check_zone[1]}")
                logger.info(f"Mon (A): {check_zone[0]}")
                if (
                    "cave" in last_zone and 
                    phase == 4 and 
                    not game_vars.yojimbo_unlocked() and 
                    memory.main.get_gil_value() >= 550000
                ):
                    path_to_yojimbo()
                else:
                    path_to_save(zone=last_zone)
                    return_to_airship()
                if game_vars.platinum():
                    if phase >= 5:
                        grid_check_early()
                    next_blitzball()
                    logger.info(f"Loop (A), phase {phase}")
                if len(memory.main.all_equipment()) > 150:
                    rin_equip_dump()
            elif complete_check(phase=phase):
                menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
                logger.debug("== Farming complete, returning to airship.")
            else:
                pass

    if get_map() != 374:
        path_to_save(zone=last_zone)
        return_to_airship()
        if game_vars.platinum():
            if phase >= 5:
                grid_check_early()
            next_blitzball()
    logger.info(f"End of farm section, phase {phase}")
    if len(memory.main.all_equipment()) > 150 or phase in [5,6,7]:
        rin_equip_dump(sell_nea=True)


def zone_to_zone(last_zone: str, next_zone: str):
    f = open("nemesis\\adjacent_zones.json")
    # Convert the zone into path_info
    array = json.load(f)
    try:
        if last_zone in array.keys():
            if next_zone in array[last_zone].keys():
                logger.warning(f"== Adjacent zone identified: {next_zone}")
                c = array[last_zone][next_zone]["checkpoint"]
                d = array[last_zone][next_zone]["direction"]
                nea = array[last_zone][next_zone]["nea"]
                logger.warning([True, c, d, nea])
                #memory.main.wait_frames(90)
                return [True, c, d, nea]
        return [False, "none", "none", "True"]
    except Exception:
        return [False, "none", "none", "True"]


def path_get_info(zone: str):
    f = open("nemesis\\zone_to_path.json")
    # Convert the zone into path_info
    path_info = json.load(f)
    try:
        return path_info[zone]
    except Exception:
        return path_info["zanarkand_(overpass)"]


def path_to_battle(zone: str, checkpoint: int = 0, direction: str = "f"):
    path_info = path_get_info(zone=zone)
    zone_num = get_zone_int(zone=zone)
    last_map = get_map()
    logger.debug(f"Zone/Path: {zone}")

    while checkpoint not in range(path_info["first_battle"], path_info["last_battle"]):
        if memory.main.battle_active():
            FFXC.set_neutral()
            advanced_battle_logic()
        elif get_map() != last_map:
            if direction == "f":
                checkpoint += 2
            else:
                checkpoint -= 2
            FFXC.set_neutral()
            logger.debug(f"Checkpoint update: {checkpoint}")
            last_map = get_map()
        elif checkpoint == path_info["sphere"] and memory.main.get_tidus_mp() < 50:
            save_sphere.touch_and_go()
        elif zone_num == 0:  # Sin
            if zone == "inside_sin_(front)":
                if get_map() == 204:
                    checkpoint = 44
                    direction = "b"
                elif checkpoint > 42:
                    checkpoint = 42
                    direction = "b"
                elif checkpoint < 40 and direction == 'b':
                    direction = "f"
            if zone == "inside_sin_(back)":
                if get_map() == 203 and direction == 'b':
                    direction = 'f'
                elif get_map() == 204 and checkpoint < 45:
                    checkpoint = 45
                    direction = 'f'
                elif checkpoint > 46:
                    checkpoint = 44
                
            if get_map() == 296:
                FFXC.set_neutral()
                logger.debug("We've reached the Seymour screen.")
                memory.main.update_formation(Tidus, Yuna, Lulu)
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                FFXC.set_neutral()
                battle.boss.omnis()
                memory.main.click_to_control()
                memory.main.update_formation(Tidus, Wakka, Rikku)
                menu.remove_all_nea()
            elif pathing.set_movement(SinFarm.execute(checkpoint)) is True:
                if direction == "b":
                    checkpoint -= 1
                else:
                    checkpoint += 1
                logger.debug(f"Checkpoint (C) {checkpoint}")
        elif zone_num == 2:  # Kilika
            if pathing.set_movement(KilikaFarm.execute(checkpoint)) is True:
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 4:  # Miihen/MRR
            # logger.warning(memory.main.controlled_actor_id())
            if checkpoint == 39:  # and memory.main.controlled_actor_id() == 20531:
                xbox.tap_a()
            if checkpoint == 38 and direction == "b":
                checkpoint -= 1
            if zone == "mrr_-_valley" and checkpoint == 63:
                checkpoint = 62
            if checkpoint == 5:  # Chocobo lady
                pathing.approach_actor_by_id(actor_id=8279)
                FFXC.set_neutral()
                memory.main.click_to_diag_progress(48)
                memory.main.click_to_control()
                checkpoint += 1
            elif checkpoint == 29:
                # logger.warning(memory.main.get_actors_loaded())
                if (
                    20531 in memory.main.get_actors_loaded()
                ):  # and zone == "mi'ihen_(newroad)":
                    logger.warning("Dismounting (A)")
                    FFXC.set_neutral()
                    xbox.tap_a()
                    xbox.tap_a()
                    xbox.tap_a()
                    xbox.tap_a()
                    xbox.tap_a()
                    memory.main.await_control()
                checkpoint += 1
            elif pathing.set_movement(MiihenFarm.execute(checkpoint)) is True:
                if direction == "f":
                    checkpoint += 1
                    if checkpoint == 35 and zone in [
                        "clasko_skip_screen",
                        "mrr_-_valley",
                    ]:
                        checkpoint = 49
                    if checkpoint in [4, 5] and zone == "mi'ihen_screen_2-3":
                        checkpoint = 201
                else:
                    checkpoint -= 1
                    if checkpoint in [49,82] and zone == "mi'ihen_(newroad)":
                        checkpoint = 35
                    if checkpoint == 44 and zone == "old_road":
                        checkpoint = 37
                        direction = "f"
                    if checkpoint > 190 and get_map() == 171:
                        checkpoint = 2
                    if checkpoint == 201 and zone in (
                        "mi'ihen_(newroad)",
                        "old_road",
                        "clasko_skip_screen",
                        "mrr_-_valley",
                    ):
                        checkpoint = 6
                        direction = "f"
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 5:  # Djose
            if pathing.set_movement(DjoseFarm.execute(checkpoint)) is True:
                if direction == "f":
                    checkpoint += 1
                else:
                    checkpoint -= 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 8:  # Thunder Plains
            if pathing.set_movement(ThunderPlainsFarm.execute(checkpoint)) is True:
                if direction == "f":
                    checkpoint += 1
                    if (
                        checkpoint in [5, 6]
                        and zone == "thunder_plains_(south)_(2_stones)"
                    ):
                        checkpoint = 14
                else:
                    checkpoint -= 1
                    if (
                        checkpoint in [13, 14]
                        and zone != "thunder_plains_(north)_(2_stones)"
                    ):
                        checkpoint = 5
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 9:  # Macalania
            if pathing.set_movement(MacFarm.execute(checkpoint)) is True:
                if direction == "f":
                    checkpoint += 1
                else:
                    checkpoint -= 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 10:  # Bikanel
            if pathing.set_movement(BikanelFarm.execute(checkpoint)) is True:
                if direction == "f":
                    checkpoint += 1
                else:
                    checkpoint -= 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 12:  # Calm Lands
            if pathing.set_movement(CalmFarm.execute(checkpoint)) is True:
                if direction == "f":
                    checkpoint += 1
                else:
                    checkpoint -= 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 13:  # Omega
            if zone == "omega_ruins_(sphere)":
                if checkpoint == 2 and direction == "f":
                    direction = "b"
                if checkpoint == 1 and direction == "b":
                    direction = "f"
            elif zone == "omega_ruins_(lower)":
                if checkpoint == 25 and direction == "f":
                    direction = "b"
                if checkpoint == 22 and direction == "b":
                    direction = "f"
            else:
                if checkpoint == 29 and direction == "f":
                    direction = "b"
                if checkpoint == 26 and direction == "b":
                    direction = "f"

            if pathing.set_movement(OmegaFarm.execute(checkpoint)) is True:
                if direction == "f":
                    checkpoint += 1
                else:
                    checkpoint -= 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 14:  # Gagazet
            if zone == "gagazet_(mountain)":
                if pathing.set_movement(GagazetMtPathFarm.execute(checkpoint)) is True:
                    if direction == "f":
                        checkpoint += 1
                    else:
                        checkpoint -= 1
                    logger.debug(f"Checkpoint {checkpoint}")
            elif zone == "gagazet_(cave)":
                if pathing.set_movement(GagazetCaveFarm.execute(checkpoint)) is True:
                    if direction == "f":
                        checkpoint += 1
                    else:
                        checkpoint -= 1
                    logger.debug(f"Checkpoint {checkpoint}")
            elif "_zone" in zone:
                if pathing.set_movement(YojimboFarm.execute(checkpoint)) is True:
                    if direction == "f":
                        checkpoint += 1
                    else:
                        checkpoint -= 1
                    logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 15:  # Zanarkand
            if pathing.set_movement(ZanarkandFarm2.execute(checkpoint)) is True:
                if direction == "f":
                    checkpoint += 1
                else:
                    checkpoint -= 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            logger.warning("Path not determined. (A)")
            return
    logger.warning(f"Arrived at battle area, checkpoint {checkpoint}")


def battle_start(zone: str):
    path_info = path_get_info(zone=zone)
    zone_num = get_zone_int(zone=zone)
    if zone_num == 13:
        memory.main.update_formation(Tidus, Wakka, Rikku)
    if zone == "omega_ruins_(upper)":
        checkpoint = 27
    else:
        checkpoint = path_info["first_battle"]
    direction = "f"
    last_map = get_map()
    while not memory.main.battle_active():
        # logger.debug(f"Checkpoint test: {checkpoint}")
        if get_map() != last_map:
            if direction == "f":
                checkpoint += 2
            else:
                checkpoint -= 2
            logger.debug(f"Checkpoint/map update {checkpoint}")
            last_map = get_map()
        if checkpoint == path_info["sphere"] and memory.main.get_tidus_mp() < 30:
            save_sphere.touch_and_go()
        elif zone_num == 0:
            if zone == "inside_sin_(front)":
                if get_map() == 204:
                    checkpoint = 44
                    direction = "b"
                elif checkpoint > 42:
                    checkpoint = 42
                    direction = "b"
                elif checkpoint < 40 and direction == 'b':
                    direction = "f"
            if zone == "inside_sin_(back)":
                if get_map() == 203 and direction == 'b':
                    direction = 'f'
                elif get_map() == 204 and checkpoint < 45:
                    checkpoint = 45
                    direction = 'f'
                elif checkpoint > 46:
                    checkpoint = 44

            if get_map() == 296:
                FFXC.set_neutral()
                logger.debug("We've reached the Seymour screen.")
                memory.main.update_formation(Tidus, Yuna, Lulu)
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                FFXC.set_neutral()
                battle.boss.omnis()
                memory.main.click_to_control()
                memory.main.update_formation(Tidus, Wakka, Rikku)
            elif pathing.set_movement(SinFarm.execute(checkpoint)) is True:
                if direction == "f":
                    if checkpoint == path_info["last_battle"]:
                        logger.debug("Looping back")
                        checkpoint -= 1
                        direction = "b"
                    else:
                        checkpoint += 1
                else:
                    if checkpoint == path_info["first_battle"]:
                        logger.debug("Looping forward")
                        checkpoint += 1
                        direction = "f"
                    else:
                        checkpoint -= 1
                logger.debug(f"Checkpoint (A) {checkpoint}")
        elif zone_num == 2:
            if pathing.set_movement(KilikaFarm.execute(checkpoint)) is True:
                if direction == "f":
                    if checkpoint == path_info["last_battle"]:
                        logger.debug("Looping back")
                        checkpoint -= 1
                        direction = "b"
                    else:
                        checkpoint += 1
                else:
                    if checkpoint == path_info["first_battle"]:
                        logger.debug("Looping forward")
                        checkpoint += 1
                        direction = "f"
                    else:
                        checkpoint -= 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 4:
            if pathing.set_movement(MiihenFarm.execute(checkpoint)) is True:
                if direction == "f":
                    if checkpoint == path_info["last_battle"]:
                        logger.debug("Looping back")
                        checkpoint -= 1
                        direction = "b"
                    else:
                        checkpoint += 1
                else:
                    if checkpoint == path_info["first_battle"]:
                        logger.debug("Looping forward")
                        checkpoint += 1
                        direction = "f"
                    else:
                        checkpoint -= 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 5:
            if pathing.set_movement(DjoseFarm.execute(checkpoint)) is True:
                if direction == "f":
                    if checkpoint == path_info["last_battle"]:
                        logger.debug("Looping back")
                        checkpoint -= 1
                        direction = "b"
                    else:
                        checkpoint += 1
                else:
                    if checkpoint == path_info["first_battle"]:
                        logger.debug("Looping forward")
                        checkpoint += 1
                        direction = "f"
                    else:
                        checkpoint -= 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 8:
            # Dodge logic
            if memory.main.dodge_lightning(game_vars.get_l_strike()):
                logger.debug("Strike!")
                game_vars.set_l_strike(memory.main.l_strike_count())
            # Regular stuff
            if pathing.set_movement(ThunderPlainsFarm.execute(checkpoint)) is True:
                if direction == "f":
                    if checkpoint == path_info["last_battle"]:
                        logger.debug("Looping back")
                        checkpoint -= 1
                        direction = "b"
                    else:
                        checkpoint += 1
                else:
                    if checkpoint == path_info["first_battle"]:
                        logger.debug("Looping forward")
                        checkpoint += 1
                        direction = "f"
                    else:
                        checkpoint -= 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 9:
            if pathing.set_movement(MacFarm.execute(checkpoint)) is True:
                if direction == "f":
                    if checkpoint == path_info["last_battle"]:
                        logger.debug("Looping back")
                        checkpoint -= 1
                        direction = "b"
                    else:
                        checkpoint += 1
                else:
                    if checkpoint == path_info["first_battle"]:
                        logger.debug("Looping forward")
                        checkpoint += 1
                        direction = "f"
                    else:
                        checkpoint -= 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 10:
            if pathing.set_movement(BikanelFarm.execute(checkpoint)) is True:
                if direction == "f":
                    if checkpoint == path_info["last_battle"]:
                        logger.debug("Looping back")
                        checkpoint -= 1
                        direction = "b"
                    else:
                        checkpoint += 1
                else:
                    if checkpoint == path_info["first_battle"]:
                        logger.debug("Looping forward")
                        checkpoint += 1
                        direction = "f"
                    else:
                        checkpoint -= 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 12:
            if pathing.set_movement(CalmFarm.execute(checkpoint)) is True:
                if direction == "f":
                    if checkpoint == path_info["last_battle"]:
                        logger.debug("Looping back")
                        checkpoint -= 1
                        direction = "b"
                    else:
                        checkpoint += 1
                else:
                    if checkpoint == path_info["first_battle"]:
                        logger.debug("Looping forward")
                        checkpoint += 1
                        direction = "f"
                    else:
                        checkpoint -= 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 13:
            if pathing.set_movement(OmegaFarm.execute(checkpoint)) is True:
                if direction == "f":
                    if checkpoint >= path_info["last_battle"]:
                        logger.debug("Looping back")
                        checkpoint -= 1
                        direction = "b"
                    else:
                        checkpoint += 1
                else:
                    if checkpoint <= path_info["first_battle"]-2:
                        logger.debug("Looping forward")
                        checkpoint += 1
                        direction = "f"
                    else:
                        checkpoint -= 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 15:
            if pathing.set_movement(ZanarkandFarm2.execute(checkpoint)) is True:
                if direction == "f":
                    if checkpoint == path_info["last_battle"]:
                        logger.debug("Looping back")
                        checkpoint -= 1
                        direction = "b"
                    else:
                        checkpoint += 1
                else:
                    if checkpoint == path_info["first_battle"]:
                        logger.debug("Looping forward")
                        checkpoint += 1
                        direction = "f"
                    else:
                        checkpoint -= 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 14:
            if zone == "gagazet_(mountain)":
                if pathing.set_movement(GagazetMtPathFarm.execute(checkpoint)) is True:
                    if direction == "f":
                        if checkpoint == path_info["last_battle"]:
                            logger.debug("Looping back")
                            checkpoint -= 1
                            direction = "b"
                        else:
                            checkpoint += 1
                    else:
                        if checkpoint == path_info["first_battle"]:
                            logger.debug("Looping forward")
                            checkpoint += 1
                            direction = "f"
                        else:
                            checkpoint -= 1
                    logger.debug(f"Checkpoint {checkpoint}")
            elif zone == "gagazet_(cave)":
                if pathing.set_movement(GagazetCaveFarm.execute(checkpoint)) is True:
                    if direction == "f":
                        if checkpoint == path_info["last_battle"]:
                            logger.debug("Looping back")
                            checkpoint -= 1
                            direction = "b"
                        else:
                            checkpoint += 1
                    else:
                        if checkpoint == path_info["first_battle"]:
                            logger.debug("Looping forward")
                            checkpoint += 1
                            direction = "f"
                        else:
                            checkpoint -= 1
                    logger.debug(f"Checkpoint {checkpoint}")
            elif "_zone" in zone:
                if pathing.set_movement(YojimboFarm.execute(checkpoint)) is True:
                    if direction == "f":
                        if checkpoint == path_info["last_battle"]:
                            logger.debug("Looping back")
                            checkpoint -= 1
                            direction = "b"
                        else:
                            checkpoint += 1
                    else:
                        if checkpoint == path_info["first_battle"]:
                            logger.debug("Looping forward")
                            checkpoint += 1
                            direction = "f"
                        else:
                            checkpoint -= 1
                    logger.debug(f"Checkpoint {checkpoint}")
    logger.debug(f"== Battle start: {memory.main.get_encounter_id()}")
    results = False
    if get_map() in [203, 204, 258, 271]:
        results = advanced_battle_logic()
    elif zone == "any":
        results = battle_farm_defer()
    else:
        results = battle_farm_all()
    if results:
        battle.main.wrap_up()
    else:
        menu.remove_all_nea()


def path_to_yojimbo():
    checkpoint = 30
    last_map = get_map()
    # menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)

    while checkpoint != 62:
        if memory.main.user_control():
            if get_map() != last_map:
                checkpoint += 2
                logger.debug(f"Checkpoint/map update {checkpoint}")
                last_map = get_map()
            elif checkpoint == 48 and (
                game_vars.yojimbo_unlocked() or
                memory.main.get_gil_value() < 550000
            ):
                return_to_airship()
                return
            elif checkpoint == 52:  # First teleporter
                logger.debug("Teleporter to Fayth room")
                FFXC.set_neutral()
                memory.main.wait_frames(9)
                FFXC.set_movement(0, 1)
                memory.main.wait_frames(2)
                FFXC.set_neutral()
                memory.main.wait_frames(6)
                xbox.tap_b()
                yojimbo_dialog()
                checkpoint = 54
                # else:
                #     checkpoint = 56
                memory.main.click_to_control()
            elif checkpoint == 55:  # Second teleporter
                logger.debug("Teleporter to entrance")
                FFXC.set_neutral()
                memory.main.wait_frames(9)
                FFXC.set_movement(0, -1)
                memory.main.wait_frames(2)
                FFXC.set_neutral()
                xbox.tap_b()
                xbox.tap_b()
                xbox.tap_b()
                checkpoint += 1
            elif pathing.set_movement(YojimboFarm.execute(checkpoint)) is True:
                checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            FFXC.set_neutral()
            if memory.main.battle_active() and memory.main.turn_ready():
                battle.main.attack()
            if memory.main.diag_skip_possible() or memory.main.menu_open():
                xbox.tap_b()
    return_to_airship()


def path_to_save(zone: str) -> bool:
    path_info = path_get_info(zone=zone)
    logger.manip(f"Returning to save sphere. Current zone: {zone}")
    if not memory.main.equipped_armor_has_ability(char_num=game_vars.ne_armor()):
        menu.equip_armor(character=game_vars.ne_armor(), ability=0x801D)
    logger.manip(path_info)
    zone_num = get_zone_int(zone=zone)
    last_map = get_map()
    direction = path_info["return_direction"]

    checkpoint = path_info["return_start"]
    while checkpoint != path_info["sphere"]:
        if get_map() != last_map:
            if path_info["return_direction"] == "b":
                checkpoint -= 2
            else:
                checkpoint += 2
            logger.debug(f"Checkpoint/map update {checkpoint}")
            last_map = get_map()
        elif zone_num == 0:  # Sin
            if get_map() == 204:
                checkpoint = 44
                direction = "b"
            elif get_map() == 203 and checkpoint > 42:
                checkpoint = 41
                direction = 'f'
            elif checkpoint < 41:
                direction = 'f'

            if pathing.set_movement(SinFarm.execute(checkpoint)) is True:
                if direction == "b":
                    checkpoint -= 1
                else:
                    checkpoint += 1
                logger.debug(f"Checkpoint (B) {checkpoint}")
        elif zone_num == 2:
            if pathing.set_movement(KilikaFarm.execute(checkpoint)) is True:
                if direction == "b":
                    checkpoint -= 1
                else:
                    checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 4:
            if checkpoint == 199:
                checkpoint = 5
            elif pathing.set_movement(MiihenFarm.execute(checkpoint)) is True:
                if path_info["return_direction"] == "b":
                    checkpoint -= 1
                else:
                    checkpoint += 1
                    if checkpoint in [33, 34, 35, 36]:
                        checkpoint = 47
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 5:
            if pathing.set_movement(DjoseFarm.execute(checkpoint)) is True:
                if path_info["return_direction"] == "b":
                    checkpoint -= 1
                else:
                    checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 8:
            if checkpoint in [13, 14] and path_info["return_direction"] == "b":
                checkpoint = 5
            if pathing.set_movement(ThunderPlainsFarm.execute(checkpoint)) is True:
                if path_info["return_direction"] == "b":
                    checkpoint -= 1
                else:
                    checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 9:
            if pathing.set_movement(MacFarm.execute(checkpoint)) is True:
                if path_info["return_direction"] == "b":
                    checkpoint -= 1
                else:
                    checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 10:  # Bikanel
            if pathing.set_movement(BikanelFarm.execute(checkpoint)) is True:
                if path_info["return_direction"] == "b":
                    checkpoint -= 1
                else:
                    checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 12:  # Calm Lands
            if pathing.set_movement(CalmFarm.execute(checkpoint)) is True:
                if path_info["return_direction"] == "b":
                    checkpoint -= 1
                else:
                    checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 13:  # Omega
            if pathing.set_movement(OmegaFarm.execute(checkpoint)) is True:
                if path_info["return_direction"] == "b":
                    checkpoint -= 1
                else:
                    checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        elif zone_num == 14:  # Gagazet/Yojimbo
            if zone == "gagazet_(mountain)":
                if pathing.set_movement(GagazetMtPathFarm.execute(checkpoint)) is True:
                    if path_info["return_direction"] == "b":
                        checkpoint -= 1
                    else:
                        checkpoint += 1
                    logger.debug(f"Checkpoint {checkpoint}")
            elif zone == "gagazet_(cave)":
                if pathing.set_movement(GagazetCaveFarm.execute(checkpoint)) is True:
                    if path_info["return_direction"] == "b":
                        checkpoint -= 1
                    else:
                        checkpoint += 1
                    logger.debug(f"Checkpoint {checkpoint}")
            elif "_zone" in zone:
                if checkpoint == 48:
                    logger.debug("Returning, we shouldn't even be here. (Yojimbo path)")
                    FFXC.set_neutral()
                    return
                if pathing.set_movement(YojimboFarm.execute(checkpoint)) is True:
                    if path_info["return_direction"] == "b":
                        checkpoint -= 1
                    else:
                        checkpoint += 1
                    logger.debug(f"Checkpoint {checkpoint}")

        elif zone_num == 15:  # Zanarkand
            if pathing.set_movement(ZanarkandFarm2.execute(checkpoint)) is True:
                if path_info["return_direction"] == "b":
                    checkpoint -= 1
                else:
                    checkpoint += 1
                logger.debug(f"Checkpoint {checkpoint}")
        else:
            logger.warning("Path not determined. (B)")
            return
    if not memory.main.user_control():
        memory.main.await_control()