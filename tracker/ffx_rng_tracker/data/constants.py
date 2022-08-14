from enum import Enum, IntEnum


class StringEnum(str, Enum):
    """Enum subclass that creates enumerated constants
    that are also subclasses of str.
    """

    def __str__(self) -> str:
        return str.__str__(self)


class EncounterCondition(StringEnum):
    PREEMPTIVE = 'Preemptive'
    NORMAL = 'Normal'
    AMBUSH = 'Ambush'


class EquipmentSlots(IntEnum):
    MIN = 1
    MAX = 4


class Element(StringEnum):
    FIRE = 'Fire'
    ICE = 'Ice'
    THUNDER = 'Thunder'
    WATER = 'Water'
    HOLY = 'Holy'


class ElementalAffinity(StringEnum):
    ABSORBS = 'Absorbs'
    IMMUNE = 'Immune'
    RESISTS = 'Resists'
    WEAK = 'Weak'
    NEUTRAL = 'Neutral'


class Status(StringEnum):
    DEATH = 'Death'
    ZOMBIE = 'Zombie'
    PETRIFY = 'Petrify'
    POISON = 'Poison'
    POWER_BREAK = 'Power Break'
    MAGIC_BREAK = 'Magic Break'
    ARMOR_BREAK = 'Armor Break'
    MENTAL_BREAK = 'Mental Break'
    CONFUSE = 'Confuse'
    BERSERK = 'Berserk'
    PROVOKE = 'Provoke'
    THREATEN = 'Threaten'
    SLEEP = 'Sleep'
    SILENCE = 'Silence'
    DARK = 'Dark'
    PROTECT = 'Protect'
    SHELL = 'Shell'
    REFLECT = 'Reflect'
    NULBLAZE = 'NulBlaze'
    NULFROST = 'NulFrost'
    NULSHOCK = 'NulShock'
    NULTIDE = 'NulTide'
    NULALL = 'Nulall'
    REGEN = 'Regen'
    HASTE = 'Haste'
    SLOW = 'Slow'


class Rarity(StringEnum):
    COMMON = 'Common'
    RARE = 'Rare'


class EquipmentType(StringEnum):
    WEAPON = 'Weapon'
    ARMOR = 'Armor'


class DamageType(StringEnum):
    HP = 'HP'
    STRENGTH = 'Strength'
    MAGIC = 'Magic'
    SPECIAL_MAGIC = 'Special Magic'
    ITEM = 'Item'
    FIXED = 'Fixed'
    PERCENTAGE_TOTAL = 'Percentage (Total)'
    PERCENTAGE_CURRENT = 'Percentage (Current)'
    HEALING = 'Healing'
    GIL = 'Gil'


class Stat(StringEnum):
    HP = 'HP'
    MP = 'MP'
    STRENGTH = 'Strength'
    DEFENSE = 'Defense'
    MAGIC = 'Magic'
    MAGIC_DEFENSE = 'Magic defense'
    AGILITY = 'Agility'
    LUCK = 'Luck'
    EVASION = 'Evasion'
    ACCURACY = 'Accuracy'
    WEAPON_DAMAGE = 'Weapon damage'
    BONUS_CRIT = 'Bonus crit'
    BONUS_STRENGTH = 'Bonus Strength'
    BONUS_MAGIC = 'Bonus Magic'
    PIERCING = 'Piercing'
    CHEER = 'Cheer'
    FOCUS = 'Focus'


class GameVersion(StringEnum):
    PS2NA = 'PS2 NA'
    HD = 'HD'


class SpeedrunCategory(StringEnum):
    ANYPERCENT = 'AnyPercent'
    BOOSTERS = 'Boosters'
    NSG = 'No Sphere Grid'
    NEMESIS = 'Nemesis'


HIT_CHANCE_TABLE = (25, 30, 30, 40, 40, 50, 60, 80, 100)

RNG_CONSTANTS_1 = (
    2100005341, 1700015771, 247163863, 891644838, 1352476256, 1563244181,
    1528068162, 511705468, 1739927914, 398147329, 1278224951, 20980264,
    1178761637, 802909981, 1130639188, 1599606659, 952700148, -898770777,
    -1097979074, -2013480859, -338768120, -625456464, -2049746478, -550389733,
    -5384772, -128808769, -1756029551, 1379661854, 904938180, -1209494558,
    -1676357703, -1287910319, 1653802906, 393811311, -824919740, 1837641861,
    946029195, 1248183957, -1684075875, -2108396259, -681826312, 1003979812,
    1607786269, -585334321, 1285195346, 1997056081, -106688232, 1881479866,
    476193932, 307456100, 1290745818, 162507240, -213809065, -1135977230,
    -1272305475, 1484222417, -1559875058, 1407627502, 1206176750, -1537348094,
    638891383, 581678511, 1164589165, -1436620514, 1412081670, -1538191350,
    -284976976, 706005400,
)

RNG_CONSTANTS_2 = (
    10259, 24563, 11177, 56952, 46197, 49826, 27077, 1257, 44164, 56565, 31009,
    46618, 64397, 46089, 58119, 13090, 19496, 47700, 21163, 16247, 574, 18658,
    60495, 42058, 40532, 13649, 8049, 25369, 9373, 48949, 23157, 32735, 29605,
    44013, 16623, 15090, 43767, 51346, 28485, 39192, 40085, 32893, 41400, 1267,
    15436, 33645, 37189, 58137, 16264, 59665, 53663, 11528, 37584, 18427,
    59827, 49457, 22922, 24212, 62787, 56241, 55318, 9625, 57622, 7580, 56469,
    49208, 41671, 36458,
)

ZANMATO_LEVELS = (0.8, 0.8, 0.8, 0.4, 0.4, 0.4)

ICV_BASE = (
    28, 28, 26, 24, 20, 16, 16, 15, 15, 15, 14, 14, 13, 13, 13, 12, 12, 11, 11,
    10, 10, 10, 10, 9, 9, 9, 9, 9, 9, 8, 8, 8, 8, 8, 8, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5,
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
    5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
    4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
)

ICV_VARIANCE = (
    0, 1, 1, 1, 1, 1, 2, 1, 2, 3, 1, 2, 1, 2, 3, 1, 2, 1, 2, 1, 2, 3, 4, 1, 2,
    3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 1, 2, 2, 3, 3,
    4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4,
    4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 1, 1,
    1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4,
    4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7,
    7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
    6, 6, 6, 6, 6, 6,
)

# Yojimbo-related constants
BASE_COMPATIBILITY = {
    GameVersion.PS2NA: 50,
    GameVersion.HD: 128,
}
COMPATIBILITY_MODIFIER = {
    GameVersion.PS2NA: 30,
    GameVersion.HD: 10,
}
OVERDRIVE_MOTIVATION = {
    GameVersion.PS2NA: 2,
    GameVersion.HD: 20,
}
GIL_MOTIVATION_MODIFIER = {
    GameVersion.PS2NA: 2,
    GameVersion.HD: 4,
}
