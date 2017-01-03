from _Framework.SliderElement import SliderElement

class SliderElementEx(SliderElement):

    def release_parameter(self):
        SliderElement.release_parameter(self)
        self.send_value(0, force = True)

