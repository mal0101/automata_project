import tkinter as tk
from tkinter import ttk

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