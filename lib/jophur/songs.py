# jophur/songs.py

# Song Names
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

# Program Data

# [(((Juno Bank, Juno Patch), Big Sky Patch), (B), (C)],
song_program_data = {
    AUTUMNESQUE: ((4, 74), 9),

    BETTER_ANGELS: [
        ((4, 53), 15), # big square, tight room delay
        ((4, 53), 16)  # big square, shimmer
    ],

    BUILDING_THE_LABYRINTH: [
        ((4, 54), 21), # Long attack, magneto
        ((4, 55), 22), # Stairway flutes, plate
        ((4, 57), 23)  # Scary chorus'd alien, big bloom
    ],

    CLUTTER: [
        ((4, 65), 24), # Soft sawtooth with nonlin
        ((4, 66), 25), # Squarewave + long LFO delay, plate
    ],

    COMPLICATED_FEELING: [
        ((4, 75), 0),  # phasey high rez,
        ((4, 75), 0),  # thou swelst,
    ],

    FOLDING_IN_THIRDS: [
        ((4, 71), 3),  # Nasal
    ],

    FORM_WITHOUT_MEANING: [
        ((4, 51), 12), # nasal tenor, tight little plate
        ((4, 51), 13)  # Long pre-delay big reverb for ending
    ],

    FUTURE_IS_GAY: [
        ((4, 52), 27), # future is gay
    ],

    INFINITE_LOOP: [
        ((4, 61), 33), # big attack hissy fit, shimmer
        ((4, 62), 33), # tight attack "closer" rip, lil' spring
        ((4, 63), 33), # random pitch crazy laboratory
    ],

    MOONLIGHT_TRIALS: [
        ((4, 72), 18), # moonlight trials
    ],

    NOBODY_REALLY: [
        ((4, 67), 6),  # Softer thing
    ],

    SHUT_THE_WINDOWS: [
        ((4, 73), 36), # shut the windows
    ],

    YOU_DIE: [
        ((4, 81), 30), # Organ
        ((4, 81), 30)  # Da randomizer
    ]
}
