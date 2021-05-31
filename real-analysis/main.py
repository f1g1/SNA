import networkx as nx
import json
import matplotlib.pyplot as plt


def generate_graph_for_movies_linked_by_the_number_of_star_actors():
    with open("final-formatted.json", "rb") as f:
        jsonData = json.load(f)

    G = nx.Graph()
    nodes = []
    edges = []
    index=0
    for movie in jsonData:
        index+=1
        #if index>100:
        #    break
        nodePlusMetadata = (movie["Id"],
                            {
                                "Title": movie["Title"],
                                "Year": movie["Year"],
                                "Image": movie["Image"],
                                "Genre": movie["Genre"],
                                "Runtime": movie["Runtime"],
                                "Director": movie["Director"],
                                "Production": movie["Production"],
                                "Language": movie["Language"],
                                "Country": movie["Country"],
                                "Rated": movie["Rated"],
                                "Awards": movie["Awards"],
                                "imdbRating": movie["imdbRating"],
                                "Metascore": movie["Metascore"],
                                "imdbVotes": movie["imdbVotes"],
                                "BoxOffice": movie["BoxOffice"],
                                "Plot": movie["Plot"],
                                "Released": movie["Released"],
                                "Actors": movie["ActorsId"]
                            })
        nodes.append(nodePlusMetadata)

        for relatedMovie in movie["RelatedMoviesByNumberOfActors"]:
            edges.append((movie["Id"], relatedMovie["Item1"]))

    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    return G

def generate_graph_for_movies_linked_by_genre():
    with open("repr2-data.json", "rb") as f:
        jsonData = json.load(f)

    G = nx.Graph()
    nodes = []
    edges = []
    for movie in jsonData:
        nodePlusMetadata = (movie["Id"],
                            {
                                "Title": movie["Title"],
                                "Year": movie["Year"],
                                "Image": movie["Image"],
                                "Genre": movie["Genre"],
                                "Runtime": movie["Runtime"],
                                "Director": movie["Director"],
                                "Production": movie["Production"],
                                "Language": movie["Language"],
                                "Country": movie["Country"],
                                "Rated": movie["Rated"],
                                "Awards": movie["Awards"],
                                "imdbRating": movie["imdbRating"],
                                "Metascore": movie["Metascore"],
                                "imdbVotes": movie["imdbVotes"],
                                "BoxOffice": movie["BoxOffice"],
                                "Plot": movie["Plot"],
                                "Released": movie["Released"],
                                "Actors": movie["ActorsId"]
                            })
        nodes.append(nodePlusMetadata)

        for relatedMovie in movie["RelatedMovieByGenre"]:
            edges.append((movie["Id"], relatedMovie[0]))

    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    return G

def show_graph(G):
    fix, ax = plt.subplots(figsize=(5, 4))
    nx.draw_spring(G,
                   with_labels=False,
                   ax=ax,
                   node_size=10,
                   node_color="#1bb277",
                   edge_color="#aa88cc",
                   width=.20,
                   font_size=6.0,
                   font_color="#005566")
    ax.set_title("Visualization")
    plt.show()

def get_the_largest_connected_component(G):
    sorted_components = sorted(nx.connected_components(G), key=len, reverse=True)
    return G.subgraph(sorted_components[0])

def show_main_component_graph(G):
    largest_component = get_the_largest_connected_component(G)
    show_graph(largest_component)

def draw_heatmap_degree_distribution(G):
    degrees = G.degree()
    max_values = max([x[1] for x in degrees])
    val_map = {}
    for degree in degrees:
        val_map[degree[0]] = degree[1] / max_values
    values = [val_map.get(node, 0.25) for node in G.nodes()]
    fix, ax = plt.subplots(figsize=(12, 6))
    nx.draw_spring(G,
                   with_labels=False,
                    ax=ax,
                    node_size=20,
                    node_color=values,
                    edge_color="#000000",
                    width=.20)
    plt.show()

def draw_heatmap_betweenness_distribution(G):
    bc = nx.betweenness_centrality(G, normalized=True)
    max_values = max(bc.values())
    val_map = {}
    for entry in bc:
        val_map[entry] = bc.get(entry) / max_values
    values = [val_map.get(node, 0.25) for node in G.nodes()]
    fix, ax = plt.subplots(figsize=(12, 6))
    nx.draw_spring(G,
                with_labels=False,
                ax=ax,
                node_size=20,
                node_color=values,
                edge_color="#000000",
                width=.20)
    plt.show()

def draw_heatmap_eigenvector_distribution(G):
    ec = nx.eigenvector_centrality(G)
    max_values = max(ec.values())
    val_map = {}
    for entry in ec:
        val_map[entry] = ec.get(entry) / max_values
    values = [val_map.get(node, 0.25) for node in G.nodes()]
    fix, ax = plt.subplots(figsize=(12, 6))
    nx.draw_spring(G,
                       with_labels=False,
                       ax=ax,
                       node_size=20,
                       node_color=values,
                       edge_color="#000000",
                       width=.20)
    plt.show()

def draw_heatmap_closeness_distribution(G):
    cc = nx.closeness_centrality(G)
    max_values = max(cc.values())
    val_map = {}
    for entry in cc:
        val_map[entry] = cc.get(entry) / max_values
    values = [val_map.get(node, 0.25) for node in G.nodes()]
    fix, ax = plt.subplots(figsize=(12, 6))
    nx.draw_spring(G,
                       with_labels=False,
                       ax=ax,
                       node_size=20,
                       node_color=values,
                       edge_color="#000000",
                       width=.20)
    plt.show()

#G = generate_graph_for_movies_linked_by_the_number_of_star_actors()
#show_graph(G)
#show_main_component_graph(G)
#draw_heatmap_degree_distribution(G)
#draw_heatmap_betweenness_distribution(G)
#draw_heatmap_eigenvector_distribution(G)
#draw_heatmap_closeness_distribution(G)

G=generate_graph_for_movies_linked_by_genre()
show_graph(G)