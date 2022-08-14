import csv
import os
from typing import Iterable

from ..configs import Configs
from ..errors import InvalidDamageValueError, SeedNotFoundError
from ..tracker import FFXRNGTracker
from ..utils import s32
from .constants import GameVersion


def get_seed(damage_values: Iterable[int]) -> int:
    damage_values_needed = DAMAGE_VALUES_NEEDED[Configs.game_version]
    if len(damage_values) < damage_values_needed:
        raise SeedNotFoundError(
            f'Need at least {damage_values_needed} damage values')
    damage_values = damage_values[:damage_values_needed]

    indexes = []
    for i, damage_value in enumerate(damage_values):
        if i in (0, 2, 4) or i >= 6:
            character = 'auron'
        else:
            character = 'tidus'
        try:
            index = _DAMAGE_VALUES[character].index(damage_value)
        except ValueError:
            if damage_value % 2 != 0:
                raise InvalidDamageValueError(
                    f'Invalid damage value for {character}: {damage_value}')
            try:
                index = _DAMAGE_VALUES[character].index(damage_value // 2) + 32
            except ValueError:
                raise InvalidDamageValueError(
                    f'Invalid damage value for {character}: {damage_value}')
        indexes.append(index)

    damage_indexes_as_string = ''.join([f'{n:02}' for n in indexes])

    if Configs.game_version is GameVersion.HD:
        absolute_file_path = _SEEDS_FILE_PATH
    else:
        absolute_file_path = _PS2_SEEDS_FILE_PATH
    with open(absolute_file_path) as file_object:
        seeds = csv.reader(file_object, delimiter=',')
        for line in seeds:
            if line[0].startswith(damage_indexes_as_string):
                break
        else:
            raise SeedNotFoundError('Seed not found')
        seed = int(line[1])
    return seed


def datetime_to_seed(datetime: int, frames: int) -> int:
    seed = s32((datetime + 1) * (s32(frames) + 1))
    seed = s32(s32(seed * 1108104919) + 11786)
    seed = s32(s32(seed * 1566083941) + 15413)
    seed = s32(s32(seed >> 16) + s32(seed << 16))
    if seed >= 0:
        return seed
    else:
        return 0x100000000 + seed


def make_seeds_file(file_path: str, frames: int) -> None:
    print('Calculating damage rolls for every possible seed'
          f' up to frame {frames}.')
    if os.path.exists(file_path):
        print(f'File {file_path} already exists!')
        return
    damage_rolls = []
    seeds = []
    rng_tracker = FFXRNGTracker(0)
    for frame in range(frames):
        print(f'\r{frame}/{frames}', end='')
        for date_time in range(256):
            seed = datetime_to_seed(date_time, frame)
            rng_tracker.__init__(seed)
            auron_rolls = [rng_tracker.advance_rng(22) for _ in range(37)]
            tidus_rolls = [rng_tracker.advance_rng(20) for _ in range(7)]
            indexes = []
            # first encounter
            # get 3 damage rolls from auron and tidus
            for i in range(1, 6, 2):
                auron_damage_index = auron_rolls[i] & 31
                # if auron crits the sinscale
                if (auron_rolls[i + 1] % 101) < 22:
                    auron_damage_index += 32
                indexes.append(auron_damage_index)
                tidus_damage = _DAMAGE_VALUES['tidus'][tidus_rolls[i] & 31]
                tidus_damage_index = _DAMAGE_VALUES['tidus'].index(
                    tidus_damage)
                # if tidus crits the sinscale
                if (tidus_rolls[i + 1] % 101) < 23:
                    tidus_damage_index += 32
                indexes.append(tidus_damage_index)
            # second encounter after dragon fang
            # get 2 damage rolls from auron
            for i in range(32, 35, 2):
                auron_damage_index = auron_rolls[i] & 31
                # if auron crits ammes
                if (auron_rolls[i + 1] % 101) < 13:
                    auron_damage_index += 32
                indexes.append(auron_damage_index)
            damage_rolls.append(''.join([f'{n:02}' for n in indexes]))
            seeds.append(str(seed))
    print(f'\r{frames}/{frames}')
    data = '\n'.join([f'{d},{s}' for d, s in zip(damage_rolls, seeds)])
    with open(file_path, 'w') as file:
        file.write(data)
    print('Done!')


_DAMAGE_VALUES: dict[str, tuple[int]] = {
    'auron': (
        260, 261, 262, 263, 264, 266, 267, 268, 269, 270, 271,
        272, 273, 274, 275, 276, 278, 279, 280, 281, 282, 283,
        284, 285, 286, 287, 288, 289, 291, 292, 293, 294,
    ),
    'tidus': (
        125, 126, 126, 127, 127, 128, 128, 129, 129, 130, 130,
        131, 131, 132, 132, 133, 134, 134, 135, 135, 136, 136,
        137, 137, 138, 138, 139, 139, 140, 140, 141, 141,
    ),
}
FRAMES_FROM_BOOT = {
    GameVersion.PS2NA: 60 * 60 * Configs.ps2_seeds_minutes,
    GameVersion.HD: 1,
}
DAMAGE_VALUES_NEEDED = {
    GameVersion.PS2NA: 8,
    GameVersion.HD: 6,
}

_SEEDS_DIRECTORY_PATH = 'ffx_rng_tracker_seeds'
try:
    os.mkdir(_SEEDS_DIRECTORY_PATH)
except FileExistsError:
    pass

_SEEDS_FILE_PATH = _SEEDS_DIRECTORY_PATH + '/seeds.csv'
_PS2_SEEDS_FILE_PATH = _SEEDS_DIRECTORY_PATH + '/ps2_seeds.csv'

if not os.path.exists(_SEEDS_FILE_PATH):
    print('Seeds file not found.')
    make_seeds_file(_SEEDS_FILE_PATH, FRAMES_FROM_BOOT[GameVersion.HD])

if Configs.game_version is not GameVersion.HD:
    if not os.path.exists(_PS2_SEEDS_FILE_PATH):
        print('Seeds file for ps2 not found.')
        make_seeds_file(
            _PS2_SEEDS_FILE_PATH, FRAMES_FROM_BOOT[GameVersion.PS2NA])
