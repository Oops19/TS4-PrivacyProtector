# Privacy Protector
This mod includes reviewed S4CL code to avoid and dependency to other mods.

## Features
It blocks, in contrary to ModGuard, also most mods which can be found on NSFW pages.

### Blocking Features
This mods blocks some Python calls which compromise security.

This mod does not block
* File access (reading, writing, encrypting, deleting files locally and in the network, USB and NAS)
* Python commands to load and/or execute code:
  * eval()
  * exec()
  * sys.modules()

Unfortunately the insecure eval() and exec() commands are used by TS4 itself.
They work very good as the initial attack vector to execute code and to encrypt files.
Python-based ransomware is available and it works fine. 
Without the ability to connect to the internet there should be at least no data breach.  

`sys.modules()` is needed by TS4 itself and file access is needed by mods to write log files.

### Logging Features
This mod supports scanning of script mods.

This mod scans `*.zip`, `*.ts4script` and `*.py` files the `The Sims 4/Mods/` and all sub-directories 
Mods which are saved to `The Sims 4/Mods/AAA/AAA/` (or any other 2nd level directory) will likely not be executed by TS4 but still scanned.

It does not yet read and scan `*.package` files. Malformed `Package`files to exploit vulnerabilities in `TS4.exe` usually crash the process and do no harm. 

## Usage
Read `Addendum / Installation` to install this mod. 
It should block all known methods to download and install malware.
It writes logs and shows an 'Alert' if something is detected.

The mod does not block execution of malware which runs completely offline.
To protect against such mods:
* Scan the mods before installing them and review the log files.
* Never ever install a mod which uses eval() or exec().  Ask the mod author to fix their mod.

If mods with eval() or exec() statements are found this mod will show a popup window and block further loading and execution of mods.
The game will shut down upon closing the window and allow you to remove these mods.
Or you might add them to the exception list and enjoy the risk.

### Background
Some mods invade the privacy of users and send a notification to the author every time `The Sims 4` is started.
While the `TS4.exe` process sends data to EA there is no need that mods do this.
Mod creators have no legitimate reason to collect data like
* Installed UGC of players
* Knowing when players start `The Sims 4`
* Geolocation of players
* EA username
* Local username
* Operating system

Other mods also download and execute malware.

All mods can be considered as UGC and the EA TOS https://tos.ea.com/legalapp/WEBTERMS/US/en/PC/ applies:

#### When you access or use an EA Service, you agree that you will not:
* Use any software or program that damages, interferes with or disrupts an EA Service or another's computer or property, such as denial of service attacks, spamming, hacking, or uploading computer viruses, worms, Trojan horses, cancelbots, spyware, corrupted files and time bombs.
* Interfere with or disrupt another player's use of an EA Service. This includes disrupting the normal flow of game play, chat or dialogue within an EA Service by, for example, using vulgar or harassing language, being abusive, excessive shouting (all caps), spamming, flooding or hitting the return key repeatedly.
* Attempt to obtain, or phish for, a password, account information, or other private information from anyone else on EA Services.

This mod does not disrupt any other normal mod.
* It will disrupt mods which violate your privacy.
* It will affect multiplayer mods which usually violate the EA TOS.
* It will also disrupt mods which make use of questionable functions for other purposes.
* Mods opening a TCP connection will also be affected even though an open socket alone does not violate privacy.

It may break some mods you have installed, but this is very unlikely.
You should be aware of these mods already.
* In case there is an issue you can always uninstall this mod.

During my tests I identified a few tracking mods but no False Positives were blocked.
I have been testing a lot, also with UGC containing malware.

The scanner itself will detect many things and lists them all.
Not everything detected is an actual call, it can also be a constant or string.
Du to the options Python has to write code it's hard to improve this behaviour.
In the scanners log file one can observe a lot of 'False Positives'.



## Internals

### Injector
The injector injects into various Python methods known to be used by trackers and malware to send data to sites and/or to download and execute code.
Normal script mods never call these methods.

