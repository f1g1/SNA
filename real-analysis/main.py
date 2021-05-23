import networkx as nx
import json
import matplotlib.pyplot as plt


def generate_graph():
    with open("final-formatted.json", "rb") as f:
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

        for relatedMovie in movie["RelatedMoviesByNumberOfActors"]:
            edges.append((movie["Id"], relatedMovie["Item1"]))

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


G = generate_graph()
show_graph(G)
