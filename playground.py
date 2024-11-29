import tkinter as tk
from tkinter import ttk, messagebox
from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt

# Neo4j connection setup
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "your_secure_password"


class Neo4jVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Neo4j Visualizer")
        self.root.geometry("600x400")

        # GUI Layout
        self.query_label = tk.Label(root, text="Enter Cypher Query:")
        self.query_label.pack(pady=10)
        self.query_entry = tk.Entry(root, width=50)
        self.query_entry.pack(pady=5)

        self.query_button = tk.Button(
            root, text="Run Query", command=self.run_query)
        self.query_button.pack(pady=10)

        self.result_label = tk.Label(root, text="Query Result:")
        self.result_label.pack(pady=5)
        self.tree = ttk.Treeview(root, columns=(
            "Node", "Relationships"), show="headings")
        self.tree.heading("Node", text="Node")
        self.tree.heading("Relationships", text="Relationships")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)

        self.visualize_button = tk.Button(
            root, text="Visualize Graph", command=self.visualize_graph)
        self.visualize_button.pack(pady=10)

        # Initialize Neo4j connection
        self.driver = GraphDatabase.driver(
            NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        self.graph = nx.Graph()

    def run_query(self):
        query = self.query_entry.get()
        if not query:
            messagebox.showerror("Error", "Please enter a Cypher query.")
            return

        with self.driver.session() as session:
            try:
                result = session.run(query)
                self.graph.clear()
                self.display_result(result)
            except Exception as e:
                messagebox.showerror("Error", f"Query failed: {e}")

    def display_result(self, result):
        # Clear existing treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Populate treeview and build graph
        for record in result:
            node_data = []
            for key, value in record.items():
                self.graph.add_node(str(value))  # Add nodes to graph
                node_data.append(f"{key}: {value}")
            self.tree.insert("", tk.END, values=node_data)

    def visualize_graph(self):
        if self.graph.number_of_nodes() == 0:
            messagebox.showinfo("No Data", "No graph data to visualize.")
            return

        # Draw the graph using matplotlib
        pos = nx.spring_layout(self.graph)
        plt.figure(figsize=(8, 6))
        nx.draw(self.graph, pos, with_labels=True,
                node_color="lightblue", node_size=2000, font_size=10)
        plt.title("Neo4j Graph Visualization")
        plt.show()

    def close(self):
        self.driver.close()


# Run the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = Neo4jVisualizer(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
