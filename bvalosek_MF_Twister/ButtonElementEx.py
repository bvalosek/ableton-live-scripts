from _Framework.ButtonElement import ButtonElement, ON_VALUE, OFF_VALUE

class ButtonElementEx(ButtonElement):
    """
    A special type of ButtonElement that allows skinning (that can be
    overridden when taking control)
    """

    default_states = { True: 'DefaultButton.On', False: 'DefaultButton.Disabled' }

    def __init__(self, default_states = None, *a, **k):
        super(ButtonElementEx, self).__init__(*a, **k)
        if default_states is not None:
            self.default_states = default_states
        self.states = dict(self.default_states)

    def set_on_off_values(self, on = None, off = None):
        self.states[True] = on or self.default_states[True]
        self.states[False] = off or self.default_states[False]

    def set_light(self, value):
        value = self.states.get(value, value)
        super(ButtonElementEx, self).set_light(value)

    def send_value(self, value, **k):
        if value is ON_VALUE:
            self.set_light(True)
        elif value is OFF_VALUE:
            self.set_light(False)
        else:
            super(ButtonElementEx, self).send_value(value, **k)

