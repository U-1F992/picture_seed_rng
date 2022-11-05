from typing import List

from Commands.PythonCommandBase import ImageProcPythonCommand

from .type_alias import ArgumentCombination

class NotMatchError(Exception):
    """テンプレートにマッチしなかった際に送出する内部例外クラス
    """
    pass

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
        NotMatchError: `isContainTemplate`がFalseを返した
    """
    for argument in arguments:
        #print(f"[DEBUG]: {argument}")
        _execute_method(command, argument)

def repeat(argument: ArgumentCombination, count: int) -> List[ArgumentCombination]:
    return [argument] * count

def _execute_method(command: ImageProcPythonCommand, argument: ArgumentCombination) -> None:
    
    command.checkIfAlive()

    # ArgumentCombinationはいずれの場合も少なくとも1つの要素があり、
    # IsContainTemplateArgumentCombinationの場合は、先頭の型は必ずstr

    # 解析できないのはしょうがないのでtype: ignore

    if isinstance(argument[0], str):
        if not command.isContainTemplate(*argument):  # type: ignore
            raise NotMatchError(argument[0])
    else:
        command.press(*argument)  # type: ignore
