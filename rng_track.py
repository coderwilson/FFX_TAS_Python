import csv
import json

import logs
import memory.main
import vars

# from tracker.data.formations import allFormations
from tracker.ffx_rng_tracker.data.monsters import MONSTERS

game_vars = vars.vars_handle()


def area_formations(area: str):
    f = open("tracker/data/formations.json")
    allFormations = json.load(f)
    f.close()
    if area in allFormations["random"].keys():
        return allFormations["random"][area]["formations"]
    elif area in allFormations["bosses"].keys():
        return allFormations["bosses"][area]["formation"]
    else:
        print("Key not found:", area)


def coming_battles(
    area: str = "kilika_woods", battle_count: int = 10, extraAdvances: int = 0
):
    formations = area_formations(area=area)
    advances = memory.main.rng_01_advances((battle_count * 2) + extraAdvances)
    if extraAdvances != 0:
        while extraAdvances != 0:
            del advances[0]
            extraAdvances -= 1
    battles = []
    for i in range(battle_count):
        nextValue = formations[(advances[(i * 2) + 1] & 0x7FFFFFFF) % len(formations)]
        battles.append(nextValue)
    return battles


def coming_battle_type(extra_advances: int = 0, initiative=False):
    advances = memory.main.rng_01_advances(2 + extra_advances)
    if extra_advances != 0:
        while extra_advances != 0:
            del advances[0]
            extra_advances -= 1
    battleType = (advances[2] & 0x7FFFFFFF) & 255
    if initiative:
        battleType -= 33

    if battleType < 32:
        return 1
    elif battleType < 255 - 32:
        return 0
    else:
        return 2


def singles_battles(
    area: str = "kilika_woods", battle_count: int = 10, extra_advances: int = 0
):
    formations = area_formations(area=area)
    advances = memory.main.rng_01_advances(battle_count + extra_advances)
    if extra_advances != 0:
        while extra_advances != 0:
            del advances[0]
            extra_advances -= 1
    battles = []
    for i in range(battle_count):
        nextValue = formations[(advances[i + 1] & 0x7FFFFFFF) % len(formations)]
        battles.append(nextValue)
    return battles


def drop_chance(enemy: str = "ghost"):
    return MONSTERS[enemy].equipment["drop_chance"]


def drop_slots(enemy: str = "ghost"):
    return MONSTERS[enemy].equipment["slots_range"]


def slot_mod(enemy: str = "ghost"):
    return MONSTERS[enemy].equipment["slots_modifier"]


def drop_ability_count(enemy: str = "ghost"):
    return MONSTERS[enemy].equipment["max_ability_rolls_range"]


def ability_mod(enemy: str = "ghost"):
    return MONSTERS[enemy].equipment["max_ability_rolls_modifier"]


def drop_ability_list(enemy: str = "ghost", equip_type: int = 0):
    if equip_type == 0:
        array = MONSTERS[enemy].equipment["ability_arrays"]["Tidus"]["Weapon"]
    else:
        array = MONSTERS[enemy].equipment["ability_arrays"]["Tidus"]["Armor"]
    retVal = []
    for i in range(len(array)):
        try:
            retVal.append(array[i].tas_id)
        except Exception:
            retVal.append(255)

    return retVal


def early_battle_count():
    with open("csv\\seed_battle_variance.csv", "r", newline="") as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            if int(row["Seed"]) == memory.main.rng_seed():
                return row


def track_drops(enemy: str = "ghost", battles: int = 20, extra_advances: int = 0):
    noAdvanceArray = []
    oneAdvanceArray = []
    twoAdvanceArray = []
    advances = (battles + 1) * 3
    randArray = memory.main.rng_10_array(array_len=advances + extra_advances)
    if extra_advances != 0:
        while extra_advances != 0:
            del randArray[0]
            extra_advances -= 1

    for i in range(len(randArray)):
        if i < 3:
            pass
        elif (randArray[i] & 0x7FFFFFFF) % 255 < drop_chance(enemy):
            if i % 3 == 0:
                noAdvanceArray.append(i / 3)
            elif i % 3 == 1:
                oneAdvanceArray.append((i - 1) / 3)
            else:
                twoAdvanceArray.append((i - 2) / 3)
    return [noAdvanceArray, oneAdvanceArray, twoAdvanceArray]


def item_to_be_dropped(
    enemy: str = "ghost",
    pre_advance_12: int = 0,
    pre_advance_13: int = 0,
    party_size: int = 7,
):
    testMode = False  # Doesn't functionally change, but prints more stuff.
    slotMod = slot_mod(enemy=enemy)
    abilityMod = ability_mod(enemy=enemy)

    if party_size == 2:
        partyChars = [0, 4]
    elif party_size == 3:
        partyChars = [0, 4, 6]
    elif party_size == 4:
        partyChars = [0, 1, 4, 5]
    elif party_size == 5:
        partyChars = [0, 1, 3, 4, 5]
    elif party_size == 6:
        partyChars = [0, 1, 2, 3, 4, 5]
    elif party_size == 7:
        partyChars = [0, 1, 2, 3, 4, 5, 6]
    else:
        partyChars = [0]

    advance12 = 4 + pre_advance_12
    testArray12 = memory.main.rng_12_array(advance12)
    del testArray12[0]
    if pre_advance_12 >= 1:
        while pre_advance_12 >= 1:
            del testArray12[0]
            pre_advance_12 -= 1

    # Assume killer is aeon
    user2 = partyChars[(testArray12[0] & 0x7FFFFFFF) % len(partyChars)]
    partyChars.append(9)
    partyChars.append(9)
    partyChars.append(9)
    # Assume user == killer
    user1 = partyChars[(testArray12[0] & 0x7FFFFFFF) % len(partyChars)]

    # Type
    equipType = (testArray12[1] & 0x7FFFFFFF) % 2

    # Slots
    baseSlots = (slotMod + ((testArray12[2] & 0x7FFFFFFF) & 7)) - 4
    slots = (baseSlots + ((baseSlots >> 31) & 7)) >> 2
    if slots == 0:
        slots = 1

    # Abilities
    baseMod = (abilityMod + ((testArray12[3] & 0x7FFFFFFF) & 7)) - 4
    abilityCount = (baseMod + ((baseMod >> 31) & 7)) >> 3
    if slots < abilityCount:
        abilityCount = slots

    # rng13 logic here, determine which ability goes where.
    newAbilities = ability_to_be_dropped(
        enemy=enemy, equip_type=equipType, slots=abilityCount, advances=pre_advance_13
    )
    abilityList = newAbilities[0]
    pre_advance_13 += newAbilities[1]
    if testMode:
        print("New Abilities: ", abilityList)

    finalItem = memory.main.Equipment(equip_num=0)
    finalItem.create_custom(
        eType=equipType,
        eOwner1=user1,
        eOwner2=user2,
        eSlots=slots,
        eAbilities=abilityList,
    )

    return finalItem, pre_advance_13


