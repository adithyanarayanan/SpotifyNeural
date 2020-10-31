import pandas as pd
from time import sleep
import tekore as tk

def create_candidates(cid, secret):
    app_token = tk.request_client_token(cid, secret)

    redirect_uri = 'https://example.com/callback'

    user_token = tk.prompt_for_user_token(cid,
                                          secret,
                                          redirect_uri,
                                          scope=tk.scope.every)

    spotify = tk.Spotify(app_token)
    spotify.token = user_token



    artists = []
    offset = 0
    while True:
        top_artists = spotify.current_user_top_artists(time_range='medium_term', limit=20, offset=offset)
        offset += 20
        if len(top_artists.items) == 0:
            break
        for artist in top_artists.items:
            artists.append(artist.id)
    print("Artists Shortlisted")
    sleep(2.5)


    related = {}
    for artist in artists:
        temp = []
        related_artists = spotify.artist_related_artists(artist)
        for related_artist in related_artists:
            temp.append(related_artist.id)
        related[artist] = temp
    print("Related Artists Shortlisted")
    sleep(2.5)

    analyzed = set()
    for k, v in related.items():
        analyzed.add(k)
        for i in v:
            analyzed.add(i)


    tracks_to_validate = []
    i = 0
    for person in analyzed:
        temp_tracks = spotify.artist_top_tracks(person, market='US')
        i += 1
        if i % 100 == 0:
            print(i, "artists analyzed")
            sleep(7.5)
        for track in temp_tracks:
            tracks_to_validate.append(track.id)

    print("Done. Top Tracks acquired from", len(analyzed), "artists")

    tracks_to_validate = set(tracks_to_validate)

    v_analysis = []
    track_final = []
    i = 0



    for track_id in tracks_to_validate:
        if i == 755 or i == 756: continue
        # print(i)
        track_final.append(track_id)
        i += 1
        temp = spotify.track_audio_features(track_id)
        v_analysis.append(temp)

        if i == 500: break

        if i % 100 == 0:
            # print(i, "tracks analysed")
            sleep(10)

    check = pd.DataFrame()
    check['tracks'] = track_final



    check['playlist'] = 0
    check['danceability'] = 0
    check['acousticness'] = 0
    check['duration_ms'] = 0
    check['energy'] = 0
    check['instrumentalness'] = 0
    check['key'] = 0
    check['liveness'] = 0
    check['loudness'] = 0
    check['mode'] = 0
    check['speechiness'] = 0
    check['tempo'] = 0
    check['time_signature'] = 0
    check['valence'] = 0
    check['analysis'] = v_analysis

    check.set_index("tracks", inplace=True)

    for i in range(0, len(v_analysis)):
        track = v_analysis[i]
        id = track.id

        check.loc[id, 'danceability'] = track.danceability
        check.loc[id, 'acousticness'] = track.acousticness
        check.loc[id, 'duration_ms'] = track.duration_ms
        check.loc[id, 'energy'] = track.energy
        check.loc[id, 'instrumentalness'] = track.instrumentalness
        check.loc[id, 'key'] = track.key
        check.loc[id, 'liveness'] = track.liveness
        check.loc[id, 'loudness'] = track.loudness
        check.loc[id, 'mode'] = track.mode
        check.loc[id, 'speechiness'] = track.speechiness
        check.loc[id, 'tempo'] = track.tempo
        check.loc[id, 'time_signature'] = track.time_signature
        check.loc[id, 'valence'] = track.valence

    # check.to_csv("candidates.csv")
    print("Done. You have", len(track_final), "candidates from which we will handpick what you might like")

    return check




