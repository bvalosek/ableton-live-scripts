from __future__ import with_statement
import Live

from _Framework.InputControlElement import *
from _Framework.ControlSurface import ControlSurface
from _Framework.ButtonElement import ButtonElement
from _Framework.SliderElement import SliderElement
from _Framework.EncoderElement import EncoderElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ComboElement import ComboElement
from _Framework.SubjectSlot import subject_slot
from _Framework.Layer import Layer

from _Framework.TransportComponent import TransportComponent

from bvalosek_common.MixerComponentEx import MixerComponentEx

from consts import *

class MPK249ControlSurface(ControlSurface):
    """
    Akai MPK249 Control Script
    """

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)

        with self.component_guard():
            self._setup_controls()
            self._setup_modes()
            self._setup_mixer()
            self._setup_transport()

    def _setup_modes(self):
        """ Map mode buttons to handlers """
        self._on_shift.subject = self.shift_button

    @subject_slot('value')
    def _on_shift(self, value):
        """ Toggle the active layers whenever holding the shift button """
        if value:
            self.mixer.layer = self.mixer_shift_layer
        else:
            self.mixer.layer = self.mixer_layer

    def _setup_mixer(self):
        """ Build component and layers used by the mixer """
        self.mixer_layer = Layer(
            pan_controls = self.encoders[0],
            volume_controls = self.sliders[0],
            track_select_buttons = self.buttons[0])
        self.mixer_shift_layer = Layer(
            send_controls = self.encoders[0],
            volume_controls = self.sliders[0],
            arm_buttons = self.buttons[0])

        self.mixer = MixerComponentEx(NUM_OF_TRACKS)
        self.mixer.layer = self.mixer_layer

    def _setup_transport(self):
        """ Build component and layers used by the transport """
        layer = Layer(
            play_button = self.play_button,
            stop_button = self.stop_button,
            seek_forward_button = self.forward_button,
            seek_backward_button = self.backward_button,
            loop_button = self.loop_button)

        self.transport = TransportComponent()
        self.transport.layer = layer

    def _setup_controls(self):
        """ Create all the instances of the physical controls on the MPK """
        self.play_button = ButtonElement(
                True, MIDI_CC_TYPE, TRANSPORT_MIDI_CHANNEL, PLAY_BUTTON)
        self.stop_button = ButtonElement(
                True, MIDI_CC_TYPE, TRANSPORT_MIDI_CHANNEL, STOP_BUTTON)
        self.loop_button = ButtonElement(
                True, MIDI_CC_TYPE, TRANSPORT_MIDI_CHANNEL, LOOP_BUTTON)
        self.forward_button = ButtonElement(
                True, MIDI_CC_TYPE, TRANSPORT_MIDI_CHANNEL, FORWARD_BUTTON)
        self.backward_button = ButtonElement(
                True, MIDI_CC_TYPE, TRANSPORT_MIDI_CHANNEL, BACKWARD_BUTTON)
        self.record_button = ButtonElement(
                True, MIDI_CC_TYPE, TRANSPORT_MIDI_CHANNEL, REC_BUTTON)

        self.buttons = []
        self.encoders = []
        self.sliders = []
        for cc_start in BUTTON_STARTS:
            buttons = [ButtonElement(
                False, MIDI_CC_TYPE,
                MIDI_CHANNEL, cc_start + n) for n in range(8)]
            self.buttons.append(ButtonMatrixElement(rows = [buttons]))
        for cc_start in ENCORDER_STARTS:
            encoders = [EncoderElement(
                MIDI_CC_TYPE, MIDI_CHANNEL, cc_start + n,
                Live.MidiMap.MapMode.relative_two_compliment) for n in range(8)]
            self.encoders.append(ButtonMatrixElement(rows = [encoders]))
        for cc_start in SLIDER_STARTS:
            sliders = [SliderElement(
                MIDI_CC_TYPE, MIDI_CHANNEL, cc_start + n) for n in range(8)]
            self.sliders.append(ButtonMatrixElement(rows = [sliders]))

        self.shift_button = self.record_button

