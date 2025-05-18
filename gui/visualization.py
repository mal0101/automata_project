import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from math import sqrt
import os
import numpy as np
    
class DraggableState:
    def __init__(self, fig, ax, pos, state_map, on_drag_complete=None):
        self.fig = fig
        self.ax = ax
        self.pos = pos
        self.state_map = state_map
        self.on_drag_complete = on_drag_complete
        self.selected_state = None
        self.offset_x = 0
        self.offset_y = 0
        
        self.cid_press = fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        
    def on_press(self, event):
        if event.inaxes != self.ax or event.button != 1:
            return
        
        closest_state = None
        min_dist = float('inf')
        for state_name, (x,y) in self.pos.items():
            dist = ((x - event.xdata)**2 + (y - event.ydata)**2)**0.5
            if dist < min_dist and dist < 0.1:
                min_dist = dist
                closest_state = state_name
        
        if closest_state:
            self.selected_state = closest_state
            self.offset_x = self.pos[closest_state][0] - event.xdata
            self.offset_y = self.pos[closest_state][1] - event.ydata
            
    def on_motion(self, event):
        if not self.selected_state or event.inaxes != self.ax:
            return
        
        self.pos[self.selected_state] = (event.xdata + self.offset_x, event.ydata + self.offset_y)
        self.ax.clear()
        self.redraw_graph()
        self.fig.canvas.draw_idle()
        
    def on_release(self, event):
        if self.selected_state and self.on_drag_complete:
            self.on_drag_complete()
        self.selected_state = None
        
    def redraw_graph(self):
        """Redraw the graph with updated node positions."""
        # Get reference to the visualizer (assuming it's stored in state_map)
        visualizer = self.state_map.get('__visualizer__', None)
    
        if visualizer:
            # Clear current axes but keep positions
            self.ax.clear()
        
            # Create a directed graph
            G = nx.DiGraph()
        
            # Add nodes (states)
            for state_name in self.pos:
                G.add_node(state_name)
        
            # Add edges (transitions)
            edge_labels = {}
            for transition in visualizer.automaton.transitions:
                source = transition.source_state.name
                target = transition.target_state.name
                symbol = transition.symbol
            
                if G.has_edge(source, target):
                    edge_labels[(source, target)] += ", " + symbol
                else:
                    G.add_edge(source, target)
                    edge_labels[(source, target)] = symbol
        
            # Draw the graph using helper
            VisualizationHelper.draw_graph(G, self.pos, self.ax, visualizer.automaton.states, edge_labels)
        
    def disconnect(self):
        """Disconnect all event callbacks to free resources."""
        if hasattr(self, 'cid_press') and self.cid_press:
            self.fig.canvas.mpl_disconnect(self.cid_press)
        if hasattr(self, 'cid_release') and self.cid_release:
            self.fig.canvas.mpl_disconnect(self.cid_release)
        if hasattr(self, 'cid_motion') and self.cid_motion:
            self.fig.canvas.mpl_disconnect(self.cid_motion)

