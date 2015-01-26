import networkx as nx

class Community(object):
	def __init__(self, subgraph, G):
		self.subgraph = subgraph
		self.ns = self.subgraph.number_of_nodes()
		self.ms = self.subgraph.number_of_edges()
		self.cs = sum([len(G[n]) for n in self.subgraph.nodes()]) - self.ms
		self.du = G.degree(self.subgraph.nodes())
	
	def internal_density(self):
		return float(self.ms) / self.ns * (self. ns - 1) / 2.0
	
	def edges_inside(self):
		return float(self.ms)
	
	def average_degree(self):
		return 2 * float(self.ms) / self.ns
	
	def fraction_over_median_degree(self, dm):
		return len([d for d in self.subgraph.degree() if d > dm]) / float(self.ns)

	def triangle_participation_ratio(self):
		count = 0.0
		for u in self.subgraph.nodes():
			for v in self.subgraph.nodes():
				if u != v:
					for w in self.subgrap.nodes():
						if u != w and v != w:
							if self.subgraph.has_edge(u,v) and \
								self.subgraph.has_edge(v, w) and \
								self.subgraph.has_edge(w, u):
									count += 1
		return count / (3 * self.ns)
	
	def expansion(self):
		return float(self.cs) / self.ns
	
	def cut_ratio(self, n):
		return float(cs) / (self.ns * (n - self.ns))
	
	def conductance(self):
		return float(self.cs) / (2 * self.ms + self.cs)
	
	def phi(self, G):
		vol = sum(self.du)
		return float(self.cs) / min(vol, 2 * G.number_of_edges() - vol)
	
	def normalized_cut(self, m):
		return float(self.cs) / (2 * self.ms + self.cs) + float(self.cs) / (2 * (m - self.ms) + self.cs)

def read_communities(file_name, G, length=3):
	communities = []
	with open(file_name) as f:
		for l in f:
			S = G.subgraph(map(int, l.split()))
			c = Community(S, G)
			if S.number_of_nodes() >= length:
				communities.append(c)
	return communities

