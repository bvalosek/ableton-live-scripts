from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.Layer import Layer
from _Framework.MixerComponent import MixerComponent
from _Framework.ModesComponent import ModesComponent, LayerMode
from _Framework.SubjectSlot import subject_slot, subject_slot_group

from consts import *
from Colors import *

from ButtonElementEx import ButtonElementEx
from DeviceComponentEx import DeviceComponentEx
from MixerComponentEx import ChannelStripComponentEx
from SendsComponent import SendsComponent
from SkinDefault import make_default_skin
from SliderElementEx import SliderElementEx

def to_matrix(buttons):
    return ButtonMatrixElement(rows = [buttons])

class TwisterControlSurface(ControlSurface):

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)

        self._handle_track_change.subject = self.song().view

        with self.component_guard():
            self._skin = make_default_skin()
            self._setup_controls()
            self._setup_device()
            self._setup_strip()
            self._setup_modes()
            self._handle_track_change()

    @subject_slot('selected_track')
    def _handle_track_change(self):
        track = self.song().view.selected_track
        self._select_device_on_track(track)

        # only change sends if the device isnt locked
        if not self._device._locked_to_device:
            self._strip.set_track(track)

    def _select_device_on_track(self, track):
        if not track or not len(track.devices):
            return
        device = track.devices[0]

        # if its a drum rack without macros, try to set the device to chain
        # instead in order to have the focus be on the selected / last played
        # pad's chain
        rack = device.can_have_drum_pads
        if rack and not device.has_macro_mappings and len(device.chains) > 0:
            chain = device.view.selected_chain or device.chains[0]
            if len(chain.devices):
                device = chain.devices[0]
        self._device.set_device(device)

    def _setup_device(self):
        self._device = DeviceComponentEx()
        self.set_device_component(self._device)
        self._device_selection_follows_track_selection = True

    def _setup_strip(self):
        self._strip = ChannelStripComponentEx()

    def _setup_controls(self):
        self._knobs = []
        self._buttons = []
        for knob_index in range(16):
            knob = SliderElementEx(
                    msg_type = MIDI_CC_TYPE,
                    channel = KNOB_CHANNEL,
                    identifier = knob_index)
            button = ButtonElementEx(
                    is_momentary = True,
                    msg_type = MIDI_CC_TYPE,
                    channel = BUTTON_CHANNEL,
                    identifier = knob_index,
                    skin = self._skin)
            self._knobs.append(knob)
            self._buttons.append(button)

    def _setup_modes(self):
        self._modes = ModesComponent()
        self._setup_main_mode()
        self._setup_sixteen_param_mode()
        self._setup_mixer_mode()
        self._modes.selected_mode = 'main_mode'
        self._modes.layer = Layer(priority = 10,
            main_mode_button = self._buttons[12],
            sixteen_param_mode_button = self._buttons[13],
            mixer_mode_button = self._buttons[14])

    def _setup_main_mode(self):
        device_bg = Layer(priority = -10,
            background_lights = to_matrix(self._buttons[0:8]))
        device_mode = LayerMode(self._device, device_bg + Layer(
            parameter_controls = to_matrix(self._knobs[0:8]),
            lock_button = self._buttons[3]))

        strip_bg = Layer(priority = -10,
            send_background_lights = to_matrix(self._buttons[8:15]),
            volume_background_light = self._buttons[15])
        strip_mode = LayerMode(self._strip, strip_bg + Layer(
            volume_control = self._knobs[15],
            send_controls = to_matrix(self._knobs[8:15])))

        self._modes.add_mode('main_mode', [ device_mode, strip_mode])

    def _setup_sixteen_param_mode(self):
        device_bg = Layer(priority = -10,
            background_lights = to_matrix(self._buttons))
        device_mode = LayerMode(self._device, device_bg + Layer(
            parameter_controls = to_matrix(self._knobs),
            bank_prev_button = self._buttons[5],
            bank_next_button = self._buttons[6],
            lock_button = self._buttons[3]))

        self._modes.add_mode('sixteen_param_mode', device_mode)

    def _setup_mixer_mode(self):
        mixer = MixerComponent(num_returns = 7, is_enabled = False)

        strips = [ LayerMode(
            mixer.return_strip(x),
            Layer(select_button = self._buttons[x])) for x in range(7) ]

        self._modes.add_mode('mixer_mode', strips)

