# jophur/songs.py
from jophur import midi

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

    MOONLIGHT_TRIALS: [
        PD(juno=(4, 72), reverb=18), # moonlight trials
    ],

    NOBODY_REALLY: [
        PD(juno=(4, 67), reverb=6),  # Softer thing
    ],

    SHUT_THE_WINDOWS: [
        PD(juno=(4, 73), reverb=36), # shut the windows
    ],

    YOU_DIE: [
        PD(juno=(4, 81), reverb=30), # Organ
        PD(juno=(4, 82), reverb=30)  # Da randomizer
    ]
}
