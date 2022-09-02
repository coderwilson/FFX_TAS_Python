import FFX_memory
import csv
#from tracker.data.formations import allFormations
from tracker.ffx_rng_tracker.data.monsters import MONSTERS
import json
import FFX_Logs
import FFX_vars
gameVars = FFX_vars.varsHandle()

def areaFormations(area:str):
    f = open('tracker/data/formations.json')
    allFormations = json.load(f)
    f.close()
    if area in allFormations["random"].keys():
        return allFormations["random"][area]["formations"]
    elif area in allFormations["bosses"].keys():
        return allFormations["bosses"][area]["formation"]
    else:
        print("Key not found:", area)

def comingBattles(area:str="kilika_woods", battleCount:int=10, extraAdvances:int=0):
    formations = areaFormations(area=area)
    advances = FFX_memory.rng01Advances((battleCount*2) + extraAdvances)
    if extraAdvances != 0:
        while extraAdvances != 0:
            del advances[0]
            extraAdvances -= 1
    battles = []
    for i in range(battleCount):
        nextValue = formations[(advances[(i*2)+1] & 0x7fffffff) % len(formations)]
        battles.append(nextValue)
    return battles

def comingBattleType(extraAdvances:int=0, initiative=False):
    advances = FFX_memory.rng01Advances(2 + extraAdvances)
    if extraAdvances != 0:
        while extraAdvances != 0:
            del advances[0]
            extraAdvances -= 1
    battleType = (advances[2] & 0x7fffffff) & 255
    if initiative == True:
        battleType -= 33
    
    if battleType < 32:
        return 1
    elif battleType < 255 - 32:
        return 0
    else:
        return 2

def singlesBattles(area:str="kilika_woods", battleCount:int=10, extraAdvances:int=0):
    formations = areaFormations(area=area)
    advances = FFX_memory.rng01Advances((battleCount) + extraAdvances)
    if extraAdvances != 0:
        while extraAdvances != 0:
            del advances[0]
            extraAdvances -= 1
    battles = []
    for i in range(battleCount):
        nextValue = formations[(advances[i+1] & 0x7fffffff) % len(formations)]
        battles.append(nextValue)
    return battles

def dropChance(enemy:str='ghost'):
    return MONSTERS[enemy].equipment['drop_chance']

def dropSlots(enemy:str='ghost'):
    return MONSTERS[enemy].equipment['slots_range']

def SlotMod(enemy:str='ghost'):
    return MONSTERS[enemy].equipment['slots_modifier']

def dropAbilityCount(enemy:str='ghost'):
    return MONSTERS[enemy].equipment['max_ability_rolls_range']

def AbilityMod(enemy:str='ghost'):
    return MONSTERS[enemy].equipment['max_ability_rolls_modifier']

def dropAbilityList(enemy:str='ghost', equipType:int=0):
    if equipType == 0:
        array = MONSTERS[enemy].equipment['ability_arrays']['Tidus']['Weapon']
    else:
        array = MONSTERS[enemy].equipment['ability_arrays']['Tidus']['Armor']
    retVal = []
    for i in range(len(array)):
        try:
            retVal.append(array[i].tas_id)
        except:
            retVal.append(255)

    return retVal

def earlyBattleCount():
    with open('csv\\Seed_Battle_Variance.csv', 'r', newline='') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            if int(row['Seed']) == FFX_memory.rngSeed():
                return row

def trackDrops(enemy:str='ghost', battles:int=20, extraAdvances:int=0):
    noAdvanceArray = []
    oneAdvanceArray = []
    twoAdvanceArray = []
    advances = (battles + 1) * 3
    randArray = FFX_memory.rng10Array(arrayLen=advances + extraAdvances)
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
                oneAdvanceArray.append((i-1) / 3)
            else:
                twoAdvanceArray.append((i-2) / 3)
    return [noAdvanceArray, oneAdvanceArray, twoAdvanceArray]

