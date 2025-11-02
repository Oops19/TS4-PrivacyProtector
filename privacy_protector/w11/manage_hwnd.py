#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from privacy_protector import pp_ctypes
from privacy_protector.pp_ctypes import wintypes

from privacy_protector.modinfo import S4CLModInfo
from privacy_protector.s4cl.s4cl_common_log_registry import S4CLCommonLog
log = S4CLCommonLog(S4CLModInfo.mod_name)
log.debug(f"hwnd ...")


class ManageHWND:
    # Constants
    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_VM_READ = 0x0010

    # Windows API functions
    FindWindowEx = pp_ctypes.windll.user32.FindWindowExW
    GetWindowThreadProcessId = pp_ctypes.windll.user32.GetWindowThreadProcessId
    OpenProcess = pp_ctypes.windll.kernel32.OpenProcess
    EnumWindows = pp_ctypes.windll.user32.EnumWindows
    EnumWindowsProc = pp_ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    GetWindowText = pp_ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = pp_ctypes.windll.user32.GetWindowTextLengthW

    # Helper function to get process ID from a window handle
    def get_process_id(self, hwnd):
        process_id = pp_ctypes.c_ulong()
        # thread_id = ManageHWND.GetWindowThreadProcessId(hwnd, pp_ctypes.byref(process_id))
        return process_id.value

    # Callback function for EnumWindows
    def enum_windows_callback(self, hwnd, lParam):
        process_id = self.get_process_id(hwnd)
        if process_id == lParam:
            title_length = ManageHWND.GetWindowTextLength(hwnd) + 1
            title = pp_ctypes.create_unicode_buffer(title_length)
            ManageHWND.GetWindowText(hwnd, title, title_length)
            vhWnds.append((hwnd, title.value))  # add the found hwnd and title to the list
            # log.debug(f"Found hWnd {hwnd} with title: {title.value}")
        return True

    # Function to get all windows associated with a process ID
    def get_all_windows_from_process_id(self, dwProcessID):
        global vhWnds
        vhWnds = []  # list to store found window handles and titles
        ManageHWND.EnumWindows(ManageHWND.EnumWindowsProc(self.enum_windows_callback), dwProcessID)
        return vhWnds
