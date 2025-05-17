import tkinter as tk
from tkinter import ttk
import os
import sys
import matplotlib
import networkx as nx

def check_requirements():
    """
    Check if all required libraries are installed.
    
    Returns:
        bool: True if all requirements are met, False otherwise
    """
    try:
        import tkinter
        import matplotlib
        import networkx
        return True
    except ImportError as e:
        print(f"Error: Missing required library: {e}")
        print("Please install required libraries using pip:")
        print("pip install matplotlib networkx")
        return False

def setup_environment():
    """
    Set up the application environment.
    
    Creates necessary directories and initializes matplotlib backend.
    """
    # Create automata directory if it doesn't exist
    if not os.path.exists("automata"):
        os.makedirs("automata")
    
    # Configure matplotlib to work with tkinter
    matplotlib.use("TkAgg")

def apply_theme(root):
    """
    Apply visual theme to the application.
    
    Args:
        root: The Tkinter root window
    """
    # Try to use a more modern theme if available
    try:
        style = ttk.Style()
        available_themes = style.theme_names()
        
        # Prefer these themes in order
        preferred_themes = ['clam', 'alt', 'vista', 'xpnative']
        
        for theme in preferred_themes:
            if theme in available_themes:
                style.theme_use(theme)
                break
    except Exception as e:
        print(f"Warning: Could not apply theme: {e}")

def main():
    """
    Main application entry point.
    """
    # Check if requirements are met
    if not check_requirements():
        sys.exit(1)
    
    # Set up environment
    setup_environment()
    
    # Create root window
    root = tk.Tk()
    root.title("Finite Automata Manager")
    
    # Set initial window size
    root.geometry("1200x700")
    
    # Apply visual theme
    apply_theme(root)
    
    # Set application icon (if available)
    try:
        if os.path.exists("icon.ico"):
            root.iconbitmap("icon.ico")
    except:
        pass  # Icon not essential
    
    # Import and create main window
    from gui.main_window import MainWindow
    app = MainWindow(root)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()