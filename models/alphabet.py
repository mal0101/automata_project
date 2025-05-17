class Alphabet:
    """
    Represents the alphabet of a finite automaton.
    
    Attributes:
        symbols (set): Set of symbols in the alphabet
        epsilon (str): Special symbol for epsilon transitions
    """
    
    def __init__(self, symbols=None):
        """Initialize a new alphabet with optional initial symbols."""
        self.symbols = set(symbols) if symbols else set()
        self.epsilon = 'ε'  # Epsilon symbol for empty transitions
    
    def add_symbol(self, symbol):
        """Add a symbol to the alphabet."""
        if symbol != self.epsilon:  # Epsilon is special and not part of alphabet
            self.symbols.add(symbol)
    
    def remove_symbol(self, symbol):
        """Remove a symbol from the alphabet."""
        if symbol in self.symbols:
            self.symbols.remove(symbol)
    
    def contains(self, symbol):
        """Check if the alphabet contains a symbol or if it's epsilon."""
        return symbol in self.symbols or symbol == self.epsilon
    
    def __str__(self):
        """String representation of the alphabet."""
        return f"Alphabet({', '.join(sorted(self.symbols))})"
    
    def to_dict(self):
        """Convert the alphabet to a dictionary for JSON serialization."""
        return {
            "symbols": list(self.symbols)
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create an alphabet from a dictionary (for JSON deserialization)."""
        return cls(symbols=set(data["symbols"]))