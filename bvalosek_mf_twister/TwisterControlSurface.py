from __future__ import with_statement
import Live

from _Framework.ControlSurface import ControlSurface
from _Framework.SliderElement import SliderElement
from _Framework.InputControlElement import *
from _Framework.Layer import Layer
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement

from TwisterDeviceComponent import TwisterDeviceComponent

from consts import *

def to_matrix(buttons):
    return ButtonMatrixElement(rows = [buttons])

class TwisterControlSurface(ControlSurface):
    """
    DJ Tech Tools MIDI Fighter Twister Control Script
    """

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)

        with self.component_guard():
            self._setup_controls()
            self._setup_device()
            self._setup_sibling_devices()

    def _setup_sibling_devices(self):
        """
        Second bank will be 4 mini device components
        """
        self.sibling_devices = [TwisterDeviceComponent() for n in range(4)]
        for n, comp in enumerate(self.sibling_devices):
            a = n * 4
            b = a + 4
            layer = Layer(
                parameter_controls = to_matrix(self.knobs[0][a:b]),
                parameter_buttons  = to_matrix(self.buttons[0][a:b]),)
            comp.layer = layer
            comp.on_off_index = 0
            comp.hide_sibling_devices_index = 1

        self.device.set_sibling_devices(self.sibling_devices)
        self.device.set_sibling_devices_enabled(False)

    def _setup_device(self):
        """
        First bank as chain mixer + macro knobs
        """
        self.device_layer = Layer(
            chain_volume_sliders = to_matrix(self.knobs[0][:8]),
            chain_select_buttons = to_matrix(self.buttons[0][:8]),
            parameter_controls   = to_matrix(self.knobs[0][8:]),
            parameter_buttons    = to_matrix(self.buttons[0][8:]),)
        self.device = TwisterDeviceComponent()
        self.device.layer = self.device_layer
        self.device.on_off_index = 0
        self.device.show_sibling_devices_index = 1

        # Blue hand
        self.set_device_component(self.device)

    def _setup_controls(self):
        """ Create the instances of the physical controls for the Twister """

        # 2D array for bank -> 16x
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

