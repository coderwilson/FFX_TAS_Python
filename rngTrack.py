import memory.main
import csv
# from tracker.data.formations import allFormations
from tracker.ffx_rng_tracker.data.monsters import MONSTERS
import json
import logs
import vars
gameVars = vars.varsHandle()


def areaFormations(area: str):
    f = open('tracker/data/formations.json')
    allFormations = json.load(f)
    f.close()
    if area in allFormations["random"].keys():
        return allFormations["random"][area]["formations"]
    elif area in allFormations["bosses"].keys():
        return allFormations["bosses"][area]["formation"]
    else:
        print("Key not found:", area)


def comingBattles(area: str = "kilika_woods", battleCount: int = 10, extraAdvances: int = 0):
    formations = areaFormations(area=area)
    advances = memory.main.rng01Advances((battleCount * 2) + extraAdvances)
    if extraAdvances != 0:
        while extraAdvances != 0:
            del advances[0]
            extraAdvances -= 1
    battles = []
    for i in range(battleCount):
        nextValue = formations[(
            advances[(i * 2) + 1] & 0x7fffffff) % len(formations)]
        battles.append(nextValue)
    return battles


def comingBattleType(extraAdvances: int = 0, initiative=False):
    advances = memory.main.rng01Advances(2 + extraAdvances)
    if extraAdvances != 0:
        while extraAdvances != 0:
            del advances[0]
            extraAdvances -= 1
    battleType = (advances[2] & 0x7fffffff) & 255
    if initiative:
        battleType -= 33

    if battleType < 32:
        return 1
    elif battleType < 255 - 32:
        return 0
    else:
        return 2


def singlesBattles(area: str = "kilika_woods", battleCount: int = 10, extraAdvances: int = 0):
    formations = areaFormations(area=area)
    advances = memory.main.rng01Advances((battleCount) + extraAdvances)
    if extraAdvances != 0:
        while extraAdvances != 0:
            del advances[0]
            extraAdvances -= 1
    battles = []
    for i in range(battleCount):
        nextValue = formations[(advances[i + 1] & 0x7fffffff) % len(formations)]
        battles.append(nextValue)
    return battles


def dropChance(enemy: str = 'ghost'):
    return MONSTERS[enemy].equipment['drop_chance']


def dropSlots(enemy: str = 'ghost'):
    return MONSTERS[enemy].equipment['slots_range']


def SlotMod(enemy: str = 'ghost'):
    return MONSTERS[enemy].equipment['slots_modifier']


def dropAbilityCount(enemy: str = 'ghost'):
    return MONSTERS[enemy].equipment['max_ability_rolls_range']


def AbilityMod(enemy: str = 'ghost'):
    return MONSTERS[enemy].equipment['max_ability_rolls_modifier']


def dropAbilityList(enemy: str = 'ghost', equipType: int = 0):
    if equipType == 0:
        array = MONSTERS[enemy].equipment['ability_arrays']['Tidus']['Weapon']
    else:
        array = MONSTERS[enemy].equipment['ability_arrays']['Tidus']['Armor']
    retVal = []
    for i in range(len(array)):
        try:
            retVal.append(array[i].tas_id)
        except Exception:
            retVal.append(255)

    return retVal


def earlyBattleCount():
    with open('csv\\Seed_Battle_Variance.csv', 'r', newline='') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            if int(row['Seed']) == memory.main.rngSeed():
                return row


def trackDrops(enemy: str = 'ghost', battles: int = 20, extraAdvances: int = 0):
    noAdvanceArray = []
    oneAdvanceArray = []
    twoAdvanceArray = []
    advances = (battles + 1) * 3
    randArray = memory.main.rng10Array(arrayLen=advances + extraAdvances)
    if extraAdvances != 0:
        while extraAdvances != 0:
            del randArray[0]
            extraAdvances -= 1

    for i in range(len(randArray)):
        if i < 3:
            pass
        elif (randArray[i] & 0x7fffffff) % 255 < dropChance(enemy):
            if i % 3 == 0:
                noAdvanceArray.append(i / 3)
            elif i % 3 == 1:
                oneAdvanceArray.append((i - 1) / 3)
            else:
                twoAdvanceArray.append((i - 2) / 3)
    return [noAdvanceArray, oneAdvanceArray, twoAdvanceArray]


