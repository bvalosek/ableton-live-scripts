from _Framework.DeviceComponent import DeviceComponent
from _Framework.SubjectSlot import subject_slot_group

import math

from Colors import *

class DeviceComponentEx(DeviceComponent):
    """
    Extended DeviceComponent that allows for more than 8 parameters to be
    mapped at once, as well as skinning.

    Extra param controls will be mapped to the next bank
    """

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

    def set_bank_buttons(self, buttons):
        """
        Augment this method to pad the bank buttons out so we can skip in
        increments of 16 instead of 8
        """
        padded_buttons = [ x for list in [ [ b, None ] for b in buttons or [] ] for x in list ]
        super(DeviceComponentEx, self).set_bank_buttons(padded_buttons)

    def update(self):
        bank_count = self._big_bank_count()
        buttons = self._real_bank_buttons()
        for (idx, button) in enumerate(buttons):
            if idx < bank_count:
                button.set_on_off_values('Device.ActiveBank', 'Device.InactiveBank')
            else:
                button.set_on_off_values('Device.NoBank', 'Device.NoBank')
        super (DeviceComponentEx, self).update()

    @subject_slot_group('value')
    def _on_bank_value(self, value, button):
        if value and button:
            bank_count = self._big_bank_count()
            buttons = self._real_bank_buttons()
            idx = buttons.index(button)
            if idx >= bank_count:
                return
        super(DeviceComponentEx, self)._on_bank_value(value, button)

    def _assign_parameters(self):
        """
        Augment normal assign behavior to also assign the next bank to the
        bottom 8 of the param controls
        """
        super(DeviceComponentEx, self)._assign_parameters()
        if len(self._parameter_controls) > 8:
            next_bank = self._get_next_bank()
            for control, parameter in zip(self._parameter_controls[8:16], next_bank):
                if control and parameter:
                    control.connect_to(parameter)
                else:
                    control.release_parameter()

    def _real_bank_buttons(self):
        """ List of the actual bank buttons, filtering out the None padding """
        return [ b for b in self._bank_buttons or [] if b ]

    def _big_bank_count(self):
        """ Bank count when factoring 16 params """
        return math.ceil(len(self._parameter_banks()) / 2.0)

    def _get_next_bank(self):
        bank = []
        banks = self._parameter_banks()
        if banks and self._bank_index != None:
            next_index = self._bank_index + 1
            if len(banks) > next_index:
                bank = banks[next_index]
        return bank

