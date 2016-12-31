from __future__ import with_statement
import Live

from _Framework.ControlSurface import ControlSurface
from _Framework.SliderElement import SliderElement
from _Framework.ButtonElement import ButtonElement
from _Framework.InputControlElement import *
from _Framework.Layer import Layer
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.SubjectSlot import subject_slot_group

# our shit
from Twister16ParamDevice import Twister16ParamDevice
from Twister4UpDevice import Twister4UpDevice

# twister MIDI addresses
from consts import *

def to_matrix(buttons):
    return ButtonMatrixElement(rows = [buttons])

class TwisterControlSurface(ControlSurface):
    """DJ Tech Tools MIDI Fighter Twister Control Script"""

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            self._setup_controls()
            self._setup_bank_1()
            self.set_device_component(self.device16)

    def _setup_bank_1(self):
        """Bank one (main mode) will control 16 parameters (8 macro +
        hueristics) and other basic device controls
        """
        self.bank_1_layer = Layer(
            parameter_controls = to_matrix(self.knobs[0][:16]),
            parameter_buttons = to_matrix(self.buttons[0][:16]))
        self.device16 = Twister16ParamDevice()
        self.device16.layer = self.bank_1_layer

        # TODO: remove
        self.device16.log = self.log_message

    @subject_slot_group('value')
    def _on_button_press(self, value, button):
        """A button was pressed"""
        if not value: return
        index = [t for t in self.buttons[0]].index(button)

    def _setup_controls(self):
        """Create the instances of the physical controls for the Twister"""
        self.knobs = []
        self.buttons = []

        for bank_index in range(KNOB_BANK_COUNT):
            knobs = []
            buttons = []
            for knob_index in range(KNOBS_PER_BANK):
                knob = SliderElement(
                    MIDI_CC_TYPE, KNOB_CHANNEL,
                    bank_index * KNOBS_PER_BANK + ENCODER_START + knob_index)
                knobs.append(knob)
                button = ButtonElement(
                    True, MIDI_CC_TYPE, BUTTON_CHANNEL,
                    bank_index * KNOBS_PER_BANK + ENCODER_START + knob_index)
                buttons.append(button)
            self.knobs.append(knobs)
            self.buttons.append(buttons)

        # listen to all buttons
        self._on_button_press.replace_subjects(to_matrix(self.buttons[0][:16]))

