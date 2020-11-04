import neural as nn
import spotify_data as sp
import spotify_create_new as new
from time import sleep
import chequered
import outcome

cid = ""     # PASTE YOUR CLIENT ID HERE
secret = ""   # PASTE YOUR CLIENT SECRET HERE

# #
# print("Processing Playlists\n")
# features, spotify = sp.get_data(cid, secret, "Dont")
# print("It might be wiser to get a coffee, we are still crunching data\n")
# # sleep(15)
# candidates = new.create_candidates(cid, secret)
#
# print("Data Prepared\n")
# model = nn.magic("features")
# print("Neural Network Trained\n")
# print("Locked and Loaded. Finding you the new songs\n")
# final = chequered.chequered(cid, secret, model, candidates)
outcome.final(cid, secret, "final")
print("All Good. Open your spotify in a few minutes. We have couriered you a few new songs to enjoy")

