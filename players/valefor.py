from players.base import Aeon


class ValeforImpl(Aeon):
    def __init__(self):
        super().__init__("Valefor", 8, [203, 204, 21])

    def overdrive(self, overdrive_num, sin_fin=False):
        while not memory.main.other_battle_menu():
            xbox.tap_right()
        battle.utils._navigate_to_single_column_index(
            target, memory.main.battle_cursor_2
        )
        if sin_fin:
            while memory.main.other_battle_menu():
                xbox.tap_b()
            xbox.tap_down()
            xbox.tap_left()
        battle.utils.tap_targeting()


Valefor = ValeforImpl()
