#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2025 https://github.com/Oops19
#


import time

from privacy_protector.modinfo import S4CLModInfo
from privacy_protector.s4cl.s4cl_common_log_registry import S4CLCommonLog

log = S4CLCommonLog(S4CLModInfo.mod_name)


class Alert:
    def __init__(self, title: str, message: str, fatal: bool = False):
        try:
            log.warn(f"{title}")
            log.error(f"{message}")
            if fatal:
                while True:
                    time.sleep(3600)
        except Exception as e:
            log.error(f"Error {e}")
