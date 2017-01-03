from _Framework.DeviceComponent import DeviceComponent

from Colors import *

class DeviceComponentEx(DeviceComponent):
    """
    Extended DeviceComponent that allows for more than 8 parameters to be
    mapped at once.

    Extra param controls will be mapped to the next bank
    """

    def __init__(self, *a, **k):
        DeviceComponent.__init__(self, *a, **k)

    def _assign_parameters(self):
        DeviceComponent._assign_parameters(self)
        if len(self._parameter_controls) > 8:
            next_bank = self._get_next_bank()
            for control, parameter in zip(self._parameter_controls[8:16], next_bank):
                if control and parameter:
                    control.connect_to(parameter)
                else:
                    control.release_parameter()

    def _update_lock_button(self):
        if self.is_enabled() and self._lock_button != None:
            self._lock_button.set_light('Device.Locked' if self._locked_to_device else 'Device.NotLocked')

    def _update_device_bank_nav_buttons(self):
        if self.is_enabled():
            if self._bank_up_button != None and self._bank_down_button != None:
                can_bank_down = self._bank_index == None or self._bank_index > 0
                can_bank_up = self._bank_index == None or self._number_of_parameter_banks() > self._bank_index + 1
                self._bank_up_button.set_light('Device.CanBank' if can_bank_up else 'Device.CantBank')
                self._bank_down_button.set_light('Device.CanBank' if can_bank_down else 'Device.CantBank')

    def _get_next_bank(self):
        bank = []
        banks = self._parameter_banks()
        if banks:
            if self._bank_index != None:
                next_index = self._bank_index + 1
                if len(banks) > next_index:
                    bank = banks[next_index]
        return bank

