import ctypes
import ctypes.wintypes
import logging
import os.path
import struct
import time
from collections import Counter
from math import cos, sin, copysign, sqrt
from typing import List

from ReadWriteMemory import Process, ReadWriteMemory, ReadWriteMemoryError
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

import logs
import pathing
import vars
import xbox

logger = logging.getLogger(__name__)

game_vars = vars.vars_handle()
FFXC = xbox.controller_handle()

# Process Permissions
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020

MAX_PATH = 260

base_value = 0


class LocProcess(Process):
    def __init__(self, *args, **kwargs):
        super(LocProcess, self).__init__(*args, **kwargs)

    def read_bytes(self, lp_base_address: int, size: int = 4):
        # See the original ReadWriteMemory values for details on how this works.
        # This version allows us to pass the number of bytes to be retrieved instead
        # of a static 4-byte size. Default is 4 for reverse-compatibility
        try:
            read_buffer = ctypes.c_uint()
            lp_buffer = ctypes.byref(read_buffer)
            lp_number_of_bytes_read = ctypes.c_ulong(0)
            ctypes.windll.kernel32.ReadProcessMemory(
                self.handle, lp_base_address, lp_buffer, size, lp_number_of_bytes_read
            )
            return read_buffer.value
        except (BufferError, ValueError, TypeError) as error:
            if self.handle:
                self.close()
            self.error_code = self.get_last_error()
            error = {
                "msg": str(error),
                "Handle": self.handle,
                "PID": self.pid,
                "Name": self.name,
                "ErrorCode": self.error_code,
            }
            ReadWriteMemoryError(error)

    def write_bytes(self, lp_base_address: int, value: int, size: int = 4) -> bool:
        # Same as above, write a passed number of bytes instead of static 4 bytes.
        # Default is 4 for reverse-compatibility
        try:
            write_buffer = ctypes.c_uint(value)
            lp_buffer = ctypes.byref(write_buffer)
            lp_number_of_bytes_written = ctypes.c_ulong(0)
            ctypes.windll.kernel32.WriteProcessMemory(
                self.handle,
                lp_base_address,
                lp_buffer,
                size,
                lp_number_of_bytes_written,
            )
            return True
        except (BufferError, ValueError, TypeError) as error:
            if self.handle:
                self.close()
            self.error_code = self.get_last_error()
            error = {
                "msg": str(error),
                "Handle": self.handle,
                "PID": self.pid,
                "Name": self.name,
                "ErrorCode": self.error_code,
            }
            # ReadWriteMemoryError(error)


class FFXMemory(ReadWriteMemory):
    def __init__(self, *args, **kwargs):
        super(FFXMemory, self).__init__(*args, **kwargs)
        self.process = LocProcess()

    def get_process_by_name(self, process_name: str | bytes) -> "Process":
        """
        :description:
        Get the process by the process executabe\'s name and return a Process object.

        :param process_name:
        The name of the executable file for
        the specified process for example, my_program.exe.

        :return: A Process object containing the information from the requested Process.
        """
        if not process_name.endswith(".exe"):
            self.process.name = process_name + ".exe"

        process_ids = self.enumerate_processes()

        for process_id in process_ids:
            self.process.handle = ctypes.windll.kernel32.OpenProcess(
                PROCESS_QUERY_INFORMATION, False, process_id
            )
            if self.process.handle:
                image_file_name = (ctypes.c_char * MAX_PATH)()
                if (
                    ctypes.windll.psapi.GetProcessImageFileNameA(
                        self.process.handle, image_file_name, MAX_PATH
                    )
                    > 0
                ):
                    filename = os.path.basename(image_file_name.value)
                    if filename.decode("utf-8") == process_name:
                        self.process.pid = process_id
                        self.process.name = process_name
                        return self.process
                self.process.close()

        raise ReadWriteMemoryError(f'Process "{self.process.name}" not found!')


def start():
    global process
    global x_ptr
    global y_ptr
    global coords_counter
    coords_counter = 0
    success = False

    # rwm = ReadWriteMemory()
    rwm = FFXMemory()
    logger.info(type(rwm))
    process = rwm.get_process_by_name("FFX.exe")
    logger.info(type(process))
    process.open()

    global base_value
    try:
        import root_mem

        logger.info("Process Modules:")
        base_value = root_mem.list_process_modules(process.pid)
        logger.info("Process Modules complete")
        logger.info(f"Dynamically determined memory address: {hex(base_value)}")
        success = True
    except Exception as err_code:
        logger.error(
            f"Could not get memory address dynamically. Error code: {err_code}"
        )
        base_value = 0x00FF0000
        time.sleep(10)
    return success


def float_from_integer(integer):
    return struct.unpack("!f", struct.pack("!I", integer))[0]


def check_near_actors(wait_results:bool = False, max_dist = 200, super_coords:bool=False):
    count = 0
    for i in range(get_actor_array_size()):
        if get_actor_id(i) != 52685 and pathing.distance(i,use_super_coords=super_coords) < max_dist:
            logger.debug(f"Actor {i}: {get_actor_id(i)}, {pathing.distance(i,use_super_coords=super_coords)}")
            count += 1
    if wait_results:
        FFXC.set_neutral()
        wait_frames(300)


def check_near_actors_print(wait_results:bool = False, max_dist = 200, super_coords:bool=False):
    print("========== TEST ==========")
    count = 0
    for i in range(get_actor_array_size()):
        if get_actor_id(i) != 52685 and pathing.distance(i,use_super_coords=super_coords) < max_dist:
            print(f"Actor {i}: {get_actor_id(i)}, {pathing.distance(i,use_super_coords=super_coords)}")
            count += 1
    if wait_results:
        FFXC.set_neutral()
        wait_frames(300)
        
    print("==========================")
    print(" ")


def check_moving_actors():
    FFXC.set_neutral()
    wait_frames(12)
    
    all_coords = {}  # Use a dictionary to store actor coordinates
    count = 0  # Initialize count

    # First loop: Initialize with actors not equal to 52685
    for i in range(get_actor_array_size()):
        if get_actor_id(i) != 52685:
            all_coords[i] = get_actor_coords(i)  # Store coords by index
            # logger.debug(f"Actor {i}: {get_actor_id(i)}, {pathing.distance(i)}")

    wait_frames(9)

    # Second loop: Check for movement based on keys in all_coords
    for i in all_coords.keys():
        if all_coords[i] != get_actor_coords(i):  # Compare stored coords to current coords
            logger.debug(f"Actor movement {i}: {get_actor_id(i)}, {all_coords[i]}")

def wait_frames(frames: int):
    frames = max(round(frames), 1)
    global base_value
    key = base_value + 0x0088FDD8
    current = process.read_bytes(key, 4)
    final = current + frames
    previous = current - 1
    while current < final:
        if not (current == previous or current == previous + 1):
            final = final - previous
        previous = current
        current = process.read_bytes(key, 4)
    return


def wait_seconds(i:int):
    logger.debug(f"Wait function, initialize for {i} seconds.")
    while i > 0:
        logger.debug(f"Wait seconds: {i}")
        i -= 1
        wait_frames(30)
    logger.debug(f"Wait function end")


def rng_seed():
    if int(game_vars.confirmed_seed()) == 999:
        global base_value
        key = base_value + 0x003988A5
        return process.read_bytes(key, 1)
    return int(game_vars.confirmed_seed())


def set_rng_seed(value):
    global base_value
    key = base_value + 0x003988A5
    logger.info(type(process))
    return process.write_bytes(key, value, 1)


def game_over():
    global base_value
    key = base_value + 0x00D2C9F1
    if process.read_bytes(key, 1) == 1:
        return True
    else:
        return False


def battle_complete():
    key = base_value + 0x00D2A8E0
    value = process.read_bytes(key, 1)
    if value in [1, 2, 3]:
        return True
    return False


def battle_arena_results():
    global base_value
    if process.read_bytes(base_value + 0x00D2C9F1, 1) == 2:
        return True
    return False


def game_over_reset():
    global base_value
    key = base_value + 0x00D2C9F1
    process.write_bytes(key, 0, 1)


def battle_value():
    # Used for wrap_up function only
    key = base_value + 0x00D2A8E0
    return process.read_bytes(key, 1)


def battle_active() -> bool:
    global base_value
    key = base_value + 0x00D2A8E0
    value = process.read_bytes(key, 1)
    if value == 0:
        return False
    return True


def battle_wrap_up_active():
    # Not working yet, this memory value does not trigger after-battle screens
    global base_value
    key = base_value + 0x014408AC
    value = process.read_bytes(key, 4) & 0x20000
    if value >= 1:
        return True
    return False


def get_current_turn():
    return get_turn_by_index(turn_index=0)


def get_next_turn():
    return get_turn_by_index(turn_index=1)


def get_turn_by_index(turn_index: int):
    global base_value
    key = base_value + 0x00D2AA00 + (turn_index * 4)
    return process.read_bytes(key, 1)


def who_goes_first_after_current_turn(actors):
    ptr = 1
    ret_val = 99
    while ret_val == 99:
        turn_char = get_turn_by_index(ptr)
        if turn_char in actors:
            logger.warning (f"{turn_char} goes next, within options {actors}")
            return turn_char
        elif ptr > 30:
            return 99
        ptr += 1


def battle_menu_cursor():
    global base_value
    if not turn_ready():
        return 255
    key2 = base_value + 0x00F3C926
    return process.read_bytes(key2, 1)


def battle_screen():
    if main_battle_menu():
        global base_value
        if battle_menu_cursor() == 255:
            return False
        else:
            wait_frames(10)
            return True
    else:
        return False


def turn_ready():
    global base_value
    key = base_value + 0x01FCC08C
    if process.read_bytes(key, 4) == 0:
        return False
    else:
        # while not main_battle_menu():
        #    pass
        wait_frames(1)
        if game_vars.use_pause():
            wait_frames(2)
        return True


def battle_cursor_2():
    global base_value
    key = base_value + 0x00F3CA01
    if process.read_bytes(key, 1) != 0:
        key = base_value + 0x00F3CA0E
        return process.read_bytes(key, 1)
    else:
        return 255


def battle_cursor_3():
    try:
        key = base_value + 0x00F3CAFE
        return process.read_bytes(key, 1)
    except:
        return 255


def overdrive_menu_active():
    global base_value
    key = base_value + 0x00F3D6F4
    return process.read_bytes(key, 1) == 4


def overdrive_menu_active_wakka():
    global base_value
    key = base_value + 0x00DA0BD0
    return process.read_bytes(key, 1)


def auron_overdrive_active():
    global base_value
    key = base_value + 0x00F3D6B4
    return process.read_bytes(key, 1) == 4


def kim_od_unlocks():
    global base_value
    results = []

    # First byte
    key = base_value + 0xD307FD
    bits = process.read_bytes(key, 1)
    results.append(1 if (bits &   1) else 0)
    results.append(1 if (bits &   2) else 0)
    results.append(1 if (bits &   4) else 0)
    results.append(1 if (bits &   8) else 0)
    results.append(1 if (bits &  16) else 0)
    results.append(1 if (bits &  32) else 0)
    results.append(1 if (bits &  64) else 0)
    results.append(1 if (bits & 128) else 0)

    # Second byte
    key = base_value + 0xD307FE
    bits = process.read_bytes(key, 1)
    results.append(1 if (bits &   1) else 0)
    results.append(1 if (bits &   2) else 0)
    results.append(1 if (bits &   4) else 0)
    results.append(1 if (bits &   8) else 0)
    #results.append(1 if (bits &  16) else 0)
    #results.append(1 if (bits &  32) else 0)
    #results.append(1 if (bits &  64) else 0)
    #results.append(1 if (bits & 128) else 0)

    logger.info(f"Kim OD unlocks: {results}")
    return results


def tidus_od_count():
    global base_value
    return process.read_bytes(base_value + 0xd3083c, 2)


def main_battle_menu():
    global base_value
    key = base_value + 0x00F3C911
    if process.read_bytes(key, 1) > 0:
        return True
    else:
        return False


def other_battle_menu():
    global base_value
    key = base_value + 0x00F3CA01
    if process.read_bytes(key, 1) > 0:
        return True
    else:
        return False


def interior_battle_menu():
    global base_value
    key = base_value + 0x00F3CAF1
    return process.read_bytes(key, 1)


def super_interior_battle_menu():
    global base_value
    key = base_value + 0x00F3CBE1
    return process.read_bytes(key, 1)


def battle_target_id():
    global base_value
    key = base_value + 0x00F3D1B4
    ret_val = process.read_bytes(key, 1)
    logger.debug(f"Battle Target ID: {ret_val}")
    return ret_val


def battle_line_target():
    return read_val(0x00F3CA42)


def enemy_targetted():
    return read_val(0x00F3D1C0)


def battle_target_active():
    global base_value
    key = base_value + 0x00F3D1B4
    ret_val = process.read_bytes(key, 1)
    logger.debug(f"Battle Target ID: {ret_val}")
    return ret_val != 255


def user_control():
    global base_value
    # Auto updating via reference to the base_value above
    control_struct = base_value + 0x00F00740
    in_control = process.read(control_struct)

    if in_control == 0:
        return False
    else:
        return True


def controlled_actor_id():
    global base_value
    # Auto updating via reference to the base_value above
    control_struct = base_value + 0xEA23A4
    return process.read(control_struct)


def await_control():
    if user_control():
        return True
    logger.debug("Awaiting control (no clicking)")
    with logging_redirect_tqdm():
        fmt = "Awaiting control... elapsed {elapsed}"
        with tqdm(bar_format=fmt) as pbar:
            while not user_control():
                pbar.update()
    #wait_frames(1)
    logger.debug("User control restored.")
    return True


def click_to_control_dumb():
    if user_control():
        return True
    logger.debug("Awaiting control (clicking)")
    with logging_redirect_tqdm():
        fmt = "Awaiting control... elapsed {elapsed}"
        with tqdm(bar_format=fmt) as pbar:
            while not user_control():
                xbox.tap_b()
                pbar.update()
    logger.debug("User control restored.")
    return True


def click_to_control_smart(allow_story_mode:bool=False):
    if user_control():
        return True
    if game_vars.story_mode() and allow_story_mode:
        FFXC.set_neutral()
        while not user_control():
            xbox.tap_confirm()
        return True
    logger.debug("Awaiting control (clicking only when appropriate - dialog)")
    wait_frames(6)  # Why?
    with logging_redirect_tqdm():
        fmt = "{desc}... elapsed {elapsed}"
        with tqdm(bar_format=fmt) as pbar:
            pbar.set_description("Awaiting control")
            while not user_control():
                if battle_active():
                    while battle_active():
                        xbox.tap_b()
                if diag_skip_possible() and not game_vars.story_mode():
                    xbox.tap_b()
                elif menu_open():
                    xbox.tap_b()

                if menu_open():
                    pbar.set_description("Post-battle menu open")
                else:
                    pbar.set_description("Awaiting control")
    logger.debug("User control restored.")
    return True


def click_to_control():
    return click_to_control_smart()


def click_to_control_2():
    return click_to_control_smart()


def click_to_control_3():
    return click_to_control_smart(allow_story_mode=True)


def click_to_control_special():
    logger.debug("Awaiting control (clicking)")
    with logging_redirect_tqdm():
        fmt = "Awaiting control... elapsed {elapsed}"
        with tqdm(bar_format=fmt) as pbar:
            while not user_control():
                FFXC.set_confirm()
                FFXC.set_value("btn_y", 1)
                wait_frames(30 * 0.035)
                FFXC.release_confirm()
                FFXC.set_value("btn_y", 0)
                wait_frames(30 * 0.035)
                pbar.update()
    #wait_frames(2)
    logger.debug("User control restored.")
    return True


def click_to_event():
    while user_control():
        FFXC.set_confirm()
        if game_vars.use_pause():
            wait_frames(2)
        else:
            wait_frames(1)
        FFXC.release_confirm()
        if game_vars.use_pause():
            wait_frames(3)
        else:
            wait_frames(1)
    wait_frames(6)


