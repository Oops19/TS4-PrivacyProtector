"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY

Code slightly modified and merged together by o19 with written permission. All PyDoc removed as parameters may be used differently.
Most of my other mods use S4CL, embedding methods like this is a pain.
Use S4CL https://github.com/ColonolNutty/Sims4CommunityLibrary unless you really feel the need to make a standalone mod.
"""


from typing import Any, Union, Iterator, Tuple
from distributor.shared_messages import IconInfoData
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4.localization import TunableLocalizedStringFactory, create_tokens, _create_localized_string, LocalizationHelperTuning
from ui.ui_dialog import UiDialogResponse
from ui.ui_dialog_notification import UiDialogNotification


class S4CLInt:
    pass


class S4CLCommonInt(S4CLInt):
    # noinspection PyPropertyDefinition
    @property
    def value(self) -> int:
        return 0


class S4CLCommonStringId(S4CLCommonInt):
    STRING_NOT_FOUND_WITH_IDENTIFIER: 'S4CLCommonStringId' = 3037244137
    pass


class S4CLCommonLocalizedStringSeparator(S4CLCommonInt):
    pass


class S4CLCommonLocalizedStringColor(S4CLCommonInt):
    DEFAULT: 'S4CLCommonLocalizedStringColor' = -1


class S4CLCommonLocalizationUtils:
    @staticmethod
    def create_localized_string(identifier: Union[int, str, LocalizedString, S4CLCommonStringId, S4CLCommonLocalizedStringSeparator], tokens: Iterator[Any] = (), localize_tokens: bool = True, text_color: S4CLCommonLocalizedStringColor = S4CLCommonLocalizedStringColor.DEFAULT) -> LocalizedString:
        if identifier is None:
            return S4CLCommonLocalizationUtils.create_localized_string(S4CLCommonStringId.STRING_NOT_FOUND_WITH_IDENTIFIER, tokens=('None',), text_color=text_color)
        if localize_tokens:
            tokens = tuple(S4CLCommonLocalizationUtils._normalize_tokens(*tokens))
        if isinstance(identifier, LocalizedString) and hasattr(identifier, 'tokens'):
            create_tokens(identifier.tokens, tokens)
            return S4CLCommonLocalizationUtils.colorize(identifier, text_color=text_color)
        if isinstance(identifier, TunableLocalizedStringFactory._Wrapper):
            if isinstance(identifier._string_id, str):
                string_id = S4CLCommonLocalizationUtils.create_from_string(identifier._string_id)
            else:
                string_id = S4CLCommonLocalizationUtils.create_from_int(identifier._string_id, *tuple(tokens))
            return S4CLCommonLocalizationUtils.colorize(string_id, text_color=text_color)
        if isinstance(identifier, int):
            return S4CLCommonLocalizationUtils.colorize(S4CLCommonLocalizationUtils.create_from_int(identifier, *tuple(tokens)), text_color=text_color)
        if hasattr(identifier, 'sim_info'):
            return identifier.sim_info
        if hasattr(identifier, 'get_sim_info'):
            return identifier.get_sim_info()
        if isinstance(identifier, str):
            return S4CLCommonLocalizationUtils.create_localized_string(S4CLCommonLocalizationUtils.create_from_string(identifier), tokens=tokens, text_color=text_color)
        return S4CLCommonLocalizationUtils.create_localized_string(str(identifier), tokens=tokens, text_color=text_color)

    @staticmethod
    def create_from_int(identifier: int, *tokens: Any) -> LocalizedString:
        return _create_localized_string(identifier, *tokens)


    @staticmethod
    def _normalize_tokens(*tokens: Any) -> Iterator[LocalizedString]:
        new_tokens = []
        for token in tokens:
            new_tokens.append(S4CLCommonLocalizationUtils.create_localized_string(token))
        return tuple(new_tokens)

    @staticmethod
    def colorize(localized_string: LocalizedString, text_color: S4CLCommonLocalizedStringColor = S4CLCommonLocalizedStringColor.DEFAULT) -> LocalizedString:
        if text_color == S4CLCommonLocalizedStringColor.DEFAULT:
            return localized_string
        if not hasattr(text_color, 'value'):
            return localized_string
        return S4CLCommonLocalizationUtils.create_localized_string(text_color.value, tokens=(localized_string,))

    @staticmethod
    def create_from_string(string_text: str) -> LocalizedString:
        return LocalizationHelperTuning.get_raw_text(string_text)


class S4CLCommonBasicNotification:
    def __init__(
        self,
        title_identifier: Union[int, str, LocalizedString, S4CLCommonStringId],
        description_identifier: Union[int, str, LocalizedString, S4CLCommonStringId],
        title_tokens: Iterator[Any] = (),
        description_tokens: Iterator[Any] = (),
        urgency: UiDialogNotification.UiDialogNotificationUrgency = UiDialogNotification.UiDialogNotificationUrgency.DEFAULT,
        information_level: UiDialogNotification.UiDialogNotificationLevel = UiDialogNotification.UiDialogNotificationLevel.SIM,
        expand_behavior: UiDialogNotification.UiDialogNotificationExpandBehavior = UiDialogNotification.UiDialogNotificationExpandBehavior.USER_SETTING,
        ui_responses: Tuple[UiDialogResponse] = ()
    ):
        self.title = S4CLCommonLocalizationUtils.create_localized_string(title_identifier, tokens=tuple(title_tokens))
        self.description = S4CLCommonLocalizationUtils.create_localized_string(description_identifier, tokens=tuple(description_tokens))
        self.visual_type = UiDialogNotification.UiDialogNotificationVisualType.INFORMATION
        self.urgency = urgency
        self.information_level = information_level
        self.expand_behavior = expand_behavior
        self.ui_responses = ui_responses

    def show(self, icon: IconInfoData = None, secondary_icon: IconInfoData = None):
        _notification = self._create_dialog()
        if _notification is None:
            return

        _notification.show_dialog(
            icon_override=icon,
            secondary_icon_override=secondary_icon
        )

    def _create_dialog(self) -> Union[UiDialogNotification, None]:
        return UiDialogNotification.TunableFactory().default(
            None,
            title=lambda *args, **kwargs: self.title,
            text=lambda *args, **kwargs: self.description,
            visual_type=self.visual_type,
            urgency=self.urgency,
            information_level=self.information_level,
            ui_responses=self.ui_responses,
            expand_behavior=self.expand_behavior
        )

