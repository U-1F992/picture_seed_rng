from typing_extensions import Protocol

class Event(Protocol):
    """multiprocessingとthreadingのEventを差し替え可能にするためのProtocol
    """
    def is_set(self) -> bool:  # type: ignore
        pass
    def set(self):
        pass
    