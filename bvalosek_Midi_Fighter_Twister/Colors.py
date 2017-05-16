from _Framework.ButtonElement import Color

from consts import *

class Rgb:
    OFF = 0
    BLUE = 1
    AZURE = 10
    TEAL = 20
    MINT = 40
    GREEN = 52
    YELLOW = 61
    ORANGE = 68
    RED = 85
    PINK_RED = 93
    PINK = 100
    FUCHSIA = 111
    PURPLE = 115

class Animation:
    NONE = 0

    GATE_8_BEATS = 1
    GATE_4_BEATS = 2
    GATE_2_BEATS = 3
    GATE_1_BEAT = 4
    GATE_HALF_BEAT = 5
    GATE_QUARTER_BEAT = 6
    GATE_EIGHTH_BEAT = 7
    GATE_SIXTEENTH_BEAT = 8

    PULSE_8_BEATS = 10
    PULSE_4_BEATS = 11
    PULSE_2_BEATS = 12
    PULSE_1_BEAT = 13
    PULSE_HALF_BEAT = 14
    PULSE_QUARTER_BEAT = 15
    PULSE_EIGHTH_BEAT = 16

    RAINBOW = 127

class Brightness:
    OFF = 17
    MIN = 18
    LOW = 25
    MID = 32
    MAX = 47

class ColorEx(Color):
    def __init__(self, midi_value = Rgb.BLUE, animation = Animation.NONE, *a, **k):
        super(ColorEx, self).__init__(midi_value, *a, **k)
        self._animation = animation

    def draw(self, interface):
        interface.send_value(self.midi_value, channel = BUTTON_CHANNEL, force = True)
        interface.send_value(self._animation, channel = BUTTON_ANIMATION_CHANNEL, force = True)
