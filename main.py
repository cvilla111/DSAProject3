import pylast
import time
import random

API_KEY = "7008b5589d58885ace36d3221e86cbd0"
API_SECRET = "a3f47c877288ee66e42a15bc603cffb6"
network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

def make_playlist(name):
    artist = network.get_artist(name)
    similar = artist.get_similar(limit = 1000)
    popularity_map = {}
    for it in similar:
        current = it.item
        popularity_score = current.get_listener_count() or 0
        track_list = current.get_top_tracks(limit = 1000)
        tracks = []
        for track in track_list:
            tracks.append(track.item.title)
        if tracks:
            popularity_map.setdefault(popularity_score, []).extend(tracks)

    scores = sorted(popularity_map.items())
    split_point = int(len(scores) * 0.30)
    popular_scores = scores[len(scores) - split_point:]
    remaining_scores = scores[:len(scores) - split_point]

    used = set()
    def insert_song(bucket):
        while True:
            popularity_score, tracks = random.choice(bucket)
            track = random.choice(tracks)
            if track not in used:
                used.add(track)
                return track

    playlist = []
    for it in range(int(250 * 0.70)):
        playlist.append(insert_song(popular_scores))
    for it in range(int(250 * 0.30)):
        playlist.append(insert_song(remaining_scores))

    random.shuffle(playlist)
    return playlist

def main():
    name = input("Which artist would you like to base your playlist on?\n")
    start = time.time()
    playlist = make_playlist(name)
    for track in playlist:
        print(track)
    elapsed = time.time() - start
    print(f"Time: {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()