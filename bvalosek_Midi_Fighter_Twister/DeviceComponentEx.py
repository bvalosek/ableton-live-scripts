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

class SnapModes:
    HALF = 'Device.HalfSnap'
    REVERSE_HALF = 'Device.ReverseHalfSnap'
    FULL = 'Device.FullSnap'

class _DeviceComponent(DeviceComponent):
    def __init__(self, log = None, *a, **k):
        super(_DeviceComponent, self).__init__(*a, **k)
        self.log = log
        self._param_offset = False

    def set_param_offset(self, value):
        self._param_offset = value
        self.update()

    def toggle_param_offset(self):
        self.set_param_offset(not self._param_offset)

    def _current_bank_details(self):
        """ Override default behavior to factor in param_offset """
        bank_name, bank = super(_DeviceComponent, self)._current_bank_details()
        if bank and len(bank) > 4 and self._param_offset:
            bank = bank[4:]
        return (bank_name, bank)

    def get_parameter(self, idx = 0):
        _, bank = self._current_bank_details()
        if idx >= len(bank): return None
        return bank[idx]


class DeviceComponentEx(CompoundComponent):
    """
    Extended DeviceComponent for the Midi Fighter Twister
    """

    next_color = 1

    def __init__(self, schedule_message, log = None, top_buttons = None, *a, **k):
        super(DeviceComponentEx, self).__init__(*a, **k)
        self.log = log
        self.schedule_message = schedule_message

        self._knobs = None
        self._buttons = None
        self._top_buttons = top_buttons

        self._snap_modes = [ SnapModes.REVERSE_HALF ] * 8

        self._param_values = [ None ] * 8
        self._param_down_values = [ None ] * 8

        self._setup_background()
        self._setup_device()
        self._setup_empty_menu()
        self._setup_device_menu()
        self._setup_active_menu()
        self._setup_top_menu()
        self._setup_modes()

    def _setup_empty_menu(self):
        actions = [
            ('Device.Lock', self._lock_device, None),
            ('Device.LockOffset', lambda: self._lock_device(True), None),
            (None, None, None),
            (None, None, None) ]
        self._empty = self.register_component(MenuComponent(
            actions = actions,
            is_enabled = False))

    def _setup_device_menu(self):
        fn = lambda n, v: lambda: self._on_param(n, v)
        actions = [
            (None, fn(n, True), fn(n, False)) for n in range(3) ] + [
            (None, lambda: self._modes.push_mode('menu'), None) ]
        self._device_buttons = self.register_component(MenuComponent(
            actions = actions,
            enable_lights = False,
            is_enabled = False))

    def _setup_active_menu(self):
        actions = [
            ('Device.Unlock', lambda: self._unlock_device(), None),
            ('Device.NormalParams', lambda: self._toggle_param_offset(), None),
            ('Device.Select', lambda: self._select_device(), None),
            ('Device.MenuActive', None, lambda: self._modes.pop_mode('menu')) ]
        self._menu = self.register_component(MenuComponent(
            actions = actions,
            is_enabled = False))

    def _setup_top_menu(self):
        fn = lambda n: lambda: self._on_toggle_snap_mode(n)
        actions = [
            (self._snap_modes[n], fn(n), None) for n in range(3) ] + [
            ('DefaultButton.Off', None, None) ]
        self._top_menu = self.register_component(MenuComponent(
            layer = Layer(priority = 20, buttons = self._top_buttons),
            actions = actions,
            is_enabled = False))

    def _setup_background(self):
        self._background = self.register_component(BackgroundComponent(
            is_enabled = False))
        color = DeviceComponentEx.next_color
        DeviceComponentEx.next_color = (color + 31) % 127
        self._background.set_raw([ ColorEx(color) for n in range(4) ])

    def _setup_device(self):
        self._device = self.register_component(_DeviceComponent(
            log = self.log,
            is_enabled = False))

    def _setup_modes(self):
        self._modes = self.register_component(ModesComponent())
        self._modes.add_mode('empty', [ ComponentMode(self._empty) ])
        self._modes.add_mode('device', [
            ComponentMode(self._device_buttons),
            ComponentMode(self._device),
            ComponentMode(self._background) ])
        self._modes.add_mode('menu', [
            ComponentMode(self._top_menu),
            ComponentMode(self._menu) ])
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

    def _toggle_param_offset(self):
        self._device.toggle_param_offset()
        self._update_menu_actions()

    def _update_menu_actions(self):
        pcolor = 'Device.NormalParams' if not self._device._param_offset else 'Device.OffsetParams'
        self._menu.update_action(1, (pcolor, self._toggle_param_offset, None))

    def _lock_device(self, offset = False):
        focused = self.song().appointed_device
        self._device.set_param_offset(offset)
        self._device.set_lock_to_device(True, focused)
        self._modes.push_mode('device')
        self._update_menu_actions()
        self.update()

    def _unlock_device(self):
        self._device.set_lock_to_device(False, None)
        self._modes.pop_mode('device')
        self._modes.pop_mode('menu')
        self._device.set_param_offset(False)
        self.update()

    def _select_device(self):
        self.song().view.select_device(self._device._device)
        self.update()

    def _on_param(self, idx, value = True):
        snap_index = idx + (4 if self._device._param_offset else 0)
        mode = self._snap_modes[snap_index]
        if mode == SnapModes.HALF:
            self._on_param_half_snap(idx, value)
        elif mode == SnapModes.REVERSE_HALF:
            self._on_param_reverse_half_snap(idx, value)
        elif mode == SnapModes.FULL:
            self._on_param_full_snap(idx, value)

    def _on_param_reverse_half_snap(self, idx, value):
        """ Restore on rising edge, cache on falling edge """
        param = self._device.get_parameter(idx)
        cached = self._param_values[idx]
        if value:
            if cached is not None: self._set_parameter_value(param, cached)
        else:
            self._param_values[idx] = param.value

    def _on_param_half_snap(self, idx, value):
        """ Cache on rising edge, restore on falling edge """
        param = self._device.get_parameter(idx)
        cached = self._param_values[idx]
        if value:
            self._param_values[idx] = param.value
        else:
            if cached is not None: self._set_parameter_value(param, cached)

    def _on_param_full_snap(self, idx, value):
        """ Cache and restore on rising and falling edge"""
        param = self._device.get_parameter(idx)
        cached = self._param_values[idx]
        self._param_values[idx] = param.value
        if cached is not None: self._set_parameter_value(param, cached)

    def _on_toggle_snap_mode(self, idx):
        pass

    def _set_parameter_value(self, param, value):
        current = param.value
        def restore():
            param.value = current
            param.value = value
        param.value = value
        self.schedule_message(1, restore)

    def _check_device(self):
        d = self._device._device
        if liveobj_valid(d): return
        self._device.set_lock_to_device(False, None)
        self._modes.pop_mode('menu')
        self._modes.pop_mode('device')

