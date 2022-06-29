import rotaryio
import board
import asyncio
import keypad
from lib.jophur import buttons

KNOB = "KNOB"
BUTTON = "BUTTON"
UP = "UP"
DOWN = "DOWN"

class Listener:
    def __init__(self):
        self.events = []
    
    def knob_rotated(self, direction):
        self.events.append((KNOB, UP if direction > 0 else DOWN))

    def button_pressed(self, button):
        self.events.append((BUTTON, button))

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
