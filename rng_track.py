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
    try:
        library_check = MONSTERS[fiend_name].stats["Luck"]
        logger.debug(f"== Dict Check: {library_check}")
        return library_check
    except:
        if fiend_name in ["arm","cid","circle","crane","dummy","gate_lock","gate_lock_2","gemini"]:
            return 0
        if fiend_name in ["geneauxs_tentacle","head","kimahri_weapon","mortiphasm","mortiphasm_3"]:
            return 0
        if fiend_name in ["mortiphasm_4","mortiphasm_5","negator","nemesis","oblitzerator"]:
            return 0
        if fiend_name.find("possessed") != -1:
            return 0
        if fiend_name.find("sinscale") != -1:
            return 1
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
    report:bool = True
):
    test_mode = False
    slot_mod = slot_modifier(enemy=enemy)
    ability_mod = ability_modifier(enemy=enemy)
    
    party_chars = memory.main.get_order_six()
    # Focused on NEA manip, we'd need to back fill this later to other fights.
    if enemy == "evrae":
        party_chars = [0,2,3,4,5,6]
    elif enemy == "larva":
        party_chars = [1,2]
    elif enemy == "evrae_altana":
        party_chars = [0,4,6]
    elif enemy == "ykt-63":
        party_chars = [0,1,2,4,5,6]
    elif enemy in ["seymour_natus","defender_x","yenke_ronso","biran_ronso","ghost"]:
        party_chars = [0,1,2,3,4,5,6]
    else:
        # Good old bubble sort
        for i in range(len(party_chars)):
            for j in range(i, len(party_chars)):
                if party_chars[j] < party_chars[i]:
                    temp = party_chars[j]
                    party_chars[j] = party_chars[i]
                    party_chars[i] = temp
    '''
    if party_size == 2:
        party_chars = [0, 4]
    elif party_size == 3:  # Oblitzerator
        party_chars = [0, 3, 5]
    elif party_size == 4:
        party_chars = [0, 1, 4, 5]
    elif party_size == 5:
        party_chars = [0, 1, 3, 4, 5]
    elif party_size == 6:  # rescue_yuna section
        party_chars = [0, 2, 3, 4, 5, 6]
    elif party_size == 7:
        party_chars = [0, 1, 2, 3, 4, 5, 6]
    else:
        party_chars = [0]
    '''
    #logger.warning(party_chars)

    advance_12 = 8 + pre_advance_12
    test_array_12 = memory.main.rng_12_array(advance_12)
    del test_array_12[0]
    if pre_advance_12 >= 1:
        while pre_advance_12 >= 1:
            del test_array_12[0]
            pre_advance_12 -= 1

    # Assume killer is not aeon
    user_2 = party_chars[(test_array_12[0] & 0x7FFFFFFF) % len(party_chars)]
    party_chars.append(9)
    party_chars.append(9)
    party_chars.append(9)
    # Assume killer is aeon
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
    
    # Killer - NEA drop only
    character = user_2  # Represents any killer except Auron or Kimahri.
    if enemy == "biran_ronso" or enemy == "yenke_ronso":
        character = 3
    elif enemy in ["defender_x", "maze_larva"]:
        character = user_1

    # rng13 logic here, determine which ability goes where.
    ability_list, advances = ability_to_be_dropped(
        enemy=enemy,
        equip_type=equip_type,
        slots=slots,
        ability_count=ability_count,
        advances=pre_advance_13,
        char=character
    )
    if test_mode:
        logger.debug(f"New Abilities: {ability_list}")
        logger.debug(f"OWNER CHECK   (aeon): {user_1}")
        logger.debug(f"OWNER CHECK (killer): {user_2}")

    final_item = memory.main.Equipment(equip_num=0)
    final_item.create_custom(
        e_type=equip_type,
        e_owner_1=user_1,
        e_owner_2=user_2,
        e_slots=slots,
        e_abilities=ability_list,
    )
    

    #return final_item, int(pre_advance_13 + advances)
    return final_item, advances


