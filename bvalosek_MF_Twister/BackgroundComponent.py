from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

from Colors import *

class BackgroundComponent(ControlSurfaceComponent):
    """
    A component that simply shows colors on the LED lights
    """

    def __init__(self, colors = None, *a, **k):
        ControlSurfaceComponent.__init__(self, *a, **k)
        self._lights = None
        self._repeat_color = 'Background.Default'
        self._color_values = colors

    def set_lights(self, lights):
        self._lights = lights

    def update(self):
        ControlSurfaceComponent.update(self)
        if self.is_enabled():
            for idx, c in enumerate(self._lights or []):
                if not c:
                    continue
                elif self._color_values and len(self._color_values) > idx:
                    c.set_light(self._color_values[idx])
                elif self._repeat_color:
                    c.set_light(self._repeat_color)

