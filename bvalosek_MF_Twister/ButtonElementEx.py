from _Framework.ButtonElement import ButtonElement

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

    def reset(self):
        self.states = dict(self.default_states)

    def set_on_off_values(self, on = None, off = None):
        self.states[True] = on or self.default_states[True]
        self.states[False] = off or self.default_states[False]

    def set_light(self, value):
        if value is True or value is False:
            value = self.states[value]
        super(ButtonElementEx, self).set_light(value)