def click_to_event_temple(direction, story_mode_dialog=False):
    if direction == 0:
        FFXC.set_movement(0, 1)
    if direction == 1:
        FFXC.set_movement(1, 1)
    if direction == 2:
        FFXC.set_movement(1, 0)
    if direction == 3:
        FFXC.set_movement(1, -1)
    if direction == 4:
        FFXC.set_movement(0, -1)
    if direction == 5:
        FFXC.set_movement(-1, -1)
    if direction == 6:
        FFXC.set_movement(-1, 0)
    if direction == 7:
        FFXC.set_movement(-1, 1)
    while user_control():
        xbox.tap_b()
    FFXC.set_neutral()
    wait_frames(6)
    if story_mode_dialog:
        click_to_control()
    else:
        click_to_control_3()


def await_event():
    wait_frames(1)
    while user_control():
        pass


def get_coords():
    global process
    global base_value
    global x_ptr
    global y_ptr
    global coords_counter
    coords_counter += 1
    x_ptr = base_value + 0x0084DED0
    y_ptr = base_value + 0x0084DED8
    coord_1 = process.get_pointer(x_ptr)
    x = float_from_integer(process.read(coord_1))
    coord_2 = process.get_pointer(y_ptr)
    y = float_from_integer(process.read(coord_2))

    return [x, y]


