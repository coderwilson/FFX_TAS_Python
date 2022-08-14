from dataclasses import dataclass, field

from ..data.characters import CHARACTERS, Character
from ..data.constants import EquipmentSlots, EquipmentType, Rarity
from ..data.equipment import Equipment, EquipmentDrop
from ..data.items import ItemDrop
from ..data.monsters import Monster
from .main import Event


@dataclass
class Kill(Event):
    monster: Monster
    killer: Character
    overkill: bool = False
    item_1: ItemDrop | None = field(init=False, repr=False)
    item_2: ItemDrop | None = field(init=False, repr=False)
    equipment: EquipmentDrop | None = field(init=False, repr=False)
    equipment_index: int | None = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.item_1 = self._get_item_1()
        self.item_2 = self._get_item_2()
        self.equipment = self._get_equipment()
        self.equipment_index = self._get_equipment_index()

    def __str__(self) -> str:
        string = f'{self.monster.name} drops: '
        drops = []
        if self.item_1:
            drops.append(str(self.item_1))
        if self.item_2:
            drops.append(str(self.item_2))
        if self.equipment:
            drops.append(f'Equipment #{self.equipment_index} '
                         f'{str(self.equipment)}')
        if len(drops):
            string += ', '.join(drops)
        else:
            string += 'No drops'
        return string

    def _get_item_1(self) -> ItemDrop | None:
        rng_drop = self._advance_rng(10) % 255
        if self.overkill:
            drop_type = 'overkill'
        else:
            drop_type = 'normal'
        if self.monster.item_1['drop_chance'] > rng_drop:
            rng_rarity = self._advance_rng(11) & 255
            if rng_rarity < 32:
                return self.monster.item_1[drop_type][Rarity.RARE]
            else:
                return self.monster.item_1[drop_type][Rarity.COMMON]

    def _get_item_2(self) -> ItemDrop | None:
        rng_drop = self._advance_rng(10) % 255
        if self.overkill:
            drop_type = 'overkill'
        else:
            drop_type = 'normal'
        if self.monster.item_2['drop_chance'] > rng_drop:
            rng_rarity = self._advance_rng(11) & 255
            if rng_rarity < 32:
                return self.monster.item_2[drop_type][Rarity.RARE]
            else:
                return self.monster.item_2[drop_type][Rarity.COMMON]

    def _get_equipment(self) -> EquipmentDrop | None:
        """Returns equipment obtained from killing a monster
        at the current rng position and advances rng accordingly.
        """
        rng_equipment_drop = self._advance_rng(10) % 255
        if self.monster.equipment['drop_chance'] <= rng_equipment_drop:
            return

        characters_enabled = self.gamestate.party
        equipment_owner_base = len(characters_enabled)
        rng_equipment_owner = self._advance_rng(12)

        # check if killing with a party member
        # always gives the equipment to that character
        killer_is_owner_test = rng_equipment_owner % (equipment_owner_base + 3)
        if killer_is_owner_test >= equipment_owner_base:
            killer_is_owner = True
        else:
            killer_is_owner = False

        # if the killer is a party member (0-6)
        # it gives them a bonus chance for the equipment to be theirs
        if self.killer.index < 7:
            owner = self.killer
            equipment_owner_base += 3

        rng_equipment_owner = rng_equipment_owner % equipment_owner_base
        number_of_enabled_party_members = 0

        # get equipment owner
        characters = tuple(CHARACTERS.values())[:7]
        for character in characters:
            if character in characters_enabled:
                number_of_enabled_party_members += 1
                if rng_equipment_owner < number_of_enabled_party_members:
                    owner = character
                    break

        # get equipment type
        rng_weapon_or_armor = self._advance_rng(12) & 1
        if rng_weapon_or_armor == 0:
            type_ = EquipmentType.WEAPON
        else:
            type_ = EquipmentType.ARMOR

        # get number of slots
        rng_number_of_slots = self._advance_rng(12) & 7
        slots_mod = (self.monster.equipment['slots_modifier']
                     + rng_number_of_slots
                     - 4)
        number_of_slots = (slots_mod + ((slots_mod >> 31) & 3)) >> 2
        if number_of_slots > EquipmentSlots.MAX:
            number_of_slots = EquipmentSlots.MAX.value
        elif number_of_slots < EquipmentSlots.MIN:
            number_of_slots = EquipmentSlots.MIN.value

        # get number of abilities
        rng_number_of_abilities = self._advance_rng(12) & 7
        abilities_mod = (self.monster.equipment['max_ability_rolls_modifier']
                         + rng_number_of_abilities
                         - 4)
        number_of_abilities = ((abilities_mod + ((abilities_mod >> 31) & 7))
                               >> 3)

        ability_arrays = self.monster.equipment['ability_arrays']
        ability_array = ability_arrays[owner.name][type_]

        abilities = []

        # the first ability of the array is usually None, but for kimahri's
        # and auron's weapons and for drops from specific enemies it exists
        forced_ability = ability_array[0]
        if number_of_slots != 0 and forced_ability:
            abilities.append(forced_ability)

        for _ in range(number_of_abilities):
            # if all the slots are filled break
            if len(abilities) >= number_of_slots:
                break
            rng_ability_index = self._advance_rng(13) % 7 + 1
            ability = ability_array[rng_ability_index]
            # if the ability is not null and not a duplicate add it
            if ability and ability not in abilities:
                abilities.append(ability)

        # other equipment information
        base_weapon_damage = self.monster.equipment['base_weapon_damage']
        bonus_crit = self.monster.equipment['bonus_critical_chance']

        equipment = Equipment(
            owner=owner,
            type_=type_,
            slots=number_of_slots,
            abilities=tuple(abilities),
            base_weapon_damage=base_weapon_damage,
            bonus_crit=bonus_crit,
        )
        equipment_drop = EquipmentDrop(
            equipment=equipment,
            killer=self.killer,
            monster=self.monster,
            killer_is_owner=killer_is_owner,
        )

        return equipment_drop

    def _get_equipment_index(self) -> int | None:
        if not self.equipment:
            return None
        self.gamestate.equipment_drops += 1
        return self.gamestate.equipment_drops


@dataclass
class Bribe(Kill):

    def _get_item_1(self) -> ItemDrop | None:
        return self.monster.bribe['item']

    def _get_item_2(self) -> None:
        return
