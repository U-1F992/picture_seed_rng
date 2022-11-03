from datetime import datetime, timedelta
from multiprocessing import Process
from typing import List, Tuple

from .pokecon_extension import wait
from .protocol import Event, Operation

def _run_and_wait_in_parallel(operations: List[Operation], wait: Process):
    """待機している間、ほかの操作を実行する。
    """
    try:
        wait.start()
        for op in operations:
            op.run()

        if not wait.is_alive():
            raise Exception("ロード完了前に待機が終了しました。")
    except:
        raise
    finally:
        wait.join()

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
    