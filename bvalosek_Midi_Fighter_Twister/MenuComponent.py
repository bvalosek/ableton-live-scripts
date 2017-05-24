from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot_group, subject_slot

from Colors import *

OFF_COLOR = ColorEx(Rgb.OFF, Brightness.OFF)

class MenuComponent(ControlSurfaceComponent):
    """
    A component that allows for a set of buttons to be grabbed and trigger
    callbacks when pressed
    """

    def __init__(self, enable_lights = True, actions = None, *a, **k):
        super(MenuComponent, self).__init__(*a, **k)

        self._enable_lights = enable_lights
        self._actions = actions
        self._buttons = None

    def set_buttons(self, buttons):
        self._buttons = buttons
        self.update()

    def on_enabled_changed(self):
        self.update()

    def update_action(self, index, action):
        self._actions[index] = action
        self.update()

    @subject_slot_group('value')
    def _on_button(self, value, button):
        idx = [b for b in self._buttons].index(button)
        if len(self._actions) > idx:
            _ , down, up = self._actions[idx]
            if value and down:
                down()
            elif not value and up:
                up()

    def update(self):
        if self.is_enabled():
            self._on_button.replace_subjects(self._buttons or [ ])
            if self._enable_lights:
                for action, button in zip(self._actions or [ ], self._buttons or [ ]):
                    color, _, _ = action
                    if color:
                        button.set_light(color)
                    else:
                        OFF_COLOR.draw(button)
        else:
            self._on_button.replace_subjects([ ])
