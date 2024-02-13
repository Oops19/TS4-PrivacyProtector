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
    output("o19.priv.shell n - start a shell, n=[a|o|s]")
    output("o19.priv.socket - open a 'socket' connection to ea.com")
    output("o19.priv.urllib - open a 'urllib' connection to ea.com")

    output("o19.priv.scan EVAL - scan mods for 'EVAL()'".lower())
    output("o19.priv.scan EXEC - scan mods for 'EXEC()'".lower())
    output("o19.priv.scan foobar - scan mods for 'foobar()' or any other string or method used.")


@sims4.commands.Command('o19.priv.test', command_type=sims4.commands.CommandType.Live)
def o19_debug_priv_browser(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    try:
        from os import system as ss
        ss('dir')
        output(f"Executed 'dir")
    except Exception as e:
        output(f"Error '{e}''.")


@sims4.commands.Command('o19.priv.browser', command_type=sims4.commands.CommandType.Live)
def o19_debug_priv_browser(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    try:
        import webbrowser as wb
        wb.open('https://www.ea.com/de-de/games/the-sims/the-sims-4')
        output(f"Opened 'https://www.ea.com/de-de/games/the-sims/the-sims-4' in a new browser.")
    except Exception as e:
        output(f"Error '{e}''.")


@sims4.commands.Command('o19.priv.socket', command_type=sims4.commands.CommandType.Live)
def o19_debug_priv_socket(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    try:
        import socket as so
        with so.socket(so.AF_INET, so.SOCK_STREAM) as s:
            s.sendall('GET / HTTP/1.9\r\nHost: ea.com\r\n\r\n'.encode('utf-8') )
            s.close()
        output(f"Sent request with 'socket.socket().sendall()'")
    except Exception as e:
        output(f"Error '{e}''.")


@sims4.commands.Command('o19.priv.urllib', command_type=sims4.commands.CommandType.Live)
def o19_debug_priv_urllib(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    try:
        import urllib.request as u
        with u.request.urlopen('http://ea.com/') as response:
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
            output(f"{command}' EXECuted.".lower())
        elif variant == "o":  # os
            output('os.system()')
            from os import system as mostly_harmless
            mostly_harmless(command)  # os.system(command)
            output(f"Started '{command}' as a new process.")
        elif variant == "s":  # subprocess
            output('subprocess.call()')
            from subprocess import call as mostly_harmless
            mostly_harmless(command)  # subprocess.call(command)
            output(f"Started '{command}' as a new process in the background.")
        else:
            output('Valid options:\na = asyncio (n/a)\no = os (foreground)\ns = subprocess (background)')
    except Exception as e:
        output(f"Error '{e}''.")
