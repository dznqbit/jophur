import rotaryio
import board
import neopixel
import digitalio
from time import sleep, time
from math import floor
from jophur import display
from jophur.midi import initMidi, playNote, reverbProgram, junoProgram, junoCC, KiwiCC
from jophur.songs import songs, song_program_data
import board
from analogio import AnalogIn

# EXPRESSION PEDAL
analog_in = AnalogIn(board.A0)
vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)

def get_voltage(pin):
    return (pin.value / 65536) * pin.reference_voltage

def get_vbat_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2

last_voltage = None

# BUTTONS
def new_button(pin):
    button = digitalio.DigitalInOut(pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    return button

buttons = {
    "Rotary": { "button": new_button(board.A2), "state": None },
    "OLED_A": { "button": new_button(board.D9), "state": None },
    "OLED_B": { "button": new_button(board.D6), "state": None },
    "OLED_C": { "button": new_button(board.D5), "state": None },
    "A":      { "button": new_button(board.D10), "state": None },
    "B":      { "button": new_button(board.D11), "state": None },
    "C":      { "button": new_button(board.D12), "state": None },
}

# KNOB
encoder = rotaryio.IncrementalEncoder(board.A3, board.A4)
position = encoder.position
last_position = None

# OUTPUTS

# TEXT AREA
text_area = display.init()

# LEDS
def new_led(pin):
    led = digitalio.DigitalInOut(pin)
    led.direction = digitalio.Direction.OUTPUT

    return led;

leds = {
    "A": new_led(board.A5),
    "B": new_led(board.D4),
    "C": new_led(board.D13),
}

def selectLed(index):
    for key in leds:
        leds[key].value = index == key

# MIDI
midi = initMidi(listen=False)

last_input_at = time()

REALTIME = 0.0005
SLEEP = 0.5

def lights_out():
    text_area.text = ""
    for led in leds:
        leds[led].value = False

sleep_interval = REALTIME

def logBattery():
    v = get_vbat_voltage(vbat_voltage);
    # Fully charge: 3.92
    print("VBat voltage: {:.2f}".format(v))

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
        selectLed(patchIndex);

while True:
    # Sleep display after
    if sleep_interval == REALTIME and time() - last_input_at > 5:
        sleep_interval = SLEEP
        lights_out()

    if sleep_interval == SLEEP and time() - last_input_at < 5:
        sleep_interval = REALTIME
        text_area.text = songs[encoder.position % len(songs)]


    sleep(sleep_interval)

    voltage = (get_voltage(analog_in))

    if last_voltage and (abs(voltage - last_voltage) > 0.02):
#        print((voltage,))
        cc_val = floor(127.0 * voltage / 3.3)
#        print((cc_val,))
        junoCC(midi, KiwiCC.LOW_PASS_CUTOFF_FREQ, cc_val)

    last_voltage = voltage

    for button_key in buttons.keys():
        button = buttons[button_key]["button"]
        button_state = buttons[button_key]["state"]

        if not button.value and button_state is None:
            last_input_at = time()
            buttons[button_key]["state"] = "pressed"
            song = songs[position]

            action = {
                "OLED_A": lambda: sendPatchData((midi, text_area), song, "A"),
                "A": lambda: sendPatchData((midi, text_area), song, "A"),
                "OLED_B": lambda: sendPatchData((midi, text_area), song, "B"),
                "B": lambda: sendPatchData((midi, text_area), song, "B"),
                "OLED_C": lambda: sendPatchData((midi, text_area), song, "C"),
                "C": lambda: sendPatchData((midi, text_area), song, "C"),
                "Rotary": lambda: logBattery()
            }.get(button_key)

            if action:
                action()

        if button.value and button_state == "pressed":
            buttons[button_key]["state"] = None

    position = encoder.position % len(songs)
    if last_position is None or position != last_position:
        last_input_at = time()
        new_song = songs[position]
        text_area.text = f"{new_song}"
        song_data = song_program_data.get(new_song)

    last_position = position
