from typing import List, Tuple, Union

from Commands.PythonCommandBase import ImageProcPythonCommand
from Commands.Keys import Button, Direction, Hat

# Pythonコマンド_作成How_to
# - https://github.com/KawaSwitch/Poke-Controller/wiki/Python%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89_%E4%BD%9C%E6%88%90How_to

#
# pressメソッドの引数buttonが取りうる型
#
ButtonSpecifier = Union[
    Button, 
    Hat, 
    Direction, 

    # 同時入力
    List[
        Union[
            Button, 
            Hat, 
            Direction
        ]
    ]
]

#
# pressメソッドが取りうる引数の組み合わせ
#
# - buttons: 押下するボタン
# - duration: 押下時間[秒] デフォルトは0.1
# - wait: 押下後に待つ時間[秒] デフォルトは0.1
#
PressArgumentCombination = Union[
    Tuple[ButtonSpecifier],
    Tuple[ButtonSpecifier, float],
    Tuple[ButtonSpecifier, float, float],
]

#
# isContainTemplateメソッドが取りうる引数の組み合わせ
#
# - template_path: 探すテンプレート画像のパス(拡張子を含む画像名)
# - threshold: しきい値 デフォルトでは0.7
# - use_gray: 処理をグレースケールで行う デフォルトではTrue
#
IsContainTemplateArgumentCombination = Union[
    Tuple[str],
    Tuple[str, float],
    Tuple[str, float, float],
]

ArgumentCombination = Union[
    PressArgumentCombination,
    IsContainTemplateArgumentCombination
]

def repeat(argument: ArgumentCombination, count: int) -> List[ArgumentCombination]:
    return [argument] * count

def execute_sequence(command: ImageProcPythonCommand, arguments: List[ArgumentCombination]):
    """引数のリストを与えて、ImageProcPythonCommandの`press`メソッドと`isContainTemplate`メソッドを一括で実行する。
    
    `isContainTemplate`がFalseを返すと例外を送出します。おもに`press`が正常に完了しているかを確認するために使用する想定です。

    Args:
        command (ImageProcPythonCommand): ImageProcPythonCommandオブジェクト（`self`）
        arguments (List[ArgumentCombination]): 各メソッドが取りうる引数の組み合わせのリスト
    
    ```python
    def press(buttons: Button | Hat | Direction | list[Button | Hat | Direction], duration: float = 0.1, wait: float = 0.1):
        pass

    def isContainTemplate(template_path: str, threshold: float = 0.7, use_gray: bool = True):
        pass
    ```
    
    Raises:
        Exception: `isContainTemplate`がFalseを返した
    """
    for argument in arguments:
        if not _execute_method(command, argument):
            raise Exception("isContainTemplateがFalseを返しました。")

def _execute_method(command: ImageProcPythonCommand, argument: ArgumentCombination) -> bool:
    
    # ArgumentCombinationはいずれの場合も少なくとも1つの要素があり、
    # IsContainTemplateArgumentCombinationの場合は、先頭の型は必ずstr

    if type(argument[0]) is str:
        return command.isContainTemplate(*argument)
    else:
        command.press(*argument)
        return True
