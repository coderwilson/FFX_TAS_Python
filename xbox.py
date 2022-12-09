import json
import logging
import math
import time

import vgamepad as vg

import memory.get
import memory.main
import vars

logger = logging.getLogger(__name__)

game_vars = vars.vars_handle()


class VgTranslator:
    def __init__(self):
        self.gamepad = vg.VX360Gamepad()

    def set_value(self, x_key, value):
        # Buttons, pressing
        if x_key == "btn_back" and value == 1:
            self.gamepad.press_button(button=0x0020)
        elif x_key == "btn_start" and value == 1:
            self.gamepad.press_button(button=0x0010)
        elif x_key == "btn_a" and value == 1:
            self.gamepad.press_button(button=0x2000)
        elif x_key == "btn_b" and value == 1:
            self.gamepad.press_button(button=0x1000)
        elif x_key == "btn_x" and value == 1:
            self.gamepad.press_button(button=0x4000)
        elif x_key == "btn_y" and value == 1:
            self.gamepad.press_button(button=0x8000)
        elif x_key == "btn_shoulder_l" and value == 1:
            self.gamepad.press_button(button=0x0100)
        elif x_key == "btn_shoulder_r" and value == 1:
            self.gamepad.press_button(button=0x0200)
        elif x_key == "d_pad" and value == 1:  # d_pad up
            self.gamepad.press_button(button=0x0001)
        elif x_key == "d_pad" and value == 2:  # d_pad down
            self.gamepad.press_button(button=0x0002)
        elif x_key == "d_pad" and value == 4:  # d_pad left
            self.gamepad.press_button(button=0x0004)
        elif x_key == "d_pad" and value == 8:  # d_pad right
            self.gamepad.press_button(button=0x0008)
        elif x_key == "trigger_l" and value == 1:
            self.gamepad.left_trigger_float(value_float=1.0)
        elif x_key == "trigger_r" and value == 1:
            self.gamepad.right_trigger_float(value_float=1.0)

        # Buttons, releasing
        elif x_key == "btn_back" and value == 0:
            self.gamepad.release_button(button=0x0020)
        elif x_key == "btn_start" and value == 0:
            self.gamepad.release_button(button=0x0010)
        elif x_key == "btn_a" and value == 0:
            self.gamepad.release_button(button=0x2000)
        elif x_key == "btn_b" and value == 0:
            self.gamepad.release_button(button=0x1000)
        elif x_key == "btn_x" and value == 0:
            self.gamepad.release_button(button=0x4000)
        elif x_key == "btn_y" and value == 0:
            self.gamepad.release_button(button=0x8000)
        elif x_key == "btn_shoulder_l" and value == 0:
            self.gamepad.release_button(button=0x0100)
        elif x_key == "btn_shoulder_r" and value == 0:
            self.gamepad.release_button(button=0x0200)
        elif x_key == "d_pad" and value == 0:
            self.gamepad.release_button(button=0x0001)
            self.gamepad.release_button(button=0x0002)
            self.gamepad.release_button(button=0x0004)
            self.gamepad.release_button(button=0x0008)
        elif x_key == "trigger_l" and value == 0:
            self.gamepad.left_trigger_float(value_float=0.0)
        elif x_key == "trigger_r" and value == 0:
            self.gamepad.right_trigger_float(value_float=0.0)

        # Error states
        elif x_key == "axis_lx" or x_key == "axis_ly":
            logger.error("ERROR - OLD MOVEMENT COMMAND FOUND")
            logger.error(f"ERROR - {x_key}")
            logger.error("ERROR - OLD MOVEMENT COMMAND FOUND")
            self.set_neutral()

        self.gamepad.update()
        # For additional details, review this website:
        # https://pypi.org/project/vgamepad/

    def set_movement(self, x, y):
        if x > 1:
            x = 1
        if x < -1:
            x = -1
        if y > 1:
            y = 1
        if y < -1:
            y = -1

        try:
            self.gamepad.left_joystick_float(x_value_float=x, y_value_float=y)
            self.gamepad.update()
        except Exception:
            pass

    def set_neutral(self):
        self.gamepad.reset()
        self.gamepad.update()


FFXC = VgTranslator()


def controller_handle():
    return FFXC


processed_cutscenes = set()


def skip_scene(fast_mode: bool = False):
    cutscene_id = memory.get.cutscene_id()
    logger.info(f"Cutscene ID: {cutscene_id}")
    if not fast_mode or cutscene_id not in processed_cutscenes:
        logger.info("Skip cutscene")
        memory.main.wait_frames(2)
        FFXC.set_value("btn_start", 1)  # Generate button to skip
        memory.main.wait_frames(1)
        FFXC.set_value("btn_start", 0)
        memory.main.wait_frames(2)
        tap_x()
        processed_cutscenes.add(cutscene_id)
    if not fast_mode:
        memory.main.wait_frames(60)


