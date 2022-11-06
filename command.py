from multiprocessing import Event
from threading import Thread

from Commands.PythonCommandBase import ImageProcPythonCommand
from Commands.Keys import Hat

from .enhance.execute import NotMatchError
from .enhance.set_if_not_alive import set_if_not_alive
from .operations import Encounter, LoadGame, MoveToDestination, Reset, SeePicture
from .picture_seed_rng.picture_seed import execute


# https://github.com/yatsuna827/Orca-GC-Controller/blob/1d69b507651b67bbb64c74cb0973180f2c1108a5/ORCA_GCController/MacroCompiler.cs#L440
GC_FPS = 59.7275
def _convert_frame_to_second(frame: int):
    return frame / GC_FPS

class PictureSeedRNG(ImageProcPythonCommand):

    def __init__(self, cam, gui=None):
        super().__init__(cam, gui)

        self.NAME = '絵画seed乱数調整サンプル'
        VERSION = "v1.0.0"
        
        FRAME_SEEING = 0x9E28
        CALIB_SEEING = 24
        self.__seconds_seeing = _convert_frame_to_second(FRAME_SEEING + CALIB_SEEING)

        FRAME_ENCOUNTERING = 48134
        CALIB_ENCOUNTERING = -552
        self.__seconds_encountering = _convert_frame_to_second(FRAME_ENCOUNTERING + CALIB_ENCOUNTERING)

        self.MESSAGE = f"""
    ==================
    title: 絵画seed乱数調整 {VERSION}（夢幻ラティ）
    author: @meilleur_pkmn

    prerequisite:
    - Zメニューのカーソルが「カートリッジこうかん」に合っている。
    - コンテスト会場（ミナモシティ）の左端にある絵画の前でレポートを書いている。
    - 手持ちが1体で、ボールの一番上にマスターボールがある。

    information:
    フレームカウンタ: {hex(FRAME_SEEING)} = {FRAME_SEEING}(F)
    待機: {FRAME_ENCOUNTERING}(F)
    おくびょう 30 3 30 31 31 31 氷70

    絵画seedずれ: {CALIB_SEEING}(F)
    エンカウントずれ: {CALIB_ENCOUNTERING}(F)
    ==================
    """

    def do(self):
        print(self.MESSAGE)

        operations = (
            Reset(self), 
            LoadGame(self), 
            SeePicture(self), 
            MoveToDestination(self), 
            Encounter(self)
        )
        wait_seconds = (
            self.__seconds_seeing,
            self.__seconds_encountering
        )

        event = Event()
        check = Thread(target=set_if_not_alive, args=(self, event))
        check.start()

        
        while True:
            # doはStopThread以外の例外をおもらししてはいけない
            try:
                execute(operations, wait_seconds, event)
                self.checkIfAlive()
                self.save_capture()

            except FileNotFoundError as e:
                # 画像が見つからない
                # => 終了
                print(f'指定されたテンプレート画像 "{str(e)}" が見つかりません。')
                return

            except NotMatchError as e:
                # 操作が失敗している
                # => リセットからやりなおし
                print(str(e))
    
    def save_capture(self):
        self.camera.saveCapture()
        self.press(Hat.RIGHT, 0.05, 3)
        self.camera.saveCapture()