def itemToBeDropped(enemy: str = 'ghost', preAdvance12: int = 0, preAdvance13: int = 0, partySize: int = 7):
    testMode = False # Doesn't functionally change, but prints more stuff.
    slotMod = SlotMod(enemy=enemy)
    abilityMod = AbilityMod(enemy=enemy)

    if partySize == 2:
        partyChars = [0, 4]
    elif partySize == 3:
        partyChars = [0, 4, 6]
    elif partySize == 4:
        partyChars = [0, 1, 4, 5]
    elif partySize == 5:
        partyChars = [0, 1, 3, 4, 5]
    elif partySize == 6:
        partyChars = [0, 1, 2, 3, 4, 5]
    elif partySize == 7:
        partyChars = [0, 1, 2, 3, 4, 5, 6]
    else:
        partyChars = [0]

    advance12 = 4 + preAdvance12
    testArray12 = memory.main.rng12Array(advance12)
    del testArray12[0]
    if preAdvance12 >= 1:
        while preAdvance12 >= 1:
            del testArray12[0]
            preAdvance12 -= 1

    # Assume killer is aeon
    user2 = partyChars[(testArray12[0] & 0x7fffffff) % len(partyChars)]
    partyChars.append(9)
    partyChars.append(9)
    partyChars.append(9)
    # Assume user == killer
    user1 = partyChars[(testArray12[0] & 0x7fffffff) % len(partyChars)]

    # Type
    equipType = (testArray12[1] & 0x7fffffff) % 2

    # Slots
    baseSlots = (slotMod + ((testArray12[2] & 0x7fffffff) & 7)) - 4
    slots = (baseSlots + ((baseSlots >> 31) & 7)) >> 2
    if slots == 0:
        slots = 1

    # Abilities
    baseMod = (abilityMod + ((testArray12[3] & 0x7fffffff) & 7)) - 4
    abilityCount = (baseMod + ((baseMod >> 31) & 7)) >> 3
    if slots < abilityCount:
        abilityCount = slots

    # rng13 logic here, determine which ability goes where.
    newAbilities = abilityToBeDropped(
        enemy=enemy, equipType=equipType, slots=abilityCount, advances=preAdvance13)
    abilityList = newAbilities[0]
    preAdvance13 += newAbilities[1]
    if testMode:
        print("New Abilities: ", abilityList)

    finalItem = memory.main.equipment(equipNum=0)
    finalItem.createCustom(eType=equipType, eOwner1=user1,
                           eOwner2=user2, eSlots=slots, eAbilities=abilityList)

    return finalItem, preAdvance13


def abilityToBeDropped(enemy: str = 'ghost', equipType: int = 0, slots: int = 1, advances: int = 0):
    testMode = False # Doesn't functionally change, but prints more stuff.
    outcomes = dropAbilityList(enemy=enemy, equipType=equipType)
    found=0
    #if testMode:
    #    print("o: ", outcomes)
    if slots == 0:
        slots = 1
    filledSlots = [99] * slots
    #if testMode:
    #    print("fs: ", filledSlots)

    ptr = 0  # Pointer that indicates how many advances needed for this evaluation
    testArray = memory.main.rng13Array(arrayLen=50 + advances)
    #if testMode:
    #    print("ta: ", testArray)

    #if outcomes[0]:
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
                print("Try: ", testArray[ptr+advances])
            arrayPos = ((testArray[ptr+advances] & 0x7fffffff) % 7) + 1
            if testMode:
                print("AP: ", arrayPos)
                print("Res: ", outcomes[arrayPos])
                print("==================================")
            if outcomes[arrayPos] in filledSlots:
                pass
            else:
                filledSlots.remove(99)
                filledSlots.append(
                    int(outcomes[arrayPos]))
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


def reportDroppedItem(enemy: str, drop=memory.main.equipment, prefType: int = 99, prefAbility: int = 255, needAdv: int = 0, report=False):
    abiStr = str(prefAbility)
    prefType
    report = True
    if prefAbility != 255 and abiStr not in drop.equipAbilities:
        report = False
    elif prefType != 99 and prefType != drop.equipType:
        print(prefType)
        print(drop.equipType)
        report = False

    if report:
        logs.writeRNGTrack("+Item drop off of:" + str(enemy) + "| advances:" + str(needAdv))
        logs.writeRNGTrack("+Owner, char-killed (9 = killer):" + str(drop.equipOwner))
        logs.writeRNGTrack("+Owner, aeon-killed:" + str(drop.equipOwnerAlt))
        if drop.equipType == 0:
            logs.writeRNGTrack("+Type: Weapon")
        else:
            logs.writeRNGTrack("+Type: Armor")
        logs.writeRNGTrack("+Open Slots: " + str(drop.slots))
        logs.writeRNGTrack("+Abilities: " + str(drop.equipAbilities))
        logs.writeRNGTrack("===================")
        return True
    else:
        logs.writeRNGTrack(
            "-Undesirable item dropped by: " + str(enemy) + " | advances:" + str(needAdv))
        logs.writeRNGTrack("-Owner, char-killed: " + str(drop.equipOwner))
        logs.writeRNGTrack("-Owner, aeon-killed: " + str(drop.equipOwnerAlt))
        if drop.equipType == 0:
            logs.writeRNGTrack("-Type: Weapon")
        else:
            logs.writeRNGTrack("-Type: Armor")
        logs.writeRNGTrack("-Open Slots: " + str(drop.slots))
        logs.writeRNGTrack("-Abilities: " + str(drop.equipAbilities))
        logs.writeRNGTrack("===================")
        return False


def tStrikeTracking(tros=False, report=False):
    return [0, 0, 0], [0, 0, 0]


