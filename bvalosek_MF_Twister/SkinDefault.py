from _Framework.ButtonElement import Color
from _Framework.Skin import Skin

from Colors import *

class Colors:
    class Background:
        Default = ColorEx(Rgb.BLUE)
        Sends = ColorEx(Rgb.ORANGE)

    class Modes:
        Selected = ColorEx(Rgb.GREEN, Animation.PULSE_1_BEAT)
        NotSelected = ColorEx(Rgb.GREEN, Brightness.LOW)

    class DefaultButton:
        On = ColorEx(Rgb.GREEN)
        Disabled = ColorEx(Rgb.GREEN, Brightness.LOW)
        Off = ColorEx(Rgb.OFF, Brightness.OFF)

    class Mixer:
        ArmOn = ColorEx(Rgb.RED, Animation.GATE_QUARTER_BEAT)
        ArmOff = ColorEx(Rgb.YELLOW)
        CantArm = ColorEx(Rgb.PURPLE)
        Track = ColorEx(Rgb.ORANGE)
        TrackSelected = ColorEx(Rgb.YELLOW, Animation.GATE_QUARTER_BEAT)
        NoTrack = ColorEx(Rgb.ORANGE, Brightness.LOW)

    class Metronome:
        Beat = ColorEx(Rgb.RED)
        Background = ColorEx(Rgb.BLUE)

    class Device:
        On = ColorEx(Rgb.MINT)
        Off = ColorEx(Rgb.RED, Animation.GATE_QUARTER_BEAT)
        NotLocked = ColorEx(Rgb.TEAL)
        Locked = ColorEx(Rgb.FUCHSIA, Animation.GATE_QUARTER_BEAT)
        CanBank = ColorEx(Rgb.TEAL)
        CantBank = ColorEx(Rgb.TEAL, Brightness.LOW)
        ActiveBank = ColorEx(Rgb.PINK_RED, Animation.GATE_QUARTER_BEAT)
        InactiveBank = ColorEx(Rgb.FUCHSIA)
        NoBank = ColorEx(Rgb.BLUE)
        Background = ColorEx(Rgb.BLUE)
        OffsetDisabled = ColorEx(Rgb.BLUE)
        OffsetEnabled = ColorEx(Rgb.ORANGE)

def make_default_skin():
    return Skin(Colors)

