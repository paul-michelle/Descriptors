from typing import Callable, Any, TypeVar, List, Optional

T = TypeVar('T')
Callback = Callable[[...], Any]


class PreInitActionManager(object):

    def __init__(self):
        self._signals_registry = {}

    def connect(self, receiver: Callback, sender: T) -> None:
        self._signals_registry[sender.__name__] = [].append(receiver)

    def check_signals_registry(self, sender_name: str) -> List[Optional[Callback]]:
        return self._signals_registry.get(sender_name, [])


pre_init = PreInitActionManager()
