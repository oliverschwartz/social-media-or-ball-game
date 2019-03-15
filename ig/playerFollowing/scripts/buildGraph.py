import os
import networkx as nx

G = nx.DiGraph()

# iterate over all processed csvs
os.chdir("../processed")
for file in os.listdir():
    G.add_node()