from random import choice
from sys import argv

def read_songs_in():
    with open(argv[1], 'r') as file:
        songlist = file.readlines()
    return songlist

def get_songs_compare(songlist):
    song1 = choice(songlist)
    songlist.remove(song1)

    song2 = choice(songlist)
    songlist.remove(song2)
    # Must remove songs after selection to avoid duplicates

    return (song1, song2, songlist)

def compare_songs(song1, song2):
    print("Which song is better?")
    print("A:", song1, sep=' ')
    print("B:", song2, sep=' ')
    ans = input(">>>").upper()

    while ans not in ('A', 'B'):
        print("That is not a valid answer, sorry.")
        ans = input(">>>")

    if ans == 'A':
        return song1
   
    else:
        return song2

def compare_three(songlist, num_to_return):
    """
    num_to_return param determine,s whether to
    return the best song or the two best songs out
    of a triple. Only accepted values are
    1 (int) and 2 (int).
    For the sake of consistency, the function
    returns either a singleton or a double, depending
    on num_to_return.
    """

    song_dict = {'A': songlist[0], 'B':songlist[1], 'C':songlist[2]}

    print("Rank these songs:")
    print("A:", songlist[0], sep=' ')
    print("B:", songlist[1], sep=' ')
    print("C:", songlist[2], sep=' ')

    first = song_dict[input("1st: ").upper()]
    second = song_dict[input("2nd: ").upper()]
    third = song_dict[input("3rd").upper()]

    if num_to_return == 1:
        return (first)
    else:
        return (fist, second)

def write_list_to_file(songlist):
    filename = "top_{}.txt".format(len(songlist))
    with open(filename, 'w') as file:
        file.writelines(songlist)

def round(songlist):
    new_songlist = []

    while len(songlist) > 3:
        song1, song2, songlist = get_songs_compare(songlist)
        # just checking that the size of songlist is decreaseing

        new_songlist.append(compare_songs(song1, song2))

    if len(songlist) == 2:
        new_songlist.append(compare_songs(songlist[0], songlist[1]))
        return new_songlist
    
    if len(new_songlist) % 2 == 0:
        best_two = compare_three(songlist, 2)
        for _ in best_two: new_songlist.append(_)
    else:
        best = compare_three(songlist, 1)
        for _ in best: new_songlist.append(_)

    return new_songlist

def main():
    songlist = read_songs_in()

    while len(songlist) > 2:
        songlist = round(songlist)
        write_list_to_file(songlist)

    best_song = compare_songs(songlist[0], songlist[1])
    with open("best_song.txt", 'w') as file:
        file.write(best_song)        

if __name__ == "__main__":
    main()
