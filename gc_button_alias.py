from enum import IntFlag

from Commands.Keys import Button as sw_button

class Button(IntFlag):
    Y = sw_button.Y
    B = sw_button.B
    A = sw_button.A
    X = sw_button.X
    L = sw_button.L
    R = sw_button.R
    Z = sw_button.ZR
    START = sw_button.HOME
