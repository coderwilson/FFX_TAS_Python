import configparser
import os
import shutil
from dataclasses import dataclass

from .data.constants import GameVersion, SpeedrunCategory
from .data.file_functions import get_resource_path
from .utils import get_contrasting_color


@dataclass
class UIWidgetConfigs:
    shown: bool
    windowed: bool

    def __str__(self) -> str:
        return ' '.join([f'{v}: {k}' for v, k in vars(self).items()])


@dataclass
class Color:
    foreground: str
    background: str
    select_foreground: str
    select_background: str


class Configs:
    seed: int | None
    game_version: GameVersion
    ps2_seeds_minutes: int
    speedrun_category: SpeedrunCategory
    use_dark_mode: bool
    font_size: int
    use_theme: bool
    colors: dict[str, Color] = {}
    important_monsters: list[str]
    ui_widgets: dict[str, UIWidgetConfigs] = {}
    _parser = configparser.ConfigParser()
    _configs_file = 'ffx_rng_tracker_configs.ini'
    _default_configs_file = 'tracker\\data\\default_configs.ini'

    @classmethod
    def getboolean(cls, section: str, option: str, fallback: bool) -> bool:
        try:
            return cls._parser.getboolean(section, option, fallback=fallback)
        except ValueError:
            return fallback

    @classmethod
    def getint(cls, section: str, option: str, fallback: int) -> int:
        try:
            return cls._parser.getint(section, option, fallback=fallback)
        except ValueError:
            return fallback

    @classmethod
    def get(cls, section: str, option: str, fallback: str) -> str:
        return cls._parser.get(section, option, fallback=fallback)

    @classmethod
    def read(cls, file_path: str) -> None:
        cls._parser.read(file_path)

    @classmethod
    def load_configs(cls) -> None:
        section = 'General'
        seed = cls.getint(section, 'seed', None)
        if seed is not None and (0 <= seed <= 0xffffffff):
            cls.seed = seed
        else:
            cls.seed = None
        try:
            cls.game_version = GameVersion(
                cls.get(section, 'game version', 'HD'))
        except ValueError:
            cls.game_version = GameVersion.HD
        cls.ps2_seeds_minutes = cls.getint(section, 'ps2 seeds minutes', 3)
        try:
            cls.speedrun_category = SpeedrunCategory(
                cls.get(section, 'category', 'AnyPercent'))
        except ValueError:
            cls.speedrun_category = SpeedrunCategory.ANYPERCENT

        section = 'UI'
        cls.use_dark_mode = cls.getboolean(section, 'use dark mode', False)
        cls.font_size = cls.getint(section, 'fontsize', 9)
        cls.use_theme = cls.getboolean(section, 'use theme', True)

        section = 'Colors'
        options = (
            'preemptive', 'ambush', 'encounter', 'crit', 'stat update',
            'comment', 'advance rng', 'equipment', 'no encounters',
            'yojimbo low gil', 'yojimbo high gil', 'error', 'status miss',
            'important monster', 'captured monster',
        )
        if cls.use_dark_mode:
            default_fg = '#ffffff'
            default_bg = '#333333'
        else:
            default_fg = '#000000'
            default_bg = '#ffffff'
        for option in options:
            fg = cls.get(section, option, default_fg)
            if len(fg) == 7 and fg[0] == '#':
                try:
                    int(fg[1:], 16)
                except ValueError:
                    fg = default_fg
            else:
                fg = default_fg
            bg = cls.get(section, f'{option} background', default_bg)
            if len(bg) == 7 and bg[0] == '#':
                try:
                    int(bg[1:], 16)
                except ValueError:
                    bg = default_bg
            else:
                bg = default_bg

            if (fg, bg) == (default_fg, default_bg):
                select_fg, select_bg = fg, '#007fff'
            elif bg == default_bg:
                select_fg = fg
                select_bg = get_contrasting_color(fg)
            else:
                select_fg = fg
                select_bg = bg
            cls.colors[option] = Color(fg, bg, select_fg, select_bg)

        ui_widgets = (
            'Seed info', 'Drops', 'Encounters', 'Encounters Table',
            'Encounters Planner', 'Actions', 'Monster Targeting', 'Status',
            'Yojimbo', 'Monster Data', 'Seedfinder', 'Configs',
        )
        for section in ui_widgets:
            shown = cls.getboolean(section, 'shown', True)
            windowed = cls.getboolean(section, 'windowed', False)
            cls.ui_widgets[section] = UIWidgetConfigs(shown, windowed)

        section = 'Encounters'
        monsters = cls.get(section, 'monsters to highlight', 'ghost')
        cls.important_monsters = [m.strip() for m in monsters.split(',')]

    @classmethod
    def get_configs(cls) -> dict[str, str | int | bool]:
        configs = {}
        for attr in dir(cls):
            if not callable(getattr(cls, attr)) and not attr.startswith('_'):
                configs[attr] = getattr(cls, attr)
        return configs

    @classmethod
    def _init_configs(cls) -> None:
        if not os.path.exists(cls._configs_file):
            shutil.copyfile(
                get_resource_path(cls._default_configs_file),
                cls._configs_file)
        Configs.read(cls._configs_file)
        Configs.load_configs()


Configs._init_configs()
