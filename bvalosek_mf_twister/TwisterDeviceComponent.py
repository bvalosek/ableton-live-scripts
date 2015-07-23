from bvalosek_common.DeviceComponentEx import DeviceComponentEx
from _Framework.SubjectSlot import subject_slot_group

from str_to_color import str_to_color

class TwisterDeviceComponent(DeviceComponentEx):

    def __init__(self, *a, **k):
        DeviceComponentEx.__init__(self, *a, **k)

        self._param_buttons = []
        self.on_off_index = None
        self.show_sibling_devices_index = None
        self.hide_sibling_devices_index = None

    def update(self):
        DeviceComponentEx.update(self)
        if not self.is_enabled(): return
        self._send_param_colors()
        self._send_chain_colors()

    def set_chain_select_buttons(self, buttons):
        DeviceComponentEx.set_chain_select_buttons(self, buttons)
        self._send_chain_colors()

    def set_parameter_buttons(self, buttons):
        self._param_buttons = buttons
        self._param_buttons_changed.replace_subjects(buttons or [])
        self._send_param_colors()

    def _send_chain_colors(self):
        d = self._device
        for n, button in enumerate(self._chain_buttons):
            if not (button): continue
            if d is None or not d.can_have_chains or n >= len(d.chains):
                button.send_value(0)
            else:
                button.send_value(str_to_color(d.chains[n].name))

    def _send_param_colors(self):
        params = self._get_current_params()
        for n, button in enumerate(self._param_buttons or []):
            if not button: continue
            if n >= len(params):
                button.send_value(0)
                continue

            param = params[n]

            if param != None and param.name.strip() != '':
                button.send_value(str_to_color(param.name))
            else:
                button.send_value(0)

    @subject_slot_group('value')
    def _param_buttons_changed(self, value, button):
        if not value: return
        index = [t for t in self._param_buttons].index(button)

        if index == self.on_off_index:
            p = self._on_off_parameter()
            p.value = 1 if p.value < 0.5 else 0
        elif index == self.show_sibling_devices_index:
            self.set_sibling_devices_enabled(True)
        elif index == self.hide_sibling_devices_index and self._parent_component:
            if self._device:
                self.song().view.select_device(self._device)
            self._parent_component.set_sibling_devices_enabled(False)

