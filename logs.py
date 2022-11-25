import datetime

import memory.main

try:
    from memory.main import base_value
except Exception:
    base_value = 0x0
game = "FFX_"
ext = ".txt"
file_name = "none"
file_stats = "none"
file_plot = "none"
file_mem_change = "none"
file_rng = "none"


def write_stats(message):
    global stats_file
    global file_stats

    stats_file = open(file_stats, "a")
    stats_file.write(str(message))
    stats_file.write("\n")
    stats_file.close()


def next_stats(rng_seed_num):
    global file_stats
    global game
    global ext
    if file_stats == "none":
        time_now = datetime.datetime.now()
        file_stats = (
            "logs/"
            + game
            + "Stats_ "
            + str(rng_seed_num)
            + "_"
            + str(time_now.year)
            + str(time_now.month)
            + str(time_now.day)
            + "_"
            + str(time_now.hour)
            + "_"
            + str(time_now.minute)
            + "_"
            + str(time_now.second)
            + ext
        )

        global stats_file
        stats_file = open(file_stats, "x")
        stats_file.close()

        stats_file = open(file_stats, "a")
        stats_file.write("Stats file is ready for writing!\n")
        stats_file.write("\n")
        stats_file.close()
    print("Stats file is ready for writing!\n")


def reset_stats_log():
    global file_stats
    file_stats = "none"


def write_plot(message):
    global plot_file
    global file_plot

    plot_file = open(file_plot, "a")
    plot_file.write(str(message))
    plot_file.write("\n")
    plot_file.close()


def next_plot():
    global file_plot
    global game
    global ext
    if file_plot == "none":
        time_now = datetime.datetime.now()
        file_plot = (
            "logs/"
            + game
            + "Plot_ "
            + str(time_now.year)
            + str(time_now.month)
            + str(time_now.day)
            + "_"
            + str(time_now.hour)
            + "_"
            + str(time_now.minute)
            + "_"
            + str(time_now.second)
            + ext
        )

        global plot_file
        plot_file = open(file_plot, "x")
        plot_file.close()

        plot_file = open(file_plot, "a")
        plot_file.write("plotting file is ready for writing!\n")
        plot_file.write("\n")
        plot_file.close()
        print("X/Y plotting file is ready for writing!\n")


def write_mem_change(message):
    global mem_change_file
    global file_mem_change

    mem_change_file = open(file_mem_change, "a")
    mem_change_file.write(str(message))
    mem_change_file.write("\n")
    mem_change_file.close()


def open_rng_track():
    global file_rng
    global game
    global ext
    time_now = datetime.datetime.now()
    file_rng = (
        "logs/"
        + game
        + "RNG_ "
        + str(time_now.year)
        + str(time_now.month)
        + str(time_now.day)
        + "_"
        + str(time_now.hour)
        + "_"
        + str(time_now.minute)
        + "_"
        + str(time_now.second)
        + ext
    )

    global RNGFile
    try:
        RNGFile = open(file_rng, "a")
    except Exception:
        RNGFile = open(file_rng, "x")
    RNGFile.close()

    RNGFile = open(file_rng, "a")
    RNGFile.write("RNG log is ready for writing!\n")
    RNGFile.write("\n")
    RNGFile.close()
    print("RNG log is ready for writing!\n")


def write_rng_track(message):
    global RNGFile
    global file_rng

    RNGFile = open(file_rng, "a")
    RNGFile.write(str(message))
    RNGFile.write("\n")
    RNGFile.close()


