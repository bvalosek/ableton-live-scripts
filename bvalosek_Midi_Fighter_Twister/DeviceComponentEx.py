from _Framework.CompoundComponent import CompoundComponent
from _Framework.SubjectSlot import subject_slot_group, subject_slot
from _Framework.DeviceComponent import DeviceComponent
from _Framework.Layer import Layer
from _Framework.ModesComponent import LayerMode

from BackgroundComponent import BackgroundComponent

from _Framework.ModesComponent import ModesComponent

class DeviceComponentEx(CompoundComponent):
    """
    Extended DeviceComponent for the Midi Fighter Twister
    """

    def __init__(self, *a, **k):
        super(DeviceComponentEx, self).__init__(*a, **k)

        self._device = self.register_component(DeviceComponent())
        self._modes = self.register_component(ModesComponent())

        self._modes.add_mode('bg', LayerMode(BackgroundComponent(color = 'Device.NoDevice'), Layer()))

        self._modes.selected_mode = 'bg'

        self._knobs = None
        self._buttons = None

    def set_knobs(self, knobs):
        self._knobs = knobs
        self._device.set_parameter_controls(knobs)
        self.update()

    def set_buttons(self, buttons):
        self._buttons = buttons
        self._button_pressed.replace_subjects(buttons or [ ])
        self._modes.get_mode('bg')._layer = Layer(lights = buttons)
        self.update()

    def update(self):
        super(DeviceComponentEx, self).update()
        self._update_buttons()
        self._update_knobs()
        self.log(self._modes.selected_mode)
        # if self._modes.selected_mode:
        #     self._modes._do_enter_mode(self._modes.selected_mode)

    def _update_buttons(self):
        # for button in self._buttons or [ ]:
        #     if not self._device._device:
        #         button.set_on_off_values('Device.NoDevice', 'Device.NoDevice')
        #     button.set_light(False)
        pass

    def _update_knobs(self):
        pass

    @subject_slot_group('value')
    def _button_pressed(self, button, value):
        pass
