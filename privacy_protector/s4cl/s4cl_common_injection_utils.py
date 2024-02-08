"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY

Code slightly modified and merged together by o19 with written permission. All PyDoc removed as parameters may be used differently.
Most of my other mods use S4CL, embedding methods like this is a pain.
Use S4CL https://github.com/ColonolNutty/Sims4CommunityLibrary unless you really feel the need to make a standalone mod.
"""


import inspect
from functools import wraps
from typing import Any, Callable


class S4CLCommonInjectionUtils:
    @staticmethod
    def inject_safely_into(nop, target_object: Any, target_function_name: str, handle_exceptions: bool = True) -> Callable:
        if handle_exceptions:
            def _function_wrapper(original_function, new_function: Callable[..., Any]) -> Any:
                # noinspection PyBroadException
                try:
                    @wraps(original_function)
                    def _wrapped_function(*args, **kwargs) -> Any:
                        try:
                            if type(original_function) is property:
                                return new_function(original_function.fget, *args, **kwargs)
                            return new_function(original_function, *args, **kwargs)
                        except Exception as ex:
                            pass
                            return original_function(*args, **kwargs)
                    if inspect.ismethod(original_function):
                        return classmethod(_wrapped_function)
                    if type(original_function) is property:
                        return property(_wrapped_function)
                    return _wrapped_function
                except:
                    def _func(*_, **__) -> Any:
                        pass
                    return _func
        else:
            def _function_wrapper(original_function, new_function: Callable[..., Any]) -> Any:
                @wraps(original_function)
                def _wrapped_function(*args, **kwargs) -> Any:
                    if type(original_function) is property:
                        return new_function(original_function.fget, *args, **kwargs)
                    return new_function(original_function, *args, **kwargs)

                if inspect.ismethod(original_function):
                    return classmethod(_wrapped_function)
                elif type(original_function) is property:
                    return property(_wrapped_function)
                return _wrapped_function

        def _injected(wrap_function) -> Any:
            original_function = getattr(target_object, str(target_function_name))
            setattr(target_object, str(target_function_name), _function_wrapper(original_function, wrap_function))
            return wrap_function
        return _injected