def distance_to_encounter(danger_val:int = 35):
    # Defaults to 35 for Clasko skip & thunder plains.
    grace_period = int(danger_val // 2)
    threat_mod = danger_val * 4

    rng_array = rng_array_from_index(index=0, array_len=800)
    for i in range(400):
        check_rng = (rng_array[i+1] & 0x7FFFFFFF) & 255
        check_value = (i) * 256 // threat_mod
        if check_rng < check_value:
            return (i+grace_period) * 10
    return 999


def ammes_fix(actor_index: int = 0):
    global process
    global base_value
    base_ptr = base_value + 0x1FC44E4
    base_addr = process.read(base_ptr)
    # x_coord = 749, y_coord = -71
    process.write(base_addr + (0x880 * actor_index) + 0x0C, 0x443B4000)
    process.write(base_addr + (0x880 * actor_index) + 0x14, 0xC28E0000)


def choco_eater_fun(actor_index: int = 0):
    global process
    global base_value
    base_ptr = base_value + 0x1FC44E4
    base_addr = process.read(base_ptr)
    process.write(base_addr + (0x880 * actor_index) + 0x14, 0xC4BB8000)


def extractor_height():
    global process
    global base_value
    height = get_actor_coords(3)[2]
    logger.debug(f"Extractor Height: {height}")
    return height


def get_height():
    global process
    global base_value
    global z_ptr

    z_ptr = base_value + 0x0084DED0
    coord_1 = process.get_pointer(z_ptr)
    return float_from_integer(process.read(coord_1))


def get_movement_vectors():
    global process
    global base_value
    addr = base_value + 0x00F00754
    ptr = process.get_pointer(addr)
    angle = float_from_integer(process.read(ptr))
    forward = [cos(angle), sin(angle)]
    right = [sin(angle), -cos(angle)]
    return (forward, right)


def get_camera():
    global base_value
    angle = base_value + 0x008A86B8
    x = base_value + 0x008A86F8
    y = base_value + 0x008A8700
    z = base_value + 0x008A86FC
    angle2 = base_value + 0x008A86C0

    key = process.get_pointer(angle)
    angle_val = round(float_from_integer(process.read(key)), 2)
    key = process.get_pointer(x)
    x_val = round(float_from_integer(process.read(key)), 2)
    key = process.get_pointer(y)
    y_val = round(float_from_integer(process.read(key)), 2)
    key = process.get_pointer(z)
    z_val = round(float_from_integer(process.read(key)), 2)
    key = process.get_pointer(angle2)
    angle_val_2 = round(float_from_integer(process.read(key)), 2)

    ret_val = [angle_val, x_val, y_val, z_val, angle_val_2]
    return ret_val


def get_hp():
    global base_value
    # Out of combat HP only

    coord = base_value + 0x00D32078
    HP_Tidus = process.read(coord)
    coord = base_value + 0x00D3210C
    HP_Yuna = process.read(coord)
    coord = base_value + 0x00D321A0
    HP_Auron = process.read(coord)
    coord = base_value + 0x00D32234
    HP_Kimahri = process.read(coord)
    coord = base_value + 0x00D322C8
    HP_Wakka = process.read(coord)
    coord = base_value + 0x00D3235C
    HP_Lulu = process.read(coord)
    coord = base_value + 0x00D323F0
    HP_Rikku = process.read(coord)
    return [HP_Tidus, HP_Yuna, HP_Auron, HP_Kimahri, HP_Wakka, HP_Lulu, HP_Rikku]


def get_max_hp():
    global base_value
    # Out of combat HP only

    coord = base_value + 0x00D32080
    HP_Tidus = process.read(coord)
    coord = base_value + 0x00D32114
    HP_Yuna = process.read(coord)
    coord = base_value + 0x00D321A8
    HP_Auron = process.read(coord)
    coord = base_value + 0x00D3223C
    HP_Kimahri = process.read(coord)
    coord = base_value + 0x00D322D0
    HP_Wakka = process.read(coord)
    coord = base_value + 0x00D32364
    HP_Lulu = process.read(coord)
    coord = base_value + 0x00D323F8
    HP_Rikku = process.read(coord)
    return [HP_Tidus, HP_Yuna, HP_Auron, HP_Kimahri, HP_Wakka, HP_Lulu, HP_Rikku]


def get_max_mp(actor_index:int=0):
    global base_value
    # Out of combat HP only
    # logger.warning(f"Check: {actor_index}")

    coord = base_value + 0x00D32084 + (actor_index * 0x94)
    actor_max_mp = process.read(coord)
    # logger.manip(f"Actor {actor_index} max MP: {actor_max_mp}")
    return actor_max_mp


def get_actor_mp(actor_id:int):
    global base_value
    offset = actor_id * 0x94
    ret_val = process.read(base_value + 0xD3207C + offset)
    return ret_val

def get_tidus_mp():
    return get_actor_mp(actor_id=0)
    # global base_value
    # ret_val = process.read(base_value + 0xD3207C)
    # return ret_val


def get_yuna_mp():
    return get_actor_mp(actor_id=1)
    # global base_value
    # ret_val = process.read(base_value + 0xD32110)
    # return ret_val


def get_rikku_mp():
    return get_actor_mp(actor_id=6)
    # global base_value
    # ret_val = process.read(base_value + 0xD322F8)  # should be 0xD323DC
    # return ret_val


def get_order():
    global base_value
    # Out of combat HP only

    coord = base_value + 0x00D307E8
    pos1 = process.read_bytes(coord, 1)
    coord = base_value + 0x00D307E9
    pos2 = process.read_bytes(coord, 1)
    coord = base_value + 0x00D307EA
    pos3 = process.read_bytes(coord, 1)
    coord = base_value + 0x00D307EB
    pos4 = process.read_bytes(coord, 1)
    coord = base_value + 0x00D307EC
    pos5 = process.read_bytes(coord, 1)
    coord = base_value + 0x00D307ED
    pos6 = process.read_bytes(coord, 1)
    coord = base_value + 0x00D307EE
    pos7 = process.read_bytes(coord, 1)

    formation = [255, pos1, pos2, pos3, pos4, pos5, pos6, pos7]
    logger.debug(f"Party formation: {formation}")
    return formation


def get_order_six():
    global base_value
    # Out of combat HP only

    coord = base_value + 0x00D307E8
    pos1 = process.read_bytes(coord, 1)
    coord = base_value + 0x00D307E9
    pos2 = process.read_bytes(coord, 1)
    coord = base_value + 0x00D307EA
    pos3 = process.read_bytes(coord, 1)
    coord = base_value + 0x00D307EB
    pos4 = process.read_bytes(coord, 1)
    coord = base_value + 0x00D307EC
    pos5 = process.read_bytes(coord, 1)
    coord = base_value + 0x00D307ED
    pos6 = process.read_bytes(coord, 1)
    coord = base_value + 0x00D307EE
    pos7 = process.read_bytes(coord, 1)

    formation = [pos1, pos2, pos3, pos4, pos5, pos6, pos7]
    #logger.debug(f"Party formation: {formation}")
    while 255 in formation:
        formation.remove(255)
    return formation


def get_order_seven():
    global base_value
    # Out of combat HP only

    coord = base_value + 0x00D307E8
    pos1 = process.read_bytes(coord, 1)
    coord = base_value + 0x00D307E9
    pos2 = process.read_bytes(coord, 1)
    coord = base_value + 0x00D307EA
    pos3 = process.read_bytes(coord, 1)
    coord = base_value + 0x00D307EB
    pos4 = process.read_bytes(coord, 1)
    coord = base_value + 0x00D307EC
    pos5 = process.read_bytes(coord, 1)
    coord = base_value + 0x00D307ED
    pos6 = process.read_bytes(coord, 1)
    coord = base_value + 0x00D307EE
    pos7 = process.read_bytes(coord, 1)
    coord = base_value + 0x00D307EF
    pos8 = process.read_bytes(coord, 1)
    coord = base_value + 0x00D307F0
    pos9 = process.read_bytes(coord, 1)

    formation = [pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9]
    while 255 in formation:
        formation.remove(255)
    return formation


def get_char_formation_slot(char_num):
    all_slots = get_order_seven()
    x = 0
    while x < len(all_slots):
        if all_slots[x] == char_num:
            return x
        else:
            x += 1
    return 255  # Character is not in the party


def get_phoenix():
    global base_value

    key = get_item_slot(6)
    p_downs = get_item_count_slot(key)
    logger.debug(f"Phoenix Down count: {p_downs}")
    return p_downs


def get_power():
    global base_value

    key = get_item_slot(70)
    power = get_item_count_slot(key)
    logger.debug(f"Power spheres: {power}")
    return power


def set_power(qty):
    global base_value

    slot = get_item_slot(70)
    key = base_value + item_count_addr(slot)
    process.write_bytes(key, qty, 1)
    power = get_power()
    return power


def get_mana():
    global base_value

    key = get_item_slot(71)
    if key == 255:
        mana = 0
    else:
        mana = get_item_count_slot(key)
    logger.debug(f"Mana spheres: {mana}")
    return mana


def get_speed():
    global base_value

    key = get_item_slot(72)
    speed = get_item_count_slot(key)
    #logger.debug(f"Speed spheres: {speed}")
    return speed


def set_speed(qty):
    global base_value

    slot = get_item_slot(72)
    key = base_value + item_count_addr(slot)
    process.write_bytes(key, qty, 1)
    speed = get_speed()
    return speed


def get_battle_hp():
    global base_value

    key = base_value + 0x00F3F7A4
    hp1 = process.read(key)
    key = base_value + 0x00F3F834
    hp2 = process.read(key)
    key = base_value + 0x00F3F8C4
    hp3 = process.read(key)
    hp_array = [hp1, hp2, hp3]
    return hp_array


def get_battle_mp(character):
    global base_value
    key = base_value + 0xD334CC
    ptr = process.read_bytes(key,4)
    offset = (0xF90 * character)
    logger.debug("==================")
    #logger.debug(process.read_bytes(ptr + offset + 0x5D4, 2))
    #logger.debug(process.read_bytes(ptr + 0x5D4, 2))
    #logger.debug(process.read_bytes(ptr + offset + 0x6E8, 2))
    #logger.debug(process.read_bytes(ptr + 0x6E8, 2))
    ret_val = process.read_bytes(ptr + offset + 0x5D4, 2)
    return ret_val


def get_encounter_id():
    global base_value

    key = base_value + 0x00D2A8EC
    formation = process.read(key)

    return formation


def get_enemy_formation():
    base_id = get_encounter_id()


def clear_encounter_id():
    global base_value

    key = base_value + 0x00D2A8EC
    process.write(key, 0)


def get_active_battle_formation():
    global base_value

    key = base_value + 0x00F3F76C
    char1 = process.read_bytes(key, 1)
    key = base_value + 0x00F3F76E
    char2 = process.read_bytes(key, 1)
    key = base_value + 0x00F3F770
    char3 = process.read_bytes(key, 1)

    battle_form = [char1, char2, char3]
    return battle_form


def get_battle_formation():
    global base_value

    key = base_value + 0x00F3F76C
    char1 = process.read_bytes(key, 1)
    key = base_value + 0x00F3F76E
    char2 = process.read_bytes(key, 1)
    key = base_value + 0x00F3F770
    char3 = process.read_bytes(key, 1)
    key = base_value + 0x00D2C8A3
    char4 = process.read_bytes(key, 1)
    key = base_value + 0x00D2C8A4
    char5 = process.read_bytes(key, 1)
    key = base_value + 0x00D2C8A5
    char6 = process.read_bytes(key, 1)
    key = base_value + 0x00D2C8A6
    char7 = process.read_bytes(key, 1)
    key = base_value + 0x00D2C8A7
    char8 = process.read_bytes(key, 1)
    key = base_value + 0x00D2C8A8
    char9 = process.read_bytes(key, 1)
    key = base_value + 0x00D2C8A9
    char10 = process.read_bytes(key, 1)

    battle_form = [char4, char5, char6, char7, char8, char9, char10]
    logger.debug(f"Battle formation before: {battle_form}")
    battle_form = [x for x in battle_form if x != 255]
    battle_form.insert(0, char3)
    battle_form.insert(0, char2)
    battle_form.insert(0, char1)
    logger.debug(f"Battle formation after: {battle_form}")
    return battle_form


def get_battle_char_slot(char_num) -> int:
    battle_form = get_battle_formation()
    if char_num not in battle_form:
        return 255
    try:
        if battle_form[0] == char_num:
            return 0
        if battle_form[1] == char_num:
            return 1
        if battle_form[2] == char_num:
            return 2
        if battle_form[3] == char_num:
            return 3
        if battle_form[4] == char_num:
            return 4
        if battle_form[5] == char_num:
            return 5
        if battle_form[6] == char_num:
            return 6
    except Exception:
        return 255


def get_battle_char_turn():
    global base_value

    key = base_value + 0x00D36A68
    battle_character = process.read(key)
    return battle_character


def get_slvl_yuna():
    return get_yuna_slvl()


def get_slvl_kim():
    global base_value
    # Out of combat HP only

    coord = base_value + 0x00D3222C
    return process.read_bytes(coord, 1)


def get_slvl_wakka():
    global base_value
    # Out of combat HP only

    key = base_value + 0x00D322E7
    s_lvl = process.read_bytes(key, 1)
    logger.debug(f"Wakka current Slvl: {s_lvl}")
    return s_lvl


def item_address(num):
    global base_value
    return base_value + 0x00D3095C + (num * 0x2)


def get_items_order():
    items = []
    for x in range(150):
        items.append(process.read_bytes(item_address(x), 1))
    return items


def get_use_items_order():
    item_array = get_items_order()
    x = 0
    while x < len(item_array):
        try:
            if item_array[x] in [52]:
                del item_array[x]
            elif item_array[x] < 20:
                del item_array[x]
            elif item_array[x] > 69:
                del item_array[x]
            else:
                x += 1
        except Exception as y:
            logger.exception(y)
    logger.debug("Items set up:")
    logger.debug(item_array)
    return item_array


def get_use_items_slot(item_num):
    items = get_use_items_order()
    x = 0
    for x in range(len(items)):
        #logger.debug(f"get_use_items_slot(): {items[x]} | {item_num} | {x}")
        if items[x] == item_num:
            logger.debug("============================")
            logger.debug(f"FOUND ITEM: {items[x]} | {item_num} | {x}")
            logger.debug("============================")
            return x
        x += 1
    return 255


def get_throw_items_order():
    item_array = get_items_order()
    logger.debug(f"get_throw_items_order(), item_array: {item_array}")
    x = 0
    while x < len(item_array):
        try:
            if item_array[x] > 19:
                item_array.remove(item_array[x])
            else:
                x += 1
        except Exception as y:
            logger.exception(y)
            logger.debug("Retrying value")
    logger.debug(f"item_array: {item_array}")
    return item_array


def get_throw_items_slot(item_num):
    items = get_throw_items_order()
    x = 0
    while x < len(items):
        if items[x] == item_num:
            logger.debug(f"Desired item {item_num} is in slot {x}")
            return x
        x += 1
    return 255


def get_grid_items_order():
    item_array = get_items_order()
    x = 0
    while x < len(item_array):
        try:
            if item_array[x] < 70 or item_array[x] > 99:
                item_array.remove(item_array[x])
            else:
                x += 1
        except Exception as y:
            logger.exception(y)
            logger.debug("Retrying value")
    return item_array


def get_grid_items_slot(item_num) -> int:
    items = get_grid_items_order()
    x = 0
    while x < len(items):
        if items[x] == item_num:
            logger.debug(f"Desired item {item_num} is in slot {x}")
            return x
        x += 1
    return 255


def get_grid_cursor_pos():
    global base_value
    key = base_value + 0x012ACB78
    return process.read_bytes(key, 1)


def get_grid_move_use_pos():
    global base_value
    key = base_value + 0x012AC838
    return process.read_bytes(key, 1)


def get_grid_move_active():
    global base_value
    key = base_value + 0x012AC82B
    if process.read_bytes(key, 1):
        return True
    else:
        return False


def get_grid_use_active():
    global base_value
    key = base_value + 0x012ACB6B
    if process.read_bytes(key, 1):
        return True
    else:
        return False


def get_item_slot(item_num):
    items = get_items_order()
    for x in range(len(items)):
        if items[x] == item_num:
            return x
    return 255


def check_items_macalania():
    bomb_core = 0
    l_marble = 0
    f_scale = 0
    a_wind = 0
    grenade = 0
    lunar = 0
    light = 0

    bomb_core = get_item_slot(27)
    l_marble = get_item_slot(30)
    f_scale = get_item_slot(32)
    a_wind = get_item_slot(24)
    grenade = get_item_slot(35)
    lunar = get_item_slot(56)
    light = get_item_slot(57)

    # Set max_spot to one more than the last undesirable item
    if light - lunar != 1:
        max_spot = light
    elif lunar - grenade != 1:
        max_spot = lunar
    elif grenade - a_wind != 1:
        max_spot = grenade
    elif a_wind - f_scale != 1:
        max_spot = a_wind
    elif f_scale - l_marble != 1:
        max_spot = f_scale
    elif l_marble - bomb_core != 1:
        max_spot = l_marble
    else:
        max_spot = bomb_core

    ret_val = [bomb_core, l_marble, f_scale, a_wind, grenade, lunar, light, max_spot]
    logger.debug(f"check_items_macalania(). Returning values: {ret_val}")
    return ret_val


def item_count_addr(num):
    return 0x00D30B5C + num


def get_items_count():
    global base_value
    item_counts = []
    for x in range(60):
        item_counts.append(process.read_bytes(base_value + 0x00D30B5C + x, 1))
    return item_counts


def get_item_count_slot(item_slot) -> int:
    global base_value
    return process.read_bytes(base_value + 0x00D30B5C + item_slot, 1)


def get_menu_display_characters():
    base = 0x01441BD4
    characters = []
    for cur in range(7):
        char = read_val(base + cur)
        # logger.debug(f"get_menu_display_characters(), Cur: {cur}, Char: {char}")
        characters.append(char)
    # logger.debug(f"get_menu_display_characters(), characters: {characters}")
    return characters


def get_gil_value():
    global base_value
    key = base_value + 0x00D307D8
    return process.read(key)


def set_gil_value(new_value):
    global base_value
    key = base_value + 0x00D307D8
    return process.write(key, new_value)


def set_story(new_value):
    global base_value
    key = base_value + 0x00D2D67C
    return process.write_bytes(key, new_value, 2)


def rikku_od_cursor_1():
    global base_value
    key = base_value + 0x00F3CB32
    return process.read_bytes(key, 1)


def rikku_od_cursor_2():
    return rikku_od_cursor_1()


def get_overdrive_battle(character):
    global process
    global base_value

    base_pointer = base_value + 0x00D334CC
    base_pointer_address = process.read(base_pointer)
    logger.manip(f"Base Pointer: {base_pointer_address}")
    offset = (0xF90 * character) + 0x5BC
    logger.manip(f"Original: Reading from {base_pointer_address + offset}")
    ret_val = process.read_bytes(base_pointer_address + offset, 1)
    logger.manip(f"In-Battle Overdrive values: {ret_val}")
    return ret_val


def get_char_weakness(character):
    global process
    global base_value

    base_pointer = base_value + 0x00D334CC
    base_pointer_address = process.read(base_pointer)
    offset = (0xF90 * character) + 0x5DD
    ret_val = process.read_bytes(base_pointer_address + offset, 1)
    logger.debug(f"In-Battle char weakness values: {ret_val}")
    return ret_val


def tidus_escaped_state():
    global base_value

    base_pointer = base_value + 0x00D334CC
    base_pointer_address = process.read(base_pointer)
    offset = 0xDC8
    ret_val = not process.read_bytes(base_pointer_address + offset, 1)
    logger.debug(f"Tidus Escaped State: {ret_val}")
    return ret_val


def state_dead(character):
    global process
    global base_value
    base_pointer = base_value + 0xD334CC
    base_pointer_address = process.read(base_pointer)
    offset = (0xF90 * character) + 0x606

    key = base_pointer_address + offset
    ret_val = process.read_bytes(key, 1)

    if ret_val % 2 == 1:
        return True
    else:
        return False


def state_berserk(character):
    global process
    global base_value
    base_pointer = base_value + 0xD334CC
    base_pointer_address = process.read(base_pointer)
    offset = (0xF90 * character) + 0x607

    key = base_pointer_address + offset
    ret_val = process.read_bytes(key, 1)

    if ret_val % 4 >= 2:
        return True
    else:
        return False


def state_petrified(character):
    if character not in get_active_battle_formation():
        return False

    global process
    global base_value
    base_pointer = base_value + 0xD334CC
    base_pointer_address = process.read(base_pointer)
    offset = (0xF90 * character) + 0x606

    key = base_pointer_address + offset
    ret_val = process.read_bytes(key, 1)

    if ret_val % 8 >= 4:
        return True
    else:
        return False


def state_confused(character):
    global process
    global base_value
    base_pointer = base_value + 0xD334CC
    base_pointer_address = process.read(base_pointer)
    offset = (0xF90 * character) + 0x607

    key = base_pointer_address + offset
    ret_val = process.read_bytes(key, 1)

    if ret_val % 2 == 1:
        logger.debug(f"Character {character} is confused")
        return True
    else:
        logger.debug(f"Character {character} is not confused")
        return False


def state_sleep(character):
    global process
    global base_value
    base_pointer = base_value + 0xD334CC
    base_pointer_address = process.read(base_pointer)
    offset = (0xF90 * character) + 0x608

    key = base_pointer_address + offset
    ret_val = process.read_bytes(key, 1)

    if ret_val != 0:
        logger.debug(f"Character {character} is asleep (probably)")
        return True
    else:
        logger.debug(f"Character {character} is not asleep (probably)")
        return False


def state_silence(character):
    global process
    global base_value
    base_pointer = base_value + 0xD334CC
    base_pointer_address = process.read(base_pointer)
    offset = (0xF90 * character) + 0x609
    result = process.read_bytes(int(base_pointer_address+offset), 1)
    logger.debug(f"Silence turns remaining for char {character}: {result}")
    return result


def state_silence(character):
    global process
    global base_value
    base_pointer = base_value + 0xD334CC
    base_pointer_address = process.read(base_pointer)
    offset = (0xF90 * character) + 0x609
    result = process.read_bytes(int(base_pointer_address+offset), 1)
    logger.debug(f"Silence turns remaining for char {character}: {result}")
    return result


def print_all_statuses():
    global process
    global base_value
    base_pointer = base_value + 0xD334CC
    base_pointer_address = process.read(base_pointer)
    for i in range(7):
        logger.warning("Statuses char {i}:")
        offset = (0xF90 * i) + 0x609
        logger.warning(process.read_bytes(int(base_pointer_address+offset), 1))
        #offset = (0xF90 * i) + 0x607
        #logger.warning(process.read_bytes(int(base_pointer_address+offset), 1))
        #offset = (0xF90 * i) + 0x608
        #logger.warning(process.read_bytes(int(base_pointer_address+offset), 1))


def state_auto_life(character: int = 0) -> bool:
    global process
    global base_value
    base_pointer = base_value + 0xD334CC
    base_pointer_address = process.read(base_pointer)
    offset = (0xF90 * character) + 0x617

    key = base_pointer_address + offset
    ret_val = process.read_bytes(key, 1)

    if ret_val % 4 >= 2:
        logger.debug(f"Character autolife is active on: {character}")
        return True
    else:
        logger.debug(f"Character autolife is not active on: {character}")
        return False


def state_confused_by_pos(position):
    pos_array = get_battle_formation()
    x = 0
    if position in pos_array:
        if pos_array[x] == position:
            return state_confused(pos_array[x])
        else:
            x += 1


def battle_type():
    # 0 is normal, 1 is pre-empt, 2 is ambushed
    return read_val(0x00D2C9DC)


def get_enemy_current_hp(ignore_dead = True):
    global process
    global base_value
    enemy_num = 20
    base_pointer = base_value + 0xD334CC
    base_pointer_address = process.read(base_pointer)

    while enemy_num < 27:
        offset1 = (0xF90 * enemy_num) + 0x594
        key1 = base_pointer_address + offset1
        offset2 = (0xF90 * enemy_num) + 0x5D0
        key2 = base_pointer_address + offset2
        if enemy_num == 20:
            max_hp = [process.read_bytes(key1, 4)]
            current_hp = [process.read_bytes(key2, 4)]
        else:
            next_hp = process.read_bytes(key1, 4)
            if next_hp != 0 or not ignore_dead:
                max_hp.append(next_hp)
                current_hp.append(process.read_bytes(key2, 4))
        enemy_num += 1
    logger.debug(f"Enemy HP current values: {current_hp}")
    return current_hp


def get_enemy_max_hp():
    global process
    global base_value
    enemy_num = 20
    base_pointer = base_value + 0xD334CC
    base_pointer_address = process.read(base_pointer)

    while enemy_num < 25:
        offset1 = (0xF90 * enemy_num) + 0x594
        key1 = base_pointer_address + offset1
        offset2 = (0xF90 * enemy_num) + 0x5D0
        key2 = base_pointer_address + offset2
        if enemy_num == 20:
            max_hp = [process.read_bytes(key1, 4)]
            current_hp = [process.read_bytes(key2, 4)]
        else:
            if max_hp != 0:
                max_hp.append(process.read_bytes(key1, 4))
                current_hp.append(process.read_bytes(key2, 4))
        enemy_num += 1
    logger.debug(f"Enemy HP max values: {max_hp}")
    logger.debug(f"Enemy HP current values: {current_hp}")
    return max_hp


def menu_open():
    global base_value

    key = base_value + 0x00F407E4
    menu_open = process.read_bytes(key, 1)
    if menu_open == 0:
        return False
    else:
        return True


def close_menu():
    while menu_open():
        xbox.tap_a()


def save_menu_open():
    global base_value

    key = base_value + 0x008E7300
    menu_open = process.read_bytes(key, 1)
    if menu_open == 1:
        return True
    else:
        return False


def back_to_main_menu():
    while menu_number() not in [1, 2, 3, 4, 5]:
        if menu_open():
            xbox.tap_a()
        else:
            xbox.tap_y()
        if game_vars.use_pause():
            wait_frames(6)


def open_menu():
    menu_counter = 0
    while not (user_control() and menu_open() and menu_number() == 5):
        if menu_open() and not user_control():
            logger.debug(
                "Post-Battle summary screen is open. "
                + f"Attempting close. menu_counter: {menu_counter}"
            )
            xbox.menu_b()
        elif user_control() and not menu_open():
            logger.debug(
                f"Menu is not open, attempting to open. menu_counter: {menu_counter}"
            )
            xbox.tap_y()
            menu_counter += 1
        elif menu_open() and user_control() and menu_number() > 5:
            logger.debug(f"The wrong menu is open. menu_counter: {menu_counter}")
            xbox.tap_a()
            menu_counter += 1
        elif battle_active():
            logger.debug(f"Can't open menu during battle. menu_counter: {menu_counter}")
            return False
        else:
            pass
    FFXC.set_neutral()
    logger.debug("Menu open returning")
    return True


def menu_number():
    global base_value
    return process.read_bytes(base_value + 0x85B2CC, 1)


def s_grid_active():
    global base_value

    key = base_value + 0x0085B30C
    menu_open = process.read_bytes(key, 1)
    if menu_open == 1:
        return True
    else:
        return False


def s_grid_menu():
    global base_value

    key = base_value + 0x0012AD860
    menu_open = process.read_bytes(key, 1)
    return menu_open


def s_grid_char():
    global base_value

    key = base_value + 0x0012BEE2C
    character = process.read_bytes(key, 1)
    return character


def s_grid_node_selected():
    global base_value

    key = base_value + 0x0012BEB7E
    node_number = process.read_bytes(key, 1)
    key = base_value + 0x0012BEB7F
    node_region = process.read_bytes(key, 1)
    return [node_number, node_region]


def s_grid_cursor_coords():
    global base_value
    key = base_value + 0x0012BEB28
    x = float_from_integer(process.read_bytes(key, 4))
    key = base_value + 0x0012BEB2C
    y = float_from_integer(process.read_bytes(key, 4))
    if x != 0 and y != 0:
        if x != None and y != None:
            return [x,y]
    key = base_value + 0x0012BEB78
    x = float_from_integer(process.read_bytes(key, 4))
    key = base_value + 0x0012BEB7C
    y = float_from_integer(process.read_bytes(key, 4))
    if x != 0 and y != 0:
        if x != None and y != None:
            return [x,y]
    key = base_value + 0x0012BEB88
    x = float_from_integer(process.read_bytes(key, 4))
    key = base_value + 0x0012BEB8C
    y = float_from_integer(process.read_bytes(key, 4))
    if x != 0 and y != 0:
        if x != None and y != None:
            return [x,y]
    key = base_value + 0x0012BECC0
    x = float_from_integer(process.read_bytes(key, 4))
    key = base_value + 0x0012BECC4
    y = float_from_integer(process.read_bytes(key, 4)) * -1
    if x != 0 and y != 0:
        if x != None and y != None:
            return [x,y]


def cursor_location():
    global base_value

    key = base_value + 0x0021D09A4
    menu1 = process.read_bytes(key, 1)
    key = base_value + 0x0021D09A6
    menu2 = process.read_bytes(key, 1)

    return [menu1, menu2]


def get_menu_cursor_pos():
    global base_value

    key = base_value + 0x01471508
    pos = process.read_bytes(key, 1)

    return pos


def get_item_menu_cursor_pos() -> (int, int):
    global base_value

    row_key = base_value + 0x01440A38
    row_pos = process.read_bytes(row_key, 1)

    column_key = base_value + 0x01440A48
    column_pos = process.read_bytes(column_key, 1)

    return row_pos, column_pos


def get_menu_2_char_num():
    global base_value

    key = base_value + 0x0147150C
    pos = process.read_bytes(key, 1)

    return pos


def get_char_cursor_pos():
    global base_value

    key = base_value + 0x01441BE8
    pos = process.read_bytes(key, 1)

    return pos


def get_story_progress():
    global base_value

    key = base_value + 0x00D2D67C
    progress = process.read_bytes(key, 2)
    return progress


def get_map():
    global base_value
    key = base_value + 0x00D2CA90
    progress = process.read_bytes(key, 2)
    return progress


def touching_save_sphere():
    global base_value

    key = base_value + 0x0021D09A6
    value = process.read_bytes(key, 1)
    if value != 0:
        return True
    else:
        return False


def save_menu_cursor():
    global base_value

    key = base_value + 0x001467942
    return process.read_bytes(key, 1)


def map_cursor():
    global base_value
    base_pointer = base_value + 0x00F2FF14
    base_pointer_address = process.read(base_pointer)
    logger.debug(f"map_cursor(), base_pointer_address: {base_pointer_address}")
    ret = process.read_bytes(base_pointer_address + 272, 1)
    logger.debug(f"map_cursor(), ret: {ret}")
    return ret


def clear_save_menu_cursor():
    global base_value

    key = base_value + 0x001467942
    return process.write_bytes(key, 0, 1)


def clear_save_menu_cursor_2():
    global base_value

    key = base_value + 0x001468302
    return process.write_bytes(key, 0, 1)


def save_menu_cursor_2():
    global base_value

    key = base_value + 0x001468302
    return process.read_bytes(key, 1)


def new_game_cursor():
    global base_value

    key = base_value + 0x001467942
    value = process.read_bytes(key, 1)
    return value


def blitz_recrut_swap_cursor():
    global base_value

    key = base_value + 0x001467E22
    value = process.read_bytes(key, 1)
    return value


def targeting_ally():
    return read_val(0x00F3D1C0) == 0


def targeting_enemy():
    return not targeting_ally()


def get_yuna_slvl():
    global base_value

    key = base_value + 0x00D3212B
    s_lvl = process.read_bytes(key, 1)
    return s_lvl


def get_tidus_slvl():
    global base_value

    key = base_value + 0x00D32097
    s_lvl = process.read_bytes(key, 1)
    return s_lvl


def get_kimahri_slvl():
    global base_value

    key = base_value + 0x00D32253
    s_lvl = process.read_bytes(key, 1)
    return s_lvl


def get_lulu_slvl():
    return read_val(0x00D3237B)


def get_tidus_xp():
    global base_value

    key = base_value + 0x00D32070
    Lvl = process.read(key)
    return Lvl


def set_tidus_slvl(levels):
    global base_value

    key = base_value + 0x00D32097
    s_lvl = process.write_bytes(key, levels, 1)
    return s_lvl


def menu_control():
    global base_value

    key = base_value + 0x0085A03C
    control = process.read_bytes(key, 1)
    if control == 1:
        return True
    else:
        return False


def diag_skip_possible_old():
    global base_value

    key = base_value + 0x0085A03C
    control = process.read_bytes(key, 1)
    if control == 1:
        wait_frames(1)
        return True
    else:
        return False


def diag_skip_possible():
    global base_value
    if auditory_dialog_playing() and game_vars.story_mode():
        # logger.debug("Skip 2")
        return False
    else:
        key = base_value + 0x0085A03C  #  English
        if process.read_bytes(key, 1) == 1:
            # logger.debug("Skip 3")
            if game_vars.accessibility_vars()[2]:
                # Placeholder for accessibility, to be implemented later.
                pass
            return True
        else:
            # logger.debug("Skip 4")
            return False


def cutscene_skip_possible():
    if not game_vars.accessibility_vars()[0]:
        return False
    global base_value
    key = base_value + 0x00D2A008
    return process.read_bytes(key, 1) == 1


def auditory_dialog_playing():
    # This is usually a no-op unless do_not_skip_cutscenes is set.
    if not game_vars.accessibility_vars()[0]:
        return False
    global base_value

    key = base_value + 0x00F30038
    control = process.read_bytes(key, 1)
    return control == 1


def special_text_open():
    global base_value

    key = base_value + 0x01466D30
    control = process.read_bytes(key, 1)
    if control == 1:
        return True
    else:
        key = base_value + 0x01476988
        control = process.read_bytes(key, 1)
        if control == 1:
            return True
        else:
            return False


def await_menu_control():
    counter = 0
    while not menu_control():
        counter += 1
        if counter % 100000 == 0:
            logger.debug(f"Waiting for menu control. {counter}")


def click_to_story_progress(destination):
    counter = 0
    current_state = get_story_progress()
    logger.debug(
        f"Story goal: {destination} | Awaiting progress state: {current_state}"
    )
    while current_state < destination:
        if menu_control() and not game_vars.story_mode():
            FFXC.set_confirm()
            FFXC.set_back()
            wait_frames(1)
            FFXC.release_confirm()
            FFXC.release_back()
            wait_frames(1)
        if counter % 100000 == 0:
            logger.debug(
                f"Story goal: {destination} | "
                + f"Awaiting progress state: {current_state} | "
                + f"counter: {counter / 100000}"
            )
        counter += 1
        current_state = get_story_progress()
    logger.debug(f"Story progress has reached destination. Value: {destination}")


def party_size():
    battle_form = get_battle_formation()
    if 255 in battle_form:
        while 255 in battle_form:
            battle_form.remove(255)
    return len(battle_form)


def active_party_size():
    battle_form = get_active_battle_formation()
    if 255 in battle_form:
        while 255 in battle_form:
            battle_form.remove(255)
    return len(battle_form)


def get_character_index_in_main_menu(character):
    res = get_menu_display_characters().index(character)
    logger.debug(f"get_character_index_in_main_menu(): Char is in position {res}")
    return res


def update_formation(first_char, second_char, third_char, *, full_menu_close=True):
    order = get_order_seven()
    party_members = len(order)
    order_final = [first_char, second_char, third_char]
    order_final.extend(x for x in order if x not in order_final)
    if Counter(order[:3]) == Counter(order_final[:3]):
        logger.debug("Good to go, no action taken.")
    else:
        logger.debug(f"Converting from formation: {order}")
        logger.debug(f"Into formation: {order_final}")
        replacement_dict = {}
        new_characters = [x for x in order_final[:3] if x not in order[:3]]
        for i in range(3):
            if order[i] in order_final[:3]:
                replacement_dict[i] = order[i]
            else:
                replacement_dict[i] = new_characters.pop()
        for i in range(3):
            order_final[i] = replacement_dict[i]
        while not menu_open():
            if not open_menu():
                return
        FFXC.set_neutral()
        while get_menu_cursor_pos() != 7:
            menu_direction(get_menu_cursor_pos(), 7, 11)
            if game_vars.use_pause():
                wait_frames(1)
        while menu_number() != 14:
            xbox.menu_b()
        start_pos = 0
        while Counter(order[:3]) != Counter(order_final[:3]):
            # Select target in the wrong spot.
            if order[start_pos] == order_final[start_pos]:
                while (
                    order[start_pos] == order_final[start_pos] and order != order_final
                ):
                    start_pos += 1
                    if start_pos == party_members:
                        start_pos = 0
            name_from_number(order_final[start_pos])

            # Set target, end position
            end_pos = 0
            if order_final[start_pos] != order[end_pos]:
                while order_final[start_pos] != order[end_pos] and order != order_final:
                    end_pos += 1

            name_from_number(order[end_pos])

            if start_pos < 3 and end_pos < 3:
                start_pos += 1
                if start_pos == party_members:
                    start_pos = 0
                continue

            # Move cursor to start position
            if party_format_cursor_1() != start_pos:
                # logger.debug("Cursor not in right spot")
                while party_format_cursor_1() != start_pos:
                    menu_direction(party_format_cursor_1(), start_pos, party_members)
                    if game_vars.use_pause():
                        wait_frames(1)

            while menu_number() != 20:
                xbox.menu_b()  # Click on Start location

            # Move cursor to end position
            while party_format_cursor_2() != end_pos:
                menu_direction(party_format_cursor_2(), end_pos, party_members)
                if game_vars.use_pause():
                    wait_frames(1)
            while menu_number() != 14:
                xbox.menu_b()  # Click on End location, performs swap.
            start_pos += 1
            if start_pos == party_members:
                start_pos = 0

            order = get_order_seven()
        if full_menu_close:
            close_menu()
        else:
            back_to_main_menu()


def menu_direction(current_menu_position, target_menu_position, menu_size):
    distance = abs(current_menu_position - target_menu_position)
    distance_unsigned = current_menu_position - target_menu_position
    halfmenusize = menu_size / 2
    if distance == halfmenusize:
        xbox.tap_up()
    elif distance < halfmenusize:
        if distance_unsigned > 0:
            xbox.tap_up()
        else:
            xbox.tap_down()
    else:
        if distance_unsigned > 0:
            xbox.tap_down()
        else:
            xbox.tap_up()
    wait_frames(1)


def side_to_side_direction(current_menu_position, target_menu_position, menu_size):
    distance = abs(current_menu_position - target_menu_position)
    distance_unsigned = current_menu_position - target_menu_position
    logger.debug(f"Menu Size: {menu_size}")
    halfmenusize = menu_size / 2
    if distance == halfmenusize:
        logger.debug("Marker 1")
        xbox.tap_left()
    elif distance < halfmenusize:
        if distance_unsigned > 0:
            logger.debug("Marker 2")
            xbox.tap_right()
        else:
            logger.debug("Marker 3")
            xbox.tap_left()
    else:
        if distance_unsigned > 0:
            logger.debug("Marker 4")
            xbox.tap_left()
        else:
            logger.debug("Marker 5")
            xbox.tap_right()


def party_format_cursor_1():
    global base_value

    coord = base_value + 0x0147151C
    ret_val = process.read_bytes(coord, 1)
    return ret_val


def party_format_cursor_2():
    global base_value

    coord = base_value + 0x01471520
    ret_val = process.read_bytes(coord, 1)
    return ret_val


def name_from_number(char_num):
    if char_num == 0:
        return "Tidus"
    if char_num == 1:
        return "Yuna"
    if char_num == 2:
        return "Auron"
    if char_num == 3:
        return "Kimahri"
    if char_num == 4:
        return "Wakka"
    if char_num == 5:
        return "Lulu"
    if char_num == 6:
        return "Rikku"
    if char_num == 9:
        return "Killing_Blow"


def get_actor_array_size():
    global base_value
    return process.read(base_value + 0x01FC44E0)


def get_actors_loaded():
    global base_value
    base_pointer = base_value + 0x01FC44E4
    base_pointer_address = process.read(base_pointer)
    array = []
    for i in range(get_actor_array_size()):
        array.append(process.read_bytes((0x880 * i) + base_pointer_address, 2))
    return array


def get_actor_id(actor_num):
    actor_index = actor_num
    global base_value
    base_pointer = base_value + 0x01FC44E4
    base_pointer_address = process.read(base_pointer)
    offset_x = 0x880 * actor_index
    return process.read_bytes(base_pointer_address + offset_x, 2)


def get_actor_coords(actor_index):
    global process
    global base_value
    ret_val = [0, 0, 0]
    try:
        base_pointer = base_value + 0x01FC44E4
        base_pointer_address = process.read(base_pointer)
        offset_x = (0x880 * actor_index) + 0x0C
        offset_y = (0x880 * actor_index) + 0x14
        offset_z = (0x880 * actor_index) + 0x10

        key_x = base_pointer_address + offset_x
        ret_val[0] = float_from_integer(process.read(key_x))
        key_y = base_pointer_address + offset_y
        ret_val[1] = float_from_integer(process.read(key_y))
        key_z = base_pointer_address + offset_z
        ret_val[2] = float_from_integer(process.read(key_z))

        return ret_val
    except Exception:
        pass


def get_actor_angle(actor_number):
    global process
    global base_value
    try:
        base_pointer = base_value + 0x01FC44E4
        base_pointer_address = process.read(base_pointer)
        offset = (0x880 * actor_number) + 0x158
        ret_val = float_from_integer(process.read(base_pointer_address + offset))
        return ret_val
    except Exception:
        pass


def miihen_guy_coords():
    spear_guy = 255
    for x in range(get_actor_array_size()):
        actor_num = get_actor_id(x)
        if actor_num == 0x202D:
            spear_guy = x
    return get_actor_coords(spear_guy)


def distance(actor_index: int, alt_index:int = 0):
    # Assume index is passed in.
    try:
        actor_coords = get_actor_coords(actor_index=actor_index)
        player_coords = get_actor_coords(actor_index=alt_index)
        distance = sqrt(
            ((player_coords[0] - actor_coords[0]) ** 2)
            + ((player_coords[1] - actor_coords[1]) ** 2)
        )
        return int(distance)
    except:
        return 0


def actor_index(actor_num: int = 41):
    # If non-unique, choose the closest one.
    actor_index = 255
    for x in range(get_actor_array_size()):
        actor_mem = get_actor_id(x)
        if actor_num == actor_mem:
            if actor_index == 255 or distance(actor_index) > distance(x):
                actor_index = x
    return actor_index


def mrr_guy_coords():
    logger.debug("Searching for MRR guy")
    mrr_guy = 255
    for x in range(get_actor_array_size()):
        actor_num = get_actor_id(x)
        # logger.debug(f"Actor {x}: {hex(actor_num)}")
        if actor_num == 0x2083:
            mrr_guy = x
    logger.debug(f"MRR guy in position: {mrr_guy}")
    mrr_guy_pos = get_actor_coords(mrr_guy)
    return [mrr_guy_pos[0], mrr_guy_pos[1]]


def lucille_miihen_coords():
    return get_actor_coords(8)


def lucille_djose_coords():
    return get_actor_coords(11)


def lucille_djose_angle():
    global process
    global base_value
    ret_val = [0, 0]

    base_pointer = base_value + 0x01FC44E4
    base_pointer_address = process.read(base_pointer)
    offset_x = 0x91D8
    offset_y = 0x91E8

    key_x = base_pointer_address + offset_x
    ret_val[0] = float_from_integer(process.read(key_x))
    key_y = base_pointer_address + offset_y
    ret_val[1] = float_from_integer(process.read(key_y))

    return ret_val


def affection_array():
    global process
    global base_value

    tidus = 255
    key = base_value + 0x00D2CAC0
    yuna = process.read_bytes(key, 1)
    key = base_value + 0x00D2CAC4
    auron = process.read_bytes(key, 1)
    key = base_value + 0x00D2CAC8
    kimahri = process.read_bytes(key, 1)
    key = base_value + 0x00D2CACC
    wakka = process.read_bytes(key, 1)
    key = base_value + 0x00D2CAD0
    lulu = process.read_bytes(key, 1)
    key = base_value + 0x00D2CAD4
    rikku = process.read_bytes(key, 1)

    return [tidus, yuna, auron, kimahri, wakka, lulu, rikku]


def overdrive_state():
    global process
    global base_value
    ret_val = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    x = 0

    base_pointer = base_value + 0x00386DD4
    base_pointer_address = process.read(base_pointer)
    for x in range(20):
        offset = (0x94 * x) + 0x39
        ret_val[x] = process.read_bytes(base_pointer_address + offset, 1)
    logger.debug(f"Overdrive values: {ret_val}")
    return ret_val


def overdrive_state_2():
    global process
    global base_value
    ret_val = [0, 0, 0, 0, 0, 0, 0]
    x = 0
    base_pointer = base_value + 0x003AB9B0
    base_pointer_address = process.read(base_pointer)
    for x in range(7):
        offset = (0x94 * x) + 0x39
        ret_val[x] = process.read_bytes(base_pointer_address + offset, 1)
    logger.debug(f"Overdrive values: {ret_val}")
    return ret_val


def fill_overdrive(character:int=1):
    global process
    global base_value
    x = 0
    base_pointer = base_value + 0x003AB9B0
    base_pointer_address = process.read(base_pointer)
    for x in range(20):
        offset = (0x94 * x) + 0x39
        if character == x:
            if x < 7:
                process.write_bytes(base_pointer_address + offset, 100, 1)
            else:
                process.write_bytes(base_pointer_address + offset, 20, 1)


def char_luck(character: int = 0):
    global process
    global base_value
    base_pointer = base_value + 0x003AB9B0
    base_pointer_address = process.read(base_pointer)
    offset = (0x94 * character) + 0x34
    ret_val = process.read_bytes(base_pointer_address + offset, 1)
    return ret_val


def char_accuracy(character: int = 0):
    global process
    global base_value
    base_pointer = base_value + 0x003AB9B0
    base_pointer_address = process.read(base_pointer)
    offset = (0x94 * character) + 0x36
    ret_val = process.read_bytes(base_pointer_address + offset, 1)
    return ret_val


def consecutive_reached():
    global base_value
    return process.read_bytes(base_value + 0xD2CE90,1)

def dodge_lightning(l_dodge_num):
    global base_value

    if l_strike_count() != l_dodge_num or (l_strike_count() == 1 and l_dodge_num == 0):
        if get_game_speed() >= 1:
            wait_frames(1)
        else:
            wait_frames(5)
        xbox.menu_b()
        if get_game_speed() >= 1:
            wait_frames(3)
        else:
            wait_frames(5)
        logger.warning(f"(Memory) DODGE: {process.read_bytes(base_value + 0xD2CE90,1)}")
        return True
    else:
        return False


def l_strike_count():
    global base_value

    key = base_value + 0x00D2CE8C
    return process.read_bytes(key, 2)


def l_dodge_count():
    global base_value

    key = base_value + 0x00D2CE8E
    return process.read_bytes(key, 2)


def cactuar_stone_4():
    global base_value

    return process.read_bytes(base_value + 0x92CF00,1)


def save_popup_cursor():
    global base_value

    key = base_value + 0x0146780A
    return process.read_bytes(key, 1)


def save_conf_cursor():
    global base_value

    key = base_value + 0x008E72F0
    return process.read_bytes(key, 1)


def diag_progress_flag():
    global base_value

    key = base_value + 0x00F25A80
    return process.read_bytes(key, 4)


def click_to_diag_progress(num, force=False):
    logger.debug(f"Clicking to dialog progress: {num}")
    last_num = diag_progress_flag()
    while diag_progress_flag() != num:
        if user_control():
            return False
        elif force:
            xbox.tap_b()
            #logger.debug("Tapping Confirm")
        elif not game_vars.story_mode():
            xbox.tap_b()
            #logger.debug("Tapping Confirm")
        if diag_progress_flag() != last_num:
            last_num = diag_progress_flag()
            logger.debug(
                f"Dialog change: {diag_progress_flag()} - clicking to {num}"
            )
    return True


def set_encounter_rate(set_val):
    global base_value

    key = base_value + 0x008421C8
    process.write_bytes(key, set_val, 1)


def get_game_speed():
    return read_val(0x008E82A4)


def set_game_speed(set_val):
    global base_value

    key = base_value + 0x008E82A4
    process.write_bytes(key, set_val, 1)


def print_rng_36():
    global base_value

    coord = base_value + 0x00D35F68
    ret_val = process.read_bytes(coord, 1)
    logger.debug(f"RNG36 value: {ret_val}")


def end():
    global process
    process.close()
    logger.info("Memory reading process is now closed.")


def get_frame_count():
    global base_value
    key = base_value + 0x0088FDD8
    return process.read_bytes(key, 4)


def name_aeon_ready():
    global base_value
    key = base_value + 0x01440A30
    return process.read_bytes(key, 1)


# Naming
def get_naming_menu():
    return read_val(0x0146A22C)


def get_naming_index():
    return read_val(0x0146A228)


def name_has_characters():
    return read_val(0x0146A240)


# ------------------------------
# Egg hunt section
def egg_x(egg_num):
    global process
    global base_value
    egg_num += 23
    base_pointer = base_value + 0x1FC44E4
    base_pointer_address = process.read(base_pointer)
    key = base_pointer_address + (0x880 * egg_num) + 0x0C
    ret_val = float_from_integer(process.read(key))
    return ret_val


def egg_y(egg_num):
    global process
    global base_value
    egg_num += 23
    base_pointer = base_value + 0x1FC44E4
    base_pointer_address = process.read(base_pointer)
    key = base_pointer_address + (0x880 * egg_num) + 0x14
    ret_val = float_from_integer(process.read(key))
    return ret_val


def get_egg_distance(egg_num):
    global process
    global base_value
    base_pointer = base_value + 0xF270B8
    base_pointer_address = process.read(base_pointer)
    key = base_pointer_address + 0x1C4CC + (0x40 * egg_num)
    ret_val = float_from_integer(process.read(key))
    return ret_val


def get_egg_life(egg_num):
    global process
    global base_value
    base_pointer = base_value + 0xF270B8
    base_pointer_address = process.read(base_pointer)
    key = base_pointer_address + 0x1C4CC + (0x40 * egg_num) + 4
    ret_val = process.read_bytes(key, 1)
    return ret_val


def get_egg_picked(egg_num):
    global process
    global base_value
    base_pointer = base_value + 0xF270B8
    base_pointer_address = process.read(base_pointer)
    key = base_pointer_address + 0x1C4CC + (0x40 * egg_num) + 5
    ret_val = process.read_bytes(key, 1)
    return ret_val


class Egg:
    def __init__(self, egg_num):
        self.num = egg_num
        self.x = egg_x(self.num)
        self.y = egg_y(self.num)
        self.distance = get_egg_distance(self.num)
        self.egg_life = get_egg_life(egg_num)
        self.egg_picked = get_egg_picked(egg_num)

        if self.distance != 0 and self.egg_picked == 0:
            self.is_active = True
        else:
            self.is_active = False

        if self.egg_picked == 1:
            self.go_for_egg = False
        elif self.egg_life > 100 and self.distance > 100:
            self.go_for_egg = False
        elif self.distance > 250:
            self.go_for_egg = False
        elif self.distance == 0:
            self.go_for_egg = False
        else:
            self.go_for_egg = True

    def report_vars(self):
        var_array = [
            self.num,
            self.is_active,
            self.x,
            self.y,
            150 - self.egg_life,
            self.egg_picked,
            self.distance,
        ]
        logger.debug("Egg_num, Is_Active, X, Y, Egg Life, Picked up, distance")
        logger.debug(f"  {var_array}")


def build_eggs():
    ret_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for x in range(10):
        ret_array[x] = Egg(x)
    return ret_array


def ice_x(actor):
    global process
    global base_value
    # Icicle 0 is actor 7 in the array, incremented for each additional icicle.
    offset = actor + 7

    base_pointer = base_value + 0x1FC44E4
    base_pointer_address = process.read(base_pointer)
    key = base_pointer_address + (0x880 * offset) + 0x0C
    ret_val = float_from_integer(process.read(key))
    return ret_val


def ice_y(actor):
    global process
    global base_value
    # Icicle 0 is actor 7 in the array, incremented for each additional icicle.
    offset = actor + 7

    base_pointer = base_value + 0x1FC44E4
    base_pointer_address = process.read(base_pointer)
    key = base_pointer_address + (0x880 * offset) + 0x14
    ret_val = float_from_integer(process.read(key))
    return ret_val


def get_ice_distance(ice_num):
    global process
    global base_value
    base_pointer = base_value + 0xF270B8
    base_pointer_address = process.read(base_pointer)
    key = base_pointer_address + 0x1C0CC + (0x40 * ice_num)
    ret_val = float_from_integer(process.read(key))
    return ret_val


def get_ice_life(ice_num):
    global process
    global base_value
    base_pointer = base_value + 0xF270B8
    base_pointer_address = process.read(base_pointer)
    key = base_pointer_address + 0x1C0CC + (0x40 * ice_num) + 4
    ret_val = process.read_bytes(key, 1)
    return ret_val


class Icicle:
    def __init__(self, ice_num):
        self.num = ice_num
        self.x = ice_x(self.num)
        self.y = ice_y(self.num)
        self.is_active = True

    def report_vars(self):
        var_array = [self.num, self.x, self.y]
        logger.debug("Ice_num, X, Y")
        logger.debug(f"  {var_array}")


def build_icicles():
    ret_array: List[Icicle] = [Icicle(x) for x in range(16)]
    return ret_array


# ------------------------------
# Soft reset section


def set_map_reset():
    global base_value

    key = base_value + 0x00D2CA90
    process.write_bytes(key, 23, 2)


def force_map_load():
    global base_value

    key = base_value + 0x00F3080C
    process.write_bytes(key, 1, 1)


def reset_battle_end():
    global base_value
    key = base_value + 0x00D2C9F1
    process.write_bytes(key, 1, 1)


def set_rng_by_index(value: int = 0, index: int = 1):
    global base_value
    global process
    key = base_value + 0x00D35ED8 + (index * 0x4)
    process.write_bytes(key, value, 4)


def set_rng_2():
    global base_value
    global process
    key = base_value + 0x00D35EE0
    process.write_bytes(key, 0x7E9F20D2, 4)


# ------------------------------
# Blitzball!


class BlitzActor:
    def __init__(self, player_num: int):
        self.num = player_num
        self.position = get_actor_coords(self.num)
        self.distance = 0

    def update_coords(self, active_player=12):
        self.position = get_actor_coords(self.num + 2)
        self.distance = 100

    def get_coords(self):
        coords = get_actor_coords(self.num)
        return coords

    def current_hp(self):
        return blitz_hp(self.num)

    def aggro(self):
        return get_blitz_aggro(self.num)


def get_blitz_aggro(player_index: int = 99):
    global base_value
    ptr_key = process.read(base_value + 0x00F2FF14)
    if player_index == 6:
        offset = 0x2DC35
    elif player_index == 7:
        offset = 0x343E5
    elif player_index == 8:
        offset = 0x3AB95
    elif player_index == 9:
        offset = 0x41345
    elif player_index == 10:
        offset = 0x47AF5

    if player_index in [6, 7, 8, 9, 10]:
        if process.read_bytes(ptr_key + offset, 1) == 255:
            return False
        else:
            return True
    else:
        return False


def blitz_hp(player_index=99):
    global base_value
    if player_index == 99:
        return 9999
    else:
        ptr_key = process.read(base_value + 0x00F2FF14)
        offset = 0x1C8 + (0x4 * player_index)
        hp_value = process.read(ptr_key + offset)
        return hp_value


def blitz_own_score():
    global base_value
    key = base_value + 0x00D2E0CE
    score = process.read_bytes(key, 1)
    return score


def blitz_opp_score():
    global base_value
    key = base_value + 0x00D2E0CF
    score = process.read_bytes(key, 1)
    return score


def blitzball_patriots_style():
    global base_value

    key = base_value + 0x00D2E0CE
    process.write_bytes(key, 50, 1)


def blitz_clock_menu():
    global base_value
    key = base_value + 0x014765FA
    status = process.read_bytes(key, 1)
    return status


def blitz_clock_pause():
    global base_value
    key = base_value + 0x014663B0
    status = process.read_bytes(key, 1)
    return status


def blitz_menu_num():
    global base_value
    # 20 = Movement menu (auto, type A, or type B)
    # 29 = Formation menu
    # 38 = Breakthrough
    # 24 = Pass To menu (other variations are set to 24)
    # Unsure about other variations, would take more testing.

    key = base_value + 0x014765DA
    status = process.read_bytes(key, 1)
    if status == 17 or status == 27:
        status = 24
    return status


def reset_blitz_menu_num():
    global base_value
    key = base_value + 0x014765DA
    process.write_bytes(key, 1, 1)


def blitz_current_player():
    global base_value

    key = base_value + 0x00F25B6A
    player = process.read_bytes(key, 1)
    return player


def blitz_target_player():
    global base_value

    key = base_value + 0x00D3761C
    player = process.read_bytes(key, 1)
    return player


def blitz_coords():
    global base_value

    key = base_value + 0x00D37698
    x_val = process.read_bytes(key, 1)
    x_val = x_val * -1
    key = base_value + 0x00D37690
    y_val = process.read_bytes(key, 1)
    return [x_val, y_val]


def blitz_game_active():
    if get_map() == 62:
        return True
    else:
        return False


def blitz_clock():
    global base_value

    base_pointer = base_value + 0x00F2FF14
    base_pointer_address = process.read(base_pointer)
    key = base_pointer_address + 0x24C
    clock_value = process.read(key)
    return clock_value


def blitz_char_select_cursor():
    global base_value

    key = base_value + 0x0146780A
    cursor = process.read_bytes(key, 1)
    return cursor


def blitz_proceed_cursor():
    global base_value

    key = base_value + 0x01467CEA
    cursor = process.read_bytes(key, 1)
    return cursor


def blitz_cursor():
    global base_value

    key = base_value + 0x014676D2
    cursor = process.read_bytes(key, 1)
    return cursor


def blitz_league_prizes():
    # 0x0120 for Status Reels
    # 0x0018 for Jupiter Sigil
    global base_value
    ret_val = [0,0,0,0]
    for i in range(3):
        # First, second, third place prizes.
        key = base_value + 0xD2E48C + (i*2)
        ret_val[i] = process.read_bytes(key, 2)

    # Top scorer
    key = base_value + 0xD2E498
    ret_val[3] = process.read_bytes(key, 2)
    return ret_val


def blitz_tournament_prizes():
    # 0x011F for Attack Reels
    # 0x0121 for Auroch Reels
    global base_value
    ret_val = [0,0,0,0]
    for i in range(3):
        # First, second, third place prizes.
        key = base_value + 0xD2E492 + (i*2)
        ret_val[i] = process.read_bytes(key, 2)

    # Top scorer
    key = base_value + 0xD2E49A
    ret_val[3] = process.read_bytes(key, 2)
    return ret_val


def blitz_tournament_active():
    return bool(blitz_tournament_prizes()[3] != 0)


def wakka_total_battles():
    global base_value
    ret_val = process.read_bytes(base_value + 0xD322FC, 4)
    return ret_val


def rikku_total_steals():
    global base_value
    ret_val = process.read_bytes(base_value + 0xD30840, 4)
    return ret_val


def wakka_od_learned():
    global base_value
    ret_val = process.read_bytes(base_value + 0xD307FE, 1)
    byte_val = ret_val[0] if isinstance(ret_val, (bytes, bytearray)) else ret_val
    learned_array = [
        bool(byte_val & (1 << 4)),
        bool(byte_val & (1 << 5)),
        bool(byte_val & (1 << 6)),
        bool(byte_val & (1 << 7))
    ]
    return learned_array



def rikku_learned_flee():
    global base_value
    ret_val = process.read_bytes(base_value + 0xD32415, 1)
    byte_val = ret_val[0] if isinstance(ret_val, (bytes, bytearray)) else ret_val
    return bool(byte_val & (1 << 0))



# ------------------------------
# Function for logging


def total_distance_travelled():
    return float_from_integer(read_val(0x00D2A9DC, 4))


def get_zone():
    return read_val(0x00D2CAA0, 2)


# ------------------------------
# Equipment array

# 0x0 - ushort - name/group (?)
# 0x3 - byte - wpn./arm. state
# 0x4 - byte - owner char (basis for field below)
# 0x5 - byte - equip type idx. (
#              0 = cur. chara wpn.,
#              1 = cur. chara arm.,
#              2 = next chara wpn., etc.)
# 0x6 - byte - equip icon shown?
#              (purely visual - a character will still keep it equipped
#              if his stat struct says so)
# 0x8 - byte - atk. type
# 0x9 - byte - dmg. constant
# 0xA - byte - base crit rate (armor has one too!!!)
# 0xB - byte - slot count (cannot be < abi count, game won't let you)
# 0xC - ushort - wpn./arm. model (?)
# 0xE - ushort - auto-ability 1
# 0x10 - ushort - auto-ability 2
# 0x12 - ushort - auto-ability 3
# 0x14 - ushort - auto-ability 4


def get_equip_type(equip_num):
    global base_value

    base_pointer = base_value + 0x00D30F2C
    key = base_pointer + (0x16 * equip_num) + 0x05
    ret_val = process.read_bytes(key, 1)
    return ret_val


def get_equip_legit(equip_num):
    #return True
    global base_value
    report = False  # Reports illegitimate equipments for troubleshooting.

    base_pointer = base_value + 0x00D30F2C
    key = base_pointer + (0x16 * equip_num) + 0x03
    ret_val = process.read_bytes(key, 1)
    if not get_equip_exists(equip_num=equip_num):
        #logger.debug(f"Equip num/pos {equip_num} does not exist.")
        return False
    if report:
        logger.warning(f"========Legitimacy check {equip_num}=========")
        logger.warning(f"Owner: {get_equip_owner(equip_num=equip_num)}")
        if get_equip_type(equip_num) == 1:
            type_val = "Armor"
        else:
            type_val = "Weapon"
        logger.warning(f"Type: {type_val}")
        logger.warning(f"Legitimacy: {ret_val}")
        logger.warning(f"Abilities: {get_equip_abilities(equip_num=equip_num)}")
        logger.warning("====================================")
    if ret_val in [0, 8, 9]:
        return True
    if ret_val == 4 and 32793 in get_equip_abilities(equip_num=equip_num):
        return True
    return False


def is_equip_brotherhood(equip_num):
    if get_equip_owner(equip_num) == 0:
        global base_value
        base_pointer = base_value + 0x00D30F2C
        key = base_pointer + (0x16 * equip_num) + 0x03
        ret_val = process.read_bytes(key, 1)
        if ret_val == 9:
            return True
    return False


def get_equip_owner(equip_num):
    global base_value

    base_pointer = base_value + 0x00D30F2C
    key = base_pointer + (0x16 * equip_num) + 0x04
    ret_val = process.read_bytes(key, 1)
    return ret_val


def get_equip_slot_count(equip_num):
    global base_value

    base_pointer = base_value + 0x00D30F2C
    key = base_pointer + (0x16 * equip_num) + 0x0B
    ret_val = process.read_bytes(key, 1)
    return ret_val


def get_equip_currently_equipped(equip_num):
    global base_value

    base_pointer = base_value + 0x00D30F2C
    key = base_pointer + (0x16 * equip_num) + 0x06
    ret_val = process.read_bytes(key, 1)
    return ret_val


def get_equip_abilities(equip_num):
    global base_value
    ret_val = [255, 255, 255, 255]

    base_pointer = base_value + 0x00D30F2C
    key = base_pointer + (0x16 * equip_num) + 0x0E
    ret_val[0] = process.read_bytes(key, 2)
    key = base_pointer + (0x16 * equip_num) + 0x10
    ret_val[1] = process.read_bytes(key, 2)
    key = base_pointer + (0x16 * equip_num) + 0x12
    ret_val[2] = process.read_bytes(key, 2)
    key = base_pointer + (0x16 * equip_num) + 0x14
    ret_val[3] = process.read_bytes(key, 2)
    return ret_val


def get_equip_exists(equip_num):
    global base_value

    base_pointer = base_value + 0x00D30F2C
    key = base_pointer + (0x16 * equip_num) + 0x02
    ret_val = process.read_bytes(key, 1)

    return ret_val


class Equipment:
    def __init__(self, equip_num):
        self.num = equip_num
        self.equip_type = get_equip_type(equip_num)
        self.equip_owner = get_equip_owner(equip_num)
        self.equip_owner_alt = get_equip_owner(equip_num)
        self.equip_abilities = get_equip_abilities(equip_num)
        self.equip_status = get_equip_currently_equipped(equip_num)
        self.slots = get_equip_slot_count(equip_num)
        self.exists = get_equip_exists(equip_num)
        self.brotherhood = is_equip_brotherhood(equip_num)

    def create_custom(
        self, e_type: int, e_owner_1: int, e_owner_2: int, e_slots: int, e_abilities
    ):
        self.equip_type = e_type
        self.equip_owner = e_owner_1
        self.equip_owner_alt = e_owner_2
        self.equip_abilities = e_abilities
        self.equip_status = 0
        self.slots = e_slots
        self.exists = 1
        self.brotherhood = False

    def equipment_type(self):
        return self.equip_type

    def owner(self):
        return self.equip_owner

    def owner_alt(self):
        return self.equip_owner_alt

    def abilities(self):
        return self.equip_abilities

    def has_ability(self, ability_num):
        if ability_num in self.equip_abilities:
            return True
        return False

    def is_equipped(self):
        return self.equip_status

    def slot_count(self):
        return self.slots

    def equip_exists(self):
        return self.exists

    def is_brotherhood(self):
        return self.brotherhood


def all_equipment():
    first_equipment = True
    for i in range(200):
        current_handle = Equipment(i)
        if get_equip_legit(i) and current_handle.equip_exists():
            if first_equipment:
                equip_handle_array = [Equipment(i)]
                first_equipment = False
            else:
                equip_handle_array.append(Equipment(i))
    return equip_handle_array


def weapon_array_character(char_num):
    equip_handles = all_equipment()
    first_equipment = True
    char_weaps = []
    while len(equip_handles) > 0:
        current_handle = equip_handles.pop(0)
        #logger.debug("===========================")
        #logger.debug(f"Owner: {current_handle.owner()}")
        #logger.debug(f"Type (0 for weapon): {current_handle.equipment_type()}")
        #logger.debug(f"Abilities: {current_handle.abilities()}")
        #logger.debug("===========================")
        if current_handle.owner() == char_num and current_handle.equipment_type() == 0:
            if first_equipment:
                char_weaps = [current_handle]
                first_equipment = False
            else:
                char_weaps.append(current_handle)
    return char_weaps


def equipped_weapon_has_ability(char_num: int = 1, ability_num: int = 32769):
    equip_handles = weapon_array_character(char_num)
    while len(equip_handles) > 0:
        current_handle = equip_handles.pop(0)
        if current_handle.is_equipped() == char_num:
            # logger.debug(f"Owner: {current_handle.owner()}")
            # logger.debug(f"Equipped: {current_handle.is_equipped()}")
            # logger.debug(f"Has Ability: {current_handle.has_ability(ability_num)}")
            if current_handle.has_ability(ability_num):
                return True
            else:
                return False


def check_thunder_strike() -> int:
    results = 0
    tidus_weaps = weapon_array_character(0)
    while len(tidus_weaps) > 0:
        current_handle = tidus_weaps.pop(0)
        if current_handle.has_ability(0x8026):
            results += 1
            break

    wakka_weaps = weapon_array_character(4)
    while len(wakka_weaps) > 0:
        current_handle = wakka_weaps.pop(0)
        if current_handle.has_ability(0x8026):
            results += 2
            break
    return results


def check_zombie_strike():
    ability = 0x8032

    char_weaps = weapon_array_character(0)  # Tidus
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            game_vars.set_zombie(0)
            return True

    char_weaps = weapon_array_character(1)  # Yuna
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            game_vars.set_zombie(1)
            return True

    char_weaps = weapon_array_character(2)  # Auron
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            game_vars.set_zombie(2)
            return True

    char_weaps = weapon_array_character(3)  # Kimahri
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            game_vars.set_zombie(3)
            return True

    char_weaps = weapon_array_character(4)  # Wakka
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            game_vars.set_zombie(4)
            return True

    char_weaps = weapon_array_character(5)  # Lulu
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            game_vars.set_zombie(5)
            return True

    char_weaps = weapon_array_character(6)  # Rikku
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            game_vars.set_zombie(6)
            return True

    return False


def check_ability(ability=0x8032):
    results = [False, False, False, False, False, False, False]

    char_weaps = weapon_array_character(0)  # Tidus
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            results[0] = True

    char_weaps = weapon_array_character(1)  # Yuna
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            results[1] = True

    char_weaps = weapon_array_character(2)  # Auron
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            results[2] = True

    char_weaps = weapon_array_character(3)  # Kimahri
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            results[3] = True

    char_weaps = weapon_array_character(4)  # Wakka
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            results[4] = True

    char_weaps = weapon_array_character(5)  # Lulu
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            results[5] = True
    try:
        char_weaps = weapon_array_character(6)  # Rikku
        while len(char_weaps) > 0:
            current_handle = char_weaps.pop(0)
            if current_handle.has_ability(ability):
                results[6] = True
    except Exception:
        # Rikku not yet in the party.
        results[6] = False

    return results


def check_ability_armor(ability=0x8032, slot_count: int = 99):
    results = [False, False, False, False, False, False, False]

    char_weaps = armor_array_character(0)  # Tidus
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            if slot_count != 99:
                if current_handle.slot_count() != slot_count:
                    results[0] = False
                else:
                    results[0] = True
            else:
                results[0] = True

    char_weaps = armor_array_character(1)  # Yuna
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            if slot_count != 99:
                if current_handle.slot_count() != slot_count:
                    results[1] = False
                else:
                    results[1] = True
            else:
                results[1] = True

    char_weaps = armor_array_character(2)  # Auron
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            if slot_count != 99:
                if current_handle.slot_count() != slot_count:
                    results[2] = False
                else:
                    results[2] = True
            else:
                results[2] = True

    char_weaps = armor_array_character(3)  # Kimahri
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            if slot_count != 99:
                if current_handle.slot_count() != slot_count:
                    results[3] = False
                else:
                    results[3] = True
            else:
                results[3] = True

    char_weaps = armor_array_character(4)  # Wakka
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            if slot_count != 99:
                if current_handle.slot_count() != slot_count:
                    results[4] = False
                else:
                    results[4] = True
            else:
                results[4] = True

    char_weaps = armor_array_character(5)  # Lulu
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            if slot_count != 99:
                if current_handle.slot_count() != slot_count:
                    results[5] = False
                else:
                    results[5] = True
            else:
                results[5] = True

    char_weaps = armor_array_character(6)  # Rikku
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        logger.debug(current_handle.abilities())
        if current_handle.has_ability(ability):
            if slot_count != 99:
                if current_handle.slot_count() != slot_count:
                    results[6] = False
                else:
                    results[6] = True
            else:
                results[6] = True
        logger.debug(results[6])

    return results


def weapon_armor_cursor():
    global base_value
    return process.read_bytes(base_value + 0x0146A5E4, 1)


def customize_menu_array():
    ret_array = []
    global base_value
    for x in range(60):
        offset = 0x1197730 + (x * 4)
        ret_array.append(process.read_bytes(base_value + offset, 2))
    return ret_array


def check_nea_armor():
    ability = 0x801D

    char_weaps = armor_array_character(1)  # Yuna
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            game_vars.set_ne_armor(1)
            return True

    char_weaps = armor_array_character(2)  # Auron
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            game_vars.set_ne_armor(2)
            return True

    char_weaps = armor_array_character(3)  # Kimahri
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            game_vars.set_ne_armor(3)
            return True

    char_weaps = armor_array_character(5)  # Lulu
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            game_vars.set_ne_armor(5)
            return True

    char_weaps = armor_array_character(4)  # Wakka
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            game_vars.set_ne_armor(4)
            return True

    char_weaps = armor_array_character(6)  # Rikku
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            game_vars.set_ne_armor(6)
            return True

    char_weaps = armor_array_character(0)  # Tidus
    while len(char_weaps) > 0:
        current_handle = char_weaps.pop(0)
        if current_handle.has_ability(ability):
            game_vars.set_ne_armor(0)
            return True

    return False


def shop_menu_dialogue_row():
    return read_val(0x0146780A)


def airship_shop_dialogue_row():
    return read_val(0x014676D2)


def hunter_spear():
    kim_weap_handles = weapon_array_character(3)
    if len(kim_weap_handles) == 1:
        return False
    else:
        while len(kim_weap_handles) > 0:
            current_handle = kim_weap_handles.pop(0)
            if current_handle.abilities() == [0x800B, 0x8000, 0x8064, 0x00FF]:
                return True
    return False


def armor_array_character(char_num):
    equip_handles = all_equipment()
    first_equipment = True
    char_weaps = []
    while len(equip_handles) > 0:
        current_handle = equip_handles.pop(0)
        if current_handle.owner() == char_num and current_handle.equipment_type() == 1:
            if first_equipment:
                char_weaps = [current_handle]
                first_equipment = False
            else:
                char_weaps.append(current_handle)
    try:
        return char_weaps
    except Exception:
        return []


def equipped_armor_has_ability(char_num: int, ability_num: int = 0x801D):
    try:
        equip_handles = armor_array_character(char_num)
        while len(equip_handles) > 0:
            current_handle = equip_handles.pop(0)
            if current_handle.is_equipped() == char_num:
                if current_handle.has_ability(ability_num):
                    return True
                else:
                    return False
        return False
    except:
        return False


def equip_weap_cursor():
    global base_value

    key = base_value + 0x01440A38
    ret_val = process.read_bytes(key, 1)
    return ret_val


def assign_ability_to_equip_cursor():
    global base_value
    key = base_value + 0x01440AD0
    ret_val = process.read_bytes(key, 1)
    return ret_val


def item_heal_character_cursor():
    global base_value
    key = base_value + 0x01440B68
    ret_val = process.read_bytes(key, 1)
    return ret_val

# ------------------------------
# Shopping related stuff


def item_shop_menu():
    global base_value
    key = base_value + 0x0085A860
    ret_val = process.read_bytes(key, 1)
    return ret_val


def equipment_sell_ready():
    return equipment_shop_prompts() == 25


def equipment_sell_prompt_open():
    return equipment_shop_prompts() == 31


def equipment_buy_ready():
    return equipment_shop_prompts() == 12


def equipment_buy_prompt_open():
    return equipment_shop_prompts() == 18


def equipment_shop_prompts():
    global base_value
    key = base_value + 0x0085A83C
    return process.read_bytes(key, 1)


def equip_shop_menu():
    global base_value
    key = base_value + 0x0085A83C
    ret_val = process.read_bytes(key, 1)
    return ret_val


def heal_menu_open():
    global base_value
    key = base_value + 0x01440A35
    ret_val = process.read_bytes(key, 1)
    return ret_val


def item_menu_number():
    global base_value
    key = base_value + 0x0085A318
    ret_val = process.read_bytes(key, 1)
    return ret_val


def item_menu_column():
    global base_value
    key = base_value + 0x01440A48
    ret_val = process.read_bytes(key, 1)
    return ret_val


def information_active():
    global base_value
    key = base_value + 0x0146AA28
    ret_val = process.read_bytes(key, 1)
    return ret_val == 7


def item_menu_row():
    global base_value
    key = base_value + 0x01440A38
    ret_val = process.read_bytes(key, 1)
    return ret_val


def equip_sell_row():
    global base_value
    key = base_value + 0x01440C00
    ret_val = process.read_bytes(key, 1)
    return ret_val


def name_confirm_open():
    return read_val(0x014408E8) == 8


def equip_buy_row():
    global base_value
    key = base_value + 0x01440B68
    ret_val = process.read_bytes(key, 1)
    return ret_val


def cursor_enabled_in_equip():
    global base_value
    key = base_value + 0x008CC7EC
    ret_val = process.read_bytes(key, 1)
    return ret_val == 12


def equip_confirmation_row():
    global base_value
    key = base_value + 0x01440C98
    ret_val = process.read_bytes(key, 1)
    return ret_val


def equip_menu_open_from_char():
    global base_value
    key = base_value + 0x01440A2A
    ret_val = process.read_bytes(key, 1)
    return ret_val == 5


def config_cursor():
    global base_value
    key = base_value + 0x0146A404
    ret_val = process.read_bytes(key, 1)
    return ret_val


def read_val(address, bytes=1, find_base=True):
    if find_base:
        global base_value
        key = base_value + address
    else:
        key = address
    ret_val = process.read_bytes(key, bytes)
    return ret_val


def spare_change_amount():
    return read_val(0x00F40424, 4)


def oaka_gil_amount():
    return read_val(0x01467A84, 4)


def oaka_gil_cursor():
    return read_val(0x014663A8)


def oaka_interface():
    return read_val(0x00F26D30)


def spare_change_cursor():
    return read_val(0x00F40418)


def spare_change_open():
    return read_val(0x00F3CAF1) == 4


def config_cursor_column():
    global base_value
    key = base_value + 0x0085A3FC
    ret_val = process.read_bytes(key, 1)
    return ret_val


def purchasing_amount_items():
    return read_val(0x01440C00)


def config_aeon_cursor_column():
    global base_value
    key = base_value + 0x0085A454
    ret_val = process.read_bytes(key, 1)
    return ret_val


def load_menu_cursor():
    global base_value
    key = base_value + 0x008E72E0
    ret_val = process.read_bytes(key, 1)
    return ret_val


def rikku_overdrive_item_selected_number():
    global base_value
    key = base_value + 0x00D2C948
    ret_val = process.read_bytes(key, 1)
    return ret_val


def sphere_grid_placement_open():
    global base_value
    key = base_value + 0x012ACB6B
    ret_val = process.read_bytes(key, 1)
    return ret_val


def moving_prompt_open():
    global base_value
    key = base_value + 0x012AD543
    ret_val = process.read_bytes(key, 1)
    return ret_val


# ------------------------------
# Bevelle Trials indicators


def bt_bi_direction():
    key = base_value + 0x0092DEED
    return process.read_bytes(key, 1)


def bt_tri_direction_main():
    key = base_value + 0x0092E1ED
    return process.read_bytes(key, 1)


def via_quad_direction():
    key = base_value + 0x00D2CC84
    return process.read_bytes(key, 1)


# ------------------------------
# Gagazet trials


def gt_outer_ring():
    global base_value
    key = base_value + 0x014DFC34
    height = float_from_integer(process.read(key))
    return height


def gt_inner_ring():
    global base_value
    key = base_value + 0x014DFDA0
    height = float_from_integer(process.read(key))
    return height


# ------------------------------
# Save spheres


def get_save_sphere_details():
    map_val = get_map()
    story_val = get_story_progress()
    logger.debug(f"Map: {map_val} | Story: {story_val}")
    x = 0
    y = 0
    diag = 0
    if map_val == 389:
        # Ammes
        x = 994
        y = -263
        diag = 9
    if map_val == 49:
        # Baaj
        x = 230
        y = -215
        diag = 17
    if map_val == 63:
        # Before Klikk
        x = -100
        y = 143
        diag = 29
    if map_val == 64:
        # Before Tros
        x = 5
        y = -170
        diag = 3
    if map_val == 19:
        # Besaid beach
        x = -310
        y = -475
        diag = 48
    if map_val == 65:
        # Kilika - before Geneaux
        x = -3
        y = 175
        diag = 46
    if map_val == 88:
        # Luca before Oblitzerator
        x = 175
        y = -310
        diag = 62
    if map_val == 123:
        # Luca after Oblitzerator
        x = -270
        y = -45
        diag = 90
    if map_val == 171:
        # Mi'ihen agency
        x = 35
        y = -10
        diag = 85
    if map_val == 115:
        # Old Road
        x = 48
        y = -910
        diag = 40
    if map_val == 59 and get_story_progress() > 1000:
        # Miihen last screen, late game
        x = 15
        y = 125
        diag = 121
    if map_val == 92:
        # MRR
        x = 5
        y = -740
        if get_story_progress() < 1000:
            diag = 39
        else:
            diag = 43  # Nemesis run
    if map_val == 119:
        # Battle Site
        x = -55
        y = 3335
        diag = 115
    if map_val == 110:
        # Mac woods start
        x = 255
        y = -15
        diag = 84
    if map_val == 221:
        # Mac woods before Spherimorph
        x = 195
        y = -123
        if get_story_progress() < 4000:
            diag = 19
        else:
            diag = 23
    if map_val == 106:
        # Mac Temple entrance
        x = -22
        y = -127
        diag = 68
    if map_val == 153:
        # Mac Temple exit
        x = 820
        y = -235
        diag = 44
    if map_val == 129:
        # Bikanel start
        x = 19
        y = -60
        diag = 35
    if map_val == 136:
        # Bikanel Rikku tent
        x = 205
        y = 30
        diag = 59
    if map_val == 130:
        # Home entrance screen
        x = 61
        y = 92
        diag = 25
    if map_val == 208:
        # Highbridge before Natus
        x = 33
        y = 1251
        diag = 124
    if map_val == 194:
        # Airship while rescuing Yuna, cockpit
        x = -275
        y = 344
        if get_story_progress() < 2700:  # During Yuna rescue
            diag = 217
        else:  # Before Shedinja/Highbridge
            diag = 220
    if map_val == 266:
        x = -305
        y = 185
        if get_story_progress() < 3000:  # NEA trip
            diag = 39
        else:
            diag = 43
    if map_val == 285:
        # After Flux
        x = 140
        y = -640
        diag = 84
    if map_val == 316:
        # Just before Zan trials
        x = -20
        y = 358
        diag = 25
    if map_val == 318:
        # Before Yunalesca
        x = -5
        y = -170
        diag = 26
    if map_val == 140:
        # Thunder plains
        x = -45
        y = -870
        diag = 77
    if map_val == 322:  # Nemesis run
        # Inside Sin, next to airship
        x = 225
        y = -250
        diag = 15
    if map_val == 19:  # Nemesis run
        # Besaid beach
        x = -310
        y = -475
        diag = 55
    if map_val == 263:  # Nemesis run
        # Thunder Plains agency
        x = -30
        y = -10
        diag = 114
    if map_val == 307:  # Nemesis run
        # Monster Arena
        x = 4
        y = 5
        diag = 166
    if map_val == 98:  # Nemesis run
        # Kilika docks
        x = 46
        y = -252
        diag = 34
    if map_val == 82:  # Nemesis run
        # Djose temple
        x = 100
        y = -240
        diag = 89
    if map_val == 137:  # Nemesis run
        # Bikanel Desert
        x = -15
        y = 240
        diag = 31
    if map_val == 313:  # Nemesis run
        # Zanarkand campfire
        x = 135
        y = -1
        diag = 4
    if map_val == 327:  # Nemesis run
        # Sin, end zone
        x = -37
        y = -508
        diag = 10
    if map_val == 258:  # Nemesis run
        # Omega (only used in Nemesis)
        x = -112
        y = -1066
        diag = 23
    if map_val == 307:
        # Monster Arena (only used in Nemesis)
        x = 2
        y = 5
        diag = 166
    if map_val == 259:  # Nemesis run
        # Gagazet (only used in Nemesis)
        x = -59
        y = 99
        diag = 219
    if map_val == 82:
        # Djose temple (only used in Nemesis)
        x = 97
        y = -241
        diag = 89
    if map_val == 128:  # Nemesis run
        # MRR upper lift (only used in Nemesis)
        x = 230
        y = 140
        diag = 68
    logger.debug(f"Values: [{x}, {y}] - {diag}")
    return [x, y, diag]


def touch_save_sphere(save_cursor_num: int = 0):
    logger.debug("Touch Save Sphere")
    clear_save_menu_cursor()
    clear_save_menu_cursor_2()
    if not user_control():
        return False

    ss_details = get_save_sphere_details()
    while user_control():
        pathing.set_movement([ss_details[0], ss_details[1]])
        xbox.tap_b()
        wait_frames(1)
    FFXC.set_neutral()
    logger.debug("Waiting for cursor to reset before we do things - Mark 1")
    while menu_control() == 0:
        if battle_active():
            return False
    wait_frames(1)
    logger.debug("Mark 2")
    # wait_frames(300)
    inc = 0

    while not (
        save_menu_cursor() == 0
        and save_menu_cursor_2() == 0
        and diag_progress_flag() == ss_details[2]
    ):
        logger.debug(
            f"Cursor test A: {get_story_progress()} | "
            + f"{diag_progress_flag()} | {get_map()} | {inc}"
        )
        inc += 1
        if save_menu_open():
            xbox.tap_a()
        elif diag_skip_possible() and diag_progress_flag() != ss_details[2]:
            xbox.tap_b()
    while not (save_menu_cursor() == 0 and save_menu_cursor_2() == 0):
        logger.debug(
            f"Cursor test B: {save_menu_cursor()} | "
            + f"{save_menu_cursor_2()} | {diag_skip_possible()} | {inc}"
        )
        inc += 1
        if save_menu_open():
            xbox.tap_a()
        elif diag_skip_possible():
            xbox.tap_a()
    while save_menu_cursor() == 0 and save_menu_cursor_2() == 0:
        logger.debug(
            f"Cursor test C: {save_menu_cursor()} | "
            + f"{save_menu_cursor_2()} | {diag_skip_possible()} | "
            + f"{get_story_progress()} | {inc}"
        )
        inc += 1
        if save_menu_open():
            xbox.tap_a()
        elif diag_skip_possible():
            if diag_progress_flag() != ss_details[2]:
                xbox.tap_b()
            else:
                xbox.tap_a()
    while not user_control():
        logger.debug(
            f"Cursor test D: {save_menu_cursor()} | {save_menu_cursor_2()} | {inc}"
        )
        inc += 1
        if save_menu_open():
            xbox.tap_a()
        else:
            xbox.tap_b()
    logger.debug(
        f"Cursor test E: {save_menu_cursor()} | {save_menu_cursor_2()} | {inc}"
    )
    inc += 1
    return True


def touch_save_sphere_not_working(save_cursor_num: int = 0):
    logger.debug("Touch Save Sphere")

    ss_details = get_save_sphere_details()
    while user_control():
        pathing.set_movement([ss_details[0], ss_details[1]])
        xbox.tap_b()
        wait_frames(1)
    FFXC.set_neutral()
    logger.debug("Waiting for cursor to reset before we do things - Mark 1")
    while menu_control() == 0:
        pass
    wait_frames(1)
    logger.debug("Mark 2")
    # wait_frames(300)

    xbox.tap_a()
    # while save_menu_cursor() == 0:
    #    if save_menu_open():
    #        xbox.tap_a()
    #    elif diag_progress_flag() != ss_details[2] and diag_skip_possible():
    #        xbox.tap_b()
    #    else:
    #        xbox.tap_a()

    while not user_control():
        if save_menu_open():
            xbox.tap_a()
        elif diag_progress_flag() == ss_details[2]:
            logger.debug(f"Cursor test: {save_menu_cursor()}")
            logger.debug(f"Cursor test2: {save_menu_cursor_2()}")
            if save_cursor_num == 0 and save_menu_cursor() == 0:
                xbox.tap_a()
            elif save_cursor_num == 1 and save_menu_cursor_2() == 0:
                xbox.tap_a()
            else:
                xbox.menu_b()
        else:
            xbox.tap_b()
    clear_save_menu_cursor()
    clear_save_menu_cursor_2()


def csr_baaj_save_clear():
    if user_control():
        logger.debug("No need to clear. User is in control.")
    else:
        logger.debug("Save dialog has popped up for some reason. Attempting clear.")
        try:
            FFXC.set_neutral()
        except Exception:
            FFXC.set_neutral()
        while not user_control():
            if save_menu_open():
                xbox.tap_a()
            elif diag_progress_flag() == 109:
                if save_menu_cursor() == 0 and save_menu_cursor_2() == 0:
                    xbox.tap_a()
                else:
                    xbox.tap_b()
                wait_frames(4)

    clear_save_menu_cursor()
    clear_save_menu_cursor_2()


# ------------------------------
# Testing


def mem_test_val_0():
    key = base_value + 0x00D35EE0
    return process.read_bytes(key, 1)


def mem_test_val_1():
    key = base_value + 0x00D35EE1
    return process.read_bytes(key, 1)


def mem_test_val_2():
    key = base_value + 0x00D35EE2
    return process.read_bytes(key, 1)


def mem_test_val_3():
    key = base_value + 0x00D35EE3
    return process.read_bytes(key, 1)


# ------------------------------
# Yojimbo


def yojimbo_compatibility():
    key = base_value + 0x00D30834
    return process.read_bytes(key, 1)


# ------------------------------


def print_memory_log():
    pass


def print_memory_log_backup():
    global base_value
    global process
    # (Pointer) [[ffx.exe + 8DED2C] + 0x6D0]
    ptr_val = process.read(base_value + 0x008DED2C)
    final_coords = ptr_val + 0x6D0
    coord_1 = process.read(final_coords)
    logs.write_stats("Temp Value 1: " + str(coord_1))

    # (Pointer) [[ffx.exe + 8DED2C] + 0x704]
    ptr_val = process.read(base_value + 0x008DED2C)
    final_coords = ptr_val + 0x704
    logs.write_stats("Temp Value 2: " + str(coord_1))

    # (Pointer) [[ffx.exe + 8CB9D8] + 0x10D2E]
    ptr_val = process.read(base_value + 0x008CB9D8)
    final_coords = ptr_val + 0x10D2E
    logs.write_stats("Temp Value 3: " + str(coord_1))

    # ffx.exe + D2A00C
    logs.write_stats("Temp Value 4: " + str(coord_1))


# ------------------------------
# Load game functions


def load_game_page():
    global base_value
    key = base_value + 0x008E72DC
    ret_val = process.read_bytes(key, 1)
    return ret_val


def load_game_cursor():
    global base_value
    key = base_value + 0x008E72E0
    ret_val = process.read_bytes(key, 1)
    return ret_val


def load_game_pos():
    return load_game_page() + load_game_cursor()


def luca_workers_battle_id():
    return read_val(0x01466DCC)


# ------------------------------
# RNG tracking based on the first six hits


def last_hit_init():
    global base_value
    logger.debug("Initializing values")
    key = base_value + 0xD334CC
    ptr_val = process.read(key)
    last_hit_vals = [0] * 8
    try:
        for x in range(8):
            last_hit_vals[x] = process.read(ptr_val + ((x + 20) * 0xF90) + 0x7AC)
            # logger.debug(f"Val: {last_hit_vals[x]}")
        # logger.debug(last_hit_vals)
        game_vars.first_hits_set(last_hit_vals)
        return True
    except Exception:
        return False


def last_hit_check_change() -> int:
    global base_value
    key = base_value + 0xD334CC
    ptr_val = process.read(key)
    change_found = False
    change_value = 9999
    for x in range(8):
        mem_val = process.read(ptr_val + ((x + 20) * 0xF90) + 0x7AC)
        if mem_val != game_vars.first_hits_value(x) and not change_found:
            change_found = True
            change_value = mem_val
            logger.info(f"Registered hit: {change_value}")
            # logs.write_stats(change_value)
            last_hit_init()
            logger.debug("Mark 1")
            return int(change_value)
    return 9999


# ------------------------------
# NE armor manip
RNG_CONSTANTS_1 = (
    2100005341,
    1700015771,
    247163863,
    891644838,
    1352476256,
    1563244181,
    1528068162,
    511705468,
    1739927914,
    398147329,
    1278224951,
    20980264,
    1178761637,
    802909981,
    1130639188,
    1599606659,
    952700148,
    -898770777,
    -1097979074,
    -2013480859,
    -338768120,
    -625456464,
    -2049746478,
    -550389733,
    -5384772,
    -128808769,
    -1756029551,
    1379661854,
    904938180,
    -1209494558,
    -1676357703,
    -1287910319,
    1653802906,
    393811311,
    -824919740,
    1837641861,
    946029195,
    1248183957,
    -1684075875,
    -2108396259,
    -681826312,
    1003979812,
    1607786269,
    -585334321,
    1285195346,
    1997056081,
    -106688232,
    1881479866,
    476193932,
    307456100,
    1290745818,
    162507240,
    -213809065,
    -1135977230,
    -1272305475,
    1484222417,
    -1559875058,
    1407627502,
    1206176750,
    -1537348094,
    638891383,
    581678511,
    1164589165,
    -1436620514,
    1412081670,
    -1538191350,
    -284976976,
    706005400,
)

RNG_CONSTANTS_2 = (
    10259,
    24563,
    11177,
    56952,
    46197,
    49826,
    27077,
    1257,
    44164,
    56565,
    31009,
    46618,
    64397,
    46089,
    58119,
    13090,
    19496,
    47700,
    21163,
    16247,
    574,
    18658,
    60495,
    42058,
    40532,
    13649,
    8049,
    25369,
    9373,
    48949,
    23157,
    32735,
    29605,
    44013,
    16623,
    15090,
    43767,
    51346,
    28485,
    39192,
    40085,
    32893,
    41400,
    1267,
    15436,
    33645,
    37189,
    58137,
    16264,
    59665,
    53663,
    11528,
    37584,
    18427,
    59827,
    49457,
    22922,
    24212,
    62787,
    56241,
    55318,
    9625,
    57622,
    7580,
    56469,
    49208,
    41671,
    36458,
)


def build_rng_array(index: int, array_size: int = 255):
    global base_value
    offset = base_value + 0xD35ED8 + (index * 4)
    array_val = [process.read(offset)]
    for x in range(array_size):
        array_val.append(roll_next_rng(array_val[x], index))
    return array_val


def next_crit(character: int, char_luck: int, enemy_luck: int) -> int:
    # Returns the next time the character will critically strike,
    # counting number of advances from present.
    # If 255 is returned, there will not be a next crit in the foreseeable future.
    results = []
    rng_index = min(20 + character, 27)
    rng_array = rng_array_from_index(index=rng_index, array_len=200)
    crit_chance = char_luck - enemy_luck
    del rng_array[0]
    del rng_array[0]
    for x in range(len(rng_array)):
        crit_roll = rng_array[x] % 101
        if crit_roll < crit_chance:
            results.append(x)
    logger.debug(f"Upcoming crits (advances): {results}")
    if len(results) == 0:
        return 255
    return results[0]


def ambushes(advances: int = 12, extra: int = 0):
    # https://grayfox96.github.io/FFX-Info/rng/encounters
    ret_array = []
    home_check = 99
    rng_array = rng_array_from_index(index=1, array_len=(advances * 2) + 1 + extra)
    for i in range(advances):
        rng_val = rng_array[(2 * i) + 2 + extra] & 255
        if rng_val >= 223:
            # Append battle number from current
            # (i.e. first or second battle), 1 == next battle.
            ret_array.append(i + 1)
        if home_check == 99:
            rng_val = rng_array[(2 * i) + 1 + extra] & 255
            if rng_val >= 223:
                # Append battle number from current
                # (i.e. first or second battle), 1 == next battle.
                home_check = i + 1

    ret_array.append(
        99
    )  # Just so we don't have an empty array. This will never be used otherwise.
    logger.manip(f"Upcoming ambushes: {ret_array}")
    logger.manip(f"Home check: {home_check}")
    if get_map() == 280:
        ret_array.append(home_check)
    return ret_array


def rikku_mix_damage() -> List[int]:
    initial_rng_vals = rng_array_from_index(index=26, array_len=9)
    dmg_rng = [(x & 31) + 0xF0 for x in initial_rng_vals[1:]]
    base_dmg = 18 * 50
    initial_damage = [(x * base_dmg) // 256 for x in dmg_rng]
    weakness_damage = [int(x * 1.5) for x in initial_damage]
    return weakness_damage


def future_attack_will_crit(
    character: int, char_luck: int, enemy_luck: int, 
    equipment_bonus: int = 0, attack_index: int = 1, 
    burn_rolls: int = 0, report: bool = False
) -> bool:
    # Returns if a specific attack in the future will crit.
    # Attack Index 1 represents the next attack.
    # Assumes no escape attempts, primarily this is used for Aeons anyway.
    if attack_index > 90:
        return False
    ptr = (attack_index*2) + burn_rolls
    rng_index = min(20 + character, 27)
    #rng_array = rng_array_from_index(index=rng_index, array_len=200)
    rng_val = rng_array_from_index(index=rng_index, array_len=ptr+1)[ptr] & 0x7FFFFFFF

    #crit_roll = (rng_array[attack_index * 2] & 0x7FFFFFFF) % 101
    crit_roll = rng_val % 101
    crit_chance = char_luck - enemy_luck + equipment_bonus
    if report:
        logger.warning(f"Crit check: {crit_roll} < {crit_chance} | RNG index {rng_index}")

    return crit_roll < crit_chance


def rng_01():
    global base_value
    return process.read(base_value + 0xD35EDC)


def rng_01_array(array_len: int = 600):
    ret_val = [rng_01()]  # First value is the current value
    for x in range(array_len):  # Subsequent values are based on first value.
        ret_val.append(roll_next_rng(ret_val[x], 1))
    return ret_val


def rng_01_advances(advance_count: int = 50):
    test_array = rng_01_array()
    range_val = advance_count
    for i in range(range_val):
        test_array.append(test_array[i] & 0x7FFFFFFF)
    return test_array


def next_chance_rng_01(version="white"):
    test_array = rng_01_array()
    even_array = []
    odd_array = []
    range_val = int((len(test_array) - 1) / 2) - 2
    if version == "white":
        modulo = 13
        battle_index = 8
    else:
        modulo = 10
        battle_index = 0
    for i in range(range_val):
        if (test_array[((i + 1) * 2) - 1] & 0x7FFFFFFF) % modulo == battle_index:
            odd_array.append(i)
        if (test_array[(i + 1) * 2] & 0x7FFFFFFF) % modulo == battle_index:
            even_array.append(i)

    # logger.debug(
    #     "Next event will appear on the odd array without manip. "
    #     + f"Area: {version}"
    # )
    # logger.debug(f"odd_array: {odd_array[0]}")
    # logger.debug(f"even_array: {even_array[0]}")
    return [odd_array, even_array]


def advance_rng_01():
    global base_value
    key = base_value + 0xD35EDC
    process.write(key, rng_01_array()[2])


def rng_02():
    global base_value
    return process.read(base_value + 0xD35EE0)


def rng_02_array(array_len: int = 200000):
    ret_val = [rng_02()]  # First value is the current value
    for x in range(array_len):  # Subsequent values are based on first value.
        ret_val.append(roll_next_rng(ret_val[x], 2))
    return ret_val


def set_test_rng_02():
    global base_value
    key = base_value + 0xD35EE0
    process.write(key, 3777588919)


def rng_10():
    global base_value
    return process.read(base_value + 0xD35F00)


def highbridge_drops():
    test_array = rng_10_array(array_len=40)
    ret_val = []
    for i in range(len(test_array)):
        if i < 3:
            pass
        elif (test_array[i] & 0x7FFFFFFF) % 255 < 30:
            ret_val.append(i - 3)
    logger.warning(ret_val)
    return ret_val

def rng_10_array(array_len: int = 256):
    ret_val = [rng_10()]  # First value is the current value
    for x in range(array_len):  # Subsequent values are based on first value.
        ret_val.append(roll_next_rng(last_rng=ret_val[x], index=10))
    return ret_val


def next_miss_rng_10(drop_chance_val: int = 60,min_steals = 0) -> int:
    test_array = rng_10_array()
    for i in range(len(test_array)):
        if i < 3+min_steals:
            pass
        elif (test_array[i] & 0x7FFFFFFF) % 255 >= drop_chance_val:
            return i - 3


def next_chance_rng_10(drop_chance_val: int = 60,min_steals = 0) -> int:
    test_array = rng_10_array()
    for i in range(len(test_array)):
        if i < 3+min_steals:
            pass
        elif (test_array[i] & 0x7FFFFFFF) % 255 < drop_chance_val:
            return i - 3


def next_chance_rng_10_full(drop_chance_val: int = 60) -> int:
    test_array = rng_10_array()
    results_array = [False, False, False]
    for i in range(len(test_array)):
        if i < 3:
            pass
        elif (test_array[i] & 0x7FFFFFFF) % 255 < drop_chance_val:
            results_array.append(True)
        else:
            results_array.append(False)
    return results_array


def next_chance_rng_10_calm() -> int:
    test_array = rng_10_array()
    for i in range(len(test_array)):
        if i < 3:
            pass
        elif (test_array[i] & 0x7FFFFFFF) % 255 >= 60 and (
            test_array[i + 3] & 0x7FFFFFFF
        ) % 255 < 60:
            return i - 3


def next_chance_rng_10_ronso() -> int:
    test_array = rng_10_array()
    for i in range(len(test_array)):
        if i < 3:
            pass
        elif (test_array[i] & 0x7FFFFFFF) % 255 < 60 and (
            test_array[i + 9] & 0x7FFFFFFF
        ) % 255 < 60:
            return i - 3


def next_chance_rng_10_ronso_calm() -> int:
    test_array = rng_10_array()
    for i in range(len(test_array)):
        if i < 3:
            pass
        elif (test_array[i] & 0x7FFFFFFF) % 255 >= 60 and (
            test_array[i + 9] & 0x7FFFFFFF
        ) % 255 < 60:
            return i - 3


def no_chance_x3_rng_10_highbridge() -> int:
    test_array = rng_10_array()
    for i in range(len(test_array)):
        if i < 3:
            pass
        elif (
            (test_array[i] & 0x7FFFFFFF) % 255 < 30
            and (test_array[i + 3] & 0x7FFFFFFF) % 255 < 30
            and (test_array[i] & 0x7FFFFFFF) % 255 < 30
        ):
            return i - 3


def advance_rng_10():
    global base_value
    key = base_value + 0xD35F00
    process.write(key, rng_10_array()[1])


def rng_12():
    global base_value
    return process.read(base_value + 0xD35F08)


def rng_12_array(advances: int = 255):
    ret_val = [rng_12()]  # First value is the current value
    for x in range(advances):  # Subsequent values are based on first value.
        ret_val.append(roll_next_rng(ret_val[x], 12))
    return ret_val


def next_chance_rng_12(before_natus: bool = False) -> int:
    ability_mod = 13

    next_chance = 256
    if before_natus:
        ptr = 5
    else:
        ptr = 1
    test_array = rng_12_array()
    while next_chance == 256:
        # Assume killer is aeon
        if ptr > 250:
            return 256
        elif (test_array[ptr + 1] & 0x7FFFFFFF) % 2 == 1:  # equipment
            # logger.debug(f"RNG12 ptr: {ptr}")
            base_mod = (ability_mod + ((test_array[ptr + 3] & 0x7FFFFFFF) & 7)) - 4
            abilities = (base_mod + ((base_mod >> 31) & 7)) >> 3

            if ptr == 1:
                if next_drop_rng_13(abilities, before_natus):
                    logger.debug("next_chance_rng_12(): Mark1")
                    next_chance = 0
                else:
                    logger.debug("next_chance_rng_12(): Mark2")
                    next_chance = 1
                if before_natus:
                    next_chance += 1
            else:
                next_chance = int((ptr - 1) / 4)
        else:
            ptr += 4
    if before_natus:
        next_chance -= 1
    return int(next_chance)


def advance_rng_12():
    global base_value
    key = base_value + 0xD35F08
    process.write(key, rng_12_array()[4])


def rng_13():
    global base_value
    return process.read(base_value + 0xD35F0C)


def rng_13_array(array_len: int = 20):
    ret_val = [rng_13()]  # First value is the current value
    for x in range(array_len):  # Subsequent values are based on first value.
        ret_val.append(roll_next_rng(ret_val[x], 13))
    return ret_val


def next_drop_rng_13(a_slots: int, before_natus: bool = False) -> int:
    outcomes = [4, 1, 1, 1, 2, 2, 3, 3]
    filled_slots = [9] * a_slots
    if before_natus:
        ptr = 2
    else:
        ptr = 1
    test_array = rng_13_array()
    while 9 in filled_slots and ptr < 20:
        try:
            if outcomes[(((test_array[ptr] & 0x7FFFFFFF) % 7) + 1)] in filled_slots:
                pass
            else:
                filled_slots.remove(9)
                filled_slots.append(
                    outcomes[(((test_array[ptr] & 0x7FFFFFFF) % 7) + 1)]
                )
        except Exception:
            pass
        ptr += 1

    # logger.debug(f"RNG13: {filled_slots}")

    if 1 in filled_slots:
        return True
    else:
        return False


def next_chance_rng_13() -> int:
    next_chance = 256
    outcomes = [4, 1, 1, 1, 2, 2, 3, 3]
    ptr = 1
    next_chance = 0
    test_array = rng_13_array()
    while next_chance == 0:
        # logger.debug("RNG13 outcome: "
        #              + f"{outcomes[(((test_array[ptr] & 0x7fffffff) % 7) + 1)]}")
        if outcomes[(((test_array[ptr] & 0x7FFFFFFF) % 7) + 1)] == 1:
            next_chance = ptr
        else:
            ptr += 1
    logger.debug(f"next_chance_rng_13: Value found. {ptr}")
    return int(next_chance)


def advance_rng_13():
    global base_value
    key = base_value + 0xD35F0C
    process.write(key, rng_13_array()[4])


def rng_23():
    global base_value
    return process.read(base_value + 0xD35F16)


def rng_23_array(array_len: int = 200):
    ret_val = [rng_23()]  # First value is the current value
    for x in range(array_len):  # Subsequent values are based on first value.
        ret_val.append(roll_next_rng(ret_val[x], 13))
    return ret_val


def advance_rng_23():
    global base_value
    key = base_value + 0xD35F16
    process.write(key, rng_23_array()[1])


def s32(integer: int) -> int:
    return ((integer & 0xFFFFFFFF) ^ 0x80000000) - 0x80000000


def roll_next_rng(last_rng: int, index: int) -> int:
    """Returns a generator object that yields rng values
    for a given rng index.
    """
    rng_value = s32(last_rng)
    rng_constant_1 = RNG_CONSTANTS_1[index]
    rng_constant_2 = RNG_CONSTANTS_2[index]

    new_value = s32(rng_value * rng_constant_1 ^ rng_constant_2)
    new_value = s32((new_value >> 0x10) + (new_value << 0x10))
    return new_value


def arena_array():
    global base_value
    ret_array = []
    for i in range(104):
        key = base_value + 0xD30C9C + i
        ret_array.append(process.read_bytes(key, 1))
    return ret_array


def arena_farm_check(
    zone: str = "besaid", end_goal: int = 10, report=False, return_array=False
):
    import nemesis.menu as menu

    complete = True
    zone = zone.lower()
    if zone == "besaid":
        zone_indexes = [8, 15, 27]
    if zone == "kilika":
        zone_indexes = [21, 30, 38, 61]
    if zone == "miihen":
        zone_indexes = [0, 9, 16, 22, 34, 47, 50, 62, 85]
    if zone == "mrr":
        zone_indexes = [5, 23, 40, 51, 63, 91]
    if zone == "djose":
        zone_indexes = [1, 10, 17, 28, 31, 79, 83]
    if zone == "tplains":
        zone_indexes = [6, 24, 35, 52, 64, 76, 89, 87]
    if zone == "maclake":
        zone_indexes = [3, 11, 18, 36]
    if zone == "macwoods":
        zone_indexes = [2, 25, 32, 65, 71, 94]
    if zone == "bikanel":
        zone_indexes = [12, 29, 41, 42, 53, 88]
    if zone == "calm":
        zone_indexes = [4, 13, 19, 33, 55, 57, 72, 73, 80]
    if zone == "gagazet":
        zone_indexes = [14, 20, 37, 39, 45, 46, 49, 58, 60, 69, 84, 86]
    if zone == "stolenfayth":
        zone_indexes = [7, 26, 44, 48, 54, 66, 68, 92, 98]
    if zone == "justtonberry":
        zone_indexes = [98]
    if zone == "sin1":
        zone_indexes = [37]
    if zone == "sin2":
        zone_indexes = [56, 70, 77, 78, 81, 93, 90, 97]
    if zone == "omega":
        zone_indexes = [67, 74, 75, 82, 95, 96, 99, 100, 101, 102, 103]

    test_array = arena_array()
    result_array = []

    for i in range(len(zone_indexes)):
        result_array.append(test_array[zone_indexes[i]])
        if test_array[zone_indexes[i]] < end_goal:
            complete = False
    if report:
        ap_needed = menu.next_ap_needed(game_vars.nem_checkpoint_ap())
        logger.debug(f"Next Sphere Grid checkpoint: {game_vars.nem_checkpoint_ap()}")
        logger.debug(f"Tidus S.levels: {get_tidus_slvl()} - need levels: {ap_needed}")
        logger.info(f"Zone Capture Progress - should reach {end_goal} total for all:")
        logger.info([min(value, end_goal) for value in result_array])
        #result_array = [min(value, end_goal) for value in result_array]
        #logger.info(result_array)
    if return_array:
        return result_array
    else:
        return complete


def arena_cursor():  # Not working properly
    global base_value

    key = base_value + 0x00D2A084
    status = process.read_bytes(key, 2)
    return status

def arena_cursor_1():  # left/right on area select screen
    global base_value

    ptr = process.read_bytes(base_value + 0xD2A084, 4)
    return process.read_bytes(ptr + 0x10, 2)

def arena_cursor_2():  # up/down on area select screen
    global base_value

    ptr = process.read_bytes(base_value + 0xD2A084, 4)
    return process.read_bytes(ptr + 0x12, 2)

def arena_cursor_3():  # up/down on monster select screen
    global base_value

    ptr = process.read_bytes(base_value + 0xD2A084, 4)
    val = process.read_bytes(ptr + 0x12, 2)
    return (val - 93)/38


# Escape logic, and used for others


def rng_from_index(index: int = 20):
    mem_target = 0xD35ED8 + (index * 0x4)
    global base_value
    return process.read(base_value + mem_target)


def get_next_rng2():
    return roll_next_rng(rng_from_index(2), 2) & 0x7FFFFFFF & 0xFFFF


def rng_array_from_index(index: int = 20, array_len: int = 20):
    ret_val = [rng_from_index(index)]  # First value is the current value
    for x in range(array_len):  # Subsequent values are based on first value.
        ret_val.append(roll_next_rng(ret_val[x], index))
    # logger.debug(ret_val)
    ret_val = [
        x & 0x7FFFFFFF for x in ret_val
    ]  # Anding it because that's the value that's actually used
    # logger.warning(ret_val)
    # wait_frames(90)
    return ret_val


def advance_rng_index(index: int = 43):
    global base_value
    key = 0xD35ED8 + (index * 0x4)
    process.write(base_value + key, rng_array_from_index(index=index)[1])


def next_steal(steal_count: int = 0, pre_advance: int = 0):
    use_array = rng_array_from_index(index=10, array_len=1 + pre_advance)
    steal_rng = use_array[1 + pre_advance] % 255
    steal_chance = 2**steal_count
    steal_threshold = 255 // steal_chance
    ret_val = steal_rng < steal_threshold
    logger.debug(
        f"next_steal(): === {use_array[1]} === {steal_rng} < "
        + f"{steal_threshold} = {ret_val}"
    )
    return ret_val


def next_steal_rare(pre_advance: int = 0):
    indeces = 1 + pre_advance
    use_array = rng_array_from_index(index=11, array_len=indeces)
    # logger.debug(use_array)
    # for i in range(len(use_array)):
    #    logger.warning(f"{i} - {use_array[i] & 255}")
    steal_crit_rng = use_array[indeces] & 255
    logger.warning(f" RNG&255: {steal_crit_rng} | Returning {steal_crit_rng < 32}")
    return steal_crit_rng < 32

def disable_battle_music():
    global base_value
    address = base_value + 0xF26B09
    original_value = process.read_bytes(address, size=1)
    modified_value = original_value | 0b00000101
    process.write_bytes(address, modified_value, size=1)

def read_bytes_external(key, length, use_base:bool=True):
    global base_value
    if use_base:
        key += base_value
    return process.read_bytes(key, length)