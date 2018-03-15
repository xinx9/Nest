import person
import networkx as nx
import matplotlib.pyplot as plt
from person import *
import pickle
import tweepy



G = nx.Graph()


starting_id = 172150972

x = PersonNode(starting_id)
x.reset_auth_and_key(1)
x.set_edges()
totalNum = len(x.edges)
count = 0
def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

save_object(x, "Target.pkl")

for i in x.edges:
    try:
        print("On user: @{}\t\t{}/{}".format(i.screenName, count, totalNum))
        tmp_followers = i.get_followers()
        tmp_followees = i.get_followees()
        numMutual = len(set(tmp_followees).intersection(tmp_followers))
        if numMutual > 450:
            print("@{}'s mutuals are too large, probably not a person.".format(i.screenName))
            continue
        else:
            i.set_edges()
    except tweepy.error.TweepError:
        print("@{} is private".format(i.screenName))
    count += 1

save_object(x, "FullData.pkl")