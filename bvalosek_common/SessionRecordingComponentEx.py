import Live
from _Framework.ClipCreator import ClipCreator
from _Framework.SessionRecordingComponent import  *
from _Framework.ViewControlComponent import ViewControlComponent


class SessionRecordingComponentEx(SessionRecordingComponent):
    """
    Stolen / adapted from the Launchpad Pro Scripts

    Combines the functionality of new and record for the session
    """

    def __init__(self, *a, **k):
        super(SessionRecordingComponentEx, self).__init__(
            ClipCreator(), ViewControlComponent(), *a, **k)

    def _start_recording(self):
        track = self.song().view.selected_track
        if track and track.can_be_armed:
            playing_slot = track_playing_slot(track)
            should_overdub = not track_is_recording(track) and playing_slot != None
            if should_overdub:
                self.song().overdub = not self.song().overdub
                if not self.song().is_playing:
                    self.song().is_playing = True
            elif not self._stop_recording():
                self._prepare_new_slot(track)
                self._actually_record()
        elif not self._stop_recording():
            self._actually_record()

    def _actually_record(self):
        super(SessionRecordingComponentEx, self)._start_recording()

    def _prepare_new_slot(self, track):
        song = self.song()
        song.overdub = False
        view = song.view
        try:
            slot_index = list(song.scenes).index(view.selected_scene)
            track.stop_all_clips(False)
            self._jump_to_next_slot(track, slot_index)
        except Live.Base.LimitationError:
            self._handle_limitation_error_on_scene_creation()
