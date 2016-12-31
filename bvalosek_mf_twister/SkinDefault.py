from _Framework.ButtonElement import Color
from _Framework.Skin import Skin

from Colors import *

class Colors:
    class Device:
        Background = ColorEx(Rgb.BLUE)
        NotLocked = ColorEx(Rgb.GREEN)
        Locked = Strobe(Rgb.PURPLE, animation = 5)
        CanBank = Pulse(Rgb.TEAL, animation = 5)
        CantBank = ColorEx(Rgb.TEAL)

    class Mixer:
        SendBackground = ColorEx(Rgb.ORANGE)
        VolumeBackground = ColorEx(Rgb.PINK)

def make_default_skin():
    return Skin(Colors)
        