def ability_to_be_dropped(
    enemy: str = "ghost", equip_type: int = 0, slots: int = 1, advances: int = 0,
    ability_count:int=1, char:int = 0
):
    test_mode = False  # Doesn't functionally change, but prints more stuff.
    outcomes = drop_ability_list(enemy=enemy, equip_type=equip_type)
    filled_slots = [99] * slots
    if char in [2,3] and equip_type == 0:  # Weapon for Auron or Kimahri
        filled_slots.remove(99)
        filled_slots.append(0x800B)
        ability_count -= 1
    
    
    found = 0
    ptr = 0  # Pointer that indicates how many advances needed for this evaluation
    test_array = memory.main.rng_13_array(array_len=50 + advances)
    
    if test_mode:
        logger.debug(f"Enemy: {enemy} - Outcomes: {outcomes}")

    while 99 in filled_slots and ptr < 50 + advances and found < ability_count:
        # Increment to match the first (and subsequent) advance(s)
        try:
            ptr += 1
            if test_mode and enemy=="ghost":
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

    return [filled_slots, ptr]


def report_dropped_item(
    enemy: str,
    drop=memory.main.Equipment,
    pref_type: int = 99,
    pref_ability: int = 255,
    need_adv: int = 0,
    report=False,
):
    report=False  # For now, we don't want to see this. Slows down the TAS slightly.
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


def nea_track(pre_defender_x:bool = False, report=False):
    drop_x = False
    bny = False
    advances = 0
    #logger.warning(memory.main.rng_array_from_index(index=12, array_len=20))
    #logger.warning(memory.main.rng_array_from_index(index=13, array_len=20))
    if pre_defender_x:
        stage = 2
    else:
        stage = 3
    
    paths, best = purifico_to_nea(
        stage=stage,
        report=False
    )
    if best == 99:
        return (99,99)
    
    bny = bool(best >= len(paths)/2)
    if stage == 2:
        drop_x = bool((best % 4) >= 2)
        if not drop_x:
            advances = 1
    
    if drop_x != game_vars.get_def_x_drop():
        game_vars.set_def_x_drop(drop_x)
    #logger.manip(f"    BnY: {bny}")
    #logger.manip(f"BnY_var: {game_vars.get_nea_after_bny()}")
    if bny != game_vars.get_nea_after_bny():
        game_vars.set_nea_after_bny(bny)
    if report:
        logger.manip(
            f"Defender X: {game_vars.get_def_x_drop()}, Ronso before NEA: {game_vars.get_nea_after_bny()}"
        )
    
    #if not drop_x and not bny:
    #    return (paths[best], memory.main.next_chance_rng_10_calm())
    #elif not drop_x and memory.main.next_chance_rng_10() != 0:
    #    return (paths[best], 0)
    #else:
    return (advances, memory.main.next_chance_rng_10())
    # Note return of 0 means we don't need any extra mobs, other than X or Ronso.


def print_manip_info(pre_x=False):
    if pre_x:
        purifico_to_nea(stage=2, report=True)
    else:
        purifico_to_nea(stage=3, report=True)
    _, advances = nea_track(pre_defender_x=pre_x, report=True)
    logger.manip(f"Setting up for NEA | " + \
    f"X: {game_vars.get_def_x_drop()} | " + \
    f"B&Y: {game_vars.get_nea_after_bny()}")
    logger.manip(f"We need {advances} extra advances for next equipment drop.")
    logger.manip(f"(One advance per steal, three per player or enemy death)")
    

def desert_to_evrae_equip_drop_count() -> []:
    drop_count = [1,1,1]  # Evrae will always drop one equipment.
    test_array = memory.main.rng_10_array()
    ptr = 3 # Ignore first two rolls, we don't care about item drops.

    # Guado guardian and three bombs
    chance = 12
    for i in range(3):  # Guado
        if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
            drop_count[i] += 1
    ptr += 3
    for i in range(3):  # Bomb
        if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
            drop_count[i] += 1
    ptr += 3
    for i in range(3):  # Bomb
        if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
            drop_count[i] += 1
    ptr += 3
    for i in range(3):  # Bomb
        if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
            drop_count[i] += 1
    ptr += 3

    # Dual horns and guado guardian
    for i in range(3):  # Dual Horn
        if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
            drop_count[i] += 1
    ptr += 3
    for i in range(3):  # Dual Horn
        if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
            drop_count[i] += 1
    ptr += 3
    chance = 60
    for i in range(3):  # Guado
        if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
            drop_count[i] += 1
    ptr += 3

    # Chimeras and guado
    chance = 12
    for i in range(3):  # Guado
        if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
            drop_count[i] += 1
    ptr += 3
    for i in range(3):  # Guado
        if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
            drop_count[i] += 1
    ptr += 3
    chance = 60
    for i in range(3):  # Guado
        if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
            drop_count[i] += 1
    ptr += 3

    return drop_count


