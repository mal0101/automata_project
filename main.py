import tkinter as tk
import os

def main():
    """Main application entry point."""
    # Create root window
    root = tk.Tk()
    root.title("Finite Automata Manager")
    
    # Set initial window size
    root.geometry("1200x700")
    
    # Set application icon (if available)
    try:
        root.iconbitmap("icon.ico")
    except:
        pass  # Icon not essential
    
    # Create automata directory if it doesn't exist
    if not os.path.exists("automata"):
        os.makedirs("automata")
    
    # Import and create main window
    from gui.main_window import MainWindow
    app = MainWindow(root)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()