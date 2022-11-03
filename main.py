from multiprocessing import Event, Process
from threading import Thread
from typing import Iterable
from Commands.PythonCommandBase import ImageProcPythonCommand

from .operations import Encounter, LoadGame, MoveToDestination, Reset, SeePicture
from .picture_seed import execute
from .pokecon_extension import check_if_alive, wait

VERSION = "v1.0.0"
MESSAGE = f"""
==================
title: 絵画seed乱数調整 {VERSION}（夢幻ラティ）
author: @meilleur_pkmn

prerequisite:
- Zメニューのカーソルが「カートリッジこうかん」に合っている。
- ミナモシティのコンテスト会場の左端の絵画の前でセーブしている。

information:
フレームカウンタ: 0x661B(F) = 26139 = 7分15秒程度
待機: 65029(F) = 18分3秒程度
ひかえめ　めざ炎70

絵画seedずれ: 63F
エンカウントずれ: -511F
==================
"""

# https://github.com/yatsuna827/Orca-GC-Controller/blob/1d69b507651b67bbb64c74cb0973180f2c1108a5/ORCA_GCController/MacroCompiler.cs#L440
GC_FPS = 59.7275
def _convert_frame_to_second(frame: int):
    return frame / GC_FPS

class PaintSeed(ImageProcPythonCommand):
    
    NAME = '絵画seed乱数調整サンプル'

    def __init__(self, cam, gui=None):
        super().__init__(cam, gui)

    def do(self):
        print(MESSAGE)

        frame_until_seeing = 26139
        calibration_seeing = 63
        
        frame_until_encountering = 65029
        calibration_encountering = -511
        
        second_until_seeing = _convert_frame_to_second(frame_until_seeing + calibration_seeing)
        second_until_encountering = _convert_frame_to_second(frame_until_encountering + calibration_encountering)
        wait_seconds = (
            second_until_seeing,
            second_until_encountering
        )

        operations = (
            Reset(self), 
            LoadGame(self), 
            SeePicture(self), 
            MoveToDestination(self), 
            Encounter(self)
        )

        event = Event()
        check = Thread(target=check_if_alive, args=(self, event))
        check.start()
        
        wait_processes = (
            Process(target=wait, args=(second_until_seeing, event)),
            Process(target=wait, args=(second_until_encountering, event))
        )

        try:
            execute(operations, wait_processes, wait_seconds)

        except Exception as e:
            print(f"操作は中断されました。{e.with_traceback(None)}")
        
        finally:
            check.join()
            for proc in wait_processes:
                proc.join()
