import s4cl_ctypes
from s4cl_ctypes import wintypes

from privacy_protector.modinfo import S4CLModInfo
from privacy_protector.s4cl.s4cl_common_log_registry import S4CLCommonLog
log = S4CLCommonLog(S4CLModInfo.mod_name)
log.debug(f"hwnd ...")


class ManageHWND:
    # Constants
    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_VM_READ = 0x0010

    # Windows API functions
    FindWindowEx = s4cl_ctypes.windll.user32.FindWindowExW
    GetWindowThreadProcessId = s4cl_ctypes.windll.user32.GetWindowThreadProcessId
    OpenProcess = s4cl_ctypes.windll.kernel32.OpenProcess
    EnumWindows = s4cl_ctypes.windll.user32.EnumWindows
    EnumWindowsProc = s4cl_ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    GetWindowText = s4cl_ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = s4cl_ctypes.windll.user32.GetWindowTextLengthW

    # Helper function to get process ID from a window handle
    def get_process_id(self, hwnd):
        process_id = s4cl_ctypes.c_ulong()
        # thread_id = ManageHWND.GetWindowThreadProcessId(hwnd, s4cl_ctypes.byref(process_id))
        return process_id.value

    # Callback function for EnumWindows
    def enum_windows_callback(self, hwnd, lParam):
        process_id = self.get_process_id(hwnd)
        if process_id == lParam:
            title_length = ManageHWND.GetWindowTextLength(hwnd) + 1
            title = s4cl_ctypes.create_unicode_buffer(title_length)
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
