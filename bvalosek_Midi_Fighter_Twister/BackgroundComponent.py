from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

class BackgroundComponent(ControlSurfaceComponent):
    """
    A nop component that we just clear everything. Set to a low-priority layer
    so that anything not mapped will get grabbed and cleared
    """

    def __init__(self, color = 'DefaultButton.Off', *a, **k):
        super(BackgroundComponent, self).__init__(*a, **k)
        self._color = color

    def set_lights(self, lights):
        for light in lights or []:
            if light:
                light.set_light(self._color)

    def set_knobs(self, knobs):
        for knob in knobs or []:
            if knob:
                knob.send_value(0, force = True)
