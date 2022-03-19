# jophur
_The control ring for your waxy congress_

jophur is a lightweight MIDI message blaster, intended to solve the problem of quickly navigating between device patches on a setlist.

## Software
jophur is coded in [CircuitPython](https://github.com/adafruit/circuitpython), with libraries from [Adafruit](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/).

## Hardware
Developed on the [Adafruit Feather M4 Express](https://learn.adafruit.com/adafruit-feather-m4-express-atsamd51). Theoretically any Feather Express should work.

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
