# Privacy Protector

## Installation
The ZIP file should be extracted into the `The Sims 4` folder to make sure that the folder structure is set up correctly.

Unless not yet installed: This mod requires S4CL, install it.

## Usage to scan for eval() and exec()
Ths mod does not inject into eval() and exec() due to 'limitations' of Python. Manual scanning is supported and recommended:
* `o19.priv.scan eval` - Scan your Mods folder for code which contains eval(...).
* `o19.priv.scan exec` - Scan your Mods folder for code which contains exec(...).
* `o19.priv.scan foobar` Scan your Mods folder for code which contains 'foobar', actually you can specify a random string. But 'eval' and 'exec' are the most interesting.

Output is written to the console and logged to the log file. There may be many matches like 'literal_eval', 'evaluate' or 'execute' which are considered as harmless.
* Seems OK. Found eval in \sims4communitylib.ts4script(sims4communitylib/utils/cas/common_outfit_utils.pyc): ['\\x00\\x00\\x00\\xda\\x1devaluate_appearance_modi']
* !!  !! Found eval in \_evil_\xxx.ts4script(xxx.pyc): ['\\x00\\x00\\x00\\xda\\x04eval\\xda\\x03hex\\xda\\x03l']
* Found 'eval' 1 times.

At the end you get a summary, the bad lines start with `''` while the 'good' lines start with 'Seems OK.' and don't count to towards the number of detected issues.
This method can be used to scan for many things in script mods.
Using eval or exec in a script mod is totally unnecessary. For the safety of your game you may want to remove mods which use one of these methods.

## License and Copying
© 2022 Oops19
https://creativecommons.org/licenses/by/4.0/ unless the EA TOS for UGC overrides it.

Have fun extending this mod and/or integrating it within your mod.  Feel free to share and improve this mod including sources with everyone interested.

I don't work with authors who added malware loaders and/or code to break other mods who reserve the right to do it again. ==> Do not ask me for WW support.

* Please don't put it behind a paywall.
* Please don't create mods which break with every TS4 update.


# Privacy Protector Docs [to be updated]

From the EA TOS https://tos.ea.com/legalapp/WEBTERMS/US/en/PC/:

### When you access or use an EA Service, you agree that you will not:
* Use any software or program that damages, interferes with or disrupts an EA Service or another's computer or property, such as denial of service attacks, spamming, hacking, or uploading computer viruses, worms, Trojan horses, cancelbots, spyware, corrupted files and time bombs.
* Interfere with or disrupt another player's use of an EA Service. This includes disrupting the normal flow of game play, chat or dialogue within an EA Service by, for example, using vulgar or harassing language, being abusive, excessive shouting (all caps), spamming, flooding or hitting the return key repeatedly.
* Attempt to obtain, or phish for, a password, account information, or other private information from anyone else on EA Services.

This mod does not disrupt any other normal mod.
It will disrupt mods which violate your privacy.
It will affect multiplayer mods which usually violate the EA TOS.
It will also disrupt mods which make use of critical functions for other purposes.
Mods opening a TCP connection will also be affected even though an open socket alone does not violate privacy.

It may break some mods you have installed, but this is very unlikely.
You should be aware of these mods already.
In case there is an issue you can always uninstall the mod.

During my tests I identified a few tracking mods but no False Positives.


## How it works
It injects into various methods know to be used by trackers and malware to send data to sites and/or to download and execute code.
Normal script mods never call these methods.

It logs data to `The Sims 4/mod_logs/PrivacyProtector.txt` (or a similar file name) for review.

If it detects the usage of a very questionable method it will show an in-game popup.

## Alerts
If you get a "Privacy Violation" alert and you want to know which mod caused it you have to look into the logs file.
There a stack trace is written with the causing method and as TS4 stacks can be quite long and nested this mod doesn't try to locate the offending mod.

The stack trace will contain as much information as possible, it will contain your user name and mod folder location so make sure to remove them before sharing a stack trace.
It will be written on your computer and only people with access to your computer can read it.
`2022-05-18T19:57:47	WARN	'os.system(('powershell',); {})' called from:
    T:\InGame\Gameplay\Scripts\Core\sims4\commands.py#398 '' in 'invoke_command()'
    ...\privacy_protector_light\commands.py#95 'os.system(command)' in 'o19_debug_priv_shell()'
    ...\privacy_protector_light\privacy_protector_light.py#283 'O19PrivacyProtector.log_data('os.system', *args, **kwargs)' in 'o19_override_os_system()'
    ...\privacy_protector_light\privacy_protector_light.py#57 'thread_details = traceback.extract_stack(sys._current_frames()[thread.ident])' in 'log_data()'
`

## Testing
The mod itself does not support testing things. Anyhow in the 'mod_documentation' folder you'll find a 'Mods' folder which you may copy to your 'The Sims 4' folder.
It should look like this afterwards: 'The Sims 4/Mods/_o19_/Scripts/commands.py'
If you do this you enable yourself to connect to EA, open the browser or a shell.

The Shift+Ctrl+C cheat console it needed to enter the commands:
* o19.priv - Print the following help
* o19.priv.browser - Open https://www.ea.com/de-de/games/the-sims/the-sims-4 in the browser. *1
* o19.priv.shell o - Open a powershell/bash.
* o19.priv.shell s - Open a powershell/bash in the background.
* o19.priv.socket - Open a socket connection to ea.com. *1
* o19.priv.urllib - Open a urllib connection to ea.com. *1

*1 EA should already know your IP address but you can edit the .py file and modify the used domain.

Actually all commands will fail as long as the Privacy Protector is running.
You may delete the mod but keep this file to make things work. Unless your endpoint security software blocks them.

I don't execute things in powershell/bash and I don't open URLs which auto-download malware but all this is possible from within TS4.
With more malicious users targeting the community I decided to release this mod.
