from players.base import Aeon


class MagusSistersImpl(Aeon):
    def _menu_order(self, unique):
        return [36, 38, unique, 86]

    def do_as_you_will(self):
        self.navigate_to_battle_menu(36)
        battle.utils.tap_targeting()

    def fight(self):
        self.navigate_to_battle_menu(38)
        battle.utils.tap_targeting()

    def unique(self):
        self.navigate_to_battle_menu(self.battle_menu[2])
        battle.utils.tap_targeting()

    def dismiss(self):
        self.navigate_to_battle_menu(86)
        battle.utils.tap_targeting()

    def shield(self):
        raise NotImplementedError()

    def boost(self):
        raise NotImplementedError()


class CindyImpl(MagusSistersImpl):
    def __init__(self):
        super().__init__("Cindy", 15, [])
        self.battle_menu = self._menu_order(40)


class SandyImpl(MagusSistersImpl):
    def __init__(self):
        super().__init__("Cindy", 16, [])
        self.battle_menu = self._menu_order(42)


class MindyImpl(MagusSistersImpl):
    def __init__(self):
        super().__init__("Mindy", 17, [])
        self.battle_menu = self._menu_order(41)


Cindy = CindyImpl()
Sandy = SandyImpl()
Mindy = MindyImpl()