def ability_to_be_dropped(
    enemy: str = "ghost", equip_type: int = 0, slots: int = 1, advances: int = 0
):
    testMode = False  # Doesn't functionally change, but prints more stuff.
    outcomes = drop_ability_list(enemy=enemy, equip_type=equip_type)
    found = 0
    # if testMode:
    #    print("o: ", outcomes)
    if slots == 0:
        slots = 1
    filledSlots = [99] * slots
    # if testMode:
    #    print("fs: ", filledSlots)

    ptr = 0  # Pointer that indicates how many advances needed for this evaluation
    testArray = memory.main.rng_13_array(array_len=50 + advances)
    # if testMode:
    #    print("ta: ", testArray)

    # if outcomes[0]:
    #    filledSlots.append(outcomes[0])
    #    filledSlots.remove(99)
    if testMode:
        print("E: ", enemy, " - O: ", outcomes)

    while 99 in filledSlots and ptr < 50 + advances:
        # Increment to match the first (and subsequent) advance(s)
        try:
            ptr += 1
            if testMode:
                print("==================================")
                print("ptr: ", ptr)
                print("Try: ", testArray[ptr + advances])
            arrayPos = ((testArray[ptr + advances] & 0x7FFFFFFF) % 7) + 1
            if testMode:
                print("AP: ", arrayPos)
                print("Res: ", outcomes[arrayPos])
                print("==================================")
            if outcomes[arrayPos] in filledSlots:
                pass
            else:
                filledSlots.remove(99)
                filledSlots.append(int(outcomes[arrayPos]))
                found += 1
                if testMode:
                    print(filledSlots)
        except Exception as e:
            print("ERR: ", e)
    if testMode:
        print("FS: ", filledSlots)

    while 99 in filledSlots:
        filledSlots.remove(99)

    # Format so that we have four slots always.
    if len(filledSlots) < 4:
        while len(filledSlots) < 4:
            filledSlots.append(255)
    if testMode:
        print("FSfin: ", filledSlots)

    return [filledSlots, found]


def report_dropped_item(
    enemy: str,
    drop=memory.main.Equipment,
    pref_type: int = 99,
    pref_ability: int = 255,
    need_adv: int = 0,
    report=False,
):
    abiStr = str(pref_ability)
    pref_type
    report = True
    if pref_ability != 255 and abiStr not in drop.equipAbilities:
        report = False
    elif pref_type != 99 and pref_type != drop.equipType:
        print(pref_type)
        print(drop.equipType)
        report = False

    if report:
        logs.write_rng_track(
            "+Item drop off of:" + str(enemy) + "| advances:" + str(need_adv)
        )
        logs.write_rng_track("+Owner, char-killed (9 = killer):" + str(drop.equipOwner))
        logs.write_rng_track("+Owner, aeon-killed:" + str(drop.equipOwnerAlt))
        if drop.equipType == 0:
            logs.write_rng_track("+Type: Weapon")
        else:
            logs.write_rng_track("+Type: Armor")
        logs.write_rng_track("+Open Slots: " + str(drop.slots))
        logs.write_rng_track("+Abilities: " + str(drop.equipAbilities))
        logs.write_rng_track("===================")
        return True
    else:
        logs.write_rng_track(
            "-Undesirable item dropped by: "
            + str(enemy)
            + " | advances:"
            + str(need_adv)
        )
        logs.write_rng_track("-Owner, char-killed: " + str(drop.equipOwner))
        logs.write_rng_track("-Owner, aeon-killed: " + str(drop.equipOwnerAlt))
        if drop.equipType == 0:
            logs.write_rng_track("-Type: Weapon")
        else:
            logs.write_rng_track("-Type: Armor")
        logs.write_rng_track("-Open Slots: " + str(drop.slots))
        logs.write_rng_track("-Abilities: " + str(drop.equipAbilities))
        logs.write_rng_track("===================")
        return False


def t_strike_tracking(tros=False, report=False):
    return [0, 0, 0], [0, 0, 0]