def enemy_target_predictions(attacks:int=4, chars:int=3):
    rolls = memory.main.rng_array_from_index(index=4, array_len=attacks+3)
    results = []
    
    for i in range(attacks):
        results.append((rolls[i+1] & 0x7FFFFFFF) % chars)
    
    logger.manip(f"Target predictions: {results}")
    return results


def evrae_targets() -> []:
    rolls = memory.main.rng_array_from_index(index=4, array_len=5)
    results = [9,9]
    results[0] = (rolls[1] & 0x7FFFFFFF) % 3
    
    if results[0] == 0:
        results[1] = (rolls[2] & 0x7FFFFFFF) % 3
    else:
        results[1] = (rolls[2] & 0x7FFFFFFF) % 2
        if results[0] == results[1]:  # Can only occur if both == 1
            results[1] = 2
    return results


def guards_to_calm_equip_drop_count(
    guard_battle_num:int, 
    ptr:int = 3, 
    pre_Evrae:bool = False,
    report_num = 99
) -> []:
    if pre_Evrae:
        final, ptr13 = item_to_be_dropped(enemy="evrae")
        if final.equipment_type() == 0:
            weap = "weapon"
        else:
            weap = "armor"
        #logger.warning(f"Evrae drops {weap} for {final.owner()} - [{final.abilities()}]")
        #logger.warning(f"RNG13 after Evrae: {memory.main.rng_array_from_index(index=13, array_len=ptr13+20)[ptr13]}")
        drop_count = [["evrae"],["evrae"],["evrae"]]  # Count for Altana, Natus, and NEA.
        ptr += 3
        tars = evrae_targets()
        if 1 in tars:
            ptr += 3
        if 2 in tars:
            ptr += 3
        #logger.warning(f"Evrae advance manips: {ptr}, {tars}")
    else:
        drop_count = [[],[],[]]  # Count for Altana, Natus, and NEA.
    test_array = memory.main.rng_10_array()
    #for x in range(ptr+10):
    #    logger.debug(f"{ptr}: {x}: {test_array[x]}")

    # Three warrior monks
    chance = 12
    if guard_battle_num <= 1:
        for i in range(3):  # Monk
            if guard_battle_num == 1:
                if (test_array[ptr] & 0x7FFFFFFF) % 255 < chance:  # Tidus kills these first
                    drop_count[i].append("warrior_monk")
                    if i == report_num:
                        logger.manip(f"{i}: Battle 1 drops equipment")
            else:
                if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:  # Tidus kills these first
                    drop_count[i].append("warrior_monk")
                    if i == report_num:
                        logger.manip(f"{i}: Battle 1 drops equipment")
        ptr += 6  # Accounting for firearm 'death'
        for i in range(3):  # Monk
            if guard_battle_num == 1:
                if (test_array[ptr] & 0x7FFFFFFF) % 255 < chance:  # Tidus kills these first
                    drop_count[i].append("warrior_monk_2")
                    if i == report_num:
                        logger.manip(f"{i}: Battle 1 drops equipment")
            else:
                if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:  # Tidus kills these first
                    drop_count[i].append("warrior_monk_2")
                    if i == report_num:
                        logger.manip(f"{i}: Battle 1 drops equipment")
        ptr += 6  # Accounting for firearm 'death'
        for i in range(3):  # Monk
            if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
                drop_count[i].append("warrior_monk")
                if i == report_num:
                    logger.manip(f"{i}: Battle 1 drops equipment")
        ptr += 6  # Accounting for firearm 'death'

    # YKT-63 and two monks. If second battle, assumes Tidus killed the bot.
    if guard_battle_num <= 2:
        chance = 30
        for i in range(3):  # YKT-63 dies first.
            if guard_battle_num == 2:
                if (test_array[ptr] & 0x7FFFFFFF) % 255 < chance:
                    drop_count[i].append("ykt-63")
                    if i == report_num:
                        logger.manip(f"{i}: Battle 2 drops equipment")
            else:
                if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
                    drop_count[i].append("ykt-63")
                    if i == report_num:
                        logger.manip(f"{i}: Battle 2 drops equipment")
        ptr += 3
        chance = 12
        for i in range(3):  # Monk
            if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
                drop_count[i].append("warrior_monk")
                if i == report_num:
                    logger.manip(f"{i}: Battle 2 drops equipment")
        ptr += 3
        for i in range(3):  # Monk
            if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
                drop_count[i].append("warrior_monk")
                if i == report_num:
                    logger.manip(f"{i}: Battle 2 drops equipment")
        ptr += 9  # Accounting for firearm 'deaths'

    # Three MORE monks
    if guard_battle_num <= 3:
        chance = 12
        # Figure out later a way to count remaining enemies in this battle.
        for i in range(3):  # Monk
            if guard_battle_num == 3:
                if (test_array[ptr] & 0x7FFFFFFF) % 255 < chance:  # Tidus kills these first
                    drop_count[i].append("warrior_monk")
                    if i == report_num:
                        logger.manip(f"{i}: Battle 3 drops equipment")
            else:
                if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:  # Tidus kills these first
                    drop_count[i].append("warrior_monk")
                    if i == report_num:
                        logger.manip(f"{i}: Battle 3 drops equipment")
        ptr += 6  # Accounting for firearm 'death'
        for i in range(3):  # Monk
            if guard_battle_num == 3:
                if (test_array[ptr] & 0x7FFFFFFF) % 255 < chance:  # Tidus kills these first
                    drop_count[i].append("warrior_monk_2")
                    if i == report_num:
                        logger.manip(f"{i}: Battle 3 drops equipment")
            else:
                if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:  # Tidus kills these first
                    drop_count[i].append("warrior_monk_2")
                    if i == report_num:
                        logger.manip(f"{i}: Battle 3 drops equipment")
        ptr += 6  # Accounting for firearm 'death'
        for i in range(3):  # Monk
            if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
                drop_count[i].append("warrior_monk")
                if i == report_num:
                    logger.manip(f"{i}: Battle 3 drops equipment")
        ptr += 6  # Accounting for firearm 'death'
        
    # YKT-63 and two monks, again. If fourth battle, assumes Tidus killed the bot.
    if guard_battle_num <= 4:
        chance = 30
        for i in range(3):  # YKT-63 dies first.
            if guard_battle_num == 4:
                if (test_array[ptr] & 0x7FFFFFFF) % 255 < chance:
                    drop_count[i].append("ykt-63")
                    if i == report_num:
                        logger.manip(f"{i}: Battle 4 drops equipment")
            else:
                if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
                    drop_count[i].append("ykt-63")
                    if i == report_num:
                        logger.manip(f"{i}: Battle 4 drops equipment")
        ptr += 3
        chance = 12
        for i in range(3):  # Monk
            if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
                drop_count[i].append("warrior_monk")
                if i == report_num:
                    logger.manip(f"{i}: Battle 4 drops equipment")
        ptr += 3
        for i in range(3):  # Monk
            if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
                drop_count[i].append("warrior_monk")
                if i == report_num:
                    logger.manip(f"{i}: Battle 4 drops equipment")
        ptr += 9  # Accounting for firearm 'deaths'
 
    # Final battle
    if guard_battle_num <= 5:
        for i in range(3):  # Monk dies first
            if guard_battle_num == 5:
                if (test_array[ptr] & 0x7FFFFFFF) % 255 < chance:
                    drop_count[i].append("warrior_monk")
                    if i == report_num:
                        logger.manip(f"{i}: Battle 5 drops equipment")
            else:
                if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
                    drop_count[i].append("warrior_monk")
                    if i == report_num:
                        logger.manip(f"{i}: Battle 5 drops equipment")
        ptr += 3
        for i in range(3):  # Monk dies first
            if guard_battle_num == 5:
                if (test_array[ptr] & 0x7FFFFFFF) % 255 < chance:
                    drop_count[i].append("warrior_monk")
                    if i == report_num:
                        logger.manip(f"{i}: Battle 5 drops equipment")
            else:
                if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
                    drop_count[i].append("warrior_monk")
                    if i == report_num:
                        logger.manip(f"{i}: Battle 5 drops equipment")
        ptr += 9  # Accounting for firearm 'deaths'
        chance = 30
        for i in range(3):  # YAT-99 dies last.
            if (test_array[ptr+i] & 0x7FFFFFFF) % 255 < chance:
                drop_count[i].append("yat-99")
                if i == report_num:
                    logger.manip(f"{i}: Battle 5 drops equipment")
        ptr += 3
    
    result_array = [99,99,99]
    for i in range(3):
        report_val = report_num == i
        result, best = purifico_to_nea(
            parent_array=drop_count[i],
            ptr=ptr+i,
            report=report_val
        )
        if best == 99:
            result_array[i] == 99
        else:
            result_array[i] = best
    
    # Now, we want to prefer three-larvae results.
    if result_array[0] % 2 == 1:
        if result_array[1] % 2 == 1:
            if result_array[2] % 2 == 0:
                result_array[0] = 99
                result_array[1] = 99
        else:
            result_array[0] = 99
    logger.warning(f"Steal check: {result_array}")
    return result_array


