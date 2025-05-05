from players.aeon import Aeon
import memory.main
import battle.main
import screen
import xbox
import logging
logger = logging.getLogger(__name__)


class YojimboImpl(Aeon):
    def __init__(self):
        super().__init__("Yojimbo", 14, [35, 87])

    def dismiss(self):
        self.navigate_to_battle_menu(87)
        self._tap_targeting()

    def shield(self):
        raise NotImplementedError()

    def boost(self):
        raise NotImplementedError()

    def unique(self):
        raise NotImplementedError()
    
    def payment_movement(self, gil_amount):
        position = {}
        gil_copy = gil_amount
        for index in range(0, 7):
            amount = battle.main.get_digit(gil_amount, index)
            #if gil_copy * 10 > memory.main.get_gil_value():
            #    if amount > 5:
            #        gil_amount += 10 ** (index + 1)
            position[index] = amount
        logger.debug(f"Amt1: {gil_amount} | Amt2: {amount} | Copy: {gil_copy}")
        logger.debug(position)

        #for cur in range(6, -1, -1):
        for cur in range(7):
            if not position[cur]:
                continue
            while memory.main.spare_change_cursor() != cur:
                while memory.main.spare_change_cursor() != cur:
                    # memory.main.side_to_side_direction(
                    #     memory.main.spare_change_cursor(), cur, 6
                    # )
                    xbox.tap_left()
                memory.main.wait_frames(2)
            target = position[cur]
            while battle.main.get_digit(memory.main.spare_change_amount(), cur) != target:
                #if target > 5:
                #    xbox.tap_down()
                #else:
                xbox.tap_up()
            if memory.main.spare_change_amount() == gil_copy:
                return
        return

    def pay(self,gil_value):
        logger.info(f"Paying Yojimbo: {gil_value}")
        if not screen.turn_aeon():
            return
        while not memory.main.other_battle_menu():
            while memory.main.battle_menu_cursor() != 35:
                xbox.menu_up()
            memory.main.wait_frames(3)
            xbox.menu_b()
        logger.info("Selecting amount")
        memory.main.wait_frames(15)
        self.payment_movement(gil_value)
        logger.info(f"Amount selected: {gil_value}")
        xbox.tap_b()
        xbox.tap_b()
        xbox.tap_b()
        xbox.menu_b()
        xbox.menu_b()
        return


Yojimbo = YojimboImpl()
