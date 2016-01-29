from _Framework.DeviceComponent import DeviceComponent
from math import ceil

class TwisterDevice(DeviceComponent):
    """Base device used for the various modules on the wister"""

    def __init__(self, *a, **k):
        DeviceComponent.__init__(self, *a, **k)
        self._param_buttons = []

    def set_parameter_buttons(self, buttons):
        """Set the ButtonMatrix of push buttons on the face of the twister,
        also used to send out color values
        """
        self._param_buttons = buttons
        self._param_buttons_changed.replace_subjects(buttons or [])

    def send_colors(self, colors):
        """Send out colors to the Twister, None will NOP and 0 will blank"""
        for n, button in enumerate(self._param_buttons or []):
            if not button: continue
            if len(colors) <= n: continue
            if colors[n] == None: continue
            button.send_value(colors[n], force = True)

    def _bank_count(self):
        """Total number of banks of 16 params"""
        return int(ceil(len(self._get_all_params()) / 16.0))

    def _get_all_params(self):
        """All DeviceParameter that is a combo of the 'best of' 8 knobs + the rest"""
        best_of = self._best_of_parameter_bank()
        banks = self._parameter_banks()
        bank_names = self._parameter_bank_names()

        params = []

        # if we have a best-of, use that as first 8 params always
        if best_of: params.extend(best_of)

        # if we dont have a best of (VST, etc) or we have more than one bank,
        # add the rest
        if not best_of or len(banks) > 1:
            for name, bank in zip(bank_names, banks):

                # dont add in macros since it will always be best-of
                if name != 'Macros': params.extend([b for b in bank if b != None])

        return params

