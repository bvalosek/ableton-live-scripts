from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot

class MetronomeComponent(ControlSurfaceComponent):
    """
    Show metronome beat readout
    """

    def __init__(self, *a, **k):
        super(MetronomeComponent, self).__init__(*a, **k)
        self._lights = None
        self._beat = None
        self._on_time.subject = self.song()

    def set_lights(self, controls):
        self._lights = controls
        self.update()

    @subject_slot('current_song_time')
    def _on_time(self):
        if not self.is_enabled() or not self._lights:
            self._beat = None
            return
        beats = self.song().get_current_beats_song_time()
        if beats.beats != self._beat:
            self._beat = (beats.beats - 1) % len(self._lights)
            self.update()

    def update(self):
        if not self._lights or not self.is_enabled():
            return
        for idx, c in enumerate(self._lights):
            if self._beat is not idx:
                c.set_light('Metronome.Background')
            else:
                c.set_light('Metronome.Beat')

