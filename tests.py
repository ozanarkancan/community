import networkx as nx
from community import *
import numpy as np
from analysis import *

def reading_graph():
	file_name = "data/youtube/com-youtube.ungraph.txt"
	f = open(file_name, "rb")

	print "... reading the undirected graph from " + file_name
	G = nx.read_adjlist(f)
	f.close()

	print "#nodes: %i #edges: %i" % (G.number_of_nodes(), G.number_of_edges())

def reading_communities():
	file_name = "data/dblp/com-dblp."

	with open(file_name + "ungraph.txt", "rb") as f:
		G = nx.read_adjlist(f, nodetype=int)
	
	communities = read_communities(file_name + "all.cmty.txt", G)

	print "#communities: ", len(communities)

#reading_graph()
#reading_communities()

def finding_community():
	file_name = "data/amazon/com-amazon."

	print "...reading graph"
	with open(file_name + "ungraph.txt", "rb") as f:
		G = nx.read_adjlist(f, nodetype=int)
	
	print "...reading communities"
	communities = read_communities(file_name + "all.cmty.txt", G)

	alpha = 1.2
	beta = 0.8
	epsilon = 0.001
	
	c = communities[10]
	ns = c.subgraph.nodes()

	print ns
	
	seed = ns[np.random.randint(len(ns))]
	print seed

	founded = detect_community(G, seed, beta, epsilon, alpha)

	print "Founded: ", founded.subgraph.nodes()

	nrel,rel, irel = evaluate_f1(c, founded)
	print (nrel, rel, irel)

finding_community()


