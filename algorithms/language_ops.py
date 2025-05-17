class LanguageOperations:
    """
    Operations for manipulating languages recognized by automata.
    """
    
    @staticmethod
    def accepts_word(automaton, word):
        """
        Check if an automaton accepts a given word.
        
        Args:
            automaton: The automaton to check
            word (str): The word to test
            
        Returns:
            bool: True if the automaton accepts the word, False otherwise
        """
        from algorithms.deterministic import DeterministicOperations
        
        # For DFA, follow the transitions directly
        if DeterministicOperations.is_deterministic(automaton):
            current_state = automaton.initial_states[0]
            
            for symbol in word:
                if symbol not in automaton.alphabet.symbols:
                    return False
                
                next_states = automaton.get_reachable_states(current_state, symbol)
                if not next_states:
                    return False
                
                # In a DFA, there should be exactly one next state
                current_state = next_states[0]
            
            return current_state.is_final
        
        # For NFA, compute all possible states after reading the word
        else:
            from algorithms.conversion import ConversionOperations
            
            # Start with the epsilon closure of initial states
            current_states = set(ConversionOperations.epsilon_closure(
                automaton, automaton.initial_states))
            
            # Process each symbol in the word
            for symbol in word:
                if symbol not in automaton.alphabet.symbols:
                    return False
                
                next_states = set()
                for state in current_states:
                    # Get states reachable via this symbol
                    targets = automaton.get_reachable_states(state, symbol)
                    for target in targets:
                        # Include epsilon closure of each target
                        next_states.update(ConversionOperations.epsilon_closure(
                            automaton, [target]))
                
                if not next_states:
                    return False
                
                current_states = next_states
            
            # Check if any current state is final
            return any(state.is_final for state in current_states)
    
    @staticmethod
    def generate_words(automaton, max_length, accepted=True):
        """
        Generate all words up to a given length that are accepted or rejected by the automaton.
        
        Args:
            automaton: The automaton
            max_length (int): Maximum length of words to generate
            accepted (bool): If True, generate accepted words; if False, generate rejected words
            
        Returns:
            list: List of generated words
        """
        # Convert to DFA for easier word generation
        from algorithms.deterministic import DeterministicOperations
        from algorithms.conversion import ConversionOperations
        
        if not DeterministicOperations.is_deterministic(automaton):
            dfa = ConversionOperations.nfa_to_dfa(automaton)
        else:
            dfa = automaton
        
        # Get all words up to max_length using BFS
        all_words = []
        for length in range(max_length + 1):
            all_words.extend(LanguageOperations._generate_words_of_length(
                dfa.alphabet.symbols, length))
        
        # Filter words based on acceptance
        result = []
        for word in all_words:
            if LanguageOperations.accepts_word(dfa, word) == accepted:
                result.append(word)
        
        return result
    
    @staticmethod
    def _generate_words_of_length(alphabet, length):
        """
        Generate all possible words of a given length from an alphabet.
        
        Args:
            alphabet (set): Set of symbols
            length (int): Length of words to generate
            
        Returns:
            list: List of all words of the given length
        """
        if length == 0:
            return ['']
        
        shorter_words = LanguageOperations._generate_words_of_length(alphabet, length - 1)
        result = []
        
        for word in shorter_words:
            for symbol in sorted(alphabet):
                result.append(word + symbol)
        
        return result
    
    @staticmethod
    def are_equivalent(automaton1, automaton2):
        """
        Check if two automata recognize the same language.
        
        Args:
            automaton1: First automaton
            automaton2: Second automaton
            
        Returns:
            bool: True if the automata are equivalent, False otherwise
        """
        # Convert both to minimal DFAs
        from algorithms.conversion import ConversionOperations
        from algorithms.minimization import MinimizationOperations
        
        dfa1 = ConversionOperations.nfa_to_dfa(automaton1)
        dfa2 = ConversionOperations.nfa_to_dfa(automaton2)
        
        min1 = MinimizationOperations.minimize(dfa1)
        min2 = MinimizationOperations.minimize(dfa2)
        
        # Check structural equivalence of the minimal DFAs
        # This is a simplified approach - a more robust method would be to build
        # a product automaton and check for the emptiness of the symmetric difference
        
        # Check if they have the same number of states
        if len(min1.states) != len(min2.states):
            return False
        
        # Check if they have the same number of final states
        if len(min1.final_states) != len(min2.final_states):
            return False
        
        # Try to establish a bijection between states
        # Start with the initial states
        if len(min1.initial_states) != 1 or len(min2.initial_states) != 1:
            return False
        
        state_map = {min1.initial_states[0]: min2.initial_states[0]}
        queue = [(min1.initial_states[0], min2.initial_states[0])]
        visited = set()
        
        while queue:
            state1, state2 = queue.pop(0)
            if (state1, state2) in visited:
                continue
            
            visited.add((state1, state2))
            
            # Check if both states agree on being final
            if state1.is_final != state2.is_final:
                return False
            
            # Check transitions
            for symbol in min1.alphabet.symbols:
                next1 = min1.get_reachable_states(state1, symbol)
                next2 = min2.get_reachable_states(state2, symbol)
                
                # In a minimal DFA, each state should have exactly one transition per symbol
                if len(next1) != 1 or len(next2) != 1:
                    return False
                
                next_state1 = next1[0]
                next_state2 = next2[0]
                
                # If we've seen state1 before, it should map to the same state2
                if next_state1 in state_map and state_map[next_state1] != next_state2:
                    return False
                
                # Update mapping and queue
                if next_state1 not in state_map:
                    state_map[next_state1] = next_state2
                    queue.append((next_state1, next_state2))
        
        # Ensure all states are mapped
        return len(state_map) == len(min1.states)
    
    @staticmethod
    def union(automaton1, automaton2):
        """
        Compute the union of two automata.
        
        The union automaton accepts a word if either automaton1 or automaton2 accepts it.
        
        Args:
            automaton1: First automaton
            automaton2: Second automaton
            
        Returns:
            Automaton: A new automaton representing the union
        """
        from models.automaton import Automaton
        from models.state import State
        from models.alphabet import Alphabet
        
        # Convert both to DFAs
        from algorithms.conversion import ConversionOperations
        
        dfa1 = ConversionOperations.nfa_to_dfa(automaton1)
        dfa2 = ConversionOperations.nfa_to_dfa(automaton2)
        
        # Create a new automaton for the union
        union = Automaton(name=f"{dfa1.name}_union_{dfa2.name}")
        
        # Combine alphabets
        combined_alphabet = set(dfa1.alphabet.symbols).union(set(dfa2.alphabet.symbols))
        union.alphabet = Alphabet(combined_alphabet)
        
        # Create product states
        state_map = {}  # Maps (state1, state2) to combined state
        
        # Create initial state from initial states of both DFAs
        initial1 = dfa1.initial_states[0]
        initial2 = dfa2.initial_states[0]
        
        initial_name = f"{initial1.name}_{initial2.name}"
        is_final = initial1.is_final or initial2.is_final
        initial_state = State(initial_name, is_initial=True, is_final=is_final)
        
        union.add_state(initial_state)
        state_map[(initial1, initial2)] = initial_state
        
        # Process product states
        queue = [(initial1, initial2)]
        visited = set()
        
        while queue:
            state1, state2 = queue.pop(0)
            if (state1, state2) in visited:
                continue
                
            visited.add((state1, state2))
            current_state = state_map[(state1, state2)]
            
            # For each symbol in the combined alphabet
            for symbol in union.alphabet.symbols:
                # Get next states in both automata
                next1 = dfa1.get_reachable_states(state1, symbol) if symbol in dfa1.alphabet.symbols else []
                next2 = dfa2.get_reachable_states(state2, symbol) if symbol in dfa2.alphabet.symbols else []
                
                # Use sink state if no transition is defined
                next1 = next1 if next1 else [None]
                next2 = next2 if next2 else [None]
                
                # There should be at most one next state in each DFA
                next_state1 = next1[0] if next1 else None
                next_state2 = next2[0] if next2 else None
                
                # Skip if both are None
                if next_state1 is None and next_state2 is None:
                    continue
                
                # Create product state name
                next_name = f"{next_state1.name if next_state1 else 'sink'}_{next_state2.name if next_state2 else 'sink'}"
                is_final = (next_state1 and next_state1.is_final) or (next_state2 and next_state2.is_final)
                
                # Create or get the product state
                if (next_state1, next_state2) not in state_map:
                    next_product = State(next_name, is_final=is_final)
                    union.add_state(next_product)
                    state_map[(next_state1, next_state2)] = next_product
                    queue.append((next_state1, next_state2))
                
                # Add transition
                union.add_transition(current_state, symbol, state_map[(next_state1, next_state2)])
        
        return union
    
    @staticmethod
    def intersection(automaton1, automaton2):
        """
        Compute the intersection of two automata.
        
        The intersection automaton accepts a word if both automaton1 and automaton2 accept it.
        
        Args:
            automaton1: First automaton
            automaton2: Second automaton
            
        Returns:
            Automaton: A new automaton representing the intersection
        """
        from models.automaton import Automaton
        from models.state import State
        from models.alphabet import Alphabet
        
        # Convert both to DFAs
        from algorithms.conversion import ConversionOperations
        
        dfa1 = ConversionOperations.nfa_to_dfa(automaton1)
        dfa2 = ConversionOperations.nfa_to_dfa(automaton2)
        
        # Create a new automaton for the intersection
        intersection = Automaton(name=f"{dfa1.name}_intersect_{dfa2.name}")
        
        # Combine alphabets - intersection accepts only symbols in both alphabets
        combined_alphabet = set(dfa1.alphabet.symbols).intersection(set(dfa2.alphabet.symbols))
        intersection.alphabet = Alphabet(combined_alphabet)
        
        # If alphabets have no common symbols, the intersection is empty
        if not combined_alphabet:
            return intersection
        
        # Create product states
        state_map = {}  # Maps (state1, state2) to combined state
        
        # Create initial state from initial states of both DFAs
        initial1 = dfa1.initial_states[0]
        initial2 = dfa2.initial_states[0]
        
        initial_name = f"{initial1.name}_{initial2.name}"
        is_final = initial1.is_final and initial2.is_final
        initial_state = State(initial_name, is_initial=True, is_final=is_final)
        intersection.add_state(initial_state)
        state_map[(initial1, initial2)] = initial_state
        
        # Process product states
        queue = [(initial1, initial2)]
        visited = set()
        
        while queue:
            state1, state2 = queue.pop(0)
            if (state1, state2) in visited:
                continue
                
            visited.add((state1, state2))
            current_state = state_map[(state1, state2)]
            
            # For each symbol in the combined alphabet
            for symbol in intersection.alphabet.symbols:
                # Get next states in both automata
                next1 = dfa1.get_reachable_states(state1, symbol)
                next2 = dfa2.get_reachable_states(state2, symbol)
                
                # There should be at most one next state in each DFA
                if next1 and next2:
                    next_state1 = next1[0]
                    next_state2 = next2[0]
                    
                    # Create product state name
                    next_name = f"{next_state1.name}_{next_state2.name}"
                    is_final = next_state1.is_final and next_state2.is_final
                    
                    # Create or get the product state
                    if (next_state1, next_state2) not in state_map:
                        next_product = State(next_name, is_final=is_final)
                        intersection.add_state(next_product)
                        state_map[(next_state1, next_state2)] = next_product
                        queue.append((next_state1, next_state2))
                    
                    # Add transition
                    intersection.add_transition(current_state, symbol, state_map[(next_state1, next_state2)])
        
        return intersection
    
    @staticmethod
    def complement(automaton):
        """
        Compute the complement of an automaton.
        
        The complement automaton accepts a word if the original automaton rejects it.
        
        Args:
            automaton: The automaton to complement
            
        Returns:
            Automaton: A new automaton representing the complement
        """
        from models.automaton import Automaton
        from algorithms.deterministic import DeterministicOperations
        from algorithms.conversion import ConversionOperations
        
        # Convert to a complete DFA
        if not DeterministicOperations.is_deterministic(automaton):
            dfa = ConversionOperations.nfa_to_dfa(automaton)
        else:
            dfa = automaton.copy()
        
        if not DeterministicOperations.is_complete(dfa):
            dfa = DeterministicOperations.complete_automaton(dfa)
        
        # Create the complement by flipping the acceptance of all states
        complement = dfa.copy()
        complement.name = f"{automaton.name}_complement"
        
        for state in complement.states:
            state.is_final = not state.is_final
        
        return complement