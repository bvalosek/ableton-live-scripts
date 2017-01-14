from _Framework.MixerComponent import MixerComponent

from bvalosek_common.MixerComponentEx import ChannelStripComponentEx as ChannelStripComponentExBase

from itertools import izip_longest

class ChannelStripComponentEx(ChannelStripComponentExBase):
    """
    Special ChannelStrip for the twister that allows for skinning
    """

    def set_arm_button(self, button):
        if button:
            button.set_on_off_values('Mixer.ArmOn', 'Mixer.ArmOff')
        super(ChannelStripComponentEx, self).set_arm_button(button)

    def update(self):
        if self._select_button:
            if self._track:
                self._select_button.set_on_off_values('Mixer.TrackSelected', 'Mixer.Track')
            else:
                self._select_button.set_on_off_values('Mixer.TrackSelected', 'Mixer.NoTrack')
        super(ChannelStripComponentEx, self).update()

class MixerComponentEx(MixerComponent):
    """
    Special MixerComponent that allows for skinning
    """

    def set_return_track_select_buttons(self, buttons):
        for strip, button in izip_longest(self._return_strips, buttons or []):
            strip.set_select_button(button)

    def _create_strip(self):
        return ChannelStripComponentEx()
