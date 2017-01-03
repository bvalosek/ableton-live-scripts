from _Framework.CompoundComponent import CompoundComponent
from _Framework.ChannelStripComponent import ChannelStripComponent

from Colors import *

class SendsComponent(CompoundComponent):

    def __init__(self, *a, **k):
        CompoundComponent.__init__(self, *a, **k)
        self._strip = ChannelStripComponent()
        self._send_lights = None
        self._volume_light = None

    def set_track(self, track):
        self._strip.set_track(track)
        self.update()

    def set_send_lights(self, lights):
        self._send_lights = lights
        self.update()

    def set_send_controls(self, controls):
        return self._strip.set_send_controls(controls)

    def set_volume_control(self, control):
        return self._strip.set_volume_control(control)

    def set_volume_light(self, light):
        self._volume_light = light
        self.update()

    def update(self):
        CompoundComponent.update(self)
        for c in self._send_lights or []:
            c.set_light('Mixer.SendBackground')
        if self._volume_light:
            self._volume_light.set_light('Mixer.VolumeBackground')
