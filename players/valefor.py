from players.aeon import Aeon


class ValeforImpl(Aeon):
    def __init__(self):
        super().__init__("Valefor", 8, [203, 204, 21])

    def overdrive(self, overdrive_num, sin_fin=False):
        while not memory.main.other_battle_menu():
            xbox.tap_right()
        self._navigate_to_single_column_index(target, memory.main.battle_cursor_2)
        while memory.main.other_battle_menu():
            xbox.tap_b()
        if sin_fin:
            xbox.tap_down()
            xbox.tap_left()
        self._tap_targeting()


Valefor = ValeforImpl()
