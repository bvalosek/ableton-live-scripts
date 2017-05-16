from _Framework.CompoundComponent import CompoundComponent
from _Framework.SubjectSlot import subject_slot_group, subject_slot

class KnobRowComponent(CompoundComponent):
    """
    4 knob super component
    """

    def __init__(self, *a, **k):
        super(KnobRowComponent, self).__init__(*a, **k)
        self._knobs = None
        self._select_button = None
        self._mode_button = None
        self._on_off_button = None
        self._device_mode = True
        self._offset = 0

    def set_knobs(self, knobs):
        self._knobs = knobs
        self.update()

    def set_select_button(self, button):
        self._select_button = button
        self.update()

    def set_mode_button(self, button):
        self._mode_button = button
        self._mode_button_value.subject = button
        self.update()

    def set_on_off_button(self, button):
        self._power_button = button
        self.update()

    def update(self):
        super(KnobRowComponent, self).update()

        if (self._device_mode and self._select_button):
            self._select_button.set_on_off_values('Device.DeviceMode', 'Device.DeviceMode')
            self._select_button.set_light(True)

    @subject_slot('value')
    def _mode_button_value(self, value):
        pass
