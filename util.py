from threading import Thread
from typing import Tuple
from typing_extensions import Protocol

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand

FRAMES_PER_SECOND = 60

def convert_frame_to_millisecond(frame: int) -> float:
    return frame / FRAMES_PER_SECOND

class WaitThread(Thread):
    """指定時間待機するスレッド
    """
    def __init__(self, command: PythonCommand, wait_frame: int, calibration_frame: int):
        """WaitThreadクラスのインスタンスを初期化する。

        Args:
            command (PythonCommand): _description_
            wait_frame (int): 待機するフレーム
            calibration_frame (int): 較正値
        """
        self.__command = command
        wait_frame_actual = wait_frame + calibration_frame
        self.__wait_millisecond = convert_frame_to_millisecond(wait_frame_actual)
    
    def run(self):
        self.__command.wait(self.__wait_millisecond)

class Operation(Protocol):
    def run(self):
        pass

def execute(operations: Tuple[Operation, Operation, Operation, Operation, Operation], wait_threads: Tuple[WaitThread, WaitThread]):
    """絵画seed乱数調整を実行する。

    Args:
        operations (Tuple[Operation, Operation, Operation, Operation, Operation]): 各操作を定義したオブジェクトのタプル
        wait_threads (Tuple[WaitThread, WaitThread]): 指定時間待機するWaitThreadオブジェクトのタプル
    """
    
    reset, load_game, see_picture, move_to_destination, encounter = operations
    wait_until_seeing, wait_until_encountering = wait_threads

    reset.run()

    wait_until_seeing.start()
    load_game.run()
    wait_until_seeing.join()

    wait_until_encountering.start()
    see_picture.run()
    move_to_destination.run()
    wait_until_encountering.join()

    encounter.run()
    