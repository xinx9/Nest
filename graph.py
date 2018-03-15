import pickle
import networkx as nx
import matplotlib.pyplot as plt
from person import *
import tweepy

with open('FullData.pkl', 'rb') as f:
    data = pickle.load(f)

G = nx.Graph()

# First iteration:

G.add_node(data.screenName, node_color='#4286f4') # Add initial node

for i in data.edges:
    G.add_node(i.screenName)
    G.add_edge(i.screenName, data.screenName)
    for x in i.edges:
        G.add_node(x.screenName)
        G.add_edge(x.screenName, i.screenName)



nx.draw(G, with_labels=True, node_size=100)
plt.show()