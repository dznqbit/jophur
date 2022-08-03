import board
import digitalio
from lib.jophur import display, songs, midi

def new_led(pin):
    led = digitalio.DigitalInOut(pin)
    led.direction = digitalio.Direction.OUTPUT

    return led

class Jophur:
    def __init__(self, setlist):
        self.songs = setlist
        self.song_program_data = songs.song_program_data

        self.selected_song_index = 0
        self.current_patch_song_index = 0
        self.current_patch_index = 0

        self.midi = midi.JophurMidi()
        self.text_area = display.init(f"Jophur v0.2")
        self.button_leds = [new_led(pin) for pin in [board.A5, board.D4, board.D13]]

    def replace_setlist(self, setlist):
        self.songs = setlist

    def selected_song_name(self):
        return self.songs[self.selected_song_index]

    def select_next_song(self):
        self.selected_song_index = (self.selected_song_index + 1) % len(self.songs)
        return self.selected_song_name()

    def select_previous_song(self):
        self.selected_song_index = (len(self.songs) + self.selected_song_index - 1) % len(self.songs)
        return self.selected_song_name()

    def current_patch_data(self):
        current_song_name = self.songs[self.current_patch_song_index]

        return (
            current_song_name,
            self.current_patch_index,
            self.song_program_data[current_song_name][self.current_patch_index]
        )

    def set_current_patch(self, song_name, patch_index):
        song_data = self.song_program_data[song_name]

        if song_data is None or len(song_data) <= patch_index:
            return None

        self.current_patch_index = patch_index
        self.current_patch_song_index = self.selected_song_index

        return self.current_patch_data()

    def selected_song_and_index(self):
      return f"{1 + self.selected_song_index}/{len(self.songs)} {self.selected_song_name()}"
