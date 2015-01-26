import networkx as np
from community import *
from analysis import *
import argparse
from datetime import datetime

def get_arg_parser():
	parser = argparse.ArgumentParser(prog="experiment")
	parser.add_argument("--data", default="amazon")
	parser.add_argument("--epsilon", default=0.005, type=float)
	parser.add_argument("--beta", default=0.75, type=float)
	parser.add_argument("--alpha", default=1.2, type=float)

	return parser

if __name__ == "__main__":
	parser = get_arg_parser()
	args = vars(parser.parse_args())

	data_name = args['data']
	epsilon = args['epsilon']
	alpha = args['alpha']
	beta = args['beta']

	file_name = "data/" + data_name + "/com-" + data_name + "."

	print "...reading graph"
	with open(file_name + "ungraph.txt", "rb") as f:
		G = nx.read_adjlist(f, nodetype=int)
	
	print "...reading ground-truth communities"
	communities = read_communities(file_name + "all.cmty.txt", G)

	ir = 0.
	r = 0.
	nr = 0.
	
	index = 0
	n_com = len(communities)

	print "...searching communities"
	print "Started: " + str(datetime.now())
	for c in communities:
		index += 1
		#print index		
		if index % 2000 == 0:
			print "%i / %i" % (index, n_com)

		ns = c.subgraph.nodes()
		seed = ns[np.random.randint(len(ns))]
		founded = detect_community(G, seed, beta, epsilon, alpha)
		nrelv, relv, irelv = evaluate_f1(c, founded)
		
		print "c: ", c.subgraph.nodes()
		print "f: ", founded.subgraph.nodes()
		print (nrelv, relv, relv)


		nr += nrelv
		r += relv
		ir += irelv
	print "End: " + str(datetime.now())
	recall = r / (nr + r)
	precision = r / (ir + r)
	f1 = 2 * recall * precision / (precision + recall)
	
	print "Results for " + data_name
	print "Precision: ", precision
	print "Recall: ", recall
	print "F1: ", f1
	print "Parameters epsilon: %f beta: %f alpha: %f" % (epsilon, beta, alpha)

