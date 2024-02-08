"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY

Code heavily modified and merged together by o19 with written permission. All PyDoc removed as parameters may be used differently.
Most of my other mods use S4CL, embedding methods like this is a pain.
Use S4CL https://github.com/ColonolNutty/Sims4CommunityLibrary unless you really feel the need to make a standalone mod.
"""


import os
from datetime import datetime


class S4CLCommonLog():
    def __init__(self, mod_name: str):
        try:
            log_path = os.path.join(os.path.dirname(os.path.realpath(__file__)).partition(f"{os.sep}Mods{os.sep}")[0], 'mod_logs')
            os.makedirs(log_path, exist_ok=True)
            filename = os.path.join(log_path, f"{mod_name}.txt")
        except:
            filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), f"{mod_name}.txt")
        self.filename = filename

    def log(self, log_level, log_message: str):
        t = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        with open(self.filename, "a") as fp:
            fp.write(f"{t}\t{log_level}\t{log_message}\n")

    def enable(self):
        pass

    def disable(self):
        pass

    def debug(self, message):
        self.log("DEBUG", message)

    def info(self, message):
        self.log("INFO", message)

    def warn(self, message):
        self.log("WARN", message)

    def error(self, message):
        self.log("ERROR", message)
