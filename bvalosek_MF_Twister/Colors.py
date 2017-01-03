from _Framework.ButtonElement import Color

from consts import *

class ColorEx(Color):
    """
    Color always sends on button channel
    """
    def draw(self, interface):
        interface.send_value(self.midi_value, channel = BUTTON_CHANNEL, force = True)
        self._draw_animation(interface, 0)

    def _draw_animation(self, interface, value):
        interface.send_value(value, channel = ANIMATION_CHANNEL, force = True)
        pass

class AnimatedColor(ColorEx):
    def __init__(self, midi_value = 127, animation = 4, *a, **k):
        super(AnimatedColor, self).__init__(midi_value, *a, **k)
        self._animation = animation

    def draw(self, interface):
        ColorEx.draw(self, interface)

class Strobe(AnimatedColor):
    def draw(self, interface):
        ColorEx.draw(self, interface)
        self._draw_animation(interface, self._animation)

class Pulse(AnimatedColor):
    def draw(self, interface):
        ColorEx.draw(self, interface)
        self._draw_animation(interface, self._animation + 8)

class Rainbow(AnimatedColor):
    def draw(self, interface):
        ColorEx.draw(self, interface)
        self._draw_animation(interface, 127)

class Rgb:
    OFF = 0
    BLUE = 1
    TEAL = 20
    MINT = 40
    GREEN = 52
    YELLOW = 61
    ORANGE = 68
    RED = 85
    PINK = 100
    PURPLE = 110

