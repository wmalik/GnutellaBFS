import random

DEBUG = False

# Loads a graph from a filename
def load_graph(fname):
	fr = open(fname, 'r')
	G = {}   # dictionary: node -> set of neighbors
	for line in fr:
		if not line.startswith('#'):
			a,b = map(int, line.split())    
			if a not in G:  G[a] = set()
			if b not in G:  G[b] = set()        
			G[a].add(b)
			G[b].add(a)    
	fr.close()    
	return G

# Uniform Independence Sample
def UIS_WR(I,n):
	return [ random.choice(I) for i in xrange(n)  ]

# Weighted Independence Sample
def WIS_WR(graph, n): 
	I_W = list()
	for key in graph:
		degree = len(graph[key])
		IWtuple = [key, degree]
		I_W.append(IWtuple)
	resultSet = list()	
	for i in range(n):
		weight_sum = sum(weight for item,weight in I_W)
		n = random.uniform(0, weight_sum)

		for item, weight in I_W:
			if n < weight:
				break
			n = n - weight
		resultSet.append(graph[item])
	return resultSet 

# Wrapper function for calling BFS multiple times
def runBFS(sample_size, graph, sampling_type):
	
	if sampling_type == 'UIS_WR':
		starting_nodes = UIS_WR(G, 100)
	if sampling_type == 'WIS_WR':
		starting_nodes = WIS_WR(G, 100)
		
	totalsum = 0
	for i in starting_nodes:
		totalsum += BFS(sample_size, graph, i)
	avg = totalsum / len(starting_nodes)
	output_str =  'Type:'+ sampling_type+ '\tSample_size:'+str(sample_size)+'\tAverage_Degree:' + str(avg)
	print output_str


# Basic BFS function
def BFS(sample_size, graph, starting_node):

	nodesList = list()
	for x in starting_node:
		nodesList.append(x)
		if len(nodesList) >= sample_size:
			break;
	
	
	index = 0
	while len(nodesList) < sample_size:
		neighbours = graph[nodesList[index]]
		for i in neighbours:
			if i not in starting_node:
				nodesList.append(i)
			if len(nodesList) >= sample_size:
				break;
		index += 1

	
	##### get children of starting_node
	totalsum = 0
	avg = 0
	for elements in nodesList:
		totalsum += len(graph[elements])
	avg = totalsum/sample_size
	
	if DEBUG == True:
		outputstr = 'BFS Average: ' + str(avg)
		print outputstr

	return avg




	
# Load the graph
G = load_graph("p2p-Gnutella31.txt")

# Run the BFS using UIS_WR
for x in range(20, 5000, 500):
	runBFS(x, G, 'UIS_WR')


# Run the BFS using WIS_WR
for x in range(20, 5000, 500):
	runBFS(x, G, 'WIS_WR')
