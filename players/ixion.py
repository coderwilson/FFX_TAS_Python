from players.base import Aeon


class IxionImpl(Aeon):
    def __init__(self):
        super().__init__("Ixion", 10, [210, 211, 21, 22])


Ixion = IxionImpl()
