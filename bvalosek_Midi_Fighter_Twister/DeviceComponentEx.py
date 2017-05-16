from _Framework.CompoundComponent import CompoundComponent
from _Framework.SubjectSlot import subject_slot_group, subject_slot
from _Framework.DeviceComponent import DeviceComponent
from _Framework.Layer import Layer
from _Framework.ModesComponent import LayerMode, ComponentMode

from BackgroundComponent import BackgroundComponent

from _Framework.ModesComponent import ModesComponent

class DeviceComponentEx(CompoundComponent):
    """
    Extended DeviceComponent for the Midi Fighter Twister
    """

    next_id = 1

    def __init__(self, *a, **k):
        super(DeviceComponentEx, self).__init__(*a, **k)
        self.id = DeviceComponentEx.next_id
        DeviceComponentEx.next_id += 1

        self._device = self.register_component(DeviceComponent())

        self._knobs = None
        self._buttons = None

    def set_knobs(self, knobs):
        self._knobs = knobs
        self.update()

    def set_buttons(self, buttons):
        self._buttons = buttons
        self._button_pressed.replace_subjects(buttons or [ ])
        self.update()

    def update(self):
        super(DeviceComponentEx, self).update()
        b = len(self._buttons or [ ])
        k = len(self._knobs or [ ])
        if b and k:
            self.log("{} enable".format(self.id))
        elif b or k:
            pass
        else:
            self.log("{} disable".format(self.id))

    @subject_slot_group('value')
    def _button_pressed(self, value, button):
        if not value: return
        idx = [b for b in self._buttons].index(button)
        self.log("{} {}".format(self.id, idx))
        pass
