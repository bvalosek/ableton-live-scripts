from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.Layer import Layer
from _Framework.ModesComponent import LayerMode

from consts import *
from Colors import *

from BackgroundComponent import BackgroundComponent
from ButtonElementEx import ButtonElementEx
from ModesComponentEx import ModesComponentEx
from SkinDefault import make_default_skin
from SliderElementEx import SliderElementEx

class TwisterControlSurface(ControlSurface):
    """
    Custom control for the DJ Tech Tools Midi Fighter Twister controller
    """

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)

        with self.component_guard():
            self._skin = make_default_skin()
            self._setup_controls()
            self._setup_background()
            self._setup_modes()

    def _setup_background(self):
        background = BackgroundComponent()
        background.layer = Layer(priority = -100, knobs = self._knobs, lights = self._buttons)

    def _setup_controls(self):
        knobs = [ [ self._make_knob(row, col) for col in range(4) ] for row in range(4) ]
        buttons = [ [ self._make_button(row, col) for col in range(4) ] for row in range(4) ]
        self._knobs = ButtonMatrixElement(knobs)
        self._buttons = ButtonMatrixElement(buttons)

    def _make_knob(self, row, col):
        return SliderElementEx(
            msg_type = MIDI_CC_TYPE,
            channel = KNOB_CHANNEL,
            identifier = row * 4 + col)

    def _make_button(self, row, col):
        return ButtonElementEx(
            msg_type = MIDI_CC_TYPE,
            channel = BUTTON_CHANNEL,
            identifier = row * 4 + col,
            is_momentary = True,
            skin = self._skin)

    def _setup_modes(self):
        self._modes = ModesComponentEx()
        mappings = dict()
        for n in range(4):
            self._create_page(n)
            mappings["page{}_mode_button".format(n + 1)] = self._buttons.get_button(n, 0)
        self._modes.layer = Layer(priority = 10, **mappings)
        self._modes.selected_mode = 'page1_mode'

    def _create_page(self, index):
        page_num = index + 1
        msg = lambda: self.show_message("Switched to page {}".format(page_num))
        mode_name = "page{}_mode".format(page_num)
        self._modes.add_mode(mode_name, [ msg ])

