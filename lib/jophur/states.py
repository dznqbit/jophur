import asyncio
import board
from math import floor
from analogio import AnalogIn

from lib.jophur import buttons
from lib.jophur.interface import PEDAL, KNOB, BUTTON, KNOB_UP, KNOB_DOWN, monitor_buttons, monitor_rotary_encoder, monitor_pedal
from lib.jophur.util import lerp

class MenuStateMachine():
    def __init__(self, menus):
        self.menu = None
        self.menus = menus

    def go_to_menu(self, menu_name):
        if self.menu:
            self.menu.exit(self)

        self.menu = self.menus[menu_name]
        self.menu.enter(self)

    async def update(self):
        if self.menu:
          await self.menu.update(self)

class Menu():
    def __init__(self, jophur):
        self.jophur = jophur

    @property
    def name(self):
        return ''

    def enter(self, machine):
        pass

    def exit(self, machine):
        pass

    async def loop(self, machine):
        return True

class InitMenu(Menu):
    def enter(self, _):
      pass

    async def loop(self, machine):
      await asyncio.sleep(2)
      machine.go_to_menu("Main")

### BATTERY STUFF ###
vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)

def get_vbat_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2
##### END BATTERY STUFF ###

class MainMenu(Menu):
    def __init__(self, jophur, listener):
        super().__init__(jophur)
        self.listener = listener

    async def loop(self, _):
        listener = self.listener
        jophur = self.jophur
        last_knob_events = []

        while True:
            if len(listener.events) > 0:
                (event_name, event_data) = listener.events.pop(0)

                if event_name == KNOB:
                    if len(last_knob_events) > 3:
                        last_knob_events.remove(last_knob_events[0])

                    last_knob_events.append(event_data)
                    
                    if len(last_knob_events) > 1:
                        if (all(e == KNOB_UP for e in last_knob_events)):
                            jophur.select_next_song()
                            jophur.text_area.text = jophur.selected_song_and_index()

                        if (all(e == KNOB_DOWN for e in last_knob_events)):
                            song = jophur.select_previous_song()
                            jophur.text_area.text = jophur.selected_song_and_index()

                        last_knob_events.clear()

                if event_name == BUTTON:
                    button = event_data
                    if button == buttons.ROTARY:
                        v = get_vbat_voltage(vbat_voltage)

                        # Fully charge: 3.92
                        print("VBat voltage: {:.2f}".format(v))
                        # jophur.text_area.text = "VBat voltage: {:.2f}".format(v)

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
                else:
                    # Update LEDs
                    for i in range(0, len(jophur.button_leds)):
                        jophur.button_leds[i].value = jophur.current_patch_index == i and \
                            jophur.selected_song_index == jophur.current_patch_song_index

            await asyncio.sleep(0)
