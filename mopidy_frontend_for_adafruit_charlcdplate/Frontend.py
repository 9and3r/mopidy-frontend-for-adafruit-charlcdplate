import threading
from time import sleep

from mopidy import core
from MainScreen import MainScreen
from InputManager import InputManager


from DisplayObject import DisplayObject

import pykka


class FrontendAdafruitCharLCDPlate(pykka.ThreadingActor, core.CoreListener):

    def __init__(self, config, core):
        super(FrontendAdafruitCharLCDPlate, self).__init__()
        self.input_manager = InputManager()
        self.display_object = DisplayObject()

        if True:
            import Adafruit_CharLCD as LCD
            self.display = LCD.Adafruit_CharLCDPlate()
        else:
            from web_socket_lcd_simulator import WebSockectLCDSimulator
            self.display = WebSockectLCDSimulator()


        self.main_screen = MainScreen(core)
        self.running = True

    def on_start(self):
        # Add newline
        self.display.set_color(1.0, 0.0, 0.0)
        self.display.create_char(0, [16, 16, 16, 16, 16, 16, 0, 0])
        self.display.create_char(1, [24, 24, 24, 24, 24, 24, 0, 0])
        self.display.create_char(2, [28, 28, 28, 28, 28, 28, 0, 0])
        self.display.create_char(3, [30, 30, 30, 30, 30, 30, 0, 0])
        self.display.create_char(4, [31, 31, 31, 31, 31, 31, 0, 0])
        try:
            self.display.on_start()



        except AttributeError:
            pass
        t = threading.Thread(target=self.start_working)
        t.start()

    def on_stop(self):
        self.running = False
        try:
            self.display.on_stop()
        except AttributeError:
            pass

    def send_screen_update(self):
        self.display.clear()
        self.display.message(self.display_object.getString())

    def start_working(self):
        while self.running:
            self.update()
            sleep(0.03)

    def update(self):
        # Check inputs
        for event in self.input_manager.update(self.display):
            print event
            self.main_screen.input_event(event)

        if self.main_screen.check_and_update(self.display_object, True) or self.display_object.update():
            self.send_screen_update()


    # Events

    def playback_state_changed(self, old_state, new_state):
        self.main_screen.playback_state_changed(old_state, new_state)

    def track_playback_started(self, tl_track):
        self.main_screen.track_playback_started(tl_track)

    def track_playback_ended(self, tl_track, time_position):
        self.main_screen.track_playback_ended(tl_track, time_position)

    def track_playback_paused(self, tl_track, time_position):
        self.main_screen.track_playback_paused(tl_track, time_position)

    def track_playback_resumed(self, tl_track, time_position):
        self.main_screen.track_playback_resumed(tl_track, time_position)

    def seeked(self, time_position):
        self.main_screen.seeked(time_position)

    def volume_changed(self, volume):
        self.main_screen.volume_changed(volume)

    def stream_title_changed(self, title):
        self.main_screen.stream_title_changed(title)

    def playlists_loaded(self):
        self.main_screen.playlists_loaded()


