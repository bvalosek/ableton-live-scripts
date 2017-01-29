from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.Layer import Layer
from _Framework.MixerComponent import MixerComponent
from _Framework.ModesComponent import LayerMode
from _Framework.SubjectSlot import subject_slot, subject_slot_group

from consts import *
from Colors import *

from bvalosek_common.MetronomeComponent import MetronomeComponent

from BackgroundComponent import BackgroundComponent
from ButtonElementEx import ButtonElementEx
from DeviceComponentEx import DeviceComponentEx
from MixerComponentEx import MixerComponentEx, ChannelStripComponentEx
from ModesComponentEx import ModesComponentEx
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
            self._setup_background()
            self._setup_device()
            self._setup_mixer()
            self._setup_metronome()
            self._setup_modes()
            self._handle_track_change()

    @subject_slot('selected_track')
    def _handle_track_change(self):
        track = self.song().view.selected_track
        self._select_device_on_track(track)

        # only change sends if the device isnt locked -- keeps strip in sync
        # with the locked device
        if not self._device._locked_to_device:
            self._strip.set_track(track)

    def _select_device_on_track(self, track):
        if not track or not len(track.devices):
            return
        device = track.devices[0]
        self._device.set_device(device)

    def _setup_background(self):
        background = BackgroundComponent()
        background.layer = Layer(priority = -100, knobs = self._knobs, lights = self._buttons)

    def _setup_device(self):
        self._device = DeviceComponentEx()
        self.set_device_component(self._device)
        self._adhoc_devices = [ DeviceComponentEx() for n in range(4) ]
        for device in self._adhoc_devices:
            device.set_lock_callback(lambda device = device: self._lock_device(device))

    def _lock_device(self, device):
        focused = self.song().appointed_device
        current = device._device
        locked = device._locked_to_device

        if not locked:
            device.set_lock_to_device(True, focused)
            self.show_message('Locked ' + focused.name + ' to adhoc device')
        else:
            device.set_lock_to_device(False, None)
            device.set_device(focused)
            self.show_message('Adhoc device unlocked')

    def _setup_metronome(self):
        self._metronome = MetronomeComponent()

    def _setup_mixer(self):
        self._strip = ChannelStripComponentEx()
        self._mixer = MixerComponentEx(num_returns = 8)

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
        self._setup_main_mode()
        self._setup_adhoc_mode()
        self._modes.layer = Layer(priority = 10,
            adhoc_mode_button = self._buttons.get_button(0, 0),
            main_mode_button = self._buttons.get_button(1, 0))
        self._modes.selected_mode = 'adhoc_mode'

    def _setup_adhoc_mode(self):
        device_layers = [ Layer(
            lock_button = self._buttons.get_button(n, 3),
            on_off_button = self._buttons.get_button(n, 2),
            param_offset_button = self._buttons.get_button(n, 1),
            parameter_controls = self._knobs.submatrix[n, 3::-1]) for n in range(4) ]

        self._modes.add_mode('adhoc_mode', [
            lambda: self.show_message('Switched to ad-hoc device mode') ] + [
            LayerMode(self._adhoc_devices[n], device_layers[n]) for n in range(4) ])

    def _setup_main_mode(self):
        strip_layer = Layer(
            volume_control = self._knobs.get_button(3, 0),
            arm_button = self._buttons.get_button(3, 0),
            send_controls = self._knobs.submatrix[:, 1])
        mixer_layer = Layer(
            prehear_volume_control = self._knobs.get_button(0, 0),
            return_track_select_buttons = self._buttons.submatrix[:, 1])
        device_layer = Layer(
            on_off_button = self._buttons.get_button(3, 3),
            parameter_controls = self._knobs.submatrix[:, 2:],
            lock_button = self._buttons.get_button(2, 3))
        metronome_layer = Layer(
            lights = self._buttons.submatrix[:, 2])

        device_bg = BackgroundComponent(color = 'Device.Background')
        device_bg_layer = Layer(priority = -10,
            lights = self._buttons.submatrix[:, 2:])

        self._modes.add_mode('main_mode', [
            lambda: self.show_message('Switched to main mode'),
            LayerMode(self._strip, strip_layer),
            LayerMode(self._mixer, mixer_layer),
            LayerMode(self._metronome, metronome_layer),
            LayerMode(device_bg, device_bg_layer),
            LayerMode(self._device, device_layer) ])

