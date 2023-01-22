# jophur
_The control ring for your waxy congress_

jophur is a lightweight MIDI message blaster, intended to solve the problem of quickly navigating between device patches on a setlist.

## Software
jophur is coded in [CircuitPython](https://github.com/adafruit/circuitpython), with libraries from [Adafruit](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/).

## Hardware
Developed on the [Adafruit Feather M4 Express](https://learn.adafruit.com/adafruit-feather-m4-express-atsamd51). Theoretically any Feather Express should work.

| M4 Pin | RP2040 Pin | M4 Code Ref | Function |
|-|-|-|-|
| A0 | GP26 (A0) | `board.A0` | Expression Pedal In |
| A1 | ? | `board.A1` | _empty_ |
| A2 | GP27 | `board.A2` | [Rotary Encoder](https://learn.adafruit.com/rotary-encoder/overview) Button |
| A3 | GP28 | `board.A3` | [Rotary Encoder](https://learn.adafruit.com/rotary-encoder/overview) Data 1 |
| A4 | GP29 | `board.A4` | [Rotary Encoder](https://learn.adafruit.com/rotary-encoder/overview) Data 2 |
| A5 | GP24 | `board.A5` | Button LED A |
| D4 | GP25 | `board.D4` | Button LED B |
| 13 | GP07 | `board.D13` | Button LED C |
| 5 | GP08 | `board.D5` | OLED A Button |
| 6 | GP09 | `board.D6` | OLED B Button |
| 9 | GP10 | `board.D9` | OLED C Button |
| 10 | GP11 | `board.D10` | Button A |
| 11 | GP12 | `board.D11` | Button B |
| 12 | GP13 | `board.D12` | Button C |
| TX | TX/GP00 (TX, UART0 TX) | `board.TX` | Midi Send |
| RX | RX/GP01 (RX, UART0 RX) | `board.RX` | Midi Receive (disabled?) |
| SCL | SCL (I2C1 SCL) | `board.i2c` | OLED |
| SDA | SDA (I2C1 SDA) | `board.i2c` | OLED |


### MIDI Environment
Right now we have a hardcoded MIDI environment
| Instrument | MIDI Channel |
|-|-|
| [Kiwi 106](https://www.kiwitechnics.com/kiwi-106.htm) | 1 |
| [Big Sky](https://www.strymon.net/support/bigsky/) | 11 |

# Development
## Getting Started
- Install [Python 3](https://www.python.org/downloads/)
- Install [pip](https://pypi.org/project/pip/)
- Install [circup](https://github.com/adafruit/circup)

### Deploy to Attached Python Board
`./script/deploy.sh`

### Read from Attached Python Booard
`./script/read.sh`
