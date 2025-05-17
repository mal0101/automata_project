class Transition:
    """
    Represents a transition in a finite automaton.
    
    Attributes:
        source_state (State): Source state of the transition
        symbol (str): Symbol that triggers the transition
        target_state (State): Target state of the transition
    """
    
    def __init__(self, source_state, symbol, target_state):
        """Initialize a new transition."""
        self.source_state = source_state
        self.symbol = symbol
        self.target_state = target_state
    
    def __eq__(self, other):
        """Transitions are equal if all attributes are equal."""
        if not isinstance(other, Transition):
            return False
        return (self.source_state == other.source_state and
                self.symbol == other.symbol and
                self.target_state == other.target_state)
    
    def __hash__(self):
        """Hash implementation for using transitions in sets."""
        return hash((hash(self.source_state), self.symbol, hash(self.target_state)))
    
    def __str__(self):
        """String representation of the transition."""
        return f"{self.source_state.name} --{self.symbol}--> {self.target_state.name}"
    
    def to_dict(self):
        """Convert the transition to a dictionary for JSON serialization."""
        return {
            "source": self.source_state.name,
            "symbol": self.symbol,
            "target": self.target_state.name
        }