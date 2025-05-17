def format_transition_string(transition):
    """
    Format a transition for display.
    
    Args:
        transition: Transition to format
        
    Returns:
        str: Formatted string representation
    """
    return f"{transition.source_state.name} --{transition.symbol}--> {transition.target_state.name}"

def find_unreachable_states(automaton):
    """
    Find states that cannot be reached from any initial state.
    
    Args:
        automaton: The automaton to analyze
        
    Returns:
        set: Set of unreachable states
    """
    # Set of all states
    all_states = set(automaton.states)
    
    # Set of reachable states
    reachable = set()
    
    # Queue for BFS
    queue = list(automaton.initial_states)
    
    # BFS to find all reachable states
    while queue:
        state = queue.pop(0)
        if state in reachable:
            continue
            
        reachable.add(state)
        
        # Add all states reachable via transitions
        for transition in automaton.get_transitions_from(state):
            if transition.target_state not in reachable:
                queue.append(transition.target_state)
    
    # Return the set difference: all states minus reachable states
    return all_states - reachable

def find_nondeterministic_transitions(automaton):
    """
    Find transitions that make an automaton non-deterministic.
    
    Args:
        automaton: The automaton to analyze
        
    Returns:
        list: List of tuples (state, symbol, [target_states]) indicating non-determinism
    """
    result = []
    
    # Check for multiple initial states
    if len(automaton.initial_states) > 1:
        result.append(("multiple_initial", None, automaton.initial_states))
    
    # Check for epsilon transitions
    epsilon_transitions = []
    for transition in automaton.transitions:
        if transition.symbol == automaton.alphabet.epsilon:
            epsilon_transitions.append(transition)
    
    if epsilon_transitions:
        result.append(("epsilon", automaton.alphabet.epsilon, epsilon_transitions))
    
    # Check for multiple transitions with the same symbol
    for state in automaton.states:
        for symbol in automaton.alphabet.symbols:
            targets = automaton.get_reachable_states(state, symbol)
            if len(targets) > 1:
                result.append((state, symbol, targets))
    
    return result

def validate_automaton_name(name):
    """
    Validate that an automaton name is acceptable.
    
    Args:
        name: Name to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not name:
        return False, "Name cannot be empty"
    
    if len(name) > 50:
        return False, "Name is too long (max 50 characters)"
    
    # Check for invalid characters
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', ' ']
    for char in invalid_chars:
        if char in name:
            return False, f"Name cannot contain the character '{char}'"
    
    return True, ""

def generate_unique_name(base_name, existing_names):
    """
    Generate a unique name based on a base name.
    
    Args:
        base_name: Base name to start with
        existing_names: List of existing names to avoid
        
    Returns:
        str: A unique name
    """
    if base_name not in existing_names:
        return base_name
    
    counter = 1
    while f"{base_name}_{counter}" in existing_names:
        counter += 1
    
    return f"{base_name}_{counter}"

def simplify_state_names(automaton):
    """
    Simplify state names in an automaton to q0, q1, q2, etc.
    
    This is useful after operations like subset construction that create
    complex state names.
    
    Args:
        automaton: The automaton to simplify
        
    Returns:
        Automaton: A new automaton with simplified state names
    """
    from models.automaton import Automaton
    from models.state import State
    
    result = Automaton(name=automaton.name)
    result.alphabet = automaton.alphabet
    
    # Create mapping from old state to new state
    state_map = {}
    
    # Create new states with simplified names
    for i, old_state in enumerate(automaton.states):
        new_name = f"q{i}"
        new_state = State(
            name=new_name,
            is_initial=old_state.is_initial,
            is_final=old_state.is_final
        )
        result.add_state(new_state)
        state_map[old_state] = new_state
    
    # Create transitions using the new states
    for transition in automaton.transitions:
        source = state_map[transition.source_state]
        target = state_map[transition.target_state]
        result.add_transition(source, transition.symbol, target)
    
    return result