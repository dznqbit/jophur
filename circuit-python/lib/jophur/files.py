from lib.jophur import songs

def fuzzy_find(setlist_song_name):
    for song_name in songs.all_songs:
        if setlist_song_name.lower() == song_name.lower():
            return song_name

    return None

def read_setlist(filename):
    with open(filename, "r", encoding="utf-8") as f:
        song_names = [line.strip() for line in f.readlines()]
        return [fuzzy_find(s) for s in song_names]
