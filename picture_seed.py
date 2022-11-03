from datetime import datetime, timedelta
from multiprocessing import Process
from typing import List, Tuple
from typing_extensions import Protocol

class Operation(Protocol):
    def run(self):
        pass

def _run_and_wait_in_parallel(operations: List[Operation], wait: Process):
    """待機している間、ほかの操作を実行する。
    """
    wait.start()
    for op in operations:
        op.run()

    if not wait.is_alive():
        raise Exception("ロード完了前に待機が終了しました。")
    wait.join()

def _get_eta(seconds: float):
    return datetime.now() + timedelta(seconds=seconds)

def execute(
    operations: Tuple[Operation, Operation, Operation, Operation, Operation], 
    wait_processes: Tuple[Process, Process], 
    wait_seconds: Tuple[float, float]
):
    """絵画seed乱数調整を実行する。

    Args:
        operations (Tuple[Operation, Operation, Operation, Operation, Operation]): 各操作を定義したオブジェクトのタプル
        wait_processes (Tuple[Tuple[Process, float], Tuple[Process, float]]): 指定時間待機するProcessオブジェクトのタプル
        wait_seconds (Tuple[float, float]): 指定した待機時間のタプル
    """
    
    reset, load_game, see_picture, move_to_destination, encounter = operations
    wait_until_seeing, wait_until_encountering = wait_processes
    seconds_until_seeing, seconds_until_encountering = wait_seconds

    reset.run()

    print(f"タイマーを開始しました。ETA:{_get_eta(seconds_until_seeing)}")
    _run_and_wait_in_parallel(
        [
            load_game
        ], 
        wait_until_seeing
    )

    print(f"タイマーを開始しました。ETA:{_get_eta(seconds_until_encountering)}")
    _run_and_wait_in_parallel(
        [
            see_picture, 
            move_to_destination
        ], 
        wait_until_encountering
    )

    encounter.run()
    