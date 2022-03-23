import rotaryio
import board
import neopixel
import digitalio
from time import sleep
from math import floor
from jophur import display
from jophur.midi import initMidi, playNote, reverbProgram, junoProgram, junoCC, KiwiCC
from jophur.songs import songs, song_program_data

import board
from analogio import AnalogIn

analog_in = AnalogIn(board.A0)

def get_voltage(pin):
    return (pin.value / 65536) * pin.reference_voltage

last_voltage = None

midi = initMidi(listen=False)

def sendPatchData(deps, song, patchIndex):
    index = { "A": 0, "B": 1, "C": 2 }.get(patchIndex) or 0

    (midi, text_area) = deps
    song_data = song_program_data.get(song)
    print(f"{song} data {song_data}")

    if type(song_data) is list:
        if len(song_data) == 0:
            return

        if len(song_data) > index:
            patch_data = song_data[index]
        else:
            patch_data = song_data[len(song_data) - 1]
    else:
        patch_data = song_data

    if (patch_data):
        ((juno_bank, juno_program), reverb_program) = patch_data
        print(f"{song}\n\tJuno {juno_program}\n\tReverb {reverb_program}");

        junoProgram(midi, juno_bank, juno_program);
        reverbProgram(midi, reverb_program);

        text_area.text = f"{song}\n{patchIndex}";

def new_button(pin):
    button = digitalio.DigitalInOut(pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    return button

# Rotary Encoder button is broadboarded up on A2
# OLED Featherwing has panel buttons on D9, D6, D5
# https://learn.adafruit.com/adafruit-oled-featherwing/pinouts

buttons = {
    "Rotary": { "button": new_button(board.A2), "state": None },
    "OLED_A": { "button": new_button(board.D9), "state": None },
    "OLED_B": { "button": new_button(board.D6), "state": None },
    "OLED_C": { "button": new_button(board.D5), "state": None },
}

noop = lambda: None

# Rotary Encoder input is broadboarded up on A3, A4
encoder = rotaryio.IncrementalEncoder(board.A3, board.A4)
position = encoder.position
last_position = None

text_area = display.init()

while True:
    sleep(0.0005)

    voltage = (get_voltage(analog_in))
    if last_voltage and (abs(voltage - last_voltage) > 0.02):
        # print((voltage,))
        cc_val = floor(127.0 * voltage / 3.3)
        print((cc_val,))
        junoCC(midi, KiwiCC.INTERNAL_CLOCK_RATE, cc_val)
    last_voltage = voltage

    for button_key in buttons.keys():
        button = buttons[button_key]["button"]
        button_state = buttons[button_key]["state"]

        if not button.value and button_state is None:
            buttons[button_key]["state"] = "pressed"

            song = songs[position]
            # match statement is not available on micropython
            action = {
                "OLED_A": lambda: sendPatchData((midi, text_area), song, "A"),
                "OLED_B": lambda: sendPatchData((midi, text_area), song, "B"),
                "OLED_C": lambda: sendPatchData((midi, text_area), song, "C")
            }.get(button_key)

            (action or noop)()
            playNote(midi)

        if button.value and button_state == "pressed":
            buttons[button_key]["state"] = None

    position = encoder.position % len(songs)
    if last_position is None or position != last_position:
        new_song = songs[position]
        text_area.text = f"{new_song}"

        song_data = song_program_data.get(new_song)

    last_position = position
