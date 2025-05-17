import os
import json
import glob
from models.automaton import Automaton

class FileManager:
    """
    Manages automaton file operations including saving, loading, and listing.
    """
    
    def __init__(self, directory="automata"):
        """
        Initialize the file manager.
        
        Args:
            directory (str): Directory for storing automaton files
        """
        self.directory = directory
        
        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def save_automaton(self, automaton):
        """
        Save an automaton to a file.
        
        Args:
            automaton: The automaton to save
            
        Returns:
            str: Path to the saved file
        """
        # Create filename from automaton name
        filename = os.path.join(self.directory, f"{automaton.name}.json")
        
        # Convert automaton to dictionary
        data = automaton.to_dict()
        
        # Save to file
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        
        return filename
    
    def load_automaton(self, filename):
        """
        Load an automaton from a file.
        
        Args:
            filename: Path to the file to load
            
        Returns:
            Automaton: The loaded automaton
        """
        # If only a name is provided, construct the full path
        if not os.path.dirname(filename):
            filename = os.path.join(self.directory, f"{filename}.json")
        
        # Load JSON data
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Create automaton from data
        return Automaton.from_dict(data)
    
    def delete_automaton(self, name):
        """
        Delete an automaton file.
        
        Args:
            name: Name of the automaton to delete
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        # Construct filename
        filename = os.path.join(self.directory, f"{name}.json")
        
        # Check if file exists
        if not os.path.exists(filename):
            return False
        
        # Delete the file
        os.remove(filename)
        return True
    
    def list_automata(self):
        """
        List all saved automata.
        
        Returns:
            list: List of automaton names (without .json extension)
        """
        # Get all JSON files in the directory
        pattern = os.path.join(self.directory, "*.json")
        files = glob.glob(pattern)
        
        # Extract names without path and extension
        names = [os.path.splitext(os.path.basename(f))[0] for f in files]
        
        return sorted(names)
    
    def automaton_exists(self, name):
        """
        Check if an automaton with the given name exists.
        
        Args:
            name: Name to check
            
        Returns:
            bool: True if an automaton with this name exists, False otherwise
        """
        filename = os.path.join(self.directory, f"{name}.json")
        return os.path.exists(filename)
    
    def rename_automaton(self, old_name, new_name):
        """
        Rename an automaton file.
        
        Args:
            old_name: Current name of the automaton
            new_name: New name for the automaton
            
        Returns:
            bool: True if renamed successfully, False otherwise
        """
        old_filename = os.path.join(self.directory, f"{old_name}.json")
        new_filename = os.path.join(self.directory, f"{new_name}.json")
        
        # Check if source file exists and target doesn't
        if not os.path.exists(old_filename):
            return False
        
        if os.path.exists(new_filename):
            return False
        
        # Rename the file
        os.rename(old_filename, new_filename)
        return True