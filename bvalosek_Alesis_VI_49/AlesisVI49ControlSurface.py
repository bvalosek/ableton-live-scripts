from _Framework.ControlSurface import ControlSurface
from _Framework.SliderElement import SliderElement
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.DeviceComponent import DeviceComponent
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.Layer import Layer
from _Framework.SubjectSlot import subject_slot

from consts import *

class AlesisVI49ControlSurface(ControlSurface):

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)

        self._handle_track_change.subject = self.song().view

        with self.component_guard():
            self._setup_controls()
            self._setup_device()
            self._setup_strip()
            self._handle_track_change()

    @subject_slot('selected_track')
    def _handle_track_change(self):
        track = self.song().view.selected_track
        self._strip.set_track(track)

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
        param_knobs = ButtonMatrixElement(rows = [self._knobs[0:8]])
        self._device.layer = Layer(parameter_controls = param_knobs)

    def _setup_strip(self):
        self._strip = ChannelStripComponent()
        send_knobs = ButtonMatrixElement(rows = [self._knobs[8:]])
        self._strip.layer = Layer(send_controls = send_knobs)
