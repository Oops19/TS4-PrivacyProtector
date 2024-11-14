"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY

Code slightly modified and merged together by o19 with written permission. All PyDoc removed as parameters may be used differently.
Most of my other mods use S4CL, embedding methods like this is a pain.
Use S4CL https://github.com/ColonolNutty/Sims4CommunityLibrary unless you really feel the need to make a standalone mod.
"""


from typing import Any, Union


class S4CLCommonModIdentity:
    def __init__(self, name: str, author: str, base_namespace: str, file_path: str, version: str):
        self._name = name.replace(' ', '_')
        self._author = author
        self._base_namespace = base_namespace
        self._script_file_path = file_path
        self._version = version

    @property
    def name(self) -> str:
        return str(self._name)

    @property
    def author(self) -> str:
        return str(self._author)

    @property
    def base_namespace(self) -> str:
        return str(self._base_namespace)

    @property
    def file_path(self) -> str:
        return str(self._script_file_path)

    @property
    def version(self) -> str:
        return str(self._version)

    @staticmethod
    def _get_mod_name(mod_identifier: Union[str, 'S4CLCommonModIdentity']) -> Union[str, None]:
        from sims4communitylib.utils.misc.common_mod_identity_utils import CommonModIdentityUtils
        return CommonModIdentityUtils.determine_mod_name_from_identifier(mod_identifier)

    def __eq__(self, other: 'S4CLCommonModIdentity') -> bool:
        if isinstance(other, str):
            return self.name == other
        if not isinstance(other, S4CLCommonModIdentity):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return 'mod_{}_version_{}_author_{}_namespace_{}'.format(self.name, self.version.replace('.', '_').replace('/', '_').replace('\\', '_'), self.author, self.base_namespace)

    def __str__(self) -> str:
        return 'Identity:\n Mod Name: {}\n Version: {}\n Mod Author: {}\n Base Namespace: {}\n Path To Mod: {}'.format(self.name, self.version, self.author, self.base_namespace, self.file_path)


class _S4CLSingleton(type):
    def __init__(cls, *args, **kwargs) -> None:
        super(_S4CLSingleton, cls).__init__(*args, **kwargs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs) -> 'S4CLCommonService':
        if cls.__instance is None:
            cls.__instance = super(_S4CLSingleton, cls).__call__(*args, **kwargs)
        return cls.__instance


class S4CLCommonService(metaclass=_S4CLSingleton):
    @classmethod
    def get(cls: Any, *_, **__) -> 'S4CLCommonService':
        return cls(*_, **__)


class S4CLCommonModInfo(S4CLCommonService):
    @classmethod
    def get_identity(cls) -> S4CLCommonModIdentity:
        identity_property_name = '_MOD_IDENTITY'
        if getattr(cls, identity_property_name, None) is None:
            mod_info: S4CLCommonModInfo = cls.get()
            setattr(cls, identity_property_name, S4CLCommonModIdentity(mod_info._name, mod_info._author, mod_info._base_namespace, mod_info._file_path, mod_info._version))
        return getattr(cls, identity_property_name)

    @property
    def _name(self) -> str:
        raise NotImplementedError('Missing \'{}._name\'.'.format(self.__class__.__name__))

    @property
    def _author(self) -> str:
        raise NotImplementedError('Missing \'{}._author\'.'.format(self.__class__.__name__))

    @property
    def _base_namespace(self) -> str:
        raise NotImplementedError('Missing \'{}._base_namespace\'.'.format(self.__class__.__name__))

    @property
    def _file_path(self) -> str:
        raise NotImplementedError('Missing \'{}._file_path\'.'.format(self.__class__.__name__))

    @property
    def _version(self) -> str:
        return '1.0'


class S4CLModInfo:
    mod_name = 'Privacy-Protector'

    @staticmethod
    def get_identity() -> str:
        return S4CLModInfo.mod_name


class ModInfo(S4CLCommonModInfo):
    _FILE_PATH: str = str(__file__)

    @property
    def _name(self) -> str:
        # This is the name that'll be used whenever a Messages.txt or Exceptions.txt file is created <_name>_Messages.txt and <_name>_Exceptions.txt.
        return 'Privacy-Protector'

    @property
    def _author(self) -> str:
        # This is your name.
        return 'o19'

    @property
    def _base_namespace(self) -> str:
        # This is the name of the root package
        return 'privacy_protector'

    @property
    def _file_path(self) -> str:
        # This is simply a file path that you do not need to change.
        return ModInfo._FILE_PATH

    @property
    def _version(self) -> str:
        return '1.9.5'


r'''
v1.9.5
    Fixes:
        PP-3 Count the number of network/launch/other calls properly.
v.1.9.4
    Fixes:
        PP-2 Last scanned mod instead of mods with issues are shown in popup.
v1.9.3
    Tested with TS4 v1.107
v1.9.2
    Improvements:
        PP-1 Add the offending mods to the popup message.
v1.9.1
    Fixed text in Popup Message
v1.9.0
    Added Popup Message & Kill-Switch
    Improved scanning pattern to list less matches
    Refactored code
v.1.8.0
    Run scanner in foreground
    Suspend loading for 30 minutes if eval() or exec() is found.
v.1.6.7
    Update README for new TS4 version
v.1.6.6
    Update README for new TS4 version
v.1.6.5
    Update README for new TS4 version
v1.6.4
    Remove ts4script.py from code
v1.6.3
    Updated for the current TS4 version
v1.6.2
    Reduced logging a bit
v1.6.1
    Scan delayed to start when the game is ready
v1.6
    Finally fixed a weird bypass issue
v1.4
    Added scanner to rS4CL at startup
v1.2
    Replaced o19.priv.scan with 'privacy.search' - 'privacy.scan' will scan everything 
v1.2
    Switched to .py instead of .ts4script for better detection rates
v1.1
    Added scan
v1.0
    Initial version
'''
