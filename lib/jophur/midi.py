# jophur/midi.py
import time
import busio
import board
import usb_midi
import adafruit_midi

from adafruit_midi.timing_clock import TimingClock
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.control_change import ControlChange
from adafruit_midi.midi_message import MIDIUnknownEvent
from adafruit_midi.program_change import ProgramChange

def initMidi(listen: True):

    uart = busio.UART(
        board.TX,
        board.RX if listen else None,
        baudrate=31250,
        timeout=0.001
    )

    return adafruit_midi.MIDI(
        midi_in=uart,
        midi_out=uart,
        in_channel=0,
        out_channel=0,
        debug=False
    )

def junoCC(midi, cc, value):
    channel = 0
    change = ControlChange(cc, value)                # Kiwi 106:
    midi.send(change, channel)

# bank:     HUMAN READABLE bank int, eg 1
# program:  HUMAN READABLE program number int, eg 71
def junoProgram(midi, bank, program):
    channel = 0

    midi_bank = (bank - 1) // 2

    midi_program_msd = program // 10 - 1
    midi_program_lsd = (program - 1) % 10
    midi_program = midi_program_msd * 8 + midi_program_lsd + ((bank - 1) % 2) * 64

    changes = [
        ControlChange(0, 0),                # Kiwi 106: Bank Select HSB (1 = Select pattern, 2 = Select seq)
        ControlChange(32, midi_bank),       # Kiwi 106: Bank Select LSB (0 = Patches 1-128, 1 = Patches 129-256, 2 = Patches 257-384, 3 = Patches 385-512)
        ControlChange(119, midi_program)    # Kiwi 106: Backdoor Program Change – we like this CC, Kiwi appears to boot with "ignore Program Change"
    ]

    for change in changes:
        midi.send(change, channel)

class Enum(object):
    def __init__(self, names):
        for number, name in enumerate(names.split()):
            setattr(self, name, number)

class KiwiCC(Enum):
    MOD_WHEEL_AMOUNT = 01
    VOLUME = 07

    DCO_PWM_MOD_AMOUNT = 10
    DCO_LFO_MOD_AMOUNT = 12

    LFO_1_RATE = 19
    LFO_1_DELAY = 20

    LFO_2_RATE = 22
    LFO_2_DELAY = 23

    LOW_PASS_CUTOFF_FREQ = 41
    LOW_PASS_Q = 42
    LOW_PASS_LFO_AMOUNT = 45

    INTERNAL_CLOCK_RATE=72

# program: HUMAN READABLE bank int, eg 0.
#          TODO support strings like '00A'
def reverbProgram(midi, program):
    channel = 10

    midi.send(ProgramChange(program), channel);

def playNote(midi):
    midi.send(NoteOn(48, 20))   # play note
    time.sleep(1.0)             # hold note
    midi.send(NoteOff(48, 0))   # release note

def logMidiIn(midi):
    msg_in = midi.receive()  # non-blocking read
    if msg_in is not None:
        print(f"MIDI ${msg_in}")
        d = midi.send(msg_in)
        print(d)
