class DeterministicOperations:
    """
    Operations related to deterministic properties of automata.
    """
    
    @staticmethod
    def is_deterministic(automaton):
        """
        Check if an automaton is deterministic.
        
        An automaton is deterministic if:
        1. It has exactly one initial state
        2. It has no epsilon transitions
        3. For each state and symbol, there is at most one transition
        
        Args:
            automaton: The automaton to check
            
        Returns:
            bool: True if the automaton is deterministic, False otherwise
        """
        # Check if there's exactly one initial state
        if len(automaton.initial_states) != 1:
            return False
        
        # Check for epsilon transitions
        if any(t.symbol == automaton.alphabet.epsilon for t in automaton.transitions):
            return False
        
        # Check for uniqueness of transitions
        for state in automaton.states:
            for symbol in automaton.alphabet.symbols:
                if len(automaton.get_reachable_states(state, symbol)) > 1:
                    return False
        
        return True
    
    @staticmethod
    def is_complete(automaton):
        """
        Check if an automaton is complete.
        
        An automaton is complete if for each state and symbol in the alphabet,
        there is at least one outgoing transition.
        
        Args:
            automaton: The automaton to check
            
        Returns:
            bool: True if the automaton is complete, False otherwise
        """
        # Check if the automaton is deterministic first
        if not DeterministicOperations.is_deterministic(automaton):
            return False
        
        # For each state and symbol, check if there's at least one transition
        for state in automaton.states:
            for symbol in automaton.alphabet.symbols:
                if not automaton.get_reachable_states(state, symbol):
                    return False
        
        return True
    
    @staticmethod
    def complete_automaton(automaton):
        """
        Complete an automaton by adding a sink state and missing transitions.
        
        Args:
            automaton: The automaton to complete
            
        Returns:
            Automaton: A new, completed automaton
        """
        from models.automaton import Automaton
        from models.state import State
        
        # Create a copy to avoid modifying the original
        result = automaton.copy()
        result.name = f"{automaton.name}_completed"
        
        # If not deterministic, convert to DFA first
        if not DeterministicOperations.is_deterministic(result):
            from algorithms.conversion import ConversionOperations
            result = ConversionOperations.nfa_to_dfa(result)
        
        # Check if already complete
        if DeterministicOperations.is_complete(result):
            return result
        
        # Add sink state
        sink_state = State("sink", is_initial=False, is_final=False)
        result.add_state(sink_state)
        
        # Add missing transitions to sink state
        for state in result.states:
            for symbol in result.alphabet.symbols:
                if not result.get_reachable_states(state, symbol):
                    result.add_transition(state, symbol, sink_state)
        
        # Add self-loops for all symbols from sink state
        for symbol in result.alphabet.symbols:
            result.add_transition(sink_state, symbol, sink_state)
        
        return result