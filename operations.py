from os.path import abspath, basename, dirname, exists, join

from Commands.PythonCommandBase import ImageProcPythonCommand, TEMPLATE_PATH
from Commands.Keys import Button, Hat

from .error import NotMatchError, InterruptError
from .pokecon_extension import execute_sequence, repeat

DEFAULT_DURATION = 0.05

# PythonCommandBase.pyで指定されたパスからたどって、リポジトリのtemplatesフォルダを指定する。
# `join(dirname(abspath(__file__)), "templates")`と同じ場所を指したい
BASE_PATH = join(TEMPLATE_PATH, "..", "Commands", "PythonCommands", basename(dirname(__file__)), "templates")
def resolve(fileName: str):
    ret = join(BASE_PATH, fileName)
    if not exists(ret):
        raise FileNotFoundError(ret)
    return ret

class Reset():
    """リセットして、マルチブート待機までの操作を定義するクラス
    """
    def __init__(self, command: ImageProcPythonCommand):
        self.__command = command
    def run(self):
        self.__command.wait(1)
        try:
            execute_sequence(self.__command, [
                # Zメニューを開く
                (Button.ZR, 0.5, 2),
                # カートリッジこうかん
                (resolve("change_cartridge_icon.png"),),
                (Button.A, DEFAULT_DURATION, 1),
                # 「ゲームを終了してカートリッジを交換しますか？」「いいえ」
                (resolve("change_cartridge_confirm.png"),),
                (Hat.LEFT, DEFAULT_DURATION, 1),
                # 「はい」
                (Button.A, DEFAULT_DURATION, 1),
                # 「カートリッジを交換してください。」
                (resolve("change_cartridge_done.png"),),
                (Button.A, DEFAULT_DURATION, 1),
                # マルチブート待機
                ([Button.HOME, Button.X], 4, 2),
                (resolve("gameboy_logo.png"),),
            ])
        except FileNotFoundError as e:
            raise InterruptError(f'指定されたテンプレート画像 "{str(e)}" が見つかりません。')
        except NotMatchError as e:
            raise InterruptError(f"テンプレートにマッチしませんでした。{str(e)}")

class LoadGame():
    """マルチブート待ち受けを解除して、絵画鑑賞の直前までの操作を定義するクラス
    """
    def __init__(self, command: ImageProcPythonCommand):
        self.__command = command
    def run(self):
        try:
            execute_sequence(self.__command, [
                # 待ち受け解除
                (Button.A, DEFAULT_DURATION, 6),
                # オープニングをスキップ
                (Button.A, DEFAULT_DURATION, 1.5),
                # タイトル表示までスキップ
                (Button.A, DEFAULT_DURATION, 1.5),
                # 「PUSH START BUTTON」
                (Button.A, DEFAULT_DURATION, 3),
                # 「でんちぎれの　ために　とけいが　うごかなくなりました」
                (Button.A, DEFAULT_DURATION, 2),
                # 「とけいに　かんけいする　できごとは　おきませんが　ゲームを　つづけて　あそぶことは　できます」
                (Button.A, DEFAULT_DURATION, 2),
                # セーブデータ選択
                (Button.A, DEFAULT_DURATION, 2),
            ])
        except FileNotFoundError as e:
            raise InterruptError(f'指定されたテンプレート画像 "{str(e)}" が見つかりません。')
        except NotMatchError as e:
            raise InterruptError(f"テンプレートにマッチしませんでした。{str(e)}")

class SeePicture():
    """絵画を見て、離脱する操作を定義するクラス
    """
    def __init__(self, command: ImageProcPythonCommand):
        self.__command = command
    def run(self):
        try:
            execute_sequence(self.__command, [
                # 絵画を見る
                (Button.A, DEFAULT_DURATION, 2),
                # 絵画画面から離脱する
                (Button.A, DEFAULT_DURATION, 2),
            ])
        except FileNotFoundError as e:
            raise InterruptError(f'指定されたテンプレート画像 "{str(e)}" が見つかりません。')
        except NotMatchError as e:
            raise InterruptError(f"テンプレートにマッチしませんでした。{str(e)}")

class MoveToDestination():
    """絵画を見た直後から、エンカウントの直前まで移動する操作を定義するクラス
    """
    def __init__(self, command: ImageProcPythonCommand):
        self.__command = command
    def run(self):
        try:
            execute_sequence(self.__command, [

                # コンテスト会場脱出
                *repeat((Hat.BTM, DEFAULT_DURATION, 0.75), 3),
                *repeat((Hat.LEFT, DEFAULT_DURATION, 0.75), 10),
                *repeat((Hat.BTM, DEFAULT_DURATION, 0.75), 8),
                (Hat.BTM, DEFAULT_DURATION, 3.5),

                # 船着き場まで
                *repeat((Hat.LEFT, DEFAULT_DURATION, 0.75), 16),
                *repeat((Hat.BTM, DEFAULT_DURATION, 0.75), 9),
                *repeat((Hat.RIGHT, DEFAULT_DURATION, 0.75), 5),      
                (Hat.TOP, DEFAULT_DURATION, 0.5),
                (Hat.TOP, DEFAULT_DURATION, 2.5),

                # 移動->会話->乗船
                *repeat((Hat.LEFT, DEFAULT_DURATION, 0.75), 4),
                *repeat((Hat.TOP, DEFAULT_DURATION, 0.75), 4),
                (Button.A, DEFAULT_DURATION, 1.5),
                (Button.A, DEFAULT_DURATION, 1.5),
                (Button.A, DEFAULT_DURATION, 4.5),
                *repeat((Button.A, DEFAULT_DURATION, 1.5), 4),
                (Button.A, DEFAULT_DURATION, 8.5),
                
                # みなみのことう移動
                *repeat((Hat.RIGHT, DEFAULT_DURATION, 0.75), 3),
                *repeat((Hat.TOP, DEFAULT_DURATION, 0.75), 7),
                *repeat((Hat.RIGHT, DEFAULT_DURATION, 0.75), 10),
                *repeat((Hat.TOP, DEFAULT_DURATION, 0.75), 9),
                *repeat((Hat.LEFT, DEFAULT_DURATION, 0.75), 6),
                *repeat((Hat.BTM, DEFAULT_DURATION, 0.75), 2),
                *repeat((Hat.LEFT, DEFAULT_DURATION, 0.75), 6),
                *repeat((Hat.TOP, DEFAULT_DURATION, 0.75), 4),
                (Hat.TOP, DEFAULT_DURATION, 2.5),
                *repeat((Hat.TOP, DEFAULT_DURATION, 0.75), 6),
            ])
        except FileNotFoundError as e:
            raise InterruptError(f'指定されたテンプレート画像 "{str(e)}" が見つかりません。')
        except NotMatchError as e:
            raise InterruptError(f"テンプレートにマッチしませんでした。{str(e)}")

class Encounter():
    """エンカウント直前から、エンカウントする操作を定義するクラス
    """
    def __init__(self, command: ImageProcPythonCommand):
        self.__command = command
    def run(self):
        try:
            execute_sequence(self.__command, [
                (Button.A, DEFAULT_DURATION, 15),
                (Button.B, DEFAULT_DURATION, 5),
            ])
        except FileNotFoundError as e:
            raise InterruptError(f'指定されたテンプレート画像 "{str(e)}" が見つかりません。')
        except NotMatchError as e:
            raise InterruptError(f"テンプレートにマッチしませんでした。{str(e)}")
