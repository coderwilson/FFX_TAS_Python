import ctypes
import ctypes.wintypes
import os.path
import struct
import time
from collections import Counter
from math import cos, sin

from ReadWriteMemory import Process, ReadWriteMemory

import logs
import targetPathing
import vars
import xbox

game_vars = vars.vars_handle()
FFXC = xbox.controller_handle()

# Process Permissions
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020

MAX_PATH = 260

baseValue = 0


class LocProcess(Process):
    def __init__(self, *args, **kwargs):
        super(LocProcess, self).__init__(*args, **kwargs)

    def readBytes(self, lp_base_address: int, size: int = 4):
        """
        See the original ReadWriteMemory values for details on how this works. This version allows us to pass
        the number of bytes to be retrieved instead of a static 4-byte size. Default is 4 for reverse-compatibility
        """
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

    def writeBytes(self, lp_base_address: int, value: int, size: int = 4) -> bool:
        """
        Same as above, write a passed number of bytes instead of static 4 bytes. Default is 4 for reverse-compatibility
        """
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
            ReadWriteMemoryError(error)


class FFXMemory(ReadWriteMemory):
    def __init__(self, *args, **kwargs):
        super(FFXMemory, self).__init__(*args, **kwargs)
        self.process = LocProcess()

    def get_process_by_name(self, process_name: str | bytes) -> "Process":
        """
        :description: Get the process by the process executabe\'s name and return a Process object.

        :param process_name: The name of the executable file for the specified process for example, my_program.exe.

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
    global xPtr
    global yPtr
    global coordsCounter
    coordsCounter = 0
    success = False

    # rwm = ReadWriteMemory()
    rwm = FFXMemory()
    print("#############")
    print(type(rwm))
    process = rwm.get_process_by_name("FFX.exe")
    print("#############")
    print(type(process))
    print("#############")
    process.open()

    global baseValue
    try:
        import zz_rootMem

        print("Process Modules:")
        baseValue = zz_rootMem.list_process_modules(process.pid)
        print("Process Modules complete")
        print("Dynamically determined memory address:", hex(baseValue))
        success = True
    except Exception as errCode:
        print("Could not get memory address dynamically. ", errCode)
        baseValue = 0x00FF0000
        time.sleep(10)
    return success


def float_from_integer(integer):
    return struct.unpack("!f", struct.pack("!I", integer))[0]


def wait_frames(frames: int):
    frames = max(round(frames), 1)
    global baseValue
    key = baseValue + 0x0088FDD8
    current = process.readBytes(key, 4)
    final = current + frames
    previous = current - 1
    while current < final:
        if not (current == previous or current == previous + 1):
            final = final - previous
        previous = current
        current = process.readBytes(key, 4)
    return


def rng_seed():
    if int(game_vars.confirmed_seed()) == 999:
        global baseValue
        key = baseValue + 0x003988A5
        return process.readBytes(key, 1)
    return int(game_vars.confirmed_seed())


def set_rng_seed(value):
    global baseValue
    key = baseValue + 0x003988A5
    print("+++++++++++++++++")
    print(type(process))
    print("+++++++++++++++++")
    return process.writeBytes(key, value, 1)


def game_over():
    global baseValue
    key = baseValue + 0x00D2C9F1
    if process.readBytes(key, 1) == 1:
        return True
    else:
        return False


def battle_complete():
    global baseValue
    key = baseValue + 0x00D2C9F1
    if process.readBytes(key, 1) == 2:
        return True
    elif process.readBytes(key, 1) == 3:
        return True
    else:
        return False


def battle_arena_results():
    global baseValue
    if process.readBytes(baseValue + 0x00D2C9F1, 1) == 2:
        return True
    return False


def game_over_reset():
    global baseValue
    key = baseValue + 0x00D2C9F1
    process.writeBytes(key, 0, 1)


def battle_active():
    global baseValue
    key = baseValue + 0x00D2C9F1
    return process.readBytes(key, 1) == 0


def get_current_turn():
    global baseValue
    key = baseValue + 0x00D2AA00
    return process.readBytes(key, 1)


def get_next_turn():
    global baseValue
    key = baseValue + 0x00D2AA04
    return process.readBytes(key, 1)


def battle_menu_cursor():
    global baseValue
    if not turn_ready():
        return 255
    key2 = baseValue + 0x00F3C926
    return process.readBytes(key2, 1)


def battle_screen():
    if main_battle_menu():
        global baseValue
        if battle_menu_cursor() == 255:
            return False
        else:
            wait_frames(10)
            return True
    else:
        return False


def turn_ready():
    global baseValue
    key = baseValue + 0x00F3F77B
    if process.readBytes(key, 1) == 0:
        return False
    else:
        while not main_battle_menu():
            pass
        wait_frames(1)
        if game_vars.use_pause():
            wait_frames(2)
        return True


def battle_cursor_2():
    global baseValue
    key = baseValue + 0x00F3CA01
    if process.readBytes(key, 1) != 0:
        key = baseValue + 0x00F3CA0E
        return process.readBytes(key, 1)
    else:
        return 255


def battle_cursor_3():
    global baseValue
    key = baseValue + 0x00F3CAFE
    return process.readBytes(key, 1)


def overdrive_menu_active():
    global baseValue
    key = baseValue + 0x00F3D6F4
    return process.readBytes(key, 1) == 4


def overdrive_menu_active_wakka():
    global baseValue
    key = baseValue + 0x00DA0BD0
    return process.readBytes(key, 1)


def auron_overdrive_active():
    global baseValue
    key = baseValue + 0x00F3D6B4
    return process.readBytes(key, 1) == 4


def main_battle_menu():
    global baseValue
    key = baseValue + 0x00F3C911
    if process.readBytes(key, 1) > 0:
        return True
    else:
        return False


def other_battle_menu():
    global baseValue
    key = baseValue + 0x00F3CA01
    if process.readBytes(key, 1) > 0:
        return True
    else:
        return False


def interior_battle_menu():
    global baseValue
    key = baseValue + 0x00F3CAF1
    return process.readBytes(key, 1)


def super_interior_battle_menu():
    global baseValue
    key = baseValue + 0x00F3CBE1
    return process.readBytes(key, 1)


def battle_target_id():
    global baseValue
    key = baseValue + 0x00F3D1B4
    retVal = process.readBytes(key, 1)
    print("Battle Target ID:", retVal)
    return retVal


def battle_line_target():
    return read_val(0x00F3CA42)


def enemy_targetted():
    return read_val(0x00F3D1C0)


def battle_target_active():
    global baseValue
    key = baseValue + 0x00F3D1B4
    retVal = process.readBytes(key, 1)
    print("Battle Target ID:", retVal)
    return retVal != 255


def user_control():
    global baseValue
    # Auto updating via reference to the baseValue above
    controlStruct = baseValue + 0x00F00740
    inControl = process.read(controlStruct)

    if inControl == 0:
        return False
    else:
        return True


def await_control():
    waitCounter = 0
    print("Awaiting control (no clicking)")
    while not user_control():
        waitCounter += 1
        if waitCounter % 10000000 == 0:
            print("Awaiting control -", waitCounter / 100000)
    wait_frames(1)
    return True


def click_to_control_dumb():
    waitCounter = 0
    print("Awaiting control (clicking)")
    while not user_control():
        xbox.tap_b()
        waitCounter += 1
        if waitCounter % 1000 == 0:
            print("Awaiting control -", waitCounter / 1000)
    print("Control restored.")
    return True

def click_to_control_smart():
    waitCounter = 0
    print("Awaiting control (clicking only when appropriate - dialog)")
    wait_frames(6)
    while not user_control():
        if battle_active():
            while battle_active():
                xbox.tap_b()
        if diag_skip_possible():
            xbox.tap_b()
        elif menu_open():
            print("Post-battle menu open")
            xbox.tap_b()
        else:
            pass
        waitCounter += 1
        if waitCounter % 10000 == 0:
            print("Awaiting control -", waitCounter / 10000)
    print("User control restored.")
    return True

def click_to_control():
    return click_to_control_smart()
def click_to_control_2():
    return click_to_control_smart()
def click_to_control_3():
    return click_to_control_smart()


def click_to_control_special():
    waitCounter = 0
    print("Awaiting control (clicking)")
    while not user_control():
        FFXC.set_value("BtnB", 1)
        FFXC.set_value("BtnY", 1)
        wait_frames(30 * 0.035)
        FFXC.set_value("BtnB", 0)
        FFXC.set_value("BtnY", 0)
        wait_frames(30 * 0.035)
        waitCounter += 1
        if waitCounter % 10000 == 0:
            print("Awaiting control -", waitCounter / 10000)
    wait_frames(30 * 0.05)
    return True


def click_to_event():
    while user_control():
        FFXC.set_value("BtnB", 1)
        if game_vars.use_pause():
            wait_frames(2)
        else:
            wait_frames(1)
        FFXC.set_value("BtnB", 0)
        if game_vars.use_pause():
            wait_frames(3)
        else:
            wait_frames(1)
    wait_frames(6)


def click_to_event_temple(direction):
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
    wait_frames(30 * 0.2)
    while not user_control():
        click_to_control_3()
        wait_frames(30 * 0.035)


def await_event():
    wait_frames(1)
    while user_control():
        pass


def get_coords():
    global process
    global baseValue
    global xPtr
    global yPtr
    global coordsCounter
    coordsCounter += 1
    xPtr = baseValue + 0x0084DED0
    yPtr = baseValue + 0x0084DED8
    coord1 = process.get_pointer(xPtr)
    x = float_from_integer(process.read(coord1))
    coord2 = process.get_pointer(yPtr)
    y = float_from_integer(process.read(coord2))

    return [x, y]


def ammes_fix(actor_index: int = 0):
    global process
    global baseValue
    basePtr = baseValue + 0x1FC44E4
    baseAddr = process.read(basePtr)
    # xCoord = 749, yCoord = -71
    process.write(baseAddr + (0x880 * actor_index) + 0x0C, 0x443B4000)
    process.write(baseAddr + (0x880 * actor_index) + 0x14, 0xC28E0000)


def choco_eater_fun(actor_index: int = 0):
    global process
    global baseValue
    basePtr = baseValue + 0x1FC44E4
    baseAddr = process.read(basePtr)
    process.write(baseAddr + (0x880 * actor_index) + 0x14, 0xC4BB8000)


def extractor_height():
    global process
    global baseValue
    height = get_actor_coords(3)[2]
    print("^^Extractor Height:", height)
    return height


def get_height():
    global process
    global baseValue
    global zPtr

    zPtr = baseValue + 0x0084DED0
    coord1 = process.get_pointer(zPtr)
    return float_from_integer(process.read(coord1))


def get_movement_vectors():
    global process
    global baseValue
    addr = baseValue + 0x00F00754
    ptr = process.get_pointer(addr)
    angle = float_from_integer(process.read(ptr))
    forward = [cos(angle), sin(angle)]
    right = [sin(angle), -cos(angle)]
    return (forward, right)


def get_camera():
    global baseValue
    angle = baseValue + 0x008A86B8
    x = baseValue + 0x008A86F8
    y = baseValue + 0x008A8700
    z = baseValue + 0x008A86FC
    angle2 = baseValue + 0x008A86C0

    key = process.get_pointer(angle)
    angleVal = round(float_from_integer(process.read(key)), 2)
    key = process.get_pointer(x)
    xVal = round(float_from_integer(process.read(key)), 2)
    key = process.get_pointer(y)
    yVal = round(float_from_integer(process.read(key)), 2)
    key = process.get_pointer(z)
    zVal = round(float_from_integer(process.read(key)), 2)
    key = process.get_pointer(angle2)
    angleVal2 = round(float_from_integer(process.read(key)), 2)

    retVal = [angleVal, xVal, yVal, zVal, angleVal2]
    return retVal


def get_hp():
    global baseValue
    # Out of combat HP only

    coord = baseValue + 0x00D32078
    HP_Tidus = process.read(coord)

    coord = baseValue + 0x00D3210C
    HP_Yuna = process.read(coord)

    coord = baseValue + 0x00D321A0
    HP_Auron = process.read(coord)

    coord = baseValue + 0x00D32234
    HP_Kimahri = process.read(coord)

    coord = baseValue + 0x00D322C8
    HP_Wakka = process.read(coord)

    coord = baseValue + 0x00D3235C
    HP_Lulu = process.read(coord)

    coord = baseValue + 0x00D323F0
    HP_Rikku = process.read(coord)

    return [HP_Tidus, HP_Yuna, HP_Auron, HP_Kimahri, HP_Wakka, HP_Lulu, HP_Rikku]


def get_max_hp():
    global baseValue
    # Out of combat HP only

    coord = baseValue + 0x00D32080
    HP_Tidus = process.read(coord)

    coord = baseValue + 0x00D32114
    HP_Yuna = process.read(coord)

    coord = baseValue + 0x00D321A8
    HP_Auron = process.read(coord)

    coord = baseValue + 0x00D3223C
    HP_Kimahri = process.read(coord)

    coord = baseValue + 0x00D322D0
    HP_Wakka = process.read(coord)

    coord = baseValue + 0x00D32364
    HP_Lulu = process.read(coord)

    coord = baseValue + 0x00D323F8
    HP_Rikku = process.read(coord)

    return [HP_Tidus, HP_Yuna, HP_Auron, HP_Kimahri, HP_Wakka, HP_Lulu, HP_Rikku]


def get_tidus_mp():
    global baseValue
    retVal = process.read(baseValue + 0xD3207C)
    return retVal


def get_yuna_mp():
    global baseValue
    retVal = process.read(baseValue + 0xD32110)
    return retVal


def get_order():
    global baseValue
    # Out of combat HP only

    coord = baseValue + 0x00D307E8
    pos1 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307E9
    pos2 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EA
    pos3 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EB
    pos4 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EC
    pos5 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307ED
    pos6 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EE
    pos7 = process.readBytes(coord, 1)

    formation = [255, pos1, pos2, pos3, pos4, pos5, pos6, pos7]
    print("Party formation:", formation)
    return formation


def get_order_six():
    global baseValue
    # Out of combat HP only

    coord = baseValue + 0x00D307E8
    pos1 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307E9
    pos2 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EA
    pos3 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EB
    pos4 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EC
    pos5 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307ED
    pos6 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EE
    pos7 = process.readBytes(coord, 1)

    formation = [pos1, pos2, pos3, pos4, pos5, pos6, pos7]
    print(formation)
    while 255 in formation:
        formation.remove(255)
    return formation


def get_order_seven():
    global baseValue
    # Out of combat HP only

    coord = baseValue + 0x00D307E8
    pos1 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307E9
    pos2 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EA
    pos3 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EB
    pos4 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EC
    pos5 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307ED
    pos6 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EE
    pos7 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307EF
    pos8 = process.readBytes(coord, 1)
    coord = baseValue + 0x00D307F0
    pos9 = process.readBytes(coord, 1)

    formation = [pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9]
    while 255 in formation:
        formation.remove(255)
    return formation


def get_char_formation_slot(char_num):
    allSlots = get_order_seven()
    x = 0
    while x < len(allSlots):
        if allSlots[x] == char_num:
            return x
        else:
            x += 1
    return 255  # Character is not in the party


def get_phoenix():
    global baseValue

    key = get_item_slot(6)
    pDowns = get_item_count_slot(key)
    print("Phoenix Down count:", pDowns)
    return pDowns


def get_power():
    global baseValue

    key = get_item_slot(70)
    power = get_item_count_slot(key)
    print("Power spheres:", power)
    return power


def set_power(qty):
    global baseValue

    slot = get_item_slot(70)
    key = baseValue + item_count_addr(slot)
    process.writeBytes(key, qty, 1)
    power = get_power()
    return power


def get_speed():
    global baseValue

    key = get_item_slot(72)
    speed = get_item_count_slot(key)
    print("Speed spheres:", speed)
    return speed


def set_speed(qty):
    global baseValue

    slot = get_item_slot(72)
    key = baseValue + item_count_addr(slot)
    process.writeBytes(key, qty, 1)
    speed = get_speed()
    return speed


def get_battle_hp():
    global baseValue

    key = baseValue + 0x00F3F7A4
    hp1 = process.read(key)
    key = baseValue + 0x00F3F834
    hp2 = process.read(key)
    key = baseValue + 0x00F3F8C4
    hp3 = process.read(key)
    hpArray = [hp1, hp2, hp3]
    return hpArray


def get_encounter_id():
    global baseValue

    key = baseValue + 0x00D2A8EC
    formation = process.read(key)

    return formation


def clear_encounter_id():
    global baseValue

    key = baseValue + 0x00D2A8EC
    process.write(key, 0)


def get_active_battle_formation():
    global baseValue

    key = baseValue + 0x00F3F76C
    char1 = process.readBytes(key, 1)
    key = baseValue + 0x00F3F76E
    char2 = process.readBytes(key, 1)
    key = baseValue + 0x00F3F770
    char3 = process.readBytes(key, 1)

    battleForm = [char1, char2, char3]
    return battleForm


def get_battle_formation():
    global baseValue

    key = baseValue + 0x00F3F76C
    char1 = process.readBytes(key, 1)
    key = baseValue + 0x00F3F76E
    char2 = process.readBytes(key, 1)
    key = baseValue + 0x00F3F770
    char3 = process.readBytes(key, 1)
    key = baseValue + 0x00D2C8A3
    char4 = process.readBytes(key, 1)
    key = baseValue + 0x00D2C8A4
    char5 = process.readBytes(key, 1)
    key = baseValue + 0x00D2C8A5
    char6 = process.readBytes(key, 1)
    key = baseValue + 0x00D2C8A6
    char7 = process.readBytes(key, 1)
    key = baseValue + 0x00D2C8A7
    char8 = process.readBytes(key, 1)
    key = baseValue + 0x00D2C8A8
    char9 = process.readBytes(key, 1)
    key = baseValue + 0x00D2C8A9
    char10 = process.readBytes(key, 1)

    battleForm = [char4, char5, char6, char7, char8, char9, char10]
    print(battleForm)
    if 255 in battleForm:
        while 255 in battleForm:
            battleForm.remove(255)
    battleForm.insert(0, char3)
    battleForm.insert(0, char2)
    battleForm.insert(0, char1)
    print(battleForm)
    return battleForm


def get_battle_char_slot(char_num) -> int:
    battleForm = get_battle_formation()
    if char_num not in battleForm:
        return 255
    try:
        if battleForm[0] == char_num:
            return 0
        if battleForm[1] == char_num:
            return 1
        if battleForm[2] == char_num:
            return 2
        if battleForm[3] == char_num:
            return 3
        if battleForm[4] == char_num:
            return 4
        if battleForm[5] == char_num:
            return 5
        if battleForm[6] == char_num:
            return 6
    except Exception:
        return 255


def get_battle_char_turn():
    global baseValue

    key = baseValue + 0x00D36A68
    battleCharacter = process.read(key)
    return battleCharacter


def get_slvl_yuna():
    global baseValue
    # Out of combat HP only

    coord = baseValue + 0x00D32104
    return process.read(coord)


def get_slvl_kim():
    global baseValue
    # Out of combat HP only

    coord = baseValue + 0x00D3222C
    return process.read(coord)


def get_slvl_wakka():
    global baseValue
    # Out of combat HP only

    key = baseValue + 0x00D322E7
    sLvl = process.readBytes(key, 1)
    print("Wakka current Slvl", sLvl)
    return sLvl


def item_address(num):
    global baseValue
    return baseValue + 0x00D3095C + (num * 0x2)


def get_items_order():
    items = []
    for x in range(100):
        items.append(process.readBytes(item_address(x), 1))
    return items


def get_use_items_order():
    itemArray = get_items_order()
    x = 0
    while x < len(itemArray):
        try:
            if itemArray[x] == 20:
                ignoreThisValue = True
                x += 1
            elif itemArray[x] < 23:
                del itemArray[x]
            elif itemArray[x] > 69:
                del itemArray[x]
            else:
                x += 1
        except Exception as y:
            print(y)
            retryThisValue = True
            print("Retrying value")
    return itemArray


def get_use_items_slot(item_num):
    items = get_use_items_order()
    x = 0
    for x in range(len(items)):
        print(items[x], "|", item_num, "|", x)
        if items[x] == item_num:
            return x
        x += 1
    return 255


def get_throw_items_order():
    itemArray = get_items_order()
    print(itemArray)
    x = 0
    while x < len(itemArray):
        try:
            if itemArray[x] > 18:
                itemArray.remove(itemArray[x])
            else:
                x += 1
        except Exception as y:
            print(y)
            retryThisValue = True
            print("Retrying value")
    print(itemArray)
    return itemArray


def get_throw_items_slot(itemNum):
    items = get_throw_items_order()
    x = 0
    while x < len(items):
        if items[x] == itemNum:
            print("Desired item", itemNum, "is in slot", x)
            return x
        x += 1
    return 255


def get_grid_items_order():
    itemArray = get_items_order()
    x = 0
    while x < len(itemArray):
        try:
            if itemArray[x] < 70 or itemArray[x] > 99:
                itemArray.remove(itemArray[x])
            else:
                x += 1
        except Exception as y:
            print(y)
            retryThisValue = True
            print("Retrying value")
    return itemArray


def get_grid_items_slot(item_num) -> int:
    items = get_grid_items_order()
    x = 0
    while x < len(items):
        if items[x] == item_num:
            print("Desired item", item_num, "is in slot", x)
            return x
        x += 1
    return 255


def get_grid_cursor_pos():
    global baseValue
    key = baseValue + 0x012ACB78
    return process.readBytes(key, 1)


def get_grid_move_use_pos():
    global baseValue
    key = baseValue + 0x012AC838
    return process.readBytes(key, 1)


def get_grid_move_active():
    global baseValue
    key = baseValue + 0x012AC82B
    if process.readBytes(key, 1):
        return True
    else:
        return False


def get_grid_use_active():
    global baseValue
    key = baseValue + 0x012ACB6B
    if process.readBytes(key, 1):
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
    bombCore = 0
    lMarble = 0
    fScale = 0
    aWind = 0
    grenade = 0
    lunar = 0
    light = 0

    bombCore = get_item_slot(27)
    lMarble = get_item_slot(30)
    fScale = get_item_slot(32)
    aWind = get_item_slot(24)
    grenade = get_item_slot(35)
    lunar = get_item_slot(56)
    light = get_item_slot(57)

    # Set MaxSpot to one more than the last undesirable item
    if light - lunar != 1:
        maxSpot = light
    elif lunar - grenade != 1:
        maxSpot = lunar
    elif grenade - aWind != 1:
        maxSpot = grenade
    elif aWind - fScale != 1:
        maxSpot = aWind
    elif fScale - lMarble != 1:
        maxSpot = fScale
    elif lMarble - bombCore != 1:
        maxSpot = lMarble
    else:
        maxSpot = bombCore

    retVal = [bombCore, lMarble, fScale, aWind, grenade, lunar, light, maxSpot]
    print("Returning values:", retVal)
    return retVal


def item_count_addr(num):
    return 0x00D30B5C + num


def get_items_count():
    global baseValue
    itemCounts = []
    for x in range(60):
        itemCounts.append(process.readBytes(baseValue + 0x00D30B5C + x, 1))
    return itemCounts


def get_item_count_slot(item_slot) -> int:
    global baseValue
    return process.readBytes(baseValue + 0x00D30B5C + item_slot, 1)


def get_menu_display_characters():
    base = 0x01441BD4
    characters = []
    for cur in range(7):
        char = read_val(base + cur)
        print(cur, char)
        characters.append(char)
    print(characters)
    return characters


def get_gil_value():
    global baseValue
    key = baseValue + 0x00D307D8
    return process.read(key)


def set_gil_value(new_value):
    global baseValue
    key = baseValue + 0x00D307D8
    return process.write(key, new_value)


def set_story(new_value):
    global baseValue
    key = baseValue + 0x00D2D67C
    return process.writeBytes(key, new_value, 2)


def rikku_od_cursor_1():
    global baseValue
    key = baseValue + 0x00F3CB32
    return process.readBytes(key, 1)


def rikku_od_cursor_2():
    return rikku_od_cursor_1()


def get_overdrive_battle(character):
    global process
    global baseValue

    basePointer = baseValue + 0x00D334CC
    basePointerAddress = process.read(basePointer)
    offset = (0xF90 * character) + 0x5BC
    retVal = process.readBytes(basePointerAddress + offset, 1)
    print("In-Battle Overdrive values:\n", retVal)
    return retVal


def get_char_weakness(character):
    global process
    global baseValue

    basePointer = baseValue + 0x00D334CC
    basePointerAddress = process.read(basePointer)
    offset = (0xF90 * character) + 0x5DD
    retVal = process.readBytes(basePointerAddress + offset, 1)
    print("In-Battle Overdrive values:\n", retVal)
    return retVal


def tidus_escaped_state():
    global baseValue

    basePointer = baseValue + 0x00D334CC
    basePointerAddress = process.read(basePointer)
    offset = 0xDC8
    retVal = not process.readBytes(basePointerAddress + offset, 1)
    print("Tidus Escaped State:", retVal)
    return retVal


def state_dead(character):
    global process
    global baseValue
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    offset = (0xF90 * character) + 0x606

    key = basePointerAddress + offset
    retVal = process.readBytes(key, 1)

    if retVal % 2 == 1:
        return True
    else:
        return False


def state_berserk(character):
    global process
    global baseValue
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    offset = (0xF90 * character) + 0x607

    key = basePointerAddress + offset
    retVal = process.readBytes(key, 1)

    if retVal % 4 >= 2:
        return True
    else:
        return False


def state_petrified(character):
    if character not in get_active_battle_formation():
        return False

    global process
    global baseValue
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    offset = (0xF90 * character) + 0x606

    key = basePointerAddress + offset
    retVal = process.readBytes(key, 1)

    if retVal % 8 >= 4:
        return True
    else:
        return False


def state_confused(character):
    global process
    global baseValue
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    offset = (0xF90 * character) + 0x607

    key = basePointerAddress + offset
    retVal = process.readBytes(key, 1)

    if retVal % 2 == 1:
        print("Character %d is confused" % character)
        return True
    else:
        print("Character %d is not confused" % character)
        return False


def state_sleep(character):
    global process
    global baseValue
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    offset = (0xF90 * character) + 0x608

    key = basePointerAddress + offset
    retVal = process.readBytes(key, 1)

    if retVal == 3:
        print("Character %d is asleep" % character)
        return True
    else:
        print("Character %d is not asleep" % character)
        return False


def state_auto_life(character: int = 0):
    global process
    global baseValue
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    offset = (0xF90 * character) + 0x617

    key = basePointerAddress + offset
    retVal = process.readBytes(key, 1)

    if retVal % 4 >= 2:
        print("Character autolife is active", character)
        return True
    else:
        print("Character autolife is not active", character)
        return False


def state_confused_by_pos(position):
    posArray = get_battle_formation()
    x = 0
    if position in posArray:
        if posArray[x] == position:
            return state_confused(posArray[x])
        else:
            x += 1


def battle_type():
    # 0 is normal, 1 is pre-empt, 2 is ambushed
    return read_val(0x00D2C9DC)


def get_enemy_current_hp():
    global process
    global baseValue
    enemyNum = 20
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)

    while enemyNum < 27:
        offset1 = (0xF90 * enemyNum) + 0x594
        key1 = basePointerAddress + offset1
        offset2 = (0xF90 * enemyNum) + 0x5D0
        key2 = basePointerAddress + offset2
        if enemyNum == 20:
            maxHP = [process.readBytes(key1, 4)]
            current_hp = [process.readBytes(key2, 4)]
        else:
            nextHP = process.readBytes(key1, 4)
            if nextHP != 0:
                maxHP.append(nextHP)
                current_hp.append(process.readBytes(key2, 4))
        enemyNum += 1
    print("Enemy HP current values:", current_hp)
    return current_hp


def get_enemy_max_hp():
    global process
    global baseValue
    enemyNum = 20
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)

    while enemyNum < 25:
        offset1 = (0xF90 * enemyNum) + 0x594
        key1 = basePointerAddress + offset1
        offset2 = (0xF90 * enemyNum) + 0x5D0
        key2 = basePointerAddress + offset2
        if enemyNum == 20:
            maxHP = [process.readBytes(key1, 4)]
            current_hp = [process.readBytes(key2, 4)]
        else:
            if maxHP != 0:
                maxHP.append(process.readBytes(key1, 4))
                current_hp.append(process.readBytes(key2, 4))
        enemyNum += 1
    print("Enemy HP max values:")
    print(maxHP)
    print("Enemy HP current values:")
    print(current_hp)
    return maxHP


def menu_open():
    global baseValue

    key = baseValue + 0x00F407E4
    menuOpen = process.readBytes(key, 1)
    if menuOpen == 0:
        return False
    else:
        return True


def close_menu():
    while menu_open():
        xbox.tap_a()


def save_menu_open():
    global baseValue

    key = baseValue + 0x008E7300
    menuOpen = process.readBytes(key, 1)
    if menuOpen == 1:
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
    menuCounter = 0
    while not (user_control() and menu_open() and menu_number() == 5):
        if menu_open() and not user_control():
            print("Post-Battle summary screen is open. Attempting close.", menuCounter)
            xbox.menu_b()
        elif user_control() and not menu_open():
            print("Menu is not open, attempting to open.", menuCounter)
            xbox.tap_y()
            menuCounter += 1
        elif menu_open() and user_control() and menu_number() > 5:
            print("The wrong menu is open.", menuCounter)
            xbox.tap_a()
            menuCounter += 1
        elif battle_active():
            print("Can't open menu during battle.", menuCounter)
            return False
        else:
            pass
    FFXC.set_neutral()
    print("Menu open returning")
    return True


def menu_number():
    global baseValue
    return process.readBytes(baseValue + 0x85B2CC, 1)


def s_grid_active():
    global baseValue

    key = baseValue + 0x0085B30C
    menuOpen = process.readBytes(key, 1)
    if menuOpen == 1:
        return True
    else:
        return False


def s_grid_menu():
    global baseValue

    key = baseValue + 0x0012AD860
    menuOpen = process.readBytes(key, 1)
    return menuOpen


def s_grid_char():
    global baseValue

    key = baseValue + 0x0012BEE2C
    character = process.readBytes(key, 1)
    return character


def s_grid_node_selected():
    global baseValue

    key = baseValue + 0x0012BEB7E
    nodeNumber = process.readBytes(key, 1)
    key = baseValue + 0x0012BEB7F
    nodeRegion = process.readBytes(key, 1)
    return [nodeNumber, nodeRegion]


def cursor_location():
    global baseValue

    key = baseValue + 0x0021D09A4
    menu1 = process.readBytes(key, 1)
    key = baseValue + 0x0021D09A6
    menu2 = process.readBytes(key, 1)

    return [menu1, menu2]


def get_menu_cursor_pos():
    global baseValue

    key = baseValue + 0x01471508
    pos = process.readBytes(key, 1)

    return pos


def get_menu_2_char_num():
    global baseValue

    key = baseValue + 0x0147150C
    pos = process.readBytes(key, 1)

    return pos


def get_char_cursor_pos():
    global baseValue

    key = baseValue + 0x01441BE8
    pos = process.readBytes(key, 1)

    return pos


def get_story_progress():
    global baseValue

    key = baseValue + 0x00D2D67C
    progress = process.readBytes(key, 2)
    return progress


def get_map():
    global baseValue

    key = baseValue + 0x00D2CA90
    progress = process.readBytes(key, 2)
    return progress


def touching_save_sphere():
    global baseValue

    key = baseValue + 0x0021D09A6
    value = process.readBytes(key, 1)
    if value != 0:
        return True
    else:
        return False


def save_menu_cursor():
    global baseValue

    key = baseValue + 0x001467942
    return process.readBytes(key, 1)


def map_cursor():
    global baseValue
    basePointer = baseValue + 0x00F2FF14
    basePointerAddress = process.read(basePointer)
    print(basePointerAddress)
    ret = process.readBytes(basePointerAddress + 272, 1)
    print(ret)
    return ret


def clear_save_menu_cursor():
    global baseValue

    key = baseValue + 0x001467942
    return process.writeBytes(key, 0, 1)


def clear_save_menu_cursor_2():
    global baseValue

    key = baseValue + 0x001468302
    return process.writeBytes(key, 0, 1)


def save_menu_cursor_2():
    global baseValue

    key = baseValue + 0x001468302
    return process.readBytes(key, 1)


def new_game_cursor():
    global baseValue

    key = baseValue + 0x001467942
    value = process.readBytes(key, 1)
    return value


def targeting_ally():
    return read_val(0x00F3D1C0) == 0


def targeting_enemy():
    return not targeting_ally()


def get_yuna_slvl():
    global baseValue

    key = baseValue + 0x00D3212B
    sLvl = process.readBytes(key, 1)
    return sLvl


def get_tidus_slvl():
    global baseValue

    key = baseValue + 0x00D32097
    sLvl = process.readBytes(key, 1)
    return sLvl


def get_kimahri_slvl():
    global baseValue

    key = baseValue + 0x00D32253
    sLvl = process.readBytes(key, 1)
    return sLvl


def get_lulu_slvl():
    return read_val(0x00D3237B)


def get_tidus_xp():
    global baseValue

    key = baseValue + 0x00D32070
    Lvl = process.read(key)
    return Lvl


def set_tidus_slvl(levels):
    global baseValue

    key = baseValue + 0x00D32097
    sLvl = process.writeBytes(key, levels, 1)
    return sLvl


def menu_control():
    global baseValue

    key = baseValue + 0x0085A03C
    control = process.readBytes(key, 1)
    if control == 1:
        return True
    else:
        return False


def diag_skip_possible_old():
    global baseValue

    key = baseValue + 0x0085A03C
    control = process.readBytes(key, 1)
    if control == 1:
        wait_frames(1)
        return True
    else:
        return False


def diag_skip_possible(ignore_audio = False):
    if not ignore_audio and auditory_dialog_playing():
        return False
    global baseValue

    if auditory_dialog_playing() and not game_vars.accessibilityVars()[1]:
        return True
    else:
        key = baseValue + 0x0085A03C
        return process.readBytes(key, 1) == 1


def cutscene_skip_possible():
    return False
    global baseValue

    key = baseValue + 0x00D2A008
    return process.readBytes(key, 1) == 1


def auditory_dialog_playing():
    global baseValue
    key = baseValue + 0x00F2FED4
    return process.readBytes(key, 1) == 1

def auditory_dialog_playing():
    #This is usually a no-op unless doNotSkipCutscenes is set.
    if game_vars.doNotSkipCutscenes:
        return false
    global baseValue

    key = baseValue + 0x00F30038
    control = process.readBytes(key, 1)
    return control == 1


def special_text_open():
    global baseValue

    key = baseValue + 0x01466D30
    control = process.readBytes(key, 1)
    if control == 1:
        return True
    else:
        key = baseValue + 0x01476988
        control = process.readBytes(key, 1)
        if control == 1:
            return True
        else:
            return False


def await_menu_control():
    counter = 0
    while not menu_control():
        counter += 1
        if counter % 100000 == 0:
            print("Waiting for menu control.", counter)


def click_to_story_progress(destination):
    counter = 0
    currentState = get_story_progress()
    print("Story goal:", destination, "| Awaiting progress state:", currentState)
    while currentState < destination:
        if menu_control():
            FFXC.set_value("BtnB", 1)
            FFXC.set_value("BtnA", 1)
            wait_frames(1)
            FFXC.set_value("BtnB", 0)
            FFXC.set_value("BtnA", 0)
            wait_frames(1)
        if counter % 100000 == 0:
            print(
                "Story goal:",
                destination,
                "| Awaiting progress state:",
                currentState,
                "| counter:",
                counter / 100000,
            )
        counter += 1
        currentState = get_story_progress()
    print("Story progress has reached destination. Value:", destination)


def desert_format(rikku_charge):
    order = get_order_six()
    if order == [0, 3, 2, 4, 6, 5]:
        print("Formation is fine, moving on.")
    elif not rikku_charge:
        full_party_format("desert1")
    else:
        full_party_format("desert2")


def party_size():
    battleForm = get_battle_formation()
    if 255 in battleForm:
        while 255 in battleForm:
            battleForm.remove(255)
    return len(battleForm)


def active_party_size():
    battleForm = get_active_battle_formation()
    if 255 in battleForm:
        while 255 in battleForm:
            battleForm.remove(255)
    return len(battleForm)


def get_character_index_in_main_menu(character):
    res = get_menu_display_characters().index(character)
    print("Char is in position", res)
    return res


def full_party_format(front_line, *, full_menu_close=True):
    order = get_order_seven()
    partyMembers = len(order)
    front_line = front_line.lower()
    orderFinal = get_party_format_from_text(front_line)
    orderFinal.extend(x for x in order if x not in orderFinal)
    if Counter(order[:3]) == Counter(orderFinal[:3]):
        print("Good to go, no action taken.")
    else:
        print("Converting from formation:")
        print(order)
        print("Into formation:")
        print(orderFinal)
        print("Manipulating final formation to minimize movements")
        replacement_dict = {}
        new_characters = [x for x in orderFinal[:3] if x not in order[:3]]
        for i in range(3):
            if order[i] in orderFinal[:3]:
                replacement_dict[i] = order[i]
            else:
                replacement_dict[i] = new_characters.pop()
        for i in range(3):
            orderFinal[i] = replacement_dict[i]
        print("New Final Order:")
        print(orderFinal)
        while not menu_open():
            if not open_menu():
                return
        FFXC.set_neutral()
        while get_menu_cursor_pos() != 7:
            menu_direction(get_menu_cursor_pos(), 7, 11)
            if game_vars.use_pause():
                wait_frames(1)
        while menu_number() != 14:
            xbox.tap_b()
        startPos = 0
        while Counter(order[:3]) != Counter(orderFinal[:3]):
            print("==Full Party Format function, original")
            # Select target in the wrong spot.
            print("Selecting start position")
            if order[startPos] == orderFinal[startPos]:
                while order[startPos] == orderFinal[startPos] and order != orderFinal:
                    startPos += 1
                    if startPos == partyMembers:
                        startPos = 0
            print(
                "Character",
                name_from_number(orderFinal[startPos]),
                "should be in position",
                startPos,
            )

            # Set target, end position
            print("Selecting destination position.")
            endPos = 0
            if orderFinal[startPos] != order[endPos]:
                while orderFinal[startPos] != order[endPos] and order != orderFinal:
                    endPos += 1

            print(
                "Character",
                name_from_number(order[endPos]),
                "found in position",
                endPos,
            )

            print("Looking for character.")
            if startPos < 3 and endPos < 3:
                startPos += 1
                if startPos == partyMembers:
                    startPos = 0
                continue

            # Move cursor to start position
            print("Moving to start position")
            if party_format_cursor_1() != startPos:
                # print("Cursor not in right spot")
                while party_format_cursor_1() != startPos:
                    menu_direction(party_format_cursor_1(), startPos, partyMembers)
                    if game_vars.use_pause():
                        wait_frames(1)

            while menu_number() != 20:
                xbox.menu_b()  # Click on Start location

            # Move cursor to end position
            print("Moving to destination position.")
            while party_format_cursor_2() != endPos:
                menu_direction(party_format_cursor_2(), endPos, partyMembers)
                if game_vars.use_pause():
                    wait_frames(1)
            while menu_number() != 14:
                xbox.menu_b()  # Click on End location, performs swap.
            print("Start and destination positions have been swapped.")
            startPos += 1
            if startPos == partyMembers:
                startPos = 0

            print("Reporting results")
            print("Converting from formation:")
            print(order)
            print("Into formation:")
            print(orderFinal)
            order = get_order_seven()
        print("Party format is good now.")
        if full_menu_close:
            close_menu()
        else:
            back_to_main_menu()


def menu_direction(current_menu_position, target_menu_position, menu_size):
    distance = abs(current_menu_position - target_menu_position)
    distanceUnsigned = current_menu_position - target_menu_position
    halfmenusize = menu_size / 2
    if distance == halfmenusize:
        xbox.tap_up()
    elif distance < halfmenusize:
        if distanceUnsigned > 0:
            xbox.tap_up()
        else:
            xbox.tap_down()
    else:
        if distanceUnsigned > 0:
            xbox.tap_down()
        else:
            xbox.tap_up()


def side_to_side_direction(current_menu_position, target_menu_position, menu_size):
    distance = abs(current_menu_position - target_menu_position)
    distanceUnsigned = current_menu_position - target_menu_position
    print("Menu Size:", menu_size)
    halfmenusize = menu_size / 2
    if distance == halfmenusize:
        print("Marker 1")
        xbox.tap_left()
    elif distance < halfmenusize:
        if distanceUnsigned > 0:
            print("Marker 2")
            xbox.tap_right()
        else:
            print("Marker 3")
            xbox.tap_left()
    else:
        if distanceUnsigned > 0:
            print("Marker 4")
            xbox.tap_left()
        else:
            print("Marker 5")
            xbox.tap_right()


def party_format_cursor_1():
    global baseValue

    coord = baseValue + 0x0147151C
    retVal = process.readBytes(coord, 1)
    return retVal


def party_format_cursor_2():
    global baseValue

    coord = baseValue + 0x01471520
    retVal = process.readBytes(coord, 1)
    return retVal


def get_party_format_from_text(front_line):
    print("||| FRONT LINE VARIABLE:", front_line)
    if front_line == "kimahri":
        orderFinal = [0, 3, 2, 6, 4, 5, 1]
    elif front_line == "rikku":
        orderFinal = [0, 6, 2, 3, 4, 5, 1]
    elif front_line == "yuna":
        orderFinal = [0, 1, 2, 6, 4, 5, 3]
    elif front_line == "kilikawoods1":
        orderFinal = [0, 1, 4, 3, 5, 2]
    elif front_line == "kilikawoodsbackup":
        orderFinal = [3, 1, 4, 0, 5]
    elif front_line == "gauntlet":
        orderFinal = [0, 1, 3, 2, 4, 5, 6]
    elif front_line == "miihen":
        orderFinal = [0, 4, 2, 3, 5, 1]
    elif front_line == "macalaniaescape":
        orderFinal = [0, 1, 6, 2, 4, 3, 5]
    elif front_line == "desert1":
        orderFinal = [0, 6, 2, 3, 4, 5]
    elif front_line == "desert2":
        orderFinal = [0, 3, 2, 6, 4, 5]
    elif front_line == "desert3":
        orderFinal = [0, 5, 2, 6, 4, 3]
    elif front_line == "desert9":
        orderFinal = [0, 4, 2, 3, 5]
    elif front_line == "guards":
        orderFinal = [0, 2, 3, 6, 4, 5]
    elif front_line == "evrae":
        orderFinal = [0, 6, 3, 2, 4, 5]
    elif front_line == "djose":
        orderFinal = [0, 4, 2, 3, 1, 5]
    elif front_line == "spheri":
        orderFinal = [0, 3, 1, 4, 2, 6, 5]
    elif front_line == "crawler":
        orderFinal = [0, 3, 5, 4, 2, 6, 1]
    elif front_line == "besaid1":
        orderFinal = [0, 1, 5, 3, 4]
    elif front_line == "besaid2":
        orderFinal = [0, 4, 5, 3, 5]
    elif front_line == "kilika":
        orderFinal = [0, 1, 4, 3, 5]
    elif front_line == "mrr1":
        orderFinal = [0, 4, 2, 3, 5, 1]
    elif front_line == "mrr2":
        orderFinal = [1, 4, 3, 5, 2, 0]
    elif front_line == "battlesite":
        orderFinal = [0, 1, 4, 5, 2, 3]
    elif front_line == "postbunyip":
        orderFinal = [0, 4, 2, 6, 1, 3, 5]
    elif front_line == "mwoodsneedcharge":
        orderFinal = [0, 6, 2, 4, 1, 3, 5]
    elif front_line == "mwoodsgotcharge":
        orderFinal = [0, 4, 2, 6, 1, 3, 5]
    elif front_line == "mwoodsdone":
        orderFinal = [0, 3, 2, 4, 1, 6, 5]
    elif front_line == "besaid":
        orderFinal = [5, 1, 0, 4]
    elif front_line == "highbridge":
        orderFinal = [0, 1, 2, 6, 4, 5]
    elif front_line == "guards_no_lulu":
        orderFinal = [0, 3, 6]
    elif front_line == "guards_lulu":
        orderFinal = [0, 5, 6]
    elif front_line == "tidkimwak":
        orderFinal = [0, 4, 3, 6, 1, 2, 5]
    elif front_line == "nemlulu":
        orderFinal = [0, 1, 5, 2, 3, 4, 6]
    elif front_line == "initiative":
        orderFinal = [0, 4, 6, 1, 2, 3, 5]
    else:
        orderFinal = [6, 5, 4, 3, 2, 1, 0]
    return orderFinal


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


def get_actor_array_size():
    global baseValue
    return process.read(baseValue + 0x01FC44E0)


def get_actor_id(actor_num):
    actor_index = actor_num
    global baseValue
    basePointer = baseValue + 0x01FC44E4
    basePointerAddress = process.read(basePointer)
    offsetX = 0x880 * actor_index
    return process.readBytes(basePointerAddress + offsetX, 2)


def get_actor_coords(actor_number):
    global process
    global baseValue
    retVal = [0, 0, 0]
    try:
        basePointer = baseValue + 0x01FC44E4
        basePointerAddress = process.read(basePointer)
        offsetX = (0x880 * actor_number) + 0x0C
        offsetY = (0x880 * actor_number) + 0x14
        offsetZ = (0x880 * actor_number) + 0x10

        keyX = basePointerAddress + offsetX
        retVal[0] = float_from_integer(process.read(keyX))
        keyY = basePointerAddress + offsetY
        retVal[1] = float_from_integer(process.read(keyY))
        keyZ = basePointerAddress + offsetZ
        retVal[2] = float_from_integer(process.read(keyZ))

        return retVal
    except Exception:
        pass


def get_actor_angle(actor_number):
    global process
    global baseValue
    try:
        basePointer = baseValue + 0x01FC44E4
        basePointerAddress = process.read(basePointer)
        offset = (0x880 * actor_number) + 0x158
        retVal = float_from_integer(process.read(basePointerAddress + offset))
        return retVal
    except Exception:
        pass


def miihen_guy_coords():
    spearGuy = 255
    for x in range(get_actor_array_size()):
        actorNum = get_actor_id(x)
        if actorNum == 0x202D:
            spearGuy = x
    return get_actor_coords(spearGuy)


def actor_index(actor_num: int = 41):
    actorIndex = 255
    for x in range(get_actor_array_size()):
        actorMem = get_actor_id(x)
        if actor_num == actorMem:
            actorIndex = x
    return actorIndex


def mrr_guy_coords():
    print("+++Searching for MRR guy")
    mrrGuy = 255
    for x in range(get_actor_array_size()):
        actorNum = get_actor_id(x)
        # print("Actor", x, ":", hex(actorNum))
        if actorNum == 0x2083:
            mrrGuy = x
    print("+++MRR guy in position:", mrrGuy)
    mrrGuyPos = get_actor_coords(mrrGuy)
    return [mrrGuyPos[0], mrrGuyPos[1]]


def lucille_miihen_coords():
    return get_actor_coords(8)


def lucille_djose_coords():
    return get_actor_coords(11)


def lucille_djose_angle():
    global process
    global baseValue
    retVal = [0, 0]

    basePointer = baseValue + 0x01FC44E4
    basePointerAddress = process.read(basePointer)
    offsetX = 0x91D8
    offsetY = 0x91E8

    keyX = basePointerAddress + offsetX
    retVal[0] = float_from_integer(process.read(keyX))
    keyY = basePointerAddress + offsetY
    retVal[1] = float_from_integer(process.read(keyY))

    return retVal


def affection_array():
    global process
    global baseValue

    tidus = 255
    key = baseValue + 0x00D2CAC0
    yuna = process.readBytes(key, 1)
    key = baseValue + 0x00D2CAC4
    auron = process.readBytes(key, 1)
    key = baseValue + 0x00D2CAC8
    kimahri = process.readBytes(key, 1)
    key = baseValue + 0x00D2CACC
    wakka = process.readBytes(key, 1)
    key = baseValue + 0x00D2CAD0
    lulu = process.readBytes(key, 1)
    key = baseValue + 0x00D2CAD4
    rikku = process.readBytes(key, 1)

    return [tidus, yuna, auron, kimahri, wakka, lulu, rikku]


def overdrive_state():
    global process
    global baseValue
    retVal = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    x = 0

    basePointer = baseValue + 0x00386DD4
    basePointerAddress = process.read(basePointer)
    for x in range(20):
        offset = (0x94 * x) + 0x39
        retVal[x] = process.readBytes(basePointerAddress + offset, 1)
    print("Overdrive values:\n", retVal)
    return retVal


def overdrive_state_2():
    global process
    global baseValue
    retVal = [0, 0, 0, 0, 0, 0, 0]
    x = 0
    basePointer = baseValue + 0x003AB9B0
    basePointerAddress = process.read(basePointer)
    for x in range(7):
        offset = (0x94 * x) + 0x39
        retVal[x] = process.readBytes(basePointerAddress + offset, 1)
    print("Overdrive values:\n", retVal)
    return retVal


def char_luck(character: int = 0):
    global process
    global baseValue
    basePointer = baseValue + 0x003AB9B0
    basePointerAddress = process.read(basePointer)
    offset = (0x94 * character) + 0x34
    retVal = process.readBytes(basePointerAddress + offset, 1)
    return retVal


def char_accuracy(character: int = 0):
    global process
    global baseValue
    basePointer = baseValue + 0x003AB9B0
    basePointerAddress = process.read(basePointer)
    offset = (0x94 * character) + 0x36
    retVal = process.readBytes(basePointerAddress + offset, 1)
    return retVal


def dodge_lightning(l_dodge_num):
    global baseValue

    if l_strike_count() != l_dodge_num or (l_strike_count() == 1 and l_dodge_num == 0):
        wait_frames(3)
        xbox.tap_b()
        wait_frames(5)
        return True
    else:
        return False


def l_strike_count():
    global baseValue

    key = baseValue + 0x00D2CE8C
    return process.readBytes(key, 2)


def l_dodge_count():
    global baseValue

    key = baseValue + 0x00D2CE8E
    return process.readBytes(key, 2)


def save_popup_cursor():
    global baseValue

    key = baseValue + 0x0146780A
    return process.readBytes(key, 1)


def diag_progress_flag():
    global baseValue

    key = baseValue + 0x00F25A80
    return process.readBytes(key, 4)


def click_to_diag_progress(num):
    print("Clicking to dialog progress:", num)
    lastNum = diag_progress_flag()
    while diag_progress_flag() != num:
        if user_control():
            return False
        else:
            if not auditory_dialog_playing():
                xbox.tap_b()
            if diag_progress_flag() != lastNum:
                lastNum = diag_progress_flag()
                print("Dialog change:", diag_progress_flag(), "- clicking to", num)
    return True


def set_encounter_rate(set_val):
    global baseValue

    key = baseValue + 0x008421C8
    process.writeBytes(key, set_val, 1)


def set_game_speed(set_val):
    global baseValue

    key = baseValue + 0x008E82A4
    process.writeBytes(key, set_val, 1)


def print_rng_36():
    global baseValue

    coord = baseValue + 0x00D35F68
    retVal = process.readBytes(coord, 1)
    print("------------------------------")
    print("RNG36 value:", retVal)
    print("------------------------------")


def end():
    global process
    process.close()
    print("Memory reading process is now closed.")


def get_frame_count():
    global baseValue
    key = baseValue + 0x0088FDD8
    return process.readBytes(key, 4)


def name_aeon_ready():
    global baseValue
    key = baseValue + 0x01440A30
    return process.readBytes(key, 1)


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
    global baseValue
    egg_num += 23
    basePointer = baseValue + 0x1FC44E4
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + (0x880 * egg_num) + 0x0C
    retVal = float_from_integer(process.read(key))
    return retVal


def egg_y(egg_num):
    global process
    global baseValue
    egg_num += 23
    basePointer = baseValue + 0x1FC44E4
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + (0x880 * egg_num) + 0x14
    retVal = float_from_integer(process.read(key))
    return retVal


def get_egg_distance(egg_num):
    global process
    global baseValue
    basePointer = baseValue + 0xF270B8
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + 0x1C4CC + (0x40 * egg_num)
    retVal = float_from_integer(process.read(key))
    return retVal


def get_egg_life(egg_num):
    global process
    global baseValue
    basePointer = baseValue + 0xF270B8
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + 0x1C4CC + (0x40 * egg_num) + 4
    retVal = process.readBytes(key, 1)
    return retVal


def get_egg_picked(egg_num):
    global process
    global baseValue
    basePointer = baseValue + 0xF270B8
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + 0x1C4CC + (0x40 * egg_num) + 5
    retVal = process.readBytes(key, 1)
    return retVal


class Egg:
    def __init__(self, egg_num):
        self.num = egg_num
        self.x = egg_x(self.num)
        self.y = egg_y(self.num)
        self.distance = get_egg_distance(self.num)
        self.eggLife = get_egg_life(egg_num)
        self.eggPicked = get_egg_picked(egg_num)

        if self.distance != 0 and self.eggPicked == 0:
            self.isActive = True
        else:
            self.isActive = False

        if self.eggPicked == 1:
            self.goForEgg = False
        elif self.eggLife > 100 and self.distance > 100:
            self.goForEgg = False
        elif self.distance > 250:
            self.goForEgg = False
        elif self.distance == 0:
            self.goForEgg = False
        else:
            self.goForEgg = True

    def report_vars(self):
        varArray = [
            self.num,
            self.isActive,
            self.x,
            self.y,
            150 - self.eggLife,
            self.eggPicked,
            self.distance,
        ]
        print("Egg_num, Is_Active, X, Y, Egg Life, Picked up, distance")
        print(varArray)


def build_eggs():
    retArray = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for x in range(10):
        retArray[x] = Egg(x)
    return retArray


def ice_x(actor):
    global process
    global baseValue
    # Icicle 0 is actor 7 in the array, incremented for each additional icicle.
    offset = actor + 7

    basePointer = baseValue + 0x1FC44E4
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + (0x880 * offset) + 0x0C
    retVal = float_from_integer(process.read(key))
    return retVal


def ice_y(actor):
    global process
    global baseValue
    # Icicle 0 is actor 7 in the array, incremented for each additional icicle.
    offset = actor + 7

    basePointer = baseValue + 0x1FC44E4
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + (0x880 * offset) + 0x14
    retVal = float_from_integer(process.read(key))
    return retVal


def get_ice_distance(ice_num):
    global process
    global baseValue
    basePointer = baseValue + 0xF270B8
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + 0x1C0CC + (0x40 * ice_num)
    retVal = float_from_integer(process.read(key))
    return retVal


def get_ice_life(ice_num):
    global process
    global baseValue
    basePointer = baseValue + 0xF270B8
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + 0x1C0CC + (0x40 * ice_num) + 4
    retVal = process.readBytes(key, 1)
    return retVal


class Icicle:
    def __init__(self, ice_num):
        self.num = ice_num
        self.x = ice_x(self.num)
        self.y = ice_y(self.num)
        self.isActive = True

    def report_vars(self):
        varArray = [self.num, self.x, self.y]
        print("Ice_num, X, Y")
        print(varArray)


def build_icicles():
    retArray = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for x in range(16):
        retArray[x] = Icicle(x)
    return retArray


# ------------------------------
# Soft reset section


def set_map_reset():
    global baseValue

    key = baseValue + 0x00D2CA90
    process.writeBytes(key, 23, 2)


def force_map_load():
    global baseValue

    key = baseValue + 0x00F3080C
    process.writeBytes(key, 1, 1)


def reset_battle_end():
    global baseValue
    key = baseValue + 0x00D2C9F1
    process.writeBytes(key, 1, 1)


def set_rng_2():
    global baseValue
    global process
    key = baseValue + 0x00D35EE0
    process.writeBytes(key, 0x7E9F20D2, 4)


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
    global baseValue
    ptrKey = process.read(baseValue + 0x00F2FF14)
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
        if process.readBytes(ptrKey + offset, 1) == 255:
            return False
        else:
            return True
    else:
        return False


def blitz_hp(player_index=99):
    global baseValue
    if player_index == 99:
        return 9999
    else:
        ptrKey = process.read(baseValue + 0x00F2FF14)
        offset = 0x1C8 + (0x4 * player_index)
        hpValue = process.read(ptrKey + offset)
        return hpValue


def blitz_own_score():
    global baseValue
    key = baseValue + 0x00D2E0CE
    score = process.readBytes(key, 1)
    return score


def blitz_opp_score():
    global baseValue
    key = baseValue + 0x00D2E0CF
    score = process.readBytes(key, 1)
    return score


def blitzball_patriots_style():
    global baseValue

    key = baseValue + 0x00D2E0CE


def blitz_clock_menu():
    global baseValue
    key = baseValue + 0x014765FA
    status = process.readBytes(key, 1)
    return status


def blitz_clock_pause():
    global baseValue
    key = baseValue + 0x014663B0
    status = process.readBytes(key, 1)
    return status


def blitz_menu_num():
    global baseValue
    # 20 = Movement menu (auto, type A, or type B)
    # 29 = Formation menu
    # 38 = Breakthrough
    # 24 = Pass To menu (other variations are set to 24)
    # Unsure about other variations, would take more testing.

    key = baseValue + 0x014765DA
    status = process.readBytes(key, 1)
    if status == 17 or status == 27:
        status = 24
    return status


def reset_blitz_menu_num():
    global baseValue
    key = baseValue + 0x014765DA
    process.writeBytes(key, 1, 1)


def blitz_current_player():
    global baseValue

    key = baseValue + 0x00F25B6A
    player = process.readBytes(key, 1)
    return player


def blitz_target_player():
    global baseValue

    key = baseValue + 0x00D3761C
    player = process.readBytes(key, 1)
    return player


def blitz_coords():
    global baseValue

    key = baseValue + 0x00D37698
    xVal = process.readBytes(key, 1)
    xVal = xVal * -1
    key = baseValue + 0x00D37690
    yVal = process.readBytes(key, 1)
    return [xVal, yVal]


def blitz_game_active():
    if get_map() == 62:
        return True
    else:
        return False


def blitz_clock():
    global baseValue

    basePointer = baseValue + 0x00F2FF14
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + 0x24C
    clockValue = process.read(key)
    return clockValue


def blitz_char_select_cursor():
    global baseValue

    key = baseValue + 0x0146780A
    cursor = process.readBytes(key, 1)
    return cursor


def blitz_proceed_cursor():
    global baseValue

    key = baseValue + 0x01467CEA
    cursor = process.readBytes(key, 1)
    return cursor


def blitz_cursor():
    global baseValue

    key = baseValue + 0x014676D2
    cursor = process.readBytes(key, 1)
    return cursor


# ------------------------------
# Function for logging


def read_bytes(key, size):
    return process.readBytes(key, size)


# ------------------------------
# Equipment array

# 0x0 - ushort - name/group (?)
# 0x3 - byte - wpn./arm. state
# 0x4 - byte - owner char (basis for field below)
# 0x5 - byte - equip type idx. (0 = cur. chara wpn., 1 = cur. chara arm., 2 = next chara wpn., etc.)
# 0x6 - byte - equip icon shown? (purely visual- a character will still keep it equipped if his stat struct says so)
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
    global baseValue

    basePointer = baseValue + 0x00D30F2C
    key = basePointer + (0x16 * equip_num) + 0x05
    retVal = process.readBytes(key, 1)
    return retVal


def get_equip_legit(equip_num):
    global baseValue

    basePointer = baseValue + 0x00D30F2C
    key = basePointer + (0x16 * equip_num) + 0x03
    retVal = process.readBytes(key, 1)
    if retVal in [0, 8, 9]:
        return True
    else:
        return False


def is_equip_brotherhood(equip_num):
    if get_equip_owner(equip_num) == 0:
        global baseValue
        basePointer = baseValue + 0x00D30F2C
        key = basePointer + (0x16 * equip_num) + 0x03
        retVal = process.readBytes(key, 1)
        if retVal == 9:
            return True
    return False


def get_equip_owner(equip_num):
    global baseValue

    basePointer = baseValue + 0x00D30F2C
    key = basePointer + (0x16 * equip_num) + 0x04
    retVal = process.readBytes(key, 1)
    return retVal


def get_equip_slot_count(equip_num):
    global baseValue

    basePointer = baseValue + 0x00D30F2C
    key = basePointer + (0x16 * equip_num) + 0x0B
    retVal = process.readBytes(key, 1)
    return retVal


def get_equip_currently_equipped(equip_num):
    global baseValue

    basePointer = baseValue + 0x00D30F2C
    key = basePointer + (0x16 * equip_num) + 0x06
    retVal = process.readBytes(key, 1)
    return retVal


def get_equip_abilities(equip_num):
    global baseValue
    retVal = [255, 255, 255, 255]

    basePointer = baseValue + 0x00D30F2C
    key = basePointer + (0x16 * equip_num) + 0x0E
    retVal[0] = process.readBytes(key, 2)
    key = basePointer + (0x16 * equip_num) + 0x10
    retVal[1] = process.readBytes(key, 2)
    key = basePointer + (0x16 * equip_num) + 0x12
    retVal[2] = process.readBytes(key, 2)
    key = basePointer + (0x16 * equip_num) + 0x14
    retVal[3] = process.readBytes(key, 2)
    return retVal


def get_equip_exists(equip_num):
    global baseValue

    basePointer = baseValue + 0x00D30F2C
    key = basePointer + (0x16 * equip_num) + 0x02
    retVal = process.readBytes(key, 1)

    return retVal


class Equipment:
    def __init__(self, equip_num):
        self.num = equip_num
        self.equipType = get_equip_type(equip_num)
        self.equipOwner = get_equip_owner(equip_num)
        self.equipOwnerAlt = get_equip_owner(equip_num)
        self.equipAbilities = get_equip_abilities(equip_num)
        self.equipStatus = get_equip_currently_equipped(equip_num)
        self.slots = get_equip_slot_count(equip_num)
        self.exists = get_equip_exists(equip_num)
        self.brotherhood = is_equip_brotherhood(equip_num)

    def create_custom(
        self, eType: int, eOwner1: int, eOwner2: int, eSlots: int, eAbilities
    ):
        self.equipType = eType
        self.equipOwner = eOwner1
        self.equipOwnerAlt = eOwner2
        self.equipAbilities = eAbilities
        self.equipStatus = 0
        self.slots = eSlots
        self.exists = 1
        self.brotherhood = False

    def equipment_type(self):
        return self.equipType

    def owner(self):
        return self.equipOwner

    def abilities(self):
        return self.equipAbilities

    def has_ability(self, ability_num):
        if ability_num in self.equipAbilities:
            return True
        return False

    def is_equipped(self):
        return self.equipStatus

    def slot_count(self):
        return self.slots

    def equip_exists(self):
        return self.exists

    def is_brotherhood(self):
        return self.brotherhood


def all_equipment():
    firstEquipment = True
    for i in range(200):
        currentHandle = Equipment(i)
        if get_equip_legit(i) and currentHandle.equip_exists():
            if firstEquipment:
                equipHandleArray = [Equipment(i)]
                firstEquipment = False
            else:
                equipHandleArray.append(Equipment(i))
    return equipHandleArray


def weapon_array_character(char_num):
    equipHandles = all_equipment()
    firstEquipment = True
    while len(equipHandles) > 0:
        currentHandle = equipHandles.pop(0)
        if currentHandle.owner() == char_num and currentHandle.equipment_type() == 0:
            if firstEquipment:
                charWeaps = [currentHandle]
                firstEquipment = False
            else:
                charWeaps.append(currentHandle)
    return charWeaps


def equipped_weapon_has_ability(char_num: int = 1, ability_num: int = 32769):
    equipHandles = weapon_array_character(char_num)
    while len(equipHandles) > 0:
        currentHandle = equipHandles.pop(0)
        if currentHandle.is_equipped() == char_num:
            print("## Owner:", currentHandle.owner())
            print("## Equipped:", currentHandle.is_equipped())
            print("## Has Ability:", currentHandle.has_ability(ability_num))
            if currentHandle.has_ability(ability_num):
                return True
            else:
                return False


def check_thunder_strike() -> int:
    results = 0
    tidusWeaps = weapon_array_character(0)
    while len(tidusWeaps) > 0:
        currentHandle = tidusWeaps.pop(0)
        if currentHandle.has_ability(0x8026):
            results += 1
            break

    wakkaWeaps = weapon_array_character(4)
    while len(wakkaWeaps) > 0:
        currentHandle = wakkaWeaps.pop(0)
        if currentHandle.has_ability(0x8026):
            results += 2
            break
    return results


def check_zombie_strike():
    ability = 0x8032

    charWeaps = weapon_array_character(0)  # Tidus
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            game_vars.set_zombie(0)
            return True

    charWeaps = weapon_array_character(1)  # Yuna
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            game_vars.set_zombie(1)
            return True

    charWeaps = weapon_array_character(2)  # Auron
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            game_vars.set_zombie(2)
            return True

    charWeaps = weapon_array_character(3)  # Kimahri
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            game_vars.set_zombie(3)
            return True

    charWeaps = weapon_array_character(4)  # Wakka
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            game_vars.set_zombie(4)
            return True

    charWeaps = weapon_array_character(5)  # Lulu
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            game_vars.set_zombie(5)
            return True

    charWeaps = weapon_array_character(6)  # Rikku
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            game_vars.set_zombie(6)
            return True

    return False


def check_ability(ability=0x8032):
    results = [False, False, False, False, False, False, False]

    charWeaps = weapon_array_character(0)  # Tidus
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            results[0] = True

    charWeaps = weapon_array_character(1)  # Yuna
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            results[1] = True

    charWeaps = weapon_array_character(2)  # Auron
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            results[2] = True

    charWeaps = weapon_array_character(3)  # Kimahri
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            results[3] = True

    charWeaps = weapon_array_character(4)  # Wakka
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            results[4] = True

    charWeaps = weapon_array_character(5)  # Lulu
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            results[5] = True

    charWeaps = weapon_array_character(6)  # Rikku
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            results[6] = True

    return results


def check_ability_armor(ability=0x8032, slot_count: int = 99):
    results = [False, False, False, False, False, False, False]

    charWeaps = armor_array_character(0)  # Tidus
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            if slot_count != 99:
                if currentHandle.slot_count() != slot_count:
                    results[0] = False
                else:
                    results[0] = True
            else:
                results[0] = True

    charWeaps = armor_array_character(1)  # Yuna
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            if slot_count != 99:
                if currentHandle.slot_count() != slot_count:
                    results[1] = False
                else:
                    results[1] = True
            else:
                results[1] = True

    charWeaps = armor_array_character(2)  # Auron
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            if slot_count != 99:
                if currentHandle.slot_count() != slot_count:
                    results[2] = False
                else:
                    results[2] = True
            else:
                results[2] = True

    charWeaps = armor_array_character(3)  # Kimahri
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            if slot_count != 99:
                if currentHandle.slot_count() != slot_count:
                    results[3] = False
                else:
                    results[3] = True
            else:
                results[3] = True

    charWeaps = armor_array_character(4)  # Wakka
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            if slot_count != 99:
                if currentHandle.slot_count() != slot_count:
                    results[4] = False
                else:
                    results[4] = True
            else:
                results[4] = True

    charWeaps = armor_array_character(5)  # Lulu
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            if slot_count != 99:
                if currentHandle.slot_count() != slot_count:
                    results[5] = False
                else:
                    results[5] = True
            else:
                results[5] = True

    charWeaps = armor_array_character(6)  # Rikku
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        print(currentHandle.abilities())
        if currentHandle.has_ability(ability):
            if slot_count != 99:
                if currentHandle.slot_count() != slot_count:
                    results[6] = False
                else:
                    results[6] = True
            else:
                results[6] = True
        print(results[6])

    return results


def weapon_armor_cursor():
    global baseValue
    return process.readBytes(baseValue + 0x0146A5E4, 1)


def customize_menu_array():
    retArray = []
    global baseValue
    for x in range(60):
        offset = 0x1197730 + (x * 4)
        retArray.append(process.readBytes(baseValue + offset, 2))
    print("Customize menu: ")
    print(retArray)
    return retArray


def check_nea_armor():
    ability = 0x801D

    charWeaps = armor_array_character(0)  # Tidus
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            game_vars.set_ne_armor(0)
            return True

    charWeaps = armor_array_character(1)  # Yuna
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            game_vars.set_ne_armor(1)
            return True

    charWeaps = armor_array_character(2)  # Auron
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            game_vars.set_ne_armor(2)
            return True

    charWeaps = armor_array_character(3)  # Kimahri
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            game_vars.set_ne_armor(3)
            return True

    charWeaps = armor_array_character(4)  # Wakka
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            game_vars.set_ne_armor(4)
            return True

    charWeaps = armor_array_character(5)  # Lulu
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            game_vars.set_ne_armor(5)
            return True

    charWeaps = armor_array_character(6)  # Rikku
    while len(charWeaps) > 0:
        currentHandle = charWeaps.pop(0)
        if currentHandle.has_ability(ability):
            game_vars.set_ne_armor(6)
            return True

    return False


def shop_menu_dialogue_row():
    return read_val(0x0146780A)


def airship_shop_dialogue_row():
    return read_val(0x014676D2)


def hunter_spear():
    kimWeapHandles = weapon_array_character(3)
    if len(kimWeapHandles) == 1:
        return False
    else:
        while len(kimWeapHandles) > 0:
            currentHandle = kimWeapHandles.pop(0)
            if currentHandle.abilities() == [0x800B, 0x8000, 0x8064, 0x00FF]:
                return True
    return False


def armor_array_character(charNum):
    equipHandles = all_equipment()
    firstEquipment = True
    charWeaps = []
    while len(equipHandles) > 0:
        currentHandle = equipHandles.pop(0)
        if currentHandle.owner() == charNum and currentHandle.equipment_type() == 1:
            if firstEquipment:
                charWeaps = [currentHandle]
                firstEquipment = False
            else:
                charWeaps.append(currentHandle)
    try:
        return charWeaps
    except Exception:
        return []


def equipped_armor_has_ability(charNum: int, abilityNum: int = 0x801D):
    equipHandles = armor_array_character(charNum)
    while len(equipHandles) > 0:
        currentHandle = equipHandles.pop(0)
        if currentHandle.is_equipped() == charNum:
            print("## Owner:", currentHandle.owner())
            print("## Equipped:", currentHandle.is_equipped())
            print("## Has Ability:", currentHandle.has_ability(abilityNum))
            if currentHandle.has_ability(abilityNum):
                return True
            else:
                return False


def equip_weap_cursor():
    global baseValue

    key = baseValue + 0x01440A38
    retVal = process.readBytes(key, 1)
    return retVal


def assign_ability_to_equip_cursor():
    global baseValue
    key = baseValue + 0x01440AD0
    retVal = process.readBytes(key, 1)
    return retVal


# ------------------------------
# Shopping related stuff


def item_shop_menu():
    global baseValue
    key = baseValue + 0x0085A860
    retVal = process.readBytes(key, 1)
    return retVal


def equip_shop_menu():
    global baseValue
    key = baseValue + 0x0085A83C
    retVal = process.readBytes(key, 1)
    return retVal


def cure_menu_open():
    global baseValue
    key = baseValue + 0x01440A35
    retVal = process.readBytes(key, 1)
    return retVal


def item_menu_number():
    global baseValue
    key = baseValue + 0x0085A318
    retVal = process.readBytes(key, 1)
    return retVal


def item_menu_column():
    global baseValue
    key = baseValue + 0x01440A48
    retVal = process.readBytes(key, 1)
    return retVal


def information_active():
    global baseValue
    key = baseValue + 0x0146AA28
    retVal = process.readBytes(key, 1)
    return retVal == 7


def item_menu_row():
    global baseValue
    key = baseValue + 0x01440A38
    retVal = process.readBytes(key, 1)
    return retVal


def equip_sell_row():
    global baseValue
    key = baseValue + 0x01440C00
    retVal = process.readBytes(key, 1)
    return retVal


def name_confirm_open():
    return read_val(0x014408E8) == 8


def equip_buy_row():
    global baseValue
    key = baseValue + 0x01440B68
    retVal = process.readBytes(key, 1)
    return retVal


def cursor_enabled_in_equip():
    global baseValue
    key = baseValue + 0x008CC7EC
    retVal = process.readBytes(key, 1)
    return retVal == 12


def equip_confirmation_row():
    global baseValue
    key = baseValue + 0x01440C98
    retVal = process.readBytes(key, 1)
    return retVal


def equip_menu_open_from_char():
    global baseValue
    key = baseValue + 0x01440A2A
    retVal = process.readBytes(key, 1)
    return retVal == 5


def config_cursor():
    global baseValue
    key = baseValue + 0x0146A404
    retVal = process.readBytes(key, 1)
    return retVal


def read_val(address, bytes=1):
    global baseValue
    key = baseValue + address
    retVal = process.readBytes(key, bytes)
    return retVal


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
    global baseValue
    key = baseValue + 0x0085A3FC
    retVal = process.readBytes(key, 1)
    return retVal


def purchasing_amount_items():
    return read_val(0x01440C00)


def config_aeon_cursor_column():
    global baseValue
    key = baseValue + 0x0085A454
    retVal = process.readBytes(key, 1)
    return retVal


def load_menu_cursor():
    global baseValue
    key = baseValue + 0x008E72E0
    retVal = process.readBytes(key, 1)
    return retVal


def rikku_overdrive_item_selected_number():
    global baseValue
    key = baseValue + 0x00D2C948
    retVal = process.readBytes(key, 1)
    return retVal


def sphere_grid_placement_open():
    global baseValue
    key = baseValue + 0x012ACB6B
    retVal = process.readBytes(key, 1)
    return retVal


def moving_prompt_open():
    global baseValue
    key = baseValue + 0x012AD543
    retVal = process.readBytes(key, 1)
    return retVal


# ------------------------------
# Bevelle Trials indicators


def bt_bi_direction():
    key = baseValue + 0x0092DEED
    return process.readBytes(key, 1)


def bt_tri_direction_main():
    key = baseValue + 0x0092E1ED
    return process.readBytes(key, 1)


# ------------------------------
# Gagazet trials


def gt_outer_ring():
    global baseValue
    key = baseValue + 0x014DFC34
    height = float_from_integer(process.read(key))
    return height


def gt_inner_ring():
    global baseValue
    key = baseValue + 0x014DFDA0
    height = float_from_integer(process.read(key))
    return height


# ------------------------------
# Save spheres


def get_save_sphere_details():
    mapVal = get_map()
    storyVal = get_story_progress()
    print("Map:", mapVal, "| Story:", storyVal)
    x = 0
    y = 0
    diag = 0
    if mapVal == 389:
        # Ammes
        x = 994
        y = -263
        diag = 9
    if mapVal == 49:
        # Baaj
        x = 230
        y = -215
        diag = 17
    if mapVal == 63:
        # Before Klikk
        x = -100
        y = 143
        diag = 29
    if mapVal == 64:
        # Before Tros
        x = 5
        y = -170
        diag = 3
    if mapVal == 19:
        # Besaid beach
        x = -310
        y = -475
        diag = 48
    if mapVal == 65:
        # Kilika - before Geneaux
        x = -3
        y = 175
        diag = 46
    if mapVal == 88:
        # Luca before Oblitzerator
        x = 175
        y = -310
        diag = 62
    if mapVal == 123:
        # Luca after Oblitzerator
        x = -270
        y = -45
        diag = 90
    if mapVal == 171:
        # Mi'ihen agency
        x = 35
        y = -10
        diag = 85
    if mapVal == 115:
        # Old Road
        x = 48
        y = -910
        diag = 40
    if mapVal == 59 and get_story_progress() > 1000:
        # Miihen last screen, late game
        x = 15
        y = 125
        diag = 121
    if mapVal == 92:
        # MRR
        x = 5
        y = -740
        if get_story_progress() < 1000:
            diag = 39
        else:
            diag = 43  # Nemesis run
    if mapVal == 119:
        # Battle Site
        x = -55
        y = 3335
        diag = 115
    if mapVal == 110:
        # Mac woods start
        x = 255
        y = -15
        diag = 84
    if mapVal == 221:
        # Mac woods before Spherimorph
        x = 195
        y = -123
        if get_story_progress() < 4000:
            diag = 19
        else:
            diag = 23
    if mapVal == 106:
        # Mac Temple entrance
        x = -22
        y = -127
        diag = 68
    if mapVal == 153:
        # Mac Temple exit
        x = 820
        y = -235
        diag = 44
    if mapVal == 129:
        # Bikanel start
        x = 19
        y = -60
        diag = 35
    if mapVal == 136:
        # Bikanel Rikku tent
        x = 205
        y = 30
        diag = 59
    if mapVal == 130:
        # Home entrance screen
        x = 61
        y = 92
        diag = 25
    if mapVal == 208:
        # Highbridge before Natus
        x = 33
        y = 1251
        diag = 124
    if mapVal == 194:
        # Airship while rescuing Yuna, cockpit
        x = -275
        y = 344
        if get_story_progress() < 2700:  # During Yuna rescue
            diag = 217
        else:  # Before Shedinja/Highbridge
            diag = 220
    if mapVal == 266:
        x = -305
        y = 185
        if get_story_progress() < 3000:  # NEA trip
            diag = 39
        else:
            diag = 43
    if mapVal == 285:
        # After Flux
        x = 140
        y = -640
        diag = 84
    if mapVal == 316:
        # Just before Zan trials
        x = -20
        y = 358
        diag = 25
    if mapVal == 318:
        # Before Yunalesca
        x = -5
        y = -170
        diag = 26
    if mapVal == 140:
        # Thunder plains
        x = -45
        y = -870
        diag = 77
    if mapVal == 322:  # Nemesis run
        # Inside Sin, next to airship
        x = 225
        y = -250
        diag = 15
    if mapVal == 19:  # Nemesis run
        # Besaid beach
        x = -310
        y = -475
        diag = 55
    if mapVal == 263:  # Nemesis run
        # Thunder Plains agency
        x = -30
        y = -10
        diag = 114
    if mapVal == 307:  # Nemesis run
        # Monster Arena
        x = 4
        y = 5
        diag = 166
    if mapVal == 98:  # Nemesis run
        # Kilika docks
        x = 46
        y = -252
        diag = 34
    if mapVal == 82:  # Nemesis run
        # Djose temple
        x = 100
        y = -240
        diag = 89
    if mapVal == 137:  # Nemesis run
        # Bikanel Desert
        x = -15
        y = 240
        diag = 31
    if mapVal == 313:  # Nemesis run
        # Zanarkand campfire
        x = 135
        y = -1
        diag = 4
    if mapVal == 327:  # Nemesis run
        # Sin, end zone
        x = -37
        y = -508
        diag = 10
    if mapVal == 258:  # Nemesis run
        # Omega (only used in Nemesis)
        x = -112
        y = -1066
        diag = 23
    if mapVal == 307:
        # Monster Arena (only used in Nemesis)
        x = 2
        y = 5
        diag = 166
    if mapVal == 259:  # Nemesis run
        # Gagazet (only used in Nemesis)
        x = -59
        y = 99
        diag = 219
    if mapVal == 82:
        # Djose temple (only used in Nemesis)
        x = 97
        y = -241
        diag = 89
    if mapVal == 128:  # Nemesis run
        # MRR upper lift (only used in Nemesis)
        x = 230
        y = 140
        diag = 68
    print("Values: [", x, ",", y, "] -", diag)
    return [x, y, diag]


def touch_save_sphere(save_cursor_num: int = 0):
    print("MEM - Touch Save Sphere")
    clear_save_menu_cursor()
    clear_save_menu_cursor_2()

    ssDetails = get_save_sphere_details()
    while user_control():
        targetPathing.set_movement([ssDetails[0], ssDetails[1]])
        xbox.tap_b()
        wait_frames(1)
    FFXC.set_neutral()
    print("Waiting for cursor to reset before we do things - Mark 1")
    while menu_control() == 0:
        pass
    wait_frames(1)
    print("Mark 2")
    # waitFrames(300)
    inc = 0

    while not (
        save_menu_cursor() == 0
        and save_menu_cursor_2() == 0
        and diag_progress_flag() == ssDetails[2]
    ):
        print(
            "Cursor test: A",
            get_story_progress(),
            "|",
            diag_progress_flag(),
            "|",
            get_map(),
            "|",
            inc,
        )
        inc += 1
        if save_menu_open():
            xbox.tap_a()
        elif diag_skip_possible() and diag_progress_flag() != ssDetails[2]:
            xbox.tap_b()
    while not (save_menu_cursor() == 0 and save_menu_cursor_2() == 0):
        print(
            "Cursor test: B",
            save_menu_cursor(),
            "|",
            save_menu_cursor_2(),
            "|",
            diag_skip_possible(),
            "|",
            inc,
        )
        inc += 1
        if save_menu_open():
            xbox.tap_a()
        elif diag_skip_possible():
            xbox.tap_a()
    while save_menu_cursor() == 0 and save_menu_cursor_2() == 0:
        print(
            "Cursor test: C",
            save_menu_cursor(),
            "|",
            save_menu_cursor_2(),
            "|",
            diag_skip_possible(),
            "|",
            get_story_progress(),
            "|",
            inc,
        )
        inc += 1
        if save_menu_open():
            xbox.tap_a()
        elif diag_skip_possible():
            if diag_progress_flag() != ssDetails[2]:
                xbox.tap_b()
            else:
                xbox.tap_a()
    while not user_control():
        print("Cursor test: D", save_menu_cursor(), "|", save_menu_cursor_2(), "|", inc)
        inc += 1
        if save_menu_open():
            xbox.tap_a()
        else:
            xbox.tap_b()
    print("Cursor test: E", save_menu_cursor(), "|", save_menu_cursor_2(), "|", inc)
    inc += 1


def touch_save_sphere_not_working(save_cursor_num: int = 0):
    print("MEM - Touch Save Sphere")

    ssDetails = get_save_sphere_details()
    while user_control():
        targetPathing.set_movement([ssDetails[0], ssDetails[1]])
        xbox.tap_b()
        wait_frames(1)
    FFXC.set_neutral()
    print("Waiting for cursor to reset before we do things - Mark 1")
    while menu_control() == 0:
        pass
    wait_frames(1)
    print("Mark 2")
    # waitFrames(300)

    xbox.tap_a()
    # while saveMenuCursor() == 0:
    #    if saveMenuOpen():
    #        xbox.tapA()
    #    elif diagProgressFlag() != ssDetails[2] and diagSkipPossible():
    #        xbox.tapB()
    #    else:
    #        xbox.tapA()

    while not user_control():
        if save_menu_open():
            xbox.tap_a()
        elif diag_progress_flag() == ssDetails[2]:
            print("Cursor test:", save_menu_cursor())
            print("Cursor test2:", save_menu_cursor_2())
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
        print("No need to clear. User is in control.")
    else:
        print("Save dialog has popped up for some reason. Attempting clear.")
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
    key = baseValue + 0x00D35EE0
    return process.readBytes(key, 1)


def mem_test_val_1():
    key = baseValue + 0x00D35EE1
    return process.readBytes(key, 1)


def mem_test_val_2():
    key = baseValue + 0x00D35EE2
    return process.readBytes(key, 1)


def mem_test_val_3():
    key = baseValue + 0x00D35EE3
    return process.readBytes(key, 1)


# ------------------------------


def print_memory_log():
    pass


def print_memory_log_backup():
    global baseValue
    global process
    # (Pointer) [[ffx.exe + 8DED2C] + 0x6D0]
    ptrVal = process.read(baseValue + 0x008DED2C)
    finalCoords = ptrVal + 0x6D0
    coord1 = process.read(finalCoords)
    logs.write_stats("Temp Value 1: " + str(coord1))

    # (Pointer) [[ffx.exe + 8DED2C] + 0x704]
    ptrVal = process.read(baseValue + 0x008DED2C)
    finalCoords = ptrVal + 0x704
    logs.write_stats("Temp Value 2: " + str(coord1))

    # (Pointer) [[ffx.exe + 8CB9D8] + 0x10D2E]
    ptrVal = process.read(baseValue + 0x008CB9D8)
    finalCoords = ptrVal + 0x10D2E
    logs.write_stats("Temp Value 3: " + str(coord1))

    # ffx.exe + D2A00C
    logs.write_stats("Temp Value 4: " + str(coord1))


# ------------------------------
# Load game functions


def load_game_page():
    global baseValue
    key = baseValue + 0x008E72DC
    retVal = process.readBytes(key, 1)
    return retVal


def load_game_cursor():
    global baseValue
    key = baseValue + 0x008E72E0
    retVal = process.readBytes(key, 1)
    return retVal


def load_game_pos():
    return load_game_page() + load_game_cursor()


def luca_workers_battle_id():
    return read_val(0x01466DCC)


# ------------------------------
# RNG tracking based on the first six hits


def last_hit_init():
    global baseValue
    print("Initializing values")
    key = baseValue + 0xD334CC
    ptrVal = process.read(key)
    lastHitVals = [0] * 8
    try:
        for x in range(8):
            lastHitVals[x] = process.read(ptrVal + ((x + 20) * 0xF90) + 0x7AC)
            # print("Val:", lastHitVals[x])
        # print(lastHitVals)
        game_vars.first_hits_set(lastHitVals)
        return True
    except Exception:
        return False


def last_hit_check_change() -> int:
    global baseValue
    key = baseValue + 0xD334CC
    ptrVal = process.read(key)
    changeFound = False
    changeValue = 9999
    for x in range(8):
        memVal = process.read(ptrVal + ((x + 20) * 0xF90) + 0x7AC)
        if memVal != game_vars.first_hits_value(x) and not changeFound:
            changeFound = True
            changeValue = memVal
            print("**Registered hit:", changeValue)
            # logs.writeStats(changeValue)
            last_hit_init()
            print("Mark 1")
            return int(changeValue)
            print("Mark 2")
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
    global baseValue
    offset = baseValue + 0xD35ED8 + (index * 4)
    arrayVal = [process.read(offset)]
    for x in range(array_size):
        arrayVal.append(roll_next_rng(arrayVal[x], index))
    return arrayVal


def next_crit(character: int, char_luck: int, enemy_luck: int) -> int:
    # Returns the next time the character will critically strike, counting number of advances from present.
    # If 255 is returned, there will not be a next crit in the foreseeable future.
    rngIndex = min(20 + character, 27)
    rngArray = rng_array_from_index(index=rngIndex, array_len=200)
    del rngArray[0]
    del rngArray[0]
    for x in range(len(rngArray)):
        crit_roll = s32(rngArray[x]) % 101
        crit_chance = char_luck - enemy_luck
        if crit_roll < crit_chance:
            if x == 0:
                pass
            else:
                return x
    return 255


def future_attack_will_crit(
    character: int, char_luck: int, enemy_luck: int, attack_index: int = 0
) -> bool:
    # Returns if a specific attack in the future will crit.
    # Attack Index 0 represents the next attack.
    # Assumes no escape attempts, primarily this is used for Aeons anyway.
    rngIndex = min(20 + character, 27)
    rngArray = rng_array_from_index(index=rngIndex, array_len=200)
    del rngArray[0]
    del rngArray[0]
    if attack_index > 90:
        return False
    crit_roll = s32(rngArray[attack_index * 2]) % 101
    crit_chance = char_luck - enemy_luck
    if crit_roll < crit_chance:
        return True
    return False


def rng_01():
    global baseValue
    return process.read(baseValue + 0xD35EDC)


def rng_01_array(array_len: int = 600):
    retVal = [rng_01()]  # First value is the current value
    for x in range(array_len):  # Subsequent values are based on first value.
        retVal.append(roll_next_rng(retVal[x], 1))
    return retVal


def rng_01_advances(advance_count: int = 50):
    testArray = rng_01_array()
    rangeVal = advance_count
    for i in range(rangeVal):
        testArray.append(testArray[i] & 0x7FFFFFFF)
    return testArray


def next_chance_rng_01(version="white"):
    testArray = rng_01_array()
    evenArray = []
    oddArray = []
    rangeVal = int((len(testArray) - 1) / 2) - 2
    if version == "white":
        modulo = 13
        battleIndex = 8
    else:
        modulo = 10
        battleIndex = 0
    for i in range(rangeVal):
        if (testArray[((i + 1) * 2) - 1] & 0x7FFFFFFF) % modulo == battleIndex:
            oddArray.append(i)
        if (testArray[(i + 1) * 2] & 0x7FFFFFFF) % modulo == battleIndex:
            evenArray.append(i)

    # print("------------------------------")
    # print("Next event will appear on the odd array without manip. Area:", version)
    # print("oddArray:", oddArray[0])
    # print("evenArray:", evenArray[0])
    # print("------------------------------")
    return [oddArray, evenArray]


def advance_rng_01():
    global baseValue
    key = baseValue + 0xD35EDC
    process.write(key, rng_01_array()[2])


def rng_02():
    global baseValue
    return process.read(baseValue + 0xD35EE0)


def rng_02_array(array_len: int = 200000):
    retVal = [rng_02()]  # First value is the current value
    for x in range(array_len):  # Subsequent values are based on first value.
        retVal.append(roll_next_rng(retVal[x], 2))
    return retVal


def set_test_rng_02():
    global baseValue
    key = baseValue + 0xD35EE0
    process.write(key, 3777588919)


def rng_10():
    global baseValue
    return process.read(baseValue + 0xD35F00)


def rng_10_array(array_len: int = 256):
    retVal = [rng_10()]  # First value is the current value
    for x in range(array_len):  # Subsequent values are based on first value.
        retVal.append(roll_next_rng(last_rng=retVal[x], index=10))
    return retVal


def next_chance_rng_10(drop_chance_val: int = 60) -> int:
    testArray = rng_10_array()
    for i in range(len(testArray)):
        if i < 3:
            pass
        elif (testArray[i] & 0x7FFFFFFF) % 255 < drop_chance_val:
            return i - 3


def next_chance_rng_10_full(drop_chance_val: int = 60) -> int:
    testArray = rng_10_array()
    resultsArray = [False, False, False]
    for i in range(len(testArray)):
        if i < 3:
            pass
        elif (testArray[i] & 0x7FFFFFFF) % 255 < drop_chance_val:
            resultsArray.append(True)
        else:
            resultsArray.append(False)
    return resultsArray


def next_chance_rng_10_calm() -> int:
    testArray = rng_10_array()
    for i in range(len(testArray)):
        if i < 3:
            pass
        elif (testArray[i] & 0x7FFFFFFF) % 255 >= 60 and (
            testArray[i + 3] & 0x7FFFFFFF
        ) % 255 < 60:
            return i - 3


def no_chance_x3_rng_10_highbridge() -> int:
    testArray = rng_10_array()
    for i in range(len(testArray)):
        if i < 3:
            pass
        elif (
            (testArray[i] & 0x7FFFFFFF) % 255 < 30
            and (testArray[i + 3] & 0x7FFFFFFF) % 255 < 30
            and (testArray[i] & 0x7FFFFFFF) % 255 < 30
        ):
            return i - 3


def advance_rng_10():
    global baseValue
    key = baseValue + 0xD35F00
    process.write(key, rng_10_array()[1])


def rng_12():
    global baseValue
    return process.read(baseValue + 0xD35F08)


def rng_12_array(advances: int = 255):
    retVal = [rng_12()]  # First value is the current value
    for x in range(advances):  # Subsequent values are based on first value.
        retVal.append(roll_next_rng(retVal[x], 12))
    return retVal


def next_chance_rng_12(beforeNatus: bool = False) -> int:
    abilityMod = 13

    nextChance = 256
    if beforeNatus:
        ptr = 5
    else:
        ptr = 1
    testArray = rng_12_array()
    while nextChance == 256:
        # Assume killer is aeon
        if ptr > 250:
            return 256
        elif (testArray[ptr + 1] & 0x7FFFFFFF) % 2 == 1:  # equipment
            # print("RNG12 ptr: ", ptr)
            baseMod = (abilityMod + ((testArray[ptr + 3] & 0x7FFFFFFF) & 7)) - 4
            abilities = (baseMod + ((baseMod >> 31) & 7)) >> 3

            if ptr == 1:
                if next_drop_rng_13(abilities, beforeNatus):
                    print("Mark1")
                    nextChance = 0
                else:
                    print("Mark2")
                    nextChance = 1
                if beforeNatus:
                    nextChance += 1
            else:
                nextChance = int((ptr - 1) / 4)
        else:
            ptr += 4
    if beforeNatus:
        nextChance -= 1
    return int(nextChance)


def advance_rng_12():
    global baseValue
    key = baseValue + 0xD35F08
    process.write(key, rng_12_array()[4])


def rng_13():
    global baseValue
    return process.read(baseValue + 0xD35F0C)


def rng_13_array(array_len: int = 20):
    retVal = [rng_13()]  # First value is the current value
    for x in range(array_len):  # Subsequent values are based on first value.
        retVal.append(roll_next_rng(retVal[x], 13))
    return retVal


def next_drop_rng_13(a_slots: int, before_natus: bool = False) -> int:
    outcomes = [4, 1, 1, 1, 2, 2, 3, 3]
    filledSlots = [9] * a_slots
    if before_natus:
        ptr = 2
    else:
        ptr = 1
    testArray = rng_13_array()
    while 9 in filledSlots and ptr < 20:
        try:
            if outcomes[(((testArray[ptr] & 0x7FFFFFFF) % 7) + 1)] in filledSlots:
                pass
            else:
                filledSlots.remove(9)
                filledSlots.append(outcomes[(((testArray[ptr] & 0x7FFFFFFF) % 7) + 1)])
        except Exception:
            pass
        ptr += 1

    # print("RNG13: ", filledSlots)

    if 1 in filledSlots:
        return True
    else:
        return False


def next_chance_rng_13() -> int:
    nextChance = 256
    outcomes = [4, 1, 1, 1, 2, 2, 3, 3]
    ptr = 1
    nextChance = 0
    testArray = rng_13_array()
    while nextChance == 0:
        # print("RNG13 outcome: ", outcomes[(((testArray[ptr] & 0x7fffffff) % 7) + 1)])
        if outcomes[(((testArray[ptr] & 0x7FFFFFFF) % 7) + 1)] == 1:
            nextChance = ptr
        else:
            ptr += 1
    print("Value found. ", ptr)
    return int(nextChance)


def advance_rng_13():
    global baseValue
    key = baseValue + 0xD35F0C
    process.write(key, rng_13_array()[4])


def rng_23():
    global baseValue
    return process.read(baseValue + 0xD35F16)


def rng_23_array(array_len: int = 200):
    retVal = [rng_23()]  # First value is the current value
    for x in range(array_len):  # Subsequent values are based on first value.
        retVal.append(roll_next_rng(retVal[x], 13))
    return retVal


def advance_rng_23():
    global baseValue
    key = baseValue + 0xD35F16
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
    global baseValue
    retArray = []
    for i in range(104):
        key = baseValue + 0xD30C9C + i
        retArray.append(process.readBytes(key, 1))
    return retArray


def arena_farm_check(
    zone: str = "besaid", end_goal: int = 10, report=False, return_array=False
):
    import nemesis.menu as menu

    complete = True
    zone = zone.lower()
    if zone == "besaid":
        zoneIndexes = [8, 15, 27]
    if zone == "kilika":
        zoneIndexes = [21, 30, 38, 61]
    if zone == "miihen":
        zoneIndexes = [0, 9, 16, 22, 34, 47, 50, 62, 85]
    if zone == "mrr":
        zoneIndexes = [5, 23, 40, 51, 63, 91]
    if zone == "djose":
        zoneIndexes = [1, 10, 17, 28, 31, 79, 83]
    if zone == "tplains":
        zoneIndexes = [6, 24, 35, 52, 64, 76, 89, 87]
    if zone == "maclake":
        zoneIndexes = [3, 11, 18, 36]
    if zone == "macwoods":
        zoneIndexes = [2, 25, 32, 65, 71, 94]
    if zone == "bikanel":
        zoneIndexes = [12, 29, 41, 42, 53, 88]
    if zone == "calm":
        zoneIndexes = [4, 13, 19, 33, 55, 57, 72, 73, 80]
    if zone == "gagazet":
        zoneIndexes = [14, 20, 37, 39, 45, 46, 49, 58, 60, 69, 84, 86]
    if zone == "stolenfayth":
        zoneIndexes = [7, 26, 44, 48, 54, 66, 68, 92, 98]
    if zone == "justtonberry":
        zoneIndexes = [98]
    if zone == "sin1":
        zoneIndexes = [37]
    if zone == "sin2":
        zoneIndexes = [56, 70, 77, 78, 81, 93, 90, 97]
    if zone == "omega":
        zoneIndexes = [67, 74, 75, 82, 95, 96, 99, 100, 101, 102, 103]

    testArray = arena_array()
    resultArray = []

    for i in range(len(zoneIndexes)):
        resultArray.append(testArray[zoneIndexes[i]])
        if testArray[zoneIndexes[i]] < end_goal:
            complete = False
    if report:
        print("############")
        print("Next Sphere Grid checkpoint:", game_vars.nem_checkpoint_ap())
        print(
            "Tidus S.levels:",
            get_tidus_slvl(),
            "- need levels:",
            menu.next_ap_needed(game_vars.nem_checkpoint_ap()),
        )
        print("Number of captures in this zone:")
        print(resultArray)
        print(
            "End goal is", end_goal, "minimum before leaving this zone for each index."
        )
        print("############")
    if return_array:
        return resultArray
    else:
        return complete


def arena_cursor():
    global baseValue

    key = baseValue + 0x00D2A084
    status = process.readBytes(key, 2)
    return status


# Escape logic, and used for others


def rng_from_index(index: int = 20):
    memTarget = 0xD35ED8 + (index * 0x4)
    global baseValue
    return process.read(baseValue + memTarget)


def rng_array_from_index(index: int = 20, array_len: int = 20):
    retVal = [rng_from_index(index)]  # First value is the current value
    for x in range(array_len):  # Subsequent values are based on first value.
        retVal.append(roll_next_rng(retVal[x], index))
    retVal = [
        x & 0x7FFFFFFF for x in retVal
    ]  # Anding it because that's the value that's actually used
    return retVal


def advance_rng_index(index: int = 43):
    global baseValue
    key = 0xD35ED8 + (index * 0x4)
    process.write(baseValue + key, rng_array_from_index(index=index)[1])


def next_steal(steal_count: int = 0, pre_advance: int = 0):
    useArray = rng_array_from_index(index=10, array_len=1 + pre_advance)
    stealRNG = useArray[1 + pre_advance] % 255
    stealChance = 2**steal_count
    print(
        "=== ",
        useArray[1],
        " === ",
        stealRNG,
        " < ",
        255 // stealChance,
        " = ",
        stealRNG < (255 // stealChance),
    )
    return stealRNG < (255 // stealChance)


def next_steal_rare(pre_advance: int = 0):
    useArray = rng_array_from_index(index=11, array_len=1 + pre_advance)
    stealCritRNG = useArray[1 + pre_advance] % 255
    return stealCritRNG < 32
