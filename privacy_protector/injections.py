#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2022 https://github.com/Oops19
#


import sys
import threading
import traceback

from privacy_protector.modinfo import S4CLModInfo
from privacy_protector.privacy_protector import PrivacyProtector
from privacy_protector.s4cl.s4cl_common_injection_utils import S4CLCommonInjectionUtils
from privacy_protector.s4cl.s4cl_common_log_registry import S4CLCommonLog

log = S4CLCommonLog(S4CLModInfo.mod_name)
log.debug("Injections ...")


class PrivacyViolationException(Exception):
    pass


class O19Injections:
    @staticmethod
    def log_data(_method: str, *args, **kwargs):
        try:
            log_message = f"'{_method}({args}; {kwargs})' called from:\n"
            for thread in threading.enumerate():
                thread_details = traceback.extract_stack(sys._current_frames()[thread.ident])
                for thread_detail in thread_details:
                    (filename, number, function, line_text) = thread_detail
                    log_message = f"{log_message}    {filename}#{number} '{line_text}' in '{function}()'\n"
            log.warn(log_message)
        except Exception as e:
            log.error(f"Error in 'log_data': '{e}'")

        if _method in ['eval', 'exec']:
            return
        try:
            notify_message = f"Privacy violated.\r\nSee 'The Sims 4/mod_logs/{S4CLModInfo.mod_name}.txt' for more details."
            PrivacyProtector.show_notification(f"{notify_message}\n{_method}(...)")
        except Exception as e:
            log.error(f"Error in show_notification({e})")

        raise PrivacyViolationException("Blocking privacy violation!")


