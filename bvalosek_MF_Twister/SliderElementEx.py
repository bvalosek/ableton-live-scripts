from _Framework.SliderElement import SliderElement

class SliderElementEx(SliderElement):
    """
    A special SliderElement for the MIDI Fighter Twister
    """

    def release_parameter(self):
        SliderElement.release_parameter(self)

        # always blank the value of the encoder when disconnecting from a bound parameter
        self.send_value(0, force = True)

