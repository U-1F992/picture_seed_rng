from time import sleep

from Commands.PythonCommandBase import PythonCommand

from picture_seed_rng.protocol import Event

def set_if_not_alive(command: PythonCommand, event: Event):
    """PythonCommandオブジェクトの`alive`がFalseになった場合にEventをセットする。
    """
    while command.alive:
        # Processを止めたいだけなのでタイミングはシビアではない。
        sleep(0.5)
    event.set()
