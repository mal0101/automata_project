import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AutomatonEditor:
    """
    Editor for creating and modifying automata with visualization.
    """
    
    def __init__(self, parent, automaton, main_window):
        """
        Initialize the automaton editor.
        
        Args:
            parent: Parent widget
            automaton: The automaton to edit
            main_window: Reference to main window for callbacks
        """
        self.parent = parent
        self.automaton = automaton
        self.main_window = main_window
        
        # Create main editor frame
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create title
        self.title_var = tk.StringVar(value=f"Editing: {automaton.name}")
        title_label = ttk.Label(self.frame, textvariable=self.title_var, font=("Arial", 14))
        title_label.pack(pady=(0, 10))
        
        # Create notebook with tabs
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_visualization_tab()
        self.create_states_tab()
        self.create_alphabet_tab()
        self.create_transitions_tab()
        
        # Initial visualization
        self.update_visualization()
    
    def update_title(self):
        """Update the editor title with the current automaton name."""
        self.title_var.set(f"Editing: {self.automaton.name}")
    
    def create_visualization_tab(self):
        """Create the tab for automaton visualization."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Visualization")
        
        # Create frame for the graph
        self.graph_frame = ttk.Frame(tab)
        self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add refresh button
        refresh_btn = ttk.Button(tab, text="Refresh", command=self.update_visualization)
        refresh_btn.pack(pady=(0, 10))
    
    def create_states_tab(self):
        """Create the tab for managing states."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="States")
        
        # Create a frame for the list and buttons
        list_frame = ttk.Frame(tab)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create state list with scrollbar
        ttk.Label(list_frame, text="States:").pack(anchor=tk.W)
        
        states_frame = ttk.Frame(list_frame)
        states_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        scrollbar = ttk.Scrollbar(states_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.states_list = tk.Listbox(states_frame, width=25, height=15)
        self.states_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.states_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.states_list.yview)
        
        # Populate list
        self.update_states_list()
        
        # Add buttons
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Add", command=self.add_state).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Edit", command=self.edit_state).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Delete", command=self.delete_state).pack(side=tk.LEFT)
        
        # Create a frame for state details
        details_frame = ttk.Frame(tab)
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(details_frame, text="State Properties:").pack(anchor=tk.W)
        
        # Frame for the form
        form_frame = ttk.Frame(details_frame)
        form_frame.pack(fill=tk.X, pady=10)
        
        # Name field
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.state_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.state_name_var).grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Initial checkbox
        self.state_initial_var = tk.BooleanVar()
        ttk.Checkbutton(form_frame, text="Initial State", variable=self.state_initial_var).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Final checkbox
        self.state_final_var = tk.BooleanVar()
        ttk.Checkbutton(form_frame, text="Final State", variable=self.state_final_var).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Save button
        ttk.Button(form_frame, text="Save", command=self.save_state).grid(row=3, column=0, columnspan=2, pady=10)

        note_frame = ttk.LabelFrame(details_frame, text="State Type Instructions")
        note_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(note_frame, text="• Check 'Initial State' for initial states\n"
                                "• Check 'Final State' for final states\n"
                                "• Leave both unchecked for regular states",
                justify=tk.LEFT, wraplength=300).pack(padx=10, pady=10)
        
        # Bind selection event
        self.states_list.bind("<<ListboxSelect>>", self.on_state_selected)
    
    def create_alphabet_tab(self):
        """Create the tab for managing the alphabet."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Alphabet")
        
        # Create a frame for the list and buttons
        list_frame = ttk.Frame(tab)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create symbol list with scrollbar
        ttk.Label(list_frame, text="Symbols:").pack(anchor=tk.W)
        
        symbols_frame = ttk.Frame(list_frame)
        symbols_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        scrollbar = ttk.Scrollbar(symbols_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.symbols_list = tk.Listbox(symbols_frame, width=25, height=15)
        self.symbols_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.symbols_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.symbols_list.yview)
        
        # Populate list
        self.update_symbols_list()
        
        # Add buttons
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Add", command=self.add_symbol).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Delete", command=self.delete_symbol).pack(side=tk.LEFT)
        
        # Create a frame for symbol details
        details_frame = ttk.Frame(tab)
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(details_frame, text="Add Symbol:").pack(anchor=tk.W)
        
        # Frame for the form
        form_frame = ttk.Frame(details_frame)
        form_frame.pack(fill=tk.X, pady=10)
        
        # Symbol field
        ttk.Label(form_frame, text="Symbol:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.symbol_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.symbol_var).grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Add button
        ttk.Button(form_frame, text="Add Symbol", command=self.add_symbol_from_form).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Notes
        note_frame = ttk.LabelFrame(details_frame, text="Notes")
        note_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(note_frame, text="• The epsilon symbol (ε) is automatically available for NFAs.\n"
                              "• Symbols should be single characters for best visualization.\n"
                              "• The alphabet is automatically updated when adding transitions.",
                 justify=tk.LEFT, wraplength=300).pack(padx=10, pady=10)
    
    def create_transitions_tab(self):
        """Create the tab for managing transitions."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Transitions")
        
        # Create a frame for the list and buttons
        list_frame = ttk.Frame(tab)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create transition list with scrollbar
        ttk.Label(list_frame, text="Transitions:").pack(anchor=tk.W)
        
        transitions_frame = ttk.Frame(list_frame)
        transitions_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        scrollbar = ttk.Scrollbar(transitions_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.transitions_list = tk.Listbox(transitions_frame, width=35, height=15)
        self.transitions_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.transitions_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.transitions_list.yview)
        
        # Populate list
        self.update_transitions_list()
        
        # Add buttons
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Add", command=self.add_transition).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Delete", command=self.delete_transition).pack(side=tk.LEFT)
        
        # Create a frame for transition details
        details_frame = ttk.Frame(tab)
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(details_frame, text="Add Transition:").pack(anchor=tk.W)
        
        # Frame for the form
        form_frame = ttk.Frame(details_frame)
        form_frame.pack(fill=tk.X, pady=10)
        
        # Source state dropdown
        ttk.Label(form_frame, text="From State:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.source_state_var = tk.StringVar()
        self.source_state_combo = ttk.Combobox(form_frame, textvariable=self.source_state_var)
        self.source_state_combo.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Symbol dropdown
        ttk.Label(form_frame, text="Symbol:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.transition_symbol_var = tk.StringVar()
        self.symbol_combo = ttk.Combobox(form_frame, textvariable=self.transition_symbol_var)
        self.symbol_combo.grid(row=1, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Target state dropdown
        ttk.Label(form_frame, text="To State:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.target_state_var = tk.StringVar()
        self.target_state_combo = ttk.Combobox(form_frame, textvariable=self.target_state_var)
        self.target_state_combo.grid(row=2, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Update comboboxes
        self.update_transition_comboboxes()
        
        # Add button
        ttk.Button(form_frame, text="Add Transition", command=self.add_transition_from_form).grid(row=3, column=0, columnspan=2, pady=10)
    
    def update_visualization(self):
        """Update the automaton visualization."""
        # Clear previous visualization
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        # Create a directed graph
        G = nx.DiGraph()
        
        # Add nodes (states)
        for state in self.automaton.states:
            G.add_node(state.name)
        
        # Add edges (transitions)
        for transition in self.automaton.transitions:
            source = transition.source_state.name
            target = transition.target_state.name
            symbol = transition.symbol
            
            # Add the edge with the symbol as a label
            # If there's already an edge, append the new symbol
            if G.has_edge(source, target):
                G[source][target]['label'] += f", {symbol}"
            else:
                G.add_edge(source, target, label=symbol)
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Calculate layout
        pos = nx.spring_layout(G, seed=42)
        
        # Draw nodes
        for state in self.automaton.states:
            name = state.name
            if state.is_initial and state.is_final:
                node_color = 'orange'  # Both initial and final
                node_shape = 'o'
                edge_color = 'none'
            elif state.is_initial:
                node_color = 'lightblue'  # Initial state
                node_shape = 'o'
                edge_color = 'none'
            elif state.is_final:
                node_color = 'lightgreen'  # Final state
                node_shape = 'o'
                edge_color = 'none'
            else:
                node_color = 'white'  # Regular state
                node_shape = 'o'
                edge_color = 'black'
            
            nx.draw_networkx_nodes(G, pos, nodelist=[name], node_color=node_color,edgecolors=edge_color, 
                                  node_shape=node_shape, node_size=700, ax=ax)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, arrowsize=20, ax=ax,min_source_margin=15,  min_target_margin=19)
        
        # Draw edge labels
        edge_labels = nx.get_edge_attributes(G, 'label')
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
                # Draw double circle for final states
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
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # State management methods
    
    def update_states_list(self):
        """Update the list of states."""
        self.states_list.delete(0, tk.END)
        
        for state in self.automaton.states:
            display = state.name
            if state.is_initial:
                display += " (initial)"
            if state.is_final:
                display += " (final)"
            
            self.states_list.insert(tk.END, display)
    
    def on_state_selected(self, event):
        """Handle state selection from the list."""
        selection = self.states_list.curselection()
        if not selection:
            return
        
        index = selection[0]
        if index < len(self.automaton.states):
            state = self.automaton.states[index]
            
            # Update form fields
            self.state_name_var.set(state.name)
            self.state_initial_var.set(state.is_initial)
            self.state_final_var.set(state.is_final)
    
    def add_state(self):
        """Add a new state."""
        self.state_name_var.set("")
        self.state_initial_var.set(False)
        self.state_final_var.set(False)
    
    def edit_state(self):
        """Edit the selected state."""
        selection = self.states_list.curselection()
        if not selection:
            messagebox.showinfo("Information", "Please select a state to edit.")
            return
        
        self.on_state_selected(None)  # Load the state into the form
    
    def save_state(self):
        """Save the current state from the form."""
        name = self.state_name_var.get().strip()
        is_initial = self.state_initial_var.get()
        is_final = self.state_final_var.get()
        
        if not name:
            messagebox.showerror("Error", "State name cannot be empty.")
            return
        
        # Check if state already exists
        existing_state = self.automaton.get_state_by_name(name)
        
        if existing_state:
            # Update existing state
            existing_state.is_initial = is_initial
            existing_state.is_final = is_final
            messagebox.showinfo("Success", f"State '{name}' updated.")
        else:
            # Create new state
            from models.state import State
            new_state = State(name, is_initial, is_final)
            self.automaton.add_state(new_state)
            messagebox.showinfo("Success", f"State '{name}' added.")
        
        # Update lists and visualization
        self.update_states_list()
        self.update_transition_comboboxes()
        self.update_visualization()
    
    def delete_state(self):
        """Delete the selected state."""
        selection = self.states_list.curselection()
        if not selection:
            messagebox.showinfo("Information", "Please select a state to delete.")
            return
        
        index = selection[0]
        if index < len(self.automaton.states):
            state = self.automaton.states[index]
            
            if messagebox.askyesno("Confirm Delete", 
                                 f"Are you sure you want to delete state '{state.name}'?\n"
                                 "This will also remove all transitions involving this state."):
                self.automaton.remove_state(state)
                
                # Update lists and visualization
                self.update_states_list()
                self.update_transitions_list()
                self.update_transition_comboboxes()
                self.update_visualization()
                
                messagebox.showinfo("Success", f"State '{state.name}' deleted.")
    
    # Alphabet management methods
    
    def update_symbols_list(self):
        """Update the list of alphabet symbols."""
        self.symbols_list.delete(0, tk.END)
        
        # Add symbols from the alphabet
        for symbol in sorted(self.automaton.alphabet.symbols):
            self.symbols_list.insert(tk.END, symbol)
    
    def add_symbol(self):
        """Add a new symbol (prepare form)."""
        self.symbol_var.set("")
    
    def add_symbol_from_form(self):
        """Add a symbol from the form."""
        symbol = self.symbol_var.get().strip()
        
        if not symbol:
            messagebox.showerror("Error", "Symbol cannot be empty.")
            return
        
        # Check if symbol is epsilon
        if symbol == self.automaton.alphabet.epsilon:
            messagebox.showinfo("Information", 
                              "The epsilon symbol is automatically available for NFAs.")
            return
        
        # Add symbol to alphabet
        self.automaton.alphabet.add_symbol(symbol)
        
        # Update lists
        self.update_symbols_list()
        self.update_transition_comboboxes()
        
        messagebox.showinfo("Success", f"Symbol '{symbol}' added to the alphabet.")
    
    def delete_symbol(self):
        """Delete the selected symbol."""
        selection = self.symbols_list.curselection()
        if not selection:
            messagebox.showinfo("Information", "Please select a symbol to delete.")
            return
        
        symbol = self.symbols_list.get(selection[0])
        
        # Check if symbol is used in transitions
        for transition in self.automaton.transitions:
            if transition.symbol == symbol:
                messagebox.showerror("Error", 
                                   f"Cannot delete symbol '{symbol}' because it is used in transitions.")
                return
        
        # Delete the symbol
        self.automaton.alphabet.remove_symbol(symbol)
        
        # Update lists
        self.update_symbols_list()
        self.update_transition_comboboxes()
        
        messagebox.showinfo("Success", f"Symbol '{symbol}' deleted from the alphabet.")
    
    # Transition management methods
    
    def update_transitions_list(self):
        """Update the list of transitions."""
        self.transitions_list.delete(0, tk.END)
        
        for transition in self.automaton.transitions:
            display = f"{transition.source_state.name} -- {transition.symbol} --> {transition.target_state.name}"
            self.transitions_list.insert(tk.END, display)
    
    def update_transition_comboboxes(self):
        """Update the comboboxes for transition form."""
        # Update state comboboxes
        state_names = [state.name for state in self.automaton.states]
        self.source_state_combo['values'] = state_names
        self.target_state_combo['values'] = state_names
        
        # Update symbol combobox
        symbols = list(self.automaton.alphabet.symbols)
        symbols.append(self.automaton.alphabet.epsilon)  # Add epsilon
        self.symbol_combo['values'] = sorted(symbols)
    
    def add_transition(self):
        """Add a new transition (prepare form)."""
        self.source_state_var.set("")
        self.transition_symbol_var.set("")
        self.target_state_var.set("")
    
    def add_transition_from_form(self):
        """Add a transition from the form."""
        source_name = self.source_state_var.get()
        symbol = self.transition_symbol_var.get()
        target_name = self.target_state_var.get()
        
        if not source_name or not symbol or not target_name:
            messagebox.showerror("Error", "All fields are required.")
            return
        
        # Get state objects
        source_state = self.automaton.get_state_by_name(source_name)
        target_state = self.automaton.get_state_by_name(target_name)
        
        if not source_state or not target_state:
            messagebox.showerror("Error", "Invalid state names.")
            return
        
        # Add transition
        if self.automaton.add_transition(source_state, symbol, target_state):
            self.update_transitions_list()
            self.update_visualization()
            messagebox.showinfo("Success", "Transition added.")
        else:
            messagebox.showinfo("Information", "This transition already exists.")
    
    def delete_transition(self):
        """Delete the selected transition."""
        selection = self.transitions_list.curselection()
        if not selection:
            messagebox.showinfo("Information", "Please select a transition to delete.")
            return
        
        index = selection[0]
        if index < len(self.automaton.transitions):
            transition = self.automaton.transitions[index]
            
            if messagebox.askyesno("Confirm Delete", 
                                 f"Are you sure you want to delete this transition?\n"
                                 f"{transition.source_state.name} -- {transition.symbol} --> {transition.target_state.name}"):
                self.automaton.remove_transition(transition)
                
                # Update lists and visualization
                self.update_transitions_list()
                self.update_visualization()
                
                messagebox.showinfo("Success", "Transition deleted.")
    
    def create_visualization_tab(self):
        """Create the tab for automaton visualization."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Visualization")
    
        # Create frame for the graph
        self.graph_frame = ttk.Frame(tab)
        self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
        # Create button frame
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
    
        # Add visualization control buttons
        ttk.Button(btn_frame, text="Refresh", 
              command=self.update_visualization).pack(side=tk.LEFT, padx=(0, 5))
    
        ttk.Button(btn_frame, text="Customize Appearance", 
              command=self.customize_appearance).pack(side=tk.LEFT, padx=(0, 5))
    
        ttk.Button(btn_frame, text="Simulate Word", 
              command=self.simulate_word).pack(side=tk.LEFT, padx=(0, 5))
    
        ttk.Button(btn_frame, text="Export Image", 
              command=self.export_visualization).pack(side=tk.LEFT)

    def update_visualization(self):
        """Update the automaton visualization."""
        # Clear previous visualization
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
    
        # Create and store the visualizer object
        from gui.visualization import AutomatonVisualizer
        self.visualizer = AutomatonVisualizer(self.graph_frame, self.automaton)
        self.visualizer.visualize()

    def customize_appearance(self):
        """Open the dialog to customize visualization appearance."""
        from gui.dialogs import StateStyleDialog
        dialog = StateStyleDialog(self.frame, self.automaton, self.visualizer)

    def simulate_word(self):
        """Open the dialog to simulate word processing."""
        from gui.dialogs import WordSimulationDialog
        dialog = WordSimulationDialog(self.frame, self.automaton, self.visualizer)

    def export_visualization(self):
        """Export the visualization as an image file."""
        if hasattr(self, 'visualizer'):
            self.visualizer.save_figure()