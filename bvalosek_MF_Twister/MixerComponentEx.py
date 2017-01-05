from _Framework.ChannelStripComponent import ChannelStripComponent

class ChannelStripComponentEx(ChannelStripComponent):
    """
    Special ChannelStrip for the twister that allows for skinning
    """

    def set_send_background_lights(self, lights):
        for light in lights or []:
            if light:
                light.set_light('Background.Sends')

    def set_volume_background_light(self, light):
        if light:
            light.set_light('Background.Volume')

