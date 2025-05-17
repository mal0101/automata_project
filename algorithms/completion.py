from models.state import State

class CompletionOperations:
    """
    Operations for completing automata.
    
    A complete DFA has a transition defined for every state and every symbol
    in the alphabet. This class provides methods to check if an automaton is
    complete and to complete it if necessary.
    """
    
    @staticmethod
    def is_complete(automaton):
        """
        Check if an automaton is complete.
        
        An automaton is complete if for every state and every symbol in the alphabet,
        there is at least one transition defined.
        
        Args:
            automaton: The automaton to check
            
        Returns:
            bool: True if complete, False otherwise
        """
        # First ensure it's deterministic
        from algorithms.deterministic import DeterministicOperations
        if not DeterministicOperations.is_deterministic(automaton):
            return False
        
        # Check if each state has a transition for each symbol
        for state in automaton.states:
            for symbol in automaton.alphabet.symbols:
                targets = automaton.get_reachable_states(state, symbol)
                if not targets:
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
        
        # First ensure it's deterministic
        from algorithms.deterministic import DeterministicOperations
        if not DeterministicOperations.is_deterministic(automaton):
            from algorithms.conversion import ConversionOperations
            dfa = ConversionOperations.nfa_to_dfa(automaton)
        else:
            dfa = automaton.copy()
        
        # If it's already complete, return it
        if CompletionOperations.is_complete(dfa):
            return dfa
        
        # Create a new automaton for the result
        result = dfa.copy()
        result.name = f"{dfa.name}_complete"
        
        # Create a sink state
        sink_state = State("sink", is_initial=False, is_final=False)
        result.add_state(sink_state)
        
        # For each state and symbol, add missing transitions to sink state
        for state in result.states:
            for symbol in result.alphabet.symbols:
                targets = result.get_reachable_states(state, symbol)
                if not targets:
                    result.add_transition(state, symbol, sink_state)
        
        # Add self-loops for the sink state
        for symbol in result.alphabet.symbols:
            result.add_transition(sink_state, symbol, sink_state)
        
        return result
    
    @staticmethod
    def add_trap_state(automaton):
        """
        Add a trap (sink) state to an automaton.
        
        This is useful for explicitly representing rejection in a visualization.
        
        Args:
            automaton: The automaton to modify
            
        Returns:
            Automaton: A new automaton with a trap state
        """
        from models.automaton import Automaton
        
        # Create a copy
        result = automaton.copy()
        
        # Create a trap state
        trap_state = State("trap", is_initial=False, is_final=False)
        result.add_state(trap_state)
        
        # For each state and symbol, if no transition exists, add one to trap
        for state in result.states:
            if state == trap_state:
                continue
                
            for symbol in result.alphabet.symbols:
                targets = result.get_reachable_states(state, symbol)
                if not targets:
                    result.add_transition(state, symbol, trap_state)
        
        # Add self-loops for all symbols from trap state
        for symbol in result.alphabet.symbols:
            result.add_transition(trap_state, symbol, trap_state)
        
        return result