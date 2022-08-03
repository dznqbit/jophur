# jophur/display.py
import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

class MockText:
    text: "hello"

def init(init_text):
    try:
        displayio.release_displays()

        i2c = board.I2C()
        display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
        display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

        splash = displayio.Group()
        display.show(splash)

        clear_screen_bitmap = displayio.Bitmap(128, 32, 1)
        clear_screen_palette = displayio.Palette(1)
        clear_screen_palette[0] = 0x000000  # Black
        clear_screen = displayio.TileGrid(
            clear_screen_bitmap, pixel_shader=clear_screen_palette, x=5, y=4
        )
        splash.append(clear_screen)

        text_area = label.Label(
            terminalio.FONT, text=init_text, color=0xFFFF00, x=0, y=3
        )
        splash.append(text_area)
        return text_area
    except Exception as error:
        print(f"Display Error {type(error)} {error}")
        return MockText()
