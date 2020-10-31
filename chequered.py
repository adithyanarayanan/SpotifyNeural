import pandas as pd
from time import sleep
import tekore as tk
import tensorflow as tf
from tensorflow import keras
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from imblearn.over_sampling import SMOTE
from tensorflow import keras

def chequered(cid, secret, model, candidates):
    # candidates = pd.read_csv("candidates.csv")
    print("Just one more authorization please")
    app_token = tk.request_client_token(cid, secret)

    redirect_uri = 'https://example.com/callback'

    user_token = tk.prompt_for_user_token(cid,
                                          secret,
                                          redirect_uri,
                                          scope=tk.scope.every)


    spotify = tk.Spotify(app_token)
    spotify.token = user_token

    X = candidates[candidates.columns[1:-2]]
    sc = StandardScaler()
    X = sc.fit_transform(X)

    y = model.predict(X)
    y = (y>0.5)

    candidates['Add'] = y
    # candidates.to_csv("candidates_updated.csv")
    return candidates