def t_strike_tracking_not_working_yet(tros=False, report=False):
    if tros:
        advance01 = 0
        advance10 = 3  # Starts off with just the Tros kill advance.
    else:
        advance01 = 1
        advance10 = 9  # Starts off with two advances for pirhanas and one for Tros
    if report:
        logs.open_rng_track()
        logs.write_rng_track(memory.main.rng_10_array(array_len=80))
        logs.write_rng_track("#########################")
    advance12 = [0, 0, 0]  # Tros drops one item
    advance13 = [0, 0, 0]  # Tros item has no abilities
    thunderCount = [0, 0, 0]  # Count results per advance, for returning later.
    # Count only if Oblitz will drop a weapon for Tidus.
    oblitzWeap = [False] * 3
    # Increment only if we need to kill yellow element on a certain battle.
    killYellow = [0, 0, 0]
    battleVariance = early_battle_count()
    try:
        lagoonCount = int(battleVariance["Lagoon"])
        kilikaCount = int(battleVariance["Kilika"])
    except Exception:
        lagoonCount = 3
        kilikaCount = 6
    partySize = 4

    # Lagoon
    lagoonBattles = coming_battles(
        area="besaid_lagoon", battle_count=lagoonCount, extraAdvances=advance01
    )
    for i in range(len(lagoonBattles)):
        logs.write_rng_track("Lagoon battle:")
        logs.write_rng_track(str(lagoonBattles[i]))
        logs.write_rng_track(
            "Battle type: "
            + str(coming_battle_type(extra_advances=advance01 + (2 * i)))
        )
        if len(lagoonBattles[i]) == 2:
            advance10 += 6
        elif (
            len(lagoonBattles[i]) == 3
            and coming_battle_type(extra_advances=advance01 + (2 * i)) == 1
        ):
            advance10 += 9
        else:
            advance10 += 0
    advance01 += len(lagoonBattles) * 2

    logs.write_rng_track("===================")
    logs.write_rng_track("Looking ahead for thunder strike drops")

    # Besaid tutorials
    dropChances = track_drops(enemy="dingo", battles=1, extra_advances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = item_to_be_dropped(
            enemy="dingo",
            pre_advance_12=advance12[0],
            pre_advance_13=advance13[0],
            party_size=partySize,
        )
        advance12[0] += 4
        if report_dropped_item(
            enemy="dingo",
            drop=finalItem,
            pref_type=0,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = item_to_be_dropped(
            enemy="dingo",
            pre_advance_12=advance12[1],
            pre_advance_13=advance13[1],
            party_size=partySize,
        )
        advance12[1] += 4
        if report_dropped_item(
            enemy="dingo",
            drop=finalItem,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[1] += 1
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = item_to_be_dropped(
            enemy="dingo",
            pre_advance_12=advance12[2],
            pre_advance_13=advance13[2],
            party_size=partySize,
        )
        advance12[2] += 4
        if report_dropped_item(
            enemy="dingo",
            drop=finalItem,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[2] += 1
    advance10 += 3

    dropChances = track_drops(enemy="condor", battles=1, extra_advances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = item_to_be_dropped(
            enemy="condor",
            pre_advance_12=advance12[0],
            pre_advance_13=advance13[0],
            party_size=partySize,
        )
        advance12[0] += 4
        if report_dropped_item(
            enemy="condor",
            drop=finalItem,
            pref_type=0,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = item_to_be_dropped(
            enemy="condor",
            pre_advance_12=advance12[1],
            pre_advance_13=advance13[1],
            party_size=partySize,
        )
        advance12[1] += 4
        if report_dropped_item(
            enemy="condor",
            drop=finalItem,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[1] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[2] = item_to_be_dropped(
            enemy="condor",
            pre_advance_12=advance12[2],
            pre_advance_13=advance13[2],
            party_size=partySize,
        )
        advance12[2] += 4
        if report_dropped_item(
            enemy="condor",
            drop=finalItem,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[2] += 1
    advance10 += 3

    dropChances = track_drops(enemy="water_flan", battles=1, extra_advances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = item_to_be_dropped(
            enemy="water_flan",
            pre_advance_12=advance12[0],
            pre_advance_13=advance13[0],
            party_size=partySize,
        )
        report_dropped_item(
            enemy="water_flan",
            drop=finalItem,
            pref_type=0,
            pref_ability=0x8026,
            report=report,
        )
        advance12[0] += 4
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = item_to_be_dropped(
            enemy="water_flan",
            pre_advance_12=advance12[1],
            pre_advance_13=advance13[1],
            party_size=partySize,
        )
        report_dropped_item(
            enemy="water_flan",
            drop=finalItem,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        )
        advance12[1] += 4
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = item_to_be_dropped(
            enemy="water_flan",
            pre_advance_12=advance12[2],
            pre_advance_13=advance13[2],
            party_size=partySize,
        )
        report_dropped_item(
            enemy="water_flan",
            drop=finalItem,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        )
        advance12[2] += 4
    advance10 += 3

    # Kimahri drops something guaranteed.
    dropChances = track_drops(enemy="???", battles=1, extra_advances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = item_to_be_dropped(
            enemy="???",
            pre_advance_12=advance12[0],
            pre_advance_13=advance13[0],
            party_size=partySize,
        )
        report_dropped_item(
            enemy="???", drop=finalItem, pref_type=0, pref_ability=0x8026, report=report
        )
        advance12[0] += 4
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = item_to_be_dropped(
            enemy="???",
            pre_advance_12=advance12[1],
            pre_advance_13=advance13[1],
            party_size=partySize,
        )
        report_dropped_item(
            enemy="???",
            drop=finalItem,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        )
        advance12[1] += 4
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = item_to_be_dropped(
            enemy="???",
            pre_advance_12=advance12[2],
            pre_advance_13=advance13[2],
            party_size=partySize,
        )
        report_dropped_item(
            enemy="???",
            drop=finalItem,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        )
        advance12[2] += 4
    advance10 += 3

    dropChances = track_drops(enemy="garuda_3", battles=1, extra_advances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = item_to_be_dropped(
            enemy="garuda_3",
            pre_advance_12=advance12[0],
            pre_advance_13=advance13[0],
            party_size=partySize,
        )
        advance12[0] += 4
        if report_dropped_item(
            enemy="garuda_3",
            drop=finalItem,
            pref_type=0,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = item_to_be_dropped(
            enemy="garuda_3",
            pre_advance_12=advance12[1],
            pre_advance_13=advance13[1],
            party_size=partySize,
        )
        advance12[1] += 4
        if report_dropped_item(
            enemy="garuda_3",
            drop=finalItem,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[1] += 1
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = item_to_be_dropped(
            enemy="garuda_3",
            pre_advance_12=advance12[2],
            pre_advance_13=advance13[2],
            party_size=partySize,
        )
        advance12[2] += 4
        if report_dropped_item(
            enemy="garuda_3",
            drop=finalItem,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[2] += 1
    advance10 += 3

    dropChances = track_drops(enemy="dingo", battles=1, extra_advances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = item_to_be_dropped(
            enemy="dingo",
            pre_advance_12=advance12[0],
            pre_advance_13=advance13[0],
            party_size=partySize,
        )
        advance12[0] += 4
        if report_dropped_item(
            enemy="dingo",
            drop=finalItem,
            pref_type=0,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = item_to_be_dropped(
            enemy="dingo",
            pre_advance_12=advance12[1],
            pre_advance_13=advance13[1],
            party_size=partySize,
        )
        advance12[1] += 4
        if report_dropped_item(
            enemy="dingo",
            drop=finalItem,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[1] += 1
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = item_to_be_dropped(
            enemy="dingo",
            pre_advance_12=advance12[2],
            pre_advance_13=advance13[2],
            party_size=partySize,
        )
        advance12[2] += 4
        if report_dropped_item(
            enemy="dingo",
            drop=finalItem,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[2] += 1
    advance10 += 3

    dropChances = track_drops(enemy="condor", battles=1, extra_advances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = item_to_be_dropped(
            enemy="condor",
            pre_advance_12=advance12[0],
            pre_advance_13=advance13[0],
            party_size=partySize,
        )
        advance12[0] += 4
        if report_dropped_item(
            enemy="condor",
            drop=finalItem,
            pref_type=0,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = item_to_be_dropped(
            enemy="condor",
            pre_advance_12=advance12[1],
            pre_advance_13=advance13[1],
            party_size=partySize,
        )
        advance12[1] += 4
        if report_dropped_item(
            enemy="condor",
            drop=finalItem,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[1] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[2] = item_to_be_dropped(
            enemy="condor",
            pre_advance_12=advance12[2],
            pre_advance_13=advance13[2],
            party_size=partySize,
        )
        advance12[2] += 4
        if report_dropped_item(
            enemy="condor",
            drop=finalItem,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[2] += 1
    advance10 += 3

    dropChances = track_drops(enemy="water_flan", battles=1, extra_advances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = item_to_be_dropped(
            enemy="water_flan",
            pre_advance_12=advance12[0],
            pre_advance_13=advance13[0],
            party_size=partySize,
        )
        report_dropped_item(
            enemy="water_flan",
            drop=finalItem,
            pref_type=0,
            pref_ability=0x8026,
            report=report,
        )
        advance12[0] += 4
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = item_to_be_dropped(
            enemy="water_flan",
            pre_advance_12=advance12[1],
            pre_advance_13=advance13[1],
            party_size=partySize,
        )
        report_dropped_item(
            enemy="water_flan",
            drop=finalItem,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        )
        advance12[1] += 4
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = item_to_be_dropped(
            enemy="water_flan",
            pre_advance_12=advance12[2],
            pre_advance_13=advance13[2],
            party_size=partySize,
        )
        report_dropped_item(
            enemy="water_flan",
            drop=finalItem,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        )
        advance12[2] += 4
    advance10 += 3
    advance01 += 6

    partySize = 5
    # Sin's Fin
    dropChances = track_drops(enemy="sin", battles=1, extra_advances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = item_to_be_dropped(
            enemy="sin",
            pre_advance_12=advance12[0],
            pre_advance_13=advance13[0],
            party_size=partySize,
        )
        advance12[0] += 4
        if report_dropped_item(
            enemy="sin-fin",
            drop=finalItem,
            pref_type=0,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = item_to_be_dropped(
            enemy="sin",
            pre_advance_12=advance12[1],
            pre_advance_13=advance13[1],
            party_size=partySize,
        )
        advance12[1] += 4
        if report_dropped_item(
            enemy="sin-fin",
            drop=finalItem,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[1] += 1
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = item_to_be_dropped(
            enemy="sin",
            pre_advance_12=advance12[2],
            pre_advance_13=advance13[2],
            party_size=partySize,
        )
        advance12[2] += 4
        if report_dropped_item(
            enemy="sin-fin",
            drop=finalItem,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[2] += 1
    advance10 += 3
    advance01 += 1

    partySize = 2
    # Sinspawn Echuilles
    dropChances = track_drops(
        enemy="sinspawn_echuilles", battles=1, extra_advances=advance10
    )
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = item_to_be_dropped(
            enemy="sinspawn_echuilles",
            pre_advance_12=advance12[0],
            pre_advance_13=advance13[0],
            party_size=partySize,
        )
        advance12[0] += 4
        if report_dropped_item(
            enemy="sinspawn_echuilles",
            drop=finalItem,
            pref_type=0,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = item_to_be_dropped(
            enemy="sinspawn_echuilles",
            pre_advance_12=advance12[1],
            pre_advance_13=advance13[1],
            party_size=partySize,
        )
        advance12[1] += 4
        if report_dropped_item(
            enemy="sinspawn_echuilles",
            drop=finalItem,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[1] += 1
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = item_to_be_dropped(
            enemy="sinspawn_echuilles",
            pre_advance_12=advance12[2],
            pre_advance_13=advance13[2],
            party_size=partySize,
        )
        advance12[2] += 4
        if report_dropped_item(
            enemy="sinspawn_echuilles",
            drop=finalItem,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[2] += 1
    advance10 += 3
    advance01 += 1

    enemy = "ragora"
    partySize = 5
    # Lancet tutorial
    dropChances = track_drops(enemy=enemy, battles=1, extra_advances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance12[0],
            pre_advance_13=advance13[0],
            party_size=partySize,
        )
        advance12[0] += 4
        if report_dropped_item(
            enemy=enemy, drop=finalItem, pref_type=0, pref_ability=0x8026, report=report
        ):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance12[1],
            pre_advance_13=advance13[1],
            party_size=partySize,
        )
        advance12[1] += 4
        if report_dropped_item(
            enemy=enemy,
            drop=finalItem,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[1] += 1
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance12[2],
            pre_advance_13=advance13[2],
            party_size=partySize,
        )
        advance12[2] += 4
        if report_dropped_item(
            enemy=enemy,
            drop=finalItem,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8026,
            report=report,
        ):
            thunderCount[2] += 1
    advance10 += 3
    advance01 += 1

    partySize = 5
    # Kilika
    geneauxTrack = False
    kilika_battles = coming_battles(
        area="kilika_woods", battle_count=3, extraAdvances=advance01
    )
    logs.write_rng_track("Kilika battles:")
    import area.kilika as kilika

    bestBattle = kilika.select_best_of_two(kilika_battles)
    ragoraKills = [0, 0, 0]
    if "ragora" in bestBattle:
        for i in range(len(bestBattle)):
            if bestBattle[i] == "ragora":
                ragoraKills[0] += 1
                ragoraKills[1] += 1
                ragoraKills[2] += 1
    bestBattleComplete = [False, False, False]

    for bCount in range(kilikaCount):
        if bCount == 3 and not geneauxTrack:
            advance10 += 3  # Tentacles
            finalItem, advance13[0] = item_to_be_dropped(
                enemy="sinspawn_geneaux",
                pre_advance_12=advance12[0],
                pre_advance_13=advance13[0],
                party_size=partySize,
            )
            advance12[0] += 4
            report_dropped_item(
                enemy="geneaux",
                drop=finalItem,
                pref_type=0,
                pref_ability=0x8026,
                report=report,
            )
            finalItem, advance13[1] = item_to_be_dropped(
                enemy="sinspawn_geneaux",
                pre_advance_12=advance12[1],
                pre_advance_13=advance13[1],
                party_size=partySize,
            )
            advance12[1] += 4
            report_dropped_item(
                enemy="geneaux",
                drop=finalItem,
                pref_type=0,
                need_adv=1,
                pref_ability=0x8026,
                report=report,
            )
            finalItem, advance13[2] = item_to_be_dropped(
                enemy="sinspawn_geneaux",
                pre_advance_12=advance12[2],
                pre_advance_13=advance13[2],
                party_size=partySize,
            )
            advance12[2] += 4
            report_dropped_item(
                enemy="geneaux",
                drop=finalItem,
                pref_type=0,
                need_adv=2,
                pref_ability=0x8026,
                report=report,
            )

            advance01 += 1
            geneauxTrack = True

        battleFormations = coming_battles(
            area="kilika_woods", battle_count=1, extraAdvances=advance01
        )
        logs.write_rng_track(str(battleFormations))
        for x in range(len(battleFormations)):
            for i in range(len(battleFormations[x])):
                thisBattle = battleFormations[x]
                if thisBattle == ["ragora"] and ragoraKills[0] == 0:
                    pass
                else:
                    dropChances = track_drops(
                        enemy=thisBattle[i], battles=1, extra_advances=advance10
                    )
                    if len(dropChances[0]) >= 1:
                        finalItem, advance13[0] = item_to_be_dropped(
                            enemy=thisBattle[i],
                            pre_advance_12=advance12[0],
                            pre_advance_13=advance13[0],
                            party_size=partySize,
                        )
                        advance12[0] += 4
                        if thisBattle == "ragora":
                            ragoraKills[0] -= 1
                        elif thisBattle == "yellow_element":
                            if finalItem.equipType == 0:
                                if report_dropped_item(
                                    enemy=thisBattle[i],
                                    drop=finalItem,
                                    pref_type=0,
                                    pref_ability=0x8026,
                                    report=report,
                                ):
                                    thunderCount[0] += 1
                                    killYellow[0] = x
                            elif (
                                thisBattle[i] == bestBattle
                                and not bestBattleComplete[0]
                            ):
                                if report_dropped_item(
                                    enemy=thisBattle[i],
                                    drop=finalItem,
                                    pref_type=0,
                                    pref_ability=0x8026,
                                    report=report,
                                ):
                                    bestBattleComplete[0] = True
                            else:
                                advance12[0] -= 4
                        else:
                            if report_dropped_item(
                                enemy=thisBattle[i],
                                drop=finalItem,
                                pref_type=0,
                                need_adv=1,
                                pref_ability=0x8026,
                                report=report,
                            ):
                                thunderCount[0] += 1
                    if len(dropChances[1]) >= 1:
                        finalItem, advance13[1] = item_to_be_dropped(
                            enemy=thisBattle[i],
                            pre_advance_12=advance12[1],
                            pre_advance_13=advance13[1],
                            party_size=partySize,
                        )
                        advance12[1] += 4
                        if thisBattle == "ragora":
                            ragoraKills[1] -= 1
                        elif thisBattle == "yellow_element":
                            if finalItem.equipType == 0:
                                if report_dropped_item(
                                    enemy=thisBattle[i],
                                    drop=finalItem,
                                    pref_type=0,
                                    pref_ability=0x8026,
                                    report=report,
                                ):
                                    thunderCount[1] += 1
                                    killYellow[1] = x
                            elif (
                                thisBattle[i] == bestBattle
                                and not bestBattleComplete[1]
                            ):
                                if report_dropped_item(
                                    enemy=thisBattle[i],
                                    drop=finalItem,
                                    pref_type=0,
                                    pref_ability=0x8026,
                                    report=report,
                                ):
                                    bestBattleComplete[1] = True
                            else:
                                advance12[1] -= 4
                        else:
                            if report_dropped_item(
                                enemy=thisBattle[i],
                                drop=finalItem,
                                pref_type=0,
                                need_adv=1,
                                pref_ability=0x8026,
                                report=report,
                            ):
                                thunderCount[1] += 1
                    if len(dropChances[2]) >= 1:
                        finalItem, advance13[2] = item_to_be_dropped(
                            enemy=thisBattle[i],
                            pre_advance_12=advance12[2],
                            pre_advance_13=advance13[2],
                            party_size=partySize,
                        )
                        advance12[2] += 4
                        if thisBattle == "ragora":
                            ragoraKills[2] -= 1
                        elif thisBattle == "yellow_element":
                            if finalItem.equipType == 0:
                                if report_dropped_item(
                                    enemy=thisBattle[i],
                                    drop=finalItem,
                                    pref_type=0,
                                    pref_ability=0x8026,
                                    report=report,
                                ):
                                    thunderCount[2] += 1
                                    killYellow[2] = x
                            elif (
                                thisBattle[i] == bestBattle
                                and not bestBattleComplete[2]
                            ):
                                if report_dropped_item(
                                    enemy=thisBattle[i],
                                    drop=finalItem,
                                    pref_type=0,
                                    pref_ability=0x8026,
                                    report=report,
                                ):
                                    bestBattleComplete[2] = True
                            else:
                                advance12[2] -= 4
                        else:
                            if report_dropped_item(
                                enemy=thisBattle[i],
                                drop=finalItem,
                                pref_type=0,
                                need_adv=1,
                                pref_ability=0x8026,
                                report=report,
                            ):
                                thunderCount[2] += 1
                    advance10 += 3
            advance01 += 2

    partySize = 5
    # Workers
    battleFormations = coming_battles(
        area="machina_1", battle_count=1, extraAdvances=advance01
    )
    for x in range(len(battleFormations)):
        for i in range(len(battleFormations[x])):
            thisBattle = battleFormations[x]
            dropChances = track_drops(
                enemy=thisBattle, battles=1, extra_advances=advance10
            )
            if len(dropChances[0]) >= 1:
                if track_drops(enemy=thisBattle, battles=1, extra_advances=advance10):
                    finalItem, advance13[0] = item_to_be_dropped(
                        enemy=thisBattle,
                        pre_advance_12=advance12[0],
                        pre_advance_13=advance13[0],
                        party_size=partySize,
                    )
                    advance12[0] += 4
                    if report_dropped_item(
                        enemy=thisBattle,
                        drop=finalItem,
                        pref_type=0,
                        pref_ability=0x8026,
                        report=report,
                    ):
                        thunderCount[0] += 1
            if len(dropChances[1]) >= 1:
                if track_drops(enemy=thisBattle, battles=1, extra_advances=advance10):
                    finalItem, advance13[1] = item_to_be_dropped(
                        enemy=thisBattle,
                        pre_advance_12=advance12[1],
                        pre_advance_13=advance13[1],
                        party_size=partySize,
                    )
                    advance12[1] += 4
                    if report_dropped_item(
                        enemy=thisBattle,
                        drop=finalItem,
                        pref_type=0,
                        need_adv=1,
                        pref_ability=0x8026,
                        report=report,
                    ):
                        thunderCount[1] += 1
            if len(dropChances[2]) >= 1:
                if track_drops(enemy=thisBattle, battles=1, extra_advances=advance10):
                    finalItem, advance13[2] = item_to_be_dropped(
                        enemy=thisBattle,
                        pre_advance_12=advance12[2],
                        pre_advance_13=advance13[2],
                        party_size=partySize,
                    )
                    advance12[2] += 4
                    if report_dropped_item(
                        enemy=thisBattle,
                        drop=finalItem,
                        pref_type=0,
                        need_adv=2,
                        pref_ability=0x8026,
                        report=report,
                    ):
                        thunderCount[2] += 1
            advance10 += 3
        advance01 += 1
    battleFormations = coming_battles(
        area="machina_2", battle_count=1, extraAdvances=advance01
    )
    for x in range(len(battleFormations)):
        for i in range(len(battleFormations[x])):
            thisBattle = battleFormations[x]
            dropChances = track_drops(
                enemy=thisBattle, battles=1, extra_advances=advance10
            )
            if len(dropChances[0]) >= 1:
                if track_drops(enemy=thisBattle, battles=1, extra_advances=advance10):
                    finalItem, advance13[0] = item_to_be_dropped(
                        enemy=thisBattle,
                        pre_advance_12=advance12[0],
                        pre_advance_13=advance13[0],
                        party_size=partySize,
                    )
                    advance12[0] += 4
                    if report_dropped_item(
                        enemy=thisBattle,
                        drop=finalItem,
                        pref_type=0,
                        pref_ability=0x8026,
                        report=report,
                    ):
                        thunderCount[0] += 1
            if len(dropChances[1]) >= 1:
                if track_drops(enemy=thisBattle, battles=1, extra_advances=advance10):
                    finalItem, advance13[1] = item_to_be_dropped(
                        enemy=thisBattle,
                        pre_advance_12=advance12[1],
                        pre_advance_13=advance13[1],
                        party_size=partySize,
                    )
                    advance12[1] += 4
                    if report_dropped_item(
                        enemy=thisBattle,
                        drop=finalItem,
                        pref_type=0,
                        need_adv=1,
                        pref_ability=0x8026,
                        report=report,
                    ):
                        thunderCount[1] += 1
            if len(dropChances[2]) >= 1:
                if track_drops(enemy=thisBattle, battles=1, extra_advances=advance10):
                    finalItem, advance13[2] = item_to_be_dropped(
                        enemy=thisBattle,
                        pre_advance_12=advance12[2],
                        pre_advance_13=advance13[2],
                        party_size=partySize,
                    )
                    advance12[2] += 4
                    if report_dropped_item(
                        enemy=thisBattle,
                        drop=finalItem,
                        pref_type=0,
                        need_adv=2,
                        pref_ability=0x8026,
                        report=report,
                    ):
                        thunderCount[2] += 1
            advance10 += 3
        advance01 += 1
    battleFormations = coming_battles(
        area="machina_3", battle_count=1, extraAdvances=advance01
    )
    for x in range(len(battleFormations)):
        for i in range(len(battleFormations[x])):
            thisBattle = battleFormations[x]
            dropChances = track_drops(
                enemy=thisBattle, battles=1, extra_advances=advance10
            )
            if len(dropChances[0]) >= 1:
                if track_drops(enemy=thisBattle, battles=1, extra_advances=advance10):
                    finalItem, advance13[0] = item_to_be_dropped(
                        enemy=thisBattle,
                        pre_advance_12=advance12[0],
                        pre_advance_13=advance13[0],
                        party_size=partySize,
                    )
                    advance12[0] += 4
                    if report_dropped_item(
                        enemy=thisBattle,
                        drop=finalItem,
                        pref_type=0,
                        pref_ability=0x8026,
                        report=report,
                    ):
                        thunderCount[0] += 1
            if len(dropChances[1]) >= 1:
                if track_drops(enemy=thisBattle, battles=1, extra_advances=advance10):
                    finalItem, advance13[1] = item_to_be_dropped(
                        enemy=thisBattle,
                        pre_advance_12=advance12[1],
                        pre_advance_13=advance13[1],
                        party_size=partySize,
                    )
                    advance12[1] += 4
                    if report_dropped_item(
                        enemy=thisBattle,
                        drop=finalItem,
                        pref_type=0,
                        need_adv=1,
                        pref_ability=0x8026,
                        report=report,
                    ):
                        thunderCount[1] += 1
            if len(dropChances[2]) >= 1:
                if track_drops(enemy=thisBattle, battles=1, extra_advances=advance10):
                    finalItem, advance13[2] = item_to_be_dropped(
                        enemy=thisBattle,
                        pre_advance_12=advance12[2],
                        pre_advance_13=advance13[2],
                        party_size=partySize,
                    )
                    advance12[2] += 4
                    if report_dropped_item(
                        enemy=thisBattle,
                        drop=finalItem,
                        pref_type=0,
                        need_adv=2,
                        pref_ability=0x8026,
                        report=report,
                    ):
                        thunderCount[2] += 1
            advance10 += 3
        advance01 += 1

    # Finally, Oblitz is guaranteed to drop an item.
    finalItem, advance13[0] = item_to_be_dropped(
        enemy="oblitzerator",
        pre_advance_12=advance12[0],
        pre_advance_13=advance13[0],
        party_size=partySize,
    )
    if report_dropped_item(
        enemy="Oblitzerator",
        drop=finalItem,
        pref_type=0,
        pref_ability=0x8026,
        report=report,
    ):
        thunderCount[0] += 1
        oblitzWeap[0] = True
    finalItem, advance13[1] = item_to_be_dropped(
        enemy="oblitzerator",
        pre_advance_12=advance12[1],
        pre_advance_13=advance13[1],
        party_size=partySize,
    )
    if report_dropped_item(
        enemy="Oblitzerator",
        drop=finalItem,
        pref_type=0,
        need_adv=1,
        pref_ability=0x8026,
        report=report,
    ):
        thunderCount[1] += 1
        oblitzWeap[1] = True
    finalItem, advance13[2] = item_to_be_dropped(
        enemy="oblitzerator",
        pre_advance_12=advance12[2],
        pre_advance_13=advance13[2],
        party_size=partySize,
    )
    if report_dropped_item(
        enemy="Oblitzerator",
        drop=finalItem,
        pref_type=0,
        need_adv=2,
        pref_ability=0x8026,
        report=report,
    ):
        thunderCount[2] += 1
        oblitzWeap[2] = True
    advance12[0] += 4
    advance10 += 3

    logs.write_rng_track("End: thunder strike drops")
    logs.write_rng_track("===================")
    logs.write_rng_track("The following values are per advance.")
    logs.write_rng_track("Drops possible:" + str(thunderCount))
    logs.write_rng_track("Weapon drops on Oblitzerator:" + str(oblitzWeap))
    logs.write_rng_track("Kill Yellow ele on Kilika battles:" + str(killYellow))
    return thunderCount, killYellow


def decide_skip_zan_luck() -> bool:
    # This function tracks if we need to pick up the luck and fortune spheres in Zanarkand.
    # This will track through from Yunalesca to BFA, the two fights with ~4% chance to miss.
    # False == there will be a miss. True == no miss.
    extraXP = 0  # where is the variable for this? Somewhere in vars file? This is if we need to kill something in Dome for XP...
    bahamutLuck = 17
    keeperCrit = memory.main.future_attack_will_crit(
        character=7, char_luck=bahamutLuck, enemy_luck=20, attack_index=extraXP
    )
    arm1Crit = False
    arm2Crit = False
    faceCrit = False

    attackCount = extraXP
    if keeperCrit:
        print("### Expecting crit on SK")
        attackCount += 1
    else:
        attackCount += 2

    # Now to test the Yunalesca fight. Crits do not matter here, only hit chance.
    for i in range(3):
        print("### YL attack num", i, "|", attackCount)
        if not future_attack_hit(
            character=7, enemy="yunalesca", attack_index=attackCount
        ):
            print("### Miss on Yunalesca, attack number", i)
            return False
        attackCount += 1
    if game_vars.nemesis():  # BFA miss does not factor in for Nemesis route.
        return True

    arm1Crit = memory.main.future_attack_will_crit(
        character=7, char_luck=bahamutLuck, enemy_luck=15, attack_index=attackCount
    )
    if arm1Crit:
        print("### Expecting crit on Arm 1")
        attackCount += 1
    else:
        attackCount += 2
    arm2Crit = memory.main.future_attack_will_crit(
        character=7, char_luck=bahamutLuck, enemy_luck=15, attack_index=attackCount
    )
    if arm2Crit:
        print("### Expecting crit on Arm 2")
        attackCount += 1
    else:
        attackCount += 2
    attackCount += 1  # Core is always one attack
    faceCrit = memory.main.future_attack_will_crit(
        character=7, char_luck=bahamutLuck, enemy_luck=15, attack_index=attackCount
    )
    if not faceCrit:
        faceCrit = memory.main.future_attack_will_crit(
            character=7,
            char_luck=bahamutLuck,
            enemy_luck=15,
            attack_index=attackCount + 1,
        )
    if faceCrit:
        print("### Expecting crit on Face")
        attackCount += 2
    else:
        attackCount += 3
    if not future_attack_hit(
        character=7, enemy="seymour_flux", attack_index=attackCount
    ):
        print("### Miss on Omnis")
        return False
    attackCount += 1  # One attack on Seymour
    for i in range(3):
        print("### BFA attack num ", i, " | ", attackCount)
        if not future_attack_hit(character=7, enemy="bfa", attack_index=attackCount):
            print("### Miss on BFA, attack number", i)
            return False
        attackCount += 1
    print("### No misses registered. Should be good to skip Luck/Fortune chests.")
    return True


def zombie_track(report=False):
    advance01 = 0
    advance10 = 0
    advance12 = [0] * 3
    advance13 = [0] * 3
    zombie_results = [99] * 3
    partySize = 7

    # "sanctuary_keeper"
    # Check random encounters for best charge, plan for 1 encounter, 1 death if possible to charge.
    # "spectral_keeper"
    # "yunalesca"

    enemy = "sanctuary_keeper"
    dropChances = track_drops(enemy=enemy, battles=1, extra_advances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance12[0],
            pre_advance_13=advance13[0],
            party_size=partySize,
        )
        advance12[0] += 4
        report_dropped_item(
            enemy=enemy, drop=finalItem, pref_type=0, pref_ability=0x8032, report=report
        )
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance12[1],
            pre_advance_13=advance13[1],
            party_size=partySize,
        )
        advance12[1] += 4
        report_dropped_item(
            enemy=enemy,
            drop=finalItem,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8032,
            report=report,
        )
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance12[2],
            pre_advance_13=advance13[2],
            party_size=partySize,
        )
        advance12[2] += 4
        report_dropped_item(
            enemy=enemy,
            drop=finalItem,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8032,
            report=report,
        )
    advance10 += 3
    advance01 += 1

    import area.zanarkand as zanarkand

    zanarkand.decide_nea(bonus_advance=1)
    # One death expected to recharge Rikku. No drops expected.
    if game_vars.get_nea_zone() in [1, 2]:
        advance10 += 3
        advance01 += 1

    enemy = "spectral_keeper"
    dropChances = track_drops(enemy=enemy, battles=1, extra_advances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance12[0],
            pre_advance_13=advance13[0],
            party_size=partySize,
        )
        advance12[0] += 4
        report_dropped_item(
            enemy=enemy, drop=finalItem, pref_type=0, pref_ability=0x8032, report=report
        )
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance12[1],
            pre_advance_13=advance13[1],
            party_size=partySize,
        )
        advance12[1] += 4
        report_dropped_item(
            enemy=enemy,
            drop=finalItem,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8032,
            report=report,
        )
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance12[2],
            pre_advance_13=advance13[2],
            party_size=partySize,
        )
        advance12[2] += 4
        report_dropped_item(
            enemy=enemy,
            drop=finalItem,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8032,
            report=report,
        )
    advance10 += 3
    advance01 += 1

    enemy = "yunalesca"
    dropChances = track_drops(enemy=enemy, battles=1, extra_advances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance12[0],
            pre_advance_13=advance13[0],
            party_size=partySize,
        )
        advance12[0] += 4
        if report_dropped_item(
            enemy=enemy, drop=finalItem, pref_type=0, pref_ability=0x8032, report=report
        ):
            zombie_results[0] = finalItem.equipOwnerAlt
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance12[1],
            pre_advance_13=advance13[1],
            party_size=partySize,
        )
        advance12[1] += 4
        if report_dropped_item(
            enemy=enemy,
            drop=finalItem,
            pref_type=0,
            need_adv=1,
            pref_ability=0x8032,
            report=report,
        ):
            zombie_results[1] = finalItem.equipOwnerAlt
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = item_to_be_dropped(
            enemy=enemy,
            pre_advance_12=advance12[2],
            pre_advance_13=advance13[2],
            party_size=partySize,
        )
        advance12[2] += 4
        if report_dropped_item(
            enemy=enemy,
            drop=finalItem,
            pref_type=0,
            need_adv=2,
            pref_ability=0x8032,
            report=report,
        ):
            zombie_results[2] = finalItem.equipOwnerAlt
    advance10 += 3
    advance01 += 1

    return zombie_results


def nea_track():
    preAdvance12 = 0
    preAdvance13 = 0

    totalAdvancePreX = 999
    totalAdvancePostX = 999
    enemy = "defender_x"

    # If already aligned for NEA, we want X to drop nothing.
    nextItem, preAdvance13 = item_to_be_dropped(enemy="ghost")
    if nextItem.equipment_type() == 1 and nextItem.has_ability(0x801D):
        totalAdvancePostX = 0
    while totalAdvancePreX == 999 or totalAdvancePostX == 999 and preAdvance12 < 100:
        preAdvance12 += 4
        nextItem, preAdvance13 = item_to_be_dropped(
            enemy="ghost", pre_advance_12=preAdvance12, pre_advance_13=preAdvance13
        )
        if nextItem.equipment_type() == 1 and 0x801D in nextItem.abilities():
            if totalAdvancePostX == 999:
                totalAdvancePostX = int(preAdvance12 / 4)
            if totalAdvancePreX == 999:
                totalAdvancePreX = int((preAdvance12 / 4) - 1)
    # print("/// Pre-X: ", totalAdvancePreX, " /// Post-X", totalAdvancePostX)
    return totalAdvancePreX, totalAdvancePostX


def print_manip_info():
    preX, postX = nea_track()
    print("--------------------------")
    print("Upcoming RNGs:")
    print("Next, before X:", preX, "| Next, after X: ", postX)
    print(
        "RNG10:",
        memory.main.next_chance_rng_10(),
        "| Pre Defender X: ",
        memory.main.next_chance_rng_10_calm(),
    )
    print("--------------------------")


def next_action_escape(character: int = 0):
    index = 20 + character
    escapeRoll = (
        memory.main.s32(memory.main.rng_array_from_index(index=index, array_len=1)[1])
        & 255
    )
    return escapeRoll < 191


def next_action_hit(character: int = 0, enemy: str = "anima"):
    return future_attack_hit(character=character, enemy=enemy)


def future_attack_hit(character: int = 0, enemy: str = "anima", attack_index: int = 0):
    # print("=========================")
    # print("Checking hit chance - character:", character)
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
        # print("Enemy luck: ", target_luck)
        target_evasion = MONSTERS[enemy].stats["Evasion"]
        # print("Enemy evasion:", target_evasion)

    # Unused, but technically part of the formula
    aims = 0
    target_reflexes = 0

    accuracyIndex = ((accuracy * 2 * 0x66666667) // 0xFFFFFFFF) // 2
    hit_chance_index = accuracyIndex - target_evasion + 10
    if hit_chance_index < 0:
        hit_chance_index = 0
    elif hit_chance_index > 8:
        hit_chance_index = 8
    base_hit_chance = hit_chance_table(hit_chance_index)

    hit_rng = (
        memory.main.rng_array_from_index(index=index, array_len=attack_index + 3)[
            attack_index + 1
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
    filepath = "json_ai_files\\oblitz_results.json"
    with open(filepath, "r") as fp:
        rngValues = json.load(fp)
    return rngValues


def save_oblitz_history(rng_vals):
    writing = dict(rng_vals)
    filepath = "json_ai_files\\oblitz_results.json"
    with open(filepath, "w") as fp:
        json.dump(writing, fp, indent=4)


def record_blitz_results_tyton(duration, test_mode=False):
    records = oblitz_history()
    if test_mode:
        seed = "31"
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
            ):
                return

    records[seed][sub_key]["duration"] = duration
    records[seed][sub_key]["victory"] = victory
    save_oblitz_history(records)


def record_blitz_results(duration, test_mode=False):
    filepath = "json_ai_files\\oblitz_results.json"
    records = oblitz_history()
    print("========================")
    if test_mode:
        newVal = {31: {9999: {"duration": duration, "victory": False}}}
        if str(31) in records.keys():
            print(newVal[31].keys())
            if 9999 in newVal[31].keys():
                records["31"]["9999"]["victory"] = True
                records["31"]["9999"]["duration"] = duration
            else:
                records["31"].update(newVal[31])
        else:
            records.update(newVal)
    else:
        newVal = {
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
                        > records[str(memory.main.rng_seed())][
                            game_vars.oblitz_rng_check()
                        ]["duration"]
                    ):
                        records[str(memory.main.rng_seed())][
                            game_vars.oblitz_rng_check()
                        ]["victory"] = game_vars.get_blitz_win()
                        records[str(memory.main.rng_seed())][
                            game_vars.oblitz_rng_check()
                        ]["duration"] = duration
            else:
                records[str(memory.main.rng_seed())].update(
                    newVal[memory.main.rng_seed()]
                )
        else:
            records.update(newVal)
    print(newVal)

    print("========================")
    print(records)

    with open(filepath, "w") as fp:
        json.dump(records, fp, indent=4)


def hits_to_seed(hits_array: int):
    with open("csv\\hits_to_seed.csv", "r", newline="") as csvFile:
        reader = csv.DictReader(csvFile)
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
