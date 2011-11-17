# Authors:	Ying Liu
#		Wasif Riaz Malik	
# Mini homework for Advanced Distributed Systems Course
# EMDC KTH 2011


import random

DEBUG = False
DATAFILE = "p2p-Gnutella31.txt"

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
		starting_nodes = UIS_WR(G, 1)
	if sampling_type == 'WIS_WR':
		starting_nodes = WIS_WR(G, 1)
		
	totalsum = 0
	for i in starting_nodes:
		totalsum += BFS(sample_size, graph, i)
	avg = totalsum / len(starting_nodes)
	output_str =  'Type:'+ sampling_type+ '\tSample_size:'+str(sample_size)+'\tAverage_Degree:' + str(avg)
	print output_str


# Basic BFS function - returns the average degree of nodes
def BFS(sample_size, graph, starting_node):

	nodesList = list()
	for x in starting_node:
		nodesList.append(x)
		if len(nodesList) >= sample_size:
			break;
	
	
	#BFS logic
	index = 0
	while len(nodesList) < sample_size:
		neighbours = graph[nodesList[index]]
		for i in neighbours:
			#print 'i:'+str(i)
			if i not in nodesList:
				nodesList.append(i)
			if len(nodesList) >= sample_size:
				break;
		index += 1
		

	
	##### calculate the average with n = sample_size
	totalsum = 0
	avg = 0
	for elements in nodesList:
		totalsum += len(graph[elements])
	avg = totalsum/len(nodesList)
	totalsum = 0
	
	if DEBUG == True:
		outputstr = 'BFS Average: ' + str(avg)
		print outputstr

	return avg


# Calculates the actual average of the dataset
def actualAverage(graph):
	mysum = 0
	for i in graph:
		mysum += len(graph[i])
	print '** Actual_Average_Degree: ' +str(mysum/len(graph))
	

# startup message
def startupMessage(G):
	print "\n\n"
	print "** Dataset: " + DATAFILE
	print '** Num_nodes_in_dataset: ' + str(len(G))
	actualAverage(G)
	print "\n\n"



# Load the graph
G = load_graph(DATAFILE)


# print some stuff about the dataset
startupMessage(G);

# Run the BFS using UIS_WR
for x in range(10, 60000, 10000):
	runBFS(x, G, 'UIS_WR')


# Run the BFS using WIS_WR
for x in range(10, 60000, 10000):
	runBFS(x, G, 'WIS_WR')
