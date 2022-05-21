#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2022 https://github.com/Oops19
#


import os
import re

import sims4.commands
import sims4
from zipfile import ZipFile


@sims4.commands.Command('o19.priv.scan', command_type=sims4.commands.CommandType.Live)
def o19_debug_zip(search_string: str = '', _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    number_findings = 0
    try:
        if search_string == '':
            output("Usage: o19.priv.scan [eval|exec] - or specify another string.")
            return
        mods_path = os.path.join(os.path.dirname(os.path.realpath(__file__)).partition(f"{os.sep}Mods{os.sep}")[0], 'Mods')
        file_list = Ts4ScriptFiles.get_files(mods_path)
        output(f"\n######################################\n")
        Ts4ScriptFiles.log(output, f"Scanning '{len(file_list)}' files in '{mods_path}'")
        for files in file_list:
            zipfile = os.path.join(files[0], files[1])
            if files[1].endswith('ts4script') or files[1].endswith('zip'):
                with ZipFile(zipfile, mode = "r") as zf:
                    for file in zf.namelist():
                        with zf.open(file) as f:
                            data = f.read()
                            if Ts4ScriptFiles.check_content(output, search_string, data, zipfile.replace(mods_path, ''), file):
                                number_findings += 1
            else:
                # py or pyc
                with open(zipfile, mode="rb") as f:
                    data = f.read()
                    file = ''
                    if Ts4ScriptFiles.check_content(output, search_string, data, zipfile.replace(mods_path, ''), file):
                        number_findings += 1
        output(f"Done")
    except Exception as e:
        Ts4ScriptFiles.log(output, f"Error '{e}''.")
    Ts4ScriptFiles.log(output, f"Found '{search_string}' {number_findings} times.")


class Ts4ScriptFiles:
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
                    rv.append([root, file])
        return rv

    @staticmethod
    def check_content(output, search_string, data, zipfile, file) -> bool:
        rv = False
        try:
            if search_string in f"{data}":
                data2 = f"{data}".replace("\n", " ").replace("\r", " ").replace("\t", "   ").replace("literal_eval", "eval_literal")
                if f"{search_string}\\" in f"{data2}" or f"{search_string}(" in f"{data2}" or f"{search_string} " in f"{data2}" or f"{search_string}\t" in f"{data2}":
                    prefix = "!!"
                    rv = True
                else:
                    prefix = "Seems OK."
                r = '.{1,20}' + f"{search_string}" + '.{1,20}'
                Ts4ScriptFiles.log(output, f"{prefix} Found {search_string} in {zipfile}({file}): {re.findall(r, f'{data}')}")
        except Exception as e:
            Ts4ScriptFiles.log(output, f"Error '{e}' occurred while checking '{zipfile}'.")
        return rv

    @staticmethod
    def log(output, message):
        output(message)
        try:
            from privacy_protector.modinfo import ModInfo
            from sims4communitylib.utils.common_log_registry import CommonLog
            from sims4communitylib.utils.common_log_registry import CommonLogRegistry
            log: CommonLog = CommonLogRegistry.get().register_log(f"{ModInfo.get_identity().name}", ModInfo.get_identity().name)
            log.enable()
            if message[0] == "!":
                log.warn(message)
            else:
                log.info(message)
        except:
            pass