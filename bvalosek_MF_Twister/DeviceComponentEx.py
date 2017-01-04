from _Framework.DeviceComponent import DeviceComponent

from Colors import *

class DeviceComponentEx(DeviceComponent):
    """
    Extended DeviceComponent that allows for more than 8 parameters to be
    mapped at once.

    Extra param controls will be mapped to the next bank
    """

    def _assign_parameters(self):
        DeviceComponent._assign_parameters(self)
        if len(self._parameter_controls) > 8:
            next_bank = self._get_next_bank()
            for control, parameter in zip(self._parameter_controls[8:16], next_bank):
                if control and parameter:
                    control.connect_to(parameter)
                else:
                    control.release_parameter()

    def _get_next_bank(self):
        bank = []
        banks = self._parameter_banks()
        if banks and self._bank_index != None:
            next_index = self._bank_index + 1
            if len(banks) > next_index:
                bank = banks[next_index]
        return bank

