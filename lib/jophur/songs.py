# jophur/songs.py
from jophur import midi

AUTUMNESQUE = "Autumnesque"
BETTER_ANGELS = "Better Angels"
BUILDING_THE_LABYRINTH = "Building the Labyrinth"
CLUTTER = "Clutter"
COMPLICATED_FEELING = "Complicated Feeling"
FOLDING_IN_THIRDS = "Folding in 3rds"
FORM_WITHOUT_MEANING = "Form Without Meaning"
FUTURE_IS_GAY = "Future is Gay"
INFINITE_LOOP = "Infinite Loop"
MOONLIGHT_TRIALS = "Moonlight Trials"
NOBODY_REALLY = "Nobody Really"
SHUT_THE_WINDOWS = "Shut the Windows"
VAPORWAVE = "Vaporwave"
YOU_DIE = "You Die"

PSYCHO_KILLER = "Psycho Killer"
LIFE_ON_MARS = "Life on Mars"
NATURE_BOY = "Nature Boy"

all_songs = [
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
    VAPORWAVE,
    PSYCHO_KILLER,
    LIFE_ON_MARS,
    NATURE_BOY,
]

class PatchData:
    def __init__(self, juno=None, reverb=None, exp=None):
        self.juno_program = juno
        self.reverb_program = reverb
        self.expression = exp

    def __repr__(self):
        return f'juno={self.juno_program} reverb={self.reverb_program} expression={self.expression}'

PD = PatchData

song_program_data = {
    AUTUMNESQUE: [
        PD(
            juno=(4, 74),
            reverb=9,
            exp=(midi.KIWI_CC_DCO_LFO_MOD_AMOUNT, 0, 20)
        )
    ],

    BETTER_ANGELS: [
        PD(juno=(4, 53), reverb=15), # big square, tight room delay
        PD(juno=(4, 53), reverb=16)  # big square, shimmer
    ],

    BUILDING_THE_LABYRINTH: [
        PD(juno=(4, 54), reverb=21), # Long attack, magneto
        PD(juno=(4, 55), reverb=22), # Stairway flutes, plate
        PD(juno=(4, 57), reverb=23)  # Scary chorus'd alien, big bloom
    ],

    CLUTTER: [
        PD(juno=(4, 65), reverb=24), # Soft sawtooth with nonlin
        PD(juno=(4, 66), reverb=25), # Squarewave + long LFO delay, plate
    ],

    COMPLICATED_FEELING: [
        PD(juno=(4, 75), reverb=0),  # phasey high rez,
        PD(juno=(4, 75), reverb=0),  # thou swelst,
    ],

    FOLDING_IN_THIRDS: [
        PD(juno=(4, 71), reverb=3),  # Nasal
    ],

    FORM_WITHOUT_MEANING: [
        PD(juno=(4, 51), reverb=12), # nasal tenor, tight little plate
        PD(juno=(4, 51), reverb=13)  # Long pre-delay big reverb for ending
    ],

    FUTURE_IS_GAY: [
        PD(juno=(4, 52), reverb=27), # future is gay
    ],

    INFINITE_LOOP: [
        PD(juno=(4, 61), reverb=33), # big attack hissy fit, shimmer
        PD(juno=(4, 62), reverb=33), # tight attack "closer" rip, lil' spring
        PD(juno=(4, 63), reverb=33), # random pitch crazy laboratory
    ],

    LIFE_ON_MARS: [
        PD(juno=(4, 55), reverb=22), # Stairway flutes, plate
    ],

    MOONLIGHT_TRIALS: [
        PD(juno=(4, 72), reverb=18), # moonlight trials
    ],

    NATURE_BOY: [
        PD(juno=(4, 55), reverb=22), # Stairway flutes, plate
    ],

    NOBODY_REALLY: [
        PD(juno=(4, 67), reverb=6),  # Softer thing
    ],

    PSYCHO_KILLER: [
        PD(juno=(4, 52), reverb=27), # future is gay
    ],

    SHUT_THE_WINDOWS: [
        PD(juno=(4, 73), reverb=36), # shut the windows
    ],

    VAPORWAVE: [
        PD(juno=(4, 45), reverb=39), # Slow attack noisy nasalness,
        PD(juno=(4, 42), reverb=40), # Verse
        PD(juno=(4, 44), reverb=39), # Quick attack phasey masterpiece,
    ],

    YOU_DIE: [
        PD(juno=(4, 81), reverb=30), # Organ
        PD(juno=(4, 82), reverb=30)  # Da randomizer
    ],
}
