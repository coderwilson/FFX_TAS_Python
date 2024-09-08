import csv
import json
import logging
import os

import logs
import memory.main
import vars
from tracker.ffx_rng_tracker.data.monsters import MONSTERS

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()


def current_battle_formation() -> []:
    battle_num = str(memory.main.get_encounter_id())
    f = open("json_ai_files/battle_id_to_formation.json")
    all_formations = json.load(f)
    f.close()
    if not battle_num in all_formations.keys():
        return []
    else:
        return all_formations[battle_num]

def luck_check(fiend_name:str):
    library_check = MONSTERS[fiend_name].stats["luck"]
    logger.debug("== Dict Check: {library_check}")
    logger.debug("== Dict Check: {library_check}")
    logger.debug("== Dict Check: {library_check}")
    logger.debug("== Dict Check: {library_check}")
    if fiend_name in ["arm","cid","circle","crane","dummy","gate_lock","gate_lock_2","gemini"]:
        return 0
    if fiend_name in ["geneauxs_tentacle","head","kimahri_weapon","mortiphasm","mortiphasm_3"]:
        return 0
    if fiend_name in ["mortiphasm_4","mortiphasm_5","negator","nemesis","oblitzerator"]:
        return 0
    if fiend_name.find("possessed") != -1:
        return 0
    if fiend_name.find("sinscale") != -1:
        return 0
    if fiend_name in ["pupu","sahagin_4","sahagin_chief"]:
        return 0
    if fiend_name in ["sinspawn_ammes","tentacle","vouivre_2","yu_yevon"]:
        return 10
    if fiend_name in ["stratoavis"]:
        return 18
    if fiend_name in ["anima","lord_ochu","mortibody","mortiphasm_2","neslug","ornitholestes"]:
        return 20
    if fiend_name in ["seymour_omnis","yunalesca"]:
        return 20
    if fiend_name in ["kottos"]:
        return 25
    if fiend_name in ["fenrir"]:
        return 30
    if fiend_name in ["hornet"]:
        return 30
    return 15


def force_drop(drop_chance:int = 255):
    values = memory.main.rng_array_from_index(index=10, array_len=100)
    if drop_chance <= 0:
        return
    if values[1] & 0x7FFFFFFF % 255 >= drop_chance:
        memory.main.advance_rng_index(index=10)
        force_drop(drop_chance=drop_chance)
    

def force_equip(equip_type:int = 0, character:int = 0, aeon_kill:bool=True, party_size:int = 7):
    get_item, _ = item_to_be_dropped(
        enemy = "yunalesca",
        party_size=party_size,
    )
    
    logger.debug("==== Equip check ====")
    logger.debug(f"Raw: {get_item}")
    logger.debug(f"Char kill: {get_item.owner()}")
    logger.debug(f"Aeon kill: {get_item.owner_alt()}")
    logger.debug(f"Type (0 for weap): {get_item.equipment_type()}")
    logger.debug(f"Abilities: {get_item.abilities()}")
    logger.debug("=====================")
    
    
    if (
        (aeon_kill and get_item.owner_alt() != character) or
        (not aeon_kill and get_item.owner() != character) or
        (equip_type != get_item.equipment_type())
    ):
        memory.main.advance_rng_index(index=12)
        force_equip(
            equip_type=equip_type,
            character=character,
            aeon_kill=aeon_kill,
            party_size=party_size
        )


def force_preempt():
    values = memory.main.rng_array_from_index(index=1, array_len=100)
    if (values[2] & 0x7FFFFFFF) & 255 >= 32:
        memory.main.advance_rng_index(index=1)
        force_preempt()


def area_formations(area: str):
    f = open("tracker/data/formations.json")
    all_formations = json.load(f)
    f.close()
    if area in all_formations["random"].keys():
        return all_formations["random"][area]["formations"]
    elif area in all_formations["bosses"].keys():
        return all_formations["bosses"][area]["formation"]
    else:
        logger.debug(f"Key not found: {area}")


def coming_battles(
    area: str = "kilika_woods", battle_count: int = 10, extra_advances: int = 0
):
    formations = area_formations(area=area)
    advances = memory.main.rng_01_advances((battle_count * 2) + extra_advances)
    if extra_advances != 0:
        while extra_advances != 0:
            del advances[0]
            extra_advances -= 1
    battles = []
    for i in range(battle_count):
        next_value = formations[(advances[(i * 2) + 1] & 0x7FFFFFFF) % len(formations)]
        battles.append(next_value)
    return battles


def coming_battle_type(extra_advances: int = 0, initiative=False):
    advances = memory.main.rng_01_advances(2 + extra_advances)
    if extra_advances != 0:
        while extra_advances != 0:
            del advances[0]
            extra_advances -= 1
    battle_type = (advances[2] & 0x7FFFFFFF) & 255
    if initiative:
        battle_type -= 33

    if battle_type < 32:
        return 1
    elif battle_type < 255 - 32:
        return 0
    else:
        return 2


def singles_battles(
    area: str = "kilika_woods", battle_count: int = 10, extra_advances: int = 0
):
    # logger.debug(f"Area: {area}")
    formations = area_formations(area=area)
    advances = memory.main.rng_01_advances(battle_count + extra_advances)
    if extra_advances != 0:
        while extra_advances != 0:
            del advances[0]
            extra_advances -= 1
    battles = []
    for i in range(battle_count):
        next_value = formations[(advances[i + 1] & 0x7FFFFFFF) % len(formations)]
        battles.append(next_value)
    # logger.debug(f"Battles: {battles}")
    return battles


def drop_chance(enemy: str = "ghost"):
    return MONSTERS[enemy].equipment["drop_chance"]


def drop_rare(drop_num:int = 1):
    return memory.main.next_steal_rare(drop_num - 1)
    

def drop_slots(enemy: str = "ghost"):
    return MONSTERS[enemy].equipment["slots_range"]


def slot_modifier(enemy: str = "ghost"):
    return MONSTERS[enemy].equipment["slots_modifier"]


def drop_ability_count(enemy: str = "ghost"):
    return MONSTERS[enemy].equipment["max_ability_rolls_range"]


def ability_modifier(enemy: str = "ghost"):
    return MONSTERS[enemy].equipment["max_ability_rolls_modifier"]


def drop_ability_list(enemy: str = "ghost", equip_type: int = 0):
    if equip_type == 0:
        array = MONSTERS[enemy].equipment["ability_arrays"]["Tidus"]["Weapon"]
    else:
        array = MONSTERS[enemy].equipment["ability_arrays"]["Tidus"]["Armor"]
    ret_val = []
    for i in range(len(array)):
        try:
            ret_val.append(array[i].tas_id)
        except Exception:
            ret_val.append(255)

    return ret_val


