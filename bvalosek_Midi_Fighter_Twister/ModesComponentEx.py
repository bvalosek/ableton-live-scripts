from _Framework.ModesComponent import ModesComponent

class ModesComponentEx(ModesComponent):
    """
    A special ModesComponent for the twister that lets us skin the mode buttons
    """

    def set_mode_button(self, name, button):
        if button:
            button.set_on_off_values('Modes.Selected', 'Modes.NotSelected')
        super(ModesComponentEx, self).set_mode_button(name, button)
