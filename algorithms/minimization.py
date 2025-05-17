class MinimizationOperations:
    """
    Operations for minimizing automata.
    """
    
    @staticmethod
    def is_minimal(automaton):
        """
        Check if an automaton is minimal.
        
        An automaton is minimal if:
        1. It is deterministic and complete
        2. All states are accessible from initial states
        3. No two distinct states are equivalent
        
        Args:
            automaton: The automaton to check
            
        Returns:
            bool: True if minimal, False otherwise
        """
        from algorithms.deterministic import DeterministicOperations
        
        # Check if deterministic and complete
        if not DeterministicOperations.is_deterministic(automaton):
            return False
        
        # Remove unreachable states and check if the result equals original
        trimmed = MinimizationOperations.remove_unreachable_states(automaton)
        if len(trimmed.states) < len(automaton.states):
            return False
        
        # Minimize the automaton and check if it has the same number of states
        minimized = MinimizationOperations.minimize(automaton)
        
        return len(minimized.states) == len(automaton.states)
    
    @staticmethod
    def remove_unreachable_states(automaton):
        """
        Remove states that cannot be reached from any initial state.
        
        Args:
            automaton: The automaton to process
            
        Returns:
            Automaton: A new automaton with only reachable states
        """
        # Create a copy to avoid modifying the original
        result = automaton.copy()
        
        # Find reachable states using BFS
        reachable = set()
        queue = list(result.initial_states)
        
        while queue:
            state = queue.pop(0)
            if state in reachable:
                continue
            
            reachable.add(state)
            
            # Add all states reachable via transitions
            for transition in result.get_transitions_from(state):
                if transition.target_state not in reachable:
                    queue.append(transition.target_state)
        
        # Remove unreachable states
        for state in list(result.states):
            if state not in reachable:
                result.remove_state(state)
        
        return result
    
    @staticmethod
    def minimize(automaton):
        """
        Minimize a deterministic finite automaton using Hopcroft's algorithm.
        
        Args:
            automaton: The automaton to minimize
            
        Returns:
            Automaton: A minimal DFA equivalent to the input
        """
        from models.automaton import Automaton
        from models.state import State
        from algorithms.deterministic import DeterministicOperations
        
        # First ensure the automaton is a DFA and complete
        if not DeterministicOperations.is_deterministic(automaton):
            from algorithms.conversion import ConversionOperations
            automaton = ConversionOperations.nfa_to_dfa(automaton)
        
        if not DeterministicOperations.is_complete(automaton):
            automaton = DeterministicOperations.complete_automaton(automaton)
        
        # Remove unreachable states
        automaton = MinimizationOperations.remove_unreachable_states(automaton)
        
        # Initial partition: {final states, non-final states}
        final_states = set(automaton.final_states)
        non_final_states = set(automaton.states) - final_states
        
        # Start with P = {F, Q-F} if both sets are non-empty
        partition = []
        if final_states:
            partition.append(frozenset(final_states))
        if non_final_states:
            partition.append(frozenset(non_final_states))
        
        # Initialize worklist with the sets in the partition
        worklist = list(partition)
        
        # Refine partition until no more refinements are possible
        while worklist:
            A = worklist.pop(0)
            
            # For each symbol in the alphabet
            for symbol in automaton.alphabet.symbols:
                # Find X = {states that have a transition to a state in A via symbol}
                X = set()
                for state in automaton.states:
                    targets = automaton.get_reachable_states(state, symbol)
                    if any(target in A for target in targets):
                        X.add(state)
                
                # Refine each set in the partition
                new_partition = []
                for Y in partition:
                    # Compute Y ∩ X and Y - X
                    Y_intersect_X = Y.intersection(X)
                    Y_minus_X = Y.difference(X)
                    
                    # If Y is split by X, replace Y with the two parts
                    if Y_intersect_X and Y_minus_X:
                        new_partition.append(frozenset(Y_intersect_X))
                        new_partition.append(frozenset(Y_minus_X))
                        
                        # Update worklist
                        if Y in worklist:
                            worklist.remove(Y)
                            worklist.append(frozenset(Y_intersect_X))
                            worklist.append(frozenset(Y_minus_X))
                        else:
                            if len(Y_intersect_X) <= len(Y_minus_X):
                                worklist.append(frozenset(Y_intersect_X))
                            else:
                                worklist.append(frozenset(Y_minus_X))
                    else:
                        # Y is not split, keep it unchanged
                        new_partition.append(Y)
                
                partition = new_partition
        
        # Create minimized automaton
        minimized = Automaton(name=f"{automaton.name}_min")
        minimized.alphabet = automaton.alphabet
        
        # Map from equivalence class to new state
        class_to_state = {}
        
        # Create states for each equivalence class
        for equiv_class in partition:
            # Use the name of the first state
            representative = next(iter(equiv_class))
            class_name = representative.name
            
            # Check if any state in this class is initial or final
            is_initial = any(state.is_initial for state in equiv_class)
            is_final = any(state.is_final for state in equiv_class)
            
            # Create the new state
            new_state = State(class_name, is_initial=is_initial, is_final=is_final)
            minimized.add_state(new_state)
            class_to_state[frozenset(equiv_class)] = new_state
        
        # Add transitions between equivalence classes
        for equiv_class, state in class_to_state.items():
            # Use the first state in the class to determine transitions
            representative = next(iter(equiv_class))
            
            for symbol in automaton.alphabet.symbols:
                targets = automaton.get_reachable_states(representative, symbol)
                if targets:
                    target = targets[0]  # There should be only one in a DFA
                    
                    # Find which equivalence class contains the target
                    for target_class in partition:
                        if target in target_class:
                            target_state = class_to_state[frozenset(target_class)]
                            minimized.add_transition(state, symbol, target_state)
                            break
        
        return minimized