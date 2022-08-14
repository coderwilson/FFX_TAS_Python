from dataclasses import dataclass, field

from ..data.actions import Action
from ..data.characters import CharacterState
from ..data.constants import (HIT_CHANCE_TABLE, ICV_BASE, DamageType,
                              ElementalAffinity, Stat)
from ..data.monsters import Monster
from .main import Event


@dataclass
class CharacterAction(Event):
    character: CharacterState
    action: Action
    target: CharacterState | Monster
    hit: bool = field(init=False, repr=False)
    damage: int = field(init=False, repr=False)
    damage_rng: int = field(init=False, repr=False)
    crit: bool = field(init=False, repr=False)
    ctb: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.hit = self._get_hit()
        self.damage, self.damage_rng, self.crit = self._get_damage()
        self.ctb = self._get_ctb()

    def __str__(self) -> str:
        string = (f'{self.character.name} -> {self.action.name}'
                  f' [{self.ctb}]'
                  f' -> {self.target.name}:')
        if self.hit:
            if self.action.does_damage:
                string += f' [{self.damage_rng}/31]'
                string += f' {self.damage}'
                if self.crit:
                    string += ' (Crit)'
            else:
                string += ' (No damage)'
        else:
            string += ' Miss'
        return string

    def _get_hit(self) -> bool:
        if not self.action.can_miss:
            return True
        index = min(36 + self.character.index, 43)
        hit_rng = self._advance_rng(index) % 101
        luck = self.character.stats[Stat.LUCK]
        accuracy = self.character.stats[Stat.ACCURACY]
        target_evasion = self.target.stats[Stat.EVASION]
        target_luck = max(self.target.stats[Stat.LUCK], 1)
        # unused for now
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
        hit_chance = HIT_CHANCE_TABLE[hit_chance_index] + luck
        hit_chance += (aims - target_reflexes) * 10 - target_luck
        return hit_chance > hit_rng

    def _get_crit(self) -> bool:
        if not self.action.can_crit:
            return False
        index = min(20 + self.character.index, 27)
        crit_roll = self._advance_rng(index) % 101
        luck = self.character.stats[Stat.LUCK]
        target_luck = max(self.target.stats[Stat.LUCK], 1)
        crit_chance = luck - target_luck
        if self.action.uses_bonus_crit:
            crit_chance += self.character.stats[Stat.BONUS_CRIT]
        return crit_roll < crit_chance

    def _get_damage(self) -> tuple[int, int, bool]:
        if not self.hit or not self.action.does_damage:
            return 0, 0, False
        index = min(20 + self.character.index, 27)
        damage_rng = self._advance_rng(index) & 31
        variance = damage_rng + 0xf0
        crit = self._get_crit()
        damage_type = self.action.damage_type
        if self.action.element:
            affinity = self.target.elemental_affinities[self.action.element]
            if affinity == ElementalAffinity.WEAK:
                element_mod = 1.5
            elif affinity == ElementalAffinity.RESISTS:
                element_mod = 0.5
            elif affinity == ElementalAffinity.IMMUNE:
                element_mod = 0
            else:
                element_mod = 1
        else:
            element_mod = 1

        # special cases where the damage formula
        # is a lot less complicated
        if damage_type == DamageType.ITEM:
            damage = self.action.base_damage * 50
            damage = damage * variance // 256
            if crit:
                damage = damage * 2
            damage = int(damage * element_mod)
            return damage, damage_rng, crit
        elif damage_type == DamageType.FIXED:
            damage = self.action.base_damage
            return damage, damage_rng, crit
        elif (damage_type is DamageType.PERCENTAGE_TOTAL
                or damage_type is DamageType.PERCENTAGE_CURRENT):
            damage = self.action.base_damage * 100 // 16
            return damage, damage_rng, crit
        elif damage_type == DamageType.HP:
            damage = self.character.stats[Stat.HP]
            damage = damage * self.action.base_damage // 100
            if crit:
                damage = int(damage * 2)
            return damage, damage_rng, crit
        elif damage_type == DamageType.GIL:
            damage = 0  # damage = gil/10
            return damage, damage_rng, crit

        # not many relevant instances of cheers or focuses on enemies
        # not used for now
        target_cheers = 0
        target_focuses = 0
        cheers = self.character.stats[Stat.CHEER]
        focuses = self.character.stats[Stat.FOCUS]
        if damage_type == DamageType.STRENGTH:
            if self.action.base_damage:
                base_damage = self.action.base_damage
            else:
                base_damage = self.character.stats[Stat.WEAPON_DAMAGE]
            defensive_buffs = target_cheers
            offensive_buffs = cheers
            offensive_stat = self.character.stats[Stat.STRENGTH]
            bonus = self.character.stats[Stat.BONUS_STRENGTH]
            defensive_stat = max(self.target.stats[Stat.DEFENSE], 1)
        elif damage_type in (DamageType.MAGIC, DamageType.SPECIAL_MAGIC,
                             DamageType.HEALING):
            base_damage = self.action.base_damage
            defensive_buffs = target_focuses
            offensive_buffs = focuses
            offensive_stat = self.character.stats[Stat.MAGIC]
            bonus = self.character.stats[Stat.BONUS_MAGIC]
            if self.action.damage_type == DamageType.MAGIC:
                defensive_stat = max(self.target.stats[Stat.MAGIC_DEFENSE], 1)
            else:
                defensive_stat = 0

        offensive_stat += offensive_buffs

        if damage_type in (DamageType.STRENGTH, DamageType.SPECIAL_MAGIC):
            power = offensive_stat * offensive_stat * offensive_stat
            power = (power // 0x20) + 0x1e
        elif damage_type == DamageType.MAGIC:
            power = offensive_stat * offensive_stat
            power = (power * 0x2AAAAAAB) // 0xffffffff
            power = power + (power // 0x80000000)
            power = (power + base_damage) * base_damage
            power = power // 4

        mitigation_1 = defensive_stat * defensive_stat
        mitigation_1 = (mitigation_1 * 0x2E8BA2E9) // 0xffffffff
        mitigation_1 = mitigation_1 // 2
        mitigation_1 = mitigation_1 + (mitigation_1 // 0x80000000)
        mitigation_2 = defensive_stat * 0x33
        mitigation = mitigation_2 - mitigation_1
        mitigation = (mitigation * 0x66666667) // 0xffffffff
        mitigation = mitigation // 4
        mitigation = mitigation + (mitigation // 0x80000000)
        mitigation = 0x2da - mitigation

        damage_1 = power * mitigation
        damage_2 = (damage_1 * -1282606671) // 0xffffffff
        damage_3 = damage_2 + damage_1
        damage_3 = damage_3 // 0x200
        damage_3 = damage_3 * (15 - defensive_buffs)
        damage_4 = (damage_3 * -2004318071) // 0xffffffff
        damage = (damage_4 + damage_3) // 0x8
        damage = damage + (damage // 0x80000000)
        if damage_type in (DamageType.STRENGTH, DamageType.SPECIAL_MAGIC):
            damage = damage * base_damage // 0x10
        damage = damage * variance // 0x100

        if crit:
            damage = damage * 2

        damage = damage * element_mod

        if (damage_type == DamageType.STRENGTH
                and isinstance(self.target, Monster)
                and self.target.armored
                and not self.character.stats[Stat.PIERCING]):
            damage = damage // 3

        damage = damage + (damage * bonus // 100)

        damage = int(damage)

        return damage, damage_rng, crit

    def _get_ctb(self) -> int:
        rank = self.action.rank
        ctb_base = ICV_BASE[self.character.stats[Stat.AGILITY]]
        return ctb_base * rank
