#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2022 https://github.com/Oops19
#


import os
import re
from typing import Tuple, Set, List

from zipfile import ZipFile
import time
import threading

import services
from privacy_protector.modinfo import S4CLModInfo
from ui.ui_dialog_notification import UiDialogNotification

from privacy_protector.privacy_protector import PrivacyProtector
from privacy_protector.s4cl.s4cl_common_log_registry import S4CLCommonLog

log = S4CLCommonLog(S4CLModInfo.mod_name)
log.debug(f"Scanner ...")


class Scanner:
    thread = None

    def __init__(self, mods_directory: str = None):
        if mods_directory is None:
            mods_directory = os.path.dirname(os.path.realpath(__file__)).partition(f"{os.sep}Mods{os.sep}")[0]
        Ts4ScriptFiles.allow_list = []
        mods_path = os.path.join(mods_directory, 'mod_data', 'privacy_protector', 'skip_mods')
        file_list = Ts4ScriptFiles.get_files(mods_path)
        for files in file_list:
            Ts4ScriptFiles.allow_list.append(files[1])
        log.debug(f"Scanner will not scan: {Ts4ScriptFiles.allow_list}")

        # Scan mods as soon as possible
        Ts4ScriptFiles.scan_files(None, None)
        log.debug(f"Scanner: Initial scan completed.")

        # Display notifications later
        Scanner.start_thread()

    @staticmethod
    def start_thread():
        if Scanner.thread:
            return
        Scanner.thread = threading.Thread(target=Scanner._thread, args=())
        Scanner.thread.daemon = True
        Scanner.thread.start()

    def _thread(*args, **kwargs):
        while True:
            current_zone = services.current_zone()
            if getattr(current_zone, 'is_zone_running', None):
                break
            time.sleep(1)

        if Ts4ScriptFiles.possible_issues == 0:
            message = f"Found no issues."
            urgency = UiDialogNotification.UiDialogNotificationUrgency.DEFAULT
        else:
            urgency = UiDialogNotification.UiDialogNotificationUrgency.URGENT
            if Ts4ScriptFiles.possible_issues == 1:
                message = f"Found one possible issue."
            else:
                message = f"*Found {Ts4ScriptFiles.possible_issues} possible issues."
        PrivacyProtector.show_notification(message, urgency=urgency)
        log.debug(f"Scanner: Notification '{message}' displayed.")


