from _Framework.MixerComponent import MixerComponent
from _Framework.ChannelStripComponent import ChannelStripComponent

class ChannelStripComponentEx(ChannelStripComponent):
    """
    Custom ChannelStrip that also selects the track and focuses the first
    device when the arm button is pressed
    """

    def __init__(self, *a, **k):
        ChannelStripComponent.__init__(self, *a, **k)

    def _arm_value(self, value):
        super(ChannelStripComponentEx, self)._arm_value(value)
        if value:
            self._select_track()

    def _select_track(self):
        track = self._track
        self.song().view.selected_track = track
        if not len(track.devices):
            return
        device = track.devices[0]
        self.song().view.select_device(device)

class MixerComponentEx(MixerComponent):
    """
    Custom MixerComponent that uses ChannelStripComponentEx instances for
    channel strips
    """

    def __init__(self, *a, **k):
        super(MixerComponentEx, self).__init__(*a, **k)

    def _create_strip(self):
        return ChannelStripComponentEx()
