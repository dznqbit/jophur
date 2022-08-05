import asyncio
import alarm
import board
from time import sleep, time
from math import floor
from lib.jophur.util import lerp

from lib.jophur.interface import PEDAL, KNOB, BUTTON, KNOB_UP, KNOB_DOWN, Listener, monitor_buttons, monitor_rotary_encoder, monitor_pedal
from lib.jophur import files, songs, menus
from lib.jophur.jophur import Jophur

async def run_state_machine(state_machine, listener):
    while True:
        try:
            await state_machine.loop()
            await asyncio.sleep(0)
        except BaseException as err:
            print(err)

async def main():
    setlist = files.read_setlist("setlists/ftg.txt")
    jophur = Jophur(songs.all_songs)
    jophur.replace_setlist(setlist)
    listener = Listener()
    state_machine = menus.menu_state_machine({
        menus.INIT: menus.init_menu(jophur),
        menus.MAIN: menus.main_menu(jophur, listener),
        menus.BATTERY: menus.battery_menu(jophur, listener),
        menus.BLANK: menus.blank_menu(jophur, listener),
    })
    state_machine.go_to_menu(menus.INIT)

    await asyncio.gather(
        asyncio.create_task(run_state_machine(state_machine, listener)),
        asyncio.create_task(monitor_buttons(listener)),
        asyncio.create_task(monitor_rotary_encoder(listener)),
        asyncio.create_task(monitor_pedal(listener)),
    )

asyncio.run(main())

all_button_pins = [board.A2, board.D9, board.D6, board.D5, board.D10, board.D11, board.D12]
for pin in all_button_pins:
    pin_alarm = alarm.pin.PinAlarm(pin=pin, value=False, pull=True)
    alarm.exit_and_deep_sleep_until_alarms(pin_alarm)