def purifico_to_nea(
    parent_array = [],
    ptr = 3,
    stage=0,  # used to skip forward, reassess in Calm or after defender X.
    report=True
):
    # parent_array passes in enemies that will drop earlier, passed from earlier in the run.
    # ptr is our position on the RNG10 array. Needs to be pre-advanced to last check +3.
    if len(parent_array) == 0:
        results = [[],[]]
    else:
        results = [[*parent_array],[*parent_array]]
    test_array = memory.main.rng_10_array()
    
    chance = 60
    if stage == 0:  # Start of Via Purifico, no Larvae killed.
        # First larva
        if (test_array[ptr] & 0x7FFFFFFF) % 255 < chance:
            results[0].append("maze_larva")
            results[1].append("maze_larva")
            logger.debug("First larvae drops item.")
        ptr += 3
        # Second larva
        if (test_array[ptr] & 0x7FFFFFFF) % 255 < chance:
            results[0].append("maze_larva")
            results[1].append("maze_larva")
            logger.debug("Second larvae drops item.")
        ptr += 3
        
        # Two larvae path
        results[1].append("evrae_altana")
        #ptr+3
        #Ifrit
        #ptr+6
        #Valefor
        #ptr+9
        #Bahamut
        #ptr+12
        #ykt-63
        chance = 30
        if (test_array[ptr+12] & 0x7FFFFFFF) % 255 < chance:
            results[1].append("ykt-63")
            logger.debug("Robot 1 drops item")
        #ptr+15
        
        chance = 60
        # Third larvae path
        if (test_array[ptr] & 0x7FFFFFFF) % 255 < chance:
            results[0].append("maze_larva")
        #ptr+3
        results[0].append("evrae_altana")
        #ptr+6
        #Ifrit
        #ptr+9
        #Valefor
        #ptr+12
        #Bahamut
        #ptr+15
        
        ptr += 15
    
    if stage <= 1:  # Highbridge start
        chance = 30
        if stage == 1 and game_vars.get_rescue_count() <= 2:
            # YKT-63, alt to third larva
            if (test_array[ptr] & 0x7FFFFFFF) % 255 < chance:
                results[0].append("ykt-63")
                results[1].append("ykt-63")
                logger.debug("Robot 1 drops item (overlap from third larvae)")
            ptr += 3
        # YKT-63
        if (test_array[ptr] & 0x7FFFFFFF) % 255 < chance:
            results[0].append("ykt-63")
            results[1].append("ykt-63")
            logger.debug("Robot 2 drops item")
        ptr += 3
        results[0].append("seymour_natus")
        results[1].append("seymour_natus")
        ptr += 3
    
    # The rest of these, we can control in the Calm Lands.
    # No need to follow RNG10 through this logic.
    # Eight possible permutations.
    if stage <= 2:  # Start of calm lands, or before.
        for i in range(2):
            results.append(results[i] + ["defender_x"])
        for i in range(4):
            results.append(results[i] + ["yenke_ronso","biran_ronso"])
        for i in range(8):
            results[i] = results[i] + ["ghost"]
        
    elif stage == 3:
        for i in range(2):
            results[i] = results[i] + ["yenke_ronso","biran_ronso","ghost"]
            results[i] = results[i] + ["ghost"]
    # else stage 4 == after B&Y completed. No extra info needed.
    
    # Now to find results.
    preferable = []
    quality = 0
    preferred_result = [0,4,6,9]
    for i in range(len(results)):
        success,equip1,_ = rng_alignment_before_nea(enemies=results[i], report=report)  # here
        if success:
            quality += 1
            if equip1.owner() in preferred_result or equip1.owner_alt() in preferred_result:
                quality += 1
        preferable.append(quality)
        quality = 0
        
    best = len(results)-1
    for i in range(best,-1,-1):
        # Prefer overwriting with the lower value in each case.
        if preferable[i] >= preferable[best]:
            # No need to search for what does not exist.
            best = i
    
    if report:
        #logger.debug(f"Best result: {best}")
        #logger.debug(f"Best Array check: {best_array}")
        logger.warning(f"Preferable check: {preferable} | best = {best}")
        #logger.warning(results[best])
    
    # Returned values are in this order:
    # best_array (extra kills needed on each path)
    # best (the preferred path to success)
    if preferable[best] == 0:
        return (preferable, 99)
    else:
        return (preferable, best)
    
    

