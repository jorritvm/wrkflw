"""create workflows and workflow collections

based on https://medium.com/hurb-engineering/building-a-task-orchestrator-with-python-and-graph-algorithms-a-fun-and-practical-guide-c1cd4c9f3d40
"""

from collections import defaultdict, deque
from typing import List
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from.tasks import Status


class Workflow:
    """A workflow uses a directed graph data structure using adjacency lists.

    Attributes:
        graph: (dict) A dictionary that maps each node to a list of its adjacent nodes.
        in_degree: (dict) A dictionary that maps each node to its in-degree.
    """

    def __init__(self) -> None:
        """
        Initializes a new empty graph.
        """
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)

    def add_edge(self, u: int, v: int) -> None:
        """Adds a directed edge from node u to node v.

        Args:
            u: (int) The starting node of the edge.
            v: (int) The ending node of the edge.
        """
        if u in self.graph and v in self.graph[u]:
            return  # Edge already exists

        # Temporarily add the edge to detect cycles
        self.graph[u].append(v)
        cycle_exists = self.detect_cycle()
        if cycle_exists:
            # If a cycle is created, remove the edge and return False
            self.graph[u].remove(v)
            return False

        # If no cycle is created, add the edge and update in-degree
        self.graph[u].append(v)
        self.in_degree[v] += 1
        return True

    def detect_cycle(self) -> bool:
        """Detects cycles in the graph using a depth-first search algorithm.

        Returns:
            (bool) True if a cycle exists, False otherwise.
        """
        visited = set()

        def dfs(node, stack=None):
            stack = set() if stack is None else stack

            visited.add(node)
            stack.add(node)

            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor, stack):
                        return True
                elif neighbor in stack:
                    return True

            stack.remove(node)
            return False

        for node in list(self.graph):
            if node not in visited:
                if dfs(node):
                    return True

        return False

    def topological_sort(self) -> List[int]:
        """Performs a topological sort of the graph using Khan's algorithm.

        Returns:
            (List[int]) A list of nodes in topological order.
        """
        result = []
        q = deque()
        in_degree_copy = self.in_degree.copy()

        # Add all nodes with in-degree 0 to the queue
        for node in self.graph.keys():
            if in_degree_copy[node] == 0:
                q.append(node)

        while q:
            # Remove a node from the queue and add it to the result
            node = q.popleft()
            result.append(node)

            # Decrement the in-degree of all adjacent nodes
            for neighbor in self.graph[node]:
                in_degree_copy[neighbor] -= 1

                # Add the neighbor to the queue if its in-degree is 0
                if in_degree_copy[neighbor] == 0:
                    q.append(neighbor)

        # Check if there was a cycle in the graph
        if len(result) != len(self.graph):
            raise ValueError("Graph contains a cycle")

        return result

    def status_table(self):
        data = []
        for obj in self.graph.keys():
            name = obj.name
            status = obj.status.value
            data.append((name, status))

        df = pd.DataFrame(data, columns=["Name", "Status"])
        return df

    def status_viz(self):
        # Create a directed graph using NetworkX
        G = nx.DiGraph()

        # Add nodes and edges from the adjacency list
        for i, source in enumerate(self.topological_sort()):
            G.add_node(source.name, status=source.status, layer=i)
            for target in self.graph[source]:
                G.add_edge(source.name, target.name)

        # Create a layout for our nodes specific to a DAG
        # Compute the multipartite_layout using the "layer" node attribute --> issue: https://stackoverflow.com/questions/75855498/graph-edge-overlay-when-visualizing-a-networkx-dag-using-multipartite-layout
        # layout = nx.multipartite_layout(G, subset_key="layer")
        layout = nx.spring_layout(G, seed=42)

        # Extract unique statuses
        unique_statuses = set()
        for node_data in G.nodes(data=True):
            unique_statuses.add(node_data[1]['status'])

        # Create a color map based on unique statuses
        color_map = {
            Status.INIT: 'blue',
            Status.WAITING: 'orange',
            Status.RUNNING: 'yellow',
            Status.FINISHED: 'GREEN',
            Status.FAILED: 'red'
        }

        # Generate node colors based on statuses
        node_colors = [color_map[G.nodes[node]['status']] for node in G.nodes()]

        # Draw the graph
        nx.draw(G, pos=layout, with_labels=True, node_size=1000, font_size=6, font_color='black', font_weight='normal', node_color=node_colors, node_shape="s")
        nx.draw_networkx

        # Create a legend
        legend_labels = {status.value: color for status, color in color_map.items()}
        legend = plt.legend(
            handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, label=status) for status, color
                     in legend_labels.items()], title='Status Legend')

        # Show the plot
        plt.show()
