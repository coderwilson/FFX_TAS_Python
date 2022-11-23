from players.aeon import Aeon


class AnimaImpl(Aeon):
    def __init__(self):
        super().__init__("Anima", 13, [219, 220, 19, 21])


Anima = AnimaImpl()