def itemToBeDropped(enemy:str='ghost', preAdvance12:int=0, preAdvance13:int=0, partySize:int=7):
    slotMod = SlotMod(enemy=enemy)
    abilityMod = AbilityMod(enemy=enemy)
    
    if partySize == 2:
        partyChars = [0,4]
    elif partySize == 3:
        partyChars = [0,4,6]
    elif partySize == 4:
        partyChars = [0,1,4,5]
    elif partySize == 5:
        partyChars = [0,1,3,4,5]
    elif partySize == 6:
        partyChars = [0,1,2,3,4,5]
    elif partySize == 7:
        partyChars = [0,1,2,3,4,5,6]
    else:
        partyChars = [0]
    
    advance12 = 4 + preAdvance12
    testArray12 = FFX_memory.rng12Array(advance12)
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
    
    #Type
    equipType = (testArray12[1] & 0x7fffffff) % 2
    
    #Slots
    baseSlots = (slotMod + ((testArray12[2] & 0x7fffffff) & 7)) - 4
    slots = (baseSlots + ((baseSlots >> 31) & 7)) >> 2
    if slots == 0:
        slots = 1

    #Abilities
    baseMod = (abilityMod + ((testArray12[3] & 0x7fffffff) & 7)) - 4
    abilityCount = (baseMod + ((baseMod >> 31) & 7)) >> 3
    if slots < abilityCount:
        abilityCount = slots
    
    #rng13 logic here, determine which ability goes where.
    newAbilities = abilityToBeDropped(enemy=enemy, equipType=equipType, slots=abilityCount, advances=preAdvance13)
    abilityList = newAbilities[0]
    preAdvance13 += newAbilities[1]
    
    finalItem = FFX_memory.equipment(equipNum=0)
    finalItem.createCustom(eType=equipType, eOwner1=user1, eOwner2=user2, eSlots=slots, eAbilities=abilityList)
    
    return finalItem, preAdvance13

def abilityToBeDropped(enemy:str='ghost', equipType:int=0, slots:int=1, advances:int=0):
    outcomes = dropAbilityList(enemy=enemy, equipType=equipType)
    if slots == 0:
        slots = 1
    filledSlots = [99] * slots
    
    ptr = 0 #Pointer that indicates how many advances needed for this evaluation
    testArray = FFX_memory.rng13Array(arrayLen=50+advances)
    
    if outcomes[0]:
        filledSlots.remove(99)
        filledSlots.append(outcomes[0])
        
    if 99 in filledSlots and ptr < 50+advances:
        while 99 in filledSlots and ptr < 50+advances:
            ptr += 1 #Increment to match the first (and subsequent) advance(s)
            try:
                if outcomes[(((testArray[ptr] & 0x7fffffff) % 7) + 1)] in filledSlots:
                    pass
                else:
                    filledSlots.remove(99)
                    filledSlots.append(
                        outcomes[(((testArray[ptr] & 0x7fffffff) % 7) + 1)])
            except:
                pass
    
    while 99 in filledSlots:
        filledSlots.remove(99)
    
    #Format so that we have four slots always.
    if len(filledSlots) < 4:
        while len(filledSlots) < 4:
            filledSlots.append(255)
    
    return [filledSlots, ptr]

def reportDroppedItem(enemy:str, drop=FFX_memory.equipment, prefType:int=99, prefAbility:int=255, needAdv:int=0, report=False):
    abiStr = str(prefAbility)
    prefType
    report = True
    if prefAbility != 255 and not abiStr in drop.equipAbilities:
        report = False
    elif prefType != 99 and prefType != drop.equipType:
        print(prefType)
        print(drop.equipType)
        report = False
    
    if report == True:
        FFX_Logs.writeRNGTrack("+Item drop off of:"+str(enemy)+" | advances:"+str(needAdv))
        FFX_Logs.writeRNGTrack("+Owner, char-killed (9 = killer): "+str(drop.equipOwner))
        FFX_Logs.writeRNGTrack("+Owner, aeon-killed: "+str(drop.equipOwnerAlt))
        if drop.equipType == 0:
            FFX_Logs.writeRNGTrack("+Type: Weapon")
        else:
            FFX_Logs.writeRNGTrack("+Type: Armor")
        FFX_Logs.writeRNGTrack("+Open Slots: "+str(drop.slots))
        FFX_Logs.writeRNGTrack("+Abilities: "+str(drop.equipAbilities))
        FFX_Logs.writeRNGTrack("===================")
        return True
    else:
        FFX_Logs.writeRNGTrack("-Undesirable item dropped by: "+str(enemy)+" | advances:"+str(needAdv))
        FFX_Logs.writeRNGTrack("-Owner, char-killed: "+str(drop.equipOwner))
        FFX_Logs.writeRNGTrack("-Owner, aeon-killed: "+str(drop.equipOwnerAlt))
        if drop.equipType == 0:
            FFX_Logs.writeRNGTrack("-Type: Weapon")
        else:
            FFX_Logs.writeRNGTrack("-Type: Armor")
        FFX_Logs.writeRNGTrack("-Open Slots: "+str(drop.slots))
        FFX_Logs.writeRNGTrack("-Abilities: "+str(drop.equipAbilities))
        FFX_Logs.writeRNGTrack("===================")
        return False

