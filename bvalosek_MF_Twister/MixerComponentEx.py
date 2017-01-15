from _Framework.MixerComponent import MixerComponent

from bvalosek_common.MixerComponentEx import ChannelStripComponentEx as ChannelStripComponentExBase

from itertools import izip_longest

class ChannelStripComponentEx(ChannelStripComponentExBase):
    """
    Special ChannelStrip for the twister that allows for skinning, and skipping
    back to a non-return track when re-selecting a return
    """

    def __init__(self, mixer = None, *a, **k):
        super(ChannelStripComponentEx, self).__init__(*a, **k)
        self._mixer = mixer

    def update(self):
        if self._select_button:
            if self._track:
                self._select_button.set_on_off_values('Mixer.TrackSelected', 'Mixer.Track')
            else:
                self._select_button.set_on_off_values('Mixer.TrackSelected', 'Mixer.NoTrack')
        if self._arm_button:
            if self._track and self._track.can_be_armed:
                self._arm_button.set_on_off_values('Mixer.ArmOn', 'Mixer.ArmOff')
            else:
                self._arm_button.set_on_off_values('Mixer.CantArm', 'Mixer.CantArm')

        super(ChannelStripComponentEx, self).update()

    def _select_value(self, value):
        if value and self.song().view.selected_track == self._track:
            self._mixer.back_to_last_non_return_track()
            return
        super(ChannelStripComponentEx, self)._select_value(value)

class MixerComponentEx(MixerComponent):
    """
    Special MixerComponent that allows for skinning and "return backing"
    """

    def __init__(self, *a, **k):
        self._last_track = None
        super(MixerComponentEx, self).__init__(*a, **k)

    def set_return_track_select_buttons(self, buttons):
        for strip, button in izip_longest(self._return_strips, buttons or []):
            strip.set_select_button(button)

    def back_to_last_non_return_track(self):
        if self._last_track:
            self.song().view.selected_track = self._last_track

    def on_selected_track_changed(self):
        track = self.song().view.selected_track
        if track not in self.song().return_tracks:
            self._last_track = track

    def _create_strip(self):
        return ChannelStripComponentEx(mixer = self)