class MemChangeMonitor:
    def __init__(
        self,
        base_offset_ref,
        is_pointer_ref=False,
        ptr_offset_ref=0x0,
        type_ref="4byte",
        child_report: int = 0,
    ):
        self.is_pointer = is_pointer_ref
        self.base_offset = base_offset_ref
        if self.is_pointer:
            self.ptr_offset = ptr_offset_ref
        self.var_type = type_ref
        self.key = base_value + 0x003988A5

        self.set_last_value()

        if child_report != 0:
            self.report_on_child = False
        else:
            self.report_on_child = True
            self.child_handle = MemChangeMonitor(
                self.base_offset, True, self.ptr_offset, self.var_type, 0
            )

    def set_last_value(self):
        if self.is_pointer:
            ptr_ref = memory.main.process.read_bytes(self.key, 4)

            if self.var_type == "byte":
                self.last_value = memory.main.process.read_bytes(
                    ptr_ref + self.ptr_offset, 1
                )
            elif self.var_type == "2byte":
                self.last_value = memory.main.process.read_bytes(
                    ptr_ref + self.ptr_offset, 2
                )
            elif self.var_type == "4byte":
                self.last_value = memory.main.process.read_bytes(
                    ptr_ref + self.ptr_offset, 4
                )
            elif self.var_type == "float":
                self.last_value = memory.main.float_from_integer(
                    memory.main.process.read_bytes(ptr_ref + self.ptr_offset, 4)
                )
        else:
            if self.var_type == "byte":
                self.last_value = memory.main.process.read_bytes(self.key, 1)
            elif self.var_type == "2byte":
                self.last_value = memory.main.process.read_bytes(self.key, 2)
            elif self.var_type == "4byte":
                self.last_value = memory.main.process.read_bytes(self.key, 4)
            elif self.var_type == "float":
                self.last_value = memory.main.float_from_integer(
                    memory.main.process.read_bytes(self.key, 4)
                )

    def report_if_change(self):
        if self.check_change():
            if self.report_on_child:
                write_mem_change("Value changed (parent)")
            else:
                write_mem_change("Value changed")
            write_mem_change("Base offset: " + str(self.base_offset))
            write_mem_change("Pointer value: " + str(self.is_pointer))
            if self.is_pointer:
                write_mem_change("Pointer offset: " + str(self.ptr_offset))
            write_mem_change("Type of variable: " + str(self.var_type))
            write_mem_change("Previous value: " + self.last_value)
            write_mem_change("Updated value: " + self.get_new_value())
            write_mem_change("Time of change: " + time_stamp())
            write_mem_change("?? Game state ??")
            write_mem_change("Story progress: " + str(memory.main.get_story_progress()))
            write_mem_change("Current map: " + str(memory.main.get_map()))
            write_mem_change("Battle Active: " + str(memory.main.battle_active()))

            write_mem_change("----------------------------")
            if self.report_on_child:
                self.child_handle.force_report_child()
            self.set_last_value()

    def force_report_child(self):
        write_mem_change("Value changed (child)")
        write_mem_change("Base offset: " + str(self.base_offset))
        write_mem_change("Pointer value: " + str(self.is_pointer))
        if self.is_pointer:
            write_mem_change("Pointer offset: " + str(self.ptr_offset))
        write_mem_change("Type of variable: " + str(self.var_type))
        write_mem_change("Previous value: " + self.last_value)
        write_mem_change("Updated value: " + self.get_new_value())
        write_mem_change("Time of change: " + time_stamp())
        write_mem_change("?? Game state ??")
        write_mem_change("Story progress: " + str(memory.main.get_story_progress()))
        write_mem_change("Current map: " + str(memory.main.get_map()))
        write_mem_change("Battle Active: " + str(memory.main.battle_active()))
        write_mem_change("----------------------------")
        self.set_last_value()

    def force_report(self):
        write_mem_change("Value force-reported")
        write_mem_change("Base offset: " + str(self.base_offset))
        write_mem_change("Pointer value: " + str(self.is_pointer))
        if self.is_pointer:
            write_mem_change("Pointer offset: " + str(self.ptr_offset))
        write_mem_change("Type of variable: " + str(self.var_type))
        write_mem_change("Previous value: " + self.last_value)
        write_mem_change("Updated value: " + self.get_new_value())
        write_mem_change("Time of change: " + time_stamp())
        write_mem_change("?? Game state ??")
        write_mem_change("Story progress: " + str(memory.main.get_story_progress()))
        write_mem_change("Current map: " + str(memory.main.get_map()))
        write_mem_change("Battle Active: " + str(memory.main.battle_active()))
        write_mem_change("----------------------------")
        self.set_last_value()

    def check_change(self):
        if self.is_pointer:
            ptr_ref = memory.main.process.read_bytes(self.key, 4)

            if self.var_type == "byte":
                if self.last_value != memory.main.process.read_bytes(
                    ptr_ref + self.ptr_offset, 1
                ):
                    return True
            elif self.var_type == "2byte":
                if self.last_value != memory.main.process.read_bytes(
                    ptr_ref + self.ptr_offset, 2
                ):
                    return True
            elif self.var_type == "4byte":
                if self.last_value != memory.main.process.read_bytes(
                    ptr_ref + self.ptr_offset, 4
                ):
                    return True
            elif self.var_type == "float":
                if self.last_value != memory.main.float_from_integer(
                    memory.main.process.read_bytes(ptr_ref + self.ptr_offset, 4)
                ):
                    return True
            return False
        else:
            if self.var_type == "byte":
                if self.last_value != memory.main.process.read_bytes(self.key, 1):
                    return True
            elif self.var_type == "2byte":
                if self.last_value != memory.main.process.read_bytes(self.key, 2):
                    return True
            elif self.var_type == "4byte":
                if self.last_value != memory.main.process.read_bytes(self.key, 4):
                    return True
            elif self.var_type == "float":
                if self.last_value != memory.main.float_from_integer(
                    memory.main.process.read_bytes(self.key, 4)
                ):
                    return True
            return False


def mem_change_list():
    # Base offset, pointer (True/False), pointer offset, type to be returned
    # Fifth element is to report on another offset, only works for pointers.
    # Types can be '1byte', '2byte', '4byte', or 'float'
    full_list = [
        [0x8E9004, True, 0x1C, "4byte", 0x8],
        [0x8E9004, True, 0x1C, "4byte", 0xC],
    ]

    return full_list


def mem_change_handle():
    ret_array = [0]
    first_ele = True
    mem_ref_list = mem_change_list()

    while len(mem_ref_list) != 0:
        if first_ele:
            first_ele = False
            variables = mem_ref_list.pop()
            ret_array[0] = MemChangeMonitor(
                base_offset_ref=variables[0],
                is_pointer_ref=variables[1],
                ptr_offset_ref=variables[2],
                type_ref=variables[3],
                child_report=variables[4],
            )
        else:
            variables = mem_ref_list.pop()
            ret_array.append(
                MemChangeMonitor(
                    base_offset_ref=variables[0],
                    is_pointer_ref=variables[1],
                    ptr_offset_ref=variables[2],
                    type_ref=variables[3],
                    child_report=variables[4],
                )
            )
    return ret_array


def time_stamp():
    return datetime.datetime.now()