It will raise a PrivacyException to prevent the further execution of this part of the mod. The mod will likely catch this exception and not notify the user.

It logs data to `The Sims 4/mod_logs/PrivacyProtector.txt` for review.

If it detects the usage of a very questionable method it will show an in-game popup.


#### Eval() & Exec()
Ths mod does not inject into eval() and exec() due to limitations of Python. The scanner will detect these methods.

## Scanner
This mod features also a scanner to scan the mods. It is not 100% accurate but quite good.
It starts one minute after starting The Sims 4 and scans all mods.

### Exclude from Scanner
To exclude some mods locate the 'The Sims 4/mod_data/privacy_protector/skip_mods/' directory and copy the mods (.ts4script files) to it.

It is enough to create an empty file with the exact mod name but copy may be easier for most users.
The content of the file does not matter. I included a few empty files of mods which are safe. You may remove them to get logs for them.

The scanner will report whether it found something when the game runs. Details are in the log file.
It runs in the background and allocates one core. There will be virtually no delay starting TS4 with a 4+ core CPU.

It is highly recommended to review the log file and to add safe mods to the skip_mods directory.

#### Manual Scanning
To scan new mods add them to the Mods folder while the game is already running.
* 'privacy.scan' scans the mods for known issues. This is the command you may want to use.
* 'privacy.search foo' allows to scan for 'foo' within mods. To scan only for 'exec' you may use this command with 'privacy.search exec'. It is slightly faster than a full scan.

Output is written to the console and also logged. As it can be quite a lot of data please be patient.

#### Eval() & Exec()
The manual and automatic scanner detect both methods.

There may be many matches like 'literal_eval', 'evaluate' or 'execute' which are considered as harmless. These will be logged as:
* Seems OK. Found eval in \sims4communitylib.ts4script(sims4communitylib/utils/cas/common_outfit_utils.pyc): ['\\x00\\x00\\x00\\xda\\x1devaluate_appearance_modi']

If you get a statement like this you may have a problem:
* !! Found eval in \_evil_\xxx.ts4script(xxx.pyc): ['\\x00\\x00\\x00\\xda\\x04eval\\xda\\x03hex\\xda\\x03l']

At the end of the scan process the summary is printed which makes it easy to look for real problems, if any. All close matches which seem to be harmless will not be counted.
* Found 'eval' 1 times.

Detected issues are logged with '!!' so they are easy to search.
The bad lines start with `''` while the 'good' lines start with 'Seems OK.' and don't count to towards the number of detected issues.

#### Output samples
This mod is a simple code scanner and as such can't be 100 % sure whether a detected issue is really malware.
So one needs to look at some code around of the statement to get an idea.

I already received requests to add AI code to this mod for a better accuracy but this would blow up the size of the mod and scanning would take ages if it ever completed. So please don't ask for this.


##### Trackers / Malware Downloader
If you find things like this you can be sure your mod has a tracker.

* !! Found 'FTP' in '\folder\mod.ts4script(file.pyc)': ['6remove)\\x01\\xda\\x03FTP\\xfa\\x01|r@\\x00\\x00\\', ...]
It's not clear what ftplib.FTP() command is executed, but for sure it's a tracker or malware downloader.

* !! Found 'open' in '\folder\mod.ts4script(file.pyc)': ['1\\x10\\x01\\xda\\x16mc_open_url_in_browser)\\x01', '\\nwebbrowser\\xda\\x04open)\\x03rq\\x00\\x00\\x00r']
Opening a web site sends at least your IP to a server, often also the operating system is submitted. The request itself may contain other personal information as URL parameters.

* !! Found 'urlopen' in '\folder\mod.ts4script(file.pyc)': ['eREQUEST_HEADERZ\\x07urlopen\\xda\\x16_parse_versi']
'urllib.request.urlopen()' is yet another way top send private data to a server.

