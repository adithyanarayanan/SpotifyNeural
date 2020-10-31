from time import sleep
import pandas as pd
import tekore as tk
import tensorflow as tf

def final(cid, secret, candidates):
    candidates = pd.read_csv("candidates_updated.csv")
    # print(candidates.head())
    shortlist = candidates[candidates["Add"] == True]

    


    app_token = tk.request_client_token(cid, secret)

    redirect_uri = 'https://example.com/callback'

    user_token = tk.prompt_for_user_token(cid,
                                          secret,
                                          redirect_uri,
                                          scope=tk.scope.every)

    spotify = tk.Spotify(app_token)
    spotify.token = user_token

    user_id = spotify.current_user().id
    try_these = spotify.playlist_create(user_id, "Try These", public=False, description='A playlist curated by a neural network')


    if len(shortlist) > 10:
        picks = shortlist.sample(n = 10)
    else:
        return "Apologies. We couldn't find the right set of tracks for you right now, please try a bit later"


    uris = [spotify.track(t).uri for t in picks.tracks]

    spotify.playlist_add(try_these.id, uris=uris)

    print("That's all folks. If your listening patterns change soon, drop by and we can suggest some more songs")

