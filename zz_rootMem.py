import ctypes
import ctypes.wintypes
from ctypes import *
from ctypes.wintypes import *

PROCESS_QUERY_INFORMATION = (0x0400)
PROCESS_VM_OPERATION = (0x0008)
PROCESS_VM_READ = (0x0010)
PROCESS_VM_WRITE = (0x0020)
TH32CS_SNAPMODULE = (0x00000008)

CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
Process32First = ctypes.windll.kernel32.Process32First
Process32Next = ctypes.windll.kernel32.Process32Next
Module32First = ctypes.windll.kernel32.Module32First
Module32Next = ctypes.windll.kernel32.Module32Next
GetLastError = ctypes.windll.kernel32.GetLastError
OpenProcess = ctypes.windll.kernel32.OpenProcess
GetPriorityClass = ctypes.windll.kernel32.GetPriorityClass
CloseHandle = ctypes.windll.kernel32.CloseHandle


class MODULEENTRY32(Structure):
    _fields_ = [('dwSize', DWORD),
                ('th32ModuleID', DWORD),
                ('th32ProcessID', DWORD),
                ('GlblcntUsage', DWORD),
                ('ProccntUsage', DWORD),
                ('modBaseAddr', POINTER(BYTE)),
                ('modBaseSize', DWORD),
                ('hModule', HMODULE),
                ('szModule', c_char * 256),
                ('szExePath', c_char * 260)]


def GetBaseAddr(ProcId, ProcName):
    me32 = MODULEENTRY32()
    me32.dwSize = sizeof(me32)
    hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, ProcId)
    if GetLastError() != 0:
        CloseHandle(hSnapshot)
        print('Handle Error %s', WinError())
        return 'Error'

    else:
        if Module32First(hSnapshot, byref(me32)):
            if me32.szModule == ProcName:
                CloseHandle(hSnapshot)
                return id(me32.modBaseAddr)

            else:
                Module32Next(hSnapshot, byref(me32))
                while int(GetLastError()) != 18:
                    if me32.szModule == ProcName:
                        CloseHandle(hSnapshot)
                        return id(me32.modBaseAddr)

                    else:
                        Module32Next(hSnapshot, byref(me32))

                CloseHandle(hSnapshot)
                print('Couldn\'t find Process with name %s', ProcName)

        else:
            print('Module32First is False %s', WinError())
            CloseHandle(hSnapshot)


def ListProcessModules(ProcessID):
    hModuleSnap = c_void_p(0)
    me32 = MODULEENTRY32()
    me32.dwSize = sizeof(MODULEENTRY32)
    hModuleSnap = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, ProcessID)

    ret = Module32First(hModuleSnap, pointer(me32))
    if ret == 0:
        print(
            'ListProcessModules() Error on Module32First[%d]', GetLastError())
        CloseHandle(hModuleSnap)
        return False

    complete = False
    while not complete:
        print("   MODULE NAME:     %s",         me32.szModule)
        print("   executable     = %s",         me32.szExePath)
        print("   process ID     = 0x%08X",     me32.th32ProcessID)
        print("   ref count (g)  =     0x%04X", me32.GlblcntUsage)
        print("   ref count (p)  =     0x%04X", me32.ProccntUsage)
        print("   base address   = 0x%08X",     me32.modBaseAddr)
        try:
            print("   Adjusted address   = 0x%08X", hex(
                ctypes.addressof(me32.modBaseAddr.contents)))
            retVal = ctypes.addressof(me32.modBaseAddr.contents)
        except Exception as x:
            print("adjusted 3 error:", x)
        print("   base size      = %d",         me32.modBaseSize)

        if me32.szModule == b'FFX.exe':
            complete = True
        else:
            ret = Module32Next(hModuleSnap, pointer(me32))

    CloseHandle(hModuleSnap)
    return retVal
