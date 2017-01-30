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

    def set_lock_button(self, button):
        if button:
            button.set_on_off_values('Device.Locked', 'Device.NotLocked')
        super(DeviceComponentEx, self).set_lock_button(button)

    def set_bank_prev_button(self, button):
        if button:
            button.set_on_off_values('Device.CanBank', 'Device.CantBank')
        super(DeviceComponentEx, self).set_bank_prev_button(button)

    def set_bank_next_button(self, button):
        if button:
            button.set_on_off_values('Device.CanBank', 'Device.CantBank')
        super(DeviceComponentEx, self).set_bank_next_button(button)

    def set_on_off_button(self, button):
        if button:
            button.set_on_off_values('Device.On', 'Device.Off')
        super(DeviceComponentEx, self).set_on_off_button(button)

    def set_param_offset_button(self, button):
        """
        Param offset button can be used to toggle a 4-button offset in the
        mapped params
        """
        if button:
            button.set_on_off_values('Device.OffsetEnabled', 'Device.OffsetDisabled')
        self._param_offset_button = button
        self._param_offset_value.subject = button
        self._update_param_offset_button()

    def _update_param_offset_button(self):
        if self._param_offset_button:
            self._param_offset_button.set_light(self._param_offset)

    @subject_slot('value')
    def _param_offset_value(self, value):
        if not self._param_offset_button.is_momentary() or value is not 0:
            self._param_offset = not self._param_offset
            self.update()

    def update(self):
        super (DeviceComponentEx, self).update()
        self._update_param_offset_button()

    def _current_bank_details(self):
        """
        Override default behavior to factor in param_offset
        """
        bank_name, bank = super(DeviceComponentEx, self)._current_bank_details()
        if bank and len(bank) > 4 and self._param_offset:
            bank = bank[4:]
        return (bank_name, bank)

