from TwisterDevice import TwisterDevice
from _Framework.SubjectSlot import subject_slot_group
from _Framework.SubjectSlot import subject_slot

ON_COLOR = 45
OFF_COLOR = 85
BANK_COLOR = 1
BANK_ACTIVE_COLOR = 65
BANK_NA_COLOR = 20

class Twister16ParamDevice(TwisterDevice):
    """Control 16 parameters at a time on the twister, using the buttons to
    page through the banks
    """

    def __init__(self, *a, **k):
        TwisterDevice.__init__(self, *a, **k)
        self.active_bank = 0

    def update(self):
        """Called by framework when the component needs to update"""
        TwisterDevice.update(self)
        if not self.is_enabled(): return

        self._on_on_off_change.subject = self._on_off_parameter()
        self._on_on_off_change()

    def set_device(self, device):
        """Make sure to reset offset when device changes"""
        self.active_bank = 0
        TwisterDevice.set_device(self, device)

    @subject_slot('value')
    def _on_on_off_change(self):
        if not self._on_off_parameter(): return
        if not self.is_enabled(): return

        is_on = self._on_off_parameter().value > 0.5
        colors = [ON_COLOR if is_on else OFF_COLOR] * 8
        colors[2] = colors[3] = None
        self.send_colors(colors)

    def _assign_parameters(self):
        """Override how parameters get assigned to take advatage of 16 knobs

        We have to map the parameter controls to the parameters from our banks
        and UNMAP anything not legit
        """
        if not self.is_enabled(): return
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
            if c: c.send_value(0, force = True)

        # remove param mappings (from original fn)
        self._release_parameters(self._parameter_controls[len(params):])

        # send colors to show how many banks we've got
        colors = [None] * 8 + [BANK_COLOR] * bank_count + [BANK_NA_COLOR] * (8 - bank_count)
        colors[8 + self.active_bank] = BANK_ACTIVE_COLOR
        self.send_colors(colors)

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

