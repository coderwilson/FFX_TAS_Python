import battle.main
import memory.main
import screen
import xbox
import logging

FFXC = xbox.controller_handle()

od_log = logging.getLogger('battle.OD')

def auron(style="dragon fang"):
    while not memory.main.other_battle_menu():
        xbox.tap_left()
    while not memory.main.interior_battle_menu():
        xbox.tap_b()
    od_log.info(f"Auron overdrive. Style: {style}")
    # Doing the actual overdrive
    if style == "dragon fang":
        battle.main._navigate_to_position(0, battle_cursor=memory.main.battle_cursor_3)
        while not memory.main.auron_overdrive_active():
            xbox.tap_b()
        od_log.debug("Starting")
        for i in range(2):  # Do it twice in case there's a miss on the first one.
            FFXC.set_value("Dpad", 2)  # down
            memory.main.wait_frames(1)
            FFXC.set_value("Dpad", 0)
            FFXC.set_value("Dpad", 4)  # left
            memory.main.wait_frames(1)
            FFXC.set_value("Dpad", 0)
            FFXC.set_value("Dpad", 1)  # up
            memory.main.wait_frames(1)
            FFXC.set_value("Dpad", 0)
            FFXC.set_value("Dpad", 8)  # right
            memory.main.wait_frames(1)
            FFXC.set_value("Dpad", 0)
            FFXC.set_value("BtnShoulderL", 1)
            memory.main.wait_frames(1)
            FFXC.set_value("BtnShoulderL", 0)
            FFXC.set_value("BtnShoulderR", 1)
            memory.main.wait_frames(1)
            FFXC.set_value("BtnShoulderR", 0)
            FFXC.set_value("BtnA", 1)
            memory.main.wait_frames(1)
            FFXC.set_value("BtnA", 0)
            FFXC.set_value("BtnB", 1)
            memory.main.wait_frames(1)
            FFXC.set_value("BtnB", 0)
    elif style == "shooting star":
        battle.main._navigate_to_position(1, battle_cursor=memory.main.battle_cursor_3)
        while not memory.main.auron_overdrive_active():
            xbox.tap_b()
        for i in range(2):  # Do it twice in case there's a miss on the first one.
            FFXC.set_value("BtnY", 1)
            memory.main.wait_frames(1)
            FFXC.set_value("BtnY", 0)
            FFXC.set_value("BtnA", 1)
            memory.main.wait_frames(1)
            FFXC.set_value("BtnA", 0)
            FFXC.set_value("BtnX", 1)
            memory.main.wait_frames(1)
            FFXC.set_value("BtnX", 0)
            FFXC.set_value("BtnB", 1)
            memory.main.wait_frames(1)
            FFXC.set_value("BtnB", 0)
            FFXC.set_value("Dpad", 4)  # left
            memory.main.wait_frames(1)
            FFXC.set_value("Dpad", 0)
            FFXC.set_value("Dpad", 8)  # right
            memory.main.wait_frames(1)
            FFXC.set_value("Dpad", 0)
            FFXC.set_value("BtnB", 1)
            memory.main.wait_frames(1)
            FFXC.set_value("BtnB", 0)


def kimahri(pos):
    od_log.info(f"Kimahri using Overdrive, pos - {pos}")
    while not memory.main.other_battle_menu():
        xbox.tap_left()
    while memory.main.other_battle_menu():
        xbox.tap_b()
    battle.main._navigate_to_position(pos, battle_cursor=memory.main.battle_cursor_3)
    while memory.main.interior_battle_menu():
        xbox.tap_b()
    battle.main.tap_targeting()


def tidus(direction=None, version: int = 0, character=99):
    od_log.info("Tidus overdrive activating")
    while not memory.main.other_battle_menu():
        xbox.tap_left()
    while not memory.main.interior_battle_menu():
        xbox.tap_b()
    if version == 1:
        memory.main.wait_frames(6)
        xbox.menu_right()
    while memory.main.interior_battle_menu():
        xbox.tap_b()
    if character != 99 and memory.main.get_enemy_current_hp()[character - 20] != 0:
        while (
            character != memory.main.battle_target_id()
            and memory.main.get_enemy_current_hp()[character - 20] != 0
        ):
            xbox.tap_left()
    elif direction:
        if direction == "left":
            xbox.tap_left()

    while not memory.main.overdrive_menu_active():
        xbox.tap_b()
    memory.main.wait_frames(12)
    od_log.info("Hit Overdrive")
    xbox.tap_b()  # First try pog
    memory.main.wait_frames(8)
    xbox.tap_b()  # Extra attempt in case of miss
    memory.main.wait_frames(9)
    xbox.tap_b()  # Extra attempt in case of miss
    memory.main.wait_frames(10)
    xbox.tap_b()  # Extra attempt in case of miss
    memory.main.wait_frames(11)
    xbox.tap_b()  # Extra attempt in case of miss
    memory.main.wait_frames(12)
    xbox.tap_b()  # Extra attempt in case of miss


def valefor(sin_fin=0, version=0):
    memory.main.wait_frames(6)
    while memory.main.main_battle_menu():
        xbox.tap_left()
    od_log.info(f"Valefor Overdrive: {version}")
    if version == 1:
        while memory.main.battle_cursor_2() != 1:
            xbox.tap_down()
    while memory.main.other_battle_menu():
        xbox.tap_b()  # Energy Blast
    if sin_fin == 1:
        xbox.tap_down()
        xbox.tap_left()
    battle.main.tap_targeting()


def wakka():
    od_log.info("Wakka overdrive activating")
    while not memory.main.other_battle_menu():
        xbox.tap_left()
    while not memory.main.interior_battle_menu():
        xbox.tap_b()
    while memory.main.interior_battle_menu():
        xbox.tap_b()

    memory.main.wait_frames(1)
    xbox.tap_b()

    while memory.main.overdrive_menu_active_wakka() == 0:
        pass
    memory.main.wait_frames(76)
    od_log.info("Hit Overdrive")
    xbox.tap_b()  # First reel
    memory.main.wait_frames(13)
    xbox.tap_b()  # Second reel
    memory.main.wait_frames(5)
    xbox.tap_b()  # Third reel


def yojimbo(gil_value: int = 263000):
    od_log.info("Yojimbo overdrive")
    screen.await_turn()
    if not screen.turn_aeon():
        return
    while memory.main.battle_menu_cursor() != 35:
        xbox.tap_up()
    memory.main.wait_frames(6)
    xbox.menu_b()
    od_log.info("Selecting amount")
    memory.main.wait_frames(15)
    xbox.tap_left()
    xbox.tap_left()
    xbox.tap_left()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_left()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_left()
    xbox.tap_up()
    xbox.tap_up()
    od_log.info("Amount selected")
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    return


def yuna(aeon_num: int = 5):
    od_log.info(f"Summoning Aeon {aeon_num}. Awaiting Yunas turn")
    while not screen.turn_yuna():
        if memory.main.turn_ready():
            battle.main.defend()
    while not memory.main.other_battle_menu():
        xbox.tap_left()
    while not memory.main.interior_battle_menu():
        xbox.tap_b()
    while not memory.main.battle_cursor_3() == aeon_num:
        if aeon_num > memory.main.battle_cursor_3():
            xbox.tap_down()
        else:
            xbox.tap_up()
        memory.main.wait_frames(2)
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