class Ts4ScriptFiles:
    allow_list = []
    possible_issues = 0

    @staticmethod
    def scan_files(output, search_string):
        c_ev = 0  # EVAL in mod
        o_ev = 0  # EVAL-like string in mod (eg: REEVALUATE())
        s_ev = 0  # EVAL in Privacy Protector - No matches, 'EVAL'.lower() using in code
        c_ex = 0  # EXEC in mod
        o_ex = 0  # EXEC-like string in mod (eg: EXECUTE())
        s_ex = 0  # EXEC in Privacy Protector - No matches, 'EVAL'.lower() using in code
        c = 0  # Other suspicious function in mod
        o = 0  # Other suspicious string in mod (eg: my_subprocess())
        s = 0  # Other suspicious function in Privacy Protector - Due to injections there will be matches
        review_mods: Set = set()

        try:
            mods_path = os.path.join(os.path.dirname(os.path.realpath(__file__)).partition(f"{os.sep}Mods{os.sep}")[0], 'Mods')
            file_list = Ts4ScriptFiles.get_files(mods_path)
            Ts4ScriptFiles.log(output, f"\n")
            Ts4ScriptFiles.log(output, f"*Scanning '{len(file_list)}' files in '{mods_path}'")
            for files in file_list:
                zipfile = os.path.join(files[0], files[1])
                _zipfile = zipfile.replace(mods_path, '')
                Ts4ScriptFiles.log(output, f"*Scanning '{_zipfile}")
                if files[1].endswith('ts4script') or files[1].endswith('zip'):
                    with ZipFile(zipfile, mode="r") as zf:
                        for file in zf.namelist():
                            with zf.open(file) as f:
                                data = f.read()
                                # return found_critical_e_val, found_something_e_val, found_self_e_val, found_critical_e_xec, found_something_e_xec, found_self_e_xec, found_critical, found_something, found_self
                                _c_ev, _o_ev, _s_ev, _c_ex, _o_ex, _s_ex, _c, _o, _s, _rf = Ts4ScriptFiles.check_content(output, search_string, data, zipfile.replace(mods_path, ''), file)
                                c_ev += _c_ev
                                o_ev += _o_ev
                                s_ev += _s_ev
                                c_ex += _c_ex
                                o_ex += _o_ex
                                s_ex += _s_ex
                                c += _c
                                o += _o
                                s += _s
                                if _rf:
                                    review_mods.add(f"{_zipfile}")
                else:
                    # py or pyc
                    with open(zipfile, mode="rb") as f:
                        data = f.read()
                        file = ''
                        _c_ev, _o_ev, _s_ev, _c_ex, _o_ex, _s_ex, _c, _o, _s, _rf = Ts4ScriptFiles.check_content(output, search_string, data, zipfile.replace(mods_path, ''), file)
                        c_ev += _c_ev
                        o_ev += _o_ev
                        s_ev += _s_ev
                        c_ex += _c_ex
                        o_ex += _o_ex
                        s_ex += _s_ex
                        c += _c
                        o += _o
                        s += _s
                        if _rf:
                            review_mods.add(f"{_zipfile}")
            Ts4ScriptFiles.log(output, f"Done")
        except Exception as e:
            Ts4ScriptFiles.log(output, f"*Error '{e}''.")

        log.debug(f"EVAL: {c_ev}, {o_ev}, {s_ev}; EXEC: {c_ex}, {o_ex}, {s_ex}; OTHER: {c}, {o}, {s}; (exact/very close match, string match, match in Privacy Protector)")
        Ts4ScriptFiles.possible_issues = c_ev + c_ex + c
        suspend_progress = False
        e_val = 'EVAL()'.lower()
        e_xec = 'EXEC()'.lower()
        if o_ev > 0:
            Ts4ScriptFiles.log(output, f"**** Found {o_ev} {e_val} string matches. These are usually OK and should be reviewed.")
        if o_ex > 0:
            Ts4ScriptFiles.log(output, f"**** Found {o_ex} {e_xec} string matches. These are usually OK and should be reviewed.")
        if o > 0:
            Ts4ScriptFiles.log(output, f"**** Found {o} string matches. These are usually OK and should be reviewed.")
        expected_self_matches = 100
        expected_self_e_vals = 1
        expected_self_e_xecs = 2
        if s > expected_self_matches or s_ev != expected_self_e_vals or s_ex != expected_self_e_xecs:
            Ts4ScriptFiles.log(output, f"!!!! Found {s} (expected <{expected_self_matches}) critical, {s_ev} (expected{expected_self_e_vals}) {e_val} and {s_ex} (expected{expected_self_e_xecs}) {e_xec} expected statements in Privacy Protector!")
            Ts4ScriptFiles.log(output, f"**** This shouldn't happen!")
        if c_ev > 0:
            suspend_progress = True
            Ts4ScriptFiles.log(output, f"!!!! Found {c_ev} {e_val} statements. Delete the offending mods and restart!")
        if c_ex > 0:
            suspend_progress = True
            Ts4ScriptFiles.log(output, f"!!!! Found {c_ex} {e_xec} statements. Delete the offending mods and restart!")
        if c > 0:
            Ts4ScriptFiles.log(output, f"!!!! Found {c} critical statements (exact or very close match). Review the offending mods and restart!")
        Ts4ScriptFiles.log(output, f"**** Summary of files with critical issues: {review_mods}")
        if suspend_progress:
            for i in sorted(range(1, 31), reverse=True):
                Ts4ScriptFiles.log(output, f"!!!! Delete the offending mods with {e_val} and/or {e_xec} or review these mods three times before adding them as exceptions and restart!")
                Ts4ScriptFiles.log(output, f"!!!! Loading will continue in {i} minutes!")
                time.sleep(60)

    @staticmethod
    def check_content(output, search_string, data, zipfile, file) -> Tuple[int, int, int, int, int, int, int, int, int, bool]:
        found_critical_e_val = 0
        found_something_e_val = 0
        found_self_e_val = 0
        found_critical_e_xec = 0
        found_something_e_xec = 0
        found_self_e_xec = 0
        found_critical = 0
        found_something = 0
        found_self = 0
        review_file: bool = False
        e_val = '.EVAL'.lower()
        e_xec = '.EXEC'.lower()

        if search_string:
            ss = [search_string, ]
        else:
            ss = [
                  'asyncio.create_subprocess_shell', 'asyncio.get_event_loop_policy', 'asyncio.create_subprocess_exec',
                  '.__builtins__',
                  # Py 2.x
                  # 'commands.getoutput',
                  e_val, e_xec,
                  # Py 2.x
                  # '.execfile',
                  '.importlib', 'imp.load_source',
                  'ftplib.FTP',
                  'os.startfile', 'os.execl', 'os.execve', 'os.spawnv', 'os.spawnve', 'os.system', 'os.popen',
                  'pip.main',
                  'pty.spawn',
                  'socket.socket', 'socket.socketpair', 'socket.fromfd', 'socket.fromshare', 'socket.create_connection',
                  'subprocess.run', 'subprocess.Popen', 'subprocess.call', 'subprocess.check_call', 'subprocess.check_output', 'subprocess.getoutput', 'subprocess.getstatusoutput',
                  'sys.modules',
                  '.timeit',
                  'urllib.request.urlopen', 'urllib.request.Request', 'urllib.request.FancyURLopener', 'urllib.request.OpenerDirector', 'urllib.request.AbstractHTTPHandler', 'urllib.request.BaseHandler', 'urllib.request.ProxyHandler',
                  'urllib.request.HTTPHandler', 'urllib.request.FileHandler', 'urllib.request.FTPHandler', 'urllib.request.CacheFTPHandler', 'urllib.request.URLopener', 'urllib.request.ftpwrapper',
                  'webbrowser.open',
                  ]
        for s in ss:
            _found_critical, _found_something, _found_self = Ts4ScriptFiles._check_content(output, s, data, zipfile, file)
            if s == e_val:
                found_critical_e_val += _found_critical
                found_something_e_val += _found_something
                found_self_e_val += _found_self
            elif s == e_xec:
                found_critical_e_xec += _found_critical
                found_something_e_xec += _found_something
                found_self_e_xec += _found_self
            else:
                found_critical += _found_critical
                found_something += _found_something
                found_self += _found_self
            if _found_critical or _found_self:
                review_file = True

        return found_critical_e_val, found_something_e_val, found_self_e_val, found_critical_e_xec, found_something_e_xec, found_self_e_xec, found_critical, found_something, found_self, review_file

    @staticmethod
    def _check_content(output, s, data, zipfile, file) -> Tuple[int, int, int]:
        found_critical = 0
        found_something = 0
        found_self = 0
        try:
            search_string = s.rsplit(".", 1)[-1]  # 'open' for 'a.os.popen'
            class_string = s.rsplit(".", 1)[-2]  # 'a.os' for 'a.os.popen'
            if search_string in f"{data}":
                if zipfile == f"{os.sep}{os.path.join('_o19_', 'privacy_protector.ts4script')}":
                    prefix = "Self."
                    found_self = 1
                elif zipfile == f"{os.sep}{os.path.join('_o19_', 'Scripts', 'privacy_protector', 'scan_ts4script.py')}" or \
                        zipfile == f"{os.sep}{os.path.join('_o19_', 'Scripts', 'privacy_protector', 'injections.py')}":
                    prefix = "!! Self (.py)."
                    found_self = 1
                elif class_string and class_string not in f"{data}":
                    # elif class_string and re.findall("[^g-z_]" + f"{class_string}" + "[^A-Za-z0-9_.]", f"{data}"):
                    prefix = f"Seems OK ({class_string} not found)."
                    found_something = 1
                else:
                    r = '[^g-z_]' + f"{search_string}" + '[^A-Za-z0-9_.]'
                    if re.findall(r, f'{data}') or f"@{search_string}" in f'{data}':
                        prefix = "!!"
                        # Ts4ScriptFiles.tmp_issues.append(f"'{search_string}' in '{zipfile}({file})'")
                        found_critical = 1
                    else:
                        prefix = "Seems OK (part of string)."
                        found_something = 1
                r = '.{1,20}' + f"{search_string}" + '.{1,20}'
                Ts4ScriptFiles.log(output, f"{prefix} Found '{search_string}' in '{zipfile}({file})': {re.findall(r, f'{data}')}")
        except Exception as e:
            Ts4ScriptFiles.log(output, f"Error '{e}' occurred while checking '{zipfile}'.")

        return found_critical, found_something, found_self

    @staticmethod
    def log(output, message):
        if output and (message[0] == "!" or message[0] == "*"):
            output(message)
        try:
            if message[0] == "!":
                log.warn(message)
            else:
                log.info(message)
        except:
            pass

    @staticmethod
    def get_files(directory: str) -> List[List[str]]:
        """
        List all files with path within a directory.
        :param directory: Directory to be rad
        :return: List with paths and files
        """
        rv = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith("ts4script") or file.endswith("zip") or file.endswith("py") or file.endswith("pyc"):
                    if file in Ts4ScriptFiles.allow_list:
                        Ts4ScriptFiles.log(None, f"*Skipping {file} in allow list.")
                    else:
                        rv.append([root, file])
        return rv


Scanner()
