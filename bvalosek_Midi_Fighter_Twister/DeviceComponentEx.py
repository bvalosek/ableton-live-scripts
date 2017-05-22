from _Framework.CompoundComponent import CompoundComponent
from _Framework.DeviceComponent import DeviceComponent
from _Framework.Layer import Layer
from _Framework.ModesComponent import LayerMode, ComponentMode
from _Framework.ModesComponent import ModesComponent
from _Framework.SubjectSlot import subject_slot_group, subject_slot
from ableton.v2.base import liveobj_valid

from random import randint

from BackgroundComponent import BackgroundComponent
from Colors import *
from MenuComponent import MenuComponent

class _DeviceComponent(DeviceComponent):
    def __init__(self, log = None, *a, **k):
        super(_DeviceComponent, self).__init__(*a, **k)
        self.log = log

class DeviceComponentEx(CompoundComponent):
    """
    Extended DeviceComponent for the Midi Fighter Twister
    """

    def __init__(self, log = None, *a, **k):
        super(DeviceComponentEx, self).__init__(*a, **k)
        self.log = log

        self._knobs = None
        self._buttons = None

        self._setup_components()
        self._setup_background()
        self._setup_modes()

    def _setup_components(self):
        self._device = self.register_component(_DeviceComponent(log = self.log, is_enabled = False))
        self._modes = self.register_component(ModesComponent())
        self._background = self.register_component(BackgroundComponent(color = 70, is_enabled = False))

        empty_actions = [
            ('Device.Lock', self._lock_device, None),
            (None, None, None),
            (None, None, None),
            (None, None, None) ]
        self._empty = self.register_component(MenuComponent(
            actions = empty_actions,
            is_enabled = False))

        device_actions = [
            (None, None, None),
            (None, None, None),
            (None, None, None),
            (None, lambda: self._modes.push_mode('menu'), None) ]
        self._device_buttons = self.register_component(MenuComponent(
            actions = device_actions,
            enable_lights = False,
            is_enabled = False))

        menu_actions = [
            ('Device.Unlock', lambda: self._unlock_device(), None),
            (None, None, None),
            ('Device.Select', lambda: self._select_device(), None),
            (None, None, lambda: self._modes.pop_mode('menu')) ]
        self._menu = self.register_component(MenuComponent(
            actions = menu_actions,
            is_enabled = False))

    def _setup_background(self):
        color = randint(1, 127)
        self._background.set_raw([ ColorEx(color) for n in range(4) ])

    def _setup_modes(self):
        self._modes.add_mode('empty', [ ComponentMode(self._empty) ])
        self._modes.add_mode('device', [
            ComponentMode(self._device_buttons),
            ComponentMode(self._device),
            ComponentMode(self._background) ])
        self._modes.add_mode('menu', [ ComponentMode(self._menu) ])

        self._modes.selected_mode = 'empty';

    def set_knobs(self, knobs):
        self._knobs = knobs
        self._device.set_parameter_controls(knobs)
        self.update();

    def set_buttons(self, buttons):
        self._buttons = buttons
        self._background.set_lights(buttons)
        self._empty.set_buttons(buttons)
        self._device_buttons.set_buttons(buttons)
        self._menu.set_buttons(buttons)
        if buttons == None: self._modes.pop_mode('menu')
        self.update();

    def update(self):
        super(DeviceComponentEx, self).update()
        self._check_device()

    def _lock_device(self):
        focused = self.song().appointed_device
        self._device.set_lock_to_device(True, focused)
        self._modes.push_mode('device')
        self.update()

    def _unlock_device(self):
        self._device.set_lock_to_device(False, None)
        self._modes.pop_mode('device')
        self._modes.pop_mode('menu')
        self.update()

    def _select_device(self):
        self.song().appointed_device = self._device._device
        self.update()

    def _check_device(self):
        d = self._device._device
        if liveobj_valid(d): return
        self._device.set_lock_to_device(False, None)
        self._modes.pop_mode('menu')
        self._modes.pop_mode('device')

