from _Framework.DeviceComponent import DeviceComponent
from _Framework.SubjectSlot import subject_slot_group
from _Framework.SubjectSlot import subject_slot
from math import ceil

ON_COLOR = 45
OFF_COLOR = 85
BANK_COLOR = 120
BANK_ACTIVE_COLOR = 65

class Twister16ParamDevice(DeviceComponent):
    """Control 16 parameters at a time on the twister, using the buttons to
    page through the banks
    """

    def __init__(self, *a, **k):
        DeviceComponent.__init__(self, *a, **k)
        self._param_buttons = []
        self.active_bank = 0

    def set_parameter_buttons(self, buttons):
        """Set the ButtonMatrix of push buttons on the face of the twister,
        also used to send out color values
        """
        self._param_buttons = buttons
        self._param_buttons_changed.replace_subjects(buttons or [])

    def update(self):
        """Called by framework when the component needs to update"""
        DeviceComponent.update(self)
        if not self.is_enabled(): return

        self._on_on_off_change.subject = self._on_off_parameter()
        self._on_on_off_change()

    def set_device(self, device):
        """Make sure to reset offset when device changes"""
        self.active_bank = 0
        DeviceComponent.set_device(self, device)

    @subject_slot('value')
    def _on_on_off_change(self):
        if not self._on_off_parameter(): return

        is_on = self._on_off_parameter().value > 0.5
        self.send_colors([ON_COLOR if is_on else OFF_COLOR] * 8)

    def _assign_parameters(self):
        """Override how parameters get assigned to take advatage of 16 knobs

        We have to map the parameter controls to the parameters from our banks
        and UNMAP anything not legit
        """
        params = self._get_all_params()
        bank_count = self._bank_count()

        # bank's outta bounds
        if self.active_bank >= bank_count:
            self.active_bank = bank_count - 1

        # wire em
        for control, p in zip(self._parameter_controls, params[self.active_bank * 16:]):
            if control and p:
                control.connect_to(p)

        # blank the difference to clean missing params
        for c in self._parameter_controls[len(params):]:
            c.send_value(0, force = True)

        # remove param mappings (from original fn)
        self._release_parameters(self._parameter_controls[len(params):])

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

    @subject_slot_group('value')
    def _param_buttons_changed(self, value, button):
        """Fired when a button was pressed"""
        if not value: return
        index = [t for t in self._param_buttons].index(button)

        if (index == 0):
            p = self._on_off_parameter()
            p.value = 1 if p.value < 0.5 else 0
        elif (7 < index < 16):
            off = index - 8
            if off < self._bank_count():
                self.active_bank = off
                self._assign_parameters()

    def send_colors(self, colors):
        """Send out colors to the Twister, None will NOP and 0 will blank"""
        for n, button in enumerate(self._param_buttons or []):
            if not button: continue
            if len(colors) <= n: continue
            if colors[n] == None: continue
            button.send_value(colors[n], force = True)

