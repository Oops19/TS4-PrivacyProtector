#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2022 https://github.com/Oops19
#


import sims4.commands
import sims4
from privacy_protector.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput


@CommonConsoleCommand(ModInfo.get_identity(), 'o19.prot', 'Whatever !')
def o19_debug_prot_help(output: CommonConsoleCommandOutput):
    output("o19.prot.browser - start a tab/browser with 'https://ea.com/'")
    output("o19.prot.shell n - start a shell, n=[aos]")
    output("o19.prot.socket - open a 'socket' connection")
    output("o19.prot.urllib - open a 'urllib' connection")


@CommonConsoleCommand(ModInfo.get_identity(), 'o19.prot.browser', 'Whatever !')
def o19_debug_prot_socket2(output: CommonConsoleCommandOutput):
    try:
        import webbrowser
        webbrowser.open('https://ea.com/')
        output(f"Opened 'https://ea.com/' in a new browser.")
    except Exception as e:
        output(f"Error '{e}''.")


@CommonConsoleCommand(ModInfo.get_identity(), 'o19.prot.socket', 'Whatever !')
def o19_debug_prot_socket(output: CommonConsoleCommandOutput):
    try:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.sendall( 'GET / HTTP/1.9\r\nHost: ea.com\r\n\r\n'.encode('utf-8') )
            s.close()
        output(f"Send request with 'socket.socket().sendall()'")
    except Exception as e:
        output(f"Error '{e}''.")


@CommonConsoleCommand(ModInfo.get_identity(), 'o19.prot.urllib', 'Whatever !')
def o19_debug_prot_urllib(output: CommonConsoleCommandOutput):
    try:
        import urllib.request
        with urllib.request.urlopen('http://ea.com/') as response:
            output(f"Read '{response.read()}' bytes with 'urllib.request.urlopen()'.")
    except Exception as e:
        output(f"Error '{e}''.")


@CommonConsoleCommand(ModInfo.get_identity(), 'o19.prot.shell', 'Whatever !')
def o19_debug_prot_shell(output: CommonConsoleCommandOutput, variant=None):
    try:
        import os
        if os.name == 'nt':
            command = 'powershell'
        else:
            command = 'bash'
        if variant == "a":  # asyncio
            output('asyncio.create_subprocess_shell()')
            import asyncio
            asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
            output(f"{command}' executed.")
        elif variant == "o":  # os
            output('os.system()')
            os.system(command)
            output(f"Started '{command}' as a new process.")
        elif variant == "s":  # subprocess
            output('subprocess.call()')
            import subprocess
            subprocess.call(command)
            output(f"Started '{command}' as a new process in the background.")
        else:
            output('Valid options:\na = asyncio (n/a)\no = os (foreground)\ns = subprocess (background)')
    except Exception as e:
        output(f"Error '{e}''.")
