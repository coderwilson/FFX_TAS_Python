from players.base import Aeon


class IfritImpl(Aeon):
    def __init__(self):
        super().__init__("Ifrit", 9, [207, 208, 21, 22])


Ifrit = IfritImpl()
