from players.aeon import Aeon


class BahamutImpl(Aeon):
    def __init__(self):
        super().__init__("Bahamut", 12, [216, 217, 21])


Bahamut = BahamutImpl()
