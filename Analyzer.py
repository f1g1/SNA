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

        if not is_network_connected:
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

    def plot_degree_distribution_in_loglog_scale(self):
        degrees = sorted([d for n, d in self.dataset.degree()], reverse=True)
        kmin = np.min(degrees)
        kmax = np.max(degrees)

        bin_edges = np.logspace(np.log10(kmin), np.log10(kmax), num=50)
        density, _ = np.histogram(degrees, bins=bin_edges, density=True)
        log_be = np.log10(bin_edges)
        x = 10 ** ((log_be[1:] + log_be[:-1]) / 2)

        fig = plt.figure(figsize=(6, 4))
        plt.loglog(x, density, marker='o', linestyle='none', color='#c7502c')
        plt.xlabel(r"degree $k$", fontsize=16)
        plt.ylabel(r"$P(k)$", fontsize=16)
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

    def distance_distribution(self):
        largest_connected_component = self.get_the_largest_connected_component()

        N = len(self.dataset)
        NO = len(largest_connected_component)
        D = np.zeros(shape=(N, N))
        vl = []
        for node1 in largest_connected_component.nodes():
            for node2 in largest_connected_component.nodes():
                if (node1 != node2) and D[int(node1) - 1][int(node2) - 1] == 0:
                    aux = nx.shortest_path(largest_connected_component, node1, node2)
                    dij = len(aux)
                    D[int(node1) - 1][int(node2) - 1] = dij
                    D[int(node2) - 1][int(node1) - 1] = dij
                    vl.append(dij)

        d = {}
        for elem in vl:
            if elem in d:
                d[elem] += 1
            else:
                d[elem] = 1

        distances = sorted(d.keys())
        pdistances = [d[i] / NO for i in distances]
        return distances, pdistances

    def plot_distance_distribution(self):
        distances, pdistances = self.distance_distribution()

        plt.figure(figsize=(6, 6))
        plt.plot(distances, pdistances, linestyle="solid", linewidth=2, color="black")
        plt.plot(distances, pdistances, "o", color='#c7502c', markersize=12)
        plt.xlabel(r"$d$", fontsize=16)
        plt.ylabel(r"$p_d$", fontsize=16)
        plt.title("Distance distribution")
        plt.grid(True)
        plt.show()

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

    def plot_closeness_centrality_distribution(self):
        cc = nx.closeness_centrality(self.dataset)
        cc = np.asarray(list(cc.values()))
        num_nodes = len(self.dataset.nodes())
        nodes_axis = range(1, num_nodes+1)
        plt.plot(nodes_axis, cc)
        plt.title(" CC", fontsize=18)
        plt.xlabel('Node Indices', fontsize=16)
        plt.ylabel('Closeness centrality', fontsize=16)
        plt.show()

    def plot_eigenvector_centrality_distribution(self):
        ec = nx.eigenvector_centrality(self.dataset)
        ec = np.asarray(list(ec.values()))
        num_nodes = len(self.dataset.nodes())
        nodes_axis = range(1, num_nodes + 1)
        plt.plot(nodes_axis, ec)
        plt.title(" Eigenvector centrality distribution", fontsize=18)
        plt.xlabel('Node Indices', fontsize=16)
        plt.ylabel('Eigenvector centrality', fontsize=16)
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

    def plot_connected_components_size_distribution_bar(self):
        bc = list(nx.connected_components(self.dataset))
        connected_components_no = [len(i) for i in bc]
        components_index = [1, 2]
        plt.bar(components_index, connected_components_no, log=True)
        plt.title(" Size", fontsize=18)
        plt.xlabel('Components', fontsize=16)
        plt.ylabel('CC', fontsize=16)
        plt.xticks(components_index)
        plt.show()

    def draw(self):
        fix, ax = plt.subplots(figsize=(5, 4))
        nx.draw_spring(self.dataset,
                       with_labels=False,
                       ax=ax,
                       node_size=10,
                       node_color="#1bb277",
                       edge_color="#aa88cc",
                       width=.20,
                       font_size=3.0,
                       font_color="#005566")
        ax.set_title("US Airports spring")
        plt.show()

    def draw_heatmap_degree_distribution(self):
        degrees = self.dataset.degree()
        max_values = max([x[1] for x in degrees])
        val_map = {}
        for degree in degrees:
            val_map[degree[0]] = degree[1] / max_values
        values = [val_map.get(node, 0.25) for node in self.dataset.nodes()]
        fix, ax = plt.subplots(figsize=(12, 6))
        nx.draw_spring(self.dataset,
                       with_labels=False,
                       ax=ax,
                       node_size=20,
                       node_color=values,
                       edge_color="#000000",
                       width=.20)
        plt.show()

    def draw_heatmap_betweenness_distribution(self):
        bc = nx.betweenness_centrality(self.dataset, normalized=True)
        max_values = max(bc.values())
        val_map = {}
        for entry in bc:
            val_map[entry] = bc.get(entry) / max_values
        values = [val_map.get(node, 0.25) for node in self.dataset.nodes()]
        fix, ax = plt.subplots(figsize=(12, 6))
        nx.draw_spring(self.dataset,
                       with_labels=False,
                       ax=ax,
                       node_size=20,
                       node_color=values,
                       edge_color="#000000",
                       width=.20)
        plt.show()

    def draw_heatmap_eigenvector_distribution(self):
        ec = nx.eigenvector_centrality(self.dataset)
        max_values = max(ec.values())
        val_map = {}
        for entry in ec:
            val_map[entry] = ec.get(entry) / max_values
        values = [val_map.get(node, 0.25) for node in self.dataset.nodes()]
        fix, ax = plt.subplots(figsize=(12, 6))
        nx.draw_spring(self.dataset,
                       with_labels=False,
                       ax=ax,
                       node_size=20,
                       node_color=values,
                       edge_color="#000000",
                       width=.20)
        plt.show()

    def draw_heatmap_closeness_distribution(self):
        cc = nx.closeness_centrality(self.dataset)
        max_values = max(cc.values())
        val_map = {}
        for entry in cc:
            val_map[entry] = cc.get(entry) / max_values
        values = [val_map.get(node, 0.25) for node in self.dataset.nodes()]
        fix, ax = plt.subplots(figsize=(12, 6))
        nx.draw_spring(self.dataset,
                       with_labels=False,
                       ax=ax,
                       node_size=20,
                       node_color=values,
                       edge_color="#000000",
                       width=.20)
        plt.show()
