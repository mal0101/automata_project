import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class MainWindow:
    """
    Main application window for the Finite Automata Manager.
    """
    
    def __init__(self, root):
        """
        Initialize the main window.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Finite Automata Manager")
        self.root.geometry("1200x700")
        
        # Initialize references to other components
        self.automaton_editor = None
        self.current_automaton = None
        
        # Create main menu
        self.create_menu()
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create sidebar for automata list
        self.create_sidebar()
        
        # Create main content area
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create welcome screen
        self.create_welcome_screen()
        
        # Load automata list
        self.refresh_automaton_list()
    
    def create_menu(self):
        """Create the main menu bar."""
        menubar = tk.Menu(self.root)
        
        # Automata menu
        automata_menu = tk.Menu(menubar, tearoff=0)
        automata_menu.add_command(label="Create New", command=self.create_new_automaton)
        automata_menu.add_command(label="Open", command=self.open_automaton)
        automata_menu.add_command(label="Save", command=self.save_automaton)
        automata_menu.add_command(label="Save As", command=self.save_automaton_as)
        automata_menu.add_separator()
        automata_menu.add_command(label="Delete", command=self.delete_automaton)
        automata_menu.add_separator()
        automata_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="Automata", menu=automata_menu)
        
        # Analysis menu
        analysis_menu = tk.Menu(menubar, tearoff=0)
        analysis_menu.add_command(label="Check Deterministic", command=self.check_deterministic)
        analysis_menu.add_command(label="Convert NFA to DFA", command=self.convert_nfa_to_dfa)
        analysis_menu.add_command(label="Check Complete", command=self.check_complete)
        analysis_menu.add_command(label="Complete Automaton", command=self.complete_automaton)
        analysis_menu.add_command(label="Check Minimal", command=self.check_minimal)
        analysis_menu.add_command(label="Minimize Automaton", command=self.minimize_automaton)
        menubar.add_cascade(label="Analysis", menu=analysis_menu)
        
        # Advanced menu
        advanced_menu = tk.Menu(menubar, tearoff=0)
        advanced_menu.add_command(label="Test Word", command=self.test_word)
        advanced_menu.add_command(label="Generate Accepted Words", command=self.generate_accepted_words)
        advanced_menu.add_command(label="Generate Rejected Words", command=self.generate_rejected_words)
        advanced_menu.add_separator()
        advanced_menu.add_command(label="Check Equivalence", command=self.check_equivalence)
        advanced_menu.add_command(label="Union", command=self.compute_union)
        advanced_menu.add_command(label="Intersection", command=self.compute_intersection)
        advanced_menu.add_command(label="Complement", command=self.compute_complement)
        menubar.add_cascade(label="Advanced", menu=advanced_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_sidebar(self):
        """Create the sidebar with automata list."""
        sidebar = ttk.Frame(self.main_frame, width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Add a label
        label = ttk.Label(sidebar, text="Saved Automata:")
        label.pack(anchor=tk.W, pady=(0, 5))
        
        # Add automata list with scrollbar
        list_frame = ttk.Frame(sidebar)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.automata_list = tk.Listbox(list_frame, width=25, height=20)
        self.automata_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.automata_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.automata_list.yview)
        
        # Bind double-click event
        self.automata_list.bind("<Double-1>", self.on_automaton_selected)
        
        # Add buttons
        button_frame = ttk.Frame(sidebar)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="New", command=self.create_new_automaton).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Open", command=self.open_selected_automaton).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Delete", command=self.delete_automaton).pack(side=tk.LEFT)
    
    def create_welcome_screen(self):
        """Create the welcome screen displayed on startup."""
        welcome_frame = ttk.Frame(self.content_frame)
        welcome_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add a welcome message
        title = ttk.Label(welcome_frame, text="Welcome to Finite Automata Manager", font=("Arial", 16))
        title.pack(pady=(50, 20))
        
        msg = ttk.Label(welcome_frame, text="Create a new automaton or open an existing one to get started.", font=("Arial", 12))
        msg.pack(pady=(0, 30))
        
        # Add quick action buttons
        button_frame = ttk.Frame(welcome_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Create New Automaton", command=self.create_new_automaton).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Open Automaton", command=self.open_automaton).pack(side=tk.LEFT, padx=10)
    
    def refresh_automaton_list(self):
        """Refresh the list of saved automata."""
        self.automata_list.delete(0, tk.END)
        
        # Ensure automata directory exists
        if not os.path.exists("automata"):
            os.makedirs("automata")
        
        # List all JSON files
        files = [f for f in os.listdir("automata") if f.endswith(".json")]
        files.sort()
        
        for file in files:
            # Remove .json extension for display
            name = file[:-5]
            self.automata_list.insert(tk.END, name)
    
    def on_automaton_selected(self, event):
        """Handle automaton selection from the list."""
        self.open_selected_automaton()
    
    def open_selected_automaton(self):
        """Open the selected automaton from the list."""
        selection = self.automata_list.curselection()
        if not selection:
            messagebox.showinfo("Information", "Please select an automaton to open.")
            return
        
        automaton_name = self.automata_list.get(selection[0])
        filename = os.path.join("automata", f"{automaton_name}.json")
        
        self.load_automaton(filename)
    
    def load_automaton(self, filename):
        """Load an automaton from a file and display it."""
        from models.automaton import Automaton
        
        try:
            automaton = Automaton.load_from_file(filename)
            self.current_automaton = automaton
            
            # Clear content frame
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            
            # Create editor for this automaton
            from gui.automaton_editor import AutomatonEditor
            self.automaton_editor = AutomatonEditor(self.content_frame, automaton, self)
            
            messagebox.showinfo("Success", f"Automaton '{automaton.name}' loaded successfully.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load automaton: {str(e)}")
    
    # Menu command handlers
    
    def create_new_automaton(self):
        """Create a new automaton."""
        from gui.dialogs import NameInputDialog
        dialog = NameInputDialog(self.root, "New Automaton", "Enter automaton name:")
        
        if dialog.result:
            name = dialog.result
            
            # Check if name already exists
            if os.path.exists(os.path.join("automata", f"{name}.json")):
                messagebox.showerror("Error", f"Automaton '{name}' already exists.")
                return
            
            # Create new automaton
            from models.automaton import Automaton
            self.current_automaton = Automaton(name=name)
            
            # Clear content frame
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            
            # Create editor for this automaton
            from gui.automaton_editor import AutomatonEditor
            self.automaton_editor = AutomatonEditor(self.content_frame, self.current_automaton, self)
    
    def open_automaton(self):
        """Open an automaton from a file."""
        filename = filedialog.askopenfilename(
            initialdir="automata",
            title="Open Automaton",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        
        if filename:
            self.load_automaton(filename)
            self.refresh_automaton_list()
    
    def save_automaton(self):
        """Save the current automaton."""
        if not self.current_automaton:
            messagebox.showinfo("Information", "No automaton to save.")
            return
        
        try:
            filename = self.current_automaton.save_to_file()
            messagebox.showinfo("Success", f"Automaton saved to {filename}")
            self.refresh_automaton_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save automaton: {str(e)}")
    
    def save_automaton_as(self):
        """Save the current automaton with a new name."""
        if not self.current_automaton:
            messagebox.showinfo("Information", "No automaton to save.")
            return
        
        from gui.dialogs import NameInputDialog
        dialog = NameInputDialog(self.root, "Save As", "Enter new automaton name:")
        
        if dialog.result:
            old_name = self.current_automaton.name
            self.current_automaton.name = dialog.result
            
            try:
                filename = self.current_automaton.save_to_file()
                messagebox.showinfo("Success", f"Automaton saved to {filename}")
                self.refresh_automaton_list()
                
                # Update editor title if it exists
                if self.automaton_editor:
                    self.automaton_editor.update_title()
                    
            except Exception as e:
                # Restore old name on error
                self.current_automaton.name = old_name
                messagebox.showerror("Error", f"Failed to save automaton: {str(e)}")
    
    def delete_automaton(self):
        """Delete the selected automaton."""
        selection = self.automata_list.curselection()
        if not selection:
            messagebox.showinfo("Information", "Please select an automaton to delete.")
            return
        
        automaton_name = self.automata_list.get(selection[0])
        filename = os.path.join("automata", f"{automaton_name}.json")
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{automaton_name}'?"):
            try:
                os.remove(filename)
                messagebox.showinfo("Success", f"Automaton '{automaton_name}' deleted.")
                
                # Close editor if the deleted automaton is currently open
                if self.current_automaton and self.current_automaton.name == automaton_name:
                    self.current_automaton = None
                    for widget in self.content_frame.winfo_children():
                        widget.destroy()
                    self.create_welcome_screen()
                
                self.refresh_automaton_list()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete automaton: {str(e)}")
    
    # Analysis menu handlers
    
    def check_deterministic(self):
        """Check if the current automaton is deterministic."""
        if not self.current_automaton:
            messagebox.showinfo("Information", "No automaton loaded.")
            return
        
        from algorithms.deterministic import DeterministicOperations
        is_deterministic = DeterministicOperations.is_deterministic(self.current_automaton)
        
        if is_deterministic:
            messagebox.showinfo("Result", "The automaton is deterministic.")
        else:
            messagebox.showinfo("Result", "The automaton is non-deterministic.")
    
    def convert_nfa_to_dfa(self):
        """Convert the current NFA to a DFA."""
        if not self.current_automaton:
            messagebox.showinfo("Information", "No automaton loaded.")
            return
        
        from algorithms.deterministic import DeterministicOperations
        if DeterministicOperations.is_deterministic(self.current_automaton):
            messagebox.showinfo("Result", "The automaton is already deterministic.")
            return
        
        from algorithms.conversion import ConversionOperations
        dfa = ConversionOperations.nfa_to_dfa(self.current_automaton)
        
        # Save the resulting DFA
        dfa.save_to_file()
        self.refresh_automaton_list()
        
        messagebox.showinfo("Success", f"Converted to DFA and saved as '{dfa.name}'.")
    
    def check_complete(self):
        """Check if the current automaton is complete."""
        if not self.current_automaton:
            messagebox.showinfo("Information", "No automaton loaded.")
            return
        
        from algorithms.deterministic import DeterministicOperations
        
        # Check if deterministic first
        if not DeterministicOperations.is_deterministic(self.current_automaton):
            messagebox.showinfo("Result", "The automaton must be deterministic to check completeness.")
            return
        
        is_complete = DeterministicOperations.is_complete(self.current_automaton)
        
        if is_complete:
            messagebox.showinfo("Result", "The automaton is complete.")
        else:
            messagebox.showinfo("Result", "The automaton is not complete.")
    
    def complete_automaton(self):
        """Complete the current automaton."""
        if not self.current_automaton:
            messagebox.showinfo("Information", "No automaton loaded.")
            return
        
        from algorithms.deterministic import DeterministicOperations
        
        # Check if already complete
        if DeterministicOperations.is_complete(self.current_automaton):
            messagebox.showinfo("Result", "The automaton is already complete.")
            return
        
        # Complete the automaton
        completed = DeterministicOperations.complete_automaton(self.current_automaton)
        
        # Save the completed automaton
        completed.save_to_file()
        self.refresh_automaton_list()
        
        messagebox.showinfo("Success", f"Completed automaton saved as '{completed.name}'.")
    
    def check_minimal(self):
        """Check if the current automaton is minimal."""
        if not self.current_automaton:
            messagebox.showinfo("Information", "No automaton loaded.")
            return
        
        from algorithms.minimization import MinimizationOperations
        is_minimal = MinimizationOperations.is_minimal(self.current_automaton)
        
        if is_minimal:
            messagebox.showinfo("Result", "The automaton is minimal.")
        else:
            messagebox.showinfo("Result", "The automaton is not minimal.")
    
    def minimize_automaton(self):
        """Minimize the current automaton."""
        if not self.current_automaton:
            messagebox.showinfo("Information", "No automaton loaded.")
            return
        
        from algorithms.minimization import MinimizationOperations
        
        # Check if already minimal
        if MinimizationOperations.is_minimal(self.current_automaton):
            messagebox.showinfo("Result", "The automaton is already minimal.")
            return
        
        # Minimize the automaton
        minimized = MinimizationOperations.minimize(self.current_automaton)
        
        # Save the minimized automaton
        minimized.save_to_file()
        self.refresh_automaton_list()
        
        messagebox.showinfo("Success", f"Minimized automaton saved as '{minimized.name}'.")
    
    # Advanced menu handlers
    
    def test_word(self):
        """Test if a word is accepted by the current automaton."""
        if not self.current_automaton:
            messagebox.showinfo("Information", "No automaton loaded.")
            return
        
        from gui.dialogs import TextInputDialog
        dialog = TextInputDialog(self.root, "Test Word", "Enter word to test:")
        
        if dialog.result is not None:
            word = dialog.result
            
            from algorithms.language_ops import LanguageOperations
            is_accepted = LanguageOperations.accepts_word(self.current_automaton, word)
            
            if is_accepted:
                messagebox.showinfo("Result", f"The word '{word}' is accepted by the automaton.")
            else:
                messagebox.showinfo("Result", f"The word '{word}' is rejected by the automaton.")
    
    def generate_accepted_words(self):
        """Generate words accepted by the current automaton."""
        if not self.current_automaton:
            messagebox.showinfo("Information", "No automaton loaded.")
            return
        
        from gui.dialogs import NumberInputDialog
        dialog = NumberInputDialog(self.root, "Generate Words", 
                                 "Maximum word length:", 
                                 minimum=0, maximum=10, default=3)
        
        if dialog.result is not None:
            max_length = dialog.result
            
            from algorithms.language_ops import LanguageOperations
            words = LanguageOperations.generate_words(
                self.current_automaton, max_length, accepted=True)
            
            if words:
                self.show_word_list("Accepted Words", words)
            else:
                messagebox.showinfo("Result", "No words are accepted up to this length.")
    
    def generate_rejected_words(self):
        """Generate words rejected by the current automaton."""
        if not self.current_automaton:
            messagebox.showinfo("Information", "No automaton loaded.")
            return
        
        from gui.dialogs import NumberInputDialog
        dialog = NumberInputDialog(self.root, "Generate Words", 
                                 "Maximum word length:", 
                                 minimum=0, maximum=10, default=3)
        
        if dialog.result is not None:
            max_length = dialog.result
            
            from algorithms.language_ops import LanguageOperations
            words = LanguageOperations.generate_words(
                self.current_automaton, max_length, accepted=False)
            
            if words:
                self.show_word_list("Rejected Words", words)
            else:
                messagebox.showinfo("Result", 
                                    "All words up to this length are accepted.")
    
    def show_word_list(self, title, words):
        """Show a list of words in a dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create a scrollable text area
        frame = ttk.Frame(dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_area = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        text_area.pack(fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=text_area.yview)
        
        # Insert words
        for word in words:
            if word == '':
                word = 'ε (empty word)'
            text_area.insert(tk.END, word + '\n')
        
        text_area.config(state=tk.DISABLED)
        
        # Add close button
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)
    
    def check_equivalence(self):
        """Check if two automata are equivalent."""
        if not self.current_automaton:
            messagebox.showinfo("Information", "No automaton loaded.")
            return
        
        # Let the user select another automaton
        filename = filedialog.askopenfilename(
            initialdir="automata",
            title="Select Second Automaton",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        
        if not filename:
            return
        
        try:
            from models.automaton import Automaton
            other_automaton = Automaton.load_from_file(filename)
            
            from algorithms.language_ops import LanguageOperations
            are_equivalent = LanguageOperations.are_equivalent(
                self.current_automaton, other_automaton)
            
            if are_equivalent:
                messagebox.showinfo("Result", 
                                   f"The automata '{self.current_automaton.name}' and "
                                   f"'{other_automaton.name}' are equivalent.")
            else:
                messagebox.showinfo("Result", 
                                   f"The automata '{self.current_automaton.name}' and "
                                   f"'{other_automaton.name}' are not equivalent.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compare automata: {str(e)}")
    
    def compute_union(self):
        """Compute the union of two automata."""
        if not self.current_automaton:
            messagebox.showinfo("Information", "No automaton loaded.")
            return
        
        # Let the user select another automaton
        filename = filedialog.askopenfilename(
            initialdir="automata",
            title="Select Second Automaton",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        
        if not filename:
            return
        
        try:
            from models.automaton import Automaton
            other_automaton = Automaton.load_from_file(filename)
            
            from algorithms.language_ops import LanguageOperations
            union = LanguageOperations.union(self.current_automaton, other_automaton)
            
            # Save the union automaton
            union.save_to_file()
            self.refresh_automaton_list()
            
            messagebox.showinfo("Success", 
                               f"Union automaton saved as '{union.name}'.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compute union: {str(e)}")
    
    def compute_intersection(self):
        """Compute the intersection of two automata."""
        if not self.current_automaton:
            messagebox.showinfo("Information", "No automaton loaded.")
            return
        
        # Let the user select another automaton
        filename = filedialog.askopenfilename(
            initialdir="automata",
            title="Select Second Automaton",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        
        if not filename:
            return
        
        try:
            from models.automaton import Automaton
            other_automaton = Automaton.load_from_file(filename)
            
            from algorithms.language_ops import LanguageOperations
            intersection = LanguageOperations.intersection(
                self.current_automaton, other_automaton)
            
            # Save the intersection automaton
            intersection.save_to_file()
            self.refresh_automaton_list()
            
            messagebox.showinfo("Success", 
                               f"Intersection automaton saved as '{intersection.name}'.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compute intersection: {str(e)}")
    
    def compute_complement(self):
        """Compute the complement of the current automaton."""
        if not self.current_automaton:
            messagebox.showinfo("Information", "No automaton loaded.")
            return
        
        try:
            from algorithms.language_ops import LanguageOperations
            complement = LanguageOperations.complement(self.current_automaton)
            
            # Save the complement automaton
            complement.save_to_file()
            self.refresh_automaton_list()
            
            messagebox.showinfo("Success", 
                               f"Complement automaton saved as '{complement.name}'.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compute complement: {str(e)}")
    
    def show_about(self):
        """Show information about the application."""
        messagebox.showinfo("About", 
                           "Finite Automata Manager\n\n"
                           "A complete application for creating, managing, and analyzing "
                           "finite automata (both deterministic and non-deterministic).\n\n"
                           "Developed for a Mathematics for Engineers module at ENSAM Casablanca.")
    