class InterruptError(Exception):
    """コマンドを中断するための例外クラス
    """
    pass
class NotMatchError(Exception):
    """テンプレートにマッチしなかった際に送出する内部例外クラス
    """
    pass
