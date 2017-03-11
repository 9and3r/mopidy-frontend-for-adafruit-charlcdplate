from BaseScreen import BaseScreen


class Playlists(BaseScreen):

    def __init__(self, core):
        BaseScreen.__init__(self, core)
        self.playlists = []
        self.current_playlist = 0
        self.on_playlists_loaded()

    def on_playlists_loaded(self):
        self.playlists = self.core.playlists.as_list().get()

    def update_display(self, display_object):
        if (len(self.playlists) == 0):
            display_object.change_display_data("Playlists", "No playlist")
        else:
            display_object.change_display_data("Playlists", self.playlists[self.current_playlist].name)

