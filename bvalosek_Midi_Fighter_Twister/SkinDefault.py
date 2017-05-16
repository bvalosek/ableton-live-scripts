from _Framework.ButtonElement import Color
from _Framework.Skin import Skin

from Colors import *

class Colors:
    class Modes:
        Selected = ColorEx(Rgb.GREEN, Animation.PULSE_1_BEAT)
        NotSelected = ColorEx(Rgb.GREEN, Brightness.LOW)

    class DefaultButton:
        On = ColorEx(Rgb.GREEN)
        Disabled = ColorEx(Rgb.GREEN, Brightness.LOW)
        Off = ColorEx(Rgb.OFF, Brightness.OFF)

    class Device:
        Menu = ColorEx(Rgb.BLUE, Animation.GATE_1_BEAT)
        MenuSelect = ColorEx(Rgb.TEAL)
        Select = ColorEx(Rgb.ORANGE)
        On = ColorEx(Rgb.GREEN)
        Off = ColorEx(Rgb.RED, Animation.GATE_HALF_BEAT)
        Unlock = ColorEx(Rgb.PURPLE, Animation.GATE_HALF_BEAT)

def make_default_skin():
    return Skin(Colors)

