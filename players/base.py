import memory
from typing import List
import xbox
import logging

logger = logging.getLogger(__name__)


class Player():
    def __init__(self, name: str, id: int, battle_menu: List[int]):
        self.name = name
        self.id = id
        self.struct_offset = id * 0x94
        self.char_rng = 20 + id
        self.battle_menu = battle_menu
        

    def __eq__(self, other):
        if isinstance(other, int):
            return self.id == other
        else:
            return self.id == other.id
        
        
    def __str__(self) -> str:
        return self.name


    def _read_char_offset_address(self, address):
        return memory.main.read_val(address + self.struct_offset)
        

    def _read_char_battle_offset_address(self, address, offset):
        return memory.main.read_val(address + ((0x90 * offset)))
        
        
    def _read_char_battle_state_address(self, offset):
        pointer = memory.main.read_val(0x00D334CC, 4)
        new_offset = (0xF90 * self.id) + offset
        return memory.main.read_val(pointer + new_offset, 1, find_base=False)

        
    def _read_char_stat_offset_address(self, address):
        pointer = memory.main.read_val(0x003AB9B0, 4)
        return memory.main.read_val(pointer + self.struct_offset + address, 1, find_base=False)
        
    def navigate_to_battle_menu(self, target):
        """Different characters have different menu orders."""
        current_position = memory.main.battle_menu_cursor()
        target_position = self.battle_menu.index(target)
        while current_position != target:
            if self.battle_menu.index(current_position) > target_position:
                xbox.tap_up()
            else:
                xbox.tap_down()
            current_position = memory.main.battle_menu_cursor()
        
        
    def luck(self) -> int:
        return self._read_char_stat_offset_address(0x34)

        
    def accuracy(self) -> int:
        return self._read_char_stat_offset_address(0x36)
        
        
    def affection(self) -> int:
        if self.id == 0:
            return 255
        return memory.main.read_val(0x00D2CABC + ((4 * self.id)), 1)
        
        
    def next_crits(self, enemy_luck: int, length: int = 20) -> List[int]:
        """Note that this says the number of increments, so the previous roll will be a hit, and this one will be the crit."""
        results = []
        cur_rng = memory.main.rng_from_index(self.char_rng)
        cur_rng = memory.main.roll_next_rng(cur_rng, self.char_rng)
        cur_rng = memory.main.roll_next_rng(cur_rng, self.char_rng)
        index = 2
        while len(results) < length:            
            crit_roll = memory.main.s32(cur_rng & 0x7FFFFFFF ) % 101
            crit_chance = self.luck() - enemy_luck
            if crit_roll < crit_chance:
                results.append(index)
                index += 1
        return results
        

    def next_crit(self, enemy_luck) -> int:
        return self.next_crits()[0]
        

    def overdrive(self, *args, **kwargs):
        raise NotImplementedError()
        
    def overdrive_active(self):
        raise NotImplementedError()
        
    
    def overdrive_percent(self, combat = False) -> int:
        if combat:
            val = self._read_char_battle_state_address(0x5BC)
            return val
        else:
            pointer = memory.main.read_val(0x003AB9B0, 4)
            return memory.main.read_val(pointer + 0x39 + self.struct_offset, 1)
        
        
    def has_overdrive(self, combat = False) -> bool:
        return self.overdrive_percent(combat = combat) == 100


    def is_turn(self) -> bool:
        return memory.main.get_battle_char_turn() == self.id
        

    def in_danger(self, danger_threshold, combat = False) -> bool:
        return self.hp(combat) <= danger_threshold
        
    def is_dead(self) -> bool:
        return memory.main.state_dead(self.id)

    def is_status_ok(self) -> bool:
        if not self.active():
            return True
        return not any(
            func(self.id)
            for func in [
                memory.main.state_petrified,
                memory.main.state_confused,
                memory.main.state_dead,
                memory.main.state_berserk,
                memory.main.state_sleep,
            ]
        )
    
    
    def escaped(self) -> bool:
        return self._read_char_battle_state_address(0xDC8)
        
    
    def hp(self, combat = False) -> int:
        if not combat:
            return self._read_char_offset_address(0x00D32078)
        else:
            return self._read_char_battle_offset_address(0x00F3F7A4, self.battle_slot())
            

    def max_hp(self, combat = False) -> int:
        if not combat:
            return self._read_char_offset_address(0x00D32080)
        else:
            return self._read_char_battle_offset_address(0x00F3F7A8, self.battle_slot())
            

    def active(self) -> bool:
        return self in memory.main.get_active_battle_formation()
        

    def battle_slot(self) -> int:
        for i in range(0, 3):
            if memory.main.read_val(0x00F3F76C + (2*i)) == self.id:
                return i
                
        offset = 0
        for i in range(0, 7):
            val = memory.main.read_val(0x00D2C8A3 + i)
            if val == 255:
                offset += 1
                continue
            elif val == self.id:
                return i + 3 - offset
        return 255
        

    def formation_slot(self) -> int:
        try:
            return memory.main.get_order_seven().index(self.id)
        except Exception:
            return 255

        
    def slvl(self) -> int:
        return self._read_char_offset_address(0x00D32097)
    
    
    def armors(self) -> List[memory.main.Equipment]:
        equipments = memory.main.all_equipment()
        return [x for x in equipments if (x.owner() == self.id and x.equipment_type() == 1)]

    
    def equipped_armor(self) -> memory.main.Equipment:
        return [x for x in self.armors() if x.is_equipped()][0]
        
    def weapons(self) -> List[memory.main.Equipment]:
        equipments = memory.main.all_equipment()
        return [x for x in equipments if (x.owner() == self.id and x.equipment_type() == 0)]
        
    def equipped_weapon(self) -> memory.main.Equipment:
        return [x for x in self.weapons() if x.is_equipped()][0]
        
    def main_menu_index(self) -> int:
        return memory.main.get_character_index_in_main_menu(self.id)
                
        
    
        