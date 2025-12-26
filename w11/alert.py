#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


import pp_ctypes
from w11.manage_hwnd import ManageHWND

from w11.message_in_a_box import MessageInABox

from privacy_protector.modinfo import S4CLModInfo
from privacy_protector.s4cl.s4cl_common_log_registry import S4CLCommonLog
log = S4CLCommonLog(S4CLModInfo.mod_name)


class Alert:
    def __init__(self, title: str, message: str, fatal: bool = False):
        try:
            dwProcessID = pp_ctypes.windll.kernel32.GetCurrentProcessId()
            # log.debug(f"hwnd dwProcessID {dwProcessID}")
            m = ManageHWND()
            windows = m.get_all_windows_from_process_id(dwProcessID)
            # log.debug(f"hwnd windows {windows}")
            hwnd = None
            for window in windows:
                _hwnd, _title = window
                if _title.endswith('4'):
                    hwnd = _hwnd
                    break
                if _title.endswith('UI') or _title.endswith('IME'):
                    continue
                hwnd = _hwnd

            log.debug(f"hwnd {hwnd}")
            mb = MessageInABox()
            mb.show_message_box(hwnd, title, message)

            if fatal:
                PROCESS_TERMINATE = 0x0001
                FALSE = 0
                dwProcessID = pp_ctypes.windll.kernel32.GetCurrentProcessId()
                hProcess = pp_ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, FALSE, dwProcessID)
                if hProcess != 0:
                    pp_ctypes.windll.kernel32.TerminateProcess(hProcess, -1)
                    pp_ctypes.windll.kernel32.CloseHandle(hProcess)

        except Exception as e:
            log.error(f"hwnd err {e}")
