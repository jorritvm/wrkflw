"""create workflows and workflow collections
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from .tasks import Status, Task


class Workflow:
    """A workflow uses a directed graph data structure using adjacency lists.

    Attributes:
        graph: (dict) A dictionary that maps each node to a list of its adjacent nodes.
        in_degree: (dict) A dictionary that maps each node to its in-degree.
    """

    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    def add_task(self, task: Task):
        """Adds a new task to the graph

        Args:
            task: (task) task to add
        """
        self.graph.add_node(task)

    def add_relation(self, task1: Task, task2: Task) -> None:
        """Adds a directed edge from task1 to task2.
        Will add task1 or task2 if they don't exist yet.

        Args:
            task1: (task) the predecessor task
            task2: (task) the successor task
        """
        self.graph.add_edge(task1, task2)
        still_a_dag = False
        if nx.is_directed_acyclic_graph(self.graph):
            still_a_dag = True
        else:
            # If a cycle is created, remove the edge and return False
            self.graph.remove_edge(task1, task2)
        return still_a_dag

        if task1 in self.graph and task2 in self.graph[task1]:
            return  # Edge already exists

    def status_table(self):
        data = []
        for obj in self.graph.nodes():
            name = obj.name
            status = obj.status.label
            data.append((name, status))

        df = pd.DataFrame(data, columns=["Name", "Status"])
        return df

    def status_viz(self):
        # Create a layout for our nodes specific to a DAG
        # Compute the multipartite_layout using the "layer" node attribute
        for layer, nodes in enumerate(nx.topological_generations(self.graph)):
            # `multipartite_layout` expects the layer as a node attribute, so add the
            # numeric layer value as a node attribute
            for node in nodes:
                self.graph.nodes[node]["layer"] = layer
        layout = nx.multipartite_layout(self.graph, subset_key="layer")

        # get labels and colors per node
        node_colors = [task.status.color for task in self.graph.nodes()]
        node_labels = {task: task.name for task in self.graph.nodes()}

        # Draw the graph
        nx.draw(self.graph, pos=layout,
                with_labels=True, labels=node_labels,
                node_size=1000, font_size=6, font_color='black', font_weight='normal',
                node_color=node_colors, node_shape="s")

        # Create a legend
        plt.legend(
            handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=status.color, label=status.label) for
                     status in Status], title='Status Legend')

        # Show the plot
        plt.show()

    def run(self):
        failed_tasks = []

        for task in nx.topological_sort(self.graph):
            if task.status == Status.WAITING:
                # first check if this task does not have failed predecessors
                is_reachable = False
                for failed_task in failed_tasks:
                    is_reachable = is_reachable or nx.has_path(self.graph.reverse(), task, failed_task)
                if not is_reachable:
                    self.status_viz() # debug
                    task.run()
                    self.status_viz()  # debug
            if task.status == Status.FAILED:
                failed_tasks.append(task)

