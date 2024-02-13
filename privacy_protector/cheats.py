#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


import sims4
import sims4.commands
from privacy_protector.scan_ts4script import Ts4ScriptFiles


@sims4.commands.Command('privacy.search', command_type=sims4.commands.CommandType.Live)
def o19_debug_privacy_search(search_string: str = '', _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    Ts4ScriptFiles.scan_files(output, search_string)


@sims4.commands.Command('privacy.scan', command_type=sims4.commands.CommandType.Live)
def o19_debug_privacy_scan(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    Ts4ScriptFiles.scan_files(output, None)
