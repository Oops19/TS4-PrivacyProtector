"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY

Code slightly modified and merged together by o19 with written permission. All PyDoc removed as parameters may be used differently.
Most of my other mods use S4CL, embedding methods like this is a pain.
Use S4CL https://github.com/ColonolNutty/Sims4CommunityLibrary unless you really feel the need to make a standalone mod.
"""


from functools import wraps
from typing import Any, Callable


class _S4CLTypeChecking:
    # noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring
    @classmethod
    def class_method(cls):
        pass

    # noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring
    def self_method(self):
        pass

    # noinspection PyPropertyDefinition,PyMissingTypeHints,PyMissingOrEmptyDocstring
    @property
    def property_type(self):
        pass

    # noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring
    @staticmethod
    def static_method():
        pass


S4CLClassMethodType = type(_S4CLTypeChecking.class_method)
S4CLSelfMethodType = type(_S4CLTypeChecking.self_method)
S4CLStaticMethodType = type(_S4CLTypeChecking.static_method)
S4CLPropertyType = type(_S4CLTypeChecking.property_type)


class S4CLCommonInjectionUtils:
    @staticmethod
    def inject_safely_into(nop, target_object: Any, target_function_name: str, handle_exceptions: bool = True) -> Callable:
        handle_exceptions = False
        if handle_exceptions:
            pass
        else:
            def _function_wrapper(original_function, new_function: Callable[..., Any]) -> Any:
                # noinspection PyBroadException
                try:
                    if isinstance(original_function, S4CLClassMethodType):
                        original_function_func = original_function.__func__

                        # noinspection PyDecorator
                        @wraps(original_function)
                        def _wrapped_class_function(cls, *args, **kwargs) -> Any:
                            # noinspection PyMissingTypeHints
                            def _do_original(*_, **__):
                                return original_function_func(cls, *_, **__)

                            return new_function(_do_original, cls, *args, **kwargs)
                        return classmethod(_wrapped_class_function)

                    if isinstance(original_function, S4CLSelfMethodType):
                        @wraps(original_function)
                        def _wrapped_self_function(self, *args, **kwargs) -> Any:
                            return new_function(original_function, self, *args, **kwargs)

                        return _wrapped_self_function

                    if isinstance(original_function, S4CLPropertyType):
                        # noinspection PyTypeChecker
                        @wraps(original_function)
                        def _wrapped_property_function(self, *args, **kwargs) -> Any:
                            return new_function(original_function.fget, self, *args, **kwargs)

                        return property(_wrapped_property_function)

                    if isinstance(original_function, S4CLStaticMethodType):
                        original_function_func = original_function.__func__

                        # noinspection PyDecorator
                        @wraps(original_function)
                        def _wrapped_static_function(*args, **kwargs) -> Any:
                            # noinspection PyMissingTypeHints
                            def _do_original(*_, **__):
                                return original_function_func(*_, **__)

                            return new_function(_do_original, *args, **kwargs)

                        return staticmethod(_wrapped_static_function)

                    @wraps(original_function)
                    def _wrapped_other_function(*args, **kwargs) -> Any:
                        return new_function(original_function, *args, **kwargs)

                    return _wrapped_other_function
                except:
                    def _func(*_, **__) -> Any:
                        pass
                    return _func

        def _injected(wrap_function) -> Any:
            original_function = getattr(target_object, str(target_function_name))
            setattr(target_object, str(target_function_name), _function_wrapper(original_function, wrap_function))
            return wrap_function
        return _injected
