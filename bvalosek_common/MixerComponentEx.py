from _Framework.MixerComponent import MixerComponent
from _Framework.ChannelStripComponent import ChannelStripComponent

class ChannelStripComponentEx(ChannelStripComponent):
    """
    * Also selects the track and focuses first device when ARM button is
        pressed
    * Prevents select button from being turned off (hitting same SELECT button
        mutliple times in a row)
    """

    def __init__(self, *a, **k):
        ChannelStripComponent.__init__(self, *a, **k)

    def _arm_value(self, value):
        ChannelStripComponent._arm_value(self, value)
        if value: self._select_track()

    def _select_value(self, value):
        ChannelStripComponent._select_value(self, value)
        self._select_track()
        if not value: self._select_button.turn_on()

    def _select_track(self):
        track = self._track
        self.song().view.selected_track = track
        if not len(track.devices):
            return
        device = track.devices[0]
        self.song().view.select_device(device)

class MixerComponentEx(MixerComponent):
    """
    * Uses ChannelStripComponentEx instances for channel strips
    """

    def __init__(self, *a, **k):
        MixerComponent.__init__(self, *a, **k)
        self._send_select_buttons = []

    def _create_strip(self):
        return ChannelStripComponentEx()

