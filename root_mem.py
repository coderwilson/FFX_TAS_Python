import logging
from ctypes import (
    POINTER,
    Structure,
    addressof,
    c_char,
    c_void_p,
    pointer,
    sizeof,
    windll,
)
from ctypes.wintypes import BYTE, DWORD, HMODULE

logger = logging.getLogger(__name__)

PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
TH32CS_SNAPMODULE = 0x00000008

CreateToolhelp32Snapshot = windll.kernel32.CreateToolhelp32Snapshot
Process32First = windll.kernel32.Process32First
Process32Next = windll.kernel32.Process32Next
Module32First = windll.kernel32.Module32First
Module32Next = windll.kernel32.Module32Next
GetLastError = windll.kernel32.GetLastError
OpenProcess = windll.kernel32.OpenProcess
GetPriorityClass = windll.kernel32.GetPriorityClass
CloseHandle = windll.kernel32.CloseHandle


class MODULEENTRY32(Structure):
    _fields_ = [
        ("dwSize", DWORD),
        ("th32ModuleID", DWORD),
        ("th32ProcessID", DWORD),
        ("GlblcntUsage", DWORD),
        ("ProccntUsage", DWORD),
        ("modBaseAddr", POINTER(BYTE)),
        ("modBaseSize", DWORD),
        ("hModule", HMODULE),
        ("szModule", c_char * 256),
        ("szExePath", c_char * 260),
    ]


def list_process_modules(ProcessID):
    hModuleSnap = c_void_p(0)
    me32 = MODULEENTRY32()
    me32.dwSize = sizeof(MODULEENTRY32)
    hModuleSnap = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, ProcessID)

    ret = Module32First(hModuleSnap, pointer(me32))
    if ret == 0:
        logger.error("ListProcessModules() Error on Module32First[%d]", GetLastError())
        CloseHandle(hModuleSnap)
        return False

    complete = False
    while not complete:
        logger.debug(f"MODULE NAME: {me32.szModule}")
        logger.debug(f"executable: {me32.szExePath}")
        logger.debug(f"process ID: {me32.th32ProcessID}")
        logger.debug(f"ref count (g): {me32.GlblcntUsage}")
        logger.debug(f"ref count (p): {me32.ProccntUsage}")
        logger.debug(f"base address: {me32.modBaseAddr}")
        try:
            logger.debug(
                f"Adjusted address = {hex(addressof(me32.modBaseAddr.contents))}"
            )
            ret_val = addressof(me32.modBaseAddr.contents)
        except Exception as x:
            logger.debug(f"adjusted 3 error: {x}")
        logger.debug(f"base size: {me32.modBaseSize}")

        if me32.szModule == b"FFX.exe":
            complete = True
        else:
            ret = Module32Next(hModuleSnap, pointer(me32))

    CloseHandle(hModuleSnap)
    return ret_val