def early_battle_count():
    with open("csv\\seed_battle_variance.csv", "r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if int(row["Seed"]) == memory.main.rng_seed():
                return row


def track_drops(enemy: str = "ghost", battles: int = 20, extra_advances: int = 0):
    no_advance_array = []
    one_advance_array = []
    two_advance_array = []
    advances = (battles + 1) * 3
    rand_array = memory.main.rng_10_array(array_len=advances + extra_advances)
    if extra_advances != 0:
        while extra_advances != 0:
            del rand_array[0]
            extra_advances -= 1

    for i in range(len(rand_array)):
        if i < 3:
            pass
        elif (rand_array[i] & 0x7FFFFFFF) % 255 < drop_chance(enemy):
            if i % 3 == 0:
                no_advance_array.append(i / 3)
            elif i % 3 == 1:
                one_advance_array.append((i - 1) / 3)
            else:
                two_advance_array.append((i - 2) / 3)
    return [no_advance_array, one_advance_array, two_advance_array]


def item_to_be_dropped(
    enemy: str = "ghost",
    pre_advance_12: int = 0,
    pre_advance_13: int = 0,
    party_size: int = 7,
):
    test_mode = False # Doesn't functionally change, but prints more stuff.
    slot_mod = slot_modifier(enemy=enemy)
    ability_mod = ability_modifier(enemy=enemy)

    if party_size == 2:
        party_chars = [0, 4]
    elif party_size == 3:  # Oblitzerator
        party_chars = [0, 3, 5]
    elif party_size == 4:
        party_chars = [0, 1, 4, 5]
    elif party_size == 5:
        party_chars = [0, 1, 3, 4, 5]
    elif party_size == 6:
        party_chars = [0, 1, 2, 3, 4, 5]
    elif party_size == 7:
        party_chars = [0, 1, 2, 3, 4, 5, 6]
    else:
        party_chars = [0]

    advance_12 = 4 + pre_advance_12
    test_array_12 = memory.main.rng_12_array(advance_12)
    del test_array_12[0]
    if pre_advance_12 >= 1:
        while pre_advance_12 >= 1:
            del test_array_12[0]
            pre_advance_12 -= 1

    # Assume killer is aeon
    user_2 = party_chars[(test_array_12[0] & 0x7FFFFFFF) % len(party_chars)]
    party_chars.append(9)
    party_chars.append(9)
    party_chars.append(9)
    # Assume user == killer
    user_1 = party_chars[(test_array_12[0] & 0x7FFFFFFF) % len(party_chars)]

    # Type
    equip_type = (test_array_12[1] & 0x7FFFFFFF) % 2

    # Slots
    base_slots = (slot_mod + ((test_array_12[2] & 0x7FFFFFFF) & 7)) - 4
    slots = (base_slots + ((base_slots >> 31) & 7)) >> 2
    if slots == 0:
        slots = 1

    # Abilities
    base_mod = (ability_mod + ((test_array_12[3] & 0x7FFFFFFF) & 7)) - 4
    ability_count = (base_mod + ((base_mod >> 31) & 7)) >> 3
    if slots < ability_count:
        ability_count = slots

    # rng13 logic here, determine which ability goes where.
    new_abilities = ability_to_be_dropped(
        enemy=enemy, equip_type=equip_type, slots=ability_count, advances=pre_advance_13
    )
    ability_list = new_abilities[0]
    pre_advance_13 += new_abilities[1]
    if test_mode:
        logger.debug(f"New Abilities: {ability_list}")
        logger.debug(f"OWNER CHECK 1: {user_1}")
        logger.debug(f"OWNER CHECK 2: {user_2}")

    final_item = memory.main.Equipment(equip_num=0)
    final_item.create_custom(
        e_type=equip_type,
        e_owner_1=user_1,
        e_owner_2=user_2,
        e_slots=slots,
        e_abilities=ability_list,
    )

    return final_item, pre_advance_13


def ability_to_be_dropped(
    enemy: str = "ghost", equip_type: int = 0, slots: int = 1, advances: int = 0
):
    test_mode = False  # Doesn't functionally change, but prints more stuff.
    outcomes = drop_ability_list(enemy=enemy, equip_type=equip_type)
    found = 0
    # if test_mode:
    #    logger.debug(f"outcomes: {outcomes}")
    if slots == 0:
        slots = 1
    filled_slots = [99] * slots
    # if test_mode:
    #    logger.debug(f"fs: {filled_slots}")

    ptr = 0  # Pointer that indicates how many advances needed for this evaluation
    test_array = memory.main.rng_13_array(array_len=50 + advances)
    # if test_mode:
    #    logger.debug(f"ta: {test_array}")

    # if outcomes[0]:
    #    filled_slots.append(outcomes[0])
    #    filled_slots.remove(99)
    if test_mode:
        logger.debug(f"Enemy: {enemy} - Outcomes: {outcomes}")

    while 99 in filled_slots and ptr < 50 + advances:
        # Increment to match the first (and subsequent) advance(s)
        try:
            ptr += 1
            if test_mode:
                logger.debug(f"ptr: {ptr}")
                logger.debug(f"Try: {test_array[ptr + advances]}")
            array_pos = ((test_array[ptr + advances] & 0x7FFFFFFF) % 7) + 1
            if test_mode:
                logger.debug(f"AP: {array_pos}")
                logger.debug(f"Res: {outcomes[array_pos]}")
            if outcomes[array_pos] in filled_slots:
                pass
            else:
                filled_slots.remove(99)
                filled_slots.append(int(outcomes[array_pos]))
                found += 1
                if test_mode:
                    logger.debug(filled_slots)
        except Exception as e:
            logger.exception(e)
    if test_mode:
        logger.debug(f"Filled Slots: {filled_slots}")

    while 99 in filled_slots:
        filled_slots.remove(99)

    # Format so that we have four slots always.
    if len(filled_slots) < 4:
        while len(filled_slots) < 4:
            filled_slots.append(255)
    if test_mode:
        logger.debug(f"Filled Slots fin: {filled_slots}")

    return [filled_slots, found]


def report_dropped_item(
    enemy: str,
    drop=memory.main.Equipment,
    pref_type: int = 99,
    pref_ability: int = 255,
    need_adv: int = 0,
    report=False,
):
    abi_str = str(pref_ability)
    pref_type
    report = True
    if pref_ability != 255 and abi_str not in drop.equip_abilities:
        report = False
    elif pref_type != 99 and pref_type != drop.equip_type:
        logger.debug(pref_type)
        logger.debug(drop.equip_type)
        report = False

    if report:
        logs.write_rng_track(
            "+Item drop off of:" + str(enemy) + "| advances:" + str(need_adv)
        )
        logs.write_rng_track(
            "+Owner, char-killed (9 = killer):" + str(drop.equip_owner)
        )
        logs.write_rng_track("+Owner, aeon-killed:" + str(drop.equip_owner_alt))
        if drop.equip_type == 0:
            logs.write_rng_track("+Type: Weapon")
        else:
            logs.write_rng_track("+Type: Armor")
        logs.write_rng_track("+Open Slots: " + str(drop.slots))
        logs.write_rng_track("+Abilities: " + str(drop.equip_abilities))
        logs.write_rng_track("===================")
        return True
    else:
        logs.write_rng_track(
            "-Undesirable item dropped by: "
            + str(enemy)
            + " | advances:"
            + str(need_adv)
        )
        logs.write_rng_track("-Owner, char-killed: " + str(drop.equip_owner))
        logs.write_rng_track("-Owner, aeon-killed: " + str(drop.equip_owner_alt))
        if drop.equip_type == 0:
            logs.write_rng_track("-Type: Weapon")
        else:
            logs.write_rng_track("-Type: Armor")
        logs.write_rng_track("-Open Slots: " + str(drop.slots))
        logs.write_rng_track("-Abilities: " + str(drop.equip_abilities))
        logs.write_rng_track("===================")
        return False


def t_strike_tracking(tros=False, report=False):
    return [0, 0, 0], [0, 0, 0]


def t_strike_tracking_not_working_yet(tros=False, report=False):
    if tros:
        advance_01 = 0
        advance_10 = 3  # Starts off with just the Tros kill advance.
    else:
        advance_01 = 1
        advance_10 = 9  # Starts off with two advances for pirhanas and one for Tros
    if report:
        logs.open_rng_track()
        logs.write_rng_track(memory.main.rng_10_array(array_len=80))
        logs.write_rng_track("#########################")
    advance_12 = [0, 0, 0]  # Tros drops one item
    advance_13 = [0, 0, 0]  # Tros item has no abilities
    thunder_count = [0, 0, 0]  # Count results per advance, for returning later.
    # Count only if Oblitz will drop a weapon for Tidus.
    oblitz_weap = [False] * 3
    # Increment only if we need to kill yellow element on a certain battle.
    kill_yellow = [0, 0, 0]
    battle_variance = early_battle_count()
    try:
        lagoon_count = int(battle_variance["Lagoon"])
        kilika_count = int(battle_variance["Kilika"])
    except Exception:
        lagoon_count = 3
        kilika_count = 6
    party_size = 4

    # Lagoon
    lagoon_battles = coming_battles(
        area="besaid_lagoon", battle_count=lagoon_count, extra_advances=advance_01
    )
    for i in range(len(lagoon_battles)):
        logs.write_rng_track("Lagoon battle:")
        logs.write_rng_track(str(lagoon_battles[i]))
        logs.write_rng_track(
            "Battle type: "
            + str(coming_battle_type(extra_advances=advance_01 + (2 * i)))
        )
        if len(lagoon_battles[i]) == 2:
            advance_10 += 6
        elif (
            len(lagoon_battles[i]) == 3
            and coming_battle_type(extra_advances=advance_01 + (2 * i)) == 1
        ):
            advance_10 += 9
        else:
            advance_10 += 0
    advance_01 += len(lagoon_battles) * 2

    logs.write_rng_track("===================")
    logs.write_rng_track("Looking ahead for thunder strike drops")

    # Besaid tutorials
    drop_chances = track_drops(enemy="dingo", battles=1, extra_advances=advance_10)
    if len(drop_chances[0]) >= 1:
        final_item, advance_13[0] = item_to_be_dropped(
            enemy="dingo",
            pre_advance_12=advance_12[0],
            pre_advance_13=advance_13[0],
            party_size=party_size,
        )
        advance_12[0] += 4
        if report_dropped_item(
            enemy="dingo",
            drop=final_item,
            pref_type=0,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[0] += 1
    if len(drop_chances[1]) >= 1:
        final_item, advance_13[1] = item_to_be_dropped(
            enemy="dingo",
            pre_advance_12=advance_12[1],
            pre_advance_13=advance_13[1],
            party_size=party_size,
        )
        advance_12[1] += 4
        if report_dropped_item(
            enemy="dingo",
            drop=final_item,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[1] += 1
    if len(drop_chances[2]) >= 1:
        final_item, advance_13[2] = item_to_be_dropped(
            enemy="dingo",
            pre_advance_12=advance_12[2],
            pre_advance_13=advance_13[2],
            party_size=party_size,
        )
        advance_12[2] += 4
        if report_dropped_item(
            enemy="dingo",
            drop=final_item,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[2] += 1
    advance_10 += 3

    drop_chances = track_drops(enemy="condor", battles=1, extra_advances=advance_10)
    if len(drop_chances[0]) >= 1:
        final_item, advance_13[0] = item_to_be_dropped(
            enemy="condor",
            pre_advance_12=advance_12[0],
            pre_advance_13=advance_13[0],
            party_size=party_size,
        )
        advance_12[0] += 4
        if report_dropped_item(
            enemy="condor",
            drop=final_item,
            pref_type=0,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[0] += 1
    if len(drop_chances[1]) >= 1:
        final_item, advance_13[1] = item_to_be_dropped(
            enemy="condor",
            pre_advance_12=advance_12[1],
            pre_advance_13=advance_13[1],
            party_size=party_size,
        )
        advance_12[1] += 4
        if report_dropped_item(
            enemy="condor",
            drop=final_item,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[1] += 1
    if len(drop_chances[1]) >= 1:
        final_item, advance_13[2] = item_to_be_dropped(
            enemy="condor",
            pre_advance_12=advance_12[2],
            pre_advance_13=advance_13[2],
            party_size=party_size,
        )
        advance_12[2] += 4
        if report_dropped_item(
            enemy="condor",
            drop=final_item,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[2] += 1
    advance_10 += 3

    drop_chances = track_drops(enemy="water_flan", battles=1, extra_advances=advance_10)
    if len(drop_chances[0]) >= 1:
        final_item, advance_13[0] = item_to_be_dropped(
            enemy="water_flan",
            pre_advance_12=advance_12[0],
            pre_advance_13=advance_13[0],
            party_size=party_size,
        )
        report_dropped_item(
            enemy="water_flan",
            drop=final_item,
            pref_type=0,
            pref_ability=0x8026,
            report=report,
        )
        advance_12[0] += 4
    if len(drop_chances[1]) >= 1:
        final_item, advance_13[1] = item_to_be_dropped(
            enemy="water_flan",
            pre_advance_12=advance_12[1],
            pre_advance_13=advance_13[1],
            party_size=party_size,
        )
        report_dropped_item(
            enemy="water_flan",
            drop=final_item,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        )
        advance_12[1] += 4
    if len(drop_chances[2]) >= 1:
        final_item, advance_13[2] = item_to_be_dropped(
            enemy="water_flan",
            pre_advance_12=advance_12[2],
            pre_advance_13=advance_13[2],
            party_size=party_size,
        )
        report_dropped_item(
            enemy="water_flan",
            drop=final_item,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        )
        advance_12[2] += 4
    advance_10 += 3

    # Kimahri drops something guaranteed.
    drop_chances = track_drops(enemy="???", battles=1, extra_advances=advance_10)
    if len(drop_chances[0]) >= 1:
        final_item, advance_13[0] = item_to_be_dropped(
            enemy="???",
            pre_advance_12=advance_12[0],
            pre_advance_13=advance_13[0],
            party_size=party_size,
        )
        report_dropped_item(
            enemy="???",
            drop=final_item,
            pref_type=0,
            pref_ability=0x8026,
            report=report,
        )
        advance_12[0] += 4
    if len(drop_chances[1]) >= 1:
        final_item, advance_13[1] = item_to_be_dropped(
            enemy="???",
            pre_advance_12=advance_12[1],
            pre_advance_13=advance_13[1],
            party_size=party_size,
        )
        report_dropped_item(
            enemy="???",
            drop=final_item,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        )
        advance_12[1] += 4
    if len(drop_chances[2]) >= 1:
        final_item, advance_13[2] = item_to_be_dropped(
            enemy="???",
            pre_advance_12=advance_12[2],
            pre_advance_13=advance_13[2],
            party_size=party_size,
        )
        report_dropped_item(
            enemy="???",
            drop=final_item,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        )
        advance_12[2] += 4
    advance_10 += 3

    drop_chances = track_drops(enemy="garuda_3", battles=1, extra_advances=advance_10)
    if len(drop_chances[0]) >= 1:
        final_item, advance_13[0] = item_to_be_dropped(
            enemy="garuda_3",
            pre_advance_12=advance_12[0],
            pre_advance_13=advance_13[0],
            party_size=party_size,
        )
        advance_12[0] += 4
        if report_dropped_item(
            enemy="garuda_3",
            drop=final_item,
            pref_type=0,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[0] += 1
    if len(drop_chances[1]) >= 1:
        final_item, advance_13[1] = item_to_be_dropped(
            enemy="garuda_3",
            pre_advance_12=advance_12[1],
            pre_advance_13=advance_13[1],
            party_size=party_size,
        )
        advance_12[1] += 4
        if report_dropped_item(
            enemy="garuda_3",
            drop=final_item,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[1] += 1
    if len(drop_chances[2]) >= 1:
        final_item, advance_13[2] = item_to_be_dropped(
            enemy="garuda_3",
            pre_advance_12=advance_12[2],
            pre_advance_13=advance_13[2],
            party_size=party_size,
        )
        advance_12[2] += 4
        if report_dropped_item(
            enemy="garuda_3",
            drop=final_item,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[2] += 1
    advance_10 += 3

    drop_chances = track_drops(enemy="dingo", battles=1, extra_advances=advance_10)
    if len(drop_chances[0]) >= 1:
        final_item, advance_13[0] = item_to_be_dropped(
            enemy="dingo",
            pre_advance_12=advance_12[0],
            pre_advance_13=advance_13[0],
            party_size=party_size,
        )
        advance_12[0] += 4
        if report_dropped_item(
            enemy="dingo",
            drop=final_item,
            pref_type=0,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[0] += 1
    if len(drop_chances[1]) >= 1:
        final_item, advance_13[1] = item_to_be_dropped(
            enemy="dingo",
            pre_advance_12=advance_12[1],
            pre_advance_13=advance_13[1],
            party_size=party_size,
        )
        advance_12[1] += 4
        if report_dropped_item(
            enemy="dingo",
            drop=final_item,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[1] += 1
    if len(drop_chances[2]) >= 1:
        final_item, advance_13[2] = item_to_be_dropped(
            enemy="dingo",
            pre_advance_12=advance_12[2],
            pre_advance_13=advance_13[2],
            party_size=party_size,
        )
        advance_12[2] += 4
        if report_dropped_item(
            enemy="dingo",
            drop=final_item,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[2] += 1
    advance_10 += 3

    drop_chances = track_drops(enemy="condor", battles=1, extra_advances=advance_10)
    if len(drop_chances[0]) >= 1:
        final_item, advance_13[0] = item_to_be_dropped(
            enemy="condor",
            pre_advance_12=advance_12[0],
            pre_advance_13=advance_13[0],
            party_size=party_size,
        )
        advance_12[0] += 4
        if report_dropped_item(
            enemy="condor",
            drop=final_item,
            pref_type=0,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[0] += 1
    if len(drop_chances[1]) >= 1:
        final_item, advance_13[1] = item_to_be_dropped(
            enemy="condor",
            pre_advance_12=advance_12[1],
            pre_advance_13=advance_13[1],
            party_size=party_size,
        )
        advance_12[1] += 4
        if report_dropped_item(
            enemy="condor",
            drop=final_item,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[1] += 1
    if len(drop_chances[1]) >= 1:
        final_item, advance_13[2] = item_to_be_dropped(
            enemy="condor",
            pre_advance_12=advance_12[2],
            pre_advance_13=advance_13[2],
            party_size=party_size,
        )
        advance_12[2] += 4
        if report_dropped_item(
            enemy="condor",
            drop=final_item,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[2] += 1
    advance_10 += 3

    drop_chances = track_drops(enemy="water_flan", battles=1, extra_advances=advance_10)
    if len(drop_chances[0]) >= 1:
        final_item, advance_13[0] = item_to_be_dropped(
            enemy="water_flan",
            pre_advance_12=advance_12[0],
            pre_advance_13=advance_13[0],
            party_size=party_size,
        )
        report_dropped_item(
            enemy="water_flan",
            drop=final_item,
            pref_type=0,
            pref_ability=0x8026,
            report=report,
        )
        advance_12[0] += 4
    if len(drop_chances[1]) >= 1:
        final_item, advance_13[1] = item_to_be_dropped(
            enemy="water_flan",
            pre_advance_12=advance_12[1],
            pre_advance_13=advance_13[1],
            party_size=party_size,
        )
        report_dropped_item(
            enemy="water_flan",
            drop=final_item,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        )
        advance_12[1] += 4
    if len(drop_chances[2]) >= 1:
        final_item, advance_13[2] = item_to_be_dropped(
            enemy="water_flan",
            pre_advance_12=advance_12[2],
            pre_advance_13=advance_13[2],
            party_size=party_size,
        )
        report_dropped_item(
            enemy="water_flan",
            drop=final_item,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        )
        advance_12[2] += 4
    advance_10 += 3
    advance_01 += 6

    party_size = 5
    # Sin's Fin
    drop_chances = track_drops(enemy="sin", battles=1, extra_advances=advance_10)
    if len(drop_chances[0]) >= 1:
        final_item, advance_13[0] = item_to_be_dropped(
            enemy="sin",
            pre_advance_12=advance_12[0],
            pre_advance_13=advance_13[0],
            party_size=party_size,
        )
        advance_12[0] += 4
        if report_dropped_item(
            enemy="sin-fin",
            drop=final_item,
            pref_type=0,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[0] += 1
    if len(drop_chances[1]) >= 1:
        final_item, advance_13[1] = item_to_be_dropped(
            enemy="sin",
            pre_advance_12=advance_12[1],
            pre_advance_13=advance_13[1],
            party_size=party_size,
        )
        advance_12[1] += 4
        if report_dropped_item(
            enemy="sin-fin",
            drop=final_item,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[1] += 1
    if len(drop_chances[2]) >= 1:
        final_item, advance_13[2] = item_to_be_dropped(
            enemy="sin",
            pre_advance_12=advance_12[2],
            pre_advance_13=advance_13[2],
            party_size=party_size,
        )
        advance_12[2] += 4
        if report_dropped_item(
            enemy="sin-fin",
            drop=final_item,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[2] += 1
    advance_10 += 3
    advance_01 += 1

    party_size = 2
    # Sinspawn Echuilles
    drop_chances = track_drops(
        enemy="sinspawn_echuilles", battles=1, extra_advances=advance_10
    )
    if len(drop_chances[0]) >= 1:
        final_item, advance_13[0] = item_to_be_dropped(
            enemy="sinspawn_echuilles",
            pre_advance_12=advance_12[0],
            pre_advance_13=advance_13[0],
            party_size=party_size,
        )
        advance_12[0] += 4
        if report_dropped_item(
            enemy="sinspawn_echuilles",
            drop=final_item,
            pref_type=0,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[0] += 1
    if len(drop_chances[1]) >= 1:
        final_item, advance_13[1] = item_to_be_dropped(
            enemy="sinspawn_echuilles",
            pre_advance_12=advance_12[1],
            pre_advance_13=advance_13[1],
            party_size=party_size,
        )
        advance_12[1] += 4
        if report_dropped_item(
            enemy="sinspawn_echuilles",
            drop=final_item,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[1] += 1
    if len(drop_chances[2]) >= 1:
        final_item, advance_13[2] = item_to_be_dropped(
            enemy="sinspawn_echuilles",
            pre_advance_12=advance_12[2],
            pre_advance_13=advance_13[2],
            party_size=party_size,
        )
        advance_12[2] += 4
        if report_dropped_item(
            enemy="sinspawn_echuilles",
            drop=final_item,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[2] += 1
    advance_10 += 3
    advance_01 += 1

    enemy = "ragora"
    party_size = 5
    # Lancet tutorial
    drop_chances = track_drops(enemy=enemy, battles=1, extra_advances=advance_10)
    if len(drop_chances[0]) >= 1:
        final_item, advance_13[0] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance_12[0],
            pre_advance_13=advance_13[0],
            party_size=party_size,
        )
        advance_12[0] += 4
        if report_dropped_item(
            enemy=enemy,
            drop=final_item,
            pref_type=0,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[0] += 1
    if len(drop_chances[1]) >= 1:
        final_item, advance_13[1] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance_12[1],
            pre_advance_13=advance_13[1],
            party_size=party_size,
        )
        advance_12[1] += 4
        if report_dropped_item(
            enemy=enemy,
            drop=final_item,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[1] += 1
    if len(drop_chances[2]) >= 1:
        final_item, advance_13[2] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance_12[2],
            pre_advance_13=advance_13[2],
            party_size=party_size,
        )
        advance_12[2] += 4
        if report_dropped_item(
            enemy=enemy,
            drop=final_item,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        ):
            thunder_count[2] += 1
    advance_10 += 3
    advance_01 += 1

    party_size = 5
    # Kilika
    geneaux_track = False
    kilika_battles = coming_battles(
        area="kilika_woods", battle_count=3, extra_advances=advance_01
    )
    logs.write_rng_track("Kilika battles:")
    import area.kilika as kilika

    best_battle = kilika.select_best_of_two(kilika_battles)
    ragora_kills = [0, 0, 0]
    if "ragora" in best_battle:
        for i in range(len(best_battle)):
            if best_battle[i] == "ragora":
                ragora_kills[0] += 1
                ragora_kills[1] += 1
                ragora_kills[2] += 1
    best_battle_complete = [False, False, False]

    for b_count in range(kilika_count):
        if b_count == 3 and not geneaux_track:
            advance_10 += 3  # Tentacles
            final_item, advance_13[0] = item_to_be_dropped(
                enemy="sinspawn_geneaux",
                pre_advance_12=advance_12[0],
                pre_advance_13=advance_13[0],
                party_size=party_size,
            )
            advance_12[0] += 4
            report_dropped_item(
                enemy="geneaux",
                drop=final_item,
                pref_type=0,
                pref_ability=0x8026,
                report=report,
            )
            final_item, advance_13[1] = item_to_be_dropped(
                enemy="sinspawn_geneaux",
                pre_advance_12=advance_12[1],
                pre_advance_13=advance_13[1],
                party_size=party_size,
            )
            advance_12[1] += 4
            report_dropped_item(
                enemy="geneaux",
                drop=final_item,
                pref_type=0,
                need_adv=1,
                pref_ability=0x8026,
                report=report,
            )
            final_item, advance_13[2] = item_to_be_dropped(
                enemy="sinspawn_geneaux",
                pre_advance_12=advance_12[2],
                pre_advance_13=advance_13[2],
                party_size=party_size,
            )
            advance_12[2] += 4
            report_dropped_item(
                enemy="geneaux",
                drop=final_item,
                pref_type=0,
                need_adv=2,
                pref_ability=0x8026,
                report=report,
            )

            advance_01 += 1
            geneaux_track = True

        battle_formations = coming_battles(
            area="kilika_woods", battle_count=1, extra_advances=advance_01
        )
        logs.write_rng_track(str(battle_formations))
        for x in range(len(battle_formations)):
            for i in range(len(battle_formations[x])):
                this_battle = battle_formations[x]
                if this_battle == ["ragora"] and ragora_kills[0] == 0:
                    pass
                else:
                    drop_chances = track_drops(
                        enemy=this_battle[i], battles=1, extra_advances=advance_10
                    )
                    if len(drop_chances[0]) >= 1:
                        final_item, advance_13[0] = item_to_be_dropped(
                            enemy=this_battle[i],
                            pre_advance_12=advance_12[0],
                            pre_advance_13=advance_13[0],
                            party_size=party_size,
                        )
                        advance_12[0] += 4
                        if this_battle == "ragora":
                            ragora_kills[0] -= 1
                        elif this_battle == "yellow_element":
                            if final_item.equip_type == 0:
                                if report_dropped_item(
                                    enemy=this_battle[i],
                                    drop=final_item,
                                    pref_type=0,
                                    pref_ability=0x8026,
                                    report=report,
                                ):
                                    thunder_count[0] += 1
                                    kill_yellow[0] = x
                            elif (
                                this_battle[i] == best_battle
                                and not best_battle_complete[0]
                            ):
                                if report_dropped_item(
                                    enemy=this_battle[i],
                                    drop=final_item,
                                    pref_type=0,
                                    pref_ability=0x8026,
                                    report=report,
                                ):
                                    best_battle_complete[0] = True
                            else:
                                advance_12[0] -= 4
                        else:
                            if report_dropped_item(
                                enemy=this_battle[i],
                                drop=final_item,
                                pref_type=0,
                                need_adv=1,
                                pref_ability=0x8026,
                                report=report,
                            ):
                                thunder_count[0] += 1
                    if len(drop_chances[1]) >= 1:
                        final_item, advance_13[1] = item_to_be_dropped(
                            enemy=this_battle[i],
                            pre_advance_12=advance_12[1],
                            pre_advance_13=advance_13[1],
                            party_size=party_size,
                        )
                        advance_12[1] += 4
                        if this_battle == "ragora":
                            ragora_kills[1] -= 1
                        elif this_battle == "yellow_element":
                            if final_item.equip_type == 0:
                                if report_dropped_item(
                                    enemy=this_battle[i],
                                    drop=final_item,
                                    pref_type=0,
                                    pref_ability=0x8026,
                                    report=report,
                                ):
                                    thunder_count[1] += 1
                                    kill_yellow[1] = x
                            elif (
                                this_battle[i] == best_battle
                                and not best_battle_complete[1]
                            ):
                                if report_dropped_item(
                                    enemy=this_battle[i],
                                    drop=final_item,
                                    pref_type=0,
                                    pref_ability=0x8026,
                                    report=report,
                                ):
                                    best_battle_complete[1] = True
                            else:
                                advance_12[1] -= 4
                        else:
                            if report_dropped_item(
                                enemy=this_battle[i],
                                drop=final_item,
                                pref_type=0,
                                need_adv=1,
                                pref_ability=0x8026,
                                report=report,
                            ):
                                thunder_count[1] += 1
                    if len(drop_chances[2]) >= 1:
                        final_item, advance_13[2] = item_to_be_dropped(
                            enemy=this_battle[i],
                            pre_advance_12=advance_12[2],
                            pre_advance_13=advance_13[2],
                            party_size=party_size,
                        )
                        advance_12[2] += 4
                        if this_battle == "ragora":
                            ragora_kills[2] -= 1
                        elif this_battle == "yellow_element":
                            if final_item.equip_type == 0:
                                if report_dropped_item(
                                    enemy=this_battle[i],
                                    drop=final_item,
                                    pref_type=0,
                                    pref_ability=0x8026,
                                    report=report,
                                ):
                                    thunder_count[2] += 1
                                    kill_yellow[2] = x
                            elif (
                                this_battle[i] == best_battle
                                and not best_battle_complete[2]
                            ):
                                if report_dropped_item(
                                    enemy=this_battle[i],
                                    drop=final_item,
                                    pref_type=0,
                                    pref_ability=0x8026,
                                    report=report,
                                ):
                                    best_battle_complete[2] = True
                            else:
                                advance_12[2] -= 4
                        else:
                            if report_dropped_item(
                                enemy=this_battle[i],
                                drop=final_item,
                                pref_type=0,
                                need_adv=1,
                                pref_ability=0x8026,
                                report=report,
                            ):
                                thunder_count[2] += 1
                    advance_10 += 3
            advance_01 += 2

    party_size = 5
    # Workers
    battle_formations = coming_battles(
        area="machina_1", battle_count=1, extra_advances=advance_01
    )
    for x in range(len(battle_formations)):
        for i in range(len(battle_formations[x])):
            this_battle = battle_formations[x]
            drop_chances = track_drops(
                enemy=this_battle, battles=1, extra_advances=advance_10
            )
            if len(drop_chances[0]) >= 1:
                if track_drops(enemy=this_battle, battles=1, extra_advances=advance_10):
                    final_item, advance_13[0] = item_to_be_dropped(
                        enemy=this_battle,
                        pre_advance_12=advance_12[0],
                        pre_advance_13=advance_13[0],
                        party_size=party_size,
                    )
                    advance_12[0] += 4
                    if report_dropped_item(
                        enemy=this_battle,
                        drop=final_item,
                        pref_type=0,
                        pref_ability=0x8026,
                        report=report,
                    ):
                        thunder_count[0] += 1
            if len(drop_chances[1]) >= 1:
                if track_drops(enemy=this_battle, battles=1, extra_advances=advance_10):
                    final_item, advance_13[1] = item_to_be_dropped(
                        enemy=this_battle,
                        pre_advance_12=advance_12[1],
                        pre_advance_13=advance_13[1],
                        party_size=party_size,
                    )
                    advance_12[1] += 4
                    if report_dropped_item(
                        enemy=this_battle,
                        drop=final_item,
                        pref_type=0,
                        need_adv=1,
                        pref_ability=0x8026,
                        report=report,
                    ):
                        thunder_count[1] += 1
            if len(drop_chances[2]) >= 1:
                if track_drops(enemy=this_battle, battles=1, extra_advances=advance_10):
                    final_item, advance_13[2] = item_to_be_dropped(
                        enemy=this_battle,
                        pre_advance_12=advance_12[2],
                        pre_advance_13=advance_13[2],
                        party_size=party_size,
                    )
                    advance_12[2] += 4
                    if report_dropped_item(
                        enemy=this_battle,
                        drop=final_item,
                        pref_type=0,
                        need_adv=2,
                        pref_ability=0x8026,
                        report=report,
                    ):
                        thunder_count[2] += 1
            advance_10 += 3
        advance_01 += 1
    battle_formations = coming_battles(
        area="machina_2", battle_count=1, extra_advances=advance_01
    )
    for x in range(len(battle_formations)):
        for i in range(len(battle_formations[x])):
            this_battle = battle_formations[x]
            drop_chances = track_drops(
                enemy=this_battle, battles=1, extra_advances=advance_10
            )
            if len(drop_chances[0]) >= 1:
                if track_drops(enemy=this_battle, battles=1, extra_advances=advance_10):
                    final_item, advance_13[0] = item_to_be_dropped(
                        enemy=this_battle,
                        pre_advance_12=advance_12[0],
                        pre_advance_13=advance_13[0],
                        party_size=party_size,
                    )
                    advance_12[0] += 4
                    if report_dropped_item(
                        enemy=this_battle,
                        drop=final_item,
                        pref_type=0,
                        pref_ability=0x8026,
                        report=report,
                    ):
                        thunder_count[0] += 1
            if len(drop_chances[1]) >= 1:
                if track_drops(enemy=this_battle, battles=1, extra_advances=advance_10):
                    final_item, advance_13[1] = item_to_be_dropped(
                        enemy=this_battle,
                        pre_advance_12=advance_12[1],
                        pre_advance_13=advance_13[1],
                        party_size=party_size,
                    )
                    advance_12[1] += 4
                    if report_dropped_item(
                        enemy=this_battle,
                        drop=final_item,
                        pref_type=0,
                        need_adv=1,
                        pref_ability=0x8026,
                        report=report,
                    ):
                        thunder_count[1] += 1
            if len(drop_chances[2]) >= 1:
                if track_drops(enemy=this_battle, battles=1, extra_advances=advance_10):
                    final_item, advance_13[2] = item_to_be_dropped(
                        enemy=this_battle,
                        pre_advance_12=advance_12[2],
                        pre_advance_13=advance_13[2],
                        party_size=party_size,
                    )
                    advance_12[2] += 4
                    if report_dropped_item(
                        enemy=this_battle,
                        drop=final_item,
                        pref_type=0,
                        need_adv=2,
                        pref_ability=0x8026,
                        report=report,
                    ):
                        thunder_count[2] += 1
            advance_10 += 3
        advance_01 += 1
    battle_formations = coming_battles(
        area="machina_3", battle_count=1, extra_advances=advance_01
    )
    for x in range(len(battle_formations)):
        for i in range(len(battle_formations[x])):
            this_battle = battle_formations[x]
            drop_chances = track_drops(
                enemy=this_battle, battles=1, extra_advances=advance_10
            )
            if len(drop_chances[0]) >= 1:
                if track_drops(enemy=this_battle, battles=1, extra_advances=advance_10):
                    final_item, advance_13[0] = item_to_be_dropped(
                        enemy=this_battle,
                        pre_advance_12=advance_12[0],
                        pre_advance_13=advance_13[0],
                        party_size=party_size,
                    )
                    advance_12[0] += 4
                    if report_dropped_item(
                        enemy=this_battle,
                        drop=final_item,
                        pref_type=0,
                        pref_ability=0x8026,
                        report=report,
                    ):
                        thunder_count[0] += 1
            if len(drop_chances[1]) >= 1:
                if track_drops(enemy=this_battle, battles=1, extra_advances=advance_10):
                    final_item, advance_13[1] = item_to_be_dropped(
                        enemy=this_battle,
                        pre_advance_12=advance_12[1],
                        pre_advance_13=advance_13[1],
                        party_size=party_size,
                    )
                    advance_12[1] += 4
                    if report_dropped_item(
                        enemy=this_battle,
                        drop=final_item,
                        pref_type=0,
                        need_adv=1,
                        pref_ability=0x8026,
                        report=report,
                    ):
                        thunder_count[1] += 1
            if len(drop_chances[2]) >= 1:
                if track_drops(enemy=this_battle, battles=1, extra_advances=advance_10):
                    final_item, advance_13[2] = item_to_be_dropped(
                        enemy=this_battle,
                        pre_advance_12=advance_12[2],
                        pre_advance_13=advance_13[2],
                        party_size=party_size,
                    )
                    advance_12[2] += 4
                    if report_dropped_item(
                        enemy=this_battle,
                        drop=final_item,
                        pref_type=0,
                        need_adv=2,
                        pref_ability=0x8026,
                        report=report,
                    ):
                        thunder_count[2] += 1
            advance_10 += 3
        advance_01 += 1

    # Finally, Oblitz is guaranteed to drop an item.
    final_item, advance_13[0] = item_to_be_dropped(
        enemy="oblitzerator",
        pre_advance_12=advance_12[0],
        pre_advance_13=advance_13[0],
        party_size=party_size,
    )
    if report_dropped_item(
        enemy="Oblitzerator",
        drop=final_item,
        pref_type=0,
        pref_ability=0x8026,
        report=report,
    ):
        thunder_count[0] += 1
        oblitz_weap[0] = True
    final_item, advance_13[1] = item_to_be_dropped(
        enemy="oblitzerator",
        pre_advance_12=advance_12[1],
        pre_advance_13=advance_13[1],
        party_size=party_size,
    )
    if report_dropped_item(
        enemy="Oblitzerator",
        drop=final_item,
        pref_type=0,
        need_adv=1,
        pref_ability=0x8026,
        report=report,
    ):
        thunder_count[1] += 1
        oblitz_weap[1] = True
    final_item, advance_13[2] = item_to_be_dropped(
        enemy="oblitzerator",
        pre_advance_12=advance_12[2],
        pre_advance_13=advance_13[2],
        party_size=party_size,
    )
    if report_dropped_item(
        enemy="Oblitzerator",
        drop=final_item,
        pref_type=0,
        need_adv=2,
        pref_ability=0x8026,
        report=report,
    ):
        thunder_count[2] += 1
        oblitz_weap[2] = True
    advance_12[0] += 4
    advance_10 += 3

    logs.write_rng_track("End: thunder strike drops")
    logs.write_rng_track("===================")
    logs.write_rng_track("The following values are per advance.")
    logs.write_rng_track("Drops possible:" + str(thunder_count))
    logs.write_rng_track("Weapon drops on Oblitzerator:" + str(oblitz_weap))
    logs.write_rng_track("Kill Yellow ele on Kilika battles:" + str(kill_yellow))
    return thunder_count, kill_yellow


def decide_skip_zan_luck() -> bool:
    # This function tracks if we need to pick up the luck and
    # fortune spheres in Zanarkand. This will track through from Yunalesca to BFA,
    # the two fights with ~4% chance to miss.
    # False == there will be a miss.
    # True == no miss.
    extra_xp = 1
    bahamut_luck = 17
    keeper_crit = memory.main.future_attack_will_crit(
        character=7, char_luck=bahamut_luck, enemy_luck=20, attack_index=extra_xp
    )
    arm1Crit = False
    arm2Crit = False
    face_crit = False

    attack_count = extra_xp
    if keeper_crit:
        logger.debug("Expecting crit on SK")
        attack_count += 1
    else:
        attack_count += 2

    # Now to test the Yunalesca fight. Crits do not matter here, only hit chance.
    for i in range(3):
        logger.debug(f"Yunalesca attack num {i} | {attack_count}")
        if not future_attack_hit(
            character=7, enemy="yunalesca", attack_index=attack_count
        ):
            logger.debug(f"Miss on Yunalesca, attack number {i}")
            return False
        attack_count += 1
    if game_vars.nemesis():  # BFA miss does not factor in for Nemesis route.
        return True

    arm1Crit = memory.main.future_attack_will_crit(
        character=7, char_luck=bahamut_luck, enemy_luck=15, attack_index=attack_count
    )
    if arm1Crit:
        logger.debug("Expecting crit on Arm 1")
        attack_count += 1
    else:
        logger.debug("Expecting no crit on Arm 1")
        attack_count += 2
    arm2Crit = memory.main.future_attack_will_crit(
        character=7, char_luck=bahamut_luck, enemy_luck=15, attack_index=attack_count
    )
    if arm2Crit:
        logger.debug("Expecting crit on Arm 2")
        attack_count += 1
    else:
        logger.debug("Expecting no crit on Arm 2")
        attack_count += 2
    attack_count += 1  # Core is always one attack
    face_crit = memory.main.future_attack_will_crit(
        character=7, char_luck=bahamut_luck, enemy_luck=15, attack_index=attack_count
    )
    if face_crit:
        logger.debug("Expecting crit on Face/impulse")
    else:
        face_crit = memory.main.future_attack_will_crit(
            character=7,
            char_luck=bahamut_luck,
            enemy_luck=15,
            attack_index=attack_count + 1,
        )
        if face_crit:
            logger.debug("Expecting crit on Face/attack (first)")
    if face_crit:
        attack_count += 2
    elif game_vars.rng_seed_num() == 31:
        attack_count += 2
    else:
        logger.debug("Expecting no crit on Face")
        attack_count += 3  # Should be 3, but we're over-damaging.
    if not future_attack_hit(
        character=7, enemy="seymour_omnis", attack_index=attack_count
    ):
        logger.debug("Miss on Omnis")
        return False
    else:
        logger.debug("No miss on Omnis")
    attack_count += 1  # One attack on Seymour
    for i in range(3):
        logger.debug(f"BFA attack num {i} | {attack_count}")
        if not future_attack_hit(character=7, enemy="bfa", attack_index=attack_count):
            logger.debug(f"Miss on BFA, attack number {i}")
            return False
        attack_count += 1
    logger.debug("No misses registered. Should be good to skip Luck/Fortune chests.")
    return True


def zombie_track(report=False):
    advance_01 = 0
    advance_10 = 0
    advance_12 = [0] * 3
    advance_13 = [0] * 3
    zombie_results = [99] * 3
    party_size = 7

    # "sanctuary_keeper"
    # Check random encounters for best charge,
    # plan for 1 encounter, 1 death if possible to charge.
    # "spectral_keeper"
    # "yunalesca"

    enemy = "sanctuary_keeper"
    drop_chances = track_drops(enemy=enemy, battles=1, extra_advances=advance_10)
    if len(drop_chances[0]) >= 1:
        final_item, advance_13[0] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance_12[0],
            pre_advance_13=advance_13[0],
            party_size=party_size,
        )
        advance_12[0] += 4
        report_dropped_item(
            enemy=enemy,
            drop=final_item,
            pref_type=0,
            pref_ability=0x8032,
            report=report,
        )
    if len(drop_chances[1]) >= 1:
        final_item, advance_13[1] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance_12[1],
            pre_advance_13=advance_13[1],
            party_size=party_size,
        )
        advance_12[1] += 4
        report_dropped_item(
            enemy=enemy,
            drop=final_item,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8032,
            report=report,
        )
    if len(drop_chances[2]) >= 1:
        final_item, advance_13[2] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance_12[2],
            pre_advance_13=advance_13[2],
            party_size=party_size,
        )
        advance_12[2] += 4
        report_dropped_item(
            enemy=enemy,
            drop=final_item,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8032,
            report=report,
        )
    advance_10 += 3
    advance_01 += 1

    import area.zanarkand as zanarkand

    zanarkand.decide_nea(bonus_advance=1)
    # One death expected to recharge Rikku. No drops expected.
    if game_vars.get_nea_zone() in [1, 2]:
        advance_10 += 3
        advance_01 += 1

    enemy = "spectral_keeper"
    drop_chances = track_drops(enemy=enemy, battles=1, extra_advances=advance_10)
    if len(drop_chances[0]) >= 1:
        final_item, advance_13[0] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance_12[0],
            pre_advance_13=advance_13[0],
            party_size=party_size,
        )
        advance_12[0] += 4
        report_dropped_item(
            enemy=enemy,
            drop=final_item,
            pref_type=0,
            pref_ability=0x8032,
            report=report,
        )
    if len(drop_chances[1]) >= 1:
        final_item, advance_13[1] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance_12[1],
            pre_advance_13=advance_13[1],
            party_size=party_size,
        )
        advance_12[1] += 4
        report_dropped_item(
            enemy=enemy,
            drop=final_item,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8032,
            report=report,
        )
    if len(drop_chances[2]) >= 1:
        final_item, advance_13[2] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance_12[2],
            pre_advance_13=advance_13[2],
            party_size=party_size,
        )
        advance_12[2] += 4
        report_dropped_item(
            enemy=enemy,
            drop=final_item,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8032,
            report=report,
        )
    advance_10 += 3
    advance_01 += 1

    enemy = "yunalesca"
    drop_chances = track_drops(enemy=enemy, battles=1, extra_advances=advance_10)
    if len(drop_chances[0]) >= 1:
        final_item, advance_13[0] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance_12[0],
            pre_advance_13=advance_13[0],
            party_size=party_size,
        )
        advance_12[0] += 4
        if report_dropped_item(
            enemy=enemy,
            drop=final_item,
            pref_type=0,
            pref_ability=0x8032,
            report=report,
        ):
            zombie_results[0] = final_item.equip_owner_alt
    if len(drop_chances[1]) >= 1:
        final_item, advance_13[1] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance_12[1],
            pre_advance_13=advance_13[1],
            party_size=party_size,
        )
        advance_12[1] += 4
        if report_dropped_item(
            enemy=enemy,
            drop=final_item,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8032,
            report=report,
        ):
            zombie_results[1] = final_item.equip_owner_alt
    if len(drop_chances[2]) >= 1:
        final_item, advance_13[2] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance_12[2],
            pre_advance_13=advance_13[2],
            party_size=party_size,
        )
        advance_12[2] += 4
        if report_dropped_item(
            enemy=enemy,
            drop=final_item,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8032,
            report=report,
        ):
            zombie_results[2] = final_item.equip_owner_alt
    advance_10 += 3
    advance_01 += 1

    return zombie_results


def nea_track():
    pre_advance_12 = 0
    pre_advance_13 = 0

    total_advance_pre_x = 999
    total_advance_post_x = 999

    # If already aligned for NEA, we want X to drop nothing.
    next_item, pre_advance_13 = item_to_be_dropped(enemy="ghost")
    if next_item.equipment_type() == 1 and next_item.has_ability(0x801D):
        total_advance_post_x = 0
    while (
        total_advance_pre_x == 999
        or total_advance_post_x == 999
        and pre_advance_12 < 100
    ):
        pre_advance_12 += 4
        next_item, pre_advance_13 = item_to_be_dropped(
            enemy="ghost", pre_advance_12=pre_advance_12, pre_advance_13=pre_advance_13
        )
        if next_item.equipment_type() == 1 and 0x801D in next_item.abilities():
            if total_advance_post_x == 999:
                total_advance_post_x = int(pre_advance_12 / 4)
            if total_advance_pre_x == 999:
                total_advance_pre_x = int((pre_advance_12 / 4) - 1)
    # logger.debug(f"// Pre-X: {total_advance_pre_x} // Post-X {total_advance_post_x}")
    return total_advance_pre_x, total_advance_post_x


def print_manip_info():
    pre_x, post_x = nea_track()
    logger.manip("Upcoming RNGs:")
    logger.manip(f"Next drop: {post_x}")
    logger.manip(
        f"RNG10: {memory.main.next_chance_rng_10()} | "
        + f"Adjusted for Defender X drop: {memory.main.next_chance_rng_10_calm()}"
    )


def next_action_escape(character: int = 0):
    index = 20 + character
    escape_roll = (
        memory.main.s32(memory.main.rng_array_from_index(index=index, array_len=1)[1])
        & 255
    )
    return escape_roll < 191


def next_action_hit(character: int = 0, enemy: str = "anima"):
    return future_attack_hit(character=character, enemy=enemy)


def future_attack_hit(character: int = 0, enemy: str = "anima", attack_index: int = 1):
    # logger.debug(f"Checking hit chance - character: {character}")
    # Need more work on this. There are a lot of variables we still need from memory.
    # Character info, get these from memory
    index = 36 + character
    luck = memory.main.char_luck(character)
    accuracy = memory.main.char_accuracy(character)

    if enemy == "bfa":
        target_luck = 15
        target_evasion = 0
    else:
        # Data directly from the tracker
        target_luck = MONSTERS[enemy].stats["Luck"]
        # logger.debug(f"Enemy luck: {target_luck}")
        target_evasion = MONSTERS[enemy].stats["Evasion"]
        # logger.debug(f"Enemy evasion: {target_evasion}")

    # Unused, but technically part of the formula
    aims = 0
    target_reflexes = 0

    accuracy_index = ((accuracy * 2 * 0x66666667) // 0xFFFFFFFF) // 2
    hit_chance_index = accuracy_index - target_evasion + 10
    if hit_chance_index < 0:
        hit_chance_index = 0
    elif hit_chance_index > 8:
        hit_chance_index = 8
    base_hit_chance = hit_chance_table(hit_chance_index)

    hit_rng = (
        memory.main.rng_array_from_index(index=index, array_len=attack_index + 3)[
            attack_index
        ]
        % 101
    )

    hit_chance = base_hit_chance + luck - target_luck
    hit_chance += (aims - target_reflexes) * 10
    return hit_chance > hit_rng


def hit_chance_table(index: int):
    if index == 0:
        return 25
    elif index in [1, 2]:
        return 30
    elif index in [3, 4]:
        return 40
    elif index in [5, 6]:
        return 50
    elif index == 7:
        return 80
    elif index == 8:
        return 100


def oblitz_history():
    filepath = os.path.join("json_ai_files", "oblitz_results.json")
    with open(filepath, "r") as fp:
        rng_values = json.load(fp)
    return rng_values


def save_oblitz_history(rng_vals):
    writing = dict(rng_vals)
    filepath = os.path.join("json_ai_files", "oblitz_results.json")
    with open(filepath, "w") as fp:
        json.dump(writing, fp, indent=4)


def record_blitz_results_tyton(duration, test_mode=False):
    records = oblitz_history()
    if test_mode:
        seed = "999"
        sub_key = "9999"
        victory = False
    else:
        seed = str(memory.main.rng_seed())
        sub_key = str(game_vars.oblitz_rng_check())
        victory = game_vars.get_blitz_win()
    if seed in records.keys():
        if sub_key in records[seed].keys():
            if records[seed][sub_key]["victory"] and not victory:
                return
            if (
                records[seed][sub_key]["victory"] == victory
                and duration >= records[str(seed)][str(sub_key)]["duration"]
                and game_vars.csr()
            ):
                return

    records[seed][sub_key]["duration"] = duration
    records[seed][sub_key]["victory"] = victory
    save_oblitz_history(records)


def record_blitz_results(duration, test_mode=False):
    filepath = os.path.join("json_ai_files", "oblitz_results.json")
    records = oblitz_history()
    if test_mode:
        new_val = {999: {9999: {"duration": duration, "victory": False}}}
        if str(999) in records.keys():
            logger.debug(new_val[999].keys())
            if 9999 in new_val[999].keys():
                records["999"]["9999"]["victory"] = True
                records["999"]["9999"]["duration"] = duration
            else:
                records["999"].update(new_val[999])
        else:
            records.update(new_val)
    else:
        new_val = {
            memory.main.rng_seed(): {
                game_vars.oblitz_rng_check(): {
                    "duration": duration,
                    "victory": game_vars.get_blitz_win(),
                }
            }
        }
        if str(memory.main.rng_seed()) in records.keys():
            if (
                game_vars.oblitz_rng_check()
                in records[str(memory.main.rng_seed())].keys()
            ):
                if (
                    not game_vars.get_blitz_win()
                    and records[str(memory.main.rng_seed())][
                        game_vars.oblitz_rng_check()
                    ]["victory"]
                ):
                    records[str(memory.main.rng_seed())][game_vars.oblitz_rng_check()][
                        "victory"
                    ] = game_vars.get_blitz_win()
                    records[str(memory.main.rng_seed())][game_vars.oblitz_rng_check()][
                        "duration"
                    ] = duration
                elif (
                    game_vars.get_blitz_win()
                    == records[str(memory.main.rng_seed())][
                        game_vars.oblitz_rng_check()
                    ]["victory"]
                ):
                    if (
                        duration
                        < records[str(memory.main.rng_seed())][
                            game_vars.oblitz_rng_check()
                        ]["duration"]
                    ):  # Prefer faster times, even if it's not consistent.
                        records[str(memory.main.rng_seed())][
                            game_vars.oblitz_rng_check()
                        ]["victory"] = game_vars.get_blitz_win()
                        records[str(memory.main.rng_seed())][
                            game_vars.oblitz_rng_check()
                        ]["duration"] = duration
            else:
                records[str(memory.main.rng_seed())].update(
                    new_val[memory.main.rng_seed()]
                )
        else:
            records.update(new_val)
    logger.debug(new_val)

    # logger.debug(records)

    with open(filepath, "w") as fp:
        json.dump(records, fp, indent=4)


def hits_to_seed(hits_array: int):
    with open("csv\\hits_to_seed.csv", "r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row["hit0"] == "":
                pass
            elif (
                int(row["hit0"]) == hits_array[0]
                and int(row["hit1"]) == hits_array[1]
                and int(row["hit2"]) == hits_array[2]
                and int(row["hit3"]) == hits_array[3]
                and int(row["hit4"]) == hits_array[4]
                and int(row["hit5"]) == hits_array[5]
            ):
                return row["seed"]
    return "Err_seed_not_found"
