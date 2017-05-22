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
        Lock = ColorEx(Rgb.BLUE, Animation.PULSE_2_BEATS)

        Unlock = ColorEx(Rgb.RED, Animation.GATE_HALF_BEAT)
        Select = ColorEx(Rgb.ORANGE, Animation.GATE_HALF_BEAT)

def make_default_skin():
    return Skin(Colors)

