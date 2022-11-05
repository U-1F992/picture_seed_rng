from time import sleep

from Commands.PythonCommandBase import PythonCommand

from .protocol import Event

def set_if_not_alive(command: PythonCommand, event: Event):
    """PythonCommandオブジェクトの`alive`がFalseになった場合にEventをセットする。
    """
    while command.alive:
        sleep(0.5)
    event.set()
