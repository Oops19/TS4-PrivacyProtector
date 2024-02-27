"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY

Code heavily modified and merged together by o19 with written permission. All PyDoc removed as parameters may be used differently.
Most of my other mods use S4CL, embedding methods like this is a pain.
Use S4CL https://github.com/ColonolNutty/Sims4CommunityLibrary unless you really feel the need to make a standalone mod.
"""


import threading
import time

import services
from privacy_protector.modinfo import S4CLModInfo
from privacy_protector.s4cl.s4cl_common_log_registry import S4CLCommonLog
from privacy_protector.s4cl.s4cl_common_basic_notification import S4CLCommonBasicNotification

from ui.ui_dialog_notification import UiDialogNotification

log = S4CLCommonLog(S4CLModInfo.mod_name)
log.enable()
log.debug(f"Starting {S4CLModInfo.mod_name}")


class PrivacyProtector:

    previous_message = None
    previous_urgency = None

    thread = None
    _cache = {}

    def __init__(self):
        PrivacyProtector.start_thread()

    @staticmethod
    def start_thread():
        if PrivacyProtector.thread:
            return
        PrivacyProtector.thread = threading.Thread(target=PrivacyProtector._thread, args=())
        PrivacyProtector.thread.daemon = True
        PrivacyProtector.thread.start()

    def _thread(*args, **kwargs):
        n = 0
        while True:
            try:
                n += 1
                if PrivacyProtector._cache or n == 100:
                    log.debug(f"PrivacyProtector._cache: {PrivacyProtector._cache}")
                    n = 0
                current_zone = services.current_zone()
                if getattr(current_zone, 'is_zone_running', None):
                    if PrivacyProtector._cache:
                        local_cache = PrivacyProtector._cache.copy()
                        log.debug(f"local_cache {local_cache}")
                        for message, urgency in local_cache.items():
                            PrivacyProtector.show_notification(message, urgency)
                        PrivacyProtector._cache = {}
                time.sleep(30)
            except Exception as e:
                log.error(f"Oops '{e}' in PrivacyProtector._thread()")
                time.sleep(60)

    @staticmethod
    def show_notification(message, urgency=UiDialogNotification.UiDialogNotificationUrgency.URGENT):
        try:

            mod_identifier = "Privacy Protector"
            basic_notification = S4CLCommonBasicNotification(
                0xFC089996,  # '{0.String}'
                0xFC089996,  # '{0.String}'
                title_tokens=(mod_identifier,),
                description_tokens=(message,),
                urgency=urgency
            )
            basic_notification.show()
        except Exception as e:
            PrivacyProtector._cache.update({message: urgency})
            raise e


PrivacyProtector()
