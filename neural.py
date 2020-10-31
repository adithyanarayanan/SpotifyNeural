import pandas as pd
import tensorflow as tf
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from imblearn.over_sampling import SMOTE
from tensorflow import keras

tf.random.set_seed(123)

def magic(features):
    features = pd.read_csv("music_features.csv")
    features.drop_duplicates(inplace=True)

    X = features[features.columns[1:-2]]
    y = features[features.columns[-1]]

    sc = StandardScaler()
    X = sc.fit_transform(X)

    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size = 0.2, random_state=5)

    sm = SMOTE(random_state = 2)
    X_train_res, y_train_res = sm.fit_sample(X_train, y_train.ravel())

    log = LogisticRegression()
    log.fit(X_train_res, y_train_res)

    # print("Logistic Regression Train Accuracy", log.score(X_train_res, y_train_res))
    # print("Logistic Regression Test Accuracy", log.score(X_test, y_test))

    y_pred_log = log.predict(X_test)
    # print("Confusion Matrix Logit", confusion_matrix(y_test, y_pred_log))

    model = keras.Sequential(
        [
            keras.layers.Dense(4, activation="relu", name="layer1"),
            # keras.layers.Dense(5, activation="relu", name="layer2"),
            keras.layers.Dense(1, activation = "sigmoid", name="layer3"),
        ]
    )

    opt = keras.optimizers.Adam(learning_rate=0.0001)

    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=['accuracy'])

    model.fit(X_train_res, y_train_res, epochs=200, verbose=0)

    training_loss = model.evaluate(X_train_res, y_train_res)
    # print("Training Loss", training_loss)

    test_loss = model.evaluate(X_test, y_test)
    # print("Test Loss", test_loss)

    y_pred = model.predict(X_test)
    y_pred_2 = (y_pred > 0.5)

    # print(confusion_matrix(y_test, y_pred_2))



    print("Preferences locked and loaded, finding new songs")
    return model


