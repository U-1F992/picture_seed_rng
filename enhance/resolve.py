from os.path import abspath, basename, dirname, exists, join

from Commands.PythonCommandBase import TEMPLATE_PATH

BASE_PATH = join("..", "Commands", "PythonCommands", basename(dirname(dirname(__file__))), "templates")
def resolve(fileName: str):
    """PythonCommandBase.pyで指定されたパスからたどって、リポジトリのtemplatesフォルダを指定する。
    
    `join(dirname(dirname(abspath(__file__))), "templates")`と同じ場所を指したい
    """
    ret = join(BASE_PATH, fileName)
    if not exists(join(TEMPLATE_PATH, ret)):
        raise FileNotFoundError(basename(ret))
    return ret
