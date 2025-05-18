# Finite Automata Manager

![Finite Automata Manager](https://img.shields.io/badge/Version-1.0-blue)
![Python](https://img.shields.io/badge/Python-3.x-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

A comprehensive Python application for creating, visualizing, and analyzing finite automata (DFA and NFA). Perfect for educational purposes and theoretical computer science explorations.

![Screenshot of Finite Automata Manager](screenshots/main_screenshot.png)

## 🌟 Features

### Core Functionality
- Create and edit both **Deterministic** and **Non-deterministic** Finite Automata
- Save, load, and manage automata through an intuitive GUI
- Visualize automata as interactive graphs

### Analysis Tools
- Check if an automaton is deterministic
- Convert NFAs to DFAs (Subset Construction Algorithm)
- Verify and complete automata
- Check minimality and minimize automata (Hopcroft's Algorithm)

### Advanced Language Operations
- Test if a word is accepted by an automaton
- Generate all accepted/rejected words up to a given length
- Simulate word processing with animated visualization
- Perform set operations (union, intersection, complement)
- Test equivalence between automata

### Enhanced Visualization
- Interactive graph manipulation with draggable states
- Custom styling options for state colors and sizes
- Animation of word processing with step-by-step visualization
- Export diagrams as PNG, JPG, SVG, or PDF

## 📋 Requirements

- Python 3.x
- Required packages:
  - matplotlib
  - networkx
  - tkinter (usually comes with Python)

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/automata_project.git
   cd automata_project
    ```
2. Install the required dependencies:
    ```bash 
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    python main.py
    ````

## 📖 Usage Examples

## 📖 Usage Examples

### Creating a Simple DFA
1. Start the application and click "Create New Automaton"
2. Give it a name like "EvenBinaryNumbers"
3. Add states:
    - q0 (initial, final) for even numbers
    - q1 (normal) for odd numbers
4. Add alphabet symbols: 0, 1
5. Add transitions:
    - q0 --0--> q0
    - q0 --1--> q1
    - q1 --0--> q0
    - q1 --1--> q1
6. Save the automaton
7. Test with input strings: "0" (accept), "1" (reject), "10" (accept)

### NFA to DFA Conversion
1. Create an NFA with epsilon transitions
2. Use Analysis -> Convert NFA to DFA
3. Compare the resulting DFA's behavior with the original NFA

### Word Processing Animation
1. Create or open an automaton
2. Click "Simulate Word" on the Visualization tab
3. Enter a word and adjust animation speed
4. Watch as the system processes the input step by step

## 🔍 Project Structure

```
automata_project/
├── models/               # Core data models
│   ├── state.py          # State representation
│   ├── alphabet.py       # Alphabet management
│   ├── transition.py     # Transition representation
│   └── automaton.py      # Main automaton class
├── algorithms/           # Algorithmic operations
│   ├── deterministic.py  # DFA-related operations
│   ├── conversion.py     # NFA to DFA conversion
│   ├── completion.py     # Automaton completion
│   ├── minimization.py   # Minimization algorithms
│   └── language_ops.py   # Language operations
├── gui/                  # User interface components
│   ├── main_window.py    # Main application window
│   ├── automaton_editor.py  # Automaton editing interface
│   ├── visualization.py  # Visualization components
│   └── dialogs.py        # Dialog boxes
├── utils/                # Utility functions
│   ├── file_manager.py   # File operations
│   └── helpers.py        # Helper functions
├── automata/             # Directory for saved automata
├── main.py               # Application entry point
└── requirements.txt      # Required dependencies
```

## 🧮 Algorithms
The application implements several key algorithms from automata theory:

| Algorithm | Description | Implementation |
|-----------|-------------|----------------|
| Subset Construction | Converts an NFA to an equivalent DFA | algorithms/conversion.py |
| Hopcroft's Algorithm | Minimizes a DFA efficiently | algorithms/minimization.py |
| Epsilon Closure | Computes states reachable via epsilon transitions | algorithms/conversion.py |
| Word Recognition | Simulates automaton execution on input | algorithms/language_ops.py |
| Set Operations | Computes union, intersection, complement | algorithms/language_ops.py |

## 📈 Future Enhancements
- Regular Expression ↔ Automaton conversion
- Pushdown automata support
- Context-free grammar integration
- Turing machine simulation
- Cloud storage integration
- Collaborative editing
- Mobile app version

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


