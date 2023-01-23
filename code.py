import asyncio
import alarm
import board
from time import sleep, time
from math import floor
from lib.jophur.util import lerp

from lib.jophur.interface import Listener, monitor_buttons, monitor_rotary_encoder, monitor_pedal
from lib.jophur import files, songs, menus
from lib.jophur.jophur import Jophur
from lib.jophur.configuration import Configuration

async def run_state_machine(state_machine, listener):
    while True:
        try:
            if listener.is_idle():
                state_machine.go_to_menu(menus.BLANK)
            await state_machine.loop()
            await asyncio.sleep(0)
        except BaseException as err:
            print(err)

async def main():
    config = Configuration.get()
    setlist = files.read_setlist("setlists/ftg.txt")
    jophur = Jophur(songs.all_songs, config)
    jophur.replace_setlist(setlist)
    listener = Listener(threshold=600)
    state_machine = menus.menu_state_machine({
        menus.INIT: menus.init_menu(jophur),
        menus.MAIN: menus.main_menu(jophur, listener),
        menus.BATTERY: menus.select_menu(jophur, listener),
        menus.BLANK: menus.blank_menu(jophur, listener),
        menus.SETLISTS: menus.setlist_menu(jophur, listener),
    })
    state_machine.go_to_menu(menus.INIT)

    await asyncio.gather(
        asyncio.create_task(run_state_machine(state_machine, listener)),
        asyncio.create_task(monitor_buttons(listener, config)),
        asyncio.create_task(monitor_rotary_encoder(listener, config)),
        asyncio.create_task(monitor_pedal(listener, config)),
    )

asyncio.run(main())