def skip_scene_spec():
    logger.debug("Skip cutscene and store an additional skip for a future scene")
    FFXC.set_value("btn_start", 1)  # Generate button to skip
    memory.main.wait_frames(2)
    FFXC.set_value("btn_start", 0)
    memory.main.wait_frames(3)
    FFXC.set_value("btn_x", 1)  # Perform the skip
    memory.main.wait_frames(1)
    FFXC.set_value("btn_x", 0)
    # Before despawn, regenerate the button for use in a future scene.
    FFXC.set_value("btn_start", 1)
    memory.main.wait_frames(1)
    FFXC.set_value("btn_start", 0)
    memory.main.wait_frames(4)


def skip_stored_scene(skip_timer: int = 3):
    logger.debug("Mashing skip button")
    current_time = time.time()
    logger.debug(f"Current Time: {current_time}")
    click_timer = current_time + skip_timer
    logger.debug(f"Click Until: {click_timer}")
    while current_time < click_timer:
        FFXC.set_value("btn_x", 1)  # Perform the skip
        memory.main.wait_frames(30 * 0.035)
        FFXC.set_value("btn_x", 0)
        memory.main.wait_frames(30 * 0.035)
        current_time = time.time()
    logger.debug("Mashing skip button - Complete")


def attack():
    logger.debug("Basic attack")
    FFXC.set_value("btn_b", 1)
    memory.main.wait_frames(30 * 0.08)
    FFXC.set_value("btn_b", 0)
    memory.main.wait_frames(30 * 0.08)
    FFXC.set_value("btn_b", 1)
    memory.main.wait_frames(30 * 0.08)
    FFXC.set_value("btn_b", 0)
    memory.main.wait_frames(30 * 0.5)


def touch_save_sphere():
    FFXC.set_neutral()
    logger.debug("Touching the save sphere")
    while memory.main.user_control():
        tap_b()
        memory.main.wait_frames(3)
    memory.main.wait_frames(15)
    while not memory.main.user_control():
        if memory.main.menu_control():
            if not memory.main.save_menu_cursor():
                menu_a()
                memory.main.wait_frames(1)
            else:
                tap_b()
    FFXC.set_neutral()
    memory.main.wait_frames(30 * 0.035)


def skip_dialog(keystrokes):
    # 2 frames per button mash
    num_repetitions = math.ceil(round(keystrokes * 30) / 2)
    logger.debug(f"Mashing B {num_repetitions} times.")
    for _ in range(num_repetitions):
        tap_b()
    logger.debug("Mashing B - Complete")


def skip_dialog_special(keystrokes):
    num_repetitions = math.ceil(round(keystrokes * 30) / 2)
    logger.debug(f"Mashing A and B {num_repetitions} times.")
    for _ in range(num_repetitions):
        FFXC.set_value("btn_b", 1)
        FFXC.set_value("btn_a", 1)
        memory.main.wait_frames(1)
        FFXC.set_value("btn_b", 0)
        FFXC.set_value("btn_a", 0)
        memory.main.wait_frames(1)
    logger.debug("Mashing A and B - Complete")


def menu_up():
    FFXC.set_value("d_pad", 1)
    memory.main.wait_frames(2)
    FFXC.set_value("d_pad", 0)
    memory.main.wait_frames(3)


def menu_down():
    FFXC.set_value("d_pad", 2)
    memory.main.wait_frames(2)
    FFXC.set_value("d_pad", 0)
    memory.main.wait_frames(3)


def menu_left():
    FFXC.set_value("d_pad", 4)
    memory.main.wait_frames(2)
    FFXC.set_value("d_pad", 0)
    memory.main.wait_frames(3)


def menu_right():
    FFXC.set_value("d_pad", 8)
    memory.main.wait_frames(2)
    FFXC.set_value("d_pad", 0)
    memory.main.wait_frames(3)


def tap_up():
    FFXC.set_value("d_pad", 1)
    memory.main.wait_frames(1)
    FFXC.set_value("d_pad", 0)
    memory.main.wait_frames(1)
    if game_vars.use_pause():
        memory.main.wait_frames(2)


def tap_down():
    FFXC.set_value("d_pad", 2)
    memory.main.wait_frames(1)
    FFXC.set_value("d_pad", 0)
    memory.main.wait_frames(1)
    if game_vars.use_pause():
        memory.main.wait_frames(2)


def tap_left():
    FFXC.set_value("d_pad", 4)
    memory.main.wait_frames(1)
    FFXC.set_value("d_pad", 0)
    memory.main.wait_frames(1)
    if game_vars.use_pause():
        memory.main.wait_frames(2)


