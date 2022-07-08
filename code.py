import board
import digitalio
from analogio import AnalogIn
import asyncio

from time import sleep, time
from math import floor
from lib.jophur.util import lerp

from lib.jophur.interface import PEDAL, KNOB, BUTTON, KNOB_UP, Listener, monitor_buttons, monitor_rotary_encoder, monitor_pedal
from lib.jophur import buttons, display, songs, midi

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

async def jophur_event_loop(jophur, listener):
    while True:
        if len(listener.events) > 0:
            (event_name, event_data) = listener.events.pop(0)

            if event_name == KNOB:
                song = jophur.select_next_song() if event_data == KNOB_UP else jophur.select_previous_song()
                jophur.text_area.text = song

            if event_name == BUTTON:
                button = event_data
                if button == buttons.ROTARY:
                    v = get_vbat_voltage(vbat_voltage)

                    # Fully charge: 3.92
                    print("VBat voltage: {:.2f}".format(v))
                    # jophur.text_area.text = "VBat voltage: {:.2f}".format(v)
                    jophur.text_area.text = ""

                if button in [buttons.A, buttons.B, buttons.C]:
                    selected_patch = jophur.set_current_patch(
                        jophur.selected_song_name(),
                        [buttons.A, buttons.B, buttons.C].index(button)
                    )

                    if selected_patch is None:
                        continue

                    (song, patch_index, patch_data) = selected_patch

                    print(song, patch_index, "send midi", patch_data)
                    jophur.midi.junoProgram(patch_data.juno_program[0], patch_data.juno_program[1])
                    jophur.midi.reverbProgram(patch_data.reverb_program)

            if event_name == PEDAL:
                selected_patch = jophur.current_patch_data()
                (_, _, patch_data) = selected_patch
                if patch_data.expression:
                    (exp_cc, exp_lo, exp_hi) = patch_data.expression
                    jophur.midi.junoCC(
                        exp_cc,
                        floor(lerp(event_data, exp_lo, exp_hi))
                    )

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
        asyncio.create_task(monitor_pedal(listener)),
        asyncio.create_task(jophur_event_loop(jophur, listener)),
    )

asyncio.run(main())
