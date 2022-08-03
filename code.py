import asyncio
from time import sleep, time
from math import floor
from lib.jophur.util import lerp

from lib.jophur.interface import PEDAL, KNOB, BUTTON, KNOB_UP, KNOB_DOWN, Listener, monitor_buttons, monitor_rotary_encoder, monitor_pedal
from lib.jophur import files, songs
from lib.jophur.jophur import Jophur
from lib.jophur.menus import menu_state_machine, init_menu, main_menu

async def delayed_turn_screen_off(jophur):
    await asyncio.sleep(300) # seconds
    turn_screen_off(jophur)

def turn_screen_off(jophur):
    for i in range(0, len(jophur.button_leds)):
        jophur.button_leds[i].value = 0

    jophur.text_area.text = ""

async def run_state_machine(state_machine):
    while True:
        await state_machine.loop()
        await asyncio.sleep(0)

async def main():
    setlist = files.read_setlist("setlists/setlist.txt")
    jophur = Jophur(songs.all_songs)
    jophur.replace_setlist(setlist)
    listener = Listener()
    state_machine = menu_state_machine({
        "Init": init_menu(jophur),
        "Main": main_menu(jophur, listener),
    })
    state_machine.go_to_menu("Init")

    await asyncio.gather(
        asyncio.create_task(run_state_machine(state_machine)),
        asyncio.create_task(monitor_buttons(listener)),
        asyncio.create_task(monitor_rotary_encoder(listener)),
        asyncio.create_task(monitor_pedal(listener)),
        # asyncio.create_task(jophur_event_loop(jophur, listener)),
    )

asyncio.run(main())
