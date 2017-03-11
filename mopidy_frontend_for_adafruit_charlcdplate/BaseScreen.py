class BaseScreen:

    def __init__(self, core):
        self.core = core
        self.update = True
        self.subscreens = []
        self.current_subscreen_index = -1
        self.subscreen_control = False

    def check_and_update(self, display_object):
        if self.update:
            self.update_display(display_object)
            self.update = False
            return True
        else:
            return False

    def update_display(self, display_object):
        pass

    def resume(self):
        self.update = True

    def input_event(self, event):
        if self.subscreen_control and self.current_subscreen_index > -1 and self.current_subscreen_index < len(self.subscreens):
            return self.subscreens[self.current_subscreen_index].on_input_event(event)
        else:
            return self.on_input_event(event)

    def on_input_event(self, event):
        pass

    # Events
    def playback_state_changed(self, old_state, new_state):
        for subscreen in self.subscreens:
            subscreen.on_playback_state_changed(old_state, new_state)
        self.on_playback_state_changed(old_state, new_state)

    def on_playback_state_changed(self, old_state, new_state):
        pass

    def track_playback_started(self, tl_track):
        for subscreen in self.subscreens:
            subscreen.track_playback_started(tl_track)
        self.on_track_playback_started(tl_track)

    def on_track_playback_started(self, tl_track):
        pass

    def track_playback_ended(self, tl_track, time_position):
        for subscreen in self.subscreens:
            subscreen.track_playback_ended(tl_track, time_position)
        self.on_track_playback_ended(tl_track, time_position)

    def on_track_playback_ended(self, tl_track, time_position):
        pass

    def track_playback_paused(self, tl_track, time_position):
        for subscreen in self.subscreens:
            subscreen.track_playback_paused(tl_track, time_position)
        self.on_track_playback_paused(tl_track, time_position)

    def on_track_playback_paused(self, tl_track, time_position):
        pass

    def track_playback_resumed(self, tl_track, time_position):
        for subscreen in self.subscreens:
            subscreen.track_playback_resumed(tl_track, time_position)
        self.on_track_playback_resumed(tl_track, time_position)

    def on_track_playback_resumed(self, tl_track, time_position):
        pass

    def seeked(self, time_position):
        for subscreen in self.subscreens:
            subscreen.seeked(time_position)
        self.on_seeked(time_position)

    def on_seeked(self, time_position):
        pass


    def volume_changed(self, volume):
        for subscreen in self.subscreens:
            subscreen.volume_changed(volume)
        self.on_volume_changed(volume)

    def on_volume_changed(self, volume):
        pass

    def stream_title_changed(self, title):
        for subscreen in self.subscreens:
            subscreen.stream_title_changed(title)
        self.on_stream_title_changed(title)

    def on_stream_title_changed(self, title):
        pass

    def playlists_loaded(self):
        for subscreen in self.subscreens:
            subscreen.on_playlists_loaded()
        self.on_playlists_loaded()


    def on_playlists_loaded(self):
        pass