import networkx as nx
import matplotlib.pyplot as plt


G = nx.DiGraph(
    [
        ("f", "a"),
        ("a", "b"),
        ("a", "e"),
        ("b", "c"),
        ("b", "d"),
        ("d", "e"),
        ("f", "c"),
        ("f", "g"),
        ("h", "f"),
    ]
)



# Compute the multipartite_layout using the "layer" node attribute
pos = nx.multipartite_layout(G, subset_key="layer")

fig, ax = plt.subplots()
nx.draw_networkx(G, pos=pos, ax=ax)
ax.set_title("DAG layout in topological order")
fig.tight_layout()
plt.show()