from _Framework.DeviceComponent import DeviceComponent
from _Framework.SubjectSlot import subject_slot_group
from _Framework.SubjectSlot import subject_slot

class Twister4UpDevice(DeviceComponent):
    """Control 4 sibling devices at once with the first 4 params mapped"""

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
        colors = [45, 65, 0, 0] * 4
        self.send_colors(colors)

    @subject_slot_group('value')
    def _param_buttons_changed(self, value, button):
        """Fired when a button was pressed"""
        if not value: return
        index = [t for t in self._param_buttons].index(button)

    def send_colors(self, colors):
        """Send out colors to the Twister, None will NOP and 0 will blank"""
        for n, button in enumerate(self._param_buttons or []):
            if not button: continue
            if len(colors) <= n: continue
            if colors[n] == None: continue
            button.send_value(colors[n], force = True)

