from datetime import datetime, timedelta
from multiprocessing import Process
from time import perf_counter
from typing import List, Tuple
from typing_extensions import Protocol

from picture_seed_rng.protocol import Event

class ExecutionInterruptedError(Exception):
    """コマンドを中断するための例外クラス
    """
    pass

class Operation(Protocol):
    def run(self):
        pass

def wait(seconds: float, event: Event):
    """指定時間待機する（別プロセスで実行することを想定）

    Args:
        seconds (float): 待機する秒数
        event (Event): 中断用`Event`オブジェクト
    """
    current_time = perf_counter()
    while perf_counter() < current_time + seconds and not event.is_set():
        pass

def _run_and_wait_in_parallel(operations: List[Operation], timer: Process, event: Event):
    """待機している間、ほかの操作を実行する。
    """
    timer.start()
    
    for op in operations:
        op.run()
    
    #
    # 正常に待機が完了
    # => joinは正常に終了する。
    #
    # GUIのStopにより中断
    # => check_if_aliveによってeventがセットされ、joinは正常に終了する。
    #    eventを確認し、中断を検知する。
    # 
    timer.join()
    if event.is_set():
        raise ExecutionInterruptedError("待機を中断しました。")

def _get_eta(seconds: float):
    return datetime.now() + timedelta(seconds=seconds)

def execute(
    operations: Tuple[Operation, Operation, Operation, Operation, Operation], 
    wait_seconds: Tuple[float, float],
    event: Event
):
    """絵画seed乱数調整を実行する。

    Args:
        operations (Tuple[Operation, Operation, Operation, Operation, Operation]): 各操作を定義したオブジェクトのタプル
        wait_seconds (Tuple[float, float]): 指定する待機時間のタプル
        event (Event): 中断用`Event`オブジェクト
    """
    
    reset, load_game, see_picture, move_to_destination, encounter = operations
    seconds_until_seeing, seconds_until_encountering = wait_seconds
    
    wait_until_seeing = Process(target=wait, args=(seconds_until_seeing, event))
    wait_until_encountering = Process(target=wait, args=(seconds_until_encountering, event))

    try:
        reset.run()

        print(f"タイマーを開始しました。ETA:{_get_eta(seconds_until_seeing)}")
        _run_and_wait_in_parallel(
            [
                load_game
            ], 
            wait_until_seeing, event
        )

        print(f"タイマーを開始しました。ETA:{_get_eta(seconds_until_encountering)}")
        _run_and_wait_in_parallel(
            [
                see_picture, 
                move_to_destination
            ], 
            wait_until_encountering, event
        )

        encounter.run()
    
    except ExecutionInterruptedError:
        raise

    finally:
        # 例外処理は呼び出し元に投げるが、Processは破棄する
        for proc in [proc for proc in [wait_until_seeing, wait_until_encountering] if proc.is_alive()]:
            proc.join()
