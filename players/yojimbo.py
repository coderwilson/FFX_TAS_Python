from players.base import Aeon


class YojimboImpl(Aeon):
    def __init__(self):
        super().__init__("Yojimbo", 14, [35, 87])

    def dismiss(self):
        self.navigate_to_battle_menu(87)
        battle.utils.tap_targeting()

    def shield(self):
        raise NotImplementedError()

    def boost(self):
        raise NotImplementedError()

    def unique(self):
        raise NotImplementedError()


Yojimbo = YojimboImpl()
