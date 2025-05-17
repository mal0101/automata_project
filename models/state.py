class State:
    """
    Represents a state in a finite automaton.
    
    Attributes:
        name (str): Unique identifier for the state
        is_initial (bool): Whether the state is an initial state
        is_final (bool): Whether the state is a final/accepting state
    """
    
    def __init__(self, name, is_initial=False, is_final=False):
        """Initialize a new state."""
        self.name = name
        self.is_initial = is_initial
        self.is_final = is_final
    
    def __eq__(self, other):
        """States are equal if they have the same name."""
        if not isinstance(other, State):
            return False
        return self.name == other.name
    
    def __hash__(self):
        """Hash implementation for using states in sets and as dictionary keys."""
        return hash(self.name)
    
    def __str__(self):
        """String representation of the state."""
        return f"State({self.name}, initial={self.is_initial}, final={self.is_final})"
    
    def to_dict(self):
        """Convert the state to a dictionary for JSON serialization."""
        return {
            "name": self.name,
            "is_initial": self.is_initial,
            "is_final": self.is_final
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a state from a dictionary (for JSON deserialization)."""
        return cls(
            name=data["name"],
            is_initial=data["is_initial"],
            is_final=data["is_final"]
        )