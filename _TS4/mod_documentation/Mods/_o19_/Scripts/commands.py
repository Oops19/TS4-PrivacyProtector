#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2022 https://github.com/Oops19
#


import sims4.commands
import sims4


@sims4.commands.Command('o19.priv', command_type=sims4.commands.CommandType.Live)
def o19_debug_priv_help(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output("o19.priv.browser - start a tab/browser with 'https://ea.com/'")
    output("o19.priv.shell n - start a shell, n=[aos]")
    output("o19.priv.socket - open a 'socket' connection to ea.com")
    output("o19.priv.urllib - open a 'urllib' connection to ea.com")


@sims4.commands.Command('o19.priv.browser', command_type=sims4.commands.CommandType.Live)
def o19_debug_priv_browser(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    try:
        import webbrowser
        webbrowser.open('https://www.ea.com/de-de/games/the-sims/the-sims-4')
        output(f"Opened 'https://www.ea.com/de-de/games/the-sims/the-sims-4' in a new browser.")
    except Exception as e:
        output(f"Error '{e}''.")


@sims4.commands.Command('o19.priv.socket', command_type=sims4.commands.CommandType.Live)
def o19_debug_priv_socket(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    try:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.sendall('GET / HTTP/1.9\r\nHost: ea.com\r\n\r\n'.encode('utf-8') )
            s.close()
        output(f"Sent request with 'socket.socket().sendall()'")
    except Exception as e:
        output(f"Error '{e}''.")


@sims4.commands.Command('o19.priv.urllib', command_type=sims4.commands.CommandType.Live)
def o19_debug_priv_urllib(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    try:
        import urllib.request
        with urllib.request.urlopen('http://ea.com/') as response:
            output(f"Read '{response.read()}' bytes with 'urllib.request.urlopen()'.")
    except Exception as e:
        output(f"Error '{e}''.")


@sims4.commands.Command('o19.priv.shell', command_type=sims4.commands.CommandType.Live)
def o19_debug_priv_shell(variant=None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
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