class AutomatonVisualizer:
    def __init__(self, frame, automaton):
        self.frame = frame
        self.automaton = automaton
        self.canvas = None
        self.figure = None
        self.pos = None  # Will store node positions
        self.draggable = None
        self.state_map = {}  # Maps state names to node objects
        self.custom_colors = None  # Store custom colors
    
    def visualize(self, interactive=True):
        # Clear previous visualization
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Create a directed graph
        G = nx.DiGraph()
        
        # Add nodes (states)
        for state in self.automaton.states:
            G.add_node(state.name)
            self.state_map[state.name] = state
        
        # Add edges (transitions)
        edge_labels = {}
        for transition in self.automaton.transitions:
            source = transition.source_state.name
            target = transition.target_state.name
            symbol = transition.symbol
            
            if G.has_edge(source, target):
                edge_labels[(source, target)] += ", " + symbol
            else:
                G.add_edge(source, target)
                edge_labels[(source, target)] = symbol
        
        # Create figure and axis
        self.figure, ax = plt.subplots(figsize=(8, 6))
        
        # Calculate layout if not already defined
        if self.pos is None:
            self.pos = nx.spring_layout(G, seed=42)
        
        # Draw the graph using helper
        VisualizationHelper.draw_graph(G, self.pos, ax, self.automaton.states, edge_labels, custom_colors=self.custom_colors)
        
        # Add title and legend
        ax.set_title(f"Automaton: {self.automaton.name}")
        
        # Create legend
        from matplotlib.lines import Line2D
        colors = self.custom_colors or {
            "initial": "lightblue",
            "final": "lightgreen",
            "initial_final": "orange",
            "regular": "white"
        }
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor=colors["initial"], markersize=15, label='Initial State'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor=colors["final"], markersize=15, label='Final State'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor=colors["initial_final"], markersize=15, label='Initial & Final State'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor=colors["regular"], markersize=15, label='Regular State')
        ]
        ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 0), ncol=4)
        
        # Embed the figure in the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas.draw()
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Add toolbar
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar_frame = tk.Frame(self.frame)
        toolbar_frame.pack(fill=tk.X)
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        
        # Enable interactive features if requested
        if interactive:
            # Make states draggable
            self.draggable = DraggableState(self.figure, ax, self.pos, self.state_map, 
                                           on_drag_complete=self.on_drag_complete)
            self.draggable.redraw_graph = self.redraw_graph
    
    def redraw_graph(self):
        # Call visualization without recreating the positions
        self.visualize(interactive=False)
    
    def on_drag_complete(self):
        """Called when dragging a state is complete."""
        # Save the current positions (can be extended to save to a file or configuration)
        if hasattr(self, 'pos') and self.pos:
            # Store positions for future reference
            self.saved_positions = self.pos.copy()
        
            # You could save the positions to a file if needed
            self.save_layout_to_file()
    
    def save_figure(self, filename):
        """
        Save the current visualization to a file.
    
        Args:
            filename: Path to save the image. If None, a file dialog will be shown.
    
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.figure:
            return False
            
        from tkinter import filedialog
        filetypes = [
            ('PNG Image', '*.png'),
            ('JPEG Image', '*.jpg'),
            ('SVG Image', '*.svg'),
            ('PDF Document', '*.pdf')
        ]
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=filetypes,
            initialfile=filename,
            title="Save Visualization As"
        )
    
        if not filename:  # User cancelled
            return False

        try:
            # Get the extension to determine format
            ext = os.path.splitext(filename)[1].lower()
    
            # If svg, need to use specific backend
            if ext == '.svg':
                from matplotlib.backends.backend_svg import FigureCanvasSVG
                canvas = FigureCanvasSVG(self.figure)
                canvas.print_figure(filename)
            else:
                self.figure.savefig(filename, dpi=300, bbox_inches='tight')
    
            return True
        except Exception as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Failed to save image: {str(e)}")
            return False

class AutomatonSimulator:
    def __init__(self, visualizer, automaton):
        self.visualizer = visualizer
        self.automaton = automaton
        self.figure = visualizer.figure
        self.ax = visualizer.figure.axes[0]
        self.pos = visualizer.pos
        self.current_states = []
        self.word = ""
        self.current_position = 0
        self.animation_speed = 1.0  # seconds per step
        self.highlight_nodes = []
        self.highlight_edges = []
        self.timer = None
    
    def simulate_word(self, word, speed=1.0):
        """Start simulating word processing."""
        from algorithms.deterministic import DeterministicOperations
        from algorithms.conversion import ConversionOperations
        
        self.word = word
        self.current_position = 0
        self.animation_speed = speed
        
        # Determine if the automaton is deterministic
        is_deterministic = DeterministicOperations.is_deterministic(self.automaton)
        
        # Get starting states
        if is_deterministic:
            self.current_states = self.automaton.initial_states.copy()
        else:
            # For NFA, start with epsilon closure of initial states
            self.current_states = list(ConversionOperations.epsilon_closure(
                self.automaton, self.automaton.initial_states))
        
        # Begin animation
        self.highlight_current_states()
        self.step_simulation()
    
    def step_simulation(self):
        """Process one step of the simulation."""
        if self.current_position >= len(self.word):
            # End of word reached - highlight final states if in accept state
            self.highlight_final_state()
            return
        
        # Get current symbol
        symbol = self.word[self.current_position]
        
        # Get next states
        next_states = []
        highlight_edges = []
        
        for state in self.current_states:
            transitions = self.automaton.get_transitions_from(state, symbol)
            for transition in transitions:
                next_states.append(transition.target_state)
                highlight_edges.append((transition.source_state.name, transition.target_state.name))
        
        # For NFA, add epsilon transitions
        from algorithms.conversion import ConversionOperations
        epsilon_closure_states = []
        for state in next_states:
            epsilon_closure_states.extend(ConversionOperations.epsilon_closure(
                self.automaton, [state]))
        next_states = list(set(epsilon_closure_states))
        
        # Update current states
        self.current_states = next_states
        self.current_position += 1
        
        # Highlight the new states and edges
        self.highlight_edges = highlight_edges
        self.highlight_current_states()
        
        # Schedule next step if there are more symbols or we need to show final state
        if self.current_position <= len(self.word):
            self.timer = self.figure.canvas.new_timer(
                interval=int(self.animation_speed * 1000))
            self.timer.add_callback(self.step_simulation)
            self.timer.start()
    
    def highlight_current_states(self):
        """Highlight the current states during simulation."""
        # Clear previous highlights
        self.ax.clear()
        
        # Redraw the graph
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
            
            if G.has_edge(source, target):
                edge_labels[(source, target)] += ", " + symbol
            else:
                G.add_edge(source, target)
                edge_labels[(source, target)] = symbol
        
        # Draw the graph using helper with highlights
        VisualizationHelper.draw_graph(G, self.pos, self.ax, self.automaton.states, 
                                     edge_labels, self.current_states, self.highlight_edges)
        
        # Add simulation status text
        processed = self.word[:self.current_position]
        remaining = self.word[self.current_position:]
        status_text = f"Processing: {processed}|{remaining}"
        self.ax.text(0.5, -0.1, status_text, transform=self.ax.transAxes,
                    ha='center', fontsize=12)
        
        # Update ax title
        self.ax.set_title(f"Simulating: {self.word}")
        
        # Redraw the figure
        self.figure.canvas.draw_idle()
    
    def highlight_final_state(self):
        """Highlight the final state of simulation and show acceptance status."""
        # Check if any current state is final (accepting)
        is_accepted = any(state.is_final for state in self.current_states)
        
        # Update the text to show acceptance status
        status_text = f"Word '{self.word}' is "
        status_text += "ACCEPTED" if is_accepted else "REJECTED"
        
        # Add or update the status text
        for text in self.ax.texts:
            if text.get_position()[1] == -0.1:  # Position of our status text
                text.set_text(status_text)
                break
        else:
            self.ax.text(0.5, -0.1, status_text, transform=self.ax.transAxes,
                        ha='center', fontsize=12, 
                        color='green' if is_accepted else 'red',
                        fontweight='bold')
        
        # Redraw the figure
        self.figure.canvas.draw_idle()

class VisualizationHelper:
    """Helper class for visualization-related operations."""
    
    @staticmethod
    def get_node_colors(states, custom_colors=None):
        """Get colors for nodes based on their type.
        
        Args:
            states: List of states to color
            custom_colors: Dictionary of custom colors for different state types
        """
        node_colors = []
        node_edge_colors = []
        
        # Default colors
        colors = {
            "regular": "white",
            "initial": "lightblue",
            "final": "lightgreen",
            "initial_final": "orange"
        }
        
        # Override with custom colors if provided
        if custom_colors:
            colors.update(custom_colors)
        
        for state in states:
            if state.is_initial and state.is_final:
                node_colors.append(colors["initial_final"])
                node_edge_colors.append('none')
            elif state.is_initial:
                node_colors.append(colors["initial"])
                node_edge_colors.append('none')
            elif state.is_final:
                node_colors.append(colors["final"])
                node_edge_colors.append('none')
            else:
                node_colors.append(colors["regular"])
                node_edge_colors.append('black')
                
        return node_colors, node_edge_colors

    @staticmethod
    def draw_graph(G, pos, ax, states, edge_labels=None, highlight_states=None, highlight_edges=None, custom_colors=None):
        """Draw the graph with labels following edge curvature correctly."""
        # Get node colors
        node_colors, node_edge_colors = VisualizationHelper.get_node_colors(states, custom_colors)
        
        # Adjust colors for highlighted states
        if highlight_states:
            for i, state in enumerate(states):
                if state in highlight_states:
                    node_colors[i] = 'red'
                    node_edge_colors[i] = 'red'
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                             node_size=700, edgecolors=node_edge_colors, ax=ax)
        
        # Custom label positioning to follow curve correctly
        def curved_edge_label_pos(u, v, rad=0.4):
            """Calculate label position for curved edges with correct orientation."""
            x1, y1 = pos[u]
            x2, y2 = pos[v]
            
            # Midpoint
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            
            # Calculate perpendicular offset based on curvature
            dx, dy = x2 - x1, y2 - y1
            perp_dx = -dy
            perp_dy = dx
            
            # Normalize perpendicular vector
            magnitude = np.sqrt(perp_dx**2 + perp_dy**2)
            
            # Adjust sign to ensure correct side of curve
            # Use cross product to determine curve direction
            cross_product = dx * perp_dy - dy * perp_dx
            sign = -1 if cross_product > 0 else 1
            
            perp_dx *= sign * rad / magnitude
            perp_dy *= sign * rad / magnitude
            
            # Offset label along the perpendicular
            label_x = mid_x + perp_dx
            label_y = mid_y + perp_dy
            
            return label_x, label_y
        
        # Handle edge drawing
        for edge in G.edges():
            # Normal edges with slight curve
            nx.draw_networkx_edges(
                G, pos, 
                edgelist=[edge], 
                connectionstyle='arc3,rad=0.4',  # Slight curve
                arrowsize=20, 
                min_source_margin=15, 
                min_target_margin=15,
                ax=ax
            )
        
        # Highlight specific edges if requested
        if highlight_edges:
            highlight_edge_list = [edge for edge in G.edges() if edge in highlight_edges]
            nx.draw_networkx_edges(
                G, pos, 
                edgelist=highlight_edge_list, 
                edge_color='red', 
                width=2.0, 
                connectionstyle='arc3,rad=0.4',
                arrowsize=20, 
                ax=ax
            )
        
        # Custom edge label positioning
        if edge_labels:
            for (u, v) in G.edges():
                if (u, v) in edge_labels:
                    label_x, label_y = curved_edge_label_pos(u, v)
                    ax.text(label_x, label_y, edge_labels[(u, v)], 
                            fontsize=10, 
                            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7),
                            horizontalalignment='center',
                            verticalalignment='center')
        
        # Draw node labels
        nx.draw_networkx_labels(G, pos, font_size=12, ax=ax)
        
        # Draw markers for initial and final states
        for state in states:
            if state.is_initial:
                x, y = pos[state.name]
                offset = 0.35
                dx, dy = 0, 0.15
                head_width = 0.05
                head_length = 0.05
                
                ax.arrow(x, y - offset, dx, dy, head_width=head_width, head_length=head_length, fc='blue', ec='blue')
            
            if state.is_final:
                x, y = pos[state.name]
                radius = 0.125
                circle = plt.Circle((x, y), radius, fill=False, linestyle='solid')
                ax.add_patch(circle)
        
        ax.set_aspect('equal')
        ax.axis('off')
