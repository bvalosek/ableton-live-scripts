from _Framework.ControlSurface import ControlSurface
from _Framework.SliderElement import SliderElement
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.DeviceComponent import DeviceComponent

from consts import *

class AlesisVI49ControlSurface(ControlSurface):

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)

        with self.component_guard():
            self._setup_controls()
            self._setup_device()

    def _setup_controls(self):
        self._knobs = []
        for knob_index in range(KNOB_COUNT):
            self._knobs.append(SliderElement(
                msg_type = MIDI_CC_TYPE,
                channel = KNOB_CHANNEL,
                identifier = KNOB_CC_START + knob_index))

    def _setup_device(self):
        self._device = DeviceComponent()
        self.set_device_component(self._device)
