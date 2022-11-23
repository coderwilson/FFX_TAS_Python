from players.base import Aeon


class ShivaImpl(Aeon):
    def __init__(self):
        super().__init__("Shiva", 11, [213, 214, 21, 22])


Shiva = ShivaImpl()
