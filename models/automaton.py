import os
import json
from collections import defaultdict, deque
from .state import State
from .alphabet import Alphabet
from .transition import Transition

class Automaton:
    """
    Represents a finite automaton.
    
    A finite automaton is defined as a 5-tuple (A, Q, I, T, E) where:
    - A is the alphabet
    - Q is the set of states
    - I ⊆ Q is the set of initial states
    - T ⊆ Q is the set of final/accepting states
    - E ⊆ Q × A × Q is the set of transitions
    
    Attributes:
        name (str): Name of the automaton
        alphabet (Alphabet): Alphabet of the automaton
        states (list): List of states in the automaton
        transitions (list): List of transitions in the automaton
    """
    
    def __init__(self, name="", alphabet=None, states=None, transitions=None):
        """Initialize a new automaton."""
        self.name = name
        self.alphabet = alphabet if alphabet else Alphabet()
        self.states = states if states else []
        self.transitions = transitions if transitions else []
    
    @property
    def initial_states(self):
        """Get all initial states in the automaton."""
        return [state for state in self.states if state.is_initial]
    
    @property
    def final_states(self):
        """Get all final states in the automaton."""
        return [state for state in self.states if state.is_final]
    
    def get_state_by_name(self, name):
        """Find a state by its name."""
        for state in self.states:
            if state.name == name:
                return state
        return None
    
    def add_state(self, state):
        """Add a state to the automaton if it doesn't already exist."""
        if not self.get_state_by_name(state.name):
            self.states.append(state)
            return True
        return False
    
    def update_state(self, state_name, is_initial=None, is_final=None):
        """Update properties of an existing state."""
        state = self.get_state_by_name(state_name)
        if state:
            if is_initial is not None:
                state.is_initial = is_initial
            if is_final is not None:
                state.is_final = is_final
            return True
        return False
    
    def remove_state(self, state):
        """Remove a state and all its associated transitions."""
        if isinstance(state, str):
            state = self.get_state_by_name(state)
        
        if state in self.states:
            self.states.remove(state)
            # Remove all transitions involving this state
            self.transitions = [t for t in self.transitions 
                               if t.source_state != state and t.target_state != state]
            return True
        return False
    
    def add_transition(self, source_state, symbol, target_state):
        """Add a transition to the automaton."""
        # Ensure states are State objects
        if isinstance(source_state, str):
            source_state = self.get_state_by_name(source_state)
            if not source_state:
                return False
        
        if isinstance(target_state, str):
            target_state = self.get_state_by_name(target_state)
            if not target_state:
                return False
        
        # Add states if they don't exist
        if source_state not in self.states:
            self.add_state(source_state)
        
        if target_state not in self.states:
            self.add_state(target_state)
        
        # Add symbol to alphabet if not epsilon
        if symbol != self.alphabet.epsilon:
            self.alphabet.add_symbol(symbol)
        
        # Create and add transition
        transition = Transition(source_state, symbol, target_state)
        if transition not in self.transitions:
            self.transitions.append(transition)
            return True
        return False
    
    def remove_transition(self, transition):
        """Remove a transition from the automaton."""
        if transition in self.transitions:
            self.transitions.remove(transition)
            return True
        return False
    
    def get_transitions_from(self, state, symbol=None):
        """Get transitions originating from a state, optionally filtered by symbol."""
        if isinstance(state, str):
            state = self.get_state_by_name(state)
        
        if not state:
            return []
        
        if symbol is None:
            return [t for t in self.transitions if t.source_state == state]
        else:
            return [t for t in self.transitions 
                   if t.source_state == state and t.symbol == symbol]
    
    def get_transitions_to(self, state, symbol=None):
        """Get transitions leading to a state, optionally filtered by symbol."""
        if isinstance(state, str):
            state = self.get_state_by_name(state)
        
        if not state:
            return []
        
        if symbol is None:
            return [t for t in self.transitions if t.target_state == state]
        else:
            return [t for t in self.transitions 
                   if t.target_state == state and t.symbol == symbol]
    
    def get_reachable_states(self, state, symbol):
        """Get states reachable from a state via a given symbol."""
        transitions = self.get_transitions_from(state, symbol)
        return [t.target_state for t in transitions]
    
    def to_dict(self):
        """Convert the automaton to a dictionary for JSON serialization."""
        return {
            "name": self.name,
            "alphabet": self.alphabet.to_dict(),
            "states": [state.to_dict() for state in self.states],
            "transitions": [t.to_dict() for t in self.transitions]
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create an automaton from a dictionary (for JSON deserialization)."""
        automaton = cls(name=data["name"])
        
        # Load alphabet
        automaton.alphabet = Alphabet.from_dict(data["alphabet"])
        
        # Load states
        for state_data in data["states"]:
            state = State.from_dict(state_data)
            automaton.add_state(state)
        
        # Load transitions
        for trans_data in data["transitions"]:
            source = automaton.get_state_by_name(trans_data["source"])
            target = automaton.get_state_by_name(trans_data["target"])
            if source and target:
                automaton.add_transition(source, trans_data["symbol"], target)
        
        return automaton
    
    def save_to_file(self, directory="automata"):
        """Save the automaton to a JSON file."""
        os.makedirs(directory, exist_ok=True)
        filename = os.path.join(directory, f"{self.name}.json")
        
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)
        
        return filename
    
    @classmethod
    def load_from_file(cls, filename):
        """Load an automaton from a JSON file."""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        return cls.from_dict(data)
    
    def copy(self):
        """Create a deep copy of the automaton."""
        new_automaton = Automaton(name=self.name)
        
        # Copy alphabet
        for symbol in self.alphabet.symbols:
            new_automaton.alphabet.add_symbol(symbol)
        
        # Copy states
        for state in self.states:
            new_state = State(state.name, state.is_initial, state.is_final)
            new_automaton.add_state(new_state)
        
        # Copy transitions
        for transition in self.transitions:
            source = new_automaton.get_state_by_name(transition.source_state.name)
            target = new_automaton.get_state_by_name(transition.target_state.name)
            new_automaton.add_transition(source, transition.symbol, target)
        
        return new_automaton