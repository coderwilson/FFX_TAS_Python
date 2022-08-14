import math
from dataclasses import dataclass, field

from ..configs import Configs
from ..data.actions import YOJIMBO_ACTIONS, YojimboAction
from ..data.constants import (COMPATIBILITY_MODIFIER, GIL_MOTIVATION_MODIFIER,
                              OVERDRIVE_MOTIVATION, ZANMATO_LEVELS)
from ..data.monsters import Monster
from .main import Event


@dataclass
class YojimboTurn(Event):
    action: YojimboAction
    monster: Monster
    overdrive: bool = False
    is_attack_free: bool = field(init=False, repr=False)
    gil: int = field(init=False, repr=False)
    compatibility: int = field(init=False, repr=False)
    motivation: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.is_attack_free = self._free_attack_check()
        if self.is_attack_free:
            self.gil = 0
            self.action, self.motivation = self._get_free_attack()
        elif self.action.needed_motivation is not None:
            self.gil, self.motivation = self._get_gil()
        else:
            self.gil = 0
            self.motivation = 0
        self.compatibility = self._update_compatibility()

    def __str__(self) -> str:
        if self.is_attack_free:
            cost = 'free'
        else:
            cost = f'{self.gil} gil'
        string = (f'{self.action.name} -> {self.monster}: '
                  f'{cost} [{self.motivation}/{self.action.needed_motivation}'
                  f' motivation][{self.compatibility}/255 compatibility]')
        return string

    def _free_attack_check(self) -> bool:
        rng = self._advance_rng(17) & 255
        compatibility = self.gamestate.compatibility // 4
        return compatibility > rng

    def _get_free_attack(self) -> tuple[YojimboAction, int]:
        base_motivation = self.gamestate.compatibility // 4
        rng = self._advance_rng(17) & 0x3f
        motivation = base_motivation + rng
        attacks = [a for a in YOJIMBO_ACTIONS.values()
                   if a.needed_motivation is not None]
        attacks.sort(key=lambda a: a.needed_motivation)
        for a in attacks:
            if motivation >= a.needed_motivation:
                attack = a

        if (attack == YOJIMBO_ACTIONS['zanmato']
                and self.monster.zanmato_level > 0):
            attack = YOJIMBO_ACTIONS['wakizashi_mt']
        return attack, motivation

    def _get_gil(self) -> tuple[int, int]:
        """"""
        base_motivation = (self.gamestate.compatibility
                           // COMPATIBILITY_MODIFIER[Configs.game_version])
        zanmato_resistance = ZANMATO_LEVELS[self.monster.zanmato_level]
        rng_motivation = self._advance_rng(17) & 0x3f
        # the zanmato level of the monster is only used to check for zanmato
        # if the desired attack is not zanmato then a second calculation is
        # made using the lowest zanmato level
        if (self.action != YOJIMBO_ACTIONS['zanmato']
                and self.monster.zanmato_level > 0):
            zanmato_resistance = ZANMATO_LEVELS[0]
            rng_motivation = self._advance_rng(17) & 0x3f
        fixed_motivation = int(base_motivation * zanmato_resistance)
        fixed_motivation += rng_motivation
        if self.overdrive:
            fixed_motivation += OVERDRIVE_MOTIVATION[Configs.game_version]

        motivation = fixed_motivation
        gil = 1
        while motivation < self.action.needed_motivation:
            gil = gil * 2
            gil_motivation = self.gil_to_motivation(gil)
            gil_motivation = int(gil_motivation * zanmato_resistance)
            motivation = fixed_motivation + gil_motivation
        return gil, motivation

    def _update_compatibility(self) -> int:
        modifier = self.action.compatibility_modifier
        self.gamestate.compatibility += modifier
        return self.gamestate.compatibility

    @staticmethod
    def gil_to_motivation(gil: int) -> int:
        modifier = GIL_MOTIVATION_MODIFIER[Configs.game_version]
        motivation = int(math.log(gil / modifier, 2)) * modifier
        return max(motivation, 0)
