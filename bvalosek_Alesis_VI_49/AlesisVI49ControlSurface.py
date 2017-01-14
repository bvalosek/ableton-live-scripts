from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.ControlSurface import ControlSurface
from _Framework.DeviceComponent import DeviceComponent
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.Layer import Layer
from _Framework.SliderElement import SliderElement
from _Framework.SubjectSlot import subject_slot
from _Framework.TransportComponent import TransportComponent

from bvalosek_common.SessionRecordingComponentEx import SessionRecordingComponentEx

from consts import *

def create_button(channel, cc):
    return ButtonElement(True, MIDI_CC_TYPE, channel, cc)

class AlesisVI49ControlSurface(ControlSurface):
    """
    Simple control script for the Alesis VI 49
    """

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        self._handle_track_change.subject = self.song().view
        with self.component_guard():
            self._setup_controls()
            self._setup_device()
            self._setup_strip()
            self._setup_transport()
            self._handle_track_change()

    @subject_slot('selected_track')
    def _handle_track_change(self):
        """Fired whenever the selected track has changed"""

        track = self.song().view.selected_track
        self._strip.set_track(track)

        # always select the first device when selecting a new track
        if track and len(track.devices):
            self.song().view.select_device(track.devices[0])

    def _setup_controls(self):
        """Create the element instances for the physical controls on the controller"""

        self._knobs = [
            SliderElement(
                msg_type = MIDI_CC_TYPE,
                channel = KNOB_CHANNEL,
                identifier = KNOB_CC_START + knob_index)
            for knob_index in range(KNOB_COUNT) ]

        self._record_button = create_button(TRANSPORT_CHANNEL, TRANSPORT_RECORD)
        self._loop_button = create_button(TRANSPORT_CHANNEL, TRANSPORT_LOOP)
        self._backward_button = create_button(TRANSPORT_CHANNEL, TRANSPORT_BACKWARD)
        self._forward_button = create_button(TRANSPORT_CHANNEL, TRANSPORT_FORWARD)
        self._stop_button = create_button(TRANSPORT_CHANNEL, TRANSPORT_STOP)
        self._play_button = create_button(TRANSPORT_CHANNEL, TRANSPORT_PLAY)

    def _setup_transport(self):
        self._transport = TransportComponent()
        self._transport.layer = Layer(
            play_button = self._play_button,
            stop_button = self._stop_button,
            tap_tempo_button = self._loop_button,
            seek_forward_button = self._forward_button,
            seek_backward_button = self._backward_button)
        self._session_record = SessionRecordingComponentEx()
        self._session_record.layer = Layer(record_button = self._record_button)

    def _setup_device(self):
        """Create a DeviceComponent to control macro knobs"""

        self._device = DeviceComponent()
        self.set_device_component(self._device)
        param_knobs = ButtonMatrixElement(rows = [self._knobs[0:8]])
        self._device.layer = Layer(parameter_controls = param_knobs)

    def _setup_strip(self):
        """Create a ChannelStrip to control the sends"""

        self._strip = ChannelStripComponent()
        send_knobs = ButtonMatrixElement(rows = [self._knobs[8:]])
        self._strip.layer = Layer(send_controls = send_knobs)

