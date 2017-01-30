from _Framework.DeviceComponent import DeviceComponent
from _Framework.SubjectSlot import subject_slot_group, subject_slot

import math

from Colors import *

class DeviceComponentEx(DeviceComponent):
    """
    Extended DeviceComponent for the MF Twister
    """

    def __init__(self, *a, **k):
        super(DeviceComponentEx, self).__init__(*a, **k)
        self._param_offset_button = None
        self._param_offset = False

    def set_param_offset_button(self, button):
        """ Button to toggle a 4-button offset in the mapped params """
        self._param_offset_button = button
        self._param_offset_value.subject = button
        self._update_param_offset_button()

    def set_lock_to_device(self, *a, **k):
        super(DeviceComponentEx, self).set_lock_to_device(*a, **k)
        self._update_param_controls()
        self._update_on_off_button()
        self._update_param_offset_button()

    def update(self):
        super (DeviceComponentEx, self).update()
        self._update_param_offset_button()
        self._update_param_controls()

    @subject_slot('value')
    def _param_offset_value(self, value):
        if not self._param_offset_button.is_momentary() or value is not 0:
            self._param_offset = not self._param_offset
            self.update()

    def _current_bank_details(self):
        """ Override default behavior to factor in param_offset """
        bank_name, bank = super(DeviceComponentEx, self)._current_bank_details()
        if bank and len(bank) > 4 and self._param_offset:
            bank = bank[4:]
        return (bank_name, bank)

    def _update_param_controls(self):
        for c in self._parameter_controls or []:
            if self._locked_to_device or not self._param_offset_button:
                c.send_value(95, channel = KNOB_ANIMATION_CHANNEL, force = True)
            else:
                c.send_value(69, channel = KNOB_ANIMATION_CHANNEL, force = True)

    def _update_param_offset_button(self):
        button = self._param_offset_button
        if not button: return
        if self._locked_to_device:
            button.set_on_off_values('Device.OffsetEnabled', 'Device.OffsetDisabled')
        else:
            button.set_on_off_values('DefaultButton.Off', 'DefaultButton.Off')
        button.set_light(self._param_offset)

    def _update_on_off_button(self):
        button = self._on_off_button
        if button:
            if self._locked_to_device:
                button.set_on_off_values('Device.On', 'Device.Off')
            else:
                button.set_on_off_values('DefaultButton.Off', 'DefaultButton.Off')
        super(DeviceComponentEx, self)._update_on_off_button()

    def _update_lock_button(self):
        if self._lock_button:
            self._lock_button.set_on_off_values('Device.Locked', 'Device.NotLocked')
        super(DeviceComponentEx, self)._update_lock_button()

