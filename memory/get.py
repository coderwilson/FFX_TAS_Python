import ctypes
import ctypes.wintypes
import os.path

from ReadWriteMemory import Process, ReadWriteMemory, ReadWriteMemoryError

import memory.main

PROCESS_QUERY_INFORMATION = 0x0400
MAX_PATH = 260
base_value = 0


class LocProcess(Process):
    def __init__(self, *args, **kwargs):
        super(LocProcess, self).__init__(*args, **kwargs)

    def read_bytes(self, lp_base_address: int, size: int = 4):
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

    def write_bytes(self, lp_base_address: int, value: int, size: int = 4) -> bool:
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


rwm = FFXMemory()
process = rwm.get_process_by_name("FFX.exe")


def cutscene_id():
    global base_value
    key = base_value + 0xD27C88
    cutscene_alt = process.read_bytes(key, 4)
    storyline_prog = memory.main.get_story_progress()
    dialogue = memory.main.diag_progress_flag()
    return (cutscene_alt, storyline_prog, dialogue)
