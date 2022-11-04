from multiprocessing import Event
from threading import Thread

from Commands.PythonCommandBase import ImageProcPythonCommand
from Commands.Keys import Hat

from .enhance.set_if_not_alive import set_if_not_alive
from .operations import Encounter, LoadGame, MoveToDestination, Reset, SeePicture
from .picture_seed_rng.picture_seed import ExecutionInterruptedError, execute

VERSION = "v1.0.0"
MESSAGE = f"""
==================
title: 絵画seed乱数調整 {VERSION}（夢幻ラティ）
author: @meilleur_pkmn

prerequisite:
- Zメニューのカーソルが「カートリッジこうかん」に合っている。
- ミナモシティのコンテスト会場の左端の絵画の前でセーブしている。
- 手持ちを1体にして、ボールの一番上にマスターボールがある。

information:
フレームカウンタ: 0x9E28 = 40488(F)
待機: 48134(F)
おくびょう 30 3 30 31 31 31 氷70

絵画seedずれ: 24F
エンカウントずれ: -511F
==================
"""

# https://github.com/yatsuna827/Orca-GC-Controller/blob/1d69b507651b67bbb64c74cb0973180f2c1108a5/ORCA_GCController/MacroCompiler.cs#L440
GC_FPS = 59.7275
def _convert_frame_to_second(frame: int):
    return frame / GC_FPS

class PictureSeedRNG(ImageProcPythonCommand):
    
    NAME = '絵画seed乱数調整サンプル'

    def __init__(self, cam, gui=None):
        super().__init__(cam, gui)

    def do(self):
        print(MESSAGE)

        frame_until_seeing = 40488
        calibration_seeing = 24
        
        frame_until_encountering = 48134
        calibration_encountering = -511
        
        wait_seconds = (
            _convert_frame_to_second(frame_until_seeing + calibration_seeing),
            _convert_frame_to_second(frame_until_encountering + calibration_encountering)
        )

        operations = (
            Reset(self), 
            LoadGame(self), 
            SeePicture(self), 
            MoveToDestination(self), 
            Encounter(self)
        )

        event = Event()
        check = Thread(target=set_if_not_alive, args=(self, event))
        check.start()

        
        while True:
            try:
                execute(operations, wait_seconds, event)
            except ExecutionInterruptedError as e:
                print(str(e))
                # 最終的にStopThreadを送出して、コマンド実行を終了させる。
                self.checkIfAlive()
            
            self.save_capture()
    
    def save_capture(self):
        self.camera.saveCapture()
        self.press(Hat.RIGHT, 0.05, 3)
        self.camera.saveCapture()
