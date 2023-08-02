Name - Chinmay Negi

Roll No - 20CS01011

# Conversion from Regex to DFA

One script converts a regular expression (regex) into a Non-Deterministic Finite Automaton (NFA) and saves the NFA in JSON format. It also generates a graph representation of the NFA using Graphviz. Then another script converts epsilon NFA to NFA. Third one converts NFA to DFA and we also first simplify the nfa by removing dead states. Finally we also have a simulator to check if string belong in regex.

## Commands

To install library for getting graph

```bash
  pip install graphviz
```

To convert regex to epsilon nfa

```bash
  python3 regexToEnfa.py output.json
```

Note that while generating output.json it converts epsilon to \u03b5 as epsilon symbol gets converted to escape format in json. But while reading in python it will automatically convert to epsilon.

To convert epsilon nfa to nfa

```bash
  python3 EnfatoNfa.py output.json final.json
```

To convert epsilon nfa to dfa

```bash
  python3 NfaToDfa.py final.json dfa.json
```

For running simulator

```bash
  python3 simulator.py
```

## Screenshots

![App Screenshot](https://drive.google.com/uc?export=view&id=1FGmZ3PwHf9cfNvDQSc9NJs2LV-6vYneV)
epsilon-NFA for _a+b_

![App Screenshot](https://drive.google.com/uc?export=view&id=1LaINOhHhHkgSNZ-HvzOr00TUJEaemHId)
NFA for _a+b_

![App Screenshot](https://drive.google.com/uc?export=view&id=1aIHDQyG1MHAE1NpQKt4PV6nfBoTNp5X2)
Simplified-NFA for _a+b_

![App Screenshot](https://drive.google.com/uc?export=view&id=11ek4jeVntD_Lu8pXZNvBD1zaI_05SM6h)
DFA for _a+b_

![App Screenshot](https://drive.google.com/uc?export=view&id=1mN_g8sDw4I6Q_X89Fe2iWucve6kC7sXv)
Simulator

Json file will also get automatically generated along with this while running the code which contains transitions.
