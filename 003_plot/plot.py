import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# create a random graph
G = nx.erdos_renyi_graph(100, 0.1)

# calculate the initial size of the giant component
initial_gc_size = len(max(nx.connected_components(G), key=len))

# define a list of edge failure probabilities
probabilities = [0.01, 0.015, 0.03, 0.04, 0.05]

# calculate the giant component size for each probability
gc_sizes = []
for p in probabilities:
    # create a copy of the original graph
    G_copy = G.copy()
    # randomly select edges to remove with probability p
    nodes_to_remove = np.random.choice(list(G_copy.nodes()), size=int(p*G_copy.number_of_nodes()), replace=False)
    G_copy.remove_nodes_from(nodes_to_remove)
    # calculate the size of the giant component
    gc_size = len(max(nx.connected_components(G_copy), key=len))
    gc_sizes.append(gc_size)

# create a boolean array indicating whether each element of gc_sizes is less than or equal to initial_gc_size
below_initial = [gc_size <= initial_gc_size for gc_size in gc_sizes]

# create a figure and axis
fig, ax = plt.subplots()

# plot the giant component size data
ax.plot(probabilities, gc_sizes, color='blue')

# fill the area between the curve and the initial giant component size
ax.fill_between(probabilities, gc_sizes, initial_gc_size, where=below_initial, interpolate=True, color='red', alpha=0.2)

# set axis labels and title
ax.set_xlabel('Probability of Edge Failure')
ax.set_ylabel('Giant Component Size')
ax.set_title('Network Resilience Changes')

# show the plot
plt.show()
