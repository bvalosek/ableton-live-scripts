from _Framework.DeviceComponent import DeviceComponent
from _Framework.SubjectSlot import subject_slot_group

class DeviceComponentEx(DeviceComponent):

    def __init__(self, *a, **k):
        DeviceComponent.__init__(self, *a, **k)
        self._chain_sliders = []
        self._chain_buttons = []
        self._sibling_devices = []

        self._parent_component = None

    def update(self):
        DeviceComponent.update(self)
        if not self.is_enabled(): return
        self._connect_sliders()
        self._connect_sibling_devices()

    def set_device(self, device):
        DeviceComponent.set_device(self, device)

        # Zero out controls whenever a device is disconnected
        if device is None:
            for c in (self._parameter_controls or []):
                if not c: continue
                c.force_next_send()
                c.send_value(0)

    def set_sibling_devices(self, devices):
        """
        Set of DeviceComponent instances that will be mapped to all sibling
        devices in the current chain / channel
        """
        self._sibling_devices = devices or []
        for d in self._sibling_devices: d._parent_component = self
        self._connect_sibling_devices()

    def set_chain_select_buttons(self, buttons):
        """
        Set of buttons that will set the current device to the first device of
        a chain on the current device
        """
        self._chain_buttons = buttons
        self._chain_buttons_changed.replace_subjects(buttons or [])

    def set_sibling_devices_enabled(self, is_enabled = True):
        for comp in self._sibling_devices:
            comp.set_enabled(is_enabled)

    def set_chain_volume_sliders(self, sliders):
        """ Set of sliders that adjust volume of chains """
        self._chain_sliders = sliders
        self._connect_sliders()

    def _connect_sliders(self):
        """ Wires chain sliders to chain volume devices """
        device = self._device
        for n, slider in enumerate(self._chain_sliders or []):
            if not slider: continue
            if device and device.can_have_chains and n < len(device.chains):
                slider.connect_to(device.chains[n].mixer_device.volume)
            else:
                slider.release_parameter()
                slider.force_next_send()
                slider.send_value(0)

    @subject_slot_group('value')
    def _chain_buttons_changed(self, value, button):
        """ Select a chain on button pressed """
        if not value: return
        if self._device is None or not self._device.can_have_chains: return
        index = [t for t in self._chain_buttons].index(button)
        if index >= len(self._device.chains): return
        chain = self._device.chains[index]
        if len(chain.devices) is 0: return
        self.song().view.select_device(chain.devices[0])

    def _get_sibling_devices(self):
        device = self._device
        if not device: return []
        parent = device.canonical_parent
        if not parent: return []
        sibs = [d for d in parent.devices]
        return sibs

    def _connect_sibling_devices(self):
        sibs = self._get_sibling_devices()
        for n, d in enumerate(self._sibling_devices):
            if n >= len(sibs):
                d.set_device(None)
            else:
                d.set_device(sibs[n])

    def _get_current_params(self):
        try:
            bank_name, params = self._current_bank_details()
            return params
        except:
            return []
