from _Framework.CompoundComponent import CompoundComponent
from _Framework.SubjectSlot import subject_slot
from _Framework.DeviceComponent import DeviceComponent
from _Framework.Layer import Layer
from _Framework.ModesComponent import LayerMode

from _Framework.ModesComponent import ModesComponent

class DeviceComponentEx(CompoundComponent):
    """
    Extended DeviceComponent for the Midi Fighter Twister
    """

    def __init__(self, *a, **k):
        super(DeviceComponentEx, self).__init__(*a, **k)

        self._device = self.register_component(DeviceComponent())
        self._modes = self.register_component(ModesComponent())

        self._knobs = None
        self._buttons = None

    def set_knobs(self, knobs):
        self._knobs = knobs
        self._update_knobs()

    def set_buttons(self, buttons):
        self._buttons = buttons
        self._update_buttons()

    def update(self):
        super(DeviceComponentEx, self).update()
        self._update_buttons()
        self._update_knobs()

    def _update_buttons(self):
        pass

    def _update_knobs(self):
        pass




