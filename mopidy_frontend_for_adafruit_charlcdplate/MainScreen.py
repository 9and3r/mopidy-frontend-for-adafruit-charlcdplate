import time

from mopidy import core
from BaseScreen import BaseScreen

from DisplayObject import DisplayObject
from InputManager import InputManager
from ProgressBar import ProgressBar
from Playlists import Playlists


class MainScreen(BaseScreen):

    def __init__(self, core):
        BaseScreen.__init__(self, core)
        self.subscreens.append(NowPlayingTrack(core))
        self.subscreens.append(SeekScreen(core))
        self.subscreens.append(VolumeScreen(core))
        self.subscreens.append(Playlists(core))
        self.current_subscreen_index = 0
        self.playing = core.playback.get_state().get()

    def check_and_update(self, display_object):
        return self.subscreens[self.current_subscreen_index].check_and_update(display_object)

    def on_playback_state_changed(self, old_state, new_state):
        if new_state == core.PlaybackState.PLAYING:
            self.playing = True
        else:
            self.playing = False

    def update_display(self, display_object):
        self.subscreens[self.current_subscreen_index].update_display(display_object)

    def on_input_event(self, event):
        if event.type == 'click':
            if event.key == InputManager.SELECT:
                if self.playing:
                    self.core.playback.pause()
                else:
                    self.core.playback.play()
                return True
            elif event.key == InputManager.UP:
                self.current_subscreen_index -= 1
                if self.current_subscreen_index < 0:
                    self.current_subscreen_index = len(self.subscreens) - 1
                self.subscreens[self.current_subscreen_index].resume()
                return True

            elif event.key == InputManager.DOWN:
                self.current_subscreen_index += 1
                if self.current_subscreen_index >= len(self.subscreens):
                    self.current_subscreen_index = 0
                self.subscreens[self.current_subscreen_index].resume()
                return True
            else:
                return self.subscreens[self.current_subscreen_index].input_event(event)
        else:
            return self.subscreens[self.current_subscreen_index].input_event(event)


class NowPlayingTrack(BaseScreen):

    def __init__(self, core):
        BaseScreen.__init__(self, core)
        self.track_name = "No track"
        self.tl_track = None

    def update_display(self, display_object):
        if self.tl_track is not None:
            display_object.change_display_data(self.track_name, NowPlayingTrack.get_artist_string(self.tl_track.track))
        else:
            display_object.change_display_data("No track", "")

    def on_track_playback_started(self, tl_track):
        self.tl_track = tl_track
        self.track_name = NowPlayingTrack.get_track_name(self.tl_track.track)
        self.update = True

    def on_track_playback_ended(self, tl_track, time_position):
        self.tl_track = None
        self.track_name = "No track"
        self.update = True

    def on_stream_title_changed(self, title):
        self.track_name = title

    def on_input_event(self, event):
        if event.type == 'click':
            if event.key == InputManager.LEFT:
                self.core.playback.previous()
            elif event.key == InputManager.RIGHT:
                self.core.playback.next()


    @staticmethod
    def get_track_name(track):
        if track.name is None:
            return track.uri
        else:
            return track.name

    @staticmethod
    def get_track_album_name(track):
        if track.album is not None and track.album.name is not None \
                and len(track.album.name) > 0:
            return track.album.name
        else:
            return "Unknow Album"

    @staticmethod
    def get_artist_string(track):
        artists_string = ''
        for artist in track.artists:
            artists_string += artist.name + ', '
        if len(artists_string) > 2:
            artists_string = artists_string[:-2]
        elif len(artists_string) == 0:
            artists_string = "Unknow Artist"
        return artists_string


class SeekScreen(BaseScreen):
    def __init__(self, core):
        BaseScreen.__init__(self, core)
        self.progress_bar = ProgressBar(0, DisplayObject.MAX_CHARS_IN_ROW, 5)

        self.reference_second = 0
        self.second_in_song = 0

        self.current_second = 0

        self.track_current_second_text = None
        self.track_length_text = None

        self.length = None
        self.paused = False

    def update_current_second(self, second):
        if self.current_second != second:
            self.current_second = second
            self.track_current_second_text = time.strftime('%M:%S', time.gmtime(self.current_second))
            return True
        else:
            return False

    def on_track_playback_started(self, tl_track):
        self.second_in_song = 0
        self.reference_second = int(time.time())
        self.length = tl_track.track.length / 1000
        self.progress_bar.set_max(self.length)
        self.track_length_text = time.strftime('%M:%S', time.gmtime(self.length))
        self.update_current_second(0)
        self.update = True

    def on_track_playback_ended(self, tl_track, time_position):
        self.length = None
        self.update_current_second(0)
        self.update = True

    def on_track_playback_paused(self, tl_track, time_position):
        self.paused = True
        self.reference_second = 0
        self.second_in_song = time_position / 1000
        self.update_current_second(self.second_in_song)
        self.progress_bar.set_value(self.current_second)
        self.update = True

    def on_track_playback_resumed(self, tl_track, time_position):
        self.paused = False
        self.second_in_song = time_position / 1000
        self.reference_second = int(time.time())
        self.update_current_second(self.second_in_song)
        self.progress_bar.set_value(self.current_second)
        self.update = True

    def seeked(self, time_position):
        self.second_in_song = time_position / 1000
        self.reference_second = int(time.time())
        self.update_current_second(self.second_in_song)
        self.progress_bar.set_value(self.current_second)
        self.update = True

    def update_display(self, display_object):
        if self.length is not None:
            display_object.change_display_data("  " + self.track_current_second_text + " / " + self.track_length_text, self.progress_bar.string)
        else:
            display_object.change_display_data("No duration", "")

    def check_and_update(self, display_object):
        if self.length is not None:
            # Update values
            if not self.paused:
                self.update_current_second(int(time.time()) - self.reference_second + self.second_in_song)
                self.progress_bar.set_value(self.current_second)
            else:
                return self.update

        if self.update or self.progress_bar.update:
            self.update_display(display_object)
            return True
        else:
            return False


class VolumeScreen(BaseScreen):

    def __init__(self, core):
        BaseScreen.__init__(self, core)
        self.volume = core.mixer.get_volume().get()
        self.progress_bar = ProgressBar(100, DisplayObject.MAX_CHARS_IN_ROW, 5)
        self.progress_bar.set_value(self.volume)


    def update_display(self, display_object):
        display_object.change_display_data('Volume ' + str(self.volume), self.progress_bar.get_string())

    def on_input_event(self, event):
        if event.type == 'click':
            if event.key == InputManager.RIGHT:
                new_volume = self.volume + 5
                if new_volume > 100:
                    new_volume = 100
                self.core.mixer.set_volume(new_volume)
            if event.key == InputManager.LEFT:
                new_volume = self.volume - 5
                if new_volume < 0:
                    new_volume = 0
                self.core.mixer.set_volume(new_volume)

    def on_volume_changed(self, volume):
        self.volume = volume
        self.progress_bar.set_value(self.volume)
        self.update = True

