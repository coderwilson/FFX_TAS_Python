from dataclasses import dataclass, field

from ..data.actions import Action
from ..data.characters import CharacterState
from ..data.constants import ICV_BASE, Stat
from ..data.monsters import Monster
from .main import Event


@dataclass
class MonsterAction(Event):
    monster: Monster
    action: Action
    slot: int
    targets: list[CharacterState] = field(init=False, repr=False)
    hits: list[bool] = field(init=False, repr=False)
    damages: list[int] = field(init=False, repr=False)
    damage_rngs: list[int] = field(init=False, repr=False)
    crits: list[bool] = field(init=False, repr=False)
    ctb: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.targets = self._get_targets()
        self.hits = self._get_hits()
        self.damages, self.damage_rngs, self.crits = self._get_damages()
        self.ctb = self._get_ctb()

    def __str__(self) -> str:
        actions = []
        for target, hit, dmg, rng, crit in zip(self.targets, self.hits,
                                               self.damages, self.damage_rngs,
                                               self.crits):
            string = f'{target.name} ->'
            if hit:
                if self.action.does_damage:
                    string += f' [{rng}/31]'
                    # string += f' {dmg}'
                    if crit:
                        string += ' (Crit)'
                else:
                    string += ' (No damage)'
            else:
                string += ' Miss'
            actions.append(string)
        string = (f'{self.monster.name} M{self.slot + 1} -> '
                  f'{self.action.name} [{self.ctb}]: '
                  f'{", ".join(actions)}')
        return string

    def _get_hits(self) -> list[bool]:
        index = min(44 + self.slot, 51)
        luck = max(self.monster.stats[Stat.LUCK], 1)
        # unused for now
        aims = 0
        hits = []
        for target in self.targets:
            if not self.action.can_miss:
                hits.append(True)
                continue
            hit_rng = self._advance_rng(index) % 101
            target_evasion = target.stats[Stat.EVASION]
            target_luck = max(target.stats[Stat.LUCK], 1)
            # unused for now
            target_reflexes = 0
            hit_chance = (self.action.accuracy
                          - target_evasion
                          + luck
                          - target_luck
                          + ((aims - target_reflexes) * 10))
            hits.append(hit_chance > hit_rng)
        return hits

    def _get_damages(self) -> tuple[list[int], list[int], list[bool]]:
        index = min(28 + self.slot, 35)
        luck = self.monster.stats[Stat.LUCK]
        damages = []
        damage_rngs = []
        crits = []
        for target, hit in zip(self.targets, self.hits):
            if not hit or not self.action.does_damage:
                damages.append(0)
                damage_rngs.append(0)
                crits.append(False)
                continue
            damages.append(0)
            damage_rngs.append(self._advance_rng(index) & 31)
            if not self.action.can_crit:
                crits.append(False)
                continue
            crit_roll = self._advance_rng(index) % 101
            target_luck = max(target.stats[Stat.LUCK], 1)
            crit_chance = luck - target_luck
            # crit_chance += self.action.bonus_crit
            crits.append(crit_roll < crit_chance)
        return damages, damage_rngs, crits

    def _get_possible_targets(self) -> list[CharacterState]:
        targets = []
        for character in self.gamestate.party[:3]:
            targets.append(self.gamestate.characters[character.name.lower()])
        return targets

    def _get_targets(self) -> list[CharacterState]:
        targets = []
        possible_targets = self._get_possible_targets()
        if self.action.multitarget:
            if self.action.random_targeting:
                # random targeting actions roll rng4 once
                self._advance_rng(4)
                for _ in range(self.action.hits):
                    if len(possible_targets) <= 1:
                        targets.append(possible_targets[0])
                    else:
                        target_rng = self._advance_rng(5)
                        target_index = target_rng % len(possible_targets)
                        targets.append(possible_targets[target_index])
                return targets
            else:
                return possible_targets
        if len(possible_targets) <= 1:
            return possible_targets * self.action.hits

        target_rng = self._advance_rng(4)
        target_index = target_rng % len(possible_targets)
        for _ in range(self.action.hits):
            targets.append(possible_targets[target_index])
        return targets

    def _get_ctb(self) -> int:
        rank = self.action.rank
        ctb_base = ICV_BASE[self.monster.stats[Stat.AGILITY]]
        return ctb_base * rank