def party_size_rng_alignment(enemy_name) -> int:
    if enemy_name in [
        "evrae",
        "warrior_monk",
        "warrior_monk_2",
        "ykt-63",
        "yat-99"
    ]:
        return 6
    if enemy_name == "evrae_altana":
        return 3
    if enemy_name == "maze_larva":
        return 2
    return 7
        


def rng_alignment_before_nea(enemies, steals:int = 0, report:bool=False):
    ptr12 = 0
    ptr13 = 0
    advances = 0
    extras = 0
    #logger.warning(enemies)
    
    for i in range(len(enemies)):
        party_size = party_size_rng_alignment(enemies[i])
        #logger.warning(f"Checking drop for enemy {enemies[i]}")
        if enemies[i] == "epaaj":
            extras += 1
    
        equipment, advances = item_to_be_dropped(
            enemy = enemies[i],
            pre_advance_12 = ptr12,
            pre_advance_13 = ptr13,
            party_size = party_size
        )
        if equipment.equipment_type() == 0:
            e_type = "weapon"
        else:
            e_type = "armor"
        if enemies[i] in ["seymour_natus","maze_larva"]:
            # aka killed by Aeon
            e_owner = memory.main.name_from_number(equipment.owner_alt())
        else:
            e_owner = memory.main.name_from_number(equipment.owner())
        e_ab_count = len([i for i in equipment.abilities() if i != 255])
        #if report:
        #    logger.manip(f"Enemy {enemies[i]} drops {e_type} for {e_owner} with {e_ab_count} abilities.")
        condition = "without"
        condition2 = "without"
        if "defender_x" in enemies:
            condition = "with"
        if "yenke_ronso" in enemies:
            condition2 = "with"
        if enemies[i] == "ghost":
            #logger.warning("Found one!")
            #if report:
                #logger.manip(f"Ghost {e_type} drops NEA with {steals} steals and {extras} extras, {condition} X, {condition2} Ronso.")
                #logger.manip(f"Owner: {e_owner}, Type: {e_type}, {e_ab_count} - {equipment.abilities()}")
            if equipment.equipment_type() == 1 and equipment.has_ability(0x801D):
                return (True, equipment, extras)
            else:
                return (False, equipment, extras)
                
        ptr12 += 4
        ptr13 += advances
    #if report:
    #    logger.manip(f"No drop identified for this version: Owner: {e_owner}, Type: {e_type}, {equipment.abilities()}")
    return (False, equipment, extras)


