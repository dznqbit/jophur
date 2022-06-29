import rotaryio
import board
import neopixel
import digitalio
from analogio import AnalogIn
import asyncio
import countio
import keypad

from time import sleep, time
from math import floor
from lib.jophur.interface import KNOB, BUTTON, UP, Listener, monitor_buttons, monitor_rotary_encoder
from lib.jophur import buttons, display, songs, midi

def new_led(pin):
    led = digitalio.DigitalInOut(pin)
    led.direction = digitalio.Direction.OUTPUT

    return led

def flatten(xss):
    return [x for xs in xss for x in xs]

class Jophur:
    def __init__(self, setlist):
        self.songs = setlist
        self.song_program_data = songs.song_program_data

        self.selected_song_index = 0
        self.current_patch_song_index = 0
        self.current_patch_index = 0

        self.midi = midi.initMidi(listen=False)
        self.text_area = display.init()
        self.button_leds = [new_led(pin) for pin in [board.A5, board.D4, board.D13]]
    
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

### BATTERY STUFF ###
vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)

def get_vbat_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2
##### END BATTERY STUFF ###

### MIDI ###
def send_patch_midi(jophur, patch_data):
    ((juno_bank, juno_program), reverb_program) = patch_data
    print(f"MIDI\n\tJuno {juno_program}\n\tReverb {reverb_program}")

    midi.junoProgram(jophur.midi, juno_bank, juno_program)
    midi.reverbProgram(jophur.midi, reverb_program)

### END MIDI ###
async def jophur_event_loop(jophur, listener):
    while True:
        if len(listener.events) > 0:
            (event_name, event_data) = listener.events.pop(0)

            if event_name == KNOB:
                song = jophur.select_next_song() if event_data == UP else jophur.select_previous_song()
                jophur.text_area.text = song

            if event_name == BUTTON:
                button = event_data
                if button == buttons.ROTARY:
                    v = get_vbat_voltage(vbat_voltage)
                    # Fully charge: 3.92
                    print("VBat voltage: {:.2f}".format(v))
                    jophur.text_area.text = "VBat voltage: {:.2f}".format(v)

                if button in [buttons.A, buttons.B, buttons.C]:
                    selected_patch = jophur.set_current_patch(
                        jophur.selected_song_name(), 
                        [buttons.A, buttons.B, buttons.C].index(button)
                    )

                    if selected_patch is None:
                        continue
                    
                    (song, patch_index, patch_data) = selected_patch
                    print(song, patch_index, "send midi", patch_data)
                    send_patch_midi(jophur, patch_data)
            
            # Update LEDs
            for i in range(0, len(jophur.button_leds)):
                jophur.button_leds[i].value = jophur.current_patch_index == i and \
                    jophur.selected_song_index == jophur.current_patch_song_index

        await asyncio.sleep(0)

async def main():
    jophur = Jophur([
        songs.BETTER_ANGELS,
        songs.FOLDING_IN_THIRDS,
        songs.MOONLIGHT_TRIALS,
        songs.BUILDING_THE_LABYRINTH,
        songs.NOBODY_REALLY,
        songs.FUTURE_IS_GAY,
        songs.AUTUMNESQUE,
        songs.YOU_DIE
    ])

    listener = Listener()

    await asyncio.gather(
        asyncio.create_task(monitor_buttons(listener)),
        asyncio.create_task(monitor_rotary_encoder(listener)),
        asyncio.create_task(jophur_event_loop(jophur, listener))
    )

asyncio.run(main())
