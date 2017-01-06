from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.MixerComponent import MixerComponent

from itertools import izip_longest

class ChannelStripComponentEx(ChannelStripComponent):
    """
    Special ChannelStrip for the twister that allows for skinning
    """

    def set_send_background_lights(self, lights):
        for light in lights or []:
            if light:
                light.set_light('Background.Sends')

    def set_arm_button(self, button):
        if button:
            button.set_on_off_values('Mixer.ArmOn', 'Mixer.ArmOff')
        super(ChannelStripComponentEx, self).set_arm_button(button)


class MixerComponentEx(MixerComponent):
    pass

    def set_return_track_select_buttons(self, buttons):
        for strip, button in izip_longest(self._return_strips, buttons or []):
            if button:
                button.set_on_off_values('Mixer.SendSelected', 'Mixer.Send')
            strip.set_select_button(button)

    def _create_strip(self):
        return ChannelStripComponentEx()
