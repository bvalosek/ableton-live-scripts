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

        # components
        self._device = self.register_component(_DeviceComponent(log = log, is_enabled = False))
        self._modes = self.register_component(ModesComponent())
        self._background = self.register_component(BackgroundComponent(color = 70, is_enabled = False))
        self._empty = self.register_component(BackgroundComponent(is_enabled = False))
        self._menu = self.register_component(BackgroundComponent(is_enabled = False))

        color = randint(1,126)
        self._background.set_raw([ ColorEx(color) for n in range(4) ])

        self._modes.add_mode('empty', [ ComponentMode(self._empty) ])
        self._modes.add_mode('device', [ 
            ComponentMode(self._device), 
            ComponentMode(self._background) ])
        self._modes.add_mode('menu', [ ComponentMode(self._menu) ])

        self._modes.selected_mode = 'empty';

        # controls
        self._knobs = None
        self._buttons = None

    def set_knobs(self, knobs):
        self._knobs = knobs
        self._device.set_parameter_controls(knobs)
        self.update();

    def set_buttons(self, buttons):
        self._buttons = buttons
        self._button_pressed.replace_subjects(buttons or [ ])
        self._background.set_lights(buttons)
        self._empty.set_lights(buttons)
        self._menu.set_lights(buttons)
        if buttons == None: self._modes.pop_mode('menu')
        self.update();

    def update(self):
        super(DeviceComponentEx, self).update()
        self._check_device()

    @subject_slot_group('value')
    def _button_pressed(self, value, button):
        idx = [b for b in self._buttons].index(button)

        if value:
            if not self._device._locked_to_device:
                focused = self.song().appointed_device
                self._device.set_lock_to_device(True, focused)
                self._modes.push_mode('device')
            else:
                focused = self._device._device
                if liveobj_valid(focused):
                    if idx == 0:
                        self.song().appointed_device = focused
                        self.song().view.select_device(focused, False)
                    elif idx == 3:
                        self._modes.push_mode('menu')

        else:
            if idx == 3:
                self._modes.pop_mode('menu')

        self.update()

    def _check_device(self):
        d = self._device._device
        if not liveobj_valid(d):
            self._device.set_lock_to_device(False, None)
            self._modes.push_mode('empty')



