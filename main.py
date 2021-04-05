import networkx as nx

from Analyzer import Analyzer


def analyze_dataset(dataset):
    analyzer = Analyzer(G)

    analyzer.print_basic_description()
    print("average degree: ", analyzer.average_degree())
    print("diameter: ", analyzer.diameter())
    analyzer.print_components_analysis()
    print("shortest path: ", analyzer.shortest_path())
    print("average clustering coefficient of the network: ", analyzer.average_clustering_coefficient_of_the_network())
    print("average clustering coefficient of the largest connected component",
          analyzer.average_clustering_coefficient_of_the_largest_connected_component())

    analyzer.plot_degree_distribution()
    analyzer.plot_degree_distribution_in_loglog_scale()
    analyzer.plot_distribution_of_the_clustering_coefficient()
    analyzer.plot_distance_distribution()
    analyzer.plot_betweenness_centrality_distribution()
    analyzer.plot_connected_components_size_distribution()
    analyzer.plot_connected_components_size_distribution_bar()
    analyzer.draw()
    analyzer.draw_heatmap_degree_distribution()
    analyzer.draw_heatmap_betweenness_distribution()
    analyzer.draw_heatmap_eigenvector_distribution()
    analyzer.draw_heatmap_closeness_distribution()


G = nx.read_weighted_edgelist("usairport.tar")
analyze_dataset(G)
