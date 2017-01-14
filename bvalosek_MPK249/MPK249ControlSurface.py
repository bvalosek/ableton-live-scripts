from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.Layer import Layer
from _Framework.SliderElement import SliderElement
from _Framework.TransportComponent import TransportComponent
from _Framework.SessionRecordingComponent import SessionRecordingComponent

from bvalosek_common.SessionRecordingComponentEx import SessionRecordingComponentEx
from bvalosek_common.MixerComponentEx import MixerComponentEx
from bvalosek_common.MetronomeComponent import MetronomeComponent

from consts import *

class MPK249ControlSurface(ControlSurface):
    """
    Custom control script for the Akai MPK249 Keyboard
    """

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            self._setup_controls()
            self._setup_mixer()
            self._setup_transport()
            self._setup_transport()

    def _setup_controls(self):
        faders = [
            SliderElement(
                msg_type = MIDI_CC_TYPE,
                channel = FADER_CHANNEL,
                identifier = FADER_CC_START + idx) for idx in range(FADER_COUNT) ]
        buttons = [
            ButtonElement(
                is_momentary = False,
                msg_type = MIDI_CC_TYPE,
                channel = BUTTON_CHANNEL,
                identifier = BUTTON_CC_START + idx) for idx in range(BUTTON_COUNT) ]
        self._faders = ButtonMatrixElement([ faders ])
        self._buttons = ButtonMatrixElement([ buttons ])

        self._backward_button = ButtonElement(True, MIDI_CC_TYPE, TRANSPORT_CHANNEL, TRANSPORT_BACKWARD)
        self._forward_button = ButtonElement(True, MIDI_CC_TYPE, TRANSPORT_CHANNEL, TRANSPORT_FORWARD)
        self._stop_button = ButtonElement(True, MIDI_CC_TYPE, TRANSPORT_CHANNEL, TRANSPORT_STOP)
        self._play_button = ButtonElement(True, MIDI_CC_TYPE, TRANSPORT_CHANNEL, TRANSPORT_PLAY)
        self._record_button = ButtonElement(True, MIDI_CC_TYPE, TRANSPORT_CHANNEL, TRANSPORT_RECORD)
        self._loop_button = ButtonElement(True, MIDI_CC_TYPE, TRANSPORT_CHANNEL, TRANSPORT_LOOP)

    def _setup_mixer(self):
        self._mixer = MixerComponentEx(num_tracks = FADER_COUNT)
        self._mixer.layer = Layer(
            volume_controls = self._faders,
            arm_buttons = self._buttons)

    def _setup_transport(self):
        self._transport = TransportComponent()
        self._transport.layer = Layer(
            play_button = self._play_button,
            stop_button = self._stop_button,
            seek_forward_button = self._forward_button,
            seek_backward_button = self._backward_button,
            tap_tempo_button = self._loop_button)
        self._session_record = SessionRecordingComponentEx()
        self._session_record.layer = Layer(record_button = self._record_button)