def tap_right():
    FFXC.set_value("d_pad", 8)
    memory.main.wait_frames(1)
    FFXC.set_value("d_pad", 0)
    memory.main.wait_frames(1)
    if game_vars.use_pause():
        memory.main.wait_frames(2)


def shoulder_left():
    FFXC.set_value("btn_shoulder_l", 1)
    memory.main.wait_frames(2)
    FFXC.set_value("btn_shoulder_l", 0)
    memory.main.wait_frames(2)
    if game_vars.use_pause():
        memory.main.wait_frames(2)


def shoulder_right():
    FFXC.set_value("btn_shoulder_r", 1)
    memory.main.wait_frames(2)
    FFXC.set_value("btn_shoulder_r", 0)
    memory.main.wait_frames(2)
    if game_vars.use_pause():
        memory.main.wait_frames(2)


def menu_a():
    FFXC.set_value("btn_a", 1)
    memory.main.wait_frames(2)
    FFXC.set_value("btn_a", 0)
    memory.main.wait_frames(4)


def menu_b():
    FFXC.set_value("btn_b", 1)
    memory.main.wait_frames(2)
    FFXC.set_value("btn_b", 0)
    memory.main.wait_frames(4)


def tap_a():
    FFXC.set_value("btn_a", 1)
    memory.main.wait_frames(1)
    FFXC.set_value("btn_a", 0)
    memory.main.wait_frames(1)
    if game_vars.use_pause():
        memory.main.wait_frames(2)


def tap_b():
    FFXC.set_value("btn_b", 1)
    memory.main.wait_frames(1)
    FFXC.set_value("btn_b", 0)
    memory.main.wait_frames(1)
    if game_vars.use_pause():
        memory.main.wait_frames(3)


def menu_x():
    FFXC.set_value("btn_x", 1)
    memory.main.wait_frames(2)
    FFXC.set_value("btn_x", 0)
    memory.main.wait_frames(4)


def menu_y():
    FFXC.set_value("btn_y", 1)
    memory.main.wait_frames(2)
    FFXC.set_value("btn_y", 0)
    memory.main.wait_frames(4)


def tap_x():
    FFXC.set_value("btn_x", 1)
    memory.main.wait_frames(2)
    FFXC.set_value("btn_x", 0)
    memory.main.wait_frames(1)
    if game_vars.use_pause():
        memory.main.wait_frames(2)


def tap_y():
    FFXC.set_value("btn_y", 1)
    memory.main.wait_frames(1)
    FFXC.set_value("btn_y", 0)
    memory.main.wait_frames(1)
    if game_vars.use_pause():
        memory.main.wait_frames(2)


def menu_back():
    FFXC.set_value("btn_back", 1)
    memory.main.wait_frames(2)
    FFXC.set_value("btn_back", 0)
    memory.main.wait_frames(2)


def l_bumper():
    FFXC.set_value("btn_shoulder_l", 1)
    memory.main.wait_frames(1)
    FFXC.set_value("btn_shoulder_l", 0)
    memory.main.wait_frames(1)
    if game_vars.use_pause():
        memory.main.wait_frames(2)


def trigger_l():
    FFXC.set_value("trigger_l", 1)
    memory.main.wait_frames(2)
    FFXC.set_value("trigger_l", 0)
    memory.main.wait_frames(2)
    if game_vars.use_pause():
        memory.main.wait_frames(2)


def trigger_r():
    FFXC.set_value("trigger_r", 1)
    memory.main.wait_frames(2)
    FFXC.set_value("trigger_r", 0)
    memory.main.wait_frames(2)
    if game_vars.use_pause():
        memory.main.wait_frames(2)


def tap_start():
    FFXC.set_value("btn_start", 1)  # Generate button to skip
    memory.main.wait_frames(1)
    FFXC.set_value("btn_start", 0)
    memory.main.wait_frames(2)


def weap_swap(position):
    logger.info(f"Weapon swap, weapon in position: {position}")
    while memory.main.main_battle_menu():
        tap_right()
    while memory.main.other_battle_menu():
        tap_b()
    while memory.main.battle_cursor_3() != position:
        tap_down()
    while memory.main.interior_battle_menu():
        tap_b()


def armor_swap(position):
    logger.info(f"Armor swap, armor in position: {position}")
    menu_right()
    memory.main.wait_frames(30 * 0.5)
    menu_down()
    memory.main.wait_frames(30 * 0.5)
    menu_b()
    memory.main.wait_frames(30 * 0.7)
    armor = 0
    while armor < position:
        menu_down()
        armor += 1
    menu_b()
    menu_b()
    memory.main.wait_frames(30 * 0.3)


