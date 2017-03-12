from BaseScreen import BaseScreen
from InputManager import InputManager


class Playlists(BaseScreen):

    def __init__(self, core):
        BaseScreen.__init__(self, core)
        self.playlists = []
        self.current_playlist = 0
        self.on_playlists_loaded()

    def on_playlists_loaded(self):
        self.playlists = self.core.playlists.as_list().get()

    def update_display(self, display_object, full_control):
        if full_control:
            if (len(self.playlists) == 0):
                display_object.change_display_data("Playlists", "No playlist")
            else:
                display_object.change_display_data("Playlists", self.playlists[self.current_playlist].name)
        else:
            display_object.change_display_data("Playlists", "")

    def on_input_event(self, event):
        if event.type == 'click':
            if event.key == InputManager.UP:
                self.move_list_item(-1)
            elif event.key == InputManager.DOWN:
                self.move_list_item(1)
            elif event.key == InputManager.SELECT:
                if len(self.playlists) > 0:
                    self.core.tracklist.clear()
                    self.core.tracklist.add(uri=self.playlists[self.current_playlist].uri)
                    self.core.playback.play()

    def move_list_item(self, move):
        self.current_playlist += move
        if self.current_playlist >= len(self.playlists):
            self.current_playlist = 0
        elif self.current_playlist < 0:
            self.current_playlist = len(self.playlists) - 1
        self.update = True