try:
    import imp
    from imp import load_source
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), load_source, load_source.__init__.__name__, handle_exceptions=False)
    def o19_injected_imp_load_source(original, self, *args, **kwargs):
        O19Injections.log_data('imp.load_source', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into imp.load_source()")
except Exception as e1:
    try:
        o19_org_imp_load_source = imp.load_source
        
        def o19_override_imp_load_source(*args, **kwargs):
            O19Injections.log_data('imp.load_source', *args, **kwargs)
            return o19_org_imp_load_source(*args, **kwargs)
        imp.load_source = o19_override_imp_load_source
        log.debug("Replaced imp.load_source()")
    except Exception as e2:
        log.warn(f"'imp.load_source()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import ftplib
    from ftplib import FTP
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), FTP, FTP.__init__.__name__, handle_exceptions=False)
    def o19_injected_ftplib_ftp(original, self, *args, **kwargs):
        O19Injections.log_data('ftplib.FTP', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into ftplib.FTP()")
except Exception as e1:
    try:
        o19_org_ftplib_ftp = ftplib.FTP
        
        def o19_override_ftplib_ftp(*args, **kwargs):
            O19Injections.log_data('ftplib.FTP', *args, **kwargs)
            return o19_org_ftplib_ftp(*args, **kwargs)
        ftplib.FTP = o19_override_ftplib_ftp
        log.debug("Replaced ftplib.FTP()")
    except Exception as e2:
        log.warn(f"'ftplib.FTP()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import os
    from os import startfile
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), startfile, startfile.__init__.__name__, handle_exceptions=False)
    def o19_injected_os_startfile(original, self, *args, **kwargs):
        O19Injections.log_data('os.startfile', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into os.startfile()")
except Exception as e1:
    try:
        o19_org_os_startfile = os.startfile
        
        def o19_override_os_startfile(*args, **kwargs):
            O19Injections.log_data('os.startfile', *args, **kwargs)
            return o19_org_os_startfile(*args, **kwargs)
        os.startfile = o19_override_os_startfile
        log.debug("Replaced os.startfile()")
    except Exception as e2:
        log.warn(f"'os.startfile()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import os
    from os import execl
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), execl, execl.__init__.__name__, handle_exceptions=False)
    def o19_injected_os_execl(original, self, *args, **kwargs):
        O19Injections.log_data('os.execl', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into os.execl()")
except Exception as e1:
    try:
        o19_org_os_execl = os.execl
        
        def o19_override_os_execl(*args, **kwargs):
            O19Injections.log_data('os.execl', *args, **kwargs)
            return o19_org_os_execl(*args, **kwargs)
        os.execl = o19_override_os_execl
        log.debug("Replaced os.execl()")
    except Exception as e2:
        log.warn(f"'os.execl()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import os
    from os import execve
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), execve, execve.__init__.__name__, handle_exceptions=False)
    def o19_injected_os_execve(original, self, *args, **kwargs):
        O19Injections.log_data('os.execve', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into os.execve()")
except Exception as e1:
    try:
        o19_org_os_execve = os.execve
        
        def o19_override_os_execve(*args, **kwargs):
            O19Injections.log_data('os.execve', *args, **kwargs)
            return o19_org_os_execve(*args, **kwargs)
        os.execve = o19_override_os_execve
        log.debug("Replaced os.execve()")
    except Exception as e2:
        log.warn(f"'os.execve()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import os
    from os import spawnv
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), spawnv, spawnv.__init__.__name__, handle_exceptions=False)
    def o19_injected_os_spawnv(original, self, *args, **kwargs):
        O19Injections.log_data('os.spawnv', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into os.spawnv()")
except Exception as e1:
    try:
        o19_org_os_spawnv = os.spawnv
        
        def o19_override_os_spawnv(*args, **kwargs):
            O19Injections.log_data('os.spawnv', *args, **kwargs)
            return o19_org_os_spawnv(*args, **kwargs)
        os.spawnv = o19_override_os_spawnv
        log.debug("Replaced os.spawnv()")
    except Exception as e2:
        log.warn(f"'os.spawnv()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import os
    from os import spawnve
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), spawnve, spawnve.__init__.__name__, handle_exceptions=False)
    def o19_injected_os_spawnve(original, self, *args, **kwargs):
        O19Injections.log_data('os.spawnve', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into os.spawnve()")
except Exception as e1:
    try:
        o19_org_os_spawnve = os.spawnve
        
        def o19_override_os_spawnve(*args, **kwargs):
            O19Injections.log_data('os.spawnve', *args, **kwargs)
            return o19_org_os_spawnve(*args, **kwargs)
        os.spawnve = o19_override_os_spawnve
        log.debug("Replaced os.spawnve()")
    except Exception as e2:
        log.warn(f"'os.spawnve()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import os
    from os import system
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), system, system.__init__.__name__, handle_exceptions=False)
    def o19_injected_os_system(original, self, *args, **kwargs):
        O19Injections.log_data('os.system', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into os.system()")
except Exception as e1:
    try:
        o19_org_os_system = os.system
        
        def o19_override_os_system(*args, **kwargs):
            O19Injections.log_data('os.system', *args, **kwargs)
            return o19_org_os_system(*args, **kwargs)
        os.system = o19_override_os_system
        log.debug("Replaced os.system()")
    except Exception as e2:
        log.warn(f"'os.system()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import os
    from os import popen
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), popen, popen.__init__.__name__, handle_exceptions=False)
    def o19_injected_os_popen(original, self, *args, **kwargs):
        O19Injections.log_data('os.popen', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into os.popen()")
except Exception as e1:
    try:
        o19_org_os_popen = os.popen
        
        def o19_override_os_popen(*args, **kwargs):
            O19Injections.log_data('os.popen', *args, **kwargs)
            return o19_org_os_popen(*args, **kwargs)
        os.popen = o19_override_os_popen
        log.debug("Replaced os.popen()")
    except Exception as e2:
        log.warn(f"'os.popen()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import socket
    from socket import socket
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), socket, socket.__init__.__name__, handle_exceptions=False)
    def o19_injected_socket_socket(original, self, *args, **kwargs):
        O19Injections.log_data('socket.socket', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into socket.socket()")
except Exception as e1:
    try:
        o19_org_socket_socket = socket.socket
        
        def o19_override_socket_socket(*args, **kwargs):
            O19Injections.log_data('socket.socket', *args, **kwargs)
            return o19_org_socket_socket(*args, **kwargs)
        socket.socket = o19_override_socket_socket
        log.debug("Replaced socket.socket()")
    except Exception as e2:
        log.warn(f"'socket.socket()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import socket
    from socket import socketpair
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), socketpair, socketpair.__init__.__name__, handle_exceptions=False)
    def o19_injected_socket_socketpair(original, self, *args, **kwargs):
        O19Injections.log_data('socket.socketpair', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into socket.socketpair()")
except Exception as e1:
    try:
        o19_org_socket_socketpair = socket.socketpair
        
        def o19_override_socket_socketpair(*args, **kwargs):
            O19Injections.log_data('socket.socketpair', *args, **kwargs)
            return o19_org_socket_socketpair(*args, **kwargs)
        socket.socketpair = o19_override_socket_socketpair
        log.debug("Replaced socket.socketpair()")
    except Exception as e2:
        log.warn(f"'socket.socketpair()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import socket
    from socket import fromfd
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), fromfd, fromfd.__init__.__name__, handle_exceptions=False)
    def o19_injected_socket_fromfd(original, self, *args, **kwargs):
        O19Injections.log_data('socket.fromfd', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into socket.fromfd()")
except Exception as e1:
    try:
        o19_org_socket_fromfd = socket.fromfd
        
        def o19_override_socket_fromfd(*args, **kwargs):
            O19Injections.log_data('socket.fromfd', *args, **kwargs)
            return o19_org_socket_fromfd(*args, **kwargs)
        socket.fromfd = o19_override_socket_fromfd
        log.debug("Replaced socket.fromfd()")
    except Exception as e2:
        log.warn(f"'socket.fromfd()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import socket
    from socket import fromshare
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), fromshare, fromshare.__init__.__name__, handle_exceptions=False)
    def o19_injected_socket_fromshare(original, self, *args, **kwargs):
        O19Injections.log_data('socket.fromshare', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into socket.fromshare()")
except Exception as e1:
    try:
        o19_org_socket_fromshare = socket.fromshare
        
        def o19_override_socket_fromshare(*args, **kwargs):
            O19Injections.log_data('socket.fromshare', *args, **kwargs)
            return o19_org_socket_fromshare(*args, **kwargs)
        socket.fromshare = o19_override_socket_fromshare
        log.debug("Replaced socket.fromshare()")
    except Exception as e2:
        log.warn(f"'socket.fromshare()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import socket
    from socket import create_connection
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), create_connection, create_connection.__init__.__name__, handle_exceptions=False)
    def o19_injected_socket_create_connection(original, self, *args, **kwargs):
        O19Injections.log_data('socket.create_connection', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into socket.create_connection()")
except Exception as e1:
    try:
        o19_org_socket_create_connection = socket.create_connection
        
        def o19_override_socket_create_connection(*args, **kwargs):
            O19Injections.log_data('socket.create_connection', *args, **kwargs)
            return o19_org_socket_create_connection(*args, **kwargs)
        socket.create_connection = o19_override_socket_create_connection
        log.debug("Replaced socket.create_connection()")
    except Exception as e2:
        log.warn(f"'socket.create_connection()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import subprocess
    from subprocess import run
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), run, run.__init__.__name__, handle_exceptions=False)
    def o19_injected_subprocess_run(original, self, *args, **kwargs):
        O19Injections.log_data('subprocess.run', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into subprocess.run()")
except Exception as e1:
    try:
        o19_org_subprocess_run = subprocess.run
        
        def o19_override_subprocess_run(*args, **kwargs):
            O19Injections.log_data('subprocess.run', *args, **kwargs)
            return o19_org_subprocess_run(*args, **kwargs)
        subprocess.run = o19_override_subprocess_run
        log.debug("Replaced subprocess.run()")
    except Exception as e2:
        log.warn(f"'subprocess.run()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import subprocess
    from subprocess import Popen
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), Popen, Popen.__init__.__name__, handle_exceptions=False)
    def o19_injected_subprocess_popen(original, self, *args, **kwargs):
        O19Injections.log_data('subprocess.Popen', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into subprocess.Popen()")
except Exception as e1:
    try:
        o19_org_subprocess_popen = subprocess.Popen
        
        def o19_override_subprocess_popen(*args, **kwargs):
            O19Injections.log_data('subprocess.Popen', *args, **kwargs)
            return o19_org_subprocess_popen(*args, **kwargs)
        subprocess.Popen = o19_override_subprocess_popen
        log.debug("Replaced subprocess.Popen()")
    except Exception as e2:
        log.warn(f"'subprocess.Popen()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import subprocess
    from subprocess import call
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), call, call.__init__.__name__, handle_exceptions=False)
    def o19_injected_subprocess_call(original, self, *args, **kwargs):
        O19Injections.log_data('subprocess.call', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into subprocess.call()")
except Exception as e1:
    try:
        o19_org_subprocess_call = subprocess.call
        
        def o19_override_subprocess_call(*args, **kwargs):
            O19Injections.log_data('subprocess.call', *args, **kwargs)
            return o19_org_subprocess_call(*args, **kwargs)
        subprocess.call = o19_override_subprocess_call
        log.debug("Replaced subprocess.call()")
    except Exception as e2:
        log.warn(f"'subprocess.call()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import subprocess
    from subprocess import check_call
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), check_call, check_call.__init__.__name__, handle_exceptions=False)
    def o19_injected_subprocess_check_call(original, self, *args, **kwargs):
        O19Injections.log_data('subprocess.check_call', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into subprocess.check_call()")
except Exception as e1:
    try:
        o19_org_subprocess_check_call = subprocess.check_call
        
        def o19_override_subprocess_check_call(*args, **kwargs):
            O19Injections.log_data('subprocess.check_call', *args, **kwargs)
            return o19_org_subprocess_check_call(*args, **kwargs)
        subprocess.check_call = o19_override_subprocess_check_call
        log.debug("Replaced subprocess.check_call()")
    except Exception as e2:
        log.warn(f"'subprocess.check_call()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import subprocess
    from subprocess import check_output
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), check_output, check_output.__init__.__name__, handle_exceptions=False)
    def o19_injected_subprocess_check_output(original, self, *args, **kwargs):
        O19Injections.log_data('subprocess.check_output', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into subprocess.check_output()")
except Exception as e1:
    try:
        o19_org_subprocess_check_output = subprocess.check_output
        
        def o19_override_subprocess_check_output(*args, **kwargs):
            O19Injections.log_data('subprocess.check_output', *args, **kwargs)
            return o19_org_subprocess_check_output(*args, **kwargs)
        subprocess.check_output = o19_override_subprocess_check_output
        log.debug("Replaced subprocess.check_output()")
    except Exception as e2:
        log.warn(f"'subprocess.check_output()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import subprocess
    from subprocess import getoutput
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), getoutput, getoutput.__init__.__name__, handle_exceptions=False)
    def o19_injected_subprocess_getoutput(original, self, *args, **kwargs):
        O19Injections.log_data('subprocess.getoutput', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into subprocess.getoutput()")
except Exception as e1:
    try:
        o19_org_subprocess_getoutput = subprocess.getoutput
        
        def o19_override_subprocess_getoutput(*args, **kwargs):
            O19Injections.log_data('subprocess.getoutput', *args, **kwargs)
            return o19_org_subprocess_getoutput(*args, **kwargs)
        subprocess.getoutput = o19_override_subprocess_getoutput
        log.debug("Replaced subprocess.getoutput()")
    except Exception as e2:
        log.warn(f"'subprocess.getoutput()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import subprocess
    from subprocess import getstatusoutput
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), getstatusoutput, getstatusoutput.__init__.__name__, handle_exceptions=False)
    def o19_injected_subprocess_getstatusoutput(original, self, *args, **kwargs):
        O19Injections.log_data('subprocess.getstatusoutput', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into subprocess.getstatusoutput()")
except Exception as e1:
    try:
        o19_org_subprocess_getstatusoutput = subprocess.getstatusoutput
        
        def o19_override_subprocess_getstatusoutput(*args, **kwargs):
            O19Injections.log_data('subprocess.getstatusoutput', *args, **kwargs)
            return o19_org_subprocess_getstatusoutput(*args, **kwargs)
        subprocess.getstatusoutput = o19_override_subprocess_getstatusoutput
        log.debug("Replaced subprocess.getstatusoutput()")
    except Exception as e2:
        log.warn(f"'subprocess.getstatusoutput()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import timeit
    from timeit import timeit
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), timeit, timeit.__init__.__name__, handle_exceptions=False)
    def o19_injected_timeit_timeit(original, self, *args, **kwargs):
        O19Injections.log_data('timeit.timeit', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into timeit.timeit()")
except Exception as e1:
    try:
        o19_org_timeit_timeit = timeit.timeit
        
        def o19_override_timeit_timeit(*args, **kwargs):
            O19Injections.log_data('timeit.timeit', *args, **kwargs)
            return o19_org_timeit_timeit(*args, **kwargs)
        timeit.timeit = o19_override_timeit_timeit
        log.debug("Replaced timeit.timeit()")
    except Exception as e2:
        log.warn(f"'timeit.timeit()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import urllib.request
    from urllib.request import urlopen
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), urlopen, urlopen.__init__.__name__, handle_exceptions=False)
    def o19_injected_urllib_request_urlopen(original, self, *args, **kwargs):
        O19Injections.log_data('urllib.request.urlopen', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into urllib.request.urlopen()")
except Exception as e1:
    try:
        o19_org_urllib_request_urlopen = urllib.request.urlopen
        
        def o19_override_urllib_request_urlopen(*args, **kwargs):
            O19Injections.log_data('urllib.request.urlopen', *args, **kwargs)
            return o19_org_urllib_request_urlopen(*args, **kwargs)
        urllib.request.urlopen = o19_override_urllib_request_urlopen
        log.debug("Replaced urllib.request.urlopen()")
    except Exception as e2:
        log.warn(f"'urllib.request.urlopen()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import urllib.request
    from urllib.request import Request
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), Request, Request.__init__.__name__, handle_exceptions=False)
    def o19_injected_urllib_request_request(original, self, *args, **kwargs):
        O19Injections.log_data('urllib.request.Request', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into urllib.request.Request()")
except Exception as e1:
    try:
        o19_org_urllib_request_request = urllib.request.Request
        
        def o19_override_urllib_request_request(*args, **kwargs):
            O19Injections.log_data('urllib.request.Request', *args, **kwargs)
            return o19_org_urllib_request_request(*args, **kwargs)
        urllib.request.Request = o19_override_urllib_request_request
        log.debug("Replaced urllib.request.Request()")
    except Exception as e2:
        log.warn(f"'urllib.request.Request()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import urllib.request
    from urllib.request import FancyURLopener
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), FancyURLopener, FancyURLopener.__init__.__name__, handle_exceptions=False)
    def o19_injected_urllib_request_fancyurlopener(original, self, *args, **kwargs):
        O19Injections.log_data('urllib.request.FancyURLopener', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into urllib.request.FancyURLopener()")
except Exception as e1:
    try:
        o19_org_urllib_request_fancyurlopener = urllib.request.FancyURLopener
        
        def o19_override_urllib_request_fancyurlopener(*args, **kwargs):
            O19Injections.log_data('urllib.request.FancyURLopener', *args, **kwargs)
            return o19_org_urllib_request_fancyurlopener(*args, **kwargs)
        urllib.request.FancyURLopener = o19_override_urllib_request_fancyurlopener
        log.debug("Replaced urllib.request.FancyURLopener()")
    except Exception as e2:
        log.warn(f"'urllib.request.FancyURLopener()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import urllib.request
    from urllib.request import OpenerDirector
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), OpenerDirector, OpenerDirector.__init__.__name__, handle_exceptions=False)
    def o19_injected_urllib_request_openerdirector(original, self, *args, **kwargs):
        O19Injections.log_data('urllib.request.OpenerDirector', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into urllib.request.OpenerDirector()")
except Exception as e1:
    try:
        o19_org_urllib_request_openerdirector = urllib.request.OpenerDirector
        
        def o19_override_urllib_request_openerdirector(*args, **kwargs):
            O19Injections.log_data('urllib.request.OpenerDirector', *args, **kwargs)
            return o19_org_urllib_request_openerdirector()
        urllib.request.OpenerDirector = o19_override_urllib_request_openerdirector
        log.debug("Replaced urllib.request.OpenerDirector()")
    except Exception as e2:
        log.warn(f"'urllib.request.OpenerDirector()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import urllib.request
    from urllib.request import AbstractHTTPHandler
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), AbstractHTTPHandler, AbstractHTTPHandler.__init__.__name__, handle_exceptions=False)
    def o19_injected_urllib_request_abstracthttphandler(original, self, *args, **kwargs):
        O19Injections.log_data('urllib.request.AbstractHTTPHandler', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into urllib.request.AbstractHTTPHandler()")
except Exception as e1:
    try:
        o19_org_urllib_request_abstracthttphandler = urllib.request.AbstractHTTPHandler
        
        def o19_override_urllib_request_abstracthttphandler(*args, **kwargs):
            O19Injections.log_data('urllib.request.AbstractHTTPHandler', *args, **kwargs)
            return o19_org_urllib_request_abstracthttphandler(*args, **kwargs)
        urllib.request.AbstractHTTPHandler = o19_override_urllib_request_abstracthttphandler
        log.debug("Replaced urllib.request.AbstractHTTPHandler()")
    except Exception as e2:
        log.warn(f"'urllib.request.AbstractHTTPHandler()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import urllib.request
    from urllib.request import BaseHandler
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), BaseHandler, BaseHandler.__init__.__name__, handle_exceptions=False)
    def o19_injected_urllib_request_basehandler(original, self, *args, **kwargs):
        O19Injections.log_data('urllib.request.BaseHandler', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into urllib.request.BaseHandler()")
except Exception as e1:
    try:
        o19_org_urllib_request_basehandler = urllib.request.BaseHandler
        
        def o19_override_urllib_request_basehandler(*args, **kwargs):
            O19Injections.log_data('urllib.request.BaseHandler', *args, **kwargs)
            return o19_org_urllib_request_basehandler()
        urllib.request.BaseHandler = o19_override_urllib_request_basehandler
        log.debug("Replaced urllib.request.BaseHandler()")
    except Exception as e2:
        log.warn(f"'urllib.request.BaseHandler()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import urllib.request
    from urllib.request import ProxyHandler
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), ProxyHandler, ProxyHandler.__init__.__name__, handle_exceptions=False)
    def o19_injected_urllib_request_proxyhandler(original, self, *args, **kwargs):
        O19Injections.log_data('urllib.request.ProxyHandler', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into urllib.request.ProxyHandler()")
except Exception as e1:
    try:
        o19_org_urllib_request_proxyhandler = urllib.request.ProxyHandler
        
        def o19_override_urllib_request_proxyhandler(*args, **kwargs):
            O19Injections.log_data('urllib.request.ProxyHandler', *args, **kwargs)
            return o19_org_urllib_request_proxyhandler(*args, **kwargs)
        urllib.request.ProxyHandler = o19_override_urllib_request_proxyhandler
        log.debug("Replaced urllib.request.ProxyHandler()")
    except Exception as e2:
        log.warn(f"'urllib.request.ProxyHandler()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import urllib.request
    from urllib.request import HTTPHandler
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), HTTPHandler, HTTPHandler.__init__.__name__, handle_exceptions=False)
    def o19_injected_urllib_request_httphandler(original, self, *args, **kwargs):
        O19Injections.log_data('urllib.request.HTTPHandler', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into urllib.request.HTTPHandler()")
except Exception as e1:
    try:
        o19_org_urllib_request_httphandler = urllib.request.HTTPHandler
        
        def o19_override_urllib_request_httphandler(*args, **kwargs):
            O19Injections.log_data('urllib.request.HTTPHandler', *args, **kwargs)
            return o19_org_urllib_request_httphandler(*args, **kwargs)
        urllib.request.HTTPHandler = o19_override_urllib_request_httphandler
        log.debug("Replaced urllib.request.HTTPHandler()")
    except Exception as e2:
        log.warn(f"'urllib.request.HTTPHandler()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import urllib.request
    from urllib.request import FileHandler
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), FileHandler, FileHandler.__init__.__name__, handle_exceptions=False)
    def o19_injected_urllib_request_filehandler(original, self, *args, **kwargs):
        O19Injections.log_data('urllib.request.FileHandler', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into urllib.request.FileHandler()")
except Exception as e1:
    try:
        o19_org_urllib_request_filehandler = urllib.request.FileHandler
        
        def o19_override_urllib_request_filehandler(*args, **kwargs):
            O19Injections.log_data('urllib.request.FileHandler', *args, **kwargs)
            return o19_org_urllib_request_filehandler()
        urllib.request.FileHandler = o19_override_urllib_request_filehandler
        log.debug("Replaced urllib.request.FileHandler()")
    except Exception as e2:
        log.warn(f"'urllib.request.FileHandler()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import urllib.request
    from urllib.request import FTPHandler
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), FTPHandler, FTPHandler.__init__.__name__, handle_exceptions=False)
    def o19_injected_urllib_request_ftphandler(original, self, *args, **kwargs):
        O19Injections.log_data('urllib.request.FTPHandler', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into urllib.request.FTPHandler()")
except Exception as e1:
    try:
        o19_org_urllib_request_ftphandler = urllib.request.FTPHandler
        
        def o19_override_urllib_request_ftphandler(*args, **kwargs):
            O19Injections.log_data('urllib.request.FTPHandler', *args, **kwargs)
            return o19_org_urllib_request_ftphandler()
        urllib.request.FTPHandler = o19_override_urllib_request_ftphandler
        log.debug("Replaced urllib.request.FTPHandler()")
    except Exception as e2:
        log.warn(f"'urllib.request.FTPHandler()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import urllib.request
    from urllib.request import CacheFTPHandler
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), CacheFTPHandler, CacheFTPHandler.__init__.__name__, handle_exceptions=False)
    def o19_injected_urllib_request_cacheftphandler(original, self, *args, **kwargs):
        O19Injections.log_data('urllib.request.CacheFTPHandler', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into urllib.request.CacheFTPHandler()")
except Exception as e1:
    try:
        o19_org_urllib_request_cacheftphandler = urllib.request.CacheFTPHandler
        
        def o19_override_urllib_request_cacheftphandler(*args, **kwargs):
            O19Injections.log_data('urllib.request.CacheFTPHandler', *args, **kwargs)
            return o19_org_urllib_request_cacheftphandler()
        urllib.request.CacheFTPHandler = o19_override_urllib_request_cacheftphandler
        log.debug("Replaced urllib.request.CacheFTPHandler()")
    except Exception as e2:
        log.warn(f"'urllib.request.CacheFTPHandler()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import urllib.request
    from urllib.request import URLopener
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), URLopener, URLopener.__init__.__name__, handle_exceptions=False)
    def o19_injected_urllib_request_urlopener(original, self, *args, **kwargs):
        O19Injections.log_data('urllib.request.URLopener', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into urllib.request.URLopener()")
except Exception as e1:
    try:
        o19_org_urllib_request_urlopener = urllib.request.URLopener
        
        def o19_override_urllib_request_urlopener(*args, **kwargs):
            O19Injections.log_data('urllib.request.URLopener', *args, **kwargs)
            return o19_org_urllib_request_urlopener(*args, **kwargs)
        urllib.request.URLopener = o19_override_urllib_request_urlopener
        log.debug("Replaced urllib.request.URLopener()")
    except Exception as e2:
        log.warn(f"'urllib.request.URLopener()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import urllib.request
    from urllib.request import ftpwrapper
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), ftpwrapper, ftpwrapper.__init__.__name__, handle_exceptions=False)
    def o19_injected_urllib_request_ftpwrapper(original, self, *args, **kwargs):
        O19Injections.log_data('urllib.request.ftpwrapper', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into urllib.request.ftpwrapper()")
except Exception as e1:
    try:
        o19_org_urllib_request_ftpwrapper = urllib.request.ftpwrapper
        
        def o19_override_urllib_request_ftpwrapper(*args, **kwargs):
            O19Injections.log_data('urllib.request.ftpwrapper', *args, **kwargs)
            return o19_org_urllib_request_ftpwrapper(*args, **kwargs)
        urllib.request.ftpwrapper = o19_override_urllib_request_ftpwrapper
        log.debug("Replaced urllib.request.ftpwrapper()")
    except Exception as e2:
        log.warn(f"'urllib.request.ftpwrapper()': Could not inject '{e1}' or replace '{e2}' ")


try:
    import webbrowser
    from webbrowser import open
    
    @S4CLCommonInjectionUtils.inject_safely_into(S4CLModInfo.get_identity(), open, open.__init__.__name__, handle_exceptions=False)
    def o19_injected_webbrowser_open(original, self, *args, **kwargs):
        O19Injections.log_data('webbrowser.open', *args, **kwargs)
        return original(self, *args, **kwargs)
    log.debug("Injected into webbrowser.open()")
except Exception as e1:
    try:
        o19_org_webbrowser_open = webbrowser.open
        
        def o19_override_webbrowser_open(*args, **kwargs):
            O19Injections.log_data('webbrowser.open', *args, **kwargs)
            return o19_org_webbrowser_open(*args, **kwargs)
        webbrowser.open = o19_override_webbrowser_open
        log.debug("Replaced webbrowser.open()")
    except Exception as e2:
        log.warn(f"'webbrowser.open()': Could not inject '{e1}' or replace '{e2}' ")


log.debug(f"Injections initialized")
