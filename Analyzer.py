import networkx as nx
import numpy as np
import collections
import matplotlib.pyplot as plt


class Analyzer:
    def __init__(self, dataset):
        self.dataset = dataset

    def print_basic_description(self):
        print("---Description---")
        print("This is the directed network of flights between US airports in 2010. Each edge represents a connection "
              "from one airport to another, and the weight of an edge shows the number of flights on that connection "
              "in the given direction, in 2010. ")
        print("nodes: ", len(self.dataset.nodes()))
        print("links: ", self.dataset.size())

        degrees = [self.dataset.degree(n) for n in self.dataset.nodes()]
        print("min degree: ", np.min(degrees))
        print("max degree: ", np.max(degrees))
        print("average degree: ", self.average_degree())

    def average_degree(self):
        degrees = [self.dataset.degree(n) for n in self.dataset.nodes()]
        return np.mean(degrees)

    def print_components_analysis(self):
        print("--components analysis--")

        is_network_connected = nx.is_connected(self.dataset)
        print("Is network connected: ", is_network_connected)

        if is_network_connected:
            largest_connected_component = self.get_the_largest_connected_component()
            print("Connected components number: ", nx.number_connected_components(self.dataset))
            print("The largest connected component nodes number: ", len(largest_connected_component))

    def get_the_largest_connected_component(self):
        sorted_components = sorted(nx.connected_components(self.dataset), key=len, reverse=True)
        return self.dataset.subgraph(sorted_components[0])

    def print_largest_connected_component_info(self):
        largest_connected_component = self.get_the_largest_connected_component()
        print(nx.info(largest_connected_component))

    def compute_degree_distribution(self):
        degrees = sorted([d for n, d in self.dataset.degree()], reverse=True)
        degree_count = collections.Counter(degrees)
        degress_list, count = zip(*degree_count.items())
        return degress_list, count

    def plot_degree_distribution(self):
        degress_list, count = self.compute_degree_distribution()
        plt.bar(degress_list, count, width=0.80, color="b")
        plt.title("Degree Histogram")
        plt.ylabel("Count")
        plt.xlabel("Degree")
        plt.show()

    def diameter(self):
        if nx.is_connected(self.dataset):
            return nx.diameter(self.dataset)
        else:
            largest_connected_component = self.get_the_largest_connected_component()
            return nx.diameter(largest_connected_component)

    def shortest_path(self):
        if nx.is_connected(self.dataset):
            return nx.average_shortest_path_length(self.dataset)
        else:
            largest_connected_component = self.get_the_largest_connected_component()
            return nx.average_shortest_path_length(largest_connected_component)

    def density(self):
        return nx.density(self.dataset)

    def density_of_the_largest_component(self):
        largest_connected_component = self.get_the_largest_connected_component()
        return nx.density(largest_connected_component)

    def average_clustering_coefficient_of_the_network(self):
        return nx.average_clustering(self.dataset)

    def average_clustering_coefficient_of_the_largest_connected_component(self):
        largest_connected_component = self.get_the_largest_connected_component()
        return nx.average_clustering(largest_connected_component)

    def plot_distribution_of_the_clustering_coefficient(self):
        clustering_coefficient = nx.clustering(self.dataset)

        plt.hist(clustering_coefficient.values(), bins=10, density=True)
        plt.grid(True)
        plt.title("Distribution of the clustering coefficient")
        plt.xlabel("Clustering coefficient")
        plt.ylabel("P")
        plt.show()

    def plot_betweenness_centrality_distribution(self):
        bc = nx.betweenness_centrality(self.dataset, normalized=False)
        bc = np.asarray(list(bc.values()))

        num_nodes = len(self.dataset.nodes())
        nodes_axis = range(1, num_nodes + 1)

        plt.plot(nodes_axis, bc)
        plt.title(" BC", fontsize=18)
        plt.xlabel('Node Indices', fontsize=16)
        plt.ylabel('BC', fontsize=16)
        plt.show()

    def plot_connected_components_size_distribution(self):
        bc = list(nx.connected_components(self.dataset))

        connected_components_no = [len(i) for i in bc]
        nodes_axis = range(1, len(bc) + 1)

        plt.plot(nodes_axis, connected_components_no)
        plt.title(" CC", fontsize=18)
        plt.xlabel('Components Indices', fontsize=16)
        plt.ylabel('CC', fontsize=16)
        plt.show()
