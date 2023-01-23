import asyncio
import board
import os
from lib.jophur.files import read_setlist
import ulab
from math import floor
from analogio import AnalogIn

from lib.jophur import buttons
from lib.jophur.interface import PEDAL, KNOB, BUTTON, KNOB_UP, KNOB_DOWN
from lib.jophur.util import lerp, rotate_index

INIT = "Init"
MAIN = "Main"
BATTERY = "Battery"
BLANK = "Blank"
SETLISTS = "Setlists"

class menu_state_machine():
    def __init__(self, menus):
        self.menu = None
        self.menus = menus

    def go_to_menu(self, menu_name):
        if self.menu:
            self.menu.exit(self)

        menu = self.menus[menu_name]

        if menu:
            self.menu = self.menus[menu_name]
            self.menu.enter(self)

    async def loop(self):
        if self.menu:
          await self.menu.loop(self)

class menu():
    def __init__(self, jophur):
        self.jophur = jophur

    def enter(self, _):
        pass

    def exit(self, _):
        pass

    async def loop(self, _):
        return True

class init_menu(menu):
    def enter(self, _):
      pass

    async def loop(self, machine):
      await asyncio.sleep(0.1)
      machine.go_to_menu(MAIN)

class main_menu(menu):
    def __init__(self, jophur, listener):
        super().__init__(jophur)
        self.listener = listener
        self.last_knob_events = []

    def update_ui(self):
        jophur = self.jophur

        # Update LEDs
        for i in range(0, len(jophur.button_leds)):
            jophur.button_leds[i].value = jophur.current_patch_index == i and \
                jophur.selected_song_index == jophur.current_patch_song_index

        jophur.text_area.text = jophur.selected_song_and_index()

    def enter(self, _):
        self.last_knob_events = []
        self.update_ui()

    def exit(self, _):
        pass

    async def loop(self, machine):
        listener = self.listener
        jophur = self.jophur
        last_knob_events = self.last_knob_events

        if len(listener.events) > 0:
            (event_name, event_data) = listener.events.pop(0)
            if event_name == KNOB:
                if len(last_knob_events) > 3:
                    last_knob_events.remove(last_knob_events[0])

                last_knob_events.append(event_data)

                if len(last_knob_events) > 1:
                    if (all(e == KNOB_UP for e in last_knob_events)):
                        jophur.select_next_song()

                    if (all(e == KNOB_DOWN for e in last_knob_events)):
                        song = jophur.select_previous_song()

                    last_knob_events.clear()

            if event_name == BUTTON:
                button = event_data
                if button == buttons.ROTARY:
                    machine.go_to_menu(BATTERY)
                    return

                if button in [buttons.A, buttons.B, buttons.C]:
                    selected_patch = jophur.set_current_patch(
                        jophur.selected_song_name(),
                        [buttons.A, buttons.B, buttons.C].index(button)
                    )

                    if selected_patch is None:
                        return

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

            self.update_ui()

### BATTERY STUFF ###
# vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)
def get_vbat_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2

class select_menu(menu):
    def __init__(self, jophur, listener):
        super().__init__(jophur)
        self.listener = listener
        self.options = [
            "battery",
            "display off",
            "setlists",
        ]
        self.current_option_index = 0
        self.last_knob_events = []

    def enter(self, _):
        self.current_option_index = 0
        self.update_ui()

    def exit(self, _):
        pass

    def update_ui(self):
        option = self.options[self.current_option_index]

        if option == "battery":
            # Fully charge: 3.92
            # Voltage monitor not available on RP2040 ?
            # v = get_vbat_voltage(vbat_voltage)
            v = 1.0
            self.jophur.text_area.text = "VBat voltage: {:.2f}".format(v)

        if option == "display off":
            self.jophur.text_area.text = "Display off"

        if option == "setlists":
            self.jophur.text_area.text = "Setlists"

    async def loop(self, machine):
        listener = self.listener
        jophur = self.jophur

        if len(listener.events) > 0:
            (event_name, event_data) = listener.events.pop(0)

            if event_name == KNOB:
                last_knob_events = self.last_knob_events

                if len(last_knob_events) > 3:
                    last_knob_events.remove(last_knob_events[0])

                last_knob_events.append(event_data)

                if len(last_knob_events) > 1:
                    if (all(e == KNOB_UP for e in last_knob_events)):
                        self.current_option_index = rotate_index(len(self.options), self.current_option_index, 1)

                    if (all(e == KNOB_DOWN for e in last_knob_events)):
                        self.current_option_index = rotate_index(len(self.options), self.current_option_index, -1)

                    last_knob_events.clear()

            if event_name == BUTTON:
                option = self.options[self.current_option_index]

                if option == "display off":
                    machine.go_to_menu(BLANK)
                    return

                elif option == "setlists":
                    machine.go_to_menu(SETLISTS)
                    return

                else:
                    machine.go_to_menu(MAIN)
                    return

            self.update_ui()

class blank_menu():
    def __init__(self, jophur, listener):
        self.jophur = jophur
        self.listener = listener

    def enter(self, _):
        j = self.jophur
        j.lights_out()
        pass

    def exit(self, _):
        pass

    async def loop(self, machine):
        if len(self.listener.events) > 0:
            (event_name, event_data) = self.listener.events.pop(0)
            if event_name == PEDAL:
                return

            machine.go_to_menu(MAIN)

##### END BATTERY STUFF ###

class setlist_menu():
    def __init__(self, jophur, listener):
        self.jophur = jophur
        self.listener = listener
        self.setlists = []
        self.selected_index = 0
        self.last_knob_events = []

    def enter(self, _):
        self.setlists = os.listdir("setlists")
        self.selected_index = 0
        self.update_ui()

    def exit(self, _):
        pass

    def update_ui(self):
        setlists_with_selection = list(map(
            lambda n: f"> {n[1]}" if n[0] == self.selected_index else n[1],
            list(enumerate(self.setlists))
        ))
        rolled_setlist = setlists_with_selection[self.selected_index:self.selected_index+2]
        if len(rolled_setlist) == 1 and len(setlists_with_selection) > 1:
            rolled_setlist.append(setlists_with_selection[0])
        self.jophur.text_area.text = "\n".join(rolled_setlist)

    def load_selected_setlist(self):
        setlist = read_setlist(f"setlists/{self.setlists[self.selected_index]}")
        self.jophur.replace_setlist(setlist)

    async def loop(self, machine):
        last_knob_events = self.last_knob_events
        j = self.jophur

        if len(self.listener.events) > 0:
            (event_name, event_data) = self.listener.events.pop(0)

            if event_name == BUTTON:
                if event_data == buttons.ROTARY:
                    self.load_selected_setlist()

                machine.go_to_menu(MAIN)

            if event_name == KNOB:
                if len(last_knob_events) > 3:
                    last_knob_events.remove(last_knob_events[0])
                last_knob_events.append(event_data)

                if len(last_knob_events) > 1:
                    if (all(e == KNOB_UP for e in last_knob_events)):
                        self.selected_index = rotate_index(len(self.setlists), self.selected_index, 1)

                    if (all(e == KNOB_DOWN for e in last_knob_events)):
                        self.selected_index = rotate_index(len(self.setlists), self.selected_index, -1)

                    last_knob_events.clear()



            self.update_ui()

