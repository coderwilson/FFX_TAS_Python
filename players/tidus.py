import players
import memory
import battles

class TidusImpl(players.base.Player):
    
    def __init__(self):
        super().__init__("Tidus", 0, [0, 19, 20, 22, 1])
        
    def overdrive(self, *args, **kwargs):
        return battles.overdrive.tidus(*args, **kwargs)
        
    def overdrive_active(self):
        return memory.main.read_val(0x00F3D6F4, 1) == 4
        
Tidus = TidusImpl()