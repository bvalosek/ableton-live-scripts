from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

class BackgroundComponent(ControlSurfaceComponent):
    """
    A nop component that we just clear everything. Set to a low-priority layer
    so that anything not mapped will get grabbed and cleared
    """

    def set_lights(self, lights):
        for light in lights:
            if light:
                light.set_light('DefaultButton.Off')

    def set_knobs(self, knobs):
        for knob in knobs:
            if knob:
                knob.send_value(0, force = True)