* !! Found 'Request' in '\folder\mod.ts4script(file.pyc)': ['\\xda\\x07requestZ\\x07Request\\xda\\x0eREQUEST_HEAD']
'urllib.request.Request()' is also used in some mods with trackers.

##### Questionable
Here one should review the code, some of the code may have been written with good intentions but it may very often be used to track you.

* !! Found 'open' in '\folder\mod.ts4script(file.pyc)': ['\\nwebbrowser\\xda\\x04open)\\x01Z\\x06dialog)\\x0']
I don't think that 'open)' is bad, anyhow with 'webbrowser' in the found string it looks odd.

* !! Found 'eval' in '\folder\mods.ts4script(file.pyc)': ['5\\xda\\x03ord\\xda\\x04eval\\xda\\x03hexr\\x13\\x00']
* !! Found 'eval' in '\folder\mod.ts4script(file.pyc)': ['\\x00\\x00\\x00\\xda\\x04eval\\xda\\x03hex\\xda\\x03l']
Here one really wants to review the code, eval() should never be used. I reviewed it and can say that the code was safe but it was totally unnecessary to use eval().

##### False Positives
* !! Found 'system' in '\folder\mod.ts4script(file.pyc)': ['\\x01\\x00\\x00\\xda\\x06system\\xda\\x07releaser7\\x0', ...]
There seems to be no os.system.releaser() function, so this seems to be safe.

* !! Found 'system' in '\folder\mod.ts4script(file.pyc)': ['\\x08platform\\xda\\x06system\\xda\\x07version\\xda\\']
There is a system.version() method which is safe from my point of view.

* !! Found 'system' in '\folder\mod.ts4script(file.pyc)': ['of {M0.his}{F0.her} system, no ...']
o19 slaps the author of this mod around a bit with a large trout. STBL belongs into .package files and not hard coded into code. No one can translate it or add gender pronouns.

