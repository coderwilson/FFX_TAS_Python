import logging

import battle
import memory
import xbox
from players.base import Player

logger = logging.getLogger(__name__)


class RikkuImp(Player):
    def __init__(self):
        super().__init__("Rikku", 6, [0, 20, 1])

    def rikku_od_items(self, slot):
        battle.utils._navigate_to_position(
            slot, battle_cursor=memory.main.rikku_od_cursor_1
        )

    def overdrive(battle):
        # First, determine which items we are using
        if battle == "tutorial":
            item1 = memory.main.get_item_slot(73)
            logger.debug(f"Ability sphere in slot: {item1}")
            item2 = item1
        elif battle == "Evrae":
            if game_vars.skip_kilika_luck():
                item1 = memory.main.get_item_slot(81)
                logger.debug(f"Lv1 sphere in slot: {item1}")
                item2 = memory.main.get_item_slot(84)
                logger.debug(f"Lv4 sphere in slot: {item2}")
            else:
                item1 = memory.main.get_item_slot(94)
                logger.debug(f"Luck sphere in slot: {item1}")
                item2 = memory.main.get_item_slot(100)
                logger.debug(f"Map in slot: {item2}")
        elif battle == "Flux":
            item1 = memory.main.get_item_slot(35)
            logger.debug(f"Grenade in slot: {item1}")
            item2 = memory.main.get_item_slot(85)
            logger.debug(f"HP Sphere in slot: {item2}")
        elif battle == "trio":
            item1 = 108
            item2 = 108
            logger.debug(f"Wings are in slot: {item1}")
        elif battle == "crawler":
            item1 = memory.main.get_item_slot(30)
            logger.debug(f"Lightning Marble in slot: {item1}")
            item2 = memory.main.get_item_slot(85)
            logger.debug(f"Mdef Sphere in slot: {item2}")
        elif battle == "spherimorph1":
            item1 = memory.main.get_item_slot(24)
            logger.debug(f"Arctic Wind in slot: {item1}")
            item2 = memory.main.get_item_slot(90)
            logger.debug(f"Mag Def Sphere in slot: {item2}")
        elif battle == "spherimorph2":
            item1 = memory.main.get_item_slot(32)
            logger.debug(f"Fish Scale in slot: {item1}")
            item2 = memory.main.get_item_slot(90)
            logger.debug(f"Mag Sphere in slot: {item2}")
        elif battle == "spherimorph3":
            item1 = memory.main.get_item_slot(30)
            logger.debug(f"Lightning Marble in slot: {item1}")
            item2 = memory.main.get_item_slot(90)
            logger.debug(f"Mag Sphere in slot: {item2}")
        elif battle == "spherimorph4":
            item1 = memory.main.get_item_slot(27)
            logger.debug(f"Bomb Core in slot: {item1}")
            item2 = memory.main.get_item_slot(90)
            logger.debug(f"Mag Sphere in slot: {item2}")
        elif battle == "bfa":
            item1 = memory.main.get_item_slot(35)
            logger.debug(f"Grenade in slot: {item1}")
            item2 = memory.main.get_item_slot(85)
            logger.debug(f"HP Sphere in slot: {item2}")
        elif battle == "shinryu":
            item1 = memory.main.get_item_slot(109)
            logger.debug(f"Gambler's Spirit in slot: {item1}")
            item2 = memory.main.get_item_slot(58)
            logger.debug(f"Star Curtain in slot: {item2}")
        elif battle == "omnis":
            both_items = omnis_items()
            logger.debug("Omnis items, many possible combinations.")
            item1 = memory.main.get_item_slot(both_items[0])
            item2 = memory.main.get_item_slot(both_items[1])

        if item1 > item2:
            item3 = item1
            item1 = item2
            item2 = item3

        # Now to enter commands

        while not memory.main.other_battle_menu():
            xbox.tap_left()

        while not memory.main.interior_battle_menu():
            xbox.tap_b()

        self.rikku_od_items(item1)

        while not memory.main.rikku_overdrive_item_selected_number():
            xbox.tap_b()

        self.rikku_od_items(item2)

        while memory.main.interior_battle_menu():
            xbox.tap_b()

        battle.utils.tap_targeting()


Rikku = RikkuImp()
