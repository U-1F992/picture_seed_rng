#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Hat, Direction, Stick

from .util import WaitThread, execute

class Reset():
    """リセットして、マルチブート待機までの操作を定義するクラス
    """
    def __init__(self, command: ImageProcPythonCommand):
        self.__command = command
    def run(self):
        pass

class LoadGame():
    """マルチブート待ち受けを解除して、絵画鑑賞の直前までの操作を定義するクラス
    """
    def __init__(self, command: ImageProcPythonCommand):
        self.__command = command
    def run(self):
        pass

class SeePicture():
    """絵画を見て、離脱する操作を定義するクラス
    """
    def __init__(self, command: ImageProcPythonCommand):
        self.__command = command
    def run(self):
        pass

class MoveToDestination():
    """絵画を見た直後から、エンカウントの直前まで移動する操作を定義するクラス
    """
    def __init__(self, command: ImageProcPythonCommand):
        self.__command = command
    def run(self):
        pass

class Encounter():
    """エンカウント直前から、エンカウントする操作を定義するクラス
    """
    def __init__(self, command: ImageProcPythonCommand):
        self.__command = command
    def run(self):
        pass

class PaintSeed(ImageProcPythonCommand):
    NAME = '絵画seed乱数調整のテンプレート'
    def __init__(self, cam, gui=None):
        super().__init__(cam, gui)

    def do(self):

        frame_until_seeing = 600
        calibration_see_picture = 63

        frame_until_encountering = 600
        calibration_encounter = 0

        operations = (
            Reset(self), 
            LoadGame(self), 
            SeePicture(self), 
            MoveToDestination(self), 
            Encounter(self)
        )
        wait_threads = (
            WaitThread(self, frame_until_seeing, calibration_see_picture), 
            WaitThread(self, frame_until_encountering, calibration_encounter)
        )

        try:
            execute(operations, wait_threads)

        except Exception as e:
            print(f"[ERROR]: 失敗しました。{e.with_traceback(None)}")
