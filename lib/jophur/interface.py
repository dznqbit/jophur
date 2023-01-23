from analogio import AnalogIn
import rotaryio
import board
import asyncio
import keypad
import time
from math import floor
from lib.jophur import buttons

KNOB = "KNOB"
BUTTON = "BUTTON"
PEDAL = "PEDAL"

KNOB_UP = "UP"
KNOB_DOWN = "DOWN"

class Listener:
    def __init__(self, threshold = 600):
        self.events = []
        self.last_event_at = time.monotonic()
        self.threshold = threshold

    def clear(self):
        self.events.clear()

    def is_idle(self):
        return self.seconds_since_last_event() > self.threshold

    def seconds_since_last_event(self):
        return time.monotonic() - self.last_event_at

    def knob_rotated(self, direction):
        self.events.append((KNOB, KNOB_UP if direction > 0 else KNOB_DOWN))
        self.last_event_at = time.monotonic()

    def button_pressed(self, button):
        self.events.append((BUTTON, button))
        self.last_event_at = time.monotonic()

    def expression_pedaled(self, linear_amount):
        self.events.append((PEDAL, linear_amount))

async def monitor_rotary_encoder(listener, config):
    encoder = rotaryio.IncrementalEncoder(config.rotaryEncoder1, config.rotaryEncoder2)
    position = encoder.position
    last_position = None

    while True:
        position = encoder.position
        if last_position is not None and position != last_position:
            listener.knob_rotated(position - last_position)

        last_position = position
        await asyncio.sleep(0)

async def monitor_buttons(listener, config):
    button_dict = {
        config.rotaryButton: buttons.ROTARY,
        config.oledButtonA: buttons.OLED_A,
        config.oledButtonB: buttons.OLED_B,
        config.oledButtonC: buttons.OLED_C,
        config.buttonA: buttons.A,
        config.buttonB: buttons.B,
        config.buttonC: buttons.C
    }

    button_pins = list(button_dict.keys())

    with keypad.Keys(button_pins, value_when_pressed=False, pull=True) as keys:
        while True:
            key_event = keys.events.get()
            if key_event and key_event.pressed:
                button_name = button_dict[button_pins[key_event.key_number]]
                listener.button_pressed(button_name)

            await asyncio.sleep(0)


def get_voltage(pin):
    return (pin.value / 65536) * pin.reference_voltage

async def monitor_pedal(listener, config):
    # TEMP while RP2040
    return None

    pedal = AnalogIn(board.A0)
    last_voltage = None

    # Moog exp pedal OTHER has clean signal and is linear.
    # STANDARD is too noisy and has a weird curve.
    voltage_threshold = 0.025

    while True:
        voltage = get_voltage(pedal)
        if last_voltage and (abs(voltage - last_voltage) > voltage_threshold):
            listener.expression_pedaled(voltage / 3.3)

        last_voltage = voltage
        await asyncio.sleep(0)

    pedal.deinit()