def tStrikeTracking(tros=False, report=False):
    if tros:
        advance01 = 0
        advance10 = 3 #Starts off with just the Tros kill advance.
    else:
        advance01 = 1
        advance10 = 9 #Starts off with two advances for pirhanas and one for Tros
    if report:
        FFX_Logs.openRNGTrack()
        FFX_Logs.writeRNGTrack(FFX_memory.rng10Array(arrayLen=80))
        FFX_Logs.writeRNGTrack("#########################")
    advance12 = [0,0,0] #Tros drops one item
    advance13 = [0,0,0] #Tros item has no abilities
    thunderCount = [0,0,0] #Count results per advance, for returning later.
    oblitzWeap = [False] * 3 #Count only if Oblitz will drop a weapon for Tidus.
    killYellow = [0,0,0] #Increment only if we need to kill yellow element on a certain battle.
    battleVariance = earlyBattleCount()
    lagoonCount = int(battleVariance['Lagoon'])
    kilikaCount = int(battleVariance['Kilika'])
    partySize=4
    
    #Lagoon
    lagoonBattles = comingBattles(area="besaid_lagoon", battleCount=lagoonCount, extraAdvances=advance01)
    for i in range(len(lagoonBattles)):
        FFX_Logs.writeRNGTrack("Lagoon battle:")
        FFX_Logs.writeRNGTrack(str(lagoonBattles[i]))
        FFX_Logs.writeRNGTrack("Battle type: "+str(comingBattleType(extraAdvances=advance01+(2*i))))
        if len(lagoonBattles[i]) == 2:
            advance10 += 6
        elif len(lagoonBattles[i]) == 3 and comingBattleType(extraAdvances=advance01+(2*i)) == 1:
            advance10 += 9
        else:
            advance10 += 0
    advance01 += len(lagoonBattles) * 2
    
    FFX_Logs.writeRNGTrack("===================")
    FFX_Logs.writeRNGTrack("Looking ahead for thunder strike drops")
    
    #Besaid tutorials
    dropChances = trackDrops(enemy="dingo", battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(enemy="dingo", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        if reportDroppedItem(enemy="dingo", drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(enemy="dingo", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        if reportDroppedItem(enemy="dingo", drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
            thunderCount[1] += 1
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(enemy="dingo", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        if reportDroppedItem(enemy="dingo", drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
            thunderCount[2] += 1
    advance10 += 3
    
    dropChances = trackDrops(enemy="condor", battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(enemy="condor", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        if reportDroppedItem(enemy="condor", drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(enemy="condor", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        if reportDroppedItem(enemy="condor", drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
            thunderCount[1] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(enemy="condor", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        if reportDroppedItem(enemy="condor", drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
            thunderCount[2] += 1
    advance10 += 3
        
    dropChances = trackDrops(enemy="water_flan", battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(enemy="water_flan", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        reportDroppedItem(enemy="water_flan", drop=finalItem, prefType=0, prefAbility=0x8026, report=report)
        advance12[0] += 4
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(enemy="water_flan", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        reportDroppedItem(enemy="water_flan", drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report)
        advance12[1] += 4
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(enemy="water_flan", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        reportDroppedItem(enemy="water_flan", drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report)
        advance12[2] += 4
    advance10 += 3
    
    # Kimahri drops something guaranteed.
    dropChances = trackDrops(enemy="???", battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(enemy="???", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        reportDroppedItem(enemy="???", drop=finalItem, prefType=0, prefAbility=0x8026, report=report)
        advance12[0] += 4
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(enemy="???", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        reportDroppedItem(enemy="???", drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report)
        advance12[1] += 4
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(enemy="???", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        reportDroppedItem(enemy="???", drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report)
        advance12[2] += 4
    advance10 += 3
    
    dropChances = trackDrops(enemy="garuda_3", battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(enemy="garuda_3", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        if reportDroppedItem(enemy="garuda_3", drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(enemy="garuda_3", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        if reportDroppedItem(enemy="garuda_3", drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
            thunderCount[1] += 1
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(enemy="garuda_3", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        if reportDroppedItem(enemy="garuda_3", drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
            thunderCount[2] += 1
    advance10 += 3
    
    dropChances = trackDrops(enemy="dingo", battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(enemy="dingo", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        if reportDroppedItem(enemy="dingo", drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(enemy="dingo", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        if reportDroppedItem(enemy="dingo", drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
            thunderCount[1] += 1
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(enemy="dingo", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        if reportDroppedItem(enemy="dingo", drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
            thunderCount[2] += 1
    advance10 += 3
    
    dropChances = trackDrops(enemy="condor", battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(enemy="condor", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        if reportDroppedItem(enemy="condor", drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(enemy="condor", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        if reportDroppedItem(enemy="condor", drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
            thunderCount[1] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(enemy="condor", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        if reportDroppedItem(enemy="condor", drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
            thunderCount[2] += 1
    advance10 += 3
        
    dropChances = trackDrops(enemy="water_flan", battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(enemy="water_flan", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        reportDroppedItem(enemy="water_flan", drop=finalItem, prefType=0, prefAbility=0x8026, report=report)
        advance12[0] += 4
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(enemy="water_flan", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        reportDroppedItem(enemy="water_flan", drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report)
        advance12[1] += 4
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(enemy="water_flan", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        reportDroppedItem(enemy="water_flan", drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report)
        advance12[2] += 4
    advance10 += 3
    advance01 += 6
    
    partySize=5
    #Sin's Fin
    dropChances = trackDrops(enemy="sin", battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(enemy="sin", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        if reportDroppedItem(enemy="sin-fin", drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(enemy="sin", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        if reportDroppedItem(enemy="sin-fin", drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
            thunderCount[1] += 1
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(enemy="sin", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        if reportDroppedItem(enemy="sin-fin", drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
            thunderCount[2] += 1
    advance10 += 3
    advance01 += 1
    
    partySize=2
    #Sinspawn Echuilles
    dropChances = trackDrops(enemy="sinspawn_echuilles", battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(enemy="sinspawn_echuilles", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        if reportDroppedItem(enemy="sinspawn_echuilles", drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(enemy="sinspawn_echuilles", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        if reportDroppedItem(enemy="sinspawn_echuilles", drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
            thunderCount[1] += 1
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(enemy="sinspawn_echuilles", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        if reportDroppedItem(enemy="sinspawn_echuilles", drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
            thunderCount[2] += 1
    advance10 += 3
    advance01 += 1
    
    enemy = "ragora"
    partySize=5
    #Lancet tutorial
    dropChances = trackDrops(enemy=enemy, battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(enemy=enemy, preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        if reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
            thunderCount[0] += 1
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(enemy=enemy, preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        if reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
            thunderCount[1] += 1
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(enemy=enemy, preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        if reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
            thunderCount[2] += 1
    advance10 += 3
    advance01 += 1
    
    partySize=5
    #Kilika
    geneauxTrack=False
    kilikaBattles = comingBattles(area="kilika_woods", battleCount=3, extraAdvances=advance01)
    FFX_Logs.writeRNGTrack("Kilika battles:")
    import FFX_Kilika
    bestBattle = FFX_Kilika.selectBestOfThree(kilikaBattles)
    ragoraKills = [0,0,0]
    if "ragora" in bestBattle:
        for i in range(len(bestBattle)):
            if bestBattle[i] == "ragora":
                ragoraKills[0] += 1
                ragoraKills[1] += 1
                ragoraKills[2] += 1
    bestBattleComplete = [False,False,False]
    
    for bCount in (range(kilikaCount)):
        if bCount == 3 and geneauxTrack==False:
            advance10 += 3 #Tentacles
            finalItem, advance13[0] = itemToBeDropped(enemy="sinspawn_geneaux", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
            advance12[0] += 4
            reportDroppedItem(enemy="geneaux", drop=finalItem, prefType=0, prefAbility=0x8026, report=report)
            finalItem, advance13[1] = itemToBeDropped(enemy="sinspawn_geneaux", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
            advance12[1] += 4
            reportDroppedItem(enemy="geneaux", drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report)
            finalItem, advance13[2] = itemToBeDropped(enemy="sinspawn_geneaux", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
            advance12[2] += 4
            reportDroppedItem(enemy="geneaux", drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report)
            
            advance01 += 1
            geneauxTrack = True
            
        battleFormations = comingBattles(area="kilika_woods", battleCount=1, extraAdvances=advance01)
        FFX_Logs.writeRNGTrack(str(battleFormations))
        for x in range(len(battleFormations)):
            for i in range(len(battleFormations[x])):
                thisBattle = battleFormations[x]
                if thisBattle == ["ragora"] and ragoraKills[0] == 0:
                    pass
                else:
                    dropChances = trackDrops(enemy=thisBattle[i], battles=1, extraAdvances=advance10)
                    if len(dropChances[0]) >= 1:
                        finalItem, advance13[0] = itemToBeDropped(enemy=thisBattle[i], preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
                        advance12[0] += 4
                        if thisBattle == "ragora":
                            ragoraKills[0] -= 1
                        elif thisBattle == "yellow_element":
                            if finalItem.equipType == 0:
                                if reportDroppedItem(enemy=thisBattle[i], drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
                                    thunderCount[0] += 1
                                    killYellow[0] = x
                            elif thisBattle[i] == bestBattle and bestBattleComplete[0] == False:
                                if reportDroppedItem(enemy=thisBattle[i], drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
                                    bestBattleComplete[0] = True
                            else:
                                advance12[0] -= 4
                        else:
                            if reportDroppedItem(enemy=thisBattle[i], drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
                                thunderCount[0] += 1
                    if len(dropChances[1]) >= 1:
                        finalItem, advance13[1] = itemToBeDropped(enemy=thisBattle[i], preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
                        advance12[1] += 4
                        if thisBattle == "ragora":
                            ragoraKills[1] -= 1
                        elif thisBattle == "yellow_element":
                            if finalItem.equipType == 0:
                                if reportDroppedItem(enemy=thisBattle[i], drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
                                    thunderCount[1] += 1
                                    killYellow[1] = x
                            elif thisBattle[i] == bestBattle and bestBattleComplete[1] == False:
                                if reportDroppedItem(enemy=thisBattle[i], drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
                                    bestBattleComplete[1] = True
                            else:
                                advance12[1] -= 4
                        else:
                            if reportDroppedItem(enemy=thisBattle[i], drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
                                thunderCount[1] += 1
                    if len(dropChances[2]) >= 1:
                        finalItem, advance13[2] = itemToBeDropped(enemy=thisBattle[i], preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
                        advance12[2] += 4
                        if thisBattle == "ragora":
                            ragoraKills[2] -= 1
                        elif thisBattle == "yellow_element":
                            if finalItem.equipType == 0:
                                if reportDroppedItem(enemy=thisBattle[i], drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
                                    thunderCount[2] += 1
                                    killYellow[2] = x
                            elif thisBattle[i] == bestBattle and bestBattleComplete[2] == False:
                                if reportDroppedItem(enemy=thisBattle[i], drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
                                    bestBattleComplete[2] = True
                            else:
                                advance12[2] -= 4
                        else:
                            if reportDroppedItem(enemy=thisBattle[i], drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
                                thunderCount[2] += 1
                    advance10 += 3
            advance01 += 2
    
    partySize=5
    #Workers
    battleFormations = comingBattles(area="machina_1", battleCount=1, extraAdvances=advance01)
    for x in range(len(battleFormations)):
        for i in range(len(battleFormations[x])):
            thisBattle = battleFormations[x]
            dropChances = trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10)
            if len(dropChances[0]) >= 1:
                if trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10):
                    finalItem, advance13[0] = itemToBeDropped(enemy=thisBattle, preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
                    advance12[0] += 4
                    if reportDroppedItem(enemy=thisBattle, drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
                        thunderCount[0] += 1
            if len(dropChances[1]) >= 1:
                if trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10):
                    finalItem, advance13[1] = itemToBeDropped(enemy=thisBattle, preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
                    advance12[1] += 4
                    if reportDroppedItem(enemy=thisBattle, drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
                        thunderCount[1] += 1
            if len(dropChances[2]) >= 1:
                if trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10):
                    finalItem, advance13[2] = itemToBeDropped(enemy=thisBattle, preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
                    advance12[2] += 4
                    if reportDroppedItem(enemy=thisBattle, drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
                        thunderCount[2] += 1
            advance10 += 3
        advance01 += 1
    battleFormations = comingBattles(area="machina_2", battleCount=1, extraAdvances=advance01)
    for x in range(len(battleFormations)):
        for i in range(len(battleFormations[x])):
            thisBattle = battleFormations[x]
            dropChances = trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10)
            if len(dropChances[0]) >= 1:
                if trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10):
                    finalItem, advance13[0] = itemToBeDropped(enemy=thisBattle, preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
                    advance12[0] += 4
                    if reportDroppedItem(enemy=thisBattle, drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
                        thunderCount[0] += 1
            if len(dropChances[1]) >= 1:
                if trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10):
                    finalItem, advance13[1] = itemToBeDropped(enemy=thisBattle, preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
                    advance12[1] += 4
                    if reportDroppedItem(enemy=thisBattle, drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
                        thunderCount[1] += 1
            if len(dropChances[2]) >= 1:
                if trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10):
                    finalItem, advance13[2] = itemToBeDropped(enemy=thisBattle, preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
                    advance12[2] += 4
                    if reportDroppedItem(enemy=thisBattle, drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
                        thunderCount[2] += 1
            advance10 += 3
        advance01 += 1
    battleFormations = comingBattles(area="machina_3", battleCount=1, extraAdvances=advance01)
    for x in range(len(battleFormations)):
        for i in range(len(battleFormations[x])):
            thisBattle = battleFormations[x]
            dropChances = trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10)
            if len(dropChances[0]) >= 1:
                if trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10):
                    finalItem, advance13[0] = itemToBeDropped(enemy=thisBattle, preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
                    advance12[0] += 4
                    if reportDroppedItem(enemy=thisBattle, drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
                        thunderCount[0] += 1
            if len(dropChances[1]) >= 1:
                if trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10):
                    finalItem, advance13[1] = itemToBeDropped(enemy=thisBattle, preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
                    advance12[1] += 4
                    if reportDroppedItem(enemy=thisBattle, drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
                        thunderCount[1] += 1
            if len(dropChances[2]) >= 1:
                if trackDrops(enemy=thisBattle, battles=1, extraAdvances=advance10):
                    finalItem, advance13[2] = itemToBeDropped(enemy=thisBattle, preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
                    advance12[2] += 4
                    if reportDroppedItem(enemy=thisBattle, drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
                        thunderCount[2] += 1
            advance10 += 3
        advance01 += 1
    
    #Finally, Oblitz is guaranteed to drop an item.
    finalItem, advance13[0] = itemToBeDropped(enemy="oblitzerator", preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
    if reportDroppedItem(enemy="Oblitzerator", drop=finalItem, prefType=0, prefAbility=0x8026, report=report):
        thunderCount[0] += 1
        oblitzWeap[0] = True
    finalItem, advance13[1] = itemToBeDropped(enemy="oblitzerator", preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
    if reportDroppedItem(enemy="Oblitzerator", drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8026, report=report):
        thunderCount[1] += 1
        oblitzWeap[1] = True
    finalItem, advance13[2] = itemToBeDropped(enemy="oblitzerator", preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
    if reportDroppedItem(enemy="Oblitzerator", drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8026, report=report):
        thunderCount[2] += 1
        oblitzWeap[2] = True
    advance12[0] += 4
    advance10 += 3
    
    FFX_Logs.writeRNGTrack("End: thunder strike drops")
    FFX_Logs.writeRNGTrack("===================")
    FFX_Logs.writeRNGTrack("The following values are per advance.")
    FFX_Logs.writeRNGTrack("Drops possible:"+str(thunderCount))
    FFX_Logs.writeRNGTrack("Weapon drops on Oblitzerator:"+str(oblitzWeap))
    FFX_Logs.writeRNGTrack("Kill Yellow ele on Kilika battles:"+str(killYellow))
    return thunderCount, killYellow

def zombieTrack(report=False):
    advance01 = 0
    advance10 = 0
    advance12 = [0]*3
    advance13 = [0]*3
    zombieResults = [99]*3
    partySize=7
    
    # "sanctuary_keeper"
    # Check random encounters for best charge, plan for 1 encounter, 1 death if possible to charge.
    # "spectral_keeper"
    # "yunalesca"
    
    enemy="sanctuary_keeper"
    dropChances = trackDrops(enemy=enemy, battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(enemy=enemy, preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0, prefAbility=0x8032, report=report)
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(enemy=enemy, preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8032, report=report)
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(enemy=enemy, preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8032, report=report)
    advance10 += 3
    advance01 += 1
    
    import FFX_Zanarkand
    FFX_Zanarkand.decideNEA(bonusAdvance=1)
    if gameVars.getNEAzone() in [1,2]: #One death expected to recharge Rikku. No drops expected.
        advance10 += 3
        advance01 += 1
        
    enemy="spectral_keeper"
    dropChances = trackDrops(enemy=enemy, battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(enemy=enemy, preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0, prefAbility=0x8032, report=report)
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(enemy=enemy, preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8032, report=report)
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(enemy=enemy, preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8032, report=report)
    advance10 += 3
    advance01 += 1
    
    enemy="yunalesca"
    dropChances = trackDrops(enemy=enemy, battles=1, extraAdvances=advance10)
    if len(dropChances[0]) >= 1:
        finalItem, advance13[0] = itemToBeDropped(enemy=enemy, preAdvance12=advance12[0], preAdvance13=advance13[0], partySize=partySize)
        advance12[0] += 4
        if reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0, prefAbility=0x8032, report=report):
            zombieResults[0] = finalItem.equipOwnerAlt
    if len(dropChances[1]) >= 1:
        finalItem, advance13[1] = itemToBeDropped(enemy=enemy, preAdvance12=advance12[1], preAdvance13=advance13[1], partySize=partySize)
        advance12[1] += 4
        if reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0, needAdv=1, prefAbility=0x8032, report=report):
            zombieResults[1] = finalItem.equipOwnerAlt
    if len(dropChances[2]) >= 1:
        finalItem, advance13[2] = itemToBeDropped(enemy=enemy, preAdvance12=advance12[2], preAdvance13=advance13[2], partySize=partySize)
        advance12[2] += 4
        if reportDroppedItem(enemy=enemy, drop=finalItem, prefType=0, needAdv=2, prefAbility=0x8032, report=report):
            zombieResults[2] = finalItem.equipOwnerAlt
    advance10 += 3
    advance01 += 1
    
    return zombieResults

def nextActionEscape(character:int=0):
    index = 20 + character
    escapeRoll = FFX_memory.s32(FFX_memory.rngArrayFromIndex(index=index, arrayLen=1)[1]) & 255
    return escapeRoll < 191

def nextActionHitMiss(character:int=0, enemy:str="anima"):
    print("=========================")
    print("Checking hit chance - character:", character)
    #Need more work on this. There are a lot of variables we still need from memory.
    #Character info, get these from memory
    index = 36 + character
    hit_rng = FFX_memory.rngArrayFromIndex(index=index)[1]
    luck = FFX_memory.charLuck(character) #Need this out of memory
    print("Luck:", luck)
    accuracy = FFX_memory.charAccuracy(character) #Need this out of memory
    print("Accuracy:", accuracy)
    
    #Data directly from the tracker
    target_luck = MONSTERS[enemy].stats['Luck']
    print("Enemy luck:", target_luck)
    target_evasion = MONSTERS[enemy].stats['Evasion']
    print("Enemy evasion:", target_evasion)
    
    #Unused, but technically part of the formula
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
    print("Hit results:", hit_chance > (FFX_memory.s32(hit_rng) % 101))
    print("=========================")
    return hit_chance > (FFX_memory.s32(hit_rng) % 101)

def hitChanceTable(index:int):
    if index == 0:
        return 25
    elif index in [1,2]:
        return 30
    elif index in [3,4]:
        return 40
    elif index in [5,6]:
        return 50
    elif index == 7:
        return 80
    elif index == 8:
        return 100