def clear_save_popup(click_to_diag_num=0):
    FFXC = controller_handle()
    FFXC.set_neutral()
    memory.main.click_to_diag_progress(click_to_diag_num)
    complete = 0
    counter = 0
    while complete == 0:
        counter += 1
        if counter % 100 == 0:
            logger.debug(f"Waiting for Save dialog: {counter / 100}")

        if (
            memory.main.diag_progress_flag() != click_to_diag_num
            and memory.main.diag_skip_possible()  # Was diag_skip_possible(True), seems to have been refactored
        ):
            tap_b()

        elif memory.main.diag_skip_possible():
            if memory.main.save_popup_cursor() == 0:
                menu_up()
            else:
                menu_b()
                complete = 1
    memory.main.wait_frames(5)


def await_save(index=0):
    clear_save_popup(click_to_diag_num=index)


def grid_up():
    FFXC.set_value("d_pad", 1)
    memory.main.wait_frames(30 * 0.04)
    FFXC.set_value("d_pad", 0)
    memory.main.wait_frames(30 * 0.12)


def grid_down():
    FFXC.set_value("d_pad", 2)
    memory.main.wait_frames(30 * 0.04)
    FFXC.set_value("d_pad", 0)
    memory.main.wait_frames(30 * 0.12)


def grid_left():
    FFXC.set_value("d_pad", 4)
    memory.main.wait_frames(30 * 0.04)
    FFXC.set_value("d_pad", 0)
    memory.main.wait_frames(30 * 0.12)


def grid_right():
    FFXC.set_value("d_pad", 8)
    memory.main.wait_frames(30 * 0.04)
    FFXC.set_value("d_pad", 0)
    memory.main.wait_frames(30 * 0.12)


def click_to_battle():
    logger.debug("Mashing A until first turn in battle")
    FFXC.set_neutral()
    while not (memory.main.battle_active() and memory.main.turn_ready()):
        if memory.main.user_control():
            break
        elif (
            not memory.main.battle_active()
            and not memory.main.auditory_dialog_playing()
        ):
            tap_b()
        elif memory.main.diag_skip_possible():
            tap_b()


character_mapping = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    "I": 8,
    "J": 9,
    "K": 10,
    "L": 11,
    "M": 12,
    "N": 13,
    "O": 14,
    "P": 15,
    "Q": 16,
    "R": 17,
    "S": 18,
    "T": 19,
    "U": 20,
    "V": 21,
    "W": 22,
    "X": 23,
    "Y": 24,
    "Z": 25,
    " ": 26,
    "a": 30,
    "b": 31,
    "c": 32,
    "d": 33,
    "e": 34,
    "f": 35,
    "g": 36,
    "h": 37,
    "i": 38,
    "j": 39,
    "k": 40,
    "l": 41,
    "m": 42,
    "n": 43,
    "o": 44,
    "p": 45,
    "q": 46,
    "r": 47,
    "s": 48,
    "t": 49,
    "u": 50,
    "v": 51,
    "w": 52,
    "x": 53,
    "y": 54,
    "z": 55,
    "1": 60,
    "2": 61,
    "3": 62,
    "4": 63,
    "5": 64,
    "6": 65,
    "7": 66,
    "8": 67,
    "9": 68,
    "0": 69,
    "!": 70,
    "?": 71,
    '"': 72,
    "+": 73,
    "-": 74,
    "*": 75,
    "/": 76,
    "%": 77,
    "&": 78,
    "=": 79,
    ".": 80,
    ",": 81,
    ":": 82,
    ";": 83,
    "[": 85,
    "]": 86,
    "(": 87,
    ")": 88,
}


def navigate_to_character(cur_character):
    position_target = character_mapping[cur_character]
    while position_target != memory.main.get_naming_index():
        if position_target - memory.main.get_naming_index() >= 15:
            tap_down()
        elif memory.main.get_naming_index() - position_target >= 15:
            tap_up()
        elif memory.main.get_naming_index() < position_target:
            tap_right()
        elif memory.main.get_naming_index() > position_target:
            tap_left()


def name_aeon(character=""):
    logger.info("Waiting for aeon naming screen")

    while not memory.main.name_aeon_ready():
        if memory.main.diag_skip_possible() or memory.main.menu_open():
            tap_b()
    if character:
        with open("character_names.json") as fp:
            custom_name = json.load(fp)[character]
        if custom_name:
            custom_name = custom_name[:8]
            while memory.main.get_naming_menu():
                tap_right()
            while memory.main.name_has_characters():
                tap_a()
            for cur_character in custom_name:
                navigate_to_character(cur_character)
                tap_b()

    logger.info("Naming screen is up.")
    while memory.main.equip_sell_row() != 1:
        tap_start()
    while memory.main.equip_sell_row() != 0:
        tap_up()
    while memory.main.name_confirm_open():
        tap_b()
