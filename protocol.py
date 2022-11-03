from typing_extensions import Protocol

class Operation(Protocol):
    def run(self):
        pass
    
class Event(Protocol):
    def is_set(self) -> bool:  # type: ignore
        pass
    def set(self):
        pass
    