import networkx as nx
import matplotlib.pyplot as plt

def WPGMA(file_name):
	#Read and parse file contents
	file_contents = [line.rstrip('\r\n') for line in open(file_name)]
	working_matrix = []

	for row in file_contents:
		parse = row.split(' ')
		working_matrix.append(parse)
		
	parsed_matrix =[]
	for row in working_matrix:
		temp = []
		for element in row:
			if element.isdigit() == True:	
				temp.append(float(element))
			else:
				temp.append(element)
		parsed_matrix.append(temp)
	#print(parsed_matrix)
	#working_row = []
	
	#Function to print current matrix at each reduction step

	def print_matrix():
		for row in parsed_matrix:
			print(row)

	#Printing the initial matrix
	print('Initial interspecies distance matrix:')
	print_matrix()

	#Initializing a NetworkX graph
	G = nx.Graph()

	while len(parsed_matrix) > 2:
		#Find minimum term in matrix to be clustered together
		minterm = parsed_matrix[2][1]
		for row in parsed_matrix[2:]:
			for element in row[1:parsed_matrix.index(row)]:
				if element < minterm:
					minterm = element

		#Find indices (row-column) of minimum term, and add appropriate cluster elements to phylogenetic tree graph
		for row in parsed_matrix:
			if minterm in row:
				cluster_a = row[0]
				cluster_b = parsed_matrix[0][row.index(minterm)]

		#Build graph in NetworkX

		if cluster_a not in G:
			G.add_node(cluster_a)
				
		if cluster_b not in G:
			G.add_node(cluster_b)
		
		cluster_ab = cluster_a + cluster_b
				
		G.add_node(cluster_ab)
		G.add_edges_from([(cluster_a, cluster_ab), (cluster_b, cluster_ab)])
				

		#Calculate values of new clustered row/column 
		cluster = []
		cluster.append(cluster_ab)
	

		for row in parsed_matrix[1:]:
			if row[0] == cluster_a:
				a_row = row[1:]
			
			elif row[0] == cluster_b:
				b_row = row[1:]

		i = 0
		while i < len(a_row):
			if a_row[i] != 0 and a_row[i] != minterm:
				new_distance = ((a_row[i]) + (b_row[i]))/2 
				cluster.append(new_distance)
			elif a_row[i] == minterm:
				cluster.append(float(0))
			i +=1

		#Remove unneccessary column

		col_adjust = parsed_matrix[0].index(cluster_a)

		for row in parsed_matrix:
			del row[col_adjust]


		#Remove unnecessary row

		for row in parsed_matrix[1:]:
			if row[0] == cluster_a:
				parsed_matrix.remove(row)
			#Filling new row with clustered species data	
			elif row[0] == cluster_b:
				parsed_matrix.insert(parsed_matrix.index(row),cluster)
				parsed_matrix.remove(row)


		#Filling new column with clustered species data	

		col_adjust = parsed_matrix[0].index(cluster_b)
		i=0
		while i < len(cluster):
			for row in parsed_matrix:
				row[col_adjust] = cluster[i]
				i +=1
		
		#Print new matrix
		print()
		print('Updated matrix after clustering together species ' + cluster_a + ' and ' + cluster_b +':')
		print_matrix()

	print()
	print('Finished constructing phylogenetic tree using WPGMA algorithm.')

	nx.draw(G,with_labels=True)

	plt.savefig('tree.png')
	plt.show()
	
	