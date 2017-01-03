from _Framework.ButtonElement import Color
from _Framework.Skin import Skin

from Colors import *

class Colors:
    class Background:
        Default = ColorEx(Rgb.BLUE)
        Device = ColorEx(Rgb.BLUE)
        Sends = ColorEx(Rgb.ORANGE)
        Volume = ColorEx(Rgb.PINK)

    class DefaultButton:
        On = ColorEx(Rgb.GREEN)
        Off = ColorEx(Rgb.RED)
        Disabled = ColorEx(Rgb.OFF)

    class Device:
        NotLocked = ColorEx(Rgb.GREEN)
        Locked = Strobe(Rgb.PURPLE, animation = 5)
        CanBank = Pulse(Rgb.TEAL, animation = 5)
        CantBank = ColorEx(Rgb.TEAL)

def make_default_skin():
    return Skin(Colors)

