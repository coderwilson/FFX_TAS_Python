
class GameState:
    def __init__(self):
        self.state = "none"
        self.step = 1
        self.rng_seed_num = 160
        self.start_time = 0

# Global
_game = GameState()

def get_gamestate():
    return _game
