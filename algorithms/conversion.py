class ConversionOperations:
    """
    Operations for converting between different types of automata.
    """
    
    @staticmethod
    def epsilon_closure(automaton, states):
        """
        Compute the epsilon closure of a set of states.
        
        The epsilon closure of a set of states S is the set of all states that can be
        reached from S by following only epsilon transitions.
        
        Args:
            automaton: The automaton
            states: A list or set of states
            
        Returns:
            set: The epsilon closure of the given states
        """
        epsilon = automaton.alphabet.epsilon
        closure = set(states)
        worklist = list(states)
        
        while worklist:
            state = worklist.pop(0)
            
            # Get all states reachable via epsilon transitions
            for transition in automaton.get_transitions_from(state, epsilon):
                target = transition.target_state
                if target not in closure:
                    closure.add(target)
                    worklist.append(target)
        
        return closure
    
    @staticmethod
    def nfa_to_dfa(automaton):
        """
        Convert a non-deterministic finite automaton (NFA) to a 
        deterministic finite automaton (DFA) using the subset construction algorithm.
        
        Args:
            automaton: The NFA to convert
            
        Returns:
            Automaton: An equivalent DFA
        """
        from models.automaton import Automaton
        from models.state import State
        from models.alphabet import Alphabet
        
        # If already deterministic, just return a copy
        from algorithms.deterministic import DeterministicOperations
        if DeterministicOperations.is_deterministic(automaton):
            return automaton.copy()
        
        # Create a new DFA
        dfa = Automaton(name=f"{automaton.name}_DFA", 
                        alphabet=Alphabet(automaton.alphabet.symbols))
        
        # Start with the epsilon closure of initial states
        initial_states = automaton.initial_states
        initial_closure = frozenset(ConversionOperations.epsilon_closure(automaton, initial_states))
        
        # Map from set of NFA states to DFA state
        state_map = {}
        
        # Create the initial DFA state
        initial_name = "_".join(sorted(s.name for s in initial_closure)) or "empty"
        is_final = any(s.is_final for s in initial_closure)
        initial_dfa_state = State(initial_name, is_initial=True, is_final=is_final)
        
        dfa.add_state(initial_dfa_state)
        state_map[initial_closure] = initial_dfa_state
        
        # Process queue of state sets
        queue = [initial_closure]
        processed = set()
        
        while queue:
            current_states = queue.pop(0)
            if current_states in processed:
                continue
                
            processed.add(current_states)
            current_dfa_state = state_map[current_states]
            
            # For each symbol in the alphabet
            for symbol in automaton.alphabet.symbols:
                next_states = set()
                
                # Get all states reachable via this symbol from any state in current set
                for state in current_states:
                    for transition in automaton.get_transitions_from(state, symbol):
                        target = transition.target_state
                        # Include epsilon closure of the target
                        next_states.update(ConversionOperations.epsilon_closure(automaton, [target]))
                
                if not next_states:
                    continue
                
                next_states_frozen = frozenset(next_states)
                
                # Create a new DFA state if needed
                if next_states_frozen not in state_map:
                    next_name = "_".join(sorted(s.name for s in next_states)) or "empty"
                    next_is_final = any(s.is_final for s in next_states)
                    next_dfa_state = State(next_name, is_final=next_is_final)
                    
                    dfa.add_state(next_dfa_state)
                    state_map[next_states_frozen] = next_dfa_state
                    queue.append(next_states_frozen)
                    dfa.add_transition(current_dfa_state, symbol, state_map[next_states_frozen])
                    
        return dfa