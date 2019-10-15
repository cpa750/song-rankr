import shelve
from random import choice
from sys import argv

from eduardo.eduardo import Elo

# TODO: code ability to pickle the elo engine
# TODO: add way of counting the number of comparisons each song has been in
# Hacky method is just to make a dict and look it up each time

# TODO: this mess needs a complete rewrite (complete with classes to manage data)

class MatchCountTracker:
    """
    Simple class to track the amount of matches
    that have been made by each song
    """

    self._match_counts = {}

    def __init__(self, songlist):
        for song in songlist:
            self._match_counts[song] = 0

    def add_to_match_count(self, song):
        self._match_counts[song] += 1

    def get_match_count(self, song):
        return self._match_counts[song]


def read_songs_in():
    with open(argv[1], 'r') as file:
        songlist = file.readlines()
    return songlist

def get_songs_to_compare(songlist):
    song1 = choice(songlist)
    song2 = choice(songlist)

    while song1 == song2:
        song2 = choice(songlist)
        # Have to ensure that a song is not being
        # put against itself

    return (song1, song2)

def get_user_choice(song1, song2):
    print("Which song is better?")
    print("A:", song1, sep=' ')
    print("B:", song2, sep=' ')
    ans = input(">>>").upper()

    while ans not in ('A', 'B'):
        print("That is not a valid answer, sorry.")
        ans = input(">>>")

    if ans == 'A':
        return (song1, song2)
   
    else:
        return (song2, song1)

def write_list_to_file(songlist):
    filename = "top_{}.txt".format(len(songlist))
    with open(filename, 'w') as file:
        file.writelines(songlist)

def pickle_elo(elo_engine, match_counts):
    with shelve.open("elo") as db:
        db["elo_engine"] = elo_engine
        db["match_counts"] = match_counts
  
def main(num_of_rounds):
    songlist = read_songs_in()
    elo_engine = Elo()
    songs = [elo_engine.create_player(song) for song in songlist]

    round_num = 0

    while round_num < int(num_of_rounds):
        song1_name, song2_name = get_songs_to_compare(songlist)

        winner_name, loser_name = get_user_choice(song1_name, song2_name)
        winner = elo_engine.find_player(winner_name)
        loser = elo_engine.find_player(loser_name)

        winner.beat(loser)
        round_num += 1

    songlist_with_elo = {}
    for song_name in songlist:
        song = elo_engine.find_player(song_name)
        songlist_with_elo[song_name] = song.rating

    songs_sorted_by_elo = sorted(songlist_with_elo, key=songlist_with_elo.__getitem__)
    # Getting a list of songs sorted by their elo

    with open("ranked_songs_with_elo.txt", 'w') as file:
        for song in songs_sorted_by_elo:
            file.write(song + ' Elo: ' + str(elo_engine.find_player(song).rating) + '\n')

if __name__ == "__main__":
    main(argv[2])