def final_nea_check(with_ronso:bool = False):
    max_drop = 3
    ghost_array = ["ghost"]
    ronso_array = []
    epaaj_array = []
    if with_ronso:
        ronso_array = ["yenke_ronso","biran_ronso"]
    result_possible = False
    for i in range(max_drop+1):
        results = ronso_array + epaaj_array + ghost_array
        result_possible, _, _ = rng_alignment_before_nea(enemies=results, report=True)
        if result_possible:
            if len(ronso_array) == 0:
                check = "without"
            else:
                check = "with"
            logger.warning(f"===  Final check found with {i} extra Epaaj drops, {check} ronso first.  ===")
            return (result_possible, i)
        epaaj_array.append("epaaj")
    logger.warning(f"===  Final check NOT found!!!  ===")
    return (result_possible, 99)

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


def future_enemy_attack_damage(
    character: int = 0, 
    enemy: str = "spectral_keeper", 
    attack_index: int = 1, 
    report:bool = False
) -> int:
    # NOT WORKING
    pre_battle_advance = int(not memory.main.battle_active())
    index = 20 + character
    damage_array = memory.main.rng_array_from_index(index=index, array_len=(attack_index*2) + 3)
    array_pos = (attack_index*2) + 1 + pre_battle_advance

    damage_roll = (damage_array[array_pos] // 0xFFFFFFFF % 31) + 240
    if enemy == "spectral_keeper":
        base_damage_value = 24
    else:
        base_damage_value = 1
    if report:
        logger.manip(f"{enemy} base damage value: {base_damage_value}")
    damage_value = (base_damage_value * damage_roll) // 256
    if report:
        logger.manip(f"Future Attack {attack_index} will hit for damage {damage_value}")
    return damage_value


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


def hits_to_seed(hits_array):  # No longer accurate.
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
