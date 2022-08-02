import board

from analogio import AnalogIn
import asyncio

from time import sleep, time
from math import floor
from lib.jophur.util import lerp

from lib.jophur.interface import PEDAL, KNOB, BUTTON, KNOB_UP, KNOB_DOWN, Listener, monitor_buttons, monitor_rotary_encoder, monitor_pedal
from lib.jophur import buttons, files, songs
from lib.jophur.jophur import Jophur

### BATTERY STUFF ###
vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)

def get_vbat_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2
##### END BATTERY STUFF ###

async def turn_screen_off(jophur):
    await asyncio.sleep(300) # seconds

    for i in range(0, len(jophur.button_leds)):
        jophur.button_leds[i].value = 0

    jophur.text_area.text = ""

async def jophur_event_loop(jophur, listener):
    asyncio.create_task(turn_screen_off(jophur))
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
                        song = jophur.select_next_song()
                        jophur.text_area.text = song

                    if (all(e == KNOB_DOWN for e in last_knob_events)):
                        song = jophur.select_previous_song()
                        jophur.text_area.text = song

                    last_knob_events.clear()

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
            else:
                asyncio.create_task(turn_screen_off(jophur))

                # Update LEDs
                for i in range(0, len(jophur.button_leds)):
                    jophur.button_leds[i].value = jophur.current_patch_index == i and \
                        jophur.selected_song_index == jophur.current_patch_song_index

        await asyncio.sleep(0)

async def main():
    # did we deploy?
    setlist = files.read_setlist("setlists/setlist.txt")
    print("Setlist", setlist)
    jophur = Jophur(setlist or songs.all_songs)
    listener = Listener()

    await asyncio.gather(
        asyncio.create_task(monitor_buttons(listener)),
        asyncio.create_task(monitor_rotary_encoder(listener)),
        asyncio.create_task(monitor_pedal(listener)),
        asyncio.create_task(jophur_event_loop(jophur, listener)),
    )

asyncio.run(main())
