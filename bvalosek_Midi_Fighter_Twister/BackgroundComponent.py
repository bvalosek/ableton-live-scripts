from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

from consts import *

class BackgroundComponent(ControlSurfaceComponent):
    """
    A nop component that we just clear everything. Set to a low-priority layer
    so that anything not mapped will get grabbed and cleared
    """

    def __init__(self, raw = None, color = 'DefaultButton.Off', *a, **k):
        super(BackgroundComponent, self).__init__(*a, **k)
        self._color = color
        self._raw = raw

        self._lights = None
        self._knobs = None

    def set_raw(self, raw):
        self._raw = raw
        self.update()

    def set_lights(self, lights):
        self._lights = lights
        self.update()

    def set_knobs(self, knobs):
        self._knobs = knobs
        self.update()

    def on_enabled_changed(self):
        self.update()

    def update(self):
        if self.is_enabled():
            for index, light in enumerate(self._lights or []):
                if light:
                    if self._raw:
                        self._raw[index].draw(light)
                    else:
                        light.set_light(self._color)
            for knob in self._knobs or []:
                if knob:
                    knob.send_value(0, force = True)
                    knob.send_value(65, channel = KNOB_ANIMATION_CHANNEL, force = True)