* !! Found 'open' in '\folder\mods.ts4script(file.pyc)': ['\\x00\\x00\\x00z\\x14ww.open_contact_page)\\x01Z\\', ...]
With open_ there is no issue at all, the filter is not perfect. :(

### Alerts
If you get a "Privacy violated. See logs for more details." alert you may want to know which mod caused it. You have to look into the logs file.
There a stack trace is written with the causing method and as TS4 stacks can be quite long and nested this mod doesn't try to locate the offending mod.
Usually it's the 2nd or 3rd line and not a vanilla function.

The stack trace will contain as much information as possible, make sure to remove them before sharing a stack trace.
It will be written on your computer and only people with access to your computer can read it.

One example for such a stack trace called by a test function:
```text
WARN	'os.system(('powershell',); {})' called from:

    T:\InGame\Gameplay\Scripts\Core\sims4\commands.py#398 '' in 'invoke_command()'
    ...\privacy_protector_light\commands.py#95 'os.system(command)' in 'o19_debug_priv_shell()'
    ...\privacy_protector_light\privacy_protector_light.py#283 'O19PrivacyProtector.log_data('os.system', *args, **kwargs)' in 'o19_override_os_system()'
    ...\privacy_protector_light\privacy_protector_light.py#57 'thread_details = traceback.extract_stack(sys._current_frames()[thread.ident])' in 'log_data()'
```

### Testing
The mod itself does not support testing things. In the 'mod_documentation' folder you'll find a 'Mods' folder which you may copy to your 'The Sims 4' folder.

It should look like this afterwards: 'The Sims 4/Mods/_o19_/Scripts/commands.py'
If you do this you enable yourself to connect to EA, open the browser or a shell. This should all work fine while this mod is not installed.
The Privacy Protector should keep you safe.

The Shift+Ctrl+C cheat console it needed to enter the commands:
* o19.priv - Print the following help
* o19.priv.browser - Open https://www.ea.com/de-de/games/the-sims/the-sims-4 in the browser. *1
* o19.priv.shell o - Open a powershell/bash.
* o19.priv.shell s - Open a powershell/bash in the background.
* o19.priv.socket - Open a socket connection to ea.com. *1
* o19.priv.urllib - Open a urllib connection to ea.com. *1
* o19.priv.scan eval - Scan mods for 'eval()'
* o19.priv.scan exec - Scan mods for 'exec()'
* o19.priv.scan foobar - Scan mods for 'foobar()' or any other function.

*1 EA should already know your IP address but you can edit the .py file and modify the used domain.

Actually all commands should fail as long as the Privacy Protector is running.
You may delete the mod but keep this file to make things work. Unless your endpoint security software blocks them.

'commands.py' doesn't execute things in powershell/bash and it doesn't open URLs which auto-download malware but all this is possible from within TS4.
With more and more malicious users targeting the community I decided to release this mod.

### Known Issues
This mod will cause an exception which is logged to lastException.txt as `FileNotFoundError: [Errno 2] No such file or directory: '50f50c67da416c0e5bc95ecb07a5a116d8b22106c27a1e60708b06e22eeed20b.zip'`.
This mod is still starting up fine while I'm looking for a way to avoid this exception.



# Addendum

## Game compatibility
This mod has been tested with `The Sims 4` 1.109.185, S4CL 3.7, TS4Lib 0.3.24 (2024-07-25).
It is expected to be compatible with many upcoming releases of TS4, S4CL and TS4Lib.

## Dependencies
Download the ZIP file, not the sources.
* [This Mod](../../releases/latest)
* [The Sims 4](https://www.ea.com/games/the-sims/the-sims-4)

If not installed download and install TS4 and these mods.
All are available for free.

## Installation
* Locate the localized `The Sims 4` folder which contains the `Mods` folder.
* Extract the ZIP file into this `The Sims 4` folder.
* It will create the directories/files `Mods/_o19_/$mod_name.ts4script`, `Mods/_o19_/$mod_name.package`, `mod_data/$mod_name/*` and/or `mod_documentation/$mod_name/*`
* `mod_logs/$mod_name.txt` will be created as soon as data is logged.

### Manual Installation
If you don't want to extract the ZIP file into `The Sims 4` folder you might want to read this. 
* The files in `ZIP-File/mod_data` are usually required and should be extracted to `The Sims 4/mod_data`.
* The files in `ZIP-File/mod_documentation` are for you to read it. They are not needed to use this mod.
* The `Mods/_o19_/*.ts4script` files can be stored in a random folder within `Mods` or directly in `Mods`. I highly recommend to store it in `_o19_` so you know who created it.

## Usage Tracking / Privacy
This mod does not send any data to tracking servers. The code is open source, not obfuscated, and can be reviewed.

Some log entries in the log file ('mod_logs' folder) may contain the local username, especially if files are not found (WARN, ERROR).

## External Links
[Sources](https://github.com/Oops19/)
[Support](https://discord.gg/d8X9aQ3jbm)
[Donations](https://www.patreon.com/o19)

## Copyright and License
* © 2024 [Oops19](https://github.com/Oops19)
* License for '.package' files: [Electronic Arts TOS for UGC](https://tos.ea.com/legalapp/WEBTERMS/US/en/PC/)  
* License for other media unless specified differently: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) unless the Electronic Arts TOS for UGC overrides it.
This allows you to use this mod and re-use the code even if you don't own The Sims 4.
Have fun extending this mod and/or integrating it with your mods.

Oops19 / o19 is not endorsed by or affiliated with Electronic Arts or its licensors.
Game content and materials copyright Electronic Arts Inc. and its licensors. 
Trademarks are the property of their respective owners.

### TOS
* Please don't put it behind a paywall.
* Please don't create mods which break with every TS4 update.
* For simple tuning modifications use [Patch-XML](https://github.com/Oops19/TS4-PatchXML) 
* or [LiveXML](https://github.com/Oops19/TS4-LiveXML).
* To check the XML structure of custom tunings use [VanillaLogs](https://github.com/Oops19/TS4-VanillaLogs).
