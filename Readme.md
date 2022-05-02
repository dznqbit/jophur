# jophur
_The control ring for your waxy congress_

jophur is a lightweight MIDI message blaster, intended to solve the problem of quickly navigating between device patches on a setlist.

## Software
jophur is coded in [CircuitPython](https://github.com/adafruit/circuitpython), with libraries from [Adafruit](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/).

## Hardware
Developed on the [Adafruit Feather M4 Express](https://learn.adafruit.com/adafruit-feather-m4-express-atsamd51). Theoretically any Feather Express should work.

| Board Pin Name | Software Pin Name | Function |
|-|-|-|
| A0 | `board.A0` | Expression Pedal In |
| A1 | `board.A1` | _empty_ |
| A2 | `board.A2` | [Rotary Encoder](https://learn.adafruit.com/rotary-encoder/overview) Button |
| A3 | `board.A3` | [Rotary Encoder](https://learn.adafruit.com/rotary-encoder/overview) Data 1 |
| A4 | `board.A4` | [Rotary Encoder](https://learn.adafruit.com/rotary-encoder/overview) Data 2 |
| A5 | `board.A5` | Button LED A |
| D4 | `board.D4` | Button LED B |
| 5 | `board.D5` | OLED A Button |
| 6 | `board.D6` | OLED B Button |
| 9 | `board.D9` | OLED C Button |
| 10 | `board.D10` | Button A |
| 11 | `board.D11` | Button B |
| 12 | `board.D12` | Button C |
| 13 | `board.D13` | Button LED C |
| TX | `board.TX` | Midi Send |
| RX | `board.RX` | Midi Receive (disabled?) |
| SCL | `board.i2c` | OLED |
| SDA | `board.i2c` | OLED |


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
