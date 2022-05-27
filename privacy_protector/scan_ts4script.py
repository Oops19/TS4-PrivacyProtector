#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2022 https://github.com/Oops19
#


import os
import re

from zipfile import ZipFile
import time
import threading

import services
import sims4
import sims4.commands
from privacy_protector.modinfo import MTSModInfo
from ui.ui_dialog_notification import UiDialogNotification

from privacy_protector.privacy_protector import PrivacyProtector
from privacy_protector.s4cl.mts_common_log_registry import MTSCommonLog


log = MTSCommonLog(MTSModInfo.mod_name)
log.debug(f"Scanner ...")


@sims4.commands.Command('privacy.search', command_type=sims4.commands.CommandType.Live)
def o19_debug_privacy_search(search_string: str = '', _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    Ts4ScriptFiles.scan_files(output, search_string)


@sims4.commands.Command('privacy.scan', command_type=sims4.commands.CommandType.Live)
def o19_debug_privacy_scan(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    Ts4ScriptFiles.scan_files(output, None)


class Scanner:
    thread = None

    def __init__(self):
        Scanner.start_thread()

    @staticmethod
    def start_thread():
        Ts4ScriptFiles.allow_list = []
        mods_path = os.path.join(os.path.dirname(os.path.realpath(__file__)).partition(f"{os.sep}Mods{os.sep}")[0], 'mod_data', 'privacy_protector', 'skip_mods')
        file_list = Ts4ScriptFiles.get_files(mods_path)
        for files in file_list:
            Ts4ScriptFiles.allow_list.append(files[1])
        log.debug(f"Skipping {Ts4ScriptFiles.allow_list}")

        if Scanner.thread:
            return
        Scanner.thread = threading.Thread(target=Scanner._thread, args=())
        Scanner.thread.daemon = True
        Scanner.thread.start()

    def _thread(*args, **kwargs):
        time.sleep(60)
        Ts4ScriptFiles.scan_files(None, None)

        n = len(Ts4ScriptFiles.possible_issues)
        if n == 0:
            message = f"Found no issues."
            urgency = UiDialogNotification.UiDialogNotificationUrgency.DEFAULT
        else:
            urgency = UiDialogNotification.UiDialogNotificationUrgency.URGENT
            if n == 1:
                message = f"Found {n} possible issue."
            else:
                message = f"*Found {n} possible issues."
        PrivacyProtector.show_notification(message, urgency=urgency)
        log.debug(f"Scanner: Initial scan completed")


class Ts4ScriptFiles:
    allow_list = []
    possible_issues = []
    tmp_issues = []

    @staticmethod
    def scan_files(output, search_string):
        number_findings = 0
        Ts4ScriptFiles.tmp_issues = []
        try:
            mods_path = os.path.join(os.path.dirname(os.path.realpath(__file__)).partition(f"{os.sep}Mods{os.sep}")[0], 'Mods')
            file_list = Ts4ScriptFiles.get_files(mods_path)
            Ts4ScriptFiles.log(output, f"\n######################################\n")
            Ts4ScriptFiles.log(output, f"*Scanning '{len(file_list)}' files in '{mods_path}'")
            for files in file_list:
                zipfile = os.path.join(files[0], files[1])
                Ts4ScriptFiles.log(output, f"*Scanning '{zipfile.replace(mods_path, '')}")
                if files[1].endswith('ts4script') or files[1].endswith('zip'):
                    with ZipFile(zipfile, mode="r") as zf:
                        for file in zf.namelist():
                            with zf.open(file) as f:
                                data = f.read()
                                _findings = Ts4ScriptFiles.check_content(output, search_string, data, zipfile.replace(mods_path, ''), file)
                                number_findings += _findings
                else:
                    # py or pyc
                    with open(zipfile, mode="rb") as f:
                        data = f.read()
                        file = ''
                        _findings = Ts4ScriptFiles.check_content(output, search_string, data, zipfile.replace(mods_path, ''), file)
                        number_findings += _findings
                time.sleep(0.5)
            Ts4ScriptFiles.log(output, f"Done")
        except Exception as e:
            Ts4ScriptFiles.log(output, f"*Error '{e}''.")

        Ts4ScriptFiles.possible_issues = Ts4ScriptFiles.tmp_issues
        if number_findings == 0:
            Ts4ScriptFiles.log(output, f"*Found no issues.")
        elif number_findings == 1:
            Ts4ScriptFiles.log(output, f"*Found {number_findings} possible issue.")
        else:
            Ts4ScriptFiles.log(output, f"*Found {number_findings} possible issues.")

    @staticmethod
    def check_content(output, search_string, data, zipfile, file) -> int:
        n = 0
        if search_string:
            if Ts4ScriptFiles._check_content(output, f".{search_string}", data, zipfile, file):
                n += 1
        if not search_string:
            for s in ['.eval', '.exec', 'ftplib.FTP', 'webbrowser.open', 'os.startfile', 'os.execl', 'os.execve', 'os.spawnv', 'os.spawnve', 'os.system', 'os.popen', 'socket.socket', 'socket.socketpair', 'socket.fromfd', 'socket.fromshare', 'socket.create_connection', 'subprocess.run',
                      'subprocess.Popen', 'subprocess.call', 'subprocess.check_call', 'subprocess.check_output', 'subprocess.getoutput', 'subprocess.getstatusoutput', 'asyncio.create_subprocess_shell', 'asyncio.get_event_loop_policy', 'asyncio.create_subprocess_exec', 'urllib.request.urlopen',
                      'urllib.request.Request', 'urllib.request.FancyURLopener', 'urllib.request.OpenerDirector', 'urllib.request.AbstractHTTPHandler', 'urllib.request.BaseHandler', 'urllib.request.ProxyHandler', 'urllib.request.HTTPHandler', 'urllib.request.FileHandler',
                      'urllib.request.FTPHandler', 'urllib.request.CacheFTPHandler', 'urllib.request.URLopener', 'urllib.request.ftpwrapper']:
                # search_string = s.rsplit(".", 1)[1]
                if Ts4ScriptFiles._check_content(output, s, data, zipfile, file):
                    n += 1
        return n

    @staticmethod
    def _check_content(output, s, data, zipfile, file) -> bool:
        rv = False
        try:
            search_string = s.rsplit(".", 1)[-1]  # 'open' for '(a.os).popen'
            class_string = s.rsplit(".", 1)[-2]  # 'os' for (a.)os.popen'
            if search_string in f"{data}":
                data2 = f"{data}".replace("\n", " ").replace("\r", " ").replace("\t", "   ").replace("literal_eval", "eval_literal")  # Dirty hack for safe eval()
                if zipfile == f"{os.sep}{os.path.join('_o19_', 'privacy_protector.ts4script')}":
                    prefix = "Self."
                elif class_string and class_string not in f"{data}":
                    prefix = f"Seems OK ({class_string} not found)."
                else:
                    r = '[^g-z_]' + f"{search_string}" + '[^A-Za-z0-9_.]'
                    if re.findall(r, f'{data}'):
                        prefix = "!!"
                        Ts4ScriptFiles.tmp_issues.append(f"'{search_string}' in '{zipfile}({file})'")
                        rv = True
                    else:
                        prefix = "Seems OK (part of string)."
                r = '.{1,20}' + f"{search_string}" + '.{1,20}'
                Ts4ScriptFiles.log(output, f"{prefix} Found '{search_string}' in '{zipfile}({file})': {re.findall(r, f'{data}')}")
        except Exception as e:
            Ts4ScriptFiles.log(output, f"Error '{e}' occurred while checking '{zipfile}'.")
        return rv

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
    def get_files(directory: str) -> []:
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
