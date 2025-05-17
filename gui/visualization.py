import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

class AutomatonVisualizer:
    """
    Handles visualization of automata using NetworkX and Matplotlib.
    """
    
    def __init__(self, frame, automaton):
        """
        Initialize the visualizer.
        
        Args:
            frame: Tkinter frame to place the visualization in
            automaton: The automaton to visualize
        """
        self.frame = frame
        self.automaton = automaton
        self.canvas = None
        self.figure = None
    
    def visualize(self):
        """
        Create and display a visualization of the automaton.
        """
        # Clear previous visualization
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Create a directed graph
        G = nx.DiGraph()
        
        # Add nodes (states)
        for state in self.automaton.states:
            G.add_node(state.name)
        
        # Add edges (transitions)
        edge_labels = {}
        for transition in self.automaton.transitions:
            source = transition.source_state.name
            target = transition.target_state.name
            symbol = transition.symbol
            
            # Create the edge if it doesn't exist
            if not G.has_edge(source, target):
                G.add_edge(source, target)
                edge_labels[(source, target)] = symbol
            else:
                # Append the symbol to existing edge label
                current_label = edge_labels[(source, target)]
                edge_labels[(source, target)] = f"{current_label},{symbol}"
        
        # Create figure and axis
        self.figure, ax = plt.subplots(figsize=(8, 6))
        
        # Calculate layout - use spring layout for natural spacing
        pos = nx.spring_layout(G, seed=42)
        
        # Draw nodes with different colors for initial and final states
        node_colors = []
        node_shapes = []
        node_edge_colors = []
        
        for state in self.automaton.states:
            if state.is_initial and state.is_final:
                node_colors.append('orange')  # Both initial and final
                node_edge_colors.append('none')
            elif state.is_initial:
                node_colors.append('lightblue')  # Initial state
                node_edge_colors.append('none')
            elif state.is_final:
                node_colors.append('lightgreen')  # Final state
                node_edge_colors.append('none')
            else:
                node_colors.append('white')  # Regular state
                node_edge_colors.append('black')
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                              node_size=700, ax=ax)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, arrowsize=20, ax=ax,min_source_margin=15,  min_target_margin=19)
        
        # Draw edge labels
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
        
        # Draw node labels
        nx.draw_networkx_labels(G, pos, font_size=12, ax=ax)

        
        
        # Draw markers for initial and final states
        for state in self.automaton.states:
            if state.is_initial:
                x, y = pos[state.name]
                offset = 0.35
                dx, dy = 0, 0.15
                head_width = 0.05
                head_length = 0.05
                
                ax.arrow(x, y - offset, dx, dy, head_width=head_width, head_length=head_length, fc='blue', ec='blue')
            
            if state.is_final:
                
                x, y = pos[state.name]
                radius = 0.15
                circle = plt.Circle((x, y), radius, fill=False, linestyle='solid')
                ax.add_patch(circle)
        
        # Remove axis
        ax.axis('off')
        ax.set_aspect('equal')
        
        # Add title
        plt.title(f"Automaton: {self.automaton.name}")
        
        # Create legend
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue', 
                  markersize=15, label='Initial State'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='lightgreen', 
                  markersize=15, label='Final State'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', 
                  markersize=15, label='Initial & Final State'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='white', 
                  markersize=15, label='Regular State')
        ]
        ax.legend(handles=legend_elements, loc='upper center', 
                 bbox_to_anchor=(0.5, 0), ncol=4)
        
        # Embed the figure in the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas.draw()
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Add toolbar
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar_frame = ttk.Frame(self.frame)
        toolbar_frame.pack(fill=tk.X)
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
    
    def save_figure(self, filename):
        """
        Save the current visualization to a file.
        
        Args:
            filename: Path to save the image
        """
        if self.figure:
            self.figure.savefig(filename, dpi=300, bbox_inches='tight')
            return True
        return False
    
    def update(self, automaton):
        """
        Update the visualization with a new automaton.
        
        Args:
            automaton: The new automaton to visualize
        """
        self.automaton = automaton
        self.visualize()