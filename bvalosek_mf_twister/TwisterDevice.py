from _Framework.DeviceComponent import DeviceComponent

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