def tStrikeTracking_notWorkingYet(tros=False, report=False):
    if tros:
        advance01 = 0
        advance10 = 3  # Starts off with just the Tros kill advance.
    else:
        advance01 = 1
        advance10 = 9  # Starts off with two advances for pirhanas and one for Tros
    if report:
        logs.openRNGTrack()
        logs.writeRNGTrack(memory.main.rng10Array(arrayLen=80))
        logs.writeRNGTrack("#########################")
    advance12 = [0, 0, 0]  # Tros drops one item
    advance13 = [0, 0, 0]  # Tros item has no abilities
    thunderCount = [0, 0, 0]  # Count results per advance, for returning later.
    # Count only if Oblitz will drop a weapon for Tidus.
    oblitzWeap = [False] * 3
    # Increment only if we need to kill yellow element on a certain battle.
    killYellow = [0, 0, 0]
    battleVariance = earlyBattleCount()
    try:
        lagoonCount = int(battleVariance['Lagoon'])
        kilikaCount = int(battleVariance['Kilika'])
    except Exception:
        lagoonCount = 3
        kilikaCount = 6
    partySize = 4

    # Lagoon
    lagoonBattles = comingBattles(
        area="besaid_lagoon", battleCount=lagoonCount, extraAdvances=advance01)
    for i in range(len(lagoonBattles)):
        logs.writeRNGTrack("Lagoon battle:")
        logs.writeRNGTrack(str(lagoonBattles[i]))
        logs.writeRNGTrack(
            "Battle type: " + str(comingBattleType(extraAdvances=advance01 + (2 * i))))
        if len(lagoonBattles[i]) == 2:
            advance10 += 6
        elif len(lagoonBattles[i]) == 3 and comingBattleType(extraAdvances=advance01 + (2 * i)) == 1:
            advance10 += 9
        else:
            advance10 += 0
    advance01 += len(lagoonBattles) * 2

    logs.writeRNGTrack("===================")
    logs.writeRNGTrack("Looking ahead for thunder strike drops")

    # Besaid tutorials
    dropChances = trackDrops(enemy="dingo", battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(
            enemy="dingo", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        if reportDroppedItem(enemy="dingo", drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(
            enemy="dingo", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        if reportDroppedItem(enemy="dingo", drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
            thunderCount[1] += 1
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(
            enemy="dingo", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        if reportDroppedItem(enemy="dingo", drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
            thunderCount[2] += 1
    advance10 += 3

    dropChances = trackDrops(enemy="condor", battles=1,
                             extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(
            enemy="condor", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        if reportDroppedItem(enemy="condor", drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(
            enemy="condor", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        if reportDroppedItem(enemy="condor", drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
            thunderCount[1] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(
            enemy="condor", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        if reportDroppedItem(enemy="condor", drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
            thunderCount[2] += 1
    advance10 += 3

    dropChances = trackDrops(
        enemy="water_flan", battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(
            enemy="water_flan", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        reportDroppedItem(enemy="water_flan", drop=finalItem,
                          prefType=0, prefAbility=0x8026, report=report)
        advance12[0] += 4
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(
            enemy="water_flan", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        reportDroppedItem(enemy="water_flan", drop=finalItem,
                          prefType=0, needAdv=1, prefAbility=0x8026, report=report)
        advance12[1] += 4
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(
            enemy="water_flan", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        reportDroppedItem(enemy="water_flan", drop=finalItem,
                          prefType=0, needAdv=2, prefAbility=0x8026, report=report)
        advance12[2] += 4
    advance10 += 3

    # Kimahri drops something guaranteed.
    dropChances = trackDrops(enemy="???", battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(
            enemy="???", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        reportDroppedItem(enemy="???", drop=finalItem,
                          prefType=0, prefAbility=0x8026, report=report)
        advance12[0] += 4
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(
            enemy="???", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        reportDroppedItem(enemy="???", drop=finalItem, prefType=0,
                          needAdv=1, prefAbility=0x8026, report=report)
        advance12[1] += 4
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(
            enemy="???", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        reportDroppedItem(enemy="???", drop=finalItem, prefType=0,
                          needAdv=2, prefAbility=0x8026, report=report)
        advance12[2] += 4
    advance10 += 3

    dropChances = trackDrops(
        enemy="garuda_3", battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(
            enemy="garuda_3", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        if reportDroppedItem(enemy="garuda_3", drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(
            enemy="garuda_3", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        if reportDroppedItem(enemy="garuda_3", drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
            thunderCount[1] += 1
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(
            enemy="garuda_3", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        if reportDroppedItem(enemy="garuda_3", drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
            thunderCount[2] += 1
    advance10 += 3

    dropChances = trackDrops(enemy="dingo", battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(
            enemy="dingo", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        if reportDroppedItem(enemy="dingo", drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(
            enemy="dingo", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        if reportDroppedItem(enemy="dingo", drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
            thunderCount[1] += 1
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(
            enemy="dingo", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        if reportDroppedItem(enemy="dingo", drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
            thunderCount[2] += 1
    advance10 += 3

    dropChances = trackDrops(enemy="condor", battles=1,
                             extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(
            enemy="condor", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        if reportDroppedItem(enemy="condor", drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(
            enemy="condor", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        if reportDroppedItem(enemy="condor", drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
            thunderCount[1] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(
            enemy="condor", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        if reportDroppedItem(enemy="condor", drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
            thunderCount[2] += 1
    advance10 += 3

    dropChances = trackDrops(
        enemy="water_flan", battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(
            enemy="water_flan", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        reportDroppedItem(enemy="water_flan", drop=finalItem,
                          prefType=0, prefAbility=0x8026, report=report)
        advance12[0] += 4
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(
            enemy="water_flan", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        reportDroppedItem(enemy="water_flan", drop=finalItem,
                          prefType=0, needAdv=1, prefAbility=0x8026, report=report)
        advance12[1] += 4
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(
            enemy="water_flan", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        reportDroppedItem(enemy="water_flan", drop=finalItem,
                          prefType=0, needAdv=2, prefAbility=0x8026, report=report)
        advance12[2] += 4
    advance10 += 3
    advance01 += 6

    partySize = 5
    # Sin's Fin
    dropChances = trackDrops(enemy="sin", battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(
            enemy="sin", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        if reportDroppedItem(enemy="sin-fin", drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(
            enemy="sin", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        if reportDroppedItem(enemy="sin-fin", drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
            thunderCount[1] += 1
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(
            enemy="sin", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        if reportDroppedItem(enemy="sin-fin", drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
            thunderCount[2] += 1
    advance10 += 3
    advance01 += 1

    partySize = 2
    # Sinspawn Echuilles
    dropChances = trackDrops(enemy="sinspawn_echuilles",
                             battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(
            enemy="sinspawn_echuilles", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        if reportDroppedItem(enemy="sinspawn_echuilles", drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(
            enemy="sinspawn_echuilles", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        if reportDroppedItem(enemy="sinspawn_echuilles", drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
            thunderCount[1] += 1
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(
            enemy="sinspawn_echuilles", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        if reportDroppedItem(enemy="sinspawn_echuilles", drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
            thunderCount[2] += 1
    advance10 += 3
    advance01 += 1

    enemy = "ragora"
    partySize = 5
    # Lancet tutorial
    dropChances = trackDrops(enemy=enemy, battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(
            enemy=enemy, preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        if reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(
            enemy=enemy, preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        if reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
            thunderCount[1] += 1
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(
            enemy=enemy, preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        if reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
            thunderCount[2] += 1
    advance10 += 3
    advance01 += 1

    partySize = 5
    # Kilika
    geneauxTrack = False
    kilikaBattles = comingBattles(
        area="kilika_woods", battleCount=3, extraAdvances=advance01)
    logs.writeRNGTrack("Kilika battles:")
    import area.kilika as kilika
    bestBattle = kilika.selectBestOfTwo(kilikaBattles)
    ragoraKills = [0, 0, 0]
    if "ragora" in bestBattle:
        for i in range(len(bestBattle)):
            if bestBattle[i] == "ragora":
                ragoraKills[0] += 1
                ragoraKills[1] += 1
                ragoraKills[2] += 1
    bestBattleComplete = [False, False, False]

    for bCount in (range(kilikaCount)):
        if bCount == 3 and not geneauxTrack:
            advance10 += 3  # Tentacles
            finalItem, advance13[0] = itemToBeDropped(
                enemy="sinspawn_geneaux", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
            advance12[0] += 4
            reportDroppedItem(enemy="geneaux", drop=finalItem,
                              prefType=0, prefAbility=0x8026, report=report)
            finalItem, advance13[1] = itemToBeDropped(
                enemy="sinspawn_geneaux", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
            advance12[1] += 4
            reportDroppedItem(enemy="geneaux", drop=finalItem, prefType=0,
                              needAdv=1, prefAbility=0x8026, report=report)
            finalItem, advance13[2] = itemToBeDropped(
                enemy="sinspawn_geneaux", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
            advance12[2] += 4
            reportDroppedItem(enemy="geneaux", drop=finalItem, prefType=0,
                              needAdv=2, prefAbility=0x8026, report=report)

            advance01 += 1
            geneauxTrack = True

        battleFormations = comingBattles(
            area="kilika_woods", battleCount=1, extraAdvances=advance01)
        logs.writeRNGTrack(str(battleFormations))
        for x in range(len(battleFormations)):
            for i in range(len(battleFormations[x])):
                thisBattle = battleFormations[x]
                if thisBattle == ["ragora"] and ragoraKills[0] == 0:
                    pass
                else:
                    dropChances = trackDrops(
                        enemy=thisBattle[i], battles=1, extraAdvances=advance10)
                    if len(dropChances[0]) >= 1:
                        finalItem, advance13[0] = itemToBeDropped(
                            enemy=thisBattle[i], preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
                        advance12[0] += 4
                        if thisBattle == "ragora":
                            ragoraKills[0] -= 1
                        elif thisBattle == "yellow_element":
                            if finalItem.equipType == 0:
                                if reportDroppedItem(enemy=thisBattle[i], drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
                                    thunderCount[0] += 1
                                    killYellow[0] = x
                            elif thisBattle[i] == bestBattle and not bestBattleComplete[0]:
                                if reportDroppedItem(enemy=thisBattle[i], drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
                                    bestBattleComplete[0] = True
                            else:
                                advance12[0] -= 4
                        else:
                            if reportDroppedItem(enemy=thisBattle[i], drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
                                thunderCount[0] += 1
                    if len(dropChances[1]) >= 1:
                        finalItem, advance13[1] = itemToBeDropped(
                            enemy=thisBattle[i], preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
                        advance12[1] += 4
                        if thisBattle == "ragora":
                            ragoraKills[1] -= 1
                        elif thisBattle == "yellow_element":
                            if finalItem.equipType == 0:
                                if reportDroppedItem(enemy=thisBattle[i], drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
                                    thunderCount[1] += 1
                                    killYellow[1] = x
                            elif thisBattle[i] == bestBattle and not bestBattleComplete[1]:
                                if reportDroppedItem(enemy=thisBattle[i], drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
                                    bestBattleComplete[1] = True
                            else:
                                advance12[1] -= 4
                        else:
                            if reportDroppedItem(enemy=thisBattle[i], drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
                                thunderCount[1] += 1
                    if len(dropChances[2]) >= 1:
                        finalItem, advance13[2] = itemToBeDropped(
                            enemy=thisBattle[i], preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
                        advance12[2] += 4
                        if thisBattle == "ragora":
                            ragoraKills[2] -= 1
                        elif thisBattle == "yellow_element":
                            if finalItem.equipType == 0:
                                if reportDroppedItem(enemy=thisBattle[i], drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
                                    thunderCount[2] += 1
                                    killYellow[2] = x
                            elif thisBattle[i] == bestBattle and not bestBattleComplete[2]:
                                if reportDroppedItem(enemy=thisBattle[i], drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
                                    bestBattleComplete[2] = True
                            else:
                                advance12[2] -= 4
                        else:
                            if reportDroppedItem(enemy=thisBattle[i], drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
                                thunderCount[2] += 1
                    advance10 += 3
            advance01 += 2

    partySize = 5
    # Workers
    battleFormations = comingBattles(
        area="machina_1", battleCount=1, extraAdvances=advance01)
    for x in range(len(battleFormations)):
        for i in range(len(battleFormations[x])):
            thisBattle = battleFormations[x]
            dropChances = trackDrops(
                enemy=thisBattle, battles=1, extraAdvances=advance10)
            if len(dropChances[0]) >= 1:
                if trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10):
                    finalItem, advance13[0] = itemToBeDropped(
                        enemy=thisBattle, preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
                    advance12[0] += 4
                    if reportDroppedItem(enemy=thisBattle, drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
                        thunderCount[0] += 1
            if len(dropChances[1]) >= 1:
                if trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10):
                    finalItem, advance13[1] = itemToBeDropped(
                        enemy=thisBattle, preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
                    advance12[1] += 4
                    if reportDroppedItem(enemy=thisBattle, drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
                        thunderCount[1] += 1
            if len(dropChances[2]) >= 1:
                if trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10):
                    finalItem, advance13[2] = itemToBeDropped(
                        enemy=thisBattle, preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
                    advance12[2] += 4
                    if reportDroppedItem(enemy=thisBattle, drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
                        thunderCount[2] += 1
            advance10 += 3
        advance01 += 1
    battleFormations = comingBattles(
        area="machina_2", battleCount=1, extraAdvances=advance01)
    for x in range(len(battleFormations)):
        for i in range(len(battleFormations[x])):
            thisBattle = battleFormations[x]
            dropChances = trackDrops(
                enemy=thisBattle, battles=1, extraAdvances=advance10)
            if len(dropChances[0]) >= 1:
                if trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10):
                    finalItem, advance13[0] = itemToBeDropped(
                        enemy=thisBattle, preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
                    advance12[0] += 4
                    if reportDroppedItem(enemy=thisBattle, drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
                        thunderCount[0] += 1
            if len(dropChances[1]) >= 1:
                if trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10):
                    finalItem, advance13[1] = itemToBeDropped(
                        enemy=thisBattle, preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
                    advance12[1] += 4
                    if reportDroppedItem(enemy=thisBattle, drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
                        thunderCount[1] += 1
            if len(dropChances[2]) >= 1:
                if trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10):
                    finalItem, advance13[2] = itemToBeDropped(
                        enemy=thisBattle, preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
                    advance12[2] += 4
                    if reportDroppedItem(enemy=thisBattle, drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
                        thunderCount[2] += 1
            advance10 += 3
        advance01 += 1
    battleFormations = comingBattles(
        area="machina_3", battleCount=1, extraAdvances=advance01)
    for x in range(len(battleFormations)):
        for i in range(len(battleFormations[x])):
            thisBattle = battleFormations[x]
            dropChances = trackDrops(
                enemy=thisBattle, battles=1, extraAdvances=advance10)
            if len(dropChances[0]) >= 1:
                if trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10):
                    finalItem, advance13[0] = itemToBeDropped(
                        enemy=thisBattle, preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
                    advance12[0] += 4
                    if reportDroppedItem(enemy=thisBattle, drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
                        thunderCount[0] += 1
            if len(dropChances[1]) >= 1:
                if trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10):
                    finalItem, advance13[1] = itemToBeDropped(
                        enemy=thisBattle, preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
                    advance12[1] += 4
                    if reportDroppedItem(enemy=thisBattle, drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
                        thunderCount[1] += 1
            if len(dropChances[2]) >= 1:
                if trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10):
                    finalItem, advance13[2] = itemToBeDropped(
                        enemy=thisBattle, preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
                    advance12[2] += 4
                    if reportDroppedItem(enemy=thisBattle, drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
                        thunderCount[2] += 1
            advance10 += 3
        advance01 += 1

    # Finally, Oblitz is guaranteed to drop an item.
    finalItem, advance13[0] = itemToBeDropped(
        enemy="oblitzerator", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
    if reportDroppedItem(enemy="Oblitzerator", drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
        thunderCount[0] += 1
        oblitzWeap[0] = True
    finalItem, advance13[1] = itemToBeDropped(
        enemy="oblitzerator", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
    if reportDroppedItem(enemy="Oblitzerator", drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
        thunderCount[1] += 1
        oblitzWeap[1] = True
    finalItem, advance13[2] = itemToBeDropped(
        enemy="oblitzerator", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
    if reportDroppedItem(enemy="Oblitzerator", drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
        thunderCount[2] += 1
        oblitzWeap[2] = True
    advance12[0] += 4
    advance10 += 3

    logs.writeRNGTrack("End: thunder strike drops")
    logs.writeRNGTrack("===================")
    logs.writeRNGTrack("The following values are per advance.")
    logs.writeRNGTrack("Drops possible:" + str(thunderCount))
    logs.writeRNGTrack("Weapon drops on Oblitzerator:" + str(oblitzWeap))
    logs.writeRNGTrack(
        "Kill Yellow ele on Kilika battles:" + str(killYellow))
    return thunderCount, killYellow


def decideSkipZanLuck() -> bool:
    # This function tracks if we need to pick up the luck and fortune spheres in Zanarkand.
    # This will track through from Yunalesca to BFA, the two fights with ~4% chance to miss.
    # False == there will be a miss. True == no miss.
    extraXP = 0  # where is the variable for this? Somewhere in vars file? This is if we need to kill something in Dome for XP...
    bahamutLuck = 17
    keeperCrit = memory.main.futureAttackWillCrit(character=7, charLuck=bahamutLuck, enemyLuck=20, attackIndex=extraXP)
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
        if not futureAttackHitMiss(character=7, enemy="yunalesca", attackIndex=attackCount):
            print("### Miss on Yunalesca, attack number", i)
            return False
        attackCount += 1
    if gameVars.nemesis():  # BFA miss does not factor in for Nemesis route.
        return True

    arm1Crit = memory.main.futureAttackWillCrit(character=7, charLuck=bahamutLuck, enemyLuck=15, attackIndex=attackCount)
    if arm1Crit:
        print("### Expecting crit on Arm 1")
        attackCount += 1
    else:
        attackCount += 2
    arm2Crit = memory.main.futureAttackWillCrit(character=7, charLuck=bahamutLuck, enemyLuck=15, attackIndex=attackCount)
    if arm2Crit:
        print("### Expecting crit on Arm 2")
        attackCount += 1
    else:
        attackCount += 2
    attackCount += 1  # Core is always one attack
    faceCrit = memory.main.futureAttackWillCrit(character=7, charLuck=bahamutLuck, enemyLuck=15, attackIndex=attackCount)
    if not faceCrit:
        faceCrit = memory.main.futureAttackWillCrit(character=7, charLuck=bahamutLuck, enemyLuck=15, attackIndex=attackCount + 1)
    if faceCrit:
        print("### Expecting crit on Face")
        attackCount += 2
    else:
        attackCount += 3
    if not futureAttackHitMiss(character=7, enemy="seymour_flux", attackIndex=attackCount):
        print("### Miss on Omnis")
        return False
    attackCount += 1  # One attack on Seymour
    for i in range(3):
        print("### BFA attack num ", i, " | ", attackCount)
        if not futureAttackHitMiss(character=7, enemy="bfa", attackIndex=attackCount):
            print("### Miss on BFA, attack number", i)
            return False
        attackCount += 1
    print("### No misses registered. Should be good to skip Luck/Fortune chests.")
    return True


def zombieTrack(report=False):
    advance01 = 0
    advance10 = 0
    advance12 = [0] * 3
    advance13 = [0] * 3
    zombieResults = [99] * 3
    partySize = 7

    # "sanctuary_keeper"
    # Check random encounters for best charge, plan for 1 encounter, 1 death if possible to charge.
    # "spectral_keeper"
    # "yunalesca"

    enemy = "sanctuary_keeper"
    dropChances = trackDrops(enemy=enemy, battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(
            enemy=enemy, preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        reportDroppedItem(enemy=enemy, drop=finalItem,
                          prefType=0, prefAbility=0x8032, report=report)
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(
            enemy=enemy, preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0,
                          needAdv=1, prefAbility=0x8032, report=report)
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(
            enemy=enemy, preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0,
                          needAdv=2, prefAbility=0x8032, report=report)
    advance10 += 3
    advance01 += 1

    import area.zanarkand as zanarkand
    zanarkand.decideNEA(bonusAdvance=1)
    # One death expected to recharge Rikku. No drops expected.
    if gameVars.getNEAzone() in [1, 2]:
        advance10 += 3
        advance01 += 1

    enemy = "spectral_keeper"
    dropChances = trackDrops(enemy=enemy, battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(
            enemy=enemy, preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        reportDroppedItem(enemy=enemy, drop=finalItem,
                          prefType=0, prefAbility=0x8032, report=report)
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(
            enemy=enemy, preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0,
                          needAdv=1, prefAbility=0x8032, report=report)
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(
            enemy=enemy, preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0,
                          needAdv=2, prefAbility=0x8032, report=report)
    advance10 += 3
    advance01 += 1

    enemy = "yunalesca"
    dropChances = trackDrops(enemy=enemy, battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(
            enemy=enemy, preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        if reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0, prefAbility=0x8032, report=report):
            zombieResults[0] = finalItem.equipOwnerAlt
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(
            enemy=enemy, preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        if reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8032, report=report):
            zombieResults[1] = finalItem.equipOwnerAlt
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(
            enemy=enemy, preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        if reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8032, report=report):
            zombieResults[2] = finalItem.equipOwnerAlt
    advance10 += 3
    advance01 += 1

    return zombieResults

def neaTrack():
    preAdvance12 = 0
    preAdvance13 = 0
    
    totalAdvancePreX = 999
    totalAdvancePostX = 999
    enemy = 'defender_x'
    
    #If already aligned for NEA, we want X to drop nothing.
    nextItem, preAdvance13 = itemToBeDropped(enemy='ghost')
    if nextItem.equipmentType() == 1 and nextItem.hasAbility(0x801D):
        #print("/// Already aligned")
        totalAdvancePostX = 0
    #else:
        #print("/// Not yet aligned. Looking for more results.")
    
    
    while totalAdvancePreX == 999 or totalAdvancePostX == 999 and preAdvance < 100:
        preAdvance12 += 4
        nextItem, preAdvance13 = itemToBeDropped(enemy='ghost', preAdvance12=preAdvance12, preAdvance13=preAdvance13)
        #print("/// post-13: ", postAdvance13)
        #preAdvance13 += postAdvance13
        #print("/// upd-pre13: ", preAdvance13)
        #print("/// Type: ", nextItem.equipmentType(), " /// Abilities: ", nextItem.abilities(), " /// ", int(preAdvance12 / 4))
        #if 0x801D in nextItem.abilities():
        #    print("AAAAAAAAAAAAAAAA")
        #if 32797 in nextItem.abilities():
        #    print("BBBBBBBBBBBBBBBB")
        #    memory.main.waitFrames(300)
        if nextItem.equipmentType() == 1 and 0x801D in nextItem.abilities():
            if totalAdvancePostX == 999:
                totalAdvancePostX = int(preAdvance12 / 4)
            if totalAdvancePreX == 999:
                totalAdvancePreX = int((preAdvance12 / 4) - 1)
    #print("/// Pre-X: ", totalAdvancePreX, " /// Post-X", totalAdvancePostX)
    return totalAdvancePreX, totalAdvancePostX

def printManipInfo():
    preX, postX = neaTrack()
    print("--------------------------")
    print("Upcoming RNGs:")
    print("Next, before X:", preX, "| Next, after X: ", postX)
    print("RNG10:", memory.main.nextChanceRNG10(), "| Pre Defender X: ", memory.main.nextChanceRNG10Calm())
    print("--------------------------")

def nextActionEscape(character: int = 0):
    index = 20 + character
    escapeRoll = memory.main.s32(
        memory.main.rngArrayFromIndex(index=index, arrayLen=1)[1]) & 255
    return escapeRoll < 191


def nextActionHitMiss(character: int = 0, enemy: str = "anima"):
    return futureAttackHitMiss(character=character, enemy=enemy)


def futureAttackHitMiss(character: int = 0, enemy: str = "anima", attackIndex: int = 0):
    # print("=========================")
    # print("Checking hit chance - character:", character)
    # Need more work on this. There are a lot of variables we still need from memory.
    # Character info, get these from memory
    index = 36 + character
    hit_rng = memory.main.rngArrayFromIndex(index=index, arrayLen=attackIndex + 3)[attackIndex + 1]
    # print("### HitRNG ", hit_rng)
    luck = memory.main.charLuck(character)
    # print("Luck:", luck)
    accuracy = memory.main.charAccuracy(character)
    # print("Accuracy:", accuracy)

    if enemy == "bfa":
        target_luck = 15
        target_evasion = 0
    else:
        # Data directly from the tracker
        target_luck = MONSTERS[enemy].stats['Luck']
        # print("Enemy luck: ", target_luck)
        target_evasion = MONSTERS[enemy].stats['Evasion']
        # print("Enemy evasion:", target_evasion)

    # Unused, but technically part of the formula
    aims = 0
    target_reflexes = 0

    hit_chance = accuracy * 2
    hit_chance = (hit_chance * 0x66666667) // 0xffffffff
    hit_chance = hit_chance // 2
    hit_chance_index = hit_chance // 0x80000000
    hit_chance_index += hit_chance - target_evasion + 10
    if hit_chance_index < 0:
        hit_chance_index = 0
    elif hit_chance_index > 8:
        hit_chance_index = 8
    hit_chance = hitChanceTable(hit_chance_index) + luck
    hit_chance += (aims - target_reflexes) * 10 - target_luck
    # print("Hit Chance: ", hit_chance, " vs ", (memory.s32(hit_rng) % 101))
    # print("Hit results: ", hit_chance > (memory.s32(hit_rng) % 101))
    # print("=========================")
    return hit_chance > (memory.main.s32(hit_rng) % 101)


def hitChanceTable(index: int):
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


def oblitzHistory():
    filepath = "oblitzRNG\\results.json"
    with open(filepath, 'r') as fp:
        rngValues = json.load(fp)
    return rngValues


def saveOblitzHistory(rngVals):
    writing = dict(rngVals)
    filepath = "oblitzRNG\\results.json"
    with open(filepath, 'w') as fp:
        json.dump(writing, fp)


def recordBlitzResults_Tyton(duration, testMode=False):
    records = oblitzHistory()
    if testMode:
        seed = '31'
        sub_key = '9999'
        victory = False
    else:
        seed = str(memory.main.rngSeed())
        sub_key = str(gameVars.oblitzRNGCheck())
        victory = gameVars.getBlitzWin()
    if seed in records.keys():
        if sub_key in records[seed].keys():
            if records[seed][sub_key]['victory'] and not victory:
                return
            if records[seed][sub_key]['victory'] == victory and duration >= records[str(seed)][str(sub_key)]['duration']:
                return

    records[seed][sub_key]['duration'] = duration
    records[seed][sub_key]['victory'] = victory
    saveOblitzHistory(records)


def recordBlitzResults(duration, testMode=False):
    filepath = "oblitzRNG\\results.json"
    records = oblitzHistory()
    print("========================")
    if testMode:
        newVal = {31: {9999: {"duration": duration, "victory": False}}}
        if str(31) in records.keys():
            print(newVal[31].keys())
            if 9999 in newVal[31].keys():
                records['31']['9999']['victory'] = True
                records['31']['9999']['duration'] = duration
            else:
                records['31'].update(newVal[31])
        else:
            records.update(newVal)
    else:
        newVal = {memory.main.rngSeed(): {gameVars.oblitzRNGCheck(): {"duration": duration, "victory": gameVars.getBlitzWin()}}}
        if str(memory.main.rngSeed()) in records.keys():
            if gameVars.oblitzRNGCheck() in records[str(memory.main.rngSeed())].keys():
                if not gameVars.getBlitzWin() and records[str(memory.main.rngSeed())][gameVars.oblitzRNGCheck()]['victory']:
                    records[str(memory.main.rngSeed())][gameVars.oblitzRNGCheck()]['victory'] = gameVars.getBlitzWin()
                    records[str(memory.main.rngSeed())][gameVars.oblitzRNGCheck()]['duration'] = duration
                elif gameVars.getBlitzWin() == records[str(memory.main.rngSeed())][gameVars.oblitzRNGCheck()]['victory']:
                    if duration > records[str(memory.main.rngSeed())][gameVars.oblitzRNGCheck()]['duration']:
                        records[str(memory.main.rngSeed())][gameVars.oblitzRNGCheck()]['victory'] = gameVars.getBlitzWin()
                        records[str(memory.main.rngSeed())][gameVars.oblitzRNGCheck()]['duration'] = duration
            else:
                records[str(memory.main.rngSeed())].update(newVal[memory.main.rngSeed()])
        else:
            records.update(newVal)
    print(newVal)

    print("========================")
    print(records)

    with open(filepath, 'w') as fp:
        json.dump(records, fp)


def hitsToSeed(hitsArray: int):
    with open('csv\\hits_to_seed.csv', 'r', newline='') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            if row['hit0'] == '':
                pass
            elif int(row['hit0']) == hitsArray[0] and int(row['hit1']) == hitsArray[1] and int(row['hit2']) == hitsArray[2] and \
                    int(row['hit3']) == hitsArray[3] and int(row['hit4']) == hitsArray[4] and int(row['hit5']) == hitsArray[5]:
                return row['seed']
    return "Err_seed_not_found"
