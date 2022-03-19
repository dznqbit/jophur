import rotaryio
import board
import neopixel
import digitalio
from jophur import display
from jophur.midi import initMidi, playNote, reverbProgram, junoProgram

midi = initMidi()

# Data
FORM_WITHOUT_MEANING = "Form Without Meaning"
FUTURE_IS_GAY = "Future is Gay"
BETTER_ANGELS = "Better Angels"
BUILDING_THE_LABYRINTH = "Building the Labyrinth"
INFINITE_LOOP = "Infinite Loop"
CLUTTER = "Clutter"
NOBODY_REALLY = "Nobody Really"
FOLDING_IN_THIRDS = "Folding in 3rds"
MOONLIGHT_TRIALS = "Moonlight Trials"
SHUT_THE_WINDOWS = "Shut the Windows"
COMPLICATED_FEELING = "Complicated Feeling"
AUTUMNESQUE = "Autumnesque"
YOU_DIE = "You Die"
IN_SLOW_MOTION = "In Slow Motion"

songs = [
    FORM_WITHOUT_MEANING,
    FUTURE_IS_GAY,
    BETTER_ANGELS,
    BUILDING_THE_LABYRINTH,
    INFINITE_LOOP,
    CLUTTER,
    NOBODY_REALLY,
    FOLDING_IN_THIRDS,
    MOONLIGHT_TRIALS,
    SHUT_THE_WINDOWS,
    COMPLICATED_FEELING,
    AUTUMNESQUE,
    YOU_DIE,
    IN_SLOW_MOTION,
]

song_program_data = {
    FORM_WITHOUT_MEANING: ((4, 51), 12),
    FUTURE_IS_GAY: ((4, 52), 27),
    BETTER_ANGELS: ((4, 53), 15),
    BUILDING_THE_LABYRINTH: ((4, 54), 21),
    INFINITE_LOOP: ((4, 61), 33),
    CLUTTER: ((4, 65), 24),
    NOBODY_REALLY: ((4, 67), 6),
    FOLDING_IN_THIRDS: ((4, 71), 3),
    MOONLIGHT_TRIALS: ((4, 72), 18),
    SHUT_THE_WINDOWS: ((4, 73), 36),
    COMPLICATED_FEELING: ((4, 75), 0),
    AUTUMNESQUE: ((4, 74), 9),
    YOU_DIE: ((4, 81), 30)
}



# Rotary Encoder
button = digitalio.DigitalInOut(board.A2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

encoder = rotaryio.IncrementalEncoder(board.A4, board.A3)
position = encoder.position
last_position = None
button_state = None
# END Rotary Encoder

text_area = display.init()

while True:
    if not button.value and button_state is None:
        button_state = "pressed"
        text_area.text = f"{songs[position]}!"
        print(text_area.text)

    if button.value and button_state == "pressed":
        button_state = None

    position = encoder.position % len(songs)
    if last_position is None or position != last_position:
        new_song = songs[position]
        text_area.text = f"{new_song}"

        song_data = song_program_data.get(new_song)
        if (song_data):
            ((juno_bank, juno_program), reverb_program) = song_data
            print(f"{new_song}\n\tJuno {juno_program}\n\tReverb {reverb_program}");

            junoProgram(midi, juno_bank, juno_program);
            reverbProgram(midi, reverb_program);

        playNote(midi)

    last_position = position
