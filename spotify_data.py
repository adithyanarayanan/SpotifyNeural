import pandas as pd
from time import sleep
import tekore as tk

def get_data(cid, secret,unliked_playlist):

    app_token = tk.request_client_token(cid, secret)

    redirect_uri = 'https://example.com/callback'

    user_token = tk.prompt_for_user_token(cid,
                                          secret,
                                          redirect_uri,
                                          scope=tk.scope.every)


    spotify = tk.Spotify(app_token)
    spotify.token = user_token
    print("Crunching your likes")
    playlist = spotify.followed_playlists()
    tracks = []
    which_list = []
    for queue in playlist.items:
        # print("PROCESSING PLAYIST:", queue.name)
        p_items = spotify.playlist_items(queue.id)
        top = min(p_items.total, 100)
        for i in range(0, top):
            tracks.append(p_items.items[i].track.id)
            which_list.append(queue.name)

    offset = 0

    while True:
        number = offset + 20
        lists = spotify.saved_tracks(offset=offset)
        offset += 20
        if len(lists.items) == 0:
            break
        for saved in lists.items:
            tracks.append(saved.track.id)
            which_list.append("liked")


    music = pd.DataFrame()
    music['tracks'] = tracks
    music['playlist'] = which_list

    music['danceability'] = 0
    music['acousticness'] = 0
    music['duration_ms'] = 0
    music['energy'] = 0
    music['instrumentalness'] = 0
    music['key'] = 0
    music['liveness'] = 0
    music['loudness'] = 0
    music['mode'] = 0
    music['speechiness'] = 0
    music['tempo'] = 0
    music['time_signature'] = 0
    music['valence'] = 0

    music.set_index("tracks", inplace=True)
    music.head()

    analysis = []
    i = 0
    print("Looking at your dislikes")
    for track_id in tracks:
        i += 1
        analysis.append(spotify.track_audio_features(track_id))
        if i%100 == 0:
            # print(i, "tracks analysed")
            sleep(10)

    music["analysis"] = analysis

    for i in range(0, len(analysis)):
        track = analysis[i]
        id = track.id

        music.loc[id, 'danceability'] = track.danceability
        music.loc[id, 'acousticness'] = track.acousticness
        music.loc[id, 'duration_ms'] = track.duration_ms
        music.loc[id, 'energy'] = track.energy
        music.loc[id, 'instrumentalness'] = track.instrumentalness
        music.loc[id, 'key'] = track.key
        music.loc[id, 'liveness'] = track.liveness
        music.loc[id, 'loudness'] = track.loudness
        music.loc[id, 'mode'] = track.mode
        music.loc[id, 'speechiness'] = track.speechiness
        music.loc[id, 'tempo'] = track.tempo
        music.loc[id, 'time_signature'] = track.time_signature
        music.loc[id, 'valence'] = track.valence

    music["like"] = 1
    music.loc[(music.playlist == unliked_playlist), "like"] = 0

    features = music
    features = features.reset_index(drop=True)

    # features.to_csv("music_features.csv", index= False)
    print("Done. We know your likes and dislikes.")

    return features, spotify
