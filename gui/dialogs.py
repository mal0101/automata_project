import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class TextInputDialog:
    """
    Dialog for getting text input from the user.
    """
    
    def __init__(self, parent, title, prompt, default=""):
        """
        Initialize the dialog.
        
        Args:
            parent: Parent window
            title: Dialog title
            prompt: Text prompt to display
            default: Default text value
        """
        self.result = None
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center on parent
        window_width = 300
        window_height = 150
        
        # Calculate position
        position_right = parent.winfo_x() + (parent.winfo_width() // 2) - (window_width // 2)
        position_down = parent.winfo_y() + (parent.winfo_height() // 2) - (window_height // 2)
        
        # Set window size and position
        self.dialog.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
        
        # Add prompt
        ttk.Label(self.dialog, text=prompt).pack(pady=(20, 10))
        
        # Add text entry
        self.entry_var = tk.StringVar(value=default)
        entry = ttk.Entry(self.dialog, textvariable=self.entry_var, width=30)
        entry.pack(pady=(0, 20))
        entry.focus_set()
        
        # Add buttons
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(pady=(0, 20))
        
        ttk.Button(button_frame, text="OK", command=self.on_ok).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=self.on_cancel).pack(side=tk.LEFT)
        
        # Handle Enter key
        self.dialog.bind("<Return>", lambda event: self.on_ok())
        self.dialog.bind("<Escape>", lambda event: self.on_cancel())
        
        # Wait for dialog to close
        parent.wait_window(self.dialog)
    
    def on_ok(self):
        """Handle OK button click."""
        self.result = self.entry_var.get().strip()
        self.dialog.destroy()
    
    def on_cancel(self):
        """Handle Cancel button click."""
        self.dialog.destroy()

class NameInputDialog(TextInputDialog):
    """Dialog specifically for getting names, with validation."""
    
    def on_ok(self):
        """Handle OK button click with validation."""
        name = self.entry_var.get().strip()
        
        if not name:
            tk.messagebox.showerror("Error", "Name cannot be empty.")
            return
        
        if ' ' in name:
            tk.messagebox.showerror("Error", "Name cannot contain spaces.")
            return
        
        self.result = name
        self.dialog.destroy()

class NumberInputDialog:
    """
    Dialog for getting a number input from the user.
    """
    
    def __init__(self, parent, title, prompt, minimum=0, maximum=100, default=0):
        """
        Initialize the dialog.
        
        Args:
            parent: Parent window
            title: Dialog title
            prompt: Text prompt to display
            minimum: Minimum allowed value
            maximum: Maximum allowed value
            default: Default value
        """
        self.result = None
        self.minimum = minimum
        self.maximum = maximum
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center on parent
        window_width = 300
        window_height = 150
        
        # Calculate position
        position_right = parent.winfo_x() + (parent.winfo_width() // 2) - (window_width // 2)
        position_down = parent.winfo_y() + (parent.winfo_height() // 2) - (window_height // 2)
        
        # Set window size and position
        self.dialog.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
        
        # Add prompt
        ttk.Label(self.dialog, text=prompt).pack(pady=(20, 10))
        
        # Add spinbox for number entry
        self.value_var = tk.IntVar(value=default)
        spinbox = ttk.Spinbox(
            self.dialog, 
            from_=minimum, 
            to=maximum, 
            textvariable=self.value_var, 
            width=10
        )
        spinbox.pack(pady=(0, 20))
        spinbox.focus_set()
        
        # Add buttons
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(pady=(0, 20))
        
        ttk.Button(button_frame, text="OK", command=self.on_ok).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=self.on_cancel).pack(side=tk.LEFT)
        
        # Handle Enter key
        self.dialog.bind("<Return>", lambda event: self.on_ok())
        self.dialog.bind("<Escape>", lambda event: self.on_cancel())
        
        # Wait for dialog to close
        parent.wait_window(self.dialog)
    
    def on_ok(self):
        """Handle OK button click with validation."""
        try:
            value = int(self.value_var.get())
            if value < self.minimum or value > self.maximum:
                tk.messagebox.showerror(
                    "Error", 
                    f"Value must be between {self.minimum} and {self.maximum}."
                )
                return
            
            self.result = value
            self.dialog.destroy()
            
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid number.")
    
    def on_cancel(self):
        """Handle Cancel button click."""
        self.dialog.destroy()
    
class StateStyleDialog:
    def __init__(self, parent, automaton, visualizer):
        self.result = None
        self.automaton = automaton
        self.visualizer = visualizer
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("State Styling")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Set window size and position
        window_width = 400
        window_height = 400
        position_right = parent.winfo_x() + (parent.winfo_width() // 2) - (window_width // 2)
        position_down = parent.winfo_y() + (parent.winfo_height() // 2) - (window_height // 2)
        self.dialog.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
        
        # Create style options
        self.create_widgets()
        
        # Wait for dialog to close
        parent.wait_window(self.dialog)
    
    def create_widgets(self):
        # Create the main frame
        main_frame = ttk.Frame(self.dialog, padding=(10, 10, 10, 10))
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Get current colors from visualizer or use defaults
        current_colors = self.visualizer.custom_colors or {
            "regular": "white",
            "initial": "lightblue",
            "final": "lightgreen",
            "initial_final": "orange"
        }
        
        # Color options
        ttk.Label(main_frame, text="State Colors").grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        colors = ["white", "lightblue", "lightgreen", "orange", "yellow", "pink", "red", "blue", "green"]
        
        # Regular state color
        ttk.Label(main_frame, text="Regular state:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.regular_color_var = tk.StringVar(value=current_colors["regular"])
        regular_combo = ttk.Combobox(main_frame, textvariable=self.regular_color_var, width=15)
        regular_combo['values'] = colors
        regular_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Initial state color
        ttk.Label(main_frame, text="Initial state:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.initial_color_var = tk.StringVar(value=current_colors["initial"])
        initial_combo = ttk.Combobox(main_frame, textvariable=self.initial_color_var, width=15)
        initial_combo['values'] = colors
        initial_combo.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Final state color
        ttk.Label(main_frame, text="Final state:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.final_color_var = tk.StringVar(value=current_colors["final"])
        final_combo = ttk.Combobox(main_frame, textvariable=self.final_color_var, width=15)
        final_combo['values'] = colors
        final_combo.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Initial & Final state color
        ttk.Label(main_frame, text="Initial & Final:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.initial_final_color_var = tk.StringVar(value=current_colors["initial_final"])
        initial_final_combo = ttk.Combobox(main_frame, textvariable=self.initial_final_color_var, width=15)
        initial_final_combo['values'] = colors
        initial_final_combo.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Size options
        ttk.Label(main_frame, text="State Size").grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        ttk.Label(main_frame, text="Node size:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.node_size_var = tk.IntVar(value=700)
        node_size_spinbox = ttk.Spinbox(main_frame, from_=300, to=1200, increment=50, textvariable=self.node_size_var, width=5)
        node_size_spinbox.grid(row=7, column=1, sticky=tk.W, pady=5)
        
        # Label font size
        ttk.Label(main_frame, text="Font size:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.font_size_var = tk.IntVar(value=12)
        font_size_spinbox = ttk.Spinbox(main_frame, from_=8, to=20, increment=1, textvariable=self.font_size_var, width=5)
        font_size_spinbox.grid(row=8, column=1, sticky=tk.W, pady=5)
        
        # Shape options - future expansion
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=9, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="Apply", command=self.on_apply).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Close", command=self.on_close).pack(side=tk.LEFT)
    
    def on_state_selected(self, event):
        # Future enhancement: load individual state styling
        pass
    
    def on_apply(self):
        """Apply the selected style settings to the visualization."""
        # Update visualizer settings
        self.visualizer.custom_colors = {
            "regular": self.regular_color_var.get(),
            "initial": self.initial_color_var.get(),
            "final": self.final_color_var.get(),
            "initial_final": self.initial_final_color_var.get()
        }
        
        # Update visualization
        self.visualizer.visualize()
    
    def on_close(self):
        self.dialog.destroy()
        
class WordSimulationDialog:
    def __init__(self, parent, automaton, visualizer):
        self.automaton = automaton
        self.visualizer = visualizer
        self.simulator = None
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Word Processing Simulation")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Set window size and position
        window_width = 400
        window_height = 250
        position_right = parent.winfo_x() + (parent.winfo_width() // 2) - (window_width // 2)
        position_down = parent.winfo_y() + (parent.winfo_height() // 2) - (window_height // 2)
        self.dialog.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
        
        # Create widgets
        self.create_widgets()
        
        # Handle dialog close
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Wait for dialog to close
        parent.wait_window(self.dialog)
    
    def create_widgets(self):
        # Create the main frame
        main_frame = ttk.Frame(self.dialog, padding=(10, 10, 10, 10))
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Word input
        ttk.Label(main_frame, text="Enter word to process:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.word_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.word_var, width=30).grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Simulation speed
        ttk.Label(main_frame, text="Simulation speed:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        speed_frame = ttk.Frame(main_frame)
        speed_frame.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(speed_frame, from_=0.2, to=3.0, orient=tk.HORIZONTAL,
                               length=200, variable=self.speed_var)
        speed_scale.pack(side=tk.LEFT)
        
        speed_label = ttk.Label(speed_frame, text="1.0 sec")
        speed_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Update label when scale is moved
        def update_speed_label(event):
            speed_label.config(text=f"{speed_scale.get():.1f} sec")
        
        speed_scale.bind("<Motion>", update_speed_label)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="Start Simulation", command=self.start_simulation).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Close", command=self.on_close).pack(side=tk.LEFT)
    
    def start_simulation(self):
        """Start the word simulation."""
        word = self.word_var.get()
        speed = self.speed_var.get()
        
        if not word and word != "":  # Allow empty word
            messagebox.showinfo("Error", "Please enter a word to process.")
            return
        
        # Initialize the simulator
        from gui.visualization import AutomatonSimulator
        self.simulator = AutomatonSimulator(self.visualizer, self.automaton)
        
        # Start the simulation
        self.dialog.withdraw()  # Hide dialog during simulation
        self.simulator.simulate_word(word, speed)
        
        # Show dialog again after simulation
        self.dialog.deiconify()
    
    def on_close(self):
        """Handle dialog close."""
        # Stop any ongoing simulation
        if self.simulator and hasattr(self.simulator, 'timer'):
            self.simulator.timer.stop()
        
        self.dialog.destroy()