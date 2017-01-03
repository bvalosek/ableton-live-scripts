from _Framework.CompoundComponent import CompoundComponent
from _Framework.ChannelStripComponent import ChannelStripComponent

from Colors import *

class SendsComponent(CompoundComponent):

    def __init__(self, *a, **k):
        CompoundComponent.__init__(self, *a, **k)
        self._strip = ChannelStripComponent()

    def set_track(self, track):
        self._strip.set_track(track)
        self.update()

    def set_send_controls(self, controls):
        return self._strip.set_send_controls(controls)

    def set_volume_control(self, control):
        return self._strip.set_volume_control(control)

