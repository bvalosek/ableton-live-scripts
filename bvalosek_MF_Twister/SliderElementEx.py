from _Framework.SliderElement import SliderElement

from consts import *

class SliderElementEx(SliderElement):

    def connect_to(self, param):
        super(SliderElementEx, self).connect_to(param)
        self.send_value(95, channel = KNOB_ANIMATION_CHANNEL, force = True)

    def release_parameter(self, *a, **k):
        super(SliderElementEx, self).release_parameter(*a, **k)
        self.send_value(0, force = True)
        self.send_value(65, channel = KNOB_ANIMATION_CHANNEL, force = True)

