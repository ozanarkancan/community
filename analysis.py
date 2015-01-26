import networkx as nx
import numpy as np
from community import *
import operator

def approx_page_rank(G, seed, beta, epsilon):
	r = np.zeros((max(G.nodes()), ), dtype="float32")
	q = r.copy()
	q[seed - 1] = 1.

	candidates = [seed]
	track = {seed : 1}
	track_r = {}

	while len(candidates) > 0:
		#Choose any vertex u where q_u / d_u >= epsilon
		u = candidates[np.random.randint(len(candidates))]

		#Push u, r, q
		r_prime = r.copy()
		q_prime = q.copy()

		r_prime[u - 1] = r[u - 1] + (1 - beta) * q[u - 1]
		track_r[u] = r_prime[u - 1]
		q_prime[u - 1] = 0.5 * beta * q[u - 1]

		for v in G[u].keys():
			q_prime[v - 1] = q[v - 1] + 0.5 * beta * (q[u - 1]/G.degree(u))
			track[v] = q_prime[v - 1]
		
		r = r_prime.copy()
		q = q_prime.copy()
		candidates = [k for k in track.keys() if q[k - 1] / G.degree(k) >= epsilon]
	return r, track_r

def detect_community(G, seed, beta, epsilon, alpha):
	r, track_r = approx_page_rank(G, seed, beta, epsilon)
	nonzero=100
	sorted_r = sorted(track_r.items(), key=operator.itemgetter(1), reverse=True)

	k_star = 0
	k = 0

	best_score = float("inf")
	prev_scores = [float("inf"), float("inf"), float("inf")]
	curr_score = float("inf")

	while k == 0 or (curr_score < alpha * best_score and k < nonzero):
		k += 1
		S = G.subgraph(map(lambda t: t[0], sorted_r[:k]))
		c = Community(S, G)
		curr_score = c.conductance()
		#curr_score = c.triangle_participation_ratio()

		if curr_score < best_score:
			best_score = curr_score
			k_star = k
		
		nums = map(lambda x: x <= curr_score, prev_scores).count(True)

		if nums == 3:
			break
	
	return Community(G.subgraph(map(lambda t: t[0], sorted_r[:k_star])), G)

#c1 ground truth, c2 predicted

def evaluate_f1(c1, c2):
	c1_nodes = c1.subgraph.nodes()
	c2_nodes = c2.subgraph.nodes()

	relv = len(filter(lambda v: v in c1_nodes, c2_nodes))
	nrelv = len(c1_nodes) - relv
	irelv = len(c2_nodes) - relv
	
	return nrelv, relv, irelv
