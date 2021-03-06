from analogio import AnalogIn
import rotaryio
import board
import asyncio
import keypad
from math import floor
from lib.jophur import buttons

KNOB = "KNOB"
BUTTON = "BUTTON"
PEDAL = "PEDAL"

KNOB_UP = "UP"
KNOB_DOWN = "DOWN"

class Listener:
    def __init__(self):
        self.events = []
    
    def knob_rotated(self, direction):
        self.events.append((KNOB, KNOB_UP if direction > 0 else KNOB_DOWN))

    def button_pressed(self, button):
        self.events.append((BUTTON, button))
    
    def expression_pedaled(self, linear_amount):
        self.events.append((PEDAL, linear_amount))

async def monitor_rotary_encoder(listener):
    encoder = rotaryio.IncrementalEncoder(board.A3, board.A4)
    position = encoder.position
    last_position = None

    while True:
        position = encoder.position
        if last_position is not None and position != last_position:
            listener.knob_rotated(position - last_position)

        last_position = position
        await asyncio.sleep(0)

async def monitor_buttons(listener):
    button_dict = {
        board.A2: buttons.ROTARY,
        board.D9: buttons.OLED_A,
        board.D6: buttons.OLED_B,
        board.D5: buttons.OLED_C,
        board.D10: buttons.A,
        board.D11: buttons.B,
        board.D12: buttons.C
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

async def monitor_pedal(listener):
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
